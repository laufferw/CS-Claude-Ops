# Prompt: Value Narrative

## Purpose

Write the story of the value delivered, from the numbers in a value report: for a customer's executive (one account), or for CS leadership, the exec team, or the board (a whole book). Only proven results are claimed. The [Adoption as a Service](https://github.com/laufferw/outcome-led-cs-ops/blob/main/specs/adoption-as-a-service.md) spec explains why this report matters.

## Inputs

- For one account: its rows from [`tools/outcome_progress.py`](https://github.com/laufferw/outcome-led-cs-ops/blob/main/tools/outcome_progress.py) with adoption readings, and its customer-agreed values
- For a book: the output of [`tools/value_report.py`](https://github.com/laufferw/outcome-led-cs-ops/blob/main/tools/value_report.py), and the [CS scorecard](https://github.com/laufferw/outcome-led-cs-ops/blob/main/tools/README.md#cs-scorecard) if available
- The audience: customer executive, CS leadership, exec team, or board
- The period covered

## Prompt

```
You are helping a Customer Success leader write a value narrative. Use only the numbers below.

Audience: {customer executive | CS leadership | exec team | board}

Write:
1. A headline: the single most important result, as a number in the reader's terms.
2. What was delivered: each Proven goal as "from [baseline] to [current] [unit]", with the customer-agreed annual value where one exists. Lead with the largest.
3. What is in progress: goals On track but not yet met, and what has to happen next.
4. What is not working and what we are doing about it: Adoption gaps, Not converting goals, and missed targets, each with the action.
5. For CS leadership, exec team, or board only: what this means for the business. Use the scorecard's retention and forecast numbers if provided, and separate them clearly from the customer-agreed value.
6. One ask, if the evidence supports it.

Rules:
- Claim a result as delivered only if its reading is Proven. For Unexplained progress, say the number moved and that we are confirming the cause, or leave it out for a board audience.
- Customer-agreed value is the customer's estimate. Call it that. Never add it to revenue, retention, or ROI figures.
- Do not show internal labels (Proven, Adoption gap) to a customer executive. Describe them in plain words.
- If results are thin, say so in the headline's place and lead with the plan. Do not dress them up.
- For a customer executive, keep it under 300 words. For a board, under 250 words, with the headline numbers first.

NUMBERS:
{paste here}
```

## Output format

Six short sections, headed, in the order above. Section 5 is omitted for a customer executive. Every number is followed by where it came from (goal, outcome ID, or report section).

## Example

For the sample book's value report as of 2026-10-01, a correct board version leads with "16 customer outcomes proven, on accounts holding 83% of ARR", names $625,500 as customer-agreed annual value (not revenue), lists Bluefin's invoicing time from 9 to 3 days as the top proof point, and states plainly that faster month-end close is stalling at two accounts despite good adoption, with the Product review that follows.

## Known failure modes

- Counts unproven results. The rules limit claims to Proven goals. Check each claim against the readings.
- Adds customer-agreed value to revenue. The rules forbid it, and the output must label it.
- Hides what isn't working. Section 4 is required.
- Uses internal labels with customers. The rules translate them.
