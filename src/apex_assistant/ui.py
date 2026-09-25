"""Optional localhost demo using the MIT-licensed Simple Sidebar template."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import mimetypes
import re
import webbrowser
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from .access import Catalog
from .assistant import answer
from .context import visible_topic_tree

DATA = Path("data/assessment")
WEB = Path(__file__).with_name("web")
ASSETS = {"/styles.css", "/template.js", "/app.js", "/app.css"}
MAX_BODY_BYTES = 8192


def demo_identities(catalog: Catalog, data_dir: Path) -> list[tuple[str, str]]:
    """Display only identities validated by the trusted assessment catalog."""
    records = json.loads((data_dir / "access" / "identities.json").read_text("utf-8"))["users"]
    return [
        (f"{record['display_name']} ({record['department']})", record["user_id"])
        for record in records
        if catalog.known_user(record["user_id"])
    ]


def respond(catalog: Catalog, question: str, user_id: str) -> dict:
    """Use the exact assessed answer path; the UI adds no evidence or authority."""
    result = answer(catalog, user_id, question)
    return {
        "state": result["state"],
        "answer": result["answer"],
        "notice": result["notice"],
        "claims": result["claims"],
        "sources": [
            {
                "citation_id": source["citation_id"],
                "document_id": source["document_id"],
                "version": source["version"],
                "title": source["title"],
                "status": source["status"],
                "line_start": source["line_start"],
                "line_end": source["line_end"],
            }
            for source in result["citations"]
        ],
    }


def source_view(catalog: Catalog, user_id: str, citation_id: str) -> dict | None:
    """Resolve a citation only inside the selected identity's authorized view."""
    if len(citation_id) > 256:
        return None
    match = re.fullmatch(r"(.+):L([1-9]\d{0,5})-L([1-9]\d{0,5}):([0-9a-f]{12})", citation_id)
    if not match or not catalog.known_user(user_id):
        return None
    key, first, last, expected_hash = match.groups()
    start, end = int(first), int(last)
    for document in catalog.authorized_documents(user_id):
        if document.key != key:
            continue
        if document.status not in {"Current", "Active", "Active advisory", "Open", "Unverified"}:
            return None
        if date.fromisoformat(document.effective_date) > date.today():
            return None
        lines = document.content.splitlines()
        if end > len(lines) or start > end:
            return None
        raw = "\n".join(lines[start - 1 : end])
        if hashlib.sha256(raw.encode()).hexdigest()[:12] != expected_hash:
            return None
        return {
            "title": document.title,
            "document_id": document.document_id,
            "version": document.version,
            "status": document.status,
            "source_path": document.source_path,
            "line_start": start,
            "line_end": end,
            "lines": [{"number": number, "text": text} for number, text in enumerate(lines, 1)],
        }
    return None


def make_server(port: int = 7860, data_dir: Path = DATA) -> ThreadingHTTPServer:
    """Return a loopback-only server so tests can use an ephemeral port."""
    catalog = Catalog(data_dir)
    identities = demo_identities(catalog, data_dir)
    if not identities:
        raise RuntimeError("No demo identities are available.")

    class Handler(BaseHTTPRequestHandler):
        def _send(self, status: int, body: bytes, content_type: str) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("X-Frame-Options", "DENY")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'self'; connect-src 'self'; script-src 'self'; "
                "style-src 'self' 'unsafe-inline'; img-src 'none'; object-src 'none'",
            )
            self.end_headers()
            self.wfile.write(body)

        def _json(self, status: int, payload: dict) -> None:
            self._send(
                status, json.dumps(payload).encode("utf-8"), "application/json; charset=utf-8"
            )

        def do_GET(self) -> None:  # noqa: N802
            route = urlsplit(self.path)
            if route.path == "/":
                options = "\n".join(
                    f'<option value="{html.escape(user_id, quote=True)}">'
                    f"{html.escape(label)}</option>"
                    for label, user_id in identities
                )
                page = (WEB / "index.html").read_text("utf-8").replace("<!--IDENTITIES-->", options)
                self._send(200, page.encode("utf-8"), "text/html; charset=utf-8")
            elif route.path == "/api/context":
                user_id = parse_qs(route.query).get("user_id", [""])[0]
                self._json(200, visible_topic_tree(catalog, user_id))
            elif route.path == "/api/source":
                params = parse_qs(route.query)
                source = source_view(
                    catalog,
                    params.get("user_id", [""])[0],
                    params.get("citation_id", [""])[0],
                )
                if source is None:
                    self._json(404, {"error": "Source unavailable."})
                else:
                    self._json(200, source)
            elif route.path in ASSETS:
                asset = WEB / route.path.removeprefix("/")
                content_type = mimetypes.guess_type(asset.name)[0] or "application/octet-stream"
                self._send(200, asset.read_bytes(), content_type)
            else:
                self._json(404, {"error": "Not found."})

        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/api/ask":
                self._json(404, {"error": "Not found."})
                return
            origin = self.headers.get("Origin")
            expected_origin = f"http://127.0.0.1:{self.server.server_port}"
            if origin is not None and origin != expected_origin:
                self._json(403, {"error": "Request rejected."})
                return
            if self.headers.get_content_type() != "application/json":
                self._json(415, {"error": "JSON is required."})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= MAX_BODY_BYTES:
                    raise ValueError("Invalid size")
                payload = json.loads(self.rfile.read(length))
                if not isinstance(payload, dict):
                    raise ValueError("Invalid JSON")
                user_id = payload["user_id"]
                question = payload["question"]
                if not isinstance(user_id, str) or not isinstance(question, str):
                    raise ValueError("Invalid input")
            except (ValueError, KeyError, TypeError, UnicodeDecodeError):
                self._json(400, {"error": "Invalid request."})
                return
            self._json(200, respond(catalog, question, user_id))

        def log_message(self, format: str, *args: object) -> None:
            # Do not write questions, identities, source IDs, or case details to logs.
            del format, args

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the optional local ApexOne demo UI.")
    parser.add_argument("--port", type=int, default=7860)
    parser.add_argument("--data-dir", type=Path, default=DATA)
    parser.add_argument("--no-browser", action="store_true", help="Do not open a browser tab.")
    args = parser.parse_args()
    server = make_server(port=args.port, data_dir=args.data_dir)
    url = f"http://127.0.0.1:{server.server_port}/"
    print(f"ApexOne demo UI: {url} (Ctrl+C to stop)", flush=True)
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
