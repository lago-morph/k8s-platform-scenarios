# Spec: `add-governed-doctype`

- **ID**: SKILL-SPEC-e82da89a38
- **Source retrospective**: ../2026-07-06-2.md

## Intent

Extend this repository's canonical-JSON governance to a new document type (findings, scenarios, assumptions) in one sitting: author the JSON Schema, register it in schemas/map.json via scripts/jq-edit, add the semantic checks JSON Schema cannot express to scripts/lint-json, and prove the loop by showing the linter catching a deliberate violation before real records land. It earns its place because the pattern was executed end-to-end for TODO.json this session - including the linter catching a real violation (unsorted tags) in its author's own file on its first run - and the same steps recur for every document type phase B introduces.

## Trigger

- Direct: "add the findings schema" (ledger T-008), "create the scenario schema" (T-009), "make <doctype> a governed document".
- Proactive: when a session is about to write structured records of a new type into a canonical (non-experiments/) tree and no schema governs them yet.
- Negative: NOT for experiments/ records (deliberately loose, well-formedness only); NOT for one-off config files with no record semantics.

## Inputs

- The document type's field list and semantics (from the ledger item's summary, the charter's field definitions, or real draft records in experiments/ — prefer real records; the findings schema is explicitly supposed to be seeded from depth-probe output, per T-008's dependency on T-005).
- Existing conventions: `schemas/todo.schema.json` as the style reference, `scripts/lint-json` structure, the `canonical-json-editing` skill.

## Outputs

- `schemas/<doctype>.schema.json` (JSON Schema draft 2020-12, canonical form).
- A new pattern→schema entry in `schemas/map.json`.
- A semantic-checks section for the doctype in `scripts/lint-json`.
- A demonstrated failing lint (deliberate violation) and a passing full lint, both shown in the transcript/PR.

## Workflow

1. Draft the schema with Write, strict by default: `additionalProperties: false`, `required` listing every field, enums for closed vocabularies, `pattern` for ID fields (e.g. `^F-[0-9]{3}$`), `minLength: 1` on prose strings.
2. Immediately canonicalize: `scripts/jq-edit schemas/<doctype>.schema.json '.'` (the bootstrap rule).
3. Register it: `scripts/jq-edit schemas/map.json '. += [$e] | sort_by(.pattern)' --argjson e '{"pattern":"<glob>","schema":"schemas/<doctype>.schema.json"}'`.
4. Add semantic checks to `scripts/lint-json` that the schema cannot express — uniqueness of IDs across files, referential integrity to other doctypes, array-ordering rules, status-vocabulary cross-checks. Put them in a named `check_<doctype>()` function mirroring `check_todo()`.
5. Prove the loop: create a deliberately invalid sample record, run `scripts/lint-json`, and confirm it fails with the intended message; fix the sample via `scripts/jq-edit`; confirm the full lint passes. Do not skip this — an unproven linter is prose with extra steps.
6. Update the `canonical-json-editing` skill's scope line and README contents table if the doctype introduces a new top-level directory.
7. Commit with the schema, map entry, linter change, and (if useful) the sample record; run `scripts/lint-json` as the last pre-commit act.

## Concrete examples

### Example 1: TODO.json (the founding execution)

Schema `schemas/todo.schema.json` (strict items, `^T-[0-9]{3}$` IDs, phase/status enums); map entry `{"pattern":"TODO.json","schema":"schemas/todo.schema.json"}`; semantic checks in `check_todo()` — duplicate IDs, dangling `depends_on`, items sorted by id, tags/depends_on sorted alphabetically, status within `conventions.status_values`. First full run of `scripts/lint-json` failed with `item tags not sorted alphabetically` — a real violation in the hand-written original — repaired via `scripts/jq-edit TODO.json '(.items[].tags) |= sort | (.items[].depends_on) |= sort'`, after which `lint-json: OK (3 file(s))`. Commit 6c2228a.

### Example 2: findings/ (the next execution, T-008)

Fields per the charter: scenario id, what was attempted, what the docs said, what happened, defect artifact class (enum: documentation/implementation/requirements/scenario/undetermined), evidence, run id, lifecycle status. Semantic checks beyond the schema: finding IDs unique across `findings/*.json`, `scenario_id` matching the catalog's ID pattern, and (once scenarios exist) referential integrity to real scenario records. Seed the field shapes from the depth-probe's draft findings in `experiments/001-s4-depth-probe/` rather than inventing them — T-008 depends on T-005 for exactly this reason.

## Anti-patterns

- **Writing the schema speculatively before real records exist.** The ledger deliberately sequences findings-schema after probe-triage; honor that (owner: schemas informed by "real shapes instead of speculation").
- **Loose schemas to avoid friction.** `additionalProperties: true` hides typos forever; TODO.json's strictness is what makes its lint failures meaningful.
- **Skipping the deliberate-violation proof.** The TODO.json linter earned trust by catching a real bug on first run; a checker that has never failed has never been tested.
- **Hand-editing schemas/map.json.** It is canonical JSON like everything else — the session's own map entry went in via Write only because the file was born then; extensions go through jq-edit.

## Acceptance criteria

- [ ] `scripts/lint-json` fails on a deliberately invalid sample and names the violated rule.
- [ ] Full `scripts/lint-json` passes on the real tree afterward.
- [ ] The schema round-trips `jq -S .` byte-identically and validates under `scripts/validate-schema.py`.
- [ ] Semantic rules not expressible in JSON Schema exist as a named check function, not as prose.

## Files this skill creates / modifies

- `schemas/<doctype>.schema.json` — the new schema.
- `schemas/map.json` — one added pattern→schema entry.
- `scripts/lint-json` — a `check_<doctype>()` semantic-check function.
- `README.md` / `.claude/skills/canonical-json-editing/SKILL.md` — scope updates when a new top-level tree appears.
