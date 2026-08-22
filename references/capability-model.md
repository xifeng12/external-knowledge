# Capability / Provider / Exposure Model — v0.3-beta.1

alpha.2 separates four layers that must not be collapsed:

```text
Information capability
  -> provider binding(s)
     -> independent exposure class(es)
        -> scoped evidence / authority
```

## 1. Capability

A capability is the user-facing information function, for example:

- `general-web.read`
- `docs.versioned`
- `github.semantic`
- `complex-web.read`

A capability is **not** a provider name.

`complex-web.read` may have multiple providers. Therefore:

```text
Firecrawl missing != complex-web.read missing
```

## 2. Provider binding

A provider is one concrete implementation that can serve a capability.

Example:

```text
complex-web.read
├─ runtime-native.webfetch
└─ firecrawl
```

Each provider has its own:

- operational status;
- semantic coverage grade;
- source-semantic discoverability observations;
- exposure contract;
- evidence.

Provider status uses:

- `AVAILABLE`
- `AVAILABLE_WITH_SCOPE`
- `UNKNOWN`
- `UNAVAILABLE`
- `BLOCKED`
- `MISSING_CONFIRMED`

Static presence can establish an exposure artifact, but not provider `AVAILABLE`.

## 3. Independent exposure class

An exposure class is an **independent execution surface** through which the current runtime can make that provider callable by the Agent.

Examples:

- `native_tool`
- `mcp`
- `path_cli`
- `local_script`

Do not automatically make these independent exposure classes:

- plugin registry;
- skill registry;
- config file;
- managed package.

Those may be **carriers / registration evidence**.

### Carrier normalization

If a plugin contributes an MCP server:

```text
plugin_registry -> mcp
```

count only:

```text
mcp
```

as the provider exposure class.

Record:

```text
carrier_class = plugin_registry
exposure_class = mcp
```

Likewise:

```text
skill_registry -> path_cli
```

counts only `path_cli` if the Skill merely instructs/calls that CLI.

This prevents double-counting one provider path as both a container and an execution surface.

## 4. Scoped absence authority

`MISSING_CONFIRMED` is provider-scoped.

For a provider:

- `L` = all declared independent legal exposure classes;
- `A` = legal classes covered by authoritative absence evidence;
- `P` = legal classes with PRESENT evidence.

```text
provider MISSING_CONFIRMED
iff
L is declared and non-empty
AND L ⊆ A
AND P = ∅
```

### PATH is scope-authoritative

For a command-backed provider:

```text
shutil.which("firecrawl")
```

is authoritative for this narrow scope:

```text
current process PATH + executable resolution semantics
```

Therefore:

```text
which(...) is None
```

can authoritatively establish absence of the provider's `path_cli` exposure class.

It does **not** establish that the software is absent everywhere on the machine.

Conversely:

```text
which(...) returns a path
```

establishes `path_cli PRESENT`, but not provider `AVAILABLE`.

A representative runtime probe or equivalent runtime evidence is still needed for `AVAILABLE`.

## 5. Capability aggregation

Capability status is computed from provider bindings.

### At least one provider operational

If any provider is `AVAILABLE` / `AVAILABLE_WITH_SCOPE`, the capability is not missing.

- best available coverage `EQUIVALENT` -> capability `AVAILABLE`;
- only degraded/specialized/scoped provider -> capability `AVAILABLE_WITH_SCOPE`.

### All providers missing

Only when **all declared provider bindings** are `MISSING_CONFIRMED` may the capability be `MISSING_CONFIRMED`.

### Unknown provider remains

If no provider is operational and at least one remains `UNKNOWN`, capability remains `UNKNOWN`.

This is the formal version of:

```text
Provider missing != Capability missing
```

## 6. Coverage

Coverage is provider-relative to the capability:

- `EQUIVALENT`
- `DEGRADED`
- `SPECIALIZED`
- `NOT_APPLICABLE`
- `UNKNOWN`

Operational status and semantic coverage remain separate axes.


## 7. Source discoverability

Discoverability is not part of Operational Status and is not another Coverage grade.

It answers:

> For this Provider × Source Semantic, how well does observed retrieval surface items from the target ecosystem?

Use evidence-backed values described in `retrieval-quality.md`.

A provider can be:

```text
Operational = AVAILABLE
Semantic Coverage = EQUIVALENT
Discoverability = LIMITED_OBSERVED
```

This is the current observed shape for `wechat-article-search` in the real SDE backup article case.

Likewise, an available general-web provider can be semantically degraded and have `VERY_LOW_OBSERVED` discoverability for WeChat article discovery without being globally broken.

## 8. Need and plan

Need remains capability-level:

- `REQUIRED`
- `RECOMMENDED`
- `WANTED`
- `OPTIONAL`
- `NOT_NEEDED`

Beta planning/execution boundaries remain defined by `provisioning-contract.md`; discoverability evidence does not itself authorize installation.
