# Source Ownership — Runtime Retrieval v0.3-beta.1

| Information need | Preferred semantic owner | Gap / fallback rule |
|---|---|---|
| Current product plan/pricing/availability | Official/current web | For "what changed", obtain historical/change evidence; do not infer change from current state alone. |
| Current announcement/release/changelog | Official announcement/release | General web/precision challenger only when official source cannot be located sufficiently. |
| Versioned library/framework/SDK/API | Version-matched docs specialist | General/official web if unresolved or insufficient. |
| GitHub PR/issue/commit/repo history | GitHub-native specialist | General web may be degraded fallback; disclose source limitation. |
| WeChat article discovery | WeChat discovery specialist | General web is semantically degraded and has `VERY_LOW_OBSERVED` discoverability for this source semantic in repeated ZCode cases. Do not spend repeated query rewrites through it. |
| Canonical WeChat article read | WeChat reader specialist | Fallback only after an observed read gap; keep runtime-specific UA/fetch behavior in runtime notes, not portable contract. |
| General current fact | General web | Precision challenger only after observable precision/recall gap. |
| Known ordinary URL | Ordinary reader/fetch | Extraction challenger only after observed read/extraction gap. |

## Runtime boundary

A preferred specialist may be semantically high-fit while operationally `UNKNOWN`.
That does not make it `MISSING_CONFIRMED`.

A provider may be operationally available while source discoverability is limited. Do not conflate:

```text
callable
with
able to surface the target item
```

Read `retrieval-quality.md` when source-specific discovery quality affects routing.

## WeChat discovery evidence

Current ZCode evidence supports:

```text
wechat-article-search:
  Operational = AVAILABLE
  Discoverability = LIMITED_OBSERVED

general web fallback:
  Operational = AVAILABLE
  Semantic Coverage = DEGRADED
  Discoverability = VERY_LOW_OBSERVED
```

The specialist remains the preferred owner because it directly targets the WeChat ecosystem, but a zero-result specialist query does not prove the article does not exist.

## Discovery vs reader

Discovery and body reading are different phases.

If the user asks only to find candidates, useful candidate discovery is a valid STOP point.

If discovery fails but the user supplies a canonical WeChat URL, switch to reader mode only because the goal/evidence changed; do not fan out discovery providers after the link already resolves the identity.
