---
task_id: TASK-20260912-001
status: implementation_review
target_repo: xifeng12/external-knowledge
target_ref: main
implementation_branch: task/20260912-001-v04-capability-diagnostics
result_path: reports/TASK-20260912-001-IMPLEMENTATION.md
isolated_worker_authorized: true
---

# Goal

Restore `external-knowledge` as the durable source of truth on the new device and evolve it toward the Human's actual product goal: give Agents a strong external-information capability that routes different information needs to the best available retrieval tools, can diagnose which Skill/provider capabilities exist on a target machine without confusing carrier presence with availability, and evaluates materially overlapping new Skills/providers against incumbents through evidence-based Challenger–Defender comparison so the result can be replace, retain by scenario, merge validated strengths, or reject.

# Current verified state

- Repository exists and is authoritative: `xifeng12/external-knowledge`.
- Authority/base commit for this increment: `579d94a7b9127307f7be066161341214990a7c93`.
- Pre-handoff implementation baseline: `529a8b374af81a17397c506b5046b614b4e37170`.
- Verified baseline package remains `external-knowledge v0.3-beta.1`; the implementation branch is a `v0.4-alpha.1 candidate`, not yet merged authority.
- Existing routing distinguishes information need/source semantic, operational status, semantic coverage, discoverability, fallback, independent exposure, and STOP behavior.
- A human-facing capability/channel map has now been implemented on the candidate branch.
- A read-only machine diagnostics path has now been implemented on the candidate branch: explicit Skill-root scan + existing Doctor runtime evidence + a combined Machine Capability Receipt.
- Actual target-machine Skill/runtime state is still `UNKNOWN` because this execution surface does not have direct access to the Human's Windows filesystem.
- Challenger–Defender lifecycle adjudication is still unimplemented; existing runtime `challenger` wording remains fallback/escalation behavior rather than lifecycle replacement governance.

# Human authorization receipt

After the original read-only alignment stop state, the Human explicitly authorized execution of the capability-map direction and requested an additional diagnostic stage to determine which Skills exist on a machine and what external-knowledge capabilities they already have.

This was interpreted as repository-only implementation authorization. It did not authorize provider installation/configuration, MCP/PATH/runtime mutation, login, proxy/TLS changes, or synthetic battles.

# Effective decisions

1. GitHub repository state is the durable source of truth. A machine-local installed Skill is a deployment copy/carrier, not repository authority.
2. The product goal is stronger retrieval capability, not merely more routing rules or diagnostics.
3. Runtime routing selects tools by concrete information need/source semantics and uses the minimum retrieval needed for a reliable answer.
4. Repository capability declarations, Skill carrier presence, provider operational availability, semantic coverage, and source discoverability are distinct evidence layers.
5. A discovered Skill proves only carrier presence under an inspected root. An explicit Skill capability declaration proves only a declared mapping. Neither state upgrades a provider/capability to `AVAILABLE`.
6. Machine-wide claims require authority over the relevant machine exposure/Skill roots. One inspected root cannot silently stand for every possible Skill location.
7. A newly added Skill/provider that materially overlaps an incumbent capability should not automatically coexist forever. Where a real replacement decision exists, compare challenger and defender on reachable, decision-relevant scenarios.
8. Comparison outcomes are bounded to evidence and may be: challenger replaces incumbent for the tested scenario; incumbent remains; responsibilities split by scenario; validated strengths are fused; or challenger is not admitted to the active pool.
9. Compare the actual execution solution at the layer where overlap exists. Shared underlying providers/failure domains must not be misrepresented as independent retrieval capability.
10. A battle is not required for non-overlapping capabilities. Evaluation scope follows the actual decision/impact surface.
11. Fusion is not automatic concatenation of two `SKILL.md` files; retain only validated useful behavior and re-verify the combined path.

# Implemented increment

The authorized capability-map + machine-diagnostics increment is implemented on:

```text
task/20260912-001-v04-capability-diagnostics
```

Durable implementation receipt:

```text
reports/TASK-20260912-001-IMPLEMENTATION.md
```

Implemented components include:

- `references/capability-map.md`;
- `references/machine-diagnostics.md`;
- `scripts/scan_skills.py`;
- `scripts/machine_report.py`;
- focused diagnostic/contract tests;
- root `SKILL.md` diagnostic routing updates;
- README candidate documentation.

No adapter, `doctor.py`, `plan.py`, provider configuration, provisioning recipe, or runtime environment was changed.

# Validation state

Focused isolated validation for the new diagnostic code/contracts:

```text
10 tests run
10 passed
0 failed
0 errors
```

The new Python files also passed `py_compile`.

The complete pre-existing repository test suite was not rerun because the isolated execution container could not resolve `github.com` for a full repository clone. This limitation is recorded in the implementation receipt; no full-suite-pass claim is made.

# Superseded / withdrawn assumptions

- Superseded: "the Skill was never put in a repository and was completely lost after the device change." The GitHub repository preserves the v0.3-beta.1 baseline.
- Superseded: treating the current fallback `precision challenger` concept as already satisfying the desired Challenger–Defender capability-evolution mechanism.
- Not accepted: inferring operational capability from Skill presence or a declaration sidecar.
- Not accepted: adding broad benchmark matrices, generic defense layers, exhaustive tool competitions, or speculative Skill roots solely for completeness.

# Unresolved items

1. Whether the old device contained post-`529a8b3` local-only changes that were never pushed. No such changes are claimed recovered.
2. The real new-device Skill inventory and runtime/provider availability. The mechanism now exists, but no target-machine receipt has been fabricated.
3. The minimum Challenger–Defender lifecycle implementation for overlap detection, scoped comparison evidence, adjudication, and routing updates without duplicating `skill-forge` or `skill-architect`.
4. The first real overlapping battle. `complex-web.read` (`runtime-native.webfetch` vs `firecrawl`) remains the natural candidate, but only after a reachable real extraction decision exists and both relevant paths have decision-changing evidence.

# Known invariants

- `UNKNOWN` is not `MISSING_CONFIRMED`.
- Skill/carrier `DISCOVERED` is not provider `AVAILABLE`.
- Capability `DECLARED_ONLY` is not provider `AVAILABLE`.
- `UNCLASSIFIED` does not mean "no capability"; it means attribution is unknown.
- Provider availability, semantic coverage, and source discoverability remain separate axes.
- Retrieval/diagnosis and environment mutation remain separate phases.
- Existing evidence-based STOP rules remain valid unless real new evidence falsifies/refines them.
- Repository task authority wins over chat summaries if they diverge.

# Current stop state

Stop this implementation phase after the candidate branch is durably reported and presented for review.

Do not:

- merge to `main` without Human review/authorization;
- install/repair/configure providers;
- mutate MCP/PATH/runtime settings;
- invent target-machine results;
- begin a synthetic Challenger–Defender battle.

# Next authorization

The next decision is intentionally narrow:

1. **review/merge authorization** for the implementation branch; and/or
2. **target-machine read-only diagnostic execution** on real supported Skill roots/runtime evidence.

No provisioning authorization is requested at this state.
