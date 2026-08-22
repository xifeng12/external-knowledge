# Evidence: WeChat Article Discovery Real Case

**Evidence ID**: WECHAT-DISCOVERY-REAL-1
**Date**: 2026-08-22
**Runtime**: ZCode (skill runtime), external-knowledge v0.3-beta.1 instrumented session
**Evidence strength**: `OBSERVED_IN_RUNTIME` + `REPEATED_ACROSS_CASES` (multi-round observations), `SCOPE_LIMITED` (WeChat article discovery only), one item `UNRESOLVED` (exact-title specialist probe `total=0` root cause).

## Case

查找微信文章《ArcPy使用之一：SDE数据定时备份》，公众号：图说新语。

## Goal

Locate a specific WeChat article by title and publisher via external retrieval.

## Runtime

- ZCode skill runtime, 2026-08-22.
- Deterministic read-only Doctor and planner run per v0.3-beta.1 setup flow (`tests/zcode-v0.3-beta.1.md`).
- No environment mutation performed during the case.

## Source semantic

`WeChat article discovery` — locating a specific article owned by a specific WeChat Official Account.

## Capability

`complex-web.read` with source semantic `WeChat article discovery` (specialized discovery, not general web read).

## Provider

- Primary: `wechat-article-search` specialist.
- Fallback: general web search (`site:mp.weixin.qq.com` + varied queries).

## Execution surface

- Carrier: `SKILL.md` / skill directory (`~/.codex/skills/wechat-article-search/`).
- Execution surface: local script `scripts/search_wechat.js`.
- Runtime dependencies: Node, cheerio.
- Network backend: `weixin.sogou.com`.
- Adapter exposure contract at the time of the case: **did not declare** the local-script execution surface (`adapters/zcode-*.json` missing the provider entry) → provider status observed as `UNKNOWN` before direct probing.

## Observed behavior

- Representative probe, provider 端到端正常运行 (end-to-end OK), returns structured JSON.
- **exact-title-like query → `total=0`** (specialist direct call).
- General web fallback, repeated observation across multiple rounds:
  - target article zero hits across materially different queries;
  - `site:mp.weixin.qq.com` could not surface the target;
  - materially different queries returned fully/highly identical Top-N;
  - user finally supplied the real article link, proving the content exists.

## Failure / limitation

Two independent problems coexisted (causal correction — do not collapse into one):

- **A. Exposure visibility defect**: provider was actually runnable, but the adapter had not declared its execution surface → provider remained `UNKNOWN` at inventory time. Once directly probed, provider resolved to `AVAILABLE`.
- **B. Retrieval-quality limitation**: after direct specialist invocation, exact-title-like query still returned `total=0`. Root cause of the zero-hit specialist result: **UNRESOLVED**.

## Architecture implication

- `Operational Status ≠ Semantic Coverage ≠ Source Discoverability` — three independent axes; a provider can be `AVAILABLE` while discovery is limited.
- `AVAILABLE` must not be read as "will find the article". Verified on the specialist (AVAILABLE + EQUIVALENT coverage + `LIMITED_OBSERVED` discoverability) and on general web fallback (`AVAILABLE` + `DEGRADED` coverage + `VERY_LOW_OBSERVED` discoverability for this source semantic).
- Retrieval-quality signal formed: `LOW_QUERY_DISCRIMINATION` — materially different queries + Top-N highly/fully identical + results semantically irrelevant → `STOP` repeated query rewriting.
- Capability presence must be judged independently of provider inventory state (`Provider missing ≠ Capability missing`).

## Evidence strength

| Claim | Label |
|---|---|
| Specialist provider end-to-end runnable, returns structured JSON | `OBSERVED_IN_RUNTIME` |
| Specialist exact-title-like probe `total=0` | `OBSERVED_IN_RUNTIME`; root cause `UNRESOLVED` |
| General web fallback zero-hit / identical Top-N across materially different queries | `REPEATED_ACROSS_CASES` (multi-round) |
| Discoverability limits apply to `WeChat article discovery` | `SCOPE_LIMITED` — not generalized to other source semantics |

## What this does NOT prove

- NOT: "Bing is globally bad" / "general web is globally bad".
- NOT: `AVAILABLE` provider implies a specific article is retrievable.
- NOT: `LOW_QUERY_DISCRIMINATION` is a universal gate for every retrieval task.
- NOT: a universal discoverability taxonomy valid for all runtimes.

## STOP decision

`LOW_QUERY_DISCRIMINATION` observed (materially different queries, identical Top-N, semantically irrelevant results) → stop repeated query rewriting; do not fabricate fixtures or further probe to force a hit. Ambiguity rule: contextual rewrite at most once; if mismatch persists → STOP; clarify with the user only when context cannot resolve ambiguity.