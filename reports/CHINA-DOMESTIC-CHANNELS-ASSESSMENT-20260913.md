# China Domestic Channel Assessment — 2026-09-13

## Decision state

`READY_FOR_DOMESTIC_CHANNEL_DECISION`

This report supersedes the provisional YouTube-first direction recorded in `reports/TASK-20260913-011-GOAL-INTEGRITY-CUT.md`.

Human direction: stop before starting a new vertical and evaluate China-domestic information channels first.

No provider is installed, staged, logged in, configured, or promoted by this report.

## Selection principle

Do not create a first-class source semantic merely because a site is Chinese or popular.

Promote a platform to a specialist capability only when it exposes decision-relevant semantics that general web search/read cannot represent equivalently, such as:

- platform-native search/discovery;
- comments/replies/danmaku;
- hot/trending feeds;
- user/profile/feed semantics;
- video/audio subtitle or transcript retrieval;
- finance/community structured data;
- login/session-scoped content that legitimately requires a specialist path.

Ordinary public article sites (for example generic CSDN/Juejin/博客园-like pages) should remain under general-web.search/read unless a concrete retrieval gap appears.

## Existing modeled domestic capability

### WeChat

Already first-class:

```text
wechat.discovery
wechat.reader
```

Current status remains evidence-driven and separate from the new-channel decision. Do not merge WeChat into generic web or use it as a generic complex-web test target.

## High-value domestic candidates

| Channel | Unique information value | Current reusable route observed | Auth / anti-bot burden | Recommended stage |
|---|---|---|---|---|
| Bilibili | video search, metadata, comments/danmaku, subtitles | `bili-cli`; OpenCLI for subtitles; Agent-Reach has current routing | LOW-MEDIUM; search/detail can be anonymous | **P1 / strongest first vertical candidate** |
| V2EX | Chinese technical community topics/replies/users | public JSON API; Agent-Reach channel | LOW; no auth for core reads | **P1 / fastest low-risk win** |
| Xiaohongshu | consumer experience, local reviews, lifestyle, comments | OpenCLI desktop; `xpzouying/xiaohongshu-mcp` server; legacy xhs-cli | HIGH; login/session, xsec_token, captcha/rate controls | **P1 value, P2 execution** |
| Weibo | hot search, public posts/users/topics | `qinyuanpei/mcp-server-weibo` visitor-passport path | LOW-MEDIUM if anonymous visitor credential remains viable | **P1/P2** |
| Zhihu | Q&A, long-form answers/articles, comments, expert/community knowledge | multiple Playwright/internal-API MCP projects | MEDIUM-HIGH; persistent browser/login improves reliability | **P1/P2** |
| Xueqiu | China finance quotes, fundamentals, forum/news/comments | `CNQQC/xueqiu-mcp`; many anonymous endpoints | LOW for public finance/community reads; some account data requires login | **P2 specialist finance** |
| Xiaoyuzhou | Chinese podcast search/episodes/transcripts | read-only `r266-tech/xiaoyuzhou` CLI; Agent-Reach podcast route | MEDIUM; personal/history functions require auth | **P2 audio specialist** |
| Douyin | short-video discovery/content/creator signals | official-OpenAPI CLI exists; community MCPs mostly publishing/creator analytics/hosted data | HIGH; OAuth/login/browser/risk; public research path fragmented | **P3 until read-only discovery path is proven** |

## Channel notes

### Bilibili

Current upstream evidence is unusually favorable for a first vertical:

- `tamnd/bilibili-cli` exposes structured search and Bilibili object reads as a pure Go binary;
- its README claims anonymous bootstrap for public endpoints and optional cookies rather than mandatory login;
- Agent-Reach currently routes Bilibili search/detail to `bili-cli` and subtitles to OpenCLI;
- Agent-Reach explicitly warns not to use yt-dlp for Bilibili because current Bilibili anti-bot behavior returns 412 in that path.

Proposed semantic shape if later authorized:

```text
bilibili.discovery
bilibili.reader
bilibili.transcript
```

A single combined `bilibili.semantic` may be acceptable initially if the first implementation keeps discovery/detail/comments/subtitles distinguishable in receipts.

