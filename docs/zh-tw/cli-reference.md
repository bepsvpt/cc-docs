> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# CLI 參考

> Claude Code 命令列介面的完整參考，包括命令和旗標。

## CLI 命令

您可以使用這些命令來啟動工作階段、管道內容、繼續對話和管理更新：

| 命令                              | 描述                                                                                                                                               | 範例                                                 |
| :------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------- |
| `claude`                        | 啟動互動式工作階段                                                                                                                                        | `claude`                                           |
| `claude "query"`                | 使用初始提示啟動互動式工作階段                                                                                                                                  | `claude "explain this project"`                    |
| `claude -p "query"`             | 透過 SDK 查詢，然後退出                                                                                                                                   | `claude -p "explain this function"`                |
| `cat file \| claude -p "query"` | 處理管道內容                                                                                                                                           | `cat logs.txt \| claude -p "explain"`              |
| `claude -c`                     | 在目前目錄中繼續最近的對話                                                                                                                                    | `claude -c`                                        |
| `claude -c -p "query"`          | 透過 SDK 繼續                                                                                                                                        | `claude -c -p "Check for type errors"`             |
| `claude -r "<session>" "query"` | 按 ID 或名稱繼續工作階段                                                                                                                                   | `claude -r "auth-refactor" "Finish this PR"`       |
| `claude update`                 | 更新到最新版本                                                                                                                                          | `claude update`                                    |
| `claude auth login`             | 登入您的 Anthropic 帳戶。使用 `--email` 預先填入您的電子郵件地址，使用 `--sso` 強制進行 SSO 驗證                                                                               | `claude auth login --email user@example.com --sso` |
| `claude auth logout`            | 從您的 Anthropic 帳戶登出                                                                                                                               | `claude auth logout`                               |
| `claude auth status`            | 以 JSON 格式顯示驗證狀態。使用 `--text` 以人類可讀的格式輸出。如果已登入則以代碼 0 退出，如果未登入則以代碼 1 退出                                                                             | `claude auth status`                               |
| `claude agents`                 | 列出所有已設定的 [subagents](/zh-TW/sub-agents)，按來源分組                                                                                                    | `claude agents`                                    |
| `claude mcp`                    | 設定 Model Context Protocol (MCP) 伺服器                                                                                                              | 請參閱 [Claude Code MCP 文件](/zh-TW/mcp)。              |
| `claude remote-control`         | 啟動 [Remote Control 工作階段](/zh-TW/remote-control)，以在本機執行時從 Claude.ai 或 Claude 應用程式控制 Claude Code。請參閱 [Remote Control](/zh-TW/remote-control) 以了解旗標 | `claude remote-control`                            |

## CLI 旗標

使用這些命令列旗標自訂 Claude Code 的行為：

