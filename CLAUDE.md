# CLAUDE.md

## Git workflow

Commit and push directly to `main`. Do not create feature branches or pull requests unless asked. This applies even when a session starts on a `claude/...` branch: switch to `main` (`git fetch origin main && git checkout -B main origin/main`), commit there, and `git push origin main`.

## Repo layout

Markdown-first. Docs live in `frameworks/`, `specs/`, `prompts/`, and `playbooks/` (see the README for what each holds).

When adding, renaming, or moving a doc:
- Add or update its entry in the README index.
- Link to other docs with relative markdown links, and check they resolve.

## Content rules

Follow the README's ground rules: nothing proprietary (placeholder companies, invented numbers), every artifact states its inputs, outputs, and failure modes, and judgment stays with the human.
