# AI Assistance Log

This log records substantial Codex assistance as the work occurs. The final README will summarize the material entries.

| Date | Artifact | Codex contribution | Logic retained | Candidate review or change | Validation |
|---|---|---|---|---|---|
| 2026-09-22 | Project plan and rubric | Analyzed the hiring brief and assessment pack and proposed weighted acceptance criteria and hard release gates. | Prioritize authorization, grounded evidence, repeatable evaluation, and explainability. | Candidate reviewed and approved the three-build plan. | Cross-checked against the supplied brief and corpus. |
| 2026-09-22 | Repository foundation | Drafted `AGENTS.md`, the quest quality-gate skill, project scaffold, rubric, build plan, decision records, evaluation contract, and foundation integrity tests. | Small reviewable changes, authorization before retrieval, deterministic assessed path, and continuous disclosure. | Pending foundation walkthrough and candidate teach-back. | Official skill validation, JSON and TOML parsing, checksum verification, metadata consistency tests, and repository review. |
| 2026-09-22 | ApexOne Project Playbook | Consolidated the assessment scope, deliverables, rubric, release gates, engineering decisions, three-build schedule, learning questions, interview exercises, video plan, and final checklist into one Word document. | Keep security and grounded behavior release blocking; build the smallest general solution the candidate can explain and modify. | Pending candidate review and answers to the foundation questions. | Reopened structurally and rendered through Microsoft Word; all 17 pages were visually inspected for pagination, clipping, numbering, and readability. |

## Entry requirements

Submission README simplification (2026-09-25): At the candidate's request,
Codex rewrote the clean copy's README to put two first-time setup commands,
one everyday launcher action, a first demo question, and two verification
commands before the concise design/disclosure sections. No application behavior
changed. The candidate still needs to perform the setup and final video/reviewer
checks personally.

Clean submission copy and decision tree (2026-09-25): At the candidate's
request, Codex added a plain-language decision tree to the final recording
guide and curated a separate Desktop submission folder. The copy retains the
runnable app, synthetic pack, tests, latest evaluation, Azure design, decision
records and AI disclosure while excluding agent/editor instructions, handoff
notes, stale study material, caches and the machine-specific virtual
environment. A short submission README marks the video and human review as
pending. The curated stage passed 74 tests, Ruff and all ten full evaluation
cases; the Desktop copy was SHA-256-identical before this log entry was synced.
No repository was published or video recorded. Candidate review remains pending.

Final recording guide (2026-09-25): At the candidate's request, Codex created
`docs/FINAL_RECORDING_GUIDE.md` as a concise on-screen speaking aid. It reuses
the verified seven supported and three protective employee/question combinations,
adds a simplified AND/OR/join process explanation, and clearly separates the
current CPU-only app from possible Ollama, Gemini, and regional Azure model
experiments. The training section distinguishes reviewed examples and evaluation
from unimplemented fine-tuning. Official vendor documentation was checked for
model-option descriptions. All ten full evaluation cases passed after the guide
was written; candidate narration, review, video and reviewer-access check remain
pending.

Safe outcome messages (2026-09-25): At the candidate's request, Codex made
unknown-identity, invalid-question and no-access/no-match responses easier to
understand in the local app, with UI labels and a generic source-view hint.
It deliberately did not report “access denied to file X”: that would reveal
restricted source existence. Tests show a restricted and nonexistent case
produce identical Engineering responses and all forbidden/invalid source links
produce the same 404 body. The 74-test suite, Ruff and both ten-case evaluation
stages pass. Candidate review of wording remains pending.

Recording plan (2026-09-25): At the candidate's request, Codex prepared a
6:30 walkthrough plan, seven supported and three intentional safe non-answer
UI combinations, a plain-language process explanation, and a distinct
Azure/model-design segment. The exact dropdown labels and questions were
checked against the current local answer path. No recording was made and
candidate narration, personal introduction, private video link and reviewer
access remain the candidate's responsibilities.

Optional model working draft (2026-09-25): At the candidate's request, Codex
added `docs/MODEL_ADD_ON_WORKING_DRAFT.md` to compare today's no-model process
with possible model insertion points and Gemini 3.5 Flash versus local Ollama.
It cites provider documentation, flags the confidential-data/free-tier and
Azure-only design constraints, and leaves the model's job and provider undecided
for a candidate-led discussion. No runtime code, dependency, model call or
assessment data changed. Candidate review and an actual benchmark are pending.

