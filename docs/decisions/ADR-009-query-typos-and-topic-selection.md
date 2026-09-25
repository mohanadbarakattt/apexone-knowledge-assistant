# ADR 009 — Conservative query correction and leave-topic selection

## Requirement and risk

Employees ask unseen questions with spelling mistakes. The prior router missed
"vaccation" and answered a sick-leave question with the annual-leave rule.
Missing a relevant answer hurts usability; presenting the wrong leave rule can
mislead an employee.

## Decision

Normalize only question words against a small, static navigation vocabulary.
Accept a correction only for a word of at least five characters with a unique,
high-similarity match. Never correct identifiers or source text. Use the
normalized question for intent and retrieval, *after* the existing document
authorization boundary. Select sick and emergency/family leave evidence from
their own exact, reviewed policy lines; annual leave remains the default for
unqualified leave and vacation wording. The two additional source lines were
reviewed against the supplied current policy and registered by exact hash.
Final claim/citation verification is unchanged.

## Alternative and limitation

An LLM could interpret more languages, typos, and nuanced subquestions, but
would require a separate answer-verification design and a model dependency.
This patch stays CPU-only and deterministic. It does not handle every typo or
answer every question in the corpus; unsupported topics still abstain. The
existing answer format remains extractive, so natural-language synthesis is a
future, separately gated capability, not a claim of this release.

## Acceptance

Unseen procurement phrasings, misspelled vacation and contractual response,
sick/emergency leave, restricted-case denial, and unrelated-question abstention
are covered in `tests/test_unseen_questions.py`. All 83 tests and all ten full
evaluation cases pass on September 25, 2026; Ruff checks pass.
