---
task_id: TASK-20260913-016
status: ready_for_x_session_verifier_discrimination
parent_task: TASK-20260912-001
predecessor: TASK-20260913-015
review_correction: TASK-20260913-015-REVIEW-CORRECTION
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

# TASK-20260913-016 — X Session Verifier Discrimination

## Goal

Correct the invalid S0 verifier used by TASK-015 and perform exactly one final, bounded XActions discrimination run.

The decision question is:

```text
Can a fresh Human-provided auth_token + ct0 session be independently proven
as accepted by an X session-only endpoint, and if so, does X search/followers
still fail under that same verified session?
```

This is the final XActions session discrimination. It is not a new code-repair round, not an Arena, and not provider-alternative staging.

## Accepted evidence

TASK-013 through TASK-015 establish:

```text
- XActions HTTP-only timeline and single-post reads work through the existing Mihomo path.
- Dynamic GraphQL query-ID discovery works and refreshes SearchTimeline from live X bundles.
- Search and followers return authorization-shaped bare 404s under both the old and one fresh two-cookie session.
- TASK-015 Outcome B was NOT accepted because its contract required S0 PASS,
  while S0 used Scraper.me(), which requires twid and therefore cannot pass
  under the authorized auth_token + ct0 session shape.
```

The raw TASK-015 probe evidence remains valid. Only its Outcome B promotion was rejected.

## S0 verifier contract

Use an X-side, authenticated-only verifier that is compatible with the authorized two-cookie session shape and independent from SearchTimeline / Followers.

Primary verifier:

```text
HomeTimeline GraphQL operation
```

Current pinned upstream documentation classifies home timeline as a session-tier capability, while public profile/user-timeline reads are guest-capable. HomeTimeline also does not require `twid` to identify a target user before the request.

A minimal task-owned HTTP probe against the pinned upstream HTTP scraper is allowed if no public convenience method exists. Do not add browser automation or a persistent adapter.

### S0 must be differential, not assumed

Against the same pinned runtime and network envelope:

```text
S0-GUEST
  no auth_token / no ct0
  -> HomeTimeline must be rejected as unauthenticated/session-required
     (authorization-shaped error or equivalent non-session response)

S0-FRESH
  exactly the one fresh Human-provided auth_token + ct0 pair
  -> HomeTimeline must be accepted and return a structurally valid authenticated
     timeline response / material entries
```

Only this guest-vs-fresh differential counts as `S0 PASS`.

Do NOT use:

- `Scraper.me()` (requires `twid` in the pinned runtime);
- `isLoggedIn()` client flags;
- presence/length of cookie strings;
- S1/S2 search or S3 followers as the verifier itself;
- public `getTweets()` alone as S0.

If HomeTimeline cannot be invoked through the pinned HTTP-only surface without changing the approved architecture, stop at `READY_FOR_X_VERIFIER_REDESIGN`. Do not invent another verifier during the run.

## Phase 0 — safety preflight

1. Read Issue #2, this task, TASK-015 review correction, TASK-015 report/receipt, and current branch head.
2. Verify production remains untouched and healthy enough to leave alone:
   - Mihomo active and loopback-only;
   - `gate-d-poller.timer` active;
   - `/opt/xactions-poc/x-session.json` metadata/hash recorded read-only.
3. Use the same pinned upstream XActions SHA previously validated by TASK-014/015 unless repository authority explicitly changes it.
4. Create only task-owned scratch paths outside repositories and production runtime.

## Phase 1 — exactly one fresh Human session

A new fresh session is required because the TASK-015 Human source file was deleted during that execution and must not be recreated or inferred.

Allowed:

- Human completes `xactions connect` interactively, or
- Human supplies a fresh browser-export/session file captured during TASK-016.

Agent may extract only `auth_token` + `ct0` into a task-owned normalized scratch file.

Strict source-file rule:

```text
Human-provided source file is READ-ONLY INPUT.
NEVER delete, truncate, overwrite, rename, move, chmod/icacls, or otherwise mutate it.
Only task-owned derived copies may be deleted during cleanup.
```

The Agent MUST NOT automatically read browser cookie databases, log in for the Human, bypass 2FA, or echo cookie values.

If no fresh session can be provided within these boundaries, stop at:

```text
READY_FOR_OWNER_X_SESSION_REFRESH
```

