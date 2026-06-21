from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


# Parametry referencyjne T04 (Merkury)
A_M = 57.91e6 * 1_000  # m
E_M = 0.2056
P_ORB_DAYS = 87.969
DELTA_1PN_ARCSEC_CENTURY = 42.9819755

# Zakresy zgodne z Plan-Danych.md
LAMBDA_MIN = 1e10
LAMBDA_MAX = 1e12
BETA_MIN = -1e-10
BETA_MAX = 1e-10


def delta_phi_y_arcsec_century(beta: np.ndarray, lam: np.ndarray) -> np.ndarray:
    fe = 1.0 / (1.0 - E_M**2)
    delta_rad_orbit = math.pi * beta * (A_M / lam) ** 2 * np.exp(-A_M / lam) * fe
    rad_to_arcsec = (180.0 / math.pi) * 3600.0
    orbits_per_century = 36525.0 / P_ORB_DAYS
    return delta_rad_orbit * rad_to_arcsec * orbits_per_century


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    out_dir = repo_root / "Badania" / "T04-GR-PPN-Yukawa-Perihelion" / "wykresy"
    out_dir.mkdir(parents=True, exist_ok=True)

    lambdas = np.logspace(np.log10(LAMBDA_MIN), np.log10(LAMBDA_MAX), 300)

    # Wykres 1: Delta_phi_Y vs lambda dla wybranych beta
    plt.figure(figsize=(10, 6))
    for beta in [-1e-10, -5e-11, 5e-11, 1e-10]:
        y = delta_phi_y_arcsec_century(np.full_like(lambdas, beta), lambdas)
        plt.plot(lambdas, y, label=f"beta={beta:.1e}")
    plt.xscale("log")
    plt.xlabel("lambda [m]")
    plt.ylabel("Delta_phi_Y [arcsec/century]")
    plt.title("T04: Precesja Yukawy vs lambda")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_dir / "t04-precesja-vs-lambda.png", dpi=180)
    plt.close()

    # Wykres 2: mapa konturowa (beta, lambda) -> Delta_phi_Y
    beta_grid = np.linspace(BETA_MIN, BETA_MAX, 240)
    lambda_grid = np.logspace(np.log10(LAMBDA_MIN), np.log10(LAMBDA_MAX), 240)
    bb, ll = np.meshgrid(beta_grid, lambda_grid)
    zz = delta_phi_y_arcsec_century(bb, ll)

    plt.figure(figsize=(10, 6))
    contour = plt.contourf(ll, bb, zz, levels=40, cmap="coolwarm")
    plt.xscale("log")
    plt.xlabel("lambda [m]")
    plt.ylabel("beta [-]")
    plt.title("T04: Mapa konturowa Delta_phi_Y(beta, lambda)")
    cbar = plt.colorbar(contour)
    cbar.set_label("Delta_phi_Y [arcsec/century]")
    plt.tight_layout()
    plt.savefig(out_dir / "t04-mapa-beta-lambda.png", dpi=180)
    plt.close()

    # Wykres 3: porownanie skladowych precesji
    beta_ref = 1e-10
    delta_y = delta_phi_y_arcsec_century(np.full_like(lambdas, beta_ref), lambdas)
    delta_1pn = np.full_like(lambdas, DELTA_1PN_ARCSEC_CENTURY)
    delta_total = delta_1pn + delta_y

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    ax1.plot(lambdas, delta_1pn, label="1PN", color="black", linewidth=2)
    ax1.plot(lambdas, delta_total, label="1PN + Yukawa", color="tab:blue")
    ax1.set_xscale("log")
    ax1.set_ylabel("Precesja [arcsec/century]")
    ax1.set_title("T04: Porownanie skladowych (beta=1e-10)")
    ax1.grid(True, which="both", alpha=0.3)
    ax1.legend()

    ax2.plot(lambdas, delta_y, label="Yukawa", color="tab:red")
    ax2.set_xscale("log")
    ax2.set_xlabel("lambda [m]")
    ax2.set_ylabel("Delta_phi_Y [arcsec/century]")
    ax2.grid(True, which="both", alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    plt.savefig(out_dir / "t04-porownanie-skladnikow.png", dpi=180)
    plt.close()


if __name__ == "__main__":
    main()
