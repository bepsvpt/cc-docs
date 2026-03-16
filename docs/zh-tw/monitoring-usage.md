> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 監控

> 了解如何為 Claude Code 啟用和配置 OpenTelemetry。

Claude Code 支援 OpenTelemetry (OTel) 指標和事件，用於監控和可觀測性。

所有指標都是透過 OpenTelemetry 的標準指標協議匯出的時間序列資料，事件則透過 OpenTelemetry 的日誌/事件協議匯出。使用者有責任確保其指標和日誌後端已正確配置，且聚合粒度符合其監控需求。

## 快速開始

使用環境變數配置 OpenTelemetry：

```bash  theme={null}
# 1. 啟用遙測
export CLAUDE_CODE_ENABLE_TELEMETRY=1

# 2. 選擇匯出器（兩者都是可選的 - 僅配置您需要的）
export OTEL_METRICS_EXPORTER=otlp       # 選項：otlp、prometheus、console
export OTEL_LOGS_EXPORTER=otlp          # 選項：otlp、console

# 3. 配置 OTLP 端點（用於 OTLP 匯出器）
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# 4. 設定身份驗證（如果需要）
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer your-token"

# 5. 用於除錯：減少匯出間隔
export OTEL_METRIC_EXPORT_INTERVAL=10000  # 10 秒（預設：60000ms）
export OTEL_LOGS_EXPORT_INTERVAL=5000     # 5 秒（預設：5000ms）

# 6. 執行 Claude Code
claude
```

<Note>
  預設匯出間隔為指標 60 秒和日誌 5 秒。在設定期間，您可能希望使用較短的間隔用於除錯目的。記得在生產環境中重設這些值。
</Note>

如需完整配置選項，請參閱 [OpenTelemetry 規範](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options)。

## 管理員配置

