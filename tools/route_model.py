#!/usr/bin/env python
"""Simple model routing based on agent name and context."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def select_model(config: dict, agent: str, gate: int | None, risk: str | None) -> str:
    overrides = config.get("agent_overrides", {})
    if agent in overrides:
        base = overrides[agent]
    else:
        base = config.get("default", "low-cost")

    # Escalation rules
    for rule in config.get("escalation_rules", []):
        condition = rule.get("condition", "")
        if gate is not None and "gate in [3,4]" in condition and gate in (3, 4):
            return rule.get("model", base)
        if risk and "risk == 'high'" in condition and risk.lower() == "high":
            return rule.get("model", base)

    return base


def main() -> int:
    parser = argparse.ArgumentParser(description="Route model for agent execution")
    parser.add_argument("agent", help="Agent name, e.g. cross-reference")
    parser.add_argument("--gate", type=int, help="Gate number (optional)")
    parser.add_argument("--risk", choices=["low", "medium", "high"], help="Risk level")
    parser.add_argument(
        "--config",
        default="tools/model_routing.json",
        help="Path to routing config",
    )
    args = parser.parse_args()

    config = load_config(Path(args.config))
    model = select_model(config, args.agent, args.gate, args.risk)
    print(model)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
