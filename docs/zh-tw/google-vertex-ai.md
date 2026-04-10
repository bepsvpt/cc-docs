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

# Google Vertex AI 上的 Claude Code

> 了解如何透過 Google Vertex AI 設定 Claude Code，包括設定、IAM 設定和故障排除。

## 先決條件

在使用 Vertex AI 設定 Claude Code 之前，請確保您具有：

* 已啟用計費的 Google Cloud Platform (GCP) 帳戶
* 已啟用 Vertex AI API 的 GCP 專案
* 存取所需的 Claude 模型（例如 Claude Sonnet 4.6）
* 已安裝並設定 Google Cloud SDK (`gcloud`)
* 在所需的 GCP 區域中分配的配額

<Note>
  如果您要將 Claude Code 部署給多個使用者，請[固定您的模型版本](#5-pin-model-versions)，以防止在 Anthropic 發佈新模型時發生中斷。
</Note>

## 區域設定

Claude Code 可與 Vertex AI [全球](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai)和區域端點搭配使用。

<Note>
  Vertex AI 可能不支援所有[區域](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models)或[全球端點](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models)上的 Claude Code 預設模型。您可能需要切換到支援的區域、使用區域端點或指定支援的模型。
</Note>

## 設定

### 1. 啟用 Vertex AI API

在您的 GCP 專案中啟用 Vertex AI API：

```bash  theme={null}
# 設定您的專案 ID
gcloud config set project YOUR-PROJECT-ID

# 啟用 Vertex AI API
gcloud services enable aiplatform.googleapis.com
```

### 2. 要求模型存取

在 Vertex AI 中要求存取 Claude 模型：

1. 導覽至 [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. 搜尋「Claude」模型
3. 要求存取所需的 Claude 模型（例如 Claude Sonnet 4.6）
4. 等待核准（可能需要 24-48 小時）

### 3. 設定 GCP 認證

Claude Code 使用標準的 Google Cloud 驗證。

如需詳細資訊，請參閱 [Google Cloud 驗證文件](https://cloud.google.com/docs/authentication)。

<Note>
  進行驗證時，Claude Code 將自動使用 `ANTHROPIC_VERTEX_PROJECT_ID` 環境變數中的專案 ID。若要覆寫此設定，請設定下列其中一個環境變數：`GCLOUD_PROJECT`、`GOOGLE_CLOUD_PROJECT` 或 `GOOGLE_APPLICATION_CREDENTIALS`。
</Note>

### 4. 設定 Claude Code

設定下列環境變數：

```bash  theme={null}
# 啟用 Vertex AI 整合
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# 選用：覆寫 Vertex 端點 URL 以用於自訂端點或閘道
# export ANTHROPIC_VERTEX_BASE_URL=https://aiplatform.googleapis.com

# 選用：如需要，停用 prompt caching
export DISABLE_PROMPT_CACHING=1

# 當 CLOUD_ML_REGION=global 時，覆寫不支援全球端點的模型的區域
export VERTEX_REGION_CLAUDE_HAIKU_4_5=us-east5
export VERTEX_REGION_CLAUDE_4_6_SONNET=europe-west1
```

每個模型版本都有其自己的 `VERTEX_REGION_CLAUDE_*` 變數。如需完整清單，請參閱[環境變數參考](/zh-TW/env-vars)。檢查 [Vertex Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) 以確定哪些模型支援全球端點與僅限區域端點。

當您指定 `cache_control` 暫時旗標時，[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) 會自動支援。若要停用它，請設定 `DISABLE_PROMPT_CACHING=1`。如需提高速率限制，請聯絡 Google Cloud 支援。使用 Vertex AI 時，`/login` 和 `/logout` 命令會被停用，因為驗證是透過 Google Cloud 認證處理的。

### 5. 固定模型版本

<Warning>
  為每個部署固定特定的模型版本。如果您使用模型別名（`sonnet`、`opus`、`haiku`）而不固定版本，Claude Code 可能會嘗試使用未在您的 Vertex AI 專案中啟用的較新模型版本，在 Anthropic 發佈更新時破壞現有使用者。
</Warning>

將這些環境變數設定為特定的 Vertex AI 模型 ID：

```bash  theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

如需目前和舊版模型 ID，請參閱[模型概覽](https://platform.claude.com/docs/en/about-claude/models/overview)。如需完整的環境變數清單，請參閱[模型設定](/zh-TW/model-config#pin-models-for-third-party-deployments)。

未設定固定變數時，Claude Code 使用這些預設模型：

| 模型類型    | 預設值                          |
| :------ | :--------------------------- |
| 主要模型    | `claude-sonnet-4-5@20250929` |
| 小型/快速模型 | `claude-haiku-4-5@20251001`  |

若要進一步自訂模型：

```bash  theme={null}
export ANTHROPIC_MODEL='claude-opus-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

## IAM 設定

指派所需的 IAM 權限：

`roles/aiplatform.user` 角色包含所需的權限：

* `aiplatform.endpoints.predict` - 模型呼叫和權杖計數所需

如需更嚴格的權限，請建立只包含上述權限的自訂角色。

如需詳細資訊，請參閱 [Vertex IAM 文件](https://cloud.google.com/vertex-ai/docs/general/access-control)。

<Note>
  為 Claude Code 建立專用的 GCP 專案，以簡化成本追蹤和存取控制。
</Note>

## 1M token context window

Claude Opus 4.6、Sonnet 4.6、Sonnet 4.5 和 Sonnet 4 在 Vertex AI 上支援 [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window)。當您選擇 1M 模型變體時，Claude Code 會自動啟用擴展 context window。

若要為您的固定模型啟用 1M context window，請在模型 ID 後附加 `[1m]`。如需詳細資訊，請參閱[為第三方部署固定模型](/zh-TW/model-config#pin-models-for-third-party-deployments)。

## 故障排除

如果您遇到配額問題：

* 透過 [Cloud Console](https://cloud.google.com/docs/quotas/view-manage) 檢查目前配額或要求增加配額

如果您遇到「找不到模型」404 錯誤：

* 確認模型在 [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) 中已啟用
* 驗證您有權存取指定的區域
* 如果使用 `CLOUD_ML_REGION=global`，請檢查您的模型是否在 [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) 中的「支援的功能」下支援全球端點。對於不支援全球端點的模型，請執行下列其中一項：
  * 透過 `ANTHROPIC_MODEL` 或 `ANTHROPIC_DEFAULT_HAIKU_MODEL` 指定支援的模型，或
  * 使用 `VERTEX_REGION_<MODEL_NAME>` 環境變數設定區域端點

如果您遇到 429 錯誤：

* 對於區域端點，請確保主要模型和小型/快速模型在您選擇的區域中受支援
* 考慮切換到 `CLOUD_ML_REGION=global` 以獲得更好的可用性

## 其他資源

* [Vertex AI 文件](https://cloud.google.com/vertex-ai/docs)
* [Vertex AI 定價](https://cloud.google.com/vertex-ai/pricing)
* [Vertex AI 配額和限制](https://cloud.google.com/vertex-ai/docs/quotas)
