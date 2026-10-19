---
name: cs-team-brief
description: "Draft a CS director's weekly brief across the team from the team rollup and renewal forecast: calls to challenge, risk by CSM, capacity, and data gaps. Use when a director or manager asks for a team review, team brief, or forecast review."
license: MIT
---

# Team Brief

Part of [Outcome-Led CS Ops](https://github.com/laufferw/outcome-led-cs-ops), built for Claude.

1. Read [references/team-brief.md](references/team-brief.md). It is the source of truth for this task. Follow the file, not your memory of it.
1. Check the user has given what its **Inputs** section lists. Ask only for what the prompt cannot work without. Leave smaller gaps to the prompt's own rules for missing data.
1. Carry out the instructions in its **Prompt** section, with the user's material in place of the placeholders.
1. Format the result as its **Output format** section says.
1. Before replying, check the result against its **Known failure modes** and fix anything you find.

## Reference docs

Read these when the prompt refers to them:

- [references/renewal-forecast.md](references/renewal-forecast.md)
- [references/capacity-model.md](references/capacity-model.md)

## Building the input

If the user gives raw account data instead of the input above, and you are running in Claude Code with the Outcome-Led CS Ops plugin installed:

- To roll the book up by CSM: `python3 "${CLAUDE_PLUGIN_ROOT}/tools/team_rollup.py" <accounts.csv> --plans <success-plans.csv> --capacity <capacity.json> --as-of <date>`
- To forecast renewals: `python3 "${CLAUDE_PLUGIN_ROOT}/tools/renewal_forecast.py" <accounts.csv> --plans <success-plans.csv> --calls <forecast-calls.csv> --as-of <date>`

Ask for the as-of date if it is not clear. Anywhere else, ask the user to paste the input, or to run the tool from the [repository](https://github.com/laufferw/outcome-led-cs-ops).

## Ground rules

- You draft, score, and flag. A person decides on escalations, pricing, and commitments.
- Never send, post, or write anything to a customer or a system of record. Return drafts.
- Use only the material the user gives you, plus the files in this skill.
