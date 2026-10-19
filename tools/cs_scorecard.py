"""Compute the CS metrics scorecard for leadership.

Implements the definitions in frameworks/cs-metrics-scorecard.md: retention
from renewal history, book health, value realized, the renewal forecast, and
capacity, each with its formula's inputs shown. Writes markdown to stdout.
Standard library only.

Usage:
    python3 tools/cs_scorecard.py sample-data/accounts.csv \
        --plans sample-data/success-plans.csv \
        --adoption sample-data/feature-adoption.csv \
        --history sample-data/renewal-history.csv \
        --calls sample-data/forecast-calls.csv \
        --capacity sample-data/capacity-inputs.json \
        --forecast-history sample-data/forecast-history.csv --as-of 2026-10-01
"""

import argparse
import csv
import json
import sys
from datetime import date, timedelta

from outcome_progress import GOOD_STATUSES, SCORED_STATUSES, add_support, load_adoption, load_library
from forecast_backtest import accuracy, load_history
from renewal_forecast import build_forecast, load_calls
from score_accounts import load_book
from team_rollup import at_risk, build_rollup

OUTCOMES = ("Renewed", "Expanded", "Downgraded", "Churned")


def retention(path, as_of):
    """Renewal-cohort retention for renewals in the 12 months up to as_of."""
    start = as_of - timedelta(days=365)
    with open(path, newline="") as f:
        rows = [r for r in csv.DictReader(f) if start < date.fromisoformat(r["renewal_date"]) <= as_of]
    for row in rows:
        if row["outcome"] not in OUTCOMES:
            raise ValueError(f"{path}: outcome must be one of {', '.join(OUTCOMES)}, got {row['outcome']!r}")
    before = sum(float(r["arr_before"]) for r in rows)
    after = sum(float(r["arr_after"]) for r in rows)
    kept = sum(min(float(r["arr_before"]), float(r["arr_after"])) for r in rows)
    churned = [r for r in rows if r["outcome"] == "Churned"]
    reasons = {}
    for r in rows:
        if r["outcome"] in ("Churned", "Downgraded"):
            lost = float(r["arr_before"]) - float(r["arr_after"])
            reasons[r["reason"] or "untagged"] = reasons.get(r["reason"] or "untagged", 0) + lost
    return {"start": start, "renewals": len(rows), "before": before, "after": after, "kept": kept,
            "logos_kept": len(rows) - len(churned), "reasons": reasons}


def money(value):
    return f"${value:,.0f}"


