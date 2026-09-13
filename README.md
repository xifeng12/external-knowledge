# external-knowledge v0.4-alpha.1 candidate

Capability-map, machine-diagnostics, and Capability Arena evolution on top of the verified v0.3-beta.1 retrieval model.

## Goal

`external-knowledge` coordinates external-information capabilities by information need and source semantics. It does not replace specialist tools/providers. The v0.4 direction adds:

1. a durable capability/channel map;
2. read-only machine diagnostics;
3. evidence-driven Challenger–Defender evaluation with lifecycle/teardown control;
4. explicit separation between controlled test evidence, opportunistic real-world validation, and final production ownership.

## Current Arena testing baseline

Accepted test-stage findings currently include:

```text
github.semantic
  -> gh-cli remains incumbent after GitHub MCP challenge

complex-web.read (CONTROLLED_BENCHMARK)
  ordinary/static -> runtime-native.webfetch preferred
  dynamic/rendered/progressive -> Crawl4AI is the current challenger/escalation candidate
  validation_debt -> OPEN_NONBLOCKING
```

The complex-web split is a provisional test-stage policy, not a universal production claim. Relevant REAL_REPLAY / REAL_WORKLOAD evidence should be collected opportunistically during normal use and may confirm, refine, or overturn it without blocking continued Arena testing.

See:

- `references/capability-map.md`
- `references/capability-arena.md`
- `tasks/TASK-20260913-008-TEST-STAGE-BASELINE-ACCEPTANCE.md`

## Machine diagnostics

The diagnostic path remains:

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
Machine Capability Receipt
    ↓
Capability map / need-aware next action
    ↓
STOP
```

`scripts/scan_skills.py` scans only explicitly supplied roots. `scripts/machine_report.py` combines carrier observations with Doctor operational evidence.

Important interpretation:

```text
Skill discovered != provider AVAILABLE
capability claim != provider AVAILABLE
one root absent != no Skills exist on the machine
UNCLASSIFIED != no external-knowledge capability
Machine Capability Receipt operational status = Doctor status only
```

## Arena evidence maturity

Arena v0.5 distinguishes:

```text
CONTROLLED_BENCHMARK
REAL_REPLAY
REAL_WORKLOAD
```

Controlled benchmarks are valid for capability profiling and may establish a provisional test-stage policy. Real-world evidence is strongest for final production claims but is non-blocking during current capability exploration.

```text
CONTROLLED_BENCHMARK
  -> TEST_STAGE_BASELINE
  -> continue testing / experimental use
  -> opportunistic real-world receipts
  -> refine / confirm / overturn
  -> final production ownership when evidence is sufficient
```

## Provisioning model unchanged

Capability discovery/evaluation and environment mutation remain separate phases. Arena-owned staging must carry provenance and mandatory teardown. A benchmark win does not mean keeping the Arena install.

No current test-stage finding implicitly authorizes persistent provider installation, credential changes, browser-profile imports, production routing changes, or PR/main merge.
