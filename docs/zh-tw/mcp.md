> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 透過 MCP 將 Claude Code 連接到工具

> 了解如何使用 Model Context Protocol 將 Claude Code 連接到您的工具。

Claude Code 可以透過 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) 連接到數百個外部工具和資料來源，這是一個開源標準，用於 AI 工具整合。MCP servers 讓 Claude Code 能夠存取您的工具、資料庫和 API。

當您發現自己從另一個工具（例如問題追蹤器或監控儀表板）複製資料到聊天中時，請連接一個 server。連接後，Claude 可以直接讀取和操作該系統，而不是根據您貼上的內容進行工作。

## 使用 MCP 可以做什麼

連接 MCP servers 後，您可以要求 Claude Code：

* **從問題追蹤器實現功能**："新增 JIRA 問題 ENG-4521 中描述的功能，並在 GitHub 上建立 PR。"
* **分析監控資料**："檢查 Sentry 和 Statsig，以檢查 ENG-4521 中描述的功能使用情況。"
* **查詢資料庫**："根據我們的 PostgreSQL 資料庫，找到 10 個使用功能 ENG-4521 的隨機使用者的電子郵件。"
* **整合設計**："根據在 Slack 中發佈的新 Figma 設計更新我們的標準電子郵件範本"
* **自動化工作流程**："建立 Gmail 草稿，邀請這 10 個使用者參加關於新功能的回饋會議。"
* **回應外部事件**：MCP server 也可以充當 [channel](/zh-TW/channels)，將訊息推送到您的 session 中，因此當您不在時，Claude 可以回應 Telegram 訊息、Discord 聊天或 webhook 事件。

## 尋找並建立 MCP servers

