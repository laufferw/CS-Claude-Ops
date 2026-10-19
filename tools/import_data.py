"""Turn raw CRM, product, and support exports into this repo's input formats.

Reads one or more exported CSVs, joins them on the account key, converts
each field as a JSON mapping file says, validates every row with the same
rules the scoring tools use, and writes the result in the sample-data format.
A coverage report on stderr shows how much of each field arrived. The
procedure is in playbooks/connect-your-data.md. Standard library only.

Usage:
    python3 tools/import_data.py sample-data/exports/mapping.json \
        --source crm=sample-data/exports/crm-companies.csv \
        --source usage=sample-data/exports/product-usage.csv \
        --as-of 2026-10-01 > accounts.csv
"""

import argparse
import csv
import json
import re
import sys
from datetime import date, datetime

from outcome_progress import REQUIRED_COLUMNS as PLAN_COLUMNS, goal_status
from score_accounts import ACCOUNT_COLUMNS, score_account

TARGETS = {
    "accounts": {"columns": ACCOUNT_COLUMNS, "required": ["account_id", "account", "arr", "renewal_date"]},
    "success-plans": {"columns": PLAN_COLUMNS + ["annual_value_per_unit"],
                      "required": ["account_id", "outcome_id", "target_value", "target_date"]},
    "feature-adoption": {"columns": ["account_id", "feature", "adoption_pct"],
                         "required": ["account_id", "feature", "adoption_pct"]},
}
TRUE_WORDS = {"yes", "y", "true", "1", "x", "checked"}


class FieldError(ValueError):
    pass


def number(value):
    """'$240,000' -> '240000', '-18%' -> '-18', '' -> ''."""
    text = re.sub(r"[$,%\s]", "", value or "")
    if text == "":
        return ""
    try:
        parsed = float(text)
    except ValueError:
        raise FieldError(f"not a number: {value!r}")
    return str(int(parsed)) if parsed.is_integer() else str(parsed)


def parse_date(value, fmt):
    try:
        return datetime.strptime(value.strip(), fmt).date()
    except ValueError:
        raise FieldError(f"date {value!r} does not match format {fmt}")


def lookup(rows, ref):
    """Read 'source:Column' from the joined row for one account."""
    source, _, column = ref.partition(":")
    if source not in rows:
        raise FieldError(f"unknown source '{source}' in {ref!r}")
    row = rows[source]
    if row is None:
        return ""
    if column not in row:
        raise FieldError(f"column '{column}' not in source '{source}'")
    return (row[column] or "").strip()


def convert(spec, rows, as_of):
    """Apply one field's mapping to one account's joined rows."""
    if isinstance(spec, str):
        spec = {"from": spec}
    kind = spec.get("type", "text")
    if "value" in spec:
        return str(spec["value"])
    if kind == "flags":
        return "|".join(flag for flag, ref in spec["from"].items() if lookup(rows, ref).lower() in TRUE_WORDS)

    raw = lookup(rows, spec["from"])
    if raw == "":
        return str(spec.get("blank", ""))
    if kind == "text":
        return raw
    if kind == "number":
        return number(raw)
    if kind == "date":
        return parse_date(raw, spec.get("format", "%Y-%m-%d")).isoformat()
    if kind == "days_since":
        return str((as_of - parse_date(raw, spec.get("format", "%Y-%m-%d"))).days)
    if kind == "map":
        mapped = spec["map"].get(raw, spec["map"].get(raw.lower()))
        if mapped is None:
            if "default" in spec:
                return str(spec["default"])
            raise FieldError(f"value {raw!r} is not in the map")
        return str(mapped)
    raise FieldError(f"unknown type '{kind}'")


def validate(target, row, as_of):
    """Run the row through the tool that will read it. Return an error message or None."""
    try:
        if target == "accounts":
            date.fromisoformat(row["renewal_date"])
            score_account(row, as_of)
        elif target == "success-plans":
            goal_status(row, as_of)
        elif target == "feature-adoption" and number(row["adoption_pct"]) == "":
            return "adoption_pct is blank"
    except (ValueError, KeyError, ZeroDivisionError) as e:
        return str(e)
    return None


