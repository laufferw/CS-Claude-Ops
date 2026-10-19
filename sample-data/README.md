# Sample Data

A fictional book of 12 accounts across a team of three CSMs, for trying the prompts and tools without touching real data. Every company, person, and number is invented.

| CSM | Accounts |
|---|---|
| Sam Example | Cedar Health Partners, Granite Payroll, Larkspur Retail, Quarry Lane Media, Riverbend Credit Union, Sable Energy |
| Priya Example | Bluefin Logistics, Meridian Analytics, Pinecrest Manufacturing |
| Jordan Example | Orchard Learning, Tidewater Clinics, Willow Biotech |

| File | What it is |
|---|---|
| [`accounts.csv`](accounts.csv) | Raw signals per account, the input to scoring |
| [`success-plans.csv`](success-plans.csv) | Success plan goals, one row per goal, with baselines and targets. The source of the Outcomes signal |
| [`feature-adoption.csv`](feature-adoption.csv) | Adoption of each feature per account, for the [adoption check](../frameworks/outcome-library.md#checking-adoption-behind-each-outcome) |
| [`forecast-calls.csv`](forecast-calls.csv) | Each CSM's forecast call and expected ARR, for the [renewal forecast](../tools/README.md#renewal-forecast) |
| [`renewal-history.csv`](renewal-history.csv) | Renewals due in the past, with ARR before and after, for retention in the [scorecard](../tools/README.md#cs-scorecard) |
| [`score-history.csv`](score-history.csv) | Signal scores from past scoring runs, about 90 days before each past renewal, for the [back-test](../tools/README.md#back-test) |
| [`forecast-history.csv`](forecast-history.csv) | Each past renewal's forecast at the start of its quarter, and what renewed, for the [forecast back-test](../tools/README.md#forecast-back-test) |
| [`capacity-inputs.json`](capacity-inputs.json) | Hours per account and per CSM, for the [Capacity Model](../frameworks/capacity-model.md) |
| [`exports/`](exports/mapping.json) | Three raw exports (CRM, product usage, support) and the mapping that imports them to `accounts.csv`. See [Connect Your Data](../playbooks/connect-your-data.md) |
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
| `annual_value_per_unit` | Optional. What the customer agrees one unit of improvement is worth per year, in dollars. Blank unless agreed |

## Fields in `feature-adoption.csv`

One row per account and feature. A feature with no row has no adoption data.

| Field | Meaning |
|---|---|
| `account_id` | Matches `accounts.csv` |
| `feature` | A feature named in the library's "Depends on" column (case doesn't matter) |
| `adoption_pct` | Share of the feature's target users who used it for real work in the last 30 days |

## Fields in `forecast-calls.csv`

One row per account the CSM has called. Accounts without a row use their signal category.

| Field | Meaning |
|---|---|
| `account_id` | Matches `accounts.csv` |
| `csm_call` | `Commit`, `Best case`, `At risk`, or `Lost` |
| `expected_arr` | ARR the CSM expects at renewal. Blank means current ARR (zero for Lost) |
| `note` | One line on why |

## Fields in `renewal-history.csv`

One row per renewal that came due, including accounts that churned and are no longer in `accounts.csv`.

| Field | Meaning |
|---|---|
| `account_id`, `account`, `csm` | Identifiers. Churned accounts keep their own IDs |
| `renewal_date` | When the renewal was due, YYYY-MM-DD |
| `arr_before`, `arr_after` | ARR going into the renewal, and after it. Zero after for a churn |
| `outcome` | `Renewed`, `Expanded`, `Downgraded`, or `Churned` |
| `reason` | A [root cause tag](../frameworks/escalation-logic.md#root-cause-tags) for any churn or downgrade |

## Fields in `score-history.csv`

One row per account per saved scoring run. To build it from your own runs, save each week's `scored-accounts.csv`: its `usage_score` to `commercial_score` columns are these signal scores.

| Field | Meaning |
|---|---|
| `account_id` | Matches the renewal history |
| `as_of` | The scoring run's date, YYYY-MM-DD |
| `usage`, `outcomes`, `engagement`, `support`, `sentiment`, `commercial` | Signal scores, 0 to 100. Blank means missing |
| `red_flags` | Red flags at that date, as in `accounts.csv` |

## Fields in `forecast-history.csv`

One row per renewal, as forecast on the first day of its quarter.

| Field | Meaning |
|---|---|
| `quarter` | The renewal's quarter, such as `2026-Q1` |
| `account_id`, `account` | Identifiers |
| `arr` | ARR up for renewal |
| `category` | The category used at the start of the quarter: `Commit`, `Best case`, `At risk`, or `Lost` |
| `expected_arr` | Expected ARR at the start of the quarter |
| `actual_arr` | ARR after the renewal. Zero for a churn |

## Files in `exports/`

`crm-companies.csv`, `product-usage.csv`, and `support-orgs.csv` look like raw exports: dollar signs in ARR, US-format dates, the last executive meeting as a date rather than days, yes/no columns for red flags, and a usage export that is missing Meridian Analytics. [`mapping.json`](exports/mapping.json) turns them into `accounts.csv` exactly:

```
python3 tools/import_data.py sample-data/exports/mapping.json --source crm=sample-data/exports/crm-companies.csv --source usage=sample-data/exports/product-usage.csv --source support=sample-data/exports/support-orgs.csv --as-of 2026-10-01
```

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
| Cedar Health Partners | All four adoption readings in one plan: Proven, two Adoption gaps, and Not converting |
| Larkspur Retail, Pinecrest Manufacturing | Faster month-end close Not converting at two accounts: a pattern for Product |
| Larkspur Retail, Tidewater Clinics | Unexplained progress: on track while the features behind the goal are lightly used |
| Orchard Learning | No adoption data, so its goals can't be proven |
| Sable Energy, Larkspur Retail, Granite Payroll | Forecast calls above what the signals support |
| Pinecrest Manufacturing | Renewing next quarter with no forecast call |
| Aspen Freight, Cobalt Studios | Churned in the last 12 months: in the renewal history, not the book |
| Dogwood Partners | Churned before the 12-month window, so retention and the back-test leave it out |
| Aspen Freight | Green 90 days out under the old 30/20 weights, Yellow under the current ones; churned from a Best case forecast |
| Quarry Lane Media (last year) | Red 90 days before its 2026 renewal, then renewed in full: the back-test's false alarm |
| Bluefin Logistics, Orchard Learning, Willow Biotech | Healthy accounts, each with a goal already Met |
