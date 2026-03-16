> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 模型配置

> 了解 Claude Code 模型配置，包括模型别名如 `opusplan`

## 可用模型

对于 Claude Code 中的 `model` 设置，你可以配置以下任一项：

* 一个**模型别名**
* 一个**模型名称**
  * Anthropic API：完整的\*\*[模型名称](https://platform.claude.com/docs/zh-CN/about-claude/models/overview)\*\*
  * Bedrock：推理配置文件 ARN
  * Foundry：部署名称
  * Vertex：版本名称

### 模型别名

模型别名提供了一种便捷的方式来选择模型设置，无需记住确切的版本号：

| 模型别名             | 行为                                                                                                                                    |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **`default`**    | 推荐的模型设置，取决于你的账户类型                                                                                                                     |
| **`sonnet`**     | 使用最新的 Sonnet 模型（当前为 Sonnet 4.6）用于日常编码任务                                                                                               |
| **`opus`**       | 使用最新的 Opus 模型（当前为 Opus 4.6）用于复杂推理任务                                                                                                   |
| **`haiku`**      | 使用快速高效的 Haiku 模型用于简单任务                                                                                                                |
| **`sonnet[1m]`** | 使用 Sonnet 和[100 万 token 上下文窗口](https://platform.claude.com/docs/zh-CN/build-with-claude/context-windows#1m-token-context-window)用于长会话 |
| **`opusplan`**   | 特殊模式，在计划模式中使用 `opus`，然后在执行时切换到 `sonnet`                                                                                               |

别名始终指向最新版本。要固定到特定版本，请使用完整模型名称（例如 `claude-opus-4-6`）或设置相应的环境变量，如 `ANTHROPIC_DEFAULT_OPUS_MODEL`。

### 设置你的模型

你可以通过多种方式配置模型，按优先级顺序列出：

1. **在会话期间** - 使用 `/model <alias|name>` 在会话中切换模型
2. **启动时** - 使用 `claude --model <alias|name>` 启动
3. **环境变量** - 设置 `ANTHROPIC_MODEL=<alias|name>`
4. **设置** - 在设置文件中使用 `model` 字段永久配置。

使用示例：

```bash  theme={null}
# 使用 Opus 启动
claude --model opus

# 在会话期间切换到 Sonnet
/model sonnet
```

设置文件示例：

```json  theme={null}
{
    "permissions": {
        ...
    },
    "model": "opus"
}
```

## 限制模型选择

企业管理员可以在[托管或策略设置](/zh-CN/settings#settings-files)中使用 `availableModels` 来限制用户可以选择的模型。

设置 `availableModels` 后，用户无法通过 `/model`、`--model` 标志、Config 工具或 `ANTHROPIC_MODEL` 环境变量切换到列表中不存在的模型。

```json  theme={null}
{
  "availableModels": ["sonnet", "haiku"]
}
```

### 默认模型行为

模型选择器中的"默认"选项不受 `availableModels` 影响。它始终保持可用，并代表系统的运行时默认值[基于用户的订阅层级](#default-model-setting)。

即使使用 `availableModels: []`，用户仍然可以使用其层级的默认模型来使用 Claude Code。

### 控制用户运行的模型

要完全控制模型体验，请将 `availableModels` 与 `model` 设置一起使用：

* **availableModels**：限制用户可以切换到的内容
* **model**：设置显式模型覆盖，优先于默认值

此示例确保所有用户运行 Sonnet 4.6，并且只能在 Sonnet 和 Haiku 之间选择：

```json  theme={null}
{
  "model": "sonnet",
  "availableModels": ["sonnet", "haiku"]
}
```

### 合并行为

当 `availableModels` 在多个级别设置时，例如用户设置和项目设置，数组会被合并并去重。要强制执行严格的允许列表，请在托管或策略设置中设置 `availableModels`，这具有最高优先级。

## 特殊模型行为

### `default` 模型设置

`default` 的行为取决于你的账户类型：

* **Max 和 Team Premium**：默认为 Opus 4.6
* **Pro 和 Team Standard**：默认为 Sonnet 4.6
* **Enterprise**：Opus 4.6 可用但不是默认值

如果你在使用 Opus 时达到使用阈值，Claude Code 可能会自动回退到 Sonnet。

### `opusplan` 模型设置

`opusplan` 模型别名提供了一种自动化的混合方法：

* **在计划模式中** - 使用 `opus` 进行复杂推理和架构决策
* **在执行模式中** - 自动切换到 `sonnet` 进行代码生成和实现

这为你提供了两全其美的方案：Opus 的卓越推理能力用于规划，Sonnet 的效率用于执行。

### 调整努力级别

[努力级别](https://platform.claude.com/docs/zh-CN/build-with-claude/effort)控制自适应推理，根据任务复杂性动态分配思考。较低的努力级别对于直接任务更快更便宜，而较高的努力级别为复杂问题提供更深入的推理。

有三个级别可用：**low**、**medium** 和 **high**。Opus 4.6 对于 Max 和 Team 订阅者默认为中等努力级别。

**设置努力级别：**

* **在 `/model` 中**：选择模型时使用左右箭头键调整努力级别滑块
* **环境变量**：设置 `CLAUDE_CODE_EFFORT_LEVEL=low|medium|high`
* **设置**：在设置文件中设置 `effortLevel`

Opus 4.6 和 Sonnet 4.6 支持努力级别。当选择支持的模型时，努力级别滑块会出现在 `/model` 中。当前努力级别也会显示在徽标和旋转器旁边（例如"with low effort"），因此你可以确认哪个设置处于活动状态，而无需打开 `/model`。

要在 Opus 4.6 和 Sonnet 4.6 上禁用自适应推理并恢复到之前的固定思考预算，请设置 `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`。禁用时，这些模型使用由 `MAX_THINKING_TOKENS` 控制的固定预算。请参阅[环境变量](/zh-CN/settings#environment-variables)。

### 扩展上下文

Opus 4.6 和 Sonnet 4.6 支持[100 万 token 上下文窗口](https://platform.claude.com/docs/zh-CN/build-with-claude/context-windows#1m-token-context-window)用于包含大型代码库的长会话。

<Note>
  100 万 token 上下文窗口目前处于测试阶段。功能、定价和可用性可能会改变。
</Note>

扩展上下文可用于：

* **API 和按使用量付费用户**：完全访问 100 万 token 上下文
* **Pro、Max、Teams 和 Enterprise 订阅者**：可通过[额外使用](https://support.claude.com/zh-CN/articles/12429409-extra-usage-for-paid-claude-plans)获得

要完全禁用 100 万 token 上下文，请设置 `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`。这会从模型选择器中删除 100 万 token 模型变体。请参阅[环境变量](/zh-CN/settings#environment-variables)。

选择 100 万 token 模型不会立即改变计费。你的会话使用标准费率，直到超过 200K token 的上下文。超过 200K token 后，请求按[长上下文定价](https://platform.claude.com/docs/zh-CN/about-claude/pricing#long-context-pricing)收费，具有专用[速率限制](https://platform.claude.com/docs/zh-CN/api/rate-limits#long-context-rate-limits)。对于订阅者，超过 200K 的 token 作为额外使用而不是通过订阅计费。

如果你的账户支持 100 万 token 上下文，该选项会出现在最新版本 Claude Code 的模型选择器（`/model`）中。如果你看不到它，请尝试重新启动你的会话。

你也可以将 `[1m]` 后缀与模型别名或完整模型名称一起使用：

```bash  theme={null}
# 使用 sonnet[1m] 别名
/model sonnet[1m]

# 或将 [1m] 附加到完整模型名称
/model claude-sonnet-4-6[1m]
```

## 检查你的当前模型

你可以通过多种方式查看你当前使用的模型：

1. 在[状态行](/zh-CN/statusline)中（如果已配置）
2. 在 `/status` 中，它也显示你的账户信息。

## 环境变量

你可以使用以下环境变量，这些变量必须是完整的**模型名称**（或你的 API 提供商的等效项），以控制别名映射到的模型名称。

| 环境变量                             | 描述                                                            |
| -------------------------------- | ------------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`   | 用于 `opus` 的模型，或在 Plan Mode 活跃时用于 `opusplan` 的模型。              |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | 用于 `sonnet` 的模型，或在 Plan Mode 不活跃时用于 `opusplan` 的模型。           |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`  | 用于 `haiku` 的模型，或用于[后台功能](/zh-CN/costs#background-token-usage) |
| `CLAUDE_CODE_SUBAGENT_MODEL`     | 用于 [subagents](/zh-CN/sub-agents) 的模型                         |

注意：`ANTHROPIC_SMALL_FAST_MODEL` 已弃用，改为使用 `ANTHROPIC_DEFAULT_HAIKU_MODEL`。

### 为第三方部署固定模型

通过 [Bedrock](/zh-CN/amazon-bedrock)、[Vertex AI](/zh-CN/google-vertex-ai) 或 [Foundry](/zh-CN/microsoft-foundry) 部署 Claude Code 时，在向用户推出前固定模型版本。

不固定模型，Claude Code 会使用模型别名（`sonnet`、`opus`、`haiku`），这些别名会解析为最新版本。当 Anthropic 发布新模型时，其账户未启用新版本的用户将无声地中断。

<Warning>
  在初始设置中将所有三个模型环境变量设置为特定版本 ID。跳过此步骤意味着 Claude Code 更新可能会在你没有任何操作的情况下破坏你的用户。
</Warning>

对你的提供商使用以下环境变量和特定版本的模型 ID：

| 提供商       | 示例                                                                      |
| :-------- | :---------------------------------------------------------------------- |
| Bedrock   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'` |
| Vertex AI | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'`                 |
| Foundry   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'`                 |

对 `ANTHROPIC_DEFAULT_SONNET_MODEL` 和 `ANTHROPIC_DEFAULT_HAIKU_MODEL` 应用相同的模式。有关所有提供商的当前和旧版模型 ID，请参阅[模型概览](https://platform.claude.com/docs/zh-CN/about-claude/models/overview)。要将用户升级到新模型版本，请更新这些环境变量并重新部署。

<Note>
  使用第三方提供商时，`settings.availableModels` 允许列表仍然适用。过滤匹配模型别名（`opus`、`sonnet`、`haiku`），而不是提供商特定的模型 ID。
</Note>

### 按版本覆盖模型 ID

上面的家族级环境变量为每个家族别名配置一个模型 ID。如果你需要将同一家族中的多个版本映射到不同的提供商 ID，请改用 `modelOverrides` 设置。

`modelOverrides` 将单个 Anthropic 模型 ID 映射到 Claude Code 发送给你的提供商 API 的提供商特定字符串。当用户在 `/model` 选择器中选择映射的模型时，Claude Code 使用你配置的值而不是内置默认值。

这让企业管理员可以将每个模型版本路由到特定的 Bedrock 推理配置文件 ARN、Vertex AI 版本名称或 Foundry 部署名称，用于治理、成本分配或区域路由。

在你的[设置文件](/zh-CN/settings#settings-files)中设置 `modelOverrides`：

```json  theme={null}
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-sonnet-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/sonnet-prod"
  }
}
```

键必须是[模型概览](https://platform.claude.com/docs/zh-CN/about-claude/models/overview)中列出的 Anthropic 模型 ID。对于带日期的模型 ID，请包含日期后缀，完全按照其显示的方式。未知的键会被忽略。

覆盖替换了支持 `/model` 选择器中每个条目的内置模型 ID。在 Bedrock 上，覆盖优先于 Claude Code 在启动时自动发现的任何推理配置文件。你通过 `ANTHROPIC_MODEL`、`--model` 或 `ANTHROPIC_DEFAULT_*_MODEL` 环境变量直接提供的值会按原样传递给提供商，不会被 `modelOverrides` 转换。

`modelOverrides` 与 `availableModels` 一起工作。允许列表针对 Anthropic 模型 ID 进行评估，而不是覆盖值，因此 `availableModels` 中的条目如 `"opus"` 即使 Opus 版本映射到 ARN 也会继续匹配。

### Prompt caching 配置

Claude Code 自动使用 [prompt caching](https://platform.claude.com/docs/zh-CN/build-with-claude/prompt-caching) 来优化性能并降低成本。你可以全局禁用 prompt caching 或针对特定模型层级禁用：

| 环境变量                            | 描述                                        |
| ------------------------------- | ----------------------------------------- |
| `DISABLE_PROMPT_CACHING`        | 设置为 `1` 以禁用所有模型的 prompt caching（优先于按模型设置） |
| `DISABLE_PROMPT_CACHING_HAIKU`  | 设置为 `1` 以仅禁用 Haiku 模型的 prompt caching     |
| `DISABLE_PROMPT_CACHING_SONNET` | 设置为 `1` 以仅禁用 Sonnet 模型的 prompt caching    |
| `DISABLE_PROMPT_CACHING_OPUS`   | 设置为 `1` 以仅禁用 Opus 模型的 prompt caching      |

这些环境变量为你提供了对 prompt caching 行为的细粒度控制。全局 `DISABLE_PROMPT_CACHING` 设置优先于特定模型的设置，允许你在需要时快速禁用所有缓存。按模型的设置对于选择性控制很有用，例如在调试特定模型或与可能具有不同缓存实现的云提供商合作时。
