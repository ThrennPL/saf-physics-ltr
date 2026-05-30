# Copilot instructions (SAF + LTR)

Jezyk: PL. Preferuj ASCII. Markdown-first.

## Zasady ogolne
- Czlowiek jest wlascicielem decyzji naukowych (human-in-the-loop).
- Nie zatwierdzaj gate bez czlowieka, nawet jesli wszystko wyglada dobrze.
- Oddzielaj fakty od wnioskow i oznaczaj poziom pewnosci.
- Nie zgaduj brakujacych danych; pytaj, oznaczaj jako DO_UZUPELNIENIA.
- Pracuj delegation-first: zadania przekazuj do wlasciciela roli, a delegacje zapisuj minimum jako kto, dlaczego, ETA.

## Artefakty i formaty
- Uzywaj formatow z Dokumentacja/Szablon-LTR oraz Dokumentacja/Szablon-Fizyka.
- Dla fizyki teoretycznej uzywaj pakietow: Experiment Context, Measurement Integrity, Risk and Safety, Reproducibility.
- Powiazania zapisz w formacie [ID:Typ].
- Taguj rownania w raportach: po wzorze w osobnej linii dodaj tag w formacie EQ:ID.
- Nietrywialne kroki oznaczaj [VERIFY-CAS].
- Standard raportowania: status OK/Warning/Blocker; pewnosc skala 0-1 (liczbowa); pytania Q-XXX z priorytetem niski/sredni/wysoki.
- ADS: jesli korzystasz z ADS, wymagaj ADS_API_TOKEN w .env.

## LTR
- Dla trybu formalnego wymagaj jawnych zalozen, definicji i krokow.
- Sprawdzaj spojnosc notacji z mapa notacji.
- Dla PDF: zakladaj ekstrakcje tekstu z warstwy tekstowej; OCR jest opcjonalny.

## Jakosci i gate
- Gate 1/2/4: akceptacja tylko czlowiek.
- Gate 3: mozliwy agent-conditional pass dla niskiego ryzyka i tylko przy statusie OK bez komentarzy krytycznych.
- Nie zatwierdzaj gate bez czlowieka, z wyjatkiem Gate 3 w trybie agent-conditional pass.
- Dla fizyki teoretycznej domyslne progi confidence: 0.85/0.70/0.50 (do doprecyzowania w projekcie).
- Statusy agentow sa robocze i nie stanowia decyzji gate.
- Semantyka statusow: OK = brak krytycznych ryzyk; Warning = ryzyka/braki niekrytyczne; Blocker = braki krytyczne lub sprzecznosci.
- Brak wymaganych danych lub niespelnione warunki gate => fail_closed (Blocker + natychmiastowa eskalacja do Orkiestratora i dalej do czlowieka).

## Runtime krytyczny (bez placeholderow)
- Ownership konfliktu: notacja/ID -> Formal Consistency; konflikt fizyczny/merytoryczny -> Model Review; konflikt danych -> Data Quality (z konsultacja Statistics Review).
- Eskalacja: kazdy Blocker lub konflikt nierozstrzygniety eskaluj natychmiast do Orkiestratora i dalej do czlowieka.

## Placeholder Policy v1
- Placeholder DO_UZUPELNIENIA jest dozwolony tylko w konfiguracji domenowej (np. zakres, progi, slowa kluczowe, narzedzia).
- Placeholder jest zakazany w runtime krytycznym: decyzja gate, ownership konfliktu, eskalacja, fallback.
- Kazdy placeholder musi miec metadane: owner, ttl, fail_closed; brak metadanych lub wygasly TTL => fail_closed.

## Zaleznosci agentow
- Formal Consistency rozstrzyga konflikty notacji i ID.
- Model Review rozstrzyga konflikty fizyczne i merytoryczne.
- Data Quality -> Statistics Review (jakosc danych warunkiem analizy).
- Discovery -> Cross-Reference (slowa kluczowe i zakres literatury).
- Language Polish Quality -> Artifact Quality (obowiazkowa walidacja jezykowa przed finalizacja dokumentow).
- Artifact Quality konsoliduje wyniki i statusy z pozostalych agentow.
- Prace implementacyjne i automatyzacje kodu deleguj do Technical Developer (Python-first).

## Walidacja jezykowa (PL) - wymagana
- Kazdy dokument .md przeznaczony do recenzji lub eksportu PDF musi przejsc przez Agenta Polskiego Jezyka i Skladni.
- Walidacja jezykowa jest obowiazkowym krokiem przed rekomendacja gate i przed wysylka materialow.
- Agent jezykowy nie moze zmieniac tresci merytorycznej, rownan, ID i tagow EQ.
- Wynik walidacji jezykowej raportuj jako status OK/Warning/Blocker z pewnoscia 0-1.

## Bramka wlaczenia Technical Developer
- Trigger: uruchom Technical Developer, gdy wystepuje przynajmniej jeden warunek: (a) potrzeba patcha kodu/skryptu, (b) awaria narzedzia blokuje przejscie gate, (c) potrzebna jest automatyzacja kontroli jakosci artefaktow.
- Owner decyzji: Orkiestrator; Gate 1/2/4 pozostaje decyzja czlowieka.
- Minimalne wejscia: brief techniczny, oczekiwany output, zakres zmian, ograniczenia ryzyka, ETA.
- Minimalne wyjscia: patch lub plan zmian, wynik testu/uruchomienia, status OK/Warning/Blocker, lista Q-XXX i DO_UZUPELNIENIA.

## Minimalna mapa narzedzi wspierajacych (MVP)
- Research Orchestrator: tools/route_model.py (routing modelu i kolejkowanie zadan).
- Cross-Reference: tools/arxiv_search.py, tools/ads_search.py (kwerendy literatury).
- Formal Consistency: tools/lint_ltr.py (kontrola tagow i spojnosci LTR).
- Statistics Review: tools/mcp_baseline.py, tools/build_evidence_packet.py (runbook + pakietowanie tabel niepewnosci).
- Simulation/Experiment: tools/mcp_baseline.py, tools/lint_ltr.py, tools/build_evidence_packet.py (runbook + kontrola ID/EQ + pakietowanie wariantow).
- Risk Compliance: tools/security_sanity_check.py (podstawowy sanity-check ryzyk technicznych).
- Knowledge Repo: tools/taxonomy_guard.py, tools/build_evidence_packet.py (normalizacja i pakietowanie artefaktow).
- Artifact Quality: tools/build_evidence_packet.py, tools/taxonomy_guard.py (kontrola kompletnosci i spojnosci paczki).
- Pozostale role (Data Quality, Model Review, Physics Discovery, Socratic Mentor): dzialanie proceduralne do czasu doprecyzowania dedykowanych narzedzi domenowych.

## Zachowanie modelu
- Nie halucynuj literatury; oznacz poziom zaufania i preprint vs peer-reviewed.
- Nie edytuj tresci merytorycznej bez zgody; proponuj zmiany.
- Jesli brak danych, dodaj sekcje "Miejsca do doprecyzowania".
- Protokol brakow danych: napisz wprost "Nie wiem" dla brakujacego faktu i nie uzupelniaj go domyslem.
- Dla kazdej luki podaj: czego brakuje, dlaczego blokuje decyzje i jaki minimalny input jest potrzebny.
- Zakoncz odpowiedz lista pytan uzupelniajacych (Q-XXX) do wlasciciela danych.
