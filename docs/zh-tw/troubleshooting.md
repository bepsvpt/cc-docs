> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 疑難排解

> 探索 Claude Code 安裝和使用中常見問題的解決方案。

## 疑難排解安裝問題

<Tip>
  如果您想完全跳過終端，[Claude Code Desktop 應用程式](/zh-TW/desktop-quickstart)可讓您透過圖形介面安裝和使用 Claude Code。下載適用於 [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) 或 [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs) 的版本，無需任何命令列設定即可開始編碼。
</Tip>

找到您看到的錯誤訊息或症狀：

| 您看到的內容                                                     | 解決方案                                                                                  |
| :--------------------------------------------------------- | :------------------------------------------------------------------------------------ |
| `command not found: claude` 或 `'claude' is not recognized` | [修復您的 PATH](#command-not-found-claude-after-installation)                             |
| `syntax error near unexpected token '<'`                   | [安裝指令碼傳回 HTML](#install-script-returns-html-instead-of-a-shell-script)                |
| `curl: (56) Failure writing output to destination`         | [先下載指令碼，然後執行](#curl-56-failure-writing-output-to-destination)                         |
| Linux 上安裝期間 `Killed`                                       | [為低記憶體伺服器新增交換空間](#install-killed-on-low-memory-linux-servers)                         |
| `TLS connect error` 或 `SSL/TLS secure channel`             | [更新 CA 憑證](#tls-or-ssl-connection-errors)                                             |
| `Failed to fetch version` 或無法連接下載伺服器                       | [檢查網路和代理設定](#check-network-connectivity)                                              |
| `irm is not recognized` 或 `&& is not valid`                | [為您的 shell 使用正確的命令](#windows-irm-or--not-recognized)                                  |
| `Claude Code on Windows requires git-bash`                 | [安裝或設定 Git Bash](#windows-claude-code-on-windows-requires-git-bash)                   |
| `Error loading shared library`                             | [您的系統安裝了錯誤的二進位變體](#linux-wrong-binary-variant-installed-muslglibc-mismatch)           |
| Linux 上的 `Illegal instruction`                             | [架構不匹配](#illegal-instruction-on-linux)                                                |
| macOS 上的 `dyld: cannot load` 或 `Abort trap`                | [二進位不相容](#dyld-cannot-load-on-macos)                                                  |
| `Invoke-Expression: Missing argument in parameter list`    | [安裝指令碼傳回 HTML](#install-script-returns-html-instead-of-a-shell-script)                |
| `App unavailable in region`                                | Claude Code 在您的國家/地區不可用。請參閱[支援的國家/地區](https://www.anthropic.com/supported-countries)。 |
| `unable to get local issuer certificate`                   | [設定公司 CA 憑證](#tls-or-ssl-connection-errors)                                           |
| `OAuth error` 或 `403 Forbidden`                            | [修復驗證](#authentication-issues)                                                        |

如果您的問題未列出，請執行這些診斷步驟。

## 偵錯安裝問題

### 檢查網路連線

安裝程式從 `storage.googleapis.com` 下載。驗證您可以連接到它：

```bash  theme={null}
curl -sI https://storage.googleapis.com
```

如果失敗，您的網路可能阻止了連線。常見原因：

* 公司防火牆或代理阻止 Google Cloud Storage
* 區域網路限制：嘗試使用 VPN 或替代網路
* TLS/SSL 問題：更新您系統的 CA 憑證，或檢查是否設定了 `HTTPS_PROXY`

如果您在公司代理後面，在安裝前設定 `HTTPS_PROXY` 和 `HTTP_PROXY` 為您的代理位址。如果您不知道代理 URL，請詢問您的 IT 團隊，或檢查您的瀏覽器代理設定。

此範例設定兩個代理變數，然後透過您的代理執行安裝程式：

```bash  theme={null}
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
curl -fsSL https://claude.ai/install.sh | bash
```

### 驗證您的 PATH

如果安裝成功但執行 `claude` 時出現 `command not found` 或 `not recognized` 錯誤，安裝目錄不在您的 PATH 中。您的 shell 在 PATH 中列出的目錄中搜尋程式，安裝程式在 macOS/Linux 上將 `claude` 放在 `~/.local/bin/claude`，或在 Windows 上放在 `%USERPROFILE%\.local\bin\claude.exe`。

透過列出您的 PATH 項目並篩選 `local/bin` 來檢查安裝目錄是否在您的 PATH 中：

<Tabs>
  <Tab title="macOS/Linux">
    ```bash  theme={null}
    echo $PATH | tr ':' '\n' | grep local/bin
    ```

    如果沒有輸出，該目錄遺失。將其新增到您的 shell 設定：

    ```bash  theme={null}
    # Zsh (macOS 預設)
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc

    # Bash (Linux 預設)
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
    ```

    或者，關閉並重新開啟您的終端。

    驗證修復是否有效：

    ```bash  theme={null}
    claude --version
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    $env:PATH -split ';' | Select-String 'local\\bin'
    ```

    如果沒有輸出，將安裝目錄新增到您的使用者 PATH：

    ```powershell  theme={null}
    $currentPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
    [Environment]::SetEnvironmentVariable('PATH', "$currentPath;$env:USERPROFILE\.local\bin", 'User')
    ```

    重新啟動您的終端以使變更生效。

    驗證修復是否有效：

    ```powershell  theme={null}
    claude --version
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    echo %PATH% | findstr /i "local\bin"
    ```

    如果沒有輸出，開啟系統設定，前往環境變數，並將 `%USERPROFILE%\.local\bin` 新增到您的使用者 PATH 變數。重新啟動您的終端。

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
    列出在您的 PATH 中找到的所有 `claude` 二進位檔：

    ```bash  theme={null}
    which -a claude
    ```

    檢查原生安裝程式和 npm 版本是否存在：

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

如果您找到多個安裝，只保留一個。建議使用 `~/.local/bin/claude` 的原生安裝。移除任何額外的安裝：

解除安裝 npm 全域安裝：

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

在 macOS 上移除 Homebrew 安裝：

```bash  theme={null}
brew uninstall --cask claude-code
```

### 檢查目錄權限

安裝程式需要對 `~/.local/bin/` 和 `~/.claude/` 的寫入存取權。如果安裝因權限錯誤而失敗，檢查這些目錄是否可寫：

```bash  theme={null}
test -w ~/.local/bin && echo "writable" || echo "not writable"
test -w ~/.claude && echo "writable" || echo "not writable"
```

如果任一目錄不可寫，建立安裝目錄並將您的使用者設定為擁有者：

```bash  theme={null}
sudo mkdir -p ~/.local/bin
sudo chown -R $(whoami) ~/.local
```

### 驗證二進位檔是否有效

如果 `claude` 已安裝但在啟動時崩潰或掛起，執行這些檢查以縮小原因範圍。

確認二進位檔存在且可執行：

```bash  theme={null}
ls -la $(which claude)
```

在 Linux 上，檢查遺失的共用程式庫。如果 `ldd` 顯示遺失的程式庫，您可能需要安裝系統套件。在 Alpine Linux 和其他基於 musl 的發行版上，請參閱 [Alpine Linux 設定](/zh-TW/setup#alpine-linux-and-musl-based-distributions)。

```bash  theme={null}
ldd $(which claude) | grep "not found"
```

執行快速健全性檢查，確認二進位檔可以執行：

```bash  theme={null}
claude --version
```

## 常見安裝問題

這些是最常遇到的安裝問題及其解決方案。

### 安裝指令碼傳回 HTML 而不是 shell 指令碼

執行安裝命令時，您可能會看到以下其中一個錯誤：

```text  theme={null}
bash: line 1: syntax error near unexpected token `<'
bash: line 1: `<!DOCTYPE html>'
```

在 PowerShell 上，同樣的問題顯示為：

```text  theme={null}
Invoke-Expression: Missing argument in parameter list.
```

這表示安裝 URL 傳回了 HTML 頁面而不是安裝指令碼。如果 HTML 頁面顯示「App unavailable in region」，Claude Code 在您的國家/地區不可用。請參閱[支援的國家/地區](https://www.anthropic.com/supported-countries)。

否則，這可能由於網路問題、區域路由或臨時服務中斷而發生。

**解決方案：**

1. **使用替代安裝方法**：

   在 macOS 或 Linux 上，透過 Homebrew 安裝：

   ```bash  theme={null}
   brew install --cask claude-code
   ```

   在 Windows 上，透過 WinGet 安裝：

   ```powershell  theme={null}
   winget install Anthropic.ClaudeCode
   ```

2. **幾分鐘後重試**：此問題通常是暫時的。等待並重試原始命令。

### 安裝後 `command not found: claude`

安裝完成但 `claude` 無法運作。確切的錯誤因平台而異：

| 平台          | 錯誤訊息                                                                   |
| :---------- | :--------------------------------------------------------------------- |
| macOS       | `zsh: command not found: claude`                                       |
| Linux       | `bash: claude: command not found`                                      |
| Windows CMD | `'claude' is not recognized as an internal or external command`        |
| PowerShell  | `claude : The term 'claude' is not recognized as the name of a cmdlet` |

這表示安裝目錄不在您的 shell 搜尋路徑中。請參閱[驗證您的 PATH](#verify-your-path) 以取得每個平台上的修復。

### `curl: (56) Failure writing output to destination`

`curl ... | bash` 命令下載指令碼並使用管道 (`|`) 將其直接傳遞給 Bash 執行。此錯誤表示連線在指令碼完成下載前中斷。常見原因包括網路中斷、下載被中途阻止或系統資源限制。

**解決方案：**

1. **檢查網路穩定性**：Claude Code 二進位檔託管在 Google Cloud Storage 上。測試您是否可以連接到它：
   ```bash  theme={null}
   curl -fsSL https://storage.googleapis.com -o /dev/null
   ```
   如果命令無聲地完成，您的連線沒問題，問題可能是間歇性的。重試安裝命令。如果您看到錯誤，您的網路可能阻止了下載。

2. **嘗試替代安裝方法**：

   在 macOS 或 Linux 上：

   ```bash  theme={null}
   brew install --cask claude-code
   ```

   在 Windows 上：

   ```powershell  theme={null}
   winget install Anthropic.ClaudeCode
   ```

### TLS 或 SSL 連線錯誤

像 `curl: (35) TLS connect error`、`schannel: next InitializeSecurityContext failed` 或 PowerShell 的 `Could not establish trust relationship for the SSL/TLS secure channel` 這樣的錯誤表示 TLS 握手失敗。

**解決方案：**

1. **更新您的系統 CA 憑證**：

   在 Ubuntu/Debian 上：

   ```bash  theme={null}
   sudo apt-get update && sudo apt-get install ca-certificates
   ```

   在 macOS 上透過 Homebrew：

   ```bash  theme={null}
   brew install ca-certificates
   ```

2. **在 Windows 上，在執行安裝程式前在 PowerShell 中啟用 TLS 1.2**：
   ```powershell  theme={null}
   [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
   irm https://claude.ai/install.ps1 | iex
   ```

3. **檢查代理或防火牆干擾**：執行 TLS 檢查的公司代理可能導致這些錯誤，包括 `unable to get local issuer certificate`。將 `NODE_EXTRA_CA_CERTS` 設定為您的公司 CA 憑證套件：
   ```bash  theme={null}
   export NODE_EXTRA_CA_CERTS=/path/to/corporate-ca.pem
   ```
   如果您沒有憑證檔案，請詢問您的 IT 團隊。您也可以嘗試直接連線以確認代理是原因。

### `Failed to fetch version from storage.googleapis.com`

安裝程式無法連接到下載伺服器。這通常表示 `storage.googleapis.com` 在您的網路上被阻止。

**解決方案：**

1. **直接測試連線**：
   ```bash  theme={null}
   curl -sI https://storage.googleapis.com
   ```

2. **如果在代理後面**，設定 `HTTPS_PROXY` 以便安裝程式可以透過它路由。請參閱[代理設定](/zh-TW/network-config#proxy-configuration)以取得詳細資訊。
   ```bash  theme={null}
   export HTTPS_PROXY=http://proxy.example.com:8080
   curl -fsSL https://claude.ai/install.sh | bash
   ```

3. **如果在受限網路上**，嘗試不同的網路或 VPN，或使用替代安裝方法：

   在 macOS 或 Linux 上：

   ```bash  theme={null}
   brew install --cask claude-code
   ```

   在 Windows 上：

   ```powershell  theme={null}
   winget install Anthropic.ClaudeCode
   ```

### Windows：`irm` 或 `&&` 無法識別

如果您看到 `'irm' is not recognized` 或 `The token '&&' is not valid`，您執行的是錯誤的 shell 命令。

* **`irm` 無法識別**：您在 CMD 中，而不是 PowerShell。您有兩個選項：

  透過在開始功能表中搜尋「PowerShell」來開啟 PowerShell，然後執行原始安裝命令：

  ```powershell  theme={null}
  irm https://claude.ai/install.ps1 | iex
  ```

  或留在 CMD 中並改用 CMD 安裝程式：

  ```batch  theme={null}
  curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
  ```

* **`&&` 無效**：您在 PowerShell 中但執行了 CMD 安裝程式命令。使用 PowerShell 安裝程式：
  ```powershell  theme={null}
  irm https://claude.ai/install.ps1 | iex
  ```

### 低記憶體 Linux 伺服器上安裝被終止

如果您在 VPS 或雲端執行個體上的安裝期間看到 `Killed`：

```text  theme={null}
Setting up Claude Code...
Installing Claude Code native build latest...
bash: line 142: 34803 Killed    "$binary_path" install ${TARGET:+"$TARGET"}
```

Linux OOM 殺手終止了該程序，因為系統記憶體不足。Claude Code 需要至少 4 GB 的可用 RAM。

**解決方案：**

1. **新增交換空間**（如果您的伺服器 RAM 有限）。交換使用磁碟空間作為溢出記憶體，讓安裝即使在低物理 RAM 的情況下也能完成。

   建立 2 GB 交換檔案並啟用它：

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

2. **關閉其他程序**以在安裝前釋放記憶體。

3. **使用更大的執行個體**（如果可能）。Claude Code 需要至少 4 GB 的 RAM。

### Docker 中安裝掛起

在 Docker 容器中安裝 Claude Code 時，以 root 身份安裝到 `/` 可能導致掛起。

**解決方案：**

1. **在執行安裝程式前設定工作目錄**。從 `/` 執行時，安裝程式掃描整個檔案系統，導致過度的記憶體使用。設定 `WORKDIR` 將掃描限制在小目錄：
   ```dockerfile  theme={null}
   WORKDIR /tmp
   RUN curl -fsSL https://claude.ai/install.sh | bash
   ```

2. **增加 Docker 記憶體限制**（如果使用 Docker Desktop）：
   ```bash  theme={null}
   docker build --memory=4g .
   ```

### Windows：Claude Desktop 覆蓋 `claude` CLI 命令

如果您安裝了舊版本的 Claude Desktop，它可能在 `WindowsApps` 目錄中註冊一個 `Claude.exe`，其 PATH 優先級高於 Claude Code CLI。執行 `claude` 會開啟 Desktop 應用程式而不是 CLI。

更新 Claude Desktop 到最新版本以修復此問題。

### Windows：「Claude Code on Windows requires git-bash」

Windows 上的 Claude Code 需要 [Git for Windows](https://git-scm.com/downloads/win)，其中包括 Git Bash。

**如果未安裝 Git**，從 [git-scm.com/downloads/win](https://git-scm.com/downloads/win) 下載並安裝它。在設定期間，選擇「Add to PATH」。安裝後重新啟動您的終端。

**如果 Git 已安裝**但 Claude Code 仍無法找到它，在您的 [settings.json 檔案](/zh-TW/settings)中設定路徑：

```json  theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

如果您的 Git 安裝在其他地方，透過在 PowerShell 中執行 `where.exe git` 找到路徑，並使用該目錄中的 `bin\bash.exe` 路徑。

### Linux：安裝了錯誤的二進位變體（musl/glibc 不匹配）

如果在安裝後看到有關遺失共用程式庫的錯誤，如 `libstdc++.so.6` 或 `libgcc_s.so.1`，安裝程式可能為您的系統下載了錯誤的二進位變體。

```text  theme={null}
Error loading shared library libstdc++.so.6: No such file or directory
```

這可能發生在已安裝 musl 交叉編譯套件的基於 glibc 的系統上，導致安裝程式誤偵測系統為 musl。

**解決方案：**

1. **檢查您的系統使用哪個 libc**：
   ```bash  theme={null}
   ldd /bin/ls | head -1
   ```
   如果它顯示 `linux-vdso.so` 或對 `/lib/x86_64-linux-gnu/` 的參考，您在 glibc 上。如果它顯示 `musl`，您在 musl 上。

2. **如果您在 glibc 上但得到了 musl 二進位檔**，移除安裝並重新安裝。您也可以從 GCS 儲存桶 `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json` 手動下載正確的二進位檔。使用 `ldd /bin/ls` 和 `ls /lib/libc.musl*` 的輸出提交 [GitHub 問題](https://github.com/anthropics/claude-code/issues)。

3. **如果您實際上在 musl 上**（Alpine Linux），安裝所需的套件：
   ```bash  theme={null}
   apk add libgcc libstdc++ ripgrep
   ```

### Linux 上的 `Illegal instruction`

如果安裝程式列印 `Illegal instruction` 而不是 OOM `Killed` 訊息，下載的二進位檔與您的 CPU 架構不匹配。這通常發生在接收 x86 二進位檔的 ARM 伺服器上，或在缺少所需指令集的較舊 CPU 上。

```text  theme={null}
bash: line 142: 2238232 Illegal instruction    "$binary_path" install ${TARGET:+"$TARGET"}
```

**解決方案：**

1. **驗證您的架構**：
   ```bash  theme={null}
   uname -m
   ```
   `x86_64` 表示 64 位 Intel/AMD，`aarch64` 表示 ARM64。如果二進位檔不匹配，[提交 GitHub 問題](https://github.com/anthropics/claude-code/issues)並附上輸出。

2. **嘗試替代安裝方法**，同時解決架構問題：
   ```bash  theme={null}
   brew install --cask claude-code
   ```

### macOS 上的 `dyld: cannot load`

如果在安裝期間看到 `dyld: cannot load` 或 `Abort trap: 6`，二進位檔與您的 macOS 版本或硬體不相容。

```text  theme={null}
dyld: cannot load 'claude-2.1.42-darwin-x64' (load command 0x80000034 is unknown)
Abort trap: 6
```

**解決方案：**

1. **檢查您的 macOS 版本**：Claude Code 需要 macOS 13.0 或更新版本。開啟 Apple 功能表並選擇「About This Mac」以檢查您的版本。

2. **更新 macOS**（如果您在較舊版本上）。二進位檔使用較舊 macOS 版本不支援的載入命令。

3. **嘗試 Homebrew** 作為替代安裝方法：
   ```bash  theme={null}
   brew install --cask claude-code
   ```

### Windows 安裝問題：WSL 中的錯誤

您可能在 WSL 中遇到以下問題：

**OS/平台偵測問題**：如果您在安裝期間收到錯誤，WSL 可能使用 Windows `npm`。嘗試：

* 在安裝前執行 `npm config set os linux`
* 使用 `npm install -g @anthropic-ai/claude-code --force --no-os-check` 安裝。不要使用 `sudo`。

**找不到 Node 錯誤**：如果執行 `claude` 時看到 `exec: node: not found`，您的 WSL 環境可能使用 Windows 安裝的 Node.js。您可以使用 `which npm` 和 `which node` 確認這一點，它們應該指向以 `/usr/` 開頭的 Linux 路徑，而不是 `/mnt/c/`。要修復此問題，請嘗試透過您的 Linux 發行版的套件管理器或透過 [`nvm`](https://github.com/nvm-sh/nvm) 安裝 Node。

**nvm 版本衝突**：如果您在 WSL 和 Windows 中都安裝了 nvm，在 WSL 中切換 Node 版本時可能會遇到版本衝突。這是因為 WSL 預設匯入 Windows PATH，導致 Windows nvm/npm 優先於 WSL 安裝。

您可以透過以下方式識別此問題：

* 執行 `which npm` 和 `which node` - 如果它們指向 Windows 路徑（以 `/mnt/c/` 開頭），則使用 Windows 版本
* 在 WSL 中使用 nvm 切換 Node 版本後遇到損壞的功能

要解決此問題，修復您的 Linux PATH 以確保 Linux node/npm 版本優先：

**主要解決方案：確保 nvm 在您的 shell 中正確載入**

最常見的原因是 nvm 未在非互動式 shell 中載入。將以下內容新增到您的 shell 設定檔（`~/.bashrc`、`~/.zshrc` 等）：

```bash  theme={null}
# 如果存在，載入 nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
```

或在您的目前工作階段中直接執行：

```bash  theme={null}
source ~/.nvm/nvm.sh
```

**替代方案：調整 PATH 順序**

如果 nvm 正確載入但 Windows 路徑仍優先，您可以在 shell 設定中明確將 Linux 路徑前置到 PATH：

```bash  theme={null}
export PATH="$HOME/.nvm/versions/node/$(node -v)/bin:$PATH"
```

<Warning>
  避免透過 `appendWindowsPath = false` 停用 Windows PATH 匯入，因為這會破壞從 WSL 呼叫 Windows 可執行檔的能力。同樣，如果您為 Windows 開發使用 Node.js，請避免從 Windows 解除安裝它。
</Warning>

### WSL2 sandbox 設定

[Sandboxing](/zh-TW/sandboxing) 在 WSL2 上受支援，但需要安裝其他套件。如果執行 `/sandbox` 時看到「Sandbox requires socat and bubblewrap」之類的錯誤，請安裝依賴項：

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

WSL1 不支援 sandboxing。如果您看到「Sandboxing requires WSL2」，您需要升級到 WSL2 或執行 Claude Code 而不進行 sandboxing。

### 安裝期間的權限錯誤

如果原生安裝程式因權限錯誤而失敗，目標目錄可能不可寫。請參閱[檢查目錄權限](#check-directory-permissions)。

如果您之前使用 npm 安裝並遇到 npm 特定的權限錯誤，請切換到原生安裝程式：

```bash  theme={null}
curl -fsSL https://claude.ai/install.sh | bash
```

## 權限和驗證

這些部分涉及登入失敗、令牌問題和權限提示行為。

### 重複的權限提示

如果您發現自己重複批准相同的命令，您可以使用 `/permissions` 命令允許特定工具無需批准即可執行。請參閱[權限文件](/zh-TW/permissions#manage-permissions)。

### 驗證問題

如果您遇到驗證問題：

1. 執行 `/logout` 以完全登出
2. 關閉 Claude Code
3. 使用 `claude` 重新啟動並再次完成驗證程序

如果瀏覽器在登入期間未自動開啟，按 `c` 將 OAuth URL 複製到您的剪貼簿，然後手動將其貼到您的瀏覽器中。

### OAuth 錯誤：無效代碼

如果您看到 `OAuth error: Invalid code. Please make sure the full code was copied`，登入代碼已過期或在複製貼上期間被截斷。

**解決方案：**

* 在瀏覽器開啟後按 Enter 重試並快速完成登入
* 輸入 `c` 以複製完整 URL（如果瀏覽器未自動開啟）
* 如果使用遠端/SSH 工作階段，瀏覽器可能在錯誤的機器上開啟。複製終端中顯示的 URL 並在您的本機瀏覽器中開啟它。

### 登入後 403 Forbidden

如果登入後看到 `API Error: 403 {"error":{"type":"forbidden","message":"Request not allowed"}}`：

* **Claude Pro/Max 使用者**：在 [claude.ai/settings](https://claude.ai/settings) 驗證您的訂閱是否有效
* **Console 使用者**：確認您的帳戶已由您的管理員指派「Claude Code」或「Developer」角色
* **在代理後面**：公司代理可能干擾 API 請求。請參閱[網路設定](/zh-TW/network-config)以取得代理設定。

### OAuth 登入在 WSL2 中失敗

如果 WSL 無法開啟您的 Windows 瀏覽器，WSL2 中基於瀏覽器的登入可能失敗。設定 `BROWSER` 環境變數：

```bash  theme={null}
export BROWSER="/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
claude
```

或手動複製 URL：當登入提示出現時，按 `c` 複製 OAuth URL，然後將其貼到您的 Windows 瀏覽器中。

### 「未登入」或令牌已過期

如果 Claude Code 在工作階段後提示您再次登入，您的 OAuth 令牌可能已過期。

執行 `/login` 以重新驗證。如果這種情況經常發生，請檢查您的系統時鐘是否準確，因為令牌驗證取決於正確的時間戳。

## 設定檔位置

Claude Code 在多個位置儲存設定：

| 檔案                            | 用途                                                            |
| :---------------------------- | :------------------------------------------------------------ |
| `~/.claude/settings.json`     | 使用者設定（權限、hooks、模型覆蓋）                                          |
| `.claude/settings.json`       | 專案設定（簽入原始碼控制）                                                 |
| `.claude/settings.local.json` | 本機專案設定（未提交）                                                   |
| `~/.claude.json`              | 全域狀態（主題、OAuth、MCP 伺服器）                                        |
| `.mcp.json`                   | 專案 MCP 伺服器（簽入原始碼控制）                                           |
| `managed-mcp.json`            | [受管 MCP 伺服器](/zh-TW/mcp#managed-mcp-configuration)            |
| 受管設定                          | [受管設定](/zh-TW/settings#settings-files)（伺服器管理、MDM/OS 層級原則或檔案型） |

在 Windows 上，`~` 指您的使用者主目錄，例如 `C:\Users\YourName`。

有關設定這些檔案的詳細資訊，請參閱[設定](/zh-TW/settings)和 [MCP](/zh-TW/mcp)。

### 重設設定

要將 Claude Code 重設為預設設定，您可以移除設定檔：

```bash  theme={null}
# 重設所有使用者設定和狀態
rm ~/.claude.json
rm -rf ~/.claude/

# 重設專案特定設定
rm -rf .claude/
rm .mcp.json
```

<Warning>
  這將移除您的所有設定、MCP 伺服器設定和工作階段歷史記錄。
</Warning>

## 效能和穩定性

這些部分涵蓋與資源使用、回應性和搜尋行為相關的問題。

### 高 CPU 或記憶體使用率

Claude Code 設計用於與大多數開發環境搭配使用，但在處理大型程式碼庫時可能消耗大量資源。如果您遇到效能問題：

1. 定期使用 `/compact` 以減少上下文大小
2. 在主要任務之間關閉並重新啟動 Claude Code
3. 考慮將大型建置目錄新增到您的 `.gitignore` 檔案

### 命令掛起或凍結

如果 Claude Code 似乎無回應：

1. 按 Ctrl+C 嘗試取消目前操作
2. 如果無回應，您可能需要關閉終端並重新啟動

### 搜尋和探索問題

如果搜尋工具、`@file` 提及、自訂代理和自訂 skills 無法運作，請安裝系統 `ripgrep`：

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

然後在您的[環境](/zh-TW/settings#environment-variables)中設定 `USE_BUILTIN_RIPGREP=0`。

### WSL 上的搜尋速度緩慢或結果不完整

在 [WSL 上跨檔案系統工作](https://learn.microsoft.com/en-us/windows/wsl/filesystems)時的磁碟讀取效能損失可能導致在 WSL 上使用 Claude Code 時搜尋結果少於預期。搜尋仍然有效，但傳回的結果少於原生檔案系統。

<Note>
  在這種情況下，`/doctor` 將顯示搜尋為正常。
</Note>

**解決方案：**

1. **提交更具體的搜尋**：透過指定目錄或檔案類型來減少搜尋的檔案數量：「在 auth-service 套件中搜尋 JWT 驗證邏輯」或「在 JS 檔案中尋找 md5 雜湊的使用」。

2. **將專案移到 Linux 檔案系統**：如果可能，確保您的專案位於 Linux 檔案系統（`/home/`）而不是 Windows 檔案系統（`/mnt/c/`）。

3. **改用原生 Windows**：考慮在 Windows 上原生執行 Claude Code 而不是透過 WSL，以獲得更好的檔案系統效能。

## IDE 整合問題

如果 Claude Code 未連接到您的 IDE 或在 IDE 終端中行為異常，請嘗試以下解決方案。

### WSL2 上未偵測到 JetBrains IDE

如果您在 WSL2 上使用 Claude Code 搭配 JetBrains IDE 並收到「No available IDEs detected」錯誤，這可能是由於 WSL2 的網路設定或 Windows 防火牆阻止連線。

#### WSL2 網路模式

WSL2 預設使用 NAT 網路，這可能會阻止 IDE 偵測。您有兩個選項：

**選項 1：設定 Windows 防火牆**（建議）

1. 找到您的 WSL2 IP 位址：
   ```bash  theme={null}
   wsl hostname -I
   # 範例輸出：172.21.123.45
   ```

2. 以管理員身份開啟 PowerShell 並建立防火牆規則：
   ```powershell  theme={null}
   New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
   ```
   根據步驟 1 中的 WSL2 子網調整 IP 範圍。

3. 重新啟動您的 IDE 和 Claude Code

**選項 2：切換到鏡像網路**

在您的 Windows 使用者目錄中新增到 `.wslconfig`：

```ini  theme={null}
[wsl2]
networkingMode=mirrored
```

然後從 PowerShell 使用 `wsl --shutdown` 重新啟動 WSL。

<Note>
  這些網路問題僅影響 WSL2。WSL1 直接使用主機的網路，不需要這些設定。
</Note>

有關其他 JetBrains 設定提示，請參閱 [JetBrains IDE 指南](/zh-TW/jetbrains#plugin-settings)。

### 報告 Windows IDE 整合問題

如果您在 Windows 上遇到 IDE 整合問題，[建立問題](https://github.com/anthropics/claude-code/issues)並提供以下資訊：

* 環境類型：原生 Windows (Git Bash) 或 WSL1/WSL2
* WSL 網路模式（如適用）：NAT 或鏡像
* IDE 名稱和版本
* Claude Code 擴充功能/外掛程式版本
* Shell 類型：Bash、Zsh、PowerShell 等

### JetBrains IDE 終端中的 Escape 鍵無法運作

如果您在 JetBrains 終端中使用 Claude Code 且 `Esc` 鍵無法如預期中斷代理，這可能是由於 JetBrains 預設快捷鍵的衝突。

要修復此問題：

1. 前往設定 → 工具 → 終端
2. 任一：
   * 取消勾選「Move focus to the editor with Escape」，或
   * 按一下「Configure terminal keybindings」並刪除「Switch focus to Editor」快捷鍵
3. 套用變更

這允許 `Esc` 鍵正確中斷 Claude Code 操作。

## Markdown 格式化問題

Claude Code 有時會產生 markdown 檔案，其程式碼圍欄上缺少語言標籤，這可能影響 GitHub、編輯器和文件工具中的語法突出顯示和可讀性。

### 程式碼區塊中缺少語言標籤

如果您在產生的 markdown 中注意到像這樣的程式碼區塊：

````markdown  theme={null}
```
function example() {
  return "hello";
}
```text
````

而不是像這樣的正確標籤區塊：

````markdown  theme={null}
```javascript
function example() {
  return "hello";
}
```text
````

**解決方案：**

1. **要求 Claude 新增語言標籤**：要求「Add appropriate language tags to all code blocks in this markdown file」。

2. **使用後處理 hooks**：設定自動格式化 hooks 以偵測並新增遺失的語言標籤。請參閱[編輯後自動格式化程式碼](/zh-TW/hooks-guide#auto-format-code-after-edits)以取得 PostToolUse 格式化 hook 的範例。

3. **手動驗證**：產生 markdown 檔案後，檢查它們是否有正確的程式碼區塊格式化，如果需要，請要求更正。

### 不一致的間距和格式化

如果產生的 markdown 有過多的空白行或不一致的間距：

**解決方案：**

1. **要求格式化更正**：要求 Claude「Fix spacing and formatting issues in this markdown file」。

2. **使用格式化工具**：設定 hooks 以在產生的 markdown 檔案上執行 markdown 格式化程式（如 `prettier`）或自訂格式化指令碼。

3. **指定格式化偏好**：在您的提示或專案[記憶體](/zh-TW/memory)檔案中包含格式化要求。

### 減少 markdown 格式化問題

要最小化格式化問題：

* **在請求中明確**：要求「properly formatted markdown with language-tagged code blocks」
* **使用專案慣例**：在 [`CLAUDE.md`](/zh-TW/memory) 中記錄您偏好的 markdown 風格
* **設定驗證 hooks**：使用後處理 hooks 自動驗證和修復常見格式化問題

## 取得更多幫助

如果您遇到此處未涵蓋的問題：

1. 在 Claude Code 中使用 `/bug` 命令直接向 Anthropic 報告問題
2. 檢查 [GitHub 儲存庫](https://github.com/anthropics/claude-code)以了解已知問題
3. 執行 `/doctor` 以診斷問題。它檢查：
   * 安裝類型、版本和搜尋功能
   * 自動更新狀態和可用版本
   * 無效的設定檔（格式不正確的 JSON、不正確的類型）
   * MCP 伺服器設定錯誤
   * 快捷鍵設定問題
   * 上下文使用警告（大型 CLAUDE.md 檔案、高 MCP 令牌使用、無法連接的權限規則）
   * 外掛程式和代理載入錯誤
4. 直接詢問 Claude 其功能和特性 - Claude 內建存取其文件
