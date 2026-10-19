# Escalation Logic

> Draft. Adapt triggers and owners to your org.

## Purpose

Make escalation a rule-based decision, not a mood. Everyone should know what triggers one, who owns it, and what happens next.

## Inputs

- Health band and red flags from [Account Health Scoring](https://github.com/laufferw/outcome-led-cs-ops/blob/main/frameworks/account-health-scoring.md)
- Pre-renewal status from the [Pre-Renewal Check](https://github.com/laufferw/outcome-led-cs-ops/blob/main/prompts/pre-renewal-check.md)
- Executive sponsor contact history
- Onboarding milestones: close date and first-value date
- Customer communications: formal concerns, termination threats, legal correspondence

## Triggers

| Trigger | Level |
|---|---|
| Health index drops into Red | L1 |
| Exec sponsor leaves or goes silent for 30 days | L1 |
| No first value 90 days after close (see [Onboarding](https://github.com/laufferw/outcome-led-cs-ops/blob/main/playbooks/onboarding.md)) | L1 |
| Customer formally raises a contract or SLA concern | L2 |
| Renewal at risk within 90 days | L2 |
| Threat of termination or legal involvement | L3 |

If more than one trigger applies, use the highest level.

**Renewal at risk** means the pre-renewal status is At risk: the band is Red, or the account has a red flag (notice of non-renewal, sponsor departure, payment dispute).

## Levels and owners

| Level | Owner | Response target | Participants |
|---|---|---|---|
| L1 | CSM | Plan within 3 business days | CSM, CS manager |
| L2 | CS manager | Plan within 2 business days | Adds Sales, RevOps, Legal as needed |
| L3 | VP / executive | Same business day | Adds executive sponsor on both sides |

The plan is an [At-Risk Save Plan](https://github.com/laufferw/outcome-led-cs-ops/blob/main/playbooks/at-risk-save-plan.md).

## Required fields on any escalation

- Account, ARR, and renewal date
- What happened and when
- What the customer asked for, in their words
- What we can and cannot commit to
- Owner and next-update date

## Rules

1. Escalate early. A false alarm is cheaper than a late one.
2. Commitments on SLAs, pricing, or legal terms need sign-off from the function that owns them.
3. Every escalation closes with a short written summary and a root cause tag. The [Escalation Summary](escalation-summary.md) prompt drafts both the opening write-up and the closing summary.

## Raising, lowering, and closing

- **Raise a level** when a higher trigger appears, or when the save plan's checkpoint shows no improvement.
- **Lower a level** only when the trigger that set it no longer applies, and the owner of the higher level agrees. Record the reason.
- **Close** when one of these is true, and record which:
  - **Resolved:** the trigger no longer applies and the customer has confirmed the fix, or the band is back out of Red for two consecutive weekly runs
  - **Renewed:** the renewal signed, even if a downgrade
  - **Lost:** the customer has confirmed they are leaving. Move to [Churn and Offboarding](https://github.com/laufferw/outcome-led-cs-ops/blob/main/playbooks/churn-and-offboarding.md)

An escalation that has had no update for two weeks past its next-update date goes to the owner's manager.

## Root cause tags

Pick one primary tag when closing. Add a secondary tag only if it changed the outcome.

| Tag | Use when |
|---|---|
| `product-defect` | Something that should work did not |
| `product-gap` | The customer needs something the product does not do |
| `adoption` | The product works, but the customer is not using it well (onboarding, training, rollout) |
| `support-responsiveness` | Our response or resolution time was the problem |
| `sponsor-change` | A champion or executive sponsor left, changed role, or disengaged |
| `expectation-mismatch` | What was sold or promised differs from what was delivered |
| `commercial` | Price, budget, payment, or seat count |
| `contract-terms` | SLA, legal, or other contract language |
| `customer-org-change` | Merger, reorg, budget cut, or strategy shift on the customer's side |

Review tag counts quarterly. A rising tag is a pattern to fix upstream, not a run of bad luck.

## Outputs

- An escalation record with the required fields, level, and owner
- A save plan, within the level's response target
- Updates at each next-update date
- A closing summary with the outcome (resolved, renewed, or lost) and a root cause tag
- Quarterly root cause tag counts

## Failure modes

- Escalating without a clear ask.
- No owner, so nothing moves.
- Escalations never closed, so the data is useless. The two-week stale rule catches these.
- Lowering a level to make the dashboard look better. Lowering needs the higher owner's agreement and a recorded reason.
