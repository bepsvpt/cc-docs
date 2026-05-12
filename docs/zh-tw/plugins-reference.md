> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Plugins 參考

> Claude Code 外掛系統的完整技術參考，包括架構、CLI 命令和元件規格。

<Tip>
  想要安裝外掛？請參閱 [探索和安裝外掛](/zh-TW/discover-plugins)。如需建立外掛，請參閱 [Plugins](/zh-TW/plugins)。如需發佈外掛，請參閱 [Plugin marketplaces](/zh-TW/plugin-marketplaces)。
</Tip>

本參考提供 Claude Code 外掛系統的完整技術規格，包括元件架構、CLI 命令和開發工具。

**plugin** 是一個自包含的目錄，包含擴展 Claude Code 功能的元件。Plugin 元件包括 skills、agents、hooks、MCP servers、LSP servers 和 monitors。

## Plugin 元件參考

### Skills

Plugins 將 skills 新增至 Claude Code，建立可由您或 Claude 叫用的 `/name` 快捷方式。

**位置**：plugin 根目錄中的 `skills/` 或 `commands/` 目錄

**檔案格式**：Skills 是包含 `SKILL.md` 的目錄；commands 是簡單的 markdown 檔案

**Skill 結構**：

```text theme={null}
skills/
├── pdf-processor/
│   ├── SKILL.md
│   ├── reference.md (optional)
│   └── scripts/ (optional)
└── code-reviewer/
    └── SKILL.md
```

**整合行為**：

* 安裝 plugin 時會自動探索 skills 和 commands
* Claude 可以根據任務上下文自動叫用它們
* Skills 可以在 SKILL.md 旁邊包含支援檔案

如需完整詳細資訊，請參閱 [Skills](/zh-TW/skills)。

### Agents

Plugins 可以提供專門的 subagents，用於 Claude 在適當時自動叫用的特定任務。

**位置**：plugin 根目錄中的 `agents/` 目錄

**檔案格式**：描述 agent 功能的 Markdown 檔案

**Agent 結構**：

```markdown theme={null}
---
name: agent-name
description: What this agent specializes in and when Claude should invoke it
model: sonnet
effort: medium
maxTurns: 20
disallowedTools: Write, Edit
---

Detailed system prompt for the agent describing its role, expertise, and behavior.
```

Plugin agents 支援 `name`、`description`、`model`、`effort`、`maxTurns`、`tools`、`disallowedTools`、`skills`、`memory`、`background` 和 `isolation` frontmatter 欄位。唯一有效的 `isolation` 值是 `"worktree"`。出於安全原因，plugin 提供的 agents 不支援 `hooks`、`mcpServers` 和 `permissionMode`。

**整合點**：

* Agents 出現在 `/agents` 介面中
* Claude 可以根據任務上下文自動叫用 agents
* Users 可以手動叫用 agents
* Plugin agents 與內建 Claude agents 一起運作

如需完整詳細資訊，請參閱 [Subagents](/zh-TW/sub-agents)。

### Hooks

Plugins 可以提供事件處理程式，自動回應 Claude Code 事件。

**位置**：plugin 根目錄中的 `hooks/hooks.json`，或在 plugin.json 中內聯

**格式**：具有事件匹配器和動作的 JSON 設定

**Hook 設定**：

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

Plugin hooks 回應與 [user-defined hooks](/zh-TW/hooks) 相同的生命週期事件：

