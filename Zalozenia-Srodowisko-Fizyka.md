# Srodowisko Agentow AI dla Fizyki (SAF) - Zalozenia


- Autor: Grzegorz Majewski
- Data: 2026-04-03
- Status: roboczy

# 1. Definicja i cel

Srodowisko Agentow AI dla Fizyki (SAF) to model operacyjny pracy badawczej, w ktorym zespol fizykow wspolpracuje z wyspecjalizowanymi agentami AI w ramach jawnego ladu metodologicznego, jakosciowego i compliance.

To nie jest tylko zestaw notebookow ani chatbot do pisania raportow. To wieloagentowy ekosystem wspierajacy caly cykl badawczy: od hipotezy i projektu badania, przez symulacje/eksperyment, po walidacje i publikowalny wynik.

W modelu SAF:
- czlowiek pozostaje wlascicielem interpretacji naukowej, oceny ryzyka i decyzji,
- agenci przejmuja prace powtarzalne: przeglad literatury, przygotowanie pipeline, kontrole jakosci danych, testy statystyczne,
- artefakty badawcze sa wersjonowane i audytowalne,
- decyzje sa podejmowane evidence-based, z jawnym poziomem pewnosci i sladami zrodlowymi.

### 1.1 SAF w prostych slowach (dla osoby bez doswiadczenia z AI)

SAF to uporzadkowany sposob pracy, w ktorym AI jest pomocnikiem, a nie autorem decyzji. W praktyce dziala to tak, ze piszesz swoje notatki i wyprowadzenia w Markdown, a agenci tylko sprawdzaja spojnosci, szukaja literatury i pilnuja standardow jakosci. Czlowiek zawsze podejmuje decyzje koncowe.

Najprostsza analogia: SAF to zespol asystentow, z ktorych kazdy ma jasno okreslona role. Jeden pilnuje spojnosci notacji, drugi robi szybki przeglad literatury, trzeci sprawdza czy wynik spelnia kryteria jakosci. Nie ma tu "magii" ani automatycznego publikowania - jest system kontroli i wsparcia.

Przykladowy przebieg pracy:
1. Naukowiec zapisuje hipoteze i zalozenia w MD.
2. Agent Discovery zbiera powiazane prace i sugeruje pytania otwarte.
3. Agent Spojnosci Formalnej sprawdza, czy notacja jest jednolita.
4. Agent Jakosci Artefaktow ocenia, czy material spelnia wymagania Gate 3.
5. Czlowiek zatwierdza lub poprawia wynik.

Wazne: agenci nie zastapią naukowca. SAF ma zmniejszyc tarcie, wykryc bledy szybciej i uporzadkowac proces.
### 1.2 Wizualizacja SAF
![agenci](Dokumentacja/SAF_PL.png)

## 2. Cel biznesowo-naukowy

Zbudowac powtarzalne srodowisko, ktore:
- skraca time-to-result dla badan,
- podnosi reprodukowalnosc i wiarygodnosc wynikow,
- zmniejsza ryzyko bledow metodologicznych i operacyjnych,
- ulatwia onboarding nowych zespolow badawczych.

## 3. Problemy, ktore rozwiazuje SAF

- Niespojne protokoly badawcze miedzy zespolami.
- Brak pelnej reprodukowalnosci wynikow (parametry, wersje danych, wersje kodu).
- Trudna traceability: hipoteza -> eksperyment -> wynik -> wniosek -> decyzja publikacyjna.
- Duzy koszt recznych czynnosci przygotowawczych i raportowych.
- Rozproszenie wiedzy miedzy notebookami, plikami lokalnymi i notatkami.
- Brak standaryzacji oceny niepewnosci i jakosci danych.

## 4. Zalozenia projektowe

- Human-in-the-loop: krytyczne decyzje naukowe sa podejmowane przez czlowieka.
- Evidence-based: kazdy wniosek ma odniesienie do danych, kodu i metody.
- Traceability by design: metadane i decyzje sa wymagane dla kazdego artefaktu.
- Segregacja kompetencji agentow: osobne role dla discovery, symulacji, statystyki, QA.
- Compliance by default: klasyfikacja danych, retencja, kontrola dostepu i audyt od poczatku.
- Iteracyjnosc: wynik przechodzi cykl hipoteza -> walidacja -> rewizja.
- Reproducibility first: kazdy wynik musi byc odtwarzalny na bazie repo i konfiguracji.
- Markdown-first: kluczowe artefakty teoretyczne powstaja w Markdown, z jawna struktura i kontraktami semantycznymi.
- Semantyczna kontrola tekstu naukowego: agenci weryfikuja spojnosci definicji, notacji i zaleznosci miedzy rozdzialami.
- Rozdzielenie faktow i wnioskow: w kazdym artefakcie jawnie oznaczamy poziom pewnosci i status argumentu.

