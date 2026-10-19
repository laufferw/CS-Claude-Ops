# Evals

Test cases for the prompts, so that editing a prompt can't quietly break what it produces. Each JSON file holds cases for one prompt: how to build the input from the sample data, and checks a correct output must pass.

| Eval | Prompt | What the case tests |
|---|---|---|
| [`weekly-csm-brief.json`](weekly-csm-brief.json) | [Weekly CSM Brief](../prompts/weekly-csm-brief.md) | Sam Example's book: the 5-account selection order, renewals soonest first, an empty expansion section, data gaps, and only Sam's accounts |
| [`pre-renewal-check.json`](pre-renewal-check.json) | [Pre-Renewal Check](../prompts/pre-renewal-check.md) | The five renewals: order, the ARR summary by status, and escalation for Red |
| [`value-narrative.json`](value-narrative.json) | [Value Narrative](../prompts/value-narrative.md) | The board version: headline numbers, agreed value not called revenue, unproven results not claimed, what isn't working stated |
| [`team-brief.json`](team-brief.json) | [Team Brief](../prompts/team-brief.md) | The sample team: forecast numbers, calls to challenge by ARR, capacity, and no judgments of people |

## Check types

| Type | Passes when |
|---|---|
| `contains` | Every value appears (case doesn't matter) |
| `not_contains` | No value appears |
| `order` | Every value appears, in the order given |
| `sections` | A markdown heading containing each value exists |
| `max_words` | The output, or the section, is within the word limit |

Any check can add `"section"`: it then applies only to the text under the first heading containing that name, up to the next heading at the same level or higher. Each check also carries a `"why"` that is printed when it fails.

## Running an eval

1. List the cases and how to build each input: `python3 tools/run_evals.py --list`
2. Build the input, run the prompt in Claude (or ask Claude Code, for example "run the weekly brief for Sam Example as of 2026-10-01"), and save the output to a file outside the repo, or under `out/`, which git ignores.
3. Check it: `python3 tools/run_evals.py evals/weekly-csm-brief.json --case sam --output out/brief.md`

Run the evals for a prompt every time you change it, and before trusting a new model with it. One failing run can be noise. The same check failing twice is a regression.

## Self-test

Each case has a good reference output, which must pass every check, and a bad one, which must fail at least one. The reference outputs are in [`outputs/`](outputs/). `python3 tools/run_evals.py --self-test` tests both for every case, and the [repo checker](../tools/README.md#repo-checker) runs it in CI. It proves the checks are satisfiable and that they catch something. It does not run Claude: CI has no model access, so checking real output is a step a person runs.

## Adding a case

- Add it to the prompt's JSON file, or create one with `prompt` and `cases`.
- Write checks for facts the sample data fixes (names, numbers, order), and for the prompt's rules (what it must never say, its length limit). Avoid checks on wording: two good outputs can phrase things differently.
- Write a good output that passes and a bad one that makes a realistic mistake, and run the self-test.

## Failure modes

- **Checks on phrasing.** They fail good outputs that word things differently. Check facts and rules, not sentences.
- **Checks too loose to fail.** The self-test's bad output catches a check that can never fail, but only for the mistake that output makes. Make bad outputs realistic.
- **Section checks on outputs without headings.** A missing heading fails the check. Every prompt evaluated here asks for headed sections, except the pre-renewal check, whose case doesn't use section checks.
- **Treating a pass as proof of quality.** The checks catch known failures. A person still reads the output.
