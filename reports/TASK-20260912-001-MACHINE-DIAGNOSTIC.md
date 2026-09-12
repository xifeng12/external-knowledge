# TASK-20260912-001 — Target-Machine Capability Diagnostic Report

## State

`READY_FOR_CAPABILITY_GAP_DECISION`

- Execution branch: `task/20260912-001-v04-capability-diagnostics`
- Authority head at execution start: `6a6fdf8c3ab409726000f56157e20f44a7a8c331` (re-verified unchanged immediately before the diagnostic writes; no concurrent writer observed)
- Machine Capability Receipt: `evidence/TASK-20260912-001-machine-capability-receipt.json`
- Contract: `tasks/TASK-20260912-001-SEARCH-CAPABILITY-EVOLUTION.md` (§ Target-machine diagnostic execution contract)
- `environment_mutation_attempted = false` in every produced artifact

## 1. Target-machine / runtime scope actually inspected

One scope was inspected: the live ZCode CLI session on the Windows host through which this
diagnosis was executed (the authorized Coordinator/Agent surface per Issue #2).

```text
date                2026-09-12 (UTC)
OS                  Windows 10.0.26200 x64
shell               Git Bash (session process)
runtime             ZCode CLI agent session (native tools + session MCP tool manifest)
python              3.12.7 (host PATH)
node                v24.13.1 (host PATH)
```

Inspection surfaces used:

- the session's native tool manifest (native `WebSearch` / `WebFetch` exposure);
- the session's MCP tool manifest (which MCP servers are actually exposed to this agent);
- current-process PATH command resolution (read-only `command -v` probes);
- declared filesystem paths from the adapter (read-only existence checks);
- read-only execution of the repository's own diagnostic scripts
  (`scripts/scan_skills.py`, `scripts/doctor.py`, `scripts/machine_report.py`).

Not inspected: other agent runtimes' live sessions (Claude Code, Codex, OpenCode),
global/project MCP configuration files beyond the session manifest, environment-variable
values, browser profiles, cookies, or any network endpoints.

## 2. Skill roots actually inspected

Six explicit roots were scanned with `scripts/scan_skills.py` (read-only, frontmatter +
sidecar only, no skill code executed):

```text
root                              exists   carriers found
~/.agents/skills                  yes      1
~/.zcode/cli/plugins/cache        yes     66
~/.codex/skills                   yes     12
~/.claude/skills                  yes     64   (each skill appears ~3x: versioned dirs)
E:/cs1/.opencode/skills           yes     43   (system/installed/custom/archived zones)
~/.agent-reach                    yes      1   (tools/wechat-article-for-ai)
```

Roots probed and confirmed absent (not scanned):

```text
~/.zcode/cli/skills        absent
~/.config/opencode/skills  absent
~/.opencode/skills         absent
```

Roots outside current authority (deliberately not scanned): arbitrary drives and any
location not a real supported/used Skill registry of this machine. Absence conclusions
below are scoped to the roots and surfaces listed here.

Summary: **187 Skill carriers discovered, 0 explicit capability sidecar declarations**
(`external-knowledge.json` found at none of them), so all 187 are
`capability_attribution = UNCLASSIFIED` in the receipt. No attribution was invented.

## 3. Discovered external-knowledge-relevant carriers

Name-based factual observation only; all remain `UNCLASSIFIED` pending human review.
Zone status per path (`system` / `installed` / `custom` / `archived` under
`E:/cs1/.opencode/skills`; user-level dirs otherwise):

```text
carrier                 zone / root                     relevance observation (not attribution)
agent-reach             system, workspace               SKILL.md description claims 13+ platform
                                                        channels; execution surface it references is
                                                        the `agent-reach` CLI (see §4)
agent-fetch             installed, workspace            name suggests external fetch; unverified
web-access              installed, workspace            name suggests web retrieval; unverified
chrome-cdp              archived, workspace             Chrome/CDP control carrier, archived
yt-dlp-downloader       installed, workspace            name suggests YouTube download semantics
微信读书                 custom, workspace               name suggests WeChat Read semantics
markdown-proxy          archived, workspace             archived carrier (weixin fetch script dir)
music-downloader        custom + archived, workspace    media retrieval carriers
knowledge-base / ima-skill / summarize   custom         name-level relevance only
wechat-to-md            ~/.agent-reach/tools/           Python tool bundle (main.py, mcp_server.py,
wechat-article-for-ai                                    cli.py, requirements.txt, SKILL.md)
browse / setup-browser-cookies  ~/.claude/skills        browser read / credential-adjacent setup
                                                        carriers (not opened, not executed)
openai-docs             ~/.codex/skills                 name suggests docs retrieval
computer-use / control-browser / web-gui-tester  ~/.zcode plugin cache (active in session manifest)
```

`setup-browser-cookies` was recorded as discovered only; it was not opened, run, or used
to read any credential material.

## 4. Agent-Reach presence and scoped doctor evidence

Agent-Reach is **partially present as carrier artifacts; its execution surface is absent
from the inspected scope.**

```text
agent-reach CLI         ABSENT from current process PATH
opencli                 ABSENT from current process PATH
mcporter                ABSENT from current process PATH
E:/cs1/.opencode/skills/system/agent-reach/SKILL.md   PRESENT (carrier)
~/.agent-reach/config.yaml                            PRESENT (keys observed: bilibili_proxy,
                                                      reddit_proxy; values NOT read)
~/.agent-reach/tools/wechat-article-for-ai            PRESENT (tool bundle)
```

Because no `agent-reach` execution surface resolves, `agent-reach doctor --json` was **not
run** (it cannot run in the observed scope). No install, update, channel configuration,
login, or cookie import/export was attempted, per contract. Scoped absence is recorded for
the current-process PATH only; an Agent-Reach CLI installed outside PATH resolution (for
example via an npm prefix not on this PATH) is **not** ruled out — this remains UNKNOWN.

The skill carrier's description claims platform channels (Twitter/X, Reddit, YouTube,
Bilibili, XiaoHongShu, Douyin, WeChat Articles, LinkedIn, RSS, Exa, web). Per contract,
carrier description claims are **not** provider evidence; they are listed in §7 as
observed/unmodeled semantics.

