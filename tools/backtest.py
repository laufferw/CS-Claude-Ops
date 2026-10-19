"""Back-test the health score: did it flag the renewals that were lost?

For each renewal in the trailing 12 months, finds the account's scoring
snapshot from about 90 days before, bands it with the rubric (current
weights, and optionally a second set to compare), and checks the band
against what happened. This is the calibration test in
frameworks/account-health-scoring.md. Writes markdown to stdout.
Standard library only.

Usage:
    python3 tools/backtest.py --history sample-data/renewal-history.csv \
        --scores sample-data/score-history.csv --as-of 2026-10-01 \
        --compare usage=30,outcomes=20,engagement=15,support=15,sentiment=10,commercial=10
"""

import argparse
import csv
import sys
from datetime import date, timedelta

from score_accounts import WEIGHTS, band_signals, num

LOST = ("Churned", "Downgraded")
BANDS = ("Green", "Yellow", "Red", "Insufficient data")


def parse_weights(text):
    weights = {}
    for part in text.split(","):
        name, _, value = part.partition("=")
        weights[name.strip()] = float(value)
    if set(weights) != set(WEIGHTS):
        raise ValueError(f"--compare must give all six signals: {', '.join(WEIGHTS)}")
    if abs(sum(weights.values()) - 100) > 1e-9:
        raise ValueError(f"--compare weights must sum to 100, not {sum(weights.values()):g}")
    return weights


def load_snapshots(path):
    snapshots = {}
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            scores = {name: num(row[name]) for name in WEIGHTS}
            flags = [x for x in row["red_flags"].split("|") if x.strip()]
            snapshots.setdefault(row["account_id"], []).append((date.fromisoformat(row["as_of"]), scores, flags))
    return snapshots


def closest(snapshots, target, window):
    """The snapshot nearest the target date, within window days, or None."""
    best = None
    for day, scores, flags in snapshots:
        gap = abs((day - target).days)
        if gap <= window and (best is None or gap < best[0]):
            best = (gap, day, scores, flags)
    return best


def evaluate(renewals, weights):
    """Band every tested renewal with these weights, and summarize the results."""
    rows = []
    for r in renewals:
        _, band, _, _ = band_signals(r["scores"], r["flags"], weights)
        rows.append(dict(r, band=band))
    lost = [r for r in rows if r["outcome"] in LOST]
    lost_arr = sum(r["lost_arr"] for r in lost)
    return rows, {
        "lost_arr": lost_arr,
        "red": sum(r["lost_arr"] for r in lost if r["band"] == "Red"),
        "red_yellow": sum(r["lost_arr"] for r in lost if r["band"] in ("Red", "Yellow")),
        "misses": [r for r in lost if r["band"] == "Green"],
        "false_alarms": [r for r in rows if r["band"] == "Red" and r["outcome"] not in LOST],
    }


def money(value):
    return f"${value:,.0f}"


