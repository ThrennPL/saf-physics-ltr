# Checklista wkladu agentow (test praktyczny)

## Metadane
- ID: T04-AGENT-CHECK-001
- Tytul: Wkład agentow vs kompetencje
- Status: closed
- Powiazania: [T04-STREAMS-001:Plan-Strumieni]

## Cel
Sprawdzic, czy kazdy agent dostarczyl merytoryczny wkład zgodny z zakresem kompetencji
oraz czy artefakty sa audytowalne i bez utraty treści.

## Kryteria per agent
| Agent | Oczekiwany artefakt | Kryterium akceptacji | Status |
|---|---|---|---|
| physics-discovery | Cross-Reference-Log-LTR | min 8 zrodel, rozroznienie preprint/peer-reviewed | PARTIAL (pilot: 3 zrodla kluczowe; pelny zakres przeniesiony do backlogu) |
| cross-reference | mapa claim->source | kazdy claim kluczowy ma zrodlo i confidence | PARTIAL (CL-001/003 verified, CL-002 verified_with_risk) |
| model-review | review merytoryczny | brak krytycznych bledow fizycznych lub jawny Blocker | PARTIAL (kanoniczne F(e) przyjete roboczo) |
| formal-consistency | raport notacji/ID/EQ | 0 konfliktow krytycznych ID i EQ | PARTIAL (EQ:T04-1..5 spisane; audyt pelny poza zakresem pilota) |
| data-quality | ocena danych referencyjnych | jawne pochodzenie parametrow i status jakosci | PARTIAL (Plan-Danych iteracja 2) |
| statistics-review | tabela niepewnosci | propagacja bledow i CI dla delta_phi_total | DONE (Monte Carlo N=120000, Plan-Danych) |
| simulation-experiment | tabela scenariuszy | mapa wrazliwosci i granice dominacji | N/A (pilot-scope; patrz Rejestr-NA-Agentow.md) |
| risk-compliance | rejestr ryzyk | progi eskalacji i plan mitygacji | DONE (T04-RISK-SAF-001 z ryzykiem rezydualnym) |
| knowledge-repo | normalizacja taxonomii | brak driftu slownika krytycznego | N/A (pilot-scope; patrz Rejestr-NA-Agentow.md) |
| language-polish-quality | walidacja jezykowa | status PL przed finalnym gate | DONE (T04-LANG-PL-001: Warning, 0.87) |
| artifact-quality | konsolidacja gate | status zbiorczy OK/Warning/Blocker + luki | DONE (Evidence-Packet-Gate3.md pass-with-comments + Evidence-Packet-Gate4.md pass) |
| technical-developer | wsparcie narzedziowe | testy przechodza, automatyzacja dziala | DONE (cas_check_t04.py + Wyniki-CAS-T04.md) |

## Decyzja zakresu (Q-401/Q-402)
- Q-401: potwierdzono klasyfikacje "zamkniete z czesciowym zakresem agentow (pilot)".
- Q-402: potwierdzono osobny rejestr "N/A w tej iteracji".
- Referencja: Rejestr-NA-Agentow.md.

## Wymuszenie zero-loss
- Kazdy wpis musi wskazac Source of Truth (plik).
- Niedopuszczalne jest zastapienie treści merytorycznej samym streszczeniem.
- Brak odniesienia do zrodla => Blocker.

## Wynik koncowy testu
- status: OK/Warning/Blocker
- confidence: 0-1
- decyzja: kontynuowac / poprawic / stop

## Postep iteracji 1
- status: Warning
- confidence: 0.58
- wykonano: szkielet artefaktow T04 + pierwsza walidacja [VERIFY-CAS].
- blocker: brak uzupelnionych zrodel w Cross-Reference-Log-LTR i brak finalnej postaci F(e).

## Postep iteracji 2
- status: Warning
- confidence: 0.66
- wykonano: uzupelnienie zrodel DOI/NASA/NIST, domkniecie CL-001, aktualizacja Plan-Danych.
- blocker: CL-002/CL-003 pozostaja partial oraz brak finalnej decyzji o F(e) i propagacji niepewnosci.

## Postep iteracji 3
- status: Warning
- confidence: 0.75
- wykonano: decyzja model-review o F(e), tabela CI i propagacja niepewnosci, aktualizacja Gate3 checklist.
- blocker: jawna etykieta RISK-PREPRINT-YUKAWA pozostaje do decyzji czlowieka o akceptacji lub dodatkowej weryfikacji.

## Postep iteracji 4
- status: Warning
- confidence: 0.80
- wykonano: walidacja jezykowa PL i korekty redakcyjne pakietu T04.
- blocker: finalna decyzja human-in-the-loop dla Gate 3/4.

## Postep iteracji 5
- status: Warning
- confidence: 0.83
- wykonano: konsolidacja artifact-quality i risk-compliance, wygenerowany strict Evidence-Packet-Gate3.
- blocker: decyzja human-in-the-loop pozostaje wymagana (Gate 1/2/4 oraz finalna akceptacja notatek Gate 3).

## Postep iteracji 6
- status: OK
- confidence: 0.90
- wykonano: decyzja human-in-the-loop potwierdzona, Gate 4 zamkniety, Q-302 zamkniete (raportowanie obu miar).
- blocker: brak.

## Postep iteracji 7
- status: OK
- confidence: 0.92
- wykonano: wygenerowano finalny Evidence-Packet-Gate4.md (decision=pass, owner=HUMAN_OWNER) w trybie strict-metadata.
- blocker: brak.

## Postep iteracji 8
- status: OK
- confidence: 0.93
- wykonano: uzgodniono i zapisano zamkniecie case T04 jako pilot z czesciowym zakresem agentow oraz wydzielono pozycje N/A do rejestru.
- blocker: brak.

## Pytania otwarte
- Q-101 (wysoki): Czy dla T04 wchodzimy w dane obserwacyjne, czy zostajemy przy benchmarku teoretycznym?
- Q-102 (sredni): Czy akceptujemy model roboczy EQ:T04-3, czy wymagamy pelnego wyprowadzenia z rownania Bineta?
