# Playbook: Outcome Review

> Generic pattern. Adapt the attendees to your org. Smaller teams can run it as one meeting.

## Purpose

Turn a quarter of outcome results across the book into decisions for Product, Marketing, Sales, and the [Outcome Library](../frameworks/outcome-library.md). Without this, outcome data stays in QBR decks and nothing upstream changes.

## Trigger

The first week of each quarter, after the last quarter's QBRs.

## Inputs

- The value report for the whole book and for each CSM, from [`tools/value_report.py`](../tools/value_report.py)
- The per-goal progress report with adoption readings, from [`tools/outcome_progress.py`](../tools/outcome_progress.py)
- The Outcome Library, with its typical ranges
- Last quarter's open items from Product

## Steps

| Step | Owner | Timing |
|---|---|---|
| 1. Run the value report and the per-goal report | CS Ops | Week 1 |
| 2. Assign an owner to every data gap: stale goals, goals with no baseline, goals with no adoption data | CS Ops, with RevOps for data feeds | Week 1 |
| 3. Product session: each outcome not converting at 2 or more accounts, with the accounts, feature adoption, and what CSMs have already checked | CS Ops and Product | Week 2 |
| 4. Adoption priorities: the lightly used features behind the most adoption gaps become enablement content and CSM campaigns | CS manager and Enablement | Week 2 |
| 5. Proof points: for each Met and Proven goal, the CSM asks the customer for written permission to use the result | CSM asks, Marketing writes | Week 3 |
| 6. Sales update: share which outcomes are proving and which aren't, and the updated typical ranges | CS Ops and Sales leadership | Week 3 |
| 7. Calibrate the library: update ranges, retire or revise weak outcomes, review custom goals that recur (see [Calibration](../frameworks/outcome-library.md#calibration)) | CS Ops | Week 3 |
| 8. Send a one-page summary of decisions to CS, Sales, Marketing, and Product leadership | CS Ops | Week 4 |

## Decision logic

- **An outcome is not converting at 2 or more accounts:** Product says which it is: a product gap (with a date, or a plain "won't build"), a configuration or process problem (CS writes the setup guide and fixes the affected accounts), or a feature list that leaves something out (CS Ops updates the library). Until a product gap is fixed, Sales stops leading with that outcome.
- **An outcome is met by fewer than a third of the plans that picked it over 4 quarters:** revise its typical range, or retire it.
- **Unexplained progress:** never used in marketing or sales material. The CSM finds the cause before the next QBR.
- **The customer declines permission:** the result can only appear in an anonymous aggregate.
- **Fewer than 5 accounts proven on an outcome:** no aggregate public claim about it yet.
- **Ranges move:** update them in both directions. Raising them after good quarters and never lowering them after bad ones turns ranges into marketing.

## Outputs

- Product's answer and owner for each pattern, tracked to next quarter
- Adoption priorities for the quarter, by feature
- Approved proof points, each with the customer's written permission on file
- An updated Outcome Library: ranges, retirements, new candidates
- The one-page decision summary

## Failure modes

- **A reporting meeting with no decisions.** Every pattern leaves with an owner and an answer, or it comes back next quarter as an open item.
- **Product hears anecdotes, not patterns.** The 2-account rule and the adoption data keep a single loud customer from setting the roadmap, and keep real patterns from being dismissed as one-offs.
- **Marketing uses results that aren't proven or approved.** Only Met and Proven goals with written permission become proof points.
- **The data gaps never close.** Stale goals and missing adoption data get named owners in step 2 and are checked first next quarter.
