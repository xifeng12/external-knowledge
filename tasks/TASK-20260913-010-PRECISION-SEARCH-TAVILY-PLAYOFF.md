---
task_id: TASK-20260913-010
status: ready_for_precision_playoff_redesign
parent_task: TASK-20260912-001
reviewed_predecessor: TASK-20260913-009
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
challenger_surface: remote-mcp-keyless
persistent_provisioning_authorized: false
new_credential_creation_authorized: false
production_routing_authority: false
pr_merge_authorized: false
---

# TASK-20260913-010 — Precision Search Challenger Playoff / Exa vs Tavily

## Goal

Run a direct controlled playoff for the **precision-search candidate slot**.

```text
capability: precision.search
candidate-slot Defender: Exa hosted MCP (anonymous)
Challenger: Tavily Remote MCP (keyless)
Evidence class: CONTROLLED_BENCHMARK
```

This is not a three-way match. `runtime-native.web-search` remains the unchanged general/default search owner and does not participate in this playoff.

TASK-009 established that Exa is operational and useful enough to remain a qualified precision-search candidate, but Human/Coordinator review did **not** promote its raw `SPLIT_BY_SCENARIO` interpretation into a test-stage Native -> Exa routing policy because the repeated-evidence gate was not met.

See:

```text
reports/TASK-20260913-009-ARENA-REVIEW.md
evidence/arena/TASK-20260913-009-precision-search-b001/review.json
```

The purpose of TASK-010 is to decide which specialist candidate has the stronger controlled evidence before the search track is promoted/refined further.

## Current anonymous/keyless execution surfaces

### Exa

Use the already-validated anonymous hosted MCP:

```text
https://mcp.exa.ai/mcp
```

Use only the ordinary search tool required by this benchmark. No Exa API key, OAuth, login, account, Agent, or persistent MCP registration.

### Tavily

Official Tavily Keyless Access documentation currently defines a no-account/no-API-key Remote MCP path:

```text
URL: https://mcp.tavily.com/mcp/
Header: X-Tavily-Access-Mode: keyless
```

The keyless MCP exposes Search and Extract; this task uses **Search only**.

Do not use OAuth, API keys, account creation, `/crawl`, `/map`, or `/research`.

If either anonymous/keyless surface is unavailable at execution time, or requires credentials, stop rather than widening authorization.

## Admission and ephemeral client boundary

Before contestant execution:

1. read Arena v0.5, TASK-009 review, this task, current Issue #2, and the current remote branch head;
2. verify both hosted surfaces with minimum anonymous/keyless MCP handshake and `tools/list`;
3. record exact server/tool versions where exposed;
4. record baseline and four lifecycle plans for any match-owned client files.

Preferred client implementation:

```text
existing host HTTP/MCP transport capability
or
match-scoped transport-only script using already-present runtime libraries
```

Do not install a package merely for convenience if a transport-only path exists.

No persistent MCP registration, PATH edit, shell/profile edit, credential state, OAuth cache, or provider account state.

If a local package is genuinely required, stop at:

```text
READY_FOR_PRECISION_PLAYOFF_STAGING_REDESIGN
```

rather than installing without a new authorization.

# Benchmark design

The prior match exposed two scoring lessons that are binding here:

```text
strict target hit != target-family recall
single-fixture advantage != repeated class advantage
```

Freeze all ground truth before contestant execution. Do not use either contestant to select the accepted targets.

Use exactly nine queries in three classes, three fixtures per class.

## Class E — exact / opaque identifier retrieval

### E1

```text
"X-Tavily-Access-Mode"
```

Strict accepted target(s):

```text
official Tavily Keyless Access documentation containing X-Tavily-Access-Mode
and/or official tavily-ai/tavily-mcp source file known by preflight to contain the identifier
```

### E2

```text
"BRAVE_API_KEY_FILE" brave search mcp
```

Strict accepted target(s):

```text
official brave/brave-search-mcp-server README/source/config page preflighted to contain BRAVE_API_KEY_FILE
```

### E3

```text
"scan_full_page" Crawl4AI
```

Strict accepted target(s):

```text
official Crawl4AI documentation/source page preflighted to contain scan_full_page
```

Primary metric for Class E is **strict accepted-target hit**. An official vendor/repository family page that is not preflighted to contain the identifier is recorded separately as `family_hit` and does not substitute for `strict_target_hit`.

## Class S — semantic paraphrase retrieval

### S1

```text
official MCP web search server whose hosted endpoint allows anonymous requests with rate limits
```

Accepted family:

```text
official Exa MCP repository/documentation describing anonymous rate-limited hosted access
```

### S2

```text
remote MCP search and extract with no account and no API key using a special request header
```

Accepted family:

```text
official Tavily Keyless Access / Remote MCP documentation
```

### S3

```text
open source web crawler option that automatically scans a full page for progressively loaded lazy content
```

Accepted family:

```text
official Crawl4AI documentation describing scan_full_page / equivalent generic progressive-load behavior
```

## Class M — multi-constraint long-tail retrieval

### M1

```text
Brave search MCP web local image video news summarizer API key file
```

Accepted family:

```text
official Brave Search MCP repository/documentation satisfying the stated feature/config constraints
```

### M2

```text
Exa hosted MCP anonymous web search rate limited no API key endpoint
```

Accepted family:

```text
official Exa MCP repository/documentation satisfying hosted + anonymous + rate-limit constraints
```

