# Job application operator startup contract

Canonical invocation: `job-search-operator — apply to N jobs`.

The primary outcome is `N` qualifying, ATS-confirmed submissions. Treat a bare numeric goal as an absolute target for the active accounting period. Query local history first and submit only the remaining delta. An explicit `another N` is additive.

Before an application run, read this file plus local `config/profile.toml`, `config/searches.toml`, and `config/resumes.toml`. If onboarding has not been completed, or the resume-readiness assessment is missing, stop and run `job-search-onboarding` first.

## Qualification

- Prefer roles inside configured target lanes.
- Missing a preferred tool or a modest experience gap is not automatically disqualifying.
- Skip hard conflicts such as work authorization, mandatory clearance, mandatory license, incompatible location, materially different role family, or a required personal fact that is unknown.
- Apply candidate-defined employer and industry exclusions from local config. Do not infer moral or industry exclusions that the candidate did not provide.
- Use only truthful candidate facts. Do not inflate titles, years, ownership, skills, or impact.

## Submission boundary

- The browser/computer-use agent owns navigation, form completion, and visible submission.
- Stop on identity verification, passwords, one-time codes, payment prompts, or other security-sensitive handoffs.
- Routine application questions may be answered from verified local profile data.
- When a required fact is unknown, record the gap and ask the candidate instead of guessing.

## Evidence and accounting

- Count a submission only when the ATS shows a clear success page, URL, or message.
- Record confirmed submissions in local history immediately.
- Dedupe by canonical URL and normalized company/title/location identity.
- Email receipts are secondary evidence and must not redefine an ATS-confirmed success.
- Telemetry must never delay or block submission.

## Closeout

Report confirmed submissions, remaining gap to `N`, skips/blockers, and material unknown facts discovered during the run. Do not expose private profile fields or compensation values unless the candidate explicitly asks for them.
