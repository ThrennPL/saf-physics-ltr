# tool-contracts.instructions.md

Data: 2026-07-02
Status: active
Wersja: 1.0.0
Owner: Technical Developer

## Cel

Ujednolicic kontrakty I/O narzedzi i klasy bledow niezaleznie od roli agenta.

## Zasady ogolne kontraktow

1. Kazde narzedzie deklaruje: input contract, output contract, error contract.
2. Wynik narzedzia musi byc mapowalny do statusu OK/Warning/Blocker.
3. Narzedzie nie podejmuje decyzji gate; zwraca tylko wynik i diagnostyke.

## Minimalny output contract

1. status
2. summary
3. diagnostics (lista)
4. metadata (czas, wersja, parametry)

## Minimalny error contract

1. code
2. reason
3. recoverable (true/false)
4. escalation_required (true/false)

## Regula zgodnosci

1. Skill korzysta z kontraktu narzedzia, nie z implementacji wewnetrznej.
2. Zmiana kontraktu wymaga aktualizacji compatibility matrix.
