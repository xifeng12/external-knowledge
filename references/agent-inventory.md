# Agent Runtime Inventory Reference

`--agent-inventory` supplies provider-scoped runtime evidence to `scripts/doctor.py`.

It is **evidence input**, not a capability declaration and not a substitute for the runtime adapter. The adapter defines legal provider exposure classes; the inventory records what the current Agent/runtime actually observed.

## Current shape

Use `inventory_version: 4` for new inventory files in this repository. The current Doctor consumes provider fields directly and does not reject another/missing version number, so the version is compatibility metadata rather than an enforcement gate at this stage.

Top-level shape:

```json
{
  "inventory_version": 4,
  "runtime": "zcode",
  "inventory_scope": "current ZCode session",
  "capabilities": {
    "<capability-id>": {
      "providers": {
        "<provider-id>": {
          "status": "UNKNOWN",
          "evidence_kind": "runtime_tool_exposure",
          "scope": "current ZCode session",
          "authoritative_for_absence": false,
          "exposure_class": "native_tool",
          "carrier_class": "",
          "absence_covers_exposure_classes": [],
          "note": ""
        }
      }
    }
  }
}
```

`capabilities` and `providers` are keyed by the IDs declared in the selected runtime adapter. Do not invent provider IDs to make an inventory look complete.

## Provider fields

### `status`

Valid operational statuses are:

```text
AVAILABLE
AVAILABLE_WITH_SCOPE
UNKNOWN
UNAVAILABLE
BLOCKED
MISSING_CONFIRMED
```

Use the status supported by the actual runtime evidence for the provider in the stated scope.

A runtime inventory may establish `AVAILABLE`, `AVAILABLE_WITH_SCOPE`, `UNAVAILABLE`, or `BLOCKED` directly for its stated scope. `MISSING_CONFIRMED` is stricter: it requires authoritative absence evidence that covers every legal exposure class relevant to the claim.

If an inventory claims `MISSING_CONFIRMED` with `authoritative_for_absence: false`, Doctor downgrades that claim to `UNKNOWN`.

### `evidence_kind`

A short provenance label describing what produced the observation, for example:

```text
runtime_tool_exposure
mcp_registry_inventory
representative_probe
command_probe
agent_inventory
```

This field is descriptive. It does not by itself upgrade the operational status.

### `scope`

The exact runtime boundary for the observation, such as:

```text
current ZCode session
current ZCode MCP execution surface
current process PATH
```

Do not write a machine-wide scope when only one session/registry/process was inspected.

### `authoritative_for_absence`

Boolean. Set `true` only when the observation is allowed to prove absence for the exposure classes named in `absence_covers_exposure_classes`.

`true` does not mean "important evidence". It means the observation has enough authority to support a provider-level missing conclusion for the declared class coverage.

### `exposure_class`

The independent execution surface represented by this inventory observation when one class is directly observed, for example:

```text
native_tool
mcp
path_cli
local_script
```

The adapter's `exposure_contract.legal_classes` remains authoritative for which classes count for that provider.

### `carrier_class`

Optional carrier/registration metadata, for example a Skill or plugin registry. Carrier evidence is kept separate from independent execution exposure.

A carrier existing does **not** prove the provider is callable.

### `absence_covers_exposure_classes`

List of adapter-declared independent exposure classes for which the inventory has authoritative absence evidence.

Example:

```json
{
  "status": "UNKNOWN",
  "evidence_kind": "mcp_registry_inventory",
  "scope": "current ZCode MCP execution surface",
  "authoritative_for_absence": true,
  "absence_covers_exposure_classes": ["mcp"]
}
```

This says MCP is authoritatively absent in the stated scope. If the provider also legally exposes `path_cli`, that provider remains unresolved until the path-CLI class is also covered or another in-contract runtime observation establishes a stronger state.

Do not copy all legal classes into this field merely because the adapter lists them. Coverage belongs here only after those classes were actually inspected by an authoritative source.

### `note`

Optional concise context needed to interpret the evidence. Do not place credentials, secret values, browser session data, or raw authentication material here.

## Carrier/static presence versus runtime exposure

Keep these separate:

```text
Skill/plugin/config/package present
  -> carrier/static evidence
  -> does not prove provider AVAILABLE

independent runtime execution/exposure observed
  -> may establish operational status for the stated scope
```

Likewise, an absent carrier is not automatically provider-level missing unless the adapter says that carrier observation authoritatively covers the provider's legal exposure class.

## Minimal valid example

```json
{
  "inventory_version": 4,
  "runtime": "zcode",
  "inventory_scope": "current ZCode session",
  "capabilities": {
    "general-web.read": {
      "providers": {
        "runtime-native.webfetch": {
          "status": "AVAILABLE",
          "evidence_kind": "runtime_tool_exposure",
          "scope": "current ZCode session",
          "authoritative_for_absence": false,
          "exposure_class": "native_tool",
          "carrier_class": "",
          "absence_covers_exposure_classes": [],
          "note": "native read tool is exposed in this session"
        }
      }
    }
  }
}
```

## Scaffold helper

Use the read-only scaffold generator when you need an inventory skeleton for an adapter:

```bash
python scripts/inventory_scaffold.py \
  --adapter adapters/zcode-v0.3-beta.1.json \
  --pretty \
  --output agent-inventory.json
```

The scaffold is intentionally non-evidentiary:

- every provider starts as `UNKNOWN`;
- `authoritative_for_absence` starts as `false`;
- `absence_covers_exposure_classes` starts empty;
- declared legal exposure classes are shown only as operator guidance;
- no runtime, filesystem, network, environment, provider, or credential probe is performed.

Fill only observations you actually have. Leaving an entry `UNKNOWN` is valid.

## Related references

- `references/machine-diagnostics.md` — diagnostic flow and Machine Capability Receipt.
- `references/capability-model.md` — operational/capability status semantics.
- `adapters/*.json` — provider bindings and legal exposure contracts.
- `tests/fixtures/agent-inventory.example.json` — repository example fixture.
