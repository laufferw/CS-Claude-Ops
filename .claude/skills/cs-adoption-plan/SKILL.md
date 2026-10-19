---
name: cs-adoption-plan
description: "Turn success plan goals with an adoption gap into a plan by feature: who, action, owners, and dates, plus what to check for goals that are not converting. Use when the user asks how to get a customer using the features behind their outcomes."
---

# Adoption Plan

1. Read `prompts/adoption-plan.md` in this repository. It is the source of truth for this task. Follow the current file, not your memory of it.
1. Check the user has given what its **Inputs** section lists. Ask only for what the prompt cannot work without. Leave smaller gaps to the prompt's own rules for missing data.
1. If the user gives raw data rather than tool output, run the tool its **Inputs** section names first (see `tools/README.md`). Ask for the as-of date if it is not clear; do not assume today for sample data.
1. Carry out the instructions in its **Prompt** section, with the user's material in place of the placeholders.
1. Format the result as its **Output format** section says.
1. Before replying, check the result against its **Known failure modes** and fix anything you find.

## Ground rules

- You draft, score, and flag. A person decides on escalations, pricing, and commitments.
- Never send, post, or write anything to a customer or a system of record. Return drafts.
- Use only the material the user gives you, plus this repository's docs.
