# SAF Physics LTR


Repozytorium modelu Srodowiska Agentow AI dla Fizyki (SAF) w podejsciu Literate Theoretical Research (LTR).
![SAF Architecture](Dokumentacja/SAF_PL.png)

## Szybki start
1. Utworz i aktywuj srodowisko Python (`.venv`).
2. Zainstaluj zaleznosci uruchomieniowe: `pip install -r requirements.txt`.
3. (Opcjonalnie, dla jakosci i CI) Zainstaluj zaleznosci developerskie: `pip install -r requirements-dev.txt`.
4. (Opcjonalnie) Wlacz hook pre-commit: `pre-commit install`.
5. Opcjonalnie: skopiuj `.env.example` do `.env` i ustaw ADS_API_TOKEN.
6. Uruchom kontrole sanity dla security/MCP: `python tools/security_sanity_check.py`.

```bash
git clone https://github.com/ThrennPL/saf-physics-ltr
cd saf-physics-ltr
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Opcjonalnie: zaleznosci developerskie (lint/test/typecheck/build)
pip install -r requirements-dev.txt

# Opcjonalnie: wlacz pre-commit (bramka dryfu MCP)
pre-commit install

# Opcjonalnie: ADS token
# Skopiuj .env.example do .env i ustaw ADS_API_TOKEN

# Sanity check security/MCP
python tools/security_sanity_check.py

# Pierwsze uruchomienie narzedzia
python tools/arxiv_search.py "lagrangian stability" --max 5
```


## Minimalne dane startowe (wymagane)
- Hipoteza i cel badania.
- Zakres i wykluczenia.
- Wariant badania (teoretyczna/eksperymentalna/obliczeniowa).
- Zalozenia krytyczne.
- Wypelniona `Dokumentacja/Karta-Badania.md`.


## Dlaczego SAF?
**Problemy badan teoretycznych, ktore rozwiazuje:**
- Niespojna notacja → **Agent Formal Consistency**
- Luki w literaturze → **Discovery (ArXiv/ADS)**
- Problemy reprodukowalnosci → **Walidacja LTR i kontrole formalne**
- Opoznienia przegladow → **Bramki jakosci Gate 1-4**


## Architektura (agenci)
14 wyspecjalizowanych agentow:
- Research Orchestrator: routing strumieni, przejscia gate, agregacja statusow.
- Formal Consistency: spojnosc notacji/ID i rozstrzyganie konfliktow notacyjnych.
- Model Review: rozstrzyganie konfliktow fizycznych i merytorycznych.
- Physics Discovery: definiowanie kierunku rozpoznania i pytan badawczych.
- Cross-Reference: mapowanie literatury ArXiv/ADS i powiazan dowodowych.
- Data Quality: kontrola jakosci danych przed analiza niepewnosci.
- Statistics Review: ocena niepewnosci/CI i odpornosci wnioskowania.
- Risk & Compliance: kontrola ryzyk i warunkow fail-closed.
- Simulation/Experiment: przygotowanie wariantow wykonania i reprodukowalnosci.
- Socratic Mentor: kwestionowanie zalozen, przypadkow granicznych i ukrytych sprzecznosci.
- Artifact Quality: konsolidacja wynikow do pakietu gate-ready.
- Knowledge Repo: normalizacja slownika i ponowne wykorzystanie artefaktow.
- Language Polish Quality: obowiazkowa walidacja jezykowa PL przed finalizacja/PDF.
- Technical Developer: poprawki kodu, automatyzacje i obsluga incydentow narzedziowych.

## Architecture 2.1: warstwa runtime (zakres srodowiskowy)
Srodowisko dziala teraz w modelu warstwowym, gdzie governance i kontrakty wykonawcze sa jawne oraz walidowane fail-closed:

- Agenci: orkiestracja, ownership, eskalacja (`.github/agents/`).
- Katalog skills: mapowanie runtime skilli (`mcp/skills/skill_catalog.json`).
- Kontrakty tools: stabilny interfejs skill->tool (`mcp/tools/tool_contract_index.json`).
- Warstwa backend: interfejs backendow i capabilities (`mcp/backends/`).
- Walidacja guardrails: spojnosc kontraktow i pokrycie agent-skill (`python tools/contract_guard.py`).

