# agent instruction

**TODO.json is the handoff — read it first, update it as you land work.** At session start in this repository, read TODO.json before planning. When work lands, update item statuses via scripts/jq-edit in the same PR (append a delivery note to the item's summary); when new ideas surface in discussion, append them as new T-NNN items rather than letting them evaporate with the session.

*Grounded in: the ledger's founding purpose — the owner losing good ideas from earlier agent sessions.*

# justification

The owner created the ledger after watching, in his words, "excellent ideas during discussion in agent sessions" get lost "over and over again" because nothing preserved them past context truncation. This session then demonstrated the intended loop end-to-end: thirty items captured from one design discussion, four of them implemented within hours with statuses flipped and delivery notes appended in the same PRs, and the S4 probe launch prompt for the next session written *against ledger item IDs* rather than against conversation memory. The rule's cost is one file read at session start and one jq-edit per landed item. Skipping it re-creates the exact failure the ledger exists to prevent — and leaves statuses lying, which is worse than no ledger because it manufactures false confidence about what is done.
