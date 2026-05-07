> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# LLM gateway 配置

> 了解如何配置 Claude Code 以使用 LLM gateway 解決方案。涵蓋 gateway 要求、身份驗證配置、模型選擇和提供商特定的端點設置。

LLM gateway 提供了 Claude Code 和模型提供商之間的集中代理層，通常提供：

* **集中身份驗證** - 單一 API 密鑰管理點
* **使用情況追蹤** - 監控跨團隊和項目的使用情況
* **成本控制** - 實施預算和速率限制
* **審計日誌** - 追蹤所有模型交互以進行合規性檢查
* **模型路由** - 無需更改代碼即可在提供商之間切換

## Gateway 要求

為了讓 LLM gateway 與 Claude Code 配合使用，它必須滿足以下要求：

**API 格式**

gateway 必須向客戶端公開以下至少一種 API 格式：

1. **Anthropic Messages**: `/v1/messages`, `/v1/messages/count_tokens`
   * 必須轉發請求標頭：`anthropic-beta`、`anthropic-version`

2. **Bedrock InvokeModel**: `/invoke`, `/invoke-with-response-stream`
   * 必須保留請求正文字段：`anthropic_beta`、`anthropic_version`

3. **Vertex rawPredict**: `:rawPredict`、`:streamRawPredict`、`/count-tokens:rawPredict`
   * 必須轉發請求標頭：`anthropic-beta`、`anthropic-version`

未能轉發標頭或保留正文字段可能會導致功能減少或無法使用 Claude Code 功能。

<Note>
  Claude Code 根據 API 格式確定要啟用的功能。使用 Bedrock 或 Vertex 的 Anthropic Messages 格式時，您可能需要設置環境變數 `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`。
</Note>

**請求標頭**

Claude Code 在每個 API 請求上包含以下標頭：

| 標頭                         | 描述                                                               |
| :------------------------- | :--------------------------------------------------------------- |
| `X-Claude-Code-Session-Id` | 當前 Claude Code 會話的唯一識別符。代理可以使用此識別符來聚合來自單個會話的所有 API 請求，而無需解析請求正文。 |

Claude Code 還在系統提示前面添加了一個簡短的歸屬塊，其中包含客戶端版本和從對話派生的指紋。Anthropic API 在處理前會刪除此塊，因此不會影響第一方提示快取。如果您的 gateway 實現了自己的提示快取，其密鑰基於完整請求正文，請設置 [`CLAUDE_CODE_ATTRIBUTION_HEADER=0`](/zh-TW/env-vars) 以省略它。

## 配置

### 模型選擇

默認情況下，Claude Code 使用所選 API 格式的標準模型名稱。

當 `ANTHROPIC_BASE_URL` 指向公開 Anthropic Messages 格式的 gateway 時，Claude Code 在啟動時會查詢 gateway 的 `/v1/models` 端點，並將返回的模型添加到 `/model` 選擇器中。設置 `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` 以啟用此功能。發現功能默認關閉，以便由共享 API 金鑰支持的 gateway 不會向每個用戶公開該金鑰可以訪問的每個模型。每個發現的條目都標記為「From gateway」，並在提供時使用響應中的 `display_name` 欄位。這需要 Claude Code v2.1.129 或更高版本。

發現功能僅適用於 Anthropic Messages 格式。它不會針對 Bedrock 或 Vertex 傳遞端點運行，也不會在 `ANTHROPIC_BASE_URL` 未設置或指向 `api.anthropic.com` 時運行。

發現請求的身份驗證方式與推理請求相同：它將 `ANTHROPIC_AUTH_TOKEN` 作為 bearer token 發送，或在未設置身份驗證令牌時將 `ANTHROPIC_API_KEY` 作為 `x-api-key` 標頭發送，以及來自 `ANTHROPIC_CUSTOM_HEADERS` 的任何標頭。只有 ID 以 `claude` 或 `anthropic` 開頭的模型才會添加到選擇器中。結果被緩存到 `~/.claude/cache/gateway-models.json`，並在每次啟動時刷新。如果請求失敗或 gateway 未實現 `/v1/models`，選擇器將回退到上次啟動時的緩存列表或內置模型列表。

