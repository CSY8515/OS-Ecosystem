from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import argparse
import json
from pathlib import Path
from time import monotonic

from ai_hub.application.api_management_service import APIManagementService
from ai_hub.application.health_service import HealthService
from ai_hub.application.inference_service import InferenceService
from ai_hub.bootstrap.configuration import load_secret_sources
from ai_hub.domain.callers import CallerRegistration
from ai_hub.domain.health import HealthRegistry, HealthState
from ai_hub.domain.providers import (
    InferenceRequest,
    Message,
    ModelRegistration,
    ProviderFamily,
    ProviderRegistration,
)
from ai_hub.domain.router import Router, RoutingCandidate, RoutingPolicy
from ai_hub.infrastructure.persistence import SQLiteExecutionRepository
from ai_hub.infrastructure.providers.claude import ClaudeAdapter
from ai_hub.infrastructure.providers.gemini import GeminiAdapter
from ai_hub.infrastructure.providers.openai import OpenAIAdapter
from ai_hub.infrastructure.secrets import EnvironmentSecretResolver


@dataclass(frozen=True, slots=True)
class ReleaseProviderSpec:
    family: ProviderFamily
    display_name: str
    key_names: tuple[str, ...]
    model_name: str


SPECS = (
    ReleaseProviderSpec(ProviderFamily.OPENAI, "OpenAI", ("AI_HUB_OPENAI_API_KEY", "OPENAI_API_KEY"), "AI_HUB_OPENAI_MODEL"),
    ReleaseProviderSpec(ProviderFamily.GEMINI, "Google Gemini", ("AI_HUB_GEMINI_API_KEY", "GEMINI_API_KEY", "GOOGLE_API_KEY"), "AI_HUB_GEMINI_MODEL"),
    ReleaseProviderSpec(ProviderFamily.CLAUDE, "Anthropic Claude", ("AI_HUB_CLAUDE_API_KEY", "ANTHROPIC_API_KEY", "CLAUDE_API_KEY"), "AI_HUB_CLAUDE_MODEL"),
)


def _first_present(values: dict[str, str], names: tuple[str, ...]) -> str | None:
    return next((name for name in names if values.get(name, "").strip()), None)


def build_preflight_report(values: dict[str, str]) -> dict:
    providers = []
    keys_ready = True
    models_ready = True
    for spec in SPECS:
        key_reference = _first_present(values, spec.key_names)
        model = values.get(spec.model_name, "").strip()
        provider_ready = bool(key_reference and model)
        keys_ready = keys_ready and bool(key_reference)
        models_ready = models_ready and bool(model)
        providers.append({
            "provider": spec.display_name,
            "key_reference": key_reference,
            "key_present": bool(key_reference),
            "model_setting": spec.model_name,
            "model_configured": bool(model),
            "ready": provider_ready,
        })
    return {
        "ready": keys_ready and models_ready,
        "keys_ready": keys_ready,
        "models_ready": models_ready,
        "providers": providers,
    }


