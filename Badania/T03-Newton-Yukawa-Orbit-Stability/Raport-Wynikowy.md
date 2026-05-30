# Raport wynikowy

## Metadane
- ID: T03-RESULT-001
- Tytuł: Newton-Yukawa-Orbit-Stability
- Autor: Zespół SAF
- Data: 2026-05-30
- Status: final
- Powiązania (format [ID:Typ]): [T03-CASE-001:Karta-Badania], [T03-LTR-DERIV-001:Raport-Wyprowadzen], [T03-ANNEX-ORB-001:Aneks-Mapowanie-Orbity]

## Podsumowanie
- Cel: ocena lokalnej stabilności orbit kołowych przy poprawce Yukawy.
- status: OK
- pewność: 0.88

## Wyniki główne
- Otrzymany warunek stabilności lokalnej:
  $1+\beta e^{-x}(1+x-x^2)>0$, gdzie $x=r_c/\lambda$.
- Dla beta = 0 odzyskujemy stabilność Newtonowską.
- Wpływ znaku beta zależy od znaku czynnika (1+x-x^2).

## Ograniczenia
- Brak kalibracji do danych i brak estymacji przedziałów dla beta, lambda.

## Rozszerzenie orbitalne (realizacja punktu 3)
- Wykonano mapowanie warunku stabilności na wybrane orbity planetarne (Merkury, Wenus, Ziemia, Mars, Jowisz).
- Scenariusze: lambda = 0.5 AU, 1.0 AU, 5.0 AU.
- Szczegóły i tabela porównawcza: Aneks-Mapowanie-Orbity.md.

## Rekomendacje gate (robocze)
- Gate 1: approved.
- Gate 2: approved.
- Gate 3: approved.
- Gate 4: approved.

## Miejsca do doprecyzowania
- Nie wiem: jaki poziom rygoru empirycznego jest wymagany dla tego testu (czysto formalny vs semi-empiryczny).

## Pytania do właściciela danych
- Q-003 (wysoki): Czy rozszerzyć mapowanie o ograniczenia z precesji perycentrum i dane efemeryd?
- Q-004 (średni): Czy utrzymać twardy próg |beta exp(-r/lambda)| < 0.1, czy zmienić go na 0.05?






