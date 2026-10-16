# CS-Claude-Ops

Claude-powered Customer Success Operations: frameworks, specs, prompts, and playbooks for running a CS org with an AI copilot.

This repo is markdown-first. Almost everything here is a document you can read, copy into Claude, or adapt, not code you have to run.

## What's inside

| Folder | What it holds |
|---|---|
| [`frameworks/`](frameworks/) | The models: CSM competencies, account health scoring, escalation logic, the account management engine |
| [`specs/`](specs/) | Design docs for tools worth building: the CSM Copilot and a HubSpot agent interface |
| [`prompts/`](prompts/) | Reusable Claude prompts, each with inputs, output format, and known failure modes |
| [`playbooks/`](playbooks/) | Step-by-step operating procedures with decision logic |

Planned, not yet started: `tools/` (small utilities such as an ROI calculator, with sample data only) and `essays/` (opinionated writing on RevOps and CS Ops as disciplines).

## Index

### Frameworks

- [Account Health Scoring](frameworks/account-health-scoring.md): the Account Success Index, its signals, weights, and bands
- [Account Management Engine](frameworks/account-management-engine.md): the weekly loop from account data to ranked CSM actions
- [Escalation Logic](frameworks/escalation-logic.md): triggers, levels, owners, and response targets
- [CSM Competency Framework](frameworks/csm-competency-framework.md): what good looks like at each CSM level

### Specs

- [CSM Copilot](specs/csm-copilot-spec.md): a Claude Code CLI copilot for CSMs, built on MCP servers
- [HubSpot Agent Interface](specs/hubspot-agent-interface.md): what an agent may read and do in HubSpot, and the guardrails

### Prompts

- [Account Review](prompts/account-review.md): a one-page review of a single account
- [Churn Risk Triage](prompts/churn-risk-triage.md): rank a book of accounts by churn risk, with drivers
- [Renewal Prep](prompts/renewal-prep.md): get ready for a renewal conversation 90 to 120 days out
- [Contract Redline Summary](prompts/contract-redline-summary.md): plain-language summary of a customer's proposed contract changes

### Playbooks

- [Sales to CS Handoff](playbooks/sales-to-cs-handoff.md): the handoff packet and steps after Closed Won
- [Handling Customer SLA Pushback](playbooks/sla-pushback.md): responding to requests for stronger service-level commitments
- [Projects Board Steps and Target Dates](playbooks/hubspot-projects-board.md): which board steps get due dates, and how to track the rest

## Ground rules

1. **Nothing proprietary.** Examples use placeholder companies and invented numbers. No customer names, contract terms, or internal pricing.
2. **Every artifact states its inputs, outputs, and failure modes.** A prompt or framework without these is not finished.
3. **Judgment stays with the human.** Claude drafts, scores, and flags. A person decides on escalations, pricing, and commitments.

## How to use

- Start with [Account Health Scoring](frameworks/account-health-scoring.md) to see how scoring works.
- Pair it with the [Account Review prompt](prompts/account-review.md) to run a review with Claude.
- Read the [CSM Copilot spec](specs/csm-copilot-spec.md) for where this is headed.

## Status

Early drafts. Weights, thresholds, and rubrics are starting points to calibrate against your own data.
