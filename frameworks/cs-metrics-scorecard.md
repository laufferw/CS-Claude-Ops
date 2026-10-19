# CS Metrics Scorecard

> Draft. Formulas are exact; targets are yours to set. Agree each definition with Finance before the scorecard goes to the board, so the CS numbers and the company numbers match.

## Purpose

One page of CS metrics with fixed definitions, for a VP or COO to run the function and report it upward. Each metric says what it counts, where the data comes from, and how it gets gamed. A metric that two people calculate differently is an argument, not a metric.

## Inputs

| Input | Source | Example |
|---|---|---|
| Renewal history: ARR before and after each renewal, and the outcome | CRM or billing | Granite: $110,000 to $95,000, Downgraded, `commercial` |
| The scored book | [Account Health Scoring](account-health-scoring.md) | Bands and red flags for every account |
| Success plans and feature adoption | [Outcome Library](outcome-library.md) | Goal statuses and readings |
| Forecast calls | [Renewal Forecast](renewal-forecast.md) | Each CSM's call and expected ARR |
| Capacity settings | [Capacity Model](capacity-model.md) | Hours per account and per CSM |

[`sample-data/renewal-history.csv`](../sample-data/renewal-history.csv) has the history format.

## The metrics

### Retention

Calculated over the renewals due in the trailing 12 months. These are **renewal-cohort** rates: they count ARR that came up for renewal, not every change during a contract term. If Finance reports company-wide GRR and NRR on all ARR, show both and label them.

| Metric | Formula | Gamed by |
|---|---|---|
| Gross renewal rate (GRR) | Sum of min(ARR before, ARR after) / sum of ARR before | Pushing renewal dates out of the period. Report renewals that slipped |
| Net renewal rate (NRR) | Sum of ARR after / sum of ARR before | Counting expansion that Sales sold as CS retention. Report GRR next to it, always |
| Logo retention | Accounts that renewed / accounts due | Splitting or merging accounts. Count by contract, consistently |
| ARR lost by reason | Lost ARR grouped by [root cause tag](escalation-logic.md#root-cause-tags) | Tagging everything `customer-org-change`. Review tags monthly |

### Book health

| Metric | Formula | Gamed by |
|---|---|---|
| ARR by band | ARR in Green, Yellow, Red, and Insufficient data, as shares of total | CSM overrides to Green. Overrides are reviewed monthly |
| ARR at risk | ARR in Red, or with any red flag | Not recording red flags. Compare with the notes |

### Value realized

| Metric | Formula | Gamed by |
|---|---|---|
| Baselined plan coverage | Accounts with at least one baselined success plan goal / all accounts, and the same by ARR | Plans with one token goal. Check plans hold 3 to 4 goals |
| Goals met or on track | Met + On track / counted goals | Easy targets. Targets below the library's typical range get reviewed |
| Goals proven | Proven goals / counted goals | Adoption measured as logins. "Used" must mean doing the work |
| ARR with a proven outcome | ARR of accounts with at least one Proven goal / total ARR | One easy goal per account. Look at goals proven too |
| Time to first value | Median days from close to first value, for accounts closed in the period | Defining first value loosely. Use the [onboarding](../playbooks/onboarding.md) definition |

### Forecast

| Metric | Formula | Gamed by |
|---|---|---|
| Commit and weighted forecast, current quarter | Per the [Renewal Forecast](renewal-forecast.md) | Optimistic calls. Count calls above signals |
| Forecast accuracy | Renewed ARR / weighted forecast at the start of the quarter | Re-forecasting mid-quarter. Measure against the start-of-quarter number |

### Capacity

| Metric | Formula | Gamed by |
|---|---|---|
| Team utilization | Total workload hours / (CSMs x hours per CSM) | Guessed hours. Recalibrate with time studies |
| CSMs needed | Total workload / (hours per CSM x target utilization) | Same |
| ARR per CSM | Total ARR / CSMs | Ignoring segment mix. Read it next to utilization |

## Outputs

- A one-page scorecard: retention, book health, value realized, forecast, and capacity, each number shown with its calculation
- A trend when run each month, compared with last month and last quarter

[`tools/cs_scorecard.py`](../tools/cs_scorecard.py) computes everything except time to first value and forecast accuracy, which need close dates, first-value dates, and past forecasts that the sample data doesn't hold.

## Worked example

The sample as of 2026-10-01. Fourteen accounts were due to renew in the 12 months before: the 12 in the book, plus Aspen Freight and Cobalt Studios, which churned.

- **GRR:** $2,307,000 was up for renewal. Losses were Aspen ($120,000, `product-gap`), Cobalt ($45,000, `sponsor-change`), and Granite's downgrade ($15,000, `commercial`). $2,127,000 kept is 92.2%.
- **NRR:** expansion at Bluefin, Orchard, and Pinecrest brought ARR after renewal to $2,240,000: 97.1%.
- **Logo retention:** 12 of 14, 85.7%.
- **Value:** 16 of 35 counted goals are proven, and 82.6% of ARR sits on accounts with at least one proven outcome.

Dogwood Partners churned in August 2025, before the 12-month window, so it isn't counted.

## Failure modes

- **Definitions that differ from Finance's.** The board sees two retention numbers and trusts neither. Agree definitions before the first report.
- **NRR without GRR.** Expansion can hide churn. Always show both.
- **Too many metrics.** This page is the whole scorecard. Add a metric only if someone will act differently because of it.
- **Small samples.** A quarter with five renewals swings GRR by 10 points on one account. Use the trailing 12 months, and show the count.
- **Value metrics without the adoption check.** Goals on track can be luck. Lead with goals proven.

## Calibration

Each quarter, check the scorecard against what Finance reports, reconcile any difference, and record why. Once a year, ask of each metric: did anyone make a decision with it? Drop the ones nobody used.
