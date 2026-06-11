from __future__ import annotations

from src.agents.base import Agent
from src.common.contracts import AgentOutput, AgentRecommendation


class CreativeIntelligenceAgent(Agent):
    name = "creative_intelligence"

    def run(self, context: dict[str, object]) -> AgentOutput:
        summary = context.get("kpi_summary", {})
        totals = summary.get("totals", {})
        ctr = float(totals.get("ctr", 0.0))
        cvr = float(totals.get("cvr", 0.0))

        findings = []
        recommendations = []
        risks = []

        if ctr < 1.0:
            findings.append("Account-level CTR is below 1.0%; creative-message resonance may be weak.")
            recommendations.append(
                AgentRecommendation(
                    action="test_creative_hooks",
                    scope_id="creative_portfolio",
                    rationale="Low CTR suggests need for stronger first-frame hooks and offer clarity.",
                    confidence=0.74,
                    expected_impact="Improve CTR and lower blended CPC over 1-2 test cycles.",
                )
            )

        if cvr < 2.0:
            risks.append("Low CVR indicates landing page or audience-intent mismatch.")
            recommendations.append(
                AgentRecommendation(
                    action="refresh_offer_angle",
                    scope_id="creative_portfolio",
                    rationale="Weak click-to-conversion flow needs tighter offer/intent alignment.",
                    confidence=0.66,
                    expected_impact="Potential improvement in conversion rate and CPA.",
                )
            )

        return AgentOutput(
            findings=findings,
            recommendations=recommendations,
            risks=risks,
            evidence=[{"ctr": ctr, "cvr": cvr}],
        )
