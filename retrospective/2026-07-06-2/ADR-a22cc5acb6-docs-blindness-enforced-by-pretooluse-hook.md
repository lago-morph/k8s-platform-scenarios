# ADR: The docs-blindness contract is enforced by a deterministic PreToolUse hook

- **ID**: ADR-a22cc5acb6
- **Status**: Draft (not yet adopted to docs/adr/)
- **Date**: 2026-07-06
- **Source retrospective**: ../2026-07-06-2.md
- **PRs covered**: #2

## Context

The charter's founding rule is that scenario authors must never read the platform repository's source — one peek "destroys the corpus's entire diagnostic value." The owner's position, from repeated experience: "CLAUDE.md rules are not worth the electrons they are created with. Rules that you depend on need to be instantiated as hooks, and be deterministic." The boundary therefore had to move from prose to mechanism before the first docs-only probe agent runs.

## Decision

A PreToolUse hook (scripts/hooks/deny-platform-source) deterministically denies any tool call whose input text references the platform source repository, failing closed on unparseable input, with the published documentation site as the only allowed platform surface.

Mechanics: the hook re-serializes `tool_input` compactly, scrubs references to this repository's own name (the `-scenarios` suffix distinguishes them), then denies on any remaining owner/repo-path or MCP repo-parameter match, case-insensitively — covering https, ssh, raw, codeload, and api URL forms. It is wired in `.claude/settings.json` for WebFetch, WebSearch, Bash, and the github/Claude_Code_Remote MCP tools. Agent-launch tools are deliberately unmatched: probe prompts legitimately contain the forbidden URL as a prohibition, and a subagent's own tool calls are hooked individually. Nineteen table-driven tests live beside the hook.

## Alternatives considered

- **Prose rules in CLAUDE.md** — rejected outright by the owner (see Context); prose depends on obedience, which this session twice demonstrated failing even for rule authors.
- **Environment network-policy allowlist** — stronger (immune to text-level evasion) but environment-scoped rather than repo-scoped, so it doesn't travel with a clone; retained as the strongest layer for dedicated authoring sessions (ledger T-027), not a replacement.
- **Narrow URL-context matching to reduce false positives** — rejected: more pattern surface means more bypass surface. The conservative full-text scan produced exactly one false positive in practice (prose about the boundary inside a command argument), which a wording convention absorbs; a false negative is unrecoverable.

## Consequences

Easier: isolation for docs-only probe agents is enforced rather than promised; the boundary travels with the repository; violations produce an explanatory denial citing the charter. Harder: tool-call text (including commit messages) must refer to the platform source obliquely — proven live when the hook denied its own author's next Bash call minutes after installation. Accepted trade-off: occasional wording contortions in exchange for a boundary that does not depend on any agent's obedience. Known residual gaps: hooks load per-session (an environment without the repo's settings is unprotected — T-027 covers this), and the empirical observation that hooks took effect mid-session is convenient but not contractual.

## References

- [`../2026-07-06-2.md`](../2026-07-06-2.md) — the source retrospective.
- [`./AGENTS-MD-5120e01835-keep-platform-source-path-out-of-tool-call-text.md`](./AGENTS-MD-5120e01835-keep-platform-source-path-out-of-tool-call-text.md) — the companion wording rule.
- PRs the decision was made in: #2 (commit 900ed7e; design discussion in the same session).
