#!/usr/bin/env python
"""Process check: verify provenance metadata for parameters and ranges in markdown plans."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")


@dataclass(frozen=True)
class Issue:
    level: str  # INFO | WARNING | BLOCKER
    message: str


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section(text: str, heading_starts_with: str) -> str:
    lines = text.splitlines()
    start = -1
    for idx, line in enumerate(lines):
        m = HEADING_RE.match(line)
        if m and m.group(1).lower().startswith(heading_starts_with.lower()):
            start = idx + 1
            break
    if start < 0:
        return ""

    end = len(lines)
    for idx in range(start, len(lines)):
        if HEADING_RE.match(lines[idx]):
            end = idx
            break
    return "\n".join(lines[start:end])


def _extract_table_after_heading(text: str, heading_starts_with: str) -> list[dict[str, str]]:
    section = _section(text, heading_starts_with)
    if not section:
        return []

    lines = [ln.rstrip() for ln in section.splitlines() if ln.strip()]
    table_start = -1
    for i in range(len(lines) - 1):
        if lines[i].strip().startswith("|") and lines[i + 1].strip().startswith("|---"):
            table_start = i
            break
    if table_start < 0:
        return []

    header_cells = [c.strip() for c in lines[table_start].strip().strip("|").split("|")]
    rows: list[dict[str, str]] = []

    for line in lines[table_start + 2 :]:
        if not line.strip().startswith("|"):
            break
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != len(header_cells):
            continue
        rows.append({header_cells[i]: cells[i] for i in range(len(header_cells))})

    return rows


def run_check(plan_path: Path, critical_params: set[str]) -> list[Issue]:
    text = _read_text(plan_path)
    issues: list[Issue] = []

    sources_section = _section(text, "Zrodla")
    if not sources_section:
        issues.append(Issue("BLOCKER", "Brak sekcji 'Zrodla'."))
        return issues

    has_url_or_doi = bool(URL_RE.search(sources_section) or DOI_RE.search(sources_section))
    if not has_url_or_doi:
        issues.append(Issue("BLOCKER", "Sekcja 'Zrodla' nie zawiera URL/DOI."))

    ref_rows = _extract_table_after_heading(text, "Tabela parametrow referencyjnych")
    if not ref_rows:
        issues.append(Issue("BLOCKER", "Brak tabeli 'Tabela parametrow referencyjnych'."))
        return issues

    required_ref_cols = {"Parametr", "Zrodlo", "Data dostepu"}
    ref_cols = set(ref_rows[0].keys()) if ref_rows else set()
    missing_ref_cols = sorted(required_ref_cols - ref_cols)
    if missing_ref_cols:
        issues.append(
            Issue("BLOCKER", f"Brak kolumn w tabeli referencyjnej: {', '.join(missing_ref_cols)}")
        )
        return issues

    provenance_by_param: dict[str, tuple[str, str]] = {}
    for row in ref_rows:
        param = row.get("Parametr", "").strip()
        src = row.get("Zrodlo", "").strip()
        date = row.get("Data dostepu", "").strip()
        if not param:
            continue

        if not src:
            issues.append(
                Issue("BLOCKER", f"Parametr '{param}' bez pola Zrodlo w tabeli referencyjnej.")
            )
        if not date:
            issues.append(
                Issue(
                    "BLOCKER", f"Parametr '{param}' bez pola Data dostepu w tabeli referencyjnej."
                )
            )

        if src and src.lower() not in sources_section.lower():
            issues.append(
                Issue(
                    "WARNING",
                    (
                        f"Parametr '{param}' ma zrodlo '{src}', "
                        "ktore nie wystepuje jawnie w sekcji Zrodla."
                    ),
                )
            )

        provenance_by_param[_norm(param)] = (src, date)

    range_rows = _extract_table_after_heading(text, "Zalozenia propagacji niepewnosci")
    if not range_rows:
        issues.append(Issue("WARNING", "Brak tabeli 'Zalozenia propagacji niepewnosci'."))
        return issues

    if "Parametr" not in range_rows[0]:
        issues.append(Issue("BLOCKER", "Tabela zalozen nie zawiera kolumny 'Parametr'."))
        return issues

    # Heurystyka mapowania parametrow zakresowych do referencyjnych
    ref_keys = list(provenance_by_param.keys())
    for row in range_rows:
        param = row.get("Parametr", "").strip()
        if not param:
            continue

        pnorm = _norm(param)
        has_provenance = False

        for rkey in ref_keys:
            if pnorm == rkey or pnorm in rkey or rkey in pnorm:
                has_provenance = True
                break

        if not has_provenance:
            level = "BLOCKER" if pnorm in critical_params else "WARNING"
            issues.append(
                Issue(
                    level,
                    (
                        "Brak metadanych provenance dla zakresu parametru "
                        f"'{param}' (DOI/URL/data dostepu)."
                    ),
                )
            )

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate parameter provenance in markdown data plans"
    )
    parser.add_argument("plan", help="Path to Plan-Danych markdown")
    parser.add_argument(
        "--critical-params",
        default="beta,lambda",
        help="Comma-separated critical parameters requiring blocker on missing provenance",
    )
    parser.add_argument(
        "--fail-on-blocker",
        action="store_true",
        help="Exit code 1 when at least one BLOCKER is found",
    )
    args = parser.parse_args()

    plan = Path(args.plan).resolve()
    if not plan.exists():
        print(f"[FAIL] file not found: {plan}")
        return 1

    critical = {_norm(x) for x in args.critical_params.split(",") if x.strip()}
    issues = run_check(plan, critical)

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
