# Capability Arena — v0.5

Domain-specific Challenger–Defender contract for `external-knowledge`. It owns overlap detection, source-semantic routing, evidence class, adjudication, ownership decisions, and Arena lifecycle boundaries; generic isolated-execution/rollback mechanics remain outside this repository (skill-forge boundary).

v0.5 preserves the v0.4 evidence-class model while removing a new over-constraint exposed after TASK-20260913-007: **real-world validation is not a mandatory blocking step during capability exploration.**

The Arena now separates four things:

```text
controlled capability evidence
provisional test-stage policy
real-world validation debt
final production ownership / guaranteed routing
```

A strong controlled benchmark may establish a provisional policy that guides later testing and day-to-day experimental use. Real-world validation may then be collected opportunistically during actual use instead of blocking the test track.

This does not turn benchmark evidence into universal production proof. It makes the confidence level explicit and allows evidence to mature incrementally.

v0.3's Source-Semantic Ownership Gate remains binding: a specialist-owned production source (WeChat, GitHub-native objects, versioned docs, etc.) must not be misused as a generic-capability exam.

## Evidence classes — declare BEFORE admission

Every Arena task must declare exactly one primary evidence class:

```text
CONTROLLED_BENCHMARK
REAL_REPLAY
REAL_WORKLOAD
```

### CONTROLLED_BENCHMARK

Purpose: capability profiling, boundary discovery, Challenger screening, regression testing, and controlled comparison.

A controlled benchmark may be purpose-built or use a public test fixture. It is valid when it has known/inspectable ground truth and isolates decision-relevant variables better than an incidental real page.

Synthetic/test pages are therefore **allowed and often preferred during capability testing**.

A controlled benchmark may support:

```text
benchmark advantage / disadvantage
capability boundary findings
candidate rejection for the tested contract
candidate advancement
scenario hypotheses
PROVISIONAL_TEST_POLICY
```

A `PROVISIONAL_TEST_POLICY` may guide later Arena selection and experimental/runtime behavior during the test phase when its scope is explicit. It is not equivalent to a final production guarantee.

### REAL_REPLAY

Purpose: replay a preserved real task/failure with enough retained ground truth to compare providers fairly.

A representative replay can increase confidence in a provisional policy and may support production-routing evidence when provenance and scope remain valid.

### REAL_WORKLOAD

Purpose: observe or decide on an actual user/project information need.

This is the strongest evidence class for final production routing/ownership claims, but it does not need to be manufactured or scheduled immediately after every controlled benchmark.

## Evidence maturity and validation debt

Use the following maturity model:

```text
CONTROLLED_BENCHMARK
  -> capability finding
  -> optional PROVISIONAL_TEST_POLICY
  -> continue testing / experimental use
  -> collect REAL_REPLAY / REAL_WORKLOAD evidence when naturally available
  -> refine / confirm / overturn the policy
  -> final production ownership only when evidence is sufficient for that claim
```

Real-world validation is therefore:

```text
required before claiming broad/final production confidence
but
non-blocking for continued test-stage evolution
```

When a provisional policy lacks real-world confirmation, record:

```text
validation_debt: OPEN
```

When later real use produces relevant evidence, attach that evidence to the policy and update:

```text
validation_debt: PARTIALLY_PAID | CLOSED | POLICY_REVISED
```

Do not create a synthetic 'real' task merely to pay validation debt.

## Source-Semantic Ownership Gate — BEFORE capability admission

For REAL_REPLAY and REAL_WORKLOAD, resolve the target's source semantic before selecting the Arena capability.

If repository authority already assigns the target to a first-class specialist semantic, that target MUST NOT be used as the representative exam case for a broader/general capability.

Examples:

```text
canonical WeChat article -> wechat.reader Arena
WeChat discovery -> wechat.discovery Arena
GitHub PR/issue/commit/history -> github.semantic Arena
versioned library/framework/API docs -> docs.versioned Arena
ordinary known URL with no specialist owner -> general-web.read / complex-web.read Arena
```

A general/fallback provider may still compete on a specialist source, but only inside that specialist Arena and only for an explicit fallback/escalation question.

For CONTROLLED_BENCHMARK, the fixture must instead declare the capability dimension it is designed to exercise. Avoid fixtures whose platform-specific behavior dominates the capability being tested unless that behavior is itself the declared test dimension.

If a real/replay scenario violates the ownership gate after execution, preserve raw receipts and teardown evidence but review the ownership result as:

```text
NO_BATTLE / INVALID_SCENARIO
```

## When a match is legal

All matches require:

```text
real provider overlap for the capability under test
operational or validly stageable contestants
independent execution receipts
bounded and fair execution conditions
result capable of changing a test, candidate, provisional policy, validation, or routing decision
```

Additionally:

```text
CONTROLLED_BENCHMARK -> known/inspectable ground truth + discriminating test design
REAL_REPLAY          -> preserved real provenance + replay validity
REAL_WORKLOAD        -> reachable decision-relevant live task
```

Otherwise return `NO_BATTLE` with evidence. Presence alone never wins a match.

## Controlled benchmark design gate

A CONTROLLED_BENCHMARK must record before execution:

```text
what capability dimension each fixture tests
ground truth / expected observable outcome
why the fixture discriminates between contestant mechanisms
what would count as pass / partial / fail
whether interaction/rendering is part of the tested capability
bounded call/time/resource budget
which conclusions the benchmark is NOT allowed to make
```

