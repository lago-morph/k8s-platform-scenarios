# agent instruction

**Restart the designated branch from main after its PR merges.** When the pull request for your working branch has merged, do not stack follow-up commits on the merged history. Run `git fetch origin main` then `git checkout -B <branch> origin/main`, and open a NEW pull request for the follow-up work. Reusing the merged branch or building on its old tip pollutes the next PR's diff with already-merged commits.

*Grounded in: restarting the branch from main after PR #3 merged, before writing this retrospective.*

# justification

This repository advances through a sequence of small, ledger-driven PRs off `main`, and this session produced two of them in a row: the T-004 depth probe (PR #3), then the retrospective as follow-up work. After PR #3 merged, continuing on the same branch tip would have carried the already-merged probe commits into the retrospective's diff, making the second PR unreviewable. Fetching main and `checkout -B`-ing the branch onto it kept each PR's diff to exactly its own work. The marginal cost is two git commands between PRs; the cost of skipping them is a follow-up PR whose diff is contaminated with a prior PR's history — a recurring hazard given the repo's many-small-PRs cadence.
