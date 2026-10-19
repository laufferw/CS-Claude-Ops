# Glossary

Terms as this repo uses them. Where a doc defines a term precisely, the entry links to it.

## Accounts and revenue

| Term | Meaning |
|---|---|
| **ARR** | Annual recurring revenue: what an account pays per year for its subscription |
| **ARR at risk** | ARR on accounts whose band or flags suggest they may not renew. The [weekly brief priority](prompts/weekly-csm-brief.md#priority) scales it by risk and urgency |
| **Book** | The set of accounts one CSM owns |
| **Churn** | A customer leaving: not renewing, or ending the contract early. See [Churn and Offboarding](playbooks/churn-and-offboarding.md) |
| **Downgrade** | A renewal at lower ARR: fewer seats, a smaller plan, or less scope. Treated as a risk, not a negotiation point |
| **Expansion** | Added ARR from an existing customer: more seats, products, or teams. See [Expansion](playbooks/expansion.md) |
| **Expansion signal** | Evidence an account may want to expand. It becomes an opportunity only after the [qualification checks](playbooks/expansion.md#qualify-first) |
| **Gross churn rate** | ARR lost to churn and downgrades in a year, as a share of ARR at the start of the year. Expansion does not offset it |
| **Renewal** | The customer signing for another term. See [Renewal](playbooks/renewal.md) |
| **Renewal window** | The accounts renewing within a set number of days, 120 by default. The [renewal window tool](tools/README.md#renewal-window) lists them |

## Health scoring

All defined in [Account Health Scoring](frameworks/account-health-scoring.md).

| Term | Meaning |
|---|---|
| **Account Success Index (health index)** | A 0 to 100 score per account, the weighted average of six signal scores |
| **Signal** | One of the six inputs to the index: usage, outcomes, engagement, support, sentiment, commercial |
| **Band** | Green (75 to 100), Yellow (50 to 74), Red (0 to 49), or Insufficient data |
| **Coverage** | The share of total signal weight that had data. Below 70%, the band is Insufficient data |
| **Red flag** | An event that overrides the index: notice of non-renewal (forces Red), executive sponsor departure or payment dispute (caps at Yellow) |
| **No measured outcomes** | No success plan, or no goal with a baseline and a measurement in the last 60 days. Caps the band at Yellow |
| **Override** | A change to the band from a red flag, from no measured outcomes, or from a CSM with a written reason |
| **Top drivers** | The two signals pulling the index down the most: largest weight x (100 - score) |
| **Seat utilization** | Active users divided by licensed seats |
| **Band move** | A change in band since the last scoring run. A move down is always worth a look |
| **Trend break** | Usage down 10% or more over 90 days, whatever the band. One of the [engine's flags](frameworks/account-management-engine.md#flags-and-actions) |
| **Action log** | The record of each recommendation, what the CSM did with it, and the outcome. The calibration input for the [Account Management Engine](frameworks/account-management-engine.md) |
| **Churn risk category** | High, Medium, Low, or Unclear, from the [v1 rules](specs/csm-copilot-spec.md#churn-risk-model-v1) |

## Escalation

All defined in [Escalation Logic](frameworks/escalation-logic.md).

| Term | Meaning |
|---|---|
| **L1, L2, L3** | Escalation levels. L1 is owned by the CSM, L2 by the CS manager, L3 by a VP or executive. Each has a response target |
| **Trigger** | A condition that requires an escalation at a given level |
| **Renewal at risk** | A pre-renewal status of At risk: a Red band, or a red flag. Within 90 days of renewal, an L2 trigger |
| **Resolved, Renewed, Lost** | The three ways an escalation closes. See [raising, lowering, and closing](frameworks/escalation-logic.md#raising-lowering-and-closing) |
| **Root cause tag** | One of nine labels recording why an escalation happened, such as `product-gap` or `sponsor-change` |
| **Save plan** | The written plan for an at-risk account. See [At-Risk Save Plan](playbooks/at-risk-save-plan.md) |
| **Walk-away point** | The condition, set in a save plan, at which you stop investing in the save |

## Relationships

| Term | Meaning |
|---|---|
| **Champion** | The person at the customer who actively advocates for the product and helps get things done |
| **Executive sponsor** | The senior person at the customer who owns the decision to buy and renew |
| **Multi-threading** | Having relationships with several people at an account, so one departure does not cut you off |
| **Stakeholder map** | Who you have relationships with at an account, their roles, and who is missing |

## Lifecycle

| Term | Meaning |
|---|---|
| **Closed won** | A deal that has been signed. Starts the [Sales to CS Handoff](playbooks/sales-to-cs-handoff.md) |
| **Handoff packet** | Everything Sales passes to the CSM at close: goals, stakeholders, commitments, contract summary, risks |
| **Success plan** | 3 to 4 goals the customer picks from the [Outcome Library](frameworks/outcome-library.md), each with a customer owner, a baseline, and a target value and date. It feeds the Outcomes signal |
| **Outcome Library** | The fixed list of measurable outcomes the company offers and is prepared to prove, each with a metric, data source, and the features that move it. See [Outcome Library](frameworks/outcome-library.md) |
| **Baseline** | A goal's measured starting value and date, taken within 30 days of kickoff from the same source as later measurements |
| **Custom goal** | A success plan goal for an outcome the library does not cover. At most one per plan |
| **Goal status** | Met, On track, Off track, Missed, Stale, or No baseline, computed from baseline, target, and the latest measurement. See [measuring progress](frameworks/outcome-library.md#measuring-progress) |
| **Feature adoption** | The share of a feature's target users who used it for real work in the last 30 days. Below 40%, the feature is lightly used |
| **Support** | Whether the features behind an outcome are in use: Supported, Unsupported, or Unknown. See [checking adoption](frameworks/outcome-library.md#checking-adoption-behind-each-outcome) |
| **Proven** | A goal Met or On track with the features behind it in use. Only Proven goals count as value the product delivered |
| **Unexplained progress** | A goal Met or On track while the features behind it are lightly used. Not claimed until the cause is known |
| **Adoption gap** | A goal Off track or Missed with the features behind it lightly used. Fixed with adoption work |
| **Not converting** | A goal Off track or Missed though the features behind it are in use. At 2 or more accounts, it goes to Product |
| **Customer-agreed value** | What the customer agrees one unit of improvement on a goal is worth per year. Recorded only when they agree it |
| **Value report** | The book-level roll-up of goal statuses, proven goals, and customer-agreed value. See the [value report tool](tools/README.md#value-report) |
| **Outcome Review** | The quarterly review that takes outcome results to Product, Marketing, Sales, and the library. See [Outcome Review](playbooks/outcome-review.md) |
| **Adoption as a Service** | A paid CS offering that takes a customer from adoption to measured outcomes. See the [spec](specs/adoption-as-a-service.md) |
| **Renewal forecast** | Renewal ARR by quarter in four categories: Commit, Best case, At risk, Lost. See [Renewal Forecast](frameworks/renewal-forecast.md) |
| **CSM call** | The forecast category and expected ARR a CSM gives an account each week |
| **Call above signals** | A CSM call more optimistic than the account's data supports. Reviewed first in the [Weekly Team Review](playbooks/weekly-team-review.md) |
| **Weighted forecast** | Expected ARR x category weight, summed over a quarter's renewals |
| **Workload** | The weekly CSM hours a book needs under the [Capacity Model](frameworks/capacity-model.md) |
| **Utilization** | Workload divided by the hours a CSM has for account work |
| **Gross renewal rate (GRR)** | ARR kept from renewals due in a period, ignoring expansion, divided by ARR up for renewal. See [CS Metrics Scorecard](frameworks/cs-metrics-scorecard.md) |
| **Net renewal rate (NRR)** | ARR after renewal, including expansion, divided by ARR up for renewal |
| **Logo retention** | Accounts that renewed divided by accounts due |
| **Mapping** | A JSON file that tells [`import_data.py`](tools/README.md#import-data) where each field comes from in raw exports. See [Connect Your Data](playbooks/connect-your-data.md) |
| **Coverage report** | What the importer prints: how many rows have a value for each field |
| **Back-test** | Checking a model against what happened: whether lost renewals scored Red or Yellow 90 days ahead. See the [back-test tool](tools/README.md#back-test) |
| **Miss** | A renewal that was lost while its account scored Green 90 days before |
| **False alarm** | An account that scored Red 90 days before renewal and then renewed in full |
| **Realization** | The share of a forecast category's expected ARR that actually renewed. With enough renewals, the category's weight |
| **Forecast accuracy** | Renewed ARR, excluding expansion, divided by the weighted forecast at the start of the quarter |
| **Eval** | A test case for a prompt: an input and checks a correct output must pass. See [evals](evals/README.md) |
| **Charter** | The written statement of what CS is for, owns, and doesn't own. See [CS Charter](frameworks/cs-charter.md) |
| **Ownership map** | Who does the work (R), decides (A), is consulted (C), and is informed (I) for each activity across functions |
| **Data class** | The policy category a piece of customer data falls in: allowed, minimum necessary, check the contract first, or never. See [AI Usage Policy](frameworks/ai-usage-policy.md) |
| **Value history** | Goals an account has met and retired from its success plan. Evidence for renewal, no longer scored |
| **Go-live** | The point at which the customer starts using the product for real work |
| **First value** | The first measured improvement on a success plan goal, from its baseline. Expected within 90 days of close (see [Onboarding](playbooks/onboarding.md)) |
| **QBR** | Quarterly business review: a review of outcomes with the customer's decision-makers. See [QBR](playbooks/qbr.md) |
| **Pre-renewal status** | Ready, Needs work, At risk, or Unclear, set 120 days before renewal by the [Pre-Renewal Check](prompts/pre-renewal-check.md) |
| **Notice period** | How far ahead of the renewal date either side must give notice to change or end the contract |
| **Exit interview** | A conversation with a churned customer's decision-maker about why they left |

## Customer signals

| Term | Meaning |
|---|---|
| **NPS** | Net Promoter Score. Here, the customer's latest 0 to 10 answer to "how likely are you to recommend us?" |
| **CSAT** | Customer satisfaction score from a survey, usually after a support interaction |
| **CSM confidence** | The CSM's own 1 to 5 rating of how healthy the relationship is |
| **TTR** | Time to resolution for support tickets |
| **Contract flag** | An open contract concern, such as a downgrade request or a question about terminating early |

## Contracts

| Term | Meaning |
|---|---|
| **MSA** | Master services agreement: the main legal contract with a customer |
| **SOW** | Statement of work: the scope, deliverables, and timeline for a specific piece of work |
| **SLA** | Service level agreement: commitments on response times, uptime, or similar. See [SLA Pushback](playbooks/sla-pushback.md) |
| **Redline** | A marked-up draft of a contract showing proposed changes. See [Contract Redline Summary](prompts/contract-redline-summary.md) |

## Business case

Used by the [ROI calculator](tools/README.md#roi-calculator).

| Term | Meaning |
|---|---|
| **Loaded cost** | What an hour of an employee's time costs the company: salary plus benefits, taxes, and overhead |
| **Capacity freed** | Hours a tool saves, valued at loaded cost. Worth money only if the hours are redeployed |
| **Realization rate** | The share of estimated benefits that actually happens, once adoption is uneven |
| **Ramp** | The months after rollout before benefits start |
| **Payback** | Months until cumulative benefit covers cumulative cost |

## Roles

| Term | Meaning |
|---|---|
| **CSM** | Customer Success Manager: owns a book of accounts and their outcomes |
| **CS manager** | Manages a team of CSMs. Owns L2 escalations |
| **RevOps** | Revenue Operations: owns CRM data, contract records, and the processes that connect Sales, CS, and Finance |
