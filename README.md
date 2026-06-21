# SAF Physics LTR ⚛️ **Science 2.0 Operating System**

**Multi-agent research platform** for SAF/LTR workflows in theoretical physics.
✅ Human-in-the-loop quality gates | Formal consistency checks | Literature cross-reference
⭐ **Fork, star, contribute!**

![SAF Architecture](Dokumentacja/SAF.png)

## Quickstart
```bash
git clone https://github.com/ThrennPL/saf-physics-ltr
cd saf-physics-ltr
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Optional: developer dependencies (lint/test/typecheck/build)
pip install -r requirements-dev.txt

# Optional: enable pre-commit MCP drift gate
pre-commit install

# Optional: ADS token
# Copy .env.example to .env and fill ADS_API_TOKEN

# Security/MCP sanity check
python tools/security_sanity_check.py

# First agent run
python tools/arxiv_search.py "lagrangian stability" --max 5
```

## Minimal Inputs (Required to Start)
- Hypothesis and research goal.
- Scope and exclusions.
- Research variant (theoretical/experimental/computational).
- Critical assumptions.
- Filled `Dokumentacja/Karta-Badania.md`.

## Why SAF?
**Theoretical physics research problems solved:**
- Inconsistent notation → **Agent Formal Consistency**
- Literature gaps → **ArXiv/ADS Discovery Agent**
- Reproducibility issues → **LTR validation and formal checks**
- Gate review delays → **Automated Quality Gates G1-G4**

## Core Architecture
13 Specialized Agents:
- Research Orchestrator: routes workstreams, coordinates gate transitions, aggregates statuses.
- Formal Consistency: validates notation/ID consistency and resolves notation conflicts.
- Model Review: resolves physical and domain-level conflicts.
- Physics Discovery: frames discovery directions and research questions.
- Cross-Reference: executes ArXiv/ADS literature linkage and evidence mapping.
- Data Quality: validates dataset quality before uncertainty analysis.
- Statistics Review: evaluates uncertainty/CI and inference robustness.
- Risk & Compliance: tracks risk posture and fail-closed conditions.
- Simulation/Experiment: prepares executable variants and reproducibility checks.
- Artifact Quality: consolidates outputs into gate-ready evidence packets.
- Knowledge Repo: normalizes terminology and reuse taxonomy.
- Language Polish Quality: mandatory PL editorial validation before finalization/PDF.
- Technical Developer: code patches, automation, and tooling incident handling.

## Orchestration Flow
Default execution order and hard dependencies:
1. Collect required artifacts and case context packs.
2. Run `Formal Consistency -> Model Review` (hard order).
3. Run `Data Quality -> Statistics Review` (hard order).
4. Run `Discovery -> Cross-Reference` for literature scope and links.
5. Run `Language Polish Quality` before final document/package export.
6. Run `Risk & Compliance` in parallel and escalate critical findings.
7. Run `Artifact Quality` to consolidate statuses and recommendation.
8. Human decision for Gate 1/2/4; Gate 3 can be conditional only under low risk.

Escalation rules:
- Any `Blocker` or unresolved conflict is escalated to Orchestrator and then to human.
- Missing required inputs triggers fail-closed behavior.

## Repository Structure

Dokumentacja/ # Templates and registers
├── Karta-Badania.md
├── Rejestr-Konfiguracji-Projektu.md
├── Rejestr-Konfliktow-i-Eskalacji.md
├── Konsolidacja-Statusow.md
├── Review-Jakosci-Gate3.md
├── Podsumowanie-Gate.md
└── Szablon-LTR/ # Literate Theoretical Research templates
Case-Template/ # New research case pattern
.github/agents/ # Agent role configurations
.github/prompts/ # Helper prompts
tools/ # CLI utilities (lint, ArXiv/ADS, model routing)

## Key Files
- **Core Design**: `Assumptions-SAF-Physics.md`
- **PL Assumptions**: `Zalozenia-Srodowisko-Fizyka.md`
- **Decisions Log**: `DECISIONS.md`
- **Agent Config**: `.github/agents/*`
- **Usage Guide**: `Dokumentacja/Instrukcja-Uzycia.md`
- **System Docs**: `Dokumentacja/Dokumentacja-Systemowa.md`

## Tech Stack

Python 3.11+ (recommended 3.13) | pypdf | sympy | bibtexparser | networkx
pillow | pytesseract | chromadb | crossrefapi | graphviz


## LTR Lint (Mathematical Consistency)
```bash
# Basic validation
python tools/lint_ltr.py

# Fail on warnings (CI/CD)
python tools/lint_ltr.py --fail-on-warning
```

## ArXiv Cross-Reference
```bash
# Semantic literature search
python tools/arxiv_search.py "CPT violation" --max 10 --cat hep-th
```

