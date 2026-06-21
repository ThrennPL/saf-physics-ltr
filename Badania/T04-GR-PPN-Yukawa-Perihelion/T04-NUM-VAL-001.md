# T04 NUM VAL 001 - Walidacja numeryczna rownania Bineta

## Metadane
- ID: T04-NUM-VAL-001
- Case: T04-GR-PPN-Yukawa-Perihelion
- Data: 2026-06-21
- Metoda: integracja RK4 rownania Bineta + detekcja kolejnego peryhelium
- Artefakt danych: T04-NUM-VAL-DATA.csv

## Konfiguracja
- Mu = G*M_sun z Plan-Danych.
- h^2 = Mu*a*(1-e^2) (przyblizenie keplerowskie do warunkow poczatkowych).
- Warunek poczatkowy: u(0)=1/(a(1-e)), u'(0)=0.
- Precesja numeryczna: Delta_phi_num = phi_peak - 2*pi.
- Precesja analityczna: Eq:T04-B13 z F(e)=1/(1-e^2).

## Wynik zbiorczy
- epsilon_median = 0.451233
- epsilon_max = 1.000000
- calibration: epsilon_median = 0.086543, epsilon_max = 0.756104
- physical: epsilon_median = 1.000000, epsilon_max = 1.000000
- Kryterium minimalne (epsilon < 5%): PARTIAL
- Interpretacja: dla fizycznie malych beta sygnal Yukawy jest ponizej rozdzielczosci aktualnej konfiguracji RK4; porownanie ilosciowe jest wiarygodne glownie w rezimie kalibracyjnym (wieksze beta).

## Wnioski
1. Niezalezna walidacja ODE zostala wykonana i zmaterializowana jako artefakty liczbowe + wykresowe.
2. Model analityczny jest kierunkowo zgodny z integracja numeryczna w scenariuszach kalibracyjnych.
3. Przed finalna publikacja zalecane jest przejscie na solver wyzszego rzedu/adaptacyjny i estymacje fazy peryhelium metoda sub-step dla scenariuszy fizycznych.

## Artefakty wykresowe
- wykresy/t04-binet-num-vs-analytic.png
- wykresy/t04-binet-error-vs-lambda.png
- wykresy/t04-binet-error-vs-e.png
- wykresy/t04-binet-error-map-beta-lambda.png
