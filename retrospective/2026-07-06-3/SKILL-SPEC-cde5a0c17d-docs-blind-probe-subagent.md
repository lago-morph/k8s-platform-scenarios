# Spec: `docs-blind-probe-subagent`

- **ID**: SKILL-SPEC-cde5a0c17d
- **Source retrospective**: ../2026-07-06-3.md

## Intent

This repository authors platform scenarios exclusively from published documentation, and does so by dispatching a fresh subagent that may read only the docs site. This skill constructs that subagent's prompt so isolation is pure and the output is diagnostic: it hands the agent only its role, the scenario bullet verbatim, the docs root URL as sole source, an output shape, and the recording discipline that makes the gap list — not the scenario — the product (cite every step with url+heading+exact quote; every needed-but-absent fact goes to missing_facts; every forced assumption is typed tool-knowledge/platform-fact/judgment; blocks are recorded and the agent continues). It earns its place because the ledger's breadth sweep (T-024) and batch L1 authoring (T-029) will each launch this same shape many times, and a probe prompt that leaks context or drops the recording rules produces a scenario that looks authored but proves nothing.

## Trigger

Activate when authoring or gap-probing a platform scenario under the
docs-blindness contract — the ledger's depth probe (T-004), breadth
sweep (T-024), or batch L1 authoring (T-029). Direct phrases: "run a
docs-only probe for scenario SNN", "L1 write from the docs alone",
"docs-blind scenario write". Proactive: any time a scenario is to be
described from the published docs. Negative triggers: work that
legitimately reads the platform source (there is none in this repo);
non-scenario research.

## Inputs

- The role being exercised (e.g. tenant application developer).
- The scenario bullet, verbatim from `scenario-brainstorm.md`.
- The published docs root URL — the ONLY allowed information source.
- The desired output shape (loose; do not over-constrain).

## Outputs

- ONE subagent returning raw JSON: actor, preconditions, steps with
  per-step citations, observable outcome, defect classes, plus
  `missing_facts[]`, typed `assumptions[]`, and `blocked[]`.
- The output captured verbatim under `experiments/` (use the
  `capture-subagent-structured-output` skill).

## Workflow

1. Confirm the docs-blindness boundary hook is active — run
   `scripts/hooks/test-deny-platform-source` and expect all-pass —
   BEFORE launching, so isolation is enforced, not promised.
2. Launch ONE fresh general-purpose subagent (fresh context; no shared
   history with prior probes).
3. Its prompt contains ONLY: the role; the scenario bullet verbatim;
   the docs root URL as sole source with an explicit "fetch nothing
   else, read no repository files" constraint; the loose output shape;
   the recording discipline (step 4).
4. State the recording discipline in the prompt: every step cites
   url + heading + a short exact quote; every needed-but-absent fact →
   `missing_facts` (this list is the product); every forced assumption
   is typed `tool-knowledge` / `platform-fact` / `judgment`; if blocked,
   record `{at_step, reason}` and continue with whatever else the docs
   support.
5. Do NOT enrich the prompt with repository context, prior probe
   outputs, or your own knowledge of the platform — the point is what
   the docs alone yield.
6. On return: capture verbatim; count candidate findings =
   `missing_facts` + `blocked` + `platform-fact` assumptions; record the
   count against any prior prediction; do NOT file findings — triage is
   a separate, owner-in-the-loop step.

## Concrete examples

### Example 1: S4 (real)

Role tenant-dev; bullet "Deploy a stateless web application from a git
repo via GitOps. Objective: the minimum deploy path is documented and
works."; docs root the published site. The probe returned a full
seven-step L1 with a url+heading+exact-quote citation on every step,
five preconditions, the docs' own "HTTP 200 over verified TLS" oracle,
eleven defect classes — plus 12 `missing_facts`, 9 typed assumptions,
and 1 `blocked`. Candidate findings = 12 + 1 blocked + 2 platform-fact
assumptions = 15, recorded against the owner's predicted 5–10.

### Example 2: an adversary scenario (illustrative)

Role adversary; bullet "Tenant deploys from a repository outside the
allowed set. Objective: the GitOps trust boundary holds."; same docs
root. The probe is expected to surface whether the trust-boundary denial
is documented — recording the denial surface as a citation if the docs
describe it, or the absence as a `missing_fact` if they do not. Either
way the isolation is pure: this probe never sees the S4 probe's output.

## Anti-patterns

- **Enriching the prompt with facts the docs do not state.** The
  omission IS the finding; adding the fact hides the gap.
- **Letting one probe read another's output.** Per-scenario isolation
  must stay pure or one scenario's reading colors another's assessment.
- **Filing findings from the raw output.** Triage is owner-in-the-loop
  (ledger T-005); the probe step only counts candidates.
- **Skipping the hook self-test.** Without it, isolation is promised in
  prose rather than enforced by the deny hook.
- **Fetching anything outside the docs root.** That breaks the
  blindness contract the whole corpus depends on.

## Acceptance criteria

- [ ] The subagent prompt contains only the five allowed inputs.
- [ ] The boundary hook was verified active immediately before launch.
- [ ] Output is captured verbatim under `experiments/`.
- [ ] The candidate-finding count is recorded against the prediction.
- [ ] No findings are formally filed by the probe step.

## Files this skill creates / modifies

- `experiments/NNN-<name>/probe-output.json` — the subagent's verbatim
  output.
- `experiments/NNN-<name>/README.md` — the probe question, how the
  probe was constructed, the candidate count vs the prediction, and
  integrity caveats.
