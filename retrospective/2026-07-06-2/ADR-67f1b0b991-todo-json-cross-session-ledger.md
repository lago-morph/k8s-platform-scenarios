# ADR: TODO.json is the cross-session handoff ledger

- **ID**: ADR-67f1b0b991
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-07-06
- **Source retrospective**: ../2026-07-06-2.md
- **PRs covered**: #2

## Context

The owner, on why a durable ledger had to exist before any implementation started: "I have seen over and over again excellent ideas during discussion in agent sessions, then losing those ideas later because they were not preserved." Session-local task trackers are precisely the ephemerality being complained about — they die with the container. The ledger had to be a committed artifact, machine-parseable (so statuses can be counted and enforced), and self-describing enough that a cold future session can act on any item without the originating conversation.

## Decision

Design decisions and pending work are preserved in TODO.json, a schema-governed canonical JSON ledger with stable append-only T-NNN identifiers, whose phase and order fields are explicit proposals for the repository owner to re-sort.

Key conventions, stated inside the file itself: IDs are never renumbered or reused (dropped items keep their ID with status=dropped); an item's presence means *preserved*, not *approved*; summaries are written to handoff quality — enough context for a cold session; statuses flip via scripts/jq-edit in the same PR that lands the work, with a delivery note appended. The file was the repository's first schema-governed document (schemas/todo.schema.json), making it the proving ground for the whole canonical-JSON stack.

## Alternatives considered

- **Session-local task tracking (harness task tools)** — rejected: dies with the session/container; exactly the failure mode the owner described.
- **Markdown TODO checklist** — rejected: unlintable statuses and unenforceable structure; contradicts the owner's structured-data doctrine adopted the same day.
- **GitHub issues as the ledger** — rejected: not diff-reviewable in PRs alongside the work they track, not governed by the repo's linters, and awkward to reference from prompts (the S4 probe launch prompt references ledger IDs directly).

## Consequences

Easier: ideas survive context truncation (thirty items captured from one discussion; four implemented and status-flipped within hours); future-session prompts can be written against item IDs; per-status counts are one jq expression. Harder: the ledger only works if sessions maintain the discipline of reading it first and updating it as work lands — a companion agents-file rule exists for exactly this; item summaries grow long as delivery notes accrete (accepted: completeness beats brevity in a handoff artifact). Accepted trade-off: some ceremony per landed item in exchange for institutional memory that no longer depends on any single session's context window.

## References

- [`../2026-07-06-2.md`](../2026-07-06-2.md) — the source retrospective.
- [`./AGENTS-MD-b54f8bb12e-todo-json-is-the-handoff.md`](./AGENTS-MD-b54f8bb12e-todo-json-is-the-handoff.md) — the companion maintenance rule.
- PRs the decision was made in: #2 (commit 2b63e12 created the ledger; schema in commit 6c2228a).
