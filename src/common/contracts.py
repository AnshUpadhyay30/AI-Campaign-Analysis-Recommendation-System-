from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentRecommendation:
    action: str
    scope_id: str
    rationale: str
    confidence: float
    expected_impact: str


@dataclass
class AgentOutput:
    findings: list[str] = field(default_factory=list)
    recommendations: list[AgentRecommendation] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class RunArtifacts:
    raw_csv_paths: list[str] = field(default_factory=list)
    normalized_csv_path: str = ""
    weekly_report_path: str = ""
    playbook_path: str = ""
