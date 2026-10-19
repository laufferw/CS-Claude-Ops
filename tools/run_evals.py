"""Check prompt outputs against eval cases.

Each file in evals/ holds cases for one prompt: how to build the input, and
checks a correct output must pass (facts it must contain, things it must
not say, order, sections, length). Check one output you got from Claude,
or self-test every case: its good reference output must pass and its bad
one must fail, which proves the checks work. Standard library only.

Usage:
    python3 tools/run_evals.py --list
    python3 tools/run_evals.py evals/weekly-csm-brief.json --case sam --output my-brief.md
    python3 tools/run_evals.py --self-test
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVALS = ROOT / "evals"
HEADING = re.compile(r"^(#{1,6})\s+(.*)$")


def section(text, name):
    """The text under the first heading containing name, up to the next heading at the same level or higher."""
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = HEADING.match(line.strip())
        if m and name.lower() in m.group(2).lower():
            level, body = len(m.group(1)), []
            for nxt in lines[i + 1:]:
                n = HEADING.match(nxt.strip())
                if n and len(n.group(1)) <= level:
                    break
                body.append(nxt)
            return "\n".join(body)
    return None


def run_check(check, text):
    """Return None if the check passes, else a reason."""
    scope = text
    if "section" in check:
        scope = section(text, check["section"])
        if scope is None:
            return f"no heading containing '{check['section']}'"
    low = scope.lower()
    kind = check["type"]
    if kind == "contains":
        missing = [v for v in check["values"] if v.lower() not in low]
        return f"missing: {', '.join(missing)}" if missing else None
    if kind == "not_contains":
        found = [v for v in check["values"] if v.lower() in low]
        return f"should not contain: {', '.join(found)}" if found else None
    if kind == "order":
        positions = [low.find(v.lower()) for v in check["values"]]
        if -1 in positions:
            return f"missing: {', '.join(v for v, p in zip(check['values'], positions) if p == -1)}"
        return None if positions == sorted(positions) else f"not in order: {' > '.join(check['values'])}"
    if kind == "sections":
        missing = [n for n in check["values"] if section(text, n) is None]
        return f"missing sections: {', '.join(missing)}" if missing else None
    if kind == "max_words":
        words = len(re.findall(r"\S+", scope))
        return f"{words} words, limit {check['value']}" if words > check["value"] else None
    return f"unknown check type '{kind}'"


def evaluate(case, text):
    """Return a list of (check, reason) for every failing check."""
    failures = []
    for check in case["checks"]:
        reason = run_check(check, text)
        if reason:
            failures.append((check, reason))
    return failures


def load(path):
    data = json.loads(Path(path).read_text())
    for case in data["cases"]:
        for key in ("name", "input", "checks", "good", "bad"):
            if key not in case:
                raise ValueError(f"{path}: case {case.get('name', '?')} has no '{key}'")
    return data


def describe(check):
    where = f" in '{check['section']}'" if "section" in check else ""
    return f"{check['type']}{where}: {check.get('why', '')}".rstrip(": ")


def self_test():
    problems, count = [], 0
    for path in sorted(EVALS.glob("*.json")):
        data = load(path)
        if not (ROOT / data["prompt"]).exists():
            problems.append(f"{path.name}: prompt {data['prompt']} not found")
        for case in data["cases"]:
            count += 1
            label = f"{path.name} case '{case['name']}'"
            for key in ("good", "bad"):
                if not (ROOT / case[key]).exists():
                    problems.append(f"{label}: {key} output {case[key]} not found")
            if problems:
                continue
            for check, reason in evaluate(case, (ROOT / case["good"]).read_text()):
                problems.append(f"{label}: good output fails {describe(check)} ({reason})")
            if not evaluate(case, (ROOT / case["bad"]).read_text()):
                problems.append(f"{label}: bad output passes every check, so the checks catch nothing")
    return count, problems


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("eval_file", nargs="?")
    parser.add_argument("--case", help="case name (default: the only case)")
    parser.add_argument("--output", help="the output to check")
    parser.add_argument("--list", action="store_true", help="list every case and how to build its input")
    parser.add_argument("--self-test", action="store_true", help="check every case's good and bad outputs")
    args = parser.parse_args()

    if args.self_test:
        count, problems = self_test()
        for p in problems:
            print(f"- {p}")
        print(f"{count} eval cases self-tested: {'all good' if not problems else f'{len(problems)} problem(s)'}.")
        sys.exit(1 if problems else 0)

    if args.list:
        for path in sorted(EVALS.glob("*.json")):
            data = load(path)
            for case in data["cases"]:
                print(f"{path.relative_to(ROOT)} --case {case['name']}  ({data['prompt']})\n  input: {case['input']}")
        return

    if not (args.eval_file and args.output):
        parser.error("give an eval file and --output, or use --list or --self-test")
    data = load(args.eval_file)
    cases = [c for c in data["cases"] if args.case in (None, c["name"])]
    if len(cases) != 1:
        sys.exit(f"pick one case with --case: {', '.join(c['name'] for c in data['cases'])}")
    case = cases[0]
    failures = evaluate(case, Path(args.output).read_text())
    for check, reason in failures:
        print(f"FAIL {describe(check)}: {reason}")
    passed = len(case["checks"]) - len(failures)
    print(f"{passed} of {len(case['checks'])} checks passed for {data['prompt']} case '{case['name']}'.")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
