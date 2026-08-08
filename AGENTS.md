# Agent instructions

- Read before writing. Use repository files as the source of truth instead of reconstructing candidate facts from chat memory.
- Keep reusable mechanisms in Git and candidate-specific data in ignored local config or private state.
- Never invent employers, credentials, dates, skills, legal status, compensation history, demographic facts, security-clearance facts, or quantitative impact.
- Distinguish verified, inferred, and unknown facts when the distinction affects an application.
- Use the smallest change that solves the task and verify important behavior with a focused check or test.
- Telemetry is subordinate to application throughput and must fail open.
- Never commit credentials, one-time codes, security answers, resume files, application screenshots, inbox contents, compensation submissions, or local application history.
- During onboarding, treat the candidate's current resume as evidence, not as ground truth when the interview reveals more specific experience.
- Onboarding may assess resume readiness but must not generate, rewrite, or silently edit the resume.
- Every resume-readiness assessment must include `confidence = high | medium | low` and one short reason for that confidence.
- Ask neutral evidence-seeking questions. Do not tell the candidate that the onboarding flow assumes their resume is weak or that another person's experience motivated the questions.
