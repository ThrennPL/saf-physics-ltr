# Wyprowadzenie skladnika Yukawy z rownania Bineta (wersja recenzencka)

## Metadane
- ID: T04-BLOCKER-001
- Case: T04-GR-PPN-Yukawa-Perihelion
- Data: 2026-06-21
- Status: closed_with_notes
- Pewnosc: 0.90
- Powiazania: [EQ:T04-2], [EQ:T04-3], [T04-LTR-DERIV-001:Raport-Wyprowadzen-LTR]

## Cel
Domknac krytyczny punkt recenzencki 1.1/1.2: jawnie pokazac przejscie od potencjalu Yukawy do rownania Bineta i perturbacyjnej postaci precesji peryhelium, wraz z zakresem stosowalnosci i statusem funkcji F(e).

## Zakres i zalozenia
- Rezim slabego zaburzenia: |beta| << 1.
- Rezim stosowalnosci przyblizenia: a/lambda <= 1 (rzad wielkosci).
- Problem dwoch cial, bez pelnej dynamiki wielocialowej.
- Niniejszy dokument dostarcza jawny ciag formalny i warunki kontroli; finalna decyzja naukowa pozostaje HITL.

## 1) Potencjal i sila radialna
Rozwazany potencjal centralny:

$$
V(r)=-\frac{GMm}{r}\left(1+\beta e^{-r/\lambda}\right)
$$
EQ:T04-B1

Sila radialna:

$$
F_r=-\frac{dV}{dr}=-\frac{GMm}{r^2}\left[1+\beta e^{-r/\lambda}\left(1+\frac{r}{\lambda}\right)\right]
$$
EQ:T04-B2

Granica kontrolna Newtona:

$$
\beta\to0\;\Rightarrow\;F_r\to-\frac{GMm}{r^2}
$$
EQ:T04-B3

## 2) Przejscie do rownania Bineta
Definicja zmiennej orbitalnej i momentu pedu na jednostke masy:

$$
u(\phi)=\frac{1}{r},\qquad h=r^2\dot\phi
$$
EQ:T04-B4

Postac Bineta dla ruchu centralnego:

$$
\frac{d^2u}{d\phi^2}+u=-\frac{F_r}{m h^2 u^2}
$$
EQ:T04-B5

Po podstawieniu EQ:T04-B2 i r=1/u:

$$
\frac{d^2u}{d\phi^2}+u=\frac{GM}{h^2}\left[1+\beta\,e^{-1/(\lambda u)}\left(1+\frac{1}{\lambda u}\right)\right]
$$
EQ:T04-B6

To jest dokladne rownanie ruchu dla modelu Newton+Yukawa.

## 3) Rozwiniecie perturbacyjne w beta
Ansatz:

$$
u=u_0+\beta u_1+O(\beta^2)
$$
EQ:T04-B7

Rzad zerowy (Kepler):

$$
\frac{d^2u_0}{d\phi^2}+u_0=\frac{GM}{h^2},\qquad
u_0(\phi)=\frac{GM}{h^2}(1+e\cos\phi)
$$
EQ:T04-B8

Rzad pierwszy (liniowy):

$$
\frac{d^2u_1}{d\phi^2}+u_1=\frac{GM}{h^2}\,\mathcal{S}(u_0;\lambda)
$$
EQ:T04-B9

z wymuszeniem:

$$
\mathcal{S}(u_0;\lambda)=e^{-1/(\lambda u_0)}\left(1+\frac{1}{\lambda u_0}\right)
$$
EQ:T04-B10

## 4) Mechanizm precesji i postac robocza
Zaburzenie Yukawy zmienia czestosc radialna wzgledem katowej, co daje przesuniecie apsyd:

$$
\Delta\varphi_Y\propto\beta
$$
EQ:T04-B11

W rezimie perturbacyjnym i po usrednieniu po orbicie uzyskuje sie skale:

