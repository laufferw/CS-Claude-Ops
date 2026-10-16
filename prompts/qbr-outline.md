# Prompt: QBR Outline

## Purpose

Draft a slide-by-slide outline for a quarterly business review that centers on the customer's outcomes, not our product's features. The [QBR](../playbooks/qbr.md) playbook covers scheduling, internal review, and follow-up.

## Inputs

- The customer's goals and success criteria (the success plan, or the [handoff packet](handoff-packet.md) for a new account)
- Outcomes this quarter, with evidence (metrics, quotes, milestones)
- Usage and adoption data, and the trend
- Support summary: tickets, escalations, and how they were resolved
- Who will attend from the customer side
- Anything we want to ask for (a reference, an expansion conversation, an executive introduction), if appropriate

## Prompt

```
You are helping a Customer Success Manager prepare a quarterly business review. Using only the information below, write a slide-by-slide outline.

Use this structure, and skip any slide the information cannot support:
1. Their goals, in their words, and how we agreed to measure them
2. Outcomes this quarter against those goals, with evidence
3. Adoption: what is working and where usage is thin
4. Support: what came up and how it was handled
5. What did not go well, and what we are doing about it
6. Plan for next quarter: goals, owners, dates
7. Asks: what we need from them, and what we are asking for

For each slide give a title, three to five bullets, and the evidence behind each bullet.

Rules:
- Lead with their goals, not our features.
- If outcomes are thin, say so on slide 2 and make slide 5 carry the plan. Do not dress up weak results.
- Make no roadmap promises or pricing statements. Mark any slide that needs Product or Sales input with [NEEDS REVIEW: who].
- Include an ask on slide 7 only if the evidence supports it. Do not ask for expansion or a reference from an account with open escalations or a Red band.
- Tailor the depth to the attendees: executives get outcomes and plan; practitioners get adoption detail.

INFORMATION:
{paste here}

ATTENDEES:
{names and roles}
```

## Output format

Numbered slides, each with a title, bullets, and evidence. Skipped slides are listed at the end with the reason.

## Known failure modes

- Turns into a product update. The first rule puts their goals first. Count how many bullets are about features.
- Overstates outcomes. The prompt asks for evidence per bullet. Check each against the data.
- Puts an expansion ask in front of an unhappy customer. The ask rule blocks this for open escalations and Red accounts. Use judgment for Yellow.
