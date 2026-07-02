from __future__ import annotations

import json
from pathlib import Path

from tools.escalation_notifier import write_escalation_event


def test_write_escalation_event_appends_jsonl(tmp_path: Path) -> None:
    incident = tmp_path / "docs" / "operations" / "incidents" / "incident_test.md"
    incident.parent.mkdir(parents=True, exist_ok=True)
    incident.write_text("incident", encoding="utf-8")

    payload: dict[str, object] = {
        "cycle": "weekly",
        "result": "Blocker",
        "blockers": 1,
        "steps": [
            {
                "task": "process-suite-t04",
                "status": "Blocker",
                "summary": "forced summary",
            }
        ],
    }

    queue = write_escalation_event(
        repo_root=tmp_path,
        cycle_payload=payload,
        incident_path=incident,
        incident_owner="OwnerY",
        incident_eta="<=2h",
        incident_impact="Impact test",
    )

    assert queue.exists()
    lines = queue.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    event = json.loads(lines[0])
    assert event["source"] == "ops_cycle_runner"
    assert event["status"] == "open"
    assert event["severity"] == "critical"
    assert event["fail_closed"] is True
    assert event["escalation_required"] is True
    assert event["owner"] == "OwnerY"
    assert event["eta"] == "<=2h"
    assert event["impact"] == "Impact test"
    assert event["summary"] == "process-suite-t04: forced summary"
    assert event["incident_path"] == "docs/operations/incidents/incident_test.md"
