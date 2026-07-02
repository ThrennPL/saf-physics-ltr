# Compatibility Matrix (Etap G2)

Data: 2026-07-02
Status: active
Wersja: 1.0.0
Owner: Technical Developer
Pewnosc: 0.93

## Cel

Utrzymac jawna kompatybilnosc miedzy rolami agentow, skillami i kontraktami narzedzi.

Legenda:
- stable: kontrakt obecny i uzywany operacyjnie
- candidate: kontrakt zdefiniowany, wdrozenie czesciowe
- partial: kontrakt istnieje, ale przeplyw wymaga kroku manualnego (HITL)

## Macierz Agent -> Skill

| Agent | Skill | Status |
|---|---|---|
| Research Orchestrator | SK-008 Operations Governance Skill | stable |
| Research Orchestrator | SK-010 Metrics and Timing Skill | stable |
| Formal Consistency | SK-001 Notation Consistency Skill | stable |
| Model Review | SK-002 Mathematical Validation Skill | stable |
| Cross-Reference | SK-003 Literature Search Skill | stable |
| Data Quality | SK-004 Data Provenance Skill | stable |
| Risk Compliance | SK-005 Risk Sanity Skill | stable |
| Artifact Quality | SK-006 Evidence Packaging Skill | stable |
| Technical Developer | SK-007 Process Suite Skill | stable |
| Simulation/Experiment | SK-009 Chart and Manuscript Skill | candidate |

## Macierz Skill -> Tool

| Skill | Tool contracts | Status |
|---|---|---|
| SK-001 | Tool.LintLTR, Tool.DefinitionConsistency | stable |
| SK-002 | Tool.CASValidate, Tool.BinetNumericValidation | stable |
| SK-003 | Tool.ArxivSearch, Tool.AdsSearch | stable |
| SK-004 | Tool.ParameterProvenance | stable |
| SK-005 | Tool.SecuritySanity, Tool.TaxonomyGuard | stable |
| SK-006 | Tool.EvidencePacket, Tool.ReviewTraceability | stable |
| SK-007 | Tool.ProcessSuite, Tool.ContractGuard, Tool.RouteModel | stable |
| SK-008 | Tool.OpsCycleRunner, Tool.OwnerWeeklySummary, Tool.OpsHealthSnapshot, Tool.EscalationQueueManager, Tool.EscalationNotifier | stable |
| SK-009 | Tool.GenerateT04Charts, Tool.ChartPipelineCheck, Tool.ManuscriptCompleteness, Tool.ManuscriptSplitter | candidate |
| SK-010 | Tool.MigrationMetricsReport, Tool.GateTimingLogger, Tool.McpBaseline | stable |

## Krytyczne flow coverage

| Metryka | Wartosc |
|---|---|
| Liczba krytycznych flow | 10 |
| Flow stable/full | 9 |
| Flow partial (HITL) | 1 |
| Coverage stable/full | 90% |

Wniosek:
- Kryterium done Iteracji G2 (>=80% mapowalnosci Agent -> Skill -> Tool) jest spelnione.

## Reguly utrzymania

1. Kazda zmiana kontraktu w tool-contracts-registry musi aktualizowac ta macierz.
2. Spadek coverage stable/full ponizej 80% powoduje status Warning i wymaga planu korekcyjnego.
3. Brak mapowania dla krytycznego flow powoduje Blocker i fail_closed.
