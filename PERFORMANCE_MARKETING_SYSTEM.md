# Local Performance Marketing Intelligence System

This repository now includes a Meta-first, Claude-powered local intelligence system with:

- Weekly pipeline orchestration (`run-weekly`)
- SQLite + vector memory persistence
- Agent-based analysis and recommendation generation
- Human approval workflow for recommendations
- Markdown/CSV output artifacts
- Email and WhatsApp summary dispatch
- Local UI endpoints for runs and approvals

## Quick Start

1. Create virtual environment and install dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Configure environment.

```bash
cp .env.example .env
# fill credentials for Meta, Claude, email, whatsapp
```

3. Initialize database.

```bash
python3 -m src.main init-db
```

4. Run pipeline in dry mode (no live API call).

```bash
python3 -m src.main run-weekly --dry-run
```

5. Run pipeline with live Meta API.

```bash
python3 -m src.main run-weekly
```

6. Launch local UI.

```bash
python3 -m src.main serve-ui
```

UI endpoints:
- `GET /runs`
- `GET /recommendations?run_id=<id>`
- `POST /recommendations/<rec_id>/status` with JSON `{ "status": "APPROVED" }`

7. Start weekly scheduler.

```bash
python3 -m src.main start-scheduler
```

Cron expression defaults to Monday 8:00 AM IST via `.env`:
`WEEKLY_CRON=0 8 * * MON`

## Core Directories

- `src/ingestion`: Meta API extraction
- `src/normalize`: schema normalization
- `src/analytics`: KPI computation
- `src/agents`: specialized agent logic + Claude report composer
- `src/orchestrator`: run pipeline and scheduler
- `src/reporting`: report and playbook generation
- `src/notifications`: email and WhatsApp adapters
- `skills/`: skill definitions, prompts, and validators
- `ui/`: local Flask API for run/recommendation review

## Notes

- Recommendations are stored as `PROPOSED` by default.
- Operator approval is required before execution in downstream campaign workflows.
- Google/Amazon extension should be implemented by adding new ingestion adapters mapped into the canonical schema.
