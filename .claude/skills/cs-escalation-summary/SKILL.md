---
name: cs-escalation-summary
description: "Draft the write-up that opens a customer escalation (level, required fields, gaps), or the summary that closes one (outcome, root cause tag). Use when the user is opening or closing an escalation."
---

# Escalation Summary

1. Read `prompts/escalation-summary.md` in this repository. It is the source of truth for this task. Follow the current file, not your memory of it.
1. Check the user has given what its **Inputs** section lists. Ask only for what the prompt cannot work without. Leave smaller gaps to the prompt's own rules for missing data.
1. The prompt file has two prompts. Use "open an escalation" or "close an escalation" according to what the user is doing, and ask if it is unclear.
1. Carry out the instructions in its **Prompt** section, with the user's material in place of the placeholders.
1. Format the result as its **Output format** section says.
1. Before replying, check the result against its **Known failure modes** and fix anything you find.

## Ground rules

- You draft, score, and flag. A person decides on escalations, pricing, and commitments.
- Never send, post, or write anything to a customer or a system of record. Return drafts.
- Use only the material the user gives you, plus this repository's docs.
