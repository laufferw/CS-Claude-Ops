# Prompt: Churn Risk Triage

## Purpose

Rank a list of accounts by churn risk and explain the top drivers for each.

## Inputs

A table of accounts with: ARR, renewal date, health index, usage trend, open escalations, last exec contact date.

## Prompt

```
You are a Customer Success analyst. Review the accounts below and triage them for churn risk.

For each account return:
- Risk: High, Medium, or Low
- Top two drivers, citing the specific data points
- One recommended action with a suggested owner

Then list the five accounts I should look at first, ordered by (ARR at risk x urgency).

Rules:
- Use only the data provided.
- If key data is missing for an account, mark the risk "Unclear" and say what is missing.
- Do not assign High risk on a single weak signal.

ACCOUNTS:
{paste table here}
```

## Output format

A table, followed by a short ranked list.

## Known failure modes

- Treats missing data as bad news. The "Unclear" rule handles this.
- Ranks by ARR alone. The prompt asks for urgency too.
