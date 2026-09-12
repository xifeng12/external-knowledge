---
task_id: TASK-20260912-003
status: ready_for_arena_execution
parent_task: TASK-20260912-001
target_repo: xifeng12/external-knowledge
target_ref: main
implementation_branch: task/20260912-001-v04-capability-diagnostics
capability: github.semantic
defender: gh-cli
challenger: github/github-mcp-server
arena_version: v0.1
ephemeral_challenger_staging_authorized: true
persistent_provisioning_authorized: false
new_credential_creation_authorized: false
pr_merge_authorized: false
---

# TASK-20260912-003 — Capability Arena v0.1 / GitHub Semantic First Match

## Goal

Establish the smallest evidence-driven Capability Arena needed by `external-knowledge`, then run the first real Challenger–Defender decision for:

```text
capability: github.semantic
Defender: gh-cli
Challenger: official GitHub MCP Server (github/github-mcp-server)
```

The purpose is not to produce a generic leaderboard. The purpose is to determine whether the existing source-semantic ownership for `github.semantic` should remain, change, split by scenario, or fuse validated strengths.

Allowed adjudication outcomes are exactly:

```text
REPLACE
KEEP_INCUMBENT
SPLIT_BY_SCENARIO
FUSE_VALIDATED_STRENGTHS
REJECT_CHALLENGER
NO_BATTLE
```

Success does not require the Challenger to win. A correctly blocked match is also a valid Arena result when admission cannot be satisfied without crossing an unauthorized boundary.

## Authority and start state

Before consequential local/runtime or repository actions, re-read:

- `tasks/TASK-20260912-001-SEARCH-CAPABILITY-EVOLUTION.md`;
- `reports/TASK-20260912-002-EVIDENCE-TIGHTENING.md`;
- this task;
- current remote head of `task/20260912-001-v04-capability-diagnostics`;
- Issue #2 as the derived routing/status pointer;
- PR #3 only where review/merge state is relevant.

Repository authority wins over chat summaries if they diverge. Never force-update over an unexpected remote writer.

## Human authorization receipt

The Human explicitly authorized two things for this phase:

1. add a hard Challenger cleanup/removal rule before any installation-based Arena work;
2. formally begin the first `github.semantic` Challenger–Defender match.

This authorizes **only the minimum ephemeral staging needed for the official GitHub MCP Challenger in this first match**, subject to the lifecycle and teardown contract below.

It does **not** authorize persistent production installation, new credential creation, interactive login, credential rotation/revocation, broad provider provisioning, additional Challengers, PR merge, or `main` merge.

# 1. Challenger Lifecycle and Teardown Contract — HARD REQUIREMENT

No Challenger may enter `STAGED` unless all four plans exist first:

```text
Provision Plan
Rollback Plan
Promotion Plan
Teardown Plan
```

The lifecycle is:

```text
DISCOVERED
  -> ADMITTED
  -> STAGED
  -> ARENA_RUNNING
  -> ADJUDICATED
       -> PROMOTED -> production deployment is a separate controlled action
       -> SPLIT/FUSED -> retain only explicitly accepted production behavior
       -> REJECTED -> TEARDOWN
  -> Arena execution cell TEARDOWN
  -> CLEAN_VERIFIED or CLEAN_WITH_RESIDUE
```

### 1.1 Baseline-before-install rule

Before Arena-owned staging, capture only decision-relevant baseline facts needed to distinguish pre-existing state from Arena-created state, for example:

```text
package/container present?
MCP registration present?
PATH/global install delta present?
temporary config path present?
cache/browser/runtime artifact present?
background process/service present?
```

Never infer ownership merely from current presence.

### 1.2 Arena provenance ledger

Every staged artifact must record:

```text
artifact / registration
preexisting: true|false
introduced_by_match: <match-id>|false
installation/staging method
scope/location
cleanup_policy
```

Arena may remove only artifacts it can prove it introduced.

Pre-existing user tools, packages, MCP registrations, credentials, caches, browsers, and config must not be deleted merely because a Challenger loses.

### 1.3 Ephemeral-by-default staging

Prefer an isolated execution cell such as:

```text
%TEMP%/external-knowledge-arena/<match-id>/
  runtime/
  config/
  cache/
  evidence/
```

