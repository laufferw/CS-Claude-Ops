"""Score accounts with the Account Success Index.

Implements the rubric in frameworks/account-health-scoring.md and the
priority formula in prompts/weekly-csm-brief.md. Standard library only.

Usage:
    python3 tools/score_accounts.py sample-data/accounts.csv --as-of 2026-10-01 > scored.csv
"""

import argparse
import csv
import sys
from datetime import date

WEIGHTS = {
    "usage": 30,
    "outcomes": 20,
    "engagement": 15,
    "support": 15,
    "sentiment": 10,
    "commercial": 10,
}
MIN_COVERAGE = 70  # percent of total weight that must be scored
BAND_ORDER = {"Red": 0, "Yellow": 1, "Green": 2}
RISK_WEIGHT = {"Red": 1.0, "Yellow": 0.5, "Insufficient data": 0.5, "Green": 0.1}


def num(value):
    """Parse a number, or return None for a blank (unknown) field."""
    value = (value or "").strip()
    return None if value == "" else float(value)


def round_half_up(value):
    """Round .5 up, as a person scoring by hand would (Python's round() goes to even)."""
    return int(value + 0.5)


def clamp(score):
    return max(0, min(100, score))


def score_usage(row):
    seats, active = num(row["licensed_seats"]), num(row["active_users"])
    if not seats or active is None:
        return None
    utilization = active / seats
    if utilization >= 0.8:
        score = 100
    elif utilization >= 0.6:
        score = 75
    elif utilization >= 0.4:
        score = 50
    elif utilization >= 0.2:
        score = 25
    else:
        score = 0
    trend = num(row["usage_trend_90d_pct"])
    if trend is not None:
        if trend >= 10:
            score += 10
        elif trend <= -25:
            score -= 30
        elif trend <= -10:
            score -= 15
    return clamp(score)


def score_engagement(row):
    meetings = num(row["meetings_60d"])
    exec_days = row["days_since_exec_contact"].strip()
    if meetings is None or exec_days == "":
        return None
    if meetings >= 3:
        score = 60
    elif meetings == 2:
        score = 45
    elif meetings == 1:
        score = 25
    else:
        score = 0
    if exec_days != "never":
        days = float(exec_days)
        if days <= 30:
            score += 40
        elif days <= 60:
            score += 25
        elif days <= 90:
            score += 10
    return clamp(score)


def score_support(row):
    escalations = num(row["open_escalations"])
    if escalations is None:
        return None
    score = 100 - 25 * min(escalations, 3)
    if row["ttr_trend"].strip() == "worsening":
        score -= 25
    return clamp(score)


def score_sentiment(row):
    parts = []
    nps = num(row["nps_score"])
    if nps is not None:
        if nps >= 9:
            parts.append(100)
        elif nps >= 7:
            parts.append(70)
        elif nps >= 5:
            parts.append(30)
        else:
            parts.append(0)
    confidence = num(row["csm_confidence"])
    if confidence is not None:
        parts.append((confidence - 1) * 25)
    return sum(parts) / len(parts) if parts else None


def score_commercial(row):
    late, flags = num(row["payment_days_late"]), num(row["contract_flags"])
    if late is None or flags is None:
        return None
    if late == 0:
        penalty = 0
    elif late <= 30:
        penalty = 20
    elif late <= 60:
        penalty = 40
    else:
        penalty = 60
    return clamp(100 - penalty - 20 * flags)


def score_outcomes(row):
    total, on_track = num(row["goals_total"]), num(row["goals_on_track"])
    if not total or on_track is None:
        return None
    return clamp(100 * on_track / total)


SCORERS = {
    "usage": score_usage,
    "outcomes": score_outcomes,
    "engagement": score_engagement,
    "support": score_support,
    "sentiment": score_sentiment,
    "commercial": score_commercial,
}


def band_for(index):
    if index >= 75:
        return "Green"
    if index >= 50:
        return "Yellow"
    return "Red"


def urgency_for(days_to_renewal):
    if days_to_renewal <= 90:
        return 1.0
    if days_to_renewal <= 180:
        return 0.6
    return 0.3


def score_account(row, as_of):
    scores = {name: scorer(row) for name, scorer in SCORERS.items()}
    scored = {name: s for name, s in scores.items() if s is not None}
    missing = [name for name in WEIGHTS if name not in scored]
    coverage = sum(WEIGHTS[name] for name in scored)
    index = round_half_up(sum(s * WEIGHTS[name] for name, s in scored.items()) / coverage) if coverage else None

    band = band_for(index) if coverage >= MIN_COVERAGE else "Insufficient data"
    overrides = []
    red_flags = [f for f in row["red_flags"].split("|") if f.strip()]
    if "non_renewal_notice" in red_flags:
        band = "Red"
        overrides.append("non_renewal_notice -> Red")
    for flag in ("exec_sponsor_departed", "payment_dispute"):
        if flag in red_flags and band == "Green":
            band = "Yellow"
            overrides.append(f"{flag} -> capped at Yellow")
        elif flag in red_flags:
            overrides.append(f"{flag} (band already {band})")

    gaps = sorted(
        ((WEIGHTS[name] * (100 - s), name, s) for name, s in scored.items() if s < 100),
        reverse=True,
    )
    drivers = [f"{name} ({round_half_up(s)})" for _, name, s in gaps[:2]]

    prior = num(row["prior_index"])
    prior_band = band_for(prior) if prior is not None else ""
    if band in BAND_ORDER and prior_band:
        delta = BAND_ORDER[band] - BAND_ORDER[prior_band]
        band_change = "down" if delta < 0 else "up" if delta > 0 else "same"
    else:
        band_change = "n/a"

    days_to_renewal = (date.fromisoformat(row["renewal_date"]) - as_of).days
    arr = float(row["arr"])
    priority = round_half_up(arr * RISK_WEIGHT[band] * urgency_for(days_to_renewal))

    result = {
        "account_id": row["account_id"],
        "account": row["account"],
        "arr": int(arr),
        "renewal_date": row["renewal_date"],
        "days_to_renewal": days_to_renewal,
    }
    for name in WEIGHTS:
        result[f"{name}_score"] = "" if scores[name] is None else round_half_up(scores[name])
    result.update({
        "coverage_pct": coverage,
        "index": "" if index is None else index,
        "band": band,
        "prior_index": "" if prior is None else int(prior),
        "prior_band": prior_band,
        "band_change": band_change,
        "overrides": "; ".join(overrides),
        "missing_signals": "|".join(missing),
        "top_drivers": "; ".join(drivers),
        "priority": priority,
        "expansion_signal": row["expansion_signal"],
        "notes": row["notes"],
    })
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("accounts_csv")
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today(),
                        help="date to measure days to renewal from (YYYY-MM-DD)")
    args = parser.parse_args()

    with open(args.accounts_csv, newline="") as f:
        rows = [score_account(row, args.as_of) for row in csv.DictReader(f)]
    rows.sort(key=lambda r: r["priority"], reverse=True)

    writer = csv.DictWriter(sys.stdout, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)


if __name__ == "__main__":
    main()
