#!/usr/bin/env python
"""Generate reviewer response traceability from implementation matrix markdown."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

ROW_SPLIT_RE = re.compile(r"\s*\|\s*")


@dataclass(frozen=True)
class MatrixRow:
    issue_id: str
    priority: str
    status: str
    action: str
    artifacts: str
    done_criteria: str


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _parse_matrix_rows(text: str) -> list[MatrixRow]:
    lines = text.splitlines()

    header_idx = -1
    for i, line in enumerate(lines):
        if line.strip().startswith("| ID uwagi |"):
            header_idx = i
            break

    if header_idx < 0 or header_idx + 2 >= len(lines):
        return []

    rows: list[MatrixRow] = []

    for line in lines[header_idx + 2 :]:
        if not line.strip().startswith("|"):
            break

        raw_cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(raw_cells) < 6:
            continue

        if len(raw_cells) > 6:
            # Some cells may contain literal '|' in action text. Find artifacts cell heuristically.
            tail = raw_cells[3:]
            artifact_idx = next((i for i, cell in enumerate(tail) if ".md" in cell), -1)
            if artifact_idx >= 0:
                action_cell = "|".join(tail[:artifact_idx]).strip()
                artifacts_cell = tail[artifact_idx].strip()
                criteria_cell = "|".join(tail[artifact_idx + 1 :]).strip()
                raw_cells = [
                    raw_cells[0],
                    raw_cells[1],
                    raw_cells[2],
                    action_cell,
                    artifacts_cell,
                    criteria_cell,
                ]
            else:
                raw_cells = [
                    raw_cells[0],
                    raw_cells[1],
                    raw_cells[2],
                    " | ".join(raw_cells[3:-2]).strip(),
                    raw_cells[-2],
                    raw_cells[-1],
                ]

        row = MatrixRow(
            issue_id=raw_cells[0],
            priority=raw_cells[1],
            status=raw_cells[2],
            action=raw_cells[3],
            artifacts=raw_cells[4],
            done_criteria=raw_cells[5],
        )
        rows.append(row)

    return rows


def _risk_level(priority: str, status: str) -> str:
    p = priority.lower()
    s = status.lower()

    if "blocker" in p and s not in {"done", "closed", "approved"}:
        return "Blocker"
    if "high" in p and s not in {"done", "closed", "approved"}:
        return "Warning"
    if s in {"in_review", "todo", "planned"}:
        return "Warning"
    return "OK"


def _md_cell(value: str) -> str:
    return value.replace("|", "\\|").strip()


def _render_report(case_id: str, matrix_path: Path, rows: list[MatrixRow]) -> str:
    ts = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")

    open_count = sum(1 for r in rows if r.status.lower() not in {"done", "closed", "approved"})
    blocker_count = sum(
        1
        for r in rows
        if "blocker" in r.priority.lower()
        and r.status.lower() not in {"done", "closed", "approved"}
    )

    lines = [
        "# Odpowiedz dla recenzenta - traceability",
        "",
        "## Metadane",
        f"- Case: {case_id}",
        f"- Data generacji: {ts}",
        f"- Zrodlo: {matrix_path.as_posix()}",
        f"- Liczba uwag: {len(rows)}",
        f"- Otwarte uwagi: {open_count}",
        f"- Otwarte blockery: {blocker_count}",
        "",
        "## Tabela mapowania uwaga -> zmiana -> plik -> status",
        (
            "| ID uwagi | Priorytet | Status | Zmiana | Plik(i) | "
            "Kryterium domkniecia | Ocena ryzyka |"
        ),
        "|---|---|---|---|---|---|---|",
    ]

    for r in rows:
        risk = _md_cell(_risk_level(r.priority, r.status))
        lines.append(
            "| "
            f"{_md_cell(r.issue_id)} | {_md_cell(r.priority)} | {_md_cell(r.status)} | "
            f"{_md_cell(r.action)} | {_md_cell(r.artifacts)} | "
            f"{_md_cell(r.done_criteria)} | {risk} |"
        )

    lines.extend(
        [
            "",
            "## Uwagi",
            "- Dokument jest generowany automatycznie z macierzy wdrozenia.",
            "- Braki statusow merytorycznych pozostaja decyzja wlasciciela badania (HITL).",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate reviewer traceability response from matrix"
    )
    parser.add_argument(
        "--matrix", required=True, help="Path to MACIERZ_WDROZENIA_UWAG_RECENZENTA.md"
    )
    parser.add_argument("--output", required=True, help="Output markdown file")
    parser.add_argument("--case-id", default="-", help="Case identifier")
    parser.add_argument(
        "--fail-on-open-blocker",
        action="store_true",
        help="Exit with code 1 if any blocker is still open",
    )
    parser.add_argument(
        "--suppress-open-blocker-warning",
        action="store_true",
        help="Do not emit WARNING when open merytory blockers are expected",
    )
    args = parser.parse_args()

    matrix_path = Path(args.matrix).resolve()
    output_path = Path(args.output).resolve()

    if not matrix_path.exists():
        print(f"[FAIL] matrix not found: {matrix_path}")
        return 1

    rows = _parse_matrix_rows(_read_text(matrix_path))
    if not rows:
        print("[FAIL] could not parse matrix table")
        return 1

    report = _render_report(args.case_id, matrix_path, rows)
    output_path.write_text(report, encoding="utf-8")
    print(f"[OK] traceability report written: {output_path}")

    open_blockers = [
        r
        for r in rows
        if "blocker" in r.priority.lower()
        and r.status.lower() not in {"done", "closed", "approved"}
    ]
    if open_blockers:
        if not args.suppress_open_blocker_warning:
            print(f"[WARNING] open blockers: {len(open_blockers)}")
        else:
            print(f"[INFO] open blockers (suppressed warning): {len(open_blockers)}")
        if args.fail_on_open_blocker:
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
