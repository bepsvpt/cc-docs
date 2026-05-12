> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 模型配置

> 了解 Claude Code 模型配置，包括模型别名如 `opusplan`

## 可用模型

对于 Claude Code 中的 `model` 设置，您可以配置以下任一项：

* 一个**模型别名**
* 一个**模型名称**
  * Anthropic API：完整的\*\*[模型名称](https://platform.claude.com/docs/zh-CN/about-claude/models/overview)\*\*
  * Bedrock：推理配置文件 ARN
  * Foundry：部署名称
  * Vertex：版本名称

<Note>
  `ANTHROPIC_BASE_URL` 改变请求发送的位置，而不是哪个模型回答它们。要通过 LLM 网关路由 Claude，请参阅 [LLM 网关配置](/zh-CN/llm-gateway)。
</Note>

### 模型别名

模型别名提供了一种便捷的方式来选择模型设置，无需记住确切的版本号：

| 模型别名             | 行为                                                                                                                               |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **`default`**    | 特殊值，清除任何模型覆盖并恢复到您的账户类型推荐的模型。本身不是模型别名                                                                                             |
| **`best`**       | 使用最强大的可用模型，当前等同于 `opus`                                                                                                          |
| **`sonnet`**     | 使用最新的 Sonnet 模型用于日常编码任务                                                                                                          |
| **`opus`**       | 使用最新的 Opus 模型用于复杂推理任务                                                                                                            |
| **`haiku`**      | 使用快速高效的 Haiku 模型用于简单任务                                                                                                           |
| **`sonnet[1m]`** | 使用 Sonnet 和[100 万令牌上下文窗口](https://platform.claude.com/docs/zh-CN/build-with-claude/context-windows#1m-token-context-window)用于长会话 |
| **`opus[1m]`**   | 使用 Opus 和[100 万令牌上下文窗口](https://platform.claude.com/docs/zh-CN/build-with-claude/context-windows#1m-token-context-window)用于长会话   |
| **`opusplan`**   | 特殊模式，在 Plan Mode 中使用 `opus`，然后在执行时切换到 `sonnet`                                                                                   |

在 Anthropic API 和 [Claude Platform on AWS](/zh-CN/claude-platform-on-aws) 上，`opus` 解析为 Opus 4.7，`sonnet` 解析为 Sonnet 4.6。在 Bedrock、Vertex 和 Foundry 上，`opus` 解析为 Opus 4.6，`sonnet` 解析为 Sonnet 4.5；通过显式选择完整模型名称或设置 `ANTHROPIC_DEFAULT_OPUS_MODEL` 或 `ANTHROPIC_DEFAULT_SONNET_MODEL` 可以在这些提供商上获得更新的模型。

别名指向您的提供商推荐的版本，并随时间更新。要固定到特定版本，请使用完整模型名称（例如 `claude-opus-4-7`）或设置相应的环境变量，如 `ANTHROPIC_DEFAULT_OPUS_MODEL`。

<Note>
  Opus 4.7 需要 Claude Code v2.1.111 或更高版本。运行 `claude update` 进行升级。
</Note>

### 设置您的模型

您可以通过多种方式配置模型，按优先级顺序列出：

1. **在会话期间** - 使用 `/model <alias|name>` 立即切换，或运行不带参数的 `/model` 打开选择器。当对话有先前的输出时，选择器会要求确认，因为下一个响应会重新读取完整历史记录而不使用缓存的上下文
2. **启动时** - 使用 `claude --model <alias|name>` 启动
3. **环境变量** - 设置 `ANTHROPIC_MODEL=<alias|name>`
4. **设置** - 在设置文件中使用 `model` 字段永久配置。

您的 `/model` 选择已保存到用户设置，并在重启后持续保留。从 v2.1.117 开始，如果项目的 `.claude/settings.json` 固定了不同的模型，Claude Code 也会将您的选择写入 `.claude/settings.local.json`，以便在重启后在该项目中继续应用。托管设置优先级最高，并在下次启动时重新应用。

当启动时的活跃模型来自项目或托管设置而不是您自己的选择时，启动标题会显示哪个设置文件设置了它。运行 `/model` 以覆盖当前会话。

使用示例：

```bash theme={null}
# 使用 Opus 启动
claude --model opus

# 在会话期间切换到 Sonnet
/model sonnet
```

设置文件示例：

```json theme={null}
{
    "permissions": {
        ...
    },
    "model": "opus"
}
```

## 限制模型选择

企业管理员可以在[托管或策略设置](/zh-CN/settings#settings-files)中使用 `availableModels` 来限制用户可以选择的模型。

设置 `availableModels` 后，用户无法通过 `/model`、`--model` 标志或 `ANTHROPIC_MODEL` 环境变量切换到列表中不包含的模型。

```json theme={null}
{
  "availableModels": ["sonnet", "haiku"]
}
```

### 默认模型行为

模型选择器中的"默认"选项不受 `availableModels` 影响。它始终保持可用，并代表系统的运行时默认值[基于用户的订阅层级](#default-model-setting)。

即使使用 `availableModels: []`，用户仍然可以使用其层级的默认模型来使用 Claude Code。

### 控制用户运行的模型

`model` 设置是初始选择，而不是强制执行。它设置会话启动时哪个模型处于活跃状态，但用户仍然可以打开 `/model` 并选择"默认"，这会解析为其层级的系统默认值，无论 `model` 设置为什么。

要完全控制模型体验，请结合三个设置：

* **`availableModels`**：限制用户可以切换到的命名模型
* **`model`**：设置会话启动时的初始模型选择
* **`ANTHROPIC_DEFAULT_SONNET_MODEL`** / **`ANTHROPIC_DEFAULT_OPUS_MODEL`** / **`ANTHROPIC_DEFAULT_HAIKU_MODEL`**：控制"默认"选项和 `sonnet`、`opus` 和 `haiku` 别名解析为什么

此示例在 Sonnet 4.5 上启动用户，将选择器限制为 Sonnet 和 Haiku，并将"默认"固定为解析为 Sonnet 4.5 而不是最新版本：

```json theme={null}
{
  "model": "claude-sonnet-4-5",
  "availableModels": ["claude-sonnet-4-5", "haiku"],
  "env": {
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-5"
  }
}
```

没有 `env` 块，在选择器中选择"默认"的用户会获得最新的 Sonnet 版本，绕过 `model` 和 `availableModels` 中的版本固定。

### 合并行为

当 `availableModels` 在多个级别设置时，例如用户设置和项目设置，数组会被合并并去重。要强制执行严格的允许列表，请在托管或策略设置中设置 `availableModels`，这具有最高优先级。

### Mantle 模型 ID

当启用[Bedrock Mantle 端点](/zh-CN/amazon-bedrock#use-the-mantle-endpoint)时，`availableModels` 中以 `anthropic.` 开头的条目会作为自定义选项添加到 `/model` 选择器，并路由到 Mantle 端点。这是对[为第三方部署固定模型](#pin-models-for-third-party-deployments)中描述的仅别名匹配的例外。该设置仍然将选择器限制为列出的条目，因此请在任何 Mantle ID 旁边包含标准别名。

## 特殊模型行为

### `default` 模型设置

`default` 的行为取决于您的账户类型：

* **Max 和 Team Premium**：默认为 Opus 4.7
* **Pro、Team Standard、Enterprise 和 Anthropic API**：默认为 Sonnet 4.6
* **Bedrock、Vertex 和 Foundry**：默认为 Sonnet 4.5

如果您在使用 Opus 时达到使用阈值，Claude Code 可能会自动回退到 Sonnet。

<Note>
  2026 年 4 月 23 日，Enterprise 按使用量付费和 Anthropic API 用户的默认模型将更改为 Opus 4.7。要保持不同的默认值，请设置 `ANTHROPIC_MODEL` 或[服务器管理的设置](/zh-CN/server-managed-settings)中的 `model` 字段。
</Note>

### `opusplan` 模型设置

`opusplan` 模型别名提供了一种自动化的混合方法：

* **在 Plan Mode 中** - 使用 `opus` 进行复杂推理和架构决策
* **在执行模式中** - 自动切换到 `sonnet` 进行代码生成和实现

这为您提供了两全其美的方案：Opus 的卓越推理能力用于规划，Sonnet 的效率用于执行。

Plan Mode 中的 Opus 阶段使用标准的 200K 上下文窗口运行。[扩展上下文](#extended-context)中描述的自动 1M 升级适用于 `opus` 模型设置，不适用于 `opusplan`。

### 调整工作量级别

[工作量级别](https://platform.claude.com/docs/zh-CN/build-with-claude/effort)控制自适应推理，让模型根据任务复杂性决定是否以及在每一步思考多少。较低的工作量对于直接任务更快更便宜，而较高的工作量为复杂问题提供更深入的推理。

Opus 4.7、Opus 4.6 和 Sonnet 4.6 支持工作量。可用的级别取决于模型：

| 模型                    | 级别                                  |
| :-------------------- | :---------------------------------- |
| Opus 4.7              | `low`、`medium`、`high`、`xhigh`、`max` |
| Opus 4.6 和 Sonnet 4.6 | `low`、`medium`、`high`、`max`         |

如果您设置活跃模型不支持的级别，Claude Code 会回退到您设置的级别或以下的最高支持级别。例如，`xhigh` 在 Opus 4.6 上运行为 `high`。

从 v2.1.117 开始，Opus 4.7 上的默认工作量是 `xhigh`，Opus 4.6 和 Sonnet 4.6 上的默认工作量是 `high`。

当您首次运行 Opus 4.7 时，Claude Code 会应用 `xhigh`，即使您之前为 Opus 4.6 或 Sonnet 4.6 设置了不同的工作量级别。切换后再次运行 `/effort` 以选择不同的级别。

`low`、`medium`、`high` 和 `xhigh` 在会话间持续存在。`max` 提供最深入的推理，对令牌支出没有限制，仅适用于当前会话，除非通过 `CLAUDE_CODE_EFFORT_LEVEL` 环境变量设置。

#### 选择工作量级别

每个级别都在令牌支出和功能之间进行权衡。默认值适合大多数编码任务；当您想要不同的平衡时进行调整。

| 级别       | 何时使用                                        |
| :------- | :------------------------------------------ |
| `low`    | 保留用于短期、范围有限、延迟敏感且不需要高智能的任务                  |
| `medium` | 减少成本敏感工作的令牌使用，可以权衡一些智能                      |
| `high`   | 平衡令牌使用和智能。用作智能敏感工作的最低要求，或相对于 `xhigh` 减少令牌支出 |
| `xhigh`  | 大多数编码和代理任务的最佳结果。Opus 4.7 上的推荐默认值            |
| `max`    | 可以改进困难任务的性能，但可能显示收益递减，容易过度思考。在广泛采用前进行测试     |

工作量规模按模型校准，因此相同的级别名称在不同模型中不代表相同的基础值。

#### 使用 ultrathink 进行一次性深入推理

在您的提示中的任何位置包含 `ultrathink` 以请求在该轮进行更深入的推理，而无需更改您的会话工作量设置。Claude Code 识别该关键字并添加上下文内指令。发送到 API 的工作量级别保持不变。其他短语如"think"、"think hard"和"think more"会作为普通提示文本传递，不被识别为关键字。

#### 设置工作量级别

您可以通过以下任何方式更改工作量：

* **`/effort`**：运行不带参数的 `/effort` 打开交互式滑块，运行 `/effort` 后跟级别名称直接设置，或运行 `/effort auto` 重置为模型默认值
* **在 `/model` 中**：选择模型时使用左右箭头键调整工作量滑块
* **`--effort` 标志**：在启动 Claude Code 时传递级别名称为单个会话设置
* **环境变量**：设置 `CLAUDE_CODE_EFFORT_LEVEL` 为级别名称或 `auto`
* **设置**：在设置文件中设置 `effortLevel`
* **Skill 和 subagent frontmatter**：在 [skill](/zh-CN/skills#frontmatter-reference) 或 [subagent](/zh-CN/sub-agents#supported-frontmatter-fields) markdown 文件中设置 `effort` 以在该 skill 或 subagent 运行时覆盖工作量级别

环境变量优先于所有其他方法，然后是您配置的级别，然后是模型默认值。Frontmatter 工作量在该 skill 或 subagent 活跃时应用，覆盖会话级别但不覆盖环境变量。

当选择支持的模型时，工作量滑块会出现在 `/model` 中。当前工作量级别也显示在徽标和旋转器旁边，例如"with low effort"，因此您可以确认哪个设置处于活动状态，而无需打开 `/model`。

#### 自适应推理和固定思考预算

自适应推理使思考在每一步都是可选的，因此 Claude 可以更快地响应常规提示，并为受益于思考的步骤保留更深入的思考。如果您希望 Claude 比当前级别产生的思考更多或更少，您可以直接在您的提示或 `CLAUDE.md` 中说明；模型会在其工作量设置范围内响应该指导。

Opus 4.7 始终使用自适应推理。固定思考预算模式和 `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` 不适用于它。

在 Opus 4.6 和 Sonnet 4.6 上，您可以设置 `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` 以恢复到由 `MAX_THINKING_TOKENS` 控制的先前固定思考预算。请参阅[环境变量](/zh-CN/env-vars)。

### 扩展思考

扩展思考是 Claude 在响应前发出的推理。在支持[自适应推理](#adjust-effort-level)的模型上，工作量级别是控制发生多少思考的主要方式；下面的设置打开或关闭思考并控制其显示方式。

| 控制        | 如何设置                                                                                                          |
| :-------- | :------------------------------------------------------------------------------------------------------------ |
| 当前会话的切换   | 在 macOS 上按 `Option+T` 或在 Windows 和 Linux 上按 `Alt+T`                                                           |
| 设置全局默认值   | 运行 `/config` 并切换思考模式。保存为 `~/.claude/settings.json` 中的 `alwaysThinkingEnabled`                                 |
| 无论工作量如何禁用 | 设置 [`MAX_THINKING_TOKENS=0`](/zh-CN/env-vars)。其他值仅适用于[固定思考预算](#adaptive-reasoning-and-fixed-thinking-budgets) |

思考输出默认折叠。按 `Ctrl+O` 切换详细模式并将推理显示为灰色斜体文本。Anthropic API 上的交互式会话默认接收编辑后的思考块，因此如果您想在展开时获得完整摘要，请在[设置](/zh-CN/settings)中设置 `showThinkingSummaries: true`。您需要为所有生成的思考令牌付费，即使它们被折叠或编辑。

### 扩展上下文

Opus 4.7、Opus 4.6 和 Sonnet 4.6 支持[100 万令牌上下文窗口](https://platform.claude.com/docs/zh-CN/build-with-claude/context-windows#1m-token-context-window)用于包含大型代码库的长会话。

可用性因模型和计划而异。在 Max、Team 和 Enterprise 计划上，Opus 会自动升级到 1M 上下文，无需额外配置。这适用于 Team Standard 和 Team Premium 席位。

| 计划                    | Opus with 1M context                                                                        | Sonnet with 1M context                                                                      |
| --------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Max、Team 和 Enterprise | 包含在订阅中                                                                                      | 需要[额外使用](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |
| Pro                   | 需要[额外使用](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) | 需要[额外使用](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |
| API 和按使用量付费           | 完全访问                                                                                        | 完全访问                                                                                        |

要完全禁用 1M 上下文，请设置 `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`。这会从模型选择器中删除 1M 模型变体。请参阅[环境变量](/zh-CN/env-vars)。

1M 上下文窗口使用标准模型定价，超过 200K 的令牌无需额外费用。对于订阅中包含扩展上下文的计划，使用仍由您的订阅覆盖。对于通过额外使用访问扩展上下文的计划，令牌计入额外使用。

如果您的账户支持 1M 上下文，该选项会出现在最新版本的 Claude Code 的模型选择器（`/model`）中。如果您看不到它，请尝试重新启动您的会话。

您也可以将 `[1m]` 后缀与模型别名或完整模型名称一起使用：

```bash theme={null}
# 使用 opus[1m] 或 sonnet[1m] 别名
/model opus[1m]
/model sonnet[1m]

# 或将 [1m] 附加到完整模型名称
/model claude-opus-4-7[1m]
```

## 检查您当前的模型

您可以通过多种方式查看您当前使用的模型：

1. 在[状态行](/zh-CN/statusline)中（如果已配置）
2. 在 `/status` 中，它也显示您的账户信息。

## 添加自定义模型选项

使用 `ANTHROPIC_CUSTOM_MODEL_OPTION` 向 `/model` 选择器添加单个自定义条目，而无需替换内置别名。这对于测试 Claude Code 默认不列出的模型 ID 很有用。对于 LLM 网关部署，当设置 `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` 时，Claude Code 可以从网关的 `/v1/models` 端点自动填充选择器，因此仅当发现被禁用或未返回您想要的模型时才需要此变量。请参阅 [LLM 网关模型选择](/zh-CN/llm-gateway#model-selection)。

此示例设置所有三个变量以使网关路由的 Opus 部署可选择：

```bash theme={null}
export ANTHROPIC_CUSTOM_MODEL_OPTION="my-gateway/claude-opus-4-7"
export ANTHROPIC_CUSTOM_MODEL_OPTION_NAME="Opus via Gateway"
export ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION="Custom deployment routed through the internal LLM gateway"
```

自定义条目出现在 `/model` 选择器的底部。`ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` 和 `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` 是可选的。如果省略，模型 ID 用作名称，描述默认为 `Custom model (<model-id>)`。

Claude Code 跳过对 `ANTHROPIC_CUSTOM_MODEL_OPTION` 中设置的模型 ID 的验证，因此您可以使用您的 API 端点接受的任何字符串。

## 环境变量

您可以使用以下环境变量，这些变量必须是完整的**模型名称**（或您的 API 提供商的等效项），以控制别名映射到的模型名称。

| 环境变量                             | 描述                                                          |
| -------------------------------- | ----------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`   | 用于 `opus` 的模型，或在 Plan Mode 活跃时用于 `opusplan` 的模型。            |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | 用于 `sonnet` 的模型，或在 Plan Mode 不活跃时用于 `opusplan` 的模型。         |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`  | 用于 `haiku` 的模型，或[后台功能](/zh-CN/costs#background-token-usage) |
| `CLAUDE_CODE_SUBAGENT_MODEL`     | 用于 [subagents](/zh-CN/sub-agents) 的模型                       |

注意：`ANTHROPIC_SMALL_FAST_MODEL` 已弃用，改为使用 `ANTHROPIC_DEFAULT_HAIKU_MODEL`。

### 为第三方部署固定模型

通过 [Bedrock](/zh-CN/amazon-bedrock)、[Vertex AI](/zh-CN/google-vertex-ai)、[Foundry](/zh-CN/microsoft-foundry) 或 [Claude Platform on AWS](/zh-CN/claude-platform-on-aws) 部署 Claude Code 时，在向用户推出前固定模型版本。

不固定模型，Claude Code 会使用模型别名（`sonnet`、`opus`、`haiku`），这些别名会解析为最新版本。当 Anthropic 发布新模型时，如果用户账户未启用新版本，Bedrock 和 Vertex AI 用户会看到通知并回退到该会话的先前版本，而 Foundry 用户会看到错误，因为 Foundry 没有等效的启动检查。

<Warning>
  在初始设置中将所有三个模型环境变量设置为特定版本 ID。固定让您控制用户何时迁移到新模型。
</Warning>

对您的提供商使用以下环境变量和特定版本的模型 ID：

| 提供商       | 示例                                                                   |
| :-------- | :------------------------------------------------------------------- |
| Bedrock   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-7'` |
| Vertex AI | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'`              |
| Foundry   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'`              |

对 `ANTHROPIC_DEFAULT_SONNET_MODEL` 和 `ANTHROPIC_DEFAULT_HAIKU_MODEL` 应用相同的模式。有关所有提供商的当前和旧版模型 ID，请参阅[模型概览](https://platform.claude.com/docs/zh-CN/about-claude/models/overview)。要将用户升级到新模型版本，请更新这些环境变量并重新部署。

要为固定模型启用[扩展上下文](#extended-context)，请在 `ANTHROPIC_DEFAULT_OPUS_MODEL` 或 `ANTHROPIC_DEFAULT_SONNET_MODEL` 中的模型 ID 后附加 `[1m]`：

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7[1m]'
```

`[1m]` 后缀将 1M 上下文窗口应用于该别名的所有使用，包括 `opusplan`。Claude Code 在将模型 ID 发送到您的提供商之前会删除该后缀。仅当底层模型支持 1M 上下文（如 Opus 4.7 或 Sonnet 4.6）时才附加 `[1m]`。

<Note>
  使用第三方提供商时，`settings.availableModels` 允许列表仍然适用。过滤与模型别名（`opus`、`sonnet`、`haiku`）匹配，而不是提供商特定的模型 ID。
</Note>

### 自定义固定模型显示和功能

当您在第三方提供商上固定模型时，提供商特定的 ID 在 `/model` 选择器中按原样显示，Claude Code 可能无法识别模型支持的功能。您可以使用每个固定模型的伴随环境变量覆盖显示名称并声明功能。

这些变量在第三方提供商（如 Bedrock、Vertex AI 和 Foundry）上生效。`_NAME` 和 `_DESCRIPTION` 变量在 `ANTHROPIC_BASE_URL` 指向 [LLM gateway](/zh-CN/llm-gateway) 时也生效。当直接连接到 `api.anthropic.com` 时无效。

| 环境变量                                                  | 描述                                                         |
| ----------------------------------------------------- | ---------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_NAME`                   | 固定 Opus 模型在 `/model` 选择器中的显示名称。未设置时默认为模型 ID                |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION`            | 固定 Opus 模型在 `/model` 选择器中的显示描述。未设置时默认为 `Custom Opus model` |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES` | 固定 Opus 模型支持的功能的逗号分隔列表                                     |

相同的 `_NAME`、`_DESCRIPTION` 和 `_SUPPORTED_CAPABILITIES` 后缀可用于 `ANTHROPIC_DEFAULT_SONNET_MODEL`、`ANTHROPIC_DEFAULT_HAIKU_MODEL` 和 `ANTHROPIC_CUSTOM_MODEL_OPTION`。

Claude Code 通过将模型 ID 与已知模式匹配来启用[工作量级别](#adjust-effort-level)和[扩展思考](#extended-thinking)等功能。提供商特定的 ID（如 Bedrock ARN 或自定义部署名称）通常与这些模式不匹配，导致支持的功能被禁用。设置 `_SUPPORTED_CAPABILITIES` 以告诉 Claude Code 模型实际支持的功能：

| 功能值                    | 启用                                          |
| ---------------------- | ------------------------------------------- |
| `effort`               | [工作量级别](#adjust-effort-level)和 `/effort` 命令 |
| `xhigh_effort`         | {/* min-version: 2.1.111 */}`xhigh` 工作量级别   |
| `max_effort`           | `max` 工作量级别                                 |
| `thinking`             | [扩展思考](#extended-thinking)                  |
| `adaptive_thinking`    | 根据任务复杂性动态分配思考的自适应推理                         |
| `interleaved_thinking` | 工具调用之间的思考                                   |

设置 `_SUPPORTED_CAPABILITIES` 时，列出的功能对匹配的固定模型启用，未列出的功能被禁用。未设置变量时，Claude Code 回退到基于模型 ID 的内置检测。

此示例将 Opus 固定到 Bedrock 自定义模型 ARN，设置友好名称，并声明其功能：

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='arn:aws:bedrock:us-east-1:123456789012:custom-model/abc'
export ANTHROPIC_DEFAULT_OPUS_MODEL_NAME='Opus via Bedrock'
export ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION='Opus 4.7 routed through a Bedrock custom endpoint'
export ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES='effort,xhigh_effort,max_effort,thinking,adaptive_thinking,interleaved_thinking'
```

### 按版本覆盖模型 ID

上面的家族级环境变量为每个家族别名配置一个模型 ID。如果您需要将同一家族中的多个版本映射到不同的提供商 ID，请改用 `modelOverrides` 设置。

`modelOverrides` 将单个 Anthropic 模型 ID 映射到 Claude Code 发送到您的提供商 API 的提供商特定字符串。当用户在 `/model` 选择器中选择映射的模型时，Claude Code 会使用您配置的值而不是内置默认值。

这让企业管理员可以将每个模型版本路由到特定的 Bedrock 推理配置文件 ARN、Vertex AI 版本名称或 Foundry 部署名称，用于治理、成本分配或区域路由。

在您的[设置文件](/zh-CN/settings#settings-files)中设置 `modelOverrides`：

```json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-7": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-sonnet-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/sonnet-prod"
  }
}
```

键必须是[模型概览](https://platform.claude.com/docs/zh-CN/about-claude/models/overview)中列出的 Anthropic 模型 ID。对于带日期的模型 ID，请包含日期后缀，完全按照其显示的方式。未知的键会被忽略。

覆盖替换了支持 `/model` 选择器中每个条目的内置模型 ID。在 Bedrock 上，覆盖优先于 Claude Code 在启动时自动发现的任何推理配置文件。您直接通过 `ANTHROPIC_MODEL`、`--model` 或 `ANTHROPIC_DEFAULT_*_MODEL` 环境变量提供的值会按原样传递给提供商，不会被 `modelOverrides` 转换。

`modelOverrides` 与 `availableModels` 一起工作。允许列表针对 Anthropic 模型 ID 进行评估，而不是覆盖值，因此 `availableModels` 中的条目（如 `"opus"`）即使在 Opus 版本映射到 ARN 时也会继续匹配。

### Prompt caching 配置

Claude Code 自动使用 [prompt caching](https://platform.claude.com/docs/zh-CN/build-with-claude/prompt-caching) 来优化性能并降低成本。您可以全局禁用 prompt caching 或针对特定模型层级禁用：

| 环境变量                            | 描述                                        |
| ------------------------------- | ----------------------------------------- |
| `DISABLE_PROMPT_CACHING`        | 设置为 `1` 以禁用所有模型的 prompt caching（优先于按模型设置） |
| `DISABLE_PROMPT_CACHING_HAIKU`  | 设置为 `1` 以仅禁用 Haiku 模型的 prompt caching     |
| `DISABLE_PROMPT_CACHING_SONNET` | 设置为 `1` 以仅禁用 Sonnet 模型的 prompt caching    |
| `DISABLE_PROMPT_CACHING_OPUS`   | 设置为 `1` 以仅禁用 Opus 模型的 prompt caching      |

这些环境变量为您提供了对 prompt caching 行为的细粒度控制。全局 `DISABLE_PROMPT_CACHING` 设置优先于模型特定的设置，允许您在需要时快速禁用所有缓存。按模型的设置对于选择性控制很有用，例如在调试特定模型或与可能具有不同缓存实现的云提供商合作时。
