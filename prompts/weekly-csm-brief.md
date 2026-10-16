# Prompt: Weekly CSM Brief

## Purpose

Turn a CSM's scored book of accounts into the weekly brief described in the [Account Management Engine](../frameworks/account-management-engine.md): a short, ranked list of where to spend time this week, with the reasoning.

## Inputs

One CSM's accounts, already scored with [Account Health Scoring](../frameworks/account-health-scoring.md). Each row needs:

- Account, ARR, renewal date, days to renewal
- Index, band, coverage, missing signals, overrides, top drivers
- Last week's band, and whether the band moved
- Priority (see below)
- Expansion signals and recent notes, if any

[`tools/score_accounts.py`](../tools/score_accounts.py) produces this table. [`sample-data/scored-accounts.csv`](../sample-data/scored-accounts.csv) is an example.

### Priority

Priority is the ARR at risk, scaled by how soon the renewal is:

**Priority = ARR x risk weight x urgency**

| Band | Risk weight | | Days to renewal | Urgency |
|---|---|---|---|---|
| Red | 1.0 | | 90 or less | 1.0 |
| Yellow | 0.5 | | 91 to 180 | 0.6 |
| Insufficient data | 0.5 | | Over 180 | 0.3 |
| Green | 0.1 | | | |

## Prompt

```
You are a Customer Success analyst writing a weekly brief for one CSM. Use only the account data below.

Write these sections:

1. Top accounts this week (at most 5)
   Pick them in this order until you have 5:
   a. Accounts whose band moved down since last week
   b. Accounts with a red-flag override (non-renewal notice, sponsor departure, payment dispute)
   c. Remaining accounts by priority, highest first
   If (a) and (b) together exceed 5, keep the 5 with the highest priority and name the rest in one line.
   For each account give:
   - Why it is here: the band, the band move or override, and the top drivers, citing the numbers
   - One recommended action, with an owner
   - A deadline. If the band is Red, follow escalation logic: a plan within 3 business days.

2. Renewals in the next 120 days
   Every account renewing within 120 days, soonest first: renewal date, ARR, band, and a one-line status from the notes.

3. Expansion signals
   Accounts with an expansion signal and a band of Green or Yellow. Say what the signal is and the next step. Leave out Red accounts; note that you did.

4. Data gaps
   Accounts with Insufficient data, missing signals, or notes that contradict the score. Say what is missing and who could fix it.

Rules:
- Every claim cites a field from the data. Do not invent contacts, dates, or history.
- If a note explains a low score (for example, low usage that is normal for the account), say so and suggest a CSM override rather than an action.
- Do not propose pricing, discounts, or contract terms. Flag where Sales or Finance is needed.
- An account appears in section 1 at most once, but can also appear in sections 2 to 4.
- Keep the whole brief under 500 words.

ACCOUNTS:
{paste scored table here}
```

## Output format

Four headed sections. Section 1 is a numbered list. Sections 2 to 4 are short bullet lists. A section with nothing in it says "None this week."

## Example

From [`sample-data/scored-accounts.csv`](../sample-data/scored-accounts.csv), scored as of 2026-10-01, a correct brief has:

- **Top accounts:**
  - Band moves down: Cedar Health Partners (Yellow to Red) and Granite Payroll (Green to Yellow, capped by the sponsor departure).
  - Red-flag overrides: Quarry Lane Media (non-renewal notice) and Larkspur Retail (payment dispute).
  - Highest remaining priority: Sable Energy.
  - Pinecrest Manufacturing has a higher priority than three of these, but it neither moved band nor has a red flag, so it misses the cut.
- **Renewals in 120 days:** Orchard Learning (30 days), Larkspur Retail (50), Cedar Health Partners (75), Sable Energy (91), and Quarry Lane Media (106).
- **Expansion:** Bluefin Logistics (50 more seats) and Pinecrest Manufacturing (new plant).
- **Data gaps:** Meridian Analytics (usage and outcomes missing, coverage 50%). Tidewater Clinics' low usage is normal per the notes, so suggest an override.

## Known failure modes

- Lists ten accounts. The 5-account cap and selection order prevent this. Check the count.
- Ranks by ARR alone, so large healthy accounts crowd out small urgent ones. Priority weights for risk and urgency.
- Recommends expansion on an account at risk. Section 3 excludes Red accounts.
- Treats Insufficient data as healthy because the index is high. The data gaps section calls it out.
- Generic actions ("check in with the customer"). Each action needs an owner and a deadline. Reject the brief if they're missing.
