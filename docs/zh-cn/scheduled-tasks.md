> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 按计划运行提示词

> 使用 /loop 和 cron 调度工具在 Claude Code 会话中重复运行提示词、轮询状态或设置一次性提醒。

<Note>
  计划任务需要 Claude Code v2.1.72 或更高版本。使用 `claude --version` 检查您的版本。
</Note>

计划任务让 Claude 按间隔自动重新运行提示词。使用它们来轮询部署、监督 PR、检查长时间运行的构建，或在会话中稍后提醒自己做某事。要对事件进行实时反应而不是轮询，请参阅 [Channels](/zh-CN/channels)：您的 CI 可以直接将失败推送到会话中。

任务是会话范围的：它们存在于当前 Claude Code 进程中，当您退出时就会消失。对于需要在重启后继续运行的持久调度，请使用 [Routines](/zh-CN/routines)、[Desktop 计划任务](/zh-CN/desktop-scheduled-tasks) 或 [GitHub Actions](/zh-CN/github-actions)。

## 比较调度选项

Claude Code offers three ways to schedule recurring work:

|                            | [Cloud](/en/routines)          | [Desktop](/en/desktop-scheduled-tasks) | [`/loop`](/en/scheduled-tasks)      |
| :------------------------- | :----------------------------- | :------------------------------------- | :---------------------------------- |
| Runs on                    | Anthropic cloud                | Your machine                           | Your machine                        |
| Requires machine on        | No                             | Yes                                    | Yes                                 |
| Requires open session      | No                             | No                                     | Yes                                 |
| Persistent across restarts | Yes                            | Yes                                    | Restored on `--resume` if unexpired |
| Access to local files      | No (fresh clone)               | Yes                                    | Yes                                 |
| MCP servers                | Connectors configured per task | [Config files](/en/mcp) and connectors | Inherits from session               |
| Permission prompts         | No (runs autonomously)         | Configurable per task                  | Inherits from session               |
| Customizable schedule      | Via `/schedule` in the CLI     | Yes                                    | Yes                                 |
| Minimum interval           | 1 hour                         | 1 minute                               | 1 minute                            |

<Tip>
  Use **cloud tasks** for work that should run reliably without your machine. Use **Desktop tasks** when you need access to local files and tools. Use **`/loop`** for quick polling during a session.
</Tip>

## 使用 /loop 重复运行提示词

`/loop` [bundled skill](/zh-CN/commands) 是在会话保持打开时重复运行提示词的最快方式。间隔和提示词都是可选的，您提供的内容决定了循环的行为方式。

