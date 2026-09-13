---
name: external-knowledge
description: Use when an answer depends on fresh, externally verifiable, source-specific, or model-unknown information, or when the user explicitly asks to diagnose/setup the external-knowledge capability set. Route by information need and source semantics rather than literal provider keywords. Do not use for stable knowledge answerable without retrieval, transformations of supplied content, or unrelated environment setup.
---

# External Knowledge

Answer the user's actual question with the minimum external retrieval needed to make the answer reliable.

This Skill coordinates existing capabilities. It does not replace specialist tools, plugins, MCP servers, search backends, or their installers.

## Modes

Choose exactly one mode from the user's goal.

### Runtime mode

Use for normal external-information tasks.

1. Identify the information need.
2. Resolve the best source semantic and available owner.
3. Retrieve only enough evidence to answer the claim or decision.
4. After a meaningful result set, check source discoverability/quality signals when source-specific discovery matters.
5. If evidence is insufficient, name the exact remaining gap before escalating.
6. Stop when another action is unlikely to change the answer, risk judgment, or next action.

Do not run a full Doctor merely because one provider is absent or unknown.
Do not install or configure providers during runtime retrieval.

### Setup/diagnostic mode

Enter only when the user explicitly asks to diagnose, set up, prepare, configure, or assess external-knowledge capabilities, when the user asks what Skills/capabilities exist on a machine, or when a setup experiment explicitly requires capability inventory.

Use the smallest diagnostic surface that can answer the unresolved question. Do not scan Skill roots when provider/runtime evidence alone is sufficient.

v0.4 diagnostic candidate flow:

```text
Goal / need profile
    ↓
Explicit Skill roots, only when machine Skill inventory matters
    ↓
Read-only Skill inventory
    +
Deterministic read-only Doctor
    +
Agent runtime inventory
    ↓
Provider-scoped evidence
    ↓
Capability aggregation
    ↓
Capability map / need-aware capability plan
    ↓
STOP
```

Skill inventory is carrier-level evidence. A discovered Skill proves only that a Skill package exists under an inspected root. An explicit `external-knowledge.json` sidecar is a declared capability claim, not proof that the provider or capability is operational.

The provisioning approval model remains unchanged: narrowly scoped installation/configuration may occur only after an approval-bound provisioning plan is explicitly approved.

Read `references/capability-map.md` for the current human-facing capability/channel map.
Read `references/machine-diagnostics.md` before scanning Skill roots or interpreting Skill capability claims.
Read `references/capability-model.md` for status semantics.
Read `references/setup-policy.md` before producing a provisioning plan.
Read `references/runtime-adapter-contract.md` when using or extending a runtime adapter.
Read `references/retrieval-quality.md` for source discoverability, low query discrimination, and semantic-mismatch handling.
Read `references/runtime-notes-zcode.md` only for ZCode-scoped observed behavior; do not promote those notes to portable rules.

## Source semantics

Prefer the source type that best matches the claim:

- current product plans/pricing/availability/releases → official/current web source;
- versioned library/framework/SDK/API semantics → version-matched documentation specialist;
- repository/PR/issue/commit/release/source-history semantics → GitHub-native specialist;
- explicit WeChat discovery or remembered Chinese long-form content for which WeChat is high-fit → WeChat discovery specialist;
- canonical `https://mp.weixin.qq.com/s/<id>` body reading → WeChat reader specialist;
- general current facts → general web owner;
- exact obscure term/API/error/version after ordinary search misses → precision challenger;
- known URL extraction gap → extraction challenger if already available.

Chinese language alone does not imply WeChat.
Semantic WeChat routing at the agent layer does not imply the underlying search backend is vector/semantic search.

## Capability status discipline

Keep these questions separate:

1. **Operational status** — can this capability actually be used in the current runtime?
2. **Semantic coverage** — is the available path equivalent for this information need, degraded, or specialized?
3. **Source discoverability** — for this Provider × Source Semantic, how well does observed retrieval actually surface items from the target ecosystem?
4. **Need** — does the user's intended workload require or merely benefit from this capability?
5. **Skill/carrier inventory** — which Skill packages are visible under the roots actually inspected, and which capabilities do they explicitly claim?

`UNKNOWN` is not `MISSING_CONFIRMED`.

Keep capability and provider status separate. A provider can be missing while the capability remains available through another provider.

Keep Skill/carrier presence separate from provider availability. A Skill directory, plugin registration, config file, or package can show that a carrier exists without proving an independent execution surface is callable.

Count only independent execution surfaces as exposure classes. Plugin/Skill/config/package observations are carrier evidence unless they independently execute the provider.
Absence observations only prove missing when authoritative absence covers every legal exposure class declared by that capability's runtime adapter contract.

