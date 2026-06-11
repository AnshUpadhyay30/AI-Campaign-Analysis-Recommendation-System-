from __future__ import annotations

import json

from src.agents.base import Agent
from src.agents.claude_client import ClaudeClient
from src.common.contracts import AgentOutput, AgentRecommendation

SYSTEM_PROMPT = """You are a performance marketing analyst.

Return ONLY one valid JSON object.
Do not use markdown.
Do not use triple backticks.
Do not add any explanation before or after the JSON.

Schema:
{
  "findings": ["string"],
  "recommendations": [
    {
      "action": "string",
      "scope_id": "string",
      "rationale": "string",
      "confidence": 0.0,
      "expected_impact": "string"
    }
  ],
  "risks": ["string"],
  "evidence": [{"metric": "string", "value": "string"}]
}

Rules:
- Use only the provided metrics
- Keep findings specific
- Keep recommendations actionable
- Return strictly valid JSON only
"""

class ReportComposerAgent(Agent):
    name = "report_composer"

    def __init__(self, client: ClaudeClient) -> None:
        self.client = client

    def run(self, context: dict[str, object]) -> AgentOutput:
        if not self.client.is_available():
            return AgentOutput(findings=["Claude unavailable; used deterministic reporting path."])

        prompt = (
            "Use this context to produce final weekly findings and recommendations JSON:\n"
            + json.dumps(context, default=str)[:60000]
        )
        payload = self.client.complete_json(SYSTEM_PROMPT, prompt)
        if not payload:
            return AgentOutput(risks=["Claude returned invalid JSON contract."])

        recs = []
        for item in payload.get("recommendations", []):
            recs.append(
                AgentRecommendation(
                    action=str(item.get("action", "hold")),
                    scope_id=str(item.get("scope_id", "unknown")),
                    rationale=str(item.get("rationale", "")),
                    confidence=float(item.get("confidence", 0.5)),
                    expected_impact=str(item.get("expected_impact", "")),
                )
            )

        return AgentOutput(
            findings=[str(x) for x in payload.get("findings", [])],
            recommendations=recs,
            risks=[str(x) for x in payload.get("risks", [])],
            evidence=[x for x in payload.get("evidence", []) if isinstance(x, dict)],
        )
