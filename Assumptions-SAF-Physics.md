# AI Agent Environment for Physics (SAF) - Assumptions

- Author: Grzegorz Majewski
- Date: 2026-04-03
- Status: draft

# 1. Definition and goal

AI Agent Environment for Physics (SAF) is an operating model of research work where a team of physicists collaborates with specialized AI agents under an explicit methodological, quality, and compliance order.

This is not just a set of notebooks or a chatbot for reports. It is a multi-agent ecosystem supporting the full research cycle: from hypothesis and study design, through simulation/experiment, to validation and a publishable result.

In SAF:
- the human remains the owner of scientific interpretation, risk assessment, and decisions,
- agents handle repetitive work: literature review, pipeline preparation, data quality checks, statistical tests,
- research artifacts are versioned and auditable,
- decisions are evidence-based, with explicit confidence levels and source traces.

### 1.1 SAF in simple words (for people new to AI)

SAF is an organized way of working where AI is an assistant, not the author of decisions. In practice, you write your notes and derivations in Markdown, while agents only check consistency, search literature, and enforce quality standards. The human always makes the final decision.

A simple analogy: SAF is a team of assistants, each with a clear role. One guards notation consistency, another does a quick literature scan, a third checks whether the result meets quality criteria. There is no "magic" or automatic publishing - there is control and support.

Example workflow:
1. The researcher writes the hypothesis and assumptions in MD.
2. The Discovery agent gathers related works and suggests open questions.
3. The Formal Consistency agent checks that notation is uniform.
4. The Artifact Quality agent assesses whether the material meets Gate 3.
5. The human approves or corrects the result.

Important: agents do not replace the scientist. SAF reduces friction, finds errors faster, and organizes the process.

### 1.2 SAF visualization

![agents](Dokumentacja/SAF_PL.png)

## 2. Business and research goal

Build a repeatable environment that:
- shortens time-to-result for studies,
- improves reproducibility and credibility of results,
- reduces risk of methodological and operational errors,
- eases onboarding of new research teams.

## 3. Problems SAF solves

- Inconsistent research protocols across teams.
- Lack of full reproducibility (parameters, data versions, code versions).
- Difficult traceability: hypothesis -> experiment -> result -> conclusion -> publication decision.
- High manual preparation and reporting effort.
- Knowledge scattered across notebooks, local files, and notes.
- Lack of standardization for uncertainty and data quality assessment.

## 4. Project assumptions

- Human-in-the-loop: critical scientific decisions are made by a human.
- Evidence-based: every conclusion links to data, code, and method.
- Traceability by design: metadata and decisions are required for each artifact.
- Segregation of agent competencies: separate roles for discovery, simulation, statistics, QA.
- Compliance by default: data classification, retention, access control, and audit from the start.
- Iterative: result goes through hypothesis -> validation -> revision.
- Reproducibility first: each result must be reproducible from repo and configuration.
- Markdown-first: key theoretical artifacts are created in Markdown with explicit structure and semantic contracts.
- Semantic control of scientific text: agents verify consistency of definitions, notation, and cross-section dependencies.
- Separation of facts and conclusions: each artifact explicitly marks confidence level and argument status.

## 5. BR/FR/NFR requirements for the environment

### 5.1 BR (Business/Research Requirements)
- BR-01: Reduce time from hypothesis to validated result by at least 30% in pilot.
- BR-02: Maintain reproducibility at >= 90% for pilot studies.
- BR-03: Ensure auditability of decisions and assumptions for each experiment/simulation.

### 5.2 FR (Functional Requirements)
- FR-01: Orchestrator splits research task into streams (discovery, model, data, validation, report).
- FR-02: Agents must generate standardized artifacts: research plan, data plan, validation report.
- FR-03: System must enforce decision logging and confidence level.
- FR-04: System must map traceability: hypothesis -> experiment -> result -> conclusion.
- FR-05: Quality gates must block publication when MUST items are missing.

### 5.3 NFR (Non-Functional Requirements)
- NFR-01: Pipeline run repeatability >= 95%.
- NFR-02: Full versioning of artifacts and input data.
- NFR-03: Access control by role and data classification.
- NFR-04: Auditability of agent operations and configuration changes.
- NFR-05: Validation report preparation time <= 1 business day after run completes.

