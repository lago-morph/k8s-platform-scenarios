# Spec: `capture-subagent-structured-output`

- **ID**: SKILL-SPEC-b92a30d853
- **Source retrospective**: ../2026-07-06-3.md

## Intent

When a subagent must return machine-readable output — JSON in the S4 depth probe — the reliable copy is not the completion notification (it HTML-escapes `<`, `>`, `&`, and `"` and is display-truncated) but the subagent's final message in the task transcript JSONL. This skill extracts that final message verbatim, tolerates a final-token truncation by repairing only the terminal delimiter, verifies the repaired text parses and is fully consumed, and records any deviation from byte-for-byte in the artifact that stores it. It earns its place because this repository's whole method is dispatching docs-blind subagents whose structured output is the product; a silently mangled or lossily copied return corrupts the evidence base.

## Trigger

Activate when you dispatch a subagent (the Agent tool, a Task, or a
workflow agent) whose deliverable is machine-readable — JSON or any
parseable structured text — that you must persist verbatim or parse.
Direct phrases: "save the subagent's output", "the agent returns JSON",
"capture the probe output". Proactive: any docs-blind probe, breadth
sweep, or batch-authoring agent in this repository. Negative triggers:
prose summaries where a lossy copy is fine; agents whose result you only
read once and do not store.

## Inputs

- The subagent's task-transcript path (the `output_file` / the
  `tasks/<id>.output` JSONL the harness writes — never the inline
  `<task-notification>` block).
- A marker substring that identifies the final structured message
  (e.g. a distinctive key such as `"scenario_id"`).
- The destination path for the verbatim artifact.

## Outputs

- A destination file holding the subagent's structured output
  byte-for-byte, modulo a disclosed minimal terminal repair.
- Small diagnostics printed to your own context (counts, top-level
  keys) — never the full payload, which would waste context.
- A one-line disclosure for the artifact's README / commit message if
  any preamble was stripped or any terminal repair applied.

## Workflow

1. Do NOT copy the output from the completion-notification wrapper — it
   HTML-escapes `<`/`>`/`&`/`"` and is display-truncated.
2. Read the transcript JSONL. Walk every event and collect all assistant
   `text` blocks (recurse into message content arrays).
3. Select the last `text` block that contains the marker substring.
4. Strip any prose preamble: find the first `{` (or `[`), then decode
   with a JSON raw-decoder to get the exact end offset of the object.
5. If it parses and consumes to the end of the string, write the sliced
   bytes verbatim to the destination.
6. If it does not parse, attempt a minimal terminal repair: append
   closing `}` / `]` one at a time, up to a small bound (≤3), until it
   parses AND the whole string is consumed. If no small repair works,
   STOP and report — never hand-edit interior content.
7. Assert there is no trailing non-whitespace after the parsed value.
8. Write the (possibly minimally repaired) JSON to the destination.
   Print only counts/keys as diagnostics.
9. If you stripped a preamble or repaired a delimiter, record exactly
   what changed in the artifact's README and the commit message.

## Concrete examples

### Example 1: the S4 probe (real)

Transcript `tasks/a70…​.output`; marker `"scenario_id"`. The final
assistant text held a one-sentence prose preamble followed by the JSON,
and the JSON arrived one byte short of well-formed (missing the single
top-level closing brace). The extractor dropped the preamble, appended
exactly one `}`, confirmed the result parsed and consumed to end, and
wrote `experiments/001-s4-depth-probe/probe-output.json`. Both
deviations (preamble drop, one-brace repair) are disclosed verbatim in
that experiment's `README.md` and the commit body.

### Example 2: clean case

An agent returns a well-formed JSON array as its entire final message.
Find the first `[`, raw-decode — it consumes the whole string, so no
repair is needed. Write the bytes verbatim; diagnostics print only the
element count. No disclosure needed because nothing was altered.

## Anti-patterns

- **Copying from the `<task-notification>` block.** Its `&lt;` / `&quot;`
  escapes silently corrupt the data — the S4 output was full of `<`
  and `"`.
- **Reading the whole transcript into your context.** It is the full
  subagent JSONL and will overflow context; walk-and-extract, printing
  only diagnostics.
- **"Fixing" the JSON by reformatting or editing interior values.**
  That destroys verbatim fidelity; only a terminal-delimiter repair is
  allowed, and it must be disclosed.
- **Silently dropping the preamble.** Any deviation from byte-for-byte
  gets recorded, or the "verbatim" claim is false.

## Acceptance criteria

- [ ] The destination file parses as JSON.
- [ ] It equals the subagent's final-message bytes except for a
      disclosed minimal terminal repair and/or a disclosed preamble
      strip.
- [ ] No interior bytes were altered.
- [ ] Every deviation is recorded in a human-readable note (README +
      commit).
- [ ] The extraction never printed the full payload into the agent's
      context.

## Files this skill creates / modifies

- A throwaway extractor script (in the scratchpad) — walks the JSONL,
  slices and repairs, writes the artifact.
- The destination artifact, e.g. `experiments/NNN-<name>/probe-output.json`.
- That experiment's `README.md` — updated to disclose any deviation.
