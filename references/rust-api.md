# Rust API Rules for Infra Code

Distilled from the local Google Rust Style Guide analysis
(`google-rust-styleguide-plan.md`, `google-rust-styleguide/upstream-source/rustguide.md`).
These are review rules, not a replacement for the full guide.

## State

- Use an `enum` for a state machine, not several booleans.
- Prefer explicit `Unknown`, `Unresolved`, `Busy`, `TimedOut`, `Cancelled`.
- Do not let a provider name become a `kind`; `kind` is isolation/execution semantics.

## Errors

- Expected failures return `Result`.
- `expect("...")` is only for a violated invariant.
- Errors carry context: operation, resource, state, whether a side effect occurred.
- Do not convert an unknown outcome into success or a blind retry.

## Public API

- `#[non_exhaustive]` on public enums/structs that may grow (capabilities, status, config).
- `#[must_use]` on receipts, guards, handles, status values.
- Keep public API docs with `# Safety`, `# Panics`, `# Errors`, cancellation semantics.
- Prefer borrowed inputs: `&str`, `&[T]`, `impl Iterator`.
- Avoid unnecessary `clone`; measure before optimizing.

## Unsafe

- Every `unsafe` block has a `SAFETY:` comment stating:
  - the invariant,
  - who guarantees it,
  - the lifetime/ownership argument.
- Infra hot spots: mount, namespace, exec, fd passing, shared memory.

## Concurrency

- Make synchronization explicit; avoid hidden global state.
- Handle mutex poisoning deliberately.
- Do not put blocking I/O on an async hot path.
- Bound channels/queues; define full/closed behavior.

## Organization

- Small crates, flat modules.
- No glob imports.
- Separate generated code from handwritten code.
- Keep test-only seams out of production APIs unless justified.

## Naming

- `try_` for fallible variants.
- `into_` for ownership-consuming conversion.
- `as_` for cheap borrowed conversion.
- `is_` for predicates.
- Avoid abbreviations that hide meaning.
