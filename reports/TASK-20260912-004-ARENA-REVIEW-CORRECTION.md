# TASK-20260912-004 — Arena Review Correction

## Review state

`NO_BATTLE / INVALID_SCENARIO`

TASK-20260912-004 executed successfully as an Arena run and returned `CLEAN_VERIFIED`, but its ownership adjudication is invalid because the selected representative case was routed to the wrong capability.

## Why the question was invalid

The target was a canonical WeChat article. Repository authority already assigns canonical WeChat article reading to the specialist semantic `wechat.reader`.

The generic `complex-web.read` capability is intended for complex extraction after an ordinary known-URL read gap. A specialist-owned source must not be used as the representative ownership exam for that broader capability.

Therefore:

```text
WeChat anti-bot result
!= generic complex-web.read ownership result
```

## What remains valid

The following execution evidence is retained as factual observation:

- native WebFetch/default native path received the WeChat verification page;
- Crawl4AI 0.9.3 default configuration also received the WeChat verification page;
- the page was reachable with a browser-like UA in the admission baseline;
- Crawl4AI staging footprint and operational burden were observed as recorded;
- the Arena-owned runtime was removed and teardown remains `CLEAN_VERIFIED`.

These facts may inform a future **WeChat-specific** Arena or provider diagnosis.

## What is superseded

The original adjudication field:

```text
REJECT_CHALLENGER
```

is superseded for `complex-web.read` ownership purposes by:

```text
NO_BATTLE / INVALID_SCENARIO
```

This does not count as a Crawl4AI loss and does not justify rejecting Crawl4AI from future correctly routed `complex-web.read` matches.

## Next state

`READY_FOR_COMPLEX_WEB_CASE_DECISION`

A new generic complex-web Arena requires a preserved real case whose source semantic is not already owned by `wechat.reader`, `wechat.discovery`, `github.semantic`, `docs.versioned`, or another first-class specialist.

WeChat competition, if authorized later, must use a separate `wechat.reader` or `wechat.discovery` Arena.
