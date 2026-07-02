# Skill Contracts Registry (Etap G2)

Data: 2026-07-02
Status: active
Wersja: 1.0.0
Owner: Orkiestrator
Pewnosc: 0.94

## Cel

Zdefiniowac wspolny katalog kontraktow Skills ponad narzedziami z katalogu tools/.

## Artefakt wykonawczy (machine-readable)

Wykonawcze definicje kontraktow skills sa utrzymywane w:
- `mcp/skills/skill_catalog.json`

Walidacja automatyczna:
- `python tools/contract_guard.py`

Ten rejestr markdown jest warstwa opisowa; source-of-truth dla runtime kontraktow skills to plik JSON.

Uruchamianie chain skillowego (adapter wykonawczy):
- lista skills: `python tools/skill_runner.py list`
- plan chain: `python tools/skill_runner.py plan --skill-id SK-007`
- dry-run chain: `python tools/skill_runner.py run --skill-id SK-007 --dry-run`

## Standard kontraktu Skill

Kazdy skill musi deklarowac:
1. Skill ID i owner.
2. Input contract.
3. Output contract.
4. Error contract.
5. Zaleznosci do instructions.
6. Zaleznosci do tool contracts.

Wspolny output contract:
1. status: OK/Warning/Blocker
2. summary: krotki opis wyniku
3. diagnostics: lista wpisow diagnostycznych
4. confidence: liczba 0-1
5. questions: lista Q-XXX (jesli dotyczy)

Wspolny error contract:
1. code
2. reason
3. recoverable (true/false)
4. escalation_required (true/false)

## Rejestr Skills

| Skill ID | Nazwa | Owner | Input contract | Output contract | Error contract | Tool contracts |
|---|---|---|---|---|---|---|
| SK-001 | Notation Consistency Skill | Formal Consistency | artifact_paths[], notation_map_ref | standard skill output | standard skill error | Tool.LintLTR, Tool.DefinitionConsistency |
| SK-002 | Mathematical Validation Skill | Model Review | equations_ref, validation_profile | standard skill output | standard skill error | Tool.CASValidate, Tool.BinetNumericValidation |
| SK-003 | Literature Search Skill | Cross-Reference | query, sources[], filters | standard skill output + citations[] | standard skill error | Tool.ArxivSearch, Tool.AdsSearch |
| SK-004 | Data Provenance Skill | Data Quality | data_artifacts[], scope | standard skill output | standard skill error | Tool.ParameterProvenance |
| SK-005 | Risk Sanity Skill | Risk Compliance | governance_artifacts[] | standard skill output + risks[] | standard skill error | Tool.SecuritySanity, Tool.TaxonomyGuard |
| SK-006 | Evidence Packaging Skill | Artifact Quality | gate_id, owner, decision, artifacts[] | standard skill output + packet_path | standard skill error | Tool.EvidencePacket, Tool.ReviewTraceability |
| SK-007 | Process Suite Skill | Technical Developer | config_path, cycle_mode | standard skill output + per_check_result[] | standard skill error | Tool.ProcessSuite, Tool.ContractGuard |
| SK-008 | Operations Governance Skill | Research Orchestrator | cycle_type, log_paths[] | standard skill output + operations_snapshot | standard skill error | Tool.OpsCycleRunner, Tool.OwnerWeeklySummary, Tool.OpsHealthSnapshot, Tool.EscalationQueueManager |
| SK-009 | Chart and Manuscript Skill | Simulation/Experiment | dataset_ref, chart_spec, manuscript_ref | standard skill output + artifact_index | standard skill error | Tool.GenerateT04Charts, Tool.ChartPipelineCheck, Tool.ManuscriptCompleteness, Tool.ManuscriptSplitter |
| SK-010 | Metrics and Timing Skill | Research Orchestrator | case_id, gate_events[] | standard skill output + metrics_report | standard skill error | Tool.MigrationMetricsReport, Tool.GateTimingLogger |

## Krytyczne flow: Agent -> Skill -> Tool

| Flow ID | Krytyczny przeplyw | Agent | Skill chain | Tool chain | Mapowalnosc |
|---|---|---|---|---|---|
| CF-01 | Gate pre-check quality | Artifact Quality | SK-007 -> SK-005 | Tool.ProcessSuite -> Tool.ContractGuard -> Tool.SecuritySanity -> Tool.TaxonomyGuard | full |
| CF-02 | Evidence packet gate | Artifact Quality | SK-006 | Tool.EvidencePacket -> Tool.ReviewTraceability | full |
| CF-03 | Walidacja formalna | Formal Consistency | SK-001 -> SK-002 | Tool.LintLTR -> Tool.DefinitionConsistency -> Tool.CASValidate | full |
| CF-04 | Walidacja literaturowa | Cross-Reference | SK-003 | Tool.ArxivSearch -> Tool.AdsSearch | full |
| CF-05 | Jakosc danych i pochodzenie | Data Quality | SK-004 | Tool.ParameterProvenance | full |
| CF-06 | Proces suite T04 | Technical Developer | SK-007 -> SK-009 | Tool.ProcessSuite -> Tool.GenerateT04Charts -> Tool.ChartPipelineCheck | full |
| CF-07 | Governance tygodniowy | Research Orchestrator | SK-008 | Tool.OpsCycleRunner -> Tool.OwnerWeeklySummary -> Tool.OpsHealthSnapshot | full |
| CF-08 | Lifecycle eskalacji | Risk Compliance | SK-008 | Tool.EscalationNotifier -> Tool.EscalationQueueManager | full |
| CF-09 | Telemetria gate i migracji | Research Orchestrator | SK-010 | Tool.GateTimingLogger -> Tool.MigrationMetricsReport | full |
| CF-10 | Decyzja GO/NO-GO HITL | Human Owner | SK-006 + review | Tool.EvidencePacket (input only) | partial (HITL required) |

## Pokrycie kryterium done G2

Metryka mapowalnosci krytycznych flow:
- full: 9
- partial (HITL): 1
- coverage full = 9/10 = 0.90

Wniosek:
- Kryterium done Iteracji G2 (minimum 80%) jest spelnione.
