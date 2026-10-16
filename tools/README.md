# Tools

Small utilities that run on sample data. Standard-library Python 3, nothing to install.

| Tool | What it does |
|---|---|
| [`score_accounts.py`](score_accounts.py) | Scores accounts with the [Account Health Scoring](../frameworks/account-health-scoring.md) rubric and adds the [Weekly CSM Brief](../prompts/weekly-csm-brief.md#priority) priority. Reads a CSV in the [`sample-data`](../sample-data/README.md) format and writes the scored CSV to stdout |

```
python3 tools/score_accounts.py sample-data/accounts.csv --as-of 2026-10-01
```

Planned: an ROI calculator.
