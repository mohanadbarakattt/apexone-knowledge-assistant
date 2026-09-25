# ApexOne Knowledge Assistant

A small, local app for answering employee questions from the supplied **synthetic** company documents. It shows evidence for supported answers and safely declines when information is missing or outside the selected employee's access. The local app needs **no AI model, Azure account, GPU, or paid API**.

## Start the app — Windows

You need **Python 3.11 or newer**. Open this folder in File Explorer, click its address bar, type `powershell`, and press Enter. Run these **two lines once**:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
```

Then **double-click `Start ApexOne Assistant.cmd`**. It opens the app in your browser. Keep its black console window open while using the app; close the window to stop it.

**On the current candidate PC only:** Python is already installed but not on PATH. Replace the **first** setup line with this one; the second line stays the same:

```powershell
& "C:\Users\user\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m venv .venv
```

On another PC, if `python` is not recognized, install Python 3.11+ with the “Add Python to PATH” option, reopen PowerShell, and repeat the two setup lines. Installation may download Python packaging and test tools; **running** the app needs no network connection. The app stays on your own computer (`127.0.0.1`); do not expose it publicly.

### Try one question

In the app, select **Leila Mansour (Procurement)**, then paste:

```text
What is our process for approving a new enterprise vendor?
```

The answer should use the current vendor policy and approval matrix. Click a citation to see its authorized normalized source lines. The employee dropdown is a **demo identity selector**, not a real sign-in. More copy-paste examples are in the [recording guide](docs/FINAL_RECORDING_GUIDE.md).

## Check the result

Open PowerShell in this folder and run:

```powershell
.\.venv\Scripts\python.exe -m apex_assistant evaluate --stage full
.\.venv\Scripts\python.exe -m pytest -q
```

The first command tests ten business cases and writes `evaluation/results/latest.json` and `latest.md`. A critical failure gives a nonzero exit code. The latest checked run passed all ten cases and 83 tests, including unseen wording and spelling mistakes. Answers remain evidence-grounded extracts, not free-form AI summaries. `passed: true` is **not** the same as `submission_ready: true`; candidate review, the recording, and reviewer-access checks remain. See the [evaluation contract](evaluation/README.md) and [safety checkpoints](evaluation/safety-checkpoints.md).

For a command-line question instead of the browser:

```powershell
.\.venv\Scripts\python.exe -m apex_assistant ask --user u-proc-310 --question "What is our process for approving a new enterprise vendor?"
```

## What the program does

```text
Check employee → allow documents → search current evidence → verify claims and citations → answer or safely decline
```

- **Permission first:** documents the employee cannot use never enter search or ranking. An unavailable response does not reveal whether a private file exists.
- **Evidence first:** important claims come from reviewed, authorized source lines; the final check verifies citations. Current policy outranks retired policy, and a missing contractual SLA is never invented.
- **Safe documents:** instructions embedded in a document cannot change app rules or permissions. The trusted hypercontext file helps navigation but is not a source of business facts or access rights.

The app reads `data/assessment/normalized/corpus.jsonl` and its trusted manifest/access files. Original PDF/DOCX files are reference material and are not parsed at runtime. The [simple process model](docs/process-model.md) and [decision records](docs/decisions/) explain the boundaries and alternatives. The main limitation is narrower language coverage than a carefully verified model-assisted system; reviewed evidence also needs reapproval when source text changes. Citations point to normalized text lines, not PDF pages.

## Azure design and AI use

The [Azure architecture](docs/azure-architecture.md) is a **design only**: it shows employee and content flows, services, access controls, operations, trade-offs, and migration priorities. No Azure resources were created. A [possible model extension](docs/azure-model-integration.md) places a regional model after authorization and evidence checks; **no model or agent runs in this local app**.

Codex substantially assisted the source, UI, tests, evaluator, Azure design, and documentation. The candidate selected the scope and key controls—permission before search, default deny, reviewed claims, final citation checks, and release-blocking tests—but personal review and ability to explain or modify the work are still pending. See the detailed [AI-assistance log](docs/ai-assistance-log.md). Do not claim candidate-only authorship or completed review.

## Before submission

**Video link:** pending the 5–7 minute recording and reviewer-access check. Add the private/unlisted URL here after filming. Publish this folder as a reviewer-accessible repository only after completing candidate review and final checks.

The bundled UI adapts Start Bootstrap Simple Sidebar; see `src/apex_assistant/web/THIRD_PARTY.md` and its MIT license. The Kentrick-inspired “K” is a demo mark, not an official logo.
