# ADR 0002: TODO.json is the cross-session handoff ledger

- **Status**: Accepted
- **Date**: 2026-07-06
- **Deciders**: repo owner
- **ID**: ADR-67f1b0b991

## Context

The owner, on why a durable ledger had to exist before any implementation started: "I have seen over and over again excellent ideas during discussion in agent sessions, then losing those ideas later because they were not preserved." Session-local task trackers are precisely the ephemerality being complained about — they die with the container. The ledger had to be a committed artifact, machine-parseable (so statuses can be counted and enforced), and self-describing enough that a cold future session can act on any item without the originating conversation.

## Decision

Design decisions and pending work are preserved in `TODO.json`, a schema-governed canonical JSON ledger with stable append-only `T-NNN` identifiers, whose phase and order fields are explicit proposals for the repository owner to re-sort.

Key conventions, stated inside the file itself: IDs are never renumbered or reused (dropped items keep their ID with `status=dropped`); an item's presence means *preserved*, not *approved*; summaries are written to handoff quality; statuses flip via `scripts/jq-edit` in the same PR that lands the work, with a delivery note appended.

## Alternatives considered

- **Session-local task tracking (harness task tools)** — rejected: dies with the session/container; exactly the failure mode the owner described.
- **Markdown TODO checklist** — rejected: unlintable statuses and unenforceable structure; contradicts the owner's structured-data doctrine adopted the same day.
- **GitHub issues as the ledger** — rejected: not diff-reviewable in PRs alongside the work they track, not governed by the repo's linters, and awkward to reference from prompts (the S4 probe launch prompt references ledger IDs directly).

## Consequences

Easier: ideas survive context truncation (thirty items captured from one discussion; several implemented and status-flipped within hours); future-session prompts can be written against item IDs; per-status counts are one jq expression. Harder: the ledger only works if sessions maintain the discipline of reading it first and updating it as work lands; item summaries grow long as delivery notes accrete (accepted: completeness beats brevity in a handoff artifact).

Enforcement: the file is governed by `schemas/todo.schema.json` and the `check_todo()` semantic checks in `scripts/lint-json` (unique IDs, referential integrity of `depends_on`, id-sorted items, alphabetically sorted arrays, status within the declared vocabulary) — it was the repository's first schema-governed document and the proving ground for the whole canonical-JSON stack. The maintenance discipline is carried by an AGENTS.md rule.

## References

- [source retrospective](../../retrospective/2026-07-06-2.md)
- [TODO.json](../../TODO.json), [schemas/todo.schema.json](../../schemas/todo.schema.json)
- [AGENTS.md](../../AGENTS.md) — the companion maintenance rule (read-first, update-as-you-land).
- [ADR 0001: canonical JSON via jq-edit](./0001-canonical-json-mutated-only-through-jq-edit.md) — the storage discipline this ledger is stored under.
- Decision made in PR #2.
