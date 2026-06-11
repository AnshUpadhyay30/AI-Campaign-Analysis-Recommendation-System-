# Roadmap and Ownership

## 1. Ownership Model

1. Product owner (marketing lead)
- defines objective priorities and approval rules

2. Engineering owner
- reliability, integrations, data model evolution

3. Ops owner
- weekly monitoring, alert triage, runbook execution

4. Analytics owner (can be shared)
- KPI quality, threshold tuning, recommendation quality review

## 2. Phase Plan

### Phase A (Current)
1. Meta ingestion
2. KPI analytics
3. Agent recommendations
4. Human approvals
5. Report + playbook output

### Phase B
1. Creative taxonomy enrichment in `creative_features`
2. Outcome feedback loops tied to recommendations
3. Better anomaly detection and confidence calibration

### Phase C
1. Google Ads adapter
2. Cross-channel KPI normalization
3. Channel-aware recommendation logic

### Phase D
1. Amazon Ads adapter
2. Retail-media KPI extensions
3. Unified budget allocator across channels

## 3. Prioritized Backlog

1. High Priority
- add integration tests for pipeline and UI endpoints
- add idempotency safeguards for repeated runs
- add structured failure alerts

2. Medium Priority
- enrich creative diagnostics with taxonomy extraction
- improve recommendation de-duplication by scope/action
- add report version metadata

3. Low Priority
- richer UI with approval comments
- scenario planning and forecast simulation
- full automation for safe low-risk actions

## 4. Team Working Agreements

1. No direct auto-mutations to ad platforms without explicit change control.
2. All recommendation logic changes require KPI validation notes.
3. Keep prompt/template changes versioned and reviewed.
4. Preserve weekly run continuity over feature expansion.
