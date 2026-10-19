"""Check that the repo is complete and consistent.

Checks:
- Every doc has the sections its folder requires (the README's ground rule:
  inputs, outputs, and failure modes)
- Every relative link, and every #anchor, resolves
- Every doc is listed in the README index
- Every prompt has a skill, every skill points at a prompt that exists, and
  the README's skills table lists every skill
- The tools run, sample-data/scored-accounts.csv matches a fresh run, and importing
  the sample exports reproduces sample-data/accounts.csv
- Every sample CSV row has as many fields as its header
- Every outcome ID in sample-data/success-plans.csv is in the Outcome Library, and every
  feature in sample-data/feature-adoption.csv is named in it

Exits non-zero and lists every problem if anything fails. Standard library only.

Usage:
    python3 tools/check_repo.py
"""

import csv
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Section headings each kind of doc must have. A required name matches any
# "## " heading that starts with it, so "Prompt" matches "Prompt: open an escalation".
REQUIRED_SECTIONS = {
    "frameworks": ["Purpose", "Inputs", "Outputs", "Failure modes"],
    "prompts": ["Purpose", "Inputs", "Prompt", "Output format", "Known failure modes"],
    "playbooks": ["Purpose", "Trigger", "Inputs", "Steps", "Outputs", "Failure modes"],
    "specs": ["Goals", "Non-goals", "Inputs", "Outputs", "Safety and trust", "Failure modes"],
    "guides": ["Who it's for", "What you need", "Your week", "What you get", "Start here", "Failure modes"],
}
INDEXED_FOLDERS = ["guides", "frameworks", "specs", "prompts", "playbooks", "essays"]
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
FENCE = re.compile(r"^```")


def markdown_files():
    skip = {".git"}
    return sorted(p for p in ROOT.rglob("*.md") if not skip & set(p.relative_to(ROOT).parts))


def strip_code(text):
    """Drop fenced code blocks, so example text inside them is not checked."""
    lines, inside = [], False
    for line in text.splitlines():
        if FENCE.match(line):
            inside = not inside
            continue
        if not inside:
            lines.append(line)
    return "\n".join(lines)


def headings(text):
    return [line.lstrip("#").strip() for line in strip_code(text).splitlines() if re.match(r"#{1,6} ", line)]


def slug(heading):
    """GitHub's anchor for a heading."""
    text = re.sub(r"[^\w\- ]", "", heading.lower())
    return text.replace(" ", "-")


def check_sections(problems):
    for folder, required in REQUIRED_SECTIONS.items():
        for path in sorted((ROOT / folder).glob("*.md")):
            if path.name == "README.md":
                continue
            found = [line[3:].strip() for line in strip_code(path.read_text()).splitlines()
                     if line.startswith("## ")]
            for name in required:
                if not any(h.startswith(name) for h in found):
                    problems.append(f"{path.relative_to(ROOT)}: missing section '## {name}'")


def check_links(problems):
    anchors = {}
    for path in markdown_files():
        text = strip_code(path.read_text())
        for target in LINK.findall(text):
            if re.match(r"[a-z]+:", target):
                continue
            file_part, _, anchor = target.partition("#")
            dest = (path.parent / file_part).resolve() if file_part else path
            where = f"{path.relative_to(ROOT)} -> {target}"
            if not dest.exists():
                problems.append(f"{where}: file not found")
                continue
            if anchor:
                if dest not in anchors:
                    anchors[dest] = {slug(h) for h in headings(dest.read_text())}
                if anchor not in anchors[dest]:
                    problems.append(f"{where}: no heading with anchor '#{anchor}'")


def check_index(problems):
    readme = (ROOT / "README.md").read_text()
    linked = set(LINK.findall(readme))
    for folder in INDEXED_FOLDERS:
        for path in sorted((ROOT / folder).glob("*.md")):
            if path.name == "README.md":
                continue
            rel = path.relative_to(ROOT).as_posix()
            if rel not in linked:
                problems.append(f"README.md: index does not link to {rel}")


