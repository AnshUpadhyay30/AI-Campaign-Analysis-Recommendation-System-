from __future__ import annotations

from src.agents.base import Agent
from src.common.contracts import AgentOutput, AgentRecommendation


class BudgetAllocatorAgent(Agent):
    name = "budget_allocator"

    def __init__(self, target_cpa: float = 50.0) -> None:
        self.target_cpa = target_cpa

    def run(self, context: dict[str, object]) -> AgentOutput:
        entities = context.get("kpi_summary", {}).get("entities", [])
        recs = []

        for row in entities[:8]:
            entity = str(row.get("entity", "unknown"))
            cpa = float(row.get("cpa", 0.0))
            if cpa == 0:
                recs.append(
                    AgentRecommendation(
                        action="hold",
                        scope_id=entity,
                        rationale="No conversion signal yet; gather more data before budget changes.",
                        confidence=0.55,
                        expected_impact="Avoid premature budget movement.",
                    )
                )
            elif cpa <= self.target_cpa:
                recs.append(
                    AgentRecommendation(
                        action="scale",
                        scope_id=entity,
                        rationale=f"CPA {cpa:.2f} is at or below target {self.target_cpa:.2f}.",
                        confidence=0.78,
                        expected_impact="Likely efficient incremental conversion volume.",
                    )
                )
            else:
                recs.append(
                    AgentRecommendation(
                        action="reduce",
                        scope_id=entity,
                        rationale=f"CPA {cpa:.2f} is above target {self.target_cpa:.2f}.",
                        confidence=0.76,
                        expected_impact="Lower cost leakage and improve blended efficiency.",
                    )
                )

        return AgentOutput(
            findings=["Budget recommendations generated using CPA guardrail policy."],
            recommendations=recs,
            evidence=[{"target_cpa": self.target_cpa}],
        )
