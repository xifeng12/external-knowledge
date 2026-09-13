---
task_id: TASK-20260913-007
status: ready_for_controlled_benchmark_execution
parent_task: TASK-20260912-001
supersedes_test_gate: TASK-20260913-006
target_repo: xifeng12/external-knowledge
implementation_branch: task/20260912-001-v04-capability-diagnostics
arena_contract: references/capability-arena.md
arena_version: v0.4
evidence_class: CONTROLLED_BENCHMARK
capability: complex-web.read
defender: runtime-native.webfetch
challenger: unclecode/crawl4ai
challenger_version_target: 0.9.3
ephemeral_challenger_staging_authorized: true
match_scoped_browser_staging_authorized: true
persistent_provisioning_authorized: false
production_routing_authority: false
pr_merge_authorized: false
---

# TASK-20260913-007 — Complex Web Controlled Benchmark

## Goal

Run the corrected second Arena as a **controlled test-stage benchmark**, not as a live production-routing decision.

Contestants:

```text
capability: complex-web.read
Defender: runtime-native.webfetch
Challenger: unclecode/crawl4ai 0.9.3
Evidence class: CONTROLLED_BENCHMARK
```

The benchmark is deliberately designed to isolate increasingly complex extraction/rendering behavior with known, inspectable ground truth.

This task restores the Human's original intent to test the Challenger–Defender mechanism. TASK-006's inability to find a retained real ordinary-URL case remains factual but is not a blocker for this controlled benchmark.

## Authority and evidence boundary

Before execution, read:

- `references/capability-arena.md` v0.4;
- `references/source-ownership.md` and `references/capability-map.md`;
- `reports/TASK-20260913-006-TEST-STAGE-REVIEW.md`;
- this task;
- current remote branch head and Issue #2.

This task may produce a benchmark advantage, candidate rejection, or a scenario hypothesis. It MUST NOT change production routing/source ownership.

Always record:

```text
production_routing_authority: false
routing_impact: none
```

A Challenger benchmark win that would imply a production change stops at:

```text
READY_FOR_REAL_WORLD_VALIDATION
```

## Benchmark platform

Use the public `web-scraping.dev` test platform. It is intentionally designed for web-scraping testing and provides controlled static and dynamic scenarios.

Preflight the exact fixtures immediately before staging. If their observable contract has materially changed, stop at:

```text
READY_FOR_BENCHMARK_REDESIGN
```

Do not substitute unrelated live production websites merely to keep the match running.

## Source-Semantic gate

These fixtures are used as **controlled extraction/rendering ground truth**, not to retrieve GitHub, WeChat, versioned-doc, or another specialist semantic.

Therefore they are admissible for the generic `complex-web.read` CONTROLLED_BENCHMARK.

Do not use benchmark performance to infer specialist-source performance such as WeChat.

# Benchmark suite

Run the three fixtures below in order.

## B0 — Static structure control

Target:

```text
https://web-scraping.dev/product/1
```

Purpose:

```text
ordinary HTML extraction sanity check
main-content precision
heading/metadata preservation
table/structured-content preservation
```

Ground-truth anchors to verify at preflight and freeze in the receipt:

```text
title: Box of Chocolate Candy
current price: $9.99
main description exists
Features Vertical Table exists
brand = ChocoDelight
Packs Horizontal Table exists
5 package rows are present
```

Minimum pass:

```text
correct title
correct current price
main description materially recovered
brand field recovered
table structure or equivalent row/value relationships preserved sufficiently to recover at least 4 of 5 pack rows
```

A provider that cannot pass B0 has not demonstrated baseline suitability for this benchmark.

## B1 — JavaScript / GraphQL rendered-content test

Target:

```text
https://web-scraping.dev/reviews
```

Purpose:

```text
distinguish shell-only HTTP extraction from rendered dynamic content recovery
```

Ground-truth contract:

```text
page title: Latest Product Reviews
actual review records are loaded dynamically via JavaScript / background GraphQL requests
page exposes Load More behavior
```

Minimum evidence levels:

```text
FAIL:
  only shell/navigation/title/Load More control, no actual review record content

PARTIAL:
  at least one real review record is recovered after generic rendering, without site-specific selectors/API calls

STRONG:
  multiple review records are recovered with useful text/metadata structure using only generic documented read/render behavior
```

No direct hidden-GraphQL/API shortcut is allowed in this match; the capability under test is web reading/extraction, not reverse-engineering the site's API.

## B2 — Progressive / infinite-scroll test

Target:

```text
https://web-scraping.dev/testimonials
```

Purpose:

```text
measure progressive dynamic-content recovery beyond the initial document/read result
```

Ground-truth contract to preflight and freeze:

```text
heading: What do our users say?
aggregate count: 60 reviews/testimonials
initial ordinary read exposes only the first batch (currently 10 testimonial texts)
additional items are client-side progressive/infinite-scroll content
```

Result levels:

```text
FAIL:    <= 10 testimonial records recovered
PARTIAL: 11-59 recovered
STRONG:  60 recovered
```

The aggregate count itself is not equivalent to recovering the records.

# Two execution profiles

The benchmark distinguishes zero-configuration behavior from documented generic dynamic-read capability.

## Profile P0 — DEFAULT_READ

For B0/B1/B2:

- use the provider's normal/default read behavior;
- no site-specific selector, script, hidden API call, custom DOM query, or target-specific wait;
- one primary attempt per fixture;
- retry only for a concrete transport/tool/runtime transient.

