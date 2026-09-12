---
task_id: TASK-20260912-001
status: ready_for_capability_gap_decision
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
- later evaluates materially overlapping Skills/providers through evidence-based Challenger–Defender comparison so the outcome can be replace, retain by scenario, fuse validated strengths, or reject.

# Current verified state

- Repository authority exists at `xifeng12/external-knowledge`.
- Authority/base commit for the v0.4 increment was `579d94a7b9127307f7be066161341214990a7c93`; the pre-handoff implementation baseline was `529a8b374af81a17397c506b5046b614b4e37170`.
- `main` remains the accepted `v0.3-beta.1` baseline; `task/20260912-001-v04-capability-diagnostics` is the unmerged `v0.4-alpha.1` candidate reviewed through Draft PR #3.
- The candidate implements a durable capability map, read-only Skill inventory, Machine Capability Receipt merger, diagnostic routing updates, and focused tests.
- Focused validation for the new diagnostic code/contracts passed: `10 tests / 10 passed`, plus `py_compile`. The complete pre-existing suite was not rerun in the isolated build surface; that limitation is recorded in the implementation receipt.
- First real target-machine diagnosis completed 2026-09-12 via the authorized ZCode session surface; see `reports/TASK-20260912-001-MACHINE-DIAGNOSTIC.md`. No target-machine result was fabricated.
- Challenger–Defender lifecycle adjudication remains deferred until a real overlap decision is reached.

# Agent-Reach reference assessment

The Human identified `Panniantong/Agent-Reach` as an important source reference. The current upstream `main` was evaluated before target-machine diagnosis.

Current Agent-Reach channel registry contains 15 channels:

```text
GitHub
Twitter/X
YouTube
Reddit
Facebook
Instagram
Bilibili
XiaoHongShu
LinkedIn
Xiaoyuzhou
V2EX
Xueqiu
RSS
Exa Search
Web
```

Do not use historical/translated documentation as current channel authority when it diverges from the current registry/root Skill.

## Existing overlap / external-knowledge strengths

Already modeled by `external-knowledge` at capability level:

- general web search;
- ordinary web reading;
- GitHub-native retrieval;
- Exa precision search.

Current `external-knowledge` also has first-class capabilities/semantics not equivalently represented by the Agent-Reach registry:

- `docs.versioned/context7`;
- `wechat.discovery`;
- `wechat.reader`;
- `complex-web.read` with Firecrawl as an extraction challenger;
- explicit capability/provider/exposure/operational-status/coverage/discoverability separation.

Agent-Reach Jina Reader is therefore a candidate provider for an existing web-read capability, not automatically a new capability. Agent-Reach's use of Exa as general search versus `external-knowledge` using Exa as a precision challenger is a routing-policy difference, not a missing provider.

## Source-semantic gaps to observe during diagnosis

The current map does not yet model these Agent-Reach source semantics as first-class capabilities:

1. Twitter/X discovery/read;
2. Reddit community search/post/comment read;
3. YouTube search/metadata/subtitle/comment/transcript paths;
4. RSS/Atom feed read;
5. XiaoHongShu search/read/comments;
6. Bilibili search/metadata/subtitle/transcription paths;
7. V2EX topic/reply/user/community access;
8. LinkedIn profile/company/job discovery;
9. Xueqiu quote/search/hot-content access;
10. Xiaoyuzhou podcast transcription;
11. Facebook and Instagram read/search surfaces.

This is 11 gap groups covering 12 Agent-Reach channels because Facebook and Instagram are grouped. It is not an independent-provider count.

Several paths share OpenCLI/Chrome or other common control planes. Shared underlying execution/failure domains must not be counted as independent retrieval capability merely because platform names differ.

## Agent-Reach normalization

Treat `agent-reach` as a router/installer/doctor/carrier, not as an independent retrieval provider by itself.

Actual execution may be owned by upstream paths such as:

```text
OpenCLI
twitter-cli
rdt-cli
bili-cli
yt-dlp
gh
Jina Reader
Exa via mcporter
public platform APIs
```

Normalize carrier → independent execution surface before judging capability overlap or redundancy.

# Effective decisions and invariants

