"""Unseen phrasings must improve recall without changing source authority."""

from pathlib import Path

import pytest

from apex_assistant.access import Catalog
from apex_assistant.assistant import answer

DATA = Path(__file__).resolve().parents[1] / "data/assessment"


@pytest.fixture
def catalog():
    return Catalog(DATA)


@pytest.mark.parametrize(
    "question",
    [
        "How do I get a new supplier aproved?",
        "What is the approvl chain for an enterprise vendor?",
        "What happens if a vendor starts work without approval?",
    ],
)
def test_new_procurement_wording_uses_current_policy_and_matrix(catalog, question):
    result = answer(catalog, "u-proc-310", question)
    assert result["state"] == "answered"
    assert {source["document_id"] for source in result["citations"]} == {
        "APX-PROC-POL-014",
        "APX-PROC-MTX-006",
    }


@pytest.mark.parametrize(
    ("question", "expected"),
    [
        ("Where should I submit a vaccation request?", "HR portal"),
        ("What is the sick leave process?", "notify their manager"),
        ("How do I request emergency leave?", "People Operations"),
    ],
)
def test_leave_subtopics_match_their_own_reviewed_evidence(catalog, question, expected):
    result = answer(catalog, "u-eng-104", question)
    assert result["state"] == "answered"
    assert expected in result["answer"]
    assert {source["document_id"] for source in result["citations"]} == {"APX-HR-POL-003"}
    if "sick" in question:
        assert "five business days" not in result["answer"]


def test_misspelled_contract_question_does_not_invent_sla(catalog):
    result = answer(
        catalog, "u-proc-310", "Does NexaServe promise a first responce within 4 hours?"
    )
    assert result["state"] == "insufficient_evidence"
    assert "4 hours" not in result["answer"]
    assert {source["document_id"] for source in result["citations"]} == {"APX-LEG-CON-NS-2026"}


def test_typo_matching_never_expands_restricted_case_access(catalog):
    result = answer(catalog, "u-eng-104", "What is the status of investgation E-8841?")
    assert result["state"] == "no_authorized_evidence"
    assert result["claims"] == result["citations"] == []
    assert "E-8841" not in result["answer"]


def test_unrelated_question_abstains(catalog):
    result = answer(catalog, "u-eng-104", "How do we work remotely?")
    assert result["state"] in {"no_authorized_evidence", "insufficient_evidence"}
    assert result["claims"] == result["citations"] == []
