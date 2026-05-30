---
description: 'Konfigurator projektu badawczego (prompt)'
---

# Konfigurator projektu badawczego (prompt)

Cel: konfiguracja projektu i artefaktow LTR.

Zapytaj o:
- Nazwe projektu
- Case (A/B/C lub nowy)
- Artefakty do wygenerowania
- Powiazane ID
- Czy dolaczyc pakiety teoretyczne (Experiment/Measurement/Risk/Reproducibility)?
- Czy ADS_API_TOKEN jest skonfigurowany w .env (jesli planowany ADS)
- Zakres modelu i domeny (np. skale energii, rezimy asymptotyczne)
- Klasa obiektow matematycznych i ich regularnosc
- Rezymy przyblizen i dozwolone uproszczenia
- Zakres notacji lokalnej vs formalnej
- Krytyczne sekcje / rownania rdzeniowe (lista ID lub sekcji)
- Tolerancje notacyjne i wyjatki
- Zaleznosci od zalozen krytycznych (z Experiment Context Pack)
- Standard raportowania (status OK/Warning/Blocker, pewnosc 0-1, pytania Q-XXX z priorytetem)
- Zaleznosci i kolejnosc agentow (Formal -> Model, Data Quality -> Statistics, Discovery -> Cross-Reference)
- Wlasciciele gate i tryb akceptacji (human-in-the-loop)
- Polityka danych i wymagania regulatora/finansujacego
- Konfiguracja narzedzi (OCR/Graphviz/ADS)

Wyjscie: lista plikow do utworzenia i powiazan.
Zapisz w: Dokumentacja/Rejestr-Konfiguracji-Projektu.md