| 旗標                                     | 描述                                                                                                                                                               | 範例                                                                                                 |
| :------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| `--add-dir`                            | 新增額外的工作目錄供 Claude 存取（驗證每個路徑是否存在為目錄）                                                                                                                              | `claude --add-dir ../apps ../lib`                                                                  |
| `--agent`                              | 為目前工作階段指定代理程式（覆蓋 `agent` 設定）                                                                                                                                     | `claude --agent my-custom-agent`                                                                   |
| `--agents`                             | 透過 JSON 動態定義自訂 [subagents](/zh-TW/sub-agents)（請參閱下方的格式）                                                                                                          | `claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'` |
| `--allow-dangerously-skip-permissions` | 啟用權限略過作為選項，但不立即啟動它。允許與 `--permission-mode` 組合（謹慎使用）                                                                                                              | `claude --permission-mode plan --allow-dangerously-skip-permissions`                               |
| `--allowedTools`                       | 無需提示權限即可執行的工具。請參閱 [權限規則語法](/zh-TW/settings#permission-rule-syntax) 以了解模式匹配。若要限制可用的工具，請改用 `--tools`                                                               | `"Bash(git log *)" "Bash(git diff *)" "Read"`                                                      |
| `--append-system-prompt`               | 將自訂文字附加到預設系統提示的末尾                                                                                                                                                | `claude --append-system-prompt "Always use TypeScript"`                                            |
| `--append-system-prompt-file`          | 從檔案載入額外的系統提示文字並附加到預設提示                                                                                                                                           | `claude --append-system-prompt-file ./extra-rules.txt`                                             |
| `--betas`                              | 要包含在 API 請求中的 Beta 標頭（僅限 API 金鑰使用者）                                                                                                                              | `claude --betas interleaved-thinking`                                                              |
| `--chrome`                             | 啟用 [Chrome 瀏覽器整合](/zh-TW/chrome)，用於網頁自動化和測試                                                                                                                      | `claude --chrome`                                                                                  |
| `--continue`, `-c`                     | 在目前目錄中載入最近的對話                                                                                                                                                    | `claude --continue`                                                                                |
| `--dangerously-skip-permissions`       | 略過所有權限提示（謹慎使用）                                                                                                                                                   | `claude --dangerously-skip-permissions`                                                            |
| `--debug`                              | 啟用偵錯模式，可選擇類別篩選（例如，`"api,hooks"` 或 `"!statsig,!file"`）                                                                                                            | `claude --debug "api,mcp"`                                                                         |
| `--disable-slash-commands`             | 為此工作階段停用所有 skills 和命令                                                                                                                                            | `claude --disable-slash-commands`                                                                  |
| `--disallowedTools`                    | 從模型的上下文中移除且無法使用的工具                                                                                                                                               | `"Bash(git log *)" "Bash(git diff *)" "Edit"`                                                      |
| `--fallback-model`                     | 當預設模型過載時啟用自動回退到指定的模型（僅限列印模式）                                                                                                                                     | `claude -p --fallback-model sonnet "query"`                                                        |
| `--fork-session`                       | 繼續時，建立新的工作階段 ID 而不是重複使用原始 ID（與 `--resume` 或 `--continue` 搭配使用）                                                                                                   | `claude --resume abc123 --fork-session`                                                            |
| `--from-pr`                            | 繼續連結到特定 GitHub PR 的工作階段。接受 PR 編號或 URL。透過 `gh pr create` 建立時會自動連結工作階段                                                                                             | `claude --from-pr 123`                                                                             |
| `--ide`                                | 如果恰好有一個有效的 IDE 可用，則在啟動時自動連線到 IDE                                                                                                                                 | `claude --ide`                                                                                     |
| `--init`                               | 執行初始化 hooks 並啟動互動模式                                                                                                                                              | `claude --init`                                                                                    |
| `--init-only`                          | 執行初始化 hooks 並退出（無互動工作階段）                                                                                                                                         | `claude --init-only`                                                                               |
| `--include-partial-messages`           | 在輸出中包含部分串流事件（需要 `--print` 和 `--output-format=stream-json`）                                                                                                       | `claude -p --output-format stream-json --include-partial-messages "query"`                         |
| `--input-format`                       | 為列印模式指定輸入格式（選項：`text`、`stream-json`）                                                                                                                             | `claude -p --output-format json --input-format stream-json`                                        |
| `--json-schema`                        | 在代理程式完成其工作流程後取得符合 JSON Schema 的驗證 JSON 輸出（僅限列印模式，請參閱 [結構化輸出](https://platform.claude.com/docs/en/agent-sdk/structured-outputs)）                                  | `claude -p --json-schema '{"type":"object","properties":{...}}' "query"`                           |
| `--maintenance`                        | 執行維護 hooks 並退出                                                                                                                                                   | `claude --maintenance`                                                                             |
| `--max-budget-usd`                     | 在停止前在 API 呼叫上花費的最大美元金額（僅限列印模式）                                                                                                                                   | `claude -p --max-budget-usd 5.00 "query"`                                                          |
| `--max-turns`                          | 限制代理程式轉數（僅限列印模式）。達到限制時以錯誤退出。預設無限制                                                                                                                                | `claude -p --max-turns 3 "query"`                                                                  |
| `--mcp-config`                         | 從 JSON 檔案或字串載入 MCP 伺服器（以空格分隔）                                                                                                                                    | `claude --mcp-config ./mcp.json`                                                                   |
| `--model`                              | 使用最新模型的別名（`sonnet` 或 `opus`）或模型的完整名稱為目前工作階段設定模型                                                                                                                  | `claude --model claude-sonnet-4-6`                                                                 |
| `--no-chrome`                          | 為此工作階段停用 [Chrome 瀏覽器整合](/zh-TW/chrome)                                                                                                                           | `claude --no-chrome`                                                                               |
| `--no-session-persistence`             | 停用工作階段持久性，使工作階段不會儲存到磁碟且無法繼續（僅限列印模式）                                                                                                                              | `claude -p --no-session-persistence "query"`                                                       |
| `--output-format`                      | 為列印模式指定輸出格式（選項：`text`、`json`、`stream-json`）                                                                                                                      | `claude -p "query" --output-format json`                                                           |
| `--permission-mode`                    | 以指定的 [權限模式](/zh-TW/permissions#permission-modes) 開始                                                                                                              | `claude --permission-mode plan`                                                                    |
| `--permission-prompt-tool`             | 指定 MCP 工具以在非互動模式中處理權限提示                                                                                                                                          | `claude -p --permission-prompt-tool mcp_auth_tool "query"`                                         |
| `--plugin-dir`                         | 為此工作階段僅從目錄載入外掛程式（可重複）                                                                                                                                            | `claude --plugin-dir ./my-plugins`                                                                 |
| `--print`, `-p`                        | 列印回應而不進入互動模式（請參閱 [Agent SDK 文件](https://platform.claude.com/docs/en/agent-sdk/overview) 以了解程式設計用法詳細資訊）                                                           | `claude -p "query"`                                                                                |
| `--remote`                             | 在 claude.ai 上建立新的 [網頁工作階段](/zh-TW/claude-code-on-the-web)，並提供工作描述                                                                                                | `claude --remote "Fix the login bug"`                                                              |
| `--resume`, `-r`                       | 按 ID 或名稱繼續特定工作階段，或顯示互動式選擇器以選擇工作階段                                                                                                                                | `claude --resume auth-refactor`                                                                    |
| `--session-id`                         | 為對話使用特定的工作階段 ID（必須是有效的 UUID）                                                                                                                                     | `claude --session-id "550e8400-e29b-41d4-a716-446655440000"`                                       |
| `--setting-sources`                    | 要載入的設定來源的逗號分隔清單（`user`、`project`、`local`）                                                                                                                        | `claude --setting-sources user,project`                                                            |
| `--settings`                           | 設定 JSON 檔案的路徑或要載入其他設定的 JSON 字串                                                                                                                                   | `claude --settings ./settings.json`                                                                |
| `--strict-mcp-config`                  | 僅使用 `--mcp-config` 中的 MCP 伺服器，忽略所有其他 MCP 設定                                                                                                                      | `claude --strict-mcp-config --mcp-config ./mcp.json`                                               |
| `--system-prompt`                      | 用自訂文字取代整個系統提示                                                                                                                                                    | `claude --system-prompt "You are a Python expert"`                                                 |
| `--system-prompt-file`                 | 從檔案載入系統提示，取代預設提示                                                                                                                                                 | `claude --system-prompt-file ./custom-prompt.txt`                                                  |
| `--teleport`                           | 在本機終端中繼續 [網頁工作階段](/zh-TW/claude-code-on-the-web)                                                                                                                 | `claude --teleport`                                                                                |
| `--teammate-mode`                      | 設定 [agent team](/zh-TW/agent-teams) 隊友的顯示方式：`auto`（預設）、`in-process` 或 `tmux`。請參閱 [設定 agent teams](/zh-TW/agent-teams#set-up-agent-teams)                         | `claude --teammate-mode in-process`                                                                |
| `--tools`                              | 限制 Claude 可以使用的內建工具。使用 `""` 停用全部，`"default"` 表示全部，或工具名稱如 `"Bash,Edit,Read"`                                                                                      | `claude --tools "Bash,Edit,Read"`                                                                  |
| `--verbose`                            | 啟用詳細記錄，顯示完整的逐轉輸出                                                                                                                                                 | `claude --verbose`                                                                                 |
| `--version`, `-v`                      | 輸出版本號                                                                                                                                                            | `claude -v`                                                                                        |
| `--worktree`, `-w`                     | 在隔離的 [git worktree](/zh-TW/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) 中啟動 Claude，位於 `<repo>/.claude/worktrees/<name>`。如果未指定名稱，則會自動產生 | `claude -w feature-auth`                                                                           |

<Tip>
  `--output-format json` 旗標對於指令碼和自動化特別有用，允許您以程式設計方式解析 Claude 的回應。
</Tip>

### Agents 旗標格式

`--agents` 旗標接受定義一個或多個自訂 subagents 的 JSON 物件。每個 subagent 需要一個唯一的名稱（作為金鑰）和一個具有以下欄位的定義物件：

| 欄位                | 必需 | 描述                                                                                                                                                     |
| :---------------- | :- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `description`     | 是  | 何時應叫用 subagent 的自然語言描述                                                                                                                                 |
| `prompt`          | 是  | 指導 subagent 行為的系統提示                                                                                                                                    |
| `tools`           | 否  | subagent 可以使用的特定工具陣列，例如 `["Read", "Edit", "Bash"]`。如果省略，則繼承所有工具。支援 [`Agent(agent_type)`](/zh-TW/sub-agents#restrict-which-subagents-can-be-spawned) 語法 |
| `disallowedTools` | 否  | 要為此 subagent 明確拒絕的工具名稱陣列                                                                                                                               |
| `model`           | 否  | 要使用的模型別名：`sonnet`、`opus`、`haiku` 或 `inherit`。如果省略，預設為 `inherit`                                                                                        |
| `skills`          | 否  | 要預先載入到 subagent 上下文中的 [skill](/zh-TW/skills) 名稱陣列                                                                                                      |
| `mcpServers`      | 否  | 此 subagent 的 [MCP servers](/zh-TW/mcp) 陣列。每個項目是伺服器名稱字串或 `{name: config}` 物件                                                                            |
| `maxTurns`        | 否  | subagent 停止前的最大代理程式轉數                                                                                                                                  |

範例：

```bash  theme={null}
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

如需有關建立和使用 subagents 的更多詳細資訊，請參閱 [subagents 文件](/zh-TW/sub-agents)。

### 系統提示旗標

Claude Code 提供四個旗標用於自訂系統提示。所有四個都在互動和非互動模式中運作。

| 旗標                            | 行為              | 使用案例                         |
| :---------------------------- | :-------------- | :--------------------------- |
| `--system-prompt`             | **取代**整個預設提示    | 完全控制 Claude 的行為和指示           |
| `--system-prompt-file`        | **取代**為檔案內容     | 從檔案載入提示以實現可重現性和版本控制          |
| `--append-system-prompt`      | **附加**到預設提示     | 新增特定指示，同時保持預設 Claude Code 行為 |
| `--append-system-prompt-file` | **附加**檔案內容到預設提示 | 從檔案載入額外指示，同時保持預設值            |

**何時使用每一個：**

* **`--system-prompt`**：當您需要完全控制 Claude 的系統提示時使用。這會移除所有預設 Claude Code 指示，為您提供一個空白的狀態。
  ```bash  theme={null}
  claude --system-prompt "You are a Python expert who only writes type-annotated code"
  ```

* **`--system-prompt-file`**：當您想從檔案載入自訂提示時使用，對於團隊一致性或版本控制的提示範本很有用。
  ```bash  theme={null}
  claude --system-prompt-file ./prompts/code-review.txt
  ```

* **`--append-system-prompt`**：當您想新增特定指示，同時保持 Claude Code 的預設功能完整時使用。這是大多數使用案例的最安全選項。
  ```bash  theme={null}
  claude --append-system-prompt "Always use TypeScript and include JSDoc comments"
  ```

* **`--append-system-prompt-file`**：當您想從檔案附加指示，同時保持 Claude Code 的預設值時使用。對於版本控制的新增很有用。
  ```bash  theme={null}
  claude --append-system-prompt-file ./prompts/style-rules.txt
  ```

`--system-prompt` 和 `--system-prompt-file` 互斥。附加旗標可與任一取代旗標一起使用。

對於大多數使用案例，建議使用 `--append-system-prompt` 或 `--append-system-prompt-file`，因為它們保留 Claude Code 的內建功能，同時新增您的自訂需求。僅當您需要完全控制系統提示時，才使用 `--system-prompt` 或 `--system-prompt-file`。

## 另請參閱

* [Chrome 擴充功能](/zh-TW/chrome) - 瀏覽器自動化和網頁測試
* [互動模式](/zh-TW/interactive-mode) - 快捷鍵、輸入模式和互動功能
* [快速入門指南](/zh-TW/quickstart) - Claude Code 入門
* [常見工作流程](/zh-TW/common-workflows) - 進階工作流程和模式
* [設定](/zh-TW/settings) - 設定選項
* [Agent SDK 文件](https://platform.claude.com/docs/en/agent-sdk/overview) - 程式設計用法和整合
