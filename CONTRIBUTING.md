# Contributing

Thanks for helping. Outcome-Led CS Ops is built for Claude and for CS teams of any size, so the best contributions make it more useful to a team that isn't yours.

## Good first contributions

- **Outcome Library entries for other kinds of products.** The [library](frameworks/outcome-library.md) is written for a fictional operations and billing platform. Examples for security, HR, developer, marketing, or vertical software help every team that adapts it. An outcome needs a metric, a direction, a data source, the features that move it, and a typical range, and must pass the library's four tests.
- **Field mappings for your CRM.** A [mapping file](playbooks/connect-your-data.md#mapping-file) for a common HubSpot, Salesforce, or Gainsight export, with fictional sample data.
- **Eval cases.** A new case in [`evals/`](evals/README.md) that catches a mistake you've seen a prompt make.
- **Fixes.** A broken link, a confusing step, a number in a doc that doesn't match the tool.

## Ground rules

These come from the [README](README.md#ground-rules) and apply to every change:

1. **Nothing proprietary.** Placeholder companies and invented numbers only. No real customer names, contract terms, pricing, or internal processes from your employer.
2. **Every artifact states its inputs, outputs, and failure modes.** Start new docs from [`templates/`](templates/README.md).
3. **Judgment stays with the human.** Skills draft, score, and flag. People decide on escalations, pricing, and commitments.

## How to make a change

1. Fork the repo and create a branch.
2. Make the change. Tools are standard-library Python 3: nothing to install.
3. If you changed a prompt, or a framework a skill bundles, rebuild the skills: `python3 tools/build_skills.py`. Never edit `skills/` by hand; it is generated.
4. If you changed a prompt, run its [evals](evals/README.md), and update the checks if the correct output changed.
5. If you added a prompt, add its skill to [`tools/skills.json`](tools/skills.json) and to the README's skills table.
6. Run `python3 tools/check_repo.py` and fix anything it reports. CI runs the same check on every pull request.
7. Open a pull request saying what changed and why.

To try your changes as a plugin, run `claude --plugin-dir .` from the repo root, or `claude plugin validate .` to check the manifests.

## Reporting problems

Open an issue with what you tried, what you expected, and what happened. Never paste real customer data into an issue: use the sample data, or describe the shape of the problem.
