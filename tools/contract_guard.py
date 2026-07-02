#!/usr/bin/env python
"""Validate Stage F contract artifacts and fail-closed invariants."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _ensure_required_keys(payload: dict[str, Any], keys: list[str], scope: str) -> list[str]:
    errors: list[str] = []
    for key in keys:
        if key not in payload:
            errors.append(f"missing key in {scope}: {key}")
    return errors


def validate_contract_file(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = _load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read {path.as_posix()}: {exc}"]

    errors.extend(
        _ensure_required_keys(
            data,
            ["contract_id", "version", "request", "response"],
            "root",
        )
    )

    request = data.get("request")
    if not isinstance(request, dict):
        errors.append("request must be an object")
    else:
        req_fields = request.get("required_fields")
        if not isinstance(req_fields, list) or not req_fields:
            errors.append("request.required_fields must be a non-empty array")

    response = data.get("response")
    if not isinstance(response, dict):
        errors.append("response must be an object")
    else:
        resp_fields = response.get("required_fields")
        if not isinstance(resp_fields, list) or not resp_fields:
            errors.append("response.required_fields must be a non-empty array")

    contract_id = str(data.get("contract_id", ""))
    if contract_id == "skill_to_tool.v1" and isinstance(response, dict):
        allowed = response.get("allowed_working_status")
        if allowed != ["OK", "Warning", "Blocker"]:
            errors.append("skill_to_tool.v1 requires allowed_working_status=[OK, Warning, Blocker]")

    invariants = data.get("invariants")
    if not isinstance(invariants, list) or not invariants:
        errors.append("invariants must be a non-empty array")

    return errors


def validate_capability_catalog(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = _load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read {path.as_posix()}: {exc}"]

    errors.extend(_ensure_required_keys(data, ["version", "capabilities"], "catalog"))
    capabilities = data.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        return errors + ["capabilities must be a non-empty array"]

    seen: set[str] = set()
    for index, capability in enumerate(capabilities, start=1):
        scope = f"capabilities[{index}]"
        if not isinstance(capability, dict):
            errors.append(f"{scope} must be an object")
            continue

        errors.extend(
            _ensure_required_keys(capability, ["capability_id", "name", "skills", "tools"], scope)
        )

        capability_id = str(capability.get("capability_id", "")).strip()
        if not capability_id:
            errors.append(f"{scope}.capability_id cannot be empty")
        elif capability_id in seen:
            errors.append(f"duplicate capability_id: {capability_id}")
        else:
            seen.add(capability_id)

        skills = capability.get("skills")
        if not isinstance(skills, list) or not skills:
            errors.append(f"{scope}.skills must be a non-empty array")

        tools = capability.get("tools")
        if not isinstance(tools, list) or not tools:
            errors.append(f"{scope}.tools must be a non-empty array")

    return errors


def validate_skill_catalog(path: Path, repo_root: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = _load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read {path.as_posix()}: {exc}"]

    errors.extend(_ensure_required_keys(data, ["version", "skills"], "skill_catalog"))
    skills = data.get("skills")
    if not isinstance(skills, list) or not skills:
        return errors + ["skills must be a non-empty array"]

    seen: set[str] = set()
    valid_status = {"active", "candidate"}
    for index, skill in enumerate(skills, start=1):
        scope = f"skills[{index}]"
        if not isinstance(skill, dict):
            errors.append(f"{scope} must be an object")
            continue

        errors.extend(
            _ensure_required_keys(
                skill,
                [
                    "skill_id",
                    "name",
                    "owner",
                    "status",
                    "input",
                    "output",
                    "error",
                    "tool_contracts",
                    "tool_implementations",
                    "instructions",
                ],
                scope,
            )
        )

        skill_id = str(skill.get("skill_id", "")).strip()
        if not skill_id:
            errors.append(f"{scope}.skill_id cannot be empty")
        elif skill_id in seen:
            errors.append(f"duplicate skill_id: {skill_id}")
        else:
            seen.add(skill_id)

        status = str(skill.get("status", "")).strip()
        if status not in valid_status:
            errors.append(f"{scope}.status must be one of {sorted(valid_status)}")

        for block_key in ["input", "output", "error"]:
            block = skill.get(block_key)
            if not isinstance(block, dict):
                errors.append(f"{scope}.{block_key} must be an object")
                continue
            required = block.get("required_fields")
            if not isinstance(required, list) or not required:
                errors.append(f"{scope}.{block_key}.required_fields must be a non-empty array")

        for list_key in ["tool_contracts", "tool_implementations", "instructions"]:
            values = skill.get(list_key)
            if not isinstance(values, list) or not values:
                errors.append(f"{scope}.{list_key} must be a non-empty array")

        for rel_path in skill.get("tool_implementations", []):
            tool_path = repo_root / str(rel_path)
            if not tool_path.is_file():
                errors.append(f"{scope}.tool_implementations missing file: {rel_path}")

        for rel_path in skill.get("instructions", []):
            instruction_path = repo_root / str(rel_path)
            if not instruction_path.is_file():
                errors.append(f"{scope}.instructions missing file: {rel_path}")

    return errors


def validate_backend_catalog(path: Path, repo_root: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = _load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read {path.as_posix()}: {exc}"]

    errors.extend(_ensure_required_keys(data, ["version", "backends"], "backend_catalog"))
    backends = data.get("backends")
    if not isinstance(backends, list) or not backends:
        return errors + ["backends must be a non-empty array"]

    seen: set[str] = set()
    valid_status = {"active", "candidate"}
    for index, backend in enumerate(backends, start=1):
        scope = f"backends[{index}]"
        if not isinstance(backend, dict):
            errors.append(f"{scope} must be an object")
            continue

        errors.extend(
            _ensure_required_keys(
                backend,
                ["backend_id", "name", "status", "capabilities", "tools", "supports"],
                scope,
            )
        )

        backend_id = str(backend.get("backend_id", "")).strip()
        if not backend_id:
            errors.append(f"{scope}.backend_id cannot be empty")
        elif backend_id in seen:
            errors.append(f"duplicate backend_id: {backend_id}")
        else:
            seen.add(backend_id)

        status = str(backend.get("status", "")).strip()
        if status not in valid_status:
            errors.append(f"{scope}.status must be one of {sorted(valid_status)}")

        capabilities = backend.get("capabilities")
        if not isinstance(capabilities, list) or not capabilities:
            errors.append(f"{scope}.capabilities must be a non-empty array")

        tools = backend.get("tools")
        if not isinstance(tools, list):
            errors.append(f"{scope}.tools must be an array")
        else:
            for rel_path in tools:
                tool_path = repo_root / str(rel_path)
                if not tool_path.is_file():
                    errors.append(f"{scope}.tools missing file: {rel_path}")

        supports = backend.get("supports")
        if not isinstance(supports, dict):
            errors.append(f"{scope}.supports must be an object")
        else:
            for method_name in ["capability_check", "execute", "validate", "export_trace"]:
                if not isinstance(supports.get(method_name), bool):
                    errors.append(f"{scope}.supports.{method_name} must be boolean")

    return errors


def validate_tool_contract_index(path: Path, repo_root: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = _load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read {path.as_posix()}: {exc}"]

    errors.extend(_ensure_required_keys(data, ["version", "contracts"], "tool_contract_index"))
    contracts = data.get("contracts")
    if not isinstance(contracts, list) or not contracts:
        return errors + ["contracts must be a non-empty array"]

    seen: set[str] = set()
    valid_criticality = {"high", "medium", "low"}
    for index, contract in enumerate(contracts, start=1):
        scope = f"contracts[{index}]"
        if not isinstance(contract, dict):
            errors.append(f"{scope} must be an object")
            continue

        errors.extend(
            _ensure_required_keys(
                contract,
                ["tool_contract", "implementation", "criticality"],
                scope,
            )
        )

        tool_contract = str(contract.get("tool_contract", "")).strip()
        if not tool_contract:
            errors.append(f"{scope}.tool_contract cannot be empty")
        elif tool_contract in seen:
            errors.append(f"duplicate tool_contract: {tool_contract}")
        else:
            seen.add(tool_contract)

        criticality = str(contract.get("criticality", "")).strip()
        if criticality not in valid_criticality:
            errors.append(f"{scope}.criticality must be one of {sorted(valid_criticality)}")

        rel_path = str(contract.get("implementation", "")).strip()
        implementation_path = repo_root / rel_path
        if not implementation_path.is_file():
            errors.append(f"{scope}.implementation missing file: {rel_path}")

    return errors


def validate_agent_skill_binding(path: Path, repo_root: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = _load_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read {path.as_posix()}: {exc}"]

    errors.extend(_ensure_required_keys(data, ["version", "bindings"], "agent_skill_binding"))
    bindings = data.get("bindings")
    if not isinstance(bindings, list) or not bindings:
        return errors + ["bindings must be a non-empty array"]

    skill_catalog = repo_root / "mcp" / "skills" / "skill_catalog.json"
    skill_catalog_data = _load_json(skill_catalog)
    skills = skill_catalog_data.get("skills", [])
    skill_ids: set[str] = {
        str(item.get("skill_id", "")).strip()
        for item in skills
        if isinstance(item, dict) and str(item.get("skill_id", "")).strip()
    }

    seen_files: set[str] = set()
    seen_names: set[str] = set()
    for index, binding in enumerate(bindings, start=1):
        scope = f"bindings[{index}]"
        if not isinstance(binding, dict):
            errors.append(f"{scope} must be an object")
            continue

        errors.extend(
            _ensure_required_keys(binding, ["agent_file", "agent_name", "skill_ids"], scope)
        )

        agent_file = str(binding.get("agent_file", "")).strip()
        if not agent_file:
            errors.append(f"{scope}.agent_file cannot be empty")
        elif agent_file in seen_files:
            errors.append(f"duplicate agent_file: {agent_file}")
        else:
            seen_files.add(agent_file)

        agent_name = str(binding.get("agent_name", "")).strip()
        if not agent_name:
            errors.append(f"{scope}.agent_name cannot be empty")
        elif agent_name in seen_names:
            errors.append(f"duplicate agent_name: {agent_name}")
        else:
            seen_names.add(agent_name)

        skill_ids_list = binding.get("skill_ids")
        if not isinstance(skill_ids_list, list) or not skill_ids_list:
            errors.append(f"{scope}.skill_ids must be a non-empty array")
        else:
            for skill_id in skill_ids_list:
                sid = str(skill_id).strip()
                if sid not in skill_ids:
                    errors.append(f"{scope}.skill_ids unknown id: {sid}")

        agent_path = repo_root / agent_file
        if not agent_path.is_file():
            errors.append(f"{scope}.agent_file missing file: {agent_file}")
        else:
            text = agent_path.read_text(encoding="utf-8")
            if "## Runtime bindings (Architecture 2.1)" not in text:
                errors.append(f"{scope}.agent_file missing Runtime bindings section")

    agent_files = sorted((repo_root / ".github" / "agents").glob("*.agent.md"))
    expected_files = {f".github/agents/{p.name}" for p in agent_files}
    missing_bindings = expected_files - seen_files
    for rel_path in sorted(missing_bindings):
        errors.append(f"missing binding for agent file: {rel_path}")

    return errors


def run(repo_root: Path) -> int:
    contracts_dir = repo_root / "mcp" / "contracts"
    contract_files = sorted(contracts_dir.glob("*.contract.json"))

    if not contract_files:
        print("[BLOCKER] no contract files found in mcp/contracts")
        return 1

    blocker_count = 0
    for contract_file in contract_files:
        errors = validate_contract_file(contract_file)
        if errors:
            blocker_count += 1
            print(f"[BLOCKER] {contract_file.as_posix()}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"[OK] {contract_file.as_posix()}")

    catalog_file = repo_root / "mcp" / "capability_catalog.json"
    catalog_errors = validate_capability_catalog(catalog_file)
    if catalog_errors:
        blocker_count += 1
        print(f"[BLOCKER] {catalog_file.as_posix()}")
        for error in catalog_errors:
            print(f"  - {error}")
    else:
        print(f"[OK] {catalog_file.as_posix()}")

    skill_catalog_file = repo_root / "mcp" / "skills" / "skill_catalog.json"
    skill_errors = validate_skill_catalog(skill_catalog_file, repo_root)
    if skill_errors:
        blocker_count += 1
        print(f"[BLOCKER] {skill_catalog_file.as_posix()}")
        for error in skill_errors:
            print(f"  - {error}")
    else:
        print(f"[OK] {skill_catalog_file.as_posix()}")

    backend_catalog_file = repo_root / "mcp" / "backends" / "backend_capabilities.json"
    backend_errors = validate_backend_catalog(backend_catalog_file, repo_root)
    if backend_errors:
        blocker_count += 1
        print(f"[BLOCKER] {backend_catalog_file.as_posix()}")
        for error in backend_errors:
            print(f"  - {error}")
    else:
        print(f"[OK] {backend_catalog_file.as_posix()}")

    tool_index_file = repo_root / "mcp" / "tools" / "tool_contract_index.json"
    tool_index_errors = validate_tool_contract_index(tool_index_file, repo_root)
    if tool_index_errors:
        blocker_count += 1
        print(f"[BLOCKER] {tool_index_file.as_posix()}")
        for error in tool_index_errors:
            print(f"  - {error}")
    else:
        print(f"[OK] {tool_index_file.as_posix()}")

    binding_file = repo_root / ".github" / "agent-skill-binding.json"
    binding_errors = validate_agent_skill_binding(binding_file, repo_root)
    if binding_errors:
        blocker_count += 1
        print(f"[BLOCKER] {binding_file.as_posix()}")
        for error in binding_errors:
            print(f"  - {error}")
    else:
        print(f"[OK] {binding_file.as_posix()}")

    print(f"[SUMMARY] blockers={blocker_count}")
    return 1 if blocker_count else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Stage F contract artifacts")
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root used to resolve mcp/contracts and mcp/capability_catalog.json",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    return run(repo_root)


if __name__ == "__main__":
    raise SystemExit(main())