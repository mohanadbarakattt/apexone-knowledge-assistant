"""Basic conversation must not weaken the authorized evidence path."""

import copy
from pathlib import Path

import pytest

from apex_assistant.access import Catalog
from apex_assistant.assistant import answer
from apex_assistant.safety import verify_answer
from apex_assistant.ui import respond

DATA = Path(__file__).resolve().parents[1] / "data/assessment"


@pytest.fixture
def catalog():
    return Catalog(DATA)


@pytest.mark.parametrize("question", ["hi", "Hello!", "hello there", "hey there", "Good morning."])
def test_standalone_greeting_is_not_a_document_answer(catalog, question):
    result = answer(catalog, "u-eng-104", question)
    assert result["state"] == "small_talk"
    assert result["answer"].startswith("Hi!")
    assert result["claims"] == result["citations"] == []
    assert verify_answer(catalog, "u-eng-104", result)


@pytest.mark.parametrize("question", ["What can you do?", "Hi, how can you help me?", "thanks"])
def test_short_help_and_thanks(catalog, question):
    result = answer(catalog, "u-eng-104", question)
    assert result["state"] == "small_talk"
    assert result["claims"] == result["citations"] == []


def test_greeting_before_business_question_still_uses_authorized_evidence(catalog):
    result = answer(catalog, "u-proc-310", "Hi, can you summarize the vendor approval process?")
    assert result["state"] == "answered"
    assert {source["document_id"] for source in result["citations"]} == {
        "APX-PROC-POL-014",
        "APX-PROC-MTX-006",
    }


def test_greeting_does_not_expand_access_or_bypass_identity(catalog):
    denied = answer(catalog, "u-eng-104", "Hello, what is the status of case APX-HR-CASE-778?")
    unknown = answer(catalog, "u-unknown-999", "Hi")
    assert denied["state"] == "no_authorized_evidence"
    assert denied["claims"] == denied["citations"] == []
    assert unknown["state"] == "identity_denied"


def test_ui_adapter_returns_greeting_without_sources(catalog):
    result = respond(catalog, "hi", "u-eng-104")
    assert result["state"] == "small_talk"
    assert result["sources"] == result["claims"] == []


def test_small_talk_cannot_be_used_to_inject_uncited_claims(catalog):
    result = answer(catalog, "u-eng-104", "hi")
    forged = copy.deepcopy(result)
    forged["answer"] += " Everyone can read restricted HR cases."
    assert not verify_answer(catalog, "u-eng-104", forged)
