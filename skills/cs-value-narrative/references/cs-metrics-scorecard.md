# CS Metrics Scorecard

> Draft. Formulas are exact; targets are yours to set. Agree each definition with Finance before the scorecard goes to the board, so the CS numbers and the company numbers match.

## Purpose

One page of CS metrics with fixed definitions, for a VP or COO to run the function and report it upward. Each metric says what it counts, where the data comes from, and how it gets gamed. A metric that two people calculate differently is an argument, not a metric.

## Inputs

| Input | Source | Example |
|---|---|---|
| Renewal history: ARR before and after each renewal, and the outcome | CRM or billing | Granite: $110,000 to $95,000, Downgraded, `commercial` |
| The scored book | [Account Health Scoring](https://github.com/laufferw/outcome-led-cs-ops/blob/main/frameworks/account-health-scoring.md) | Bands and red flags for every account |
| Success plans and feature adoption | [Outcome Library](outcome-library.md) | Goal statuses and readings |
| Forecast calls | [Renewal Forecast](https://github.com/laufferw/outcome-led-cs-ops/blob/main/frameworks/renewal-forecast.md) | Each CSM's call and expected ARR |
| Capacity settings | [Capacity Model](https://github.com/laufferw/outcome-led-cs-ops/blob/main/frameworks/capacity-model.md) | Hours per account and per CSM |

[`sample-data/renewal-history.csv`](https://github.com/laufferw/outcome-led-cs-ops/blob/main/sample-data/renewal-history.csv) has the history format.

## The metrics

### Retention

Calculated over the renewals due in the trailing 12 months. These are **renewal-cohort** rates: they count ARR that came up for renewal, not every change during a contract term. If Finance reports company-wide GRR and NRR on all ARR, show both and label them.

| Metric | Formula | Gamed by |
|---|---|---|
| Gross renewal rate (GRR) | Sum of min(ARR before, ARR after) / sum of ARR before | Pushing renewal dates out of the period. Report renewals that slipped |
| Net renewal rate (NRR) | Sum of ARR after / sum of ARR before | Counting expansion that Sales sold as CS retention. Report GRR next to it, always |
| Logo retention | Accounts that renewed / accounts due | Splitting or merging accounts. Count by contract, consistently |
| ARR lost by reason | Lost ARR grouped by [root cause tag](https://github.com/laufferw/outcome-led-cs-ops/blob/main/frameworks/escalation-logic.md#root-cause-tags) | Tagging everything `customer-org-change`. Review tags monthly |

### Book health

| Metric | Formula | Gamed by |
|---|---|---|
| ARR by band | ARR in Green, Yellow, Red, and Insufficient data, as shares of total | CSM overrides to Green. Overrides are reviewed monthly |
| ARR at risk | ARR in Red, or with any red flag | Not recording red flags. Compare with the notes |

### Value realized

| Metric | Formula | Gamed by |
|---|---|---|
| Baselined plan coverage | Accounts with at least one baselined success plan goal / all accounts, and the same by ARR | Plans with one token goal. Check plans hold 3 to 4 goals |
| Goals met or on track | Met + On track / counted goals | Easy targets. Targets below the library's typical range get reviewed |
| Goals proven | Proven goals / counted goals | Adoption measured as logins. "Used" must mean doing the work |
| ARR with a proven outcome | ARR of accounts with at least one Proven goal / total ARR | One easy goal per account. Look at goals proven too |
| Time to first value | Median days from close to first value, for accounts closed in the period | Defining first value loosely. Use the [onboarding](https://github.com/laufferw/outcome-led-cs-ops/blob/main/playbooks/onboarding.md) definition |

### Forecast

| Metric | Formula | Gamed by |
|---|---|---|
| Commit and weighted forecast, current quarter | Per the [Renewal Forecast](https://github.com/laufferw/outcome-led-cs-ops/blob/main/frameworks/renewal-forecast.md) | Optimistic calls. Count calls above signals |
| Forecast accuracy | Renewed ARR, excluding expansion, / weighted forecast at the start of the quarter. Over 100% means too cautious | Re-forecasting mid-quarter. Measure against the start-of-quarter number |

### Capacity

| Metric | Formula | Gamed by |
|---|---|---|
| Team utilization | Total workload hours / (CSMs x hours per CSM) | Guessed hours. Recalibrate with time studies |
| CSMs needed | Total workload / (hours per CSM x target utilization) | Same |
| ARR per CSM | Total ARR / CSMs | Ignoring segment mix. Read it next to utilization |

## Scale segment

For a book covered one-to-many: a pooled team or a program owner runs onboarding, education, and campaigns across hundreds of accounts, and no CSM owns each one. Those accounts rarely have success plans, so the value realized section above has little to count. Report a scale book on retention, forecast, and capacity as above, and use this section in place of value realized. For a scale owner it is the whole scorecard, not an addition to it.

Every number here is reported for the whole book, not for the accounts a program touched. A program that only improves the accounts it picked hasn't shown it moved the book.

### Scale inputs

| Input | Source | Example |
|---|---|---|
| Build activity by user | Product analytics | User 4411 at Harbor Supply published a change to an app on 2026-09-14 |
| App runs and viewers | Product analytics | Harbor's "Returns intake" app ran 1,200 times last week, used by 14 people |
| Learning path starts and completions | Learning platform (LMS) | 38 users at Harbor started "Build your first app"; 22 finished |
| Live session registrations and attendance | Webinar or event platform | 61 registered for the October office hours; 40 stayed at least half |
| Sends, target actions, and holdouts per campaign | Comms platform and product analytics | 2,000 sent, 200 held out; target action: publish an app within 14 days |
| Program log | CS Ops | Which account entered which program, when, and why |
| Motion register | CS Ops | Each motion, the book it started on, its result against its holdout, and where else it runs |

Define "build", "active", and "load-bearing" with Product before the first report, from actions that do work in the product. Logins and page views never count.

### Retention: the north star

| Metric | Formula | Gamed by |
|---|---|---|
| Gross renewal rate (GRR) | As above, for the renewals due on the scale book | As above |
| Gross dollar retention (DRR) | Sum, over accounts on the book 12 months ago, of min(ARR then, ARR now) / their ARR then | Moving shrinking accounts out of the book. Fix the book at the start of the period |

Use GRR where contracts renew annually. Use DRR where billing is monthly or usage-based, because a renewal cohort misses contraction between renewals. Pick one per segment, label it, and don't switch between reports. NRR still goes next to it, but GRR or DRR is the number the scale owner answers for.

### Builders and apps: impact across the book

| Metric | Formula | Gamed by |
|---|---|---|
| Net active builders | Active builders at period end − active builders at period start, across every account in the book. Show gross added and gross lost next to it | Counting trivial edits as building. Use the agreed build actions only |
| Net load-bearing apps | Load-bearing apps at period end − at period start. Show gross added and gross lost | Splitting one app into several. Read it next to accounts with a load-bearing app |
| Accounts with a load-bearing app | Accounts with at least one load-bearing app / accounts in the book, and the same by ARR | One token app per account. Look at net load-bearing apps too |

An **active builder** is a user who did an agreed build action in the last 28 days. A **load-bearing app** is one the customer depends on: used by at least 3 people besides its builder, or run on a schedule, in each of the last 4 weeks. Both thresholds are placeholders; set yours from the back-test under [Calibration](#calibration).

For a scale account with no success plan, its first load-bearing app is its **first value**. Net builders measure activity; load-bearing apps are the nearest a scale book gets to the outcomes in the value realized section, so lead with them.

### Education

| Metric | Formula | Gamed by |
|---|---|---|
| Learning path completion | Users who finished a path within 60 days of starting it / users who started it, per path | Counting enrolments, or shortening paths. Report starts next to completions, and path length |
| Live session engagement | Attendees who stayed at least half the session / registrants. Also: accounts with at least one attendee this quarter / accounts in the book | Counting registrations. Count attendance |
| Time to first value, educated vs. not | Median days from an account's start to first value, for accounts where a user finished a path within 30 days of start, and separately for accounts where no one did. Show both counts | Reading the gap as education's effect. See below |

Accounts that take training are often the ones that would have succeeded anyway, so the gap between the two cohorts is a correlation, not a measure of what education did. Compare like with like (same size band, same start month) and say "correlation". For a causal answer, invite a random half of new accounts to a path first and compare the halves.

### Programs

| Metric | Formula | Gamed by |
|---|---|---|
| Onboarding completion | Accounts that met the scale exit criteria within 90 days of start / accounts that started in the period, by start month | Lowering the exit criteria. Change them only with a dated note |
| Comms performance | Per campaign: action rate of recipients minus action rate of the holdout, where the action is the campaign's target action in the product within 14 days | Reporting opens and clicks. Use them only to diagnose a campaign, never as its result |
| Re-engagement conversion | Accounts back to active within 60 days of entering a re-engagement program / accounts that entered, compared with a holdout | Entering accounts that would have come back anyway, such as seasonal dips. The holdout catches it |

Scale onboarding exit criteria: at least one active builder in week 4 or later, and first value within 90 days. Re-engagement entry is a [trend break](https://github.com/laufferw/outcome-led-cs-ops/blob/main/frameworks/account-health-scoring.md) or no active builders for 30 days; back to active means at least one active builder in each of 4 consecutive weeks.

Every campaign and program keeps a random **holdout** of 10% of eligible accounts that gets nothing from it. Without one, comms and re-engagement numbers count the customers who would have acted anyway.

### Leverage

| Metric | Formula | Gamed by |
|---|---|---|
| Graduated motions | Motions first run on this book that the CS manager adopted as a team standard this period | Renaming small changes as new motions. A motion graduates only on a result against its holdout |
| Accounts reached by graduated motions | Accounts outside the originating book that a graduated motion ran on this period | Running it everywhere without checking it still works. Each new book keeps a holdout |

A **motion** is a repeatable piece of work: a campaign, a session format, a template, a re-engagement play. It **graduates** when the CS manager adds it to a playbook or the team's program calendar, on evidence that it beat its holdout on the original book, and at least one other owner runs it. The decision is made at the [Weekly Team Review](https://github.com/laufferw/outcome-led-cs-ops/blob/main/playbooks/weekly-team-review.md) or the [Outcome Review](https://github.com/laufferw/outcome-led-cs-ops/blob/main/playbooks/outcome-review.md), not by the metric.

### Scale worked example

A fictional scale book of 400 accounts and $3.2M ARR, for the quarter to 2026-09-30.

- **DRR:** accounts on the book 12 months ago had $3,000,000 ARR. Capped at that, $2,730,000 remains: 91.0%.
- **Net active builders:** 1,150 at the start, 310 gained, 190 lost: 1,270, net +120.
- **Net load-bearing apps:** 520 at the start, 80 gained, 25 lost: 575, net +55. 236 of 400 accounts (59.0%) have at least one, $2,080,000 of ARR (65.0%).
- **Time to first value:** of 140 accounts that started in the first half, 52 had a user finish a path within 30 days, with a median of 24 days to first value. The other 88 took a median of 41. Correlation, not proof that the path saved 17 days.
- **Re-engagement:** 21 of 60 accounts in the program were back to active within 60 days (35.0%), against 3 of 15 in the holdout (20.0%). Fifteen points of lift, on samples small enough that one quarter can't settle it.

## Outputs

- A one-page scorecard: retention, book health, value realized, forecast, and capacity, each number shown with its calculation
- A trend when run each month, compared with last month and last quarter

- For a scale book: retention, builders and apps, education, programs, and leverage, in place of value realized

[`tools/cs_scorecard.py`](https://github.com/laufferw/outcome-led-cs-ops/blob/main/tools/cs_scorecard.py) computes everything except time to first value, which needs close dates and first-value dates the sample data doesn't hold, and the scale segment metrics, which need product, learning, and comms data the sample doesn't hold. Forecast accuracy comes from past forecasts in [`sample-data/forecast-history.csv`](https://github.com/laufferw/outcome-led-cs-ops/blob/main/sample-data/forecast-history.csv). [`tools/forecast_backtest.py`](https://github.com/laufferw/outcome-led-cs-ops/blob/main/tools/forecast_backtest.py) breaks it down by quarter and category.

## Worked example

The sample as of 2026-10-01. Fourteen accounts were due to renew in the 12 months before: the 12 in the book, plus Aspen Freight and Cobalt Studios, which churned.

- **GRR:** $2,307,000 was up for renewal. Losses were Aspen ($120,000, `product-gap`), Cobalt ($45,000, `sponsor-change`), and Granite's downgrade ($15,000, `commercial`). $2,127,000 kept is 92.2%.
- **NRR:** expansion at Bluefin, Orchard, and Pinecrest brought ARR after renewal to $2,240,000: 97.1%.
- **Logo retention:** 12 of 14, 85.7%.
- **Value:** 16 of 35 counted goals are proven, and 82.6% of ARR sits on accounts with at least one proven outcome.

Dogwood Partners churned in August 2025, before the 12-month window, so it isn't counted.

## Failure modes

- **Definitions that differ from Finance's.** The board sees two retention numbers and trusts neither. Agree definitions before the first report.
- **NRR without GRR.** Expansion can hide churn. Always show both.
- **Too many metrics.** This page is the whole scorecard. Add a metric only if someone will act differently because of it.
- **Small samples.** A quarter with five renewals swings GRR by 10 points on one account. Use the trailing 12 months, and show the count.
- **Value metrics without the adoption check.** Goals on track can be luck. Lead with goals proven.
- **Scale programs without holdouts.** Comms and re-engagement get credit for customers who would have acted anyway. Keep a holdout on every program.
- **Activity reported as value on a scale book.** Builders and session attendance can rise while nothing the customer depends on changes. Lead with load-bearing apps and DRR.
- **Scale accounts scored as if a CSM owned them.** With no success plan, [health scoring](https://github.com/laufferw/outcome-led-cs-ops/blob/main/frameworks/account-health-scoring.md) caps an account at Yellow, so the whole segment looks unhealthy. Agree how scale accounts are scored, for example a self-serve success plan or load-bearing apps as the outcomes signal, before they enter the scorecard's book health.

## Calibration

Each quarter, check the scorecard against what Finance reports, reconcile any difference, and record why. Once a year, ask of each metric: did anyone make a decision with it? Drop the ones nobody used.

For a scale book, back-test the definitions once a year: did accounts with a load-bearing app retain better than similar accounts without one? If they didn't, the threshold is counting the wrong apps. Change it, and restate last year's numbers on the new definition.
