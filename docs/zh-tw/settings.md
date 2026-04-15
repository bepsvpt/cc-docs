> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code 設定

> 使用全域和專案層級設定以及環境變數來設定 Claude Code。

Claude Code 提供多種設定選項，可根據您的需求配置其行為。您可以在使用互動式 REPL 時執行 `/config` 命令來設定 Claude Code，這會開啟一個標籤式設定介面，您可以在其中查看狀態資訊並修改設定選項。

## 設定範圍

Claude Code 使用**範圍系統**來決定設定的適用位置和共享對象。了解範圍可幫助您決定如何為個人使用、團隊協作或企業部署設定 Claude Code。

### 可用的範圍

| 範圍          | 位置                                               | 影響對象       | 與團隊共享？        |
| :---------- | :----------------------------------------------- | :--------- | :------------ |
| **Managed** | 伺服器管理的設定、plist / 登錄或系統層級 `managed-settings.json` | 機器上的所有使用者  | 是（由 IT 部署）    |
| **User**    | `~/.claude/` 目錄                                  | 您，跨所有專案    | 否             |
| **Project** | 儲存庫中的 `.claude/`                                 | 此儲存庫的所有協作者 | 是（提交到 git）    |
| **Local**   | `.claude/settings.local.json`                    | 您，僅在此儲存庫中  | 否（gitignored） |

### 何時使用各個範圍

**Managed 範圍**用於：

* 必須在整個組織範圍內強制執行的安全政策
* 無法覆蓋的合規要求
* 由 IT/DevOps 部署的標準化設定

**User 範圍**最適合：

* 您想在任何地方使用的個人偏好設定（主題、編輯器設定）
* 您在所有專案中使用的工具和 plugins
* API 金鑰和身份驗證（安全儲存）

**Project 範圍**最適合：

* 團隊共享的設定（權限、hooks、MCP servers）
* 整個團隊應該擁有的 plugins
* 跨協作者標準化工具

**Local 範圍**最適合：

* 特定專案的個人覆蓋
* 在與團隊共享之前測試設定
* 對其他人不適用的機器特定設定

### 範圍如何互動

當相同的設定在多個範圍中配置時，更具體的範圍優先：

1. **Managed**（最高）- 無法被任何東西覆蓋
2. **命令列引數** - 臨時工作階段覆蓋
3. **Local** - 覆蓋專案和使用者設定
4. **Project** - 覆蓋使用者設定
5. **User**（最低）- 當沒有其他東西指定設定時適用

例如，如果使用者設定中允許某個權限，但專案設定中拒絕該權限，則專案設定優先，該權限被阻止。

### 哪些功能使用範圍

範圍適用於許多 Claude Code 功能：

| 功能              | 使用者位置                     | 專案位置                              | 本機位置                          |
| :-------------- | :------------------------ | :-------------------------------- | :---------------------------- |
| **Settings**    | `~/.claude/settings.json` | `.claude/settings.json`           | `.claude/settings.local.json` |
| **Subagents**   | `~/.claude/agents/`       | `.claude/agents/`                 | 無                             |
| **MCP servers** | `~/.claude.json`          | `.mcp.json`                       | `~/.claude.json`（每個專案）        |
| **Plugins**     | `~/.claude/settings.json` | `.claude/settings.json`           | `.claude/settings.local.json` |
| **CLAUDE.md**   | `~/.claude/CLAUDE.md`     | `CLAUDE.md` 或 `.claude/CLAUDE.md` | 無                             |

***

## 設定檔案

`settings.json` 檔案是透過分層設定來設定 Claude Code 的官方機制：

* **使用者設定**在 `~/.claude/settings.json` 中定義，適用於所有專案。
* **專案設定**儲存在您的專案目錄中：
  * `.claude/settings.json` 用於簽入原始碼控制並與您的團隊共享的設定
  * `.claude/settings.local.json` 用於未簽入的設定，適用於個人偏好和實驗。Claude Code 將在建立時設定 git 以忽略 `.claude/settings.local.json`。
