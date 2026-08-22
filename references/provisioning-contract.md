# Provisioning Contract — v0.3-beta

The beta phase adds controlled environment mutation **after** diagnosis. It does not add a universal installer.

## Lifecycle

```text
Doctor
  ↓
Capability plan
  ↓
Provider selection
  ↓
Concrete provisioning plan
  ↓
Explicit human approval bound to plan_id
  ↓
Agent executes only approved steps
  ↓
Doctor again
  ↓
Representative read-only probe when safe/available
  ↓
STOP
```

## Hard gate

No mutation is allowed from:

- provider `UNKNOWN`;
- non-authoritative absence;
- `NOT_NEEDED` / `OPTIONAL`;
- an unvalidated provisioning recipe;
- a plan that the user has not explicitly approved.

`INSTALL_CANDIDATE` is capability-level. The selected provider must itself be `MISSING_CONFIRMED`.

## No universal installer

`scripts/plan.py` only materializes an approval-bound plan.

It never executes commands or writes runtime configuration.

The Agent performs approved actions using the runtime's normal execution/configuration tools.

This avoids turning `external-knowledge` into another package manager.

## Provisioning recipe schema

A provider adapter may declare:

```json
"provisioning": {
  "install": {
    "source": "upstream or previously validated installation contract",
    "steps": [
      {
        "kind": "run_command",
        "description": "Install package X",
        "argv": ["tool", "install", "x"]
      }
    ],
    "verification": [
      {
        "kind": "doctor_then_representative_probe",
        "success": "..."
      }
    ]
  }
}
```

Supported planning step kinds:

- `run_command`
- `write_config`
- `install_skill`
- `register_mcp`
- `agent_instruction`

The planner does not execute any of them.

## Approval binding

The planner hashes the semantic plan content into:

```text
plan_id = ekp-...
```

Approval applies only to that exact plan.

If any of these change:

- provider;
- command/argv;
- config target/content;
- installation target;
- verification requirement;

generate a new plan and obtain new approval.

Failure does not authorize improvisation.

```text
approved command fails
→ STOP_AND_REPLAN
```

Do not silently add package-manager repair, proxy fixes, TLS fixes, PATH changes, alternate mirrors, privilege escalation, or unrelated dependencies.

## Verification

Installation success is not:

```text
file exists
CLI exists
package manager returned 0
config was written
```

Success requires the capability gap to be reduced.

Default verification:

1. rerun Doctor;
2. check provider runtime exposure;
3. perform a representative read-only probe when safe and available;
4. confirm capability-level state/coverage changed as expected.

Static presence may support verification but is not sufficient by itself.

## Provenance

Only add a provisioning recipe when its source is explicit and its steps have been reviewed for the target runtime.

A missing provisioning recipe is:

```text
UNRESOLVED
```

not permission for the Agent to invent installation steps.
