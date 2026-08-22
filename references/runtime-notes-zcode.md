# ZCode Runtime Notes — external-knowledge v0.3-beta.1

These are runtime-scoped observations, not portable hard requirements.

## WeChat discovery provider

### OBSERVED_IN_RUNTIME — 2026-08-22

`wechat-article-search` is present as a self-contained local provider package:

```text
~/.codex/skills/wechat-article-search/
├─ SKILL.md
├─ scripts/search_wechat.js
└─ node_modules/...
```

Carrier normalization:

```text
SKILL.md / skill directory = carrier
scripts/search_wechat.js   = independent local_script execution surface
Node + cheerio             = runtime dependencies
weixin.sogou.com           = network backend
```

The package is outside ZCode's normal Skill discovery directories, but a direct Bash invocation of the local script succeeded. Therefore Skill registration is not required for this binding to be operational in the observed ZCode runtime.

Representative probe:

```text
query = "ArcPy使用之一 SDE数据定时备份"
provider executed end-to-end
returned structured JSON
total = 0
```

Interpretation:

```text
Operational = AVAILABLE
Retrieval quality/discoverability = limited for this observed target
```

Do not infer that exact-title discovery is reliable merely because the provider is callable.

## WeChat article reader

### OBSERVED_IN_RUNTIME

In one real article-reading case:

1. `ctx_fetch_and_index` timed out on the WeChat article;
2. an independent Node HTTP fetch using a WeChat/browser-compatible UA succeeded and returned the body.

Keep this as a fallback observation only.

Do not turn it into a portable requirement such as:

- “always use Node”;
- “always use this UA”;
- “all WeChat reads need a longer timeout”;
- “these two paths are always independent failure domains”.

Use the current reader specialist/normal path first; use an independent read path only after an observed read gap and when it remains legitimate/read-only.
