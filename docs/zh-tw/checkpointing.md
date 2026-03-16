> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Checkpointing

> 自動追蹤並回溯 Claude 的編輯，快速恢復不想要的變更。

Claude Code 會自動追蹤 Claude 在您工作時所做的檔案編輯，讓您可以快速復原變更並回溯到先前的狀態，以防任何事情出現偏差。

## Checkpointing 如何運作

當您與 Claude 合作時，checkpointing 會自動在每次編輯前捕捉您程式碼的狀態。這個安全網讓您可以放心地進行雄心勃勃的大規模任務，因為您隨時可以回到先前的程式碼狀態。

### 自動追蹤

Claude Code 追蹤其檔案編輯工具所做的所有變更：

* 每個使用者提示都會建立一個新的 checkpoint
* Checkpoints 在工作階段之間持續存在，因此您可以在恢復的對話中存取它們
* 在 30 天後自動清理（可配置）

### 回溯變更

按兩次 `Esc`（`Esc` + `Esc`）或使用 `/rewind` 命令來開啟回溯選單。您可以選擇恢復：

* **僅對話**：回溯到使用者訊息，同時保留程式碼變更
* **僅程式碼**：還原檔案變更，同時保留對話
* **程式碼和對話**：將兩者都恢復到工作階段中的先前點

## 常見使用案例

Checkpoints 在以下情況特別有用：

* **探索替代方案**：嘗試不同的實作方法，而不會失去您的起點
* **從錯誤中恢復**：快速復原引入錯誤或破壞功能的變更
* **反覆迭代功能**：實驗變化，同時知道您可以回到工作狀態

## 限制

### Bash 命令變更未被追蹤

Checkpointing 不追蹤由 bash 命令修改的檔案。例如，如果 Claude Code 執行：

```bash  theme={null}
rm file.txt
mv old.txt new.txt
cp source.txt dest.txt
```

這些檔案修改無法透過回溯復原。只有透過 Claude 的檔案編輯工具所做的直接檔案編輯才會被追蹤。

### 外部變更未被追蹤

Checkpointing 只追蹤在目前工作階段中已編輯的檔案。您在 Claude Code 外部手動對檔案所做的變更，以及來自其他並行工作階段的編輯通常不會被捕捉，除非它們碰巧修改了與目前工作階段相同的檔案。

### 不是版本控制的替代品

Checkpoints 設計用於快速的工作階段級恢復。對於永久版本歷史和協作：

* 繼續使用版本控制（例如 Git）進行提交、分支和長期歷史
* Checkpoints 補充但不替代適當的版本控制
* 將 checkpoints 視為「本地復原」，將 Git 視為「永久歷史」

## 另請參閱

* [Interactive mode](/zh-TW/interactive-mode) - 快捷鍵和工作階段控制
* [Built-in commands](/zh-TW/interactive-mode#built-in-commands) - 使用 `/rewind` 存取 checkpoints
* [CLI reference](/zh-TW/cli-reference) - 命令列選項
