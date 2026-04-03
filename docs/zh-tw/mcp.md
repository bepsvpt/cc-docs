> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 透過 MCP 將 Claude Code 連接到工具

> 了解如何使用 Model Context Protocol 將 Claude Code 連接到您的工具。

export const MCPServersTable = ({platform = "all"}) => {
  const ifYouAreAnAiAgentReadingThisYouShouldInsteadFetch = 'https://api.anthropic.com/mcp-registry/docs';
  const [servers, setServers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    const fetchServers = async () => {
      try {
        setLoading(true);
        const allServers = [];
        let cursor = null;
        do {
          const url = new URL('https://api.anthropic.com/mcp-registry/v0/servers');
          url.searchParams.set('version', 'latest');
          url.searchParams.set('visibility', 'commercial');
          url.searchParams.set('limit', '100');
          if (cursor) {
            url.searchParams.set('cursor', cursor);
          }
          const response = await fetch(url);
          if (!response.ok) {
            throw new Error(`Failed to fetch MCP registry: ${response.status}`);
          }
          const data = await response.json();
          allServers.push(...data.servers);
          cursor = data.metadata?.nextCursor || null;
        } while (cursor);
        const transformedServers = allServers.map(item => {
          const server = item.server;
          const meta = item._meta?.['com.anthropic.api/mcp-registry'] || ({});
          const worksWith = meta.worksWith || [];
          const availability = {
            claudeCode: worksWith.includes('claude-code'),
            mcpConnector: worksWith.includes('claude-api'),
            claudeDesktop: worksWith.includes('claude-desktop')
          };
          const remotes = server.remotes || [];
          const httpRemote = remotes.find(r => r.type === 'streamable-http');
          const sseRemote = remotes.find(r => r.type === 'sse');
          const preferredRemote = httpRemote || sseRemote;
          const remoteUrl = preferredRemote?.url || meta.url;
          const remoteType = preferredRemote?.type;
          const isTemplatedUrl = remoteUrl?.includes('{');
          let setupUrl;
          if (isTemplatedUrl && meta.requiredFields) {
            const urlField = meta.requiredFields.find(f => f.field === 'url');
            setupUrl = urlField?.sourceUrl || meta.documentation;
          }
          const urls = {};
          if (!isTemplatedUrl) {
            if (remoteType === 'streamable-http') {
              urls.http = remoteUrl;
            } else if (remoteType === 'sse') {
              urls.sse = remoteUrl;
            }
          }
          let envVars = [];
          if (server.packages && server.packages.length > 0) {
            const npmPackage = server.packages.find(p => p.registryType === 'npm');
            if (npmPackage) {
              urls.stdio = `npx -y ${npmPackage.identifier}`;
              if (npmPackage.environmentVariables) {
                envVars = npmPackage.environmentVariables;
              }
            }
          }
          return {
            name: meta.displayName || server.title || server.name,
            description: meta.oneLiner || server.description,
            documentation: meta.documentation,
            urls: urls,
            envVars: envVars,
            availability: availability,
            customCommands: meta.claudeCodeCopyText ? {
              claudeCode: meta.claudeCodeCopyText
            } : undefined,
            setupUrl: setupUrl
          };
        });
        setServers(transformedServers);
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching MCP registry:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchServers();
  }, []);
  const generateClaudeCodeCommand = server => {
    if (server.customCommands && server.customCommands.claudeCode) {
      return server.customCommands.claudeCode;
    }
    const serverSlug = server.name.toLowerCase().replace(/[^a-z0-9]/g, '-');
    if (server.urls.http) {
      return `claude mcp add ${serverSlug} --transport http ${server.urls.http}`;
    }
    if (server.urls.sse) {
      return `claude mcp add ${serverSlug} --transport sse ${server.urls.sse}`;
    }
    if (server.urls.stdio) {
      const envFlags = server.envVars && server.envVars.length > 0 ? server.envVars.map(v => `--env ${v.name}=YOUR_${v.name}`).join(' ') : '';
      const baseCommand = `claude mcp add ${serverSlug} --transport stdio`;
      return envFlags ? `${baseCommand} ${envFlags} -- ${server.urls.stdio}` : `${baseCommand} -- ${server.urls.stdio}`;
    }
    return null;
  };
  if (loading) {
    return <div>Loading MCP servers...</div>;
  }
  if (error) {
    return <div>Error loading MCP servers: {error}</div>;
  }
  const filteredServers = servers.filter(server => {
    if (platform === "claudeCode") {
      return server.availability.claudeCode;
    } else if (platform === "mcpConnector") {
      return server.availability.mcpConnector;
    } else if (platform === "claudeDesktop") {
      return server.availability.claudeDesktop;
    } else if (platform === "all") {
      return true;
    } else {
      throw new Error(`Unknown platform: ${platform}`);
    }
  });
  return <>
      <style jsx>{`
        .cards-container {
          display: grid;
          gap: 1rem;
          margin-bottom: 2rem;
        }
        .server-card {
          border: 1px solid var(--border-color, #e5e7eb);
          border-radius: 6px;
          padding: 1rem;
        }
        .command-row {
          display: flex;
          align-items: center;
          gap: 0.25rem;
        }
        .command-row code {
          font-size: 0.75rem;
          overflow-x: auto;
        }
      `}</style>

      <div className="cards-container">
        {filteredServers.map(server => {
    const claudeCodeCommand = generateClaudeCodeCommand(server);
    const mcpUrl = server.urls.http || server.urls.sse;
    const commandToShow = platform === "claudeCode" ? claudeCodeCommand : mcpUrl;
    return <div key={server.name} className="server-card">
              <div>
                {server.documentation ? <a href={server.documentation}>
                    <strong>{server.name}</strong>
                  </a> : <strong>{server.name}</strong>}
              </div>

              <p style={{
      margin: '0.5rem 0',
      fontSize: '0.9rem'
    }}>
                {server.description}
              </p>

              {server.setupUrl && <p style={{
      margin: '0.25rem 0',
      fontSize: '0.8rem',
      fontStyle: 'italic',
      opacity: 0.7
    }}>
                  Requires user-specific URL.{' '}
                  <a href={server.setupUrl} style={{
      textDecoration: 'underline'
    }}>
                    Get your URL here
                  </a>.
                </p>}

              {commandToShow && !server.setupUrl && <>
                <p style={{
      display: 'block',
      fontSize: '0.75rem',
      fontWeight: 500,
      minWidth: 'fit-content',
      marginTop: '0.5rem',
      marginBottom: 0
    }}>
                  {platform === "claudeCode" ? "Command" : "URL"}
                </p>
                <div className="command-row">
                  <code>
                    {commandToShow}
                  </code>
                </div>
              </>}
            </div>;
  })}
      </div>
    </>;
};

Claude Code 可以透過 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) 連接到數百個外部工具和資料來源，這是一個開源標準，用於 AI 工具整合。MCP servers 讓 Claude Code 能夠存取您的工具、資料庫和 API。

