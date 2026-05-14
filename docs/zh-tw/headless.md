> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 以程式方式執行 Claude Code

> 使用 Agent SDK 從 CLI、Python 或 TypeScript 以程式方式執行 Claude Code。

<Note>
  Starting June 15, 2026, Agent SDK and `claude -p` usage on subscription plans will draw from a new monthly Agent SDK credit, separate from your interactive usage limits. See [Use the Claude Agent SDK with your Claude plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan) for details.
</Note>

[Agent SDK](/zh-TW/agent-sdk/overview) 提供與 Claude Code 相同的工具、agent 迴圈和上下文管理。它可作為 CLI 用於指令碼和 CI/CD，或作為 [Python](/zh-TW/agent-sdk/python) 和 [TypeScript](/zh-TW/agent-sdk/typescript) 套件供完整的程式控制。

若要以非互動模式執行 Claude Code，請傳遞 `-p` 和您的提示以及任何 [CLI 選項](/zh-TW/cli-reference)：

```bash theme={null}
claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"
```

本頁涵蓋透過 CLI (`claude -p`) 使用 Agent SDK。如需具有結構化輸出、工具核准回呼和原生訊息物件的 Python 和 TypeScript SDK 套件，請參閱 [完整 Agent SDK 文件](/zh-TW/agent-sdk/overview)。

## 基本用法

將 `-p`（或 `--print`）旗標新增至任何 `claude` 命令以非互動方式執行它。所有 [CLI 選項](/zh-TW/cli-reference) 都適用於 `-p`，包括：

