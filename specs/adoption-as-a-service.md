# Adoption as a Service Spec

> Draft design doc. A paid CS offering that takes a customer from adoption to measured outcomes from the [Outcome Library](../frameworks/outcome-library.md), and the report that shows what CS delivered. Prices, tiers, and numbers are placeholders.

## Goals

- Give customers a reliable, measured path to the 3 to 4 outcomes they choose, which lowers the risk of their investment in the product.
- Fund outcome-focused CS work with revenue, so CS's worth to the company shows up in bookings, not only in retention estimates.
- Report value delivered, per account and across the book, with evidence that the product delivered it.
- Give Marketing, Sales, Product, and CS one definition of value: the library.

## Non-goals (what it will not do)

- Guarantee outcomes, or refund on a missed target. Not in the first version (see open questions).
- Charge for support, bug fixes, or anything the product or the contract already owes the customer.
- Replace implementation or professional services. Configuration projects stay with Services. This offering is adoption and measurement.
- Set prices. Finance and Sales do. This spec sets the guardrails.
- Make measurement paid-only. Every customer gets the library, a baselined success plan, and the progress report.

## Inputs

| Source | What it provides | Access |
|---|---|---|
| [Outcome Library](../frameworks/outcome-library.md) | The outcomes on offer, their metrics, data sources, and features | Read |
| Success plans | Each customer's goals: baseline, target, latest value, customer-agreed value per unit | Read, plus confirmed writes by the CSM |
| Product analytics | Adoption of each feature an outcome depends on | Read |
| Customer systems, through integrations | The measurements behind each outcome | Read, with the customer's consent |
| CS time tracking | Hours spent per engagement | Read |
| CRM and billing | Offering bookings, renewal dates, ARR | Read |

## Packaging

| Tier | For | Includes | Price basis |
|---|---|---|---|
| Included | Every customer | The library, a success plan with baselines, the automated progress report, outcome-centered QBRs per the [QBR playbook](../playbooks/qbr.md) | Part of the subscription |
| Adoption as a Service | Customers who want a CS-led path to their outcomes | Everything included, plus: an adoption plan for each outcome built on the features behind it, monthly working sessions, diagnosis of adoption gaps and outcomes that aren't converting, a quarterly outcome review with the executive sponsor, and a value report for the customer's leadership | Annual fee |
| Outcome sprint | One outcome that is off track, or newly picked | A 90-day engagement on that outcome only | Fixed fee |

## Capabilities

| Capability | Description | Backing |
|---|---|---|
| Outcome selection and baselines | Help the customer pick outcomes and take baselines within 30 days | [Customer Onboarding](../playbooks/onboarding.md), [Outcome Library](../frameworks/outcome-library.md#success-plans-built-from-the-library) |
| Adoption plan | For each outcome, who must use which features, by when | The library's "Depends on" column, feature adoption data |
| Progress and diagnosis | Monthly status and reading for each goal: Proven, Unexplained progress, Adoption gap, or Not converting | [`tools/outcome_progress.py`](../tools/outcome_progress.py) |
| Executive value report | Each goal's movement from baseline, and the customer-agreed value of proven goals | [`tools/value_report.py`](../tools/value_report.py), run per account or across a book |
| Product feedback | Outcomes not converting at 2 or more accounts, taken to Product | [Outcome Review](../playbooks/outcome-review.md) |

## Pricing guardrails

Finance and Sales set the price. Whatever they set must hold to these:

1. **Cover the cost.** Price at or above the fully loaded CS time an engagement takes, at the target services margin. Track hours per engagement from the first pilot.
2. **Charge for the work, not the result.** In the first version, the fee does not depend on hitting a target.
3. **Don't charge for what is already owed.** An outcome blocked by a product gap is Product's to fix. Adoption gaps are in scope; bugs are not.
4. **Record giveaways.** If the offering is bundled free to win a deal, record it as a concession at list value, so CS's contribution stays visible.
5. **Sell only from the library.** Typical ranges are shown as ranges from past customers, never as a promise.
6. **Renew on evidence.** The offering's renewal conversation starts from the customer's value report.

## Outputs

- **Per account:** the success plan with a status and reading for each goal, a monthly progress update, and a quarterly executive value report.
- **Across the book:** the [value report](../tools/README.md#value-report): goals met or on track, proven goals, ARR on accounts with at least one proven outcome, the customer-agreed value of proven goals, and what the outcome review should look at. For the sample book as of 2026-10-01: 16 proven goals, $1.85M of $2.24M ARR with at least one proven outcome, and $625,500 of customer-agreed annual value.
- **The CS business case:** offering bookings and margin, the value report, and retention of offering customers compared with similar accounts. The [ROI calculator](../tools/README.md#roi-calculator) measures something else: the CS team's own efficiency with a copilot. Report them side by side, and don't add them together.

## Safety and trust

- **Measurements come from feeds, not from people.** Baselines and later values come from the outcome's data source. A manual correction is logged with who made it and why.
- **The customer signs off.** The customer owner agrees each baseline and target in writing.
- **Dollar values come from the customer.** Annual value per unit is recorded only when the customer agrees it, with who agreed and when. CS never invents one.
- **Only Proven goals are claimed** as value the product delivered, in any report, deck, or case study.
- **Marketing use needs permission.** Naming a customer's result needs their written permission. Anonymous aggregate claims need 5 or more accounts behind them.
- **No commitments without an owner.** Outcome guarantees or fee-at-risk terms need Legal and Finance. Claude drafts reports and plans; a person reviews and sends them, as in [Claude Drafts, People Decide](../essays/claude-drafts-people-decide.md).

## Failure modes

| Failure | Guard |
|---|---|
| The offering becomes a paywall on value, and customers who don't buy get worse service | Measurement stays in the Included tier, and health scoring treats every account the same |
| Selling it where the product can't deliver, so the customer pays for a miss | Check the outcome's record in the value report before selling. Don't sell an outcome Product has open as not converting |
| The revenue target bends the targets: CSMs set easy goals so everything looks on track | Targets below the library's typical range need CS manager review. The outcome review recalibrates ranges |
| Retention credit is overclaimed. Engaged customers buy the offering and also renew, whether or not it helped | Compare with similar accounts that didn't buy, and call the result a correlation |
| Value is inflated through generous per-unit values | Values are customer-agreed and recorded, and only Proven goals count |
| Sold beyond CS capacity | Track hours per engagement, and cap engagements per CSM |
| An outcome is sold before it can be measured automatically | It isn't in the library until it can be (the library's four tests) |

## Milestones

1. **M1:** Every new customer gets a success plan from the library, with baselines.
2. **M2:** Automated measurement for every library outcome, and a feature adoption feed.
3. **M3:** The value report goes to CS leadership monthly.
4. **M4:** Pilot the offering with 5 customers at a fixed fee, tracking hours.
5. **M5:** Set the price from pilot hours and results, launch, and start the quarterly [Outcome Review](../playbooks/outcome-review.md).

## Open questions

- **Should part of the fee depend on Proven outcomes?** Proposed: not until the library has 4 quarters of calibration data.
- **Who books the revenue: CS or Services?** Proposed: CS, so the value shows where the work happens.
- **Should customers see the readings?** Proposed: show adoption and progress, but not internal labels like "Unexplained progress". Explain them in plain words instead.
