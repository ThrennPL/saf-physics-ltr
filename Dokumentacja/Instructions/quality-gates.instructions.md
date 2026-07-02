# quality-gates.instructions.md

Data: 2026-07-02
Status: active
Wersja: 1.0.0
Owner: Orkiestrator

## Cel

Jedno zrodlo prawdy dla semantyki gate, statusow i fail-closed.

## Reguly gate

1. Gate 1/2/4: decyzja zawsze human-in-the-loop.
2. Gate 3: dopuszczony agent-conditional pass tylko przy niskim ryzyku i bez krytycznych uwag.
3. Status roboczy agenta (OK/Warning/Blocker) nie jest decyzja gate.

## Semantyka statusow

1. OK: brak krytycznych ryzyk.
2. Warning: braki lub ryzyka niekrytyczne, wymagaja planu korekcyjnego.
3. Blocker: braki krytyczne, konflikt nierozstrzygniety, naruszenie kontraktu.

## Fail-closed

Uruchom fail-closed natychmiast, gdy wystapi przynajmniej jeden warunek:
1. Brak danych krytycznych.
2. Niespelnione warunki gate.
3. Naruszenie kontraktu workflow/capability/skill/tool/service.
4. Konflikt nierozstrzygniety w runtime krytycznym.

Efekt fail-closed:
1. stop_flow=true
2. gate_transition=denied
3. status=Blocker
4. eskalacja do Orkiestratora i Ownera

## Minimalny output gate review

1. status: OK/Warning/Blocker
2. pewnosc: 0-1
3. pytania Q-XXX
4. owner i ETA dla kazdego Warning/Blocker
