# Prompt: Renewal Prep

## Purpose

Prepare a CSM for a renewal conversation roughly 90 to 120 days out.

## Inputs

Account summary, contract details (term, price, scope), usage and outcomes data, stakeholder list, any open issues.

Run the [Pre-Renewal Check](pre-renewal-check.md) across the book first to find which accounts need this.

## Prompt

```
You are helping a Customer Success Manager prepare for a renewal.

Produce:
1. A renewal timeline working back from the renewal date (key milestones and owners)
2. The value story: outcomes delivered, in the customer's terms, with evidence
3. Risks to the renewal and how to address each
4. Likely objections and suggested responses
5. Expansion opportunities, if the evidence supports them
6. Questions to ask the customer in the next conversation

Rules:
- Use only the information provided. Mark assumptions clearly.
- Do not propose pricing or discounts. Flag where Sales or Finance input is needed.
- Keep the value story honest. If outcomes are thin, say so.

INPUT:
{paste here}
```

## Output format

Six labeled sections. Timeline as a short list.

## Known failure modes

- Overstates value when outcome data is weak.
- Suggests commercial terms. The rules forbid it, so review for it anyway.