## Phase 2 — S0 verifier

Run S0-GUEST and S0-FRESH through the unchanged mainland Mihomo path in the isolated pinned XActions runtime.

Record only:

```text
verifier operation
query-ID provenance class when GraphQL is used
guest result class
fresh result class
response structural validity / bounded item count
S0 PASS|FAIL
```

Never record private home-timeline content. Use counts/shape only.

### S0 PASS

Required:

```text
Guest control is rejected/non-session
AND
Fresh session is accepted with structurally valid HomeTimeline data
```

Only then continue to Phase 3.

### S0 FAIL

If the fresh session does not pass while the verifier itself is proven session-only, stop at:

```text
READY_FOR_OWNER_X_SESSION_REFRESH
```

Do not interpret it as provider loss.

## Phase 3 — final discrimination

Only after `S0 PASS`, run exactly:

```text
S1 searchTweets('from:zcode_ai', 5, 'Latest')
S2 searchTweets('ZCode', 5, 'Latest')
S3 bounded getFollowers on the known public target
S4 getTweets('zcode_ai', 5)
S5 getTweet(real numeric Post ID from S1/S2 when available, otherwise S4 control)
```

Use live/dynamic query-ID resolution. No hand-pinned IDs.

Retry discipline:

```text
one primary call per probe
+ at most one retry only for a concrete transport/runtime failure
```

Authorization-shaped 401/403/404 is a result, not retry credit.

## Outcome A — XActions viable

Required:

```text
S0 PASS
S1 PASS
S2 PASS
S3 PASS
S4 PASS
S5 PASS
```

Then:

```text
x.semantic = AVAILABLE_WITH_SCOPE (test-stage)
```

Record the credential-lifecycle dependency explicitly. Do not deploy the fresh session to production in this task.

Terminal state:

```text
X_SEMANTIC_TEST_STAGE_AVAILABLE
```

## Outcome B — provider alternative finally justified

Required:

```text
S0 PASS
S4/S5 PASS
but S1/S2 and/or S3 still fail authorization-shaped
```

Then conclude only:

```text
A fresh session is independently accepted by X for a session-only endpoint,
but the required X search/followers capability still fails under the same
account/provider/runtime envelope.
```

At this point, per Goal Integrity:

```text
STOP all further XActions search/session/query-ID hardening in this project.
```

Terminal state:

```text
X_PROVIDER_ALTERNATIVE_REQUIRED
```

The next task may compare bounded provider alternatives. TASK-016 itself does not stage them.

## Explicitly unauthorized

- modifying/replacing `/opt/xactions-poc/x-session.json`;
- production deployment or hot patch;
- modifying/restarting Mihomo, n8n, Docker, Gate D timers, or X monitor;
- automatic browser cookie DB extraction;
- agent-driven login or verification bypass;
- deleting or mutating any Human-provided source credential file;
- new proxy/VPN/TUN/network configuration;
- browser automation for content retrieval;
- another query-ID/code repair loop;
- staging another X provider;
- new X account;
- provider binding changes;
- PR #3/main merge or vpsmanage merge.

## Required outputs

Write:

```text
reports/TASK-20260913-016-X-SESSION-VERIFIER.md
evidence/TASK-20260913-016-x-session-verifier.json
```

Receipt must include S0 guest/fresh result classes, S1-S5 statuses, dynamic query-ID provenance, production-unchanged proof, Human-source-file unchanged proof, cleanup status, and terminal state. It must not contain cookies, private home timeline data, private account identity, private keys, proxy credentials, or other secrets.

If Outcome A occurs, a bounded test-stage capability-map note is allowed. If Outcome B/C occurs, do not claim x.semantic availability.

## Cleanup

Delete only task-owned scratch artifacts and derived session copies.

Verify:

```text
Human source credential file still exists unchanged (when one was supplied)
production x-session metadata/hash unchanged
Mihomo active
Gate D timer active
no task-owned host/local secret residue
```

Classify cleanup honestly.

## Stop states

Stop at the first accurate state:

```text
X_SEMANTIC_TEST_STAGE_AVAILABLE
X_PROVIDER_ALTERNATIVE_REQUIRED
READY_FOR_OWNER_X_SESSION_REFRESH
READY_FOR_X_VERIFIER_REDESIGN
```

Push report/receipt, synchronize Issue #2, and stop.