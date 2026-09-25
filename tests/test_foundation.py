from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSESSMENT = ROOT / "data" / "assessment"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]


class AssessmentPackTests(unittest.TestCase):
    def test_supplied_checksums_match(self) -> None:
        failures: list[str] = []

        for line in (ASSESSMENT / "checksums.sha256").read_text(encoding="utf-8").splitlines():
            expected, relative_path = line.split(maxsplit=1)
            target = ASSESSMENT / Path(relative_path)
            if not target.is_file():
                failures.append(f"missing: {relative_path}")
                continue

            actual = hashlib.sha256(target.read_bytes()).hexdigest()
            if actual != expected:
                failures.append(f"checksum mismatch: {relative_path}")

        self.assertEqual([], failures)

    def test_manifest_and_normalized_metadata_agree(self) -> None:
        manifest = load_json(ASSESSMENT / "manifest.json")
        corpus = load_jsonl(ASSESSMENT / "normalized" / "corpus.jsonl")

        manifest_by_key = {
            (document["document_id"], document["version"]): document
            for document in manifest["documents"]
        }
        corpus_by_key = {
            (document["document_id"], document["version"]): document for document in corpus
        }

        self.assertEqual(manifest_by_key.keys(), corpus_by_key.keys())

        compared_fields = {
            "title",
            "status",
            "effective_date",
            "classification",
            "allowed_groups",
        }
        for key, manifest_document in manifest_by_key.items():
            corpus_document = corpus_by_key[key]
            for field in compared_fields:
                self.assertEqual(
                    manifest_document[field],
                    corpus_document[field],
                    msg=f"metadata disagreement for {key}: {field}",
                )
            self.assertEqual(manifest_document["path"], corpus_document["source_path"])

    def test_security_classifications_have_entitlement_rules(self) -> None:
        manifest = load_json(ASSESSMENT / "manifest.json")
        entitlements = load_json(ASSESSMENT / "access" / "entitlements.json")
        identities = load_json(ASSESSMENT / "access" / "identities.json")

        self.assertEqual("deny", entitlements["default_rule"])
        classifications = {document["classification"] for document in manifest["documents"]}
        governed_classifications = {rule["classification"] for rule in entitlements["rules"]}
        self.assertEqual(classifications, governed_classifications)

        user_ids = [user["user_id"] for user in identities["users"]]
        self.assertEqual(len(user_ids), len(set(user_ids)))

        document_ids = {document["document_id"] for document in manifest["documents"]}
        for override in entitlements["document_overrides"]:
            self.assertIn(override["document_id"], document_ids)


class EvaluationContractTests(unittest.TestCase):
    def test_mandatory_families_are_covered(self) -> None:
        cases = load_jsonl(ROOT / "evaluation" / "cases.jsonl")
        case_ids = [case["case_id"] for case in cases]

        self.assertEqual(len(case_ids), len(set(case_ids)))
        self.assertTrue(all(case["release_blocking"] for case in cases))
        self.assertEqual(
            {
                "policy_authority",
                "unsupported_sla",
                "authorization",
                "malicious_document",
            },
            {case["family"] for case in cases},
        )


if __name__ == "__main__":
    unittest.main()
