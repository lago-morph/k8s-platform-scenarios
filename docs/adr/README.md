# Architecture Decision Records

Numbered, immutable records of binding architectural decisions and the
context that produced them. Format and lifecycle are defined by the
`adr` skill (`.claude/skills/adr/SKILL.md`). Substantive change means a
new superseding ADR, never an in-place edit.

Each ADR also carries a durable `ADR-<hash>` ID (preserved from the
session retrospective it was harvested in); the `NNNN` number is the
human-friendly sequence and the hash is the stable cross-reference.

| # | Title | Status | Date | ID |
|---|-------|--------|------|----|
| [0001](./0001-canonical-json-mutated-only-through-jq-edit.md) | Canonical JSON documents are mutated only through jq-edit | Accepted | 2026-07-06 | ADR-f68da1c75c |
| [0002](./0002-todo-json-cross-session-ledger.md) | TODO.json is the cross-session handoff ledger | Accepted | 2026-07-06 | ADR-67f1b0b991 |
| [0003](./0003-findings-live-here-pulled-by-consumers.md) | Findings live in this repository and are pulled by consumers | Accepted | 2026-07-06 | ADR-a1e6164091 |

Drafts proposed but not yet adopted live in the source retrospective's
sibling directory (`retrospective/2026-07-06-2/`), keyed by the same
`ADR-<hash>` IDs.