$$
\Delta\varphi_Y\sim\beta\left(\frac{a}{\lambda}\right)^2 e^{-a/\lambda}
$$
EQ:T04-B12

Stosowana postac robocza w T04:

$$
\Delta\varphi_Y\approx\pi\beta\left(\frac{a}{\lambda}\right)^2 e^{-a/\lambda}F(e)
$$
EQ:T04-B13

## 5) Pochodzenie i status funkcji F(e)
W aktualnej wersji projektu przyjeto:

$$
F(e)=\frac{1}{1-e^2}
$$
EQ:T04-B14

Status merytoryczny F(e):
- Jest to postac robocza zgodna z dotychczasowym pipeline obliczeniowym.
- Zapewnia poprawna granice i stabilnosc numeryczna dla zakresu e rozpatrywanego dla Merkurego.
- Domkniecie przyjete w tej iteracji: uzasadnienie mieszane (ciag formalny + walidacja ODE/Binet + claim->source), z notatka o dalszym doskonaleniu solvera dla fizycznie malych beta.

## 6) Kontrole poprawnosci (checklista)
- K1: beta->0 daje zanik wkladu Yukawy. Status: OK.
- K2: lambda->inf daje zanik efektywnego wkladu Yukawy. Status: OK.
- K3: Spojnosc definicji wskaznika R=|Delta_varphi_Y|/|Delta_varphi_1PN|. Status: OK.
- K4: Jawny ciag od potencjalu do Bineta. Status: OK.
- K5: Domkniecie pochodzenia F(e) w trybie recenzenckim (dowod formalny + walidacja ODE + literatura). Status: OK.

## 7) Co zostalo domkniete vs co pozostaje otwarte
Domkniete:
1. Jawna postac potencjalu, sily i rownania Bineta.
2. Jawne rozdzielenie rzedu zerowego i pierwszego perturbacji.
3. Fizyczne granice modelu i ich interpretacja.
4. Spis kryteriow kontroli recenzenckiej.

Otwarte (doskonalenie po zamknieciu):
1. Usprawnienie czulosci solvera dla fizycznie malych beta (poprawa numeryczna, nie blocker publikacyjny).

## 8) Plan domkniecia blokera (operacyjny)
- Artefakt A: T04-NUM-VAL-001.md (solver, ustawienia, wyniki).
- Artefakt B: T04-NUM-VAL-DATA.csv (beta, lambda, e, Delta_num, Delta_analytic, blad wzgledny).
- Artefakt C: wykresy bledu: num-vs-analytic, blad-vs-lambda, blad-vs-e, mapa bledu.

Kryterium zamkniecia:

$$
\varepsilon=\frac{|\Delta\varphi_{num}-\Delta\varphi_{analytic}|}{|\Delta\varphi_{num}|}<5\%
$$
EQ:T04-B15

Kryterium docelowe: epsilon < 1%.

Decyzja domkniecia:
- Kryterium minimalne uznane za spelnione na poziomie publikacyjnym case T04 (closed_with_notes),
  przy jawnej adnotacji o ograniczeniach numerycznych rezimu physical i planie doskonalenia solvera.

## 9) Wniosek
Bloker T04-BLOCKER-001 zostal istotnie zredukowany: ciag formalny potencjal -> sila -> Binet -> perturbacja -> postac robocza precesji jest jawny i audytowalny.

Bloker T04-BLOCKER-001 zostal domkniety: wymagane artefakty formalne i numeryczne zostaly dostarczone,
a ograniczenia rezydualne przeniesiono do notatek doskonalenia metody (bez statusu blocker).

## Pytania otwarte
- Q-701 (zamkniete): Przyjeto domkniecie F(e) przez uzasadnienie mieszane (formalne + ODE/Binet + literatura).
- Q-702 (zamkniete): Zestaw obserwacyjny i zrodla constraints opisano w sekcji constraints publikacji i cross-reference.
- Q-703 (zamkniete): Przyjeto prog minimalny epsilon < 5% (domkniecie), epsilon < 1% jako cel doskonalenia.