Do not infer `AVAILABLE` merely because a CLI, file, package, Skill, sidecar, or config entry exists. Presence is component/carrier evidence; operational availability needs runtime exposure or a representative probe.

## Fallback

A fallback is justified only by a concrete gap or a preferred path that is not currently viable.

A degraded fallback may be used when:

- it is actually available;
- it can still make progress on the user's goal;
- the semantic coverage loss is disclosed when material;
- no false claim is made that the preferred specialist is confirmed missing.

Do not fan out providers "for completeness".

For WeChat article discovery in the current ZCode evidence profile:

- the specialist is operational but has `LIMITED_OBSERVED` discoverability;
- general web is `DEGRADED` with `VERY_LOW_OBSERVED` discoverability.

Therefore a zero-result query from either path does not prove non-existence. Do not spend repeated same-channel rewrites once the query-quality STOP signals fire.

## Environment mutation boundary

Capability discovery and environment mutation are separate phases.

During runtime mode, and during diagnosis/planning before explicit approval, do not:

- install a provider;
- modify MCP configuration;
- modify PATH;
- change proxy/TLS settings;
- log in to services;
- repair launchers;
- create background services;
- upgrade unrelated dependencies.

A capability plan may say `INSTALL_CANDIDATE` or `CONFIGURE_CANDIDATE`.

Before any mutation:
1. read `references/provisioning-contract.md`;
2. materialize a concrete plan with `scripts/plan.py`;
3. show exact steps/targets and the `plan_id`;
4. obtain explicit approval for that exact plan;
5. execute only the approved actions;
6. on any required change, STOP and create a new plan for new approval;
7. verify with Doctor + runtime exposure/representative probe.

## Skill inventory contract

`scripts/scan_skills.py` is deterministic and read-only with respect to the target Skill roots.

It may:

- inspect only explicitly supplied Skill roots;
- find directories containing `SKILL.md`;
- read simple top-level inventory fields from `SKILL.md` frontmatter;
- read an adjacent `external-knowledge.json` capability-declaration sidecar when present;
- report discovered carriers, explicit claims, unclassified Skills, and unavailable roots.

It must not:

- execute Skill code;
- infer capabilities from names/descriptions when no explicit declaration exists;
- claim one inspected root is a machine-wide inventory;
- mark a provider/capability `AVAILABLE` from Skill presence or a capability claim;
- perform network access or environment mutation.

A missing root proves only that the supplied root was unavailable. An unclassified Skill means capability attribution is unknown, not that the Skill has no external-knowledge capability.

## Doctor contract

`scripts/doctor.py` is deterministic and read-only with respect to the runtime environment.

It may inspect:

- command presence in PATH;
- file/path/glob presence;
- environment-variable **names/presence only**, never secret values;
- agent-supplied runtime inventory evidence.

It must not perform network access, install packages, edit configuration, or run provider login/setup commands.

A single failed local check must degrade to evidence for that capability and must not abort the whole report.

For provider-level absence, Doctor must use each provider binding's `exposure_contract`. A `PRESENT` observation only conflicts when it belongs to an independent legal exposure class for that provider. If the legal exposure classes are undeclared or only partially covered by authoritative absence, keep `UNKNOWN`.

## Stop

### Runtime Evidence STOP

Before another retrieval ask:

> What concrete unknown remains, can this action reduce it, and would the result change the answer, risk judgment, or next action?

If not, stop.

Also stop repeated query rewriting when `LOW_QUERY_DISCRIMINATION` is observed.

When Top-N results strongly reflect the wrong sense of an ambiguous term:

- if user context already resolves the sense, make at most one contextual rewrite;
- if mismatch persists, stop and disclose it;
- if context does not resolve the sense, ask the user to disambiguate.

### Setup Evidence STOP

Stop diagnosis/planning when:

- explicitly authorized Skill roots, when relevant, have been inventoried without being treated as machine-wide unless that authority is real;
- discovered carriers, explicit capability claims, and unclassified Skills remain separate from operational availability;
- deterministic local evidence is collected;
- agent runtime exposure is recorded where available;
- `UNKNOWN` and `MISSING_CONFIRMED` are not conflated;
- each relevant capability has a need-aware action;
- no installation/configuration was executed.

## Beta provisioning boundary

Read `references/provisioning-contract.md` before proposing any install/configuration action.

The planner is non-executing. A provisioning recipe must exist in the runtime adapter before a provider can become an executable plan.

Never invent installation commands because a capability is missing.

Explicit approval is bound to the exact `plan_id`. A changed action invalidates approval.

After an approved change, rerun Doctor and verify runtime exposure. Presence alone is not success.
