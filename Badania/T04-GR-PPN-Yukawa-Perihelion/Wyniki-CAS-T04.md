# Wyniki CAS T04

- Data: 2026-06-21 01:27:38 UTC
- Narzedzie: SymPy
- Case ID: T04-GR-PPN-Yukawa-Perihelion
- Status: OK

## Wyniki [VERIFY-CAS]
| Check | Wynik | Szczegoly |
|---|---|---|
| K5a beta->0 | PASS | limit(delta_total - delta_1pn, beta->0) = 0 |
| K5b lambda->inf | PASS | limit(delta_y, lam->oo) = 0 |
| K5c R(beta->0) | PASS | limit(ratio, beta->0) = 0 |
| K5d struktura R | PASS | Fe*a**3*beta*c**2*exp(-a/lam)*Abs(e**2 - 1)/(6*G*M*lam**2) |
| N1 1PN Merkury (arcsec/century) | PASS | value=42.98197550, expected=42.98200000, abs_diff=0.00002450, abs_tol=0.10000000 |
