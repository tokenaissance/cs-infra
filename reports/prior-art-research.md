# CS Infra 编写最佳实践：FastAgent Meta Skill 先验调研

- 调研日期：2026-11-04
- 方法：`fastagent-meta-skill/scripts/research_prior_art.py` + `search_skillsmp.py`
- 查询：
  - computer systems infrastructure engineering best practices
  - distributed systems infrastructure design
  - cloud infrastructure control plane architecture
  - production systems programming reliability
  - kubernetes operator
  - infrastructure as code
  - storage engine database internals
  - site reliability engineering
  - systems programming rust
- 证据边界：skills.sh 因本机 npm cache 权限失败（`EPERM /Users/reina/.npm/_cacache`），未取得安装量；SkillsMP 可用。以下 star 数是源仓库 star，不是 skill 评分或安装量。

## 候选（去重后真正相关）

| 候选 | 来源 | 相关性 | 可借 |
|---|---|---|---|
| `kubernetes-patterns` | affaan-m/ECC | K8s workload、probes、RBAC、HPA/PDB、资源 limits | 声明式、探针、最小权限、资源边界 |
| `deployment-patterns` | affaan-m/ECC | rolling/blue-green/canary、Docker、healthcheck、rollback | 渐进发布、回滚、生产就绪 |
| `gitops-workflow` | wshobson/agents | OpenGitOps 四原则、ArgoCD/Flux、reconcile | desired state、版本化、持续调谐 |
| `latency-critical-systems` | affaan-m/ECC | p50/p95/p99、热路径、队列深度、backpressure | 指标拆分、热路径测量、背压 |
| `enterprise-agent-ops` | affaan-m/ECC | 长生命周期 runtime、可观测、kill switch、rollout | 生命周期、least privilege、审计 |
| `helm-chart-scaffolding` | wshobson/agents | Helm 模板、values、可复用部署 | 参数化、可重复构建 |
| `k8s-security-policies` | wshobson/agents | NetworkPolicy、RBAC、PodSecurity | 安全边界 |
| `safety-guard` | affaan-m/ECC | destructive command 拦截、freeze | 变更保护 |

## 提炼出的 12 条 CS Infra 编写最佳实践

1. **Desired state 先于命令式操作**
   - 先定义目标状态，再让 reconciler 收敛。
   - 失败可重入，不依赖“上一条命令成功”。

2. **明确 failure domain 与 blast radius**
   - 一个进程/节点/租户/Store 挂掉，影响范围必须可枚举。
   - 不把全局锁、全局队列、全局单点塞进热路径。

3. **幂等与可重入**
   - 每个写操作有 idempotency key 或 revision。
   - 重试不产生第二个副作用；无法确认时进入 `Unknown`，而不是猜。

4. **有界资源**
   - CPU/memory/disk/queue/connections 都有 limit。
   - 有 backpressure；队列不能无限增长。
   - 超时、取消、drain 是协议的一部分。

5. **生命周期显式**
   - create/start/ready/drain/stop/failed 状态机。
   - graceful shutdown：停止接收、排空、超时、强制。
   - 启动探针与 readiness 分离。

6. **可观测性是接口**
   - p50/p95/p99、吞吐、错误率、队列深度、freshness。
   - 日志带 correlation id；trace 跨控制面/数据面。
   - 能回答“现在有几个、在跑什么、为什么失败”。

7. **控制面/数据面分离**
   - 控制面拥有记录与意图；数据面只执行。
   - 数据面不读控制面 home；不把数据库当网络文件系统。
   - 计算可替换，数据/历史不随计算漂移。

8. **渐进发布与可回滚**
   - rolling/blue-green/canary；先小流量。
   - 迁移必须 backward-compatible；expand/contract。
   - 每次变更可回滚，回滚本身被测试。

9. **最小权限与隔离**
   - 每个 workload 独立身份；RBAC 最小化。
   - 不可信代码放进独立 Sandbox/namespace/VM。
   - 默认拒绝网络；显式放行。

10. **不可变制品与可重复构建**
    - 镜像/二进制按 digest 固定，不用 `latest`。
    - 构建可重复；依赖锁定；SBOM/签名。
    - 配置与代码同仓库、同 review。

11. **测试失败路径**
    - 单元测试之外：集成、故障注入、chaos、恢复演练。
    - 测“进程被杀/网络断/磁盘满/队列堵/依赖超时”，不只测 happy path。
    - 每个 SLO 有对应验收。

12. **Runbook 与决策记录**
    - 每个告警有 runbook；每个架构取舍有 ADR。
    - 记录“为什么不做”，避免后来者重复踩坑。
    - on-call 能在 5 分钟内判断 blast radius 和止血动作。

## 对 LayerFS 的直接映射