or an equivalent temporary container/process scope.

Prefer, in order:

1. already operational Challenger exposure requiring no mutation;
2. temporary container or isolated executable/runtime;
3. temporary package prefix / venv / match-scoped config;
4. persistent/global installation only under a later explicit Human authorization.

Do not modify user-global PATH, persistent MCP config, shell profile, or production adapter merely to stage this match when an ephemeral path is viable.

### 1.4 Promotion is not “keep the Arena install”

If the Challenger wins or earns split/fused ownership:

```text
Arena runtime != Production runtime
```

The temporary Arena copy must still be torn down. Any production deployment/re-bind is a separate controlled action after adjudication and authorization.

### 1.5 Teardown verification

Uninstall/stop/delete success alone is insufficient. Verify the Arena-owned delta is gone and report:

```text
package/container delta reverted
match-scoped MCP/config removed
match-scoped process/service stopped
temporary runtime/cache removed where Arena-owned
persistent user state unchanged
repository working tree/state accounted for
```

Terminal cleanup classification:

```text
CLEAN_VERIFIED
CLEAN_WITH_RESIDUE
```

`CLEAN_WITH_RESIDUE` must enumerate exact residue and must not be presented as full rollback.

### 1.6 Credential lifecycle

Do not create, rotate, revoke, print, commit, or persist GitHub tokens/PATs/OAuth secrets in this task.

Existing GitHub authentication may be reused only when the runtime can pass it to the Challenger without exposing the secret value in logs/repository evidence and without creating persistent credential state.

If Challenger execution requires a new interactive login, new PAT/OAuth app, secret export into an unsafe surface, or credential mutation, stop at:

```text
READY_FOR_GITHUB_MCP_AUTH_DECISION
```

Remote credential revocation is never an implicit Arena teardown action.

# 2. Admission Gate

Do not run the match until both contestants satisfy operational admission for the selected scenario.

## Defender

Verify `gh-cli` using retained runtime evidence or one bounded read-only probe. Required:

```text
AVAILABLE
```

## Challenger

First inspect whether an official GitHub MCP execution surface is already operational in the current target runtime.

If already operational, use it and do not stage a second copy.

If not operational, the Human has authorized **ephemeral staging only** of `github/github-mcp-server` for this match, under Section 1.

Staging must not require persistent global configuration. If no safe ephemeral route exists, stop rather than widening scope.

Repository/package documentation or carrier presence alone is not operational evidence.

## Admission stop states

Use the first applicable state:

```text
READY_FOR_GITHUB_MCP_AUTH_DECISION
READY_FOR_GITHUB_MCP_STAGING_REDESIGN
NO_BATTLE
```

Do not manufacture a battle when admission is incomplete.

# 3. Arena Contract v0.1

Implement only the smallest domain-specific Arena contract needed by `external-knowledge`, preferably in:

```text
references/capability-arena.md
```

Do not build a generic benchmark platform.

A match requires all of:

```text
real capability overlap
real routing/ownership decision
operational Defender
operational Challenger
reachable decision-relevant real scenario
independent execution receipts
result capable of changing routing or ownership
```

Otherwise return `NO_BATTLE` with evidence.

Supported match modes in v0.1:

```text
SHADOW
HEAD_TO_HEAD
```

Use `SHADOW` unless a direct head-to-head read-only match is clearly safe and fair.

# 4. First real scenario

Use a real `external-knowledge` GitHub task, not a synthetic benchmark.

Preferred current scenario is Issue #2 / Draft PR #3 / current implementation branch. The task should exercise several real GitHub semantics, for example:

```text
identify current task/stop state
inspect PR metadata and branch head
inspect changed files or relevant commits
trace one decision/evidence artifact
return exact GitHub object references
explain current stop boundary
```

Both contestants are read-only with respect to GitHub objects during the match.

The same scenario, repository scope, authorization, evidence requirement, and bounded time/call budget must be given to both contestants.

Contestants must not consume each other's output.

# 5. Failure-domain normalization

Record whether the contestants share material execution dependencies such as:

```text
same GitHub API backend
same auth identity/token scope
same network/proxy
same local process/container
same MCP host/control plane
```

Shared dependencies do not invalidate semantic comparison, but they must not be misrepresented as independent resilience.

