# Outcome-Led CS Ops

**Customer Success operations that prove the value customers get. Built for Claude.**

Outcome-Led CS Ops is an open-source set of Claude skills, frameworks, playbooks, and small tools for running Customer Success around measurable customer outcomes: success plans with baselines, health scores you can explain, renewal forecasts you can defend, and value reports that claim only what's proven.

It's built first for small CS teams without a CS platform, and it works for any team. Take the whole set, or pull out just the skills and docs you need.

## Get it

### In Claude Code: install the plugin

```
/plugin marketplace add laufferw/outcome-led-cs-ops
/plugin install outcome-led-cs-ops@outcome-led-cs-ops
```

Then ask in plain language ("write my weekly brief from this export", "draft a success plan from these kickoff notes"), or call a skill by name, such as `/outcome-led-cs-ops:cs-weekly-brief`. The plugin includes the tools, so Claude can score a raw export before it writes.

### In the Claude apps: upload the skills you want

Download one skill's zip from the table below, or [all of them in one zip](https://github.com/laufferw/outcome-led-cs-ops/releases/latest/download/outcome-led-cs-ops-all-skills.zip), and upload it under Skills in your Claude settings. Each skill carries its own prompt and reference docs, so it works on its own with data you paste in.

### Take only what you need

- **One skill:** every folder in [`skills/`](skills/) is self-contained. Copy it into `~/.claude/skills/` for yourself, or into a project's `.claude/skills/` for a team.
- **One doc:** frameworks, playbooks, and prompts are plain markdown. Copy, adapt, and share them.
- **The tools:** standard-library Python, nothing to install. Clone the repo and run them.

### Try it on the sample data

```
git clone https://github.com/laufferw/outcome-led-cs-ops.git && cd outcome-led-cs-ops
python3 tools/run_week.py sample-data/accounts.csv --plans sample-data/success-plans.csv --adoption sample-data/feature-adoption.csv --calls sample-data/forecast-calls.csv --csm "Sam Example" --as-of 2026-10-01
```

Open `out/2026-10-01-sam-example/week.md` for a CSM's week: band drops, renewals, adoption gaps, and which skill to use next.

## Skills

