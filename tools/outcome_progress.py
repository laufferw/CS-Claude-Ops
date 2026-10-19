"""Measure success plan goals against their baselines and targets.

Implements the progress, status, and adoption rules in
frameworks/outcome-library.md. Writes one row per goal, for QBRs and renewal
value stories, and gives score_accounts.py the goal statuses behind the
Outcomes signal. With --adoption, it also checks whether the features each
outcome depends on are in use. Standard library only.

Usage:
    python3 tools/outcome_progress.py sample-data/success-plans.csv \
        --adoption sample-data/feature-adoption.csv --as-of 2026-10-01
"""

import argparse
import csv
import sys
from datetime import date
from pathlib import Path

LIBRARY = Path(__file__).resolve().parent.parent / "frameworks" / "outcome-library.md"

STALE_DAYS = 60  # a goal not measured for longer than this is Stale
TOLERANCE = 0.25  # how far behind the straight line to target a goal can be and still be On track
MIN_GOALS, MAX_GOALS = 3, 4
SCORED_STATUSES = ("Met", "On track", "Off track", "Missed")
GOOD_STATUSES = ("Met", "On track")
LIGHT_USE = 40  # a feature used by fewer than this % of its target users is lightly used
READINGS = {  # (goal is Met or On track, features are in use) -> reading
    (True, True): "Proven",
    (True, False): "Unexplained progress",
    (False, False): "Adoption gap",
    (False, True): "Not converting",
}
REQUIRED_COLUMNS = ["account_id", "outcome_id", "goal", "customer_owner", "unit",
                    "baseline_value", "baseline_date", "target_value", "target_date",
                    "current_value", "current_date"]


def num(value):
    """Parse a number, or return None for a blank (unknown) field."""
    value = (value or "").strip()
    return None if value == "" else float(value)


def day(value):
    """Parse a YYYY-MM-DD date, or return None for a blank field."""
    value = (value or "").strip()
    return None if value == "" else date.fromisoformat(value)


def round_half_up(value):
    """Round .5 up, as a person scoring by hand would (Python's round() goes to even)."""
    return int(value + 0.5)


def goal_status(row, as_of):
    """Return progress, expected progress (both 0 to 1, or None), and status for one goal."""
    baseline, baseline_date = num(row["baseline_value"]), day(row["baseline_date"])
    target, target_date = num(row["target_value"]), day(row["target_date"])
    current, current_date = num(row["current_value"]), day(row["current_date"])
    if target is None or target_date is None:
        raise ValueError("target_value and target_date are required")
    if (current is None) != (current_date is None):
        raise ValueError("current_value and current_date must both be set or both be blank")

    if baseline is None or baseline_date is None:
        return None, None, "No baseline"
    if target == baseline:
        raise ValueError("target_value equals baseline_value, so progress cannot be measured")
    if target_date <= baseline_date:
        raise ValueError("target_date must be after baseline_date")

    # Before the first measurement, the latest reading is the baseline itself.
    if current is None:
        current, current_date = baseline, baseline_date
    if (as_of - current_date).days > STALE_DAYS:
        return None, None, "Stale"

    progress = (current - baseline) / (target - baseline)
    elapsed = (current_date - baseline_date).days / (target_date - baseline_date).days
    expected = max(0.0, min(1.0, elapsed))
    if progress >= 1:
        status = "Met"
    elif as_of > target_date:
        status = "Missed"
    elif progress >= expected - TOLERANCE:
        status = "On track"
    else:
        status = "Off track"
    return progress, expected, status


def load_plans(path, as_of):
    """Read a success plans CSV. Return {account_id: [goal rows with progress and status]}."""
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"{path}: missing columns: {', '.join(missing)}")
        plans = {}
        for line, row in enumerate(reader, start=2):
            try:
                progress, expected, status = goal_status(row, as_of)
            except ValueError as e:
                raise ValueError(f"{path} line {line} ({row['account_id']}, {row['outcome_id']}): {e}")
            plans.setdefault(row["account_id"], []).append(
                dict(row, progress=progress, expected=expected, status=status))
    return plans


