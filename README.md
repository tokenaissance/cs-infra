# CS Infra

**English** | [中文](docs/README.zh-CN.md)

> Review CS infrastructure design and Rust implementation, not a tutorial.
> 评审 CS infra 设计与 Rust 实现，不是教程。

## At a glance / 一览

| English | 中文 |
|---|---|
| **What** — review/design checklist for control planes, schedulers, storage, agent runtimes, sandboxes. | **是什么** — 面向 control plane、scheduler、存储、agent runtime、sandbox 的 review/design checklist。 |
| **Layers** — A–I infra design, J Rust code/API, K review gate. | **分层** — A–I infra 设计，J Rust code/API，K 评审 gate。 |
| **Output** — verdict, P0/P1 findings, missing evidence, checklist coverage. | **输出** — verdict、P0/P1 findings、missing evidence、checklist coverage。 |
| **Evidence** — `E0–E3`; no production evidence means `missing evidence`. | **证据** — `E0–E3`；没有生产证据就标 `missing evidence`。 |
| **Not for** — tutorials, UI/product features, pentesting, compliance certification. | **不适用** — 教程、UI/product 功能、渗透测试、合规认证。 |

## What it does / 功能

| English | 中文 |
|---|---|
| `cs-infra` is a single review/design checklist for control planes, schedulers, storage services, agent runtimes, and sandbox platforms. | `cs-infra` 是一个用于 control plane、scheduler、存储服务、agent runtime 和 sandbox 平台的单页 review/design checklist。 |
| It reviews failure domains, idempotency, bounded queues, data/consistency, capacity, rollout, DR, SLO, on-call, security, and Rust API shape. | 它评审 failure domain、幂等、有界队列、数据/一致性、容量、发布、DR、SLO、on-call、安全，以及 Rust API 形状。 |
| It is advisory: findings are recommendations, not automated changes. | 它只给建议：findings 是建议，不自动变更。 |

## Covers / 覆盖

| English | 中文 |
|---|---|
| failure domains and blast radius | failure domain 与 blast radius |
| idempotency, leases, bounded queues | 幂等、lease、有界队列 |
| data, consistency, storage, recovery | 数据、一致性、存储、恢复 |
| capacity, cost, backpressure | 容量、成本、背压 |
| rollout, rollback, migration | 发布、回滚、迁移 |
| multi-region and disaster recovery | 多区域与灾难恢复 |
| SLO, observability, on-call, incident response | SLO、可观测性、on-call、事故响应 |
| security and isolation | 安全与隔离 |
| Rust API rules from the Google Rust Style Guide | Google Rust Style Guide 的 Rust API 规则 |

## Natural-language examples / 示例

| English | 中文 |
|---|---|
| “Review this control plane design for failure domains and idempotency.” | “帮我 review 这个 control plane 的 failure domain 和幂等设计。” |
| “Review this distributed scheduler for capacity, failover, and on-call readiness.” | “帮我 review 这个分布式调度器的 capacity、failover 和 on-call。” |
| “Review this Rust sandbox API for unsafe, error handling, and extensibility.” | “Review this Rust sandbox API for unsafe、错误处理和可扩展性。” |
| “Write a production readiness checklist for a storage service.” | “给这个存储服务写一份 production readiness checklist。” |

## Output / 输出

```text
## Verdict
## Blockers (P0)
## Should fix (P1)
## Missing evidence
## Checklist coverage
```

| English | 中文 |
|---|---|
| Findings are separated from missing input. | findings 与 missing input 分开。 |
| Evidence tiers `E0–E3` are explicit. | 证据等级 `E0–E3` 必须明确。 |
| No evidence means `missing evidence`, not “pass”. | 没有证据就写 `missing evidence`，不能算“通过”。 |

## Structure / 目录

```text
SKILL.md                 routing + review protocol
references/checklist.md  A–K full checklist
references/rust-api.md   Rust code/API review rules
references/sources.md    sources + known gaps
evals/trigger_cases.json trigger boundaries
agents/interface.yaml    adapter metadata
reports/                 evidence and handoff
```

