# CS-Claude-Ops

Claude-powered Customer Success Operations: frameworks, specs, prompts, and playbooks for running a CS org with an AI copilot.

This repo is markdown-first. Almost everything here is a document you can read, copy into Claude, or adapt, not code you have to run.

## Start here

| You are | Read | Then run |
|---|---|---|
| A CSM | [CSM guide](guides/csm.md) | `run_week.py` for your book, then `/cs-weekly-brief` |
| CS Ops or RevOps | [CS Ops guide](guides/cs-ops.md) | `import_data.py` on your exports ([Connect Your Data](playbooks/connect-your-data.md)) |
| A CS director or manager | [Director guide](guides/cs-director.md) | `team_rollup.py` and `renewal_forecast.py`, then `/cs-team-brief` |
| A VP or COO | [Executive guide](guides/cs-executive.md) | `cs_scorecard.py`, then `/cs-value-narrative` |

## What's inside

| Folder | What it holds |
|---|---|
| [`guides/`](guides/) | Start-here guides by role: CSM, CS Ops, director, and executive |
| [`frameworks/`](frameworks/) | The models: the outcome library, account health scoring, the renewal forecast, capacity, the metrics scorecard, escalation logic, the account management engine, CSM competencies |
| [`specs/`](specs/) | Design docs for what's worth building: the CSM Copilot, a HubSpot agent interface, and Adoption as a Service |
| [`prompts/`](prompts/) | Reusable Claude prompts, each with inputs, output format, and known failure modes |
| [`playbooks/`](playbooks/) | Step-by-step operating procedures with decision logic |
| [`tools/`](tools/) | Small utilities, standard-library Python: a data importer, a weekly run, health scoring, outcome progress, a value report, a renewal window, a renewal forecast, a team rollup, a CS scorecard, and an ROI calculator |
| [`sample-data/`](sample-data/) | A fictional book of accounts for trying the prompts and tools |
| [`essays/`](essays/) | Opinionated writing on CS Ops and RevOps as disciplines |
| [`evals/`](evals/README.md) | Test cases for the prompts, with good and bad reference outputs |
| [`templates/`](templates/) | Starting points for new frameworks, prompts, playbooks, and specs |
| [`.claude/skills/`](.claude/skills/) | Each prompt packaged as a Claude Code skill |

Terms are defined in the [glossary](glossary.md).

## Index

### Guides

- [Customer Success Manager](guides/csm.md): what to run each week, and the skill for each customer moment
- [CS Operations and RevOps](guides/cs-ops.md): connecting the data, the weekly and monthly runs, and calibration
- [CS Director or Manager](guides/cs-director.md): the team rollup, the forecast review, and capacity
- [CS Executive (VP or COO)](guides/cs-executive.md): the scorecard, the value story, and staffing

### Frameworks

- [Outcome Library](frameworks/outcome-library.md): the measurable outcomes customers pick for their success plans, and how progress from baseline is measured
- [Account Health Scoring](frameworks/account-health-scoring.md): the Account Success Index, its signals, weights, and bands
- [Renewal Forecast](frameworks/renewal-forecast.md): forecast categories from signals, CSM calls, and the calls to challenge
- [Capacity Model](frameworks/capacity-model.md): weekly CSM hours per account, utilization, and headcount
- [CS Metrics Scorecard](frameworks/cs-metrics-scorecard.md): fixed definitions for retention, book health, value, forecast, and capacity
- [CS Charter and Ownership Map](frameworks/cs-charter.md): what CS owns, what it doesn't, and who decides what across functions
- [AI Usage Policy](frameworks/ai-usage-policy.md): which customer data may go into AI tools, approved tools, human review, and logging
- [Account Management Engine](frameworks/account-management-engine.md): the weekly loop from account data to ranked CSM actions
- [Escalation Logic](frameworks/escalation-logic.md): triggers, levels, owners, response targets, and root cause tags
- [CSM Competency Framework](frameworks/csm-competency-framework.md): what good looks like at each CSM level

### Specs

- [CSM Copilot](specs/csm-copilot-spec.md): a Claude Code CLI copilot for CSMs, built on MCP servers
- [HubSpot Agent Interface](specs/hubspot-agent-interface.md): what an agent may read and do in HubSpot, and the guardrails
- [Adoption as a Service](specs/adoption-as-a-service.md): a paid CS offering that takes customers to measured outcomes, its pricing guardrails, and the value report

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
- [Success Plan Builder](prompts/success-plan-builder.md): draft a success plan from kickoff notes, or repair unmeasured goals
- [Adoption Plan](prompts/adoption-plan.md): turn adoption gaps into actions by feature
- [Value Narrative](prompts/value-narrative.md): the story of value delivered, for a customer executive or the board
- [Team Brief](prompts/team-brief.md): a director's weekly brief across the team
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

Team and cross-functional:

- [Connect Your Data](playbooks/connect-your-data.md): get real CRM, product, and support data into the tools
- [Weekly Team Review](playbooks/weekly-team-review.md): the director's weekly meeting on risk, forecast calls, and capacity
- [Outcome Review](playbooks/outcome-review.md): each quarter, take outcome results to Product, Marketing, Sales, and the Outcome Library

Situational:

- [Handling Customer SLA Pushback](playbooks/sla-pushback.md): responding to requests for stronger service-level commitments
- [Projects Board Steps and Target Dates](playbooks/hubspot-projects-board.md): which board steps get due dates, and how to track the rest