* `--continue` 用於 [繼續對話](#continue-conversations)
* `--allowedTools` 用於 [自動核准工具](#auto-approve-tools)
* `--output-format` 用於 [結構化輸出](#get-structured-output)

此範例詢問 Claude 關於您的程式碼庫的問題並列印回應：

```bash theme={null}
claude -p "What does the auth module do?"
```

### 使用裸機模式加快速度

新增 `--bare` 以跳過 hooks、skills、plugins、MCP 伺服器、自動記憶體和 CLAUDE.md 的自動探索來減少啟動時間。沒有它，`claude -p` 會載入互動式工作階段會載入的相同 [上下文](/zh-TW/how-claude-code-works#the-context-window)，包括在工作目錄或 `~/.claude` 中設定的任何內容。

裸機模式對於 CI 和指令碼很有用，您需要在每台機器上獲得相同的結果。隊友 `~/.claude` 中的 hook 或專案的 `.mcp.json` 中的 MCP 伺服器不會執行，因為裸機模式永遠不會讀取它們。只有您明確傳遞的旗標才會生效。

此範例在裸機模式下執行一次性摘要任務，並預先核准 Read 工具，以便呼叫完成而無需許可提示：

```bash theme={null}
claude --bare -p "Summarize this file" --allowedTools "Read"
```

在裸機模式下，Claude 可以存取 Bash、檔案讀取和檔案編輯工具。使用旗標傳遞您需要的任何上下文：

| 要載入       | 使用                                                      |
| --------- | ------------------------------------------------------- |
| 系統提示新增    | `--append-system-prompt`, `--append-system-prompt-file` |
| 設定        | `--settings <file-or-json>`                             |
| MCP 伺服器   | `--mcp-config <file-or-json>`                           |
| 自訂 agents | `--agents <json>`                                       |
| 外掛程式      | `--plugin-dir <path>`, `--plugin-url <url>`             |

裸機模式跳過 OAuth 和鑰匙圈讀取。Anthropic 驗證必須來自 `ANTHROPIC_API_KEY` 或傳遞給 `--settings` 的 JSON 中的 `apiKeyHelper`。Bedrock、Vertex 和 Foundry 使用其通常的提供者認證。

<Note>
  `--bare` 是指令碼和 SDK 呼叫的建議模式，將在未來版本中成為 `-p` 的預設值。
</Note>

## 範例

這些範例突出顯示常見的 CLI 模式。對於 CI 和其他指令碼呼叫，新增 [`--bare`](#start-faster-with-bare-mode) 以便它們不會選擇本地設定的任何內容。

### 透過 Claude 管道傳送資料

非互動模式讀取 stdin，因此您可以像任何其他命令列工具一樣管道傳送資料並重新導向回應。

此範例將建置日誌管道傳送至 Claude 並將說明寫入檔案：

```bash theme={null}
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

使用 `--output-format json`，回應承載包括 `total_cost_usd` 和每個模型的成本明細，因此指令碼呼叫者可以追蹤每次叫用的支出，而無需查詢 [使用儀表板](/zh-TW/costs)。

<Note>
  自 Claude Code v2.1.128 起，管道傳送的 stdin 上限為 10MB。如果超過上限，Claude Code 會以清晰的錯誤和非零狀態代碼退出。若要處理更大的輸入，請將內容寫入檔案，並在提示中參考檔案路徑，而不是管道傳送它。
</Note>

### 將 Claude 新增至建置指令碼

您可以在指令碼中包裝非互動呼叫，以將 Claude 用作專案特定的 linter 或審查者。

此 `package.json` 指令碼將針對 `main` 的差異管道傳送至 Claude，並要求它報告拼寫錯誤。管道傳送差異意味著 Claude 不需要 Bash 權限來讀取它，而逸出的雙引號使指令碼可移植到 Windows：

```json theme={null}
{
  "scripts": {
    "lint:claude": "git diff main | claude -p \"you are a typo linter. for each typo in this diff, report filename:line on one line and the issue on the next. return nothing else.\""
  }
}
```

### 取得結構化輸出

使用 `--output-format` 控制回應的傳回方式：

* `text`（預設）：純文字輸出
* `json`：包含結果、工作階段 ID 和中繼資料的結構化 JSON
* `stream-json`：用於即時串流的換行分隔 JSON

此範例以 JSON 格式傳回專案摘要及工作階段中繼資料，文字結果在 `result` 欄位中：

```bash theme={null}
claude -p "Summarize this project" --output-format json
```

若要取得符合特定結構描述的輸出，請使用 `--output-format json` 搭配 `--json-schema` 和 [JSON Schema](https://json-schema.org/) 定義。回應包含關於請求的中繼資料（工作階段 ID、使用情況等），結構化輸出在 `structured_output` 欄位中。

此範例從 auth.py 提取函式名稱並將其作為字串陣列傳回：

```bash theme={null}
claude -p "Extract the main function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

<Tip>
  使用 [jq](https://jqlang.github.io/jq/) 之類的工具來解析回應並提取特定欄位：

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

### 串流回應

使用 `--output-format stream-json` 搭配 `--verbose` 和 `--include-partial-messages` 以在產生令牌時接收它們。每一行都是代表事件的 JSON 物件：

```bash theme={null}
claude -p "Explain recursion" --output-format stream-json --verbose --include-partial-messages
```

下列範例使用 [jq](https://jqlang.github.io/jq/) 篩選文字差異並僅顯示串流文字。`-r` 旗標輸出原始字串（無引號），`-j` 不帶換行符號的聯結，因此令牌會連續串流：

```bash theme={null}
claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

當 API 請求因可重試錯誤而失敗時，Claude Code 會在重試前發出 `system/api_retry` 事件。您可以使用此來顯示重試進度或實施自訂退避邏輯。

| 欄位               | 類型            | 描述                                                                                                                                                 |
| ---------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`           | `"system"`    | 訊息類型                                                                                                                                               |
| `subtype`        | `"api_retry"` | 將此識別為重試事件                                                                                                                                          |
| `attempt`        | 整數            | 目前嘗試次數，從 1 開始                                                                                                                                      |
| `max_retries`    | 整數            | 允許的總重試次數                                                                                                                                           |
| `retry_delay_ms` | 整數            | 毫秒直到下一次嘗試                                                                                                                                          |
| `error_status`   | 整數或 null      | HTTP 狀態碼，或 `null` 表示沒有 HTTP 回應的連線錯誤                                                                                                                |
| `error`          | 字串            | 錯誤類別：`authentication_failed`、`oauth_org_not_allowed`、`billing_error`、`rate_limit`、`invalid_request`、`server_error`、`max_output_tokens` 或 `unknown` |
| `uuid`           | 字串            | 唯一事件識別碼                                                                                                                                            |
| `session_id`     | 字串            | 事件所屬的工作階段                                                                                                                                          |

`system/init` 事件報告工作階段中繼資料，包括模型、工具、MCP 伺服器和載入的外掛程式。除非設定了 [`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`](/zh-TW/env-vars)，否則它是串流中的第一個事件，在這種情況下 `plugin_install` 事件在其之前。使用外掛程式欄位在外掛程式未載入時使 CI 失敗：

| 欄位              | 類型 | 描述                                                                                                                                  |
| --------------- | -- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `plugins`       | 陣列 | 成功載入的外掛程式，每個都有 `name` 和 `path`                                                                                                      |
| `plugin_errors` | 陣列 | 外掛程式載入時間錯誤，每個都有 `plugin`、`type` 和 `message`。包括不滿足的相依性版本和 `--plugin-dir` 載入失敗，例如遺失的路徑或無效的封存。受影響的外掛程式被降級並從 `plugins` 中缺失。當沒有錯誤時，金鑰被省略 |

當設定了 [`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`](/zh-TW/env-vars) 時，Claude Code 在第一次轉換前發出 `system/plugin_install` 事件，同時市場外掛程式安裝。使用這些在您自己的 UI 中顯示安裝進度。

| 欄位           | 類型                                                   | 描述                                                           |
| ------------ | ---------------------------------------------------- | ------------------------------------------------------------ |
| `type`       | `"system"`                                           | 訊息類型                                                         |
| `subtype`    | `"plugin_install"`                                   | 將此識別為外掛程式安裝事件                                                |
| `status`     | `"started"`、`"installed"`、`"failed"` 或 `"completed"` | `started` 和 `completed` 括住整體安裝；`installed` 和 `failed` 報告個別市場 |
| `name`       | 字串，選用                                                | 市場名稱，在 `installed` 和 `failed` 上出現                            |
| `error`      | 字串，選用                                                | 失敗訊息，在 `failed` 上出現                                          |
| `uuid`       | 字串                                                   | 唯一事件識別碼                                                      |
| `session_id` | 字串                                                   | 事件所屬的工作階段                                                    |

如需具有回呼和訊息物件的程式化串流，請參閱 Agent SDK 文件中的 [即時串流回應](/zh-TW/agent-sdk/streaming-output)。

### 自動核准工具

使用 `--allowedTools` 讓 Claude 使用某些工具而無需提示。此範例執行測試套件並修復失敗，允許 Claude 執行 Bash 命令和讀取/編輯檔案而無需請求許可：

```bash theme={null}
claude -p "Run the test suite and fix any failures" \
  --allowedTools "Bash,Read,Edit"
```

若要為整個工作階段設定基準而不是列出個別工具，請傳遞 [權限模式](/zh-TW/permission-modes)。`dontAsk` 拒絕 `permissions.allow` 規則或 [唯讀命令集](/zh-TW/permissions#read-only-commands) 中未包含的任何內容，這對於鎖定的 CI 執行很有用。`acceptEdits` 讓 Claude 寫入檔案而無需提示，也自動核准常見的檔案系統命令，例如 `mkdir`、`touch`、`mv` 和 `cp`。其他 shell 命令和網路請求仍然需要 `--allowedTools` 項目或 `permissions.allow` 規則，否則當嘗試執行時執行會中止：

```bash theme={null}
claude -p "Apply the lint fixes" --permission-mode acceptEdits
```

### 建立提交

此範例檢查暫存的變更並建立具有適當訊息的提交：

```bash theme={null}
claude -p "Look at my staged changes and create an appropriate commit" \
  --allowedTools "Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git commit *)"
```

`--allowedTools` 旗標使用 [權限規則語法](/zh-TW/settings#permission-rule-syntax)。尾部的 ` *` 啟用前綴匹配，因此 `Bash(git diff *)` 允許任何以 `git diff` 開頭的命令。空格在 `*` 之前很重要：沒有它，`Bash(git diff*)` 也會符合 `git diff-index`。

<Note>
  使用者叫用的 [skills](/zh-TW/skills) 如 `/commit` 和 [內建命令](/zh-TW/commands) 僅在互動模式中可用。在 `-p` 模式中，改為描述您想要完成的任務。
</Note>

### 自訂系統提示

使用 `--append-system-prompt` 新增指示同時保持 Claude Code 的預設行為。此範例將 PR 差異管道傳送至 Claude 並指示它檢查安全漏洞：

```bash theme={null}
gh pr diff "$1" | claude -p \
  --append-system-prompt "You are a security engineer. Review for vulnerabilities." \
  --output-format json
```

請參閱 [系統提示旗標](/zh-TW/cli-reference#system-prompt-flags) 以取得更多選項，包括 `--system-prompt` 以完全取代預設提示。

### 繼續對話

使用 `--continue` 繼續最近的對話，或使用 `--resume` 搭配工作階段 ID 以繼續特定對話。此範例執行檢查，然後傳送後續提示：

```bash theme={null}
# First request
claude -p "Review this codebase for performance issues"

# Continue the most recent conversation
claude -p "Now focus on the database queries" --continue
claude -p "Generate a summary of all issues found" --continue
```

如果您執行多個對話，請擷取工作階段 ID 以繼續特定對話：

```bash theme={null}
session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')
claude -p "Continue that review" --resume "$session_id"
```

## 後續步驟

* [Agent SDK 快速入門](/zh-TW/agent-sdk/quickstart)：使用 Python 或 TypeScript 建立您的第一個 agent
* [CLI 參考](/zh-TW/cli-reference)：所有 CLI 旗標和選項
* [GitHub Actions](/zh-TW/github-actions)：在 GitHub 工作流程中使用 Agent SDK
* [GitLab CI/CD](/zh-TW/gitlab-ci-cd)：在 GitLab 管道中使用 Agent SDK
