# HubSpot Agent Interface

> Draft spec. What an AI agent should be able to read and do in HubSpot, and the guardrails around it.

## Purpose

Let an AI agent handle routine HubSpot work (lookups, updates, project board hygiene, reporting) so people spend time on judgment calls.

## Access model

| Tier | Capability | Approval |
|---|---|---|
| Read | Search and read companies, contacts, deals, tickets, projects, notes | None |
| Draft | Prepare note, task, and field updates as a proposed change | Human reviews |
| Write | Apply approved changes | Human confirms each batch |
| Admin | Properties, pipelines, workflows | Not available to the agent |

## Candidate tools

| Tool | Type | Notes |
|---|---|---|
| `search_records` | Read | Companies, contacts, deals, tickets |
| `get_record` | Read | With associations and recent activity |
| `list_project_items` | Read | Projects board items with owner and status |
| `propose_update` | Draft | Returns a diff of fields to change |
| `apply_update` | Write | Applies a confirmed diff |
| `create_task` | Write | Assigned to a named owner with a due date |
| `log_note` | Write | Attached to a record |

## Guardrails

- Never delete records.
- Never change deal amount, stage, or close date without a human confirming the diff.
- Every write is logged with who approved it.
- Rate limits and batch size caps to avoid runaway updates.
- Dry-run mode by default.

## Example workflows

1. **Board hygiene:** find items missing an owner or stale for 14 days and propose updates. See [Projects Board Steps and Target Dates](../playbooks/hubspot-projects-board.md).
2. **Pre-renewal check:** gather open tickets, usage trend, and last contact for accounts renewing in 120 days. See the [Pre-Renewal Check](../prompts/pre-renewal-check.md) prompt.
3. **Handoff packet:** assemble a closed-won summary for the CSM from deal notes and associated contacts. See [Sales to CS Handoff](../playbooks/sales-to-cs-handoff.md) and the [Handoff Packet](../prompts/handoff-packet.md) prompt.

## Open questions

- Which API access level is available in your portal?
- How will confirmations be presented (CLI prompt, Slack, a review queue)?
- What audit trail is required?
