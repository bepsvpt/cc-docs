> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Hooks 參考

> Claude Code hook 事件、配置架構、JSON 輸入/輸出格式、退出代碼、非同步 hooks、HTTP hooks、提示 hooks 和 MCP 工具 hooks 的參考。

<Tip>
  如需快速入門指南和範例，請參閱 [使用 hooks 自動化工作流程](/zh-TW/hooks-guide)。
</Tip>

Hooks 是使用者定義的 shell 命令、HTTP 端點或 LLM 提示，在 Claude Code 生命週期的特定時間點自動執行。使用此參考來查詢事件架構、配置選項、JSON 輸入/輸出格式，以及非同步 hooks、HTTP hooks 和 MCP 工具 hooks 等進階功能。如果您是第一次設定 hooks，請改為從 [指南](/zh-TW/hooks-guide) 開始。

## Hook 生命週期

Hooks 在 Claude Code 工作階段期間的特定時間點觸發。當事件觸發且匹配器匹配時，Claude Code 會將有關該事件的 JSON 上下文傳遞給您的 hook 處理程式。對於命令 hooks，輸入會到達 stdin。對於 HTTP hooks，它會作為 POST 請求正文到達。您的處理程式可以檢查輸入、採取行動，並可選擇性地返回決定。某些事件每個工作階段觸發一次，而其他事件在代理迴圈內重複觸發：

<div style={{maxWidth: "500px", margin: "0 auto"}}>
  <Frame>
    <img src="https://mintcdn.com/claude-code/2YzYcIR7V1VggfgF/images/hooks-lifecycle.svg?fit=max&auto=format&n=2YzYcIR7V1VggfgF&q=85&s=3004e6c5dc95c4fe7fa3eb40fdc4176c" alt="Hook 生命週期圖表，顯示從 SessionStart 通過代理迴圈（PreToolUse、PermissionRequest、PostToolUse、SubagentStart/Stop、TaskCompleted）到 Stop 或 StopFailure、TeammateIdle、PreCompact、PostCompact 和 SessionEnd 的 hooks 序列，Elicitation 和 ElicitationResult 嵌套在 MCP 工具執行內，WorktreeCreate、WorktreeRemove、Notification、ConfigChange 和 InstructionsLoaded 作為獨立非同步事件" width="520" height="1100" data-path="images/hooks-lifecycle.svg" />
  </Frame>
</div>

下表總結了每個事件何時觸發。[Hook 事件](#hook-events) 部分記錄了每個事件的完整輸入架構和決定控制選項。

| Event                | When it fires                                                                                                                                  |
| :------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`       | When a session begins or resumes                                                                                                               |
| `UserPromptSubmit`   | When you submit a prompt, before Claude processes it                                                                                           |
| `PreToolUse`         | Before a tool call executes. Can block it                                                                                                      |
| `PermissionRequest`  | When a permission dialog appears                                                                                                               |
| `PostToolUse`        | After a tool call succeeds                                                                                                                     |
| `PostToolUseFailure` | After a tool call fails                                                                                                                        |
| `Notification`       | When Claude Code sends a notification                                                                                                          |
| `SubagentStart`      | When a subagent is spawned                                                                                                                     |
| `SubagentStop`       | When a subagent finishes                                                                                                                       |
| `Stop`               | When Claude finishes responding                                                                                                                |
| `StopFailure`        | When the turn ends due to an API error. Output and exit code are ignored                                                                       |
| `TeammateIdle`       | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                             |
| `TaskCompleted`      | When a task is being marked as completed                                                                                                       |
| `InstructionsLoaded` | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session |
| `ConfigChange`       | When a configuration file changes during a session                                                                                             |
| `WorktreeCreate`     | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                    |
| `WorktreeRemove`     | When a worktree is being removed, either at session exit or when a subagent finishes                                                           |
| `PreCompact`         | Before context compaction                                                                                                                      |
| `PostCompact`        | After context compaction completes                                                                                                             |
| `Elicitation`        | When an MCP server requests user input during a tool call                                                                                      |
| `ElicitationResult`  | After a user responds to an MCP elicitation, before the response is sent back to the server                                                    |
| `SessionEnd`         | When a session terminates                                                                                                                      |

### Hook 如何解析

為了了解這些部分如何組合在一起，請考慮此 `PreToolUse` hook，它會阻止破壞性 shell 命令。該 hook 在每次 Bash 工具呼叫之前執行 `block-rm.sh`：

```json  theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/block-rm.sh"
          }
        ]
      }
    ]
  }
}
```

該指令碼從 stdin 讀取 JSON 輸入，提取命令，如果包含 `rm -rf`，則返回 `permissionDecision` 為 `"deny"`：

```bash  theme={null}
#!/bin/bash
# .claude/hooks/block-rm.sh
COMMAND=$(jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q 'rm -rf'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Destructive command blocked by hook"
    }
  }'
else
  exit 0  # allow the command
fi
```

現在假設 Claude Code 決定執行 `Bash "rm -rf /tmp/build"`。以下是發生的情況：

<Frame>
  <img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/hook-resolution.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=ad667ee6d86ab2276aa48a4e73e220df" alt="Hook 解析流程：PreToolUse 事件觸發，匹配器檢查 Bash 匹配，hook 處理程式執行，結果返回到 Claude Code" width="780" height="290" data-path="images/hook-resolution.svg" />
</Frame>

<Steps>
  <Step title="事件觸發">
    `PreToolUse` 事件觸發。Claude Code 將工具輸入作為 JSON 在 stdin 上發送到 hook：

    ```json  theme={null}
    { "tool_name": "Bash", "tool_input": { "command": "rm -rf /tmp/build" }, ... }
    ```
  </Step>

  <Step title="匹配器檢查">
    匹配器 `"Bash"` 與工具名稱匹配，因此 `block-rm.sh` 執行。如果您省略匹配器或使用 `"*"`，hook 會在事件的每次出現時執行。只有當定義了匹配器且不匹配時，hooks 才會跳過。
  </Step>

  <Step title="Hook 處理程式執行">
    該指令碼從輸入中提取 `"rm -rf /tmp/build"` 並找到 `rm -rf`，因此它將決定列印到 stdout：

    ```json  theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Destructive command blocked by hook"
      }
    }
    ```

    如果命令是安全的（例如 `npm test`），指令碼會改為執行 `exit 0`，這告訴 Claude Code 允許工具呼叫而無需進一步操作。
  </Step>

  <Step title="Claude Code 根據結果採取行動">
    Claude Code 讀取 JSON 決定，阻止工具呼叫，並向 Claude 顯示原因。
  </Step>
</Steps>

下面的 [配置](#configuration) 部分記錄了完整架構，每個 [hook 事件](#hook-events) 部分記錄了您的命令接收的輸入以及它可以返回的輸出。

## 配置

Hooks 在 JSON 設定檔中定義。配置有三個嵌套層級：

1. 選擇要回應的 [hook 事件](#hook-events)，例如 `PreToolUse` 或 `Stop`
2. 新增 [匹配器群組](#matcher-patterns) 以篩選何時觸發，例如'僅針對 Bash 工具'
3. 定義一個或多個 [hook 處理程式](#hook-handler-fields) 以在匹配時執行

有關完整的逐步說明和註解範例，請參閱上面的 [Hook 如何解析](#how-a-hook-resolves)。

<Note>
  此頁面為每個層級使用特定術語：**hook 事件** 表示生命週期點，**匹配器群組** 表示篩選器，**hook 處理程式** 表示執行的 shell 命令、HTTP 端點、提示或代理。'Hook'本身指的是一般功能。
</Note>

### Hook 位置

您定義 hook 的位置決定了其範圍：

| 位置                                                              | 範圍        | 可共享          |
| :-------------------------------------------------------------- | :-------- | :----------- |
| `~/.claude/settings.json`                                       | 您的所有專案    | 否，本機限定       |
| `.claude/settings.json`                                         | 單一專案      | 是，可提交到儲存庫    |
| `.claude/settings.local.json`                                   | 單一專案      | 否，gitignored |
| 受管理的原則設定                                                        | 組織範圍      | 是，由管理員控制     |
| [Plugin](/zh-TW/plugins) `hooks/hooks.json`                     | 啟用外掛程式時   | 是，與外掛程式一起打包  |
| [Skill](/zh-TW/skills) 或 [agent](/zh-TW/sub-agents) frontmatter | 元件處於活動狀態時 | 是，在元件檔案中定義   |

有關設定檔解析的詳細資訊，請參閱 [settings](/zh-TW/settings)。企業管理員可以使用 `allowManagedHooksOnly` 來阻止使用者、專案和外掛程式 hooks。請參閱 [Hook 配置](/zh-TW/settings#hook-configuration)。

### 匹配器模式

`matcher` 欄位是一個正規表達式字串，用於篩選 hooks 何時觸發。使用 `"*"`、`""` 或完全省略 `matcher` 以匹配所有出現次數。每個事件類型在不同的欄位上匹配：

| 事件                                                                                         | 匹配器篩選的內容  | 範例匹配器值                                                                                                              |
| :----------------------------------------------------------------------------------------- | :-------- | :------------------------------------------------------------------------------------------------------------------ |
| `PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`PermissionRequest`                        | 工具名稱      | `Bash`、`Edit\|Write`、`mcp__.*`                                                                                      |
| `SessionStart`                                                                             | 工作階段如何開始  | `startup`、`resume`、`clear`、`compact`                                                                                |
| `SessionEnd`                                                                               | 工作階段為何結束  | `clear`、`resume`、`logout`、`prompt_input_exit`、`bypass_permissions_disabled`、`other`                                 |
| `Notification`                                                                             | 通知類型      | `permission_prompt`、`idle_prompt`、`auth_success`、`elicitation_dialog`                                               |
| `SubagentStart`                                                                            | 代理類型      | `Bash`、`Explore`、`Plan` 或自訂代理名稱                                                                                     |
| `PreCompact`、`PostCompact`                                                                 | 觸發壓縮的原因   | `manual`、`auto`                                                                                                     |
| `SubagentStop`                                                                             | 代理類型      | 與 `SubagentStart` 相同的值                                                                                              |
| `ConfigChange`                                                                             | 配置來源      | `user_settings`、`project_settings`、`local_settings`、`policy_settings`、`skills`                                      |
| `StopFailure`                                                                              | 錯誤類型      | `rate_limit`、`authentication_failed`、`billing_error`、`invalid_request`、`server_error`、`max_output_tokens`、`unknown` |
| `InstructionsLoaded`                                                                       | 載入原因      | `session_start`、`nested_traversal`、`path_glob_match`、`include`、`compact`                                            |
| `Elicitation`                                                                              | MCP 伺服器名稱 | 您配置的 MCP 伺服器名稱                                                                                                      |
| `ElicitationResult`                                                                        | MCP 伺服器名稱 | 與 `Elicitation` 相同的值                                                                                                |
| `UserPromptSubmit`、`Stop`、`TeammateIdle`、`TaskCompleted`、`WorktreeCreate`、`WorktreeRemove` | 不支援匹配器    | 總是在每次出現時觸發                                                                                                          |

