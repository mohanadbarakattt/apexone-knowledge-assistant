# ADR 003 Build 1 evidence retrieval

## Decision

Keep identity and entitlement configuration separate from document prose. Intersect
classification access, document allowed groups, and override allow groups; explicit
deny groups take precedence. Duplicate identities, ambiguous rules, and unknown
override targets fail configuration loading. Invalid or inconsistent document
metadata makes the document unavailable without an explanatory public diagnostic.

Authorize before chunking and scoring. Scores use only each authorized candidate's
text, title, and section; no corpus-wide document frequencies or restricted counts
enter ranking. Current retrieval excludes retired, unknown-status, and future records.
Status eligibility is not complete authority resolution, which belongs to Build 2.

Use numbered sections and overlapping line windows, with source line spans and content
hashes for citations. Preserve the flattened matrix as a whole: guessing row boundaries
could associate a financial threshold with the wrong approvers. This deliberately
adjusts the planned row-chunk strategy to the supplied normalized data.

Use lexical overlap, a small domain vocabulary map, title/section weights, and character
trigrams. No evaluation case IDs, full-question matches, or prewritten answers appear
in runtime retrieval. Sensitive records require a specific identifier or descriptive
title match to avoid exposing irrelevant investigations in broad leave searches.

## Alternatives and limits

Post-search filtering fails the information-flow requirement. A global lexical index
could allow inaccessible documents to change IDF scores. Embeddings add dependencies
before there is evidence they are necessary. Whole-document retrieval loses citation
precision, but is preferable to incorrectly splitting the supplied flattened matrix.

The sensitive-record rule is conservative and heuristic, not a substitute for access
control. The CLI identity is a simulation; local files and local operators are trusted.
Startup parsing and authorization enumeration are not constant-time. Malformed shared
configuration can affect availability. We test answer-visible evidence and ranking
independence, not the absence of every possible timing side channel.

## Validation

Unit and CLI tests cover deny precedence, unknown/malformed configuration, metadata
disagreement, duplicate records, authorized HR access, restricted-content mutation and
removal invariance, citation integrity, paraphrases, and retired/future exclusion.
Evidence-stage evaluation runs all ten supplied questions and checks required/forbidden
sources and denial states. It explicitly leaves final-answer requirements unevaluated.
A deliberately broken authorization boundary fails evaluation; a failed CLI case exits 1.
