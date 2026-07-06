# agent instruction

**Clean up scheduled check-ins when their PR closes.** If you armed a send_later self check-in to watch a pull request, delete the trigger the moment the PR merges or closes. Orphaned triggers fire into finished work and waste a wake-up on nothing.

*Grounded in: deleting the armed check-in triggers after PR #1 and PR #2 merged.*

# justification

Both PRs in this session had hourly self check-ins armed (webhooks do not deliver CI success or merge transitions, so the check-ins are necessary while a PR is open). Both were deleted at merge time — the second one seconds after the merge call returned. The first deletion attempt hit a transient tool failure and had to be retried after an MCP reconnect, which is exactly why the rule needs stating: the cleanup is easy to drop when it errors once, and an orphaned trigger then fires into a merged PR, wakes a session with no work to do, and — if the firing session lacks context — can generate a confused status message to the owner. Cost of the rule: one delete_trigger call per merged PR. Cost without it: a phantom wake-up per orphan per hour.
