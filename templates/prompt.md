# Prompt: {Name}

## Purpose

{One sentence: what this produces and for whom.}

## Inputs

> Everything to paste in. Link to the framework or tool that produces each input, if there is one.

- {input}

## Prompt

> Write instructions as you would brief a capable new analyst. Every prompt has a Rules block that covers: use only the data given; how to mark missing or uncertain information; and what Claude must not decide (pricing, commitments, legal positions).

```
You are {role}. Using only the {data} below, {task}.

Produce:
1. {section}
2. {section}

Rules:
- Use only the information provided. If something is missing, write "unknown" rather than guessing.
- {what it must not do or decide}

{DATA}:
{paste here}
```

## Output format

{Sections, lists, or tables, and any length limit.}

## Example

> Optional, but recommended when the prompt applies rules to data: what a correct output contains for the [sample data](../sample-data/README.md).

## Known failure modes

> What the output gets wrong in practice, which rule reduces it, and what the reviewer should still check.

- {failure mode}