| Event                 | When it fires                                                                                                                                          |
| :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`        | When a session begins or resumes                                                                                                                       |
| `Setup`               | When you start Claude Code with `--init-only`, or with `--init` or `--maintenance` in `-p` mode. For one-time preparation in CI or scripts             |
| `UserPromptSubmit`    | When you submit a prompt, before Claude processes it                                                                                                   |
| `UserPromptExpansion` | When a user-typed command expands into a prompt, before it reaches Claude. Can block the expansion                                                     |
| `PreToolUse`          | Before a tool call executes. Can block it                                                                                                              |
| `PermissionRequest`   | When a permission dialog appears                                                                                                                       |
| `PermissionDenied`    | When a tool call is denied by the auto mode classifier. Return `{retry: true}` to tell the model it may retry the denied tool call                     |
| `PostToolUse`         | After a tool call succeeds                                                                                                                             |
| `PostToolUseFailure`  | After a tool call fails                                                                                                                                |
| `PostToolBatch`       | After a full batch of parallel tool calls resolves, before the next model call                                                                         |
| `Notification`        | When Claude Code sends a notification                                                                                                                  |
| `SubagentStart`       | When a subagent is spawned                                                                                                                             |
| `SubagentStop`        | When a subagent finishes                                                                                                                               |
| `TaskCreated`         | When a task is being created via `TaskCreate`                                                                                                          |
| `TaskCompleted`       | When a task is being marked as completed                                                                                                               |
| `Stop`                | When Claude finishes responding                                                                                                                        |
| `StopFailure`         | When the turn ends due to an API error. Output and exit code are ignored                                                                               |
| `TeammateIdle`        | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                                     |
| `InstructionsLoaded`  | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session         |
| `ConfigChange`        | When a configuration file changes during a session                                                                                                     |
| `CwdChanged`          | When the working directory changes, for example when Claude executes a `cd` command. Useful for reactive environment management with tools like direnv |
| `FileChanged`         | When a watched file changes on disk. The `matcher` field specifies which filenames to watch                                                            |
| `WorktreeCreate`      | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                            |
| `WorktreeRemove`      | When a worktree is being removed, either at session exit or when a subagent finishes                                                                   |
| `PreCompact`          | Before context compaction                                                                                                                              |
| `PostCompact`         | After context compaction completes                                                                                                                     |
| `Elicitation`         | When an MCP server requests user input during a tool call                                                                                              |
| `ElicitationResult`   | After a user responds to an MCP elicitation, before the response is sent back to the server                                                            |
| `SessionEnd`          | When a session terminates                                                                                                                              |

**Hook 類型**：

* `command`：執行 shell 命令或指令碼
* `http`：將事件 JSON 作為 POST 請求傳送到 URL
* `mcp_tool`：在已設定的 [MCP server](/zh-TW/mcp) 上呼叫工具
* `prompt`：使用 LLM 評估提示（使用 `$ARGUMENTS` 佔位符表示上下文）
* `agent`：執行具有工具的 agentic 驗證器以進行複雜驗證任務

### MCP servers

Plugins 可以捆綁 Model Context Protocol (MCP) servers，將 Claude Code 與外部工具和服務連接。

**位置**：plugin 根目錄中的 `.mcp.json`，或在 plugin.json 中內聯

**格式**：標準 MCP server 設定

**MCP server 設定**：

```json theme={null}
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    },
    "plugin-api-client": {
      "command": "npx",
      "args": ["@company/mcp-server", "--plugin-mode"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

**整合行為**：

* 啟用 plugin 時，Plugin MCP servers 會自動啟動
* Servers 在 Claude 的工具組中顯示為標準 MCP 工具
* Server 功能與 Claude 的現有工具無縫整合
* Plugin servers 可以獨立於使用者 MCP servers 進行設定

### LSP servers

<Tip>
  想要使用 LSP plugins？從官方 marketplace 安裝它們：在 `/plugin` Discover 標籤中搜尋「lsp」。本節記錄如何為官方 marketplace 未涵蓋的語言建立 LSP plugins。
</Tip>

Plugins 可以提供 [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) (LSP) servers，在處理程式碼庫時為 Claude 提供即時程式碼智慧。

LSP 整合提供：

* **即時診斷**：Claude 在每次編輯後立即看到錯誤和警告
* **程式碼導航**：前往定義、尋找參考和懸停資訊
* **語言感知**：程式碼符號的類型資訊和文件

**位置**：plugin 根目錄中的 `.lsp.json`，或在 `plugin.json` 中內聯

**格式**：將語言伺服器名稱對應到其設定的 JSON 設定

**`.lsp.json` 檔案格式**：

```json theme={null}
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

**在 `plugin.json` 中內聯**：

```json theme={null}
{
  "name": "my-plugin",
  "lspServers": {
    "go": {
      "command": "gopls",
      "args": ["serve"],
      "extensionToLanguage": {
        ".go": "go"
      }
    }
  }
}
```

**必需欄位：**

| 欄位                    | 描述                        |
| :-------------------- | :------------------------ |
| `command`             | 要執行的 LSP 二進位檔（必須在 PATH 中） |
| `extensionToLanguage` | 將檔案副檔名對應到語言識別碼            |

**選用欄位：**

| 欄位                      | 描述                                          |
| :---------------------- | :------------------------------------------ |
| `args`                  | LSP server 的命令列引數                           |
| `transport`             | 通訊傳輸：`stdio`（預設）或 `socket`                  |
| `env`                   | 啟動 server 時要設定的環境變數                         |
| `initializationOptions` | 在初始化期間傳遞給 server 的選項                        |
| `settings`              | 透過 `workspace/didChangeConfiguration` 傳遞的設定 |
| `workspaceFolder`       | server 的工作區資料夾路徑                            |
| `startupTimeout`        | 等待 server 啟動的最長時間（毫秒）                       |
| `shutdownTimeout`       | 等待正常關閉的最長時間（毫秒）                             |
| `restartOnCrash`        | 如果 server 當機，是否自動重新啟動                       |
| `maxRestarts`           | 放棄前的最大重新啟動嘗試次數                              |

<Warning>
  **您必須單獨安裝語言伺服器二進位檔。** LSP plugins 設定 Claude Code 如何連接到語言伺服器，但它們不包括伺服器本身。如果您在 `/plugin` Errors 標籤中看到 `Executable not found in $PATH`，請為您的語言安裝所需的二進位檔。
</Warning>

**可用的 LSP plugins：**

| Plugin              | 語言伺服器                      | 安裝命令                                                                            |
| :------------------ | :------------------------- | :------------------------------------------------------------------------------ |
| `pyright-lsp`       | Pyright (Python)           | `pip install pyright` 或 `npm install -g pyright`                                |
| `typescript-lsp`    | TypeScript Language Server | `npm install -g typescript-language-server typescript`                          |
| `rust-analyzer-lsp` | rust-analyzer              | [參閱 rust-analyzer 安裝](https://rust-analyzer.github.io/manual.html#installation) |

先安裝語言伺服器，然後從 marketplace 安裝 plugin。

### Monitors

Plugins 可以宣告背景 monitors，Claude Code 在 plugin 啟用時自動啟動。每個 monitor 執行一個 shell 命令，持續整個工作階段，並將每個 stdout 行傳遞給 Claude 作為通知，以便 Claude 可以對日誌項目、狀態變更或輪詢事件做出反應，而無需被要求自行啟動監視。

Plugin monitors 使用與 [Monitor tool](/zh-TW/tools-reference#monitor-tool) 相同的機制，並共享其可用性限制。它們僅在互動式 CLI 工作階段中執行，以與 [hooks](#hooks) 相同的信任級別在未沙箱化的環境中執行，並在 Monitor tool 不可用的主機上被跳過。

<Note>
  Plugin monitors 需要 Claude Code v2.1.105 或更新版本。
</Note>

**位置**：plugin 根目錄中的 `monitors/monitors.json`，或在 `plugin.json` 中內聯

**格式**：monitor 項目的 JSON 陣列

以下 `monitors/monitors.json` 監視部署狀態端點和本機錯誤日誌：

```json theme={null}
[
  {
    "name": "deploy-status",
    "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/poll-deploy.sh ${user_config.api_endpoint}",
    "description": "Deployment status changes"
  },
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Application error log",
    "when": "on-skill-invoke:debug"
  }
]
```

若要內聯宣告 monitors，請將 `plugin.json` 中的 `experimental.monitors` 設定為相同的陣列。若要從非預設路徑載入，請將 `experimental.monitors` 設定為相對路徑字串，例如 `"./config/monitors.json"`。Monitors 是 [experimental component](#experimental-components)。

**必需欄位：**

| 欄位            | 描述                                                 |
| :------------ | :------------------------------------------------- |
| `name`        | 在 plugin 中唯一的識別碼。防止 plugin 重新載入或再次叫用 skill 時出現重複程序 |
| `command`     | 在工作階段工作目錄中作為持久背景程序執行的 shell 命令                     |
| `description` | 正在監視的內容的簡短摘要。顯示在任務面板和通知摘要中                         |

**選用欄位：**

| 欄位     | 描述                                                                                                                       |
| :----- | :----------------------------------------------------------------------------------------------------------------------- |
| `when` | 控制 monitor 何時啟動。`"always"` 在工作階段啟動和 plugin 重新載入時啟動它，是預設值。`"on-skill-invoke:<skill-name>"` 在此 plugin 中的命名 skill 首次被分派時啟動它 |

`command` 值支援與 MCP 和 LSP server 設定相同的 [variable substitutions](#environment-variables)：`${CLAUDE_PLUGIN_ROOT}`、`${CLAUDE_PLUGIN_DATA}`、`${CLAUDE_PROJECT_DIR}`、`${user_config.*}` 和環境中的任何 `${ENV_VAR}`。如果指令碼需要從 plugin 自己的目錄執行，請在命令前加上 `cd "${CLAUDE_PLUGIN_ROOT}" && `。

在工作階段中途停用 plugin 不會停止已在執行的 monitors。它們在工作階段結束時停止。

### Themes

Plugins 可以提供顏色主題，這些主題與內建預設值和使用者的本機主題一起出現在 `/theme` 中。主題是 `themes/` 中的 JSON 檔案，具有 `base` 預設值和稀疏的 `overrides` 顏色令牌對應。Themes 是 [experimental component](#experimental-components)。

```json theme={null}
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555",
    "success": "#50fa7b"
  }
}
```

選擇 plugin 主題會在使用者的設定中保留 `custom:<plugin-name>:<slug>`。Plugin 主題是唯讀的；在 `/theme` 中按 `Ctrl+E` 會將其複製到 `~/.claude/themes/`，以便使用者可以編輯副本。

***

## Plugin 安裝範圍

安裝 plugin 時，您選擇一個**範圍**，決定 plugin 的可用位置和誰可以使用它：

| 範圍        | 設定檔                                                | 使用案例                     |
| :-------- | :------------------------------------------------- | :----------------------- |
| `user`    | `~/.claude/settings.json`                          | 在所有專案中可用的個人 plugins（預設）  |
| `project` | `.claude/settings.json`                            | 透過版本控制共享的團隊 plugins      |
| `local`   | `.claude/settings.local.json`                      | 專案特定的 plugins，gitignored |
| `managed` | [Managed settings](/zh-TW/settings#settings-files) | 受管理的 plugins（唯讀，僅更新）     |

Plugins 使用與其他 Claude Code 設定相同的範圍系統。如需安裝說明和範圍旗標，請參閱 [安裝 plugins](/zh-TW/discover-plugins#install-plugins)。如需範圍的完整說明，請參閱 [Configuration scopes](/zh-TW/settings#configuration-scopes)。

***

## Plugin manifest 架構

`.claude-plugin/plugin.json` 檔案定義您的 plugin 的中繼資料和設定。本節記錄所有支援的欄位和選項。

manifest 是選用的。如果省略，Claude Code 會自動探索[預設位置](#file-locations-reference)中的元件，並從目錄名稱衍生 plugin 名稱。當您需要提供中繼資料或自訂元件路徑時，請使用 manifest。

### 完整架構

```json theme={null}
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "skills": "./custom/skills/",
  "commands": ["./custom/commands/special.md"],
  "agents": ["./custom/agents/reviewer.md"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json",
  "experimental": {
    "themes": "./themes/",
    "monitors": "./monitors.json"
  },
  "dependencies": [
    "helper-lib",
    { "name": "secrets-vault", "version": "~2.1.0" }
  ]
}
```

### 必需欄位

如果您包含 manifest，`name` 是唯一必需的欄位。

| 欄位     | 類型     | 描述                    | 範例                   |
| :----- | :----- | :-------------------- | :------------------- |
| `name` | string | 唯一識別碼（kebab-case，無空格） | `"deployment-tools"` |

此名稱用於命名空間元件。例如，在 UI 中，名稱為 `plugin-dev` 的 plugin 的 agent `agent-creator` 將顯示為 `plugin-dev:agent-creator`。

### 中繼資料欄位

| 欄位            | 類型     | 描述                                                                                                                                                                                               | 範例                                                                |
| :------------ | :----- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------- |
| `$schema`     | string | JSON Schema URL，用於編輯器自動完成和驗證。Claude Code 在載入時忽略此欄位。                                                                                                                                              | `"https://json.schemastore.org/claude-code-plugin-manifest.json"` |
| `version`     | string | 選用。語義版本。設定此項會將 plugin 固定到該版本字串，因此使用者只會在您提升版本時收到更新。如果省略，Claude Code 會回退到 git commit SHA，因此每個 commit 都被視為新版本。如果也在 marketplace 項目中設定，`plugin.json` 優先。請參閱[Version management](#version-management)。 | `"2.1.0"`                                                         |
| `description` | string | plugin 用途的簡短說明                                                                                                                                                                                   | `"Deployment automation tools"`                                   |
| `author`      | object | 作者資訊                                                                                                                                                                                             | `{"name": "Dev Team", "email": "dev@company.com"}`                |
| `homepage`    | string | 文件 URL                                                                                                                                                                                           | `"https://docs.example.com"`                                      |
| `repository`  | string | 原始程式碼 URL                                                                                                                                                                                        | `"https://github.com/user/plugin"`                                |
| `license`     | string | 授權識別碼                                                                                                                                                                                            | `"MIT"`、`"Apache-2.0"`                                            |
| `keywords`    | array  | 探索標籤                                                                                                                                                                                             | `["deployment", "ci-cd"]`                                         |

### 元件路徑欄位

| 欄位                      | 類型                    | 描述                                                                                                             | 範例                                                   |
| :---------------------- | :-------------------- | :------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------- |
| `skills`                | string\|array         | 包含 `<name>/SKILL.md` 的自訂 skill 目錄（除了預設 `skills/`）                                                              | `"./custom/skills/"`                                 |
| `commands`              | string\|array         | 自訂平面 `.md` skill 檔案或目錄（取代預設 `commands/`）                                                                       | `"./custom/cmd.md"` 或 `["./cmd1.md"]`                |
| `agents`                | string\|array         | 自訂 agent 檔案（取代預設 `agents/`）                                                                                    | `"./custom/agents/reviewer.md"`                      |
| `hooks`                 | string\|array\|object | Hook 設定路徑或內聯設定                                                                                                 | `"./my-extra-hooks.json"`                            |
| `mcpServers`            | string\|array\|object | MCP 設定路徑或內聯設定                                                                                                  | `"./my-extra-mcp-config.json"`                       |
| `outputStyles`          | string\|array         | 自訂輸出樣式檔案/目錄（取代預設 `output-styles/`）                                                                             | `"./styles/"`                                        |
| `lspServers`            | string\|array\|object | [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) 設定，用於程式碼智慧（前往定義、尋找參考等）       | `"./.lsp.json"`                                      |
| `experimental.themes`   | string\|array         | 色彩主題檔案/目錄（取代預設 `themes/`）。請參閱[Themes](#themes)                                                                 | `"./themes/"`                                        |
| `experimental.monitors` | string\|array         | 背景 [Monitor](/zh-TW/tools-reference#monitor-tool) 設定，在 plugin 啟用時自動啟動。請參閱[Monitors](#monitors)                 | `"./monitors.json"`                                  |
| `userConfig`            | object                | 在啟用時提示使用者的使用者可設定值。請參閱[User configuration](#user-configuration)                                                 | 請參閱下方                                                |
| `channels`              | array                 | 訊息注入的頻道宣告（Telegram、Slack、Discord 風格）。請參閱[Channels](#channels)                                                  | 請參閱下方                                                |
| `dependencies`          | array                 | 此 plugin 需要的其他 plugins，可選擇使用 semver 版本限制。請參閱[Constrain plugin dependency versions](/zh-TW/plugin-dependencies) | `[{ "name": "secrets-vault", "version": "~2.1.0" }]` |

### 實驗性元件

`experimental` 金鑰下的元件 `themes` 和 `monitors` 具有在版本之間穩定時可能會變更的 manifest 架構。您宣告它們的位置是一個單獨的遷移：頂層仍然有效，`claude plugin validate` 會發出警告，未來的版本將需要 `experimental.*`。

### User configuration

`userConfig` 欄位宣告 Claude Code 在啟用 plugin 時提示使用者的值。使用此方法而不是要求使用者手動編輯 `settings.json`。

```json theme={null}
{
  "userConfig": {
    "api_endpoint": {
      "type": "string",
      "title": "API endpoint",
      "description": "Your team's API endpoint"
    },
    "api_token": {
      "type": "string",
      "title": "API token",
      "description": "API authentication token",
      "sensitive": true
    }
  }
}
```

金鑰必須是有效的識別碼。每個選項支援這些欄位：

| 欄位            | 必需  | 描述                                                    |
| :------------ | :-- | :---------------------------------------------------- |
| `type`        | Yes | 其中之一：`string`、`number`、`boolean`、`directory` 或 `file` |
| `title`       | Yes | 設定對話方塊中顯示的標籤                                          |
| `description` | Yes | 欄位下方顯示的說明文字                                           |
| `sensitive`   | No  | 如果 `true`，遮罩輸入並將值儲存在安全儲存體中，而不是 `settings.json`        |
| `required`    | No  | 如果 `true`，當欄位為空時驗證失敗                                  |
| `default`     | No  | 使用者未提供任何內容時使用的值                                       |
| `multiple`    | No  | 對於 `string` 類型，允許字串陣列                                 |
| `min` / `max` | No  | `number` 類型的界限                                        |

每個值都可用於在 MCP 和 LSP server 設定、hook 命令、monitor 命令中替換為 `${user_config.KEY}`，以及（僅適用於非敏感值）skill 和 agent 內容。值也會匯出到 plugin 子程序作為 `CLAUDE_PLUGIN_OPTION_<KEY>` 環境變數。

非敏感值儲存在 `settings.json` 中的 `pluginConfigs[<plugin-id>].options` 下。敏感值進入系統鑰匙圈（或在鑰匙圈不可用的地方進入 `~/.claude/.credentials.json`）。鑰匙圈儲存與 OAuth 令牌共享，總限制約為 2 KB，因此請保持敏感值較小。

### Channels

`channels` 欄位讓 plugin 宣告一個或多個訊息頻道，將內容注入對話中。每個頻道繫結到 plugin 提供的 MCP server。

```json theme={null}
{
  "channels": [
    {
      "server": "telegram",
      "userConfig": {
        "bot_token": {
          "type": "string",
          "title": "Bot token",
          "description": "Telegram bot token",
          "sensitive": true
        },
        "owner_id": {
          "type": "string",
          "title": "Owner ID",
          "description": "Your Telegram user ID"
        }
      }
    }
  ]
}
```

`server` 欄位是必需的，必須與 plugin 的 `mcpServers` 中的金鑰相符。選用的每個頻道 `userConfig` 使用與頂層欄位相同的架構，讓 plugin 在啟用 plugin 時提示輸入機器人令牌或擁有者 ID。

### 路徑行為規則

自訂路徑是否取代或擴展 plugin 的預設目錄取決於欄位：

* **取代預設值**：`commands`、`agents`、`outputStyles`、`experimental.themes`、`experimental.monitors`。例如，當 manifest 指定 `commands` 時，預設 `commands/` 目錄不會被掃描。若要保留預設值並新增更多，請明確列出：`"commands": ["./commands/", "./extras/"]`
* **新增到預設值**：`skills`。預設 `skills/` 目錄始終被掃描，`skills` 中列出的目錄與其一起載入
* **自有合併規則**：[hooks](#hooks)、[MCP servers](#mcp-servers) 和 [LSP servers](#lsp-servers)。請參閱每個部分以了解多個來源如何組合

對於所有路徑欄位：

* 所有路徑必須相對於 plugin 根目錄，並以 `./` 開頭
* 來自自訂路徑的元件使用相同的命名和命名空間規則
* 可以將多個路徑指定為陣列
* 當 skill 路徑指向直接包含 `SKILL.md` 的目錄時，例如 `"skills": ["./"]` 指向 plugin 根目錄，frontmatter 中的 `name` 欄位決定 skill 的叫用名稱。這提供了一個穩定的名稱，無論安裝目錄如何。如果 frontmatter 中未設定 `name`，目錄基名將用作後備。

**路徑範例**：

```json theme={null}
{
  "commands": [
    "./specialized/deploy.md",
    "./utilities/batch-process.md"
  ],
  "agents": [
    "./custom-agents/reviewer.md",
    "./custom-agents/tester.md"
  ]
}
```

### 環境變數

Claude Code 提供三個變數用於參考路徑。所有變數都在 skill 內容、agent 內容、hook 命令、monitor 命令以及 MCP 或 LSP server 設定中出現的任何地方內聯替換。所有變數也會匯出為環境變數到 hook 程序和 MCP 或 LSP server 子程序。

**`${CLAUDE_PLUGIN_ROOT}`**：plugin 安裝目錄的絕對路徑。使用此方法參考與 plugin 捆綁的指令碼、二進位檔和設定檔。在 hook 命令中，使用[執行形式](/zh-TW/hooks#exec-form-and-shell-form)搭配 `args`，以便路徑作為一個引數傳遞，無需引號。在 shell 形式的 hooks 和 monitor 命令中，將其包裝在雙引號中，如 `"${CLAUDE_PLUGIN_ROOT}"`。此路徑在 plugin 更新時會變更。前一個版本的目錄在更新後約七天內保留在磁碟上，然後才進行清理，但應將其視為暫時性的，不要在此處寫入狀態。

當 plugin 在工作階段中途更新時，hook 命令、monitors、MCP servers 和 LSP servers 會繼續使用前一個版本的路徑。執行 `/reload-plugins` 以將 hooks、MCP servers 和 LSP servers 切換到新路徑；monitors 需要工作階段重新啟動。

**`${CLAUDE_PLUGIN_DATA}`**：用於在更新後保留的 plugin 狀態的持久目錄。使用此方法用於已安裝的依賴項，例如 `node_modules` 或 Python 虛擬環境、生成的程式碼、快取和任何應在 plugin 版本之間保留的其他檔案。首次參考此變數時會自動建立目錄。

**`${CLAUDE_PROJECT_DIR}`**：專案根目錄。這是 hooks 在其 `CLAUDE_PROJECT_DIR` 變數中接收的相同目錄。使用此方法參考專案本地指令碼或設定檔。包裝在引號中以處理包含空格的路徑，例如 `"${CLAUDE_PROJECT_DIR}/scripts/server.sh"`。MCP servers 也可以呼叫 MCP `roots/list` 請求，該請求會傳回啟動 Claude Code 的目錄。

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

#### 持久資料目錄

`${CLAUDE_PLUGIN_DATA}` 目錄解析為 `~/.claude/plugins/data/{id}/`，其中 `{id}` 是 plugin 識別碼，其中 `a-z`、`A-Z`、`0-9`、`_` 和 `-` 以外的字元被替換為 `-`。對於安裝為 `formatter@my-marketplace` 的 plugin，目錄是 `~/.claude/plugins/data/formatter-my-marketplace/`。

常見用途是一次安裝語言依賴項並在工作階段和 plugin 更新中重複使用它們。因為資料目錄的壽命超過任何單一 plugin 版本，僅檢查目錄存在無法偵測更新何時變更 plugin 的依賴項清單。建議的模式是比較捆綁的清單與資料目錄中的副本，並在它們不同時重新安裝。

此 `SessionStart` hook 在第一次執行時安裝 `node_modules`，並在 plugin 更新包含變更的 `package.json` 時再次安裝：

```json theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cd \"${CLAUDE_PLUGIN_DATA}\" && cp \"${CLAUDE_PLUGIN_ROOT}/package.json\" . && npm install) || rm -f \"${CLAUDE_PLUGIN_DATA}/package.json\""
          }
        ]
      }
    ]
  }
}
```

`diff` 在儲存的副本遺失或與捆綁的副本不同時以非零值退出，涵蓋第一次執行和依賴項變更更新。如果 `npm install` 失敗，尾部 `rm` 會移除複製的清單，以便下一個工作階段重試。

捆綁在 `${CLAUDE_PLUGIN_ROOT}` 中的指令碼可以針對保留的 `node_modules` 執行：

```json theme={null}
{
  "mcpServers": {
    "routines": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
      "env": {
        "NODE_PATH": "${CLAUDE_PLUGIN_DATA}/node_modules"
      }
    }
  }
}
```

當您從最後一個安裝 plugin 的範圍卸載 plugin 時，資料目錄會自動刪除。`/plugin` 介面顯示目錄大小並在刪除前提示。CLI 預設刪除；傳遞 [`--keep-data`](#plugin-uninstall) 以保留它。

***

## Plugin 快取和檔案解析

Plugins 可以透過以下兩種方式之一指定：

* 透過 `claude --plugin-dir` 或 `claude --plugin-url`，在工作階段期間。
* 透過 marketplace，為未來的工作階段安裝。

出於安全和驗證目的，Claude Code 將 *marketplace* plugins 複製到使用者的本機 **plugin 快取**（`~/.claude/plugins/cache`），而不是就地使用它們。在開發參考外部檔案的 plugins 時，理解此行為很重要。

每個已安裝的版本是快取中的單獨目錄。當您更新或卸載 plugin 時，先前的版本目錄被標記為孤立，並在 7 天後自動移除。寬限期讓已載入舊版本的並行 Claude Code 工作階段繼續執行而不出錯。

Claude 的 Glob 和 Grep 工具在搜尋期間跳過孤立的版本目錄，因此檔案結果不包含過時的 plugin 程式碼。

### 路徑遍歷限制

已安裝的 plugins 無法參考其目錄外的檔案。遍歷 plugin 根目錄外的路徑（例如 `../shared-utils`）在安裝後將無法運作，因為這些外部檔案不會複製到快取中。

### 使用 symlinks 在 marketplace 內共享檔案

如果您的 plugin 需要與同一 marketplace 的其他部分共享檔案，您可以在 plugin 目錄內建立符號連結。當 plugin 被複製到快取時，symlink 的處理方式取決於其目標的解析位置：

* **在 plugin 自身目錄內：** symlink 在快取中被保留為相對 symlink，因此在執行時繼續解析到複製的目標。
* **在同一 marketplace 內的其他位置：** symlink 被取消參考。目標的內容被複製到快取中以取代它。這讓 meta-plugin 的 `skills/` 目錄可以連結到 marketplace 中其他 plugins 定義的 skills。
* **在 marketplace 外：** symlink 因安全考量而被跳過。這防止 plugins 將任意主機檔案（例如系統路徑）拉入快取。

對於使用 `--plugin-dir` 安裝或從本機路徑安裝的 plugins，只有解析在 plugin 自身目錄內的 symlinks 被保留。所有其他的都被跳過。

以下命令從 marketplace plugin 內建立到由同級 plugin 定義的共享 skill 的連結。在 Windows 上，從提升的命令提示字元使用 `mklink /D` 或啟用開發人員模式：

```bash theme={null}
ln -s ../../shared-plugin/skills/foo ./skills/foo
```

這在維持快取系統安全優勢的同時提供了靈活性。

***

## Plugin 目錄結構

### 標準 plugin 配置

完整的 plugin 遵循此結構：

```text theme={null}
enterprise-plugin/
├── .claude-plugin/           # Metadata directory (optional)
│   └── plugin.json             # plugin manifest
├── skills/                   # Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── commands/                 # Skills as flat .md files
│   ├── status.md
│   └── logs.md
├── agents/                   # Subagent definitions
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── output-styles/            # Output style definitions
│   └── terse.md
├── themes/                   # Color theme definitions
│   └── dracula.json
├── monitors/                 # Background monitor configurations
│   └── monitors.json
├── hooks/                    # Hook configurations
│   ├── hooks.json           # Main hook config
│   └── security-hooks.json  # Additional hooks
├── bin/                      # Plugin executables added to PATH
│   └── my-tool               # Invokable as bare command in Bash tool
├── settings.json            # Default settings for the plugin
├── .mcp.json                # MCP server definitions
├── .lsp.json                # LSP server configurations
├── scripts/                 # Hook and utility scripts
│   ├── security-scan.sh
│   ├── format-code.py
│   └── deploy.js
├── LICENSE                  # License file
└── CHANGELOG.md             # Version history
```

<Warning>
  `.claude-plugin/` 目錄包含 `plugin.json` 檔案。所有其他目錄（commands/、agents/、skills/、output-styles/、themes/、monitors/、hooks/）必須位於 plugin 根目錄，而不是在 `.claude-plugin/` 內。
</Warning>

plugin 根目錄的 `CLAUDE.md` 檔案不會作為專案內容載入。Plugin 透過 skills、agents 和 hooks 貢獻內容，而不是透過 CLAUDE.md。若要提供載入到 Claude 內容中的指示，請將其放在 [skill](#skills) 中。

### 檔案位置參考

| 元件                | 預設位置                         | 用途                                                                                                                         |
| :---------------- | :--------------------------- | :------------------------------------------------------------------------------------------------------------------------- |
| **Manifest**      | `.claude-plugin/plugin.json` | Plugin 中繼資料和設定（選用）                                                                                                         |
| **Skills**        | `skills/`                    | 具有 `<name>/SKILL.md` 結構的 Skills                                                                                            |
| **Commands**      | `commands/`                  | 作為平面 Markdown 檔案的 Skills。新 plugins 使用 `skills/`                                                                            |
| **Agents**        | `agents/`                    | Subagent Markdown 檔案                                                                                                       |
| **Output styles** | `output-styles/`             | 輸出樣式定義                                                                                                                     |
| **Themes**        | `themes/`                    | 色彩主題定義                                                                                                                     |
| **Hooks**         | `hooks/hooks.json`           | Hook 設定                                                                                                                    |
| **MCP servers**   | `.mcp.json`                  | MCP server 定義                                                                                                              |
| **LSP servers**   | `.lsp.json`                  | 語言伺服器設定                                                                                                                    |
| **Monitors**      | `monitors/monitors.json`     | 背景 monitor 設定                                                                                                              |
| **Executables**   | `bin/`                       | 新增到 Bash tool 的 `PATH` 的可執行檔。此處的檔案在 plugin 啟用時可在任何 Bash tool 呼叫中作為裸命令叫用                                                    |
| **Settings**      | `settings.json`              | 啟用 plugin 時套用的預設設定。目前僅支援 [`agent`](/zh-TW/sub-agents) 和 [`subagentStatusLine`](/zh-TW/statusline#subagent-status-lines) 金鑰 |

***

## CLI 命令參考

Claude Code 提供 CLI 命令用於非互動式 plugin 管理，適用於指令碼和自動化。

### plugin install

從可用的 marketplaces 安裝 plugin。

```bash theme={null}
claude plugin install <plugin> [options]
```

**引數：**

* `<plugin>`：Plugin 名稱或 `plugin-name@marketplace-name` 用於特定 marketplace

**選項：**

| 選項                    | 描述                              | 預設     |
| :-------------------- | :------------------------------ | :----- |
| `-s, --scope <scope>` | 安裝範圍：`user`、`project` 或 `local` | `user` |
| `-h, --help`          | 顯示命令說明                          |        |

範圍決定已安裝的 plugin 新增到哪個設定檔。例如，`--scope project` 寫入 `.claude/settings.json` 中的 `enabledPlugins`，使 plugin 對克隆專案存放庫的每個人都可用。

**範例：**

```bash theme={null}
# Install to user scope (default)
claude plugin install formatter@my-marketplace

