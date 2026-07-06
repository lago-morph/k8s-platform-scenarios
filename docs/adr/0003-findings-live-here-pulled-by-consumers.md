# ADR 0003: Findings live in this repository and are pulled by consumers

- **Status**: Accepted
- **Date**: 2026-07-06
- **Deciders**: repo owner
- **ID**: ADR-a1e6164091

## Context

The charter says findings "flow back to the platform repository as issues" but specifies no transport. The session exposed a real tension: granting a scenario-authoring session write access to the platform repository (to file issues) would also put the platform *source* within its reach, and the docs-blindness contract treats a single source peek as corpus-destroying. The session had already watched the access boundary work in the opposite direction — its own GitHub scope denied it a sibling repository. The owner resolved the question directly: "Findings live here. They are pulled into where they need to go if it is a different repo."

## Decision

Findings are stored as schema-governed records in this repository, and the platform repository pulls them to materialize issues on its side, using the finding ID as the idempotency key, with no write-backs in either direction.

The pull direction means scenario sessions never hold credentials for the platform repository, and the platform's pull job needs only read access here. The platform side keeps its own finding-to-issue mapping, so finding records never mutate on account of downstream state.

## Alternatives considered

- **Scenario sessions file issues directly on the platform repository** — rejected: repo access is not scoped finely enough; "could read source but promised not to" is a soft contract, and the owner's doctrine rejects soft contracts for load-bearing rules.
- **A courier step (human or dedicated session) pushing findings outward** — the agent's original proposal; superseded by the owner's pull model, which removes the manual hop and the courier's credentials entirely.
- **Findings as GitHub issues in this repository, mirrored by automation** — rejected: issues are not schema-governed records; files under `findings/` can be linted, versioned, and pulled with the same deterministic tooling as everything else.

## Consequences

Easier: the docs-blindness boundary stays airtight (no cross-boundary credentials in either direction); the platform side can also feed findings into its documentation-generation process. Harder: findings visibility on the platform side depends on a pull job existing there (until then, findings sit here unconverted); status telemetry ("was this finding turned into an issue?") lives outside this repository by design.

Enforcement of the record side is the findings schema and its semantic checks — deferred to ledger item T-008, to be built with the `add-governed-doctype` skill and seeded from real depth-probe output rather than speculation; the stable pull contract (layout, schema version, status semantics) is ledger item T-025. Until those land, this ADR records the direction so no session arms itself with platform-repo write access in the meantime.

## References

- [source retrospective](../../retrospective/2026-07-06-2.md)
- [ADR 0001: canonical JSON via jq-edit](./0001-canonical-json-mutated-only-through-jq-edit.md) — the storage discipline findings records inherit.
- [add-governed-doctype skill](../../.claude/skills/add-governed-doctype/SKILL.md) — how the findings schema (T-008) will be built.
- [experiments/README.md](../../experiments/README.md) — where draft findings from the depth probe land first.
- Decision recorded in PR #2; adopted here.