def run_live(project_root: Path, values: dict[str, str]) -> dict:
    preflight = build_preflight_report(values)
    if not preflight["keys_ready"]:
        return {"success": False, "stage": "preflight", **preflight}

    adapters = {
        ProviderFamily.OPENAI: OpenAIAdapter(),
        ProviderFamily.GEMINI: GeminiAdapter(),
        ProviderFamily.CLAUDE: ClaudeAdapter(),
    }
    provider_reports = []
    candidates = []
    registry = HealthRegistry()
    health_service = HealthService(registry)
    registrations = []

    for spec in SPECS:
        key_reference = _first_present(values, spec.key_names)
        assert key_reference is not None
        credential = values[key_reference]
        configured_model = values[spec.model_name].strip()
        adapter = adapters[spec.family]
        list_started = monotonic()
        models = adapter.list_models(credential, 20)
        list_duration = round((monotonic() - list_started) * 1000, 3)
        if not configured_model or configured_model not in models:
            provider_reports.append({
                "provider": spec.display_name,
                "success": False,
                "stage": "model_selection_required" if not configured_model else "model_lookup",
                "model_count": len(models),
                "configured_model_available": False,
                "available_models": models[:50],
                "duration_ms": list_duration,
            })
            continue
        provider = ProviderRegistration(str(spec.family), spec.family, spec.display_name, key_reference)
        model = ModelRegistration(
            f"{spec.family}-release", str(spec.family), configured_model,
            frozenset({"generation"}), suitability=0.8, max_output_tokens=1024,
        )
        health = health_service.check(
            provider, model, adapter, credential,
            checked_at=datetime.now(UTC), timeout_seconds=20,
        )
        provider_reports.append({
            "provider": spec.display_name,
            "success": health.state == HealthState.ONLINE,
            "stage": "health",
            "model_count": len(models),
            "configured_model_available": True,
            "model_lookup_duration_ms": list_duration,
            "health": str(health.state),
            "last_check": health.checked_at.isoformat(),
            "response_time_ms": health.response_time_ms,
            "availability": health.availability,
            "error_code": health.error_code,
        })
        if health.state == HealthState.ONLINE:
            candidates.append(RoutingCandidate(provider, model, health))
            registrations.append((spec, provider, model))

    if len(registrations) != len(SPECS):
        return {"success": False, "stage": "provider_validation", "providers": provider_reports}

    repository = SQLiteExecutionRepository(project_root / "data" / "release_validation.sqlite3")
    repository.migrate()
    api_management = APIManagementService()
    api_management.register(CallerRegistration("release-validation", "Release Validation", frozenset({"inference"})))
    inference = InferenceService(
        router=Router(), adapters=adapters,
        secret_resolver=EnvironmentSecretResolver(values),
        execution_repository=repository, api_management=api_management,
        clock=lambda: datetime.now(UTC),
    )

    inference_reports = []
    for spec, provider, model in registrations:
        response = inference.execute(
            InferenceRequest(
                f"release-{spec.family}", "release-validation", "generation",
                (Message("user", "Reply exactly with AI_HUB_OK"),), max_output_tokens=32,
            ),
            tuple(candidate for candidate in candidates if candidate.provider.family == spec.family),
            RoutingPolicy(auto_routing=False, default_provider_id=provider.provider_id, retry_count=0),
            timeout_seconds=20, overall_timeout_seconds=30,
        )
        inference_reports.append({
            "provider": spec.display_name,
            "success": response.success,
            "duration_ms": response.duration_ms,
            "attempt_count": response.attempt_count,
            "error_code": response.error_code,
        })

    automatic = inference.execute(
        InferenceRequest(
            "release-router-auto", "release-validation", "generation",
            (Message("user", "Reply exactly with AI_HUB_ROUTER_OK"),), max_output_tokens=32,
        ),
        tuple(candidates), RoutingPolicy(retry_count=2),
        timeout_seconds=20, overall_timeout_seconds=60,
    )
    records = repository.recent(20)
    return {
        "success": all(item["success"] for item in provider_reports + inference_reports) and automatic.success,
        "stage": "complete",
        "providers": provider_reports,
        "inference": inference_reports,
        "router": {
            "success": automatic.success,
            "selected_provider": automatic.provider_id,
            "duration_ms": automatic.duration_ms,
            "attempt_count": automatic.attempt_count,
            "failover": automatic.failover,
            "error_code": automatic.error_code,
        },
        "execution_log_records": len(records),
        "execution_log_path": str(repository.database_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="AI Hub v0.1 Release provider validation")
    parser.add_argument("--live", action="store_true", help="perform authorized live Provider calls")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.project_root.resolve()
    values = load_secret_sources(root)
    report = run_live(root, values) if args.live else build_preflight_report(values)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report.get("success", report.get("ready", False)) else 2


if __name__ == "__main__":
    raise SystemExit(main())
