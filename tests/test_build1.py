import json
import shutil
import subprocess
import sys
from dataclasses import replace
from datetime import date
from pathlib import Path
from unittest.mock import patch

import pytest

from apex_assistant.access import Catalog, ConfigurationError
from apex_assistant.retrieval import chunks, rank, retrieve

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/assessment"
TODAY = date(2026, 9, 22)
RESTRICTED = "APX-HR-CASE-778"


@pytest.fixture
def catalog():
    return Catalog(DATA)


@pytest.fixture
def pack(tmp_path):
    for relative in ("access", "normalized"):
        shutil.copytree(DATA / relative, tmp_path / relative)
    shutil.copy(DATA / "manifest.json", tmp_path / "manifest.json")
    return tmp_path


def edit_json(path, change):
    value = json.loads(path.read_text("utf-8"))
    change(value)
    path.write_text(json.dumps(value), encoding="utf-8")


def test_known_access(catalog):
    for user in ("u-eng-104", "u-proc-310"):
        assert RESTRICTED not in {d.document_id for d in catalog.authorized_documents(user)}
    assert RESTRICTED in {d.document_id for d in catalog.authorized_documents("u-hr-207")}
    assert catalog.authorized_documents("unknown") == ()


def test_unknown_user_never_calls_authorization_or_ranking(catalog):
    with (
        patch.object(catalog, "authorized_documents", side_effect=AssertionError),
        patch("apex_assistant.retrieval.rank", side_effect=AssertionError),
    ):
        assert retrieve(catalog, "unknown", "vendor") == {
            "state": "identity_denied",
            "evidence": [],
        }


def test_deny_override_wins_over_membership(pack):
    edit_json(
        pack / "access/identities.json",
        lambda value: value["users"][0]["groups"].append("hr_investigations"),
    )
    assert RESTRICTED not in {
        d.document_id for d in Catalog(pack).authorized_documents("u-eng-104")
    }


@pytest.mark.parametrize(
    "field,value",
    [
        ("classification", "UNKNOWN"),
        ("allowed_groups", []),
        ("allowed_groups", "all_employees"),
        ("status", "Retired"),
        ("effective_date", "not-a-date"),
        ("path", "different.pdf"),
    ],
)
def test_inconsistent_metadata_denies_document(pack, field, value):
    edit_json(pack / "manifest.json", lambda data: data["documents"][0].update({field: value}))
    assert "APX-PROC-POL-014@3.0" not in {
        d.key for d in Catalog(pack).authorized_documents("u-proc-310")
    }


def test_missing_rule_denies_classification(pack):
    edit_json(pack / "access/entitlements.json", lambda data: data.update(rules=[]))
    assert Catalog(pack).authorized_documents("u-hr-207") == ()


def test_unknown_override_target_fails_closed(pack):
    edit_json(
        pack / "access/entitlements.json",
        lambda data: data["document_overrides"][0].update(document_id="TYPO"),
    )
    with pytest.raises(ConfigurationError):
        Catalog(pack)


