---
task_id: TASK-20260912-004
status: ready_for_arena_execution
parent_task: TASK-20260912-001
target_repo: xifeng12/external-knowledge
target_ref: main
implementation_branch: task/20260912-001-v04-capability-diagnostics
arena_contract: references/capability-arena.md
arena_version: v0.2
capability: complex-web.read
defender: runtime-native.webfetch
challenger: unclecode/crawl4ai
ephemeral_challenger_staging_authorized: true
match_scoped_browser_staging_authorized: true
persistent_provisioning_authorized: false
system_dependency_install_authorized: false
new_credential_creation_authorized: false
pr_merge_authorized: false
---

# TASK-20260912-004 — Capability Arena / Complex Web Read: WebFetch vs Crawl4AI

## Goal

Run the second real Capability Arena match for:

```text
capability: complex-web.read
Defender: runtime-native.webfetch
Challenger: unclecode/crawl4ai
```

The purpose is to decide whether the current degraded native path should remain the sole/default owner for complex-page reads, or whether Crawl4AI earns a scenario-specific escalation/ownership role.

This is not a synthetic crawler benchmark and not a request to install Crawl4AI permanently.

Allowed adjudication outcomes remain:

```text
REPLACE
KEEP_INCUMBENT
SPLIT_BY_SCENARIO
FUSE_VALIDATED_STRENGTHS
REJECT_CHALLENGER
NO_BATTLE
```

## Authority and start state

Before consequential local/runtime or repository actions, re-read:

- `tasks/TASK-20260912-001-SEARCH-CAPABILITY-EVOLUTION.md` as historical parent authority;
- `reports/TASK-20260912-002-EVIDENCE-TIGHTENING.md`;
- `tasks/TASK-20260912-003-CAPABILITY-ARENA-GITHUB.md` and its accepted result;
- `references/capability-arena.md` v0.2;
- this task as the active execution authority;
- current remote head of `task/20260912-001-v04-capability-diagnostics`;
- Issue #2 as the derived status pointer;
- PR #3 only where review/merge state is relevant.

TASK-001 remains preserved as historical parent authority; TASK-004 is the current execution contract for this match. Repository authority wins over chat summaries. Never force-update over an unexpected remote writer.

## Human authorization receipt

After accepting Arena v0.1, the Human explicitly authorized starting the next match.

For TASK-004 this authorizes only the minimum **ephemeral staging** required to execute Crawl4AI as the Challenger, after the real-scenario Admission Gate passes.

Authorized staging may include, only inside the match-scoped Arena cell:

```text
isolated Python virtual environment / package prefix
Crawl4AI package and its Python dependencies
match-scoped Playwright/Chromium browser binary when required
match-scoped pip/package/browser cache
match driver/config/evidence files
```

All such artifacts must have baseline/provenance/rollback/promotion/teardown records and must be removed after the match, even if Crawl4AI wins.

Not authorized:

```text
persistent/global Crawl4AI installation
system-wide or user-global PATH change
persistent MCP registration
admin/elevated OS package installation
system dependency mutation
browser/profile/cookie import
new credentials/API keys
proxy/TLS mutation
production adapter/routing change
other Challengers
PR #3/main merge
```

If safe isolated staging is impossible without crossing one of those boundaries, stop at `READY_FOR_CRAWL4AI_STAGING_REDESIGN`.

# 1. Real-Scenario Admission Gate — BEFORE staging

Do not stage Crawl4AI merely to exercise Arena machinery.

First identify one preserved, decision-relevant **real complex-web read case** from accepted repository evidence or an already-reachable current workload.

Preferred candidate order:

1. the exact canonical WeChat article used by TASK-20260912-002 P7, **only if its target identity is durably recorded and the page remains reachable**; this is a real anti-bot/complex-read case where `web_reader` previously supplied useful extraction-fallback evidence;
2. another preserved real case in current repository evidence where ordinary/native reading was observed to be incomplete, degraded, dynamic, blocked, or otherwise decision-relevant for `complex-web.read`.

Do not invent a demo site, benchmark page, or artificial JavaScript page.

The selected case must have enough accepted evidence to define what matters, such as title/author/body/sections/code/metadata or another concrete completeness criterion.

