# Runbook Gate-Executor (operacyjny)

Cel: wykonanie gate w sposob powtarzalny, z jasnym torem pre/run/post oraz fail-path i eskalacja.

## 1. Pre-check (przed gate)
1) Potwierdz scope i gate ID (G1/G2/G3/G4).
2) Potwierdz ownera decyzji human-in-the-loop.
3) Uruchom lokalny sanity check:
   - `python tools/security_sanity_check.py`
   - `python tools/taxonomy_guard.py`
4) Zbierz artefakty decyzji do pakietu dowodow:
   - `python tools/build_evidence_packet.py --output Dokumentacja/Evidence-Packet-Gate.md --decision pending --owner "OWNER"`

## 2. Run (wykonanie gate)
1) Uzupelnij statusy agentow: OK/Warning/Blocker.
2) Zweryfikuj konflikt i eskalacje w Rejestrze Konfliktow.
3) Zweryfikuj podsumowanie statusow i pytania Q-XXX.
4) Zapisz propozycje decyzji: `pass | pass-with-comments | fail`.

## 3. Post (po decyzji)
1) Zapisz finalna decyzje i uzasadnienie w Podsumowanie-Gate.
2) Dolacz Evidence Packet do artefaktow case.
3) Dla `pass-with-comments` i `fail` dopisz plan korekcyjny z ownerem i ETA.

## 4. Fail-path
Warunki uruchomienia:
- sanity check FAIL,
- taxonomy guard FAIL,
- status Blocker bez akceptacji ownera,
- brak krytycznego artefaktu decyzji.

Kroki:
1) Oznacz gate jako `fail` lub `blocked`.
2) Zaloguj przyczyne i impact w Rejestrze Konfliktow i Eskalacji.
3) Utworz akcje naprawcze z ownerem i ETA.
4) Wroc do kroku Pre-check po usunieciu blokera.

## 5. Escalation
Kiedy eskalowac:
- konflikt merytoryczny miedzy agentami,
- brak danych do decyzji,
- rozjazd slownika (taxonomy drift) bez szybkiej naprawy.

Format wpisu eskalacyjnego:
- Kto (owner)
- Dlaczego (ryzyko decyzji)
- ETA (termin domkniecia)

## 6. Minimalne kryterium GO
- Wszystkie checki z Pre-check sa zielone,
- decyzja ma ownera human-in-the-loop,
- Evidence Packet zawiera linki i statusy artefaktow,
- brak otwartego Blocker bez planu naprawczego.
