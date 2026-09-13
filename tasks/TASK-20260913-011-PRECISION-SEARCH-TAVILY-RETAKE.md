---
task_id: TASK-20260913-011
status: ready_for_controlled_benchmark_execution
parent_task: TASK-20260912-001
reviewed_predecessor: TASK-20260913-010
target_repo: xifeng12/external-knowledge
implementation_branch: task/20260912-001-v04-capability-diagnostics
arena_contract: references/capability-arena.md
arena_version: v0.5
evidence_class: CONTROLLED_BENCHMARK
capability: precision.search
defender_role: precision-search-candidate-slot
defender: exa
challenger: tavily
defender_surface: hosted-mcp-anonymous
challenger_surface: keyless-search-rest
persistent_provisioning_authorized: false
new_credential_creation_authorized: false
production_routing_authority: false
pr_merge_authorized: false
---

# TASK-20260913-011 — Precision Search Playoff Retake / Exa vs Tavily

## Goal

Complete the candidate-slot playoff invalidated by TASK-010's Tavily keyless burst/window exhaustion without changing the benchmark questions or scoring gates.

```text
capability: precision.search
candidate-slot Defender: Exa anonymous hosted search
Challenger: Tavily keyless Search REST
Evidence class: CONTROLLED_BENCHMARK
```

`runtime-native.web-search` remains the unchanged general/default owner and is not a contestant.

TASK-010 remains valid evidence for its completed cells, but its overall outcome is `NO_BATTLE`. See:

```text
reports/TASK-20260913-010-ARENA-REVIEW.md
```

## Why the Tavily surface changes

The retake evaluates Tavily search-provider quality, not Remote-MCP/SSE error ergonomics.

Use Tavily's official keyless Search API directly:

```text
POST https://api.tavily.com/search
Header: X-Tavily-Access-Mode: keyless
Content-Type: application/json
```

No API key, account, OAuth, login, or persistent configuration is authorized.

The official keyless client model exposes structured rate-limit metadata such as:

```text
code
window
retry_after_seconds
next_actions
```

Use that metadata for scheduling. Do not guess a fixed cooldown when the service supplies an explicit retry interval.

Exa remains on the already-validated anonymous Hosted MCP ordinary search surface.

## Benchmark integrity — unchanged from TASK-010

Reuse the exact nine frozen queries and accepted target sets from TASK-010.

Do not alter:

- query wording;
- strict target URLs/files;
- target-family definitions;
- top-5 normalization;
- the three classes;
- the 2-of-3 class winner gate;
- strict-hit versus family-recall separation.

The three classes remain:

```text
Class E — exact / opaque identifiers (3 fixtures)
Class S — semantic paraphrase (3 fixtures)
Class M — multi-constraint long-tail retrieval (3 fixtures)
```

A provider wins a class only with material advantage on at least 2 of 3 fixtures.

One dramatic query cannot determine the candidate slot.

## Search parameters

Use search only.

### Exa

```text
web_search_exa
numResults = 5
```

No fetch, Exa Agent, account, API key, or authenticated features.

### Tavily

```text
POST /search
max_results = 5
```

Use the normal/default keyless search behavior except for `max_results=5` needed for benchmark normalization.

Do not use Tavily Extract/Crawl/Map/Research, answer synthesis, hidden content fetches, or query rewrites for scoring.

## Rate-limit-aware Tavily execution — HARD RULE

The retake must be checkpointed and window-aware.

For Tavily, execute one scored fixture at a time.

After every completed fixture, persist before issuing the next search:

```text
query_id
raw request parameters
HTTP status
raw response or compact lossless response artifact
first five result URLs/titles
elapsed time
rate-limit metadata if present
checkpoint timestamp
```

### On explicit keyless limit

If the service returns a structured keyless limit/quota error:

1. persist the exact structured error;
2. stop all subsequent Tavily requests immediately;
3. read `retry_after_seconds` / `window` from the response;
4. wait for the server-provided interval plus only a minimal transport safety margin;
5. retry the SAME blocked fixture once;
6. only after it completes may the next fixture begin.

The cooldown is scheduling, not a query retry intended to improve relevance.

