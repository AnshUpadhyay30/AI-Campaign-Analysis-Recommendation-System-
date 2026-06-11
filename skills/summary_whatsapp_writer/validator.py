from __future__ import annotations

def validate(payload: dict[str, object]) -> list[str]:
    if not isinstance(payload, dict):
        return ["payload must be an object"]
    return []
