# TASK-20260912-002 — Evidence-Tightening Report: wechat.reader / Exa / Firecrawl UNKNOWNs

## State

`READY_FOR_BIND_AND_PROVISION_DECISION`

- Predecessor: `reports/TASK-20260912-001-MACHINE-DIAGNOSTIC.md` (terminal state `READY_FOR_CAPABILITY_GAP_DECISION`)
- Machine evidence: `evidence/TASK-20260912-002-evidence-tightening.json`
- Authorization in force: read-only / limited-execution evaluation of `wechat-to-md` (`~/.agent-reach/tools/wechat-article-for-ai`) plus evidence-tightening for the three UNKNOWNs. **No provider installation or configuration was performed.**
- Doctor re-aggregation was executed with the tightened evidence (`scripts/doctor.py`, adapter `zcode-v0.3-beta.1.json`); intermediates kept outside the repository.

## 1. Scope actually inspected (2026-09-12, Windows 10.0.26200 x64, ZCode session, python 3.12.7)

- `~/.agent-reach/tools/wechat-article-for-ai` bundle: full read of entry files + package; import and argparse-level safe execution probes.
- Live session MCP manifest (complete enumeration) + read-only parse of static MCP config domains: `~/.claude.json` (incl. per-project), `~/.claude/settings.json`, `~/.codex/config.toml`, `E:/cs1/opencode.json`, `~/.zcode/cli/config.json`. Server names only; secret values never read.
- PATH command resolution re-probes (`firecrawl`, `agent-reach`, `opencli`, `mcporter`); npm global prefix listing (single prefix scope); env-var existence-only checks (`EXA_API_KEY` / `FIRECRAWL_API_KEY` / `JINA_API_KEY`).
- Network read probes: `weixin.sogou.com` search endpoint; one `/link` redirect follow; one representative WeChat canonical-article read via the already-exposed `web_reader` MCP.
- Not inspected: other agent runtimes' live sessions, browser profiles/cookies, MCP_DOCKER gateway contents, other npm prefixes.

## 2. Tightened statuses (doctor v0.3-beta.1 semantics)

```text
capability           status                change      best provider / note
wechat.reader        MISSING_CONFIRMED     UNKNOWN ->  weixin-articles-reader: mcp class not exposed in the
                                           MISSING_    session manifest and unregistered in every inspected
                                           CONFIRMED   config domain (scoped absence; uninspected registration
                                                       mechanisms may still exist, e.g. MCP_DOCKER gateway)
precision.search     MISSING_CONFIRMED     UNKNOWN ->  exa: no exposure/registration anywhere inspected;
                                           MISSING_    EXA_API_KEY UNSET (existence-only)
                                           CONFIRMED
complex-web.read     AVAILABLE_WITH_SCOPE  unchanged   runtime-native.webfetch AVAILABLE (DEGRADED);
                                                       provider firecrawl MISSING_CONFIRMED (was UNKNOWN):
                                                       path_cli absence re-verified; mcp class unregistered;
                                                       FIRECRAWL_API_KEY UNSET
wechat.discovery     MISSING_CONFIRMED     unchanged   + new corroboration: sogou search endpoint REACHABLE
                                                       (real results, no CAPTCHA); /link redirect is
                                                       CAPTCHA-gated for automated clients (2nd anti-bot layer)
```

`UNKNOWN → MISSING_CONFIRMED` is **scoped** to the session manifest plus the inspected config domains, per capability-model §4 (L = declared legal classes fully covered by authoritative absence, P = ∅). It is not machine-wide absence.

## 3. wechat-to-md carrier evaluation (limited execution)

| Axis | Result |
|---|---|
| Carrier | PRESENT; git-versioned; SKILL.md/README complete; `main.py`/`mcp_server.py` shims over the `wechat_to_md` package |
| Python runtime deps | all 5 (`camoufox`, `markdownify`, `bs4`, `httpx`, `mcp`) importable — nothing to install |
| Executable health | `main.py --help` renders; all modules import OK |
| End-to-end | **BLOCKED**: Camoufox browser binary ABSENT (`%LOCALAPPDATA%\camoufox`); `scraper.py` has no non-browser path (`AsyncCamoufox` only); first run auto-downloads ~493 MB |
| MCP surface | `mcp_server.py` exposes `convert_article`/`batch_convert` but is registered in no inspected config domain |
| Semantic fit | strong for `wechat.reader` (URL→markdown, frontmatter, locally downloaded images); **not** a fit for `wechat.discovery` (no search function) |
| Failure domain | shares network egress + WeChat anti-bot domain with other WeChat read paths; not independent redundancy |

