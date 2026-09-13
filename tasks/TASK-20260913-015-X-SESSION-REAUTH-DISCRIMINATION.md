---
task_id: TASK-20260913-015
status: ready_for_owner_session_discrimination
parent_task: TASK-20260912-001
predecessor: TASK-20260913-014
target_repo: xifeng12/external-knowledge
reference_repo: xifeng12/vpsmanage
implementation_branch: task/20260912-001-v04-capability-diagnostics
capability: x.semantic
human_assisted_session_refresh_authorized: true
automatic_browser_cookie_db_read_authorized: false
production_session_replace_authorized: false
production_deployment_authorized: false
provider_alternative_staging_authorized: false
new_account_authorized: false
network_change_authorized: false
external_knowledge_merge_authorized: false
vpsmanage_merge_authorized: false
---

# TASK-20260913-015 — X Session Re-auth Discrimination

## Goal

Resolve the last decision-changing uncertainty in the X path with exactly one fresh Human-assisted X session:

```text
Does a freshly captured, X-verified auth_token + ct0 session restore the
full-session endpoint class (search / followers) in the already-validated
HTTP-only XActions runtime?
```

This is the final XActions discrimination task. It is not another code-repair round and not a provider tournament.

The result must choose between:

```text
fresh session restores full-session endpoints
  -> x.semantic may become AVAILABLE_WITH_SCOPE (test-stage)
  -> dynamic query-ID machinery remains the accepted XActions direction

fresh verified session still fails the same full-session class
  -> stop XActions search hardening
  -> X_PROVIDER_ALTERNATIVE_REQUIRED
```

Do not create a third explanation-seeking loop after this task.

## Accepted evidence

TASK-013 and TASK-014 already establish:

```text
existing mainland execution envelope:
  XActions HTTP client
  -> Mihomo 127.0.0.1:7890
  -> approved upstream
  -> X

healthy with existing stored session:
  getTweets('zcode_ai', 5) -> PASS
  getTweet(real numeric Post ID) -> PASS

full-session class with existing stored session:
  searchTweets(...) -> bare 404
  getFollowers(...) -> bare 404

TASK-014 dynamic query-ID validation:
  upstream SHA f2fb3ed2d052838578e68a224eccc2cbaebcb7ca
  live bundle discovery -> PASS
  148 operations discovered
  SearchTimeline ID obtained from live x.com bundle
  search with fresh live-discovered ID -> still bare 404
```

Therefore query-ID staleness is not the remaining blocker. The unresolved variable is the effective X session/authentication tier.

The current evidence supports only:

```text
full-session-tier requests are not being accepted as fully authenticated
```

It does NOT yet prove whether the cause is cookie freshness, cookie pairing, account state, or an X-side authentication-policy change.

## Source authority for fresh-session capture

Current upstream XActions provides `xactions connect`, which:

- opens a real Chrome window;
- requires the Human to log in interactively, including 2FA when applicable;
- waits until both `auth_token` and `ct0` exist;
- writes only those session cookies to an owner-only local file;
- performs its own X-side verification;
- does not transmit the cookies elsewhere by itself.

For this task, that flow is an allowed Human-assisted capture mechanism only.

Alternative allowed path: the Human may manually provide a fresh file containing exactly the current-session `auth_token` + `ct0` pair.

The Agent MUST NOT:

- read Chrome/Edge/Firefox cookie databases automatically;
- use `xactions login --from-browser` or equivalent automatic browser-cookie extraction;
- log in on behalf of the Human;
- bypass 2FA or any X verification;
- echo cookie values to terminal/log/report/chat;
- copy the existing server session and call it "fresh".

## Phase 0 — authority / safety preflight

Before any credential action:

1. Read Issue #2, TASK-015, TASK-014 report/receipt, and the current branch head.
2. Verify the production X monitor remains healthy enough to leave untouched:
   - Mihomo active and loopback-only;
   - `gate-d-poller.timer` active;
   - `/opt/xactions-poc/x-session.json` exists and remains unchanged;
   - no production service restart is needed.
3. Record non-secret hashes/metadata needed to prove the production session file was not replaced.
4. Create task-owned scratch paths outside both repositories.

Do not inspect or print the production session contents.

## Phase 1 — capture exactly one fresh Human session

Preferred path:

```text
local Windows workstation
  -> task-owned isolated upstream XActions runtime pinned to
     f2fb3ed2d052838578e68a224eccc2cbaebcb7ca
  -> XACTIONS_HOME redirected to a task-owned temporary directory
  -> Human runs/completes `xactions connect`
  -> real Chrome login / 2FA by Human
  -> task-owned owner-only cookies.json
```

The task may launch the supported `xactions connect` command, but the Human performs the login interaction.

If the local workstation cannot reach X through its already-existing network environment, do not configure a new proxy/VPN/TUN or alter system networking. Stop at:

```text
READY_FOR_OWNER_X_SESSION_REFRESH
```

If the Human instead supplies a fresh two-cookie file manually, use it only from a task-owned path outside repositories.

Freshness requirement:

```text
session captured/provided during TASK-015
AND
contains both auth_token and ct0
AND
not copied from /opt/xactions-poc/x-session.json
```

Record only booleans, file mode/ACL, capture timestamp, and verification status. Never record cookie values.

## Phase 2 — isolated session discrimination on the mainland host

Do NOT replace `/opt/xactions-poc/x-session.json`.

Transfer the fresh session through SSH to a task-owned temporary server path with owner-only permissions, then run the exact tested upstream runtime:

```text
nirholas/xactions @ f2fb3ed2d052838578e68a224eccc2cbaebcb7ca
XACTIONS_HOME = task-owned temporary directory
existing Mihomo path = unchanged
production /opt/xactions-poc = read-only
```

