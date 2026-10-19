"""Forecast renewal ARR by quarter, and compare CSM calls with what the data says.

Implements frameworks/renewal-forecast.md: each renewing account gets a
category from its signals (Commit, Best case, At risk, Lost), the CSM's call
is used where one exists, and every call that disagrees with the signals is
listed for the forecast review. Writes markdown to stdout. Standard library only.

Usage:
    python3 tools/renewal_forecast.py sample-data/accounts.csv \
        --plans sample-data/success-plans.csv --calls sample-data/forecast-calls.csv \
        --as-of 2026-10-01 --quarters 2
"""

import argparse
import csv
import sys
from datetime import date

from score_accounts import load_book, num

CATEGORIES = ["Lost", "At risk", "Best case", "Commit"]  # worst to best
WEIGHTS = {"Commit": 0.95, "Best case": 0.7, "At risk": 0.4, "Lost": 0.0}
OTHER_RED_FLAGS = ("exec_sponsor_departed", "payment_dispute")


def quarter(day):
    return f"{day.year}-Q{(day.month - 1) // 3 + 1}"


def next_quarters(as_of, count):
    year, q = as_of.year, (as_of.month - 1) // 3 + 1
    labels = []
    for _ in range(count):
        labels.append(f"{year}-Q{q}")
        q += 1
        if q == 5:
            year, q = year + 1, 1
    return labels


def signal_category(raw, scored):
    """The category the data supports, before any CSM call."""
    flags = [f for f in raw["red_flags"].split("|") if f.strip()]
    if "non_renewal_notice" in flags:
        return "Lost"
    if scored["band"] == "Red" or any(f in flags for f in OTHER_RED_FLAGS):
        return "At risk"
    if (scored["band"] == "Green" and not num(raw["contract_flags"])
            and not num(raw["open_escalations"])):
        return "Commit"
    return "Best case"


def load_calls(path):
    calls = {}
    if not path:
        return calls
    with open(path, newline="") as f:
        for line, row in enumerate(csv.DictReader(f), start=2):
            if row["csm_call"] not in CATEGORIES:
                raise ValueError(f"{path} line {line}: csm_call must be one of {', '.join(CATEGORIES)}")
            calls[row["account_id"]] = row
    return calls


def build_forecast(raw_rows, scored_rows, calls, as_of, quarters):
    """Return (rows, totals by quarter) for accounts renewing in the forecast quarters."""
    labels = next_quarters(as_of, quarters)
    rows = []
    for raw, scored in zip(raw_rows, scored_rows):
        renewal = date.fromisoformat(raw["renewal_date"])
        if renewal < as_of or quarter(renewal) not in labels:
            continue
        signal = signal_category(raw, scored)
        call = calls.get(raw["account_id"])
        used = call["csm_call"] if call else signal
        arr = float(raw["arr"])
        if call and (call.get("expected_arr") or "").strip():
            expected = float(call["expected_arr"])
        else:
            expected = 0.0 if used == "Lost" else arr
        if not call:
            gap = "no call"
        else:
            diff = CATEGORIES.index(call["csm_call"]) - CATEGORIES.index(signal)
            gap = "call above signals" if diff > 0 else "call below signals" if diff < 0 else ""
        rows.append({
            "quarter": quarter(renewal), "account_id": raw["account_id"], "account": raw["account"],
            "csm": raw["csm"], "renewal_date": raw["renewal_date"], "arr": arr, "band": scored["band"],
            "signal": signal, "call": call["csm_call"] if call else "", "used": used,
            "expected": expected, "weighted": expected * WEIGHTS[used], "gap": gap,
            "note": call["note"] if call else "",
        })
    rows.sort(key=lambda r: (r["renewal_date"], r["account"]))

    totals = {}
    for label in labels:
        q = [r for r in rows if r["quarter"] == label]
        commit = sum(r["expected"] for r in q if r["used"] == "Commit")
        totals[label] = {
            "accounts": len(q),
            "up_for_renewal": sum(r["arr"] for r in q),
            "commit": commit,
            "best_case": commit + sum(r["expected"] for r in q if r["used"] == "Best case"),
            "weighted": sum(r["weighted"] for r in q),
            "lost": sum(r["arr"] for r in q if r["used"] == "Lost"),
            "downgrades": sum(r["arr"] - r["expected"] for r in q
                              if r["used"] != "Lost" and r["expected"] < r["arr"]),
        }
    return rows, totals


def money(value):
    return f"${value:,.0f}"


def render(rows, totals, as_of):
    out = ["# Renewal Forecast", "", f"As of {as_of}. Weights: "
           + ", ".join(f"{k} {int(v * 100)}%" for k, v in WEIGHTS.items()) + ".", "",
           "## By quarter", "",
           "| Quarter | Accounts | Up for renewal | Commit | Best case | Weighted | Lost | Known downgrades |",
           "|---|---|---|---|---|---|---|---|"]
    for label, t in totals.items():
        out.append(f"| {label} | {t['accounts']} | {money(t['up_for_renewal'])} | {money(t['commit'])} | "
                   f"{money(t['best_case'])} | {money(t['weighted'])} | {money(t['lost'])} | {money(t['downgrades'])} |")
    out += ["", "## By account", "",
            "| Quarter | Account | CSM | Renewal | ARR | Band | Signals say | CSM call | Expected ARR | Check |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        out.append(f"| {r['quarter']} | {r['account']} | {r['csm']} | {r['renewal_date']} | {money(r['arr'])} | "
                   f"{r['band']} | {r['signal']} | {r['call'] or '(none)'} | {money(r['expected'])} | {r['gap']} |")
    review = [r for r in rows if r["gap"]]
    review.sort(key=lambda r: ({"call above signals": 0, "no call": 1, "call below signals": 2}[r["gap"]], -r["arr"]))
    out += ["", "## Calls to review", ""]
    if review:
        for r in review:
            why = f"{r['csm']} calls {r['call']}, signals say {r['signal']}" if r["call"] else \
                  f"no call from {r['csm']}; using {r['signal']} from signals"
            out.append(f"- **{r['account']}** ({money(r['arr'])}, {r['gap']}): {why}." + (f" Note: {r['note']}" if r["note"] else ""))
    else:
        out.append("None. Every call matches the signals.")
    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("accounts_csv")
    parser.add_argument("--plans", help="success plans CSV, the source of the Outcomes signal")
    parser.add_argument("--calls", help="CSM forecast calls CSV")
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today(),
                        help="forecast date (YYYY-MM-DD)")
    parser.add_argument("--quarters", type=int, default=2, help="quarters to forecast, starting with the current one")
    args = parser.parse_args()
    try:
        raw, scored, _ = load_book(args.accounts_csv, args.plans, args.as_of)
        calls = load_calls(args.calls)
    except ValueError as e:
        sys.exit(str(e))
    if not args.plans:
        print("warning: no --plans file, so no account can be Green or Commit from signals", file=sys.stderr)
    unknown = sorted(set(calls) - {r["account_id"] for r in raw})
    if unknown:
        print(f"warning: calls for accounts not in {args.accounts_csv}: {', '.join(unknown)}", file=sys.stderr)
    rows, totals = build_forecast(raw, scored, calls, args.as_of, args.quarters)
    sys.stdout.write(render(rows, totals, args.as_of))


if __name__ == "__main__":
    main()
