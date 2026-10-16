# Sample Data

A fictional book of 12 accounts for one CSM, for trying the prompts and the scoring rubric without touching real data. Every company, person, and number is invented.

| File | What it is |
|---|---|
| [`accounts.csv`](accounts.csv) | Raw signals per account, the input to scoring |
| [`scored-accounts.csv`](scored-accounts.csv) | The same accounts scored as of 2026-10-01, sorted by priority. The input to the [Weekly CSM Brief](../prompts/weekly-csm-brief.md) |

Regenerate the scored file after changing the data or the rubric:

```
python3 tools/score_accounts.py sample-data/accounts.csv --as-of 2026-10-01 > sample-data/scored-accounts.csv
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
| `goals_total`, `goals_on_track` | Success plan goals. `goals_total` of 0 means no success plan |
| `red_flags` | `non_renewal_notice`, `exec_sponsor_departed`, `payment_dispute`, separated by `\|` |
| `prior_index` | Last week's index, for detecting band moves |
| `expansion_signal`, `notes` | Free text |

## What the accounts exercise

| Account | Case |
|---|---|
| Cedar Health Partners | Band drop to Red, large ARR, renewal in 75 days |
| Granite Payroll | Sponsor departure caps a Green index at Yellow |
| Larkspur Retail | Payment dispute, missing NPS |
| Meridian Analytics | High index but Insufficient data (coverage 50%) |
| Orchard Learning | Healthy account renewing in 30 days |
| Pinecrest Manufacturing | Largest ARR, Yellow, expansion signal |
| Quarry Lane Media | Non-renewal notice, no exec contact ever |
| Sable Energy | Downgrade request, renewal in 91 days |
| Tidewater Clinics | Low usage that is normal for the account |
| Bluefin Logistics, Riverbend Credit Union, Willow Biotech | Healthy baseline |
