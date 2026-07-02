# SAF/LTR Etap G: Layered Completion Plan (post-Architecture-2.0)

Data: 2026-07-02
Status: accepted (HITL, G1-G3 completed)
Pewnosc: 0.98

## 1. Cel etapu

Domknac luki wskazane w `Dokumentacja/Analiza-Architektury-SAF-Layered-Migration.md` bez naruszania stabilnego scope `Architecture-2.0`.

Zasada organizacyjna:
- `Architecture-2.0` pozostaje zamkniete (baseline produkcyjny).
- Nowe zmiany warstwowe realizujemy jako osobny etap `G` w oddzielnym pakiecie dokumentow.

## 2. Zakres Etapu G (co dochodzi)

1. Wydzielenie i wersjonowanie instrukcji domenowych (`*.instructions.md`) jako source-of-truth polityk przekrojowych.
2. Uporzadkowanie warstwy Skills (katalog + kontrakty I/O) ponad obecnymi narzedziami `tools/`.
3. Kontrakty Tool registry i compatibility matrix.
4. Specyfikacja Scientific Backend Interface i mapowanie min. 2 backendow.
5. Aktualizacja promptow/agentow do modelu orchestrator-only (bez regresji runtime).

Poza zakresem Etapu G:
- Zmiana semantyki gate/HITL/fail-closed (to pozostaje invariant z 2.0).
- Przebudowa dzialajacego monitoringu operacyjnego (utrzymujemy obecne runbooki i scheduler).

## 3. Macierz luk (plan vs stan)

| ID | Luka z analizy | Stan obecny | Cel Etapu G | Priorytet |
|---|---|---|---|---|
| G-L01 | Brak dedykowanych `*.instructions.md` | niezaadresowane systemowo | komplet instrukcji przekrojowych + ownerzy | wysoki |
| G-L02 | Skills glownie opisowe, bez wspolnego katalogu kontraktowego | czesciowo | katalog skill contracts + chain patterns | wysoki |
| G-L03 | Brak jawnego tool-contracts registry | czesciowo | rejestr kontraktow + compatibility matrix | wysoki |
| G-L04 | Brak backend-interface-spec i backend-capabilities | niezaadresowane | spec + mapowanie SymPy/NumPy (+ kandydaci) | sredni |
| G-L05 | Brak formalnego migration/compatibility report Etapu 6 z analizy | niezaadresowane | raport zamkniecia Etapu G | sredni |

## 4. Plan wdrozenia (3 iteracje)

### Iteracja G1: Instructions foundation
Zakres:
1. Dodanie dokumentow:
   - `Dokumentacja/Instructions/quality-gates.instructions.md`
   - `Dokumentacja/Instructions/reporting.instructions.md`
   - `Dokumentacja/Instructions/tool-contracts.instructions.md`
   - `Dokumentacja/Instructions/notation.instructions.md`
   - `Dokumentacja/Instructions/literature.instructions.md`
2. Ustalenie ownerow i wersjonowania instrukcji.
3. Referencje w runbookach i dokumentacji systemowej.

Kryterium done:
- Policy duplication w agent docs ograniczone do referencji (bez copy-paste runtime policy).

### Iteracja G2: Skills + Tool contracts
Zakres:
1. Dodanie katalogu kontraktow skills:
   - `Dokumentacja/Skills/skill-contracts-registry.md`
2. Dodanie rejestru tool contracts:
   - `Dokumentacja/Tools/tool-contracts-registry.md`
   - `Dokumentacja/Tools/compatibility-matrix.md`
3. Mapowanie istniejacych narzedzi `tools/*.py` do kontraktow.

Kryterium done:
- Min. 80% krytycznych flow mapowalne jako `Agent -> Skill -> Tool` na kontraktach.

### Iteracja G3: Backend interface + closure
Zakres:
1. Dodanie:
   - `Dokumentacja/Backends/backend-interface-spec.md`
   - `Dokumentacja/Backends/backend-capabilities.md`
2. Raport zamkniecia:
   - `Dokumentacja/Architecture-2.1/SAF-LTR-Etap-G-Migration-Report.md`
   - `Dokumentacja/Architecture-2.1/SAF-LTR-Etap-G-Compatibility-Report.md`
3. GO/NO-GO dla Etapu G (HITL).

Kryterium done:
- Brak krytycznych blockerow semantycznych, fail-closed nienaruszony, gotowosc do Architecture-2.1 accepted.

## 5. Governance i kontrola ryzyk

Reguly:
1. Każda iteracja G przechodzi przez quality-gates-offline + review formal-consistency.
2. Brak danych krytycznych => fail_closed (Blocker + eskalacja do Orkiestratora i Ownera).
3. Decyzje GO dla Etapu G pozostaja HITL.

Ryzyka i mitigacje:
1. Ryzyko over-fragmentation instrukcji.
   - Mitigacja: minimalna granularnosc + owner per instruction.
2. Ryzyko driftu miedzy instructions i runbookami.
   - Mitigacja: checklista synchronizacji dokumentow przy kazdej iteracji.
3. Ryzyko regresji w dzialajacym weekly governance.
   - Mitigacja: nie modyfikowac mechaniki scheduler/runbook operacyjnego bez oddzielnego ADR.

## 6. Artefakty wejscia/wyjscia

Wejscie:
- `Dokumentacja/Analiza-Architektury-SAF-Layered-Migration.md`
- `Dokumentacja/Architecture-2.0/SAF-LTR-Migration-Plan.md`
- `Dokumentacja/Architecture-2.0/SAF-LTR-Plan-vs-Wdrozenie-Mini-Audyt.md`

