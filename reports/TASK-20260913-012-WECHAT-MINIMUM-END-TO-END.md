# TASK-20260913-012 — WeChat Minimum End-to-End Vertical

```text
task_id: TASK-20260913-012
status: WECHAT_MINIMUM_VERTICAL_AVAILABLE (test-stage route; not a production binding change)
parent: TASK-20260912-001
branch: task/20260912-001-v04-capability-diagnostics
receipt: evidence/TASK-20260913-012-wechat-minimum-receipt.json
```

## What this task set out to do

Complete the shortest useful WeChat knowledge path — query/title → discover
candidates → obtain and verify a canonical `mp.weixin.qq.com` URL → read the body
via the already-exposed `web_reader` fallback — using a bounded verification set of
at most 3 fixtures (≥2 requiring discovery), with no login, no cookie/profile
import, no CAPTCHA bypass, no browser download, and no persistent provisioning.

## The discovery bridge that was found

TASK-002 established that Sogou `/link` resolution was CAPTCHA-gated for automated
clients. This run found a working no-login variant of that bridge, verified on a
real fixture:

```text
1. GET weixin.sogou.com/weixin?type=2&query=...        (public result page, no login)
2. extract candidates: title + account + wrapped /link?url=
3. GET the /link URL with the SAME session cookies + Referer
   -> response body is a JS-assembly page (no CAPTCHA this time)
4. concatenate the url += '...' fragments
   -> https://mp.weixin.qq.com/s?src=11&timestamp=...&signature=...
5. Phase B: verify host, canonical form, title material match, account
6. Phase C: read via web_reader
```

The only cookies involved are the anonymous ones Sogou itself sets during this
request flow, held in a session-scoped jar and never persisted. CAPTCHA bodies are
classified and treated as a stop condition, never bypassed.

## Verification set results

| Fixture | Class | Discovery | Canonical URL | Phase B | Reader |
|---|---|---|---|---|---|
| F1 `ArcPy使用之一：SDE数据定时备份` (图说新语) | discovery-required | FAILED | none | 2 candidates rejected | not reached |
| F2 `不可不知的 ArcGIS Python 开发 PPT` | discovery-required | OK (Sogou, account GIS前沿) | OK (signed_query, assembled) | PASS | PASS |
| F3 `https://mp.weixin.qq.com/s/RNKDCK2KoyeuMeEs6GUrow` | supplied canonical URL | not required | OK (public_slug) | PASS | PASS |

### F2 — full vertical success

Sogou returned 5 candidates with the top match titled
`不可不知的ArcGIS Python开发(PPT可下载)` by account `GIS前沿`. Same-session `/link`
resolution produced a signed canonical URL, which verified (HTTP 200, correct host
and form, matching account) and then read end-to-end via `web_reader`:

```text
title    不可不知的ArcGIS Python开发（PPT可下载）
author   李远祥 (og:article:author)
account  GIS前沿
body     intro paragraphs + PPT page images + 资料下载 closing (发送 0718)
```

This is the first complete discovery → canonicalization → verification → read
vertical for WeChat in the project's evidence base, achieved with no login and no
browser.

### F1 — honest discovery failure (retained as evidence)

- Sogou: exact-title query → 0 candidates; shortened query → 20 candidates, all
  irrelevant; keyword-set query → empty page (Sogou left as-is per the no-hammer
  rule after prior attempts).
- Native web search with quoted exact title → no `mp.weixin.qq.com` candidates at
  all (only cnblogs/CSDN/Esri/GitHub pages).
- Native web search (backend-rewritten `site:`-restricted) → 2 `mp.weixin.qq.com/s/`
  candidates. Phase B read both and **rejected both as wrong articles**
  (`明确AI使用边界，国内期刊AIGC审查跟踪解读来了！` by 常湘萍; an unrelated
  高墙履职 profile). "Search results are candidates, not truth" did real work here.

This reproduces the historical `LIMITED_OBSERVED` discoverability of this exact
article: it is effectively absent from public indexes reachable without WeChat
ecosystem access. The failure is retained deliberately — it bounds what the new
route can claim.

### F3 — reader reuse on a retained canonical URL

`web_reader` again recovered title (`阿里又一个 20k+ stars 开源项目诞生，恭喜
fastjson！`), author (杨立滨), and material body from the TASK-002 retained URL,
confirming the reader leg is repeatable on `public_slug` form URLs.

## Test-stage route (recorded in capability-map)

```text
wechat.discovery
  -> Sogou weixin public result page (session-scoped anonymous cookies)
     -> candidates (title/account/wrapped /link)
     -> same-session /link resolution
     -> JS-assembly canonical URL
     -> Phase B verification
     helper: scripts/wechat_discovery.py

wechat.reader
  -> web_reader fallback on a verified canonical URL
     (native web search restricted to site:mp.weixin.qq.com is an admissible
      discovery fallback; its hits are candidates and must pass Phase B)
```

## Minimal repository helper

`scripts/wechat_discovery.py` (standard library only) implements exactly the
verified bridge plus its verification logic:

- `classify_mp_url` / `is_canonical_mp_url` — canonical-form rules; a wrapped
  `/link?url=` is never canonical, `public_slug` and `signed_query` are the two
  admissible article forms;
- `extract_results` — candidate title/account/link extraction from result pages;
- `classify_link_body` — `captcha` / `js_assembled` / `js_replace` / `unknown`;
- `extract_article_fields` + `verify_candidate` — Phase B fields and title
  material match (width/punctuation-tolerant);
- `SogouDiscovery` — the session-scoped no-login flow with pacing and a hard stop
  on CAPTCHA; stdout JSON CLI (`search` / `discover` / `verify`), no file writes.

`tests/test_wechat_discovery.py` adds 14 offline tests covering URL
classification, candidate extraction, link-body classification (including the
captcha stop), article field extraction, and title matching — including the
F1 case itself: a wrong-article candidate must fail verification. Result:
**14 passed**. No provider binding, adapter, or declared specialist changed; the
helper stays under `wechat.discovery` ownership as the contract requires, and the
capability-map change is explicitly marked test-stage.

## Environment / validation notes

- Baseline test run at HEAD `2c8e88c` (before any TASK-012 change): 34 passed,
  1 failed —
  `test_v04_diagnostic_contract.py::test_machine_diagnostics_requires_explicit_roots_and_explicit_claims`.
  The cause is wording drift (`references/machine-diagnostics.md` now says
  "do not execute Skill code"; the test still asserts the older
  "does not execute Skill code"). Pre-existing and outside TASK-012's authorized
  scope; recorded here as baseline debt rather than fixed in this task.
- The signed-query canonical URL for F2 is session-scoped and may expire; the
  `public_slug` form (as in F3) is the durable public form when obtainable.
- No full article bodies were stored; the receipt carries field summaries only.

## Authorization boundary compliance

No login or account creation; no cookie/browser-profile import (only Sogou's own
anonymous session cookies); no CAPTCHA bypass or verification automation; no
Camoufox or browser download; no persistent provider install/registration; no
WeChat write actions; no X/Twitter provisioning; no PR #3 / main merge. All
probing used public result pages, current native search, the already-exposed
`web_reader`, and small ephemeral scripts plus the narrowly scoped repository
helper the contract permits.

## Stop

Pushed to `task/20260912-001-v04-capability-diagnostics`; Issue #2 synchronized.
Stopping at the first terminal state:

```text
WECHAT_MINIMUM_VERTICAL_AVAILABLE
```

The next Human decision surface is whether/when to promote this test-stage route
(or provision a discovery specialist) given F1's demonstrated discovery boundary.
