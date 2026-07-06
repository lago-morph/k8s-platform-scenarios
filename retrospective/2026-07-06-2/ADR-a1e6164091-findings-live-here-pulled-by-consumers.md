# ADR: Findings live in this repository and are pulled by consumers

- **ID**: ADR-a1e6164091
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-07-06
- **Source retrospective**: ../2026-07-06-2.md
- **PRs covered**: #2

## Context

The charter says findings "flow back to the platform repository as issues" but specifies no transport. The session exposed a real tension: granting a scenario-authoring session write access to the platform repository (to file issues) would also put the platform *source* within its reach, and the docs-blindness contract treats a single source peek as corpus-destroying. The session had already watched the access boundary work in the opposite direction — its own GitHub scope denied it a sibling repository. The owner resolved the question directly: "Findings live here. They are pulled into where they need to go if it is a different repo."

## Decision

Findings are stored as schema-governed records in this repository, and the platform repository pulls them to materialize issues on its side, using the finding ID as the idempotency key, with no write-backs in either direction.

The pull direction means scenario sessions never hold credentials for the platform repository, and the platform's pull job needs only read access here. The platform side keeps its own finding-to-issue mapping, so finding records never mutate on account of downstream state. Enforced finding schemas (ledger T-008) are what make the pull mechanical; the stable pull contract (layout, schema version, status semantics) is ledger T-025.

## Alternatives considered

- **Scenario sessions file issues directly on the platform repository** — rejected: repo access is not scoped finely enough; "could read source but promised not to" is a soft contract, and the owner's doctrine rejects soft contracts for load-bearing rules.
- **A courier step (human or dedicated session) pushing findings outward** — the agent's original proposal; superseded by the owner's pull model, which removes the manual hop and the courier's credentials entirely.
- **Findings as GitHub issues in this repository, mirrored by automation** — rejected implicitly: issues are not schema-governed records; files under findings/ can be linted, versioned, and pulled with the same deterministic tooling as everything else.

## Consequences

Easier: the blindness boundary stays airtight (no cross-boundary credentials in either direction); the platform side can also feed findings into its documentation-generation process — an open question the owner flagged, expected to send discoveries back that change this repository. Harder: findings visibility on the platform side depends on a pull job existing there (until then, findings sit here unconverted); status telemetry ("was this finding turned into an issue?") lives outside this repository by design. Accepted trade-off: an eventually-consistent, one-directional flow in exchange for never arming a scenario session with platform-repo access.

## References

- [`../2026-07-06-2.md`](../2026-07-06-2.md) — the source retrospective.
- [`./ADR-a22cc5acb6-docs-blindness-enforced-by-pretooluse-hook.md`](./ADR-a22cc5acb6-docs-blindness-enforced-by-pretooluse-hook.md) — the boundary this transport decision protects.
- PRs the decision was made in: #2 (ledger items T-008/T-025 record the decision; owner statement in the same session's discussion).
