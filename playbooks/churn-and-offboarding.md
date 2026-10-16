# Playbook: Churn and Offboarding

> Generic pattern. Data retention and access terms come from the contract. Legal confirms them.

## Purpose

When a customer leaves, offboard them professionally, learn why they left, and feed that back into scoring and the playbooks.

## Trigger

Any of these:

- A notice of non-renewal is received and a save plan has closed as lost
- A renewal date passes without signature
- A contract is terminated early

## Inputs

- The contract: end date, data retention and export terms, notice clauses
- Account history: health scores over time, escalations, root cause tags, save plan
- Stakeholder contacts

## Steps

| Step | Owner | Timing |
|---|---|---|
| 1. Confirm the end date and data terms from the contract | RevOps, Legal | Within 2 business days of the trigger |
| 2. Acknowledge the decision to the customer in writing, with the end date and what happens to their data | CSM | Within 3 business days |
| 3. Exit interview with the decision-maker (questions below) | CSM, or CS manager for large accounts | Before the end date |
| 4. Data export and access shutdown, as the contract requires | Support, IT | By the end date |
| 5. Close the account record: reason, root cause tag, final ARR lost | RevOps | Within 5 business days of the end date |
| 6. Churn review: was it predictable, and what would have caught it? | CS manager | Monthly, across all churned accounts |

## Exit interview questions

- What was the main reason for the decision?
- When did you start considering leaving?
- What would have had to be different for you to stay?
- What are you moving to, if anything?
- Is there anything we committed to that we did not deliver?

Ask, listen, and record the answers in the customer's words. Do not try to reopen the deal in the interview. If they raise it, route it to Sales afterwards.

## Decision logic

- **Customer wants to reconsider:** pause offboarding and hand to Sales with the exit interview notes. Do not offer terms in the interview.
- **Contract terms on data are unclear:** Legal decides before anything is deleted.
- **The account never scored Red:** flag it in the churn review. The scoring model missed it, which is a calibration input.

## Feedback into the system

The churn review is where the [Account Health Scoring](../frameworks/account-health-scoring.md) calibration gets its data. For each churned account, record:

- The band 90 days before renewal (the calibration test)
- The root cause tag
- The earliest signal that, in hindsight, predicted it

Patterns in root cause tags go to the owner of that area: product gaps to Product, `support-responsiveness` to Support, `expectation-mismatch` to Sales leadership.

## Outputs

- A written acknowledgement to the customer, with the end date and data terms
- Exit interview notes in the customer's words
- A closed account record with reason, root cause tag, and ARR lost
- A monthly churn review with calibration notes

## Failure modes

- Skipping the exit interview because the relationship is uncomfortable. That is when it is most useful.
- Recording "price" as the reason when price was the stated reason, not the cause.
- Deleting data before the contract says to, or keeping it after.
- Churn reviews that blame individuals instead of finding the earlier signal.
