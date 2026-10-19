# Playbook: Customer Onboarding

> Generic pattern. Adapt milestones and timings to your product's time to value.

## Purpose

Take a new customer from signed contract to first measurable value, with a success plan in place, so the account starts its life scoreable and on track.

## Trigger

The CSM sends the kickoff note, the last step of the [Sales to CS Handoff](sales-to-cs-handoff.md).

## Inputs

- The completed handoff packet (see the [Handoff Packet](../prompts/handoff-packet.md) prompt)
- Contract scope and any implementation commitments
- Technical and integration requirements
- Customer stakeholders and their roles

## Steps

| Step | Owner | Timing |
|---|---|---|
| 1. Kickoff call: confirm goals, success criteria, and roles with the customer. Walk through the [Outcome Library](../frameworks/outcome-library.md), starting from the outcomes sold in the handoff packet, and have the customer pick 3 to 4 that matter most now. Reset any result Sales promised that is outside the library's typical range | CSM | Within 10 business days of close |
| 2. Write the success plan: for each outcome, the goal in the customer's words, a customer owner, a baseline measured from the outcome's data source, and a target value and date | CSM, with customer champion | Baselines within 30 days of kickoff; plan within 30 days of close |
| 3. Technical setup and integrations | Implementation or Support | Per the plan, tracked weekly |
| 4. Train the first users and admins | CSM or Enablement | Before go-live |
| 5. Go-live | CSM | Target set at kickoff |
| 6. First-value check: has any success plan goal measurably improved on its baseline? | CSM | Within 90 days of close |
| 7. Onboarding review and handover to steady state | CSM and CS manager | When the exit criteria are met |

## Decision logic

- **Success plan missing at day 30:** treat as a data gap. The account's Outcomes signal cannot be scored, so in [Account Health Scoring](../frameworks/account-health-scoring.md) the account cannot be better than Yellow.
- **A goal has no baseline at day 30:** it is not counted toward the Outcomes signal. Measure it now. A baseline taken months later, after the product has already moved the number, understates the value delivered.
- **The customer wants an outcome the library doesn't cover:** allow one custom goal, with the same baseline, target, and measurement. Tell CS Ops so it can be reviewed as a library candidate.
- **Go-live slips more than 2 weeks:** tell the customer's champion and the CS manager in writing, with the cause and a new date. Slips that come from unmet sales commitments are tagged `expectation-mismatch`.
- **No first value by day 90:** open an L1 escalation per [Escalation Logic](../frameworks/escalation-logic.md). Onboarding that has not delivered value is the earliest churn signal you get.
- **Champion or sponsor changes during onboarding:** re-run the kickoff with the new person before continuing.

## Exit criteria

Onboarding is done when all of these are true:

- The success plan is written and agreed with the customer, and every goal has a baseline
- The customer is live, with active users on at least 40% of licensed seats
- First value: at least one goal has measurably improved on its baseline, and that goal is Met or On track
- Health scoring has 70% or more coverage

## Outputs

- A success plan: 3 to 4 goals with baselines and targets, stored where the scoring inputs read it (the format of [`sample-data/success-plans.csv`](../sample-data/success-plans.csv))
- Go-live date and first-value date, recorded on the account
- An onboarding review note: what went well, what slipped, and any commitments still open

## Failure modes

- A success plan written by the CSM alone. Goals the customer did not agree to are not goals.
- Measuring onboarding by tasks completed instead of value delivered.
- Goals with no baseline, so nobody can show later how far the customer came.
- Implementation commitments from the sale that never reached the project plan. Check the handoff packet's commitments list at kickoff.
- Declaring onboarding done at go-live, before anyone has used the product for real work.
