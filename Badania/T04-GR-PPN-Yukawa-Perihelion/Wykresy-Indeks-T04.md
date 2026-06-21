# Indeks wykresow T04

- Status: draft (pipeline TD-P5)
- Cel: Source of Truth dla artefaktow wykresowych wymaganych przez recenzje.

## Wymagane pozycje
| ID | Tytul | Plik | Status pliku |
|---|---|---|---|
| T04-CH-001 | Precesja Yukawy vs lambda | wykresy/t04-precesja-vs-lambda.png | PRESENT (generated) |
| T04-CH-002 | Mapa konturowa (beta, lambda) | wykresy/t04-mapa-beta-lambda.png | PRESENT (generated) |
| T04-CH-003 | Porownanie skladnikow precesji | wykresy/t04-porownanie-skladnikow.png | PRESENT (generated) |

## Dodatkowe pozycje walidacji ODE/Binet
| ID | Tytul | Plik | Status pliku |
|---|---|---|---|
| T04-CH-004 | Numeryczna vs analityczna precesja Yukawy | wykresy/t04-binet-num-vs-analytic.png | PRESENT (generated) |
| T04-CH-005 | Blad wzgledny vs lambda | wykresy/t04-binet-error-vs-lambda.png | PRESENT (generated) |
| T04-CH-006 | Blad wzgledny vs e | wykresy/t04-binet-error-vs-e.png | PRESENT (generated) |
| T04-CH-007 | Mapa bledu epsilon(beta, lambda) | wykresy/t04-binet-error-map-beta-lambda.png | PRESENT (generated) |

## Uwagi
- Brakujace pliki sa sygnalizowane przez checker `tools/chart_artifact_pipeline_check.py` jako Blocker.
- Aktualne pliki wykresowe zostaly wygenerowane automatycznie skryptem `tools/generate_t04_charts.py`.
