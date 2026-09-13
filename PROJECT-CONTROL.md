# External Knowledge — Project Control

```yaml
project_control_ref: PROJECT-CONTROL.md
project_control_version: agent-runtime-pilot-2026-09-13
final_outcome: >-
  Evolve external-knowledge into a durable external-information capability layer
  that routes concrete information needs/source semantics to the best available
  retrieval path, diagnoses real runtime availability without conflating presence
  with capability, and evolves overlapping providers only from evidence.
scope_baseline_version: tasks/TASK-20260912-001-SEARCH-CAPABILITY-EVOLUTION.md
schedule_baseline_version: SCHEDULE_UNBASELINED
channel_roadmap_state: FROZEN_CURRENT_BASELINE
agent_operationalization_state: READY_FOR_AGENT_RUNTIME_INSPECTION
current_outcome: validate_the_frozen_capability_baseline_on_one_real_agent_runtime
current_actual_state: READY_FOR_AGENT_RUNTIME_INSPECTION
current_work_class: RUNTIME_INTEGRATION_PILOT
current_blocker: none
forecast_state: unbaselined
next_authorized_action: execute TASK-20260913-018 read-only Agent runtime/binding-surface inspection and stop before mutation
resume_point: frozen capability baseline preserved; before any Agent Skill binding mutation or behavioral routing pilot
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

## Agent operationalization — active pilot

The Human subsequently authorized a separate, orthogonal objective: put the **existing frozen capability baseline** into real Agent practice and use real work to validate it.

This does **not** reopen the channel roadmap.

Current task authority:

```text
tasks/TASK-20260913-018-AGENT-RUNTIME-PILOT.md
branch: task/20260913-018-agent-runtime-pilot
pinned frozen capability baseline: 450fc67351bad8d38e99234a1b3276b127d663c2
```

TASK-018 is intentionally read-only with respect to the Agent runtime. It may identify the actual supported Skill loading/binding surface and whether `external-knowledge` is already discoverable, but it may not perform the binding/configuration change.

Allowed terminal states for TASK-018:

```text
READY_FOR_AGENT_BIND_APPROVAL
READY_FOR_AGENT_BEHAVIOR_PILOT
AGENT_BINDING_INCONCLUSIVE
AGENT_BINDING_BLOCKED
```

If binding is required, the exact minimal mutation must be presented for explicit Human approval before execution.

If the Skill is already discoverable, the next step is a separate neutral real-task behavioral pilot. That later behavioral task must not tell the tested Agent to use `external-knowledge`; it must judge actual routing/tool evidence rather than Agent self-report.

## Accepted state to preserve

- `general-web.search` remains the general discovery owner.
- `general-web.read` remains the ordinary known-URL reader.
- `docs.versioned` remains the versioned docs specialist.
- `github.semantic` remains accepted on `gh-cli` (`KEEP_INCUMBENT`).
- `precision.search` keeps Exa as the qualified precision challenger; Native Search remains default.
- `complex-web.read` retains the native-static / Crawl4AI dynamic test-stage split.
- WeChat minimum vertical is available at test stage: `wechat.discovery` remains `LIMITED_OBSERVED`; verified canonical URLs can be read through the existing reader route.
- Mainland no-proxy remote retrieval is demonstrated: anonymous Exa hosted MCP can discover and remotely read at least some foreign sources that are locally transport-blocked.

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

The previously evaluated candidates are retained only as future expansion options.

### Domestic candidates

```text
Bilibili   -> search / metadata / comments-danmaku / subtitle-transcript semantics
V2EX       -> topic / reply / user / node-community semantics
Weibo      -> discovery / read / trends
Zhihu      -> question / answer / article / comment semantics
Xiaohongshu -> discovery / read / comments
Xueqiu     -> market / community semantics
Xiaoyuzhou -> discovery / podcast transcript semantics
Douyin     -> future read-only discovery/read path only after such a path is directly verified
```

The assessment's former decision order is preserved as context, not active authorization:

```text
Bilibili
V2EX
Weibo
Zhihu
Xiaohongshu
Xueqiu
Xiaoyuzhou
Douyin
```

### Cross-cutting / later candidates

```text
RSS / Atom
Reddit
YouTube
LinkedIn
Facebook
Instagram
selected additional video/social/domain specialists when justified by a real workload
```

These entries are not a backlog and create no obligation to implement every channel. A future specialist is justified only when its source semantics add decision-relevant information that general routes cannot represent equivalently.

## Resume rule

The channel roadmap remains frozen. Do not start a new source vertical from this pilot.

For the active Agent operationalization path, resume only through TASK-018:

```text
FROZEN_CURRENT_BASELINE
+
READY_FOR_AGENT_RUNTIME_INSPECTION
-> inspect one real supported Agent runtime read-only
-> identify current Skill discoverability / exact minimal binding surface
-> STOP at the TASK-018 terminal state
```

After TASK-018, do not silently bind the Skill. A required binding mutation needs explicit Human approval.

A later behavioral pilot, if authorized, should use ordinary real tasks and independently observable routing evidence. Only a concrete practice failure may justify modifying the frozen Skill/routing mechanism.

Future channel expansion remains separately gated:

```text
Human identifies a real information/source-semantic need
-> select one candidate only if general routes are not equivalent
-> create/authorize one bounded minimum vertical task
-> validate end-to-end evidence
-> return to a controlled stop state
```
