#!/usr/bin/env python
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

ALLOWED_DECISIONS = {"pending", "pass", "pass-with-comments", "fail"}
ALLOWED_STATUSES = {"OK", "Warning", "Blocker", "Missing"}
ALLOWED_GATES = {"G1", "G2", "G3", "G4"}


@dataclass
class ArtifactEntry:
    path: str
    status: str
    note: str
    exists: bool
    artifact_id: str
    artifact_type: str


def _slug(value: str) -> str:
    return "".join(char if char.isalnum() else "-" for char in value).strip("-")


def _artifact_id(path_text: str) -> str:
    stem = Path(path_text).stem.upper()
    stem_slug = _slug(stem)
    return f"ART-{stem_slug or 'UNNAMED'}"


def _artifact_type(path_text: str) -> str:
    stem = Path(path_text).stem
    return _slug(stem) or "unknown"


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
    return ArtifactEntry(
        path=normalized_path,
        status=status,
        note=note,
        exists=exists,
        artifact_id=_artifact_id(normalized_path),
        artifact_type=_artifact_type(normalized_path),
    )


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
    gate_id: str,
    case_id: str,
    schema_version: str,
    manifest_mode: str,
) -> None:
    timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    rows = []
    for artifact in artifacts:
        exists_text = "yes" if artifact.exists else "no"
        note = artifact.note or "-"
        rows.append(f"| {artifact.path} | {artifact.status} | {exists_text} | {note} |")

    manifest_rows = []
    for artifact in artifacts:
        exists_text = "yes" if artifact.exists else "no"
        note = artifact.note or "-"
        manifest_rows.append(
            "| "
            f"{artifact.artifact_id} | {artifact.artifact_type} | {artifact.path} | "
            f"{gate_id} | {artifact.status} | {exists_text} | {note} |"
        )

    content_lines = [
        "# Evidence Packet (minimalny)",
        "",
        f"- Decyzja: {decision}",
        f"- Owner (human-in-the-loop): {owner}",
        f"- Gate ID: {gate_id}",
        f"- Case ID: {case_id if case_id else '-'}",
        f"- Data budowy: {timestamp}",
        "",
        "## Artefakty i statusy",
        "| Artefakt | Status | Exists | Notatka |",
        "|---|---|---|---|",
        *rows,
        "",
    ]

    if manifest_mode == "inline":
        content_lines.extend(
            [
                "## Manifest OKF-lite",
                f"- Schema: {schema_version}",
                "- Tryb: selektywny transfer metadanych (bez utraty merytoryki).",
                "| Artifact ID | Type | Path | Required For | Status | Exists | Note |",
                "|---|---|---|---|---|---|---|",
                *manifest_rows,
                "",
            ]
        )

    content_lines.extend(
        [
            "## Zero-loss guard (merytoryka)",
            "- Generator nie przenosi ani nie kompresuje tresci merytorycznej dokumentow case.",
            (
                "- Evidence packet ma role indeksu i statusow; tresc naukowa pozostaje "
                "w artefaktach zrodlowych."
            ),
            (
                "- Brak krytycznych artefaktow powinien byc traktowany fail_closed "
                "(Blocker + eskalacja)."
            ),
            "",
            "## Notatki",
            "- Statusy: OK / Warning / Blocker / Missing.",
            "- Plik jest generowany przez tools/build_evidence_packet.py.",
            "",
        ]
    )

    content = "\n".join(content_lines)

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
        "--gate-id",
        default="G3",
        choices=sorted(ALLOWED_GATES),
        help="Gate identifier",
    )
    parser.add_argument(
        "--case-id",
        default="",
        help="Optional case identifier (e.g. T03-Newton-Yukawa-Orbit-Stability)",
    )
    parser.add_argument(
        "--schema-version",
        default="okf-lite/v1",
        help="Schema label for the inline manifest",
    )
    parser.add_argument(
        "--manifest-mode",
        default="table-only",
        choices=["table-only", "inline"],
        help="Output mode: legacy table-only or table + inline OKF-lite manifest",
    )
    parser.add_argument(
        "--strict-metadata",
        action="store_true",
        help="Enable fail-closed checks for required metadata and critical artifacts",
    )
    parser.add_argument(
        "--require-artifact",
        action="append",
        default=[],
        help="Critical artifact path. Repeat option for multiple entries.",
    )
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

    owner = args.owner.strip()
    if not owner:
        print("[FAIL] owner cannot be empty")
        return 1

    if len({artifact.path for artifact in artifacts}) != len(artifacts):
        print("[FAIL] duplicate artifact path detected")
        return 1

    if len({artifact.artifact_id for artifact in artifacts}) != len(artifacts):
        print("[FAIL] duplicate artifact id detected; rename one of the artifacts")
        return 1

    required_paths = {Path(path).as_posix() for path in args.require_artifact}
    if args.strict_metadata:
        if args.gate_id not in ALLOWED_GATES:
            print(f"[FAIL] invalid gate id '{args.gate_id}'")
            return 1

        artifact_paths = {artifact.path for artifact in artifacts}
        missing_required = sorted(
            path for path in required_paths if path not in artifact_paths
        )
        if missing_required:
            print(f"[FAIL] missing required artifacts in packet: {', '.join(missing_required)}")
            return 1

        blocking = [
            artifact.path
            for artifact in artifacts
            if artifact.path in required_paths
            and (not artifact.exists or artifact.status in {"Missing", "Blocker"})
        ]
        if blocking:
            print(
                "[FAIL] fail_closed: required artifacts are missing or blocking: "
                + ", ".join(sorted(blocking))
            )
            return 1

    build_packet(
        output_file=output_file,
        decision=args.decision,
        owner=owner,
        artifacts=artifacts,
        gate_id=args.gate_id,
        case_id=args.case_id.strip(),
        schema_version=args.schema_version,
        manifest_mode=args.manifest_mode,
    )
    print(f"[OK] Evidence packet written: {output_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
