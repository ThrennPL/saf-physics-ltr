#!/usr/bin/env python
"""Synchronize and validate local .vscode/mcp.json against repository baseline."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE_FILE = ROOT / "mcp" / "mcp-baseline.json"
BASELINE_HASH_FILE = ROOT / "mcp" / "mcp-baseline.sha256"
LOCAL_MCP_FILE = ROOT / ".vscode" / "mcp.json"
NO_LATEST_PATTERN = re.compile(r"@latest", re.IGNORECASE)


def _fail(message: str, verbose: bool) -> int:
    if verbose:
        print(f"[FAIL] {message}")
    return 1


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _get_baseline_vscode_config() -> dict | None:
    if not BASELINE_FILE.exists():
        return None

    data = _load_json(BASELINE_FILE)
    vscode_cfg = data.get("vscodeMcp")
    return vscode_cfg if isinstance(vscode_cfg, dict) else None


def _get_baseline_policy() -> dict:
    if not BASELINE_FILE.exists():
        return {}
    data = _load_json(BASELINE_FILE)
    policy = data.get("policy", {})
    return policy if isinstance(policy, dict) else {}


def _canonical_json_bytes(data: dict) -> bytes:
    return json.dumps(
        data,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _baseline_sha256() -> str:
    baseline_data = _load_json(BASELINE_FILE)
    return hashlib.sha256(_canonical_json_bytes(baseline_data)).hexdigest()


def _check_baseline_hash_lock(verbose: bool) -> int:
    if not BASELINE_FILE.exists():
        return _fail("Missing mcp/mcp-baseline.json", verbose)

    if not BASELINE_HASH_FILE.exists():
        return _fail(
            "Missing mcp/mcp-baseline.sha256 (run: python tools/mcp_baseline.py lock)",
            verbose,
        )

    expected = BASELINE_HASH_FILE.read_text(encoding="utf-8").strip().lower()
    if not re.fullmatch(r"[a-f0-9]{64}", expected):
        return _fail("Invalid hash format in mcp/mcp-baseline.sha256", verbose)

    current = _baseline_sha256()
    if current != expected:
        return _fail(
            "MCP baseline hash lock mismatch "
            "(run: python tools/mcp_baseline.py lock after approved baseline change)",
            verbose,
        )

    if verbose:
        print("[OK] MCP baseline hash lock verified")
    return 0


def _contains_latest_tag(config: dict) -> bool:
    servers = config.get("servers", {})
    if not isinstance(servers, dict):
        return False

    for server in servers.values():
        if not isinstance(server, dict):
            continue
        args = server.get("args", [])
        if any(NO_LATEST_PATTERN.search(str(arg)) for arg in args):
            return True
    return False


def _enforce_allowlists(config: dict, policy: dict, verbose: bool) -> int:
    servers = config.get("servers", {})
    if not isinstance(servers, dict):
        return _fail("Invalid MCP config: servers must be an object", verbose)

    allowed_server_names = set(policy.get("allowedServerNames", []))
    allowed_commands = set(policy.get("allowedCommands", []))

    if policy.get("allowOnlyPolicyServers") and not allowed_server_names:
        return _fail(
            "Policy requires allowOnlyPolicyServers but allowedServerNames is empty",
            verbose,
        )

    if policy.get("allowOnlyPolicyCommands") and not allowed_commands:
        return _fail(
            "Policy requires allowOnlyPolicyCommands but allowedCommands is empty",
            verbose,
        )

    server_names = set(servers.keys())
    if policy.get("allowOnlyPolicyServers") and not server_names.issubset(allowed_server_names):
        extra = sorted(server_names - allowed_server_names)
        return _fail(f"MCP server allowlist violation: {extra}", verbose)

    for name, server in servers.items():
        if not isinstance(server, dict):
            return _fail(f"Invalid MCP server config for '{name}'", verbose)

        command = str(server.get("command", "")).strip()
        if policy.get("allowOnlyPolicyCommands") and command not in allowed_commands:
            return _fail(f"MCP command allowlist violation for '{name}': {command}", verbose)

    return 0


def _normalized(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True)


def check_mcp_config(verbose: bool = True) -> int:
    baseline_hash_check = _check_baseline_hash_lock(verbose=verbose)
    if baseline_hash_check != 0:
        return baseline_hash_check

    baseline_vscode = _get_baseline_vscode_config()
    if baseline_vscode is None:
        return _fail("Missing or invalid mcp/mcp-baseline.json (vscodeMcp)", verbose)

    baseline_policy = _get_baseline_policy()

    baseline_allowlist = _enforce_allowlists(baseline_vscode, baseline_policy, verbose)
    if baseline_allowlist != 0:
        return baseline_allowlist

    if not LOCAL_MCP_FILE.exists():
        return _fail("Missing .vscode/mcp.json (run: python tools/mcp_baseline.py sync)", verbose)

    try:
        local_mcp = _load_json(LOCAL_MCP_FILE)
    except json.JSONDecodeError as exc:
        return _fail(f"Invalid JSON in .vscode/mcp.json: {exc}", verbose)

    if _contains_latest_tag(baseline_vscode):
        return _fail("Baseline contains @latest; pin exact server versions", verbose)

    if _contains_latest_tag(local_mcp):
        return _fail("Local .vscode/mcp.json uses @latest; pin exact server versions", verbose)

    local_allowlist = _enforce_allowlists(local_mcp, baseline_policy, verbose)
    if local_allowlist != 0:
        return local_allowlist

    if _normalized(local_mcp) != _normalized(baseline_vscode):
        return _fail(
            "Local .vscode/mcp.json is out of sync with baseline (run sync command)",
            verbose,
        )

    if verbose:
        print("[OK] Local .vscode/mcp.json matches mcp/mcp-baseline.json")
    return 0


def sync_local_mcp(verbose: bool = True) -> int:
    baseline_vscode = _get_baseline_vscode_config()
    if baseline_vscode is None:
        return _fail("Missing or invalid mcp/mcp-baseline.json (vscodeMcp)", verbose)

    if _contains_latest_tag(baseline_vscode):
        return _fail("Baseline contains @latest; pin exact server versions", verbose)

    baseline_policy = _get_baseline_policy()
    baseline_allowlist = _enforce_allowlists(baseline_vscode, baseline_policy, verbose)
    if baseline_allowlist != 0:
        return baseline_allowlist

    LOCAL_MCP_FILE.parent.mkdir(parents=True, exist_ok=True)
    LOCAL_MCP_FILE.write_text(
        json.dumps(baseline_vscode, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    if verbose:
        print("[OK] Synchronized .vscode/mcp.json from mcp/mcp-baseline.json")
    return 0


def update_baseline_hash_lock(verbose: bool = True) -> int:
    if not BASELINE_FILE.exists():
        return _fail("Missing mcp/mcp-baseline.json", verbose)

    digest = _baseline_sha256()
    BASELINE_HASH_FILE.write_text(digest + "\n", encoding="utf-8")

    if verbose:
        print("[OK] Updated mcp/mcp-baseline.sha256")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="MCP baseline sync/check helper")
    parser.add_argument(
        "action",
        nargs="?",
        choices=["check", "sync", "lock"],
        default="check",
        help="Action to perform: check, sync, or lock",
    )
    args = parser.parse_args()

    if args.action == "lock":
        return update_baseline_hash_lock(verbose=True)
    if args.action == "sync":
        return sync_local_mcp(verbose=True)
    return check_mcp_config(verbose=True)


if __name__ == "__main__":
    raise SystemExit(main())
