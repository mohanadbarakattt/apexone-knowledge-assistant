"""Trusted, versioned approval of exact evidence spans, never document ACLs."""

from __future__ import annotations

import hashlib
import json
import re
from functools import lru_cache
from importlib.resources import files

from .access import Document


@lru_cache(maxsize=1)
def approved_spans() -> frozenset[tuple[str, str, int, int, str]]:
    data = json.loads(files("apex_assistant").joinpath("approved_spans.json").read_text())
    if set(data) != {"schema_version", "spans"} or data["schema_version"] != "1.0":
        raise ValueError("Invalid reviewed evidence registry")
    if not isinstance(data["spans"], list):
        raise ValueError("Invalid reviewed evidence spans")
    entries = set()
    for item in data["spans"]:
        if not isinstance(item, dict) or set(item) != {
            "document_id",
            "version",
            "line_start",
            "line_end",
            "sha256",
        }:
            raise ValueError("Invalid reviewed evidence entry")
        start, end = item["line_start"], item["line_end"]
        if (
            not isinstance(item["document_id"], str)
            or not item["document_id"]
            or not isinstance(item["version"], str)
            or not item["version"]
            or type(start) is not int
            or type(end) is not int
            or start < 1
            or end < start
            or not isinstance(item["sha256"], str)
            or re.fullmatch(r"[0-9a-f]{64}", item["sha256"]) is None
        ):
            raise ValueError("Invalid reviewed evidence value")
        entry = (item["document_id"], item["version"], start, end, item["sha256"])
        if entry in entries:
            raise ValueError("Duplicate reviewed evidence entry")
        entries.add(entry)
    return frozenset(entries)


def is_approved(document: Document, start: int, end: int, raw: str) -> bool:
    digest = hashlib.sha256(raw.encode()).hexdigest()
    return (document.document_id, document.version, start, end, digest) in approved_spans()
