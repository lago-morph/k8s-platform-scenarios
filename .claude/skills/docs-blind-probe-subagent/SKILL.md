---
name: docs-blind-probe-subagent
description: Construct and run ONE fresh docs-only subagent that attempts an L1 scenario write from the published documentation alone, so the facts the docs cannot supply become the product. Use for docs-blindness scenario work — the depth probe (ledger T-004), the breadth sweep (T-024), batch L1 authoring (T-029), or any "write scenario SNN from the docs" task. Core rules — verify the docs-blindness boundary hook is active before launching; give the subagent ONLY its role, the scenario bullet verbatim, the docs root URL as sole source, an output shape, and the recording discipline (cite every step; missing facts and blocks are the product; type every assumption); keep each probe isolated from every other; capture the output verbatim and count candidate findings, but do NOT file findings (triage is owner-in-the-loop). Triggers on "docs-only probe", "L1 write from the docs alone", "docs-blind scenario write", "gap-probe scenario SNN".
---

# Skill: docs-blind-probe-subagent

This repository authors platform scenarios **exclusively** from the
published documentation (the docs-blindness contract in `charter.md`). It
does so by dispatching a fresh subagent that may read only the docs site.
This skill constructs that subagent so isolation is pure and the output is
diagnostic: the gap list — not the scenario — is the product.

The pattern was executed for scenario S4 (ledger T-004) and recurs for the
breadth sweep (T-024) and batch L1 authoring (T-029). It pairs with the
`capture-subagent-structured-output` skill, which saves the return
faithfully.

## When to use

- Describing or gap-probing a scenario at L1 under the docs-blindness
  contract — from a single bullet in `scenario-brainstorm.md`.

Do **not** use it for work that legitimately reads the platform source
(there is none in this repo) or for non-scenario research.

## Inputs

- The **role** being exercised (e.g. tenant application developer).
- The **scenario bullet**, verbatim from `scenario-brainstorm.md`.
- The **published docs root URL** — the ONLY allowed information source
  (`https://lago-morph.github.io/k8s-platform/`).
- The desired **output shape** (loose; do not over-constrain).

## Outputs

- ONE subagent's raw JSON: actor, preconditions, steps with per-step
  citations (url + heading + exact quote), observable outcome, defect
  classes, plus `missing_facts[]`, typed `assumptions[]`, `blocked[]`.
- That output saved verbatim under `experiments/NNN-<name>/`, plus a
  README with the candidate-finding count against any prediction.

## Workflow

1. **Verify the boundary is live before launching.** Run
   `scripts/hooks/test-deny-platform-source` and confirm all cases pass.
   The hook denies any tool call referencing the platform source
   repository, and it applies to the subagent's own tool calls in-session
   — so isolation is *enforced*, not promised. Launching without this
   check means the blindness is a request, not a guarantee.
2. **Fill the prompt template** at
   `resources/probe-prompt-template.md`: substitute the role, the
   scenario bullet verbatim, the docs root URL, and the scenario id.
3. **Launch exactly ONE fresh general-purpose subagent** with that filled
   text as its entire prompt. One scenario per subagent: per-scenario
   isolation keeps one scenario's docs reading from coloring another's.
4. **Put nothing else in the prompt** — no repository files, no prior
   probe output, no platform knowledge of your own. The whole point is
   what the docs *alone* yield; anything you add hides a gap.
5. **On return, capture verbatim** with the
   `capture-subagent-structured-output` skill into
   `experiments/NNN-<name>/probe-output.json`.
6. **Count candidate findings** = `missing_facts` + `blocked` +
   `platform-fact` assumptions. Record the count in the experiment README
   next to any prior prediction. (`tool-knowledge` and `judgment`
   assumptions are the expected cost of a docs-only write, not
   candidates.)
7. **Do NOT file findings.** Triage into real finding records is a
   separate, owner-in-the-loop step (ledger T-005). The probe step ends
   at the counted candidates.

## Concrete examples

### Example 1: S4 (real)

Role `tenant application developer`; bullet "Deploy a stateless web
application from a git repo via GitOps. Objective: the minimum deploy
path is documented and works."; docs root the published site. The hook
self-test passed 19/19 at launch. The probe returned a full seven-step L1
with a url+heading+exact-quote citation on every step, five preconditions,
the docs' own "HTTP 200 over verified TLS" oracle, and eleven defect
classes — plus 12 `missing_facts`, 9 typed assumptions, 1 `blocked`.
Candidates = 12 + 1 + 2 platform-fact = **15**, recorded against the
owner's predicted 5–10. No findings were filed.

### Example 2: an adversary scenario (illustrative)

Role `adversary`; bullet "Tenant deploys from a repository outside the
allowed set. Objective: the GitOps trust boundary holds."; same docs
root. The probe surfaces whether the trust-boundary denial is documented —
recording the denial surface as a citation if the docs describe it, or the
absence as a `missing_fact` if they do not. It never sees the S4 probe's
output: isolation stays pure.

## Anti-patterns

- **Enriching the prompt with facts the docs do not state.** The omission
  IS the finding; supplying the fact hides the gap.
- **Letting one probe read another's output.** Cross-contamination
  destroys the per-scenario isolation the gap map depends on.
- **Skipping the hook self-test.** Without it, blindness is prose, not
  enforcement.
- **Fetching anything outside the docs root**, or naming the platform
  source repository in a tool call — the boundary hook denies it, and it
  breaks the contract.
- **Filing findings from the raw output.** Triage is owner-in-the-loop
  (T-005); the probe only counts candidates.

## Acceptance criteria

- [ ] The subagent prompt contained only the five allowed inputs.
- [ ] `scripts/hooks/test-deny-platform-source` passed immediately before
      launch.
- [ ] Exactly one subagent ran for the scenario; it read only the docs
      site.
- [ ] Output was captured verbatim under `experiments/`.
- [ ] The candidate-finding count was recorded against the prediction.
- [ ] No findings were formally filed by the probe step.

## Files

- `resources/probe-prompt-template.md` — the fill-in-the-blanks probe
  prompt (role, scenario bullet, docs root, output shape, recording
  discipline).
