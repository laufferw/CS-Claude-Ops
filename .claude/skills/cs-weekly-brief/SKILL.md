---
name: cs-weekly-brief
description: "Write a weekly brief for one CSM's book of accounts: top accounts to act on, renewals in 120 days, expansion signals, and data gaps. Use when the user asks for a weekly brief, a book review, or what to focus on this week, and provides account data."
---

# Weekly CSM Brief

1. Read `prompts/weekly-csm-brief.md` in this repository. It is the source of truth for this task. Follow the current file, not your memory of it.
1. Check the user has given what its **Inputs** section lists. Ask only for what the prompt cannot work without. Leave smaller gaps to the prompt's own rules for missing data.
1. If the user gives raw account signals (the `sample-data/accounts.csv` format) rather than scored accounts, score them first: `python3 tools/score_accounts.py <file> --as-of <date>`. Ask for the as-of date if it is not clear; do not assume today for sample data.
1. Carry out the instructions in its **Prompt** section, with the user's material in place of the placeholders.
1. Format the result as its **Output format** section says.
1. Before replying, check the result against its **Known failure modes** and fix anything you find.

## Ground rules

- You draft, score, and flag. A person decides on escalations, pricing, and commitments.
- Never send, post, or write anything to a customer or a system of record. Return drafts.
- Use only the material the user gives you, plus this repository's docs.