匹配器是正規表達式，因此 `Edit|Write` 匹配任一工具，`Notebook.*` 匹配任何以 Notebook 開頭的工具。匹配器針對 Claude Code 在 stdin 上發送給您的 hook 的 [JSON 輸入](#hook-input-and-output) 中的欄位執行。對於工具事件，該欄位是 `tool_name`。每個 [hook 事件](#hook-events) 部分列出了該事件的完整匹配器值集和輸入架構。

此範例僅在 Claude 寫入或編輯檔案時執行 linting 指令碼：

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/lint-check.sh"
          }
        ]
      }
    ]
  }
}
```

`UserPromptSubmit`、`Stop`、`TeammateIdle`、`TaskCompleted`、`WorktreeCreate` 和 `WorktreeRemove` 不支援匹配器，總是在每次出現時觸發。如果您將 `matcher` 欄位新增到這些事件，它會被無聲地忽略。

#### 匹配 MCP 工具

[MCP](/zh-TW/mcp) 伺服器工具在工具事件中顯示為常規工具（`PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`PermissionRequest`），因此您可以像匹配任何其他工具名稱一樣匹配它們。

MCP 工具遵循命名模式 `mcp__<server>__<tool>`，例如：

* `mcp__memory__create_entities`：Memory 伺服器的建立實體工具
* `mcp__filesystem__read_file`：Filesystem 伺服器的讀取檔案工具
* `mcp__github__search_repositories`：GitHub 伺服器的搜尋工具

使用正規表達式模式來針對特定 MCP 工具或工具群組：

* `mcp__memory__.*` 匹配來自 `memory` 伺服器的所有工具
* `mcp__.*__write.*` 匹配來自任何伺服器的任何包含「write」的工具

此範例記錄所有 memory 伺服器操作並驗證來自任何 MCP 伺服器的寫入操作：

```json  theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

### Hook 處理程式欄位

內部 `hooks` 陣列中的每個物件都是一個 hook 處理程式：當匹配器匹配時執行的 shell 命令、HTTP 端點、LLM 提示或代理。有四種類型：

* **[命令 hooks](#command-hook-fields)**（`type: "command"`）：執行 shell 命令。您的指令碼在 stdin 上接收事件的 [JSON 輸入](#hook-input-and-output)，並通過退出代碼和 stdout 傳回結果。
* **[HTTP hooks](#http-hook-fields)**（`type: "http"`）：將事件的 JSON 輸入作為 HTTP POST 請求發送到 URL。端點通過使用與命令 hooks 相同的 [JSON 輸出格式](#json-output) 的回應正文傳回結果。
* **[提示 hooks](#prompt-and-agent-hook-fields)**（`type: "prompt"`）：將提示發送到 Claude 模型進行單輪評估。模型以 JSON 形式返回是/否決定。請參閱 [基於提示的 hooks](#prompt-based-hooks)。
* **[代理 hooks](#prompt-and-agent-hook-fields)**（`type: "agent"`）：生成一個可以使用 Read、Grep 和 Glob 等工具來驗證條件的 subagent，然後返回決定。請參閱 [基於代理的 hooks](#agent-based-hooks)。

#### 通用欄位

這些欄位適用於所有 hook 類型：

| 欄位              | 必需 | 描述                                                                                                  |
| :-------------- | :- | :-------------------------------------------------------------------------------------------------- |
| `type`          | 是  | `"command"`、`"http"`、`"prompt"` 或 `"agent"`                                                         |
| `timeout`       | 否  | 取消前的秒數。預設值：命令 600、提示 30、代理 60                                                                       |
| `statusMessage` | 否  | hook 執行時顯示的自訂微調訊息                                                                                   |
| `once`          | 否  | 如果為 `true`，每個工作階段只執行一次，然後被移除。僅限 Skills，不適用於代理。請參閱 [Skills 和代理中的 Hooks](#hooks-in-skills-and-agents) |

#### 命令 hook 欄位

除了 [通用欄位](#common-fields) 外，命令 hooks 還接受這些欄位：

| 欄位        | 必需 | 描述                                                                   |
| :-------- | :- | :------------------------------------------------------------------- |
| `command` | 是  | 要執行的 shell 命令                                                        |
| `async`   | 否  | 如果為 `true`，在背景執行而不阻止。請參閱 [在背景執行 hooks](#run-hooks-in-the-background) |

#### HTTP hook 欄位

除了 [通用欄位](#common-fields) 外，HTTP hooks 還接受這些欄位：

| 欄位               | 必需 | 描述                                                                                          |
| :--------------- | :- | :------------------------------------------------------------------------------------------ |
| `url`            | 是  | 要發送 POST 請求的 URL                                                                            |
| `headers`        | 否  | 其他 HTTP 標頭作為鍵值對。值支援使用 `$VAR_NAME` 或 `${VAR_NAME}` 語法的環境變數插值。只有列在 `allowedEnvVars` 中的變數才會被解析 |
| `allowedEnvVars` | 否  | 可能被插值到標頭值中的環境變數名稱清單。對未列出的變數的參考會被替換為空字串。任何環境變數插值都需要此項                                        |

Claude Code 將 hook 的 [JSON 輸入](#hook-input-and-output) 作為 POST 請求正文發送，`Content-Type: application/json`。回應正文使用與命令 hooks 相同的 [JSON 輸出格式](#json-output)。

錯誤處理與命令 hooks 不同：非 2xx 回應、連線失敗和逾時都會產生非阻止性錯誤，允許執行繼續。要阻止工具呼叫或拒絕權限，請返回 2xx 回應，其 JSON 正文包含 `decision: "block"` 或 `hookSpecificOutput` 與 `permissionDecision: "deny"`。

此範例將 `PreToolUse` 事件發送到本機驗證服務，使用來自 `MY_TOKEN` 環境變數的令牌進行驗證：

```json  theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/pre-tool-use",
            "timeout": 30,
            "headers": {
              "Authorization": "Bearer $MY_TOKEN"
            },
            "allowedEnvVars": ["MY_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

#### 提示和代理 hook 欄位

除了 [通用欄位](#common-fields) 外，提示和代理 hooks 還接受這些欄位：

| 欄位       | 必需 | 描述                                               |
| :------- | :- | :----------------------------------------------- |
| `prompt` | 是  | 要發送到模型的提示文字。使用 `$ARGUMENTS` 作為 hook 輸入 JSON 的佔位符 |
| `model`  | 否  | 用於評估的模型。預設為快速模型                                  |

所有匹配的 hooks 並行執行，相同的處理程式會自動去重。命令 hooks 按命令字串去重，HTTP hooks 按 URL 去重。處理程式在目前目錄中執行，使用 Claude Code 的環境。在遠端網路環境中，`$CLAUDE_CODE_REMOTE` 環境變數設定為 `"true"`，在本機 CLI 中未設定。

### 按路徑參考指令碼

使用環境變數按相對於專案或外掛程式根目錄的路徑參考 hook 指令碼，無論 hook 執行時的工作目錄如何：

* `$CLAUDE_PROJECT_DIR`：專案根目錄。用引號括起來以處理包含空格的路徑。
* `${CLAUDE_PLUGIN_ROOT}`：外掛程式的根目錄，用於與 [plugin](/zh-TW/plugins) 一起打包的指令碼。在每次外掛程式更新時變更。
* `${CLAUDE_PLUGIN_DATA}`：外掛程式的 [持久資料目錄](/zh-TW/plugins-reference#persistent-data-directory)，用於應該在外掛程式更新後保留的依賴項和狀態。

<Tabs>
  <Tab title="專案指令碼">
    此範例使用 `$CLAUDE_PROJECT_DIR` 在任何 `Write` 或 `Edit` 工具呼叫後從專案的 `.claude/hooks/` 目錄執行樣式檢查器：

    ```json  theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-style.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="外掛程式指令碼">
    在 `hooks/hooks.json` 中定義外掛程式 hooks，使用可選的頂層 `description` 欄位。啟用外掛程式時，其 hooks 會與您的使用者和專案 hooks 合併。

    此範例執行與外掛程式一起打包的格式化指令碼：

    ```json  theme={null}
    {
      "description": "Automatic code formatting",
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
                "timeout": 30
              }
            ]
          }
        ]
      }
    }
    ```

    有關建立外掛程式 hooks 的詳細資訊，請參閱 [外掛程式元件參考](/zh-TW/plugins-reference#hooks)。
  </Tab>
</Tabs>

### Skills 和代理中的 Hooks

除了設定檔和外掛程式外，hooks 還可以使用 frontmatter 直接在 [skills](/zh-TW/skills) 和 [subagents](/zh-TW/sub-agents) 中定義。這些 hooks 的範圍限於元件的生命週期，只有在該元件處於活動狀態時才執行。

支援所有 hook 事件。對於 subagents，`Stop` hooks 會自動轉換為 `SubagentStop`，因為這是 subagent 完成時觸發的事件。

Hooks 使用與基於設定的 hooks 相同的配置格式，但範圍限於元件的生命週期，並在完成時清理。

此 skill 定義了一個 `PreToolUse` hook，在每個 `Bash` 命令之前執行安全驗證指令碼：

```yaml  theme={null}
---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---
```

代理在其 YAML frontmatter 中使用相同的格式。

### `/hooks` 選單

在 Claude Code 中輸入 `/hooks` 以開啟唯讀瀏覽器來查看您配置的 hooks。選單顯示每個 hook 事件及其配置的 hooks 計數，讓您深入查看匹配器，並顯示每個 hook 處理程式的完整詳細資訊。使用它來驗證配置、檢查 hook 來自哪個設定檔，或檢查 hook 的命令、提示或 URL。

選單顯示所有四種 hook 類型：`command`、`prompt`、`agent` 和 `http`。每個 hook 都標有 `[type]` 前綴和指示其定義位置的來源：

* `User`：來自 `~/.claude/settings.json`
* `Project`：來自 `.claude/settings.json`
* `Local`：來自 `.claude/settings.local.json`
* `Plugin`：來自外掛程式的 `hooks/hooks.json`
* `Session`：在目前工作階段中記錄在記憶體中
* `Built-in`：由 Claude Code 內部註冊

選擇 hook 會開啟詳細檢視，顯示其事件、匹配器、類型、來源檔案和完整命令、提示或 URL。選單是唯讀的：要新增、修改或移除 hooks，請直接編輯設定 JSON 或要求 Claude 進行變更。

### 停用或移除 hooks

要移除 hook，請從設定 JSON 檔案中刪除其項目。

要暫時停用所有 hooks 而不移除它們，請在設定檔中設定 `"disableAllHooks": true`。沒有辦法在保留 hook 在配置中的同時停用單個 hook。

`disableAllHooks` 設定遵循受管理的設定階層。如果管理員已通過受管理的原則設定配置了 hooks，則在使用者、專案或本機設定中設定的 `disableAllHooks` 無法停用這些受管理的 hooks。只有在受管理的設定層級設定的 `disableAllHooks` 才能停用受管理的 hooks。

對設定檔中 hooks 的直接編輯通常由檔案監視程式自動拾取。

## Hook 輸入和輸出

命令 hooks 通過 stdin 接收 JSON 資料，並通過退出代碼、stdout 和 stderr 傳回結果。HTTP hooks 接收相同的 JSON 作為 POST 請求正文，並通過 HTTP 回應正文傳回結果。本部分涵蓋所有事件通用的欄位和行為。每個事件在 [Hook 事件](#hook-events) 下的部分包括其特定的輸入架構和決定控制選項。

### 通用輸入欄位

除了每個 [hook 事件](#hook-events) 部分中記錄的事件特定欄位外，所有 hook 事件都接收這些欄位作為 JSON。對於命令 hooks，此 JSON 通過 stdin 到達。對於 HTTP hooks，它作為 POST 請求正文到達。

| 欄位                | 描述                                                                                                                                                                  |
| :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `session_id`      | 目前工作階段識別碼                                                                                                                                                           |
| `transcript_path` | 對話 JSON 的路徑                                                                                                                                                         |
| `cwd`             | 叫用 hook 時的目前工作目錄                                                                                                                                                    |
| `permission_mode` | 目前 [權限模式](/zh-TW/permissions#permission-modes)：`"default"`、`"plan"`、`"acceptEdits"`、`"auto"`、`"dontAsk"` 或 `"bypassPermissions"`。並非所有事件都接收此欄位：請參閱下面每個事件的 JSON 範例以檢查 |
| `hook_event_name` | 觸發的事件名稱                                                                                                                                                             |

使用 `--agent` 執行或在 subagent 內執行時，包括兩個額外欄位：

| 欄位           | 描述                                                                                                                                     |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------- |
| `agent_id`   | Subagent 的唯一識別碼。僅當 hook 在 subagent 呼叫內觸發時出現。使用此項來區分 subagent hook 呼叫與主執行緒呼叫。                                                           |
| `agent_type` | 代理名稱（例如 `"Explore"` 或 `"security-reviewer"`）。當工作階段使用 `--agent` 或 hook 在 subagent 內觸發時出現。對於 subagents，subagent 的類型優先於工作階段的 `--agent` 值。 |

例如，Bash 命令的 `PreToolUse` hook 在 stdin 上接收此內容：

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl",
  "cwd": "/home/user/my-project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}
```

