# ADR 007 — Trusted output contract and final answer gate

## Requirement and risk

The candidate requested an output format and built-in safety rules in the
hypercontext file, ahead of considering a model. A text-only rule list would
look protective while leaving the runtime unchanged. Letting the file define
permissions or override source authority would be worse.

## Decision

Keep `hypercontext.json` as bundled, trusted application configuration. Version
1.1 adds a response shape, allowed outcome states, exact-span/citation format,
and named safety checkpoints. `context.py` rejects missing or weakened
declarations. The existing `Catalog` remains the only authorization authority;
the topic map still cannot grant access or create claims.

After the deterministic composer runs, `safety.verify_answer` checks the output
against documents authorized for that identity and effective date. It verifies
the required fields and state, citation metadata and line hash, claim text
against the cited normalized lines, use of every citation, and absence of extra
answer text outside trusted safety notices and cited claim bullets. A failed
check produces `insufficient_evidence` with no claims or citations. This gate
also applies to CLI and UI because both call `answer()`.

The rules named `identity_and_metadata_default_deny`,
`authorize_before_search_or_ranking`, and `current_and_effective_source_only`
describe controls enforced earlier in the pipeline. The final gate does not
move those checks or use topic mappings as permissions. The current notice
field accepts only application-owned safety wording; it is not free-form model
output.

## Alternative and limitation

A long natural-language system prompt in the hypercontext file was rejected:
the current local path has no model, and prompt text is not a security boundary.
A fully curated fact database could prevent more source-text contamination but
would require a separate content-review/update workflow and could lag policy
changes. The selected final gate catches structural unsupported output; it
does **not** prove semantic entailment of arbitrary source prose. ADR 008 later
added exact reviewed-span approval to close the demonstrated bypass. A future model
must not be connected until its draft schema and semantic claim checks are
designed and adversarially tested.

## Verification

Tests mutate the contract, forge a claim, append unsupported answer text,
tamper with a citation hash, substitute an HR citation for an Engineering
answer, and patch the composer to return unsupported text. The gate rejects
those variants. The full 71-test suite and ten release-blocking evaluation
cases pass after this change.