Wyjscie:
- pakiet `Dokumentacja/Instructions/*`
- pakiet `Dokumentacja/Skills/*`
- pakiet `Dokumentacja/Tools/*`
- pakiet `Dokumentacja/Backends/*`
- raporty zamkniecia Etapu G

## 7. Decyzja i nastepny krok

Rekomendacja:
- Zatwierdzic Etap G jako osobny strumien `Architecture-2.1`.

Nastepny krok po akceptacji ownera:
- Uruchomic Iteracje G1 i dostarczyc pierwszy pakiet `Instructions foundation`.

## 8. Wykonanie Iteracji G1

Status: completed
Data: 2026-07-02
Pewnosc: 0.96

Zakres wykonany:
1. Dodano pakiet `Dokumentacja/Instructions/*`.
2. Ustalono ownerow i wersjonowanie instrukcji w `Dokumentacja/Instructions/README.md`.
3. Dodano referencje do pakietu instructions w runbooku i dokumentacji systemowej.

Artefakty dowodowe:
- `Dokumentacja/Instructions/README.md`
- `Dokumentacja/Instructions/quality-gates.instructions.md`
- `Dokumentacja/Instructions/reporting.instructions.md`
- `Dokumentacja/Instructions/tool-contracts.instructions.md`
- `Dokumentacja/Instructions/notation.instructions.md`
- `Dokumentacja/Instructions/literature.instructions.md`
- `Dokumentacja/Runbook-Gate-Executor.md`
- `Dokumentacja/Dokumentacja-Systemowa.md`

Wniosek:
- Iteracja G1 jest domknieta i gotowa do przejscia do Iteracji G2.

## 9. Wykonanie Iteracji G2

Status: completed
Data: 2026-07-02
Pewnosc: 0.95

Zakres wykonany:
1. Dodano katalog kontraktow skills.
2. Dodano rejestr kontraktow tools i compatibility matrix.
3. Zmapowano krytyczne flow Agent -> Skill -> Tool z coverage 90%.

Artefakty dowodowe:
- `Dokumentacja/Skills/skill-contracts-registry.md`
- `Dokumentacja/Tools/tool-contracts-registry.md`
- `Dokumentacja/Tools/compatibility-matrix.md`

Wniosek:
- Iteracja G2 jest domknieta i gotowa do przejscia do Iteracji G3.

## 10. Wykonanie Iteracji G3

Status: completed
Data: 2026-07-02
Pewnosc: 0.96

Zakres wykonany:
1. Dodano Scientific Backend Interface spec.
2. Dodano backend capabilities map z mapowaniem minimum 2 backendow.
3. Dodano raport migracyjny i raport kompatybilnosci Etapu G.

Artefakty dowodowe:
- `Dokumentacja/Backends/backend-interface-spec.md`
- `Dokumentacja/Backends/backend-capabilities.md`
- `Dokumentacja/Architecture-2.1/SAF-LTR-Etap-G-Migration-Report.md`
- `Dokumentacja/Architecture-2.1/SAF-LTR-Etap-G-Compatibility-Report.md`

Wniosek:
- Iteracja G3 jest domknieta; Etap G jest gotowy do decyzji GO/NO-GO w trybie HITL.

## 11. Decyzja koncowa Etapu G

Status decyzji: GO accepted (HITL)
Rekomendacja techniczna: GO (conditional)

Warunki:
1. Finalna akceptacja human owner.
2. Dalsza integracja backendow candidate tylko przez oddzielny ADR.

Wykonanie warunkow:
1. Akceptacja human owner: completed (2026-07-02).
2. Integracje backendow candidate pozostaja poza Etapem G i wymagaja oddzielnego ADR: active constraint.

## 12. Post-acceptance baseline verification

Status: completed
Data: 2026-07-02
Pewnosc: 0.98

Wynik:
1. `python tools/contract_guard.py` -> PASS (`blockers=0`)
2. `python -m ruff check tools tests` -> PASS
3. `python -m pytest -q` -> PASS

Wniosek:
- Etap G utrzymuje zgodnosc runtime i governance po akceptacji HITL.

## 13. Etap 2: orchestrator-only profiles (.github)

Status: completed (v1)
Data: 2026-07-02
Pewnosc: 0.96

Zakres:
1. De-dup polityk wspolnych do referencji centralnych.
2. Runtime bindings aktywne we wszystkich profilach agentow.
3. Uproszczenie kluczowych profilow agentow do ownership/routing/eskalacja.

Definition of Done (Etap 2):
1. 14/14 agent profiles zawiera `Runtime bindings (Architecture 2.1)`.
2. Brak lokalnych kopii polityk przekrojowych jako source-of-truth.
3. `contract_guard` waliduje mapowanie Agent -> Skill i pokrycie wszystkich agentow.

## 14. Etap 2: orchestrator-only full sweep

Status: completed (full)
Data: 2026-07-02
Pewnosc: 0.98

Zakres:
1. Ujednolicono wszystkie pozostale profile agentow do wspolnego schematu orchestrator-only.
2. Zachowano runtime bindings i centralne source-of-truth bez duplikowania polityk.
3. Utrzymano fail-closed oraz sciezki eskalacji przez Orkiestratora.

Walidacja:
1. ruff -> PASS
2. pytest -> PASS
3. mypy -> PASS
4. build -> PASS
5. security_sanity_check -> PASS
6. taxonomy_guard -> PASS
7. process_suite_t04 -> PASS (blockers=0)
8. contract_guard -> PASS (blockers=0)

Wniosek:
- Etap 2 jest domkniety w wersji pelnej i spojnosc governance-runtime utrzymana.
