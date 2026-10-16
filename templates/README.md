# Templates

Start every new doc from one of these. Each template has the sections the README's ground rules require: inputs, outputs, and failure modes.

| Template | Use for | Goes in |
|---|---|---|
| [`framework.md`](framework.md) | A model or method: how to score, decide, or evaluate something | `frameworks/` |
| [`prompt.md`](prompt.md) | A reusable Claude prompt | `prompts/` |
| [`playbook.md`](playbook.md) | A step-by-step procedure with owners and timings | `playbooks/` |
| [`spec.md`](spec.md) | A design doc for a tool worth building | `specs/` |

To use one:

1. Copy it into the right folder with a lowercase, hyphenated file name.
2. Replace every `{placeholder}` and delete the guidance in `>` quote blocks.
3. Keep every section. If one doesn't apply, write why instead of deleting it.
4. Add the doc to the README index, and link it to and from the docs it depends on.
5. For a new prompt, add a matching skill in `.claude/skills/` (see the existing ones for the pattern).

A doc is finished when a reader can use it without asking its author anything.
