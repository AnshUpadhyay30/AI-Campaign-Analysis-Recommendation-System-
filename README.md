# Alteryx Codex Operating Model

This workspace turns the plan into a practical starter kit for running Ben Canning's "new way of working" in Codex.

## What's here

- `career-story.md`: master career narrative, audience-specific summaries, signature strengths, proof bank, and translation layer.
- `playbook/career-narrative-system.md`: the step-by-step process for turning your full experience into a market-aware narrative system.
- `playbook/90-day-pilot.md`: a concrete pilot plan for one PM/UX/Engineering triad.
- `playbook/team-operating-model.md`: the scalable operating model for broader adoption.
- `templates/career/evidence-base.md`: structured inventory for roles, products, technologies, methods, and impact.
- `templates/career/market-translation.md`: template for mapping your master story to a specific company, role, or recruiter conversation.
- `templates/context-layer/`: the shared context files every feature should use.
- `templates/prompts/`: prompt templates for kickoff, design-to-spec, spec-to-Jira, implementation, and architecture review.
- `templates/agents.md`: role rules for Codex agents.
- `metrics/pilot-scorecard.md`: success criteria and evidence collection for the pilot.

## How to use this in Codex

1. Copy `templates/context-layer/` into a feature folder.
2. Fill in `00-overview.md` first, then resolve decisions in `01-decisions.md`.
3. Ask Codex to read the context layer plus `templates/agents.md` before drafting any output.
4. Use the prompt templates in order:
   - `feature-kickoff.md`
   - `design-to-spec.md`
   - `spec-to-jira.md`
   - `story-to-implementation.md`
   - `architecture-review.md`
5. During the pilot, log outcomes in `metrics/pilot-scorecard.md`.

## Design principles

- Shared context beats separate functional documents.
- Human precision is the bottleneck; agent speed is not.
- PM, UX, and Engineering each own a slice of judgment.
- Agents can draft and execute, but humans must approve intent and coherence.
- Architecture review is a continuous ritual, not a last-mile task.
- Career narrative should be built from evidence and patterns, not resume bullet inflation.
- Technologies matter as proof of judgment and adaptability, not as disconnected keyword lists.

## Performance Marketing System

A full local implementation for the Meta-first, Claude-powered performance marketing intelligence workflow has been added.

- Design and setup guide: `PERFORMANCE_MARKETING_SYSTEM.md`
- Team handoff documentation: `docs/performance-marketing/00-TEAM-HANDOFF-INDEX.md`
- Entry command: `python3 -m src.main`
- Core modules: `src/ingestion`, `src/analytics`, `src/agents`, `src/orchestrator`, `src/reporting`, `src/notifications`, `ui`
