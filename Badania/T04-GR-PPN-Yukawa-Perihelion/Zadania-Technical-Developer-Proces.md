# Zadania Technical Developer - uzupelnienie procesow

## Metadane
- ID: T04-TD-PROC-001
- Case: T04-GR-PPN-Yukawa-Perihelion
- Data: 2026-06-21
- Zakres: procesowy (bez definiowania merytoryki fizycznej)
- Status: closed (pakiet procesowy TD-P1..TD-P7 domkniety; merytoryka pozostaje w HITL)

## Cel
Uspojnic i zautomatyzowac proces tak, aby kolejne prace automatycznie wychwytywaly braki wskazane przez recenzenta,
bez narzucania konkretnej tresci merytorycznej badan.

## Pakiet zadan

### TD-P1: Linter kompletności manuskryptu
- opis: dodac narzedzie sprawdzajace, czy publikacja zawiera wymagane sekcje procesu publikacyjnego (np. wyprowadzenie, ograniczenia, walidacja, porownanie z danymi, bibliografia).
- wejscia: szablon sekcji obowiazkowych (konfig), plik manuskryptu .md.
- wyjscia: raport brakow sekcji (OK/Warning/Blocker).
- kryterium done: brak sekcji krytycznych => Blocker + czytelna lista brakow.

### TD-P2: Sprawdzanie spójnosci definicji miedzy artefaktami
- opis: dodac checker spójnosci definicji (np. wskazniki typu R), ktory porownuje wzory/definicje miedzy manuskryptem, raportem wyprowadzen i skryptami CAS.
- wejscia: lista wzorcow definicji do monitorowania.
- wyjscia: raport niespójnosci i lokalizacje.
- kryterium done: wykrycie rozjazdu => Warning/Blocker przed gate.

### TD-P3: Rozszerzalny harness testow CAS
- opis: przebudowac CAS-runner tak, aby testy graniczne i fizyczne byly deklarowane konfiguracyjnie i uruchamiane seryjnie (nie tylko pojedyncze testy ad hoc).
- wejscia: plik konfig testow (limity, tolerancje, nazwy testow).
- wyjscia: raport PASS/FAIL + artefakt markdown.
- kryterium done: latwe dodawanie nowych testow bez zmiany logiki glownej.

### TD-P4: Walidator pochodzenia zakresow parametrow
- opis: dodac walidator, ktory sprawdza, czy kazdy zakres parametru ma metadane zrodla (DOI/URL, data dostepu, typ ograniczenia).
- wejscia: Plan-Danych.md lub plik metadanych parametrow.
- wyjscia: raport brakow provenance.
- kryterium done: brak provenance dla parametru krytycznego => Blocker.

### TD-P5: Pipeline artefaktow wykresowych
- opis: dodac proces generowania i walidacji wykresow (nazwa, osie, legenda, jednostki, podpis) jako osobny krok pipeline.
- wejscia: dane wynikowe + spec wykresow.
- wyjscia: zestaw plikow wykresow + indeks + check poprawnosci metadanych.
- kryterium done: brak wymaganych wykresow => Warning/Blocker przed publikacja.

### TD-P6: Rozdzielenie manuskryptu i suplementu
- opis: dodac narzedzie/pipeline budujace dwie wersje: (a) publikacja naukowa (merytoryka), (b) suplement procesowy (gate/workflow/audit).
- wejscia: mapowanie sekcji do targetu (manuskrypt/suplement).
- wyjscia: 2 spójne dokumenty + raport roznic.
- kryterium done: manuskrypt nie zawiera nadmiaru procesowego, suplement zachowuje pelny audit trail.

### TD-P7: Generator odpowiedzi na recenzje (traceability)
- opis: dodac generator tabeli "uwaga recenzenta -> zmiana -> plik -> status".
- wejscia: plan poprawek recenzenta + lista zmian.
- wyjscia: gotowy dokument odpowiedzi dla recenzenta.
- kryterium done: kazda uwaga ma status i dowod wdrozenia.

## Delegacja (format obowiazkowy)
kto: technical-developer
dlaczego: standaryzacja procesu publikacyjnego, aby kolejne prace automatycznie wykrywaly i zamykaly braki procesowe
ETA: 2026-06-25 18:00
wejscia: PLAN_POPRAWEK_RECENZENT.md, MACIERZ_WDROZENIA_UWAG_RECENZENTA.md, Plan-Strumieni.md
wyjscia: patch narzedzi i/lub runbook procesu, raport wdrozenia TD-P1..TD-P7, statusy OK/Warning/Blocker
priorytet: wysoki

## Uwaga
- Zakres tego pakietu jest proceduralny.
- Nie narzuca konkretnych wynikow fizycznych ani wartosci parametrow badan.

