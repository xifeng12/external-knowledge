# Runtime Adapter Contract — v0.3-beta.1

The adapter maps portable external-knowledge capabilities to concrete providers and independent execution surfaces in one runtime.

## Shape

```json
{
  "capabilities": [
    {
      "id": "complex-web.read",
      "providers": [
        {
          "id": "firecrawl",
          "coverage_grade": "EQUIVALENT",
          "exposure_contract": {
            "legal_classes": ["mcp", "path_cli"],
            "scope": "current ZCode Agent execution surfaces for Firecrawl"
          },
          "checks": []
        }
      ]
    }
  ]
}
```

## Provider binding is mandatory

Do not write:

```text
capability = complex-web.read / Firecrawl
```

Write:

```text
capability = complex-web.read
provider = firecrawl
```

This prevents one provider's state from being silently promoted to capability state.

## Independent exposure classes only

`legal_classes` must contain only independent execution surfaces.

For ZCode, the current discovery evidence supports classes such as:

- `native_tool`
- `mcp`
- `path_cli`

Do not duplicate a path by adding its carrier as another class.

### Plugin carrier example

If:

```text
plugin manifest
  -> mcpServers
  -> Firecrawl MCP
```

model evidence as:

```json
{
  "exposure_class": "mcp",
  "carrier_class": "plugin_registry"
}
```

Do not create both `plugin_registry` and `mcp` as independent legal classes for the same path.

### Skill carrier example

If a Skill only tells the Agent to call a CLI:

```json
{
  "exposure_class": "path_cli",
  "carrier_class": "skill_registry"
}
```

Do not count `skill_registry` separately.

### Config carrier example

A config file that registers an MCP server is evidence for `mcp`; config itself is not another independent execution surface.

### Managed package

An npm/pip/package artifact is not an exposure class unless the runtime independently executes through that package surface. If it merely produces a CLI shim or MCP server, normalize to `path_cli` or `mcp`.

## PATH absence authority

A `command` check may use:

```json
{
  "type": "command",
  "value": "firecrawl",
  "exposure_class": "path_cli",
  "absence_authoritative": true
}
```

The authority scope is limited to the current process command-resolution surface.

This can prove:

```text
path_cli absent
```

but not:

```text
Firecrawl absent from entire machine
```

## Agent inventory v3

Agent inventory is provider-specific:

```json
{
  "capabilities": {
    "complex-web.read": {
      "providers": {
        "runtime-native.webfetch": {
          "status": "AVAILABLE",
          "evidence_kind": "runtime_tool_exposure",
          "scope": "current ZCode session"
        },
        "firecrawl": {
          "status": "UNKNOWN",
          "evidence_kind": "runtime_inventory",
          "scope": "current ZCode session",
          "authoritative_for_absence": true,
          "absence_covers_exposure_classes": ["mcp"]
        }
      }
    }
  }
}
```

## Absence merge

For each provider separately:

1. collect deterministic observations;
2. collect runtime/provider inventory evidence;
3. normalize carriers to their execution `exposure_class`;
4. check authoritative absence coverage across all legal independent classes;
5. preserve PRESENT outside legal classes as notes;
6. never infer provider `AVAILABLE` from static presence alone.

Then aggregate provider statuses into the capability state.

## Compatibility

alpha.2 may read a legacy direct capability inventory only when a provider explicitly declares `legacy_inventory_key`. New adapters should use provider-scoped inventory.


## `local_script` exposure

A provider may be directly callable by an Agent through a known local script path even if the package directory is not part of the runtime's Skill registry.

Example:

```text
skill directory = carrier
search_wechat.js = local_script exposure
node/cheerio = dependencies
remote search site = backend
```

Only `local_script` is an independent Agent exposure class in that chain.

If a provider binding is explicitly scoped to one known local package/path, exact-path absence may be authoritative for that binding. It does not prove that equivalent implementations are absent elsewhere.

## Runtime dependencies are not exposure classes

Keep:

- language runtime;
- bundled package dependency;
- remote backend endpoint;

separate from independent Agent exposure classes.

Dependency failure may make a present provider unavailable, but must not be double-counted as another exposure path.

## Source-semantic profiles

Runtime adapters may retain evidence-backed `source_semantic_profiles` for routing quality.

These profiles are observational and scoped. They must not be used to infer provider Operational Status.
