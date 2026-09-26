# Requirements and grading review

Reviewed against the newly supplied Kentrick.ai brief on September 26, 2026.
This is a traceability check, not a predicted recruiter score.

## Scope that matters

The local requirement is a CPU-only, no-cloud, retrieval-grounded assistant using
the supplied normalized corpus. A generative model is optional and must be
justified; PDF parsing, a UI, real authentication and production load testing
are not local requirements. Extra features earn no credit unless they improve
a required business outcome. The Azure production proposal must be Azure-only.

## Deliverables and evidence

| Requirement | Submitted evidence | Review conclusion |
|---|---|---|
| Local question + supplied identity interface | CLI and optional browser UI; README commands | Implemented; identity selection is a simulation, not authentication. |
| Current, relevant, traceable answers | `assistant.py`, `reviewed.py`, citation verifier; policy/matrix/Legal cases | Tested on supplied corpus. Reviewed spans are evidence, not prewritten complete answers; fixed intent/section routing still limits unseen questions. |
| Missing contractual SLA | Full evaluation contract case | Safely qualifies missing evidence and asks for executed schedule; no numeric invention. |
| Permission-consistent Engineering and HR outcomes | Paired leave/case tests, restricted-content mutation tests, UI source checks | Tested; authorization precedes chunking and scoring. P6 resolves only to case 778 v1.0 for HR. |
| Malicious document remains data | Migration case, poisoned Current-document tests, exact reviewed-span gate | Tested against known attacks. Human approval quality and source freshness remain limitations. |
| Four repeatable release-blocking families | `evaluation/cases.jsonl`, full evaluation command, latest reports | Ten cases cover the four families. Any case failure or absent family now blocks overall pass. |
| Compact flow, alternatives, configuration and limitations | README, process model, decision records | README includes the flow/test pack and now names configuration and alternatives. |
| Azure diagram, component map and alternatives | `azure-architecture.md`, `azure-model-integration.md` | Design only. Eligibility store and latency headroom clarified; regional availability, scale and isolation need validation before deployment. |
| Azure lifecycle, retries, failures, scale, latency, cost and releases | Architecture content lifecycle and operations sections | Proposed controls, not measured production achievements. First investments are secure ingestion/retrieval, then evaluation/observability. |
| 5–7 minute decision video and reviewer access | README video link | Link supplied by candidate. Duration, anonymous access and required Azure walkthrough have not been independently verified. |
| AI disclosure and personal ownership | README note and assistance log | Assistance disclosed. Candidate explanation/debugging ability cannot be certified by tests or by Codex. |

## Grading priorities

The earlier supplied quest listing explicitly gave these weights. The latest
paste retains the categories but does not restate percentages.

| Area | Earlier official weight | Evidence to defend, not merely show |
|---|---:|---|
| Retrieval and grounded behaviour | 25% | Why current policy, matrix and scoped memo are combined; why a citation alone does not prove a claim; limits of the intent router. |
| Security and Responsible AI | 25% | Deny before retrieval; no denied metadata in output; document instructions cannot grant authority; changed evidence fails closed. |
| Evaluation and tests | 20% | Repeatable cases, adversarial mutations, exit codes, and how a failing or removed case blocks release. |
| Architecture and software quality | 20% | Named Azure services, both data flows, failure/retry semantics, region constraints, operational budgets and alternatives. |
| Judgment and ownership | 10% | Explain the model-free choice, admit bounded coverage and manual review costs, and safely modify an unseen variation without assistance. |

The former 90/100 target is an internal ambition, not an achieved grade.
Disqualifying risks take precedence over weighted totals: unauthorized influence,
confident unsupported claims, broken documented commands, inability to explain or
change the work, and undisclosed or unvalidated AI assistance.

## Remaining checks the candidate must perform

1. Watch the submitted video: it must show a useful answer and a protective case,
   explain the main risk/limitation, trace an Azure employee request AND content
   change, and state the first investment and regression detection approach.
   Talking only about a future model does not satisfy the Azure walkthrough.
2. Verify video/repository access without the candidate's login. Confirm the
   invitation deadline, timezone and channel; these are not in this pasted brief.
3. Practise changing a policy threshold in a disposable fixture, explain why it
   abstains until review, and add an unseen paraphrase test. Do not silently
   update approval hashes just to make tests green.
4. Do not describe the prototype as general natural-language reasoning, Arabic
   support, production authentication, deployed Azure, or proven 20 RPS/p95 SLO.
   Those capabilities were not implemented or validated by this review.

No new UI, agent framework, cloud deployment or paid model is needed to close
these assessment requirements. Prioritize evidence quality, security and the
candidate's ability to defend the implementation over additional polish.
