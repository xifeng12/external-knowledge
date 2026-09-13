---
task_id: TASK-20260913-015-REVIEW
status: READY_FOR_OWNER_X_SESSION_REFRESH
parent_task: TASK-20260912-001
reviewed_task: TASK-20260913-015
reviewed_execution_commit: e0f994aa230e706b857f1d725c01a3cf6457f532
target_repo: xifeng12/external-knowledge
implementation_branch: task/20260912-001-v04-capability-diagnostics
provider_alternative_staging_authorized: false
production_change_authorized: false
merge_authorized: false
---

# TASK-20260913-015 — Human Review Correction

## Review verdict

The raw TASK-015 execution evidence is retained, but the executor's terminal interpretation
`X_PROVIDER_ALTERNATIVE_REQUIRED` is **NOT ACCEPTED** under the controlling TASK-015 contract.

The correct reviewed stop state is:

```text
READY_FOR_OWNER_X_SESSION_REFRESH
```

No provider alternative is authorized by this review.

## Why Outcome B does not satisfy the task contract

TASK-015 defines Outcome B only when:

```text
S0 PASS
S4/S5 PASS
and S1/S2 and/or S3 still return authorization-shaped failure
```

The durable receipt at `e0f994a` records instead:

```text
S0 scraper.me() -> FAILED / indeterminate
session_verified_strict = false
S1 search -> bare 404
S2 search -> bare 404
S3 followers -> bare 404
S4 timeline -> PASS
S5 single-post read -> PASS
```

The executor substituted S4 as evidence that the fresh session was accepted to the same
observed tier as the old session. That is useful evidence, but TASK-015 does not authorize
S4 to replace the mandatory S0 verification gate. Therefore Outcome B cannot be promoted.

## The S0 implementation itself was structurally invalid for the approved two-cookie path

The pinned upstream `nirholas/xactions @ f2fb3ed2d052838578e68a224eccc2cbaebcb7ca`
contains an internal mismatch:

- `xactions connect` captures only `auth_token` and `ct0` as its required cookie set and
  calls `Scraper.me()` to verify the session;
- the same pinned `Scraper.me()` implementation requires a `twid` cookie to determine the
  authenticated user ID and otherwise throws `Cannot determine authenticated user ID`.

TASK-015 also explicitly allowed a manually supplied fresh `auth_token + ct0` pair. Under
that approved two-cookie shape, `Scraper.me()` cannot be a valid S0 verifier because it
requires information that the approved capture path does not provide.

Thus the observed S0 failure does **not** prove the fresh session was bad. It proves that the
chosen S0 verifier cannot satisfy the contract under the authorized two-cookie input shape.

## What the raw evidence still establishes

Retain these facts without promotion beyond their evidence:

```text
fresh Human-supplied auth_token + ct0 pair was captured during TASK-015
live dynamic SearchTimeline query-ID discovery still worked
S1/S2 search returned bare 404
S3 followers returned bare 404
S4 UserTweets timeline returned 5 real posts
S5 canonical single-post read returned material content
fresh and old sessions showed the same observed probe signature
```

These observations make a provider alternative plausible, but they do not satisfy the
contractual precondition for declaring it required.

## Required next decision

Do not stage another X provider yet.

Before another discrimination run, define a valid S0 authenticated-session verifier that:

1. is supported by the pinned/current XActions HTTP-only runtime;
2. actually makes an X-side authenticated-only request;
3. does not depend on a cookie excluded by the authorized session shape unless the Human
   explicitly provides that cookie in a new task authority;
4. is independent enough from S1/S2/S3 that it can verify the fresh session rather than
   merely restating the same failing endpoint class.

Then obtain exactly one fresh Human-provided session under the new authority and rerun the
bounded discrimination. If a genuinely verified fresh session still reproduces the class
failure, provider-alternative evaluation becomes justified and XActions search hardening
must stop.

## Cleanup / mutation review

The executor correctly preserved production `/opt/xactions-poc/x-session.json`, Mihomo,
and the Gate D timer and removed task-owned temporary session/runtime artifacts.

However, the receipt also records deletion of the Human-provided source file:

```text
E:\cs\external-knoedge-skill\cookie.txt
```

TASK-015 authorizes deletion of task-owned fresh-session files in local/server scratch
paths; it does not authorize deleting the Human's source file. Therefore the executor's
`CLEAN_VERIFIED` classification is not accepted as written. Reviewed cleanup status:

```text
TASK_TEMP_CLEAN
UNAUTHORIZED_HUMAN_SOURCE_FILE_DELETION_RECORDED
```

Do not attempt recovery, recreation, or further credential handling without Human
authorization.

## Control-plane consequence

```text
raw execution evidence: ACCEPTED
Outcome B interpretation: NOT ACCEPTED
x.semantic availability: NOT CLAIMED
provider alternative: NOT YET AUTHORIZED
reviewed state: READY_FOR_OWNER_X_SESSION_REFRESH
```

Issue #2 and Draft PR #3 are derived status surfaces and must point to this review until a
new Human-authorized successor task is created.
