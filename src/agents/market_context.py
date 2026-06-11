from __future__ import annotations

from datetime import date

from src.agents.base import Agent
from src.common.contracts import AgentOutput


class MarketContextAgent(Agent):
    name = "market_context"

    def run(self, context: dict[str, object]) -> AgentOutput:
        today = date.today().isoformat()
        findings = [
            "Meta automation and structured testing remain central for budget efficiency.",
            "IAB trend narrative indicates continued video and social format pressure on creative quality.",
        ]
        evidence = [
            {"source": "Meta Performance Marketing", "date": today},
            {"source": "IAB industry trends", "date": today},
        ]
        return AgentOutput(findings=findings, evidence=evidence)
