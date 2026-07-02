from __future__ import annotations

import json
from pathlib import Path

from tools.escalation_queue_manager import _append_event, _current_status_map, _transition


def test_transition_open_ack_resolved(tmp_path: Path) -> None:
    queue = tmp_path / "docs" / "operations" / "escalation_queue.jsonl"
    queue.parent.mkdir(parents=True, exist_ok=True)

    incident_path = "docs/operations/incidents/incident_sample.md"
    open_event = {
        "timestamp_utc": "2026-07-02T10:00:00Z",
        "source": "ops_cycle_runner",
        "event_type": "open",
        "status": "open",
        "severity": "critical",
        "fail_closed": True,
        "escalation_required": True,
        "cycle": "weekly",
        "result": "Blocker",
        "blockers": 1,
        "owner": "OwnerA",
        "eta": "<=24h",
        "impact": "Impact",
        "summary": "forced",
        "incident_path": incident_path,
        "escalation_key": incident_path,
    }
    _append_event(queue, open_event)

    ack_code = _transition(queue, incident_path, "OwnerA", "ack now", "acknowledged")
    resolve_code = _transition(queue, incident_path, "OwnerA", "resolved now", "resolved")

    assert ack_code == 0
    assert resolve_code == 0

    entries = [json.loads(line) for line in queue.read_text(encoding="utf-8").splitlines() if line]
    latest = _current_status_map(entries)[incident_path]
    assert latest["status"] == "resolved"
    assert latest["previous_status"] == "acknowledged"
    assert latest["actor"] == "OwnerA"
