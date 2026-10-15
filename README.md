# CS-Claude-Ops

Claude-powered Customer Success Operations: frameworks, specs, prompts, and playbooks for running a CS org with an AI copilot.

This repo is markdown-first. Almost everything here is a document you can read, copy into Claude, or adapt, not code you have to run.

## What's inside

| Folder | What it holds |
|---|---|
| `frameworks/` | The models: CSM competencies, account health scoring, escalation logic, the account management engine |
| `specs/` | Design docs for tools worth building: the CSM Copilot and a HubSpot agent interface |
| `prompts/` | Reusable Claude prompts, each with inputs, output format, and known failure modes |
| `playbooks/` | Step-by-step operating procedures with decision logic |
| `tools/` | Small utilities (for example, an ROI calculator) with sample data only |
| `essays/` | Opinionated writing on RevOps and CS Ops as disciplines |

## Ground rules

1. **Nothing proprietary.** Examples use placeholder companies and invented numbers. No customer names, contract terms, or internal pricing.
2. **Every artifact states its inputs, outputs, and failure modes.** A prompt or framework without these is not finished.
3. **Judgment stays with the human.** Claude drafts, scores, and flags. A person decides on escalations, pricing, and commitments.

## How to use

- Start with `frameworks/account-health-scoring.md` to see how scoring works.
- Pair it with `prompts/account-review.md` to run a review with Claude.
- Read `specs/csm-copilot-spec.md` for where this is headed.

## Status

Early drafts. Weights, thresholds, and rubrics are starting points to calibrate against your own data.
