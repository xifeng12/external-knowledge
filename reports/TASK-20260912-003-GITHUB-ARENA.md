# TASK-20260912-003 — Capability Arena v0.1 / GitHub Semantic First Match

## State

`READY_FOR_ARENA_REVIEW` — Arena cleanup status: **CLEAN_VERIFIED**

> Correction record (v0.1 review, 2026-09-12): first-attempt / final-answer statistics in §2 and §3 were reconciled against the contestant receipts as primary execution evidence — the challenger's Q5 is `NOT EXTRACTED` (4/5 final items), and the defender's Q5 came from the op1b projection-completeness repeat (4/5 first-attempt). Receipts unchanged; outcome, routing, and cleanup classification unchanged.

- Contract: `tasks/TASK-20260912-003-CAPABILITY-ARENA-GITHUB.md` (authorized at remote head `453b7a1`)
- Match id: `TASK-20260912-003-gh-semantic-001`
- Receipts: `evidence/arena/TASK-20260912-003-gh-semantic-001/{defender,challenger,adjudication}.json`
- Arena contract: `references/capability-arena.md` (v0.1, minimal domain-specific)

## 1. Admission Gate — PASSED (both contestants)

Baseline-before-install facts (§1.1): `github-mcp-server` ABSENT from PATH; no GitHub MCP in the live session manifest; no registration in the five static MCP config domains inspected in TASK-002; Docker ABSENT; arena temp cell ABSENT; `gh` authenticated as `xifeng12` (keyring; scopes `gist, read:org, repo, workflow`).

- **Defender `gh-cli`**: AVAILABLE (retained TASK-001 runtime evidence + live authenticated calls in this match).
- **Challenger `github/github-mcp-server`**: not operational anywhere → **ephemeral staging only**, per authorization. Docker unavailable, so preference-2 "isolated executable" route: official `v1.12.1` release binary downloaded into `%TEMP%/external-knowledge-arena/<match-id>/runtime/` (one transient TLS-handshake-timeout retry on the release CDN; api.github.com unaffected). MCP handshake over stdio (`--read-only`) succeeded; `tools/list` exposed 26 read-only tools; `get_me` confirmed the reused identity.
- Credential lifecycle (§1.6): the existing gh token was passed to the challenger only via a process-scope environment variable; the value was never printed, logged, or persisted; no credential creation/rotation/revocation occurred. `READY_FOR_GITHUB_MCP_AUTH_DECISION` was not needed.

## 2. Match — HEAD_TO_HEAD (read-only, fair, isolated)

Mode justification: both contestants answered the identical 5-question scenario (tracking-issue state; draft-PR metadata + head; latest implementation-branch commit + changed files; evidence receipt path; current authorization boundary) against the same repository, with the same ≤8-op / 3-minute budget, isolated from each other's output, read-only with respect to GitHub objects (challenger additionally constrained by its server-side `--read-only` flag).

| | Defender (gh-cli) | Challenger (github-mcp-server v1.12.1) |
|---|---|---|
| ops used | 5 / 8 | 8 / 8 |
| measured time | ~4.0 s | ~6.8 s tool time (+ one-off 34 MB staging) |
| first-attempt correctness | 4/5 items (Q1–Q4) | 2/5 items (Q2, Q3) |
| retries within budget | 1 projection-completeness repeat (op1b re-fetched the body because op1's jq projection discarded the boundary sentence; not an error) | 2 (tool-signature error on Q1; default-branch scoping on Q4) |
| final answer quality | complete, exact refs — 5/5 | 4/5 — complete, exact refs for Q1–Q4 after retries; **Q5 NOT EXTRACTED** (issue body was fetched; the fixed extraction pattern did not match the body's current boundary wording) |

Notable evidence: the challenger's evidence-directory reads defaulted to the **default branch** (`ref=579d94a7…`, where the TASK receipts do not exist) until a ref-pinned final budgeted op returned all three files. Its Q5 extraction pattern missed the issue body's current boundary wording while the underlying data was fetched. Both are driver/extraction behaviors, not capability ceilings — recorded as such.

## 3. Adjudication — KEEP_INCUMBENT

Full dimension-by-dimension comparison in `adjudication.json`. Summary:

- `gh-cli` matches or beats the challenger on every decision-relevant dimension for this scenario (semantic correctness, precision, determinism/replayability, execution cost, operational burden) **with zero staging cost**, because it is already operational in this runtime. The corrected receipts strengthen this: the challenger's final answer covered 4 of 5 items (Q5 never extracted), while the defender covered all 5.
- The challenger's genuine strength is agent ergonomics (typed tools, structured responses, built-in read-only mode), but in this runtime the agent consumes `gh` JSON equally well through the shell, so the advantage is scenario-invariant here.
- **No failure-domain independence**: same GitHub API backend, same reused auth identity, same network path. Shared dependencies are recorded and were not presented as resilience.
- `SPLIT_BY_SCENARIO` was tested as the plausible hypothesis and rejected: no scenario emerged that the defender cannot serve equivalently; a split would add a second operational surface without a requiring scenario.
- `REJECT_CHALLENGER` was deliberately **not** chosen: the challenger is validated as operationally capable and remains a viable future candidate (runtimes without `gh`, OAuth-scoped delegation needs).

**Routing impact: none.** Source-semantic ownership of `github.semantic` remains `gh-cli`. Per contract §8 the run stops at `READY_FOR_ARENA_REVIEW` rather than `READY_FOR_ROUTING_CHANGE_DECISION`.

## 4. Staging provenance and teardown

Arena-owned artifacts (all introduced by this match, none pre-existing): the release binary + extracted runtime, match driver scripts, all inside the match-scoped temp cell. No PATH change, no persistent MCP registration, no shell-profile/proxy/TLS/browser change, no credential state.

Teardown verification (beyond delete-success): no `github-mcp-server.exe` process running; 34 MB cell deleted and confirmed absent; `github-mcp-server` still ABSENT from PATH; no registration in any inspected config domain; no docker artifacts; repository tree contains only intended durable outputs.

```text
classification: CLEAN_VERIFIED
residue: none
```

## 5. Invariants and scope discipline

§11 invariants enforced as process checks recorded in the receipts; **no repository code was introduced** (the Arena contract is documentation; driver scripts were ephemeral match tooling and were torn down), so no new test files were required. skill-forge boundary (§9): no generic harness was built; integration point noted for a future run if reusable execution/rollback mechanics are wanted. Explicitly unauthorized items (§10) — persistent install, other Challengers, credential creation, global environment changes, synthetic matrices, GitHub object mutation, promotion, PR #3/main merge, retaining the Arena runtime — none performed.

## 6. Next authorization needed

None required to close this task. The Human may next review the adjudication (this state), authorize a production routing change if they disagree with `KEEP_INCUMBENT`, or authorize the next Arena match / Challenger. No further work continues from this run.
