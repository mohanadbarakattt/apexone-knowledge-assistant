# ADR 010 — Short conversational replies outside document retrieval

## Requirement and risk

A plain greeting previously produced a no-evidence error. That makes the app
feel broken. Treating arbitrary document prose as a chat response would create
an unsupported-claim and prompt-injection risk.

## Decision

After the employee identity and input-length checks, recognize a finite set of
standalone greetings, help questions, and thanks. These receive a `small_talk`
state, no claims, and no citations. The final verifier allows only the exact
trusted application replies for that state. A greeting attached to a substantive
question is removed before normal authorized retrieval; it never changes
permissions or the evidence requirements. The UI labels this as an assistant
message rather than a supported document answer.

## Alternative and limitation

An open-ended chat model could handle more social language but would add an
unnecessary model dependency and a new trust boundary. This bounded handler
does not recognize every conversational phrase or create free-form summaries.

## Acceptance

Standalone greetings/help/thanks reply without sources. Mixed greeting and
business questions use the normal cited path. An unknown identity remains
denied, a restricted case stays unavailable, and a forged small-talk claim is
rejected by the final verifier. Full tests and evaluation remain release gates.
