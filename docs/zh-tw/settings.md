> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code 設定

> 使用全域和專案層級設定以及環境變數來設定 Claude Code。

Claude Code 提供多種設定選項，可根據您的需求配置其行為。您可以在使用互動式 REPL 時執行 `/config` 命令來設定 Claude Code，這會開啟一個標籤式設定介面，您可以在其中查看狀態資訊並修改設定選項。

## 設定範圍

Claude Code 使用**範圍系統**來決定設定的適用位置和共享對象。了解範圍可幫助您決定如何為個人使用、團隊協作或企業部署配置 Claude Code。

### 可用的範圍

| 範圍          | 位置                                               | 影響對象        | 與團隊共享？        |
| :---------- | :----------------------------------------------- | :---------- | :------------ |
| **Managed** | 伺服器管理的設定、plist / 登錄或系統層級 `managed-settings.json` | 機器上的所有使用者   | 是（由 IT 部署）    |
| **User**    | `~/.claude/` 目錄                                  | 您，跨所有專案     | 否             |
| **Project** | 儲存庫中的 `.claude/`                                 | 此儲存庫上的所有協作者 | 是（提交到 git）    |
| **Local**   | `.claude/settings.local.json`                    | 您，僅在此儲存庫中   | 否（gitignored） |

### 何時使用各個範圍

**Managed 範圍**用於：

* 必須在整個組織範圍內強制執行的安全政策
* 無法覆蓋的合規要求
* 由 IT/DevOps 部署的標準化配置

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
* 在與團隊共享之前測試配置
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

| 功能              | 使用者位置                     | 專案位置                              | Local 位置                      |
| :-------------- | :------------------------ | :-------------------------------- | :---------------------------- |
| **Settings**    | `~/.claude/settings.json` | `.claude/settings.json`           | `.claude/settings.local.json` |
| **Subagents**   | `~/.claude/agents/`       | `.claude/agents/`                 | —                             |
| **MCP servers** | `~/.claude.json`          | `.mcp.json`                       | `~/.claude.json`（每個專案）        |
| **Plugins**     | `~/.claude/settings.json` | `.claude/settings.json`           | `.claude/settings.local.json` |
| **CLAUDE.md**   | `~/.claude/CLAUDE.md`     | `CLAUDE.md` 或 `.claude/CLAUDE.md` | —                             |

***

## 設定檔案

`settings.json` 檔案是我們用於透過分層設定來配置 Claude Code 的官方機制：

* **使用者設定**在 `~/.claude/settings.json` 中定義，適用於所有專案。
* **專案設定**儲存在您的專案目錄中：
  * `.claude/settings.json` 用於簽入原始碼控制並與您的團隊共享的設定
  * `.claude/settings.local.json` 用於未簽入的設定，適用於個人偏好設定和實驗。Claude Code 在建立時會將 `.claude/settings.local.json` 配置為 git 忽略。
* **Managed 設定**：對於需要集中控制的組織，Claude Code 支援多種 managed 設定的傳遞機制。所有機制都使用相同的 JSON 格式，無法被使用者或專案設定覆蓋：

  * **伺服器管理的設定**：透過 Claude.ai 管理員主控台從 Anthropic 的伺服器傳遞。請參閱[伺服器管理的設定](/zh-TW/server-managed-settings)。
  * **MDM/OS 層級政策**：透過 macOS 和 Windows 上的原生裝置管理傳遞：
    * macOS：`com.anthropic.claudecode` managed preferences 網域（透過 Jamf、Kandji 或其他 MDM 工具中的設定檔案部署）
    * Windows：`HKLM\SOFTWARE\Policies\ClaudeCode` 登錄機碼，其中包含 JSON 的 `Settings` 值（REG\_SZ 或 REG\_EXPAND\_SZ）（透過群組原則或 Intune 部署）
    * Windows（使用者層級）：`HKCU\SOFTWARE\Policies\ClaudeCode`（最低政策優先順序，僅在沒有管理員層級來源時使用）
  * **檔案型**：`managed-settings.json` 和 `managed-mcp.json` 部署到系統目錄：
    * macOS：`/Library/Application Support/ClaudeCode/`
    * Linux 和 WSL：`/etc/claude-code/`
    * Windows：`C:\Program Files\ClaudeCode\`

  請參閱 [managed 設定](/zh-TW/permissions#managed-only-settings) 和 [Managed MCP 配置](/zh-TW/mcp#managed-mcp-configuration) 以取得詳細資訊。

  <Note>
    Managed 部署也可以使用 `strictKnownMarketplaces` 限制 **plugin marketplace 新增**。如需詳細資訊，請參閱 [Managed marketplace 限制](/zh-TW/plugin-marketplaces#managed-marketplace-restrictions)。
  </Note>
* **其他配置**儲存在 `~/.claude.json` 中。此檔案包含您的偏好設定（主題、通知設定、編輯器模式）、OAuth 工作階段、[MCP server](/zh-TW/mcp) 配置（用於使用者和 local 範圍）、每個專案的狀態（允許的工具、信任設定）和各種快取。專案範圍的 MCP servers 分別儲存在 `.mcp.json` 中。

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
    "歡迎來到 Acme Corp！請在 docs.acme.com 查看我們的程式碼指南",
    "提醒：所有 PR 都需要程式碼審查",
    "新的安全政策已生效"
  ]
}
```

