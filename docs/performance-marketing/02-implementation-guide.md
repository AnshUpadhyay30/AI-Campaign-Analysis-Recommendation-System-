# Implementation Guide

## 1. Prerequisites

1. Python 3.11+ recommended.
2. Virtual environment tooling.
3. Meta Marketing API credentials.
4. Anthropic API key for Claude.
5. SMTP and Twilio (optional for notifications).

## 2. Setup

1. Create and activate venv.
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies.
```bash
pip install -r requirements.txt
```

3. Configure environment.
```bash
cp .env.example .env
# fill required keys
```

4. Initialize database.
```bash
python3 -m src.main init-db
```

## 3. Command Reference

1. Initialize DB
```bash
python3 -m src.main init-db
```

2. Weekly dry run (safe smoke test)
```bash
python3 -m src.main run-weekly --dry-run
```

3. Weekly live run
```bash
python3 -m src.main run-weekly
```

4. List recent runs
```bash
python3 -m src.main list-runs
```

5. Update recommendation status
```bash
python3 -m src.main set-rec-status --rec-id <id> --status APPROVED
```

6. Serve local UI API
```bash
python3 -m src.main serve-ui
```

7. Start scheduler
```bash
python3 -m src.main start-scheduler
```

## 4. UI Endpoints

1. `GET /`
- health check

2. `GET /runs`
- list recent runs

3. `GET /recommendations?run_id=<id>`
- fetch recommendations for run

4. `POST /recommendations/<rec_id>/status`
- body: `{ "status": "APPROVED" }`

## 5. Artifact Locations

1. Raw extracts
- `data/raw/*.csv`

2. Processed extracts
- `data/processed/*.csv`

3. Reports and playbooks
- `output/reports/*.md`

4. Logs
- `logs/system.log`

## 6. Implementation Notes

1. Dry-run mode bypasses live API and generates mock datasets.
2. Claude output is optional; deterministic agents still run without Anthropic key.
3. Skill registry is file-backed under `skills/*`.
4. Recommendation approval is persisted to SQLite.

## 7. Deployment Model (Local)

Recommended runtime process model for now:
1. Terminal 1: `python3 -m src.main start-scheduler`
2. Terminal 2 (optional): `python3 -m src.main serve-ui`

For always-on local reliability, run scheduler via system service:
1. macOS `launchd` or Linux `systemd`.
2. Ensure environment variables are injected securely.

## 8. Extension Implementation Path

### 8.1 Google Ads

1. Build ingestion adapter with GAQL extraction.
2. Normalize into existing canonical CSV/DB schema.
3. Add platform tag in facts table.
4. Validate KPI parity before enabling recommendations.

### 8.2 Amazon Ads

1. Build report ingestion adapter.
2. Map campaign/adgroup/ad units into canonical entities.
3. Introduce retail-specific KPI fields as optional columns.
4. Gate recommendations until data quality checks pass.
