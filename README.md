# job-application-kit

Reusable support infrastructure for an agent-assisted job search while candidate-specific state stays local.

## Capabilities

- deterministic job and resume routing;
- URL and role deduplication;
- local submission history;
- fail-open telemetry;
- a version-controlled application-run contract;
- onboarding that collects candidate facts and checks whether the current resume supports the target search.

## Evidence-first review

Before a role-fit or resume-readiness assessment, read
[the evidence-first review method](docs/evidence-first-review.md).
Routing is not qualification. Keep paid, project, adjacent, and unknown evidence
separate; review actual duties and responsibility level; do not manufacture lane
or strong/stretch quotas. Place role-relevant evidence first. Preserve original
resumes and require explicit authorization for any rewrite. Keep confidence and
its reason in each readiness assessment.

Use the existing local history for outcome measurement. Unanswered applications
are unresolved, not rejections. Compare artifact versions, role families, fit,
channels, and cohort ages before drawing conclusions. Application throughput is
an execution measure, not evidence of career success. This review method does
not launch a batch or create a second tracker.

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

The review method supplements these controls; it does not override security,
factual accuracy, explicit authorization, or privacy requirements.

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
