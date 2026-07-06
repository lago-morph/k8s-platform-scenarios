# agent instruction

**Capture a subagent's structured output from the transcript, not the notification.** When a subagent returns machine-readable output, do not copy it from the completion-notification wrapper — that wrapper HTML-escapes `<`, `>`, `&`, and `"` and is display-truncated. Read the final message verbatim from the task transcript JSONL instead. Expect a possible final-token truncation; if you must repair the text to make it parse, keep the repair to the terminal delimiter only, verify the result parses with no trailing content, and disclose the exact repair in the artifact that stores the output.

*Grounded in: saving the S4 probe output, whose final message arrived one byte short of well-formed JSON.*

# justification

The S4 depth-probe subagent returned a ~23 KB JSON object dense with `<`, `>`, and `"` — every one of which appears in the `<task-notification>` block as `&lt;`, `&gt;`, `&quot;`. Copying the output from that notification would have silently corrupted the evidence the whole experiment exists to produce. Worse, the agent's final message arrived one byte short of well-formed — missing its single top-level closing brace — so a naive copy would not even parse. Extracting from the transcript JSONL and repairing exactly one delimiter (then disclosing it) preserved fidelity. The marginal cost of the rule is one small extractor script; the cost of ignoring it is a corrupted or unparseable record that looks authoritative. This repository runs subagents as its primary instrument, so the rule pays for itself on the very next probe.
