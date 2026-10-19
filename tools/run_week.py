"""Run every weekly tool for one CSM, or the whole book, in one step.

Filters the inputs to one CSM's accounts, then writes the scored book, the
renewal window, the per-goal outcome report, the renewal forecast, and the
value report into one folder, with a week.md that says what to do with each
and which skill to use. Standard library only.

Usage:
    python3 tools/run_week.py sample-data/accounts.csv \
        --plans sample-data/success-plans.csv \
        --adoption sample-data/feature-adoption.csv \
        --calls sample-data/forecast-calls.csv \
        --csm "Sam Example" --as-of 2026-10-01
"""

import argparse
import csv
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

TOOLS = Path(__file__).resolve().parent


def filter_csv(src, dest, keep):
    """Copy the rows of src that keep() accepts to dest. Return the kept rows."""
    with open(src, newline="") as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader if keep(r)]
        fields = reader.fieldnames
    with open(dest, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return rows


def run(tool, args, dest, warnings):
    result = subprocess.run([sys.executable, str(TOOLS / tool), *args], capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"{tool} failed: {result.stderr.strip()}")
    Path(dest).write_text(result.stdout)
    warnings += [f"{tool}: {line}" for line in result.stderr.splitlines() if line.startswith("warning")]


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("accounts_csv")
    parser.add_argument("--plans", required=True, help="success plans CSV")
    parser.add_argument("--adoption", help="feature adoption CSV")
    parser.add_argument("--calls", help="CSM forecast calls CSV")
    parser.add_argument("--csm", help="the CSM to run for, as named in the csm column (default: the whole book)")
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today(),
                        help="date to run as of (YYYY-MM-DD)")
    parser.add_argument("--out", help="output folder (default out/<as-of>-<csm>)")
    args = parser.parse_args()

    out = Path(args.out or f"out/{args.as_of}" + (f"-{slug(args.csm)}" if args.csm else "-book"))
    out.mkdir(parents=True, exist_ok=True)
    inputs = out / "inputs"
    inputs.mkdir(exist_ok=True)

    accounts = filter_csv(args.accounts_csv, inputs / "accounts.csv",
                          lambda r: not args.csm or r["csm"] == args.csm)
    if not accounts:
        sys.exit(f"no accounts for CSM {args.csm!r} in {args.accounts_csv}")
    ids = {r["account_id"] for r in accounts}
    filter_csv(args.plans, inputs / "success-plans.csv", lambda r: r["account_id"] in ids)
    if args.adoption:
        filter_csv(args.adoption, inputs / "feature-adoption.csv", lambda r: r["account_id"] in ids)
    if args.calls:
        filter_csv(args.calls, inputs / "forecast-calls.csv", lambda r: r["account_id"] in ids)

    acc, as_of = str(inputs / "accounts.csv"), ["--as-of", str(args.as_of)]
    plans = ["--plans", str(inputs / "success-plans.csv")]
    adoption = ["--adoption", str(inputs / "feature-adoption.csv")] if args.adoption else []
    calls = ["--calls", str(inputs / "forecast-calls.csv")] if args.calls else []
    warnings = []
    run("score_accounts.py", [acc, *plans, *as_of], out / "scored.csv", warnings)
    run("renewal_window.py", [acc, *plans, *as_of], out / "renewal-window.csv", warnings)
    run("outcome_progress.py", [str(inputs / "success-plans.csv"), *adoption, *as_of], out / "outcome-progress.csv", warnings)
    run("renewal_forecast.py", [acc, *plans, *calls, *as_of], out / "forecast.md", warnings)
    run("value_report.py", [acc, *plans, *adoption, *as_of], out / "value-report.md", warnings)

    scored = list(csv.DictReader(open(out / "scored.csv", newline="")))
    window = list(csv.DictReader(open(out / "renewal-window.csv", newline="")))
    goals = list(csv.DictReader(open(out / "outcome-progress.csv", newline="")))
    bands = {b: sum(1 for r in scored if r["band"] == b) for b in ("Green", "Yellow", "Red", "Insufficient data")}
    drops = [r["account"] for r in scored if r["band_change"] == "down"]
    names = {r["account_id"]: r["account"] for r in accounts}
    gaps = sorted({names[g["account_id"]] for g in goals if g.get("reading") == "Adoption gap"})
    no_plan = sorted(names[i] for i in ids if not any(g["account_id"] == i for g in goals))
    unbaselined = sorted({names[g["account_id"]] for g in goals if g["status"] in ("No baseline", "Stale")})

    who = args.csm or "the whole book"
    lines = [f"# Week of {args.as_of}: {who}", "",
             f"{len(scored)} accounts: {bands['Green']} Green, {bands['Yellow']} Yellow, {bands['Red']} Red, "
             f"{bands['Insufficient data']} Insufficient data. Band drops: {', '.join(drops) or 'none'}.", "",
             "## Do this week", "",
             "1. **Weekly brief.** Run the `cs-weekly-brief` skill on `scored.csv`."]
    step = 2
    if window:
        lines.append(f"{step}. **Renewals.** {len(window)} renewing within 120 days. Run the `cs-pre-renewal-check` skill on "
                     f"`renewal-window.csv`, then the `cs-renewal-prep` skill for each one that needs work: "
                     + ", ".join(r["account"] for r in window) + ".")
        step += 1
    if gaps:
        lines.append(f"{step}. **Adoption plans.** Goals with an adoption gap at {', '.join(gaps)}. "
                     "Run the `cs-adoption-plan` skill with those rows of `outcome-progress.csv`.")
        step += 1
    if no_plan or unbaselined:
        parts = ([f"no success plan: {', '.join(no_plan)}"] if no_plan else []) + \
                ([f"goals with no baseline or gone stale: {', '.join(unbaselined)}"] if unbaselined else [])
        text = "; ".join(parts)
        lines.append(f"{step}. **Success plans.** {text[0].upper()}{text[1:]}. "
                     "Run the `cs-success-plan` skill to draft or repair them.")
        step += 1
    lines.append(f"{step}. **Forecast.** Check `forecast.md`, and update your call for anything under \"Calls to review\".")
    lines += ["", "## Files", "",
              "| File | What it is |", "|---|---|",
              "| `scored.csv` | The book scored with Account Health Scoring, sorted by priority |",
              "| `renewal-window.csv` | Accounts renewing within 120 days, for the Pre-Renewal Check |",
              "| `outcome-progress.csv` | Each success plan goal: progress from baseline, status, and adoption reading |",
              "| `forecast.md` | Renewal forecast by quarter, and calls that disagree with the signals |",
              "| `value-report.md` | Value realized: proven goals and customer-agreed value |",
              "| `inputs/` | The filtered inputs these were built from |"]
    if warnings:
        lines += ["", "## Warnings", ""] + [f"- {w}" for w in warnings]
    (out / "week.md").write_text("\n".join(lines) + "\n")
    print(f"Wrote {out}/: week.md and 5 reports for {who}.", file=sys.stderr)


if __name__ == "__main__":
    main()
