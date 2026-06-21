# Evidence Packet (minimalny)

- Decyzja: pass
- Owner (human-in-the-loop): HUMAN_OWNER
- Gate ID: G4
- Case ID: T04-GR-PPN-Yukawa-Perihelion
- Data budowy: 2026-06-20 23:45:30 UTC

## Artefakty i statusy
| Artefakt | Status | Exists | Notatka |
|---|---|---|---|
| Badania/T04-GR-PPN-Yukawa-Perihelion/Checklista-Gate4-Auditability.md | OK | yes | Auditability domkniete po akceptacji HITL |
| Badania/T04-GR-PPN-Yukawa-Perihelion/Akceptacje-Decyzje.md | OK | yes | Finalna decyzja Gate 4 (T04-DEC-007) |
| Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Wynikowy.md | OK | yes | Status case: closed, Gate 4 approved |
| Badania/T04-GR-PPN-Yukawa-Perihelion/Orkiestrator-Log.md | OK | yes | Zamkniecie Gate 4 i Q-302 |
| Badania/T04-GR-PPN-Yukawa-Perihelion/Plan-Danych.md | OK | yes | Q-302 zamkniete: raportowanie obu miar |
| Badania/T04-GR-PPN-Yukawa-Perihelion/Walidacja-Jezykowa-PL.md | Warning | yes | Walidacja jezykowa PL pozostaje referencyjna |

## Manifest OKF-lite
- Schema: okf-lite/v1
- Tryb: selektywny transfer metadanych (bez utraty merytoryki).
| Artifact ID | Type | Path | Required For | Status | Exists | Note |
|---|---|---|---|---|---|---|
| ART-CHECKLISTA-GATE4-AUDITABILITY | Checklista-Gate4-Auditability | Badania/T04-GR-PPN-Yukawa-Perihelion/Checklista-Gate4-Auditability.md | G4 | OK | yes | Auditability domkniete po akceptacji HITL |
| ART-AKCEPTACJE-DECYZJE | Akceptacje-Decyzje | Badania/T04-GR-PPN-Yukawa-Perihelion/Akceptacje-Decyzje.md | G4 | OK | yes | Finalna decyzja Gate 4 (T04-DEC-007) |
| ART-RAPORT-WYNIKOWY | Raport-Wynikowy | Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Wynikowy.md | G4 | OK | yes | Status case: closed, Gate 4 approved |
| ART-ORKIESTRATOR-LOG | Orkiestrator-Log | Badania/T04-GR-PPN-Yukawa-Perihelion/Orkiestrator-Log.md | G4 | OK | yes | Zamkniecie Gate 4 i Q-302 |
| ART-PLAN-DANYCH | Plan-Danych | Badania/T04-GR-PPN-Yukawa-Perihelion/Plan-Danych.md | G4 | OK | yes | Q-302 zamkniete: raportowanie obu miar |
| ART-WALIDACJA-JEZYKOWA-PL | Walidacja-Jezykowa-PL | Badania/T04-GR-PPN-Yukawa-Perihelion/Walidacja-Jezykowa-PL.md | G4 | Warning | yes | Walidacja jezykowa PL pozostaje referencyjna |

## Zero-loss guard (merytoryka)
- Generator nie przenosi ani nie kompresuje tresci merytorycznej dokumentow case.
- Evidence packet ma role indeksu i statusow; tresc naukowa pozostaje w artefaktach zrodlowych.
- Brak krytycznych artefaktow powinien byc traktowany fail_closed (Blocker + eskalacja).

## Notatki
- Statusy: OK / Warning / Blocker / Missing.
- Plik jest generowany przez tools/build_evidence_packet.py.