## Prerequisites / 前置条件

- [ ] Node.js and npx installed: `node --version && npx --version`
- [ ] Python 3 installed: `python3 --version`
- [ ] Reviewed the skill's permissions and risk boundary
- [ ] Node.js 与 npx 已安装：`node --version && npx --version`
- [ ] Python 3 已安装：`python3 --version`
- [ ] 已检查 skill 权限与风险边界

## Install / 安装

```bash
npx skills add tokenaissance/cs-infra
```

```bash
npx skills add ./cs-infra
```

| English | 中文 |
|---|---|
| First command: after publishing. | 第一条：发布后使用。 |
| Second command: local checkout. | 第二条：本地 checkout。 |

## Verification / 验证

```bash
python3.12 /Users/reina/.agents/skills/fastagent-meta-skill/scripts/validate_skill.py .
python3.12 /Users/reina/.agents/skills/fastagent-meta-skill/scripts/trigger_eval.py . \
  --cases evals/trigger_cases.json \
  --output reports/trigger-eval.json
```

## Design philosophy / 设计原则

| English | 中文 |
|---|---|
| **Two layers** — infra checklist + Rust guide; do not duplicate Rust rules. | **两层** — infra checklist + Rust guide；Rust 规则不重复。 |
| **Evidence over assertion** — a passing test is not a production observation. | **证据优先** — 测试通过不等于生产观测。 |
| **Failure modes, not generic advice** — name what breaks and why. | **写 failure mode** — 说清什么条件下、什么会坏。 |
| **Small root** — details live in `references/`. | **根目录保持小** — 细节放 `references/`。 |

## Troubleshooting / 常见问题

| Problem / 问题 | Cause / 原因 | Fix / 修复 |
|---|---|---|
| Skill does not trigger / 不触发 | Description lacks `infra`/`review`/`rust` | Edit `description`, rerun trigger eval / 改 description 后重跑 |
| Review is too generic / 评审太泛 | No concrete failure mode | Rewrite as “what breaks, under which condition” |
| Rust section drifts / Rust 规则漂移 | Rules copied into `SKILL.md` | Keep them in `references/rust-api.md` |
| Missing evidence not reported / 没报 missing evidence | Checklist marked pass without tier | Require `E0–E3` for each critical item |

## Credits / 致谢

| English | 中文 |
|---|---|
| Google Rust Style Guide (local analysis and upstream mirror). | Google Rust Style Guide（本地分析 + upstream mirror）。 |
| Community skills: kubernetes-patterns, deployment-patterns, gitops-workflow, latency-critical-systems, distributed-systems, tla-plus, quint-modeling, slo-implementation, incident-responder, eng-runbook, qdrant-scaling. | 社区 skill：kubernetes-patterns、deployment-patterns、gitops-workflow、latency-critical-systems、distributed-systems、tla-plus、quint-modeling、slo-implementation、incident-responder、eng-runbook、qdrant-scaling。 |
| Authoring method: `fastagent-meta-skill`. | 打包方法：`fastagent-meta-skill`。 |

## Security boundary / 安全边界

| English | 中文 |
|---|---|
| Advisory only; no infrastructure changes, cloud API calls, or secret reads. | 只做建议；不执行基础设施变更、不调用云 API、不读取 secret。 |
| Findings are recommendations; apply through normal change control. | findings 是建议；通过项目正常变更流程落地。 |

---

## 中文

以上各节已逐项对应英文；中文说明与左侧表格一致。

- **范围**：control plane、scheduler、存储、agent runtime、sandbox。
- **分层**：A–I infra checklist，J Rust API，K 评审 gate。
- **证据**：`E0–E3`；没有生产证据就标 `missing evidence`。
- **不做**：教程、UI/product 功能、渗透测试、合规认证。
- **安装**：`npx skills add ./cs-infra`（本地）或 `npx skills add tokenaissance/cs-infra`（发布后）。

## License

MIT (see [LICENSE](LICENSE) for copyright holders).
MIT，版权信息见 [LICENSE](LICENSE)。
