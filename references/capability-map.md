# External Knowledge Capability Map — v0.4 candidate

This map describes repository authority: what information capabilities are modeled, which providers are bound to them, and how routing is intended to work. It is **not** a receipt that every provider is callable on the current machine.

## Capability registry

| Capability | Information need / source semantic | Declared provider(s) | Intended role |
|---|---|---|---|
| `general-web.search` | General current facts and web discovery | `runtime-native.web-search` | General search owner |
| `general-web.read` | Known ordinary URL reading | `runtime-native.webfetch` | General reader |
| `docs.versioned` | Version-matched library/framework/SDK/API semantics | `context7` | Documentation specialist |
| `github.semantic` | Repository/PR/issue/commit/release/source-history semantics | `gh-cli` | GitHub-native specialist |
| `wechat.discovery` | WeChat article discovery | `wechat-article-search` | WeChat discovery specialist |
| `wechat.reader` | Canonical WeChat article body reading | `weixin-articles-reader` | WeChat reader specialist |
| `precision.search` | Exact obscure term/API/error/version after ordinary search has an observed precision/recall gap | `exa` | Precision challenger |
| `complex-web.read` | Complex extraction after ordinary reading has an observed extraction gap | `runtime-native.webfetch`, `firecrawl` | Degraded ordinary reader + extraction challenger |

The runtime adapter remains the machine-readable authority for provider bindings and exposure contracts. This document is the human-facing map.

## Channel classes

The current provider set falls into four operational roles:

1. **General backbone** — general web search and ordinary URL reading.
2. **Source specialists** — versioned docs, GitHub-native retrieval, WeChat discovery/reading.
3. **Precision/extraction challengers** — Exa and Firecrawl, entered only after a concrete gap or when the source semantic directly requires the specialist.
4. **Runtime evidence** — Doctor/inventory evidence that determines whether a declared provider is actually callable in one execution surface.

Do not fan out every provider merely because multiple channels exist.

## Routing map

```text
Information need
├─ general current fact / discovery
│  └─ general web
│     └─ observed precision/recall gap -> precision challenger
├─ versioned docs/API
│  └─ version-matched docs specialist
├─ GitHub object/history
│  └─ GitHub-native specialist
├─ WeChat
│  ├─ discovery -> WeChat discovery specialist
│  └─ canonical URL read -> WeChat reader specialist
└─ known ordinary URL
   └─ ordinary reader
      └─ observed extraction gap -> extraction challenger
```

## Five-axis decision record

For each capability/provider decision, keep these fields separate:

1. **Source semantic** — what kind of information is being sought.
2. **Default owner** — which provider is preferred when viable.
3. **Operational availability** — whether this runtime can actually call it.
4. **Observed quality** — source-semantic discoverability/extraction quality supported by evidence.
5. **Escalation/challenger** — what concrete gap permits another provider to enter.

A repository declaration fills (1), (2), and sometimes the intended challenger relationship. It does not automatically fill (3) or (4).

## Current evidence boundary

The WeChat case is the strongest retained quality evidence:

```text
wechat-article-search
  Operational (observed ZCode case) = AVAILABLE
  Semantic Coverage = EQUIVALENT
  Discoverability = LIMITED_OBSERVED

general web for WeChat discovery
  Semantic Coverage = DEGRADED
  Discoverability = VERY_LOW_OBSERVED
```

These observations are scoped to the recorded cases. They are not global quality rankings.

## Test-stage route (TASK-20260913-012)

A no-login WeChat discovery/canonicalization bridge was verified end-to-end on one discovery-required fixture and recorded as a **test-stage route**, not a production binding change. Declared provider ownership is unchanged; the adapter is unchanged.

```text
wechat.discovery (test-stage route)
  Sogou weixin public result page (session-scoped anonymous cookies)
    -> candidate title/account + wrapped /link?url= (evidence only, never canonical)
    -> same-session /link resolution (Referer-bound)
    -> JS-assembly canonical mp.weixin.qq.com URL
    -> Phase B verification (host, canonical form, title material match, account)
  helper: scripts/wechat_discovery.py (standard library only; CAPTCHA classified, never bypassed)
  tests: tests/test_wechat_discovery.py (offline, no network)

wechat.reader (test-stage route)
  web_reader fallback on a verified canonical URL
  (native web search restricted to site:mp.weixin.qq.com is an admissible discovery
   fallback, but its results are candidates and were observed to require Phase B
   rejection of wrong-article hits)
```

Observed boundary within the same run: the Sogou route succeeded for one fixture and failed at discovery for another (exact-title article absent from public indexes), reconfirming `LIMITED_OBSERVED` discoverability for WeChat article discovery as a class.

## Test-stage reachability profile (TASK-20260913-013)

Evidence-first profile from the mainland host, run entirely without proxy. Three axes stay separate (`discovery_status` / `local_direct_read` / `provider_remote_read`); they are never collapsed into one availability flag.

```text
github.com (control)        DIRECT_AVAILABLE
x.com (control)             DISCOVERABLE_BUT_NOT_DIRECTLY_READABLE (TCP timeout; DNS resolves)
cn.bing.com                 reachable frontend, foreign-content discovery weak
                            (zero en.wikipedia mentions in bounded queries; mainland-flavored results)
en.wikipedia.org (S1)       locally BLOCKED_TRANSPORT; NOT surfaced by cn.bing;
                            DISCOVERED and remotely read via Exa below
mcp.exa.ai (anonymous MCP)  DIRECT_AVAILABLE + REMOTE_READ_AVAILABLE (no key, no account)
```

Test-stage route (no-proxy mainland remote read):

```text
foreign source locally unreadable
  -> Exa anonymous hosted MCP (no-proxy reachable): web_search_exa surfaces the exact URL
  -> web_fetch_exa returns material Markdown for that URL
```

Observed boundary in the same run: `x.semantic` reuse via the existing vpsmanage/XActions surface is broken only at the SearchTimeline GraphQL queryId (HTTP 404; timeline read `getTweets` and canonical single-post read `getTweet` remain healthy through the unchanged envelope) — pending the Human's provider-repair decision, no `x.semantic` availability is claimed here.

## X provider repair validation (TASK-20260913-014)

Gate A validated the current upstream XActions (`nirholas/xactions` @ `f2fb3ed`) in an isolated runtime: the dynamic query-ID discovery machinery is real and operational (148 operations discovered live from x.com's own bundle, SearchTimeline ID refreshed, provenance recorded — not a hand-pinned ID). Search still fails with a bare 404 under fresh IDs, and a differential (timeline PASS vs followers/search bare-404 on BOTH the upstream clone and the production install) matches the upstream project's own documented session-tier signature: the stored ct0 is no longer honoured server-side for the full-session endpoint class. Outcome: repair is **not** a queryId fix; the decision surface is an Owner-side session refresh, after which the same fixtures can re-run and the dynamic machinery becomes the natural repair candidate. No vpsmanage branch/PR was created (Gate B gated on a Gate A pass). `x.semantic` availability remains unclaimed; production untouched.

## Machine map versus repository map

Keep two artifacts conceptually separate:

```text
Repository Capability Map
  = declared capabilities/providers/ownership rules

Machine Capability Receipt
  = discovered carriers + runtime exposure + representative probes
```

Only the second can answer whether a provider is actually usable on a particular machine/session.

Use `scripts/scan_skills.py` when the unresolved question is which Skill carriers are present under explicit roots. Then use Doctor/runtime evidence to determine operational capability. Skill presence alone is never promoted to `AVAILABLE`.
