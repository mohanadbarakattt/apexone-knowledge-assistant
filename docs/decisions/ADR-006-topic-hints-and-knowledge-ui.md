# ADR 006 — Hypercontext topic hints and employee-facing UI

## Requirement and risk

The candidate wants a chat-like program with an employee selector and a visible
tree of business topics mapped to relevant files. A global context file that
contains all prose, permissions, or instructions could leak restricted metadata,
override access rules, or turn untrusted text into answers.

## Decision

Keep the existing `Catalog` as the only access authority. Bundle a small,
versioned `hypercontext.json` with topic labels, keywords, document IDs and
example questions. `context.py` validates its shape, matches topics only after
authorization, and projects a topic tree using only the selected employee's
authorized, eligible documents. Retrieval uses matching topics as a small rank
boost after the existing relevance threshold, never as a hard filter or source
of claims. Unknown questions retain ordinary lexical search.

Adapt the existing MIT-licensed Bootstrap sidebar into a Kentrick-inspired
chat layout: dark navigation, local topic tree, demo employee selector, plain
text claims and citations, and a clear simulated-identity warning. Keep the
same core `answer()` path for CLI and UI. The "K" demo mark is not an official
logo asset; replace it if an approved logo file is supplied.

## Alternative and limitation

A single giant prompt/context file would be simpler to write but would mix
permissions, source authority, and untrusted prose. Hard topic filtering could
lose valid paraphrases; the rank hint retains fallback retrieval. This topic
map is hand-maintained for the small assessment pack and does not solve the
open-ended claim-contamination problem or constitute a production taxonomy.
The local selector is not authentication and must remain loopback-only.

## Verification

Tests verify topic targets, unknown users, authorized tree projection, an
attempted restricted-document mapping, and the HTTP boundary. A live browser
check showed Engineering without the investigation topic; HR with that topic
and a cited answer; then Engineering again with the HR answer cleared. The
64-test suite and ten full evaluation cases pass after this change.
