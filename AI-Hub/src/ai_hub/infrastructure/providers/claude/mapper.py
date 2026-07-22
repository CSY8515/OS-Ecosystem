from ai_hub.domain.providers import InferenceRequest, Usage
from ai_hub.infrastructure.providers.shared import attribute


def map_messages(request: InferenceRequest) -> tuple[str | None, list[dict[str, str]]]:
    instructions = [item.content for item in request.messages if item.role in {"system", "developer"}]
    messages = [
        {"role": item.role, "content": item.content}
        for item in request.messages
        if item.role in {"user", "assistant"}
    ]
    return ("\n\n".join(instructions) or None), messages


def map_usage(response) -> Usage:
    usage = attribute(response, "usage")
    input_units = attribute(usage, "input_tokens")
    output_units = attribute(usage, "output_tokens")
    total_units = input_units + output_units if input_units is not None and output_units is not None else None
    return Usage(input_units, output_units, total_units)


def map_output(response) -> str:
    blocks = attribute(response, "content", []) or []
    return "".join(str(attribute(block, "text", "")) for block in blocks if attribute(block, "type") == "text")
