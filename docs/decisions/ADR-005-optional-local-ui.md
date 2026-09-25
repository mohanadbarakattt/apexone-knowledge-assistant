# ADR 005 — Optional Local Browser UI

## Requirement and risk

The candidate requested a simple visual interface to understand and demonstrate
the assistant, using an existing free online template. The assessment itself does
not require a UI. A UI must not create a second authorization path, persist restricted
chat, render malicious document markup, or make the fake identity selector look like
real authentication.

## Decision

Adapt [Start Bootstrap Simple Sidebar](https://startbootstrap.com/template/simple-sidebar)
(MIT) for the page shell. Bundle its CSS and sidebar script locally, with attribution
and license under `src/apex_assistant/web/`. A small Python standard-library server
binds only to loopback and calls the same `answer()` function used by the CLI. It
accepts only JSON questions and supplied demo identities; the core still decides
authorization. The browser uses `textContent`, not HTML/Markdown rendering, for
answers. Identity changes clear visible messages, and no chat history is sent back
as evidence. The UI is explicitly optional and not a deployable enterprise login.
The answer adapter exposes only the core's authorized claims and a minimal citation
allowlist, then the browser presents source details separately from claim text.
Citation buttons open a local source viewer containing the authorized normalized
document with the exact cited lines highlighted. Each viewer request checks the
selected identity's current document view, eligible status/date, line range, and
citation hash again. An identity change closes the viewer. This is not a direct
PDF/DOCX page link: the assessment citations are normalized-text line numbers.

## Alternative and tradeoff

Gradio's ready-made `ChatInterface` was investigated and installed. Its required
native dependency was blocked by Windows Application Control on this machine, so it
would not provide a reliable demo here. The Bootstrap template plus standard-library
server needs a small amount of event-handling code, but keeps the assessed runtime
dependency-free and the page usable without a CDN. The UI still permits intentional
identity switching because the supplied identities simulate authentication.

## Verification and limitation

Tests cover the HTTP path, denied versus authorized answers, missing SLA, loopback
binding, local assets, plain-text rendering, and cross-origin rejection. The full
CLI and case suite remain the release authority. This interface is for a single
candidate on one computer; it is not suitable for network deployment or real users.
The citation viewer tests cover authorized resolution and generic refusal for
unauthorized, unknown, malformed, and hash-tampered references.
The documented `--data-dir` flag is passed only at local server startup. A fresh
editable install and built wheel were verified on September 23, 2026.
An unseen modification exercise: add a new supplied identity to a disposable pack,
then confirm the dropdown changes without granting access beyond the pack's rules.