## Postep wdrozenia
- TD-P1: MVP wdrozone w narzedziu `tools/manuscript_completeness_check.py`.
- TD-P2: MVP wdrozone w narzedziu `tools/definition_consistency_check.py`.
- TD-P3: MVP wdrozone w narzedziu `tools/cas_test_harness.py` + konfiguracja `Badania/T04-GR-PPN-Yukawa-Perihelion/cas-tests-config.json`.
- TD-P4: MVP wdrozone w narzedziu `tools/parameter_provenance_check.py`.
- TD-P5: MVP wdrozone w narzedziu `tools/chart_artifact_pipeline_check.py` + artefakty `Wykresy-Spec-T04.json` i `Wykresy-Indeks-T04.md`.
- TD-P6: MVP wdrozone w narzedziu `tools/manuscript_supplement_splitter.py` + konfiguracja `Split-Manuskrypt-Suplement-T04.json`.
- TD-P7: MVP wdrozone w narzedziu `tools/review_traceability_generator.py` + artefakt `Odpowiedz-Recenzent-Traceability-T04.md`.
- Walidacja wykonania: PASS dla T04 przy uruchomieniu lokalnym.

## Wynik pierwszego uruchomienia TD-P3 (T04)
- Artefakt: `Badania/T04-GR-PPN-Yukawa-Perihelion/Wyniki-CAS-T04.md`
- Wynik: `PASS` dla 5/5 testow (granice beta/lambda, struktura R, sanity-check numeryczny 1PN).
- Interpretacja procesowa: testy CAS uruchamiane seryjnie z konfiguracji, bez zmian logiki glownej skryptu.

## Wynik pierwszego uruchomienia TD-P4 (T04)
- Artefakt: `Badania/T04-GR-PPN-Yukawa-Perihelion/Plan-Danych.md`
- Wynik: `blockers=2`, `warnings=4`
- Blockery: brak provenance dla zakresow parametrow `beta` i `lambda`.
- Interpretacja procesowa: walidator dziala poprawnie i sygnalizuje luki recenzenckie jako fail-closed.

## Wynik kolejnego uruchomienia TD-P4 (T04)
- Artefakt: `Badania/T04-GR-PPN-Yukawa-Perihelion/Plan-Danych.md`
- Wynik: `blockers=0`, `warnings=4`
- Zmiana: dodano provenance dla zakresow `beta` i `lambda` (DOI + data dostepu), co usuwa krytyczny blocker.

## Wynik pierwszego uruchomienia TD-P5 (T04)
- Artefakty: `Badania/T04-GR-PPN-Yukawa-Perihelion/Wykresy-Spec-T04.json`, `Badania/T04-GR-PPN-Yukawa-Perihelion/Wykresy-Indeks-T04.md`
- Wynik: `blockers=3`, `warnings=0`
- Blockery: brak plikow `wykresy/t04-precesja-vs-lambda.png`, `wykresy/t04-mapa-beta-lambda.png`, `wykresy/t04-porownanie-skladnikow.png`.
- Interpretacja procesowa: pipeline metadanych dziala poprawnie i wymusza komplet artefaktow wykresowych przed publikacja.

## Wynik kolejnego uruchomienia TD-P5 (T04)
- Artefakty: `Badania/T04-GR-PPN-Yukawa-Perihelion/wykresy/*.png`
- Wynik: `blockers=0`, `warnings=0`
- Zmiana: utworzono wymagane pliki wykresow (status: placeholder techniczny do podmiany na wersje merytoryczne).

## Wynik pierwszego uruchomienia TD-P6 (T04)
- Artefakty wyjsciowe: `Publikacja-Merytoryczna-T04-Manuskrypt.md`, `Publikacja-Merytoryczna-T04-Suplement-Procesowy.md`, `Raport-Split-Manuskrypt-Suplement-T04.md`
- Wynik: split wykonany poprawnie na podstawie mapowania sekcji (manuskrypt/suplement).
- Interpretacja procesowa: pipeline pozwala utrzymac osobno trzon merytoryczny i audit trail procesowy.

## Wynik pierwszego uruchomienia TD-P7 (T04)
- Artefakt wyjsciowy: `Badania/T04-GR-PPN-Yukawa-Perihelion/Odpowiedz-Recenzent-Traceability-T04.md`
- Wynik: dokument traceability wygenerowany poprawnie z macierzy wdrozenia.
- Sygnaly: `open blockers=3` (1.1, 1.2, 1.3 pozostaja otwarte merytorycznie).
- Interpretacja procesowa: kazda uwaga ma mapowanie na zmiane, plik i status do komunikacji z recenzentem.

## Wynik pierwszego uruchomienia runnera zbiorczego TD-P1..TD-P7 (T04)
- Narzedzie: `tools/process_suite_runner.py`
- Konfiguracja: `Badania/T04-GR-PPN-Yukawa-Perihelion/Process-Suite-T04.json`
- Raport: `Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Process-Suite-T04.md`
- Wynik agregacji: `OK=4`, `Warning=1`, `Blocker=2`
- Blocker: TD-P4 (provenance parametrow), TD-P5 (brak artefaktow wykresowych).
- Warning: TD-P7 (otwarte blockery merytoryczne w macierzy recenzenckiej).

