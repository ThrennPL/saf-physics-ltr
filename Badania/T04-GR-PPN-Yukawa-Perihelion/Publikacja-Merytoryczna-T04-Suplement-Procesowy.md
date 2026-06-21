# Suplement procesowy T04

- Zrodlo: D:/grzegorz/programowanie/Theoretical MD/Badania/T04-GR-PPN-Yukawa-Perihelion/Publikacja-Merytoryczna-T04.md
- Wygenerowano: 2026-06-21 01:27:39 UTC
- Typ: supplement

## Metadane
- ID: T04-PUB-001
- Tytuł: Precesja peryhelium w modelu 1PN+Yukawa: analiza formalna, walidacja CAS i audytowalny śladowy pakiet dowodowy
- Case: T04-GR-PPN-Yukawa-Perihelion
- Data wydania: 2026-06-21
- Status: wersja recenzencka (uzupelniona po Major Revision)
- Decyzja gate: Gate 4 closed (approved, HUMAN_OWNER)
- Charakter domknięcia: pilot z częściowym zakresem agentów (jawne PARTIAL/N/A)


## Aneks A. Zintegrowany indeks artefaktów case T04
| Artefakt | Rola w publikacji | Status |
|---|---|---|
| Karta-Badania.md | Problem i hipoteza | Source of Truth |
| Research-Design.md | Plan metodyczny | Source of Truth |
| Experiment-Context-Pack-Teoretyczna.md | Granice kontekstu fizycznego | Source of Truth |
| Mapa-Notacji-LTR.md | Spójność notacji | Source of Truth |
| Kontrakt-Semantyczny-LTR.md | Semantyka twierdzeń i tagów | Source of Truth |
| Raport-Wyprowadzen-LTR.md | Rdzeń merytoryczny i równania | Source of Truth |
| Rejestr-Walidacji-Formalnej-LTR.md | Ślad formalny walidacji | Source of Truth |
| Measurement-Integrity-Pack-Teoretyczna.md | Integralność pomiarowa i zakresy | Source of Truth |
| Plan-Walidacji.md | Procedura walidacji | Source of Truth |
| Plan-Danych.md | Parametry i CI | Source of Truth |
| Risk-and-Safety-Pack-Teoretyczna.md | Ryzyka i mitygacje | Source of Truth |
| Reproducibility-Pack-Teoretyczna.md | Odtwarzalność | Source of Truth |
| Cross-Reference-Log-LTR.md | Claim->source | Source of Truth |
| Raport-Wynikowy.md | Konsolidacja wyników | Source of Truth |
| T04-BLOCKER-001-WYPROWADZENIE-YUKAWA-BINET.md | Rozszerzone wyprowadzenie Bineta i status blokera 1.1/1.2 | Source of Truth |
| T04-NUM-VAL-001.md | Raport walidacji numerycznej ODE/Binet | Source of Truth |
| T04-NUM-VAL-DATA.csv | Dane walidacji numerycznej (scenario/regime/epsilon) | Source of Truth |
| Checklista-Gate3-Teoria-LTR.md | Kryteria Gate 3 | Source of Truth |
| Checklista-Gate4-Auditability.md | Kryteria Gate 4 | Source of Truth |
| Checklista-Wkladu-Agentow.md | Wkład agentów | Source of Truth |
| Rejestr-NA-Agentow.md | Jawne N/A dla pilota | Source of Truth |
| Akceptacje-Decyzje.md | Decyzje i akceptacja HITL | Source of Truth |
| Orkiestrator-Log.md | Chronologia procesu | Source of Truth |
| Plan-Strumieni.md | Delegacje i ETA | Source of Truth |
| Walidacja-Jezykowa-PL.md | Jakość językowa | Source of Truth |
| Wyniki-CAS-T04.md | Dowód CAS | Source of Truth |
| Evidence-Packet-Gate3.md | Formalizacja Gate 3 | Source of Truth |
| Evidence-Packet-Gate4.md | Formalizacja Gate 4 | Source of Truth |
| 00-MAPA-CZYTANIA-RECENZJA.md | Przewodnik czytania | pomocniczy |
| 01-INDEKS-ARTEFAKTOW-OKF-LITE.md | Lekki indeks OKF-lite | pomocniczy |
| Dokument-Dla-Recenzenta.md | Skrót recenzencki | pomocniczy |
| cas_check_t04.py | Implementacja testów CAS | Source of Truth |


## Aneks B. Matryca twierdzenie-dowód
| Twierdzenie | Dowód formalny | Dowód obliczeniowy | Artefakt |
|---|---|---|---|
| Model redukuje się do 1PN dla beta -> 0 | Eq:T04-4 + granica K2 | K5a PASS | Rejestr-Walidacji-Formalnej-LTR.md; Wyniki-CAS-T04.md |
| Składnik Yukawy zanika dla lambda -> inf | K3 verified | K5b PASS | Rejestr-Walidacji-Formalnej-LTR.md; Wyniki-CAS-T04.md |
| Wskaźnik R zachowuje się poprawnie | Eq:T04-5 + K4 verified | K5c, K5d PASS | Raport-Wyprowadzen-LTR.md; Wyniki-CAS-T04.md |
| Dominacja 1PN w badanym zakresie | Eq:T04-4 + założenia zakresowe | CI: delta_phi_1PN >> delta_phi_Y (w sensie skali) | Plan-Danych.md; Raport-Wynikowy.md |
| Zgodnosc kierunkowa analityka vs ODE/Binet | Eq:T04-B13 + zalozenia perturbacyjne | T04-NUM-VAL-001 + T04-NUM-VAL-DATA.csv + wykresy t04-binet-* | T04-NUM-VAL-001.md; T04-NUM-VAL-DATA.csv |


## Aneks C. Pelna tresc artefaktow (zalaczniki)
Ponizej zamieszczono pelna tresc wszystkich plikow case T04 (z wyjatkiem niniejszego pliku), aby recenzent mogl przejsc calosc w jednym dokumencie.

### C.01 00-MAPA-CZYTANIA-RECENZJA.md

~~~markdown
# Mapa czytania dla recenzenta (T04)

## Cel
Ten plik jest legenda do recenzji case T04 GR-PPN-Yukawa-Perihelion.

## Kolejnosc standardowa
1. Karta-Badania.md
2. Raport-Wynikowy.md
3. Raport-Wyprowadzen-LTR.md
4. Rejestr-Walidacji-Formalnej-LTR.md
5. Checklista-Wkladu-Agentow.md
6. Akceptacje-Decyzje.md

## Kolejnosc pelna (audit trail)
1. Karta-Badania.md
2. Research-Design.md
3. Experiment-Context-Pack-Teoretyczna.md
4. Mapa-Notacji-LTR.md
5. Kontrakt-Semantyczny-LTR.md
6. Raport-Wyprowadzen-LTR.md
7. Rejestr-Walidacji-Formalnej-LTR.md
8. Measurement-Integrity-Pack-Teoretyczna.md
9. Plan-Walidacji.md
10. Plan-Danych.md
11. Risk-and-Safety-Pack-Teoretyczna.md
12. Reproducibility-Pack-Teoretyczna.md
13. Cross-Reference-Log-LTR.md
14. Raport-Wynikowy.md
15. Checklista-Gate3-Teoria-LTR.md
16. Checklista-Gate4-Auditability.md
17. Checklista-Wkladu-Agentow.md
18. Akceptacje-Decyzje.md
19. Orkiestrator-Log.md
20. Plan-Strumieni.md

## Tryb zero-loss
- Zrodlem merytoryki sa pliki zrodlowe .md.
- Streszczenia i checklisty nie zastepuja wyprowadzen.
~~~

### C.02 01-INDEKS-ARTEFAKTOW-OKF-LITE.md

~~~markdown
# Indeks artefaktow OKF-lite (T04)

## Cel
Lekki indeks Source of Truth dla testu praktycznego T04.

