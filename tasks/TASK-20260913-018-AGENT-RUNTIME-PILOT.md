---
task_id: TASK-20260913-018
status: ready_for_read_only_runtime_inspection
target_repo: xifeng12/external-knowledge
target_ref: task/20260913-018-agent-runtime-pilot
project_control_ref: PROJECT-CONTROL.md
frozen_capability_baseline: 450fc67351bad8d38e99234a1b3276b127d663c2
result_path: reports/TASK-20260913-018-AGENT-RUNTIME-PILOT.md
isolated_worker_authorized: true
---

# Goal

Prepare the frozen `external-knowledge` capability baseline for one real Agent runtime pilot without expanding channel coverage.

This task answers one concrete question:

> On the current authorized Agent/Codex execution surface used for real repository engineering, what supported Skill loading/binding surface would make the frozen `external-knowledge` Skill discoverable, and is it already discoverable there?

The task is **read-only with respect to the Agent runtime/environment**. It may write only this repository's required durable result/status artifacts.

# Frozen baseline and scope boundary

The capability/channel roadmap remains frozen at:

```text
450fc67351bad8d38e99234a1b3276b127d663c2
FROZEN_CURRENT_BASELINE
```

The pilot must use that accepted capability baseline as the source under evaluation. This task does not reopen channel evolution, X search, provider competition, or Arena work.

Do not add or evaluate Bilibili, V2EX, Weibo, Zhihu, Xiaohongshu, Xueqiu, Xiaoyuzhou, Douyin, RSS/Atom, Reddit, YouTube, LinkedIn, Facebook, Instagram, or another new channel merely because it is a future expansion candidate.

# Required inspection

Inspect only the real, supported execution/configuration surfaces relevant to the current Agent/Codex runtime that performs repository engineering for the Human.

Establish, from current runtime/configuration/documentation evidence where available:

1. the actual Agent/Codex runtime/execution surface being inspected;
2. the supported Skill discovery/loading roots or registration mechanism applicable to that runtime;
3. whether `external-knowledge` is already discoverable by that runtime;
4. if it is not discoverable, the **single minimal binding change** that would make the pinned frozen baseline discoverable;
5. the exact file/path/config/registration target that change would affect;
6. whether that change would be a copy, link, registration/config edit, plugin/Skill install action, or another supported mechanism;
7. any real blocker that prevents a safe binding decision.

Prefer direct runtime/configuration evidence over inferred conventions. Inspect only supported/actually configured roots; do not scan arbitrary drives or speculate about inactive Agent products.

If several supported binding mechanisms are genuinely active, report only those that could materially change the next binding decision. Do not enumerate theoretical alternatives for completeness.

# Explicitly authorized

- read repository authority and the pinned baseline;
- inspect the current Agent/Codex runtime identity and supported Skill/configuration surfaces;
- inspect relevant Skill roots/config files/registration metadata read-only;
- run bounded read-only commands whose result can distinguish `already discoverable`, `binding required`, or `blocked/inconclusive`;
- create/update only the durable report/status artifacts required by this task in this repository;
- commit and push those repository artifacts to the task branch.

# Explicitly unauthorized

Do **not**:

- copy, symlink, install, register, enable, update, repair, or remove `external-knowledge` in the Agent runtime;
- edit Agent/Codex configuration, global/project `AGENTS.md`, MCP configuration, plugin settings, Skill roots, PATH, shell profiles, proxy/TLS/network settings, browser state, credentials, cookies, or login/session state;
- install or configure any provider;
- run provider benchmarks, channel probes, Doctor sweeps, or broad Skill inventories unless a narrowly scoped observation is necessary to identify the actual binding surface;
- modify the frozen capability map merely to prepare the pilot;
- merge Draft PR #3, this task branch, or `main`;
- start behavioral routing acceptance in this task.

# Acceptance criteria

The durable report must make the next authorization mechanically clear and include:

```text
inspected Agent/runtime identity
supported binding/discovery surface actually evidenced
current external-knowledge discoverability: YES | NO | INCONCLUSIVE
pinned source baseline: 450fc67351bad8d38e99234a1b3276b127d663c2
if NO: one minimal binding action and exact target
if YES: exact evidence showing current discoverability
if INCONCLUSIVE: exact missing evidence/blocker
runtime/environment mutation attempted: false
channel roadmap reopened: false
```

Evidence must be sufficient for a later reviewer to distinguish the outcome without trusting the Agent's prose alone. Use direct path/config/runtime observations where available; do not commit secrets or machine-sensitive raw dumps.

# Outcome classification

Use exactly one terminal classification:

## `READY_FOR_AGENT_BIND_APPROVAL`

Use when `external-knowledge` is not yet discoverable and one concrete, supported, minimal binding action has been identified. No binding has been executed.

## `READY_FOR_AGENT_BEHAVIOR_PILOT`

Use when the frozen `external-knowledge` baseline is already discoverable by the intended Agent runtime with direct evidence, so no binding mutation is required before a neutral real-task behavior pilot.

## `AGENT_BINDING_INCONCLUSIVE`

Use when current authority/evidence cannot identify the supported binding surface or discoverability strongly enough to authorize a specific binding action. Record only the exact unresolved evidence needed; do not broaden inspection merely for reassurance.

## `AGENT_BINDING_BLOCKED`

Use when a concrete supported path is identified but a real blocker prevents a safe next authorization.

# Behavioral pilot boundary

Behavioral validation is a **later task**.

When later authorized, it must follow the `codex-control` observable-agent-behavior method:

- use an ordinary real information task as the neutral stimulus;
- do not tell the tested Agent to use `external-knowledge` or reveal the expected route;
- observe independently verifiable tool/action/artifact evidence;
- classify `BEHAVIOR_PASS`, `BEHAVIOR_FAIL`, `BEHAVIOR_INCONCLUSIVE`, or `NOT_EXERCISED`;
- do not manufacture channel/provider probes merely to fill coverage.

This task stops before that phase.

# Required durable output

Write and push:

```text
reports/TASK-20260913-018-AGENT-RUNTIME-PILOT.md
```

The report should be concise and evidence-oriented. It must record the branch head used for inspection and any repository head advancement before consequential writes.

# Stop condition

Stop immediately after the report is pushed and one terminal classification above is reached.

Do not perform the binding action in the same run, even if it appears trivial.
