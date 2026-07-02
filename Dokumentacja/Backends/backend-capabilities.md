# Backend Capabilities Map (Etap G3)

Data: 2026-07-02
Status: active
Wersja: 1.0.0
Owner: Technical Developer
Pewnosc: 0.94

## Cel

Zmapowac backendy obliczeniowe do wspolnego interfejsu i wskazac ich aktualna gotowosc.

## Artefakty wykonawcze (machine-readable)

1. `mcp/backends/backend_interface.contract.json`
2. `mcp/backends/backend_capabilities.json`

Walidacja automatyczna:
- `python tools/contract_guard.py`

## Legenda

- active: backend uzywany w obecnych narzedziach
- candidate: backend planowany, bez integracji runtime w tools/

## Tabela capabilities

| Backend | Status | capability_check | execute | validate | export_trace | Uzycia w repo |
|---|---|---|---|---|---|---|
| SymPy | active | symbolic: yes | symbolic: yes | symbolic checks: yes | partial | tools/cas_test_harness.py |
| NumPy | active | numeric: yes | numeric: yes | numeric checks: yes | partial | tools/binet_numeric_validation_t04.py |
| Matplotlib | active | visualization: yes | chart generation: yes | artifact checks: via tools | partial | tools/generate_t04_charts.py |
| SciPy | candidate | statistical: planned | statistical: planned | planned | planned | brak integracji runtime |
| JAX | candidate | numeric-hpc: planned | numeric-hpc: planned | planned | planned | brak integracji runtime |
| PyTorch | candidate | tensor: planned | tensor: planned | planned | planned | brak integracji runtime |
| Cadabra | candidate | symbolic-physics: planned | planned | planned | planned | brak integracji runtime |
| FORM | candidate | symbolic-physics: planned | planned | planned | planned | brak integracji runtime |

## Minimalne mapowanie wymagane przez G3

Wymog G3: mapowanie minimum 2 backendow.

Stan:
1. SymPy: mapped (active)
2. NumPy: mapped (active)

Wniosek:
- Kryterium minimalne mapowania backendow jest spelnione.

## Ograniczenia i ryzyka

1. export_trace jest czesciowy i realizowany glownie przez warstwe tools/reporting.
2. Backendy candidate wymagaja osobnego ADR przed integracja runtime.
3. Brak backendu dla zadania krytycznego musi skutkowac fail-closed.
