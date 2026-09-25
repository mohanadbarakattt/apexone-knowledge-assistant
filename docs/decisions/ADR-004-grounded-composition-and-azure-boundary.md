# ADR 004 Grounded Composition and Azure Boundary

**Later decisions:** ADR 008 supersedes the claim-level pattern guard with
reviewed exact spans. ADR 009 narrows the first Azure model to evidence-ID
selection after authorization and review. The historical text below records
the earlier design and should not be read as the current runtime contract.

## Decision

Use deterministic intent classification to select authorized document sections. Answer claims are
extracted from current source lines and carry exact line and content-hash citations. The full
evaluator independently compares each claim with the trusted corpus, checks required and forbidden
answer properties, and validates the citation hash. Current-version conflicts produce a conflict
state. Unverified source text can support a qualified summary but cannot define instructions,
permissions or actions.

Every selected claim, including one from a Current document, is checked for
instruction-like source text before citation or answer assembly. A contaminated
claim causes safe abstention with no claim or citation; silently trimming the
line would make the cited span misleading. This is an output-integrity guard,
not a claim that a regex can recognize every possible prompt injection.
The guard scans the normalized whole claim, so a directive split across lines
cannot evade a line-local check. It covers instruction overrides, claimed system
notes, disclosure of restricted material, and fabrication commands. Ordinary
policy instructions such as ignoring informal requests remain usable. Unseen
phrasing and false positives remain a limitation of deterministic screening.

For Azure, resolve Entra identity and trusted groups in the API before Search. Apply mandatory
document security filters and physically separate the restricted HR index. Send only authorized,
authority-checked excerpts to Azure OpenAI. Treat preview-native ACL features as future options.
Use regional Application Gateway WAF for ingress under the approved-region constraint,
not a global edge by default. Incrementally update individual Search documents and
apply an immediate trusted revocation gate; reserve index aliases for bulk rebuilds.
Regional model-processing guarantees must be validated before launch. Defer APIM,
AML pipelines and additional classifiers until a measured need justifies them.

## Tradeoffs and limitations

Extractive answers are predictable and inspectable but cover a bounded set of business intents. Pattern-based
evaluation is transparent but does not prove semantic entailment for arbitrary language; production
adds model-assisted claim verification under the same release gates. Separate indexes cost more and
complicate operations, but reduce the blast radius of filter errors for the highest-sensitivity data.
The previous fixed claim wording was replaced because it was too close to the brief's prohibited
prewritten mandatory answers. The extracted answer now follows changed source facts. The remaining
limits are heading-dependent extraction, bounded intent routing, and the lack of broad semantic
entailment testing; these must be explained during the candidate review.
Small domain-level aliases (for example, vacation and time off as leave requests)
improve reasonable paraphrase recall. They are vocabulary rules, not exact-question
answers; they do not relax source authorization or claim validation.

## Verification

Tests cover paraphrases, changed source facts, missing/new SLA, permission-consistent outcomes,
malicious directives, current-version conflict and nonzero evaluator failures. The ten supplied
cases pass the full evaluator. Exact claim/source equality and citation hashes are checked.
An independent Grok Bot review found that an instruction embedded in a Current
policy could previously be emitted as a cited claim. The poisoned-policy
regression failed before this change and passes after it. A second Grok Bot
recheck found synonym, split-line, alternate-section, matrix, and CONTROL-line
bypasses. The five disposable-fixture regressions now abstain, while a benign
instructional policy line still answers. The 59-test suite and ten full cases
pass on September 24, 2026.
Azure claims were checked against current Microsoft Learn documentation on September 22, 2026.
The September 23 edge pass added fail-closed handling for unknown forbidden
concept labels and case sets without a release-blocking case. A restricted HR
content mutation also left Engineering answers exactly unchanged.
