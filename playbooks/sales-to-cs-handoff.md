# Playbook: Sales to CS Handoff

> Generic pattern. Adapt fields to your CRM.

## Purpose

Make sure a closed-won deal reaches the CSM with everything needed to start well, so customers never have to repeat themselves.

## Trigger

Deal moves to Closed Won.

## Inputs

- Deal notes, call notes, and the email thread with the customer
- Contacts and their roles from the CRM
- The signed contract or order form

## Handoff packet (required)

- Customer goals and the success criteria they were sold
- Outcomes sold: which [Outcome Library](../frameworks/outcome-library.md) outcomes were discussed, the customer's current value for each if known (with its source, as a provisional baseline), and any target or result Sales mentioned
- Key stakeholders, roles, and who the champion and executive sponsor are
- Commitments made during the sale (scope, timelines, terms, anything promised informally)
- Contract summary: term, renewal date, ARR, special clauses
- Known risks or concerns from the sales process
- Technical or integration requirements

## Steps

| Step | Owner | Timing |
|---|---|---|
| 1. Sales completes the packet (the [Handoff Packet](../prompts/handoff-packet.md) prompt drafts it from deal notes) | Sales rep | Within 2 business days of close |
| 2. RevOps checks completeness | RevOps | Within 1 business day |
| 3. Internal handoff call | Sales and CSM | Within 5 business days |
| 4. CSM sends the customer kickoff note | CSM | Within 7 business days |

Onboarding starts from the kickoff note. See [Customer Onboarding](onboarding.md).

## Quality check

If the CSM cannot answer "why did they buy and what does success look like?" from the packet, it is incomplete. Success should be described as outcomes from the library, so onboarding starts from what was sold.

## Outputs

- A completed handoff packet, checked by RevOps, stored on the account
- A list of commitments made during the sale, each confirmed with the rep
- The kickoff note sent to the customer, which starts [Customer Onboarding](onboarding.md)

## Failure modes

- Informal promises that never reach the CSM.
- A typical range presented as a promise ("you'll cut invoicing time in half"). Any expected result Sales stated is listed as a commitment, so the CSM can confirm or reset it at kickoff.
- Outcomes sold that aren't in the library, so nobody can measure them. Flag them at the handoff call.
- Packet filled with copy-paste instead of real answers.
- No check, so gaps surface at the first customer call.
