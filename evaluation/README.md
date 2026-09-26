# Evaluation Contract

## Build 1 evidence-stage evaluation

Run `python -m apex_assistant evaluate --stage retrieval` from the repository root.
It checks required and forbidden sources, unknown-user denial, absent authorized
evidence, retired-source exclusion, and unverified-source labels for all ten questions.
Results are written to `results/build1.json` and `results/build1.md`.

These are retrieval prerequisites, not final answer judgments. The report explicitly
sets `submission_ready` to false and lists checks deferred to Build 2. A failed check
returns exit code 1; bad configuration returns 2. Tests deliberately break access and
inject an impossible required source to verify the failure path and process exit code.

## Full assistant contract (Build 2)

Run `python -m apex_assistant evaluate --stage full`. The command writes
`results/latest.json` and `results/latest.md` and exits nonzero when a release-blocking
case fails. Any failed case now blocks the overall result even if accidentally
labelled non-blocking; all four required families must be present and at least
one case must be marked release-blocking. Suite-level failures are reported in
`suite_failures`. It evaluates response state, source inclusion/exclusion, independent answer
text properties and claim citation references. Passing the fixed suite is necessary but
does not replace unseen variations, candidate review or production evaluation.
The reviewed-span gate is checked separately in adversarial unit tests; ten
fixed cases alone cannot establish resistance to novel document injections.
The `submission_ready` field remains false until human review, an unseen variation,
video and submission access checks are complete. A fresh local setup passed on
September 23, 2026. See `safety-checkpoints.md`.

`cases.jsonl` is the version-controlled behavioral contract for the local assistant. It contains required outcomes and safety properties, not complete expected answer strings.

## Case fields

- `case_id`: Stable evaluation identifier.
- `family`: Mandatory business-behavior family.
- `user_id`: Supplied authenticated identity or an intentionally invalid ID.
- `question`: Input question.
- `expected_outcome`: Expected response category.
- `required_source_ids`: Evidence that must support the response when applicable.
- `forbidden_source_ids`: Evidence that must not influence observable output.
- `required_concepts`: Semantic properties the evaluator must establish.
- `forbidden_concepts`: Behaviors or claims that must not appear.
- `release_blocking`: Whether failure blocks release.

## Evaluation principles

- Do not compare complete response strings.
- Do not route runtime behavior by case ID or exact question.
- Test citations, decision state, and safe diagnostics in addition to answer text.
- Add paraphrases and input variations for mandatory behavior.
- Keep critical security and unsupported-claim failures release-blocking.
- Unknown required or forbidden concept labels and a case set with no
  release-blocking cases fail closed rather than silently weakening the gate.
- The final command must return a nonzero exit code when a release-blocking case fails.

## Mandatory family coverage

1. Current policy authority over retired or materially conflicting guidance.
2. Unsupported contractual SLA handled without invention.
3. Permission-consistent outcomes for authorized and unauthorized users.
4. Embedded document instructions cannot override policy or expand access.
