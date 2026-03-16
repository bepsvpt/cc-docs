> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 協調 Claude Code 工作階段團隊

> 協調多個 Claude Code 實例作為團隊一起工作，具有共享任務、代理間訊息傳遞和集中管理。

<Warning>
  Agent teams 是實驗性功能，預設為停用。透過在 [settings.json](/zh-TW/settings) 或環境中新增 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` 來啟用。Agent teams 在工作階段恢復、任務協調和關閉行為方面有[已知限制](#limitations)。
</Warning>

Agent teams 讓您協調多個 Claude Code 實例一起工作。一個工作階段充當團隊主管，協調工作、分配任務並綜合結果。隊友獨立工作，各自在自己的 context window 中，並直接相互溝通。

與 [subagents](/zh-TW/sub-agents) 不同，subagents 在單個工作階段內運行，只能向主代理報告，您也可以直接與個別隊友互動，無需透過主管。

<Note>
  Agent teams 需要 Claude Code v2.1.32 或更新版本。使用 `claude --version` 檢查您的版本。
</Note>

本頁涵蓋：

* [何時使用 agent teams](#when-to-use-agent-teams)，包括最佳使用案例以及與 subagents 的比較
* [啟動團隊](#start-your-first-agent-team)
* [控制隊友](#control-your-agent-team)，包括顯示模式、任務分配和委派
* [並行工作的最佳實踐](#best-practices)

## 何時使用 agent teams

Agent teams 最適合用於並行探索能增加真實價值的任務。請參閱[使用案例範例](#use-case-examples)以了解完整情景。最強的使用案例是：

* **研究和審查**：多個隊友可以同時調查問題的不同方面，然後分享並質疑彼此的發現
* **新模組或功能**：隊友可以各自擁有一個獨立部分，不會相互干擾
* **使用競爭假設進行除錯**：隊友並行測試不同的理論，更快地收斂到答案
* **跨層協調**：跨越前端、後端和測試的變更，各由不同的隊友負責

Agent teams 增加了協調開銷，並使用的 tokens 遠多於單個工作階段。當隊友可以獨立運作時，它們效果最佳。對於順序任務、相同檔案編輯或具有許多依賴關係的工作，單個工作階段或 [subagents](/zh-TW/sub-agents) 更有效。

### 與 subagents 比較

Agent teams 和 [subagents](/zh-TW/sub-agents) 都讓您並行化工作，但它們的運作方式不同。根據您的工作人員是否需要相互溝通來選擇：

<Frame caption="Subagents 只向主代理報告結果，彼此不交談。在 agent teams 中，隊友共享任務列表、認領工作並直接相互溝通。">
  <img src="https://mintcdn.com/claude-code/nsvRFSDNfpSU5nT7/images/subagents-vs-agent-teams-light.png?fit=max&auto=format&n=nsvRFSDNfpSU5nT7&q=85&s=2f8db9b4f3705dd3ab931fbe2d96e42a" className="dark:hidden" alt="比較 subagent 和 agent team 架構的圖表。Subagents 由主代理生成、執行工作並報告結果。Agent teams 透過共享任務列表進行協調，隊友彼此直接溝通。" width="4245" height="1615" data-path="images/subagents-vs-agent-teams-light.png" />

  <img src="https://mintcdn.com/claude-code/nsvRFSDNfpSU5nT7/images/subagents-vs-agent-teams-dark.png?fit=max&auto=format&n=nsvRFSDNfpSU5nT7&q=85&s=d573a037540f2ada6a9ae7d8285b46fd" className="hidden dark:block" alt="比較 subagent 和 agent team 架構的圖表。Subagents 由主代理生成、執行工作並報告結果。Agent teams 透過共享任務列表進行協調，隊友彼此直接溝通。" width="4245" height="1615" data-path="images/subagents-vs-agent-teams-dark.png" />
</Frame>

|              | Subagents                   | Agent teams             |
| :----------- | :-------------------------- | :---------------------- |
| **Context**  | 自己的 context window；結果返回給呼叫者 | 自己的 context window；完全獨立 |
| **溝通**       | 只向主代理報告結果                   | 隊友直接相互訊息傳遞              |
| **協調**       | 主代理管理所有工作                   | 具有自我協調的共享任務列表           |
| **最適合**      | 只有結果重要的專注任務                 | 需要討論和協作的複雜工作            |
| **Token 成本** | 較低：結果摘要返回到主 context         | 較高：每個隊友是一個獨立的 Claude 實例 |

當您需要快速、專注的工作人員報告結果時，使用 subagents。當隊友需要分享發現、相互質疑並自行協調時，使用 agent teams。

## 啟用 agent teams

Agent teams 預設為停用。透過將 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` 環境變數設定為 `1`，在您的 shell 環境或透過 [settings.json](/zh-TW/settings) 來啟用：

