---
task_id: TASK-20260913-012
status: ready_for_wechat_vertical_execution
parent_task: TASK-20260912-001
target_repo: xifeng12/external-knowledge
implementation_branch: task/20260912-001-v04-capability-diagnostics
capability_scope:
  - wechat.discovery
  - wechat.reader
persistent_provisioning_authorized: false
cookie_or_login_authorized: false
browser_provisioning_authorized: false
production_merge_authorized: false
---

# TASK-20260913-012 — WeChat Minimum End-to-End Vertical

## Goal

Complete the shortest useful WeChat public-account knowledge path before starting X/Twitter work:

```text
query / title / account
  -> discover article candidates
  -> obtain and verify canonical mp.weixin.qq.com URL
  -> read canonical article body as Markdown/text
```

This is vertical capability completion, not another provider leaderboard.

## Current accepted evidence

From TASK-002:

```text
wechat.discovery = MISSING_CONFIRMED
Sogou search endpoint = reachable and returns real results
Sogou /link resolution = CAPTCHA-gated for automated clients
wechat.reader specialist exposure = MISSING_CONFIRMED
web_reader = already-exposed fallback with one successful real canonical WeChat article read
wechat-to-md = healthy carrier but blocked on ~493 MB Camoufox browser provisioning
```

Therefore the current bottleneck is discovery/canonical-link resolution, not body reading.

## Scope and priority

### Phase A — Discovery first

Re-verify the smallest no-login paths that can yield direct canonical WeChat article URLs.

Allowed discovery ingredients, in this order:

1. existing Sogou WeChat result page as candidate generator;
2. existing native/general web search restricted to `site:mp.weixin.qq.com/s` as a canonical-URL resolver/discovery fallback;
3. small match-scoped/read-only reference probes inspired by maintained public implementations (for example multi-source Google/Bing/Sogou discovery or Sogou resolver approaches), only when needed to resolve a concrete gap.

Do not treat a wrapped Sogou `/link` URL as a canonical article URL.

Do not bypass CAPTCHA, automate verification, import cookies, or repeatedly hammer an anti-bot page.

### Phase B — Canonical verification

For every candidate promoted to a usable result, verify at minimum:

```text
final host = mp.weixin.qq.com
article URL form is canonical/public
returned title materially matches the discovery candidate
publisher/account identity is preserved when observable
```

Search results are candidates, not truth.

### Phase C — Reader reuse

Once a canonical URL is obtained, use the already-exposed `web_reader` fallback first.

Success means recovering enough to satisfy:

```text
title
publisher/author when available
material body text
stable source URL
```

Do not provision Camoufox or re-bind `wechat-to-md` in this task. Local image archival/frontmatter/batch conversion are not required for the minimum vertical.

## Controlled verification set

Use a small bounded set of public WeChat articles with known canonical URLs/titles. Reuse the retained TASK-002 article as one fixture when still reachable, and add only enough additional fixtures to distinguish a one-off from a repeatable path.

Target size:

```text
3 fixtures maximum
```

At least two should require discovery from title/keywords rather than being supplied directly as canonical URLs.

For each fixture record:

```text
input query/title/account hint
discovery path used
candidate title/account/date if available
wrapped URL if returned (for evidence only)
canonical URL obtained or not
canonical verification result
reader result
failure stage if any
```

Do not store full article bodies; compact hashes/field summaries are sufficient.

## Minimal implementation rule

If an existing callable path cannot bridge candidate -> canonical URL, a minimal repository-owned no-login discovery helper may be implemented only if all of these hold:

```text
it solves the concrete bridge gap
it uses public search/result pages or existing native search only
it does not bypass CAPTCHA/access controls
it does not require credentials/cookies/browser automation
it stays narrowly scoped to WeChat discovery/canonicalization
```

Do not import an entire third-party framework just to get one function.

If implemented, add focused tests for URL normalization/candidate verification and keep source ownership under `wechat.discovery`.

## Decision outputs

Preferred successful terminal state:

```text
WECHAT_MINIMUM_VERTICAL_AVAILABLE
```

with an explicit test-stage route such as:

```text
wechat.discovery
  -> <verified no-login discovery/canonicalization path>

wechat.reader
  -> web_reader fallback
```

If discovery remains blocked without login/browser/credential provisioning, stop at:

```text
READY_FOR_WECHAT_DISCOVERY_PROVISION_DECISION
```

Do not compensate by provisioning X/Twitter in the same task.

## Durable outputs

Write:

```text
reports/TASK-20260913-012-WECHAT-MINIMUM-END-TO-END.md
evidence/TASK-20260913-012-wechat-minimum-receipt.json
```

If repository code/adapter/capability-map is changed, include exact tests/validation and explain the provider/source-semantic binding.

## Authorization boundary

Authorized:

- read-only public discovery probes;
- current native search/web tools;
- current already-exposed `web_reader`;
- small ephemeral scripts/files for bounded probing;
- minimal repository helper implementation when required by the concrete discovery bridge gap.

Not authorized:

- login or account creation;
- cookie/browser-profile import or reading;
- CAPTCHA bypass or verification automation;
- Camoufox/browser download;
- persistent external provider install/registration;
- WeChat write actions;
- X/Twitter provisioning;
- PR #3 merge or merge to `main`.

## Stop

Push the report/receipt and any narrowly necessary repository changes, synchronize Issue #2, then stop at the first terminal state above.