## 5. Wymagania BR/FR/NFR dla srodowiska

### 5.1 BR (Business/Research Requirements)
- BR-01: Skracac czas od hipotezy do wyniku zwalidowanego o min. 30% w pilocie.
- BR-02: Utrzymac reprodukowalnosc wynikow na poziomie >= 90% dla badan pilotowych.
- BR-03: Zapewnic audytowalnosc decyzji i zalozen dla kazdego eksperymentu/symulacji.

### 5.2 FR (Functional Requirements)
- FR-01: Orkiestrator ma rozbijac zadanie badawcze na strumienie (discovery, model, dane, walidacja, raport).
- FR-02: Agenci musza generowac artefakty standaryzowane: plan badania, plan danych, raport walidacji.
- FR-03: System musi wymuszac rejestr decyzji i poziom pewnosci.
- FR-04: System musi mapowac traceability: hipoteza -> eksperyment -> wynik -> wniosek.
- FR-05: Quality gate musi blokowac publikacje wyniku przy brakach MUSI.

### 5.3 NFR (Non-Functional Requirements)
- NFR-01: Powtarzalnosc uruchomien pipeline >= 95%.
- NFR-02: Pelna wersjonowalnosc artefaktow i danych wejsciowych.
- NFR-03: Kontrola dostepu wg roli i klasyfikacji danych.
- NFR-04: Audytowalnosc operacji agentow i zmian konfiguracji.
- NFR-05: Czas przygotowania raportu walidacyjnego <= 1 dzien roboczy od zakonczenia runu.

## 6. Zakres kompetencyjny SAF

### 6.1 Kompetencje eksploracyjne
- Analiza literatury i stanu badan.
- Identyfikacja hipotez, ograniczen i pytan otwartych.

### 6.2 Kompetencje strukturyzujace
- Budowa planu badania, slownika pojec i struktury danych.
- Standaryzacja konfiguracji symulacji/eksperymentu.
- Definicja kontraktow semantycznych dla artefaktow teoretycznych (definicje, twierdzenia, zalozenia, ograniczenia).

### 6.3 Kompetencje diagnostyczne
- Wykrywanie anomalii danych i bledow metodologicznych.
- Ocena wrazliwosci wyniku na parametry.
- Wykrywanie niespojnosci notacji, niejawnych zalozen i luk w argumentacji.

### 6.4 Kompetencje projektowe
- Generowanie wariantow eksperymentu/symulacji.
- Propozycja minimalnego zestawu testow walidacyjnych.

### 6.5 Kompetencje kontrolne
- Walidacja statystyczna, niepewnosci i biasu.
- Kontrola spelnienia quality gate.
- Walidacja formalna wyprowadzen z uzyciem narzedzi symbolicznych (CAS) tam, gdzie to mozliwe.

### 6.6 Kompetencje organizacyjne
- Budowa pamieci projektowej i katalogu decyzji.
- Wykrywanie duplikacji badan i rekomendacje reuse.

## 7. Architektura SAF - model warstwowy

- Warstwa interakcji: fizyk i lider badania zarzadzaja zadaniami.
- Orkiestrator badan: planuje DAG zadan i sekwencje agentow.
- Agenci specjalistyczni: discovery, modelowanie, symulacje, statystyka, QA.
- Pamiec robocza i dlugotrwala: kontekst sesyjny i repo wiedzy badawczej.
- Repozytorium wiedzy: literatura, notatki, protokoly, wyniki, decyzje.
- Warstwa integracji: HPC, repo kodu, storage danych, system publikacyjny.
- Warstwa polityk: guardrails danych, retencja, dostep, etyka badan.
- Warstwa audytu: logi, wersje, metryki jakosci i reprodukowalnosci.

## 8. Role w modelu docelowym

### 8.1 Role ludzkie

- Principal Investigator / Lead Physicist
  - Wlasciciel celu badawczego i decyzji naukowych.
