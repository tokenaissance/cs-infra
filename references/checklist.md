# CS Infra Review / Design Checklist

- 版本：0.1（候选）
- 日期：2026-11-04
- 定位：**单页 review/design checklist**，不是教程。
- 结构：**infra checklist + Google Rust code/API guide** 两层。
- 用法：设计评审逐项过；代码评审只看 J 节 + 对应 infra 节。
- 证据：每项尽量附 test / benchmark / ADR / runbook；无证据标 `missing evidence`。

---

## 0. 评审前：先写清楚

- [ ] 一句话说明系统做什么、不做什么。
- [ ] 明确 SLO：可用性、延迟、持久性、成本。
- [ ] 明确 failure domain：进程 / Sandbox / Machine / Store / region。
- [ ] 明确数据真相在哪里：Store / 外部数据库 / 对象存储。
- [ ] 明确控制面与数据面边界。
- [ ] 列出不变量（invariants）：什么永远不能发生。
- [ ] 列出非目标：这次明确不解决什么。

**证据**：ADR / design doc / issue。

---

## A. 正确性与形式化

- [ ] 关键状态机有显式状态，不用多个 bool 拼。
- [ ] 关键不变量写成可检查的断言或模型。
- [ ] 并发/分布式协议是否值得 TLA+ / Quint 建模？
- [ ] 模型是否覆盖：崩溃、重复消息、乱序、分区、超时。
- [ ] 是否有 safety + liveness 区分？
- [ ] 模型检查结果是否可复现（配置、边界、状态数）？

**适用**：共识、复制、leader election、lease、两阶段提交、任务调度。

**证据**：TLA+/Quint spec、TLC/Apalache 结果、反例。

---

## B. 架构与 failure domain

- [ ] 一张图能画出：控制面、数据面、Store、执行单元。
- [ ] 每个组件挂掉，blast radius 可枚举。
- [ ] 没有全局锁 / 全局队列 / 全局单点在热路径。
- [ ] 重试、超时、取消、drain 是协议的一部分。
- [ ] 失败是显式状态：`Unknown` / `Unresolved` / `Busy` / `Retained`。
- [ ] 失败不跨层归因：guest ≠ Sandbox ≠ Machine ≠ Store。
- [ ] 控制面拥有记录，数据面不读控制面 home。
- [ ] 计算可替换，历史不随计算漂移。

**LayerFS 映射**：Store / Branch / Workspace / Sandbox / Machine / Worker / Daemon。

---

## C. 数据、一致性与存储

- [ ] 明确一致性模型：线性一致 / 因果 / 最终一致。
- [ ] 明确 CAP/PACELC 取舍，以及分区时的行为。
- [ ] 写路径有 WAL / fsync / checksum / 原子 rename。
- [ ] 崩溃恢复可重放，且幂等。
- [ ] 快照有 manifest、base revision、完整性校验。
- [ ] 备份可恢复，不只是“备份成功”。
- [ ] 复制有 lag 指标和 failover 策略。
- [ ] 不做网络 SQLite；不把对象存储当活数据库。
- [ ] schema 迁移 expand/contract，可回滚。

**证据**：恢复演练、校验和、迁移脚本、复制 lag 面板。

---

## D. 容量、成本与背压

- [ ] 明确 scaling 目标：数据量 / QPS / 延迟 / 返回体积。
- [ ] 每个资源有 limit：CPU、内存、磁盘、连接、队列、in-flight。
- [ ] 有 headroom 目标（例如 30–50%），不是跑满。
- [ ] 队列有上限和 load shedding。
- [ ] 有 admission control，拒绝比无限排队好。
- [ ] 有单位成本模型：每请求 / 每 GB / 每 Sandbox-hour。
- [ ] idle 资源可回收；没有“永远在跑”的默认。
- [ ] 成本有归属标签：project / provider / machine / sandbox。

**证据**：压测、容量模型、成本 dashboard、load-shedding 测试。

---

## E. 发布、回滚与迁移

- [ ] 发布策略：rolling / blue-green / canary，选一个并写理由。
- [ ] 有 readiness / startup probe，失败不接流量。
- [ ] 有 rollback，且 rollback 被测试。
- [ ] 变更 backward-compatible；先 expand 后 contract。
- [ ] 配置与代码同仓库、同 review。
- [ ] 制品不可变：image digest、签名、SBOM。
- [ ] 数据迁移有 dry-run、校验、回滚路径。

**证据**：发布 runbook、回滚演练、迁移 dry-run 报告。

---

## F. 多区域与灾难恢复

- [ ] 明确 RPO / RTO。
- [ ] 明确 region failure 的行为：降级 / failover / 只读。
- [ ] 数据复制方向、冲突解决、split-brain 防护。
- [ ] DNS / 流量切换有 TTL 和回切策略。
- [ ] 定期做 restore / failover drill，不只做 backup。
- [ ] 区域间延迟和出网成本被测量。
- [ ] 数据主权 / 合规边界明确。

**证据**：DR drill 报告、RPO/RTO 实测、failover runbook。

---

## G. 可观测性与 SLO

