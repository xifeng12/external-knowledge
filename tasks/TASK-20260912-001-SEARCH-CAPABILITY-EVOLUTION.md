---
task_id: TASK-20260912-001
status: ready
target_repo: xifeng12/external-knowledge
target_ref: main
result_path: reports/TASK-20260912-001-IMPLEMENTATION.md
isolated_worker_authorized: true
---

# Goal

Restore `external-knowledge` as the durable source of truth on the new device and evolve it toward the Human's actual product goal: give Agents a strong external-information capability that routes different information needs to the best available retrieval tools, and evaluates overlapping new Skills/providers against existing ones through evidence-based Challenger–Defender comparison so that the result is replace, retain by scenario, merge, or reject.

# Current verified state

- Repository exists and is authoritative: `xifeng12/external-knowledge`.
- Pre-handoff `main` baseline: `529a8b374af81a17397c506b5046b614b4e37170`.
- Repository package/version remains `external-knowledge v0.3-beta.1`.
- Existing durable assets include `SKILL.md`, ZCode adapter, capability/retrieval/source-ownership references, `doctor.py`, `plan.py`, tests, and the real WeChat retrieval evidence case.
- Existing routing already distinguishes information need/source semantic, operational status, semantic coverage, discoverability, fallback, and STOP behavior.
- Existing uses of the word `challenger` are fallback/escalation behavior after an observed retrieval gap; they are not yet a lifecycle mechanism for a new Skill/provider to challenge the incumbent default owner.
- No open Issue or project-local task authority existed before this handoff.

# Effective decisions

1. GitHub repository state is the durable source of truth. A machine-local installed Skill is a deployment copy, not the authority.
2. The product goal is stronger retrieval capability, not merely more routing rules or diagnostics.
3. Runtime routing should select tools by concrete information need/source semantics and use the minimum retrieval needed for a reliable answer.
4. A newly added Skill/provider that materially overlaps an incumbent capability should not automatically coexist forever. Where a real replacement decision exists, compare challenger and defender on reachable, decision-relevant scenarios.
5. Comparison outcomes are bounded to the evidence and may be: challenger replaces incumbent for the tested scenario; incumbent remains; responsibilities split by scenario; validated strengths are fused; or challenger is not admitted to the active pool.
6. Compare the actual execution solution at the layer where overlap exists. Shared underlying providers/failure domains must not be misrepresented as independent retrieval capability.
7. A battle is not required for non-overlapping capabilities. Evaluation scope follows the actual decision/impact surface.
8. Fusion is not automatic concatenation of two `SKILL.md` files; retain only validated useful behavior and re-verify the combined path.

# Superseded / withdrawn assumptions

- Superseded: "the Skill was never put in a repository and was completely lost after the device change." The GitHub repository exists and preserves the v0.3-beta.1 baseline.
- Superseded: treating the current fallback `precision challenger` concept as already satisfying the desired Challenger–Defender capability-evolution mechanism.
- Not accepted: adding broad benchmark matrices, generic defense layers, or exhaustive tool competitions without a concrete unresolved decision that they can change.

# Unresolved items

1. Whether the old device contained post-`529a8b3` local-only changes that were never pushed. No such changes are claimed recovered.
2. Whether the new device currently has an installed/deployed copy of the Skill and, if so, whether it matches repository authority.
3. The minimum v0.4 design needed to represent overlap detection, comparison evidence, adjudication, and routing updates without duplicating `skill-forge` or `skill-architect` responsibilities.
4. Which first real overlapping candidate should exercise the Challenger–Defender mechanism. Do not invent a synthetic battle solely to make the framework look complete.

# Next authorized action

Read-only alignment only:

- re-read current repository authority and the v0.3-beta.1 implementation;
- verify the current repository baseline and, when the new-device execution surface is available, identify any deployment drift relevant to resuming work;
- derive the smallest concrete v0.4 delta required by the goal above;
- identify the first real decision-relevant candidate/scenario if one is already available from current work;
- return the proposed implementation boundary and the exact next authorization needed.

Do not modify `SKILL.md`, adapters, scripts, tests, provider configuration, or the runtime environment until the Human explicitly authorizes implementation/provisioning.

# Acceptance criteria for this handoff phase

- The receiver can recover the project from GitHub without relying on this chat transcript.
- Verified facts, execution receipts, unknown/local-only state, and unimplemented design intent remain clearly separated.
- The proposed v0.4 increment is bounded to real unresolved decisions and does not duplicate neighboring Skill responsibilities.
- The receiver stops before implementation and asks only for the next authorization that is actually required.

# Known invariants

- `UNKNOWN` is not `MISSING_CONFIRMED`.
- Provider availability, semantic coverage, and source discoverability remain separate axes.
- Retrieval and environment mutation remain separate phases.
- Existing evidence-based STOP rules remain valid unless real new evidence falsifies/refines them.
- Repository task authority wins over chat summaries if they diverge.

# Stop conditions

Stop this phase after the read-only alignment and bounded v0.4 proposal are durably reported or presented for Human authorization. Do not implement the new mechanism or install/repair providers without explicit authorization.