## Profile P1 — GENERIC_DYNAMIC_READ

Run only for B1/B2 when the provider exposes a documented generic render/full-page/scroll/read capability.

Allowed:

```text
generic JavaScript rendering
generic wait-for-render/network-idle behavior
generic full-page scan/scroll behavior
provider-documented non-target-specific dynamic-read option
```

Disallowed:

```text
site-specific CSS/XPath selectors
custom JavaScript written specifically for these fixtures
direct GraphQL/hidden API calls
hard-coded testimonial/review strings
configuration learned from the opponent's output
```

If a contestant has no generic dynamic-read profile, record:

```text
UNSUPPORTED
```

Do not invent an equivalent mechanism for fairness theater. Capability difference is part of the test.

# Fairness and attempt budget

Each contestant receives the same objective and ground truth.

The same target may be run under P0 and P1 because those are declared benchmark profiles, not retries.

Within each fixture/profile:

```text
1 primary attempt
+ at most 1 retry only for concrete transport/tool/runtime failure
```

A valid but incomplete/wrong content result is not a transient error and does not earn a free retry.

Do not tune after seeing the opponent's result.

# Challenger staging

If Crawl4AI is not already operational in an authorized supported exposure, ephemeral staging is authorized for this task.

Reuse the previously tested version pin where available:

```text
crawl4ai==0.9.3
```

All match artifacts must remain in a match-scoped Arena cell:

```text
%TEMP%/external-knowledge-arena/<match-id>/
  venv/
  browser/
  cache/
  profile/
  config/
  evidence/
```

Before staging, record:

```text
baseline
Provision Plan
Rollback Plan
Promotion Plan
Teardown Plan
```

If browser binaries are required, force them into the match cell. No persistent user/system Python, PATH, MCP registration, browser profile, or cache mutation.

A per-process network/proxy override is NOT implicitly authorized. If downloads cannot complete under current network state without changing proxy/TLS behavior, stop at `READY_FOR_CRAWL4AI_STAGING_REDESIGN` unless current repository authority explicitly grants that exact bounded override.

No LLM/API-key extraction is allowed.

# Evidence and adjudication

Write:

```text
reports/TASK-20260913-007-COMPLEX-WEB-BENCHMARK.md
evidence/arena/<match-id>/defender.json
evidence/arena/<match-id>/challenger.json
evidence/arena/<match-id>/adjudication.json
```

The receipts must preserve, per fixture/profile:

```text
exact target
preflight ground truth
provider/profile
attempt count and retry reason
fields/records recovered
structure preservation evidence
render/dynamic recovery evidence
timing/resource evidence
errors
```

Do not commit full page bodies when compact field/record summaries and hashes are sufficient.

Adjudicate dimensions separately; no arbitrary aggregate score.

At minimum compare:

```text
B0 baseline correctness
B1 rendered dynamic-content recovery
B2 progressive-load recovery
precision/boilerplate
structure preservation
determinism
fetch/runtime cost
staging footprint
operational burden
agent ergonomics
```

# Interpretation rules

Possible benchmark conclusions include:

```text
KEEP_INCUMBENT
  challenger adds no material controlled-test advantage for the declared contract

SPLIT_BY_SCENARIO
  benchmark hypothesis: native read is sufficient for ordinary/static pages while Crawl4AI materially improves dynamic/progressive extraction

FUSE_VALIDATED_STRENGTHS
  benchmark hypothesis: WebFetch-first -> observed dynamic gap -> Crawl4AI escalation

REJECT_CHALLENGER
  challenger fails the declared benchmark contract or adds no useful capability at unjustified burden

NO_BATTLE
  benchmark could not be executed fairly or ground truth/preflight became invalid
```

For every outcome:

```text
evidence_class = CONTROLLED_BENCHMARK
production_routing_authority = false
routing_impact = none
```

If the benchmark supports a production-changing hypothesis, terminal state is:

```text
READY_FOR_REAL_WORLD_VALIDATION
```

not `READY_FOR_ROUTING_CHANGE_DECISION`.

# Teardown

Mandatory after any staging, regardless of outcome.

Verify:

```text
no Crawl4AI/browser process remains
match venv removed
match browser/cache/profile removed
no PATH/MCP/system/user Python mutation
no persistent env/proxy/TLS change
pre-existing user state unchanged
repository contains only intended durable outputs
```

Classify:

```text
CLEAN_VERIFIED
CLEAN_WITH_RESIDUE
```

A winning benchmark Challenger's Arena runtime is still deleted.

# Explicitly unauthorized

Do not:

- persistently install Crawl4AI;
- add Firecrawl/Tavily/Brave/Browser Use/other contestants;
- create credentials/API keys;
- use LLM extraction;
- mutate production routing/source ownership;
- treat benchmark outcome as production ownership proof;
- use WeChat/GitHub/docs specialist sources as substitute fixtures;
- merge PR #3 or `main`.

# Stop states

Use the first applicable:

```text
READY_FOR_BENCHMARK_REDESIGN
READY_FOR_CRAWL4AI_STAGING_REDESIGN
READY_FOR_ARENA_REVIEW
READY_FOR_REAL_WORLD_VALIDATION
```

Every terminal state after staging must include cleanup classification.

Do not continue into real-world validation or another Challenger in the same run.