1. GitHub repository state is durable project authority; a machine-local Skill is a deployment carrier/copy, not repository authority.
2. Runtime routing follows concrete information need/source semantics and uses the minimum retrieval needed for a reliable answer.
3. `UNKNOWN` is not `MISSING_CONFIRMED`.
4. Skill/carrier `DISCOVERED` is not provider `AVAILABLE`.
5. Capability `DECLARED_ONLY` is not provider `AVAILABLE`.
6. `UNCLASSIFIED` means attribution is unknown, not that the Skill has no external-knowledge capability.
7. Provider operational availability, semantic coverage, source discoverability, and source-semantic fit remain separate axes.
8. Carrier/registration/config/package evidence must not be double-counted as an independent execution surface.
9. One inspected Skill root does not prove machine-wide absence when other supported roots remain outside the inspected authority.
10. Retrieval/diagnosis and environment mutation are separate phases.
11. A safe command artifact/probe may show executable health, but substantive capability `AVAILABLE` requires runtime exposure or representative evidence appropriate to the capability claim.
12. No broad benchmark or synthetic battle is needed merely to fill the matrix.

# Implemented diagnostic mechanism

Candidate branch includes:

```text
references/capability-map.md
references/machine-diagnostics.md
scripts/scan_skills.py
scripts/machine_report.py
```

The diagnostic model is intentionally layered:

```text
PASSIVE_INVENTORY
  -> Skill/path/command/registration presence

SAFE_EXEC_PROBE
  -> only bounded read-only probes whose result can change operational classification
  -> do not infer AVAILABLE from static presence

REPRESENTATIVE_READ_PROBE
  -> only when the capability is decision-relevant and a safe representative read/search can distinguish availability/quality

PROVISIONING
  -> separate future phase requiring explicit authorization
```

Agent-Reach's ordered-backend and `active_backend` diagnostics are useful evidence, but their status values must not be copied mechanically into `external-knowledge` operational status when the underlying probe scope differs.

# Human authorization — target-machine read-only diagnosis

The Human has now authorized the next phase: perform the first real target-machine diagnosis **through the authorized Agent/Coordinator execution surface and GitHub handoff**.

This authorization includes read-only local/runtime inspection and bounded read-only probes needed to establish the current machine capability map. It does not authorize provisioning or credential/session mutation.

The Human is not the default repository or machine operator for this phase. Routine repository mechanics and diagnostic execution belong to the authorized Coordinator/Agent when reachable.

# Target-machine diagnostic execution contract

## 1. Authority and branch freshness

Before consequential repository writes, re-read:

- this task contract;
- current remote head of `task/20260912-001-v04-capability-diagnostics`;
- Issue #2 as the derived routing/status pointer;
- PR #3 only where review state is relevant.

Respect current writer/head ownership. If the branch has advanced unexpectedly, inspect the decision-relevant delta before writing; do not force-update or overwrite.

## 2. Inspect only real supported execution surfaces

Identify the actual Skill roots/runtime exposure surfaces available to the current target-machine Agent from current supported configuration/documentation/runtime state.

Do not scan arbitrary drives or invent speculative Skill roots for completeness.

Use `scripts/scan_skills.py` on the actual supported roots that are decision-relevant.

Record:

- roots actually inspected;
- roots unavailable/outside current authority;
- discovered Skill carriers;
- explicit capability sidecar claims when present;
- `UNCLASSIFIED` Skills without invented attribution.

## 3. Provider/runtime evidence

Use the existing `external-knowledge` Doctor/runtime evidence model for currently modeled providers.

Where a provider has only static presence, preserve `UNKNOWN` unless existing scoped absence evidence proves `MISSING_CONFIRMED` or bounded runtime evidence establishes a stronger state.

A command that exists but fails a safe executable probe may be reported as broken/unusable evidence, but do not invent a new global status taxonomy unless it is necessary to represent an observed reachable state. Map the evidence into the existing operational state with the concrete failure note where possible.

## 4. Agent-Reach evidence when actually installed

If Agent-Reach is present on the target machine, the Coordinator may run its existing read-only `agent-reach doctor --json` and record:

- Agent-Reach version/identity when directly observable;
- each channel status;
- ordered backend list when reported;
- `active_backend` when reported;
- channels left unverified by Agent-Reach Doctor;
- shared backend/failure-domain relationships that affect independence.

Do not install/update Agent-Reach, configure channels, import cookies, log in, or read/export browser cookies/session secrets during this phase.

Do not treat an Agent-Reach channel as an independent provider when its execution is actually delegated to a shared upstream backend.

If Agent-Reach is absent, record scoped absence only for the execution surface actually checked; do not install it.

## 5. Bounded representative probes

A representative read/search probe is allowed only when all are true:

- the relevant provider is already configured/exposed without mutation;
- the probe is read-only and safe under the current runtime;
- a concrete operational/quality unknown remains;
- the result can change capability status, routing judgment, or the next authorization.

Do not log in, solve CAPTCHA, import credentials, change proxy/TLS, start provisioning, or fan out probes merely for reassurance.

