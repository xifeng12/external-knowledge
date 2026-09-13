---
task_id: TASK-20260913-018
date: 2026-09-13
inspected_head: 2c184a1a3e97bc41464a458477b44899a37a5065 (origin/task/20260913-018-agent-runtime-pilot at inspection time)
pinned_frozen_capability_baseline: 450fc67351bad8d38e99234a1b3276b127d663c2
current_external_knowledge_discoverability: NO at inspection; binding executed mid-run under direct Human instruction
terminal_state: READY_FOR_AGENT_BEHAVIOR_PILOT
runtime_environment_mutation_performed: true (documented deviation, see "Mid-run Human authorization")
channel_roadmap_reopened: false
---

# TASK-20260913-018 — Agent runtime pilot / binding-surface inspection

## Inspected runtime identity

```text
runtime    ZCode CLI agent session on the Windows host (win32 10.0.26200 x64, Git Bash shell)
role       the live surface through which this repository's engineering tasks are executed
scope      the session executing this task; consistent with the runtime scope recorded in
           reports/TASK-20260912-001-MACHINE-DIAGNOSTIC.md ("the live ZCode CLI session ... through which this repository's engineering is performed")
```

Codex surfaces exist on the same machine (`~/.codex/` is configured and active, with its own
`~/.codex/skills/` root and a Skills-aware global `AGENTS.md`). Per the Human's mid-run instruction
recorded below, Codex was **out of scope** for binding: no Codex configuration, skill root, or
session state was read beyond two bounded exclusion checks, and **no Codex mutation occurred**.

## Supported Skill discovery/binding surface actually evidenced

Direct evidence from the live session's skill manifest (the runtime enumerates its Skill surface
at session start):

1. `C:\Users\fengxi\.agents\skills\` — user-level Skill root. The session manifest loads
   `agently-mail` from `C:\Users\fengxi\.agents\skills\agently-mail\SKILL.md`. This root is
   actively scanned by the inspected runtime.
2. `C:\Users\fengxi\.zcode\cli\plugins\cache\**` — plugin-provided skills (official plugins and
   `local-plugins`). Registration runs through plugin installation, which is heavier than a
   directory placement and not the minimal mechanism.
3. `C:\Users\fengxi\.agents\.skill-lock.json` — version 3 lock file tracking installer-sourced
   skills (single entry: `agently-mail`, `sourceType: well-known`, `sourceUrl: agent.qq.com`).
   The lock records installer bookkeeping; discovery of a manually placed directory is expected
   to be by root scan, to be confirmed at next session start (see Open caveat).

Bounded read-only exclusions checked (no existing registration found):

- `~/.agents/skills/` contained only `agently-mail` before this task;
- global `~/.codex/AGENTS.md` references Skills generically but not `external-knowledge`;
- no `AGENTS.md` at repo root or workspace root; no `.agents/` directory in the repo.

## Discoverability determination

`current external-knowledge discoverability: NO`

The frozen baseline repo **is already a complete Agent Skill package** — `SKILL.md` with valid
frontmatter (`name: external-knowledge`, routing description) at the repository root of
`450fc67351bad8d38e99234a1b3276b127d663c2` (101 tracked files, 740K as an archive). It was simply
not present in any root the inspected runtime scans. The live session manifest (the authoritative
discovery result for this runtime) contained no `external-knowledge` entry, and no registration
reference to it existed anywhere checked.

## Mid-run Human authorization (deviation from the stop-before-mutation default)

After inspection identified the binding surface, the Human issued a direct instruction
(quoting verbatim):

```text
停止，我什么说要给codex安装，我要的是给zcode安装
```

This is explicit Human authorization to bind the frozen baseline into the ZCode Skill surface.
It supersedes the Issue's stop-before-mutation default for this run. The binding below was
executed as exactly one minimal mutation — a plain directory copy of the pinned baseline — with
no installer/lock/config edits, no Codex mutation, and no other runtime change.

## Binding action executed

```text
mechanism   plain copy (git archive of the pinned commit, extracted verbatim)
source      450fc67351bad8d38e99234a1b3276b127d663c2 (git archive; sha256
            9ba78eac7ff645242d9e39f657c28596fd778fc18310609ca75fb56e151bc61f)
target      C:\Users\fengxi\.agents\skills\external-knowledge\
verified    101 files extracted = 101 tracked files at the pinned commit;
            SKILL.md frontmatter intact (`name: external-knowledge`);
            top-level layout matches the baseline tree exactly
not done    no .skill-lock.json edit, no symlink, no AGENTS.md/MCP/config edit, no Codex change
```

## Acceptance block

```text
inspected Agent/runtime identity:                ZCode CLI session, win32 host
supported binding/discovery surface evidenced:   C:\Users\fengxi\.agents\skills\ (user root, scan-based)
                                                 + plugin cache (plugin-install path, not minimal)
current external-knowledge discoverability:      NO at inspection -> bound mid-run per Human instruction
pinned source baseline:                          450fc67351bad8d38e99234a1b3276b127d663c2
minimal binding action and exact target:         copy pinned baseline to
                                                 C:\Users\fengxi\.agents\skills\external-knowledge\ (DONE)
runtime/environment mutation attempted:          true — one binding copy, under direct Human
                                                 instruction (deviation from the Issue's read-only
                                                 default, documented above); template value "false"
                                                 applies only to the inspection phase that preceded it
channel roadmap reopened:                        false
```

## Terminal state

```text
READY_FOR_AGENT_BEHAVIOR_PILOT
```

The binding gate that TASK-018 was designed to resolve has been resolved and executed under
direct Human instruction. The next step is a separate, neutral real-task behavioral pilot.

## Open caveat for the next run

Skills are enumerated by the runtime at session start; this session cannot re-enumerate its own
manifest. Therefore the first post-binding session must confirm `external-knowledge` appears in
the Skill manifest before the behavioral pilot begins. If it does not appear, the unresolved
question is the root's scan-vs-lock semantics (`~/.agents/.skill-lock.json` v3) — the identified
fallback is registering through that lock's installer semantics. Do not re-copy or duplicate the
Skill folder while troubleshooting.

The behavioral pilot, when separately authorized, must follow the `codex-control`
observable-agent-behavior method defined in the task contract: ordinary real task, no hint of the
expected route, independently verifiable tool/action/artifact evidence, classification into
`BEHAVIOR_PASS` / `BEHAVIOR_FAIL` / `BEHAVIOR_INCONCLUSIVE` / `NOT_EXERCISED`.

## Repository head advancement

Inspection and binding verification were performed at head `2c184a1`. This report and the
synchronized `PROJECT-CONTROL.md` state are the repository advancement produced by this task;
no other repo content was modified, and `main` and Draft PR #3 were not touched.
