---
task_id: TASK-20260913-019
status: ready
target_repo: xifeng12/external-knowledge
target_ref: task/20260913-019-p0-practice-remediation
project_control_ref: PROJECT-CONTROL.md
parent_practice_result: TASK-20260913-018
baseline_sha: be597313bc35eedb6b0be37f5b5d11f0535586e1
result_path: reports/TASK-20260913-019-P0-PRACTICE-REMEDIATION.md
isolated_worker_authorized: true
---

# Goal

Repair only the three P0 issues justified by the first real ZCode practice run, without reopening channel expansion or broadening the diagnostic model.

# Authorized changes

## P0-1 — ZCode WeChat local-script exposure modeling

Correct the ZCode adapter so its deterministic local-script checks can represent both actually evidenced locations relevant to ZCode execution:

- the official ZCode user Skill root used by the current binding: `~/.zcode/skills/...`;
- the previously observed shared/legacy Codex-root provider location: `~/.codex/skills/...`.

Requirements:

- preserve `local_script` as the independent execution class;
- do not promote static path presence to provider `AVAILABLE`;
- do not let one absent candidate path cause `MISSING_CONFIRMED` when an equivalent declared path is present;
- `MISSING_CONFIRMED` is allowed only when the declared `local_script` exposure class is authoritatively absent across all adapter-declared candidate paths;
- document why both locations exist; do not replace one hard-coded product path with another undocumented guess.

If the current Doctor merge semantics cannot express this correctly, make only the smallest Doctor change necessary and add regression coverage.

## P0-2 — Agent runtime inventory reference

Add `references/agent-inventory.md` as the normative operator-facing reference for Doctor `--agent-inventory` input.

It must document at minimum:

- `inventory_version` currently supported by repository examples;
- top-level `runtime`, `inventory_scope`, and `capabilities` structure;
- provider-scoped entries;
- valid operational statuses;
- `evidence_kind`, `scope`, `authoritative_for_absence`, `exposure_class`, `carrier_class`, `absence_covers_exposure_classes`, and `note` semantics;
- the rule that `MISSING_CONFIRMED` without authoritative absence is downgraded;
- the distinction between carrier/static presence and independent runtime exposure;
- one minimal valid example;
- a link from `references/machine-diagnostics.md`.

Do not invent a broader versioning policy or generic schema framework.

## P0-3 — Read-only inventory scaffold

Add `scripts/inventory_scaffold.py`.

Behavior:

- input: one adapter JSON path;
- output: deterministic JSON scaffold derived only from declared adapter capabilities/providers/exposure contracts;
- include provider identifiers and legal exposure classes so an operator can fill observed runtime evidence;
- default every provider to `UNKNOWN`;
- default `authoritative_for_absence` to `false`;
- do not perform runtime probes, filesystem scans, network access, environment-variable reads, provider execution, or secret access;
- do not claim `AVAILABLE`/`MISSING_CONFIRMED` automatically;
- support stdout and optional `--output`; `--pretty` may format output but must not change semantics.

Add focused automated tests for deterministic output and non-promotion defaults.

# Explicitly out of scope

Do not:

- add or model new channels/providers;
- add `web_reader` to the adapter;
- change `source_semantic_profiles` except if strictly necessary to keep an existing invariant (not expected);
- add adapter-id resolution, `--list-adapters`, or Doctor UNKNOWN hints;
- refactor/shorten `SKILL.md`;
- repair Context7, Exa, WeChat runtime packages, credentials, or environment state;
- modify the installed `~/.zcode/skills/external-knowledge` copy in this task;
- merge Draft PR #3, this task branch, or `main`.

# Acceptance criteria

1. ZCode adapter no longer structurally treats the Codex root as the only deterministic local-script location for `wechat-article-search`.
2. Regression tests prove:
   - official ZCode-root present + Codex-root absent does not yield provider `MISSING_CONFIRMED` from deterministic local checks alone;
   - both declared candidate paths absent can yield `MISSING_CONFIRMED` for the `local_script` class;
   - static path presence alone is not promoted to `AVAILABLE`.
3. `references/agent-inventory.md` contains the documented fields/status semantics above and `machine-diagnostics.md` links to it.
4. `inventory_scaffold.py` produces a deterministic provider-scoped inventory skeleton with `UNKNOWN`, `authoritative_for_absence=false`, and declared legal exposure classes; it is read-only and probe-free.
5. Focused tests for all changed behavior pass. Run the existing diagnostic-related test surface affected by the changes; do not broaden unrelated test scope.
6. Write the required durable implementation report with exact tests/results and final head.
7. Channel roadmap remains `FROZEN_CURRENT_BASELINE`.

# Stop condition

Stop after implementation, focused validation, report, and project-control/Issue status synchronization are pushed to this task branch.

Terminal state:

```text
READY_FOR_P0_REMEDIATION_ACCEPTANCE
```

Do not deploy/re-bind the updated Skill to ZCode in the same task.