# Install to project scope (shared with team)
claude plugin install formatter@my-marketplace --scope project

# Install to local scope (gitignored)
claude plugin install formatter@my-marketplace --scope local
```

### plugin uninstall

移除已安裝的 plugin。

```bash theme={null}
claude plugin uninstall <plugin> [options]
```

**引數：**

* `<plugin>`：Plugin 名稱或 `plugin-name@marketplace-name`

**選項：**

| 選項                    | 描述                                                                  | 預設     |
| :-------------------- | :------------------------------------------------------------------ | :----- |
| `-s, --scope <scope>` | 從範圍卸載：`user`、`project` 或 `local`                                    | `user` |
| `--keep-data`         | 保留 plugin 的 [persistent data directory](#persistent-data-directory) |        |
| `--prune`             | 同時移除其他 plugin 不需要的自動安裝相依性。請參閱 [plugin prune](#plugin-prune)         |        |
| `-y, --yes`           | 跳過 `--prune` 確認提示。當 stdin 不是 TTY 時為必需                               |        |
| `-h, --help`          | 顯示命令說明                                                              |        |

**別名：** `remove`、`rm`

預設情況下，從最後一個剩餘範圍卸載也會刪除 plugin 的 `${CLAUDE_PLUGIN_DATA}` 目錄。使用 `--keep-data` 保留它，例如在測試新版本後重新安裝時。

### plugin prune

移除不再被任何已安裝 plugin 所需的自動安裝 plugin 相依性。Claude Code 為滿足另一個 plugin 的 [`dependencies`](/zh-TW/plugin-dependencies) 欄位而引入的相依性會被移除；您直接安裝的 plugins 永遠不會被觸及。

```bash theme={null}
claude plugin prune [options]
```

**選項：**

| 選項                    | 描述                                 | 預設     |
| :-------------------- | :--------------------------------- | :----- |
| `-s, --scope <scope>` | 在範圍進行修剪：`user`、`project` 或 `local` | `user` |
| `--dry-run`           | 列出將被移除的內容而不實際移除                    |        |
| `-y, --yes`           | 跳過確認提示。當 stdin 不是 TTY 時為必需         |        |
| `-h, --help`          | 顯示命令說明                             |        |

**別名：** `autoremove`

該命令列出孤立的相依性並在移除前要求確認。若要在一個步驟中移除 plugin 並清理其相依性，請執行 `claude plugin uninstall <plugin> --prune`。

<Note>
  `claude plugin prune` 需要 Claude Code v2.1.121 或更新版本。
</Note>

### plugin enable

啟用已停用的 plugin。

```bash theme={null}
claude plugin enable <plugin> [options]
```

**引數：**

* `<plugin>`：Plugin 名稱或 `plugin-name@marketplace-name`

**選項：**

| 選項                    | 描述                                | 預設     |
| :-------------------- | :-------------------------------- | :----- |
| `-s, --scope <scope>` | 要啟用的範圍：`user`、`project` 或 `local` | `user` |
| `-h, --help`          | 顯示命令說明                            |        |

### plugin disable

停用 plugin 而不卸載它。

```bash theme={null}
claude plugin disable <plugin> [options]
```

**引數：**

* `<plugin>`：Plugin 名稱或 `plugin-name@marketplace-name`

**選項：**

| 選項                    | 描述                                | 預設     |
| :-------------------- | :-------------------------------- | :----- |
| `-s, --scope <scope>` | 要停用的範圍：`user`、`project` 或 `local` | `user` |
| `-h, --help`          | 顯示命令說明                            |        |

### plugin update

將 plugin 更新到最新版本。

```bash theme={null}
claude plugin update <plugin> [options]
```

**引數：**

* `<plugin>`：Plugin 名稱或 `plugin-name@marketplace-name`

**選項：**

| 選項                    | 描述                                          | 預設     |
| :-------------------- | :------------------------------------------ | :----- |
| `-s, --scope <scope>` | 要更新的範圍：`user`、`project`、`local` 或 `managed` | `user` |
| `-h, --help`          | 顯示命令說明                                      |        |

***

### plugin list

列出已安裝的 plugins 及其版本、來源 marketplace 和啟用狀態。

```bash theme={null}
claude plugin list [options]
```

**選項：**

| 選項            | 描述                                        | 預設 |
| :------------ | :---------------------------------------- | :- |
| `--json`      | 輸出為 JSON                                  |    |
| `--available` | 包含來自 marketplaces 的可用 plugins。需要 `--json` |    |
| `-h, --help`  | 顯示命令說明                                    |    |

### plugin details

顯示 plugin 的元件清單和預計的 token 成本。輸出列出 plugin 貢獻的所有元件，分組為 Skills（技能和命令）、Agents、Hooks 和 MCP servers，以及它為每個工作階段新增多少 tokens 的估計。

```bash theme={null}
claude plugin details <name>
```

**引數：**

* `<name>`：Plugin 名稱或 `plugin-name@marketplace-name`

**選項：**

| 選項           | 描述     | 預設 |
| :----------- | :----- | :- |
| `-h, --help` | 顯示命令說明 |    |

輸出為每個元件顯示兩個成本數字：

* **Always-on：** plugin 的列表文字新增到每個工作階段的 tokens，例如技能描述、agent 描述和命令名稱，無論任何元件是否觸發。
* **On-invoke：** 元件觸發時的成本。按元件顯示，而不是作為 plugin 總計，因為典型的工作階段只會呼叫元件的子集。

此範例顯示具有兩個技能的 plugin 的輸出外觀：

```
security-guidance 1.2.0
  Real-time security analysis for Claude Code sessions
  Source: security-guidance@claude-code-marketplace

