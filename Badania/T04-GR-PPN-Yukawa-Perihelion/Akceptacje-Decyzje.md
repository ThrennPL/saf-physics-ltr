# Sekcja akceptacji i decyzji

## Akceptacje
- Status: approved_with_mitigation
- Akceptujący (PI): HUMAN_OWNER
- Data: 2026-06-21

## Decyzje
| ID | Decyzja | Uzasadnienie | Owner | Data | Status |
|---|---|---|---|---|---|
| T04-DEC-001 | Start testu T04 | Test praktyczny agentów na złożonych wzorach | HUMAN_OWNER | 2026-06-21 | accepted |
| T04-DEC-002 | Kanoniczne F(e)=1/(1-e^2) (roboczo) | Potrzebna jednoznaczna postać do CI i raportowania; zgodność z perturbacyjnym trybem pracy | model-review | 2026-06-21 | accepted |
| T04-DEC-003 | CI przez Monte Carlo (N=120000) | Wymaganie Gate 3: tabela niepewnosci i przedzialy CI dla delta_phi_total | statistics-review | 2026-06-21 | accepted |
| T04-DEC-004 | Polityka zrodel: peer-reviewed + preprint z etykieta ryzyka | Zachowanie merytoryki i ciągłości evidence przy jawnej kontroli ryzyka interpretacyjnego | HUMAN_OWNER | 2026-06-21 | accepted |
| T04-DEC-005 | Walidacja językowa PL przed finalnym gate | Wymaganie redakcyjne i audytowalność dokumentów | language-polish-quality | 2026-06-21 | accepted |
| T04-DEC-006 | Akceptacja zgodnie z czynnościami mitygacyjnymi | Akceptacja warunkowa ryzyka preprint przy utrzymaniu etykiety RISK-PREPRINT-YUKAWA | HUMAN_OWNER | 2026-06-21 | accepted |
| T04-DEC-007 | Finalna decyzja Gate 4 (HITL) | Po domknięciu auditability i potwierdzeniu zero-loss merytoryki zatwierdzono zamknięcie case T04 | HUMAN_OWNER | 2026-06-21 | approved |

## Uwagi
- Gate 1/2/4 zatwierdza człowiek.
- Gate 3 moze mieć agent-conditional pass tylko przy niskim ryzyku i statusie OK bez krytycznych komentarzy.
