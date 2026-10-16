---
name: cs-redline-summary
description: "Summarize a customer's proposed contract changes (MSA, SOW, SLA) in plain language and route each to the function that owns it. Use when the user shares a redline or a list of contract changes. Not legal advice."
---

# Contract Redline Summary

1. Read `prompts/contract-redline-summary.md` in this repository. It is the source of truth for this task. Follow the current file, not your memory of it.
1. Check the user has given what its **Inputs** section lists. Ask only for what the prompt cannot work without. Leave smaller gaps to the prompt's own rules for missing data.
1. Carry out the instructions in its **Prompt** section, with the user's material in place of the placeholders.
1. Format the result as its **Output format** section says.
1. Before replying, check the result against its **Known failure modes** and fix anything you find.

## Ground rules

- You draft, score, and flag. A person decides on escalations, pricing, and commitments.
- Never send, post, or write anything to a customer or a system of record. Return drafts.
- Use only the material the user gives you, plus this repository's docs.
