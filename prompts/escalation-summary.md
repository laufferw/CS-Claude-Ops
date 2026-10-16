# Prompt: Escalation Summary

## Purpose

Draft the two written records [Escalation Logic](../frameworks/escalation-logic.md) requires: the write-up that opens an escalation, and the summary that closes it.

## Inputs

**To open:** the account's ARR, renewal date, and health band; what happened, with dates; the customer's own words (an email, ticket, or call notes); anything already promised.

**To close:** the opening write-up, what was done and when, the outcome, and the customer's latest response.

## Prompt: open an escalation

```
You are helping a Customer Success Manager open an escalation. Use only the information below.

1. Recommend a level (L1, L2, or L3) using these triggers, and name the trigger that applies:
   - L1: health index drops into Red; exec sponsor leaves or goes silent for 30 days; no first value 90 days after close
   - L2: customer formally raises a contract or SLA concern; renewal at risk within 90 days (at risk means a Red band, or a non-renewal notice, sponsor departure, or payment dispute)
   - L3: threat of termination or legal involvement
   If more than one applies, use the highest.

2. Fill in the required fields:
   - Account, ARR, and renewal date
   - What happened and when
   - What the customer asked for, in their words (quote them)
   - What we can and cannot commit to, as far as the information shows
   - Owner and next-update date, based on the level's response target
     (L1: plan within 3 business days, owned by the CSM; L2: 2 business days, CS manager; L3: same business day, VP)

3. List anything missing that the owner needs before acting.

Rules:
- If a required field is not in the information, write "MISSING" rather than guessing.
- Quote the customer exactly. Do not paraphrase their ask into something easier to meet.
- Under "can commit to", list only what is already in our standard terms or already approved. Everything else is "needs sign-off from" the function that owns it (Support, Legal, Finance, Sales).

INFORMATION:
{paste here}
```

## Prompt: close an escalation

```
You are helping close an escalation. Use only the information below.

Write:
1. A summary of no more than five sentences: what happened, what we did, and how it ended
2. A primary root cause tag, and a secondary tag only if it changed the outcome. Choose from:
   product-defect, product-gap, adoption, support-responsiveness, sponsor-change,
   expectation-mismatch, commercial, contract-terms, customer-org-change
   Give one sentence of evidence for each tag.
3. Any commitments made during the escalation that must now be tracked, with an owner
4. One thing that would have caught this earlier, if the information suggests one

Rules:
- If the outcome is not clear from the information, say "Not resolved" and do not write a closing summary.
- Pick the tag for the cause, not the symptom: a slow fix for a bug is product-defect unless the delay itself was the complaint.

INFORMATION:
{paste here}
```

## Output format

Opening: the level with its trigger, then the required fields as a labeled list, then missing items. Closing: four numbered sections.

## Known failure modes

- Chooses a lower level to avoid alarm. The prompt says to use the highest trigger that applies.
- Softens the customer's ask in paraphrase. The prompt requires a direct quote.
- Lists commitments nobody approved under "can commit to". Check that section against your standard terms before sending it anywhere.
- Tags the symptom instead of the cause, which makes quarterly tag reviews useless.
