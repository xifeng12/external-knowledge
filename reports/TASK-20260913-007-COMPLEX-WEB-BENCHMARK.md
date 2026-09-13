# TASK-20260913-007 — Complex Web Controlled Benchmark

## State

`TEST_STAGE_BASELINE_ACCEPTED` — Arena cleanup status: **CLEAN_VERIFIED**

> Human review (TASK-20260913-008): the original execution stop `READY_FOR_REAL_WORLD_VALIDATION` remains part of the historical run record, but immediate real-world validation is no longer a blocking next step. Arena v0.5 treats real-world confirmation as non-blocking validation debt during the current testing phase. The benchmark split is accepted as a provisional test-stage policy.

- Contract: `tasks/TASK-20260913-007-COMPLEX-WEB-CONTROLLED-BENCHMARK.md` (executed under Arena v0.4, evidence class CONTROLLED_BENCHMARK)
- Review authority: `tasks/TASK-20260913-008-TEST-STAGE-BASELINE-ACCEPTANCE.md` (Arena v0.5)
- Match id: `TASK-20260913-007-complexweb-b001`
- Receipts: `evidence/arena/TASK-20260913-007-complexweb-b001/{defender,challenger,adjudication}.json`
- Executed at remote head `f3536c5`; raw receipts remain unchanged.

## 1. Preflight — PASSED

All three `web-scraping.dev` fixtures matched the frozen controlled ground truth:

- **B0** `/product/1`: title/price/brand/table anchors present.
- **B1** `/reviews`: dynamic review records absent from raw HTML; Load More shell present.
- **B2** `/testimonials`: aggregate 60; initial batch 10.

## 2. Defender — runtime-native.webfetch

```text
B0 P0: PASS — static content and tables recovered
B1 P0: FAIL — shell only, 0 review records
B2 P0: FAIL — 10/60 testimonials
P1: UNSUPPORTED — no documented generic render/scroll profile
```

## 3. Challenger — Crawl4AI 0.9.3

Ephemeral staging used a match-scoped venv + Chromium, ~1.59 GB total, with mandatory teardown. Downloads completed direct; no proxy override was used.

Recorded results:

```text
B0 P0: PASS — equivalent static/table fidelity
B1 P0: FAIL — 0 records
B1 P1: STRONG — 20 rendered review records
B2 P0: FAIL — 10/60
B2 P1: PARTIAL — 30/60 via generic full-page scan
```

The first execution pass had a measurement-layer defect; the recorded second pass used identical contestant configuration with a corrected format-neutral measurement layer. This is disclosed in the contestant receipt.

## 4. Adjudication — SPLIT_BY_SCENARIO

Controlled evidence supports:

```text
ordinary/static known URL
  -> runtime-native.webfetch is sufficient and cheaper

observed dynamic/rendered/progressive extraction need
  -> Crawl4AI has a material capability advantage when its generic dynamic-read profile is available
```

Rationale:

- B0 was a tie;
- B1 showed a decisive dynamic-render advantage for Crawl4AI (20 vs 0);
- B2 showed a material progressive-load advantage (30/60 vs 10/60), though not full recovery;
- native WebFetch retains a decisive operational-cost advantage for ordinary/static reads;
- Crawl4AI carries a substantial browser/runtime lifecycle cost.

## 5. Evidence maturity after Human review

The benchmark remains:

```text
evidence_class = CONTROLLED_BENCHMARK
```

Human review accepts the result as:

```text
policy_status = TEST_STAGE_BASELINE
outcome = SPLIT_BY_SCENARIO
validation_debt = OPEN_NONBLOCKING
production_confidence = UNVALIDATED
```

This policy may guide continued testing and experimental use. It is not a claim of universal production superiority and does not authorize persistent provider installation or final source-owner changes.

Real-world evidence should be collected opportunistically when normal use naturally encounters relevant dynamic/progressive pages. Such evidence may confirm, refine, or overturn this policy without blocking new Arena work.

## 6. Teardown

Arena-owned artifacts were removed and verified:

```text
classification: CLEAN_VERIFIED
residue: none Arena-owned
```

No persistent Crawl4AI install, browser profile, PATH/MCP registration, environment mutation, or production routing change was left by the run.

## 7. Current next state

Per TASK-20260913-008 and Arena v0.5:

```text
READY_FOR_NEXT_ARENA_DECISION
```

Immediate REAL_REPLAY / REAL_WORKLOAD validation is optional and non-blocking during the current testing phase.
