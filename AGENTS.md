# AGENTS.md

Operating rules for agents working in this repository. Each rule is
assembled verbatim from a per-rule source file in a session
retrospective; the `<!-- AGENTS-MD-<hash> -->` comment above each rule
is its durable identifier and points back to that source (which also
carries the justification). Rules are added here only after review — do
not edit rule text in place; supersede it with a new retrospective
rule instead.

## Boundary

<!-- AGENTS-MD-5120e01835 — retrospective/2026-07-06-2/AGENTS-MD-5120e01835-keep-platform-source-path-out-of-tool-call-text.md -->

**Keep the platform-source path out of tool-call text.** The docs-blindness hook scans the full text of Bash commands and other tool inputs. Never write the platform source repository's owner/repo path into a shell command, a commit message, or prose passed through a command argument — refer to it obliquely ("the platform source repository") instead. Content at rest in files is not scanned; only tool-call text is.

*Grounded in: the hook denying its own author's next Bash call minutes after installation.*

## Canonical data

<!-- AGENTS-MD-4f3a50e00b — retrospective/2026-07-06-2/AGENTS-MD-4f3a50e00b-mutate-canonical-json-only-via-jq-edit.md -->

**Mutate canonical JSON only via jq-edit.** Never text-edit a tracked .json file (no Edit/Write tools, no sed/awk). Use scripts/jq-edit FILE FILTER [JQ_ARGS...] — the filter is always the second argument, and options like --arg come after it — and run scripts/lint-json before every commit.

*Grounded in: the tool's author violating its argument order minutes after writing it, plus the identical error in a just-written skill recipe.*

<!-- AGENTS-MD-f6a1a629a1 — retrospective/2026-07-06-2/AGENTS-MD-f6a1a629a1-bootstrap-new-json-files-through-immediate-canonicalization.md -->

**Bootstrap new JSON files through immediate canonicalization.** Creating a JSON document with the Write tool is acceptable exactly once, at birth; immediately canonicalize and lint it with scripts/jq-edit FILE '.' before doing anything else. All subsequent mutations go through jq-edit.

*Grounded in: schemas/todo.schema.json, schemas/map.json, and .claude/settings.json all bootstrapped this way this session.*

## Working across repositories

<!-- AGENTS-MD-fd414c21c9 — retrospective/2026-07-06-2/AGENTS-MD-fd414c21c9-fetch-out-of-scope-public-repos-via-raw-githubusercontent.md -->

**Fetch out-of-scope public repos via raw.githubusercontent.com.** For public GitHub repositories outside the session's repository scope, github.com, api.github.com, and codeload.github.com are proxy-intercepted and return a JSON error body; raw.githubusercontent.com serves file content. A missing file returns the literal body "404: Not Found" with curl exit 0 — check for that sentinel explicitly.

*Grounded in: importing three skills from a sibling public repository through the proxy.*

## Process

<!-- AGENTS-MD-b54f8bb12e — retrospective/2026-07-06-2/AGENTS-MD-b54f8bb12e-todo-json-is-the-handoff.md -->

**TODO.json is the handoff — read it first, update it as you land work.** At session start in this repository, read TODO.json before planning. When work lands, update item statuses via scripts/jq-edit in the same PR (append a delivery note to the item's summary); when new ideas surface in discussion, append them as new T-NNN items rather than letting them evaporate with the session.

*Grounded in: the ledger's founding purpose — the owner losing good ideas from earlier agent sessions.*

<!-- AGENTS-MD-d2782280eb — retrospective/2026-07-06-2/AGENTS-MD-d2782280eb-clean-up-scheduled-check-ins-when-their-pr-closes.md -->

**Clean up scheduled check-ins when their PR closes.** If you armed a send_later self check-in to watch a pull request, delete the trigger the moment the PR merges or closes. Orphaned triggers fire into finished work and waste a wake-up on nothing.

*Grounded in: deleting the armed check-in triggers after PR #1 and PR #2 merged.*
