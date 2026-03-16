> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 代码审查

> 设置自动化 PR 审查，使用多代理分析您的完整代码库来捕获逻辑错误、安全漏洞和回归问题

<Note>
  Code Review 处于研究预览阶段，可用于 [Teams 和 Enterprise](https://claude.ai/admin-settings/claude-code) 订阅。对于启用了 [Zero Data Retention](/zh-CN/zero-data-retention) 的组织，不可用。
</Note>

Code Review 分析您的 GitHub pull request，并在发现问题的代码行上发布内联注释。一队专门的代理在您完整代码库的上下文中检查代码更改，寻找逻辑错误、安全漏洞、破损的边界情况和微妙的回归问题。

发现结果按严重程度标记，不会批准或阻止您的 PR，因此现有的审查工作流保持不变。您可以通过向存储库添加 `CLAUDE.md` 或 `REVIEW.md` 文件来调整 Claude 标记的内容。

要在您自己的 CI 基础设施中运行 Claude 而不是使用此托管服务，请参阅 [GitHub Actions](/zh-CN/github-actions) 或 [GitLab CI/CD](/zh-CN/gitlab-ci-cd)。

本页涵盖：

* [审查工作原理](#how-reviews-work)
* [设置](#set-up-code-review)
* [自定义审查](#customize-reviews)，使用 `CLAUDE.md` 和 `REVIEW.md`
* [定价](#pricing)

## 审查工作原理

一旦管理员为您的组织 [启用 Code Review](#set-up-code-review)，当 pull request 打开或更新时，审查会自动运行。多个代理在 Anthropic 基础设施上并行分析差异和周围代码。每个代理寻找不同类别的问题，然后验证步骤根据实际代码行为检查候选项以过滤掉误报。结果被去重、按严重程度排序，并作为内联注释发布在发现问题的特定行上。如果未发现问题，Claude 会在 PR 上发布简短的确认注释。

审查成本随 PR 大小和复杂性而扩展，平均在 20 分钟内完成。管理员可以通过 [分析仪表板](#view-usage) 监控审查活动和支出。

### 严重程度级别

每个发现都标记有严重程度级别：

| 标记 | 严重程度 | 含义                   |
| :- | :--- | :------------------- |
| 🔴 | 正常   | 应在合并前修复的错误           |
| 🟡 | 小问题  | 轻微问题，值得修复但不阻止        |
| 🟣 | 预先存在 | 代码库中存在但不是由此 PR 引入的错误 |

发现包括可折叠的扩展推理部分，您可以展开以了解 Claude 为什么标记该问题以及它如何验证问题。

### Code Review 检查的内容

默认情况下，Code Review 专注于正确性：会破坏生产的错误，而不是格式偏好或缺失的测试覆盖。您可以通过 [添加指导文件](#customize-reviews) 到您的存储库来扩展它检查的内容。

## 设置 Code Review

管理员为组织启用一次 Code Review，并选择要包含的存储库。

<Steps>
  <Step title="打开 Claude Code 管理员设置">
    转到 [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) 并找到 Code Review 部分。您需要对 Claude 组织的管理员访问权限和在 GitHub 组织中安装 GitHub Apps 的权限。
  </Step>

  <Step title="开始设置">
    点击 **Setup**。这开始 GitHub App 安装流程。
  </Step>

  <Step title="安装 Claude GitHub App">
    按照提示将 Claude GitHub App 安装到您的 GitHub 组织。该应用请求这些存储库权限：

    * **Contents**：读和写
    * **Issues**：读和写
    * **Pull requests**：读和写

    Code Review 使用对内容的读访问权限和对 pull request 的写访问权限。更广泛的权限集也支持 [GitHub Actions](/zh-CN/github-actions)，如果您稍后启用它。
  </Step>

  <Step title="选择存储库">
    选择要为 Code Review 启用的存储库。如果您看不到存储库，请确保在安装期间给了 Claude GitHub App 访问权限。您可以稍后添加更多存储库。
  </Step>

  <Step title="为每个存储库设置审查触发器">
    设置完成后，Code Review 部分在表格中显示您的存储库。对于每个存储库，使用下拉菜单选择审查何时运行：

    * **仅在 PR 创建后**：当 PR 打开或标记为准备审查时审查运行一次
    * **在每次推送到 PR 分支后**：在每次推送时运行审查，在 PR 演变时捕获新问题，并在您修复标记的问题时自动解决线程

    在每次推送时审查会运行更多审查并花费更多。从仅 PR 创建开始，对于您想要持续覆盖和自动线程清理的存储库切换到推送时。
  </Step>
</Steps>

存储库表还显示每个存储库基于最近活动的平均审查成本。使用行操作菜单为每个存储库打开或关闭 Code Review，或完全删除存储库。

要验证设置，请打开测试 PR。在几分钟内会出现名为 **Claude Code Review** 的检查运行。如果没有，请确认存储库在您的管理员设置中列出，并且 Claude GitHub App 有权访问它。

## 自定义审查

Code Review 从您的存储库读取两个文件来指导它标记的内容。两者都是在默认正确性检查之上的附加：

* **`CLAUDE.md`**：共享项目说明，Claude Code 用于所有任务，不仅仅是审查。当指导也适用于交互式 Claude Code 会话时使用它。
* **`REVIEW.md`**：仅审查指导，在代码审查期间专门读取。对于严格关于在审查期间标记或跳过什么的规则，以及会使您的常规 `CLAUDE.md` 混乱的规则，使用它。

### CLAUDE.md

Code Review 读取您的存储库的 `CLAUDE.md` 文件，并将新引入的违规视为小问题级别的发现。这是双向工作的：如果您的 PR 以使 `CLAUDE.md` 语句过时的方式更改代码，Claude 会标记文档需要更新。

Claude 在目录层次结构的每个级别读取 `CLAUDE.md` 文件，因此子目录的 `CLAUDE.md` 中的规则仅适用于该路径下的文件。有关 `CLAUDE.md` 如何工作的更多信息，请参阅 [内存文档](/zh-CN/memory)。

对于您不想应用于常规 Claude Code 会话的仅审查指导，请改用 [`REVIEW.md`](#review-md)。

### REVIEW\.md

将 `REVIEW.md` 文件添加到您的存储库根目录以获取仅审查规则。使用它来编码：

* 公司或团队风格指南："优先使用早期返回而不是嵌套条件"
* 语言或框架特定的约定，不被 linter 覆盖
* Claude 应始终标记的内容："任何新 API 路由必须有集成测试"
* Claude 应跳过的内容："不要对 `/gen/` 下生成的代码中的格式进行注释"

示例 `REVIEW.md`：

```markdown  theme={null}
# 代码审查指南

## 始终检查
- 新 API 端点有相应的集成测试
- 数据库迁移向后兼容
- 错误消息不会向用户泄露内部详情

## 风格
- 优先使用 `match` 语句而不是链式 `isinstance` 检查
- 使用结构化日志，而不是日志调用中的 f 字符串插值

## 跳过
- `src/gen/` 下的生成文件
- `*.lock` 文件中仅格式的更改
```

Claude 自动发现存储库根目录中的 `REVIEW.md`。无需配置。

## 查看使用情况

转到 [claude.ai/analytics/code-review](https://claude.ai/analytics/code-review) 以查看整个组织的 Code Review 活动。仪表板显示：

| 部分     | 显示内容                          |
| :----- | :---------------------------- |
| 审查的 PR | 所选时间范围内审查的 pull request 的每日计数 |
| 每周成本   | Code Review 的每周支出             |
| 反馈     | 因开发人员解决问题而自动解决的审查注释计数         |
| 存储库分解  | 每个存储库审查的 PR 计数和解决的注释          |

管理员设置中的存储库表也显示每个存储库的平均审查成本。

## 定价

Code Review 根据令牌使用情况计费。审查平均 \$15-25，随 PR 大小、代码库复杂性和需要验证的问题数量而扩展。Code Review 使用通过 [额外使用](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) 单独计费，不计入您的计划包含的使用。

您选择的审查触发器影响总成本：

* **仅在 PR 创建后**：每个 PR 运行一次
* **在每次推送时**：在每次提交时运行，将成本乘以推送次数

无论您的组织是否为其他 Claude Code 功能使用 AWS Bedrock 或 Google Vertex AI，成本都会出现在您的 Anthropic 账单上。要为 Code Review 设置每月支出上限，请转到 [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) 并为 Claude Code Review 服务配置限制。

通过 [分析](#view-usage) 中的每周成本图表或管理员设置中的每个存储库平均成本列监控支出。

## 相关资源

Code Review 设计用于与 Claude Code 的其余部分一起工作。如果您想在打开 PR 之前在本地运行审查、需要自托管设置或想更深入地了解 `CLAUDE.md` 如何在工具中塑造 Claude 的行为，这些页面是很好的下一步：

* [Plugins](/zh-CN/discover-plugins)：浏览插件市场，包括用于在推送前本地运行按需审查的 `code-review` 插件
* [GitHub Actions](/zh-CN/github-actions)：在您自己的 GitHub Actions 工作流中运行 Claude，用于超越代码审查的自定义自动化
* [GitLab CI/CD](/zh-CN/gitlab-ci-cd)：GitLab 管道的自托管 Claude 集成
* [Memory](/zh-CN/memory)：`CLAUDE.md` 文件如何在 Claude Code 中工作
* [Analytics](/zh-CN/analytics)：跟踪超越代码审查的 Claude Code 使用情况
