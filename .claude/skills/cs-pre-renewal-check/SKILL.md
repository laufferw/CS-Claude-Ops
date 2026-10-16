---
name: cs-pre-renewal-check
description: "Check every account renewing in the next 120 days and give each a readiness status (Ready, Needs work, At risk, Unclear). Use when the user asks about upcoming renewals across a book."
---

# Pre-Renewal Check

1. Read `prompts/pre-renewal-check.md` in this repository. It is the source of truth for this task. Follow the current file, not your memory of it.
1. Check the user has given what its **Inputs** section lists. Ask only for what the prompt cannot work without. Leave smaller gaps to the prompt's own rules for missing data.
1. The prompt needs fields from both the scored table and the raw signals. With files in the `sample-data` format, read both and join them on `account_id`.
1. Carry out the instructions in its **Prompt** section, with the user's material in place of the placeholders.
1. Format the result as its **Output format** section says.
1. Before replying, check the result against its **Known failure modes** and fix anything you find.

## Ground rules

- You draft, score, and flag. A person decides on escalations, pricing, and commitments.
- Never send, post, or write anything to a customer or a system of record. Return drafts.
- Use only the material the user gives you, plus this repository's docs.
