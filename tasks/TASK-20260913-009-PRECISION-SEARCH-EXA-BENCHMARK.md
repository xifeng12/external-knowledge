---
task_id: TASK-20260913-009
status: ready_for_arena_review
parent_task: TASK-20260912-001
target_repo: xifeng12/external-knowledge
implementation_branch: task/20260912-001-v04-capability-diagnostics
arena_contract: references/capability-arena.md
arena_version: v0.5
evidence_class: CONTROLLED_BENCHMARK
capability: precision.search
defender: runtime-native.web-search
challenger: exa
challenger_surface: hosted-mcp-anonymous
persistent_provisioning_authorized: false
new_credential_creation_authorized: false
production_routing_authority: false
pr_merge_authorized: false
---

# TASK-20260913-009 — Precision Search Controlled Benchmark / Native Search vs Exa

## Goal

Test the repository's existing precision-search architecture before introducing another search Challenger.

```text
capability: precision.search
Defender: runtime-native.web-search
Challenger: Exa hosted MCP
Evidence class: CONTROLLED_BENCHMARK
```

Repository authority already declares Exa as the specialized precision challenger for exact obscure term/API/error/version queries after ordinary search shows a precision/recall gap. This Arena asks whether Exa actually demonstrates a useful controlled-test advantage over native web search for that role.

This is not a production routing change and not an authorization to install Exa permanently.

## Why Exa before Tavily

Evaluate the declared architecture first:

```text
general-web.search
  -> runtime-native.web-search

observed precision / recall gap
  -> precision.search / Exa
```

Only after Exa has evidence should Tavily be considered as a Challenger to that precision-search track. Do not create a three-way benchmark in this task.

## Current runtime evidence boundary

Retained TASK-002 evidence recorded:

```text
precision.search = MISSING_CONFIRMED
Exa MCP exposure = not found
EXA_API_KEY = unset
```

That was a scoped machine-exposure finding, not proof that Exa cannot run in an Arena.

Current official Exa hosted MCP documentation advertises anonymous rate-limited access to default search/fetch tools. TASK-009 may use the anonymous hosted MCP only if that remains true at execution time.

No API key, OAuth, interactive login, credential creation, credential persistence, or account setup is authorized.

If anonymous access is no longer available or rate limiting prevents a fair benchmark, stop at:

```text
READY_FOR_EXA_BENCHMARK_REDESIGN
```

Do not create credentials to keep the match running.

# 1. Admission and staging

Before contestant execution:

1. read Arena v0.5 and current Issue #2;
2. verify current branch head is unchanged from the authority you read;
3. verify Defender native web search is operational;
4. probe the Exa hosted MCP anonymously with the minimum protocol handshake / tool-list action needed to establish an execution surface;
5. record baseline and all Arena-owned client/runtime artifacts before use.

Preferred Challenger order:

```text
1. already exposed Exa MCP in current runtime
2. direct anonymous hosted MCP via match-scoped transport/client
3. small match-scoped MCP client dependency only if needed
```

Do not register Exa persistently in user/global MCP config. Do not use `?login`, OAuth, API keys, or Exa Agent. Use only the ordinary web-search surface needed for this benchmark.

If a small client package is needed, it must live in the Arena cell and be torn down. Provider staging itself should remain remote/anonymous when possible.

Before any match-owned package/client staging, record:

```text
Baseline
Provision Plan
Rollback Plan
Promotion Plan
Teardown Plan
```

# 2. Benchmark design

Evidence class is `CONTROLLED_BENCHMARK`.

The suite is deliberately a set of precision-search needles with inspectable ground truth. The source pages may belong to GitHub/docs/etc.; they are used only as controlled retrieval targets. Do not infer production source-semantic ownership from these fixtures.

Immediately before contestant runs, preflight every target directly and freeze the accepted target URL/domain + anchor. If any fixture has materially disappeared or changed, replace nothing ad hoc; stop at `READY_FOR_SEARCH_BENCHMARK_REDESIGN`.

Use exactly these six queries.

## S0 — baseline explicit target

Query:

```text
Exa MCP Server web search web crawling
```

Accepted target family:

```text
official Exa MCP repository / official Exa MCP documentation
```

Purpose: baseline ability to locate the obvious canonical target.

## S1 — rare exact identifier

Query:

```text
"X-Tavily-Access-Mode"
```

Accepted target family:

```text
official tavily-ai/tavily-mcp source or official Tavily MCP documentation containing that identifier
```

Purpose: exact rare-token recall and rank.

## S2 — rare configuration key

Query:

```text
"BRAVE_API_KEY_FILE" brave search mcp
```

Accepted target family:

```text
official brave/brave-search-mcp-server README/docs containing BRAVE_API_KEY_FILE
```

Purpose: exact configuration-symbol retrieval with namespace disambiguation.

## S3 — semantic paraphrase without the distinctive identifier

Query:

```text
official MCP web search server whose hosted endpoint allows anonymous requests with rate limits
```

Accepted target family:

```text
official Exa MCP repository / documentation describing anonymous rate-limited hosted MCP access
```

