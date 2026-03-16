> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 建立自訂 subagents

> 在 Claude Code 中建立並使用專門的 AI subagents，用於特定任務的工作流程和改進的上下文管理。

Subagents 是專門的 AI 助手，用於處理特定類型的任務。每個 subagent 在自己的 context window 中執行，具有自訂系統提示、特定工具存取和獨立權限。當 Claude 遇到與 subagent 描述相符的任務時，它會委派給該 subagent，該 subagent 獨立工作並返回結果。

<Note>
  如果您需要多個代理並行工作並相互通訊，請改為參閱 [agent teams](/zh-TW/agent-teams)。Subagents 在單一工作階段內工作；agent teams 跨越多個獨立工作階段進行協調。
</Note>

Subagents 可幫助您：

* **保留上下文**，將探索和實現保持在主要對話之外
* **強制執行約束**，限制 subagent 可以使用的工具
* **跨專案重複使用配置**，使用使用者層級的 subagents
* **專門化行為**，針對特定領域使用專注的系統提示
* **控制成本**，將任務路由到更快、更便宜的模型（如 Haiku）

Claude 使用每個 subagent 的描述來決定何時委派任務。建立 subagent 時，請寫清楚的描述，以便 Claude 知道何時使用它。

Claude Code 包含多個內建 subagents，例如 **Explore**、**Plan** 和 **general-purpose**。您也可以建立自訂 subagents 來處理特定任務。本頁涵蓋 [內建 subagents](#built-in-subagents)、[如何建立您自己的](#quickstart-create-your-first-subagent)、[完整配置選項](#configure-subagents)、[使用 subagents 的模式](#work-with-subagents) 和 [範例 subagents](#example-subagents)。

## 內建 subagents

Claude Code 包含內建 subagents，Claude 會在適當時自動使用。每個都繼承父對話的權限，並有額外的工具限制。

<Tabs>
  <Tab title="Explore">
    一個快速、唯讀的代理，針對搜尋和分析程式碼庫進行最佳化。

    * **模型**：Haiku（快速、低延遲）
    * **工具**：唯讀工具（拒絕存取 Write 和 Edit 工具）
    * **目的**：檔案發現、程式碼搜尋、程式碼庫探索

    當 Claude 需要搜尋或理解程式碼庫而不進行更改時，它會委派給 Explore。這可以將探索結果保持在主要對話上下文之外。

    叫用 Explore 時，Claude 會指定詳盡程度：**quick** 用於目標查詢、**medium** 用於平衡探索，或 **very thorough** 用於全面分析。
  </Tab>

  <Tab title="Plan">
    在 [plan mode](/zh-TW/common-workflows#use-plan-mode-for-safe-code-analysis) 期間用於在呈現計畫之前收集上下文的研究代理。

    * **模型**：繼承自主對話
    * **工具**：唯讀工具（拒絕存取 Write 和 Edit 工具）
    * **目的**：用於規劃的程式碼庫研究

    當您處於 plan mode 且 Claude 需要理解您的程式碼庫時，它會將研究委派給 Plan subagent。這可以防止無限嵌套（subagents 無法產生其他 subagents），同時仍然收集必要的上下文。
  </Tab>

  <Tab title="General-purpose">
    一個能夠處理複雜、多步驟任務的代理，需要探索和行動。

    * **模型**：繼承自主對話
    * **工具**：所有工具
    * **目的**：複雜研究、多步驟操作、程式碼修改

    當任務需要探索和修改、複雜推理來解釋結果，或多個相依步驟時，Claude 會委派給 general-purpose。
  </Tab>

  <Tab title="Other">
    Claude Code 包含用於特定任務的其他輔助代理。這些通常會自動叫用，因此您不需要直接使用它們。

    | 代理                | 模型     | Claude 何時使用它                 |
    | :---------------- | :----- | :--------------------------- |
    | Bash              | 繼承     | 在單獨的上下文中執行終端命令               |
    | statusline-setup  | Sonnet | 當您執行 `/statusline` 來配置您的狀態行時 |
    | Claude Code Guide | Haiku  | 當您詢問有關 Claude Code 功能的問題時    |
  </Tab>
</Tabs>

除了這些內建 subagents 之外，您可以建立自己的 subagents，具有自訂提示、工具限制、權限模式、hooks 和 skills。以下各節展示如何開始和自訂 subagents。

## 快速入門：建立您的第一個 subagent

Subagents 在具有 YAML frontmatter 的 Markdown 檔案中定義。您可以 [手動建立它們](#write-subagent-files) 或使用 `/agents` 命令。

本逐步解說指導您使用 `/agent` 命令建立使用者層級的 subagent。該 subagent 審查程式碼並為程式碼庫建議改進。

<Steps>
  <Step title="開啟 subagents 介面">
    在 Claude Code 中，執行：

    ```text  theme={null}
    /agents
    ```
  </Step>

  <Step title="建立新的使用者層級代理">
    選擇 **Create new agent**，然後選擇 **User-level**。這會將 subagent 儲存到 `~/.claude/agents/`，以便在所有專案中使用。
  </Step>

  <Step title="使用 Claude 產生">
    選擇 **Generate with Claude**。出現提示時，描述 subagent：

    ```text  theme={null}
    A code improvement agent that scans files and suggests improvements
    for readability, performance, and best practices. It should explain
    each issue, show the current code, and provide an improved version.
    ```

    Claude 產生系統提示和配置。按 `e` 在編輯器中開啟它，如果您想自訂它。
  </Step>

  <Step title="選擇工具">
    對於唯讀審查者，取消選擇除 **Read-only tools** 之外的所有內容。如果您保持所有工具選中，subagent 會繼承主對話可用的所有工具。
  </Step>

  <Step title="選擇模型">
    選擇 subagent 使用的模型。對於此範例代理，選擇 **Sonnet**，它在分析程式碼模式的能力和速度之間取得平衡。
  </Step>

  <Step title="選擇顏色">
    為 subagent 選擇背景顏色。這可幫助您識別在 UI 中執行的 subagent。
  </Step>

  <Step title="儲存並試用">
    儲存 subagent。它立即可用（無需重新啟動）。試用它：

    ```text  theme={null}
    Use the code-improver agent to suggest improvements in this project
    ```

    Claude 委派給您的新 subagent，它掃描程式碼庫並返回改進建議。
  </Step>
</Steps>

您現在有一個 subagent，可以在機器上的任何專案中使用，以分析程式碼庫並建議改進。

您也可以手動建立 subagents 作為 Markdown 檔案、透過 CLI 旗標定義它們，或透過 plugins 分發它們。以下各節涵蓋所有配置選項。

## 配置 subagents

### 使用 /agents 命令

`/agents` 命令提供用於管理 subagents 的互動式介面。執行 `/agents` 以：

* 檢視所有可用的 subagents（內建、使用者、專案和 plugin）
* 使用引導式設定或 Claude 產生建立新的 subagents
* 編輯現有 subagent 配置和工具存取
* 刪除自訂 subagents
* 查看重複項存在時哪些 subagents 處於活動狀態

這是建立和管理 subagents 的建議方式。對於手動建立或自動化，您也可以直接新增 subagent 檔案。

若要從命令行列出所有已配置的 subagents 而不啟動互動式工作階段，請執行 `claude agents`。這會按來源分組顯示代理，並指示哪些被更高優先級定義覆蓋。

### 選擇 subagent 範圍

Subagents 是具有 YAML frontmatter 的 Markdown 檔案。根據範圍將它們儲存在不同位置。當多個 subagents 共享相同名稱時，更高優先級位置獲勝。

| 位置                    | 範圍            | 優先級   | 如何建立                            |
| :-------------------- | :------------ | :---- | :------------------------------ |
| `--agents` CLI 旗標     | 目前工作階段        | 1（最高） | 啟動 Claude Code 時傳遞 JSON         |
| `.claude/agents/`     | 目前專案          | 2     | 互動式或手動                          |
| `~/.claude/agents/`   | 您的所有專案        | 3     | 互動式或手動                          |
| Plugin 的 `agents/` 目錄 | 啟用 plugin 的位置 | 4（最低） | 使用 [plugins](/zh-TW/plugins) 安裝 |

**專案 subagents**（`.claude/agents/`）非常適合特定於程式碼庫的 subagents。將它們簽入版本控制，以便您的團隊可以協作使用和改進它們。

**使用者 subagents**（`~/.claude/agents/`）是在所有專案中可用的個人 subagents。

**CLI 定義的 subagents** 在啟動 Claude Code 時作為 JSON 傳遞。它們僅存在於該工作階段，不會儲存到磁碟，使其適用於快速測試或自動化指令碼：

```bash  theme={null}
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

`--agents` 旗標接受 JSON，具有與檔案型 subagents 相同的 [frontmatter](#supported-frontmatter-fields) 欄位：`description`、`prompt`、`tools`、`disallowedTools`、`model`、`permissionMode`、`mcpServers`、`hooks`、`maxTurns`、`skills` 和 `memory`。使用 `prompt` 作為系統提示，等同於檔案型 subagents 中的 markdown 主體。請參閱 [CLI 參考](/zh-TW/cli-reference#agents-flag-format) 以取得完整的 JSON 格式。

**Plugin subagents** 來自您已安裝的 [plugins](/zh-TW/plugins)。它們與您的自訂 subagents 一起出現在 `/agents` 中。請參閱 [plugin 元件參考](/zh-TW/plugins-reference#agents) 以取得建立 plugin subagents 的詳細資訊。

### 編寫 subagent 檔案

Subagent 檔案使用 YAML frontmatter 進行配置，後面跟著 Markdown 中的系統提示：

<Note>
  Subagents 在工作階段開始時載入。如果您透過手動新增檔案來建立 subagent，請重新啟動您的工作階段或使用 `/agents` 立即載入它。
</Note>

```markdown  theme={null}
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

Frontmatter 定義 subagent 的中繼資料和配置。主體成為指導 subagent 行為的系統提示。Subagents 僅接收此系統提示（加上基本環境詳細資訊，如工作目錄），而不是完整的 Claude Code 系統提示。

#### 支援的 frontmatter 欄位

以下欄位可用於 YAML frontmatter。只有 `name` 和 `description` 是必需的。

| 欄位                | 必需 | 描述                                                                                                                                                                            |
| :---------------- | :- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`            | 是  | 使用小寫字母和連字號的唯一識別碼                                                                                                                                                              |
| `description`     | 是  | Claude 何時應委派給此 subagent                                                                                                                                                       |
| `tools`           | 否  | subagent 可以使用的 [工具](#available-tools)。如果省略，繼承所有工具                                                                                                                             |
| `disallowedTools` | 否  | 要拒絕的工具，從繼承或指定的清單中移除                                                                                                                                                           |
| `model`           | 否  | 要使用的 [模型](#choose-a-model)：`sonnet`、`opus`、`haiku` 或 `inherit`。預設為 `inherit`                                                                                                  |
| `permissionMode`  | 否  | [權限模式](#permission-modes)：`default`、`acceptEdits`、`dontAsk`、`bypassPermissions` 或 `plan`                                                                                      |
| `maxTurns`        | 否  | subagent 停止前的最大代理轉數                                                                                                                                                           |
| `skills`          | 否  | 在啟動時載入到 subagent 上下文中的 [Skills](/zh-TW/skills)。注入完整的 skill 內容，而不僅僅是可供叫用。Subagents 不繼承父對話中的 skills                                                                             |
| `mcpServers`      | 否  | 此 subagent 可用的 [MCP servers](/zh-TW/mcp)。每個項目要麼是參考已配置伺服器的伺服器名稱（例如 `"slack"`），要麼是內聯定義，其中伺服器名稱為鍵，完整的 [MCP 伺服器配置](/zh-TW/mcp#configure-mcp-servers) 為值                           |
| `hooks`           | 否  | 限定於此 subagent 的 [生命週期 hooks](#define-hooks-for-subagents)                                                                                                                     |
| `memory`          | 否  | [持久記憶體範圍](#enable-persistent-memory)：`user`、`project` 或 `local`。啟用跨工作階段學習                                                                                                     |
| `background`      | 否  | 設定為 `true` 以始終將此 subagent 作為 [背景任務](#run-subagents-in-foreground-or-background) 執行。預設：`false`                                                                                 |
| `isolation`       | 否  | 設定為 `worktree` 以在臨時 [git worktree](/zh-TW/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) 中執行 subagent，為其提供儲存庫的隔離副本。如果 subagent 不進行任何更改，worktree 會自動清理 |

### 選擇模型

`model` 欄位控制 subagent 使用的 [AI 模型](/zh-TW/model-config)：

* **模型別名**：使用可用的別名之一：`sonnet`、`opus` 或 `haiku`
* **inherit**：使用與主對話相同的模型
* **省略**：如果未指定，預設為 `inherit`（使用與主對話相同的模型）

### 控制 subagent 功能

您可以透過工具存取、權限模式和條件規則來控制 subagents 可以執行的操作。

#### 可用工具

Subagents 可以使用 Claude Code 的任何 [內部工具](/zh-TW/settings#tools-available-to-claude)。預設情況下，subagents 繼承主對話的所有工具，包括 MCP 工具。

若要限制工具，請使用 `tools` 欄位（允許清單）或 `disallowedTools` 欄位（拒絕清單）：

```yaml  theme={null}
---
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
---
```

#### 限制可以產生的 subagents

當代理以 `claude --agent` 作為主執行緒執行時，它可以使用 Agent 工具產生 subagents。若要限制它可以產生的 subagent 類型，請在 `tools` 欄位中使用 `Agent(agent_type)` 語法。

<Note>在版本 2.1.63 中，Task 工具已重新命名為 Agent。設定和代理定義中的現有 `Task(...)` 參考仍可作為別名使用。</Note>

```yaml  theme={null}
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---
```

這是一個允許清單：只有 `worker` 和 `researcher` subagents 可以產生。如果代理嘗試產生任何其他類型，請求會失敗，代理在其提示中只看到允許的類型。若要在允許所有其他類型的同時阻止特定代理，請改用 [`permissions.deny`](#disable-specific-subagents)。

若要允許產生任何 subagent 而不受限制，請使用不帶括號的 `Agent`：

```yaml  theme={null}
tools: Agent, Read, Bash
```

如果 `Agent` 完全從 `tools` 清單中省略，代理無法產生任何 subagents。此限制僅適用於以 `claude --agent` 作為主執行緒執行的代理。Subagents 無法產生其他 subagents，因此 `Agent(agent_type)` 在 subagent 定義中無效。

#### 權限模式

`permissionMode` 欄位控制 subagent 如何處理權限提示。Subagents 繼承主對話的權限上下文，但可以覆蓋模式。

| 模式                  | 行為                    |
| :------------------ | :-------------------- |
| `default`           | 標準權限檢查，帶提示            |
| `acceptEdits`       | 自動接受檔案編輯              |
| `dontAsk`           | 自動拒絕權限提示（明確允許的工具仍然有效） |
| `bypassPermissions` | 跳過所有權限檢查              |
| `plan`              | Plan mode（唯讀探索）       |

<Warning>
  謹慎使用 `bypassPermissions`。它跳過所有權限檢查，允許 subagent 執行任何操作而無需批准。
</Warning>

如果父級使用 `bypassPermissions`，這優先級最高，無法覆蓋。

#### 將 skills 預載入 subagents

使用 `skills` 欄位在啟動時將 skill 內容注入到 subagent 的上下文中。這為 subagent 提供領域知識，而無需在執行期間發現和載入 skills。

```yaml  theme={null}
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---

Implement API endpoints. Follow the conventions and patterns from the preloaded skills.
```

每個 skill 的完整內容被注入到 subagent 的上下文中，而不僅僅是可供叫用。Subagents 不繼承父對話中的 skills；您必須明確列出它們。

<Note>
  這與 [在 subagent 中執行 skill](/zh-TW/skills#run-skills-in-a-subagent) 相反。使用 subagent 中的 `skills`，subagent 控制系統提示並載入 skill 內容。使用 skill 中的 `context: fork`，skill 內容被注入到您指定的代理中。兩者都使用相同的基礎系統。
</Note>

#### 啟用持久記憶體

`memory` 欄位為 subagent 提供一個跨對話存活的持久目錄。Subagent 使用此目錄隨著時間推移建立知識，例如程式碼庫模式、除錯見解和架構決策。

```yaml  theme={null}
---
name: code-reviewer
description: Reviews code for quality and best practices
memory: user
---

You are a code reviewer. As you review code, update your agent memory with
patterns, conventions, and recurring issues you discover.
```

根據記憶體應該應用的廣泛程度選擇範圍：

| 範圍        | 位置                                            | 使用時機                          |
| :-------- | :-------------------------------------------- | :---------------------------- |
| `user`    | `~/.claude/agent-memory/<name-of-agent>/`     | subagent 應該記住跨所有專案的學習         |
| `project` | `.claude/agent-memory/<name-of-agent>/`       | subagent 的知識是特定於專案的並可透過版本控制共享 |
| `local`   | `.claude/agent-memory-local/<name-of-agent>/` | subagent 的知識是特定於專案的但不應簽入版本控制  |

啟用記憶體時：

* subagent 的系統提示包括讀取和寫入記憶體目錄的說明。
* subagent 的系統提示還包括記憶體目錄中 `MEMORY.md` 的前 200 行，以及如果 `MEMORY.md` 超過 200 行則策劃 `MEMORY.md` 的說明。
* Read、Write 和 Edit 工具會自動啟用，以便 subagent 可以管理其記憶體檔案。

##### 持久記憶體提示

* `user` 是建議的預設範圍。當 subagent 的知識僅與特定程式碼庫相關時，使用 `project` 或 `local`。
* 要求 subagent 在開始工作前查詢其記憶體："Review this PR, and check your memory for patterns you've seen before."
* 要求 subagent 在完成任務後更新其記憶體："Now that you're done, save what you learned to your memory." 隨著時間推移，這會建立一個知識庫，使 subagent 更有效。
* 直接在 subagent 的 markdown 檔案中包含記憶體說明，以便它主動維護自己的知識庫：

  ```markdown  theme={null}
  Update your agent memory as you discover codepaths, patterns, library
  locations, and key architectural decisions. This builds up institutional
  knowledge across conversations. Write concise notes about what you found
  and where.
  ```

#### 使用 hooks 的條件規則

為了更動態地控制工具使用，請使用 `PreToolUse` hooks 在執行前驗證操作。當您需要允許工具的某些操作同時阻止其他操作時，這很有用。

此範例建立一個只允許唯讀資料庫查詢的 subagent。`PreToolUse` hook 在每個 Bash 命令執行前執行 `command` 中指定的指令碼：

```yaml  theme={null}
---
name: db-reader
description: Execute read-only database queries
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---
```

Claude Code [透過 stdin 將 hook 輸入作為 JSON 傳遞](/zh-TW/hooks#pretooluse-input) 給 hook 命令。驗證指令碼讀取此 JSON，提取 Bash 命令，並 [以代碼 2 退出](/zh-TW/hooks#exit-code-2-behavior-per-event) 以阻止寫入操作：

```bash  theme={null}
#!/bin/bash
# ./scripts/validate-readonly-query.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block SQL write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b' > /dev/null; then
  echo "Blocked: Only SELECT queries are allowed" >&2
  exit 2
fi

exit 0
```

請參閱 [Hook 輸入](/zh-TW/hooks#pretooluse-input) 以取得完整的輸入架構，以及 [退出代碼](/zh-TW/hooks#exit-code-output) 以了解退出代碼如何影響行為。

#### 禁用特定 subagents

您可以透過將 subagents 新增到 [設定](/zh-TW/settings#permission-settings) 中的 `deny` 陣列來防止 Claude 使用特定 subagents。使用格式 `Agent(subagent-name)`，其中 `subagent-name` 與 subagent 的 name 欄位相符。

```json  theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}
```

這適用於內建和自訂 subagents。您也可以使用 `--disallowedTools` CLI 旗標：

```bash  theme={null}
claude --disallowedTools "Agent(Explore)"
```

請參閱 [權限文件](/zh-TW/permissions#tool-specific-permission-rules) 以取得有關權限規則的更多詳細資訊。

### 為 subagents 定義 hooks

Subagents 可以定義在 subagent 生命週期期間執行的 [hooks](/zh-TW/hooks)。有兩種方式來配置 hooks：

1. **在 subagent 的 frontmatter 中**：定義僅在該 subagent 活動時執行的 hooks
2. **在 `settings.json` 中**：定義在 subagents 啟動或停止時在主工作階段中執行的 hooks

#### Subagent frontmatter 中的 Hooks

直接在 subagent 的 markdown 檔案中定義 hooks。這些 hooks 僅在該特定 subagent 活動時執行，並在完成時清理。

支援所有 [hook 事件](/zh-TW/hooks#hook-events)。subagents 最常見的事件是：

| 事件            | 匹配器輸入 | 何時觸發                                   |
| :------------ | :---- | :------------------------------------- |
| `PreToolUse`  | 工具名稱  | 在 subagent 使用工具之前                      |
| `PostToolUse` | 工具名稱  | 在 subagent 使用工具之後                      |
| `Stop`        | （無）   | 當 subagent 完成時（在執行時轉換為 `SubagentStop`） |

此範例使用 `PreToolUse` hook 驗證 Bash 命令，並在檔案編輯後使用 `PostToolUse` 執行 linter：

```yaml  theme={null}
---
name: code-reviewer
description: Review code changes with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh $TOOL_INPUT"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

Frontmatter 中的 `Stop` hooks 會自動轉換為 `SubagentStop` 事件。

#### 用於 subagent 事件的專案層級 hooks

在 `settings.json` 中配置 hooks，以回應主工作階段中的 subagent 生命週期事件。

| 事件              | 匹配器輸入  | 何時觸發             |
| :-------------- | :----- | :--------------- |
| `SubagentStart` | 代理類型名稱 | 當 subagent 開始執行時 |
| `SubagentStop`  | 代理類型名稱 | 當 subagent 完成時   |

兩個事件都支援匹配器以按名稱針對特定代理類型。此範例僅在 `db-agent` subagent 啟動時執行設定指令碼，並在任何 subagent 停止時執行清理指令碼：

```json  theme={null}
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/setup-db-connection.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/cleanup-db-connection.sh" }
        ]
      }
    ]
  }
}
```

請參閱 [Hooks](/zh-TW/hooks) 以取得完整的 hook 配置格式。

## 使用 subagents

### 理解自動委派

Claude 根據您請求中的任務描述、subagent 配置中的 `description` 欄位和目前上下文自動委派任務。為了鼓勵主動委派，在 subagent 的 description 欄位中包含"use proactively"之類的短語。

您也可以明確要求特定 subagent：

```text  theme={null}
Use the test-runner subagent to fix failing tests
Have the code-reviewer subagent look at my recent changes
```

### 在前景或背景中執行 subagents

Subagents 可以在前景（阻止）或背景（並行）中執行：

* **前景 subagents** 阻止主對話直到完成。權限提示和澄清問題（如 [`AskUserQuestion`](/zh-TW/settings#tools-available-to-claude)）會傳遞給您。
* **背景 subagents** 在您繼續工作時並行執行。啟動前，Claude Code 會提示輸入 subagent 需要的任何工具權限，確保它具有必要的批准。執行後，subagent 繼承這些權限並自動拒絕未預先批准的任何內容。如果背景 subagent 需要提出澄清問題，該工具呼叫會失敗，但 subagent 會繼續。

如果背景 subagent 因缺少權限而失敗，您可以 [恢復它](#resume-subagents) 在前景中以使用互動式提示重試。

Claude 根據任務決定是否在前景或背景中執行 subagents。您也可以：

* 要求 Claude "run this in the background"
* 按 **Ctrl+B** 將執行中的任務放在背景中

若要禁用所有背景任務功能，請將 `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` 環境變數設定為 `1`。請參閱 [環境變數](/zh-TW/settings#environment-variables)。

### 常見模式

#### 隔離高容量操作

subagents 最有效的用途之一是隔離產生大量輸出的操作。執行測試、獲取文件或處理日誌檔案可能會消耗大量上下文。透過將這些委派給 subagent，詳細輸出保留在 subagent 的上下文中，而只有相關摘要返回到主對話。

```text  theme={null}
Use a subagent to run the test suite and report only the failing tests with their error messages
```

#### 執行並行研究

對於獨立調查，產生多個 subagents 以同時工作：

```text  theme={null}
Research the authentication, database, and API modules in parallel using separate subagents
```

每個 subagent 獨立探索其區域，然後 Claude 綜合發現。當研究路徑彼此不相依時，這效果最佳。

<Warning>
  當 subagents 完成時，其結果返回到主對話。執行許多 subagents，每個都返回詳細結果，可能會消耗大量上下文。
</Warning>

對於需要持續並行性或超過上下文視窗的任務，[agent teams](/zh-TW/agent-teams) 為每個工作者提供自己的獨立上下文。

#### 鏈接 subagents

對於多步驟工作流程，要求 Claude 按順序使用 subagents。每個 subagent 完成其任務並將結果返回給 Claude，然後 Claude 將相關上下文傳遞給下一個 subagent。

```text  theme={null}
Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them
```

### 在 subagents 和主對話之間選擇

在以下情況下使用**主對話**：

* 任務需要頻繁的來回或反覆改進
* 多個階段共享重要上下文（規劃 → 實現 → 測試）
* 您進行快速、有針對性的更改
* 延遲很重要。Subagents 從頭開始，可能需要時間收集上下文

在以下情況下使用 **subagents**：

* 任務產生您不需要在主上下文中的詳細輸出
* 您想強制執行特定的工具限制或權限
* 工作是自包含的，可以返回摘要

當您想要可重複使用的提示或在主對話上下文中執行的工作流程而不是隔離的 subagent 上下文時，請改為考慮 [Skills](/zh-TW/skills)。

對於關於對話中已有內容的快速問題，請使用 [`/btw`](/zh-TW/interactive-mode#side-questions-with-btw) 而不是 subagent。它看到您的完整上下文但沒有工具存取，答案被丟棄而不是新增到歷史記錄。

<Note>
  Subagents 無法產生其他 subagents。如果您的工作流程需要嵌套委派，請使用 [Skills](/zh-TW/skills) 或從主對話 [鏈接 subagents](#chain-subagents)。
</Note>

### 管理 subagent 上下文

#### 恢復 subagents

每個 subagent 叫用都會建立一個具有新鮮上下文的新實例。若要繼續現有 subagent 的工作而不是重新開始，請要求 Claude 恢復它。

恢復的 subagents 保留其完整的對話歷史記錄，包括所有先前的工具呼叫、結果和推理。Subagent 從停止的地方精確繼續，而不是從頭開始。

當 subagent 完成時，Claude 接收其代理 ID。若要恢復 subagent，請要求 Claude 繼續先前的工作：

```text  theme={null}
Use the code-reviewer subagent to review the authentication module
[Agent completes]

Continue that code review and now analyze the authorization logic
[Claude resumes the subagent with full context from previous conversation]
```

您也可以要求 Claude 提供代理 ID（如果您想明確參考它），或在 `~/.claude/projects/{project}/{sessionId}/subagents/` 的文字檔案中找到 ID。每個文字檔案儲存為 `agent-{agentId}.jsonl`。

Subagent 文字檔案獨立於主對話持續存在：

* **主對話壓縮**：當主對話壓縮時，subagent 文字檔案不受影響。它們儲存在單獨的檔案中。
* **工作階段持續性**：Subagent 文字檔案在其工作階段內持續存在。您可以透過恢復相同工作階段在重新啟動 Claude Code 後 [恢復 subagent](#resume-subagents)。
* **自動清理**：文字檔案根據 `cleanupPeriodDays` 設定（預設：30 天）進行清理。

#### 自動壓縮

Subagents 支援使用與主對話相同的邏輯進行自動壓縮。預設情況下，自動壓縮在大約 95% 容量時觸發。若要更早觸發壓縮，請將 `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` 設定為較低的百分比（例如 `50`）。請參閱 [環境變數](/zh-TW/settings#environment-variables) 以取得詳細資訊。

壓縮事件記錄在 subagent 文字檔案中：

```json  theme={null}
{
  "type": "system",
  "subtype": "compact_boundary",
  "compactMetadata": {
    "trigger": "auto",
    "preTokens": 167189
  }
}
```

`preTokens` 值顯示壓縮發生前使用了多少個 tokens。

## 範例 subagents

這些範例展示了建立 subagents 的有效模式。將它們用作起點，或使用 Claude 產生自訂版本。

<Tip>
  **最佳實踐：**

  * **設計專注的 subagents：** 每個 subagent 應該在一個特定任務上表現出色
  * **編寫詳細的描述：** Claude 使用描述來決定何時委派
  * **限制工具存取：** 僅授予必要的權限以確保安全和專注
  * **簽入版本控制：** 與您的團隊共享專案 subagents
</Tip>

### 程式碼審查者

一個唯讀 subagent，審查程式碼而不修改它。此範例展示如何設計一個具有有限工具存取（無 Edit 或 Write）和詳細提示的專注 subagent，該提示明確指定要查找的內容以及如何格式化輸出。

```markdown  theme={null}
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

### 除錯器

一個可以分析和修復問題的 subagent。與程式碼審查者不同，這個包括 Edit，因為修復錯誤需要修改程式碼。提示提供了從診斷到驗證的清晰工作流程。

```markdown  theme={null}
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.
```

### 資料科學家

用於資料分析工作的特定領域 subagent。此範例展示如何為典型編碼任務之外的專門工作流程建立 subagents。它明確設定 `model: sonnet` 以進行更有能力的分析。

```markdown  theme={null}
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.
```

### 資料庫查詢驗證器

一個允許 Bash 存取但驗證命令以僅允許唯讀 SQL 查詢的 subagent。此範例展示如何使用 `PreToolUse` hooks 進行條件驗證，當您需要比 `tools` 欄位更精細的控制時。

```markdown  theme={null}
---
name: db-reader
description: Execute read-only database queries. Use when analyzing data or generating reports.
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

You are a database analyst with read-only access. Execute SELECT queries to answer questions about the data.

When asked to analyze data:
1. Identify which tables contain the relevant data
2. Write efficient SELECT queries with appropriate filters
3. Present results clearly with context

You cannot modify data. If asked to INSERT, UPDATE, DELETE, or modify schema, explain that you only have read access.
```

Claude Code [透過 stdin 將 hook 輸入作為 JSON 傳遞](/zh-TW/hooks#pretooluse-input) 給 hook 命令。驗證指令碼讀取此 JSON，提取正在執行的命令，並根據 SQL 寫入操作清單檢查它。如果檢測到寫入操作，指令碼 [以代碼 2 退出](/zh-TW/hooks#exit-code-2-behavior-per-event) 以阻止執行，並透過 stderr 向 Claude 返回錯誤訊息。

在專案中的任何位置建立驗證指令碼。路徑必須與 hook 配置中的 `command` 欄位相符：

```bash  theme={null}
#!/bin/bash
# Blocks SQL write operations, allows SELECT queries

# Read JSON input from stdin
INPUT=$(cat)

# Extract the command field from tool_input using jq
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
  exit 0
fi

# Block write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|REPLACE|MERGE)\b' > /dev/null; then
  echo "Blocked: Write operations not allowed. Use SELECT queries only." >&2
  exit 2
fi

exit 0
```

使指令碼可執行：

```bash  theme={null}
chmod +x ./scripts/validate-readonly-query.sh
```

Hook 透過 stdin 接收 JSON，Bash 命令在 `tool_input.command` 中。退出代碼 2 阻止操作並將錯誤訊息反饋給 Claude。請參閱 [Hooks](/zh-TW/hooks#exit-code-output) 以取得有關退出代碼的詳細資訊，以及 [Hook 輸入](/zh-TW/hooks#pretooluse-input) 以取得完整的輸入架構。

## 後續步驟

現在您理解了 subagents，請探索這些相關功能：

* [使用 plugins 分發 subagents](/zh-TW/plugins) 以跨團隊或專案共享 subagents
* [以程式方式執行 Claude Code](/zh-TW/headless) 使用 Agent SDK 進行 CI/CD 和自動化
* [使用 MCP servers](/zh-TW/mcp) 為 subagents 提供外部工具和資料的存取
