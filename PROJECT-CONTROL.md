# External Knowledge — Project Control

```yaml
project_control_ref: PROJECT-CONTROL.md
project_control_version: p0-practice-remediation-2026-09-13
final_outcome: >-
  Evolve external-knowledge into a durable external-information capability layer
  that routes concrete information needs/source semantics to the best available
  retrieval path, diagnoses real runtime availability without conflating presence
  with capability, and evolves overlapping providers only from evidence.
scope_baseline_version: tasks/TASK-20260912-001-SEARCH-CAPABILITY-EVOLUTION.md
schedule_baseline_version: SCHEDULE_UNBASELINED
channel_roadmap_state: FROZEN_CURRENT_BASELINE
agent_operationalization_state: P0_REMEDIATION_IN_PROGRESS
current_outcome: remediate_three_confirmed_practice_findings_without_expanding_scope
current_actual_state: P0_REMEDIATION_IN_PROGRESS
current_work_class: RUNTIME_INTEGRATION_REMEDIATION
current_blocker: none
forecast_state: unbaselined
next_authorized_action: execute TASK-20260913-019 only; stop at READY_FOR_P0_REMEDIATION_ACCEPTANCE
resume_point: ZCode binding remains at C:\Users\fengxi\.zcode\skills\external-knowledge\ from pinned baseline 450fc67; repository remediation proceeds on task/20260913-019-p0-practice-remediation and must not re-bind during implementation
```

## Channel freeze remains authoritative

The Human stopped further channel expansion for the current roadmap slice. Preserve all accepted evidence and current capability decisions. Do not start Bilibili, V2EX, Weibo, Zhihu, Xiaohongshu, Xueqiu, Xiaoyuzhou, Douyin, RSS/Atom, Reddit, YouTube, LinkedIn, Facebook, Instagram, or another new vertical from this remediation.

Future channels remain options, not a backlog. X search remains closed unless a future decision-critical Human need explicitly reopens it.

## Agent operationalization baseline

TASK-018 established the current ZCode binding:

```text
C:\Users\fengxi\.zcode\skills\external-knowledge\
source baseline: 450fc67351bad8d38e99234a1b3276b127d663c2
TASK-018 accepted result: d8bebf5a61f15991f0025382f408a3a0c3ed8207
acceptance: ACCEPTED_WITH_AUTHORITY_DEVIATION
formal behavior status: BEHAVIOR_INCONCLUSIVE
```

The binding is retained as intentional current runtime state. Do not repeat TASK-018 discovery/binding work for reassurance.

## Confirmed practice findings

Repository review after the first real ZCode practice run confirmed:

1. **ZCode adapter path coupling** — `wechat.discovery/wechat-article-search` uses only a Codex-root deterministic local-script path even though the current official ZCode user Skill root is `~/.zcode/skills`; the adapter must represent the actually evidenced candidate locations without turning static presence into `AVAILABLE`.
2. **Agent runtime inventory documentation gap** — `references/machine-diagnostics.md` exposes `--agent-inventory` but the schema/status/absence-authority semantics live mainly in `scripts/doctor.py` and `tests/fixtures/agent-inventory.example.json`.
3. **Inventory scaffold opportunity** — no deterministic read-only scaffold exists; operators currently construct provider-scoped runtime inventory JSON from fixtures/source.
4. `web_reader` representation gap, Doctor adapter-id ergonomics, and Doctor UNKNOWN guidance are real but remain outside TASK-019.
5. Expanding `source_semantic_profiles`, shortening `SKILL.md`, or installing/fixing missing providers is not justified by the current evidence and remains frozen.

## Active remediation authority

Human authorization on 2026-09-13 selected remediation path A.

```text
task: tasks/TASK-20260913-019-P0-PRACTICE-REMEDIATION.md
branch: task/20260913-019-p0-practice-remediation
baseline: be597313bc35eedb6b0be37f5b5d11f0535586e1
required report: reports/TASK-20260913-019-P0-PRACTICE-REMEDIATION.md
terminal state: READY_FOR_P0_REMEDIATION_ACCEPTANCE
```

TASK-019 is limited to:

```text
P0-1 ZCode WeChat local-script exposure/path modeling
P0-2 normative references/agent-inventory.md
P0-3 deterministic read-only scripts/inventory_scaffold.py + focused tests
```

No deployment/re-binding of the installed ZCode copy is authorized in TASK-019. Repository source first, acceptance second, deployment decision later.

## Accepted state to preserve

- `general-web.search` remains the general discovery owner.
- `general-web.read` remains the ordinary known-URL reader.
- `docs.versioned` remains the versioned docs specialist.
- `github.semantic` remains accepted on `gh-cli` (`KEEP_INCUMBENT`).
- `precision.search` keeps Exa as the qualified precision challenger; Native Search remains default.
- `complex-web.read` retains the native-static / Crawl4AI dynamic test-stage split.
- WeChat minimum vertical remains accepted at test stage under its recorded evidence boundary.
- Mainland no-proxy remote retrieval remains demonstrated through the retained anonymous Exa hosted MCP evidence.

## X workstream — closed

```text
TASK-016 -> X_PROVIDER_ALTERNATIVE_REQUIRED
TASK-017 -> X_SEARCH_DEFERRED_BY_GOAL_INTEGRITY (0/2 Exa fixtures)

x.account.timeline -> existing vpsmanage / XActions
x.post.read        -> existing vpsmanage / XActions
x.search           -> unresolved; deferred by Goal Integrity
```

Do not replay TASK-013 through TASK-017 or reopen XActions search/session/query-ID work without a future decision-critical Human need.

## Resume rule

While TASK-019 is active:

```text
confirmed practice defect/usability evidence
-> implement only the three authorized P0 items
-> run the affected diagnostic/scaffold tests
-> write durable implementation report
-> synchronize project/Issue status
-> STOP at READY_FOR_P0_REMEDIATION_ACCEPTANCE
```

After acceptance, any ZCode re-binding/deployment is a separate authorization. Do not modify `~/.zcode/skills/external-knowledge` from this repository remediation task.
