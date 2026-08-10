# job-application-kit

Reusable support infrastructure for an agent-assisted job search while candidate-specific state stays local.

## Capabilities

- deterministic job and resume routing;
- URL and role deduplication;
- local submission history;
- fail-open telemetry;
- a version-controlled application-run contract;
- onboarding that collects candidate facts and checks whether the current resume supports the target search.

## Privacy model

Candidate-specific data is local and ignored by default:

```text
config/profile.toml
config/resumes.toml
config/searches.toml
config/application-state.toml
resumes/
private/
```

Credentials, security answers, compensation submissions, screenshots, inbox data, resumes, and application history must stay outside Git.

## Setup

```bash
python scripts/bootstrap.py
```

Then invoke:

```text
job-search-onboarding
```

Complete onboarding before running applications.

## Runtime authority

1. `AGENTS.md`
2. `startup.md`
3. local `config/profile.toml`
4. local `config/searches.toml`
5. local `config/resumes.toml`
6. code and local state

## Development

```bash
python -m unittest discover -v
```

## Public-repository safety

Before each push, confirm that candidate files remain untracked:

```bash
git status --short
git ls-files config/ resumes/ private/
```

Only `*.example.toml` files should be tracked under `config/`.
