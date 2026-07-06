# ADR: Canonical JSON documents are mutated only through jq-edit

- **ID**: ADR-f68da1c75c
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-07-06
- **Source retrospective**: ../2026-07-06-2.md
- **PRs covered**: #2

## Context

The repository owner's founding requirement for this repo's data layer: rules that matter must be deterministic, "linters like having more structured document formats," and canonical records should be "JSON, only edited using jq or equivalent, never with a text editor." The requirement was validated within the hour it was implemented: the first hand-authored TODO.json violated its own sorting convention (caught by the new linter's first full run), and the author of the mutation wrapper then violated its argument order on his own next call. Text-editing structured data fails even when the editor wrote the rules that morning.

## Decision

All canonical records in this repository are stored as JSON in jq -S canonical form (sorted keys, 2-space indent, trailing newline) and are mutated exclusively through scripts/jq-edit, which applies a jq filter, rewrites the file atomically in canonical form, and lints the result.

Supporting detail: `scripts/lint-json` enforces well-formedness, canonical-form round-trip (`jq -S .` must be byte-identical), JSON Schema conformance per `schemas/map.json`, and per-document semantic checks (referential integrity, array ordering). Initial file creation is the one sanctioned exception (there is nothing to mutate yet): Write once, then immediately `scripts/jq-edit FILE '.'`. The `canonical-json-editing` skill carries the conventions and recipes for future sessions.

## Alternatives considered

- **Markdown with structured frontmatter as the canonical format** — rejected by the owner directly: "Markdown is bad for trying to make simple and complete linters." Markdown remains the rendering target for humans, never the machine-owned record.
- **YAML instead of JSON** — friendlier multi-line prose, but weaker deterministic tooling (parse footguns, multiple string syntaxes) and no jq-grade standard mutation tool; the owner named JSON+jq explicitly.
- **Free editing plus CI-only validation** — rejected because errors would surface minutes-to-hours after the mistake, in CI, instead of in the same tool call; the wrapper gives atomicity (a failed filter leaves the file untouched) that after-the-fact validation cannot.

## Consequences

Easier: logical diffs (formatting noise is impossible), simple and complete linters, safe concurrent-ish editing (atomic replace), and a uniform recipe book any session can follow. Harder: multi-line prose inside JSON strings is clumsy to author; every mutation requires composing a jq filter (a real skill floor); initial creation needs the bootstrap exception. Accepted trade-off: authoring friction in exchange for records that machines can trust without human vigilance. Structural enforcement (deny Edit/Write on canonical paths; CI gate) is deliberately deferred to ledger items T-014/T-013 until schemas stabilize.

## References

- [`../2026-07-06-2.md`](../2026-07-06-2.md) — the source retrospective.
- [`./SKILL-SPEC-e82da89a38-add-governed-doctype.md`](./SKILL-SPEC-e82da89a38-add-governed-doctype.md) — extending governance to new document types.
- PRs the decision was made in: #2 (commit 6c2228a and the design discussion preceding it).
