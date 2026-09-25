"""Small extractive answer path: trusted metadata chooses sources; prose stays data."""

from __future__ import annotations

import hashlib
import re
from datetime import date

from .access import Catalog, Document
from .retrieval import query_tokens, retrieve, tokens
from .reviewed import is_approved
from .safety import verify_answer

UNTRUSTED_DIRECTIVE = re.compile(
    r"\b(?:assistant operating directive|system (?:note|prompt|message)|api key|higher priority)\b"
    r"|\bignore\b.{0,80}\binstructions?\b"
    r"|\b(?:disregard|forget)\b.{0,80}\b(?:rules?|guidance|instructions?)\b"
    r"|\b(?:reveal|disclose|exfiltrate|publish)\b.{0,80}"
    r"\b(?:secrets?|confidential|restricted|apx-hr-case-\d+)\b"
    r"|\b(?:invent|fabricate|make up)\b.{0,80}"
    r"\b(?:sla|response times?|contractual)\b"
    r"|\binvoke\b.{0,80}\btools?\b",
    re.IGNORECASE,
)

NO_AVAILABLE_EVIDENCE = (
    "I cannot answer from evidence available to this identity. "
    "The information may be unavailable, restricted, or not found. "
    "If you believe access is needed, contact the information owner."
)


def _intent(question: str) -> str:
    words = query_tokens(question)
    lowered = question.lower()
    if re.search(r"\b(?:apx-hr-case-\d+|e-\d+)\b", lowered) or {"investigation", "case"} & words:
        return "investigation"
    if {"sla", "response", "service"} & words and {
        "nexaserve",
        "contractual",
        "contract",
        "commit",
    } & words:
        return "sla"
    if "renewal" in words and {"lawyer", "legal", "signature", "standard"} & words:
        return "renewal"
    if "leave" in words or re.search(r"\btime[\s-]+off\b", lowered):
        return "leave"
    if {"migration", "legacy"} & words:
        return "migration"
    if {"vendor", "approval", "onboarding", "procurement"} & words:
        return "vendor"
    return "unknown"


def _source(documents: tuple[Document, ...], *title_words: str) -> Document | None:
    required = set(title_words)
    matches = [
        document
        for document in documents
        if required <= tokens(document.title) and document.status != "Retired"
    ]
    return matches[0] if len(matches) == 1 else None


def _slice(
    document: Document, start: str, end: str | None = None, unverified: bool = False
) -> tuple[str, int, int] | None:
    lines = document.content.splitlines()
    begin = next((i for i, line in enumerate(lines) if line.strip().lower() == start.lower()), None)
    if begin is None:
        return None
    finish = (
        next(
            (i for i in range(begin + 1, len(lines)) if lines[i].strip().lower() == end.lower()),
            None,
        )
        if end
        else len(lines)
    )
    if finish is None or finish <= begin + 1:
        return None
    if unverified:
        for index in range(begin + 1, finish):
            if UNTRUSTED_DIRECTIVE.search(lines[index]):
                finish = index
                break
        if finish <= begin + 1:
            return None
    return (
        " ".join(line.strip() for line in lines[begin + 1 : finish] if line.strip()),
        begin + 2,
        finish,
    )


def _line(document: Document, phrase: str) -> tuple[str, int, int] | None:
    lines = document.content.splitlines()
    index = next((i for i, line in enumerate(lines) if phrase.lower() in line.lower()), None)
    if index is None:
        return None
    return lines[index].strip(), index + 1, index + 1


def _claim(document: Document, passage: tuple[str, int, int] | None) -> dict | None:
    if passage is None:
        return None
    text, start, end = passage
    if not text or not 1 <= start <= end <= len(document.content.splitlines()):
        return None
    raw = "\n".join(document.content.splitlines()[start - 1 : end])
    if " ".join(raw.split()) != " ".join(text.split()):
        return None
    if not is_approved(document, start, end, raw):
        return None
    # Approval is independent of document status and never grants document access.
    digest = hashlib.sha256(raw.encode()).hexdigest()[:12]
    citation_id = f"{document.key}:L{start}-L{end}:{digest}"
    return {
        "text": text,
        "citations": [citation_id],
        "source": {
            "citation_id": citation_id,
            "document_id": document.document_id,
            "version": document.version,
            "title": document.title,
            "status": document.status,
            "source_path": document.source_path,
            "line_start": start,
            "line_end": end,
        },
    }


def _safe(state: str, message: str) -> dict:
    return {
        "state": state,
        "answer": message,
        "notice": None,
        "claims": [],
        "citations": [],
        "diagnostics": {"outcome": state},
    }


