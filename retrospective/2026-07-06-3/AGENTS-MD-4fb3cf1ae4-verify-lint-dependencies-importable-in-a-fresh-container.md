# agent instruction

**Verify lint dependencies are importable in a fresh container.** Before relying on `scripts/lint-json` or `scripts/jq-edit` in a new remote session, confirm the Python `jsonschema` package imports (`python3 -c 'import jsonschema'`); if it does not, run `pip install jsonschema` first. Without it, both scripts fail with `validate-schema` exit 2 on the very first JSON mutation — schema validation cannot run — and the failure reads like a lint violation rather than a missing dependency.

*Grounded in: the first jq-edit of the T-004 session failing on a fresh container until jsonschema was installed (see ledger T-031).*

# justification

Executing T-004, the first `scripts/jq-edit TODO.json …` of the session failed immediately with `validate-schema: the python 'jsonschema' package is not installed` and exit 2 — the ledger mutation had actually landed, but the linter could not confirm it, and the error surface looked like a schema violation rather than an environment gap. The canonical-json-editing skill documents the dependency, but nothing in a fresh remote container installs it, so every new session hits this wall before it can touch a canonical document. The permanent fix is tracked as ledger item T-031 (deterministic provisioning); until that lands, the marginal cost of this rule is a single `import` check at session start, which turns a confusing exit-2 into a one-line install. The asymmetry is stark: one cheap check versus a mislabeled failure on the session's first mutation.
