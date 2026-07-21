"""Small, deterministic data-shaping operations; business logic stays with projects."""

from typing import Any

from .models import TransformationResult, TransformationRule

_TYPE_CONVERTERS = {"str": str, "int": int, "float": float, "bool": bool}


def transform_record(record: dict[str, Any], rules: tuple[TransformationRule, ...]) -> TransformationResult:
    output = dict(record)
    applied = 0
    try:
        for rule in rules:
            operation = rule.operation.lower()
            if operation in {"map", "rename"}:
                if not rule.source or not rule.target:
                    raise ValueError("map/rename requires source and target")
                if rule.source in output:
                    output[rule.target] = output.pop(rule.source)
            elif operation == "include":
                fields = set(rule.value or ())
                output = {key: value for key, value in output.items() if key in fields}
            elif operation == "exclude":
                for field_name in rule.value or ():
                    output.pop(str(field_name), None)
            elif operation == "default":
                if not rule.target:
                    raise ValueError("default requires target")
                output.setdefault(rule.target, rule.value)
            elif operation == "convert":
                field_name = rule.target or rule.source
                converter = _TYPE_CONVERTERS.get(str(rule.target_type).lower())
                if not field_name or converter is None:
                    raise ValueError("convert requires a field and supported target_type")
                if field_name in output:
                    output[field_name] = converter(output[field_name])
            elif operation == "metadata":
                metadata = dict(output.get("metadata") or {})
                metadata[str(rule.target)] = rule.value
                output["metadata"] = metadata
            else:
                raise ValueError(f"unsupported transformation: {rule.operation}")
            applied += 1
        return TransformationResult(True, output, applied)
    except (TypeError, ValueError) as exc:
        return TransformationResult(False, output, applied, (str(exc),))
