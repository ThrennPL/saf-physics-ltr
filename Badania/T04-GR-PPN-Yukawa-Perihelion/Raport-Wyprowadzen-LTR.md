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
- Uzupelnienie: jawny ciag potencjal->sila->Binet->perturbacja udokumentowano w `T04-BLOCKER-001-WYPROWADZENIE-YUKAWA-BINET.md`.
- Uzupelnienie: niezalezna walidacja numeryczna ODE/Binet udokumentowana w `T04-NUM-VAL-001.md` i `T04-NUM-VAL-DATA.csv`.
- Do dopiecia: finalne domkniecie pochodzenia F(e) (dowod lub mocniejsze umocowanie literaturowe peer-reviewed) oraz poprawa rozdzielczosci solvera dla fizycznie malych beta.

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
- Fakty (pewnosc: 0.83): model pozwala rozdzielic skladniki i policzyc R; testy graniczne potwierdzone CAS, a walidacja ODE zostala wykonana.
- Wnioski (pewnosc: 0.76): F(e) pozostaje postacia robocza (EQ:T04-6), lecz uzyskano dodatkowe wsparcie z walidacji numerycznej w rezimie kalibracyjnym.

## Miejsca do doprecyzowania
- Q-202 (zamkniete): Raportujemy precesje w obu miarach (na orbite i na stulecie).
- Q-203 (wysoki): Czy utrzymujemy RISK-PREPRINT-YUKAWA do czasu drugiego niezaleznego zrodla peer-reviewed dla tego samego przyblizenia?
- Q-704 (wysoki): Czy akceptujemy domkniecie 1.2 na podstawie walidacji ODE + literatury, czy wymagamy pelnego dowodu analitycznego F(e) przed wysylka?
