# Detailed Design Document

## 1. System Overview

The system is a local, human-in-the-loop performance marketing intelligence platform that:

1. Pulls Meta Ads data at campaign/adset/ad levels.
2. Normalizes and stores history in SQLite.
3. Computes KPI diagnostics deterministically.
4. Uses agent pipeline (including Claude) for recommendations.
5. Produces weekly report + action playbook.
6. Sends summary notifications via email and WhatsApp.
7. Exposes UI endpoints for recommendation approvals.

Primary cadence is Monday 8:00 AM IST.

## 2. Architecture

### 2.1 Components

1. Ingestion Layer
- Module: `src/ingestion/meta.py`
- Responsibilities: Meta Insights API extraction, retry/backoff, pagination, row flattening.

2. Normalization Layer
- Module: `src/normalize/normalize.py`
- Responsibilities: column alias normalization, multi-file merge into canonical CSV.

3. Analytics Layer
- Module: `src/analytics/kpi.py`
- Responsibilities: KPI computation (CTR, CPC, CPM, CPA, CVR), entity ranking.

4. Agent Layer
- Modules: `src/agents/*`
- Responsibilities:
  - data quality assessment
  - performance diagnostics
  - creative diagnostics
  - budget allocation
  - external market context
  - Claude-assisted report composition

5. Orchestration Layer
- Modules: `src/orchestrator/pipeline.py`, `src/orchestrator/scheduler.py`
- Responsibilities: stage sequencing, persistence, run status, scheduling.

6. Persistence Layer
- Modules: `src/common/db.py`, `src/common/vector_store.py`
- Responsibilities: structured history in SQLite, semantic memory in Chroma/fallback JSONL.

7. Reporting Layer
- Module: `src/reporting/builder.py`
- Responsibilities: Markdown weekly report and action playbook artifacts.

8. Delivery Layer
- Modules: `src/notifications/emailer.py`, `src/notifications/whatsapp.py`, `ui/app.py`
- Responsibilities: team notifications and approval interface APIs.

## 3. Data Flow

1. Orchestrator creates `run_id` and inserts `RUNNING` run record.
2. For each level (`campaign`, `adset`, `ad`), ingestion pulls rows and writes raw CSV.
3. Normalizer merges and standardizes into one processed CSV.
4. KPI engine computes account and entity-level summaries.
5. Metrics are persisted to SQLite (`entity_metrics_daily`).
6. KPI summary snapshot is written to vector memory.
7. Agents run sequentially with shared context.
8. Recommendations are persisted as `PROPOSED`.
9. Weekly report + playbook are generated.
10. Notification adapters send summary messages.
11. Run record is updated to `SUCCEEDED` or `FAILED`.

## 4. Data Model

SQLite tables (from `src/common/db.py`):

1. `runs`
- Run lifecycle tracking and failure context.

2. `entity_metrics_daily`
- Normalized metric fact table by entity/date.

3. `creative_features`
- Creative taxonomy storage (v1.5+ enrichment).

4. `recommendations`
- Agent-generated actions with confidence and status.

5. `recommendation_feedback`
- Outcome feedback loop after execution.

6. `external_context`
- Stored market context facts (Meta/IAB).

## 5. Agent and Contract Design

### 5.1 Contract

Each agent returns `AgentOutput`:
- `findings[]`
- `recommendations[]`
- `risks[]`
- `evidence[]`

Recommendation contract:
- `action`
- `scope_id`
- `rationale`
- `confidence` (0-1)
- `expected_impact`

### 5.2 Agents

1. DataQualityAgent
- Detects low volume/missing ingestion signals.

2. PerformanceDiagnosticsAgent
- Identifies top/bottom entities and efficiency patterns.

3. CreativeIntelligenceAgent
- Flags weak CTR/CVR patterns and proposes creative tests.

4. BudgetAllocatorAgent
- Applies CPA guardrails for scale/reduce/hold decisions.

5. MarketContextAgent
- Adds non-causal external trend context for framing.

6. ReportComposerAgent
- Uses Claude to synthesize final structured findings (when available).

## 6. Human-in-the-Loop Governance

1. Every recommendation starts with `PROPOSED` status.
2. Allowed transitions: `PROPOSED` -> `APPROVED | DEFERRED | REJECTED`.
3. Approval endpoint: `POST /recommendations/<rec_id>/status`.
4. Only approved recommendations should be actioned in ad platforms.

## 7. Configuration and Environment

Environment variables are defined in `.env.example`.

Key groups:
1. Meta API
- `META_ACCESS_TOKEN`
- `META_AD_ACCOUNT_ID`
- `META_API_VERSION`

2. Claude
- `ANTHROPIC_API_KEY`
- `CLAUDE_MODEL`
- `LLM_MAX_TOKENS`
- `LLM_TEMPERATURE`

3. Storage/Runtime
- `DB_PATH`
- `VECTOR_DB_PATH`
- `REPORT_OUTPUT_DIR`
- `LOG_DIR`
- `TIMEZONE`
- `WEEKLY_CRON`

4. Delivery
- `EMAIL_*`
- `WHATSAPP_*`

## 8. Scheduling and Reliability

1. Scheduler uses APScheduler with cron semantics.
2. Default weekly trigger: Monday 8:00 AM (`Asia/Kolkata`).
3. Pipeline writes run status and error summary for failures.
4. Dry-run mode uses deterministic mock rows for smoke validation.

## 9. Security and Compliance

1. Secrets must remain only in local `.env`; never in source control.
2. No automated campaign mutation in current v1 implementation.
3. Notification channels may include sensitive KPI data; secure recipients.
4. PII should not be ingested from ad platform exports unless explicitly governed.

## 10. Extension Design (Google, Amazon)

Extension principle: preserve a canonical schema and add source adapters.

1. Add `src/ingestion/google.py` and `src/ingestion/amazon.py`.
2. Map source hierarchies to canonical entity types.
3. Reuse analytics and agent layers with channel-specific metric adapters.
4. Add cross-channel allocator logic only after metric parity validation.