### M3

```text
GitHub official MCP server remote hosted read-only toolsets dynamic discovery
```

Accepted family:

```text
official github/github-mcp-server repository/documentation satisfying the stated remote/read-only/toolset constraints
```

# Preflight ground truth

Before contestant execution freeze, per fixture:

```text
query id
raw query text
class
strict accepted target URL(s), when Class E
accepted target family/domain/repository
short anchor proving target validity
preflight timestamp
```

Use direct official pages, repository files, or authoritative documentation for preflight. Do not store unnecessary page bodies.

# Fairness and execution

Both contestants receive the exact same raw query once.

Use only each provider's normal search surface. Configure only the result-count parameter required to request five results when the API supports it.

Do not use:

```text
query rewriting
site/domain filters
include/exclude-domain tuning
content extraction
page fetch
answer synthesis as a second retrieval stage
provider-specific target hints
```

Per fixture/provider:

```text
1 primary search call
+ at most 1 retry only for concrete transport/5xx/timeout failure
```

A poor/empty search result is final evidence, not retry credit.

Use the same non-burst execution cadence for both providers. Record provider-call latency separately from any fixed pacing delay.

HTTP/provider rate limiting is an operational observation, not a free retry. If either provider is rate-limited on two or more of the nine fixtures, stop at `READY_FOR_PRECISION_PLAYOFF_REDESIGN` because the quality matrix is incomplete; preserve the rate-limit evidence.

Normalize scoring to the first five search results.

# Scoring

For every fixture record:

```text
strict_target_hit@1/@3/@5 (Class E)
family_hit@1/@3/@5
rank of first strict/family target
relevant result count in top 5
noise count in top 5
duplicate count
constraint fidelity
stale/wrong-version status when applicable
latency
errors/retries/rate-limit response
```

Do not collapse to one opaque aggregate score.

## Class winner gate

A provider wins a query class only when it materially wins at least **2 of the 3** fixtures in that class on the class-primary metrics.

Examples:

```text
Class E -> strict accepted-target recall/rank dominates
Class S -> accepted-family semantic recall/rank + noise dominates
Class M -> simultaneous constraint fidelity + recall/rank dominates
```

One dramatic fixture is not enough to claim a class win.

## Playoff outcome gate

Use existing Arena outcomes for the candidate slot:

```text
KEEP_INCUMBENT
  Exa wins at least 2 of 3 query classes

REPLACE
  Tavily wins at least 2 of 3 query classes

SPLIT_BY_SCENARIO
  each provider wins at least one different query class and remaining evidence is tied/inconclusive, with a defensible class boundary

NO_BATTLE
  fair complete comparison cannot be executed
```

If neither provider meets a repeated-evidence promotion gate, retain Exa by status quo as the declared candidate but record the playoff as inconclusive; do not invent a winner from one query.

Regardless of outcome:

```text
evidence_class = CONTROLLED_BENCHMARK
production_routing_authority = false
production routing impact = none
```

Any candidate-slot change is a **test-stage capability-map recommendation**, requiring Human review before modifying repository provider bindings.

# Failure-domain and operational comparison

Record:

```text
search backend/index independence
anonymous/keyless rate-limit behavior
handshake overhead
per-query latency
local client footprint
credential/account burden
result structure/agent ergonomics
```

Do not claim resilience independence merely because both are different MCP servers; document the observed backend/control-plane evidence available.

# Durable outputs

If the match runs, write:

```text
reports/TASK-20260913-010-PRECISION-SEARCH-PLAYOFF.md
evidence/arena/TASK-20260913-010-precision-playoff-b001/defender.json
evidence/arena/TASK-20260913-010-precision-playoff-b001/challenger.json
evidence/arena/TASK-20260913-010-precision-playoff-b001/adjudication.json
```

Raw provider results should be preserved in compact sanitized form sufficient to verify the top-5 classification. Do not repeat TASK-009's raw-output copy-out slip: ensure durable receipt data exists before teardown.

# Teardown

Mandatory for all match-owned local client/runtime artifacts.

Verify:

```text
match client/config/evidence temp cell removed
no persistent Exa/Tavily MCP registration
no OAuth/API-key/account state created
no background client process
PATH/shell/profile unchanged
user caches unchanged
repository contains only intended durable outputs
```

Classify:

```text
CLEAN_VERIFIED
CLEAN_WITH_RESIDUE
```

# Explicitly unauthorized

Do not:

- create Exa or Tavily accounts/API keys;
- run Tavily OAuth/login;
- enable Exa authenticated Agent features;
- use Tavily crawl/map/research;
- install Brave/SearXNG/Perplexity or another Challenger;
- add Native Search as a third contestant;
- perform page extraction/fetch for contestant scoring;
- change production routing/source ownership;
- modify the capability map/provider binding during the match itself;
- merge PR #3 or main.

# Stop states

Use the first applicable:

```text
READY_FOR_PRECISION_PLAYOFF_STAGING_REDESIGN
READY_FOR_PRECISION_PLAYOFF_REDESIGN
READY_FOR_ARENA_REVIEW
READY_FOR_NEXT_ARENA_DECISION
```

If a complete match produces a repeated-evidence candidate-slot result and teardown is clean, stop at `READY_FOR_ARENA_REVIEW` for Human acceptance/rejection of that test-stage recommendation.
