# Account Management Engine

> Draft concept. Describes the loop that turns account data into next actions.

## Purpose

A repeatable loop that takes raw account data and returns a short, ranked list of actions for each CSM each week.

## The loop

1. **Ingest:** pull usage, support, CRM, and billing data.
2. **Score:** compute the health index (see [Account Health Scoring](account-health-scoring.md)).
3. **Detect:** flag changes: band moves, trend breaks, missing data, upcoming renewals.
4. **Decide:** map each flag to a recommended action using rules (see [Escalation Logic](escalation-logic.md)).
5. **Rank:** order actions by revenue at stake and time to deadline.
6. **Deliver:** send the CSM a weekly brief with the top actions and the reasoning.
7. **Learn:** log what the CSM did and the outcome. Feed it back into calibration.

## Output: weekly CSM brief

- Top 5 accounts needing attention, each with: why, recommended action, deadline
- Renewals in the next 120 days with status
- Expansion signals worth a conversation
- Data gaps to fix

## Design principles

- Explain every recommendation. No black-box rankings.
- Few actions, well chosen. Ten tasks is no brief.
- The CSM can dismiss a recommendation with a reason, and the system learns from it.

## Failure modes

- Alert fatigue from too many flags.
- Garbage in: poor CRM hygiene produces poor recommendations.
- No feedback loop, so the model stagnates.
