# TASK-20260913-007 — Complex Web Controlled Benchmark

## State

`READY_FOR_REAL_WORLD_VALIDATION` — Arena cleanup status: **CLEAN_VERIFIED**

- Contract: `tasks/TASK-20260913-007-COMPLEX-WEB-CONTROLLED-BENCHMARK.md` (Arena v0.4, evidence class CONTROLLED_BENCHMARK)
- Match id: `TASK-20260913-007-complexweb-b001`
- Receipts: `evidence/arena/TASK-20260913-007-complexweb-b001/{defender,challenger,adjudication}.json`
- Executed at remote head `f3536c5`; `production_routing_authority: false`; `routing_impact: none` throughout.

## 1. Preflight — PASSED (ground truth frozen before staging)

All three `web-scraping.dev` fixtures were preflighted immediately before staging and matched the contract's observable ground truth exactly:

- **B0** `/product/1`: 200, 33.8 KB — title/price/brand/table anchors all present.
- **B1** `/reviews`: 200, 14.7 KB — GraphQL-mock shell page ("graphql mock website" in title), Load More present, review records confirmed absent from raw HTML.
- **B2** `/testimonials`: 200, 30.1 KB — heading, aggregate 60, initial batch of 10 testimonial texts in raw HTML.

No fixture drift; no substitution needed.

## 2. Defender (runtime-native.webfetch)

P0 DEFAULT_READ via the observed native chain (WebFetch → host hook → context-mode fetcher):

```text
B0: PASS  — title, $9.99, description, brand ChocoDelight, Features table,
            Packs table preserved as GFM with ALL 5 rows
B1: FAIL  — shell only (title/nav/Load More), 0 review records
B2: FAIL  — heading + aggregate 60 + exactly the first 10 testimonial texts
P1: UNSUPPORTED — the native path has no documented generic render/scroll capability
```

## 3. Challenger (crawl4ai 0.9.3, ephemeral cell)

Staging: venv + `crawl4ai==0.9.3` + match-scoped chromium-1234, all in-cell (~1.59 GB). Notably, **all downloads completed DIRECT this run** — the TASK-004 CDN stall did not recur and no proxy override was used (TASK-007 does not implicitly authorize one).

Attempt accounting (disclosed): attempt 1 executed the full suite successfully at tool level, but the orchestrator's measurement layer was format-biased (table-regex and class-literal mismatches) and raw artifacts were not persisted. Attempt 2 — the recorded attempt for every fixture/profile — used identical contestant configs (no tuning from any result) with a corrected, format-neutral measurement layer and full artifact emission; within the 1+1 budget.

Results (record counts from adjudicator-side counting of emitted artifacts):

```text
fixture/profile      defender      challenger
B0  P0 static        PASS          PASS (equal table fidelity, 5/5 pack rows)
B1  P0 shell         FAIL (0)      FAIL (0 — default domcontentloaded returns early)
B1  P1 dynamic       UNSUPPORTED   STRONG (20 date-led review records, network-idle)
B2  P0 initial       FAIL (10/60)  FAIL (10/60)
B2  P1 progressive   UNSUPPORTED   PARTIAL (30/60, generic scan_full_page)
```

The P1-B2 result stands at 30/60: `scan_full_page` tripled recovery (10→30) but did not reach the full aggregate, and post-observation tuning (e.g., scroll delays) is forbidden by the contract.

## 4. Adjudication — SPLIT_BY_SCENARIO (benchmark hypothesis)

- **B0 tie**: both contestants are baseline-suitable for ordinary static extraction with equal structure fidelity.
- **B1 decisive challenger advantage**: rendered review records are reachable only through the challenger's documented generic dynamic-read profile (20 vs 0; defender P1 unsupported).
- **B2 material challenger advantage**: progressive recovery tripled (30/60 vs 10/60) under generic scroll behavior, without reaching full aggregate.
- Cost/burden remains real: ~1.59 GB ephemeral footprint and a venv/browser lifecycle vs zero staging for the defender. This is exactly a scenario split, not a replacement case.

Per the evidence boundary: `evidence_class = CONTROLLED_BENCHMARK`, `production_routing_authority = false`, `routing_impact = none`. Because the split hypothesis is production-changing if adopted, the terminal state is `READY_FOR_REAL_WORLD_VALIDATION` — real-workload validation (e.g., a qualifying ordinary-URL case per the TASK-006 findings, or an equivalent retained need) must precede any routing decision. No inference to specialist sources (WeChat/GitHub/docs) is made from this benchmark.

## 5. Teardown

All Arena-owned artifacts removed and verified: no Arena-owned chrome/python processes (command-line scan); 1.6 GB cell deleted and confirmed absent; crawl4ai not importable on host python; `PLAYWRIGHT_BROWSERS_PATH` was per-command only; no registrations; pre-existing ms-playwright user cache untouched (no chromium-1234 leaked — install logs prove all downloads landed in the cell); repository tree contains only intended durable outputs.

```text
classification: CLEAN_VERIFIED
residue: none Arena-owned (TASK-004-era caveat about the truncated user-cache baseline carries over)
```

## 6. Notes

- The challenger's attempt-1 measurement defect is disclosed in its receipt; recorded results come from attempt 2 with identical configs.
- Arena v0.4's three evidence classes worked as designed: this benchmark produces mechanism evidence only; the TASK-006 real-case negative result remains the factual barrier for any production claim.
- Next action belongs to the Human: review the benchmark adjudication; if the split hypothesis is to be pursued, authorize a real-world validation task; a third match or production promotion is not authorized in this run.
