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
| [`tools/`](tools/) | Small utilities that run on sample data: a health score calculator, a renewal window extractor, and an ROI calculator |
| [`sample-data/`](sample-data/) | A fictional book of accounts for trying the prompts and tools |
| [`essays/`](essays/) | Opinionated writing on CS Ops and RevOps as disciplines |
| [`templates/`](templates/) | Starting points for new frameworks, prompts, playbooks, and specs |
| [`.claude/skills/`](.claude/skills/) | Each prompt packaged as a Claude Code skill |

Terms are defined in the [glossary](glossary.md).

## Index

### Frameworks

- [Account Health Scoring](frameworks/account-health-scoring.md): the Account Success Index, its signals, weights, and bands
- [Account Management Engine](frameworks/account-management-engine.md): the weekly loop from account data to ranked CSM actions
- [Escalation Logic](frameworks/escalation-logic.md): triggers, levels, owners, response targets, and root cause tags
- [CSM Competency Framework](frameworks/csm-competency-framework.md): what good looks like at each CSM level

### Specs

- [CSM Copilot](specs/csm-copilot-spec.md): a Claude Code CLI copilot for CSMs, built on MCP servers
- [HubSpot Agent Interface](specs/hubspot-agent-interface.md): what an agent may read and do in HubSpot, and the guardrails

### Prompts

- [Weekly CSM Brief](prompts/weekly-csm-brief.md): the top accounts, renewals, expansion signals, and data gaps for one CSM's week
- [Account Review](prompts/account-review.md): a one-page review of a single account
- [Churn Risk Triage](prompts/churn-risk-triage.md): rank a book of accounts by churn risk, with drivers
- [Renewal Prep](prompts/renewal-prep.md): get ready for a renewal conversation 90 to 120 days out
- [Pre-Renewal Check](prompts/pre-renewal-check.md): readiness status for every account renewing in the next 120 days
- [Contract Redline Summary](prompts/contract-redline-summary.md): plain-language summary of a customer's proposed contract changes
- [Handoff Packet](prompts/handoff-packet.md): draft the closed-won handoff packet from deal notes
- [Escalation Summary](prompts/escalation-summary.md): open an escalation with the required fields, and close it with a root cause tag
- [Customer Email](prompts/customer-email.md): draft a customer email for the CSM to review and send
- [QBR Outline](prompts/qbr-outline.md): a slide-by-slide QBR outline built on the customer's outcomes
- [Internal Account Update](prompts/internal-account-update.md): a short status update on one account for managers or leadership
- [CSM Competency Evaluation](prompts/csm-competency-evaluation.md): evidence from a CSM's work, mapped to the competency framework

### Playbooks

The customer lifecycle, in order:

- [Sales to CS Handoff](playbooks/sales-to-cs-handoff.md): the handoff packet and steps after Closed Won
- [Customer Onboarding](playbooks/onboarding.md): from kickoff to first value, with a success plan in place
- [Quarterly Business Review](playbooks/qbr.md): reviewing outcomes with decision-makers and agreeing next quarter's plan
- [Expansion](playbooks/expansion.md): qualifying expansion signals and handing them to Sales
- [Renewal](playbooks/renewal.md): the 120-day renewal timeline and who owns each decision
- [At-Risk Save Plan](playbooks/at-risk-save-plan.md): what goes into the plan for a Red or escalated account
- [Churn and Offboarding](playbooks/churn-and-offboarding.md): offboarding, exit interviews, and feeding churn back into scoring

Situational:

- [Handling Customer SLA Pushback](playbooks/sla-pushback.md): responding to requests for stronger service-level commitments
- [Projects Board Steps and Target Dates](playbooks/hubspot-projects-board.md): which board steps get due dates, and how to track the rest

### Tools and sample data

- [Health score calculator](tools/score_accounts.py): applies the scoring rubric to a CSV of accounts
- [Renewal window](tools/README.md#renewal-window): the accounts renewing in the next 120 days, ready to paste into the Pre-Renewal Check
- [ROI calculator](tools/README.md#roi-calculator): first-year ROI of a CS copilot, with cash return kept separate from time saved
- [Repo checker](tools/README.md#repo-checker): checks required sections, links, the index, skills, and tools. Runs in CI on every push
- [Sample accounts](sample-data/README.md): 12 fictional accounts, raw and scored, plus sample ROI inputs

### Essays

- [CS Ops Is a Discipline, Not a Help Desk](essays/cs-ops-is-a-discipline.md)
- [Health Scores Are for Deciding, Not Reporting](essays/health-scores-are-for-deciding.md)
- [Claude Drafts, People Decide](essays/claude-drafts-people-decide.md)

## Ground rules

1. **Nothing proprietary.** Examples use placeholder companies and invented numbers. No customer names, contract terms, or internal pricing.
2. **Every artifact states its inputs, outputs, and failure modes.** A prompt or framework without these is not finished.
3. **Judgment stays with the human.** Claude drafts, scores, and flags. A person decides on escalations, pricing, and commitments.

## How to use

### With Claude Code

Open this repo in Claude Code and ask in plain language: "write my weekly brief from sample-data/accounts.csv as of 2026-10-01", or "draft a handoff packet from these notes". Claude picks the matching skill, reads the prompt file, and follows it. You can also call a skill by name, such as `/cs-weekly-brief`.

| Skill | Prompt |
|---|---|
| `cs-weekly-brief` | [Weekly CSM Brief](prompts/weekly-csm-brief.md) |
| `cs-account-review` | [Account Review](prompts/account-review.md) |
| `cs-churn-triage` | [Churn Risk Triage](prompts/churn-risk-triage.md) |
| `cs-renewal-prep` | [Renewal Prep](prompts/renewal-prep.md) |
| `cs-pre-renewal-check` | [Pre-Renewal Check](prompts/pre-renewal-check.md) |
| `cs-redline-summary` | [Contract Redline Summary](prompts/contract-redline-summary.md) |
| `cs-handoff-packet` | [Handoff Packet](prompts/handoff-packet.md) |
| `cs-escalation-summary` | [Escalation Summary](prompts/escalation-summary.md) |
| `cs-customer-email` | [Customer Email](prompts/customer-email.md) |
| `cs-qbr-outline` | [QBR Outline](prompts/qbr-outline.md) |
| `cs-account-update` | [Internal Account Update](prompts/internal-account-update.md) |
| `cs-competency-evaluation` | [CSM Competency Evaluation](prompts/csm-competency-evaluation.md) |

The skills only point at the prompt files, so editing a prompt changes its skill too.

### By hand

- Start with [Account Health Scoring](frameworks/account-health-scoring.md) to see how scoring works.
- Score the [sample accounts](sample-data/README.md) with `python3 tools/score_accounts.py sample-data/accounts.csv --as-of 2026-10-01`, then paste the result into the [Weekly CSM Brief](prompts/weekly-csm-brief.md) prompt.
- Run `python3 tools/renewal_window.py sample-data/accounts.csv --as-of 2026-10-01` and paste the result into the [Pre-Renewal Check](prompts/pre-renewal-check.md) prompt.
- Pair scoring with the [Account Review prompt](prompts/account-review.md) to review a single account with Claude.
- Read the [CSM Copilot spec](specs/csm-copilot-spec.md) for where this is headed, and run `python3 tools/roi_calculator.py sample-data/roi-inputs.json` for a sample business case.

## Contributing

Start new docs from [`templates/`](templates/README.md), then run `python3 tools/check_repo.py` before pushing. CI runs the same check.

## Status

Early drafts. Weights, thresholds, and rubrics are starting points to calibrate against your own data.

## License

[MIT](LICENSE).
