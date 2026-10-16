# CSM Copilot Spec

> Draft design doc. A Claude Code CLI-based copilot for Customer Success Managers, built on MCP servers.

## Goals

- Give each CSM a daily and weekly view of what matters across their book.
- Compute and explain account health and churn risk.
- Draft customer communications and internal updates for human review.
- Keep CRM data current with less manual entry.

## Non-goals (what it will not do)

- Send customer-facing messages without human approval.
- Make commitments on SLAs, pricing, or contract terms.
- Change CRM fields without showing the proposed change first.
- Replace CSM judgment on escalations.

## Inputs

| Source | What it provides | Access |
|---|---|---|
| CRM | Accounts, contacts, deals, notes, renewal dates, contract terms, red flags | Read, plus confirmed writes for notes and fields |
| Product analytics | Active users, licensed seats, 90-day usage trend | Read |
| Ticketing | Open tickets, escalations, time-to-resolution trend | Read |
| Billing | Invoices, days late, payment disputes | Read |
| Success plans | Goals and their status | Read |
| Surveys | Latest NPS response per account | Read |
| The CSM | Confidence rating, band overrides with reasons, approvals | Entered through the copilot |

Field-level formats follow [`sample-data/accounts.csv`](../sample-data/README.md).

## Architecture

```
CSM terminal (Claude Code CLI)
        |
   Copilot skills + prompts (this repo)
        |
   MCP servers
   |- crm-server        (accounts, contacts, deals, notes)
   |- usage-server      (product analytics)
   |- support-server    (tickets, escalations)
   |- billing-server    (invoices, payment status)
   |- scoring-server    (health index, churn model, action log)
```

Each MCP server exposes read tools by default. Write tools are separate and require explicit confirmation.

## MCP tools

| Server | Tool | Type | Takes | Returns |
|---|---|---|---|---|
| crm-server | `search_accounts` | Read | Query text, owner | Matching accounts: id, name, ARR, renewal date, owner |
| crm-server | `get_account` | Read | Account id | Account, contacts with roles, open deals, last 90 days of notes, contract terms, red flags |
| crm-server | `list_renewals` | Read | Owner, days ahead | Accounts renewing in the window, soonest first |
| crm-server | `propose_change` | Draft | Account id, a note or field values | A change id and a diff of current and proposed values |
| crm-server | `apply_change` | Write | Change id | What was applied. Refuses if the record changed since the proposal |
| usage-server | `get_usage` | Read | Account id, days | Licensed seats, active users, trend percentage |
| support-server | `list_tickets` | Read | Account id, status | Tickets with priority, age, and escalation flag |
| billing-server | `get_billing` | Read | Account id | Open invoices, days late, disputes |
| scoring-server | `score_book` | Read | Owner, as-of date | Every account scored, sorted by priority (the [`score_accounts.py`](../tools/score_accounts.py) output) |
| scoring-server | `score_account` | Read | Account id, as-of date | Index, band, signal scores, coverage, overrides, top drivers |
| scoring-server | `churn_risk` | Read | Account id | Risk category and drivers (see the v1 rules below) |
| scoring-server | `log_outcome` | Write | Recommendation id, what the CSM did, reason | Confirmation. Feeds calibration |

## Core capabilities

| Capability | Description | Backing |
|---|---|---|
| Brief | Top accounts needing action. Weekly by default, on demand any day | `score_book`, [weekly brief](../prompts/weekly-csm-brief.md) |
| Account review | One-page summary of any account | All read tools, [account review](../prompts/account-review.md) |
| Health scoring | Compute the index with a breakdown | `score_account`, [Account Health Scoring](../frameworks/account-health-scoring.md) |
| Churn risk | Risk category plus the top drivers | `churn_risk`, [churn triage](../prompts/churn-risk-triage.md) |
| Renewal prep | Timeline, risks, and talking points | `list_renewals`, [pre-renewal check](../prompts/pre-renewal-check.md), [renewal prep](../prompts/renewal-prep.md) |
| Drafting | Emails, QBR outlines, internal updates | [customer email](../prompts/customer-email.md), [QBR outline](../prompts/qbr-outline.md), [internal update](../prompts/internal-account-update.md) |
| CRM update | Propose note and field changes for approval | `propose_change`, then `apply_change` after confirmation |

## Churn risk model (v1)

v1 is rule-based, using the health score and flags, so every result can be explained:

| Risk | Rule (first match wins) |
|---|---|
| High | Band is Red, or any red flag (notice of non-renewal, sponsor departure, payment dispute) |
| Unclear | Band is Insufficient data |
| Medium | Band is Yellow, or a usage trend break (down 10% or more over 90 days), or no executive contact in 60 days |
| Low | None of the above |

Drivers are the account's top drivers from scoring, plus whichever rule set the category. These match the categories in the [Churn Risk Triage](../prompts/churn-risk-triage.md) prompt.

- Move to a simple statistical model (v2) once 12 or more months of labeled outcomes exist.
- Always return drivers alongside the category or probability. A number without reasons is not actionable.

## Outputs

- The brief, account reviews, and renewal prep, in the formats their prompts define
- Drafts of emails, QBR outlines, and internal updates, never sent by the copilot
- Proposed CRM changes as diffs, applied only after confirmation
- An action log: each recommendation, what the CSM did, and why

## Safety and trust

- Read-only by default. Writes need confirmation.
- Every recommendation cites the data behind it.
- Log what was suggested and what the CSM did, for calibration.
- Credentials are scoped per user. No shared admin tokens.
- No tool sends email or posts to customers. Drafts leave the copilot only when a person sends them.

## Failure modes

| Failure | Guard |
|---|---|
| A broken data feed shows up as a healthy or unhealthy account | Missing data is scored as unknown, coverage is reported, and low coverage becomes a data gap flag |
| A draft makes a commitment nobody approved | Prompts use `[NEEDS APPROVAL]` placeholders, and no tool can send |
| A confirmed write overwrites someone else's newer edit | `apply_change` refuses if the record changed since the proposal |
| CSMs approve diffs without reading them | Batches are capped at 25 changes, and deal amount, stage, and close date changes are shown one at a time |
| Recommendations drift from reality | The action log feeds quarterly calibration. If no one logs outcomes, the calibration report says so |
| CSMs stop trusting the brief | Every item cites its data, and a dismissed recommendation with a reason suppresses that flag until the next review |

## Milestones

1. **M1:** Read-only account review from CRM data.
2. **M2:** Health scoring with breakdown.
3. **M3:** Daily brief and renewal prep.
4. **M4:** Drafting with human approval.
5. **M5:** Confirmed CRM writes.
6. **M6:** Churn model v2 and feedback loop.

## Open questions

Each has a proposed answer to start from. Confirm or change them before M1.

- **Which data sources are reliable enough for scoring on day one?** Proposed: CRM and billing from day one. Add usage, support, and surveys as each feed is checked against a sample of accounts. The coverage rule keeps the score honest in the meantime.
- **How are overrides captured and reviewed?** Proposed: a band override field and a required reason field in the CRM, written through `propose_change`, with a monthly report of all overrides for the CS manager.
- **What is the approval UX for writes in a terminal?** Proposed: show the full diff, then require an explicit yes for the batch. Show sensitive fields one at a time.
