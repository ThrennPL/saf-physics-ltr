# Scientific Backend Interface Spec (Etap G3)

Data: 2026-07-02
Status: active
Wersja: 1.0.0
Owner: Technical Developer
Pewnosc: 0.95

## Cel

Oddzielic warstwe backend obliczeniowy od warstw Agent/Skill/Tool i utrzymac audytowalny kontrakt wykonania.

## Zakres

Specyfikacja obejmuje:
1. kontrakt capability_check,
2. kontrakt execute,
3. kontrakt validate,
4. kontrakt export_trace,
5. wymagane metadane wykonania.

Poza zakresem:
- decyzje gate,
- routing agentow,
- polityki HITL/fail-closed.

## Kontrakt logiczny interfejsu

Interface: ScientificBackend

### 1) capability_check(task_type, context)

Input contract:
- task_type: symbolic | numeric | statistical | visualization | governance
- context: ograniczenia i wymagania zadania

Output contract:
- supported: true/false
- reason: tekst
- limits: lista ograniczen backendu
- status: OK/Warning/Blocker

Error contract:
- code: capability_query_failed
- recoverable: true
- escalation_required: false

### 2) execute(task_spec, context)

Input contract:
- task_spec: specyfikacja operacji obliczeniowej
- context: parametry runtime (np. precision, seed, timeout)

Output contract:
- result_payload: wynik domenowy
- diagnostics[]: komunikaty wykonania
- metadata: komplet metadanych wykonania
- status: OK/Warning/Blocker

Error contract:
- code: execution_failed
- recoverable: true/false (zalezne od przyczyny)
- escalation_required: true dla bledow krytycznych

### 3) validate(result_payload, validation_spec)

Input contract:
- result_payload
- validation_spec: kryteria walidacyjne

Output contract:
- validation_report
- findings[]
- confidence: 0-1
- status: OK/Warning/Blocker

Error contract:
- code: validation_failed
- recoverable: true
- escalation_required: false

### 4) export_trace(result_payload, metadata)

Input contract:
- result_payload
- metadata

Output contract:
- audit_artifacts[]
- trace_hash
- status: OK/Warning/Blocker

Error contract:
- code: trace_export_failed
- recoverable: true
- escalation_required: true

## Obowiazkowe metadane

Kazde wykonanie backendu musi eksportowac:
1. backend_name
2. backend_version
3. execution_mode
4. deterministic_seed (jesli dotyczy)
5. input_hash
6. runtime_limits
7. started_at
8. finished_at

## Zasady fail-closed

1. Brak wymaganych metadanych => Blocker.
2. Niespelnienie kontraktu output/error => Blocker.
3. Backend nie moze nadpisywac semantyki gate.

## Mapowanie do warstw

1. Agent wybiera chain skillowy.
2. Skill korzysta z Tool contract.
3. Tool moze delegowac obliczenia do Scientific Backend Interface.
4. Wynik wraca do skilla w standaryzowanym kontrakcie.
