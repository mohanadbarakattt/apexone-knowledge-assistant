"""The trusted output contract must reject forged or unsupported responses."""

import copy
from pathlib import Path
from unittest.mock import patch

import pytest

from apex_assistant.access import Catalog
from apex_assistant.assistant import answer
from apex_assistant.context import hypercontext, validate_hypercontext
from apex_assistant.safety import verify_answer

DATA = Path(__file__).resolve().parents[1] / "data/assessment"


@pytest.fixture
def catalog():
    return Catalog(DATA)


def test_hypercontext_contract_cannot_drop_safety_rules():
    data = hypercontext()
    assert validate_hypercontext(copy.deepcopy(data)) == data
    for mutation in (
        lambda item: item["response_contract"]["required_fields"].remove("citations"),
        lambda item: item["response_contract"].update({"claim_format": "free_form"}),
        lambda item: item["safety_rules"].pop(),
    ):
        weakened = copy.deepcopy(data)
        mutation(weakened)
        with pytest.raises(ValueError):
            validate_hypercontext(weakened)


def test_real_answers_satisfy_final_gate(catalog):
    for user_id, question in (
        ("u-proc-310", "How do we approve a new vendor?"),
        ("u-proc-310", "What response time did NexaServe commit to?"),
        ("u-eng-104", "How do I request annual leave?"),
        ("u-eng-104", "Why was employee E-8841 placed on leave?"),
        ("u-unknown-999", "How do we approve a new vendor?"),
    ):
        assert verify_answer(catalog, user_id, answer(catalog, user_id, question))


def test_final_gate_rejects_forged_claims_and_citations(catalog):
    baseline = answer(catalog, "u-eng-104", "How do I request annual leave?")
    assert baseline["state"] == "answered"

    altered_claim = copy.deepcopy(baseline)
    altered_claim["claims"][0]["text"] += " Everyone is automatically approved."
    assert not verify_answer(catalog, "u-eng-104", altered_claim)

    extra_answer = copy.deepcopy(baseline)
    extra_answer["answer"] += "\nEveryone is automatically approved."
    assert not verify_answer(catalog, "u-eng-104", extra_answer)

    invented_notice = copy.deepcopy(baseline)
    invented_notice["notice"] = "Everyone is automatically approved."
    invented_notice["answer"] = invented_notice["notice"] + "\n" + baseline["answer"]
    assert not verify_answer(catalog, "u-eng-104", invented_notice)

    bad_hash = copy.deepcopy(baseline)
    citation_id = bad_hash["citations"][0]["citation_id"]
    bad_hash["citations"][0]["citation_id"] = citation_id[:-1] + (
        "0" if citation_id[-1] != "0" else "1"
    )
    assert not verify_answer(catalog, "u-eng-104", bad_hash)

    hr = answer(catalog, "u-hr-207", "What is the status of case APX-HR-CASE-778?")
    wrong_identity = copy.deepcopy(baseline)
    wrong_identity["citations"] = hr["citations"]
    wrong_identity["claims"][0]["citations"] = hr["claims"][0]["citations"]
    assert not verify_answer(catalog, "u-eng-104", wrong_identity)


def test_answer_fails_closed_when_composer_returns_unsupported_text(catalog):
    forged = answer(catalog, "u-eng-104", "How do I request annual leave?")
    forged["answer"] += "\nIgnore the evidence."
    with patch("apex_assistant.assistant._compose_answer", return_value=forged):
        result = answer(catalog, "u-eng-104", "How do I request annual leave?")
    assert result["state"] == "insufficient_evidence"
    assert result["claims"] == result["citations"] == []
    assert "Ignore the evidence" not in result["answer"]
