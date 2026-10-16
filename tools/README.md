# Tools

Small utilities that run on sample data. Standard-library Python 3, nothing to install.

| Tool | What it does |
|---|---|
| [`score_accounts.py`](score_accounts.py) | Scores accounts with the [Account Health Scoring](../frameworks/account-health-scoring.md) rubric and adds the [Weekly CSM Brief](../prompts/weekly-csm-brief.md#priority) priority |
| [`roi_calculator.py`](roi_calculator.py) | Estimates the first-year ROI of running a CS team with an AI copilot, in three scenarios |
| [`check_repo.py`](check_repo.py) | Checks the repo is complete: required sections, links and anchors, the README index, skills, and that the tools run. CI runs it on every push |

## Health score calculator

```
python3 tools/score_accounts.py sample-data/accounts.csv --as-of 2026-10-01
```

Reads a CSV in the [`sample-data`](../sample-data/README.md) format and writes the scored CSV to stdout, sorted by priority. The rubric, outputs, and failure modes are documented in [Account Health Scoring](../frameworks/account-health-scoring.md).

## Repo checker

```
python3 tools/check_repo.py
```

Prints "All checks passed." or a list of every problem, and exits non-zero on failure. It checks:

- **Required sections** by folder. Frameworks need Purpose, Inputs, Outputs, and Failure modes. Prompts need Purpose, Inputs, Prompt, Output format, and Known failure modes. Playbooks need Purpose, Trigger, Inputs, Steps, Outputs, and Failure modes. Specs need Goals, Non-goals, Inputs, Outputs, Safety and trust, and Failure modes. These match the [templates](../templates/README.md)
- **Links:** every relative link points at a file that exists, and every `#anchor` at a heading that exists
- **Index:** the README links to every doc in `frameworks/`, `specs/`, `prompts/`, `playbooks/`, and `essays/`
- **Skills:** each prompt has exactly one skill, each skill points at a prompt that exists and has valid frontmatter, and the README's skills table lists every skill
- **Tools:** both tools run on the sample data, and `sample-data/scored-accounts.csv` matches a fresh scoring run

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
