> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 使用 Claude Code Desktop

> 充分利用 Claude Code Desktop：具有 Git 隔離的並行會話、視覺化差異檢查、應用程式預覽、PR 監控、權限模式、連接器和企業配置。

Claude Desktop 應用程式中的 Code 標籤讓您可以透過圖形介面而不是終端機來使用 Claude Code。

Desktop 在標準 Claude Code 體驗的基礎上增加了這些功能：

* [視覺化差異檢查](#review-changes-with-diff-view)，包含內嵌註解
* [即時應用程式預覽](#preview-your-app)，搭配開發伺服器
* [GitHub PR 監控](#monitor-pull-request-status)，具有自動修復和自動合併
* [並行會話](#work-in-parallel-with-sessions)，具有自動 Git worktree 隔離
* [排程任務](#schedule-recurring-tasks)，按照定期排程執行 Claude
* [連接器](#connect-external-tools)，用於 GitHub、Slack、Linear 等
* 本機、[SSH](#ssh-sessions) 和[雲端](#run-long-running-tasks-remotely)環境

<Tip>
  初次使用 Desktop？從[開始使用](/zh-TW/desktop-quickstart)開始安裝應用程式並進行第一次編輯。
</Tip>

本頁涵蓋[使用程式碼](#work-with-code)、[管理會話](#manage-sessions)、[擴展 Claude Code](#extend-claude-code)、[排程任務](#schedule-recurring-tasks)和[配置](#environment-configuration)。它還包括 [CLI 比較](#coming-from-the-cli)和[疑難排解](#troubleshooting)。

## 開始會話

在發送第一條訊息之前，在提示區域中配置四項內容：

* **環境**：選擇 Claude 執行的位置。選擇 **Local** 用於您的機器、**Remote** 用於 Anthropic 託管的雲端會話，或用於您管理的遠端機器的 [**SSH 連線**](#ssh-sessions)。請參閱[環境配置](#environment-configuration)。
* **專案資料夾**：選擇 Claude 工作的資料夾或儲存庫。對於遠端會話，您可以新增[多個儲存庫](#run-long-running-tasks-remotely)。
* **模型**：從傳送按鈕旁的下拉式選單中選擇[模型](/zh-TW/model-config#available-models)。會話開始後，模型會被鎖定。
* **權限模式**：從[模式選擇器](#choose-a-permission-mode)中選擇 Claude 擁有多少自主權。您可以在會話期間變更此設定。

輸入您的任務並按 **Enter** 開始。每個會話都會追蹤自己的上下文並獨立進行變更。

## 使用程式碼

為 Claude 提供正確的上下文，控制它自主執行的程度，並檢查它所做的變更。

### 使用提示框

輸入您希望 Claude 執行的操作，然後按 **Enter** 傳送。Claude 會讀取您的專案檔案、進行變更，並根據您的[權限模式](#choose-a-permission-mode)執行命令。您可以隨時中斷 Claude：按一下停止按鈕或輸入您的更正並按 **Enter**。Claude 會停止正在執行的操作並根據您的輸入進行調整。

提示框旁的 **+** 按鈕可讓您存取檔案附件、[skills](#use-skills)、[連接器](#connect-external-tools)和[plugins](#install-plugins)。

### 將檔案和上下文新增至提示

提示框支援兩種方式來引入外部上下文：

* **@mention 檔案**：輸入 `@` 後跟檔案名稱，將檔案新增至對話上下文。Claude 隨後可以讀取和參考該檔案。
* **附加檔案**：使用附件按鈕將影像、PDF 和其他檔案附加到您的提示，或直接將檔案拖放到提示中。這對於分享錯誤的螢幕截圖、設計模型或參考文件很有用。

### 選擇權限模式

權限模式控制 Claude 在會話期間擁有多少自主權：它是否在編輯檔案、執行命令或兩者之前詢問。您可以隨時使用傳送按鈕旁的模式選擇器切換模式。從「詢問權限」開始，以查看 Claude 確切執行的操作，然後隨著您變得更加熟悉，移至「自動接受編輯」或 Plan Mode。

| 模式            | 設定金鑰                | 行為                                                                                                                               |
| ------------- | ------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **詢問權限**      | `default`           | Claude 在編輯檔案或執行命令之前詢問。您會看到差異，並可以接受或拒絕每項變更。建議新使用者使用。                                                                              |
| **自動接受編輯**    | `acceptEdits`       | Claude 自動接受檔案編輯，但在執行終端機命令之前仍會詢問。當您信任檔案變更並希望更快速地迭代時，請使用此選項。                                                                       |
| **Plan Mode** | `plan`              | Claude 分析您的程式碼並建立計畫，而不修改檔案或執行命令。適合您想要先檢查方法的複雜任務。                                                                                 |
| **略過權限**      | `bypassPermissions` | Claude 執行時不會出現任何權限提示，相當於 CLI 中的 `--dangerously-skip-permissions`。在「設定」→「Claude Code」下的「允許略過權限模式」中啟用。僅在沙箱容器或 VM 中使用。企業管理員可以停用此選項。 |

`dontAsk` 權限模式僅在 [CLI](/zh-TW/permissions#permission-modes) 中可用。

<Tip title="最佳實踐">
  在 Plan Mode 中開始複雜任務，以便 Claude 在進行變更之前規劃方法。批准計畫後，切換到'自動接受編輯'或'詢問權限'以執行它。有關此工作流程的更多資訊，請參閱[先探索，然後計畫，然後編碼](/zh-TW/best-practices#explore-first-then-plan-then-code)。
</Tip>

遠端會話支援'自動接受編輯'和 Plan Mode。'詢問權限'不可用，因為遠端會話預設會自動接受檔案編輯，'略過權限'不可用，因為遠端環境已經是沙箱化的。

企業管理員可以限制哪些權限模式可用。有關詳細資訊，請參閱[企業配置](#enterprise-configuration)。

### 預覽您的應用程式

Claude 可以啟動開發伺服器並開啟嵌入式瀏覽器來驗證其變更。這適用於前端網路應用程式以及後端伺服器：Claude 可以測試 API 端點、檢視伺服器日誌，並對其發現的問題進行迭代。在大多數情況下，Claude 在編輯專案檔案後會自動啟動伺服器。您也可以隨時要求 Claude 進行預覽。預設情況下，Claude [自動驗證](#auto-verify-changes)每次編輯後的變更。

從預覽面板，您可以：

* 直接在嵌入式瀏覽器中與執行中的應用程式互動
* 觀看 Claude 自動驗證自己的變更：它會擷取螢幕截圖、檢查 DOM、按一下元素、填寫表單，並修復它發現的問題
* 從會話工具列中的 **Preview** 下拉式選單啟動或停止伺服器
* 透過在下拉式選單中選擇 **Persist sessions**，在伺服器重新啟動時保留 Cookie 和本機儲存，這樣您就不必在開發期間重新登入
* 編輯伺服器配置或一次停止所有伺服器

Claude 根據您的專案建立初始伺服器配置。如果您的應用程式使用自訂開發命令，請編輯 `.claude/launch.json` 以符合您的設定。有關完整參考，請參閱[配置預覽伺服器](#configure-preview-servers)。

若要清除已儲存的會話資料，請在'設定'→'Claude Code'中切換 **Persist preview sessions** 關閉。若要完全停用預覽，請在'設定'→'Claude Code'中切換 **Preview** 關閉。

### 使用差異檢查檢查變更

Claude 對您的程式碼進行變更後，差異檢查可讓您在建立提取請求之前逐個檔案檢查修改。

當 Claude 變更檔案時，會出現一個差異統計指示器，顯示新增和移除的行數，例如 `+12 -1`。按一下此指示器以開啟差異檢視器，該檢視器在左側顯示檔案清單，在右側顯示每個檔案的變更。

若要對特定行進行註解，請按一下差異中的任何行以開啟註解框。輸入您的回饋並按 **Enter** 新增註解。在多行新增註解後，一次提交所有註解：

* **macOS**：按 **Cmd+Enter**
* **Windows**：按 **Ctrl+Enter**

Claude 會讀取您的註解並進行要求的變更，這些變更會顯示為您可以檢查的新差異。

### 檢查您的程式碼

在差異檢查中，按一下右上角工具列中的 **Review code**，要求 Claude 在您提交之前評估變更。Claude 會檢查目前的差異，並直接在差異檢查中留下註解。您可以回應任何註解或要求 Claude 進行修訂。

檢查著重於高信號問題：編譯錯誤、明確的邏輯錯誤、安全漏洞和明顯的錯誤。它不會標記樣式、格式、預先存在的問題或 linter 會捕捉的任何內容。

### 監控提取請求狀態

開啟提取請求後，CI 狀態列會出現在會話中。Claude Code 使用 GitHub CLI 來輪詢檢查結果並顯示失敗。

* **自動修復**：啟用後，Claude 會透過讀取失敗輸出並進行迭代，自動嘗試修復失敗的 CI 檢查。
* **自動合併**：啟用後，Claude 會在所有檢查通過後合併 PR。合併方法是壓縮。自動合併必須在您的 GitHub 儲存庫設定中[啟用](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-auto-merge-for-pull-requests-in-your-repository)才能運作。

使用 CI 狀態列中的 **Auto-fix** 和 **Auto-merge** 切換來啟用任一選項。Claude Code 也會在 CI 完成時傳送桌面通知。

<Note>
  PR 監控需要在您的機器上安裝並驗證 [GitHub CLI (`gh`)](https://cli.github.com/)。如果未安裝 `gh`，Desktop 會在您第一次嘗試建立 PR 時提示您安裝它。
</Note>

## 管理會話

每個會話都是一個獨立的對話，具有自己的上下文和變更。您可以並行執行多個會話或將工作傳送到雲端。

### 使用會話並行工作

按一下側邊欄中的 **+ New session** 以並行處理多個任務。對於 Git 儲存庫，每個會話都會使用 [Git worktrees](/zh-TW/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) 獲得自己的隔離專案副本，因此一個會話中的變更不會影響其他會話，直到您提交它們。

Worktrees 預設儲存在 `<project-root>/.claude/worktrees/` 中。您可以在'設定'→'Claude Code'下的'Worktree location'中將其變更為自訂目錄。您也可以設定一個分支前綴，該前綴會被加到每個 worktree 分支名稱前面，這對於保持 Claude 建立的分支井然有序很有用。完成後，若要移除 worktree，請將滑鼠懸停在側邊欄中的會話上，然後按一下封存圖示。

<Note>
  會話隔離需要 [Git](https://git-scm.com/downloads)。大多數 Mac 預設包含 Git。在終端機中執行 `git --version` 進行檢查。在 Windows 上，Code 標籤需要 Git 才能運作：[下載 Git for Windows](https://git-scm.com/downloads/win)、安裝它，然後重新啟動應用程式。如果您遇到 Git 錯誤，請嘗試 Cowork 會話來幫助排除您的設定問題。
</Note>

使用側邊欄頂部的篩選圖示按狀態（Active、Archived）和環境（Local、Cloud）篩選會話。若要重新命名會話或檢查上下文使用情況，請按一下活動會話頂部工具列中的會話標題。當上下文填滿時，Claude 會自動總結對話並繼續工作。您也可以輸入 `/compact` 來更早觸發總結並釋放上下文空間。有關壓縮如何運作的詳細資訊，請參閱[上下文視窗](/zh-TW/how-claude-code-works#the-context-window)。

### 遠端執行長時間執行的任務

對於大型重構、測試套件、遷移或其他長時間執行的任務，在啟動會話時選擇 **Remote** 而不是 **Local**。遠端會話在 Anthropic 的雲端基礎設施上執行，即使您關閉應用程式或關閉電腦，也會繼續執行。隨時檢查以查看進度或引導 Claude 朝不同方向發展。您也可以從 [claude.ai/code](https://claude.ai/code) 或 Claude iOS 應用程式監控遠端會話。

遠端會話也支援多個儲存庫。選擇雲端環境後，按一下儲存庫藥丸旁的 **+** 按鈕，將其他儲存庫新增到會話中。每個儲存庫都有自己的分支選擇器。這對於跨越多個程式碼庫的任務很有用，例如更新共用程式庫及其使用者。

有關遠端會話如何運作的更多資訊，請參閱[網路上的 Claude Code](/zh-TW/claude-code-on-the-web)。

### 在另一個表面繼續

**Continue in** 選單可從會話工具列右下角的 VS Code 圖示存取，可讓您將會話移至另一個表面：

* **Claude Code on the Web**：將您的本機會話傳送到遠端繼續執行。Desktop 推送您的分支、產生對話摘要，並使用完整上下文建立新的遠端會話。然後您可以選擇封存本機會話或保留它。這需要乾淨的工作樹，不適用於 SSH 會話。
* **Your IDE**：在目前工作目錄的支援 IDE 中開啟您的專案。

## 擴展 Claude Code

連接外部服務、新增可重複使用的工作流程、自訂 Claude 的行為，並配置預覽伺服器。

### 連接外部工具

對於本機和 [SSH](#ssh-sessions) 會話，按一下提示框旁的 **+** 按鈕，然後選擇 **Connectors** 以新增 Google Calendar、Slack、GitHub、Linear、Notion 等整合。您可以在會話之前或期間新增連接器。遠端會話不提供連接器。

若要管理或斷開連接器，請在桌面應用程式中前往'設定'→'Connectors'，或從提示框中的'Connectors'選單中選擇 **Manage connectors**。

連接後，Claude 可以讀取您的日曆、傳送訊息、建立問題，並直接與您的工具互動。您可以詢問 Claude 在您的會話中配置了哪些連接器。

連接器是[MCP servers](/zh-TW/mcp)，具有圖形設定流程。使用它們可以快速與支援的服務整合。對於'連接器'中未列出的整合，透過[設定檔案](/zh-TW/mcp#installing-mcp-servers)手動新增 MCP servers。您也可以[建立自訂連接器](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp)。

### 使用 skills

[Skills](/zh-TW/skills) 擴展 Claude 可以執行的操作。Claude 在相關時自動載入它們，或者您可以直接呼叫一個：在提示框中輸入 `/` 或按一下 **+** 按鈕並選擇 **Slash commands** 以瀏覽可用的內容。這包括[內建命令](/zh-TW/interactive-mode#built-in-commands)、您的[自訂 skills](/zh-TW/skills#create-custom-skills)、來自您程式碼庫的專案 skills，以及來自任何[已安裝 plugins](/zh-TW/plugins) 的 skills。選擇一個，它會在輸入欄位中突出顯示。在其後輸入您的任務並照常傳送。

### 安裝 plugins

[Plugins](/zh-TW/plugins) 是可重複使用的套件，可將 skills、agents、hooks、MCP servers 和 LSP 配置新增到 Claude Code。您可以從桌面應用程式安裝 plugins，而無需使用終端機。

對於本機和 [SSH](#ssh-sessions) 會話，按一下提示框旁的 **+** 按鈕，然後選擇 **Plugins** 以查看您已安裝的 plugins 及其命令。若要新增 plugin，從子選單中選擇 **Add plugin** 以開啟 plugin 瀏覽器，該瀏覽器顯示來自您配置的[市場](/zh-TW/plugin-marketplaces)的可用 plugins，包括官方 Anthropic 市場。選擇 **Manage plugins** 以啟用、停用或解除安裝 plugins。

Plugins 可以限定於您的使用者帳戶、特定專案或僅限本機。遠端會話不提供 Plugins。有關完整的 plugin 參考（包括建立您自己的 plugins），請參閱 [plugins](/zh-TW/plugins)。

### 配置預覽伺服器

Claude 會自動偵測您的開發伺服器設定，並將配置儲存在啟動會話時選擇的資料夾根目錄中的 `.claude/launch.json`。Preview 使用此資料夾作為其工作目錄，因此如果您選擇了父資料夾，具有自己開發伺服器的子資料夾將不會自動偵測。若要使用子資料夾的伺服器，請直接在該資料夾中啟動會話，或手動新增配置。

若要自訂伺服器的啟動方式，例如使用 `yarn dev` 而不是 `npm run dev` 或變更連接埠，請手動編輯檔案或按一下 Preview 下拉式選單中的 **Edit configuration** 以在您的程式碼編輯器中開啟它。該檔案支援帶註解的 JSON。

```json  theme={null}
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "my-app",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "port": 3000
    }
  ]
}
```

您可以定義多個配置以從同一專案執行不同的伺服器，例如前端和 API。請參閱下面的[範例](#examples)。

#### 自動驗證變更

啟用 `autoVerify` 時，Claude 會在編輯檔案後自動驗證程式碼變更。它會擷取螢幕截圖、檢查錯誤，並在完成回應之前確認變更有效。

自動驗證預設為開啟。透過將 `"autoVerify": false` 新增到 `.claude/launch.json` 來按專案停用它，或從 **Preview** 下拉式選單切換它。

```json  theme={null}
{
  "version": "0.0.1",
  "autoVerify": false,
  "configurations": [...]
}
```

停用後，預覽工具仍然可用，您可以隨時要求 Claude 進行驗證。自動驗證使其在每次編輯後自動進行。

#### 配置欄位

`configurations` 陣列中的每個項目接受以下欄位：

| 欄位                  | 類型        | 描述                                                                                                    |
| ------------------- | --------- | ----------------------------------------------------------------------------------------------------- |
| `name`              | string    | 此伺服器的唯一識別碼                                                                                            |
| `runtimeExecutable` | string    | 要執行的命令，例如 `npm`、`yarn` 或 `node`                                                                       |
| `runtimeArgs`       | string\[] | 傳遞給 `runtimeExecutable` 的引數，例如 `["run", "dev"]`                                                       |
| `port`              | number    | 您的伺服器監聽的連接埠。預設為 3000                                                                                  |
| `cwd`               | string    | 相對於您的專案根目錄的工作目錄。預設為專案根目錄。使用 `${workspaceFolder}` 明確參考專案根目錄                                            |
| `env`               | object    | 其他環境變數作為鍵值對，例如 `{ "NODE_ENV": "development" }`。不要在此處放置機密，因為此檔案會提交到您的儲存庫。在您的 shell 設定檔中設定的機密會自動繼承。     |
| `autoPort`          | boolean   | 如何處理連接埠衝突。請參閱下面                                                                                       |
| `program`           | string    | 使用 `node` 執行的指令碼。請參閱[何時使用 `program` 與 `runtimeExecutable`](#when-to-use-program-vs-runtimeexecutable) |
| `args`              | string\[] | 傳遞給 `program` 的引數。僅在設定 `program` 時使用                                                                  |

##### 何時使用 `program` 與 `runtimeExecutable`

使用 `runtimeExecutable` 搭配 `runtimeArgs` 透過套件管理器啟動開發伺服器。例如，`"runtimeExecutable": "npm"` 搭配 `"runtimeArgs": ["run", "dev"]` 執行 `npm run dev`。

當您有想要直接使用 `node` 執行的獨立指令碼時，使用 `program`。例如，`"program": "server.js"` 執行 `node server.js`。使用 `args` 傳遞其他標誌。

#### 連接埠衝突

`autoPort` 欄位控制當您偏好的連接埠已在使用中時會發生什麼：

* **`true`**：Claude 自動尋找並使用空閒連接埠。適合大多數開發伺服器。
* **`false`**：Claude 失敗並出現錯誤。當您的伺服器必須使用特定連接埠時使用此選項，例如 OAuth 回呼或 CORS 允許清單。
* **未設定（預設）**：Claude 詢問伺服器是否需要該確切連接埠，然後儲存您的答案。

當 Claude 選擇不同的連接埠時，它會透過 `PORT` 環境變數將指派的連接埠傳遞給您的伺服器。

#### 範例

這些配置顯示不同專案類型的常見設定：

<Tabs>
  <Tab title="Next.js">
    此配置使用 Yarn 在連接埠 3000 上執行 Next.js 應用程式：

    ```json  theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "web",
          "runtimeExecutable": "yarn",
          "runtimeArgs": ["dev"],
          "port": 3000
        }
      ]
    }
    ```
  </Tab>

  <Tab title="Multiple servers">
    對於具有前端和 API 伺服器的 monorepo，定義多個配置。前端使用 `autoPort: true`，因此如果 3000 被佔用，它會選擇空閒連接埠，而 API 伺服器需要確切的連接埠 8080：

    ```json  theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "frontend",
          "runtimeExecutable": "npm",
          "runtimeArgs": ["run", "dev"],
          "cwd": "apps/web",
          "port": 3000,
          "autoPort": true
        },
        {
          "name": "api",
          "runtimeExecutable": "npm",
          "runtimeArgs": ["run", "start"],
          "cwd": "server",
          "port": 8080,
          "env": { "NODE_ENV": "development" },
          "autoPort": false
        }
      ]
    }
    ```
  </Tab>

  <Tab title="Node.js script">
    若要直接執行 Node.js 指令碼而不是使用套件管理器命令，請使用 `program` 欄位：

    ```json  theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "server",
          "program": "server.js",
          "args": ["--verbose"],
          "port": 4000
        }
      ]
    }
    ```
  </Tab>
</Tabs>

## 排程定期任務

排程任務會在您選擇的時間和頻率自動啟動新的本機會話。使用它們進行定期工作，例如每日程式碼檢查、相依性更新檢查或從您的日曆和收件箱提取的早晨簡報。

任務在您的機器上執行，因此桌面應用程式必須開啟且您的電腦保持清醒才能觸發它們。有關錯過的執行和追趕行為的詳細資訊，請參閱[排程任務如何執行](#how-scheduled-tasks-run)。

<Note>
  預設情況下，排程任務針對您的工作目錄所處的任何狀態執行，包括未提交的變更。在提示輸入中啟用 worktree 切換，以為每次執行提供自己的隔離 Git worktree，與[並行會話](#work-in-parallel-with-sessions)的方式相同。
</Note>

若要建立排程任務，請按一下側邊欄中的 **Schedule**，然後按 **+ New task**。配置這些欄位：

| 欄位          | 描述                                                                               |
| ----------- | -------------------------------------------------------------------------------- |
| Name        | 任務的識別碼。轉換為小寫 kebab-case 並用作磁碟上的資料夾名稱。在您的任務中必須是唯一的。                               |
| Description | 任務清單中顯示的簡短摘要。                                                                    |
| Prompt      | 任務執行時傳送給 Claude 的指示。以您在提示框中編寫任何訊息的相同方式編寫此內容。提示輸入還包括模型、權限模式、工作資料夾和 worktree 的控制項。 |
| Frequency   | 任務執行的頻率。請參閱下面的[頻率選項](#frequency-options)。                                        |

您也可以透過在任何會話中描述您想要的內容來建立任務。例如，「設定一個每天早上 9 點執行的每日程式碼檢查。」

### 頻率選項

* **Manual**：無排程，僅在您按一下 **Run now** 時執行。適合儲存您按需觸發的提示
* **Hourly**：每小時執行一次。每個任務從整點開始獲得最多 10 分鐘的固定偏移，以錯開 API 流量
* **Daily**：顯示時間選擇器，預設為當地時間上午 9:00
* **Weekdays**：與 Daily 相同，但跳過星期六和星期日
* **Weekly**：顯示時間選擇器和日期選擇器

對於選擇器不提供的間隔（每 15 分鐘、每月第一天等），在任何 Desktop 會話中詢問 Claude 設定排程。使用純文字；例如，「排程一個任務每 6 小時執行一次所有測試。」

### 排程任務如何執行

排程任務在您的機器上本機執行。Desktop 在應用程式開啟時每分鐘檢查一次排程，並在任務到期時啟動新會話，獨立於您開啟的任何手動會話。每個任務在排程時間後獲得最多 10 分鐘的固定延遲，以錯開 API 流量。延遲是確定性的：同一任務始終在相同的偏移處啟動。

當任務觸發時，您會收到桌面通知，新會話會出現在側邊欄的 **Scheduled** 部分下。開啟它以查看 Claude 執行的操作、檢查變更或回應權限提示。會話的工作方式與任何其他會話相同：Claude 可以編輯檔案、執行命令、建立提交和開啟提取請求。

任務僅在桌面應用程式執行且您的電腦清醒時執行。如果您的電腦在排程時間內進入睡眠狀態，執行會被跳過。若要防止閒置睡眠，請在「設定」下的 **Desktop app → General** 中啟用 **Keep computer awake**。關閉筆記本電腦蓋仍會使其進入睡眠狀態。

### 錯過的執行

當應用程式啟動或您的電腦喚醒時，Desktop 會檢查每個任務是否在過去七天內錯過了任何執行。如果有，Desktop 會為最近錯過的時間啟動恰好一次追趕執行，並丟棄任何較舊的執行。每日任務錯過六天會在喚醒時執行一次。Desktop 會在追趕執行啟動時顯示通知。

編寫提示時請記住這一點。排程在上午 9 點的任務可能在晚上 11 點執行，如果您的電腦整天都在睡眠狀態。如果時間很重要，請在提示本身中新增護欄，例如：「僅檢查今天的提交。如果已過下午 5 點，請跳過檢查，只發佈錯過內容的摘要。」

### 排程任務的權限

每個任務都有自己的權限模式，您在建立或編輯任務時設定。來自 `~/.claude/settings.json` 的允許規則也適用於排程任務會話。如果任務在詢問模式下執行並需要執行它沒有權限的工具，執行會停滯，直到您批准它。會話保持在側邊欄中開啟，以便您稍後可以回答。

若要避免停滯，請在建立任務後按一下 **Run now**，觀察權限提示，並為每個提示選擇「always allow」。該任務的未來執行會自動批准相同的工具，而無需提示。您可以從任務的詳細資訊頁面檢查和撤銷這些批准。

### 管理排程任務

按一下 **Schedule** 清單中的任務以開啟其詳細資訊頁面。從這裡您可以：

* **Run now**：立即啟動任務，無需等待下一個排程時間
* **Toggle repeats**：暫停或恢復排程執行，而無需刪除任務
* **Edit**：變更提示、頻率、資料夾或其他設定
* **Review history**：查看每次過去的執行，包括因您的電腦睡眠而被跳過的執行
* **Review allowed permissions**：從 **Always allowed** 面板查看和撤銷此任務的已儲存工具批准
* **Delete**：移除任務並封存它建立的所有會話

您也可以透過在任何 Desktop 會話中詢問 Claude 來管理任務。例如，「暫停我的 dependency-audit 任務」、「刪除 standup-prep 任務」或「顯示我的排程任務。」

若要在磁碟上編輯任務的提示，請開啟 `~/.claude/scheduled-tasks/<task-name>/SKILL.md`（或在設定 [`CLAUDE_CONFIG_DIR`](/zh-TW/settings#environment-variables) 時在其下）。該檔案使用 YAML frontmatter 用於 `name` 和 `description`，提示作為正文。變更在下一次執行時生效。排程、資料夾、模型和啟用狀態不在此檔案中：透過編輯表單或詢問 Claude 來變更它們。

## 環境配置

您在[啟動會話](#start-a-session)時選擇的環境決定了 Claude 執行的位置以及您如何連接：

* **Local**：在您的機器上執行，直接存取您的檔案
* **Remote**：在 Anthropic 的雲端基礎設施上執行。即使您關閉應用程式，會話也會繼續。
* **SSH**：在您透過 SSH 連接的遠端機器上執行，例如您自己的伺服器、雲端 VM 或開發容器

### 本機會話

本機會話從您的 shell 繼承環境變數。如果您需要其他變數，請在您的 shell 設定檔（例如 `~/.zshrc` 或 `~/.bashrc`）中設定它們，並重新啟動桌面應用程式。有關支援的變數的完整清單，請參閱[環境變數](/zh-TW/settings#environment-variables)。

[擴展思考](/zh-TW/common-workflows#use-extended-thinking-thinking-mode)預設啟用，這改進了複雜推理任務的效能，但使用額外的 tokens。若要完全停用思考，請在您的 shell 設定檔中設定 `MAX_THINKING_TOKENS=0`。在 Opus 上，除了 `0` 外，`MAX_THINKING_TOKENS` 會被忽略，因為自適應推理控制思考深度。

### 遠端會話

遠端會話即使在您關閉應用程式後也會在背景繼續。使用量計入您的[訂閱計畫限制](/zh-TW/costs)，沒有單獨的計算費用。

您可以建立具有不同網路存取級別和環境變數的自訂雲端環境。在啟動遠端會話時選擇環境下拉式選單，然後選擇 **Add environment**。有關配置網路存取和環境變數的詳細資訊，請參閱[雲端環境](/zh-TW/claude-code-on-the-web#cloud-environment)。

### SSH 會話

SSH 會話讓您在遠端機器上執行 Claude Code，同時使用桌面應用程式作為您的介面。這對於使用位於雲端 VM、開發容器或具有特定硬體或相依性的伺服器上的程式碼庫很有用。

若要新增 SSH 連線，請在啟動會話之前按一下環境下拉式選單，然後選擇 **+ Add SSH connection**。對話框要求：

* **Name**：此連線的友善標籤
* **SSH Host**：`user@hostname` 或在 `~/.ssh/config` 中定義的主機
* **SSH Port**：如果留空則預設為 22，或使用您的 SSH 配置中的連接埠
* **Identity File**：您的私鑰的路徑，例如 `~/.ssh/id_rsa`。留空以使用預設金鑰或您的 SSH 配置。

新增後，連線會出現在環境下拉式選單中。選擇它以在該機器上啟動會話。Claude 在遠端機器上執行，可以存取其檔案和工具。

Claude Code 必須安裝在遠端機器上。連接後，SSH 會話支援權限模式、連接器、plugins 和 MCP servers。

## 企業配置

Teams 或 Enterprise 計畫上的組織可以透過管理員主控台控制、受管設定檔案和裝置管理原則來管理桌面應用程式行為。

### 管理員主控台控制

這些設定透過[管理員設定主控台](https://claude.ai/admin-settings/claude-code)配置：

* **啟用或停用 Code 標籤**：控制您組織中的使用者是否可以在桌面應用程式中存取 Claude Code
* **停用略過權限模式**：防止您組織中的使用者啟用略過權限模式
* **停用網路上的 Claude Code**：為您的組織啟用或停用遠端會話

### 受管設定

受管設定會覆蓋專案和使用者設定，並在 Desktop 產生 CLI 會話時套用。您可以在組織的[受管設定](/zh-TW/settings#settings-precedence)檔案中設定這些金鑰，或透過管理員主控台遠端推送它們。

| 金鑰                             | 描述                                                                                  |
| ------------------------------ | ----------------------------------------------------------------------------------- |
| `disableBypassPermissionsMode` | 設定為 `"disable"` 以防止使用者啟用略過權限模式。請參閱[受管設定](/zh-TW/permissions#managed-only-settings)。 |

有關受管專用設定（包括 `allowManagedPermissionRulesOnly` 和 `allowManagedHooksOnly`）的完整清單，請參閱[受管專用設定](/zh-TW/permissions#managed-only-settings)。

透過管理員主控台上傳的遠端受管設定目前僅適用於 CLI 和 IDE 會話。對於 Desktop 特定的限制，請使用上面的管理員主控台控制。

### 裝置管理原則

IT 團隊可以透過 macOS 上的 MDM 或 Windows 上的群組原則來管理桌面應用程式。可用的原則包括啟用或停用 Claude Code 功能、控制自動更新和設定自訂部署 URL。

* **macOS**：使用 Jamf 或 Kandji 等工具透過 `com.anthropic.Claude` 偏好設定網域配置
* **Windows**：透過 `SOFTWARE\Policies\Claude` 的登錄配置

### 驗證和 SSO

企業組織可以要求所有使用者進行 SSO。有關計畫級別的詳細資訊，請參閱[驗證](/zh-TW/authentication)，有關 SAML 和 OIDC 配置，請參閱[設定 SSO](https://support.claude.com/en/articles/13132885-setting-up-single-sign-on-sso)。

### 資料處理

Claude Code 在本機會話中本機處理您的程式碼，或在遠端會話中在 Anthropic 的雲端基礎設施上處理。對話和程式碼上下文會傳送到 Anthropic 的 API 進行處理。有關資料保留、隱私和合規性的詳細資訊，請參閱[資料處理](/zh-TW/data-usage)。

### 部署

Desktop 可以透過企業部署工具分發：

* **macOS**：透過 MDM（例如 Jamf 或 Kandji）使用 `.dmg` 安裝程式分發
* **Windows**：透過 MSIX 套件或 `.exe` 安裝程式部署。有關企業部署選項（包括無聲安裝），請參閱[為 Windows 部署 Claude Desktop](https://support.claude.com/en/articles/12622703-deploy-claude-desktop-for-windows)

有關網路配置（例如代理設定、防火牆允許清單和 LLM 閘道），請參閱[網路配置](/zh-TW/network-config)。

有關完整的企業配置參考，請參閱[企業配置指南](https://support.claude.com/en/articles/12622667-enterprise-configuration)。

## 來自 CLI？

如果您已經使用 Claude Code CLI，Desktop 會執行相同的基礎引擎，但具有圖形介面。您可以在同一機器上同時執行兩者，甚至在同一專案上執行。每個都維護單獨的會話歷史記錄，但它們透過 CLAUDE.md 檔案共用配置和專案記憶。

若要將 CLI 會話移至 Desktop，請在終端機中執行 `/desktop`。Claude 會儲存您的會話並在桌面應用程式中開啟它，然後退出 CLI。此命令僅在 macOS 和 Windows 上可用。

<Tip>
  何時使用 Desktop 與 CLI：當您想要視覺化差異檢查、檔案附件或側邊欄中的會話管理時，請使用 Desktop。當您需要指令碼、自動化、第三方提供者或偏好終端機工作流程時，請使用 CLI。
</Tip>

### CLI 標誌等效項

此表顯示常見 CLI 標誌的桌面應用程式等效項。未列出的標誌沒有桌面等效項，因為它們是為指令碼或自動化設計的。

| CLI                                   | Desktop 等效項                                                                 |
| ------------------------------------- | --------------------------------------------------------------------------- |
| `--model sonnet`                      | 傳送按鈕旁的模型下拉式選單，在啟動會話之前                                                       |
| `--resume`, `--continue`              | 按一下側邊欄中的會話                                                                  |
| `--permission-mode`                   | 傳送按鈕旁的模式選擇器                                                                 |
| `--dangerously-skip-permissions`      | 略過權限模式。在「設定」→「Claude Code」→「Allow bypass permissions mode」中啟用。企業管理員可以停用此設定。 |
| `--add-dir`                           | 在遠端會話中使用 **+** 按鈕新增多個儲存庫                                                    |
| `--allowedTools`, `--disallowedTools` | 在 Desktop 中不可用                                                              |
| `--verbose`                           | 不可用。檢查系統日誌：macOS 上的 Console.app、Windows 上的「事件檢視器」→「Windows 日誌」→「應用程式」       |
| `--print`, `--output-format`          | 不可用。Desktop 僅限互動。                                                           |
| `ANTHROPIC_MODEL` env var             | 傳送按鈕旁的模型下拉式選單                                                               |
| `MAX_THINKING_TOKENS` env var         | 在 shell 設定檔中設定；適用於本機會話。請參閱[環境配置](#environment-configuration)。               |

### 共用配置

Desktop 和 CLI 讀取相同的配置檔案，因此您的設定會轉移：

* **[CLAUDE.md](/zh-TW/memory)** 檔案在您的專案中由兩者使用
* **[MCP servers](/zh-TW/mcp)** 在 `~/.claude.json` 或 `.mcp.json` 中配置的在兩者中都有效
* **[Hooks](/zh-TW/hooks)** 和 **[skills](/zh-TW/skills)** 在設定中定義的適用於兩者
* **[Settings](/zh-TW/settings)** 在 `~/.claude.json` 和 `~/.claude/settings.json` 中是共用的。`settings.json` 中的權限規則、允許的工具和其他設定適用於 Desktop 會話。
* **Models**：Sonnet、Opus 和 Haiku 在兩者中都可用。在 Desktop 中，在啟動會話之前從傳送按鈕旁的下拉式選單中選擇模型。您無法在活動會話期間變更模型。

<Note>
  **MCP servers：桌面聊天應用程式與 Claude Code**：在 `claude_desktop_config.json` 中為 Claude Desktop 聊天應用程式配置的 MCP servers 與 Claude Code 分開，不會出現在 Code 標籤中。若要在 Claude Code 中使用 MCP servers，請在 `~/.claude.json` 或您的專案的 `.mcp.json` 檔案中配置它們。有關詳細資訊，請參閱 [MCP 配置](/zh-TW/mcp#installing-mcp-servers)。
</Note>

### 功能比較

此表比較 CLI 和 Desktop 之間的核心功能。有關 CLI 標誌的完整清單，請參閱 [CLI 參考](/zh-TW/cli-reference)。

| 功能                                        | CLI                                                            | Desktop                                                       |
| ----------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------- |
| 權限模式                                      | 所有模式，包括 `dontAsk`                                              | 詢問權限、自動接受編輯、Plan Mode 和透過「設定」的略過權限                            |
| `--dangerously-skip-permissions`          | CLI 標誌                                                         | 略過權限模式。在「設定」→「Claude Code」→「Allow bypass permissions mode」中啟用 |
| [第三方提供者](/zh-TW/third-party-integrations) | Bedrock、Vertex、Foundry                                         | 不可用。Desktop 直接連接到 Anthropic 的 API。                            |
| [MCP servers](/zh-TW/mcp)                 | 在設定檔案中配置                                                       | 本機和 SSH 會話的連接器 UI，或設定檔案                                       |
| [Plugins](/zh-TW/plugins)                 | `/plugin` 命令                                                   | plugin 管理器 UI                                                 |
| @mention 檔案                               | 文字型                                                            | 帶自動完成                                                         |
| 檔案附件                                      | 不可用                                                            | 影像、PDF                                                        |
| 會話隔離                                      | [`--worktree`](/zh-TW/cli-reference) 標誌                        | 自動 worktrees                                                  |
| 多個會話                                      | 單獨的終端機                                                         | 側邊欄標籤                                                         |
| 定期任務                                      | cron 工作、CI 管道                                                  | [排程任務](#schedule-recurring-tasks)                             |
| 指令碼和自動化                                   | [`--print`](/zh-TW/cli-reference)、[Agent SDK](/zh-TW/headless) | 不可用                                                           |

### Desktop 中不可用的內容

以下功能僅在 CLI 或 VS Code 擴充功能中可用：

* **第三方提供者**：Desktop 直接連接到 Anthropic 的 API。改用 [CLI](/zh-TW/quickstart) 搭配 Bedrock、Vertex 或 Foundry。
* **Linux**：桌面應用程式僅在 macOS 和 Windows 上可用。
* **內嵌程式碼建議**：Desktop 不提供自動完成樣式的建議。它透過對話提示和明確的程式碼變更進行工作。
* **Agent teams**：多代理協調可透過 [CLI](/zh-TW/agent-teams) 和 [Agent SDK](/zh-TW/headless) 使用，不在 Desktop 中。

## 疑難排解

### 檢查您的版本

若要查看您執行的桌面應用程式版本：

* **macOS**：按一下選單列中的 **Claude**，然後按 **About Claude**
* **Windows**：按一下 **Help**，然後按 **About**

按一下版本號碼將其複製到您的剪貼簿。

### Code 標籤中的 403 或驗證錯誤

如果在使用 Code 標籤時看到 `Error 403: Forbidden` 或其他驗證失敗：

1. 從應用程式選單登出並重新登入。這是最常見的修復。
2. 驗證您有有效的付費訂閱：Pro、Max、Teams 或 Enterprise。
3. 如果 CLI 有效但 Desktop 無效，請完全退出桌面應用程式（不只是關閉視窗），然後重新開啟並登入。
4. 檢查您的網際網路連線和代理設定。

### 啟動時螢幕空白或卡住

如果應用程式開啟但顯示空白或無反應的螢幕：

1. 重新啟動應用程式。
2. 檢查待處理的更新。應用程式在啟動時自動更新。
3. 在 Windows 上，檢查「事件檢視器」中的崩潰日誌，位於 **Windows 日誌 → 應用程式**。

### 「Failed to load session」

如果您看到 `Failed to load session`，選定的資料夾可能不再存在、Git 儲存庫可能需要未安裝的 Git LFS，或檔案權限可能阻止存取。嘗試選擇不同的資料夾或重新啟動應用程式。

### 會話找不到已安裝的工具

如果 Claude 找不到 `npm`、`node` 或其他 CLI 命令等工具，請驗證工具在您的常規終端機中有效、檢查您的 shell 設定檔是否正確設定 PATH，並重新啟動桌面應用程式以重新載入環境變數。

### Git 和 Git LFS 錯誤

在 Windows 上，Git 是啟動本機會話的 Code 標籤所需的。如果您看到「Git is required」，請安裝 [Git for Windows](https://git-scm.com/downloads/win) 並重新啟動應用程式。

如果您看到「Git LFS is required by this repository but is not installed」，請從 [git-lfs.com](https://git-lfs.com/) 安裝 Git LFS，執行 `git lfs install`，然後重新啟動應用程式。

### Windows 上的 MCP servers 無法運作

如果 MCP server 切換沒有回應或伺服器在 Windows 上無法連接，請檢查伺服器是否在您的設定中正確配置、重新啟動應用程式、驗證伺服器程序在工作管理員中執行，並檢查伺服器日誌以查看連接錯誤。

### 應用程式無法退出

* **macOS**：按 Cmd+Q。如果應用程式沒有回應，請使用 Cmd+Option+Esc 強制退出，選擇 Claude，然後按「強制退出」。
* **Windows**：使用 Ctrl+Shift+Esc 的工作管理員來結束 Claude 程序。

### Windows 特定問題

* **安裝後 PATH 未更新**：開啟新的終端機視窗。PATH 更新僅適用於新的終端機會話。
* **並行安裝錯誤**：如果您看到有關另一個安裝進行中的錯誤，但實際上沒有，請嘗試以管理員身份執行安裝程式。
* **ARM64**：Windows ARM64 裝置完全支援。

### Intel Mac 上的 Cowork 標籤不可用

Cowork 標籤在 macOS 上需要 Apple Silicon（M1 或更新版本）。在 Windows 上，Cowork 在所有支援的硬體上可用。Chat 和 Code 標籤在 Intel Mac 上正常運作。

### 在 CLI 中開啟時「Branch doesn't exist yet」

遠端會話可以建立在您的本機機器上不存在的分支。按一下會話工具列中的分支名稱以複製它，然後在本機提取它：

```bash  theme={null}
git fetch origin <branch-name>
git checkout <branch-name>
```

### 仍然卡住？

* 在 [GitHub Issues](https://github.com/anthropics/claude-code/issues) 上搜尋或提交錯誤
* 造訪 [Claude 支援中心](https://support.claude.com/)

提交錯誤時，請包括您的桌面應用程式版本、您的作業系統、確切的錯誤訊息和相關日誌。在 macOS 上，檢查 Console.app。在 Windows 上，檢查「事件檢視器」→「Windows 日誌」→「應用程式」。
