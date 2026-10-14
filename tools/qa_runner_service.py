#!/usr/bin/env python
from __future__ import annotations

import hmac
import json
import os
import re
import subprocess
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
MAX_REQUEST_BYTES = 1024
MAX_LOG_REQUEST_BYTES = 32_768
LOG_FILE_NAME = "Cross-Reference-Log-LTR.md"
TOPIC_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,80}$")
ARXIV_ID_RE = re.compile(r"^(\d{4}\.\d{4,5}|[a-z\-]+(\.[A-Za-z\-]{2,10})?/\d{7})$")
ARXIV_URL_RE = re.compile(r"^https?://arxiv\.org/abs/[A-Za-z0-9./\-]{1,40}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MAX_OUTPUT_CHARS = 20_000
CHECK_COMMANDS: dict[str, tuple[str, ...]] = {
    "lint_ltr": (str(ROOT / "tools" / "lint_ltr.py"), "--fail-on-warning"),
    "taxonomy_guard": (str(ROOT / "tools" / "taxonomy_guard.py"),),
    "pytest": ("-m", "pytest"),
}


def _truncate(value: str) -> str:
    if len(value) <= MAX_OUTPUT_CHARS:
        return value
    return value[:MAX_OUTPUT_CHARS] + "\n[output truncated]"


QUERY_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 .,:+\-_'\"()]{0,199}$")
CATEGORY_RE = re.compile(r"^[a-z][a-z\-]{1,20}(\.[A-Za-z\-]{1,10})?$")


def validate_arxiv_params(payload: Any) -> tuple[str, int, list[str]]:
    if not isinstance(payload, dict):
        raise ValueError("body must be a JSON object")
    query = payload.get("query")
    if not isinstance(query, str) or not QUERY_RE.match(query.strip()):
        raise ValueError("invalid query")
    max_results = payload.get("max", 10)
    if isinstance(max_results, bool) or not isinstance(max_results, int) or not 1 <= max_results <= 20:
        raise ValueError("max must be an integer 1-20")
    categories = payload.get("categories", [])
    if not isinstance(categories, list) or len(categories) > 5:
        raise ValueError("categories must be a list of up to 5 items")
    for category in categories:
        if not isinstance(category, str) or not CATEGORY_RE.match(category):
            raise ValueError("invalid category")
    return query.strip(), max_results, categories


def _clean_text(value: Any, field: str, limit: int) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError(f"invalid {field}")
    if any(ord(ch) < 32 for ch in value):
        raise ValueError(f"invalid {field}")
    return " ".join(value.replace("|", "/").split())


def validate_log_params(payload: Any) -> tuple[Path, list[dict[str, str]]]:
    if not isinstance(payload, dict) or set(payload) != {"topic", "publications"}:
        raise ValueError("expected exactly: topic, publications")
    topic = payload["topic"]
    if not isinstance(topic, str) or not TOPIC_RE.fullmatch(topic):
        raise ValueError("invalid topic")
    base = (ROOT / "Badania").resolve()
    log_path = (base / topic / LOG_FILE_NAME).resolve()
    if log_path.parent.parent != base or not log_path.is_file():
        raise ValueError("unknown topic or missing log file")
    pubs = payload["publications"]
    if not isinstance(pubs, list) or not 1 <= len(pubs) <= 20:
        raise ValueError("publications must be a list of 1-20 items")
    cleaned: list[dict[str, str]] = []
    for pub in pubs:
        if not isinstance(pub, dict) or set(pub) != {"id", "title", "authors", "date", "url"}:
            raise ValueError("invalid publication fields")
        pub_id, date, url = pub["id"], pub["date"], pub["url"]
        if not (isinstance(pub_id, str) and ARXIV_ID_RE.fullmatch(pub_id)):
            raise ValueError("invalid arxiv id")
        if not (isinstance(date, str) and DATE_RE.fullmatch(date)):
            raise ValueError("invalid date")
        if not (isinstance(url, str) and ARXIV_URL_RE.fullmatch(url)):
            raise ValueError("invalid url")
        cleaned.append(
            {
                "id": pub_id,
                "date": date,
                "url": url,
                "title": _clean_text(pub["title"], "title", 300),
                "authors": _clean_text(pub["authors"], "authors", 300),
            }
        )
    return log_path, cleaned


def append_literature_log(log_path: Path, pubs: list[dict[str, str]]) -> dict[str, Any]:
    raw = log_path.read_bytes()
    existing = raw.decode("utf-8")
    new = [p for p in pubs if p["id"] not in existing]
    skipped = [p["id"] for p in pubs if p["id"] in existing]
    if not new:
        return {"status": "Warning", "added": 0, "skipped": skipped, "file": log_path.name}
    eol = "\r\n" if b"\r\n" in raw else "\n"
    today = time.strftime("%Y-%m-%d")
    lines = [
        "",
        f"## Kandydaci literatury z arXiv ({today}) - do weryfikacji",
        "- Zrodlo: arXiv (preprinty, brak recenzji); wybor dokonany przez uzytkownika w workflow n8n.",
        "- To nie sa zweryfikowane claimy; wpis do tabeli claim -> source wymaga zgody wlasciciela badania.",
        "",
        "| ArXiv ID | Data | Autorzy | Tytul | URL | Typ zrodla | Status |",
        "|---|---|---|---|---|---|---|",
    ]
    lines += [
        f"| {p['id']} | {p['date']} | {p['authors']} | {p['title']} | {p['url']} | preprint | do_weryfikacji |"
        for p in new
    ]
    prefix = "" if raw.endswith(b"\n") else eol
    with log_path.open("ab") as handle:
        handle.write((prefix + eol.join(lines) + eol).encode("utf-8"))
    return {"status": "OK", "added": len(new), "skipped": skipped, "file": log_path.name}


def run_command(name: str, command: tuple[str, ...], timeout: int = 120) -> dict[str, Any]:
    started = time.monotonic()
    try:
        result = subprocess.run(
            [sys.executable, *command],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            shell=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {
            "check": name,
            "status": "Blocker",
            "exit_code": None,
            "duration_ms": round((time.monotonic() - started) * 1000),
            "stdout": "",
            "stderr": f"Check exceeded the {timeout} second timeout",
        }
    except OSError as exc:
        return {
            "check": name,
            "status": "Blocker",
            "exit_code": None,
            "duration_ms": round((time.monotonic() - started) * 1000),
            "stdout": "",
            "stderr": f"Could not start check: {exc}",
        }

    return {
        "check": name,
        "status": "OK" if result.returncode == 0 else "Warning",
        "exit_code": result.returncode,
        "duration_ms": round((time.monotonic() - started) * 1000),
        "stdout": _truncate(result.stdout),
        "stderr": _truncate(result.stderr),
    }


def run_check(name: str) -> dict[str, Any]:
    command = CHECK_COMMANDS.get(name)
    if command is None:
        raise KeyError(name)
    return run_command(name, command)


def run_arxiv_search(query: str, max_results: int, categories: list[str]) -> dict[str, Any]:
    command: list[str] = [str(ROOT / "tools" / "arxiv_search.py"), "--max", str(max_results)]
    for category in categories:
        command += ["--cat", category]
    command += ["--", query]
    return run_command("arxiv_search", tuple(command), timeout=90)


def make_handler(token: str) -> type[BaseHTTPRequestHandler]:
    class QAHandler(BaseHTTPRequestHandler):
        server_version = "RepoQARunner/1.0"
        sys_version = ""

        def _send_json(self, status_code: int, payload: dict[str, Any]) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def _authorized(self) -> bool:
            supplied = self.headers.get("Authorization", "")
            expected = f"Bearer {token}"
            if not hmac.compare_digest(supplied, expected):
                self._send_json(401, {"error": "unauthorized"})
                return False
            return True

        def do_GET(self) -> None:
            if not self._authorized():
                return
            if urlsplit(self.path).path != "/v1/checks":
                self._send_json(404, {"error": "not_found"})
                return
            self._send_json(200, {"checks": sorted(CHECK_COMMANDS)})

        def do_POST(self) -> None:
            if not self._authorized():
                return

            length_text = self.headers.get("Content-Length", "0")
            try:
                content_length = int(length_text)
            except ValueError:
                self._send_json(400, {"error": "bad_content_length"})
                return
            if content_length < 0:
                self._send_json(400, {"error": "bad_content_length"})
                return
            path = urlsplit(self.path).path
            limit = MAX_LOG_REQUEST_BYTES if path == "/v1/literature/log" else MAX_REQUEST_BYTES
            if content_length > limit:
                self._send_json(413, {"error": "request_too_large"})
                return
            raw_body = self.rfile.read(content_length)

            if path == "/v1/literature/log":
                try:
                    log_path, pubs = validate_log_params(json.loads(raw_body or b"null"))
                except (ValueError, UnicodeDecodeError) as exc:
                    self._send_json(400, {"error": "bad_request", "detail": str(exc)})
                    return
                self._send_json(200, append_literature_log(log_path, pubs))
                return
            if path == "/v1/literature/arxiv":
                try:
                    params = validate_arxiv_params(json.loads(raw_body or b"null"))
                except (ValueError, UnicodeDecodeError) as exc:
                    self._send_json(400, {"error": "bad_request", "detail": str(exc)})
                    return
                self._send_json(200, run_arxiv_search(*params))
                return
            prefix = "/v1/checks/"
            if not path.startswith(prefix):
                self._send_json(404, {"error": "not_found"})
                return
            name = path.removeprefix(prefix)
            if "/" in name or name not in CHECK_COMMANDS:
                self._send_json(404, {"error": "unknown_check"})
                return
            self._send_json(200, run_check(name))

        def log_message(self, format: str, *args: object) -> None:
            super().log_message(format, *args)

    return QAHandler


def create_server(host: str, port: int, token: str) -> ThreadingHTTPServer:
    if len(token) < 32:
        raise ValueError("QA_RUNNER_TOKEN must contain at least 32 characters")
    return ThreadingHTTPServer((host, port), make_handler(token))


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Allowlisted local repository QA runner")
    parser.add_argument("--host", default="127.0.0.1", help="Bind address (use 0.0.0.0 for Docker)")
    parser.add_argument("--port", type=int, default=8765, help="Listen port")
    args = parser.parse_args()

    token = os.environ.get("QA_RUNNER_TOKEN", "")
    if len(token) < 32:
        parser.error("QA_RUNNER_TOKEN must be set and contain at least 32 characters")

    server = create_server(args.host, args.port, token)
    print(f"QA runner listening on {args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("QA runner stopping")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
