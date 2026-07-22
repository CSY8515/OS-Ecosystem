from ai_hub.domain.providers import InferenceRequest, Usage
from ai_hub.infrastructure.providers.shared import attribute


def map_input(request: InferenceRequest) -> str:
    return "\n\n".join(f"{item.role.upper()}: {item.content}" for item in request.messages)


def map_usage(response) -> Usage:
    usage = attribute(response, "usage_metadata") or attribute(response, "usage")
    input_units = attribute(usage, "prompt_token_count") or attribute(usage, "input_tokens")
    output_units = attribute(usage, "candidates_token_count") or attribute(usage, "output_tokens")
    total_units = attribute(usage, "total_token_count") or attribute(usage, "total_tokens")
    return Usage(input_units, output_units, total_units)
