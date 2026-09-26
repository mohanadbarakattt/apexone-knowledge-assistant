# ADR 013 — Full evaluation cannot hide a failing case

Requirement: the four critical business safeguards must be repeatable and
release-blocking. Previously, a failed case labelled non-blocking could coexist
with an overall pass. That metadata mistake could conceal a security regression.

Decision: full evaluation passes only when every included case passes, all four
required families exist, and at least one release-blocking case is declared.
Suite-level failures are explicit in JSON and Markdown. The existing CLI maps a
failed overall result to exit code 1. No assistant answer behavior changes.

Alternative: trust case authors to tag all critical tests correctly. Rejected
because this small assessment suite benefits more from a strict gate than from
optional failing experiments. Exploratory cases should run separately.

Limit: a family label does not prove a good test, and a passing fixed dataset does
not prove general correctness. Keep adversarial tests and candidate review.

Acceptance: a deliberately wrong non-blocking case and a missing malicious-document
family both fail; the intact assessment suite remains green. Practise reproducing
the failure through the CLI, not only reading a passing report.