### V2EX

Strong low-cost specialist because general web does not equivalently expose thread/reply/user/node semantics, yet core data is available through public JSON APIs without login.

Proposed semantic:

```text
v2ex.community
```

This is likely the cheapest capability to establish and regression-test.

### Xiaohongshu

Very high information value, but operationally expensive:

- Agent-Reach currently has a three-backend route: OpenCLI -> xiaohongshu-mcp -> legacy xhs-cli;
- OpenCLI reuses an already-controlled Chrome session;
- xiaohongshu-mcp requires explicit login/cookie state and first-run browser provisioning;
- xsec_token and request-frequency constraints are platform semantics, not incidental implementation details;
- `xpzouying/xiaohongshu-mcp` remains actively released (v2.5.0 observed in Aug 2026), but recent issues show continuing login/network/risk friction.

Therefore Xiaohongshu should become a first-class specialist eventually, but it is a poor choice for the very first domestic vertical if the goal is rapid capability expansion with bounded operational risk.

Proposed semantics:

```text
xiaohongshu.discovery
xiaohongshu.reader
xiaohongshu.comments
```

### Weibo

`qinyuanpei/mcp-server-weibo` currently advertises public-user/post/trending/search access and an automatically generated visitor-passport credential path without manual cookie setup. This is promising enough for a bounded anonymous-read probe before any login-capable design.

Proposed semantic:

```text
weibo.discovery
weibo.reader
weibo.trends
```

### Zhihu

There are now multiple active community MCP implementations. The strongest read-oriented designs expose search, question, answer, article, comment, user and activity semantics, but typically depend on Playwright/persistent cookies/internal APIs.

Proposed semantics:

```text
zhihu.discovery
zhihu.reader
zhihu.comments
```

Treat publishing-oriented Zhihu MCPs as a different product concern; external-knowledge should remain read-first.

### Xueqiu

`CNQQC/xueqiu-mcp` is a notably mature specialist candidate: it exposes quotes, financials, flows and community/forum data and currently documents anonymous token acquisition for many reads, with login required only for some WAF/account-specific paths.

This is valuable but domain-specific; it should not outrank broad Chinese knowledge/community channels unless finance becomes a primary user need.

Proposed semantic:

```text
xueqiu.market
xueqiu.community
```

### Xiaoyuzhou

`r266-tech/xiaoyuzhou` provides a read-only CLI with podcast/episode search, metadata and official transcript support, plus auth-scoped subscriptions/history. This is a good example of a clean specialist surface but narrower than Bilibili/V2EX/Weibo/Zhihu.

Proposed semantic:

```text
xiaoyuzhou.discovery
xiaoyuzhou.transcript
```

### Douyin

Current open-source landscape is fragmented:

- one current Rust CLI exposes an official OpenAPI/MCP route with OAuth-oriented configuration;
- several community MCP projects focus on publishing or creator-center analytics rather than broad public information retrieval;
- hosted public-research services exist but hide the implementation.

Do not promote a Douyin provider until a legitimate read-only discovery/read surface is directly verified. Avoid browser/login automation merely to claim channel coverage.

## Recommended domestic expansion order

### Track A — fastest reliable coverage

```text
1. Bilibili
2. V2EX
3. Weibo
```

Why: each adds genuinely new source semantics; Bilibili/V2EX already have comparatively low-auth read paths, and Weibo has a promising anonymous visitor path.

### Track B — high-value but session-heavy

```text
4. Zhihu
5. Xiaohongshu
```

Why: very valuable Chinese knowledge/consumer content, but browser/login/cookie/anti-bot lifecycle must be designed deliberately.

### Track C — domain/niche specialists

```text
6. Xueqiu
7. Xiaoyuzhou
8. Douyin (after a read-only retrieval route is proven)
```

## Recommended next decision

Do not reopen TASK-011 and do not start YouTube yet.

The next vertical should be selected from the domestic P1 candidates.

Recommended default:

```text
Bilibili first
```

with V2EX as the alternative if the Human wants the lowest-risk/fastest capability win.

No Arena/provisioning authorization is implied by this assessment.