If no qualifying real case exists, do not stage the Challenger. Record the search scope and stop at:

```text
READY_FOR_COMPLEX_WEB_CASE_DECISION
```

A valid `NO_BATTLE` is preferable to a synthetic match.

# 2. Defender Admission

Verify `runtime-native.webfetch` is operational in the current target runtime for the selected target using retained runtime evidence plus the match's representative call.

Static/native-tool presence alone is insufficient if the selected target cannot actually be attempted.

Record the exact observed behavior without upgrading generic `complex-web.read` beyond the selected scenario.

# 3. Challenger Baseline and Ephemeral Staging

Only after Sections 1 and 2 pass:

1. capture the decision-relevant pre-staging baseline;
2. check whether Crawl4AI is already operational in a supported runtime exposure;
3. if it is already operational, use that exposure and do not stage a second copy;
4. otherwise create a match-scoped Arena cell and stage it ephemerally.

Before `STAGED`, record all four plans:

```text
Provision Plan
Rollback Plan
Promotion Plan
Teardown Plan
```

## Isolation requirements

Prefer a cell under a temporary Arena root, e.g.:

```text
%TEMP%/external-knowledge-arena/<match-id>/
  runtime/
  venv/
  browser/
  cache/
  config/
  evidence/
```

Use an isolated venv/package prefix. Do not install into system/user Python.

If Playwright/Chromium is needed, force its browser/cache location into the match cell (for example with a match-scoped `PLAYWRIGHT_BROWSERS_PATH` or equivalent supported mechanism) so teardown ownership is unambiguous.

Prefer no persistent package cache; otherwise keep it in the match cell.

Do not call setup helpers whose side effects are unknown merely to inspect presence. The Camoufox incident from TASK-002 remains the precedent: path/verify helpers that trigger download are provisioning actions.

Pin and record the exact Crawl4AI version actually staged. Do not use external LLM/API extraction in this match; the Challenger must run without introducing a new LLM-provider/API-key variable.

If staging requires admin rights, OS packages, persistent browser state, global configuration, or another non-cell mutation, stop at `READY_FOR_CRAWL4AI_STAGING_REDESIGN` and teardown any Arena-owned partial staging.

# 4. Match Mode and Fairness

Use `HEAD_TO_HEAD` only if both contestants can independently read the same real target safely. Otherwise use `SHADOW` and explain why.

Both receive the same:

```text
target URL / source identity
content objective
success evidence criteria
network/proxy state already in force
read-only authorization
time window
bounded data-attempt budget
```

Contestants must not consume each other's outputs.

Historical accepted evidence for the selected page may be used by the adjudicator as a reference baseline, but neither contestant may consume the other contestant's current-run output.

## Bounded attempts

Each contestant gets:

```text
1 primary data attempt
+ at most 1 retry for a concrete transient/tool/runtime error
```

Do not tune site-specific selectors, scripts, waits, or extraction rules after seeing the opponent's result. If a provider needs provider-specific default configuration to perform its documented normal read, record that configuration and its operational cost.

Staging/download time is not hidden inside fetch latency; record it separately as operational burden.

# 5. Match Evidence

For the selected real case, compare only decision-relevant dimensions. At minimum consider:

```text
semantic/content correctness
main-body completeness
structure preservation (headings/lists/code/tables where applicable)
metadata fidelity when present
source/link traceability
required rendered/dynamic content if the case depends on it
precision / boilerplate noise
determinism / reproducibility
fetch latency
staging/download/runtime footprint
operational burden
failure-domain independence
agent ergonomics
scenario fit
```

Images/media are scored only if the accepted case evidence says they matter. Do not add dimensions for completeness theater.

Do not reduce the outcome to one aggregate score.

# 6. Failure-Domain Normalization

Record shared and independent dependencies, including where relevant:

```text
network/proxy path
DNS/TLS path
remote extraction service vs local browser
browser engine
anti-bot surface
cache/control plane
```

A local browser-based Challenger may provide a different execution/failure domain from native WebFetch, but independence must be demonstrated from the actual path, not assumed from product names.

# 7. Durable Receipts

