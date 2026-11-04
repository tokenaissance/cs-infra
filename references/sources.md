# Sources and Gaps

## Community skills reviewed

| Skill | Source | Used for |
|---|---|---|
| `kubernetes-patterns` | affaan-m/ECC | probes, RBAC, resources, production manifests |
| `deployment-patterns` | affaan-m/ECC | rolling/blue-green/canary, rollback |
| `gitops-workflow` | wshobson/agents | desired state, reconciliation |
| `latency-critical-systems` | affaan-m/ECC | p50/p95/p99, hot path, backpressure |
| `enterprise-agent-ops` | affaan-m/ECC | lifecycle, observability, kill switch |
| `distributed-systems` | FerroxLabs | CAP/PACELC, consensus, fallacies |
| `tla-plus` | apache/cassandra | formal spec, invariants, model checking |
| `quint-modeling` | quint-co | executable specs, model checking |
| `slo-implementation` | wshobson/agents | SLI/SLO, error budgets |
| `incident-responder` | davila7 | severity, command, stabilization |
| `eng-runbook` | nexu-io | runbook structure, on-call |
| `qdrant-scaling` | github/awesome-copilot | scaling by data/QPS/latency/volume |
| `mysql-patterns` / `database-migrations` | affaan-m/ECC | replication, migrations, rollback |

## Local source

- Google Rust Style Guide analysis: `google-rust-styleguide-plan.md`
- Upstream mirror: `google-rust-styleguide/upstream-source/rustguide.md`

## Gaps

- No dedicated storage-engine internals skill (B-tree/LSM/WAL/compaction).
- No general unit-economics/FinOps model beyond cloud-provider fragments.
- No Jepsen-style consensus fault-injection skill.
- Real on-call data must come from the organization; not in any catalog.
- Cross-region data-sovereignty/compliance needs legal review.
