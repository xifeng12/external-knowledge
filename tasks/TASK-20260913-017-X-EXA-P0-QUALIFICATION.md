---
task_id: TASK-20260913-017
status: ready_for_x_exa_p0_qualification
parent_task: TASK-20260912-001
predecessor: TASK-20260913-016
assessment: reports/X-PROVIDER-ALTERNATIVES-ASSESSMENT-20260913.md
target_repo: xifeng12/external-knowledge
implementation_branch: task/20260912-001-v04-capability-diagnostics
capability: x.search
provider_under_test: exa-hosted-mcp
paid_provider_staging_authorized: false
new_credentials_authorized: false
production_binding_authorized: false
network_change_authorized: false
merge_authorized: false
---

# TASK-20260913-017 — X Search P0 Qualification via Exa

## Goal

Perform one tiny, bounded qualification of the already-available anonymous Exa hosted MCP as a replacement **only for the missing `x.search` leg**.

This task exists because the project has already spent enough time on X. It is the final X task in the current roadmap slice.

Existing XActions capabilities remain untouched:

```text
x.account.timeline -> existing vpsmanage / XActions
x.post.read        -> existing vpsmanage / XActions
x.search           -> missing; only this leg is under test here
```

Do not reopen XActions search/session/query-ID work.

## Goal Integrity stop rule

This task has exactly two search fixtures.

```text
2/2 PASS -> X_SEARCH_EXA_TEST_STAGE_AVAILABLE
anything else -> X_SEARCH_DEFERRED_BY_GOAL_INTEGRITY
```

If the result is deferred, STOP X work. Do not continue to SocialData, official X API, TwitterAPI.io, OpenCLI, Android GraphQL, another CLI, or another search provider in this task. Do not create a successor X task automatically.

## Existing accepted evidence

TASK-013 already proved on the mainland host, without proxy:

```text
mcp.exa.ai reachable
anonymous MCP initialize PASS
web_search_exa PASS
web_fetch_exa PASS
provider-side read of a locally blocked foreign source PASS
```

TASK-016 accepted final XActions state:

```text
S0 HomeTimeline guest-vs-fresh differential PASS
search/followers still authorization-shaped failure
getTweets PASS
getTweet PASS
X_PROVIDER_ALTERNATIVE_REQUIRED
```

Provider-alternative assessment ranks Exa P0 first because it adds no new credentials, no installation, and no new operational surface.

## Execution environment

Run from the existing mainland host used in TASK-013/016.

Requirements:

- no proxy for Exa probes;
- no network/system configuration changes;
- anonymous Exa hosted MCP only;
- no API key, account signup, OAuth, paid plan, or provider installation;
- no changes to `vpsmanage`, XActions, Mihomo, n8n, Gate D, or production X monitoring.

## Fixture preparation

Use the existing healthy XActions timeline read **only as a control source**, not as the search provider.

Make one bounded read:

```text
getTweets('zcode_ai', 5)
```

From those returned public posts, freeze exactly two distinct recent fixtures before calling Exa:

### F1 — exact account + distinctive phrase

Choose one recent post with sufficiently distinctive material text.

Freeze:

```text
expected_post_id
expected_username = zcode_ai
expected_canonical_url = https://x.com/zcode_ai/status/<numeric-id>
query = account identity + distinctive phrase from the post
```

### F2 — broader keyword discovery

Choose a second, different recent post.

Build a broader query from its subject/keywords without using the full exact sentence and without including the expected numeric Post ID.

Freeze:

```text
expected_post_id
expected_username = zcode_ai
expected_canonical_url
query = broader topical phrase
```

The two fixtures must use different Post IDs.

Do not add more fixtures.

## Exa probe

Use the existing anonymous hosted MCP.

For each fixture:

1. Search with `web_search_exa`.
2. Target/restrict toward `x.com` / `twitter.com` when the tool schema supports domain restriction; otherwise encode the site/domain constraint in the query.
3. Inspect at most the first 10 results.
4. Accept only canonical or canonicalizable status URLs matching:

```text
https://x.com/<username>/status/<numeric-id>
https://twitter.com/<username>/status/<numeric-id>
```

5. For the expected target when found, require material post text/snippet from search or a successful provider-side `web_fetch_exa` read.
6. Record publication/date metadata when Exa provides it; do not invent recency.

## Fixture PASS criteria

A fixture passes only when all are true:

```text
expected numeric Post ID found within first 10 Exa results
returned/canonicalized username matches expected public account
material post text/snippet is available
text is materially consistent with the frozen control post
no false canonical substitution
```

A search result that merely links to an X profile, search page, mirror, screenshot, quoted article, or unrelated status does not pass.

## Overall outcome

### Outcome A — Exa sufficient for bounded X discovery

Required:

```text
F1 PASS
F2 PASS
```

Then record:

```text
x.search -> Exa hosted MCP (test-stage, web-indexed discovery)
x.account.timeline -> existing XActions
x.post.read -> existing XActions
```

Important scope language:

- This is **web-indexed X discovery**, not a claim of complete X search/firehose parity.
- Coverage and recency are limited by Exa indexing.
- Do not claim followers, home timeline, bookmarks, or other X session semantics through Exa.

Terminal state:

```text
X_SEARCH_EXA_TEST_STAGE_AVAILABLE
```

A bounded capability-map note is authorized only for this outcome.

### Outcome B — Exa insufficient

If either fixture fails for coverage, freshness, wrong target, missing material text, or inability to fetch the target:

```text
x.search remains unresolved
the gap is explicitly deferred by Goal Integrity
existing XActions timeline/known-post read remains preserved
```

Terminal state:

```text
X_SEARCH_DEFERRED_BY_GOAL_INTEGRITY
```

Do NOT evaluate or stage P1/P2/P3/P4/P5 afterward. The Human may reopen X search later if it becomes decision-critical.

## Time / scope budget

This task must remain tiny:

```text
one control timeline read
2 frozen fixtures
<= 10 Exa results inspected per fixture
at most one provider-side fetch per expected target
no retries for quality/coverage failure
```

A single retry is allowed only for a concrete transient transport/runtime error.

Do not broaden the benchmark, add providers, or investigate why Exa misses a post.

## Required outputs

Write:

```text
reports/TASK-20260913-017-X-EXA-P0-QUALIFICATION.md
evidence/TASK-20260913-017-x-exa-p0.json
```

Receipt should contain only non-secret evidence:

```text
fixture IDs and queries
expected public Post IDs / canonical URLs
Exa result ranks and returned URLs
a material-text-match boolean / short non-copyright-heavy excerpt if needed
fetch success/failure
observed date metadata when provided
overall outcome
cleanup state
```

Do not store credentials, private data, cookies, private timeline content, or unrelated result bodies.

## Explicitly unauthorized

- any further XActions search/session/query-ID repair;
- SocialData signup/key use;
- official X API signup/key use;
- TwitterAPI.io signup/key use;
- installing/authenticating OpenCLI, twitter-cli, x-cli, or another X client;
- browser automation for X;
- new X account;
- new proxy/VPN/TUN/network changes;
- production provider binding;
- changes to vpsmanage or production X monitoring;
- PR #3 merge or main merge.

## Cleanup

Remove only task-owned scratch probe artifacts.

Verify production X monitoring and prior sessions were untouched.

## Stop

Stop at the first accurate terminal state:

```text
X_SEARCH_EXA_TEST_STAGE_AVAILABLE
X_SEARCH_DEFERRED_BY_GOAL_INTEGRITY
```

Push report/receipt, synchronize Issue #2, and stop. This closes the current X workstream regardless of outcome.
