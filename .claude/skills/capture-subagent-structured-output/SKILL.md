---
name: capture-subagent-structured-output
description: Capture a subagent's machine-readable output (JSON) verbatim from its task transcript, tolerating a final-token truncation and disclosing any repair. Use whenever a dispatched subagent (Agent/Task/workflow agent) returns structured output you must persist or parse — docs-blind probes, breadth sweeps, batch authoring, any agent whose JSON is the product. Core rule — never copy the output from the completion-notification wrapper (it HTML-escapes < > & " and is display-truncated); read the final message from the transcript JSONL, repair only the terminal delimiter if truncated, verify it parses and fully consumes, and record any deviation from byte-for-byte. Triggers on "save the subagent's output", "capture the probe output", "the agent returns JSON", "extract the agent's result".
---

# Skill: capture-subagent-structured-output

When a subagent's deliverable is machine-readable — a JSON object, as in
the S4 depth probe — the reliable copy is **not** the completion
notification. That wrapper HTML-escapes `<`, `>`, `&`, and `"` (they
arrive as `&lt;`, `&gt;`, `&amp;`, `&quot;`) and is display-truncated, so
copying structured output from it silently corrupts the data. The task
**transcript JSONL** carries the subagent's final message unescaped; that
is the source of truth.

This repository dispatches subagents as its primary instrument, so a
lossy or unparseable capture corrupts the evidence base. This skill makes
the capture faithful and the fidelity auditable.

## When to use

- A subagent returned JSON (or any parseable structured text) you must
  save verbatim or parse — probe output, gap maps, structured findings.
- You are about to copy an agent's result into a file or the ledger.

Do **not** use it for prose summaries where a lossy copy is acceptable,
or for agent results you only read once and never store.

## Inputs

- The subagent's transcript path — the `output_file` the harness reports
  when the agent is launched, i.e. the `tasks/<agentId>.output` JSONL.
  **Never** the inline `<task-notification>` block.
- A marker substring that uniquely identifies the final structured
  message (a distinctive key such as `"scenario_id"`).
- The destination path for the verbatim artifact.

## Outputs

- The destination file, holding the subagent's structured output
  byte-for-byte — modulo a **disclosed** minimal terminal repair.
- A disclosure line (preamble stripped? delimiters appended?) to copy
  into the artifact's README and the commit message.

## The tool

`scripts/extract-json.py` does the whole procedure deterministically:

```
python3 .claude/skills/capture-subagent-structured-output/scripts/extract-json.py \
  --transcript <tasks/<agentId>.output> \
  --marker '"scenario_id"' \
  --out <destination.json> \
  [--max-repair 3]
```

It walks the JSONL, collects every assistant `text` block, takes the
**last** one containing the marker, strips any prose preamble (finds the
first `{`/`[` and raw-decodes from there), and — if the value does not
parse — appends only closing delimiters (`}`/`]`), shortest sequence
first, up to `--max-repair`, until the value parses **and** consumes the
whole string. It refuses a slice with trailing non-whitespace, never
edits interior bytes, prints diagnostics (never the full payload) on
stderr, and exits non-zero if it cannot produce well-formed JSON. Copy
its `DISCLOSE:` lines into your artifact.

## Workflow

1. Get the subagent's transcript path from its launch metadata
   (`output_file` / `tasks/<agentId>.output`). Do not read that file
   into your own context — it is the full JSONL and will overflow it.
2. Run `extract-json.py` with a marker unique to the final message.
3. Read the stderr diagnostics. If it exits non-zero, do not fabricate
   output — investigate (wrong marker? the agent never returned JSON?
   truncated beyond a terminal-delimiter repair?).
4. If the destination must be canonical (it is under a governed tree,
   not `experiments/`), run it through `scripts/jq-edit FILE '.'`. For
   `experiments/` records, well-formedness is the only requirement.
5. Record every deviation the tool disclosed (preamble stripped, N
   delimiters appended) in the artifact's README and the commit body.
   "Verbatim" is a claim you must be able to back.

## Concrete examples

### Example 1: the S4 probe (real, reproducible)

```
python3 .claude/skills/capture-subagent-structured-output/scripts/extract-json.py \
  --transcript /…/tasks/a709795193e2ea0bf.output \
  --marker '"scenario_id"' \
  --out experiments/001-s4-depth-probe/probe-output.json
```

stderr:

```
wrote …/probe-output.json: object with keys: assumptions, blocked, docs_root, l1, missing_facts, notes, objective, role, scenario_id
DISCLOSE: stripped prose preamble (174 chars): 'I now have complete coverage of the deploy path…'
DISCLOSE: appended 1 closing delimiter(s) '}' to terminate a truncated value
```

The agent prefaced its JSON with one sentence and stopped one byte short
of well-formed (missing the single top-level `}`). The tool stripped the
preamble, appended exactly one `}`, and verified full consumption. Both
disclosures went into the experiment's README and commit.

### Example 2: clean case

An agent returns a well-formed JSON array as its entire final message.
`extract-json.py --marker '"finding_id"'` finds the first `[`, raw-decodes
the whole string, needs no repair, and prints
`verbatim: no preamble, no repair`. Nothing to disclose.

## Anti-patterns

- **Copying from the `<task-notification>` block.** Its `&lt;` / `&quot;`
  escapes corrupt the data — the S4 output was dense with `<` and `"`.
- **Reading the transcript JSONL into your own context** to eyeball the
  JSON. It overflows context; run the tool instead.
- **"Fixing" the JSON by reformatting or editing interior values.** Only
  a terminal-delimiter append is allowed, and it must be disclosed.
- **Silently dropping the preamble or a repair.** An undisclosed
  deviation makes the "verbatim" claim false.
- **Accepting a slice with trailing content.** That means the wrong span
  was taken; the tool rejects it and so should you.

## Acceptance criteria

- [ ] The destination parses as JSON.
- [ ] It equals the subagent's final-message bytes except for a disclosed
      preamble strip and/or a disclosed minimal terminal repair.
- [ ] No interior bytes were altered.
- [ ] Every deviation is recorded in a human-readable note (README +
      commit).
- [ ] The full payload was never printed into the agent's context.

## Files

- `scripts/extract-json.py` — the deterministic extractor described above.
