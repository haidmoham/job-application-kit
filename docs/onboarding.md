# Onboarding contract

Onboarding builds a trustworthy candidate model before application automation starts.

## Inputs

Require the candidate's current resume in readable form. Also ask for the intended job-search direction in the candidate's own words. Do not assume one resume is enough and do not assume multiple resumes are required.

## Interview sequence

Start from the resume, then ask neutral questions that reveal evidence the document may omit. Cover these areas only as needed:

1. **Role scope** — what the candidate was responsible for, what they owned, and what others owned.
2. **Systems and artifacts** — services, pipelines, applications, data models, infrastructure, experiments, tooling, or operational processes they actually built or maintained.
3. **Scale** — users, traffic, data volume, latency, reliability, cost, team size, frequency, geographic scope, or other relevant scale. Accept `unknown` when not measured.
4. **Decisions** — architecture choices, tradeoffs, migrations, debugging decisions, experiments, or process changes where the candidate exercised judgment.
5. **Outcomes** — measurable results when available; otherwise specific qualitative outcomes. Never force invented numbers.
6. **Failure and repair** — incidents, regressions, difficult bugs, migrations, reversals, or systems the candidate stabilized.
7. **Collaboration** — stakeholders, cross-team work, reviews, mentoring, requirements translation, or handoffs.
8. **Depth signals** — difficult technical constraints, non-obvious implementation details, and why the work was hard.
9. **Career constraints** — authorization, sponsorship, location, schedule, travel, level boundaries, and candidate-selected employer/industry exclusions.
10. **Application facts** — contact details and other repetitive ATS fields that the candidate explicitly verifies.

Do not ask every question mechanically. Follow the strongest evidence and probe until the agent can distinguish strong experience from vague descriptions.

## Resume-readiness assessment

After the interview, compare the resume with the verified evidence. Choose exactly one status:

- `usable_as_is` — the resume represents the candidate's strongest relevant evidence well enough for the target lanes.
- `usable_with_targeted_edits` — the core evidence is present, but a small number of specific omissions or vague bullets are likely to hurt routing or evaluation.
- `materially_undersells_experience` — important verified ownership, technical depth, scope, or outcomes are absent or distorted enough that the resume is not a reliable representation of the candidate for the intended search.

Every assessment must include:

```text
assessment = usable_as_is | usable_with_targeted_edits | materially_undersells_experience
confidence = high | medium | low
confidence_reason = <one sentence>
evidence_gaps = [specific, verified omissions]
search_impact = <which target lanes are affected and how>
```

Confidence means confidence in the assessment, not confidence in the candidate.

Use `high` when the current resume and interview evidence are both detailed and consistent. Use `medium` when meaningful evidence is available but some important scope or outcomes remain uncertain. Use `low` when the resume is incomplete/unreadable, the interview is shallow, or critical facts cannot be verified.

## Hard boundary: no resume generation

Do not draft bullets, rewrite sections, generate a new resume, or modify the candidate's resume during onboarding. It is acceptable to identify missing evidence, name the affected section, and explain why it matters. Resume writing is a separate user-authorized task.

## Completion gate

Application automation can start when:

- identity/application facts required for common ATS forms are verified;
- target lanes and hard exclusions are explicit;
- at least one usable resume route exists;
- resume-readiness status and confidence are recorded;
- material unknowns are either resolved or marked as facts that require candidate confirmation.