Zmiana ma charakter srodowiskowy: poprawia utrzymanie i spojnosc runtime bez zmiany ownership decyzji gate (HITL bez zmian).

## Przeplyw orkiestracji
Domyslna kolejnosc i zaleznosci:
1. Zebranie wymaganych artefaktow i pakietow kontekstu case'u.
2. `Formal Consistency -> Model Review` (kolejnosc twarda).
3. `Data Quality -> Statistics Review` (kolejnosc twarda).
4. `Discovery -> Cross-Reference` dla zakresu literatury i mapowania powiazan.
5. `Language Polish Quality` przed finalizacja dokumentow i eksportem paczki.
6. `Risk & Compliance` rownolegle, z eskalacja znalezisk krytycznych.
7. `Artifact Quality` jako konsolidacja statusow i rekomendacja.
8. Decyzja czlowieka dla Gate 1/2/4; Gate 3 warunkowo, tylko przy niskim ryzyku.

Reguly eskalacji:
- Kazdy `Blocker` lub nierozstrzygniety konflikt eskaluj do Orkiestratora, a potem do czlowieka.
- Brak wymaganych danych uruchamia fail-closed.


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

Nowe pakiety artefaktow dla fizyki teoretycznej sa w `Case-Template/Artefakty/`.


## Najwazniejsze pliki
- Zalozenia (PL): Zalozenia-Srodowisko-Fizyka.md
- Zalozenia (EN): Assumptions-SAF-Physics.md
- Rejestr decyzji: DECISIONS.md
- Dokumentacja systemowa: Dokumentacja/Dokumentacja-Systemowa.md
- Konfiguracja agentow: .github/agents/
- Instrukcja uzycia: Dokumentacja/Instrukcja-Uzycia.md


## Zaleznosci
- Python 3.11+ (rekomendowane 3.13)
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


Polecenie zakonczy sie bledem, gdy sa ostrzezenia:


```bash
python tools/lint_ltr.py --fail-on-warning
```

## Lokalny runner QA dla n8n

Runner z allowlista udostepnia tylko `lint_ltr`, `taxonomy_guard` i testy pytest
repozytorium oraz endpointy tylko do odczytu/dopisywania opisane nizej. Nie przyjmuje
polecen powloki, sciezek plikow ani argumentow skryptow z HTTP. Repozytorium zostaje
poza kontenerem n8n; ustaw losowy `QA_RUNNER_TOKEN` (min. 32 znaki). Nasluchuj na
`0.0.0.0` tylko, gdy Docker musi dotrzec do uslugi na hoscie, i ogranicz dostep do
portu 8765 zaporą hosta.

```powershell
$env:QA_RUNNER_TOKEN = "<losowy token, min. 32 znaki>"
python tools/qa_runner_service.py --host 0.0.0.0 --port 8765
```

W n8n utworz credential Header Auth (nazwa naglowka `Authorization`, wartosc:
`Bearer <ten sam token>`). Adres runnera z kontenera: `http://host.docker.internal:8765`.
Endpointy: `GET /v1/checks`, `POST /v1/checks/{lint_ltr|taxonomy_guard|pytest}`,
`POST /v1/literature/arxiv` (wyszukiwanie), `POST /v1/literature/log` (dopisanie
kandydatow do logu), `POST /v1/gate/pack` (raport tylko do odczytu). Limit czasu
kontroli to 120 s, wyjscie jest obcinane. Usluge trzymaj lokalnie i zatrzymaj po uzyciu.

### Synchronizacja workflow n8n przez Public API

Klucz API utworz w n8n (Settings -> n8n API) i przechowuj poza repozytorium, np. jako
zmienna uzytkownika (`N8N_LOCAL_API_KEY_TMD`) lub w `.env`. Nigdy nie wklejaj go do
czatow ani do commitow.

```powershell
python tools/n8n_sync.py list
python tools/n8n_sync.py pull Ku19rXEPiP6PkDWu n8n/repo-qa-raport-workflow.json
python tools/n8n_sync.py push Ku19rXEPiP6PkDWu n8n/repo-qa-raport-workflow.json
python tools/n8n_sync.py check   # tylko odczyt: porownanie n8n z n8n/*.json (nodes, connections); kod 1 = rozbieznosc
```

