#!/usr/bin/env python
"""Run configured process checks and build a single markdown status report."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class CheckResult:
    check_id: str
    name: str
    command: str
    exit_code: int
    status: str  # OK | Warning | Blocker
    summary: str


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _classify(exit_code: int, output: str) -> tuple[str, str]:
    text = output or ""
    upper = text.upper()

    if "[BLOCKER]" in upper:
        return "Blocker", "Wykryto krytyczne braki procesowe."
    if "[WARNING]" in upper or "[WARN]" in upper:
        return "Warning", "Wykryto niekrytyczne braki lub otwarte pozycje."
    if "[FAIL]" in upper or exit_code != 0:
        return "Blocker", "Krok zakonczyl sie bledem wykonania lub testu."
    return "OK", "Brak sygnalow ostrzegawczych w kroku."


def _run_check(repo_root: Path, check: dict[str, Any]) -> CheckResult:
    check_id = str(check.get("id", "-")).strip() or "-"
    name = str(check.get("name", check_id)).strip() or check_id
    argv = check.get("argv", [])
    if not isinstance(argv, list) or not argv:
        return CheckResult(check_id, name, "<invalid>", 1, "Blocker", "Brak poprawnego argv.")

    resolved_argv = [str(item) for item in argv]

    cmd: list[str]
    first = resolved_argv[0]
    if first.endswith(".py"):
        script_path = (repo_root / first).resolve()
        cmd = [sys.executable, str(script_path)] + resolved_argv[1:]
    else:
        cmd = resolved_argv

    try:
        cp = subprocess.run(
            cmd,
            cwd=repo_root,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        output = (cp.stdout or "") + "\n" + (cp.stderr or "")
        status, summary = _classify(cp.returncode, output)
        return CheckResult(
            check_id=check_id,
            name=name,
            command=" ".join(cmd),
            exit_code=cp.returncode,
            status=status,
            summary=summary,
        )
    except OSError as exc:
        return CheckResult(check_id, name, " ".join(cmd), 1, "Blocker", f"Blad uruchomienia: {exc}")


def _render_report(case_id: str, config_path: Path, results: list[CheckResult]) -> str:
    ts = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    ok_count = sum(1 for r in results if r.status == "OK")
    warning_count = sum(1 for r in results if r.status == "Warning")
    blocker_count = sum(1 for r in results if r.status == "Blocker")

    lines = [
        "# Raport process suite (TD-P1..TD-P7)",
        "",
        "## Metadane",
        f"- Case: {case_id}",
        f"- Data: {ts}",
        f"- Konfiguracja: {config_path.as_posix()}",
        f"- Podsumowanie: OK={ok_count}, Warning={warning_count}, Blocker={blocker_count}",
        "",
        "## Wyniki krokow",
        "| ID | Krok | Status | Exit code | Podsumowanie |",
        "|---|---|---|---:|---|",
    ]

    for r in results:
        lines.append(f"| {r.check_id} | {r.name} | {r.status} | {r.exit_code} | {r.summary} |")

    lines.extend(
        [
            "",
            "## Uwagi",
            "- Raport ma charakter procesowy i nie zmienia tresci merytorycznej badan.",
            "- Decyzje gate 1/2/4 pozostaja w trybie HITL.",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run process suite checks from JSON config")
    parser.add_argument("--config", required=True, help="Path to process suite config JSON")
    parser.add_argument("--output", required=True, help="Output markdown report path")
    parser.add_argument(
        "--fail-on-blocker",
        action="store_true",
        help="Exit 1 when at least one check is Blocker",
    )
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    output_path = Path(args.output).resolve()

    if not config_path.exists():
        print(f"[FAIL] config not found: {config_path}")
        return 1

    try:
        cfg = _load_json(config_path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[FAIL] cannot load config: {exc}")
        return 1

    case_id = str(cfg.get("case_id", "-")).strip() or "-"
    checks = cfg.get("checks", [])
    if not isinstance(checks, list) or not checks:
        print("[FAIL] no checks configured")
        return 1

    repo_root = config_path.parents[2]
    results = [_run_check(repo_root, check) for check in checks]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(_render_report(case_id, config_path, results), encoding="utf-8")

    for result in results:
        print(f"[{result.status}] {result.check_id} {result.name} (exit={result.exit_code})")

    blockers = sum(1 for r in results if r.status == "Blocker")
    print(f"[SUMMARY] blockers={blockers} total={len(results)}")

    if blockers and args.fail_on_blocker:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
