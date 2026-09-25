"""Topic navigation must stay subordinate to document authorization."""

import copy
import json
from datetime import date
from pathlib import Path
from unittest.mock import patch

from apex_assistant.access import Catalog
from apex_assistant.context import hypercontext, topic_document_ids, visible_topic_tree

DATA = Path(__file__).resolve().parents[1] / "data/assessment"
TODAY = date(2026, 9, 24)


def test_hypercontext_maps_existing_documents_without_answer_text():
    mapped = {
        document_id
        for area in hypercontext()["areas"]
        for topic in area["topics"]
        for document_id in topic["document_ids"]
    }
    manifest = json.loads((DATA / "manifest.json").read_text("utf-8"))
    known = {document["document_id"] for document in manifest["documents"]}
    assert mapped <= known
    assert "content" not in json.dumps(hypercontext())
    assert "allowed_groups" not in json.dumps(hypercontext())


def test_topic_tree_is_projected_through_employee_entitlements():
    catalog = Catalog(DATA)
    engineering = visible_topic_tree(catalog, "u-eng-104", TODAY)
    hr = visible_topic_tree(catalog, "u-hr-207", TODAY)
    assert "APX-HR-CASE-778" not in json.dumps(engineering)
    assert "Investigations" not in json.dumps(engineering)
    assert "APX-HR-POL-003" in json.dumps(engineering)
    assert "APX-HR-CASE-778" in json.dumps(hr)
    assert visible_topic_tree(catalog, "unknown", TODAY) == {"areas": []}


def test_topic_hints_cannot_mint_document_access():
    catalog = Catalog(DATA)
    engineering = catalog.authorized_documents("u-eng-104")
    altered = copy.deepcopy(hypercontext())
    altered["areas"][0]["topics"][0]["document_ids"].append("APX-HR-CASE-778")
    with patch("apex_assistant.context.hypercontext", return_value=altered):
        tree = visible_topic_tree(catalog, "u-eng-104", TODAY)
        hints = topic_document_ids("vendor approval", engineering, TODAY)
    assert "APX-HR-CASE-778" not in json.dumps(tree)
    assert "APX-HR-CASE-778" not in hints
    assert {"APX-PROC-POL-014", "APX-PROC-MTX-006"} <= hints


def test_topic_hint_does_not_filter_unknown_questions():
    catalog = Catalog(DATA)
    documents = catalog.authorized_documents("u-proc-310")
    assert topic_document_ids("unrelated wording", documents, TODAY) == frozenset()
