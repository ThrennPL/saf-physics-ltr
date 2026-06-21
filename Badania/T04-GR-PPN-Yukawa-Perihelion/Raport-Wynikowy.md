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
- Wykonano niezalezna walidacje ODE/Binet (artefakty: T04-NUM-VAL-001.md, T04-NUM-VAL-DATA.csv, wykresy t04-binet-*).

## Ograniczenia
- Składnik Yukawa korzysta z polityki peer-reviewed + preprint; aktywna etykieta ryzyka: RISK-PREPRINT-YUKAWA.
- Decyzja Gate 1/2/4 pozostaje po stronie człowieka (human-in-the-loop).
- Walidacja ODE/Binet ma status PARTIAL dla kryterium epsilon < 5% w scenariuszach fizycznych; potrzebna poprawa czulosci solvera.

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
