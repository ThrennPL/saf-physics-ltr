#!/usr/bin/env python
"""Manage escalation queue status transitions in an append-only JSONL log."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _queue_path(repo_root: Path) -> Path:
    return repo_root / "docs" / "operations" / "escalation_queue.jsonl"


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


def _append_event(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=True) + "\n")


def _incident_key(event: dict[str, Any]) -> str:
    return str(event.get("escalation_key") or event.get("incident_path") or "")


def _current_status_map(events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    state: dict[str, dict[str, Any]] = {}
    for event in events:
        key = _incident_key(event)
        if not key:
            continue
        state[key] = event
    return state


def _list_current(events: list[dict[str, Any]], status_filter: str) -> list[dict[str, Any]]:
    state = _current_status_map(events)
    items = list(state.values())
    if status_filter == "all":
        return sorted(items, key=lambda x: str(x.get("timestamp_utc", "")), reverse=True)
    return sorted(
        [item for item in items if str(item.get("status", "")) == status_filter],
        key=lambda x: str(x.get("timestamp_utc", "")),
        reverse=True,
    )


def _transition(
    queue: Path,
    incident_path: str,
    actor: str,
    note: str,
    target_status: str,
) -> int:
    events = _load_events(queue)
    current = _current_status_map(events).get(incident_path)
    if current is None:
        print(f"[ERROR] Nie znaleziono eskalacji dla incident_path={incident_path}")
        return 1

    current_status = str(current.get("status", ""))
    if target_status == "acknowledged" and current_status != "open":
        print(f"[ERROR] ack wymaga status=open, obecny={current_status}")
        return 1
    if target_status == "resolved" and current_status != "acknowledged":
        print(f"[ERROR] resolve wymaga status=acknowledged, obecny={current_status}")
        return 1

    blockers_raw = current.get("blockers")
    blockers_value = blockers_raw if isinstance(blockers_raw, int) else 1

    payload: dict[str, Any] = {
        "timestamp_utc": _now_iso(),
        "source": "escalation_queue_manager",
        "event_type": "status_change",
        "status": target_status,
        "previous_status": current_status,
        "severity": str(current.get("severity", "critical")),
        "fail_closed": bool(current.get("fail_closed", True)),
        "escalation_required": bool(current.get("escalation_required", True)),
        "cycle": str(current.get("cycle", "unknown")),
        "result": str(current.get("result", "Blocker")),
        "blockers": blockers_value,
        "owner": str(current.get("owner", "Orkiestrator")),
        "eta": str(current.get("eta", "TBD")),
        "impact": str(current.get("impact", "TBD")),
        "summary": str(current.get("summary", "Brak")),
        "incident_path": incident_path,
        "escalation_key": incident_path,
        "actor": actor,
        "note": note,
    }
    _append_event(queue, payload)
    print(f"[OK] {target_status} incident_path={incident_path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage escalation queue")
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list", help="List current escalation states")
    list_parser.add_argument(
        "--status",
        choices=["open", "acknowledged", "resolved", "all"],
        default="open",
    )

    ack_parser = sub.add_parser("ack", help="Acknowledge escalation")
    ack_parser.add_argument("--incident-path", required=True)
    ack_parser.add_argument("--actor", default="Orkiestrator")
    ack_parser.add_argument("--note", default="")

    resolve_parser = sub.add_parser("resolve", help="Resolve escalation")
    resolve_parser.add_argument("--incident-path", required=True)
    resolve_parser.add_argument("--actor", default="Orkiestrator")
    resolve_parser.add_argument("--note", default="")

    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    queue = _queue_path(repo_root)

    if args.command == "list":
        events = _load_events(queue)
        current = _list_current(events, args.status)
        print(f"[SUMMARY] current={len(current)} status={args.status}")
        for item in current:
            print(
                "[ITEM] status={status} incident={incident} owner={owner} eta={eta}".format(
                    status=item.get("status", "-"),
                    incident=item.get("incident_path", "-"),
                    owner=item.get("owner", "-"),
                    eta=item.get("eta", "-"),
                )
            )
        return 0

    if args.command == "ack":
        return _transition(
            queue=queue,
            incident_path=args.incident_path,
            actor=args.actor,
            note=args.note,
            target_status="acknowledged",
        )

    if args.command == "resolve":
        return _transition(
            queue=queue,
            incident_path=args.incident_path,
            actor=args.actor,
            note=args.note,
            target_status="resolved",
        )

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
