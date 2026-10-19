# Prompt: Account Review

## Purpose

Produce a one-page review of a single account for a CSM or manager.

## Inputs

- Account name and ARR
- Renewal date
- Health index and band (see [Account Health Scoring](account-health-scoring.md))
- Usage trend, open tickets, recent meeting notes, key contacts

## Prompt

```
You are a Customer Success analyst. Using only the data below, write a one-page account review.

Structure:
1. Snapshot (ARR, renewal date, health band)
2. What is going well (evidence only)
3. Risks (each with the evidence and how serious it is)
4. Stakeholder map (who we have, who is missing)
5. Recommended next three actions, each with an owner and a date
6. Data gaps that limit this review

Rules:
- Do not invent facts. If the data does not say, write "unknown".
- Separate facts from your judgment.
- Keep it under 400 words.

DATA:
{paste data here}
```

## Output format

Short sections with bullets. Actions are numbered.

## Known failure modes

- Fills gaps with plausible-sounding guesses. The "unknown" rule reduces this.
- Over-weights the most recent note. Include notes from the last 90 days.
