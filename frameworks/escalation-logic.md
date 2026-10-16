# Escalation Logic

> Draft. Adapt triggers and owners to your org.

## Purpose

Make escalation a rule-based decision, not a mood. Everyone should know what triggers one, who owns it, and what happens next.

## Triggers

| Trigger | Level |
|---|---|
| Health index drops into Red | L1 |
| Exec sponsor leaves or goes silent for 30 days | L1 |
| No first value 90 days after close (see [Onboarding](../playbooks/onboarding.md)) | L1 |
| Customer formally raises a contract or SLA concern | L2 |
| Renewal at risk within 90 days | L2 |
| Threat of termination or legal involvement | L3 |

## Levels and owners

| Level | Owner | Response target | Participants |
|---|---|---|---|
| L1 | CSM | Plan within 3 business days | CSM, CS manager |
| L2 | CS manager | Plan within 2 business days | Adds Sales, RevOps, Legal as needed |
| L3 | VP / executive | Same business day | Adds executive sponsor on both sides |

The plan is an [At-Risk Save Plan](../playbooks/at-risk-save-plan.md).

## Required fields on any escalation

- Account, ARR, and renewal date
- What happened and when
- What the customer asked for, in their words
- What we can and cannot commit to
- Owner and next-update date

## Rules

1. Escalate early. A false alarm is cheaper than a late one.
2. Commitments on SLAs, pricing, or legal terms need sign-off from the function that owns them.
3. Every escalation closes with a short written summary and a root cause tag. The [Escalation Summary](../prompts/escalation-summary.md) prompt drafts both the opening write-up and the closing summary.

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

## Failure modes

- Escalating without a clear ask.
- No owner, so nothing moves.
- Escalations never closed, so the data is useless.
