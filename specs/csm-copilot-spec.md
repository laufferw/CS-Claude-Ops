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
   |- scoring-server    (health index, churn model)
```

Each MCP server exposes read tools by default. Write tools are separate and require explicit confirmation.

## Core capabilities

| Capability | Description | Backing |
|---|---|---|
| Daily brief | Top accounts needing action today | scoring + crm, [weekly brief](../prompts/weekly-csm-brief.md) |
| Account review | One-page summary of any account | all servers, [account review](../prompts/account-review.md) |
| Health scoring | Compute the index with a breakdown | scoring-server |
| Churn risk model | Probability plus the top drivers | scoring-server |
| Renewal prep | Timeline, risks, and talking points | crm + usage, [pre-renewal check](../prompts/pre-renewal-check.md), [renewal prep](../prompts/renewal-prep.md) |
| Drafting | Emails, QBR outlines, internal updates | [customer email](../prompts/customer-email.md), [QBR outline](../prompts/qbr-outline.md), [internal update](../prompts/internal-account-update.md) |
| CRM update | Propose note and field changes for approval | crm-server |

## Churn risk model (v1)

- Start rule-based: transparent flags from the health index and override rules.
- Move to a simple statistical model once 12 or more months of labeled outcomes exist.
- Always return drivers alongside the probability. A number without reasons is not actionable.

## Safety and trust

- Read-only by default. Writes need confirmation.
- Every recommendation cites the data behind it.
- Log what was suggested and what the CSM did, for calibration.
- Credentials are scoped per user. No shared admin tokens.

## Milestones

1. **M1:** Read-only account review from CRM data.
2. **M2:** Health scoring with breakdown.
3. **M3:** Daily brief and renewal prep.
4. **M4:** Drafting with human approval.
5. **M5:** Confirmed CRM writes.
6. **M6:** Churn model v2 and feedback loop.

## Open questions

- Which data sources are reliable enough for scoring on day one?
- How are overrides captured and reviewed?
- What is the approval UX for writes in a terminal?
