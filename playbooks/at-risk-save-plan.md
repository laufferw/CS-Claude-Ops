# Playbook: At-Risk Save Plan

> Generic pattern. Adapt owners to your escalation structure.

## Purpose

Define what goes into the "plan" that [Escalation Logic](../frameworks/escalation-logic.md) requires for an at-risk account, so every save attempt has a diagnosis, actions with owners, and a point where you decide whether it is working.

## Trigger

Any of these:

- The account's band drops to Red
- A red flag: notice of non-renewal, executive sponsor departure, payment dispute
- The [Pre-Renewal Check](../prompts/pre-renewal-check.md) returns At risk
- An L1, L2, or L3 escalation is opened

## Inputs

- The escalation write-up (see the [Escalation Summary](../prompts/escalation-summary.md) prompt)
- Health score breakdown and top drivers
- Success plan and outcomes to date
- Stakeholder map: who we still have, who we have lost
- Contract and renewal details

## Steps

| Step | Owner | Timing |
|---|---|---|
| 1. Diagnose: name the root cause, using the escalation root cause tags | CSM | Per the escalation level's response target |
| 2. Hear it from the customer: a conversation with the decision-maker about what would have to change | CSM, CS manager for L2 and above | Within 5 business days of the trigger |
| 3. Write the save plan (see below) | CSM | Same response target as the escalation |
| 4. Review the plan | CS manager (L1), VP (L2 and L3) | Within 1 business day of drafting |
| 5. Run the plan, with a weekly update to the escalation owner (see the [Internal Account Update](../prompts/internal-account-update.md) prompt) | Named action owners | Weekly |
| 6. Checkpoint: is it working? | Escalation owner | At the date set in the plan, at most 30 days out |
| 7. Close: saved, or move to [Churn and Offboarding](churn-and-offboarding.md). Close the escalation with a summary and root cause tag | Escalation owner | At the outcome |

## What the save plan contains

- The root cause, and the evidence for it
- What the customer said would have to change, in their words
- Three to five actions, each with an owner, a date, and how you will know it worked
- What we can and cannot offer, with sign-off from the function that owns each item (Support, Product, Legal, Finance)
- The checkpoint date and the signals that will mean it is working
- The walk-away point: what would make us stop investing in the save

## Decision logic

- **Cause is `product-gap`:** do not promise the feature. Ask Product for an honest answer and a date, or say it will not be built.
- **Cause is `sponsor-change`:** the first action is a meeting with the new sponsor, before anything else.
- **Cause is `commercial`:** route to Sales and Finance. The CSM does not offer discounts.
- **Checkpoint shows no improvement:** escalate one level, or decide to stop. Do not extend the plan silently.

## Outputs

- A written save plan, reviewed and approved
- Weekly updates to the escalation owner
- A recorded outcome (saved, downgraded, or lost) with a root cause tag

## Failure modes

- A plan made of activity ("more check-ins") instead of fixes for the root cause.
- A discount offered as the first action, which teaches customers that threatening to leave works.
- No checkpoint, so a failing plan runs until the renewal date.
- Saving the account without fixing the cause, so it is at risk again next quarter.
