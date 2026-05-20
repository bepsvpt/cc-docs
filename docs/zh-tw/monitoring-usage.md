> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 監控

> 了解如何為 Claude Code 啟用和配置 OpenTelemetry。

透過 OpenTelemetry (OTel) 匯出遙測資料，追蹤 Claude Code 在整個組織中的使用情況、成本和工具活動。Claude Code 透過標準指標協議匯出指標作為時間序列資料、透過日誌/事件協議匯出事件，以及可選地透過[追蹤協議](#traces-beta)匯出分散式追蹤。配置您的指標、日誌和追蹤後端以符合您的監控需求。

## 快速開始

使用環境變數配置 OpenTelemetry：

```bash theme={null}
# 1. 啟用遙測
export CLAUDE_CODE_ENABLE_TELEMETRY=1

# 2. 選擇匯出器（兩者都是可選的 - 僅配置您需要的）
export OTEL_METRICS_EXPORTER=otlp       # 選項：otlp、prometheus、console、none
export OTEL_LOGS_EXPORTER=otlp          # 選項：otlp、console、none

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

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.example.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer example-token"
  }
}
```

<Note>
  受管設定可以透過 MDM（行動裝置管理）或其他裝置管理解決方案進行分發。在受管設定檔中定義的環境變數具有高優先順序，使用者無法覆蓋。
</Note>

Claude Code 不會將 `OTEL_*` 環境變數傳遞給它產生的子程序，包括 Bash 工具、hooks、MCP 伺服器和語言伺服器。透過 Bash 工具執行的 OpenTelemetry 檢測應用程式不會繼承 Claude Code 的匯出器端點或標頭，因此如果該應用程式需要匯出自己的遙測，請直接在命令中設定這些變數。

## 配置詳情

### 常見配置變數

| 環境變數                                                | 描述                                                                                                                                                                                                          | 範例值                                                                  |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                      | 啟用遙測收集（必需）                                                                                                                                                                                                  | `1`                                                                  |
| `OTEL_METRICS_EXPORTER`                             | 指標匯出器類型，逗號分隔。使用 `none` 以停用                                                                                                                                                                                  | `console`、`otlp`、`prometheus`、`none`                                 |
| `OTEL_LOGS_EXPORTER`                                | 日誌/事件匯出器類型，逗號分隔。使用 `none` 以停用                                                                                                                                                                               | `console`、`otlp`、`none`                                              |
| `OTEL_EXPORTER_OTLP_PROTOCOL`                       | OTLP 匯出器的協議，適用於所有訊號                                                                                                                                                                                         | `grpc`、`http/json`、`http/protobuf`                                   |
| `OTEL_EXPORTER_OTLP_ENDPOINT`                       | 所有訊號的 OTLP 收集器端點                                                                                                                                                                                            | `http://localhost:4317`                                              |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL`               | 指標協議，覆蓋一般設定                                                                                                                                                                                                 | `grpc`、`http/json`、`http/protobuf`                                   |
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`               | OTLP 指標端點，覆蓋一般設定                                                                                                                                                                                            | `http://localhost:4318/v1/metrics`                                   |
| `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL`                  | 日誌協議，覆蓋一般設定                                                                                                                                                                                                 | `grpc`、`http/json`、`http/protobuf`                                   |
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`                  | OTLP 日誌端點，覆蓋一般設定                                                                                                                                                                                            | `http://localhost:4318/v1/logs`                                      |
| `OTEL_EXPORTER_OTLP_HEADERS`                        | OTLP 的身份驗證標頭                                                                                                                                                                                                | `Authorization=Bearer token`                                         |
| `OTEL_METRIC_EXPORT_INTERVAL`                       | 匯出間隔（毫秒）（預設：60000）                                                                                                                                                                                          | `5000`、`60000`                                                       |
| `OTEL_LOGS_EXPORT_INTERVAL`                         | 日誌匯出間隔（毫秒）（預設：5000）                                                                                                                                                                                         | `1000`、`10000`                                                       |
| `OTEL_LOG_USER_PROMPTS`                             | 啟用使用者提示內容的日誌記錄（預設：停用）                                                                                                                                                                                       | `1` 以啟用                                                              |
| `OTEL_LOG_TOOL_DETAILS`                             | 啟用在工具事件和追蹤跨度屬性中記錄工具參數和輸入引數的日誌：Bash 命令、MCP 伺服器和工具名稱、技能名稱和工具輸入。也在 `user_prompt` 事件上啟用自訂、plugin 和 MCP 命令名稱（預設：停用）                                                                                              | `1` 以啟用                                                              |
| `OTEL_LOG_TOOL_CONTENT`                             | 啟用在跨度事件中記錄工具輸入和輸出內容的日誌（預設：停用）。需要[追蹤](#traces-beta)。內容在 60 KB 處截斷                                                                                                                                            | `1` 以啟用                                                              |
| `OTEL_LOG_RAW_API_BODIES`                           | 將完整的 Anthropic Messages API 請求和回應 JSON 作為 `api_request_body` / `api_response_body` 日誌事件發出（預設：停用）。主體包括整個對話歷史記錄。啟用此選項意味著同意 `OTEL_LOG_USER_PROMPTS`、`OTEL_LOG_TOOL_DETAILS` 和 `OTEL_LOG_TOOL_CONTENT` 會揭露的所有內容 | `1` 用於在 60 KB 處截斷的內聯主體，或 `file:<dir>` 用於磁碟上未截斷的主體，事件中有 `body_ref` 指標 |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` | 指標時間性偏好（預設：`delta`）。如果您的後端期望累積時間性，請設定為 `cumulative`                                                                                                                                                         | `delta`、`cumulative`                                                 |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`       | 重新整理動態標頭的間隔（預設：1740000ms / 29 分鐘）                                                                                                                                                                           | `900000`                                                             |

### mTLS 身份驗證

您為 OTLP 匯出器配置用戶端憑證的方式取決於該訊號使用的 OTLP 協議，透過 `OTEL_EXPORTER_OTLP_PROTOCOL` 或每個訊號的覆蓋設定。相同的配置適用於指標、日誌和追蹤。

| 協議                          | 用戶端憑證變數                                                                                                                                          | 信任收集器的 CA                        |
| :-------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------- |
| `http/protobuf`、`http/json` | `CLAUDE_CODE_CLIENT_CERT`、`CLAUDE_CODE_CLIENT_KEY` 和可選的 `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE`。請參閱[網路配置](/zh-TW/network-config#mtls-authentication) | `NODE_EXTRA_CA_CERTS`            |
| `grpc`                      | `OTEL_EXPORTER_OTLP_CLIENT_KEY` 和 `OTEL_EXPORTER_OTLP_CLIENT_CERTIFICATE`，或每個訊號的變體，例如 `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY` 以針對每個訊號使用不同的憑證     | `OTEL_EXPORTER_OTLP_CERTIFICATE` |

對於 `grpc`，OpenTelemetry SDK 直接讀取標準 OTLP 變數，因此設定每個訊號指標變數的現有配置會繼續運作。

### 指標基數控制

以下環境變數控制指標中包含哪些屬性以管理基數：

| 環境變數                                | 描述                                              | 預設值     | 停用範例    |
| ----------------------------------- | ----------------------------------------------- | ------- | ------- |
| `OTEL_METRICS_INCLUDE_SESSION_ID`   | 在指標中包含 session.id 屬性                            | `true`  | `false` |
| `OTEL_METRICS_INCLUDE_VERSION`      | 在指標中包含 app.version 屬性                           | `false` | `true`  |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | 在指標中包含 user.account\_uuid 和 user.account\_id 屬性 | `true`  | `false` |

這些變數有助於控制指標的基數，這會影響指標後端中的儲存需求和查詢效能。較低的基數通常意味著更好的效能和更低的儲存成本，但分析的資料粒度較低。

### Traces (beta)

分散式追蹤匯出跨度，將每個使用者提示連結到它觸發的 API 請求和工具執行，因此您可以在追蹤後端中將完整請求檢視為單個追蹤。

追蹤預設為關閉。若要啟用它，請同時設定 `CLAUDE_CODE_ENABLE_TELEMETRY=1` 和 `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`，然後設定 `OTEL_TRACES_EXPORTER` 以選擇跨度的傳送位置。追蹤重複使用[常見 OTLP 配置](#common-configuration-variables)以取得端點、協議、標頭和 [mTLS](#mtls-authentication)。

| 環境變數                                  | 描述                                              | 範例值                                |
| ------------------------------------- | ----------------------------------------------- | ---------------------------------- |
| `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` | 啟用跨度追蹤（必需）。也接受 `ENABLE_ENHANCED_TELEMETRY_BETA` | `1`                                |
| `OTEL_TRACES_EXPORTER`                | 追蹤匯出器類型，逗號分隔。使用 `none` 以停用                      | `console`、`otlp`、`none`            |
| `OTEL_EXPORTER_OTLP_TRACES_PROTOCOL`  | 追蹤協議，覆蓋 `OTEL_EXPORTER_OTLP_PROTOCOL`           | `grpc`、`http/json`、`http/protobuf` |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT`  | OTLP 追蹤端點，覆蓋 `OTEL_EXPORTER_OTLP_ENDPOINT`      | `http://localhost:4318/v1/traces`  |
| `OTEL_TRACES_EXPORT_INTERVAL`         | 跨度批次匯出間隔（毫秒）（預設：5000）                           | `1000`、`10000`                     |

跨度預設會編輯使用者提示文字、工具輸入詳情和工具內容。設定 `OTEL_LOG_USER_PROMPTS=1`、`OTEL_LOG_TOOL_DETAILS=1` 和 `OTEL_LOG_TOOL_CONTENT=1` 以包含它們。

當追蹤處於活動狀態時，Bash 和 PowerShell 子程序會自動繼承包含活動工具執行跨度的 W3C 追蹤上下文的 `TRACEPARENT` 環境變數。這讓任何讀取 `TRACEPARENT` 的子程序都可以在同一追蹤下將其自己的跨度作為父項，透過 Claude 執行的指令碼和命令啟用端到端分散式追蹤。

當追蹤處於活動狀態且 Claude Code 直接連接到 Anthropic API 時，每個模型請求都會攜帶設定為 `claude_code.llm_request` 跨度上下文的 W3C `traceparent` 標頭，並且 API 的 `traceresponse` 標頭被記錄為跨度連結。這些一起透過任何相容的中介將 Claude Code 的用戶端跨度連接到伺服器端追蹤。標頭不會傳送給第三方提供者。

在 Agent SDK 和以 `-p` 啟動的非互動式工作階段中，Claude Code 也會在啟動每個互動跨度時從其自己的環境中讀取 `TRACEPARENT` 和 `TRACESTATE`。這讓嵌入程序將其活動 W3C 追蹤上下文傳遞到子程序中，以便 Claude Code 的跨度顯示為呼叫者分散式追蹤的子項。互動式工作階段會忽略入站 `TRACEPARENT` 以避免意外繼承來自 CI 或容器環境的環境值。

#### 跨度階層

每個使用者提示啟動一個 `claude_code.interaction` 根跨度。API 呼叫、工具呼叫和 hook 執行被記錄為其子項。工具跨度有兩個自己的子跨度：一個用於等待權限決定所花費的時間，一個用於執行本身。當 Task 工具產生子代理時，子代理的 API 和工具跨度會嵌套在父項的 `claude_code.tool` 跨度下。

```text theme={null}
claude_code.interaction
├── claude_code.llm_request
├── claude_code.hook                    (requires detailed beta tracing)
└── claude_code.tool
    ├── claude_code.tool.blocked_on_user
    ├── claude_code.tool.execution
    └── (Task tool) subagent claude_code.llm_request / claude_code.tool spans
```

在 Agent SDK 和 `claude -p` 工作階段中，當環境中設定 `TRACEPARENT` 時，`claude_code.interaction` 本身會成為呼叫者跨度的子項。

#### 跨度屬性

每個跨度都帶有[標準屬性](#standard-attributes)加上與其名稱相符的 `span.type` 屬性。下表列出在每個跨度上設定的其他屬性。`llm_request`、`tool.execution` 和 `hook` 跨度在記錄失敗時設定 OpenTelemetry 狀態 `ERROR`；其他跨度始終以狀態 `UNSET` 結束。

**`claude_code.interaction`**

| 屬性                        | 描述                             | 由以下控制                   |
| ------------------------- | ------------------------------ | ----------------------- |
| `user_prompt`             | 提示文字。除非設定了閘道，否則值為 `<REDACTED>` | `OTEL_LOG_USER_PROMPTS` |
| `user_prompt_length`      | 提示長度（字元）                       |                         |
| `interaction.sequence`    | 此工作階段中互動的 1 為基數計數器             |                         |
| `interaction.duration_ms` | 輪次的牆上時間持續時間                    |                         |

**`claude_code.llm_request`**

| 屬性                               | 描述                                                                                                  | 由以下控制 |
| -------------------------------- | --------------------------------------------------------------------------------------------------- | ----- |
| `model`                          | 模型識別碼                                                                                               |       |
| `gen_ai.system`                  | 始終為 `anthropic`。OpenTelemetry GenAI 語義慣例                                                            |       |
| `gen_ai.request.model`           | 與 `model` 相同的值。OpenTelemetry GenAI 語義慣例                                                             |       |
| `query_source`                   | 發出請求的子系統，例如 `repl_main_thread` 或子代理名稱                                                               |       |
| `agent_id`                       | 發出請求的子代理或隊友的識別碼。在主工作階段上不存在                                                                          |       |
| `parent_agent_id`                | 產生此代理的代理的識別碼。對於主工作階段和直接從其產生的代理不存在                                                                   |       |
| `speed`                          | `fast` 或 `normal`                                                                                   |       |
| `llm_request.context`            | `interaction`、`tool` 或 `standalone`，取決於父跨度                                                          |       |
| `duration_ms`                    | 包括重試的牆上時間持續時間                                                                                       |       |
| `ttft_ms`                        | 首個權杖的時間（毫秒）                                                                                         |       |
| `input_tokens`                   | 來自 API 使用區塊的輸入權杖計數                                                                                  |       |
| `output_tokens`                  | 輸出權杖計數                                                                                              |       |
| `cache_read_tokens`              | 從提示快取讀取的權杖                                                                                          |       |
| `cache_creation_tokens`          | 寫入提示快取的權杖                                                                                           |       |
| `request_id`                     | 來自 `request-id` 回應標頭的 Anthropic API 請求 ID                                                           |       |
| `gen_ai.response.id`             | 與 `request_id` 相同的值。OpenTelemetry GenAI 語義慣例                                                        |       |
| `client_request_id`              | 最後一次嘗試的用戶端產生的 `x-client-request-id`                                                                 |       |
| `attempt`                        | 為此請求進行的總嘗試次數                                                                                        |       |
| `success`                        | `true` 或 `false`                                                                                    |       |
| `status_code`                    | 請求失敗時的 HTTP 狀態碼                                                                                     |       |
| `error`                          | 請求失敗時的錯誤訊息                                                                                          |       |
| `response.has_tool_call`         | 當回應包含工具使用區塊時為 `true`                                                                                |       |
| `stop_reason`                    | API 回應 `stop_reason`，例如 `end_turn`、`tool_use`、`max_tokens`、`stop_sequence`、`pause_turn` 或 `refusal` |       |
| `gen_ai.response.finish_reasons` | 與 `stop_reason` 相同的值，包裝在字串陣列中。OpenTelemetry GenAI 語義慣例                                              |       |

每次重試嘗試也被記錄為具有 `attempt` 和 `client_request_id` 屬性的 `gen_ai.request.attempt` 跨度事件。

**`claude_code.tool`**

| 屬性                | 描述                                | 由以下控制                   |
| ----------------- | --------------------------------- | ----------------------- |
| `tool_name`       | 工具名稱                              |                         |
| `duration_ms`     | 包括權限等待和執行的牆上時間持續時間                |                         |
| `result_tokens`   | 工具結果的近似權杖大小                       |                         |
| `agent_id`        | 發出請求的子代理或隊友的識別碼。在主工作階段上不存在        |                         |
| `parent_agent_id` | 產生此代理的代理的識別碼。對於主工作階段和直接從其產生的代理不存在 |                         |
| `file_path`       | Read、Edit 和 Write 工具的目標檔案路徑       | `OTEL_LOG_TOOL_DETAILS` |
| `full_command`    | Bash 工具的命令字串                      | `OTEL_LOG_TOOL_DETAILS` |
| `skill_name`      | Skill 工具的技能名稱                     | `OTEL_LOG_TOOL_DETAILS` |
| `subagent_type`   | Task 工具的子代理類型                     | `OTEL_LOG_TOOL_DETAILS` |

當 `OTEL_LOG_TOOL_CONTENT=1` 時，此跨度也會記錄一個 `tool.output` 跨度事件，其屬性包含工具的輸入和輸出主體，在每個屬性處截斷 60 KB。

**`claude_code.tool.blocked_on_user`**

| 屬性            | 描述                                    | 由以下控制 |
| ------------- | ------------------------------------- | ----- |
| `duration_ms` | 等待權限決定所花費的時間                          |       |
| `decision`    | `accept` 或 `reject`                   |       |
| `source`      | 決定來源，符合[工具決定事件](#tool-decision-event) |       |

**`claude_code.tool.execution`**

| 屬性            | 描述                                                            | 由以下控制                   |
| ------------- | ------------------------------------------------------------- | ----------------------- |
| `duration_ms` | 執行工具主體所花費的時間                                                  |                         |
| `success`     | `true` 或 `false`                                              |                         |
| `error`       | 執行失敗時的錯誤類別字串，例如 `Error:ENOENT` 或 `ShellError`。當設定了閘道時包含完整錯誤訊息 | `OTEL_LOG_TOOL_DETAILS` |

**`claude_code.hook`**

此跨度僅在詳細 beta 追蹤處於活動狀態時發出，除了上述追蹤匯出器配置外，還需要 `ENABLE_BETA_TRACING_DETAILED=1` 和 `BETA_TRACING_ENDPOINT`。在互動式 CLI 工作階段中，這也需要您的組織被列入該功能的允許清單。Agent SDK 和非互動式 `-p` 工作階段不受限制。當僅設定 `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` 時不會發出。

| 屬性                       | 描述                               | 由以下控制                   |
| ------------------------ | -------------------------------- | ----------------------- |
| `hook_event`             | Hook 事件類型，例如 `PreToolUse`        |                         |
| `hook_name`              | 完整 hook 名稱，例如 `PreToolUse:Write` |                         |
| `num_hooks`              | 執行的匹配 hook 命令數                   |                         |
| `hook_definitions`       | JSON 序列化的 hook 配置                | `OTEL_LOG_TOOL_DETAILS` |
| `duration_ms`            | 所有匹配 hook 的牆上時間持續時間              |                         |
| `num_success`            | 成功完成的 hook 計數                    |                         |
| `num_blocking`           | 傳回阻止決定的 hook 計數                  |                         |
| `num_non_blocking_error` | 在不阻止的情況下失敗的 hook 計數              |                         |
| `num_cancelled`          | 在完成前取消的 hook 計數                  |                         |

<Note>
  其他內容承載屬性，例如 `new_context`、`system_prompt_preview`、`user_system_prompt`、`tool_input` 和 `response.model_output`，僅在詳細 beta 追蹤處於活動狀態時發出。它們不是穩定跨度架構的一部分。`user_system_prompt` 另外需要 `OTEL_LOG_USER_PROMPTS=1`。它僅包含您透過 `systemPrompt` SDK 選項或 `--system-prompt` 和 `--append-system-prompt` 旗標提供的系統提示文字，在 60 KB 處截斷，並且每個工作階段發出一次而不是每個請求發出一次。
</Note>

### 動態標頭

對於需要動態身份驗證的企業環境，您可以配置指令碼來動態產生標頭。動態標頭僅適用於 `http/protobuf` 和 `http/json` 協議。`grpc` 匯出器僅使用靜態 `OTEL_EXPORTER_OTLP_HEADERS` 值。

#### 設定配置

新增至您的 `.claude/settings.json`：

```json theme={null}
{
  "otelHeadersHelper": "/bin/generate_opentelemetry_headers.sh"
}
```

#### 指令碼需求

指令碼必須輸出有效的 JSON，其中包含代表 HTTP 標頭的字串鍵值對：

```bash theme={null}
#!/bin/bash
# 範例：多個標頭
echo "{\"Authorization\": \"Bearer $(get-token.sh)\", \"X-API-Key\": \"$(get-api-key.sh)\"}"
```

#### 重新整理行為

標頭協助程式指令碼在啟動時執行，之後定期執行以支援權杖重新整理。預設情況下，指令碼每 29 分鐘執行一次。使用 `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS` 環境變數自訂間隔。

### 多團隊組織支援

具有多個團隊或部門的組織可以使用 `OTEL_RESOURCE_ATTRIBUTES` 環境變數新增自訂屬性以區分不同的群組：

```bash theme={null}
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

  `OTEL_RESOURCE_ATTRIBUTES` 環境變數使用逗號分隔的鍵=值對，具有嚴格的格式要求：

  * **不允許空格**：值不能包含空格。例如，`user.organizationName=My Company` 無效
  * **格式**：必須是逗號分隔的鍵=值對：`key1=value1,key2=value2`
  * **允許的字元**：僅限 US-ASCII 字元，不包括控制字元、空格、雙引號、逗號、分號和反斜線
  * **特殊字元**：允許範圍外的字元必須進行百分比編碼

  **範例：**

  ```bash theme={null}
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

在執行 `claude` 之前設定這些環境變數。每個區塊顯示不同匯出器或部署情境的完整配置：

```bash theme={null}
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
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://metrics.example.com:4318
export OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://logs.example.com:4317

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

| 屬性                  | 描述                                                             | 控制者                                          |
| ------------------- | -------------------------------------------------------------- | -------------------------------------------- |
| `session.id`        | 唯一的工作階段識別碼                                                     | `OTEL_METRICS_INCLUDE_SESSION_ID`（預設：true）   |
| `app.version`       | 目前的 Claude Code 版本                                             | `OTEL_METRICS_INCLUDE_VERSION`（預設：false）     |
| `organization.id`   | 組織 UUID（已驗證時）                                                  | 可用時始終包含                                      |
| `user.account_uuid` | 帳戶 UUID（已驗證時）                                                  | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID`（預設：true） |
| `user.account_id`   | 帳戶 ID（採用標籤格式，符合 Anthropic 管理 API），例如 `user_01BWBeN28...`（已驗證時） | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID`（預設：true） |
| `user.id`           | 匿名裝置/安裝識別碼，每個 Claude Code 安裝產生一次                               | 始終包含                                         |
| `user.email`        | 使用者電子郵件地址（透過 OAuth 驗證時）                                        | 可用時始終包含                                      |
| `terminal.type`     | 終端機類型，例如 `iTerm.app`、`vscode`、`cursor` 或 `tmux`                | 偵測到時始終包含                                     |

事件另外包含以下屬性。這些永遠不會附加到指標，因為它們會導致無限制的基數：

* `prompt.id`：UUID 將使用者提示與所有後續事件關聯到下一個提示。請參閱[事件關聯屬性](#event-correlation-attributes)。
* `workspace.host_paths`：在桌面應用程式中選擇的主機工作區目錄，作為字串陣列

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

每個指標都包含上面列出的標準屬性。具有額外內容特定屬性的指標如下所述。

#### 工作階段計數器

在每個工作階段開始時遞增。

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `start_type`：工作階段的啟動方式。`"fresh"`、`"resume"` 或 `"continue"` 之一

#### 程式碼行計數器

在新增或移除程式碼時遞增。

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `type`：（`"added"`、`"removed"`）

#### 提取請求計數器

透過 Claude Code 建立提取請求或合併請求時遞增。

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
* `model`：模型識別碼（例如，"claude-sonnet-4-6"）
* `query_source`：發出請求的子系統的類別。`"main"`、`"subagent"` 或 `"auxiliary"` 之一
* `speed`：當請求使用快速模式時為 `"fast"`。否則不存在
* `effort`：應用於請求的[努力等級](/zh-TW/model-config#adjust-effort-level)：`"low"`、`"medium"`、`"high"`、`"xhigh"` 或 `"max"`。當模型不支援努力時不存在。
* `agent.name`：發出請求的子代理類型。內建代理名稱和官方市場 plugin 的代理按原樣出現。其他使用者定義的代理名稱被替換為 `"custom"`。當請求不是由命名的子代理類型發出時不存在。
* `skill.name`：對請求有效的 Skill，由 Skill 工具、`/` 命令設定或由衍生的子代理繼承。內建、捆綁、使用者定義和官方市場 plugin skill 名稱按原樣出現。第三方 plugin skill 名稱被替換為 `"third-party"`。當沒有 skill 有效時不存在。
* `plugin.name`：當活躍 skill 或子代理由 plugin 提供時的擁有 plugin。官方市場 plugin 名稱按原樣出現。第三方 plugin 名稱被替換為 `"third-party"`。當 skill 和子代理都沒有擁有 plugin 時不存在。
* `marketplace.name`：擁有 plugin 的安裝市場。僅針對官方市場 plugin 發出。否則不存在。

#### 權杖計數器

在每個 API 請求後遞增。

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `type`：（`"input"`、`"output"`、`"cacheRead"`、`"cacheCreation"`）
* `model`：模型識別碼（例如，"claude-sonnet-4-6"）
* `query_source`：發出請求的子系統的類別。`"main"`、`"subagent"` 或 `"auxiliary"` 之一
* `speed`：當請求使用快速模式時為 `"fast"`。否則不存在
* `effort`：應用於請求的[努力等級](/zh-TW/model-config#adjust-effort-level)。詳見[成本計數器](#cost-counter)。
* `agent.name`、`skill.name`、`plugin.name`、`marketplace.name`：請求的 Skill、plugin 和代理歸屬。詳見[成本計數器](#cost-counter)以了解定義和編輯行為。

#### 程式碼編輯工具決定計數器

當使用者接受或拒絕 Edit、Write 或 NotebookEdit 工具使用時遞增。

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `tool_name`：工具名稱（`"Edit"`、`"Write"`、`"NotebookEdit"`）
* `decision`：使用者決定（`"accept"`、`"reject"`）
* `source`：決定來源。`"config"`、`"hook"`、`"user_permanent"`、`"user_temporary"`、`"user_abort"` 或 `"user_reject"` 之一。詳見[工具決定事件](#tool-decision-event)以了解每個值的含義。
* `language`：編輯檔案的程式設計語言，例如 `"TypeScript"`、`"Python"`、`"JavaScript"` 或 `"Markdown"`。對於無法識別的副檔名，傳回 `"unknown"`。

#### 活躍時間計數器

追蹤實際花費在主動使用 Claude Code 上的時間，不包括閒置時間。此指標在使用者互動期間遞增（輸入、讀取回應）以及在 CLI 處理期間遞增（工具執行、AI 回應產生）。

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `type`：`"user"` 用於鍵盤互動，`"cli"` 用於工具執行和 AI 回應

### 事件

Claude Code 透過 OpenTelemetry 日誌/事件匯出以下事件（當配置 `OTEL_LOGS_EXPORTER` 時）：

#### 事件關聯屬性

當使用者提交提示時，Claude Code 可能會進行多個 API 呼叫並執行多個工具。`prompt.id` 屬性可讓您將所有這些事件與觸發它們的單個提示相關聯。

| 屬性          | 描述                              |
| ----------- | ------------------------------- |
| `prompt.id` | UUID v4 識別碼，連結處理單個使用者提示時產生的所有事件 |

若要追蹤由單個提示觸發的所有活動，請按特定 `prompt.id` 值篩選您的事件。這會傳回使用者提示事件、任何 api\_request 事件以及處理該提示時發生的任何 tool\_result 事件。

<Note>
  `prompt.id` 有意從指標中排除，因為每個提示都會產生唯一的 ID，這會建立不斷增長的時間序列數量。僅將其用於事件級分析和稽核追蹤。
</Note>

#### 使用者提示事件

當使用者提交提示時記錄。

**事件名稱**：`claude_code.user_prompt`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"user_prompt"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `prompt_length`：提示的長度
* `prompt`：提示內容（預設為編輯，使用 `OTEL_LOG_USER_PROMPTS=1` 啟用）
* `command_name`：當提示叫用命令時的命令名稱。內建和捆綁的命令名稱（例如 `compact` 或 `debug`）按原樣發出；別名（例如 `reset`）按輸入方式發出而不是規範名稱。自訂、plugin 和 MCP 命令名稱除非設定 `OTEL_LOG_TOOL_DETAILS=1`，否則會摺疊為 `custom` 或 `mcp`
* `command_source`：命令的來源（如果存在）：`builtin`、`custom` 或 `mcp`。Plugin 提供的命令報告為 `custom`

#### 工具結果事件

當工具完成執行時記錄。

**事件名稱**：`claude_code.tool_result`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"tool_result"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `tool_name`：工具的名稱
* `tool_use_id`：此工具叫用的唯一識別碼。符合傳遞給 hooks 的 `tool_use_id`，允許 OTel 事件和 hook 擷取資料之間的關聯。
* `success`：`"true"` 或 `"false"`
* `duration_ms`：執行時間（毫秒）
* `error_type`：工具失敗時的錯誤類別字串，例如 `"Error:ENOENT"` 或 `"ShellError"`
* `error`（當 `OTEL_LOG_TOOL_DETAILS=1` 時）：工具失敗時的完整錯誤訊息
* `decision_type`：`"accept"` 或 `"reject"`
* `decision_source`：決定來源。`"config"`、`"hook"`、`"user_permanent"`、`"user_temporary"`、`"user_abort"` 或 `"user_reject"` 之一。詳見[工具決定事件](#tool-decision-event)以了解每個值的含義。
* `tool_input_size_bytes`：JSON 序列化工具輸入的大小（位元組）
* `tool_result_size_bytes`：工具結果的大小（位元組）
* `mcp_server_scope`：MCP 伺服器範圍識別碼（用於 MCP 工具）
* `tool_parameters`（當 `OTEL_LOG_TOOL_DETAILS=1` 時）：包含工具特定參數的 JSON 字串：
  * 對於 Bash 工具：包括 `bash_command`、`full_command`、`timeout`、`description`、`dangerouslyDisableSandbox` 和 `git_commit_id`（git commit 命令成功時的提交 SHA）
  * 對於 MCP 工具：包括 `mcp_server_name`、`mcp_tool_name`
  * 對於 Skill 工具：包括 `skill_name`
  * 對於 Task 工具：包括 `subagent_type`
* `tool_input`（當 `OTEL_LOG_TOOL_DETAILS=1` 時）：JSON 序列化的工具引數。超過 512 個字元的個別值會被截斷，整個承載的上限約為 4 K 字元。適用於所有工具，包括 MCP 工具。

#### API 請求事件

為每個 API 請求記錄到 Claude。

**事件名稱**：`claude_code.api_request`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"api_request"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `model`：使用的模型（例如，"claude-sonnet-4-6"）
* `cost_usd`：估計成本（美元）
* `duration_ms`：請求持續時間（毫秒）
* `input_tokens`：輸入權杖數
* `output_tokens`：輸出權杖數
* `cache_read_tokens`：從快取讀取的權杖數
* `cache_creation_tokens`：用於快取建立的權杖數
* `request_id`：來自回應的 `request-id` 標頭的 Anthropic API 請求 ID，例如 `"req_011..."`。僅當 API 傳回時才存在。
* `speed`：`"fast"` 或 `"normal"`，指示是否啟用了快速模式
* `query_source`：發出請求的子系統，例如 `"repl_main_thread"`、`"compact"` 或子代理名稱
* `effort`：應用於請求的[努力等級](/zh-TW/model-config#adjust-effort-level)：`"low"`、`"medium"`、`"high"`、`"xhigh"` 或 `"max"`。當模型不支援努力時不存在。

#### API 錯誤事件

當 API 請求到 Claude 失敗時記錄。

**事件名稱**：`claude_code.api_error`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"api_error"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `model`：使用的模型（例如，"claude-sonnet-4-6"）
* `error`：錯誤訊息
* `status_code`：HTTP 狀態碼（數字形式）。對於非 HTTP 錯誤（例如連線失敗），不存在。
* `duration_ms`：請求持續時間（毫秒）
* `attempt`：進行的嘗試總次數，包括初始請求（`1` 表示未發生重試）
* `request_id`：來自回應的 `request-id` 標頭的 Anthropic API 請求 ID，例如 `"req_011..."`。僅當 API 傳回時才存在。
* `speed`：`"fast"` 或 `"normal"`，指示是否啟用了快速模式
* `query_source`：發出請求的子系統，例如 `"repl_main_thread"`、`"compact"` 或子代理名稱
* `effort`：應用於請求的[努力等級](/zh-TW/model-config#adjust-effort-level)。當模型不支援努力時不存在。

#### API 請求主體事件

當設定 `OTEL_LOG_RAW_API_BODIES` 時，為每個 API 請求嘗試記錄。每次嘗試發出一個事件，因此使用調整參數的重試各自產生自己的事件。

**事件名稱**：`claude_code.api_request_body`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"api_request_body"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `body`：JSON 序列化的 Messages API 請求參數（系統提示、訊息、工具等），在 60 KB 處截斷。先前助手輪次中的擴展思考內容被編輯。僅在內聯模式下發出（`OTEL_LOG_RAW_API_BODIES=1`）。
* `body_ref`：包含未截斷主體的 `<dir>/<uuid>.request.json` 檔案的絕對路徑。僅在檔案模式下發出（`OTEL_LOG_RAW_API_BODIES=file:<dir>`）。
* `body_length`：未截斷的主體長度。當 `OTEL_LOG_RAW_API_BODIES=file:<dir>` 時為 UTF-8 位元組，或當 `=1` 時為 UTF-16 程式碼單位
* `body_truncated`：當發生內聯截斷時為 `"true"`。在檔案模式下和未發生截斷時不存在。
* `model`：來自請求參數的模型識別碼
* `query_source`：發出請求的子系統（例如，`"compact"`）

#### API 回應主體事件

當設定 `OTEL_LOG_RAW_API_BODIES` 時，為每個成功的 API 回應記錄。

**事件名稱**：`claude_code.api_response_body`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"api_response_body"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `body`：JSON 序列化的 Messages API 回應（id、內容區塊、使用情況、停止原因），在 60 KB 處截斷。擴展思考內容被編輯。僅在內聯模式下發出（`OTEL_LOG_RAW_API_BODIES=1`）。
* `body_ref`：包含未截斷主體的 `<dir>/<request_id>.response.json` 檔案的絕對路徑。僅在檔案模式下發出（`OTEL_LOG_RAW_API_BODIES=file:<dir>`）。
* `body_length`：未截斷的主體長度。當 `OTEL_LOG_RAW_API_BODIES=file:<dir>` 時為 UTF-8 位元組，或當 `=1` 時為 UTF-16 程式碼單位
* `body_truncated`：當發生內聯截斷時為 `"true"`。在檔案模式下和未發生截斷時不存在。
* `model`：模型識別碼
* `query_source`：發出請求的子系統
* `request_id`：來自回應的 `request-id` 標頭的 Anthropic API 請求 ID，例如 `"req_011..."`。僅當 API 傳回時才存在。

#### 工具決定事件

當做出工具權限決定（接受/拒絕）時記錄。

**事件名稱**：`claude_code.tool_decision`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"tool_decision"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `tool_name`：工具的名稱（例如，"Read"、"Edit"、"Write"、"NotebookEdit"）
* `tool_use_id`：此工具叫用的唯一識別碼。符合傳遞給 hooks 的 `tool_use_id`，允許 OTel 事件和 hook 擷取資料之間的關聯。
* `decision`：`"accept"` 或 `"reject"`
* `source`：決定來源：
  * `"config"`：根據專案設定、使用者個人設定中的允許規則、企業受管原則、`--allowedTools` 或 `--disallowedTools` 旗標、活躍權限模式、來自同一互動 CLI 工作階段中較早提示的工作階段範圍授予或因為工具本身是安全的，自動決定而不提示。該事件不指示這些來源中的哪一個相符。
  * `"hook"`：`PreToolUse` 或 `PermissionRequest` hook 傳回了決定。
  * `"user_permanent"`：當使用者在權限提示時選擇「是，且不再詢問...」時發出，將允許規則儲存到其個人設定。在互動 CLI 中，僅針對該選擇本身發出；稍後符合儲存規則的呼叫發出 `"config"` 代替。在 Agent SDK 或非互動 `-p` 工作階段中，初始選擇和稍後的規則相符都發出 `"user_permanent"`。視為接受。
  * `"user_temporary"`：當使用者在權限提示時選擇「是」或在檔案編輯或讀取提示時選擇「...在此工作階段期間」選項之一時發出。在互動 CLI 中，僅針對選擇本身發出；稍後由該工作階段範圍授予允許的呼叫發出 `"config"` 代替。在 Agent SDK 或非互動 `-p` 工作階段中，選擇和稍後的相符都發出 `"user_temporary"`。視為接受。
  * `"user_abort"`：當使用者關閉權限提示而不回答時發出。視為拒絕。
  * `"user_reject"`：當使用者選擇「否」時發出，或呼叫符合其個人設定中的拒絕規則。視為拒絕。

#### 權限模式變更事件

當權限模式變更時記錄，例如從 `Shift+Tab` 循環、退出計畫模式或自動模式閘道檢查。

**事件名稱**：`claude_code.permission_mode_changed`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"permission_mode_changed"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `from_mode`：先前的權限模式，例如 `"default"`、`"plan"`、`"acceptEdits"`、`"auto"` 或 `"bypassPermissions"`
* `to_mode`：新的權限模式
* `trigger`：導致變更的原因。`"shift_tab"`、`"exit_plan_mode"`、`"auto_gate_denied"` 或 `"auto_opt_in"` 之一。當轉換來自 SDK 或橋接時不存在。

#### 身份驗證事件

當 `/login` 或 `/logout` 完成時記錄。

**事件名稱**：`claude_code.auth`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"auth"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `action`：`"login"` 或 `"logout"`
* `success`：`"true"` 或 `"false"`
* `auth_method`：身份驗證方法，例如 `"oauth"`
* `error_category`：操作失敗時的分類錯誤類型。永遠不包括原始錯誤訊息
* `status_code`：操作因 HTTP 錯誤而失敗時的 HTTP 狀態碼（字串形式）

#### MCP 伺服器連線事件

當 MCP 伺服器連線、斷開連線或無法連線時記錄。

**事件名稱**：`claude_code.mcp_server_connection`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"mcp_server_connection"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `status`：`"connected"`、`"failed"` 或 `"disconnected"`
* `transport_type`：伺服器傳輸，例如 `"stdio"`、`"sse"` 或 `"http"`
* `server_scope`：伺服器配置的範圍，例如 `"user"`、`"project"` 或 `"local"`
* `duration_ms`：連線嘗試持續時間（毫秒）
* `error_code`：連線失敗時的錯誤碼
* `server_name`（當 `OTEL_LOG_TOOL_DETAILS=1` 時）：配置的伺服器名稱
* `error`（當 `OTEL_LOG_TOOL_DETAILS=1` 時）：連線失敗時的完整錯誤訊息

#### 內部錯誤事件

當 Claude Code 捕捉到意外的內部錯誤時記錄。僅記錄錯誤類別名稱和 errno 樣式碼。永遠不包括錯誤訊息和堆疊追蹤。當針對 Bedrock、Vertex 或 Foundry 執行或設定 `DISABLE_ERROR_REPORTING` 時，不會發出此事件。

**事件名稱**：`claude_code.internal_error`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"internal_error"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `error_name`：錯誤類別名稱，例如 `"TypeError"` 或 `"SyntaxError"`
* `error_code`：Node.js errno 碼，例如 `"ENOENT"`（如果存在於錯誤上）

#### Plugin 已安裝事件

當 plugin 完成安裝時記錄，來自 `claude plugin install` CLI 命令和互動式 `/plugin` UI。

**事件名稱**：`claude_code.plugin_installed`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"plugin_installed"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `marketplace.is_official`：如果市場是官方 Anthropic 市場，則為 `"true"`，否則為 `"false"`
* `install.trigger`：`"cli"` 或 `"ui"`
* `plugin.name`：已安裝 plugin 的名稱。對於第三方市場，僅當 `OTEL_LOG_TOOL_DETAILS=1` 時才包含
* `plugin.version`：Plugin 版本（如果在市場條目中宣告）。對於第三方市場，僅當 `OTEL_LOG_TOOL_DETAILS=1` 時才包含
* `marketplace.name`：安裝 plugin 的市場。對於第三方市場，僅當 `OTEL_LOG_TOOL_DETAILS=1` 時才包含

#### Plugin 已載入事件

在工作階段開始時為每個啟用的 plugin 記錄一次。使用此事件來清點您的整個環境中哪些 plugin 是活躍的，作為記錄安裝動作本身的 `plugin_installed` 的補充。

**事件名稱**：`claude_code.plugin_loaded`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"plugin_loaded"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `plugin.name`：plugin 的名稱。對於官方市場和內建捆綁之外的 plugin，除非 `OTEL_LOG_TOOL_DETAILS=1`，否則值為 `"third-party"`
* `marketplace.name`：plugin 的安裝市場（如果已知）。在與 `plugin.name` 相同的條件下編輯為 `"third-party"`
* `plugin.version`：來自 plugin 清單的版本。僅當名稱未被編輯且清單宣告版本時才包含
* `plugin.scope`：plugin 的來源類別：`"official"`、`"org"`、`"user-local"` 或 `"default-bundle"`
* `enabled_via`：plugin 如何被啟用的方式：`"default-enable"`、`"org-policy"`、`"seed-mount"` 或 `"user-install"`
* `plugin_id_hash`：plugin 名稱和市場的確定性雜湊，僅傳送到您配置的匯出器。讓您計算整個環境中載入了多少個不同的第三方 plugin，而無需記錄其名稱
* `has_hooks`：plugin 是否貢獻 hooks
* `has_mcp`：plugin 是否貢獻 MCP 伺服器
* `skill_path_count`：plugin 宣告的 skill 目錄數
* `command_path_count`：plugin 宣告的命令目錄數
* `agent_path_count`：plugin 宣告的代理目錄數

#### Skill 已啟動事件

當叫用 skill 時記錄，無論 Claude 是透過 Skill 工具呼叫它，還是您將其作為 `/` 命令執行。

**事件名稱**：`claude_code.skill_activated`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"skill_activated"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `skill.name`：Skill 的名稱。對於使用者定義和第三方 plugin skill，除非 `OTEL_LOG_TOOL_DETAILS=1`，否則值為預留位置 `"custom_skill"`
* `invocation_trigger`：Skill 的觸發方式（`"user-slash"`、`"claude-proactive"` 或 `"nested-skill"`）
* `skill.source`：Skill 的載入位置（例如，`"bundled"`、`"userSettings"`、`"projectSettings"`、`"plugin"`）
* `plugin.name`（當 `OTEL_LOG_TOOL_DETAILS=1` 或 plugin 來自官方市場時）：當 skill 由 plugin 提供時的擁有 plugin 名稱
* `marketplace.name`（當 `OTEL_LOG_TOOL_DETAILS=1` 或 plugin 來自官方市場時）：當 skill 由 plugin 提供時，擁有 plugin 的安裝市場

#### @ 提及事件

當 Claude Code 解析提示中的 `@` 提及時記錄。並非每個提及都會發出事件：早期退出路徑（例如權限拒絕、超大檔案、PDF 參考附件和目錄列表失敗）會在不記錄的情況下返回。

**事件名稱**：`claude_code.at_mention`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"at_mention"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `mention_type`：提及的類型（`"file"`、`"directory"`、`"agent"`、`"mcp_resource"`）
* `success`：提及是否成功解析（`"true"` 或 `"false"`）

#### API 重試已耗盡事件

當 API 請求在多次嘗試後失敗時記錄一次。與最終 `api_error` 事件一起發出。

**事件名稱**：`claude_code.api_retries_exhausted`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"api_retries_exhausted"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `model`：使用的模型
* `error`：最終錯誤訊息
* `status_code`：HTTP 狀態碼（數字形式）。對於非 HTTP 錯誤，不存在。
* `total_attempts`：進行的嘗試總次數
* `total_retry_duration_ms`：所有嘗試的總牆上時間
* `speed`：`"fast"` 或 `"normal"`

#### Hook 已註冊事件

在工作階段開始時為每個配置的 hook 記錄一次。使用此事件來清點您的整個環境中哪些 hook 是活躍的，作為每次執行 `hook_execution_start` 和 `hook_execution_complete` 事件的補充。

**事件名稱**：`claude_code.hook_registered`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"hook_registered"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `hook_event`：hook 事件類型，例如 `"PreToolUse"` 或 `"PostToolUse"`
* `hook_type`：hook 實作類型：`"command"`、`"prompt"`、`"mcp_tool"`、`"http"` 或 `"agent"`
* `hook_source`：hook 的定義位置：`"userSettings"`、`"projectSettings"`、`"localSettings"`、`"flagSettings"`、`"policySettings"` 或 `"pluginHook"`
* `hook_matcher`（當 `OTEL_LOG_TOOL_DETAILS=1` 時）：hook 配置中的匹配器字串（如果已設定）
* `plugin.name`（當 `hook_source` 是 `"pluginHook"` 時）：貢獻 plugin 的名稱。對於官方市場和內建捆綁之外的 plugin，除非 `OTEL_LOG_TOOL_DETAILS=1`，否則值為 `"third-party"`
* `plugin_id_hash`（當 `hook_source` 是 `"pluginHook"` 時）：plugin 名稱和市場的確定性雜湊，僅傳送到您配置的匯出器。讓您計算不同的貢獻 plugin，而無需記錄其名稱

#### Hook 執行開始事件

當一個或多個 hook 開始為 hook 事件執行時記錄。

**事件名稱**：`claude_code.hook_execution_start`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"hook_execution_start"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `hook_event`：Hook 事件類型，例如 `"PreToolUse"` 或 `"PostToolUse"`
* `hook_name`：完整 hook 名稱，包括匹配器，例如 `"PreToolUse:Write"`
* `num_hooks`：匹配 hook 命令的數量
* `managed_only`：當僅允許受管原則 hook 時為 `"true"`
* `hook_source`：`"policySettings"` 或 `"merged"`
* `hook_definitions`：JSON 序列化的 hook 配置。僅當詳細 beta 追蹤和 `OTEL_LOG_TOOL_DETAILS=1` 都啟用時才包含

#### Hook 執行完成事件

當 hook 事件的所有 hook 完成時記錄。

**事件名稱**：`claude_code.hook_execution_complete`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"hook_execution_complete"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `hook_event`：Hook 事件類型
* `hook_name`：完整 hook 名稱，包括匹配器
* `num_hooks`：匹配 hook 命令的數量
* `num_success`：成功完成的計數
* `num_blocking`：傳回阻止決定的計數
* `num_non_blocking_error`：在不阻止的情況下失敗的計數
* `num_cancelled`：在完成前取消的計數
* `total_duration_ms`：所有匹配 hook 的牆上時間持續時間
* `managed_only`：當僅允許受管原則 hook 時為 `"true"`
* `hook_source`：`"policySettings"` 或 `"merged"`
* `hook_definitions`：JSON 序列化的 hook 配置。僅當詳細 beta 追蹤和 `OTEL_LOG_TOOL_DETAILS=1` 都啟用時才包含

#### Hook plugin 指標事件

當官方市場 plugin hook 發出每次叫用指標時記錄。僅從官方 Anthropic 市場安裝的 plugin 可以發出這些。第三方市場 plugin 和使用者配置的 hook 不會發出到此事件。使用此事件從您自己的可觀測性堆疊監控 plugin 行為，例如尋找速率、成本和持續時間。

**事件名稱**：`claude_code.hook_plugin_metrics`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"hook_plugin_metrics"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `plugin_id`：plugin 識別碼，格式為 `<name>@<marketplace>`
* `hook_event`：發出指標的 hook 事件類型
* 最多 20 個 plugin 發出的指標鍵。名稱符合 `^[a-z][a-z0-9_]{0,39}$`。值為布林值或數字。

#### 壓縮事件

當對話壓縮完成時記錄。

**事件名稱**：`claude_code.compaction`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"compaction"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `trigger`：`"auto"` 或 `"manual"`
* `success`：`"true"` 或 `"false"`
* `duration_ms`：壓縮持續時間
* `pre_tokens`：壓縮前的近似權杖計數
* `post_tokens`：壓縮後的近似權杖計數
* `error`：壓縮失敗時的錯誤訊息

#### 回饋調查事件

當顯示或回答工作階段品質調查時記錄。詳見[工作階段品質調查](/zh-TW/data-usage#session-quality-surveys)以了解調查收集的內容以及如何控制它們。

**事件名稱**：`claude_code.feedback_survey`

**屬性**：

* 所有[標準屬性](#standard-attributes)
* `event.name`：`"feedback_survey"`
* `event.timestamp`：ISO 8601 時間戳
* `event.sequence`：單調遞增計數器，用於排序工作階段內的事件
* `event_type`：調查生命週期事件，例如 `"appeared"`、`"responded"` 或 `"transcript_prompt_appeared"`
* `appearance_id`：唯一 ID，連結為一個調查實例發出的事件
* `survey_type`：哪個調查產生了事件。`"session"` 是「Claude 表現如何？」評分提示
* `response`：使用者在 `responded` 事件上的選擇
* `enabled_via_override`：當設定 [`CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL`](/zh-TW/env-vars) 時為 `true`。作為布林值而非字串發出。存在於 `session` 調查事件上。篩選此屬性以確認覆蓋在整個環境中應用

## 解釋指標和事件資料

匯出的指標和事件支援一系列分析：

### 使用情況監控

| 指標                                                            | 分析機會                                                                     |
| ------------------------------------------------------------- | ------------------------------------------------------------------------ |
| `claude_code.token.usage`                                     | 按 `type`（輸入/輸出）、使用者、團隊、模型、`skill.name`、`plugin.name` 或 `agent.name` 進行細分 |
| `claude_code.session.count`                                   | 追蹤一段時間內的採用和參與度                                                           |
| `claude_code.lines_of_code.count`                             | 透過追蹤程式碼新增/移除來衡量生產力                                                       |
| `claude_code.commit.count` & `claude_code.pull_request.count` | 了解對開發工作流程的影響                                                             |

### 成本監控

`claude_code.cost.usage` 指標有助於：

* 追蹤跨團隊或個人的使用趨勢
* 識別高使用量工作階段以進行最佳化
* 透過 `skill.name`、`plugin.name` 和 `agent.name` 屬性將支出歸因於特定技能、外掛程式或子代理類型

<Note>
  成本指標是近似值。如需官方帳單資料，請參閱您的 API 提供者（Claude Console、Amazon Bedrock 或 Google Cloud Vertex）。
</Note>

### 警報和分段

要考慮的常見警報：

* 成本尖峰
* 異常的權杖消耗
* 來自特定使用者的高工作階段量

所有指標都可以按 `user.account_uuid`、`user.account_id`、`organization.id`、`session.id`、`model` 和 `app.version` 進行分段。

### 偵測重試耗盡

Claude Code 在內部重試失敗的 API 請求，並僅在放棄後才發出單個 `claude_code.api_error` 事件，因此事件本身是該請求的終端訊號。中間重試嘗試不會作為單獨的事件記錄。

事件上的 `attempt` 屬性記錄進行的嘗試總次數。大於 `CLAUDE_CODE_MAX_RETRIES`（預設 `10`）的值表示請求在暫時性錯誤上耗盡了所有重試。較低的值表示不可重試的錯誤，例如 `400` 回應。

若要區分從一個恢復的工作階段與停滯的工作階段，請按 `session.id` 分組事件，並檢查錯誤後是否存在更晚的 `api_request` 事件。

### 事件分析

事件資料提供了對 Claude Code 互動的詳細見解：

**工具使用模式**：分析工具結果事件以識別：

* 最常使用的工具
* 工具成功率
* 平均工具執行時間
* 按工具類型的錯誤模式

**效能監控**：追蹤 API 請求持續時間和工具執行時間以識別效能瓶頸。

## 稽核安全事件

OpenTelemetry 事件是 Claude Code 活動的稽核資料來源。每個事件都帶有身份屬性，將工具呼叫、MCP 活動和權限決定與觸發它們的使用者相關聯，OTLP 日誌匯出器可以將這些事件傳遞到任何具有 OTLP 接收器的安全資訊和事件管理 (SIEM) 平台或轉發到您的 SIEM 的 OpenTelemetry Collector。

### 將屬性操作歸因於使用者

每個事件上的[標準屬性](#standard-attributes)包括已驗證使用者的身份：使用 Claude 帳戶登入時的 `user.email`、`user.account_uuid`、`user.account_id` 和 `organization.id`，加上安裝範圍的 `user.id` 和每個工作階段的 `session.id`。

MCP 工具呼叫、Bash 命令和檔案編輯因此歸因於啟動工作階段的開發人員。Claude Code 不在單獨的服務帳戶下運作；每個事件上記錄的身份是開發人員自己的 Claude 帳戶。

當 Claude Code 使用直接 API 金鑰進行身份驗證，或針對 Bedrock、Vertex AI 或 Microsoft Foundry 進行身份驗證時，工作階段中沒有 Claude 帳戶，僅填充 `user.id` 和 `session.id`。在這些部署中，使用 `OTEL_RESOURCE_ATTRIBUTES` 自行附加使用者身份，透過[受管設定](#administrator-configuration)檔案或啟動包裝器按使用者設定：

```bash theme={null}
export OTEL_RESOURCE_ATTRIBUTES="enduser.id=jdoe@example.com,enduser.directory_id=S-1-5-21-..."
```

### 稽核 MCP 活動

若要使用完整呼叫詳情捕捉 MCP 伺服器活動，請啟用日誌匯出器並設定 `OTEL_LOG_TOOL_DETAILS=1`。每個 MCP 操作然後產生結構化事件，其中包含伺服器名稱、工具名稱和呼叫引數以及標準身份屬性：

| 事件                      | 它為 MCP 記錄的內容                                                                                                                            |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `mcp_server_connection` | 伺服器連線、斷開連線和連線失敗，包含 `server_name`、`transport_type`、`server_scope` 和錯誤詳情                                                                  |
| `tool_result`           | 每個 MCP 工具呼叫，包含 `tool_name` 和 `mcp_server_scope`、包含 `mcp_server_name` 和 `mcp_tool_name` 的 `tool_parameters` 承載，以及包含呼叫引數的 `tool_input` 承載 |
| `tool_decision`         | 呼叫是否被允許或拒絕，以及決定是來自配置、hook 還是使用者                                                                                                         |

沒有 `OTEL_LOG_TOOL_DETAILS`，`tool_result` 事件仍然帶有 `tool_name` 和 `mcp_server_scope` 但省略 `mcp_server_name`/`mcp_tool_name` 細分和引數，`mcp_server_connection` 事件省略 `server_name` 和錯誤訊息。

### 將安全問題對應到事件

建立偵測規則時，查詢您想要監控的訊號並查詢您的後端以取得相應的事件和屬性：

| 訊號               | 事件                                           | 關鍵屬性                                                       |
| ---------------- | -------------------------------------------- | ---------------------------------------------------------- |
| 工具呼叫被允許或拒絕，以及由什麼 | `tool_decision`                              | `decision`、`source`、`tool_name`                            |
| 權限模式升級           | `permission_mode_changed`                    | `from_mode`、`to_mode`、`trigger`                            |
| 原則 hook 阻止了操作    | `hook_execution_complete`                    | `hook_event`、`num_blocking`                                |
| 登入、登出和身份驗證失敗     | `auth`                                       | `action`、`success`、`error_category`                        |
| MCP 伺服器連線或失敗     | `mcp_server_connection`                      | `status`、`server_name`、`error_code`                        |
| Plugin 已安裝及其來源   | `plugin_installed`                           | `plugin.name`、`marketplace.name`、`marketplace.is_official` |
| 執行的命令和觸及的檔案      | `tool_result` with `OTEL_LOG_TOOL_DETAILS=1` | `tool_parameters`、`tool_input`                             |

Claude Code 僅發出原始事件流。異常偵測、基線設定、跨工作階段關聯和警報是您的 SIEM 或可觀測性後端的責任。

### 將事件傳送到 SIEM

將 `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT` 指向您的 SIEM 的 OTLP 接收器，或指向轉發到您的 SIEM 的原生擷取 API 的 OpenTelemetry Collector。以下受管設定範例僅匯出事件，並啟用完整工具詳情以進行 MCP 和 Bash 稽核：

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_LOG_TOOL_DETAILS": "1",
    "OTEL_EXPORTER_OTLP_LOGS_PROTOCOL": "http/protobuf",
    "OTEL_EXPORTER_OTLP_LOGS_ENDPOINT": "https://siem.example.com:4318/v1/logs",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer your-siem-token"
  }
}
```

## 後端考量

您選擇的指標、日誌和追蹤後端決定了您可以執行的分析類型：

### 對於指標

* **時間序列資料庫（例如，Prometheus）**：速率計算、聚合指標
* **欄式存儲（例如，ClickHouse）**：複雜查詢、唯一使用者分析
* **功能完整的可觀測性平台（例如，Honeycomb、Datadog）**：進階查詢、視覺化、警報

### 對於事件/日誌

* **日誌聚合系統（例如，Elasticsearch、Loki）**：全文搜尋、日誌分析
* **欄式存儲（例如，ClickHouse）**：結構化事件分析
* **功能完整的可觀測性平台（例如，Honeycomb、Datadog）**：指標和事件之間的關聯

### 對於追蹤

選擇支援分散式追蹤儲存和跨度關聯的後端：

* **分散式追蹤系統（例如，Jaeger、Zipkin、Grafana Tempo）**：跨度視覺化、請求瀑布圖、延遲分析
* **功能完整的可觀測性平台（例如，Honeycomb、Datadog）**：追蹤搜尋和與指標和日誌的關聯

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

## 安全性和隱私

* OpenTelemetry 匯出到您的後端是選擇加入的，需要明確配置。如需了解 Anthropic 的獨立營運遙測以及如何停用它，請參閱[資料使用](/zh-TW/data-usage#telemetry-services)
* 原始檔案內容和程式碼片段不包含在指標或事件中。追蹤跨度是單獨的資料路徑：請參閱下面的 `OTEL_LOG_TOOL_CONTENT` 項目
* 透過 OAuth 驗證時，`user.email` 包含在遙測屬性中。如果這對您的組織是個問題，請與您的遙測後端合作以篩選或編輯此欄位
* 預設不收集使用者提示內容。僅記錄提示長度。若要包含提示內容，請設定 `OTEL_LOG_USER_PROMPTS=1`
* 工具輸入引數和參數預設不記錄。若要包含它們，請設定 `OTEL_LOG_TOOL_DETAILS=1`。啟用時，`tool_result` 事件包含 `tool_parameters` 屬性，其中包含 Bash 命令、MCP 伺服器和工具名稱以及技能名稱，以及包含檔案路徑、URL、搜尋模式和其他引數的 `tool_input` 屬性。`user_prompt` 事件包含自訂、plugin 和 MCP 命令的逐字 `command_name`。追蹤跨度包含相同的 `tool_input` 屬性和輸入衍生屬性，例如 `file_path`。超過 512 個字元的個別值會被截斷，總計上限約為 4 K 字元，但引數仍可能包含敏感值。根據需要配置您的遙測後端以篩選或編輯這些屬性
* 工具輸入和輸出內容預設不在追蹤跨度中記錄。若要包含它，請設定 `OTEL_LOG_TOOL_CONTENT=1`。啟用時，跨度事件包含完整工具輸入和輸出內容，在每個跨度處截斷 60 KB。這可以包含來自 Read 工具結果的原始檔案內容和 Bash 命令輸出。根據需要配置您的遙測後端以篩選或編輯這些屬性
* 原始 Anthropic Messages API 請求和回應主體預設不記錄。若要包含它們，請設定 `OTEL_LOG_RAW_API_BODIES`。使用 `=1` 時，每個 API 呼叫發出 `api_request_body` 和 `api_response_body` 日誌事件，其 `body` 屬性是 JSON 序列化的承載，在 60 KB 處截斷。使用 `=file:<dir>` 時，未截斷的主體寫入該目錄下的 `.request.json` 和 `.response.json` 檔案，事件帶有 `body_ref` 路徑而不是內聯主體。使用日誌收集器或邊車傳送目錄，而不是透過遙測流。在兩種模式中，主體包含完整的對話歷史記錄（系統提示、每個先前的使用者和助手輪次、工具結果），因此啟用此選項意味著同意其他 `OTEL_LOG_*` 內容旗標會揭露的所有內容。Claude 的擴展思考內容始終從這些主體中編輯，無論其他設定如何

## 在 Amazon Bedrock 上監控 Claude Code

如需 Amazon Bedrock 上 Claude Code 使用情況監控的詳細指南，請參閱 [Claude Code 監控實作 (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)。