## 6. SAF competency scope

### 6.1 Exploratory competencies
- Literature analysis and state-of-the-art mapping.
- Identification of hypotheses, constraints, and open questions.

### 6.2 Structuring competencies
- Research plan, concept glossary, and data structure building.
- Simulation/experiment configuration standardization.
- Definition of semantic contracts for theoretical artifacts (definitions, theorems, assumptions, constraints).

### 6.3 Diagnostic competencies
- Detection of data anomalies and methodological errors.
- Sensitivity analysis to parameters.
- Detection of notation inconsistencies, implicit assumptions, and reasoning gaps.

### 6.4 Design competencies
- Generation of experiment/simulation variants.
- Proposal of a minimal set of validation tests.

### 6.5 Control competencies
- Statistical validation, uncertainty, and bias checks.
- Quality gate compliance.
- Formal derivation validation using symbolic tools (CAS) where possible.

### 6.6 Organizational competencies
- Building project memory and decision catalog.
- Detection of study duplication and reuse recommendations.

## 7. SAF architecture - layered model

- Interaction layer: physicist and study lead manage tasks.
- Research orchestrator: plans task DAG and agent sequence.
- Specialist agents: discovery, modeling, simulations, statistics, QA.
- Working and long-term memory: session context and research knowledge base.
- Knowledge repository: literature, notes, protocols, results, decisions.
- Integration layer: HPC, code repository, data storage, publication system.
- Policy layer: data guardrails, retention, access, research ethics.
- Audit layer: logs, versions, quality and reproducibility metrics.

## 8. Roles in the target model

### 8.1 Human roles

- Principal Investigator / Lead Physicist
  - Owner of research goal and scientific decisions.
- Research Physicist
  - Validation of result interpretation and physical model.
- Computational Physicist
  - Responsibility for implementation and compute performance.
- Data Steward
  - Data quality, lineage, retention, classification.
- Statistics Reviewer
  - Verification of statistical tests and uncertainty.
- Security/Compliance Officer
  - Control of regulatory areas and sensitive data.
- Delivery/Operations Manager
  - Planning resource throughput (HPC, storage, timelines).

### 8.2 Agent roles

- Research Orchestrator Agent
  - Mission: manage the research lifecycle from hypothesis to publication.
  - Tasks: split complex physical problems into streams (discovery, model, validation), enforce Quality Gates.
  - Interaction: Your research plan requires Gate 1 approval. Do you want me to launch the Discovery Agent now?
- Scientific Discovery Agent
  - Mission: map knowledge landscape and identify research gaps.
  - Tasks: literature analysis (ArXiv), open questions, hypothesis map in MD.
  - Interaction: I found three conflicting hypotheses about vacuum energy in your model. Here is a comparison.
- Physical Model Agent
  - Mission: guardian of formal and physical correctness.
  - Tasks: LaTeX equation verification, assumption checks (e.g., conservation laws), boundary conditions.
  - Interaction: Equation (4.2) is missing the relativistic factor $\gamma$, which is inconsistent with your assumption $v \approx c$.
- Simulation/Experiment Agent
  - Mission: design numerical verification for theory.
  - Tasks: propose test runs and parameter configurations.
  - Interaction: To check stability, I propose 100 Monte Carlo simulations over $T \in [0, 100] K$.
- Data Quality Agent
  - Mission: detect anomalies in input and output data.
  - Tasks: missing values, outliers, drift in time series.
  - Interaction: Dataset result_v1.csv has 5% NaN in momentum column. Recommend recalibration.
- Statistics and Uncertainty Agent
  - Mission: quantify confidence of scientific results.
  - Tasks: test selection, confidence intervals, sensitivity analysis.
  - Interaction: With current sample size, CI for particle mass is $\pm 12\%$. Is that acceptable?
- Risk and Compliance Agent
  - Mission: mitigate methodological and operational risks.
  - Tasks: regulatory/ethical risk, data retention compliance.
  - Interaction: Warning: external data require CC-BY license. Add citation.
