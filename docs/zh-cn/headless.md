> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 以编程方式运行 Claude Code

> 使用 Agent SDK 从 CLI、Python 或 TypeScript 以编程方式运行 Claude Code。

[Agent SDK](/zh-CN/agent-sdk/overview) 为您提供了与 Claude Code 相同的工具、agent 循环和上下文管理。它可作为 CLI 用于脚本和 CI/CD，或作为 [Python](/zh-CN/agent-sdk/python) 和 [TypeScript](/zh-CN/agent-sdk/typescript) 包供完整的编程控制。

<Note>
  CLI 之前被称为"headless mode"。`-p` 标志和所有 CLI 选项的工作方式相同。
</Note>

要从 CLI 以编程方式运行 Claude Code，请使用 `-p` 传递您的提示和任何 [CLI 选项](/zh-CN/cli-reference)：

```bash theme={null}
claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"
```

本页面涵盖通过 CLI (`claude -p`) 使用 Agent SDK。对于具有结构化输出、工具批准回调和原生消息对象的 Python 和 TypeScript SDK 包，请参阅 [完整 Agent SDK 文档](/zh-CN/agent-sdk/overview)。

## 基本用法

将 `-p`（或 `--print`）标志添加到任何 `claude` 命令以非交互方式运行它。所有 [CLI 选项](/zh-CN/cli-reference) 都适用于 `-p`，包括：