## 5. Provider / exposure evidence and capability operational status

Doctor run: `python scripts/doctor.py --adapter adapters/zcode-v0.3-beta.1.json
--agent-inventory <session inventory> --output <doctor-report.json>`

Runtime evidence source for `AVAILABLE` states is the live session manifest / in-session
representative execution, as recorded in the receipt; Doctor operational status is sourced
from the Doctor report only (Skill carriers could not and did not upgrade it).

```text
capability           status                best provider                coverage
general-web.search   AVAILABLE             runtime-native.web-search    EQUIVALENT
general-web.read     AVAILABLE             runtime-native.webfetch      EQUIVALENT
docs.versioned       AVAILABLE             context7                     EQUIVALENT
github.semantic      AVAILABLE             gh-cli                       EQUIVALENT
complex-web.read     AVAILABLE_WITH_SCOPE  runtime-native.webfetch      DEGRADED
wechat.reader        UNKNOWN               —                            UNKNOWN
precision.search     UNKNOWN               —                            UNKNOWN
wechat.discovery     MISSING_CONFIRMED     —                            NOT_APPLICABLE
```

Provider-level notes:

- `gh-cli`: command PRESENT (gh 2.87.3) **plus** representative runtime execution in this
  session (`gh repo view`, `gh issue view` succeeded against the task repo). Satisfies
  invariant 11 (runtime exposure + representative evidence), not command presence alone.
- `context7`: MCP server exposed in the live session manifest (resolve-library-id,
  query-docs). No queries were fanned out during diagnosis.
- `runtime-native.web-search` / `runtime-native.webfetch`: native tools exposed in the
  live session manifest.
- `firecrawl` (complex-web.read challenger): `firecrawl` command ABSENT, and the adapter
  declares `absence_authoritative` for PATH only — the MCP exposure class remains
  uncovered, so the provider is **UNKNOWN**, not MISSING_CONFIRMED. The capability stays
  AVAILABLE_WITH_SCOPE through the native DEGRADED webfetch path.
- `wechat-article-search` (wechat.discovery): adapter-bound path
  `~/.codex/skills/wechat-article-search/scripts/search_wechat.js` is **ABSENT**
  (authoritative for its `local_script` exposure class, which is the only legal class).
  Provider and capability are **MISSING_CONFIRMED** for the observed scope. This is a real
  regression vs. the 2026-08-22 OBSERVED_IN_RUNTIME record in
  `references/runtime-notes-zcode.md`: the package no longer exists at its bound path and
  no wechat-named carrier was found in any inspected root.

## 6. Shared control-plane / failure-domain notes

- `agent-reach` carrier normalizes to a router/installer over upstream backends
  (opencli/CLIs/Jina/Exa per the task contract); even if provisioned, its channels must not
  be counted as independent providers. The `~/.agent-reach/config.yaml` bilibili/reddit
  proxy keys indicate two channels would additionally share a proxy failure domain.
