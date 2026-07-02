from __future__ import annotations

from tools.ops_health_snapshot import _open_escalations_count, _overall_status


def test_open_escalations_count_uses_current_state() -> None:
    events = [
        {
            "incident_path": "docs/operations/incidents/a.md",
            "escalation_key": "docs/operations/incidents/a.md",
            "status": "open",
        },
        {
            "incident_path": "docs/operations/incidents/a.md",
            "escalation_key": "docs/operations/incidents/a.md",
            "status": "resolved",
        },
        {
            "incident_path": "docs/operations/incidents/b.md",
            "escalation_key": "docs/operations/incidents/b.md",
            "status": "open",
        },
    ]
    assert _open_escalations_count(events) == 1


def test_overall_status_rules() -> None:
    assert _overall_status("OK", 0, 0) == "OK"
    assert _overall_status("OK", 0, None) == "Warning"
    assert _overall_status("unknown", 0, 0) == "Warning"
    assert _overall_status("Blocker", 0, 0) == "Blocker"
    assert _overall_status("OK", 2, 0) == "Blocker"
    assert _overall_status("OK", 0, 1) == "Blocker"
