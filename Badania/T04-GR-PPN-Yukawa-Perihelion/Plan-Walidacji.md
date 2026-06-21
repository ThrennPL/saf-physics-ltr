# Plan walidacji

## Metadane
- ID: T04-VAL-PLAN-001
- Tytul: GR-PPN-Yukawa-Perihelion
- Status: draft
- Powiazania: [T04-CASE-001:Karta-Badania]

## Rownania testowe
1. Skladnik 1PN (dla porownania):
$$
\Delta\varphi_{1PN} = \frac{6\pi GM}{a(1-e^2)c^2}
$$
EQ:T04-1

2. Potencjal Yukawy:
$$
V_Y(r) = -\frac{GMm}{r}\,\beta e^{-r/\lambda}
$$
EQ:T04-2

3. Przyblizona poprawka precesji od Yukawy (rezim perturbacyjny, model roboczy):
$$
\Delta\varphi_{Y} \approx \pi\,\beta\left(\frac{a}{\lambda}\right)^2 e^{-a/\lambda}\,F(e)
$$
EQ:T04-3

4. Suma:
$$
\Delta\varphi_{total} = \Delta\varphi_{1PN} + \Delta\varphi_{Y}
$$
EQ:T04-4

## Testy formalne i numeryczne
- T1: Kontrola wymiarowa EQ:T04-1..EQ:T04-4.
- T2: Granica beta -> 0 daje czysty 1PN.
- T3: Granica lambda -> inf daje zanik sensownego wkladu Yukawy w modelu roboczym.
- T4: [VERIFY-CAS] Niezalezna kontrola pochodnych i rozwiniec asymptotycznych.
- T5: Test wrazliwosci na (a, e, beta, lambda) z tabela niepewnosci.

## Kryteria pass/fail
- pass: wszystkie T1..T5 sa zaliczone, brak sprzecznosci formalnych.
- warning: czesc testow wrazliwosci niejednoznaczna, ale bez krytycznych konfliktow.
- fail: niespojnosc formalna, brak [VERIFY-CAS], albo brak mozliwosci odtworzenia obliczen.

## Wynik raportowania
- status: OK/Warning/Blocker
- confidence: 0-1
- pytania: Q-XXX z priorytetem niski/sredni/wysoki
