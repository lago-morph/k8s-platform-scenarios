# agent instruction

**Mutate canonical JSON only via jq-edit.** Never text-edit a tracked .json file (no Edit/Write tools, no sed/awk). Use scripts/jq-edit FILE FILTER [JQ_ARGS...] — the filter is always the second argument, and options like --arg come after it — and run scripts/lint-json before every commit.

*Grounded in: the tool's author violating its argument order minutes after writing it, plus the identical error in a just-written skill recipe.*

# justification

The author of `scripts/jq-edit` put `--arg` before the filter on the first real call after writing the tool — jq failed, the wrapper correctly left the file unchanged, and investigating the failure revealed the same wrong order baked into a recipe in the freshly written `canonical-json-editing` skill. Two violations of a convention by its own author, inside ten minutes, is the whole argument for deterministic enforcement in one anecdote: humans and agents will not hold argument order in their heads, so the wrapper (atomic replace + auto-lint) and the pre-commit lint have to. Cost of the rule: none — `jq-edit` is already the shorter path. Cost without it: malformed JSON, trailing commas, and diffs that lie, each requiring recovery-by-hand in a repo whose premise is that machine-owned records stay machine-parseable.
