# CRM Agent Interface

> Draft spec. What a Claude agent should be able to read and do in a CRM (HubSpot, Salesforce, or similar) through an MCP server, and the guardrails around it.

## Purpose

Let a Claude agent handle routine CRM work (lookups, updates, record hygiene, packets) so people spend time on judgment calls. The agent reaches the CRM through an MCP server that exposes only the tools below.

## Goals

- Answer questions about accounts, deals, and tickets without anyone clicking through records.
- Keep account records clean: owners set, renewal dates and ARR current, follow-ups dated.
- Assemble packets (handoff, pre-renewal) from records that already exist.
- Turn routine updates into proposed changes a person approves in one step.

## Non-goals (what it will not do)

- Delete records.
- Change properties, pipelines, or workflows.
- Change a deal's amount, stage, or close date without a person confirming that specific change.
- Email or message customers.

## Inputs

| CRM object | What the agent uses | Access |
|---|---|---|
| Companies | Account details, owner, ARR, renewal date | Read, confirmed writes to notes and agreed fields |
| Contacts | Names, roles, associations | Read |
| Deals | Stage, amount, close date, notes | Read. Sensitive fields need per-change confirmation |
| Tickets | Status, priority, age | Read |
| Notes and tasks | Recent activity | Read, confirmed creates |

The agent's credentials carry only these scopes, issued per user.

## Access model

| Tier | Capability | Approval |
|---|---|---|
| Read | Search and read companies, contacts, deals, tickets, notes | None |
| Draft | Prepare note, task, and field updates as a proposed change | Human reviews |
| Write | Apply approved changes | Human confirms each batch |
| Admin | Properties, pipelines, workflows | Not available to the agent |

## Tools

| Tool | Type | Takes | Returns |
|---|---|---|---|
| `search_records` | Read | Object type, query, filters | Matching records with id, name, owner, and last modified time |
| `get_record` | Read | Object type, id | The record, its associations, and the last 90 days of activity |
| `list_stale_records` | Read | Object type, filters (owner, missing field, days since update) | Records missing an owner or a key field, or not updated in the given days |
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
- A record hygiene report: accounts missing an owner, ARR, or renewal date, and records not updated recently

## Example workflows

1. **Record hygiene:** find accounts missing an owner, ARR, or renewal date, the fields the [data import](../playbooks/connect-your-data.md) requires, and propose updates.
2. **Pre-renewal check:** gather open tickets, usage trend, and last contact for accounts renewing in 120 days. See the [Pre-Renewal Check](../prompts/pre-renewal-check.md) prompt.
3. **Handoff packet:** assemble a closed-won summary for the CSM from deal notes and associated contacts. See [Sales to CS Handoff](../playbooks/sales-to-cs-handoff.md) and the [Handoff Packet](../prompts/handoff-packet.md) prompt.

## Failure modes

| Failure | Guard |
|---|---|
| A bulk update goes wrong across many records | Batch cap, dry run by default, and `revert_update` |
| The agent overwrites a person's newer edit | Stale proposals are refused and re-proposed |
| Approvals become rubber stamps | Sensitive deal fields are confirmed one change at a time, and the audit log names the approver |
| Hygiene updates guess at values nobody confirmed | The agent proposes only values it can cite from another record, and leaves the rest as questions for the owner |
| Packets look complete when the records are thin | Packets mark missing sections as NOT FOUND, as the handoff prompt requires |
| Credentials broader than the agent needs | Per-user scopes limited to the objects above. No admin scopes |

## Open questions

- Which API access level does your CRM plan include, and is there an existing MCP server for it?
- How will confirmations be presented (CLI prompt, Slack, a review queue)?
- What audit trail is required?
