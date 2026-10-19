---
name: cs-value-narrative
description: "Write the story of value delivered from a value report or one account's outcome progress, for a customer executive, CS leadership, the exec team, or the board. Use when the user asks to show or report the value CS or the product has delivered."
license: MIT
---

# Value Narrative

Part of [Outcome-Led CS Ops](https://github.com/laufferw/outcome-led-cs-ops), built for Claude.

1. Read [references/value-narrative.md](references/value-narrative.md). It is the source of truth for this task. Follow the file, not your memory of it.
1. Check the user has given what its **Inputs** section lists. Ask only for what the prompt cannot work without. Leave smaller gaps to the prompt's own rules for missing data.
1. Carry out the instructions in its **Prompt** section, with the user's material in place of the placeholders.
1. Format the result as its **Output format** section says.
1. Before replying, check the result against its **Known failure modes** and fix anything you find.

## Reference docs

Read these when the prompt refers to them:

- [references/outcome-library.md](references/outcome-library.md)
- [references/cs-metrics-scorecard.md](references/cs-metrics-scorecard.md)

## Building the input

If the user gives raw account data instead of the input above, and you are running in Claude Code with the Outcome-Led CS Ops plugin installed:

- To build the value report: `python3 "${CLAUDE_PLUGIN_ROOT}/tools/value_report.py" <accounts.csv> --plans <success-plans.csv> --adoption <feature-adoption.csv> --as-of <date>`
- To add the scorecard, for leadership audiences: `python3 "${CLAUDE_PLUGIN_ROOT}/tools/cs_scorecard.py" <accounts.csv> --plans <success-plans.csv> --adoption <feature-adoption.csv> --history <renewal-history.csv> --as-of <date>`

Ask for the as-of date if it is not clear. Anywhere else, ask the user to paste the input, or to run the tool from the [repository](https://github.com/laufferw/outcome-led-cs-ops).

## Ground rules

- You draft, score, and flag. A person decides on escalations, pricing, and commitments.
- Never send, post, or write anything to a customer or a system of record. Return drafts.
- Use only the material the user gives you, plus the files in this skill.
