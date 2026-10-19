# CLAUDE.md

## Git workflow

Commit and push directly to `main`. Do not create feature branches or pull requests unless asked. This applies even when a session starts on a `claude/...` branch: switch to `main` (`git fetch origin main && git checkout -B main origin/main`), commit there, and `git push origin main`.

## Repo layout

This repo is Outcome-Led CS Ops, an open-source Claude plugin and marketplace (`.claude-plugin/`). Markdown-first. Docs live in `frameworks/`, `specs/`, `prompts/`, and `playbooks/`, with opinion pieces in `essays/` and start-here guides by role in `guides/`. Runnable utilities live in `tools/` (standard-library Python), and fictional data for them in `sample-data/`. See the README for what each holds.

If you change the scoring rubric, update `tools/score_accounts.py` to match and regenerate `sample-data/scored-accounts.csv` (command in `sample-data/README.md`).

When adding, renaming, or moving a doc:
- Start new docs from the matching file in `templates/`.
- For a new prompt, add its skill to `tools/skills.json` (name, title, prompt, description, bundled references, tool commands), run `python3 tools/build_skills.py`, and add it to the README's skills table.
- Add new terms to `glossary.md`.
- Add or update its entry in the README index.
- Link to other docs with relative markdown links.

`skills/` is generated from `tools/skills.json` and the prompts and frameworks it bundles. Never edit it by hand. After changing a prompt or a bundled framework, run `python3 tools/build_skills.py`. To use the skills while working here, start Claude Code with `claude --plugin-dir .`.

For a release, bump `version` in `.claude-plugin/plugin.json`, add a matching section to `CHANGELOG.md`, then push a `v<version>` tag or run the "Release skills" workflow from the Actions tab. The workflow creates the release and attaches one zip per skill.

When you change a prompt, run its evals (`python3 tools/run_evals.py --list` shows the cases; see `evals/README.md`), and update the eval's checks and reference outputs if the correct output changes.

Never commit real customer data. Real exports go in `private/` or outside the repo (see `frameworks/ai-usage-policy.md`).

Before every push, run `python3 tools/check_repo.py` and fix anything it reports. CI runs the same check on `main`.

## Content rules

Follow the README's ground rules: nothing proprietary (placeholder companies, invented numbers), every artifact states its inputs, outputs, and failure modes, and judgment stays with the human.