管理員可以透過[受管設定檔](/zh-TW/settings#settings-files)為所有使用者配置 OpenTelemetry 設定。這允許在整個組織中集中控制遙測設定。請參閱[設定優先順序](/zh-TW/settings#settings-precedence)以了解有關如何應用設定的更多資訊。

受管設定配置範例：

```json  theme={null}
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.company.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer company-token"
  }
}
```

<Note>
  受管設定可以透過 MDM（行動裝置管理）或其他裝置管理解決方案進行分發。在受管設定檔中定義的環境變數具有高優先順序，使用者無法覆蓋。
</Note>

## 配置詳情

### 常見配置變數

| 環境變數                                            | 描述                                | 範例值                                |
| ----------------------------------------------- | --------------------------------- | ---------------------------------- |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                  | 啟用遙測收集（必需）                        | `1`                                |
| `OTEL_METRICS_EXPORTER`                         | 指標匯出器類型（逗號分隔）                     | `console`、`otlp`、`prometheus`      |
| `OTEL_LOGS_EXPORTER`                            | 日誌/事件匯出器類型（逗號分隔）                  | `console`、`otlp`                   |
| `OTEL_EXPORTER_OTLP_PROTOCOL`                   | OTLP 匯出器的協議（所有訊號）                 | `grpc`、`http/json`、`http/protobuf` |
| `OTEL_EXPORTER_OTLP_ENDPOINT`                   | OTLP 收集器端點（所有訊號）                  | `http://localhost:4317`            |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL`           | 指標協議（覆蓋一般設定）                      | `grpc`、`http/json`、`http/protobuf` |
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`           | OTLP 指標端點（覆蓋一般設定）                 | `http://localhost:4318/v1/metrics` |
| `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL`              | 日誌協議（覆蓋一般設定）                      | `grpc`、`http/json`、`http/protobuf` |
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`              | OTLP 日誌端點（覆蓋一般設定）                 | `http://localhost:4318/v1/logs`    |
| `OTEL_EXPORTER_OTLP_HEADERS`                    | OTLP 的身份驗證標頭                      | `Authorization=Bearer token`       |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY`         | mTLS 身份驗證的用戶端金鑰                   | 用戶端金鑰檔案的路徑                         |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE` | mTLS 身份驗證的用戶端憑證                   | 用戶端憑證檔案的路徑                         |
| `OTEL_METRIC_EXPORT_INTERVAL`                   | 匯出間隔（毫秒）（預設：60000）                | `5000`、`60000`                     |
| `OTEL_LOGS_EXPORT_INTERVAL`                     | 日誌匯出間隔（毫秒）（預設：5000）               | `1000`、`10000`                     |
| `OTEL_LOG_USER_PROMPTS`                         | 啟用使用者提示內容的日誌記錄（預設：停用）             | `1` 以啟用                            |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`   | 重新整理動態標頭的間隔（預設：1740000ms / 29 分鐘） | `900000`                           |

### 指標基數控制

以下環境變數控制指標中包含哪些屬性以管理基數：

| 環境變數                                | 描述                           | 預設值     | 停用範例    |
| ----------------------------------- | ---------------------------- | ------- | ------- |
| `OTEL_METRICS_INCLUDE_SESSION_ID`   | 在指標中包含 session.id 屬性         | `true`  | `false` |
| `OTEL_METRICS_INCLUDE_VERSION`      | 在指標中包含 app.version 屬性        | `false` | `true`  |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | 在指標中包含 user.account\_uuid 屬性 | `true`  | `false` |

這些變數有助於控制指標的基數，這會影響指標後端中的儲存需求和查詢效能。較低的基數通常意味著更好的效能和更低的儲存成本，但分析的資料粒度較低。

### 動態標頭

對於需要動態身份驗證的企業環境，您可以配置指令碼來動態產生標頭：

#### 設定配置

新增至您的 `.claude/settings.json`：

```json  theme={null}
{
  "otelHeadersHelper": "/bin/generate_opentelemetry_headers.sh"
}
```

#### 指令碼需求

指令碼必須輸出有效的 JSON，其中包含代表 HTTP 標頭的字串鍵值對：

```bash  theme={null}
#!/bin/bash
# 範例：多個標頭
echo "{\"Authorization\": \"Bearer $(get-token.sh)\", \"X-API-Key\": \"$(get-api-key.sh)\"}"
```

#### 重新整理行為

標頭協助程式指令碼在啟動時執行，之後定期執行以支援權杖重新整理。預設情況下，指令碼每 29 分鐘執行一次。使用 `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS` 環境變數自訂間隔。

### 多團隊組織支援

具有多個團隊或部門的組織可以使用 `OTEL_RESOURCE_ATTRIBUTES` 環境變數新增自訂屬性以區分不同的群組：

```bash  theme={null}
# 新增自訂屬性以進行團隊識別
export OTEL_RESOURCE_ATTRIBUTES="department=engineering,team.id=platform,cost_center=eng-123"
```

這些自訂屬性將包含在所有指標和事件中，允許您：

* 按團隊或部門篩選指標
* 追蹤每個成本中心的成本
* 建立團隊特定的儀表板
* 為特定團隊設定警報

<Warning>
  **OTEL\_RESOURCE\_ATTRIBUTES 的重要格式要求：**

  `OTEL_RESOURCE_ATTRIBUTES` 環境變數遵循 [W3C Baggage 規範](https://www.w3.org/TR/baggage/)，具有嚴格的格式要求：

  * **不允許空格**：值不能包含空格。例如，`user.organizationName=My Company` 無效
  * **格式**：必須是逗號分隔的鍵=值對：`key1=value1,key2=value2`
  * **允許的字元**：僅限 US-ASCII 字元，不包括控制字元、空格、雙引號、逗號、分號和反斜線
  * **特殊字元**：允許範圍外的字元必須進行百分比編碼

  **範例：**

  ```bash  theme={null}
  # ❌ 無效 - 包含空格
  export OTEL_RESOURCE_ATTRIBUTES="org.name=John's Organization"

  # ✅ 有效 - 改用底線或駝峰式大小寫
  export OTEL_RESOURCE_ATTRIBUTES="org.name=Johns_Organization"
  export OTEL_RESOURCE_ATTRIBUTES="org.name=JohnsOrganization"

  # ✅ 有效 - 如果需要，對特殊字元進行百分比編碼
  export OTEL_RESOURCE_ATTRIBUTES="org.name=John%27s%20Organization"
  ```

  注意：將值用引號括起來不會逃逸空格。例如，`org.name="My Company"` 會產生字面值 `"My Company"`（包括引號），而不是 `My Company`。
</Warning>

### 配置範例

```bash  theme={null}
# 控制台除錯（1 秒間隔）
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console
export OTEL_METRIC_EXPORT_INTERVAL=1000

# OTLP/gRPC
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Prometheus
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=prometheus

# 多個匯出器
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console,otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=http/json

# 指標和日誌的不同端點/後端
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_METRICS_PROTOCOL=http/protobuf
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://metrics.company.com:4318
export OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://logs.company.com:4317

# 僅指標（無事件/日誌）
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# 僅事件/日誌（無指標）
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

## 可用的指標和事件

### 標準屬性

所有指標和事件共享這些標準屬性：

| 屬性                  | 描述                                             | 控制者                                          |
| ------------------- | ---------------------------------------------- | -------------------------------------------- |
| `session.id`        | 唯一的工作階段識別碼                                     | `OTEL_METRICS_INCLUDE_SESSION_ID`（預設：true）   |
| `app.version`       | 目前的 Claude Code 版本                             | `OTEL_METRICS_INCLUDE_VERSION`（預設：false）     |
| `organization.id`   | 組織 UUID（已驗證時）                                  | 可用時始終包含                                      |
| `user.account_uuid` | 帳戶 UUID（已驗證時）                                  | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID`（預設：true） |
| `terminal.type`     | 終端機類型（例如，`iTerm.app`、`vscode`、`cursor`、`tmux`） | 偵測到時始終包含                                     |

### 指標

Claude Code 匯出以下指標：

| 指標名稱                                  | 描述                  | 單位     |
| ------------------------------------- | ------------------- | ------ |
| `claude_code.session.count`           | 啟動的 CLI 工作階段計數      | count  |
| `claude_code.lines_of_code.count`     | 修改的程式碼行數計數          | count  |
| `claude_code.pull_request.count`      | 建立的提取請求數            | count  |
| `claude_code.commit.count`            | 建立的 git 提交數         | count  |
| `claude_code.cost.usage`              | Claude Code 工作階段的成本 | USD    |
| `claude_code.token.usage`             | 使用的權杖數              | tokens |
| `claude_code.code_edit_tool.decision` | 程式碼編輯工具權限決定的計數      | count  |
| `claude_code.active_time.total`       | 總活躍時間（秒）            | s      |

### 指標詳情

#### 工作階段計數器

在每個工作階段開始時遞增。

**屬性**：

* 所有[標準屬性](#standard-attributes)

#### 程式碼行計數器

在新增或移除程式碼時遞增。

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `type`：（`"added"`、`"removed"`）

#### 提取請求計數器

透過 Claude Code 建立提取請求時遞增。

**屬性**：

* 所有[標準屬性](#standard-attributes)

#### 提交計數器

透過 Claude Code 建立 git 提交時遞增。

**屬性**：

* 所有[標準屬性](#standard-attributes)

#### 成本計數器

在每個 API 請求後遞增。

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `model`：模型識別碼（例如，"claude-sonnet-4-5-20250929"）

#### 權杖計數器

在每個 API 請求後遞增。

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `type`：（`"input"`、`"output"`、`"cacheRead"`、`"cacheCreation"`）
* `model`：模型識別碼（例如，"claude-sonnet-4-5-20250929"）

#### 程式碼編輯工具決定計數器

當使用者接受或拒絕 Edit、Write 或 NotebookEdit 工具使用時遞增。

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `tool`：工具名稱（`"Edit"`、`"Write"`、`"NotebookEdit"`）
* `decision`：使用者決定（`"accept"`、`"reject"`）
* `language`：編輯檔案的程式設計語言（例如，`"TypeScript"`、`"Python"`、`"JavaScript"`、`"Markdown"`）。對於無法識別的副檔名，傳回 `"unknown"`。

#### 活躍時間計數器

追蹤實際花費在主動使用 Claude Code 上的時間（非閒置時間）。此指標在使用者互動期間遞增，例如輸入提示或接收回應。

**屬性**：

* 所有[標準屬性](#standard-attributes)

### 事件

Claude Code 透過 OpenTelemetry 日誌/事件匯出以下事件（當配置 `OTEL_LOGS_EXPORTER` 時）：

#### 使用者提示事件

當使用者提交提示時記錄。

**事件名稱**：`claude_code.user_prompt`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"user_prompt"`
* `event.timestamp`：ISO 8601 時間戳
* `prompt_length`：提示的長度
* `prompt`：提示內容（預設為編輯，使用 `OTEL_LOG_USER_PROMPTS=1` 啟用）

#### 工具結果事件

當工具完成執行時記錄。

**事件名稱**：`claude_code.tool_result`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"tool_result"`
* `event.timestamp`：ISO 8601 時間戳
* `tool_name`：工具的名稱
* `success`：`"true"` 或 `"false"`
* `duration_ms`：執行時間（毫秒）
* `error`：錯誤訊息（如果失敗）
* `decision`：`"accept"` 或 `"reject"`
* `source`：決定來源 - `"config"`、`"user_permanent"`、`"user_temporary"`、`"user_abort"` 或 `"user_reject"`
* `tool_parameters`：包含工具特定參數的 JSON 字串（如果可用）
  * 對於 Bash 工具：包括 `bash_command`、`full_command`、`timeout`、`description`、`sandbox`

#### API 請求事件

為每個 API 請求記錄到 Claude。

**事件名稱**：`claude_code.api_request`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"api_request"`
* `event.timestamp`：ISO 8601 時間戳
* `model`：使用的模型（例如，"claude-sonnet-4-5-20250929"）
* `cost_usd`：估計成本（美元）
* `duration_ms`：請求持續時間（毫秒）
* `input_tokens`：輸入權杖數
* `output_tokens`：輸出權杖數
* `cache_read_tokens`：從快取讀取的權杖數
* `cache_creation_tokens`：用於快取建立的權杖數

#### API 錯誤事件

當 API 請求到 Claude 失敗時記錄。

**事件名稱**：`claude_code.api_error`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"api_error"`
* `event.timestamp`：ISO 8601 時間戳
* `model`：使用的模型（例如，"claude-sonnet-4-5-20250929"）
* `error`：錯誤訊息
* `status_code`：HTTP 狀態碼（如果適用）
* `duration_ms`：請求持續時間（毫秒）
* `attempt`：嘗試次數（用於重試的請求）

#### 工具決定事件

當做出工具權限決定（接受/拒絕）時記錄。

**事件名稱**：`claude_code.tool_decision`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"tool_decision"`
* `event.timestamp`：ISO 8601 時間戳
* `tool_name`：工具的名稱（例如，"Read"、"Edit"、"Write"、"NotebookEdit"）
* `decision`：`"accept"` 或 `"reject"`
* `source`：決定來源 - `"config"`、`"user_permanent"`、`"user_temporary"`、`"user_abort"` 或 `"user_reject"`

## 解釋指標和事件資料

Claude Code 匯出的指標提供了對使用模式和生產力的寶貴見解。以下是您可以建立的一些常見視覺化和分析：

### 使用情況監控

| 指標                                                            | 分析機會                          |
| ------------------------------------------------------------- | ----------------------------- |
| `claude_code.token.usage`                                     | 按 `type`（輸入/輸出）、使用者、團隊或模型進行細分 |
| `claude_code.session.count`                                   | 追蹤一段時間內的採用和參與度                |
| `claude_code.lines_of_code.count`                             | 透過追蹤程式碼新增/移除來衡量生產力            |
| `claude_code.commit.count` & `claude_code.pull_request.count` | 了解對開發工作流程的影響                  |

### 成本監控

`claude_code.cost.usage` 指標有助於：

* 追蹤跨團隊或個人的使用趨勢
* 識別高使用量工作階段以進行最佳化

<Note>
  成本指標是近似值。如需官方帳單資料，請參閱您的 API 提供者（Claude Console、AWS Bedrock 或 Google Cloud Vertex）。
</Note>

### 警報和分段

要考慮的常見警報：

* 成本尖峰
* 異常的權杖消耗
* 來自特定使用者的高工作階段量

所有指標都可以按 `user.account_uuid`、`organization.id`、`session.id`、`model` 和 `app.version` 進行分段。

### 事件分析

事件資料提供了對 Claude Code 互動的詳細見解：

**工具使用模式**：分析工具結果事件以識別：

* 最常使用的工具
* 工具成功率
* 平均工具執行時間
* 按工具類型的錯誤模式

**效能監控**：追蹤 API 請求持續時間和工具執行時間以識別效能瓶頸。

## 後端考量

您選擇的指標和日誌後端決定了您可以執行的分析類型：

### 對於指標

* **時間序列資料庫（例如，Prometheus）**：速率計算、聚合指標
* **欄式存儲（例如，ClickHouse）**：複雜查詢、唯一使用者分析
* **功能完整的可觀測性平台（例如，Honeycomb、Datadog）**：進階查詢、視覺化、警報

### 對於事件/日誌

* **日誌聚合系統（例如，Elasticsearch、Loki）**：全文搜尋、日誌分析
* **欄式存儲（例如，ClickHouse）**：結構化事件分析
* **功能完整的可觀測性平台（例如，Honeycomb、Datadog）**：指標和事件之間的關聯

對於需要日活躍使用者/週活躍使用者/月活躍使用者 (DAU/WAU/MAU) 指標的組織，請考慮支援高效唯一值查詢的後端。

## 服務資訊

所有指標和事件都使用以下資源屬性匯出：

* `service.name`：`claude-code`
* `service.version`：目前的 Claude Code 版本
* `os.type`：作業系統類型（例如，`linux`、`darwin`、`windows`）
* `os.version`：作業系統版本字串
* `host.arch`：主機架構（例如，`amd64`、`arm64`）
* `wsl.version`：WSL 版本號（僅在 Windows Subsystem for Linux 上執行時出現）
* 計量器名稱：`com.anthropic.claude_code`

## ROI 測量資源

如需有關測量 Claude Code 投資回報率的綜合指南，包括遙測設定、成本分析、生產力指標和自動化報告，請參閱 [Claude Code ROI 測量指南](https://github.com/anthropics/claude-code-monitoring-guide)。此儲存庫提供現成可用的 Docker Compose 配置、Prometheus 和 OpenTelemetry 設定，以及用於產生與 Linear 等工具整合的生產力報告的範本。

## 安全性/隱私考量

* 遙測是選擇加入的，需要明確配置
* 敏感資訊（如 API 金鑰或檔案內容）永遠不會包含在指標或事件中
* 使用者提示內容預設為編輯 - 僅記錄提示長度。若要啟用使用者提示日誌記錄，請設定 `OTEL_LOG_USER_PROMPTS=1`

## 在 Amazon Bedrock 上監控 Claude Code

如需 Amazon Bedrock 上 Claude Code 使用情況監控的詳細指南，請參閱 [Claude Code 監控實作 (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)。