def share(part, whole):
    return f"{100 * part / whole:.0f}%" if whole else "n/a"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--history", required=True, help="renewal history CSV")
    parser.add_argument("--scores", required=True, help="score history CSV: signal scores per account per date")
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today(),
                        help="end of the 12-month window (YYYY-MM-DD)")
    parser.add_argument("--lead-days", type=int, default=90, help="how far before renewal to look (default 90)")
    parser.add_argument("--window-days", type=int, default=21,
                        help="how far from the lead date a snapshot may be (default 21)")
    parser.add_argument("--compare", help="a second weight set, such as usage=30,outcomes=20,...")
    args = parser.parse_args()

    try:
        compare = parse_weights(args.compare) if args.compare else None
        snapshots = load_snapshots(args.scores)
    except ValueError as e:
        sys.exit(str(e))

    start = args.as_of - timedelta(days=365)
    with open(args.history, newline="") as f:
        due = [r for r in csv.DictReader(f) if start < date.fromisoformat(r["renewal_date"]) <= args.as_of]
    renewals, untested = [], []
    for r in due:
        target = date.fromisoformat(r["renewal_date"]) - timedelta(days=args.lead_days)
        found = closest(snapshots.get(r["account_id"], []), target, args.window_days)
        if found is None:
            untested.append(r["account"])
            continue
        _, day, scores, flags = found
        renewals.append(dict(r, snapshot=day, scores=scores, flags=flags,
                             lost_arr=max(0.0, float(r["arr_before"]) - float(r["arr_after"]))))

    sets = [("Current weights", WEIGHTS)] + ([("Compare weights", compare)] if compare else [])
    results = [(label,) + evaluate(renewals, w) for label, w in sets]
    lost_count = sum(1 for r in renewals if r["outcome"] in LOST)

    out = ["# Health Score Back-test", "",
           f"Renewals due {start + timedelta(days=1)} to {args.as_of}, banded from the snapshot nearest "
           f"{args.lead_days} days before renewal (within {args.window_days} days). "
           f"{len(renewals)} of {len(due)} tested; {lost_count} lost or downgraded, "
           f"{money(results[0][2]['lost_arr'])} ARR lost.", ""]
    if untested:
        out += [f"Not tested, no snapshot in range: {', '.join(untested)}.", ""]
    for label, w in sets:
        out.append(f"- {label}: " + ", ".join(f"{k} {v:g}" for k, v in w.items()))
    out += ["", "## Summary", "", "| Measure | " + " | ".join(label for label, *_ in results) + " |",
            "|---|" + "---|" * len(results)]
    out.append("| Lost ARR flagged Red | " + " | ".join(
        f"{money(s['red'])} ({share(s['red'], s['lost_arr'])})" for _, _, s in results) + " |")
    out.append("| Lost ARR flagged Red or Yellow | " + " | ".join(
        f"{money(s['red_yellow'])} ({share(s['red_yellow'], s['lost_arr'])})" for _, _, s in results) + " |")
    out.append("| Lost while Green (misses) | " + " | ".join(
        f"{len(s['misses'])} ({money(sum(r['lost_arr'] for r in s['misses']))})" for _, _, s in results) + " |")
    out.append("| Red that renewed in full (false alarms) | " + " | ".join(
        str(len(s["false_alarms"])) for _, _, s in results) + " |")

    label, rows, stats = results[0]
    out += ["", f"## By band, {label.lower()}", "",
            "| Band 90 days before | Renewals | Renewed or expanded | Downgraded | Churned | ARR lost |",
            "|---|---|---|---|---|---|"]
    for band in BANDS:
        b = [r for r in rows if r["band"] == band]
        if not b:
            continue
        out.append(f"| {band} | {len(b)} | {sum(1 for r in b if r['outcome'] not in LOST)} | "
                   f"{sum(1 for r in b if r['outcome'] == 'Downgraded')} | "
                   f"{sum(1 for r in b if r['outcome'] == 'Churned')} | {money(sum(r['lost_arr'] for r in b))} |")

    out += ["", "## Misses to review", ""]
    if stats["misses"]:
        for r in stats["misses"]:
            out.append(f"- **{r['account']}**: Green on {r['snapshot']}, then {r['outcome'].lower()} "
                       f"({money(r['lost_arr'])}, `{r['reason'] or 'untagged'}`). Which signal should have caught it?")
    else:
        out.append(f"None with {label.lower()}.")
    if compare:
        changed = [(a, b) for a, b in zip(rows, results[1][1]) if a["band"] != b["band"]]
        out += ["", "## Bands that change with the compare weights", ""]
        out += [f"- {a['account']} ({a['outcome'].lower()}): {a['band']} with current weights, {b['band']} with compare weights"
                for a, b in changed] or ["None."]
    if len(renewals) < 30:
        out += ["", f"Only {len(renewals)} renewals were tested. Treat the rates as anecdotes until "
                    "there are at least 30, and change weights on patterns, not single accounts."]
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
