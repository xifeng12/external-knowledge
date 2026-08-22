# ZCode v0.3-beta.1 — Real-Case Regression Check

Do not repeat the full WeChat discovery investigation.

The real case already established:

```text
wechat-article-search execution = callable
known target exact-title-like query = zero results
general web WeChat discoverability = VERY_LOW_OBSERVED
```

## Goal

Verify only that beta.1 now represents those facts correctly.

## Checks

1. Doctor/adapter no longer leaves `wechat-article-search` exposure contract empty.
2. The provider binding uses `local_script`; Skill registry is carrier evidence.
3. Node/cheerio/Sogou backend are dependencies/backend, not independent exposure classes.
4. A representative runtime inventory may mark the provider `AVAILABLE` without claiming the target article is discoverable.
5. Runtime routing distinguishes:
   - Operational Status;
   - Semantic Coverage;
   - Source Discoverability.
6. General Web for `wechat.article-discovery` is recorded as:
   - Operational available (runtime fact);
   - semantic coverage degraded;
   - discoverability `VERY_LOW_OBSERVED`.
7. `LOW_QUERY_DISCRIMINATION` stops repeated same-channel rewrites.
8. High semantic mismatch:
   - context resolved -> one contextual rewrite;
   - persists -> STOP;
   - context unresolved -> clarify.
9. Provisioning remains untouched: no install/config candidate is created merely from limited discoverability.

## No new live probe required

The prior representative probe is sufficient. Do not search for the SDE article again merely to make beta.1 pass.

## Output

```text
WECHAT_EXPOSURE_CONTRACT_FIXED =
DEPENDENCY_VS_EXPOSURE_SEPARATION =
OPERATIONAL_VS_DISCOVERABILITY_SEPARATION =
GENERAL_WEB_WECHAT_PROFILE =
LOW_QUERY_DISCRIMINATION_RULE =
SEMANTIC_MISMATCH_RULE =
PROVISIONING_MODEL_UNCHANGED =
NEW_STRUCTURAL_FAILURES =

V0.3_BETA1_STATUS =
```

If all checks pass and no new structural contradiction appears:

```text
V0.3_BETA1_STATUS = COMPLETE
```

Then STOP. Future evidence should come from real work.