## 使用 MCP 可以做什麼

連接 MCP servers 後，您可以要求 Claude Code：

* **從問題追蹤器實現功能**："新增 JIRA 問題 ENG-4521 中描述的功能，並在 GitHub 上建立 PR。"
* **分析監控資料**："檢查 Sentry 和 Statsig，以檢查 ENG-4521 中描述的功能使用情況。"
* **查詢資料庫**："根據我們的 PostgreSQL 資料庫，找到 10 個使用功能 ENG-4521 的隨機使用者的電子郵件。"
* **整合設計**："根據在 Slack 中發佈的新 Figma 設計更新我們的標準電子郵件範本"
* **自動化工作流程**："建立 Gmail 草稿，邀請這 10 個使用者參加關於新功能的回饋會議。"
* **回應外部事件**：MCP server 也可以充當 [channel](/zh-TW/channels)，將訊息推送到您的 session 中，因此當您不在時，Claude 可以回應 Telegram 訊息、Discord 聊天或 webhook 事件。

## 熱門 MCP servers

以下是一些您可以連接到 Claude Code 的常用 MCP servers：

<Warning>
  使用第三方 MCP servers 需自行承擔風險 - Anthropic 尚未驗證
  所有這些 servers 的正確性或安全性。
  請確保您信任要安裝的 MCP servers。
  使用可能會取得不受信任內容的 MCP servers 時要特別小心，
  因為這些可能會使您面臨提示注入風險。
</Warning>

<MCPServersTable platform="claudeCode" />

