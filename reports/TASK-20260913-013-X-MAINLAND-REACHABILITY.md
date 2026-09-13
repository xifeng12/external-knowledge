# TASK-20260913-013 — X Reuse + Mainland No-Proxy Knowledge Reachability

```text
task_id: TASK-20260913-013
status: READY_FOR_X_PROVIDER_REPAIR_DECISION (X leg stop per contract §2.4; Phase B profile complete with remote read demonstrated)
parent: TASK-20260912-001
branch: task/20260912-001-v04-capability-diagnostics
receipt: evidence/TASK-20260913-013-x-mainland-receipt.json
```

## What this task did

Two vertical questions were executed against the existing mainland host
(Aliyun ECS `139.196.229.56`, Shanghai, connected via the authorized
`E:\cs\key` material) — no proxy reconfiguration, no new credentials, no
vpsmanage changes, no service restarts.

## Phase A — X reuse: search broken, read healthy (differential proven)

Preflight on the host confirmed the existing vpsmanage surface intact:
`/opt/xactions-poc` with XActions **3.5.0**, session file `0600 root`,
Mihomo active loopback-only on `127.0.0.1:7890`, and the production
`gate-d-poller.timer` running (untouched throughout).

The bounded search probes both failed with the exact error the contract
anticipated:

```text
X1  searchTweets('from:zcode_ai', 5, 'Latest')  -> HTTP 404: Not Found
X2  searchTweets('ZCode', 5, 'Latest')          -> HTTP 404: Not Found
```

A differential check proves the failure is search-endpoint-specific, not
session/envelope degradation, through the same unchanged envelope:

```text
getTweets('zcode_ai', 5)  -> PASS: 5 real posts, numeric IDs
getTweet(2098396306750517317) -> PASS:
    id match, username zcode_ai,
    canonical URL https://x.com/zcode_ai/status/2098396306750517317,
    297 chars of material text
```

Non-secret failure evidence: installed 3.5.0 ships SearchTimeline queryId
`flaR-PUMshxFWZWPNpq4zA` (in `src/scrapers/twitter/http/endpoints.js`); X has
rotated that queryId, so the endpoint 404s. Session, auth, proxy path, and the
UserTweets/TweetDetail queryIds all remain healthy.

Per contract §2.4 the X leg stops at:

```text
READY_FOR_X_PROVIDER_REPAIR_DECISION
```

The repair scope is narrow: only the SearchTimeline queryId needs updating in
the existing vpsmanage/XActions surface. Search is the broken leg; timeline
read and canonical single-post read still work. No Puppeteer/Chrome fallback
was used, no cookies were copied, and the production monitor was not touched.

## Phase B — mainland no-proxy reachability profile (complete)

All probes ran with proxy variables unset per-process. Mihomo kept running;
nothing system-level changed.

### Direct-reachability controls

| Control | Target | DNS | TCP/TLS | HTTP | local_direct_read |
|---|---|---|---|---|---|
| D1 | github.com | resolved | ok (0.09s) | 200 | AVAILABLE |
| D2 | x.com | resolved (Cloudflare IP) | **TCP timeout 15s** | — | BLOCKED_TRANSPORT |
| D3 | www.bing.com | resolved | ok | 302 → cn.bing.com | AVAILABLE |
| D4 | mcp.exa.ai | resolved | ok | 405 (POST-only app) | AVAILABLE |
| S1 | en.wikipedia.org (GIS article) | resolved | **TCP timeout 15s** | — | BLOCKED_TRANSPORT |

Both controls behaved as expected: github reachable, x.com transport-blocked.

### Search-discovery probe (Bing, no proxy)

Two bounded queries targeting the locally unreadable Wikipedia page. The
frontend redirects to **cn.bing.com** and serves organic results — but they
are mainland-flavored (National Geographic, 百度百科, Cambridge dictionary) with
**zero en.wikipedia.org mentions** across both queries.

```text
a reachable search frontend does NOT imply foreign-content discoverability
DISCOVERED != READABLE (and on the mainland frontend: also != surfacable)
```

### Exa anonymous hosted-MCP remote read (no proxy, no key)

`https://mcp.exa.ai` is transport-reachable from the mainland host, and the
anonymous MCP surface worked end to end:

```text
initialize   -> 200, exa-search-server 3.2.1
tools/list   -> 200, [web_search_exa, web_fetch_exa]
web_search_exa -> 200, 27,524 chars; FIRST result is exactly the locally
                  blocked S1 URL (DISCOVERED via provider)
web_fetch_exa  -> 200, 3,098 chars material Markdown for that same URL
```

(The single `web_fetch_exa` attempt with a `url` string failed input
validation — the tool requires a `urls` array; probe bug, corrected and
disclosed. Not a service failure.)

## Reachability model (three independent axes — not collapsed)

```text
github.com                 DISCOVERABLE   | AVAILABLE          | NOT_TESTED   -> DIRECT_AVAILABLE
x.com                      DISCOVERABLE   | BLOCKED_TRANSPORT  | NOT_TESTED   -> DISCOVERABLE_BUT_NOT_DIRECTLY_READABLE
www.bing.com               DISCOVERABLE   | AVAILABLE          | NOT_TESTED   -> DIRECT_AVAILABLE (weak foreign discovery)
mcp.exa.ai                 DISCOVERABLE   | AVAILABLE          | AVAILABLE    -> DIRECT_AVAILABLE + REMOTE_READ_AVAILABLE
en.wikipedia.org (S1)      DISCOVERED (Exa only) | BLOCKED_TRANSPORT | AVAILABLE -> DISCOVERABLE_AND_REMOTE_READABLE
```

Headline finding: **from the mainland host with no proxy, an Agent can still
discover and read foreign sources through the no-proxy-reachable Exa anonymous
hosted MCP** — the source is locally transport-blocked AND invisible on the
mainland search frontend, yet discoverable and remotely readable via Exa. This
validates the task's core distinction:

```text
discoverable != locally directly readable != remotely retrievable by a provider
```

## Capability-map note

A narrowly scoped test-stage note was added to `references/capability-map.md`
recording the reachability profile and the remote-read route. No production
provider binding, adapter binding, or routing change was made.

## Secret handling / mutation boundary / cleanup

- No private-key contents, tokens, cookies, or session values were printed or
  committed; session cookies were consumed only in-process by the existing
  XActions path.
- `E:\cs\key` files were not modified; because the original key's Windows ACL
  is open (and may not be chmodded per contract), a temporary ACL-restricted
  copy outside the repo was used for SSH and deleted at stop.
- vpsmanage was read-only (temp shallow clone, deleted).
- Host `/tmp` probe scripts and artifacts removed; verification: zero
  task-owned files remain, mihomo and gate-d-poller.timer still active.
  `CLEAN_VERIFIED`.

## Stop

Report/receipt pushed; Issue #2 synchronized with the new head and the exact
terminal state. Stopping at the first accurate terminal state:

```text
READY_FOR_X_PROVIDER_REPAIR_DECISION
```

Decision surface for the Human: update the SearchTimeline queryId in the
existing vpsmanage/XActions surface (search leg only), after which
`x.semantic = AVAILABLE_WITH_SCOPE (test-stage)` can be re-validated with the
same X1/X2/read fixtures. The mainland remote-read capability demonstrated in
Phase B needs no provisioning decision — it is already demonstrated no-proxy.
