#!/usr/bin/env python
from __future__ import annotations

import hmac
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
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
    if not isinstance(payload, dict) or not {"topic", "publications"} <= set(payload) <= {
        "topic",
        "publications",
        "approved_by",
    }:
        raise ValueError("expected: topic, publications, optional approved_by")
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


def validate_approved_by(payload: Any) -> str | None:
    value = payload.get("approved_by") if isinstance(payload, dict) else None
    if value is None:
        return None
    if not isinstance(value, str) or not 2 <= len(value.strip()) <= 80:
        raise ValueError("invalid approved_by")
    return _clean_text(value, "approved_by", 80)


def append_literature_log(
    log_path: Path, pubs: list[dict[str, str]], approved_by: str | None = None
) -> dict[str, Any]:
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
        f"- Wybor zatwierdzil: {approved_by}." if approved_by else "- Wybor zatwierdzil: formularz n8n (osoba nie podana).",
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


SRC_MVP = "Artefakty-Wymagania.md (MVP)"
SRC_FULL = "Artefakty-Wymagania.md (pelny zestaw)"
SRC_G2 = "Artefakty-Wymagania.md (Gate 2) / Checklista-Research-Gate"
SRC_OPS = "quality-gates / walidacja jezykowa PL (wymog procesu)"
# Konfiguracja domenowa: nazwa artefaktu -> zrodlo wymagania.
# Przypisanie Risk/Measurement Pack do Gate 2 to decyzja wlasciciela (Q-002 potwierdzone).
GATE_ARTIFACT_SOURCES: dict[int, dict[str, str]] = {
    1: {
        "Karta-Badania.md": SRC_MVP,
        "Experiment-Context-Pack-Teoretyczna.md": SRC_MVP,
        "Orkiestrator-Log.md": SRC_MVP,
        "Plan-Strumieni.md": SRC_MVP,
    },
    2: {
        "Plan-Danych.md": SRC_G2,
        "Plan-Walidacji.md": SRC_G2,
        "Risk-and-Safety-Pack-Teoretyczna.md": SRC_FULL,
        "Measurement-Integrity-Pack-Teoretyczna.md": SRC_FULL,
    },
    3: {
        "Raport-Wyprowadzen-LTR.md": SRC_FULL,
        "Rejestr-Walidacji-Formalnej-LTR.md": SRC_FULL,
        "Cross-Reference-Log-LTR.md": SRC_FULL,
        "Reproducibility-Pack-Teoretyczna.md": SRC_FULL,
        "Checklista-Gate3-Teoria-LTR.md": SRC_FULL,
    },
    4: {
        "Measurement-Integrity-Pack-Teoretyczna.md": SRC_FULL,
        "Risk-and-Safety-Pack-Teoretyczna.md": SRC_FULL,
        "Reproducibility-Pack-Teoretyczna.md": SRC_FULL,
        "Raport-Wyprowadzen-LTR.md": SRC_FULL,
        "Rejestr-Walidacji-Formalnej-LTR.md": SRC_FULL,
        "Cross-Reference-Log-LTR.md": SRC_FULL,
        "Raport-Wynikowy.md": SRC_FULL,
        "Checklista-Gate3-Teoria-LTR.md": SRC_FULL,
        "Checklista-Gate4-Auditability.md": SRC_FULL,
        "Akceptacje-Decyzje.md": SRC_FULL,
        "Walidacja-Jezykowa-PL.md": SRC_OPS,
    },
}
GATE_REQUIRED_ARTIFACTS: dict[int, tuple[str, ...]] = {
    gate: tuple(items) for gate, items in GATE_ARTIFACT_SOURCES.items()
}
MAX_DOC_BYTES = 2_000_000
QUESTION_RE = re.compile(r"\bQ-\d{3}\b")
CLOSED_RE = re.compile(r"(?<!nie)(?<!nie )zamkni", re.IGNORECASE)
CLAIM_ROW_RE = re.compile(r"^\|\s*[A-Z0-9]+-CL-\d+\s*\|")


