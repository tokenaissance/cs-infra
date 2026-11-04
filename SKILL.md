---
name: cs-infra
description: Review CS infrastructure design and Rust implementation for failure domains, idempotency, bounded resources, observability, control/data separation, capacity, cost, failover, on-call readiness, and Google Rust API rules. Use when designing or reviewing control planes, distributed services, storage, schedulers, or Rust infrastructure code. Do not use for general coding tutorials or non-infra product features.
license: MIT
metadata:
  author: Tokenaissance
  version: "0.1.0"
---

# CS Infra

A review/design checklist for computer-systems infrastructure. It reviews two layers:

```text
A–I  infra design: failure domains, data, capacity, rollout, DR, observability, on-call, security
J    Rust code/API: enums, Result, non_exhaustive, must_use, unsafe, docs
K    review gate: evidence and verdict
```

## When to use

- Reviewing a control plane, scheduler, storage service, agent runtime, or sandbox platform.
- Designing failure domains, idempotency, leases, queues, capacity, or multi-region behavior.
- Reviewing Rust infra code for API shape, error handling, unsafe, or concurrency.
- Writing an ADR, design review, runbook, or production-readiness checklist.

## When not to use

- General programming tutorials or language syntax questions.
- Product/UI features with no infrastructure semantics.
- Security pentesting or compliance certification.
- Pure benchmark execution without design/review output.

## Review protocol

### Pass 1 — Scope and invariants

Ask for, or infer and label:

```text
one-sentence purpose
SLOs: availability, latency, durability, cost
failure domains: process / sandbox / machine / store / region
source of truth: store / external DB / object storage
control plane vs data plane
invariants: what must never happen
non-goals
```

If these are missing, report them as `missing input`, not as design findings.

### Pass 2 — Design checklist (A–I)

Read [checklist](references/checklist.md). Cover:

- A correctness and formal methods
- B architecture and failure domains
- C data, consistency, storage
- D capacity, cost, backpressure
- E release, rollback, migration
- F multi-region and disaster recovery
- G observability and SLO
- H incident response and on-call
- I security and isolation

Do not mark a section "pass" without evidence. Use `E0–E3` evidence tiers.

### Pass 3 — Rust code/API (J)

Read [Rust API rules](references/rust-api.md). Check:

- state as enum, not multiple bools
- `Result` for expected failures; `expect` only for invariants
- `#[non_exhaustive]` for extensible public types
- `#[must_use]` for receipts, guards, handles, status
- borrowed inputs before clone
- `SAFETY:` comments for unsafe
- explicit concurrency; no blocking I/O in async hot paths
- `# Safety` / `# Panics` / `# Errors` docs
- no glob imports; small modules

### Pass 4 — Gate (K)

Use [checklist](references/checklist.md) K.

Required outputs:

```text
## Verdict
pass / pass-with-conditions / block

## Blockers (P0)
finding | why | evidence | required fix

## Should fix (P1)
finding | why | evidence | suggested fix

## Missing evidence
item | current tier | required tier | how to obtain

## Checklist coverage
A–K: covered / not applicable / missing
```

## Severity

| Level | Meaning |
|---|---|
| P0 | data loss, correctness, security, unbounded failure, no rollback |
| P1 | reliability/observability/cost gap that will hurt production |
| P2 | maintainability/API/docs gap |

## Core rules

1. **No checklist theater.** Every finding needs a concrete failure mode or missing invariant.
2. **Evidence over assertion.** E0 claim ≠ E2 test. Mark the gap.
3. **Design and code are separate passes.** Do not mix an ADR finding with a Rust style nit.
4. **No retry without idempotency.** If retry is proposed, require an idempotency key and a duplicate-side-effect analysis.
5. **No unbounded queue.** Require a limit and a load-shedding/drop policy.
6. **Failure domains must be enumerable.** "It's HA" is not an answer.
7. **Control plane owns records; data plane executes.** Data plane must not read the control-plane home.
8. **Do not invent providers or limits.** Label uncertain claims and ask for source/benchmark.
9. **Separate storage from compute.** Network SQLite and object-storage-as-database are anti-patterns.
10. **Reference, don't duplicate.** Rust rules live in `references/rust-api.md`; do not restate them in every review.

## Output style

- Concise Chinese by default; technical terms may stay English.
- Use tables for findings.
- Quote the invariant or failure mode, not generic advice.
- End with the smallest next action, not a lecture.

## References

- [Full checklist](references/checklist.md)
- [Rust API rules](references/rust-api.md)
- [Sources and gaps](references/sources.md)
