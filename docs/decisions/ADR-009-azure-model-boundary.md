# ADR 009 — Model after authorization and reviewed evidence

## Requirement and risk

The Azure proposal must show where an AI model adds value without suggesting
that a prompt, model citation or JSON schema enforces access and truth. A model
that searches globally, sees restricted excerpts, or freely writes final claims
would reopen the assessment's highest-priority failures.

## Decision

Keep the assessed CPU-only implementation unchanged. In production, start with
Entra-authenticated API authorization, mandatory Search filtering, current and
revocation checks, and approved evidence before a regional Azure OpenAI call.
The first model contract selects bounded evidence IDs. Application code validates
the selection and renders exact approved spans with citations. Missing evidence,
conflict, denial, timeout or invalid output returns a safe state. A later
paraphrasing model requires independent entailment validation and new release
tests; it is not assumed to be safe just because its output is structured.

## Alternative, limitation and acceptance

An autonomous agent with direct Search/tools was rejected as unnecessary and
harder to bound. No model at all remains valid if deterministic quality is
adequate. The narrow model may improve routing but not fluent synthesis, and
production review-state coverage at enterprise scale still needs source-owner
workflow design. `docs/azure-model-integration.md` traces request and content
flows, the contract, failures, Azure services and verification gates. No Azure
resource was deployed and no model was added locally.
