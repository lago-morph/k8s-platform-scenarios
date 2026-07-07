<!--
TEMPLATE: the prompt for ONE docs-blind scenario-probe subagent.
Fill in %%ROLE%%, %%SCENARIO_BULLET%% (verbatim from scenario-brainstorm.md),
and %%DOCS_ROOT_URL%% (the published docs site — the ONLY allowed source).
Pass the whole filled-in text as the subagent's prompt and NOTHING ELSE:
no repository context, no prior probe output, no platform knowledge of your own.
The subagent's own tool calls are individually hooked by the docs-blindness
boundary, so isolation is enforced per-call, not merely requested here.
-->

You are a %%ROLE%%.

Your scenario (verbatim): "%%SCENARIO_BULLET%%"

Your SOLE information source is the platform's published documentation
site, rooted at:
%%DOCS_ROOT_URL%%

Rules about sources:
- You may fetch pages under that docs site root only. Do not fetch any
  other URL and do not use web search.
- Do not read any files from the local repository or filesystem.
- Everything you write must either come from a fetched docs page (and be
  cited) or be explicitly recorded as an assumption or a missing fact.

Your task: attempt a FULL L1 scenario write for this scenario from the
docs alone. An L1 scenario consists of: actor, preconditions, prose
steps, observable outcome, and the defect classes it would catch.

Recording rules:
- Every step cites the doc page it came from: url + section heading + a
  short exact quote from that page.
- Every fact you need but cannot find in the docs goes in missing_facts.
  This list is the product — be specific and complete (one entry per
  distinct missing fact).
- Every assumption you are forced to make goes in assumptions, each with
  a type: "tool-knowledge" (general knowledge of tools such as git,
  kubectl, GitOps engines), "platform-fact" (something about this
  specific platform the docs did not tell you and you had to guess), or
  "judgment" (a reasonable-person call).
- If you cannot proceed at some point, record a blocked entry
  ({at_step, reason}) and continue with whatever else the docs support.

Return your result as raw JSON: your final message must be ONLY the JSON
object — no markdown fences, no surrounding prose. Suggested output shape
(loose — adapt as needed):
{ "scenario_id": "%%SCENARIO_ID%%", "role": ..., "objective": ...,
  "l1": { "actor": ..., "preconditions": [...],
          "steps": [{"n": 1, "text": ..., "citations": [{"url": ..., "heading": ..., "quote": ...}]}],
          "observable_outcome": ..., "defect_classes": [...] },
  "missing_facts": [...],
  "assumptions": [{"statement": ..., "type": ...}],
  "blocked": [{"at_step": ..., "reason": ...}],
  "notes": ... }
