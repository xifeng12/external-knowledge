# External Knowledge — Project Control

```yaml
project_control_ref: PROJECT-CONTROL.md
project_control_version: p0-practice-remediation-ready-2026-09-13
final_outcome: >-
  Evolve external-knowledge into a durable external-information capability layer
  that routes concrete information needs/source semantics to the best available
  retrieval path, diagnoses real runtime availability without conflating presence
  with capability, and evolves overlapping providers only from evidence.
scope_baseline_version: tasks/TASK-20260912-001-SEARCH-CAPABILITY-EVOLUTION.md
schedule_baseline_version: SCHEDULE_UNBASELINED
channel_roadmap_state: FROZEN_CURRENT_BASELINE
agent_operationalization_state: READY_FOR_P0_REMEDIATION_ACCEPTANCE
current_outcome: three_confirmed_practice_p0_items_implemented_in_repository_source
current_actual_state: READY_FOR_P0_REMEDIATION_ACCEPTANCE
current_work_class: RUNTIME_INTEGRATION_REMEDIATION
current_blocker: none
forecast_state: unbaselined
next_authorized_action: Human/Coordinator reviews TASK-019 implementation/report; no ZCode re-bind, PR merge, or further remediation is authorized yet
resume_point: TASK-019 latest implementation report amendment is 22a1c1a0b73475e262355a0c4d5b83722343b7a6 on task/20260913-019-p0-practice-remediation; this file is the current status authority and Issue #6 records the current branch head; ZCode installed copy remains pinned to 450fc67 until a later deployment decision
```

## Freeze decision — 2026-09-13

The Human explicitly stopped further channel expansion for the current roadmap slice.

Freeze semantics:

- preserve all accepted evidence and decisions already recorded in this repository;
- do not start Bilibili, V2EX, Weibo, Zhihu, Xiaohongshu, Xueqiu, Xiaoyuzhou, Douyin, RSS/Atom, or other new channel implementation merely because it appears in an assessment;
- do not reopen X search work;
- do not provision, bind, install, configure, promote, or merge merely to increase nominal channel coverage;
- keep the remaining channel assessments as future expansion options, not an active backlog;
- a future channel expansion begins only from a new explicit Human decision and one bounded source-semantic task.

This freeze changes channel-roadmap activity, not the validity of accepted evidence.

## Agent operationalization — current state

The Human separately authorized putting the **existing frozen capability baseline** into real ZCode Agent practice. This remains orthogonal to channel expansion.

TASK-018 authority:

```text
tasks/TASK-20260913-018-AGENT-RUNTIME-PILOT.md
branch: task/20260913-018-agent-runtime-pilot
pinned frozen capability baseline: 450fc67351bad8d38e99234a1b3276b127d663c2
accepted result head: d8bebf5a61f15991f0025382f408a3a0c3ed8207
```

TASK-018 was authored as read-only with respect to the Agent runtime and required STOP before binding. During execution, after ZCode was clarified as the intended target, the Human directly instructed the executor to bind the Skill. The pinned baseline was ultimately installed at the official ZCode user root:

```text
C:\Users\fengxi\.zcode\skills\external-knowledge\
```

The first `.agents\skills` target was superseded after a fresh-session non-discovery observation. No Codex binding was retained.

Acceptance classification recorded on Issue #5:

```text
TASK-018 outcome: ACCEPTED_WITH_AUTHORITY_DEVIATION
binding result: retained as intentional current runtime state
strict task-contract compliance: NOT PASSED
channel roadmap: FROZEN_CURRENT_BASELINE
formal behavioral acceptance: BEHAVIOR_INCONCLUSIVE
```

Reason for the deviation classification: the Human's runtime instruction made the ZCode binding intentional, but the durable task authority was not updated before executing a mutation that the task explicitly prohibited. Future mid-run supersession should update durable authority before the newly authorized mutation when that path is available.

The Human subsequently reported a successful fresh-session Skill discovery, a neutral real information task, and additional Doctor work. These observations are useful practice evidence and exposed concrete usability/adapter issues. They are not promoted to formal `BEHAVIOR_PASS` because no independently reviewable durable behavior receipt/tool trace was committed or attached to the Issue.

## Confirmed practice findings

Repository review after the practice run confirms:

1. **ZCode adapter path coupling** — `wechat.discovery/wechat-article-search` uses a Codex-specific `~/.codex/skills/.../search_wechat.js` local-script check inside the ZCode adapter. Without explicit runtime inventory overriding the local check, an equivalent ZCode-root installation cannot be discovered by that deterministic check and may be misclassified.
2. **Agent runtime inventory documentation gap** — `references/machine-diagnostics.md` shows `--agent-inventory` usage but does not document the inventory schema/status vocabulary/absence-authority fields. The actual semantics are distributed across `scripts/doctor.py` and `tests/fixtures/agent-inventory.example.json`.
3. **Inventory scaffold opportunity** — no scaffold/generator exists; operators currently construct runtime inventory JSON from the fixture/source. This is a usability improvement justified by observed operator cost, not a correctness defect by itself.
4. **`web_reader` representation gap** — `references/capability-map.md` records `web_reader` as a test-stage verified-URL fallback, while the ZCode adapter has no corresponding provider binding. Adding a binding requires provider/exposure evidence; the documentation/adapter mismatch is real, but promotion is not automatic.
5. **Doctor CLI ergonomics** — `--adapter` accepts a file path only and generic file-not-found handling gives no adapter discovery hint; no `--list-adapters`/id resolver exists.
6. **Doctor escalation hint** — the human-readable Doctor output does not suggest `--agent-inventory` when UNKNOWNs remain.

