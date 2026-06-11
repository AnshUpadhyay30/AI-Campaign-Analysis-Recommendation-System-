from __future__ import annotations

import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import uuid4

from src.agents.budget_allocator import BudgetAllocatorAgent
from src.agents.claude_client import ClaudeClient
from src.agents.creative_intelligence import CreativeIntelligenceAgent
from src.agents.data_quality import DataQualityAgent
from src.agents.market_context import MarketContextAgent
from src.agents.performance_diagnostics import PerformanceDiagnosticsAgent
from src.agents.report_composer import ReportComposerAgent
from src.analytics.kpi import compute_kpi_summary, to_float
from src.common.config import Settings
from src.common.contracts import AgentOutput, AgentRecommendation, RunArtifacts
from src.common.db import connect, init_db
from src.common.vector_store import VectorStore
from src.ingestion.meta import PullConfig, pull_insights, write_csv
from src.normalize.normalize import normalize_csv
from src.notifications.emailer import send_weekly_email
from src.notifications.whatsapp import send_whatsapp_summary
from src.reporting.builder import build_action_playbook, build_weekly_report


LOGGER = logging.getLogger(__name__)


DEFAULT_FIELDS = (
    "campaign_id,campaign_name,adset_id,adset_name,ad_id,ad_name,date_start,date_stop,"
    "spend,impressions,reach,clicks,ctr,cpc,cpm,frequency,inline_link_clicks,"
    "actions,action_values"
)


def _run_id(prefix: str = "run") -> str:
    return f"{prefix}_{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}_{uuid4().hex[:8]}"


def _friendly_file_stamp() -> str:
    now = datetime.now()
    day_name = now.strftime("%A")      # Tuesday
    day = now.strftime("%d")           # 14
    month = now.strftime("%B")         # April
    year = now.strftime("%Y")          # 2026
    time_part = now.strftime("%H-%M")  # 13-35
    return f"{day_name}_{day}_{month}_{year}_{time_part}"


def initialize(settings: Settings) -> None:
    init_db(settings.db_path)
    settings.report_output_dir.mkdir(parents=True, exist_ok=True)


def _insert_run(settings: Settings, run_id: str, status: str, started_at: str) -> None:
    conn = connect(settings.db_path)
    with conn:
        conn.execute(
            """
            INSERT OR REPLACE INTO runs(run_id, status, started_at, platform, window_start, window_end)
            VALUES(?, ?, ?, 'meta', date('now','-7 day'), date('now'))
            """,
            (run_id, status, started_at),
        )
    conn.close()


def _update_run(settings: Settings, run_id: str, status: str, error_summary: Optional[str] = None) -> None:
    conn = connect(settings.db_path)
    with conn:
        conn.execute(
            "UPDATE runs SET status=?, ended_at=?, error_summary=? WHERE run_id=?",
            (status, datetime.utcnow().isoformat(), error_summary, run_id),
        )
    conn.close()


