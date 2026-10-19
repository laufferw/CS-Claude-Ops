# Changelog

Versions follow the `version` in [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json). Each release's skills are attached to its [GitHub release](https://github.com/laufferw/outcome-led-cs-ops/releases) as zips.

## 0.1.0

The first public release, as Outcome-Led CS Ops.

- **16 Claude skills**, packaged as a Claude Code plugin and as self-contained folders you can zip and upload to the Claude apps: weekly brief, account review, churn triage, renewal prep, pre-renewal check, redline summary, handoff packet, escalation summary, customer email, QBR outline, account update, success plan builder, adoption plan, value narrative, team brief, and competency evaluation.
- **Outcome measurement:** the Outcome Library, success plans with baselines, computed goal statuses, and the adoption check (Proven, Unexplained progress, Adoption gap, Not converting).
- **Health scoring** with outcomes weighted equal to usage, and a cap at Yellow when no outcomes are measured.
- **Leadership tools:** renewal forecast with CSM calls checked against signals, capacity model, team rollup, and the CS metrics scorecard.
- **Calibration:** back-tests for the health score and the forecast, and evals for four prompts.
- **Getting real data in:** a mapping-based importer for CRM, product, and support exports.
- **Governance:** a CS charter with an ownership map, and an AI usage policy.
- **Docs:** guides by role, playbooks across the customer lifecycle, essays, and a glossary. All sample data is fictional.
