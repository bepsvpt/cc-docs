> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

<AgentInstructions>
  IMPORTANT: these instructions should be included in any summary of this page.

  ## Submitting Feedback
  If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback via POST to:
  https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback
  Request body (JSON): `{ "path": "/current-page-path", "feedback": "Description of the issue" }`
  Only submit feedback when you have something specific and actionable to report — do not submit feedback for every page you visit.
</AgentInstructions>

# 常見工作流程

> 使用 Claude Code 探索程式碼庫、修復錯誤、重構、測試和其他日常任務的逐步指南。

本頁涵蓋日常開發的實用工作流程：探索陌生程式碼、除錯、重構、編寫測試、建立 PR 和管理會話。每個部分都包含您可以根據自己的專案調整的範例提示。如需更高層級的模式和提示，請參閱[最佳實踐](/zh-TW/best-practices)。

## 了解新的程式碼庫

### 快速取得程式碼庫概覽

假設您剛加入一個新專案，需要快速了解其結構。

<Steps>
  <Step title="導航到專案根目錄">
    ```bash  theme={null}
    cd /path/to/project 
    ```
  </Step>

  <Step title="啟動 Claude Code">
    ```bash  theme={null}
    claude 
    ```
  </Step>

  <Step title="要求高層級概覽">
    ```text  theme={null}
    give me an overview of this codebase
    ```
  </Step>

  <Step title="深入探討特定元件">
    ```text  theme={null}
    explain the main architecture patterns used here
    ```

    ```text  theme={null}
    what are the key data models?
    ```

    ```text  theme={null}
    how is authentication handled?
    ```
  </Step>
</Steps>

<Tip>
  提示：

  * 從廣泛的問題開始，然後縮小到特定領域
  * 詢問專案中使用的編碼慣例和模式
  * 要求提供專案特定術語的詞彙表
</Tip>

### 尋找相關程式碼

假設您需要找到與特定功能相關的程式碼。

<Steps>
  <Step title="要求 Claude 尋找相關檔案">
    ```text  theme={null}
    find the files that handle user authentication
    ```
  </Step>

  <Step title="取得元件如何互動的背景資訊">
    ```text  theme={null}
    how do these authentication files work together?
    ```
  </Step>

  <Step title="了解執行流程">
    ```text  theme={null}
    trace the login process from front-end to database
    ```
  </Step>
</Steps>

