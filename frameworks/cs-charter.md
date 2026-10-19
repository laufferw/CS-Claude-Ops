# CS Charter and Ownership Map

> Draft. A starting charter for a CS team in the model the rest of this repo assumes: CS owns outcomes and renewal readiness, Sales owns commercial terms. Adapt it, then agree it with every function named here before relying on it.

## Purpose

Say in writing what Customer Success is for, what it owns, what it does not, and who decides what across Sales, Support, Services, Product, Finance, Legal, Marketing, and CS Ops. Without this, CS fills every gap nobody else owns, and "that's not our job" becomes the honest answer to the work that matters most: helping customers reach measurable outcomes.

## Inputs

| Input | Source | Example |
|---|---|---|
| The company's go-to-market model | Executive team | Sales owns new business and renewal pricing |
| Each function's current responsibilities | Function leaders | Support owns tickets; Services owns implementation projects |
| Where work falls through today | Escalation root cause tags, churn reviews | `expectation-mismatch`: promises Sales made that nobody delivered |
| How CS is measured and funded | CS leadership, Finance | The [CS Metrics Scorecard](cs-metrics-scorecard.md) |

## The charter

**Mission.** Customers reach the measurable outcomes they chose, and renew and grow because of it.

**CS owns:**

- **Outcomes.** Every customer has a success plan from the [Outcome Library](outcome-library.md), with baselines, measured progress, and an adoption plan where needed.
- **Account health.** Scoring, flags, and the actions they trigger, per [Account Health Scoring](account-health-scoring.md) and the [Account Management Engine](account-management-engine.md).
- **Renewal readiness and the value story.** The [Pre-Renewal Check](../prompts/pre-renewal-check.md), the renewal conversation about value, and the forecast call.
- **Expansion signals.** Spotting and qualifying them, per [Expansion](../playbooks/expansion.md).
- **Escalation coordination.** Opening, running, and closing escalations at L1 and L2, per [Escalation Logic](escalation-logic.md).
- **The customer's voice, with evidence.** Outcome patterns to Product, and proven results to Marketing, through the [Outcome Review](../playbooks/outcome-review.md).

**CS does not own:**

| Not CS's | Owned by | CS's part |
|---|---|---|
| Pricing, discounts, and renewal proposals | Sales, with Finance approval | The value story and the readiness status |
| Contract terms, SLAs, and redlines | Legal and Sales | A plain-language summary, and routing (the [Redline Summary](../prompts/contract-redline-summary.md)) |
| Support tickets and bug fixes | Support and Product | Escalating when a ticket threatens an outcome or a renewal |
| Implementation and configuration projects | Services | Adoption after go-live, and success plan baselines |
| Roadmap and feature decisions | Product | Patterns with evidence, never promises |
| Collections and payment disputes | Finance | Flagging, and keeping the relationship intact |
| Data definitions and systems | CS Ops or RevOps | Keeping their own accounts' data current |

**How CS is measured:** retention (GRR, NRR, logo retention), value realized (baselined plans, goals proven, ARR with a proven outcome), forecast accuracy, and time to first value, all defined in the [CS Metrics Scorecard](cs-metrics-scorecard.md). Not by meetings held or tickets touched.

**How CS is funded:** as a cost of keeping ARR, plus any revenue from [Adoption as a Service](../specs/adoption-as-a-service.md).

## Ownership map

**R** does the work. **A** is accountable and decides. Each row has exactly one A. **C** is consulted before. **I** is informed after.

| Activity | CS | Sales | Support | Services | Product | Finance | Legal | Marketing | CS Ops / RevOps |
|---|---|---|---|---|---|---|---|---|---|
| Handoff packet | C | A/R | | I | | | | | R (checks it) |
| Onboarding and first value | A/R | I | C | R (implementation) | | | | | |
| Success plan and baselines | A/R | C (outcomes sold) | | C | | | | | I |
| Adoption plans | A/R | | C | C | C | | | | |
| Support tickets | I | | A/R | | C | | | | |
| Escalations, L1 and L2 | A/R | I | R | C | C | C | | | |
| Escalations, L3 | R | C | C | C | C | C | C | | |
| Renewal readiness and forecast call | A/R | C | | | | I | | | C |
| Renewal proposal and pricing | C | A/R | | | | C (approves discounts) | C | | |
| Contract terms and redlines | C | R | | | | C | A | | |
| Payment disputes | C | I | | | | A/R | | | |
| Expansion qualification | A/R | C | | | | | | | |
| Expansion opportunity and close | C | A/R | | | | C | | | |
| Product gaps and roadmap answers | R (evidence) | I | C | | A | | | | |
| Proof points and case studies | R (customer permission) | I | | | | | C | A | |
| Churn analysis and root cause tags | R | C | C | | C | I | | | A |
| Metric definitions and data | C | C | | | | C | | | A/R |

L3 escalations are accountable to the executive who owns the account relationship, usually the CS VP. Name that person in your copy.

## Choosing your model

This charter assumes **CS owns outcomes, Sales owns commercial terms**. Some companies give CS the renewal number and pricing authority within limits (an account management model). If yours does, change the rows for renewal proposal and expansion close, give CS a renewal quota in the scorecard, and keep everything else. What matters is that the choice is written down, not which one you pick.

## Outputs

- A signed charter: mission, what CS owns, what it doesn't, and how it is measured and funded
- An ownership map with one accountable function per activity
- A list of activities nobody owned before, now assigned

## Worked example

The sample data shows why the map matters. Aspen Freight churned for `product-gap`, and its forecast said Best case until the end. With the map, the gap goes to Product with evidence through the outcome review (Product is A), the renewal stays CS's to call honestly (CS is A for the forecast call), and Sales doesn't discount to cover a missing feature (Sales owns pricing, Finance approves).

Larkspur Retail's payment dispute shows the other side. Finance is accountable for resolving it. The CSM's job is to flag it and protect the relationship, not to negotiate the invoice.

## Failure modes

- **A charter nobody else signed.** Ownership CS declares alone isn't ownership. Every function in the map signs, or the rows are still open.
- **Two A's in a row.** Shared accountability means nobody's. Pick one.
- **CS keeps doing what it gave away.** If CSMs still chase invoices or negotiate price, the charter is decoration. Directors check it in the [Weekly Team Review](../playbooks/weekly-team-review.md).
- **Outcomes treated as optional.** The charter puts outcomes first. If success plans are the first thing dropped in a busy quarter, the scorecard's value metrics will show it.
- **Never revisited.** Review the charter once a year, and whenever the go-to-market model changes.

## Calibration

Each quarter, look at escalation and churn root cause tags. Any loss tagged `expectation-mismatch`, or any escalation that stalled waiting for an owner, points at a row of the map that isn't working. Fix the row, not just the account.