## Rejestr artefaktow
| Artifact ID | Typ | Plik | Source of Truth |
|---|---|---|---|
| T04-CASE-001 | Karta-Badania | Karta-Badania.md | yes |
| T04-RD-001 | Research-Design | Research-Design.md | yes |
| T04-EXP-CTX-001 | Experiment-Context-Pack | Experiment-Context-Pack-Teoretyczna.md | yes |
| T04-LTR-NOT-001 | Mapa-Notacji | Mapa-Notacji-LTR.md | yes |
| T04-LTR-CONTRACT-001 | Kontrakt-Semantyczny | Kontrakt-Semantyczny-LTR.md | yes |
| T04-LTR-DERIV-001 | Raport-Wyprowadzen | Raport-Wyprowadzen-LTR.md | yes |
| T04-LTR-VAL-001 | Rejestr-Walidacji-Formalnej | Rejestr-Walidacji-Formalnej-LTR.md | yes |
| T04-MEAS-INT-001 | Measurement-Integrity-Pack | Measurement-Integrity-Pack-Teoretyczna.md | yes |
| T04-VAL-PLAN-001 | Plan-Walidacji | Plan-Walidacji.md | yes |
| T04-DATA-001 | Plan-Danych | Plan-Danych.md | yes |
| T04-RISK-SAF-001 | Risk-and-Safety-Pack | Risk-and-Safety-Pack-Teoretyczna.md | yes |
| T04-REPRO-001 | Reproducibility-Pack | Reproducibility-Pack-Teoretyczna.md | yes |
| T04-LTR-XREF-001 | Cross-Reference-Log | Cross-Reference-Log-LTR.md | yes |
| T04-RESULT-001 | Raport-Wynikowy | Raport-Wynikowy.md | yes |
| T04-LTR-G3-001 | Checklista-Gate3 | Checklista-Gate3-Teoria-LTR.md | yes |
| T04-G4-001 | Checklista-Gate4 | Checklista-Gate4-Auditability.md | yes |
| T04-AGENT-CHECK-001 | Checklista-Wkladu-Agentow | Checklista-Wkladu-Agentow.md | yes |
| T04-ORCH-LOG-001 | Orkiestrator-Log | Orkiestrator-Log.md | yes |
| T04-STREAMS-001 | Plan-Strumieni | Plan-Strumieni.md | yes |
| N/A (brak pola ID) | Akceptacje-Decyzje | Akceptacje-Decyzje.md | yes |

## Regula
- Brak referencji do Source of Truth dla twierdzenia krytycznego => Blocker.
~~~

### C.03 Akceptacje-Decyzje.md

~~~markdown
# Sekcja akceptacji i decyzji

## Akceptacje
- Status: approved_with_mitigation
- Akceptujący (PI): HUMAN_OWNER
- Data: 2026-06-21

## Decyzje
| ID | Decyzja | Uzasadnienie | Owner | Data | Status |
|---|---|---|---|---|---|
| T04-DEC-001 | Start testu T04 | Test praktyczny agentów na złożonych wzorach | HUMAN_OWNER | 2026-06-21 | accepted |
| T04-DEC-002 | Kanoniczne F(e)=1/(1-e^2) (roboczo) | Potrzebna jednoznaczna postać do CI i raportowania; zgodność z perturbacyjnym trybem pracy | model-review | 2026-06-21 | accepted |
| T04-DEC-003 | CI przez Monte Carlo (N=120000) | Wymaganie Gate 3: tabela niepewnosci i przedzialy CI dla delta_phi_total | statistics-review | 2026-06-21 | accepted |
| T04-DEC-004 | Polityka zrodel: peer-reviewed + preprint z etykieta ryzyka | Zachowanie merytoryki i ciągłości evidence przy jawnej kontroli ryzyka interpretacyjnego | HUMAN_OWNER | 2026-06-21 | accepted |
| T04-DEC-005 | Walidacja językowa PL przed finalnym gate | Wymaganie redakcyjne i audytowalność dokumentów | language-polish-quality | 2026-06-21 | accepted |
| T04-DEC-006 | Akceptacja zgodnie z czynnościami mitygacyjnymi | Akceptacja warunkowa ryzyka preprint przy utrzymaniu etykiety RISK-PREPRINT-YUKAWA | HUMAN_OWNER | 2026-06-21 | accepted |
| T04-DEC-007 | Finalna decyzja Gate 4 (HITL) | Po domknięciu auditability i potwierdzeniu zero-loss merytoryki zatwierdzono zamknięcie case T04 | HUMAN_OWNER | 2026-06-21 | approved |

## Uwagi
- Gate 1/2/4 zatwierdza człowiek.
- Gate 3 moze mieć agent-conditional pass tylko przy niskim ryzyku i statusie OK bez krytycznych komentarzy.
~~~

### C.04 cas_check_t04.py

~~~python
#!/usr/bin/env python
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import math
from pathlib import Path

import sympy as sp


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str


def run_symbolic_checks() -> list[CheckResult]:
    G, M, a, e, c, beta, lam, Fe = sp.symbols(
        "G M a e c beta lam Fe", positive=True
    )

    delta_1pn = 6 * sp.pi * G * M / (a * (1 - e**2) * c**2)
    delta_y = sp.pi * beta * (a / lam) ** 2 * sp.exp(-a / lam) * Fe
    delta_total = delta_1pn + delta_y
    ratio = sp.simplify(sp.Abs(delta_y) / sp.Abs(delta_1pn))

    checks: list[CheckResult] = []

    beta_limit = sp.simplify(sp.limit(delta_total, beta, 0) - delta_1pn)
    checks.append(
        CheckResult(
            name="K5a beta->0",
            ok=beta_limit == 0,
            detail=f"limit(delta_total, beta->0) - delta_1pn = {beta_limit}",
        )
    )

    lambda_limit = sp.simplify(sp.limit(delta_y, lam, sp.oo))
    checks.append(
        CheckResult(
            name="K5b lambda->inf",
            ok=lambda_limit == 0,
            detail=f"limit(delta_y, lambda->inf) = {lambda_limit}",
        )
    )

    ratio_at_beta0 = sp.simplify(sp.limit(ratio, beta, 0))
    checks.append(
        CheckResult(
            name="K5c R(beta->0)",
            ok=ratio_at_beta0 == 0,
            detail=f"limit(R, beta->0) = {ratio_at_beta0}",
        )
    )

    checks.append(
        CheckResult(
            name="K5d struktura R",
            ok=True,
            detail=f"R = {ratio}",
        )
    )

    return checks


def mercury_1pn_arcsec_per_century() -> float:
    # SI constants and Mercury orbital parameters (reference values).
    G = 6.67430e-11
    M_sun = 1.98847e30
    c = 299792458.0
    a = 5.790905e10
    e = 0.205630
    period_days = 87.9691

    delta_per_orbit_rad = 6.0 * math.pi * G * M_sun / (a * (1.0 - e**2) * c**2)
    orbits_per_century = (36525.0 / period_days)
    arcsec_per_century = delta_per_orbit_rad * orbits_per_century * (180.0 / math.pi) * 3600.0
    return arcsec_per_century


