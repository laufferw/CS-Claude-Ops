# Sample Data

A fictional book of 12 accounts for one CSM, for trying the prompts and the scoring rubric without touching real data. Every company, person, and number is invented.

| File | What it is |
|---|---|
| [`accounts.csv`](accounts.csv) | Raw signals per account, the input to scoring |
| [`success-plans.csv`](success-plans.csv) | Success plan goals, one row per goal, with baselines and targets. The source of the Outcomes signal |
| [`roi-inputs.json`](roi-inputs.json) | Inputs for the [ROI calculator](../tools/README.md#roi-calculator) for a fictional 8-CSM team |
| [`scored-accounts.csv`](scored-accounts.csv) | The same accounts scored as of 2026-10-01, sorted by priority. The input to the [Weekly CSM Brief](../prompts/weekly-csm-brief.md) |

Regenerate the scored file after changing the data or the rubric:

```
python3 tools/score_accounts.py sample-data/accounts.csv --plans sample-data/success-plans.csv --as-of 2026-10-01 > sample-data/scored-accounts.csv
```

## Fields in `accounts.csv`

A blank field means unknown. Scoring treats it as missing, not as zero (see [missing data](../frameworks/account-health-scoring.md#missing-data)).

| Field | Meaning |
|---|---|
| `account_id`, `account`, `csm` | Identifiers |
| `arr` | Annual recurring revenue, in dollars |
| `renewal_date` | YYYY-MM-DD |
| `licensed_seats`, `active_users` | Seats sold, and average active users over 90 days |
| `usage_trend_90d_pct` | Change in active users over 90 days, in percent |
| `meetings_60d` | Customer meetings held in the last 60 days |
| `days_since_exec_contact` | Days since last contact with the executive sponsor, or `never` |
| `open_escalations` | Escalations currently open |
| `ttr_trend` | Time-to-resolution trend: `improving`, `flat`, or `worsening` |
| `nps_score` | Latest NPS response, 0 to 10 |
| `csm_confidence` | CSM's own rating, 1 to 5 |
| `payment_days_late` | Days the oldest open invoice is past due |
| `contract_flags` | Count of open contract concerns (described in `notes`) |
| `red_flags` | `non_renewal_notice`, `exec_sponsor_departed`, `payment_dispute`, separated by `\|` |
| `prior_index` | Last week's index, for detecting band moves |
| `expansion_signal`, `notes` | Free text |

## Fields in `success-plans.csv`

One row per goal. An account with no rows has no success plan. The rules that turn these fields into a goal status are in the [Outcome Library](../frameworks/outcome-library.md#measuring-progress).

| Field | Meaning |
|---|---|
| `account_id` | Matches `accounts.csv` |
| `outcome_id` | An ID from the [Outcome Library](../frameworks/outcome-library.md#the-library), or `custom` |
| `goal`, `customer_owner` | The goal in the customer's words, and who owns it on their side |
| `unit` | The metric's unit, for reading the report |
| `baseline_value`, `baseline_date` | The starting measurement. Blank means no baseline |
| `target_value`, `target_date` | Agreed with the customer owner. Required |
| `current_value`, `current_date` | The latest measurement. Both blank until the first one after the baseline |

## What the accounts exercise

| Account | Case |
|---|---|
| Cedar Health Partners | Band drop to Red, large ARR, renewal in 75 days |
| Granite Payroll | Sponsor departure caps a Green index at Yellow |
| Larkspur Retail | Payment dispute, missing NPS |
| Meridian Analytics | High index but Insufficient data (coverage 50%), no success plan |
| Orchard Learning | Healthy account renewing in 30 days |
| Pinecrest Manufacturing | Largest ARR, Yellow, expansion signal |
| Quarry Lane Media | Non-renewal notice, no exec contact ever |
| Riverbend Credit Union | Success plan gone stale: a Green index capped at Yellow by no measured outcomes |
| Sable Energy | Downgrade request, renewal in 91 days, one goal with no baseline |
| Tidewater Clinics | Low usage that is normal for the account, a custom goal |
| Cedar Health Partners, Quarry Lane Media, Willow Biotech | Goals that passed their target date unmet (Missed) |
| Bluefin Logistics, Orchard Learning, Willow Biotech | Healthy accounts, each with a goal already Met |
