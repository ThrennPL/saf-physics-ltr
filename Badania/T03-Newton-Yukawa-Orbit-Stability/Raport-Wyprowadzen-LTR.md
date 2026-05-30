# Raport wyprowadzeń LTR (case)

## Metadane
- ID: T03-LTR-DERIV-001
- Tytuł: Newton-Yukawa-Orbit-Stability
- Autor: Zespół SAF
- Data: 2026-05-30
- Status: draft
- Tryb pracy: formalny
- Powiązany kontrakt (format [ID:Typ]): [T03-LTR-CONTRACT-001:Kontrakt-Semantyczny], [T03-CASE-001:Karta-Badania]

## Cel wyprowadzenia
- Wyznaczyć warunek lokalnej stabilności orbit kołowych dla potencjału Newton + Yukawa.

## Założenia i warunki brzegowe
- mu = GM > 0, lambda > 0, |beta| << 1.
- Zaburzenia radialne: r = r_c + delta r, |delta r|/r_c < 0.1.
- Ruch w potencjale centralnym, brak efektów post-Newtonowskich.

## Definicje
- $V(r)=-\frac{\mu}{r}\left(1+\beta e^{-r/\lambda}\right)$
EQ:T03-1
- $V_{\mathrm{eff}}(r)=V(r)+\frac{L^2}{2mr^2}$
EQ:T03-1a

## [TRYB: FORMALNY] Wyprowadzenie krokowe
1. Warunek orbity kołowej i stabilności lokalnej:
- $\frac{dV_{\mathrm{eff}}}{dr}\big|_{r=r_c}=0,\quad \frac{d^2V_{\mathrm{eff}}}{dr^2}\big|_{r=r_c}>0$
EQ:T03-2

2. Pierwsza pochodna:
- $\frac{dV_{\mathrm{eff}}}{dr}=\frac{\mu}{r^2}+\mu\beta e^{-r/\lambda}\left(\frac{1}{\lambda r}+\frac{1}{r^2}\right)-\frac{L^2}{mr^3}$
EQ:T03-3

3. Druga pochodna:
- $\frac{d^2V_{\mathrm{eff}}}{dr^2}=-\frac{2\mu}{r^3}-\mu\beta e^{-r/\lambda}\left(\frac{1}{\lambda^2 r}+\frac{2}{\lambda r^2}+\frac{2}{r^3}\right)+\frac{3L^2}{mr^4}$
EQ:T03-4

4. Z warunku orbity kołowej:
- $\frac{L^2}{mr_c^3}=\frac{\mu}{r_c^2}+\mu\beta e^{-r_c/\lambda}\left(\frac{1}{\lambda r_c}+\frac{1}{r_c^2}\right)$
EQ:T03-4a

5. Po podstawieniu do EQ:T03-4:
- $\frac{d^2V_{\mathrm{eff}}}{dr^2}\Big|_{r_c}=\frac{\mu}{r_c^3}+\mu\beta e^{-r_c/\lambda}\left(-\frac{1}{\lambda^2 r_c}+\frac{1}{\lambda r_c^2}+\frac{1}{r_c^3}\right)$
EQ:T03-5

6. Dla $x=r_c/\lambda$:
- $\frac{d^2V_{\mathrm{eff}}}{dr^2}\Big|_{r_c}=\frac{\mu}{r_c^3}\left[1+\beta e^{-x}(1+x-x^2)\right]$
EQ:T03-6

7. Kryterium stabilności:
- $1+\beta e^{-x}(1+x-x^2)>0$
EQ:T03-7

## Fakty i wnioski
- Fakty (pewność: 0.90): EQ:T03-3..EQ:T03-7 wynikają algebraicznie z definicji V i V_eff.
- Wniosek (pewność: 0.78): dla x > (1+sqrt(5))/2 czynnik (1+x-x^2) zmienia znak, co zmienia interpretację stabilizującej roli dodatniego beta.
- [VERIFY-CAS] Wykonano: niezależna kontrola symboliczna (SymPy) potwierdziła zgodność EQ:T03-3..EQ:T03-7.

## Zakres stosowalności
- Lokalna stabilność radialna, bez wniosków o stabilności globalnej i bez danych obserwacyjnych.





