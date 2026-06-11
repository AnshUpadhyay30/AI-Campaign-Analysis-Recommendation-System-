# Operations Runbook

## 1. Weekly Cadence (Owner Procedure)

Monday (8:00 AM IST automated run):
1. Verify run status in `/runs`.
2. Open latest report and action playbook in `output/reports/`.
3. Review proposed recommendations.
4. Approve/defer/reject recommendations via UI endpoint or CLI.
5. Execute approved actions in Meta Ads Manager manually.
6. Log outcome notes for next cycle learning.

## 2. Manual Fallback Run

If scheduled run fails:
1. Execute `python3 -m src.main run-weekly`.
2. Inspect stdout and `logs/system.log`.
3. Confirm artifacts are generated.
4. Notify stakeholders with rerun timestamp.

## 3. Incident Playbook

### 3.1 Meta API Failure

Symptoms:
- Run marked `FAILED`
- Error summary includes API error code

Actions:
1. Check token validity and ad account permissions.
2. Validate API version in `.env`.
3. Run with `--dry-run` to confirm non-API path is healthy.
4. Re-run live pipeline.

### 3.2 Claude Unavailable

Symptoms:
- Claude composer returns warning/empty contract

Actions:
1. Verify `ANTHROPIC_API_KEY` and model name.
2. Continue operations with deterministic agent outputs.
3. Re-enable Claude once key is valid.

### 3.3 Notification Delivery Failure

Symptoms:
- Email/WhatsApp status skipped or failed

Actions:
1. Validate recipient and sender settings.
2. Confirm provider credentials.
3. Share artifacts manually while issue is fixed.

## 4. Approval Governance

1. Approval authority: designated marketing owner.
2. Status policy:
- `APPROVED`: ready for execution
- `DEFERRED`: revisit next run
- `REJECTED`: do not execute
3. Keep rationale notes for rejected high-confidence recommendations.

## 5. Data Retention and Cleanup

1. Keep raw + processed files for minimum 8 weeks.
2. Keep SQLite history for full quarter before archival.
3. Rotate logs monthly.

## 6. Weekly Checklist

1. Run succeeded.
2. Data quality findings reviewed.
3. Top/bottom entities sanity checked.
4. Recommendations status updated.
5. Reports communicated to stakeholders.
6. Feedback captured for learning loop.
