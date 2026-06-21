#!/usr/bin/env python
"""Process tool: split markdown into manuscript and process supplement by section mapping."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

H2_RE = re.compile(r"^##\s+(.+?)\s*$")


@dataclass(frozen=True)
class Section:
    title: str
    lines: list[str]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_source(path: Path) -> tuple[str, list[Section]]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    title = lines[0] if lines else "# Dokument"

    starts: list[tuple[int, str]] = []
    in_fence = False
    fence_token = ""
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            token = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_token = token
            elif token == fence_token:
                in_fence = False
                fence_token = ""
            continue

        if in_fence:
            continue

        m = H2_RE.match(line)
        if m:
            starts.append((i, m.group(1).strip()))

    sections: list[Section] = []
    for idx, (start, section_title) in enumerate(starts):
        end = starts[idx + 1][0] if idx + 1 < len(starts) else len(lines)
        sections.append(Section(title=section_title, lines=lines[start:end]))

    return title, sections


def _classify(title: str, rules: list[dict[str, str]], default_target: str) -> str:
    for rule in rules:
        pattern = str(rule.get("pattern", "")).strip()
        target = str(rule.get("target", "")).strip().lower()
        if not pattern or target not in {"manuscript", "supplement", "both"}:
            continue
        if re.search(pattern, title, flags=re.IGNORECASE):
            return target
    return default_target


def _render_doc(doc_title: str, source: Path, sections: list[Section], kind: str) -> str:
    ts = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    out: list[str] = [
        doc_title,
        "",
        f"- Zrodlo: {source.as_posix()}",
        f"- Wygenerowano: {ts}",
        f"- Typ: {kind}",
        "",
    ]

    for section in sections:
        out.extend(section.lines)
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def _render_report(
    source: Path,
    manuscript_path: Path,
    supplement_path: Path,
    section_targets: list[tuple[str, str]],
) -> str:
    ts = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    man_count = sum(1 for _, t in section_targets if t in {"manuscript", "both"})
    sup_count = sum(1 for _, t in section_targets if t in {"supplement", "both"})

    lines = [
        "# Raport splitu manuskrypt/suplement",
        "",
        f"- Data: {ts}",
        f"- Zrodlo: {source.as_posix()}",
        f"- Manuskript: {manuscript_path.as_posix()}",
        f"- Suplement: {supplement_path.as_posix()}",
        f"- Sekcje do manuskryptu: {man_count}",
        f"- Sekcje do suplementu: {sup_count}",
        "",
        "## Mapowanie sekcji",
        "| Sekcja | Target |",
        "|---|---|",
    ]

    for title, target in section_targets:
        lines.append(f"| {title} | {target} |")

    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Split markdown into manuscript and supplement")
    parser.add_argument("--config", required=True, help="Path to split config JSON")
    args = parser.parse_args()

    cfg_path = Path(args.config).resolve()
    if not cfg_path.exists():
        print(f"[FAIL] config not found: {cfg_path}")
        return 1

    try:
        cfg = _load_json(cfg_path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[FAIL] cannot load config: {exc}")
        return 1

    source = (cfg_path.parent / str(cfg.get("source", ""))).resolve()
    out_man = (cfg_path.parent / str(cfg.get("manuscript_output", ""))).resolve()
    out_sup = (cfg_path.parent / str(cfg.get("supplement_output", ""))).resolve()
    out_rep = (cfg_path.parent / str(cfg.get("report_output", ""))).resolve()
    default_target = str(cfg.get("default_target", "manuscript")).strip().lower()
    rules = cfg.get("rules", [])

    if default_target not in {"manuscript", "supplement", "both"}:
        print("[FAIL] invalid default_target")
        return 1

    if not source.exists():
        print(f"[FAIL] source not found: {source}")
        return 1

    _, sections = _read_source(source)
    if not sections:
        print("[FAIL] no level-2 sections found")
        return 1

    manuscript_sections: list[Section] = []
    supplement_sections: list[Section] = []
    section_targets: list[tuple[str, str]] = []

    for section in sections:
        target = _classify(section.title, rules, default_target)
        section_targets.append((section.title, target))

        if target in {"manuscript", "both"}:
            manuscript_sections.append(section)
        if target in {"supplement", "both"}:
            supplement_sections.append(section)

    out_man.parent.mkdir(parents=True, exist_ok=True)
    out_sup.parent.mkdir(parents=True, exist_ok=True)
    out_rep.parent.mkdir(parents=True, exist_ok=True)

    man_title = str(cfg.get("manuscript_title", "# Manuskrypt"))
    sup_title = str(cfg.get("supplement_title", "# Suplement procesowy"))

    out_man.write_text(
        _render_doc(man_title, source, manuscript_sections, "manuscript"), encoding="utf-8"
    )
    out_sup.write_text(
        _render_doc(sup_title, source, supplement_sections, "supplement"), encoding="utf-8"
    )
    out_rep.write_text(_render_report(source, out_man, out_sup, section_targets), encoding="utf-8")

    print(f"[OK] manuscript: {out_man}")
    print(f"[OK] supplement: {out_sup}")
    print(f"[OK] report: {out_rep}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