### Tools and sample data

- [Data importer](tools/README.md#import-data): turns raw exports into the repo formats, with a coverage report
- [Run week](tools/README.md#run-week): every weekly report for one CSM in one folder, with next steps
- [Health score calculator](tools/score_accounts.py): applies the scoring rubric to a CSV of accounts and their success plans
- [Outcome progress](tools/README.md#outcome-progress): each success plan goal's progress from baseline to target, and whether the features behind it are in use, for QBRs and renewals
- [Value report](tools/README.md#value-report): the value a book has realized: proven goals, customer-agreed value, and inputs for the Outcome Review
- [Renewal window](tools/README.md#renewal-window): the accounts renewing in the next 120 days, ready to paste into the Pre-Renewal Check
- [Renewal forecast](tools/README.md#renewal-forecast): renewal ARR by quarter, with calls that disagree with the data
- [Team rollup](tools/README.md#team-rollup): health, risk, outcomes, and workload by CSM
- [CS scorecard](tools/README.md#cs-scorecard): the leadership scorecard
- [Back-test](tools/README.md#back-test): did the health score flag lost renewals 90 days ahead, under two weight sets?
- [Forecast back-test](tools/README.md#forecast-back-test): forecast accuracy, and how much of each category renewed
- [Evals](evals/README.md): test cases that catch a prompt change breaking its output
- [ROI calculator](tools/README.md#roi-calculator): first-year ROI of a CS copilot, with cash return kept separate from time saved
- [Repo checker](tools/README.md#repo-checker): checks required sections, links, the index, skills, and tools. Runs in CI on every push
- [Sample accounts](sample-data/README.md): 12 fictional accounts across three CSMs, raw and scored, with success plans, feature adoption, forecast calls, renewal, score, and forecast history, capacity settings, raw exports to import, and sample ROI inputs

### Essays

- [CS Ops Is a Discipline, Not a Help Desk](essays/cs-ops-is-a-discipline.md)
- [Health Scores Are for Deciding, Not Reporting](essays/health-scores-are-for-deciding.md)
- [Claude Drafts, People Decide](essays/claude-drafts-people-decide.md)
- [Prove the Value, Then Sell It](essays/prove-the-value-then-sell-it.md)

## Ground rules

1. **Nothing proprietary.** Examples use placeholder companies and invented numbers. No customer names, contract terms, or internal pricing.
2. **Every artifact states its inputs, outputs, and failure modes.** A prompt or framework without these is not finished.
3. **Judgment stays with the human.** Claude drafts, scores, and flags. A person decides on escalations, pricing, and commitments.

## How to use

### With Claude Code

Open this repo in Claude Code and ask in plain language: "run my week as Sam Example as of 2026-10-01", "write the team brief for the sample team", or "draft a handoff packet from these notes". Claude picks the matching skill, reads the prompt file, and follows it. You can also call a skill by name, such as `/cs-weekly-brief`.

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
| `cs-success-plan` | [Success Plan Builder](prompts/success-plan-builder.md) |
| `cs-adoption-plan` | [Adoption Plan](prompts/adoption-plan.md) |
| `cs-value-narrative` | [Value Narrative](prompts/value-narrative.md) |
| `cs-team-brief` | [Team Brief](prompts/team-brief.md) |
| `cs-competency-evaluation` | [CSM Competency Evaluation](prompts/csm-competency-evaluation.md) |

The skills only point at the prompt files, so editing a prompt changes its skill too.

### By hand

- Start with the guide for your role in [Start here](#start-here). Each has the commands to run on the sample data.
- To use your own data, follow [Connect Your Data](playbooks/connect-your-data.md).
- Start with the [Outcome Library](frameworks/outcome-library.md) to see how value is defined and measured, then [Account Health Scoring](frameworks/account-health-scoring.md) to see how scoring works.
- Run `python3 tools/outcome_progress.py sample-data/success-plans.csv --adoption sample-data/feature-adoption.csv --as-of 2026-10-01` for each goal's progress from baseline and its adoption reading, ready for a QBR.
- Run `python3 tools/value_report.py sample-data/accounts.csv --plans sample-data/success-plans.csv --adoption sample-data/feature-adoption.csv --as-of 2026-10-01` for the value the book has realized, and read [Adoption as a Service](specs/adoption-as-a-service.md) for how to sell it.
- Score the [sample accounts](sample-data/README.md) with `python3 tools/score_accounts.py sample-data/accounts.csv --plans sample-data/success-plans.csv --as-of 2026-10-01`, then paste the result into the [Weekly CSM Brief](prompts/weekly-csm-brief.md) prompt.
- Run `python3 tools/renewal_window.py sample-data/accounts.csv --plans sample-data/success-plans.csv --as-of 2026-10-01` and paste the result into the [Pre-Renewal Check](prompts/pre-renewal-check.md) prompt.
- Pair scoring with the [Account Review prompt](prompts/account-review.md) to review a single account with Claude.
- Read the [CSM Copilot spec](specs/csm-copilot-spec.md) for where this is headed, and run `python3 tools/roi_calculator.py sample-data/roi-inputs.json` for a sample business case.

## Contributing

Start new docs from [`templates/`](templates/README.md). If you change a prompt, run its [evals](evals/README.md). Run `python3 tools/check_repo.py` before pushing. CI runs the same check.

## Status

Early drafts. Weights, thresholds, and rubrics are starting points to calibrate against your own data.

## License

[MIT](LICENSE).