`tool_name` 和 `tool_input` 欄位是事件特定的。每個 [hook 事件](#hook-events) 部分記錄了該事件的額外欄位。

### 退出代碼輸出

來自您的 hook 命令的退出代碼告訴 Claude Code 該操作是應該進行、被阻止還是被忽略。

**退出 0** 表示成功。Claude Code 解析 stdout 以查找 [JSON 輸出欄位](#json-output)。JSON 輸出僅在退出 0 時處理。對於大多數事件，stdout 僅在詳細模式（`Ctrl+O`）中顯示。例外是 `UserPromptSubmit` 和 `SessionStart`，其中 stdout 被新增為 Claude 可以看到和作用的上下文。

**退出 2** 表示阻止性錯誤。Claude Code 忽略 stdout 和其中的任何 JSON。相反，stderr 文字被反饋給 Claude 作為錯誤訊息。效果取決於事件：`PreToolUse` 阻止工具呼叫，`UserPromptSubmit` 拒絕提示，等等。有關完整清單，請參閱 [退出代碼 2 行為](#exit-code-2-behavior-per-event)。

**任何其他退出代碼** 是非阻止性錯誤。stderr 在詳細模式（`Ctrl+O`）中顯示，執行繼續。

例如，一個 hook 命令指令碼，阻止危險的 Bash 命令：

```bash  theme={null}
#!/bin/bash
# 從 stdin 讀取 JSON 輸入，檢查命令
command=$(jq -r '.tool_input.command' < /dev/stdin)

if [[ "$command" == rm* ]]; then
  echo "Blocked: rm commands are not allowed" >&2
  exit 2  # 阻止性錯誤：工具呼叫被阻止
fi

exit 0  # 成功：工具呼叫進行
```

#### 每個事件的退出代碼 2 行為

退出代碼 2 是 hook 發出「停止，不要這樣做」的方式。效果取決於事件，因為某些事件代表可以被阻止的操作（例如尚未發生的工具呼叫），而其他事件代表已經發生或無法防止的事情。

| Hook 事件              | 可以阻止？ | 退出 2 時發生的情況                    |
| :------------------- | :---- | :----------------------------- |
| `PreToolUse`         | 是     | 阻止工具呼叫                         |
| `PermissionRequest`  | 是     | 拒絕權限                           |
| `UserPromptSubmit`   | 是     | 阻止提示處理並清除提示                    |
| `Stop`               | 是     | 防止 Claude 停止，繼續對話              |
| `SubagentStop`       | 是     | 防止 subagent 停止                 |
| `TeammateIdle`       | 是     | 防止隊友閒置（隊友繼續工作）                 |
| `TaskCompleted`      | 是     | 防止任務被標記為已完成                    |
| `ConfigChange`       | 是     | 阻止配置變更生效（除了 `policy_settings`） |
| `StopFailure`        | 否     | 輸出和退出代碼被忽略                     |
| `PostToolUse`        | 否     | 向 Claude 顯示 stderr（工具已執行）      |
| `PostToolUseFailure` | 否     | 向 Claude 顯示 stderr（工具已失敗）      |
| `Notification`       | 否     | 僅向使用者顯示 stderr                 |
| `SubagentStart`      | 否     | 僅向使用者顯示 stderr                 |
| `SessionStart`       | 否     | 僅向使用者顯示 stderr                 |
| `SessionEnd`         | 否     | 僅向使用者顯示 stderr                 |
| `PreCompact`         | 否     | 僅向使用者顯示 stderr                 |
| `PostCompact`        | 否     | 僅向使用者顯示 stderr                 |
| `Elicitation`        | 是     | 拒絕徵詢                           |
| `ElicitationResult`  | 是     | 阻止回應（操作變為拒絕）                   |
| `WorktreeCreate`     | 是     | 任何非零退出代碼都會導致 worktree 建立失敗     |
| `WorktreeRemove`     | 否     | 失敗僅在偵錯模式中記錄                    |
| `InstructionsLoaded` | 否     | 退出代碼被忽略                        |

### HTTP 回應處理

HTTP hooks 使用 HTTP 狀態代碼和回應正文，而不是退出代碼和 stdout：

* **2xx 且正文為空**：成功，等同於退出代碼 0 且無輸出
* **2xx 且正文為純文字**：成功，文字被新增為上下文
* **2xx 且正文為 JSON**：成功，使用與命令 hooks 相同的 [JSON 輸出](#json-output) 架構進行解析
* **非 2xx 狀態**：非阻止性錯誤，執行繼續
* **連線失敗或逾時**：非阻止性錯誤，執行繼續

與命令 hooks 不同，HTTP hooks 無法僅通過狀態代碼發出阻止性錯誤信號。要阻止工具呼叫或拒絕權限，請返回 2xx 回應，其 JSON 正文包含適當的決定欄位。

### JSON 輸出

退出代碼讓您允許或阻止，但 JSON 輸出提供更細粒度的控制。與其以代碼 2 退出來阻止，不如以 0 退出並將 JSON 物件列印到 stdout。Claude Code 從該 JSON 讀取特定欄位以控制行為，包括 [決定控制](#decision-control) 以阻止、允許或升級給使用者。

<Note>
  您必須為每個 hook 選擇一種方法，而不是兩種：要麼單獨使用退出代碼進行信號傳遞，要麼以 0 退出並列印 JSON 以進行結構化控制。Claude Code 僅在退出 0 時處理 JSON。如果您退出 2，任何 JSON 都會被忽略。
</Note>

您的 hook 的 stdout 必須僅包含 JSON 物件。如果您的 shell 設定檔在啟動時列印文字，它可能會干擾 JSON 解析。請參閱故障排除指南中的 [JSON 驗證失敗](/zh-TW/hooks-guide#json-validation-failed)。

JSON 物件支援三種欄位：

* **通用欄位**，如 `continue`，在所有事件中工作。這些列在下表中。
* **頂層 `decision` 和 `reason`** 由某些事件用來阻止或提供反饋。
* **`hookSpecificOutput`** 是一個嵌套物件，用於需要更豐富控制的事件。它需要一個設定為事件名稱的 `hookEventName` 欄位。

| 欄位               | 預設      | 描述                                                     |
| :--------------- | :------ | :----------------------------------------------------- |
| `continue`       | `true`  | 如果為 `false`，Claude 在 hook 執行後完全停止處理。優先於任何事件特定的決定欄位     |
| `stopReason`     | 無       | hook 執行後當 `continue` 為 `false` 時向使用者顯示的訊息。不向 Claude 顯示 |
| `suppressOutput` | `false` | 如果為 `true`，隱藏詳細模式輸出中的 stdout                           |
| `systemMessage`  | 無       | 向使用者顯示的警告訊息                                            |

要無論事件類型如何都完全停止 Claude：

```json  theme={null}
{ "continue": false, "stopReason": "Build failed, fix errors before continuing" }
```

#### 決定控制

並非每個事件都支援阻止或通過 JSON 控制行為。支援的事件各自使用不同的欄位集來表達該決定。在編寫 hook 之前，使用此表作為快速參考：

| 事件                                                                                           | 決定模式                    | 關鍵欄位                                                                                               |
| :------------------------------------------------------------------------------------------- | :---------------------- | :------------------------------------------------------------------------------------------------- |
| UserPromptSubmit、PostToolUse、PostToolUseFailure、Stop、SubagentStop、ConfigChange               | 頂層 `decision`           | `decision: "block"`、`reason`                                                                       |
| TeammateIdle、TaskCompleted                                                                   | 退出代碼或 `continue: false` | 退出代碼 2 使用 stderr 反饋阻止操作。JSON `{"continue": false, "stopReason": "..."}` 也會完全停止隊友，匹配 `Stop` hook 行為 |
| PreToolUse                                                                                   | `hookSpecificOutput`    | `permissionDecision`（allow/deny/ask）、`permissionDecisionReason`                                    |
| PermissionRequest                                                                            | `hookSpecificOutput`    | `decision.behavior`（allow/deny）                                                                    |
| WorktreeCreate                                                                               | stdout 路徑               | Hook 列印建立的 worktree 的絕對路徑。非零退出失敗建立                                                                 |
| Elicitation                                                                                  | `hookSpecificOutput`    | `action`（accept/decline/cancel）、`content`（accept 的表單欄位值）                                           |
| ElicitationResult                                                                            | `hookSpecificOutput`    | `action`（accept/decline/cancel）、`content`（覆蓋表單欄位值）                                                 |
| WorktreeRemove、Notification、SessionEnd、PreCompact、PostCompact、InstructionsLoaded、StopFailure | 無                       | 無決定控制。用於副作用，如記錄或清理                                                                                 |

以下是每種模式的實際範例：

<Tabs>
  <Tab title="頂層決定">
    由 `UserPromptSubmit`、`PostToolUse`、`PostToolUseFailure`、`Stop`、`SubagentStop` 和 `ConfigChange` 使用。唯一的值是 `"block"`。要允許操作進行，請從 JSON 中省略 `decision`，或以 0 退出而不帶任何 JSON：

    ```json  theme={null}
    {
      "decision": "block",
      "reason": "Test suite must pass before proceeding"
    }
    ```
  </Tab>

  <Tab title="PreToolUse">
    使用 `hookSpecificOutput` 進行更豐富的控制：允許、拒絕或升級給使用者。您還可以在執行前修改工具輸入或為 Claude 注入額外上下文。有關完整的選項集，請參閱 [PreToolUse 決定控制](#pretooluse-decision-control)。

    ```json  theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Database writes are not allowed"
      }
    }
    ```
  </Tab>

  <Tab title="PermissionRequest">
    使用 `hookSpecificOutput` 代表使用者允許或拒絕權限請求。允許時，您還可以修改工具的輸入或應用權限規則，以便使用者不會再次被提示。有關完整的選項集，請參閱 [PermissionRequest 決定控制](#permissionrequest-decision-control)。

    ```json  theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PermissionRequest",
        "decision": {
          "behavior": "allow",
          "updatedInput": {
            "command": "npm run lint"
          }
        }
      }
    }
    ```
  </Tab>
</Tabs>

有關擴展範例，包括 Bash 命令驗證、提示篩選和自動批准指令碼，請參閱指南中的 [您可以自動化的內容](/zh-TW/hooks-guide#what-you-can-automate) 和 [Bash 命令驗證器參考實現](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py)。

## Hook 事件

每個事件對應於 Claude Code 生命週期中 hooks 可以執行的一個點。下面的部分按順序排列以匹配生命週期：從工作階段設定通過代理迴圈到工作階段結束。每個部分描述事件何時觸發、它支援什麼匹配器、它接收的 JSON 輸入，以及如何通過輸出控制行為。

### SessionStart

在 Claude Code 啟動新工作階段或恢復現有工作階段時執行。適用於載入開發上下文，例如現有問題或程式碼庫的最近變更，或設定環境變數。對於不需要指令碼的靜態上下文，請改用 [CLAUDE.md](/zh-TW/memory)。

SessionStart 在每個工作階段執行，因此請保持這些 hooks 快速。僅支援 `type: "command"` hooks。

匹配器值對應於工作階段的啟動方式：

| 匹配器       | 何時觸發                                |
| :-------- | :---------------------------------- |
| `startup` | 新工作階段                               |
| `resume`  | `--resume`、`--continue` 或 `/resume` |
| `clear`   | `/clear`                            |
| `compact` | 自動或手動壓縮                             |

#### SessionStart 輸入

除了 [通用輸入欄位](#common-input-fields) 外，SessionStart hooks 還接收 `source`、`model` 和可選的 `agent_type`。`source` 欄位指示工作階段如何啟動：新工作階段為 `"startup"`，恢復的工作階段為 `"resume"`，`/clear` 後為 `"clear"`，或壓縮後為 `"compact"`。`model` 欄位包含模型識別碼。如果您使用 `claude --agent <name>` 啟動 Claude Code，`agent_type` 欄位包含代理名稱。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionStart",
  "source": "startup",
  "model": "claude-sonnet-4-6"
}
```

#### SessionStart 決定控制

您的 hook 指令碼列印到 stdout 的任何文字都被新增為 Claude 的上下文。除了所有 hooks 可用的 [JSON 輸出欄位](#json-output) 外，您還可以返回這些事件特定欄位：

| 欄位                  | 描述                               |
| :------------------ | :------------------------------- |
| `additionalContext` | 新增到 Claude 上下文的字串。多個 hooks 的值被連接 |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "My additional context here"
  }
}
```

#### 持久化環境變數

SessionStart hooks 可以存取 `CLAUDE_ENV_FILE` 環境變數，該變數提供一個檔案路徑，您可以在其中為後續 Bash 命令持久化環境變數。

要設定個別環境變數，請將 `export` 陳述式寫入 `CLAUDE_ENV_FILE`。使用追加（`>>`）來保留由其他 hooks 設定的變數：

```bash  theme={null}
#!/bin/bash

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG_LOG=true' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

要捕獲設定命令中的所有環境變更，請比較之前和之後的匯出變數：

```bash  theme={null}
#!/bin/bash

ENV_BEFORE=$(export -p | sort)

# 執行修改環境的設定命令
source ~/.nvm/nvm.sh
nvm use 20

if [ -n "$CLAUDE_ENV_FILE" ]; then
  ENV_AFTER=$(export -p | sort)
  comm -13 <(echo "$ENV_BEFORE") <(echo "$ENV_AFTER") >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

寫入此檔案的任何變數都將在工作階段期間 Claude Code 執行的所有後續 Bash 命令中可用。

<Note>
  `CLAUDE_ENV_FILE` 可用於 SessionStart hooks。其他 hook 類型無法存取此變數。
</Note>

### InstructionsLoaded

當 `CLAUDE.md` 或 `.claude/rules/*.md` 檔案被載入到上下文中時觸發。此事件在工作階段開始時針對急切載入的檔案觸發，稍後當檔案被延遲載入時再次觸發，例如當 Claude 存取包含嵌套 `CLAUDE.md` 的子目錄時，或當具有 `paths:` frontmatter 的條件規則匹配時。該 hook 不支援阻止或決定控制。它以非同步方式執行以用於可觀測性目的。

匹配器針對 `load_reason` 執行。例如，使用 `"matcher": "session_start"` 僅針對在工作階段開始時載入的檔案觸發，或使用 `"matcher": "path_glob_match|nested_traversal"` 僅針對延遲載入觸發。

#### InstructionsLoaded 輸入

除了 [通用輸入欄位](#common-input-fields) 外，InstructionsLoaded hooks 還接收這些欄位：

| 欄位                  | 描述                                                                                                                           |
| :------------------ | :--------------------------------------------------------------------------------------------------------------------------- |
| `file_path`         | 被載入的指令檔案的絕對路徑                                                                                                                |
| `memory_type`       | 檔案的範圍：`"User"`、`"Project"`、`"Local"` 或 `"Managed"`                                                                           |
| `load_reason`       | 檔案被載入的原因：`"session_start"`、`"nested_traversal"`、`"path_glob_match"`、`"include"` 或 `"compact"`。`"compact"` 值在壓縮事件後重新載入指令檔案時觸發 |
| `globs`             | 檔案 `paths:` frontmatter 中的路徑 glob 模式（如果有）。僅針對 `path_glob_match` 載入出現                                                         |
| `trigger_file_path` | 觸發此載入的檔案的路徑，用於延遲載入                                                                                                           |
| `parent_file_path`  | 包含此檔案的父指令檔案的路徑，用於 `include` 載入                                                                                               |

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "InstructionsLoaded",
  "file_path": "/Users/my-project/CLAUDE.md",
  "memory_type": "Project",
  "load_reason": "session_start"
}
```

#### InstructionsLoaded 決定控制

InstructionsLoaded hooks 沒有決定控制。它們無法阻止或修改指令載入。使用此事件進行稽核記錄、合規性追蹤或可觀測性。

### UserPromptSubmit

在使用者提交提示時執行，在 Claude 處理之前。這允許您根據提示/對話新增額外上下文、驗證提示或阻止某些類型的提示。

#### UserPromptSubmit 輸入

除了 [通用輸入欄位](#common-input-fields) 外，UserPromptSubmit hooks 還接收包含使用者提交的文字的 `prompt` 欄位。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial of a number"
}
```

#### UserPromptSubmit 決定控制

`UserPromptSubmit` hooks 可以控制使用者提示是否被處理並新增上下文。所有 [JSON 輸出欄位](#json-output) 都可用。

有兩種方式在退出代碼 0 時向對話新增上下文：

* **純文字 stdout**：寫入 stdout 的任何非 JSON 文字都被新增為上下文
* **帶有 `additionalContext` 的 JSON**：使用下面的 JSON 格式以獲得更多控制。`additionalContext` 欄位被新增為上下文

純 stdout 在成績單中顯示為 hook 輸出。`additionalContext` 欄位被更謹慎地新增。

要阻止提示，請返回一個 JSON 物件，其中 `decision` 設定為 `"block"`：

| 欄位                  | 描述                                       |
| :------------------ | :--------------------------------------- |
| `decision`          | `"block"` 防止提示被處理並從上下文中清除它。省略以允許提示進行     |
| `reason`            | 當 `decision` 為 `"block"` 時向使用者顯示。不新增到上下文 |
| `additionalContext` | 新增到 Claude 上下文的字串                        |

```json  theme={null}
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here"
  }
}
```

<Note>
  JSON 格式對於簡單用例不是必需的。要新增上下文，您可以使用退出代碼 0 將純文字列印到 stdout。當您需要阻止提示或想要更結構化的控制時，請使用 JSON。
</Note>

### PreToolUse

在 Claude 建立工具參數後和處理工具呼叫之前執行。匹配工具名稱：`Bash`、`Edit`、`Write`、`Read`、`Glob`、`Grep`、`Agent`、`WebFetch`、`WebSearch` 和任何 [MCP 工具名稱](#match-mcp-tools)。

使用 [PreToolUse 決定控制](#pretooluse-decision-control) 來允許、拒絕或要求使用工具的權限。

#### PreToolUse 輸入

除了 [通用輸入欄位](#common-input-fields) 外，PreToolUse hooks 還接收 `tool_name`、`tool_input` 和 `tool_use_id`。`tool_input` 欄位取決於工具：

##### Bash

執行 shell 命令。

| 欄位                  | 類型  | 範例                 | 描述            |
| :------------------ | :-- | :----------------- | :------------ |
| `command`           | 字串  | `"npm test"`       | 要執行的 shell 命令 |
| `description`       | 字串  | `"Run test suite"` | 命令執行內容的可選描述   |
| `timeout`           | 數字  | `120000`           | 可選逾時（毫秒）      |
| `run_in_background` | 布林值 | `false`            | 是否在背景執行命令     |

##### Write

建立或覆寫檔案。

| 欄位          | 類型 | 範例                    | 描述          |
| :---------- | :- | :-------------------- | :---------- |
| `file_path` | 字串 | `"/path/to/file.txt"` | 要寫入的檔案的絕對路徑 |
| `content`   | 字串 | `"file content"`      | 要寫入檔案的內容    |

##### Edit

替換現有檔案中的字串。

| 欄位            | 類型  | 範例                    | 描述          |
| :------------ | :-- | :-------------------- | :---------- |
| `file_path`   | 字串  | `"/path/to/file.txt"` | 要編輯的檔案的絕對路徑 |
| `old_string`  | 字串  | `"original text"`     | 要查詢和替換的文字   |
| `new_string`  | 字串  | `"replacement text"`  | 替換文字        |
| `replace_all` | 布林值 | `false`               | 是否替換所有出現次數  |

##### Read

讀取檔案內容。

| 欄位          | 類型 | 範例                    | 描述          |
| :---------- | :- | :-------------------- | :---------- |
| `file_path` | 字串 | `"/path/to/file.txt"` | 要讀取的檔案的絕對路徑 |
| `offset`    | 數字 | `10`                  | 可選的開始讀取的行號  |
| `limit`     | 數字 | `50`                  | 可選的要讀取的行數   |

##### Glob

尋找與 glob 模式匹配的檔案。

| 欄位        | 類型 | 範例               | 描述                |
| :-------- | :- | :--------------- | :---------------- |
| `pattern` | 字串 | `"**/*.ts"`      | 要匹配檔案的 glob 模式    |
| `path`    | 字串 | `"/path/to/dir"` | 可選的搜尋目錄。預設為目前工作目錄 |

##### Grep

使用正規表達式搜尋檔案內容。

| 欄位            | 類型  | 範例               | 描述                                                                        |
| :------------ | :-- | :--------------- | :------------------------------------------------------------------------ |
| `pattern`     | 字串  | `"TODO.*fix"`    | 要搜尋的正規表達式模式                                                               |
| `path`        | 字串  | `"/path/to/dir"` | 可選的要搜尋的檔案或目錄                                                              |
| `glob`        | 字串  | `"*.ts"`         | 可選的 glob 模式以篩選檔案                                                          |
| `output_mode` | 字串  | `"content"`      | `"content"`、`"files_with_matches"` 或 `"count"`。預設為 `"files_with_matches"` |
| `-i`          | 布林值 | `true`           | 不區分大小寫的搜尋                                                                 |
| `multiline`   | 布林值 | `false`          | 啟用多行匹配                                                                    |

##### WebFetch

擷取和處理網路內容。

| 欄位       | 類型 | 範例                            | 描述           |
| :------- | :- | :---------------------------- | :----------- |
| `url`    | 字串 | `"https://example.com/api"`   | 要擷取內容的 URL   |
| `prompt` | 字串 | `"Extract the API endpoints"` | 在擷取的內容上執行的提示 |

##### WebSearch

搜尋網路。

| 欄位                | 類型 | 範例                             | 描述              |
| :---------------- | :- | :----------------------------- | :-------------- |
| `query`           | 字串 | `"react hooks best practices"` | 搜尋查詢            |
| `allowed_domains` | 陣列 | `["docs.example.com"]`         | 可選：僅包含來自這些網域的結果 |
| `blocked_domains` | 陣列 | `["spam.example.com"]`         | 可選：排除來自這些網域的結果  |

##### Agent

生成一個 [subagent](/zh-TW/sub-agents)。

| 欄位              | 類型 | 範例                         | 描述            |
| :-------------- | :- | :------------------------- | :------------ |
| `prompt`        | 字串 | `"Find all API endpoints"` | 代理要執行的任務      |
| `description`   | 字串 | `"Find API endpoints"`     | 任務的簡短描述       |
| `subagent_type` | 字串 | `"Explore"`                | 要使用的專門代理類型    |
| `model`         | 字串 | `"sonnet"`                 | 可選的模型別名以覆蓋預設值 |

#### PreToolUse 決定控制

`PreToolUse` hooks 可以控制工具呼叫是否進行。與使用頂層 `decision` 欄位的其他 hooks 不同，PreToolUse 在 `hookSpecificOutput` 物件內返回其決定。這提供了更豐富的控制：三個結果（允許、拒絕或詢問）加上在執行前修改工具輸入的能力。

| 欄位                         | 描述                                                                                                                          |
| :------------------------- | :-------------------------------------------------------------------------------------------------------------------------- |
| `permissionDecision`       | `"allow"` 跳過權限提示。`"deny"` 防止工具呼叫。`"ask"` 提示使用者確認。[拒絕和詢問規則](/zh-TW/permissions#manage-permissions) 在 hook 返回 `"allow"` 時仍然適用 |
| `permissionDecisionReason` | 對於 `"allow"` 和 `"ask"`，向使用者顯示但不向 Claude 顯示。對於 `"deny"`，向 Claude 顯示                                                          |
| `updatedInput`             | 在執行前修改工具的輸入參數。與 `"allow"` 結合以自動批准，或與 `"ask"` 結合以向使用者顯示修改後的輸入                                                                |
| `additionalContext`        | 在工具執行前新增到 Claude 上下文的字串                                                                                                     |

當 hook 返回 `"ask"` 時，向使用者顯示的權限提示包括一個標籤，識別 hook 來自何處：例如 `[User]`、`[Project]`、`[Plugin]` 或 `[Local]`。這幫助使用者了解哪個配置來源正在請求確認。

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "My reason here",
    "updatedInput": {
      "field_to_modify": "new value"
    },
    "additionalContext": "Current environment: production. Proceed with caution."
  }
}
```

<Note>
  PreToolUse 之前使用頂層 `decision` 和 `reason` 欄位，但這些對此事件已棄用。改用 `hookSpecificOutput.permissionDecision` 和 `hookSpecificOutput.permissionDecisionReason`。棄用的值 `"approve"` 和 `"block"` 對應於 `"allow"` 和 `"deny"`。PostToolUse 和 Stop 等其他事件繼續使用頂層 `decision` 和 `reason` 作為其目前格式。
</Note>

### PermissionRequest

在向使用者顯示權限對話框時執行。使用 [PermissionRequest 決定控制](#permissionrequest-decision-control) 代表使用者允許或拒絕。

匹配工具名稱，與 PreToolUse 相同的值。

#### PermissionRequest 輸入

PermissionRequest hooks 接收 `tool_name` 和 `tool_input` 欄位，如 PreToolUse hooks，但沒有 `tool_use_id`。可選的 `permission_suggestions` 陣列包含使用者通常在權限對話框中看到的「總是允許」選項。區別在於 hook 何時觸發：PermissionRequest hooks 在權限對話框即將向使用者顯示時執行，而 PreToolUse hooks 在工具執行前執行，無論權限狀態如何。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PermissionRequest",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf node_modules",
    "description": "Remove node_modules directory"
  },
  "permission_suggestions": [
    {
      "type": "addRules",
      "rules": [{ "toolName": "Bash", "ruleContent": "rm -rf node_modules" }],
      "behavior": "allow",
      "destination": "localSettings"
    }
  ]
}
```

#### PermissionRequest 決定控制

`PermissionRequest` hooks 可以允許或拒絕權限請求。除了所有 hooks 可用的 [JSON 輸出欄位](#json-output) 外，您的 hook 指令碼可以返回一個 `decision` 物件，其中包含這些事件特定欄位：

| 欄位                   | 描述                                                                             |
| :------------------- | :----------------------------------------------------------------------------- |
| `behavior`           | `"allow"` 授予權限，`"deny"` 拒絕它                                                    |
| `updatedInput`       | 僅適用於 `"allow"`：在執行前修改工具的輸入參數                                                   |
| `updatedPermissions` | 僅適用於 `"allow"`：應用的 [權限更新項目](#permission-update-entries) 陣列，例如新增允許規則或變更工作階段權限模式 |
| `message`            | 僅適用於 `"deny"`：告訴 Claude 為什麼權限被拒絕                                               |
| `interrupt`          | 僅適用於 `"deny"`：如果為 `true`，停止 Claude                                             |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": {
        "command": "npm run lint"
      }
    }
  }
}
```

#### 權限更新項目

`updatedPermissions` 輸出欄位和 [`permission_suggestions` 輸入欄位](#permissionrequest-input) 都使用相同的項目物件陣列。每個項目都有一個 `type` 決定其他欄位，以及一個 `destination` 控制變更寫入位置。

| `type`              | 欄位                               | 效果                                                                                                                   |
| :------------------ | :------------------------------- | :------------------------------------------------------------------------------------------------------------------- |
| `addRules`          | `rules`、`behavior`、`destination` | 新增權限規則。`rules` 是 `{toolName, ruleContent?}` 物件的陣列。省略 `ruleContent` 以匹配整個工具。`behavior` 是 `"allow"`、`"deny"` 或 `"ask"` |
| `replaceRules`      | `rules`、`behavior`、`destination` | 用提供的 `rules` 替換 `destination` 處給定 `behavior` 的所有規則                                                                   |
| `removeRules`       | `rules`、`behavior`、`destination` | 移除匹配的給定 `behavior` 的規則                                                                                               |
| `setMode`           | `mode`、`destination`             | 變更權限模式。有效模式為 `default`、`acceptEdits`、`dontAsk`、`bypassPermissions` 和 `plan`                                          |
| `addDirectories`    | `directories`、`destination`      | 新增工作目錄。`directories` 是路徑字串的陣列                                                                                        |
| `removeDirectories` | `directories`、`destination`      | 移除工作目錄                                                                                                               |

每個項目上的 `destination` 欄位決定變更是保留在記憶體中還是持久化到設定檔。

| `destination`     | 寫入                            |
| :---------------- | :---------------------------- |
| `session`         | 僅在記憶體中，工作階段結束時丟棄              |
| `localSettings`   | `.claude/settings.local.json` |
| `projectSettings` | `.claude/settings.json`       |
| `userSettings`    | `~/.claude/settings.json`     |

Hook 可以回顯它接收的 `permission_suggestions` 之一作為其自己的 `updatedPermissions` 輸出，這等同於使用者在對話框中選擇該「總是允許」選項。

### PostToolUse

在工具成功完成後立即執行。

匹配工具名稱，與 PreToolUse 相同的值。

#### PostToolUse 輸入

`PostToolUse` hooks 在工具已經成功執行後觸發。輸入包括 `tool_input`（發送給工具的參數）和 `tool_response`（它返回的結果）。兩者的確切架構取決於工具。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  },
  "tool_use_id": "toolu_01ABC123..."
}
```

#### PostToolUse 決定控制

`PostToolUse` hooks 可以在工具執行後向 Claude 提供反饋。除了所有 hooks 可用的 [JSON 輸出欄位](#json-output) 外，您的 hook 指令碼可以返回這些事件特定欄位：

| 欄位                     | 描述                                           |
| :--------------------- | :------------------------------------------- |
| `decision`             | `"block"` 提示 Claude 使用 `reason`。省略以允許操作進行    |
| `reason`               | 當 `decision` 為 `"block"` 時向 Claude 顯示的解釋     |
| `additionalContext`    | Claude 要考慮的額外上下文                             |
| `updatedMCPToolOutput` | 僅適用於 [MCP 工具](#match-mcp-tools)：用提供的值替換工具的輸出 |

```json  theme={null}
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude"
  }
}
```

### PostToolUseFailure

當工具執行失敗時執行。此事件針對拋出錯誤或返回失敗結果的工具呼叫觸發。使用此項來記錄失敗、發送警報或向 Claude 提供更正反饋。

匹配工具名稱，與 PreToolUse 相同的值。

#### PostToolUseFailure 輸入

PostToolUseFailure hooks 接收與 PostToolUse 相同的 `tool_name` 和 `tool_input` 欄位，以及作為頂層欄位的錯誤資訊：

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUseFailure",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run test suite"
  },
  "tool_use_id": "toolu_01ABC123...",
  "error": "Command exited with non-zero status code 1",
  "is_interrupt": false
}
```

| 欄位             | 描述                    |
| :------------- | :-------------------- |
| `error`        | 描述出錯的字串               |
| `is_interrupt` | 可選的布林值，指示失敗是否由使用者中斷引起 |

#### PostToolUseFailure 決定控制

`PostToolUseFailure` hooks 可以在工具失敗後向 Claude 提供上下文。除了所有 hooks 可用的 [JSON 輸出欄位](#json-output) 外，您的 hook 指令碼可以返回這些事件特定欄位：

| 欄位                  | 描述                    |
| :------------------ | :-------------------- |
| `additionalContext` | Claude 要與錯誤一起考慮的額外上下文 |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUseFailure",
    "additionalContext": "Additional information about the failure for Claude"
  }
}
```

### Notification

當 Claude Code 發送通知時執行。匹配通知類型：`permission_prompt`、`idle_prompt`、`auth_success`、`elicitation_dialog`。省略匹配器以針對所有通知類型執行 hooks。

使用單獨的匹配器根據通知類型執行不同的處理程式。此配置在 Claude 需要權限批准時觸發權限特定的警報指令碼，在 Claude 閒置時觸發不同的通知：

```json  theme={null}
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/permission-alert.sh"
          }
        ]
      },
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/idle-notification.sh"
          }
        ]
      }
    ]
  }
}
```

#### Notification 輸入

除了 [通用輸入欄位](#common-input-fields) 外，Notification hooks 還接收包含通知文字的 `message`、可選的 `title` 和指示哪個類型觸發的 `notification_type`。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Notification",
  "message": "Claude needs your permission to use Bash",
  "title": "Permission needed",
  "notification_type": "permission_prompt"
}
```

Notification hooks 無法阻止或修改通知。除了所有 hooks 可用的 [JSON 輸出欄位](#json-output) 外，您可以返回 `additionalContext` 以向對話新增上下文：

| 欄位                  | 描述                |
| :------------------ | :---------------- |
| `additionalContext` | 新增到 Claude 上下文的字串 |

### SubagentStart

當通過 Agent 工具生成 Claude Code subagent 時執行。支援匹配器以按代理類型名稱篩選（內建代理，如 `Bash`、`Explore`、`Plan` 或來自 `.claude/agents/` 的自訂代理名稱）。

#### SubagentStart 輸入

除了 [通用輸入欄位](#common-input-fields) 外，SubagentStart hooks 還接收 `agent_id`（subagent 的唯一識別碼）和 `agent_type`（代理名稱，內建代理，如 `"Bash"`、`"Explore"`、`"Plan"` 或自訂代理名稱）。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SubagentStart",
  "agent_id": "agent-abc123",
  "agent_type": "Explore"
}
```

SubagentStart hooks 無法阻止 subagent 建立，但它們可以將上下文注入到 subagent 中。除了所有 hooks 可用的 [JSON 輸出欄位](#json-output) 外，您可以返回：

| 欄位                  | 描述                  |
| :------------------ | :------------------ |
| `additionalContext` | 新增到 subagent 上下文的字串 |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "Follow security guidelines for this task"
  }
}
```

### SubagentStop

當 Claude Code subagent 完成回應時執行。匹配代理類型，與 SubagentStart 相同的值。

#### SubagentStop 輸入

除了 [通用輸入欄位](#common-input-fields) 外，SubagentStop hooks 還接收 `stop_hook_active`、`agent_id`、`agent_type`、`agent_transcript_path` 和 `last_assistant_message`。`agent_type` 欄位是用於匹配器篩選的值。`transcript_path` 是主工作階段的成績單，而 `agent_transcript_path` 是 subagent 自己的成績單，存儲在嵌套的 `subagents/` 資料夾中。`last_assistant_message` 欄位包含 subagent 最終回應的文字內容，因此 hooks 可以存取它而無需解析成績單檔案。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../abc123.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SubagentStop",
  "stop_hook_active": false,
  "agent_id": "def456",
  "agent_type": "Explore",
  "agent_transcript_path": "~/.claude/projects/.../abc123/subagents/agent-def456.jsonl",
  "last_assistant_message": "Analysis complete. Found 3 potential issues..."
}
```

SubagentStop hooks 使用與 [Stop hooks](#stop-decision-control) 相同的決定控制格式。

### Stop

當主 Claude Code 代理完成回應時執行。如果停止是由於使用者中斷，則不執行。API 錯誤會觸發 [StopFailure](#stopfailure)。

#### Stop 輸入

除了 [通用輸入欄位](#common-input-fields) 外，Stop hooks 還接收 `stop_hook_active` 和 `last_assistant_message`。`stop_hook_active` 欄位在 Claude Code 已經作為 stop hook 的結果繼續時為 `true`。檢查此值或處理成績單以防止 Claude Code 無限執行。`last_assistant_message` 欄位包含 Claude 最終回應的文字內容，因此 hooks 可以存取它而無需解析成績單檔案。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": true,
  "last_assistant_message": "I've completed the refactoring. Here's a summary..."
}
```

#### Stop 決定控制

`Stop` 和 `SubagentStop` hooks 可以控制 Claude 是否繼續。除了所有 hooks 可用的 [JSON 輸出欄位](#json-output) 外，您的 hook 指令碼可以返回這些事件特定欄位：

| 欄位         | 描述                                              |
| :--------- | :---------------------------------------------- |
| `decision` | `"block"` 防止 Claude 停止。省略以允許 Claude 停止          |
| `reason`   | 當 `decision` 為 `"block"` 時必需。告訴 Claude 為什麼它應該繼續 |

```json  theme={null}
{
  "decision": "block",
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

### StopFailure

當轉向因 API 錯誤而結束時執行，而不是 [Stop](#stop)。輸出和退出代碼被忽略。使用此項來記錄失敗、發送警報或在 Claude 因速率限制、驗證問題或其他 API 錯誤而無法完成回應時採取恢復操作。

#### StopFailure 輸入

除了 [通用輸入欄位](#common-input-fields) 外，StopFailure hooks 還接收 `error`、可選的 `error_details` 和可選的 `last_assistant_message`。`error` 欄位識別錯誤類型，用於匹配器篩選。

| 欄位                       | 描述                                                                                                                                   |
| :----------------------- | :----------------------------------------------------------------------------------------------------------------------------------- |
| `error`                  | 錯誤類型：`rate_limit`、`authentication_failed`、`billing_error`、`invalid_request`、`server_error`、`max_output_tokens` 或 `unknown`           |
| `error_details`          | 有關錯誤的其他詳細資訊（如果可用）                                                                                                                    |
| `last_assistant_message` | 在對話中顯示的呈現錯誤文字。與 `Stop` 和 `SubagentStop` 不同，其中此欄位包含 Claude 的對話輸出，對於 `StopFailure`，它包含 API 錯誤字串本身，例如 `"API Error: Rate limit reached"` |

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "StopFailure",
  "error": "rate_limit",
  "error_details": "429 Too Many Requests",
  "last_assistant_message": "API Error: Rate limit reached"
}
```

StopFailure hooks 沒有決定控制。它們僅用於通知和記錄目的執行。

### TeammateIdle

當 [agent team](/zh-TW/agent-teams) 隊友在完成其輪次後即將閒置時執行。使用此項來在隊友停止工作之前強制執行品質閘道，例如要求通過 lint 檢查或驗證輸出檔案存在。

當 `TeammateIdle` hook 以代碼 2 退出時，隊友會收到 stderr 訊息作為反饋，並繼續工作而不是閒置。要完全停止隊友而不是重新執行它，請返回 JSON，其中 `{"continue": false, "stopReason": "..."}`。TeammateIdle hooks 不支援匹配器，在每次出現時觸發。

#### TeammateIdle 輸入

除了 [通用輸入欄位](#common-input-fields) 外，TeammateIdle hooks 還接收 `teammate_name` 和 `team_name`。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TeammateIdle",
  "teammate_name": "researcher",
  "team_name": "my-project"
}
```

| 欄位              | 描述         |
| :-------------- | :--------- |
| `teammate_name` | 即將閒置的隊友的名稱 |
| `team_name`     | 團隊的名稱      |

#### TeammateIdle 決定控制

TeammateIdle hooks 支援兩種方式來控制隊友行為：

* **退出代碼 2**：隊友會收到 stderr 訊息作為反饋，並繼續工作而不是閒置。
* **JSON `{"continue": false, "stopReason": "..."}`**：完全停止隊友，匹配 `Stop` hook 行為。`stopReason` 向使用者顯示。

此範例在允許隊友閒置之前檢查建置成品是否存在：

```bash  theme={null}
#!/bin/bash

if [ ! -f "./dist/output.js" ]; then
  echo "Build artifact missing. Run the build before stopping." >&2
  exit 2
fi

exit 0
```

### TaskCompleted

當任務被標記為已完成時執行。這在兩種情況下觸發：當任何代理通過 TaskUpdate 工具明確標記任務為已完成時，或當 [agent team](/zh-TW/agent-teams) 隊友完成其輪次並有進行中的任務時。使用此項來強制執行完成條件，例如通過測試或 lint 檢查，然後任務才能關閉。

當 `TaskCompleted` hook 以代碼 2 退出時，任務不被標記為已完成，stderr 訊息被反饋給模型作為反饋。要完全停止隊友而不是重新執行它，請返回 JSON，其中 `{"continue": false, "stopReason": "..."}`。TaskCompleted hooks 不支援匹配器，在每次出現時觸發。

#### TaskCompleted 輸入

除了 [通用輸入欄位](#common-input-fields) 外，TaskCompleted hooks 還接收 `task_id`、`task_subject` 和可選的 `task_description`、`teammate_name` 和 `team_name`。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TaskCompleted",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "my-project"
}
```

| 欄位                 | 描述               |
| :----------------- | :--------------- |
| `task_id`          | 被完成的任務的識別碼       |
| `task_subject`     | 任務的標題            |
| `task_description` | 任務的詳細描述。可能不存在    |
| `teammate_name`    | 完成任務的隊友的名稱。可能不存在 |
| `team_name`        | 團隊的名稱。可能不存在      |

#### TaskCompleted 決定控制

TaskCompleted hooks 支援兩種方式來控制任務完成：

* **退出代碼 2**：任務不被標記為已完成，stderr 訊息被反饋給模型作為反饋。
* **JSON `{"continue": false, "stopReason": "..."}`**：完全停止隊友，匹配 `Stop` hook 行為。`stopReason` 向使用者顯示。

此範例執行測試並在失敗時阻止任務完成：

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

# 執行測試套件
if ! npm test 2>&1; then
  echo "Tests not passing. Fix failing tests before completing: $TASK_SUBJECT" >&2
  exit 2
fi

exit 0
```

### ConfigChange

當配置檔案在工作階段期間變更時執行。使用此項來稽核設定變更、強制執行安全原則或阻止對配置檔案的未授權修改。

ConfigChange hooks 針對設定檔、受管理的原則設定和 skill 檔案的變更觸發。輸入中的 `source` 欄位告訴您哪種類型的配置變更，可選的 `file_path` 欄位提供變更檔案的路徑。

匹配器篩選配置來源：

| 匹配器                | 何時觸發                             |
| :----------------- | :------------------------------- |
| `user_settings`    | `~/.claude/settings.json` 變更     |
| `project_settings` | `.claude/settings.json` 變更       |
| `local_settings`   | `.claude/settings.local.json` 變更 |
| `policy_settings`  | 受管理的原則設定變更                       |
| `skills`           | `.claude/skills/` 中的 skill 檔案變更  |

此範例記錄所有配置變更以進行安全稽核：

```json  theme={null}
{
  "hooks": {
    "ConfigChange": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/audit-config-change.sh"
          }
        ]
      }
    ]
  }
}
```

#### ConfigChange 輸入

除了 [通用輸入欄位](#common-input-fields) 外，ConfigChange hooks 還接收 `source` 和可選的 `file_path`。`source` 欄位指示哪種配置類型變更，`file_path` 提供被修改的特定檔案的路徑。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "ConfigChange",
  "source": "project_settings",
  "file_path": "/Users/.../my-project/.claude/settings.json"
}
```

#### ConfigChange 決定控制

ConfigChange hooks 可以阻止配置變更生效。使用退出代碼 2 或 JSON `decision` 來防止變更。被阻止時，新設定不會應用於執行中的工作階段。

| 欄位         | 描述                                  |
| :--------- | :---------------------------------- |
| `decision` | `"block"` 防止配置變更被應用。省略以允許變更         |
| `reason`   | 當 `decision` 為 `"block"` 時向使用者顯示的解釋 |

```json  theme={null}
{
  "decision": "block",
  "reason": "Configuration changes to project settings require admin approval"
}
```

`policy_settings` 變更無法被阻止。Hooks 仍然針對 `policy_settings` 來源觸發，因此您可以使用它們進行稽核記錄，但任何阻止決定都會被忽略。這確保企業管理的設定始終生效。

### WorktreeCreate

當您執行 `claude --worktree` 或 [subagent 使用 `isolation: "worktree"`](/zh-TW/sub-agents#choose-the-subagent-scope) 時，Claude Code 使用 `git worktree` 建立隔離的工作副本。如果您配置 WorktreeCreate hook，它會替換預設的 git 行為，讓您使用不同的版本控制系統，如 SVN、Perforce 或 Mercurial。

Hook 必須在 stdout 上列印建立的 worktree 目錄的絕對路徑。Claude Code 使用此路徑作為隔離工作階段的工作目錄。

此範例建立 SVN 工作副本並列印路徑供 Claude Code 使用。將儲存庫 URL 替換為您自己的：

```json  theme={null}
{
  "hooks": {
    "WorktreeCreate": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'NAME=$(jq -r .name); DIR=\"$HOME/.claude/worktrees/$NAME\"; svn checkout https://svn.example.com/repo/trunk \"$DIR\" >&2 && echo \"$DIR\"'"
          }
        ]
      }
    ]
  }
}
```

Hook 從 stdin 上的 JSON 輸入讀取 worktree `name`，將新副本簽出到新目錄，並列印目錄路徑。最後一行的 `echo` 是 Claude Code 讀取的 worktree 路徑。將任何其他輸出重定向到 stderr，以免干擾路徑。

#### WorktreeCreate 輸入

除了 [通用輸入欄位](#common-input-fields) 外，WorktreeCreate hooks 還接收 `name` 欄位。這是新 worktree 的 slug 識別碼，由使用者指定或自動生成（例如 `bold-oak-a3f2`）。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeCreate",
  "name": "feature-auth"
}
```

#### WorktreeCreate 輸出

Hook 必須在 stdout 上列印建立的 worktree 目錄的絕對路徑。如果 hook 失敗或不產生輸出，worktree 建立失敗並出現錯誤。

WorktreeCreate hooks 不使用標準的允許/阻止決定模型。相反，hook 的成功或失敗決定結果。僅支援 `type: "command"` hooks。

### WorktreeRemove

[WorktreeCreate](#worktreecreate) 的清理對應項。此 hook 在 worktree 被移除時觸發，要麼當您退出 `--worktree` 工作階段並選擇移除它時，要麼當具有 `isolation: "worktree"` 的 subagent 完成時。對於基於 git 的 worktrees，Claude 使用 `git worktree remove` 自動處理清理。如果您為非 git 版本控制系統配置了 WorktreeCreate hook，請將其與 WorktreeRemove hook 配對以處理清理。沒有它，worktree 目錄會留在磁碟上。

Claude Code 將 WorktreeCreate 在 stdout 上列印的路徑作為 `worktree_path` 在 hook 輸入中傳遞。此範例讀取該路徑並移除目錄：

```json  theme={null}
{
  "hooks": {
    "WorktreeRemove": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'jq -r .worktree_path | xargs rm -rf'"
          }
        ]
      }
    ]
  }
}
```

#### WorktreeRemove 輸入

除了 [通用輸入欄位](#common-input-fields) 外，WorktreeRemove hooks 還接收 `worktree_path` 欄位，這是被移除的 worktree 的絕對路徑。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeRemove",
  "worktree_path": "/Users/.../my-project/.claude/worktrees/feature-auth"
}
```

WorktreeRemove hooks 沒有決定控制。它們無法阻止 worktree 移除，但可以執行清理任務，如移除版本控制狀態或存檔變更。Hook 失敗僅在偵錯模式中記錄。僅支援 `type: "command"` hooks。

### PreCompact

在 Claude Code 即將執行壓縮操作之前執行。

匹配器值指示壓縮是手動觸發還是自動觸發：

| 匹配器      | 何時觸發         |
| :------- | :----------- |
| `manual` | `/compact`   |
| `auto`   | 當上下文視窗滿時自動壓縮 |

#### PreCompact 輸入

除了 [通用輸入欄位](#common-input-fields) 外，PreCompact hooks 還接收 `trigger` 和 `custom_instructions`。對於 `manual`，`custom_instructions` 包含使用者傳遞到 `/compact` 的內容。對於 `auto`，`custom_instructions` 為空。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```

### PostCompact

在 Claude Code 完成壓縮操作後執行。使用此事件來對新的壓縮狀態做出反應，例如記錄生成的摘要或更新外部狀態。

與 `PreCompact` 相同的匹配器值適用：

| 匹配器      | 何時觸發           |
| :------- | :------------- |
| `manual` | 在 `/compact` 後 |
| `auto`   | 在上下文視窗滿時自動壓縮後  |

#### PostCompact 輸入

除了 [通用輸入欄位](#common-input-fields) 外，PostCompact hooks 還接收 `trigger` 和 `compact_summary`。`compact_summary` 欄位包含壓縮操作生成的對話摘要。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PostCompact",
  "trigger": "manual",
  "compact_summary": "Summary of the compacted conversation..."
}
```

PostCompact hooks 沒有決定控制。它們無法影響壓縮結果，但可以執行後續任務。

### SessionEnd

當 Claude Code 工作階段結束時執行。適用於清理任務、記錄工作階段統計資訊或儲存工作階段狀態。支援匹配器以按退出原因篩選。

輸入中的 `reason` 欄位指示工作階段為何結束：

| 原因                            | 描述                     |
| :---------------------------- | :--------------------- |
| `clear`                       | 使用 `/clear` 命令清除工作階段   |
| `resume`                      | 通過互動式 `/resume` 切換工作階段 |
| `logout`                      | 使用者登出                  |
| `prompt_input_exit`           | 使用者在提示輸入可見時退出          |
| `bypass_permissions_disabled` | 繞過權限模式被停用              |
| `other`                       | 其他退出原因                 |

#### SessionEnd 輸入

除了 [通用輸入欄位](#common-input-fields) 外，SessionEnd hooks 還接收指示工作階段為何結束的 `reason` 欄位。有關所有值，請參閱上面的 [原因表](#sessionend)。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionEnd",
  "reason": "other"
}
```

SessionEnd hooks 沒有決定控制。它們無法阻止工作階段終止，但可以執行清理任務。

SessionEnd hooks 的預設逾時為 1.5 秒。這適用於工作階段退出、`/clear` 和通過互動式 `/resume` 切換工作階段。如果您的 hooks 需要更多時間，請將 `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` 環境變數設定為毫秒的更高值。任何每個 hook 的 `timeout` 設定也受此值的限制。

```bash  theme={null}
CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS=5000 claude
```

### Elicitation

當 MCP 伺服器在任務中途請求使用者輸入時執行。預設情況下，Claude Code 顯示互動式對話框供使用者回應。Hooks 可以攔截此請求並以程式方式回應，完全跳過對話框。

匹配器欄位與 MCP 伺服器名稱匹配。

#### Elicitation 輸入

除了 [通用輸入欄位](#common-input-fields) 外，Elicitation hooks 還接收 `mcp_server_name`、`message` 和可選的 `mode`、`url`、`elicitation_id` 和 `requested_schema` 欄位。

對於表單模式徵詢（最常見的情況）：

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please provide your credentials",
  "mode": "form",
  "requested_schema": {
    "type": "object",
    "properties": {
      "username": { "type": "string", "title": "Username" }
    }
  }
}
```

對於 URL 模式徵詢（基於瀏覽器的驗證）：

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please authenticate",
  "mode": "url",
  "url": "https://auth.example.com/login"
}
```

#### Elicitation 輸出

要以程式方式回應而不顯示對話框，請返回帶有 `hookSpecificOutput` 的 JSON 物件：

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "Elicitation",
    "action": "accept",
    "content": {
      "username": "alice"
    }
  }
}
```

| 欄位        | 值                           | 描述                                   |
| :-------- | :-------------------------- | :----------------------------------- |
| `action`  | `accept`、`decline`、`cancel` | 是否接受、拒絕或取消請求                         |
| `content` | 物件                          | 要提交的表單欄位值。僅在 `action` 為 `accept` 時使用 |

退出代碼 2 拒絕徵詢並向使用者顯示 stderr。

### ElicitationResult

在使用者回應 MCP 徵詢後執行。Hooks 可以觀察、修改或阻止回應，然後將其發送回 MCP 伺服器。

匹配器欄位與 MCP 伺服器名稱匹配。

#### ElicitationResult 輸入

除了 [通用輸入欄位](#common-input-fields) 外，ElicitationResult hooks 還接收 `mcp_server_name`、`action` 和可選的 `mode`、`elicitation_id` 和 `content` 欄位。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "ElicitationResult",
  "mcp_server_name": "my-mcp-server",
  "action": "accept",
  "content": { "username": "alice" },
  "mode": "form",
  "elicitation_id": "elicit-123"
}
```

#### ElicitationResult 輸出

要覆蓋使用者的回應，請返回帶有 `hookSpecificOutput` 的 JSON 物件：

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "ElicitationResult",
    "action": "decline",
    "content": {}
  }
}
```

| 欄位        | 值                           | 描述                                  |
| :-------- | :-------------------------- | :---------------------------------- |
| `action`  | `accept`、`decline`、`cancel` | 覆蓋使用者的操作                            |
| `content` | 物件                          | 覆蓋表單欄位值。僅在 `action` 為 `accept` 時有意義 |

退出代碼 2 阻止回應，將有效操作變更為 `decline`。

## 基於提示的 hooks

除了命令和 HTTP hooks 外，Claude Code 還支援基於提示的 hooks（`type: "prompt"`），使用 LLM 評估是否允許或阻止操作，以及代理 hooks（`type: "agent"`），生成具有工具存取權限的代理驗證器。並非所有事件都支援每種 hook 類型。

支援所有四種 hook 類型（`command`、`http`、`prompt` 和 `agent`）的事件：

* `PermissionRequest`
* `PostToolUse`
* `PostToolUseFailure`
* `PreToolUse`
* `Stop`
* `SubagentStop`
* `TaskCompleted`
* `UserPromptSubmit`

僅支援 `type: "command"` hooks 的事件：

* `ConfigChange`
* `Elicitation`
* `ElicitationResult`
* `InstructionsLoaded`
* `Notification`
* `PostCompact`
* `PreCompact`
* `SessionEnd`
* `SessionStart`
* `StopFailure`
* `SubagentStart`
* `TeammateIdle`
* `WorktreeCreate`
* `WorktreeRemove`

### 基於提示的 hooks 如何工作

基於提示的 hooks 不執行 Bash 命令，而是：

1. 將 hook 輸入和您的提示發送到 Claude 模型，預設為 Haiku
2. LLM 以包含決定的結構化 JSON 回應
3. Claude Code 自動處理決定

### 提示 hook 配置

將 `type` 設定為 `"prompt"` 並提供 `prompt` 字串而不是 `command`。使用 `$ARGUMENTS` 佔位符將 hook 的 JSON 輸入資料注入到您的提示文字中。Claude Code 將組合的提示和輸入發送到快速 Claude 模型，該模型返回 JSON 決定。

此 `Stop` hook 詢問 LLM 在允許 Claude 完成之前是否應該停止：

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete."
          }
        ]
      }
    ]
  }
}
```

| 欄位        | 必需 | 描述                                                                                     |
| :-------- | :- | :------------------------------------------------------------------------------------- |
| `type`    | 是  | 必須為 `"prompt"`                                                                         |
| `prompt`  | 是  | 要發送到 LLM 的提示文字。使用 `$ARGUMENTS` 作為 hook 輸入 JSON 的佔位符。如果 `$ARGUMENTS` 不存在，輸入 JSON 會附加到提示 |
| `model`   | 否  | 用於評估的模型。預設為快速模型                                                                        |
| `timeout` | 否  | 逾時（秒）。預設值：30                                                                           |

### 回應架構

LLM 必須以包含以下內容的 JSON 回應：

```json  theme={null}
{
  "ok": true | false,
  "reason": "Explanation for the decision"
}
```

| 欄位       | 描述                                  |
| :------- | :---------------------------------- |
| `ok`     | `true` 允許操作，`false` 防止它             |
| `reason` | 當 `ok` 為 `false` 時必需。向 Claude 顯示的解釋 |

### 範例：多條件 Stop hook

此 `Stop` hook 使用詳細提示在允許 Claude 停止之前檢查三個條件。如果 `"ok"` 為 `false`，Claude 繼續工作，提供的原因作為其下一個指令。`SubagentStop` hooks 使用相同的格式來評估 [subagent](/zh-TW/sub-agents) 是否應該停止：

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are evaluating whether Claude should stop working. Context: $ARGUMENTS\n\nAnalyze the conversation and determine if:\n1. All user-requested tasks are complete\n2. Any errors need to be addressed\n3. Follow-up work is needed\n\nRespond with JSON: {\"ok\": true} to allow stopping, or {\"ok\": false, \"reason\": \"your explanation\"} to continue working.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## 基於代理的 hooks

基於代理的 hooks（`type: "agent"`）類似於基於提示的 hooks，但具有多輪工具存取。代理 hook 不是單一 LLM 呼叫，而是生成一個可以讀取檔案、搜尋程式碼和檢查程式碼庫以驗證條件的 subagent。代理 hooks 支援與基於提示的 hooks 相同的事件。

### 代理 hooks 如何工作

當代理 hook 觸發時：

1. Claude Code 生成一個 subagent，使用您的提示和 hook 的 JSON 輸入
2. Subagent 可以使用 Read、Grep 和 Glob 等工具進行調查
3. 在最多 50 輪後，subagent 返回結構化的 `{ "ok": true/false }` 決定
4. Claude Code 以與提示 hook 相同的方式處理決定

代理 hooks 在驗證需要檢查實際檔案或測試輸出時很有用，而不僅僅是評估 hook 輸入資料。

### 代理 hook 配置

將 `type` 設定為 `"agent"` 並提供 `prompt` 字串。配置欄位與 [提示 hooks](#prompt-hook-configuration) 相同，但逾時更長：

| 欄位        | 必需 | 描述                                               |
| :-------- | :- | :----------------------------------------------- |
| `type`    | 是  | 必須為 `"agent"`                                    |
| `prompt`  | 是  | 描述要驗證的內容的提示。使用 `$ARGUMENTS` 作為 hook 輸入 JSON 的佔位符 |
| `model`   | 否  | 要使用的模型。預設為快速模型                                   |
| `timeout` | 否  | 逾時（秒）。預設值：60                                     |

回應架構與提示 hooks 相同：`{ "ok": true }` 允許或 `{ "ok": false, "reason": "..." }` 阻止。

此 `Stop` hook 驗證所有單元測試通過，然後允許 Claude 完成：

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

## 在背景執行 hooks

預設情況下，hooks 會阻止 Claude 的執行，直到它們完成。對於長時間執行的任務，如部署、測試套件或外部 API 呼叫，設定 `"async": true` 以在背景執行 hook，同時 Claude 繼續工作。非同步 hooks 無法阻止或控制 Claude 的行為：回應欄位，如 `decision`、`permissionDecision` 和 `continue` 沒有效果，因為它們會控制的操作已經完成。

### 配置非同步 hook

將 `"async": true` 新增到命令 hook 的配置以在背景執行它而不阻止 Claude。此欄位僅在 `type: "command"` hooks 上可用。

此 hook 在每個 `Write` 工具呼叫後執行測試指令碼。Claude 立即繼續工作，同時 `run-tests.sh` 執行最多 120 秒。當指令碼完成時，其輸出在下一個對話輪次上傳遞：

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/run-tests.sh",
            "async": true,
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

`timeout` 欄位設定背景程序的最大時間（秒）。如果未指定，非同步 hooks 使用與同步 hooks 相同的 10 分鐘預設值。

### 非同步 hooks 如何執行

當非同步 hook 觸發時，Claude Code 啟動 hook 程序並立即繼續，而不等待它完成。Hook 在 stdin 上接收與同步 hook 相同的 JSON 輸入。

背景程序退出後，如果 hook 產生了帶有 `systemMessage` 或 `additionalContext` 欄位的 JSON 回應，該內容會在下一個對話輪次上作為上下文傳遞給 Claude。

非同步 hook 完成通知預設被抑制。要查看它們，請使用 `Ctrl+O` 啟用詳細模式或使用 `--verbose` 啟動 Claude Code。

### 範例：檔案變更後執行測試

此 hook 在 Claude 寫入檔案時在背景啟動測試套件，然後在測試完成時將結果報告回 Claude。將此指令碼儲存到專案中的 `.claude/hooks/run-tests-async.sh` 並使用 `chmod +x` 使其可執行：

```bash  theme={null}
#!/bin/bash
# run-tests-async.sh

# 從 stdin 讀取 hook 輸入
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# 僅針對原始檔案執行測試
if [[ "$FILE_PATH" != *.ts && "$FILE_PATH" != *.js ]]; then
  exit 0
fi

# 執行測試並通過 systemMessage 報告結果
RESULT=$(npm test 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "{\"systemMessage\": \"Tests passed after editing $FILE_PATH\"}"
else
  echo "{\"systemMessage\": \"Tests failed after editing $FILE_PATH: $RESULT\"}"
fi
```

然後將此配置新增到專案根目錄中的 `.claude/settings.json`。`async: true` 標誌讓 Claude 在測試執行時繼續工作：

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/run-tests-async.sh",
            "async": true,
            "timeout": 300
          }
        ]
      }
    ]
  }
}
```

### 限制

非同步 hooks 與同步 hooks 相比有幾個限制：

* 僅 `type: "command"` hooks 支援 `async`。基於提示的 hooks 無法非同步執行。
* 非同步 hooks 無法阻止工具呼叫或返回決定。到 hook 完成時，觸發操作已經進行。
* Hook 輸出在下一個對話輪次上傳遞。如果工作階段閒置，回應會等待直到下一個使用者互動。
* 每次執行都會建立一個單獨的背景程序。同一非同步 hook 的多次觸發之間沒有去重。

## 安全考慮

### 免責聲明

命令 hooks 以您的系統使用者的完整權限執行。

<Warning>
  命令 hooks 以您的完整使用者權限執行 shell 命令。它們可以修改、刪除或存取您的使用者帳戶可以存取的任何檔案。在將任何 hook 命令新增到您的配置之前，請審查並測試它們。
</Warning>

### 安全最佳實踐

編寫 hooks 時，請記住這些實踐：

* **驗證和清理輸入**：永遠不要盲目信任輸入資料
* **始終引用 shell 變數**：使用 `"$VAR"` 而不是 `$VAR`
* **阻止路徑遍歷**：檢查檔案路徑中的 `..`
* **使用絕對路徑**：為指令碼指定完整路徑，使用 `"$CLAUDE_PROJECT_DIR"` 作為專案根目錄
* **跳過敏感檔案**：避免 `.env`、`.git/`、金鑰等

## 偵錯 hooks

執行 `claude --debug` 以查看 hook 執行詳細資訊，包括哪些 hooks 匹配、它們的退出代碼和輸出。使用 `Ctrl+O` 切換詳細模式以在成績單中查看 hook 進度。

```text  theme={null}
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Getting matching hook commands for PostToolUse with query: Write
[DEBUG] Found 1 hook matchers in settings
[DEBUG] Matched 1 hooks for query "Write"
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 600000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

有關故障排除常見問題，如 hooks 不觸發、無限 Stop hook 迴圈或配置錯誤，請參閱指南中的 [限制和故障排除](/zh-TW/hooks-guide#limitations-and-troubleshooting)。
