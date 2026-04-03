> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 進階設定

> Claude Code 的系統需求、平台特定安裝、版本管理和卸載。

本頁涵蓋系統需求、平台特定安裝詳情、更新和卸載。如需首次會話的引導式逐步說明，請參閱[快速入門](/zh-TW/quickstart)。如果您從未使用過終端機，請參閱[終端機指南](/zh-TW/terminal-guide)。

## 系統需求

Claude Code 在以下平台和配置上運行：

* **作業系統**：
  * macOS 13.0+
  * Windows 10 1809+ 或 Windows Server 2019+
  * Ubuntu 20.04+
  * Debian 10+
  * Alpine Linux 3.19+
* **硬體**：4 GB+ RAM
* **網路**：需要網際網路連線。請參閱[網路配置](/zh-TW/network-config#network-access-requirements)。
* **Shell**：Bash、Zsh、PowerShell 或 CMD。在 Windows 上，需要 [Git for Windows](https://git-scm.com/downloads/win)。
* **位置**：[Anthropic 支援的國家](https://www.anthropic.com/supported-countries)

### 其他依賴項

* **ripgrep**：通常包含在 Claude Code 中。如果搜尋失敗，請參閱[搜尋疑難排解](/zh-TW/troubleshooting#search-and-discovery-issues)。

## 安裝 Claude Code

<Tip>
  偏好圖形介面？[桌面應用程式](/zh-TW/desktop-quickstart)讓您無需終端機即可使用 Claude Code。下載適用於 [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) 或 [Windows](https://claude.com/download?utm_source=claude_code\&utm_medium=docs) 的版本。

  初次使用終端機？請參閱[終端機指南](/zh-TW/terminal-guide)以取得逐步說明。
</Tip>

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

    If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. Use the PowerShell command above instead. Your prompt shows `PS C:\` when you're in PowerShell.

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

安裝完成後，在您要使用的專案中開啟終端機並啟動 Claude Code：

```bash  theme={null}
claude
```

如果您在安裝期間遇到任何問題，請參閱[疑難排解指南](/zh-TW/troubleshooting)。

### 在 Windows 上設定

Windows 上的 Claude Code 需要 [Git for Windows](https://git-scm.com/downloads/win) 或 WSL。您可以從 PowerShell、CMD 或 Git Bash 啟動 `claude`。Claude Code 在內部使用 Git Bash 來執行命令。您不需要以系統管理員身分執行 PowerShell。

**選項 1：使用 Git Bash 的原生 Windows**

安裝 [Git for Windows](https://git-scm.com/downloads/win)，然後從 PowerShell 或 CMD 執行安裝命令。

如果 Claude Code 找不到您的 Git Bash 安裝，請在您的 [settings.json 檔案](/zh-TW/settings)中設定路徑：

```json  theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

Claude Code 也可以在 Windows 上以選擇加入預覽的方式原生執行 PowerShell。請參閱 [PowerShell tool](/zh-TW/tools-reference#powershell-tool) 以了解設定和限制。

**選項 2：WSL**

支援 WSL 1 和 WSL 2。WSL 2 支援[沙箱](/zh-TW/sandboxing)以增強安全性。WSL 1 不支援沙箱。

### Alpine Linux 和 musl 型發行版

Alpine 和其他 musl/uClibc 型發行版上的原生安裝程式需要 `libgcc`、`libstdc++` 和 `ripgrep`。使用您的發行版套件管理員安裝這些，然後設定 `USE_BUILTIN_RIPGREP=0`。

此範例在 Alpine 上安裝所需的套件：

```bash  theme={null}
apk add libgcc libstdc++ ripgrep
```

然後在您的 [`settings.json`](/zh-TW/settings#available-settings) 檔案中將 `USE_BUILTIN_RIPGREP` 設定為 `0`：

```json  theme={null}
{
  "env": {
    "USE_BUILTIN_RIPGREP": "0"
  }
}
```

## 驗證您的安裝

安裝後，確認 Claude Code 正常運作：

```bash  theme={null}
claude --version
```

如需更詳細的安裝和配置檢查，請執行 [`claude doctor`](/zh-TW/troubleshooting#get-more-help)：

```bash  theme={null}
claude doctor
```

## 驗證身份

Claude Code 需要 Pro、Max、Team、Enterprise 或 Console 帳戶。免費的 Claude.ai 方案不包括 Claude Code 存取權。您也可以透過第三方 API 提供者（如 [Amazon Bedrock](/zh-TW/amazon-bedrock)、[Google Vertex AI](/zh-TW/google-vertex-ai) 或 [Microsoft Foundry](/zh-TW/microsoft-foundry)）使用 Claude Code。

安裝後，執行 `claude` 並按照瀏覽器提示登入。請參閱[驗證](/zh-TW/authentication)以了解所有帳戶類型和團隊設定選項。

## 更新 Claude Code

原生安裝會在背景自動更新。您可以[配置發行版本通道](#configure-release-channel)來控制您是立即接收更新還是按延遲穩定時間表接收，或[完全停用自動更新](#disable-auto-updates)。Homebrew 和 WinGet 安裝需要手動更新。

### 自動更新

Claude Code 在啟動時和執行期間定期檢查更新。更新會在背景下載和安裝，然後在您下次啟動 Claude Code 時生效。

<Note>
  Homebrew 和 WinGet 安裝不會自動更新。使用 `brew upgrade claude-code` 或 `winget upgrade Anthropic.ClaudeCode` 手動更新。

  **已知問題**：Claude Code 可能會在新版本在這些套件管理員中可用之前通知您有更新。如果升級失敗，請稍候並稍後重試。

  Homebrew 在升級後會將舊版本保留在磁碟上。定期執行 `brew cleanup claude-code` 以回收磁碟空間。
</Note>

### 配置發行版本通道

使用 `autoUpdatesChannel` 設定控制 Claude Code 為自動更新和 `claude update` 遵循的發行版本通道：

* `"latest"`，預設值：在新功能發佈時立即接收
* `"stable"`：使用通常約一週舊的版本，跳過有重大迴歸的發佈

透過 `/config` → **自動更新通道**配置此項，或將其新增到您的 [settings.json 檔案](/zh-TW/settings)：

```json  theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

對於企業部署，您可以使用[受管設定](/zh-TW/permissions#managed-settings)在整個組織中強制執行一致的發行版本通道。

### 停用自動更新

在您的 [`settings.json`](/zh-TW/settings#available-settings) 檔案的 `env` 鍵中將 `DISABLE_AUTOUPDATER` 設定為 `"1"`：

```json  theme={null}
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

### 手動更新

若要立即套用更新而不等待下一次背景檢查，請執行：

```bash  theme={null}
claude update
```

## 進階安裝選項

這些選項適用於版本固定、從 npm 遷移和驗證二進位檔案完整性。

### 安裝特定版本

原生安裝程式接受特定版本號或發行版本通道（`latest` 或 `stable`）。您在安裝時選擇的通道將成為自動更新的預設值。請參閱[配置發行版本通道](#configure-release-channel)以取得更多資訊。

若要安裝最新版本（預設）：

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
    curl -fsSL https://claude.ai/install.sh | bash -s 2.1.89
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 2.1.89
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 2.1.89 && del install.cmd
    ```
  </Tab>
</Tabs>

### 已棄用的 npm 安裝

npm 安裝已棄用。原生安裝程式更快、不需要依賴項，並在背景自動更新。盡可能使用[原生安裝](#install-claude-code)方法。

#### 從 npm 遷移到原生

如果您之前使用 npm 安裝了 Claude Code，請切換到原生安裝程式：

```bash  theme={null}
# 安裝原生二進位檔案
curl -fsSL https://claude.ai/install.sh | bash

# 移除舊的 npm 安裝
npm uninstall -g @anthropic-ai/claude-code
```

您也可以從現有的 npm 安裝執行 `claude install` 以在其旁邊安裝原生二進位檔案，然後移除 npm 版本。

#### 使用 npm 安裝

如果您因相容性原因需要 npm 安裝，您必須安裝 [Node.js 18+](https://nodejs.org/en/download)。全域安裝套件：

```bash  theme={null}
npm install -g @anthropic-ai/claude-code
```

<Warning>
  請勿使用 `sudo npm install -g`，因為這可能導致權限問題和安全風險。如果您遇到權限錯誤，請參閱[疑難排解權限錯誤](/zh-TW/troubleshooting#permission-errors-during-installation)。
</Warning>

### 二進位檔案完整性和程式碼簽署

每個發佈都會發佈一個 `manifest.json`，其中包含每個平台二進位檔案的 SHA256 校驗和。該資訊清單使用 Anthropic GPG 金鑰簽署，因此驗證資訊清單上的簽名可以傳遞地驗證它列出的每個二進位檔案。

#### 驗證資訊清單簽名

步驟 1-3 需要具有 `gpg` 和 `curl` 的 POSIX shell。在 Windows 上，在 Git Bash 或 WSL 中執行它們。步驟 4 包括 PowerShell 選項。

<Steps>
  <Step title="下載並匯入公開金鑰">
    發佈簽署金鑰發佈在固定 URL。

    ```bash  theme={null}
    curl -fsSL https://downloads.claude.ai/keys/claude-code.asc | gpg --import
    ```

    顯示匯入金鑰的指紋。

    ```bash  theme={null}
    gpg --fingerprint security@anthropic.com
    ```

    確認輸出包含此指紋：

    ```text  theme={null}
    31DD DE24 DDFA B679 F42D  7BD2 BAA9 29FF 1A7E CACE
    ```
  </Step>

  <Step title="下載資訊清單和簽名">
    將 `VERSION` 設定為您要驗證的發佈。

    ```bash  theme={null}
    REPO=https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases
    VERSION=2.1.89
    curl -fsSLO "$REPO/$VERSION/manifest.json"
    curl -fsSLO "$REPO/$VERSION/manifest.json.sig"
    ```
  </Step>

  <Step title="驗證簽名">
    驗證分離的簽名對比資訊清單。

    ```bash  theme={null}
    gpg --verify manifest.json.sig manifest.json
    ```

    有效的結果報告 `Good signature from "Anthropic Claude Code Release Signing <security@anthropic.com>"`。

    `gpg` 也會為任何新匯入的金鑰列印 `WARNING: This key is not certified with a trusted signature!`。這是預期的。`Good signature` 行確認密碼檢查已通過。第 1 步中的指紋比較確認金鑰本身是真實的。
  </Step>

  <Step title="根據資訊清單檢查二進位檔案">
    將您下載的二進位檔案的 SHA256 校驗和與 `manifest.json` 中 `platforms.<platform>.checksum` 下列出的值進行比較。

    <Tabs>
      <Tab title="Linux">
        ```bash  theme={null}
        sha256sum claude
        ```
      </Tab>

      <Tab title="macOS">
        ```bash  theme={null}
        shasum -a 256 claude
        ```
      </Tab>

      <Tab title="Windows PowerShell">
        ```powershell  theme={null}
        (Get-FileHash claude.exe -Algorithm SHA256).Hash.ToLower()
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>

<Note>
  資訊清單簽名適用於 `2.1.89` 及以後的發佈。較早的發佈在 `manifest.json` 中發佈校驗和，但沒有分離的簽名。
</Note>

#### 平台程式碼簽名

除了簽署的資訊清單外，個別二進位檔案在支援的地方還帶有平台原生程式碼簽名。

* **macOS**：由「Anthropic PBC」簽署並由 Apple 公證。使用 `codesign --verify --verbose ./claude` 驗證。
* **Windows**：由「Anthropic, PBC」簽署。使用 `Get-AuthenticodeSignature .\claude.exe` 驗證。
* **Linux**：使用上面的資訊清單簽名來驗證完整性。Linux 二進位檔案不是單獨程式碼簽署的。

## 卸載 Claude Code

若要移除 Claude Code，請按照您的安裝方法的說明進行。

### 原生安裝

移除 Claude Code 二進位檔案和版本檔案：

<Tabs>
  <Tab title="macOS、Linux、WSL">
    ```bash  theme={null}
    rm -f ~/.local/bin/claude
    rm -rf ~/.local/share/claude
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
    Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
    ```
  </Tab>
</Tabs>

### Homebrew 安裝

移除 Homebrew cask：

```bash  theme={null}
brew uninstall --cask claude-code
```

### WinGet 安裝

移除 WinGet 套件：

```powershell  theme={null}
winget uninstall Anthropic.ClaudeCode
```

### npm

移除全域 npm 套件：

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### 移除配置檔案

<Warning>
  移除配置檔案將刪除您的所有設定、允許的工具、MCP 伺服器配置和會話歷史記錄。
</Warning>

若要移除 Claude Code 設定和快取資料：

<Tabs>
  <Tab title="macOS、Linux、WSL">
    ```bash  theme={null}
    # 移除使用者設定和狀態
    rm -rf ~/.claude
    rm ~/.claude.json

    # 移除專案特定設定（從您的專案目錄執行）
    rm -rf .claude
    rm -f .mcp.json
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    # 移除使用者設定和狀態
    Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
    Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

    # 移除專案特定設定（從您的專案目錄執行）
    Remove-Item -Path ".claude" -Recurse -Force
    Remove-Item -Path ".mcp.json" -Force
    ```
  </Tab>
</Tabs>
