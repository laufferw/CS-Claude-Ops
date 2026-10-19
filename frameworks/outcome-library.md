# Outcome Library

> Draft. The outcomes, metrics, and ranges below are for a fictional operations and billing platform, and every number is invented. Replace them with outcomes your product can move and you can measure.

## Purpose

A short, fixed list of measurable business outcomes that the company offers its customers and is prepared to prove. Each customer picks 3 to 4 for their success plan. A baseline is set at the start, and progress is measured from data, not reported from memory.

It gives the customer, CS, and Sales one definition of value. It also gives the Outcomes signal in [Account Health Scoring](account-health-scoring.md) something real to count.

## Inputs

| Input | Source | Example |
|---|---|---|
| The customer's priorities | Kickoff call, [handoff packet](../playbooks/sales-to-cs-handoff.md) | "We invoice two weeks late and lose track of billable charges" |
| Baseline measurement | The outcome's data source, at or before kickoff | Invoice cycle time of 9 days on 2026-01-10 |
| Ongoing measurements | The same source, read automatically | Invoice cycle time each month |
| Feature adoption | Product analytics | Share of each feature's target users who used it in the last 30 days |
| Results across customers | Past success plans | How much accounts that met an outcome improved it |

## What earns a place in the library

An outcome goes in the library only if all four of these are true:

1. **Defined metric.** A unit, a formula, and a direction, precise enough that two people measuring the same data get the same number.
2. **Measured automatically.** From product data or a customer system the product connects to, for the baseline and every month after. If someone has to compile it by hand, it is not provable yet.
3. **Linked to features.** Named product capabilities that move it, so adoption work aims at the outcome rather than at usage for its own sake.
4. **Evidence.** At least 3 customers have improved it by a meaningful amount. Until then it is a candidate, not an offer.

Keep the library to about 8 to 12 outcomes. A longer list stops being a menu a customer can choose from.

## The library

| ID | Outcome | Metric (unit) | Better when | Measured from | Depends on | Typical 12-month change |
|---|---|---|---|---|---|---|
| OL-01 | Faster invoicing | Days from work delivered to invoice sent | Lower | Billing module timestamps | Time capture, billing rules, invoice batching | 40 to 70% shorter |
| OL-02 | Less revenue leakage | Billable charges never invoiced, as a % of billable charges | Lower | Billing module vs. work records | Billing rules, charge capture, exception reports | 50 to 75% less |
| OL-03 | Faster collection | Days sales outstanding (DSO) | Lower | Accounts receivable integration | Payment portal, automated reminders | 10 to 25% shorter |
| OL-04 | Higher billable utilization | Billed hours as a % of available hours | Higher | Time tracking | Resource scheduling, time capture | 5 to 15 points higher |
| OL-05 | Margin control | Points between planned and actual project margin | Lower | Project budgets vs. actuals | Budgeting, forecast alerts | Gap cut by 40 to 60% |
| OL-06 | Faster month-end close | Business days to close the books | Lower | Close checklist completion dates | Reconciliation, period locking | 30 to 50% shorter |
| OL-07 | Less manual work | Hours per week spent on a named manual process | Lower | Workflow logs, before and after | Workflow automation, imports | 50 to 80% fewer hours |
| OL-08 | Fewer data errors | Records needing correction, as a % of records | Lower | Correction and edit logs | Validation rules, integrations | 50 to 70% fewer |
| OL-09 | Faster rollout to new teams | Days from a new team or site being added to live use | Lower | Provisioning and first-use dates | Templates, bulk provisioning | 40 to 60% shorter |
| OL-10 | Faster reporting | Time from request to delivered report (hours or days) | Lower | Report request and delivery logs | Dashboards, scheduled reports | 50 to 80% shorter |
| OL-11 | Faster approvals | Days from request to approval | Lower | Approval workflow timestamps | Approval workflows, mobile approvals | 40 to 70% shorter |

Typical changes are a check on whether a target is realistic. They are not a promise to the customer.

## Success plans built from the library

