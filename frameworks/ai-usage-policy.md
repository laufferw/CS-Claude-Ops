# AI Usage Policy for Customer Success

> Draft. A starting policy for using Claude, and the tools in this repo, with customer data. It is not legal advice. Legal and Security must review and adapt it, especially the data classes and the approved tools, before anyone uses real customer data.

## Purpose

Let a CS team use AI on real accounts without putting customer data, contracts, or trust at risk. It sets what data may go into an AI tool, which tools and accounts may be used, what a person must review, and what gets logged, so Legal and Security can approve the rollout and CSMs know where the lines are.

## Inputs

| Input | Source | Example |
|---|---|---|
| The company's agreement with the AI provider | Legal, Procurement | Data retention, data use, and sub-processor terms |
| The company's data classification | Security | Public, internal, confidential, restricted |
| Customer contracts and DPAs | Legal | A customer that prohibits new sub-processors |
| Regulations that apply to customers' data | Legal, Compliance | Health data for healthcare customers |
| The repo's ground rule | [Claude Drafts, People Decide](../essays/claude-drafts-people-decide.md) | People decide on escalations, pricing, and commitments |

## The policy

### 1. Approved tools and accounts

- Use only AI tools and accounts covered by the company's agreement with the provider: a company-managed workspace, or API access under company terms. Never a personal account.
- Legal and Security confirm what the agreement says about retention and use of inputs, and record it here: {retention and data-use terms, from the agreement}.
- New tools, plugins, or connectors are added to this list by Security before use: {approved tools}.

### 2. Data classes

| Class | Examples | Rule |
|---|---|---|
| Allowed | Account-level business data: ARR, renewal dates, health scores, aggregate usage, success plan metrics, ticket counts | Use in approved tools for CS work |
| Allowed, minimum necessary | Customer contacts' names, roles, and business email addresses; meeting notes; email threads from company systems | Include only what the task needs. Remove personal details that don't matter to it |
| Check the contract first | Anything from a customer whose contract or DPA restricts sub-processors or AI use | Legal confirms before any of that customer's data goes into an AI tool |
| Never | Credentials, API keys, and passwords; payment card numbers; government ID numbers; health or other special-category personal data; end users' individual activity tied to names; anything a customer has asked not to share | Do not paste, upload, or connect. If it is in a document, remove it first |

Healthcare and financial-services customers need particular care: notes and tickets can contain patient or account-holder details. Strip them before use.

### 3. Human review

- **Nothing reaches a customer without a person reading it.** Drafts mark commitments with `[NEEDS APPROVAL]` (see the [Customer Email](../prompts/customer-email.md) prompt), and the sender resolves each one.
- **Nothing writes to a system of record without confirmation.** Agents propose changes as a diff, and a person applies them (see the [CRM Agent Interface](../specs/crm-agent-interface.md)).
- **People decide** on escalations, pricing, contract terms, commitments, and anything about a person's performance. Claude drafts, scores, and flags.
- **The sender owns what they send.** Whether or not AI helped, a CSM is accountable for every word in their name. Follow the company's policy on disclosing AI use to customers: {disclosure policy}.

### 4. Data handling with this repo

- This repository holds fictional data only. Never commit real customer data to it.
- Keep real exports outside the repository, or in `private/`, which git ignores. `tools/run_week.py` writes to `out/`, which git also ignores.
- Delete real exports and outputs when they are no longer needed, per the company's retention schedule.

### 5. Logging and audit

- Keep the inputs each report was built from. `tools/run_week.py` saves them in its output folder's `inputs/`.
- Prompts and rubrics are versioned in git, so any output can be traced to the prompt that produced it.
- Prompt changes pass their [evals](../evals/README.md) before use.

### 6. Incidents

If restricted data is pasted into an AI tool, or a draft goes to a customer unreviewed, report it to Security the same day through the normal incident process. Reporting quickly is what matters. Nobody is punished for an honest report.

## Before rollout

| Check | Owner |
|---|---|
| The provider agreement covers the intended use, and its terms are recorded in section 1 | Legal |
| The data classes match the company's classification | Security |
| Customers with contracts restricting AI or sub-processors are listed, and excluded or cleared | Legal, CS Ops |
| CSMs are trained on this policy and on what "never" means | CS leadership |
| Real data paths (`private/`, `out/`) are set up and ignored by git | CS Ops |
| The disclosure policy is decided | Legal, CS leadership |

## Outputs

- An approved policy, signed by Legal, Security, and CS leadership
- A list of approved tools and accounts
- A list of customers whose data needs clearance first
- A record that each CSM was trained

## Worked example

A CSM wants to draft Cedar Health Partners' escalation summary from the last 90 days of notes. Health account notes can mention patients. Under the policy, the CSM removes any patient details (never), keeps contact names and roles only where the summary needs them (minimum necessary), checks that Cedar's contract doesn't restrict AI use (Legal maintains that list), and uses the company workspace. The draft goes to the CS manager for review before anything is sent, because escalation decisions stay with people.

## Failure modes

- **Personal accounts.** The easiest way to break the policy is a CSM using a personal AI account because it's faster. Make the approved tool the easy path.
- **Pasting whole threads.** Full email threads carry signatures, phone numbers, and side conversations. Paste what the task needs.
- **A policy nobody reads.** Train on the data classes with real examples, and repeat it when tools change.
- **Review in name only.** Rubber-stamping drafts defeats the review rule. Directors spot-check sent emails against drafts.
- **Out of date.** Provider terms and tools change. Review this policy every six months.

## Calibration

Every six months, Security and CS Ops review incidents, near misses, and spot-check findings, re-read the provider agreement, and update the data classes and approved tools.
