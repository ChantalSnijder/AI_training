"""Mandatory checks for every transformation step. See CLAUDE.md §4.

Usage in src/03_clean.py:
    from checks.checks import log_step, assert_unique, assert_join, assert_range, reconcile, write_log

Every function prints its result so it appears verbatim in the agent's output.
Never weaken a check to make it pass. If it fails, stop and report.
"""
from __future__ import annotations
import pandas as pd

LOG: list[dict] = []


def log_step(step: str, df_in: pd.DataFrame, df_out: pd.DataFrame, note: str = "") -> None:
    row = {"step": step, "rows_in": len(df_in), "rows_out": len(df_out), "note": note}
    LOG.append(row)
    print(f"[step] {step:<32} {len(df_in):>10,} -> {len(df_out):>10,}  {note}")


def assert_unique(df: pd.DataFrame, keys: list[str], name: str) -> None:
    dups = df.duplicated(subset=keys).sum()
    print(f"[check] unique {name} on {keys}: {dups:,} duplicates")
    assert dups == 0, f"{name}: {dups} duplicate rows on {keys}"


def assert_join(left: pd.DataFrame, right: pd.DataFrame, keys: list[str],
                how: str, expected: str, name: str) -> pd.DataFrame:
    """expected: '1:1', '1:m', 'm:1'. Uses pandas validate and reports row counts."""
    validate = {"1:1": "one_to_one", "1:m": "one_to_many", "m:1": "many_to_one"}[expected]
    out = left.merge(right, on=keys, how=how, validate=validate, indicator=True)
    counts = out["_merge"].value_counts().to_dict()
    print(f"[check] join {name} ({how}, {expected}) on {keys}: "
          f"left={len(left):,} right={len(right):,} out={len(out):,} match={counts}")
    return out.drop(columns="_merge")


def null_rates(df: pd.DataFrame, name: str) -> pd.Series:
    rates = df.isna().mean().round(4)
    print(f"[check] null rates {name}:\n{rates[rates > 0].to_string() or '  none'}")
    return rates


def assert_range(df: pd.DataFrame, col: str, lo=None, hi=None) -> None:
    s = df[col]
    bad = ((s < lo) if lo is not None else False) | ((s > hi) if hi is not None else False)
    n = int(bad.sum()) if hasattr(bad, "sum") else 0
    print(f"[check] range {col} in [{lo}, {hi}]: {n:,} violations")
    assert n == 0, f"{col}: {n} values outside [{lo}, {hi}]"


def reconcile(ours: float, target: float, tolerance: float, label: str) -> None:
    delta = ours - target
    rel = delta / target if target else float("nan")
    ok = abs(rel) <= tolerance
    print(f"[reconcile] {label}: ours={ours:,.2f} target={target:,.2f} "
          f"delta={delta:,.2f} ({rel:+.2%}) tolerance={tolerance:.2%} -> {'PASS' if ok else 'FAIL'}")
    assert ok, f"Reconciliation failed for {label}; do not adjust tolerance, report and ask."


def write_log(path: str = "analysis/03_data_log.csv") -> None:
    pd.DataFrame(LOG).to_csv(path, index=False)
    print(f"[log] {len(LOG)} steps written to {path}")
