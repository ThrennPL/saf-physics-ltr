#!/usr/bin/env python
"""Run skill chains based on machine-readable skill catalog."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ToolRunResult:
    tool_path: str
    command: list[str]
    exit_code: int
    status: str  # OK | Blocker
    summary: str


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_skill_catalog(repo_root: Path, catalog_rel_path: str) -> dict[str, Any]:
    path = (repo_root / catalog_rel_path).resolve()
    return _load_json(path)


def _find_skill(catalog: dict[str, Any], skill_id: str) -> dict[str, Any] | None:
    skills = catalog.get("skills")
    if not isinstance(skills, list):
        return None
    for skill in skills:
        if isinstance(skill, dict) and str(skill.get("skill_id", "")).strip() == skill_id:
            return skill
    return None


def _load_tool_args_map(repo_root: Path, args_file: str | None) -> dict[str, list[str]]:
    if not args_file:
        return {}

    path = (repo_root / args_file).resolve()
    payload = _load_json(path)
    if not isinstance(payload, dict):
        raise ValueError("tool-args-file must contain a JSON object")

    normalized: dict[str, list[str]] = {}
    for key, value in payload.items():
        if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
            raise ValueError(f"tool args for {key} must be an array of strings")
        normalized[str(key)] = [str(item) for item in value]
    return normalized


def _run_single_tool(
    repo_root: Path,
    tool_path: str,
    tool_args: list[str],
    dry_run: bool,
) -> ToolRunResult:
    script = (repo_root / tool_path).resolve()
    command = [sys.executable, str(script), *tool_args]

    if not script.is_file():
        return ToolRunResult(tool_path, command, 1, "Blocker", "Brak pliku narzedzia")

    if dry_run:
        return ToolRunResult(tool_path, command, 0, "OK", "Dry-run: command prepared")

    cp = subprocess.run(
        command,
        cwd=repo_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if cp.returncode == 0:
        return ToolRunResult(tool_path, command, 0, "OK", "Tool completed successfully")
    return ToolRunResult(tool_path, command, cp.returncode, "Blocker", "Tool execution failed")


def _run_skill(
    repo_root: Path,
    skill: dict[str, Any],
    tool_args_map: dict[str, list[str]],
    dry_run: bool,
    allow_candidate: bool,
) -> tuple[dict[str, Any], int]:
    skill_id = str(skill.get("skill_id", "-")).strip() or "-"
    skill_name = str(skill.get("name", skill_id)).strip() or skill_id
    skill_status = str(skill.get("status", "candidate")).strip() or "candidate"

    if skill_status == "candidate" and not allow_candidate:
        payload = {
            "skill_id": skill_id,
            "name": skill_name,
            "status": "Blocker",
            "summary": "Skill ma status candidate; uruchomienie zablokowane (fail-closed).",
            "confidence": 0.0,
            "questions": ["Q-001: Potwierdz uruchomienie candidate skill (--allow-candidate)."],
            "tool_results": [],
        }
        return payload, 1

    tools = skill.get("tool_implementations", [])
    if not isinstance(tools, list) or not tools:
        payload = {
            "skill_id": skill_id,
            "name": skill_name,
            "status": "Blocker",
            "summary": "Brak tool_implementations dla skill.",
            "confidence": 0.0,
            "questions": ["Q-002: Uzupelnij tool_implementations w skill catalog."],
            "tool_results": [],
        }
        return payload, 1

    results: list[ToolRunResult] = []
    blocked = False
    for tool_path_raw in tools:
        tool_path = str(tool_path_raw)
        tool_args = tool_args_map.get(tool_path, [])
        result = _run_single_tool(repo_root, tool_path, tool_args, dry_run)
        results.append(result)
        if result.status == "Blocker":
            blocked = True
            break

    summary = (
        "Skill chain zatrzymany na Blocker."
        if blocked
        else "Skill chain wykonany poprawnie."
    )
    questions = []
    if blocked:
        questions = ["Q-003: Napraw narzedzie z pierwszym statusem Blocker."]

    payload = {
        "skill_id": skill_id,
        "name": skill_name,
        "status": "Blocker" if blocked else "OK",
        "summary": summary,
        "confidence": 0.4 if blocked else 0.95,
        "questions": questions,
        "tool_results": [
            {
                "tool_path": item.tool_path,
                "status": item.status,
                "exit_code": item.exit_code,
                "summary": item.summary,
                "command": item.command,
            }
            for item in results
        ],
    }
    return payload, 1 if blocked else 0


def _cmd_list(catalog: dict[str, Any]) -> int:
    skills = catalog.get("skills", [])
    if not isinstance(skills, list) or not skills:
        print("[FAIL] no skills in catalog")
        return 1
    for skill in skills:
        if not isinstance(skill, dict):
            continue
        print(
            f"{skill.get('skill_id', '-')} | {skill.get('name', '-')} | "
            f"owner={skill.get('owner', '-')} | status={skill.get('status', '-') }"
        )
    return 0


def _cmd_plan(skill: dict[str, Any]) -> int:
    tools = skill.get("tool_implementations", [])
    if not isinstance(tools, list):
        print("[FAIL] invalid tool_implementations")
        return 1

    print(f"Skill: {skill.get('skill_id', '-') } {skill.get('name', '-')}")
    print(f"Status: {skill.get('status', '-')}")
    print("Tool chain:")
    for idx, tool in enumerate(tools, start=1):
        print(f"  {idx}. {tool}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run skill chain from mcp skill catalog")
    parser.add_argument(
        "--catalog",
        default="mcp/skills/skill_catalog.json",
        help="Relative path to skill catalog JSON",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="List skills from catalog")

    plan_parser = subparsers.add_parser("plan", help="Show tool chain for selected skill")
    plan_parser.add_argument("--skill-id", required=True, help="Skill ID, e.g. SK-007")

    run_parser = subparsers.add_parser("run", help="Run selected skill chain")
    run_parser.add_argument("--skill-id", required=True, help="Skill ID, e.g. SK-007")
    run_parser.add_argument(
        "--tool-args-file",
        default=None,
        help="Optional JSON map: {\"tools/script.py\": [\"--arg\", \"value\"]}",
    )
    run_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not execute tools; only build commands and validate flow",
    )
    run_parser.add_argument(
        "--allow-candidate",
        action="store_true",
        help="Allow running skills with status=candidate",
    )
    run_parser.add_argument(
        "--output",
        default=None,
        help="Optional output path for JSON execution report",
    )

    args = parser.parse_args()
    repo_root = Path(".").resolve()

    try:
        catalog = _load_skill_catalog(repo_root, args.catalog)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[FAIL] cannot load catalog: {exc}")
        return 1

    if args.command == "list":
        return _cmd_list(catalog)

    skill = _find_skill(catalog, args.skill_id)
    if not skill:
        print(f"[FAIL] skill not found: {args.skill_id}")
        return 1

    if args.command == "plan":
        return _cmd_plan(skill)

    try:
        tool_args_map = _load_tool_args_map(repo_root, args.tool_args_file)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"[FAIL] invalid tool args map: {exc}")
        return 1

    payload, exit_code = _run_skill(
        repo_root=repo_root,
        skill=skill,
        tool_args_map=tool_args_map,
        dry_run=bool(args.dry_run),
        allow_candidate=bool(args.allow_candidate),
    )

    text = json.dumps(payload, ensure_ascii=True, indent=2)
    print(text)

    if args.output:
        output_path = (repo_root / str(args.output)).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(text + "\n", encoding="utf-8")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