- Research Physicist
  - Walidacja interpretacji wynikow i modelu fizycznego.
- Computational Physicist
  - Odpowiedzialnosc za implementacje i wydajnosc obliczen.
- Data Steward
  - Jakosc danych, lineage, retencja i klasyfikacja.
- Statistics Reviewer
  - Weryfikacja testow statystycznych i niepewnosci.
- Security/Compliance Officer
  - Kontrola obszarow regulacyjnych i danych wrazliwych.
- Delivery/Operations Manager
  - Planowanie przepustowosci zasobow (HPC, storage, terminy).

### 8.2 Role agentowe

- Agent Orkiestrator Badan
  - Misja: zarzadzanie cyklem zycia badania od hipotezy do publikacji.
  - Zadania: rozbijanie zlozonych problemow fizycznych na strumienie (discovery, model, walidacja), pilnowanie przejsc miedzy bramkami jakosciowymi (Quality Gates).
  - Interakcja: Twoj plan badania wymaga zatwierdzenia Gate 1. Czy chcesz, abym teraz uruchomil Agenta Discovery?
- Agent Discovery Naukowy
  - Misja: mapowanie krajobrazu wiedzy i identyfikacja luk badawczych.
  - Zadania: analiza literatury (ArXiv), formulowanie pytan otwartych i budowa mapy hipotez w plikach MD.
  - Interakcja: Zidentyfikowalem trzy sprzeczne hipotezy dotyczace energii prozni w Twoim modelu. Oto ich zestawienie.
- Agent Modelu Fizycznego
  - Misja: straznik poprawnosci formalnej i fizycznej opisu.
  - Zadania: weryfikacja rownan LaTeX, sprawdzanie zalozen (np. zasady zachowania) i warunkow brzegowych.
  - Interakcja: W rownaniu (4.2) brakuje czynnika relatywistycznego $\gamma$, co jest niespojne z Twoim zalozeniem $v \approx c$.
- Agent Symulacji/Eksperymentu
  - Misja: projektowanie weryfikacji numerycznej dla teorii.
  - Zadania: proponowanie scenariuszy testowych (runow) i optymalnej konfiguracji parametrow dla modeli.
  - Interakcja: Aby sprawdzic stabilnosc tego rozwiazania, proponuje 100 symulacji typu Monte Carlo w zakresie $T \in [0, 100] K$.
- Agent Jakosci Danych
  - Misja: detekcja anomalii w danych wejsciowych i wynikowych.
  - Zadania: walidacja brakow, wykrywanie outlierow oraz identyfikacja driftu w seriach czasowych danych.
  - Interakcja: Zbior danych 'result_v1.csv' zawiera 5% wartosci NaN w kolumnie pedu. Zalecam re-kalibracje.
- Agent Statystyki i Niepewnosci
  - Misja: kwantyfikacja pewnosci wynikow naukowych.
  - Zadania: dobor testow statystycznych, wyliczanie przedzialow ufnosci i analiza wrazliwosci modelu na zmiany parametrow.
  - Interakcja: Przy obecnej wielkosci probki, przedzial ufnosci dla masy czastki wynosi $\pm 12\%$. Czy to akceptowalne?
- Agent Ryzyka i Zgodnosci
  - Misja: mitygacja ryzyk metodologicznych i operacyjnych.
  - Zadania: ocena ryzyk regulacyjnych, etycznych oraz zgodnosci z polityka retencji danych.
  - Interakcja: Ostrzezenie: wykorzystane dane z zewnetrznego repozytorium wymagaja licencji CC-BY. Dodaj cytowanie.
- Agent Jakosci Artefaktow
  - Misja: koncowa kontrola jakosci przed "wysylka".
  - Zadania: sprawdzanie spojnosci miedzy plikami (np. czy raport koncowy odpowiada hipotezie). Nadawanie statusu: pass / pass-with-comments / fail.
  - Interakcja: Status: pass-with-comments. Wszystkie testy zaliczone, ale brak opisu niepewnosci systematycznej.
- Agent Repozytorium Wiedzy
  - Misja: pamiec instytucjonalna i unikanie duplikacji.
  - Zadania: indeksowanie wynikow, wykrywanie mozliwosci ponownego uzycia (reuse) metod lub fragmentow teorii.
  - Interakcja: Podobny model matematyczny byl testowany w projekcie 'DarkMatter_2024'. Sprawdz tamtejsze wnioski.
