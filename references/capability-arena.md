# Capability Arena — v0.3

Domain-specific Challenger–Defender match contract for `external-knowledge`. Deliberately minimal: overlap detection, source-semantic rules, evidence adjudication, ownership decisions, and Arena lifecycle boundaries stay here; generic isolated-execution/rollback mechanics remain out of scope (skill-forge boundary).

v0.3 adds the Source-Semantic Ownership Gate after Human review of TASK-20260912-004. The second match used a canonical WeChat article to adjudicate generic `complex-web.read`; that scenario was misrouted because canonical WeChat reading already has a first-class specialist semantic (`wechat.reader`). The execution evidence remains valid as an observation, but the ownership adjudication is non-binding for `complex-web.read`.

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

## Source-Semantic Ownership Gate — BEFORE capability admission

Resolve the target's source semantic before selecting the Arena capability.

If repository authority already assigns the target to a first-class specialist semantic, that target MUST NOT be used as the representative exam case for a broader/general capability.

Examples:

```text
canonical WeChat article -> wechat.reader Arena
WeChat discovery -> wechat.discovery Arena
GitHub PR/issue/commit/history -> github.semantic Arena
versioned library/framework/API docs -> docs.versioned Arena
ordinary known URL with no specialist owner -> general-web.read / complex-web.read Arena
```

A general/fallback provider may still compete on a specialist source, but only inside that specialist Arena and only for an explicit fallback/escalation ownership question.

Therefore:

```text
specialist source semantic
!= generic complex-web exam case
```

A provider failure on a specialist-owned source cannot by itself promote, reject, or otherwise adjudicate that provider for the broader generic capability.

If a selected scenario is discovered to violate this gate after execution, preserve raw receipts and teardown evidence, but review the ownership result as:

```text
NO_BATTLE / INVALID_SCENARIO
```

and reselect a correctly routed real case before any new staging.

## Match modes

```text
SHADOW       challenger mirrors the defender's live answer; defender output remains authoritative
HEAD_TO_HEAD both contestants independently execute the identical scenario; allowed when the match is safe and fair
```

Fairness rules: identical scenario, target/source scope, authorization, evidence requirement, and bounded time/call/resource budget; contestants must not consume each other's output.

## Admission gate

- Source-Semantic Ownership Gate must pass first.
- Defender: verified operational for the selected scenario (retained runtime evidence or one bounded representative probe).
- Challenger: operational execution surface; if absent, ephemeral staging only under an explicitly authorized lifecycle contract, with all four plans (Provision / Rollback / Promotion / Teardown) recorded before `STAGED`.
- A real scenario must already exist or be directly reachable from accepted project evidence/workload. Do not invent a synthetic failure merely to exercise the Arena.
- Credential rule: existing authentication may be reused only through a safe ephemeral channel with secret values never printed, logged, or persisted. New/interactive credential work stops the match unless explicitly authorized.

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

## Scenario contract

A scenario must be a real `external-knowledge` retrieval/read/search/source-semantic case, not a fabricated benchmark. The task-specific contract defines the target and success evidence.

Examples of decision-relevant scenario evidence may include:

```text
exact source/object identity
content or result completeness
metadata fidelity
structure preservation
source references / links
required dynamic or rendered content
observed failure/degradation
latency / call count / resource cost
```

Do not add dimensions that cannot change the routing, risk, or next action.

## Independent receipts

Each contestant receipt records the minimum evidence required to reproduce and adjudicate that match, including:

```text
provider
execution surface
capability
scenario / target identity
match mode
operations or calls used
result summary
source/evidence references or hashes where appropriate
errors / retries
elapsed time and bounded resource evidence
authorization boundary
staging / environment-mutation evidence
```

The adjudication receipt additionally records staging provenance, shared failure domains, decision, routing impact, and final teardown status. Never store secrets, cookies, raw credentials, or unnecessary sensitive content.

## Adjudication dimensions

Use only dimensions relevant to the capability under test. The standard pool is:

```text
semantic correctness
content/result completeness
evidence fidelity / traceability
coverage / recall
precision / irrelevant output
structure / metadata preservation
determinism / reproducibility
execution latency and resource cost
operational burden
failure-domain independence
agent ergonomics
scenario fit
```

A task may select a strict subset and may add a capability-specific dimension when it is decision-relevant. Do not reduce the result to an arbitrary aggregate score.

Keep verified fact, execution receipt, interpretation, and decision separate. Shared backend, auth, proxy, browser, or control-plane dependencies are recorded and never presented as independent resilience.

## Allowed outcomes

```text
REPLACE
KEEP_INCUMBENT
SPLIT_BY_SCENARIO
FUSE_VALIDATED_STRENGTHS
REJECT_CHALLENGER
NO_BATTLE
```

`REJECT_CHALLENGER` means evidence shows the candidate should not remain an active challenger for the tested ownership question. A capable loser may remain eligible for future scenario-specific re-challenge without being installed or routed in production.

`NO_BATTLE / INVALID_SCENARIO` means the match cannot support an ownership decision because the scenario was not legally routed to the capability under test. It does not count as a loss for either contestant.

## Teardown

Uninstall/stop/delete success alone is insufficient: verify the Arena-owned delta is gone (package/runtime, registration, process, temp cache/browser artifacts, persistent user state, repository state). Terminal classification:

```text
CLEAN_VERIFIED
CLEAN_WITH_RESIDUE
```

`CLEAN_WITH_RESIDUE` must enumerate exact residue and cannot be presented as full rollback.

Promotion is never "keep the Arena install": the temporary copy is torn down even when the Challenger wins; production deployment/re-bind is a separate controlled action.

## Routing impact

An adjudication outcome alone changes no routing. If a routing/ownership change is supported, the task stops at `READY_FOR_ROUTING_CHANGE_DECISION`; only a later explicit authorization may promote it.

## Arena evolution rule

A completed real match may amend this contract only when it exposes a reusable invariant that applies beyond that one provider/source. Provider-specific quirks belong in the match report or provider evidence, not in the generic Arena contract.
