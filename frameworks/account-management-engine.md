# Account Management Engine

> Draft concept. Describes the loop that turns account data into next actions.

## Purpose

A repeatable loop that takes raw account data and returns a short, ranked list of actions for each CSM each week.

## Inputs

| Input | Source | Used for |
|---|---|---|
| Account signals: usage, engagement, support, sentiment, commercial, outcomes | Product analytics, CRM, ticketing, billing, success plans | Scoring |
| Last week's index for each account | The previous run | Detecting band moves |
| Renewal dates and contract terms | CRM, contract records | Urgency and renewal flags |
| Red flags and notes | CRM, CSM | Overrides and context |
| What each CSM did with last week's recommendations | The action log (see Learn, below) | Calibration |

[`sample-data/accounts.csv`](../sample-data/accounts.csv) shows the signal inputs in a usable format.

## The loop

1. **Ingest:** pull usage, support, CRM, and billing data.
2. **Score:** compute the health index (see [Account Health Scoring](account-health-scoring.md)). [`tools/score_accounts.py`](../tools/score_accounts.py) does this step.
3. **Detect:** raise the flags in the table below.
4. **Decide:** map each flag to its recommended action, using the same table.
5. **Rank:** order actions by revenue at stake and time to deadline (see the priority formula in the [Weekly CSM Brief](../prompts/weekly-csm-brief.md#priority)).
6. **Deliver:** send the CSM a weekly brief with the top actions and the reasoning (see the [Weekly CSM Brief](../prompts/weekly-csm-brief.md) prompt).
7. **Learn:** log what the CSM did with each recommendation (acted, dismissed with a reason, or ignored) and the outcome. Feed it into the quarterly calibration.

## Flags and actions

Each flag maps to one recommended action and the playbook or prompt that carries it out. An account can raise several flags; the brief shows the highest-priority action first.

| Flag | Raised when | Recommended action | Deadline | Carried out by |
|---|---|---|---|---|
| Red-flag override | Notice of non-renewal, sponsor departure, or payment dispute | Start a save plan. For a payment dispute, bring in Finance. For a sponsor departure, meet the new sponsor first | Per escalation level | [At-Risk Save Plan](../playbooks/at-risk-save-plan.md) |
| Band drop to Red | Band is Red and was not last week | Open an L1 escalation (L2 if renewing within 90 days) and write a save plan | 3 business days (L1), 2 (L2) | [Escalation Logic](escalation-logic.md), [Escalation Summary](../prompts/escalation-summary.md) |
| Band drop to Yellow | Band moved from Green to Yellow | Review the account and set one defined action against the top driver | 1 week | [Account Review](../prompts/account-review.md) |
| Usage trend break | 90-day usage trend down 10% or more, whatever the band | Find the cause with the champion: adoption, a broken integration, or a team change | 2 weeks | [Account Review](../prompts/account-review.md) |
| Renewal window | 120 days or fewer to renewal | Run the pre-renewal check and start the renewal timeline | Day -120 | [Renewal](../playbooks/renewal.md), [Pre-Renewal Check](../prompts/pre-renewal-check.md) |
| Executive contact gap | No executive sponsor contact in 60 days, or never | Book a meeting with the sponsor | 2 weeks | [Customer Email](../prompts/customer-email.md) |
| Data gap | Band is Insufficient data, or any signal is missing | Name an owner to fix the data source (usually RevOps) | 10 business days | [Account Health Scoring](account-health-scoring.md#missing-data) |
| Outcomes unmeasured | A success plan goal has no baseline or has not been measured in 60 days | Restore the measurement: take the baseline, or fix the data feed | 10 business days | [Outcome Library](outcome-library.md#measuring-progress) |
| Adoption gap | A goal is Off track or Missed and the features behind it are lightly used | Build an adoption plan with the champion for the named features | 2 weeks | [Outcome Library](outcome-library.md#checking-adoption-behind-each-outcome) |
| Not converting | A goal is Off track or Missed though the features behind it are in use | Check configuration and process with the customer. Log it for the outcome review | 2 weeks | [Outcome Review](../playbooks/outcome-review.md) |
| Unexplained progress | A goal is Met or On track but the features behind it are lightly used | Find what moved the number before citing it as our result | Before the next QBR | [Outcome Library](outcome-library.md#checking-adoption-behind-each-outcome) |
| Onboarding stall | No success plan 30 days after close, or no first value at 90 | Finish the success plan; at day 90, open an L1 escalation | Immediately | [Customer Onboarding](../playbooks/onboarding.md) |
| Expansion signal | Expansion signal on a Green or Yellow account | Qualify it before anything goes to Sales | 5 business days | [Expansion](../playbooks/expansion.md) |

A band override recorded by the CSM, with a reason, suppresses the band flags for that account until the monthly override review.

## Outputs

**The weekly CSM brief:**

- Top 5 accounts needing attention, each with: why, recommended action, deadline
- Renewals in the next 120 days with status
- Expansion signals worth a conversation
- Data gaps to fix

**The action log:** each recommendation, what the CSM did with it, any dismissal reason, and the outcome. This is the calibration input.

## Design principles

- Explain every recommendation. No black-box rankings.
- Few actions, well chosen. Ten tasks is no brief.
- The CSM can dismiss a recommendation with a reason, and the system learns from it.

## Failure modes

- **Alert fatigue from too many flags.** The brief's 5-account cap and the priority ranking limit this. If CSMs dismiss more than half of the recommendations for a flag, its threshold is wrong.
- **Garbage in.** Poor CRM hygiene produces poor recommendations. The data gap flag makes the problem visible instead of hiding it in the score.
- **No feedback loop, so the model stagnates.** Without the action log there is nothing to calibrate against. Treat a missing log as a broken engine.
- **The same account flagged every week with no change.** If an action has not moved the account in three weeks, the next step is escalation, not another reminder.