Conclusion: the bundle is a healthy, dependency-complete **re-bind candidate** for `wechat.reader`, gated on exactly one provisioning action (Camoufox browser fetch) before a representative probe can upgrade it.

## 4. Decisions (per the four authorized options)

1. **wechat.reader — 复用 + re-bind (conditional), no Challenger–Defender.**
   - Today, without any mutation: route canonical WeChat URL reads through the already-exposed `web_reader` MCP as the read fallback (per source-ownership: fallback after the declared specialist is absent — which it now is, scoped). Probe P7 demonstrates it returns title/author/full body in one call. Images degrade to `blob:`/remote URLs.
   - If specialist quality is needed (locally archived images, frontmatter, batch conversion): authorize **one** bounded provisioning step — `python -m camoufox fetch` (~493 MB, no package installs needed) → representative probe on one article → on success, re-bind `wechat.reader` to `wechat-to-md` as a `local_script` provider (carrier_class: tool bundle). Re-bind is justified by P1/P2 evidence; only the runtime gap blocks it today.
   - Challenger–Defender does not apply: the declared defender (`weixin-articles-reader`) is MISSING_CONFIRMED — there is nothing to compete against.

2. **Exa (`precision.search`) — 后续 provisioning (deferred), DO_NOT_INSTALL now.**
   - MISSING_CONFIRMED scoped; per setup-policy the precision challenger is entered only after an observed precision/recall gap, and per invariant 12 no provisioning pressure from status alone. Provisioning later requires: EXA_API_KEY acquisition + MCP registration — an explicit, separately-authorized step.

3. **Firecrawl — 不供给.**
   - `complex-web.read` is already AVAILABLE_WITH_SCOPE through the native DEGRADED path, and `web_reader` demonstrated WeChat-page extraction (P7) as an observed extraction-fallback channel. Recommendation: record `web_reader` as the observed extraction fallback / challenger-slot re-bind candidate (documentation-level adapter change, no runtime mutation) instead of provisioning Firecrawl. Firecrawl provisioning (CLI + API key + MCP) stays deferred until a real, repeated extraction gap that `web_reader` demonstrably fails.

4. **Challenger–Defender — not initiated.** No materially overlapping *operational* pair exists today (declared WeChat reader missing; Exa/Firecrawl missing). The only future CD candidate is `wechat-to-md` vs `web_reader` for WeChat reading, and only if the Camoufox provisioning above is authorized. Synthetic battles remain forbidden (invariant 12).

## 5. Environment mutation confirmation

```text
environment_mutation_attempted = inadvertent-only, immediately terminated, no persisted state
```

Incident (recorded for honesty): a Camoufox binary-presence check via `camoufox.pkgman.camoufox_path()` triggered the library's first-run auto-download (~493 MB). The background process was terminated at ~0.26 MB transferred; no artifact persisted (`%LOCALAPPDATA%\camoufox` holds only an empty `Cache` directory; the outer directory pre-existed). The machine is back to its pre-check state. Lesson recorded: pkgman path/verify calls are **not** read-only and must never run during diagnosis phases.

All repository writes in this phase are the two durable outputs (this report + the evidence JSON); no commit/push performed.

## 6. Next authorization needed (if any)

- **A (recommended, small):** `python -m camoufox fetch` at `~/.agent-reach/tools/wechat-article-for-ai` → representative probe → re-bind `wechat.reader` adapter binding to `wechat-to-md` (`local_script`).
- **B (optional):** adapter documentation update adding `web_reader` as observed extraction-fallback for `complex-web.read` (no runtime change).
- **C (deferred):** Exa provisioning (API key + MCP registration) — only upon a real observed precision/recall gap.
- **D (deferred):** Firecrawl provisioning — only upon a real observed extraction gap that `web_reader` fails.
- wechat.discovery re-provisioning remains the open decision from TASK-001 §9.1(a); P6 shows its backend is still healthy, which keeps option (a) viable.