在 [Anthropic Directory](https://claude.ai/directory) 中瀏覽已審核的連接器。Directory 連接器使用與 Claude Code 相同的 MCP 基礎設施，因此您可以使用 `claude mcp add` 新增任何列在其中的遠端伺服器。

<Warning>
  在連接伺服器之前，請驗證您信任每個伺服器。取得外部內容的伺服器可能會使您面臨[提示注入風險](/zh-TW/security#protect-against-prompt-injection)。
</Warning>

若要建立您自己的伺服器，請參閱 [MCP server 指南](https://modelcontextprotocol.io/docs/develop/build-server) 以了解協議基礎知識，以及 [Claude 連接器建立文件](https://claude.com/docs/connectors/building) 以了解身份驗證、測試和 Directory 提交。

您也可以使用官方的 [`mcp-server-dev` plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/mcp-server-dev) 讓 Claude 為您建立伺服器。

<Steps>
  <Step title="安裝 plugin">
    在 Claude Code 工作階段中，執行：

    ```
    /plugin install mcp-server-dev@claude-plugins-official
    ```

    然後執行 `/reload-plugins` 以在目前工作階段中啟用它。
  </Step>

  <Step title="執行建立 skill">
    ```
    /mcp-server-dev:build-mcp-server
    ```

    Claude 會詢問您的使用案例，並建立遠端 HTTP 或本機 stdio 伺服器。
  </Step>
</Steps>

## 安裝 MCP servers

MCP servers 可以根據您的需求以三種不同的方式進行配置：

### 選項 1：新增遠端 HTTP server

HTTP servers 是連接到遠端 MCP servers 的推薦選項。這是雲端服務最廣泛支援的傳輸方式。

```bash theme={null}
# 基本語法
claude mcp add --transport http <name> <url>

# 實際範例：連接到 Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# 使用 Bearer token 的範例
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

當透過 `.mcp.json`、`~/.claude.json` 或 `claude mcp add-json` 中的 JSON 配置 MCP servers 時，`type` 欄位接受 `streamable-http` 作為 `http` 的別名。MCP 規範使用名稱 `streamable-http` 作為此傳輸，因此從 server 文件複製的配置無需修改即可運作。

### 選項 2：新增遠端 SSE server

<Warning>
  SSE (Server-Sent Events) 傳輸已棄用。請改用 HTTP servers（如果可用）。
</Warning>

```bash theme={null}
# 基本語法
claude mcp add --transport sse <name> <url>

# 實際範例：連接到 Asana
claude mcp add --transport sse asana https://mcp.asana.com/sse

# 使用驗證標頭的範例
claude mcp add --transport sse private-api https://api.company.com/sse \
  --header "X-API-Key: your-key-here"
```

### 選項 3：新增本機 stdio server

Stdio servers 在您的機器上作為本機程序執行。它們非常適合需要直接系統存取或自訂指令碼的工具。

Claude Code 在生成的 server 環境中設定 `CLAUDE_PROJECT_DIR`，以指向專案根目錄，因此您的 server 可以解析專案相對路徑，而無需依賴工作目錄。這與 hooks 在其 `CLAUDE_PROJECT_DIR` 變數中接收的目錄相同。從您的 server 程序內部讀取它，例如 Node 中的 `process.env.CLAUDE_PROJECT_DIR` 或 Python 中的 `os.environ["CLAUDE_PROJECT_DIR"]`。您的 server 也可以呼叫 MCP `roots/list` 請求，該請求會傳回啟動 Claude Code 的目錄。

此變數在 server 的環境中設定，而不是在 Claude Code 自己的環境中，因此在專案或使用者範圍的 `.mcp.json` `command` 或 `args` 中透過 `${VAR}` 擴展參考它需要預設值，例如 `${CLAUDE_PROJECT_DIR:-.}`。Plugin 提供的 MCP 配置直接替換 `${CLAUDE_PROJECT_DIR}`，不需要預設值。

```bash theme={null}
# 基本語法
claude mcp add [options] <name> -- <command> [args...]

# 實際範例：新增 Airtable server
claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \
  -- npx -y airtable-mcp-server
```

<Note>
  **重要：選項順序**

  所有選項（`--transport`、`--env`、`--scope`、`--header`）必須在 server 名稱**之前**。然後 `--` (雙破折號) 將 server 名稱與傳遞給 MCP server 的命令和引數分開。

  例如：

  * `claude mcp add --transport stdio myserver -- npx server` → 執行 `npx server`
  * `claude mcp add --transport stdio --env KEY=value myserver -- python server.py --port 8080` → 執行 `python server.py --port 8080`，環境中有 `KEY=value`

  這可以防止 Claude 的旗標與 server 旗標之間的衝突。
</Note>

### 管理您的 servers

配置後，您可以使用這些命令管理您的 MCP servers：

```bash theme={null}
# 列出所有已配置的 servers
claude mcp list

# 取得特定 server 的詳細資訊
claude mcp get github

# 移除 server
claude mcp remove github

# (在 Claude Code 中) 檢查 server 狀態
/mcp
```

`/mcp` 面板會在每個已連接的 server 旁邊顯示工具計數，並標記宣告工具功能但未公開任何工具的 servers。

如果您的請求需要來自仍在背景連接的 server 的工具，Claude 會在繼續之前等待該 server。啟用 [tool search](#scale-with-mcp-tool-search)（預設啟用）後，等待會在 `ToolSearch` 呼叫內進行。在沒有工具搜尋的配置中，例如 Vertex AI、自訂 `ANTHROPIC_BASE_URL` 或 `ENABLE_TOOL_SEARCH=false`，Claude 會改用 `WaitForMcpServers` 工具。

server 名稱 `workspace` 保留供內部使用。如果您的配置定義了具有該名稱的 server，Claude Code 會在載入時跳過它，並顯示警告要求您重新命名它。

### 動態工具更新

Claude Code 支援 MCP `list_changed` 通知，允許 MCP servers 動態更新其可用工具、提示和資源，而無需您斷開連接並重新連接。當 MCP server 傳送 `list_changed` 通知時，Claude Code 會自動重新整理該 server 的可用功能。

### 自動重新連接

如果 HTTP 或 SSE server 在 session 中途斷開連接，Claude Code 會自動以指數退避方式重新連接：最多五次嘗試，從一秒延遲開始，每次加倍。在 `/mcp` 中，server 會顯示為待處理狀態，同時重新連接正在進行中。五次失敗嘗試後，server 被標記為失敗，您可以從 `/mcp` 手動重試。Stdio servers 是本機程序，不會自動重新連接。

相同的退避策略適用於 HTTP 或 SSE server 在啟動時初始連接失敗的情況。自 v2.1.121 起，Claude Code 在暫時性錯誤（例如 5xx 回應、連接被拒絕或逾時）上最多重試初始連接三次，如果仍無法連接，則將 server 標記為失敗。驗證和找不到錯誤不會重試，因為它們需要配置變更才能解決。

### 使用 channels 推送訊息

MCP server 也可以直接將訊息推送到您的 session 中，以便 Claude 可以回應外部事件，例如 CI 結果、監控警報或聊天訊息。若要啟用此功能，您的 server 宣告 `claude/channel` 功能，並在啟動時使用 `--channels` 旗標選擇加入。請參閱 [Channels](/zh-TW/channels) 以使用官方支援的 channel，或 [Channels reference](/zh-TW/channels-reference) 以建立您自己的。

<Tip>
  提示：

  * 使用 `--scope` 旗標指定配置的儲存位置：
    * `local` (預設)：僅在目前專案中對您可用 (在較舊版本中稱為 `project`)
    * `project`：透過 `.mcp.json` 檔案與專案中的所有人共享
    * `user`：在所有專案中對您可用 (在較舊版本中稱為 `global`)
  * 使用 `--env` 旗標設定環境變數 (例如，`--env KEY=value`)
  * 使用 MCP\_TIMEOUT 環境變數配置 MCP server 啟動逾時 (例如，`MCP_TIMEOUT=10000 claude` 設定 10 秒逾時)
  * 透過在該 server 的 `.mcp.json` 項目中新增 `timeout` 欄位（以毫秒為單位）來設定每個 server 的工具執行逾時，例如 `"timeout": 600000` 表示十分鐘。這只會覆寫該 server 的 `MCP_TOOL_TIMEOUT` 環境變數
  * 當 MCP 工具輸出超過 10,000 個 tokens 時，Claude Code 會顯示警告。若要增加此限制，請設定 `MAX_MCP_OUTPUT_TOKENS` 環境變數 (例如，`MAX_MCP_OUTPUT_TOKENS=50000`)
  * 使用 `/mcp` 向需要 OAuth 2.0 驗證的遠端 servers 進行驗證
</Tip>

每個 server 的 `timeout` 是每個工具呼叫的硬牆鐘限制，來自 server 的進度通知不會延長它。低於 1000 的值會被調整為一秒。對於 HTTP 和 SSE servers，每個請求的 fetch 首位元組預算無論此值如何都有 60 秒的最小值，因此只有工具呼叫看門狗會遵守較小的值。

### Plugin 提供的 MCP servers

[Plugins](/zh-TW/plugins) 可以捆綁 MCP servers，在啟用 plugin 時自動提供工具和整合。Plugin MCP servers 的工作方式與使用者配置的 servers 相同。

**Plugin MCP servers 的工作方式**：

* Plugins 在 plugin 根目錄的 `.mcp.json` 中或在 `plugin.json` 中內聯定義 MCP servers
* 啟用 plugin 時，其 MCP servers 會自動啟動
* Plugin MCP 工具與手動配置的 MCP 工具一起出現
* Plugin servers 透過 plugin 安裝進行管理 (不是 `/mcp` 命令)

**Plugin MCP 配置範例**：

在 plugin 根目錄的 `.mcp.json` 中：

```json theme={null}
{
  "mcpServers": {
    "database-tools": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_URL": "${DB_URL}"
      }
    }
  }
}
```

或在 `plugin.json` 中內聯：

```json theme={null}
{
  "name": "my-plugin",
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}
```

**Plugin MCP 功能**：

* **自動生命週期**：在 session 啟動時，已啟用 plugins 的 servers 會自動連接。如果您在 session 期間啟用或停用 plugin，請執行 `/reload-plugins` 以連接或斷開其 MCP servers
* **環境變數**：使用 `${CLAUDE_PLUGIN_ROOT}` 表示 plugin 根目錄中的捆綁 plugin 檔案，`${CLAUDE_PLUGIN_DATA}` 表示 [persistent state](/zh-TW/plugins-reference#persistent-data-directory) 在 plugin 更新後仍然存在，以及 `${CLAUDE_PROJECT_DIR}` 表示穩定的專案根目錄
* **使用者環境存取**：存取與手動配置的 servers 相同的環境變數
* **多種傳輸類型**：支援 stdio、SSE 和 HTTP 傳輸 (傳輸支援可能因 server 而異)

**檢視 plugin MCP servers**：

```bash theme={null}
# 在 Claude Code 中，查看所有 MCP servers，包括 plugin 的
/mcp
```

Plugin servers 在列表中出現，並有指示器顯示它們來自 plugins。

**Plugin MCP servers 的優點**：

* **捆綁分發**：工具和 servers 一起打包
* **自動設定**：無需手動 MCP 配置
* **團隊一致性**：安裝 plugin 時，每個人都會獲得相同的工具

請參閱 [plugin 元件參考](/zh-TW/plugins-reference#mcp-servers)，了解有關使用 plugins 捆綁 MCP servers 的詳細資訊。

## MCP 安裝範圍

MCP servers 可以在三個不同的範圍級別進行配置。您選擇的範圍控制 server 在哪些專案中載入，以及配置是否與您的團隊共享。管理員也可以透過[受管配置](#managed-mcp-configuration)在企業級別部署 servers。

| 範圍                        | 載入位置   | 與團隊共享    | 儲存位置                |
| ------------------------- | ------ | -------- | ------------------- |
| [Local](#local-scope)     | 僅目前專案  | 否        | `~/.claude.json`    |
| [Project](#project-scope) | 僅目前專案  | 是，透過版本控制 | 專案根目錄中的 `.mcp.json` |
| [User](#user-scope)       | 您的所有專案 | 否        | `~/.claude.json`    |

### Local scope

Local scope 是預設值。本機範圍的 server 僅在您新增它的專案中載入，並對您保持私密。Claude Code 將其儲存在 `~/.claude.json` 中該專案的路徑下，因此相同的 server 不會出現在您的其他專案中。使用本機範圍進行個人開發 servers、實驗配置或包含您不想在版本控制中的認證的 servers。

<Note>
  MCP servers 的「local scope」術語與一般本機設定不同。MCP 本機範圍的 servers 儲存在 `~/.claude.json` (您的主目錄) 中，而一般本機設定使用 `.claude/settings.local.json` (在專案目錄中)。請參閱 [Settings](/zh-TW/settings#settings-files) 了解設定檔案位置的詳細資訊。
</Note>

```bash theme={null}
# 新增本機範圍的 server (預設)
claude mcp add --transport http stripe https://mcp.stripe.com

# 明確指定本機範圍
claude mcp add --transport http stripe --scope local https://mcp.stripe.com
```

當您從 `/path/to/your/project` 執行命令時，該命令會將 server 寫入 `~/.claude.json` 中您目前專案的項目。下面的範例顯示結果：

```json theme={null}
{
  "projects": {
    "/path/to/your/project": {
      "mcpServers": {
        "stripe": {
          "type": "http",
          "url": "https://mcp.stripe.com"
        }
      }
    }
  }
}
```

### Project scope

Project scope 的 servers 透過在專案根目錄中儲存配置在 `.mcp.json` 檔案中來啟用團隊協作。此檔案設計為簽入版本控制，確保所有團隊成員都能存取相同的 MCP 工具和服務。新增 project scope 的 server 時，Claude Code 會自動建立或更新此檔案，使用適當的配置結構。

```bash theme={null}
# 新增 project scope 的 server
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp
```

產生的 `.mcp.json` 檔案遵循標準化格式：

```json theme={null}
{
  "mcpServers": {
    "shared-server": {
      "command": "/path/to/server",
      "args": [],
      "env": {}
    }
  }
}
```

出於安全考慮，Claude Code 在使用來自 `.mcp.json` 檔案的 project scope servers 之前會提示批准。如果您需要重設這些批准選擇，請使用 `claude mcp reset-project-choices` 命令。

### User scope

User scope 的 servers 儲存在 `~/.claude.json` 中，並提供跨專案可存取性，使其在您機器上的所有專案中可用，同時對您的使用者帳戶保持私密。此範圍非常適合個人公用程式 servers、開發工具或您在不同專案中經常使用的服務。

```bash theme={null}
# 新增使用者 server
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic
```

### Scope 階層和優先順序

當相同的 server 在多個位置定義時，Claude Code 連接到它一次，使用來自最高優先順序來源的定義：

1. Local scope
2. Project scope
3. User scope
4. [Plugin-provided servers](/zh-TW/plugins)
5. [claude.ai connectors](#use-mcp-servers-from-claude-ai)

三個範圍按名稱符合重複項。Plugins 和 connectors 按端點符合，因此指向與上述 server 相同 URL 或命令的端點被視為重複項。

### `.mcp.json` 中的環境變數擴展

Claude Code 支援 `.mcp.json` 檔案中的環境變數擴展，允許團隊共享配置，同時保持機器特定路徑和 API 金鑰等敏感值的靈活性。

**支援的語法：**

* `${VAR}` - 擴展為環境變數 `VAR` 的值
* `${VAR:-default}` - 如果設定了 `VAR`，則擴展為 `VAR`，否則使用 `default`

**擴展位置：**
環境變數可以在以下位置擴展：

* `command` - server 可執行檔路徑
* `args` - 命令列引數
* `env` - 傳遞給 server 的環境變數
* `url` - 對於 HTTP server 類型
* `headers` - 對於 HTTP server 驗證

**使用變數擴展的範例：**

```json theme={null}
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

如果未設定必需的環境變數且沒有預設值，Claude Code 將無法解析配置。

## 實用範例

{/* ### 範例：使用 Playwright 自動化瀏覽器測試

```bash
claude mcp add --transport stdio playwright -- npx -y @playwright/mcp@latest
```

然後編寫並執行瀏覽器測試：

```text
Test if the login flow works with test@example.com
```
```text
Take a screenshot of the checkout page on mobile
```
```text
Verify that the search feature returns results
``` */}

### 範例：使用 Sentry 監控錯誤

```bash theme={null}
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

使用您的 Sentry 帳戶進行驗證：

```text theme={null}
/mcp
```

然後除錯生產問題：

```text theme={null}
過去 24 小時內最常見的錯誤是什麼？
```

```text theme={null}
顯示錯誤 ID abc123 的堆疊追蹤
```

```text theme={null}
哪個部署引入了這些新錯誤？
```

### 範例：連接到 GitHub 進行程式碼審查

GitHub 的遠端 MCP server 使用作為標頭傳遞的 GitHub 個人存取 token 進行驗證。若要取得一個，請開啟您的 [GitHub token 設定](https://github.com/settings/personal-access-tokens)，產生一個新的細粒度 token，具有對您希望 Claude 使用的儲存庫的存取權，然後新增 server：

```bash theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
  --header "Authorization: Bearer YOUR_GITHUB_PAT"
```

然後使用 GitHub：

```text theme={null}
審查 PR #456 並建議改進
```

```text theme={null}
為我們剛發現的錯誤建立新問題
```

```text theme={null}
顯示所有指派給我的開放 PRs
```

### 範例：查詢您的 PostgreSQL 資料庫

```bash theme={null}
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:pass@prod.db.com:5432/analytics"
```

然後自然地查詢您的資料庫：

```text theme={null}
本月我們的總收入是多少？
```

```text theme={null}
顯示 orders 表的架構
```

```text theme={null}
找到 90 天內未進行購買的客戶
```

## 使用遠端 MCP servers 進行驗證

許多雲端 MCP servers 需要驗證。Claude Code 支援 OAuth 2.0 以進行安全連接。

Claude Code 會在 server 以 `401 Unauthorized` 或 `403 Forbidden` 回應時，將遠端 server 標記為需要驗證。任一狀態碼都會在 `/mcp` 中標記 server，以便您可以完成 OAuth 流程。傳回指向其授權 server 的 `WWW-Authenticate` 標頭的自訂 server 會獲得與任何其他遠端 server 相同的自動探索。

<Steps>
  <Step title="新增需要驗證的 server">
    例如：

    ```bash theme={null}
    claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
    ```
  </Step>

  <Step title="在 Claude Code 中使用 /mcp 命令">
    在 Claude Code 中，使用命令：

    ```text theme={null}
    /mcp
    ```

    然後按照瀏覽器中的步驟登入。
  </Step>
</Steps>

<Tip>
  提示：

  * 驗證 tokens 安全儲存並自動重新整理
  * 使用 `/mcp` 功能表中的「Clear authentication」撤銷存取權
  * 如果瀏覽器未自動開啟，請複製提供的 URL 並手動開啟
  * 如果瀏覽器重新導向在驗證後失敗並出現連接錯誤，請將瀏覽器位址列中的完整回呼 URL 貼到 Claude Code 中出現的 URL 提示中
  * OAuth 驗證適用於 HTTP servers
</Tip>

### 使用固定的 OAuth 回呼連接埠

某些 MCP servers 需要預先註冊的特定重新導向 URI。根據預設，Claude Code 為 OAuth 回呼選擇隨機可用連接埠。使用 `--callback-port` 固定連接埠，使其符合 `http://localhost:PORT/callback` 形式的預先註冊重新導向 URI。

您可以單獨使用 `--callback-port` (使用動態用戶端註冊) 或與 `--client-id` 一起使用 (使用預先配置的認證)。

```bash theme={null}
# 使用動態用戶端註冊的固定回呼連接埠
claude mcp add --transport http \
  --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

### 使用預先配置的 OAuth 認證

某些 MCP servers 不支援透過 Dynamic Client Registration 進行自動 OAuth 設定。如果您看到類似「Incompatible auth server: does not support dynamic client registration」的錯誤，server 需要預先配置的認證。Claude Code 也支援使用 Client ID Metadata Document (CIMD) 而不是 Dynamic Client Registration 的 servers，並自動探索這些。如果自動探索失敗，請先透過 server 的開發人員入口網站註冊 OAuth 應用程式，然後在新增 server 時提供認證。

<Steps>
  <Step title="使用 server 註冊 OAuth 應用程式">
    透過 server 的開發人員入口網站建立應用程式，並記下您的用戶端 ID 和用戶端密碼。

    許多 servers 也需要重新導向 URI。如果是這樣，請選擇一個連接埠並以 `http://localhost:PORT/callback` 的格式註冊重新導向 URI。在下一步中使用該相同連接埠搭配 `--callback-port`。
  </Step>

  <Step title="使用您的認證新增 server">
    選擇以下方法之一。用於 `--callback-port` 的連接埠可以是任何可用的連接埠。它只需要符合您在上一步中註冊的重新導向 URI。

    <Tabs>
      <Tab title="claude mcp add">
        使用 `--client-id` 傳遞您應用程式的用戶端 ID。`--client-secret` 旗標會提示輸入帶有遮罩輸入的密碼：

        ```bash theme={null}
        claude mcp add --transport http \
          --client-id your-client-id --client-secret --callback-port 8080 \
          my-server https://mcp.example.com/mcp
        ```
      </Tab>

      <Tab title="claude mcp add-json">
        在 JSON 配置中包含 `oauth` 物件，並將 `--client-secret` 作為單獨的旗標傳遞：

        ```bash theme={null}
        claude mcp add-json my-server \
          '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' \
          --client-secret
        ```
      </Tab>

      <Tab title="claude mcp add-json (僅回呼連接埠)">
        使用 `--callback-port` 而不使用用戶端 ID 來固定連接埠，同時使用動態用戶端註冊：

        ```bash theme={null}
        claude mcp add-json my-server \
          '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"callbackPort":8080}}'
        ```
      </Tab>

      <Tab title="CI / env var">
        透過環境變數設定密碼以跳過互動式提示：

        ```bash theme={null}
        MCP_CLIENT_SECRET=your-secret claude mcp add --transport http \
          --client-id your-client-id --client-secret --callback-port 8080 \
          my-server https://mcp.example.com/mcp
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="在 Claude Code 中進行驗證">
    在 Claude Code 中執行 `/mcp` 並按照瀏覽器登入流程。
  </Step>
</Steps>

<Tip>
  提示：

  * 用戶端密碼安全地儲存在您的系統鑰匙圈 (macOS) 或認證檔案中，而不是在您的配置中
  * 如果 server 使用沒有密碼的公開 OAuth 用戶端，請僅使用 `--client-id` 而不使用 `--client-secret`
  * `--callback-port` 可以與或不與 `--client-id` 一起使用
  * 這些旗標僅適用於 HTTP 和 SSE 傳輸。它們對 stdio servers 沒有影響
  * 使用 `claude mcp get <name>` 驗證為 server 配置了 OAuth 認證
</Tip>

### 覆蓋 OAuth 中繼資料探索

指向 Claude Code 特定的 OAuth 授權 server 中繼資料 URL 以繞過預設探索鏈。當 MCP server 的標準端點出錯時，或當您想要透過內部代理路由探索時，設定 `authServerMetadataUrl`。根據預設，Claude Code 首先檢查 RFC 9728 Protected Resource Metadata at `/.well-known/oauth-protected-resource`，然後回退到 RFC 8414 authorization server metadata at `/.well-known/oauth-authorization-server`。

在 `.mcp.json` 中 server 配置的 `oauth` 物件中設定 `authServerMetadataUrl`：

```json theme={null}
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "authServerMetadataUrl": "https://auth.example.com/.well-known/openid-configuration"
      }
    }
  }
}
```

URL 必須使用 `https://`。`authServerMetadataUrl` 需要 Claude Code v2.1.64 或更新版本。中繼資料 URL 的 `scopes_supported` 會覆蓋上游 server 宣傳的範圍。