Not promoted from this single practice observation:

- expanding `source_semantic_profiles` merely because one general-web retrieval succeeded or one fallback was observed;
- restructuring/shortening `SKILL.md` solely because of its size when no routing failure has been attributed to that density;
- installing/fixing missing providers merely to improve diagnostic completeness.

## TASK-019 — P0 remediation result

The Human selected remediation path A on 2026-09-13.

```text
task: tasks/TASK-20260913-019-P0-PRACTICE-REMEDIATION.md
branch: task/20260913-019-p0-practice-remediation
baseline: be597313bc35eedb6b0be37f5b5d11f0535586e1
implementation report: reports/TASK-20260913-019-P0-PRACTICE-REMEDIATION.md
latest report amendment: 22a1c1a0b73475e262355a0c4d5b83722343b7a6
terminal state: READY_FOR_P0_REMEDIATION_ACCEPTANCE
```

Implemented scope:

```text
P0-1 ZCode WeChat local-script exposure/path modeling
  -> official ZCode + previously observed shared Codex candidate paths
  -> same independent local_script exposure class
  -> static presence still does not establish AVAILABLE

P0-2 normative references/agent-inventory.md
  -> provider-scoped schema/status/absence-authority semantics
  -> linked from machine diagnostics

P0-3 deterministic read-only scripts/inventory_scaffold.py
  -> UNKNOWN/non-authoritative defaults
  -> declared legal classes exposed only as guidance
  -> focused tests added
```

Focused validation recorded in the report: 8/8 new focused tests passed in the available isolated validation harness; new Python files compile and adapter JSON parses. The execution sandbox could not obtain a full GitHub checkout and the repository has no CI workflow, so the full pre-existing suite was not represented as executed.

The confirmed `web_reader` representation gap, Doctor CLI ergonomics, Doctor UNKNOWN hint, semantic-profile growth, SKILL.md restructuring, provider repair, and channel expansion remain outside TASK-019.

No deployment/re-binding of the installed ZCode copy occurred in TASK-019. Repository source and installed Skill therefore intentionally differ until a later deployment decision.

## Accepted state to preserve

- `general-web.search` remains the general discovery owner.
- `general-web.read` remains the ordinary known-URL reader.
- `docs.versioned` remains the versioned docs specialist.
- `github.semantic` remains accepted on `gh-cli` (`KEEP_INCUMBENT`).
- `precision.search` keeps Exa as the qualified precision challenger; Native Search remains default.
- `complex-web.read` retains the native-static / Crawl4AI dynamic test-stage split.
- WeChat minimum vertical remains accepted at test stage under its recorded evidence boundary.
- Mainland no-proxy remote retrieval remains demonstrated through the retained anonymous Exa hosted MCP evidence.

## X workstream — closed for this roadmap slice

Accepted terminal state:

```text
TASK-016 -> X_PROVIDER_ALTERNATIVE_REQUIRED
TASK-017 -> X_SEARCH_DEFERRED_BY_GOAL_INTEGRITY (0/2 Exa fixtures)
```

Preserve:

```text
x.account.timeline -> existing vpsmanage / XActions
x.post.read        -> existing vpsmanage / XActions
x.search           -> unresolved; deferred by Goal Integrity
```

Do not reopen XActions search/session/query-ID work or begin another X provider comparison unless a future decision-critical Human need explicitly reopens X.

## Frozen expansion surface

Reference assessment: `reports/CHINA-DOMESTIC-CHANNELS-ASSESSMENT-20260913.md`.

The previously evaluated candidates remain future expansion options only:

```text
Domestic: Bilibili, V2EX, Weibo, Zhihu, Xiaohongshu, Xueqiu, Xiaoyuzhou, Douyin
Cross-cutting/later: RSS/Atom
Deferred international: Reddit, YouTube, LinkedIn, Facebook, Instagram
```

These entries are not a backlog and create no obligation to implement every channel.

## Resume rule

The channel roadmap remains frozen.

Current stop state:

```text
READY_FOR_P0_REMEDIATION_ACCEPTANCE
```

The next Human/Coordinator action is review/acceptance of TASK-019 only. Do not deploy/re-bind the ZCode Skill, merge a PR/main, or begin the deferred P1 findings merely because implementation is complete.

If TASK-019 is accepted, deployment/re-binding of the updated repository source into `~/.zcode/skills/external-knowledge` is a separate explicit action. A later evidence-complete behavioral pilot also remains separately gated.

Future channel expansion remains separately gated and is not implied by remediation, deployment, or behavioral validation.
