---
task_id: TASK-20260913-013
status: ready_for_x_mainland_vertical_execution
parent_task: TASK-20260912-001
target_repo: xifeng12/external-knowledge
implementation_branch: task/20260912-001-v04-capability-diagnostics
related_repo_read_only: xifeng12/vpsmanage
capability_scope:
  - x.semantic
  - general-web.search
  - general-web.read
execution_class: TEST_STAGE_VERTICAL
persistent_provisioning_authorized: false
new_credential_creation_authorized: false
proxy_or_network_reconfiguration_authorized: false
production_routing_authority: false
pr_merge_authorized: false
---

# TASK-20260913-013 — X Reuse + Mainland No-Proxy Knowledge Reachability

## Goal

Advance two vertical questions that can materially expand external-knowledge without rebuilding already-solved infrastructure:

```text
A. X semantic reuse
   Can the already-proven XActions execution surface from xifeng12/vpsmanage
   provide search + canonical post read for external-knowledge without creating
   a second X auth/network stack?

B. Mainland no-proxy knowledge reachability
   From the existing mainland host, can an Agent discover foreign information
   through reachable search/remote-retrieval services even when the foreign
   source itself is not directly reachable?
```

This is not an Arena, not a provider tournament, and not a proxy-design task.

The task must preserve the distinction:

```text
discoverable
!= locally directly readable
!= remotely retrievable by a provider
```

## Existing evidence to reuse

### From `xifeng12/vpsmanage`

Treat the private repository as read-only evidence authority for the already-proven X execution surface.

Relevant established facts include:

```text
XActions v3.5.0 fetch client
minimum X session = auth_token + ct0
session stored outside Git as local 0600 file
HTTP-only fetch client; no Puppeteer required
production X path = XActions -> Mihomo 127.0.0.1:7890 -> approved upstream -> X
getTweets(@zcode_ai) validated 5 runs x 5 posts
getTweetsAndReplies already used in the corpus path
canonical post URL derived deterministically from numeric Post ID
```

Current XActions 3.5.0 upstream also exposes HTTP-client `searchTweets()` over the internal GraphQL `SearchTimeline` endpoint. This task verifies that capability on the existing authenticated/proxied execution surface rather than assuming it works.

### From external-knowledge

Current accepted baselines remain unchanged:

```text
WeChat minimum vertical = WECHAT_MINIMUM_VERTICAL_AVAILABLE
Native Search = default general search owner
Exa = qualified precision-search candidate
TASK-010 Tavily = NO_BATTLE / operationally valid but unadjudicated
```

Do not reopen those tracks.

# 1. Local connection authority — `E:\cs\key`

The Human explicitly states that host connection information / key material is available under:

```text
E:\cs\key
```

The target-machine Coordinator/Agent may inspect that folder only as needed to identify the mainland host and establish SSH.

Hard secret-handling rules:

- never print private-key contents;
- never print passphrases, tokens, passwords, X cookies, proxy subscription URLs, or secret env values;
- never copy key files into the repository;
- never commit host credentials or connection secrets;
- do not rename, chmod, move, rewrite, or otherwise mutate files in `E:\cs\key`;
- it is acceptable to record non-secret facts such as which local file path was selected as the SSH key, but not its contents;
- if multiple candidate hosts/keys exist, infer the intended mainland host from existing `vpsmanage` evidence and local metadata; do not ask the Human to repeat information already present in the authorized local folder or repository.

# 2. Phase A — verify and reuse the existing X execution surface

## 2.1 Read-only preflight

On the mainland host, first verify without changing services:

```text
existing /opt/xactions-poc (or current equivalent) exists
existing XActions package/version
existing session file exists and remains 0600
Mihomo 127.0.0.1:7890 is available
no need to restart or edit Mihomo/n8n/systemd/X session
```

Do not read or print the actual `auth_token` / `ct0` values. They may be consumed only by the existing local XActions process path.

## 2.2 Search capability probe

Use the existing XActions HTTP client and existing authenticated/proxied execution envelope.

