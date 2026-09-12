# Capability Arena — v0.1

Domain-specific Challenger–Defender match contract for `external-knowledge`. Deliberately minimal: overlap detection, source-semantic rules, and ownership adjudication stay here; generic isolated-execution/rollback mechanics remain out of scope (skill-forge boundary, TASK-003 §9).

## When a match is legal

A match requires all of:

```text
real capability overlap
real routing/ownership decision
operational Defender
operational Challenger
reachable decision-relevant real scenario
independent execution receipts
result capable of changing routing or ownership
```

Otherwise return `NO_BATTLE` with evidence. Presence alone never wins a match.

## Match modes

```text
SHADOW       challenger mirrors the defender's live answer; defender output remains authoritative
HEAD_TO_HEAD both contestants independently answer the identical scenario; allowed when the match is read-only and clearly safe and fair
```

Fairness rules: identical scenario text, repository scope, authorization, evidence requirement, and bounded time/call budget; contestants must not consume each other's output.

## Admission gate

- Defender: verified `AVAILABLE` (retained runtime evidence or one bounded read-only probe).
- Challenger: operational execution surface; if absent, ephemeral staging only under the lifecycle contract (TASK-003 §1), with all four plans (Provision / Rollback / Promotion / Teardown) recorded before `STAGED`.
- Credential rule: existing authentication may be reused only via an ephemeral channel (process-scope env) with the secret value never printed, logged, or persisted. New/interactive credential work stops the match.

## Staging provenance ledger (per staged artifact)

```text
artifact / registration
preexisting: true|false
introduced_by_match: <match-id>|false
installation/staging method
scope/location
cleanup_policy
```

Arena may remove only artifacts it introduced. Baseline facts must be captured before staging so Arena-created deltas are distinguishable from pre-existing state.

## Scenario

A real `external-knowledge` GitHub task (never a synthetic benchmark), exercising several real GitHub semantics, read-only with respect to GitHub objects.

## Receipts

Per contestant: provider, execution surface, capability, scenario, match mode, operations used, GitHub objects inspected, result summary, evidence references, errors/retries, elapsed time, authorization boundary, staging/mutation evidence. Adjudication receipt additionally records staging provenance and final teardown status. No secrets, ever.

## Adjudication dimensions

```text
semantic correctness | evidence fidelity / traceability | coverage | precision
determinism / reproducibility | execution cost | operational burden
failure-domain independence | agent ergonomics | scenario fit
```

Keep verified fact, execution receipt, interpretation, and decision separate. A shared backend or shared auth identity between contestants is recorded and never presented as independent resilience.

## Allowed outcomes

```text
REPLACE | KEEP_INCUMBENT | SPLIT_BY_SCENARIO | FUSE_VALIDATED_STRENGTHS | REJECT_CHALLENGER | NO_BATTLE
```

## Teardown

Uninstall/stop/delete success alone is insufficient: verify the Arena-owned delta is gone (package, registration, process, temp runtime/cache, persistent user state, repository state). Terminal classification:

```text
CLEAN_VERIFIED
CLEAN_WITH_RESIDUE (must enumerate exact residue)
```

Promotion is never "keep the Arena install": the temporary copy is torn down even when the Challenger wins; production deployment is a separate controlled action.

## Routing impact

An adjudication outcome alone changes no routing. If a routing/ownership change is supported, the terminal state is `READY_FOR_ROUTING_CHANGE_DECISION` and only a later explicit authorization may promote it.