AI-assisted process expansion (2026-09-25): The candidate clarified that this
file should explain the full conceptual design, not just a narrow model test.
Codex revised it to cover bilingual/typo query understanding, authorized
retrieval, scoped conversational memory, grounded answer drafting, independent
claim checks and bounded repair loops, with unseen safety/evaluation examples.
This is still documentation only. Cross-language entailment, production review
workflow, provider selection and candidate validation remain open.

Azure model placement (2026-09-25): At the candidate's request, Codex expanded
the production-only Azure design with an employee request flow, a narrow model
input/output contract, reviewed-evidence and revocation gates, failure table,
and a staged path to any later paraphrasing. The model selects approved evidence
IDs only; application code owns authorization, final text and citations. This
was checked against current Microsoft Learn guidance for Search security
filters, vector prefilters, deployment residency, structured outputs and Prompt
Shields. No cloud resource or local model was added. Candidate review and
teach-back are pending; code evaluations were not used to claim the Azure
design has been deployed or tested.

Reviewed evidence fix (2026-09-24): At the candidate's request, Codex added a
bundled exact-span approval registry and checks at claim composition and final
verification. It removed the claim-level deny-list that Grok Bot bypassed and
that rejected benign prose. The candidate has not yet reviewed or explained
the design. Disposable tests now cover both new bypass phrasings, a legitimate
policy instruction, and threshold/SLA changes before and after explicit
approval. The 73-test suite, Ruff, and ten retrieval/full cases pass. Human
review of future approved entries remains essential; no model was added.

Hypercontext output contract (2026-09-24): At the candidate's request, Codex
extended the trusted topic map to version 1.1 with a response schema and named
safety checkpoints. It added a final output gate that rechecks authorized
source metadata, effective status/date, exact normalized claim spans, citation
hashes, answer formatting and trusted safety notices. Invalid output returns
`insufficient_evidence` with no claims or citations. This is code-enforced,
not a natural-language prompt or a new permission source. Tests forge claim
text, hashes, identity-crossed citations, notices and extra answer text; 71
tests, lint/format checks, and ten full cases pass. The known semantic
source-contamination bypass remains unresolved and no model was added.

Desktop launch setup (2026-09-24): At the candidate's request, Codex added a
small Windows launcher in the repository and created two Desktop shortcuts:
one starts the local UI, and one opens the existing CODEQUEST folder. The
candidate chose a folder shortcut instead of a duplicate project copy. The
launcher uses the project's virtual environment, selects a free loopback port,
and keeps a visible console so closing it stops that instance. Codex also
opened the trusted hypercontext JSON in the project panel. No model runtime
or authorization behavior changed.

Citation viewer and identity clarity (2026-09-24): After the candidate's live
test transcript, Codex verified that the HR case question answers for the HR
identity but not Engineering. The browser tab containing the transcript was
still set to Engineering, so the visible refusal was consistent with access
rules. Codex added the selected employee label to each question and clickable
citations that open the full authorized normalized source at the cited lines.
The server rechecks authorization, status/date, line range, and hash on each
source request, returning a generic unavailable response on failure. It does
not serve the original PDF/DOCX as if normalized line numbers were page links.
An unseen-phrasing check exposed a missed vacation/time-off paraphrase; Codex
added domain-level leave synonyms rather than an exact-question exception.
Validation: 67 tests, ten full evaluation cases, Ruff, JavaScript syntax, and
a live browser click from an answer citation to its highlighted source line.

Process gateway annotation (2026-09-24): Codex revised the local request and
evaluation diagrams to distinguish XOR route choice, inclusive-OR merging of
eligible authorized source signals, and AND joins for authorization, required
claims, and release-blocking cases. It checked the labels against the current
answer and retrieval code; these are logical gateways, not concurrent workers
or a BPMN engine. Candidate teach-back remains pending.

