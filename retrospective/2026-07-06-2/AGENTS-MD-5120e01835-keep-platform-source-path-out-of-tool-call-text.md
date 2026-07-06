# agent instruction

**Keep the platform-source path out of tool-call text.** The docs-blindness hook scans the full text of Bash commands and other tool inputs. Never write the platform source repository's owner/repo path into a shell command, a commit message, or prose passed through a command argument — refer to it obliquely ("the platform source repository") instead. Content at rest in files is not scanned; only tool-call text is.

*Grounded in: the hook denying its own author's next Bash call minutes after installation.*

# justification

Within one minute of `.claude/settings.json` being written, the hook denied the very next Bash call — a `jq-edit` invocation whose `--arg` string described the hook and spelled out the forbidden path. The whole three-command chain died at PreToolUse, costing a full rewrite of the ledger-update text and a re-run; the subsequent commit message had to be reworded the same way. The failure mode recurs every time an agent writes *about* the boundary (ledger notes, commit messages, README prose piped through a command), which in a scenario-testing repository is constantly. The marginal cost of the rule is one oblique phrase instead of a literal path; the cost of not knowing it is a denied call and a confused retry loop every session, or — worse — an agent "fixing" the denial by weakening the hook.
