# Capacity Model

> Draft. The hours per account are invented. Replace them with a time study of your own team before using them in a headcount request.

## Purpose

Turn a book of accounts into weekly CSM hours, so a director can see who is overloaded, rebalance books, and back a headcount request with numbers instead of a feeling.

## Inputs

| Input | Source | Example |
|---|---|---|
| Each account's ARR, band, red flags, and renewal date | Scored book from [Account Health Scoring](account-health-scoring.md) | Cedar: $410,000, Red, renewing in 75 days |
| Hours per account by segment | A time study | Enterprise accounts take 3 hours a week |
| Extra hours for at-risk accounts and renewals | A time study | +2 hours while at risk |
| Hours each CSM has for account work, and the utilization target | CS leadership | 30 hours a week, 85% target |

[`sample-data/capacity-inputs.json`](../sample-data/capacity-inputs.json) holds these settings.

## The model

Each account's weekly hours = its segment's base hours, plus extras that apply:

| Segment | ARR | Base hours a week |
|---|---|---|
| Enterprise | $200,000 or more | 3.0 |
| Mid-market | $75,000 to $199,999 | 1.5 |
| SMB | Under $75,000 | 0.5 |

| Extra | Applies when | Hours |
|---|---|---|
| At risk | Red band, or any red flag | +2.0 |
| Renewal | Renewing within 120 days | +1.0 |

A CSM's **workload** is the sum over their accounts. **Utilization** = workload / hours available for account work. The **CSMs needed** for a book = total workload / (hours per CSM x utilization target).

The target is below 100% on purpose. Weeks with an escalation, a new account, or a sick day need slack, and a team planned at 100% is late on everything.

## Outputs

- Each CSM's workload and utilization, next to their book's health, renewals, and outcomes
- CSMs over target, and CSMs under half of target
- The headcount the book needs at the target

[`tools/team_rollup.py`](../tools/team_rollup.py) produces these, and [`tools/cs_scorecard.py`](../tools/cs_scorecard.py) carries the team figures.

## Worked example

Sam Example's book in the sample, as of 2026-10-01:

| Account | Segment | Base | At risk | Renewal | Hours |
|---|---|---|---|---|---|
| Cedar Health Partners | Enterprise | 3.0 | +2 (Red) | +1 | 6.0 |
| Sable Energy | Enterprise | 3.0 | | +1 | 4.0 |
| Granite Payroll | Mid-market | 1.5 | +2 (sponsor left) | | 3.5 |
| Riverbend Credit Union | Mid-market | 1.5 | | | 1.5 |
| Larkspur Retail | SMB | 0.5 | +2 (payment dispute) | +1 | 3.5 |
| Quarry Lane Media | SMB | 0.5 | +2 (non-renewal) | +1 | 3.5 |

That is 22 hours a week, 73% of 30. The whole book needs 33 hours, or 1.3 CSMs at an 85% target. The sample is tiny: a real book has 30 to 80 accounts. What it does show is the imbalance. Sam carries 22 of the 33 hours, and every at-risk account.

## Failure modes

- **Guessed hours.** Teams underestimate the time hard accounts take. Base the hours on a time study of a sample of weeks.
- **ARR as the only segment.** A small account with a complex integration can take more time than a large, quiet one. Add an extra for the cause, or override the account's segment.
- **Rebalancing by hours alone.** Moving an account breaks a relationship. Move accounts at natural points, such as after a renewal, and never in the middle of a save.
- **Utilization read as performance.** High utilization means a heavy book, not a good CSM. Use the competency framework for performance.
- **Headcount math without the ramp.** A new CSM takes months to carry a full book. Plan hires ahead of the need.

## Calibration

Twice a year, have CSMs log their time for two weeks. Compare the actual hours per account with the model by segment, and update the base hours and extras. Check that the accounts needing the most real time are the ones the model weights highest.
