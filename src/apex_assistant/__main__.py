"""Build 1 exposes evidence retrieval; answer composition follows in Build 2."""

import argparse
import json
from pathlib import Path

from .access import Catalog, ConfigurationError
from .assistant import answer
from .evaluation import evaluate_full, evaluate_retrieval, write_report
from .retrieval import retrieve


def main() -> int:
    parser = argparse.ArgumentParser(description="ApexOne authorized evidence retrieval")
    subparsers = parser.add_subparsers(dest="command", required=True)
    search = subparsers.add_parser("retrieve", help="Return source excerpts, not a final answer")
    search.add_argument("--user", required=True)
    search.add_argument("--question", required=True)
    search.add_argument("--limit", type=int, default=8)
    search.add_argument("--data-dir", type=Path, default=Path("data/assessment"))
    ask = subparsers.add_parser("ask", help="Return an evidence-backed answer")
    ask.add_argument("--user", required=True)
    ask.add_argument("--question", required=True)
    ask.add_argument("--data-dir", type=Path, default=Path("data/assessment"))
    evaluate = subparsers.add_parser("evaluate", help="Run repeatable checks")
    evaluate.add_argument("--stage", choices=["retrieval", "full"], default="full")
    evaluate.add_argument("--data-dir", type=Path, default=Path("data/assessment"))
    evaluate.add_argument("--cases", type=Path, default=Path("evaluation/cases.jsonl"))
    evaluate.add_argument("--output", type=Path, default=Path("evaluation/results"))
    args = parser.parse_args()
    try:
        if args.command == "evaluate":
            cases = [
                json.loads(line)
                for line in args.cases.read_text("utf-8").splitlines()
                if line.strip()
            ]
            catalog = Catalog(args.data_dir)
            report = (
                evaluate_retrieval(catalog, cases)
                if args.stage == "retrieval"
                else evaluate_full(catalog, cases)
            )
            write_report(report, args.output)
            print(json.dumps(report, indent=2))
            return 0 if report["passed"] else 1
        catalog = Catalog(args.data_dir)
        result = (
            answer(catalog, args.user, args.question)
            if args.command == "ask"
            else retrieve(catalog, args.user, args.question, args.limit)
        )
    except (ConfigurationError, OSError, ValueError, KeyError, TypeError):
        result = {"state": "configuration_error", "evidence": []}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return (
        0
        if result["state"]
        in {
            "evidence_found",
            "answered",
            "answered_with_warning",
            "insufficient_evidence",
            "no_authorized_evidence",
        }
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
