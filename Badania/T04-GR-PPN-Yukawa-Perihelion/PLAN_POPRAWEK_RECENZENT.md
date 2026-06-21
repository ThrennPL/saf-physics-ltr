# PLAN POPRAWEK MERYTORYCZNYCH PRZED PUBLIKACJĄ

## Publikacja T04 – GR-PPN-Yukawa-Perihelion

### Status

Wynik niezależnej recenzji merytorycznej: **Major Revision**

### Cel dokumentu

Dokument identyfikuje elementy wymagające poprawy przed uznaniem pracy za publikację naukową spełniającą standardy recenzowanych czasopism z zakresu:

* ogólnej teorii względności,
* mechaniki nieba,
* testów alternatywnych teorii grawitacji,
* ograniczeń modeli typu Yukawa (fifth force).

---

# 1. POPRAWKI KRYTYCZNE (BLOCKER)

## 1.1. Pełne wyprowadzenie składnika Yukawy

### Problem

W publikacji wykorzystano przybliżenie:

[
\Delta\phi_Y \approx \pi\beta\left(\frac{a}{\lambda}\right)^2 e^{-a/\lambda}F(e)
]

bez pełnego wyprowadzenia.

Obecnie wzór został przyjęty jako model roboczy.

### Wymagane działania

Należy dodać osobny rozdział:

## Wyprowadzenie precesji Yukawy

obejmujący:

1. potencjał

[
V(r)=-\frac{GMm}{r}\left(1+\beta e^{-r/\lambda}\right)
]

2. równanie ruchu,

3. przejście do równania Bineta,

4. rozwinięcie perturbacyjne dla:

[
|\beta| \ll 1
]

5. wyprowadzenie przesunięcia peryhelium,

6. wskazanie wszystkich przybliżeń.

### Oczekiwany rezultat

Recenzent musi móc prześledzić cały tok rachunku bez odwoływania się do niejawnych założeń.

---

## 1.2. Uzasadnienie funkcji F(e)

### Problem

Przyjęto:

[
F(e)=\frac{1}{1-e^2}
]

bez dowodu.

### Wymagane działania

Należy wykazać:

* skąd pochodzi funkcja,
* czy wynika bezpośrednio z wyprowadzenia,
* czy jest przybliżeniem,
* jaki jest zakres jej stosowalności.

### Oczekiwany rezultat

F(e) nie może być w publikacji określona jako „kanoniczna roboczo”.

Musi być:

* wyprowadzona,
* albo jednoznacznie zacytowana z literatury.

---

## 1.3. Usunięcie niespójności definicji wskaźnika R

### Problem

W publikacji:

[
R=\frac{|\Delta\phi_{1PN}|}{|\Delta\phi_Y|}
]

natomiast implementacja CAS wykorzystuje:

[
R=\frac{|\Delta\phi_Y|}{|\Delta\phi_{1PN}|}
]

Powoduje to sprzeczne granice dla:

[
\beta \to 0
]

### Wymagane działania

Wybrać jedną definicję.

Rekomendacja:

[
R_Y=
\frac{|\Delta\phi_Y|}
{|\Delta\phi_{1PN}|}
]

Interpretacja:

* RY << 1 → dominacja GR,
* RY ~ 1 → porównywalny wkład,
* RY > 1 → dominacja Yukawy.

### Oczekiwany rezultat

Definicja, tekst i kod CAS muszą być identyczne.

---

# 2. POPRAWKI WYSOKIEGO PRIORYTETU

## 2.1. Rozszerzenie walidacji CAS

### Problem

CAS weryfikuje wyłącznie:

* granicę β→0,
* granicę λ→∞,
* spójność algebraiczną.

Nie weryfikuje poprawności fizycznej modelu.

### Wymagane działania

Dodać testy:

* limit e→0 (orbita kołowa),
* limit a/λ→0,
* limit a/λ→∞,
* porównanie z rozwiązaniem numerycznym równania ruchu.

### Oczekiwany rezultat

Walidacja fizyczna zamiast wyłącznie algebraicznej.

---