Run a bounded one-shot search test using `Scraper.searchTweets()`.

Required fixtures:

### X1 — account-scoped search consistency

```text
query: from:zcode_ai
mode: Latest
count: 5
```

Acceptance:

- returns at least one real post;
- every accepted result has numeric Post ID and material text;
- canonical URL is reconstructed as `https://x.com/<username>/status/<POST_ID>`;
- at least one returned ID is consistent with the current account timeline when checked through the existing `getTweets()` path.

### X2 — global keyword search

Choose one bounded, non-sensitive query relevant to the existing monitored domain (for example `ZCode`, `ZCode AI`, or another current public term visible in the retained corpus).

Acceptance:

- global search returns real structured posts from one or more accounts;
- record only bounded metadata/snippets needed to prove the path;
- do not expand into trend analysis or corpus building.

## 2.3 Canonical post read

Select one search result from X1 or X2 and call the existing HTTP-only single-post read path (`getTweet(id)` or equivalent current XActions client method).

Prove:

```text
search result -> numeric Post ID -> canonical X URL -> single post body/metadata
```

If the existing XActions client can expose conversation/reply context without introducing a browser or new auth surface, one bounded read may be recorded. Do not make full-thread coverage a success requirement.

## 2.4 X result classification

If X1 + X2 + canonical post read succeed under the existing vpsmanage execution envelope, record:

```text
x.semantic = AVAILABLE_WITH_SCOPE (test-stage)
provider candidate = existing vpsmanage/XActions read surface
network/auth ownership = retained by vpsmanage execution environment
```

Do NOT copy X cookies into external-knowledge, do NOT install a second XActions runtime locally, and do NOT change the existing production monitor.

If `searchTweets()` fails because the current X GraphQL endpoint changed, preserve the exact non-secret failure evidence and stop the X leg at:

```text
READY_FOR_X_PROVIDER_REPAIR_DECISION
```

Do not fall back to Puppeteer/Chrome in this task.

# 3. Phase B — mainland no-proxy knowledge reachability profile

This phase answers whether foreign knowledge can still be discovered/read without configuring a proxy on the mainland host.

## 3.1 No-proxy execution rule

For every Phase B probe, explicitly remove process-scoped proxy variables for that command only:

```text
HTTP_PROXY
HTTPS_PROXY
ALL_PROXY
http_proxy
https_proxy
all_proxy
```

Also avoid application-specific proxy dispatchers.

This is a process-scoped test only. Do not stop Mihomo, do not change system routes, do not change shell profiles, and do not alter system proxy configuration.

## 3.2 Direct-reachability controls

Use bounded HTTPS GET/HEAD-style checks with short timeouts and classify transport separately from HTTP/application status.

Required controls:

```text
D1 github.com        known direct-reachable control from retained evidence
D2 x.com             known/expected direct-read negative control; re-verify, do not assume
D3 bing.com          candidate mainland-reachable search frontend
D4 mcp.exa.ai        candidate remote search/fetch provider endpoint
```

Add at most two public foreign content sources only if needed to obtain a meaningful source that is search-discoverable but locally unreadable. Prefer ordinary public text sources; do not turn this into a broad censorship survey.

For each record:

```text
DNS resolution result (non-sensitive)
TCP/TLS/HTTP reachability classification
HTTP status if reached
elapsed time
whether failure is transport-level vs application-level
```

Do not infer geopolitical/network root cause beyond observed evidence.

## 3.3 Mainland search-discovery probe

If Bing is reachable without proxy, run one or two bounded search queries that target a known foreign-domain public page.

Purpose:

```text
prove or disprove that a mainland host can discover a foreign URL through a reachable search index even when that source may not be locally readable
```

Record only result titles/domains/URLs needed for evidence.

A source appearing in a search result is `DISCOVERED`, not `READABLE`.

## 3.4 Exa no-proxy remote provider probe

If `mcp.exa.ai` is reachable without proxy:

