# TASK-20260913-010 — Precision Search Challenger Playoff / Exa vs Tavily

## State

`READY_FOR_PRECISION_PLAYOFF_REDESIGN` — Arena cleanup status: **CLEAN_VERIFIED**

- Contract: `tasks/TASK-20260913-010-PRECISION-SEARCH-TAVILY-PLAYOFF.md` (Arena v0.5, evidence class CONTROLLED_BENCHMARK)
- Match id: `TASK-20260913-010-precision-playoff-b001`
- Receipts: `evidence/arena/TASK-20260913-010-precision-playoff-b001/{defender,challenger,adjudication}.json` + raw runs (`playoff-run-attempt1.json`, `playoff-run-tavily-attempt2.json`) + `driver-snapshot.py`
- Executed at remote head `65f1c7b`; `production_routing_authority: false`; `routing_impact: none`.

## 1. Admission — PASSED, then overtaken by rate limiting

Both hosted surfaces verified with minimal anonymous/keyless handshakes:

```text
Exa    https://mcp.exa.ai/mcp       200  exa-search-server v3.2.1  tools: web_search_exa, web_fetch_exa
Tavily https://mcp.tavily.com/mcp/  200  tavily-mcp v4.0.3 (keyless header)  tools: tavily_search (+extract/crawl/map/research, not used)
```

Ground truth frozen for all nine fixtures before any contestant ran (strict identifier-bearing targets for Class E verified by static fetch/code-search; family anchors for Classes S/M verified via official pages/repositories). The E1 frozen strict target set includes the Tavily keyless docs page itself — static fetch shows the exact header `X-Tavily-Access-Mode` present 12 times.

## 2. Execution

- **Exa (defender, candidate-slot incumbent): completed all 9 fixtures on attempt 1**, no retries:
  - Class E: **3/3 strict accepted-target hits, all at rank 1** (E1 keyless-docs page; E2 brave README; E3 crawl4ai parameters page).
  - Class S: 1/3 weak family hit (S3: official repo #1 + lazy-loading docs #3); S1/S2 repeated the TASK-009 wrong-vendor failure mode (Parallel.ai surfaces).
  - Class M: 3/3 family hits at rank 1 with constraint-satisfying surfaces (M1 brave features; M2 its own hosted docs; M3 github remote-server.md + readonly toolset endpoints).
- **Tavily (challenger, keyless): completed exactly 1 of 9 fixtures.**
  - E1 succeeded with a full 5-result list (frozen strict target at rank 2; tavily-python source at rank 1).
  - E2–M3 returned HTTP 200 with empty payloads. Out-of-band diagnostics proved the same request shape returns full results on a fresh window — the failure is the **keyless rate-limit window** consuming the burst budget (attempt 1's empties were compounded by a driver SSE first-data-line parse defect; both causes are separated and documented in the receipts).
  - Attempt 2 (corrected parser) hit the rate-limit window on all calls including `initialize` ("no matching rpc response" at constant ~260 ms); a single post-window diagnostic succeeded, proving intermittent rather than hard blocking.
  - Per-fixture 1+1 budget exhausted; per contract, rate limiting on ≥2 fixtures mandates the redesign stop state. No further calls were made.

## 3. Adjudication — NO_BATTLE (incomplete quality matrix)

The class-winner gate cannot be applied: Classes S and M have zero completed Tavily fixtures, and Class E has only a single completed comparison (E1: Exa rank 1 vs Tavily rank 2). No winner is invented from one cell.

```text
outcome: NO_BATTLE (fair complete comparison could not be executed)
evidence_class: CONTROLLED_BENCHMARK
production_routing_authority: false
routing_impact: none
candidate slot: Exa remains declared candidate by status quo; Tavily remains unadjudicated
```

Operational findings preserved for the redesign:

1. **Tavily keyless rate limiting is burst-based and windowed** — a single call works after a cool-down; a 9-call paced burst (even at 2 s spacing) exhausts it. Raw evidence: `playoff-run-attempt2.json` (constant ~260 ms no-matching-response on all calls) vs the post-window diagnostic (full valid response).
2. **Exa's controlled profile is stable across matches** — this run reproduced TASK-009 exactly: strict hits on identifier queries (now 3/3 with properly frozen target sets), wrong-vendor misses on identifier-less semantic paraphrases (S1/S2 again), and perfect multi-constraint family recall on its own ecosystem.
3. **TASK-009's evidence-handling slip is corrected**: raw run JSON and driver snapshot were copied into the repository before cell deletion.

## 4. Teardown

Raw runs + driver snapshot copied into the repository before deletion; match cell removed and confirmed absent; no client packages staged (host httpx only); no Exa/Tavily registration in any inspected config domain; no OAuth/API-key/account state; no background processes; PATH/shell/profile unchanged; user caches untouched; repository tree contains only intended durable outputs.

```text
classification: CLEAN_VERIFIED
residue: none
```

## 5. Redesign input for the next authorization

A Tavily retake needs one bounded change to the keyless execution model — e.g., (a) a session-reused connection with per-fixture cool-downs on the order of the observed rate-limit window, (b) spreading the 9 fixtures across the window with durable checkpointing, or (c) a differently authorized Tavily surface. Exa's side needs no restaging (transport-only, remote, anonymous). The TASK-009 S1 lesson also stands: strict-versus-family target sets must be frozen per fixture before scoring.

## 6. Next action (Human)

Review the rate-limit evidence and the incomplete matrix; authorize a redesigned playoff (per §5) or accept Exa as the candidate-slot incumbent without a Tavily comparison. No credential creation, production change, or further match is authorized in this run.