### 限制 OAuth 範圍

設定 `oauth.scopes` 以固定 Claude Code 在授權流程中要求的範圍。這是限制 MCP server 到安全團隊批准的子集的支援方式，當上游授權 server 宣傳的範圍超過您想要授予的範圍時。該值是單個空格分隔的字串，符合 RFC 6749 §3.3 中的 `scope` 參數格式。

```json theme={null}
{
  "mcpServers": {
    "slack": {
      "type": "http",
      "url": "https://mcp.slack.com/mcp",
      "oauth": {
        "scopes": "channels:read chat:write search:read"
      }
    }
  }
}
```

`oauth.scopes` 優先於 `authServerMetadataUrl` 和 server 在 `/.well-known` 發現的範圍。保持未設定以讓 MCP server 決定要求的範圍集。

如果授權 server 在 `scopes_supported` 中宣傳 `offline_access`，Claude Code 會將其附加到固定範圍，以便可以在沒有新瀏覽器登入的情況下重新整理存取 token。

如果 server 稍後為工具呼叫傳回 403 `insufficient_scope`，Claude Code 會使用相同的固定範圍重新驗證。當您需要的工具需要固定範圍外的範圍時，擴展 `oauth.scopes`。

### 使用動態標頭進行自訂驗證

如果您的 MCP server 使用 OAuth 以外的驗證方案 (例如 Kerberos、短期 tokens 或內部 SSO)，請使用 `headersHelper` 在連接時產生請求標頭。Claude Code 執行命令並將其輸出合併到連接標頭中。