## 2.2. Uzasadnienie zakresów parametrów β i λ

### Problem

Zakresy Monte Carlo zostały przyjęte arbitralnie.

### Wymagane działania

Dla każdego zakresu wskazać:

* źródło,
* ograniczenie eksperymentalne,
* publikację referencyjną.

Przykładowe źródła:

* Sun et al. (2019),
* Kapner et al. (2007),
* współczesne analizy efemeryd planetarnych.

### Oczekiwany rezultat

Czytelnik powinien wiedzieć, dlaczego badany jest właśnie taki zakres parametrów.

---

## 2.3. Analiza czułości

Dodać mapę:

[
(\beta,\lambda)\rightarrow \Delta\phi_Y
]

oraz wykresy:

* poziomice precesji,
* granice dominacji,
* obszary wykluczone.

---

# 3. NOWE ELEMENTY WYMAGANE W WERSJI PUBLIKACYJNEJ

## 3.1. Porównanie z obserwacjami

Obecna wersja jest jedynie benchmarkiem teoretycznym.

Należy dodać:

### Dane obserwacyjne

Precesja Merkurego:

[
42.98''/century
]

oraz niepewność obserwacyjną.

### Test zgodności

Porównać:

[
\Delta\phi_{obs}
]

z

[
\Delta\phi_{1PN}+\Delta\phi_Y
]

### Wynik

Wyznaczyć:

* dopuszczalne β,
* dopuszczalne λ,
* regiony wykluczone.

---

## 3.2. Ograniczenia na piątą siłę

Dodać rozdział:

## Constraints on Yukawa-type Fifth Forces

z porównaniem do:

* Solar System tests,
* Lunar Laser Ranging,
* perihelion precession,
* laboratory inverse-square-law tests.

---

## 3.3. Wykresy

Minimalny zestaw:

### Wykres 1

Precesja vs λ

dla kilku wartości β.

### Wykres 2

Mapa konturowa

[
(\beta,\lambda)
]

### Wykres 3

Porównanie:

* 1PN,
* Yukawa,
* suma.

---

# 4. POPRAWKI REDAKCYJNE

## 4.1. Rozdzielenie walidacji procesu od walidacji fizycznej

Aktualna publikacja zawiera dużo informacji o:

* gate,
* workflow,
* auditability,
* artefaktach.

W czasopiśmie naukowym powinny znaleźć się głównie:

* teoria,
* wyprowadzenia,
* wyniki,
* ograniczenia.

Artefakty procesu należy przenieść do suplementu.

---

## 4.2. Rozbudowa części matematycznej

Dodać:

* równania pośrednie,
* definicje wszystkich symboli,
* zakresy przybliżeń.

---

## 4.3. Rozszerzenie bibliografii

Dodać pozycje dotyczące:

* perihelion precession in modified gravity,
* Yukawa potentials in celestial mechanics,
* fifth-force constraints,
* PPN formalism.

---

# REKOMENDOWANA STRUKTURA WERSJI PUBLIKACYJNEJ

1. Wstęp
2. Potencjał Newtonowski i Yukawy
3. Wyprowadzenie z równania Bineta
4. Precesja 1PN
5. Precesja Yukawy
6. Granice i testy analityczne
7. Monte Carlo
8. Analiza czułości
9. Porównanie z obserwacjami
10. Ograniczenia na parametry β i λ
11. Dyskusja
12. Wnioski

---

# OCENA GOTOWOŚCI

## Obecny stan

Formalna gotowość: 90%

Gotowość publikacyjna: 60%

Gotowość naukowa: 65%

---

## Po wdrożeniu poprawek

Formalna gotowość: 95%

Gotowość publikacyjna: 90%

Gotowość naukowa: 90–95%

---

# Najważniejsze zadanie

Jeżeli można wykonać tylko jedną poprawkę, należy wykonać:

**Pełne wyprowadzenie składnika Yukawy z równania Bineta wraz z uzasadnieniem postaci F(e).**

Jest to główny element decydujący o akceptowalności pracy przez recenzenta naukowego.