* `--continue` 用于 [继续对话](#continue-conversations)
* `--allowedTools` 用于 [自动批准工具](#auto-approve-tools)
* `--output-format` 用于 [获取结构化输出](#get-structured-output)

此示例询问 Claude 关于您的代码库的问题并打印响应：

```bash theme={null}
claude -p "What does the auth module do?"
```

### 使用裸模式更快启动

添加 `--bare` 以通过跳过 hooks、skills、plugins、MCP 服务器、自动内存和 CLAUDE.md 的自动发现来减少启动时间。没有它，`claude -p` 会加载交互式会话相同的 [上下文](/zh-CN/how-claude-code-works#the-context-window)，包括在工作目录或 `~/.claude` 中配置的任何内容。

裸模式对于 CI 和脚本很有用，您需要在每台机器上获得相同的结果。队友的 `~/.claude` 中的 hook 或项目的 `.mcp.json` 中的 MCP 服务器不会运行，因为裸模式从不读取它们。只有您显式传递的标志才会生效。

此示例在裸模式下运行一次性摘要任务，并预先批准 Read 工具，以便调用完成而无需权限提示：

```bash theme={null}
claude --bare -p "Summarize this file" --allowedTools "Read"
```

在裸模式下，Claude 可以访问 Bash、文件读取和文件编辑工具。使用标志传递您需要的任何上下文：

| 要加载        | 使用                                                      |
| ---------- | ------------------------------------------------------- |
| 系统提示添加     | `--append-system-prompt`, `--append-system-prompt-file` |
| 设置         | `--settings <file-or-json>`                             |
| MCP 服务器    | `--mcp-config <file-or-json>`                           |
| 自定义 agents | `--agents <json>`                                       |
| 插件         | `--plugin-dir <path>`, `--plugin-url <url>`             |

裸模式跳过 OAuth 和钥匙链读取。Anthropic 身份验证必须来自 `ANTHROPIC_API_KEY` 或传递给 `--settings` 的 JSON 中的 `apiKeyHelper`。Bedrock、Vertex 和 Foundry 使用其常规提供商凭证。

<Note>
  `--bare` 是脚本和 SDK 调用的推荐模式，将在未来版本中成为 `-p` 的默认值。
</Note>

## 示例

这些示例突出了常见的 CLI 模式。对于 CI 和其他脚本调用，添加 [`--bare`](#start-faster-with-bare-mode) 以便它们不会选择本地配置的任何内容。

### 通过 Claude 管道传输数据

非交互模式读取 stdin，因此您可以像任何其他命令行工具一样管道传输数据并重定向响应。

此示例将构建日志管道传输到 Claude 并将说明写入文件：

```bash theme={null}
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

使用 `--output-format json`，响应有效负载包括 `total_cost_usd` 和按模型的成本分解，因此脚本调用者可以跟踪每次调用的支出，而无需查询 [使用情况仪表板](/zh-CN/costs)。

<Note>
  从 Claude Code v2.1.128 开始，管道 stdin 的上限为 10MB。如果超过上限，Claude Code 会以清晰的错误和非零状态退出。要处理更大的输入，请将内容写入文件并在提示中引用文件路径，而不是管道传输它。
</Note>

### 将 Claude 添加到构建脚本

您可以在脚本中包装非交互调用，以将 Claude 用作项目特定的 linter 或审查者。

此 `package.json` 脚本将针对 `main` 的 diff 管道传输到 Claude，并要求它报告拼写错误。管道传输 diff 意味着 Claude 不需要 Bash 权限来读取它，转义的双引号使脚本可移植到 Windows：

```json theme={null}
{
  "scripts": {
    "lint:claude": "git diff main | claude -p \"you are a typo linter. for each typo in this diff, report filename:line on one line and the issue on the next. return nothing else.\""
  }
}
```

### 获取结构化输出

使用 `--output-format` 控制响应的返回方式：

* `text`（默认）：纯文本输出
* `json`：包含结果、会话 ID 和元数据的结构化 JSON
* `stream-json`：用于实时流式传输的换行符分隔的 JSON

此示例以 JSON 格式返回项目摘要以及会话元数据，文本结果在 `result` 字段中：

```bash theme={null}
claude -p "Summarize this project" --output-format json
```

要获得符合特定架构的输出，请使用 `--output-format json` 与 `--json-schema` 和 [JSON Schema](https://json-schema.org/) 定义。响应包括关于请求的元数据（会话 ID、使用情况等），结构化输出在 `structured_output` 字段中。

此示例从 auth.py 中提取函数名称并将其作为字符串数组返回：

```bash theme={null}
claude -p "Extract the main function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

<Tip>
  使用 [jq](https://jqlang.github.io/jq/) 之类的工具来解析响应并提取特定字段：

  ```bash theme={null}
  # Extract the text result
  claude -p "Summarize this project" --output-format json | jq -r '.result'

  # Extract structured output
  claude -p "Extract function names from auth.py" \
    --output-format json \
    --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
    | jq '.structured_output'
  ```
</Tip>

### 流式传输响应

使用 `--output-format stream-json` 与 `--verbose` 和 `--include-partial-messages` 来接收生成的令牌。每一行都是代表一个事件的 JSON 对象：

```bash theme={null}
claude -p "Explain recursion" --output-format stream-json --verbose --include-partial-messages
```

以下示例使用 [jq](https://jqlang.github.io/jq/) 来过滤文本增量并仅显示流式文本。`-r` 标志输出原始字符串（无引号），`-j` 不带换行符连接，以便令牌连续流式传输：

```bash theme={null}
claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

当 API 请求因可重试错误而失败时，Claude Code 在重试前发出 `system/api_retry` 事件。您可以使用此来显示重试进度或实现自定义退避逻辑。

| 字段               | 类型            | 描述                                                                                                                                                 |
| ---------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`           | `"system"`    | 消息类型                                                                                                                                               |
| `subtype`        | `"api_retry"` | 将其标识为重试事件                                                                                                                                          |
| `attempt`        | 整数            | 当前尝试次数，从 1 开始                                                                                                                                      |
| `max_retries`    | 整数            | 允许的总重试次数                                                                                                                                           |
| `retry_delay_ms` | 整数            | 毫秒直到下一次尝试                                                                                                                                          |
| `error_status`   | 整数或 null      | HTTP 状态代码，或 `null` 表示没有 HTTP 响应的连接错误                                                                                                               |
| `error`          | 字符串           | 错误类别：`authentication_failed`、`oauth_org_not_allowed`、`billing_error`、`rate_limit`、`invalid_request`、`server_error`、`max_output_tokens` 或 `unknown` |
| `uuid`           | 字符串           | 唯一事件标识符                                                                                                                                            |
| `session_id`     | 字符串           | 事件所属的会话                                                                                                                                            |

`system/init` 事件报告会话元数据，包括模型、工具、MCP 服务器和加载的插件。它是流中的第一个事件，除非设置了 [`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`](/zh-CN/env-vars)，在这种情况下 `plugin_install` 事件在其之前。使用插件字段在插件未加载时使 CI 失败：

| 字段              | 类型 | 描述                                                                                                                          |
| --------------- | -- | --------------------------------------------------------------------------------------------------------------------------- |
| `plugins`       | 数组 | 成功加载的插件，每个都有 `name` 和 `path`                                                                                                |
| `plugin_errors` | 数组 | 插件加载时错误，每个都有 `plugin`、`type` 和 `message`。包括不满足的依赖版本和 `--plugin-dir` 加载失败，例如缺失路径或无效存档。受影响的插件被降级并从 `plugins` 中缺失。当没有错误时，该键被省略 |

当设置了 [`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`](/zh-CN/env-vars) 时，Claude Code 在第一轮之前安装市场插件时发出 `system/plugin_install` 事件。使用这些在您自己的 UI 中显示安装进度。

| 字段           | 类型                                                   | 描述                                                           |
| ------------ | ---------------------------------------------------- | ------------------------------------------------------------ |
| `type`       | `"system"`                                           | 消息类型                                                         |
| `subtype`    | `"plugin_install"`                                   | 将其标识为插件安装事件                                                  |
| `status`     | `"started"`、`"installed"`、`"failed"` 或 `"completed"` | `started` 和 `completed` 括住整体安装；`installed` 和 `failed` 报告单个市场 |
| `name`       | 字符串，可选                                               | 市场名称，在 `installed` 和 `failed` 上存在                            |
| `error`      | 字符串，可选                                               | 失败消息，在 `failed` 上存在                                          |
| `uuid`       | 字符串                                                  | 唯一事件标识符                                                      |
| `session_id` | 字符串                                                  | 事件所属的会话                                                      |

对于具有回调和消息对象的编程流式传输，请参阅 Agent SDK 文档中的 [实时流式传输响应](/zh-CN/agent-sdk/streaming-output)。

### 自动批准工具

使用 `--allowedTools` 让 Claude 使用某些工具而无需提示。此示例运行测试套件并修复失败，允许 Claude 执行 Bash 命令和读取/编辑文件而无需请求权限：

```bash theme={null}
claude -p "Run the test suite and fix any failures" \
  --allowedTools "Bash,Read,Edit"
```

要为整个会话设置基线而不是列出单个工具，请传递 [权限模式](/zh-CN/permission-modes)。`dontAsk` 拒绝您的 `permissions.allow` 规则或 [只读命令集](/zh-CN/permissions#read-only-commands) 中未包含的任何内容，这对于锁定的 CI 运行很有用。`acceptEdits` 让 Claude 写入文件而无需提示，还自动批准常见的文件系统命令，例如 `mkdir`、`touch`、`mv` 和 `cp`。其他 shell 命令和网络请求仍然需要 `--allowedTools` 条目或 `permissions.allow` 规则，否则当尝试时运行会中止：

```bash theme={null}
claude -p "Apply the lint fixes" --permission-mode acceptEdits
```

### 创建提交

此示例审查暂存的更改并创建具有适当消息的提交：

```bash theme={null}
claude -p "Look at my staged changes and create an appropriate commit" \
  --allowedTools "Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git commit *)"
```

`--allowedTools` 标志使用 [权限规则语法](/zh-CN/settings#permission-rule-syntax)。尾部的 ` *` 启用前缀匹配，因此 `Bash(git diff *)` 允许任何以 `git diff` 开头的命令。空格在 `*` 之前很重要：没有它，`Bash(git diff*)` 也会匹配 `git diff-index`。

<Note>
  用户调用的 [skills](/zh-CN/skills) 如 `/commit` 和 [内置命令](/zh-CN/commands) 仅在交互模式下可用。在 `-p` 模式下，改为描述您想要完成的任务。
</Note>

### 自定义系统提示

使用 `--append-system-prompt` 添加指令同时保持 Claude Code 的默认行为。此示例将 PR diff 传递给 Claude 并指示它审查安全漏洞：

```bash theme={null}
gh pr diff "$1" | claude -p \
  --append-system-prompt "You are a security engineer. Review for vulnerabilities." \
  --output-format json
```

有关更多选项（包括 `--system-prompt` 以完全替换默认提示），请参阅 [系统提示标志](/zh-CN/cli-reference#system-prompt-flags)。

### 继续对话

使用 `--continue` 继续最近的对话，或使用 `--resume` 与会话 ID 继续特定对话。此示例运行审查，然后发送后续提示：

```bash theme={null}
# First request
claude -p "Review this codebase for performance issues"

# Continue the most recent conversation
claude -p "Now focus on the database queries" --continue
claude -p "Generate a summary of all issues found" --continue
```

如果您运行多个对话，请捕获会话 ID 以恢复特定对话：

```bash theme={null}
session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')
claude -p "Continue that review" --resume "$session_id"
```

## 后续步骤

* [Agent SDK 快速入门](/zh-CN/agent-sdk/quickstart)：使用 Python 或 TypeScript 构建您的第一个 agent
* [CLI 参考](/zh-CN/cli-reference)：所有 CLI 标志和选项
* [GitHub Actions](/zh-CN/github-actions)：在 GitHub 工作流中使用 Agent SDK
* [GitLab CI/CD](/zh-CN/gitlab-ci-cd)：在 GitLab 管道中使用 Agent SDK
