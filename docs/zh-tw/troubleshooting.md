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

# 故障排除

> 發現 Claude Code 安裝和使用中常見問題的解決方案。

## 故障排除安裝問題

<Tip>
  如果您想完全跳過終端，[Claude Code 桌面應用](/zh-TW/desktop-quickstart)讓您可以通過圖形界面安裝和使用 Claude Code。下載適用於 [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) 或 [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs) 的版本，無需任何命令行設置即可開始編碼。
</Tip>

找到您看到的錯誤消息或症狀：

| 您看到的內容                                                     | 解決方案                                                                                  |
| :--------------------------------------------------------- | :------------------------------------------------------------------------------------ |
| `command not found: claude` 或 `'claude' is not recognized` | [修復您的 PATH](#command-not-found-claude-after-installation)                             |
| `syntax error near unexpected token '<'`                   | [安裝腳本返回 HTML](#install-script-returns-html-instead-of-a-shell-script)                 |
| `curl: (56) Failure writing output to destination`         | [先下載腳本，然後運行](#curl-56-failure-writing-output-to-destination)                          |
| 在 Linux 上安裝期間 `Killed`                                     | [為低內存服務器添加交換空間](#install-killed-on-low-memory-linux-servers)                          |
| `TLS connect error` 或 `SSL/TLS secure channel`             | [更新 CA 證書](#tls-or-ssl-connection-errors)                                             |
| `Failed to fetch version` 或無法連接下載服務器                       | [檢查網絡和代理設置](#check-network-connectivity)                                              |
| `irm is not recognized` 或 `&& is not valid`                | [為您的 shell 使用正確的命令](#windows-irm-or--not-recognized)                                  |
| `Claude Code on Windows requires git-bash`                 | [安裝或配置 Git Bash](#windows-claude-code-on-windows-requires-git-bash)                   |
| `Error loading shared library`                             | [您的系統安裝了錯誤的二進制變體](#linux-wrong-binary-variant-installed-muslglibc-mismatch)           |
| Linux 上的 `Illegal instruction`                             | [架構不匹配](#illegal-instruction-on-linux)                                                |
| macOS 上的 `dyld: cannot load` 或 `Abort trap`                | [二進制不兼容](#dyld-cannot-load-on-macos)                                                  |
| `Invoke-Expression: Missing argument in parameter list`    | [安裝腳本返回 HTML](#install-script-returns-html-instead-of-a-shell-script)                 |
| `App unavailable in region`                                | Claude Code 在您的國家/地區不可用。請參閱[支持的國家/地區](https://www.anthropic.com/supported-countries)。 |
| `unable to get local issuer certificate`                   | [配置企業 CA 證書](#tls-or-ssl-connection-errors)                                           |
| `OAuth error` 或 `403 Forbidden`                            | [修復身份驗證](#authentication-issues)                                                      |

如果您的問題未列出，請按照這些診斷步驟進行操作。

## 調試安裝問題

### 檢查網絡連接

安裝程序從 `storage.googleapis.com` 下載。驗證您可以訪問它：

```bash  theme={null}
curl -sI https://storage.googleapis.com
```

如果失敗，您的網絡可能阻止了連接。常見原因：

* 企業防火牆或代理阻止 Google Cloud Storage
* 區域網絡限制：嘗試使用 VPN 或替代網絡
* TLS/SSL 問題：更新您系統的 CA 證書，或檢查是否配置了 `HTTPS_PROXY`

如果您在企業代理後面，在安裝前設置 `HTTPS_PROXY` 和 `HTTP_PROXY` 為您的代理地址。如果您不知道代理 URL，請向您的 IT 團隊詢問，或檢查您的瀏覽器代理設置。

此示例設置兩個代理變量，然後通過您的代理運行安裝程序：

```bash  theme={null}
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
curl -fsSL https://claude.ai/install.sh | bash
```

### 驗證您的 PATH

如果安裝成功但運行 `claude` 時出現 `command not found` 或 `not recognized` 錯誤，安裝目錄不在您的 PATH 中。您的 shell 在 PATH 中列出的目錄中搜索程序，安裝程序在 macOS/Linux 上將 `claude` 放在 `~/.local/bin/claude`，或在 Windows 上放在 `%USERPROFILE%\.local\bin\claude.exe`。

通過列出您的 PATH 條目並過濾 `local/bin` 來檢查安裝目錄是否在您的 PATH 中：

<Tabs>
  <Tab title="macOS/Linux">
    ```bash  theme={null}
    echo $PATH | tr ':' '\n' | grep local/bin
    ```

    如果沒有輸出，該目錄缺失。將其添加到您的 shell 配置：

    ```bash  theme={null}
    # Zsh (macOS 默認)
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc

    # Bash (Linux 默認)
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
    ```

    或者，關閉並重新打開您的終端。

    驗證修復是否有效：

    ```bash  theme={null}
    claude --version
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    $env:PATH -split ';' | Select-String 'local\\bin'
    ```

    如果沒有輸出，將安裝目錄添加到您的用戶 PATH：

    ```powershell  theme={null}
    $currentPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
    [Environment]::SetEnvironmentVariable('PATH', "$currentPath;$env:USERPROFILE\.local\bin", 'User')
    ```

    重新啟動您的終端以使更改生效。

    驗證修復是否有效：

    ```powershell  theme={null}
    claude --version
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    echo %PATH% | findstr /i "local\bin"
    ```

    如果沒有輸出，打開系統設置，轉到環境變量，並將 `%USERPROFILE%\.local\bin` 添加到您的用戶 PATH 變量。重新啟動您的終端。

    驗證修復是否有效：

    ```batch  theme={null}
    claude --version
    ```
  </Tab>
</Tabs>

### 檢查衝突的安裝

多個 Claude Code 安裝可能導致版本不匹配或意外行為。檢查已安裝的內容：

<Tabs>
  <Tab title="macOS/Linux">
    列出在您的 PATH 中找到的所有 `claude` 二進制文件：

    ```bash  theme={null}
    which -a claude
    ```

    檢查是否存在本機安裝程序和 npm 版本：

    ```bash  theme={null}
    ls -la ~/.local/bin/claude
    ```

    ```bash  theme={null}
    ls -la ~/.claude/local/
    ```

    ```bash  theme={null}
    npm -g ls @anthropic-ai/claude-code 2>/dev/null
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    where.exe claude
    Test-Path "$env:LOCALAPPDATA\Claude Code\claude.exe"
    ```
  </Tab>
</Tabs>

如果您找到多個安裝，只保留一個。建議使用 `~/.local/bin/claude` 的本機安裝。刪除任何額外的安裝：

卸載 npm 全局安裝：

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

在 macOS 上刪除 Homebrew 安裝：

```bash  theme={null}
brew uninstall --cask claude-code
```

### 檢查目錄權限

安裝程序需要對 `~/.local/bin/` 和 `~/.claude/` 的寫入訪問權限。如果安裝失敗並出現權限錯誤，檢查這些目錄是否可寫：

```bash  theme={null}
test -w ~/.local/bin && echo "writable" || echo "not writable"
test -w ~/.claude && echo "writable" || echo "not writable"
```

如果任一目錄不可寫，創建安裝目錄並將您的用戶設置為所有者：

```bash  theme={null}
sudo mkdir -p ~/.local/bin
sudo chown -R $(whoami) ~/.local
```

### 驗證二進制文件是否有效

如果 `claude` 已安裝但在啟動時崩潰或掛起，運行這些檢查以縮小原因範圍。

確認二進制文件存在且可執行：

```bash  theme={null}
ls -la $(which claude)
```

在 Linux 上，檢查缺失的共享庫。如果 `ldd` 顯示缺失的庫，您可能需要安裝系統包。在 Alpine Linux 和其他基於 musl 的發行版上，請參閱 [Alpine Linux 設置](/zh-TW/setup#alpine-linux-and-musl-based-distributions)。

```bash  theme={null}
ldd $(which claude) | grep "not found"
```

運行快速健全性檢查，確認二進制文件可以執行：

```bash  theme={null}
claude --version
```

## 常見安裝問題

這些是最常見的安裝問題及其解決方案。

### 安裝腳本返回 HTML 而不是 shell 腳本

運行安裝命令時，您可能會看到以下錯誤之一：

```text  theme={null}
bash: line 1: syntax error near unexpected token `<'
bash: line 1: `<!DOCTYPE html>'
```

在 PowerShell 上，同樣的問題顯示為：

```text  theme={null}
Invoke-Expression: Missing argument in parameter list.
```

這意味著安裝 URL 返回了 HTML 頁面而不是安裝腳本。如果 HTML 頁面顯示"App unavailable in region"，Claude Code 在您的國家/地區不可用。請參閱[支持的國家/地區](https://www.anthropic.com/supported-countries)。

否則，這可能由於網絡問題、區域路由或臨時服務中斷而發生。

**解決方案：**

1. **使用替代安裝方法**：

   在 macOS 或 Linux 上，通過 Homebrew 安裝：

   ```bash  theme={null}
   brew install --cask claude-code
   ```

   在 Windows 上，通過 WinGet 安裝：

   ```powershell  theme={null}
   winget install Anthropic.ClaudeCode
   ```

2. **幾分鐘後重試**：該問題通常是暫時的。等待並重試原始命令。

### 安裝後 `command not found: claude`

安裝完成但 `claude` 不起作用。確切的錯誤因平台而異：

| 平台          | 錯誤消息                                                                   |
| :---------- | :--------------------------------------------------------------------- |
| macOS       | `zsh: command not found: claude`                                       |
| Linux       | `bash: claude: command not found`                                      |
| Windows CMD | `'claude' is not recognized as an internal or external command`        |
| PowerShell  | `claude : The term 'claude' is not recognized as the name of a cmdlet` |

這意味著安裝目錄不在您的 shell 搜索路徑中。請參閱[驗證您的 PATH](#verify-your-path) 以了解每個平台上的修復。

### `curl: (56) Failure writing output to destination`

`curl ... | bash` 命令下載腳本並使用管道 (`|`) 將其直接傳遞給 Bash 執行。此錯誤意味著連接在腳本完成下載前中斷。常見原因包括網絡中斷、下載被中途阻止或系統資源限制。

**解決方案：**

1. **檢查網絡穩定性**：Claude Code 二進制文件託管在 Google Cloud Storage 上。測試您是否可以訪問它：
   ```bash  theme={null}
   curl -fsSL https://storage.googleapis.com -o /dev/null
   ```
   如果命令無聲完成，您的連接良好，問題可能是間歇性的。重試安裝命令。如果您看到錯誤，您的網絡可能阻止了下載。

2. **嘗試替代安裝方法**：

   在 macOS 或 Linux 上：

   ```bash  theme={null}
   brew install --cask claude-code
   ```

   在 Windows 上：

   ```powershell  theme={null}
   winget install Anthropic.ClaudeCode
   ```

### TLS 或 SSL 連接錯誤

像 `curl: (35) TLS connect error`、`schannel: next InitializeSecurityContext failed` 或 PowerShell 的 `Could not establish trust relationship for the SSL/TLS secure channel` 這樣的錯誤表示 TLS 握手失敗。

**解決方案：**

1. **更新您的系統 CA 證書**：

   在 Ubuntu/Debian 上：

   ```bash  theme={null}
   sudo apt-get update && sudo apt-get install ca-certificates
   ```

   在 macOS 上通過 Homebrew：

   ```bash  theme={null}
   brew install ca-certificates
   ```

2. **在 Windows 上，在運行安裝程序前在 PowerShell 中啟用 TLS 1.2**：
   ```powershell  theme={null}
   [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
   irm https://claude.ai/install.ps1 | iex
   ```

3. **檢查代理或防火牆干擾**：執行 TLS 檢查的企業代理可能導致這些錯誤，包括 `unable to get local issuer certificate`。將 `NODE_EXTRA_CA_CERTS` 設置為您的企業 CA 證書包：
   ```bash  theme={null}
   export NODE_EXTRA_CA_CERTS=/path/to/corporate-ca.pem
   ```
   如果您沒有證書文件，請向您的 IT 團隊索取。您也可以嘗試直接連接以確認代理是原因。

### `Failed to fetch version from storage.googleapis.com`

安裝程序無法訪問下載服務器。這通常意味著 `storage.googleapis.com` 在您的網絡上被阻止。

**解決方案：**

1. **直接測試連接**：
   ```bash  theme={null}
   curl -sI https://storage.googleapis.com
   ```

2. **如果在代理後面**，設置 `HTTPS_PROXY` 以便安裝程序可以通過它路由。有關詳細信息，請參閱[代理配置](/zh-TW/network-config#proxy-configuration)。
   ```bash  theme={null}
   export HTTPS_PROXY=http://proxy.example.com:8080
   curl -fsSL https://claude.ai/install.sh | bash
   ```

3. **如果在受限網絡上**，嘗試不同的網絡或 VPN，或使用替代安裝方法：

   在 macOS 或 Linux 上：

   ```bash  theme={null}
   brew install --cask claude-code
   ```

   在 Windows 上：

   ```powershell  theme={null}
   winget install Anthropic.ClaudeCode
   ```

### Windows：`irm` 或 `&&` 未被識別

如果您看到 `'irm' is not recognized` 或 `The token '&&' is not valid`，您正在為您的 shell 運行錯誤的命令。

* **`irm` 未被識別**：您在 CMD 中，而不是 PowerShell。您有兩個選項：

  通過在開始菜單中搜索"PowerShell"打開 PowerShell，然後運行原始安裝命令：

  ```powershell  theme={null}
  irm https://claude.ai/install.ps1 | iex
  ```

  或留在 CMD 中並改用 CMD 安裝程序：

  ```batch  theme={null}
  curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
  ```

* **`&&` 無效**：您在 PowerShell 中但運行了 CMD 安裝程序命令。使用 PowerShell 安裝程序：
  ```powershell  theme={null}
  irm https://claude.ai/install.ps1 | iex
  ```

### 在低內存 Linux 服務器上安裝被殺死

如果在 VPS 或雲實例上安裝期間看到 `Killed`：

```text  theme={null}
Setting up Claude Code...
Installing Claude Code native build latest...
bash: line 142: 34803 Killed    "$binary_path" install ${TARGET:+"$TARGET"}
```

Linux OOM 殺手終止了該進程，因為系統內存不足。Claude Code 至少需要 4 GB 可用 RAM。

**解決方案：**

1. **添加交換空間**，如果您的服務器 RAM 有限。交換使用磁盤空間作為溢出內存，即使物理 RAM 較低也能讓安裝完成。

   創建 2 GB 交換文件並啟用它：

   ```bash  theme={null}
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

   然後重試安裝：

   ```bash  theme={null}
   curl -fsSL https://claude.ai/install.sh | bash
   ```

2. **關閉其他進程**以在安裝前釋放內存。

3. **使用更大的實例**，如果可能的話。Claude Code 至少需要 4 GB RAM。

### 在 Docker 中安裝掛起

在 Docker 容器中安裝 Claude Code 時，以 root 身份安裝到 `/` 可能導致掛起。

**解決方案：**

1. **在運行安裝程序前設置工作目錄**。從 `/` 運行時，安裝程序掃描整個文件系統，導致過度的內存使用。設置 `WORKDIR` 將掃描限制在小目錄：
   ```dockerfile  theme={null}
   WORKDIR /tmp
   RUN curl -fsSL https://claude.ai/install.sh | bash
   ```

2. **增加 Docker 內存限制**，如果使用 Docker Desktop：
   ```bash  theme={null}
   docker build --memory=4g .
   ```

### Windows：Claude Desktop 覆蓋 `claude` CLI 命令

如果您安裝了舊版本的 Claude Desktop，它可能在 `WindowsApps` 目錄中註冊一個 `Claude.exe`，該目錄在 PATH 中優先於 Claude Code CLI。運行 `claude` 會打開桌面應用而不是 CLI。

更新 Claude Desktop 到最新版本以修復此問題。

### Windows："Claude Code on Windows requires git-bash"

Windows 上的 Claude Code 需要 [Git for Windows](https://git-scm.com/downloads/win)，其中包括 Git Bash。

**如果未安裝 Git**，從 [git-scm.com/downloads/win](https://git-scm.com/downloads/win) 下載並安裝它。在設置期間，選擇"Add to PATH"。安裝後重新啟動您的終端。

**如果已安裝 Git** 但 Claude Code 仍然找不到它，在您的 [settings.json 文件](/zh-TW/settings)中設置路徑：

```json  theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

如果您的 Git 安裝在其他地方，通過在 PowerShell 中運行 `where.exe git` 找到路徑，並使用該目錄中的 `bin\bash.exe` 路徑。

### Linux：安裝了錯誤的二進制變體（musl/glibc 不匹配）

如果在安裝後看到有關缺失共享庫的錯誤，如 `libstdc++.so.6` 或 `libgcc_s.so.1`，安裝程序可能為您的系統下載了錯誤的二進制變體。

```text  theme={null}
Error loading shared library libstdc++.so.6: No such file or directory
```

這可能發生在安裝了 musl 交叉編譯包的基於 glibc 的系統上，導致安裝程序誤檢測系統為 musl。

**解決方案：**

1. **檢查您的系統使用哪個 libc**：
   ```bash  theme={null}
   ldd /bin/ls | head -1
   ```
   如果它顯示 `linux-vdso.so` 或對 `/lib/x86_64-linux-gnu/` 的引用，您在 glibc 上。如果它顯示 `musl`，您在 musl 上。

2. **如果您在 glibc 上但得到了 musl 二進制文件**，刪除安裝並重新安裝。您也可以從 GCS 存儲桶 `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json` 手動下載正確的二進制文件。使用 `ldd /bin/ls` 和 `ls /lib/libc.musl*` 的輸出提交 [GitHub 問題](https://github.com/anthropics/claude-code/issues)。

3. **如果您實際上在 musl 上**（Alpine Linux），安裝所需的包：
   ```bash  theme={null}
   apk add libgcc libstdc++ ripgrep
   ```

### Linux 上的 `Illegal instruction`

如果安裝程序打印 `Illegal instruction` 而不是 OOM `Killed` 消息，下載的二進制文件與您的 CPU 架構不匹配。這通常發生在接收 x86 二進制文件的 ARM 服務器上，或在缺少所需指令集的較舊 CPU 上。

```text  theme={null}
bash: line 142: 2238232 Illegal instruction    "$binary_path" install ${TARGET:+"$TARGET"}
```

**解決方案：**

1. **驗證您的架構**：
   ```bash  theme={null}
   uname -m
   ```
   `x86_64` 表示 64 位 Intel/AMD，`aarch64` 表示 ARM64。如果二進制文件不匹配，[提交 GitHub 問題](https://github.com/anthropics/claude-code/issues)並附上輸出。

2. **嘗試替代安裝方法**，同時解決架構問題：
   ```bash  theme={null}
   brew install --cask claude-code
   ```

### macOS 上的 `dyld: cannot load`

如果在安裝期間看到 `dyld: cannot load` 或 `Abort trap: 6`，二進制文件與您的 macOS 版本或硬件不兼容。

```text  theme={null}
dyld: cannot load 'claude-2.1.42-darwin-x64' (load command 0x80000034 is unknown)
Abort trap: 6
```

**解決方案：**

1. **檢查您的 macOS 版本**：Claude Code 需要 macOS 13.0 或更高版本。打開 Apple 菜單並選擇"About This Mac"以檢查您的版本。

2. **更新 macOS**，如果您在較舊版本上。二進制文件使用較舊 macOS 版本不支持的加載命令。

3. **嘗試 Homebrew** 作為替代安裝方法：
   ```bash  theme={null}
   brew install --cask claude-code
   ```

### Windows 安裝問題：WSL 中的錯誤

您可能在 WSL 中遇到以下問題：

**OS/平台檢測問題**：如果在安裝期間收到錯誤，WSL 可能使用 Windows `npm`。嘗試：

* 在安裝前運行 `npm config set os linux`
* 使用 `npm install -g @anthropic-ai/claude-code --force --no-os-check` 安裝。不要使用 `sudo`。

**Node 未找到錯誤**：如果運行 `claude` 時看到 `exec: node: not found`，您的 WSL 環境可能使用 Windows 安裝的 Node.js。您可以使用 `which npm` 和 `which node` 確認這一點，它們應該指向以 `/usr/` 開頭的 Linux 路徑，而不是 `/mnt/c/`。要修復此問題，請嘗試通過您的 Linux 發行版的包管理器或通過 [`nvm`](https://github.com/nvm-sh/nvm) 安裝 Node。

**nvm 版本衝突**：如果您在 WSL 和 Windows 中都安裝了 nvm，在 WSL 中切換 Node 版本時可能會遇到版本衝突。這是因為 WSL 默認導入 Windows PATH，導致 Windows nvm/npm 優先於 WSL 安裝。

您可以通過以下方式識別此問題：

* 運行 `which npm` 和 `which node` - 如果它們指向 Windows 路徑（以 `/mnt/c/` 開頭），則使用 Windows 版本
* 在 WSL 中使用 nvm 切換 Node 版本後遇到損壞的功能

要解決此問題，修復您的 Linux PATH 以確保 Linux node/npm 版本優先：

**主要解決方案：確保 nvm 在您的 shell 中正確加載**

最常見的原因是 nvm 未在非交互式 shell 中加載。將以下內容添加到您的 shell 配置文件（`~/.bashrc`、`~/.zshrc` 等）：

```bash  theme={null}
# 如果存在，加載 nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
```

或在您的當前會話中直接運行：

```bash  theme={null}
source ~/.nvm/nvm.sh
```

**替代方案：調整 PATH 順序**

如果 nvm 正確加載但 Windows 路徑仍然優先，您可以在 shell 配置中明確將 Linux 路徑添加到 PATH 的前面：

```bash  theme={null}
export PATH="$HOME/.nvm/versions/node/$(node -v)/bin:$PATH"
```

<Warning>
  避免通過 `appendWindowsPath = false` 禁用 Windows PATH 導入，因為這會破壞從 WSL 調用 Windows 可執行文件的能力。同樣，如果您在 Windows 開發中使用 Node.js，避免從 Windows 卸載它。
</Warning>

### WSL2 sandbox 設置

[Sandboxing](/zh-TW/sandboxing) 在 WSL2 上受支持，但需要安裝額外的包。如果運行 `/sandbox` 時看到"Sandbox requires socat and bubblewrap"之類的錯誤，安裝依賴項：

<Tabs>
  <Tab title="Ubuntu/Debian">
    ```bash  theme={null}
    sudo apt-get install bubblewrap socat
    ```
  </Tab>

  <Tab title="Fedora">
    ```bash  theme={null}
    sudo dnf install bubblewrap socat
    ```
  </Tab>
</Tabs>

WSL1 不支持 sandboxing。如果您看到"Sandboxing requires WSL2"，您需要升級到 WSL2 或在不使用 sandboxing 的情況下運行 Claude Code。

### 安裝期間的權限錯誤

如果本機安裝程序因權限錯誤而失敗，目標目錄可能不可寫。請參閱[檢查目錄權限](#check-directory-permissions)。

如果您之前使用 npm 安裝並遇到 npm 特定的權限錯誤，切換到本機安裝程序：

```bash  theme={null}
curl -fsSL https://claude.ai/install.sh | bash
```

## 權限和身份驗證

這些部分涉及登錄失敗、令牌問題和權限提示行為。

### 重複的權限提示

如果您發現自己反覆批准相同的命令，您可以使用 `/permissions` 命令允許特定工具無需批准即可運行。請參閱[權限文檔](/zh-TW/permissions#manage-permissions)。

### 身份驗證問題

如果您遇到身份驗證問題：

1. 運行 `/logout` 完全登出
2. 關閉 Claude Code
3. 使用 `claude` 重新啟動並再次完成身份驗證過程

如果瀏覽器在登錄期間未自動打開，按 `c` 將 OAuth URL 複製到您的剪貼板，然後手動將其粘貼到您的瀏覽器中。

### OAuth 錯誤：無效代碼

如果您看到 `OAuth error: Invalid code. Please make sure the full code was copied`，登錄代碼已過期或在複製粘貼期間被截斷。

**解決方案：**

* 按 Enter 重試，並在瀏覽器打開後快速完成登錄
* 輸入 `c` 複製完整 URL，如果瀏覽器未自動打開
* 如果使用遠程/SSH 會話，瀏覽器可能在錯誤的機器上打開。複製終端中顯示的 URL 並在您的本地瀏覽器中打開它。

### 登錄後 403 Forbidden

如果登錄後看到 `API Error: 403 {"error":{"type":"forbidden","message":"Request not allowed"}}`：

* **Claude Pro/Max 用戶**：在 [claude.ai/settings](https://claude.ai/settings) 驗證您的訂閱是否有效
* **Console 用戶**：確認您的帳戶已由您的管理員分配"Claude Code"或"Developer"角色
* **在代理後面**：企業代理可能干擾 API 請求。有關代理設置，請參閱[網絡配置](/zh-TW/network-config)。

### OAuth 登錄在 WSL2 中失敗

如果 WSL 無法打開您的 Windows 瀏覽器，WSL2 中基於瀏覽器的登錄可能失敗。設置 `BROWSER` 環境變量：

```bash  theme={null}
export BROWSER="/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
claude
```

或手動複製 URL：當登錄提示出現時，按 `c` 複製 OAuth URL，然後將其粘貼到您的 Windows 瀏覽器中。

### "未登錄"或令牌已過期

如果 Claude Code 在會話後提示您再次登錄，您的 OAuth 令牌可能已過期。

運行 `/login` 重新進行身份驗證。如果這種情況經常發生，檢查您的系統時鐘是否準確，因為令牌驗證取決於正確的時間戳。

## 配置文件位置

Claude Code 在多個位置存儲配置：

| 文件                            | 目的                                                             |
| :---------------------------- | :------------------------------------------------------------- |
| `~/.claude/settings.json`     | 用戶設置（權限、hooks、模型覆蓋）                                            |
| `.claude/settings.json`       | 項目設置（簽入源代碼控制）                                                  |
| `.claude/settings.local.json` | 本地項目設置（未提交）                                                    |
| `~/.claude.json`              | 全局狀態（主題、OAuth、MCP 服務器）                                         |
| `.mcp.json`                   | 項目 MCP 服務器（簽入源代碼控制）                                            |
| `managed-mcp.json`            | [託管 MCP 服務器](/zh-TW/mcp#managed-mcp-configuration)             |
| 託管設置                          | [託管設置](/zh-TW/settings#settings-files)（服務器管理、MDM/OS 級別策略或基於文件） |

在 Windows 上，`~` 指您的用戶主目錄，例如 `C:\Users\YourName`。

有關配置這些文件的詳細信息，請參閱[設置](/zh-TW/settings)和 [MCP](/zh-TW/mcp)。

### 重置配置

要將 Claude Code 重置為默認設置，您可以刪除配置文件：

```bash  theme={null}
# 重置所有用戶設置和狀態
rm ~/.claude.json
rm -rf ~/.claude/

# 重置項目特定設置
rm -rf .claude/
rm .mcp.json
```

<Warning>
  這將刪除您的所有設置、MCP 服務器配置和會話歷史記錄。
</Warning>

## 性能和穩定性

這些部分涵蓋與資源使用、響應性和搜索行為相關的問題。

### 高 CPU 或內存使用

Claude Code 設計用於與大多數開發環境配合使用，但在處理大型代碼庫時可能消耗大量資源。如果您遇到性能問題：

1. 定期使用 `/compact` 減少上下文大小
2. 在主要任務之間關閉並重新啟動 Claude Code
3. 考慮將大型構建目錄添加到您的 `.gitignore` 文件

### 命令掛起或凍結

如果 Claude Code 似乎無響應：

1. 按 Ctrl+C 嘗試取消當前操作
2. 如果無響應，您可能需要關閉終端並重新啟動

### 搜索和發現問題

如果搜索工具、`@file` 提及、自定義代理和自定義 skills 不起作用，安裝系統 `ripgrep`：

```bash  theme={null}
# macOS (Homebrew)  
brew install ripgrep

# Windows (winget)
winget install BurntSushi.ripgrep.MSVC

# Ubuntu/Debian
sudo apt install ripgrep

# Alpine Linux
apk add ripgrep

# Arch Linux
pacman -S ripgrep
```

然後在您的[環境](/zh-TW/env-vars)中設置 `USE_BUILTIN_RIPGREP=0`。

### WSL 上的搜索速度慢或結果不完整

在 WSL 上[跨文件系統工作](https://learn.microsoft.com/en-us/windows/wsl/filesystems)時的磁盤讀取性能損失可能導致在 WSL 上使用 Claude Code 時匹配數少於預期。搜索仍然有效，但在本機文件系統上返回的結果較少。

<Note>
  在這種情況下，`/doctor` 將顯示搜索為正常。
</Note>

**解決方案：**

1. **提交更具體的搜索**：通過指定目錄或文件類型來減少搜索的文件數量："Search for JWT validation logic in the auth-service package"或"Find use of md5 hash in JS files"。

2. **將項目移動到 Linux 文件系統**：如果可能，確保您的項目位於 Linux 文件系統（`/home/`）而不是 Windows 文件系統（`/mnt/c/`）。

3. **改用本機 Windows**：考慮在 Windows 上本機運行 Claude Code 而不是通過 WSL，以獲得更好的文件系統性能。

## IDE 集成問題

如果 Claude Code 未連接到您的 IDE 或在 IDE 終端中表現異常，請嘗試以下解決方案。

### JetBrains IDE 在 WSL2 上未被檢測到

如果您在 WSL2 上使用 Claude Code 和 JetBrains IDE，並收到"No available IDEs detected"錯誤，這可能是由於 WSL2 的網絡配置或 Windows 防火牆阻止連接。

#### WSL2 網絡模式

WSL2 默認使用 NAT 網絡，這可能阻止 IDE 檢測。您有兩個選項：

**選項 1：配置 Windows 防火牆**（推薦）

1. 找到您的 WSL2 IP 地址：
   ```bash  theme={null}
   wsl hostname -I
   # 示例輸出：172.21.123.45
   ```

2. 以管理員身份打開 PowerShell 並創建防火牆規則：
   ```powershell  theme={null}
   New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
   ```
   根據步驟 1 中的 WSL2 子網調整 IP 範圍。

3. 重新啟動您的 IDE 和 Claude Code

**選項 2：切換到鏡像網絡**

添加到 Windows 用戶目錄中的 `.wslconfig`：

```ini  theme={null}
[wsl2]
networkingMode=mirrored
```

然後從 PowerShell 使用 `wsl --shutdown` 重新啟動 WSL。

<Note>
  這些網絡問題僅影響 WSL2。WSL1 直接使用主機的網絡，不需要這些配置。
</Note>

有關其他 JetBrains 配置提示，請參閱 [JetBrains IDE 指南](/zh-TW/jetbrains#plugin-settings)。

### 報告 Windows IDE 集成問題

如果您在 Windows 上遇到 IDE 集成問題，[創建一個問題](https://github.com/anthropics/claude-code/issues)並提供以下信息：

* 環境類型：本機 Windows (Git Bash) 或 WSL1/WSL2
* WSL 網絡模式（如適用）：NAT 或鏡像
* IDE 名稱和版本
* Claude Code 擴展/插件版本
* Shell 類型：Bash、Zsh、PowerShell 等

### JetBrains IDE 終端中的 Escape 鍵不起作用

如果您在 JetBrains 終端中使用 Claude Code，`Esc` 鍵未按預期中斷代理，這可能是由於 JetBrains 默認快捷鍵的衝突。

要修復此問題：

1. 轉到設置 → 工具 → 終端
2. 要么：
   * 取消選中"Move focus to the editor with Escape"，或
   * 點擊"Configure terminal keybindings"並刪除"Switch focus to Editor"快捷鍵
3. 應用更改

這允許 `Esc` 鍵正確中斷 Claude Code 操作。

## Markdown 格式問題

Claude Code 有時生成 markdown 文件，代碼圍欄上缺少語言標籤，這可能影響 GitHub、編輯器和文檔工具中的語法突出顯示和可讀性。

### 代碼塊中缺少語言標籤

如果您在生成的 markdown 中注意到這樣的代碼塊：

````markdown  theme={null}
```
function example() {
  return "hello";
}
```text
````

而不是正確標記的塊，如：

````markdown  theme={null}
```javascript
function example() {
  return "hello";
}
```text
````

**解決方案：**

1. **要求 Claude 添加語言標籤**：請求"Add appropriate language tags to all code blocks in this markdown file."

2. **使用後處理 hooks**：設置自動格式化 hooks 以檢測和添加缺失的語言標籤。有關示例，請參閱[編輯後自動格式化代碼](/zh-TW/hooks-guide#auto-format-code-after-edits)的 PostToolUse 格式化 hook。

3. **手動驗證**：生成 markdown 文件後，檢查它們是否有正確的代碼塊格式，如果需要，請求更正。

### 不一致的間距和格式

如果生成的 markdown 有過多的空行或不一致的間距：

**解決方案：**

1. **請求格式更正**：要求 Claude"Fix spacing and formatting issues in this markdown file."

2. **使用格式化工具**：設置 hooks 以在生成的 markdown 文件上運行 markdown 格式化程序，如 `prettier` 或自定義格式化腳本。

3. **指定格式化首選項**：在您的提示或項目[內存](/zh-TW/memory)文件中包含格式化要求。

### 減少 markdown 格式問題

要最小化格式問題：

* **在請求中明確**：要求"properly formatted markdown with language-tagged code blocks"
* **使用項目約定**：在 [`CLAUDE.md`](/zh-TW/memory) 中記錄您首選的 markdown 風格
* **設置驗證 hooks**：使用後處理 hooks 自動驗證和修復常見格式問題

## 獲取更多幫助

如果您遇到此處未涵蓋的問題：

1. 在 Claude Code 中使用 `/bug` 命令直接向 Anthropic 報告問題
2. 檢查 [GitHub 存儲庫](https://github.com/anthropics/claude-code)以了解已知問題
3. 運行 `/doctor` 診斷問題。它檢查：
   * 安裝類型、版本和搜索功能
   * 自動更新狀態和可用版本
   * 無效的設置文件（格式錯誤的 JSON、不正確的類型）
   * MCP 服務器配置錯誤
   * 快捷鍵配置問題
   * 上下文使用警告（大型 CLAUDE.md 文件、高 MCP 令牌使用、無法訪問的權限規則）
   * 插件和代理加載錯誤
4. 直接向 Claude 詢問其功能和特性 - Claude 內置訪問其文檔