Purpose: semantic retrieval when the query does not supply the repository/tool name.

## S4 — capability parameter lookup

Query:

```text
Crawl4AI automatic full page scroll dynamic content scan option
```

Accepted target family:

```text
official Crawl4AI documentation containing `scan_full_page`
```

Purpose: retrieve a precise API/config concept from a natural-language paraphrase.

## S5 — multi-constraint long-tail lookup

Query:

```text
Tavily MCP no API key keyless mode search extract only
```

Accepted target family:

```text
official Tavily MCP source/README documenting keyless mode and search/extract availability
```

Purpose: satisfy several simultaneous constraints rather than keyword-match one token.

# 3. Preflight ground truth

For each fixture freeze before contestant runs:

```text
query id
raw query text
accepted canonical target URL(s)
accepted target domain/repository
one short anchor proving the page is the intended target
preflight timestamp
```

Do not store long copyrighted content.

The preflight may use direct known URLs or repository files. It must not use either contestant's search results to choose or modify the targets.

# 4. Fairness and execution

Both contestants receive the exact same raw query text.

Per query:

```text
one primary search call
+ at most one retry only for concrete transport/tool/runtime failure
```

A poor or empty result is an observed search result, not retry credit.

Normalize evaluation to the first 5 returned web results. If a provider returns fewer than 5, evaluate what it returned and record the count.

Do not use content fetch/extract as part of contestant scoring. This Arena tests **search retrieval**, not page reading.

Do not add query rewrites after seeing results. No provider consumes the other provider's output.

# 5. Scoring dimensions

Do not collapse to one arbitrary aggregate score.

For each query record:

```text
target_hit@1
target_hit@3
target_hit@5
rank of first accepted target, if any
number of clearly relevant results in top 5
number of clearly irrelevant/noise results in top 5
whether exact constraints were preserved
whether the returned result is stale/wrong-version when the fixture is version/config specific
latency / call count
errors / retries
```

Then adjudicate across these dimensions:

```text
exact-needle recall
semantic-paraphrase recall
rank / precision
multi-constraint fidelity
noise
freshness/version correctness when applicable
determinism/reproducibility
latency/call cost
operational burden
agent ergonomics
failure-domain independence
```

A difference must be material and repeated across relevant fixtures before it changes the test-stage policy.

# 6. Interpretation

Possible controlled-benchmark outcomes:

```text
KEEP_INCUMBENT
  native search is sufficient; Exa adds no material precision-search value

SPLIT_BY_SCENARIO
  native remains default general search; Exa demonstrates material advantage on defined precision/long-tail query classes

FUSE_VALIDATED_STRENGTHS
  provisional policy: native first -> observed precision/recall gap -> Exa escalation

REJECT_CHALLENGER
  Exa is operational but fails to justify the precision-search track under this benchmark

NO_BATTLE
  anonymous Exa execution or benchmark fairness/ground truth cannot be established
```

For every outcome:

```text
evidence_class = CONTROLLED_BENCHMARK
production_routing_authority = false
```

A successful Exa result may establish or refine a `PROVISIONAL_TEST_POLICY` under Arena v0.5. Real-world validation debt is non-blocking and may be collected later during actual use.

# 7. Durable outputs

If the match runs, write:

```text
reports/TASK-20260913-009-PRECISION-SEARCH-BENCHMARK.md
evidence/arena/TASK-20260913-009-precision-search-b001/defender.json
evidence/arena/TASK-20260913-009-precision-search-b001/challenger.json
evidence/arena/TASK-20260913-009-precision-search-b001/adjudication.json
```

Receipts must include the frozen preflight ground truth, query-by-query results, timing, retry/error evidence, execution surface, staging provenance, authorization boundary, evidence class, policy implication, and teardown status.

Do not store credentials or unnecessary page bodies.

# 8. Teardown

Mandatory for all Arena-owned client/runtime artifacts even though the Exa provider is remote.

Verify as applicable:

```text
match-scoped client/package/cache removed
no persistent MCP registration
no token/OAuth/API-key state created
no background client process remains
PATH/shell/profile unchanged
repository contains only intended durable outputs
```

Classify:

```text
CLEAN_VERIFIED
CLEAN_WITH_RESIDUE
```

# 9. Explicitly unauthorized

Do not:

- create an Exa account/API key/OAuth session;
- persistently register Exa MCP;
- enable Exa Agent or authenticated-only features;
- install Tavily/Brave/SearXNG/Perplexity or another search Challenger;
- perform a three-way search match;
- change production routing/source ownership;
- merge PR #3 or main.

# 10. Stop states

Use the first applicable:

```text
READY_FOR_EXA_BENCHMARK_REDESIGN
READY_FOR_SEARCH_BENCHMARK_REDESIGN
READY_FOR_ARENA_REVIEW
READY_FOR_NEXT_ARENA_DECISION
```

If the benchmark produces a clear provisional search policy and teardown is clean, prefer `READY_FOR_ARENA_REVIEW`; Human review decides whether to accept it as the next test-stage baseline and whether Tavily should become the next Challenger.
