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
| 1. Kickoff call: confirm goals, success criteria, and roles with the customer | CSM | Within 10 business days of close |
| 2. Write the success plan: 3 to 6 measurable goals, each with a customer owner and a target date | CSM, with customer champion | Within 30 days of close |
| 3. Technical setup and integrations | Implementation or Support | Per the plan, tracked weekly |
| 4. Train the first users and admins | CSM or Enablement | Before go-live |
| 5. Go-live | CSM | Target set at kickoff |
| 6. First-value check: has the customer reached the first goal in the success plan? | CSM | Within 90 days of close |
| 7. Onboarding review and handover to steady state | CSM and CS manager | When the exit criteria are met |

## Decision logic

- **Success plan missing at day 30:** treat as a data gap. The account's Outcomes signal cannot be scored, which lowers coverage in [Account Health Scoring](../frameworks/account-health-scoring.md).
- **Go-live slips more than 2 weeks:** tell the customer's champion and the CS manager in writing, with the cause and a new date. Slips that come from unmet sales commitments are tagged `expectation-mismatch`.
- **No first value by day 90:** open an L1 escalation per [Escalation Logic](../frameworks/escalation-logic.md). Onboarding that has not delivered value is the earliest churn signal you get.
- **Champion or sponsor changes during onboarding:** re-run the kickoff with the new person before continuing.

## Exit criteria

Onboarding is done when all of these are true:

- The success plan is written and agreed with the customer
- The customer is live, with active users on at least 40% of licensed seats
- The first success plan goal is met, with evidence
- Health scoring has 70% or more coverage

## Outputs

- A success plan, stored where the scoring inputs read it
- Go-live date and first-value date, recorded on the account
- An onboarding review note: what went well, what slipped, and any commitments still open

## Failure modes

- A success plan written by the CSM alone. Goals the customer did not agree to are not goals.
- Measuring onboarding by tasks completed instead of value delivered.
- Implementation commitments from the sale that never reached the project plan. Check the handoff packet's commitments list at kickoff.
- Declaring onboarding done at go-live, before anyone has used the product for real work.
