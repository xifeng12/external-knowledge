# Agent-Reach Channel Assessment — 2026-09-12

## Scope

This assessment compares the current `external-knowledge` v0.4 candidate against the current upstream `Panniantong/Agent-Reach` repository before target-machine diagnosis.

Evidence baseline:

- Agent-Reach `main` observed head: `da5044d26fc6adddb6554d5679c94ac22e76e428` (2026-09-01).
- Latest published Agent-Reach release observed: `v1.5.0` (2026-06-11).
- Current Agent-Reach channel registry contains 15 channels: GitHub, Twitter, YouTube, Reddit, Facebook, Instagram, Bilibili, XiaoHongShu, LinkedIn, Xiaoyuzhou, V2EX, Xueqiu, RSS, Exa Search, Web.
- The current authoritative Chinese README / `agent_reach/skill/SKILL.md` does not list WeChat Articles as one of the 15 channels. Some translated/historical docs still mention WeChat; those are not used as current channel authority.

The comparison is by source semantic and independent execution path, not by marketing channel count.

## Current overlap

| Source / need | external-knowledge | Agent-Reach | Assessment |
|---|---|---|---|
| General web search | `general-web.search` + `precision.search/exa` | Exa Search | Covered; routing policy differs. External-knowledge keeps native general search as owner and Exa as a precision challenger. |
| Known web page reading | `general-web.read/runtime-native.webfetch` | Jina Reader + optional web-reader MCP | Covered at capability level; Jina is a provider candidate, not automatically a missing capability. |
| Complex extraction | `complex-web.read` + Firecrawl | Jina/web-reader oriented | external-knowledge has a stronger explicit extraction-challenger model. |
| GitHub | `github.semantic/gh-cli` | GitHub / gh CLI | Covered. Agent-Reach contributes stronger local executable-health probing. |
| Versioned technical docs | `docs.versioned/context7` | No equivalent first-class channel | external-knowledge-only specialist. |
| WeChat discovery/read | `wechat.discovery`, `wechat.reader` | Not in current 15-channel authority | external-knowledge-only specialist in the compared current baseline. |

## Real channel gaps relative to Agent-Reach

The following current Agent-Reach source semantics are not first-class capabilities in external-knowledge:

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
11. Facebook and Instagram read/search surfaces (login-dependent OpenCLI paths).

This is 11 capability/source-semantic gaps, not 11 independent backend families. Several Agent-Reach platforms share OpenCLI and therefore share an execution/control-plane failure domain.

## Do not count these as independent gaps

### Agent-Reach itself

`agent-reach` is a router/installer/doctor carrier. Most retrieval is performed by upstream execution surfaces (`opencli`, `twitter`, `rdt`, `bili`, `yt-dlp`, `gh`, Jina, Exa via mcporter, direct APIs, etc.). Do not model `agent-reach` plus those upstream tools as independent retrieval providers.

### OpenCLI platform count

OpenCLI can serve multiple platform semantics, but one OpenCLI/Chrome failure can affect many of them. Platform breadth must not be presented as independent failure-domain diversity.

### Jina Reader

Jina is a useful low-friction ordinary web reader provider candidate. It is not a new information capability when `general-web.read` is already viable. Add or challenge only if a real reading/extraction decision exists.

### Exa

Exa already exists in external-knowledge as `precision.search`. Agent-Reach treats it as its web-search channel. This is a routing-policy difference, not a missing provider.

## Diagnostic-method gap

Agent-Reach v1.5 introduced a useful behavior that external-knowledge does not yet fully have: lightweight executable probes to distinguish "command exists" from "command is actually runnable" and an `active_backend` chosen from ordered candidates.

External-knowledge currently has the stronger evidence model:

- capability != provider;
- carrier != independent exposure;
- `UNKNOWN` != `MISSING_CONFIRMED`;
- operational availability != semantic coverage != discoverability;
- machine receipt != repository map.

But its Doctor is deliberately passive: local command/path presence plus supplied runtime inventory. Therefore a stale/broken CLI can remain `UNKNOWN` unless an Agent runtime inventory or representative probe is supplied.

