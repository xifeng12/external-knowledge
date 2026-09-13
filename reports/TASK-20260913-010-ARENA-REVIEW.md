# TASK-20260913-010 — Arena Review

## Review conclusion

`NO_BATTLE` is accepted. The Exa-vs-Tavily candidate-slot playoff did not produce a fair complete quality matrix.

## Why this is not a Tavily capability loss

The retained execution evidence separates three facts:

1. Tavily keyless Remote MCP admitted successfully and E1 returned a valid full result set.
2. The subsequent burst entered a keyless quota/rate-limit window; later calls returned empty/ambiguous payloads rather than comparable search results.
3. A post-window diagnostic returned valid results again.

Therefore the incomplete Tavily matrix is an execution-envelope failure, not evidence that Tavily search quality lost to Exa.

The attempt-1 SSE parsing defect is separately disclosed and does not explain the later corrected-parser window failures.

## What remains valid

- Exa completed all nine frozen fixtures and its results are valid retained evidence.
- Strict target hits and target-family recall remained separated as required.
- Tavily E1 is valid evidence, but one completed fixture cannot decide any 2-of-3 class gate.
- `CLEAN_VERIFIED` is accepted.
- No candidate-slot promotion/rejection follows from TASK-010.

```text
candidate slot before retake: Exa (status quo qualified candidate)
Tavily: unadjudicated
Native Search: unchanged default owner
```

## Redesign decision

Authorize a retake under a new task using the same frozen nine-query suite and class gates, but with a rate-limit-aware execution envelope.

Preferred Tavily scoring surface for the retake is the official keyless Search REST endpoint rather than the Remote MCP transport. This keeps the Tavily search backend while exposing structured keyless-limit metadata needed for fair checkpoint/cooldown scheduling.

The retake must:

- keep all query text and target sets unchanged;
- keep Exa `numResults=5` and Tavily `max_results=5`;
- checkpoint each completed fixture before the next call;
- stop issuing Tavily calls immediately on a keyless-limit response;
- honor the service-provided retry/cooldown metadata before retrying only the blocked fixture;
- never score a rate-limit envelope/error as a search-quality result;
- preserve raw provider responses before teardown.

## State

`READY_FOR_PRECISION_PLAYOFF_RETAKE`