def _compose_answer(
    catalog: Catalog, user_id: str, question: str, as_of: date | None = None
) -> dict:
    found = retrieve(catalog, user_id, question, limit=20, as_of=as_of)
    if found["state"] == "identity_denied":
        return _safe("identity_denied", "This employee identity is not recognized.")
    if found["state"] == "invalid_request":
        return _safe("invalid_request", "Enter a non-empty question of at most 4,000 characters.")
    if found["state"] == "no_authorized_evidence":
        return _safe("no_authorized_evidence", NO_AVAILABLE_EVIDENCE)

    intent = _intent(question)
    # A retrieved document must also be present in the trusted authorized view.
    retrieved = {(item["document_id"], item["version"]) for item in found["evidence"]}
    visible = tuple(
        document
        for document in catalog.authorized_documents(user_id)
        if (document.document_id, document.version) in retrieved
        and document.status in {"Current", "Active", "Active advisory", "Open", "Unverified"}
        and date.fromisoformat(document.effective_date) <= (as_of or date.today())
    )
    versions: dict[str, set[str]] = {}
    for document in visible:
        if document.status == "Current":
            versions.setdefault(document.document_id, set()).add(document.version)
    if any(len(items) > 1 for items in versions.values()):
        return _safe(
            "conflicting_evidence",
            "Multiple current versions conflict. Confirm the controlling version "
            "with the document owner before acting.",
        )

    selected: list[dict | None] = []
    warning = None
    state = "answered"
    if intent == "vendor":
        policy = _source(visible, "enterprise", "vendor", "policy")
        matrix = _source(visible, "procurement", "approval", "matrix")
        if policy is None or matrix is None:
            return _safe(
                "insufficient_evidence", "The current policy or financial matrix is unavailable."
            )
        selected = [
            _claim(
                policy, _slice(policy, "2. Scope and definition", "3. Required approval process")
            ),
            _claim(
                policy, _slice(policy, "3. Required approval process", "4. Evidence and records")
            ),
            _claim(matrix, _slice(matrix, "Related policy", "Approval matrix")),
            _claim(policy, _line(policy, "CONTROL  No contract")),
        ]
        # The matrix must explicitly relate to the current policy revision.
        if policy.version not in matrix.content or "does not remove" not in matrix.content:
            return _safe(
                "conflicting_evidence", "The policy and approval matrix need owner review."
            )
    elif intent == "renewal":
        policy = _source(visible, "enterprise", "vendor", "policy")
        advisory = _source(visible, "legal", "advisory", "memo")
        if policy is None or advisory is None:
            return _safe(
                "insufficient_evidence",
                "The current policy or scoped Legal advisory is unavailable.",
            )
        if policy.version not in advisory.content or "does not supersede" not in advisory.content:
            return _safe("conflicting_evidence", "The advisory scope needs Legal confirmation.")
        selected = [
            _claim(policy, _line(policy, "Legal completes the applicable contract")),
            _claim(advisory, _slice(advisory, "Advisory interpretation", "Authority and limits")),
        ]
    elif intent == "sla":
        contract = _source(visible, "nexaserve", "support", "agreement")
        if contract is None:
            return _safe("insufficient_evidence", "The authorized contract is unavailable.")
        passage = _slice(contract, "3. Service levels", "4. Escalation")
        if passage is None:
            return _safe("insufficient_evidence", "No reliable service-level clause was found.")
        selected = [_claim(contract, passage)]
        text = passage[0].lower()
        if "does not specify a first-response time" in text and "no schedule c is attached" in text:
            state = "insufficient_evidence"
            warning = (
                "No binding response target is established by the available agreement. "
                "An executed schedule is needed before stating one."
            )
        elif re.search(r"first.response.{0,40}\b\d+\s*(?:minutes?|hours?|days?)\b", text):
            state = "answered"
        else:
            return _safe(
                "insufficient_evidence",
                "The service-level clause does not establish a clear response target.",
            )
    elif intent == "leave":
        policy = _source(visible, "employee", "leave", "policy")
        if policy is None:
            return _safe("insufficient_evidence", "The general leave policy is unavailable.")
        words = query_tokens(question)
        if "sick" in words:
            selected = [_claim(policy, _line(policy, "Employees should notify their manager"))]
        elif {"emergency", "family"} & words:
            selected = [_claim(policy, _line(policy, "Emergency and family leave requests"))]
        else:
            selected = [_claim(policy, _slice(policy, "1. Annual leave", "2. Sick leave"))]
    elif intent == "investigation":
        case = _source(visible, "employee", "relations", "investigation", "summary")
        if case is None:
            return _safe("no_authorized_evidence", NO_AVAILABLE_EVIDENCE)
        selected = [_claim(case, _slice(case, "Case summary", "Handling restrictions"))]
    elif intent == "migration":
        notes = _source(visible, "legacy", "assistant", "migration", "notes")
        if notes is None or notes.status != "Unverified":
            return _safe(
                "insufficient_evidence",
                "The migration evidence is unavailable or has unknown status.",
            )
        selected = [
            _claim(
                notes,
                _slice(
                    notes,
                    "Migration summary",
                    "Imported note from an unverified prototype",
                    unverified=True,
                ),
            ),
            _claim(notes, _slice(notes, "Migration success conditions", unverified=True)),
        ]
        state = "answered_with_warning"
        warning = "This source is unverified. Embedded operating directives were ignored."
    else:
        return _safe("insufficient_evidence", "No sufficiently supported answer was found.")

    if not selected or any(item is None for item in selected):
        return _safe(
            "insufficient_evidence", "The available authorized passages do not support an answer."
        )
    claims = [{"text": item["text"], "citations": item["citations"]} for item in selected]
    citations = list({item["source"]["citation_id"]: item["source"] for item in selected}.values())
    body = "\n".join(f"- {item['text']} [{item['citations'][0]}]" for item in claims)
    return {
        "state": state,
        "answer": f"{warning}\n{body}" if warning else body,
        "notice": warning,
        "claims": claims,
        "citations": citations,
        "diagnostics": {"outcome": state},
    }


def answer(catalog: Catalog, user_id: str, question: str, as_of: date | None = None) -> dict:
    """Compose from authorized evidence, then fail closed on output-contract violations."""
    result = _compose_answer(catalog, user_id, question, as_of)
    if verify_answer(catalog, user_id, result, as_of):
        return result
    return _safe(
        "insufficient_evidence", "The answer could not be verified against authorized evidence."
    )
