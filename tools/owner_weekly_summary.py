#!/usr/bin/env python
"""Build a weekly owner summary from operational control cycle logs."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any


def _parse_ts(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


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


def _load_escalations(path: Path) -> list[dict[str, Any]]:
    return _load_events(path)


def _current_escalation_state(events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    state: dict[str, dict[str, Any]] = {}
    for event in events:
        key = str(event.get("escalation_key") or event.get("incident_path") or "")
        if not key:
            continue
        state[key] = event
    return state


def _within_window(event: dict[str, Any], since: datetime) -> bool:
    ts = _parse_ts(str(event.get("timestamp_utc", "")))
    return ts is not None and ts >= since


def _render(
    generated_at: datetime,
    events: list[dict[str, Any]],
    escalation_events: list[dict[str, Any]],
    output_path: Path,
    source_path: Path,
    escalation_path: Path,
) -> str:
    total = len(events)
    ok_count = sum(1 for event in events if str(event.get("result", "")) == "OK")
    blocker_count = sum(1 for event in events if str(event.get("result", "")) == "Blocker")

    by_cycle: dict[str, int] = {}
    for event in events:
        cycle = str(event.get("cycle", "unknown"))
        by_cycle[cycle] = by_cycle.get(cycle, 0) + 1

    escalation_state = _current_escalation_state(escalation_events)
    escalation_values = list(escalation_state.values())
    esc_open = sum(1 for item in escalation_values if str(item.get("status", "")) == "open")
    esc_ack = sum(1 for item in escalation_values if str(item.get("status", "")) == "acknowledged")
    esc_resolved = sum(1 for item in escalation_values if str(item.get("status", "")) == "resolved")

    lines = [
        "# SAF/LTR Owner Weekly Summary",
        "",
        "## Metadane",
        f"- Data raportu: {generated_at.strftime('%Y-%m-%d %H:%M:%S UTC')}",
        "- Okno analizy: ostatnie 7 dni",
        f"- Zrodlo logu: {source_path.as_posix()}",
        f"- Raport: {output_path.as_posix()}",
        "",
        "## Podsumowanie wykonania",
        f"- Liczba cykli: {total}",
        f"- Wynik OK: {ok_count}",
        f"- Wynik Blocker: {blocker_count}",
        f"- Eskalacje open: {esc_open}",
        f"- Eskalacje acknowledged: {esc_ack}",
        f"- Eskalacje resolved: {esc_resolved}",
        "",
        "## Status biezacy",
    ]

    latest_by_cycle: dict[str, dict[str, Any]] = {}
    for event in events:
        cycle = str(event.get("cycle", "unknown"))
        prev = latest_by_cycle.get(cycle)
        if prev is None or str(event.get("timestamp_utc", "")) > str(prev.get("timestamp_utc", "")):
            latest_by_cycle[cycle] = event

    current_blockers = 0
    for cycle in sorted(latest_by_cycle.keys()):
        result = str(latest_by_cycle[cycle].get("result", "-"))
        if result == "Blocker":
            current_blockers += 1
        lines.append(f"- {cycle}: {result}")

    lines.append(
        f"- escalation_queue: open={esc_open}, "
        f"acknowledged={esc_ack}, resolved={esc_resolved}"
    )

    lines.extend(
        [
            "",
            "## Rozklad cykli",
            "| Typ cyklu | Liczba uruchomien |",
            "|---|---:|",
        ]
    )

    for cycle in sorted(by_cycle.keys()):
        lines.append(f"| {cycle} | {by_cycle[cycle]} |")

    lines.extend(
        [
            "",
            "## Ostatnie uruchomienia",
            "| Timestamp UTC | Cycle | Result | Blockers | Steps |",
            "|---|---|---|---:|---:|",
        ]
    )

    recent = sorted(
        events,
        key=lambda event: str(event.get("timestamp_utc", "")),
        reverse=True,
    )[:10]
    for event in recent:
        timestamp = str(event.get("timestamp_utc", "-"))
        cycle = str(event.get("cycle", "-"))
        result = str(event.get("result", "-"))
        blockers = int(event.get("blockers", 0))
        steps = event.get("steps", [])
        step_count = len(steps) if isinstance(steps, list) else 0
        lines.append(f"| {timestamp} | {cycle} | {result} | {blockers} | {step_count} |")

    lines.extend(
        [
            "",
            "## Eskalacje (status biezacy)",
            f"- Zrodlo kolejki: {escalation_path.as_posix()}",
            "| Incident | Status | Owner | ETA |",
            "|---|---|---|---|",
        ]
    )

    current_escalations = sorted(
        escalation_values,
        key=lambda item: str(item.get("timestamp_utc", "")),
        reverse=True,
    )[:10]
    if current_escalations:
        for item in current_escalations:
            incident = str(item.get("incident_path", "-"))
            status = str(item.get("status", "-"))
            owner = str(item.get("owner", "-"))
            eta = str(item.get("eta", "-"))
            lines.append(f"| {incident} | {status} | {owner} | {eta} |")
    else:
        lines.append("| - | - | - | - |")

    if current_blockers > 0 or esc_open > 0:
        lines.extend(
            [
                "",
                "## Rekomendacja owner",
                "- Status: Warning",
                "- Wykryto Blocker i/lub otwarte eskalacje; wymagany plan naprawczy z ETA.",
            ]
        )
    else:
        lines.extend(
            [
                "",
                "## Rekomendacja owner",
                "- Status: OK",
                "- Biezace cykle sa zielone; kontynuowac rytm PR/48h/weekly.",
            ]
        )

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate owner weekly summary from cycle logs")
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days for analysis window (default: 7)",
    )
    parser.add_argument(
        "--input",
        default="docs/operations/control_cycle_log.jsonl",
        help="Path to control cycle log JSONL",
    )
    parser.add_argument(
        "--output",
        default="docs/operations/owner_weekly_summary.md",
        help="Path to generated markdown summary",
    )
    parser.add_argument(
        "--escalation-input",
        default="docs/operations/escalation_queue.jsonl",
        help="Path to escalation queue JSONL",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    input_path = (repo_root / args.input).resolve()
    output_path = (repo_root / args.output).resolve()
    escalation_path = (repo_root / args.escalation_input).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now(UTC)
    since = now - timedelta(days=args.days)
    events = _load_events(input_path)
    filtered = [event for event in events if _within_window(event, since)]
    escalation_events = _load_escalations(escalation_path)
    escalation_filtered = [event for event in escalation_events if _within_window(event, since)]

    report = _render(now, filtered, escalation_filtered, output_path, input_path, escalation_path)
    output_path.write_text(report, encoding="utf-8")

    blocker_count = sum(1 for event in filtered if str(event.get("result", "")) == "Blocker")
    esc_open = sum(
        1
        for item in _current_escalation_state(escalation_filtered).values()
        if str(item.get("status", "")) == "open"
    )
    print(
        f"[SUMMARY] cycles={len(filtered)} blockers_history={blocker_count} "
        f"escalation_open={esc_open}"
    )
    print(f"[OUTPUT] {output_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