def _persist_metrics(settings: Settings, run_id: str, normalized_csv_path: Path) -> None:
    conn = connect(settings.db_path)
    with normalized_csv_path.open("r", newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = []
        for row in reader:
            entity_id = row.get("ad_id") or row.get("adset_id") or row.get("campaign_id") or "unknown"
            entity_type = "ad" if row.get("ad_id") else "adset" if row.get("adset_id") else "campaign"
            entity_name = row.get("ad_name") or row.get("adset_name") or row.get("campaign_name") or "unknown"
            payload_json = json.dumps(row)
            rows.append(
                (
                    run_id,
                    entity_id,
                    entity_type,
                    entity_name,
                    row.get("date_start", ""),
                    to_float(row.get("spend", "0")),
                    to_float(row.get("impressions", "0")),
                    to_float(row.get("clicks", row.get("link_clicks", "0"))),
                    to_float(row.get("ctr", "0")),
                    to_float(row.get("cpc", "0")),
                    to_float(row.get("cpm", "0")),
                    to_float(row.get("actions.purchase", row.get("actions.lead", "0"))),
                    to_float(row.get("action_values.purchase", "0")),
                    payload_json,
                )
            )

    with conn:
        conn.executemany(
            """
            INSERT INTO entity_metrics_daily(
                run_id, entity_id, entity_type, entity_name, metric_date,
                spend, impressions, clicks, ctr, cpc, cpm, conversions, conversion_value, payload_json
            ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows,
        )
    conn.close()


def _persist_recommendations(settings: Settings, run_id: str, recs: list[AgentRecommendation]) -> None:
    conn = connect(settings.db_path)
    with conn:
        for rec in recs:
            rec_id = _run_id("rec")
            conn.execute(
                """
                INSERT INTO recommendations(rec_id, run_id, scope_id, action, rationale, confidence, expected_impact, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'PROPOSED')
                """,
                (
                    rec_id,
                    run_id,
                    rec.scope_id,
                    rec.action,
                    rec.rationale,
                    rec.confidence,
                    rec.expected_impact,
                ),
            )
    conn.close()


def _fetch_recommendations(settings: Settings, run_id: str) -> list[dict[str, object]]:
    conn = connect(settings.db_path)
    rows = conn.execute(
        "SELECT rec_id, scope_id, action, rationale, confidence, expected_impact, status FROM recommendations WHERE run_id=? ORDER BY confidence DESC",
        (run_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def set_recommendation_status(settings: Settings, rec_id: str, status: str) -> None:
    if status not in {"APPROVED", "DEFERRED", "REJECTED", "PROPOSED"}:
        raise ValueError("Invalid recommendation status")
    conn = connect(settings.db_path)
    with conn:
        conn.execute("UPDATE recommendations SET status=? WHERE rec_id=?", (status, rec_id))
    conn.close()


def _mock_rows(level: str) -> list[dict[str, str]]:
    base = {
        "date_start": datetime.utcnow().strftime("%Y-%m-%d"),
        "date_stop": datetime.utcnow().strftime("%Y-%m-%d"),
        "impressions": "15000",
        "clicks": "220",
        "spend": "180.0",
        "actions.purchase": "9",
        "action_values.purchase": "760.0",
        "ctr": "1.46",
        "cpc": "0.82",
        "cpm": "12.0",
    }
    rows = []
    for idx in range(1, 5):
        row = dict(base)
        row["campaign_id"] = f"cmp_{idx}"
        row["campaign_name"] = f"Campaign {idx}"
        row["adset_id"] = f"adset_{idx}"
        row["adset_name"] = f"Audience {idx}"
        row["ad_id"] = f"ad_{idx}"
        row["ad_name"] = f"Creative {idx}"
        row["spend"] = str(130 + idx * 35)
        row["actions.purchase"] = str(4 + idx)
        rows.append(row)
    return rows


def run_weekly(settings: Settings, rerun: bool = False, dry_run: bool = False) -> RunArtifacts:
    initialize(settings)
    run_id = _run_id("weekly")
    started = datetime.utcnow().isoformat()
    _insert_run(settings, run_id, "RUNNING", started)
    artifacts = RunArtifacts()

    try:
        file_stamp = _friendly_file_stamp()
        stamp = datetime.utcnow().strftime("%Y%m%d")
        raw_paths: list[Path] = []

        for level in ["campaign", "adset", "ad"]:
            config = PullConfig(
                account_id=settings.meta_ad_account_id,
                access_token=settings.meta_access_token,
                api_version=settings.meta_api_version,
                level=level,
                fields=DEFAULT_FIELDS,
                date_preset="last_7d",
                breakdowns="publisher_platform,platform_position",
            )
            if dry_run:
                rows = _mock_rows(level)
            else:
                rows = pull_insights(config)

            raw_path = Path("data/raw") / f"Meta_{level.capitalize()}_{file_stamp}.csv"
            write_csv(raw_path, rows)
            raw_paths.append(raw_path)

        normalized_path = Path("data/processed") / f"Normalized_Data_{file_stamp}.csv"
        normalize_csv(raw_paths, normalized_path)

        kpi_summary = compute_kpi_summary(normalized_path, group_by="campaign_name")
        _persist_metrics(settings, run_id, normalized_path)

        vector_store = VectorStore(settings.vector_db_path)
        vector_store.add(
            doc_id=f"kpi_{run_id}",
            text=json.dumps(kpi_summary)[:10000],
            metadata={"run_id": run_id, "type": "kpi_summary"},
        )

        claude = ClaudeClient(
            api_key=settings.anthropic_api_key,
            model=settings.claude_model,
            max_tokens=settings.llm_max_tokens,
            temperature=settings.llm_temperature,
        )

        context = {
            "run_id": run_id,
            "kpi_summary": kpi_summary,
            "objective": "balanced_funnel",
            "budget_guardrail": "target_cpa_cpl",
            "rerun": rerun,
        }

        agents = [
            DataQualityAgent(),
            PerformanceDiagnosticsAgent(),
            CreativeIntelligenceAgent(),
            BudgetAllocatorAgent(),
            MarketContextAgent(),
            ReportComposerAgent(claude),
        ]

        all_outputs: list[tuple[str, AgentOutput]] = []
        all_recs: list[AgentRecommendation] = []
        for agent in agents:
            output = agent.run(context)
            all_outputs.append((agent.name, output))
            all_recs.extend(output.recommendations)

        _persist_recommendations(settings, run_id, all_recs)
        rec_rows = _fetch_recommendations(settings, run_id)

        report_path = settings.report_output_dir / f"Weekly_Report_{file_stamp}.md"
        playbook_path = settings.report_output_dir / f"Action_Playbook_{file_stamp}.md"

        build_weekly_report(report_path, run_id, kpi_summary, all_outputs)
        build_action_playbook(playbook_path, run_id, rec_rows)

        email_body = (
            f"Weekly run {run_id} completed. "
            f"Proposed recommendations: {len(rec_rows)}. "
            f"Review report and approve actions in UI."
        )
        send_weekly_email(settings, f"Weekly Performance Report {stamp}", email_body, [report_path, playbook_path])

        whatsapp_body = (
            f"Weekly run complete ({run_id}). "
            f"Top actions: {', '.join([r['action'] for r in rec_rows[:3]]) or 'none'}."
        )
        send_whatsapp_summary(settings, whatsapp_body)

        artifacts.raw_csv_paths = [str(p) for p in raw_paths]
        artifacts.normalized_csv_path = str(normalized_path)
        artifacts.weekly_report_path = str(report_path)
        artifacts.playbook_path = str(playbook_path)

        _update_run(settings, run_id, "SUCCEEDED")
        return artifacts

    except Exception as exc:
        LOGGER.exception("Weekly run failed")
        _update_run(settings, run_id, "FAILED", error_summary=str(exc))
        raise