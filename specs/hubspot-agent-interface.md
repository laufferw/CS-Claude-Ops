# HubSpot Agent Interface

> Draft spec. What an AI agent should be able to read and do in HubSpot, and the guardrails around it.

## Purpose

Let an AI agent handle routine HubSpot work (lookups, updates, project board hygiene, reporting) so people spend time on judgment calls.

## Goals

- Answer questions about accounts, deals, and tickets without anyone clicking through records.
- Keep the projects board clean: owners set, statuses current, follow-ups dated.
- Assemble packets (handoff, pre-renewal) from records that already exist.
- Turn routine updates into proposed changes a person approves in one step.

## Non-goals (what it will not do)

- Delete records.
- Change properties, pipelines, or workflows.
- Change a deal's amount, stage, or close date without a person confirming that specific change.
- Email or message customers.

## Inputs

| HubSpot object | What the agent uses | Access |
|---|---|---|
| Companies | Account details, owner, ARR, renewal date | Read, confirmed writes to notes and agreed fields |
| Contacts | Names, roles, associations | Read |
| Deals | Stage, amount, close date, notes | Read. Sensitive fields need per-change confirmation |
| Tickets | Status, priority, age | Read |
| Projects board items | Step, owner, status, dates, blockers | Read, confirmed writes |
| Notes and tasks | Recent activity | Read, confirmed creates |

The agent's credentials carry only these scopes, issued per user.

## Access model

| Tier | Capability | Approval |
|---|---|---|
| Read | Search and read companies, contacts, deals, tickets, projects, notes | None |
| Draft | Prepare note, task, and field updates as a proposed change | Human reviews |
| Write | Apply approved changes | Human confirms each batch |
| Admin | Properties, pipelines, workflows | Not available to the agent |

## Tools

| Tool | Type | Takes | Returns |
|---|---|---|---|
| `search_records` | Read | Object type, query, filters | Matching records with id, name, owner, and last modified time |
| `get_record` | Read | Object type, id | The record, its associations, and the last 90 days of activity |
| `list_project_items` | Read | Board, filters (owner, step, stale days) | Items with step, owner, status, dates, and blocker |
| `propose_update` | Draft | Record id, field values or a note | A change id, the diff of current and proposed values, and the record's last modified time |
| `apply_update` | Write | Change ids (one batch) | Each change: applied, or refused with the reason |
| `revert_update` | Write | Change id | The record restored to the values before the change |
| `create_task` | Write | Record id, owner, due date, description | The task id |
| `log_note` | Write | Record id, text | The note id |

## Errors and rollback

- **Stale proposal:** if a record changed after its change was proposed, `apply_update` refuses that change and the agent proposes it again against the current values.
- **Partial batch failure:** the agent stops, reports which changes applied and which did not, and does not retry without a new confirmation.
- **Rate limits:** the agent backs off and resumes the same batch. It never splits a batch into smaller ones to get around a cap.
- **Undo:** every applied change stores the previous values, so `revert_update` can restore them. A revert is itself a write and needs confirmation.

## Safety and trust

- Never delete records.
- Never change deal amount, stage, or close date without a human confirming the diff.
- Every write is logged with who approved it.
- Rate limits and batch size caps (25 changes) to avoid runaway updates.
- Dry-run mode by default.

## Outputs

- Answers to lookups, citing the records they came from
- Proposed changes as diffs, and an audit log of every applied change and its approver
- Assembled packets: handoff and pre-renewal
- A board hygiene report: items missing an owner, stale items, and missing follow-up dates

## Example workflows

1. **Board hygiene:** find items missing an owner or stale for 14 days and propose updates. See [Projects Board Steps and Target Dates](../playbooks/hubspot-projects-board.md).
2. **Pre-renewal check:** gather open tickets, usage trend, and last contact for accounts renewing in 120 days. See the [Pre-Renewal Check](../prompts/pre-renewal-check.md) prompt.
3. **Handoff packet:** assemble a closed-won summary for the CSM from deal notes and associated contacts. See [Sales to CS Handoff](../playbooks/sales-to-cs-handoff.md) and the [Handoff Packet](../prompts/handoff-packet.md) prompt.

## Failure modes

| Failure | Guard |
|---|---|
| A bulk update goes wrong across many records | Batch cap, dry run by default, and `revert_update` |
| The agent overwrites a person's newer edit | Stale proposals are refused and re-proposed |
| Approvals become rubber stamps | Sensitive deal fields are confirmed one change at a time, and the audit log names the approver |
| Board hygiene adds due dates to steps nobody controls | The workflow follows the projects board playbook: external-dependent steps get follow-up dates, not due dates |
| Packets look complete when the records are thin | Packets mark missing sections as NOT FOUND, as the handoff prompt requires |
| Credentials broader than the agent needs | Per-user scopes limited to the objects above. No admin scopes |

## Open questions

- Which API access level is available in your portal?
- How will confirmations be presented (CLI prompt, Slack, a review queue)?
- What audit trail is required?