- Agent Spojnosci Formalnej
  - Misja: straznik notacji i logiki dokumentu.
  - Zadania: sprawdzanie, czy symbole zdefiniowane na poczatku (np. $\hbar=1$) sa stosowane konsekwentnie w calym repozytorium MD.
  - Interakcja: W sekcji 'Metryka' uzywasz sygnatury $(-,+,+,+)$, ale w sekcji 'Lagranżjan' obliczenia sugeruja $(+,-,-,-)$. Prosze o ujednolicenie.
- Agent Cross-Reference
  - Misja: lacznik ze swiatowa literatura w czasie rzeczywistym.
  - Zadania: mapowanie fragmentow Twojego tekstu MD na publikacje z ArXiv/ADS; wskazywanie podobienstw i rozbieznosci z istniejacymi teoriami.
  - Interakcja: Twoje wyprowadzenie tenzora energii-pedu jest identyczne z modelem zaproponowanym przez Smitha (2025). Czy chcesz dodac odniesienie?
- Agent Socratic Mentor
  - Misja: krytyczny sparring partner (Reviewer #2).
  - Zadania: testowanie granic zalozen poprzez pytania o przypadki graniczne, osobliwosci i konsekwencje logiczne.
  - Interakcja: Co dzieje sie z Twoim rozwiazaniem, gdy masa dazy do nieskonczonosci? Czy nie prowadzi to do niefizycznej osobliwosci w punkcie $r=0$?

### 8.3 Profil LTR (tryb hybrydowy)

- Tryb domyslny: hybrydowy (przelaczanie na poziomie pliku i sekcji).
- Oznaczenia sekcji: [TRYB: FORMALNY] i [TRYB: BADACZ].
- Walidacja formalna: srednia restrykcyjnosc, CAS SymPy dla newralgicznych krokow.
- Artefakty LTR: kontrakt semantyczny, raport wyprowadzen, rejestr walidacji formalnej, checklista Gate 3 (teoria), mapa notacji, cross-reference log.

## 9. Model wspolpracy czlowiek-agent

- Czlowiek definiuje cel badawczy, ograniczenia i kryteria sukcesu.
- Orkiestrator tworzy plan strumieni i uruchamia agentow specjalistycznych.
- Agenci generuja artefakty robocze i pytania otwarte.
- Czlowiek zatwierdza metody, odrzuca tresci niskiej pewnosci i finalizuje wynik.
- Agent jakosci wykonuje quality gate przed publikacja.

### Trzy poziomy akceptacji
- Akceptacja robocza: Lead Physicist/Research Physicist.
- Akceptacja metodologiczna: Statistics Reviewer/Computational Physicist.
- Akceptacja compliance: Security/Compliance dla danych wrazliwych/regulowanych.

## 10. Quality gate dla badan

### Gate 1 - Gotowosc projektu badania
- Hipoteza i cel mierzalny sa jawne.
- Zakres i wykluczenia sa zapisane.
- Plan eksperymentu/symulacji jest kompletny.
- Traceability od hipotezy do metryk jest zdefiniowane.
- Akceptacja: wylacznie czlowiek (Principal Investigator).

### Gate 2 - Gotowosc danych i metody
- Klasyfikacja danych i podstawa przetwarzania sa potwierdzone.
- Kontrole dostepu i retencja sa zdefiniowane.
- Ryzyko metodologiczne i operacyjne ma ownera i plan mitygacji.
- Akceptacja: wylacznie czlowiek (Principal Investigator).

### Gate 3 - Jakosc wyniku
- Wynik jest reprodukowalny (kod, dane, parametry, wersje).
- Niepewnosc i wrazliwosc sa policzone i opisane.
- Wnioski sa oddzielone od faktow i poziom pewnosci jest jawny.
- Dla badan teoretycznych: wyprowadzenie jest odtwarzalne z jawnych zalozen, definicji i lematow.
- Dla badan teoretycznych: brak sprzecznosci notacji i definicji pomiedzy rozdzialami.
- Dla badan teoretycznych: kluczowe kroki algebraiczne przechodza walidacje CAS lub sa oznaczone jako wymagajace recznej weryfikacji.
- Akceptacja: mozliwy tryb agent-conditional pass dla wynikow niskiego ryzyka, pod warunkiem statusu pass bez komentarzy krytycznych od Agenta Jakosci Artefaktow.

### Gate 4 - Publikacja/transfer
- Decyzje i akceptacje sa kompletne.
- Artefakt spelnia wymagania raportowe organizacji.
- Plan rollback/awaryjny istnieje dla badan wysokiego ryzyka.
- Akceptacja: bezwzglednie czlowiek + Statistics Reviewer.

## 11. Minimalne artefakty do uruchomienia

1. Karta badania (cel, zakres, hipoteza, ownerzy).
2. Research Design (model, metody, parametry, ograniczenia).
3. Plan danych (zrodla, klasyfikacja, retencja, dostep).
4. Plan walidacji (testy, metryki, kryteria pass/fail).
5. Rejestr decyzji i ryzyk.
6. Raport wynikowy (fakty, analiza, niepewnosc, rekomendacja).
7. Kontrakt semantyczny artefaktu teoretycznego (definicje, twierdzenia, zalozenia, ograniczenia).
8. Rejestr walidacji formalnej (status CAS, reczna weryfikacja, niepewne kroki).

## 12. Literate Theoretical Research (LTR) - doprecyzowania

LTR zaklada, ze podstawowe wyprowadzenia i argumenty teoretyczne sa tworzone jako artefakty Markdown, a system agentowy zapewnia semantyczna kontrole spojnosci.

### Kontrakty semantyczne (Markdown-first)
- Definicje: kazdy nowy symbol lub obiekt musi miec jawna definicje.
- Tezy/Twierdzenia: jawny zakres, warunki i status (robocza/zweryfikowana).
- Dowody: kroki oznaczone, w tym punkty wymagajace CAS lub recznej weryfikacji.
- Ograniczenia: jawne warunki brzegowe i zakres stosowalnosci.

### LTR - kontrole jakosci
- Lint matematyczny: wykrywanie skokow logicznych, zmian notacji i brakow warunkow brzegowych.
- Analiza wymiarowa: automatyczna kontrola zgodnosci jednostek tam, gdzie to mozliwe.
- Cross-reference literatury: oznaczanie podobienstw i rozbieznosci z istniejacymi pracami.

### LTR - mitygacja problemu "Parsed Math"
- Integracja z CAS (np. SymPy/WolframAlpha) jako warunek potwierdzenia kluczowych przeksztalcen.
- Wymuszenie krokowej postaci wyprowadzen w newralgicznych fragmentach.

### Przyklady LTR
- Tagowanie rownania:
  $$E = mc^2$$
  [EQ:ENERGY-01]
- Oznaczenie kroku do walidacji: [VERIFY-CAS] przy nietrywialnym przeksztalceniu.
- Powiazane artefakty (format [ID:Typ]): [LTR-DERIV-001:Raport], [LTR-VAL-001:Walidacja].
- Globalne zalozenia jednostkowe: c=1, hbar=1 w mapie notacji.

## 13. Ustalenia pilota i polityki LTR (v1)

### Zakres pilota (2-3 case'y teoretyczne)
- Case A (analityczny): wyprowadzenie nowej poprawki do istniejacego lagranjanu; cel: spojnosc notacji i brak bledow w algebraicznym "copy-pasting".
- Case B (numeryczno-teoretyczny): walidacja stabilnosci rozwiazania analitycznego przez proste skrypty (np. Python/SymPy); cel: integracja agenta modelu z agentem symulacji.
- Case C (przegladowy/hipoteza): synteza nowej hipotezy na podstawie 20 najnowszych preprintow z ArXiv; cel: test Agenta Discovery i Cross-Reference.

### Przyklady artefaktow dla case'ow
- Case A (analityczny)
  - Kontrakt semantyczny: [LTR-CONTRACT-A01:Kontrakt]
  - Raport wyprowadzen: [LTR-DERIV-A01:Raport]
  - Rejestr walidacji: [LTR-VAL-A01:Walidacja]
  - Mapa notacji: [LTR-NOT-A01:Notacja]
  - Przyklad tagowania: $$\Delta\mathcal{L} = \alpha R^2$$
    [EQ:DL-01]
    [VERIFY-CAS]
- Case B (numeryczno-teoretyczny)
  - Raport wyprowadzen: [LTR-DERIV-B01:Raport]
  - Rejestr walidacji: [LTR-VAL-B01:Walidacja]
  - Cross-reference log: [LTR-XREF-B01:CrossRef]
  - Przyklad powiazan: [LTR-DERIV-B01:Raport], [LTR-VAL-B01:Walidacja], [LTR-XREF-B01:CrossRef]
- Case C (przegladowy/hipoteza)
  - Kontrakt semantyczny: [LTR-CONTRACT-C01:Kontrakt]
  - Cross-reference log: [LTR-XREF-C01:CrossRef]
  - Checklista Gate 3: [LTR-G3-C01:Gate3]
  - Przyklad tagu literatury: arXiv:2026.12345 (preprint)

### Poziomy formalizacji
- Tryb badacza (discovery): luzne notatki w MD, brak wymogu pelnej traceability; agenci dzialaja jako Socratic Mentors.
- Tryb formalny (validation/CAS): wymagany od momentu zamrozenia Research Design; kazde rownanie ma przypisany poziom pewnosci i zrodlo.

### Reguly walidacji i CAS
- Kluczowy krok: kazde nietrywialne przejscie matematyczne oznacz tagiem [VERIFY-CAS].
- Agent Spojnosci Formalnej wysyla oznaczone fragmenty do walidacji (SymPy lub inny CAS).
- Brak walidacji: oznacz w metadanych jako status unverified i pokaz w raporcie.

### Sposob pracy z literatura
- Zrodla: priorytet ArXiv (preprinty) oraz ADS/DOI (recenzowane).
- Format: BibTeX zintegrowany z plikami MD.
- Poziom zaufania: agenci oznaczaja preprint vs peer-reviewed i flaguja wnioski oparte wyylacznie na preprintach.
- PDF: dokumenty wejsciowe sa odczytywane i indeksowane (ekstrakcja tekstu z warstwy tekstowej; OCR opcjonalnie dla skanow), tak by agenci mieli pelny dostep do tresci.

### Polityka danych (LtrDataPolicy)
- Klasyfikacja: publiczne (literatura), wewnetrzne (notatki), poufne (odkrycia przed publikacja).
- Retencja: artefakty badawcze przechowywane 5-10 lat.
- Licencje: kod symulacyjny MIT/GPL, tresc MD CC-BY-NC-ND.

### Standard repozytorium
- Struktura: zgodna ze schematem v1 (Dokumentacja/Szablony/Agenci).
- Naming: wersjonowanie semantyczne (np. Hypothesis-v1.2.0-alpha).
- Decyzje: rejestrowane w pliku DECISIONS.md z linkami do commitow.

## 14. Struktura repozytorium (v1)

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

## 15. Plan wdrozenia (propozycja)

### Etap 1 (0-2 miesiace): Standaryzacja
- Zdefiniowac szablony artefaktow i slownik pojec.
- Wybrac 2-3 scenariusze pilotowe.

### Etap 2 (2-4 miesiace): Pilotaz
- Uruchomic orkiestrator + 3 agentow (discovery, data quality, statystyka).
- Mierzyc czas i jakosc wzgledem sposobu tradycyjnego.

### Etap 3 (4-8 miesiecy): Governance
- Wlaczyc quality gate, audyt, retencje i kontrole dostepu.
- Dookreslic polityke akceptacji (human-only vs agent-conditional).

### Etap 4 (8-12 miesiecy): Skalowanie
- Rozszerzyc katalog agentow i integracje z HPC/repo.
- Uruchomic pamiec wiedzy i reuse wzorcow badan.

## 16. Metryki sukcesu

### Efektywnosc
- Time-to-Result: redukcja >= 30% w pilocie.
- Lead time raportu walidacji: <= 1 dzien.

### Jakosc
- Reproducibility Score: >= 90%.
- Consistency Score artefaktow: >= 85%.
- Odsetek runow wymagajacych ponownego uruchomienia z powodow jakosciowych: < 15%.
- Odsetek wyprowadzen teoretycznych z potwierdzona walidacja formalna: >= 70% w pilocie.
- Wykrycie przez agentow min. 1 bledu formalnego/rachunkowego przed Gate 3.
- Odtworzenie toku rozumowania i obliczen przez drugiego fizyka w czasie < 2h.

### Organizacyjne
- Reuse Rate metod i artefaktow: >= 25%.
- CSAT interesariuszy naukowych: >= 4.2/5.

## 17. Ryzyka i mitygacje

### Ryzyka biznesowe
- Niski poziom adopcji przez zespoly.
- Mitygacja: pilotaz na realnych use-case i mierzalne KPI.

### Ryzyka systemowe
- Brak reprodukowalnosci przez niespojne srodowiska uruchomieniowe.
- Mitygacja: standaryzacja runtime, lock wersji, konteneryzacja.

### Ryzyka regulacyjne
- Nieuprawnione przetwarzanie danych wrazliwych.
- Mitygacja: klasyfikacja danych, kontrola dostepu, audyt i zatwierdzenia.

### Ryzyka operacyjne
- Braki MUSI blokujace gate bez ownera i SLA.
- Mitygacja: RACI + SLA eskalacji, dziennik blokad i rewizji.

### Ryzyka LTR (Literate Theoretical Research)
- Bledne tagowanie rownan i artefaktow (np. brak [EQ:ID], niepoprawny format [ID:Typ]).
- Mitygacja: walidacja szablonow, automatyczny lint tagow, checklista Gate 3.
- Falszywie pozytywna walidacja CAS lub pomijanie warunkow brzegowych.
- Mitygacja: wymaganie uzasadnienia, oznaczanie krokow jako unverified i reczna weryfikacja kluczowych krokow.
- Niespojnosci notacji wynikajace z trybu hybrydowego.
- Mitygacja: mapa notacji + globalne zalozenia jednostkowe + Agent Spojnosci Formalnej.
- Nadmierne poleganie na literaturze nierecenzowanej (preprinty).
- Mitygacja: oznaczanie poziomu zaufania, flagowanie wnioskow opartych tylko na preprintach.

## 18. Wymagane decyzje i ownerzy

1. Model akceptacji (human-only czy agent-conditional).
- Wlasciciel decyzji biznesowej: Principal Investigator / Business Owner.
- Wlasciciel decyzji technicznej: Lead Physicist + Security/Compliance.

2. Zakres danych dopuszczonych do pracy agentowej.
- Wlasciciel decyzji biznesowej: Data Owner.
- Wlasciciel decyzji technicznej: Data Steward + Security.

3. Minimalny zestaw metryk quality gate.
- Wlasciciel decyzji biznesowej: Lead Physicist.
- Wlasciciel decyzji technicznej: Statistics Reviewer.

## 19. Sekcja compliance (minimum)

- Klasyfikacja danych: public/internal/confidential/restricted.
- Podstawa przetwarzania: opis i owner.
- Retencja i usuwanie: okres, mechanizm, owner.
- Kontrola dostepu: role i uprawnienia.
- Audytowalnosc: co logujemy, gdzie i jak dlugo.
- Role zatwierdzajace: Biznes, Security, Compliance.
- Ocena ryzyka regulacyjnego: niskie/srednie/wysokie.
- Rollback i plan awaryjny: wymagane dla obszarow wysokiego ryzyka.

## 20. Akceptacje

- Status akceptacji: draft
- Typ akceptacji: DO UZUPELNIENIA
- Wlasciciel biznesowy: DO UZUPELNIENIA
- Wlasciciel techniczny: DO UZUPELNIENIA
- Security/Compliance: DO UZUPELNIENIA
- Data ostatniej aktualizacji: 2026-04-03

## 21. Decyzje

| ID | Decyzja | Uzasadnienie biznesowe | Uzasadnienie techniczne | Wlasciciel | Data | Powiazane wymaganie | Powiazane ryzyko | Status |
|---|---|---|---|---|---|---|---|---|
| DEC-001 | Uruchomic pilotaż SAF dla 2-3 przypadkow badawczych | Skrócenie czasu i poprawa jakosci wynikow | Walidacja modelu pracy przed skalowaniem | Grzegorz Majewski | 2026-04-03 | BR-01, BR-02 | R-OPS-01 | open |
| DEC-002 | Wprowadzic quality gate reprodukowalnosci przed publikacja | Ograniczenie ryzyka blednych wnioskow | Sprawdzenie odtwarzalnosci wynikow i konfiguracji | Grzegorz Majewski | 2026-04-03 | FR-05, NFR-01 | R-SYS-01, R-REG-01 | open |
| DEC-003 | Ustalic polityke akceptacji agentowej dla projektu | Jasna odpowiedzialnosc i audyt | Spojnosc dzialania orkiestratora i eskalacji | Grzegorz Majewski | 2026-04-03 | FR-03 | R-OPS-02 | open |