```json theme={null}
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "/opt/bin/get-mcp-auth-headers.sh"
    }
  }
}
```

命令也可以內聯：

```json theme={null}
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "echo '{\"Authorization\": \"Bearer '\"$(get-token)\"'\"}'"
    }
  }
}
```

**需求：**

* 命令必須將字串鍵值對的 JSON 物件寫入 stdout
* 命令在 shell 中執行，逾時時間為 10 秒
* 動態標頭會覆蓋任何具有相同名稱的靜態 `headers`

helper 在每次連接時執行 (在 session 啟動和重新連接時)。沒有快取，因此您的指令碼負責任何 token 重複使用。

Claude Code 在執行 helper 時設定這些環境變數：

| 變數                            | 值                |
| :---------------------------- | :--------------- |
| `CLAUDE_CODE_MCP_SERVER_NAME` | MCP server 的名稱   |
| `CLAUDE_CODE_MCP_SERVER_URL`  | MCP server 的 URL |

使用這些來編寫為多個 MCP servers 服務的單一 helper 指令碼。

<Note>
  `headersHelper` 執行任意 shell 命令。在專案或本機範圍定義時，它僅在您接受工作區信任對話框後執行。
</Note>

## 從 JSON 配置新增 MCP servers

如果您有 MCP server 的 JSON 配置，您可以直接新增它：

