#!/usr/bin/env python
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

ALLOWED_DECISIONS = {"pending", "pass", "pass-with-comments", "fail"}
ALLOWED_STATUSES = {"OK", "Warning", "Blocker", "Missing"}


@dataclass
class ArtifactEntry:
    path: str
    status: str
    note: str
    exists: bool


def _parse_artifact(raw: str, root: Path) -> ArtifactEntry:
    parts = [part.strip() for part in raw.split("|", 2)]
    if len(parts) < 2:
        raise ValueError("artifact must use format: path|status|optional note")

    path_text = parts[0]
    status = parts[1]
    note = parts[2] if len(parts) == 3 else ""

    if status not in ALLOWED_STATUSES:
        raise ValueError(f"invalid status '{status}' for artifact '{path_text}'")

    artifact_path = (root / path_text).resolve()
    exists = artifact_path.exists()
    normalized_path = Path(path_text).as_posix()
    return ArtifactEntry(path=normalized_path, status=status, note=note, exists=exists)


def _default_artifacts() -> list[str]:
    return [
        "Dokumentacja/Konsolidacja-Statusow.md|Missing|Uzupelnij statusy agentow",
        "Dokumentacja/Rejestr-Konfliktow-i-Eskalacji.md|Missing|Uzupelnij konflikty i decyzje",
        "Dokumentacja/Podsumowanie-Gate.md|Missing|Uzupelnij finalna decyzje gate",
        "Dokumentacja/Review-Jakosci-Gate3.md|Missing|Wymagane dla przeplywu gate 3",
    ]


def build_packet(
    output_file: Path,
    decision: str,
    owner: str,
    artifacts: list[ArtifactEntry],
) -> None:
    timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    rows = []
    for artifact in artifacts:
        exists_text = "yes" if artifact.exists else "no"
        note = artifact.note or "-"
        rows.append(f"| {artifact.path} | {artifact.status} | {exists_text} | {note} |")

    content = "\n".join(
        [
            "# Evidence Packet (minimalny)",
            "",
            f"- Decyzja: {decision}",
            f"- Owner (human-in-the-loop): {owner}",
            f"- Data budowy: {timestamp}",
            "",
            "## Artefakty i statusy",
            "| Artefakt | Status | Exists | Notatka |",
            "|---|---|---|---|",
            *rows,
            "",
            "## Notatki",
            "- Statusy: OK / Warning / Blocker / Missing.",
            "- Plik jest generowany przez tools/build_evidence_packet.py.",
            "",
        ]
    )

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build minimal evidence packet for gate decision")
    parser.add_argument(
        "--output",
        default="Dokumentacja/Evidence-Packet-Gate.md",
        help="Output markdown file path relative to repository root",
    )
    parser.add_argument(
        "--decision",
        default="pending",
        choices=sorted(ALLOWED_DECISIONS),
        help="Gate decision status",
    )
    parser.add_argument("--owner", required=True, help="Decision owner (human-in-the-loop)")
    parser.add_argument(
        "--artifact",
        action="append",
        default=[],
        help="Artifact entry in format: path|status|optional note",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    output_file = (root / args.output).resolve()

    raw_artifacts = args.artifact if args.artifact else _default_artifacts()
    artifacts: list[ArtifactEntry] = []
    try:
        for raw in raw_artifacts:
            artifacts.append(_parse_artifact(raw, root))
    except ValueError as exc:
        print(f"[FAIL] {exc}")
        return 1

    build_packet(
        output_file=output_file,
        decision=args.decision,
        owner=args.owner,
        artifacts=artifacts,
    )
    print(f"[OK] Evidence packet written: {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
