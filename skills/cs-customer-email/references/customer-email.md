# Prompt: Customer Email

## Purpose

Draft a customer-facing email for a CSM to review, edit, and send. Claude never sends it.

## Inputs

- What the email is for (follow-up, update on an issue, meeting request, renewal kickoff, check-in after a quiet period)
- The recipient's name and role
- Account context: recent meetings, open issues, health band
- The points to make, and anything that must not be said
- Tone: formal, friendly, or direct

## Prompt

```
You are drafting an email from a Customer Success Manager to a customer. The CSM will review and send it.

Write a subject line and a body that:
- States the purpose in the first two sentences
- Covers each point below, in plain language
- Ends with one clear next step and, if a meeting is wanted, a suggested time window
- Is under 200 words unless the purpose needs more

Rules:
- Make no commitments on SLAs, pricing, discounts, contract terms, roadmap dates, or feature delivery. If a point needs one, write [NEEDS APPROVAL: what and from whom] in its place.
- State only facts that appear in the context. Mark anything you are unsure of with [CONFIRM].
- Do not mention internal health scores, bands, or risk ratings.
- Do not over-apologize or blame other teams. One acknowledgement of a problem is enough.

After the email, list every factual claim it makes, so the CSM can check them.

PURPOSE:
{purpose}

RECIPIENT:
{name, role}

CONTEXT:
{context}

POINTS TO MAKE:
{points}

MUST NOT SAY:
{anything off limits}

TONE:
{tone}
```

## Output format

Subject line, email body, then a bullet list of factual claims to verify. Placeholders in square brackets show what the CSM must resolve before sending.

## Known failure modes

- Slips in a soft commitment ("we'll have that fixed next week"). The rules forbid it, but read for promise-shaped phrases anyway.
- Leaks internal language ("your account is Yellow"). The rules forbid it.
- Gets the relationship tone wrong for a long-standing contact. Give it a past email from the CSM as a style sample if tone matters.
