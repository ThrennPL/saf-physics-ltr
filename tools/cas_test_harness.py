#!/usr/bin/env python
"""Config-driven CAS harness for symbolic and numeric process checks."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import sympy as sp


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    detail: str


def _load_config(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_target(raw: str) -> Any:
    raw = str(raw).strip()
    if raw.lower() in {"oo", "inf", "infinity"}:
        return sp.oo
    if raw.lower() in {"-oo", "-inf", "-infinity"}:
        return -sp.oo
    return sp.sympify(raw)


def _build_context(cfg: dict[str, Any]) -> dict[str, Any]:
    context: dict[str, Any] = {"pi": sp.pi, "E": sp.E, "exp": sp.exp, "Abs": sp.Abs}

    for symbol in cfg.get("symbols", []):
        if not isinstance(symbol, str) or not symbol.strip():
            continue
        context[symbol] = sp.symbols(symbol.strip(), positive=True)

    for name, expr in cfg.get("derived", {}).items():
        context[name] = sp.sympify(str(expr), locals=context)

    return context


def _run_test(test: dict[str, Any], context: dict[str, Any]) -> CheckResult:
    test_type = str(test.get("type", "")).strip()
    name = str(test.get("name", "unnamed"))

    if test_type == "limit_zero":
        expr = sp.sympify(str(test["expr"]), locals=context)
        var = context[str(test["var"])]
        target = _parse_target(str(test.get("target", "0")))
        value = sp.simplify(sp.limit(expr, var, target))
        passed = value == 0
        return CheckResult(
            name=name,
            passed=passed,
            detail=f"limit({test['expr']}, {test['var']}->{target}) = {value}",
        )

    if test_type == "symbolic_equals":
        left = sp.sympify(str(test["left"]), locals=context)
        right = sp.sympify(str(test["right"]), locals=context)
        diff = sp.simplify(left - right)
        passed = diff == 0
        return CheckResult(name=name, passed=passed, detail=f"simplify(left-right) = {diff}")

    if test_type == "contains_tokens":
        expr = sp.sympify(str(test["expr"]), locals=context)
        rendered = str(sp.simplify(expr))
        tokens = [str(token) for token in test.get("tokens", [])]
        missing = [token for token in tokens if token not in rendered]
        passed = not missing
        detail = rendered if passed else f"missing tokens={missing}; expr={rendered}"
        return CheckResult(name=name, passed=passed, detail=detail)

    if test_type == "numeric_close":
        expr = sp.sympify(str(test["expr"]), locals=context)
        numeric_context = {
            context[k]: float(v) for k, v in test.get("numeric_context", {}).items() if k in context
        }
        value = float(expr.evalf(subs=numeric_context))
        expected = float(test["expected"])
        abs_tol = float(test.get("abs_tol", 1e-6))
        diff = abs(value - expected)
        passed = diff <= abs_tol
        return CheckResult(
            name=name,
            passed=passed,
            detail=(
                f"value={value:.8f}, expected={expected:.8f}, "
                f"abs_diff={diff:.8f}, abs_tol={abs_tol:.8f}"
            ),
        )

    return CheckResult(name=name, passed=False, detail=f"unsupported test type: {test_type}")


def _write_report(
    report_path: Path, title: str, results: list[CheckResult], meta: dict[str, Any]
) -> None:
    timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    all_passed = all(item.passed for item in results)
    status = "OK" if all_passed else "Warning"

    lines = [
        f"# {title}",
        "",
        f"- Data: {timestamp}",
        "- Narzedzie: SymPy",
        f"- Case ID: {meta.get('case_id', '-')}",
        f"- Status: {status}",
        "",
        "## Wyniki [VERIFY-CAS]",
        "| Check | Wynik | Szczegoly |",
        "|---|---|---|",
    ]

    for item in results:
        lines.append(f"| {item.name} | {'PASS' if item.passed else 'FAIL'} | {item.detail} |")

    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run config-driven CAS checks")
    parser.add_argument("--config", required=True, help="Path to JSON config")
    parser.add_argument("--report", required=True, help="Path to markdown report")
    parser.add_argument(
        "--fail-on-fail",
        action="store_true",
        help="Exit 1 when at least one test fails",
    )
    args = parser.parse_args()

    cfg_path = Path(args.config).resolve()
    report_path = Path(args.report).resolve()

    if not cfg_path.exists():
        print(f"[FAIL] config not found: {cfg_path}")
        return 1

    try:
        cfg = _load_config(cfg_path)
        context = _build_context(cfg)
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"[FAIL] cannot load config: {exc}")
        return 1

    tests = cfg.get("tests", [])
    if not tests:
        print("[FAIL] no tests in config")
        return 1

    results: list[CheckResult] = []
    for test in tests:
        results.append(_run_test(test, context))

    for item in results:
        level = "OK" if item.passed else "FAIL"
        print(f"[{level}] {item.name}: {item.detail}")

    _write_report(
        report_path=report_path,
        title=str(cfg.get("title", "Wyniki CAS")),
        results=results,
        meta=cfg.get("meta", {}),
    )
    print(f"[OK] report written: {report_path}")

    if args.fail_on_fail and any(not item.passed for item in results):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
