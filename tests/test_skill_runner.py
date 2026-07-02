from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SKILL_RUNNER = Path(__file__).resolve().parents[1] / "tools" / "skill_runner.py"


def _write_skill_catalog(path: Path, tool_path: str, status: str = "active") -> None:
    payload = {
        "version": "1.0.0",
        "skills": [
            {
                "skill_id": "SK-T01",
                "name": "Test Skill",
                "owner": "technical-developer",
                "status": status,
                "input": {"required_fields": ["x"]},
                "output": {"required_fields": ["status"]},
                "error": {"required_fields": ["code"]},
                "tool_contracts": ["Tool.Test"],
                "tool_implementations": [tool_path],
                "instructions": ["Dokumentacja/Instructions/reporting.instructions.md"],
            }
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def _write_test_tool(path: Path, exit_code: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "import sys\n"
        f"raise SystemExit({exit_code})\n",
        encoding="utf-8",
    )


def test_skill_runner_list_and_plan(tmp_path: Path) -> None:
    tool_path = tmp_path / "tools" / "test_tool.py"
    _write_test_tool(tool_path, 0)

    instructions_path = tmp_path / "Dokumentacja" / "Instructions" / "reporting.instructions.md"
    instructions_path.parent.mkdir(parents=True, exist_ok=True)
    instructions_path.write_text("x\n", encoding="utf-8")

    catalog_path = tmp_path / "mcp" / "skills" / "skill_catalog.json"
    _write_skill_catalog(catalog_path, "tools/test_tool.py")

    cmd_list = [
        sys.executable,
        str(SKILL_RUNNER),
        "--catalog",
        "mcp/skills/skill_catalog.json",
        "list",
    ]
    cp_list = subprocess.run(cmd_list, cwd=tmp_path, capture_output=True, text=True, check=False)
    assert cp_list.returncode == 0
    assert "SK-T01" in cp_list.stdout

    cmd_plan = [
        sys.executable,
        str(SKILL_RUNNER),
        "--catalog",
        "mcp/skills/skill_catalog.json",
        "plan",
        "--skill-id",
        "SK-T01",
    ]
    cp_plan = subprocess.run(cmd_plan, cwd=tmp_path, capture_output=True, text=True, check=False)
    assert cp_plan.returncode == 0
    assert "tools/test_tool.py" in cp_plan.stdout


def test_skill_runner_run_dry_run_ok(tmp_path: Path) -> None:
    tool_path = tmp_path / "tools" / "test_tool.py"
    _write_test_tool(tool_path, 1)

    instructions_path = tmp_path / "Dokumentacja" / "Instructions" / "reporting.instructions.md"
    instructions_path.parent.mkdir(parents=True, exist_ok=True)
    instructions_path.write_text("x\n", encoding="utf-8")

    catalog_path = tmp_path / "mcp" / "skills" / "skill_catalog.json"
    _write_skill_catalog(catalog_path, "tools/test_tool.py")

    cmd = [
        sys.executable,
        str(SKILL_RUNNER),
        "--catalog",
        "mcp/skills/skill_catalog.json",
        "run",
        "--skill-id",
        "SK-T01",
        "--dry-run",
    ]
    cp = subprocess.run(cmd, cwd=tmp_path, capture_output=True, text=True, check=False)
    assert cp.returncode == 0
    assert '"status": "OK"' in cp.stdout


def test_skill_runner_candidate_fail_closed(tmp_path: Path) -> None:
    tool_path = tmp_path / "tools" / "test_tool.py"
    _write_test_tool(tool_path, 0)

    instructions_path = tmp_path / "Dokumentacja" / "Instructions" / "reporting.instructions.md"
    instructions_path.parent.mkdir(parents=True, exist_ok=True)
    instructions_path.write_text("x\n", encoding="utf-8")

    catalog_path = tmp_path / "mcp" / "skills" / "skill_catalog.json"
    _write_skill_catalog(catalog_path, "tools/test_tool.py", status="candidate")

    cmd = [
        sys.executable,
        str(SKILL_RUNNER),
        "--catalog",
        "mcp/skills/skill_catalog.json",
        "run",
        "--skill-id",
        "SK-T01",
    ]
    cp = subprocess.run(cmd, cwd=tmp_path, capture_output=True, text=True, check=False)
    assert cp.returncode == 1
    assert '"status": "Blocker"' in cp.stdout
