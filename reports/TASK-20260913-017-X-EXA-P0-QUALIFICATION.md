# TASK-20260913-017 — X Search P0 Qualification via Exa

```text
task_id: TASK-20260913-017
status: X_SEARCH_DEFERRED_BY_GOAL_INTEGRITY (Outcome B — 0/2 fixtures)
parent: TASK-20260912-001
predecessor: TASK-20260913-016
branch: task/20260912-001-v04-capability-diagnostics
receipt: evidence/TASK-20260913-017-x-exa-p0.json
```

## What this task did

One tiny, bounded qualification of the anonymous Exa hosted MCP as a
replacement for only the missing `x.search` leg, run from the mainland host
with no proxy and no new credentials. This is the final X task in the current
roadmap slice; it closes the X workstream regardless of outcome.

## Control and frozen fixtures

Control read (existing XActions, read-only, production session consumed
in-process only): `getTweets('zcode_ai', 5)` returned the same 5 real posts as
TASK-013/014/016 — timeline and known-post read remain healthy.

Two frozen fixtures with different Post IDs:

```text
F1  expected 2098396306750517317 (zcode_ai)
    query: zcode_ai "WEEKEND BUILD V" "300M tokens" x.com
F2  expected 2092635718766215590 (zcode_ai)
    query: ZCode GLM-5.3-Flash multimodal GLM-5 launch x.com
```

The search tool schema exposes only `query` / `numResults` / `objective` (no
domain-restriction field), so the site constraint was encoded in the query.

## Result — 0/2 fixtures pass

| | F1 | F2 |
|---|---|---|
| result blocks inspected | 8 | 10 |
| x.com/twitter.com status URLs among them | **0** | **0** |
| expected Post ID in first 10 results | no | no |
| provider-side fetch of canonical status URL | **SOURCE_NOT_AVAILABLE** | **SOURCE_NOT_AVAILABLE** |
| date metadata observed (Exa-provided) | 2026-09-11T14:35:37Z | 2026-08-26T00:00:00Z |

Exa's web index returned results for both queries (including publication
dates), but **none of the 18 inspected results contained a canonical or
canonicalizable status URL**, and its fetcher cannot read the canonical status
pages at all (`SOURCE_NOT_AVAILABLE`). Material post text therefore could not
be established from search or provider-side fetch for either fixture.

Probe correction disclosed: the first probe execution sent JSON-RPC
`tools/call` with `id: null` (treated as a notification — empty responses),
a probe runtime error corrected to numeric request ids; the single corrected
run is the qualification evidence. No quality/coverage retries were made and
no investigation of why Exa misses the posts was performed, per contract.

## Outcome B — deferred by Goal Integrity

```text
x.search remains unresolved
the gap is explicitly deferred by Goal Integrity
existing XActions timeline/known-post read remains preserved
terminal state: X_SEARCH_DEFERRED_BY_GOAL_INTEGRITY
```

Per the contract's stop rule: no SocialData, official X API, TwitterAPI.io,
OpenCLI, Android GraphQL, another CLI, or another search provider was
evaluated or staged, and no successor X task is created automatically. The
Human may reopen X search later if it becomes decision-critical.

## Final X capability state (unchanged from TASK-016)

```text
x.account.timeline -> existing vpsmanage / XActions (healthy)
x.post.read        -> existing vpsmanage / XActions (healthy)
x.search           -> unresolved; deferred by Goal Integrity
```

## Production / cleanup

Production X monitoring untouched and verified after probes (Mihomo active,
`gate-d-poller.timer` active, production session hash `598f3b16…` unchanged).
Host probe scripts removed (residue 0); local temp key copy removed.
`CLEAN_VERIFIED`.

## Stop

Pushed report/receipt; Issue #2 synchronized. This closes the current X
workstream. Stopping at the terminal state:

```text
X_SEARCH_DEFERRED_BY_GOAL_INTEGRITY
```
