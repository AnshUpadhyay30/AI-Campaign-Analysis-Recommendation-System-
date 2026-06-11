from __future__ import annotations

from src.agents.base import Agent
from src.common.contracts import AgentOutput


class DataQualityAgent(Agent):
    name = "data_quality"

    def run(self, context: dict[str, object]) -> AgentOutput:
        summary = context.get("kpi_summary", {})
        row_count = int(summary.get("row_count", 0))

        findings = []
        risks = []
        evidence = [{"source": "normalized_csv", "row_count": row_count}]

        if row_count == 0:
            risks.append("No rows were ingested for this run.")
        else:
            findings.append(f"Data ingestion returned {row_count} normalized rows.")

        if row_count < 10:
            risks.append("Low row volume may reduce reliability of recommendations.")

        return AgentOutput(findings=findings, risks=risks, evidence=evidence)
