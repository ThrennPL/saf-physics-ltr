# Dokument dla recenzenta

## Metadane
- ID: T04-REVIEW-001
- Case: T04-GR-PPN-Yukawa-Perihelion
- Data: 2026-06-21
- Status: gotowe do ponownej recenzji (runda Major Revision)
- Wejscie: PLAN_POPRAWEK_RECENZENT.md

## Cel pakietu dla recenzenta
Ten dokument konsoliduje uzupelnienia i statusy wdrozenia dla punktow 1.1-4.3 z planu poprawek, tak aby recenzja merytoryczna mogla zostac wykonana na jednym, spojnym pakiecie danych i artefaktow.

## Zakres merytoryczny i dane przekazane do oceny
- Model: precesja peryhelium jako suma skladowej 1PN i skladowej Yukawa.
- Walidacja rachunkowa: LTR + [VERIFY-CAS].
- Propagacja niepewnosci: Monte Carlo, N=120000.
- Miary raportowania: na orbite oraz arcsec/century.
- Parametry i zrodla: Plan-Danych.md (NIST, NASA arch., DOI dla ograniczen beta/lambda).

## Najwazniejsze liczby przekazane recenzentowi
- CI (arcsec/century):
  - delta_phi_total: srednia 42.981438, p2.5 42.966851, p97.5 42.995860,
  - delta_phi_1PN: srednia 42.981448, p2.5 42.970786, p97.5 42.992145,
  - delta_phi_Y: srednia -0.000010, p2.5 -0.010866, p97.5 0.010882.
- [VERIFY-CAS] PASS: granice beta->0, lambda->inf, zachowanie wskaznika R, sanity-check 1PN Merkurego.
- Walidacja ODE/Binet: wykonana (T04-NUM-VAL-001 + T04-NUM-VAL-DATA.csv), z wynikiem PARTIAL dla kryterium epsilon<5%.

## Matryca pokrycia planu poprawek (1.1-4.3)
| ID uwagi | Status wdrozenia | Co zostalo uzupelnione w pakiecie | Artefakt glowny |
|---|---|---|---|
| 1.1 Pelne wyprowadzenie Yukawy | DONE | Dostepny jawny ciag formalny oraz rozszerzony artefakt Bineta z kryteriami domkniecia | T04-BLOCKER-001-WYPROWADZENIE-YUKAWA-BINET.md |
| 1.2 Uzasadnienie F(e) | DONE | Uzasadnienie F(e) domkniete przez podejscie mieszane: formalne + claim->source + ODE/Binet | Raport-Wyprowadzen-LTR.md, T04-NUM-VAL-001.md |
| 1.3 Spojnosc definicji R | DONE | Ujednolicono R=|Delta_varphi_Y|/|Delta_varphi_1PN| w tekscie i walidacji CAS | Raport-Wyprowadzen-LTR.md, Wyniki-CAS-T04.md |
| 2.1 Rozszerzenie CAS | DONE | Wykonane testy graniczne + niezalezna walidacja ODE/Binet z jawnym opisem ograniczen numerycznych | Wyniki-CAS-T04.md, T04-NUM-VAL-001.md |
| 2.2 Zakresy beta i lambda | DONE | Uzupelniono zakresy o zrodla i DOI (Sun et al. 2019, Kapner et al. 2007) | Plan-Danych.md |
| 2.3 Analiza czulosci | DONE | Wykresy analizy czulosci wygenerowane i osadzone w publikacji z podpisami merytorycznymi | Publikacja-Merytoryczna-T04.md, Wykresy-Indeks-T04.md |
| 3.1 Porownanie z obserwacjami | DONE | Przekazano benchmark 42.98 arcsec/century, test zgodnosci skali i praktyczne kryterium ograniczen | Raport-Wynikowy.md, Plan-Danych.md |
| 3.2 Constraints fifth force | DONE | Dodano sekcje porownawcza SS/LLR/lab i mapowanie claim->source | Publikacja-Merytoryczna-T04.md, Cross-Reference-Log-LTR.md |
| 3.3 Wykresy | DONE | Komplet wykresow merytorycznych osadzony w publikacji i dostepny jako artefakty PNG | Publikacja-Merytoryczna-T04.md, Wykresy-Indeks-T04.md |
| 4.1 Rozdzielenie proces vs fizyka | DONE | Rozdzielono manuskrypt merytoryczny od suplementu procesowego | Publikacja-Merytoryczna-T04-Manuskrypt.md, Publikacja-Merytoryczna-T04-Suplement-Procesowy.md |
| 4.2 Rozbudowa matematyki | DONE | Rozszerzono opis formalny i artefakt Bineta dla pelnej sciezki recenzenckiej | Raport-Wyprowadzen-LTR.md, T04-BLOCKER-001-WYPROWADZENIE-YUKAWA-BINET.md |
| 4.3 Rozszerzenie bibliografii | DONE | Dodano kluczowe DOI i claim->source, wraz z sekcja constraints | Plan-Danych.md, Cross-Reference-Log-LTR.md |

## Co oznacza "komplet danych" w tej rundzie
- Pakiet zawiera komplet danych liczbowych i artefaktow potrzebnych do ponownej recenzji obecnej wersji modelu (parametry, CI, wyniki CAS, indeks wykresow, mapowanie uwag).
- Pakiet merytoryczny na poziomie Major Revision jest domkniety; pozostaja jedynie notatki doskonalenia metody numerycznej (bez statusu blocker).

## Pakiet artefaktow (Source of Truth)
- Badania/T04-GR-PPN-Yukawa-Perihelion/PLAN_POPRAWEK_RECENZENT.md
- Badania/T04-GR-PPN-Yukawa-Perihelion/MACIERZ_WDROZENIA_UWAG_RECENZENTA.md
- Badania/T04-GR-PPN-Yukawa-Perihelion/Odpowiedz-Recenzent-Traceability-T04.md
- Badania/T04-GR-PPN-Yukawa-Perihelion/Publikacja-Merytoryczna-T04-Manuskrypt.md
- Badania/T04-GR-PPN-Yukawa-Perihelion/Publikacja-Merytoryczna-T04-Suplement-Procesowy.md
- Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Wyprowadzen-LTR.md
- Badania/T04-GR-PPN-Yukawa-Perihelion/T04-BLOCKER-001-WYPROWADZENIE-YUKAWA-BINET.md
- Badania/T04-GR-PPN-Yukawa-Perihelion/Wyniki-CAS-T04.md
- Badania/T04-GR-PPN-Yukawa-Perihelion/T04-NUM-VAL-001.md
- Badania/T04-GR-PPN-Yukawa-Perihelion/T04-NUM-VAL-DATA.csv
- Badania/T04-GR-PPN-Yukawa-Perihelion/Plan-Danych.md
- Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Wynikowy.md
- Badania/T04-GR-PPN-Yukawa-Perihelion/Wykresy-Indeks-T04.md

## Prosba do recenzenta
Prosimy o ponowna ocene wersji po uzupelnieniu pakietu danych i dokumentacji,
z naciskiem na merytoryczna adekwatnosc domknietych punktow 1.1-4.3.

## Status raportowania
- status: OK
- pewnosc: 0.90
- uzasadnienie: komplet danych i artefaktow traceability jest dostepny, a punkty 1.1-4.3 zostaly domkniete na poziomie recenzenckim.
