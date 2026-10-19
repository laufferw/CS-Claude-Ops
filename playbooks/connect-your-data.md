# Playbook: Connect Your Data

> Generic pattern. Field names differ in every CRM, and most CS fields are custom. Treat the system notes below as where to look, not exact field names.

## Purpose

Get a team's real account data into the formats the tools read, so scoring, briefs, forecasts, and value reports run on the actual book instead of the sample. Done once to set up, then repeated weekly with the same exports and mapping.

## Trigger

A team decides to use the tools on real accounts, or a source system changes (a new CRM, a renamed field, a new product analytics tool).

## Inputs

- Admin or report-building access to the CRM, product analytics, ticketing, and billing systems
- The target formats in [`sample-data`](../sample-data/README.md): accounts, success plans, and feature adoption
- The example exports and mapping in [`sample-data/exports`](../sample-data/exports/mapping.json)
- One shared account ID that every system can export. Usually the CRM record ID

## Where each field usually lives

| Field | Usual source | HubSpot | Salesforce | Gainsight |
|---|---|---|---|---|
| `account_id`, `account`, `csm` | CRM | Company record ID, name, owner | Account ID, name, owner (or a CSM lookup field) | Company GSID or CRM ID, name, CSM |
| `arr`, `renewal_date` | CRM or billing | Custom company properties, or from the renewal deal | Custom Account fields, or from the renewal Opportunity | Company ARR and renewal date fields |
| `licensed_seats` | Billing or CRM | Custom property or line items | Custom field or contract line items | Company or subscription field |
| `active_users`, `usage_trend_90d_pct` | Product analytics | Synced custom properties, or a separate export | Synced custom fields, or a separate export | Usage data measures |
| `meetings_60d`, `days_since_exec_contact` | CRM activities | Meeting activity report, filtered by contact role | Event or Task report, filtered by contact role | Timeline activities |
| `open_escalations`, `ttr_trend` | Ticketing | Help desk tickets, or a separate export | Cases | Synced from the ticketing system |
| `nps_score`, `csm_confidence` | Surveys, CSM | Survey responses; a custom property for confidence | Survey object; a custom field | Survey responses; a CSM sentiment field |
| `payment_days_late` | Billing | Usually a separate billing export | Usually a separate billing export | Synced from billing |
| `contract_flags`, `red_flags` | CRM | Custom checkbox or count properties | Custom checkbox or count fields | Risk CTAs or custom fields |
| `prior_index` | Last week's run | Last week's `scored-accounts.csv` | Same | Same |
| Success plans | Wherever CSMs keep them | Often a spreadsheet or a custom object | Often a custom object | Success plan objectives |
| Feature adoption | Product analytics | Separate export | Separate export | Feature adoption measures |

If a field exists nowhere, leave it unmapped. Scoring treats it as missing, not as zero, and coverage shows the gap.

## Steps

| Step | Owner | Timing |
|---|---|---|
| 1. Fill in the table above for your systems: where each field lives, or that it doesn't | CS Ops, with RevOps | Day 1 to 2 |
| 2. Build one saved export per system, each including the shared account ID. Note the date each was taken | RevOps or system admins | Week 1 |
| 3. Copy [`sample-data/exports/mapping.json`](../sample-data/exports/mapping.json) and change the source names, key columns, field columns, and formats to match your exports | CS Ops | Week 1 |
| 4. Run [`tools/import_data.py`](../tools/import_data.py) and read the coverage report and errors | CS Ops | Week 1 |
| 5. Fix each error at its source or in the mapping. Decide on each gap: fix the source, or accept it as missing | CS Ops, with RevOps | Week 2 |
| 6. Do the same for success plans and feature adoption, with a mapping whose `target` is `success-plans` or `feature-adoption` | CS Ops | Week 2 |
| 7. Score the book and check it with the people who know it: each CSM picks 5 accounts and says whether the band matches their judgment | CS manager and CSMs | Week 2 |
| 8. Make it weekly: same exports, same mapping, then [`tools/run_week.py`](../tools/run_week.py) for each CSM | CS Ops | Every Monday |

## Mapping file

A mapping is a JSON file with three parts:

- **`target`**: `accounts`, `success-plans`, or `feature-adoption`.
- **`keys`**: each source's name and its account ID column. The first source is the primary: it decides which rows exist. Other sources join to it by key.
- **`fields`**: for each output column, where it comes from. A plain string such as `"crm:Company name"` copies the value. An object converts it:

| `type` | Does | Options |
|---|---|---|
| `text` (default) | Copies the value | `blank`: value to use when empty |
| `number` | Strips `$`, `,`, `%`, and spaces: `"$240,000"` becomes `240000` | `blank` |
| `date` | Converts to YYYY-MM-DD | `format`, such as `%m/%d/%Y`. `blank` |
| `days_since` | Days from a date to `--as-of`, for fields stored as a date | `format`. `blank`, such as `"never"` |
| `map` | Translates values, such as picklist labels | `map`, and an optional `default` |
| `flags` | Builds `red_flags` from yes/no columns | `from`: each flag name and its column |

A field with `"value"` instead of `"from"` gets that fixed value. Columns not mapped are left blank, and the report lists them.

## Decision logic

- **The systems don't share an account ID:** export a crosswalk (CRM ID to product account ID) and add it as a source, or add the CRM ID to the other system. Never join on company name: names drift and collide.
- **A required field (ID, name, ARR, renewal date) is blank for a row:** the row is left out with an error. Fix it in the CRM. An account without a renewal date can't be forecast or prioritized.
- **A value isn't in a map:** the row fails. Add the value to the map. Use `default` only when you have decided what unknown values mean.
- **Coverage under 70% on an important signal:** fix the source before anyone acts on bands. Bands built mostly on missing data read as Insufficient data, as they should.
- **CSMs say the bands are wrong for most of their 5 accounts:** check the mapping for that signal first (a percent stored as a fraction, an inverted trend), then the rubric's weights.

## Outputs

- A mapping file per target, kept with the team's other CS Ops files
- `accounts.csv`, `success-plans.csv`, and `feature-adoption.csv` for the real book
- A list of data gaps, each with an owner or a decision to accept it
- A weekly refresh routine

## Failure modes

- **Joining on names.** "Acme Inc" and "Acme, Inc." become two accounts. Join on IDs.
- **Exports taken on different days.** Usage from last month and CRM from today make a misleading score. Take the exports the same day and use that date as `--as-of`.
- **Silent defaults.** A `default` on a map, or a `blank` on a field, can hide bad data. Use them deliberately and record why in the mapping's comment.
- **Unquoted commas in an export.** A note with a comma in it can shift every column after it. The import stops with the line number when a row has more fields than the header.
- **Mapping drift.** Someone renames a CRM field and the import fails, or worse, maps the wrong column. Rerun the import after any CRM change, and read the coverage report every week, not only the errors.
