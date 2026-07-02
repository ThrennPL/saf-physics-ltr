#!/usr/bin/env python
"""Append and summarize gate timing events for Gate 1-4."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4


def _now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _log_path(repo_root: Path) -> Path:
    return repo_root / "docs" / "operations" / "gate_timing_log.jsonl"


def _append_event(
    repo_root: Path,
    case_id: str,
    gate_id: str,
    action: str,
    actor: str,
    note: str,
    timestamp_utc: str | None,
) -> int:
    log_file = _log_path(repo_root)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    timestamp = timestamp_utc if timestamp_utc else _now_iso()
    event = {
        "event_id": f"GTL-{uuid4().hex[:8]}",
        "timestamp_utc": timestamp,
        "case_id": case_id,
        "gate_id": gate_id,
        "action": action,
        "actor": actor,
        "note": note,
    }

    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=True) + "\n")

    print(f"[OK] zapisano event: {event['event_id']}")
    print(f"[OUTPUT] {log_file.as_posix()}")
    return 0


def _read_events(log_file: Path) -> list[dict[str, str]]:
    if not log_file.exists():
        return []

    events: list[dict[str, str]] = []
    with log_file.open("r", encoding="utf-8") as handle:
        for line in handle:
            text = line.strip()
            if not text:
                continue
            payload = json.loads(text)
            if isinstance(payload, dict):
                events.append({str(k): str(v) for k, v in payload.items()})
    return events


def _report(repo_root: Path, case_id: str | None) -> int:
    log_file = _log_path(repo_root)
    events = _read_events(log_file)

    if case_id:
        events = [event for event in events if event.get("case_id") == case_id]

    events.sort(key=lambda event: event.get("timestamp_utc", ""))
    total_pairs = 0
    by_gate: dict[str, list[float]] = {}
    open_starts: dict[tuple[str, str], list[datetime]] = {}

    for event in events:
        gate_id = event.get("gate_id", "")
        action = event.get("action", "")
        c_id = event.get("case_id", "")
        ts_raw = event.get("timestamp_utc", "")

        try:
            ts = _parse_iso(ts_raw)
        except ValueError:
            continue

        key = (c_id, gate_id)
        if action == "start":
            open_starts.setdefault(key, []).append(ts)
            continue
        if action != "end":
            continue

        starts = open_starts.get(key, [])
        if not starts:
            continue

        start_ts = starts.pop(0)
        duration_h = (ts - start_ts).total_seconds() / 3600.0
        if duration_h < 0:
            continue

        by_gate.setdefault(gate_id, []).append(duration_h)
        total_pairs += 1

    print(f"[SUMMARY] pairs={total_pairs}")
    for gate_id in sorted(by_gate.keys()):
        durations = by_gate[gate_id]
        avg_h = sum(durations) / len(durations)
        print(f"[GATE] {gate_id} count={len(durations)} avg_h={avg_h:.2f}")

    print(f"[OUTPUT] {log_file.as_posix()}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Log and report Gate timing events")
    subparsers = parser.add_subparsers(dest="command", required=True)

    append_parser = subparsers.add_parser("append", help="Append start/end event")
    append_parser.add_argument(
        "--case-id",
        required=True,
        help="Case ID, e.g. T04-GR-PPN-Yukawa-Perihelion",
    )
    append_parser.add_argument("--gate-id", required=True, choices=["G1", "G2", "G3", "G4"])
    append_parser.add_argument("--action", required=True, choices=["start", "end"])
    append_parser.add_argument("--actor", default="Orkiestrator")
    append_parser.add_argument("--note", default="")
    append_parser.add_argument(
        "--timestamp-utc",
        help="Optional explicit timestamp, format YYYY-MM-DDTHH:MM:SSZ",
    )

    report_parser = subparsers.add_parser("report", help="Print aggregate timing report")
    report_parser.add_argument("--case-id", help="Optional case filter")

    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]

    if args.command == "append":
        return _append_event(
            repo_root=repo_root,
            case_id=args.case_id,
            gate_id=args.gate_id,
            action=args.action,
            actor=args.actor,
            note=args.note,
            timestamp_utc=args.timestamp_utc,
        )

    return _report(repo_root=repo_root, case_id=args.case_id)


if __name__ == "__main__":
    raise SystemExit(main())
