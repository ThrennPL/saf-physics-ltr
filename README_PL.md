# SAF Physics LTR


Repozytorium dla modelu Srodowiska Agentow AI dla Fizyki (SAF) w podejsciu Literate Theoretical Research (LTR).
![SAF Architecture](Dokumentacja/SAF_PL.png)

## Szybki start
1. Utworz i aktywuj srodowisko Python (`.venv`).
2. Zainstaluj zaleznosci: `pip install -r requirements.txt`.
3. Opcjonalnie: skopiuj `.env.example` do `.env` i ustaw ADS_API_TOKEN.

```bash
git clone https://github.com/ThrennPL/saf-physics-ltr
cd saf-physics-ltr
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Opcjonalnie: ADS token
# Skopiuj .env.example do .env i ustaw ADS_API_TOKEN

# Pierwsze uruchomienie narzedzia
python tools/arxiv_search.py "lagrangian stability" --max 5
```


## Minimalne dane startowe (wymagane)
- Hipoteza i cel badania.
- Zakres i wykluczenia.
- Wariant badania (teoretyczna/eksperymentalna/computational).
- Zalozenia krytyczne.
- Wypelniona Dokumentacja/Karta-Badania.md.


## Dlaczego SAF?
**Problemy badan teoretycznych, ktore rozwiazuje:**
- Niespojna notacja → **Agent Formal Consistency**
- Luki w literaturze → **Discovery (ArXiv/ADS)**
- Problemy reprodukowalnosci → **Walidacja LTR i kontrole formalne**
- Opoznienia przegladow → **Bramki jakosci Gate 1-4**


## Architektura (agenci)
12 specjalizowanych agentow:
├── Research Orchestrator
├── Formal Consistency
├── Model Review
├── Scientific Discovery (ArXiv/ADS)
├── Cross-Reference
├── Data Quality
├── Statistics & Uncertainty
├── Risk & Compliance
├── Artifact Quality
├── Simulation/Experiment
├── Socratic Mentor
└── Knowledge Repo


## Struktura
- Dokumentacja/ - szablony i rejestry
	- Karta-Badania.md
	- Rejestr-Konfiguracji-Projektu.md
	- Rejestr-Konfliktow-i-Eskalacji.md
	- Konsolidacja-Statusow.md
	- Review-Jakosci-Gate3.md
	- Podsumowanie-Gate.md
	- Szablon-LTR/
- Case-Template/ - wzorzec nowego case'a badawczego
- .github/agents/ - profile agentow (konfiguracja rol)
- .github/prompts/ - prompty pomocnicze
- tools/ - narzedzia CLI (lint LTR, ArXiv/ADS, routing modeli)

Nowe pakiety artefaktow dla fizyki teoretycznej sa w Case-Template/Artefakty/.


## Najwazniejsze pliki
- Zalozenia (PL): Zalozenia-Srodowisko-Fizyka.md
- Zalozenia (EN): Assumptions-SAF-Physics.md
- Rejestr decyzji: DECISIONS.md
- Dokumentacja systemowa: Dokumentacja/Dokumentacja-Systemowa.md
- Konfiguracja agentow: .github/agents/
- Instrukcja uzycia: Dokumentacja/Instrukcja-Uzycia.md


## Zaleznosci
- Python 3.13+
- pypdf
- sympy
- bibtexparser
- networkx
- pillow
- pytesseract
- chromadb
- crossrefapi
- graphviz


## OCR
OCR wymaga zewnetrznego narzedzia (np. Tesseract). `pytesseract` jest tylko wrapperem.


## Indeks semantyczny
Uzywamy `chromadb` jako lekkiego indeksu lokalnego.


## Cytowania i DOI
Metadane DOI przez `crossrefapi`.


## Graf zaleznosci
`graphviz` wymaga instalacji narzedzia systemowego Graphviz.


## LTR lint
Prosta walidacja tagow LTR:


```bash
python tools/lint_ltr.py
```


Zakoncz z bledem, gdy sa ostrzezenia:


```bash
python tools/lint_ltr.py --fail-on-warning
```


## ArXiv (Cross-Reference)
Proste wyszukiwanie ArXiv i wynik w tabeli Markdown:


```bash
python tools/arxiv_search.py "CPT violation" --max 10 --cat hep-th
```


## ADS (Cross-Reference, token wymagany)
```bash
python tools/ads_search.py "CPT violation" --max 10
```


## Routing modelu
Routing modeli dla agentow:


```bash
python tools/route_model.py cross-reference
python tools/route_model.py model-review --gate 3
```


Konfiguracja w tools/model_routing.json.


## Standard raportowania
- Status: OK / Warning / Blocker
- Pewnosc: 0-1 (liczbowa)
- Pytania: Q-XXX z priorytetem (niski/sredni/wysoki)


## Prompty
- .github/prompts/kickoff-badania.prompt.md
- .github/prompts/konfigurator-projektu-badawczego.prompt.md
- .github/prompts/review-jakosci-badania.prompt.md
- .github/prompts/eskalacja-konfliktow.prompt.md
- .github/prompts/konsolidacja-statusow.prompt.md
- .github/prompts/podsumowanie-gate.prompt.md


## Wspolpraca
1. Star repozytorium
2. Fork -> zmiany -> PR
3. Issues dla nowych funkcji agentow