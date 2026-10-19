# Prompt: Team Brief

## Purpose

Draft a CS director's weekly brief across the whole team, from the team rollup and the renewal forecast: where revenue is at risk, which forecast calls to challenge, who needs help, and what to decide. It is the agenda for the [Weekly Team Review](../playbooks/weekly-team-review.md).

## Inputs

- The output of [`tools/team_rollup.py`](../tools/team_rollup.py), with capacity
- The output of [`tools/renewal_forecast.py`](../tools/renewal_forecast.py), with this week's calls
- Last week's action list, if any

## Prompt

```
You are helping a CS director prepare the weekly team review. Use only the material below.

Write these sections:

1. Headline (two sentences): the forecast for the current quarter (commit and weighted against up for renewal) and the single biggest risk.
2. Calls to challenge: every call above signals, largest ARR first. For each: account, CSM, the call, what the signals say, and the one question to ask.
3. Risk by CSM: for each CSM with ARR at risk or band drops, the accounts and what they need from the director (an escalation, a sponsor meeting, a save plan review). Skip CSMs with nothing at risk.
4. Capacity: anyone over the utilization target or under half of it, and a suggested move. Say if no move is needed.
5. Data gaps: CSMs whose books have growing data gaps, and what to fix.
6. Last week's actions: done, not done, and why, if the material says.

Rules:
- Every claim cites a number from the rollup or forecast.
- Do not judge CSM performance from utilization or band counts. Describe the book, not the person.
- Do not propose pricing, discounts, or contract terms.
- Keep it under 400 words.

TEAM ROLLUP:
{paste here}

FORECAST:
{paste here}

LAST WEEK'S ACTIONS:
{paste here, or "none"}
```

## Output format

Six headed sections. Sections 2 and 3 are bullet lists. A section with nothing in it says "Nothing this week."

## Example

For the sample team as of 2026-10-01, a correct brief opens with 2026-Q4: $271,333 commit and $463,766 weighted of $788,000 up for renewal, and names Cedar Health Partners ($410,000, Red) as the biggest risk. Calls to challenge are Sable Energy (Commit against Best case signals), Granite Payroll, and Larkspur Retail (Best case against At risk). Risk sits entirely with Sam Example: $637,000 at risk across four accounts. Capacity notes Sam at 73% while Priya and Jordan are under half of target, and suggests Priya take on part of Sam's load.

## Known failure modes

- Reads like a status report on every account. The sections limit it to disagreements, risk, capacity, and gaps.
- Treats a heavy book as a weak CSM. The rules forbid judging performance from these numbers.
- Skips the calls to challenge because they're uncomfortable. Section 2 is required whenever the forecast lists them.