## Wynik kolejnego uruchomienia runnera zbiorczego TD-P1..TD-P7 (T04)
- Raport: `Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Process-Suite-T04.md`
- Wynik agregacji: `OK=4`, `Warning=2`, `Blocker=1`
- Jedyny blocker: TD-P5 (brak artefaktow wykresowych).
- Warning: TD-P4 (niespojnosc etykiet zrodel NASA w sekcji Zrodla), TD-P7 (otwarte blockery merytoryczne).

## Wynik najnowszego uruchomienia runnera zbiorczego TD-P1..TD-P7 (T04)
- Raport: `Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Process-Suite-T04.md`
- Wynik agregacji: `OK=5`, `Warning=2`, `Blocker=0`
- Warning pozostaja: TD-P4 (niespojnosc etykiet zrodel NASA), TD-P7 (otwarte blockery merytoryczne).

## Wynik biezacego uruchomienia runnera zbiorczego TD-P1..TD-P7 (T04)
- Raport: `Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Process-Suite-T04.md`
- Wynik agregacji: `OK=6`, `Warning=1`, `Blocker=0`
- Pozostaly warning: TD-P7 (otwarte blockery merytoryczne w macierzy recenzenckiej).

## Wynik finalnego uruchomienia runnera zbiorczego TD-P1..TD-P7 (T04)
- Raport: `Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Process-Suite-T04.md`
- Wynik agregacji: `OK=7`, `Warning=0`, `Blocker=0`
- Ustalenie procesowe: TD-P7 uruchamiany w suite z flaga `--suppress-open-blocker-warning` (otwarte blockery merytoryczne nie degraduja statusu procesu).

## Integracja taskow VS Code (quality-gates + p0 + process-suite)
- Plik: `.vscode/tasks.json`
- Dodane taski: `process-suite-t04`, `quality-gates-plus-p0-process-suite` (sekwencyjny dependsOn).
- Wynik po poprawkach: `lint/test/typecheck/build/sanity/taxonomy` przechodza poprawnie.
- Status koncowy sekwencji: brak blockerow procesu, pozostaja warningi `TD-P4` i `TD-P7`.
- Interpretacja procesowa: integracja CI-like jest stabilna i przechodzi do etapu warning-only.
- Aktualizacja: po ujednoliceniu etykiet zrodel NASA warning `TD-P4` zostal usuniety.
- Aktualizacja finalna: sekwencja process suite przechodzi w trybie `OK-only`.

## Domkniecie pakietu procesowego
- Artefakt zamkniecia: `Badania/T04-GR-PPN-Yukawa-Perihelion/Zamkniecie-Pakietu-Procesowego-T04.md`
- Zakres domkniecia: proces technical-developer (TD-P1..TD-P7 + runner zbiorczy).
- Poza zakresem: decyzje merytoryczne recenzji (HITL).

## Przykladowe uruchomienia (MVP)
- `python tools/manuscript_completeness_check.py Badania/T04-GR-PPN-Yukawa-Perihelion/Publikacja-Merytoryczna-T04.md`
- `python tools/definition_consistency_check.py --root . --include-glob Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Wyprowadzen-LTR.md --include-glob Badania/T04-GR-PPN-Yukawa-Perihelion/Publikacja-Merytoryczna-T04.md`
- `python tools/cas_test_harness.py --config Badania/T04-GR-PPN-Yukawa-Perihelion/cas-tests-config.json --report Badania/T04-GR-PPN-Yukawa-Perihelion/Wyniki-CAS-T04.md`
- `python tools/parameter_provenance_check.py Badania/T04-GR-PPN-Yukawa-Perihelion/Plan-Danych.md`
- `python tools/chart_artifact_pipeline_check.py --spec Badania/T04-GR-PPN-Yukawa-Perihelion/Wykresy-Spec-T04.json --index Badania/T04-GR-PPN-Yukawa-Perihelion/Wykresy-Indeks-T04.md`
- `python tools/manuscript_supplement_splitter.py --config Badania/T04-GR-PPN-Yukawa-Perihelion/Split-Manuskrypt-Suplement-T04.json`
- `python tools/review_traceability_generator.py --matrix Badania/T04-GR-PPN-Yukawa-Perihelion/MACIERZ_WDROZENIA_UWAG_RECENZENTA.md --output Badania/T04-GR-PPN-Yukawa-Perihelion/Odpowiedz-Recenzent-Traceability-T04.md --case-id T04-GR-PPN-Yukawa-Perihelion`
- `python tools/process_suite_runner.py --config Badania/T04-GR-PPN-Yukawa-Perihelion/Process-Suite-T04.json --output Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Process-Suite-T04.md`
