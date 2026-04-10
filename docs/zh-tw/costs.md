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

# 有效管理成本

> 追蹤 token 使用情況、設定團隊支出限制，並透過上下文管理、模型選擇、延伸思考設定和預處理 hooks 來降低 Claude Code 成本。

Claude Code 在每次互動時都會消耗 token。成本因程式碼庫大小、查詢複雜性和對話長度而異。平均成本為每位開發人員每天 $6，90% 的使用者每日成本保持在 $12 以下。

對於團隊使用，Claude Code 按 API token 消耗量計費。平均而言，Claude Code 使用 Sonnet 4.6 時的成本約為每位開發人員每月 \$100-200，但根據使用者執行的執行個體數量以及他們是否在自動化中使用它，成本差異很大。

本頁涵蓋如何[追蹤您的成本](#track-your-costs)、[管理團隊成本](#managing-costs-for-teams)和[減少 token 使用](#reduce-token-usage)。

## 追蹤您的成本

### 使用 `/cost` 命令

<Note>
  `/cost` 命令顯示 API token 使用情況，適用於 API 使用者。Claude Max 和 Pro 訂閱者的使用情況已包含在其訂閱中，因此 `/cost` 資料與計費無關。訂閱者可以使用 `/stats` 來檢視使用模式。
</Note>

`/cost` 命令為您目前的工作階段提供詳細的 token 使用統計資訊：

```text  theme={null}
Total cost:            $0.55
Total duration (API):  6m 19.7s
Total duration (wall): 6h 33m 10.2s
Total code changes:    0 lines added, 0 lines removed
```

## 管理團隊成本

使用 Claude API 時，您可以在 Claude Code 工作區支出上[設定工作區支出限制](https://platform.claude.com/docs/zh-TW/build-with-claude/workspaces#workspace-limits)。管理員可以在主控台中[檢視成本和使用情況報告](https://platform.claude.com/docs/zh-TW/build-with-claude/workspaces#usage-and-cost-tracking)。

<Note>
  當您首次使用 Claude Console 帳戶驗證 Claude Code 時，系統會自動為您建立一個名為「Claude Code」的工作區。此工作區為您的組織中所有 Claude Code 使用情況提供集中式成本追蹤和管理。您無法為此工作區建立 API 金鑰；它專門用於 Claude Code 驗證和使用。
</Note>

在 Bedrock、Vertex 和 Foundry 上，Claude Code 不會從您的雲端傳送指標。若要取得成本指標，多家大型企業報告使用[LiteLLM](/zh-TW/llm-gateway#litellm-configuration)，這是一個開源工具，可幫助公司[按金鑰追蹤支出](https://docs.litellm.ai/docs/proxy/virtual_keys#tracking-spend)。此專案與 Anthropic 無關，且尚未進行安全審計。

### 速率限制建議

為團隊設定 Claude Code 時，請根據您的組織規模考慮這些每位使用者的 Token Per Minute (TPM) 和 Request Per Minute (RPM) 建議：

| 團隊規模         | 每位使用者 TPM | 每位使用者 RPM |
| ------------ | --------- | --------- |
| 1-5 位使用者     | 200k-300k | 5-7       |
| 5-20 位使用者    | 100k-150k | 2.5-3.5   |
| 20-50 位使用者   | 50k-75k   | 1.25-1.75 |
| 50-100 位使用者  | 25k-35k   | 0.62-0.87 |
| 100-500 位使用者 | 15k-20k   | 0.37-0.47 |
| 500+ 位使用者    | 10k-15k   | 0.25-0.35 |

例如，如果您有 200 位使用者，您可能會為每位使用者請求 20k TPM，或總共 400 萬 TPM (200\*20,000 = 400 萬)。

隨著團隊規模增長，每位使用者的 TPM 會減少，因為在較大的組織中，傾向於較少的使用者同時使用 Claude Code。這些速率限制適用於組織層級，而不是每個個別使用者，這意味著當其他人未主動使用該服務時，個別使用者可以暫時消耗超過其計算份額的資源。

<Note>
  如果您預期會出現異常高的並行使用情況（例如與大型群組進行的即時培訓課程），您可能需要更高的每位使用者 TPM 配置。
</Note>

### Agent 團隊 token 成本

[Agent 團隊](/zh-TW/agent-teams)會產生多個 Claude Code 執行個體，每個都有自己的上下文視窗。Token 使用量會隨著活躍隊友數量和每個隊友執行時間的長短而擴展。

為了保持 agent 團隊成本可控：

* 為隊友使用 Sonnet。它為協調任務平衡了功能和成本。
* 保持團隊規模小。每位隊友執行自己的上下文視窗，因此 token 使用量大致與團隊規模成正比。
* 保持產生提示的焦點。隊友會自動載入 CLAUDE.md、MCP 伺服器和技能，但產生提示中的所有內容都會從一開始就新增到其上下文中。
* 工作完成時清理團隊。活躍的隊友即使閒置也會繼續消耗 token。
* Agent 團隊預設為停用。在您的[settings.json](/zh-TW/settings)或環境中設定 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` 以啟用它們。請參閱[啟用 agent 團隊](/zh-TW/agent-teams#enable-agent-teams)。

## 減少 token 使用

Token 成本隨上下文大小而擴展：Claude 處理的上下文越多，您使用的 token 就越多。Claude Code 透過 prompt caching（減少重複內容（如系統提示）的成本）和 auto-compact（在接近上下文限制時總結對話歷史記錄）自動優化成本。

以下策略可幫助您保持上下文較小並降低每條訊息的成本。

### 主動管理上下文

使用 `/cost` 檢查您目前的 token 使用情況，或[設定您的狀態行](/zh-TW/statusline#context-window-usage)以持續顯示它。

* **在任務之間清除**：切換到不相關的工作時，使用 `/clear` 重新開始。過時的上下文會在後續的每條訊息上浪費 token。在清除之前使用 `/rename` 以便稍後輕鬆找到工作階段，然後使用 `/resume` 返回到它。
* **新增自訂壓縮指示**：`/compact Focus on code samples and API usage` 告訴 Claude 在總結期間要保留什麼。

您也可以在 CLAUDE.md 中自訂壓縮行為：

```markdown  theme={null}
# Compact instructions

When you are using compact, please focus on test output and code changes
```

### 選擇正確的模型

Sonnet 能很好地處理大多數編碼任務，成本低於 Opus。為複雜的架構決策或多步驟推理保留 Opus。使用 `/model` 在工作階段中途切換模型，或在 `/config` 中設定預設值。對於簡單的 subagent 任務，在您的[subagent 設定](/zh-TW/sub-agents#choose-a-model)中指定 `model: haiku`。

### 減少 MCP 伺服器開銷

每個 MCP 伺服器都會將工具定義新增到您的上下文中，即使在閒置時也是如此。執行 `/context` 以查看消耗空間的內容。

* **在可用時偏好 CLI 工具**：`gh`、`aws`、`gcloud` 和 `sentry-cli` 等工具比 MCP 伺服器更具上下文效率，因為它們不會新增持久的工具定義。Claude 可以直接執行 CLI 命令，無需開銷。
* **停用未使用的伺服器**：執行 `/mcp` 以查看已設定的伺服器，並停用任何您未主動使用的伺服器。
* **工具搜尋是自動的**：當 MCP 工具描述超過您的上下文視窗的 10% 時，Claude Code 會自動延遲它們，並透過[工具搜尋](/zh-TW/mcp#scale-with-mcp-tool-search)按需載入工具。由於延遲的工具只在實際使用時進入上下文，較低的閾值意味著較少的閒置工具定義消耗空間。使用 `ENABLE_TOOL_SEARCH=auto:<N>` 設定較低的閾值（例如，`auto:5` 在工具超過您的上下文視窗的 5% 時觸發）。

### 為型別化語言安裝程式碼智慧外掛

[程式碼智慧外掛](/zh-TW/discover-plugins#code-intelligence)為 Claude 提供精確的符號導航，而不是基於文字的搜尋，在探索不熟悉的程式碼時減少不必要的檔案讀取。單一「前往定義」呼叫取代了可能需要的 grep 後跟讀取多個候選檔案。已安裝的語言伺服器也會在編輯後自動報告型別錯誤，因此 Claude 無需執行編譯器即可捕捉錯誤。

### 將處理卸載到 hooks 和技能

自訂[hooks](/zh-TW/hooks)可以在 Claude 看到資料之前對其進行預處理。Claude 不是讀取 10,000 行日誌檔案來尋找錯誤，hook 可以 grep `ERROR` 並僅返回匹配的行，將上下文從數萬個 token 減少到數百個。

[技能](/zh-TW/skills)可以為 Claude 提供領域知識，因此它不必進行探索。例如，「codebase-overview」技能可以描述您的專案架構、關鍵目錄和命名慣例。當 Claude 呼叫該技能時，它會立即獲得此上下文，而不是花費 token 讀取多個檔案來理解結構。

例如，此 PreToolUse hook 篩選測試輸出以僅顯示失敗：

<Tabs>
  <Tab title="settings.json">
    將此新增到您的[settings.json](/zh-TW/settings#settings-files)以在每個 Bash 命令之前執行 hook：

    ```json  theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Bash",
            "hooks": [
              {
                "type": "command",
                "command": "~/.claude/hooks/filter-test-output.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="filter-test-output.sh">
    hook 呼叫此指令碼，該指令碼檢查命令是否為測試執行器並修改它以僅顯示失敗：

    ```bash  theme={null}
    #!/bin/bash
    input=$(cat)
    cmd=$(echo "$input" | jq -r '.tool_input.command')

    # If running tests, filter to show only failures
    if [[ "$cmd" =~ ^(npm test|pytest|go test) ]]; then
      filtered_cmd="$cmd 2>&1 | grep -A 5 -E '(FAIL|ERROR|error:)' | head -100"
      echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"updatedInput\":{\"command\":\"$filtered_cmd\"}}}"
    else
      echo "{}"
    fi
    ```
  </Tab>
</Tabs>

### 將指示從 CLAUDE.md 移至技能

您的[CLAUDE.md](/zh-TW/memory)檔案在工作階段開始時載入到上下文中。如果它包含特定工作流程的詳細指示（例如 PR 審查或資料庫遷移），即使您在進行不相關的工作時，這些 token 也會存在。[技能](/zh-TW/skills)僅在呼叫時按需載入，因此將專門指示移至技能可以保持您的基本上下文較小。目標是透過僅包含必要內容來將 CLAUDE.md 保持在約 500 行以下。

### 調整延伸思考

延伸思考預設為啟用，預算為 31,999 個 token，因為它可以顯著改善複雜規劃和推理任務的效能。但是，思考 token 會作為輸出 token 計費，因此對於不需要深度推理的較簡單任務，您可以透過在 `/effort` 中降低[努力等級](/zh-TW/model-config#adjust-effort-level)或在 `/model` 中降低、在 `/config` 中停用思考或降低預算（例如，`MAX_THINKING_TOKENS=8000`）來降低成本。

### 將詳細操作委派給 subagents

執行測試、擷取文件或處理日誌檔案可能會消耗大量上下文。將這些委派給[subagents](/zh-TW/sub-agents#isolate-high-volume-operations)，以便詳細輸出保留在 subagent 的上下文中，而只有摘要返回到您的主要對話。

### 管理 agent 團隊成本

當隊友在 plan mode 中執行時，Agent 團隊使用的 token 大約是標準工作階段的 7 倍，因為每位隊友維護自己的上下文視窗並作為單獨的 Claude 執行個體執行。保持團隊任務小且自成一體，以限制每位隊友的 token 使用。有關詳細資訊，請參閱[agent 團隊](/zh-TW/agent-teams)。

### 撰寫具體提示

模糊的請求（例如「改進此程式碼庫」）會觸發廣泛掃描。具體的請求（例如「在 auth.ts 中的登入函式中新增輸入驗證」）讓 Claude 能夠以最少的檔案讀取高效地工作。

### 有效處理複雜任務

對於較長或更複雜的工作，這些習慣有助於避免因走錯方向而浪費的 token：

* **對複雜任務使用 plan mode**：按 Shift+Tab 進入[plan mode](/zh-TW/common-workflows#use-plan-mode-for-safe-code-analysis)，然後再進行實施。Claude 探索程式碼庫並提出一個方法供您批准，防止當初始方向錯誤時進行昂貴的返工。
* **及早糾正方向**：如果 Claude 開始朝著錯誤的方向前進，按 Escape 立即停止。使用 `/rewind` 或雙擊 Escape 將對話和程式碼恢復到先前的 checkpoint。
* **提供驗證目標**：在您的提示中包含測試案例、貼上螢幕截圖或定義預期輸出。當 Claude 可以驗證自己的工作時，它會在您需要請求修復之前捕捉問題。
* **增量測試**：寫一個檔案、測試它，然後繼續。這會在問題便宜時及早捕捉問題。

## 背景 token 使用

Claude Code 即使在閒置時也會為某些背景功能使用 token：

* **對話總結**：為 `claude --resume` 功能總結先前對話的背景工作
* **命令處理**：某些命令（例如 `/cost`）可能會產生檢查狀態的請求

這些背景程序即使沒有主動互動也會消耗少量 token（通常每個工作階段不到 \$0.04）。

## 瞭解 Claude Code 行為的變化

Claude Code 定期接收可能改變功能工作方式的更新，包括成本報告。執行 `claude --version` 以檢查您目前的版本。如有具體計費問題，請透過您的[主控台帳戶](https://platform.claude.com/login)聯絡 Anthropic 支援。對於團隊部署，請從小型試點群組開始，以在更廣泛的推出前建立使用模式。
