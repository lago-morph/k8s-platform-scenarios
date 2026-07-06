# agent instruction

**Route actionable items to the ledger, never to a retrospective.** Any defect, follow-up, or todo discovered mid-session goes into `TODO.json` as a `T-NNN` item via `scripts/jq-edit` — the queue future sessions actually read. Retrospectives are knowledge-harvest only: no defined process reads a retrospective after it is produced, so an actionable item parked there is lost. A retrospective may still propose skills, agents-file rules, and ADR drafts (each has a downstream consumer), but a discovered defect belongs in the ledger.

*Grounded in: the owner redirecting the fresh-container jsonschema gap into ledger item T-031 rather than the retrospective.*

# justification

When the session surfaced the jsonschema setup gap, the first instinct was to let the retrospective carry it. The owner corrected this directly: "retrospectives are NOT places to put defects or todo items — there is no defined process that ever reads a retrospective after it is produced." The gap was instead recorded as ledger item T-031, where the handoff discipline (already codified in AGENTS.md as "TODO.json is the handoff") guarantees a future session sees it. This rule sharpens that existing handoff rule with the specific negative: the retrospective is the wrong home for anything actionable. The marginal cost is one jq-edit; the cost of getting it wrong is a real defect evaporating into a document nobody re-reads.
