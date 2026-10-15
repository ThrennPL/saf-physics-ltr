# SAF Physics LTR


Repozytorium modelu Środowiska Agentów AI dla Fizyki (SAF) w podejściu Literate Theoretical Research (LTR).
![SAF Architecture](Dokumentacja/SAF_PL.png)

## Szybki start
1. Utwórz i aktywuj środowisko Python (`.venv`).
2. Zainstaluj zależności potrzebne do uruchomienia: `pip install -r requirements.txt`.
3. Opcjonalnie, do jakości kodu i CI: zainstaluj zależności developerskie: `pip install -r requirements-dev.txt`.
4. Opcjonalnie: włącz hook pre-commit: `pre-commit install`.
5. Opcjonalnie: skopiuj `.env.example` do `.env` i ustaw ADS_API_TOKEN.
6. Uruchom kontrolę bezpieczeństwa i MCP: `python tools/security_sanity_check.py`.

```bash
git clone https://github.com/ThrennPL/saf-physics-ltr
cd saf-physics-ltr
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Opcjonalnie: zależności developerskie (lint/test/typecheck/build)
pip install -r requirements-dev.txt

# Opcjonalnie: włącz pre-commit (bramka dryfu MCP)
pre-commit install

# Opcjonalnie: ADS token
# Skopiuj .env.example do .env i ustaw ADS_API_TOKEN

# Sanity check security/MCP
python tools/security_sanity_check.py

# Pierwsze uruchomienie narzędzia
python tools/arxiv_search.py "lagrangian stability" --max 5
```


## Minimalne dane startowe (wymagane)
- Hipoteza i cel badania.
- Zakres i wykluczenia.
- Wariant badania (teoretyczny/eksperymentalny/obliczeniowy).
- Założenia krytyczne.
- Wypełniona `Dokumentacja/Karta-Badania.md`.


## Dlaczego SAF?
**Problemy w badaniach teoretycznych, które to rozwiązuje:**
- Niespójna notacja → **Agent Formal Consistency**
- Luki w literaturze → **Discovery (ArXiv/ADS)**
- Kłopoty z powtarzalnością wyników → **Walidacja LTR i kontrole formalne**
- Wolne przeglądy → **Bramki jakości Gate 1-4**


## Architektura (agenci)
14 wyspecjalizowanych agentów:
- Research Orchestrator: kieruje pracą, pilnuje przejść między gate i zbiera statusy.
- Formal Consistency: pilnuje spójności notacji i ID oraz rozstrzyga konflikty notacyjne.
- Model Review: rozstrzyga konflikty fizyczne i merytoryczne.
- Physics Discovery: ustala kierunek rozpoznania i pytania badawcze.
- Cross-Reference: łączy literaturę z ArXiv/ADS z dowodami.
- Data Quality: sprawdza jakość danych przed analizą niepewności.
- Statistics Review: ocenia niepewności/CI i odporność wnioskowania.
- Risk & Compliance: pilnuje ryzyk i warunków fail-closed.
- Simulation/Experiment: przygotowuje warianty wykonania i sprawdza powtarzalność.
- Socratic Mentor: kwestionuje założenia, przypadki graniczne i ukryte sprzeczności.
- Artifact Quality: zbiera wyniki w pakiet gotowy do gate.
- Knowledge Repo: porządkuje słownik i pozwala ponownie używać artefaktów.
- Language Polish Quality: obowiązkowa korekta językowa PL przed finalizacją i PDF.
- Technical Developer: poprawki kodu, automatyzacje i obsługa awarii narzędzi.

## Architecture 2.1: warstwa runtime (zakres środowiskowy)
Środowisko jest teraz podzielone na warstwy. Zasady i kontrakty wykonawcze są jawne, a ich poprawność jest sprawdzana w trybie fail-closed:

- Agenci: orkiestracja, odpowiedzialność, eskalacja (`.github/agents/`).
- Katalog skills: mapowanie skilli używanych w runtime (`mcp/skills/skill_catalog.json`).
- Kontrakty tools: stały interfejs skill->tool (`mcp/tools/tool_contract_index.json`).
- Warstwa backend: interfejs backendów i capabilities (`mcp/backends/`).
- Walidacja guardrails: spójność kontraktów i pokrycie agent-skill (`python tools/contract_guard.py`).

Zmiana dotyczy tylko środowiska: ułatwia utrzymanie i poprawia spójność runtime. Decyzje gate nadal należą do tych samych osób (HITL bez zmian).

