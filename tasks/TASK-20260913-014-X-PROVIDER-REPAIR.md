---
task_id: TASK-20260913-014
status: ready_for_x_provider_repair_execution
parent_task: TASK-20260912-001
predecessor: TASK-20260913-013
target_repo: xifeng12/external-knowledge
secondary_repo: xifeng12/vpsmanage
implementation_branch: task/20260912-001-v04-capability-diagnostics
capability: x.semantic
production_deployment_authorized: false
credential_change_authorized: false
network_change_authorized: false
vpsmanage_merge_authorized: false
external_knowledge_merge_authorized: false
---

# TASK-20260913-014 — X Provider Repair / Dynamic GraphQL Query-ID Resolution

## Goal

Repair only the broken X search leg identified by TASK-013, while preserving the already-healthy authentication, network, timeline-read, and single-post-read envelope.

The target test-stage vertical is:

```text
query
  -> X search results
  -> numeric Post ID
  -> canonical https://x.com/<user>/status/<id>
  -> single-post read
```

Success may promote:

```text
x.semantic = AVAILABLE_WITH_SCOPE (test-stage)
```

This task is a provider repair, not a provider replacement and not a new Arena.

## Accepted predecessor evidence

TASK-013 proved on the existing mainland execution surface:

```text
XActions 3.5.0
+ existing auth_token/ct0 session
+ existing Mihomo 127.0.0.1:7890 path

searchTweets('from:zcode_ai', 5, 'Latest') -> HTTP 404
searchTweets('ZCode', 5, 'Latest')         -> HTTP 404
getTweets('zcode_ai', 5)                  -> PASS
getTweet(<real numeric id>)                -> PASS
```

The failure is isolated to the stale `SearchTimeline` persisted GraphQL query ID. Do not re-investigate cookies, X reachability, Mihomo, or the working read paths unless new direct evidence contradicts this predecessor result.

Current upstream XActions source also contains dynamic GraphQL query-ID discovery/cache machinery that reads live x.com bundles and prefers discovered/cache IDs over hardcoded fallbacks. The task must verify the exact upstream SHA used at execution time rather than assuming a package version implies those changes are present.

## Authority and repositories

Primary task authority remains this file in `xifeng12/external-knowledge`.

`xifeng12/vpsmanage` is authorized for a **bounded repair branch/PR only** if Gate A proves the upstream dynamic-resolution path fixes the search leg.

Do not merge either repository.

## Host / secret boundary

Authorized local connection material is under:

```text
E:\cs\key
```

It may be used only to establish the existing host connection.

Never print, copy into a repository, commit, or expose:

- SSH private-key contents or passphrases;
- X `auth_token` / `ct0` values;
- proxy credentials or subscription URLs;
- n8n / Server酱 / other secrets.

The existing server-side X session remains the only X credential source.

## Gate A — Isolated upstream repair validation

Do **not** modify `/opt/xactions-poc` in place.

Create a task-owned isolated temporary runtime on the existing mainland host (or equivalent task-owned temporary directory) and:

1. record the installed production XActions state read-only;
2. fetch/checkout the current authoritative XActions upstream source and record its exact commit SHA;
3. verify the upstream contains dynamic query-ID discovery/resolution for GraphQL operations, including `SearchTimeline`;
4. reuse the existing server-side session **read-only** and the existing Mihomo X path without copying credential values;
5. run the same bounded fixtures through the isolated upstream runtime:

```text
X1 searchTweets('from:zcode_ai', 5, 'Latest')
X2 searchTweets('ZCode', 5, 'Latest')
X3 getTweets('zcode_ai', 5)
X4 getTweet(<one returned real numeric Post ID>)
```

For successful search results, verify:

```text
numeric post ID
non-empty text
username/author when exposed
canonical URL deterministically constructed from user + Post ID
single-post read returns the same ID and material content
```

Also record the `SearchTimeline` query-ID provenance used by the successful run:

```text
discovered/cache/live-resolution
```

A merely substituted hardcoded current ID is not sufficient evidence for Gate A success.

### Gate A success

