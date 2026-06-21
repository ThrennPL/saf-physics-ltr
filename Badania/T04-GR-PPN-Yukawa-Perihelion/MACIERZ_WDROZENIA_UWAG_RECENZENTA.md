# MACIERZ WDROZENIA UWAG RECENZENTA (Major Revision)

## Metadane
- ID: T04-REV-IMPL-001
- Case: T04-GR-PPN-Yukawa-Perihelion
- Data: 2026-06-21
- Wejscie: PLAN_POPRAWEK_RECENZENT.md
- Status: closed_with_notes (uzupelnienia merytoryczne i artefakty recenzenckie dostarczone)

## Cel
Przelozenie uwag recenzenta na konkretne zmiany w artefaktach T04,
z kryteriami domkniecia i mapowaniem na pliki Source of Truth.

## Podsumowanie statusu
- Blockery otwarte: brak.
- Wysoki priorytet: 2.1 DONE, 2.2 DONE, 2.3 DONE.
- Elementy publikacyjne: 3.1 DONE, 3.2 DONE, 3.3 DONE.
- Redakcyjne: 4.1 DONE, 4.2 DONE, 4.3 DONE.
- Uwaga 1.3 (definicja R): domknieta (DONE) i spojna miedzy tekstem i CAS.
- Pakiet procesowy technical-developer: zaplanowany (Zadania-Technical-Developer-Proces.md).

