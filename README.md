# external-knowledge v0.3-beta.1

Real-case refinement after WeChat discovery testing.

## What changed

A real task searched for the known-existing WeChat article:

```text
《ArcPy使用之一：SDE数据定时备份》
公众号：图说新语
```

The case produced two independent findings:

1. **Exposure finding** — `wechat-article-search` was actually present and callable as a local Node script even though its Skill directory was outside ZCode's Skill discovery surface.
2. **Retrieval-quality finding** — the specialist itself returned zero results for an exact-title-like query, while General Web repeatedly showed very low discoverability for WeChat content.

Therefore the failure cannot be attributed only to routing/exposure. Operational availability and item discoverability must remain separate.

## Model

```text
Information Need / Source Semantic
        ↓
Capability
        ↓
Provider
        ├─ Operational Status
        ├─ Semantic Coverage
        ├─ Source Discoverability
        └─ Independent Exposure
```

## WeChat provider normalization

```text
~/.codex/skills/wechat-article-search/
├─ SKILL.md                 = carrier
├─ scripts/search_wechat.js = local_script exposure
└─ node_modules/cheerio     = runtime dependency

Node runtime                = runtime dependency
weixin.sogou.com            = network backend
```

The network backend and dependencies are not Agent exposure classes.

## Routing quality additions

- `Provider × Source Semantic` discoverability axis;
- `LOW_QUERY_DISCRIMINATION` STOP signal;
- high semantic mismatch → one contextual rewrite if context already disambiguates, otherwise ask;
- repeated WeChat-specific General Web limitations remain scoped evidence, not a global search-engine judgment.

## Provisioning model unchanged

The beta approval model is unchanged:

```text
Doctor -> Plan -> exact plan_id -> explicit approval -> exact execution -> Verify
```

This real case creates **no provisioning candidate** because the WeChat discovery provider is already callable.

## Files

```text
external-knowledge-v0.3-beta.1/
├── SKILL.md
├── adapters/zcode-v0.3-beta.1.json
├── references/
│   ├── capability-model.md
│   ├── retrieval-quality.md
│   ├── runtime-adapter-contract.md
│   ├── runtime-notes-zcode.md
│   ├── source-ownership.md
│   ├── setup-policy.md
│   └── provisioning-contract.md
├── scripts/
│   ├── doctor.py
│   └── plan.py
└── tests/
```