## Przepływ orkiestracji
Domyślna kolejność i zależności:
1. Zbierz wymagane artefakty i pakiety kontekstu case'u.
2. `Formal Consistency -> Model Review` (kolejność obowiązkowa).
3. `Data Quality -> Statistics Review` (kolejność obowiązkowa).
4. `Discovery -> Cross-Reference`: zakres literatury i powiązania.
5. `Language Polish Quality` przed finalizacją dokumentów i eksportem paczki.
6. `Risk & Compliance` równolegle, z eskalacją poważnych znalezisk.
7. `Artifact Quality`: zebranie statusów i rekomendacja.
8. Decyzję podejmuje człowiek dla Gate 1/2/4. Gate 3 może przejść warunkowo, tylko przy niskim ryzyku.

Reguły eskalacji:
- Każdy `Blocker` lub nierozstrzygnięty konflikt idzie do Orkiestratora, a potem do człowieka.
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
- .github/agents/ - profile agentów (konfiguracja ról)
- .github/prompts/ - prompty pomocnicze
- tools/ - narzędzia CLI (lint LTR, ArXiv/ADS, routing modeli)

Nowe pakiety artefaktów dla fizyki teoretycznej są w `Case-Template/Artefakty/`.


## Najważniejsze pliki
- Założenia (PL): Zalozenia-Srodowisko-Fizyka.md
- Założenia (EN): Assumptions-SAF-Physics.md
- Rejestr decyzji: DECISIONS.md
- Dokumentacja systemowa: Dokumentacja/Dokumentacja-Systemowa.md
- Konfiguracja agentów: .github/agents/
- Instrukcja użycia: Dokumentacja/Instrukcja-Uzycia.md


## Zależności
- Python 3.11+ (zalecany 3.13)
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
OCR wymaga zewnętrznego narzędzia (np. Tesseract). `pytesseract` jest tylko nakładką.


## Indeks semantyczny
Używamy `chromadb` jako lekkiego indeksu lokalnego.


## Cytowania i DOI
Metadane DOI pobieramy przez `crossrefapi`.


## Graf zależności
`graphviz` wymaga zainstalowania systemowego narzędzia Graphviz.


## LTR lint
Prosta walidacja tagów LTR:


```bash
python tools/lint_ltr.py
```


Polecenie zakończy się błędem, gdy są ostrzeżenia:


```bash
python tools/lint_ltr.py --fail-on-warning
```

## Lokalny runner QA dla n8n

Runner to mała usługa HTTP, która pozwala n8n uruchamiać kontrole repozytorium. Działa
na liście dozwolonych poleceń: udostępnia tylko `lint_ltr`, `taxonomy_guard`, testy pytest
repozytorium oraz endpointy opisane niżej (tylko odczyt albo dopisywanie). Nie przyjmuje
z HTTP poleceń powłoki, ścieżek plików ani argumentów skryptów. Repozytorium zostaje poza
kontenerem n8n. Ustaw losowy `QA_RUNNER_TOKEN` (min. 32 znaki). Nasłuchuj na `0.0.0.0`
tylko wtedy, gdy Docker musi dotrzeć do usługi na hoście, i wtedy ogranicz dostęp do
portu 8765 zaporą hosta.

```powershell
$env:QA_RUNNER_TOKEN = "<losowy token, min. 32 znaki>"
python tools/qa_runner_service.py --host 0.0.0.0 --port 8765
```

W n8n utwórz credential Header Auth (nazwa nagłówka `Authorization`, wartość:
`Bearer <ten sam token>`). Adres runnera z kontenera: `http://host.docker.internal:8765`.
Endpointy:
- `GET /v1/checks`
- `POST /v1/checks/{lint_ltr|taxonomy_guard|pytest}`
- `POST /v1/literature/arxiv` (wyszukiwanie)
- `POST /v1/literature/log` (dopisanie kandydatów do logu)
- `POST /v1/gate/pack` (raport tylko do odczytu)

Kontrola ma limit czasu 120 s, a jej wyjście jest obcinane. Trzymaj usługę lokalnie
i zatrzymaj ją po użyciu.

### Synchronizacja workflow n8n przez Public API

Klucz API utwórz w n8n (Settings -> n8n API) i przechowuj go poza repozytorium, np. jako
zmienną użytkownika (`N8N_LOCAL_API_KEY_TMD`) albo w `.env`. Nigdy nie wklejaj go do
czatów ani do commitów.

```powershell
python tools/n8n_sync.py list
python tools/n8n_sync.py pull Ku19rXEPiP6PkDWu n8n/repo-qa-raport-workflow.json
python tools/n8n_sync.py push Ku19rXEPiP6PkDWu n8n/repo-qa-raport-workflow.json
python tools/n8n_sync.py check   # tylko odczyt: porównanie n8n z n8n/*.json (nodes, connections); kod 1 = rozbieżność
```

