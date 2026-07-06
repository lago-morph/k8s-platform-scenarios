---
name: add-governed-doctype
description: Bring a new canonical document type (findings, scenarios, assumptions, or any future record type) under this repository's JSON governance in one sitting — author its JSON Schema, register it in schemas/map.json, add the semantic checks JSON Schema cannot express to scripts/lint-json, and prove the loop by making the linter catch a deliberate violation before real records land. Use when a session is about to write structured records of a new type into a canonical (non-experiments/) tree and no schema governs them yet, or when a ledger item calls for a new schema (e.g. T-008 findings, T-009 scenarios). Do NOT use for experiments/ records (deliberately loose, well-formedness only) or one-off config files with no record semantics. Companion to the canonical-json-editing skill.
---

# Skill: add-governed-doctype

Extend this repository's canonical-JSON governance to a new document
type in one sitting. The pattern was executed end-to-end for `TODO.json`
— including the linter catching a real violation (unsorted tags) in its
author's own file on its first run — and it recurs for every document
type the roadmap introduces (`findings/`, `scenarios/`, `assumptions/`).

Read the `canonical-json-editing` skill first; this skill produces the
schemas and checks that skill's `scripts/jq-edit` and `scripts/lint-json`
enforce.

## Inputs

- The document type's field list and semantics — from the ledger item's
  summary, the charter's field definitions, or (best) real draft records
  in `experiments/`. Prefer real records: the findings schema is
  explicitly meant to be seeded from depth-probe output (ledger T-008
  depends on T-005) rather than invented.
- Existing conventions to mirror: `schemas/todo.schema.json` as the
  style reference, the `check_todo()` function in `scripts/lint-json`,
  and the `canonical-json-editing` skill.

## Outputs

- `schemas/<doctype>.schema.json` — a JSON Schema (draft 2020-12) in
  canonical form.
- One added pattern→schema entry in `schemas/map.json`.
- A `check_<doctype>()` semantic-check function in `scripts/lint-json`.
- A demonstrated failing lint (deliberate violation) followed by a
  passing full lint, both visible in the transcript / PR.

## Workflow

1. **Draft the schema** with the Write tool, strict by default:
   `additionalProperties: false`, `required` listing every field, enums
   for closed vocabularies, `pattern` for ID fields (e.g.
   `^F-[0-9]{3}$`), `minLength: 1` on prose strings.
2. **Canonicalize immediately**: `scripts/jq-edit schemas/<doctype>.schema.json '.'`
   (the bootstrap rule — Write once, then jq-edit).
3. **Register it**:
   `scripts/jq-edit schemas/map.json '. += [$e] | sort_by(.pattern)' --argjson e '{"pattern":"<glob>","schema":"schemas/<doctype>.schema.json"}'`.
4. **Add semantic checks** to `scripts/lint-json` that a schema cannot
   express — ID uniqueness across files, referential integrity to other
   doctypes, array-ordering rules, status-vocabulary cross-checks. Put
   them in a named `check_<doctype>()` function mirroring `check_todo()`.
5. **Prove the loop**: create a deliberately invalid sample record, run
   `scripts/lint-json`, confirm it fails with the intended message; fix
   the sample via `scripts/jq-edit`; confirm the full lint passes. Do
   not skip this — an unproven linter is prose with extra steps.
6. **Update scope docs**: the `canonical-json-editing` skill's scope
   line and the README contents table, if the doctype introduces a new
   top-level directory.
7. **Commit** the schema, map entry, linter change, and (if useful) the
   sample record; run `scripts/lint-json` as the last pre-commit act.

## Concrete examples

### Example 1: TODO.json (the founding execution)

Schema `schemas/todo.schema.json` (strict items, `^T-[0-9]{3}$` IDs,
phase/status enums); map entry
`{"pattern":"TODO.json","schema":"schemas/todo.schema.json"}`; semantic
checks in `check_todo()` — duplicate IDs, dangling `depends_on`, items
sorted by id, tags/depends_on sorted alphabetically, status within
`conventions.status_values`. The first full run of `scripts/lint-json`
failed with `item tags not sorted alphabetically` — a real violation in
the hand-written original — repaired via
`scripts/jq-edit TODO.json '(.items[].tags) |= sort | (.items[].depends_on) |= sort'`,
after which `lint-json: OK`.

### Example 2: findings/ (the next execution, ledger T-008)

Fields per the charter: scenario id, what was attempted, what the docs
said, what happened, defect-artifact class (enum:
documentation/implementation/requirements/scenario/undetermined),
evidence, run id, lifecycle status. Semantic checks beyond the schema:
finding IDs unique across `findings/*.json`, `scenario_id` matching the
catalog's ID pattern, and (once scenarios exist) referential integrity
to real scenario records. Seed the field shapes from the depth-probe's
draft findings in `experiments/001-s4-depth-probe/` rather than
inventing them.

## Anti-patterns

- **Writing the schema speculatively before real records exist.** The
  roadmap deliberately sequences the findings schema after probe
  triage — schemas informed by real shapes, not speculation.
- **Loose schemas to avoid friction.** `additionalProperties: true`
  hides typos forever; TODO.json's strictness is what makes its lint
  failures meaningful.
- **Skipping the deliberate-violation proof.** A checker that has never
  failed has never been tested.
- **Hand-editing `schemas/map.json`.** It is canonical JSON like
  everything else — extend it through `scripts/jq-edit`.

## Acceptance criteria

- [ ] `scripts/lint-json` fails on a deliberately invalid sample and
      names the violated rule.
- [ ] Full `scripts/lint-json` passes on the real tree afterward.
- [ ] The schema round-trips `jq -S .` byte-identically and validates
      under `scripts/validate-schema.py`.
- [ ] Semantic rules not expressible in JSON Schema exist as a named
      check function, not as prose.

## Files this skill creates / modifies

- `schemas/<doctype>.schema.json` — the new schema.
- `schemas/map.json` — one added pattern→schema entry.
- `scripts/lint-json` — a `check_<doctype>()` semantic-check function.
- `README.md` / `.claude/skills/canonical-json-editing/SKILL.md` — scope
  updates when a new top-level tree appears.

## See also

- `.claude/skills/canonical-json-editing/SKILL.md` — the mutation and
  linting conventions this skill's schemas enforce.
- `retrospective/2026-07-06-2/SKILL-SPEC-e82da89a38-add-governed-doctype.md`
  — the source spec (`SKILL-SPEC-e82da89a38`).
