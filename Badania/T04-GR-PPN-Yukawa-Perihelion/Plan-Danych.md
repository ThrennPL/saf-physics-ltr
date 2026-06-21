# Plan danych

## Metadane
- ID: T04-DATA-001
- Tytul: GR-PPN-Yukawa-Perihelion
- Status: draft
- Powiazania (format [ID:Typ]): [T04-MEAS-INT-001:Measurement-Integrity-Pack]

## Zakres danych
- Parametry orbitalne referencyjne (a, e).
- Stale fizyczne (G, c, M dla ukladu testowego).
- Ewentualny punkt odniesienia obserwacyjnego dla precesji.
- Raportowanie wynikow w obu miarach: na orbitę i na stulecie.

## Zrodla
- NIST CODATA 2022 (stale fundamentalne):
	- c: https://physics.nist.gov/cgi-bin/cuu/Value?c
	- G: https://physics.nist.gov/cgi-bin/cuu/Value?bg
- NASA NSSDC Fact Sheet (archiwum):
	- NASA Mercury Fact Sheet (arch.): https://web.archive.org/web/20190403160651/https://nssdc.gsfc.nasa.gov/planetary/factsheet/mercuryfact.html
	- NASA Sun Fact Sheet (arch.): https://web.archive.org/web/20190403160431/https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html
- Literatura testow precesji:
	- Park et al. (2017), AJ, DOI: 10.3847/1538-3881/aa5be2
	- Will (2014), LRR, DOI: 10.12942/lrr-2014-4
	- Sun, Cao, Shao (2019), PRD, DOI: 10.1103/PhysRevD.100.084030
	- Kapner et al. (2007), PRL, DOI: 10.1103/PhysRevLett.98.021101

## Tabela parametrow referencyjnych (iteracja 2)
| Parametr | Wartosc robocza | Jednostka | Zrodlo | Data dostepu |
|---|---|---|---|---|
| c | 299792458 | m/s | NIST CODATA | 2026-06-21 |
| G | 6.67430e-11 | m^3 kg^-1 s^-2 | NIST CODATA | 2026-06-21 |
| M_sun | 1.9885e30 | kg | NASA Sun Fact Sheet (arch.) | 2026-06-21 |
| a_Mercury | 57.91e6 | km | NASA Mercury Fact Sheet (arch.) | 2026-06-21 |
| e_Mercury | 0.2056 | 1 | NASA Mercury Fact Sheet (arch.) | 2026-06-21 |
| P_orb_Mercury | 87.969 | days | NASA Mercury Fact Sheet (arch.) | 2026-06-21 |
| beta | [-1e-10, 1e-10] | 1 | Sun, Cao, Shao (2019), PRD, DOI: 10.1103/PhysRevD.100.084030 | 2026-06-21 |
| lambda | [1e10, 1e12] | m | Kapner et al. (2007), PRL, DOI: 10.1103/PhysRevLett.98.021101 | 2026-06-21 |

## Uwagi jakosci danych
- Wartosci powyzej sa zgodne z pierwszym sanity-check CAS (Wyniki-CAS-T04.md).
- Jesli potrzebna jest wersja efemerydowa high-precision (np. epoch-specific), wymagane jest dopiecie zrodla JPL Horizons.

## Zalozenia propagacji niepewnosci (Gate 3, iteracja 3)
| Parametr | Zakres/niepewnosc robocza | Uwaga |
|---|---|---|
| a | +/- 1e-4 rel. wokol a_Mercury | zakres roboczy do testu odpornosci |
| e | +/- 5e-4 abs wokol e_Mercury | zakres roboczy do testu odpornosci |
| beta | [-1e-10, 1e-10] | benchmark teorii piatej sily |
| lambda | [1e10, 1e12] m (log-uniform) | zakres dlugozasiegowy Yukawa |

## Tabela CI (Monte Carlo, N=120000)
Miara: arcsec/century.

| Wielkosc | srednia | p2.5 | p50 | p97.5 | min | max |
|---|---|---|---|---|---|---|
| delta_phi_total | 42.981438 | 42.966851 | 42.981464 | 42.995860 | 42.953806 | 43.008241 |
| delta_phi_1PN | 42.981448 | 42.970786 | 42.981445 | 42.992145 | 42.967933 | 42.994933 |
| delta_phi_Y | -0.000010 | -0.010866 | -0.000003 | 0.010882 | -0.015188 | 0.015202 |

Wniosek roboczy: dla zadanych zakresow dominuje skladnik 1PN, a skladnik modelu Yukawy miesci sie w waskim pasmie wokol zera.

## Decyzja raportowania miar (Q-302)
- Status: zamkniete

- Ustalenie: raportujemy obie miary rownolegle:
	- na orbitę,
	- na stulecie (arcsec/century).
- Uzasadnienie: zwieksza to porownywalnosc z literatura i czytelnosc wynikow bez utraty tresci merytorycznej.

## Zasady jakosci
- Kazda wartosc ma zrodlo i date dostepu.
- Brak zrodla dla parametru krytycznego => Blocker.

## Status
- status: Warning
- pewnosc: 0.74
