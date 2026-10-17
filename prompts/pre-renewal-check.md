# Prompt: Pre-Renewal Check

## Purpose

Check every account renewing in the next 120 days for readiness, so problems surface while there is still time to act. Accounts that need work go on to [Renewal Prep](renewal-prep.md).

## Inputs

For each account renewing in the window: ARR, renewal date, days to renewal, band and index, overrides, top drivers, open escalations, days since executive contact, contract flags, and recent notes.

Get them in one step with the [renewal window tool](../tools/README.md#renewal-window), and paste its output:

```
python3 tools/renewal_window.py sample-data/accounts.csv --as-of 2026-10-01
```

## Prompt

```
You are a Customer Success analyst checking renewal readiness. Use only the data below.

Consider only accounts with 120 or fewer days to renewal. For each one, assign a status using the first rule that matches:
- At risk: band is Red, or any red flag (non-renewal notice, sponsor departure, payment dispute)
- Unclear: band is Insufficient data
- Needs work: band is Yellow, or any open escalation, or executive contact more than 60 days ago or never, or any open contract flag
- Ready: none of the above

For each account return:
- Status, and the rule that set it
- What is in place, citing the data
- Gaps, citing the data
- Next step with an owner, and whether to start Renewal Prep now (yes for anything not Ready)
- Who else needs to be involved (Sales, Finance, Legal, Support), if anyone

Then a summary line: how much ARR is in each status.

Rules:
- Order accounts by days to renewal, soonest first.
- At risk accounts with a Red band also follow escalation logic. Say so.
- Do not propose pricing, discounts, or terms. Name who owns that decision.

ACCOUNTS:
{paste data here}
```

## Output format

One short block per account, soonest renewal first, then the ARR summary line.

## Example

From the sample data as of 2026-10-01, five accounts are in the window:

| Account | Days | Status | Why |
|---|---|---|---|
| Orchard Learning | 30 | Ready | Green, no escalations, exec contact 15 days ago, paperwork sent |
| Larkspur Retail | 50 | At risk | Payment dispute |
| Cedar Health Partners | 75 | At risk | Red band, renewing within 90 days: an L2 escalation |
| Sable Energy | 91 | Needs work | Yellow, exec contact 62 days ago, downgrade request |
| Quarry Lane Media | 106 | At risk | Non-renewal notice |

That puts $38,000 in Ready, $280,000 in Needs work, and $542,000 at risk.

## Known failure modes

- Marks an account Ready on a high index while a note shows a problem. The rules check flags and contact, not just the band. Read the notes column too.
- Starts negotiating, suggesting discounts to save at-risk renewals. The rules forbid it.
- Drops accounts at the edge of the window. Check the count against your renewal report.