`tools/n8n_sync.py` odmawia zapisu lub wyslania plikow wygladajacych na zawierajace
sekrety. Public API nie obsluguje folderow: po utworzeniu workflow przenies go do
folderu `TheoreticalMD` w UI n8n (karta workflow -> Move). Credentiale (Header Auth z
tokenem runnera) tworzy sie tylko w UI. Do `n8n/*.json` trafiaja wylacznie workflow
z zakresu repo; pozostale (np. YouTube/RSS, Telegram) zostaja poza repo, a `check`
zglasza je jako WARNING.

### Workflow w repo (`n8n/`)

- **Repo QA - raport (reczny)** (`repo-qa-raport-workflow.json`, ID `Ku19rXEPiP6PkDWu`):
  uruchamia trzy kontrole; status inny niz `OK` dopisuje wpis do `qa-alerts.log`
  w katalogu plikow n8n (`/data` w kontenerze) i zapisuje raport PL w
  `reports/qa-<znacznik>.md` (`D:\n8n-files\reports`). Bez harmonogramu i publikacji.
- **Przeglad literatury arXiv (reczny)** (`repo-arxiv-przeglad-workflow.json`,
  ID `lS7H9QuTFx6hXuJm`): formularz ze slowami kluczowymi (jedna fraza w linii, max 5),
  kategoriami arXiv i limitem wynikow na fraze; wywoluje `POST /v1/literature/arxiv`
  i zapisuje raport w `reports/arxiv-<znacznik>.md`. Wyniki to preprinty. Drugi
  ekran ("Wybor publikacji") pokazuje unikalne wyniki jako pola wyboru oraz temat
  badania (folder w `Badania/`, np. `T04-GR-PPN-Yukawa-Perihelion`); wybor trafia do
  `reports/arxiv-wybor-<znacznik>.json` (status `do_weryfikacji`), a przy poprawnym
  temacie i 1-20 pozycjach wywolywany jest `POST /v1/literature/log`, ktory tylko
  dopisuje sekcje "Kandydaci literatury z arXiv" do
  `Badania/<temat>/Cross-Reference-Log-LTR.md`: nie zmienia istniejacego tekstu, pomija
  ID juz obecne i nie dotyka tabeli claim -> source. Formularz testowy uruchamiaj raz
  na "Execute workflow" i uzywaj jednej karty przegladarki.
- **Repo - paczka przed gate (reczny)** (`repo-gate-paczka-workflow.json`,
  ID `FwgFTYrcMBI8tuQR`): formularz z tematem i numerem gate (1-4). Endpoint
  `POST /v1/gate/pack` (tylko odczyt) raportuje obecne/brakujace artefakty, status logu
  literatury, liczbe `DO_UZUPELNIENIA` oraz otwarte i zamkniete `Q-XXX` (pytanie
  uznajemy za zamkniete, gdy linia z jego ID zawiera "zamkniete"/"zamknieto"; tylko
  otwarte daja Warning). Workflow dodaje kontrole lint_ltr, taxonomy_guard i pytest
  i zapisuje raport PL `reports/gate<N>-<temat>-<znacznik>.md` (status
  OK/Warning/Blocker, pewnosc 0-1). Raport nigdy nie rekomenduje zatwierdzenia gate;
  dla Gate 3 tylko przypomina regule agent-conditional pass. Wymagane artefakty dla
  gate pochodza z `Dokumentacja/Artefakty-Wymagania.md` (konfiguracja domenowa
  `GATE_ARTIFACT_SOURCES`, kazda pozycja ma zrodlo). Sprawdzana jest tylko obecnosc
  plikow; kryteria z `Checklista-Research-Gate` sa wypisane do oceny przez czlowieka,
  a kazdy Warning/Blocker ma kolumny owner/ETA (DO_UZUPELNIENIA). Raport podaje tez, czy
  istnieje `Raport-Process-Suite-<Txx>.md` i jaka jest data pliku (tylko informacyjnie:
  nie zmienia statusu, a jego wyniki nie sa interpretowane).