def check_skills(problems):
    readme = (ROOT / "README.md").read_text()
    pointed_at = {}
    for skill in sorted((ROOT / ".claude" / "skills").glob("*/SKILL.md")):
        name = skill.parent.name
        text = skill.read_text()
        front = re.match(r"---\n(.*?)\n---\n", text, re.S)
        if not front or f"name: {name}\n" not in front.group(1) + "\n":
            problems.append(f"{skill.relative_to(ROOT)}: frontmatter name must be '{name}'")
        if front and not re.search(r'^description: ".+"$', front.group(1), re.M):
            problems.append(f"{skill.relative_to(ROOT)}: description must be a quoted string")
        prompts = re.findall(r"`(prompts/[\w-]+\.md)`", text)
        if len(prompts) != 1:
            problems.append(f"{skill.relative_to(ROOT)}: must point at exactly one prompt file")
        for prompt in prompts:
            if not (ROOT / prompt).exists():
                problems.append(f"{skill.relative_to(ROOT)}: {prompt} does not exist")
            pointed_at.setdefault(prompt, []).append(name)
        if f"`{name}`" not in readme:
            problems.append(f"README.md: skills table does not list {name}")
    for path in sorted((ROOT / "prompts").glob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        count = len(pointed_at.get(rel, []))
        if count != 1:
            problems.append(f"{rel}: has {count} skills pointing at it, expected 1")


def run(args):
    return subprocess.run([sys.executable, *args], cwd=ROOT, capture_output=True, text=True)


def check_tools(problems):
    plans = ["--plans", "sample-data/success-plans.csv", "--as-of", "2026-10-01"]
    scored = run(["tools/score_accounts.py", "sample-data/accounts.csv", *plans])
    if scored.returncode != 0:
        problems.append(f"tools/score_accounts.py failed: {scored.stderr.strip()}")
    elif scored.stdout != (ROOT / "sample-data" / "scored-accounts.csv").read_text():
        problems.append("sample-data/scored-accounts.csv is stale: regenerate it (see sample-data/README.md)")
    window = run(["tools/renewal_window.py", "sample-data/accounts.csv", *plans])
    if window.returncode != 0:
        problems.append(f"tools/renewal_window.py failed: {window.stderr.strip()}")
    adoption = ["--adoption", "sample-data/feature-adoption.csv"]
    progress = run(["tools/outcome_progress.py", "sample-data/success-plans.csv", *adoption, "--as-of", "2026-10-01"])
    if progress.returncode != 0:
        problems.append(f"tools/outcome_progress.py failed: {progress.stderr.strip()}")
    report = run(["tools/value_report.py", "sample-data/accounts.csv", *plans, *adoption])
    if report.returncode != 0:
        problems.append(f"tools/value_report.py failed: {report.stderr.strip()}")
    exports = "sample-data/exports"
    imported = run(["tools/import_data.py", f"{exports}/mapping.json", "--source", f"crm={exports}/crm-companies.csv",
                    "--source", f"usage={exports}/product-usage.csv", "--source", f"support={exports}/support-orgs.csv",
                    "--as-of", "2026-10-01"])
    if imported.returncode != 0:
        problems.append(f"tools/import_data.py failed: {imported.stderr.strip()}")
    elif imported.stdout != (ROOT / "sample-data" / "accounts.csv").read_text():
        problems.append("tools/import_data.py: importing sample-data/exports no longer reproduces sample-data/accounts.csv")
    calls = ["--calls", "sample-data/forecast-calls.csv"]
    capacity = ["--capacity", "sample-data/capacity-inputs.json"]
    for args in (["tools/renewal_forecast.py", "sample-data/accounts.csv", *plans, *calls],
                 ["tools/team_rollup.py", "sample-data/accounts.csv", *plans, *adoption, *capacity],
                 ["tools/cs_scorecard.py", "sample-data/accounts.csv", *plans, *adoption, *calls, *capacity,
                  "--history", "sample-data/renewal-history.csv"]):
        result = run(args)
        if result.returncode != 0:
            problems.append(f"{args[0]} failed: {result.stderr.strip()}")
    with tempfile.TemporaryDirectory() as out:
        week = run(["tools/run_week.py", "sample-data/accounts.csv", *plans, *adoption, *calls,
                    "--csm", "Sam Example", "--out", out])
        if week.returncode != 0 or not (Path(out) / "week.md").exists():
            problems.append(f"tools/run_week.py failed: {week.stderr.strip()}")
    roi = run(["tools/roi_calculator.py", "sample-data/roi-inputs.json"])
    if roi.returncode != 0:
        problems.append(f"tools/roi_calculator.py failed: {roi.stderr.strip()}")


def check_csv_widths(problems):
    for path in sorted((ROOT / "sample-data").rglob("*.csv")):
        with open(path, newline="") as f:
            rows = list(csv.reader(f))
        for line, row in enumerate(rows[1:], start=2):
            if len(row) != len(rows[0]):
                problems.append(f"{path.relative_to(ROOT)} line {line}: {len(row)} fields, header has {len(rows[0])}")


def check_outcome_ids(problems):
    sys.path.insert(0, str(ROOT / "tools"))
    from outcome_progress import load_library
    outcomes = load_library(ROOT / "frameworks" / "outcome-library.md")
    library = set(outcomes)
    features = {f for o in outcomes.values() for f in o["features"]}
    with open(ROOT / "sample-data" / "feature-adoption.csv", newline="") as f:
        for line, row in enumerate(csv.DictReader(f), start=2):
            if row["feature"].strip().lower() not in features:
                problems.append(f"sample-data/feature-adoption.csv line {line}: "
                                f"feature '{row['feature']}' is not in the library's Depends on column")
    with open(ROOT / "sample-data" / "success-plans.csv", newline="") as f:
        for line, row in enumerate(csv.DictReader(f), start=2):
            if row["outcome_id"] != "custom" and row["outcome_id"] not in library:
                problems.append(f"sample-data/success-plans.csv line {line}: "
                                f"outcome {row['outcome_id']} is not in frameworks/outcome-library.md")


def main():
    problems = []
    for check in (check_sections, check_links, check_index, check_skills, check_tools, check_outcome_ids, check_csv_widths):
        check(problems)
    if problems:
        print(f"{len(problems)} problem(s):")
        for problem in problems:
            print(f"- {problem}")
        sys.exit(1)
    print("All checks passed.")


if __name__ == "__main__":
    main()