A [success plan](../playbooks/onboarding.md) holds **3 to 4 goals**, picked by the customer from the library for where they are in their journey now. Fewer leaves too little value proven. More spreads adoption work too thin to move any of them.

A plan may hold **one custom goal** (outcome ID `custom`) for something the library does not cover. It needs the same baseline, target, and measurement. If 3 or more accounts pick a similar custom goal, review it as a library candidate.

Each goal records:

| Field | Meaning |
|---|---|
| Outcome ID | From the library, or `custom` |
| Goal | The goal in the customer's words |
| Customer owner | The person at the customer accountable for it |
| Unit | The library metric's unit |
| Baseline value and date | Measured before work starts, within 30 days of kickoff |
| Target value and date | Agreed with the customer owner |
| Current value and date | The latest measurement. Blank until the first one after the baseline |
| Annual value per unit (optional) | What the customer agrees one unit of improvement is worth per year, such as $2,750 per weekly hour saved. Blank unless the customer agreed it |

[`sample-data/success-plans.csv`](../sample-data/success-plans.csv) has this format.

When a goal is met and the customer picks the next one, move the met goal to the account's value history. It stays evidence for the renewal, but stops counting toward the Outcomes signal.

## Measuring progress

**Progress** = (current - baseline) / (target - baseline). The same formula works whether lower or higher is better.

**Expected progress** = the share of the time from baseline date to target date that had passed when the current value was measured.

Each goal gets the first status in this table that applies:

| Status | Rule | Counts toward the Outcomes signal |
|---|---|---|
| No baseline | Baseline value or date is missing | No. It is a data gap |
| Stale | The latest measurement (the baseline, if there is no current value) is more than 60 days old | No. It is a data gap |
| Met | Progress is 100% or more | Yes, as on track |
| Missed | The target date has passed and the goal is not met | Yes, as not on track |
| On track | Progress is no more than 25 points behind expected progress | Yes, as on track |
| Off track | Anything else | Yes, as not on track |

The 25-point tolerance is there because outcomes rarely improve in a straight line. Results lag adoption by weeks or months.

