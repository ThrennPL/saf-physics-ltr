# Aneks mapowania orbitalnego

## Metadane
- ID: T03-ANNEX-ORB-001
- Tytuł: Mapowanie warunku stabilności na orbity planetarne
- Autor: Zespół SAF
- Data: 2026-05-30
- Status: final
- Powiązania (format [ID:Typ]): [T03-RESULT-001:Raport-Wynikowy], [T03-LTR-DERIV-001:Raport-Wyprowadzen]

## Definicje
- Warunek stabilności lokalnej: $1+\beta c(x)>0$.
- $x=r_c/\lambda$.
- $c(x)=e^{-x}(1+x-x^2)$.

## Metoda mapowania
- Przyjęto półosie wielkie orbit planetarnych jako przybliżenie r_c w AU.
- Sprawdzono trzy scenariusze zasięgu poprawki: $\lambda=0.5, 1.0, 5.0$ AU.
- Dla każdego przypadku wyznaczono znak c(x) i granice na beta wynikające z samej stabilności.

## Tabela porównawcza (wycinek)
| Obiekt | lambda [AU] | x=r_c/lambda | c(x) | Wniosek ze stabilności |
|---|---:|---:|---:|---|
| Merkury | 0.5 | 0.774 | 0.54183 | beta > -1.8456 |
| Merkury | 1.0 | 0.387 | 0.84019 | beta > -1.1902 |
| Ziemia | 0.5 | 2.000 | -0.13534 | beta < 7.3891 |
| Ziemia | 1.0 | 1.000 | 0.36788 | beta > -2.7183 |
| Mars | 0.5 | 3.048 | -0.24877 | beta < 4.0198 |
| Jowisz | 1.0 | 5.203 | -0.11478 | beta < 8.7126 |
| Jowisz | 5.0 | 1.041 | 0.33832 | beta > -2.9558 |

## Interpretacja
- Znak czynnika $1+x-x^2$ zmienia się przy $x=(1+\sqrt{5})/2\approx1.618$.
- Dla $x<1.618$ dodatni beta zwykle wspiera stabilność lokalną.
- Dla $x>1.618$ ten efekt może się odwracać (zależnie od znaku c(x)).
- Same nierówności stabilności są zwykle słabsze niż perturbacyjne ograniczenie robocze $|\beta e^{-x}|<0.1$.

## Status i pewność
- status: OK
- pewność: 0.84

## Ograniczenia
- Brak inferencji statystycznej i dopasowania do danych efemeryd.
- Użyto uproszczenia r_c ~ półoś wielka.





