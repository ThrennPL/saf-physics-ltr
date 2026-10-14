from __future__ import annotations

import http.client
import json
import threading
import urllib.error
import urllib.request
from collections.abc import Iterator
from http.server import ThreadingHTTPServer

import pytest

from tools import qa_runner_service

TOKEN = "t" * 40


@pytest.fixture
def runner_server() -> Iterator[str]:
    server: ThreadingHTTPServer = qa_runner_service.create_server("127.0.0.1", 0, TOKEN)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address
    try:
        yield f"http://{host}:{port}"
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


def _request(
    base_url: str,
    path: str,
    *,
    method: str = "GET",
    token: str | None = TOKEN,
    body: bytes = b"",
) -> tuple[int, dict[str, object]]:
    headers = {}
    if token is not None:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(
        f"{base_url}{path}",
        data=body if method == "POST" else None,
        headers=headers,
        method=method,
    )
    try:
        response = urllib.request.urlopen(request, timeout=5)
    except urllib.error.HTTPError as exc:
        response = exc
    return response.status, json.loads(response.read())


def test_lists_only_allowlisted_checks(runner_server: str) -> None:
    status, payload = _request(runner_server, "/v1/checks")

    assert status == 200
    assert payload == {"checks": ["lint_ltr", "pytest", "taxonomy_guard"]}


@pytest.mark.parametrize("check", ["lint_ltr", "pytest", "taxonomy_guard"])
def test_runs_allowlisted_check(
    runner_server: str,
    monkeypatch: pytest.MonkeyPatch,
    check: str,
) -> None:
    class Result:
        returncode = 0
        stdout = "passed"
        stderr = ""

    monkeypatch.setattr(qa_runner_service.subprocess, "run", lambda *args, **kwargs: Result())

    status, payload = _request(runner_server, f"/v1/checks/{check}", method="POST")

    assert status == 200
    assert payload["check"] == check
    assert payload["status"] == "OK"
    assert payload["exit_code"] == 0
    assert payload["stdout"] == "passed"


def test_rejects_unknown_and_injected_checks(runner_server: str) -> None:
    status, payload = _request(
        runner_server,
        "/v1/checks/lint_ltr%3Bwhoami",
        method="POST",
    )

    assert status == 404
    assert payload == {"error": "unknown_check"}


@pytest.mark.parametrize("token", [None, "wrong-token"])
def test_requires_bearer_token(runner_server: str, token: str | None) -> None:
    status, payload = _request(runner_server, "/v1/checks", token=token)

    assert status == 401
    assert payload == {"error": "unauthorized"}


def test_rejects_large_request_body(runner_server: str) -> None:
    host, port = runner_server.removeprefix("http://").split(":")
    connection = http.client.HTTPConnection(host, int(port), timeout=5)
    connection.putrequest("POST", "/v1/checks/lint_ltr")
    connection.putheader("Authorization", f"Bearer {TOKEN}")
    connection.putheader("Content-Length", str(qa_runner_service.MAX_REQUEST_BYTES + 1))
    connection.endheaders()
    response = connection.getresponse()
    status = response.status
    payload = json.loads(response.read())
    connection.close()

    assert status == 413
    assert payload == {"error": "request_too_large"}


def test_arxiv_endpoint_passes_validated_args_without_shell(
    runner_server: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, object] = {}

    class Result:
        returncode = 0
        stdout = "| 1234.5678 |"
        stderr = ""

    def fake_run(args: list[str], **kwargs: object) -> Result:
        captured["args"] = args
        captured["kwargs"] = kwargs
        return Result()

    monkeypatch.setattr(qa_runner_service.subprocess, "run", fake_run)
    body = json.dumps({"query": "Yukawa perihelion", "categories": ["gr-qc"], "max": 3}).encode()

    status, payload = _request(runner_server, "/v1/literature/arxiv", method="POST", body=body)

    assert status == 200
    assert payload["check"] == "arxiv_search"
    args = captured["args"]
    assert args[-3:] == ["gr-qc", "--", "Yukawa perihelion"]
    assert captured["kwargs"]["shell"] is False


@pytest.mark.parametrize(
    "payload",
    [
        {"query": "-rf"},
        {"query": "a; whoami"},
        {"query": "ok", "max": 999},
        {"query": "ok", "max": True},
        {"query": "ok", "categories": ["gr-qc; x"]},
        {"query": "ok", "categories": ["gr-qc"] * 6},
        {"max": 3},
        [],
    ],
)
def test_arxiv_endpoint_rejects_invalid_params(runner_server: str, payload: object) -> None:
    status, response = _request(
        runner_server,
        "/v1/literature/arxiv",
        method="POST",
        body=json.dumps(payload).encode(),
    )

    assert status == 400
    assert response["error"] == "bad_request"


def test_requires_long_token() -> None:
    with pytest.raises(ValueError, match="at least 32 characters"):
        qa_runner_service.create_server("127.0.0.1", 0, "too-short")


def _log_payload(**overrides: object) -> bytes:
    pub = {
        "id": "2601.05750",
        "title": "Parameterized | Post-Newtonian Analysis",
        "authors": "Jie Zhu, Hao Li",
        "date": "2026-01-09",
        "url": "http://arxiv.org/abs/2601.05750v3",
    }
    payload: dict[str, object] = {"topic": "T99-Test", "publications": [pub]}
    payload.update(overrides)
    return json.dumps(payload).encode()


