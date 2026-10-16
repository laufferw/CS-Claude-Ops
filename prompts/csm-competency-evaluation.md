# Prompt: CSM Competency Evaluation

## Purpose

Gather evidence from a CSM's real work against the [CSM Competency Framework](../frameworks/csm-competency-framework.md), so a manager's coaching or promotion conversation starts from examples, not impressions.

> The output is evidence for a manager to weigh. It is not a rating, and it should not be the only input to a promotion or performance decision.

## Inputs

- The competency framework (areas, levels, and any example behaviors)
- Work samples from at least three accounts: account plans, call notes, customer emails, escalation write-ups, QBR decks
- The CSM's current level, if the review is for promotion

## Prompt

```
You are helping a Customer Success manager prepare a coaching conversation. Using only the framework and work samples below, gather evidence for each competency area.

For each of the six areas (Customer outcomes, Relationship depth, Commercial acumen, Risk management, Operational rigor, Communication):
1. Evidence: up to three specific examples, each citing the sample it comes from (account and document)
2. The level the evidence best matches (1 Developing, 2 Proficient, 3 Advanced, 4 Leading), with one sentence on why
   - If there is too little evidence to judge, write "Insufficient evidence" and say what kind of sample would show it
3. One concrete development suggestion tied to the evidence

Then:
- The two strongest areas and the two with the most room to grow
- Any area where the samples conflict (strong on one account, weak on another)

Rules:
- Evidence first. Never suggest a level without at least one cited example.
- Judge what the CSM did, not how they wrote it. Tone and style are not evidence unless the area is Communication.
- Do not treat time in role as evidence of level.
- If all samples come from one account, say so and treat every level as provisional.

FRAMEWORK:
{paste the framework}

WORK SAMPLES:
{paste samples, each labeled with account and document type}
```

## Output format

Six labeled sections, each with evidence, a suggested level, and a development suggestion, followed by the strengths, growth areas, and conflicts.

## Known failure modes

- Rates on writing polish instead of what happened. The rules separate style from substance, but check the evidence lists for it.
- Over-reads a single strong example. Three examples per area, from several accounts, is the target.
- The framework only has example behaviors for Risk management, so levels in other areas rest on the general level descriptions. Treat those suggestions as rougher until the framework fills them in.
- Fills in a level for every area even when the samples don't cover it. "Insufficient evidence" is a valid answer and should appear.
