# Cross-Reference Log LTR

## Metadane
- ID: T04-LTR-XREF-001
- Tytul: GR-PPN-Yukawa-Perihelion
- Autor: Zespol SAF
- Data: 2026-06-21
- Status: draft

## Tabela claim -> source
| Claim ID | Twierdzenie | Zrodlo | Typ zrodla | Pewnosc | Status |
|---|---|---|---|---|---|
| T04-CL-001 | Postac precesji 1PN jak w EQ:T04-1 | Will (2014), Living Rev. Relativity, DOI: 10.12942/lrr-2014-4; Park et al. (2017), AJ, DOI: 10.3847/1538-3881/aa5be2 | peer-reviewed | 0.88 | verified |
| T04-CL-002 | Uzyte przyblizenie Yukawy dla precesji | Sun, Cao, Shao (2019), Phys. Rev. D 100, 084030, DOI: 10.1103/PhysRevD.100.084030; arXiv:1910.05666 | peer-reviewed + preprint (RISK-PREPRINT-YUKAWA) | 0.78 | verified_with_risk |
| T04-CL-003 | Zakres poprawnosci perturbacyjnej | Kapner et al. (2007), PRL 98, 021101, DOI: 10.1103/PhysRevLett.98.021101; Will (2014), DOI: 10.12942/lrr-2014-4 | peer-reviewed | 0.69 | verified |
| T04-CL-004 | Constraints Yukawa (Solar System/LLR/lab) sa zgodne z zakresem analizy T04 | Park et al. (2017), DOI: 10.3847/1538-3881/aa5be2; Sun et al. (2019), DOI: 10.1103/PhysRevD.100.084030; Kapner et al. (2007), DOI: 10.1103/PhysRevLett.98.021101 | peer-reviewed | 0.80 | verified |

## Metadane bibliograficzne (zweryfikowane API)
- 10.12942/lrr-2014-4 -> Living Reviews in Relativity (2014): "The Confrontation between General Relativity and Experiment".
- 10.3847/1538-3881/aa5be2 -> The Astronomical Journal (2017): "Precession of Mercury's Perihelion from Ranging to the MESSENGER Spacecraft".
- 10.1103/PhysRevD.100.084030 -> Physical Review D (2019): "Constraints on fifth forces through perihelion precession of planets".
- 10.1103/PhysRevLett.98.021101 -> Physical Review Letters (2007): laboratory inverse-square-law test constraints.

## Uwagi
- Braki zrodlowe sa krytyczne dla finalnej rekomendacji gate.
- Discovery i cross-reference uzupelniaja ten rejestr przed Gate 2.
- Do czasu uzupelnienia tabeli claim->source, status gate powinien pozostac co najmniej Warning.
- Jesli braki obejmuja twierdzenia krytyczne (EQ:T04-1..EQ:T04-4), traktuj jako Blocker (fail_closed).
- Polityka zrodel: peer-reviewed + preprint jest dopuszczona, ale kazdy preprint musi miec jawna etykiete ryzyka.
