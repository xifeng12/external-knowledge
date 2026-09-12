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

## Agent-Reach channel assessment

The Human identified `Panniantong/Agent-Reach` as an important source reference and requested a full channel-gap assessment before the first real machine diagnostic.

### Compared authority

Observed upstream baseline:

```text
Panniantong/Agent-Reach
main = da5044d26fc6adddb6554d5679c94ac22e76e428
latest release = v1.5.0 (2026-06-11)
```

The current Agent-Reach channel registry contains 15 channels:

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

Current authoritative `main` / root Skill does not include WeChat Articles among these 15. Historical/translated documentation that still mentions WeChat is not treated as current channel authority.

### Overlap and external-knowledge-only strengths

Already covered at capability level:

- general web search;
- ordinary web reading;
- GitHub;
- Exa precision search.

`external-knowledge` additionally has first-class capabilities not represented equivalently in the current Agent-Reach channel registry:

- `docs.versioned/context7`;
- `wechat.discovery`;
- `wechat.reader`;
- `complex-web.read` with Firecrawl as an extraction challenger;
- formal separation of capability/provider/exposure/operational status/coverage/discoverability.

Agent-Reach's Jina Reader is therefore a provider candidate for an existing web-read capability, not automatically a new capability gap. Likewise, Agent-Reach uses Exa as its web-search channel while external-knowledge uses Exa as a precision challenger; that is a routing-policy difference, not a missing provider.

### Real source-semantic gaps relative to Agent-Reach

The current external-knowledge map does not yet model these Agent-Reach source semantics as first-class capabilities:

1. Twitter/X discovery and reading.
2. Reddit community search, post and comment reading.
3. YouTube search, metadata, subtitles/comments and transcript fallback.
4. RSS/Atom feed reading.
5. XiaoHongShu search/read/comments.
6. Bilibili search/metadata/subtitles/audio-to-transcript path.
7. V2EX topics/replies/user/community access.
8. LinkedIn profile/company/job discovery.
9. Xueqiu quote/search/hot-content access.
10. Xiaoyuzhou podcast transcription.
11. Facebook and Instagram read/search surfaces.

This is a source-semantic gap count, not an independent-provider count. Several of these channels share OpenCLI/Chrome and therefore share a control-plane/failure domain.

### Do not double-count Agent-Reach

`agent-reach` is a router/installer/doctor carrier. Retrieval is normally executed by upstream paths such as:

```text
opencli
twitter-cli
rdt-cli
bili-cli
yt-dlp
gh
Jina Reader
Exa via mcporter
direct public APIs
```

Therefore:

```text
Agent-Reach carrier + upstream execution surface
!= two independent providers
```

The current external-knowledge carrier/exposure model remains authoritative for this normalization.

### Diagnostic-method gap exposed by Agent-Reach

Agent-Reach v1.5 adds a useful behavior missing from the current external-knowledge Doctor: bounded executable health probes that can distinguish a command artifact from a runnable command and expose the currently selected ordered backend via `active_backend`.

External-knowledge is stronger at evidence semantics but currently more passive. Its Doctor relies on deterministic local presence plus supplied runtime inventory/representative evidence, so a stale or broken command may remain `UNKNOWN`.

Minimum diagnostic evolution before broad provisioning:

```text
PASSIVE_INVENTORY
  -> Skill/path/command/config presence only

SAFE_EXEC_PROBE
  -> adapter-declared read-only bounded commands only
  -> e.g. version/help probe with telemetry/update checks suppressed where supported
  -> may distinguish PRESENT_BUT_BROKEN from executable presence

REPRESENTATIVE_READ_PROBE
  -> only when a capability is decision-relevant
  -> require substantive read/search output before AVAILABLE

PROVISIONING
  -> separate phase, explicit authorization still required
```

Do not copy all Agent-Reach Doctor statuses directly into external-knowledge operational status. Agent-Reach itself sometimes deliberately avoids remote validation; external-knowledge must preserve scoped authority and `UNKNOWN` semantics.

### Skill-attribution gap before target-machine diagnosis

The v0.4 Skill scanner intentionally leaves third-party Skills `UNCLASSIFIED` unless an explicit `external-knowledge.json` sidecar exists. Agent-Reach does not ship that sidecar.

For Agent-Reach, the preferred future evidence path is therefore:

```text
Skill carrier discovered
  + agent-reach doctor --json actually executed
  -> translate scoped channel/backend evidence
```

rather than inferring capability from package name or prose.

### Priority after diagnosis

Do not install channels to fill a matrix. If the target machine proves the capability genuinely missing, current priority is:

```text
P1: Twitter/X, Reddit, YouTube/transcript, RSS
P2: XiaoHongShu, Bilibili, V2EX
P3: LinkedIn, Xueqiu, Xiaoyuzhou
P4: Facebook, Instagram (login-heavy; task-driven only)
```

Priority is for later capability evolution, not current provisioning authorization.

## Actual target-machine state

Still unknown.

This implementation creates the diagnostic mechanism but this ChatGPT execution surface has no direct access to the Human's Windows filesystem/Skill roots. Therefore no target-machine Skill inventory or Machine Capability Receipt has been fabricated.

The first real target-machine run should use only actual supported Skill roots. For example, if `~/.codex/skills` is a real root on that machine:

```bash
python scripts/scan_skills.py --root ~/.codex/skills --pretty --output skill-inventory.json
```

If Agent-Reach is discovered and its CLI is installed, collect its own scoped channel receipt without installing or configuring anything:

```bash
agent-reach doctor --json
```

Then obtain provider/runtime evidence for the external-knowledge adapter and merge:

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
- Agent-Reach doctor JSON ingestion/translation;
- bounded SAFE_EXEC_PROBE support in external-knowledge Doctor;
- broad benchmark matrices;
- generic Skill evaluation framework duplicated from `skill-forge`;
- Challenger–Defender lifecycle adjudication;
- synthetic battle fixtures.

The first real overlap remains `complex-web.read` (`runtime-native.webfetch` vs `firecrawl`), but a battle should begin only when a reachable real extraction decision exists and both relevant paths have decision-changing evidence.

## Stop state

Repository implementation plus Agent-Reach channel assessment is complete for this phase and remains ready for review.

Next decision-relevant action is the first real target-machine diagnostic. No provisioning authorization is currently requested.
