#!/usr/bin/env python
"""Append escalation events to a local JSONL queue."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path


def _now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _first_blocker_summary(cycle_payload: dict[str, object]) -> str:
    steps = cycle_payload.get("steps", [])
    if not isinstance(steps, list):
        return "Blocker detected in cycle"

    for step in steps:
        if isinstance(step, dict) and str(step.get("status", "")) == "Blocker":
            task = str(step.get("task", "unknown"))
            summary = str(step.get("summary", "Brak szczegolow"))
            return f"{task}: {summary}"

    return "Blocker detected in cycle"


def write_escalation_event(
    repo_root: Path,
    cycle_payload: dict[str, object],
    incident_path: Path,
    incident_owner: str,
    incident_eta: str,
    incident_impact: str,
) -> Path:
    """Persist escalation event for operational follow-up."""
    queue_path = repo_root / "docs" / "operations" / "escalation_queue.jsonl"
    queue_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        incident_rel = incident_path.relative_to(repo_root).as_posix()
    except ValueError:
        incident_rel = incident_path.as_posix()

    blockers_raw = cycle_payload.get("blockers", 0)
    blockers_value = blockers_raw if isinstance(blockers_raw, int) else 0

    event = {
        "timestamp_utc": _now_iso(),
        "source": "ops_cycle_runner",
        "event_type": "open",
        "status": "open",
        "severity": "critical",
        "fail_closed": True,
        "escalation_required": True,
        "cycle": str(cycle_payload.get("cycle", "unknown")),
        "result": str(cycle_payload.get("result", "unknown")),
        "blockers": blockers_value,
        "owner": incident_owner,
        "eta": incident_eta,
        "impact": incident_impact,
        "summary": _first_blocker_summary(cycle_payload),
        "incident_path": incident_rel,
        "escalation_key": incident_rel,
    }

    with queue_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=True) + "\n")

    return queue_path