<Steps>
  <Step title="從 JSON 新增 MCP server">
    ```bash theme={null}
    # 基本語法
    claude mcp add-json <name> '<json>'

    # 範例：使用 JSON 配置新增 HTTP server
    claude mcp add-json weather-api '{"type":"http","url":"https://api.weather.com/mcp","headers":{"Authorization":"Bearer token"}}'

    # 範例：使用 JSON 配置新增 stdio server
    claude mcp add-json local-weather '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"],"env":{"CACHE_DIR":"/tmp"}}'

    # 範例：使用預先配置的 OAuth 認證新增 HTTP server
    claude mcp add-json my-server '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' --client-secret
    ```
  </Step>

  <Step title="驗證 server 已新增">
    ```bash theme={null}
    claude mcp get weather-api
    ```
  </Step>
</Steps>

<Tip>
  提示：

  * 確保 JSON 在您的 shell 中正確逸出
  * JSON 必須符合 MCP server 配置架構
  * 您可以使用 `--scope user` 將 server 新增到您的使用者配置，而不是專案特定的配置
</Tip>

## 從 Claude Desktop 匯入 MCP servers

如果您已在 Claude Desktop 中配置了 MCP servers，您可以匯入它們：

<Steps>
  <Step title="從 Claude Desktop 匯入 servers">
    ```bash theme={null}
    # 基本語法 
    claude mcp add-from-claude-desktop 
    ```
  </Step>

  <Step title="選擇要匯入的 servers">
    執行命令後，您會看到一個互動式對話框，允許您選擇要匯入的 servers。
  </Step>

  <Step title="驗證 servers 已匯入">
    ```bash theme={null}
    claude mcp list 
    ```
  </Step>
