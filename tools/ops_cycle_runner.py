#!/usr/bin/env python
"""Run operational control cycles and write audit execution logs."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

try:
    import tools.escalation_notifier as _escalation_notifier_module
except ModuleNotFoundError:
    import escalation_notifier as _fallback_escalation_notifier_module

    _escalation_notifier_module = _fallback_escalation_notifier_module


@dataclass(frozen=True)
class StepResult:
    task_label: str
    exit_code: int
    status: str  # OK | Blocker
    summary: str


def _now_iso() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _run_task(repo_root: Path, task_label: str) -> StepResult:
    command = [
        sys.executable,
        "-m",
        "pip",
        "show",
        "theoretical-md-tools",
    ]

    # This step ensures environment is responsive before running a task command.
    _ = subprocess.run(
        command,
        cwd=repo_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )

    # Task mapping to direct commands, independent from VS Code task host.
    mapping: dict[str, list[str]] = {
        "quality-gates": [sys.executable, "-m", "ruff", "check", "tools", "tests"],
        "quality-gates-offline": [sys.executable, "-m", "ruff", "check", "tools", "tests"],
        "p0-process-check": [sys.executable, "tools/security_sanity_check.py"],
        "process-suite-t04": [
            sys.executable,
            "tools/process_suite_runner.py",
            "--config",
            "Badania/T04-GR-PPN-Yukawa-Perihelion/Process-Suite-T04.json",
            "--output",
            "Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Process-Suite-T04.md",
        ],
        "migration-metrics-report": [sys.executable, "tools/migration_metrics_report.py"],
        "gate-timing-report": [sys.executable, "tools/gate_timing_logger.py", "report"],
    }

    argv = mapping.get(task_label)
    if argv is None:
        return StepResult(task_label, 1, "Blocker", f"Nieznany task: {task_label}")

    cp = subprocess.run(
        argv,
        cwd=repo_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    status = "OK" if cp.returncode == 0 else "Blocker"
    output = f"{cp.stdout}\n{cp.stderr}".strip()
    first_line = output.splitlines()[0] if output else "Brak output"
    return StepResult(task_label, cp.returncode, status, first_line[:220])


def _cycle_definition(cycle: str) -> list[str]:
    if cycle == "pr":
        return ["quality-gates-offline", "p0-process-check"]
    if cycle == "48h":
        return ["p0-process-check", "process-suite-t04", "migration-metrics-report"]
    if cycle == "weekly":
        return [
            "quality-gates-offline",
            "p0-process-check",
            "process-suite-t04",
            "migration-metrics-report",
            "gate-timing-report",
        ]
    raise ValueError(f"Nieobslugiwany cycle: {cycle}")


def _write_log(repo_root: Path, payload: dict[str, object]) -> Path:
    log_path = repo_root / "docs" / "operations" / "control_cycle_log.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, ensure_ascii=True) + "\n")
    return log_path


def _write_blocker_incident(
    repo_root: Path,
    payload: dict[str, object],
    incident_owner: str,
    incident_eta: str,
    incident_impact: str,
) -> Path:
    incidents_dir = repo_root / "docs" / "operations" / "incidents"
    incidents_dir.mkdir(parents=True, exist_ok=True)

    timestamp_raw = str(payload.get("timestamp_utc", _now_iso()))
    safe_ts = (
        timestamp_raw.replace("-", "")
        .replace(":", "")
        .replace("T", "_")
        .replace("Z", "")
    )
    cycle = str(payload.get("cycle", "unknown"))
    incident_path = incidents_dir / f"incident_{safe_ts}_{cycle}.md"

    steps = payload.get("steps", [])
    blocker_steps: list[dict[str, object]] = []
    if isinstance(steps, list):
        for step in steps:
            if isinstance(step, dict) and str(step.get("status", "")) == "Blocker":
                blocker_steps.append(step)

    lines = [
        "# Incident Report (Auto)",
        "",
        "## Metadane",
        f"- Timestamp UTC: {payload.get('timestamp_utc', '-')}",
        f"- Cycle: {payload.get('cycle', '-')}",
        f"- Result: {payload.get('result', '-')}",
        f"- Owner: {incident_owner}",
        f"- ETA: {incident_eta}",
        f"- Impact: {incident_impact}",
        "- Source log: docs/operations/control_cycle_log.jsonl",
        "",
        "## Blocker Details",
    ]

    if blocker_steps:
        for step in blocker_steps:
            lines.append(
                "- Task={task}; Exit={exit_code}; Summary={summary}".format(
                    task=step.get("task", "-"),
                    exit_code=step.get("exit_code", "-"),
                    summary=step.get("summary", "-"),
                )
            )
    else:
        lines.append("- Brak szczegolow kroku Blocker (sprawdz log JSONL).")

    lines.extend(
        [
            "",
            "## Action Plan",
            "- [TBD] Root cause analysis",
            "- [TBD] Mitigation steps",
            "- [TBD] Verification evidence",
            "",
            "## Governance",
            "- fail_closed: tak",
            "- escalation_required: tak",
            "",
        ]
    )

    incident_path.write_text("\n".join(lines), encoding="utf-8")
    return incident_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run operational control cycle")
    parser.add_argument("--cycle", required=True, choices=["pr", "48h", "weekly"])
    parser.add_argument("--owner", default="Orkiestrator")
    parser.add_argument("--note", default="")
    parser.add_argument("--incident-owner", default="Orkiestrator")
    parser.add_argument("--incident-eta", default="TBD")
    parser.add_argument("--incident-impact", default="TBD")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    tasks = _cycle_definition(args.cycle)
    started_at = _now_iso()

    results: list[StepResult] = []
    for task in tasks:
        result = _run_task(repo_root, task)
        results.append(result)
        if result.status == "Blocker":
            break

    blocker_count = sum(1 for item in results if item.status == "Blocker")
    warning_count = 0
    overall = "OK" if blocker_count == 0 else "Blocker"

    payload = {
        "timestamp_utc": _now_iso(),
        "cycle": args.cycle,
        "owner": args.owner,
        "note": args.note,
        "started_at": started_at,
        "finished_at": _now_iso(),
        "result": overall,
        "blockers": blocker_count,
        "warnings": warning_count,
        "steps": [
            {
                "task": item.task_label,
                "status": item.status,
                "exit_code": item.exit_code,
                "summary": item.summary,
            }
            for item in results
        ],
    }

    incident_path: Path | None = None
    escalation_queue_path: Path | None = None
    if blocker_count > 0:
        incident_path = _write_blocker_incident(
            repo_root,
            payload,
            incident_owner=args.incident_owner,
            incident_eta=args.incident_eta,
            incident_impact=args.incident_impact,
        )
        escalation_queue_path = _escalation_notifier_module.write_escalation_event(
            repo_root=repo_root,
            cycle_payload=payload,
            incident_path=incident_path,
            incident_owner=args.incident_owner,
            incident_eta=args.incident_eta,
            incident_impact=args.incident_impact,
        )
        payload["incident_path"] = incident_path.as_posix()
        payload["escalation_queue_path"] = escalation_queue_path.as_posix()
        payload["escalation_status"] = "queued"

    log_path = _write_log(repo_root, payload)
    print(
        f"[SUMMARY] cycle={args.cycle} result={overall} "
        f"steps={len(results)} blockers={blocker_count}"
    )
    print(f"[OUTPUT] {log_path.as_posix()}")
    if incident_path is not None:
        print(f"[INCIDENT] {incident_path.as_posix()}")
    if escalation_queue_path is not None:
        print(f"[ESCALATION] {escalation_queue_path.as_posix()}")
    return 1 if blocker_count > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
