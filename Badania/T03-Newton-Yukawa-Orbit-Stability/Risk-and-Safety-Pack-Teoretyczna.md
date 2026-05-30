# Risk and Safety Pack (fizyka teoretyczna)

## Metadane
- ID: T03-RISK-SAF-001
- Tytuł: Newton-Yukawa-Orbit-Stability
- Autor: Zespół SAF
- Data: 2026-05-30
- Status: draft
- Powiązania (format [ID:Typ]): [T03-CASE-001:Karta-Badania], [T03-EXP-CTX-001:Experiment-Context-Pack]

## Ryzyka merytoryczne
| ID | Ryzyko | Skutek | Prawdopodobieństwo | Mitygacja | Owner | Status |
|---|---|---|---|---|---|---|
| T03-R1 | Nadinterpretacja stabilności lokalnej jako globalnej | Błędna konkluzja fizyczna | Średnie | Jawne rozdzielenie lokalna/globalna | Grzegorz Majewski | monitored |
| T03-R2 | Zbyt szeroka ekstrapolacja poza |beta| << 1 | Utrata poprawności perturbacyjnej | Średnie | Twarde progi perturbacyjne | Grzegorz Majewski | monitored |
| T03-R3 | Pomieszanie roli lambda i r_c | Błędna interpretacja warunku | Średnie | Wprowadzenie x = r_c/lambda | Grzegorz Majewski | monitored |

## Ryzyka obliczeniowe
| ID | Ryzyko | Skutek | Prawdopodobieństwo | Mitygacja | Owner | Status |
|---|---|---|---|---|---|---|
| T03-C1 | Błąd znaków przy pochodnych wykładniczych | Niepoprawny warunek stabilności | Średnie | Walidacja ręczna + [VERIFY-CAS] | Grzegorz Majewski | monitored |

## Plan danych
- Status: N/A.
- Uzasadnienie: badanie jest analityczne, bez pomiarów i akwizycji danych.

## Kryteria stop/eskalacji
- Stop: wykrycie sprzeczności formalnej w równaniach bazowych.
- Eskalacja: status Blocker w formal-consistency lub model-review.
- Owner decyzji gate: człowiek (human-in-the-loop).




