> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 設定 Claude Code

> 在您的開發機器上安裝、驗證和開始使用 Claude Code。

## 系統需求

* **作業系統**：
  * macOS 13.0+
  * Windows 10 1809+ 或 Windows Server 2019+ ([查看設定說明](#platform-specific-setup))
  * Ubuntu 20.04+
  * Debian 10+
  * Alpine Linux 3.19+ ([需要額外的依賴項](#platform-specific-setup))
* **硬體**：4 GB+ RAM
* **網路**：需要網際網路連線 (查看 [網路設定](/zh-TW/network-config#network-access-requirements))
* **Shell**：在 Bash 或 Zsh 中效果最佳
* **位置**：[Anthropic 支援的國家](https://www.anthropic.com/supported-countries)

### 額外的依賴項

* **ripgrep**：通常包含在 Claude Code 中。如果搜尋失敗，請查看 [搜尋疑難排解](/zh-TW/troubleshooting#search-and-discovery-issues)。
* **[Node.js 18+](https://nodejs.org/en/download)**：僅在 [已棄用的 npm 安裝](#npm-installation-deprecated) 時需要

## 安裝

To install Claude Code, use one of the following methods:

<Tabs>
  <Tab title="Native Install (Recommended)">
    **macOS, Linux, WSL:**

    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell:**

    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD:**

    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```

    **Windows requires [Git for Windows](https://git-scm.com/downloads/win).** Install it first if you don't have it.

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash  theme={null}
    brew install --cask claude-code
    ```

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` periodically to get the latest features and security fixes.
    </Info>
  </Tab>

  <Tab title="WinGet">
    ```powershell  theme={null}
    winget install Anthropic.ClaudeCode
    ```

    <Info>
      WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
    </Info>
  </Tab>
</Tabs>

安裝程序完成後，導航到您的專案並啟動 Claude Code：

```bash  theme={null}
cd your-awesome-project
claude
```

如果您在安裝過程中遇到任何問題，請查閱 [疑難排解指南](/zh-TW/troubleshooting)。

<Tip>
  安裝後執行 `claude doctor` 以檢查您的安裝類型和版本。
</Tip>

### 平台特定設定

**Windows**：原生執行 Claude Code (需要 [Git Bash](https://git-scm.com/downloads/win)) 或在 WSL 內執行。支援 WSL 1 和 WSL 2，但 WSL 1 的支援有限，不支援 Bash 工具沙箱等功能。

**Alpine Linux 和其他 musl/uClibc 型發行版**：

Alpine 和其他 musl/uClibc 型發行版上的原生安裝程式需要 `libgcc`、`libstdc++` 和 `ripgrep`。使用您的發行版的套件管理員安裝這些，然後設定 `USE_BUILTIN_RIPGREP=0`。

在 Alpine 上：

```bash  theme={null}
apk add libgcc libstdc++ ripgrep
```

### 驗證

#### 針對個人

1. **Claude Pro 或 Max 方案** (建議)：訂閱 Claude 的 [Pro 或 Max 方案](https://claude.ai/pricing)，以獲得統一的訂閱，包括 Claude Code 和網頁版 Claude。在一個地方管理您的帳戶，並使用您的 Claude.ai 帳戶登入。
2. **Claude Console**：透過 [Claude Console](https://console.anthropic.com) 連線並完成 OAuth 程序。需要在 Anthropic Console 中有有效的帳單。系統會自動為使用情況追蹤和成本管理建立「Claude Code」工作區。您無法為 Claude Code 工作區建立 API 金鑰；它專門用於 Claude Code 使用。

#### 針對團隊和組織

1. **Claude for Teams 或 Enterprise** (建議)：訂閱 [Claude for Teams](https://claude.com/pricing#team-&-enterprise) 或 [Claude for Enterprise](https://anthropic.com/contact-sales)，以獲得集中式帳單、團隊管理以及對 Claude Code 和網頁版 Claude 的存取。團隊成員使用其 Claude.ai 帳戶登入。
2. **Claude Console 與團隊帳單**：設定共用的 [Claude Console](https://console.anthropic.com) 組織，並使用團隊帳單。邀請團隊成員並指派角色以進行使用情況追蹤。
3. **雲端提供商**：設定 Claude Code 以使用 [Amazon Bedrock、Google Vertex AI 或 Microsoft Foundry](/zh-TW/third-party-integrations)，以便與您現有的雲端基礎結構進行部署。

### 安裝特定版本

原生安裝程式接受特定版本號或發行頻道 (`latest` 或 `stable`)。您在安裝時選擇的頻道將成為自動更新的預設值。如需詳細資訊，請查看 [設定發行頻道](#configure-release-channel)。

若要安裝最新版本 (預設)：

<Tabs>
  <Tab title="macOS、Linux、WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```
  </Tab>
</Tabs>

若要安裝穩定版本：

<Tabs>
  <Tab title="macOS、Linux、WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s stable
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) stable
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd stable && del install.cmd
    ```
  </Tab>
</Tabs>

若要安裝特定版本號：

<Tabs>
  <Tab title="macOS、Linux、WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 1.0.58 && del install.cmd
    ```
  </Tab>
</Tabs>

### 二進位完整性和程式碼簽署

* 所有平台的 SHA256 校驗和都發佈在發行版本清單中，目前位於 `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json` (範例：將 `{VERSION}` 替換為 `2.0.30`)
* 簽署的二進位檔案分佈在以下平台上：
  * macOS：由'Anthropic PBC'簽署並由 Apple 公證
  * Windows：由'Anthropic, PBC'簽署

## NPM 安裝 (已棄用)

NPM 安裝已棄用。盡可能使用 [原生安裝](#installation) 方法。若要將現有的 npm 安裝遷移到原生安裝，請執行 `claude install`。

**全域 npm 安裝**

```sh  theme={null}
npm install -g @anthropic-ai/claude-code
```

<Warning>
  請勿使用 `sudo npm install -g`，因為這可能導致權限問題和安全風險。
  如果您遇到權限錯誤，請查看 [疑難排解權限錯誤](/zh-TW/troubleshooting#command-not-found-claude-or-permission-errors) 以獲得建議的解決方案。
</Warning>

## Windows 設定

**選項 1：WSL 內的 Claude Code**

* 支援 WSL 1 和 WSL 2
* WSL 2 支援 [沙箱](/zh-TW/sandboxing) 以增強安全性。WSL 1 不支援沙箱。

**選項 2：使用 Git Bash 在原生 Windows 上執行 Claude Code**

* 需要 [Git for Windows](https://git-scm.com/downloads/win)
* 對於可攜式 Git 安裝，請指定您的 `bash.exe` 的路徑：
  ```powershell  theme={null}
  $env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
  ```

## 更新 Claude Code

### 自動更新

Claude Code 會自動保持最新狀態，以確保您擁有最新的功能和安全修補程式。

* **更新檢查**：在啟動時和執行時定期執行
* **更新程序**：在背景自動下載和安裝
* **通知**：安裝更新時您會看到通知
* **套用更新**：更新在您下次啟動 Claude Code 時生效

<Note>
  Homebrew 和 WinGet 安裝不會自動更新。使用 `brew upgrade claude-code` 或 `winget upgrade Anthropic.ClaudeCode` 以手動更新。

  **已知問題**：Claude Code 可能會在新版本在這些套件管理員中可用之前通知您有更新。如果升級失敗，請稍候並稍後重試。
</Note>

### 設定發行頻道

使用 `autoUpdatesChannel` 設定來設定 Claude Code 針對自動更新和 `claude update` 遵循的發行頻道：

* `"latest"` (預設)：在新功能發佈時立即接收
* `"stable"`：使用通常約一週舊的版本，跳過有重大迴歸的發行版本

透過 `/config` → **自動更新頻道** 進行設定，或將其新增到您的 [settings.json 檔案](/zh-TW/settings)：

```json  theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

對於企業部署，您可以使用 [受管設定](/zh-TW/settings#settings-files) 在整個組織中強制執行一致的發行頻道。

### 停用自動更新

在您的 shell 或 [settings.json 檔案](/zh-TW/settings) 中設定 `DISABLE_AUTOUPDATER` 環境變數：

```bash  theme={null}
export DISABLE_AUTOUPDATER=1
```

### 手動更新

```bash  theme={null}
claude update
```

## 解除安裝 Claude Code

如果您需要解除安裝 Claude Code，請按照您的安裝方法的說明進行操作。

### 原生安裝

移除 Claude Code 二進位檔案和版本檔案：

**macOS、Linux、WSL：**

```bash  theme={null}
rm -f ~/.local/bin/claude
rm -rf ~/.local/share/claude
```

**Windows PowerShell：**

```powershell  theme={null}
Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
```

**Windows CMD：**

```batch  theme={null}
del "%USERPROFILE%\.local\bin\claude.exe"
rmdir /s /q "%USERPROFILE%\.local\share\claude"
```

### Homebrew 安裝

```bash  theme={null}
brew uninstall --cask claude-code
```

### WinGet 安裝

```powershell  theme={null}
winget uninstall Anthropic.ClaudeCode
```

### NPM 安裝

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### 清理設定檔案 (選用)

<Warning>
  移除設定檔案將刪除您的所有設定、允許的工具、MCP 伺服器設定和工作階段歷史記錄。
</Warning>

若要移除 Claude Code 設定和快取資料：

**macOS、Linux、WSL：**

```bash  theme={null}
# 移除使用者設定和狀態
rm -rf ~/.claude
rm ~/.claude.json

# 移除專案特定設定 (從您的專案目錄執行)
rm -rf .claude
rm -f .mcp.json
```

**Windows PowerShell：**

```powershell  theme={null}
# 移除使用者設定和狀態
Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

# 移除專案特定設定 (從您的專案目錄執行)
Remove-Item -Path ".claude" -Recurse -Force
Remove-Item -Path ".mcp.json" -Force
```

**Windows CMD：**

```batch  theme={null}
REM 移除使用者設定和狀態
rmdir /s /q "%USERPROFILE%\.claude"
del "%USERPROFILE%\.claude.json"

REM 移除專案特定設定 (從您的專案目錄執行)
rmdir /s /q ".claude"
del ".mcp.json"
```