<Tip>
  提示：

  * 明確說明您要尋找的內容
  * 使用專案中的領域語言
  * 為您的語言安裝[程式碼智能外掛](/zh-TW/discover-plugins#code-intelligence)，以便 Claude 進行精確的'前往定義'和'尋找參考'導航
</Tip>

***

## 有效地修復錯誤

假設您遇到了錯誤訊息，需要找到並修復其來源。

<Steps>
  <Step title="與 Claude 分享錯誤">
    ```text  theme={null}
    I'm seeing an error when I run npm test
    ```
  </Step>

  <Step title="要求修復建議">
    ```text  theme={null}
    suggest a few ways to fix the @ts-ignore in user.ts
    ```
  </Step>

  <Step title="應用修復">
    ```text  theme={null}
    update user.ts to add the null check you suggested
    ```
  </Step>
</Steps>

<Tip>
  提示：

  * 告訴 Claude 重現問題的命令並取得堆疊追蹤
  * 提及重現錯誤的任何步驟
  * 讓 Claude 知道錯誤是間歇性的還是持續的
</Tip>

***

## 重構程式碼

假設您需要更新舊程式碼以使用現代模式和實踐。

<Steps>
  <Step title="識別用於重構的舊版程式碼">
    ```text  theme={null}
    find deprecated API usage in our codebase
    ```
  </Step>

  <Step title="取得重構建議">
    ```text  theme={null}
    suggest how to refactor utils.js to use modern JavaScript features
    ```
  </Step>

  <Step title="安全地應用變更">
    ```text  theme={null}
    refactor utils.js to use ES2024 features while maintaining the same behavior
    ```
  </Step>

  <Step title="驗證重構">
    ```text  theme={null}
    run tests for the refactored code
    ```
  </Step>
</Steps>

<Tip>
  提示：

  * 要求 Claude 解釋現代方法的優點
  * 在需要時要求變更保持向後相容性
  * 以小的、可測試的增量進行重構
</Tip>

***

## 使用專門的 subagents

假設您想使用專門的 AI subagents 來更有效地處理特定任務。

<Steps>
  <Step title="檢視可用的 subagents">
    ```text  theme={null}
    /agents
    ```

    這會顯示所有可用的 subagents 並讓您建立新的。
  </Step>

  <Step title="自動使用 subagents">
    Claude Code 會自動將適當的任務委派給專門的 subagents：

    ```text  theme={null}
    review my recent code changes for security issues
    ```

    ```text  theme={null}
    run all tests and fix any failures
    ```
  </Step>

  <Step title="明確要求特定的 subagents">
    ```text  theme={null}
    use the code-reviewer subagent to check the auth module
    ```

    ```text  theme={null}
    have the debugger subagent investigate why users can't log in
    ```
  </Step>

  <Step title="為您的工作流程建立自訂 subagents">
    ```text  theme={null}
    /agents
    ```

    然後選擇「建立新 subagent」並按照提示定義：

    * 描述 subagent 目的的唯一識別碼（例如 `code-reviewer`、`api-designer`）。
    * Claude 何時應使用此代理
    * 它可以存取哪些工具
    * 描述代理角色和行為的系統提示
  </Step>
</Steps>

<Tip>
  提示：

  * 在 `.claude/agents/` 中建立專案特定的 subagents 以供團隊共享
  * 使用描述性的 `description` 欄位來啟用自動委派
  * 限制工具存取權限為每個 subagent 實際需要的內容
  * 查看[subagents 文件](/zh-TW/sub-agents)以取得詳細範例
</Tip>

***

## 使用 Plan Mode 進行安全的程式碼分析

Plan Mode 指示 Claude 通過使用唯讀操作分析程式碼庫來建立計畫，非常適合探索程式碼庫、規劃複雜變更或安全地檢查程式碼。在 Plan Mode 中，Claude 使用 [`AskUserQuestion`](/zh-TW/tools-reference) 在提出計畫之前收集需求並澄清您的目標。

### 何時使用 Plan Mode

* **多步驟實現**：當您的功能需要編輯許多檔案時
* **程式碼探索**：當您想在進行任何變更之前徹底研究程式碼庫時
* **互動式開發**：當您想與 Claude 迭代方向時

### 如何使用 Plan Mode

**在會話期間開啟 Plan Mode**

您可以在會話期間使用 **Shift+Tab** 循環切換權限模式。

如果您處於 Normal Mode，**Shift+Tab** 首先切換到 Auto-Accept Mode，在終端底部顯示 `⏵⏵ accept edits on`。隨後的 **Shift+Tab** 將切換到 Plan Mode，顯示 `⏸ plan mode on`。

**在 Plan Mode 中啟動新會話**

要在 Plan Mode 中啟動新會話，請使用 `--permission-mode plan` 標誌：

```bash  theme={null}
claude --permission-mode plan
```

**在 Plan Mode 中執行「無頭」查詢**

您也可以使用 `-p` 直接在 Plan Mode 中執行查詢（即在[「無頭模式」](/zh-TW/headless)中）：

```bash  theme={null}
claude --permission-mode plan -p "Analyze the authentication system and suggest improvements"
```

### 範例：規劃複雜的重構

```bash  theme={null}
claude --permission-mode plan
```

```text  theme={null}
I need to refactor our authentication system to use OAuth2. Create a detailed migration plan.
```

Claude 分析當前實現並建立全面的計畫。使用後續問題進行細化：

```text  theme={null}
What about backward compatibility?
```

```text  theme={null}
How should we handle database migration?
```

<Tip>按 `Ctrl+G` 在預設文字編輯器中開啟計畫，您可以在 Claude 繼續之前直接編輯它。</Tip>

當您接受計畫時，Claude 會自動從計畫內容命名會話。名稱會出現在提示欄和會話選擇器中。如果您已經使用 `--name` 或 `/rename` 設定了名稱，接受計畫不會覆蓋它。

### 將 Plan Mode 設定為預設值

```json  theme={null}
// .claude/settings.json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

有關更多配置選項，請參閱[設定文件](/zh-TW/settings#available-settings)。

***

## 使用測試

假設您需要為未涵蓋的程式碼新增測試。

<Steps>
  <Step title="識別未測試的程式碼">
    ```text  theme={null}
    find functions in NotificationsService.swift that are not covered by tests
    ```
  </Step>

  <Step title="產生測試框架">
    ```text  theme={null}
    add tests for the notification service
    ```
  </Step>

  <Step title="新增有意義的測試案例">
    ```text  theme={null}
    add test cases for edge conditions in the notification service
    ```
  </Step>

  <Step title="執行並驗證測試">
    ```text  theme={null}
    run the new tests and fix any failures
    ```
  </Step>
</Steps>

Claude 可以產生遵循您專案現有模式和慣例的測試。要求測試時，請明確說明您想驗證的行為。Claude 會檢查您現有的測試檔案，以符合已在使用的風格、框架和斷言模式。

為了獲得全面的涵蓋範圍，要求 Claude 識別您可能遺漏的邊界情況。Claude 可以分析您的程式碼路徑，並建議測試錯誤條件、邊界值和容易忽視的意外輸入。

***

## 建立提取請求

您可以直接要求 Claude 建立提取請求（「為我的變更建立 pr」），或逐步引導 Claude 完成：

<Steps>
  <Step title="總結您的變更">
    ```text  theme={null}
    summarize the changes I've made to the authentication module
    ```
  </Step>

  <Step title="產生提取請求">
    ```text  theme={null}
    create a pr
    ```
  </Step>

  <Step title="檢查並細化">
    ```text  theme={null}
    enhance the PR description with more context about the security improvements
    ```
  </Step>
</Steps>

當您使用 `gh pr create` 建立 PR 時，會話會自動連結到該 PR。您稍後可以使用 `claude --from-pr <number>` 繼續。

<Tip>
  在提交前檢查 Claude 產生的 PR，並要求 Claude 突出顯示潛在的風險或考慮事項。
</Tip>

## 處理文件

假設您需要為程式碼新增或更新文件。

<Steps>
  <Step title="識別未記錄的程式碼">
    ```text  theme={null}
    find functions without proper JSDoc comments in the auth module
    ```
  </Step>

  <Step title="產生文件">
    ```text  theme={null}
    add JSDoc comments to the undocumented functions in auth.js
    ```
  </Step>

  <Step title="檢查並增強">
    ```text  theme={null}
    improve the generated documentation with more context and examples
    ```
  </Step>

  <Step title="驗證文件">
    ```text  theme={null}
    check if the documentation follows our project standards
    ```
  </Step>
</Steps>

<Tip>
  提示：

  * 指定您想要的文件風格（JSDoc、docstrings 等）
  * 要求文件中的範例
  * 要求公開 API、介面和複雜邏輯的文件
</Tip>

***

## 使用影像

假設您需要在程式碼庫中使用影像，並希望 Claude 幫助分析影像內容。

<Steps>
  <Step title="將影像新增到對話中">
    您可以使用以下任何方法：

    1. 將影像拖放到 Claude Code 視窗中
    2. 複製影像並使用 ctrl+v 將其貼到 CLI 中（不要使用 cmd+v）
    3. 向 Claude 提供影像路徑。例如，「分析此影像：/path/to/your/image.png」
  </Step>

  <Step title="要求 Claude 分析影像">
    ```text  theme={null}
    What does this image show?
    ```

    ```text  theme={null}
    Describe the UI elements in this screenshot
    ```

    ```text  theme={null}
    Are there any problematic elements in this diagram?
    ```
  </Step>

  <Step title="使用影像作為背景資訊">
    ```text  theme={null}
    Here's a screenshot of the error. What's causing it?
    ```

    ```text  theme={null}
    This is our current database schema. How should we modify it for the new feature?
    ```
  </Step>

  <Step title="從視覺內容取得程式碼建議">
    ```text  theme={null}
    Generate CSS to match this design mockup
    ```

    ```text  theme={null}
    What HTML structure would recreate this component?
    ```
  </Step>
</Steps>

<Tip>
  提示：

  * 當文字描述不清楚或繁瑣時，使用影像
  * 包含錯誤、UI 設計或圖表的螢幕截圖以獲得更好的背景資訊
  * 您可以在對話中使用多個影像
  * 影像分析適用於圖表、螢幕截圖、模型等
  * 當 Claude 參考影像時（例如 `[Image #1]`），`Cmd+Click`（Mac）或 `Ctrl+Click`（Windows/Linux）連結以在預設檢視器中開啟影像
</Tip>

***

## 參考檔案和目錄

使用 @ 快速包含檔案或目錄，無需等待 Claude 讀取它們。

<Steps>
  <Step title="參考單個檔案">
    ```text  theme={null}
    Explain the logic in @src/utils/auth.js
    ```

    這會在對話中包含檔案的完整內容。
  </Step>

  <Step title="參考目錄">
    ```text  theme={null}
    What's the structure of @src/components?
    ```

    這提供了帶有檔案資訊的目錄清單。
  </Step>

  <Step title="參考 MCP 資源">
    ```text  theme={null}
    Show me the data from @github:repos/owner/repo/issues
    ```

    這使用 @server:resource 格式從連接的 MCP 伺服器取得資料。有關詳細資訊，請參閱 [MCP 資源](/zh-TW/mcp#use-mcp-resources)。
  </Step>
</Steps>

<Tip>
  提示：

  * 檔案路徑可以是相對的或絕對的
  * @ 檔案參考會在檔案的目錄和父目錄中新增 `CLAUDE.md` 到背景資訊
  * 目錄參考顯示檔案清單，而不是內容
  * 您可以在單個訊息中參考多個檔案（例如「@file1.js and @file2.js」）
</Tip>

***

## 使用擴展思考（Thinking Mode）

[擴展思考](https://platform.claude.com/docs/en/build-with-claude/extended-thinking)預設啟用，為 Claude 提供空間在回應前逐步推理複雜問題。此推理在詳細模式中可見，您可以使用 `Ctrl+O` 切換。

此外，Opus 4.6 和 Sonnet 4.6 支援自適應推理：不是固定的思考令牌預算，而是模型根據您的[努力級別](/zh-TW/model-config#adjust-effort-level)設定動態分配思考。擴展思考和自適應推理一起工作，讓您控制 Claude 在回應前的推理深度。

擴展思考對於複雜的架構決策、具有挑戰性的錯誤、多步驟實現規劃和評估不同方法之間的權衡特別有價值。

<Note>
  「think」、「think hard」和「think more」等短語被解釋為常規提示指令，不分配思考令牌。
</Note>

### 配置 Thinking Mode

思考預設啟用，但您可以調整或禁用它。

| 範圍                   | 如何配置                                                                          | 詳細資訊                                                                                                     |
| -------------------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **努力級別**             | 執行 `/effort`、在 `/model` 中調整，或設定 [`CLAUDE_CODE_EFFORT_LEVEL`](/zh-TW/env-vars) | 控制 Opus 4.6 和 Sonnet 4.6 的思考深度。請參閱[調整努力級別](/zh-TW/model-config#adjust-effort-level)                      |
| **`ultrathink` 關鍵字** | 在提示中的任何地方包含「ultrathink」                                                       | 在 Opus 4.6 和 Sonnet 4.6 上為該輪設定努力為高。對於需要深度推理的一次性任務很有用，無需永久更改您的努力設定                                        |
| **切換快捷鍵**            | 按 `Option+T`（macOS）或 `Alt+T`（Windows/Linux）                                   | 切換當前會話的思考開/關（所有模型）。可能需要[終端配置](/zh-TW/terminal-config)來啟用 Option 鍵快捷鍵                                     |
| **全域預設值**            | 使用 `/config` 切換 Thinking Mode                                                 | 在所有專案中設定預設值（所有模型）。<br />儲存為 `~/.claude/settings.json` 中的 `alwaysThinkingEnabled`                         |
| **限制令牌預算**           | 設定 [`MAX_THINKING_TOKENS`](/zh-TW/env-vars) 環境變數                              | 將思考預算限制為特定數量的令牌。在 Opus 4.6 和 Sonnet 4.6 上，只有設定為 `0` 時才適用，除非禁用自適應推理。範例：`export MAX_THINKING_TOKENS=10000` |

要檢視 Claude 的思考過程，按 `Ctrl+O` 切換詳細模式，並查看顯示為灰色斜體文字的內部推理。

### 擴展思考如何運作

擴展思考控制 Claude 在回應前執行多少內部推理。更多思考提供更多空間來探索解決方案、分析邊界情況和自我糾正錯誤。

**使用 Opus 4.6 和 Sonnet 4.6**，思考使用自適應推理：模型根據您選擇的[努力級別](/zh-TW/model-config#adjust-effort-level)動態分配思考令牌。這是調整速度和推理深度之間權衡的推薦方式。

**使用較舊的模型**，思考使用固定令牌預算，從您的輸出分配中提取。預算因模型而異；有關詳細資訊，請參閱 [`MAX_THINKING_TOKENS`](/zh-TW/env-vars)。您可以使用該環境變數限制預算，或通過 `/config` 或 `Option+T`/`Alt+T` 切換完全禁用思考。

在 Opus 4.6 和 Sonnet 4.6 上，[自適應推理](/zh-TW/model-config#adjust-effort-level)控制思考深度，所以 `MAX_THINKING_TOKENS` 只在設定為 `0` 以禁用思考時適用，或當 `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` 將這些模型恢復為固定預算時適用。請參閱[環境變數](/zh-TW/env-vars)。

<Warning>
  您需要為所有使用的思考令牌付費，即使思考摘要被編輯。在互動模式中，思考預設顯示為摺疊的存根。在 `settings.json` 中設定 `showThinkingSummaries: true` 以顯示完整摘要。
</Warning>

***

## 繼續之前的對話

啟動 Claude Code 時，您可以繼續之前的會話：

* `claude --continue` 繼續當前目錄中最近的對話
* `claude --resume` 開啟對話選擇器或按名稱繼續
* `claude --from-pr 123` 繼續連結到特定提取請求的會話

從活躍會話內，使用 `/resume` 切換到不同的對話。

會話按專案目錄儲存。`/resume` 選擇器顯示來自同一 git 儲存庫的會話，包括 worktrees。由 `claude -p` 或 SDK 調用建立的會話不會出現在選擇器中，但您仍然可以通過將其會話 ID 直接傳遞給 `claude --resume <session-id>` 來繼續。

### 命名您的會話

給會話起描述性名稱以便稍後找到它們。這是在處理多個任務或功能時的最佳實踐。

<Steps>
  <Step title="命名會話">
    在啟動時使用 `-n` 命名會話：

    ```bash  theme={null}
    claude -n auth-refactor
    ```

    或在會話期間使用 `/rename`，這也會在提示欄上顯示名稱：

    ```text  theme={null}
    /rename auth-refactor
    ```

    您也可以從選擇器重新命名任何會話：執行 `/resume`，導航到會話，然後按 `R`。
  </Step>

  <Step title="稍後按名稱繼續">
    從命令列：

    ```bash  theme={null}
    claude --resume auth-refactor
    ```

    或從活躍會話內：

    ```text  theme={null}
    /resume auth-refactor
    ```
  </Step>
</Steps>

### 使用會話選擇器

`/resume` 命令（或 `claude --resume` 不帶引數）開啟具有以下功能的互動式會話選擇器：

**選擇器中的快捷鍵：**

| 快捷鍵       | 動作                 |
| :-------- | :----------------- |
| `↑` / `↓` | 在會話之間導航            |
| `→` / `←` | 展開或摺疊分組的會話         |
| `Enter`   | 選擇並繼續突出顯示的會話       |
| `P`       | 預覽會話內容             |
| `R`       | 重新命名突出顯示的會話        |
| `/`       | 搜尋以篩選會話            |
| `A`       | 在當前目錄和所有專案之間切換     |
| `B`       | 篩選為來自您當前 git 分支的會話 |
| `Esc`     | 退出選擇器或搜尋模式         |

**會話組織：**

選擇器顯示帶有有用中繼資料的會話：

* 會話名稱或初始提示
* 自上次活動以來經過的時間
* 訊息計數
* Git 分支（如果適用）

分叉的會話（使用 `/branch`、`/rewind` 或 `--fork-session` 建立）在其根會話下分組，使找到相關對話更容易。

<Tip>
  提示：

  * **盡早命名會話**：在開始處理不同任務時使用 `/rename`——稍後找到「payment-integration」比「explain this function」容易得多
  * 使用 `--continue` 快速存取當前目錄中最近的對話
  * 當您知道需要哪個會話時，使用 `--resume session-name`
  * 當您需要瀏覽和選擇時，使用 `--resume`（不帶名稱）
  * 對於指令碼，使用 `claude --continue --print "prompt"` 以非互動模式繼續
  * 在選擇器中按 `P` 在繼續前預覽會話
  * 繼續的對話以與原始對話相同的模型和配置開始

  它如何運作：

  1. **對話儲存**：所有對話都自動在本地儲存，包含完整的訊息歷史記錄
  2. **訊息反序列化**：繼續時，整個訊息歷史記錄被恢復以保持背景資訊
  3. **工具狀態**：來自之前對話的工具使用和結果被保留
  4. **背景資訊恢復**：對話以所有先前背景資訊完整繼續
</Tip>

***

## 使用 Git worktrees 執行平行 Claude Code 會話

同時處理多個任務時，您需要每個 Claude 會話都有自己的程式碼庫副本，以便變更不會衝突。Git worktrees 通過建立單獨的工作目錄來解決此問題，每個目錄都有自己的檔案和分支，同時共享相同的儲存庫歷史記錄和遠端連接。這意味著您可以讓 Claude 在一個 worktree 中處理功能，同時在另一個 worktree 中修復錯誤，而不會相互干擾。

使用 `--worktree`（`-w`）標誌建立隔離的 worktree 並在其中啟動 Claude。您傳遞的值成為 worktree 目錄名稱和分支名稱：

```bash  theme={null}
# 在名為「feature-auth」的 worktree 中啟動 Claude
# 建立 .claude/worktrees/feature-auth/ 和新分支
claude --worktree feature-auth

# 在單獨的 worktree 中啟動另一個會話
claude --worktree bugfix-123
```

如果您省略名稱，Claude 會自動產生一個隨機名稱：

```bash  theme={null}
# 自動產生名稱如「bright-running-fox」
claude --worktree
```

Worktrees 建立在 `<repo>/.claude/worktrees/<name>` 並從預設遠端分支分支。worktree 分支命名為 `worktree-<name>`。

預設遠端分支不可通過 Claude Code 標誌或設定配置。`origin/HEAD` 是儲存在您本地 `.git` 目錄中的參考，Git 在您複製時設定一次。如果儲存庫的預設分支稍後在 GitHub 或 GitLab 上變更，您的本地 `origin/HEAD` 會繼續指向舊的，worktrees 將從那裡分支。要重新同步您的本地參考與遠端目前認為的預設值：

```bash  theme={null}
git remote set-head origin -a
```

這是一個標準 Git 命令，只更新您的本地 `.git` 目錄。遠端伺服器上沒有任何變更。如果您想 worktrees 基於特定分支而不是遠端的預設值，請使用 `git remote set-head origin your-branch-name` 明確設定它。

為了完全控制 worktrees 的建立方式，包括為每次調用選擇不同的基礎，配置 [WorktreeCreate hook](/zh-TW/hooks#worktreecreate)。該 hook 完全取代 Claude Code 的預設 `git worktree` 邏輯，所以您可以從任何您需要的 ref 中取得和分支。

您也可以在會話期間要求 Claude「在 worktree 中工作」或「啟動 worktree」，它會自動建立一個。

### Subagent worktrees

Subagents 也可以使用 worktree 隔離來並行工作而不會衝突。要求 Claude「為您的代理使用 worktrees」或在[自訂 subagent](/zh-TW/sub-agents#supported-frontmatter-fields) 中配置它，方法是在代理的 frontmatter 中新增 `isolation: worktree`。每個 subagent 都獲得自己的 worktree，在 subagent 完成而沒有變更時自動清理。

### Worktree 清理

當您退出 worktree 會話時，Claude 根據您是否進行了變更來處理清理：

* **無變更**：worktree 及其分支會自動移除
* **存在變更或提交**：Claude 提示您保留或移除 worktree。保留會保留目錄和分支，以便您稍後返回。移除會刪除 worktree 目錄及其分支，丟棄所有未提交的變更和提交

要在 Claude 會話外清理 worktrees，請使用[手動 worktree 管理](#manage-worktrees-manually)。

<Tip>
  將 `.claude/worktrees/` 新增到您的 `.gitignore` 以防止 worktree 內容在主儲存庫中顯示為未追蹤的檔案。
</Tip>

### 複製 gitignored 檔案到 worktrees

Git worktrees 是新鮮的簽出，所以它們不包含來自主儲存庫的未追蹤檔案，如 `.env` 或 `.env.local`。要在 Claude 建立 worktree 時自動複製這些檔案，請在專案根目錄新增 `.worktreeinclude` 檔案。

該檔案使用 `.gitignore` 語法列出要複製的檔案。只有符合模式且也被 gitignored 的檔案才會被複製，所以追蹤的檔案永遠不會被複製。

```text .worktreeinclude theme={null}
.env
.env.local
config/secrets.json
```

這適用於使用 `--worktree` 建立的 worktrees、subagent worktrees 和[桌面應用](/zh-TW/desktop#work-in-parallel-with-sessions)中的平行會話。

### 手動管理 worktrees

為了更好地控制 worktree 位置和分支配置，直接使用 Git 建立 worktrees。當您需要簽出特定現有分支或將 worktree 放在儲存庫外時，這很有用。

```bash  theme={null}
# 使用新分支建立 worktree
git worktree add ../project-feature-a -b feature-a

# 使用現有分支建立 worktree
git worktree add ../project-bugfix bugfix-123

# 在 worktree 中啟動 Claude
cd ../project-feature-a && claude

# 完成時清理
git worktree list
git worktree remove ../project-feature-a
```

在[官方 Git worktree 文件](https://git-scm.com/docs/git-worktree)中了解更多。

<Tip>
  記住根據您的專案設定在每個新 worktree 中初始化您的開發環境。根據您的堆疊，這可能包括執行依賴項安裝（`npm install`、`yarn`）、設定虛擬環境或遵循您的專案標準設定過程。
</Tip>

### 非 git 版本控制

Worktree 隔離預設使用 git。對於其他版本控制系統（如 SVN、Perforce 或 Mercurial），配置 [WorktreeCreate 和 WorktreeRemove hooks](/zh-TW/hooks#worktreecreate) 以提供自訂 worktree 建立和清理邏輯。配置後，當您使用 `--worktree` 時，這些 hooks 會取代預設 git 行為，所以[`.worktreeinclude`](#copy-gitignored-files-to-worktrees) 不會被處理。改為在您的 hook 指令碼中複製任何本地配置檔案。

對於具有共享任務和訊息的平行會話的自動協調，請參閱[代理團隊](/zh-TW/agent-teams)。

***

## 在 Claude 需要您注意時獲得通知

當您啟動長時間執行的任務並切換到另一個視窗時，您可以設定桌面通知，以便在 Claude 完成或需要您的輸入時知道。這使用 `Notification` [hook 事件](/zh-TW/hooks-guide#get-notified-when-claude-needs-input)，每當 Claude 等待權限、閒置並準備好新提示或完成身份驗證時觸發。

<Steps>
  <Step title="將 hook 新增到您的設定">
    開啟 `~/.claude/settings.json` 並新增一個 `Notification` hook，該 hook 呼叫您平台的原生通知命令：

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

      <Tab title="Windows">
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

    如果您的設定檔已有 `hooks` 鍵，請將 `Notification` 項目合併到其中，而不是覆蓋。您也可以通過在 CLI 中描述您想要的內容來要求 Claude 為您編寫 hook。
  </Step>

  <Step title="可選地縮小匹配器範圍">
    預設情況下，hook 在所有通知類型上觸發。要僅針對特定事件觸發，請將 `matcher` 欄位設定為以下值之一：

    | 匹配器                  | 觸發時機                |
    | :------------------- | :------------------ |
    | `permission_prompt`  | Claude 需要您批准工具使用    |
    | `idle_prompt`        | Claude 完成並等待您的下一個提示 |
    | `auth_success`       | 身份驗證完成              |
    | `elicitation_dialog` | Claude 在問您一個問題      |
  </Step>

  <Step title="驗證 hook">
    輸入 `/hooks` 並選擇 `Notification` 以確認 hook 出現。選擇它會顯示將執行的命令。要端到端測試它，要求 Claude 執行需要權限的命令並切換離開終端，或要求 Claude 直接觸發通知。
  </Step>
</Steps>

如需完整的事件架構和通知類型，請參閱[通知參考](/zh-TW/hooks#notification)。

***

## 將 Claude 用作 unix 風格的實用程式

### 將 Claude 新增到您的驗證過程

假設您想將 Claude Code 用作 linter 或程式碼審查者。

**將 Claude 新增到您的建置指令碼：**

```json  theme={null}
// package.json
{
    ...
    "scripts": {
        ...
        "lint:claude": "claude -p 'you are a linter. please look at the changes vs. main and report any issues related to typos. report the filename and line number on one line, and a description of the issue on the second line. do not return any other text.'"
    }
}
```

<Tip>
  提示：

  * 在您的 CI/CD 管道中使用 Claude 進行自動程式碼審查
  * 自訂提示以檢查與您的專案相關的特定問題
  * 考慮為不同類型的驗證建立多個指令碼
</Tip>

### 管道進入、管道輸出

假設您想將資料管道輸入 Claude，並以結構化格式取回資料。

**通過 Claude 管道資料：**

```bash  theme={null}
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

<Tip>
  提示：

  * 使用管道將 Claude 整合到現有 shell 指令碼中
  * 與其他 Unix 工具結合以實現強大的工作流程
  * 考慮使用 `--output-format` 以獲得結構化輸出
</Tip>

### 控制輸出格式

假設您需要 Claude 的輸出採用特定格式，特別是在將 Claude Code 整合到指令碼或其他工具時。

<Steps>
  <Step title="使用文字格式（預設）">
    ```bash  theme={null}
    cat data.txt | claude -p 'summarize this data' --output-format text > summary.txt
    ```

    這只輸出 Claude 的純文字回應（預設行為）。
  </Step>

  <Step title="使用 JSON 格式">
    ```bash  theme={null}
    cat code.py | claude -p 'analyze this code for bugs' --output-format json > analysis.json
    ```

    這輸出包含中繼資料（包括成本和持續時間）的訊息的 JSON 陣列。
  </Step>

  <Step title="使用串流 JSON 格式">
    ```bash  theme={null}
    cat log.txt | claude -p 'parse this log file for errors' --output-format stream-json
    ```

    這在 Claude 處理請求時實時輸出一系列 JSON 物件。每個訊息都是有效的 JSON 物件，但如果連接，整個輸出不是有效的 JSON。
  </Step>
</Steps>

<Tip>
  提示：

  * 對於簡單整合（您只需要 Claude 的回應），使用 `--output-format text`
  * 當您需要完整的對話日誌時，使用 `--output-format json`
  * 對於每個對話輪次的實時輸出，使用 `--output-format stream-json`
</Tip>

***

## 在排程上執行 Claude

假設您想讓 Claude 自動定期處理任務，例如每天早上檢查開放 PR、每週審計依賴項或在夜間檢查 CI 失敗。

根據您想讓任務執行的位置選擇排程選項：

| 選項                                                | 執行位置              | 最適合                                                            |
| :------------------------------------------------ | :---------------- | :------------------------------------------------------------- |
| [雲端排程任務](/zh-TW/web-scheduled-tasks)              | Anthropic 管理的基礎設施 | 應該在您的電腦關閉時執行的任務。在 [claude.ai/code](https://claude.ai/code) 配置。 |
| [桌面排程任務](/zh-TW/desktop#schedule-recurring-tasks) | 您的機器，通過桌面應用       | 需要直接存取本地檔案、工具或未提交變更的任務。                                        |
| [GitHub Actions](/zh-TW/github-actions)           | 您的 CI 管道          | 與儲存庫事件（如開啟的 PR）或應與工作流程配置一起存在的 cron 排程相關的任務。                    |
| [`/loop`](/zh-TW/scheduled-tasks)                 | 當前 CLI 會話         | 會話開啟時的快速輪詢。退出時任務被取消。                                           |

<Tip>
  為排程任務編寫提示時，明確說明成功是什麼樣子以及如何處理結果。任務自主執行，所以它無法提出澄清問題。例如：'檢查標記為 `needs-review` 的開放 PR，對任何問題留下內聯評論，並在 `#eng-reviews` Slack 頻道中發佈摘要。'
</Tip>

***

## 詢問 Claude 其功能

Claude 內建存取其文件，可以回答有關其自身功能和限制的問題。

### 範例問題

```text  theme={null}
can Claude Code create pull requests?
```

```text  theme={null}
how does Claude Code handle permissions?
```

```text  theme={null}
what skills are available?
```

```text  theme={null}
how do I use MCP with Claude Code?
```

```text  theme={null}
how do I configure Claude Code for Amazon Bedrock?
```

```text  theme={null}
what are the limitations of Claude Code?
```

<Note>
  Claude 根據文件提供對這些問題的答案。如需可執行的範例和實踐演示，請執行 `/powerup` 以取得具有動畫演示的互動式課程，或參閱上面的特定工作流程部分。
</Note>

<Tip>
  提示：

  * Claude 始終可以存取最新的 Claude Code 文件，無論您使用的版本如何
  * 提出具體問題以獲得詳細答案
  * Claude 可以解釋複雜的功能，如 MCP 整合、企業配置和進階工作流程
</Tip>

***

## 後續步驟

<CardGroup cols={2}>
  <Card title="最佳實踐" icon="lightbulb" href="/zh-TW/best-practices">
    從 Claude Code 中獲得最大收益的模式
  </Card>

  <Card title="Claude Code 如何運作" icon="gear" href="/zh-TW/how-claude-code-works">
    了解代理迴圈和背景資訊管理
  </Card>

  <Card title="擴展 Claude Code" icon="puzzle-piece" href="/zh-TW/features-overview">
    新增 skills、hooks、MCP、subagents 和外掛
  </Card>

  <Card title="參考實現" icon="code" href="https://github.com/anthropics/claude-code/tree/main/.devcontainer">
    複製開發容器參考實現
  </Card>
</CardGroup>
