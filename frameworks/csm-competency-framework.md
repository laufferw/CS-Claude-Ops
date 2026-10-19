# CSM Competency Framework

> Draft. Calibrate levels and behaviors to your own org.

## Purpose

Define what good looks like for a Customer Success Manager at each level, so hiring, coaching, and promotion use the same yardstick, and so Claude can help evaluate call notes and account plans against it.

## Inputs

Evidence of what the CSM actually did, from at least three accounts:

- Account plans and success plans
- Call notes, customer emails, and QBR materials
- Escalation write-ups and save plans
- Outcomes: renewals, expansions, churn, and health trends on their book
- CRM records: activity, forecast entries, and data quality
- Observations from the manager and from peers

## Competency areas

| Area | What it covers |
|---|---|
| Customer outcomes | Defining, tracking, and proving the value the customer bought for |
| Relationship depth | Multi-threading, executive access, champion development |
| Commercial acumen | Renewals, expansion, pricing conversations, contract basics |
| Risk management | Spotting and acting on churn signals early |
| Operational rigor | CRM hygiene, forecasting accuracy, handoffs |
| Communication | Clear written and verbal updates, directness, expectation setting |

## Levels

Each area is rated 1 to 4.

| Level | Description |
|---|---|
| 1 Developing | Executes defined tasks with guidance |
| 2 Proficient | Owns a book independently, follows the playbooks |
| 3 Advanced | Adapts playbooks, mentors others, handles complex accounts |
| 4 Leading | Shapes the playbooks, influences strategy across accounts |

## Example behaviors

What each level looks like in practice. A CSM is at a level in an area when the evidence shows that behavior consistently, across accounts.

### Customer outcomes

- **1:** Records the goals the customer states, when asked to.
- **2:** Writes a success plan for every account: 3 to 4 goals from the [Outcome Library](outcome-library.md), each with a baseline, a target, and a customer owner, agreed with the customer.
- **3:** Ties outcomes to the customer's business results and uses them as evidence in QBRs and renewals.
- **4:** Proposes new outcomes for the library, with the measurement and evidence to back them, that other CSMs adopt.

### Relationship depth

- **1:** Keeps a working relationship with the day-to-day contact.
- **2:** Knows the champion and the executive sponsor on every account, and meets the sponsor at least each quarter.
- **3:** Multi-threads complex accounts so that no single departure cuts off the relationship, and develops new champions.
- **4:** Builds executive relationships that change the customer's strategy, and coaches others to do the same.

### Commercial acumen

- **1:** Knows each account's ARR, renewal date, and term.
- **2:** Runs the renewal timeline, builds the value story, and spots expansion signals to qualify.
- **3:** Handles downgrade requests and complex renewals with Sales, and qualifies expansion that closes.
- **4:** Shapes renewal and expansion approach across the book, and improves forecast accuracy for the team.

### Risk management

- **1:** Logs a risk when told one exists.
- **2:** Notices missed meetings and low usage and raises them within a week.
- **3:** Builds a save plan with an executive sponsor, with dates and owners.
- **4:** Identifies a pattern across accounts and changes the early-warning criteria.

### Operational rigor

- **1:** Updates the CRM when reminded.
- **2:** Keeps notes, stakeholders, and next steps current, and forecasts renewals accurately.
- **3:** Runs clean handoffs in and out of their book, with nothing lost.
- **4:** Improves the processes and data the team relies on.

### Communication

- **1:** Responds clearly to customer questions.
- **2:** Sends updates without being asked, with bad news first and commitments only where approved.
- **3:** Handles difficult conversations (price, failure, a lost champion) directly and keeps trust.
- **4:** Sets the standard for written and executive communication on the team.

## How to use with Claude

Give Claude a CSM's account plan or call notes plus this framework and ask for evidence per competency, not a score. Evidence first keeps the rating defensible. The [CSM Competency Evaluation](../prompts/csm-competency-evaluation.md) prompt does this.

## Outputs

For each CSM:

- Evidence per area, each item citing the account and document it came from
- A level per area, or "Insufficient evidence" where the samples don't cover it
- Two strengths and two growth areas, each with a concrete development step

The manager decides the levels. Claude's evidence is an input, not the rating.

## Failure modes

- Rating on style instead of evidence.
- Treating levels as tenure.
- Using a single account as the basis for the whole rating.
- Rating every area at once with thin samples. "Insufficient evidence" is a valid outcome. Gather more before deciding.
