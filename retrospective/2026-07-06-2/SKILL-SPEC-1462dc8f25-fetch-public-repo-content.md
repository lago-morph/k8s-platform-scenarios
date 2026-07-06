# Spec: `fetch-public-repo-content`

- **ID**: SKILL-SPEC-1462dc8f25
- **Source retrospective**: ../2026-07-06-2.md

## Intent

Retrieve files from a public GitHub repository that lies outside the session's authorized repository scope, where the environment proxy intercepts github.com, api.github.com, and codeload.github.com but permits raw.githubusercontent.com. The skill turns an un-listable remote directory into a complete local mirror by combining reference-scanning of already-fetched files with probing of conventional subdirectory names, using the literal '404: Not Found' body as an existence sentinel. It earns its place because this session lost a file (a skill's spec/SPEC.md) to naive reference-scanning and only recovered it by a systematic probe.

## Trigger

- Direct: "copy the skill at <github URL> into this repo", "grab files from <public repo> we don't have access to", "mirror directory X from repo Y".
- Proactive: any GitHub MCP call or curl to a repository that returns the proxy's "not enabled for this session" JSON error, when the user has confirmed (or the task implies) the repository is public.
- Negative: do NOT use for repositories in the session's scope (use git/MCP directly); do NOT use to reach a repository the user has declined to add or that policy forbids (in this repo, the platform source is hook-denied regardless).

## Inputs

- Owner/repo, branch (default `main`), and the directory or file paths wanted.
- The proxy CA bundle if curl needs it (`--cacert /root/.ccr/ca-bundle.crt` in this environment).
- A destination directory in the local repo.

## Outputs

- A local mirror of the requested files, byte-identical to the source branch.
- A fetch report in chat: files copied, files probed-and-absent, any referenced-but-unfetched paths that belong to other directories.

## Workflow

1. Fetch the entry-point file first (e.g. `SKILL.md`) from `https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>`. If the response body is the proxy's JSON interception message, the repo is not reachable even via raw — stop and report; do not retry other hosts.
2. Grep every fetched file for path-like references: pattern `(resources|scripts|templates|spec|references|assets|examples)/[A-Za-z0-9._-]+` plus a broader `[A-Za-z0-9._/-]+\.(md|py|sh|json|yaml|yml|txt)` sweep. Classify each hit: inside the target directory (fetch it) vs. elsewhere in the source repo (report, don't fetch, unless asked).
3. Probe conventional filenames regardless of references: for each of `resources/ scripts/ templates/ spec/ references/ assets/ examples/`, try plausible standard files (`SPEC.md` under `spec/`, `README.md` at the directory root, etc.).
4. Detect absence explicitly: a missing file returns HTTP 200-ish behavior from curl (exit 0) with the exact 14-byte body `404: Not Found`. Compare the body, never the exit code.
5. Repeat steps 2–4 on newly fetched files until no new in-scope references appear (transitive closure).
6. Write files to the destination preserving relative structure; verify each is non-empty and not the 404 sentinel; report the final tree.

## Concrete examples

### Example 1: the miss this spec exists to prevent

Importing `self-retrospective` from the software-factory repo, the first pass grepped SKILL.md with `(resources|scripts|assets|references)/...` — no `spec/` in the pattern — and shipped 5 files. The skill's `spec/SPEC.md` (48,101 bytes) surfaced only later, during step-3-style probing done for a *different* skill: `curl .../self-retrospective/spec/SPEC.md` returned real content, and the file had to be back-filled in a follow-up commit (860c7ae). With step 3 in the workflow, the first pass would have been complete.

### Example 2: reference classification done right

The same repo's `adr` skill referenced `scripts/check_adr_links.py`, `templates/0000-template.md`, and `docs/adr/...` paths. Steps 2–3 fetched the first two plus probed-and-found `spec/SPEC.md`; the `docs/adr/` references were classified "elsewhere in repo — artifacts the skill writes, not skill files" and correctly excluded. Meanwhile `self-retrospective`'s mention of `check_adr_links.py` was recognized as belonging to the *adr* skill's tree, not copied into self-retrospective's.

## Anti-patterns

- **Trusting curl's exit code for existence.** The 404 sentinel arrives with exit 0; this session nearly saved `404: Not Found` as `scripts/check_adr_links.py` (14 bytes, caught by the byte-count check).
- **Trying api.github.com / codeload / github.com HTML first.** All three burned a call each returning the proxy's JSON message; raw.githubusercontent.com is the only path that works. Don't rediscover this per session.
- **Reference-scanning as the sole enumeration.** The spec/SPEC.md miss. References find what's linked; probes find what's conventional; only both find everything reachable without a directory listing.
- **Pre-checking reachability before add_repo when the user asked for session integration.** Different tool for a different ask — this skill is for content copies of public repos, not for wiring a repo into the session.

## Acceptance criteria

- [ ] Every file in the mirrored directory is byte-identical to the source branch (spot-check sizes + first/last lines).
- [ ] No mirrored file contains the 404 sentinel or the proxy's JSON interception message.
- [ ] The conventional-subdirectory probe ran even if references seemed complete, and the report says which probes came back absent.
- [ ] Out-of-directory references are reported, not silently fetched or silently dropped.

## Files this skill creates / modifies

- `<destination>/…` — the mirrored files, preserving relative structure.
- No repository metadata, no settings changes; the skill is read-only against the source and additive locally.
