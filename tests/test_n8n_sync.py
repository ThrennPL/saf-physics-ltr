import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import n8n_sync  # noqa: E402


def test_to_export_keeps_only_allowed_fields():
    wf = {"id": "x", "name": "A", "nodes": [], "connections": {}, "settings": {}, "active": False}
    assert set(n8n_sync.to_export(wf)) == {"name", "nodes", "connections", "settings"}


def test_update_body_normalizes_settings():
    body = n8n_sync.to_update_body({"name": "A", "nodes": [], "connections": {}, "settings": {"binaryMode": "separate"}})
    assert body["settings"] == {"executionOrder": "v1"}


def test_secret_detection():
    assert n8n_sync.has_secret("Authorization: Bearer abcdefghijklmnop1234")
    assert not n8n_sync.has_secret("plain text")


def test_invalid_id_rejected():
    with pytest.raises(SystemExit):
        n8n_sync.check_id("../x")


def test_missing_key_is_blocker(monkeypatch):
    for name in n8n_sync.KEY_VARS:
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(n8n_sync.sys, "platform", "linux")
    with pytest.raises(SystemExit):
        n8n_sync.get_api_key()


def test_restore_creates_only_missing(tmp_path, monkeypatch):
    import json

    for name in ("A", "B"):
        (tmp_path / f"{name}.json").write_text(
            json.dumps({"name": name, "nodes": [], "connections": {}}), encoding="utf-8"
        )
    calls = []

    def fake_request(method, path, payload=None):
        calls.append((method, path))
        if method == "GET":
            return {"data": [{"id": "x1", "name": "A"}]}
        return {"id": "n1", "name": payload["name"]}

    monkeypatch.setattr(n8n_sync, "request", fake_request)
    assert n8n_sync.main(["restore", str(tmp_path)]) == 0
    assert [c for c in calls if c[0] == "POST"] == [("POST", "/workflows")]


def test_compare_workflows_detects_differences():
    same = {"nodes": [{"name": "A"}], "connections": {}}
    assert n8n_sync.compare_workflows(same, dict(same, name="x")) == []
    assert n8n_sync.compare_workflows(same, {"nodes": [], "connections": {}}) == ["nodes"]


def test_check_reports_mismatch_and_missing(tmp_path, monkeypatch, capsys):
    (tmp_path / "a.json").write_text('{"name":"A","nodes":[],"connections":{}}', encoding="utf-8")
    (tmp_path / "b.json").write_text('{"name":"B","nodes":[],"connections":{}}', encoding="utf-8")
    remote = {"A": {"nodes": [{"name": "x"}], "connections": {}}}

    def fake(method, path, payload=None):
        if path.startswith("/workflows?"):
            return {"data": [{"id": "id1", "name": "A"}, {"id": "id2", "name": "Zlaczony"}]}
        return remote["A"]

    monkeypatch.setattr(n8n_sync, "request", fake)
    args = n8n_sync.build_parser().parse_args(["check", str(tmp_path)])
    assert args.func(args) == 1
    out = capsys.readouterr().out
    assert "rozbiezne" in out and "brak w n8n: B" in out and "brak pliku w repo: Zlaczony" in out
