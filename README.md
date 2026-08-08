# job-application-kit

Candidate-agnostic support infrastructure for an agent-assisted job search, designed so the reusable repository can be public while candidate-specific state stays local.

This repository separates reusable mechanisms from candidate-specific facts. It is designed for a technically experienced candidate who wants to give an application agent a reliable, auditable contract without committing identity data, resume files, compensation decisions, credentials, or application history to Git.

## What it owns

- deterministic job/resume routing;
- URL and role deduplication;
- local submission history;
- low-overhead fail-open telemetry;
- a version-controlled application-run contract;
- an onboarding interview that collects candidate facts and evaluates whether the candidate's current resume is sufficient for the target search.

The onboarding process **does not write or rewrite a resume**. It inspects the current resume, interviews the candidate about actual experience, and reports whether the resume is usable as-is, usable with targeted edits, or materially undersells the available evidence. The assessment must include explicit confidence.

## Privacy model

Git contains schemas, examples, policy, and code. Candidate-specific data is local and ignored by default:

```text
config/profile.toml
config/resumes.toml
config/searches.toml
config/application-state.toml
resumes/
private/
```

Credentials, security answers, exact compensation submissions, screenshots, inbox data, and application history must stay outside Git.

## Setup

```bash
python scripts/bootstrap.py
```

Then invoke the onboarding skill in your coding agent:

```text
job-search-onboarding
```

Give it your current resume when requested. Complete the evidence interview before running applications.

## Runtime authority

1. `AGENTS.md` — global repository constraints.
2. `startup.md` — application-run contract.
3. local `config/profile.toml` — candidate facts and boundaries.
4. local `config/searches.toml` — target role lanes and exclusions.
5. local `config/resumes.toml` — resume routes and local paths.
6. code and local state — routing, dedupe, history, telemetry.

## Development

```bash
python -m unittest discover -v
```

## Lineage

This kit was generalized from two private upstream systems: a working computer-use job-application agent and a small cross-repository agent-context system. The first supplied the routing, dedupe, history, fail-open telemetry, and run-contract patterns. The second supplied the scope rule used here: keep personal state at the narrowest useful scope and keep reusable agent instructions small, explicit, and source-controlled.

No upstream candidate profile, resume URL, contact data, compensation record, employer preference, application ledger, or telemetry row is included here.

## Public-repository safety

This repository is intended to be publishable. Before each push, confirm that ignored candidate files remain untracked:

```bash
git status --short
git ls-files config/ resumes/ private/
```

Only the `*.example.toml` configuration files should be tracked under `config/`. Candidate resumes and local profile/application state must remain untracked.
