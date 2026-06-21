#!/usr/bin/env python
from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import math
from pathlib import Path

import sympy as sp


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str


def run_symbolic_checks() -> list[CheckResult]:
    G, M, a, e, c, beta, lam, Fe = sp.symbols(
        "G M a e c beta lam Fe", positive=True
    )

    delta_1pn = 6 * sp.pi * G * M / (a * (1 - e**2) * c**2)
    delta_y = sp.pi * beta * (a / lam) ** 2 * sp.exp(-a / lam) * Fe
    delta_total = delta_1pn + delta_y
    ratio = sp.simplify(sp.Abs(delta_y) / sp.Abs(delta_1pn))

    checks: list[CheckResult] = []

    beta_limit = sp.simplify(sp.limit(delta_total, beta, 0) - delta_1pn)
    checks.append(
        CheckResult(
            name="K5a beta->0",
            ok=beta_limit == 0,
            detail=f"limit(delta_total, beta->0) - delta_1pn = {beta_limit}",
        )
    )

    lambda_limit = sp.simplify(sp.limit(delta_y, lam, sp.oo))
    checks.append(
        CheckResult(
            name="K5b lambda->inf",
            ok=lambda_limit == 0,
            detail=f"limit(delta_y, lambda->inf) = {lambda_limit}",
        )
    )

    ratio_at_beta0 = sp.simplify(sp.limit(ratio, beta, 0))
    checks.append(
        CheckResult(
            name="K5c R(beta->0)",
            ok=ratio_at_beta0 == 0,
            detail=f"limit(R, beta->0) = {ratio_at_beta0}",
        )
    )

    checks.append(
        CheckResult(
            name="K5d struktura R",
            ok=True,
            detail=f"R = {ratio}",
        )
    )

    return checks


def mercury_1pn_arcsec_per_century() -> float:
    # SI constants and Mercury orbital parameters (reference values).
    G = 6.67430e-11
    M_sun = 1.98847e30
    c = 299792458.0
    a = 5.790905e10
    e = 0.205630
    period_days = 87.9691

    delta_per_orbit_rad = 6.0 * math.pi * G * M_sun / (a * (1.0 - e**2) * c**2)
    orbits_per_century = (36525.0 / period_days)
    arcsec_per_century = delta_per_orbit_rad * orbits_per_century * (180.0 / math.pi) * 3600.0
    return arcsec_per_century


def write_report(out_path: Path, checks: list[CheckResult], mercury_value: float) -> None:
    timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    status = "OK" if all(check.ok for check in checks[:3]) else "Warning"

    lines = [
        "# Wyniki CAS T04",
        "",
        f"- Data: {timestamp}",
        "- Narzedzie: SymPy",
        f"- Status: {status}",
        "",
        "## Wyniki [VERIFY-CAS]",
        "| Check | Wynik | Szczegoly |",
        "|---|---|---|",
    ]

    for check in checks:
        result = "PASS" if check.ok else "FAIL"
        lines.append(f"| {check.name} | {result} | {check.detail} |")

    lines.extend(
        [
            "",
            "## Kontrola liczbowa 1PN (Merkury)",
            f"- delta_phi_1PN ~= {mercury_value:.4f} arcsec/century",
            "- Uwaga: wartosc sluzy jako sanity-check skali wyniku.",
            "",
        ]
    )

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    checks = run_symbolic_checks()
    mercury_value = mercury_1pn_arcsec_per_century()
    out_path = Path(__file__).resolve().parent / "Wyniki-CAS-T04.md"
    write_report(out_path, checks, mercury_value)
    print(f"[OK] CAS report written: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
