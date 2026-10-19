# Guide: Customer Success Manager

> For a frontline CSM: what to run each week, and which skill to use for each moment with a customer.

## Who it's for

A CSM who owns a book of accounts. It helps you decide where to spend this week, prepare for QBRs and renewals, prove the value your customers got, and draft the writing in between. You decide what to do. Claude drafts.

## What you need

- Your accounts, success plans, and feature adoption in the [`sample-data`](../sample-data/README.md) formats. CS Ops sets this up once with [Connect Your Data](../playbooks/connect-your-data.md). Until then, practice on the sample book as Sam Example
- Claude Code, opened in this repository, under your company's [AI Usage Policy](../frameworks/ai-usage-policy.md). Know which data is never allowed
- Your forecast call for each account renewing in the next two quarters

## Your week

| When | Do | With |
|---|---|---|
| Monday | Run your week. It writes every report and a `week.md` that lists what to do | [`tools/run_week.py`](../tools/run_week.py) with `--csm "<your name>"` |
| Monday | Read your brief: top accounts, renewals, expansion, data gaps | `/cs-weekly-brief` on `scored.csv` |
| Monday | Update forecast calls for anything in "Calls to review" | `forecast.md`, then your calls file |
| As needed | Accounts renewing within 120 days | `/cs-pre-renewal-check`, then `/cs-renewal-prep` |
| As needed | A goal with an adoption gap | `/cs-adoption-plan` |
| As needed | A new customer, or a plan with no baselines | `/cs-success-plan` |
| As needed | QBR prep, then the follow-up email | `/cs-qbr-outline`, `/cs-customer-email` |
| As needed | A Red band or red flag | `/cs-escalation-summary`, then the [At-Risk Save Plan](../playbooks/at-risk-save-plan.md) |
| As needed | Status for your manager | `/cs-account-update` |

Try it on the sample: ask Claude "run my week as Sam Example as of 2026-10-01", or run:

```
python3 tools/run_week.py sample-data/accounts.csv --plans sample-data/success-plans.csv --adoption sample-data/feature-adoption.csv --calls sample-data/forecast-calls.csv --csm "Sam Example" --as-of 2026-10-01
```

## What you get

- A ranked list of where to spend the week, with the reasons
- Renewal readiness for every account inside 120 days
- Each customer's progress from baseline on the outcomes they chose, ready for a QBR
- Drafts of emails, QBR outlines, success plans, adoption plans, and escalations to review and send yourself

## Start here

1. Read the [Outcome Library](../frameworks/outcome-library.md): it defines the value you are there to prove.
2. Run your week on the sample as Sam Example, and read `week.md`.
3. Skim [Account Health Scoring](../frameworks/account-health-scoring.md) so you can explain any band to your manager.

## Failure modes

- **Sending drafts unread.** Every draft marks commitments it can't make as `[NEEDS APPROVAL]`. Resolve them before anything goes to a customer.
- **Arguing with the band instead of the data.** If a band looks wrong, find the signal causing it. Override with a written reason only when the data is right but misleading.
- **Claiming unproven results.** In QBRs and renewals, claim only Proven goals as the product's doing.
- **Skipping baselines.** A goal with no baseline can never show value. Get it in the first 30 days.