`tools/n8n_sync.py` (czyta `N8N_API_KEY` / `N8N_LOCAL_API_KEY_TMD`) odmawia zapisu lub
wysłania plików, które wyglądają na zawierające sekrety. Public API nie obsługuje
folderów, więc po utworzeniu workflow przenieś go ręcznie do folderu `TheoreticalMD`
w UI n8n (karta workflow -> Move). Credentiale (Header Auth z tokenem runnera) tworzy
się tylko w UI. W `n8n/*.json` trzymamy wyłącznie workflow związane z tym repozytorium.
Pozostałe (np. YouTube/RSS, Telegram) zostają poza repo, a `check` zgłasza je jako WARNING.
Starszy workflow "Repo QA - reczne kontrole" został zarchiwizowany w n8n (można go
przywrócić), a jego eksport usunięto z repozytorium.

### Workflow w repo (`n8n/`)

- **Repo QA - raport (reczny)** (`repo-qa-raport-workflow.json`, ID `Ku19rXEPiP6PkDWu`):
  uruchamia trzy kontrole. Jeśli status jest inny niż `OK`, dopisuje wpis do `qa-alerts.log`
  w katalogu plików n8n (`/data` w kontenerze). Raport po polsku zapisuje w
  `reports/qa-<znacznik>.md` (`D:\n8n-files\reports`). Nie ma harmonogramu ani publikacji.
- **Przeglad literatury arXiv (reczny)** (`repo-arxiv-przeglad-workflow.json`,
  ID `lS7H9QuTFx6hXuJm`): formularz pyta o słowa kluczowe (jedna fraza w linii, max 5),
  kategorie arXiv i limit wyników na frazę. Workflow wywołuje `POST /v1/literature/arxiv`
  i zapisuje raport w `reports/arxiv-<znacznik>.md`. Wyniki to preprinty. Drugi
  ekran ("Wybor publikacji") pokazuje unikalne wyniki jako pola wyboru oraz temat
  badania (folder w `Badania/`, np. `T04-GR-PPN-Yukawa-Perihelion`). Wybór trafia do
  `reports/arxiv-wybor-<znacznik>.json` (status `do_weryfikacji`). Jeśli temat jest
  poprawny i wybrano 1-20 pozycji, workflow wywołuje `POST /v1/literature/log`. Ten
  endpoint tylko dopisuje sekcję "Kandydaci literatury z arXiv" do
  `Badania/<temat>/Cross-Reference-Log-LTR.md`. Nie zmienia istniejącego tekstu,
  pomija ID, które już są w logu, i nie rusza tabeli claim -> source. Formularz testowy
  uruchamiaj raz na "Execute workflow" i używaj jednej karty przeglądarki.
- **Repo - paczka przed gate (reczny)** (`repo-gate-paczka-workflow.json`,
  ID `FwgFTYrcMBI8tuQR`): formularz z tematem i numerem gate (1-4). Endpoint
  `POST /v1/gate/pack` (tylko odczyt) podaje, które artefakty są, a których brakuje,
  jaki jest status logu literatury, ile jest `DO_UZUPELNIENIA` oraz ile `Q-XXX` jest
  otwartych i zamkniętych. Pytanie uznajemy za zamknięte, gdy linia z jego ID zawiera
  "zamkniete"/"zamknieto". Tylko otwarte pytania dają Warning. Workflow dodaje kontrole
  lint_ltr, taxonomy_guard i pytest i zapisuje raport po polsku
  `reports/gate<N>-<temat>-<znacznik>.md` (status OK/Warning/Blocker, pewność 0-1).
  Raport nigdy nie rekomenduje zatwierdzenia gate. Dla Gate 3 tylko przypomina regułę
  agent-conditional pass. Wymagane artefakty dla każdego gate pochodzą z
  `Dokumentacja/Artefakty-Wymagania.md` (konfiguracja domenowa `GATE_ARTIFACT_SOURCES`,
  każda pozycja ma swoje źródło). Sprawdzamy tylko, czy pliki istnieją. Kryteria z
  `Checklista-Research-Gate` są wypisane do oceny przez człowieka, a każdy
  Warning/Blocker ma kolumny owner/ETA (DO_UZUPELNIENIA). Raport podaje też, czy istnieje
  `Raport-Process-Suite-<Txx>.md` i jaka jest data tego pliku. To tylko informacja:
  nie zmienia statusu, a wyniki z tego pliku nie są interpretowane.
