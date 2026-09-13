# X Provider Alternatives Assessment — 2026-09-13

State entering review: `X_PROVIDER_ALTERNATIVE_REQUIRED` after TASK-016. XActions remains accepted for account timeline / known-post read, but all further XActions search/session/query-ID hardening is stopped.

## Decision target

Replace only the missing search leg:

```text
query
  -> real X posts
  -> numeric Post ID
  -> canonical https://x.com/<user>/status/<id>
  -> material post content
```

Do not replace the working `vpsmanage` timeline/post-read monitor unless evidence later requires it.

## Candidate classes

### P0 — Existing Exa hosted MCP, domain-restricted X discovery probe

Why first:
- already demonstrated directly reachable from the mainland host without proxy;
- anonymous hosted MCP already works in this project;
- no new account, API key, browser, X session, proxy, or persistent install required for a bounded probe;
- Exa Search supports domain inclusion filters, so a probe can restrict discovery to `x.com` / `twitter.com`.

Uncertainty:
- Exa documentation proves domain filtering, not that its index has sufficient current X-post coverage;
- even if it returns X posts, it may be discovery-oriented rather than equivalent to platform-native Latest/Top search.

Decision: **FIRST PROBE**, not yet a provider promotion.

### P1 — SocialData remote X API / MCP

Current documented surface:
- real X search endpoint with website-style operators;
- plain REST JSON and MCP surface;
- public-data/read-only orientation; no connected X account required;
- $0.0002 per tweet/profile returned ($0.20 / 1000 items), pay-as-you-go; no subscription requirement.

Strength:
- strongest clean failure-domain separation from XActions: provider operates the X retrieval layer remotely;
- exactly matches the missing `x.search` semantic and returns structured X data.

Cost/unknowns:
- requires SocialData account/API key and positive balance for sustained use;
- mainland no-proxy reachability not yet tested;
- third-party service dependency.

Decision: **PRIMARY PAID FALLBACK** if P0 fails or coverage is inadequate.

### P2 — Official X API v2 Search Posts

Current official surface:
- `/2/tweets/search/recent` for recent search; `/2/tweets/search/all` for full archive;
- official supported operators including `from:`, keywords, hashtags, language, etc.;
- pay-per-use, no subscription; current documented Post read cost $0.005 per returned Post; 24-hour deduplication; 2M post-read/month pay-per-use cap.

Strength:
- authoritative / most stable contract;
- independent of browser cookies and private GraphQL behavior.

Cost/unknowns:
- requires X developer account/app/credentials and prepaid credits;
- materially more expensive per returned post than SocialData/TwitterAPI.io for this use case;
- mainland reachability not yet tested.

Decision: **AUTHORITATIVE FALLBACK**, especially if long-term compliance/stability dominates cost.

### P3 — TwitterAPI.io remote API

Current documented pricing:
- advanced tweet search around $0.15 / 1000 returned tweets;
- pay-per-use foundation.

Strength:
- provider-side retrieval gives a different failure domain from local X sessions;
- low unit price.

Unknowns:
- mainland reachability and exact result/canonical-ID contract need live validation;
- third-party dependency and operational trust need comparison against SocialData.

Decision: **SECOND REMOTE-API CANDIDATE**; compare only if P1 is unattractive or fails.

### P4 — OpenCLI Twitter browser adapter

Current project evidence:
- built-in `twitter search`, including live/latest filtering;
- browser mode reuses a logged-in Chrome session;
- very active/popular project with broad browser-adapter surface.

Strength:
- real browser/session execution is a genuinely different X surface from the failed HTTP-only XActions search path;
- likely closest to what a Human can search in the X UI.

Cost/unknowns:
- requires a logged-in browser plus an X-reachable network path;
- heavier operational surface for unattended/server-side agents;
- browser/runtime coupling and account/session lifecycle remain.

Decision: **BEST LOCAL/BROWSER FALLBACK**, but behind provider-side approaches for external-knowledge.

### P5 — `yashiels/twitter-cli`

Current project evidence:
- active through 2026-09-06;
- Go CLI; `twt search` supported;
- uses private Android GraphQL (`api.twitter.com/graphql`) reverse-engineered from X Android APK;
- authentication uses `auth_token + ct0` browser session cookies.

Strength:
- protocol/query family differs from XActions web GraphQL, so it is not a pure wrapper replacement;
- lightweight and easy to stage in isolation.

Risk:
- still depends on the same Human X account/session class;
- private API reverse engineering can break with app/API changes;
- includes write operations, so any external-knowledge use would require an explicit read-only wrapper/allowlist.

Decision: **FREE PROTOCOL-DIFFERENT CANDIDATE**, behind remote providers and OpenCLI.

### Lower priority — `public-clis/twitter-cli`, `tamnd/x-cli`

`public-clis/twitter-cli` has search, full-cookie forwarding, TLS impersonation and live query-ID fallback; this makes it more browser-like than the minimal two-cookie XActions path, but it still uses X web GraphQL and has significant anti-detection/session operational burden.

`tamnd/x-cli` is a strong read-only pure-Go design, but its `x search` is explicitly Tier-2 session GraphQL using `auth_token + ct0`; that is too close to the failure class TASK-016 just exhausted. Keep it for public/timeline/thread reads, not as the first search alternative.

## Recommended execution order

```text
1. P0 Exa x.com-domain discovery probe
   - no new credentials/provisioning
   - proves whether an already-qualified mainland-reachable provider can fill the gap

2. If P0 fails coverage/recency:
   P1 SocialData reachability + tiny paid/search qualification

3. If third-party provider is rejected or insufficient:
   P2 official X API recent search

4. Browser/local alternative:
   P4 OpenCLI

5. Free protocol-different experiment only if needed:
   P5 yashiels/twitter-cli
```

Do not stage `tamnd/x-cli` or another two-cookie web-GraphQL client before these higher-information alternatives.

## Proposed next task shape

The next task should be a small **provider-alternative qualification**, not an Arena. First gate is P0 only:

```text
Exa anonymous hosted MCP from mainland host, no proxy
  -> restrict/target results to x.com / twitter.com
  -> run two frozen X search fixtures:
       A. account-scoped discovery (known public account)
       B. keyword/current-topic discovery
  -> require real `/status/<numeric-id>` URLs
  -> require material post text/snippet or successful provider-side fetch
  -> record recency and false-positive rate
```

If P0 cannot supply real, sufficiently current X posts, stop P0 cleanly and move to an explicit credential/cost decision for P1; do not silently stage paid providers.