## 6. Machine Capability Receipt

Generate the candidate machine receipt with `scripts/machine_report.py` where its inputs are valid.

Do not let Skill carrier/claim evidence upgrade Doctor operational status.

For Agent-Reach channels not yet represented in the current adapter, retain them in the diagnostic report as observed/unmodeled source-semantic evidence rather than forcing them into an unrelated existing capability.

# Required durable outputs

Write and push:

```text
reports/TASK-20260912-001-MACHINE-DIAGNOSTIC.md
evidence/TASK-20260912-001-machine-capability-receipt.json
```

The JSON receipt may contain only non-secret, sanitized machine capability evidence. If a raw tool output contains sensitive material or unnecessary machine-identifying detail, do not commit it; summarize the minimum evidence in the report instead.

The diagnostic report must include:

- exact target-machine/runtime scope actually inspected;
- Skill roots actually inspected;
- discovered external-knowledge-relevant Skills/carriers;
- Agent-Reach presence and scoped doctor evidence if present;
- provider/exposure evidence for currently modeled capabilities;
- capability operational status under existing semantics;
- observed/unmodeled source-semantic channels;
- shared provider/control-plane/failure-domain notes where decision-relevant;
- remaining true capability gaps after real machine evidence;
- which gaps are only `UNKNOWN`, not confirmed missing;
- exact next authorization needed if any capability requires provisioning/configuration;
- explicit confirmation that no environment mutation/provisioning was performed.

Do not commit cookies, tokens, secret environment-variable values, browser session data, or raw authentication material.

# Explicitly unauthorized in this phase

Do not:

- install, update, repair, or remove providers/Skills;
- modify MCP configuration, PATH, shell profiles, proxies, TLS, browser configuration, or runtime settings;
- log in to services or import/export cookies/credentials;
- enable new browser extensions/services/background daemons;
- merge PR #3 or `main` merely because diagnosis completes;
- add all Agent-Reach channels to the adapter before machine evidence shows the required evolution decision;
- run broad benchmark matrices;
- begin Challenger–Defender competition without a real overlapping decision;
- infer machine-wide absence from one partial root/inventory.

# Diagnostic stop state

Stop when the first real target-machine capability receipt is durably pushed and the report distinguishes:

```text
what is actually available
what is available with scope/degradation
what remains unknown
what is blocked/unusable in the observed scope
what is confirmed missing only where absence authority is complete
what source-semantic channels are present but not yet modeled
what provisioning/configuration decision, if any, is now justified
```

Successful terminal state for this phase:

```text
READY_FOR_CAPABILITY_GAP_DECISION
```

Do not continue into provisioning or Challenger–Defender implementation in the same run.

# Later capability-evolution priority

Only after the real diagnostic shows genuine gaps should later capability evolution consider the current priority order:

```text
P1: Twitter/X, Reddit, YouTube/transcript, RSS
P2: XiaoHongShu, Bilibili, V2EX
P3: LinkedIn, Xueqiu, Xiaoyuzhou
P4: Facebook, Instagram (task-driven only)
```

This priority does not authorize installation. Real machine evidence and actual workload need decide which candidate, if any, proceeds.

# Current stop / next action

The target-machine read-only diagnosis was executed on 2026-09-12 through the authorized ZCode session surface. Results:

- `reports/TASK-20260912-001-MACHINE-DIAGNOSTIC.md` — full diagnostic report;
- `evidence/TASK-20260912-001-machine-capability-receipt.json` — machine capability receipt (`environment_mutation_attempted = false`).

Headline machine evidence: `general-web.search`, `general-web.read`, `docs.versioned`, `github.semantic` are AVAILABLE (EQUIVALENT, live-session runtime evidence); `complex-web.read` is AVAILABLE_WITH_SCOPE (native DEGRADED path; Firecrawl challenger UNKNOWN in observed scope); `wechat.discovery` is MISSING_CONFIRMED (adapter-bound local provider package absent from its path — a real regression vs. the 2026-08-22 observation); `wechat.reader` and `precision.search` remain UNKNOWN; 187 Skill carriers discovered across 6 explicit roots with 0 explicit capability sidecar claims; Agent-Reach carrier artifacts are present but its CLI execution surface is absent from the inspected PATH scope, so its doctor was not runnable. No provisioning, configuration, login, or environment mutation was performed.

Terminal state for this phase reached:

```text
READY_FOR_CAPABILITY_GAP_DECISION
```

The next action belongs to the Human/capability-gap decision: choose among the provisioning/re-bind options recorded in the diagnostic report §9. No provisioning authorization is granted by this state.
