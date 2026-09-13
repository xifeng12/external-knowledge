# TASK-20260913-011 — Goal-Integrity Stop

## Review decision

`CANCELLED_BY_GOAL_INTEGRITY`

TASK-011 was authorized as a 60-minute, rate-limit-aware Exa-vs-Tavily retake after TASK-010 ended `NO_BATTLE` because Tavily's free keyless surface exhausted a burst/window budget.

The Human reviewed that next step before execution and rejected it as low-value horizontal hardening relative to the project goal.

## Why the retake is cancelled

The unresolved question is narrow:

```text
Which already-qualified precision-search candidate should occupy the candidate slot under a free/keyless rate-limited test envelope?
```

Current evidence already establishes enough for the test stage:

- Native web search remains the general/default owner.
- Exa is operational through anonymous Hosted MCP and is a `QUALIFIED_CHALLENGER_CANDIDATE`.
- Tavily keyless search is operational but unadjudicated because TASK-010's quality matrix was incomplete under its free rate-limit envelope.
- TASK-010 is `NO_BATTLE`, not a Tavily loss.

Spending up to 60 minutes to complete that candidate-slot playoff would improve confidence inside an already-covered search capability, but would not add a new source semantic or materially expand what the Agent can know.

The external-knowledge project still has first-class P1 source-semantic gaps:

```text
Twitter/X
Reddit
YouTube/transcript
RSS
```

Therefore Goal Integrity requires moving vertically into capability coverage rather than continuing the precision-search playoff.

## Preserved state

Do not rewrite TASK-009 or TASK-010 raw receipts.

Preserve:

```text
Native default search policy = unchanged
Exa = QUALIFIED_CHALLENGER_CANDIDATE
Tavily = OPERATIONAL_CANDIDATE_UNADJUDICATED
TASK-010 = NO_BATTLE / CLEAN_VERIFIED
```

No automatic Native -> Exa escalation policy is frozen from TASK-009.

## TASK-011 execution status

TASK-011 was cancelled before the target-machine retake executed.

Therefore:

```text
no TASK-011 contestant run
no TASK-011 rate-limit waiting
no TASK-011 provider staging
no TASK-011 cleanup receipt required
```

The existing TASK-011 contract remains a historical record of the proposed redesign and MUST NOT be executed unless a later Human explicitly reopens it.

## Next direction

Return to vertical capability expansion.

Selected next P1 vertical slice:

```text
YouTube discovery / metadata / transcript
```

Rationale:

- it fills a currently unmodeled first-class source semantic;
- the target machine already exposed a `yt-dlp-downloader` carrier clue, though operational status is still unverified;
- upstream `yt-dlp` natively supports YouTube search (`ytsearch:`) and subtitle/automatic-caption workflows without requiring media download;
- it can be tested without login/cookies on public fixtures before any durable provisioning decision.

Current stop state:

```text
READY_FOR_YOUTUBE_VERTICAL_EXECUTION
```
