# Playbook: Quarterly Business Review

> Generic pattern. Adapt cadence to account size: quarterly for large accounts, twice a year for the rest.

## Purpose

Review progress against the customer's goals with the people who decide whether to renew, and agree on the plan for next quarter.

## Trigger

Calendar cadence. For accounts above your QBR threshold, hold one each quarter. Also hold one within 30 days of a new executive sponsor taking over.

## Inputs

- The success plan: goals, owners, and target dates
- Outcomes this quarter, with evidence
- Usage and adoption data, and the trend
- Support summary: tickets, escalations, resolutions
- Health band and drivers (for internal prep only, never shown to the customer)

## Steps

| Step | Owner | Timing |
|---|---|---|
| 1. Schedule with the executive sponsor and champion. Confirm attendees | CSM | 4 weeks before |
| 2. Gather data and draft the outline with the [QBR Outline](../prompts/qbr-outline.md) prompt | CSM | 2 weeks before |
| 3. Internal review: agree on the story, the asks, and anything Product or Sales must weigh in on | CSM, CS manager, Sales if commercial | 1 week before |
| 4. Send the agenda to the customer | CSM | 3 business days before |
| 5. Hold the QBR | CSM | Scheduled date |
| 6. Send the follow-up: agreed goals, owners, dates (see the [Customer Email](../prompts/customer-email.md) prompt) | CSM | Within 2 business days |
| 7. Update the success plan and CRM | CSM | Within 5 business days |

## Decision logic

- **Executive sponsor cannot attend:** reschedule rather than run it without them. A QBR without a decision-maker is a status meeting.
- **Outcomes are thin:** say so. Lead with what is being done about it. Do not fill the slot with a product demo.
- **Account is Red or has an open escalation:** hold the QBR as a recovery review instead, and make no asks for expansion or references.
- **Customer asks for roadmap commitments:** note the request and route it to Product. Do not commit in the meeting.

## Outputs

- An agreed plan for next quarter: goals, owners, and dates
- An updated success plan
- A follow-up email sent within 2 business days
- Any asks (reference, expansion, introduction) and the customer's response

## Failure modes

- The QBR turns into a product roadmap presentation.
- No customer-side owners on next quarter's goals, so nothing happens until the next QBR.
- Internal health language ("you're Yellow") leaks into the deck.
- The follow-up never goes out, so the agreements live only in people's memories.
