# Guide: CS Executive (VP or COO)

> For the executive who owns customer retention: a scorecard with fixed definitions, the value story for the board, and the case for funding CS.

## Who it's for

A VP of Customer Success, Chief Customer Officer, or COO. It helps you report CS with numbers Finance agrees with, show the value customers actually got, forecast renewals, staff the team, and decide whether to sell [Adoption as a Service](../specs/adoption-as-a-service.md).

## What you need

- A CS Ops owner who keeps the data and definitions current (see the [CS Ops guide](cs-ops.md))
- Renewal history for the last 12 months: ARR before and after each renewal, and the reason for any loss
- Agreement with Finance on retention definitions
- Directors running the [Weekly Team Review](../playbooks/weekly-team-review.md)

## Your week

| When | Do | With |
|---|---|---|
| Weekly | Read each director's note: forecast changes and new risks | [Weekly Team Review](../playbooks/weekly-team-review.md) outputs |
| Monthly | Scorecard: retention, book health, value realized, forecast, capacity | [`tools/cs_scorecard.py`](../tools/cs_scorecard.py), [CS Metrics Scorecard](../frameworks/cs-metrics-scorecard.md) |
| Quarterly | Value story for the exec team or board | [`tools/value_report.py`](../tools/value_report.py), then the `cs-value-narrative` skill |
| Quarterly | Outcome Review decisions for Product, Marketing, and Sales | [Outcome Review](../playbooks/outcome-review.md) |
| Once, then yearly | Charter and ownership map, signed by every function; AI policy approved | [CS Charter](../frameworks/cs-charter.md), [AI Usage Policy](../frameworks/ai-usage-policy.md) |
| Planning | Headcount from the capacity model; Adoption as a Service pilot | [Capacity Model](../frameworks/capacity-model.md), [Adoption as a Service](../specs/adoption-as-a-service.md) |

Try it on the sample:

```
python3 tools/cs_scorecard.py sample-data/accounts.csv --plans sample-data/success-plans.csv --adoption sample-data/feature-adoption.csv --history sample-data/renewal-history.csv --calls sample-data/forecast-calls.csv --capacity sample-data/capacity-inputs.json --as-of 2026-10-01
```

## What you get

- A one-page scorecard, each number shown with its calculation
- A board-ready value story that claims only proven results
- A renewal forecast built from CSM calls checked against the data
- Headcount needs backed by a workload model

## Start here

1. Read the essay [Prove the Value, Then Sell It](../essays/prove-the-value-then-sell-it.md).
2. Run the scorecard above, and compare its definitions with how your company reports retention today.
3. Pick one team to pilot the weekly routine for a quarter, then compare its forecast accuracy and data coverage with the rest.

Before rolling this out widely, agree the [CS Charter and Ownership Map](../frameworks/cs-charter.md) with your peers, and get the [AI Usage Policy](../frameworks/ai-usage-policy.md) approved by Legal and Security.

## Failure modes

- **Reporting NRR without GRR.** Expansion hides churn. Show both, always.
- **Customer-agreed value presented as revenue.** It is the customer's estimate. Label it every time.
- **Funding CS on retention claims alone.** Retention invites arguments about what would have happened anyway. Proven outcomes and Adoption as a Service bookings are harder to dispute.
- **Rolling out everywhere at once.** Pilot with one team, fix the data, then expand.