* **Managed 設定**：對於需要集中控制的組織，Claude Code 支援多種 managed 設定的傳遞機制。所有機制都使用相同的 JSON 格式，無法被使用者或專案設定覆蓋：

  * **伺服器管理的設定**：透過 Claude.ai 管理員主控台從 Anthropic 的伺服器傳遞。請參閱[伺服器管理的設定](/zh-TW/server-managed-settings)。
  * **MDM/OS 層級政策**：透過 macOS 和 Windows 上的原生裝置管理傳遞：
    * macOS：`com.anthropic.claudecode` managed preferences 網域（透過 Jamf、Kandji 或其他 MDM 工具中的設定檔案部署）
    * Windows：`HKLM\SOFTWARE\Policies\ClaudeCode` 登錄機碼，其中包含 `Settings` 值（REG\_SZ 或 REG\_EXPAND\_SZ）包含 JSON（透過群組原則或 Intune 部署）
    * Windows（使用者層級）：`HKCU\SOFTWARE\Policies\ClaudeCode`（最低政策優先順序，僅在沒有管理員層級來源時使用）
  * **檔案型**：`managed-settings.json` 和 `managed-mcp.json` 部署到系統目錄：

    * macOS：`/Library/Application Support/ClaudeCode/`
    * Linux 和 WSL：`/etc/claude-code/`
    * Windows：`C:\Program Files\ClaudeCode\`

    <Warning>
      自 v2.1.75 起，舊版 Windows 路徑 `C:\ProgramData\ClaudeCode\managed-settings.json` 不再受支援。已將設定部署到該位置的管理員必須將檔案遷移到 `C:\Program Files\ClaudeCode\managed-settings.json`。
    </Warning>

    檔案型 managed 設定也支援在與 `managed-settings.json` 相同的系統目錄中的 `managed-settings.d/` 放入目錄。這讓不同的團隊可以部署獨立的政策片段，而無需協調對單一檔案的編輯。

    遵循 systemd 慣例，`managed-settings.json` 首先作為基礎合併，然後放入目錄中的所有 `*.json` 檔案按字母順序排序並合併在頂部。對於純量值，後面的檔案會覆蓋前面的檔案；陣列會連接並去重；物件會深度合併。以 `.` 開頭的隱藏檔案會被忽略。

    使用數字前綴來控制合併順序，例如 `10-telemetry.json` 和 `20-security.json`。

  請參閱 [managed 設定](/zh-TW/permissions#managed-only-settings) 和 [Managed MCP 設定](/zh-TW/mcp#managed-mcp-configuration) 以取得詳細資訊。

  <Note>
    Managed 部署也可以使用 `strictKnownMarketplaces` 限制 **plugin marketplace 新增**。如需詳細資訊，請參閱 [Managed marketplace 限制](/zh-TW/plugin-marketplaces#managed-marketplace-restrictions)。
  </Note>
* **其他設定**儲存在 `~/.claude.json` 中。此檔案包含您的偏好設定（主題、通知設定、編輯器模式）、OAuth 工作階段、[MCP server](/zh-TW/mcp) 設定（用於使用者和本機範圍）、每個專案的狀態（允許的工具、信任設定）和各種快取。專案範圍的 MCP servers 分別儲存在 `.mcp.json` 中。

<Note>
  Claude Code 會自動建立設定檔案的時間戳記備份，並保留最近五個備份以防止資料遺失。
</Note>

```JSON 設定檔案範例 theme={null}
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test *)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  },
  "companyAnnouncements": [
    "Welcome to Acme Corp! Review our code guidelines at docs.acme.com",
    "Reminder: Code reviews required for all PRs",
    "New security policy in effect"
  ]
}
```

上面範例中的 `$schema` 行指向 Claude Code 設定的[官方 JSON 架構](https://json.schemastore.org/claude-code-settings.json)。將其新增到您的 `settings.json` 可在 VS Code、Cursor 和任何其他支援 JSON 架構驗證的編輯器中啟用自動完成和內嵌驗證。

### 可用的設定

`settings.json` 支援多個選項：

| 金鑰                                | 說明                                                                                                                                                                                                                                                                            | 範例                                                                                                                            |
| :-------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| `agent`                           | 將主執行緒作為命名 subagent 執行。應用該 subagent 的系統提示、工具限制和模型。請參閱[明確叫用 subagents](/zh-TW/sub-agents#invoke-subagents-explicitly)                                                                                                                                                           | `"code-reviewer"`                                                                                                             |
| `allowedChannelPlugins`           | （Managed 設定僅限）可能推送訊息的頻道 plugins 白名單。在設定時替換預設 Anthropic 白名單。未定義 = 回退到預設值，空陣列 = 阻止所有頻道 plugins。需要 `channelsEnabled: true`。請參閱[限制哪些頻道 plugins 可以執行](/zh-TW/channels#restrict-which-channel-plugins-can-run)                                                                      | `[{ "marketplace": "claude-plugins-official", "plugin": "telegram" }]`                                                        |
| `allowedHttpHookUrls`             | HTTP hooks 可能針對的 URL 模式白名單。支援 `*` 作為萬用字元。設定時，具有不匹配 URL 的 hooks 會被阻止。未定義 = 無限制，空陣列 = 阻止所有 HTTP hooks。陣列跨設定來源合併。請參閱 [Hook 設定](#hook-configuration)                                                                                                                              | `["https://hooks.example.com/*"]`                                                                                             |
| `allowedMcpServers`               | 在 managed-settings.json 中設定時，使用者可以設定的 MCP servers 白名單。未定義 = 無限制，空陣列 = 鎖定。適用於所有範圍。拒絕清單優先。請參閱 [Managed MCP 設定](/zh-TW/mcp#managed-mcp-configuration)                                                                                                                            | `[{ "serverName": "github" }]`                                                                                                |
| `allowManagedHooksOnly`           | （Managed 設定僅限）防止載入使用者、專案和 plugin hooks。僅允許 managed hooks 和 SDK hooks。請參閱 [Hook 設定](#hook-configuration)                                                                                                                                                                       | `true`                                                                                                                        |
| `allowManagedMcpServersOnly`      | （Managed 設定僅限）僅尊重 managed 設定中的 `allowedMcpServers`。`deniedMcpServers` 仍從所有來源合併。使用者仍可新增 MCP servers，但僅適用管理員定義的白名單。請參閱 [Managed MCP 設定](/zh-TW/mcp#managed-mcp-configuration)                                                                                                   | `true`                                                                                                                        |
| `allowManagedPermissionRulesOnly` | （Managed 設定僅限）防止使用者和專案設定定義 `allow`、`ask` 或 `deny` 權限規則。僅適用 managed 設定中的規則。請參閱 [Managed 專用設定](/zh-TW/permissions#managed-only-settings)                                                                                                                                        | `true`                                                                                                                        |
| `alwaysThinkingEnabled`           | 為所有工作階段預設啟用[擴展思考](/zh-TW/common-workflows#use-extended-thinking-thinking-mode)。通常透過 `/config` 命令而不是直接編輯來設定                                                                                                                                                                    | `true`                                                                                                                        |
| `apiKeyHelper`                    | 自訂指令碼，在 `/bin/sh` 中執行，以產生驗證值。此值將作為 `X-Api-Key` 和 `Authorization: Bearer` 標頭傳送以進行模型請求                                                                                                                                                                                          | `/bin/generate_temp_api_key.sh`                                                                                               |
| `attribution`                     | 自訂 git 提交和拉取請求的歸屬。請參閱[歸屬設定](#attribution-settings)                                                                                                                                                                                                                            | `{"commit": "🤖 Generated with Claude Code", "pr": ""}`                                                                       |
| `autoMemoryDirectory`             | [自動記憶](/zh-TW/memory#storage-location)儲存的自訂目錄。接受 `~/` 展開的路徑。不在專案設定（`.claude/settings.json`）中接受，以防止共享儲存庫將記憶寫入重定向到敏感位置。從政策、本機和使用者設定接受                                                                                                                                           | `"~/my-memory-dir"`                                                                                                           |
| `autoMode`                        | 自訂[自動模式](/zh-TW/permission-modes#eliminate-prompts-with-auto-mode)分類器阻止和允許的內容。包含 `environment`、`allow` 和 `soft_deny` 陣列的散文規則。請參閱[設定自動模式分類器](/zh-TW/permissions#configure-the-auto-mode-classifier)。不從共享專案設定讀取                                                                 | `{"environment": ["Trusted repo: github.example.com/acme"]}`                                                                  |
| `autoUpdatesChannel`              | 遵循更新的發行頻道。使用 `"stable"` 以取得通常約一週舊的版本並跳過有重大迴歸的版本，或 `"latest"`（預設）以取得最新版本                                                                                                                                                                                                       | `"stable"`                                                                                                                    |
| `availableModels`                 | 限制使用者可透過 `/model`、`--model`、Config 工具或 `ANTHROPIC_MODEL` 選擇的模型。不影響預設選項。請參閱[限制模型選擇](/zh-TW/model-config#restrict-model-selection)                                                                                                                                              | `["sonnet", "haiku"]`                                                                                                         |
| `awsAuthRefresh`                  | 修改 `.aws` 目錄的自訂指令碼（請參閱[進階認證設定](/zh-TW/amazon-bedrock#advanced-credential-configuration)）                                                                                                                                                                                      | `aws sso login --profile myprofile`                                                                                           |
| `awsCredentialExport`             | 輸出包含 AWS 認證的 JSON 的自訂指令碼（請參閱[進階認證設定](/zh-TW/amazon-bedrock#advanced-credential-configuration)）                                                                                                                                                                                | `/bin/generate_aws_grant.sh`                                                                                                  |
| `blockedMarketplaces`             | （Managed 設定僅限）marketplace 來源的黑名單。在下載前檢查被阻止的來源，因此它們永遠不會接觸檔案系統。請參閱 [Managed marketplace 限制](/zh-TW/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                        | `[{ "source": "github", "repo": "untrusted/plugins" }]`                                                                       |
| `channelsEnabled`                 | （Managed 設定僅限）允許 Team 和 Enterprise 使用者使用[頻道](/zh-TW/channels)。未設定或 `false` 會阻止頻道訊息傳遞，無論使用者傳遞什麼給 `--channels`                                                                                                                                                                  | `true`                                                                                                                        |
| `cleanupPeriodDays`               | 非使用中超過此期間的工作階段在啟動時刪除（預設：30 天，最少 1 天）。設定為 `0` 會被拒絕並出現驗證錯誤。若要在非互動模式（`-p`）中完全停用文字記錄寫入，請使用 `--no-session-persistence` 旗標或 `persistSession: false` SDK 選項；沒有互動模式的等效項。                                                                                                              | `20`                                                                                                                          |
| `companyAnnouncements`            | 在啟動時向使用者顯示的公告。如果提供多個公告，它們將隨機循環。                                                                                                                                                                                                                                               | `["Welcome to Acme Corp! Review our code guidelines at docs.acme.com"]`                                                       |
| `defaultShell`                    | 輸入框 `!` 命令的預設 shell。接受 `"bash"`（預設）或 `"powershell"`。設定 `"powershell"` 會在 Windows 上透過 PowerShell 路由互動式 `!` 命令。需要 `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`。請參閱 [PowerShell tool](/zh-TW/tools-reference#powershell-tool)                                                             | `"powershell"`                                                                                                                |
| `deniedMcpServers`                | 在 managed-settings.json 中設定時，明確阻止的 MCP servers 拒絕清單。適用於所有範圍，包括 managed servers。拒絕清單優先於白名單。請參閱 [Managed MCP 設定](/zh-TW/mcp#managed-mcp-configuration)                                                                                                                          | `[{ "serverName": "filesystem" }]`                                                                                            |
| `disableAllHooks`                 | 停用所有 [hooks](/zh-TW/hooks) 和任何自訂[狀態行](/zh-TW/statusline)                                                                                                                                                                                                                      | `true`                                                                                                                        |
| `disableAutoMode`                 | 設定為 `"disable"` 以防止[自動模式](/zh-TW/permission-modes#eliminate-prompts-with-auto-mode)被啟用。從 `Shift+Tab` 循環中移除 `auto` 並在啟動時拒絕 `--permission-mode auto`。在[managed 設定](/zh-TW/permissions#managed-settings)中最有用，使用者無法覆蓋它                                                            | `"disable"`                                                                                                                   |
| `disableDeepLinkRegistration`     | 設定為 `"disable"` 以防止 Claude Code 在啟動時向作業系統註冊 `claude-cli://` 協議處理程式。深層連結讓外部工具透過 `claude-cli://open?q=...` 以預先填入的提示開啟 Claude Code 工作階段。在協議處理程式註冊受限或單獨管理的環境中很有用                                                                                                                  | `"disable"`                                                                                                                   |
| `disabledMcpjsonServers`          | 要拒絕的 `.mcp.json` 檔案中特定 MCP servers 的清單                                                                                                                                                                                                                                        | `["filesystem"]`                                                                                                              |
| `effortLevel`                     | 跨工作階段持久化[努力等級](/zh-TW/model-config#adjust-effort-level)。接受 `"low"`、`"medium"` 或 `"high"`。當您執行 `/effort low`、`/effort medium` 或 `/effort high` 時自動寫入。在 Opus 4.6 和 Sonnet 4.6 上支援                                                                                               | `"medium"`                                                                                                                    |
| `enableAllProjectMcpServers`      | 自動批准專案 `.mcp.json` 檔案中定義的所有 MCP servers                                                                                                                                                                                                                                       | `true`                                                                                                                        |
| `enabledMcpjsonServers`           | 要批准的 `.mcp.json` 檔案中特定 MCP servers 的清單                                                                                                                                                                                                                                        | `["memory", "github"]`                                                                                                        |
| `env`                             | 將應用於每個工作階段的環境變數                                                                                                                                                                                                                                                               | `{"FOO": "bar"}`                                                                                                              |
| `fastModePerSessionOptIn`         | 當為 `true` 時，快速模式不會跨工作階段持久化。每個工作階段都以快速模式關閉開始，需要使用者使用 `/fast` 啟用它。使用者的快速模式偏好仍會儲存。請參閱[需要每個工作階段的選擇加入](/zh-TW/fast-mode#require-per-session-opt-in)                                                                                                                                | `true`                                                                                                                        |
| `feedbackSurveyRate`              | [工作階段品質調查](/zh-TW/data-usage#session-quality-surveys)出現時符合條件的機率（0–1）。設定為 `0` 以完全抑制。在使用 Bedrock、Vertex 或 Foundry 時很有用，其中預設樣本率不適用                                                                                                                                               | `0.05`                                                                                                                        |
| `fileSuggestion`                  | 為 `@` 檔案自動完成設定自訂指令碼。請參閱[檔案建議設定](#file-suggestion-settings)                                                                                                                                                                                                                    | `{"type": "command", "command": "~/.claude/file-suggestion.sh"}`                                                              |
| `forceLoginMethod`                | 使用 `claudeai` 限制登入到 Claude.ai 帳戶，`console` 限制登入到 Claude Console（API 使用計費）帳戶                                                                                                                                                                                                   | `claudeai`                                                                                                                    |
| `forceLoginOrgUUID`               | 要求登入屬於特定組織。接受單一 UUID 字串（也會在登入期間預先選擇該組織），或 UUID 陣列，其中接受任何列出的組織而不預先選擇。在 managed 設定中設定時，如果驗證帳戶不屬於列出的組織，登入會失敗；空陣列會失敗關閉並使用誤設定訊息阻止登入                                                                                                                                                | `"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"` 或 `["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"]` |
| `hooks`                           | 設定自訂命令以在生命週期事件執行。請參閱 [hooks 文件](/zh-TW/hooks)以了解格式                                                                                                                                                                                                                            | 請參閱 [hooks](/zh-TW/hooks)                                                                                                     |
| `httpHookAllowedEnvVars`          | HTTP hooks 可能插入到標頭中的環境變數名稱白名單。設定時，每個 hook 的有效 `allowedEnvVars` 是與此清單的交集。未定義 = 無限制。陣列跨設定來源合併。請參閱 [Hook 設定](#hook-configuration)                                                                                                                                                | `["MY_TOKEN", "HOOK_SECRET"]`                                                                                                 |
| `includeCoAuthoredBy`             | **已棄用**：改用 `attribution`。是否在 git 提交和拉取請求中包含 `co-authored-by Claude` 署名（預設：`true`）                                                                                                                                                                                             | `false`                                                                                                                       |
| `includeGitInstructions`          | 在 Claude 的系統提示中包含內建提交和 PR 工作流程指示和 git 狀態快照（預設：`true`）。設定為 `false` 以移除兩者，例如在使用您自己的 git 工作流程 skills 時。`CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` 環境變數在設定時優先於此設定                                                                                                                     | `false`                                                                                                                       |
| `language`                        | 設定 Claude 的首選回應語言（例如 `"japanese"`、`"spanish"`、`"french"`）。Claude 預設會以此語言回應。也設定[語音聽寫](/zh-TW/voice-dictation#change-the-dictation-language)語言                                                                                                                                  | `"japanese"`                                                                                                                  |
| `model`                           | 覆蓋 Claude Code 使用的預設模型                                                                                                                                                                                                                                                        | `"claude-sonnet-4-6"`                                                                                                         |
| `modelOverrides`                  | 將 Anthropic 模型 ID 對應到提供者特定的模型 ID，例如 Bedrock 推論設定檔 ARN。每個模型選擇器項目在呼叫提供者 API 時使用其對應的值。請參閱[按版本覆蓋模型 ID](/zh-TW/model-config#override-model-ids-per-version)                                                                                                                        | `{"claude-opus-4-6": "arn:aws:bedrock:..."}`                                                                                  |
| `otelHeadersHelper`               | 產生動態 OpenTelemetry 標頭的指令碼。在啟動時和定期執行（請參閱[動態標頭](/zh-TW/monitoring-usage#dynamic-headers)）                                                                                                                                                                                       | `/bin/generate_otel_headers.sh`                                                                                               |
| `outputStyle`                     | 設定輸出樣式以調整系統提示。請參閱[輸出樣式文件](/zh-TW/output-styles)                                                                                                                                                                                                                               | `"Explanatory"`                                                                                                               |
| `permissions`                     | 請參閱下表以了解權限的結構。                                                                                                                                                                                                                                                                |                                                                                                                               |
| `plansDirectory`                  | 自訂計畫檔案的儲存位置。路徑相對於專案根目錄。預設：`~/.claude/plans`                                                                                                                                                                                                                                   | `"./plans"`                                                                                                                   |
| `pluginTrustMessage`              | （Managed 設定僅限）在安裝前顯示的 plugin 信任警告中附加的自訂訊息。使用此選項新增組織特定的內容，例如確認來自您內部 marketplace 的 plugins 已經過審查。                                                                                                                                                                               | `"All plugins from our marketplace are approved by IT"`                                                                       |
| `prefersReducedMotion`            | 減少或停用 UI 動畫（微調器、閃爍、閃光效果）以提高可訪問性                                                                                                                                                                                                                                               | `true`                                                                                                                        |
| `respectGitignore`                | 控制 `@` 檔案選擇器是否尊重 `.gitignore` 模式。當為 `true`（預設）時，符合 `.gitignore` 模式的檔案會從建議中排除                                                                                                                                                                                                  | `false`                                                                                                                       |
| `showClearContextOnPlanAccept`    | 在計畫接受畫面上顯示「清除內容」選項。預設為 `false`。設定為 `true` 以還原選項                                                                                                                                                                                                                               | `true`                                                                                                                        |
| `showThinkingSummaries`           | 在互動式工作階段中顯示[擴展思考](/zh-TW/common-workflows#use-extended-thinking-thinking-mode)摘要。未設定或 `false`（互動模式中的預設值）時，思考區塊由 API 編輯並顯示為摺疊的存根。編輯只會改變您看到的內容，而不是模型生成的內容：若要減少思考支出，請[降低預算或停用思考](/zh-TW/common-workflows#use-extended-thinking-thinking-mode)。非互動模式（`-p`）和 SDK 呼叫者無論此設定如何都始終接收摘要 | `true`                                                                                                                        |
| `spinnerTipsEnabled`              | 在 Claude 工作時在微調器中顯示提示。設定為 `false` 以停用提示（預設：`true`）                                                                                                                                                                                                                            | `false`                                                                                                                       |
| `spinnerTipsOverride`             | 使用自訂字串覆蓋微調器提示。`tips`：提示字串陣列。`excludeDefault`：如果為 `true`，僅顯示自訂提示；如果為 `false` 或不存在，自訂提示會與內建提示合併                                                                                                                                                                                 | `{ "excludeDefault": true, "tips": ["Use our internal tool X"] }`                                                             |
| `spinnerVerbs`                    | 自訂在微調器和輪次持續時間訊息中顯示的動作動詞。將 `mode` 設定為 `"replace"` 以僅使用您的動詞，或 `"append"` 以將它們新增到預設值                                                                                                                                                                                             | `{"mode": "append", "verbs": ["Pondering", "Crafting"]}`                                                                      |
| `statusLine`                      | 設定自訂狀態行以顯示內容。請參閱 [`statusLine` 文件](/zh-TW/statusline)                                                                                                                                                                                                                         | `{"type": "command", "command": "~/.claude/statusline.sh"}`                                                                   |
| `strictKnownMarketplaces`         | （Managed 設定僅限）使用者可以新增的 plugin marketplaces 白名單。未定義 = 無限制，空陣列 = 鎖定。僅適用於 marketplace 新增。請參閱 [Managed marketplace 限制](/zh-TW/plugin-marketplaces#managed-marketplace-restrictions)                                                                                               | `[{ "source": "github", "repo": "acme-corp/plugins" }]`                                                                       |
| `useAutoModeDuringPlan`           | Plan Mode 在自動模式可用時是否使用自動模式語義。預設：`true`。不從共享專案設定讀取。在 `/config` 中顯示為「在計畫期間使用自動模式」                                                                                                                                                                                               | `false`                                                                                                                       |
| `voiceEnabled`                    | 啟用推送說話[語音聽寫](/zh-TW/voice-dictation)。當您執行 `/voice` 時自動寫入。需要 Claude.ai 帳戶                                                                                                                                                                                                      | `true`                                                                                                                        |

### 全域設定設定

這些設定儲存在 `~/.claude.json` 中，而不是 `settings.json`。將它們新增到 `settings.json` 將觸發架構驗證錯誤。

| 金鑰                           | 說明                                                                                                                                                                                    | 範例             |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------- |
| `autoConnectIde`             | 當 Claude Code 從外部終端機啟動時自動連線到執行中的 IDE。預設：`false`。在 VS Code 或 JetBrains 終端機外執行時在 `/config` 中顯示為**自動連線到 IDE（外部終端機）**                                                                     | `true`         |
| `autoInstallIdeExtension`    | 從 VS Code 終端機執行時自動安裝 Claude Code IDE 擴充功能。預設：`true`。在 VS Code 或 JetBrains 終端機內執行時在 `/config` 中顯示為**自動安裝 IDE 擴充功能**。您也可以設定 [`CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`](/zh-TW/env-vars) 環境變數 | `false`        |
| `editorMode`                 | 輸入提示的快捷鍵模式：`"normal"` 或 `"vim"`。預設：`"normal"`。當您執行 `/vim` 時自動寫入。在 `/config` 中顯示為**快捷鍵模式**                                                                                             | `"vim"`        |
| `showTurnDuration`           | 在回應後顯示輪次持續時間訊息，例如「Cooked for 1m 6s」。預設：`true`。在 `/config` 中顯示為**顯示輪次持續時間**                                                                                                            | `false`        |
| `terminalProgressBarEnabled` | 在支援的終端機中顯示終端機進度條：ConEmu、Ghostty 1.2.0+ 和 iTerm2 3.6.6+。預設：`true`。在 `/config` 中顯示為**終端機進度條**                                                                                           | `false`        |
| `teammateMode`               | [agent team](/zh-TW/agent-teams) 隊友的顯示方式：`auto`（在 tmux 或 iTerm2 中選擇分割窗格，否則為進程內）、`in-process` 或 `tmux`。請參閱[選擇顯示模式](/zh-TW/agent-teams#choose-a-display-mode)                           | `"in-process"` |

### Worktree 設定

設定 `--worktree` 如何建立和管理 git worktrees。使用這些設定來減少大型 monorepos 中的磁碟使用量和啟動時間。

| 金鑰                            | 說明                                                                                  | 範例                                    |
| :---------------------------- | :---------------------------------------------------------------------------------- | :------------------------------------ |
| `worktree.symlinkDirectories` | 要從主儲存庫符號連結到每個 worktree 的目錄，以避免在磁碟上複製大型目錄。預設不符號連結任何目錄                                | `["node_modules", ".cache"]`          |
| `worktree.sparsePaths`        | 要在每個 worktree 中透過 git sparse-checkout（cone 模式）簽出的目錄。僅將列出的路徑寫入磁碟，在大型 monorepos 中速度更快 | `["packages/my-app", "shared/utils"]` |

若要將 gitignored 檔案（如 `.env`）複製到新的 worktrees，請改用專案根目錄中的 [`.worktreeinclude` 檔案](/zh-TW/common-workflows#copy-gitignored-files-to-worktrees)，而不是設定。

### 權限設定

| 金鑰                                  | 說明                                                                                                                                                                      | 範例                                                                     |
| :---------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `allow`                             | 允許工具使用的權限規則陣列。請參閱下面的[權限規則語法](#permission-rule-syntax)以了解模式匹配詳細資訊                                                                                                        | `[ "Bash(git diff *)" ]`                                               |
| `ask`                               | 要求在工具使用時確認的權限規則陣列。請參閱下面的[權限規則語法](#permission-rule-syntax)                                                                                                               | `[ "Bash(git push *)" ]`                                               |
| `deny`                              | 拒絕工具使用的權限規則陣列。使用此選項從 Claude Code 存取中排除敏感檔案。請參閱[權限規則語法](#permission-rule-syntax)和 [Bash 權限限制](/zh-TW/permissions#tool-specific-permission-rules)                         | `[ "WebFetch", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)" ]` |
| `additionalDirectories`             | Claude 有權存取的其他[工作目錄](/zh-TW/permissions#working-directories)。大多數 `.claude/` 設定[未從這些目錄發現](/zh-TW/permissions#additional-directories-grant-file-access-not-configuration) | `[ "../docs/" ]`                                                       |
| `defaultMode`                       | 開啟 Claude Code 時的預設[權限模式](/zh-TW/permission-modes)。有效值：`default`、`acceptEdits`、`plan`、`auto`、`dontAsk`、`bypassPermissions`。`--permission-mode` CLI 旗標會覆蓋此設定以進行單一工作階段    | `"acceptEdits"`                                                        |
| `disableBypassPermissionsMode`      | 設定為 `"disable"` 以防止啟用 `bypassPermissions` 模式。這會停用 `--dangerously-skip-permissions` 旗標。在[managed 設定](/zh-TW/permissions#managed-settings)中最有用，使用者無法覆蓋它                   | `"disable"`                                                            |
| `skipDangerousModePermissionPrompt` | 跳過透過 `--dangerously-skip-permissions` 或 `defaultMode: "bypassPermissions"` 進入 bypass permissions 模式之前顯示的確認提示。在專案設定（`.claude/settings.json`）中設定時被忽略，以防止不受信任的儲存庫自動繞過提示    | `true`                                                                 |

### 權限規則語法

權限規則遵循 `Tool` 或 `Tool(specifier)` 的格式。規則按順序評估：首先是拒絕規則，然後是詢問，最後是允許。第一個匹配的規則獲勝。

快速範例：

| 規則                             | 效果                    |
| :----------------------------- | :-------------------- |
| `Bash`                         | 符合所有 Bash 命令          |
| `Bash(npm run *)`              | 符合以 `npm run` 開頭的命令   |
| `Read(./.env)`                 | 符合讀取 `.env` 檔案        |
| `WebFetch(domain:example.com)` | 符合對 example.com 的擷取請求 |

如需完整的規則語法參考，包括萬用字元行為、Read、Edit、WebFetch、MCP 和 Agent 規則的工具特定模式，以及 Bash 模式的安全限制，請參閱[權限規則語法](/zh-TW/permissions#permission-rule-syntax)。

### Sandbox 設定

設定進階 sandboxing 行為。Sandboxing 將 bash 命令與您的檔案系統和網路隔離。請參閱 [Sandboxing](/zh-TW/sandboxing) 以了解詳細資訊。

| 金鑰                                     | 說明                                                                                                                                                                                   | 範例                              |
| :------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------ |
| `enabled`                              | 啟用 bash sandboxing（macOS、Linux 和 WSL2）。預設：false                                                                                                                                      | `true`                          |
| `failIfUnavailable`                    | 如果 `sandbox.enabled` 為 true 但 sandbox 無法啟動（遺失相依性、不支援的平台或平台限制），則在啟動時以錯誤結束。當為 false（預設）時，會顯示警告，命令會以 unsandboxed 方式執行。適用於需要 sandboxing 作為硬閘門的 managed 設定部署                              | `true`                          |
| `autoAllowBashIfSandboxed`             | 在 sandboxed 時自動批准 bash 命令。預設：true                                                                                                                                                    | `true`                          |
| `excludedCommands`                     | 應在 sandbox 外執行的命令                                                                                                                                                                    | `["git", "docker"]`             |
| `allowUnsandboxedCommands`             | 允許命令透過 `dangerouslyDisableSandbox` 參數在 sandbox 外執行。當設定為 `false` 時，`dangerouslyDisableSandbox` 逃脫艙口完全停用，所有命令必須 sandboxed（或在 `excludedCommands` 中）。適用於需要嚴格 sandboxing 的企業政策。預設：true    | `false`                         |
| `filesystem.allowWrite`                | sandboxed 命令可以寫入的其他路徑。陣列跨所有設定範圍合併：使用者、專案和 managed 路徑合併，不替換。也與 `Edit(...)` 允許權限規則中的路徑合併。請參閱下面的[路徑前綴](#sandbox-path-prefixes)。                                                         | `["/tmp/build", "~/.kube"]`     |
| `filesystem.denyWrite`                 | sandboxed 命令無法寫入的路徑。陣列跨所有設定範圍合併。也與 `Edit(...)` 拒絕權限規則中的路徑合併。                                                                                                                         | `["/etc", "/usr/local/bin"]`    |
| `filesystem.denyRead`                  | sandboxed 命令無法讀取的路徑。陣列跨所有設定範圍合併。也與 `Read(...)` 拒絕權限規則中的路徑合併。                                                                                                                         | `["~/.aws/credentials"]`        |
| `filesystem.allowRead`                 | 在 `denyRead` 區域內重新允許讀取的路徑。優先於 `denyRead`。陣列跨所有設定範圍合併。使用此選項建立僅工作區讀取存取模式。                                                                                                              | `["."]`                         |
| `filesystem.allowManagedReadPathsOnly` | （Managed 設定僅限）僅尊重 managed 設定中的 `filesystem.allowRead` 路徑。`denyRead` 仍從所有來源合併。預設：false                                                                                                | `true`                          |
| `network.allowUnixSockets`             | sandbox 中可存取的 Unix socket 路徑（用於 SSH 代理等）                                                                                                                                             | `["~/.ssh/agent-socket"]`       |
| `network.allowAllUnixSockets`          | 允許 sandbox 中的所有 Unix socket 連線。預設：false                                                                                                                                              | `true`                          |
| `network.allowLocalBinding`            | 允許繫結到 localhost 連接埠（僅限 macOS）。預設：false                                                                                                                                               | `true`                          |
| `network.allowedDomains`               | 允許出站網路流量的網域陣列。支援萬用字元（例如 `*.example.com`）。                                                                                                                                            | `["github.com", "*.npmjs.org"]` |
| `network.allowManagedDomainsOnly`      | （Managed 設定僅限）僅尊重 managed 設定中的 `allowedDomains` 和 `WebFetch(domain:...)` 允許規則。來自使用者、專案和本機設定的網域會被忽略。非允許的網域會自動阻止，不會提示使用者。拒絕的網域仍從所有來源受尊重。預設：false                                       | `true`                          |
| `network.httpProxyPort`                | 如果您想帶上自己的代理，使用的 HTTP 代理連接埠。如果未指定，Claude 將執行自己的代理。                                                                                                                                    | `8080`                          |
| `network.socksProxyPort`               | 如果您想帶上自己的代理，使用的 SOCKS5 代理連接埠。如果未指定，Claude 將執行自己的代理。                                                                                                                                  | `8081`                          |
| `enableWeakerNestedSandbox`            | 為無特權 Docker 環境啟用較弱的 sandbox（僅限 Linux 和 WSL2）。**降低安全性。** 預設：false                                                                                                                     | `true`                          |
| `enableWeakerNetworkIsolation`         | （僅限 macOS）允許在 sandbox 中存取系統 TLS 信任服務（`com.apple.trustd.agent`）。使用 `httpProxyPort` 和自訂 CA 的 MITM 代理時，Go 型工具（如 `gh`、`gcloud` 和 `terraform`）需要驗證 TLS 憑證。**透過開啟潛在的資料外洩路徑降低安全性**。預設：false | `true`                          |

#### Sandbox 路徑前綴

`filesystem.allowWrite`、`filesystem.denyWrite`、`filesystem.denyRead` 和 `filesystem.allowRead` 中的路徑支援這些前綴：

| 前綴        | 含義                                        | 範例                                                                |
| :-------- | :---------------------------------------- | :---------------------------------------------------------------- |
| `/`       | 從檔案系統根目錄的絕對路徑                             | `/tmp/build` 保持 `/tmp/build`                                      |
| `~/`      | 相對於主目錄                                    | `~/.kube` 變成 `$HOME/.kube`                                        |
| `./` 或無前綴 | 相對於專案根目錄（用於專案設定）或相對於 `~/.claude`（用於使用者設定） | `./output` 在 `.claude/settings.json` 中解析為 `<project-root>/output` |

較舊的 `//path` 前綴用於絕對路徑仍然有效。如果您之前使用單斜線 `/path` 期望專案相對解析，請切換到 `./path`。此語法與[讀取和編輯權限規則](/zh-TW/permissions#read-and-edit)不同，後者使用 `//path` 用於絕對和 `/path` 用於專案相對。Sandbox 檔案系統路徑使用標準慣例：`/tmp/build` 是絕對路徑。

**設定範例：**

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker"],
    "filesystem": {
      "allowWrite": ["/tmp/build", "~/.kube"],
      "denyRead": ["~/.aws/credentials"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org", "registry.yarnpkg.com"],
      "allowUnixSockets": [
        "/var/run/docker.sock"
      ],
      "allowLocalBinding": true
    }
  }
}
```

**檔案系統和網路限制**可以透過兩種合併在一起的方式設定：

* **`sandbox.filesystem` 設定**（如上所示）：在 OS 層級 sandbox 邊界控制路徑。這些限制適用於所有子流程命令（例如 `kubectl`、`terraform`、`npm`），而不僅僅是 Claude 的檔案工具。
* **權限規則**：使用 `Edit` 允許/拒絕規則控制 Claude 的檔案工具存取，`Read` 拒絕規則阻止讀取，`WebFetch` 允許/拒絕規則控制網路網域。這些規則中的路徑也會合併到 sandbox 設定中。

### 歸屬設定

Claude Code 將歸屬新增到 git 提交和拉取請求。這些分別設定：

* 提交預設使用 [git trailers](https://git-scm.com/docs/git-interpret-trailers)（如 `Co-Authored-By`），可以自訂或停用
* 拉取請求說明是純文字

| 金鑰       | 說明                                |
| :------- | :-------------------------------- |
| `commit` | git 提交的歸屬，包括任何 trailers。空字串隱藏提交歸屬 |
| `pr`     | 拉取請求說明的歸屬。空字串隱藏拉取請求歸屬             |

**預設提交歸屬：**

```text theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**預設拉取請求歸屬：**

```text theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**範例：**

```json theme={null}
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": ""
  }
}
```

<Note>
  `attribution` 設定優先於已棄用的 `includeCoAuthoredBy` 設定。若要隱藏所有歸屬，請將 `commit` 和 `pr` 設定為空字串。
</Note>

### 檔案建議設定

為 `@` 檔案路徑自動完成設定自訂命令。內建檔案建議使用快速檔案系統遍歷，但大型 monorepos 可能受益於專案特定的索引，例如預先建立的檔案索引或自訂工具。

```json theme={null}
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

該命令使用與 [hooks](/zh-TW/hooks) 相同的環境變數執行，包括 `CLAUDE_PROJECT_DIR`。它透過 stdin 接收包含 `query` 欄位的 JSON：

```json theme={null}
{"query": "src/comp"}
```

將換行符分隔的檔案路徑輸出到 stdout（目前限制為 15）：

```text theme={null}
src/components/Button.tsx
src/components/Modal.tsx
src/components/Form.tsx
```

**範例：**

```bash theme={null}
#!/bin/bash
query=$(cat | jq -r '.query')
your-repo-file-index --query "$query" | head -20
```

### Hook 設定

這些設定控制允許執行哪些 hooks 以及 HTTP hooks 可以存取的內容。`allowManagedHooksOnly` 設定只能在 [managed 設定](#settings-files)中設定。URL 和環境變數白名單可以在任何設定層級設定，並跨來源合併。

**當 `allowManagedHooksOnly` 為 `true` 時的行為：**

* 載入 Managed hooks 和 SDK hooks
* 使用者 hooks、專案 hooks 和 plugin hooks 被阻止

**限制 HTTP hook URL：**

限制 HTTP hooks 可以針對的 URL。支援 `*` 作為匹配的萬用字元。定義陣列時，針對不匹配 URL 的 HTTP hooks 會被無聲地阻止。

```json theme={null}
{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}
```

**限制 HTTP hook 環境變數：**

限制 HTTP hooks 可以插入到標頭值中的環境變數名稱。每個 hook 的有效 `allowedEnvVars` 是其自己清單與此設定的交集。

```json theme={null}
{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}
```

### 設定優先順序

設定按優先順序順序應用。從最高到最低：

1. **Managed 設定**（[伺服器管理](/zh-TW/server-managed-settings)、[MDM/OS 層級政策](#configuration-scopes)或 [managed 設定](/zh-TW/settings#settings-files)）
   * 由 IT 透過伺服器傳遞、MDM 設定檔案、登錄政策或 managed 設定檔案部署的政策
   * 無法被任何其他層級覆蓋，包括命令列引數
   * 在 managed 層級內，優先順序為：伺服器管理 > MDM/OS 層級政策 > 檔案型（`managed-settings.d/*.json` + `managed-settings.json`）> HKCU 登錄（僅限 Windows）。僅使用一個 managed 來源；來源不合併跨層級。在檔案型層級內，放入檔案和基礎檔案會合併在一起。

2. **命令列引數**
   * 特定工作階段的臨時覆蓋

3. **本機專案設定**（`.claude/settings.local.json`）
   * 個人專案特定設定

4. **共享專案設定**（`.claude/settings.json`）
   * 原始碼控制中的團隊共享專案設定

5. **使用者設定**（`~/.claude/settings.json`）
   * 個人全域設定

此階層確保組織政策始終被強制執行，同時仍允許團隊和個人自訂其體驗。無論您從 CLI、[VS Code 擴充功能](/zh-TW/vs-code)或 [JetBrains IDE](/zh-TW/jetbrains) 執行 Claude Code，相同的優先順序都適用。

例如，如果您的使用者設定允許 `Bash(npm run *)`，但專案的共享設定拒絕它，則專案設定優先，命令被阻止。

<Note>
  **陣列設定跨範圍合併。** 當相同的陣列值設定（例如 `sandbox.filesystem.allowWrite` 或 `permissions.allow`）出現在多個範圍中時，陣列會**連接和去重**，而不是替換。這意味著較低優先順序的範圍可以新增項目而不覆蓋由較高優先順序範圍設定的項目，反之亦然。例如，如果 managed 設定將 `allowWrite` 設定為 `["/opt/company-tools"]`，使用者新增 `["~/.kube"]`，則最終設定中包含兩個路徑。
</Note>

### 驗證使用中的設定

在 Claude Code 內執行 `/status` 以查看哪些設定來源處於使用中以及它們來自何處。輸出顯示每個設定層（managed、使用者、專案）及其來源，例如 `Enterprise managed settings (remote)`、`Enterprise managed settings (plist)`、`Enterprise managed settings (HKLM)` 或 `Enterprise managed settings (file)`。如果設定檔案包含錯誤，`/status` 會報告問題，以便您可以修復它。

### 設定系統的關鍵要點

* **記憶檔案（`CLAUDE.md`）**：包含 Claude 在啟動時載入的指示和內容
* **設定檔案（JSON）**：設定權限、環境變數和工具行為
* **Skills**：可以使用 `/skill-name` 叫用或由 Claude 自動載入的自訂提示
* **MCP servers**：使用其他工具和整合擴展 Claude Code
* **優先順序**：較高層級的設定（Managed）覆蓋較低層級的設定（User/Project）
* **繼承**：設定會合併，更具體的設定新增到或覆蓋更廣泛的設定

### 系統提示

Claude Code 的內部系統提示未發佈。若要新增自訂指示，請使用 `CLAUDE.md` 檔案或 `--append-system-prompt` 旗標。

### 排除敏感檔案

若要防止 Claude Code 存取包含敏感資訊（如 API 金鑰、機密和環境檔案）的檔案，請在您的 `.claude/settings.json` 檔案中使用 `permissions.deny` 設定：

```json theme={null}
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Read(./build)"
    ]
  }
}
```

這取代了已棄用的 `ignorePatterns` 設定。符合這些模式的檔案會從檔案發現和搜尋結果中排除，並拒絕對這些檔案的讀取操作。

## Subagent 設定

Claude Code 支援可在使用者和專案層級設定的自訂 AI subagents。這些 subagents 儲存為具有 YAML frontmatter 的 Markdown 檔案：

* **使用者 subagents**：`~/.claude/agents/` - 在所有專案中可用
* **專案 subagents**：`.claude/agents/` - 特定於您的專案，可與您的團隊共享

Subagent 檔案定義具有自訂提示和工具權限的專門 AI 助手。在 [subagents 文件](/zh-TW/sub-agents)中深入了解建立和使用 subagents。

## Plugin 設定

Claude Code 支援 plugin 系統，可讓您使用 skills、agents、hooks 和 MCP servers 擴展功能。Plugins 透過 marketplaces 分發，可以在使用者和儲存庫層級設定。

### Plugin 設定

`settings.json` 中的 plugin 相關設定：

```json theme={null}
{
  "enabledPlugins": {
    "formatter@acme-tools": true,
    "deployer@acme-tools": true,
    "analyzer@security-plugins": false
  },
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": "github",
      "repo": "acme-corp/claude-plugins"
    }
  }
}
```

#### `enabledPlugins`

控制啟用哪些 plugins。格式：`"plugin-name@marketplace-name": true/false`

**範圍**：

* **使用者設定**（`~/.claude/settings.json`）：個人 plugin 偏好設定
* **專案設定**（`.claude/settings.json`）：與團隊共享的專案特定 plugins
* **本機設定**（`.claude/settings.local.json`）：每台機器的覆蓋（未提交）
* **Managed 設定**（`managed-settings.json`）：組織範圍的政策覆蓋，在所有範圍阻止安裝並從 marketplace 隱藏 plugin

**範例**：

```json theme={null}
{
  "enabledPlugins": {
    "code-formatter@team-tools": true,
    "deployment-tools@team-tools": true,
    "experimental-features@personal": false
  }
}
```

#### `extraKnownMarketplaces`

定義應為儲存庫提供的其他 marketplaces。通常在儲存庫層級設定中使用，以確保團隊成員有權存取所需的 plugin 來源。

**當儲存庫包含 `extraKnownMarketplaces` 時**：

1. 當團隊成員信任資料夾時，系統會提示他們安裝 marketplace
2. 然後提示團隊成員從該 marketplace 安裝 plugins
3. 使用者可以跳過不需要的 marketplaces 或 plugins（儲存在使用者設定中）
4. 安裝尊重信任邊界並需要明確同意

**範例**：

```json theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    },
    "security-plugins": {
      "source": {
        "source": "git",
        "url": "https://git.example.com/security/plugins.git"
      }
    }
  }
}
```

**Marketplace 來源類型**：

* `github`：GitHub 儲存庫（使用 `repo`）
* `git`：任何 git URL（使用 `url`）
* `directory`：本機檔案系統路徑（使用 `path`，僅用於開發）
* `hostPattern`：正規表達式模式以符合 marketplace 主機（使用 `hostPattern`）
* `settings`：直接在 settings.json 中宣告的內嵌 marketplace，無需單獨的託管儲存庫（使用 `name` 和 `plugins`）

使用 `source: 'settings'` 宣告一小組 plugins，無需設定託管 marketplace 儲存庫。此處列出的 Plugins 必須參考外部來源，例如 GitHub 或 npm。您仍需要在 `enabledPlugins` 中分別啟用每個 plugin。

```json theme={null}
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "settings",
        "name": "team-tools",
        "plugins": [
          {
            "name": "code-formatter",
            "source": {
              "source": "github",
              "repo": "acme-corp/code-formatter"
            }
          }
        ]
      }
    }
  }
}
```

#### `strictKnownMarketplaces`

**Managed 設定僅限**：控制使用者可以新增哪些 plugin marketplaces。此設定只能在 [managed 設定](/zh-TW/settings#settings-files)中設定，並為管理員提供對 marketplace 來源的嚴格控制。

**Managed 設定檔案位置**：

* **macOS**：`/Library/Application Support/ClaudeCode/managed-settings.json`
* **Linux 和 WSL**：`/etc/claude-code/managed-settings.json`
* **Windows**：`C:\Program Files\ClaudeCode\managed-settings.json`

**關鍵特性**：

* 僅在 managed 設定（`managed-settings.json`）中可用
* 無法被使用者或專案設定覆蓋（最高優先順序）
* 在網路/檔案系統操作之前強制執行（被阻止的來源永遠不會執行）
* 對來源規格使用精確匹配（包括 git 來源的 `ref`、`path`），除了 `hostPattern`，它使用正規表達式匹配

**白名單行為**：

* `undefined`（預設）：無限制 - 使用者可以新增任何 marketplace
* 空陣列 `[]`：完全鎖定 - 使用者無法新增任何新 marketplaces
* 來源清單：使用者只能新增完全符合的 marketplaces

**所有支援的來源類型**：

白名單支援多種 marketplace 來源類型。大多數來源使用精確匹配，而 `hostPattern` 使用正規表達式匹配 marketplace 主機。

1. **GitHub 儲存庫**：

```json theme={null}
{ "source": "github", "repo": "acme-corp/approved-plugins" }
{ "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main", "path": "marketplace" }
```

欄位：`repo`（必需）、`ref`（選用：分支/標籤/SHA）、`path`（選用：子目錄）

2. **Git 儲存庫**：

```json theme={null}
{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git" }
{ "source": "git", "url": "https://bitbucket.org/acme-corp/plugins.git", "ref": "production" }
{ "source": "git", "url": "ssh://git@git.example.com/plugins.git", "ref": "v3.1", "path": "approved" }
```

欄位：`url`（必需）、`ref`（選用：分支/標籤/SHA）、`path`（選用：子目錄）

3. **基於 URL 的 marketplaces**：

```json theme={null}
{ "source": "url", "url": "https://plugins.example.com/marketplace.json" }
{ "source": "url", "url": "https://cdn.example.com/marketplace.json", "headers": { "Authorization": "Bearer ${TOKEN}" } }
```

欄位：`url`（必需）、`headers`（選用：用於驗證存取的 HTTP 標頭）

<Note>
  基於 URL 的 marketplaces 僅下載 `marketplace.json` 檔案。它們不從伺服器下載 plugin 檔案。基於 URL 的 marketplaces 中的 Plugins 必須使用外部來源（GitHub、npm 或 git URL），而不是相對路徑。對於具有相對路徑的 plugins，請改用基於 Git 的 marketplace。請參閱[疑難排解](/zh-TW/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces)以了解詳細資訊。
</Note>

4. **NPM 套件**：

```json theme={null}
{ "source": "npm", "package": "@acme-corp/claude-plugins" }
{ "source": "npm", "package": "@acme-corp/approved-marketplace" }
```

欄位：`package`（必需，支援範圍套件）

5. **檔案路徑**：

```json theme={null}
{ "source": "file", "path": "/usr/local/share/claude/acme-marketplace.json" }
{ "source": "file", "path": "/opt/acme-corp/plugins/marketplace.json" }
```

欄位：`path`（必需：marketplace.json 檔案的絕對路徑）

6. **目錄路徑**：

```json theme={null}
{ "source": "directory", "path": "/usr/local/share/claude/acme-plugins" }
{ "source": "directory", "path": "/opt/acme-corp/approved-marketplaces" }
```

欄位：`path`（必需：包含 `.claude-plugin/marketplace.json` 的目錄的絕對路徑）

7. **主機模式匹配**：

```json theme={null}
{ "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" }
{ "source": "hostPattern", "hostPattern": "^gitlab\\.internal\\.example\\.com$" }
```

欄位：`hostPattern`（必需：用於符合 marketplace 主機的正規表達式模式）

當您想允許來自特定主機的所有 marketplaces 而不列舉每個儲存庫時，請使用主機模式匹配。這對於具有內部 GitHub Enterprise 或 GitLab 伺服器的組織很有用，開發人員可以在其中建立自己的 marketplaces。

按來源類型的主機提取：

* `github`：始終符合 `github.com`
* `git`：從 URL 提取主機名稱（支援 HTTPS 和 SSH 格式）
* `url`：從 URL 提取主機名稱
* `npm`、`file`、`directory`：不支援主機模式匹配

**設定範例**：

範例：僅允許特定 marketplaces：

```json theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    },
    {
      "source": "npm",
      "package": "@acme-corp/compliance-plugins"
    }
  ]
}
```

範例 - 停用所有 marketplace 新增：

```json theme={null}
{
  "strictKnownMarketplaces": []
}
```

範例：允許來自內部 git 伺服器的所有 marketplaces：

```json theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

**精確匹配要求**：

Marketplace 來源必須**完全符合**才能允許使用者的新增。對於基於 git 的來源（`github` 和 `git`），這包括所有選用欄位：

* `repo` 或 `url` 必須完全符合
* `ref` 欄位必須完全符合（或兩者都未定義）
* `path` 欄位必須完全符合（或兩者都未定義）

**不符合**的來源範例：

```json theme={null}
// 這些是不同的來源：
{ "source": "github", "repo": "acme-corp/plugins" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main" }

// 這些也不同：
{ "source": "github", "repo": "acme-corp/plugins", "path": "marketplace" }
{ "source": "github", "repo": "acme-corp/plugins" }
```

**與 `extraKnownMarketplaces` 的比較**：

| 方面         | `strictKnownMarketplaces` | `extraKnownMarketplaces` |
| ---------- | ------------------------- | ------------------------ |
| **目的**     | 組織政策強制執行                  | 團隊便利                     |
| **設定檔案**   | 僅 `managed-settings.json` | 任何設定檔案                   |
| **行為**     | 阻止非白名單新增                  | 自動安裝遺失的 marketplaces     |
| **何時強制執行** | 在網路/檔案系統操作之前              | 在使用者信任提示之後               |
| **可以被覆蓋**  | 否（最高優先順序）                 | 是（由較高優先順序設定）             |
| **來源格式**   | 直接來源物件                    | 具有巢狀來源的命名 marketplace    |
| **使用案例**   | 合規、安全限制                   | 上線、標準化                   |

**格式差異**：

`strictKnownMarketplaces` 使用直接來源物件：

```json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ]
}
```

`extraKnownMarketplaces` 需要命名 marketplaces：

```json theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

**同時使用兩者**：

`strictKnownMarketplaces` 是政策閘門：它控制使用者可能新增的內容，但不註冊任何 marketplaces。若要同時限制和為所有使用者預先註冊 marketplace，請在 `managed-settings.json` 中設定兩者：

```json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ],
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

僅設定 `strictKnownMarketplaces` 時，使用者仍可透過 `/plugin marketplace add` 手動新增允許的 marketplace，但它不會自動提供。

**重要注意事項**：

* 限制在任何網路請求或檔案系統操作之前檢查
* 被阻止時，使用者會看到清晰的錯誤訊息，指示來源被 managed 政策阻止
* 限制僅適用於新增 NEW marketplaces；先前安裝的 marketplaces 仍可存取
* Managed 設定具有最高優先順序，無法被覆蓋

請參閱 [Managed marketplace 限制](/zh-TW/plugin-marketplaces#managed-marketplace-restrictions)以了解面向使用者的文件。

### 管理 plugins

使用 `/plugin` 命令以互動方式管理 plugins：

* 瀏覽 marketplaces 中的可用 plugins
* 安裝/解除安裝 plugins
* 啟用/停用 plugins
* 檢視 plugin 詳細資訊（提供的命令、agents、hooks）
* 新增/移除 marketplaces

在 [plugins 文件](/zh-TW/plugins)中深入了解 plugin 系統。

## 環境變數

環境變數可讓您控制 Claude Code 行為，而無需編輯設定檔案。任何變數也可以在 [`settings.json`](#available-settings) 中的 `env` 金鑰下設定，以將其應用於每個工作階段或推出到您的團隊。

請參閱[環境變數參考](/zh-TW/env-vars)以了解完整清單。

## Claude 可用的工具

Claude Code 可以存取一組工具，用於讀取、編輯、搜尋、執行命令和協調 subagents。工具名稱是您在權限規則和 hook 匹配器中使用的確切字串。

請參閱[工具參考](/zh-TW/tools-reference)以了解完整清單和 Bash 工具行為詳細資訊。

## 另請參閱

* [Permissions](/zh-TW/permissions)：權限系統、規則語法、工具特定模式和 managed 政策
* [Authentication](/zh-TW/authentication)：設定使用者對 Claude Code 的存取
* [Troubleshooting](/zh-TW/troubleshooting)：常見設定問題的解決方案
