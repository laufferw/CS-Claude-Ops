# Account Health Scoring (Account Success Index)

> Draft. Weights and thresholds are starting points. Calibrate against your own churn and expansion history.

## Purpose

A single, explainable score per account that tells a CSM where to spend time, and tells leadership where revenue is at risk.

## Inputs

| Signal | Source | Example metric |
|---|---|---|
| Product usage | Product analytics | Active users / licensed seats, trend over 90 days |
| Engagement | CRM, calendar | Meetings held in last 60 days, exec sponsor contact |
| Support | Ticketing | Open escalations, time-to-resolution trend |
| Sentiment | Surveys, CSM judgment | NPS or CSAT, CSM confidence rating |
| Commercial | CRM, billing | Payment delays, contract flags |
| Outcomes | Success plan | Share of agreed goals on track |

Days to renewal is not a health signal: a healthy account can renew next month. It sets urgency instead (see the [Weekly CSM Brief](../prompts/weekly-csm-brief.md)).

The field-level format these inputs take is defined in [sample-data](../sample-data/README.md).

## Scoring model

Each signal is scored 0 to 100 with the rubric below, then weighted.

| Signal | Starting weight |
|---|---|
| Product usage | 30% |
| Outcomes | 20% |
| Engagement | 15% |
| Support | 15% |
| Sentiment | 10% |
| Commercial | 10% |

**Index = sum of (signal score x weight) / sum of weights scored**, rounded to a whole number. With every signal present, the divisor is 100%. Signal scores are not rounded before weighting.

## Signal rubric

Every result is clamped to the range 0 to 100.

**Product usage.** Seat utilization (active users / licensed seats) sets a base, and the 90-day trend adjusts it.

| Utilization | Base |
|---|---|
| 80% or more | 100 |
| 60 to 79% | 75 |
| 40 to 59% | 50 |
| 20 to 39% | 25 |
| Under 20% | 0 |

| 90-day trend | Adjustment |
|---|---|
| Up 10% or more | +10 |
| Between -10% and +10% | 0 |
| Down 10 to 24% | -15 |
| Down 25% or more | -30 |

**Outcomes.** Goals on track / goals in the success plan x 100. No success plan means the signal is missing, not zero.

**Engagement.** Meetings in the last 60 days, plus points for recency of executive sponsor contact.

| Meetings (60 days) | Points | | Last exec contact | Points |
|---|---|---|---|---|
| 3 or more | 60 | | 30 days or less | 40 |
| 2 | 45 | | 31 to 60 days | 25 |
| 1 | 25 | | 61 to 90 days | 10 |
| 0 | 0 | | Over 90 days, or never | 0 |

**Support.** Start at 100. Subtract 25 per open escalation (at most 75). Subtract 25 more if time to resolution is worsening.

**Sentiment.** The average of whichever of these two you have:

| Latest NPS response (0 to 10) | Score | | CSM confidence (1 to 5) | Score |
|---|---|---|---|---|
| 9 to 10 | 100 | | 5 | 100 |
| 7 to 8 | 70 | | 4 | 75 |
| 5 to 6 | 30 | | 3 | 50 |
| 0 to 4 | 0 | | 2 | 25 |
| | | | 1 | 0 |

**Commercial.** Start at 100. Subtract for late payment (1 to 30 days: 20, 31 to 60: 40, over 60: 60), then 20 per open contract flag (a downgrade request, a termination-for-convenience question, non-standard terms).

## Missing data

Missing data is unknown, not bad. Scoring it as zero creates false reds.

1. Score only the signals you have, and divide by the weight you scored (the formula above does this).
2. Report **coverage**: the share of total weight that was scored.
3. If coverage is below 70%, the band is **Insufficient data**. Report the index, but treat it as unreliable, and list the missing signals as data gaps to fix.

"Never" is data, not a gap: an account with no executive contact on record scores 0 for exec contact.

## Bands

| Band | Range | Meaning |
|---|---|---|
| Green | 75 to 100 | Healthy. Look for expansion |
| Yellow | 50 to 74 | Watch. Needs a defined action |
| Red | 0 to 49 | At risk. Triggers [escalation logic](escalation-logic.md) |
| Insufficient data | Coverage under 70% | Fix the data before trusting the score |

## Override rules

Some single events matter more than any index. Apply these after banding:

| Red flag | Effect |
|---|---|
| Notice of non-renewal | Band is Red, whatever the index or coverage |
| Executive sponsor departure | Band is at most Yellow |
| Payment dispute | Band is at most Yellow |

A CSM can also override a band with a written reason (for example, low usage that is normal for the account). Overrides are reviewed monthly.

## Outputs

For each account:

- Index (0 to 100) and band
- Score for each signal, and which signals were missing
- Coverage
- Overrides applied
- Top two drivers: the scored signals with the largest weighted gap, weight x (100 - score)

[`tools/score_accounts.py`](../tools/score_accounts.py) implements this rubric and produces all of the above.

## Worked example

Cedar Health Partners, from the [sample data](../sample-data/accounts.csv):

| Signal | Data | Score | Weight | Contribution |
|---|---|---|---|---|
| Usage | 230 of 500 seats (46%), down 18% | 50 - 15 = 35 | 30% | 10.5 |
| Outcomes | 1 of 4 goals on track | 25 | 20% | 5.0 |
| Engagement | 1 meeting, exec contact 95 days ago | 25 + 0 = 25 | 15% | 3.75 |
| Support | 2 escalations, resolution worsening | 100 - 50 - 25 = 25 | 15% | 3.75 |
| Sentiment | NPS 5, CSM confidence 2 | (30 + 25) / 2 = 27.5 | 10% | 2.75 |
| Commercial | Paid on time, 1 contract flag | 100 - 20 = 80 | 10% | 8.0 |
| **Index** | | | | **33.75, rounds to 34: Red** |

Coverage is 100%. The top drivers are usage (gap 30 x 65 = 1,950) and outcomes (20 x 75 = 1,500). Last week the index was 52 (Yellow), so this is a band drop.

Meridian Analytics shows the missing-data rule. Its usage export is broken and it has no success plan, so usage and outcomes are missing. The four remaining signals score an index of 95, but coverage is 50%, so the band is Insufficient data rather than Green.

## Failure modes

- Usage can mislead for products where low usage is normal. Use a CSM override with a reason, or recalibrate usage for that segment.
- Missing data scored as zero creates false reds. The missing-data rule prevents this. Watch coverage instead.
- Weights drift out of date. Re-test quarterly against actual outcomes.
- Thresholds create cliffs: 79% utilization scores 75 and 80% scores 100. Look at the breakdown, not just the band, for accounts near a boundary.

## Calibration

Back-test on the last 12 months: did accounts that churned score Red 90 days before renewal? Adjust weights until the answer is mostly yes.
