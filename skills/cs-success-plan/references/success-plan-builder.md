# Prompt: Success Plan Builder

## Purpose

Draft a success plan from kickoff material: 3 to 4 goals from the [Outcome Library](outcome-library.md), each with a customer owner, a baseline, and a target. Also repairs an existing plan whose goals have no baseline or have gone stale. The CSM confirms every number with the customer before it goes in the plan. The [Customer Onboarding](https://github.com/laufferw/outcome-led-cs-ops/blob/main/playbooks/onboarding.md) playbook says when.

## Inputs

- Kickoff call notes or transcript, and the [handoff packet](https://github.com/laufferw/outcome-led-cs-ops/blob/main/prompts/handoff-packet.md), especially its outcomes sold
- The Outcome Library table
- Any current values the customer has shared, with their source and date
- For a repair: the account's rows from [`tools/outcome_progress.py`](https://github.com/laufferw/outcome-led-cs-ops/blob/main/tools/outcome_progress.py)

## Prompt

```
You are helping a Customer Success Manager draft a success plan. Use only the material below.

1. Pick 3 to 4 outcomes from the Outcome Library that the customer said matter most now. Quote what they said for each. If they named more than 4, rank them by how strongly they said it and list the rest as later candidates.
2. For each outcome, write:
   - The goal in the customer's words
   - The customer owner, only if the material names one
   - The baseline value and date, only if the material states it, with the source
   - A proposed target value and date, checked against the library's typical range
3. Write the plan as CSV rows in this format:
   account_id,outcome_id,goal,customer_owner,unit,baseline_value,baseline_date,target_value,target_date,current_value,current_date,annual_value_per_unit
   Leave a field blank when the material doesn't give it. Leave current_value, current_date, and annual_value_per_unit blank.
4. List what the CSM must confirm with the customer: every blank baseline, every proposed target, and every owner.

For a repair (outcome progress rows provided): for each goal with status No baseline or Stale, say what measurement is missing, where the library says it comes from, and what to ask for. Do not change goals that are already measured.

Rules:
- Use library outcomes only. If the customer's goal matches none, propose it as the one allowed custom goal, with outcome_id "custom", and say why no library outcome fits.
- Never invent a baseline. A missing baseline is a question for the customer, not a number to estimate.
- If a target falls outside the typical range, say so and give the range. Never present the range as a promise.
- If Sales stated an expected result outside the range, flag it as a commitment to reset at kickoff.

ACCOUNT ID:
{id}

MATERIAL:
{kickoff notes, handoff packet, customer values}

OUTCOME LIBRARY:
{paste the library table}

OUTCOME PROGRESS (repair only):
{paste the account's rows}
```

## Output format

The chosen outcomes with the customer's words, the CSV rows, then the list of items to confirm. For a repair, one line per unmeasured goal saying what is missing and what to ask for.

## Example

From kickoff notes where the customer's controller says "we invoice nine days after delivery and it kills our cash", and the VP Operations says "rekeying carrier rates eats 30 hours a week", a correct draft includes:

- OL-01 Faster invoicing: baseline 9 days, owner Controller, target 3 days by year end (inside the 40 to 70% range)
- OL-07 Less manual work: baseline 30 hours a week, owner VP Operations, target 8 hours (73% fewer, inside the range)
- To confirm: the baseline date and source for both, and the target dates

## Known failure modes

- Estimates baselines from vague statements ("about a week"). The rules forbid it. A vague statement goes on the confirm list as a question.
- Picks outcomes the CSM wants instead of what the customer said. Each pick must quote the customer.
- Sets targets at the top of the range to impress. The range check flags it. The CSM agrees targets with the customer owner.
- Forces a goal onto a library outcome that measures something different. The rules allow one custom goal instead.