## ADS Cross-Reference (token required)
```bash
# Requires ADS_API_TOKEN in .env
python tools/ads_search.py "CPT violation" --max 10
```

## Model Routing
```bash
# Route tasks to optimal models
python tools/route_model.py cross-reference
python tools/route_model.py model-review --gate 3
```

## Reporting Standard
- Status: OK / Warning / Blocker
- Confidence: 0-1 numeric
- Questions: Q-XXX with priority (low/medium/high)

## Prompts
- `.github/prompts/kickoff-badania.prompt.md`
- `.github/prompts/konfigurator-projektu-badawczego.prompt.md`
- `.github/prompts/review-jakosci-badania.prompt.md`
- `.github/prompts/eskalacja-konfliktow.prompt.md`
- `.github/prompts/konsolidacja-statusow.prompt.md`
- `.github/prompts/podsumowanie-gate.prompt.md`

## Pilot Case: T03 Newton-Yukawa Orbit Stability
The team prepared a full pilot case under `Badania/T03-Newton-Yukawa-Orbit-Stability`.

Scientific summary:
- Objective: verify whether a weak Yukawa correction changes local stability of circular orbits.
- Main result: local stability condition
	$1+\beta e^{-x}(1+x-x^2)>0$, where $x=r_c/\lambda$.
- Outcome: baseline Newtonian limit recovered for `beta = 0`; sign impact depends on `(1+x-x^2)`.

Technical summary:
- End-to-end artifact chain completed (research card, derivation, validation register, risk pack, gate checklists).
- Formal validation includes manual checks and CAS closure (`SymPy`, K5 `[VERIFY-CAS]` closed).
- Human-in-the-loop gate decisions recorded as approved for Gate 1-4.

Recommended entry points:
- `Badania/T03-Newton-Yukawa-Orbit-Stability/00-MAPA-CZYTANIA-RECENZJA.md`
- `Badania/T03-Newton-Yukawa-Orbit-Stability/Raport-Wynikowy.md`
- `Badania/T03-Newton-Yukawa-Orbit-Stability/Raport-Wyprowadzen-LTR.md`
- `Badania/T03-Newton-Yukawa-Orbit-Stability/Rejestr-Walidacji-Formalnej-LTR.md`
- `Badania/T03-Newton-Yukawa-Orbit-Stability/Akceptacje-Decyzje.md`

## OCR Requirements
**Tesseract required** (`pytesseract` wrapper only):
```bash
# Ubuntu/Debian
sudo apt install tesseract-ocr

# macOS
brew install tesseract
```

## Semantic Index
**Local ChromaDB** (lightweight vector store).

## DOI Metadata
**CrossRef API** integration for citations.

## Dependency Graphs
**Graphviz system package** required:
```bash
sudo apt install graphviz  # Ubuntu
brew install graphviz      # macOS
```

## 🚀 Contribute
1. **⭐ Star** the repo
2. **Fork** → experiment → PR
3. **Issues** for new agent features
4. **Physics cases** welcome (Case B/C pilots)

**Science 2.0 = Theoretical Physicists + SAF Agents = Scientific Acceleration**

## MCP Baseline (repo-wide)

```bash
# Sync local VS Code MCP config from repository baseline
python tools/mcp_baseline.py sync

# Validate hash lock, allowlists, and local drift
python tools/mcp_baseline.py check

# Update baseline hash lock after approved baseline change
python tools/mcp_baseline.py lock
```

CI also enforces MCP drift checks in `.github/workflows/security-mcp-gate.yml`.

## P0 Process Pack
- Operational runbook: `Dokumentacja/Runbook-Gate-Executor.md`.
- Build minimal evidence packet:
	- `python tools/build_evidence_packet.py --owner "HUMAN_OWNER" --decision pending --gate-id G3 --manifest-mode inline --strict-metadata --artifact "Dokumentacja/Konsolidacja-Statusow.md|Warning|Initial consolidation" --artifact "Dokumentacja/Rejestr-Konfliktow-i-Eskalacji.md|Warning|Initial conflict register" --artifact "Dokumentacja/Podsumowanie-Gate.md|Warning|Final decision pending owner review" --require-artifact Dokumentacja/Konsolidacja-Statusow.md --require-artifact Dokumentacja/Rejestr-Konfliktow-i-Eskalacji.md --require-artifact Dokumentacja/Podsumowanie-Gate.md`
	- `--strict-metadata` is fail-closed: missing critical artifacts or `Missing/Blocker` status stops the process.
	- Zero-loss guard: the generator builds index/status metadata and does not move scientific content out of case artifacts.
- Taxonomy drift guard (alias map + canonical terms):
	- `python tools/taxonomy_guard.py`
- Combined task in VS Code:
	- `quality-gates-plus-p0`
