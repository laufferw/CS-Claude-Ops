"""Roll a scored book up by CSM: health, renewals, outcomes, data gaps, and workload.

Gives a CS director one table across the team, and applies the capacity
model in frameworks/capacity-model.md to show each CSM's weekly workload,
their utilization, and the headcount the book needs. Writes markdown to
stdout. Standard library only.

Usage:
    python3 tools/team_rollup.py sample-data/accounts.csv \
        --plans sample-data/success-plans.csv \
        --adoption sample-data/feature-adoption.csv \
        --capacity sample-data/capacity-inputs.json --as-of 2026-10-01
"""

import argparse
import json
import sys
from datetime import date

from outcome_progress import GOOD_STATUSES, SCORED_STATUSES, add_support, load_adoption, load_library
from score_accounts import load_book

RED_FLAGS = ("non_renewal_notice", "exec_sponsor_departed", "payment_dispute")
RENEWAL_WINDOW = 120
OVER, UNDER = 1.0, 0.5  # flag utilization above target, or below half of target


def at_risk(raw, scored):
    flags = [f for f in raw["red_flags"].split("|") if f.strip()]
    return scored["band"] == "Red" or any(f in RED_FLAGS for f in flags)


def account_hours(raw, scored, capacity):
    """Weekly CSM hours this account needs, and its segment name."""
    arr = float(raw["arr"])
    segment = next(s for s in sorted(capacity["segments"], key=lambda s: -s["min_arr"]) if arr >= s["min_arr"])
    hours = segment["hours"]
    extra = capacity.get("extra_hours", {})
    if at_risk(raw, scored):
        hours += extra.get("at_risk", 0)
    if 0 <= scored["days_to_renewal"] <= RENEWAL_WINDOW:
        hours += extra.get("renewal_within_120_days", 0)
    return hours, segment["name"]


def build_rollup(raw_rows, scored_rows, plans, capacity):
    """Return ({csm: stats}, team totals)."""
    by_csm = {}
    for raw, scored in zip(raw_rows, scored_rows):
        s = by_csm.setdefault(raw["csm"] or "(unassigned)", {
            "accounts": 0, "arr": 0.0, "Green": 0, "Yellow": 0, "Red": 0, "Insufficient data": 0,
            "band_drops": 0, "arr_at_risk": 0.0, "renewals": 0, "renewal_arr": 0.0,
            "goals_good": 0, "goals_counted": 0, "proven": 0, "data_gaps": 0, "hours": 0.0})
        arr = float(raw["arr"])
        goals = plans.get(raw["account_id"], [])
        s["accounts"] += 1
        s["arr"] += arr
        s[scored["band"]] += 1
        s["band_drops"] += scored["band_change"] == "down"
        if at_risk(raw, scored):
            s["arr_at_risk"] += arr
        if 0 <= scored["days_to_renewal"] <= RENEWAL_WINDOW:
            s["renewals"] += 1
            s["renewal_arr"] += arr
        s["goals_counted"] += sum(1 for g in goals if g["status"] in SCORED_STATUSES)
        s["goals_good"] += sum(1 for g in goals if g["status"] in GOOD_STATUSES)
        s["proven"] += sum(1 for g in goals if g.get("reading") == "Proven")
        gap = scored["missing_signals"] or any(g["status"] in ("Stale", "No baseline") for g in goals)
        s["data_gaps"] += bool(gap)
        if capacity:
            s["hours"] += account_hours(raw, scored, capacity)[0]

    team = {key: sum(s[key] for s in by_csm.values()) for key in next(iter(by_csm.values()))}
    if capacity:
        weekly = capacity["hours_per_csm_per_week"]
        target = capacity["target_utilization_pct"] / 100
        for s in [*by_csm.values(), team]:
            s["utilization"] = s["hours"] / weekly
        team["utilization"] = team["hours"] / (weekly * len(by_csm))
        team["csms_needed"] = team["hours"] / (weekly * target)
    return by_csm, team


def money(value):
    return f"${value:,.0f}"


def pct(value):
    return f"{round(100 * value)}%"


def render(by_csm, team, capacity, as_of):
    show_capacity = bool(capacity)
    head = ["CSM", "Accounts", "ARR", "Green / Yellow / Red / Insufficient", "Band drops", "ARR at risk",
            f"Renewals in {RENEWAL_WINDOW} days", "Goals on track", "Proven", "Accounts with data gaps"]
    if show_capacity:
        head += ["Hours per week", "Utilization"]
    out = ["# Team Rollup", "", f"As of {as_of}. {len(by_csm)} CSMs, {team['accounts']} accounts, {money(team['arr'])} ARR.", "",
           "| " + " | ".join(head) + " |", "|" + "---|" * len(head)]

    def line(name, s, bold=False):
        cells = [name, s["accounts"], money(s["arr"]),
                 f"{s['Green']} / {s['Yellow']} / {s['Red']} / {s['Insufficient data']}",
                 s["band_drops"], money(s["arr_at_risk"]), f"{s['renewals']} ({money(s['renewal_arr'])})",
                 f"{s['goals_good']} of {s['goals_counted']}", s["proven"], s["data_gaps"]]
        if show_capacity:
            cells += [f"{s['hours']:g}", pct(s["utilization"])]
        cells = [f"**{c}**" if bold else str(c) for c in cells]
        return "| " + " | ".join(cells) + " |"

    for name in sorted(by_csm, key=lambda n: -by_csm[n]["arr_at_risk"]):
        out.append(line(name, by_csm[name]))
    out.append(line("Team", team, bold=True))

    if show_capacity:
        target = capacity["target_utilization_pct"] / 100
        out += ["", "## Capacity", "",
                f"The book needs {team['hours']:g} CSM hours a week. At {capacity['hours_per_csm_per_week']} hours "
                f"per CSM and a target utilization of {capacity['target_utilization_pct']}%, that is "
                f"{team['csms_needed']:.1f} CSMs, against {len(by_csm)} today."]
        over = [n for n, s in by_csm.items() if s["utilization"] > target * OVER]
        under = [n for n, s in by_csm.items() if s["utilization"] < target * UNDER]
        if over:
            out.append(f"Over target: {', '.join(sorted(over))}. Move accounts or add capacity.")
        if under:
            out.append(f"Under half of target: {', '.join(sorted(under))}. Room to take accounts.")
    return "\n".join(out) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("accounts_csv")
    parser.add_argument("--plans", help="success plans CSV")
    parser.add_argument("--adoption", help="feature adoption CSV, to count proven goals")
    parser.add_argument("--capacity", help="capacity model JSON, for workload and utilization")
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today(),
                        help="date to score as of (YYYY-MM-DD)")
    args = parser.parse_args()
    try:
        raw, scored, plans = load_book(args.accounts_csv, args.plans, args.as_of)
        if args.adoption:
            add_support(plans, load_library(), load_adoption(args.adoption))
        capacity = json.load(open(args.capacity)) if args.capacity else None
    except ValueError as e:
        sys.exit(str(e))
    by_csm, team = build_rollup(raw, scored, plans, capacity)
    sys.stdout.write(render(by_csm, team, capacity, args.as_of))


if __name__ == "__main__":
    main()
