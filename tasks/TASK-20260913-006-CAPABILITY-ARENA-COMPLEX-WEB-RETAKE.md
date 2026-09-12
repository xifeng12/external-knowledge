---
task_id: TASK-20260913-006
status: ready_for_complex_web_case_decision
parent_task: TASK-20260912-001
supersedes_exam: TASK-20260912-004
target_repo: xifeng12/external-knowledge
implementation_branch: task/20260912-001-v04-capability-diagnostics
arena_contract: references/capability-arena.md
arena_version: v0.3
capability: complex-web.read
defender: runtime-native.webfetch
challenger: unclecode/crawl4ai
challenger_staging_authorized: false
persistent_provisioning_authorized: false
routing_change_authorized: false
pr_merge_authorized: false
---

# TASK-20260913-006 — Corrected Complex Web Arena / Case Qualification

## Goal

Reset the generic `complex-web.read` exam after TASK-004 was invalidated by the Source-Semantic Ownership Gate.

The intended future match remains:

```text
capability: complex-web.read
Defender: runtime-native.webfetch
Challenger: unclecode/crawl4ai
```

But no Challenger staging or match execution is authorized until a correctly routed real case is selected and frozen.

## First-match precedent

TASK-003 was reviewed under Arena v0.3 and remains valid because its exam objects were GitHub-native and therefore correctly routed to `github.semantic`.

See:

```text
reports/TASK-20260913-003-SOURCE-SEMANTIC-REVIEW.md
```

## Phase A — Source-Semantic Qualification

Select exactly one real candidate target from accepted project evidence or an actual current user/workload URL.

The candidate MUST satisfy all of:

```text
known ordinary URL
no first-class specialist owner in source-ownership/capability-map
directly relevant to a real information need or retained real workload
safe/read-only to access
ordinary/native read path can be attempted without mutation
```

Explicitly disallowed as the generic exam target:

```text
GitHub PR/issue/commit/repository/history
canonical WeChat article
WeChat discovery result
versioned library/framework/SDK/API documentation
any source that repository authority already assigns to another specialist semantic
synthetic/demo/test pages created or selected merely because they are crawler-friendly or crawler-hostile
```

Do not choose a target because it is famous for anti-bot behavior. The target must first be a real information task; complexity is discovered from the read attempt, not manufactured as the reason for selection.

## Phase B — Native Gap Qualification

Before any Crawl4AI staging, attempt the candidate through the current ordinary/native read path.

A `complex-web.read` Arena is justified only if this read exposes a concrete extraction gap, for example:

```text
main body materially incomplete
required rendered/dynamic content missing
critical table/list/section not extracted
page shell returned without decision-relevant content
content structure materially destroyed such that the user goal cannot be satisfied
read is blocked or fails while the target itself remains legitimately reachable
```

The following do NOT by themselves qualify:

```text
page looks complex in a browser
site uses JavaScript
provider has fewer features on paper
we want to test Crawl4AI
minor formatting differences that do not affect the information goal
```

A content-level failure is not automatically a retryable transient error. Retry only for a concrete transport/tool/runtime transient under Arena rules.

## Case freeze receipt

If a valid case is found, write a small durable qualification receipt before any staging:

```text
evidence/arena/<future-match-id>/case.json
```

It must record:

```text
exact URL/source identity
real workload/provenance
why no specialist semantic owns it
native read attempt/result
specific extraction gap
minimum success criteria for the future match
whether any retry occurred and why
```

Do not include unnecessary copyrighted body text.

## Stop states

If no valid case exists in current accepted evidence/workload:

```text
READY_FOR_COMPLEX_WEB_CASE_DECISION
```

If a valid case is selected and frozen:

```text
READY_FOR_COMPLEX_WEB_MATCH_AUTHORIZATION
```

Stop there.

Do not stage Crawl4AI, download a browser, install Python packages, change proxy/TLS state, or execute the head-to-head match in this task.

## Future match authorization

Only after the Human reviews the frozen case may a follow-up task authorize ephemeral Crawl4AI staging and the actual match.

That follow-up must retain Arena v0.3 lifecycle rules:

```text
baseline
provenance
Provision Plan
Rollback Plan
Promotion Plan
Teardown Plan
CLEAN_VERIFIED / CLEAN_WITH_RESIDUE
```

A future result remains scoped to the selected real case; one case cannot establish universal crawler superiority.
