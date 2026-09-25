# ADR 008 — Reviewed source spans before claim emission

## Requirement and business risk

A citation can accurately point to attacker-written text inserted into an otherwise
Current, authorized policy. Grok Bot reproduced two out-of-vocabulary directives
that passed the earlier deny-list. This could surface restricted identifiers or
fabricated commitments as apparently grounded claims.

## Decision

`approved_spans.json` is bundled application configuration, separate from the
assessment pack. Each entry approves one exact normalized document/version/line
range/full SHA-256 span. It contains no answer template and no permissions.
Authorization and source eligibility still occur before retrieval. The composer
may emit a candidate only if its exact span was reviewed; the final output gate
independently checks the same approval. A changed or shifted span produces
`insufficient_evidence` with empty claims/citations until a human compares the
new text with the source, confirms business authority and classification, then
updates the entry and runs tests/evaluations. Never auto-approve at runtime.

The former claim-level keyword deny-list was removed: it missed unseen verbs
and rejected legitimate policy language. Unverified-document slicing still
truncates known directive lines, but this is defense in depth, not authority.

## Alternatives and limitation

Expanding the regex is brittle. Auto-normalizing arbitrary Current prose into
facts would create another parser trust boundary. Exact approval is deliberately
conservative: real document edits can temporarily reduce answer coverage, and
human approval can itself be mistaken. It does not make all retrieved excerpts
safe to display or provide a semantic proof for future generative-model output.
The current assessed path is a bounded, CPU-only extractive prototype.

## Acceptance evidence

Both unseen Grok Bot phrasings now abstain without claims or citations. Existing
policy, HR, contract, and migration cases still pass. Changed threshold and SLA
fixtures abstain before review and reflect the new evidence after explicit test
approval. Benign policy wording that matches the old regex answers after review.
The complete 73-test suite, Ruff checks, and ten retrieval/full evaluation cases
pass on September 24, 2026. `submission_ready` remains false.
