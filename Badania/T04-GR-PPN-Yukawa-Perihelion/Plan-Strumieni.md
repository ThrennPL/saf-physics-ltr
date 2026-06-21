# Plan strumieni

## Metadane
- ID: T04-STREAMS-001
- Tytul: GR-PPN-Yukawa-Perihelion
- Status: draft

## Strumienie prac
1. discovery: zakres literatury i benchmark precesji.
2. model: wyprowadzenia 1PN + Yukawa i granice stosowalnosci.
3. walidacja: CAS, niepewnosci, checki formalne.
4. raport: konsolidacja artefaktow i decyzji gate.

## Delegacje (wklad agentow)
kto: physics-discovery
dlaczego: wyszukanie i porownanie zrodel o precesji 1PN i ograniczeniach Yukawy.
ETA: 2026-06-24 12:00
wejscia: Karta-Badania, zakres parametrow.
wyjscia: Cross-Reference-Log-LTR z min. 8 zrodlami.
priorytet: wysoki

kto: cross-reference
dlaczego: mapowanie twierdzen do literatury i identyfikacja luk.
ETA: 2026-06-24 13:00
wejscia: Cross-Reference-Log-LTR, lista twierdzen EQ.
wyjscia: tabela claim->source z confidence.
priorytet: wysoki

kto: model-review
dlaczego: kontrola fizycznej poprawnosci wzorow i przyblizen.
ETA: 2026-06-24 14:00
wejscia: Raport-Wyprowadzen-LTR.
wyjscia: status OK/Warning/Blocker + lista poprawek.
priorytet: wysoki

kto: formal-consistency
dlaczego: kontrola notacji, ID i tagow EQ:T04-*.
ETA: 2026-06-24 15:00
wejscia: Raport-Wyprowadzen-LTR, Mapa-Notacji-LTR.
wyjscia: raport niespojnosci notacyjnych.
priorytet: wysoki

kto: data-quality
dlaczego: ocena jakosci danych referencyjnych (parametry orbitalne, stale).
ETA: 2026-06-24 16:00
wejscia: Plan-Danych, zrodla parametrow.
wyjscia: status jakosci danych + braki.
priorytet: sredni

kto: statistics-review
dlaczego: ocena niepewnosci i propagacji bledow dla delta_phi_total.
ETA: 2026-06-24 17:00
wejscia: Measurement-Integrity-Pack, tabela parametrow.
wyjscia: tabela niepewnosci i CI.
priorytet: sredni

kto: simulation-experiment
dlaczego: test parametryczny i mapa wrazliwosci (beta, lambda, e, a).
ETA: 2026-06-24 18:00
wejscia: model rownan, zakres parametrow.
wyjscia: tabela scenariuszy i granic dominacji.
priorytet: sredni

kto: risk-compliance
dlaczego: identyfikacja ryzyka nadinterpretacji i warunkow stop.
ETA: 2026-06-24 19:00
wejscia: wyniki walidacji i benchmarki.
wyjscia: Risk-and-Safety-Pack z progami eskalacji.
priorytet: sredni

kto: knowledge-repo
dlaczego: normalizacja slownika i klasyfikacja artefaktow.
ETA: 2026-06-24 20:00
wejscia: zestaw artefaktow roboczych.
wyjscia: zgodnosc taxonomii i mapa artefaktow.
priorytet: niski

kto: language-polish-quality
dlaczego: walidacja jezykowa PL przed gate i PDF.
ETA: 2026-06-24 21:00
wejscia: Raport-Wynikowy, Podsumowanie-Gate.
wyjscia: status OK/Warning/Blocker + lista korekt redakcyjnych.
priorytet: sredni

kto: artifact-quality
dlaczego: konsolidacja statusow i gotowosci gate.
ETA: 2026-06-24 22:00
wejscia: wszystkie raporty agentow.
wyjscia: rekomendacja gate + lista brakow.
priorytet: wysoki

kto: technical-developer
dlaczego: automatyzacja walidacji rownan i budowy evidence pack.
ETA: 2026-06-24 23:00
wejscia: wymagania walidacyjne i runbook.
wyjscia: patch narzedzi + wynik testow lint/test/typecheck.
priorytet: sredni

## Delegacja uzupelniajaca (procesowa, dla kolejnych prac)
kto: technical-developer
dlaczego: uzupelnienie procesu publikacyjnego tak, aby kolejne prace automatycznie wykrywaly braki procesowe z recenzji (bez narzucania merytoryki badan).
ETA: 2026-06-25 18:00
wejscia: PLAN_POPRAWEK_RECENZENT.md, MACIERZ_WDROZENIA_UWAG_RECENZENTA.md, Zadania-Technical-Developer-Proces.md
wyjscia: wdrozenie pakietu TD-P1..TD-P7 (linter kompletnosci, checker spojnosci definicji, harness CAS, walidator provenance, pipeline wykresow, split manuskrypt/suplement, generator odpowiedzi do recenzji)
priorytet: wysoki
