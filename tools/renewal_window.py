"""List the accounts renewing in the next N days, ready for the Pre-Renewal Check.

Scores the accounts with score_accounts.py, keeps those renewing within the
window, and writes the fields prompts/pre-renewal-check.md asks for, soonest
renewal first. It does not assign readiness statuses: that is the prompt's
job, and the CSM's call. Standard library only.

Usage:
    python3 tools/renewal_window.py sample-data/accounts.csv \
        --plans sample-data/success-plans.csv --as-of 2026-10-01 --days 120
"""

import argparse
import csv
import sys
from datetime import date

from outcome_progress import load_plans
from score_accounts import score_account

# Fields from the scored row, then fields carried over from the raw row.
SCORED_FIELDS = ["account_id", "account", "arr", "renewal_date", "days_to_renewal",
                 "band", "index", "overrides", "top_drivers", "goals"]
RAW_FIELDS = ["red_flags", "open_escalations", "days_since_exec_contact", "contract_flags", "notes"]
REQUIRED_COLUMNS = ["account_id", "account", "arr", "renewal_date", "licensed_seats", "active_users",
                    "usage_trend_90d_pct", "meetings_60d", "days_since_exec_contact",
                    "open_escalations", "ttr_trend", "nps_score", "csm_confidence",
                    "payment_days_late", "contract_flags", "red_flags", "prior_index", "expansion_signal", "notes"]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("accounts_csv")
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today(),
                        help="date to measure days to renewal from (YYYY-MM-DD)")
    parser.add_argument("--days", type=int, default=120,
                        help="include accounts renewing within this many days (default 120)")
    parser.add_argument("--plans", help="success plans CSV, the source of the Outcomes signal")
    args = parser.parse_args()

    plans = {}
    if args.plans:
        try:
            plans = load_plans(args.plans, args.as_of)
        except ValueError as e:
            sys.exit(str(e))
    else:
        print("warning: no --plans file, so Outcomes is missing and no account can be Green",
              file=sys.stderr)

    with open(args.accounts_csv, newline="") as f:
        reader = csv.DictReader(f)
        missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            sys.exit(f"{args.accounts_csv}: missing columns: {', '.join(missing)}")
        raw_rows = list(reader)

    rows, problems = [], []
    for raw in raw_rows:
        try:
            scored = score_account(raw, args.as_of, plans.get(raw["account_id"], []))
        except ValueError as e:
            problems.append(f"{raw['account_id']} ({raw['account']}): could not score: {e}")
            continue
        days = scored["days_to_renewal"]
        if days < 0:
            problems.append(f"{raw['account_id']} ({raw['account']}): renewal date {raw['renewal_date']} "
                            f"is before {args.as_of}; update it or check whether it renewed")
        elif days <= args.days:
            row = {field: scored[field] for field in SCORED_FIELDS}
            row.update({field: raw[field] for field in RAW_FIELDS})
            rows.append(row)
    rows.sort(key=lambda r: (r["days_to_renewal"], r["account"]))

    writer = csv.DictWriter(sys.stdout, fieldnames=SCORED_FIELDS + RAW_FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)

    total_arr = sum(r["arr"] for r in rows)
    print(f"{len(rows)} of {len(raw_rows)} accounts renew within {args.days} days of {args.as_of}, "
          f"${total_arr:,} ARR.", file=sys.stderr)
    for problem in problems:
        print(f"warning: {problem}", file=sys.stderr)
    if any("could not score" in p for p in problems):
        sys.exit(1)


if __name__ == "__main__":
    main()
