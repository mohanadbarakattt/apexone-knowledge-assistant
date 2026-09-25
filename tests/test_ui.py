"""The optional local UI must preserve the core's access boundary."""

import json
import subprocess
import sys
import threading
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pytest

from apex_assistant.access import Catalog
from apex_assistant.ui import DATA, demo_identities, make_server, respond, source_view


@pytest.fixture
def server():
    instance = make_server(port=0)
    thread = threading.Thread(target=instance.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{instance.server_port}"
    finally:
        instance.shutdown()
        instance.server_close()
        thread.join(timeout=2)


def post(base, user_id, question, origin=None):
    headers = {"Content-Type": "application/json"}
    if origin is not None:
        headers["Origin"] = origin
    request = Request(
        f"{base}/api/ask",
        data=json.dumps({"user_id": user_id, "question": question}).encode(),
        headers=headers,
    )
    with urlopen(request, timeout=5) as response:
        return json.load(response)


def test_ui_identity_choices_come_from_trusted_fixture():
    catalog = Catalog(DATA)
    choices = demo_identities(catalog, DATA)
    assert {value for _, value in choices} == {"u-eng-104", "u-hr-207", "u-proc-310"}


def test_ui_adapter_keeps_permission_boundary():
    catalog = Catalog(DATA)
    question = "For case APX-HR-CASE-778, why is the employee on administrative leave?"
    allowed = respond(catalog, question, "u-hr-207")
    denied = respond(catalog, question, "u-eng-104")
    assert "APX-HR-CASE-778" in allowed["answer"]
    assert allowed["claims"]
    assert allowed["sources"][0]["document_id"] == "APX-HR-CASE-778"
    assert allowed["claims"][0]["citations"] == [allowed["sources"][0]["citation_id"]]
    assert denied["state"] == "no_authorized_evidence"
    assert denied["claims"] == []
    assert denied["sources"] == []
    assert "APX-HR-CASE-778" not in json.dumps(denied)


def test_ui_http_denial_and_missing_sla(server):
    question = "For case APX-HR-CASE-778, why is the employee on administrative leave?"
    denied = post(server, "u-eng-104", question)
    assert denied["state"] == "no_authorized_evidence"
    assert "APX-HR-CASE-778" not in json.dumps(denied)
    missing = post(server, "u-proc-310", "What response time did NexaServe commit to?")
    assert missing["state"] == "insufficient_evidence"
    assert "executed Schedule C" in missing["answer"]
    assert missing["notice"]
    assert missing["sources"][0]["document_id"] == "APX-LEG-CON-NS-2026"


def test_failure_messages_are_actionable_without_source_enumeration(server):
    restricted = post(server, "u-eng-104", "What is the status of case APX-HR-CASE-778?")
    nonexistent = post(server, "u-eng-104", "What is the status of case APX-HR-CASE-999?")
    assert restricted == nonexistent
    assert restricted["state"] == "no_authorized_evidence"
    assert "may be unavailable, restricted, or not found" in restricted["answer"]
    assert restricted["claims"] == restricted["sources"] == []
    assert "APX-HR-CASE-778" not in json.dumps(restricted)

    unknown = post(server, "u-not-a-user", "How do I request annual leave?")
    invalid = post(server, "u-eng-104", " ")
    assert unknown["state"] == "identity_denied"
    assert "identity is not recognized" in unknown["answer"]
    assert invalid["state"] == "invalid_request"
    assert "non-empty question" in invalid["answer"]
    assert unknown["claims"] == unknown["sources"] == []
    assert invalid["claims"] == invalid["sources"] == []


def test_ui_page_uses_local_template_and_plain_text(server):
    with urlopen(server, timeout=5) as response:
        page = response.read().decode()
        assert response.headers["Content-Security-Policy"].startswith("default-src 'self'")
    assert "Start Bootstrap Simple Sidebar" in page
    assert "not authentication" in page
    assert "u-hr-207" in page
    assert "APX-HR-CASE-778" not in page
    assert 'id="topic-tree"' in page
    assert "cdn.jsdelivr" not in page
    with urlopen(f"{server}/app.js", timeout=5) as response:
        script = response.read().decode()
    assert "content.textContent = text" in script
    assert "renderAnswer(output, result, selectedUser, requestGeneration)" in script
    assert "sourceButton(source," in script
    assert "Question ·" in script
    assert 'heading.textContent = "Sources"' in script
    assert 'no_authorized_evidence: "No accessible information for this employee"' in script
    assert "It may be restricted, changed, or an invalid link." in script
    assert 'identity.addEventListener("change", clearMessages)' in script


def test_citation_opens_only_authorized_exact_source(server):
    question = "For case APX-HR-CASE-778, why was the employee placed on administrative leave?"
    allowed = post(server, "u-hr-207", question)
    assert allowed["state"] == "answered"
    citation_id = allowed["sources"][0]["citation_id"]
    query = urlencode({"user_id": "u-hr-207", "citation_id": citation_id})
    with urlopen(f"{server}/api/source?{query}", timeout=5) as response:
        source = json.load(response)
        assert response.headers["Cache-Control"] == "no-store"
    assert source["document_id"] == "APX-HR-CASE-778"
    assert source["line_start"] < source["line_end"]
    cited = " ".join(
        line["text"]
        for line in source["lines"]
        if source["line_start"] <= line["number"] <= source["line_end"]
    )
    assert "administrative leave" in cited
    assert source_view(Catalog(DATA), "u-hr-207", citation_id) == source

    error_bodies = []
    for user_id, attempted_id in [
        ("u-eng-104", citation_id),
        ("u-unknown-999", citation_id),
        ("u-hr-207", citation_id[:-1] + ("0" if citation_id[-1] != "0" else "1")),
        ("u-hr-207", "../manifest.json"),
    ]:
        query = urlencode({"user_id": user_id, "citation_id": attempted_id})
        with pytest.raises(HTTPError) as error:
            urlopen(f"{server}/api/source?{query}", timeout=5)
        assert error.value.code == 404
        body = error.value.read().decode()
        assert "APX-HR-CASE-778" not in body
        error_bodies.append(body)
    assert len(set(error_bodies)) == 1


def test_ui_topic_tree_hides_restricted_sources_for_engineering(server):
    with urlopen(f"{server}/api/context?user_id=u-eng-104", timeout=5) as response:
        engineering = json.load(response)
    with urlopen(f"{server}/api/context?user_id=u-hr-207", timeout=5) as response:
        hr = json.load(response)
    assert "APX-HR-CASE-778" not in json.dumps(engineering)
    assert "Investigations" not in json.dumps(engineering)
    assert "APX-HR-CASE-778" in json.dumps(hr)


def test_ui_help_documents_data_dir():
    process = subprocess.run(
        [sys.executable, "-m", "apex_assistant.ui", "--help"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert "--data-dir" in process.stdout


def test_ui_rejects_cross_origin_posts(server):
    with pytest.raises(HTTPError) as error:
        post(server, "u-hr-207", "leave", origin="https://outside.example")
    assert error.value.code == 403
