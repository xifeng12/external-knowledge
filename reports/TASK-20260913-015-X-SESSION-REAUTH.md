# TASK-20260913-015 — X Session Re-auth Discrimination

```text
task_id: TASK-20260913-015
status: X_PROVIDER_ALTERNATIVE_REQUIRED (Outcome B)
parent: TASK-20260912-001
predecessor: TASK-20260913-014
branch: task/20260912-001-v04-capability-diagnostics
receipt: evidence/TASK-20260913-015-x-session-reauth.json
```

## Question this task answered

With exactly one fresh Human-assisted X session, does the full-session endpoint
class (search / followers) come back in the already-validated HTTP-only
XActions runtime?

**Answer: no.** The fresh session behaves identically to the old stored session
on every probe. This is Outcome B. Per the contract, XActions search hardening
stops in this project, and the next decision is a provider-alternative
comparison. No root-cause speculation is recorded.

## Phase 1 — capture

The preferred local `xactions connect` path was infeasible without forbidden
network changes: the workstation's local proxy was not running and x.com is
transport-unreachable directly. The Human chose the contract's allowed
alternative: a manually supplied browser cookie export
(`E:\cs\external-knoedge-skill\cookie.txt`, JSON array of 8 cookies). Only the
two required cookies (`auth_token`, `ct0`) were extracted in-process into a
normalized two-cookie session file; values were never printed, logged, or
recorded. The file was transferred to a task-owned server path (`600 root`)
and deleted at cleanup, along with the local normalized copy and the
Human-provided source file.

Freshness criteria met: captured during the task; both cookies present;
not copied from the production session file.

## Phase 2 — discrimination probes (isolated runtime @ f2fb3ed)

Dynamic query-ID discovery re-ran live in a fresh task-owned cache: 148
operations from x.com's own bundle, SearchTimeline ID `KPSo2_UWdOMpPJwjhfT1Qg`
(discovered/cache/live-resolution — no hand-pinned ID).

| Probe | Fresh session | Old session (control) |
|---|---|---|
| S0 identity (`scraper.me()`) | **indeterminate** | **indeterminate** (control — same failure) |
| S1 `searchTweets('from:zcode_ai')` | **bare 404** | bare 404 (TASK-013/014) |
| S2 `searchTweets('ZCode')` | **bare 404** | bare 404 |
| S3 `getFollowers` differential | **bare 404** | bare 404 (TASK-014) |
| S4 `getTweets` timeline control | **PASS** (5 posts) | PASS |
| S5 `getTweet` canonical read | **PASS** (`https://x.com/zcode_ai/status/2098396306750517317`, 297-char body) | PASS |

S0 notes, recorded honestly: the runtime's identity check (`me()`) fails with
"Cannot determine authenticated user ID" for **both** sessions — the identity
lookup itself sits in (or depends on) the failing endpoint class, so it cannot
discriminate session quality. Session acceptance is instead evidenced by S4:
UserTweets is a documented login-required endpoint (vpsmanage Gate C proved a
guest session cannot pull timelines), and the fresh session pulls it normally.
The fresh session is therefore as authenticated as the historically validated
old session — and reproduces its failure signature exactly.

Retry discipline: one primary call per probe; the only retries were the S0
probe-implementation fix (probe runtime failure, permitted) and the me()
control on the old session; no authorization-shaped error was retried; no
second session was captured.

## Conclusion (Outcome B)

```text
fresh session did not restore the full-session endpoint class under this
account/provider/runtime envelope
```

Cookie freshness/pairing is thereby eliminated as the variable — a freshly
captured, login-gated-accepted session reproduces the class failure exactly.
The contract forbids further explanation-seeking loops; the only narrowing
recorded is that the remaining hypotheses are account state or an X-side
authentication-policy change for this envelope, neither of which is proven
here.

## Consequences

- `x.semantic` availability is **not** claimed; capability-map is unchanged
  (contract allows a map note only for Outcome A).
- XActions search hardening **stops** in this project.
- Next decision surface (a separate task): bounded provider alternatives, e.g.
  the existing browser-session surface / OpenCLI, a maintained HTTP/session
  client, or a legitimate provider-side remote X read surface. Nothing is
  installed or authenticated in this task.

## Production / secrets / cleanup

- Production untouched and proven unchanged: `x-session.json` sha256
  `598f3b16…` identical before/after; Mihomo and `gate-d-poller.timer` active
  throughout; no service restarts; no network changes.
- No cookie values, account identity, or key material printed or committed.
- Cleanup `CLEAN_VERIFIED`: host fresh-session file, probe scripts, and the
  isolated runtime (clone + cache) removed (residue grep = 0); local normalized
  session copy, temp SSH-key copies, and the Human-provided `cookie.txt`
  deleted.

## Stop

Pushed report/receipt; Issue #2 synchronized. Stopping at the first accurate
terminal state:

```text
X_PROVIDER_ALTERNATIVE_REQUIRED
```
