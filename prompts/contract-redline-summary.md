# Prompt: Contract Redline Summary

## Purpose

Summarize a customer's proposed changes to a contract (MSA, SOW, SLA) into a plain-language list a non-lawyer can act on.

> This is a reading aid. It is not legal advice. Legal reviews and approves positions.

## Inputs

The redlined text or a list of the customer's proposed changes, plus your standard terms for comparison.

## Prompt

```
You are helping a revenue operations professional understand a contract redline. You are not giving legal advice.

For each proposed change, return:
- Clause (name or number)
- What the customer wants, in one plain sentence
- How it differs from our standard terms
- Who needs to weigh in (Legal, Finance, Product, Support, Sales)
- Whether it can be measured or operationalized (for example, can we actually track a response-time commitment?)

Then give:
- A short list of the changes that need Legal first
- A short list that looks routine
- Questions to ask the customer to clarify intent

Rules:
- Quote nothing you are unsure of. If text is ambiguous, say so.
- Do not recommend accepting or rejecting. Flag and route.

REDLINE:
{paste here}

OUR STANDARD TERMS:
{paste here}
```

## Output format

A table of changes, followed by the two short lists and the questions.

## Known failure modes

- Reads ambiguous clauses as settled. The rules ask it to flag them.
- Misses cross-references between clauses. Spot-check those.
