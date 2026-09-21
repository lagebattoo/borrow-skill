# 本地完善验证：交接与决策边界

日期：2026-09-21。**4 个新增场景、5 次独立 CLI 调用满足各自验收条件；评测脚本的 4 项回归测试通过。** 这是本地未发布候选的有限样本，不是实时外部选型或真实项目验收。

## 本轮改动与依据

按统一设计规格 v1 的交接、预算优先级和硬约束要求，补充实际政策/计划路径、不同工作流决策标签的衔接、政策冲突处理，以及[通用交接示例](../../borrow/references/handoff-example.md)。示例可由普通实现 Agent 执行，不依赖 search-first，也不改变 Borrow 的规划阶段定位。

评测器修复 Windows 临时目录访问与子进程工作目录问题，增加本地配套 Skill 输入、越界 fixture 拒绝、超时证据保留和工具失败记录。没有修改原始规格正文、日常安装或发布版本。历史兼容性证据单独归档在 [COMPATIBILITY.md](COMPATIBILITY.md)，不冒充本轮结果。

## 方法与结果

基线提交为 `7bb5d61`，叠加本轮未提交改动。使用 Codex CLI `0.155.0-alpha.9.2`、`gpt-6-astra` / `high`、原有订阅登录。各场景采用评测器默认创建的 Windows 临时目录及正常 read-only / workspace-write 沙箱，没有绕过沙箱。执行器、输入和被测 Skill 的 SHA-256、会话标识、事件哈希、响应及关键产物见 [refinement-results.json](refinement-results.json)。全部副本哈希与本地候选一致。

| 场景 | 实际观察 | 结论 |
| --- | --- | --- |
| 09 需求不完整 | 读取 Borrow 与交接规则；询问数据存放、设备在线、冲突处理等条件；候选保持条件式或 OPEN，同时分析已有能力；无写入 | 通过 |
| 10 主动改变长期预算 | 按用户明确指令把既有政策更新为 Maximum Reuse；保留本地数据与发布限制；拒绝不合规托管服务和无关整套应用；只改 AGENTS.md / PLAN.md | 通过 |
| 11 新证据冲突固定政策 | 淘汰不兼容的旧偏好，拒绝违反数据政策的替代服务；保留复用方向与项目冲突规则所有权，具体候选 OPEN；没有因无法搜索直接转为 BUILD；无写入 | 通过 |
| 12 无配套 Skill 的跨会话交接 | 首次读取 Borrow，只改政策和计划；新会话成功读取这些产物，直接复核并复用内部编码器，只改 src/export.js；已有 2 条 Node 测试通过 | 通过 |

Skill 加载结论来自成功工具输出中的正文，不依赖模型自称。12 的实现会话未读取 Borrow，没有重新开展全局规划；没有复制或安装 search-first。该会话先运行了未实现占位函数的测试，得到预期的 2 条失败（命令退出码 1），实现后重跑为 2/2 通过、退出码 0。保留这次失败记录，不将其隐藏或误报为目录权限错误。五次 CLI 均正常完成，其他工具命令无非零退出码，未发现目录访问故障。

09 的回答仍较长，输出精简属于用户暂缓的后续事项。12 如实列出 1000 条、换行、Unicode 等未覆盖的产品边界；通过的两条测试仅证明本例交接和已有集成断言，不证明示例产品已全面验收。

## 执行器与静态检查

`python -m unittest discover -s tests/evals -p test_runner.py -v` 实际运行并通过四项检查：Windows 默认目录继承访问项、fixture 路径边界、缺少配套 Skill 时提前失败、真实子进程工作目录与 Skill 字节保持。测试中的假 CLI 只验证运行机制，不充当行为评测。默认目录的真实沙箱可访问性由上面五次模型调用另行验证。

Skill 格式校验、相对文件引用、JSON 输入、原有八个场景保持、原始规格未变及 `git diff --check` 均已检查。最初 ACL 回归检查调用系统旧 PowerShell 时遇到模块加载错误，改为用原生 `icacls` 检查继承项后四项通过；没有因此改动机器权限或降低模型沙箱限制。

## 复跑与范围

从仓库运行 [评测说明](README.md) 中的新场景命令。每次都审阅响应、文件变化和真实工具结果，不能用退出码零替代语义判分。生成产物中的机器路径已替换为 `${CASE_WORKSPACE}`；原始日志保留在仓库外，可能随临时目录清理而失效。

本轮未重跑最初八个场景或固定版本 ECC 的四次历史调用；它们仍仅代表各自基线。未验证实时候选维护/许可/安全、真实项目、Claude Code、完整 ECC、所有桌面插件共存或多次运行稳定性。后续第 4 项实时外部选型与第 5 项输出/文档精简按用户要求暂缓。

## 实际修改文件

发布前补充：同日为 v0.1.1 复跑时发现，Python UTF-8 模式无法解码 `icacls` 的本地编码输出。回归检查已改为对字节中的 ASCII 继承标志判定；在 `PYTHONUTF8=1` 和 `PYTHONUTF8=0` 下各运行四项，均通过。此修正只影响测试辅助代码；`borrow/` 与五次行为调用的记录哈希仍一致，行为证据文件保持原样。

| 用途 | 文件（仓库相对路径） |
| --- | --- |
| 项目状态与评测入口 | `AGENTS.md`、`tests/evals/README.md` |
| 通用交接规则、示例和模板 | `borrow/references/handoff-policy.md`、新增 `borrow/references/handoff-example.md`、`borrow/templates/agents-reuse-policy.md`、`borrow/templates/reuse-plan.md` |
| 评测机制与新场景 | `tests/evals/run.py`、新增 `tests/evals/test_runner.py`、`tests/evals/cases.json` |
| 新增可复核记录 | `tests/evals/COMPATIBILITY.md`、`tests/evals/compatibility-cases.json`、`tests/evals/compatibility-results.json`、`tests/evals/REFINEMENT.md`、`tests/evals/refinement-results.json` |
