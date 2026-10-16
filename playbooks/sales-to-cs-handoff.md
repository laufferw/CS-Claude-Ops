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

If the CSM cannot answer "why did they buy and what does success look like?" from the packet, it is incomplete.

## Outputs

- A completed handoff packet, checked by RevOps, stored on the account
- A list of commitments made during the sale, each confirmed with the rep
- The kickoff note sent to the customer, which starts [Customer Onboarding](onboarding.md)

## Failure modes

- Informal promises that never reach the CSM.
- Packet filled with copy-paste instead of real answers.
- No check, so gaps surface at the first customer call.
