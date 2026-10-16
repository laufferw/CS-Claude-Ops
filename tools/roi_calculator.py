"""Estimate first-year ROI of running a CS team with an AI copilot.

Benefits come from two sources, reported separately:
- Retained ARR: churn avoided through earlier risk detection. This is cash.
- Capacity freed: CSM hours saved, valued at loaded cost. This is only
  worth money if the hours are redeployed (more accounts per CSM, or
  hires avoided), so it is never folded into the cash ROI.

Benefits start after a ramp period (adoption takes time, and retained ARR
only lands at renewal), so first-year benefits cover 12 - ramp months.

Each scenario applies a realization rate to both benefits: the share of
the estimated savings that actually happens once adoption is uneven.
Standard library only.

Usage:
    python3 tools/roi_calculator.py sample-data/roi-inputs.json
"""

import argparse
import json


def money(value):
    sign = "-" if value < 0 else ""
    return f"{sign}${abs(value):,.0f}"


def ratio(numerator, denominator):
    return f"{numerator / denominator:.1f}x" if denominator else "n/a"


def payback_months(ramp, one_time, monthly_recurring_cost, monthly_benefit):
    """Months until cumulative net benefit turns positive.

    Costs run from month 0. Benefits start after the ramp.
    """
    monthly_net = monthly_benefit - monthly_recurring_cost
    if monthly_net <= 0:
        return "never"
    sunk = one_time + monthly_recurring_cost * ramp
    return f"{ramp + sunk / monthly_net:.1f}"


def scenario(inputs, realization):
    team, retention, costs = inputs["team"], inputs["retention"], inputs["costs"]
    csms = team["csm_count"]
    rate = team["loaded_cost_per_hour"]
    ramp = inputs.get("ramp_months", 0)
    year_one_share = (12 - ramp) / 12

    hours_per_csm_week = sum(t["hours_before"] - t["hours_after"] for t in inputs["time_savings"])
    hours_per_year = hours_per_csm_week * csms * team["working_weeks_per_year"] * realization
    capacity_value = hours_per_year * rate

    churned_arr = retention["arr_under_management"] * retention["gross_churn_rate_pct"] / 100
    retained_arr = churned_arr * retention["churn_reduction_pct"] / 100 * realization

    recurring_cost = (costs["license_per_user_per_month"] * csms
                      + costs["admin_hours_per_month"] * rate) * 12
    one_time = costs["one_time_implementation"]
    total_cost = recurring_cost + one_time

    annual_capacity, annual_retained = capacity_value, retained_arr
    monthly_recurring = recurring_cost / 12
    hours_per_year *= year_one_share
    capacity_value *= year_one_share
    retained_arr *= year_one_share

    return {
        "hours_freed": hours_per_year,
        "fte_freed": hours_per_year / (40 * team["working_weeks_per_year"]),
        "capacity_value": capacity_value,
        "retained_arr": retained_arr,
        "total_cost": total_cost,
        "cash_net": retained_arr - total_cost,
        "cash_roi": ratio(retained_arr - total_cost, total_cost),
        "cash_payback": payback_months(ramp, one_time, monthly_recurring, annual_retained / 12),
        "full_net": retained_arr + capacity_value - total_cost,
        "full_roi": ratio(retained_arr + capacity_value - total_cost, total_cost),
        "full_payback": payback_months(ramp, one_time, monthly_recurring,
                                       (annual_retained + annual_capacity) / 12),
    }


ROWS = [
    ("CSM hours freed in year one", "hours_freed", lambda v: f"{v:,.0f}"),
    ("Equivalent full-time CSMs", "fte_freed", lambda v: f"{v:.2f}"),
    ("Value of capacity freed", "capacity_value", money),
    ("Retained ARR (cash)", "retained_arr", money),
    ("First-year cost", "total_cost", money),
    ("Cash net benefit", "cash_net", money),
    ("Cash ROI", "cash_roi", str),
    ("Cash payback (months)", "cash_payback", str),
    ("Net benefit incl. capacity", "full_net", money),
    ("ROI incl. capacity", "full_roi", str),
    ("Payback incl. capacity (months)", "full_payback", str),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("inputs_json")
    args = parser.parse_args()

    with open(args.inputs_json) as f:
        inputs = json.load(f)
    scenarios = inputs["scenarios"]
    results = {name: scenario(inputs, rate) for name, rate in scenarios.items()}

    headers = ["Measure"] + [f"{name} ({rate:.0%})" for name, rate in scenarios.items()]
    print("| " + " | ".join(headers) + " |")
    print("|" + "---|" * len(headers))
    for label, key, fmt in ROWS:
        print("| " + " | ".join([label] + [fmt(results[name][key]) for name in scenarios]) + " |")
    print()
    print(f"Year one, with benefits starting after a {inputs.get('ramp_months', 0)}-month ramp.")
    print("Percentages are realization rates: the share of estimated savings that actually happens.")
    print("ROI is net benefit / cost. Capacity is worth money only if the hours are redeployed.")


if __name__ == "__main__":
    main()
