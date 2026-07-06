# agent instruction

**Founding-document claims about platform state are not evidence.** The charter and brainstorm may assert platform facts (for example, a scenario "already at L4"). Do not propagate such claims into scenario or ledger records unless they are verifiable from the published documentation; an unverifiable claim is finding material, not fact.

*Grounded in: the owner rejecting the founding claim that the rebuild scenario was already at L4 — no rebuild documentation exists.*

# justification

The brainstorm document states that scenario S1 (rebuild the platform from nothing) is "already at L4 — this is the existing clean-build loop." The agent repeated that claim in a design recommendation; the owner rejected it flatly: as a user, he has no documented way to rebuild, no owner-facing status surface, no remediation story — so by the corpus's own maturity definitions the scenario cannot be past L0, and the founding claim itself is a likely documentation bug. The subtlety that makes this rule necessary: the charter is an *allowed source* under the docs-blindness contract, so nothing mechanical stops the contamination — the claim rode in through a legitimate channel. The rule costs one verification question per inherited claim ("which docs page supports this?"). Without it, the corpus's baseline data is polluted by the very repository that defines its rules.
