# ADR 002 Authorization Before Retrieval

## Status

Accepted.

## Context

The assessment treats any influence from inaccessible information as a critical security failure, including influence on answers, references, diagnostics, and operational records.

## Decision

Resolve the trusted user identity and compute the accessible document set before retrieval or scoring. The retriever receives only authorized evidence. Unknown or inconsistent identity and entitlement states fail closed.

## Rationale

Filtering after retrieval would still allow restricted content to affect ranking, candidate counts, latency, traces, and error output. Pre-retrieval authorization removes that influence boundary.

## Alternatives considered

- Post-retrieval filtering is simpler but fails the no-influence requirement.
- Prompt-only instructions are not a security boundary.
- A separate index per user is unnecessary locally and would complicate maintenance; the Azure design may use physical separation for the highest-sensitivity collections.

## Consequences and limitations

Authorization metadata becomes part of the trusted computing base. Missing, unknown, or inconsistent metadata must deny access rather than silently degrade.

## Verification

Tests must prove that restricted identifiers and content never appear in unauthorized retrieval results, answers, citations, diagnostics, or logs.