1. perform the minimum anonymous MCP handshake/tool-list needed to establish the surface;
2. run one bounded `web_search_exa` query;
3. if a public source is found that the mainland host cannot directly read at the transport/content level, use `web_fetch_exa` on that exact URL;
4. verify whether Exa returns material content/Markdown.

Use no API key, no OAuth, no account, no persistent registration.

If Exa is unreachable from the mainland host, record that fact and stop this leg. Do not add a proxy to make the no-proxy probe pass.

If Exa search works but remote fetch cannot read the selected source, record the split honestly.

# 4. Required reachability model

Classify each tested source/provider on independent axes:

```text
discovery_status:
  DISCOVERABLE
  NOT_DISCOVERED
  UNRESOLVED

local_direct_read:
  AVAILABLE
  BLOCKED_TRANSPORT
  BLOCKED_APPLICATION
  UNRESOLVED

provider_remote_read:
  AVAILABLE
  UNAVAILABLE
  NOT_TESTED
  UNRESOLVED
```

Derived useful states may include:

```text
DIRECT_AVAILABLE
DISCOVERABLE_BUT_NOT_DIRECTLY_READABLE
REMOTE_READ_AVAILABLE
DISCOVERABLE_AND_REMOTE_READABLE
UNRESOLVED
```

Do not collapse these axes into one generic `foreign_web = available/blocked` flag.

# 5. Minimal implementation boundary

This task is evidence-first.

Allowed implementation only when needed to capture receipts:

- tiny ephemeral scripts under `/tmp` on the mainland host;
- a small repository-owned probe helper in external-knowledge only if repeated manual commands cannot reliably produce structured evidence;
- no changes to `xifeng12/vpsmanage` production code, services, timers, workflows, network config, or secret files.

Any ephemeral mainland-host script must be removed before stop unless it is explicitly promoted into external-knowledge as a non-secret test helper.

# 6. Durable outputs

Write at minimum:

```text
reports/TASK-20260913-013-X-MAINLAND-REACHABILITY.md
evidence/TASK-20260913-013-x-mainland-receipt.json
```

The receipt must separate:

```text
X reuse evidence
mainland no-proxy direct reachability
search discoverability
provider-side remote read
secret-handling / mutation boundary
cleanup status
```

If the result justifies a test-stage capability-map note, a narrowly scoped documentation update is allowed. No production provider binding or adapter binding change is authorized.

# 7. Explicitly unauthorized

Do not:

- modify `xifeng12/vpsmanage` production logic;
- restart/reconfigure Mihomo, n8n, Docker, systemd timers, or X monitoring workflows;
- rotate or copy X session cookies;
- expose `auth_token`, `ct0`, SSH private keys, proxy credentials, subscription URLs, or other secrets;
- install a new proxy/VPN/TUN/relay;
- change mainland routes/DNS/firewall/system proxy;
- provision Puppeteer/Chrome for X;
- install a second persistent XActions runtime for external-knowledge;
- create Exa/Tavily/X accounts or API keys;
- use a proxy in Phase B no-proxy probes;
- change production routing/provider bindings;
- merge PR #3 or merge to `main`.

# 8. Stop states

Use the first accurate terminal state:

```text
X_REUSE_AND_MAINLAND_REMOTE_READ_AVAILABLE
  X search/read reuse works and mainland no-proxy remote-provider read is demonstrated

X_REUSE_AVAILABLE_MAINLAND_PROFILE_ONLY
  X reuse works but remote-provider read is unavailable/unproven; reachability profile is still complete enough to guide routing

READY_FOR_X_PROVIDER_REPAIR_DECISION
  existing X execution surface cannot support the required search/read path without a new repair decision

READY_FOR_MAINLAND_REMOTE_READ_DECISION
  X reuse is proven but mainland no-proxy provider-side remote read needs a separate decision/provisioning step
```

Before stopping:

- push report/receipt and any narrowly necessary external-knowledge changes;
- synchronize Issue #2 with the new branch head and exact terminal state;
- preserve `vpsmanage` as read-only;
- verify no secret or temporary credential material entered Git;
- clean any match/task-owned temporary files on the mainland host.
