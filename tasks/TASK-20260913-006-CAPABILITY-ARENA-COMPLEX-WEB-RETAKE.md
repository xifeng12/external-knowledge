---
task_id: TASK-20260913-006
status: superseded_by_task_007
parent_task: TASK-20260912-001
supersedes_exam: TASK-20260912-004
superseded_by: TASK-20260913-007
target_repo: xifeng12/external-knowledge
implementation_branch: task/20260912-001-v04-capability-diagnostics
arena_contract: references/capability-arena.md
arena_version: v0.4
capability: complex-web.read
defender: runtime-native.webfetch
challenger: unclecode/crawl4ai
challenger_staging_authorized: false
persistent_provisioning_authorized: false
routing_change_authorized: false
pr_merge_authorized: false
---

# TASK-20260913-006 — Corrected Complex Web Arena / Real-Case Qualification

## Historical purpose

TASK-006 attempted to qualify a **real ordinary-URL workload case** after TASK-004 was invalidated by the Source-Semantic Ownership Gate.

Its execution result remains factual:

```text
READY_FOR_COMPLEX_WEB_CASE_DECISION
no qualifying real ordinary-URL case existed in retained evidence/workload
no Challenger staging occurred
```

See:

```text
reports/TASK-20260913-006-CASE-QUALIFICATION.md
```

## Human review correction

The Human clarified that the project is currently in the **testing stage**. Requiring every test-stage Arena to originate from a real workload was an over-constraint.

Controlled synthetic/public benchmark fixtures may provide stronger evidence for capability testing because they offer known ground truth, repeatability, and deliberate isolation of static/dynamic/progressive extraction behavior.

Arena v0.4 therefore separates:

```text
CONTROLLED_BENCHMARK
REAL_REPLAY
REAL_WORKLOAD
```

TASK-006's real-case search remains valid evidence but is no longer a prerequisite for continuing the test-stage `complex-web.read` competition.

The active successor is:

```text
tasks/TASK-20260913-007-COMPLEX-WEB-CONTROLLED-BENCHMARK.md
```

See also:

```text
reports/TASK-20260913-006-TEST-STAGE-REVIEW.md
```

## Production boundary

The distinction introduced by v0.4 is:

```text
controlled benchmark -> capability profile / Challenger screening / scenario hypothesis
real replay/workload  -> production routing/ownership validation
```

A controlled benchmark alone cannot change production routing/source ownership.