- **Repo - dopisanie kandydatow arXiv do logu (API)**
  (`repo-arxiv-log-kandydatow-workflow.json`, ID `RdcYApAjxCWV5eF8`): webhook dla agentow
  (narzedzie `log_arxiv_candidates`).
- **n8n - Testowy workflow** (`n8n-testowy-workflow.json`): przyklad i test lacznosci
  (webhook `/healthz`).

### Webhooki narzedzi agentowych

Narzedzia sa zadeklarowane w `mcp/tools/tool_contract_index.json` (sekcja `tools`);
workflow musi byc aktywny, a runner uruchomiony z `QA_RUNNER_TOKEN`:

| Narzedzie | Webhook (POST, JSON) | Eksport workflow |
|---|---|---|
| `run_repo_qa` | `/webhook/v1/qa/run` | `n8n/repo-qa-raport-workflow.json` |
| `generate_gate_pack` | `/webhook/v1/gate/pack-run` | `n8n/repo-gate-paczka-workflow.json` |
| `search_arxiv_literature` | `/webhook/v1/literature/arxiv-search` | `n8n/repo-arxiv-przeglad-workflow.json` |
| `log_arxiv_candidates` | `/webhook/v1/literature/log-candidates` | `n8n/repo-arxiv-log-kandydatow-workflow.json` |

Bledne dane wejsciowe daja HTTP 400 z `{"status":"Blocker","error":...,"detail":...}`.
`search_arxiv_literature` tylko zwraca kandydatow (`pubs`); wybor nalezy do czlowieka.
`log_arxiv_candidates` dopisuje wybrane pozycje (pelne obiekty z `pubs`) do
`Cross-Reference-Log-LTR.md` danego badania; wymagany jest `approved_by` (osoba, ktora
dokonala wyboru), zapisywany w logu. Duplikaty sa pomijane (status Warning), istniejacy
tekst nigdy nie jest zmieniany.

### Docker, tunel i odtwarzanie srodowiska

- Kontener n8n uzywa lokalnego obrazu `n8n-tmd:local`
  (`docker build -t n8n-tmd:local n8n/docker`; dodaje `youtube-transcript`, uruchamiany
  z `NODE_FUNCTION_ALLOW_EXTERNAL=youtube-transcript`).
- `n8n start --tunnel` nie jest dostepne w aktualnym n8n. Dla Telegram Trigger uzyj
  kontenera Cloudflare Quick Tunnel (`cloudflare/cloudflared`) i ustaw na kontenerze n8n
  `WEBHOOK_URL` na adres tunelu oraz `N8N_PROXY_HOPS=1`. Adres Quick Tunnel zmienia sie
  po restarcie; zatrzymaj tunel, gdy nie jest potrzebny.
- Odtworzenie n8n od zera: utworz credential Header Auth (token runnera) w UI, potem
  `python tools/n8n_sync.py restore n8n` tworzy brakujace workflow z `n8n/*.json`
  (nowe ID; w razie potrzeby ponownie wybierz credential w wezlach HTTP), a na koniec
  przenies je do `TheoreticalMD`. Adres formularza testowego uzywa ID webhooka
  (`/form-test/<webhookId>`), nie wartosci `path`.

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


Konfiguracja: `tools/model_routing.json`.


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

## Pilot badawczy: T03 Newton-Yukawa Orbit Stability
Zespol przygotowal pelny pilot w katalogu `Badania/T03-Newton-Yukawa-Orbit-Stability`.

Podsumowanie merytoryczne:
- Cel: sprawdzic, czy slaba poprawka Yukawy zmienia lokalna stabilnosc orbit kolowych.
- Wynik glowny: warunek stabilnosci lokalnej
	$1+\beta e^{-x}(1+x-x^2)>0$, gdzie $x=r_c/\lambda$.
- Wniosek: dla `beta = 0` odzyskujemy limit Newtonowski; wplyw znaku zalezy od `(1+x-x^2)`.

