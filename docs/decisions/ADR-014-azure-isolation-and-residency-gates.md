# ADR 014 — Azure isolation and residency are launch gates

## Requirement and business risk

The quest requires zero unauthorized influence, including ranking and diagnostics,
and services/data within an approved Azure region. A Search result filter can hide
restricted rows while mixed-index BM25 statistics still alter authorized ranking.
Revoked chunks can do the same before index deletion. Choosing a resource region
does not prove every managed service or existing identity/source dependency stays
in that single region.

## Decision

The proposed production path admits only access-equivalent Search collections:
every indexed chunk must be visible to every principal routed to that collection.
The API still applies mandatory filters and live eligibility checks. A collection
is quarantined before acknowledging revocation, retirement or ACL changes that
break that invariant, and remains unavailable until cleanup and verification.
Documents with ACLs that cannot be safely partitioned are excluded from the
first answerable launch scope. Normal telemetry omits source identifiers and
content. Service-by-service processing, replication, backup and telemetry
locations must be approved before deployment; an unproven path does not launch.

## Alternative and limitation

One mixed-access Search index with security filters is cheaper and simpler, but
does not establish the strict no-ranking-influence outcome. A filter-only or
application-owned authorized-candidate ranker could later cover overlapping ACLs,
but needs its own quality and latency proof. Collection quarantine reduces
availability, and many overlapping ACL scopes may make index fan-out expensive.
The design is not deployed or measured, and Entra/source-system residency may
require an explicit organization-approved exception.

## Acceptance before production

Mutating denied content must not change an unauthorized caller's candidate set,
ordering, answer, citations or ordinary telemetry. Revocation races must show
no query to a dirty collection after event acknowledgement. Measure end-to-end
p95 under six seconds at 20 requests/second with concurrent updates and the
production-shaped corpus; set and test an owner-approved freshness and cost
budget. Document the approved-region evidence for every dependency. Any failed
security or residency gate blocks launch rather than being hidden by a prompt.
