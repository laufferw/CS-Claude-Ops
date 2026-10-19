# Guide: CS Operations and RevOps

> For the person who runs the system: connects the data, keeps the definitions, and runs the weekly and quarterly reports.

## Who it's for

CS Ops, RevOps, or whoever owns CS data and process. You make the tools run on the real book, keep the rubric and library calibrated, and make sure every number leadership sees has one definition. The essay [CS Ops Is a Discipline, Not a Help Desk](../essays/cs-ops-is-a-discipline.md) is the job description.

## What you need

- Report-building access to the CRM, product analytics, ticketing, and billing
- One account ID every system can export
- Finance's definitions of retention, to reconcile with the [CS Metrics Scorecard](../frameworks/cs-metrics-scorecard.md)
- Python 3 (standard library only; nothing to install)

## Your week

| When | Do | With |
|---|---|---|
| Once, then on any system change | Map exports to the repo formats and check coverage | [Connect Your Data](../playbooks/connect-your-data.md), [`tools/import_data.py`](../tools/import_data.py) |
| Monday, early | Refresh exports, import, and score | `import_data.py`, then [`tools/score_accounts.py`](../tools/score_accounts.py) |
| Monday | Run each CSM's week, and the team rollup and forecast for the director | [`tools/run_week.py`](../tools/run_week.py), [`tools/team_rollup.py`](../tools/team_rollup.py), [`tools/renewal_forecast.py`](../tools/renewal_forecast.py) |
| Monthly | Scorecard and value report for leadership; review CSM overrides | [`tools/cs_scorecard.py`](../tools/cs_scorecard.py), [`tools/value_report.py`](../tools/value_report.py) |
| Quarterly | Outcome Review, and calibration of weights, ranges, and forecast weights | [Outcome Review](../playbooks/outcome-review.md), each framework's Calibration section |
| On every change | Keep docs and tools consistent | `python3 tools/check_repo.py` |

## What you get

- The real book in the tools' formats, refreshed weekly, with a coverage report
- Per-CSM weekly bundles, and the director's rollup and forecast
- A monthly scorecard whose numbers match Finance's
- A calibration record: what changed in the rubric, library, and weights, and why

## Start here

1. Run [`tools/import_data.py`](../tools/import_data.py) on the [sample exports](../sample-data/exports/mapping.json) and see it reproduce `sample-data/accounts.csv`.
2. Fill in the field table in [Connect Your Data](../playbooks/connect-your-data.md#where-each-field-usually-lives) for your systems.
3. Read the [Calibration](../frameworks/account-health-scoring.md#calibration) sections, and book the first back-test.

## Failure modes

- **Becoming the report desk.** When someone asks for a new report, ask what decision it serves. Often a rule already covers it.
- **Silent mapping fixes.** A `default` in a mapping hides bad data. Fix sources, and record every default's reason.
- **Calibration that never happens.** Weights and thresholds here are starting points. Put the quarterly calibration on the calendar.
- **Numbers that differ from Finance's.** Reconcile before the first leadership report, not after.