- [ ] SLI 定义：可用性 / 延迟 / 持久性 /  freshness。
- [ ] SLO 目标与 error budget 明确。
- [ ] 指标拆 p50/p95/p99，不只看平均。
- [ ] 队列深度、in-flight、重试率、超时率可观测。
- [ ] trace 跨控制面/数据面；日志带 correlation id。
- [ ] 告警高信号，绑定 runbook。
- [ ] 能回答：现在几个、在跑什么、为什么失败、影响谁。

**证据**：dashboard、SLO 报告、告警演练。

---

## H. 事故响应与 on-call

- [ ] 每个服务有 owner、severity tier、on-call rotation。
- [ ] 前 5 分钟：定级、指挥、止血、沟通。
- [ ] 有 rollback / feature flag / 限流 / 切流手段。
- [ ] 状态更新节奏固定（例如 15 分钟）。
- [ ] 有 incident timeline、决策记录、影响指标。
- [ ] 事后有 postmortem、action item、owner、截止日期。
- [ ] 真实 on-call 数据进入复盘，不只靠模拟。

**证据**：runbook、incident review、on-call 反馈。

---

## I. 安全与隔离

- [ ] 最小权限：每个 workload 独立身份。
- [ ] 默认拒绝网络，显式放行。
- [ ] 不可信代码进 Sandbox / namespace / VM。
- [ ] guest 不读控制面 home / secrets。
- [ ] 密钥不落日志、不进镜像、不进 prompt。
- [ ] 供应链：digest、签名、SBOM、依赖扫描。
- [ ] destructive 操作有确认 / freeze / kill switch。

**证据**：威胁模型、权限矩阵、渗透/隔离测试。

---

## J. Rust code / API 层（Google Rust Style Guide）

- [ ] 状态用 enum，不用多个 bool。
- [ ] 预期失败用 `Result`，不 panic；`expect` 只用于不变量。
- [ ] 公共 enum/struct 用 `#[non_exhaustive]` 留扩展。
- [ ] receipt / guard / handle / status 用 `#[must_use]`。
- [ ] 入参借用优先：`&str` / `&[T]` / `impl Iterator`。
- [ ] unsafe 有 `SAFETY:` 注释：invariant、生命周期、谁保证。
- [ ] 并发原语显式；mutex poison 有处理；blocking I/O 不进 async 热路径。
- [ ] 公开 API 文档写 `# Safety` / `# Panics` / `# Errors` / 取消语义。
- [ ] 禁止 glob import；小 crate、扁平模块。
- [ ] 生成代码与手写代码分开。

**参考**：`google-rust-styleguide-plan.md`、`google-rust-styleguide/upstream-source/rustguide.md`。

---

## K. 评审 gate

### 设计评审必须回答

- [ ] failure domain 是什么？
- [ ] 数据真相在哪里？
- [ ] 幂等键是什么？
- [ ] 队列上限多少？满了怎么办？
- [ ] 超时/取消/drain 语义？
- [ ] 失败后状态是什么？
- [ ] 怎么回滚？
- [ ] 怎么观测？
- [ ] 成本怎么算？
- [ ] 哪个不变量用 TLA+/Quint 检查过？

### 代码评审必须回答

- [ ] 状态是否 enum？
- [ ] 错误是否带上下文？
- [ ] unsafe 是否有 SAFETY？
- [ ] 公共 API 是否可扩展？
- [ ] 是否有无界队列/无界重试？
- [ ] 是否有阻塞 I/O 在 async 热路径？
- [ ] 测试是否覆盖失败路径？

### 证据等级

| 等级 | 含义 |
|---|---|
| E0 | 口头/设计文档 |
| E1 | 单元/集成测试 |
| E2 | 故障注入 / 压测 / 恢复演练 |
| E3 | 生产观测 / on-call 数据 / 形式化验证 |

没有 E2/E3 的关键路径，标 `missing evidence`。

---

## 来源

- `kubernetes-patterns`（affaan-m/ECC）
- `deployment-patterns`（affaan-m/ECC）
- `gitops-workflow`（wshobson/agents）
- `latency-critical-systems`（affaan-m/ECC）
- `enterprise-agent-ops`（affaan-m/ECC）
- `distributed-systems`（FerroxLabs）
- `tla-plus`（apache/cassandra）
- `quint-modeling` / `quint-lang`（quint-co）
- `slo-implementation`（wshobson/agents）
- `incident-responder`（davila7）
- `eng-runbook`（nexu-io）
- `qdrant-scaling`（github/awesome-copilot）
- `mysql-patterns` / `database-migrations`（affaan-m/ECC）
- Google Rust Style Guide（本地）

## 仍未覆盖

- 存储引擎 internals（B-tree/LSM/WAL/compaction）——没有找到专门 skill，需第一性原理 + 论文/实现。
- 真实 on-call 数据——只能靠组织自己的 incident 记录。
- 成本模型——只有云厂商 FinOps 片段，没有通用单位经济模型。
- 共识实现的工程细节——有概念 skill，但缺 Jepsen/故障注入实操。
- 跨区域数据主权/合规——需按地区法务确认。

## 结论

> **不是“从零造一个 CS infra skill”，而是：**
> **infra checklist（A–I）+ Google Rust code/API guide（J）+ 评审 gate（K）。**
>
> 这个 checklist 可以直接作为 `cs-infra` 的 review 主体；Rust 细节引用本地 guide，避免规则漂移。
