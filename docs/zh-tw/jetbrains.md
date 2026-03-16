> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# JetBrains IDEs

> 使用 Claude Code 與 JetBrains IDEs（包括 IntelliJ、PyCharm、WebStorm 等）整合

Claude Code 透過專用外掛程式與 JetBrains IDEs 整合，提供互動式差異檢視、選擇內容共享等功能。

## 支援的 IDEs

Claude Code 外掛程式適用於大多數 JetBrains IDEs，包括：

* IntelliJ IDEA
* PyCharm
* Android Studio
* WebStorm
* PhpStorm
* GoLand

## 功能

* **快速啟動**：使用 `Cmd+Esc`（Mac）或 `Ctrl+Esc`（Windows/Linux）直接從編輯器開啟 Claude Code，或點擊 UI 中的 Claude Code 按鈕
* **差異檢視**：程式碼變更可直接在 IDE 差異檢視器中顯示，而不是在終端機中
* **選擇內容共享**：IDE 中的目前選擇/分頁會自動與 Claude Code 共享
* **檔案參考快捷方式**：使用 `Cmd+Option+K`（Mac）或 `Alt+Ctrl+K`（Linux/Windows）插入檔案參考（例如 @File#L1-99）
* **診斷共享**：IDE 中的診斷錯誤（lint、語法等）會在您工作時自動與 Claude 共享

## 安裝

### Marketplace 安裝

從 JetBrains marketplace 尋找並安裝 [Claude Code 外掛程式](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-)，然後重新啟動您的 IDE。

如果您還未安裝 Claude Code，請參閱[我們的快速入門指南](/zh-TW/quickstart)以取得安裝說明。

<Note>
  安裝外掛程式後，您可能需要完全重新啟動 IDE 才能使其生效。
</Note>

## 使用方式

### 從您的 IDE

從 IDE 的整合終端機執行 `claude`，所有整合功能將處於活躍狀態。

### 從外部終端機

在任何外部終端機中使用 `/ide` 命令，將 Claude Code 連接到您的 JetBrains IDE 並啟動所有功能：

```bash  theme={null}
claude
```

```text  theme={null}
/ide
```

如果您希望 Claude 能夠存取與 IDE 相同的檔案，請從與 IDE 專案根目錄相同的目錄啟動 Claude Code。

## 設定

### Claude Code 設定

透過 Claude Code 的設定來設定 IDE 整合：

1. 執行 `claude`
2. 輸入 `/config` 命令
3. 將差異工具設定為 `auto` 以進行自動 IDE 偵測

### 外掛程式設定

透過前往 **Settings → Tools → Claude Code \[Beta]** 來設定 Claude Code 外掛程式：

#### 一般設定

* **Claude 命令**：指定自訂命令以執行 Claude（例如 `claude`、`/usr/local/bin/claude` 或 `npx @anthropic/claude`）
* **抑制找不到 Claude 命令的通知**：略過有關找不到 Claude 命令的通知
* **啟用使用 Option+Enter 進行多行提示**（僅限 macOS）：啟用時，Option+Enter 會在 Claude Code 提示中插入新行。如果遇到 Option 鍵被意外捕獲的問題，請停用此選項（需要終端機重新啟動）
* **啟用自動更新**：自動檢查並安裝外掛程式更新（在重新啟動時套用）

<Tip>
  對於 WSL 使用者：將 `wsl -d Ubuntu -- bash -lic "claude"` 設定為您的 Claude 命令（將 `Ubuntu` 替換為您的 WSL 發行版名稱）
</Tip>

#### ESC 鍵設定

如果 ESC 鍵無法在 JetBrains 終端機中中斷 Claude Code 操作：

1. 前往 **Settings → Tools → Terminal**
2. 執行下列其中一項：
   * 取消勾選「使用 Escape 將焦點移至編輯器」，或
   * 點擊「設定終端機快捷鍵」並刪除「切換焦點至編輯器」快捷方式
3. 套用變更

這將允許 ESC 鍵正確中斷 Claude Code 操作。

## 特殊設定

### 遠端開發

<Warning>
  使用 JetBrains 遠端開發時，您必須透過 **Settings → Plugin (Host)** 在遠端主機上安裝外掛程式。
</Warning>

外掛程式必須安裝在遠端主機上，而不是在您的本機用戶端機器上。

### WSL 設定

<Warning>
  WSL 使用者可能需要額外設定才能使 IDE 偵測正常運作。請參閱我們的 [WSL 疑難排解指南](/zh-TW/troubleshooting#jetbrains-ide-not-detected-on-wsl2)以取得詳細的設定說明。
</Warning>

WSL 設定可能需要：

* 適當的終端機設定
* 網路模式調整
* 防火牆設定更新

## 疑難排解

### 外掛程式無法運作

* 確保您從專案根目錄執行 Claude Code
* 檢查 JetBrains 外掛程式在 IDE 設定中是否已啟用
* 完全重新啟動 IDE（您可能需要執行多次）
* 對於遠端開發，確保外掛程式已安裝在遠端主機上

### IDE 未被偵測

* 驗證外掛程式已安裝並啟用
* 完全重新啟動 IDE
* 檢查您是否從整合終端機執行 Claude Code
* 對於 WSL 使用者，請參閱 [WSL 疑難排解指南](/zh-TW/troubleshooting#jetbrains-ide-not-detected-on-wsl2)

### 找不到命令

如果點擊 Claude 圖示顯示「找不到命令」：

1. 驗證 Claude Code 已安裝：`npm list -g @anthropic-ai/claude-code`
2. 在外掛程式設定中設定 Claude 命令路徑
3. 對於 WSL 使用者，使用設定部分中提到的 WSL 命令格式

## 安全考量

當 Claude Code 在啟用自動編輯權限的 JetBrains IDE 中執行時，它可能能夠修改可由您的 IDE 自動執行的 IDE 設定檔。這可能會增加在自動編輯模式下執行 Claude Code 的風險，並允許繞過 Claude Code 對 bash 執行的權限提示。

在 JetBrains IDEs 中執行時，請考慮：

* 對編輯使用手動核准模式
* 特別注意確保 Claude 僅與受信任的提示一起使用
* 注意 Claude Code 有權限修改的檔案

如需其他協助，請參閱我們的[疑難排解指南](/zh-TW/troubleshooting)。
