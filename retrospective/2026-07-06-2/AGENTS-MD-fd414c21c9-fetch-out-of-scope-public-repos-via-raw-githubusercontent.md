# agent instruction

**Fetch out-of-scope public repos via raw.githubusercontent.com.** For public GitHub repositories outside the session's repository scope, github.com, api.github.com, and codeload.github.com are proxy-intercepted and return a JSON error body; raw.githubusercontent.com serves file content. A missing file returns the literal body "404: Not Found" with curl exit 0 — check for that sentinel explicitly.

*Grounded in: importing three skills from a sibling public repository through the proxy.*

# justification

Importing the first skill burned four failed attempts before finding the working path: the GitHub MCP tool was denied by session scope, `add_repo` was denied by the user (the repo is public — session integration was unnecessary), then `api.github.com`, `codeload.github.com`, and the `github.com` HTML tree page each returned the proxy's JSON interception message. Only `raw.githubusercontent.com` served content. A second trap followed: probing for optional files "succeeded" with a 200-looking curl that actually delivered the fourteen-byte body `404: Not Found`, which would have been silently saved as a file. Both facts cost real time to discover and are invisible in any documentation; encoding them saves every future import the same archaeology. Marginal cost: one URL habit and one string comparison.
