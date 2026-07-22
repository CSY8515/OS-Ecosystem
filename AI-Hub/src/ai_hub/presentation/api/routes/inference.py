from ai_hub.application.inference_service import InferenceService


def execute_inference(service: InferenceService, request, candidates, policy, settings):
    """Framework-neutral v0.1 transport handler for Living OS and ULE clients."""
    return service.execute(
        request,
        candidates,
        policy,
        timeout_seconds=settings.timeout_seconds,
        overall_timeout_seconds=settings.overall_timeout_seconds,
    )
