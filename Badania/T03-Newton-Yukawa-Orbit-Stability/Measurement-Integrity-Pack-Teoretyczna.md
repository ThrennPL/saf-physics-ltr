# Measurement Integrity Pack (fizyka teoretyczna)

## Metadane
- ID: T03-MEAS-INT-001
- Tytuł: Newton-Yukawa-Orbit-Stability
- Autor: Zespół SAF
- Data: 2026-05-30
- Status: draft
- Powiązania (format [ID:Typ]): [T03-CASE-001:Karta-Badania], [T03-EXP-CTX-001:Experiment-Context-Pack]

## Dane wejściowe i parametry
- Źródła: założenia modelu teoretycznego.
- Parametry: mu > 0, beta (bezwymiarowe), lambda > 0.
- Warunki brzegowe: orbita kołowa r = r_c i małe odchylenia radialne.
- Plan danych/retencja: N/A (brak danych empirycznych).

## Sprawność obliczeń
- Stabilność numeryczna: nie dotyczy (wyprowadzenie analityczne).
- Zbieżność: nie dotyczy.
- Sanity-check: analiza wymiarowa i limity beta -> 0 oraz lambda -> inf.

## Walidacja wewnętrzna
- Benchmark 1: Odtwórzenie Newtona dla beta = 0.
- Benchmark 2: zachowanie dla lambda -> inf, gdzie exp(-r/lambda) -> 1.
- Benchmark 3: zgodność znaku wkładki Yukawy w V_eff''.

## Niepewność i wrażliwość
- Dominująca niepewność: wybór reżimu perturbacyjnego.
- Wrażliwość: znak i moduł czynnika (1 + x - x^2), x = r_c/lambda.
- status: Warning
- pewność: 0.77