The Outcomes signal is the share of counted goals that are Met or On track (see [Account Health Scoring](account-health-scoring.md#signal-rubric)). An account with no counted goals has no measured outcomes, which caps its band at Yellow.

[`tools/outcome_progress.py`](../tools/outcome_progress.py) applies these rules and writes the per-goal report.

## Checking adoption behind each outcome

A goal's number can move for reasons that have nothing to do with the product, and a goal can stall even when the product is used well. So each counted goal is checked against adoption of the features its outcome depends on (the library's "Depends on" column).

A feature is **lightly used** when fewer than 40% of its target users used it in the last 30 days. An outcome is **Supported** when more than half of its features with adoption data are not lightly used, and **Unsupported** otherwise. With no adoption data for any of its features, support is **Unknown**. Custom goals have no feature link, so they are not checked.

Status and support together give each counted goal a reading:

| | Features in use (Supported) | Features lightly used (Unsupported) |
|---|---|---|
| **Met or On track** | **Proven.** Cite it as our result | **Unexplained progress.** The number moved, but not through the product. Find out why before claiming it |
| **Off track or Missed** | **Not converting.** The features are used but the number isn't moving. Check configuration and process with the customer. If it happens at 2 or more accounts, it goes to Product through the [Outcome Review](../playbooks/outcome-review.md) | **Adoption gap.** The fix is adoption work on the named lightly used features |

Only Proven goals count as evidence that the product delivered: in QBRs, renewal value stories, the [value report](../specs/adoption-as-a-service.md#outputs), and marketing. Goals with Unknown support are reported as data gaps until adoption data exists.

With `--adoption`, `outcome_progress.py` adds each goal's support, its lightly used features, and its reading.

## Outputs

- A success plan for each account: 3 to 4 goals, each with a baseline, a target, and the latest measurement
- A per-goal progress report for QBRs, renewal value stories, and expansion evidence, with an adoption reading for each goal
- The Outcomes signal and the no-measured-outcomes override in [Account Health Scoring](account-health-scoring.md)
- Across the book: which outcomes customers pick and how often they are met, as evidence for Sales, Marketing, and Product

## Worked example

Cedar Health Partners, from the [sample success plans](../sample-data/success-plans.csv), as of 2026-10-01. The baseline date for every goal is 2026-01-20.

| Outcome | Goal | Baseline | Target (date) | Current (date) | Progress | Expected | Status |
|---|---|---|---|---|---|---|---|
| OL-06 | Close the books in 6 business days | 12 | 6 (2026-09-30) | 10 (2026-09-25) | 33% | 98% | Missed |
| OL-08 | Cut patient billing records that need correcting | 7.5% | 3.0% (2026-12-31) | 7.0% (2026-09-15) | 11% | 69% | Off track |
| OL-03 | Collect payer invoices faster | 58 days | 45 (2026-12-31) | 51 (2026-09-15) | 54% | 69% | On track |
| OL-11 | Approve supply requests in 2 days | 6 days | 2 (2026-11-30) | 5.5 (2026-09-15) | 13% | 76% | Off track |

Collection (OL-03) step by step: progress is (51 - 58) / (45 - 58) = 7 / 13 = 54%. On 2026-09-15, 238 of the 345 days from baseline to target had passed, so expected progress is 69%. 54 is within 25 points of 69, so the goal is On track.

The close goal (OL-06) passed its target date without being met, so it is Missed whatever its progress.

One of four goals counts as on track, so Cedar's Outcomes signal is 25. Every goal has a baseline and a recent measurement, so the QBR can show the customer each number.

The adoption check splits the three goals that are behind into two different problems:

| Outcome | Status | Features (adoption) | Reading |
|---|---|---|---|
| OL-06 | Missed | Reconciliation 22%, period locking 15% | Adoption gap |
| OL-08 | Off track | Validation rules 30%, integrations 35% | Adoption gap |
| OL-03 | On track | Payment portal 74%, automated reminders 80% | Proven |
| OL-11 | Off track | Approval workflows 82%, mobile approvals 58% | Not converting |

Two goals need adoption work on four named features. The approvals goal needs something else: the features are in use, so the CSM checks how approvals are configured and routed before asking anyone to use the product more.

The sample data has the other statuses too. Riverbend Credit Union's goals were last measured in June, so all four are Stale, and its band is capped at Yellow. One of Sable Energy's goals never had a baseline, so it is left out of the count and listed as a data gap.

## Failure modes

- **The library grows into a feature list.** Every request becomes an outcome, and the menu stops being a menu. The four tests and the cap of about 12 guard against this.
- **Baselines set late or guessed.** A baseline taken after the product has already moved the number understates value. One estimated by hand can't be compared with automated measurements. Take it within 30 days of kickoff, from the same source as every later measurement.
- **Easy targets, so everything is on track.** Check targets against the typical range. A CS manager reviews any target below the bottom of the range.
- **Claiming credit for moves the product didn't make.** The customer's number can move because of a reorg or a new hire. The adoption check marks such goals Unexplained progress, and only Proven goals count as our result.
- **Adoption data that measures logins, not use.** "Used the feature" must mean doing the work in it, such as approving a request, not opening the screen. Otherwise every goal looks Supported.
- **A broken data feed makes goals go quiet.** Stale is a status, it shows as a data gap, and an account with no measured outcomes cannot be Green.
- **Goals picked for the CSM's convenience.** The customer picks, and every goal has a customer-side owner.
- **Typical ranges sold as guarantees.** They are evidence, not commitments. Any promised result goes through Sales and Legal, like any other commitment.

## Calibration

Each quarter, for each outcome: how many plans picked it, the share met by their target date, and the median improvement. Update the typical ranges from those results. Retire outcomes that are rarely picked or can't be measured reliably, and promote custom goals that recur with evidence.

Check the tolerance too. If many goals marked On track halfway to their target end up Missed, tighten the 25 points.

Check the feature lists. An outcome that is often Not converting despite good adoption either depends on features the list leaves out, or has a product gap. The [Outcome Review](../playbooks/outcome-review.md) decides which. Check the 40% light-use threshold the same way: Proven goals should rarely sit on features just above it.
