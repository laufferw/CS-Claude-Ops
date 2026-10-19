# Playbook: Weekly Team Review

> Generic pattern. Adapt the length to team size: 30 minutes for up to 6 CSMs, 45 for more.

## Purpose

Give a CS director one weekly meeting that covers the whole team: where revenue is at risk, which forecast calls don't match the data, who is overloaded, and what each CSM needs help with. It replaces going around the room account by account.

## Trigger

Every Monday, after the [weekly data refresh](connect-your-data.md) and each CSM's own weekly run.

## Inputs

- The team rollup from [`tools/team_rollup.py`](../tools/team_rollup.py), with capacity
- The renewal forecast from [`tools/renewal_forecast.py`](../tools/renewal_forecast.py), with this week's calls
- Each CSM's `week.md` from [`tools/run_week.py`](../tools/run_week.py)
- Last week's action list

## Steps

| Step | Owner | Timing |
|---|---|---|
| 1. Refresh the data and run the rollup and forecast for the whole team | CS Ops | Monday morning |
| 2. Each CSM updates their forecast calls and expected ARR for the next two quarters | Each CSM | Before the review |
| 3. Draft the team brief with the [Team Brief](../prompts/team-brief.md) prompt | Director | 30 minutes before |
| 4. Review last week's actions: done, or why not | Director | First 5 minutes |
| 5. Calls above signals, largest ARR first: what does the CSM know that the data doesn't? | Director, with each CSM | 10 minutes |
| 6. Band drops and new red flags: confirm each has an action and an owner per the [Account Management Engine](../frameworks/account-management-engine.md) | Director | 10 minutes |
| 7. Capacity: anyone over target, anyone with room. Decide on moves or help | Director | 5 minutes |
| 8. Send the action list: owner and date for each item | Director | Within 2 hours |

## Decision logic

- **A call is above signals and the CSM can't name the evidence:** move the call to the signal category for this week's forecast. The CSM can raise it again with evidence.
- **A call is above signals with evidence the data doesn't hold** (a verbal yes, a signed order form in legal): keep the call, and record the evidence in the CRM so the signals catch up.
- **A call is below signals:** find out what the CSM knows, and add the missing red flag or note to the CRM.
- **A CSM is over the utilization target two weeks running:** move an account, or take on part of the work (an escalation, a QBR) yourself. Don't wait for the quarter.
- **Data gaps are growing on one CSM's book:** treat it as a process issue to coach, not a data team problem.
- **An account appears three weeks running with no progress:** escalate per [Escalation Logic](../frameworks/escalation-logic.md).

## Outputs

- An updated forecast, with each disagreement resolved or recorded
- An action list: account, action, owner, date
- Any capacity moves, with dates
- For the VP: the week's forecast changes and new risks, in a short note (see the [Internal Account Update](../prompts/internal-account-update.md) prompt for the format)

## Failure modes

- **Account-by-account status reading.** The rollup and forecast already show status. Spend the meeting on disagreements and decisions.
- **Calls never challenged.** Without step 5, the forecast is the sum of everyone's hopes. The signals give the director a fair way to ask.
- **Capacity discussed only at planning time.** Overload shows up weeks before anyone says so. Look at it every week.
- **The action list never goes out.** Then next week starts from memory. Send it within two hours.
