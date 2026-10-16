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
| Commercial | CRM, billing | Days to renewal, payment delays, contract flags |
| Outcomes | Success plan | Share of agreed goals on track |

## Scoring model

Each signal is scored 0 to 100, then weighted.

| Signal | Starting weight |
|---|---|
| Product usage | 30% |
| Outcomes | 20% |
| Engagement | 15% |
| Support | 15% |
| Sentiment | 10% |
| Commercial | 10% |

**Index = sum of (signal score x weight).**

## Bands

| Band | Range | Meaning |
|---|---|---|
| Green | 75 to 100 | Healthy. Look for expansion |
| Yellow | 50 to 74 | Watch. Needs a defined action |
| Red | 0 to 49 | At risk. Triggers escalation logic |

## Override rules

- A single red flag can force Yellow or Red regardless of the index: executive sponsor departure, notice of non-renewal, or a payment dispute.
- A CSM can override a band with a written reason. Overrides are reviewed monthly.

## Failure modes

- Usage can mislead for products where low usage is normal.
- Missing data gets scored as zero and creates false reds. Treat missing as unknown and flag it.
- Weights drift out of date. Re-test quarterly against actual outcomes.

## Calibration

Back-test on the last 12 months: did accounts that churned score Red 90 days before renewal? Adjust weights until the answer is mostly yes.
