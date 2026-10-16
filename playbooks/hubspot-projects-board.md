# Playbook: Projects Board Steps and Target Dates

> Generic pattern for a deal-support or contracting board. Adapt step names to your process.

## Purpose

Decide which steps on a projects board get a target due date, who sets it, and how to treat steps whose timing you do not control.

## Trigger

Setting up a projects board, adding a new step type to one, or a request to "add due dates" to an existing board.

## Inputs

- The list of steps on the board, with their current owners
- For each step: whether its effort is internal and predictable, internal and deal-specific, or dependent on another company
- Historical time-in-step, if the board has history
- Who asked for dates, and what they want to use them for

## Core idea

Not every step is equally schedulable. Treat three kinds differently.

| Kind | Example | How to set the date |
|---|---|---|
| **Internal, fixed effort** | A finance pricing request | Standing target (for example, 3 business days) |
| **Internal, owner-driven** | A statement of work | The owning CSM sets the date per deal |
| **External-dependent** | A master agreement under redline | No target. Track status and next-touch date instead |

## Why external-dependent steps get no target

Timing depends on the other company's legal and procurement process. A made-up date creates false overdue flags and erodes trust in the board.

## What to track instead

- Status (drafted, sent, in redline, awaiting signature)
- Last contact date
- Next follow-up date, set by the owner
- Blocker, if any

## Before adding target dates, ask

1. What decision will the dates inform?
2. Who will act when a date is missed?
3. Is the goal visibility, accountability, or forecasting? Each needs a different design.

## Steps

| Step | Owner | Timing |
|---|---|---|
| 1. Answer the three questions above with whoever asked for dates | RevOps | Before changing the board |
| 2. Classify each step as fixed effort, owner-driven, or external-dependent | RevOps, with step owners | Same week |
| 3. Set standing targets for fixed-effort steps, from historical time-in-step where it exists | RevOps, with the owning function | Same week |
| 4. Add a required owner-set date field for owner-driven steps | RevOps | Same week |
| 5. Add status, last contact, next follow-up, and blocker fields for external-dependent steps. No due date | RevOps | Same week |
| 6. Agree who acts on a missed date, and how they hear about it | RevOps, team leads | Before go-live |
| 7. Review after one month: are the dates used and the overdue flags trusted? | RevOps | One month after go-live |

## Outputs

- Each step classified, with its date rule
- Standing targets for fixed-effort steps
- Follow-up fields in place of dates for external-dependent steps
- A named owner for missed dates, and a one-month review

The [HubSpot Agent Interface](../specs/hubspot-agent-interface.md) board hygiene workflow checks the board against these rules.

## Failure modes

- Dates added everywhere, then ignored.
- Overdue flags on steps nobody controls.
- Dates with no owner or consequence.