Use the already-proven dynamic query-ID mechanism. Do not hand-pin a SearchTimeline ID.

Run exactly these functional probes:

### S0 — fresh-session verification

Prove the new session is accepted by an authenticated-only identity/session check supported by the pinned upstream runtime.

Do not report the Human account identity unless strictly necessary; `verified=true/false` is sufficient.

### S1 — X search, account-scoped

```text
searchTweets('from:zcode_ai', 5, 'Latest')
```

Require real result objects with numeric Post IDs when PASS.

### S2 — X search, global keyword

```text
searchTweets('ZCode', 5, 'Latest')
```

Require real result objects with numeric Post IDs when PASS.

### S3 — full-session differential

Run a bounded followers call against the known public target account/user ID.

Purpose: distinguish `search-only` breakage from the broader full-session class.

### S4 — timeline control

```text
getTweets('zcode_ai', 5)
```

### S5 — canonical single-post read

Choose one real numeric Post ID from S1/S2 when search succeeds; otherwise from S4 only for control.

Verify:

```text
getTweet(id) -> material text
canonical URL = https://x.com/<returned username>/status/<numeric id>
```

## Retry / interpretation rules

Use one fresh session only.

Per probe:

```text
one primary call
+ at most one retry only for a concrete transport/runtime failure
```

Do not treat an authorization-shaped 401/403/404 as transport retry credit.

Do not recapture a second session in the same task.

### Outcome A — session hypothesis confirmed

Required pattern:

```text
S0 PASS
S1 PASS
S2 PASS
S3 PASS
S4 PASS
S5 PASS
```

Then conclude:

```text
fresh authenticated session restores the full-session endpoint class
query-ID dynamic discovery remains valid
x.semantic = AVAILABLE_WITH_SCOPE (test-stage)
```

Do not deploy the fresh session into production and do not replace the existing monitor session in this task.

Record that the future x.semantic provider requires a separately managed fresh-session credential lifecycle.

Terminal state:

```text
X_SEMANTIC_TEST_STAGE_AVAILABLE
```

### Outcome B — fresh verified session still reproduces the class failure

Pattern:

```text
S0 PASS
S4/S5 PASS
but S1/S2 and/or S3 still return authorization-shaped failure
```

Then conclude only:

```text
fresh session did not restore the full-session endpoint class under this
account/provider/runtime envelope
```

Do not continue repairing XActions search in this project.

Do not speculate whether the root cause is account restriction or a new X policy unless directly proven.

Terminal state:

```text
X_PROVIDER_ALTERNATIVE_REQUIRED
```

### Outcome C — fresh session cannot be captured or verified

If Human interaction is unavailable, login cannot complete without unauthorized network changes, or the newly captured session itself fails basic verification:

```text
READY_FOR_OWNER_X_SESSION_REFRESH
```

Do not interpret this as an XActions provider loss.

## Provider-alternative boundary

TASK-015 does NOT authorize staging another X provider.

If the result is `X_PROVIDER_ALTERNATIVE_REQUIRED`, stop and leave the next task to compare bounded alternatives such as:

```text
existing browser-session surface / OpenCLI
twitter-cli or another maintained HTTP/session client
provider-side remote X search/read if a legitimate read-only surface exists
```

No alternative gets installed or authenticated in TASK-015.

## Production and credential safety

Explicitly unauthorized:

- replacing `/opt/xactions-poc/x-session.json`;
- modifying/restarting Gate D, n8n, Docker, Mihomo, systemd timers, or the production X monitor;
- rotating/revoking the production X session;
- automatic browser cookie DB extraction;
- creating another X account;
- disabling 2FA or automating X verification;
- new proxy/VPN/TUN/relay/network configuration;
- browser automation for X content retrieval (browser use is allowed only for Human-assisted `xactions connect` session capture);
- production provider binding;
- PR #3 merge / main merge;
- vpsmanage merge or production deployment.

Secrets must never enter Git/GitHub, reports, receipts, stdout captured into evidence, or chat.

## Required durable outputs

Write to `xifeng12/external-knowledge`:

```text
reports/TASK-20260913-015-X-SESSION-REAUTH.md
evidence/TASK-20260913-015-x-session-reauth.json
```

The receipt may record:

```text
capture_method
fresh_session_captured: true|false
both_required_cookies_present: true|false
session_verified: true|false
probe status/error classes
result counts / numeric Post IDs / canonical URLs for public target content
dynamic query-ID provenance class
production session unchanged proof
cleanup status
terminal state
```

It MUST NOT contain session values, private account identity, private-key contents, proxy credentials, or other secrets.

If outcome A is reached, update `references/capability-map.md` only with a bounded test-stage `x.semantic` note.

If outcome B/C is reached, do not claim `x.semantic` availability.

## Cleanup

Before stop:

- delete task-owned fresh-session files from local and server scratch paths;
- delete isolated XActions runtime/cache unless needed only as a non-secret code artifact outside production (prefer delete);
- verify `/opt/xactions-poc/x-session.json` metadata/hash unchanged;
- verify Mihomo and Gate D timer remain active;
- leave `E:\cs\key` untouched;
- leave `vpsmanage` untouched;
- classify cleanup as `CLEAN_VERIFIED` or `CLEAN_WITH_RESIDUE`.

## Stop states

Stop at the first accurate state:

```text
X_SEMANTIC_TEST_STAGE_AVAILABLE
X_PROVIDER_ALTERNATIVE_REQUIRED
READY_FOR_OWNER_X_SESSION_REFRESH
```

Push the report/receipt and any explicitly allowed capability-map note, synchronize Issue #2, and stop.
