from ai_hub.utilities.redaction import redact_mapping, sanitize_text


def test_redaction_is_recursive_and_does_not_mutate_source() -> None:
    source = {"api_key": "top-secret", "nested": {"authorization": "Bearer abc"}}
    redacted = redact_mapping(source)
    assert redacted == {"api_key": "[REDACTED]", "nested": {"authorization": "[REDACTED]"}}
    assert source["api_key"] == "top-secret"


def test_sanitize_text_removes_bearer_value_and_newlines() -> None:
    assert sanitize_text("failed\nBearer abc.def") == "failed Bearer [REDACTED]"
