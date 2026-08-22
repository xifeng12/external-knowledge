# Retrieval Quality — v0.3-beta.1

Operational availability, semantic coverage, and source discoverability are separate.

```text
Operational Status
  = can the provider be called?

Semantic Coverage
  = does this provider semantically match the information need/source type?

Source Discoverability
  = in observed use, how well can this provider actually surface items from the target source semantic?
```

## Discoverability values

Use these as evidence-backed observations, not permanent provider traits:

- `GOOD`
- `LIMITED`
- `LIMITED_OBSERVED`
- `VERY_LOW_OBSERVED`
- `UNKNOWN`

`VERY_LOW_OBSERVED` is not the same as a proven structural blind spot.

Do not write `STRUCTURAL_BLIND_SPOT` unless mechanism-level evidence establishes that the source is not indexed/visible through the provider.

Discoverability is scoped to:

```text
Provider × Source Semantic
```

Example:

```text
general-web search × ordinary public web
!=
general-web search × WeChat article discovery
```

A provider can be fully operational while discoverability for one source semantic is very low.

## WeChat evidence from real cases

### wechat-article-search specialist

Observed:

```text
Operational = AVAILABLE
Semantic Coverage = EQUIVALENT
Discoverability = LIMITED_OBSERVED
```

Reason: the local Node provider executed end-to-end against the Sogou WeChat backend, but an exact-title-like query for a known-existing article returned zero results.

This means:

```text
provider callable
!=
target article discoverable
```

### general web fallback for WeChat discovery

Observed repeatedly:

```text
Operational = AVAILABLE
Semantic Coverage = DEGRADED
Discoverability = VERY_LOW_OBSERVED
```

This statement is scoped only to WeChat article discovery. It is not a claim that the general-web provider is globally poor.

When a fallback is `VERY_LOW_OBSERVED`, do not treat it as a normal productive degraded path. At most make one bounded attempt if it can still change the answer; otherwise disclose the limitation and prefer the specialist, targeted re-verification, or user-supplied title/account/link evidence.

## LOW_QUERY_DISCRIMINATION signal

Record:

```text
QUALITY_SIGNAL = LOW_QUERY_DISCRIMINATION
```

when all of these are observed:

1. materially different queries were issued;
2. Top-N results are highly or fully identical;
3. results are semantically irrelevant to the requested meaning/source.

Consequence:

```text
STOP repeated query rewriting
```

Then choose only a materially different next step:

- use a specialist source owner;
- targeted re-verification if runtime profile contradicts observed behavior;
- use stronger user-provided identifiers;
- disclose the retrieval limitation.

Do not convert this signal into provider `UNAVAILABLE` or `BLOCKED`.

## Semantic mismatch / ambiguity

After the first meaningful result set, compare the semantic cluster of Top-N results with the resolved user intent.

### Context already resolves the meaning

If:

```text
SEMANTIC_MISMATCH = HIGH
and
CONTEXT_ALREADY_RESOLVES_AMBIGUITY = YES
```

perform at most one contextual rewrite.

Example:

```text
SDE 数据库
→ ArcGIS SDE / enterprise geodatabase context
```

If the mismatch persists, STOP repeated rewriting and disclose the mismatch.

### Context does not resolve the meaning

If:

```text
SEMANTIC_MISMATCH = HIGH
and
CONTEXT_ALREADY_RESOLVES_AMBIGUITY = NO
```

ask the user to disambiguate rather than spending search actions on guesses.

## STOP interaction

Discoverability and quality signals strengthen Evidence STOP.

Another query is justified only when it introduces materially new evidence, not merely another wording through the same degraded channel.
