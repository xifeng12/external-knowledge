---
task_id: TASK-20260912-001
status: ready_for_second_arena_execution
target_repo: xifeng12/external-knowledge
target_ref: main
implementation_branch: task/20260912-001-v04-capability-diagnostics
active_arena_task: tasks/TASK-20260912-004-CAPABILITY-ARENA-COMPLEX-WEB.md
---

# Current authority

The active execution contract is `tasks/TASK-20260912-004-CAPABILITY-ARENA-COMPLEX-WEB.md` under `references/capability-arena.md` v0.2.

Accepted prior result:

```text
TASK-003 github.semantic
gh-cli vs github/github-mcp-server
KEEP_INCUMBENT
routing remains gh-cli
CLEAN_VERIFIED
```

Current authorized match:

```text
TASK-004
capability: complex-web.read
Defender: runtime-native.webfetch
Challenger: unclecode/crawl4ai
```

Before staging, the target-machine Coordinator must pass TASK-004's real-scenario gate. No synthetic/demo page is allowed. If no qualifying preserved real complex-web case exists, stop at `READY_FOR_COMPLEX_WEB_CASE_DECISION` without staging.

If the gate passes, only match-scoped ephemeral Crawl4AI staging is authorized: isolated Python environment/package dependencies, match-scoped Playwright/Chromium when required, and match-owned caches/config/evidence. Arena-owned staging requires baseline/provenance and Provision/Rollback/Promotion/Teardown plans and must end `CLEAN_VERIFIED` or explicitly `CLEAN_WITH_RESIDUE`.

Persistent/global provider installation, system/user Python or PATH/MCP mutation, elevation/system dependencies, profile/cookie import, new credentials/API keys, proxy/TLS mutation, other Challengers, production routing change, PR #3 merge, and `main` merge remain unauthorized.

Current state:

```text
READY_FOR_SECOND_ARENA_EXECUTION
```

Execute TASK-004 through its first terminal state, push its durable report/receipts, synchronize Issue #2, and stop. No third match or production promotion is authorized in the same run.
