# Tool Contracts Registry (Etap G2)

Data: 2026-07-02
Status: active
Wersja: 1.0.0
Owner: Technical Developer
Pewnosc: 0.95

## Cel

Ujednolicic kontrakty I/O dla narzedzi wykonawczych w katalogu tools/.

## Artefakt wykonawczy (machine-readable)

Wykonawcze mapowanie kontraktow tools jest utrzymywane w:
- `mcp/tools/tool_contract_index.json`

Walidacja automatyczna:
- `python tools/contract_guard.py`

Ten rejestr markdown jest warstwa opisowa; source-of-truth dla runtime mapowania tools to plik JSON.

## Wspolny minimalny output contract

1. status: OK/Warning/Blocker
2. summary
3. diagnostics[]
4. metadata: {timestamp, tool_version, params_hash}

## Wspolny minimalny error contract

1. code
2. reason
3. recoverable
4. escalation_required

## Rejestr kontraktow narzedzi

| Tool contract | Implementacja | Input contract | Output contract | Error contract | Krytycznosc |
|---|---|---|---|---|---|
| Tool.ArxivSearch | tools/arxiv_search.py | query, max_results, categories | citations[] + status | source_unavailable | high |
| Tool.AdsSearch | tools/ads_search.py | query, max_results, ADS_API_TOKEN(optional) | citations[] + status | auth_or_source_unavailable | high |
| Tool.LintLTR | tools/lint_ltr.py | artifact_paths[], lint_profile | findings[] + status | invalid_artifact | high |
| Tool.CASValidate | tools/cas_test_harness.py | equations_ref, test_profile | cas_results[] + status | cas_failure | high |
| Tool.BinetNumericValidation | tools/binet_numeric_validation_t04.py | scenario_config | numeric_validation[] + status | numeric_instability | medium |
| Tool.DefinitionConsistency | tools/definition_consistency_check.py | artifact_paths[], notation_map | definition_findings[] + status | missing_definition_map | high |
| Tool.ParameterProvenance | tools/parameter_provenance_check.py | data_artifacts[] | provenance_findings[] + status | missing_metadata | high |
| Tool.SecuritySanity | tools/security_sanity_check.py | workspace_scope | security_findings[] + status | security_check_failed | high |
| Tool.TaxonomyGuard | tools/taxonomy_guard.py | artifact_paths[] | taxonomy_findings[] + status | taxonomy_drift | high |
| Tool.ContractGuard | tools/contract_guard.py | contract_scope, policy_refs | contract_findings[] + status | contract_violation | high |
| Tool.EvidencePacket | tools/build_evidence_packet.py | gate_id, owner, decision, artifacts[] | packet_path, manifest, status | invalid_manifest | high |
| Tool.ReviewTraceability | tools/review_traceability_generator.py | review_artifacts[] | traceability_report + status | missing_trace_link | medium |
| Tool.ProcessSuite | tools/process_suite_runner.py | config_path, output_path | status_report, per_check_result[] | check_failed | high |
| Tool.McpBaseline | tools/mcp_baseline.py | baseline_config | baseline_status, findings[] | baseline_error | medium |
| Tool.RouteModel | tools/route_model.py | task_type, risk_level, gate_id | model_decision + status | invalid_routing_rule | medium |
| Tool.MigrationMetricsReport | tools/migration_metrics_report.py | source_logs[] | migration_metrics_report + status | incomplete_metrics_data | medium |
| Tool.GateTimingLogger | tools/gate_timing_logger.py | case_id, gate_event | timing_log_update/report | invalid_gate_event | medium |
| Tool.OpsCycleRunner | tools/ops_cycle_runner.py | cycle(pr/48h/weekly), metadata | cycle_summary + status | cycle_blocker | high |
| Tool.OwnerWeeklySummary | tools/owner_weekly_summary.py | operations_logs[] | owner_summary + status | summary_generation_failed | medium |
| Tool.OpsHealthSnapshot | tools/ops_health_snapshot.py | operations_logs[], scheduler_state | health_snapshot_txt_json + status | snapshot_failed | medium |
| Tool.EscalationNotifier | tools/escalation_notifier.py | incident_metadata | escalation_event + status | queue_write_failed | high |
| Tool.EscalationQueueManager | tools/escalation_queue_manager.py | action(list/ack/resolve), incident_path | queue_state + status | invalid_transition | high |
| Tool.GenerateT04Charts | tools/generate_t04_charts.py | input_dataset, chart_spec | chart_artifacts[] + status | chart_generation_failed | medium |
| Tool.ChartPipelineCheck | tools/chart_artifact_pipeline_check.py | chart_artifacts[] | chart_pipeline_report + status | chart_missing | medium |
| Tool.ManuscriptCompleteness | tools/manuscript_completeness_check.py | manuscript_path | completeness_report + status | manuscript_incomplete | low |
| Tool.ManuscriptSplitter | tools/manuscript_supplement_splitter.py | manuscript_path, split_rules | split_artifacts + status | split_failed | low |

## Zasady kompatybilnosci

1. Narzedzia deklarowane jako high musza miec mapowanie do co najmniej jednego skillu krytycznego.
2. Zmiana input/output/error contract wymaga aktualizacji compatibility-matrix.
3. Narzedzia nie podejmuja decyzji gate, tylko dostarczaja dane decyzyjne.
