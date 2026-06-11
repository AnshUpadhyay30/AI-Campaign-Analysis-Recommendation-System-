# Performance Marketing Intelligence System: Team Handoff Index

This folder contains implementation and operations documentation for the local, Meta-first, Claude-powered performance marketing intelligence system.

## Audience

- Engineering team implementing and extending the system
- Marketing operations owner running weekly cycles
- Tech lead managing reliability and future platform expansion

## Documents

1. `01-detailed-design.md`
- End-to-end architecture
- Data model and contracts
- Agent and skill design
- Scheduling and operations behavior

2. `02-implementation-guide.md`
- Local setup
- Configuration
- Commands and workflows
- Extension path (Google/Amazon)

3. `03-operations-runbook.md`
- Weekly operating procedure
- Incident handling
- Recovery and rerun process
- Approval governance

4. `04-testing-and-acceptance.md`
- Test strategy and acceptance criteria
- Pre-production checklist
- Weekly quality gates

5. `05-roadmap-and-ownership.md`
- Phase plan
- Ownership model
- Backlog and priorities

## Source Implementation Paths

- `src/main.py`
- `src/orchestrator/pipeline.py`
- `src/ingestion/meta.py`
- `src/analytics/kpi.py`
- `src/agents/*`
- `src/reporting/builder.py`
- `src/notifications/*`
- `ui/app.py`
- `skills/*`

## Current Delivery Status

- Core local pipeline: implemented
- Dry run workflow: validated
- Live integrations: require credentials in `.env`
- Weekly scheduler: implemented, requires process hosting
- UI API: implemented (run/recommendation endpoints)
