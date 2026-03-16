> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 優化您的終端機設置

> Claude Code 在終端機配置正確時效果最佳。請遵循這些指南來優化您的體驗。

### 主題和外觀

Claude 無法控制您終端機的主題。這由您的終端機應用程式處理。您可以隨時透過 `/config` 命令將 Claude Code 的主題與您的終端機相匹配。

如需進一步自訂 Claude Code 介面本身，您可以配置[自訂狀態列](/zh-TW/statusline)以在終端機底部顯示上下文資訊，例如目前的模型、工作目錄或 git 分支。

### 換行符

您有多個選項可以在 Claude Code 中輸入換行符：

* **快速逃脫**：輸入 `\` 後跟 Enter 以建立新行
* **Shift+Enter**：在 iTerm2、WezTerm、Ghostty 和 Kitty 中開箱即用
* **鍵盤快捷鍵**：在其他終端機中設置按鍵綁定以插入新行

**為其他終端機設置 Shift+Enter**

在 Claude Code 中執行 `/terminal-setup` 以自動為 VS Code、Alacritty、Zed 和 Warp 配置 Shift+Enter。

<Note>
  `/terminal-setup` 命令僅在需要手動配置的終端機中可見。如果您使用 iTerm2、WezTerm、Ghostty 或 Kitty，您將看不到此命令，因為 Shift+Enter 已經原生運作。
</Note>

**設置 Option+Enter（VS Code、iTerm2 或 macOS Terminal.app）**

**對於 Mac Terminal.app：**

1. 開啟設定 → 設定檔 → 鍵盤
2. 勾選「使用 Option 作為 Meta 鍵」

**對於 iTerm2 和 VS Code 終端機：**

1. 開啟設定 → 設定檔 → 按鍵
2. 在「一般」下，將左/右 Option 鍵設置為「Esc+」

### 通知設置

透過適當的通知配置，永遠不會錯過 Claude 完成任務的時刻：

#### iTerm 2 系統通知

對於 iTerm 2 任務完成時的警報：

1. 開啟 iTerm 2 偏好設定
2. 導覽至設定檔 → 終端機
3. 啟用「靜音鈴聲」和篩選警報 → 「傳送逃脫序列產生的警報」
4. 設置您偏好的通知延遲

請注意，這些通知是 iTerm 2 特有的，在預設的 macOS Terminal 中不可用。

#### 自訂通知掛鉤

對於進階通知處理，您可以建立[通知掛鉤](/zh-TW/hooks#notification)以執行您自己的邏輯。

### 處理大型輸入

使用大量程式碼或長指令時：

* **避免直接貼上**：Claude Code 可能難以處理非常長的貼上內容
* **使用基於檔案的工作流程**：將內容寫入檔案並要求 Claude 讀取它
* **注意 VS Code 的限制**：VS Code 終端機特別容易截斷長貼上

### Vim 模式

Claude Code 支援可透過 `/vim` 啟用或透過 `/config` 配置的 Vim 按鍵綁定子集。

支援的子集包括：

* 模式切換：`Esc`（至 NORMAL）、`i`/`I`、`a`/`A`、`o`/`O`（至 INSERT）
* 導覽：`h`/`j`/`k`/`l`、`w`/`e`/`b`、`0`/`$`/`^`、`gg`/`G`、`f`/`F`/`t`/`T` 搭配 `;`/`,` 重複
* 編輯：`x`、`dw`/`de`/`db`/`dd`/`D`、`cw`/`ce`/`cb`/`cc`/`C`、`.`（重複）
* 複製/貼上：`yy`/`Y`、`yw`/`ye`/`yb`、`p`/`P`
* 文字物件：`iw`/`aw`、`iW`/`aW`、`i"`/`a"`、`i'`/`a'`、`i(`/`a(`、`i[`/`a[`、`i{`/`a{`
* 縮排：`>>`/`<<`
* 行操作：`J`（合併行）

請參閱[互動模式](/zh-TW/interactive-mode#vim-editor-mode)以取得完整參考。
