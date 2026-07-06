# ADR 0001: Canonical JSON documents are mutated only through jq-edit

- **Status**: Accepted
- **Date**: 2026-07-06
- **Deciders**: repo owner
- **ID**: ADR-f68da1c75c

## Context

The repository owner's founding requirement for the data layer: rules that matter must be deterministic, "linters like having more structured document formats," and canonical records should be "JSON, only edited using jq or equivalent, never with a text editor." The requirement was validated within the hour it was implemented: the first hand-authored `TODO.json` violated its own sorting convention (caught by the new linter's first full run), and the author of the mutation wrapper then violated its argument order on his own next call. Text-editing structured data fails even when the editor wrote the rules that morning.

## Decision

All canonical records in this repository are stored as JSON in `jq -S` canonical form (sorted keys, 2-space indent, trailing newline) and are mutated exclusively through `scripts/jq-edit`, which applies a jq filter, rewrites the file atomically in canonical form, and lints the result.

Initial file creation is the one sanctioned exception (there is nothing to mutate yet): Write once, then immediately `scripts/jq-edit FILE '.'`. The `canonical-json-editing` skill carries the conventions and recipes for future sessions.

## Alternatives considered

- **Markdown with structured frontmatter as the canonical format** — rejected by the owner directly: "Markdown is bad for trying to make simple and complete linters." Markdown remains the rendering target for humans, never the machine-owned record.
- **YAML instead of JSON** — friendlier multi-line prose, but weaker deterministic tooling (parse footguns, multiple string syntaxes) and no jq-grade standard mutation tool; the owner named JSON+jq explicitly.
- **Free editing plus CI-only validation** — rejected because errors would surface minutes-to-hours after the mistake, in CI, instead of in the same tool call; the wrapper gives atomicity (a failed filter leaves the file untouched) that after-the-fact validation cannot.

## Consequences

Easier: logical diffs (formatting noise is impossible), simple and complete linters, safe editing (atomic replace), and a uniform recipe book any session can follow. Harder: multi-line prose inside JSON strings is clumsy to author; every mutation requires composing a jq filter (a real skill floor); initial creation needs the bootstrap exception.

Enforcement is what makes this decision binding rather than aspirational: `scripts/lint-json` checks well-formedness, canonical-form round-trip, JSON Schema conformance, and per-document semantic rules, and `scripts/jq-edit` is the atomic mutation path. Structural enforcement that removes the remaining discretion (deny the Edit/Write tools on canonical paths; a CI gate) is deferred to ledger items T-014 and T-013 until schemas stabilize; until then the `canonical-json-editing` skill and the AGENTS.md rules carry it.

## References

- [source retrospective](../../retrospective/2026-07-06-2.md)
- [canonical-json-editing skill](../../.claude/skills/canonical-json-editing/SKILL.md)
- [add-governed-doctype skill](../../.claude/skills/add-governed-doctype/SKILL.md)
- [scripts/jq-edit](../../scripts/jq-edit), [scripts/lint-json](../../scripts/lint-json)
- [ADR 0002: TODO.json ledger](./0002-todo-json-cross-session-ledger.md) — the first record stored under this decision.
- Decision made in PR #2.
