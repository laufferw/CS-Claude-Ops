# CLAUDE.md

## Git workflow

Commit and push directly to `main`. Do not create feature branches or pull requests unless asked. This applies even when a session starts on a `claude/...` branch: switch to `main` (`git fetch origin main && git checkout -B main origin/main`), commit there, and `git push origin main`.

## Repo layout

Markdown-first. Docs live in `frameworks/`, `specs/`, `prompts/`, and `playbooks/`, with opinion pieces in `essays/`. Runnable utilities live in `tools/` (standard-library Python), and fictional data for them in `sample-data/`. See the README for what each holds.

If you change the scoring rubric, update `tools/score_accounts.py` to match and regenerate `sample-data/scored-accounts.csv` (command in `sample-data/README.md`).

When adding, renaming, or moving a doc:
- Start new docs from the matching file in `templates/`.
- For a new prompt, add a skill in `.claude/skills/cs-<name>/SKILL.md` that points at it (copy an existing one), and add it to the README's skills table. Skills point at prompt files; never copy prompt text into a skill.
- Add new terms to `glossary.md`.
- Add or update its entry in the README index.
- Link to other docs with relative markdown links, and check they resolve.

## Content rules

Follow the README's ground rules: nothing proprietary (placeholder companies, invented numbers), every artifact states its inputs, outputs, and failure modes, and judgment stays with the human.