- **Repo - dopisanie kandydatow arXiv do logu (API)**
  (`repo-arxiv-log-kandydatow-workflow.json`, ID `RdcYApAjxCWV5eF8`): webhook dla agentów
  (narzędzie `log_arxiv_candidates`).
- **n8n - Testowy workflow** (`n8n-testowy-workflow.json`): przykład i test łączności
  (webhook `/healthz`).

### Webhooki narzędzi agentowych

Narzędzia są zadeklarowane w `mcp/tools/tool_contract_index.json` (sekcja `tools`).
Workflow musi być aktywny, a runner uruchomiony z `QA_RUNNER_TOKEN`:

| Narzędzie | Webhook (POST, JSON) | Eksport workflow |
|---|---|---|
| `run_repo_qa` | `/webhook/v1/qa/run` | `n8n/repo-qa-raport-workflow.json` |
| `generate_gate_pack` | `/webhook/v1/gate/pack-run` | `n8n/repo-gate-paczka-workflow.json` |
| `search_arxiv_literature` | `/webhook/v1/literature/arxiv-search` | `n8n/repo-arxiv-przeglad-workflow.json` |
| `log_arxiv_candidates` | `/webhook/v1/literature/log-candidates` | `n8n/repo-arxiv-log-kandydatow-workflow.json` |

Błędne dane wejściowe dają HTTP 400 z `{"status":"Blocker","error":...,"detail":...}`.
`search_arxiv_literature` tylko zwraca kandydatów (`pubs`). Wyboru dokonuje człowiek.
`log_arxiv_candidates` dopisuje wybrane pozycje (pełne obiekty z `pubs`) do
`Cross-Reference-Log-LTR.md` danego badania. Pole `approved_by` jest wymagane: wpisz
tam osobę, która dokonała wyboru, a trafi ona do logu. Duplikaty są pomijane
(status Warning), a istniejący tekst nigdy nie jest zmieniany.

### Docker, tunel i odtwarzanie środowiska

- Kontener n8n używa lokalnego obrazu `n8n-tmd:local`
  (`docker build -t n8n-tmd:local n8n/docker`). Obraz dodaje `youtube-transcript`
  i jest uruchamiany z `NODE_FUNCTION_ALLOW_EXTERNAL=youtube-transcript`.
- `n8n start --tunnel` nie jest dostępne w obecnej wersji n8n. Dla Telegram Trigger użyj
  kontenera Cloudflare Quick Tunnel (`cloudflare/cloudflared`) i ustaw na kontenerze n8n
  `WEBHOOK_URL` na adres tunelu oraz `N8N_PROXY_HOPS=1`. Adres Quick Tunnel zmienia się
  po restarcie. Zatrzymaj tunel, gdy nie jest potrzebny.
- Odtworzenie n8n od zera: najpierw utwórz w UI credential Header Auth (token runnera).
  Potem `python tools/n8n_sync.py restore n8n` utworzy brakujące workflow z `n8n/*.json`
  (z nowymi ID; w razie potrzeby wybierz credential ponownie w węzłach HTTP). Na końcu
  przenieś je do `TheoreticalMD`. Adres formularza testowego używa ID webhooka
  (`/form-test/<webhookId>`), a nie wartości `path`.

## ArXiv (Cross-Reference)
Proste wyszukiwanie ArXiv, wynik w tabeli Markdown:


```bash
python tools/arxiv_search.py "CPT violation" --max 10 --cat hep-th
```


## ADS (Cross-Reference, token wymagany)
```bash
python tools/ads_search.py "CPT violation" --max 10
```


## Routing modelu
Routing modeli dla agentów:


```bash
python tools/route_model.py cross-reference
python tools/route_model.py model-review --gate 3
```


Konfiguracja: `tools/model_routing.json`.


## Standard raportowania
- Status: OK / Warning / Blocker
- Pewność: 0-1 (liczbowa)
- Pytania: Q-XXX z priorytetem (niski/średni/wysoki)


## Prompty
- .github/prompts/kickoff-badania.prompt.md
- .github/prompts/konfigurator-projektu-badawczego.prompt.md
- .github/prompts/review-jakosci-badania.prompt.md
- .github/prompts/eskalacja-konfliktow.prompt.md
- .github/prompts/konsolidacja-statusow.prompt.md
- .github/prompts/podsumowanie-gate.prompt.md

## Pilot badawczy: T03 Newton-Yukawa Orbit Stability
Zespół przygotował pełny pilot w katalogu `Badania/T03-Newton-Yukawa-Orbit-Stability`.

Podsumowanie merytoryczne:
- Cel: sprawdzić, czy słaba poprawka Yukawy zmienia lokalną stabilność orbit kołowych.
- Wynik główny: warunek stabilności lokalnej
	$1+\beta e^{-x}(1+x-x^2)>0$, gdzie $x=r_c/\lambda$.
