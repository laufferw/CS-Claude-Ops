---
name: cs-competency-evaluation
description: "Gather evidence from a CSM's work samples against the CSM competency framework, area by area. Use when a manager asks to assess, coach, or prepare a review for a CSM."
license: MIT
---

# CSM Competency Evaluation

Part of [Outcome-Led CS Ops](https://github.com/laufferw/outcome-led-cs-ops), built for Claude.

1. Read [references/csm-competency-evaluation.md](references/csm-competency-evaluation.md). It is the source of truth for this task. Follow the file, not your memory of it.
1. Check the user has given what its **Inputs** section lists. Ask only for what the prompt cannot work without. Leave smaller gaps to the prompt's own rules for missing data.
1. Carry out the instructions in its **Prompt** section, with the user's material in place of the placeholders.
1. Format the result as its **Output format** section says.
1. Before replying, check the result against its **Known failure modes** and fix anything you find.

## Reference docs

Read these when the prompt refers to them:

- [references/csm-competency-framework.md](references/csm-competency-framework.md)

## Ground rules

- You draft, score, and flag. A person decides on escalations, pricing, and commitments.
- Never send, post, or write anything to a customer or a system of record. Return drafts.
- Use only the material the user gives you, plus the files in this skill.