- Artifact Quality Agent
  - Mission: final quality check before release.
  - Tasks: cross-file consistency, pass/pass-with-comments/fail status.
  - Interaction: Status: pass-with-comments. All tests passed, but systematic uncertainty is missing.
- Knowledge Repository Agent
  - Mission: institutional memory and reuse.
  - Tasks: result indexing, reuse opportunities.
  - Interaction: A similar model was tested in project DarkMatter_2024. Check conclusions there.
- Formal Consistency Agent
  - Mission: guardian of notation and logic.
  - Tasks: ensure definitions (e.g., $\hbar=1$) are consistently used across MD.
  - Interaction: You use signature $(-,+,+,+)$ in Metric, but Lagrangian suggests $(+,-,-,-)$. Please unify.
- Cross-Reference Agent
  - Mission: real-time literature linkage.
  - Tasks: map MD fragments to ArXiv/ADS, identify similarities and differences.
  - Interaction: Your energy-momentum tensor derivation matches Smith (2025). Add reference?
- Socratic Mentor Agent
  - Mission: critical sparring partner (Reviewer #2).
  - Tasks: boundary cases, singularities, logical consequences.
  - Interaction: What happens when mass goes to infinity? Does it create an unphysical singularity at $r=0$?

### 8.3 LTR profile (hybrid mode)

- Default mode: hybrid (switchable at file and section level).
- Section tags: [TRYB: FORMALNY] and [TRYB: BADACZ].
- Formal validation: medium strictness, CAS SymPy for critical steps.
- LTR artifacts: semantic contract, derivation report, formal validation log, Gate 3 checklist (theory), notation map, cross-reference log.

## 9. Human-agent collaboration model

- Human defines research goal, constraints, and success criteria.
- Orchestrator creates stream plan and runs specialist agents.
- Agents generate working artifacts and open questions.
- Human approves methods, rejects low-confidence content, and finalizes results.
- Quality agent runs quality gate before publication.

### Three levels of acceptance
- Working acceptance: Lead Physicist/Research Physicist.
- Methodological acceptance: Statistics Reviewer/Computational Physicist.
- Compliance acceptance: Security/Compliance for sensitive/regulatory data.

## 10. Quality gates for research

### Gate 1 - Project readiness
- Hypothesis and measurable goal are explicit.
- Scope and exclusions are documented.
- Experiment/simulation plan is complete.
- Traceability from hypothesis to metrics is defined.
- Acceptance: human only (Principal Investigator).

### Gate 2 - Data and method readiness
- Data classification and processing basis confirmed.
- Access control and retention defined.
- Methodological and operational risk has an owner and mitigation plan.
- Acceptance: human only (Principal Investigator).

### Gate 3 - Result quality
- Result is reproducible (code, data, parameters, versions).
- Uncertainty and sensitivity are computed and described.
- Conclusions separated from facts, confidence explicit.
- For theory: derivation reproducible from explicit assumptions, definitions, lemmas.
- For theory: no notation/definition contradictions across sections.
- For theory: key algebraic steps validated by CAS or flagged for manual review.
- Acceptance: agent-conditional pass possible for low-risk results, only if Artifact Quality Agent returns pass with no critical comments.

### Gate 4 - Publication/transfer
- Decisions and approvals complete.
- Artifact meets org reporting requirements.
- Rollback/contingency plan exists for high-risk research.
- Acceptance: human + Statistics Reviewer.

## 11. Minimal artifacts to start

1. Study card (goal, scope, hypothesis, owners).
2. Research Design (model, methods, parameters, constraints).
3. Data plan (sources, classification, retention, access).
4. Validation plan (tests, metrics, pass/fail criteria).
5. Decision and risk log.
6. Result report (facts, analysis, uncertainty, recommendation).
7. Theoretical semantic contract (definitions, theorems, assumptions, constraints).
8. Formal validation log (CAS status, manual checks, uncertain steps).

## 12. Literate Theoretical Research (LTR) - clarifications

LTR assumes that core derivations and arguments are created as Markdown artifacts and the agent system enforces semantic consistency.

### Semantic contracts (Markdown-first)
- Definitions: every new symbol or object has an explicit definition.
- Theses/Theorems: explicit scope, conditions, and status (draft/verified).
- Proofs: steps marked, including points requiring CAS or manual review.
- Constraints: explicit boundary conditions and scope of applicability.

### LTR - quality controls
- Mathematical lint: detect logical jumps, notation changes, missing boundary conditions.
- Dimensional analysis: automatic unit checks where possible.
- Literature cross-reference: mark similarities and differences with existing works.

### LTR - mitigation of "Parsed Math"
- CAS integration (e.g., SymPy/WolframAlpha) as a condition for confirming key transformations.
- Enforced stepwise derivations in critical fragments.

### LTR examples
- Equation tagging:
  $$E = mc^2$$
  [EQ:ENERGY-01]
- Step requiring validation: [VERIFY-CAS] on nontrivial transformation.
- Related artifacts (format [ID:Type]): [LTR-DERIV-001:Report], [LTR-VAL-001:Validation].
- Global unit assumptions: c=1, hbar=1 in notation map.

## 13. Pilot scope and LTR policies (v1)

### Pilot scope (2-3 theoretical cases)
- Case A (analytical): derive a new correction to existing Lagrangian; goal: notation consistency and no algebraic copy-paste errors.
- Case B (numerical-theoretical): validate analytic solution stability with simple scripts (e.g., Python/SymPy); goal: integrate model agent with simulation agent.
- Case C (review/hypothesis): synthesize a new hypothesis from 20 latest ArXiv preprints; goal: test Discovery and Cross-Reference agents.

### Artifact examples per case
- Case A (analytical)
  - Semantic contract: [LTR-CONTRACT-A01:Contract]
  - Derivation report: [LTR-DERIV-A01:Report]
  - Validation log: [LTR-VAL-A01:Validation]
  - Notation map: [LTR-NOT-A01:Notation]
  - Tag example: $$\Delta\mathcal{L} = \alpha R^2$$
    [EQ:DL-01]
    [VERIFY-CAS]
- Case B (numerical-theoretical)
  - Derivation report: [LTR-DERIV-B01:Report]
  - Validation log: [LTR-VAL-B01:Validation]
  - Cross-reference log: [LTR-XREF-B01:CrossRef]
  - Example relations: [LTR-DERIV-B01:Report], [LTR-VAL-B01:Validation], [LTR-XREF-B01:CrossRef]
- Case C (review/hypothesis)
  - Semantic contract: [LTR-CONTRACT-C01:Contract]
  - Cross-reference log: [LTR-XREF-C01:CrossRef]
  - Gate 3 checklist: [LTR-G3-C01:Gate3]
  - Literature tag example: arXiv:2026.12345 (preprint)

### Formalization levels
- Researcher mode (discovery): loose MD notes, no full traceability; agents act as Socratic Mentors.
- Formal mode (validation/CAS): required from Research Design freeze; each equation has confidence level and source.

### Validation and CAS rules
- Key step: any nontrivial mathematical transition is tagged [VERIFY-CAS].
- Formal Consistency Agent sends tagged fragments for validation (SymPy or other CAS).
- Missing validation: mark in metadata as unverified and show in report.

### Literature workflow
- Sources: priority ArXiv (preprints) and ADS/DOI (peer-reviewed).
- Format: BibTeX integrated with MD files.
- Confidence: agents distinguish preprint vs peer-reviewed and flag conclusions based only on preprints.
- PDF: input documents are read and indexed (text-layer extraction; OCR optional for scans) so agents can access content.

### Data policy (LtrDataPolicy)
- Classification: public (literature), internal (notes), confidential (pre-publication discoveries).
- Retention: research artifacts stored 5-10 years.
- Licenses: simulation code MIT/GPL, MD content CC-BY-NC-ND.

### Repository standard
- Structure: consistent with v1 scheme (Documentation/Templates/Agents).
- Naming: semantic versioning (e.g., Hypothesis-v1.2.0-alpha).
- Decisions: recorded in DECISIONS.md with commit links.

## 14. Repository structure (v1)

```text
DECISIONS.md
README.md
requirements.txt
Dokumentacja/
  Zalozenia-Srodowisko-Fizyka.md
  Szablon-Fizyka/
    Standard-Operacyjny-Badania.md
    Standard-Operacyjny-Research-Design.md
    Checklista-Research-Gate.md
    Sekcje-Akceptacje-Decyzje.md
    README.md
  Szablon-LTR/
    README.md
    Kontrakt-Semantyczny-LTR.md
    Raport-Wyprowadzen-LTR.md
    Rejestr-Walidacji-Formalnej-LTR.md
    Checklista-Gate3-Teoria-LTR.md
    Mapa-Notacji-LTR.md
    Cross-Reference-Log-LTR.md
.github/
  copilot-instructions.md
  agents/
    research-orkiestrator.agent.md
    physics-discovery.agent.md
    model-review.agent.md
    simulation-experiment.agent.md
    data-quality.agent.md
    statistics-review.agent.md
    risk-compliance.agent.md
    artifact-quality.agent.md
    knowledge-repo.agent.md
    formal-consistency.agent.md
    cross-reference.agent.md
    socratic-mentor.agent.md
  prompts/
    kickoff-badania.prompt.md
    review-jakosci-badania.prompt.md
    konfigurator-projektu-badawczego.prompt.md
Case-Template/
  Artefakty/
  Notatki/
  Dane/
  Wyniki/
  Bibliografia/
```

## 15. Implementation plan (proposal)

### Stage 1 (0-2 months): Standardization
- Define artifact templates and concept glossary.
- Select 2-3 pilot scenarios.

### Stage 2 (2-4 months): Pilot
- Run orchestrator + 3 agents (discovery, data quality, statistics).
- Measure time and quality vs traditional approach.

### Stage 3 (4-8 months): Governance
- Enable quality gates, audit, retention, access control.
- Finalize acceptance policy (human-only vs agent-conditional).

### Stage 4 (8-12 months): Scaling
- Extend agent catalog and integrate with HPC/repo.
- Launch knowledge memory and reuse patterns.

## 16. Success metrics

### Efficiency
- Time-to-Result: reduction >= 30% in pilot.
- Validation report lead time: <= 1 day.

### Quality
- Reproducibility Score: >= 90%.
- Consistency Score for artifacts: >= 85%.
- Runs requiring re-run for quality reasons: < 15%.
- Share of theoretical derivations with formal validation: >= 70% in pilot.
- Agents detect at least 1 formal/arithmetical error before Gate 3.
- Another physicist can reproduce reasoning and computations within < 2h.

### Organizational
- Reuse rate of methods and artifacts: >= 25%.
- Scientific stakeholder CSAT: >= 4.2/5.

## 17. Risks and mitigations

### Business risks
- Low adoption by teams.
- Mitigation: pilot on real use-cases with measurable KPIs.

### System risks
- Lack of reproducibility due to inconsistent runtime environments.
- Mitigation: runtime standardization, version locking, containerization.

### Regulatory risks
- Unauthorized processing of sensitive data.
- Mitigation: data classification, access control, audit and approvals.

### Operational risks
- MUST blockers without owner and SLA.
- Mitigation: RACI + escalation SLA, blockage log and review.

### LTR risks (Literate Theoretical Research)
- Incorrect tagging of equations and artifacts (missing [EQ:ID], invalid [ID:Type]).
- Mitigation: template validation, tag lint, Gate 3 checklist.
- False positive CAS validation or missing boundary conditions.
- Mitigation: require justification, mark steps unverified, manual review of key steps.
- Notation inconsistencies from hybrid mode.
- Mitigation: notation map + global unit assumptions + Formal Consistency Agent.
- Overreliance on non-peer-reviewed literature (preprints).
- Mitigation: mark confidence level, flag conclusions based only on preprints.

## 18. Required decisions and owners

1. Acceptance model (human-only vs agent-conditional).
- Business owner: Principal Investigator / Business Owner.
- Technical owner: Lead Physicist + Security/Compliance.

2. Data scope allowed for agent work.
- Business owner: Data Owner.
- Technical owner: Data Steward + Security.

3. Minimal set of quality gate metrics.
- Business owner: Lead Physicist.
- Technical owner: Statistics Reviewer.

## 19. Compliance section (minimum)

- Data classification: public/internal/confidential/restricted.
- Processing basis: description and owner.
- Retention and deletion: period, mechanism, owner.
- Access control: roles and permissions.
- Auditability: what we log, where, for how long.
- Approval roles: Business, Security, Compliance.
- Regulatory risk level: low/medium/high.
- Rollback and contingency plan: required for high-risk research.

## 20. Acceptances

- Acceptance status: draft
- Acceptance type: TO FILL
- Business owner: TO FILL
- Technical owner: TO FILL
- Security/Compliance: TO FILL
- Last updated: 2026-04-03

## 21. Decisions

| ID | Decision | Business rationale | Technical rationale | Owner | Date | Related requirement | Related risk | Status |
|---|---|---|---|---|---|---|---|---|
| DEC-001 | Launch SAF pilot for 2-3 research cases | Reduce time and improve quality | Validate work model before scaling | Grzegorz Majewski | 2026-04-03 | BR-01, BR-02 | R-OPS-01 | open |
| DEC-002 | Add reproducibility quality gate before publication | Limit risk of wrong conclusions | Check reproducibility of results and configs | Grzegorz Majewski | 2026-04-03 | FR-05, NFR-01 | R-SYS-01, R-REG-01 | open |
| DEC-003 | Define agent acceptance policy | Clear responsibility and audit | Orchestrator and escalation consistency | Grzegorz Majewski | 2026-04-03 | FR-03 | R-OPS-02 | open |
</attachment>
</attachments>
<context>
The current date is 8 kwietnia 2026.
There have been some changes between the last request and now.
Some edits were made, by the user or possibly by a formatter or another automated tool, to:
- d:\grzegorz\programowanie\Theoretical MD\README.md
So be sure to check the current file contents before making any new edits.
Terminals:
Terminal: powershell
Last Command: & "d:\grzegorz\programowanie\Theoretical MD\.venv\Scripts\Activate.ps1"
Cwd: D:\grzegorz\programowanie\Theoretical MD
Exit Code: 0
Terminal: powershell
Last Command: & "d:\grzegorz\programowanie\Theoretical MD\.venv\Scripts\Activate.ps1"
Cwd: D:\grzegorz\programowanie\Theoretical MD
Exit Code: 0
Terminal: powershell
Last Command: & "d:\grzegorz\programowanie\Theoretical MD\.venv\Scripts\Activate.ps1"
Cwd: D:\grzegorz\programowanie\Theoretical MD
Exit Code: 0
Terminal: powershell
Last Command: & "d:\grzegorz\programowanie\Theoretical MD\.venv\Scripts\Activate.ps1"
Cwd: D:\grzegorz\programowanie\Theoretical MD
Exit Code: 0
Terminal: powershell
Last Command: & "d:\grzegorz\programowanie\Theoretical MD\.venv\Scripts\Activate.ps1"
Cwd: D:\grzegorz\programowanie\Theoretical MD
Exit Code: 0
Terminal: powershell
Last Command: & "d:\grzegorz\programowanie\Theoretical MD\.venv\Scripts\Activate.ps1"
Cwd: D:\grzegorz\programowanie\Theoretical MD
Exit Code: 0

</context>
<editorContext>
The user's current file is d:\grzegorz\programowanie\Theoretical MD\Zalozenia-Srodowisko-Fizyka.md. The current selection is from line 34 to line 34.
</editorContext>
<reminderInstructions>

</reminderInstructions>
<userRequest>
Przygotuj wersję angielską dokumentu Zalozenia-Srodowisko-Fizyka.md
</userRequest>
```

Please note: The assistant has moved from the previous response into a new conversation turn. This prompt is a continuation with no overlapping messages. Some of the state is in the attachments. Please rely on that for context. The user's original request is: "Przygotuj wersję angielską dokumentu Zalozenia-Srodowisko-Fizyka.md".
