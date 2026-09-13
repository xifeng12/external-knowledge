# TASK-20260913-009 — Precision Search Controlled Benchmark / Native Search vs Exa

## State

`READY_FOR_ARENA_REVIEW` — Arena cleanup status: **CLEAN_VERIFIED**

- Contract: `tasks/TASK-20260913-009-PRECISION-SEARCH-EXA-BENCHMARK.md` (Arena v0.5, evidence class CONTROLLED_BENCHMARK)
- Match id: `TASK-20260913-009-precision-search-b001`
- Receipts: `evidence/arena/TASK-20260913-009-precision-search-b001/{defender,challenger,adjudication}.json`
- Executed at remote head `5e4b98b`; `production_routing_authority: false`; `routing_impact: none`.

## 1. Admission — PASSED

- Defender `runtime-native.web-search`: operational (retained runtime evidence + live use).
- Challenger `exa`: not exposed in any local runtime surface (consistent with TASK-002), so the **anonymous hosted MCP** route was used: `https://mcp.exa.ai/mcp` answered `initialize` (200, exa-search-server v3.2.1) and `tools/list` (`web_search_exa`, `web_fetch_exa`) with **no credentials** — the anonymous rate-limited access the contract conditions on remains true at execution time. No API key/OAuth/login/Exa Agent; no persistent registration; the transport-only client script lived in the match cell.
- Preflight froze canonical targets + anchors for all six fixtures via `gh api` (repo/readme/code-search) before any contestant ran; no contestant output shaped the targets.

## 2. Results (first-5 window, family-scored)

```text
query                          defender                     challenger (Exa)
S0 baseline canonical          hit@1 (2 rel / 2 noise)      hit@1 (4 rel / 0 noise)
S1 "X-Tavily-Access-Mode"      MISS - 0/5 relevant          family-hit@1 - 5/5 official Tavily
                               (tokenized music/fuzzy)      surfaces (page-level identifier
                                                            presence unverified: fetch excluded)
S2 "BRAVE_API_KEY_FILE" …      hit@1 (5/5 relevant)         hit@1 (3 rel / 2 adjacent)
S3 semantic paraphrase         hit@1 (4/5 relevant)         MISS - 0/5 wrong vendor family
                               via 4 internal search        (returned Parallel.ai's hosted
                               rounds (observed trace)      search MCP)
S4 crawl4ai scan option        hit@1 (5/5 relevant)         hit@1 (3 rel / 2 noise)
S5 tavily keyless multi-cstr   hit@1 (1 rel / 3 noise)      hit@1 (5/5 official Tavily)
```

Two symmetric single-fixture failures decided the texture of this match:

- **S1 (the declared precision-search class: exact rare identifier)** — the native tool tokenized the quoted identifier into fragments and returned pure noise (phonk music videos, fuzzy "Tally"/"Tailscale"/"XTLS" matches); Exa returned five official Tavily surfaces (keyless docs, search/extract API endpoints, mcp.tavily.com) — the pages semantically governed by that header. Caveat recorded: page-level identifier verification would require a content fetch, which the contract excludes from scoring; the strict bullseye (`src/index.ts`) was not returned.
- **S3 (semantic paraphrase without the identifier)** — the native tool's default agentic behavior internally issued **4 search rounds** (rewrites observed in the trace) and landed hit@1 with the exact README anchor; single-shot Exa retrieved a different vendor's hosted search MCP and never surfaced the accepted family.

## 3. Adjudication — SPLIT_BY_SCENARIO (scoped)

- The declared precision-search architecture is **directionally supported on its declared class**: for exact rare identifiers, native search exhibited a complete recall failure while Exa recalled the correct official family (S1), with real failure-domain independence (different indices/backends over the same live web — unlike TASK-004's correlated anti-bot block).
- The advantage is **not repeated dominance**: each provider failed exactly one fixture, both went 5/6 or equivalent on hit@1, and the S1 page-level verification is bounded by the no-fetch scoring rule.
- The defender's S3 win came through hidden multi-call cost (4 internal rounds) — recorded as an observed operational characteristic of the incumbent, not penalized.
- Exa's operational burden this run was trivial (remote anonymous service, transport-only script) — materially cheaper than the Crawl4AI staging model.

**Provisional-test-policy implication** (per Arena v0.5, non-production): keep the declared architecture — `general-web.search` first; on an observed exact-obscure-token precision/recall gap, escalate to `precision.search`/Exa via the anonymous hosted surface for test-stage use. **Do not** extend Exa's role to general semantic-paraphrase search on this evidence.

`evidence_class = CONTROLLED_BENCHMARK`; `production_routing_authority = false`; `routing_impact = none`.

## 4. Teardown

Match cell (transport script + run evidence) deleted and confirmed absent; no client packages were staged (host `httpx` only); no exa registration in any inspected config domain; no token/OAuth/API-key state created (anonymous session abandoned with the client process); no background processes; PATH/shell/profile unchanged; pre-existing user caches untouched; repository tree contains only intended durable outputs.

```text
classification: CLEAN_VERIFIED
residue: none
evidence-handling note (disclosed): the challenger's raw stdout JSON was transcribed into
challenger.json; the raw file itself was not copied out before cell removal (orchestrator
slip). All scored values are as observed and printed at run time.
```

## 5. Next action (Human)

Review the adjudication and decide: (a) accept the provisional precision-search policy as the next test-stage baseline; (b) whether Tavily becomes the next Challenger (TASK-009's "why Exa first" precondition is now met — Exa has evidence); (c) any real-world validation debt collection remains opportunistic and non-blocking. No further match, credential creation, or production change is authorized in this run.
