# Account Health Scoring (Account Success Index)

> Weights and thresholds are starting points. Calibrate against your own churn and expansion history.

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
| Outcomes | Success plan, measured against the [Outcome Library](https://github.com/laufferw/outcome-led-cs-ops/blob/main/frameworks/outcome-library.md) | Share of measured goals met or on track |

Days to renewal is not a health signal: a healthy account can renew next month. It sets urgency instead (see the [Weekly CSM Brief](weekly-csm-brief.md)).

The field-level format these inputs take is defined in [sample-data](https://github.com/laufferw/outcome-led-cs-ops/blob/main/sample-data/README.md). Success plan goals are a separate file, one row per goal.

## Scoring model

Each signal is scored 0 to 100 with the rubric below, then weighted.

| Signal | Starting weight |
|---|---|
| Product usage | 25% |
| Outcomes | 25% |
| Engagement | 15% |
| Support | 15% |
| Sentiment | 10% |
| Commercial | 10% |

Outcomes weighs as much as usage. Usage only matters if it is delivering the outcomes the customer agreed to, and usage alone can look healthy while nothing the customer cares about improves.

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

**Outcomes.** Goals Met or On track / goals counted x 100, with each goal's status measured from its baseline, target, and latest value under the [Outcome Library](https://github.com/laufferw/outcome-led-cs-ops/blob/main/frameworks/outcome-library.md#measuring-progress) rules. Goals with no baseline, or not measured in 60 days, are not counted: they are data gaps. No counted goals (including no success plan) means the signal is missing, not zero, and the no-measured-outcomes override below applies.

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
| Red | 0 to 49 | At risk. Triggers [escalation logic](https://github.com/laufferw/outcome-led-cs-ops/blob/main/frameworks/escalation-logic.md) |
| Insufficient data | Coverage under 70% | Fix the data before trusting the score |

## Override rules

Some single events, and one missing piece of evidence, matter more than any index. Apply these after banding:

| Condition | Effect |
|---|---|
| Notice of non-renewal | Band is Red, whatever the index or coverage |
| Executive sponsor departure | Band is at most Yellow |
| Payment dispute | Band is at most Yellow |
| No measured outcomes: no success plan, or no goal with a baseline and a measurement in the last 60 days | Band is at most Yellow |

The last rule closes a gap in the missing-data rule. Without it, an account with no measured outcomes still has 75% coverage, enough to be Green on usage and relationship signals alone. Green means the account is healthy, and an account can't be called healthy when nobody can show it is getting value. The cap does not make it Red: unknown is still not bad.

A CSM can also override a band with a written reason (for example, low usage that is normal for the account). Overrides are reviewed monthly.

## Outputs

For each account:

- Index (0 to 100) and band
- Score for each signal, and which signals were missing
- Coverage
- Overrides applied
- Success plan summary: goals counted, how many are on track, and any with no baseline or gone stale
- Top two drivers: the scored signals with the largest weighted gap, weight x (100 - score)

[`tools/score_accounts.py`](https://github.com/laufferw/outcome-led-cs-ops/blob/main/tools/score_accounts.py) implements this rubric and produces all of the above.

## Worked example

Cedar Health Partners, from the [sample data](https://github.com/laufferw/outcome-led-cs-ops/blob/main/sample-data/accounts.csv):

| Signal | Data | Score | Weight | Contribution |
|---|---|---|---|---|
| Usage | 230 of 500 seats (46%), down 18% | 50 - 15 = 35 | 25% | 8.75 |
| Outcomes | 1 of 4 goals on track ([worked example](https://github.com/laufferw/outcome-led-cs-ops/blob/main/frameworks/outcome-library.md#worked-example)) | 25 | 25% | 6.25 |
| Engagement | 1 meeting, exec contact 95 days ago | 25 + 0 = 25 | 15% | 3.75 |
| Support | 2 escalations, resolution worsening | 100 - 50 - 25 = 25 | 15% | 3.75 |
| Sentiment | NPS 5, CSM confidence 2 | (30 + 25) / 2 = 27.5 | 10% | 2.75 |
| Commercial | Paid on time, 1 contract flag | 100 - 20 = 80 | 10% | 8.0 |
| **Index** | | | | **33.25, rounds to 33: Red** |

Coverage is 100%. The top drivers are outcomes (gap 25 x 75 = 1,875) and usage (25 x 65 = 1,625). Last week the index was 52 (Yellow), so this is a band drop.

Meridian Analytics shows the missing-data rule. Its usage export is broken and it has no success plan, so usage and outcomes are missing. The four remaining signals score an index of 95, but coverage is 50%, so the band is Insufficient data rather than Green.

Riverbend Credit Union shows the no-measured-outcomes override. Its four goals were last measured in June, so all are Stale and none is counted. The other five signals give an index of 87 at 75% coverage, which would be Green. The override caps it at Yellow, and the fix is to measure the success plan again, not to change how the account is managed.

## Failure modes

- Usage can mislead for products where low usage is normal. Use a CSM override with a reason, or recalibrate usage for that segment.
- Missing data scored as zero creates false reds. The missing-data rule prevents this. Watch coverage instead.
- An account looks healthy on usage while delivering nothing the customer cares about. Equal weight for outcomes and the no-measured-outcomes cap guard against this.
- Weights drift out of date. Re-test quarterly against actual outcomes.
- Thresholds create cliffs: 79% utilization scores 75 and 80% scores 100. Look at the breakdown, not just the band, for accounts near a boundary.

## Calibration

Back-test on the last 12 months: did accounts that churned score Red 90 days before renewal? Adjust weights until the answer is mostly yes. [`tools/backtest.py`](https://github.com/laufferw/outcome-led-cs-ops/blob/main/tools/backtest.py) runs this test from saved scoring snapshots, and compares a second weight set side by side. Outcomes moved from 20% to 25% and usage from 30% to 25% on the argument above. In the sample back-test, the old weights left Aspen Freight's $120,000 churn Green 90 days out, and the new ones flag it Yellow. That is one account, not proof: test the change on your own history, with at least 30 renewals. The monthly churn review in [Churn and Offboarding](https://github.com/laufferw/outcome-led-cs-ops/blob/main/playbooks/churn-and-offboarding.md) collects this data.