</Steps>

<Tip>
  提示：

  * 此功能僅適用於 macOS 和 Windows Subsystem for Linux (WSL)
  * 它從這些平台上的標準位置讀取 Claude Desktop 配置檔案
  * 使用 `--scope user` 旗標將 servers 新增到您的使用者配置
  * 匯入的 servers 將具有與 Claude Desktop 中相同的名稱
  * 如果已存在相同名稱的 servers，它們將獲得數字尾碼 (例如，`server_1`)
</Tip>

## 使用來自 Claude.ai 的 MCP servers

如果您已使用 [Claude.ai](https://claude.ai) 帳戶登入 Claude Code，您在 Claude.ai 中新增的 MCP servers 會自動在 Claude Code 中可用：

<Steps>
  <Step title="在 Claude.ai 中配置 MCP servers">
    在 [claude.ai/customize/connectors](https://claude.ai/customize/connectors) 新增 servers。在 Team 和 Enterprise 計畫上，只有管理員可以新增 servers。
  </Step>

  <Step title="驗證 MCP server">
    在 Claude.ai 中完成任何必需的驗證步驟。
  </Step>

  <Step title="在 Claude Code 中檢視和管理 servers">
    在 Claude Code 中，使用命令：

    ```text theme={null}
    /mcp
    ```

    Claude.ai servers 在列表中出現，並有指示器顯示它們來自 Claude.ai。
  </Step>
</Steps>

Claude.ai connectors 只有在您的活躍[驗證方法](/zh-TW/authentication#authentication-precedence)是您的 Claude.ai 訂閱時才會被取得。當 `ANTHROPIC_API_KEY`、`ANTHROPIC_AUTH_TOKEN`、`apiKeyHelper` 或第三方提供者（例如 Bedrock 或 Vertex）處於活躍狀態時，它們不會被載入，即使您之前執行過 `/login`。如果 `/mcp` 沒有列出您新增的 connector，請執行 `/status` 以確認哪個驗證方法處於活躍狀態，取消設定該環境變數或移除 `apiKeyHelper` 設定，然後執行 `/login` 以選擇您的 Claude.ai 帳戶。

您在 Claude Code 中新增的 server 優先於指向相同 URL 的 claude.ai connector。發生這種情況時，`/mcp` 會將 connector 列為隱藏，並顯示如何移除重複項（如果您寧願使用 connector）。

若要在 Claude Code 中停用 claude.ai MCP servers，請將 `ENABLE_CLAUDEAI_MCP_SERVERS` 環境變數設定為 `false`：

```bash theme={null}
ENABLE_CLAUDEAI_MCP_SERVERS=false claude
```

## 使用 Claude Code 作為 MCP server

您可以使用 Claude Code 本身作為其他應用程式可以連接到的 MCP server：

```bash theme={null}
# 啟動 Claude 作為 stdio MCP server
claude mcp serve
```

您可以透過將此配置新增到 claude\_desktop\_config.json 在 Claude Desktop 中使用它：

```json theme={null}
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

<Warning>
  **配置可執行檔路徑**：`command` 欄位必須參考 Claude Code 可執行檔。如果 `claude` 命令不在您的系統 PATH 中，您需要指定可執行檔的完整路徑。

  若要找到完整路徑：

  ```bash theme={null}
  which claude
  ```

  然後在您的配置中使用完整路徑：

  ```json theme={null}
  {
    "mcpServers": {
      "claude-code": {
        "type": "stdio",
        "command": "/full/path/to/claude",
        "args": ["mcp", "serve"],
        "env": {}
      }
    }
  }
  ```

  沒有正確的可執行檔路徑，您會遇到類似 `spawn claude ENOENT` 的錯誤。
</Warning>

<Tip>
  提示：

  * server 提供對 Claude 工具 (如 View、Edit、LS 等) 的存取
  * 在 Claude Desktop 中，嘗試要求 Claude 讀取目錄中的檔案、進行編輯等。
  * 請注意，此 MCP server 僅將 Claude Code 的工具公開給您的 MCP 用戶端，因此您自己的用戶端負責為個別工具呼叫實現使用者確認。
</Tip>

## MCP 輸出限制和警告

當 MCP 工具產生大型輸出時，Claude Code 可幫助管理 token 使用情況，以防止淹沒您的對話內容：

* **輸出警告閾值**：當任何 MCP 工具輸出超過 10,000 個 tokens 時，Claude Code 會顯示警告
* **可配置限制**：您可以使用 `MAX_MCP_OUTPUT_TOKENS` 環境變數調整最大允許的 MCP 輸出 tokens
* **預設限制**：預設最大值為 25,000 個 tokens
* **範圍**：環境變數適用於未宣告自己限制的工具。設定 [`anthropic/maxResultSizeChars`](#raise-the-limit-for-a-specific-tool) 的工具使用該值代替文字內容，無論 `MAX_MCP_OUTPUT_TOKENS` 設定為什麼。傳回影像資料的工具仍受 `MAX_MCP_OUTPUT_TOKENS` 限制

若要增加產生大型輸出的工具的限制：

```bash theme={null}
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

這在使用以下 MCP servers 時特別有用：

* 查詢大型資料集或資料庫
* 產生詳細報告或文件
* 處理廣泛的日誌檔案或除錯資訊

### 提高特定工具的限制

如果您正在建立 MCP server，您可以透過在工具的 `tools/list` 回應項目中設定 `_meta["anthropic/maxResultSizeChars"]` 來允許個別工具傳回超過預設持久化到磁碟閾值的結果。Claude Code 將該工具的閾值提高到註解值，最高為 500,000 個字元的硬上限。

這對於傳回本質上很大但必要的輸出的工具很有用，例如資料庫架構或完整檔案樹。沒有註解，超過預設閾值的結果會持久化到磁碟，並在對話中被檔案參考取代。

```json theme={null}
{
  "name": "get_schema",
  "description": "Returns the full database schema",
  "_meta": {
    "anthropic/maxResultSizeChars": 200000
  }
}
```

對於文字內容，註解獨立於 `MAX_MCP_OUTPUT_TOKENS` 應用，因此使用者無需提高環境變數來使用宣告它的工具。傳回影像資料的工具仍受 token 限制。

<Warning>
  如果您經常遇到特定 MCP servers 的輸出警告，請考慮增加 `MAX_MCP_OUTPUT_TOKENS` 限制。您也可以要求 server 作者新增 `anthropic/maxResultSizeChars` 註解或分頁其回應。註解對傳回影像內容的工具沒有影響；對於這些，提高 `MAX_MCP_OUTPUT_TOKENS` 是唯一的選項。
</Warning>

## 回應 MCP 引發請求

MCP servers 可以使用引發在任務中途要求您提供結構化輸入。當 server 需要無法自行取得的資訊時，Claude Code 會顯示互動式對話框並將您的回應傳回給 server。您無需進行任何配置：當 server 要求時，引發對話框會自動出現。

Servers 可以透過兩種方式要求輸入：

* **表單模式**：Claude Code 顯示一個對話框，其中包含 server 定義的表單欄位 (例如，使用者名稱和密碼提示)。填入欄位並提交。
* **URL 模式**：Claude Code 開啟瀏覽器 URL 以進行驗證或批准。在瀏覽器中完成流程，然後在 CLI 中確認。

若要自動回應引發請求而不顯示對話框，請使用 [`Elicitation` hook](/zh-TW/hooks#Elicitation)。

如果您正在建立使用引發的 MCP server，請參閱 [MCP 引發規格](https://modelcontextprotocol.io/docs/learn/client-concepts#elicitation)，了解協議詳細資訊和架構範例。

## 使用 MCP 資源

MCP servers 可以公開資源，您可以使用 @ 提及來參考，類似於您參考檔案的方式。

### 參考 MCP 資源

<Steps>
  <Step title="列出可用資源">
    在您的提示中輸入 `@` 以查看所有連接的 MCP servers 中的可用資源。資源與檔案一起出現在自動完成功能表中。
  </Step>

  <Step title="參考特定資源">
    使用格式 `@server:protocol://resource/path` 來參考資源：

    ```text theme={null}
    Can you analyze @github:issue://123 and suggest a fix?
    ```

    ```text theme={null}
    Please review the API documentation at @docs:file://api/authentication
    ```
  </Step>

  <Step title="多個資源參考">
    您可以在單個提示中參考多個資源：

    ```text theme={null}
    Compare @postgres:schema://users with @docs:file://database/user-model
    ```
  </Step>
</Steps>

<Tip>
  提示：

  * 資源在參考時會自動取得並作為附件包含
  * 資源路徑在 @ 提及自動完成中可進行模糊搜尋
  * Claude Code 在 servers 支援時自動提供列出和讀取 MCP 資源的工具
  * 資源可以包含 MCP server 提供的任何類型的內容 (文字、JSON、結構化資料等)
</Tip>

## 使用 MCP Tool Search 進行擴展

Tool search 透過延遲工具定義直到 Claude 需要它們來保持 MCP 內容使用低。只有工具名稱在 session 啟動時載入，因此新增更多 MCP servers 對您的內容視窗的影響最小。

### 工作原理

Tool search 預設啟用。MCP 工具被延遲而不是預先載入到內容中，Claude 使用搜尋工具在任務需要時探索相關的工具。只有 Claude 實際使用的工具才會進入內容。從您的角度來看，MCP 工具的工作方式完全相同。

如果您偏好基於閾值的載入，請設定 `ENABLE_TOOL_SEARCH=auto` 以在工具適合內容視窗的 10% 內時預先載入架構，並僅延遲溢出。請參閱 [配置 tool search](#configure-tool-search) 了解所有選項。

### 對於 MCP server 作者

如果您正在建立 MCP server，啟用 Tool Search 時 server 指示欄位會變得更有用。Server 指示可幫助 Claude 了解何時搜尋您的工具，類似於 [skills](/zh-TW/skills) 的工作方式。

新增清晰、描述性的 server 指示，說明：

* 您的工具處理的任務類別
* Claude 應何時搜尋您的工具
* 您的 server 提供的關鍵功能

Claude Code 將工具描述和 server 指示截斷為每個 2KB。保持簡潔以避免截斷，並將關鍵詳細資訊放在開始處。

### 配置 tool search

Tool search 預設啟用：MCP 工具被延遲並按需探索。Claude Code 在 Vertex AI 上預設停用它。當 `ANTHROPIC_BASE_URL` 指向非第一方主機時，它也被停用，因為大多數代理不轉發 `tool_reference` 區塊。設定 `ENABLE_TOOL_SEARCH` 明確以覆蓋任一回退。

Tool search 需要支援 `tool_reference` 區塊的模型：Sonnet 4 及更新版本，或 Opus 4 及更新版本。Haiku 模型不支援它。在 Vertex AI 上，tool search 支援 Claude Sonnet 4.5 及更新版本和 Claude Opus 4.5 及更新版本。

使用 `ENABLE_TOOL_SEARCH` 環境變數控制 tool search 行為：

| 值        | 行為                                                                                                                                   |
| :------- | :----------------------------------------------------------------------------------------------------------------------------------- |
| (未設定)    | 所有 MCP 工具被延遲並按需載入。在 Vertex AI 上或當 `ANTHROPIC_BASE_URL` 是非第一方主機時回退到預先載入                                                               |
| `true`   | 所有 MCP 工具被延遲。Claude Code 即使在 Vertex AI 上和透過代理也會傳送 beta 標頭。在不支援 `tool_reference` 區塊的 Vertex AI 模型上或在不支援 `tool_reference` 區塊的代理上，請求會失敗 |
| `auto`   | 閾值模式：如果工具適合內容視窗的 10% 內，則預先載入，否則延遲                                                                                                    |
| `auto:N` | 閾值模式，具有自訂百分比，其中 `N` 是 0-100。例如，`auto:5` 表示 5%                                                                                        |
| `false`  | 所有 MCP 工具預先載入，無延遲                                                                                                                    |

```bash theme={null}
# 使用自訂 5% 閾值
ENABLE_TOOL_SEARCH=auto:5 claude

# 完全停用 tool search
ENABLE_TOOL_SEARCH=false claude
```

或在您的 [settings.json `env` 欄位](/zh-TW/settings#available-settings) 中設定值。

您也可以特別停用 `ToolSearch` 工具：

```json theme={null}
{
  "permissions": {
    "deny": ["ToolSearch"]
  }
}
```

### 豁免伺服器延遲

如果伺服器的工具應始終對 Claude 可見而無需搜尋步驟，請在該伺服器的配置中將 `alwaysLoad` 設定為 `true`。該伺服器的每個工具隨後都會在 session 啟動時載入到內容中，無論 `ENABLE_TOOL_SEARCH` 設定如何。對於 Claude 在每個回合都需要的少量工具，請使用此選項，因為每個預先載入的工具會消耗內容，否則這些內容將可用於您的對話。

以下 `.mcp.json` 項目豁免一個 HTTP 伺服器，同時保持其他伺服器延遲：

```json theme={null}
{
  "mcpServers": {
    "core-tools": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "alwaysLoad": true
    }
  }
}
```

`alwaysLoad` 欄位在所有伺服器類型上可用，需要 Claude Code v2.1.121 或更新版本。MCP 伺服器也可以透過在工具的 `_meta` 物件中包含 `"anthropic/alwaysLoad": true` 來標記個別工具為始終載入，這對該工具只有相同的效果。

設定 `alwaysLoad: true` 也會阻止啟動直到伺服器連線，上限為標準 5 秒連線逾時。即使 MCP 啟動在其他方面[預設為非阻塞](/zh-TW/env-vars)，這也適用，因為工具必須在建立第一個提示時存在。其他伺服器繼續在背景中連線。

## 使用 MCP 提示作為命令

MCP servers 可以公開提示，這些提示在 Claude Code 中變成可用的命令。

### 執行 MCP 提示

<Steps>
  <Step title="探索可用提示">
    輸入 `/` 以查看所有可用命令，包括來自 MCP servers 的命令。MCP 提示以 `/mcp__servername__promptname` 的格式出現。
  </Step>

  <Step title="執行沒有引數的提示">
    ```text theme={null}
    /mcp__github__list_prs
    ```
  </Step>

  <Step title="執行帶有引數的提示">
    許多提示接受引數。在命令後以空格分隔的方式傳遞它們：

    ```text theme={null}
    /mcp__github__pr_review 456
    ```

    ```text theme={null}
    /mcp__jira__create_issue "Bug in login flow" high
    ```
  </Step>
</Steps>

<Tip>
  提示：

  * MCP 提示從連接的 servers 動態探索
  * 引數根據提示的定義參數進行解析
  * 提示結果直接注入到對話中
  * Server 和提示名稱已標準化 (空格變成底線)
</Tip>

## 受管理的 MCP 配置

對於需要對使用者可以連接的 MCP servers 進行集中控制的組織，請參閱 [受管理的 MCP 配置](/zh-TW/managed-mcp)。它涵蓋使用 `managed-mcp.json` 部署固定的 server 集合、使用 `allowedMcpServers` 和 `deniedMcpServers` 限制 servers，以及當 server 被阻止時使用者看到的內容。
