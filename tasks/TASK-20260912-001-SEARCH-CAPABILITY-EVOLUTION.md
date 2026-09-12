---
task_id: TASK-20260912-001
status: ready_for_second_arena_execution
target_repo: xifeng12/external-knowledge
target_ref: main
implementation_branch: task/20260912-001-v04-capability-diagnostics
result_path: reports/TASK-20260912-001-IMPLEMENTATION.md
diagnostic_result_path: reports/TASK-20260912-001-MACHINE-DIAGNOSTIC.md
machine_receipt_path: evidence/TASK-20260912-001-machine-capability-receipt.json
isolated_worker_authorized: true
active_arena_task: tasks/TASK-20260912-004-CAPABILITY-ARENA-COMPLEX-WEB.md
---

# Goal

`external-knowledge` is the durable source of truth for external-information capability routing, diagnosis, and evidence-driven Challenger–Defender ownership decisions.

The current program must:

- route concrete information needs/source semantics to the best available retrieval path;
- diagnose machine capability without confusing carrier/config presence with runtime availability;
- preserve operational status, semantic coverage, discoverability, source-semantic fit, and failure-domain independence as separate evidence axes;
- admit a Challenger only when there is real overlap and a real decision-relevant scenario;
- keep Arena staging temporary, provenance-tracked, reversible, and independently adjudicated;
- promote no routing/provider merely because it was installed or won one scoped match.

# Current accepted baseline

`main` remains the accepted `v0.3-beta.1` baseline. Candidate evolution remains on:

```text
task/20260912-001-v04-capability-diagnostics
```

under Draft PR #3.

Completed durable increments:

```text
TASK-001  machine-capability diagnostics and capability map
TASK-002  evidence tightening for wechat.reader / Exa / Firecrawl
TASK-003  Capability Arena v0.1 first real match
```

TASK-003 was accepted after review correction against raw contestant receipts:

```text
capability: github.semantic
defender: gh-cli
challenger: github/github-mcp-server v1.12.1
outcome: KEEP_INCUMBENT
routing: github.semantic -> gh-cli
teardown: CLEAN_VERIFIED
```

No production GitHub MCP installation remains.

# Capability Arena authority

The reusable Arena authority is:

```text
references/capability-arena.md
```

Current version: `v0.2`.

v0.2 generalizes the accepted v0.1 lifecycle beyond GitHub-specific objects while preserving:

```text
real overlap + real scenario admission
SHADOW / HEAD_TO_HEAD isolation
same-scenario fairness
raw contestant receipts as primary execution evidence
baseline + staging provenance
Provision / Rollback / Promotion / Teardown plans
Arena may delete only Arena-owned artifacts
Arena runtime != Production runtime
CLEAN_VERIFIED / CLEAN_WITH_RESIDUE teardown
no routing mutation without later explicit authorization
```

# Effective invariants

1. Repository authority outranks chat summaries and machine-local copies.
2. `UNKNOWN != MISSING_CONFIRMED`.
3. Skill/carrier/config/package presence does not establish provider `AVAILABLE`.
4. Provider availability, semantic coverage, discoverability, source fit, and failure-domain independence stay separate.
5. No synthetic battle merely to exercise a framework or fill a matrix.
6. A battle requires real overlap, operational contestants, a reachable real case, independent receipts, and decision relevance.
7. Arena-owned staging requires baseline/provenance and all four lifecycle plans before `STAGED`.
8. Arena can remove only artifacts proven to be introduced by that match.
9. A winning temporary Challenger runtime is still torn down; production deployment is a separate decision.
10. Reports/adjudications must reconcile to raw contestant receipts.
11. One real case supports only a scoped conclusion unless broader evidence exists.
12. Do not broaden work after the first authorized terminal state.

# Current Human authorization — TASK-004

The Human accepted Arena v0.1 and authorized the next real match.

The active execution contract is:

```text
tasks/TASK-20260912-004-CAPABILITY-ARENA-COMPLEX-WEB.md
```

Match:

```text
capability: complex-web.read
Defender: runtime-native.webfetch
Challenger: unclecode/crawl4ai
Arena contract: references/capability-arena.md v0.2
```

## Real-scenario gate

Before any Crawl4AI staging, the Coordinator must identify one preserved, decision-relevant real complex-web read case from accepted repository evidence/current workload.

Preferred candidate is the exact canonical WeChat article used by TASK-002 P7 only if its identity is durably recorded and it remains reachable. Otherwise use another preserved real case with accepted evidence of incomplete/degraded/dynamic/blocked native reading.

Do not invent a demo/synthetic page.

If no qualifying case exists, do not stage Crawl4AI; stop at:

```text
READY_FOR_COMPLEX_WEB_CASE_DECISION
```

## Authorized ephemeral staging

Only after the real-scenario gate passes, TASK-004 may stage Crawl4AI inside a match-scoped Arena cell, including only:

```text
isolated Python venv/package prefix
Crawl4AI + Python dependencies
match-scoped Playwright/Chromium binary if required
match-scoped package/browser caches
match driver/config/evidence
```

Browser/package/cache paths must remain match-owned so teardown is provable.

Persistent/global installation, system/user Python mutation, PATH/MCP changes, elevation/system dependency install, browser profile/cookie import, new credentials/API keys, proxy/TLS mutation, and other Challengers are not authorized.

If safe isolated staging requires any such action, teardown partial staging and stop at:

```text
READY_FOR_CRAWL4AI_STAGING_REDESIGN
```

# Required TASK-004 execution behavior

The target-machine Coordinator/Agent must:

```text
re-read TASK-001 + TASK-004 + Arena v0.2 + current Issue/PR/head
pass the real-case Admission Gate before staging
capture pre-staging baseline and four lifecycle plans
stage Crawl4AI ephemerally only if eligible
run one bounded real match under TASK-004 fairness rules
produce independent defender/challenger/adjudication receipts
teardown all Arena-owned artifacts even if Crawl4AI wins
verify CLEAN_VERIFIED or enumerate CLEAN_WITH_RESIDUE
push durable report/receipts
synchronize Issue #2
stop at the first TASK-004 terminal state
```

No adapter/source-ownership change, persistent provider promotion, third match, PR #3 merge, or `main` merge is authorized in the same run.

# Current stop / next action

Current state:

```text
READY_FOR_SECOND_ARENA_EXECUTION
```

Next authorized action belongs to the target-machine Coordinator/Agent executing TASK-004 through its first terminal state.
