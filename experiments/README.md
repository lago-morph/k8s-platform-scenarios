# experiments/

Throwaway probe records. **Nothing in this tree is canonical** — records
here exist to inform the design of the real schemas and storage
(`scenarios/`, `findings/`, `assumptions/`), and are expected to be
discarded or superseded once those exist.

## Conventions

- One directory per experiment: `experiments/NNN-short-name/`, numbered
  in creation order (`001-…`, `002-…`).
- Records are JSON from day one (so later hardening has a substrate to
  attach to), but **deliberately loose**: no schema, no canonical-form
  requirement, no semantic linting. `scripts/lint-json` checks files in
  this tree for well-formedness only — a malformed record isn't a
  record at all — and skips every other check.
- Each experiment directory should contain a short `README.md` stating
  what question the experiment was probing and what came of it, so a
  future session can tell whether the records still matter.

Ledger: T-003 (this convention), T-004/T-005 (the first experiment).