```json settings.json theme={null}
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## 啟動您的第一個 agent team

啟用 agent teams 後，告訴 Claude 建立一個 agent team 並用自然語言描述您想要的任務和團隊結構。Claude 建立團隊、生成隊友並根據您的提示協調工作。

此範例效果很好，因為三個角色是獨立的，可以在不相互等待的情況下探索問題：

```text  theme={null}
I'm designing a CLI tool that helps developers track TODO comments across
their codebase. Create an agent team to explore this from different angles: one
teammate on UX, one on technical architecture, one playing devil's advocate.
```

從那裡，Claude 建立一個具有[共享任務列表](/zh-TW/interactive-mode#task-list)的團隊，為每個觀點生成隊友，讓他們探索問題，綜合發現，並嘗試在完成時[清理團隊](#clean-up-the-team)。

主管的終端列出所有隊友及其正在進行的工作。使用 Shift+Down 循環瀏覽隊友並直接向他們傳送訊息。在最後一個隊友之後，Shift+Down 會回到主管。

如果您希望每個隊友都在自己的分割窗格中，請參閱[選擇顯示模式](#choose-a-display-mode)。

## 控制您的 agent team

用自然語言告訴主管您想要什麼。它根據您的指示處理團隊協調、任務分配和委派。

### 選擇顯示模式

Agent teams 支援兩種顯示模式：

* **In-process**：所有隊友在您的主終端內運行。使用 Shift+Down 循環瀏覽隊友並輸入以直接向他們傳送訊息。在任何終端中工作，無需額外設定。
* **Split panes**：每個隊友都有自己的窗格。您可以同時看到所有人的輸出並點擊窗格直接互動。需要 tmux 或 iTerm2。

<Note>
  `tmux` 在某些作業系統上有已知限制，傳統上在 macOS 上效果最佳。在 iTerm2 中使用 `tmux -CC` 是進入 `tmux` 的建議入口點。
</Note>

預設值是 `"auto"`，如果您已在 tmux 工作階段內運行，則使用分割窗格，否則使用 in-process。`"tmux"` 設定啟用分割窗格模式，並根據您的終端自動偵測是否使用 tmux 或 iTerm2。若要覆蓋，請在 [settings.json](/zh-TW/settings) 中設定 `teammateMode`：

```json  theme={null}
{
  "teammateMode": "in-process"
}
```

若要為單個工作階段強制 in-process 模式，請將其作為旗標傳遞：

```bash  theme={null}
claude --teammate-mode in-process
```

分割窗格模式需要 [tmux](https://github.com/tmux/tmux/wiki) 或 iTerm2 搭配 [`it2` CLI](https://github.com/mkusaka/it2)。若要手動安裝：

* **tmux**：透過您系統的套件管理器安裝。請參閱 [tmux wiki](https://github.com/tmux/tmux/wiki/Installing) 以了解平台特定的指示。
* **iTerm2**：安裝 [`it2` CLI](https://github.com/mkusaka/it2)，然後在 **iTerm2 → Settings → General → Magic → Enable Python API** 中啟用 Python API。

### 指定隊友和模型

Claude 根據您的任務決定要生成的隊友數量，或者您可以指定您想要的確切內容：

```text  theme={null}
Create a team with 4 teammates to refactor these modules in parallel.
Use Sonnet for each teammate.
```

### 要求隊友的計畫批准

對於複雜或有風險的任務，您可以要求隊友在實施前進行計畫。隊友在唯讀計畫模式下工作，直到主管批准其方法：

```text  theme={null}
Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes.
```

當隊友完成計畫時，它會向主管發送計畫批准請求。主管審查計畫並批准或拒絕並提供反饋。如果被拒絕，隊友保持在計畫模式，根據反饋進行修訂並重新提交。一旦批准，隊友退出計畫模式並開始實施。

主管自主做出批准決定。若要影響主管的判斷，在您的提示中提供標準，例如「只批准包含測試覆蓋的計畫」或「拒絕修改資料庫架構的計畫」。

### 直接與隊友交談

每個隊友都是一個完整、獨立的 Claude Code 工作階段。您可以直接向任何隊友傳送訊息，以提供額外指示、提出後續問題或重新定向其方法。

* **In-process 模式**：使用 Shift+Down 循環瀏覽隊友，然後輸入以向他們傳送訊息。按 Enter 查看隊友的工作階段，然後按 Escape 中斷其目前回合。按 Ctrl+T 切換任務列表。
* **Split-pane 模式**：點擊隊友的窗格以直接與其工作階段互動。每個隊友都有自己終端的完整檢視。

### 分配和認領任務

共享任務列表協調整個團隊的工作。主管建立任務，隊友完成它們。任務有三種狀態：待處理、進行中和已完成。任務也可以依賴其他任務：具有未解決依賴關係的待處理任務在這些依賴關係完成之前無法被認領。

主管可以明確分配任務，或隊友可以自行認領：

* **主管分配**：告訴主管將哪個任務分配給哪個隊友
* **自行認領**：完成任務後，隊友自行選擇下一個未分配、未阻止的任務

任務認領使用檔案鎖定來防止多個隊友同時嘗試認領同一任務時的競爭條件。

### 關閉隊友

若要優雅地結束隊友的工作階段：

```text  theme={null}
Ask the researcher teammate to shut down
```

主管發送關閉請求。隊友可以批准並優雅地退出，或拒絕並提供解釋。

### 清理團隊

完成後，要求主管清理：

```text  theme={null}
Clean up the team
```

這會移除共享的團隊資源。當主管運行清理時，它會檢查活躍的隊友，如果仍有任何隊友在運行，則失敗，因此請先關閉他們。

<Warning>
  始終使用主管進行清理。隊友不應運行清理，因為他們的團隊 context 可能無法正確解析，可能會使資源處於不一致的狀態。
</Warning>

### 使用 hooks 強制執行品質閘門

使用 [hooks](/zh-TW/hooks) 在隊友完成工作或任務完成時強制執行規則：

* [`TeammateIdle`](/zh-TW/hooks#teammateidle)：當隊友即將閒置時運行。以代碼 2 退出以發送反饋並保持隊友工作。
* [`TaskCompleted`](/zh-TW/hooks#taskcompleted)：當任務被標記為完成時運行。以代碼 2 退出以防止完成並發送反饋。

## Agent teams 如何工作

本節涵蓋 agent teams 背後的架構和機制。如果您想開始使用它們，請參閱上面的[控制您的 agent team](#control-your-agent-team)。

### Claude 如何啟動 agent teams

Agent teams 有兩種啟動方式：

* **您請求一個團隊**：給 Claude 一個受益於並行工作的任務，並明確要求一個 agent team。Claude 根據您的指示建立一個。
* **Claude 提議一個團隊**：如果 Claude 確定您的任務將受益於並行工作，它可能會建議建立一個團隊。您在它繼續之前確認。

在這兩種情況下，您都保持控制。Claude 不會在沒有您批准的情況下建立團隊。

### 架構

Agent team 由以下部分組成：

| 元件            | 角色                                 |
| :------------ | :--------------------------------- |
| **Team lead** | 建立團隊、生成隊友並協調工作的主要 Claude Code 工作階段 |
| **Teammates** | 各自處理分配任務的獨立 Claude Code 實例         |
| **Task list** | 隊友認領和完成的共享工作項目列表                   |
| **Mailbox**   | 代理之間通訊的訊息系統                        |

請參閱[選擇顯示模式](#choose-a-display-mode)以了解顯示配置選項。隊友訊息自動到達主管。

系統自動管理任務依賴關係。當隊友完成其他任務依賴的任務時，被阻止的任務會自動解除阻止。

團隊和任務存儲在本地：

* **Team config**：`~/.claude/teams/{team-name}/config.json`
* **Task list**：`~/.claude/tasks/{team-name}/`

團隊配置包含一個 `members` 陣列，其中包含每個隊友的名稱、代理 ID 和代理類型。隊友可以讀取此檔案以發現其他團隊成員。

### 權限

隊友開始時具有主管的權限設定。如果主管使用 `--dangerously-skip-permissions` 運行，所有隊友也會這樣做。生成後，您可以更改個別隊友模式，但在生成時無法設定每個隊友的模式。

### Context 和通訊

每個隊友都有自己的 context window。生成時，隊友載入與常規工作階段相同的專案 context：CLAUDE.md、MCP servers 和 skills。它還接收來自主管的生成提示。主管的對話歷史不會延續。

**隊友如何分享資訊：**

* **自動訊息傳遞**：當隊友發送訊息時，它們會自動傳遞給收件人。主管不需要輪詢更新。
* **閒置通知**：當隊友完成並停止時，他們會自動通知主管。
* **共享任務列表**：所有代理都可以看到任務狀態並認領可用工作。

**隊友訊息傳遞：**

* **message**：向一個特定隊友發送訊息
* **broadcast**：同時發送給所有隊友。謹慎使用，因為成本隨團隊規模而增加。

### Token 使用

Agent teams 使用的 tokens 遠多於單個工作階段。每個隊友都有自己的 context window，token 使用量隨活躍隊友數量而增加。對於研究、審查和新功能工作，額外的 tokens 通常是值得的。對於日常任務，單個工作階段更具成本效益。請參閱 [agent team token 成本](/zh-TW/costs#agent-team-token-costs)以了解使用指南。

## 使用案例範例

這些範例展示了 agent teams 如何處理並行探索增加價值的任務。

### 運行並行程式碼審查

單個審查者傾向於一次專注於一種類型的問題。將審查標準分成獨立領域意味著安全性、效能和測試覆蓋都同時獲得徹底的關注。提示為每個隊友分配一個不同的視角，以便他們不重疊：

```text  theme={null}
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
```

每個審查者從相同的 PR 工作，但應用不同的篩選器。主管在他們完成後綜合所有三個的發現。

### 使用競爭假設進行調查

當根本原因不清楚時，單個代理傾向於找到一個看似合理的解釋並停止尋找。提示透過使隊友明確對抗來對抗這一點：每個隊友的工作不僅是調查自己的理論，還要質疑其他隊友的理論。

```text  theme={null}
Users report the app exits after one message instead of staying connected.
Spawn 5 agent teammates to investigate different hypotheses. Have them talk to
each other to try to disprove each other's theories, like a scientific
debate. Update the findings doc with whatever consensus emerges.
```

辯論結構是這裡的關鍵機制。順序調查受到錨定的影響：一旦探索了一個理論，後續調查就會偏向於它。

有多個獨立調查人員積極嘗試相互反駁，倖存的理論更有可能是實際的根本原因。

## 最佳實踐

### 給隊友足夠的 context

隊友自動載入專案 context，包括 CLAUDE.md、MCP servers 和 skills，但他們不繼承主管的對話歷史。請參閱[Context 和通訊](#context-and-communication)以了解詳情。在生成提示中包含任務特定的詳情：

```text  theme={null}
Spawn a security reviewer teammate with the prompt: "Review the authentication module
at src/auth/ for security vulnerabilities. Focus on token handling, session
management, and input validation. The app uses JWT tokens stored in
httpOnly cookies. Report any issues with severity ratings."
```

### 選擇適當的團隊規模

隊友數量沒有硬性限制，但實際限制適用：

* **Token 成本線性增加**：每個隊友都有自己的 context window 並獨立消耗 tokens。請參閱 [agent team token 成本](/zh-TW/costs#agent-team-token-costs)以了解詳情。
* **協調開銷增加**：更多隊友意味著更多通訊、任務協調和潛在衝突
* **收益遞減**：超過一定點後，額外的隊友不會按比例加快工作

對於大多數工作流程，從 3-5 個隊友開始。這平衡了並行工作與可管理的協調。本指南中的範例使用 3-5 個隊友，因為該範圍在不同任務類型中效果很好。

每個隊友有 5-6 個[任務](/zh-TW/agent-teams#architecture)可以保持每個人的生產力，而不會過度的上下文切換。如果您有 15 個獨立任務，3 個隊友是一個很好的起點。

只有當工作真正受益於隊友同時工作時才擴展。三個專注的隊友通常優於五個分散的隊友。

### 適當調整任務大小

* **太小**：協調開銷超過收益
* **太大**：隊友工作時間過長而沒有檢查點，增加浪費努力的風險
* **恰到好處**：自包含的單位，產生清晰的可交付成果，例如函數、測試檔案或審查

<Tip>
  主管將工作分解為任務並自動分配給隊友。如果它沒有建立足夠的任務，要求它將工作分成更小的部分。每個隊友有 5-6 個任務可以保持每個人的生產力，並讓主管在有人卡住時重新分配工作。
</Tip>

### 等待隊友完成

有時主管開始自己實施任務，而不是等待隊友。如果您注意到這一點：

```text  theme={null}
Wait for your teammates to complete their tasks before proceeding
```

### 從研究和審查開始

如果您是 agent teams 的新手，請從具有清晰邊界且不需要編寫程式碼的任務開始：審查 PR、研究庫或調查錯誤。這些任務展示了並行探索的價值，而不會帶來並行實施所帶來的協調挑戰。

### 避免檔案衝突

兩個隊友編輯同一檔案會導致覆蓋。分解工作，使每個隊友擁有不同的檔案集。

### 監控和引導

檢查隊友的進度，重新定向不起作用的方法，並在發現時綜合發現。讓團隊無人值守運行太長時間會增加浪費努力的風險。

## 故障排除

### 隊友未出現

如果在您要求 Claude 建立團隊後隊友未出現：

* 在 in-process 模式中，隊友可能已在運行但不可見。按 Shift+Down 循環瀏覽活躍隊友。
* 檢查您給 Claude 的任務是否足夠複雜以保證團隊。Claude 根據任務決定是否生成隊友。
* 如果您明確要求分割窗格，請確保 tmux 已安裝並在您的 PATH 中可用：
  ```bash  theme={null}
  which tmux
  ```
* 對於 iTerm2，驗證 `it2` CLI 已安裝且 Python API 在 iTerm2 偏好設定中啟用。

### 過多權限提示

隊友權限請求冒泡到主管，這可能會造成摩擦。在生成隊友之前在 [permission settings](/zh-TW/permissions) 中預批准常見操作以減少中斷。

### 隊友在錯誤時停止

隊友可能在遇到錯誤後停止，而不是恢復。使用 in-process 模式中的 Shift+Down 或分割模式中的點擊窗格檢查其輸出，然後：

* 直接給他們額外的指示
* 生成替換隊友以繼續工作

### 主管在工作完成前關閉

主管可能在所有任務實際完成之前決定團隊已完成。如果發生這種情況，告訴它繼續。您也可以告訴主管在繼續之前等待隊友完成，如果它開始做工作而不是委派。

### 孤立的 tmux 工作階段

如果 tmux 工作階段在團隊結束後仍然存在，它可能未被完全清理。列出工作階段並殺死由團隊建立的工作階段：

```bash  theme={null}
tmux ls
tmux kill-session -t <session-name>
```

## 限制

Agent teams 是實驗性的。要注意的目前限制：

* **In-process 隊友沒有工作階段恢復**：`/resume` 和 `/rewind` 不會恢復 in-process 隊友。恢復工作階段後，主管可能會嘗試向不再存在的隊友傳送訊息。如果發生這種情況，告訴主管生成新隊友。
* **任務狀態可能滯後**：隊友有時無法將任務標記為已完成，這會阻止依賴任務。如果任務似乎卡住，請檢查工作是否實際完成並手動更新任務狀態或告訴主管推動隊友。
* **關閉可能很慢**：隊友在關閉前完成其目前請求或工具呼叫，這可能需要時間。
* **每個工作階段一個團隊**：主管一次只能管理一個團隊。在啟動新團隊之前清理目前團隊。
* **沒有嵌套團隊**：隊友無法生成自己的團隊或隊友。只有主管可以管理團隊。
* **主管是固定的**：建立團隊的工作階段在其生命週期內是主管。您無法將隊友提升為主管或轉移領導權。
* **權限在生成時設定**：所有隊友開始時具有主管的權限模式。您可以在生成後更改個別隊友模式，但在生成時無法設定每個隊友的模式。
* **分割窗格需要 tmux 或 iTerm2**：預設 in-process 模式在任何終端中工作。VS Code 的整合終端、Windows Terminal 或 Ghostty 不支援分割窗格模式。

<Tip>
  **`CLAUDE.md` 正常工作**：隊友從其工作目錄讀取 `CLAUDE.md` 檔案。使用此為所有隊友提供專案特定的指導。
</Tip>

## 後續步驟

探索並行工作和委派的相關方法：

* **輕量級委派**：[subagents](/zh-TW/sub-agents) 在您的工作階段內為研究或驗證生成幫助代理，更適合不需要代理間協調的任務
* **手動並行工作階段**：[Git worktrees](/zh-TW/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) 讓您自己運行多個 Claude Code 工作階段，無需自動化團隊協調
* **比較方法**：請參閱 [subagent vs agent team](/zh-TW/features-overview#compare-similar-features) 比較以了解並排細分
