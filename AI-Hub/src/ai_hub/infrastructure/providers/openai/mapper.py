from ai_hub.domain.providers import InferenceRequest, Usage
from ai_hub.infrastructure.providers.shared import attribute


def map_input(request: InferenceRequest) -> list[dict[str, str]]:
    return [{"role": "developer" if item.role == "system" else item.role, "content": item.content} for item in request.messages]


def map_usage(response) -> Usage:
    usage = attribute(response, "usage")
    input_units = attribute(usage, "input_tokens")
    output_units = attribute(usage, "output_tokens")
    total_units = attribute(usage, "total_tokens")
    if total_units is None and input_units is not None and output_units is not None:
        total_units = input_units + output_units
    return Usage(input_units, output_units, total_units)