| 您提供的内容 | 示例                          | 发生的情况                                                                 |
| :----- | :-------------------------- | :-------------------------------------------------------------------- |
| 间隔和提示词 | `/loop 5m check the deploy` | 您的提示词在[固定计划](#run-on-a-fixed-interval)上运行                             |
| 仅提示词   | `/loop check the deploy`    | 您的提示词在 Claude 选择的[间隔](#let-claude-choose-the-interval)上运行，每次迭代        |
| 仅间隔或无  | `/loop`                     | [内置维护提示词](#run-the-built-in-maintenance-prompt)运行，或您的 `loop.md`（如果存在） |

您也可以将另一个命令作为提示词传递，例如 `/loop 20m /review-pr 1234`，以在每次迭代时重新运行打包的工作流。

### 在固定间隔上运行

当您提供间隔时，Claude 将其转换为 cron 表达式，计划作业，并确认频率和作业 ID。

```text theme={null}
/loop 5m check if the deployment finished and tell me what happened
```

间隔可以作为裸令牌（如 `30m`）在提示词前面，或作为子句（如 `every 2 hours`）在后面。支持的单位是 `s` 表示秒、`m` 表示分钟、`h` 表示小时、`d` 表示天。

秒数向上舍入到最近的分钟，因为 cron 的粒度为一分钟。不能均匀映射到干净 cron 步长的间隔，例如 `7m` 或 `90m`，会舍入到最近的间隔，Claude 会告诉您它选择了什么。

### 让 Claude 选择间隔

当您省略间隔时，Claude 会动态选择一个，而不是在固定 cron 计划上运行。在每次迭代后，它会根据观察到的情况选择一个一分钟到一小时之间的延迟：在构建完成或 PR 活跃时等待较短时间，当没有待处理项时等待较长时间。选择的延迟和原因会在每次迭代结束时打印。

下面的示例检查 CI 和审查评论，Claude 在 PR 变得安静后在迭代之间等待更长时间：

```text theme={null}
/loop check whether CI passed and address any review comments
```

当您要求动态 `/loop` 计划时，Claude 可能会直接使用 [Monitor tool](/zh-CN/tools-reference#monitor-tool)。Monitor 运行后台脚本并流式传输每个输出行，这完全避免了轮询，通常比在间隔上重新运行提示词更节省令牌且响应更快。

动态计划的循环出现在您的[计划任务列表](#manage-scheduled-tasks)中，就像任何其他任务一样，所以您可以以相同的方式列出或取消它。[抖动规则](#jitter)不适用于它，但[七天过期](#seven-day-expiry)适用：循环在您启动它七天后自动结束。

<Note>
  在 Bedrock、Vertex AI 和 Microsoft Foundry 上，没有间隔的提示词在固定的 10 分钟计划上运行。
</Note>

### 运行内置维护提示词

当您省略提示词时，Claude 使用内置维护提示词而不是您提供的提示词。在每次迭代中，它按顺序处理以下内容：

* 继续对话中的任何未完成工作
* 照顾当前分支的拉取请求：审查评论、失败的 CI 运行、合并冲突
* 运行清理通过，例如当没有其他待处理项时的错误搜索或简化

Claude 不会启动该范围之外的新举措，不可逆的操作（如推送或删除）仅在继续转录已授权的内容时进行。

```text theme={null}
/loop
```

裸 `/loop` 在[动态选择的间隔](#let-claude-choose-the-interval)上运行此提示词。添加间隔，例如 `/loop 15m`，以在固定计划上运行它。要用您自己的默认值替换内置提示词，请参阅[使用 loop.md 自定义默认提示词](#customize-the-default-prompt-with-loop-md)。

<Note>
  在 Bedrock、Vertex AI 和 Microsoft Foundry 上，没有提示词的 `/loop` 打印使用消息而不是启动维护循环。
</Note>

### 使用 loop.md 自定义默认提示词

`loop.md` 文件用您自己的说明替换内置维护提示词。它为裸 `/loop` 定义单个默认提示词，而不是单独计划任务的列表，并且在您在命令行上提供提示词时被忽略。要在其旁边计划其他提示词，请使用 `/loop <prompt>` 或[直接询问 Claude](#manage-scheduled-tasks)。

Claude 在两个位置查找文件，并使用它找到的第一个。

| 路径                  | 范围                  |
| :------------------ | :------------------ |
| `.claude/loop.md`   | 项目级别。当两个文件都存在时优先。   |
| `~/.claude/loop.md` | 用户级别。适用于任何未定义自己的项目。 |

该文件是纯 Markdown，没有必需的结构。像您直接输入 `/loop` 提示词一样编写它。以下示例保持发布分支健康：

```markdown title=".claude/loop.md" theme={null}
Check the `release/next` PR. If CI is red, pull the failing job log,
diagnose, and push a minimal fix. If new review comments have arrived,
address each one and resolve the thread. If everything is green and
quiet, say so in one line.
```

对 `loop.md` 的编辑在下一次迭代时生效，所以您可以在循环运行时优化说明。当任一位置都不存在 `loop.md` 时，循环回退到内置维护提示词。保持文件简洁：超过 25,000 字节的内容会被截断。

## 设置一次性提醒

对于一次性提醒，用自然语言描述您想要的内容，而不是使用 `/loop`。Claude 计划一个单次触发的任务，该任务在运行后删除自己。

```text theme={null}
remind me at 3pm to push the release branch
```

```text theme={null}
in 45 minutes, check whether the integration tests passed
```

Claude 使用 cron 表达式将触发时间固定到特定的分钟和小时，并确认何时触发。

## 管理计划任务

用自然语言要求 Claude 列出或取消任务，或直接引用底层工具。

```text theme={null}
what scheduled tasks do I have?
```

```text theme={null}
cancel the deploy check job
```

在幕后，Claude 使用这些工具：

| 工具           | 目的                                          |
| :----------- | :------------------------------------------ |
| `CronCreate` | 计划新任务。接受 5 字段 cron 表达式、要运行的提示词以及是否重复或仅触发一次。 |
| `CronList`   | 列出所有计划任务及其 ID、计划和提示词。                       |
| `CronDelete` | 按 ID 取消任务。                                  |

每个计划任务都有一个 8 字符的 ID，您可以将其传递给 `CronDelete`。一个会话最多可以同时保存 50 个计划任务。

## 计划任务如何运行

调度程序每秒检查一次到期的任务，并以低优先级将其加入队列。计划的提示词在您的回合之间触发，而不是在 Claude 正在响应时。如果 Claude 在任务到期时忙碌，提示词会等到当前回合结束。

所有时间都在您的本地时区中解释。像 `0 9 * * *` 这样的 cron 表达式意味着 9am 在您运行 Claude Code 的任何地方，而不是 UTC。

### 抖动

为了避免每个会话在同一个挂钟时刻击中 API，调度程序会向触发时间添加一个小的确定性偏移：

* 重复任务最多晚触发其周期的 10%，上限为 15 分钟。每小时的作业可能在 `:00` 到 `:06` 之间的任何时间触发。
* 为小时顶部或底部计划的一次性任务最多提前 90 秒触发。

偏移是从任务 ID 派生的，所以相同的任务总是获得相同的偏移。如果精确的时间很重要，选择不是 `:00` 或 `:30` 的分钟，例如 `3 9 * * *` 而不是 `0 9 * * *`，一次性抖动将不适用。

### 七天过期

重复任务在创建后 7 天自动过期。任务最后触发一次，然后删除自己。这限制了被遗忘的循环可以运行多长时间。如果您需要重复任务持续更长时间，请在过期前取消并重新创建它，或使用 [Routines](/zh-CN/routines) 或 [Desktop 计划任务](/zh-CN/desktop-scheduled-tasks) 进行持久调度。

## Cron 表达式参考

`CronCreate` 接受标准 5 字段 cron 表达式：`minute hour day-of-month month day-of-week`。所有字段都支持通配符 (`*`)、单个值 (`5`)、步长 (`*/15`)、范围 (`1-5`) 和逗号分隔的列表 (`1,15,30`)。

| 示例             | 含义                  |
| :------------- | :------------------ |
| `*/5 * * * *`  | 每 5 分钟              |
| `0 * * * *`    | 每小时整点               |
| `7 * * * *`    | 每小时的第 7 分钟          |
| `0 9 * * *`    | 每天本地时间 9am          |
| `0 9 * * 1-5`  | 工作日本地时间 9am         |
| `30 14 15 3 *` | 3 月 15 日本地时间下午 2:30 |

星期几使用 `0` 或 `7` 表示星期日，`6` 表示星期六。不支持扩展语法如 `L`、`W`、`?` 和名称别名如 `MON` 或 `JAN`。

当月份日期和星期几都受到限制时，如果任一字段匹配，日期就匹配。这遵循标准的 vixie-cron 语义。

## 禁用计划任务

在您的环境中设置 `CLAUDE_CODE_DISABLE_CRON=1` 以完全禁用调度程序。cron 工具和 `/loop` 变得不可用，任何已计划的任务都停止触发。有关禁用标志的完整列表，请参阅[环境变量](/zh-CN/env-vars)。

## 限制

会话范围的调度有固有的限制：

* 任务仅在 Claude Code 运行且空闲时触发。关闭终端或让会话退出会取消所有内容。
* 没有错过触发的追赶。如果任务的计划时间在 Claude 忙于长时间运行的请求时经过，它会在 Claude 变为空闲时触发一次，而不是每个错过的间隔触发一次。
* 没有跨重启的持久性。重启 Claude Code 会清除所有会话范围的任务。

对于需要无人值守运行的 cron 驱动自动化：

* [Routines](/zh-CN/routines)：在 Anthropic 管理的基础设施上按计划运行、通过 API 调用或在 GitHub 事件上运行
* [GitHub Actions](/zh-CN/github-actions)：在 CI 中使用 `schedule` 触发器
* [Desktop 计划任务](/zh-CN/desktop-scheduled-tasks)：在您的机器上本地运行
