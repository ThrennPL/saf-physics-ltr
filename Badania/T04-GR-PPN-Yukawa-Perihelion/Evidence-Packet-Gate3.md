# Evidence Packet (minimalny)

- Decyzja: pass-with-comments
- Owner (human-in-the-loop): HUMAN_OWNER
- Gate ID: G3
- Case ID: T04-GR-PPN-Yukawa-Perihelion
- Data budowy: 2026-06-20 23:31:54 UTC

## Artefakty i statusy
| Artefakt | Status | Exists | Notatka |
|---|---|---|---|
| Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Wyprowadzen-LTR.md | OK | yes | Model i rownania EQ |
| Badania/T04-GR-PPN-Yukawa-Perihelion/Rejestr-Walidacji-Formalnej-LTR.md | OK | yes | Walidacja formalna i [VERIFY-CAS] domkniete |
| Badania/T04-GR-PPN-Yukawa-Perihelion/Plan-Danych.md | Warning | yes | CI i propagacja niepewnosci |
| Badania/T04-GR-PPN-Yukawa-Perihelion/Risk-and-Safety-Pack-Teoretyczna.md | Warning | yes | RISK-PREPRINT-YUKAWA zaakceptowane warunkowo |
| Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Wynikowy.md | OK | yes | Konsolidacja Gate 3 |
| Badania/T04-GR-PPN-Yukawa-Perihelion/Walidacja-Jezykowa-PL.md | Warning | yes | Walidacja jezykowa PL |

## Manifest OKF-lite
- Schema: okf-lite/v1
- Tryb: selektywny transfer metadanych (bez utraty merytoryki).
  
| Artifact ID | Type | Path | Required For | Status | Exists | Note |
|---|---|---|---|---|---|---|
| ART-RAPORT-WYPROWADZEN-LTR | Raport-Wyprowadzen-LTR | Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Wyprowadzen-LTR.md | G3 | OK | yes | Model i rownania EQ |
| ART-REJESTR-WALIDACJI-FORMALNEJ-LTR | Rejestr-Walidacji-Formalnej-LTR | Badania/T04-GR-PPN-Yukawa-Perihelion/Rejestr-Walidacji-Formalnej-LTR.md | G3 | OK | yes | Walidacja formalna i [VERIFY-CAS] domkniete |
| ART-PLAN-DANYCH | Plan-Danych | Badania/T04-GR-PPN-Yukawa-Perihelion/Plan-Danych.md | G3 | Warning | yes | CI i propagacja niepewnosci |
| ART-RISK-AND-SAFETY-PACK-TEORETYCZNA | Risk-and-Safety-Pack-Teoretyczna | Badania/T04-GR-PPN-Yukawa-Perihelion/Risk-and-Safety-Pack-Teoretyczna.md | G3 | Warning | yes | RISK-PREPRINT-YUKAWA zaakceptowane warunkowo |
| ART-RAPORT-WYNIKOWY | Raport-Wynikowy | Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Wynikowy.md | G3 | OK | yes | Konsolidacja Gate 3 |
| ART-WALIDACJA-JEZYKOWA-PL | Walidacja-Jezykowa-PL | Badania/T04-GR-PPN-Yukawa-Perihelion/Walidacja-Jezykowa-PL.md | G3 | Warning | yes | Walidacja jezykowa PL |

## Zero-loss guard (merytoryka)
- Generator nie przenosi ani nie kompresuje tresci merytorycznej dokumentow case.
- Evidence packet ma role indeksu i statusow; tresc naukowa pozostaje w artefaktach zrodlowych.
- Brak krytycznych artefaktow powinien byc traktowany fail_closed (Blocker + eskalacja).

## Notatki
- Statusy: OK / Warning / Blocker / Missing.
- Plik jest generowany przez tools/build_evidence_packet.py.
