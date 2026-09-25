# Safety checkpoints and release rule

Run from the repository root with the installed project environment. Every checkpoint
must pass before sharing a submission candidate. This file describes observable
checks; it does not replace the version-controlled evaluator.

| Checkpoint | Failure it prevents | Evidence | Gate |
|---|---|---|---|
| 1 Identity and permissions | Unknown, denied or inconsistent access entering retrieval | `tests/test_build1.py` and `tests/test_context.py` identity, override, metadata, topic-tree and no-influence tests | Any failure blocks |
| 2 Source authority | Retired or contradictory versions presented as current | Current-policy and two-current-version tests; evaluator source checks | Any failure blocks |
| 3 Claim support | Answer text diverges from its cited normalized lines | `test_every_emitted_claim_matches_authorized_source_lines`; full evaluator span/hash checks | Any failure blocks |
| 4 Changed evidence | Prewritten answers surviving source changes | Changed threshold and newly executed SLA tests | Any failure blocks |
| 5 Safe uncertainty | A missing SLA becomes a numeric commitment | Missing-SLA case and contract mutation | Any failure blocks |
| 6 Untrusted content | Embedded directives affect output or behavior | Migration-note tests; poisoned Current policy, matrix, CONTROL-line and cross-line regressions; benign policy-language control | Any failure blocks |
| 7 End-to-end cases | A scored incident regresses unnoticed | `python -m apex_assistant evaluate --stage full`; optional UI HTTP and fail-closed evaluator tests are in the 64-test suite | Nonzero exit blocks |
| 8 Reproducibility and ownership | Reviewer cannot run or candidate cannot explain work | Fresh local setup and wheel smoke passed; teach-back and unseen modification remain | Incomplete blocks submission |

Commands:

```powershell
.\.venv\Scripts\python.exe -m ruff check src tests
.\.venv\Scripts\python.exe -m ruff format --check src tests
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m apex_assistant evaluate --stage full
```

The fixed evaluator tests source inclusion, response categories, answer concepts,
forbidden claims, authorization, and exact claim-to-source equality. It verifies
the citation's line hash independently from the answer composer. A pass of the
fixed cases is necessary, but the candidate still needs an unseen modification,
teach-back, video, and reviewer-access checks. A fresh local installation passed
on September 23, 2026. The report keeps `submission_ready: false` until the
remaining manual gates are completed.
