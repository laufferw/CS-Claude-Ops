# Prompt: Adoption Plan

## Purpose

Turn the goals with an Adoption gap into a plan: for each lightly used feature, who at the customer needs to use it, what will get them there, and by when. Also sets out what to check for goals that are Not converting. The [adoption check](../frameworks/outcome-library.md#checking-adoption-behind-each-outcome) defines both readings.

## Inputs

- The account's rows from [`tools/outcome_progress.py`](../tools/outcome_progress.py), run with `--adoption`
- The Outcome Library table, for the features each outcome depends on
- Stakeholders and their roles
- Notes on what has been tried, and any blockers (training, permissions, integrations)

## Prompt

```
You are helping a Customer Success Manager write an adoption plan. Use only the material below.

For each goal whose reading is "Adoption gap":
1. Name the goal, its status, and the lightly used features with their adoption.
2. For each lightly used feature, write:
   - Who should be using it: the role or team, and the customer contact who can make it happen
   - Why usage is low, if the material says. If not, write "cause unknown" and the question to ask
   - The action: training, configuration, a workflow change, an executive ask, or removing a blocker
   - The owner on our side and on the customer's side
   - A date, and the adoption level that counts as done (at least 40% of target users)
3. Say what should happen to the goal's number once adoption is up, and when to check.

For each goal whose reading is "Not converting":
- Say that adoption is not the problem. List what to check instead: configuration, the customer's process around the feature, data quality, and whether the outcome depends on features not in the library list.
- Write the questions for the customer owner.

Rules:
- Order the plan by goal status: Missed, then Off track.
- One action per feature. Prefer the action that removes a blocker over more training.
- Make no commitments on product changes or roadmap dates. If a fix needs Product, write [NEEDS REVIEW: Product].
- Do not include goals that are Proven, Unexplained progress, Stale, or No baseline.

ACCOUNT:
{name}

OUTCOME PROGRESS ROWS:
{paste rows}

OUTCOME LIBRARY:
{paste the library table}

STAKEHOLDERS AND NOTES:
{paste here}
```

## Output format

One section per goal, Missed first. Under each Adoption gap goal, a table with one row per lightly used feature: who, cause, action, owners, date, done when. Under each Not converting goal, the checks and the questions. End with the check-back date.

## Example

For Cedar Health Partners in the [sample data](../sample-data/feature-adoption.csv), a correct plan has two Adoption gap goals: OL-06 faster close (Missed: reconciliation at 22%, period locking at 15%) and OL-08 fewer data errors (Off track: validation rules at 30%, integrations at 35%). It has one Not converting goal: OL-11 faster approvals, where approval workflows are at 82%, so the plan checks routing and approval rules rather than asking for more use.

## Known failure modes

- Prescribes training for everything. The rules ask for one action per feature, and prefer removing a blocker.
- Treats Not converting as an adoption problem. The prompt separates it, because more usage won't fix it.
- Invents the cause of low usage. Unknown causes become questions.
- Promises a product fix to raise adoption. Product changes are marked for review.
