# ADR: Two-tier document governance separates canonical records from throwaway experiments

- **ID**: ADR-dc790b3003
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-07-06
- **Source retrospective**: ../2026-07-06-2.md
- **PRs covered**: #2

## Context

The owner's sequencing doctrine for the first experiments: "The schema should be loose and no linting with these first experiments — we will almost certainly throw them all away anyway," while simultaneously wanting JSON storage from day one so later hardening has a substrate. Full governance (canonical form, schemas, semantic checks) would tax probe agents whose output is expected to be discarded; zero structure would make the outputs unaggregatable. The tension surfaced concretely when the linter was written: its default sweep covers every tracked .json file, which would have imposed canonical form on probe records.

## Decision

Tracked JSON under experiments/ is checked for well-formedness only, while all other tracked JSON is fully governed (canonical form, JSON Schema, semantic checks).

Well-formedness stays mandatory everywhere because a malformed record is not a record at all — it cannot even be read for triage. The experiments/README.md carries the convention: numbered `NNN-name/` directories, loose JSON, a per-experiment README stating the question probed, and the explicit expectation that contents are superseded once real schemas exist (ledger T-008/T-009).

## Alternatives considered

- **Full governance everywhere** — rejected: canonical-form and schema failures on throwaway records generate friction and noise exactly where the owner asked for looseness, and probe subagents would need the whole editing skill just to save output.
- **No linting at all under experiments/** — rejected narrowly: a probe record that isn't parseable JSON silently defeats the aggregation the records exist for; well-formedness is the minimum that keeps the substrate claim honest.
- **Untracked scratch space instead of a committed tree** — rejected: the records are evidence (they seed the findings schema and test the owner's 5–10 findings prediction) and must survive the ephemeral container and be reviewable in PRs.

## Consequences

Easier: probe agents write freely; the canonical tier stays strict without exceptions leaking into it; the linter encodes the boundary in one `case` branch, so the rule is deterministic rather than remembered. Harder: two rule-sets to know (mitigated by experiments/README.md stating its own rules); data graduating from experiments/ to canonical trees must be re-shaped rather than moved. Accepted trade-off: a deliberate, visible looseness tier instead of either taxing experiments or corrupting the canonical tier's guarantees.

## References

- [`../2026-07-06-2.md`](../2026-07-06-2.md) — the source retrospective.
- [`./ADR-f68da1c75c-canonical-json-mutated-only-through-jq-edit.md`](./ADR-f68da1c75c-canonical-json-mutated-only-through-jq-edit.md) — the canonical tier this decision carves an exception from.
- PRs the decision was made in: #2 (commit 900ed7e).