- `wechat-to-md` and any future WeChat reader share network egress and
  WeChat-anti-bot failure domains; they are not independent of each other for redundancy.
- `chrome-cdp` (archived), `control-browser`, `computer-use`, `web-gui-tester` all ride a
  shared browser/desktop control plane; they are one practical failure domain, not several
  retrieval providers.
- `gh-cli` is independent of the native web tools (separate process, auth, and rate-limit
  domain). `context7` MCP is independent of native web read.

## 7. Observed / unmodeled source-semantic channels

Present on the machine but not modeled in the current adapter (kept out of existing
capabilities per contract §6):

1. **Agent-Reach channel semantics** (carrier-claimed, execution surface absent):
   Twitter/X, Reddit, YouTube, Bilibili, XiaoHongShu, Douyin, WeChat Articles, LinkedIn,
   RSS, Exa-as-general-search — claimed by the `agent-reach` system-skill description.
2. **wechat-to-md** (`~/.agent-reach/tools/wechat-article-for-ai`): a concrete local
   Python wechat-article→markdown tool bundle including `mcp_server.py`. Static presence
   only; operational status UNKNOWN (not executed; dependencies unverified; unmodeled).
3. **Browser automation surfaces**: live-session MCP/plugin exposure of `control-browser`
   (Browser Use), `computer-use`, `web-gui-tester`, plus archived `chrome-cdp`. These can
   read JS-heavy pages and are a plausible future provider/challenger for
   `complex-web.read`, but are unmodeled and were not probed.
4. **yt-dlp-downloader / 微信读书 / agent-fetch / web-access / openai-docs**: name-level
   observations only; attribution intentionally not assigned.

## 8. Stop-state classification

```text
actually available
    general-web.search, general-web.read, docs.versioned, github.semantic
    (all EQUIVALENT, live-session runtime evidence)

available with scope/degradation
    complex-web.read — native webfetch only (DEGRADED); extraction challenger
    (Firecrawl) unconfirmed in the observed scope

unknown (true UNKNOWN, absence not established)
    wechat.reader (weixin-articles-reader MCP)
    precision.search (Exa via MCP/mcporter/other scopes)
    firecrawl via MCP class
    Agent-Reach CLI presence outside PATH resolution
    operational state of every UNCLASSIFIED carrier listed in §3/§7

blocked/unusable in the observed scope
    agent-reach carrier execution (CLI absent; doctor not runnable; no channel
    verification possible without provisioning)

confirmed missing (absence authority complete for the binding)
    wechat.discovery — adapter-bound local_script path absent; single legal
    exposure class fully covered by authoritative absence

present but not yet modeled
    wechat-to-md tool bundle; Agent-Reach channel claim set; browser automation
    surfaces; the remaining name-relevant carriers in §3
```

## 9. Provisioning / configuration decisions now justified (for the Human — none executed)

1. **wechat.discovery (MISSING_CONFIRMED)** — a real capability regression. Decision
   needed between: (a) re-provision the `wechat-article-search` local provider package at
   its adapter-bound path; (b) re-bind the adapter to an existing observed carrier
   (`wechat-to-md` / Agent-Reach tooling) after evaluation; or (c) drop the capability.
   Option (b) would first need a bounded probe authorization for
   `~/.agent-reach/tools/wechat-article-for-ai` (local Python execution) plus its own
   attribution sidecar/human review.
2. **Optional evidence-tightening authorizations** (all currently UNKNOWN by design):
   inspect additional MCP configuration scopes for `weixin-articles-reader` / `exa` /
   `firecrawl`; authorize one representative Exa search probe if an existing exposure is
   found. Each is cheap but only worth authorizing if the capability is decision-relevant.
3. **Agent-Reach CLI** — provisioning (e.g. `npm install`) would activate the carrier's
   channel router; explicitly **not** requested as a default, because the 11 Agent-Reach
   gap groups should be prioritized (P1: Twitter/X, Reddit, YouTube/transcript, RSS) only
   against real workload need, per the contract's later-evolution priority.

No provisioning, provider installation/repair/configuration, login/cookie import, MCP/PATH/
runtime mutation, PR merge, or Challenger–Defender execution was performed in this phase.

## 10. Environment mutation confirmation

```text
environment_mutation_attempted = false   (skill inventory, doctor report, receipt)
```

Writes in this phase were limited to the repository's required durable outputs (this
report, the receipt JSON, and the task-contract status update). Diagnostic intermediates
were kept outside the repository.