Component inventory
  Skills (2)  scan-dependencies, review-changes
  Agents (0)
  Hooks (1)  (harness-only — no model context cost)
  MCP servers (0)

Projected token cost
  Always-on:   ~180 tok   added to every session

Per-component (rounded)
  component            always-on  on-invoke
  scan-dependencies        ~100      ~2400
  review-changes            ~80      ~1800

  On-invoke cost is paid each time a skill or agent fires.
  Token counts are estimates and may differ from actual usage.
```

always-on 總計是透過您的作用中模型的 `count_tokens` API 計算的。按元件的數字按比例從該總計縮放。如果 API 無法連線，該命令會回退到基於字元的估計。

### plugin tag

為目前目錄中的 plugin 建立發行版 git 標籤。從 plugin 的資料夾內執行。請參閱 [Tag plugin releases](/zh-TW/plugin-dependencies#tag-plugin-releases-for-version-resolution)。

```bash theme={null}
claude plugin tag [options]
```

**選項：**

| 選項            | 描述                 | 預設 |
| :------------ | :----------------- | :- |
| `--push`      | 建立標籤後將其推送到遠端       |    |
| `--dry-run`   | 列印將被標籤的內容而不建立標籤    |    |
| `-f, --force` | 即使工作樹髒污或標籤已存在也建立標籤 |    |
| `-h, --help`  | 顯示命令說明             |    |

***

## 偵錯和開發工具

### 偵錯命令

使用 `claude --debug` 查看 plugin 載入詳細資訊：

這會顯示：

* 正在載入哪些 plugins
* plugin manifests 中的任何錯誤
* Skill、agent 和 hook 註冊
* MCP server 初始化

### 常見問題

| 問題                                  | 原因                         | 解決方案                                                                                                                            |
| :---------------------------------- | :------------------------- | :------------------------------------------------------------------------------------------------------------------------------ |
| Plugin 未載入                          | 無效的 `plugin.json`          | 執行 `claude plugin validate` 或 `/plugin validate` 檢查 `plugin.json`、skill/agent/command frontmatter 和 `hooks/hooks.json` 的語法和架構錯誤 |
| Skills 未出現                          | 目錄結構錯誤                     | 確保 `skills/` 或 `commands/` 在 plugin 根目錄，而不是在 `.claude-plugin/` 中                                                                |
| Hooks 未觸發                           | 指令碼不可執行                    | 執行 `chmod +x script.sh`                                                                                                         |
| MCP server 失敗                       | 缺少 `${CLAUDE_PLUGIN_ROOT}` | 對所有 plugin 路徑使用變數                                                                                                               |
| 路徑錯誤                                | 使用了絕對路徑                    | 所有路徑必須是相對的，並以 `./` 開頭                                                                                                           |
| LSP `Executable not found in $PATH` | 未安裝語言伺服器                   | 安裝二進位檔（例如 `npm install -g typescript-language-server typescript`）                                                               |

### 範例錯誤訊息

**Manifest 驗證錯誤**：

* `Invalid JSON syntax: Unexpected token } in JSON at position 142`：檢查是否缺少逗號、多餘逗號或未引用的字串
* `Plugin has an invalid manifest file at .claude-plugin/plugin.json. Validation errors: name: Required`：缺少必需欄位
* `Plugin has a corrupt manifest file at .claude-plugin/plugin.json. JSON parse error: ...`：JSON 語法錯誤

**Plugin 載入錯誤**：

* `Warning: No commands found in plugin my-plugin custom directory: ./cmds. Expected .md files or SKILL.md in subdirectories.`：命令路徑存在但不包含有效的命令檔案
* `Plugin directory not found at path: ./plugins/my-plugin. Check that the marketplace entry has the correct path.`：marketplace.json 中的 `source` 路徑指向不存在的目錄
* `Plugin my-plugin has conflicting manifests: both plugin.json and marketplace entry specify components.`：移除重複的元件定義或移除 marketplace 項目中的 `strict: false`

### Hook 疑難排解

**Hook 指令碼未執行**：

1. 檢查指令碼是否可執行：`chmod +x ./scripts/your-script.sh`
2. 驗證 shebang 行：第一行應為 `#!/bin/bash` 或 `#!/usr/bin/env bash`
3. 檢查路徑是否使用 `${CLAUDE_PLUGIN_ROOT}`：`"command": "${CLAUDE_PLUGIN_ROOT}/scripts/your-script.sh"`
4. 手動測試指令碼：`./scripts/your-script.sh`

