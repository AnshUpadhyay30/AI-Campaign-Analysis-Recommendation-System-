from __future__ import annotations

from datetime import datetime
from pathlib import Path

from src.common.contracts import AgentOutput


def fmt_money(value: float) -> str:
    return f"${value:,.2f}"


def build_weekly_report(
    output_path: Path,
    run_id: str,
    kpi_summary: dict[str, object],
    agent_outputs: list[tuple[str, AgentOutput]],
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    totals = kpi_summary.get("totals", {})
    top = kpi_summary.get("top", [])
    bottom = kpi_summary.get("bottom", [])

    lines = [
        "# Weekly Performance Marketing Report",
        "",
        f"Generated: {datetime.utcnow().isoformat()}Z",
        f"Run ID: `{run_id}`",
        "",
        "## KPI Snapshot",
        "",
        f"- Spend: {fmt_money(float(totals.get('spend', 0.0)))}",
        f"- Impressions: {float(totals.get('impressions', 0.0)):,.0f}",
        f"- Clicks: {float(totals.get('clicks', 0.0)):,.0f}",
        f"- CTR: {float(totals.get('ctr', 0.0)):.2f}%",
        f"- CPC: {fmt_money(float(totals.get('cpc', 0.0)))}",
        f"- CPA: {fmt_money(float(totals.get('cpa', 0.0)))}",
        "",
        "## Top Entities",
        "",
    ]

    for row in top[:5]:
        lines.append(
            f"- {row.get('entity', 'unknown')}: spend {fmt_money(float(row.get('spend', 0.0)))}, "
            f"CTR {float(row.get('ctr', 0.0)):.2f}%, CPA {fmt_money(float(row.get('cpa', 0.0)))}"
        )

    lines.extend(["", "## Risk Entities", ""])
    for row in bottom[:5]:
        lines.append(
            f"- {row.get('entity', 'unknown')}: CPA {fmt_money(float(row.get('cpa', 0.0)))}, "
            f"CPC {fmt_money(float(row.get('cpc', 0.0)))}"
        )

    lines.extend(["", "## Agent Findings", ""])
    for agent_name, output in agent_outputs:
        lines.append(f"### {agent_name}")
        for finding in output.findings:
            lines.append(f"- {finding}")
        for risk in output.risks:
            lines.append(f"- Risk: {risk}")
        if not output.findings and not output.risks:
            lines.append("- No additional findings.")
        lines.append("")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def build_action_playbook(
    output_path: Path,
    run_id: str,
    recommendations: list[dict[str, object]],
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Weekly Action Playbook",
        "",
        f"Run ID: `{run_id}`",
        "",
        "## Proposed Actions (Human Approval Required)",
        "",
    ]

    if not recommendations:
        lines.append("- No recommendations generated.")
    for rec in recommendations:
        lines.append(
            f"- [{rec['status']}] `{rec['action']}` on `{rec['scope_id']}` "
            f"(confidence {float(rec['confidence']):.2f}): {rec['rationale']}"
        )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path
