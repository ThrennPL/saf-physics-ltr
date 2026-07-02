from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from tools.owner_weekly_summary import _render


def test_render_includes_escalation_section_and_counts(tmp_path: Path) -> None:
    now = datetime.now(UTC)
    output_path = tmp_path / "owner_weekly_summary.md"
    source_path = tmp_path / "control_cycle_log.jsonl"
    escalation_path = tmp_path / "escalation_queue.jsonl"

    cycle_events = [
        {
            "timestamp_utc": "2026-07-02T10:00:00Z",
            "cycle": "weekly",
            "result": "OK",
            "blockers": 0,
            "steps": [],
        }
    ]

    escalation_events = [
        {
            "timestamp_utc": "2026-07-02T10:01:00Z",
            "incident_path": "docs/operations/incidents/a.md",
            "escalation_key": "docs/operations/incidents/a.md",
            "status": "open",
            "owner": "OwnerA",
            "eta": "<=24h",
        },
        {
            "timestamp_utc": "2026-07-02T10:02:00Z",
            "incident_path": "docs/operations/incidents/b.md",
            "escalation_key": "docs/operations/incidents/b.md",
            "status": "resolved",
            "owner": "OwnerB",
            "eta": "<=12h",
        },
    ]

    report = _render(
        generated_at=now,
        events=cycle_events,
        escalation_events=escalation_events,
        output_path=output_path,
        source_path=source_path,
        escalation_path=escalation_path,
    )

    assert "- Eskalacje open: 1" in report
    assert "- Eskalacje resolved: 1" in report
    assert "## Eskalacje (status biezacy)" in report
    assert "docs/operations/incidents/a.md" in report
    assert "Status: Warning" in report
