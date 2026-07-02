#!/usr/bin/env python
"""Generate a periodic Architecture 2.0 migration metrics report."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class MetricRow:
    metric_id: str
    name: str
    value: str
    target: str
    status: str  # OK | Warning | Blocker
    evidence: str
    notes: str


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _format_ratio(numerator: int, denominator: int) -> str:
    if denominator <= 0:
        return "0.00%"
    return f"{(100.0 * numerator / denominator):.2f}%"


def _metric_capability_skill_coverage(repo_root: Path) -> MetricRow:
    catalog_path = repo_root / "mcp" / "capability_catalog.json"
    try:
        catalog = _load_json(catalog_path)
    except (OSError, json.JSONDecodeError) as exc:
        return MetricRow(
            metric_id="MM-001",
            name="Coverage capability->skill mapping",
            value="Nie wiem",
            target=">= 100.00%",
            status="Blocker",
            evidence=catalog_path.as_posix(),
            notes=f"Blad odczytu katalogu capability: {exc}",
        )

    capabilities = catalog.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        return MetricRow(
            metric_id="MM-001",
            name="Coverage capability->skill mapping",
            value="0.00%",
            target=">= 100.00%",
            status="Blocker",
            evidence=catalog_path.as_posix(),
            notes="Brak capability w katalogu.",
        )

    mapped = 0
    for item in capabilities:
        skills = item.get("skills") if isinstance(item, dict) else None
        if isinstance(skills, list) and len(skills) > 0:
            mapped += 1

    value = _format_ratio(mapped, len(capabilities))
    status = "OK" if mapped == len(capabilities) else "Warning"
    return MetricRow(
        metric_id="MM-001",
        name="Coverage capability->skill mapping",
        value=value,
        target=">= 100.00%",
        status=status,
        evidence=catalog_path.as_posix(),
        notes=f"Mapped {mapped}/{len(capabilities)} capability.",
    )


def _metric_skill_tool_tests(repo_root: Path) -> MetricRow:
    contract_path = repo_root / "mcp" / "contracts" / "skill_to_tool.contract.json"
    test_path = repo_root / "tests" / "test_contract_guard.py"

    contract_exists = contract_path.exists()
    test_exists = test_path.exists()
    test_has_coverage = False

    if test_exists:
        content = test_path.read_text(encoding="utf-8")
        test_has_coverage = "skill_to_tool.contract.json" in content

    checks = [contract_exists, test_exists, test_has_coverage]
    passed = sum(1 for check in checks if check)
    value = _format_ratio(passed, len(checks))
    status = "OK" if passed == len(checks) else "Warning"

    notes = []
    if not contract_exists:
        notes.append("Brak skill_to_tool.contract.json")
    if not test_exists:
        notes.append("Brak tests/test_contract_guard.py")
    if test_exists and not test_has_coverage:
        notes.append("Brak asercji pokrywajacej skill_to_tool kontrakt")

    return MetricRow(
        metric_id="MM-002",
        name="Coverage skill->tool contract tests",
        value=value,
        target=">= 100.00%",
        status=status,
        evidence=f"{contract_path.as_posix()} + {test_path.as_posix()}",
        notes="; ".join(notes) if notes else "Pokrycie kontraktu i testu potwierdzone.",
    )


def _metric_fail_closed_coverage(repo_root: Path) -> MetricRow:
    contract_path = repo_root / "mcp" / "contracts" / "skill_to_tool.contract.json"
    tasks_path = repo_root / ".vscode" / "tasks.json"

    invariant_stop_flow = False
    invariant_escalation = False
    guard_task_present = False

    try:
        contract = _load_json(contract_path)
        invariants = contract.get("invariants", [])
        if isinstance(invariants, list):
            invariant_stop_flow = any("stop_flow == true" in str(item) for item in invariants)
            invariant_escalation = any("escalation_target" in str(item) for item in invariants)
    except (OSError, json.JSONDecodeError):
        pass

    try:
        tasks = _load_json(tasks_path)
        entries = tasks.get("tasks", [])
        if isinstance(entries, list):
            for entry in entries:
                if not isinstance(entry, dict):
                    continue
                label = str(entry.get("label", ""))
                args = entry.get("args", [])
                if label == "stage-f-contract-guard" and isinstance(args, list):
                    guard_task_present = "tools/contract_guard.py" in [str(arg) for arg in args]
                    break
    except (OSError, json.JSONDecodeError):
        pass

    checks = [invariant_stop_flow, invariant_escalation, guard_task_present]
    passed = sum(1 for check in checks if check)
    value = _format_ratio(passed, len(checks))
    status = "OK" if passed == len(checks) else "Warning"

    notes = []
    if not invariant_stop_flow:
        notes.append("Brak invariantu stop_flow dla Blocker")
    if not invariant_escalation:
        notes.append("Brak invariantu escalation_target dla Blocker")
    if not guard_task_present:
        notes.append("Brak taska stage-f-contract-guard")

    return MetricRow(
        metric_id="MM-003",
        name="Coverage fail-closed trigger tests",
        value=value,
        target=">= 100.00%",
        status=status,
        evidence=f"{contract_path.as_posix()} + {tasks_path.as_posix()}",
        notes="; ".join(notes) if notes else "Fail-closed coverage potwierdzone.",
    )


def _metric_invariant_violations(repo_root: Path) -> MetricRow:
    command = [sys.executable, str(repo_root / "tools" / "contract_guard.py")]
    try:
        cp = subprocess.run(
            command,
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError as exc:
        return MetricRow(
            metric_id="MM-004",
            name="Liczba naruszen invariantow na iteracje",
            value="Nie wiem",
            target="0",
            status="Blocker",
            evidence="tools/contract_guard.py",
            notes=f"Blad uruchomienia contract_guard: {exc}",
        )

    output = f"{cp.stdout}\n{cp.stderr}"
    match = re.search(r"\[SUMMARY\]\s+blockers=(\d+)", output)
    if not match:
        return MetricRow(
            metric_id="MM-004",
            name="Liczba naruszen invariantow na iteracje",
            value="Nie wiem",
            target="0",
            status="Warning",
            evidence="tools/contract_guard.py",
            notes="Nie znaleziono podsumowania blockers w output contract_guard.",
        )

    blockers = int(match.group(1))
    status = "OK" if blockers == 0 else "Blocker"
    return MetricRow(
        metric_id="MM-004",
        name="Liczba naruszen invariantow na iteracje",
        value=str(blockers),
        target="0",
        status=status,
        evidence="tools/contract_guard.py [SUMMARY]",
        notes="Wartosc pochodzi z automatycznej walidacji kontraktow.",
    )


def _metric_gate_cycle_time() -> MetricRow:
    repo_root = Path(__file__).resolve().parents[1]
    log_path = repo_root / "docs" / "operations" / "gate_timing_log.jsonl"

    if not log_path.exists():
        return MetricRow(
            metric_id="MM-005",
            name="Czas przejscia case przez Gate 1-3",
            value="Nie wiem",
            target="<= 72h median (G1-G3)",
            status="Warning",
            evidence=log_path.as_posix(),
            notes="Brak logu telemetrycznego Gate timing. Dodaj eventy start/end dla G1-G3.",
        )

    events: list[dict[str, str]] = []
    try:
        for line in log_path.read_text(encoding="utf-8").splitlines():
            payload = json.loads(line)
            if isinstance(payload, dict):
                events.append({str(k): str(v) for k, v in payload.items()})
    except (OSError, json.JSONDecodeError) as exc:
        return MetricRow(
            metric_id="MM-005",
            name="Czas przejscia case przez Gate 1-3",
            value="Nie wiem",
            target="<= 72h median (G1-G3)",
            status="Warning",
            evidence=log_path.as_posix(),
            notes=f"Blad odczytu logu telemetrycznego: {exc}",
        )

    def parse_ts(raw: str) -> datetime | None:
        try:
            return datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except ValueError:
            return None

    by_case: dict[str, dict[str, datetime]] = {}
    for event in events:
        case_id = event.get("case_id", "")
        gate_id = event.get("gate_id", "")
        action = event.get("action", "")
        ts = parse_ts(event.get("timestamp_utc", ""))
        if not case_id or gate_id not in {"G1", "G3"} or action != "end" or ts is None:
            continue

        state = by_case.setdefault(case_id, {})
        existing = state.get(gate_id)
        if existing is None or ts > existing:
            state[gate_id] = ts

    durations_h: list[float] = []
    for _, state in by_case.items():
        g1_end = state.get("G1")
        g3_end = state.get("G3")
        if g1_end is None or g3_end is None:
            continue
        duration = (g3_end - g1_end).total_seconds() / 3600.0
        if duration >= 0:
            durations_h.append(duration)

    if not durations_h:
        return MetricRow(
            metric_id="MM-005",
            name="Czas przejscia case przez Gate 1-3",
            value="Nie wiem",
            target="<= 72h median (G1-G3)",
            status="Warning",
            evidence=log_path.as_posix(),
            notes="Brak par pomiarowych G1-end i G3-end w tym samym case.",
        )

    durations_h.sort()
    mid = len(durations_h) // 2
    if len(durations_h) % 2 == 1:
        median_h = durations_h[mid]
    else:
        median_h = (durations_h[mid - 1] + durations_h[mid]) / 2.0

    status = "OK" if median_h <= 72.0 else "Warning"
    return MetricRow(
        metric_id="MM-005",
        name="Czas przejscia case przez Gate 1-3",
        value=f"{median_h:.2f}h",
        target="<= 72h median (G1-G3)",
        status=status,
        evidence=log_path.as_posix(),
        notes=f"Pomiary case: {len(durations_h)} (mediana czasu od G1-end do G3-end).",
    )


def _render_report(rows: list[MetricRow], generated_at: str) -> str:
    ok_count = sum(1 for row in rows if row.status == "OK")
    warning_count = sum(1 for row in rows if row.status == "Warning")
    blocker_count = sum(1 for row in rows if row.status == "Blocker")

    lines = [
        "# SAF/LTR Migration Metrics Report",
        "",
        "## Metadane",
        f"- Data raportu: {generated_at}",
        "- Zakres: Architecture 2.0 migration (Etap F i stabilizacja)",
        f"- Podsumowanie: OK={ok_count}, Warning={warning_count}, Blocker={blocker_count}",
        "",
        "## Tabela metryk",
        "| ID | Metryka | Wartosc | Cel | Status | Dowod | Uwagi |",
        "|---|---|---|---|---|---|---|",
    ]

    for row in rows:
        lines.append(
            "| "
            f"{row.metric_id} | {row.name} | {row.value} | {row.target} | {row.status} | "
            f"{row.evidence} | {row.notes} |"
        )

    unresolved = [row for row in rows if row.value == "Nie wiem"]
    if unresolved:
        lines.extend(
            [
                "",
                "## Miejsca do doprecyzowania",
            ]
        )
        for row in unresolved:
            lines.append(f"- Nie wiem: metryka {row.metric_id} wymaga doprecyzowania danych.")

        lines.extend(
            [
                "",
                "## Pytania uzupelniajace",
            ]
        )
        for row in unresolved:
            lines.append(
                f"- Q-{row.metric_id[-3:]} (wysoki): Jakie jest "
                f"kanoniczne zrodlo danych dla {row.metric_id}?"
            )

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate SAF/LTR migration metrics report")
    parser.add_argument(
        "--output",
        default="Dokumentacja/Architecture-2.0/SAF-LTR-Migration-Metrics-Report.md",
        help="Output markdown report path",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    output_path = (repo_root / args.output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows = [
        _metric_capability_skill_coverage(repo_root),
        _metric_skill_tool_tests(repo_root),
        _metric_fail_closed_coverage(repo_root),
        _metric_invariant_violations(repo_root),
        _metric_gate_cycle_time(),
    ]

    generated_at = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    output_path.write_text(_render_report(rows, generated_at), encoding="utf-8")

    blocker_count = sum(1 for row in rows if row.status == "Blocker")
    warning_count = sum(1 for row in rows if row.status == "Warning")
    ok_count = len(rows) - warning_count - blocker_count
    print(f"[SUMMARY] OK={ok_count} Warning={warning_count} Blocker={blocker_count}")
    print(f"[OUTPUT] {output_path.as_posix()}")

    return 1 if blocker_count > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
