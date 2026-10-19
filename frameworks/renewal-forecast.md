# Renewal Forecast

> Draft. The category weights are starting points. Replace them with your own close rates once you have 4 quarters of forecast history.

## Purpose

A renewal forecast by quarter that a CS leader can defend: what is committed, what could renew, and what is likely lost. It sets each CSM's call next to what the account data says, so the forecast review spends its time on the disagreements instead of reading every account aloud.

## Inputs

| Input | Source | Example |
|---|---|---|
| Accounts renewing in the forecast quarters | CRM | Renewal date, ARR |
| Health band, red flags, contract flags, open escalations | [Account Health Scoring](account-health-scoring.md) | Red, payment dispute |
| The CSM's call and expected ARR | The CSM, weekly | Commit at $233,333 (a known downgrade to 250 seats) |

[`sample-data/forecast-calls.csv`](../sample-data/forecast-calls.csv) has the call format: account, call, expected ARR, and a one-line note.

## Categories

Each renewing account gets a category from its signals, checked in this order:

| Category | Signals say this when | Weight |
|---|---|---|
| Lost | Notice of non-renewal | 0% |
| At risk | Red band, or a sponsor departure or payment dispute | 40% |
| Commit | Green band, no open contract flags, and no open escalations | 95% |
| Best case | Anything else: Yellow, Insufficient data, or Green with a contract flag or escalation | 70% |

The CSM's call replaces the signal category when there is one, because the CSM knows things the data doesn't, such as a verbal yes or a budget freeze. **Expected ARR** is the CSM's number if they gave one. Otherwise it is current ARR, or zero for Lost.

Each call is compared with the signals:

- **Call above signals:** the CSM is more optimistic than the data. Review these first. They are where forecasts go wrong.
- **Call below signals:** the CSM knows something bad the data doesn't show yet. Ask what it is, and whether a red flag or note is missing from the CRM.
- **No call:** the signal category is used until the CSM makes one.

## Forecast numbers

For each quarter:

| Number | Calculation |
|---|---|
| Up for renewal | Current ARR of every account renewing in the quarter |
| Commit | Expected ARR of Commit accounts |
| Best case | Commit plus expected ARR of Best case accounts |
| Weighted | Sum of expected ARR x category weight |
| Lost | Current ARR of Lost accounts |
| Known downgrades | Current ARR minus expected ARR, where expected is lower and the account isn't Lost |

At risk accounts count in the weighted number only. They are never in Commit or Best case until something changes.

## Outputs

- The forecast by quarter, with the six numbers above
- Each renewing account: band, signal category, CSM call, expected ARR, and whether the call disagrees with the signals
- A list of calls to review, most optimistic first

[`tools/renewal_forecast.py`](../tools/renewal_forecast.py) produces all of these. The [Weekly Team Review](../playbooks/weekly-team-review.md) is where they get discussed.

## Worked example

The sample book as of 2026-10-01, for 2026-Q4:

| Account | ARR | Band | Signals say | CSM call | Expected ARR |
|---|---|---|---|---|---|
| Orchard Learning | $38,000 | Green | Commit | Commit | $38,000 |
| Larkspur Retail | $60,000 | Yellow | At risk (payment dispute) | Best case | $60,000 |
| Cedar Health Partners | $410,000 | Red | At risk | At risk | $410,000 |
| Sable Energy | $280,000 | Yellow | Best case | Commit | $233,333 |

Commit is $38,000 + $233,333 = $271,333. Best case adds Larkspur: $331,333. Weighted is $38,000 x 95% + $233,333 x 95% + $60,000 x 70% + $410,000 x 40% = $463,766, which is 59% of the $788,000 up for renewal. The downgrade Sam expects at Sable is $46,667.

Two of the four calls are above the signals. Sable is called Commit while it's Yellow with a downgrade request, and Larkspur is called Best case during a payment dispute. Those are the first two questions in the review.

## Failure modes

- **Calls drift up as the quarter ends.** Comparing every call with the signals makes optimism visible. Track how often "call above signals" accounts actually renew.
- **Commit includes downgrades at full ARR.** Expected ARR exists to catch this. Ask for it on every account with a contract flag.
- **Stale bands.** The forecast is only as current as the scoring run. Rerun both on the same day.
- **Weights treated as truth.** 95/70/40 are placeholders. Replace them with the share of each category's ARR that actually renewed.
- **At risk ignored because it's not in Best case.** It's still in the weighted number, and it's the work list for save plans.

## Calibration

Each quarter, for each category, compare forecast ARR at the start of the quarter with what renewed. Set each weight to that share once you have 4 quarters. Also report **forecast accuracy**: actual renewed ARR divided by the weighted forecast at the start of the quarter. See the [CS Metrics Scorecard](cs-metrics-scorecard.md).
