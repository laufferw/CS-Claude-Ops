"""Build the self-contained Claude skills in skills/ from the prompts.

Each skill in tools/skills.json becomes a folder under skills/: a SKILL.md,
plus references/ holding a copy of its prompt and the frameworks it needs,
with links rewritten so they work inside the folder (or point to GitHub).
The prompts stay the source of truth; skills/ is generated. Each folder
works on its own: installed as part of the Claude Code plugin, or zipped
and uploaded to the Claude apps. Standard library only.

Usage:
    python3 tools/build_skills.py            # rebuild skills/
    python3 tools/build_skills.py --check    # exit 1 if skills/ is out of date
    python3 tools/build_skills.py --zip dist # also write one zip per skill, plus one with all
"""

import argparse
import json
import posixpath
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "tools" / "skills.json"
SKILLS = ROOT / "skills"
REPO_URL = "https://github.com/laufferw/outcome-led-cs-ops"
LINK = re.compile(r"\]\(([^)\s]+)\)")
FENCE = re.compile(r"^```")
ALL_ZIP = "outcome-led-cs-ops-all-skills.zip"

SKILL_TEMPLATE = """---
name: {name}
description: "{description}"
license: MIT
---

# {title}

Part of [Outcome-Led CS Ops]({repo}), built for Claude.

1. Read [references/{prompt_file}](references/{prompt_file}). It is the source of truth for this task. Follow the file, not your memory of it.
1. Check the user has given what its **Inputs** section lists. Ask only for what the prompt cannot work without. Leave smaller gaps to the prompt's own rules for missing data.
1. Carry out the instructions in its **Prompt** section, with the user's material in place of the placeholders.
1. Format the result as its **Output format** section says.
1. Before replying, check the result against its **Known failure modes** and fix anything you find.
{references}{tools}
## Ground rules

- You draft, score, and flag. A person decides on escalations, pricing, and commitments.
- Never send, post, or write anything to a customer or a system of record. Return drafts.
- Use only the material the user gives you, plus the files in this skill.
"""


def rewrite_links(text, source, bundled):
    """Point each relative link at a bundled copy if there is one, otherwise at GitHub."""
    out, inside = [], False
    for line in text.splitlines(keepends=True):
        if FENCE.match(line):
            inside = not inside
        if inside:
            out.append(line)
            continue

        def fix(match):
            target = match.group(1)
            if re.match(r"[a-z]+:", target) or target.startswith("#"):
                return match.group(0)
            path, _, anchor = target.partition("#")
            resolved = posixpath.normpath(posixpath.join(posixpath.dirname(source), path))
            suffix = f"#{anchor}" if anchor else ""
            if resolved in bundled:
                return f"]({posixpath.basename(resolved)}{suffix})"
            kind = "tree" if (ROOT / resolved).is_dir() else "blob"
            return f"]({REPO_URL}/{kind}/main/{resolved}{suffix})"

        out.append(LINK.sub(fix, line))
    return "".join(out)


def render(skill):
    """Return {relative path: text} for one skill folder."""
    sources = [skill["prompt"], *skill["references"]]
    bundled = set(sources)
    files = {}
    for source in sources:
        text = (ROOT / source).read_text()
        files[f"references/{posixpath.basename(source)}"] = rewrite_links(text, source, bundled)

    references = ""
    if skill["references"]:
        references = "\n## Reference docs\n\nRead these when the prompt refers to them:\n\n" + "".join(
            f"- [references/{posixpath.basename(r)}](references/{posixpath.basename(r)})\n" for r in skill["references"])
    tools = ""
    if skill["tools"]:
        commands = "".join(
            f"- To {t['for']}: `python3 \"${{CLAUDE_PLUGIN_ROOT}}/{t['run'].split(' ', 1)[0]}\" {t['run'].split(' ', 1)[1]}`\n"
            for t in skill["tools"])
        tools = ("\n## Building the input\n\nIf the user gives raw account data instead of the input above, and you are "
                 "running in Claude Code with the Outcome-Led CS Ops plugin installed:\n\n" + commands +
                 "\nAsk for the as-of date if it is not clear. Anywhere else, ask the user to paste the input, or to run "
                 f"the tool from the [repository]({REPO_URL}).\n")
    files["SKILL.md"] = SKILL_TEMPLATE.format(
        name=skill["name"], description=skill["description"].replace('"', "'"), title=skill["title"],
        repo=REPO_URL, prompt_file=posixpath.basename(skill["prompt"]), references=references, tools=tools)
    return files


def build(target):
    skills = json.loads(MANIFEST.read_text())
    if target.exists():
        shutil.rmtree(target)
    for skill in skills:
        for rel, text in render(skill).items():
            path = target / skill["name"] / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
    return skills


def snapshot(folder):
    if not folder.exists():
        return {}
    return {p.relative_to(folder).as_posix(): p.read_text() for p in sorted(folder.rglob("*")) if p.is_file()}


def write_zips(skills, dest):
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest / ALL_ZIP, "w", zipfile.ZIP_DEFLATED) as everything:
        for skill in skills:
            folder = SKILLS / skill["name"]
            with zipfile.ZipFile(dest / f"{skill['name']}.zip", "w", zipfile.ZIP_DEFLATED) as one:
                for path in sorted(folder.rglob("*")):
                    if path.is_file():
                        arcname = path.relative_to(SKILLS).as_posix()
                        one.write(path, arcname)
                        everything.write(path, arcname)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="exit 1 if skills/ differs from a fresh build")
    parser.add_argument("--zip", metavar="DIR", help="after building, write one zip per skill and one with all of them")
    args = parser.parse_args()

    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            build(Path(tmp) / "skills")
            fresh, current = snapshot(Path(tmp) / "skills"), snapshot(SKILLS)
        stale = sorted(set(fresh) ^ set(current) | {p for p in fresh if p in current and fresh[p] != current[p]})
        if stale:
            print("skills/ is out of date. Run python3 tools/build_skills.py. Differs: " + ", ".join(stale[:10]))
            sys.exit(1)
        print(f"skills/ is up to date ({len({p.split('/')[0] for p in fresh})} skills).")
        return

    skills = build(SKILLS)
    print(f"Built {len(skills)} skills in skills/.", file=sys.stderr)
    if args.zip:
        write_zips(skills, Path(args.zip))
        print(f"Wrote {len(skills) + 1} zips to {args.zip}/.", file=sys.stderr)


if __name__ == "__main__":
    main()
