from __future__ import annotations

from src.agents.base import Agent
from src.common.contracts import AgentOutput, AgentRecommendation


class PerformanceDiagnosticsAgent(Agent):
    name = "performance_diagnostics"

    def run(self, context: dict[str, object]) -> AgentOutput:
        summary = context.get("kpi_summary", {})
        top = summary.get("top", [])
        bottom = summary.get("bottom", [])

        findings = []
        recommendations = []
        evidence = []

        for row in top[:3]:
            entity = row.get("entity", "unknown")
            findings.append(f"Top delivery entity: {entity} with spend {row.get('spend', 0):.2f}.")
            recommendations.append(
                AgentRecommendation(
                    action="scale",
                    scope_id=str(entity),
                    rationale="Entity is among top spend leaders with viable efficiency indicators.",
                    confidence=0.68,
                    expected_impact="Potential incremental conversions with controlled budget increase.",
                )
            )
            evidence.append({"entity": entity, "spend": row.get("spend", 0), "cpa": row.get("cpa", 0)})

        for row in bottom[:3]:
            entity = row.get("entity", "unknown")
            recommendations.append(
                AgentRecommendation(
                    action="fix_or_reduce",
                    scope_id=str(entity),
                    rationale="Entity is in the weakest efficiency cohort by CPA.",
                    confidence=0.72,
                    expected_impact="Lower wasted spend and improved blended CPA.",
                )
            )
            evidence.append({"entity": entity, "risk_cpa": row.get("cpa", 0)})

        return AgentOutput(findings=findings, recommendations=recommendations, evidence=evidence)
