#!/usr/bin/env python
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALIAS_MAP_FILE = ROOT / "Dokumentacja" / "Szablon-LTR" / "alias-map.json"
REFERENCE_README = ROOT / "Dokumentacja" / "Szablon-LTR" / "README.md"


@dataclass
class Term:
    canonical: str
    aliases: list[str]


def _normalize(value: str) -> str:
    return " ".join(value.strip().lower().split())


def _load_terms() -> list[Term]:
    data = json.loads(ALIAS_MAP_FILE.read_text(encoding="utf-8"))
    raw_terms = data.get("terms", [])
    terms: list[Term] = []
    for item in raw_terms:
        canonical = str(item.get("canonical", "")).strip()
        aliases = [str(alias).strip() for alias in item.get("aliases", [])]
        terms.append(Term(canonical=canonical, aliases=aliases))
    return terms


def check_taxonomy_drift(verbose: bool = True) -> int:
    if not ALIAS_MAP_FILE.exists():
        if verbose:
            print("[FAIL] Missing alias map: Dokumentacja/Szablon-LTR/alias-map.json")
        return 1

    if not REFERENCE_README.exists():
        if verbose:
            print("[FAIL] Missing reference file: Dokumentacja/Szablon-LTR/README.md")
        return 1

    try:
        terms = _load_terms()
    except json.JSONDecodeError as exc:
        if verbose:
            print(f"[FAIL] Invalid JSON in alias map: {exc}")
        return 1

    failures: list[str] = []
    canonical_seen: set[str] = set()
    alias_owner: dict[str, str] = {}

    for term in terms:
        canonical = term.canonical
        if not canonical:
            failures.append("Empty canonical term in alias map")
            continue

        canonical_norm = _normalize(canonical)
        if canonical_norm in canonical_seen:
            failures.append(f"Duplicate canonical term: {canonical}")
        canonical_seen.add(canonical_norm)

        for alias in term.aliases:
            alias_norm = _normalize(alias)
            if not alias_norm:
                failures.append(f"Empty alias for canonical term: {canonical}")
                continue

            existing_owner = alias_owner.get(alias_norm)
            if existing_owner and existing_owner != canonical:
                collision = (
                    f"Alias collision: '{alias}' mapped to both "
                    f"'{existing_owner}' and '{canonical}'"
                )
                failures.append(
                    collision
                )
            alias_owner[alias_norm] = canonical

    readme_text_norm = _normalize(REFERENCE_README.read_text(encoding="utf-8"))
    for term in terms:
        if _normalize(term.canonical) not in readme_text_norm:
            failures.append(
                f"Taxonomy drift: canonical term '{term.canonical}' missing in README reference"
            )

    if failures:
        if verbose:
            for failure in failures:
                print(f"[FAIL] {failure}")
        return 1

    if verbose:
        print("[OK] Taxonomy guard passed (aliases and canonical terms are consistent)")
    return 0


def main() -> int:
    return check_taxonomy_drift(verbose=True)


if __name__ == "__main__":
    raise SystemExit(main())
