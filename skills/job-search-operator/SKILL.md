---
name: job-search-operator
description: Explicit-only interface for a candidate's configured job-application workflow. Use when the candidate asks the agent to run, resume, continue, or submit applications.
---

# Job Search Operator

Act as a thin router. Durable policy and candidate facts belong in the repository's local config, not in this skill or chat memory.

1. Read `AGENTS.md` and `startup.md`.
2. Read local profile, searches, resumes, and application state.
3. Refuse to start an application run when onboarding is incomplete or resume readiness has not been assessed with explicit confidence.
4. Query local history before computing progress toward a numeric goal.
5. Use configured lanes and resume routes. Do not invent a route from chat memory.
6. Record confirmed submissions and fail-open telemetry.
7. Stop for required unknown personal facts or security-sensitive handoffs instead of guessing.
8. Keep closeout concise and report confirmed progress, blockers, and unresolved candidate facts.
