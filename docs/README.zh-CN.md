# CS Infra

[![English](https://img.shields.io/badge/Docs-English-black)](../README.md)
[![中文](https://img.shields.io/badge/Docs-%E4%B8%AD%E6%96%87-red)](README.zh-CN.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-black.svg)](../LICENSE)

> 评审 CS infra 设计与 Rust 实现，不是教程。

`cs-infra` 是一个面向 control plane、scheduler、存储服务、agent runtime 和 sandbox 平台的 review/design checklist。

## 覆盖范围

- failure domain 与 blast radius
- 幂等、lease、有界队列
- 数据、一致性、存储、恢复
- 容量、成本、背压
- 发布、回滚、迁移
- 多区域与灾难恢复
- SLO、可观测性、on-call、事故响应
- 安全与隔离
- Google Rust Style Guide 的 Rust API 规则

## 你可以直接这样说

- “帮我 review 这个 control plane 的 failure domain 和幂等设计。”
- “帮我 review 这个分布式调度器的 capacity、failover 和 on-call。”
- “Review this Rust sandbox API for unsafe、错误处理和可扩展性。”
- “给这个存储服务写一份 production readiness checklist。”

## 输出

```text
## Verdict
## Blockers (P0)
## Should fix (P1)
## Missing evidence
## Checklist coverage
```

findings 与 missing input 分开；证据等级 `E0–E3` 必须明确；没有证据就写 `missing evidence`。

## 目录

```text
SKILL.md                 routing + review protocol
references/checklist.md  A–K full checklist
references/rust-api.md   Rust code/API review rules
references/sources.md    sources + known gaps
evals/trigger_cases.json trigger boundaries
agents/interface.yaml    adapter metadata
reports/                 evidence and handoff
```

## 安装

```bash
npx skills add tokenaissance/cs-infra
```

本地 checkout：

```bash
npx skills add ./cs-infra
```

## 前置条件

- [ ] Node.js 与 npx 已安装：`node --version && npx --version`
- [ ] Python 3 已安装：`python3 --version`
- [ ] 已检查 skill 权限与风险边界

## 验证

```bash
python3 ~/.agents/skills/cs-infra/scripts/validate_skill.py ~/.agents/skills/cs-infra
```

或本地：

```bash
python3 /Users/reina/.agents/skills/fastagent-meta-skill/scripts/validate_skill.py .
```

## Troubleshooting

| 问题 | 原因 | 修复 |
|---|---|---|
| skill 不触发 | description 缺 `infra`/`review`/`rust` | 改 description 后重跑 trigger eval |
| 评审太泛 | finding 没有具体 failure mode | 改写成“什么条件下、什么会坏” |
| Rust 规则漂移 | 规则被复制进 `SKILL.md` | 保留在 `references/rust-api.md` |
| 没报 missing evidence | checklist 没标证据等级 | 每个关键项要求 `E0–E3` |

## 设计原则

- **两层**：infra checklist + Rust guide；Rust 规则不重复。
- **证据优先**：测试通过不等于生产观测。
- **写 failure mode**：说清什么条件下、什么会坏。
- **根目录保持小**：细节放 `references/`。

## 致谢

- Google Rust Style Guide（本地分析 + upstream mirror）。
- 社区 skill：kubernetes-patterns、deployment-patterns、gitops-workflow、latency-critical-systems、distributed-systems、tla-plus、quint-modeling、slo-implementation、incident-responder、eng-runbook、qdrant-scaling。
- 打包方法：`fastagent-meta-skill`。

## 安全边界

本 skill 只做评审建议，不执行基础设施变更、不调用云 API、不读取 secret。发现项需通过项目正常变更流程落地。

## License

MIT（版权信息见 [LICENSE](../LICENSE)）。
