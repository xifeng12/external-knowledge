# TASK-20260913-014 — X Provider Repair / Dynamic GraphQL Query-ID Resolution

```text
task_id: TASK-20260913-014
status: READY_FOR_X_PROVIDER_ALTERNATIVE_DECISION (Gate A failed: mechanism works, session tier does not)
parent: TASK-20260912-001
predecessor: TASK-20260913-013
branch: task/20260912-001-v04-capability-diagnostics
receipt: evidence/TASK-20260913-014-x-provider-repair.json
```

## What this task did

Gate A validated the current authoritative XActions upstream
(`github.com/nirholas/xactions` @ `f2fb3ed2d052838578e68a224eccc2cbaebcb7ca`,
committed 2026-09-06) in a task-owned isolated runtime on the mainland host,
against the same fixtures that failed in TASK-013 — with production
`/opt/xactions-poc` strictly read-only and the existing session consumed only
in-process.

## 1. The dynamic query-ID mechanism is real and works

The upstream HEAD (version string still `3.5.0`, but content materially differs
from the installed npm copy, which has no dynamic machinery) contains exactly
what the task contract described:

```text
src/scrapers/twitter/http/queryIds.js      discoverQueryIds() / refreshQueryIds()
src/scrapers/twitter/http/client.js:429    stale-ID auto-recovery wiring
src/scrapers/twitter/http/x-endpoints.generated.js
                                           generated queryId table (fa0311
                                           TwitterInternalAPIDocument, 2026-08-27 sync)
```

A live discovery run through the existing Mihomo path succeeded:

```text
entryUrl     https://x.com/home
mainBundle   https://abs.twimg.com/responsive-web/client-web/main.59435dbf6f40166da.js
discovered   148 operations, 11/11 chunks, 2,089,648 bytes, 0 failures
SearchTimeline discovered ID   KPSo2_UWdOMpPJwjhfT1Qg  (fresh, from x.com's own bundle)
generated-table ID             hyPfJYJ_XAtDYoslQc-Rgg  (2026-08-27 - already stale)
installed static ID            flaR-PUMshxFWZWPNpq4zA  (dead - TASK-013's 404)
provenance                     discovered/cache/live-resolution; NOT a hand-pinned ID
```

## 2. But search still fails — and the differential isolates why

```text
X1 searchTweets('from:zcode_ai')  -> bare HTTP 404 (one 403 observation mid-flow)
X2 searchTweets('ZCode')          -> bare HTTP 404
X3 getTweets('zcode_ai', 5)       -> PASS (5 real posts; same IDs as TASK-013)
```

A search request intercepted mid-flight used the **fresh live-discovered ID**
(`KPSo2_UWdOMpPJwjhfT1Qg`) and still returned 404 — the query-ID staleness is
no longer the blocker.

The decisive differential matches the upstream project's own documented
diagnostic (`doctor.js:148`):

> "X treats a session without ct0 as logged out, so **search, followers and
> DMs all fail with a bare 404**" (while timeline reads keep working)

Observed on both runtimes, same session file:

| Probe | upstream clone @ f2fb3ed | production 3.5.0 |
|---|---|---|
| `getTweets` (timeline, auth_token-tier) | PASS | PASS |
| `getFollowers` (full-session-tier) | **bare 404** | **bare 404** |
| `searchTweets` (full-session-tier) | **bare 404** | bare 404 (TASK-013) |

The client-side flags (`_isLoggedIn`, `_authenticated`) are `true`, but they
only prove a ct0-*shaped* cookie is present — X's server-side verdict is the
bare 404 on the full-session endpoint class. The stored session (~2026-09-07
vintage) has been rotated/invalidated server-side for search/followers/DMs,
while timeline and single-post reads (auth_token-tier) remain healthy.

## 3. Gate A verdict and stop state

```text
Gate A: FAIL — the upstream dynamic mechanism is operational, but the
        upstream runtime still cannot search.
Gate B: NOT ENTERED — no vpsmanage repair branch or PR was created
        (contract permits Gate B only after a Gate A pass).
```

Per the contract's Gate A failure rule, the X leg stops at:

```text
READY_FOR_X_PROVIDER_ALTERNATIVE_DECISION
```

No browser fallback, second provider, or cookie handling was attempted — all
forbidden.

## 4. Decision surface for the Human

1. **Primary**: refresh/re-verify the server-side X session (an Owner
   credential action — upstream's documented fix is its interactive
   `xactions connect` capture; equivalent: re-supply `/opt/xactions-poc/
   x-session.json` with a fresh `auth_token` + `ct0` pair). This is outside
   Agent authorization. After a fresh session, the same X1–X4 fixtures can be
   re-run; if they pass, the already-proven dynamic query-ID machinery
   (`f2fb3ed`) becomes the natural Gate B absorption candidate and this task's
   successor can complete the vpsmanage repair PR.
2. **Secondary**: if a refreshed session still bare-404s on search, the account
   itself may be search-restricted — that is a provider-level alternative
   decision, not a code repair.

## 5. Production safety / secrets / cleanup

- `/opt/xactions-poc` untouched (no hot-patching, no package replacement);
  Mihomo and `gate-d-poller.timer` never restarted; verified active after all
  probes.
- No private-key, cookie, or session values printed or committed; session
  consumed only in-process; `E:\cs\key` untouched (ACL-restricted temp key
  copies used for SSH batches, deleted after each).
- Host cleanup verified: `/tmp/xrepair-t14` (clone + task-owned
  `XACTIONS_HOME` cache) and all probe scripts removed; no stray `~/.xactions`.
  Two pre-existing unrelated files matching the pattern (`/tmp/act14.json`,
  `/tmp/act14b.json`) are not task-owned and were left untouched.
  `CLEAN_VERIFIED`.
- vpsmanage: read-only usage only; zero mutations.

## Stop

Pushed receipt/report; Issue #2 synchronized. Stopping at the first accurate
terminal state:

```text
READY_FOR_X_PROVIDER_ALTERNATIVE_DECISION
```
