> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 故障排除

> 修復 Claude Code 中的高 CPU 或記憶體使用、掛起、auto-compact 抖動和搜尋問題，並找到其他問題的正確頁面。

本頁涵蓋 Claude Code 執行後的效能、穩定性和搜尋問題。如需其他問題，請從符合您遇到問題位置的頁面開始：

| 症狀                                                              | 前往                                                                |
| :-------------------------------------------------------------- | :---------------------------------------------------------------- |
| `command not found`、安裝失敗、PATH 問題、`EACCES`、TLS 錯誤                | [故障排除安裝和登入](/zh-TW/troubleshoot-install)                          |
| 登入迴圈、OAuth 錯誤、`403 Forbidden`、「組織已停用」、Bedrock/Vertex/Foundry 認證 | [故障排除安裝和登入](/zh-TW/troubleshoot-install#login-and-authentication) |
| 設定未套用、hooks 未觸發、MCP 伺服器未載入                                      | [偵錯您的設定](/zh-TW/debug-your-config)                                |
| `API Error: 5xx`、`529 Overloaded`、`429`、請求驗證錯誤                  | [錯誤參考](/zh-TW/errors)                                             |
| `model not found` 或 `you may not have access to it`             | [錯誤參考](/zh-TW/errors#theres-an-issue-with-the-selected-model)     |
| VS Code 擴充功能未連接或未偵測到 Claude                                     | [VS Code 整合](/zh-TW/vs-code#fix-common-issues)                    |
| JetBrains 外掛程式或 IDE 未偵測到                                        | [JetBrains 整合](/zh-TW/jetbrains#troubleshooting)                  |
| 高 CPU 或記憶體、回應緩慢、掛起、搜尋找不到檔案                                      | [效能和穩定性](#performance-and-stability)下方                            |

如果您不確定哪個適用，請在 Claude Code 內執行 `/doctor` 以自動檢查您的安裝、設定、MCP 伺服器和上下文使用情況。如果 `claude` 根本無法啟動，請改為從您的 shell 執行 `claude doctor`。

## 效能和穩定性

這些部分涵蓋與資源使用、回應性和搜尋行為相關的問題。

### 高 CPU 或記憶體使用

Claude Code 設計用於與大多數開發環境配合使用，但在處理大型程式碼庫時可能消耗大量資源。如果您遇到效能問題：

1. 定期使用 `/compact` 減少上下文大小
2. 在主要任務之間關閉並重新啟動 Claude Code
3. 考慮將大型構建目錄新增到您的 `.gitignore` 檔案

如果在這些步驟後記憶體使用仍然很高，請執行 `/heapdump` 以將 JavaScript 堆快照和記憶體分解寫入 `~/Desktop`。在沒有 Desktop 資料夾的 Linux 上，檔案會寫入您的主目錄。

分解顯示駐留集大小、JS 堆、陣列緩衝區和未計算的原生記憶體，這有助於識別增長是在 JavaScript 物件還是原生程式碼中。若要檢查保留者，請在 Chrome DevTools 中的 Memory → Load 下開啟 `.heapsnapshot` 檔案。在 [GitHub](https://github.com/anthropics/claude-code/issues) 上報告記憶體問題時附加兩個檔案。

### Auto-compaction 停止並出現 thrashing 錯誤

如果您看到 `Autocompact is thrashing: the context refilled to the limit...`，自動 compaction 成功，但檔案或工具輸出立即多次重新填充上下文視窗。Claude Code 停止重試以避免在沒有進展的迴圈上浪費 API 呼叫。

若要復原：

1. 要求 Claude 以較小的塊讀取超大檔案，例如特定行範圍或函式，而不是整個檔案
2. 執行 `/compact` 並關注丟棄大輸出，例如 `/compact keep only the plan and the diff`
3. 將大檔案工作移動到 [subagent](/zh-TW/sub-agents)，以便它在單獨的上下文視窗中執行
4. 如果早期對話不再需要，執行 `/clear`

### 命令掛起或凍結

如果 Claude Code 似乎無回應：

1. 按 Ctrl+C 嘗試取消目前操作
2. 如果無回應，您可能需要關閉終端並重新啟動

重新啟動不會遺失您的對話。在同一目錄中執行 `claude --resume` 以繼續會話。

### 搜尋和發現問題

如果搜尋工具、`@file` 提及、自訂代理或自訂 skills 找不到檔案，捆綁的 `ripgrep` 二進位檔可能無法在您的系統上執行。安裝您平台的 `ripgrep` 套件並告訴 Claude Code 改用它：

<Tabs>
  <Tab title="macOS">
    ```bash theme={null}
    brew install ripgrep
    ```
  </Tab>

  <Tab title="Ubuntu/Debian">
    ```bash theme={null}
    sudo apt install ripgrep
    ```
  </Tab>

  <Tab title="Alpine">
    ```bash theme={null}
    apk add ripgrep
    ```
  </Tab>

  <Tab title="Arch">
    ```bash theme={null}
    pacman -S ripgrep
    ```
  </Tab>

  <Tab title="Windows">
    ```powershell theme={null}
    winget install BurntSushi.ripgrep.MSVC
    ```
  </Tab>
</Tabs>

然後在您的[環境](/zh-TW/env-vars)中設定 `USE_BUILTIN_RIPGREP=0`。

### WSL 上的搜尋速度緩慢或結果不完整

在 WSL 上[跨檔案系統工作](https://learn.microsoft.com/en-us/windows/wsl/filesystems)時的磁碟讀取效能損失可能導致在 WSL 上使用 Claude Code 時匹配數少於預期。搜尋仍然有效，但在原生檔案系統上返回的結果較少。

<Note>
  在這種情況下，`/doctor` 將顯示搜尋為正常。
</Note>

**解決方案：**

1. **提交更具體的搜尋**：透過指定目錄或檔案類型來減少搜尋的檔案數量：「Search for JWT validation logic in the auth-service package」或「Find use of md5 hash in JS files」。

2. **將專案移動到 Linux 檔案系統**：如果可能，確保您的專案位於 Linux 檔案系統（`/home/`）而不是 Windows 檔案系統（`/mnt/c/`）。

3. **改用原生 Windows**：考慮在 Windows 上原生執行 Claude Code 而不是透過 WSL，以獲得更好的檔案系統效能。

## 取得更多幫助

如果您遇到此處未涵蓋的問題：

1. 執行 `/doctor` 以一次檢查安裝健康狀況、設定有效性、MCP 設定和上下文使用情況
2. 在 Claude Code 內使用 `/feedback` 命令直接向 Anthropic 報告問題
3. 檢查 [GitHub 存儲庫](https://github.com/anthropics/claude-code)以了解已知問題
4. 直接向 Claude 詢問其功能和特性。Claude 內置訪問其文檔。