@pytest.fixture
def log_root(tmp_path, monkeypatch):
    topic = tmp_path / "Badania" / "T99-Test"
    topic.mkdir(parents=True)
    log = topic / "Cross-Reference-Log-LTR.md"
    log.write_text("# Log\n\n## Uwagi\n- x\n", encoding="utf-8")
    monkeypatch.setattr(qa_runner_service, "ROOT", tmp_path)
    return log


def test_log_endpoint_appends_and_dedupes(runner_server: str, log_root) -> None:
    status, payload = _request(runner_server, "/v1/literature/log", method="POST", body=_log_payload())
    assert status == 200 and payload["added"] == 1
    text = log_root.read_text(encoding="utf-8")
    assert text.startswith("# Log\n\n## Uwagi\n- x\n")
    assert "| 2601.05750 |" in text and "Parameterized / Post-Newtonian" in text
    assert "preprint | do_weryfikacji" in text

    status, payload = _request(runner_server, "/v1/literature/log", method="POST", body=_log_payload())
    assert status == 200 and payload["added"] == 0
    assert log_root.read_text(encoding="utf-8") == text


@pytest.mark.parametrize(
    "overrides",
    [
        {"topic": "../Badania"},
        {"topic": "T98-Missing"},
        {"topic": "..\\x"},
        {"publications": []},
        {"publications": [{"id": "x"}]},
        {"extra": 1},
    ],
)
def test_log_endpoint_rejects_invalid(runner_server: str, log_root, overrides: dict) -> None:
    before = log_root.read_text(encoding="utf-8")
    status, _ = _request(runner_server, "/v1/literature/log", method="POST", body=_log_payload(**overrides))
    assert status == 400
    assert log_root.read_text(encoding="utf-8") == before


def test_log_endpoint_rejects_bad_url_and_id(runner_server: str, log_root) -> None:
    for field, value in (("url", "http://evil.example/abs/1"), ("id", "1; rm")):
        pub = {"id": "2601.05750", "title": "t", "authors": "a", "date": "2026-01-09",
               "url": "http://arxiv.org/abs/2601.05750v3", field: value}
        status, _ = _request(runner_server, "/v1/literature/log", method="POST",
                             body=_log_payload(publications=[pub]))
        assert status == 400


def _gate_payload(**overrides: object) -> bytes:
    payload: dict[str, object] = {"topic": "T99-Test", "gate": 1}
    payload.update(overrides)
    return json.dumps(payload).encode()


def test_gate_pack_reports_missing_and_is_read_only(runner_server: str, log_root) -> None:
    topic = log_root.parent
    (topic / "Karta-Badania.md").write_text("# K\nQ-001 DO_UZUPELNIENIA\n", encoding="utf-8")
    log_root.write_text(
        "| Claim ID | x |\n|---|---|\n| T99-CL-001 | c | s | peer-reviewed | 0.9 | verified |\n"
        "| 1105.2998 | d | a | t | u | preprint | do_weryfikacji |\n",
        encoding="utf-8",
    )
    before = {p.name: p.read_bytes() for p in topic.iterdir()}
    status, payload = _request(runner_server, "/v1/gate/pack", method="POST", body=_gate_payload())
    assert status == 200
    assert payload["status"] == "Blocker"
    assert payload["artifacts"]["missing"] == ["Experiment-Context-Pack-Teoretyczna.md", "Orkiestrator-Log.md", "Plan-Strumieni.md"]
    assert payload["markers"]["open_questions"] == ["Q-001"]
    assert payload["markers"]["placeholders_total"] == 1
    assert payload["sources"] == {"claims_by_status": {"verified": 1}, "pending_preprints": 1}
    assert {p.name: p.read_bytes() for p in topic.iterdir()} == before


@pytest.mark.parametrize(
    "overrides",
    [{"topic": "../x"}, {"topic": "T98-Missing"}, {"gate": 5}, {"gate": True}, {"gate": "1"}, {"extra": 1}],
)
def test_gate_pack_rejects_invalid(runner_server: str, log_root, overrides: dict) -> None:
    status, _ = _request(runner_server, "/v1/gate/pack", method="POST", body=_gate_payload(**overrides))
    assert status == 400


def test_gate_pack_only_open_questions_warn(runner_server: str, log_root) -> None:
    topic = log_root.parent
    for name in (
        "Karta-Badania.md", "Experiment-Context-Pack-Teoretyczna.md",
        "Orkiestrator-Log.md", "Plan-Strumieni.md",
    ):
        (topic / name).write_text("", encoding="utf-8")
    (topic / "Karta-Badania.md").write_text(
        "- Q-001 (wysoki): pytanie\n- Q-002 (zamkniete): ok\n- Zamknieto Q-003\n- Q-004 niezamkniete\n",
        encoding="utf-8",
    )
    log_root.write_text("| Claim ID | x |\n", encoding="utf-8")
    _, payload = _request(runner_server, "/v1/gate/pack", method="POST", body=_gate_payload())
    assert payload["status"] == "Warning"
    assert payload["markers"]["open_questions"] == ["Q-001", "Q-004"]
    assert payload["markers"]["closed_questions"] == ["Q-002", "Q-003"]


def test_gate_pack_ok_when_all_questions_closed(runner_server: str, log_root) -> None:
    topic = log_root.parent
    for name in (
        "Karta-Badania.md", "Experiment-Context-Pack-Teoretyczna.md",
        "Orkiestrator-Log.md", "Plan-Strumieni.md",
    ):
        (topic / name).write_text("Q-009 zamkniete\n", encoding="utf-8")
    log_root.write_text("| Claim ID | x |\n", encoding="utf-8")
    _, payload = _request(runner_server, "/v1/gate/pack", method="POST", body=_gate_payload())
    assert payload["status"] == "OK"