def load_sources(pairs, keys):
    """Read each name=path source into {name: {key value: row}}, keeping the primary's order."""
    sources, order = {}, []
    for pair in pairs:
        name, _, path = pair.partition("=")
        if name not in keys:
            raise ValueError(f"source '{name}' has no key in the mapping (known: {', '.join(keys)})")
        with open(path, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            if keys[name] not in (reader.fieldnames or []):
                raise ValueError(f"{path}: key column '{keys[name]}' not found")
            rows = {}
            for line, row in enumerate(reader, start=2):
                if None in row:
                    raise ValueError(f"{path} line {line}: more fields than the header. Check for an unquoted comma")
                key = (row[keys[name]] or "").strip()
                if key in rows:
                    raise ValueError(f"{path} line {line}: duplicate key {key!r}")
                rows[key] = row
                if name == next(iter(keys)):
                    order.append(key)
        sources[name] = rows
    missing = [name for name in keys if name not in sources]
    if missing:
        raise ValueError(f"no --source given for: {', '.join(missing)}")
    return sources, order


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("mapping_json")
    parser.add_argument("--source", action="append", default=[], metavar="NAME=PATH",
                        help="an export to read; repeat for each source named in the mapping")
    parser.add_argument("--as-of", type=date.fromisoformat, default=date.today(),
                        help="date the export was taken, for days-since fields (YYYY-MM-DD)")
    parser.add_argument("--output", help="file to write (default stdout)")
    args = parser.parse_args()

    with open(args.mapping_json) as f:
        mapping = json.load(f)
    target = mapping.get("target")
    if target not in TARGETS:
        sys.exit(f"{args.mapping_json}: target must be one of {', '.join(TARGETS)}")
    columns, required = TARGETS[target]["columns"], TARGETS[target]["required"]
    fields = mapping.get("fields", {})
    unknown = [c for c in fields if c not in columns]
    if unknown:
        sys.exit(f"{args.mapping_json}: fields not in the {target} format: {', '.join(unknown)}")
    unmapped_required = [c for c in required if c not in fields]
    if unmapped_required:
        sys.exit(f"{args.mapping_json}: required fields not mapped: {', '.join(unmapped_required)}")

    try:
        sources, order = load_sources(args.source, mapping["keys"])
    except (ValueError, OSError) as e:
        sys.exit(str(e))

    primary = next(iter(mapping["keys"]))
    out_rows, errors, unmatched = [], [], {}
    for key in order:
        joined = {}
        for name, rows in sources.items():
            joined[name] = rows.get(key)
            if joined[name] is None:
                unmatched.setdefault(name, []).append(key)
        row, failed = {}, False
        for column in columns:
            if column not in fields:
                row[column] = ""
                continue
            try:
                row[column] = convert(fields[column], joined, args.as_of)
            except FieldError as e:
                errors.append(f"{primary} key {key}: {column}: {e}")
                failed = True
        if failed:
            continue
        blank_required = [c for c in required if row[c] == ""]
        if blank_required:
            errors.append(f"{primary} key {key}: required fields blank: {', '.join(blank_required)}")
            continue
        problem = validate(target, row, args.as_of)
        if problem:
            errors.append(f"{primary} key {key}: {problem}")
            continue
        out_rows.append(row)

    out = open(args.output, "w", newline="") if args.output else sys.stdout
    writer = csv.DictWriter(out, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    writer.writerows(out_rows)
    if args.output:
        out.close()

    report = [f"{len(out_rows)} of {len(order)} rows written to the {target} format."]
    not_mapped = [c for c in columns if c not in fields]
    if not_mapped:
        report.append(f"Not mapped, left blank (scored as missing): {', '.join(not_mapped)}")
    report.append("Coverage (rows with a value):")
    for column in columns:
        filled = sum(1 for r in out_rows if r[column] != "")
        report.append(f"  {column:26} {filled}/{len(out_rows)}")
    for name, keys in unmatched.items():
        report.append(f"warning: {len(keys)} {primary} keys have no row in '{name}': {', '.join(keys)}")
    print("\n".join(report), file=sys.stderr)
    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