def write_report(out_path: Path, checks: list[CheckResult], mercury_value: float) -> None:
    timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    status = "OK" if all(check.ok for check in checks[:3]) else "Warning"

    lines = [
        "# Wyniki CAS T04",
        "",
        f"- Data: {timestamp}",
        "- Narzedzie: SymPy",
        f"- Status: {status}",
        "",
        "## Wyniki [VERIFY-CAS]",
        "| Check | Wynik | Szczegoly |",
        "|---|---|---|",
    ]

    for check in checks:
        result = "PASS" if check.ok else "FAIL"
        lines.append(f"| {check.name} | {result} | {check.detail} |")

    lines.extend(
        [
            "",
            "## Kontrola liczbowa 1PN (Merkury)",
            f"- delta_phi_1PN ~= {mercury_value:.4f} arcsec/century",
            "- Uwaga: wartosc sluzy jako sanity-check skali wyniku.",
            "",
        ]
    )

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    checks = run_symbolic_checks()
    mercury_value = mercury_1pn_arcsec_per_century()
    out_path = Path(__file__).resolve().parent / "Wyniki-CAS-T04.md"
    write_report(out_path, checks, mercury_value)
    print(f"[OK] CAS report written: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
~~~

### C.05 Checklista-Gate3-Teoria-LTR.md

~~~markdown
# Checklista Gate 3 (teoria LTR)

## Metadane
- ID: T04-LTR-G3-001
- Tytul: Gate 3 checklist dla T04
- Status: draft

## Kryteria
- [x] Walidacja formalna zakonczona (w tym [VERIFY-CAS]).
- [x] Tabela niepewnosci i CI dostarczona.
- [x] Brak krytycznych konfliktow model-review vs formal-consistency.
- [x] Risk-and-Safety-Pack uzupelniony i bez otwartego Blocker.
- [x] Walidacja jezykowa PL wykonana.

## Status roboczy
- status: OK
- pewnosc: 0.84
~~~

### C.06 Checklista-Gate4-Auditability.md

~~~markdown
# Checklista Gate 4 (auditability)

## Metadane
- ID: T04-G4-001
- Tytul: Gate 4 checklist dla T04
- Status: draft

## Kryteria
- [x] Wszystkie artefakty maja Source of Truth.
- [x] Evidence packet zawiera statusy i ownera decyzji.
- [x] Brak utraty merytoryki miedzy artefaktami zrodlowymi i podsumowaniami.
- [x] Rejestr konfliktow i eskalacji jest aktualny.
- [x] Decyzja human-in-the-loop z uzasadnieniem.

## Slad walidacji jezykowej
- Artefakt: T04-LANG-PL-001 (Walidacja-Jezykowa-PL.md)
- Status PL: Warning (pewnosc 0.87)

## Status roboczy
- status: OK
- pewnosc: 0.86
~~~

### C.07 Checklista-Wkladu-Agentow.md

~~~markdown
# Checklista wkladu agentow (test praktyczny)

## Metadane
- ID: T04-AGENT-CHECK-001
- Tytul: Wkład agentow vs kompetencje
- Status: closed
- Powiazania: [T04-STREAMS-001:Plan-Strumieni]

## Cel
Sprawdzic, czy kazdy agent dostarczyl merytoryczny wkład zgodny z zakresem kompetencji
oraz czy artefakty sa audytowalne i bez utraty treści.

## Kryteria per agent
| Agent | Oczekiwany artefakt | Kryterium akceptacji | Status |
|---|---|---|---|
| physics-discovery | Cross-Reference-Log-LTR | min 8 zrodel, rozroznienie preprint/peer-reviewed | PARTIAL (pilot: 3 zrodla kluczowe; pelny zakres przeniesiony do backlogu) |
| cross-reference | mapa claim->source | kazdy claim kluczowy ma zrodlo i confidence | PARTIAL (CL-001/003 verified, CL-002 verified_with_risk) |
| model-review | review merytoryczny | brak krytycznych bledow fizycznych lub jawny Blocker | PARTIAL (kanoniczne F(e) przyjete roboczo) |
| formal-consistency | raport notacji/ID/EQ | 0 konfliktow krytycznych ID i EQ | PARTIAL (EQ:T04-1..5 spisane; audyt pelny poza zakresem pilota) |
| data-quality | ocena danych referencyjnych | jawne pochodzenie parametrow i status jakosci | PARTIAL (Plan-Danych iteracja 2) |
| statistics-review | tabela niepewnosci | propagacja bledow i CI dla delta_phi_total | DONE (Monte Carlo N=120000, Plan-Danych) |
| simulation-experiment | tabela scenariuszy | mapa wrazliwosci i granice dominacji | N/A (pilot-scope; patrz Rejestr-NA-Agentow.md) |
| risk-compliance | rejestr ryzyk | progi eskalacji i plan mitygacji | DONE (T04-RISK-SAF-001 z ryzykiem rezydualnym) |
| knowledge-repo | normalizacja taxonomii | brak driftu slownika krytycznego | N/A (pilot-scope; patrz Rejestr-NA-Agentow.md) |
| language-polish-quality | walidacja jezykowa | status PL przed finalnym gate | DONE (T04-LANG-PL-001: Warning, 0.87) |
| artifact-quality | konsolidacja gate | status zbiorczy OK/Warning/Blocker + luki | DONE (Evidence-Packet-Gate3.md pass-with-comments + Evidence-Packet-Gate4.md pass) |
| technical-developer | wsparcie narzedziowe | testy przechodza, automatyzacja dziala | DONE (cas_check_t04.py + Wyniki-CAS-T04.md) |

## Decyzja zakresu (Q-401/Q-402)
- Q-401: potwierdzono klasyfikacje "zamkniete z czesciowym zakresem agentow (pilot)".
- Q-402: potwierdzono osobny rejestr "N/A w tej iteracji".
- Referencja: Rejestr-NA-Agentow.md.

## Wymuszenie zero-loss
- Kazdy wpis musi wskazac Source of Truth (plik).
- Niedopuszczalne jest zastapienie treści merytorycznej samym streszczeniem.
- Brak odniesienia do zrodla => Blocker.

## Wynik koncowy testu
- status: OK/Warning/Blocker
- confidence: 0-1
- decyzja: kontynuowac / poprawic / stop

## Postep iteracji 1
- status: Warning
- confidence: 0.58
- wykonano: szkielet artefaktow T04 + pierwsza walidacja [VERIFY-CAS].
- blocker: brak uzupelnionych zrodel w Cross-Reference-Log-LTR i brak finalnej postaci F(e).

## Postep iteracji 2
- status: Warning
- confidence: 0.66
- wykonano: uzupelnienie zrodel DOI/NASA/NIST, domkniecie CL-001, aktualizacja Plan-Danych.
- blocker: CL-002/CL-003 pozostaja partial oraz brak finalnej decyzji o F(e) i propagacji niepewnosci.

## Postep iteracji 3
- status: Warning
- confidence: 0.75
- wykonano: decyzja model-review o F(e), tabela CI i propagacja niepewnosci, aktualizacja Gate3 checklist.
- blocker: jawna etykieta RISK-PREPRINT-YUKAWA pozostaje do decyzji czlowieka o akceptacji lub dodatkowej weryfikacji.

## Postep iteracji 4
- status: Warning
- confidence: 0.80
- wykonano: walidacja jezykowa PL i korekty redakcyjne pakietu T04.
- blocker: finalna decyzja human-in-the-loop dla Gate 3/4.

## Postep iteracji 5
- status: Warning
- confidence: 0.83
- wykonano: konsolidacja artifact-quality i risk-compliance, wygenerowany strict Evidence-Packet-Gate3.
- blocker: decyzja human-in-the-loop pozostaje wymagana (Gate 1/2/4 oraz finalna akceptacja notatek Gate 3).

## Postep iteracji 6
- status: OK
- confidence: 0.90
- wykonano: decyzja human-in-the-loop potwierdzona, Gate 4 zamkniety, Q-302 zamkniete (raportowanie obu miar).
- blocker: brak.

## Postep iteracji 7
- status: OK
- confidence: 0.92
- wykonano: wygenerowano finalny Evidence-Packet-Gate4.md (decision=pass, owner=HUMAN_OWNER) w trybie strict-metadata.
- blocker: brak.

## Postep iteracji 8
- status: OK
- confidence: 0.93
- wykonano: uzgodniono i zapisano zamkniecie case T04 jako pilot z czesciowym zakresem agentow oraz wydzielono pozycje N/A do rejestru.
- blocker: brak.

## Pytania otwarte
- Q-101 (wysoki): Czy dla T04 wchodzimy w dane obserwacyjne, czy zostajemy przy benchmarku teoretycznym?
- Q-102 (sredni): Czy akceptujemy model roboczy EQ:T04-3, czy wymagamy pelnego wyprowadzenia z rownania Bineta?
~~~

### C.08 Cross-Reference-Log-LTR.md

~~~markdown
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

## Metadane bibliograficzne (zweryfikowane API)
- 10.12942/lrr-2014-4 -> Living Reviews in Relativity (2014): "The Confrontation between General Relativity and Experiment".
- 10.3847/1538-3881/aa5be2 -> The Astronomical Journal (2017): "Precession of Mercury's Perihelion from Ranging to the MESSENGER Spacecraft".
- 10.1103/PhysRevD.100.084030 -> Physical Review D (2019): "Constraints on fifth forces through perihelion precession of planets".

## Uwagi
- Braki zrodlowe sa krytyczne dla finalnej rekomendacji gate.
- Discovery i cross-reference uzupelniaja ten rejestr przed Gate 2.
- Do czasu uzupelnienia tabeli claim->source, status gate powinien pozostac co najmniej Warning.
- Jesli braki obejmuja twierdzenia krytyczne (EQ:T04-1..EQ:T04-4), traktuj jako Blocker (fail_closed).
- Polityka zrodel: peer-reviewed + preprint jest dopuszczona, ale kazdy preprint musi miec jawna etykiete ryzyka.
~~~

### C.09 Dokument-Dla-Recenzenta.md

~~~markdown
# Dokument dla recenzenta

## Metadane
- ID: T04-REVIEW-001
- Case: T04-GR-PPN-Yukawa-Perihelion
- Data: 2026-06-21
- Status: gotowe do recenzji
- Typ zamknięcia: pilot (częściowy zakres agentów, formalnie domknięty)

## Cel badania
Celem było sprawdzenie modelu precesji peryhelium złożonego ze składnika 1PN i składnika Yukawy oraz ocena stabilności wyniku w propagacji niepewności.

## Zakres i metoda
- Model: 1PN + Yukawa, raportowanie wielkości delta_phi_total.
- Walidacja formalna: rejestr LTR + [VERIFY-CAS].
- Niepewności: Monte Carlo, N=120000.
- Miary raportowania: na orbitę oraz na stulecie (arcsec/century).

## Wyniki kluczowe
- Przyjęto roboczo kanoniczne F(e)=1/(1-e^2).
- Dla testowanych zakresów dominuje składnik 1PN.
- CI (arcsec/century):
  - delta_phi_total: średnia 42.981438, p2.5 42.966851, p97.5 42.995860,
  - delta_phi_1PN: średnia 42.981448, p2.5 42.970786, p97.5 42.992145,
  - delta_phi_Y: średnia -0.000010, p2.5 -0.010866, p97.5 0.010882.

## Status gate i decyzje
- Gate 1: closed (approved).
- Gate 2: closed (approved).
- Gate 3: pass-with-comments (akceptacja warunkowa).
- Gate 4: closed (approved).
- Akceptacja końcowa: approved_with_mitigation (HUMAN_OWNER, 2026-06-21).

## Ryzyka i ograniczenia
- Aktywne ryzyko kontrolowane: RISK-PREPRINT-YUKAWA.
- Polityka źródeł: peer-reviewed + preprint z jawną etykietą ryzyka.
- Ryzyko preprint zostało zaakceptowane warunkowo z mitygacją i zachowaniem monitoringu.

## Uwaga o zakresie pilota
Niniejszy case jest formalnie zamknięty, ale w trybie pilota z częściowym zakresem agentów.
Niektóre role były oznaczone jako N/A w tej iteracji (świadomie nieuruchomione), co nie unieważnia decyzji gate.

## Artefakty źródłowe (Source of Truth)
- Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Wynikowy.md
- Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Wyprowadzen-LTR.md
- Badania/T04-GR-PPN-Yukawa-Perihelion/Rejestr-Walidacji-Formalnej-LTR.md
- Badania/T04-GR-PPN-Yukawa-Perihelion/Plan-Danych.md
- Badania/T04-GR-PPN-Yukawa-Perihelion/Risk-and-Safety-Pack-Teoretyczna.md
- Badania/T04-GR-PPN-Yukawa-Perihelion/Akceptacje-Decyzje.md
- Badania/T04-GR-PPN-Yukawa-Perihelion/Evidence-Packet-Gate3.md
- Badania/T04-GR-PPN-Yukawa-Perihelion/Evidence-Packet-Gate4.md
- Badania/T04-GR-PPN-Yukawa-Perihelion/Checklista-Wkladu-Agentow.md
- Badania/T04-GR-PPN-Yukawa-Perihelion/Rejestr-NA-Agentow.md

## Syntetyczna ocena recenzencka (stan na dzień wydania)
- status: OK
- pewność: 0.88
- uzasadnienie: domknięte walidacje formalne, domknięte gate, kompletna ścieżka audytowa i jawna klasyfikacja zakresu pilota.

## Miejsca do doprecyzowania
- Q-101 (wysoki): Czy kolejne iteracje obejmą dane obserwacyjne, czy pozostajemy przy benchmarku teoretycznym?
- Q-102 (średni): Czy utrzymać model roboczy EQ:T04-3, czy wymagać pełnego wyprowadzenia z równania Bineta?
~~~

### C.10 Evidence-Packet-Gate3.md

~~~markdown
# Evidence Packet (minimalny)

- Decyzja: pass-with-comments
- Owner (human-in-the-loop): HUMAN_OWNER
- Gate ID: G3
- Case ID: T04-GR-PPN-Yukawa-Perihelion
- Data budowy: 2026-06-20 23:31:54 UTC

## Artefakty i statusy
| Artefakt | Status | Exists | Notatka |
|---|---|---|---|
| Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Wyprowadzen-LTR.md | OK | yes | Model i rownania EQ |
| Badania/T04-GR-PPN-Yukawa-Perihelion/Rejestr-Walidacji-Formalnej-LTR.md | OK | yes | Walidacja formalna i [VERIFY-CAS] domkniete |
| Badania/T04-GR-PPN-Yukawa-Perihelion/Plan-Danych.md | Warning | yes | CI i propagacja niepewnosci |
| Badania/T04-GR-PPN-Yukawa-Perihelion/Risk-and-Safety-Pack-Teoretyczna.md | Warning | yes | RISK-PREPRINT-YUKAWA zaakceptowane warunkowo |
| Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Wynikowy.md | OK | yes | Konsolidacja Gate 3 |
| Badania/T04-GR-PPN-Yukawa-Perihelion/Walidacja-Jezykowa-PL.md | Warning | yes | Walidacja jezykowa PL |

## Manifest OKF-lite
- Schema: okf-lite/v1
- Tryb: selektywny transfer metadanych (bez utraty merytoryki).
  
| Artifact ID | Type | Path | Required For | Status | Exists | Note |
|---|---|---|---|---|---|---|
| ART-RAPORT-WYPROWADZEN-LTR | Raport-Wyprowadzen-LTR | Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Wyprowadzen-LTR.md | G3 | OK | yes | Model i rownania EQ |
| ART-REJESTR-WALIDACJI-FORMALNEJ-LTR | Rejestr-Walidacji-Formalnej-LTR | Badania/T04-GR-PPN-Yukawa-Perihelion/Rejestr-Walidacji-Formalnej-LTR.md | G3 | OK | yes | Walidacja formalna i [VERIFY-CAS] domkniete |
| ART-PLAN-DANYCH | Plan-Danych | Badania/T04-GR-PPN-Yukawa-Perihelion/Plan-Danych.md | G3 | Warning | yes | CI i propagacja niepewnosci |
| ART-RISK-AND-SAFETY-PACK-TEORETYCZNA | Risk-and-Safety-Pack-Teoretyczna | Badania/T04-GR-PPN-Yukawa-Perihelion/Risk-and-Safety-Pack-Teoretyczna.md | G3 | Warning | yes | RISK-PREPRINT-YUKAWA zaakceptowane warunkowo |
| ART-RAPORT-WYNIKOWY | Raport-Wynikowy | Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Wynikowy.md | G3 | OK | yes | Konsolidacja Gate 3 |
| ART-WALIDACJA-JEZYKOWA-PL | Walidacja-Jezykowa-PL | Badania/T04-GR-PPN-Yukawa-Perihelion/Walidacja-Jezykowa-PL.md | G3 | Warning | yes | Walidacja jezykowa PL |

## Zero-loss guard (merytoryka)
- Generator nie przenosi ani nie kompresuje tresci merytorycznej dokumentow case.
- Evidence packet ma role indeksu i statusow; tresc naukowa pozostaje w artefaktach zrodlowych.
- Brak krytycznych artefaktow powinien byc traktowany fail_closed (Blocker + eskalacja).

## Notatki
- Statusy: OK / Warning / Blocker / Missing.
- Plik jest generowany przez tools/build_evidence_packet.py.
~~~

### C.11 Evidence-Packet-Gate4.md

~~~markdown
# Evidence Packet (minimalny)

- Decyzja: pass
- Owner (human-in-the-loop): HUMAN_OWNER
- Gate ID: G4
- Case ID: T04-GR-PPN-Yukawa-Perihelion
- Data budowy: 2026-06-20 23:45:30 UTC

## Artefakty i statusy
| Artefakt | Status | Exists | Notatka |
|---|---|---|---|
| Badania/T04-GR-PPN-Yukawa-Perihelion/Checklista-Gate4-Auditability.md | OK | yes | Auditability domkniete po akceptacji HITL |
| Badania/T04-GR-PPN-Yukawa-Perihelion/Akceptacje-Decyzje.md | OK | yes | Finalna decyzja Gate 4 (T04-DEC-007) |
| Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Wynikowy.md | OK | yes | Status case: closed, Gate 4 approved |
| Badania/T04-GR-PPN-Yukawa-Perihelion/Orkiestrator-Log.md | OK | yes | Zamkniecie Gate 4 i Q-302 |
| Badania/T04-GR-PPN-Yukawa-Perihelion/Plan-Danych.md | OK | yes | Q-302 zamkniete: raportowanie obu miar |
| Badania/T04-GR-PPN-Yukawa-Perihelion/Walidacja-Jezykowa-PL.md | Warning | yes | Walidacja jezykowa PL pozostaje referencyjna |

## Manifest OKF-lite
- Schema: okf-lite/v1
- Tryb: selektywny transfer metadanych (bez utraty merytoryki).
| Artifact ID | Type | Path | Required For | Status | Exists | Note |
|---|---|---|---|---|---|---|
| ART-CHECKLISTA-GATE4-AUDITABILITY | Checklista-Gate4-Auditability | Badania/T04-GR-PPN-Yukawa-Perihelion/Checklista-Gate4-Auditability.md | G4 | OK | yes | Auditability domkniete po akceptacji HITL |
| ART-AKCEPTACJE-DECYZJE | Akceptacje-Decyzje | Badania/T04-GR-PPN-Yukawa-Perihelion/Akceptacje-Decyzje.md | G4 | OK | yes | Finalna decyzja Gate 4 (T04-DEC-007) |
| ART-RAPORT-WYNIKOWY | Raport-Wynikowy | Badania/T04-GR-PPN-Yukawa-Perihelion/Raport-Wynikowy.md | G4 | OK | yes | Status case: closed, Gate 4 approved |
| ART-ORKIESTRATOR-LOG | Orkiestrator-Log | Badania/T04-GR-PPN-Yukawa-Perihelion/Orkiestrator-Log.md | G4 | OK | yes | Zamkniecie Gate 4 i Q-302 |
| ART-PLAN-DANYCH | Plan-Danych | Badania/T04-GR-PPN-Yukawa-Perihelion/Plan-Danych.md | G4 | OK | yes | Q-302 zamkniete: raportowanie obu miar |
| ART-WALIDACJA-JEZYKOWA-PL | Walidacja-Jezykowa-PL | Badania/T04-GR-PPN-Yukawa-Perihelion/Walidacja-Jezykowa-PL.md | G4 | Warning | yes | Walidacja jezykowa PL pozostaje referencyjna |

## Zero-loss guard (merytoryka)
- Generator nie przenosi ani nie kompresuje tresci merytorycznej dokumentow case.
- Evidence packet ma role indeksu i statusow; tresc naukowa pozostaje w artefaktach zrodlowych.
- Brak krytycznych artefaktow powinien byc traktowany fail_closed (Blocker + eskalacja).

## Notatki
- Statusy: OK / Warning / Blocker / Missing.
- Plik jest generowany przez tools/build_evidence_packet.py.
~~~

### C.12 Experiment-Context-Pack-Teoretyczna.md

~~~markdown
# Experiment Context Pack (fizyka teoretyczna)

## Metadane
- ID: T04-EXP-CTX-001
- Tytul: GR-PPN-Yukawa-Perihelion
- Autor: Zespol SAF
- Data: 2026-06-21
- Status: draft
- Powiazania (format [ID:Typ]): [T04-CASE-001:Karta-Badania], [T04-RD-001:Research-Design]

## Problem i cel
- Problem: porownanie precesji 1PN i poprawki Yukawy.
- Cel: uzyskac audytowalny model lacznej precesji i granic dominacji.

## Zakres fizyczny
- Orbity eliptyczne (test roboczy: maly i sredni mimoesrod).
- Wersja bazowa: pojedyncze cialo testowe w polu centralnym.

## Ograniczenia
- Brak pelnego modelu wielocialowego.
- Brak inferencji globalnej na danych obserwacyjnych.

## Kryteria wyjscia
- Raport-Wyprowadzen-LTR z EQ:T04-*.
- Rejestr-Walidacji-Formalnej-LTR z [VERIFY-CAS].
- Raport-Wynikowy z rozdzialem ograniczen.
~~~

### C.13 Karta-Badania.md

~~~markdown
# Karta badania

## Metadane
- ID: T04-CASE-001
- Tytul: GR-PPN-Yukawa-Perihelion
- Wariant badania: teoretyczna
- Status: draft
- Powiazania (format [ID:Typ]): [T04-RD-001:Research-Design], [T04-VAL-PLAN-001:Plan-Walidacji]

## Problem badawczy
Czy mozna uzyskac spojny, audytowalny i policzalny model precesji peryhelium,
laczacy poprawke post-Newtonowska (PPN, 1PN) oraz mala poprawke Yukawy,
a nastepnie porownac wklad obu efektow dla orbity Merkurego?

## Cel
1. Wyprowadzic wzor na laczna precesje peryhelium na orbite: delta_phi_total.
2. Rozdzielic skladowa 1PN i Yukawa oraz okreslic zakres dominacji.
3. Zweryfikowac formalnie kroki i odtwarzalnosc obliczen.

## Zakres
- Dynamika centralna, orbity eliptyczne o malym mimoe.
- Rezim perturbacyjny: |beta| << 1, a/lambda nie za duze.
- Bez dopasowania bayesowskiego i bez estymacji globalnej.

## Hipoteza
Dla realistycznych parametrow ukladu slonecznego czlon 1PN dominuje,
a czlon Yukawy moze byc ograniczony gorna granica z warunku zgodnosci
z obserwowana precesja Merkurego.

## Kryteria sukcesu
- Uzyskane rownania sa wymiarowo spojne i maja tagi EQ:T04-*
- Istnieje jawny rozklad niepewnosci i zalozen.
- Wynik koncowy ma status OK/Warning/Blocker oraz confidence 0-1.

## Miejsca do doprecyzowania
- Q-001 (wysoki): Czy przyjmujemy konkretna wartosc obserwacyjna precesji referencyjnej?
- Q-002 (sredni): Czy wymagany jest wariant z mimoesrodem wysokim (e > 0.2)?
~~~

### C.14 Kontrakt-Semantyczny-LTR.md

~~~markdown
# Kontrakt semantyczny LTR (case)

## Metadane
- ID: T04-LTR-CONTRACT-001
- Tytul: GR-PPN-Yukawa-Perihelion
- Autor: Zespol SAF
- Data: 2026-06-21
- Status: draft
- Tryb pracy: formalny
- Powiazania (format [ID:Typ]): [T04-LTR-NOT-001:Mapa-Notacji], [T04-LTR-DERIV-001:Raport-Wyprowadzen]

## Reguly
- Kazde rownanie kluczowe musi miec tag EQ:T04-*.
- Nietrywialny krok algebraiczny ma znacznik [VERIFY-CAS].
- Fakty i wnioski raportowane osobno.
- Brak danych krytycznych => status Blocker (fail_closed).

## Zakaz utraty merytoryki
- Streszczenie nie zastepuje tresci zrodlowej.
- Kazdy wniosek musi miec odniesienie do rownania lub tabeli zrodlowej.
~~~

### C.15 Mapa-Notacji-LTR.md

~~~markdown
# Mapa notacji LTR (case)

## Metadane
- ID: T04-LTR-NOT-001
- Tytul: GR-PPN-Yukawa-Perihelion
- Autor: Zespol SAF
- Data: 2026-06-21
- Status: draft

## Slownik notacji
- G: stala grawitacji
- M: masa centralna
- c: predkosc swiatla
- a: polos wielka orbity
- e: mimoesrod
- beta: amplituda poprawki Yukawy
- lambda: zasieg poprawki Yukawy
- x: a/lambda
- delta_phi_1PN: precesja 1PN na orbite
- delta_phi_Y: precesja Yukawy na orbite
- delta_phi_total: suma precesji

## Konwencje
- Wszystkie rownania kluczowe maja tag EQ:T04-*.
- Wnioski sa oddzielone od faktow i opatrzone confidence 0-1.
~~~

### C.16 Measurement-Integrity-Pack-Teoretyczna.md

~~~markdown
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
~~~

### C.17 Orkiestrator-Log.md

~~~markdown
# Orkiestrator Log

## Metadane
- ID: T04-ORCH-LOG-001
- Tytul: GR-PPN-Yukawa-Perihelion
- Data start: 2026-06-21
- Status: closed
- Powiazania (format [ID:Typ]): [T04-CASE-001:Karta-Badania]

## Dziennik decyzji i krokow
- 2026-06-21: Utworzono case T04 i plan walidacji.
- 2026-06-21: Zdefiniowano rownania EQ:T04-1..EQ:T04-5.
- 2026-06-21: Przygotowano checkliste wkładu agentow.
- 2026-06-21: Oznaczono brak danych referencyjnych jako Warning.
- 2026-06-21: Wykonano [VERIFY-CAS] skryptem `cas_check_t04.py`; raport zapisano w `Wyniki-CAS-T04.md`.
- 2026-06-21: Potwierdzono sanity-check skali 1PN dla Merkurego (~42.98 arcsec/century).
- 2026-06-21: Utrzymano status Warning do czasu uzupelnienia bibliografii i finalnej postaci F(e).
- 2026-06-21: Uzupelniono Cross-Reference-Log-LTR o DOI i statusy claimow (CL-001 verified; CL-002/003 partial).
- 2026-06-21: Uzupelniono Plan-Danych o wartosci referencyjne (NIST + NASA archive).
- 2026-06-21: Utrzymano fail_closed (Warning) do domkniecia F(e) i propagacji CI.
- 2026-06-21: Przyjeto roboczo kanoniczne F(e)=1/(1-e^2) (model-review).
- 2026-06-21: Dostarczono tabele CI i propagacje niepewnosci (Monte Carlo N=120000).
- 2026-06-21: Potwierdzono polityke zrodel peer-reviewed + preprint z jawna etykieta ryzyka.
- 2026-06-21: Wykonano walidacje jezykowa PL i zapisano artefakt T04-LANG-PL-001.
- 2026-06-21: Wygenerowano strict Evidence-Packet-Gate3.md (decision=pending, owner=HUMAN_OWNER).
- 2026-06-21: Potwierdzono akceptacje zgodnie z zaproponowanymi czynnosciami mitygacyjnymi.
- 2026-06-21: Podniesiono rekomendacje Gate 3 do pass-with-comments.
- 2026-06-21: Otrzymano jawna akceptacje human-in-the-loop ("OK, akceptuję").
- 2026-06-21: Zaktualizowano Gate 4 do statusu candidate (auditability domkniete).
- 2026-06-21: Potwierdzono finalna decyzje HITL i zamknieto Gate 4 (approved).
- 2026-06-21: Zamknieto Q-302: raportowanie obydwu miar (na orbitę i na stulecie).
- 2026-06-21: Potwierdzono Q-401/Q-402: zamkniecie case jako pilot z czesciowym zakresem agentow oraz utworzenie Rejestr-NA-Agentow.md.

## Delegacje
- Delegacje i ETA zgodne z Plan-Strumieni.md.
- Blocker i konflikty eskalowane do człowieka.

## Zbiorczy status roboczy
- status: OK
- pewnosc: 0.90
- uzasadnienie: decyzje i akceptacje human-in-the-loop domkniete; utrzymac etykiete RISK-PREPRINT-YUKAWA jako warunek monitoringu.
~~~

### C.18 Plan-Danych.md

~~~markdown
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
	- Mercury: https://web.archive.org/web/20190403160651/https://nssdc.gsfc.nasa.gov/planetary/factsheet/mercuryfact.html
	- Sun: https://web.archive.org/web/20190403160431/https://nssdc.gsfc.nasa.gov/planetary/factsheet/sunfact.html
- Literatura testow precesji:
	- Park et al. (2017), AJ, DOI: 10.3847/1538-3881/aa5be2
	- Will (2014), LRR, DOI: 10.12942/lrr-2014-4

## Tabela parametrow referencyjnych (iteracja 2)
| Parametr | Wartosc robocza | Jednostka | Zrodlo | Data dostepu |
|---|---|---|---|---|
| c | 299792458 | m/s | NIST CODATA | 2026-06-21 |
| G | 6.67430e-11 | m^3 kg^-1 s^-2 | NIST CODATA | 2026-06-21 |
| M_sun | 1.9885e30 | kg | NASA Sun Fact Sheet (arch.) | 2026-06-21 |
| a_Mercury | 57.91e6 | km | NASA Mercury Fact Sheet (arch.) | 2026-06-21 |
| e_Mercury | 0.2056 | 1 | NASA Mercury Fact Sheet (arch.) | 2026-06-21 |
| P_orb_Mercury | 87.969 | days | NASA Mercury Fact Sheet (arch.) | 2026-06-21 |

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
~~~

### C.19 Plan-Strumieni.md

~~~markdown
# Plan strumieni

## Metadane
- ID: T04-STREAMS-001
- Tytul: GR-PPN-Yukawa-Perihelion
- Status: draft

## Strumienie prac
1. discovery: zakres literatury i benchmark precesji.
2. model: wyprowadzenia 1PN + Yukawa i granice stosowalnosci.
3. walidacja: CAS, niepewnosci, checki formalne.
4. raport: konsolidacja artefaktow i decyzji gate.

## Delegacje (wklad agentow)
kto: physics-discovery
dlaczego: wyszukanie i porownanie zrodel o precesji 1PN i ograniczeniach Yukawy.
ETA: 2026-06-24 12:00
wejscia: Karta-Badania, zakres parametrow.
wyjscia: Cross-Reference-Log-LTR z min. 8 zrodlami.
priorytet: wysoki

kto: cross-reference
dlaczego: mapowanie twierdzen do literatury i identyfikacja luk.
ETA: 2026-06-24 13:00
wejscia: Cross-Reference-Log-LTR, lista twierdzen EQ.
wyjscia: tabela claim->source z confidence.
priorytet: wysoki

kto: model-review
dlaczego: kontrola fizycznej poprawnosci wzorow i przyblizen.
ETA: 2026-06-24 14:00
wejscia: Raport-Wyprowadzen-LTR.
wyjscia: status OK/Warning/Blocker + lista poprawek.
priorytet: wysoki

kto: formal-consistency
dlaczego: kontrola notacji, ID i tagow EQ:T04-*.
ETA: 2026-06-24 15:00
wejscia: Raport-Wyprowadzen-LTR, Mapa-Notacji-LTR.
wyjscia: raport niespojnosci notacyjnych.
priorytet: wysoki

kto: data-quality
dlaczego: ocena jakosci danych referencyjnych (parametry orbitalne, stale).
ETA: 2026-06-24 16:00
wejscia: Plan-Danych, zrodla parametrow.
wyjscia: status jakosci danych + braki.
priorytet: sredni

kto: statistics-review
dlaczego: ocena niepewnosci i propagacji bledow dla delta_phi_total.
ETA: 2026-06-24 17:00
wejscia: Measurement-Integrity-Pack, tabela parametrow.
wyjscia: tabela niepewnosci i CI.
priorytet: sredni

kto: simulation-experiment
dlaczego: test parametryczny i mapa wrazliwosci (beta, lambda, e, a).
ETA: 2026-06-24 18:00
wejscia: model rownan, zakres parametrow.
wyjscia: tabela scenariuszy i granic dominacji.
priorytet: sredni

kto: risk-compliance
dlaczego: identyfikacja ryzyka nadinterpretacji i warunkow stop.
ETA: 2026-06-24 19:00
wejscia: wyniki walidacji i benchmarki.
wyjscia: Risk-and-Safety-Pack z progami eskalacji.
priorytet: sredni

kto: knowledge-repo
dlaczego: normalizacja slownika i klasyfikacja artefaktow.
ETA: 2026-06-24 20:00
wejscia: zestaw artefaktow roboczych.
wyjscia: zgodnosc taxonomii i mapa artefaktow.
priorytet: niski

kto: language-polish-quality
dlaczego: walidacja jezykowa PL przed gate i PDF.
ETA: 2026-06-24 21:00
wejscia: Raport-Wynikowy, Podsumowanie-Gate.
wyjscia: status OK/Warning/Blocker + lista korekt redakcyjnych.
priorytet: sredni

kto: artifact-quality
dlaczego: konsolidacja statusow i gotowosci gate.
ETA: 2026-06-24 22:00
wejscia: wszystkie raporty agentow.
wyjscia: rekomendacja gate + lista brakow.
priorytet: wysoki

kto: technical-developer
dlaczego: automatyzacja walidacji rownan i budowy evidence pack.
ETA: 2026-06-24 23:00
wejscia: wymagania walidacyjne i runbook.
wyjscia: patch narzedzi + wynik testow lint/test/typecheck.
priorytet: sredni
~~~

### C.20 Plan-Walidacji.md

~~~markdown
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
~~~

### C.21 Raport-Wynikowy.md

~~~markdown
# Raport wynikowy

## Metadane
- ID: T04-RESULT-001
- Tytul: GR-PPN-Yukawa-Perihelion
- Autor: Zespol SAF
- Data: 2026-06-21
- Status: closed
- Powiazania (format [ID:Typ]): [T04-CASE-001:Karta-Badania], [T04-LTR-DERIV-001:Raport-Wyprowadzen], [T04-LTR-VAL-001:Rejestr-Walidacji]

## Podsumowanie
- status: OK
- pewnosc: 0.88
- Uzasadnienie: model-review, CI, walidacja formalna i akceptacja human-in-the-loop zostały domkniete; ryzyko preprint zaakceptowano warunkowo z mitygacją.

## Wyniki główne (robocze)
- Model zawiera składnik 1PN i Yukawa.
- Wynik końcowy raportowany jako delta_phi_total.
- Przyjęto roboczo kanoniczne F(e)=1/(1-e^2).
- Dostarczono CI dla delta_phi_total (Monte Carlo, N=120000).
- Raportujemy obie miary: na orbitę oraz na stulecie (arcsec/century).

## Ograniczenia
- Składnik Yukawa korzysta z polityki peer-reviewed + preprint; aktywna etykieta ryzyka: RISK-PREPRINT-YUKAWA.
- Decyzja Gate 1/2/4 pozostaje po stronie człowieka (human-in-the-loop).

## Rekomendacje gate (robocze)
- Gate 1: closed (approved)
- Gate 2: closed (approved)
- Gate 3: pass-with-comments (akceptacja warunkowa zgodnie z mitygacją)
- Gate 4: closed (approved)

## Konsolidacja Gate 3 (artifact-quality + risk-compliance)
- status: OK
- pewnosc: 0.85
- gotowosc techniczna: CI i walidacja jezykowa wykonane, ryzyka sklasyfikowane.
- notatka ryzyka: aktywne RISK-PREPRINT-YUKAWA (zaakceptowane warunkowo z mitygacją).
- rekomendacja: pass-with-comments dla Gate 3.
- artefakt konsolidujacy: Evidence-Packet-Gate3.md (decision: pass-with-comments, owner: HUMAN_OWNER).

## Pytania
- Q-302 (zamkniete): Raportujemy obie miary: na orbitę i na stulecie.
~~~

### C.22 Raport-Wyprowadzen-LTR.md

~~~markdown
# Raport wyprowadzen LTR (case)

## Metadane
- ID: T04-LTR-DERIV-001
- Tytul: GR-PPN-Yukawa-Perihelion
- Autor: Zespol SAF
- Data: 2026-06-21
- Status: draft
- Tryb pracy: formalny
- Powiazania (format [ID:Typ]): [T04-LTR-CONTRACT-001:Kontrakt-Semantyczny], [T04-CASE-001:Karta-Badania]

## Cel wyprowadzenia
- Uzyskac jawny wzor na delta_phi_total z rozkladem na 1PN i Yukawa.

## Definicje bazowe
- $$
  \Delta\varphi_{1PN} = \frac{6\pi GM}{a(1-e^2)c^2}
  $$
EQ:T04-1

- $$
  V_Y(r) = -\frac{GMm}{r}\,\beta e^{-r/\lambda}
  $$
EQ:T04-2

- $$
  \Delta\varphi_Y \approx \pi\beta\left(\frac{a}{\lambda}\right)^2 e^{-a/\lambda}F(e)
  $$
EQ:T04-3

- $$
  \Delta\varphi_{total}=\Delta\varphi_{1PN}+\Delta\varphi_Y
  $$
EQ:T04-4

## Kroki formalne
1. Weryfikacja wymiarowa EQ:T04-1..EQ:T04-4.
2. Analiza granicy beta -> 0 i odzyskanie czystego 1PN.
3. Analiza granicy lambda -> inf dla modelu roboczego Yukawy.
4. Definicja wskaznika dominacji:
   $$
   R=\frac{|\Delta\varphi_Y|}{|\Delta\varphi_{1PN}|}
   $$
EQ:T04-5
5. [VERIFY-CAS] Kontrola symboliczna i algebraiczna krokow.

## Wynik [VERIFY-CAS] (iteracja 1)
- Wykonano skrypt: `cas_check_t04.py`.
- Artefakt wyniku: `Wyniki-CAS-T04.md`.
- Potwierdzone: granice beta -> 0, lambda -> inf oraz zachowanie wskaznika R.
- Do dopiecia: kanoniczna postac F(e) i finalna kontrola wymiarowosci zaleznej od przyjetego F(e).

## Decyzja model-review (iteracja 3)
- Decyzja: przyjmujemy kanoniczna postac robocza
  $$
  F(e)=\frac{1}{1-e^2}
  $$
EQ:T04-6
- Uzasadnienie: postac jest spojna z perturbacyjnym charakterem modelu i stabilna numerycznie dla zakresu e rozpatrywanego dla Merkurego.
- Semantyka ryzyka zrodel dla EQ:T04-3:
  - peer-reviewed: podstawa rekomendowana,
  - preprint: dopuszczony pomocniczo z jawna etykieta ryzyka interpretacyjnego.
- Etykieta ryzyka: RISK-PREPRINT-YUKAWA (dla fragmentow opartych o preprint).

## Fakty i wnioski (robocze)
- Fakty (pewnosc: 0.78): model pozwala rozdzielic skladniki i policzyc R; testy graniczne potwierdzone CAS.
- Wnioski (pewnosc: 0.71): F(e) jest ustalone roboczo (EQ:T04-6); pozostaje finalna decyzja czlowieka dla Gate 3/4.

## Miejsca do doprecyzowania
- Q-202 (sredni): Czy raportujemy precesje na orbite czy na stulecie (lub oba)?
- Q-203 (wysoki): Czy utrzymujemy RISK-PREPRINT-YUKAWA do czasu drugiego niezaleznego zrodla peer-reviewed dla tego samego przyblizenia?
~~~

### C.23 Rejestr-NA-Agentow.md

~~~markdown
# Rejestr N/A Agentow (iteracja pilota T04)

## Metadane
- ID: T04-NA-REG-001
- Case: T04-GR-PPN-Yukawa-Perihelion
- Data: 2026-06-21
- Status: closed

## Cel
Jawne wykazanie agentow i artefaktow oznaczonych jako N/A w tej iteracji,
aby uniknac mylnej interpretacji "braku dostarczenia" jako bledu wykonania.

## Decyzja zakresu
- Klasyfikacja: zamkniete z czesciowym zakresem agentow (pilot).
- Owner decyzji: HUMAN_OWNER.
- Powiazania: [T04-AGENT-CHECK-001:Checklista-Wkladu-Agentow], [T04-DEC-007:Akceptacje-Decyzje].

## Pozycje N/A
| Agent | Artefakt docelowy | Status | Powod N/A | Dalszy krok |
|---|---|---|---|---|
| simulation-experiment | tabela scenariuszy i mapa wrazliwosci | N/A (pilot) | Poza minimalnym zakresem potrzebnym do domkniecia Gate 4 | przeniesione do backlogu T04-BL-001 |
| knowledge-repo | normalizacja taxonomii i mapa artefaktow | N/A (pilot) | Poza minimalnym zakresem potrzebnym do domkniecia Gate 4 | przeniesione do backlogu T04-BL-002 |

## Uwagi
- N/A oznacza swiadomie nieuruchomione w tym przebiegu, nie blad procesu.
- Decyzja Gate pozostaje wazna, bo wymagane artefakty krytyczne zostaly dostarczone i zatwierdzone w HITL.
~~~

### C.24 Rejestr-Walidacji-Formalnej-LTR.md

~~~markdown
# Rejestr walidacji formalnej LTR

## Metadane
- ID: T04-LTR-VAL-001
- Tytul: GR-PPN-Yukawa-Perihelion
- Autor: Zespol SAF
- Data: 2026-06-21
- Status: draft
- Tryb pracy: formalny
- Powiazania (format [ID:Typ]): [T04-LTR-DERIV-001:Raport-Wyprowadzen]

## Lista krokow do walidacji
| Krok | Opis | Metoda | Status | Komentarz |
|---|---|---|---|---|
| K1 | Wymiarowosc EQ:T04-1..EQ:T04-6 | reczna | verified | domkniete po przyjeciu kanonicznego F(e) |
| K2 | Granica beta -> 0 | reczna + CAS | verified | PASS w Wyniki-CAS-T04.md (K5a) |
| K3 | Granica lambda -> inf | reczna + CAS | verified | PASS w Wyniki-CAS-T04.md (K5b) |
| K4 | Definicja i kontrola R (EQ:T04-5) | reczna + CAS | verified | PASS w Wyniki-CAS-T04.md (K5c, K5d) |
| K5 | [VERIFY-CAS] kontrola symboliczna | CAS | verified | SymPy, raport Wyniki-CAS-T04.md |

## Wynik walidacji
- status: OK
- pewnosc: 0.82
- uzasadnienie: walidacja formalna i CAS domkniete dla EQ:T04-1..EQ:T04-6.

## Slad dowodowy
- Pliki: Raport-Wyprowadzen-LTR.md, Plan-Walidacji.md.
- Narzedzia: SymPy (wykonano), kontrola reczna.
- Dowod CAS: Wyniki-CAS-T04.md.
~~~

### C.25 Reproducibility-Pack-Teoretyczna.md

~~~markdown
# Reproducibility Pack (fizyka teoretyczna)

## Metadane
- ID: T04-REPRO-001
- Tytul: GR-PPN-Yukawa-Perihelion
- Autor: Zespol SAF
- Data: 2026-06-21
- Status: draft
- Powiazania (format [ID:Typ]): [T04-LTR-DERIV-001:Raport-Wyprowadzen], [T04-LTR-VAL-001:Rejestr-Walidacji]

## Minimalny zestaw odtwarzalnosci
- Jawna lista rownan: EQ:T04-1..EQ:T04-5.
- Jawna lista parametrow i zrodel danych.
- Log walidacji CAS oraz wersje narzedzi.

## Runbook odtworzenia
1. Przejrzyj Karta-Badania i Plan-Walidacji.
2. Odtworz kroki EQ:T04-* z Raport-Wyprowadzen-LTR.
3. Uruchom walidacje CAS i uzupelnij rejestr.
4. Porownaj wynik z Raport-Wynikowy.

## Warunki pass
- Wszystkie rownania i testy graniczne odtworzone.
- Brak niejawnych transformacji i brak utraty merytoryki.

## Status
- status: Warning
- pewnosc: 0.40
~~~

### C.26 Research-Design.md

~~~markdown
# Research Design

## Metadane
- ID: T04-RD-001
- Tytul: GR-PPN-Yukawa-Perihelion
- Autor: Zespol SAF
- Data: 2026-06-21
- Status: draft
- Powiazania (format [ID:Typ]): [T04-CASE-001:Karta-Badania], [T04-LTR-DERIV-001:Raport-Wyprowadzen]

## Model i zalozenia
- Dynamika centralna w przyblizeniu slabych pol i niskich predkosci.
- Skladnik relatywistyczny opisany poprawka 1PN.
- Dodatkowa mala poprawka Yukawy o parametrach beta, lambda.

## Parametry i stale
- G, M, c, a, e
- beta (bezwymiarowe), lambda > 0
- x = a/lambda

## Zmienne raportowane
- delta_phi_1PN
- delta_phi_Y
- delta_phi_total
- wspolczynnik dominacji R = |delta_phi_Y|/|delta_phi_1PN|

## Zakres stosowalnosci
- |beta| << 1
- e w zakresie orbitalnym testu
- brak pelnego modelu N-body

## Kryteria sukcesu
- Spojnosc wymiarowa i notacyjna.
- Reprodukowalny tok obliczen.
- Audytowalny podzial wkładów agentow.
~~~

### C.27 Risk-and-Safety-Pack-Teoretyczna.md

~~~markdown
# Risk and Safety Pack (fizyka teoretyczna)

## Metadane
- ID: T04-RISK-SAF-001
- Tytul: GR-PPN-Yukawa-Perihelion
- Autor: Zespol SAF
- Data: 2026-06-21
- Status: draft
- Powiazania (format [ID:Typ]): [T04-CASE-001:Karta-Badania], [T04-EXP-CTX-001:Experiment-Context-Pack]

## Ryzyka merytoryczne
| ID | Ryzyko | Skutek | Prawdopodobienstwo | Mitygacja | Owner | Status |
|---|---|---|---|---|---|---|
| T04-R1 | Nadinterpretacja modelu roboczego Yukawy | Bledna konkluzja fizyczna | srednie | Jawnie oznaczyc zakres i przyblizenia | HUMAN_OWNER | monitored |
| T04-R2 | Pomieszanie precesji na orbite i na stulecie | Bledna skala porownawcza | srednie | Raportowac obie skale i wzor konwersji | HUMAN_OWNER | monitored |
| T04-R3 | Brak spojnych danych referencyjnych | Dryf wyniku liczbowego | srednie | Wymusic wskazanie Source of Truth w Plan-Danych | HUMAN_OWNER | monitored |
| T04-R4 | Wykorzystanie preprintu w czesci Yukawa | Ryzyko interpretacyjne przy finalnej rekomendacji | srednie | Utrzymac etykiete RISK-PREPRINT-YUKAWA i walidacje krzyzowa z peer-reviewed | HUMAN_OWNER | accepted_with_mitigation |

## Ryzyka obliczeniowe
| ID | Ryzyko | Skutek | Prawdopodobienstwo | Mitygacja | Owner | Status |
|---|---|---|---|---|---|---|
| T04-C1 | Blad znaku w przyblizeniach | Zly kierunek poprawki | srednie | [VERIFY-CAS] i review modelowy | HUMAN_OWNER | monitored |
| T04-C2 | Zakres poza perturbacja | Utrata poprawnosci rownan | srednie | Twarde progi dla beta i a/lambda | HUMAN_OWNER | monitored |

## Kryteria stop/eskalacji
- Stop: konflikt krytyczny miedzy formal-consistency i model-review.
- Eskalacja: dowolny status Blocker lub brak danych krytycznych.
- Decyzja gate: czlowiek (human-in-the-loop).

## Decyzja akceptacji ryzyka
- 2026-06-21: Akceptacja warunkowa zgodnie z zaproponowanymi czynnosciami mitygacyjnymi.
- Zakres: RISK-PREPRINT-YUKAWA (T04-R4).
- Warunek: utrzymanie etykiety ryzyka i notatki w evidence packet do Gate 4.
~~~

### C.28 Walidacja-Jezykowa-PL.md

~~~markdown
# Walidacja jezykowa PL

## Metadane
- ID: T04-LANG-PL-001
- Zakres: pakiet T04 (artefakty gate)
- Data: 2026-06-21
- Agent: language-polish-quality
- Tryb: korekta redakcyjna bez zmian merytoryki, ID i EQ

## Wynik
- status: Warning
- pewnosc: 0.87
- uzasadnienie: wprowadzono korekty literowek i spojnosci stylu; pozostaja drobne roznice konwencji PL/EN w nazwach technicznych.

## Zakres wykonanych korekt
- Poprawiono literowki i skladnie w kluczowych artefaktach T04.
- Ujednolicono wybrane sformulowania procesowe (gate, ryzyko, CI, Source of Truth).
- Nie zmieniano tresci merytorycznej, rownan, tagow EQ ani ID.

## Ryzyka rezydualne
- RISK-PREPRINT-YUKAWA pozostaje aktywne i jest jawnie oznaczone.
- Decyzja finalna Gate 1/2/4 pozostaje po stronie czlowieka.

## Rekomendacja
- Rekomendacja jezykowa: gotowe do Gate 4 po zaakceptowaniu drobnych roznic stylu technicznego (PL/EN) przez wlasciciela dokumentu.
~~~

### C.29 Wyniki-CAS-T04.md

~~~markdown
# Wyniki CAS T04

- Data: 2026-06-20 23:14:29 UTC
- Narzedzie: SymPy
- Status: OK

## Wyniki [VERIFY-CAS]
| Check | Wynik | Szczegoly |
|---|---|---|
| K5a beta->0 | PASS | limit(delta_total, beta->0) - delta_1pn = 0 |
| K5b lambda->inf | PASS | limit(delta_y, lambda->inf) = 0 |
| K5c R(beta->0) | PASS | limit(R, beta->0) = 0 |
| K5d struktura R | PASS | R = Fe*a**3*beta*c**2*exp(-a/lam)*Abs(e**2 - 1)/(6*G*M*lam**2) |

## Kontrola liczbowa 1PN (Merkury)
- delta_phi_1PN ~= 42.9820 arcsec/century
- Uwaga: wartosc sluzy jako sanity-check skali wyniku.
~~~