def test_malformed_security_file_cli_is_generic(pack):
    (pack / "access/identities.json").write_text("SECRET malformed JSON", encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "apex_assistant",
            "retrieve",
            "--user",
            "u-eng-104",
            "--question",
            "vendor",
            "--data-dir",
            str(pack),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 2
    assert json.loads(result.stdout) == {"state": "configuration_error", "evidence": []}
    assert "SECRET" not in result.stdout + result.stderr


def test_duplicate_identity_configuration_error(pack):
    edit_json(pack / "access/identities.json", lambda data: data["users"].append(data["users"][0]))
    with pytest.raises(ConfigurationError, match="configuration is unavailable or invalid"):
        Catalog(pack)


def test_duplicate_corpus_document_denied(pack):
    path = pack / "normalized/corpus.jsonl"
    text = path.read_text("utf-8")
    path.write_text(text + "\n" + text.splitlines()[0], encoding="utf-8")
    assert "APX-PROC-POL-014@3.0" not in {
        d.key for d in Catalog(pack).authorized_documents("u-proc-310")
    }


def test_only_authorized_documents_reach_rank(catalog):
    with patch("apex_assistant.retrieval.rank", return_value=[]) as scoring:
        retrieve(catalog, "u-eng-104", "administrative leave")
    assert RESTRICTED not in {d.document_id for d in scoring.call_args.args[0]}


def test_restricted_content_cannot_change_engineering_results(pack, catalog, capsys):
    question = "annual leave request"
    expected = retrieve(catalog, "u-eng-104", question, as_of=TODAY)
    path = pack / "normalized/corpus.jsonl"
    records = [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]
    for record in records:
        if record["document_id"] == RESTRICTED:
            record["content"] = "annual leave request API_SECRET_123 " * 1000
    path.write_text("\n".join(json.dumps(record) for record in records), encoding="utf-8")
    assert retrieve(Catalog(pack), "u-eng-104", question, as_of=TODAY) == expected
    records = [record for record in records if record["document_id"] != RESTRICTED]
    path.write_text("\n".join(json.dumps(record) for record in records), encoding="utf-8")
    assert retrieve(Catalog(pack), "u-eng-104", question, as_of=TODAY) == expected
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize(
    "question",
    [
        "What is our process for approving a new enterprise vendor?",
        "How do we onboard a supplier that will access company systems?",
        "Explain enterprise supplier approval requirements",
    ],
)
def test_current_vendor_evidence_and_matrix(catalog, question):
    result = retrieve(catalog, "u-proc-310", question, as_of=TODAY)
    keys = {(hit["document_id"], hit["version"]) for hit in result["evidence"]}
    assert ("APX-PROC-POL-014", "3.0") in keys
    assert ("APX-PROC-MTX-006", "1.2") in keys
    assert ("APX-PROC-POL-014", "2.1") not in keys


def test_citations_are_stable_exact_source_spans(catalog):
    for document in catalog.authorized_documents("u-hr-207"):
        first = chunks(document)
        assert first == chunks(document)
        assert len({chunk.citation_id for chunk in first}) == len(first)
        for chunk in first:
            assert (
                chunk.text
                == "\n".join(
                    document.content.splitlines()[chunk.line_start - 1 : chunk.line_end]
                ).strip()
            )
            assert chunk.citation_id.startswith(document.key + ":L")


def test_retired_future_and_unknown_status_excluded(catalog):
    document = catalog.authorized_documents("u-proc-310")[0]
    for alternative in (
        replace(document, status="Retired"),
        replace(document, status="UNKNOWN"),
        replace(document, effective_date="2099-01-01"),
    ):
        assert rank((alternative,), "vendor approval", 8, TODAY) == []


def test_unverified_content_is_labelled_and_cannot_execute(catalog):
    result = retrieve(catalog, "u-eng-104", "legacy assistant migration notes", as_of=TODAY)
    notes = [hit for hit in result["evidence"] if hit["status"] == "Unverified"]
    assert notes and all(hit["warning"] for hit in notes)
    assert RESTRICTED not in json.dumps(result)


def test_invalid_requests(catalog):
    for question, limit in (("", 8), ("x" * 4001, 8), ("vendor", 0), ("vendor", 51)):
        assert retrieve(catalog, "u-eng-104", question, limit)["state"] == "invalid_request"


def test_cli_json_and_exit_codes():
    command = [sys.executable, "-m", "apex_assistant", "retrieve", "--question", "vendor"]
    result = subprocess.run(
        command + ["--user", "unknown"], cwd=ROOT, text=True, capture_output=True, check=False
    )
    assert result.returncode == 2
    assert json.loads(result.stdout) == {"state": "identity_denied", "evidence": []}
    assert result.stderr == ""


def test_case_specific_and_general_hr_queries(catalog):
    specific = "For case APX-HR-CASE-778, why was the employee placed on administrative leave?"
    hr = retrieve(catalog, "u-hr-207", specific, as_of=TODAY)
    assert hr["evidence"]
    assert {hit["document_id"] for hit in hr["evidence"]} == {RESTRICTED}
    engineering = retrieve(catalog, "u-eng-104", specific, as_of=TODAY)
    assert engineering == {"state": "no_authorized_evidence", "evidence": []}
    for user in ("u-eng-104", "u-hr-207"):
        result = retrieve(catalog, user, "How do employees request annual leave?", as_of=TODAY)
        assert RESTRICTED not in json.dumps(result)


def test_retrieval_evaluator_and_broken_access(catalog):
    from apex_assistant.evaluation import evaluate_retrieval

    cases = [
        json.loads(line)
        for line in (ROOT / "evaluation/cases.jsonl").read_text().splitlines()
        if line.strip()
    ]
    report = evaluate_retrieval(catalog, cases)
    assert report["passed"]
    assert not report["submission_ready"]
    original = catalog.authorized_documents
    with patch.object(catalog, "authorized_documents", side_effect=lambda _: original("u-hr-207")):
        broken = evaluate_retrieval(catalog, cases)
    assert not broken["passed"]


def test_evaluator_failure_exits_nonzero(tmp_path):
    cases_path = tmp_path / "cases.jsonl"
    case = {
        "case_id": "deliberately-impossible",
        "user_id": "u-eng-104",
        "question": "vendor",
        "required_source_ids": ["MISSING"],
        "forbidden_source_ids": [],
        "expected_outcome": "answered",
        "release_blocking": True,
    }
    cases_path.write_text(json.dumps(case), encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "apex_assistant",
            "evaluate",
            "--stage",
            "retrieval",
            "--cases",
            str(cases_path),
            "--output",
            str(tmp_path / "results"),
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 1
    assert not json.loads(result.stdout)["passed"]
