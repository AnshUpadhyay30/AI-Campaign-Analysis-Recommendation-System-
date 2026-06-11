# Testing and Acceptance

## 1. Test Strategy

1. Unit tests
- KPI calculations
- DB initialization
- Contract validation

2. Integration tests
- Dry-run full pipeline
- Report/playbook generation
- Recommendation persistence

3. Operational tests
- Scheduler trigger behavior
- UI status updates
- Notification adapter behavior with test credentials

## 2. Current Baseline

Implemented tests:
- `tests/test_db.py`
- `tests/test_kpi.py`

Recommended additions before production usage:
1. ingestion response parser tests
2. agent contract schema tests
3. scheduler trigger unit tests
4. UI endpoint tests
5. notification mock tests

## 3. Acceptance Criteria

A build is accepted when:
1. `run-weekly --dry-run` succeeds and writes all artifacts.
2. `run-weekly` succeeds with live credentials.
3. Recommendations persist with status `PROPOSED`.
4. Status updates work for all allowed states.
5. Weekly report and action playbook are generated for each run.
6. At least one notification channel confirms delivery (or is explicitly skipped due to config).

## 4. Pre-Go-Live Checklist

1. `.env` populated with production-safe secrets.
2. Scheduler hosted in persistent process.
3. Backup strategy for `data/db` defined.
4. Owner assigned for Monday run monitoring.
5. Incident response channel documented.
6. Manual rerun drill executed at least once.

## 5. Regression Checklist (for every major change)

1. DB migrations backward-compatible.
2. Existing CLI commands unchanged or versioned.
3. Report format remains readable for stakeholders.
4. Approval flow remains intact.
5. Existing run artifacts still generated in expected paths.