<Note>
  **需要特定的整合？** [在 GitHub 上找到數百個更多 MCP servers](https://github.com/modelcontextprotocol/servers)，或使用 [MCP SDK](https://modelcontextprotocol.io/quickstart/server) 建立您自己的。
</Note>

## 安裝 MCP servers

MCP servers 可以根據您的需求以三種不同的方式進行配置：

### 選項 1：新增遠端 HTTP server

HTTP servers 是連接到遠端 MCP servers 的推薦選項。這是雲端服務最廣泛支援的傳輸方式。

```bash  theme={null}
# 基本語法
claude mcp add --transport http <name> <url>

# 實際範例：連接到 Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# 使用 Bearer token 的範例
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### 選項 2：新增遠端 SSE server

<Warning>
  SSE (Server-Sent Events) 傳輸已棄用。請改用 HTTP servers（如果可用）。
</Warning>

```bash  theme={null}
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

```bash  theme={null}
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

```bash  theme={null}
# 列出所有已配置的 servers
claude mcp list

# 取得特定 server 的詳細資訊
claude mcp get github

# 移除 server
claude mcp remove github

# (在 Claude Code 中) 檢查 server 狀態
/mcp
```

### 動態工具更新

Claude Code 支援 MCP `list_changed` 通知，允許 MCP servers 動態更新其可用工具、提示和資源，而無需您斷開連接並重新連接。當 MCP server 傳送 `list_changed` 通知時，Claude Code 會自動重新整理該 server 的可用功能。

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
  * 當 MCP 工具輸出超過 10,000 個 tokens 時，Claude Code 會顯示警告。若要增加此限制，請設定 `MAX_MCP_OUTPUT_TOKENS` 環境變數 (例如，`MAX_MCP_OUTPUT_TOKENS=50000`)
  * 使用 `/mcp` 向需要 OAuth 2.0 驗證的遠端 servers 進行驗證
</Tip>

<Warning>
  **Windows 使用者**：在原生 Windows (不是 WSL) 上，使用 `npx` 的本機 MCP servers 需要 `cmd /c` 包裝器以確保正確執行。

  ```bash  theme={null}
  # 這會建立 command="cmd"，Windows 可以執行
  claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
  ```

  沒有 `cmd /c` 包裝器，您會遇到「Connection closed」錯誤，因為 Windows 無法直接執行 `npx`。(請參閱上面的注意事項，了解 `--` 參數的說明。)
</Warning>

### Plugin 提供的 MCP servers

[Plugins](/zh-TW/plugins) 可以捆綁 MCP servers，在啟用 plugin 時自動提供工具和整合。Plugin MCP servers 的工作方式與使用者配置的 servers 相同。

**Plugin MCP servers 的工作方式**：

* Plugins 在 plugin 根目錄的 `.mcp.json` 中或在 `plugin.json` 中內聯定義 MCP servers
* 啟用 plugin 時，其 MCP servers 會自動啟動
* Plugin MCP 工具與手動配置的 MCP 工具一起出現
* Plugin servers 透過 plugin 安裝進行管理 (不是 `/mcp` 命令)

**Plugin MCP 配置範例**：

在 plugin 根目錄的 `.mcp.json` 中：

```json  theme={null}
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

```json  theme={null}
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
* **環境變數**：使用 `${CLAUDE_PLUGIN_ROOT}` 表示 plugin 相對路徑，以及 `${CLAUDE_PLUGIN_DATA}` 表示 [persistent state](/zh-TW/plugins-reference#persistent-data-directory) 在 plugin 更新後仍然存在
* **使用者環境存取**：存取與手動配置的 servers 相同的環境變數
* **多種傳輸類型**：支援 stdio、SSE 和 HTTP 傳輸 (傳輸支援可能因 server 而異)

**檢視 plugin MCP servers**：

```bash  theme={null}
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

MCP servers 可以在三個不同的範圍級別進行配置，每個級別都用於管理 server 可存取性和共享的不同目的。了解這些範圍可幫助您確定為特定需求配置 servers 的最佳方式。

### 本機範圍

本機範圍的 servers 代表預設配置級別，儲存在您專案路徑下的 `~/.claude.json` 中。這些 servers 對您保持私密，只有在專案目錄中工作時才可存取。此範圍非常適合個人開發 servers、實驗配置或包含不應共享的敏感認證的 servers。

<Note>
  MCP servers 的「本機範圍」術語與一般本機設定不同。MCP 本機範圍的 servers 儲存在 `~/.claude.json` (您的主目錄) 中，而一般本機設定使用 `.claude/settings.local.json` (在專案目錄中)。請參閱 [Settings](/zh-TW/settings#settings-files) 了解設定檔案位置的詳細資訊。
</Note>

```bash  theme={null}
# 新增本機範圍的 server (預設)
claude mcp add --transport http stripe https://mcp.stripe.com

# 明確指定本機範圍
claude mcp add --transport http stripe --scope local https://mcp.stripe.com
```

### 專案範圍

專案範圍的 servers 透過在專案根目錄中儲存配置在 `.mcp.json` 檔案中來啟用團隊協作。此檔案設計為簽入版本控制，確保所有團隊成員都能存取相同的 MCP 工具和服務。新增專案範圍的 server 時，Claude Code 會自動建立或更新此檔案，使用適當的配置結構。

```bash  theme={null}
# 新增專案範圍的 server
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp
```

產生的 `.mcp.json` 檔案遵循標準化格式：

```json  theme={null}
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

出於安全考慮，Claude Code 在使用來自 `.mcp.json` 檔案的專案範圍 servers 之前會提示批准。如果您需要重設這些批准選擇，請使用 `claude mcp reset-project-choices` 命令。

### 使用者範圍

使用者範圍的 servers 儲存在 `~/.claude.json` 中，並提供跨專案可存取性，使其在您機器上的所有專案中可用，同時對您的使用者帳戶保持私密。此範圍非常適合個人公用程式 servers、開發工具或您在不同專案中經常使用的服務。

```bash  theme={null}
# 新增使用者 server
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic
```

### 選擇正確的範圍

根據以下條件選擇您的範圍：

* **本機範圍**：個人 servers、實驗配置或特定於一個專案的敏感認證
* **專案範圍**：團隊共享的 servers、專案特定的工具或協作所需的服務
* **使用者範圍**：跨多個專案所需的個人公用程式、開發工具或經常使用的服務

<Note>
  **MCP servers 儲存在哪裡？**

  * **使用者和本機範圍**：`~/.claude.json` (在 `mcpServers` 欄位或專案路徑下)
  * **專案範圍**：專案根目錄中的 `.mcp.json` (簽入原始碼控制)
  * **受管理**：系統目錄中的 `managed-mcp.json` (請參閱 [受管理 MCP 配置](#managed-mcp-configuration))
</Note>

### 範圍階層和優先順序

MCP server 配置遵循清晰的優先順序階層。當相同名稱的 servers 存在於多個範圍時，系統透過優先考慮本機範圍的 servers 來解決衝突，其次是專案範圍的 servers，最後是使用者範圍的 servers。此設計確保個人配置可以在需要時覆蓋共享配置。

如果 server 同時透過本機配置和 [claude.ai connector](#use-mcp-servers-from-claude-ai) 進行配置，本機配置優先，connector 項目會被跳過。

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

```json  theme={null}
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

```bash  theme={null}
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

使用您的 Sentry 帳戶進行驗證：

```text  theme={null}
/mcp
```

然後除錯生產問題：

```text  theme={null}
過去 24 小時內最常見的錯誤是什麼？
```

```text  theme={null}
顯示錯誤 ID abc123 的堆疊追蹤
```

```text  theme={null}
哪個部署引入了這些新錯誤？
```

### 範例：連接到 GitHub 進行程式碼審查

```bash  theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

如果需要，透過為 GitHub 選擇「Authenticate」進行驗證：

```text  theme={null}
/mcp
```

然後使用 GitHub：

```text  theme={null}
審查 PR #456 並建議改進
```

```text  theme={null}
為我們剛發現的錯誤建立新問題
```

```text  theme={null}
顯示所有指派給我的開放 PRs
```

### 範例：查詢您的 PostgreSQL 資料庫

```bash  theme={null}
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:pass@prod.db.com:5432/analytics"
```

然後自然地查詢您的資料庫：

```text  theme={null}
本月我們的總收入是多少？
```

```text  theme={null}
顯示 orders 表的架構
```

```text  theme={null}
找到 90 天內未進行購買的客戶
```

## 使用遠端 MCP servers 進行驗證

許多雲端 MCP servers 需要驗證。Claude Code 支援 OAuth 2.0 以進行安全連接。

<Steps>
  <Step title="新增需要驗證的 server">
    例如：

    ```bash  theme={null}
    claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
    ```
  </Step>

  <Step title="在 Claude Code 中使用 /mcp 命令">
    在 Claude Code 中，使用命令：

    ```text  theme={null}
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

```bash  theme={null}
# 使用動態用戶端註冊的固定回呼連接埠
claude mcp add --transport http \
  --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

### 使用預先配置的 OAuth 認證

某些 MCP servers 不支援自動 OAuth 設定。如果您看到類似「Incompatible auth server: does not support dynamic client registration」的錯誤，server 需要預先配置的認證。Claude Code 也支援使用 Client ID Metadata Document (CIMD) 而不是 Dynamic Client Registration 的 servers，並自動探索這些。如果自動探索失敗，請先透過 server 的開發人員入口網站註冊 OAuth 應用程式，然後在新增 server 時提供認證。

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

        ```bash  theme={null}
        claude mcp add --transport http \
          --client-id your-client-id --client-secret --callback-port 8080 \
          my-server https://mcp.example.com/mcp
        ```
      </Tab>

      <Tab title="claude mcp add-json">
        在 JSON 配置中包含 `oauth` 物件，並將 `--client-secret` 作為單獨的旗標傳遞：

        ```bash  theme={null}
        claude mcp add-json my-server \
          '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' \
          --client-secret
        ```
      </Tab>

      <Tab title="claude mcp add-json (僅回呼連接埠)">
        使用 `--callback-port` 而不使用用戶端 ID 來固定連接埠，同時使用動態用戶端註冊：

        ```bash  theme={null}
        claude mcp add-json my-server \
          '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"callbackPort":8080}}'
        ```
      </Tab>

      <Tab title="CI / env var">
        透過環境變數設定密碼以跳過互動式提示：

        ```bash  theme={null}
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

如果您的 MCP server 的標準 OAuth 中繼資料端點返回錯誤，但公開了工作的 OIDC 端點，您可以指向 Claude Code 特定的中繼資料 URL 以繞過預設探索鏈。根據預設，Claude Code 首先檢查 RFC 9728 Protected Resource Metadata at `/.well-known/oauth-protected-resource`，然後回退到 RFC 8414 authorization server metadata at `/.well-known/oauth-authorization-server`。

在 `.mcp.json` 中 server 配置的 `oauth` 物件中設定 `authServerMetadataUrl`：

```json  theme={null}
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

URL 必須使用 `https://`。此選項需要 Claude Code v2.1.64 或更新版本。

### 使用動態標頭進行自訂驗證

如果您的 MCP server 使用 OAuth 以外的驗證方案 (例如 Kerberos、短期 tokens 或內部 SSO)，請使用 `headersHelper` 在連接時產生請求標頭。Claude Code 執行命令並將其輸出合併到連接標頭中。

```json  theme={null}
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

```json  theme={null}
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
    ```bash  theme={null}
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
    ```bash  theme={null}
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
    ```bash  theme={null}
    # 基本語法 
    claude mcp add-from-claude-desktop 
    ```
  </Step>

  <Step title="選擇要匯入的 servers">
    執行命令後，您會看到一個互動式對話框，允許您選擇要匯入的 servers。
  </Step>

  <Step title="驗證 servers 已匯入">
    ```bash  theme={null}
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
    在 [claude.ai/settings/connectors](https://claude.ai/settings/connectors) 新增 servers。在 Team 和 Enterprise 計畫上，只有管理員可以新增 servers。
  </Step>

  <Step title="驗證 MCP server">
    在 Claude.ai 中完成任何必需的驗證步驟。
  </Step>

  <Step title="在 Claude Code 中檢視和管理 servers">
    在 Claude Code 中，使用命令：

    ```text  theme={null}
    /mcp
    ```

    Claude.ai servers 在列表中出現，並有指示器顯示它們來自 Claude.ai。
  </Step>
</Steps>

若要在 Claude Code 中停用 claude.ai MCP servers，請將 `ENABLE_CLAUDEAI_MCP_SERVERS` 環境變數設定為 `false`：

```bash  theme={null}
ENABLE_CLAUDEAI_MCP_SERVERS=false claude
```

## 使用 Claude Code 作為 MCP server

您可以使用 Claude Code 本身作為其他應用程式可以連接到的 MCP server：

```bash  theme={null}
# 啟動 Claude 作為 stdio MCP server
claude mcp serve
```

您可以透過將此配置新增到 claude\_desktop\_config.json 在 Claude Desktop 中使用它：

```json  theme={null}
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

  ```bash  theme={null}
  which claude
  ```

  然後在您的配置中使用完整路徑：

  ```json  theme={null}
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

若要增加產生大型輸出的工具的限制：

```bash  theme={null}
# 為 MCP 工具輸出設定更高的限制
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

這在使用以下 MCP servers 時特別有用：

* 查詢大型資料集或資料庫
* 產生詳細報告或文件
* 處理廣泛的日誌檔案或除錯資訊

<Warning>
  如果您經常遇到特定 MCP servers 的輸出警告，請考慮增加限制或配置 server 以分頁或篩選其回應。
</Warning>

## 回應 MCP 引發請求

MCP servers 可以在任務中途使用引發來要求您提供結構化輸入。當 server 需要無法自行取得的資訊時，Claude Code 會顯示互動式對話框並將您的回應傳回給 server。您無需進行任何配置：當 server 要求時，引發對話框會自動出現。

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

    ```text  theme={null}
    Can you analyze @github:issue://123 and suggest a fix?
    ```

    ```text  theme={null}
    Please review the API documentation at @docs:file://api/authentication
    ```
  </Step>

  <Step title="多個資源參考">
    您可以在單個提示中參考多個資源：

    ```text  theme={null}
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

Tool search 預設啟用：MCP 工具被延遲並按需探索。當 `ANTHROPIC_BASE_URL` 指向非第一方主機時，tool search 預設停用，因為大多數代理不轉發 `tool_reference` 區塊。如果您的代理執行此操作，請明確設定 `ENABLE_TOOL_SEARCH`。此功能需要支援 `tool_reference` 區塊的模型：Sonnet 4 及更新版本，或 Opus 4 及更新版本。Haiku 模型不支援 tool search。

使用 `ENABLE_TOOL_SEARCH` 環境變數控制 tool search 行為：

| 值          | 行為                                                       |
| :--------- | :------------------------------------------------------- |
| (未設定)      | 所有 MCP 工具被延遲並按需載入。當 `ANTHROPIC_BASE_URL` 是非第一方主機時回退到預先載入 |
| `true`     | 所有 MCP 工具被延遲，包括對於非第一方 `ANTHROPIC_BASE_URL`               |
| `auto`     | 閾值模式：如果工具適合內容視窗的 10% 內，則預先載入，否則延遲                        |
| `auto:<N>` | 閾值模式，具有自訂百分比，其中 `<N>` 是 0-100 (例如，`auto:5` 表示 5%)        |
| `false`    | 所有 MCP 工具預先載入，無延遲                                        |

```bash  theme={null}
# 使用自訂 5% 閾值
ENABLE_TOOL_SEARCH=auto:5 claude

# 完全停用 tool search
ENABLE_TOOL_SEARCH=false claude
```

或在您的 [settings.json `env` 欄位](/zh-TW/settings#available-settings) 中設定值。

您也可以特別停用 `ToolSearch` 工具：

```json  theme={null}
{
  "permissions": {
    "deny": ["ToolSearch"]
  }
}
```

## 使用 MCP 提示作為命令

MCP servers 可以公開提示，這些提示在 Claude Code 中變成可用的命令。

### 執行 MCP 提示

<Steps>
  <Step title="探索可用提示">
    輸入 `/` 以查看所有可用命令，包括來自 MCP servers 的命令。MCP 提示以 `/mcp__servername__promptname` 的格式出現。
  </Step>

  <Step title="執行沒有引數的提示">
    ```text  theme={null}
    /mcp__github__list_prs
    ```
  </Step>

  <Step title="執行帶有引數的提示">
    許多提示接受引數。在命令後以空格分隔的方式傳遞它們：

    ```text  theme={null}
    /mcp__github__pr_review 456
    ```

    ```text  theme={null}
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

對於需要對 MCP servers 進行集中控制的組織，Claude Code 支援兩個配置選項：

1. **使用 `managed-mcp.json` 的獨佔控制**：部署一組固定的 MCP servers，使用者無法修改或擴展
2. **使用允許清單/拒絕清單的基於原則的控制**：允許使用者新增自己的 servers，但限制允許的 servers

這些選項允許 IT 管理員：

* **控制 MCP servers 員工可以存取的內容**：在整個組織中部署一組標準化的已批准 MCP servers
* **防止未授權的 MCP servers**：限制使用者新增未批准的 MCP servers
* **完全停用 MCP**：如果需要，完全移除 MCP 功能

### 選項 1：使用 managed-mcp.json 的獨佔控制

當您部署 `managed-mcp.json` 檔案時，它對所有 MCP servers 進行**獨佔控制**。使用者無法新增、修改或使用此檔案中定義的 MCP servers 以外的任何 MCP servers。這是希望完全控制的組織的最簡單方法。

系統管理員將配置檔案部署到系統範圍的目錄：

* macOS：`/Library/Application Support/ClaudeCode/managed-mcp.json`
* Linux 和 WSL：`/etc/claude-code/managed-mcp.json`
* Windows：`C:\Program Files\ClaudeCode\managed-mcp.json`

<Note>
  這些是系統範圍的路徑 (不是像 `~/Library/...` 這樣的使用者主目錄)，需要管理員權限。它們設計為由 IT 管理員部署。
</Note>

`managed-mcp.json` 檔案使用與標準 `.mcp.json` 檔案相同的格式：

```json  theme={null}
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/mcp"
    },
    "company-internal": {
      "type": "stdio",
      "command": "/usr/local/bin/company-mcp-server",
      "args": ["--config", "/etc/company/mcp-config.json"],
      "env": {
        "COMPANY_API_URL": "https://internal.company.com"
      }
    }
  }
}
```

### 選項 2：使用允許清單和拒絕清單的基於原則的控制

管理員可以允許使用者配置自己的 MCP servers，同時對允許的 servers 強制執行限制，而不是進行獨佔控制。此方法在 [受管理設定檔案](/zh-TW/settings#settings-files) 中使用 `allowedMcpServers` 和 `deniedMcpServers`。

<Note>
  **在選項之間選擇**：當您想要部署一組固定的 servers 而不進行使用者自訂時，使用選項 1 (`managed-mcp.json`)。當您想要允許使用者在原則約束內新增自己的 servers 時，使用選項 2 (允許清單/拒絕清單)。
</Note>

#### 限制選項

允許清單或拒絕清單中的每個項目可以透過三種方式限制 servers：

1. **按 server 名稱** (`serverName`)：符合 server 的已配置名稱
2. **按命令** (`serverCommand`)：符合用於啟動 stdio servers 的確切命令和引數
3. **按 URL 模式** (`serverUrl`)：符合遠端 server URLs，支援萬用字元

**重要**：每個項目必須恰好有 `serverName`、`serverCommand` 或 `serverUrl` 之一。

#### 配置範例

```json  theme={null}
{
  "allowedMcpServers": [
    // 按 server 名稱允許
    { "serverName": "github" },
    { "serverName": "sentry" },

    // 按確切命令允許 (對於 stdio servers)
    { "serverCommand": ["npx", "-y", "@modelcontextprotocol/server-filesystem"] },
    { "serverCommand": ["python", "/usr/local/bin/approved-server.py"] },

    // 按 URL 模式允許 (對於遠端 servers)
    { "serverUrl": "https://mcp.company.com/*" },
    { "serverUrl": "https://*.internal.corp/*" }
  ],
  "deniedMcpServers": [
    // 按 server 名稱阻止
    { "serverName": "dangerous-server" },

    // 按確切命令阻止 (對於 stdio servers)
    { "serverCommand": ["npx", "-y", "unapproved-package"] },

    // 按 URL 模式阻止 (對於遠端 servers)
    { "serverUrl": "https://*.untrusted.com/*" }
  ]
}
```

#### 基於命令的限制如何工作

**確切符合**：

* 命令陣列必須**確切**符合 - 命令和所有引數的順序正確
* 範例：`["npx", "-y", "server"]` 將**不**符合 `["npx", "server"]` 或 `["npx", "-y", "server", "--flag"]`

**Stdio server 行為**：

* 當允許清單包含**任何** `serverCommand` 項目時，stdio servers **必須**符合其中一個命令
* Stdio servers 在存在命令限制時無法單獨按名稱通過
* 這確保管理員可以強制執行允許執行的命令

**非 stdio server 行為**：

* 遠端 servers (HTTP、SSE、WebSocket) 在允許清單中存在 `serverUrl` 項目時使用基於 URL 的符合
* 如果不存在 URL 項目，遠端 servers 會回退到基於名稱的符合
* 命令限制不適用於遠端 servers

#### 基於 URL 的限制如何工作

URL 模式使用 `*` 支援萬用字元以符合任何字元序列。這對於允許整個網域或子網域很有用。

**萬用字元範例**：

* `https://mcp.company.com/*` - 允許特定網域上的所有路徑
* `https://*.example.com/*` - 允許 example.com 的任何子網域
* `http://localhost:*/*` - 允許 localhost 上的任何連接埠

**遠端 server 行為**：

* 當允許清單包含**任何** `serverUrl` 項目時，遠端 servers **必須**符合其中一個 URL 模式
* 遠端 servers 在存在 URL 限制時無法單獨按名稱通過
* 這確保管理員可以強制執行允許的遠端端點

<Accordion title="範例：僅 URL 允許清單">
  ```json  theme={null}
  {
    "allowedMcpServers": [
      { "serverUrl": "https://mcp.company.com/*" },
      { "serverUrl": "https://*.internal.corp/*" }
    ]
  }
  ```

  **結果**：

  * `https://mcp.company.com/api` 上的 HTTP server：✅ 允許 (符合 URL 模式)
  * `https://api.internal.corp/mcp` 上的 HTTP server：✅ 允許 (符合萬用字元子網域)
  * `https://external.com/mcp` 上的 HTTP server：❌ 阻止 (不符合任何 URL 模式)
  * 任何命令的 Stdio server：❌ 阻止 (沒有名稱或命令項目可符合)
</Accordion>

<Accordion title="範例：僅命令允許清單">
  ```json  theme={null}
  {
    "allowedMcpServers": [
      { "serverCommand": ["npx", "-y", "approved-package"] }
    ]
  }
  ```

  **結果**：

  * 使用 `["npx", "-y", "approved-package"]` 的 Stdio server：✅ 允許 (符合命令)
  * 使用 `["node", "server.js"]` 的 Stdio server：❌ 阻止 (不符合命令)
  * 名為「my-api」的 HTTP server：❌ 阻止 (沒有名稱項目可符合)
</Accordion>

<Accordion title="範例：混合名稱和命令允許清單">
  ```json  theme={null}
  {
    "allowedMcpServers": [
      { "serverName": "github" },
      { "serverCommand": ["npx", "-y", "approved-package"] }
    ]
  }
  ```

  **結果**：

  * 名為「local-tool」、使用 `["npx", "-y", "approved-package"]` 的 Stdio server：✅ 允許 (符合命令)
  * 名為「local-tool」、使用 `["node", "server.js"]` 的 Stdio server：❌ 阻止 (存在命令項目但不符合)
  * 名為「github」、使用 `["node", "server.js"]` 的 Stdio server：❌ 阻止 (存在命令限制時 stdio servers 必須符合命令)
  * 名為「github」的 HTTP server：✅ 允許 (符合名稱)
  * 名為「other-api」的 HTTP server：❌ 阻止 (名稱不符合)
</Accordion>

<Accordion title="範例：僅名稱允許清單">
  ```json  theme={null}
  {
    "allowedMcpServers": [
      { "serverName": "github" },
      { "serverName": "internal-tool" }
    ]
  }
  ```

  **結果**：

  * 名為「github」、任何命令的 Stdio server：✅ 允許 (沒有命令限制)
  * 名為「internal-tool」、任何命令的 Stdio server：✅ 允許 (沒有命令限制)
  * 名為「github」的 HTTP server：✅ 允許 (符合名稱)
  * 任何名為「other」的 server：❌ 阻止 (名稱不符合)
</Accordion>

#### 允許清單行為 (`allowedMcpServers`)

* `undefined` (預設)：無限制 - 使用者可以配置任何 MCP server
* 空陣列 `[]`：完全鎖定 - 使用者無法配置任何 MCP servers
* 項目清單：使用者只能配置符合名稱、命令或 URL 模式的 servers

#### 拒絕清單行為 (`deniedMcpServers`)

* `undefined` (預設)：沒有 servers 被阻止
* 空陣列 `[]`：沒有 servers 被阻止
* 項目清單：指定的 servers 在所有範圍中被明確阻止

#### 重要注意事項

* **選項 1 和選項 2 可以結合**：如果 `managed-mcp.json` 存在，它具有獨佔控制，使用者無法新增 servers。允許清單/拒絕清單仍然適用於受管理的 servers 本身。
* **拒絕清單具有絕對優先順序**：如果 server 符合拒絕清單項目 (按名稱、命令或 URL)，即使它在允許清單上也會被阻止
* 基於名稱、基於命令和基於 URL 的限制一起工作：如果 server 符合**任何**名稱項目、命令項目或 URL 模式，它就會通過 (除非被拒絕清單阻止)

<Note>
  **使用 `managed-mcp.json` 時**：使用者無法透過 `claude mcp add` 或配置檔案新增 MCP servers。`allowedMcpServers` 和 `deniedMcpServers` 設定仍然適用於篩選實際載入的受管理 servers。
</Note>