Gate A passes only if both X1 and X2 return real search results and X3/X4 remain healthy under the isolated upstream runtime.

### Gate A failure

If current upstream still cannot search, stop without inventing a browser fallback or second provider. Record the exact failure and use:

```text
READY_FOR_X_PROVIDER_ALTERNATIVE_DECISION
```

## Gate B — Minimal durable repair in `vpsmanage`

Enter Gate B only after Gate A passes.

The preferred repair is to absorb the **smallest maintainable upstream mechanism** needed for dynamic GraphQL query-ID resolution, not to pin a one-off `SearchTimeline` string.

Allowed forms, in preference order:

1. upgrade/vendor the minimal HTTP-client/query-ID components from the verified upstream source if they can remain low-dependency and compatible with the existing fetch-client deployment;
2. add a narrowly scoped query-ID refresh/resolution helper and wiring derived from the verified upstream mechanism;
3. if neither can be done cleanly without dragging the full browser/dependency stack, stop for Human decision rather than broadening scope.

The durable change must live on a dedicated `vpsmanage` repair branch and be reviewable through a PR. Do not merge it.

### Required invariants

The repair must preserve:

```text
no Puppeteer / Chrome requirement
no second X credential store
existing auth_token + ct0 session contract unchanged
existing Mihomo/upstream X network path unchanged
existing Gate D monitor behavior unchanged
canonical URL from trusted numeric Post ID
read-only X capability only
```

Do not modify n8n workflows, Server酱 logic, classification rules, systemd timers, Mihomo configuration, routing, DNS, firewall, or the production X session.

## Production safety

Production `/opt/xactions-poc` is read-only in this task.

Do not:

- hot-patch `node_modules` in place;
- restart or stop `gate-d-poller.timer`;
- restart Mihomo/n8n/Docker;
- replace the production XActions package;
- rotate/copy X cookies;
- install browser automation;
- change proxy topology.

If a future deployment is desired after review, it requires a separate Human authorization.

## Validation after durable repair

Validate the `vpsmanage` repair artifact in an isolated runtime using the same four fixtures.

Required pass conditions:

```text
X1 account-scoped search -> PASS
X2 global keyword search -> PASS
X3 timeline read         -> PASS
X4 single-post read      -> PASS
SearchTimeline ID provenance is dynamic/discovered or cache-backed from live discovery
no secret leakage
no production service mutation
```

If Gate B passes, external-knowledge may record a test-stage provider result:

```text
x.semantic
  search -> repaired vpsmanage/XActions HTTP-only surface
  timeline/read -> existing XActions HTTP-only surface
  auth -> existing server-side auth_token + ct0
  network -> existing Mihomo/upstream path
  production deployment -> NOT AUTHORIZED
```

## External-knowledge durable outputs

Write:

```text
reports/TASK-20260913-014-X-PROVIDER-REPAIR.md
evidence/TASK-20260913-014-x-provider-repair.json
```

Update `references/capability-map.md` only if supported by actual Gate A/B evidence. Keep any route explicitly test-stage.

Synchronize Issue #2 after the execution stop state.

## vpsmanage durable outputs when Gate B is entered

Use a dedicated repair branch and PR containing only the minimum non-secret repair, tests/validation helper if needed, and a concise report/receipt sufficient to review the patch.

Do not merge the PR.

## Stop states

Use the first accurate state:

```text
X_SEMANTIC_TEST_STAGE_AVAILABLE
READY_FOR_X_PROVIDER_ALTERNATIVE_DECISION
READY_FOR_X_REPAIR_REVIEW
```

Interpretation:

- `X_SEMANTIC_TEST_STAGE_AVAILABLE`: Gate A and Gate B validation both pass; durable repair PR exists, but production deployment remains unauthorized.
- `READY_FOR_X_PROVIDER_ALTERNATIVE_DECISION`: current upstream mechanism does not restore search, or repair would require a materially different provider/runtime.
- `READY_FOR_X_REPAIR_REVIEW`: Gate A passes but the maintainable durable repair cannot be completed safely inside this scope.

After the first stop state, push authorized repository artifacts, synchronize Issue #2, and stop.
