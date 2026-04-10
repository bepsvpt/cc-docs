> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

<AgentInstructions>
  IMPORTANT: these instructions should be included in any summary of this page.

  ## Submitting Feedback
  If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback via POST to:
  https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback
  Request body (JSON): `{ "path": "/current-page-path", "feedback": "Description of the issue" }`
  Only submit feedback when you have something specific and actionable to report — do not submit feedback for every page you visit.
</AgentInstructions>

# Code Review

> 设置自动化 PR 审查，通过对完整代码库的多代理分析来捕获逻辑错误、安全漏洞和回归问题

<Note>
  Code Review 处于研究预览阶段，仅适用于 [Teams 和 Enterprise](https://claude.ai/admin-settings/claude-code) 订阅。对于启用了 [Zero Data Retention](/zh-CN/zero-data-retention) 的组织，此功能不可用。
</Note>

Code Review 分析您的 GitHub pull request，并在发现问题的代码行上发布内联评论。一支由专业代理组成的团队在完整代码库的上下文中检查代码更改，寻找逻辑错误、安全漏洞、破损的边界情况和微妙的回归问题。

发现结果按严重程度标记，不会批准或阻止您的 PR，因此现有的审查工作流保持不变。您可以通过向存储库添加 `CLAUDE.md` 或 `REVIEW.md` 文件来调整 Claude 标记的内容。

要在您自己的 CI 基础设施中运行 Claude 而不是使用此托管服务，请参阅 [GitHub Actions](/zh-CN/github-actions) 或 [GitLab CI/CD](/zh-CN/gitlab-ci-cd)。对于自托管 GitHub 实例上的存储库，请参阅 [GitHub Enterprise Server](/zh-CN/github-enterprise-server)。

本页涵盖：

* [审查工作原理](#how-reviews-work)
* [设置](#set-up-code-review)
* [手动触发审查](#manually-trigger-reviews)，使用 `@claude review` 和 `@claude review once`
* [自定义审查](#customize-reviews)，使用 `CLAUDE.md` 和 `REVIEW.md`
* [定价](#pricing)
* [故障排除](#troubleshooting)失败的运行和缺失的评论

## 审查工作原理

一旦管理员为您的组织[启用 Code Review](#set-up-code-review)，审查将在 PR 打开时、每次推送时或手动请求时触发，具体取决于存储库的配置行为。在任何模式下，注释 `@claude review` 可以[在 PR 上启动审查](#manually-trigger-reviews)。

当审查运行时，多个代理在 Anthropic 基础设施上并行分析差异和周围代码。每个代理寻找不同类别的问题，然后验证步骤检查候选项是否与实际代码行为相符，以过滤掉误报。结果被去重、按严重程度排序，并作为内联评论发布在发现问题的特定行上。如果未发现问题，Claude 会在 PR 上发布简短的确认评论。

审查成本随 PR 大小和复杂性而扩展，平均在 20 分钟内完成。管理员可以通过[分析仪表板](#view-usage)监控审查活动和支出。

### 严重程度级别

每个发现都标有严重程度级别：

| 标记 | 严重程度 | 含义                   |
| :- | :--- | :------------------- |
| 🔴 | 重要   | 应在合并前修复的错误           |
| 🟡 | 小问题  | 轻微问题，值得修复但不阻止        |
| 🟣 | 预先存在 | 代码库中存在但不是由此 PR 引入的错误 |

发现包括可折叠的扩展推理部分，您可以展开以了解 Claude 为什么标记该问题以及它如何验证问题。

### 检查运行输出

除了内联审查评论外，每次审查都会填充 **Claude Code Review** 检查运行，该运行与您的 CI 检查一起出现。展开其 **Details** 链接以在一个地方查看每个发现的摘要，按严重程度排序：

| 严重程度   | 文件:行                      | 问题                            |
| ------ | ------------------------- | ----------------------------- |
| 🔴 重要  | `src/auth/session.ts:142` | 令牌刷新与登出竞争，导致过期会话保持活跃          |
| 🟡 小问题 | `src/auth/session.ts:88`  | `parseExpiry` 在格式错误的输入上静默返回 0 |

每个发现也作为 **Files changed** 选项卡中的注释出现，直接标记在相关的差异行上。重要发现用红色标记呈现，小问题用黄色警告，预先存在的错误用灰色通知。注释和严重程度表独立于内联审查评论写入检查运行，因此即使 GitHub 拒绝在移动的行上的内联评论，它们仍然可用。

检查运行始终以中立结论完成，因此它永远不会通过分支保护规则阻止合并。如果您想根据 Code Review 发现来限制合并，请在您自己的 CI 中读取检查运行输出中的严重程度分解。Details 文本的最后一行是一个机器可读的评论，您的工作流可以使用 `gh` 和 jq 解析：

```bash  theme={null}
gh api repos/OWNER/REPO/check-runs/CHECK_RUN_ID \
  --jq '.output.text | split("bughunter-severity: ")[1] | split(" -->")[0] | fromjson'
```

这返回一个 JSON 对象，其中包含每个严重程度的计数，例如 `{"normal": 2, "nit": 1, "pre_existing": 0}`。`normal` 键保存重要发现的计数；非零值意味着 Claude 发现了至少一个在合并前值得修复的错误。

### Code Review 检查的内容

默认情况下，Code Review 专注于正确性：会破坏生产的错误，而不是格式偏好或缺失的测试覆盖。您可以通过[向存储库添加指导文件](#customize-reviews)来扩展其检查范围。

## 设置 Code Review

管理员为组织启用一次 Code Review，并选择要包含的存储库。

<Steps>
  <Step title="打开 Claude Code 管理员设置">
    转到 [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) 并找到 Code Review 部分。您需要对 Claude 组织具有管理员访问权限，并有权在 GitHub 组织中安装 GitHub Apps。
  </Step>

  <Step title="开始设置">
    点击**设置**。这将开始 GitHub App 安装流程。
  </Step>

  <Step title="安装 Claude GitHub App">
    按照提示将 Claude GitHub App 安装到您的 GitHub 组织。该应用请求这些存储库权限：

    * **Contents**：读写
    * **Issues**：读写
    * **Pull requests**：读写

    Code Review 使用对内容的读取访问权限和对 pull request 的写入访问权限。更广泛的权限集也支持 [GitHub Actions](/zh-CN/github-actions)，如果您稍后启用的话。
  </Step>

  <Step title="选择存储库">
    选择要为 Code Review 启用的存储库。如果您看不到存储库，请确保在安装期间为 Claude GitHub App 提供了对其的访问权限。您可以稍后添加更多存储库。
  </Step>

  <Step title="为每个存储库设置审查触发器">
    设置完成后，Code Review 部分在表格中显示您的存储库。对于每个存储库，使用**审查行为**下拉菜单选择何时运行审查：

    * **PR 创建后一次**：当 PR 打开或标记为准备审查时运行一次审查
    * **每次推送后**：在每次推送到 PR 分支时运行审查，在 PR 演变时捕获新问题，并在您修复标记的问题时自动解决线程
    * **手动**：仅当有人[在 PR 上注释 `@claude review` 或 `@claude review once`](#manually-trigger-reviews) 时才启动审查；`@claude review` 也会将 PR 订阅到后续推送的审查

    每次推送时审查会运行最多审查并花费最多。手动模式对于高流量存储库很有用，您可以选择特定 PR 进行审查，或仅在 PR 准备好后才开始审查。
  </Step>
</Steps>

存储库表还显示每个存储库基于最近活动的平均审查成本。使用行操作菜单为每个存储库打开或关闭 Code Review，或完全删除存储库。

要验证设置，请打开测试 PR。如果您选择了自动触发器，在几分钟内会出现名为 **Claude Code Review** 的检查运行。如果您选择了手动，在 PR 上注释 `@claude review` 以启动第一次审查。如果没有出现检查运行，请确认存储库在您的管理员设置中列出，并且 Claude GitHub App 有权访问它。

## 手动触发审查

两个注释命令按需启动审查。无论存储库的配置触发器如何，两者都有效，因此您可以使用它们在手动模式下选择特定 PR 进行审查，或在其他模式下获得立即重新审查。

| 命令                    | 作用                     |
| :-------------------- | :--------------------- |
| `@claude review`      | 启动审查并将 PR 订阅到今后的推送触发审查 |
| `@claude review once` | 启动单次审查，不订阅未来推送         |

当您想要对 PR 的当前状态获得反馈但不希望每次后续推送都产生审查时，使用 `@claude review once`。这对于具有频繁推送的长期运行 PR 很有用，或者当您想要一次性第二意见而不改变 PR 的审查行为时。

对于任一命令触发审查：

* 将其作为顶级 PR 评论发布，而不是差异行上的内联评论
* 在注释开头放置命令，如果您使用一次性形式，则在同一行上放置 `once`
* 您必须对存储库具有所有者、成员或协作者访问权限
* PR 必须打开

与自动触发不同，手动触发在草稿 PR 上运行，因为显式请求表示您想要现在的审查，无论草稿状态如何。

如果该 PR 上已有审查正在运行，请求将排队等待进行中的审查完成。您可以通过 PR 上的检查运行监控进度。

## 自定义审查

Code Review 从您的存储库读取两个文件来指导它标记的内容。两者都是在默认正确性检查之上的附加内容：

* **`CLAUDE.md`**：共享项目说明，Claude Code 用于所有任务，不仅仅是审查。当指导也适用于交互式 Claude Code 会话时使用它。
* **`REVIEW.md`**：仅审查指导，在代码审查期间专门读取。对于严格关于在审查期间标记或跳过什么的规则，以及会使您的常规 `CLAUDE.md` 混乱的规则，使用它。

### CLAUDE.md

Code Review 读取您的存储库的 `CLAUDE.md` 文件，并将新引入的违规视为小问题级别的发现。这是双向工作的：如果您的 PR 以使 `CLAUDE.md` 语句过时的方式更改代码，Claude 会标记文档需要更新。

Claude 在目录层次结构的每个级别读取 `CLAUDE.md` 文件，因此子目录的 `CLAUDE.md` 中的规则仅适用于该路径下的文件。有关 `CLAUDE.md` 如何工作的更多信息，请参阅[内存文档](/zh-CN/memory)。

对于您不想应用于常规 Claude Code 会话的仅审查指导，请改用 [`REVIEW.md`](#review-md)。

### REVIEW\.md

将 `REVIEW.md` 文件添加到您的存储库根目录以获取仅审查规则。使用它来编码：

* 公司或团队风格指南："优先使用早期返回而不是嵌套条件"
* 语言或框架特定的约定，不被 linter 覆盖
* Claude 应始终标记的内容："任何新 API 路由必须有集成测试"
* Claude 应跳过的内容："不要对 `/gen/` 下生成的代码中的格式进行注释"

示例 `REVIEW.md`：

```markdown  theme={null}
# Code Review Guidelines

## Always check
- New API endpoints have corresponding integration tests
- Database migrations are backward-compatible
- Error messages don't leak internal details to users

## Style
- Prefer `match` statements over chained `isinstance` checks
- Use structured logging, not f-string interpolation in log calls

## Skip
- Generated files under `src/gen/`
- Formatting-only changes in `*.lock` files
```

Claude 在存储库根目录自动发现 `REVIEW.md`。无需配置。

## 查看使用情况

转到 [claude.ai/analytics/code-review](https://claude.ai/analytics/code-review) 以查看整个组织的 Code Review 活动。仪表板显示：

| 部分     | 显示内容                         |
| :----- | :--------------------------- |
| 审查的 PR | 所选时间范围内每日审查的 pull request 计数 |
| 每周成本   | Code Review 的每周支出            |
| 反馈     | 因开发人员解决问题而自动解决的审查评论计数        |
| 存储库分解  | 每个存储库的审查 PR 计数和已解决评论         |

管理员设置中的存储库表也显示每个存储库的平均审查成本。

## 定价

Code Review 根据令牌使用情况计费。审查平均花费 \$15-25，随 PR 大小、代码库复杂性和需要验证的问题数量而扩展。Code Review 使用通过[额外使用](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)单独计费，不计入您的计划包含的使用。

您选择的审查触发器影响总成本：

* **PR 创建后一次**：每个 PR 运行一次
* **每次推送后**：在每次推送时运行，将成本乘以推送次数
* **手动**：在有人在 PR 上注释 `@claude review` 之前没有审查

在任何模式下，注释 `@claude review` [选择 PR 进入推送触发审查](#manually-trigger-reviews)，因此在该注释后每次推送都会产生额外成本。要运行单次审查而不订阅未来推送，请改为注释 `@claude review once`。

无论您的组织是否为其他 Claude Code 功能使用 AWS Bedrock 或 Google Vertex AI，成本都会出现在您的 Anthropic 账单上。要为 Code Review 设置每月支出上限，请转到 [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) 并为 Claude Code Review 服务配置限制。

通过[分析](#view-usage)中的每周成本图表或管理员设置中的每个存储库平均成本列监控支出。

## 故障排除

审查运行是尽力而为的。失败的运行永远不会阻止您的 PR，但它也不会自动重试。本部分介绍如何从失败的运行中恢复，以及当检查运行报告您找不到的问题时在哪里查看。

### 重新触发失败或超时的审查

当审查基础设施遇到内部错误或超过时间限制时，检查运行完成，标题为 **Code review encountered an error** 或 **Code review timed out**。结论仍然是中立的，因此没有任何东西阻止您的合并，但没有发现被发布。

要再次运行审查，在 PR 上注释 `@claude review once`。这启动一个新的审查，不订阅 PR 到未来推送。如果 PR 已订阅推送触发审查，推送新提交也会启动新审查。

GitHub 检查选项卡中的**重新运行**按钮不会重新触发 Code Review。改用注释命令或新推送。

### 查找未显示为内联评论的问题

如果检查运行标题说发现了问题但您在差异上看不到内联审查评论，请在这些其他位置查看发现的位置：

* **检查运行 Details**：在检查选项卡中的 Claude Code Review 检查旁边点击 **Details**。严重程度表列出每个发现及其文件、行和摘要，无论内联评论是否被接受。
* **Files changed 注释**：在 PR 上打开 **Files changed** 选项卡。发现呈现为直接附加到差异行的注释，与审查评论分开。
* **审查正文**：如果您在审查运行时推送到 PR，某些发现可能引用当前差异中不再存在的行。这些出现在审查正文文本中的 **Additional findings** 标题下，而不是作为内联评论。

## 相关资源

Code Review 旨在与 Claude Code 的其余部分一起工作。如果您想在打开 PR 之前在本地运行审查、需要自托管设置或想深入了解 `CLAUDE.md` 如何在工具中塑造 Claude 的行为，这些页面是很好的下一步：

* [Plugins](/zh-CN/discover-plugins)：浏览插件市场，包括用于在推送前本地运行按需审查的 `code-review` 插件
* [GitHub Actions](/zh-CN/github-actions)：在您自己的 GitHub Actions 工作流中运行 Claude，以实现超越代码审查的自定义自动化
* [GitLab CI/CD](/zh-CN/gitlab-ci-cd)：GitLab 管道的自托管 Claude 集成
* [Memory](/zh-CN/memory)：`CLAUDE.md` 文件如何在 Claude Code 中工作
* [Analytics](/zh-CN/analytics)：跟踪超越代码审查的 Claude Code 使用情况