Do not continue firing the remaining fixtures while the window is known to be closed.

### If no structured retry interval is available

If Tavily returns an ambiguous empty/error envelope without a usable structured retry interval:

- do not score it as search quality;
- do not guess repeated cooldown values;
- stop at `READY_FOR_PRECISION_PLAYOFF_REDESIGN` with the raw response preserved.

### Attempt budget

Per Tavily fixture:

```text
1 primary search-quality attempt
+ 1 exact same-query retry only after an explicit rate-limit window blocks the primary
```

No third attempt.

For Exa:

```text
1 primary attempt
+ at most 1 retry only for concrete transport/runtime failure
```

Returned-but-poor search results are scored and are not retry credit.

## Bounded wall-clock envelope

The match may span multiple Tavily keyless windows because the scheduler is intentionally quota-aware.

Use a bounded total wall-clock budget of 60 minutes for the nine-query playoff.

If all nine Tavily fixtures cannot complete fairly within that envelope, stop with `NO_BATTLE` / redesign rather than widening credentials or inventing results.

## Fairness

Both providers receive the identical nine raw query strings.

Do not:

- rewrite queries;
- tune one provider after observing the other;
- use fetch/extract to verify contestant results during scoring;
- classify family recall as strict target hit;
- score rate-limit errors as misses;
- use prior TASK-010 Tavily result quality as a substitute for an unexecuted retake cell.

Ground truth may be re-checked directly before the retake only to ensure the frozen targets still exist; do not redesign targets ad hoc.

## Evidence

Write a new match id:

```text
TASK-20260913-011-precision-playoff-b002
```

Required durable outputs:

```text
reports/TASK-20260913-011-PRECISION-SEARCH-PLAYOFF-RETAKE.md
evidence/arena/TASK-20260913-011-precision-playoff-b002/defender.json
evidence/arena/TASK-20260913-011-precision-playoff-b002/challenger.json
evidence/arena/TASK-20260913-011-precision-playoff-b002/adjudication.json
evidence/arena/TASK-20260913-011-precision-playoff-b002/raw/*
evidence/arena/TASK-20260913-011-precision-playoff-b002/checkpoints/*
```

Preserve raw responses/checkpoints before teardown. Do not repeat TASK-009's lost-raw-evidence mistake.

## Adjudication

Candidate-slot outcomes:

```text
KEEP_INCUMBENT
  Exa retains the precision-search candidate slot

REPLACE
  Tavily becomes the recommended precision-search candidate

SPLIT_BY_SCENARIO
  repeated class evidence supports a defensible specialist split

NO_BATTLE
  fair complete matrix cannot be obtained inside the bounded rate-limit-aware envelope
```

Do not promote a candidate from one fixture.

Separate:

```text
strict target hit
family recall
relevance/noise
constraint fidelity
latency
rate-limit/operational burden
failure-domain independence
```

Every result remains:

```text
evidence_class = CONTROLLED_BENCHMARK
production_routing_authority = false
```

Human review is required before any capability-map/provider-binding change.

## Teardown

No persistent provider setup is needed.

Arena-owned local artifacts are limited to transport scripts, raw responses, temporary checkpoints/caches, and match-scoped runtime files.

After durable copy-out, verify:

```text
match cell removed
no client/background process remains
no MCP registration created
no credential/account/OAuth state created
PATH/shell/profile unchanged
repository contains only intended durable outputs
```

Classify `CLEAN_VERIFIED` or exact `CLEAN_WITH_RESIDUE`.

## Explicitly unauthorized

Do not:

- create/use Tavily or Exa API keys/accounts/OAuth;
- switch to a paid/authenticated quota to finish the benchmark;
- use Tavily Extract/Crawl/Map/Research;
- use Exa fetch/Agent;
- add Native/Brave/SearXNG/Perplexity or another contestant;
- change production routing/provider bindings;
- merge PR #3 or main.

## Stop states

Use the first applicable:

```text
READY_FOR_PRECISION_PLAYOFF_REDESIGN
READY_FOR_ARENA_REVIEW
```

After any execution, include cleanup classification and stop. Do not continue to another Challenger in the same run.
