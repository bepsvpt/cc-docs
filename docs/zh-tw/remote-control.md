> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 使用遠端控制從任何裝置繼續本機工作階段

> 使用遠端控制從您的手機、平板電腦或任何瀏覽器繼續本機 Claude Code 工作階段。適用於 claude.ai/code 和 Claude 行動應用程式。

<Note>
  遠端控制適用於所有方案。Team 和 Enterprise 管理員必須先在[管理員設定](https://claude.ai/admin-settings/claude-code)中啟用 Claude Code。
</Note>

遠端控制將 [claude.ai/code](https://claude.ai/code) 或 Claude 應用程式（[iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) 和 [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude)）連接到在您機器上執行的 Claude Code 工作階段。在您的辦公桌開始一項任務，然後從沙發上的手機或另一台電腦上的瀏覽器繼續進行。

當您在機器上啟動遠端控制工作階段時，Claude 會在整個過程中在本機執行，因此沒有任何內容會移至雲端。使用遠端控制，您可以：

* **遠端使用您的完整本機環境**：您的檔案系統、[MCP servers](/zh-TW/mcp)、工具和專案設定都保持可用
* **同時在兩個介面上工作**：對話在所有連接的裝置上保持同步，因此您可以從終端機、瀏覽器和手機交替傳送訊息
* **度過中斷**：如果您的筆記型電腦進入睡眠狀態或網路中斷，當您的機器重新上線時，工作階段會自動重新連接

與在雲端基礎設施上執行的 [Claude Code on the web](/zh-TW/claude-code-on-the-web) 不同，遠端控制工作階段直接在您的機器上執行並與您的本機檔案系統互動。Web 和行動介面只是該本機工作階段的一個視窗。

<Note>
  遠端控制需要 Claude Code v2.1.51 或更新版本。使用 `claude --version` 檢查您的版本。
</Note>

本頁涵蓋設定、如何啟動和連接到工作階段，以及遠端控制與 Claude Code on the web 的比較。

## 需求

在使用遠端控制之前，請確認您的環境符合以下條件：

* **訂閱**：適用於 Pro、Max、Team 和 Enterprise 方案。Team 和 Enterprise 管理員必須先在[管理員設定](https://claude.ai/admin-settings/claude-code)中啟用 Claude Code。不支援 API 金鑰。
* **驗證**：執行 `claude` 並使用 `/login` 透過 claude.ai 登入（如果您還沒有登入）。
* **工作區信任**：在您的專案目錄中至少執行一次 `claude` 以接受工作區信任對話。

## 啟動遠端控制工作階段

您可以直接在遠端控制中啟動新工作階段，或連接已在執行的工作階段。

<Tabs>
  <Tab title="新工作階段">
    導覽至您的專案目錄並執行：

    ```bash  theme={null}
    claude remote-control
    ```

    該程序在您的終端機中保持執行，等待遠端連接。它顯示一個工作階段 URL，您可以使用該 URL 從另一個裝置[連接](#connect-from-another-device)，您可以按空格鍵顯示 QR 碼以從您的手機快速存取。當遠端工作階段處於活動狀態時，終端機會顯示連接狀態和工具活動。

    此命令支援以下旗標：

    * **`--name "My Project"`**：設定在 claude.ai/code 的工作階段清單中可見的自訂工作階段標題。您也可以將名稱作為位置引數傳遞：`claude remote-control "My Project"`
    * **`--verbose`**：顯示詳細的連接和工作階段日誌
    * **`--sandbox`** / **`--no-sandbox`**：啟用或停用工作階段期間檔案系統和網路隔離的[沙箱](/zh-TW/sandboxing)。預設情況下沙箱已關閉。
  </Tab>

  <Tab title="從現有工作階段">
    如果您已經在 Claude Code 工作階段中並想遠端繼續，請使用 `/remote-control`（或 `/rc`）命令：

    ```text  theme={null}
    /remote-control
    ```

    傳遞名稱作為引數以設定自訂工作階段標題：

    ```text  theme={null}
    /remote-control My Project
    ```

    這會啟動一個遠端控制工作階段，該工作階段會延續您目前的對話歷史記錄，並顯示一個工作階段 URL 和 QR 碼，您可以使用它從另一個裝置[連接](#connect-from-another-device)。`--verbose`、`--sandbox` 和 `--no-sandbox` 旗標不適用於此命令。
  </Tab>
</Tabs>

### 從另一個裝置連接

遠端控制工作階段啟動後，您有幾種方式可以從另一個裝置連接：

* **開啟工作階段 URL** 在任何瀏覽器中直接前往 [claude.ai/code](https://claude.ai/code) 上的工作階段。`claude remote-control` 和 `/remote-control` 都會在終端機中顯示此 URL。
* **掃描 QR 碼** 顯示在工作階段 URL 旁邊，直接在 Claude 應用程式中開啟它。使用 `claude remote-control` 時，按空格鍵切換 QR 碼顯示。
* **開啟 [claude.ai/code](https://claude.ai/code) 或 Claude 應用程式**，並在工作階段清單中按名稱找到工作階段。遠端控制工作階段在線上時會顯示帶有綠色狀態點的電腦圖示。

遠端工作階段從 `--name` 引數（或傳遞給 `/remote-control` 的名稱）、您的最後一條訊息、您的 `/rename` 值或「遠端控制工作階段」（如果沒有對話歷史記錄）取得其名稱。如果環境已經有一個活動工作階段，系統會詢問您是否要繼續它或啟動一個新工作階段。

如果您還沒有 Claude 應用程式，請在 Claude Code 內使用 `/mobile` 命令顯示 [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) 或 [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) 的下載 QR 碼。

### 為所有工作階段啟用遠端控制

預設情況下，遠端控制只在您明確執行 `claude remote-control` 或 `/remote-control` 時啟動。若要為每個工作階段自動啟用它，請在 Claude Code 內執行 `/config` 並將**為所有工作階段啟用遠端控制**設定為 `true`。將其設定回 `false` 以停用。

每個 Claude Code 執行個體一次支援一個遠端工作階段。如果您執行多個執行個體，每個執行個體都會獲得自己的環境和工作階段。

## 連接和安全性

您的本機 Claude Code 工作階段僅發出出站 HTTPS 請求，永遠不會在您的機器上開啟入站連接埠。當您啟動遠端控制時，它會向 Anthropic API 註冊並輪詢工作。當您從另一個裝置連接時，伺服器會透過串流連接在 Web 或行動用戶端與您的本機工作階段之間路由訊息。

所有流量都透過 TLS 上的 Anthropic API 傳輸，與任何 Claude Code 工作階段相同的傳輸安全性。連接使用多個短期認證，每個認證的範圍限定為單一目的並獨立過期。

## 遠端控制與 Claude Code on the web

遠端控制和 [Claude Code on the web](/zh-TW/claude-code-on-the-web) 都使用 claude.ai/code 介面。關鍵區別在於工作階段執行的位置：遠端控制在您的機器上執行，因此您的本機 MCP servers、工具和專案設定保持可用。Claude Code on the web 在 Anthropic 管理的雲端基礎設施中執行。

當您在本機工作中途並想從另一個裝置繼續時，請使用遠端控制。當您想在沒有任何本機設定的情況下啟動任務、處理您沒有複製的儲存庫或並行執行多個任務時，請使用 Claude Code on the web。

## 限制

* **一次一個遠端工作階段**：每個 Claude Code 工作階段支援一個遠端連接。
* **終端機必須保持開啟**：遠端控制作為本機程序執行。如果您關閉終端機或停止 `claude` 程序，工作階段就會結束。再次執行 `claude remote-control` 以啟動新工作階段。
* **延長網路中斷**：如果您的機器處於喚醒狀態但無法在大約 10 分鐘以上的時間內連接到網路，工作階段會逾時並且程序會退出。再次執行 `claude remote-control` 以啟動新工作階段。

## 相關資源

* [Claude Code on the web](/zh-TW/claude-code-on-the-web)：在 Anthropic 管理的雲端環境中執行工作階段，而不是在您的機器上
* [驗證](/zh-TW/authentication)：設定 `/login` 並管理 claude.ai 的認證
* [CLI 參考](/zh-TW/cli-reference)：完整的旗標和命令清單，包括 `claude remote-control`
* [安全性](/zh-TW/security)：遠端控制工作階段如何適應 Claude Code 安全性模型
* [資料使用](/zh-TW/data-usage)：在本機和遠端工作階段期間透過 Anthropic API 流動的資料
