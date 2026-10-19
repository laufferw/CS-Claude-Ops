"""Report the value a book of accounts has realized from its success plans.

Rolls up every goal's status and adoption reading (from outcome_progress.py)
into the book-level report described in specs/adoption-as-a-service.md:
how many goals are met or on track, which are proven, the customer-agreed
value of proven goals, and what the outcome review should look at. Writes
markdown to stdout. Standard library only.

Usage:
    python3 tools/value_report.py sample-data/accounts.csv \
        --plans sample-data/success-plans.csv \
        --adoption sample-data/feature-adoption.csv --as-of 2026-10-01
"""

import argparse
import csv
import sys
from datetime import date
from statistics import median

from outcome_progress import (GOOD_STATUSES, LIBRARY, SCORED_STATUSES, add_support,
                              load_adoption, load_library, load_plans, round_half_up)

PATTERN_ACCOUNTS = 2  # an outcome Not converting at this many accounts goes to Product
READING_COLUMNS = ["Proven", "Unexplained progress", "Adoption gap", "Not converting"]


def number(value):
    """Format a measurement without float noise: 2.2, not 2.2000000000000002."""
    return f"{round(value, 2):g}"


def improvement(goal):
    """Units improved since baseline, positive when moving toward the target, or None."""
    if goal["progress"] is None:
        return None
    baseline, target = float(goal["baseline_value"]), float(goal["target_value"])
    return goal["progress"] * abs(target - baseline)


def why_not_proven(goal):
    if goal.get("reading"):
        return goal["reading"]
    if goal.get("support") == "Unknown":
        return "no adoption data"
    if goal.get("support") == "n/a":
        return "custom goal, no feature link"
    return "no adoption file" if "support" not in goal else goal["status"]


