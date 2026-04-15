> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Checkpointing

> 追蹤、回溯和總結 Claude 的編輯和對話以管理會話狀態。

Claude Code 會自動追蹤 Claude 在您工作時所做的檔案編輯，讓您可以快速撤銷變更並回溯到先前的狀態，以防任何事情出現偏差。

## Checkpointing 的運作方式

當您與 Claude 合作時，checkpointing 會自動捕捉每次編輯前的程式碼狀態。這個安全網讓您可以進行雄心勃勃的大規模任務，同時知道您可以隨時回到先前的程式碼狀態。

### 自動追蹤

Claude Code 追蹤由其檔案編輯工具所做的所有變更：

* 每個使用者提示都會建立一個新的 checkpoint
* Checkpoints 在會話之間持續存在，因此您可以在恢復的對話中存取它們
* 自動清理，與會話一起在 30 天後刪除（可配置）

### 回溯和總結

按兩次 `Esc`（`Esc` + `Esc`）或使用 `/rewind` 命令來開啟回溯選單。可滾動的清單顯示會話中的每個提示。選擇您想要操作的點，然後選擇一個動作：

* **恢復程式碼和對話**：將程式碼和對話都回復到該點
* **恢復對話**：回溯到該訊息，同時保持目前程式碼
* **恢復程式碼**：回復檔案變更，同時保持對話
* **從此處總結**：將此點之後的對話壓縮為摘要，釋放 context window 空間
* **算了**：返回訊息清單而不進行任何變更

恢復對話或總結後，所選訊息的原始提示會恢復到輸入欄位中，以便您可以重新傳送或編輯它。

#### 恢復與總結

三個恢復選項會回復狀態：它們撤銷程式碼變更、對話歷史或兩者。「從此處總結」的運作方式不同：

* 所選訊息之前的訊息保持完整
* 所選訊息及其後的所有訊息都被替換為緊湊的 AI 生成摘要
* 磁碟上的檔案不會改變
* 原始訊息保存在會話記錄中，因此 Claude 可以在需要時參考詳細資訊

這類似於 `/compact`，但更有針對性：您不是總結整個對話，而是保持早期上下文的完整詳細資訊，只壓縮佔用空間的部分。您可以輸入可選指示來引導摘要的重點。

<Note>
  總結讓您保持在同一會話中並壓縮上下文。如果您想嘗試不同的方法，同時保持原始會話完整，請改用 [fork](/zh-TW/how-claude-code-works#resume-or-fork-sessions)（`claude --continue --fork-session`）。
</Note>

## 常見使用案例

Checkpoints 在以下情況下特別有用：

* **探索替代方案**：嘗試不同的實現方法，而不會失去起點
* **從錯誤中恢復**：快速撤銷引入錯誤或破壞功能的變更
* **迭代功能**：進行變化實驗，同時知道您可以回復到工作狀態
* **釋放上下文空間**：從中點開始總結冗長的除錯會話，保持初始指示完整

## 限制

### Bash 命令變更未追蹤

Checkpointing 不追蹤由 bash 命令修改的檔案。例如，如果 Claude Code 執行：

```bash theme={null}
rm file.txt
mv old.txt new.txt
cp source.txt dest.txt
```

這些檔案修改無法透過回溯撤銷。只有透過 Claude 的檔案編輯工具進行的直接檔案編輯才會被追蹤。

### 外部變更未追蹤

Checkpointing 只追蹤在目前會話中已編輯的檔案。您在 Claude Code 外部對檔案所做的手動變更以及來自其他並行會話的編輯通常不會被捕捉，除非它們碰巧修改與目前會話相同的檔案。

### 不是版本控制的替代品

Checkpoints 設計用於快速的會話級恢復。對於永久版本歷史和協作：

* 繼續使用版本控制（例如 Git）進行提交、分支和長期歷史
* Checkpoints 補充但不替代適當的版本控制
* 將 checkpoints 視為「本地撤銷」，Git 視為「永久歷史」

## 另請參閱

* [Interactive mode](/zh-TW/interactive-mode) - 快捷鍵和會話控制
* [Built-in commands](/zh-TW/commands) - 使用 `/rewind` 存取 checkpoints
* [CLI reference](/zh-TW/cli-reference) - 命令列選項