**Hook 未在預期事件上觸發**：

1. 驗證事件名稱是否正確（區分大小寫）：`PostToolUse`，而不是 `postToolUse`
2. 檢查匹配器模式是否與您的工具相符：`"matcher": "Write|Edit"` 用於檔案操作
3. 確認 hook 類型有效：`command`、`http`、`mcp_tool`、`prompt` 或 `agent`

### MCP server 疑難排解

**Server 未啟動**：

1. 檢查命令是否存在且可執行
2. 驗證所有路徑是否使用 `${CLAUDE_PLUGIN_ROOT}` 變數
3. 檢查 MCP server 日誌：`claude --debug` 顯示初始化錯誤
4. 在 Claude Code 外手動測試 server

**Server 工具未出現**：

1. 確保 server 在 `.mcp.json` 或 `plugin.json` 中正確設定
2. 驗證 server 是否正確實現 MCP 協定
3. 檢查偵錯輸出中的連接逾時

### 目錄結構錯誤

**症狀**：Plugin 載入但元件（skills、agents、hooks）遺失。

**正確結構**：元件必須位於 plugin 根目錄，而不是在 `.claude-plugin/` 內。只有 `plugin.json` 屬於 `.claude-plugin/`。

```text theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json      ← Only manifest here
├── commands/            ← At root level
├── agents/              ← At root level
└── hooks/               ← At root level
```