上面範例中的 `$schema` 行指向 Claude Code 設定的[官方 JSON 架構](https://json.schemastore.org/claude-code-settings.json)。將其新增到您的 `settings.json` 可在 VS Code、Cursor 和任何其他支援 JSON 架構驗證的編輯器中啟用自動完成和內聯驗證。

### 可用的設定

`settings.json` 支援多個選項：

| 金鑰                                | 描述                                                                                                                                                                                               | 範例                                                               |
| :-------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------- |
| `apiKeyHelper`                    | 自訂指令碼，在 `/bin/sh` 中執行，以產生驗證值。此值將作為 `X-Api-Key` 和 `Authorization: Bearer` 標頭傳送以進行模型請求                                                                                                             | `/bin/generate_temp_api_key.sh`                                  |
| `cleanupPeriodDays`               | 非作用中超過此期間的工作階段在啟動時被刪除。設定為 `0` 會立即刪除所有工作階段。（預設值：30 天）                                                                                                                                             | `20`                                                             |
| `companyAnnouncements`            | 在啟動時顯示給使用者的公告。如果提供多個公告，它們將隨機循環。                                                                                                                                                                  | `["歡迎來到 Acme Corp！請在 docs.acme.com 查看我們的程式碼指南"]`                 |
| `env`                             | 將應用於每個工作階段的環境變數                                                                                                                                                                                  | `{"FOO": "bar"}`                                                 |
| `attribution`                     | 自訂 git 提交和提取請求的歸屬。請參閱[歸屬設定](#attribution-settings)                                                                                                                                               | `{"commit": "🤖 Generated with Claude Code", "pr": ""}`          |
| `includeCoAuthoredBy`             | **已棄用**：改用 `attribution`。是否在 git 提交和提取請求中包含 `co-authored-by Claude` 署名（預設值：`true`）                                                                                                               | `false`                                                          |
| `includeGitInstructions`          | 在 Claude 的系統提示中包含內建提交和 PR 工作流程指示（預設值：`true`）。設定為 `false` 以移除這些指示，例如在使用您自己的 git 工作流程 skills 時。`CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` 環境變數在設定時優先於此設定                                               | `false`                                                          |
| `permissions`                     | 請參閱下表以了解權限的結構。                                                                                                                                                                                   |                                                                  |
| `hooks`                           | 配置自訂命令以在生命週期事件執行。請參閱 [hooks 文件](/zh-TW/hooks) 以了解格式                                                                                                                                              | 請參閱 [hooks](/zh-TW/hooks)                                        |
| `disableAllHooks`                 | 停用所有 [hooks](/zh-TW/hooks) 和任何自訂[狀態行](/zh-TW/statusline)                                                                                                                                         | `true`                                                           |
| `allowManagedHooksOnly`           | （Managed 設定僅限）防止載入使用者、專案和 plugin hooks。僅允許 managed hooks 和 SDK hooks。請參閱 [Hook 配置](#hook-configuration)                                                                                          | `true`                                                           |
| `allowedHttpHookUrls`             | HTTP hooks 可能針對的 URL 模式的允許清單。支援 `*` 作為萬用字元。設定時，具有不符合 URL 的 hooks 被阻止。未定義 = 無限制，空陣列 = 阻止所有 HTTP hooks。陣列跨設定來源合併。請參閱 [Hook 配置](#hook-configuration)                                                | `["https://hooks.example.com/*"]`                                |
| `httpHookAllowedEnvVars`          | HTTP hooks 可能插入到標頭中的環境變數名稱的允許清單。設定時，每個 hook 的有效 `allowedEnvVars` 是與此清單的交集。未定義 = 無限制。陣列跨設定來源合併。請參閱 [Hook 配置](#hook-configuration)                                                                 | `["MY_TOKEN", "HOOK_SECRET"]`                                    |
| `allowManagedPermissionRulesOnly` | （Managed 設定僅限）防止使用者和專案設定定義 `allow`、`ask` 或 `deny` 權限規則。僅適用 managed 設定中的規則。請參閱 [Managed 專用設定](/zh-TW/permissions#managed-only-settings)                                                           | `true`                                                           |
| `allowManagedMcpServersOnly`      | （Managed 設定僅限）僅尊重 managed 設定中的 `allowedMcpServers`。`deniedMcpServers` 仍從所有來源合併。使用者仍可新增 MCP servers，但僅適用管理員定義的允許清單。請參閱 [Managed MCP 配置](/zh-TW/mcp#managed-mcp-configuration)                     | `true`                                                           |
| `model`                           | 覆蓋 Claude Code 使用的預設模型                                                                                                                                                                           | `"claude-sonnet-4-6"`                                            |
| `availableModels`                 | 限制使用者可透過 `/model`、`--model`、Config 工具或 `ANTHROPIC_MODEL` 選擇的模型。不影響預設選項。請參閱[限制模型選擇](/zh-TW/model-config#restrict-model-selection)                                                                 | `["sonnet", "haiku"]`                                            |
| `modelOverrides`                  | 將 Anthropic 模型 ID 對應到提供者特定的模型 ID，例如 Bedrock 推論設定檔 ARN。每個模型選擇器項目在呼叫提供者 API 時使用其對應的值。請參閱[覆蓋每個版本的模型 ID](/zh-TW/model-config#override-model-ids-per-version)                                         | `{"claude-opus-4-6": "arn:aws:bedrock:..."}`                     |
| `otelHeadersHelper`               | 指令碼以產生動態 OpenTelemetry 標頭。在啟動時和定期執行（請參閱[動態標頭](/zh-TW/monitoring-usage#dynamic-headers)）                                                                                                          | `/bin/generate_otel_headers.sh`                                  |
| `statusLine`                      | 配置自訂狀態行以顯示上下文。請參閱 [`statusLine` 文件](/zh-TW/statusline)                                                                                                                                           | `{"type": "command", "command": "~/.claude/statusline.sh"}`      |
| `fileSuggestion`                  | 為 `@` 檔案自動完成配置自訂指令碼。請參閱[檔案建議設定](#file-suggestion-settings)                                                                                                                                       | `{"type": "command", "command": "~/.claude/file-suggestion.sh"}` |
| `respectGitignore`                | 控制 `@` 檔案選擇器是否尊重 `.gitignore` 模式。當為 `true`（預設值）時，符合 `.gitignore` 模式的檔案被排除在建議之外                                                                                                                   | `false`                                                          |
| `outputStyle`                     | 配置輸出樣式以調整系統提示。請參閱[輸出樣式文件](/zh-TW/output-styles)                                                                                                                                                  | `"Explanatory"`                                                  |
| `forceLoginMethod`                | 使用 `claudeai` 限制登入到 Claude.ai 帳戶，`console` 限制登入到 Claude Console（API 使用計費）帳戶                                                                                                                      | `claudeai`                                                       |
| `forceLoginOrgUUID`               | 指定組織的 UUID 以在登入期間自動選擇它，繞過組織選擇步驟。需要設定 `forceLoginMethod`                                                                                                                                          | `"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"`                         |
| `enableAllProjectMcpServers`      | 自動批准專案 `.mcp.json` 檔案中定義的所有 MCP servers                                                                                                                                                          | `true`                                                           |
| `enabledMcpjsonServers`           | 要批准的 `.mcp.json` 檔案中特定 MCP servers 的清單                                                                                                                                                           | `["memory", "github"]`                                           |
| `disabledMcpjsonServers`          | 要拒絕的 `.mcp.json` 檔案中特定 MCP servers 的清單                                                                                                                                                           | `["filesystem"]`                                                 |
| `allowedMcpServers`               | 在 managed-settings.json 中設定時，使用者可以配置的 MCP servers 的允許清單。未定義 = 無限制，空陣列 = 鎖定。適用於所有範圍。拒絕清單優先。請參閱 [Managed MCP 配置](/zh-TW/mcp#managed-mcp-configuration)                                             | `[{ "serverName": "github" }]`                                   |
| `deniedMcpServers`                | 在 managed-settings.json 中設定時，明確阻止的 MCP servers 的拒絕清單。適用於所有範圍，包括 managed servers。拒絕清單優先於允許清單。請參閱 [Managed MCP 配置](/zh-TW/mcp#managed-mcp-configuration)                                           | `[{ "serverName": "filesystem" }]`                               |
| `strictKnownMarketplaces`         | 在 managed-settings.json 中設定時，使用者可以新增的 plugin marketplaces 的允許清單。未定義 = 無限制，空陣列 = 鎖定。僅適用於 marketplace 新增。請參閱 [Managed marketplace 限制](/zh-TW/plugin-marketplaces#managed-marketplace-restrictions) | `[{ "source": "github", "repo": "acme-corp/plugins" }]`          |
| `blockedMarketplaces`             | （Managed 設定僅限）marketplace 來源的阻止清單。在下載前檢查被阻止的來源，因此它們永遠不會接觸檔案系統。請參閱 [Managed marketplace 限制](/zh-TW/plugin-marketplaces#managed-marketplace-restrictions)                                          | `[{ "source": "github", "repo": "untrusted/plugins" }]`          |
| `pluginTrustMessage`              | （Managed 設定僅限）自訂訊息附加到安裝前顯示的 plugin 信任警告。使用此選項新增組織特定的上下文，例如確認來自您內部 marketplace 的 plugins 已獲得批准。                                                                                                   | `"來自我們 marketplace 的所有 plugins 都已獲得 IT 批准"`                      |
| `awsAuthRefresh`                  | 修改 `.aws` 目錄的自訂指令碼（請參閱[進階認證配置](/zh-TW/amazon-bedrock#advanced-credential-configuration)）                                                                                                         | `aws sso login --profile myprofile`                              |
| `awsCredentialExport`             | 輸出包含 AWS 認證的 JSON 的自訂指令碼（請參閱[進階認證配置](/zh-TW/amazon-bedrock#advanced-credential-configuration)）                                                                                                   | `/bin/generate_aws_grant.sh`                                     |
| `alwaysThinkingEnabled`           | 預設為所有工作階段啟用[延伸思考](/zh-TW/common-workflows#use-extended-thinking-thinking-mode)。通常透過 `/config` 命令而不是直接編輯來配置                                                                                       | `true`                                                           |
| `plansDirectory`                  | 自訂計畫檔案的儲存位置。路徑相對於專案根目錄。預設值：`~/.claude/plans`                                                                                                                                                     | `"./plans"`                                                      |
| `showTurnDuration`                | 在回應後顯示回合持續時間訊息（例如「Cooked for 1m 6s」）。設定為 `false` 以隱藏這些訊息                                                                                                                                         | `true`                                                           |
| `spinnerVerbs`                    | 自訂在微調器和回合持續時間訊息中顯示的動作動詞。將 `mode` 設定為 `"replace"` 以僅使用您的動詞，或 `"append"` 以將其新增到預設值                                                                                                                 | `{"mode": "append", "verbs": ["Pondering", "Crafting"]}`         |
| `language`                        | 配置 Claude 的首選回應語言（例如 `"japanese"`、`"spanish"`、`"french"`）。Claude 預設將以此語言回應                                                                                                                       | `"japanese"`                                                     |
| `autoUpdatesChannel`              | 遵循更新的發行頻道。使用 `"stable"` 以取得通常約一週舊的版本並跳過具有主要迴歸的版本，或 `"latest"`（預設值）以取得最新版本                                                                                                                        | `"stable"`                                                       |
| `spinnerTipsEnabled`              | 在 Claude 工作時在微調器中顯示提示。設定為 `false` 以停用提示（預設值：`true`）                                                                                                                                              | `false`                                                          |
| `spinnerTipsOverride`             | 使用自訂字串覆蓋微調器提示。`tips`：提示字串陣列。`excludeDefault`：如果為 `true`，僅顯示自訂提示；如果為 `false` 或不存在，自訂提示與內建提示合併                                                                                                     | `{ "excludeDefault": true, "tips": ["使用我們的內部工具 X"] }`            |
| `terminalProgressBarEnabled`      | 啟用終端進度條，在 Windows Terminal 和 iTerm2 等支援的終端中顯示進度（預設值：`true`）                                                                                                                                      | `false`                                                          |
| `prefersReducedMotion`            | 減少或停用 UI 動畫（微調器、閃爍、閃光效果）以提高可訪問性                                                                                                                                                                  | `true`                                                           |
| `fastModePerSessionOptIn`         | 當為 `true` 時，快速模式不會跨工作階段持續。每個工作階段都以快速模式關閉開始，需要使用者使用 `/fast` 啟用它。使用者的快速模式偏好設定仍會儲存。請參閱[要求每個工作階段的選擇加入](/zh-TW/fast-mode#require-per-session-opt-in)                                                  | `true`                                                           |
| `teammateMode`                    | [agent team](/zh-TW/agent-teams) 隊友的顯示方式：`auto`（在 tmux 或 iTerm2 中選擇分割窗格，否則為進程內）、`in-process` 或 `tmux`。請參閱[設定 agent teams](/zh-TW/agent-teams#set-up-agent-teams)                                 | `"in-process"`                                                   |

### 權限設定

| 金鑰                             | 描述                                                                                                                                                  | 範例                                                                     |
| :----------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `allow`                        | 允許工具使用的權限規則陣列。請參閱下面的[權限規則語法](#permission-rule-syntax)以了解模式匹配詳細資訊                                                                                    | `[ "Bash(git diff *)" ]`                                               |
| `ask`                          | 要求在工具使用時確認的權限規則陣列。請參閱下面的[權限規則語法](#permission-rule-syntax)                                                                                           | `[ "Bash(git push *)" ]`                                               |
| `deny`                         | 拒絕工具使用的權限規則陣列。使用此選項從 Claude Code 存取中排除敏感檔案。請參閱[權限規則語法](#permission-rule-syntax)和 [Bash 權限限制](/zh-TW/permissions#tool-specific-permission-rules)     | `[ "WebFetch", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)" ]` |
| `additionalDirectories`        | Claude 有權存取的其他[工作目錄](/zh-TW/permissions#working-directories)                                                                                        | `[ "../docs/" ]`                                                       |
| `defaultMode`                  | 開啟 Claude Code 時的預設[權限模式](/zh-TW/permissions#permission-modes)                                                                                      | `"acceptEdits"`                                                        |
| `disableBypassPermissionsMode` | 設定為 `"disable"` 以防止啟用 `bypassPermissions` 模式。這會停用 `--dangerously-skip-permissions` 命令列旗標。請參閱 [managed 設定](/zh-TW/permissions#managed-only-settings) | `"disable"`                                                            |

### 權限規則語法

權限規則遵循 `Tool` 或 `Tool(specifier)` 的格式。規則按順序評估：首先是拒絕規則，然後是詢問，最後是允許。第一個符合的規則獲勝。

快速範例：

| 規則                             | 效果                    |
| :----------------------------- | :-------------------- |
| `Bash`                         | 符合所有 Bash 命令          |
| `Bash(npm run *)`              | 符合以 `npm run` 開頭的命令   |
| `Read(./.env)`                 | 符合讀取 `.env` 檔案        |
| `WebFetch(domain:example.com)` | 符合對 example.com 的提取請求 |

如需完整的規則語法參考，包括萬用字元行為、Read、Edit、WebFetch、MCP 和 Agent 規則的工具特定模式，以及 Bash 模式的安全限制，請參閱[權限規則語法](/zh-TW/permissions#permission-rule-syntax)。

### Sandbox 設定

配置進階 sandboxing 行為。Sandboxing 將 bash 命令與您的檔案系統和網路隔離。請參閱 [Sandboxing](/zh-TW/sandboxing) 以了解詳細資訊。

| 金鑰                                | 描述                                                                                                                                                                                        | 範例                              |
| :-------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------ |
| `enabled`                         | 啟用 bash sandboxing（macOS、Linux 和 WSL2）。預設值：false                                                                                                                                          | `true`                          |
| `autoAllowBashIfSandboxed`        | 在 sandboxed 時自動批准 bash 命令。預設值：true                                                                                                                                                        | `true`                          |
| `excludedCommands`                | 應在 sandbox 外執行的命令                                                                                                                                                                         | `["git", "docker"]`             |
| `allowUnsandboxedCommands`        | 允許命令透過 `dangerouslyDisableSandbox` 參數在 sandbox 外執行。當設定為 `false` 時，`dangerouslyDisableSandbox` 逃脫艙完全停用，所有命令必須 sandboxed（或在 `excludedCommands` 中）。對於需要嚴格 sandboxing 的企業政策很有用。預設值：true       | `false`                         |
| `filesystem.allowWrite`           | sandboxed 命令可以寫入的其他路徑。陣列跨所有設定範圍合併：使用者、專案和 managed 路徑合併，不替換。也與 `Edit(...)` 允許權限規則中的路徑合併。請參閱下面的[路徑前綴](#sandbox-path-prefixes)。                                                              | `["//tmp/build", "~/.kube"]`    |
| `filesystem.denyWrite`            | sandboxed 命令無法寫入的路徑。陣列跨所有設定範圍合併。也與 `Edit(...)` 拒絕權限規則中的路徑合併。                                                                                                                              | `["//etc", "//usr/local/bin"]`  |
| `filesystem.denyRead`             | sandboxed 命令無法讀取的路徑。陣列跨所有設定範圍合併。也與 `Read(...)` 拒絕權限規則中的路徑合併。                                                                                                                              | `["~/.aws/credentials"]`        |
| `network.allowUnixSockets`        | sandbox 中可存取的 Unix socket 路徑（用於 SSH 代理等）                                                                                                                                                  | `["~/.ssh/agent-socket"]`       |
| `network.allowAllUnixSockets`     | 允許 sandbox 中的所有 Unix socket 連線。預設值：false                                                                                                                                                  | `true`                          |
| `network.allowLocalBinding`       | 允許繫結到 localhost 連接埠（僅限 macOS）。預設值：false                                                                                                                                                   | `true`                          |
| `network.allowedDomains`          | 允許出站網路流量的網域陣列。支援萬用字元（例如 `*.example.com`）。                                                                                                                                                 | `["github.com", "*.npmjs.org"]` |
| `network.allowManagedDomainsOnly` | （Managed 設定僅限）僅尊重 managed 設定中的 `allowedDomains` 和 `WebFetch(domain:...)` 允許規則。來自使用者、專案和 local 設定的網域被忽略。非允許的網域自動被阻止，不提示使用者。拒絕的網域仍從所有來源受尊重。預設值：false                                        | `true`                          |
| `network.httpProxyPort`           | 如果您想帶上自己的代理，則使用的 HTTP 代理連接埠。如果未指定，Claude 將執行自己的代理。                                                                                                                                        | `8080`                          |
| `network.socksProxyPort`          | 如果您想帶上自己的代理，則使用的 SOCKS5 代理連接埠。如果未指定，Claude 將執行自己的代理。                                                                                                                                      | `8081`                          |
| `enableWeakerNestedSandbox`       | 為無特權 Docker 環境啟用較弱的 sandbox（僅限 Linux 和 WSL2）。**降低安全性。** 預設值：false                                                                                                                         | `true`                          |
| `enableWeakerNetworkIsolation`    | （僅限 macOS）允許在 sandbox 中存取系統 TLS 信任服務（`com.apple.trustd.agent`）。對於 Go 型工具（如 `gh`、`gcloud` 和 `terraform`）在使用 `httpProxyPort` 與 MITM 代理和自訂 CA 時驗證 TLS 憑證是必需的。**降低安全性**，開啟潛在的資料洩露路徑。預設值：false | `true`                          |

#### Sandbox 路徑前綴

`filesystem.allowWrite`、`filesystem.denyWrite` 和 `filesystem.denyRead` 中的路徑支援這些前綴：

| 前綴        | 含義                    | 範例                                |
| :-------- | :-------------------- | :-------------------------------- |
| `//`      | 從檔案系統根目錄的絕對路徑         | `//tmp/build` 變成 `/tmp/build`     |
| `~/`      | 相對於主目錄                | `~/.kube` 變成 `$HOME/.kube`        |
| `/`       | 相對於設定檔案的目錄            | `/build` 變成 `$SETTINGS_DIR/build` |
| `./` 或無前綴 | 相對路徑（由 sandbox 執行時解析） | `./output`                        |

**配置範例：**

```json  theme={null}
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker"],
    "filesystem": {
      "allowWrite": ["//tmp/build", "~/.kube"],
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

**檔案系統和網路限制**可以透過兩種合併在一起的方式配置：

* **`sandbox.filesystem` 設定**（如上所示）：在 OS 層級 sandbox 邊界控制路徑。這些限制適用於所有子流程命令（例如 `kubectl`、`terraform`、`npm`），而不僅僅是 Claude 的檔案工具。
* **權限規則**：使用 `Edit` 允許/拒絕規則控制 Claude 的檔案工具存取，`Read` 拒絕規則阻止讀取，`WebFetch` 允許/拒絕規則控制網路網域。這些規則中的路徑也合併到 sandbox 配置中。

### 歸屬設定

Claude Code 將歸屬新增到 git 提交和提取請求。這些分別配置：

* 提交預設使用 [git trailers](https://git-scm.com/docs/git-interpret-trailers)（如 `Co-Authored-By`），可以自訂或停用
* 提取請求描述是純文字

| 金鑰       | 描述                                |
| :------- | :-------------------------------- |
| `commit` | git 提交的歸屬，包括任何 trailers。空字串隱藏提交歸屬 |
| `pr`     | 提取請求描述的歸屬。空字串隱藏提取請求歸屬             |

**預設提交歸屬：**

```text  theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**預設提取請求歸屬：**

```text  theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**範例：**

```json  theme={null}
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

為 `@` 檔案路徑自動完成配置自訂命令。內建檔案建議使用快速檔案系統遍歷，但大型 monorepos 可能受益於專案特定的索引，例如預先建立的檔案索引或自訂工具。

```json  theme={null}
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

該命令使用與 [hooks](/zh-TW/hooks) 相同的環境變數執行，包括 `CLAUDE_PROJECT_DIR`。它透過 stdin 接收包含 `query` 欄位的 JSON：

```json  theme={null}
{"query": "src/comp"}
```

將換行符分隔的檔案路徑輸出到 stdout（目前限制為 15）：

```text  theme={null}
src/components/Button.tsx
src/components/Modal.tsx
src/components/Form.tsx
```

**範例：**

```bash  theme={null}
#!/bin/bash
query=$(cat | jq -r '.query')
your-repo-file-index --query "$query" | head -20
```

### Hook 配置

這些設定控制允許執行哪些 hooks 以及 HTTP hooks 可以存取的內容。`allowManagedHooksOnly` 設定只能在 [managed 設定](#settings-files)中配置。URL 和環境變數允許清單可以在任何設定層級設定，並跨來源合併。

**當 `allowManagedHooksOnly` 為 `true` 時的行為：**

* 載入 managed hooks 和 SDK hooks
* 使用者 hooks、專案 hooks 和 plugin hooks 被阻止

**限制 HTTP hook URL：**

限制 HTTP hooks 可以針對的 URL。支援 `*` 作為匹配的萬用字元。定義陣列時，針對不符合 URL 的 HTTP hooks 被無聲地阻止。

```json  theme={null}
{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}
```

**限制 HTTP hook 環境變數：**

限制 HTTP hooks 可以插入到標頭值中的環境變數名稱。每個 hook 的有效 `allowedEnvVars` 是其自己清單與此設定的交集。

```json  theme={null}
{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}
```

### 設定優先順序

設定按優先順序順序應用。從最高到最低：

1. **Managed 設定**（[伺服器管理](/zh-TW/server-managed-settings)、[MDM/OS 層級政策](#configuration-scopes) 或 [managed 設定](/zh-TW/settings#settings-files)）
   * 由 IT 透過伺服器傳遞、MDM 設定檔案、登錄政策或 managed 設定檔案部署的政策
   * 無法被任何其他層級覆蓋，包括命令列引數
   * 在 managed 層級內，優先順序為：伺服器管理 > MDM/OS 層級政策 > `managed-settings.json` > HKCU 登錄（僅限 Windows）。僅使用一個 managed 來源；來源不合併。

2. **命令列引數**
   * 特定工作階段的臨時覆蓋

3. **Local 專案設定**（`.claude/settings.local.json`）
   * 個人專案特定設定

4. **共享專案設定**（`.claude/settings.json`）
   * 原始碼控制中的團隊共享專案設定

5. **使用者設定**（`~/.claude/settings.json`）
   * 個人全域設定

此階層確保組織政策始終被強制執行，同時仍允許團隊和個人自訂其體驗。

例如，如果您的使用者設定允許 `Bash(npm run *)`，但專案的共享設定拒絕它，則專案設定優先，命令被阻止。

<Note>
  **陣列設定跨範圍合併。** 當相同的陣列值設定（例如 `sandbox.filesystem.allowWrite` 或 `permissions.allow`）出現在多個範圍中時，陣列被**連接和去重**，而不是替換。這意味著較低優先順序的範圍可以新增項目而不覆蓋由較高優先順序範圍設定的項目，反之亦然。例如，如果 managed 設定將 `allowWrite` 設定為 `["//opt/company-tools"]`，使用者新增 `["~/.kube"]`，則最終配置中包含兩個路徑。
</Note>

### 驗證作用中的設定

在 Claude Code 內執行 `/status` 以查看哪些設定來源是作用中的以及它們來自何處。輸出顯示每個配置層（managed、使用者、專案）及其來源，例如 `Enterprise managed settings (remote)`、`Enterprise managed settings (plist)`、`Enterprise managed settings (HKLM)` 或 `Enterprise managed settings (file)`。如果設定檔案包含錯誤，`/status` 會報告問題，以便您可以修復它。

### 關於配置系統的要點

* **記憶體檔案（`CLAUDE.md`）**：包含 Claude 在啟動時載入的指示和上下文
* **設定檔案（JSON）**：配置權限、環境變數和工具行為
* **Skills**：可以使用 `/skill-name` 叫用或由 Claude 自動載入的自訂提示
* **MCP servers**：使用其他工具和整合擴展 Claude Code
* **優先順序**：較高層級的配置（Managed）覆蓋較低層級的配置（User/Project）
* **繼承**：設定被合併，更具體的設定新增到或覆蓋更廣泛的設定

### 系統提示

Claude Code 的內部系統提示未發佈。若要新增自訂指示，請使用 `CLAUDE.md` 檔案或 `--append-system-prompt` 旗標。

### 排除敏感檔案

若要防止 Claude Code 存取包含敏感資訊（如 API 金鑰、機密和環境檔案）的檔案，請在您的 `.claude/settings.json` 檔案中使用 `permissions.deny` 設定：

```json  theme={null}
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

這取代了已棄用的 `ignorePatterns` 配置。符合這些模式的檔案被排除在檔案發現和搜尋結果之外，這些檔案上的讀取操作被拒絕。

## Subagent 配置

Claude Code 支援可在使用者和專案層級配置的自訂 AI subagents。這些 subagents 儲存為具有 YAML frontmatter 的 Markdown 檔案：

* **使用者 subagents**：`~/.claude/agents/` - 在所有專案中可用
* **專案 subagents**：`.claude/agents/` - 特定於您的專案，可與您的團隊共享

Subagent 檔案定義具有自訂提示和工具權限的專門 AI 助手。在 [subagents 文件](/zh-TW/sub-agents)中了解更多關於建立和使用 subagents 的資訊。

## Plugin 配置

Claude Code 支援 plugin 系統，可讓您使用 skills、agents、hooks 和 MCP servers 擴展功能。Plugins 透過 marketplaces 分發，可以在使用者和儲存庫層級配置。

### Plugin 設定

`settings.json` 中的 plugin 相關設定：

```json  theme={null}
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
* **Local 設定**（`.claude/settings.local.json`）：每台機器的覆蓋（未提交）

**範例**：

```json  theme={null}
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
2. 然後系統會提示團隊成員安裝來自該 marketplace 的 plugins
3. 使用者可以跳過不需要的 marketplaces 或 plugins（儲存在使用者設定中）
4. 安裝尊重信任邊界並需要明確同意

**範例**：

```json  theme={null}
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

#### `strictKnownMarketplaces`

**Managed 設定僅限**：控制使用者可以新增哪些 plugin marketplaces。此設定只能在 [managed 設定](/zh-TW/settings#settings-files)中配置，為管理員提供對 marketplace 來源的嚴格控制。

**Managed 設定檔案位置**：

* **macOS**：`/Library/Application Support/ClaudeCode/managed-settings.json`
* **Linux 和 WSL**：`/etc/claude-code/managed-settings.json`
* **Windows**：`C:\Program Files\ClaudeCode\managed-settings.json`

**主要特徵**：

* 僅在 managed 設定（`managed-settings.json`）中可用
* 無法被使用者或專案設定覆蓋（最高優先順序）
* 在網路/檔案系統操作之前強制執行（被阻止的來源永遠不會執行）
* 對來源規格使用精確匹配（包括 git 來源的 `ref`、`path`），除了 `hostPattern`，它使用正規表達式匹配

**允許清單行為**：

* `undefined`（預設值）：無限制 - 使用者可以新增任何 marketplace
* 空陣列 `[]`：完全鎖定 - 使用者無法新增任何新 marketplaces
* 來源清單：使用者只能新增完全符合的 marketplaces

**所有支援的來源類型**：

允許清單支援七種 marketplace 來源類型。大多數來源使用精確匹配，而 `hostPattern` 使用正規表達式匹配 marketplace 主機。

1. **GitHub 儲存庫**：

```json  theme={null}
{ "source": "github", "repo": "acme-corp/approved-plugins" }
{ "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main", "path": "marketplace" }
```

欄位：`repo`（必需）、`ref`（可選：分支/標籤/SHA）、`path`（可選：子目錄）

2. **Git 儲存庫**：

```json  theme={null}
{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git" }
{ "source": "git", "url": "https://bitbucket.org/acme-corp/plugins.git", "ref": "production" }
{ "source": "git", "url": "ssh://git@git.example.com/plugins.git", "ref": "v3.1", "path": "approved" }
```

欄位：`url`（必需）、`ref`（可選：分支/標籤/SHA）、`path`（可選：子目錄）

3. **基於 URL 的 marketplaces**：

```json  theme={null}
{ "source": "url", "url": "https://plugins.example.com/marketplace.json" }
{ "source": "url", "url": "https://cdn.example.com/marketplace.json", "headers": { "Authorization": "Bearer ${TOKEN}" } }
```

欄位：`url`（必需）、`headers`（可選：用於驗證存取的 HTTP 標頭）

<Note>
  基於 URL 的 marketplaces 僅下載 `marketplace.json` 檔案。它們不從伺服器下載 plugin 檔案。基於 URL 的 marketplaces 中的 Plugins 必須使用外部來源（GitHub、npm 或 git URL），而不是相對路徑。對於具有相對路徑的 plugins，請改用基於 Git 的 marketplace。請參閱[故障排除](/zh-TW/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces)以了解詳細資訊。
</Note>

4. **NPM 套件**：

```json  theme={null}
{ "source": "npm", "package": "@acme-corp/claude-plugins" }
{ "source": "npm", "package": "@acme-corp/approved-marketplace" }
```

欄位：`package`（必需，支援範圍套件）

5. **檔案路徑**：

```json  theme={null}
{ "source": "file", "path": "/usr/local/share/claude/acme-marketplace.json" }
{ "source": "file", "path": "/opt/acme-corp/plugins/marketplace.json" }
```

欄位：`path`（必需：marketplace.json 檔案的絕對路徑）

6. **目錄路徑**：

```json  theme={null}
{ "source": "directory", "path": "/usr/local/share/claude/acme-plugins" }
{ "source": "directory", "path": "/opt/acme-corp/approved-marketplaces" }
```

欄位：`path`（必需：包含 `.claude-plugin/marketplace.json` 的目錄的絕對路徑）

7. **主機模式匹配**：

```json  theme={null}
{ "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" }
{ "source": "hostPattern", "hostPattern": "^gitlab\\.internal\\.example\\.com$" }
```

欄位：`hostPattern`（必需：正規表達式模式以匹配 marketplace 主機）

當您想允許來自特定主機的所有 marketplaces 而不列舉每個儲存庫時，請使用主機模式匹配。這對於具有內部 GitHub Enterprise 或 GitLab 伺服器的組織很有用，開發人員在其中建立自己的 marketplaces。

按來源類型的主機提取：

* `github`：始終匹配 `github.com`
* `git`：從 URL 提取主機名稱（支援 HTTPS 和 SSH 格式）
* `url`：從 URL 提取主機名稱
* `npm`、`file`、`directory`：不支援主機模式匹配

**配置範例**：

範例：僅允許特定 marketplaces：

```json  theme={null}
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

```json  theme={null}
{
  "strictKnownMarketplaces": []
}
```

範例：允許來自內部 git 伺服器的所有 marketplaces：

```json  theme={null}
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

Marketplace 來源必須**完全符合**才能允許使用者的新增。對於基於 git 的來源（`github` 和 `git`），這包括所有可選欄位：

* `repo` 或 `url` 必須完全符合
* `ref` 欄位必須完全符合（或兩者都未定義）
* `path` 欄位必須完全符合（或兩者都未定義）

不符合的來源範例：

```json  theme={null}
// 這些是不同的來源：
{ "source": "github", "repo": "acme-corp/plugins" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main" }

// 這些也是不同的：
{ "source": "github", "repo": "acme-corp/plugins", "path": "marketplace" }
{ "source": "github", "repo": "acme-corp/plugins" }
```

**與 `extraKnownMarketplaces` 的比較**：

| 方面         | `strictKnownMarketplaces` | `extraKnownMarketplaces` |
| ---------- | ------------------------- | ------------------------ |
| **目的**     | 組織政策強制執行                  | 團隊便利                     |
| **設定檔案**   | 僅 `managed-settings.json` | 任何設定檔案                   |
| **行為**     | 阻止非允許清單新增                 | 自動安裝遺失的 marketplaces     |
| **何時強制執行** | 在網路/檔案系統操作之前              | 在使用者信任提示之後               |
| **可以被覆蓋**  | 否（最高優先順序）                 | 是（由較高優先順序設定）             |
| **來源格式**   | 直接來源物件                    | 具有巢狀來源的命名 marketplace    |
| **使用案例**   | 合規、安全限制                   | 上線、標準化                   |

**格式差異**：

`strictKnownMarketplaces` 使用直接來源物件：

```json  theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ]
}
```

`extraKnownMarketplaces` 需要命名 marketplaces：

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

**重要注意事項**：

* 限制在任何網路請求或檔案系統操作之前檢查
* 被阻止時，使用者會看到清晰的錯誤訊息，指示來源被 managed 政策阻止
* 限制僅適用於新增 NEW marketplaces；先前安裝的 marketplaces 保持可存取
* Managed 設定具有最高優先順序，無法被覆蓋

請參閱 [Managed marketplace 限制](/zh-TW/plugin-marketplaces#managed-marketplace-restrictions)以了解面向使用者的文件。

### 管理 plugins

使用 `/plugin` 命令以互動方式管理 plugins：

* 瀏覽來自 marketplaces 的可用 plugins
* 安裝/卸載 plugins
* 啟用/停用 plugins
* 檢視 plugin 詳細資訊（提供的命令、agents、hooks）
* 新增/移除 marketplaces

在 [plugins 文件](/zh-TW/plugins)中了解更多關於 plugin 系統的資訊。

## 環境變數

Claude Code 支援以下環境變數來控制其行為：

<Note>
  所有環境變數也可以在 [`settings.json`](#available-settings) 中配置。這是自動為每個工作階段設定環境變數或為整個團隊或組織推出一組環境變數的有用方式。
</Note>

| 變數                                             | 目的                                                                                                                                                                                                                                                                                 |     |
| :--------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- |
| `ANTHROPIC_API_KEY`                            | 作為 `X-Api-Key` 標頭傳送的 API 金鑰，通常用於 Claude SDK（對於互動式使用，執行 `/login`）                                                                                                                                                                                                                   |     |
| `ANTHROPIC_AUTH_TOKEN`                         | `Authorization` 標頭的自訂值（您在此設定的值將以 `Bearer ` 為前綴）                                                                                                                                                                                                                                    |     |
| `ANTHROPIC_CUSTOM_HEADERS`                     | 要新增到請求的自訂標頭（`Name: Value` 格式，多個標頭用換行符分隔）                                                                                                                                                                                                                                           |     |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`                | 請參閱[模型配置](/zh-TW/model-config#environment-variables)                                                                                                                                                                                                                               |     |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`                 | 請參閱[模型配置](/zh-TW/model-config#environment-variables)                                                                                                                                                                                                                               |     |
| `ANTHROPIC_DEFAULT_SONNET_MODEL`               | 請參閱[模型配置](/zh-TW/model-config#environment-variables)                                                                                                                                                                                                                               |     |
| `ANTHROPIC_FOUNDRY_API_KEY`                    | Microsoft Foundry 驗證的 API 金鑰（請參閱 [Microsoft Foundry](/zh-TW/microsoft-foundry)）                                                                                                                                                                                                    |     |
| `ANTHROPIC_FOUNDRY_BASE_URL`                   | Foundry 資源的完整基本 URL（例如 `https://my-resource.services.ai.azure.com/anthropic`）。`ANTHROPIC_FOUNDRY_RESOURCE` 的替代方案（請參閱 [Microsoft Foundry](/zh-TW/microsoft-foundry)）                                                                                                                |     |
| `ANTHROPIC_FOUNDRY_RESOURCE`                   | Foundry 資源名稱（例如 `my-resource`）。如果未設定 `ANTHROPIC_FOUNDRY_BASE_URL`，則為必需（請參閱 [Microsoft Foundry](/zh-TW/microsoft-foundry)）                                                                                                                                                          |     |
| `ANTHROPIC_MODEL`                              | 要使用的模型設定名稱（請參閱[模型配置](/zh-TW/model-config#environment-variables)）                                                                                                                                                                                                                   |     |
| `ANTHROPIC_SMALL_FAST_MODEL`                   | \[已棄用] [Haiku 級模型用於背景工作](/zh-TW/costs)的名稱                                                                                                                                                                                                                                          |     |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION`        | 使用 Bedrock 時覆蓋 Haiku 級模型的 AWS 區域                                                                                                                                                                                                                                                   |     |
| `AWS_BEARER_TOKEN_BEDROCK`                     | Bedrock API 金鑰用於驗證（請參閱 [Bedrock API 金鑰](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/)）                                                                                                                                    |     |
| `BASH_DEFAULT_TIMEOUT_MS`                      | 長時間執行 bash 命令的預設逾時                                                                                                                                                                                                                                                                 |     |
| `BASH_MAX_OUTPUT_LENGTH`                       | bash 輸出中的最大字元數，超過此數量後會進行中間截斷                                                                                                                                                                                                                                                       |     |
| `BASH_MAX_TIMEOUT_MS`                          | 模型可以為長時間執行 bash 命令設定的最大逾時                                                                                                                                                                                                                                                          |     |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`              | 設定自動壓縮觸發的上下文容量百分比（1-100）。預設情況下，自動壓縮在約 95% 容量時觸發。使用較低的值（如 `50`）以更早壓縮。高於預設閾值的值無效。適用於主要對話和 subagents。此百分比與[狀態行](/zh-TW/statusline)中可用的 `context_window.used_percentage` 欄位對齊                                                                                                          |     |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR`     | 在每個 Bash 命令後返回原始工作目錄                                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_ACCOUNT_UUID`                     | 已驗證使用者的帳戶 UUID。由 SDK 呼叫者使用以同步提供帳戶資訊，避免早期遙測事件缺少帳戶中繼資料的競爭條件。需要同時設定 `CLAUDE_CODE_USER_EMAIL` 和 `CLAUDE_CODE_ORGANIZATION_UUID`                                                                                                                                                        |     |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | 設定為 `1` 以從使用 `--add-dir` 指定的目錄載入 CLAUDE.md 檔案。預設情況下，其他目錄不載入記憶體檔案                                                                                                                                                                                                                   | `1` |
| `CLAUDE_CODE_API_KEY_HELPER_TTL_MS`            | 應刷新認證的間隔（以毫秒為單位）（使用 `apiKeyHelper` 時）                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_CLIENT_CERT`                      | 用於 mTLS 驗證的用戶端憑證檔案的路徑                                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_CLIENT_KEY`                       | 用於 mTLS 驗證的用戶端私密金鑰檔案的路徑                                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE`            | 加密 CLAUDE\_CODE\_CLIENT\_KEY 的密碼（可選）                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT`               | 設定為 `1` 以停用 [1M 上下文視窗](/zh-TW/model-config#extended-context)支援。設定時，1M 模型變體在模型選擇器中不可用。對於具有合規要求的企業環境很有用                                                                                                                                                                              |     |
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING`        | 設定為 `1` 以停用 Opus 4.6 和 Sonnet 4.6 的[自適應推理](/zh-TW/model-config#adjust-effort-level)。停用時，這些模型回退到由 `MAX_THINKING_TOKENS` 控制的固定思考預算                                                                                                                                                   |     |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY`              | 設定為 `1` 以停用[自動記憶](/zh-TW/memory#auto-memory)。設定為 `0` 以在逐步推出期間強制啟用自動記憶。停用時，Claude 不建立或載入自動記憶檔案                                                                                                                                                                                      |     |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS`         | 設定為 `1` 以從 Claude 的系統提示中移除內建提交和 PR 工作流程指示。在使用您自己的 git 工作流程 skills 時很有用。設定時優先於 [`includeGitInstructions`](#available-settings) 設定                                                                                                                                                   |     |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`         | 設定為 `1` 以停用所有背景工作功能，包括 Bash 和 subagent 工具上的 `run_in_background` 參數、自動背景化和 Ctrl+B 快捷鍵                                                                                                                                                                                               |     |
| `CLAUDE_CODE_DISABLE_CRON`                     | 設定為 `1` 以停用[排程工作](/zh-TW/scheduled-tasks)。`/loop` skill 和 cron 工具變得不可用，任何已排程的工作停止觸發，包括已在工作階段中執行的工作                                                                                                                                                                                 |     |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`       | 設定為 `1` 以停用 Anthropic API 特定的 `anthropic-beta` 標頭。如果在使用具有第三方提供者的 LLM 閘道時遇到「Unexpected value(s) for the `anthropic-beta` header」之類的問題，請使用此選項                                                                                                                                        |     |
| `CLAUDE_CODE_DISABLE_FAST_MODE`                | 設定為 `1` 以停用[快速模式](/zh-TW/fast-mode)                                                                                                                                                                                                                                                |     |
| `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY`          | 設定為 `1` 以停用「Claude 表現如何？」工作階段品質調查。在使用第三方提供者或停用遙測時也會停用。請參閱[工作階段品質調查](/zh-TW/data-usage#session-quality-surveys)                                                                                                                                                                     |     |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`     | 等同於設定 `DISABLE_AUTOUPDATER`、`DISABLE_BUG_COMMAND`、`DISABLE_ERROR_REPORTING` 和 `DISABLE_TELEMETRY`                                                                                                                                                                                  |     |
| `CLAUDE_CODE_DISABLE_TERMINAL_TITLE`           | 設定為 `1` 以停用基於對話上下文的自動終端標題更新                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_EFFORT_LEVEL`                     | 為支援的模型設定努力級別。值：`low`、`medium`、`high`。較低的努力更快且更便宜，較高的努力提供更深入的推理。在 Opus 4.6 和 Sonnet 4.6 上支援。請參閱[調整努力級別](/zh-TW/model-config#adjust-effort-level)                                                                                                                                    |     |
| `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION`         | 設定為 `false` 以停用提示建議（`/config` 中的「提示建議」切換）。這些是 Claude 回應後出現在您的提示輸入中的灰色預測。請參閱[提示建議](/zh-TW/interactive-mode#prompt-suggestions)                                                                                                                                                      |     |
| `CLAUDE_CODE_ENABLE_TASKS`                     | 設定為 `false` 以暫時還原為先前的 TODO 清單而不是工作追蹤系統。預設值：`true`。請參閱[工作清單](/zh-TW/interactive-mode#task-list)                                                                                                                                                                                     |     |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                 | 設定為 `1` 以啟用用於指標和日誌的 OpenTelemetry 資料收集。在配置 OTel 匯出器之前需要。請參閱[監控](/zh-TW/monitoring-usage)                                                                                                                                                                                           |     |
| `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY`            | 查詢迴圈變為閒置後自動退出前等待的時間（以毫秒為單位）。對於使用 SDK 模式的自動化工作流程和指令碼很有用                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`         | 設定為 `1` 以啟用 [agent teams](/zh-TW/agent-teams)。Agent teams 是實驗性的，預設停用                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS`      | 覆蓋檔案讀取的預設令牌限制。當您需要完整讀取較大的檔案時很有用                                                                                                                                                                                                                                                    |     |
| `CLAUDE_CODE_HIDE_ACCOUNT_INFO`                | 設定為 `1` 以從 Claude Code UI 隱藏您的電子郵件地址和組織名稱。在串流或錄製時很有用                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`            | 跳過 IDE 擴展的自動安裝                                                                                                                                                                                                                                                                     |     |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS`                | 為大多數請求設定最大輸出令牌數。預設值：32,000。最大值：64,000。增加此值會減少在[自動壓縮](/zh-TW/costs#reduce-token-usage)觸發之前可用的有效上下文視窗。                                                                                                                                                                               |     |
| `CLAUDE_CODE_ORGANIZATION_UUID`                | 已驗證使用者的組織 UUID。由 SDK 呼叫者使用以同步提供帳戶資訊。需要同時設定 `CLAUDE_CODE_ACCOUNT_UUID` 和 `CLAUDE_CODE_USER_EMAIL`                                                                                                                                                                                   |     |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`  | 刷新動態 OpenTelemetry 標頭的間隔（以毫秒為單位）（預設值：1740000 / 29 分鐘）。請參閱[動態標頭](/zh-TW/monitoring-usage#dynamic-headers)                                                                                                                                                                           |     |
| `CLAUDE_CODE_PLAN_MODE_REQUIRED`               | 自動設定為 `true` 在需要計畫批准的 [agent team](/zh-TW/agent-teams) 隊友上。唯讀：在生成隊友時由 Claude Code 設定。請參閱[要求隊友的計畫批准](/zh-TW/agent-teams#require-plan-approval-for-teammates)                                                                                                                        |     |
| `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`            | 安裝或更新 plugins 時 git 操作的逾時（以毫秒為單位）（預設值：120000）。對於大型儲存庫或緩慢的網路連線，增加此值。請參閱 [Git 操作逾時](/zh-TW/plugin-marketplaces#git-operations-time-out)                                                                                                                                              |     |
| `CLAUDE_CODE_PROXY_RESOLVES_HOSTS`             | 設定為 `true` 以允許代理執行 DNS 解析而不是呼叫者。對於代理應處理主機名稱解析的環境選擇加入                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_SHELL`                            | 覆蓋自動 shell 偵測。當您的登入 shell 與您的首選工作 shell 不同時很有用（例如 `bash` 與 `zsh`）                                                                                                                                                                                                                  |     |
| `CLAUDE_CODE_SHELL_PREFIX`                     | 命令前綴以包裝所有 bash 命令（例如用於日誌或審計）。範例：`/path/to/logger.sh` 將執行 `/path/to/logger.sh <command>`                                                                                                                                                                                            |     |
| `CLAUDE_CODE_SIMPLE`                           | 設定為 `1` 以使用最小系統提示和僅 Bash、檔案讀取和檔案編輯工具執行。停用 MCP 工具、附件、hooks 和 CLAUDE.md 檔案                                                                                                                                                                                                           |     |
| `CLAUDE_CODE_SKIP_BEDROCK_AUTH`                | 跳過 Bedrock 的 AWS 驗證（例如在使用 LLM 閘道時）                                                                                                                                                                                                                                                 |     |
| `CLAUDE_CODE_SKIP_FOUNDRY_AUTH`                | 跳過 Microsoft Foundry 的 Azure 驗證（例如在使用 LLM 閘道時）                                                                                                                                                                                                                                     |     |
| `CLAUDE_CODE_SKIP_VERTEX_AUTH`                 | 跳過 Vertex 的 Google 驗證（例如在使用 LLM 閘道時）                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_SUBAGENT_MODEL`                   | 請參閱[模型配置](/zh-TW/model-config)                                                                                                                                                                                                                                                     |     |
| `CLAUDE_CODE_TASK_LIST_ID`                     | 跨工作階段共享工作清單。在多個 Claude Code 實例中設定相同的 ID 以協調共享工作清單。請參閱[工作清單](/zh-TW/interactive-mode#task-list)                                                                                                                                                                                     |     |
| `CLAUDE_CODE_TEAM_NAME`                        | 此隊友所屬的 agent team 的名稱。在 [agent team](/zh-TW/agent-teams) 成員上自動設定                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_TMPDIR`                           | 覆蓋用於內部臨時檔案的臨時目錄。Claude Code 將 `/claude/` 附加到此路徑。預設值：Unix/macOS 上的 `/tmp`，Windows 上的 `os.tmpdir()`                                                                                                                                                                                  |     |
| `CLAUDE_CODE_USER_EMAIL`                       | 已驗證使用者的電子郵件地址。由 SDK 呼叫者使用以同步提供帳戶資訊。需要同時設定 `CLAUDE_CODE_ACCOUNT_UUID` 和 `CLAUDE_CODE_ORGANIZATION_UUID`                                                                                                                                                                             |     |
| `CLAUDE_CODE_USE_BEDROCK`                      | 使用 [Bedrock](/zh-TW/amazon-bedrock)                                                                                                                                                                                                                                                |     |
| `CLAUDE_CODE_USE_FOUNDRY`                      | 使用 [Microsoft Foundry](/zh-TW/microsoft-foundry)                                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_USE_VERTEX`                       | 使用 [Vertex](/zh-TW/google-vertex-ai)                                                                                                                                                                                                                                               |     |
| `CLAUDE_CONFIG_DIR`                            | 自訂 Claude Code 儲存其配置和資料檔案的位置                                                                                                                                                                                                                                                       |     |
| `DISABLE_AUTOUPDATER`                          | 設定為 `1` 以停用自動更新。                                                                                                                                                                                                                                                                   |     |
| `DISABLE_BUG_COMMAND`                          | 設定為 `1` 以停用 `/bug` 命令                                                                                                                                                                                                                                                              |     |
| `DISABLE_COST_WARNINGS`                        | 設定為 `1` 以停用成本警告訊息                                                                                                                                                                                                                                                                  |     |
| `DISABLE_ERROR_REPORTING`                      | 設定為 `1` 以選擇退出 Sentry 錯誤報告                                                                                                                                                                                                                                                          |     |
| `DISABLE_INSTALLATION_CHECKS`                  | 設定為 `1` 以停用安裝警告。僅在手動管理安裝位置時使用，因為這可能會掩蓋標準安裝的問題                                                                                                                                                                                                                                      |     |
| `DISABLE_NON_ESSENTIAL_MODEL_CALLS`            | 設定為 `1` 以停用非關鍵路徑（如風味文字）的模型呼叫                                                                                                                                                                                                                                                       |     |
| `DISABLE_PROMPT_CACHING`                       | 設定為 `1` 以停用所有模型的提示快取（優先於每個模型的設定）                                                                                                                                                                                                                                                   |     |
| `DISABLE_PROMPT_CACHING_HAIKU`                 | 設定為 `1` 以停用 Haiku 模型的提示快取                                                                                                                                                                                                                                                          |     |
| `DISABLE_PROMPT_CACHING_OPUS`                  | 設定為 `1` 以停用 Opus 模型的提示快取                                                                                                                                                                                                                                                           |     |
| `DISABLE_PROMPT_CACHING_SONNET`                | 設定為 `1` 以停用 Sonnet 模型的提示快取                                                                                                                                                                                                                                                         |     |
| `DISABLE_TELEMETRY`                            | 設定為 `1` 以選擇退出 Statsig 遙測（請注意 Statsig 事件不包含使用者資料，如程式碼、檔案路徑或 bash 命令）                                                                                                                                                                                                                |     |
| `ENABLE_CLAUDEAI_MCP_SERVERS`                  | 設定為 `false` 以停用 Claude Code 中的 [claude.ai MCP servers](/zh-TW/mcp#use-mcp-servers-from-claudeai)。對於已登入的使用者預設啟用                                                                                                                                                                     |     |
| `ENABLE_TOOL_SEARCH`                           | 控制 [MCP 工具搜尋](/zh-TW/mcp#scale-with-mcp-tool-search)。值：`auto`（預設值，在 10% 上下文時啟用）、`auto:N`（自訂閾值，例如 `auto:5` 表示 5%）、`true`（始終開啟）、`false`（停用）                                                                                                                                          |     |
| `FORCE_AUTOUPDATE_PLUGINS`                     | 設定為 `true` 以強制 plugin 自動更新，即使主自動更新器透過 `DISABLE_AUTOUPDATER` 停用                                                                                                                                                                                                                     |     |
| `HTTP_PROXY`                                   | 為網路連線指定 HTTP 代理伺服器                                                                                                                                                                                                                                                                 |     |
| `HTTPS_PROXY`                                  | 為網路連線指定 HTTPS 代理伺服器                                                                                                                                                                                                                                                                |     |
| `IS_DEMO`                                      | 設定為 `true` 以啟用演示模式：從 UI 隱藏電子郵件和組織、跳過上線和隱藏內部命令。對於串流或錄製工作階段很有用                                                                                                                                                                                                                       |     |
| `MAX_MCP_OUTPUT_TOKENS`                        | MCP 工具回應中允許的最大令牌數。當輸出超過 10,000 個令牌時，Claude Code 顯示警告（預設值：25000）                                                                                                                                                                                                                    |     |
| `MAX_THINKING_TOKENS`                          | 覆蓋[延伸思考](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)令牌預算。思考預設在最大預算（31,999 個令牌）啟用。使用此選項限制預算（例如 `MAX_THINKING_TOKENS=10000`）或完全停用思考（`MAX_THINKING_TOKENS=0`）。對於 Opus 4.6，思考深度由[努力級別](/zh-TW/model-config#adjust-effort-level)控制，此變數被忽略，除非設定為 `0` 以停用思考。 |     |
| `MCP_CLIENT_SECRET`                            | 需要[預先配置認證](/zh-TW/mcp#use-pre-configured-oauth-credentials)的 MCP servers 的 OAuth 用戶端機密。在新增具有 `--client-secret` 的伺服器時避免互動式提示                                                                                                                                                        |     |
| `MCP_OAUTH_CALLBACK_PORT`                      | OAuth 重定向回呼的固定連接埠，作為在新增具有[預先配置認證](/zh-TW/mcp#use-pre-configured-oauth-credentials)的 MCP server 時 `--callback-port` 的替代方案                                                                                                                                                           |     |
| `MCP_TIMEOUT`                                  | MCP 伺服器啟動的逾時（以毫秒為單位）                                                                                                                                                                                                                                                               |     |
| `MCP_TOOL_TIMEOUT`                             | MCP 工具執行的逾時（以毫秒為單位）                                                                                                                                                                                                                                                                |     |
| `NO_PROXY`                                     | 將直接發出請求的網域和 IP 清單，繞過代理                                                                                                                                                                                                                                                             |     |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET`               | 覆蓋為 [Skill 工具](/zh-TW/skills#control-who-invokes-a-skill)顯示的 skill 中繼資料的字元預算。預算在上下文視窗的 2% 動態縮放，回退為 16,000 個字元。為了向後相容性保留舊名稱                                                                                                                                                         |     |
| `USE_BUILTIN_RIPGREP`                          | 設定為 `0` 以使用系統安裝的 `rg` 而不是 Claude Code 包含的 `rg`                                                                                                                                                                                                                                     |     |
| `VERTEX_REGION_CLAUDE_3_5_HAIKU`               | 使用 Vertex AI 時覆蓋 Claude 3.5 Haiku 的區域                                                                                                                                                                                                                                              |     |
| `VERTEX_REGION_CLAUDE_3_7_SONNET`              | 使用 Vertex AI 時覆蓋 Claude 3.7 Sonnet 的區域                                                                                                                                                                                                                                             |     |
| `VERTEX_REGION_CLAUDE_4_0_OPUS`                | 使用 Vertex AI 時覆蓋 Claude 4.0 Opus 的區域                                                                                                                                                                                                                                               |     |
| `VERTEX_REGION_CLAUDE_4_0_SONNET`              | 使用 Vertex AI 時覆蓋 Claude 4.0 Sonnet 的區域                                                                                                                                                                                                                                             |     |
| `VERTEX_REGION_CLAUDE_4_1_OPUS`                | 使用 Vertex AI 時覆蓋 Claude 4.1 Opus 的區域                                                                                                                                                                                                                                               |     |

## Claude 可用的工具

Claude Code 可以存取一組強大的工具，可幫助它理解和修改您的程式碼庫：

| 工具                       | 描述                                                                                                                                                              | 需要權限 |
| :----------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--- |
| **Agent**                | 生成具有自己上下文視窗的 [subagent](/zh-TW/sub-agents) 以處理工作                                                                                                                | 否    |
| **AskUserQuestion**      | 詢問多選問題以收集要求或澄清歧義                                                                                                                                                | 否    |
| **Bash**                 | 在您的環境中執行 shell 命令。請參閱 [Bash 工具行為](#bash-tool-behavior)                                                                                                          | 是    |
| **CronCreate**           | 在目前工作階段內排程重複或一次性提示（Claude 退出時消失）。請參閱[排程工作](/zh-TW/scheduled-tasks)                                                                                              | 否    |
| **CronDelete**           | 按 ID 取消排程工作                                                                                                                                                     | 否    |
| **CronList**             | 列出工作階段中的所有排程工作                                                                                                                                                  | 否    |
| **Edit**                 | 對特定檔案進行有針對性的編輯                                                                                                                                                  | 是    |
| **EnterPlanMode**        | 切換到計畫模式以在編碼前設計方法                                                                                                                                                | 否    |
| **EnterWorktree**        | 建立隔離的 [git worktree](/zh-TW/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) 並切換到其中                                                       | 否    |
| **ExitPlanMode**         | 提出計畫以供批准並退出計畫模式                                                                                                                                                 | 是    |
| **ExitWorktree**         | 退出 worktree 工作階段並返回原始目錄                                                                                                                                         | 否    |
| **Glob**                 | 根據模式匹配查找檔案                                                                                                                                                      | 否    |
| **Grep**                 | 在檔案內容中搜尋模式                                                                                                                                                      | 否    |
| **ListMcpResourcesTool** | 列出連接的 [MCP servers](/zh-TW/mcp) 公開的資源                                                                                                                           | 否    |
| **LSP**                  | 透過語言伺服器的程式碼智慧。在檔案編輯後自動報告型別錯誤和警告。也支援導航操作：跳轉到定義、尋找參考、取得型別資訊、列出符號、尋找實現、追蹤呼叫階層。需要 [code intelligence plugin](/zh-TW/discover-plugins#code-intelligence) 及其語言伺服器二進位檔 | 否    |
| **NotebookEdit**         | 修改 Jupyter notebook 儲存格                                                                                                                                         | 是    |
| **Read**                 | 讀取檔案的內容                                                                                                                                                         | 否    |
| **ReadMcpResourceTool**  | 按 URI 讀取特定 MCP 資源                                                                                                                                               | 否    |
| **Skill**                | 在主要對話中執行 [skill](/zh-TW/skills#control-who-invokes-a-skill)                                                                                                     | 是    |
| **TaskCreate**           | 在工作清單中建立新工作                                                                                                                                                     | 否    |
| **TaskGet**              | 檢索特定工作的完整詳細資訊                                                                                                                                                   | 否    |
| **TaskList**             | 列出所有工作及其目前狀態                                                                                                                                                    | 否    |
| **TaskOutput**           | 檢索背景工作的輸出                                                                                                                                                       | 否    |
| **TaskStop**             | 按 ID 終止執行中的背景工作                                                                                                                                                 | 否    |
| **TaskUpdate**           | 更新工作狀態、依賴項、詳細資訊或刪除工作                                                                                                                                            | 否    |
| **TodoWrite**            | 管理工作階段工作檢查清單。在非互動式模式和 [Agent SDK](/zh-TW/headless) 中可用；互動式工作階段改用 TaskCreate、TaskGet、TaskList 和 TaskUpdate                                                       | 否    |
| **ToolSearch**           | 當啟用 [tool search](/zh-TW/mcp#scale-with-mcp-tool-search) 時搜尋並載入延遲工具                                                                                             | 否    |
| **WebFetch**             | 從指定的 URL 提取內容                                                                                                                                                   | 是    |
| **WebSearch**            | 執行網路搜尋                                                                                                                                                          | 是    |
| **Write**                | 建立或覆蓋檔案                                                                                                                                                         | 是    |

權限規則可以使用 `/allowed-tools` 或在[權限設定](/zh-TW/settings#available-settings)中配置。另請參閱[工具特定權限規則](/zh-TW/permissions#tool-specific-permission-rules)。

### Bash 工具行為

Bash 工具使用以下持續性行為執行 shell 命令：

* **工作目錄持續**：當 Claude 變更工作目錄（例如 `cd /path/to/dir`）時，後續 Bash 命令將在該目錄中執行。您可以使用 `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1` 在每個命令後重設為專案目錄。
* **環境變數不持續**：在一個 Bash 命令中設定的環境變數（例如 `export MY_VAR=value`）在後續 Bash 命令中**不可用**。每個 Bash 命令在新的 shell 環境中執行。

若要在 Bash 命令中提供環境變數，您有**三個選項**：

**選項 1：在啟動 Claude Code 前啟用環境**（最簡單的方法）

在啟動 Claude Code 前在您的終端中啟用您的虛擬環境：

```bash  theme={null}
conda activate myenv
# 或：source /path/to/venv/bin/activate
claude
```

這適用於 shell 環境，但在 Claude 的 Bash 命令中設定的環境變數不會在命令之間持續。

**選項 2：在啟動 Claude Code 前設定 CLAUDE\_ENV\_FILE**（持續環境設定）

匯出包含您的環境設定的 shell 指令碼的路徑：

```bash  theme={null}
export CLAUDE_ENV_FILE=/path/to/env-setup.sh
claude
```

其中 `/path/to/env-setup.sh` 包含：

```bash  theme={null}
conda activate myenv
# 或：source /path/to/venv/bin/activate
# 或：export MY_VAR=value
```

Claude Code 將在每個 Bash 命令前來源此檔案，使環境在所有命令中持續。

**選項 3：使用 SessionStart hook**（專案特定配置）

在 `.claude/settings.json` 中配置：

```json  theme={null}
{
  "hooks": {
    "SessionStart": [{
      "matcher": "startup",
      "hooks": [{
        "type": "command",
        "command": "echo 'conda activate myenv' >> \"$CLAUDE_ENV_FILE\""
      }]
    }]
  }
}
```

hook 寫入 `$CLAUDE_ENV_FILE`，然後在每個 Bash 命令前來源。這對於團隊共享的專案配置很理想。

請參閱 [SessionStart hooks](/zh-TW/hooks#persist-environment-variables) 以了解有關選項 3 的更多詳細資訊。

### 使用 hooks 擴展工具

您可以使用 [Claude Code hooks](/zh-TW/hooks-guide) 在任何工具執行前或執行後執行自訂命令。

例如，您可以在 Claude 修改 Python 檔案後自動執行 Python 格式化程式，或透過阻止對某些路徑的 Write 操作來防止修改生產配置檔案。

## 另請參閱

* [權限](/zh-TW/permissions)：權限系統、規則語法、工具特定模式和 managed 政策
* [驗證](/zh-TW/authentication)：設定使用者對 Claude Code 的存取
* [故障排除](/zh-TW/troubleshooting)：常見配置問題的解決方案
