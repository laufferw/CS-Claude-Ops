# Prompt: Internal Account Update

## Purpose

Draft a short internal update on one account for a manager, an account team, or a leadership channel: where it stands, what changed, and what help is needed.

## Inputs

- The account's ARR, renewal date, health band, and the band last time you reported
- What changed since the last update
- Open risks and escalations
- What you need from others, if anything
- Who the update is for

## Prompt

```
You are helping a Customer Success Manager write an internal update on one account. Use only the information below.

Write, in this order:
1. One line up front: the account, its band, and the single most important thing the reader needs to know
2. What changed since the last update (facts, with dates)
3. Risks, each with how serious it is and what is being done
4. Asks: what you need, from whom, by when. If nothing, say "No asks."
5. Next steps, with owners and dates

Rules:
- Under 150 words.
- Put bad news first. If the band dropped, say so in the first line.
- Separate facts from judgment. Label judgment as such ("I think", "likely").
- Every ask names a person or team and a date.
- Do not include customer contact details or contract terms beyond ARR and renewal date. Updates get forwarded.

INFORMATION:
{paste here}

AUDIENCE:
{who it is for}
```

## Output format

Five short labeled sections, under 150 words in total.

## Known failure modes

- Buries the headline in paragraph three. The first-line rule fixes this. Check that the first line could stand alone.
- Asks with no owner ("we need help with pricing"). The rules require a name and date.
- Reads as more confident than the data. Look for judgment stated as fact.
