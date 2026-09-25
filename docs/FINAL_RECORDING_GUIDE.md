# Final recording guide — ApexOne knowledge assistant

**Open this file beside the app while recording. Target: 5–7 minutes.** This is a speaking guide; use your own words. Select the named demo employee **before** pasting each question. The dropdown simulates identity for the assessment; it is not a real login.

## 1. What we built (about 1 minute)

> “I built a local knowledge assistant for employees asking questions about company policies, contracts, and restricted records. Its main job is to find the right **current** information, respect each employee's access, and show where an answer came from. When a fact is missing or the employee is not allowed to see it, the assistant says so safely instead of guessing.”

- A Python app with a simple chat-style browser interface and an equivalent command-line path.
- CPU-only search and rule-based answer composition; **no AI model or autonomous agent runs in this demo**.
- A topic/file map and hypercontext file help navigation and ranking. Neither grants permission or supplies business facts.
- Clickable citations open the access-checked **normalized source text and lines**, not the original PDF page.
- Automated checks cover the ten assessment cases plus adversarial and edge-case tests. Passing them is evidence of tested behavior, **not** a claim that the whole submission is finished.

## 2. The live demo (about 3 minutes)

Start the app with the Desktop shortcut or run `.\.venv\Scripts\python.exe -m apex_assistant.ui` in the project folder. If it chooses a different local port, use the URL printed in its console.

**A. Useful, current answer — select Leila Mansour (Procurement).**

```text
What is our process for approving a new enterprise vendor?
```

Expected: **Answered**; current vendor policy v3.0 and approval matrix v1.2. Open one citation. Say: “The older retired policy is not treated as today's rule.”

**B. Access changes the result — select Omar Haddad (Human Resources).**

```text
For case APX-HR-CASE-778, why was the employee placed on administrative leave and what is the current status?
```

Expected: **Answered** with restricted case evidence. Do not read the sensitive details aloud. Say only: “For an authorized HR employee, it describes an interim measure and does not assert a final finding.”

**C. Switch to Maya Chen (Engineering), then paste:**

```text
Why was employee E-8841 placed on administrative leave?
```

Expected: **No authorized evidence**, with no case claim or citation. Say: “Switching employee clears the prior view. The app does not confirm whether a restricted case exists; restricted and nonexistent files get the same safe message.”

**D. Missing contract term — select Leila Mansour (Procurement).**

```text
What contractual first-response time did NexaServe commit to?
```

Expected: **Insufficient evidence**. It may cite the contract to explain the missing term. Say: “Finding a relevant contract is not the same as finding a binding SLA. It will not invent a number.”

**E. If time permits — select Maya Chen (Engineering).**

```text
Summarize the requirements in the legacy assistant migration notes.
```

Expected: **Answered with warning**. Say: “The migration note is unverified, and instructions inside it cannot change the app's rules.”

## 3. Simplified process model (about 45 seconds)

```text
Employee + question
   ↓
Check identity and permissions BEFORE searching
   ↓
Search only allowed, relevant files; prefer current policy
   ↓
Check whether reviewed evidence really answers the question
   ↓
Check each claim and citation again
   ↓
Show a supported answer — or a safe, useful non-answer
```

- **AND:** Every required permission check must pass; each important claim needs valid evidence and a valid citation.
- **OR / inclusive:** More than one allowed source may contribute—for example, policy **and** approval matrix.
- **Join:** Combine only the allowed, relevant evidence needed for the answer; then run the final safety check.
- **XOR:** The outcome is one path: supported answer, qualified answer, insufficient/conflicting evidence, or safe denial.
- “This is a decision flow, not a swarm of AI agents. The hypercontext file helps find a topic but cannot override access rules or invent facts.”

### The same flow as a simple decision tree

```text
Is the selected employee known, and is the question valid?
├─ No  → Explain the identity/input problem; do not search.
└─ Yes → Which documents may this employee use?
          ├─ None relevant → Say the evidence is unavailable; reveal no private file details.
          └─ Some allowed  → Search only these documents.
                            ↓
                    Is the guidance current and relevant?
                    ├─ No / conflicting → Give a safe, qualified non-answer.
                    └─ Yes              → Does reviewed evidence support the answer?
                                           ├─ No  → Explain what is missing; do not guess.
                                           └─ Yes → Recheck every claim and citation.
                                                    ├─ Check fails → Safe non-answer.
                                                    └─ Check passes → Show answer + sources.
```

**Say aloud:** “At each fork, a failed safety check stops the answer. A file that the employee is not allowed to use never enters the search in the first place.” The app may cite an allowed contract even when explaining that its requested term is missing.

