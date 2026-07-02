from __future__ import annotations

import json
from pathlib import Path

from tools.contract_guard import (
    validate_agent_skill_binding,
    validate_backend_catalog,
    validate_capability_catalog,
    validate_contract_file,
    validate_skill_catalog,
    validate_tool_contract_index,
)


def test_validate_contract_file_skill_to_tool_ok() -> None:
    path = Path("mcp/contracts/skill_to_tool.contract.json")
    errors = validate_contract_file(path)
    assert errors == []


def test_validate_capability_catalog_ok() -> None:
    path = Path("mcp/capability_catalog.json")
    errors = validate_capability_catalog(path)
    assert errors == []


def test_validate_capability_catalog_duplicate_id(tmp_path: Path) -> None:
    payload = {
        "version": "1.0.0",
        "capabilities": [
            {
                "capability_id": "CAP-001",
                "name": "A",
                "skills": ["x"],
                "tools": ["tools/a.py"],
            },
            {
                "capability_id": "CAP-001",
                "name": "B",
                "skills": ["y"],
                "tools": ["tools/b.py"],
            },
        ],
    }
    file_path = tmp_path / "capability_catalog.json"
    file_path.write_text(json.dumps(payload), encoding="utf-8")

    errors = validate_capability_catalog(file_path)
    assert any("duplicate capability_id" in err for err in errors)


def test_validate_skill_catalog_ok() -> None:
    path = Path("mcp/skills/skill_catalog.json")
    errors = validate_skill_catalog(path, Path("."))
    assert errors == []


def test_validate_skill_catalog_missing_instruction(tmp_path: Path) -> None:
    payload = {
        "version": "1.0.0",
        "skills": [
            {
                "skill_id": "SK-999",
                "name": "X",
                "owner": "x",
                "status": "active",
                "input": {"required_fields": ["a"]},
                "output": {"required_fields": ["b"]},
                "error": {"required_fields": ["c"]},
                "tool_contracts": ["Tool.X"],
                "tool_implementations": ["tools/contract_guard.py"],
                "instructions": ["Dokumentacja/Instructions/nie_istnieje.md"],
            }
        ],
    }
    file_path = tmp_path / "skill_catalog.json"
    file_path.write_text(json.dumps(payload), encoding="utf-8")

    errors = validate_skill_catalog(file_path, Path("."))
    assert any("instructions missing file" in err for err in errors)


def test_validate_backend_catalog_ok() -> None:
    path = Path("mcp/backends/backend_capabilities.json")
    errors = validate_backend_catalog(path, Path("."))
    assert errors == []


def test_validate_backend_catalog_duplicate_id(tmp_path: Path) -> None:
    payload = {
        "version": "1.0.0",
        "backends": [
            {
                "backend_id": "BE-1",
                "name": "A",
                "status": "active",
                "capabilities": ["symbolic"],
                "tools": ["tools/contract_guard.py"],
                "supports": {
                    "capability_check": True,
                    "execute": True,
                    "validate": True,
                    "export_trace": False,
                },
            },
            {
                "backend_id": "BE-1",
                "name": "B",
                "status": "candidate",
                "capabilities": ["numeric"],
                "tools": [],
                "supports": {
                    "capability_check": False,
                    "execute": False,
                    "validate": False,
                    "export_trace": False,
                },
            },
        ],
    }
    file_path = tmp_path / "backend_capabilities.json"
    file_path.write_text(json.dumps(payload), encoding="utf-8")

    errors = validate_backend_catalog(file_path, Path("."))
    assert any("duplicate backend_id" in err for err in errors)


def test_validate_tool_contract_index_ok() -> None:
    path = Path("mcp/tools/tool_contract_index.json")
    errors = validate_tool_contract_index(path, Path("."))
    assert errors == []


def test_validate_tool_contract_index_missing_file(tmp_path: Path) -> None:
    payload = {
        "version": "1.0.0",
        "contracts": [
            {
                "tool_contract": "Tool.X",
                "implementation": "tools/nie_istnieje.py",
                "criticality": "high",
            }
        ],
    }
    file_path = tmp_path / "tool_contract_index.json"
    file_path.write_text(json.dumps(payload), encoding="utf-8")

    errors = validate_tool_contract_index(file_path, Path("."))
    assert any("implementation missing file" in err for err in errors)


def test_validate_agent_skill_binding_ok() -> None:
    path = Path(".github/agent-skill-binding.json")
    errors = validate_agent_skill_binding(path, Path("."))
    assert errors == []


def test_validate_agent_skill_binding_unknown_skill(tmp_path: Path) -> None:
    agent_file = tmp_path / ".github" / "agents" / "a.agent.md"
    agent_file.parent.mkdir(parents=True, exist_ok=True)
    agent_file.write_text("## Runtime bindings (Architecture 2.1)\n", encoding="utf-8")

    skill_catalog = tmp_path / "mcp" / "skills" / "skill_catalog.json"
    skill_catalog.parent.mkdir(parents=True, exist_ok=True)
    skill_catalog.write_text(
        json.dumps(
            {
                "version": "1.0.0",
                "skills": [{"skill_id": "SK-001"}],
            }
        ),
        encoding="utf-8",
    )

    payload = {
        "version": "1.0.0",
        "bindings": [
            {
                "agent_file": ".github/agents/a.agent.md",
                "agent_name": "a",
                "skill_ids": ["SK-999"],
            }
        ],
    }
    binding_file = tmp_path / ".github" / "agent-skill-binding.json"
    binding_file.write_text(json.dumps(payload), encoding="utf-8")

    errors = validate_agent_skill_binding(binding_file, tmp_path)
    assert any("unknown id" in err for err in errors)