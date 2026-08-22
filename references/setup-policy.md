# Setup Policy — v0.3-beta

## Purpose

Diagnose the capability set and produce a need-aware plan without mutating the runtime.

## Flow

```text
Need profile
  ↓
Capability
  ↓
Provider bindings
  ↓
Independent exposure evidence
  ↓
Provider status
  ↓
Capability aggregation
  ↓
Plan
  ↓
STOP
```

## Installation boundary

alpha.2 does not install, configure, authenticate, repair, or update providers.

A provider may be `MISSING_CONFIRMED` while the capability remains available through another provider.

Therefore do not produce installation pressure from provider status alone.

## Carrier normalization gate

Before merging evidence:

- plugin/skill/config/package observations must be mapped to the independent execution surface they actually create;
- the carrier must not become a second legal exposure class for the same provider path.

## PATH gate

`path_cli` absence may be authoritative when the check is explicitly scoped to current process command resolution.

`path_cli PRESENT` proves exposure presence only. It does not prove provider operational availability.

## Capability plan

At capability level:

- operational equivalent provider -> `KEEP`;
- operational degraded/specialized provider -> `KEEP` in alpha unless an explicit observed gap requires challenger provisioning;
- capability `UNKNOWN` -> `TARGETED_DIAGNOSIS`;
- capability `MISSING_CONFIRMED` + meaningful Need + no equivalent fallback -> `INSTALL_CANDIDATE`;
- optional/not-needed -> `DO_NOT_INSTALL`.

No action is executed in alpha.


## Beta transition

Diagnosis and planning remain non-mutating.

Environment mutation is allowed only after:

```text
reviewed provider recipe
+ concrete plan
+ exact plan_id
+ explicit human approval
```

Execution is performed by the Agent/runtime tools, not by `plan.py`.

Any deviation from the approved steps requires STOP_AND_REPLAN.
