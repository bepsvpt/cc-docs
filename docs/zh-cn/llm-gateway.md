> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# LLM gateway 配置

> 了解如何配置 Claude Code 以使用 LLM gateway 解决方案。涵盖网关要求、身份验证配置、模型选择和特定提供商的端点设置。

LLM gateway 提供了 Claude Code 和模型提供商之间的集中代理层，通常提供以下功能：

* **集中身份验证** - API 密钥管理的单一入口
* **使用情况跟踪** - 监控团队和项目的使用情况
* **成本控制** - 实施预算和速率限制
* **审计日志** - 跟踪所有模型交互以实现合规性
* **模型路由** - 无需更改代码即可在提供商之间切换

## 网关要求

为了使 LLM gateway 与 Claude Code 配合使用，它必须满足以下要求：

**API 格式**

网关必须向客户端公开以下至少一种 API 格式：

1. **Anthropic Messages**: `/v1/messages`, `/v1/messages/count_tokens`
   * 必须转发请求头：`anthropic-beta`、`anthropic-version`

2. **Bedrock InvokeModel**: `/invoke`, `/invoke-with-response-stream`
   * 必须保留请求体字段：`anthropic_beta`、`anthropic_version`

3. **Vertex rawPredict**: `:rawPredict`、`:streamRawPredict`、`/count-tokens:rawPredict`
   * 必须转发请求头：`anthropic-beta`、`anthropic-version`

未能转发请求头或保留请求体字段可能导致功能减少或无法使用 Claude Code 功能。

<Note>
  Claude Code 根据 API 格式确定要启用的功能。当使用 Bedrock 或 Vertex 的 Anthropic Messages 格式时，您可能需要设置环境变量 `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`。
</Note>

**请求头**

Claude Code 在每个 API 请求上包含以下请求头：

| 请求头                             | 描述                                                                                             |
| :------------------------------ | :--------------------------------------------------------------------------------------------- |
| `X-Claude-Code-Session-Id`      | 当前 Claude Code 会话的唯一标识符。代理可以使用此标识符来聚合来自单个会话的所有 API 请求，而无需解析请求体。                                |
| `X-Claude-Code-Agent-Id`        | 发出请求的子代理或队友的标识符。您的代理可以使用此标识符将 API 成本归属于会话内的各个并行子代理，而无需解析请求体。仅在由进程内子代理或队友发出的请求中出现。              |
| `X-Claude-Code-Parent-Agent-Id` | 生成发出请求的代理的代理的标识符。将此与 `X-Claude-Code-Agent-Id` 一起使用，以在您的代理中跨嵌套代理归属 API 成本。仅当请求代理本身由另一个代理生成时才出现。 |

两个代理 ID 请求头都是每次生成的临时标识符，而不是持久的用户或设备 ID。

Claude Code 还会在系统提示前面添加一个简短的归属块，其中包含客户端版本和从对话派生的指纹。Anthropic API 在处理前会删除此块，因此不会影响第一方提示缓存。如果您的网关实现了自己的提示缓存（以完整请求体为键），请设置 [`CLAUDE_CODE_ATTRIBUTION_HEADER=0`](/zh-CN/env-vars) 以省略它。

## 配置

### 模型选择

默认情况下，Claude Code 使用所选 API 格式的标准模型名称。

当 `ANTHROPIC_BASE_URL` 指向一个公开 Anthropic Messages 格式的网关时，Claude Code 在启动时可以查询网关的 `/v1/models` 端点，并将返回的模型添加到 `/model` 选择器中。设置 `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` 来启用此功能。默认情况下发现功能是关闭的，以便由共享 API 密钥支持的网关不会向每个用户显示该密钥可以访问的每个模型。每个发现的条目都标记为"From gateway"，并在响应中提供 `display_name` 字段时使用该字段。这需要 Claude Code v2.1.129 或更高版本。

发现功能仅适用于 Anthropic Messages 格式。它不会对 Bedrock 或 Vertex 直通端点运行，也不会在 `ANTHROPIC_BASE_URL` 未设置或指向 `api.anthropic.com` 时运行。

发现请求的身份验证方式与推理请求相同：它将 `ANTHROPIC_AUTH_TOKEN` 作为 bearer 令牌发送，或在未设置身份验证令牌时将 `ANTHROPIC_API_KEY` 作为 `x-api-key` 标头发送，以及来自 `ANTHROPIC_CUSTOM_HEADERS` 的任何标头。只有 ID 以 `claude` 或 `anthropic` 开头的模型才会被添加到选择器中。结果被缓存到 `~/.claude/cache/gateway-models.json`，并在每次启动时刷新。如果请求失败或网关未实现 `/v1/models`，选择器将回退到上一次启动时的缓存列表或内置模型列表。

