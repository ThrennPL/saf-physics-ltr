# SAF/LTR Etap G Migration Report

Data: 2026-07-02
Status: accepted (HITL)
Pewnosc: 0.98
Owner: Orkiestrator

## Cel

Potwierdzic domkniecie migracji warstwowej Etapu G (Architecture-2.1) bez regresji runtime Architecture-2.0.

## Zakres wykonany

1. G1 Instructions foundation:
- `Dokumentacja/Instructions/README.md`
- `Dokumentacja/Instructions/*.instructions.md`

2. G2 Skills + Tool contracts:
- `Dokumentacja/Skills/skill-contracts-registry.md`
- `Dokumentacja/Tools/tool-contracts-registry.md`
- `Dokumentacja/Tools/compatibility-matrix.md`

3. G3 Backend interface + closure:
- `Dokumentacja/Backends/backend-interface-spec.md`
- `Dokumentacja/Backends/backend-capabilities.md`
- niniejszy raport migracyjny
- raport kompatybilnosci Etapu G

## Weryfikacja kryteriow done

| Kryterium | Oczekiwane | Stan |
|---|---|---|
| G1 policy extraction | Instructions jako source-of-truth | OK |
| G2 mapowalnosc flow | >=80% Agent->Skill->Tool | OK (90%) |
| G3 backend mapping | min. 2 backendy | OK (SymPy, NumPy) |
| Invarianty 2.0 | HITL/fail-closed bez zmian | OK |

## Walidacja operacyjna

Wynik quality-gates-offline po wdrozeniu G1-G3:
1. ruff: PASS
2. pytest: PASS
3. mypy: PASS
4. build-smoke-offline: PASS

## Ryzyka resztkowe

1. Warning: backendy candidate nie sa jeszcze zintegrowane runtime.
2. Warning: export_trace jest realizowany glownie przez tools, nie przez dedykowany adapter backendowy.

## Wniosek

Etap G jest wykonany technicznie i gotowy do decyzji GO/NO-GO przez human owner (HITL).

## Decyzja HITL

1. Status: GO accepted
2. Data decyzji: 2026-07-02
3. Zakres akceptacji: komplet G1-G3
4. Ograniczenie po akceptacji: integracje backendow candidate tylko przez oddzielny ADR

## Etap poakceptacyjny: Bridge i de-dup agentow (.github)

Status: completed
Data: 2026-07-02
Pewnosc: 0.97

Zakres wykonany:
1. Dodano centralne mapowanie Agent -> Skill:
	- `.github/agent-skill-binding.json`
2. Dodano source-of-truth runtime do instrukcji globalnych:
	- `.github/copilot-instructions.md`
3. Ujednolicono profile agentow `.github/agents/*`:
	- sekcje `Runtime bindings (Architecture 2.1)`
	- de-dup sekcji polityk wspolnych (statusy/placeholder/reporting) do referencji centralnych
4. Rozszerzono walidacje fail-closed:
	- `tools/contract_guard.py` sprawdza mapowanie agent-skill i pokrycie wszystkich agentow

Wynik:
- Warstwa `.github` i warstwa runtime `mcp/*` nie sa juz odrebnymi swiatami.

## Etap 2: orchestrator-only profiles (.github)

Status: completed (v1)
Data: 2026-07-02
Pewnosc: 0.96

Zakres wykonany:
1. Uproszczono kluczowe profile agentow do modelu ownership/routing/eskalacja.
2. Usunieto nadmiarowe szablony proceduralne z Orkiestratora.
3. Naprawiono i domknieto profil `language-polish-quality` po zmianach formatowania.
4. Utrzymano runtime bindings i centralne polityki jako source-of-truth.

Wynik:
- Profile agentow sa krotsze, mniej zdublowane i zgodne z warstwa runtime `mcp/*`.

## Etap 2: orchestrator-only full sweep (.github)

Status: completed (full)
Data: 2026-07-02
Pewnosc: 0.98

Zakres wykonany:
1. Ujednolicono wszystkie pozostale profile agentow do wspolnego schematu orchestrator-only.
2. Zachowano sekcje runtime bindings i referencje do centralnych polityk.
3. Potwierdzono fail-closed i sciezki eskalacji na poziomie profilow agentow.

Walidacja po full sweep:
1. ruff: PASS
2. pytest: PASS
3. mypy: PASS
4. build: PASS
5. security sanity: PASS
6. taxonomy guard: PASS
7. process suite T04: PASS (blockers=0)
8. contract_guard: PASS (blockers=0)

Wynik:
- Refaktor orchestrator-only jest zakonczony dla calej grupy profilow `.github/agents/*`.
