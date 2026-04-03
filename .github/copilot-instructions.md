# Copilot instructions (SAF + LTR)

Jezyk: PL. Preferuj ASCII. Markdown-first.

## Zasady ogolne
- Czlowiek jest wlascicielem decyzji naukowych (human-in-the-loop).
- Nie zatwierdzaj gate bez czlowieka, nawet jesli wszystko wyglada dobrze.
- Oddzielaj fakty od wnioskow i oznaczaj poziom pewnosci.
- Nie zgaduj brakujacych danych; pytaj, oznaczaj jako DO_UZUPELNIENIA.

## Artefakty i formaty
- Uzywaj formatow z Dokumentacja/Szablon-LTR oraz Dokumentacja/Szablon-Fizyka.
- Powiazania zapisz w formacie [ID:Typ].
- Taguj rownania w raportach: po wzorze w osobnej linii dodaj [EQ:ID].
- Nietrywialne kroki oznaczaj [VERIFY-CAS].

## LTR
- Dla trybu formalnego wymagaj jawnych zalozen, definicji i krokow.
- Sprawdzaj spojnosc notacji z mapa notacji.
- Dla PDF: zakladaj ekstrakcje tekstu z warstwy tekstowej; OCR jest opcjonalny.

## Jakosci i gate
- Gate 1/2/4: akceptacja tylko czlowiek.
- Gate 3: mozliwy agent-conditional pass dla niskiego ryzyka i tylko przy statusie pass bez komentarzy krytycznych.
- Nie zatwierdzaj gate bez czlowieka, z wyjatkiem Gate 3 w trybie agent-conditional pass.

## Zachowanie modelu
- Nie halucynuj literatury; oznacz poziom zaufania i preprint vs peer-reviewed.
- Nie edytuj tresci merytorycznej bez zgody; proponuj zmiany.
- Jesli brak danych, dodaj sekcje "Miejsca do doprecyzowania".