如果您的 gateway 使用與發現篩選器不匹配的模型名稱，請使用 [模型配置](/zh-TW/model-config) 中記錄的環境變數手動添加它們。

## LiteLLM 配置

<Warning>
  LiteLLM PyPI 版本 1.82.7 和 1.82.8 被盜竊憑證的惡意軟體破壞。請勿安裝這些版本。如果您已經安裝了它們：

  * 移除該軟體包
  * 輪換受影響系統上的所有憑證
  * 按照 [BerriAI/litellm#24518](https://github.com/BerriAI/litellm/issues/24518) 中的補救步驟進行操作

  LiteLLM 是第三方代理服務。Anthropic 不認可、維護或審計 LiteLLM 的安全性或功能。本指南僅供參考，可能會過時。請自行決定是否使用。
</Warning>

### 先決條件

* Claude Code 已更新至最新版本
* LiteLLM Proxy Server 已部署且可訪問
* 通過您選擇的提供商訪問 Claude 模型

### 基本 LiteLLM 設置

**配置 Claude Code**：

#### 身份驗證方法

##### 靜態 API 密鑰

使用固定 API 密鑰的最簡單方法：

```bash theme={null}
# 在環境中設置
export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key

# 或在 Claude Code 設置中
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-litellm-static-key"
  }
}
```

此值將作為 `Authorization` 標頭發送。

##### 使用幫助程序的動態 API 密鑰

用於輪換密鑰或按用戶身份驗證：

1. 創建 API 密鑰幫助程序腳本：

```bash theme={null}
#!/bin/bash
# ~/bin/get-litellm-key.sh

# 示例：從保管庫獲取密鑰
vault kv get -field=api_key secret/litellm/claude-code

# 示例：生成 JWT 令牌
jwt encode \
  --secret="${JWT_SECRET}" \
  --exp="+1h" \
  '{"user":"'${USER}'","team":"engineering"}'
```

2. 配置 Claude Code 設置以使用幫助程序：

```json theme={null}
{
  "apiKeyHelper": "~/bin/get-litellm-key.sh"
}
```

3. 設置令牌刷新間隔：

```bash theme={null}
# 每小時刷新一次（3600000 毫秒）
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000
```

此值將作為 `Authorization` 和 `X-Api-Key` 標頭發送。`apiKeyHelper` 的優先級低於 `ANTHROPIC_AUTH_TOKEN` 或 `ANTHROPIC_API_KEY`。

#### 統一端點（推薦）

使用 LiteLLM 的 [Anthropic 格式端點](https://docs.litellm.ai/docs/anthropic_unified)：

```bash theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000
```

**統一端點相對於傳遞端點的優勢：**

* 負載均衡
* 故障轉移
* 對成本追蹤和最終用戶追蹤的一致支持

#### 提供商特定的傳遞端點（替代方案）

##### 通過 LiteLLM 的 Claude API

使用 [傳遞端點](https://docs.litellm.ai/docs/pass_through/anthropic_completion)：

```bash theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic
```

##### 通過 LiteLLM 的 Amazon Bedrock

使用 [傳遞端點](https://docs.litellm.ai/docs/pass_through/bedrock)：

```bash theme={null}
export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1
```

##### 通過 LiteLLM 的 Google Vertex AI

使用 [傳遞端點](https://docs.litellm.ai/docs/pass_through/vertex_ai)：

```bash theme={null}
export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
```

有關更多詳細信息，請參閱 [LiteLLM 文檔](https://docs.litellm.ai/)。

## 其他資源

* [LiteLLM 文檔](https://docs.litellm.ai/)
* [Claude Code 設置](/zh-TW/settings)
* [企業網絡配置](/zh-TW/network-config)
* [第三方集成概述](/zh-TW/third-party-integrations)
