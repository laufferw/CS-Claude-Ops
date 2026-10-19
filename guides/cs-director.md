# Guide: CS Director or Manager

> For the leader of a CS team: one weekly view across every CSM, a forecast you can defend, and capacity numbers for staffing decisions.

## Who it's for

A director or manager responsible for a team's retention, forecast, and people. It helps you see risk across the team without reading every account, challenge forecast calls fairly, balance books, and coach CSMs on evidence.

## What you need

- The whole team's book in the repo formats, refreshed weekly by CS Ops (see the [CS Ops guide](cs-ops.md))
- Each CSM's forecast call and expected ARR for the next two quarters
- Capacity settings from a time study: hours per account and per CSM (see the [Capacity Model](../frameworks/capacity-model.md))

## Your week

| When | Do | With |
|---|---|---|
| Monday | Team rollup: health, risk, renewals, outcomes, and workload by CSM | [`tools/team_rollup.py`](../tools/team_rollup.py) |
| Monday | Renewal forecast and calls that disagree with the data | [`tools/renewal_forecast.py`](../tools/renewal_forecast.py) |
| Monday | Draft the team brief, then run the review | `/cs-team-brief`, [Weekly Team Review](../playbooks/weekly-team-review.md) |
| Within 3 days of a band drop to Red | Confirm the escalation and save plan | [Escalation Logic](../frameworks/escalation-logic.md), [At-Risk Save Plan](../playbooks/at-risk-save-plan.md) |
| Monthly | Review CSM band overrides and their reasons | [Account Health Scoring](../frameworks/account-health-scoring.md#override-rules) |
| Quarterly | Coaching evidence for each CSM | `/cs-competency-evaluation` |
| Quarterly | Outcome Review with Product, Marketing, and Sales | [Outcome Review](../playbooks/outcome-review.md) |

Try it on the sample team:

```
python3 tools/team_rollup.py sample-data/accounts.csv --plans sample-data/success-plans.csv --adoption sample-data/feature-adoption.csv --capacity sample-data/capacity-inputs.json --as-of 2026-10-01
python3 tools/renewal_forecast.py sample-data/accounts.csv --plans sample-data/success-plans.csv --calls sample-data/forecast-calls.csv --as-of 2026-10-01
```

## What you get

- One table across the team: bands, band drops, ARR at risk, renewals, goals on track and proven, data gaps, and workload
- A quarterly forecast with commit, best case, and weighted numbers, and a short list of calls to challenge
- Capacity: who is over target, who has room, and the headcount the book needs
- A weekly action list, and a note for your VP

## Start here

1. Run the two commands above and read them side by side.
2. Read the [Renewal Forecast](../frameworks/renewal-forecast.md) categories, so you can explain a challenge to a CSM.
3. Run one [Weekly Team Review](../playbooks/weekly-team-review.md) with your team.

## Failure modes

- **Reading utilization as performance.** A heavy book isn't a weak CSM. Use the [competency framework](../frameworks/csm-competency-framework.md) for performance.
- **Accepting every call.** The forecast is only as good as the challenge. Ask about every call above signals.
- **Rebalancing mid-save.** Move accounts at natural points, never during an escalation.
- **Letting data gaps slide.** A book full of Insufficient data can't be managed. Treat growing gaps as a coaching topic.
