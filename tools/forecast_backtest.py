"""Back-test the renewal forecast: how much of each category actually renewed?

Reads the category and expected ARR each renewal had at the start of its
quarter, and what actually renewed. Reports forecast accuracy by quarter and
how much of each category's expected ARR landed, which is the evidence for
changing the weights in frameworks/renewal-forecast.md. Writes markdown to
stdout. Standard library only.

Usage:
    python3 tools/forecast_backtest.py sample-data/forecast-history.csv
"""

import argparse
import csv
import sys

from renewal_forecast import CATEGORIES, WEIGHTS

MIN_RENEWALS = 10  # renewals a category needs before its realization should set a weight


def load_history(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    for line, row in enumerate(rows, start=2):
        if row["category"] not in CATEGORIES:
            raise ValueError(f"{path} line {line}: category must be one of {', '.join(CATEGORIES)}")
        for field in ("arr", "expected_arr", "actual_arr"):
            row[field] = float(row[field])
        # Renewed ARR excludes expansion: the forecast is of keeping ARR, not growing it.
        row["kept"] = min(row["actual_arr"], row["arr"])
        row["weighted"] = row["expected_arr"] * WEIGHTS[row["category"]]
    return rows


def accuracy(rows):
    """{quarter: (renewed ARR, weighted forecast)}, plus the same summed over all quarters."""
    quarters = {}
    for row in rows:
        kept, weighted = quarters.get(row["quarter"], (0.0, 0.0))
        quarters[row["quarter"]] = (kept + row["kept"], weighted + row["weighted"])
    total = (sum(k for k, _ in quarters.values()), sum(w for _, w in quarters.values()))
    return dict(sorted(quarters.items())), total


def money(value):
    return f"${value:,.0f}"


def pct(part, whole):
    return f"{100 * part / whole:.0f}%" if whole else "n/a"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("history_csv")
    args = parser.parse_args()
    try:
        rows = load_history(args.history_csv)
    except (ValueError, KeyError) as e:
        sys.exit(str(e))

    quarters, (kept, weighted) = accuracy(rows)
    out = ["# Forecast Back-test", "",
           f"{len(rows)} renewals across {len(quarters)} quarters, scored with today's weights: "
           + ", ".join(f"{k} {int(v * 100)}%" for k, v in WEIGHTS.items()) + ".", "",
           "## Forecast accuracy", "",
           "Renewed ARR (excluding expansion) divided by the weighted forecast at the start of the quarter. "
           "Over 100% means the forecast was too cautious.", "",
           "| Quarter | Renewals | Weighted forecast | Renewed | Accuracy |", "|---|---|---|---|---|"]
    for quarter, (k, w) in quarters.items():
        count = sum(1 for r in rows if r["quarter"] == quarter)
        out.append(f"| {quarter} | {count} | {money(w)} | {money(k)} | {pct(k, w)} |")
    out.append(f"| **All** | **{len(rows)}** | **{money(weighted)}** | **{money(kept)}** | **{pct(kept, weighted)}** |")

    out += ["", "## Realization by category", "",
            "The share of each category's expected ARR that renewed. With enough renewals, it is the weight to use.", "",
            "| Category | Renewals | Expected ARR | Renewed (up to expected) | Realization | Current weight | Suggested weight |",
            "|---|---|---|---|---|---|---|"]
    for category in reversed(CATEGORIES):
        c = [r for r in rows if r["category"] == category]
        if not c:
            continue
        expected = sum(r["expected_arr"] for r in c)
        landed = sum(min(r["actual_arr"], r["expected_arr"]) for r in c)
        if len(c) >= MIN_RENEWALS and expected:
            suggested = f"{round(20 * landed / expected) * 5}%"
        else:
            suggested = f"keep: under {MIN_RENEWALS} renewals"
        out.append(f"| {category} | {len(c)} | {money(expected)} | {money(landed)} | {pct(landed, expected)} | "
                   f"{int(WEIGHTS[category] * 100)}% | {suggested} |")

    surprises = [r for r in rows if r["category"] in ("Commit", "Best case") and r["actual_arr"] == 0]
    out += ["", "## Churned from Commit or Best case", ""]
    out += [f"- **{r['account']}** ({r['quarter']}, {r['category']}): {money(r['arr'])} expected to renew, churned. "
            "What did the call and the signals miss?" for r in surprises] or ["None."]
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