def build_report(accounts, plans, library, adoption_given, as_of):
    names = {a["account_id"]: a["account"] for a in accounts}
    arr = {a["account_id"]: float(a["arr"]) for a in accounts}
    goals = [g for gs in plans.values() for g in gs]
    counted = [g for g in goals if g["status"] in SCORED_STATUSES]
    good = [g for g in counted if g["status"] in GOOD_STATUSES]
    proven = [g for g in goals if g.get("reading") == "Proven"]
    proven_accounts = {g["account_id"] for g in proven}
    planned = [a for a in plans if a in names]

    valued = [g for g in goals if (g.get("annual_value_per_unit") or "").strip()]
    proven_value = sum(improvement(g) * float(g["annual_value_per_unit"])
                       for g in valued if g.get("reading") == "Proven")

    def share(part, whole):
        return f"{round_half_up(100 * part / whole)}%" if whole else "n/a"

    stale = sum(1 for g in goals if g["status"] == "Stale")
    no_baseline = sum(1 for g in goals if g["status"] == "No baseline")
    unknown = sum(1 for g in goals if g.get("support") == "Unknown")

    out = [f"# Outcome Value Report", "",
           f"As of {as_of}. {len(accounts)} accounts, {len(planned)} with a success plan.", "",
           "## Book summary", "",
           "| Measure | Value |", "|---|---|",
           f"| Accounts with a success plan | {len(planned)} of {len(accounts)} "
           f"(${sum(arr[a] for a in planned):,.0f} of ${sum(arr.values()):,.0f} ARR) |",
           f"| Goals counted (baseline and a recent measurement) | {len(counted)} of {len(goals)} |",
           f"| Met or on track | {len(good)} ({share(len(good), len(counted))} of counted) |",
           f"| Proven: met or on track, with the features behind it in use | {len(proven)} ({share(len(proven), len(counted))} of counted) |",
           f"| ARR on accounts with at least one proven outcome | ${sum(arr.get(a, 0) for a in proven_accounts):,.0f} "
           f"({share(sum(arr.get(a, 0) for a in proven_accounts), sum(arr.values()))}) |",
           f"| Customer-agreed annual value, proven goals only | ${proven_value:,.0f} |",
           f"| Data gaps | {stale} stale, {no_baseline} with no baseline, {unknown} with no adoption data |",
           ""]
    if not adoption_given:
        out += ["No adoption file was given, so no goal can be proven. Run with `--adoption`.", ""]

    out += ["## By outcome", "",
            "| ID | Outcome | Plans | Met | On track | Off track | Missed | Median progress | "
            + " | ".join(READING_COLUMNS) + " |",
            "|---|---|---|---|---|---|---|---|" + "---|" * len(READING_COLUMNS)]
    for outcome_id in [*library, "custom"]:
        picked = [g for g in goals if g["outcome_id"] == outcome_id]
        if not picked:
            continue
        name = library[outcome_id]["name"] if outcome_id in library else "Custom goals"
        counts = [sum(1 for g in picked if g["status"] == s) for s in SCORED_STATUSES]
        progress = [g["progress"] for g in picked if g["status"] in SCORED_STATUSES]
        mid = f"{round_half_up(100 * median(progress))}%" if progress else "n/a"
        readings = [sum(1 for g in picked if g.get("reading") == r) for r in READING_COLUMNS]
        out.append(f"| {outcome_id} | {name} | {len(picked)} | " + " | ".join(map(str, counts))
                   + f" | {mid} | " + " | ".join(map(str, readings)) + " |")
    out.append("")

    out += ["## Customer-agreed value", "",
            "Only goals whose customer agreed what one unit of improvement is worth. "
            "The total counts proven goals only.", ""]
    if valued:
        out += ["| Account | Outcome | Improvement | Annual value | Counted |", "|---|---|---|---|---|"]
        for g in valued:
            gained = improvement(g)
            if gained is None:
                out.append(f"| {names.get(g['account_id'], g['account_id'])} | {g['outcome_id']} | n/a | n/a | No: {g['status']} |")
                continue
            value = gained * float(g["annual_value_per_unit"])
            counted_as = "Yes" if g.get("reading") == "Proven" else f"No: {why_not_proven(g)}"
            out.append(f"| {names.get(g['account_id'], g['account_id'])} | {g['outcome_id']} | "
                       f"{number(gained)} {g['unit']} | ${value:,.0f} | {counted_as} |")
        out += [f"| **Total counted** | | | **${proven_value:,.0f}** | |", ""]
    else:
        out += ["None.", ""]

    out += ["## For the outcome review", ""]
    not_converting = {}
    for g in goals:
        if g.get("reading") == "Not converting":
            not_converting.setdefault(g["outcome_id"], []).append(names.get(g["account_id"], g["account_id"]))
    patterns = {o: a for o, a in not_converting.items() if len(set(a)) >= PATTERN_ACCOUNTS}
    singles = sum(len(a) for o, a in not_converting.items() if o not in patterns)
    if patterns:
        lines = [f"{o} {library[o]['name']} ({', '.join(sorted(set(a)))})" for o, a in sorted(patterns.items())]
        out.append(f"- **Product:** not converting at {PATTERN_ACCOUNTS} or more accounts: " + "; ".join(lines)
                   + f". {singles} more goals are not converting at a single account.")
    else:
        out.append(f"- **Product:** no outcome is not converting at {PATTERN_ACCOUNTS} or more accounts. "
                   f"{singles} goals are not converting at a single account.")

    light = {}
    for g in goals:
        if g.get("reading") == "Adoption gap":
            for part in filter(None, g["light_features"].split("; ")):
                light.setdefault(part.rsplit(" ", 1)[0], set()).add(g["account_id"])
    ranked = sorted(light.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    out.append("- **Adoption:** lightly used features behind adoption gaps, by accounts affected: "
               + (", ".join(f"{f} ({len(a)})" for f, a in ranked) or "none") + ".")

    proof = [g for g in proven if g["status"] == "Met"]
    out.append("- **Marketing:** met and proven goals, candidates for a proof point with the customer's written permission: "
               + ("; ".join(f"{names.get(g['account_id'], g['account_id'])}, {g['outcome_id']}: "
                            f"{g['baseline_value']} to {g['current_value']} {g['unit']}" for g in proof) or "none") + ".")

    unexplained = [g for g in goals if g.get("reading") == "Unexplained progress"]
    out.append("- **Unexplained progress:** do not claim these until the cause is known: "
               + ("; ".join(f"{names.get(g['account_id'], g['account_id'])}, {g['outcome_id']}" for g in unexplained)
                  or "none") + ".")
    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("accounts_csv")
    parser.add_argument("--plans", required=True, help="success plans CSV")
    parser.add_argument("--adoption", help="feature adoption CSV, needed to prove any goal")
    parser.add_argument("--library", default=LIBRARY, help="the Outcome Library markdown file")
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today(),
                        help="date to judge staleness and missed targets from (YYYY-MM-DD)")
    args = parser.parse_args()

    try:
        with open(args.accounts_csv, newline="") as f:
            accounts = list(csv.DictReader(f))
        plans = load_plans(args.plans, args.as_of)
        library = load_library(args.library)
        if args.adoption:
            add_support(plans, library, load_adoption(args.adoption))
        else:
            print("warning: no --adoption file, so no goal can be proven", file=sys.stderr)
    except ValueError as e:
        sys.exit(str(e))

    unknown = sorted(set(plans) - {a["account_id"] for a in accounts})
    if unknown:
        print(f"warning: success plans for accounts not in {args.accounts_csv}: {', '.join(unknown)}",
              file=sys.stderr)
    sys.stdout.write(build_report(accounts, plans, library, bool(args.adoption), args.as_of))


if __name__ == "__main__":
    main()
