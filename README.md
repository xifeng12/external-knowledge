# external-knowledge v0.4-alpha.1 candidate

Capability-map and machine-diagnostics increment on top of the verified v0.3-beta.1 retrieval model.

## Goal

`external-knowledge` coordinates external-information capabilities by information need and source semantics. It does not replace specialist tools/providers. The v0.4 direction adds two missing pieces without weakening the existing evidence model:

1. a durable capability/channel map;
2. a read-only diagnostic stage that can inventory Skill carriers on a target machine and keep those carrier observations separate from actual provider/capability availability.

## Capability map

Current repository authority models these capabilities:

- `general-web.search`
- `general-web.read`
- `docs.versioned`
- `github.semantic`
- `wechat.discovery`
- `wechat.reader`
- `precision.search`
- `complex-web.read`

See `references/capability-map.md` for the human-facing map. The runtime adapter remains the machine-readable provider/exposure authority.

## Machine diagnostics

The diagnostic path is now:

```text
Explicit Skill roots, when relevant
    ↓
Read-only Skill inventory
    +
Doctor local/runtime evidence
    ↓
Provider status
    ↓
Capability aggregation
    ↓
Capability map / need-aware next action
    ↓
STOP
```

`scripts/scan_skills.py` scans only explicitly supplied roots. It records discovered `SKILL.md` carriers and optional explicit capability claims from an adjacent `external-knowledge.json` sidecar.

Example:

```bash
python scripts/scan_skills.py \
  --root ~/.codex/skills \
  --pretty \
  --output skill-inventory.json
```

Important interpretation:

```text
Skill discovered != provider AVAILABLE
capability claim != provider AVAILABLE
one root absent != no Skills exist on the machine
UNCLASSIFIED != no external-knowledge capability
```

Operational availability still requires runtime exposure or a representative probe and is merged by Doctor under the existing provider/exposure contract.

See `references/machine-diagnostics.md` for the diagnostic contract.

## Existing v0.3-beta.1 evidence retained

The WeChat real case remains authoritative evidence for the separation of operational status from source discoverability:

```text
wechat-article-search
  Operational (observed ZCode case) = AVAILABLE
  Discoverability = LIMITED_OBSERVED

general web for WeChat discovery
  Semantic Coverage = DEGRADED
  Discoverability = VERY_LOW_OBSERVED
```

The finding remains scoped to the recorded cases; it is not a global search-engine ranking.

## Provisioning model unchanged

Capability discovery and environment mutation remain separate phases:

```text
Doctor -> Plan -> exact plan_id -> explicit approval -> exact execution -> Verify
```

Skill inventory does not authorize installation, MCP edits, PATH changes, login, proxy/TLS repair, or other environment mutation.

## Files

```text
external-knowledge/
├── SKILL.md
├── adapters/
├── references/
│   ├── capability-map.md
│   ├── machine-diagnostics.md
│   ├── capability-model.md
│   ├── retrieval-quality.md
│   ├── runtime-adapter-contract.md
│   ├── runtime-notes-zcode.md
│   ├── source-ownership.md
│   ├── setup-policy.md
│   └── provisioning-contract.md
├── scripts/
│   ├── scan_skills.py
│   ├── doctor.py
│   └── plan.py
├── evidence/
└── tests/
```

The existing `BUILD-RECEIPT.json` remains the receipt for the verified v0.3-beta.1 baseline until this candidate completes review/validation.
