#!/usr/bin/env python
"""Process check: consistency of key symbolic definitions across markdown artifacts."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Rule:
    name: str
    include: list[str]
    must_match: list[str]
    must_not_match: list[str]


def _default_rules() -> list[Rule]:
    return [
        Rule(
            name="ratio_RY",
            include=[
                "Badania/**/Raport-Wyprowadzen-LTR.md",
                "Badania/**/Publikacja-Merytoryczna-*.md",
            ],
            must_match=[
                r"R\s*=\s*\\frac\{\|\\Delta\\(?:phi|varphi)_Y\|\}\{\|\\Delta\\(?:phi|varphi)_\{1PN\}\|\}",
            ],
            must_not_match=[
                r"R\s*=\s*\\frac\{\|\\Delta\\(?:phi|varphi)_\{1PN\}\|\}\{\|\\Delta\\(?:phi|varphi)_Y\|\}",
            ],
        )
    ]


def _load_rules(config_path: Path | None) -> list[Rule]:
    if config_path is None:
        return _default_rules()

    raw = json.loads(config_path.read_text(encoding="utf-8"))
    rules: list[Rule] = []
    for item in raw.get("rules", []):
        name = str(item.get("name", "")).strip()
        include = [str(v) for v in item.get("include", []) if str(v).strip()]
        must_match = [str(v) for v in item.get("must_match", []) if str(v).strip()]
        must_not_match = [str(v) for v in item.get("must_not_match", []) if str(v).strip()]
        if name and include and must_match:
            rules.append(
                Rule(
                    name=name,
                    include=include,
                    must_match=must_match,
                    must_not_match=must_not_match,
                )
            )
    return rules or _default_rules()


def _resolve_files(root: Path, include_globs: list[str]) -> list[Path]:
    files: dict[Path, None] = {}
    for glob in include_globs:
        for path in root.glob(glob):
            if path.is_file():
                files[path.resolve()] = None
    return sorted(files.keys())


def _run_rule(root: Path, rule: Rule) -> tuple[list[str], list[str]]:
    files = _resolve_files(root, rule.include)
    errors: list[str] = []
    infos: list[str] = []

    if not files:
        errors.append(f"{rule.name}: no files matched include globs")
        return infos, errors

    must_match_re = [re.compile(p) for p in rule.must_match]
    must_not_re = [re.compile(p) for p in rule.must_not_match]

    for file_path in files:
        text = file_path.read_text(encoding="utf-8")

        for pattern in must_match_re:
            if not pattern.search(text):
                errors.append(
                    f"{rule.name}: missing required pattern in {file_path}: {pattern.pattern}"
                )

        for pattern in must_not_re:
            if pattern.search(text):
                errors.append(
                    f"{rule.name}: forbidden pattern found in {file_path}: {pattern.pattern}"
                )

        infos.append(f"{rule.name}: checked {file_path}")

    return infos, errors


def _apply_include_override(rules: list[Rule], include_globs: list[str]) -> list[Rule]:
    if not include_globs:
        return rules

    overridden: list[Rule] = []
    for rule in rules:
        overridden.append(
            Rule(
                name=rule.name,
                include=include_globs,
                must_match=rule.must_match,
                must_not_match=rule.must_not_match,
            )
        )
    return overridden


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check definition consistency in markdown artifacts"
    )
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--config", help="Optional JSON config with custom rules")
    parser.add_argument(
        "--include-glob",
        action="append",
        default=[],
        help="Override include globs for all rules (repeatable)",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    config_path = Path(args.config).resolve() if args.config else None

    try:
        rules = _load_rules(config_path)
        rules = _apply_include_override(rules, args.include_glob)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[FAIL] cannot load config: {exc}")
        return 1

    all_infos: list[str] = []
    all_errors: list[str] = []

    for rule in rules:
        infos, errors = _run_rule(root, rule)
        all_infos.extend(infos)
        all_errors.extend(errors)

    for item in all_infos:
        print(f"[INFO] {item}")

    if all_errors:
        print("[FAIL] definition consistency check failed")
        for item in all_errors:
            print(f"- {item}")
        return 1

    print("[OK] definition consistency check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
