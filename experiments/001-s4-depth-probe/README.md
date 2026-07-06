# Experiment 001 — S4 depth probe

One docs-blind agent tried to write scenario S4 (tenant developer deploys
a stateless web app from a git repo via GitOps) at L1, from the published
docs site alone. This README says how the probe was built and what came
back; `probe-output.json` is the agent's own record, kept verbatim.
Nothing here is triaged yet — that happens with the owner.

## The question

Can the published documentation, by itself, carry a scenario author all
the way to a full L1 write — actor, preconditions, cited prose steps,
observable outcome, defect classes — and what does it fail to provide?
S4 was chosen deliberately as the best-documented path (the sole tutorial
plus a how-to), so gaps found here bound everything else. The owner's
recorded prediction: **5–10 immediate documentation findings** from this
single write.

## Result at a glance

**15 candidate findings against the predicted 5–10.** The prediction was
exceeded, and exceeded on the best-documented path in the corpus.

| Candidate class | Count |
|---|---|
| Missing facts (needed, not findable in the docs) | 12 |
| Blocked (could not proceed as a self-service tenant) | 1 |
| Platform facts the agent was forced to guess | 2 |
| **Total candidates** | **15** |

The other assumption classes (4 tool-knowledge, 3 judgment) are not
counted as candidates — they are the expected cost of any docs-only
write, not documentation defects.

The headline is the *shape*, though, not the count: the deploy mechanics
themselves documented out almost completely — the probe produced a full
seven-step L1 with a citation (url + heading + exact quote) on every
step, five preconditions, an observable outcome with the docs' own
"HTTP 200 over verified TLS" oracle, and eleven defect classes. The gaps
cluster *around* the path, not on it:

- **Access** — the one hard block: every verification step needs kubectl
  read access, the docs name "No human kubectl access path" as a gap,
  and the only access guide is marked contract-stability ("do not
  automate against it"). The probe proceeded by assuming operator-granted
  access out of band.
- **Discovery** — which spoke clusters exist, their short names and
  subdomains, and even *which repository is "the platform repository"*:
  its URL appears only as an example value inside ApplicationSet YAML,
  never stated as a fact — and spelled `k8-platform` where the docs site
  path says `k8s-platform`.
- **Scoping** — the documented deployment unit targets *every* registered
  spoke, while the deploy how-to's precondition says "you know which
  cluster you're deploying to"; no documented way to pin an app to one
  cluster.
- **Operational contracts** — no onboarding request flow, no PR
  review/merge expectations, no end-to-end latency bound a scenario
  could use as a timeout, no namespace-collision rule between tenants.

## How the probe was constructed

One fresh general-purpose subagent, launched with a prompt containing
only: the role (tenant application developer), the S4 bullet verbatim
from the brainstorm, the docs site root URL as its sole information
source, the recording rules (cite every step; missing facts are the
product; type every assumption tool-knowledge / platform-fact /
judgment; record blocks and continue), and a loose output shape to
return as raw JSON. It was told not to read this repository's files and
not to fetch anything outside the docs site. The docs-blindness hook
(ledger item T-002) was live for the whole run — its self-test passed
19/19 immediately before launch — so isolation was enforced, not
promised.

## Integrity notes on the record

- `probe-output.json` is the agent's final message byte-for-byte, with
  two disclosed exceptions: (1) a one-sentence prose preamble before the
  JSON was dropped, and (2) the message stopped one byte short of
  well-formed — mid-object, after the final `notes` string — so the
  single terminating `}` was appended. Everything inside the braces is
  untouched.
- The agent itself flags that its quotes were extracted via a
  summarizing fetch tool: **verify exact wording against the live pages
  before filing any finding.** One suspected doc nit (the tutorial
  saying "four files" where five appear) needs that check first.

## What happens next

Triage (ledger item T-005, pending) reads this output with the owner,
extracts real draft findings from the candidates, and compares against
the prediction properly. Those drafts then seed the findings schema with
observed shapes instead of speculation. Per the experiments/ convention,
everything in this directory is throwaway once that hardening exists.

Ledger: T-004 (this probe), T-005 (triage), T-002 (the boundary hook).
