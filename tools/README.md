# Tools

Small utilities that run on sample data. Standard-library Python 3, nothing to install.

| Tool | What it does |
|---|---|
| [`score_accounts.py`](score_accounts.py) | Scores accounts with the [Account Health Scoring](../frameworks/account-health-scoring.md) rubric and adds the [Weekly CSM Brief](../prompts/weekly-csm-brief.md#priority) priority |
| [`outcome_progress.py`](outcome_progress.py) | Measures each success plan goal against its baseline and target, per the [Outcome Library](../frameworks/outcome-library.md#measuring-progress) rules |
| [`value_report.py`](value_report.py) | Rolls goal statuses and adoption readings up into a book-level report of the value realized, for CS leadership and the [Outcome Review](../playbooks/outcome-review.md) |
| [`renewal_window.py`](renewal_window.py) | Lists the accounts renewing in the next 120 days with the fields the [Pre-Renewal Check](../prompts/pre-renewal-check.md) needs |
| [`roi_calculator.py`](roi_calculator.py) | Estimates the first-year ROI of running a CS team with an AI copilot, in three scenarios |
| [`check_repo.py`](check_repo.py) | Checks the repo is complete: required sections, links and anchors, the README index, skills, and that the tools run. CI runs it on every push |

## Health score calculator

```
python3 tools/score_accounts.py sample-data/accounts.csv --plans sample-data/success-plans.csv --as-of 2026-10-01
```

Reads the accounts and success plans in the [`sample-data`](../sample-data/README.md) format and writes the scored CSV to stdout, sorted by priority. The Outcomes signal comes from `--plans`. Without it, Outcomes is missing for every account, the no-measured-outcomes override caps them all at Yellow, and a warning says so. The rubric, outputs, and failure modes are documented in [Account Health Scoring](../frameworks/account-health-scoring.md).

## Outcome progress

```
python3 tools/outcome_progress.py sample-data/success-plans.csv --adoption sample-data/feature-adoption.csv --as-of 2026-10-01
```

### Purpose

Show each success plan goal's progress from baseline to target, and whether the features behind it are in use, so a CSM can bring the numbers to a QBR or renewal. It also gives the health score the goal statuses behind its Outcomes signal.

### Inputs

A success plans CSV in the [`sample-data`](../sample-data/README.md#fields-in-success-planscsv) format, and an `--as-of` date (default today), used to judge staleness and missed targets.

Optional: `--adoption`, a [feature adoption CSV](../sample-data/README.md#fields-in-feature-adoptioncsv), and `--library`, the Outcome Library file (default [`frameworks/outcome-library.md`](../frameworks/outcome-library.md)). The tool reads each outcome's features from the library table's "Depends on" column, so keep that table's columns in place.

### Outputs

A CSV on stdout with one row per goal: account, outcome, goal, owner, unit, baseline, target and target date, latest value and date, progress and expected progress (in percent), and status. With `--adoption`, three more columns: support, the lightly used features with their adoption, and the reading (Proven, Unexplained progress, Adoption gap, or Not converting). The rules are in the [Outcome Library](../frameworks/outcome-library.md#measuring-progress).

For the sample data with adoption: 16 goals are Proven, 2 show Unexplained progress, 9 have an Adoption gap, and 4 are Not converting.

A summary line goes to stderr with the count of goals in each status. For the sample data as of 2026-10-01: 11 accounts and 40 goals, with 3 met, 19 on track, 10 off track, 3 missed, 1 with no baseline, and 4 stale.

### Failure modes

- **Invalid goal rows.** A missing target, a target equal to the baseline, a target date before the baseline date, or a current value without a date. The tool exits with the file, line, and account, and writes nothing.
- **Plans outside 3 to 4 goals.** A warning names the account. The goals are still measured.
- **Unknown outcome IDs.** The tool does not read the library. The [repo checker](#repo-checker) checks the sample file's IDs against it; check your own file the same way.
- **Straight-line expectations.** Expected progress assumes steady improvement. The 25-point tolerance absorbs some lag, but a goal that improves late in its window can show Off track early. Read the trend, not just one status.
- **Feature names that don't match.** A feature in the adoption file that isn't spelled as in the library is ignored, which can make an outcome's support Unknown. The repo checker checks the sample file's names.
- **Measurements that aren't comparable.** The tool trusts that the baseline and later values come from the same source and definition. It can't tell if they don't.

## Value report

```
python3 tools/value_report.py sample-data/accounts.csv --plans sample-data/success-plans.csv --adoption sample-data/feature-adoption.csv --as-of 2026-10-01
```

### Purpose

Show what a book of accounts has realized from its success plans, in the customer's numbers, with proof the product delivered it. It is the CS value case described in [Adoption as a Service](../specs/adoption-as-a-service.md#outputs), and the input to the [Outcome Review](../playbooks/outcome-review.md).

### Inputs

The accounts CSV (for names and ARR), `--plans` (required), `--adoption` (needed to prove any goal), `--library` (default [`frameworks/outcome-library.md`](../frameworks/outcome-library.md)), and `--as-of`. Run it on one CSM's accounts or the whole book.

### Outputs

Markdown on stdout, in four sections:

- **Book summary:** accounts with a success plan and their ARR, goals counted, goals met or on track, Proven goals, ARR on accounts with at least one Proven outcome, the customer-agreed annual value of Proven goals, and data gaps.
- **By outcome:** for each outcome picked, the plans that picked it, counts by status, median progress, and counts by reading.
- **Customer-agreed value:** each goal with an agreed value per unit, its improvement so far, the annual value, and whether it is counted (Proven goals only) or why not.
- **For the outcome review:** outcomes not converting at 2 or more accounts, for Product. Lightly used features behind adoption gaps, for enablement. Met and Proven goals, for Marketing to ask permission to use. Unexplained progress not to claim.

For the sample data as of 2026-10-01: 11 of 12 accounts have a plan, 22 of 35 counted goals are met or on track, and 16 are Proven. $1,850,000 of $2,240,000 ARR (83%) is on accounts with at least one Proven outcome, and Proven goals carry $625,500 of customer-agreed annual value. Faster month-end close is not converting at two accounts.

### Failure modes

- **No adoption file.** Nothing can be Proven, so the Proven counts and value are zero. A warning says so.
- **Reading the value total as revenue.** It is the customer's own estimate of what the improvement is worth to them. It supports the value story, and it is not a number to book or add to the [ROI calculator](#roi-calculator)'s results.
- **ARR with a proven outcome read as ARR saved.** An account with one Proven goal can still churn. The figure shows how much of the book can see evidence, not how much is safe.
- **Small numbers.** Median progress and status counts on an outcome picked by 2 or 3 plans are anecdotes. The outcome review's 2-account and 5-account rules apply.
- **Plans for unknown accounts.** Goals whose account isn't in the accounts CSV are still counted, with the ID in place of a name, and a warning lists them.

## Renewal window

```
python3 tools/renewal_window.py sample-data/accounts.csv --plans sample-data/success-plans.csv --as-of 2026-10-01 --days 120
```

### Purpose

Give the [Pre-Renewal Check](../prompts/pre-renewal-check.md) its input in one step, instead of matching rows across `scored-accounts.csv` and `accounts.csv` by hand.

### Inputs

The accounts and success plans in the [`sample-data`](../sample-data/README.md) format (`--plans`, as for the health score calculator), an `--as-of` date (default today), and `--days`, the window length (default 120).

### Outputs

A CSV on stdout with one row per account renewing within the window, soonest first: ID, account, ARR, renewal date, days to renewal, band, index, overrides, top drivers, success plan summary, red flags, open escalations, days since executive contact, contract flags, and notes. Paste it into the prompt as-is. Scoring comes from [`score_accounts.py`](score_accounts.py), so the bands always match the rubric.

A summary line goes to stderr: how many accounts are in the window, and their total ARR. Check that count against your renewal report.

It does not assign readiness statuses. The prompt does that, and the CSM decides what to do with them.

For the sample data as of 2026-10-01, five accounts with $860,000 ARR are in the window, the same five as the [prompt's example](../prompts/pre-renewal-check.md#example).

### Failure modes

- **Missing columns.** Exits with the list of missing columns and writes nothing.
- **A row that can't be scored**, such as a renewal date not in YYYY-MM-DD format. The row is left out, a warning names it, and the tool exits non-zero, so a dropped account does not go unnoticed.
- **Renewal date already passed.** The row is left out with a warning: either the account renewed and the date is stale, or the renewal slipped. Find out which.
- **Empty window.** Writes only the header, and the summary line says 0 accounts. Check the `--as-of` date before concluding nothing is renewing.
- **Stale data.** The window is only as current as the CSV. A renewal date that moved in the CRM but not in the export puts an account in the wrong window.

## Repo checker

```
python3 tools/check_repo.py
```

Prints "All checks passed." or a list of every problem, and exits non-zero on failure. It checks:

- **Required sections** by folder. Frameworks need Purpose, Inputs, Outputs, and Failure modes. Prompts need Purpose, Inputs, Prompt, Output format, and Known failure modes. Playbooks need Purpose, Trigger, Inputs, Steps, Outputs, and Failure modes. Specs need Goals, Non-goals, Inputs, Outputs, Safety and trust, and Failure modes. These match the [templates](../templates/README.md)
- **Links:** every relative link points at a file that exists, and every `#anchor` at a heading that exists
- **Index:** the README links to every doc in `frameworks/`, `specs/`, `prompts/`, `playbooks/`, and `essays/`
- **Skills:** each prompt has exactly one skill, each skill points at a prompt that exists and has valid frontmatter, and the README's skills table lists every skill
- **Tools:** each tool runs on the sample data, and `sample-data/scored-accounts.csv` matches a fresh scoring run
- **Outcome IDs:** every `outcome_id` in `sample-data/success-plans.csv` is in the [Outcome Library](../frameworks/outcome-library.md), or is `custom`
- **Feature names:** every feature in `sample-data/feature-adoption.csv` is named in the library's "Depends on" column

It does not judge whether the content is right. That is still a review.

## ROI calculator

```
python3 tools/roi_calculator.py sample-data/roi-inputs.json
```

### Purpose

Give a CS leader an honest first-year business case for a copilot like the one in the [CSM Copilot spec](../specs/csm-copilot-spec.md), with the cash return kept apart from the time savings.

### Inputs

A JSON file. [`sample-data/roi-inputs.json`](../sample-data/roi-inputs.json) is a filled-in example for a fictional 8-CSM team.

| Field | Meaning |
|---|---|
| `ramp_months` | Months before benefits start. Adoption takes time, and retained ARR only lands at renewal |
| `team.csm_count` | CSMs using the copilot |
| `team.loaded_cost_per_hour` | Salary, benefits, and overhead per CSM hour |
| `team.working_weeks_per_year` | Weeks a CSM actually works |
| `time_savings[]` | Per task: hours per CSM per week before and after the copilot. Measure "before" with a time study, not a guess |
| `retention.arr_under_management` | Total ARR across the team's books |
| `retention.gross_churn_rate_pct` | ARR lost to churn and downgrades in a year, as a percent |
| `retention.churn_reduction_pct` | Relative reduction in churn you expect from earlier risk detection. 10 means 12% churn becomes 10.8% |
| `costs.license_per_user_per_month` | Copilot cost per CSM |
| `costs.one_time_implementation` | Setup, integration, and training |
| `costs.admin_hours_per_month` | Ongoing upkeep: prompts, data quality, calibration |
| `scenarios` | Name and realization rate for each scenario: the share of estimated benefits that actually happens |

### How it calculates

- **Capacity freed** = hours saved per CSM per week x CSMs x working weeks x realization, for the months after the ramp. Valued at loaded cost.
- **Retained ARR** = ARR x gross churn rate x churn reduction x realization, for the months after the ramp.
- **First-year cost** = licenses + admin hours + one-time implementation.
- **ROI** = (benefit - cost) / cost, reported twice: cash only (retained ARR), and including capacity.
- **Payback** = months until cumulative benefit covers cumulative cost. Costs start in month 0. Benefits start after the ramp.

### Outputs

A markdown table with one column per scenario: hours freed, equivalent full-time CSMs, value of capacity freed, retained ARR, first-year cost, then net benefit, ROI, and payback, both cash-only and including capacity.

For the sample inputs, the base scenario (75% realization) shows $162,000 of retained ARR against $33,800 of first-year cost: a cash ROI of 3.8x, with payback in 4.4 months. It also frees about 1,700 CSM hours in year one.

### Failure modes

- **Counting capacity as cash.** Freed hours are worth money only if they are redeployed: more accounts per CSM, or a hire you don't make. That is why the table reports the cash ROI on its own. Lead with it.
- **Attributing all churn reduction to the tool.** Churn moves for many reasons. Set `churn_reduction_pct` from a pilot compared against a control group, not from a vendor claim. Even 10% is a strong assumption.
- **Guessed "before" hours.** Teams overestimate time spent on tasks they dislike. Time a sample week before the rollout.
- **Ignoring upkeep.** Prompts, data feeds, and scoring weights need maintenance. Don't set `admin_hours_per_month` to zero.
- **Reading a high ROI as a reason to skip the pilot.** Small costs make the ratio large even when the absolute benefit is modest. Look at the net benefit, and at the conservative column.
