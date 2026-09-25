# ADR 001 Deterministic Local Core

## Status

Accepted for the default assessed path.

## Context

The assessed solution must run on a standard CPU-only workstation without a GPU, Azure account, paid credits, or cloud service. Important claims must remain supported, and the candidate must understand and modify the system during review.

## Decision

Use a deterministic evidence-first local pipeline as the default. Retrieval and answer composition will not require an LLM. A model may be considered later only as an optional, non-authoritative enhancement that cannot weaken the default safeguards.

## Rationale

- Avoids paid or remote dependencies.
- Reduces hallucination risk in the critical path.
- Produces repeatable evaluation results.
- Makes claim-to-evidence behavior inspectable.
- Keeps the implementation small enough to defend and modify.

## Alternatives considered

- A quantized local LLM could improve fluency but adds a large download, CPU latency, and nondeterministic claims.
- A remote LLM would violate the assessed no-cloud path.
- Prewritten responses would be simple but would fail the paraphrase and generalization requirement.

## Consequences and limitations

Answers may be less fluent than generated prose. The implementation must therefore compose clear evidence-backed sentences and bullets without encoding answers for individual mandatory questions.

## Verification

Paraphrased and adversarial evaluation cases must produce equivalent safety properties without exact-question matching.

