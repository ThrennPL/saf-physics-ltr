from __future__ import annotations

from pathlib import Path

from tools.ops_cycle_runner import _write_blocker_incident


def test_write_blocker_incident_creates_markdown_file(tmp_path: Path) -> None:
    payload: dict[str, object] = {
        "timestamp_utc": "2026-07-02T12:00:00Z",
        "cycle": "weekly",
        "result": "Blocker",
        "steps": [
            {
                "task": "quality-gates-offline",
                "status": "Blocker",
                "exit_code": 1,
                "summary": "forced failure",
            },
            {
                "task": "migration-metrics-report",
                "status": "OK",
                "exit_code": 0,
                "summary": "ok",
            },
        ],
    }

    out = _write_blocker_incident(
        repo_root=tmp_path,
        payload=payload,
        incident_owner="OwnerX",
        incident_eta="<=8h",
        incident_impact="Krytyczny impact test",
    )

    assert out.exists()
    assert out.parent == tmp_path / "docs" / "operations" / "incidents"
    content = out.read_text(encoding="utf-8")
    assert "# Incident Report (Auto)" in content
    assert "- Owner: OwnerX" in content
    assert "- ETA: <=8h" in content
    assert "- Impact: Krytyczny impact test" in content
    assert "Task=quality-gates-offline; Exit=1; Summary=forced failure" in content
    assert "Task=migration-metrics-report" not in content
    assert "## Action Plan" in content
    assert "- [TBD] Root cause analysis" in content
