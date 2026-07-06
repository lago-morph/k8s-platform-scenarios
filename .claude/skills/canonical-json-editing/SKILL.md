---
name: canonical-json-editing
description: How to read, create, and above all MODIFY the canonical JSON documents in this repository (TODO.json today; findings/, scenarios/, assumptions/ records as they appear). Use whenever a task involves editing any .json file in this repo — updating the todo ledger, marking an item done, adding a todo item, recording a finding, changing a scenario status, adding a schema, or fixing a lint-json failure. Core rules — mutate only through scripts/jq-edit (never the Edit/Write tools, never sed/awk, never a text editor), keep every document in canonical form (jq -S round-trips to a no-op), run scripts/lint-json before committing so errors surface locally instead of in CI, and sort sub-elements alphabetically wherever order is not semantic. Triggers on phrases like "update the todo", "mark T-NNN done", "add a finding", "edit the JSON", "canonicalize", "lint failure in lint-json".
---

# Skill: canonical-json-editing

Canonical JSON documents are this repository's machine-owned records
(the todo ledger, and soon findings, scenarios, and assumptions).
Humans and agents read them freely; **mutation goes through one path**
so the documents stay well-formed, diffs stay logical, and linters
stay simple.

## The rules

1. **Never text-edit a canonical JSON document.** Do not use the
   Edit or Write tools, sed, awk, or any string-level manipulation on
   an existing `.json` file. Text edits produce trailing commas,
   duplicate keys, broken quoting, and diffs that lie.
2. **All mutations go through `scripts/jq-edit`.** It applies your jq
   filter, rewrites the file atomically in canonical form, and lints
   the result — one command, no partial states:

   ```
   scripts/jq-edit FILE FILTER [JQ_ARGS...]
   ```
3. **Canonical form** is `jq -S .` output: keys sorted alphabetically,
   2-space indent, trailing newline, UTF-8. Re-running `jq -S .` on a
   canonical file is byte-identical (this is linted).
4. **Sort sub-elements alphabetically wherever order is not
   semantic.** In `TODO.json`: `items` sorted by `id`, and each item's
   `tags` and `depends_on` sorted alphabetically (all linted). Where
   order *is* semantic (e.g. prose steps in a future scenario record),
   the document's schema/checks say so explicitly.
5. **Run `scripts/lint-json` before committing.** It checks
   well-formedness, canonical form, JSON Schema conformance (per
   `schemas/map.json`), and per-document semantic rules. Do not wait
   for CI to find what a local command reports in a second.
   `scripts/jq-edit` already lints the file it touched; run the
   full linter before a commit that touched several files.
6. **Fix lint failures with jq, not by hand.** A canonical-form
   failure is fixed by `scripts/jq-edit FILE '.'`; a semantic failure
   (unsorted tags, dangling depends_on) is fixed by a filter that
   repairs the data.

## Creating a new document

Initial creation is the one place the Write tool is acceptable —
there is nothing to mutate yet. Immediately after creating:

```
scripts/jq-edit NEW_FILE '.'     # canonicalize + lint the new file
```

If the new file is an instance of a governed document type, confirm a
`schemas/map.json` entry covers it (add the schema and the map entry —
the map is itself canonical JSON, so extend it with `scripts/jq-edit`).

## Recipes

Mark a todo item done:

```
scripts/jq-edit TODO.json '(.items[] | select(.id=="T-007") | .status) = "done"'
```

Add a todo item (append; the linter enforces id-sorted order, so add
in order or re-sort in the same filter):

```
scripts/jq-edit TODO.json '.items += [$item] | .items |= sort_by(.id)' \
  --argjson item '{
    "depends_on": [],
    "id": "T-031",
    "order": 8,
    "phase": "D",
    "status": "pending",
    "summary": "…",
    "tags": ["process"],
    "title": "…"
  }'
```

Edit one field of one item:

```
scripts/jq-edit TODO.json '(.items[] | select(.id=="T-004") | .summary) = "…new text…"'
```

Sort every item's tags and depends_on (repair after a violation):

```
scripts/jq-edit TODO.json '(.items[].tags) |= sort | (.items[].depends_on) |= sort'
```

Bump the updated stamp:

```
scripts/jq-edit TODO.json '.updated = $d' --arg d "$(date -u +%F)"
```

(Argument order matters: `FILE FILTER [JQ_ARGS...]` — the filter always
comes second; `--arg`/`--argjson` and friends come after it.)

Read without mutating — plain `jq` is always fine:

```
jq -r '.items[] | select(.status=="pending") | "\(.id) \(.title)"' TODO.json
```

## Tooling and dependencies

- `scripts/jq-edit` — the mutation path (jq filter → canonical form →
  atomic replace → lint).
- `scripts/lint-json` — the deterministic linter; also run standalone
  before commits. Exit 0 clean, 1 violations.
- `scripts/validate-schema.py` — JSON Schema (draft 2020-12) checker
  used by the linter. Requires python3 with the `jsonschema` package
  (`pip install jsonschema`); it fails loudly, with exit 2, if the
  package is missing.
- `schemas/map.json` — glob-pattern → schema mapping that tells the
  linter which schema governs which documents.

## Why this exists

These conventions are the repo owner's requirements: rules that
matter must be deterministic and enforced by machines, JSON canonical
form makes diffs logical and linters complete, and local lint feedback
must not wait for CI. This skill is the executable form of those
conventions until hooks (todo T-014) and CI (todo T-013) enforce them
structurally; the todo ledger tracks that hardening.