Good controlled tests isolate variables. Examples for `complex-web.read`:

```text
static baseline -> ordinary HTML + tables/structure
dynamic render -> meaningful content absent until JavaScript executes
progressive load -> additional content requires generic scroll/load behavior
```

Do not tailor selectors/content rules after seeing one contestant's result. Do not hide provider-specific setup cost.

## Match modes

```text
SHADOW       challenger mirrors the defender's answer; defender remains authoritative
HEAD_TO_HEAD both independently execute the identical objective under the declared evidence class
```

Fairness means identical objective, target/fixture scope, evidence requirement, authorization, and bounded time/call/resource budget. Internal mechanisms need not be identical; differences in rendering, browser use, interaction, or extraction are often exactly what the Arena is measuring. Contestants must not consume each other's output.

## Admission gate

- Evidence class declared first.
- Applicable Source-Semantic / benchmark-design gate passes.
- Defender operational for the selected task/fixture.
- Challenger has an operational execution surface or is ephemerally stageable under explicit authorization.
- Before `STAGED`, record Provision / Rollback / Promotion / Teardown plans.
- Existing authentication may be reused only through a safe ephemeral channel with secret values never printed, logged, or persisted. New/interactive credential work stops unless explicitly authorized.

## Staging provenance ledger

For every staged artifact record:

```text
artifact / registration
preexisting: true|false
introduced_by_match: <match-id>|false
installation/staging method
scope/location
cleanup_policy
```

Arena may remove only artifacts it introduced. Baseline facts must be captured before staging.

## Independent receipts

Each contestant receipt records the minimum evidence needed to reproduce and adjudicate the match:

```text
provider
execution surface/version
capability
evidence_class
scenario / fixture identity
objective + ground truth when benchmarked
match mode
operations/calls used
result summary
source/evidence references or hashes where appropriate
errors / retries
elapsed time + bounded resource evidence
authorization boundary
staging / environment-mutation evidence
```

The adjudication receipt additionally records staging provenance, shared failure domains, decision, evidence-class scope, policy maturity, validation debt when applicable, and teardown status. Never store secrets, cookies, raw credentials, or unnecessary copyrighted/sensitive content.

## Adjudication dimensions

Select only decision-relevant dimensions from:

```text
semantic/content correctness
content/result completeness
evidence fidelity / traceability
coverage / recall
precision / irrelevant output
structure / metadata preservation
dynamic/rendered-content recovery
determinism / reproducibility
execution latency and resource cost
operational burden
failure-domain independence
agent ergonomics
scenario fit
```

A task may add a capability-specific dimension. Do not reduce the decision to an arbitrary aggregate score.

Keep verified fact, execution receipt, interpretation, benchmark conclusion, provisional policy, and final production decision separate.

## Outcomes and policy authority

Existing outcomes remain available:

```text
REPLACE
KEEP_INCUMBENT
SPLIT_BY_SCENARIO
FUSE_VALIDATED_STRENGTHS
REJECT_CHALLENGER
NO_BATTLE
```

Every outcome must be qualified by `evidence_class`.

For `CONTROLLED_BENCHMARK`, an outcome may produce:

```text
policy_status = TEST_STAGE_BASELINE
production_confidence = UNVALIDATED | PARTIALLY_VALIDATED
validation_debt = OPEN
```

This is permitted to guide continued testing and experimental use. It does not by itself justify a claim such as 'universally superior in production'.

A benchmark may reject a candidate from the current test track when it fails the declared capability contract, but the rejection remains scoped to that tested contract and may be re-challenged under a materially different configuration.

For REAL_REPLAY / REAL_WORKLOAD, a routing-changing result may advance to `READY_FOR_ROUTING_CHANGE_DECISION` when the evidence is representative enough for the stated scope.

## Retry rule

A content-level failure is not automatically transient.

Retry only for a concrete transport/tool/runtime failure that plausibly prevented the intended attempt from completing. A valid returned-but-wrong/incomplete page counts as an observed result, not free retry credit, unless the task explicitly defines repeated sampling as part of the benchmark.

## Teardown

Uninstall/stop/delete success alone is insufficient. Verify the Arena-owned delta is gone: package/runtime, registration, process, temporary cache/browser/profile, environment state, and repository state.

Terminal classification:

```text
CLEAN_VERIFIED
CLEAN_WITH_RESIDUE
```

`CLEAN_WITH_RESIDUE` must enumerate exact residue and cannot be presented as full rollback.

Promotion is never 'keep the Arena install': the temporary copy is torn down even when the Challenger wins; any persistent deployment remains a separate controlled action.

## Non-blocking continuation rule

After a controlled benchmark establishes a test-stage baseline, the Arena may stop at:

```text
READY_FOR_NEXT_ARENA_DECISION
```

with validation debt left open.

Do not force an immediate REAL_REPLAY / REAL_WORKLOAD solely to satisfy process ceremony. Collect relevant real evidence when later use naturally provides it.

## Arena evolution rule

A completed match may amend this contract only when it exposes a reusable invariant that applies beyond one provider/source/fixture. Provider- or fixture-specific quirks belong in the match task/report/receipt, not in the generic Arena contract.
