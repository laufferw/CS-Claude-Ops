---
name: cs-account-review
description: "Write a one-page review of a single customer account: snapshot, what's going well, risks, stakeholder map, next actions, and data gaps. Use when the user asks to review, summarize, or assess one account."
license: MIT
---

# Account Review

Part of [Outcome-Led CS Ops](https://github.com/laufferw/outcome-led-cs-ops), built for Claude.

1. Read [references/account-review.md](references/account-review.md). It is the source of truth for this task. Follow the file, not your memory of it.
1. Check the user has given what its **Inputs** section lists. Ask only for what the prompt cannot work without. Leave smaller gaps to the prompt's own rules for missing data.
1. Carry out the instructions in its **Prompt** section, with the user's material in place of the placeholders.
1. Format the result as its **Output format** section says.
1. Before replying, check the result against its **Known failure modes** and fix anything you find.

## Reference docs

Read these when the prompt refers to them:

- [references/account-health-scoring.md](references/account-health-scoring.md)

## Building the input

If the user gives raw account data instead of the input above, and you are running in Claude Code with the Outcome-Led CS Ops plugin installed:

- To score the book: `python3 "${CLAUDE_PLUGIN_ROOT}/tools/score_accounts.py" <accounts.csv> --plans <success-plans.csv> --as-of <date>`
- To measure the account's goals: `python3 "${CLAUDE_PLUGIN_ROOT}/tools/outcome_progress.py" <success-plans.csv> --adoption <feature-adoption.csv> --as-of <date>`

Ask for the as-of date if it is not clear. Anywhere else, ask the user to paste the input, or to run the tool from the [repository](https://github.com/laufferw/outcome-led-cs-ops).

## Ground rules

- You draft, score, and flag. A person decides on escalations, pricing, and commitments.
- Never send, post, or write anything to a customer or a system of record. Return drafts.
- Use only the material the user gives you, plus the files in this skill.
