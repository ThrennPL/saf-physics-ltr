#!/usr/bin/env python
from __future__ import annotations

from pathlib import Path

import mcp_baseline
import taxonomy_guard

ROOT = Path(__file__).resolve().parents[1]
ENV_EXAMPLE = ROOT / ".env.example"


def fail(message: str) -> int:
    print(f"[FAIL] {message}")
    return 1


def check_mcp() -> int:
    return mcp_baseline.check_mcp_config(verbose=True)


def check_env_example() -> int:
    if not ENV_EXAMPLE.exists():
        return fail("Missing .env.example")

    token_line = None
    for raw in ENV_EXAMPLE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("ADS_API_TOKEN="):
            token_line = line
            break

    if token_line is None:
        return fail(".env.example does not define ADS_API_TOKEN")

    value = token_line.split("=", 1)[1].strip()
    if not value or value == "__SET_LOCAL_ADS_TOKEN__":
        print("[OK] .env.example uses placeholder for ADS_API_TOKEN")
        return 0

    return fail(".env.example ADS_API_TOKEN must be placeholder or empty")


def check_taxonomy() -> int:
    return taxonomy_guard.check_taxonomy_drift(verbose=True)


def main() -> int:
    checks = [check_mcp(), check_env_example(), check_taxonomy()]
    if any(code != 0 for code in checks):
        return 1
    print("[OK] Security sanity check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
