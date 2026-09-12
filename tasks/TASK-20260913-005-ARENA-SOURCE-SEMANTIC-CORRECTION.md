---
task_id: TASK-20260913-005
status: completed
parent_task: TASK-20260912-001
reviewed_task: TASK-20260912-004
target_repo: xifeng12/external-knowledge
implementation_branch: task/20260912-001-v04-capability-diagnostics
arena_contract: references/capability-arena.md
arena_version: v0.3
review_outcome: NO_BATTLE_INVALID_SCENARIO
next_task: TASK-20260913-006
---

# TASK-20260913-005 — Arena Source-Semantic Routing Correction

## Human review finding

TASK-20260912-004 used a canonical WeChat article as the representative scenario for generic `complex-web.read`.

That was a routing error.

Repository authority already models canonical WeChat article reading as the first-class specialist semantic `wechat.reader`; `complex-web.read` is the extraction-escalation path for ordinary known URLs after an observed ordinary-read gap.

Therefore the TASK-004 scenario did not legally represent the ownership question it attempted to adjudicate.

## Review decision

The TASK-004 execution facts remain valid observations:

- native WebFetch/default native path was fingerprint-blocked on the selected WeChat article;
- Crawl4AI 0.9.3 default configuration was also fingerprint-blocked;
- Crawl4AI staging/teardown evidence remains valid;
- Arena cleanup remains `CLEAN_VERIFIED`.

But the ownership adjudication is superseded:

```text
previous: REJECT_CHALLENGER for complex-web.read
review:   NO_BATTLE / INVALID_SCENARIO
```

The reviewed match does **not** count as a loss for Crawl4AI and does not establish that Crawl4AI should be rejected for generic `complex-web.read`.

No routing change follows from TASK-004.

## Correct exam routing

### Generic complex-web.read Arena

A future generic `complex-web.read` match must use a real ordinary/complex URL that is **not already owned by a first-class specialist semantic**.

The Source-Semantic Ownership Gate in Arena v0.3 must pass before any Challenger staging.

### WeChat Arena

WeChat content must be evaluated separately under its own specialist semantics:

```text
wechat.discovery
wechat.reader
```

General readers/crawlers such as `web_reader`, Crawl4AI, or other extraction tools may compete there only as explicit fallback/escalation candidates for the WeChat semantic. They must not be used to infer generic `complex-web.read` ownership from a WeChat-only case.

No WeChat Arena execution is authorized by this correction task.

## Evidence preservation

Do not delete or rewrite the original TASK-004 contestant receipts. They are primary execution evidence for what actually happened.

The review correction is a higher-level adjudication record that supersedes only the ownership conclusion, not the raw execution facts or teardown receipt.

## First-match cross-check

The first `github.semantic` Arena has now been rechecked under v0.3 and remains valid because its target objects were GitHub-native and both contestants competed inside the correct specialist semantic.

Durable review:

```text
reports/TASK-20260913-003-SOURCE-SEMANTIC-REVIEW.md
```

## Next task

The Human authorized resetting the generic complex-web exam. The active follow-up is:

```text
tasks/TASK-20260913-006-CAPABILITY-ARENA-COMPLEX-WEB-RETAKE.md
```

TASK-006 performs case qualification only. No Challenger staging is authorized until a correctly routed real ordinary URL with an observed native extraction gap is frozen and reviewed.
