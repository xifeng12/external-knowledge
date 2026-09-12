---
task_id: TASK-20260912-001
status: arena_v02_second_match_authorized
target_repo: xifeng12/external-knowledge
target_ref: main
implementation_branch: task/20260912-001-v04-capability-diagnostics
result_path: reports/TASK-20260912-001-IMPLEMENTATION.md
diagnostic_result_path: reports/TASK-20260912-001-MACHINE-DIAGNOSTIC.md
machine_receipt_path: evidence/TASK-20260912-001-machine-capability-receipt.json
isolated_worker_authorized: true
---

# Goal

Restore `external-knowledge` as the durable source of truth and evolve it into a strong external-information capability layer that:

- routes concrete information needs/source semantics to the best available retrieval path;
- can diagnose what external-knowledge Skills/providers/capabilities a target machine actually exposes without confusing carrier presence with runtime availability;
- preserves operational status, semantic coverage, source discoverability, and failure-domain independence as separate evidence axes;
- evaluates materially overlapping providers through evidence-based Challenger–Defender comparison so the outcome can be replace, retain, split by scenario, fuse validated strengths, or reject.

# Current verified state

- `main` remains the accepted `v0.3-beta.1` baseline.
- Candidate work remains on `task/20260912-001-v04-capability-diagnostics` under Draft PR #3.
- v0.4 diagnostic mechanisms, target-machine diagnosis, and TASK-002 evidence tightening are complete and durably recorded.
- Capability Arena v0.1 completed its first real match (`github.semantic`: `gh-cli` vs official GitHub MCP Server), was review-corrected against primary contestant receipts, and is accepted.
- First-match adjudication is `KEEP_INCUMBENT`; `github.semantic` remains owned by `gh-cli`.
- First-match teardown is `CLEAN_VERIFIED`; the GitHub MCP Arena runtime was removed and no production installation/routing change was made.
- `references/capability-arena.md` is now v0.2, generalized from the accepted first match so non-GitHub capability matches use the same admission, fairness, provenance, teardown, and routing invariants.

# Effective invariants retained

1. GitHub repository state is durable project authority; machine-local carriers are deployment/runtime evidence, not authority.
2. Runtime routing follows concrete information need/source semantics and uses the minimum retrieval needed for a reliable answer.
3. `UNKNOWN` is not `MISSING_CONFIRMED`.
4. Carrier/Skill presence or declaration is not provider `AVAILABLE`.
5. Operational availability, semantic coverage, discoverability, source-semantic fit, and failure-domain independence remain separate axes.
6. No broad benchmark or synthetic Challenger–Defender battle is needed merely to fill a matrix.
7. A battle requires real overlap, real decision relevance, operational contestants, a real reachable scenario, isolated receipts, and a result capable of changing routing/ownership.
8. Arena-owned provisioning must have baseline, provenance, Provision/Rollback/Promotion/Teardown plans, and verified teardown.
9. Arena may remove only artifacts it can prove it introduced.
10. `Arena runtime != Production runtime`; even a winning Challenger's temporary runtime is torn down before any later production promotion.
11. Routing does not change merely because a Challenger runs or wins; production promotion is a separate Human authorization.
12. Raw contestant receipts are primary execution evidence; reports/adjudication summaries must reconcile to them.

# Accepted Capability Arena baseline

The accepted reusable contract is:

```text
references/capability-arena.md  (v0.2)
```

The first accepted real-match evidence is:

```text
reports/TASK-20260912-003-GITHUB-ARENA.md
evidence/arena/TASK-20260912-003-gh-semantic-001/
```

Outcome:

```text
capability: github.semantic
defender: gh-cli
challenger: github/github-mcp-server v1.12.1
decision: KEEP_INCUMBENT
routing impact: none
teardown: CLEAN_VERIFIED
```

# Human authorization — second Capability Arena match

The Human has authorized the next match after acceptance of Arena v0.1.

Current execution authority is:

```text
tasks/TASK-20260912-004-CAPABILITY-ARENA-COMPLEX-WEB.md
```

Match target:

```text
capability: complex-web.read
Defender: runtime-native.webfetch
Challenger: unclecode/crawl4ai
Arena contract: references/capability-arena.md v0.2
```

This authorization includes only the minimum ephemeral Challenger staging explicitly allowed by TASK-004 after its real-scenario Admission Gate passes.

It does not authorize persistent Crawl4AI installation, system/user Python mutation, global PATH/MCP changes, OS/system dependency installation, browser profile/cookie import, new credentials/API keys, proxy/TLS mutation, other Challengers, production routing changes, PR #3 merge, or `main` merge.

# Second-match real-scenario rule

TASK-004 must not create a synthetic/demo complex-web page just to force a contest.

Before any Crawl4AI staging, the Coordinator must identify a preserved decision-relevant real complex-web read case from current accepted evidence/workload. Preferred candidate is the exact canonical WeChat article used in TASK-002 P7 only if its identity is durably recorded and still reachable; otherwise use another preserved real complex-read case with accepted evidence of incomplete/degraded/dynamic/blocked reading.

If no qualifying real case exists, stop without staging at:

```text
READY_FOR_COMPLEX_WEB_CASE_DECISION
```

# Second-match staging authorization

If the real-scenario gate passes, TASK-004 may stage Crawl4AI only in a match-scoped ephemeral cell. Authorized artifacts include an isolated Python venv/package prefix, Crawl4AI package/dependencies, and a match-scoped Playwright/Chromium browser/cache when required.

All Arena-owned artifacts require provenance and teardown. No elevation/system dependency changes are allowed. If safe isolation cannot be maintained, teardown any partial staging and stop at:

```text
READY_FOR_CRAWL4AI_STAGING_REDESIGN
```

# Current stop / next action

Current phase is ready for target-machine Agent/Coordinator execution of TASK-004 under the v0.2 Arena contract.

The Agent must:

```text
re-read current repository authority
pass the real-scenario Admission Gate before staging
stage Crawl4AI only ephemerally if eligible
run the bounded real match
produce independent contestant/adjudication receipts
teardown all Arena-owned runtime artifacts
push durable result/report
synchronize Issue #2
stop at the first TASK-004 terminal state
```

No third match or production promotion is authorized in the same run.
