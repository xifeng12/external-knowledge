# Machine Diagnostics — Skill Inventory and Capability Evidence

## Purpose

Machine diagnostics answers three different questions without collapsing them:

1. **Which Skill carriers are discoverable under the roots we actually inspected?**
2. **Which external-knowledge capabilities do those Skills explicitly claim?**
3. **Which providers/capabilities are actually operational in the current runtime?**

The first two are handled by `scripts/scan_skills.py`. The third remains Doctor + runtime inventory / representative-probe territory.

## Diagnostic flow

```text
Explicit Skill roots
    ↓
Read-only Skill inventory
    ↓
Skill carrier presence
+ explicit capability declarations, when present
    ↓
Runtime adapter + Agent runtime inventory
    ↓
Doctor provider evidence merge
    ↓
Capability operational status
    ↓
Capability map / need-aware next action
    ↓
STOP
```

This flow is diagnostic only. It does not authorize provisioning.

## Skill inventory command

Example:

```bash
python scripts/scan_skills.py \
  --root ~/.codex/skills \
  --root /path/to/another/known/skill-root \
  --pretty \
  --output skill-inventory.json
```

Roots are explicit by design. A scan of one registry/root must not be described as a machine-wide inventory when other legal roots may exist.

## Capability declaration sidecar

A Skill may declare external-knowledge capability claims in a sidecar file next to `SKILL.md`:

```text
<skill>/
├─ SKILL.md
└─ external-knowledge.json
```

Schema v1:

```json
{
  "schema_version": 1,
  "capability_claims": [
    {
      "capability": "wechat.discovery",
      "provider": "wechat-article-search",
      "coverage_grade": "EQUIVALENT",
      "note": "Optional declaration note"
    }
  ]
}
```

Interpretation is intentionally weak:

```text
Skill directory discovered
  -> carrier_status = DISCOVERED

explicit sidecar mapping
  -> claim_status = DECLARED_ONLY

neither state
  -> provider AVAILABLE
```

The sidecar says what the Skill claims to contribute. It does not prove that the provider is callable, authenticated, reachable, correctly configured, or able to retrieve the target source.

## Unclassified Skills

A discovered Skill with no explicit declaration is reported as:

```text
capability_attribution = UNCLASSIFIED
```

Do not infer capability from its name or prose description merely to make the inventory look complete. Human/Agent review may later add an explicit mapping when the overlap decision becomes real.

## Operational verification

Operational availability still requires provider-scoped runtime evidence, for example:

- native tool exposure;
- MCP exposure;
- PATH CLI exposure plus representative runtime evidence where required;
- local script execution plus representative probe;
- other independent execution surfaces explicitly declared by the runtime adapter.

Static Skill presence is carrier evidence only.

## Absence boundary

If an explicit root does not exist, the scanner may report that root absent. It must not conclude:

```text
no Skills exist anywhere on this machine
```

Likewise, an unclassified Skill is not evidence that it has no external-knowledge capability; it means capability attribution is currently unknown.

## Security and mutation boundary

The scanner:

- reads `SKILL.md` frontmatter only for simple inventory fields;
- reads `external-knowledge.json` when present;
- does not execute Skill code;
- does not perform network access;
- does not read environment-variable values or secrets;
- does not install packages;
- does not edit registries, MCP configuration, PATH, proxies, or Skill files.

Output must contain:

```text
environment_mutation_attempted = false
```

## STOP

Stop the inventory phase when all explicitly authorized roots have been inspected and the report distinguishes:

- discovered carriers;
- explicit capability claims;
- unclassified Skills;
- roots not inspected or unavailable;
- operational status still requiring Doctor/runtime evidence.

Do not add more roots merely to claim completeness. Add a root only when it is a real supported/used location whose inspection could change the machine capability conclusion.
