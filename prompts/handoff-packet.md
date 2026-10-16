# Prompt: Handoff Packet

## Purpose

Draft the closed-won handoff packet from the [Sales to CS Handoff](../playbooks/sales-to-cs-handoff.md) playbook from what Sales already has, so the rep reviews and fills gaps instead of starting from a blank page.

## Inputs

Deal notes, call notes or transcripts, the email thread with the customer, the contact list with roles, and the contract or order form summary.

## Prompt

```
You are helping hand a newly closed deal from Sales to Customer Success. Using only the material below, draft the handoff packet.

Fill in each section, citing the source (for example, "call notes, Aug 12") for every item:
1. Customer goals and the success criteria they were sold
2. Key stakeholders: name, role, and whether each is the champion, the executive sponsor, or neither
3. Commitments made during the sale: scope, timelines, terms, and anything promised informally
4. Contract summary: term, renewal date, ARR, special clauses
5. Known risks or concerns from the sales process
6. Technical or integration requirements

Then:
- Answer in two sentences: why did they buy, and what does success look like for them?
- List questions the sales rep must answer before the handoff call.

Rules:
- If a section has nothing in the material, write "NOT FOUND" and add a question for the rep.
- Under commitments, include anything that sounds like a promise ("we can do that", "that will be ready by"), even if casual. Mark these "informal" so the CSM can confirm them.
- Do not infer a champion or executive sponsor from job title alone. Say who the material shows acting in that role.
- Quote numbers and dates exactly as they appear. If sources disagree, show both.

MATERIAL:
{paste here}
```

## Output format

Six labeled sections with a source on every item, then the two-sentence answer, then the rep's questions.

## Known failure modes

- Misses informal promises buried in long threads. The rule asks for anything promise-shaped. The rep still confirms the list.
- Names the most senior contact as executive sponsor. The prompt asks for evidence of the role.
- Produces a complete-looking packet from thin material. Count the NOT FOUND sections. If the two-sentence answer is vague, the playbook's quality check fails.
