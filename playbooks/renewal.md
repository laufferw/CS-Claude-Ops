# Playbook: Renewal

> Generic pattern. Adapt the timeline to your contract lengths and approval process.

## Purpose

Run every renewal on the same timeline, starting early enough that problems can still be fixed, with clear ownership of the commercial decisions.

## Trigger

An account reaches 120 days before its renewal date.

## Inputs

- Health band, index, and drivers from [Account Health Scoring](../frameworks/account-health-scoring.md)
- Contract details: term, price, seats, scope, renewal clauses and notice periods
- Success plan outcomes
- Open escalations, contract flags, and stakeholder status

## Steps

| Step | Owner | Timing |
|---|---|---|
| 1. Run the [Pre-Renewal Check](../prompts/pre-renewal-check.md) and set a status | CSM | Day -120 |
| 2. Confirm the notice period and any auto-renewal terms | RevOps | Day -120 |
| 3. Prepare the renewal with the [Renewal Prep](../prompts/renewal-prep.md) prompt | CSM | Day -110 |
| 4. Renewal conversation with the decision-maker: value delivered, plans for next term | CSM, with Sales if commercial changes are expected | By day -90 |
| 5. Proposal: price, seats, and terms | Sales, with Finance approval for any discount | By day -60 |
| 6. Negotiation and redlines (see [Contract Redline Summary](../prompts/contract-redline-summary.md) and [SLA Pushback](sla-pushback.md)) | Sales, Legal | Day -60 to -30 |
| 7. Paperwork signed | Sales, RevOps | By day -30 |
| 8. Record the outcome, the final terms, and the reason for any change in ARR | RevOps | Within 5 business days of signature |

## Decision logic

Use the pre-renewal status to decide the path:

| Status | Path |
|---|---|
| Ready | Standard timeline above |
| Needs work | Standard timeline, plus a dated fix for each gap before the day -90 conversation |
| At risk | Start an [At-Risk Save Plan](at-risk-save-plan.md) now, in parallel with the timeline. Red accounts within 90 days of renewal are an L2 escalation |
| Unclear | Fix the data first (within 10 business days), then re-run the check |

- **Downgrade request:** treat as a risk, not a negotiation point. Find out why before Sales responds with numbers.
- **Expansion interest:** handle it in the renewal only if it is qualified (see [Expansion](expansion.md)). Do not let an expansion conversation delay the base renewal.
- **Customer goes silent after day -60:** escalate to the executive sponsor on both sides.

## Outputs

- Pre-renewal status, set at day -120 and updated at each step
- Signed renewal, or a recorded non-renewal (then follow [Churn and Offboarding](churn-and-offboarding.md))
- Final ARR change, split into price, seats, and scope, with the reason

## Failure modes

- Starting at day -30, when the only lever left is discount.
- The CSM negotiating price. Pricing belongs to Sales and Finance. The CSM owns the value story.
- Missing a notice period and losing the right to change terms. Step 2 checks it.
- Recording a renewal without the reason for an ARR change, which leaves nothing to learn from.
