# External Knowledge — Project Control

```yaml
project_control_ref: PROJECT-CONTROL.md
project_control_version: session-handoff-2026-09-13
final_outcome: >-
  Evolve external-knowledge into a durable external-information capability layer
  that routes concrete information needs/source semantics to the best available
  retrieval path, diagnoses real runtime availability without conflating presence
  with capability, and evolves overlapping providers only from evidence.
scope_baseline_version: tasks/TASK-20260912-001-SEARCH-CAPABILITY-EVOLUTION.md
schedule_baseline_version: SCHEDULE_UNBASELINED
current_outcome: expand_first_class_source_specialists_after_x_stop
current_actual_state: READY_FOR_NEXT_VERTICAL_SELECTION
current_work_class: GOVERNANCE
current_blocker: none
forecast_state: unbaselined
next_authorized_action: Human selects the next domestic P1 vertical; default Bilibili, lowest-risk alternative V2EX
resume_point: after TASK-20260913-017 closed the X workstream; before creating/authorizing the next vertical task
```

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

## Current vertical-selection authority

Reference: `reports/CHINA-DOMESTIC-CHANNELS-ASSESSMENT-20260913.md`.

Recommended order already accepted for decision-making:

```text
Default next vertical: Bilibili
Lowest-risk / fastest alternative: V2EX
Then: Weibo
Later session-heavy: Zhihu, Xiaohongshu
```

No Bilibili or V2EX execution task is authorized merely by this checkpoint. The next conversation should first read this file, Issue #2, the domestic-channel assessment, and the current branch/head, then return the current goal/state/gaps and wait for or apply the Human's vertical selection.

## Remaining known gaps

Decision-relevant gaps still visible from TASK-001 and the domestic-channel assessment include:

- Bilibili search/metadata/subtitle-transcript semantics;
- V2EX topic/reply/user/community semantics;
- Weibo discovery/read/trends;
- Zhihu Q&A/answer/article/comment semantics;
- Xiaohongshu discovery/read/comments;
- later/niche: RSS/Atom, Xueqiu, Xiaoyuzhou, selected video/social channels when justified.

Do not convert this list into a backlog that must all be implemented. Expand vertically only when the source semantic adds decision-relevant information not equivalently covered by general web routes.

## Resume rule

The next capable executor should not replay TASK-013 through TASK-017 or re-derive why X was stopped. Resume from the current product path:

```text
X workstream closed
-> choose next high-value source specialist
-> create one bounded minimum vertical
-> validate end-to-end evidence
-> only then decide whether deeper platform semantics are worth adding
```
