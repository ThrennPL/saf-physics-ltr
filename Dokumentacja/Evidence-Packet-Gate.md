# Evidence Packet (minimalny)

- Decyzja: pending
- Owner (human-in-the-loop): HUMAN_OWNER
- Gate ID: G3
- Case ID: -
- Data budowy: 2026-06-20 22:58:02 UTC

## Artefakty i statusy
| Artefakt | Status | Exists | Notatka |
|---|---|---|---|
| Dokumentacja/Konsolidacja-Statusow.md | Warning | yes | Wstepna konsolidacja |
| Dokumentacja/Rejestr-Konfliktow-i-Eskalacji.md | Warning | yes | Wstepny rejestr |
| Dokumentacja/Podsumowanie-Gate.md | Warning | yes | Decyzja finalna przed owner review |

## Manifest OKF-lite
- Schema: okf-lite/v1
- Tryb: selektywny transfer metadanych (bez utraty merytoryki).
| Artifact ID | Type | Path | Required For | Status | Exists | Note |
|---|---|---|---|---|---|---|
| ART-KONSOLIDACJA-STATUSOW | Konsolidacja-Statusow | Dokumentacja/Konsolidacja-Statusow.md | G3 | Warning | yes | Wstepna konsolidacja |
| ART-REJESTR-KONFLIKTOW-I-ESKALACJI | Rejestr-Konfliktow-i-Eskalacji | Dokumentacja/Rejestr-Konfliktow-i-Eskalacji.md | G3 | Warning | yes | Wstepny rejestr |
| ART-PODSUMOWANIE-GATE | Podsumowanie-Gate | Dokumentacja/Podsumowanie-Gate.md | G3 | Warning | yes | Decyzja finalna przed owner review |

## Zero-loss guard (merytoryka)
- Generator nie przenosi ani nie kompresuje tresci merytorycznej dokumentow case.
- Evidence packet ma role indeksu i statusow; tresc naukowa pozostaje w artefaktach zrodlowych.
- Brak krytycznych artefaktow powinien byc traktowany fail_closed (Blocker + eskalacja).

## Notatki
- Statusy: OK / Warning / Blocker / Missing.
- Plik jest generowany przez tools/build_evidence_packet.py.
