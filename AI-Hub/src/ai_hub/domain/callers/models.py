from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CallerRegistration:
    caller_id: str
    display_name: str
    scopes: frozenset[str]
    enabled: bool = True

    def __post_init__(self) -> None:
        if not self.caller_id.strip() or not self.display_name.strip():
            raise ValueError("caller identity is required")
        if not self.scopes:
            raise ValueError("at least one caller scope is required")