If a match runs, write:

```text
reports/TASK-20260912-004-COMPLEX-WEB-ARENA.md
evidence/arena/<match-id>/defender.json
evidence/arena/<match-id>/challenger.json
evidence/arena/<match-id>/adjudication.json
```

Contestant receipts must include at least:

```text
provider
exact execution surface/version where observable
capability
real target identity
match mode
attempts/calls
result summary
content/structure evidence sufficient for adjudication
errors/retries
fetch timing
resource/staging evidence
authorization boundary
environment mutation evidence
```

Do not commit full copyrighted article bodies merely to prove extraction quality. Store only minimum necessary snippets/hashes/field summaries consistent with repository evidence policy.

The adjudication receipt must include the Challenger provenance ledger, four plans, failure-domain analysis, decision, routing impact, and teardown status.

# 8. Adjudication Guidance

Test these hypotheses; do not pre-decide them:

```text
KEEP_INCUMBENT
  native WebFetch is sufficient and cheaper for the observed complex case

SPLIT_BY_SCENARIO
  WebFetch remains default, Crawl4AI is justified for a clearly defined complex/dynamic escalation scenario

FUSE_VALIDATED_STRENGTHS
  routing becomes WebFetch-first -> observed gap -> Crawl4AI fallback, if evidence supports that chain

REPLACE
  Crawl4AI materially dominates the current owner broadly enough for this capability ownership question

REJECT_CHALLENGER
  Crawl4AI is operational but its quality/cost/burden does not justify remaining an active challenger for this ownership question
```

One real case is enough to make a scoped scenario decision; it is not enough to claim universal web superiority. Preserve scope in the wording.

# 9. Teardown — mandatory after any staging

Regardless of outcome, remove the Arena-owned Challenger runtime and verify return to baseline.

Verify, as applicable:

```text
no Crawl4AI/browser process remains
match venv/package prefix removed
match-scoped browser binary/cache removed
no PATH/MCP/shell-profile changes exist
no persistent browser profile/cookies created
pre-existing user Python/browser state unchanged
repository state contains only intended durable outputs
```

Classify exactly:

```text
CLEAN_VERIFIED
CLEAN_WITH_RESIDUE
```

If residue remains, enumerate it. Do not call teardown complete merely because uninstall/delete returned success.

Even a winning Crawl4AI Arena runtime must be deleted. Production deployment is a later explicit authorization.

# 10. Routing Impact

Do not modify adapter/source ownership during this run.

If evidence supports a routing or ownership change, stop at:

```text
READY_FOR_ROUTING_CHANGE_DECISION
```

If no routing change is supported, stop at `READY_FOR_ARENA_REVIEW`.

# 11. Arena Contract Evolution

TASK-004 may amend `references/capability-arena.md` only if this real match exposes a reusable provider-agnostic invariant. Crawl4AI/WebFetch-specific behavior belongs in this report/receipts, not the generic contract.

Do not build a generic benchmark/runtime harness. If reusable staging/rollback mechanics should move to `skill-forge`, record the integration point and defer it.

# 12. Explicitly Unauthorized

Do not:

- install/configure Firecrawl, Exa, Tavily, Brave, Browser Use, Perplexity, Agent-Reach, or any other Challenger;
- use a synthetic/demo page merely to force a match;
- persistently install Crawl4AI;
- mutate system/user Python or PATH;
- install OS/system dependencies or use elevation;
- create/import browser profiles, cookies, or credentials;
- change proxy/TLS configuration;
- use paid/external LLM extraction as a hidden dependency;
- modify production routing/adapter ownership;
- merge PR #3 or `main`.

# 13. Terminal States

Use the first applicable terminal state:

```text
READY_FOR_COMPLEX_WEB_CASE_DECISION
READY_FOR_CRAWL4AI_STAGING_REDESIGN
READY_FOR_ARENA_REVIEW
READY_FOR_ROUTING_CHANGE_DECISION
```

If staging was attempted, every terminal state must include `CLEAN_VERIFIED` or `CLEAN_WITH_RESIDUE`.

Stop at the first terminal state. Do not continue into a third Challenger/match or production promotion in the same run.