如果您的元件在 `.claude-plugin/` 內，請將它們移到 plugin 根目錄。

**偵錯檢查清單**：

1. 執行 `claude --debug` 並查找「loading plugin」訊息
2. 檢查每個元件目錄是否列在偵錯輸出中
3. 驗證檔案權限允許讀取 plugin 檔案

***

## 發佈和版本控制參考

### 版本管理

Claude Code 使用 plugin 的版本作為快取金鑰，以決定是否有可用的更新。當您執行 `/plugin update` 或自動更新觸發時，Claude Code 會計算目前版本，如果與已安裝的版本相符，則跳過更新。

版本會從以下第一個設定的項目解析：

1. Plugin 的 `plugin.json` 中的 `version` 欄位
2. Plugin 在 `marketplace.json` 中的 marketplace 項目中的 `version` 欄位
3. Plugin 來源的 git commit SHA，適用於 git 託管 marketplace 中的 `github`、`url`、`git-subdir` 和相對路徑來源
4. `unknown`，適用於 `npm` 來源或不在 git 儲存庫內的本機目錄

這為您提供了兩種方式來版本化 plugin：

| 方法                | 如何操作                                          | 更新行為                                                                     | 最適合                  |
| :---------------- | :-------------------------------------------- | :----------------------------------------------------------------------- | :------------------- |
| **明確版本**          | 在 `plugin.json` 中設定 `"version": "2.1.0"`      | 使用者只有在您提升此欄位時才會獲得更新。推送新的 commit 而不提升版本沒有效果，`/plugin update` 會報告「已是最新版本」。 | 具有穩定發行週期的已發佈 plugin  |
| **Commit-SHA 版本** | 從 `plugin.json` 和 marketplace 項目中省略 `version` | 使用者在每次 plugin 的 git 來源有新 commit 時都會獲得更新                                  | 正在積極開發中的內部或團隊 plugin |

<Warning>
  如果您在 `plugin.json` 中設定 `version`，每次您想讓使用者接收變更時，都必須提升它。僅推送新的 commit 是不夠的，因為 Claude Code 會看到相同的版本字串並保留快取副本。如果您正在快速迭代，請保持 `version` 未設定，以便改為使用 git commit SHA。
</Warning>

如果您使用明確版本，請遵循 [semantic versioning](https://semver.org)（`MAJOR.MINOR.PATCH`）：針對破壞性變更提升 MAJOR，針對新功能提升 MINOR，針對錯誤修正提升 PATCH。在 `CHANGELOG.md` 中記錄變更。

***

## 另請參閱

* [Plugins](/zh-TW/plugins) - 教學和實際使用
* [Plugin marketplaces](/zh-TW/plugin-marketplaces) - 建立和管理 marketplaces
* [Skills](/zh-TW/skills) - Skill 開發詳細資訊
* [Subagents](/zh-TW/sub-agents) - Agent 設定和功能
* [Hooks](/zh-TW/hooks) - 事件處理和自動化
* [MCP](/zh-TW/mcp) - 外部工具整合
* [Settings](/zh-TW/settings) - Plugins 的設定選項
