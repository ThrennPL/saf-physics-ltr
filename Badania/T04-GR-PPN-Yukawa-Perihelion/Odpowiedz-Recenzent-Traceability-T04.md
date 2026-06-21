# Odpowiedz dla recenzenta - traceability

## Metadane
- Case: T04-GR-PPN-Yukawa-Perihelion
- Data generacji: 2026-06-21 01:27:39 UTC
- Zrodlo: D:/grzegorz/programowanie/Theoretical MD/Badania/T04-GR-PPN-Yukawa-Perihelion/MACIERZ_WDROZENIA_UWAG_RECENZENTA.md
- Liczba uwag: 12
- Otwarte uwagi: 0
- Otwarte blockery: 0

## Tabela mapowania uwaga -> zmiana -> plik -> status
| ID uwagi | Priorytet | Status | Zmiana | Plik(i) | Kryterium domkniecia | Ocena ryzyka |
|---|---|---|---|---|---|---|
| 1.1 Pelne wyprowadzenie Yukawy | Blocker | DONE | Domknieto formalny ciag potencjal->sila->Binet->perturbacja oraz kryteria recenzenckie w artefakcie blokera i publikacji | T04-BLOCKER-001-WYPROWADZENIE-YUKAWA-BINET.md, Raport-Wyprowadzen-LTR.md, Publikacja-Merytoryczna-T04.md | Ciag rachunkowy jawny, bez ukrytych zalozen, recenzent moze przejsc krok po kroku | OK |
| 1.2 Uzasadnienie F(e) | Blocker | DONE | Domknieto uzasadnienie F(e) w trybie mieszanym: formalnym, literaturowym i numerycznym (ODE/Binet) | T04-BLOCKER-001-WYPROWADZENIE-YUKAWA-BINET.md, T04-NUM-VAL-001.md, Cross-Reference-Log-LTR.md, Publikacja-Merytoryczna-T04.md | F(e) nie wystepuje jako "roboczo", tylko jako uzasadnione matematycznie/literaturowo | OK |
| 1.3 Spojnosc definicji R | Blocker | DONE | Utrzymano jedna definicje R_Y=\|DeltaY\|/\|Delta1PN\|w tekscie i CAS oraz dopisano interpretacje | Raport-Wyprowadzen-LTR.md, Wyniki-CAS-T04.md, Publikacja-Merytoryczna-T04.md | Tozsama definicja i granice w kodzie oraz tekscie | OK |
| 2.1 Rozszerzenie CAS | High | DONE | Dodano niezalezna walidacje numeryczna ODE/Binet (raport, CSV, wykresy) i opis ograniczen numerycznych | tools/binet_numeric_validation_t04.py, T04-NUM-VAL-001.md, T04-NUM-VAL-DATA.csv, Rejestr-Walidacji-Formalnej-LTR.md | Testy fizyczne PASS + opis ograniczen numerycznych | OK |
| 2.2 Zakresy beta i lambda | High | DONE | Uzupelniono uzasadnienie zakresow parametrow z DOI i komentarzem ograniczen | Plan-Danych.md, Cross-Reference-Log-LTR.md, Publikacja-Merytoryczna-T04.md | Kazdy zakres ma zrodlo, DOI i komentarz ograniczenia | OK |
| 2.3 Analiza czulosci | High | DONE | Dodano mape (beta,lambda)->DeltaY oraz komplet wykresow z opisami merytorycznymi | Plan-Danych.md, Raport-Wynikowy.md, Publikacja-Merytoryczna-T04.md | Co najmniej 3 wykresy i opis regionow | OK |
| 3.1 Porownanie z obserwacjami | High | DONE | Dodano benchmark obserwacyjny, test zgodnosci skali i kryterium ograniczen parametrow | Plan-Danych.md, Raport-Wynikowy.md, Publikacja-Merytoryczna-T04.md | Wyznaczone dopuszczalne beta/lambda i regiony wykluczone | OK |
| 3.2 Constraints fifth force | High | DONE | Dodano rozdzial porownawczy constraints (SS/LLR/lab) i powiazano z claim->source | Publikacja-Merytoryczna-T04.md, Cross-Reference-Log-LTR.md | Sekcja constraints z tabela porownawcza | OK |
| 3.3 Wykresy | High | DONE | Wykresy osadzone i opisane merytorycznie w publikacji; pliki wygenerowane i zweryfikowane | Publikacja-Merytoryczna-T04.md, wykresy/*.png | Wykresy osadzone i opisane | OK |
| 4.1 Rozdzielic proces vs fizyka | Medium | DONE | Workflow/gate pozostawiono w suplementach i artefaktach procesowych, trzon fizyki utrzymano w manuskrypcie | Publikacja-Merytoryczna-T04.md, Dokument-Dla-Recenzenta.md | IMRaD-like trzon bez nadmiaru procesowego | OK |
| 4.2 Rozbudowa matematyki | Medium | DONE | Dodano rownania posrednie, rozszerzony szkic Bineta i artefakt dedykowany blockerowi 1.1/1.2 | Raport-Wyprowadzen-LTR.md, T04-BLOCKER-001-WYPROWADZENIE-YUKAWA-BINET.md, Publikacja-Merytoryczna-T04.md | Brak skokow rachunkowych | OK |
| 4.3 Rozszerzenie bibliografii | Medium | DONE | Uzupelniono bibliografie bazowa i claim->source, wraz z sekcja constraints | Cross-Reference-Log-LTR.md, Publikacja-Merytoryczna-T04.md | Bibliografia pokrywa wszystkie kluczowe twierdzenia | OK |

## Uwagi
- Dokument jest generowany automatycznie z macierzy wdrozenia.
- Braki statusow merytorycznych pozostaja decyzja wlasciciela badania (HITL).
