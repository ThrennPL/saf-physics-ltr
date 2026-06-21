#!/usr/bin/env python
"""Process check: validate chart artifact pipeline (spec, files, metadata, index)."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Issue:
    level: str  # INFO | WARNING | BLOCKER
    message: str


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _has_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def run_check(spec_path: Path, index_path: Path) -> list[Issue]:
    issues: list[Issue] = []

    if not spec_path.exists():
        return [Issue("BLOCKER", f"Brak pliku spec: {spec_path}")]

    try:
        spec = _load_json(spec_path)
    except (OSError, json.JSONDecodeError) as exc:
        return [Issue("BLOCKER", f"Nie mozna wczytac spec: {exc}")]

    charts = spec.get("charts", [])
    if not isinstance(charts, list) or not charts:
        return [Issue("BLOCKER", "Spec nie zawiera listy charts.")]

    root = spec_path.parent
    index_text = ""
    if index_path.exists():
        index_text = index_path.read_text(encoding="utf-8")
    else:
        issues.append(Issue("WARNING", f"Brak indeksu wykresow: {index_path}"))

    required_fields = ["id", "title", "x_axis", "y_axis", "units", "legend", "caption", "file"]

    for i, chart in enumerate(charts, start=1):
        if not isinstance(chart, dict):
            issues.append(Issue("BLOCKER", f"Pozycja charts[{i}] nie jest obiektem."))
            continue

        chart_id = str(chart.get("id", f"chart_{i}")).strip()

        for field in required_fields:
            if not _has_text(chart.get(field, "")):
                level = "BLOCKER" if field in {"id", "title", "file", "caption"} else "WARNING"
                issues.append(Issue(level, f"Wykres '{chart_id}': brak pola '{field}'."))

        file_value = chart.get("file", "")
        if _has_text(file_value):
            file_path = (root / str(file_value)).resolve()
            if not file_path.exists():
                issues.append(Issue("BLOCKER", f"Wykres '{chart_id}': brak pliku {file_value}."))
            elif file_path.stat().st_size == 0:
                issues.append(
                    Issue("BLOCKER", f"Wykres '{chart_id}': plik {file_value} jest pusty.")
                )

            if index_text and str(file_value) not in index_text:
                issues.append(
                    Issue(
                        "WARNING",
                        f"Wykres '{chart_id}': plik {file_value} nie wystepuje w indeksie.",
                    )
                )

    if len(charts) < 3:
        issues.append(
            Issue("WARNING", f"Spec zawiera {len(charts)} wykres(y); oczekiwano co najmniej 3.")
        )

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate chart artifact pipeline metadata and files"
    )
    parser.add_argument("--spec", required=True, help="Path to chart spec JSON")
    parser.add_argument("--index", required=True, help="Path to markdown index of charts")
    parser.add_argument(
        "--fail-on-blocker",
        action="store_true",
        help="Exit 1 when blocker is found",
    )
    args = parser.parse_args()

    spec_path = Path(args.spec).resolve()
    index_path = Path(args.index).resolve()

    issues = run_check(spec_path, index_path)

    blockers = 0
    warnings = 0
    infos = 0

    for issue in issues:
        print(f"[{issue.level}] {issue.message}")
        if issue.level == "BLOCKER":
            blockers += 1
        elif issue.level == "WARNING":
            warnings += 1
        else:
            infos += 1

    print(f"[SUMMARY] blockers={blockers} warnings={warnings} infos={infos}")

    if blockers and args.fail_on_blocker:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
