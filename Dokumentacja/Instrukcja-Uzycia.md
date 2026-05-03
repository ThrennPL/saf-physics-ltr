# Instrukcja uzycia konfiguracji (PL/EN)

## 1. Cel i dla kogo (PL)
Ten dokument opisuje, jak uruchomic i prowadzic badanie w konfiguracji SAF/LTR dla nowego uzytkownika.

## 1. Purpose and audience (EN)
This document explains how to start and run a study using the SAF/LTR setup for a new user.

## 2. Minimalny start (MVP) (PL)
1) Utworz nowy folder badawczy (case).
2) Wypelnij Karta-Badania (Dokumentacja/Karta-Badania.md).
3) Przygotuj Experiment Context Pack (teoretyczna) z hipoteza, zalozeniami i zakresem.
4) Utworz Orkiestrator Log (minimalny wpis startowy).
5) Ustal standard raportowania: status OK/Warning/Blocker, pewnosc 0-1, pytania Q-XXX z priorytetem.
6) Przejdz Gate 1 (human-in-the-loop).

## 2. Minimal start (MVP) (EN)
1) Create a new research case folder.
2) Fill Karta-Badania (Dokumentacja/Karta-Badania.md).
3) Prepare Experiment Context Pack (theoretical) with hypothesis, assumptions, and scope.
4) Create Orchestrator Log (minimal start entry).
5) Set reporting standard: status OK/Warning/Blocker, confidence 0-1, Q-XXX questions with priority.
6) Complete Gate 1 (human-in-the-loop).

## 3. Pelny przebieg (PL)
1) Dodaj pakiety: Measurement Integrity, Risk and Safety, Reproducibility.
2) Uzupelnij Rejestr Konfiguracji Projektu (Dokumentacja/Rejestr-Konfiguracji-Projektu.md).
3) Utworz Raport-Wyprowadzen-LTR i Rejestr Walidacji Formalnej LTR.
4) Uzupelnij Cross-Reference Log; jesli uzywasz ADS, ustaw ADS_API_TOKEN w .env.
5) Prowadz Rejestr Konfliktow i Eskalacji (Dokumentacja/Rejestr-Konfliktow-i-Eskalacji.md).
6) Prowadz Konsolidacja-Statusow (Dokumentacja/Konsolidacja-Statusow.md).
7) Przejdz Gate 2 i Gate 3 z akceptacjami czlowieka.
8) Utworz Raport Wynikowy, Review-Jakosci-Gate3 (Dokumentacja/Review-Jakosci-Gate3.md) i Checkliste Gate 4.
9) Utworz Podsumowanie-Gate (Dokumentacja/Podsumowanie-Gate.md).
10) Przejdz Gate 4 (human-in-the-loop).

## 3. Full flow (EN)
1) Add packs: Measurement Integrity, Risk and Safety, Reproducibility.
2) Fill Project Configuration Register (Dokumentacja/Rejestr-Konfiguracji-Projektu.md).
3) Create Raport-Wyprowadzen-LTR and Formal Validation Register.
4) Fill Cross-Reference Log; if using ADS, set ADS_API_TOKEN in .env.
5) Maintain Conflict and Escalation Register (Dokumentacja/Rejestr-Konfliktow-i-Eskalacji.md).
6) Maintain Status Consolidation (Dokumentacja/Konsolidacja-Statusow.md).
7) Complete Gate 2 and Gate 3 with human approvals.
8) Create Final Results Report, Review-Jakosci-Gate3 (Dokumentacja/Review-Jakosci-Gate3.md) and Gate 4 Checklist.
9) Create Gate Summary (Dokumentacja/Podsumowanie-Gate.md).
10) Complete Gate 4 (human-in-the-loop).

## 4. Rola orkiestratora (PL)
- Ustala scope i priorytety.
- Dzieli prace na strumienie (discovery/model/walidacja/raport).
- Zleca zadania agentom i zbiera zwrotki.
- Prowadzi Orkiestrator Log i Plan Strumieni.
- Wnioskuje o decyzje gate (nie zatwierdza).

## 4. Orchestrator role (EN)
- Defines scope and priorities.
- Splits work into streams (discovery/model/validation/report).
- Delegates tasks to agents and collects responses.
- Maintains Orchestrator Log and Stream Plan.
- Recommends gate decisions (does not approve).

## 5. Zasady gate (PL)
- Gate 1/2/4: zawsze zatwierdzane przez czlowieka.
- Gate 3: mozliwy pass-with-comments, ale bez autoryzacji automatycznej.

## 5. Gate rules (EN)
- Gate 1/2/4: always require human approval.
- Gate 3: pass-with-comments allowed, no automatic approval.

## 6. Format identyfikatorow (PL)
- Prefiks case: T01, T02, ...
- Przykladowe ID: T01-CASE-001, T01-LTR-DERIV-001, T01-REPRO-001.
- Powiazania zapisuj w formacie [ID:Typ].

## 6. Identifier format (EN)
- Case prefix: T01, T02, ...
- Example IDs: T01-CASE-001, T01-LTR-DERIV-001, T01-REPRO-001.
- References use format [ID:Typ].

## 7. Minimalny zestaw artefaktow (PL)
- Karta-Badania (Dokumentacja/Karta-Badania.md)
- Experiment Context Pack (teoretyczna)
- Orkiestrator Log
- Plan Strumieni

## 7. Minimal artifact set (EN)
- Karta-Badania (Dokumentacja/Karta-Badania.md)
- Experiment Context Pack (theoretical)
- Orchestrator Log
- Stream Plan

## 8. Pelny zestaw artefaktow (PL)
- Measurement Integrity Pack
- Risk and Safety Pack
- Reproducibility Pack
- Rejestr-Konfiguracji-Projektu (Dokumentacja/Rejestr-Konfiguracji-Projektu.md)
- Raport-Wyprowadzen-LTR
- Rejestr Walidacji Formalnej LTR
- Cross-Reference Log
- Rejestr-Konfliktow-i-Eskalacji (Dokumentacja/Rejestr-Konfliktow-i-Eskalacji.md)
- Konsolidacja-Statusow (Dokumentacja/Konsolidacja-Statusow.md)
- Raport Wynikowy
- Checklista Gate 3
- Review-Jakosci-Gate3 (Dokumentacja/Review-Jakosci-Gate3.md)
- Checklista Gate 4
- Podsumowanie-Gate (Dokumentacja/Podsumowanie-Gate.md)
- Akceptacje/Decyzje

## 8. Full artifact set (EN)
- Measurement Integrity Pack
- Risk and Safety Pack
- Reproducibility Pack
- Project Configuration Register (Dokumentacja/Rejestr-Konfiguracji-Projektu.md)
- Raport-Wyprowadzen-LTR
- Formal Validation Register
- Cross-Reference Log
- Conflict and Escalation Register (Dokumentacja/Rejestr-Konfliktow-i-Eskalacji.md)
- Status Consolidation (Dokumentacja/Konsolidacja-Statusow.md)
- Final Results Report
- Gate 3 Checklist
- Review-Jakosci-Gate3 (Dokumentacja/Review-Jakosci-Gate3.md)
- Gate 4 Checklist
- Gate Summary (Dokumentacja/Podsumowanie-Gate.md)
- Approvals/Decisions