如果您的网关使用与发现过滤器不匹配的模型名称，请使用 [模型配置](/zh-CN/model-config) 中记录的环境变量来手动添加它们。

## LiteLLM 配置

<Warning>
  LiteLLM PyPI 版本 1.82.7 和 1.82.8 被恶意软件感染，存在凭证窃取风险。请勿安装这些版本。如果您已经安装了它们：

  * 删除该软件包
  * 轮换受影响系统上的所有凭证
  * 按照 [BerriAI/litellm#24518](https://github.com/BerriAI/litellm/issues/24518) 中的补救步骤进行操作

  LiteLLM 是第三方代理服务。Anthropic 不认可、维护或审计 LiteLLM 的安全性或功能。本指南仅供参考，可能会过时。请自行判断使用。
</Warning>

### 前置条件

* Claude Code 更新到最新版本
* LiteLLM Proxy Server 已部署且可访问
* 通过您选择的提供商访问 Claude 模型

### 基本 LiteLLM 设置

**配置 Claude Code**：

#### 身份验证方法

##### 静态 API 密钥

使用固定 API 密钥的最简单方法：

```bash theme={null}
# 在环境中设置
export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key

# 或在 Claude Code 设置中
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-litellm-static-key"
  }
}
```

此值将作为 `Authorization` 请求头发送。

##### 使用辅助程序的动态 API 密钥

用于轮换密钥或按用户身份验证：

1. 创建 API 密钥辅助程序脚本：

```bash theme={null}
#!/bin/bash
# ~/bin/get-litellm-key.sh

# 示例：从保险库获取密钥
vault kv get -field=api_key secret/litellm/claude-code

# 示例：生成 JWT 令牌
jwt encode \
  --secret="${JWT_SECRET}" \
  --exp="+1h" \
  '{"user":"'${USER}'","team":"engineering"}'
```

2. 配置 Claude Code 设置以使用辅助程序：

```json theme={null}
{
  "apiKeyHelper": "~/bin/get-litellm-key.sh"
}
```

3. 设置令牌刷新间隔：

```bash theme={null}
# 每小时刷新一次（3600000 毫秒）
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000
```

此值将作为 `Authorization` 和 `X-Api-Key` 请求头发送。`apiKeyHelper` 的优先级低于 `ANTHROPIC_AUTH_TOKEN` 或 `ANTHROPIC_API_KEY`。

#### 统一端点（推荐）

使用 LiteLLM 的 [Anthropic 格式端点](https://docs.litellm.ai/docs/anthropic_unified)：

```bash theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000
```

**统一端点相对于直通端点的优势：**

* 负载均衡
* 故障转移
* 对成本跟踪和最终用户跟踪的一致支持

#### 特定提供商的直通端点（替代方案）

##### 通过 LiteLLM 的 Claude API

使用 [直通端点](https://docs.litellm.ai/docs/pass_through/anthropic_completion)：

```bash theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic
```

##### 通过 LiteLLM 的 Amazon Bedrock

使用 [直通端点](https://docs.litellm.ai/docs/pass_through/bedrock)：

```bash theme={null}
export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1
```

##### 通过 LiteLLM 的 Google Vertex AI

使用 [直通端点](https://docs.litellm.ai/docs/pass_through/vertex_ai)：

```bash theme={null}
export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
```

##### 通过网关的 AWS 上的 Claude Platform

路由到转发到 [AWS 上的 Claude Platform](/zh-CN/claude-platform-on-aws) 端点的网关：

```bash theme={null}
export ANTHROPIC_AWS_BASE_URL=https://litellm-server:4000/anthropic-aws
export ANTHROPIC_AWS_WORKSPACE_ID=wrkspc_01ABCDEFGHIJKLMN
export CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH=1
export CLAUDE_CODE_USE_ANTHROPIC_AWS=1
```

有关更多详细信息，请参阅 [LiteLLM 文档](https://docs.litellm.ai/)。

## 其他资源

* [LiteLLM 文档](https://docs.litellm.ai/)
* [Claude Code 设置](/zh-CN/settings)
* [企业网络配置](/zh-CN/network-config)
* [第三方集成概述](/zh-CN/third-party-integrations)
