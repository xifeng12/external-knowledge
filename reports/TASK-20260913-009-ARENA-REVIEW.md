# TASK-20260913-009 — Arena Review / Precision Search Policy Promotion

## Review conclusion

The raw TASK-009 execution evidence is accepted, including `CLEAN_VERIFIED`, but its `SPLIT_BY_SCENARIO` interpretation is **not promoted into a new test-stage routing policy**.

```text
raw benchmark adjudication: SPLIT_BY_SCENARIO
policy-promotion review:   POLICY_NOT_PROMOTED
Exa status:                QUALIFIED_CHALLENGER_CANDIDATE
current default:           runtime-native.web-search remains unchanged
```

The contestant receipts remain primary execution evidence and are not rewritten.

## Why the split is not promoted

TASK-009 §5 explicitly requires:

> A difference must be material and repeated across relevant fixtures before it changes the test-stage policy.

The benchmark did not satisfy that bar.

### S1 is useful evidence, but not a strict target hit

Query:

```text
"X-Tavily-Access-Mode"
```

The frozen accepted target required official Tavily source/docs **containing that identifier**. Exa returned five official Tavily-family surfaces, but did not return the strict bullseye `tavily-ai/tavily-mcp/src/index.ts`, and the contract explicitly excluded content fetching that could verify identifier presence on the returned pages.

Therefore preserve two different observations:

```text
family recall: strong
strict exact-target hit: not demonstrated
```

Family recall must not be silently upgraded into an exact-token bullseye.

The native contestant's 0/5 pure-noise result on S1 is still a real and important failure.

### The advantage was not repeated across the declared precision class

- S1: Exa materially better at target-family recall; strict target unresolved.
- S2 exact configuration symbol: both hit@1; native had the fuller top-5.
- S4 precise capability parameter: both hit@1; native had the cleaner top-5.
- S5 multi-constraint: both hit@1; Exa had a much cleaner list.
- S3 semantic paraphrase: native succeeded; Exa returned the wrong vendor family.

This supports **Exa as a credible independent precision-search candidate**, but not a repeated enough advantage to freeze an automatic Native -> Exa escalation policy yet.

## What TASK-009 did prove

Exa is no longer merely a declared provider candidate.

Verified in this runtime/test track:

```text
anonymous hosted MCP is operational
no API key / OAuth / login required for the tested Exa search surface
single-call latency was stable in the observed run
failure domain is materially independent from the native search backend
exact/opaque-token family recall can succeed where native search can completely miss
structured result output is suitable for deterministic scoring
```

The candidate therefore advances rather than being rejected.

## Tavily admission decision

The prerequisite established by TASK-009 is satisfied: Exa now has execution and benchmark evidence.

Tavily may enter the next Arena as Challenger to the **precision-search candidate slot**, not as a third contestant against Native in the same match.

The next match is therefore:

```text
capability: precision.search
candidate-slot Defender: Exa hosted MCP (anonymous)
Challenger: Tavily Remote MCP (keyless)
evidence_class: CONTROLLED_BENCHMARK
```

Native search remains outside this playoff as the unchanged general/default owner.

## Tavily current anonymous surface

Official Tavily keyless documentation currently states that Search and Extract can run without an account or API key. For Remote MCP, the required request header is:

```text
X-Tavily-Access-Mode: keyless
```

The keyless MCP exposes `tavily-search` and `tavily-extract`; TASK-010 will use search only. Keyless access is rate-limited. `/crawl`, `/map`, and `/research` require an API key and are out of scope.

No API key, OAuth flow, login, account creation, or persistent MCP registration is authorized.

## Evidence maturity

TASK-009 contributes candidate evidence, not final production ownership:

```text
Exa candidate evidence = ACCEPTED
Native -> Exa automatic escalation policy = NOT YET FROZEN
real-world validation debt = OPEN_NONBLOCKING
```

The next controlled playoff is allowed immediately.