# 6. Independent evidence receipts

If a match runs, write sanitized receipts under:

```text
evidence/arena/<match-id>/defender.json
evidence/arena/<match-id>/challenger.json
evidence/arena/<match-id>/adjudication.json
```

Each contestant receipt should record at minimum:

```text
provider
execution_surface
capability
scenario
match mode
operations used
GitHub objects inspected
result summary
evidence references
errors/retries
elapsed time or bounded timing evidence
authorization boundary
environment mutation/staging evidence
```

Never store tokens, cookies, PATs, OAuth secrets, or raw credentials.

The adjudication receipt must also record the Challenger staging provenance and final teardown status.

# 7. Adjudication dimensions

Do not reduce the decision to one arbitrary aggregate score. Compare explicitly on:

```text
semantic correctness
evidence fidelity / traceability
coverage
precision / irrelevant output
determinism / reproducibility
execution cost
operational burden
failure-domain independence
agent ergonomics
scenario fit
```

Separate:

```text
verified fact
execution receipt
interpretation
decision
```

A likely `SPLIT_BY_SCENARIO` hypothesis may be tested — e.g. MCP for agent-native structured operations and `gh-cli` for deterministic shell/replay — but the result is not pre-decided.

# 8. Routing impact

Do not modify source ownership or adapters merely because the Challenger completes the match.

If adjudication supports a routing/ownership change, stop at:

```text
READY_FOR_ROUTING_CHANGE_DECISION
```

Only a later explicit authorization may promote the adjudicated result into production routing or persistent provider deployment.

# 9. Relationship with skill-forge

Do not duplicate a generic evaluation/runtime harness already owned by `skill-forge`.

Boundary:

```text
skill-forge
  = generic isolated execution / evaluation / rollback mechanics when reusable

external-knowledge
  = overlap detection / retrieval-specific rules / source-semantic adjudication / ownership decision
```

If using `skill-forge` requires broad integration work beyond this first match, record the integration point and defer it rather than expanding scope.

# 10. Explicitly unauthorized

Do not:

- persistently install/register GitHub MCP for production;
- install any other Challenger (Crawl4AI, Tavily, Brave, Perplexity, Browser Use, etc.);
- create or rotate credentials;
- expose credential values;
- change global PATH/shell profiles merely for the match;
- modify proxies/TLS/browser state;
- run synthetic benchmark matrices;
- modify GitHub issues/PRs as part of contestant actions;
- promote GitHub MCP without adjudication + later authorization;
- delete `gh-cli` or any pre-existing user tool;
- merge PR #3 or merge to `main`;
- keep an Arena-owned temporary installation simply because the Challenger wins.

# 11. Validation invariants

At minimum validate these decision-relevant invariants:

```text
no overlap -> NO_BATTLE
missing operational contestant -> no fabricated battle
Arena cannot delete pre-existing artifacts
Arena-owned staged artifact -> teardown required after match
promotion decision != retain Arena runtime
credential mutation requirement -> stop for authorization
shared backend != independent resilience
contestant outputs remain isolated
only adjudication may recommend routing ownership change
presence alone cannot win a match
```

Add focused tests only where code is introduced to protect these invariants. Do not create a broad benchmark suite.

# 12. Required durable outputs

If admission succeeds and a match runs:

```text
references/capability-arena.md
reports/TASK-20260912-003-GITHUB-ARENA.md
evidence/arena/<match-id>/defender.json
evidence/arena/<match-id>/challenger.json
evidence/arena/<match-id>/adjudication.json
```

If admission stops before a real match, still write:

```text
reports/TASK-20260912-003-GITHUB-ARENA.md
```

with exact scoped evidence, the stop reason, and any Arena staging/teardown receipt if staging was attempted.

Update Issue #2 as the derived status pointer. Do not create a parallel issue unless current repository authority requires one.

# 13. Terminal states

Use the first applicable terminal state:

```text
READY_FOR_GITHUB_MCP_AUTH_DECISION
READY_FOR_GITHUB_MCP_STAGING_REDESIGN
READY_FOR_ARENA_REVIEW
READY_FOR_ROUTING_CHANGE_DECISION
```

All terminal states must include Arena cleanup status when any staging occurred.

Do not continue from this task into the next Challenger or production promotion in the same run.