| Skill | What it does | Source prompt | Download |
|---|---|---|---|
| `cs-weekly-brief` | Write a weekly brief for one CSM's book of accounts: top accounts to act on, renewals in 120 days, expansion signals, and data gaps | [Weekly CSM Brief](prompts/weekly-csm-brief.md) | [zip](https://github.com/laufferw/outcome-led-cs-ops/releases/latest/download/cs-weekly-brief.zip) |
| `cs-account-review` | Write a one-page review of a single customer account: snapshot, what's going well, risks, stakeholder map, next actions, and data gaps | [Account Review](prompts/account-review.md) | [zip](https://github.com/laufferw/outcome-led-cs-ops/releases/latest/download/cs-account-review.zip) |
| `cs-churn-triage` | Rank a list of accounts by churn risk with the top drivers and a recommended action for each | [Churn Risk Triage](prompts/churn-risk-triage.md) | [zip](https://github.com/laufferw/outcome-led-cs-ops/releases/latest/download/cs-churn-triage.zip) |
| `cs-renewal-prep` | Prepare a CSM for one account's renewal conversation: timeline, value story, risks, objections, expansion, and questions | [Renewal Prep](prompts/renewal-prep.md) | [zip](https://github.com/laufferw/outcome-led-cs-ops/releases/latest/download/cs-renewal-prep.zip) |
| `cs-pre-renewal-check` | Check every account renewing in the next 120 days and give each a readiness status (Ready, Needs work, At risk, Unclear) | [Pre-Renewal Check](prompts/pre-renewal-check.md) | [zip](https://github.com/laufferw/outcome-led-cs-ops/releases/latest/download/cs-pre-renewal-check.zip) |
| `cs-redline-summary` | Summarize a customer's proposed contract changes (MSA, SOW, SLA) in plain language and route each to the function that owns it | [Contract Redline Summary](prompts/contract-redline-summary.md) | [zip](https://github.com/laufferw/outcome-led-cs-ops/releases/latest/download/cs-redline-summary.zip) |
| `cs-handoff-packet` | Draft the Sales-to-CS handoff packet for a closed-won deal from deal notes, calls, and emails | [Handoff Packet](prompts/handoff-packet.md) | [zip](https://github.com/laufferw/outcome-led-cs-ops/releases/latest/download/cs-handoff-packet.zip) |
| `cs-escalation-summary` | Draft the write-up that opens a customer escalation (level, required fields, gaps), or the summary that closes one (outcome, root cause tag) | [Escalation Summary](prompts/escalation-summary.md) | [zip](https://github.com/laufferw/outcome-led-cs-ops/releases/latest/download/cs-escalation-summary.zip) |
| `cs-customer-email` | Draft a customer-facing email for a CSM to review and send | [Customer Email](prompts/customer-email.md) | [zip](https://github.com/laufferw/outcome-led-cs-ops/releases/latest/download/cs-customer-email.zip) |
| `cs-qbr-outline` | Draft a slide-by-slide outline for a quarterly business review built on the customer's goals and outcomes | [QBR Outline](prompts/qbr-outline.md) | [zip](https://github.com/laufferw/outcome-led-cs-ops/releases/latest/download/cs-qbr-outline.zip) |
| `cs-account-update` | Write a short internal status update on one account for a manager, account team, or leadership | [Internal Account Update](prompts/internal-account-update.md) | [zip](https://github.com/laufferw/outcome-led-cs-ops/releases/latest/download/cs-account-update.zip) |
| `cs-competency-evaluation` | Gather evidence from a CSM's work samples against the CSM competency framework, area by area | [CSM Competency Evaluation](prompts/csm-competency-evaluation.md) | [zip](https://github.com/laufferw/outcome-led-cs-ops/releases/latest/download/cs-competency-evaluation.zip) |
| `cs-success-plan` | Draft a success plan from kickoff material: 3 to 4 outcomes from the Outcome Library, each with a customer owner, baseline, and target, or repair goals with no baseline or gone stale | [Success Plan Builder](prompts/success-plan-builder.md) | [zip](https://github.com/laufferw/outcome-led-cs-ops/releases/latest/download/cs-success-plan.zip) |
| `cs-adoption-plan` | Turn success plan goals with an adoption gap into a plan by feature: who, action, owners, and dates, plus what to check for goals that are not converting | [Adoption Plan](prompts/adoption-plan.md) | [zip](https://github.com/laufferw/outcome-led-cs-ops/releases/latest/download/cs-adoption-plan.zip) |
| `cs-value-narrative` | Write the story of value delivered from a value report or one account's outcome progress, for a customer executive, CS leadership, the exec team, or the board | [Value Narrative](prompts/value-narrative.md) | [zip](https://github.com/laufferw/outcome-led-cs-ops/releases/latest/download/cs-value-narrative.zip) |
| `cs-team-brief` | Draft a CS director's weekly brief across the team from the team rollup and renewal forecast: calls to challenge, risk by CSM, capacity, and data gaps | [Team Brief](prompts/team-brief.md) | [zip](https://github.com/laufferw/outcome-led-cs-ops/releases/latest/download/cs-team-brief.zip) |

## Start here

| You are | Read | Then use |
|---|---|---|
| A CSM | [CSM guide](guides/csm.md) | `run_week.py` for your book, then the `cs-weekly-brief` skill |
| CS Ops or RevOps | [CS Ops guide](guides/cs-ops.md) | `import_data.py` on your exports ([Connect Your Data](playbooks/connect-your-data.md)) |
| A CS director or manager | [Director guide](guides/cs-director.md) | `team_rollup.py` and `renewal_forecast.py`, then the `cs-team-brief` skill |
| A VP or COO | [Executive guide](guides/cs-executive.md) | `cs_scorecard.py`, then the `cs-value-narrative` skill |

## What's inside

| Folder | What it holds |
|---|---|
| [`skills/`](skills/) | The Claude skills, one self-contained folder each. Generated from `prompts/` by `tools/build_skills.py` |
| [`guides/`](guides/) | Start-here guides by role: CSM, CS Ops, director, and executive |
| [`frameworks/`](frameworks/) | The models: the outcome library, account health scoring, the renewal forecast, capacity, the metrics scorecard, the CS charter, the AI usage policy, escalation logic, the account management engine, CSM competencies |
| [`specs/`](specs/) | Design docs for what's worth building: the CSM Copilot, a CRM agent interface, and Adoption as a Service |
| [`prompts/`](prompts/) | The source prompt behind each skill, with inputs, output format, and known failure modes |
| [`playbooks/`](playbooks/) | Step-by-step operating procedures with decision logic |
| [`tools/`](tools/) | Small utilities, standard-library Python: a data importer, a weekly run, health scoring, outcome progress, a value report, a renewal window, a renewal forecast, a team rollup, a CS scorecard, back-tests, evals, and an ROI calculator |
| [`sample-data/`](sample-data/) | A fictional book of accounts for trying the skills and tools |
| [`essays/`](essays/) | Opinionated writing on CS Ops and RevOps as disciplines |
| [`evals/`](evals/README.md) | Test cases for the prompts, with good and bad reference outputs |
| [`templates/`](templates/) | Starting points for new frameworks, prompts, playbooks, specs, and guides |
| [`.claude-plugin/`](.claude-plugin/plugin.json) | The Claude Code plugin and marketplace manifests |

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
- [CS Metrics Scorecard](frameworks/cs-metrics-scorecard.md): fixed definitions for retention, book health, value, forecast, and capacity, plus a scale segment section for books run one-to-many
- [CS Charter and Ownership Map](frameworks/cs-charter.md): what CS owns, what it doesn't, and who decides what across functions
- [AI Usage Policy](frameworks/ai-usage-policy.md): which customer data may go into AI tools, approved tools, human review, and logging
- [Account Management Engine](frameworks/account-management-engine.md): the weekly loop from account data to ranked CSM actions
- [Escalation Logic](frameworks/escalation-logic.md): triggers, levels, owners, response targets, and root cause tags
- [CSM Competency Framework](frameworks/csm-competency-framework.md): what good looks like at each CSM level

### Specs

- [CSM Copilot](specs/csm-copilot-spec.md): a Claude Code CLI copilot for CSMs, built on MCP servers
- [CRM Agent Interface](specs/crm-agent-interface.md): what a Claude agent may read and do in a CRM through MCP, and the guardrails
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

## Run the tools yourself

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

Contributions are welcome, especially Outcome Library entries for other kinds of products. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Status

Version 0.1.0, an early release. Weights, thresholds, and rubrics are starting points to calibrate against your own data, with the back-tests in `tools/`. See the [changelog](CHANGELOG.md).

## License

[MIT](LICENSE).