Topic map and UI redesign (2026-09-24): At the candidate's request, Codex kept
the existing CPU-only answer path and built a bundled hypercontext topic tree
for navigation and rank hints, projected through authorized documents only.
It redesigned the optional browser demo with a Kentrick-inspired dark wordmark,
employee selector, topic-to-file tree, chat composer, citations, and a clear
simulated-identity warning. The official Kentrick site was inspected for visual
direction; no official logo asset was supplied, so the small "K" mark is a demo
mark. Restricted case examples were removed from the static page. Tests cover
topic-schema mapping, identity isolation, an attempted restricted mapping, HTTP
projection, and the existing mandatory outcomes. Validation: 64 tests, Ruff,
JavaScript syntax check, ten full cases, and a live UI check that HR topics and
answers disappear when switching to Engineering. Known unseen prompt-injection
wording remains unsolved; this feature does not claim otherwise.

Second independent security recheck (2026-09-24): Grok Bot found that synonyms,
cross-line wording, alternate sections, matrix text, and a CONTROL line could
still be repeated as cited claims. Codex added five disposable-fixture attack
variations plus a benign-language control, widened the shared directive guard,
and checks the whole normalized claim span. The malicious variations now
abstain without claims or citations; the benign policy instruction still answers.
Ruff, 59 tests, and ten full cases pass. A first full-suite run had an
intermittent Windows connection-aborted error in the cross-origin UI test; that
test passed alone and the complete rerun passed. The candidate has not yet
reviewed or explained this tradeoff, and unseen phrasings remain a limitation.

Independent security recheck (2026-09-24): Grok Bot reviewed the local project
read-only and reproduced an injected directive in a Current vendor policy being
emitted as a cited claim. Codex independently reproduced it, added a disposable
poisoned-policy regression that failed before the fix, and moved the directive
guard into claim validation for all document statuses. Contaminated claims now
cause abstention without citations. The candidate should review the change and
explain why exact source citation alone did not establish that source text was
safe to repeat. Initial validation: 53 tests, Ruff, and all ten full cases passed;
the subsequent Grok Bot recheck is recorded above.

Optional local UI (2026-09-23): At the candidate's request, Codex investigated
Gradio's free chat template and the MIT-licensed Start Bootstrap Simple Sidebar.
Gradio's native dependency was blocked by this Windows machine's application
policy, so Codex adapted the Bootstrap template instead. It added a loopback-only
standard-library server, plain-text answer rendering, demo-identity switching,
HTTP safety checks, tests, README instructions and ADR 005. The existing `answer()`
path remains authoritative; no assessment data was modified. Candidate review and
explanation of the UI's simulated-identity limitation remain pending.

UI clarity and clean-install verification (2026-09-23): At the candidate's request,
Codex added a structured presentation of authorized answer claims and a separate,
minimal source list using the existing `answer()` output. It added the documented
startup-only `--data-dir` option and aligned the UI's default data directory with
the repository-root CLI workflow. A fresh virtual environment installed the
project with development tools and passed 49 tests, Ruff, and ten full cases.
A second environment installed a built wheel offline and started the UI with
bundled template assets. Browser checks covered vendor citations, Engineering
denial, and HR identity switching. The candidate has not yet completed the
teach-back or unseen modification.

Process model (2026-09-23): Codex traced the actual local modules and documented
the request, authorization, retrieval, answer, presentation, and independent
evaluation flows in `docs/process-model.md`. It separated implemented behavior
from the Azure production design and added four incident walkthroughs and a
candidate exercise. The candidate still needs to explain and challenge this
model personally before using it as interview evidence.

Edge-case and study preparation (2026-09-23): Codex added regression tests for
unknown forbidden evaluation labels, case sets without release blockers, and
restricted HR content mutation leaving Engineering answers unchanged. It fixed
the two evaluation-gate weaknesses without changing the answer path. Eight live
question variants were inspected; the retired-policy wording limitation was
recorded rather than scored as solved. The full suite passed 52 tests and ten
cases with Ruff checks. Codex prepared the September 24 study and recording
guide; candidate teach-back, unseen modification, video and access checks remain.

Research review and Azure simplification (2026-09-22): Codex compared the brief,
local implementation, and Azure design with current Microsoft documentation.
It proposed regional Application Gateway ingress, conditional regional model
deployment, incremental Search document updates, immediate revocation checks,
per-document Service Bus sessions only when ordering is needed, and deferral of
optional APIM/AML/Content Safety layers. These decisions are recorded in
`docs/research-review.md` and the Azure architecture and reflected in the 21-page
playbook. Candidate approval and ability to defend the tradeoffs remain pending.
The latest playbook PDF render was visually inspected. The isolated no-dependency
runtime passed the full evaluator; fresh package installation was blocked by
network-restricted access to `setuptools>=68` and remains a release checkpoint.

