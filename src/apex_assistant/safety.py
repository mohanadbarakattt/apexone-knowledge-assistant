"""Final structural gate for extractive answers; never grants document access."""

from __future__ import annotations

import hashlib
from datetime import date

from .access import Catalog, Document
from .context import ELIGIBLE_STATUSES, hypercontext
from .reviewed import is_approved

SOURCE_FIELDS = frozenset(
    {
        "citation_id",
        "document_id",
        "version",
        "title",
        "status",
        "source_path",
        "line_start",
        "line_end",
    }
)
ALLOWED_NOTICES = frozenset(
    {
        "No binding response target is established by the available agreement. "
        "An executed schedule is needed before stating one.",
        "This source is unverified. Embedded operating directives were ignored.",
    }
)


def _source_span(source: dict, documents: dict[tuple[str, str], Document]) -> str | None:
    """Return the exact normalized span only for a current authorized citation."""
    if not isinstance(source, dict) or set(source) != SOURCE_FIELDS:
        return None
    if not all(
        isinstance(source.get(key), str) for key in SOURCE_FIELDS - {"line_start", "line_end"}
    ):
        return None
    start, end = source["line_start"], source["line_end"]
    if type(start) is not int or type(end) is not int or start < 1 or end < start:
        return None
    document = documents.get((source["document_id"], source["version"]))
    if document is None:
        return None
    if any(
        source[field] != getattr(document, field)
        for field in ("document_id", "version", "title", "status", "source_path")
    ):
        return None
    lines = document.content.splitlines()
    if end > len(lines):
        return None
    raw = "\n".join(lines[start - 1 : end])
    if not is_approved(document, start, end, raw):
        return None
    digest = hashlib.sha256(raw.encode()).hexdigest()[:12]
    expected_id = f"{document.key}:L{start}-L{end}:{digest}"
    return raw if source["citation_id"] == expected_id else None


def verify_answer(catalog: Catalog, user_id: str, result: dict, as_of: date | None = None) -> bool:
    """Reject unsupported output; the composer remains responsible for meaning."""
    contract = hypercontext()["response_contract"]
    if not isinstance(result, dict) or set(result) != set(contract["required_fields"]):
        return False
    state = result["state"]
    if state not in contract["allowed_states"]:
        return False
    if not isinstance(result["answer"], str) or not result["answer"].strip():
        return False
    notice = result["notice"]
    if notice is not None and (not isinstance(notice, str) or notice not in ALLOWED_NOTICES):
        return False
    claims, citations = result["claims"], result["citations"]
    if not isinstance(claims, list) or not isinstance(citations, list):
        return False
    if result["diagnostics"] != {"outcome": state}:
        return False
    if state == "identity_denied" and catalog.known_user(user_id):
        return False
    if not catalog.known_user(user_id) and state != "identity_denied":
        return False
    if not claims:
        return (
            not citations and notice is None and state not in {"answered", "answered_with_warning"}
        )
    if state not in {"answered", "answered_with_warning", "insufficient_evidence"}:
        return False
    if state == "answered" and notice is not None:
        return False
    if state == "answered_with_warning" and notice is None:
        return False

    today = as_of or date.today()
    documents = {
        (document.document_id, document.version): document
        for document in catalog.authorized_documents(user_id)
        if document.status in ELIGIBLE_STATUSES
        and date.fromisoformat(document.effective_date) <= today
    }
    spans = {}
    for source in citations:
        raw = _source_span(source, documents)
        if raw is None or source["citation_id"] in spans:
            return False
        spans[source["citation_id"]] = " ".join(raw.split())
    used = set()
    for claim in claims:
        if not isinstance(claim, dict) or set(claim) != {"text", "citations"}:
            return False
        if not isinstance(claim["text"], str) or not claim["text"].strip():
            return False
        refs = claim["citations"]
        if not isinstance(refs, list) or len(refs) != 1 or not isinstance(refs[0], str):
            return False
        if " ".join(claim["text"].split()) != spans.get(refs[0]):
            return False
        used.add(refs[0])
    if used != set(spans):
        return False
    if state == "answered_with_warning" and not any(
        source["status"] == "Unverified" for source in citations
    ):
        return False
    body = "\n".join(f"- {claim['text']} [{claim['citations'][0]}]" for claim in claims)
    expected_answer = f"{notice}\n{body}" if notice else body
    return result["answer"] == expected_answer
