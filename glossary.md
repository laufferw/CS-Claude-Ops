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
| **Override** | A change to the band from a red flag, or from a CSM with a written reason |
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
| **Success plan** | The customer's goals, each measurable, with an owner and target date, agreed with the customer. It feeds the Outcomes signal |
| **Go-live** | The point at which the customer starts using the product for real work |
| **First value** | The customer reaching the first goal in their success plan. Expected within 90 days of close (see [Onboarding](playbooks/onboarding.md)) |
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