Evidence-derived revision (2026-09-22): Codex replaced fixed answer prose with
authorized source-section extraction, exact line citations and a content hash.
Added changed-threshold, newly executed Schedule C, injected-directive and
claim/source equality tests. Updated the independent evaluator to verify claim
text and citation hashes against the authorized corpus. Added eight explicit
safety checkpoints and an internal 89/100 rubric assessment. Candidate review,
unseen variation, clean setup, recording and access checks remain pending.

Final review finding (2026-09-22): Codex rendered and visually inspected the
updated 20-page playbook. The fixed-template composer was identified as a material
rubric risk despite passing fixed cases. Removed the fallback citation behavior,
changed `submission_ready` to false, and documented the evidence-derived revision
and adversarial tests still required. Candidate review remains pending.

Builds 2 and 3 (2026-09-22): Codex implemented deterministic grounded answer composition,
claim citations, missing-evidence and conflict states, the full release-blocking evaluator,
Build 2 tests, an Azure-only architecture, migration/operations design, video outline,
README updates and ADR 004. Logic retained: authorized evidence precedes composition;
every emitted important claim requires a citation; unverified prose cannot define behavior;
the Azure API derives identity and mandatory filters before Search and physically separates
restricted HR content. Validation: 39 tests before final hardening, Ruff checks and all ten
full evaluation cases. Final counts are recorded in the latest results. Candidate review,
teach-back, clean-machine verification, video and submission remain pending.

Cursor handoff (2026-09-22): Codex created `CURSOR_START_HERE.md` and `handoff/`
with conversation context, current implementation status, known gaps, rubric provenance,
ordered continuation steps, a reusable starting prompt, and unchanged copies of both
original hiring briefs. Updated `AGENTS.md` to point new sessions to the handoff.
Verified copied briefs by SHA-256 and reran the baseline: 31 tests, lint/format checks,
and ten retrieval-stage cases pass. Full answer evaluation and candidate review remain
pending. No runtime behavior changed and no repository publication occurred.

Build 1 implementation (2026-09-22): Codex generated trusted configuration loading,
authorization, chunking, lexical retrieval, CLI, evidence-stage evaluator, tests, and
documentation. Retained decisions: authorization before scoring, default deny,
deterministic CPU-only retrieval, normalized-line citations, and intact matrix context.
Validation includes restricted-content mutation/removal invariance, broken-access
evaluation, nonzero failure exits, source checks, lint, formatting, and the full test suite.
Final answer behavior is still pending Build 2. Candidate review and teach-back are pending.

September 25, 2026 — Codex investigated unseen questions and typos, then added
conservative static-vocabulary query correction and leave-subtopic selection.
The business logic retained was authorization before retrieval, reviewed exact
source spans before claims, and final citation verification. Two additional
lines of the supplied current leave policy were explicitly reviewed and
hash-registered; no assessment data was edited. The candidate should review
the distinction between deterministic evidence answers and true model-written
summaries. Validation: 83 tests, all ten full evaluation cases, and Ruff checks.

September 25, 2026 — Codex added a bounded conversational handler for
greetings, help, and thanks. This is application-owned text, not document
evidence or an LLM output. Identity validation precedes it; mixed prompts
continue through authorized retrieval; the final verifier rejects any altered
small-talk reply. Focused, full-suite, and end-to-end evaluation checks were
used to guard the existing assessment behavior.

September 26, 2026 — Codex rechecked the submitted P6 HR answer against the
authorized case citation and source viewer, strengthened the regression test
for that exact source, and rewrote the GitHub README in plain text with a
simple process flow and ten copy-paste cases. No runtime behavior or supplied
assessment files changed. The 96-test suite and all ten full evaluation cases
passed; reviewer access to the video remains a manual check.

For each substantially assisted artifact, record:

1. The tool used.
2. What was generated or suggested.
3. The underlying logic retained and why.
4. What the candidate changed, rejected, or approved.
5. How the result was tested, secured, or otherwise validated.
