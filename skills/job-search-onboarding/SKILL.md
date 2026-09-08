---
name: job-search-onboarding
description: Build a verified local candidate profile, target lanes, and resume-readiness assessment before automated job applications. Requires the candidate's current resume. Does not write or rewrite resumes.
---

# Job Search Onboarding

Read `AGENTS.md` and `docs/onboarding.md` first.

## Goal

Produce enough verified local state for the job application operator to act without inventing candidate facts. Treat the current resume as one evidence source, then interview the candidate for stronger or missing evidence.

## Phase 1: current resume

Ask the candidate to provide the resume they currently intend to use. Inspect it before asking broad career questions. Record its apparent role direction, experience chronology, technologies, stated scope, and stated outcomes. Do not edit it.

If the candidate has multiple current resumes, inspect each and record its intended route. Do not create new variants during onboarding.

## Phase 2: evidence interview

Ask neutral questions to gather evidence. Follow the strongest experiences rather than asking a fixed checklist. Probe for:

- actual ownership versus participation;
- systems or artifacts built, migrated, operated, debugged, or designed;
- scale and constraints when known;
- technical decisions and tradeoffs;
- failures, incidents, difficult bugs, and repairs;
- measurable outcomes when real measurements exist;
- specific qualitative outcomes when measurements do not exist;
- cross-team and stakeholder interfaces;
- projects that provide evidence not captured by job titles;
- target role families and level;
- authorization, sponsorship, location, travel, schedule, and explicit exclusions;
- repetitive ATS facts the candidate explicitly verifies.

Never force numbers. Never convert a vague recollection into a precise claim without confirmation.

## Phase 3: resume sufficiency

Compare the current resume against the verified evidence. Choose exactly one:

- `usable_as_is`
- `usable_with_targeted_edits`
- `materially_undersells_experience`

Always include:

- `confidence = high | medium | low`
- `confidence_reason = one sentence`
- a short list of verified evidence gaps;
- the likely impact on the intended search lanes.

Confidence is confidence in the assessment. It is not a rating of the person.

Do not generate, rewrite, or silently modify the resume. If the current resume is insufficient, identify what evidence is missing and stop there unless the candidate separately asks for a resume-writing task.

## Phase 4: persist local config

Populate the ignored local files:

- `config/profile.toml`
- `config/resumes.toml`
- `config/searches.toml`
- `config/application-state.toml`

Use environment variables for resume paths. Keep resume files outside Git. Mark onboarding complete only after the resume-readiness assessment and confidence are recorded and at least one usable resume route exists.

## Final onboarding output

Return a compact summary:

- target lanes;
- resume route(s);
- resume-readiness assessment;
- explicit confidence and reason;
- material unknown facts that still require confirmation;
- whether automated applications are ready to start.
