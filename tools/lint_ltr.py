#!/usr/bin/env python
"""LTR lint: checks basic tag formats in Markdown files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


EQ_TAG_RE = re.compile(r"^\s*\[EQ:([A-Za-z0-9_-]+)\]\s*$")
ID_TYP_RE = re.compile(r"\[[A-Za-z0-9_-]+:[A-Za-z0-9_-]+\]")


def should_skip(path: Path) -> bool:
    parts = {p.lower() for p in path.parts}
    return ".git" in parts or ".venv" in parts


def lint_file(path: Path) -> list[str]:
    warnings: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"{path}: nie mozna odczytac pliku ({exc})"]

    for idx, line in enumerate(text.splitlines(), start=1):
        if "[EQ:" in line and not EQ_TAG_RE.match(line):
            warnings.append(f"{path}:{idx}: niepoprawny tag [EQ:ID]")
        if ("Powiazane artefakty" in line or "Powiazany" in line) and "[" in line:
            if not ID_TYP_RE.search(line):
                warnings.append(f"{path}:{idx}: brak formatu [ID:Typ] w powiazaniach")
    return warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="LTR lint for tag formats")
    parser.add_argument("path", nargs="?", default=".", help="Sciezka do repo")
    parser.add_argument("--fail-on-warning", action="store_true", help="Zakoncz z kodem 1")
    args = parser.parse_args()

    root = Path(args.path).resolve()
    md_files = [p for p in root.rglob("*.md") if not should_skip(p)]

    warnings: list[str] = []
    for md_file in md_files:
        warnings.extend(lint_file(md_file))

    if warnings:
        print("LTR lint: ostrzezenia")
        for item in warnings:
            print(f"- {item}")
        return 1 if args.fail_on_warning else 0

    print("LTR lint: brak ostrzezen")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
