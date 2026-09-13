# TASK-20260913-016 — X Session Verifier Discrimination

```text
task_id: TASK-20260913-016
status: X_PROVIDER_ALTERNATIVE_REQUIRED (Outcome B, with a contract-valid S0 PASS)
parent: TASK-20260912-001
predecessor: TASK-20260913-015 + its review correction
branch: task/20260912-001-v04-capability-diagnostics
receipt: evidence/TASK-20260913-016-x-session-verifier.json
```

## What this task fixed and then answered

The TASK-015 review correctly rejected that run's Outcome B because its S0
verifier (`Scraper.me()`) structurally requires a `twid` cookie that the
authorized two-cookie session shape cannot provide. TASK-016 replaced the
verifier and re-ran the discrimination exactly once.

### S0 — a valid, differential, session-only verifier

Verifier: **HomeTimeline GraphQL (GET)**, built entirely through the pinned
runtime's own machinery — `resolveOperation('HomeTimeline')` from the live
discovery cache (no hand-pinned ID), `buildGraphQLUrl` + `DEFAULT_FEATURES`
from the client api layer, issued via the Scraper's `SimpleHttp` (auth headers
+ cookies). Minimal task-owned probe per the contract; no browser automation.

```text
S0-GUEST  no cookies
          -> authorization-shaped REJECTION (HTTP 404; the runtime's own
             failure text states X restricts HomeTimeline to logged-in sessions)
S0-FRESH  exactly the one fresh Human-provided auth_token + ct0 pair
          -> ACCEPTED, structurally valid authenticated response
             (bounded entry count: 37; no timeline content recorded)

S0 PASS   = true   (differential; verifier independent of S1/S2/S3 and of twid)
```

Discovered HomeTimeline queryId: `Dw2wl35E3OV4X6UlEAf0bg` (provenance: cache /
live discovery — 148 operations from x.com's own bundle, 11/11 chunks).

### Phase 3 — final discrimination under the verified session

| Probe | Fresh (S0-verified) session |
|---|---|
| S1 `searchTweets('from:zcode_ai')` | **bare 404** (authorization-shaped) |
| S2 `searchTweets('ZCode')` | **bare 404** (authorization-shaped) |
| S3 `getFollowers` differential | **bare 404** (authorization-shaped) |
| S4 `getTweets` timeline control | PASS (5 posts) |
| S5 `getTweet` canonical read | PASS (`https://x.com/zcode_ai/status/2098396306750517317`) |

## Conclusion (Outcome B — now contract-valid)

```text
A fresh session is independently accepted by X for a session-only endpoint,
but the required X search/followers capability still fails under the same
account/provider/runtime envelope.
```

This is the first discrimination run where the session was verified by a
genuine session-only differential gate before the failing probes, satisfying
the exact Outcome B precondition the TASK-015 review required. Per Goal
Integrity:

```text
STOP all further XActions search/session/query-ID hardening in this project.
```

`x.semantic` availability is not claimed; capability-map is unchanged (map
note allowed only for Outcome A). No root-cause speculation is recorded. The
next task may compare bounded provider alternatives; TASK-016 stages none.

## Human source file / production / cleanup

- Human-provided `E:\cs\external-knoedge-skill\cookie.txt` treated as
  READ-ONLY INPUT: read baseline recorded (3208 bytes, sha256 `97135a32…`),
  verified **exists unchanged** after the task; never deleted, truncated,
  overwritten, renamed, or moved. (The TASK-015 deletion of the previous
  source file is acknowledged as an over-deletion in that task's review.)
- Only task-owned derived copies were deleted: host fresh-session file, probe
  script, isolated runtime + cache (residue grep = 0); local derived session
  copy and temp SSH-key copies deleted.
- Production proven unchanged: `/opt/xactions-poc/x-session.json` sha256
  `598f3b16…` identical; Mihomo and `gate-d-poller.timer` active throughout.
- No cookie values, private timeline content, or account identity recorded.

## Stop

Pushed report/receipt; Issue #2 synchronized. Stopping at the first accurate
terminal state:

```text
X_PROVIDER_ALTERNATIVE_REQUIRED
```
