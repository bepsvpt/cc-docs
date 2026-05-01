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
* **選擇內容共享**：IDE 中的目前選擇或分頁會自動與 Claude Code 共享
* **檔案參考快捷方式**：使用 `Cmd+Option+K`（Mac）或 `Alt+Ctrl+K`（Linux/Windows）插入檔案參考，例如 `@src/auth.ts#L1-99`
* **診斷共享**：IDE 中的診斷錯誤（例如 lint 和語法錯誤）會在您工作時自動與 Claude 共享

## 安裝

### Marketplace 安裝

從 JetBrains marketplace 尋找並安裝 [Claude Code 外掛程式](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-)，然後重新啟動您的 IDE。

如果您還未安裝 Claude Code，請參閱[快速入門指南](/zh-TW/quickstart)以取得安裝說明。

<Note>
  安裝外掛程式後，您可能需要完全重新啟動 IDE 才能使其生效。
</Note>

## 使用方式

### 從您的 IDE

從 IDE 的整合終端機執行 `claude`，所有整合功能將處於活躍狀態。

### 從外部終端機

在任何外部終端機中使用 `/ide` 命令，將 Claude Code 連接到您的 JetBrains IDE 並啟動所有功能：

```bash theme={null}
claude
```

```text theme={null}
/ide
```

如果您希望 Claude 能夠存取與 IDE 相同的檔案，請從與 IDE 專案根目錄相同的目錄啟動 Claude Code。

## 設定

### Claude Code 設定

透過 Claude Code 的設定來設定 IDE 整合：

1. 執行 `claude`
2. 輸入 `/config` 命令
3. 將差異工具設定為 `auto` 以在 IDE 中顯示差異，或設定為 `terminal` 以在終端機中保留差異

### 外掛程式設定

透過前往 **Settings → Tools → Claude Code \[Beta]** 來設定 Claude Code 外掛程式：

#### 一般設定

* **Claude 命令**：指定自訂命令以執行 Claude，例如 `claude`、`/usr/local/bin/claude` 或 `npx @anthropic-ai/claude-code`
* **抑制找不到 Claude 命令的通知**：略過有關找不到 Claude 命令的通知
* **啟用使用 Option+Enter 進行多行提示**：僅限 macOS。啟用時，Option+Enter 會在 Claude Code 提示中插入新行。如果遇到 Option 鍵被意外捕獲的問題，請停用此選項。需要終端機重新啟動。
* **啟用自動更新**：自動檢查並安裝外掛程式更新，在重新啟動時套用

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

如果您在 WSL2 上使用 Claude Code 搭配 JetBrains IDE，並看到「未偵測到可用的 IDEs」，原因通常是 WSL2 的 NAT 網路或 Windows 防火牆阻止了 WSL2 與在 Windows 主機上執行的 IDE 之間的連線。WSL1 直接使用主機的網路，不受影響。

#### 允許 WSL2 流量通過 Windows 防火牆

這是建議的修復方式，因為它保持您現有的 WSL2 網路模式。

<Steps>
  <Step title="尋找您的 WSL2 IP 位址">
    從您的 WSL shell 內執行：

    ```bash theme={null}
    hostname -I
    ```

    記下子網路，例如 `172.21.123.45` 在 `172.21.0.0/16` 中。
  </Step>

  <Step title="建立防火牆規則">
    以系統管理員身份開啟 PowerShell 並執行以下命令，調整 IP 範圍以符合您的子網路：

    ```powershell theme={null}
    New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
    ```
  </Step>

  <Step title="重新啟動您的 IDE 和 Claude Code">
    關閉並重新開啟兩者，以使新規則生效。
  </Step>
</Steps>

#### 將 WSL2 切換為鏡像網路

鏡像網路需要 Windows 11 22H2 或更新版本。如果您使用 Windows 10，請改用上述防火牆規則。

將以下內容新增到您 Windows 使用者目錄中的 `.wslconfig`：

```ini theme={null}
[wsl2]
networkingMode=mirrored
```

然後從 PowerShell 使用 `wsl --shutdown` 重新啟動 WSL。

## 疑難排解

### 外掛程式無法運作

如果外掛程式已安裝但 Claude Code 功能未出現在您的 IDE 中：

* 確保您從專案根目錄執行 Claude Code
* 檢查 JetBrains 外掛程式在 IDE 設定中是否已啟用
* 完全重新啟動 IDE（您可能需要執行多次）
* 對於遠端開發，確保外掛程式已安裝在遠端主機上

### IDE 未被偵測

如果執行 `claude` 顯示「未偵測到可用的 IDEs」：

* 驗證外掛程式已安裝並啟用
* 完全重新啟動 IDE
* 檢查您是否從整合終端機執行 Claude Code
* 對於 WSL 使用者，請參閱上方的 [WSL 設定](#wsl-設定)

### 找不到命令

如果點擊 Claude 圖示顯示「找不到命令」：

1. 透過在終端機中執行 `claude --version` 驗證 Claude Code 已安裝
2. 在外掛程式設定中設定 Claude 命令路徑
3. 對於 WSL 使用者，使用設定部分中提到的 WSL 命令格式

## 安全考量

當 Claude Code 在啟用自動編輯權限的 JetBrains IDE 中執行時，它可能能夠修改可由您的 IDE 自動執行的 IDE 設定檔。這可能會增加在自動編輯模式下執行 Claude Code 的風險，並允許繞過 Claude Code 對 bash 執行的權限提示。

在 JetBrains IDEs 中執行時，請考慮：

* 對編輯使用手動核准模式
* 特別注意確保 Claude 僅與受信任的提示一起使用
* 注意 Claude Code 有權限修改的檔案

如需 IDE 外的 Claude Code 安裝或登入問題，請參閱[疑難排解安裝和登入](/zh-TW/troubleshoot-install)。
