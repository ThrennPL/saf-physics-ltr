# reporting.instructions.md

Data: 2026-07-02
Status: active
Wersja: 1.0.0
Owner: Artifact Quality

## Cel

Ujednolicenie formatu raportow w calym workflow SAF/LTR.

## Minimalny standard raportowania

Kazdy raport decyzyjny lub kontrolny musi zawierac:
1. status: OK/Warning/Blocker
2. pewnosc: liczba 0-1
3. liste pytan Q-XXX z priorytetem niski/sredni/wysoki
4. owner i ETA dla elementow nie-OK

## Konwencje identyfikatorow

1. Powiazania artefaktow: [ID:Typ]
2. Tag rownania: EQ:ID (w osobnej linii)
3. Nietrywialny krok formalny: [VERIFY-CAS]

## Zasady redakcyjne

1. Fakt oddziel od interpretacji.
2. Nie dopelniaj brakujacych danych domyslem.
3. Braki oznacz jawnie jako "Nie wiem" i dodaj wymagany input.

## Tabele rekomendowane

1. Tabela statusow komponentow
2. Tabela pytan Q-XXX
3. Tabela ryzyk z ownerem i ETA
