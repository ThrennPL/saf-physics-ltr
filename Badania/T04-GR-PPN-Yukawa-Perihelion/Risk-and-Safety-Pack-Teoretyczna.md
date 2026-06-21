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
