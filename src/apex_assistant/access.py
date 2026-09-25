"""Trusted configuration and authorization. Document prose never grants access."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path


class ConfigurationError(ValueError):
    """Intentionally generic: configuration failures must not disclose records."""


@dataclass(frozen=True)
class Document:
    document_id: str
    version: str
    title: str
    status: str
    effective_date: str
    classification: str
    allowed_groups: frozenset[str]
    source_path: str
    content: str

    @property
    def key(self) -> str:
        return f"{self.document_id}@{self.version}"


def strings(value: object) -> frozenset[str]:
    if not isinstance(value, list) or not value:
        raise ValueError("Expected nonempty string list")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError("Expected strings")
    if len(set(value)) != len(value):
        raise ValueError("Duplicate value")
    return frozenset(value)


def required(record: dict, field: str) -> str:
    value = record[field]
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Expected string")
    return value


def unique(records: list[dict], field: str) -> dict[str, dict]:
    result = {}
    for record in records:
        key = required(record, field)
        if key in result:
            raise ValueError("Duplicate identifier")
        result[key] = record
    return result


class Catalog:
    """Load trusted local configuration once; provide per-user document views.

    The CLI identity selector simulates authentication for the supplied fixtures.
    It is not a production authentication mechanism.
    """

    def __init__(self, root: Path):
        try:
            identities = self._read(root / "access/identities.json")
            entitlements = self._read(root / "access/entitlements.json")
            manifest = self._read(root / "manifest.json")
            if entitlements["default_rule"] != "deny":
                raise ValueError("Unsafe default")
            self._users = {
                key: strings(record["groups"])
                for key, record in unique(identities["users"], "user_id").items()
            }
            self._rules = {
                key: strings(record["allow_groups"])
                for key, record in unique(entitlements["rules"], "classification").items()
            }
            self._overrides = {}
            for key, record in unique(entitlements["document_overrides"], "document_id").items():
                deny = record["deny_groups"]
                self._overrides[key] = (
                    strings(record["allow_groups"]),
                    strings(deny) if deny != [] else frozenset(),
                )
            self._manifest = {}
            for record in manifest["documents"]:
                key = (required(record, "document_id"), required(record, "version"))
                if key in self._manifest:
                    raise ValueError("Duplicate manifest entry")
                self._manifest[key] = record
            if not self._overrides.keys() <= {key[0] for key in self._manifest}:
                raise ValueError("Override references an unknown document")
            # Content is loaded but not chunked, indexed, scored, or logged here.
            self._records = [
                json.loads(line)
                for line in (root / "normalized/corpus.jsonl").read_text("utf-8").splitlines()
                if line.strip()
            ]
            self._counts: dict[tuple[str, str], int] = {}
            for record in self._records:
                key = (required(record, "document_id"), required(record, "version"))
                self._counts[key] = self._counts.get(key, 0) + 1
        except (OSError, ValueError, KeyError, TypeError, AttributeError):
            raise ConfigurationError(
                "Assessment configuration is unavailable or invalid."
            ) from None

    @staticmethod
    def _read(path: Path) -> dict:
        value = json.loads(path.read_text("utf-8"))
        if value["schema_version"] != "1.0":
            raise ValueError("Unsupported schema")
        return value

    def known_user(self, user_id: str) -> bool:
        return user_id in self._users

    def authorized_documents(self, user_id: str) -> tuple[Document, ...]:
        groups = self._users.get(user_id)
        if groups is None:
            return ()
        allowed = []
        for record in self._records:
            try:
                document = self._authorize(record, groups)
                if document is not None:
                    allowed.append(document)
            except (ValueError, KeyError, TypeError, AttributeError):
                # A bad document is unavailable, without disclosing its existence.
                continue
        return tuple(allowed)

    def _authorize(self, record: dict, groups: frozenset[str]) -> Document | None:
        key = (record["document_id"], record["version"])
        metadata = self._manifest[key]
        classification = required(metadata, "classification")
        rule = self._rules.get(classification, frozenset())
        if not groups & rule:
            return None
        if not groups & strings(metadata["allowed_groups"]):
            return None
        override = self._overrides.get(key[0])
        if override is not None:
            allow, deny = override
            if groups & deny or not groups & allow:
                return None
        if record["schema_version"] != "1.0" or self._counts[key] != 1:
            return None
        for field in ("title", "status", "effective_date", "classification", "allowed_groups"):
            if record[field] != metadata[field]:
                return None
        if record["source_path"] != metadata["path"]:
            return None
        date.fromisoformat(required(record, "effective_date"))
        path = Path(required(record, "source_path"))
        if path.is_absolute() or ".." in path.parts:
            return None
        return Document(
            document_id=required(record, "document_id"),
            version=required(record, "version"),
            title=required(record, "title"),
            status=required(record, "status"),
            effective_date=required(record, "effective_date"),
            classification=classification,
            allowed_groups=strings(record["allowed_groups"]),
            source_path=str(path).replace("\\", "/"),
            content=required(record, "content"),
        )
