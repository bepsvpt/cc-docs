> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 使用 hooks 自動化工作流程

> 當 Claude Code 編輯檔案、完成任務或需要輸入時，自動執行 shell 命令。格式化程式碼、發送通知、驗證命令並強制執行專案規則。

Hooks 是使用者定義的 shell 命令，在 Claude Code 生命週期的特定時間點執行。它們提供對 Claude Code 行為的確定性控制，確保某些操作始終發生，而不是依賴 LLM 選擇執行它們。使用 hooks 來強制執行專案規則、自動化重複性任務，並將 Claude Code 與您現有的工具整合。

對於需要判斷而不是確定性規則的決策，您也可以使用[基於提示的 hooks](#prompt-based-hooks) 或[基於代理的 hooks](#agent-based-hooks)，它們使用 Claude 模型來評估條件。

有關擴展 Claude Code 的其他方式，請參閱[skills](/zh-TW/skills)以提供 Claude 額外的指令和可執行命令、[subagents](/zh-TW/sub-agents)以在隔離的上下文中執行任務，以及[plugins](/zh-TW/plugins)以打包要在專案間共享的擴展。

<Tip>
  本指南涵蓋常見用例和入門方式。有關完整的事件架構、JSON 輸入/輸出格式和非同步 hooks 和 MCP 工具 hooks 等進階功能，請參閱 [Hooks 參考](/zh-TW/hooks)。
</Tip>

## 設定您的第一個 hook

若要建立 hook，請將 `hooks` 區塊新增到[設定檔](#configure-hook-location)。本逐步解說建立一個桌面通知 hook，因此每當 Claude 等待您的輸入而不是監視終端時，您都會收到警報。

<Steps>
  <Step title="將 hook 新增到您的設定">
    開啟 `~/.claude/settings.json` 並新增 `Notification` hook。下面的範例使用 `osascript` 進行 macOS；有關 Linux 和 Windows 命令，請參閱[當 Claude 需要輸入時收到通知](#get-notified-when-claude-needs-input)。

    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
              }
            ]
          }
        ]
      }
    }
    ```

    如果您的設定檔已經有 `hooks` 鍵，請將 `Notification` 項目合併到其中，而不是替換整個物件。您也可以透過在 CLI 中描述您想要的內容，要求 Claude 為您編寫 hook。
  </Step>

  <Step title="驗證配置">
    輸入 `/hooks` 以開啟 hooks 瀏覽器。您將看到所有可用 hook 事件的列表，每個配置了 hooks 的事件旁邊都有一個計數。選擇 `Notification` 以確認您的新 hook 出現在列表中。選擇 hook 會顯示其詳細資訊：事件、匹配器、類型、來源檔案和命令。
  </Step>

  <Step title="測試 hook">
    按 `Esc` 返回 CLI。要求 Claude 執行需要權限的操作，然後切換離開終端。您應該會收到桌面通知。
  </Step>
</Steps>

<Tip>
  `/hooks` 選單是唯讀的。若要新增、修改或移除 hooks，請直接編輯您的設定 JSON 或要求 Claude 進行變更。
</Tip>

## 您可以自動化的內容

Hooks 讓您在 Claude Code 生命週期的關鍵點執行程式碼：編輯後格式化檔案、在執行前阻止命令、當 Claude 需要輸入時發送通知、在工作階段開始時注入上下文等。有關 hook 事件的完整列表，請參閱 [Hooks 參考](/zh-TW/hooks#hook-lifecycle)。

每個範例都包含一個現成可用的配置區塊，您可以將其新增到[設定檔](#configure-hook-location)。最常見的模式：

* [當 Claude 需要輸入時收到通知](#get-notified-when-claude-needs-input)
* [編輯後自動格式化程式碼](#auto-format-code-after-edits)
* [阻止編輯受保護的檔案](#block-edits-to-protected-files)
* [壓縮後重新注入上下文](#re-inject-context-after-compaction)
* [審計配置變更](#audit-configuration-changes)
* [當目錄或檔案變更時重新載入環境](#reload-environment-when-directory-or-files-change)
* [自動批准特定權限提示](#auto-approve-specific-permission-prompts)

### 當 Claude 需要輸入時收到通知

每當 Claude 完成工作並需要您的輸入時收到桌面通知，這樣您可以切換到其他任務而無需檢查終端。

此 hook 使用 `Notification` 事件，當 Claude 等待輸入或權限時觸發。下面的每個標籤使用平台的原生通知命令。將此新增到 `~/.claude/settings.json`：

<Tabs>
  <Tab title="macOS">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Linux">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "notify-send 'Claude Code' 'Claude Code needs your attention'"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Windows (PowerShell)">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "powershell.exe -Command \"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')\""
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>
</Tabs>

### 編輯後自動格式化程式碼

在 Claude 編輯的每個檔案上自動執行 [Prettier](https://prettier.io/)，以便格式保持一致而無需手動干預。

此 hook 使用 `PostToolUse` 事件搭配 `Edit|Write` 匹配器，因此它只在檔案編輯工具之後執行。該命令使用 [`jq`](https://jqlang.github.io/jq/) 提取編輯的檔案路徑並將其傳遞給 Prettier。將此新增到您的專案根目錄中的 `.claude/settings.json`：

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

<Note>
  本頁上的 Bash 範例使用 `jq` 進行 JSON 解析。使用 `brew install jq`（macOS）、`apt-get install jq`（Debian/Ubuntu）安裝它，或參閱 [`jq` 下載](https://jqlang.github.io/jq/download/)。
</Note>

### 阻止編輯受保護的檔案

防止 Claude 修改敏感檔案，如 `.env`、`package-lock.json` 或 `.git/` 中的任何內容。Claude 會收到解釋編輯被阻止原因的回饋，因此它可以調整其方法。

此範例使用 hook 呼叫的單獨指令檔。該指令檢查目標檔案路徑是否與受保護的模式列表相符，並以代碼 2 退出以阻止編輯。

<Steps>
  <Step title="建立 hook 指令">
    將此儲存到 `.claude/hooks/protect-files.sh`：

    ```bash  theme={null}
    #!/bin/bash
    # protect-files.sh

    INPUT=$(cat)
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

    PROTECTED_PATTERNS=(".env" "package-lock.json" ".git/")

    for pattern in "${PROTECTED_PATTERNS[@]}"; do
      if [[ "$FILE_PATH" == *"$pattern"* ]]; then
        echo "Blocked: $FILE_PATH matches protected pattern '$pattern'" >&2
        exit 2
      fi
    done

    exit 0
    ```
  </Step>

  <Step title="使指令可執行（macOS/Linux）">
    Hook 指令必須可執行，Claude Code 才能執行它們：

    ```bash  theme={null}
    chmod +x .claude/hooks/protect-files.sh
    ```
  </Step>

  <Step title="註冊 hook">
    將 `PreToolUse` hook 新增到 `.claude/settings.json`，在任何 `Edit` 或 `Write` 工具呼叫之前執行指令：

    ```json  theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Edit|Write",
            "hooks": [
              {
                "type": "command",
                "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Step>
</Steps>

### 壓縮後重新注入上下文

當 Claude 的上下文視窗填滿時，壓縮會總結對話以釋放空間。這可能會遺失重要細節。使用帶有 `compact` 匹配器的 `SessionStart` hook 在每次壓縮後重新注入關鍵上下文。

您的命令寫入 stdout 的任何文字都會新增到 Claude 的上下文中。此範例提醒 Claude 專案慣例和最近的工作。將此新增到您的專案根目錄中的 `.claude/settings.json`：

```json  theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Reminder: use Bun, not npm. Run bun test before committing. Current sprint: auth refactor.'"
          }
        ]
      }
    ]
  }
}
```

您可以將 `echo` 替換為任何產生動態輸出的命令，如 `git log --oneline -5` 以顯示最近的提交。有關在每個工作階段開始時注入上下文，請考慮改用 [CLAUDE.md](/zh-TW/memory)。有關環境變數，請參閱參考中的 [`CLAUDE_ENV_FILE`](/zh-TW/hooks#persist-environment-variables)。

### 審計配置變更

追蹤工作階段期間設定或 skills 檔案何時變更。`ConfigChange` 事件在外部程序或編輯器修改配置檔案時觸發，因此您可以記錄變更以進行合規性檢查或阻止未授權的修改。

此範例將每個變更附加到審計日誌。將此新增到 `~/.claude/settings.json`：

```json  theme={null}
{
  "hooks": {
    "ConfigChange": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "jq -c '{timestamp: now | todate, source: .source, file: .file_path}' >> ~/claude-config-audit.log"
          }
        ]
      }
    ]
  }
}
```

匹配器按配置類型篩選：`user_settings`、`project_settings`、`local_settings`、`policy_settings` 或 `skills`。要阻止變更生效，以代碼 2 退出或傳回 `{"decision": "block"}`。有關完整的輸入架構，請參閱 [ConfigChange 參考](/zh-TW/hooks#configchange)。

### 當目錄或檔案變更時重新載入環境

某些專案根據您所在的目錄設定不同的環境變數。[direnv](https://direnv.net/) 之類的工具在您的 shell 中自動執行此操作，但 Claude 的 Bash 工具不會自行選取這些變更。

`CwdChanged` hook 修復了這個問題：它在 Claude 每次變更目錄時執行，因此您可以為新位置重新載入正確的變數。hook 將更新的值寫入 `CLAUDE_ENV_FILE`，Claude Code 在每個 Bash 命令之前應用它。將此新增到 `~/.claude/settings.json`：

```json  theme={null}
{
  "hooks": {
    "CwdChanged": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "direnv export bash >> \"$CLAUDE_ENV_FILE\""
          }
        ]
      }
    ]
  }
}
```

若要對特定檔案而不是每次目錄變更做出反應，請使用 `FileChanged` 搭配 `matcher` 列出要監視的檔案名稱（以管道分隔）。`matcher` 既配置要監視的檔案，也篩選哪些 hooks 執行。此範例監視當前目錄中 `.envrc` 和 `.env` 的變更：

```json  theme={null}
{
  "hooks": {
    "FileChanged": [
      {
        "matcher": ".envrc|.env",
        "hooks": [
          {
            "type": "command",
            "command": "direnv export bash >> \"$CLAUDE_ENV_FILE\""
          }
        ]
      }
    ]
  }
}
```

有關輸入架構、`watchPaths` 輸出和 `CLAUDE_ENV_FILE` 詳細資訊，請參閱 [CwdChanged](/zh-TW/hooks#cwdchanged) 和 [FileChanged](/zh-TW/hooks#filechanged) 參考項目。

### 自動批准特定權限提示

跳過您始終允許的工具呼叫的批准對話。此範例自動批准 `ExitPlanMode`，這是 Claude 在完成呈現計畫並要求繼續時呼叫的工具，因此您不會在每次計畫準備好時被提示。

與上面的退出代碼範例不同，自動批准要求您的 hook 將 JSON 決策寫入 stdout。`PermissionRequest` hook 在 Claude Code 即將顯示權限對話時觸發，傳回 `"behavior": "allow"` 會代表您回答它。

匹配器將 hook 的範圍限制為僅 `ExitPlanMode`，因此不會影響其他提示。將此新增到 `~/.claude/settings.json`：

```json  theme={null}
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "ExitPlanMode",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\": {\"hookEventName\": \"PermissionRequest\", \"decision\": {\"behavior\": \"allow\"}}}'"
          }
        ]
      }
    ]
  }
}
```

當 hook 批准時，Claude Code 退出計畫模式並恢復進入計畫模式之前處於活動狀態的任何權限模式。文字記錄顯示「由 PermissionRequest hook 允許」，其中對話會出現。hook 路徑始終保持當前對話：它無法清除上下文並以對話可以執行的方式啟動新的實現工作階段。

若要改為設定特定的權限模式，您的 hook 的輸出可以包含帶有 `setMode` 項目的 `updatedPermissions` 陣列。`mode` 值是任何權限模式，如 `default`、`acceptEdits` 或 `bypassPermissions`，`destination: "session"` 僅將其應用於當前工作階段。

若要將工作階段切換到 `acceptEdits`，您的 hook 會將此 JSON 寫入 stdout：

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedPermissions": [
        { "type": "setMode", "mode": "acceptEdits", "destination": "session" }
      ]
    }
  }
}
```

保持匹配器盡可能狹窄。在 `.*` 上進行匹配或留空匹配器會自動批准每個權限提示，包括檔案寫入和 shell 命令。有關決策欄位的完整集合，請參閱 [PermissionRequest 參考](/zh-TW/hooks#permissionrequest-decision-control)。

## Hooks 如何工作

Hook 事件在 Claude Code 的特定生命週期點觸發。當事件觸發時，所有匹配的 hooks 並行執行，相同的 hook 命令會自動去重。下表顯示每個事件及其觸發時間：

| Event                | When it fires                                                                                                                                          |
| :------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`       | When a session begins or resumes                                                                                                                       |
| `UserPromptSubmit`   | When you submit a prompt, before Claude processes it                                                                                                   |
| `PreToolUse`         | Before a tool call executes. Can block it                                                                                                              |
| `PermissionRequest`  | When a permission dialog appears                                                                                                                       |
| `PostToolUse`        | After a tool call succeeds                                                                                                                             |
| `PostToolUseFailure` | After a tool call fails                                                                                                                                |
| `Notification`       | When Claude Code sends a notification                                                                                                                  |
| `SubagentStart`      | When a subagent is spawned                                                                                                                             |
| `SubagentStop`       | When a subagent finishes                                                                                                                               |
| `Stop`               | When Claude finishes responding                                                                                                                        |
| `StopFailure`        | When the turn ends due to an API error. Output and exit code are ignored                                                                               |
| `TeammateIdle`       | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                                     |
| `TaskCompleted`      | When a task is being marked as completed                                                                                                               |
| `InstructionsLoaded` | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session         |
| `ConfigChange`       | When a configuration file changes during a session                                                                                                     |
| `CwdChanged`         | When the working directory changes, for example when Claude executes a `cd` command. Useful for reactive environment management with tools like direnv |
| `FileChanged`        | When a watched file changes on disk. The `matcher` field specifies which filenames to watch                                                            |
| `WorktreeCreate`     | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                            |
| `WorktreeRemove`     | When a worktree is being removed, either at session exit or when a subagent finishes                                                                   |
| `PreCompact`         | Before context compaction                                                                                                                              |
| `PostCompact`        | After context compaction completes                                                                                                                     |
| `Elicitation`        | When an MCP server requests user input during a tool call                                                                                              |
| `ElicitationResult`  | After a user responds to an MCP elicitation, before the response is sent back to the server                                                            |
| `SessionEnd`         | When a session terminates                                                                                                                              |

每個 hook 都有一個 `type` 來決定它如何執行。大多數 hooks 使用 `"type": "command"`，它執行 shell 命令。還有三種其他類型可用：

* `"type": "http"`：POST 事件資料到 URL。請參閱 [HTTP hooks](#http-hooks)。
* `"type": "prompt"`：單輪 LLM 評估。請參閱[基於提示的 hooks](#prompt-based-hooks)。
* `"type": "agent"`：具有工具存取的多輪驗證。請參閱[基於代理的 hooks](#agent-based-hooks)。

### 讀取輸入並傳回輸出

Hooks 透過 stdin、stdout、stderr 和退出代碼與 Claude Code 通訊。當事件觸發時，Claude Code 將事件特定的資料作為 JSON 傳遞到您的指令的 stdin。您的指令讀取該資料、執行其工作，並透過退出代碼告訴 Claude Code 接下來要做什麼。

#### Hook 輸入

每個事件都包含常見欄位，如 `session_id` 和 `cwd`，但每個事件類型都新增不同的資料。例如，當 Claude 執行 Bash 命令時，`PreToolUse` hook 在 stdin 上接收類似以下內容：

```json  theme={null}
{
  "session_id": "abc123",          // 此工作階段的唯一 ID
  "cwd": "/Users/sarah/myproject", // 事件觸發時的工作目錄
  "hook_event_name": "PreToolUse", // 哪個事件觸發了此 hook
  "tool_name": "Bash",             // Claude 即將使用的工具
  "tool_input": {                  // Claude 傳遞給工具的引數
    "command": "npm test"          // 對於 Bash，這是 shell 命令
  }
}
```

您的指令可以解析該 JSON 並對任何這些欄位採取行動。`UserPromptSubmit` hooks 改為取得 `prompt` 文字，`SessionStart` hooks 取得 `source`（startup、resume、clear、compact），等等。有關共享欄位，請參閱參考中的[常見輸入欄位](/zh-TW/hooks#common-input-fields)，以及每個事件的部分以了解事件特定的架構。

#### Hook 輸出

您的指令透過寫入 stdout 或 stderr 並以特定代碼退出來告訴 Claude Code 接下來要做什麼。例如，想要阻止命令的 `PreToolUse` hook：

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q "drop table"; then
  echo "Blocked: dropping tables is not allowed" >&2  // stderr 變成 Claude 的回饋
  exit 2 // exit 2 = 阻止操作
fi

exit 0  // exit 0 = 讓它繼續
```

退出代碼決定接下來會發生什麼：

* **Exit 0**：操作繼續。對於 `UserPromptSubmit` 和 `SessionStart` hooks，您寫入 stdout 的任何內容都會新增到 Claude 的上下文中。
* **Exit 2**：操作被阻止。寫入原因到 stderr，Claude 會收到它作為回饋，以便它可以調整。
* **任何其他退出代碼**：操作繼續。Stderr 被記錄但不顯示給 Claude。使用 `Ctrl+O` 切換詳細模式以在文字記錄中查看這些訊息。

#### 結構化 JSON 輸出

退出代碼給您兩個選項：允許或阻止。為了獲得更多控制，退出 0 並改為將 JSON 物件列印到 stdout。

<Note>
  使用 exit 2 以 stderr 訊息阻止，或使用 exit 0 和 JSON 進行結構化控制。不要混合它們：Claude Code 在您退出 2 時忽略 JSON。
</Note>

例如，`PreToolUse` hook 可以拒絕工具呼叫並告訴 Claude 為什麼，或將其升級給使用者以獲得批准：

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Use rg instead of grep for better performance"
  }
}
```

Claude Code 讀取 `permissionDecision` 並取消工具呼叫，然後將 `permissionDecisionReason` 回饋給 Claude。這三個選項特定於 `PreToolUse`：

* `"allow"`：繼續而不顯示權限提示
* `"deny"`：取消工具呼叫並將原因傳送給 Claude
* `"ask"`：照常向使用者顯示權限提示

其他事件使用不同的決策模式。例如，`PostToolUse` 和 `Stop` hooks 使用頂級 `decision: "block"` 欄位，而 `PermissionRequest` 使用 `hookSpecificOutput.decision.behavior`。有關按事件的完整分解，請參閱參考中的[摘要表](/zh-TW/hooks#decision-control)。

對於 `UserPromptSubmit` hooks，改用 `additionalContext` 將文字注入到 Claude 的上下文中。基於提示的 hooks（`type: "prompt"`）以不同方式處理輸出：請參閱[基於提示的 hooks](#prompt-based-hooks)。

### 使用匹配器篩選 hooks

沒有匹配器，hook 會在其事件的每次出現時觸發。匹配器讓您縮小範圍。例如，如果您只想在檔案編輯後執行格式化程式（而不是在每次工具呼叫後），請將匹配器新增到您的 `PostToolUse` hook：

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "prettier --write ..." }
        ]
      }
    ]
  }
}
```

`"Edit|Write"` 匹配器是與工具名稱相符的正規表達式模式。hook 只在 Claude 使用 `Edit` 或 `Write` 工具時觸發，而不是在它使用 `Bash`、`Read` 或任何其他工具時。

每個事件類型都在特定欄位上進行匹配。匹配器支援精確字串和正規表達式模式：

| 事件                                                                                                      | 匹配器篩選的內容        | 範例匹配器值                                                                                                              |
| :------------------------------------------------------------------------------------------------------ | :-------------- | :------------------------------------------------------------------------------------------------------------------ |
| `PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`PermissionRequest`                                     | 工具名稱            | `Bash`、`Edit\|Write`、`mcp__.*`                                                                                      |
| `SessionStart`                                                                                          | 工作階段如何開始        | `startup`、`resume`、`clear`、`compact`                                                                                |
| `SessionEnd`                                                                                            | 工作階段為什麼結束       | `clear`、`resume`、`logout`、`prompt_input_exit`、`bypass_permissions_disabled`、`other`                                 |
| `Notification`                                                                                          | 通知類型            | `permission_prompt`、`idle_prompt`、`auth_success`、`elicitation_dialog`                                               |
| `SubagentStart`                                                                                         | 代理類型            | `Bash`、`Explore`、`Plan` 或自訂代理名稱                                                                                     |
| `PreCompact`、`PostCompact`                                                                              | 什麼觸發了壓縮         | `manual`、`auto`                                                                                                     |
| `SubagentStop`                                                                                          | 代理類型            | 與 `SubagentStart` 相同的值                                                                                              |
| `ConfigChange`                                                                                          | 配置來源            | `user_settings`、`project_settings`、`local_settings`、`policy_settings`、`skills`                                      |
| `StopFailure`                                                                                           | 錯誤類型            | `rate_limit`、`authentication_failed`、`billing_error`、`invalid_request`、`server_error`、`max_output_tokens`、`unknown` |
| `InstructionsLoaded`                                                                                    | 載入原因            | `session_start`、`nested_traversal`、`path_glob_match`、`include`、`compact`                                            |
| `Elicitation`                                                                                           | MCP 伺服器名稱       | 您配置的 MCP 伺服器名稱                                                                                                      |
| `ElicitationResult`                                                                                     | MCP 伺服器名稱       | 與 `Elicitation` 相同的值                                                                                                |
| `FileChanged`                                                                                           | 檔案名稱（變更檔案的基本名稱） | `.envrc`、`.env`、任何您想監視的檔案名稱                                                                                         |
| `UserPromptSubmit`、`Stop`、`TeammateIdle`、`TaskCompleted`、`WorktreeCreate`、`WorktreeRemove`、`CwdChanged` | 不支援匹配器          | 始終在每次出現時觸發                                                                                                          |

顯示不同事件類型上匹配器的更多範例：

<Tabs>
  <Tab title="記錄每個 Bash 命令">
    只匹配 `Bash` 工具呼叫並將每個命令記錄到檔案。`PostToolUse` 事件在命令完成後觸發，因此 `tool_input.command` 包含執行的內容。hook 在 stdin 上接收事件資料作為 JSON，`jq -r '.tool_input.command'` 只提取命令字串，`>>` 將其附加到日誌檔案：

    ```json  theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Bash",
            "hooks": [
              {
                "type": "command",
                "command": "jq -r '.tool_input.command' >> ~/.claude/command-log.txt"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="匹配 MCP 工具">
    MCP 工具使用與內建工具不同的命名慣例：`mcp__<server>__<tool>`，其中 `<server>` 是 MCP 伺服器名稱，`<tool>` 是它提供的工具。例如，`mcp__github__search_repositories` 或 `mcp__filesystem__read_file`。使用正規表達式匹配器來針對來自特定伺服器的所有工具，或使用 `mcp__.*__write.*` 之類的模式跨伺服器進行匹配。有關完整的範例列表，請參閱參考中的[匹配 MCP 工具](/zh-TW/hooks#match-mcp-tools)。

    下面的命令使用 `jq` 從 hook 的 JSON 輸入中提取工具名稱，並將其寫入 stderr，其中它在詳細模式（`Ctrl+O`）中顯示：

    ```json  theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "mcp__github__.*",
            "hooks": [
              {
                "type": "command",
                "command": "echo \"GitHub tool called: $(jq -r '.tool_name')\" >&2"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="在工作階段結束時清理">
    `SessionEnd` 事件支援工作階段結束原因的匹配器。此 hook 只在 `clear` 時觸發（當您執行 `/clear` 時），而不是在正常退出時：

    ```json  theme={null}
    {
      "hooks": {
        "SessionEnd": [
          {
            "matcher": "clear",
            "hooks": [
              {
                "type": "command",
                "command": "rm -f /tmp/claude-scratch-*.txt"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>
</Tabs>

有關完整的匹配器語法，請參閱 [Hooks 參考](/zh-TW/hooks#configuration)。

### 配置 hook 位置

您新增 hook 的位置決定了其範圍：

| 位置                                                          | 範圍                 | 可共享          |
| :---------------------------------------------------------- | :----------------- | :----------- |
| `~/.claude/settings.json`                                   | 您的所有專案             | 否，本機到您的機器    |
| `.claude/settings.json`                                     | 單個專案               | 是，可以提交到儲存庫   |
| `.claude/settings.local.json`                               | 單個專案               | 否，gitignored |
| 受管理的原則設定                                                    | 組織範圍               | 是，由管理員控制     |
| [Plugin](/zh-TW/plugins) `hooks/hooks.json`                 | 啟用外掛時              | 是，與外掛捆綁      |
| [Skill](/zh-TW/skills) 或[代理](/zh-TW/sub-agents) frontmatter | 當 skill 或代理處於活動狀態時 | 是，在元件檔案中定義   |

在 Claude Code 中執行 [`/hooks`](/zh-TW/hooks#the-hooks-menu) 以瀏覽按事件分組的所有配置的 hooks。若要一次禁用所有 hooks，請在設定檔中設定 `"disableAllHooks": true`。

如果您在 Claude Code 執行時直接編輯設定檔，檔案監視程式通常會自動選取 hook 變更。

## 基於提示的 hooks

對於需要判斷而不是確定性規則的決策，使用 `type: "prompt"` hooks。Claude Code 不執行 shell 命令，而是將您的提示和 hook 的輸入資料傳送到 Claude 模型（預設為 Haiku）以做出決策。如果您需要更多功能，可以使用 `model` 欄位指定不同的模型。

模型的唯一工作是傳回 yes/no 決策作為 JSON：

* `"ok": true`：操作繼續
* `"ok": false`：操作被阻止。模型的 `"reason"` 被回饋給 Claude，以便它可以調整。

此範例使用 `Stop` hook 詢問模型是否所有請求的任務都已完成。如果模型傳回 `"ok": false`，Claude 會繼續工作並使用 `reason` 作為其下一個指令：

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if all tasks are complete. If not, respond with {\"ok\": false, \"reason\": \"what remains to be done\"}."
          }
        ]
      }
    ]
  }
}
```

有關完整的配置選項，請參閱參考中的[基於提示的 hooks](/zh-TW/hooks#prompt-based-hooks)。

## 基於代理的 hooks

當驗證需要檢查檔案或執行命令時，使用 `type: "agent"` hooks。與只進行單個 LLM 呼叫的提示 hooks 不同，代理 hooks 生成一個 subagent，可以讀取檔案、搜尋程式碼和使用其他工具在傳回決策之前驗證條件。

代理 hooks 使用與提示 hooks 相同的 `"ok"` / `"reason"` 回應格式，但預設超時時間更長（60 秒）且最多 50 個工具使用輪次。

此範例驗證在允許 Claude 停止之前測試通過：

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

當 hook 輸入資料本身足以做出決策時，使用提示 hooks。當您需要根據程式碼庫的實際狀態驗證某些內容時，使用代理 hooks。

有關完整的配置選項，請參閱參考中的[基於代理的 hooks](/zh-TW/hooks#agent-based-hooks)。

## HTTP hooks

使用 `type: "http"` hooks 將事件資料 POST 到 HTTP 端點，而不是執行 shell 命令。端點接收命令 hook 在 stdin 上接收的相同 JSON，並使用相同的 JSON 格式透過 HTTP 回應主體傳回結果。

HTTP hooks 在您希望 Web 伺服器、雲端函數或外部服務處理 hook 邏輯時很有用：例如，一個共享的審計服務，在整個團隊中記錄工具使用事件。

此範例將每個工具使用 POST 到本機記錄服務：

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/tool-use",
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

端點應使用與命令 hooks 相同的[輸出格式](/zh-TW/hooks#json-output)傳回 JSON 回應主體。要阻止工具呼叫，傳回 2xx 回應並包含適當的 `hookSpecificOutput` 欄位。HTTP 狀態代碼本身無法阻止操作。

標頭值支援使用 `$VAR_NAME` 或 `${VAR_NAME}` 語法的環境變數插值。只有在 `allowedEnvVars` 陣列中列出的變數才會被解析；所有其他 `$VAR` 參考保持為空。

有關完整的配置選項和回應處理，請參閱參考中的 [HTTP hooks](/zh-TW/hooks#http-hook-fields)。

## 限制和故障排除

### 限制

* 命令 hooks 只透過 stdout、stderr 和退出代碼通訊。它們無法直接觸發命令或工具呼叫。HTTP hooks 改為透過回應主體通訊。
* Hook 超時預設為 10 分鐘，可透過 `timeout` 欄位（以秒為單位）按 hook 配置。
* `PostToolUse` hooks 無法撤銷操作，因為工具已經執行。
* `PermissionRequest` hooks 在[非互動模式](/zh-TW/headless)（`-p`）中不觸發。對於自動化權限決策，使用 `PreToolUse` hooks。
* `Stop` hooks 在 Claude 完成回應時觸發，而不僅在任務完成時。它們在使用者中斷時不觸發。API 錯誤觸發 [StopFailure](/zh-TW/hooks#stopfailure) 代替。

### Hook 未觸發

Hook 已配置但從不執行。

* 執行 `/hooks` 並確認 hook 出現在正確的事件下
* 檢查匹配器模式是否與工具名稱完全相符（匹配器區分大小寫）
* 驗證您觸發的是正確的事件類型（例如，`PreToolUse` 在工具執行前觸發，`PostToolUse` 在之後觸發）
* 如果在非互動模式（`-p`）中使用 `PermissionRequest` hooks，改用 `PreToolUse`

### Hook 輸出中的錯誤

您在文字記錄中看到類似「PreToolUse hook error: ...」的訊息。

* 您的指令意外以非零代碼退出。透過管道傳輸範例 JSON 來手動測試它：
  ```bash  theme={null}
  echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./my-hook.sh
  echo $?  // 檢查退出代碼
  ```
* 如果您看到「command not found」，使用絕對路徑或 `$CLAUDE_PROJECT_DIR` 來參考指令
* 如果您看到「jq: command not found」，安裝 `jq` 或使用 Python/Node.js 進行 JSON 解析
* 如果指令根本沒有執行，使其可執行：`chmod +x ./my-hook.sh`

### `/hooks` 顯示未配置任何 hooks

您編輯了設定檔但 hooks 未出現在選單中。

* 檔案編輯通常會自動選取。如果在幾秒鐘後仍未出現，檔案監視程式可能已錯過變更：重新啟動您的工作階段以強制重新載入。
* 驗證您的 JSON 有效（不允許尾隨逗號和註解）
* 確認設定檔在正確的位置：`.claude/settings.json` 用於專案 hooks，`~/.claude/settings.json` 用於全域 hooks

### Stop hook 永遠執行

Claude 在無限迴圈中繼續工作而不是停止。

您的 Stop hook 指令需要檢查它是否已經觸發了延續。從 JSON 輸入解析 `stop_hook_active` 欄位，如果為 `true` 則提前退出：

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0  // 允許 Claude 停止
fi
// ... 您的 hook 邏輯的其餘部分
```

### JSON 驗證失敗

Claude Code 顯示 JSON 解析錯誤，即使您的 hook 指令輸出有效的 JSON。

當 Claude Code 執行 hook 時，它生成一個 shell，該 shell 來源您的設定檔（`~/.zshrc` 或 `~/.bashrc`）。如果您的設定檔包含無條件的 `echo` 陳述式，該輸出會被前置到您的 hook 的 JSON：

```text  theme={null}
Shell ready on arm64
{"decision": "block", "reason": "Not allowed"}
```

Claude Code 嘗試將其解析為 JSON 並失敗。要修復此問題，在您的 shell 設定檔中包裝 echo 陳述式，使其只在互動式 shell 中執行：

```bash  theme={null}
// 在 ~/.zshrc 或 ~/.bashrc 中
if [[ $- == *i* ]]; then
  echo "Shell ready"
fi
```

`$-` 變數包含 shell 旗標，`i` 表示互動式。Hooks 在非互動式 shell 中執行，因此 echo 被跳過。

### 除錯技術

使用 `Ctrl+O` 切換詳細模式以在文字記錄中查看 hook 輸出，或執行 `claude --debug` 以獲得完整的執行詳細資訊，包括哪些 hooks 相符及其退出代碼。

## 深入瞭解

* [Hooks 參考](/zh-TW/hooks)：完整的事件架構、JSON 輸出格式、非同步 hooks 和 MCP 工具 hooks
* [安全考量](/zh-TW/hooks#security-considerations)：在共享或生產環境中部署 hooks 之前進行檢查
* [Bash 命令驗證器範例](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py)：完整的參考實現