- Wniosek: dla `beta = 0` odzyskujemy limit newtonowski; wpływ znaku zależy od `(1+x-x^2)`.

Podsumowanie techniczne:
- Domknięto pełny łańcuch artefaktów (karta badania, wyprowadzenie, rejestr walidacji, pakiet ryzyk, checklisty Gate).
- Walidacja formalna obejmuje kontrole ręczne i domknięcie CAS (`SymPy`, K5 `[VERIFY-CAS]` zamknięty).
- Decyzje human-in-the-loop dla Gate 1-4 są zapisane jako `approved`.

Polecane punkty wejścia:
- `Badania/T03-Newton-Yukawa-Orbit-Stability/00-MAPA-CZYTANIA-RECENZJA.md`
- `Badania/T03-Newton-Yukawa-Orbit-Stability/Raport-Wynikowy.md`
- `Badania/T03-Newton-Yukawa-Orbit-Stability/Raport-Wyprowadzen-LTR.md`
- `Badania/T03-Newton-Yukawa-Orbit-Stability/Rejestr-Walidacji-Formalnej-LTR.md`
- `Badania/T03-Newton-Yukawa-Orbit-Stability/Akceptacje-Decyzje.md`


## Współpraca
1. Dodaj gwiazdkę repozytorium
2. Fork -> zmiany -> PR
3. Zgłoś issue dla nowych funkcji agentów

## Baseline MCP (repo-wide)

```bash
# Synchronizacja lokalnego .vscode/mcp.json z baseline repo
python tools/mcp_baseline.py sync

# Walidacja locka hash, allowlist i dryfu konfiguracji
python tools/mcp_baseline.py check

# Aktualizacja hash lock po zatwierdzonej zmianie baseline
python tools/mcp_baseline.py lock
```

W CI działa też bramka dryfu MCP: `.github/workflows/security-mcp-gate.yml`.

## Pakiet procesowy P0
- Runbook wykonania gate: `Dokumentacja/Runbook-Gate-Executor.md`.
- Budowa minimalnego pakietu dowodów:
	- `python tools/build_evidence_packet.py --owner "HUMAN_OWNER" --decision pending --gate-id G3 --manifest-mode inline --strict-metadata --artifact "Dokumentacja/Konsolidacja-Statusow.md|Warning|Wstepna konsolidacja" --artifact "Dokumentacja/Rejestr-Konfliktow-i-Eskalacji.md|Warning|Wstepny rejestr" --artifact "Dokumentacja/Podsumowanie-Gate.md|Warning|Decyzja finalna przed owner review" --require-artifact Dokumentacja/Konsolidacja-Statusow.md --require-artifact Dokumentacja/Rejestr-Konfliktow-i-Eskalacji.md --require-artifact Dokumentacja/Podsumowanie-Gate.md`
	- Tryb `--strict-metadata` działa fail_closed: brak krytycznego artefaktu albo status `Missing/Blocker` zatrzymuje proces.
	- Zero-loss: generator buduje indeks i statusy, ale nie przenosi treści merytorycznej dokumentów case.
- Kontrola dryfu słownika (aliasy + terminy kanoniczne):
	- `python tools/taxonomy_guard.py`
- Zadanie łączone w VS Code:
	- `quality-gates-plus-p0`
	- `stage-f-contract-guard` (walidacja kontraktów Workflow/Capability/Skill/Tool)
	- `dual-run-stage-f` (ścieżka legacy P0 + process-suite T04)
	- `quality-gates-plus-p0-process-suite` (pełny łańcuch; zawiera `stage-f-contract-guard` przez `p0-process-check`)
	- `migration-metrics-report` (cykliczny raport MM-001..MM-005 do Architecture 2.0)
	- `gate-timing-report` (zbiorcza telemetria czasu Gate 1-4 z docs/operations/gate_timing_log.jsonl)
	- `build-offline` (próba zbudowania paczki przez `python -m build` bez izolacji)
	- `build-smoke-offline` (plan awaryjny: `python -m pip install . --no-deps --no-build-isolation`)
	- `quality-gates-offline` (lint+test+typecheck+build-smoke-offline)
	- `owner-weekly-summary` (tygodniowy raport ownera z logu cykli)

Automatyzacja harmonogramu (Windows):
	- rejestracja: `powershell -ExecutionPolicy Bypass -File tools/scheduler/register_windows_tasks.ps1`
	- runner: `tools/scheduler/run_ops_cycle.ps1`
	- log schedulera: `docs/operations/scheduler_runs.log`
