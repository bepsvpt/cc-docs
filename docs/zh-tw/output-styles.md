> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 輸出樣式

> 將 Claude Code 適配用於軟體工程以外的用途

輸出樣式改變 Claude 的回應方式，而不是 Claude 知道什麼。它們修改系統提示以設定角色、語氣和輸出格式，同時保留核心功能，例如執行指令碼、讀取和寫入檔案，以及追蹤待辦事項。當您每次都重新提示相同的語音或格式，或者當您希望 Claude 充當軟體工程師以外的角色時，請使用一個。

有關您的專案、慣例或程式碼庫的說明，請改用 [CLAUDE.md](/zh-TW/memory)。

## 內建輸出樣式

Claude Code 的**預設**輸出樣式是現有的系統提示，旨在幫助您有效地完成軟體工程任務。

還有三種額外的內建輸出樣式：

* **Proactive**：Claude 立即執行，做出合理的假設而不是暫停進行例行決策，並偏好行動而非規劃。這應用與[自動模式](/zh-TW/permission-modes#eliminate-prompts-with-auto-mode)相同的指導，而不改變您的權限模式，因此您在工具運行前仍會看到權限提示。

* **Explanatory**：在幫助您完成軟體工程任務的同時提供教育性的「Insights」。幫助您理解實現選擇和程式碼庫模式。

* **Learning**：協作式的邊做邊學模式，Claude 不僅會在編碼時分享「Insights」，還會要求您自己貢獻小的、策略性的程式碼片段。Claude Code 將在您的程式碼中添加 `TODO(human)` 標記供您實現。

## 輸出樣式的工作原理

輸出樣式直接修改 Claude Code 的系統提示。

* 自訂輸出樣式排除了編碼指令（例如使用測試驗證程式碼），除非 `keep-coding-instructions` 為真。
* 所有輸出樣式都在系統提示的末尾添加了自己的自訂指令。
* 所有輸出樣式都會在對話期間觸發提醒，讓 Claude 遵守輸出樣式指令。

Token 使用量取決於樣式。將指令添加到系統提示會增加輸入 token，儘管 prompt caching 在工作階段中的第一個請求之後會降低此成本。內建的 Explanatory 和 Learning 樣式按設計會產生比預設更長的回應，這會增加輸出 token。對於自訂樣式，輸出 token 使用量取決於您的指令告訴 Claude 要產生什麼。

## 變更您的輸出樣式

執行 `/config` 並選擇**輸出樣式**以從選單中選擇樣式。您的選擇會儲存到[本地專案層級](/zh-TW/settings)的 `.claude/settings.local.json`。

若要在不使用選單的情況下設定樣式，請直接編輯設定檔中的 `outputStyle` 欄位：

```json theme={null}
{
  "outputStyle": "Explanatory"
}
```

由於輸出樣式是在工作階段開始時在系統提示中設定的，變更將在您下次啟動新工作階段時生效。這使系統提示在整個對話中保持穩定，以便 prompt caching 可以降低延遲和成本。

## 建立自訂輸出樣式

自訂輸出樣式是具有 frontmatter 和將添加到系統提示的文字的 Markdown 檔案：

```markdown theme={null}
---
name: My Custom Style
description:
  A brief description of what this style does, to be displayed to the user
---

# Custom Style Instructions

You are an interactive CLI tool that helps users with software engineering
tasks. [Your custom instructions here...]

## Specific Behaviors

[Define how the assistant should behave in this style...]
```

您可以在三個層級儲存這些檔案：

* 使用者：`~/.claude/output-styles`
* 專案：`.claude/output-styles`
* 受管原則：[受管設定目錄](/zh-TW/settings#settings-files)內的 `.claude/output-styles`

[Plugins](/zh-TW/plugins-reference) 也可以在 `output-styles/` 目錄中提供輸出樣式。

### Frontmatter

輸出樣式檔案支援 frontmatter 以指定中繼資料：

| Frontmatter                | 用途                                                                                                   | 預設      |
| :------------------------- | :--------------------------------------------------------------------------------------------------- | :------ |
| `name`                     | 輸出樣式的名稱，如果不是檔案名稱                                                                                     | 繼承自檔案名稱 |
| `description`              | 輸出樣式的描述，在 `/config` 選擇器中顯示                                                                           | 無       |
| `keep-coding-instructions` | 是否保留 Claude Code 系統提示中與編碼相關的部分。                                                                      | false   |
| `force-for-plugin`         | 僅限 Plugin 輸出樣式：在啟用 plugin 時自動應用此樣式，無需要求使用者選擇它。覆蓋使用者的 `outputStyle` 設定。如果多個啟用的 plugin 設定此項，則第一個載入的獲勝。 | false   |

## 與相關功能的比較

### 輸出樣式 vs. CLAUDE.md vs. --append-system-prompt

根據 Claude 是否應該停止充當編碼助手或保持其預設角色並學習更多內容來選擇。輸出樣式用您自己的角色和聲音替換 Claude Code 系統提示中的軟體工程部分，因此當 Claude 應該採用不同的身份（例如寫作編輯或數據分析助手）時，請使用一個。CLAUDE.md 和 `--append-system-prompt` 都保持 Claude Code 的預設身份並添加到它，因此當 Claude 應該保持編碼助手身份同時遵循您的專案慣例或額外指示時，請使用它們。

機制也不同。輸出樣式直接編輯系統提示。CLAUDE.md 在系統提示之後將其內容添加為使用者訊息。`--append-system-prompt` 將內容附加到系統提示的末尾，而不移除任何內容。

### 輸出樣式 vs. [Agents](/zh-TW/sub-agents)

使用輸出樣式在每個工作階段中改變主對話的回應方式。當您想要一個單獨作用域的幫助程式，由主對話委派給它時，請使用 [subagent](/zh-TW/sub-agents)。輸出樣式僅影響主代理迴圈的系統提示。Agents 處理特定任務，可以攜帶自己的模型、工具和有關何時呼叫它們的上下文。

### 輸出樣式 vs. [Skills](/zh-TW/skills)

輸出樣式修改 Claude 的回應方式（格式、語氣、結構），一旦選擇就始終處於活動狀態。Skills 是特定於任務的提示，您可以使用 `/skill-name` 呼叫或 Claude 在相關時自動載入。使用輸出樣式來實現一致的格式設定偏好；使用 skills 來實現可重複使用的工作流程和任務。
