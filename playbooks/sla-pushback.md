# Playbook: Handling Customer SLA Pushback

> Generic pattern. Use placeholder details when sharing examples.

## Purpose

Answer a request for stronger service levels with one consolidated position that every owning function has agreed, and that you can measure.

## Trigger

A customer asks for stronger service-level commitments than your standard terms: faster response times, penalties, or uptime guarantees. Often this arrives in a redline (see the [Contract Redline Summary](../prompts/contract-redline-summary.md) prompt) or during a [Renewal](renewal.md).

## Inputs

- The customer's asks, in their words, or the redlined SLA
- Your standard SLA terms
- Support's actual performance data: response and resolution times by priority, for at least the last two quarters
- What your systems can measure and report today

## Principles

1. **Commit only to what you can measure.** If you cannot track it, you cannot promise it.
2. **The right function owns the answer.** Support owns response capability, Legal owns wording, Finance owns credits, Sales owns the relationship.
3. **Offer a defined middle ground, not an open negotiation.**

## Steps

| Step | Owner | Output |
|---|---|---|
| 1. List every ask in plain language | RevOps / CSM | Table of asks |
| 2. Check measurability for each | Support / RevOps | Yes / No / Partial, with the data source |
| 3. Legal review of wording and risk | Legal | Position per ask |
| 4. Decide the middle ground | CS lead + Sales | A short counter-proposal |
| 5. Respond with one consolidated answer | CSM | Single reply, not piecemeal |
| 6. Record the agreed terms and how they are tracked | RevOps | Updated contract record |

## Decision logic

- **Measurable and achievable:** accept, with a clear definition (what starts the clock, what counts as a response).
- **Measurable but not achievable:** counter with a realistic target and cutoff times.
- **Not measurable:** decline as written, and propose a measurable alternative.
- **Penalties or credits:** route to Legal and Finance. Do not discuss amounts without them.

## Outputs

- A table of asks, each with its measurability, Legal's position, and the decision
- One consolidated reply to the customer
- The agreed terms in the contract record, with the data source and owner that track each one

## A useful counter pattern

Offer a turnaround commitment tied to a submission cutoff (for example, requests received by a stated time are handled within a stated window), rather than an open-ended response-time promise.

## Failure modes

- Promising a number nobody can report on.
- Answering ask by ask and giving away ground gradually.
- The CSM absorbing a decision that belongs to Legal or Support.