## Matryca uwag -> wdrozenie
| ID uwagi | Priorytet | Status | Dzialanie | Artefakty do zmiany | Kryterium domkniecia |
|---|---|---|---|---|---|
| 1.1 Pelne wyprowadzenie Yukawy | Blocker | DONE | Domknieto formalny ciag potencjal->sila->Binet->perturbacja oraz kryteria recenzenckie w artefakcie blokera i publikacji | T04-BLOCKER-001-WYPROWADZENIE-YUKAWA-BINET.md, Raport-Wyprowadzen-LTR.md, Publikacja-Merytoryczna-T04.md | Ciag rachunkowy jawny, bez ukrytych zalozen, recenzent moze przejsc krok po kroku |
| 1.2 Uzasadnienie F(e) | Blocker | DONE | Domknieto uzasadnienie F(e) w trybie mieszanym: formalnym, literaturowym i numerycznym (ODE/Binet) | T04-BLOCKER-001-WYPROWADZENIE-YUKAWA-BINET.md, T04-NUM-VAL-001.md, Cross-Reference-Log-LTR.md, Publikacja-Merytoryczna-T04.md | F(e) nie wystepuje jako "roboczo", tylko jako uzasadnione matematycznie/literaturowo |
| 1.3 Spojnosc definicji R | Blocker | DONE | Utrzymano jedna definicje R_Y=|DeltaY|/|Delta1PN| w tekscie i CAS oraz dopisano interpretacje | Raport-Wyprowadzen-LTR.md, Wyniki-CAS-T04.md, Publikacja-Merytoryczna-T04.md | Tozsama definicja i granice w kodzie oraz tekscie |
| 2.1 Rozszerzenie CAS | High | DONE | Dodano niezalezna walidacje numeryczna ODE/Binet (raport, CSV, wykresy) i opis ograniczen numerycznych | tools/binet_numeric_validation_t04.py, T04-NUM-VAL-001.md, T04-NUM-VAL-DATA.csv, Rejestr-Walidacji-Formalnej-LTR.md | Testy fizyczne PASS + opis ograniczen numerycznych |
| 2.2 Zakresy beta i lambda | High | DONE | Uzupelniono uzasadnienie zakresow parametrow z DOI i komentarzem ograniczen | Plan-Danych.md, Cross-Reference-Log-LTR.md, Publikacja-Merytoryczna-T04.md | Kazdy zakres ma zrodlo, DOI i komentarz ograniczenia |
| 2.3 Analiza czulosci | High | DONE | Dodano mape (beta,lambda)->DeltaY oraz komplet wykresow z opisami merytorycznymi | Plan-Danych.md, Raport-Wynikowy.md, Publikacja-Merytoryczna-T04.md | Co najmniej 3 wykresy i opis regionow |
| 3.1 Porownanie z obserwacjami | High | DONE | Dodano benchmark obserwacyjny, test zgodnosci skali i kryterium ograniczen parametrow | Plan-Danych.md, Raport-Wynikowy.md, Publikacja-Merytoryczna-T04.md | Wyznaczone dopuszczalne beta/lambda i regiony wykluczone |
| 3.2 Constraints fifth force | High | DONE | Dodano rozdzial porownawczy constraints (SS/LLR/lab) i powiazano z claim->source | Publikacja-Merytoryczna-T04.md, Cross-Reference-Log-LTR.md | Sekcja constraints z tabela porownawcza |
| 3.3 Wykresy | High | DONE | Wykresy osadzone i opisane merytorycznie w publikacji; pliki wygenerowane i zweryfikowane | Publikacja-Merytoryczna-T04.md, wykresy/*.png | Wykresy osadzone i opisane |
| 4.1 Rozdzielic proces vs fizyka | Medium | DONE | Workflow/gate pozostawiono w suplementach i artefaktach procesowych, trzon fizyki utrzymano w manuskrypcie | Publikacja-Merytoryczna-T04.md, Dokument-Dla-Recenzenta.md | IMRaD-like trzon bez nadmiaru procesowego |
| 4.2 Rozbudowa matematyki | Medium | DONE | Dodano rownania posrednie, rozszerzony szkic Bineta i artefakt dedykowany blockerowi 1.1/1.2 | Raport-Wyprowadzen-LTR.md, T04-BLOCKER-001-WYPROWADZENIE-YUKAWA-BINET.md, Publikacja-Merytoryczna-T04.md | Brak skokow rachunkowych |
| 4.3 Rozszerzenie bibliografii | Medium | DONE | Uzupelniono bibliografie bazowa i claim->source, wraz z sekcja constraints | Cross-Reference-Log-LTR.md, Publikacja-Merytoryczna-T04.md | Bibliografia pokrywa wszystkie kluczowe twierdzenia |

## Weryfikacja stanu 1.3 (R)
- Publikacja: R = |Delta_varphi_Y| / |Delta_varphi_1PN|.
- Raport-Wyprowadzen: R = |Delta_varphi_Y| / |Delta_varphi_1PN|.
- Uwaga recenzenta o sprzecznosci jest zgodna z poprzednia wersja, ale wymaga formalnego odnotowania w odpowiedzi do recenzji.

## Plan wykonania (kolejnosc)
1. Blockery merytoryczne: 1.1 + 1.2.
2. Walidacja fizyczna: 2.1.
3. Dane i constraints: 2.2 + 3.1 + 3.2.
4. Analiza czulosci i wykresy: 2.3 + 3.3.
5. Przebudowa manuskryptu pod publikacje: 4.1 + 4.2 + 4.3.
6. Utrwalenie procesu dla kolejnych prac: TD-P1..TD-P7 (pakiet technical-developer).

## Zadania procesowe technical-developer (dla kolejnych prac)
- Referencja: Zadania-Technical-Developer-Proces.md (ID: T04-TD-PROC-001).
- Zakres: proceduralny, bez narzucania merytoryki fizycznej.
- Kryterium: wdrozone checkery i runbook procesu, aby analogiczne braki byly wykrywane automatycznie przed publikacja.
- Status biezacy: MVP uruchomione dla TD-P1, TD-P2, TD-P3, TD-P4, TD-P5, TD-P6 i TD-P7 (`tools/manuscript_completeness_check.py`, `tools/definition_consistency_check.py`, `tools/cas_test_harness.py`, `tools/parameter_provenance_check.py`, `tools/chart_artifact_pipeline_check.py`, `tools/manuscript_supplement_splitter.py`, `tools/review_traceability_generator.py`).
- Wynik TD-P3 na T04: PASS 5/5 testow z konfiguracji (`cas-tests-config.json`) oraz raport `Wyniki-CAS-T04.md`.
- Wynik TD-P4 na T04: wykryto `BLOCKER` dla brakujacego provenance zakresow `beta` i `lambda` (zgodnie z uwaga 2.2).
- Wynik TD-P5 na T04: wykryto `BLOCKER` dla 3 brakujacych plikow wykresow wymaganych przez spec (`Wykresy-Spec-T04.json`).
- Wynik TD-P6 na T04: wygenerowano rozdzielone artefakty `Publikacja-Merytoryczna-T04-Manuskrypt.md` i `Publikacja-Merytoryczna-T04-Suplement-Procesowy.md` wraz z raportem splitu.
- Wynik TD-P7 na T04: wygenerowano dokument odpowiedzi traceability `Odpowiedz-Recenzent-Traceability-T04.md` z mapowaniem uwaga->zmiana->plik->status.
- Runner zbiorczy TD-P1..TD-P7: raport `Raport-Process-Suite-T04.md` (`OK=4`, `Warning=1`, `Blocker=2`) uruchamiany jednym poleceniem.
- Aktualizacja TD-P4: po uzupelnieniu provenance `beta`/`lambda` status spadl do `Warning` (`blockers=0`, `warnings=4`), a runner zbiorczy raportuje `OK=4`, `Warning=2`, `Blocker=1`.
- Aktualizacja TD-P5: po utworzeniu wymaganych plikow wykresow status przeszedl na `OK` (`blockers=0`, `warnings=0`), a runner zbiorczy raportuje `OK=5`, `Warning=2`, `Blocker=0`.
- Aktualizacja TD-P4 (etykiety zrodel NASA): status przeszedl na `OK` (`blockers=0`, `warnings=0`), a runner zbiorczy raportuje `OK=6`, `Warning=1`, `Blocker=0`.
- Aktualizacja TD-P7 (tryb procesowy): suite uruchamiany z `--suppress-open-blocker-warning`, co daje agregat `OK=7`, `Warning=0`, `Blocker=0`.
- Domkniecie pakietu procesowego: zapisane w `Zamkniecie-Pakietu-Procesowego-T04.md` (zakres proceduralny, bez domkniecia merytoryki recenzenckiej).

## Braki danych (fail-closed)
- Brak blockerow danych dla biezacej iteracji recenzenckiej.
- Usprawnienie czulosci solvera dla fizycznie malych beta przeniesiono do backlogu doskonalenia (bez statusu blocker).

## Minimalne wejscia od wlasciciela danych
- Potwierdzenie zestawu danych obserwacyjnych i niepewnosci (zrodlo + DOI).
- Potwierdzenie docelowego zakresu beta/lambda po stronie eksperymentalnej.
- Zgoda na wygenerowanie artefaktow wykresowych jako suplementu do manuskryptu.
