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

The current program must route concrete information needs/source semantics to the best available retrieval path, diagnose machine capability without confusing carrier/config presence with runtime availability, and evaluate materially overlapping providers through bounded real-task Arena matches.

# Current accepted baseline

- `main` remains the accepted `v0.3-beta.1` baseline.
- Candidate evolution remains on `task/20260912-001-v04-capability-diagnostics` under Draft PR #3.
- TASK-001 diagnostics and TASK-002 evidence tightening are complete.
- TASK-003 Capability Arena v0.1 was accepted after receipt reconciliation.
- First match outcome: `github.semantic` → `KEEP_INCUMBENT`; owner remains `gh-cli`; teardown `CLEAN_VERIFIED`.
- `references/capability-arena.md` is now v0.2 and is the reusable Arena authority.

# Effective invariants

1. Repository authority outranks chat summaries and machine-local copies.
2. `UNKNOWN != MISSING_CONFIRMED`.
3. Presence/declaration/config does not establish provider `AVAILABLE`.
4. Availability, semantic coverage, discoverability, source fit, and failure-domain independence remain separate.
5. No synthetic battle merely to exercise the framework.
6. A match requires real overlap, operational contestants, a real reachable scenario, independent receipts, and decision relevance.
7. Arena-owned staging requires baseline/provenance plus Provision/Rollback/Promotion/Teardown plans before `STAGED`.
8. Arena may remove only artifacts proven to be introduced by that match.
9. `Arena runtime != Production runtime`; winning temporary runtimes are still torn down.
10. Raw contestant receipts are primary execution evidence.
11. One real case supports only a scoped conclusion unless broader evidence exists.
12. Routing promotion is always a later explicit authorization.

# Current Human authorization — TASK-004

The Human accepted Arena v0.1 and authorized the next real match.

Active contract:

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

Before any Crawl4AI staging, the Coordinator must identify one preserved decision-relevant real complex-web case from accepted evidence/current workload. Preferred candidate is the exact canonical WeChat article from TASK-002 P7 only if its identity is durably recorded and still reachable; otherwise use another preserved real case with accepted evidence of degraded/dynamic/blocked native reading.

If no qualifying case exists, do not stage Crawl4AI; stop at `READY_FOR_COMPLEX_WEB_CASE_DECISION`.

If the gate passes, TASK-004 may ephemerally stage only a match-scoped Python venv/package prefix, Crawl4AI and Python dependencies, a match-scoped Playwright/Chromium binary if required, and match-owned caches/config/evidence. Persistent/global installation, system/user Python mutation, PATH/MCP changes, elevation/system dependency install, browser profile/cookie import, new credentials/API keys, proxy/TLS mutation, other Challengers, production routing changes, PR #3 merge, and `main` merge remain unauthorized.

If safe isolation is impossible, teardown partial staging and stop at `READY_FOR_CRAWL4AI_STAGING_REDESIGN`.

# Current stop / next action

```text
READY_FOR_SECOND_ARENA_EXECUTION
```

The target-machine Coordinator/Agent must execute TASK-004 through its first terminal state, push the required report/receipts, synchronize Issue #2, and stop. No third match or production promotion is authorized in the same run.
