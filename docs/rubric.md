# Assessment Rubric and Release Gates

## Hard release gates

The submission is not releasable if any of the following occurs:

- Restricted information affects an unauthorized answer, citation, score, diagnostic, log, or other observable behavior.
- The assistant presents an important unsupported claim without a safe fallback.
- Retired policy is presented as current guidance.
- Document-embedded instructions change system behavior, permissions, or tool use.
- An unknown or invalid identity receives access.
- A citation does not support its associated claim.
- Documented setup, run, test, or evaluation commands fail.
- Substantial AI assistance is undisclosed or cannot be explained and validated.

## Weight provenance and internal targets

The earlier user-supplied quest listing states the weights below (archived in
the development handoff). The newly supplied brief repeats the five categories
but omits numeric percentages. These weights are from the earlier listing,
not inferred from the latest paste. The target column is our own planning
target, not a reviewer score or evidence that the project earned those marks.

| Area | Weight | Target |
|---|---:|---:|
| Retrieval and grounded behavior | 25 | 22 |
| Security and Responsible AI | 25 | 25 |
| Evaluation and tests | 20 | 18 |
| Architecture and software quality | 20 | 17 |
| Judgment and ownership | 10 | 9 |

Internal ambition: at least 90 out of 100, with every hard release gate passing.
No numerical score is claimed. Passing a fixed test suite does not establish
answer quality on arbitrary questions, production readiness, or candidate ownership.
Use `docs/requirements-review.md` for evidence and remaining verification work.

## Retrieval and grounded behavior

- Relevant evidence is found for reasonable paraphrases.
- Current policy, retired policy, matrices, agreements, and scoped advisories are distinguished correctly.
- Every important claim has traceable supporting evidence.
- Missing or weak evidence produces a useful refusal or qualification.
- Responses are useful and readable rather than raw search results.

## Security and Responsible AI

- Authorization is enforced before retrieval.
- Restricted information cannot influence unauthorized processing.
- Answers, citations, logs, diagnostics, and errors contain no unauthorized details.
- Embedded instructions cannot override system policy.
- Failed identity, entitlement, or retrieval dependencies fail closed.

## Evaluation and tests

- All four mandatory case families are represented.
- Authorized and unauthorized identity variations are tested.
- Paraphrases and adversarial variations prevent exact-question hardcoding.
- One repeatable command produces readable and machine-readable results.
- Critical failures block release automatically.
- Latest results and conclusions are committed.

## Architecture and software quality

- The Python implementation is focused and understandable.
- The local flow and trust boundary are explicit.
- The Azure design traces both employee-request and content-change flows.
- Important Azure services have responsibilities, rationales, and alternatives.
- Scale, latency, reliability, residency, security, operations, and cost are addressed.
- Migration priorities are practical.

## Judgment and ownership

- Scope follows the business risks and assessment weights.
- Assumptions and limitations are candid.
- Alternatives and trade-offs are defensible.
- AI assistance is accurately disclosed.
- The candidate can explain and safely modify every submitted artifact.