def load_library(path=LIBRARY):
    """Read the library table. Return {outcome_id: {"name": ..., "features": [...]}}."""
    library, columns = {}, None
    for line in Path(path).read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells[:2] == ["ID", "Outcome"]:
            columns = cells
        elif columns and len(cells) == len(columns) and cells[0].startswith("OL-"):
            row = dict(zip(columns, cells))
            features = [f.strip().lower() for f in row["Depends on"].split(",")]
            library[row["ID"]] = {"name": row["Outcome"], "features": features}
    if not library:
        raise ValueError(f"{path}: no outcome table found")
    return library


def load_adoption(path):
    """Read a feature adoption CSV. Return {account_id: {feature: adoption %}}."""
    adoption = {}
    with open(path, newline="") as f:
        for line, row in enumerate(csv.DictReader(f), start=2):
            pct_used = num(row["adoption_pct"])
            if pct_used is None:
                raise ValueError(f"{path} line {line}: adoption_pct is blank")
            adoption.setdefault(row["account_id"], {})[row["feature"].strip().lower()] = pct_used
    return adoption


def add_support(plans, library, adoption):
    """Add support, light_features, and reading to each goal, in place."""
    for account_id, goals in plans.items():
        used = adoption.get(account_id, {})
        for goal in goals:
            outcome = library.get(goal["outcome_id"])
            if outcome is None:  # custom goal: no feature link to check
                goal.update(support="n/a", light_features="", reading="")
                continue
            measured = {f: used[f] for f in outcome["features"] if f in used}
            light = [f for f, value in measured.items() if value < LIGHT_USE]
            if not measured:
                support = "Unknown"
            else:
                support = "Supported" if len(measured) - len(light) > len(measured) / 2 else "Unsupported"
            reading = ""
            if support in ("Supported", "Unsupported") and goal["status"] in SCORED_STATUSES:
                reading = READINGS[(goal["status"] in GOOD_STATUSES, support == "Supported")]
            goal.update(support=support, reading=reading,
                        light_features="; ".join(f"{f} {round_half_up(measured[f])}%" for f in light))


def summarize(goals):
    """One-line goal summary, such as '2 of 3 on track; 1 no baseline'."""
    scored = [g for g in goals if g["status"] in SCORED_STATUSES]
    good = sum(1 for g in scored if g["status"] in GOOD_STATUSES)
    parts = [f"{good} of {len(scored)} on track"] if scored else []
    for status in ("No baseline", "Stale"):
        count = sum(1 for g in goals if g["status"] == status)
        if count:
            parts.append(f"{count} {status.lower()}")
    return "; ".join(parts) or "no success plan"


def pct(value):
    return "" if value is None else round_half_up(100 * value)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("plans_csv")
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today(),
                        help="date to judge staleness and missed targets from (YYYY-MM-DD)")
    parser.add_argument("--adoption", help="feature adoption CSV, to check the features behind each goal")
    parser.add_argument("--library", default=LIBRARY, help="the Outcome Library markdown file")
    args = parser.parse_args()

    try:
        plans = load_plans(args.plans_csv, args.as_of)
        if args.adoption:
            add_support(plans, load_library(args.library), load_adoption(args.adoption))
    except ValueError as e:
        sys.exit(str(e))

    fields = ["account_id", "outcome_id", "goal", "customer_owner", "unit", "baseline_value",
              "target_value", "target_date", "current_value", "current_date",
              "progress_pct", "expected_pct", "status"]
    if args.adoption:
        fields += ["support", "light_features", "reading"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    for account_id, goals in plans.items():
        for goal in goals:
            writer.writerow(dict(goal, progress_pct=pct(goal["progress"]), expected_pct=pct(goal["expected"])))
        if not MIN_GOALS <= len(goals) <= MAX_GOALS:
            print(f"warning: {account_id} has {len(goals)} goals; a success plan holds "
                  f"{MIN_GOALS} to {MAX_GOALS}", file=sys.stderr)

    counts = {}
    for goals in plans.values():
        for goal in goals:
            counts[goal["status"]] = counts.get(goal["status"], 0) + 1
    summary = ", ".join(f"{counts[s]} {s.lower()}" for s in (*SCORED_STATUSES, "No baseline", "Stale") if s in counts)
    print(f"{len(plans)} accounts, {sum(counts.values())} goals: {summary}", file=sys.stderr)


if __name__ == "__main__":
    main()
