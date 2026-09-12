# TASK-20260912-001 — Implementation Receipt

## State

`AWAITING_REVIEW`

Implementation branch:

```text
task/20260912-001-v04-capability-diagnostics
```

Authority/base commit:

```text
579d94a7b9127307f7be066161341214990a7c93
```

Validated code/document candidate head before this bookkeeping receipt:

```text
99d4cbee98b001e07d9085f1f9ad93b2397e6621
```

## Human authorization received

After the read-only alignment stop state, the Human explicitly authorized execution of the capability-map direction and additionally requested a diagnostic stage that can determine which Skills exist on a machine and what external-knowledge capabilities they already have.

This authorization was interpreted as repository-only implementation. It did **not** authorize provider installation/configuration, MCP/PATH/runtime mutation, login, proxy/TLS changes, or synthetic Challenger–Defender battles.

## Implemented increment

### 1. Durable capability map

Added:

```text
references/capability-map.md
```

It records the current eight modeled capabilities and their declared provider/channel roles while separating:

- source semantic;
- default owner;
- runtime availability;
- observed quality;
- escalation/challenger entry conditions.

It explicitly separates the repository capability map from a machine capability receipt.

### 2. Read-only Skill inventory

Added:

```text
scripts/scan_skills.py
references/machine-diagnostics.md
```

The scanner accepts explicit Skill roots and reports:

- discovered `SKILL.md` carriers;
- simple inventory metadata;
- optional explicit capability declarations from adjacent `external-knowledge.json` sidecars;
- unclassified Skills;
- unavailable roots.

It does not execute Skill code, access the network, install/configure anything, or infer provider availability from Skill presence.

Capability declaration state is intentionally weak:

```text
DISCOVERED      = carrier presence only
DECLARED_ONLY   = explicit capability claim only
UNCLASSIFIED    = no explicit capability attribution
```

None of these states imply `AVAILABLE`.

### 3. Machine Capability Receipt

Added:

```text
scripts/machine_report.py
```

It combines:

```text
Skill inventory + existing Doctor report
```

into one machine capability receipt. Its invariant is:

```text
operational_status_source = Doctor report only
```

Skill carrier/claim evidence can be attached to a capability but cannot upgrade Doctor operational status.

### 4. Root Skill routing

Updated `SKILL.md` so Setup/Diagnostic mode can enter Skill inventory only when the unresolved question actually concerns the machine Skill landscape.

The new path is bounded:

```text
explicit roots -> Skill inventory -> Doctor/runtime evidence -> capability aggregation -> receipt/map -> STOP
```

The existing provisioning approval boundary is unchanged.

## Files changed before bookkeeping

Comparison from authority commit to candidate code/doc head showed nine implementation files:

```text
README.md
SKILL.md
references/capability-map.md
references/machine-diagnostics.md
scripts/machine_report.py
scripts/scan_skills.py
tests/test_machine_report.py
tests/test_scan_skills.py
tests/test_v04_diagnostic_contract.py
```

No adapter, `doctor.py`, `plan.py`, provider configuration, runtime environment, or provisioning recipe was changed.

## Validation receipt

Isolated validation was run against the newly authored diagnostic code/contracts:

```text
python3 -m py_compile \
  scripts/scan_skills.py \
  scripts/machine_report.py \
  tests/test_scan_skills.py \
  tests/test_machine_report.py \
  tests/test_v04_diagnostic_contract.py
```

and:

```text
python3 -m unittest -v \
  tests/test_scan_skills.py \
  tests/test_machine_report.py \
  tests/test_v04_diagnostic_contract.py
```

Result:

```text
10 tests run
10 passed
0 failed
0 errors
```

Covered decision-relevant invariants include:

- discovered Skill does not invent capability attribution;
- only explicit sidecar claims are treated as claims;
- malformed sidecar does not abort the scan;
- missing inspected root is not promoted to machine-wide absence;
- Skill claim does not upgrade Doctor `UNKNOWN` to `AVAILABLE`;
- unclassified Skills and unmatched claims remain visible;
- all new diagnostic outputs retain `environment_mutation_attempted = false`;
- repository capability map and machine receipt remain separate.

### Validation limitation

The agent execution container could not resolve `github.com`, so a network `git clone` of the complete repository was unavailable. Therefore the full pre-existing repository test suite was **not** re-run in that container. No claim is made that the full suite was executed.

This limitation is bounded because the implementation did not modify `doctor.py`, `plan.py`, the adapter, or existing tests. The new executable code was syntax-checked and exercised by its focused tests. A full-suite run remains desirable before merge if an execution surface with the complete checkout is available.

## Actual target-machine state

Still unknown.

This implementation creates the diagnostic mechanism but this ChatGPT execution surface has no direct access to the Human's Windows filesystem/Skill roots. Therefore no target-machine Skill inventory or Machine Capability Receipt has been fabricated.

The first real target-machine run should use only actual supported Skill roots. For example, if `~/.codex/skills` is a real root on that machine:

```bash
python scripts/scan_skills.py --root ~/.codex/skills --pretty --output skill-inventory.json
```

Then produce/obtain a real Doctor report for the same runtime scope and merge:

```bash
python scripts/machine_report.py \
  --skill-inventory skill-inventory.json \
  --doctor-report doctor-report.json \
  --pretty \
  --output machine-capability-receipt.json
```

Do not add speculative roots merely to claim completeness.

## Deferred work

Not implemented in this increment:

- provider provisioning or repair;
- automatic inference of capability from Skill prose/name;
- broad benchmark matrices;
- generic Skill evaluation framework duplicated from `skill-forge`;
- Challenger–Defender lifecycle adjudication;
- synthetic battle fixtures.

The first real overlap remains `complex-web.read` (`runtime-native.webfetch` vs `firecrawl`), but a battle should begin only when a reachable real extraction decision exists and both relevant paths have decision-changing evidence.

## Stop state

Repository implementation is complete for the authorized capability-map + machine-diagnostics increment and is ready for review.

Next authorization required:

1. review/merge this implementation branch; and/or
2. run the read-only diagnostic on a real target-machine Skill root/runtime execution surface.

No provisioning authorization is currently requested.
