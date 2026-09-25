# ADR 010 — Helpful outcome messages without source enumeration

## Requirement and risk

The candidate wants errors to explain what happened—for example, when the
selected employee cannot open a source. A message that names a denied file or
says “you lack access to case X” would disclose that restricted material exists.
The same source-view URL must not reveal whether a citation is forbidden,
missing, stale, malformed or tampered with.

## Decision

Keep machine-readable outcome states and the authorization checks unchanged.
Give unknown identity and invalid question distinct core messages. For
`no_authorized_evidence`, use one helpful but non-enumerating message: evidence
available to this identity does not answer; the information may be unavailable,
restricted or not found, and the employee can contact an information owner.
This exact message is returned for both a known restricted case and a
nonexistent case when neither has authorized evidence.

The optional UI translates each state into a plain-language label. Its source
viewer keeps one generic 404 for denied, missing, stale and invalid citations;
the visible dialog says the source is not available to the selected employee
or the link may be invalid/changed. It never names an inaccessible document.
The UI does not infer a new access reason from the user's question.

## Alternative, limitation and verification

Per-document “access denied” errors were rejected because they would become
an existence oracle. The state-level explanation is less specific, but it is
truthful for both denied and absent material. The local employee selector is
still a simulation, not authentication.

Tests compare restricted and nonexistent case responses byte-for-byte for an
Engineering identity, check distinct identity/request messages, and verify
identical 404 bodies for forbidden and invalid citations. The complete 74-test
suite, Ruff checks and both ten-case evaluation stages pass. `submission_ready`
remains false pending candidate and submission checks.
