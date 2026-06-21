#!/usr/bin/env python
"""Process check: manuscript completeness against required section patterns."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SectionRule:
    name: str
    pattern: str


def _default_rules() -> list[SectionRule]:
    return [
        SectionRule("intro", r"^##\s+((\d+\.)\s*)?(Wstep|Wstęp|Problem i cel)\b"),
        SectionRule(
            "model",
            r"^##\s+((\d+\.)\s*)?(Model teoretyczny|Potencja[łl] Newtonowski i Yukawy)\b",
        ),
        SectionRule("results", r"^##\s+Wyniki\b"),
        SectionRule("limits", r"^##\s+((\d+\.)\s*)?(Ograniczenia|Limitations)\b"),
        SectionRule(
            "conclusions",
            r"^##\s+((\d+\.)\s*)?(Wnioski|Wnioski koncowe|Wnioski końcowe)\b",
        ),
        SectionRule("bibliography", r"^##\s+((\d+\.)\s*)?Bibliografia\b"),
    ]


def _load_rules(config_path: Path | None) -> list[SectionRule]:
    if config_path is None:
        return _default_rules()

    raw = json.loads(config_path.read_text(encoding="utf-8"))
    loaded: list[SectionRule] = []
    for item in raw.get("required_sections", []):
        name = str(item.get("name", "")).strip()
        pattern = str(item.get("pattern", "")).strip()
        if name and pattern:
            loaded.append(SectionRule(name=name, pattern=pattern))
    return loaded or _default_rules()


def run_check(manuscript: Path, rules: list[SectionRule]) -> tuple[list[str], list[str]]:
    text = manuscript.read_text(encoding="utf-8")
    lines = text.splitlines()

    ok: list[str] = []
    missing: list[str] = []

    for rule in rules:
        compiled = re.compile(rule.pattern)
        found = any(compiled.search(line) for line in lines)
        if found:
            ok.append(rule.name)
        else:
            missing.append(rule.name)

    return ok, missing


def main() -> int:
    parser = argparse.ArgumentParser(description="Check manuscript completeness")
    parser.add_argument("manuscript", help="Path to manuscript markdown file")
    parser.add_argument(
        "--config",
        help="Optional JSON config with required_sections",
    )
    parser.add_argument(
        "--fail-on-missing",
        action="store_true",
        help="Exit with code 1 when any required section is missing",
    )
    args = parser.parse_args()

    manuscript = Path(args.manuscript).resolve()
    if not manuscript.exists():
        print(f"[FAIL] manuscript not found: {manuscript}")
        return 1

    config_path = Path(args.config).resolve() if args.config else None
    try:
        rules = _load_rules(config_path)
        ok, missing = run_check(manuscript, rules)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[FAIL] cannot run completeness check: {exc}")
        return 1

    print(f"[INFO] manuscript: {manuscript}")
    print(f"[INFO] required sections: {len(rules)}")
    print(f"[OK] present: {', '.join(ok) if ok else '-'}")

    if missing:
        print(f"[WARN] missing: {', '.join(missing)}")
        return 1 if args.fail_on_missing else 0

    print("[OK] completeness check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
