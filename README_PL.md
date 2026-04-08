# SAF Physics LTR


Repozytorium dla modelu Srodowiska Agentow AI dla Fizyki (SAF) w podejsciu Literate Theoretical Research (LTR).
![SAF Architecture](Dokumentacja/SAF_PL.png)

## Szybki start
1. Utworz i aktywuj srodowisko Python (`.venv`).
2. Zainstaluj zaleznosci: `pip install -r requirements.txt`.


## Struktura
- Dokumentacja/ - zalozenia i szablony
- Case-Template/ - wzorzec nowego case'a badawczego
- .github/agents/ - profile agentow (konfiguracja rol)
- .github/prompts/ - prompty pomocnicze


## Najwazniejsze pliki
- Zalozenia: Dokumentacja/Zalozenia-Srodowisko-Fizyka.md
- Rejestr decyzji: DECISIONS.md


## Zaleznosci
- Python 3.13+
- pypdf
- sympy
- bibtexparser
- networkx
- pillow
- pytesseract
- chromadb
- crossrefapi
- graphviz


## OCR
OCR wymaga zewnetrznego narzedzia (np. Tesseract). `pytesseract` jest tylko wrapperem.


## Indeks semantyczny
Uzywamy `chromadb` jako lekkiego indeksu lokalnego.


## Cytowania i DOI
Metadane DOI przez `crossrefapi`.


## Graf zaleznosci
`graphviz` wymaga instalacji narzedzia systemowego Graphviz.


## LTR lint
Prosta walidacja tagow LTR:


```bash
python tools/lint_ltr.py
```


Zakoncz z bledem, gdy sa ostrzezenia:


```bash
python tools/lint_ltr.py --fail-on-warning
```


## ArXiv (Cross-Reference)
Proste wyszukiwanie ArXiv i wynik w tabeli Markdown:


```bash
python tools/arxiv_search.py "CPT violation" --max 10 --cat hep-th
```


## Routing modelu
Routing modeli dla agentow:


```bash
python tools/route_model.py cross-reference
python tools/route_model.py model-review --gate 3
```


Konfiguracja w tools/model_routing.json.