def validate_gate_params(payload: Any) -> tuple[Path, int]:
    if not isinstance(payload, dict) or set(payload) != {"topic", "gate"}:
        raise ValueError("expected exactly: topic, gate")
    topic, gate = payload["topic"], payload["gate"]
    if not isinstance(topic, str) or not TOPIC_RE.fullmatch(topic):
        raise ValueError("invalid topic")
    if isinstance(gate, bool) or gate not in GATE_REQUIRED_ARTIFACTS:
        raise ValueError("gate must be one of 1, 2, 3, 4")
    base = (ROOT / "Badania").resolve()
    folder = (base / topic).resolve()
    if folder.parent != base or not folder.is_dir():
        raise ValueError("unknown topic")
    return folder, gate


PROCESS_SUITE_REPORT = "Raport-Process-Suite-{topic}.md"


def build_gate_pack(folder: Path, gate: int) -> dict[str, Any]:
    """Raport tylko do odczytu: kompletnosc artefaktow, zrodla i otwarte luki."""
    required = GATE_REQUIRED_ARTIFACTS[gate]
    missing = [name for name in required if not (folder / name).is_file()]
    claim_status: dict[str, int] = {}
    pending_preprints = 0
    questions: set[str] = set()
    closed: set[str] = set()
    placeholders: list[dict[str, Any]] = []
    for doc in sorted(folder.glob("*.md")):
        if doc.stat().st_size > MAX_DOC_BYTES:
            continue
        text = doc.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            ids = QUESTION_RE.findall(line)
            if ids:
                questions.update(ids)
                if CLOSED_RE.search(line):
                    closed.update(ids)
        count = text.count("DO_UZUPELNIENIA")
        if count:
            placeholders.append({"file": doc.name, "count": count})
        if doc.name == "Cross-Reference-Log-LTR.md":
            for line in text.splitlines():
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if CLAIM_ROW_RE.match(line):
                    claim_status[cells[-1]] = claim_status.get(cells[-1], 0) + 1
                elif line.startswith("|") and cells and cells[-1] == "do_weryfikacji":
                    pending_preprints += 1
    suite_file = folder / PROCESS_SUITE_REPORT.format(topic=folder.name.split("-", 1)[0])
    process_suite = {"file": suite_file.name, "present": suite_file.is_file(), "modified": None}
    if process_suite["present"]:
        process_suite["modified"] = datetime.fromtimestamp(suite_file.stat().st_mtime, timezone.utc).strftime("%Y-%m-%d")
    open_questions = sorted(questions - closed)
    placeholders.sort(key=lambda item: (-item["count"], item["file"]))
    status = "OK"
    if missing:
        status = "Blocker"
    elif pending_preprints or placeholders or open_questions or any(k != "verified" for k in claim_status):
        status = "Warning"
    return {
        "status": status,
        "topic": folder.name,
        "gate": gate,
        "artifacts": {
            "required": list(required),
            "missing": missing,
            "sources": GATE_ARTIFACT_SOURCES[gate],
        },
        "process_suite": process_suite,
        "sources": {"claims_by_status": claim_status, "pending_preprints": pending_preprints},
        "markers": {
            "open_questions": open_questions,
            "closed_questions": sorted(closed),
            "placeholders_total": sum(item["count"] for item in placeholders),
            "placeholders_top": placeholders[:10],
        },
    }


def run_command(name: str, command: tuple[str, ...], timeout: int = 120) -> dict[str, Any]:
    started = time.monotonic()
    try:
        result = subprocess.run(
            [sys.executable, *command],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"},
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
            limit = (
                MAX_LOG_REQUEST_BYTES if path == "/v1/literature/log" else MAX_REQUEST_BYTES
            )
            if content_length > limit:
                self._send_json(413, {"error": "request_too_large"})
                return
            raw_body = self.rfile.read(content_length)

            if path == "/v1/gate/pack":
                try:
                    folder, gate = validate_gate_params(json.loads(raw_body or b"null"))
                except (ValueError, UnicodeDecodeError) as exc:
                    self._send_json(400, {"error": "bad_request", "detail": str(exc)})
                    return
                self._send_json(200, build_gate_pack(folder, gate))
                return
            if path == "/v1/literature/log":
                try:
                    log_payload = json.loads(raw_body or b"null")
                    log_path, pubs = validate_log_params(log_payload)
                    approved_by = validate_approved_by(log_payload)
                except (ValueError, UnicodeDecodeError) as exc:
                    self._send_json(400, {"error": "bad_request", "detail": str(exc)})
                    return
                self._send_json(200, append_literature_log(log_path, pubs, approved_by))
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
