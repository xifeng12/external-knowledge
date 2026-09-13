# External Knowledge — Project Control

```yaml
project_control_ref: PROJECT-CONTROL.md
project_control_version: frozen-baseline-2026-09-13
final_outcome: >-
  Evolve external-knowledge into a durable external-information capability layer
  that routes concrete information needs/source semantics to the best available
  retrieval path, diagnoses real runtime availability without conflating presence
  with capability, and evolves overlapping providers only from evidence.
scope_baseline_version: tasks/TASK-20260912-001-SEARCH-CAPABILITY-EVOLUTION.md
schedule_baseline_version: SCHEDULE_UNBASELINED
current_outcome: preserve_current_capability_baseline_and_defer_expansion
current_actual_state: FROZEN_CURRENT_BASELINE
current_work_class: GOVERNANCE
current_blocker: none
forecast_state: unbaselined
next_authorized_action: none while frozen; future expansion requires an explicit Human reopen/selection
resume_point: from this frozen baseline; do not replay the X workstream or start a new vertical unless explicitly reopened
```

## Freeze decision — 2026-09-13

The Human explicitly stopped further channel expansion for the current roadmap slice.

Freeze semantics:

- preserve all accepted evidence and decisions already recorded in this repository;
- do not start Bilibili, V2EX, Weibo, Zhihu, Xiaohongshu, Xueqiu, Xiaoyuzhou, Douyin, RSS/Atom, or other new channel implementation merely because it appears in an assessment;
- do not reopen X search work;
- do not provision, bind, install, configure, promote, or merge merely to increase nominal channel coverage;
- keep the remaining channel assessments as future expansion options, not an active backlog;
- a future expansion begins only from a new explicit Human decision and one bounded source-semantic task.

This freeze changes roadmap activity, not the validity of accepted evidence.

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

While frozen, the correct action is STOP.

A future capable executor should first read this file, Issue #2, the relevant retained assessment/evidence, and the then-current branch/head. It must preserve settled evidence and must not replay prior investigations solely to regain confidence.

Only an explicit future Human decision may advance the roadmap:

```text
FROZEN_CURRENT_BASELINE
-> Human identifies a real information/source-semantic need
-> select one candidate only if general routes are not equivalent
-> create/authorize one bounded minimum vertical task
-> validate end-to-end evidence
-> decide whether deeper platform semantics are worth adding
-> return to a controlled stop state
```
