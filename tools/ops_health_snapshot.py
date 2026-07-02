#!/usr/bin/env python
"""Generate a one-line operational health snapshot for weekly governance."""

from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []

    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        text = line.strip()
        if not text:
            continue
        payload = json.loads(text)
        if isinstance(payload, dict):
            events.append(payload)
    return events


def _latest_weekly_result(events: list[dict[str, Any]]) -> str:
    weekly = [event for event in events if str(event.get("cycle", "")) == "weekly"]
    if not weekly:
        return "unknown"
    latest = max(weekly, key=lambda x: str(x.get("timestamp_utc", "")))
    return str(latest.get("result", "unknown"))


def _current_escalation_state(events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    state: dict[str, dict[str, Any]] = {}
    for event in events:
        key = str(event.get("escalation_key") or event.get("incident_path") or "")
        if not key:
            continue
        state[key] = event
    return state


def _open_escalations_count(events: list[dict[str, Any]]) -> int:
    current = _current_escalation_state(events)
    return sum(1 for item in current.values() if str(item.get("status", "")) == "open")


def _scheduler_last_result(task_name: str) -> int | None:
    command = (
        f"(Get-ScheduledTaskInfo -TaskName '{task_name}' "
        "-ErrorAction Stop).LastTaskResult"
    )
    cp = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if cp.returncode != 0:
        return None
    text = cp.stdout.strip()
    if not text:
        return None
    try:
        return int(text.splitlines()[-1].strip())
    except ValueError:
        return None


def _overall_status(weekly_result: str, open_count: int, scheduler_result: int | None) -> str:
    if weekly_result == "Blocker" or open_count > 0:
        return "Blocker"
    if scheduler_result not in (None, 0):
        return "Blocker"
    if weekly_result == "unknown" or scheduler_result is None:
        return "Warning"
    return "OK"


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    control_log = repo_root / "docs" / "operations" / "control_cycle_log.jsonl"
    escalation_log = repo_root / "docs" / "operations" / "escalation_queue.jsonl"
    output_json = repo_root / "docs" / "operations" / "ops_health_snapshot.json"
    output_txt = repo_root / "docs" / "operations" / "ops_health_snapshot.txt"

    cycle_events = _load_events(control_log)
    escalation_events = _load_events(escalation_log)

    weekly_result = _latest_weekly_result(cycle_events)
    open_escalations = _open_escalations_count(escalation_events)
    scheduler_result = _scheduler_last_result("SAF-LTR Ops Cycle Weekly")
    status = _overall_status(weekly_result, open_escalations, scheduler_result)

    payload: dict[str, Any] = {
        "timestamp_utc": _now_iso(),
        "status": status,
        "weekly_result": weekly_result,
        "open_escalations": open_escalations,
        "scheduler_last_task_result": scheduler_result,
    }
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )

    scheduler_text = "unknown" if scheduler_result is None else str(scheduler_result)
    line = (
        f"OPS_HEALTH status={status} weekly={weekly_result} "
        f"open_escalations={open_escalations} scheduler_last_result={scheduler_text}"
    )
    output_txt.write_text(line + "\n", encoding="utf-8")

    print(f"[SUMMARY] {line}")
    print(f"[OUTPUT] {output_json.as_posix()}")
    print(f"[OUTPUT] {output_txt.as_posix()}")
    return 0 if status in {"OK", "Warning"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
