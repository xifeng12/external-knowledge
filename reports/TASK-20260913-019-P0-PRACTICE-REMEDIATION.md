---
task_id: TASK-20260913-019
date: 2026-09-13
baseline_sha: be597313bc35eedb6b0be37f5b5d11f0535586e1
implementation_head_before_report: 39f674ce4502dd89dc943e9d69297a334cf04966
terminal_state: READY_FOR_P0_REMEDIATION_ACCEPTANCE
channel_roadmap_state: FROZEN_CURRENT_BASELINE
zcode_runtime_rebound: false
---

# TASK-20260913-019 — P0 practice remediation result

## Status

`DONE` — the three authorized P0 items were implemented in repository source. No ZCode deployment/re-binding was performed.

## Authority

```text
task: tasks/TASK-20260913-019-P0-PRACTICE-REMEDIATION.md
branch: task/20260913-019-p0-practice-remediation
baseline: be597313bc35eedb6b0be37f5b5d11f0535586e1
implementation head before this report: 39f674ce4502dd89dc943e9d69297a334cf04966
issue: #6
```

The Human selected remediation path A after TASK-018 practice findings. Channel expansion remained frozen throughout.

## Changed

### P0-1 — ZCode WeChat local-script exposure modeling

Updated `adapters/zcode-v0.3-beta.1.json` for `wechat.discovery/wechat-article-search`.

The provider still has one independent legal exposure class:

```text
local_script
```

Its deterministic candidate paths now represent both locations supported by retained evidence:

```text
~/.zcode/skills/wechat-article-search/scripts/search_wechat.js
~/.codex/skills/wechat-article-search/scripts/search_wechat.js
```

Both checks describe candidate carriers for the same `local_script` exposure class. Existing Doctor merge semantics are sufficient:

- one declared path PRESENT + the other ABSENT -> provider remains `UNKNOWN` from static evidence; presence prevents false missing confirmation but does not establish `AVAILABLE`;
- both declared paths authoritatively ABSENT -> the `local_script` class is covered and the provider may become `MISSING_CONFIRMED` when no stronger runtime inventory conflicts;
- no Doctor core change was needed.

The adapter notes/binding scope now explain why both roots are represented instead of silently replacing one product-specific path with another.

### P0-2 — Agent runtime inventory reference

Added `references/agent-inventory.md` and linked it from `references/machine-diagnostics.md`.

The reference documents:

- current repository inventory version (`4`);
- top-level and provider-scoped structure;
- valid operational statuses;
- `evidence_kind`, `scope`, `authoritative_for_absence`, `exposure_class`, `carrier_class`, `absence_covers_exposure_classes`, and `note`;
- downgrade behavior for non-authoritative `MISSING_CONFIRMED` claims;
- carrier/static presence versus independent runtime exposure;
- one minimal valid inventory example;
- the new scaffold workflow.

The document explicitly states that Doctor currently consumes provider fields rather than enforcing `inventory_version` as a hard schema gate.

### P0-3 — Read-only inventory scaffold

Added `scripts/inventory_scaffold.py`.

The scaffold:

- reads exactly one adapter JSON;
- derives capability/provider identifiers and declared legal exposure classes;
- emits `inventory_version: 4`;
- initializes every provider to `status: UNKNOWN`;
- initializes `authoritative_for_absence: false`;
- leaves `absence_covers_exposure_classes` empty;
- exposes declared legal classes only through `declared_legal_exposure_classes` operator guidance;
- performs no runtime, filesystem scan, environment, network, provider, credential, or registration probe;
- supports stdout plus optional `--output` and `--pretty`.

The scaffold therefore cannot manufacture `AVAILABLE` or `MISSING_CONFIRMED` evidence.

## Tests

Added:

```text
tests/test_zcode_adapter_paths.py
tests/test_agent_inventory_reference.py
tests/test_inventory_scaffold.py
```

Focused acceptance cases cover:

1. both evidenced WeChat candidate paths are declared as the same `local_script` exposure class;
2. ZCode-root PRESENT + Codex-root ABSENT -> `UNKNOWN`, not `AVAILABLE` and not `MISSING_CONFIRMED`;
3. both candidate paths ABSENT -> `MISSING_CONFIRMED` for the covered `local_script` class;
4. inventory documentation exposes the required fields/status terms and is linked from machine diagnostics;
5. scaffold output is deterministic;
6. all scaffold provider entries begin `UNKNOWN` and non-authoritative;
7. declared legal exposure classes are guidance, not absence coverage;
8. CLI output written to a requested file matches the builder output.

Validation result:

```text
8 focused tests / 8 passed
python -m py_compile (new script + new tests): PASS
adapter JSON parse validation: PASS
```

Validation-environment limitation: this ChatGPT execution sandbox could not resolve `github.com`, and the repository has no `.github/workflows` CI surface to execute the branch remotely. The focused run therefore used an isolated reconstructed harness containing the exact new test files and changed scaffold contract plus the relevant unchanged Doctor merge semantics read from repository source. The full pre-existing repository suite was not executed here. Existing adapter contract tests were inspected for affected assumptions; `test_beta1_contract.py` only requires the first WeChat check to remain a binding-scoped `local_script` path containing `search_wechat.js`, which the updated first ZCode-root check preserves.

This limitation is recorded rather than treating an unavailable full checkout as a passing full suite.

## Scope / safety

Not changed:

- `scripts/doctor.py` core behavior;
- `source_semantic_profiles`;
- `web_reader` provider modeling;
- Doctor adapter-id/list UX;
- Doctor UNKNOWN guidance;
- `SKILL.md` structure;
- Context7/Exa/WeChat provider installation or credentials;
- X workstream;
- future domestic/international channel candidates;
- Draft PR #3 or `main`.

Runtime/environment mutation:

```text
ZCode installed Skill copy changed: false
provider/runtime configuration changed: false
credentials/session/network changed: false
channel roadmap reopened: false
```

## Remaining issues

The previously confirmed P1 findings remain deferred:

```text
web_reader representation gap
Doctor --adapter ergonomics / adapter-id discovery
Doctor UNKNOWN -> --agent-inventory hint
```

They were intentionally not bundled into this P0 remediation.

Formal behavior acceptance also remains separate; TASK-019 fixes repository source but does not convert TASK-018 practice observations into `BEHAVIOR_PASS`.

## Final state

```text
READY_FOR_P0_REMEDIATION_ACCEPTANCE
```

The next decision is repository acceptance. If accepted, deployment/re-binding of the updated repository source into the ZCode user Skill root requires a separate explicit authorization/action; TASK-019 itself does not modify the installed copy.