| 原则 | LayerFS 落点 |
|---|---|
| desired state | Branch/Commit/record `op` intent |
| failure domain | Machine / Sandbox / Workspace / Store 分层 |
| idempotency | commit trailer + unique index；no retry/replay |
| bounded resources | admission / capacity / control slot / queue depth |
| lifecycle | Sandbox state machine + idle TTL + drain |
| observability | B8/B10/B9；machine/sandbox list/get、doctor、worker health |
| control/data split | Store 拥有历史；guest 不读 home；no network SQLite |
| progressive rollout | provider/backend canary；Branch 级回滚 |
| least privilege | guest namespace/container/VM；no home |
| immutable artifacts | image digest；Store snapshot manifest/checksum |
| failure testing | kill -9、断网、磁盘满、provider eviction |
| runbook/ADR | #533/#545 + docs/issues |

## 结论

- 没有找到“CS infra 编写最佳实践”的单一权威 skill；只有 Kubernetes、GitOps、部署、延迟敏感系统等相邻 skill。
- 最值得吸收的机制是：**desired state + reconciliation、failure domain、bounded resources、observability、control/data separation、progressive delivery**。
- 如果要沉淀成 FastAgent skill，建议命名 `cs-infra`，定位为“review/design checklist”，而不是教程百科；核心应围绕 failure domain、idempotency、backpressure、observability、rollout/rollback。
- 缺口：共识/复制、存储引擎 internals、形式化验证、容量规划、成本模型、跨区域故障切换，现有候选覆盖不足。

## 缺失证据

- skills.sh 安装量：未取得（npm cache EPERM）。
- 候选 skill 的实际使用反馈/评分：未取得。
- 部分候选的维护活跃度与许可证：未逐一核验。

---

## 本地补充：Google Rust Style Guide

之前只搜了 SkillsMP / skills.sh，漏掉本地已有的一份重要来源：

- `/Users/reina/Project/google-rust-styleguide-plan.md`
- `/Users/reina/Project/google-rust-styleguide/`
  - `upstream-source/rustguide.md`（Google Style Guides 的 Rust 页）
  - `MANIFEST.json`、`LICENSE`、`site/`

### 定位

它不是“CS infra 架构指南”，而是 **Rust 代码/API 级规范**。
和前面的 infra checklist 是两层，不冲突：

```text
CS infra checklist   = failure domain / idempotency / bounded / observability / rollout
Google Rust guide    = API 形状 / ownership / errors / concurrency / unsafe / docs
```

### 对 infra Rust 最相关的规则

1. **用 enum 表达状态，不用 bool**
   - `ExecStatus { Ok, Failed, TimedOut, Cancelled }`
   - `SandboxState { Creating, Ready, Draining, Closed, Unresolved }`
   - 避免 `is_running: bool` 这类不可扩展状态。

2. **错误是返回值，不是 panic**
   - 预期失败用 `Result`；
   - `expect("...")` 只用于不变量；
   - 错误带上下文，不吞掉。

3. **公共 API 稳定**
   - `#[non_exhaustive]` 用于会扩展的 enum/struct（provider capabilities、status、config）；
   - `#[must_use]` 用于 receipt、guard、status、handle。

4. **借用优先**
   - 入参用 `&str` / `&[T]` / `impl Iterator`；
   - 不为了省事 clone；
   - 但 infra 热点要按测量决定，不盲目。

5. **unsafe 必须有 SAFETY 证明**
   - mount / namespace / exec / fd passing 的 unsafe 块；
   - 注释写清 invariant、生命周期、谁保证；
   - 这是 infra 代码 review 的重点。

6. **并发原语显式**
   - 不用隐式全局状态；
   - mutex poison 要处理；
   - 明确 async/thread 边界；
   - 不把 blocking I/O 放进 async 热路径。

7. **文档是 API 的一部分**
   - 公开 API 写清 panic、unsafe、错误、取消语义；
   - `# Safety` / `# Panics` / `# Errors`；
   - 对 infra 来说，“失败时留下什么状态”必须写。

8. **代码组织**
   - 小 crate、扁平模块；
   - 禁止 glob import；
   - import 明确；
   - 生成代码与手写代码分开。

### 对拟建 skill 的影响

不应该把 Google Rust 规则复制进 `cs-infra`。
更好的结构是：

```text
cs-infra
  → 架构/可靠性 checklist
  → 引用 Google Rust guide 作为 code-level review

google-rust-style (local/reference)
  → API/ownership/errors/concurrency/unsafe/docs
```

如果做 skill，建议：

```text
name: cs-infra
description: Review CS infrastructure design and Rust implementation for
failure domains, idempotency, bounded resources, observability,
control/data separation, rollout/rollback, and Google Rust API rules.
```

但 `cs-infra` 只保留“infra 特有判断”，Rust 细节引用本地 guide，避免两套规则漂移。

### 结论修正

> 之前说“没有权威 CS infra skill”仍然成立；
> 但本地已有 **Google Rust Style Guide**，它补上了 code/API 层。
> 所以最终不是“从零造一个”，而是“infra checklist + 本地 Rust guide”两层组合。
