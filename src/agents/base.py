from __future__ import annotations

from src.common.contracts import AgentOutput


class Agent:
    name = "base"

    def run(self, context: dict[str, object]) -> AgentOutput:
        raise NotImplementedError