def pct(part, whole):
    return f"{100 * part / whole:.1f}%" if whole else "n/a"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("accounts_csv")
    parser.add_argument("--plans", required=True, help="success plans CSV")
    parser.add_argument("--adoption", help="feature adoption CSV, to count proven goals")
    parser.add_argument("--history", help="renewal history CSV, for retention rates")
    parser.add_argument("--calls", help="CSM forecast calls CSV")
    parser.add_argument("--capacity", help="capacity model JSON")
    parser.add_argument("--forecast-history", help="past forecasts and outcomes CSV, for forecast accuracy")
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today(),
                        help="scorecard date (YYYY-MM-DD)")
    args = parser.parse_args()

    try:
        raw, scored, plans = load_book(args.accounts_csv, args.plans, args.as_of)
        if args.adoption:
            add_support(plans, load_library(), load_adoption(args.adoption))
        calls = load_calls(args.calls)
        capacity = json.load(open(args.capacity)) if args.capacity else None
        history = retention(args.history, args.as_of) if args.history else None
        forecasts = load_history(args.forecast_history) if args.forecast_history else None
    except (ValueError, KeyError) as e:
        sys.exit(str(e))

    total_arr = sum(float(r["arr"]) for r in raw)
    out = ["# CS Metrics Scorecard", "",
           f"As of {args.as_of}. {len(raw)} accounts, {money(total_arr)} ARR. "
           "Definitions in frameworks/cs-metrics-scorecard.md.", ""]

    out += ["## Retention", ""]
    if history:
        h = history
        out += ["| Metric | Value | Calculation |", "|---|---|---|",
                f"| Gross renewal rate (GRR) | {pct(h['kept'], h['before'])} | {money(h['kept'])} kept of {money(h['before'])} up for renewal |",
                f"| Net renewal rate (NRR) | {pct(h['after'], h['before'])} | {money(h['after'])} renewed of {money(h['before'])} up for renewal |",
                f"| Logo retention | {pct(h['logos_kept'], h['renewals'])} | {h['logos_kept']} of {h['renewals']} accounts renewed |",
                "", f"Renewals due from {h['start'] + timedelta(days=1)} to {args.as_of}. ARR lost by reason: "
                + (", ".join(f"{k} {money(v)}" for k, v in sorted(h["reasons"].items(), key=lambda kv: -kv[1])) or "none") + ".", ""]
    else:
        out += ["No `--history` file, so retention is not computed.", ""]

    bands = {}
    for s in scored:
        bands[s["band"]] = bands.get(s["band"], 0) + s["arr"]
    risk_arr = sum(float(r["arr"]) for r, s in zip(raw, scored) if at_risk(r, s))
    out += ["## Book health", "", "| Metric | Value |", "|---|---|"]
    for band in ("Green", "Yellow", "Red", "Insufficient data"):
        out.append(f"| ARR in {band} | {money(bands.get(band, 0))} ({pct(bands.get(band, 0), total_arr)}) |")
    out += [f"| ARR at risk (Red, or a red flag) | {money(risk_arr)} ({pct(risk_arr, total_arr)}) |", ""]

    goals = [g for gs in plans.values() for g in gs]
    counted = [g for g in goals if g["status"] in SCORED_STATUSES]
    good = [g for g in counted if g["status"] in GOOD_STATUSES]
    baselined = {a for a, gs in plans.items() if any(g["status"] != "No baseline" for g in gs)}
    baselined_arr = sum(float(r["arr"]) for r in raw if r["account_id"] in baselined)
    out += ["## Value realized", "", "| Metric | Value |", "|---|---|",
            f"| Accounts with a baselined success plan | {len(baselined & {r['account_id'] for r in raw})} of {len(raw)} "
            f"({pct(baselined_arr, total_arr)} of ARR) |",
            f"| Goals met or on track | {len(good)} of {len(counted)} counted ({pct(len(good), len(counted))}) |"]
    if args.adoption:
        proven = [g for g in goals if g.get("reading") == "Proven"]
        proven_arr = sum(float(r["arr"]) for r in raw if r["account_id"] in {g["account_id"] for g in proven})
        out += [f"| Goals proven | {len(proven)} of {len(counted)} counted ({pct(len(proven), len(counted))}) |",
                f"| ARR with at least one proven outcome | {money(proven_arr)} ({pct(proven_arr, total_arr)}) |"]
    out += ["| Time to first value | Not computed: needs close dates and first-value dates |", ""]

    rows, totals = build_forecast(raw, scored, calls, args.as_of, 1)
    (label, t), = totals.items()
    out += ["## Renewal forecast", "", "| Metric | Value |", "|---|---|",
            f"| Up for renewal in {label} | {money(t['up_for_renewal'])} across {t['accounts']} accounts |",
            f"| Commit | {money(t['commit'])} ({pct(t['commit'], t['up_for_renewal'])}) |",
            f"| Weighted forecast | {money(t['weighted'])} ({pct(t['weighted'], t['up_for_renewal'])}) |",
            f"| Calls that disagree with signals | {sum(1 for r in rows if r['gap'] and r['gap'] != 'no call')} |"]
    if forecasts:
        quarters, (kept, weighted) = accuracy(forecasts)
        last, (last_kept, last_weighted) = list(quarters.items())[-1]
        out += [f"| Forecast accuracy, {last} | {pct(last_kept, last_weighted)} ({money(last_kept)} renewed of "
                f"{money(last_weighted)} weighted) |",
                f"| Forecast accuracy, last {len(quarters)} quarters | {pct(kept, weighted)} |"]
    out.append("")

    if capacity:
        _, team = build_rollup(raw, scored, plans, capacity)
        out += ["## Capacity", "", "| Metric | Value |", "|---|---|",
                f"| Team utilization | {round(100 * team['utilization'])}% of {capacity['hours_per_csm_per_week']} hours per CSM |",
                f"| CSMs the book needs at {capacity['target_utilization_pct']}% target | {team['csms_needed']:.1f}, "
                f"against {len({r['csm'] for r in raw})} today |",
                f"| ARR per CSM | {money(total_arr / len({r['csm'] for r in raw}))} |", ""]
    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
