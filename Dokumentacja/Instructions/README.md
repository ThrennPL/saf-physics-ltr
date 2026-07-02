# SAF/LTR Instructions Foundation

Data: 2026-07-02
Status: active
Pewnosc: 0.95

Cel:
- Centralne source-of-truth dla polityk przekrojowych, aby ograniczyc duplikacje w profilach agentow.

Zakres pakietu G1:
1. quality-gates.instructions.md
2. reporting.instructions.md
3. tool-contracts.instructions.md
4. notation.instructions.md
5. literature.instructions.md

## Reguly wersjonowania

1. Kazdy plik instructions ma metadane: owner, wersja, data zmiany.
2. Zmiana semantyki gate/status/fail-closed wymaga wpisu w changelog projektu i review HITL.
3. Agent profile powinny referowac instrukcje zamiast kopiowac polityki runtime.

## Ownerzy obszarow

| Obszar | Owner |
|---|---|
| Quality gates i fail-closed | Orkiestrator |
| Reporting i Q-XXX | Artifact Quality |
| Tool contracts | Technical Developer |
| Notation i EQ/ID | Formal Consistency |
| Literature policy | Cross-Reference |

## Zasada operacyjna

- W razie konfliktu miedzy profilem agenta a instrukcja przekrojowa, instrukcja przekrojowa ma priorytet.
