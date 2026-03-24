> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 使用 Remote Control 從任何裝置繼續本地會話

> 使用 Remote Control 從您的手機、平板電腦或任何瀏覽器繼續本地 Claude Code 會話。適用於 claude.ai/code 和 Claude 行動應用程式。

<Note>
  Remote Control 在所有方案上都可用。Team 和 Enterprise 管理員必須先在[管理員設定](https://claude.ai/admin-settings/claude-code)中啟用 Claude Code。
</Note>

Remote Control 將 [claude.ai/code](https://claude.ai/code) 或 Claude 應用程式（[iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) 和 [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude)）連接到在您機器上執行的 Claude Code 會話。在您的辦公桌開始一項任務，然後從沙發上的手機或另一台電腦上的瀏覽器繼續。

當您在機器上啟動 Remote Control 會話時，Claude 會在整個過程中在本地執行，因此沒有任何內容會移至雲端。使用 Remote Control，您可以：

* **遠端使用您的完整本地環境**：您的檔案系統、[MCP servers](/zh-TW/mcp)、工具和專案配置都保持可用
* **同時在兩個介面上工作**：對話在所有連接的裝置上保持同步，因此您可以從終端機、瀏覽器和手機交替發送訊息
* **克服中斷**：如果您的筆記型電腦進入睡眠狀態或網路中斷，當您的機器重新上線時，會話會自動重新連接

與[網頁版 Claude Code](/zh-TW/claude-code-on-the-web)（在雲端基礎設施上執行）不同，Remote Control 會話直接在您的機器上執行並與您的本地檔案系統互動。網頁和行動介面只是該本地會話的一個窗口。

<Note>
  Remote Control 需要 Claude Code v2.1.51 或更新版本。使用 `claude --version` 檢查您的版本。
</Note>

本頁涵蓋設定、如何啟動和連接到會話，以及 Remote Control 與網頁版 Claude Code 的比較。

## 需求

在使用 Remote Control 之前，請確認您的環境符合以下條件：

* **訂閱**：在 Pro、Max、Team 和 Enterprise 方案上可用。Team 和 Enterprise 管理員必須先在[管理員設定](https://claude.ai/admin-settings/claude-code)中啟用 Claude Code。不支援 API 金鑰。
* **驗證**：執行 `claude` 並使用 `/login` 透過 claude.ai 登入（如果您還沒有登入）。
* **工作區信任**：在您的專案目錄中至少執行一次 `claude` 以接受工作區信任對話框。

## 啟動 Remote Control 會話

您可以啟動專用的 Remote Control 伺服器、啟動啟用了 Remote Control 的互動式會話，或連接已在執行的會話。

<Tabs>
  <Tab title="伺服器模式">
    導航到您的專案目錄並執行：

    ```bash  theme={null}
    claude remote-control
    ```

    該過程在您的終端機中以伺服器模式保持執行，等待遠端連接。它顯示一個會話 URL，您可以使用該 URL 從[另一個裝置連接](#connect-from-another-device)，您可以按空格鍵顯示 QR 碼以從手機快速存取。當遠端會話處於活動狀態時，終端機會顯示連接狀態和工具活動。

    可用的旗標：

    | 旗標                           | 說明                                                                                                                                                                                                                    |
    | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `--name "My Project"`        | 設定自訂會話標題，在 claude.ai/code 的會話清單中可見。                                                                                                                                                                                   |
    | `--spawn <mode>`             | 如何建立並行會話。在執行時按 `w` 切換。<br />• `same-dir`（預設）：所有會話共享目前的工作目錄，因此如果編輯相同的檔案可能會衝突。<br />• `worktree`：每個按需會話都會獲得自己的 [git worktree](/zh-TW/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees)。需要 git 儲存庫。 |
    | `--capacity <N>`             | 並行會話的最大數量。預設值為 32。                                                                                                                                                                                                    |
    | `--verbose`                  | 顯示詳細的連接和會話日誌。                                                                                                                                                                                                         |
    | `--sandbox` / `--no-sandbox` | 啟用或停用[沙箱](/zh-TW/sandboxing)以進行檔案系統和網路隔離。預設為關閉。                                                                                                                                                                       |
  </Tab>

  <Tab title="互動式會話">
    要啟動啟用了 Remote Control 的一般互動式 Claude Code 會話，請使用 `--remote-control` 旗標（或 `--rc`）：

    ```bash  theme={null}
    claude --remote-control
    ```

    可選地為會話傳遞一個名稱：

    ```bash  theme={null}
    claude --remote-control "My Project"
    ```

    這為您提供了一個完整的互動式會話在您的終端機中，您也可以從 claude.ai 或 Claude 應用程式控制。與 `claude remote-control`（伺服器模式）不同，您可以在會話也可遠端使用時在本地輸入訊息。
  </Tab>

  <Tab title="從現有會話">
    如果您已經在 Claude Code 會話中並想遠端繼續它，請使用 `/remote-control`（或 `/rc`）命令：

    ```text  theme={null}
    /remote-control
    ```

    傳遞一個名稱作為引數以設定自訂會話標題：

    ```text  theme={null}
    /remote-control My Project
    ```

    這啟動一個 Remote Control 會話，該會話會延續您目前的對話歷史記錄，並顯示一個會話 URL 和 QR 碼，您可以使用它從[另一個裝置連接](#connect-from-another-device)。`--verbose`、`--sandbox` 和 `--no-sandbox` 旗標不適用於此命令。
  </Tab>
</Tabs>

### 從另一個裝置連接

一旦 Remote Control 會話處於活動狀態，您有幾種方式從另一個裝置連接：

* **開啟會話 URL** 在任何瀏覽器中直接進入 [claude.ai/code](https://claude.ai/code) 上的會話。`claude remote-control` 和 `/remote-control` 都在終端機中顯示此 URL。
* **掃描 QR 碼** 顯示在會話 URL 旁邊，直接在 Claude 應用程式中開啟它。使用 `claude remote-control` 時，按空格鍵切換 QR 碼顯示。
* **開啟 [claude.ai/code](https://claude.ai/code) 或 Claude 應用程式**，並在會話清單中按名稱找到會話。Remote Control 會話在線上時顯示帶有綠色狀態點的電腦圖示。

遠端會話從 `--name` 引數（或傳遞給 `/remote-control` 的名稱）、您的最後一條訊息、您的 `/rename` 值或「Remote Control session」（如果沒有對話歷史記錄）取得其名稱。如果環境已經有一個活動會話，您將被詢問是否繼續它或啟動一個新會話。

如果您還沒有 Claude 應用程式，請在 Claude Code 內使用 `/mobile` 命令顯示 [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) 或 [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) 的下載 QR 碼。

### 為所有會話啟用 Remote Control

預設情況下，Remote Control 只在您明確執行 `claude remote-control`、`claude --remote-control` 或 `/remote-control` 時啟動。要為每個互動式會話自動啟用它，請在 Claude Code 內執行 `/config` 並將**為所有會話啟用 Remote Control** 設定為 `true`。將其設定回 `false` 以停用。

啟用此設定後，每個互動式 Claude Code 程序會註冊一個遠端會話。如果您執行多個實例，每個實例都會獲得自己的環境和會話。要從單個程序執行多個並行會話，請改用伺服器模式搭配 `--spawn`。

## 連接和安全性

您的本地 Claude Code 會話僅發出出站 HTTPS 請求，永遠不會在您的機器上開啟入站連接埠。當您啟動 Remote Control 時，它會向 Anthropic API 註冊並輪詢工作。當您從另一個裝置連接時，伺服器會透過串流連接在網頁或行動用戶端與您的本地會話之間路由訊息。

所有流量都透過 TLS 上的 Anthropic API 傳輸，與任何 Claude Code 會話相同的傳輸安全性。連接使用多個短期認證，每個認證的範圍限定為單一目的並獨立過期。

## Remote Control 與網頁版 Claude Code 的比較

Remote Control 和[網頁版 Claude Code](/zh-TW/claude-code-on-the-web)都使用 claude.ai/code 介面。關鍵區別在於會話執行的位置：Remote Control 在您的機器上執行，因此您的本地 MCP servers、工具和專案配置保持可用。網頁版 Claude Code 在 Anthropic 管理的雲端基礎設施中執行。

當您在本地工作中途並想從另一個裝置繼續時，請使用 Remote Control。當您想在沒有任何本地設定的情況下啟動任務、處理您沒有複製的儲存庫或並行執行多個任務時，請使用網頁版 Claude Code。

## 限制

* **每個互動式程序一個遠端會話**：在伺服器模式之外，每個 Claude Code 實例一次支援一個遠端會話。使用伺服器模式搭配 `--spawn` 從單個程序執行多個並行會話。
* **終端機必須保持開啟**：Remote Control 作為本地程序執行。如果您關閉終端機或停止 `claude` 程序，會話結束。再次執行 `claude remote-control` 以啟動新會話。
* **延長的網路中斷**：如果您的機器處於喚醒狀態但無法在大約 10 分鐘以上的時間內到達網路，會話會逾時並且程序退出。再次執行 `claude remote-control` 以啟動新會話。

## 相關資源

* [網頁版 Claude Code](/zh-TW/claude-code-on-the-web)：在 Anthropic 管理的雲端環境中執行會話，而不是在您的機器上
* [驗證](/zh-TW/authentication)：設定 `/login` 並管理 claude.ai 的認證
* [CLI 參考](/zh-TW/cli-reference)：包括 `claude remote-control` 的旗標和命令的完整清單
* [安全性](/zh-TW/security)：Remote Control 會話如何適應 Claude Code 安全模型
* [資料使用](/zh-TW/data-usage)：在本地和遠端會話期間透過 Anthropic API 流動的資料
