# k8s-platform-scenarios

Scenario-based testing for the `k8s-platform` Kubernetes platform. This
repository finds defects by using the platform the way its real users would —
owners, tenant admins, tenant developers, end-users, a blog author, and
adversaries — and by comparing what the platform's *documentation* promises
with what the *product* actually does.

## How it works

Every scenario is simultaneously a test of four artifacts: the
**documentation**, the **implementation**, the **requirements**, and the
**scenario itself**. When a scenario fails, the finding names which of the
four is defective.

The founding rule is the **docs-blindness contract**: scenarios are written
exclusively from the platform's published documentation site, this
repository's charter, and role credentials — never from the platform
repository's source code. If a scenario can't be written because the docs
lack the information, that *is* the finding: it's filed as a documentation
bug and the scenario stays visibly blocked-on-docs.

Scenarios mature through a five-level pipeline, from a one-line bullet
(**L0**) through a prose scenario (**L1**), an executable spec (**L2**), an
automated test (**L3**), and finally a gating test that runs on every clean
platform build (**L4**). New scenarios are generated as cells in a
roles × verbs × surfaces matrix; findings flow back to the platform
repository as issues — this repository never fixes the platform itself.

## Contents

| Path | What it is |
|---|---|
| [`charter.md`](charter.md) | The founding charter: mission, docs-blindness contract, maturity pipeline, execution contract, findings format, and governance |
| [`scenario-brainstorm.md`](scenario-brainstorm.md) | The seed L0 catalog: 39 scenarios ranked into five waves by when the platform can execute them |
| [`TODO.json`](TODO.json) | Cross-session idea ledger: design decisions and pending work with stable IDs, phases, and dependencies, in canonical JSON |
| [`AGENTS.md`](AGENTS.md) | Operating rules for agents in this repo, assembled from reviewed session-retrospective rules |
| [`docs/adr/`](docs/adr/) | Architecture Decision Records: the binding decisions behind the data layer, ledger, and findings model |
| [`schemas/`](schemas/) | JSON Schemas for the repository's canonical documents, plus the pattern→schema map the linter uses |
| [`scripts/`](scripts/) | Deterministic tooling: `lint-json` (canonical-form + schema + semantic checks), `jq-edit` (the sanctioned mutation path), `validate-schema.py` |
| [`scripts/hooks/`](scripts/hooks/) | PreToolUse hook (with tests) that deterministically enforces the docs-blindness boundary — platform source denied, published docs allowed — wired via [`.claude/settings.json`](.claude/settings.json) |
| [`experiments/`](experiments/) | Throwaway probe records: loose JSON, well-formedness-only linting, expected to be superseded by real schemas |
| [`.claude/skills/canonical-json-editing/`](.claude/skills/canonical-json-editing/) | A Claude Code skill defining how canonical JSON documents are edited: jq-only mutation, canonical form, explicit local linting |
| [`.claude/skills/add-governed-doctype/`](.claude/skills/add-governed-doctype/) | A Claude Code skill for bringing a new document type (findings, scenarios, assumptions) under JSON-schema governance and linting |
| [`.claude/skills/self-retrospective/`](.claude/skills/self-retrospective/) | A Claude Code skill that harvests session knowledge into a structured retrospective (report, skill specs, ADR drafts, agents-file rules) before it's lost to context truncation |
| [`.claude/skills/adr/`](.claude/skills/adr/) | A Claude Code skill for authoring and maintaining Architecture Decision Records at `docs/adr/`, with a link checker and canonical template |
| [`.claude/skills/human-scoped-deliverables/`](.claude/skills/human-scoped-deliverables/) | A Claude Code skill that calibrates human-facing deliverables (summaries, overviews, explainers) for this repository's human reader |

## Relationship to the platform repository

The platform repository (`k8s-platform`) owns the implementation, the
requirements, and the documentation source. This repository owns the
scenarios, their harness, and the findings. The two meet only at the
published docs site and at findings filed as issues.

Start with [`charter.md`](charter.md) — it is deliberately self-contained,
since scenario-writing sessions must not see the platform repository at all.
