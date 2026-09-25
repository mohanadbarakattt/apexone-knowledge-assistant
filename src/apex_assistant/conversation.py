"""Trusted, finite conversational responses outside the evidence answer path."""

from __future__ import annotations

import re

GREETING_PREFIX = re.compile(
    r"^\s*(?:(?:hi|hello|hey)(?: there)?|good (?:morning|afternoon|evening))"
    r"(?=[\s,!.:;?-]|$)[\s,!.:;?-]*",
    re.IGNORECASE,
)
SMALL_TALK = {
    "greeting": (
        "Hi! Ask me about an available company policy or document, and I'll show the "
        "supporting source when I can."
    ),
    "help": (
        "I can help with questions about available company policies and documents. "
        "I cite supporting sources and will say when information is missing or "
        "unavailable to this employee."
    ),
    "thanks": "You're welcome. Ask another question whenever you're ready.",
}


def conversation(question: str) -> tuple[str, str | None]:
    """Separate a short greeting from a substantive question; never use document prose."""
    rest = GREETING_PREFIX.sub("", question, count=1).strip()
    normalized = re.sub(r"\s+", " ", rest.lower().strip(" \t\r\n.,!?;:"))
    if not normalized:
        return "", "greeting"
    if normalized in {"help", "what can you do", "how can you help", "how can you help me"}:
        return "", "help"
    if normalized in {"thanks", "thank you", "thank you very much"}:
        return "", "thanks"
    return rest, None
