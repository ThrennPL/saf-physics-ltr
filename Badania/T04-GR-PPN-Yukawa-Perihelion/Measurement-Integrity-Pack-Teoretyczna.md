# Measurement Integrity Pack (fizyka teoretyczna)

## Metadane
- ID: T04-MEAS-INT-001
- Tytul: GR-PPN-Yukawa-Perihelion
- Autor: Zespol SAF
- Data: 2026-06-21
- Status: draft
- Powiazania (format [ID:Typ]): [T04-CASE-001:Karta-Badania], [T04-VAL-PLAN-001:Plan-Walidacji]

## Parametry i zakresy robocze
- a: polos wielka orbity (wartosci referencyjne do uzupelnienia)
- e: mimoesrod orbity
- beta: amplituda Yukawy (|beta| << 1)
- lambda: zasieg Yukawy
- Szczegoly referencyjne: patrz Plan-Danych.md (iteracja 2).

## Kontrole integralnosci
- Jawne zrodla parametrow dla kazdej stalej i zmiennej.
- Sprawdzenie jednostek i konwersji.
- Rozdzielenie wartosci nominalnych i zakresow niepewnosci.

## Testy sanity
- Odzyskanie 1PN dla beta -> 0.
- Stabilnosc znaku i rzedu wielkosci dla lambda/a.

## Status roboczy
- status: Warning
- pewnosc: 0.61
- uwaga: tabela parametrow referencyjnych uzupelniona; brak finalnej tabeli CI i propagacji bledow.