Podsumowanie techniczne:
- Domknieto pelny lancuch artefaktow (karta badania, wyprowadzenie, rejestr walidacji, pakiet ryzyk, checklisty Gate).
- Walidacja formalna obejmuje kontrole reczne i domkniecie CAS (`SymPy`, K5 `[VERIFY-CAS]` zamkniety).
- Decyzje human-in-the-loop dla Gate 1-4 sa zapisane jako `approved`.

Rekomendowane punkty wejscia:
- `Badania/T03-Newton-Yukawa-Orbit-Stability/00-MAPA-CZYTANIA-RECENZJA.md`
- `Badania/T03-Newton-Yukawa-Orbit-Stability/Raport-Wynikowy.md`
- `Badania/T03-Newton-Yukawa-Orbit-Stability/Raport-Wyprowadzen-LTR.md`
- `Badania/T03-Newton-Yukawa-Orbit-Stability/Rejestr-Walidacji-Formalnej-LTR.md`
- `Badania/T03-Newton-Yukawa-Orbit-Stability/Akceptacje-Decyzje.md`


## Wspolpraca
1. Dodaj gwiazdke repozytorium
2. Fork -> zmiany -> PR
3. Zglos issue dla nowych funkcji agentow

## Baseline MCP (repo-wide)

```bash
# Synchronizacja lokalnego .vscode/mcp.json z baseline repo
python tools/mcp_baseline.py sync

# Walidacja locka hash, allowlist i dryfu konfiguracji
python tools/mcp_baseline.py check

# Aktualizacja hash lock po zatwierdzonej zmianie baseline
python tools/mcp_baseline.py lock
```

W CI dziala tez bramka dryfu MCP: `.github/workflows/security-mcp-gate.yml`.

## Pakiet procesowy P0
- Runbook wykonania gate: `Dokumentacja/Runbook-Gate-Executor.md`.
- Budowa minimalnego pakietu dowodow:
	- `python tools/build_evidence_packet.py --owner "HUMAN_OWNER" --decision pending --gate-id G3 --manifest-mode inline --strict-metadata --artifact "Dokumentacja/Konsolidacja-Statusow.md|Warning|Wstepna konsolidacja" --artifact "Dokumentacja/Rejestr-Konfliktow-i-Eskalacji.md|Warning|Wstepny rejestr" --artifact "Dokumentacja/Podsumowanie-Gate.md|Warning|Decyzja finalna przed owner review" --require-artifact Dokumentacja/Konsolidacja-Statusow.md --require-artifact Dokumentacja/Rejestr-Konfliktow-i-Eskalacji.md --require-artifact Dokumentacja/Podsumowanie-Gate.md`
	- Tryb `--strict-metadata` dziala fail_closed: brak krytycznego artefaktu albo status `Missing/Blocker` zatrzymuje proces.
	- Zero-loss: generator buduje indeks i statusy, ale nie przenosi tresci merytorycznej dokumentow case.
- Kontrola dryfu slownika (aliasy + terminy kanoniczne):
	- `python tools/taxonomy_guard.py`
- Zadanie laczone w VS Code:
	- `quality-gates-plus-p0`
	- `stage-f-contract-guard` (walidacja kontraktow Workflow/Capability/Skill/Tool)
	- `dual-run-stage-f` (sciezka legacy P0 + process-suite T04)
	- `quality-gates-plus-p0-process-suite` (pelny lancuch; zawiera `stage-f-contract-guard` przez `p0-process-check`)
	- `migration-metrics-report` (cykliczny raport MM-001..MM-005 do Architecture 2.0)
	- `gate-timing-report` (agregacja telemetryczna czasu Gate 1-4 z docs/operations/gate_timing_log.jsonl)
	- `build-offline` (proba pakietowania przez `python -m build` bez izolacji)
	- `build-smoke-offline` (fallback przez `python -m pip install . --no-deps --no-build-isolation`)
	- `quality-gates-offline` (lint+test+typecheck+build-smoke-offline)
	- `owner-weekly-summary` (raport tygodniowy ownera z logu cykli)

Automatyzacja harmonogramu (Windows):
	- rejestracja: `powershell -ExecutionPolicy Bypass -File tools/scheduler/register_windows_tasks.ps1`
	- runner: `tools/scheduler/run_ops_cycle.ps1`
	- log scheduler: `docs/operations/scheduler_runs.log`
