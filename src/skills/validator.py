from __future__ import annotations

from src.common.contracts import AgentOutput


def validate_agent_output(output: AgentOutput) -> list[str]:
    errors: list[str] = []
    for rec in output.recommendations:
        if not (0.0 <= rec.confidence <= 1.0):
            errors.append(f"confidence out of range for scope {rec.scope_id}")
        if not rec.action:
            errors.append("recommendation action missing")
        if not rec.rationale:
            errors.append("recommendation rationale missing")
    return errors