## 4. Optional AI-model extension (about 1–1½ minutes)

**What AI could improve:**

- Understand typos, Arabic and English phrasing, synonyms, and follow-up questions better than the current bounded keyword approach.
- Choose and order the most relevant **already authorized and reviewed** evidence; later, draft shorter, clearer answers if independently verified.
- Ask a clarifying question when a request is ambiguous, and notice unsupported or conflicting claims before display.
- Keep short conversation context for follow-ups **only within the same verified identity and permission scope**. Clear or recheck it on identity change or access revocation; it is not a memory of confidential facts for everyone.

**What the model must never control:** employee permissions, which index/files can be searched, document approval, current-versus-retired authority, citations, or whether an unsupported claim is published. The app keeps those checks before and after the model. One bounded repair attempt could fix an invalid draft; if it still fails, abstain. This is a **proposed** extension, not built into the local demo.

**Options to evaluate, not installed in this app:**

| Option | Best use | Main trade-off |
|---|---|---|
| **Local Ollama + a suitable open model** | Free-to-call, on-device experiment; no per-request API bill | Needs a capable machine; benchmark CPU speed and Arabic/English quality before claiming it is practical. |
| **Gemini API free tier, if the chosen model/account offers it** | Small prototype with usage limits | External processing and tier/data-use terms must be approved before sending company or HR content. |
| **Paid Gemini 3.5 Flash API** | Compare language quality and latency at modest scale | Usage cost and external data-governance review; an experiment, **not** the Azure-only production design. |
| **Regional Azure-hosted model** | Proposed enterprise production path alongside Entra ID and Azure AI Search | Paid service; confirm region, model availability, privacy, latency, and cost. |

**“Training” plan:** First, do **not** train on the confidential corpus or expect a model to memorize company policy. Give it a narrow role and output format; build reviewed examples and tests for typos, Arabic/English, paraphrases, access boundaries, retired policy, missing SLA, malicious document instructions, and citation support. Compare each option on answer quality, safety, speed, and cost. Only consider actual fine-tuning later if those tests show a persistent gap, training data is approved and access-scoped, and the organization accepts the added maintenance/privacy cost. Changing policies should update approved evidence, **not** require retraining model weights.

**Closing line:** “The model can make the assistant easier to talk to; the application still decides what it is allowed to know and what it can prove.”

## Backup copy-paste bank (rehearsal or reviewer questions)

The live sequence above includes three supported answers and two correct safe non-answers. These remaining five give the full **seven supported + three protective** case set. Expected outcomes were checked in the local answer path on 2026-09-25; re-run the evaluation before recording.

**Supported — Leila Mansour (Procurement):**

```text
How do we onboard a supplier that will access company systems?
```

Expected: **Answered**, current policy and matrix; a paraphrase of the vendor need.

**Supported — Leila Mansour (Procurement):**

```text
Does a low-risk renewal below USD 100,000 using the unchanged approved standard agreement need a separate lawyer signature?
```

Expected: **Answered**, current policy plus a narrow Legal advisory; Legal review is not removed generally.

**Supported — Maya Chen (Engineering):**

```text
How do I request annual leave and when should I submit it?
```

Expected: **Answered** from the general leave policy, with no investigation case detail.

**Supported — Omar Haddad (Human Resources):**

```text
How do employees request annual leave?
```

Expected: **Answered** from the same general policy; broader HR access does not make a private case relevant.

**Protective — Maya Chen (Engineering):**

```text
What is our remote-work policy?
```

Expected: **Insufficient evidence**; no invented remote-work policy.

## Final checks before filming

- Confirm the selected employee before every question and that a citation opens for that employee.
- Run `.\.venv\Scripts\python.exe -m apex_assistant evaluate --stage full`; explain that `passed: true` does not automatically mean `submission_ready: true`.
- Keep the recording within the requested 5–7 minutes. Add the private/unlisted video link to `README.md` after confirming reviewer access.
- Be ready to explain the limitations: demo identity is simulated, approved evidence needs review after source changes, and the current language understanding is narrower than a verified AI-assisted design.

## Model-option references (checked 2026-09-25)

- [Ollama Windows download](https://ollama.com/download/windows) and [Ollama model library example](https://ollama.com/library/qwen3)
- [Gemini 3.5 Flash model](https://ai.google.dev/gemini-api/docs/models/gemini-3.5-flash), [Gemini API billing and free tier](https://ai.google.dev/gemini-api/docs/billing)
- [Microsoft Foundry deployment types and regional processing](https://learn.microsoft.com/en-us/azure/foundry/concepts/architecture)