### Minimum diagnostic improvement before broad provisioning

Add a bounded probe stage, not a general command runner:

1. `PASSIVE_INVENTORY` — Skill carriers, paths, command presence, config presence without secret values.
2. `SAFE_EXEC_PROBE` — only adapter-declared, read-only, bounded commands such as `tool --version`; suppress telemetry/update checks when the tool supports it. This may distinguish `PRESENT_BUT_BROKEN` from executable presence.
3. `REPRESENTATIVE_READ_PROBE` — only when the capability is decision-relevant; perform a real read/search request and require substantive output before `AVAILABLE` is claimed.
4. `PROVISIONING` remains separate and requires explicit authorization.

Do not promote all Agent-Reach doctor behavior wholesale: some channels intentionally avoid live remote validation, and external-knowledge should preserve scoped authority instead of converting every `warn/off` into a global provider state.

## Skill-diagnosis gap

The new v0.4 Skill scanner intentionally classifies an unknown third-party Skill as `UNCLASSIFIED` unless it has an explicit `external-knowledge.json` sidecar. Agent-Reach does not provide that sidecar.

Therefore target-machine diagnosis needs one of these evidence paths:

- a reviewed known-Skill profile for Agent-Reach; or
- ingestion of `agent-reach doctor --json` as scoped carrier/provider evidence.

The second path is preferable because it uses Agent-Reach's own current backend selection instead of inferring capabilities from its prose or package name.

## Priority for capability evolution

### P0 — required for useful target-machine diagnosis

- Recognize Agent-Reach as a carrier/orchestrator, not a provider.
- Accept its `doctor --json` result as scoped runtime evidence when it is actually installed and run.
- Add a safe executable-probe contract so static CLI presence is not the end state.
- Keep the current external-knowledge operational/coverage/discoverability axes authoritative.

### P1 — high-value general research gaps

- Twitter/X.
- Reddit.
- YouTube/transcript.
- RSS.

These add source semantics that general web search does not reliably replace.

### P2 — high-value Chinese/community gaps

- XiaoHongShu.
- Bilibili.
- V2EX.

These are source-specific ecosystems and should not be collapsed into general Chinese web search.

### P3 — specialized workload gaps

- LinkedIn/jobs.
- Xueqiu/market social content.
- Xiaoyuzhou podcast transcription.

Admit when the workload requires them; do not install merely to make the matrix complete.

### P4 — login-heavy optional gaps

- Facebook.
- Instagram.

Keep as optional until a real task requires them. Both rely on authenticated browser-session paths in the current Agent-Reach design.

## Overall channel map after comparison

The durable target map should be broader than Agent-Reach but not duplicate it:

```text
General backbone
  - general web search
  - ordinary web read
  - complex extraction

Technical specialists
  - versioned docs
  - GitHub

Chinese/content ecosystems
  - WeChat
  - XiaoHongShu [candidate]
  - Bilibili [candidate]
  - V2EX [candidate]

Global social/community
  - Twitter/X [candidate]
  - Reddit [candidate]
  - Facebook [optional candidate]
  - Instagram [optional candidate]

Media/feeds
  - YouTube/transcript [candidate]
  - RSS [candidate]
  - Xiaoyuzhou/transcript [specialized candidate]

Career/finance
  - LinkedIn [specialized candidate]
  - Xueqiu [specialized candidate]

Precision/challengers
  - Exa
  - Firecrawl
```

## Stop / next diagnostic state

This assessment does not authorize installation or channel admission. The next decision-relevant action is a real target-machine diagnostic:

1. enumerate actual Skill roots;
2. identify whether Agent-Reach and other retrieval Skills are present;
3. if Agent-Reach is present, collect `agent-reach doctor --json` without installing/configuring anything;
4. collect local command/exposure evidence for the current external-knowledge providers;
5. produce the first Machine Capability Receipt;
6. only then decide which P1/P2/P3 gaps are genuinely missing on this machine.
