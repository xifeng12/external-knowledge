# TASK-20260912-004 — Capability Arena / Complex Web Read: WebFetch vs Crawl4AI

## State

`READY_FOR_ARENA_REVIEW` — Arena cleanup status: **CLEAN_VERIFIED**

- Contract: `tasks/TASK-20260912-004-CAPABILITY-ARENA-COMPLEX-WEB.md` (Arena contract v0.2)
- Match id: `TASK-20260912-004-complexweb-001`
- Receipts: `evidence/arena/TASK-20260912-004-complexweb-001/{defender,challenger,adjudication}.json`
- Executed at remote head `30687d0` (branch `task/20260912-001-v04-capability-diagnostics`); authority re-read per contract start state.

## 1. Real-Scenario Admission Gate — PASSED (no staging before the gate)

Selected case (preferred candidate #1): the canonical WeChat article preserved by TASK-20260912-002 P7 — "阿里又一个 20k+ stars 开源项目诞生，恭喜 fastjson！" (author 杨立滨). The P7 evidence recorded the harvest chain (doocs/md USERS.md via `github.semantic`) but not the URL string, so the gate re-derived the URL deterministically from that recorded chain (`https://mp.weixin.qq.com/s/RNKDCK2KoyeuMeEs6GUrow` — first link in USERS.md), confirmed the author against the P7 record, and verified reachability (HTTP 200, 3.2 MB, 2.5 s). The exact URL is now durably recorded in the match receipts. No synthetic/demo page was used; no discovery fan-out was needed.

Admission-relevant baseline observation (orchestrator check, not a contestant op, used only as adjudicator reference): a plain `curl` with a browser UA received the **real article page** — the anti-bot gate is automation-fingerprint-based, not IP- or paywall-based.

## 2. Defender admission and result

`runtime-native.webfetch` was attempted on the target (bounded 1+1). Observed native chain in this runtime: the WebFetch tool is hook-redirected by the host control plane to the context-mode fetcher (`ctx_fetch_and_index`), which is the effective native read path. Both attempts returned the **WeChat anti-bot verification page** ("环境异常…去验证", ~0.2 KB) — 0/4 objective fields (title/author/metadata/body). Fast-fail ~2–3 s per attempt. This reproduces, on today's network, the same WeChat anti-bot failure domain recorded historically in `runtime-notes-zcode.md`.

## 3. Challenger baseline, staging, and result

Baseline: crawl4ai absent from all Python environments; `PLAYWRIGHT_BROWSERS_PATH` unset; pre-existing `%LOCALAPPDATA%\ms-playwright` cache (chromium-1208 era + mcp-chrome) present and never touched; arena root absent.

Ephemeral staging (all Arena-owned, all in-cell): venv with `crawl4ai==0.9.3` + deps (697 MB; pip cache in-cell, 190 MB); match-scoped Playwright `chromium-1234` / Chrome for Testing 151.0.7922.34 + headless shell + ffmpeg (703 MB) via `playwright install chromium` with cell-scoped `PLAYWRIGHT_BROWSERS_PATH`. No LLM/API keys, no `crawl4ai-setup`-style side-effect helpers (TASK-002 Camoufox precedent), no persistent install. One staging friction event: the playwright CDN stalled at 0% for ~16 min on the direct connection; the retry used a **per-command** `HTTPS_PROXY` env var (no persistent proxy change) and completed all downloads from the official CDN.

Match attempts (bounded 1+1, provider-default `CrawlerRunConfig`, no anti-detection options):

```text
attempt 1 (primary): crawler executed; output lost before recording — orchestrator driver bug
                     (crawl4ai.__version__ is a module; JSON serialization crash). Disclosed.
attempt 2 (retry):   tool-level success=True, fetch 4163 ms; content = the SAME WeChat anti-bot
                     verification page (heading '环境异常', ~20 KB HTML, no js_content, no article
                     metadata); 0/4 objective fields.
```

## 4. Adjudication — REJECT_CHALLENGER (scoped)

Both contestants, under default configurations and the bounded budget, were identically fingerprint-blocked by the same WeChat anti-bot surface — correlated failures, **no demonstrated failure-domain independence** (different mechanism: plain HTTP client vs local chromium, same outcome). The challenger staged and ran mechanically correctly but demonstrated **zero extraction advantage at materially higher cost**: ~1.59 GB ephemeral footprint, CDN stall + proxy retry, venv/browser lifecycle burden.

- `KEEP_INCUMBENT` hypothesis ("native is sufficient") does not hold as stated — the defender failed the case too.
- `SPLIT_BY_SCENARIO` / `FUSE_VALIDATED_STRENGTHS` fail: Crawl4AI did not earn an escalation role — the escalation chain breaks exactly where the gap appears (it does not fill the gap).
- `REJECT_CHALLENGER` matches the evidence precisely per Arena v0.2: operational, but no justified active-challenger role **for this ownership question**. As a capable loser it remains eligible for a future scenario-specific re-challenge (e.g., with explicitly authorized anti-detection configuration such as crawl4ai's documented `magic`/`simulate` options, which were out of bounds here).

**Scope limits (contract §8):** one real case, one runtime, default configurations, 1+1 attempts. No claim about Crawl4AI's general extraction quality or non-anti-bot JS-heavy pages.

**Routing impact: none.** `complex-web.read` stays `AVAILABLE_WITH_SCOPE` under the native DEGRADED path; the observed extraction fallback for this source remains `web_reader` (TASK-002 P7, which did read this exact page). Terminal state therefore `READY_FOR_ARENA_REVIEW`, not `READY_FOR_ROUTING_CHANGE_DECISION`.

## 5. Teardown

All Arena-owned artifacts removed and verified: no chrome/python processes; 1.6 GB cell deleted and confirmed absent; crawl4ai not importable on host python; `PLAYWRIGHT_BROWSERS_PATH` was per-command only; no crawl4ai registration in any inspected config domain; pre-existing ms-playwright cache untouched (no chromium-1234 leaked there — install logs prove all four Arena downloads landed in the cell); repository tree contains only intended durable outputs. Orchestrator gate temp files removed.

```text
classification: CLEAN_VERIFIED
caveat: the pre-staging baseline listing truncated the ms-playwright directory to 3 entries
(head -3), so pre-existence of user-cache entries ffmpeg-1011/winldd-1007/mcp-chrome is not
fully distinguishable; they are conservatively treated as not Arena-owned (install-log
evidence shows the match wrote only into the cell) and were left untouched.
residue: none Arena-owned.
```

## 6. Arena contract evolution (§11)

One reusable provider-agnostic invariant was exposed and is recorded here rather than in the generic contract: **default read paths must be fingerprint-tested against the target before concluding a capability gap** — both contestants' failures were automation-fingerprint blocks, and only the orchestrator's UA-pinned baseline distinguished "blocked" from "unreachable". Provider-specific behavior (WeChat gate, crawl4ai staging friction) stays in this report/receipts. No generic harness built; skill-forge integration not needed for this match.

## 7. Authorization discipline

Not performed: persistent install, system/user Python or PATH mutation, OS-level deps, browser profiles/cookies/credentials, proxy/TLS persistence (the per-command proxy env var left no state), LLM/API extraction, other Challengers, adapter/routing change, PR #3/main merge. The driver-bug-lost attempt is disclosed in the challenger receipt rather than silently retried beyond budget.
