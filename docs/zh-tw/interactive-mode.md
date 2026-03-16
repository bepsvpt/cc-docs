> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 互動模式

> Claude Code 會話中鍵盤快捷鍵、輸入模式和互動功能的完整參考。

## 鍵盤快捷鍵

<Note>
  鍵盤快捷鍵可能因平台和終端而異。按 `?` 查看您環境中可用的快捷鍵。

  **macOS 使用者**：Option/Alt 鍵快捷鍵（`Alt+B`、`Alt+F`、`Alt+Y`、`Alt+M`、`Alt+P`）需要在終端中將 Option 配置為 Meta：

  * **iTerm2**：設定 → 設定檔 → 鍵 → 將左/右 Option 鍵設定為「Esc+」
  * **Terminal.app**：設定 → 設定檔 → 鍵盤 → 勾選「使用 Option 作為 Meta 鍵」
  * **VS Code**：設定 → 設定檔 → 鍵 → 將左/右 Option 鍵設定為「Esc+」

  詳見[終端配置](/zh-TW/terminal-config)。
</Note>

### 一般控制

| 快捷鍵                                          | 說明                    | 上下文                                        |
| :------------------------------------------- | :-------------------- | :----------------------------------------- |
| `Ctrl+C`                                     | 取消目前輸入或生成             | 標準中斷                                       |
| `Ctrl+F`                                     | 終止所有背景代理。在 3 秒內按兩次以確認 | 背景代理控制                                     |
| `Ctrl+D`                                     | 退出 Claude Code 會話     | EOF 信號                                     |
| `Ctrl+G`                                     | 在預設文字編輯器中開啟           | 在預設文字編輯器中編輯您的提示或自訂回應                       |
| `Ctrl+L`                                     | 清除終端螢幕                | 保留對話歷史                                     |
| `Ctrl+O`                                     | 切換詳細輸出                | 顯示詳細的工具使用和執行情況                             |
| `Ctrl+R`                                     | 反向搜尋命令歷史              | 以互動方式搜尋先前的命令                               |
| `Ctrl+V` 或 `Cmd+V`（iTerm2）或 `Alt+V`（Windows） | 從剪貼簿貼上影像              | 貼上影像或影像檔案的路徑                               |
| `Ctrl+B`                                     | 背景執行工作                | 將 bash 命令和代理放在背景執行。Tmux 使用者按兩次             |
| `Ctrl+T`                                     | 切換工作清單                | 在終端狀態區域中顯示或隱藏[工作清單](#task-list)            |
| `Left/Right arrows`                          | 在對話框標籤之間循環            | 在權限對話框和選單中的標籤之間導航                          |
| `Up/Down arrows`                             | 導航命令歷史                | 回憶先前的輸入                                    |
| `Esc` + `Esc`                                | 回溯或摘要                 | 將程式碼和/或對話恢復到先前的點，或從選定的訊息進行摘要               |
| `Shift+Tab` 或 `Alt+M`（某些配置）                  | 切換權限模式                | 在自動接受模式、Plan Mode 和正常模式之間切換。               |
| `Option+P`（macOS）或 `Alt+P`（Windows/Linux）    | 切換模型                  | 在不清除提示的情況下切換模型                             |
| `Option+T`（macOS）或 `Alt+T`（Windows/Linux）    | 切換擴展思考                | 啟用或停用擴展思考模式。首先執行 `/terminal-setup` 以啟用此快捷鍵 |

### 文字編輯

| 快捷鍵                    | 說明          | 上下文                                                                 |
| :--------------------- | :---------- | :------------------------------------------------------------------ |
| `Ctrl+K`               | 刪除到行尾       | 儲存已刪除的文字以供貼上                                                        |
| `Ctrl+U`               | 刪除整行        | 儲存已刪除的文字以供貼上                                                        |
| `Ctrl+Y`               | 貼上已刪除的文字    | 貼上使用 `Ctrl+K` 或 `Ctrl+U` 刪除的文字                                      |
| `Alt+Y`（在 `Ctrl+Y` 之後） | 循環貼上歷史      | 貼上後，循環瀏覽先前刪除的文字。在 macOS 上需要[將 Option 設定為 Meta](#keyboard-shortcuts) |
| `Alt+B`                | 將游標向後移動一個單字 | 單字導航。在 macOS 上需要[將 Option 設定為 Meta](#keyboard-shortcuts)            |
| `Alt+F`                | 將游標向前移動一個單字 | 單字導航。在 macOS 上需要[將 Option 設定為 Meta](#keyboard-shortcuts)            |

### 主題和顯示

| 快捷鍵      | 說明             | 上下文                                            |
| :------- | :------------- | :--------------------------------------------- |
| `Ctrl+T` | 切換程式碼區塊的語法醒目提示 | 僅在 `/theme` 選擇器選單內有效。控制 Claude 回應中的程式碼是否使用語法著色 |

<Note>
  語法醒目提示僅在 Claude Code 的原生版本中可用。
</Note>

### 多行輸入

| 方法          | 快捷鍵            | 上下文                                  |
| :---------- | :------------- | :----------------------------------- |
| 快速逃脫        | `\` + `Enter`  | 適用於所有終端                              |
| macOS 預設    | `Option+Enter` | macOS 上的預設                           |
| Shift+Enter | `Shift+Enter`  | 在 iTerm2、WezTerm、Ghostty、Kitty 中開箱即用 |
| 控制序列        | `Ctrl+J`       | 多行的換行符                               |
| 貼上模式        | 直接貼上           | 適用於程式碼區塊、日誌                          |

<Tip>
  Shift+Enter 在 iTerm2、WezTerm、Ghostty 和 Kitty 中無需配置即可使用。對於其他終端（VS Code、Alacritty、Zed、Warp），執行 `/terminal-setup` 以安裝繫結。
</Tip>

### 快速命令

| 快捷鍵     | 說明        | 備註                                                     |
| :------ | :-------- | :----------------------------------------------------- |
| `/` 在開始 | 命令或 skill | 請參閱[內建命令](#built-in-commands)和 [skills](/zh-TW/skills) |
| `!` 在開始 | Bash 模式   | 直接執行命令並將執行輸出新增到會話                                      |
| `@`     | 檔案路徑提及    | 觸發檔案路徑自動完成                                             |

## 內建命令

在 Claude Code 中輸入 `/` 以查看所有可用命令，或輸入 `/` 後跟任何字母以篩選。並非所有命令對每個使用者都可見。有些取決於您的平台、計畫或環境。例如，`/desktop` 僅在 macOS 和 Windows 上出現，`/upgrade` 和 `/privacy-settings` 僅在 Pro 和 Max 計畫上可用，而 `/terminal-setup` 在您的終端原生支援其快捷鍵時隱藏。

Claude Code 還附帶[捆綁的 skills](/zh-TW/skills#bundled-skills)，例如 `/simplify`、`/batch` 和 `/debug`，當您輸入 `/` 時會與內建命令一起出現。若要建立您自己的命令，請參閱 [skills](/zh-TW/skills)。

在下表中，`<arg>` 表示必需的引數，`[arg]` 表示可選的引數。

| 命令                        | 用途                                                                                                                                                                                 |
| :------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/add-dir <path>`         | 將新的工作目錄新增到目前會話                                                                                                                                                                     |
| `/agents`                 | 管理 [agent](/zh-TW/sub-agents) 配置                                                                                                                                                   |
| `/btw <question>`         | 提出快速[側面問題](#side-questions-with-%2Fbtw)，無需新增到對話                                                                                                                                    |
| `/chrome`                 | 配置[Chrome 中的 Claude](/zh-TW/chrome) 設定                                                                                                                                             |
| `/clear`                  | 清除對話歷史並釋放上下文。別名：`/reset`、`/new`                                                                                                                                                    |
| `/compact [instructions]` | 壓縮對話，可選擇焦點指示                                                                                                                                                                       |
| `/config`                 | 開啟[設定](/zh-TW/settings)介面以調整主題、模型、[輸出樣式](/zh-TW/output-styles)和其他偏好設定。別名：`/settings`                                                                                               |
| `/context`                | 將目前上下文使用情況視覺化為彩色網格                                                                                                                                                                 |
| `/copy`                   | 將最後一個助手回應複製到剪貼簿。當存在程式碼區塊時，顯示互動式選擇器以選擇個別區塊或完整回應                                                                                                                                     |
| `/cost`                   | 顯示 token 使用統計資訊。詳見[成本追蹤指南](/zh-TW/costs#using-the-cost-command)以了解訂閱特定詳細資訊                                                                                                         |
| `/desktop`                | 在 Claude Code 桌面應用程式中繼續目前會話。僅限 macOS 和 Windows。別名：`/app`                                                                                                                           |
| `/diff`                   | 開啟互動式差異檢視器，顯示未提交的變更和每個回合的差異。使用左/右箭頭在目前 git 差異和個別 Claude 回合之間切換，使用上/下瀏覽檔案                                                                                                           |
| `/doctor`                 | 診斷並驗證您的 Claude Code 安裝和設定                                                                                                                                                          |
| `/exit`                   | 退出 CLI。別名：`/quit`                                                                                                                                                                  |
| `/export [filename]`      | 將目前對話匯出為純文字。使用檔案名稱時，直接寫入該檔案。不使用時，開啟對話框以複製到剪貼簿或儲存到檔案                                                                                                                                |
| `/extra-usage`            | 配置額外使用量以在達到速率限制時繼續工作                                                                                                                                                               |
| `/fast [on\|off]`         | 切換 [fast mode](/zh-TW/fast-mode) 開啟或關閉                                                                                                                                             |
| `/feedback [report]`      | 提交有關 Claude Code 的意見反應。別名：`/bug`                                                                                                                                                   |
| `/fork [name]`            | 在此點建立目前對話的分支                                                                                                                                                                       |
| `/help`                   | 顯示說明和可用命令                                                                                                                                                                          |
| `/hooks`                  | 管理工具事件的 [hook](/zh-TW/hooks) 配置                                                                                                                                                    |
| `/ide`                    | 管理 IDE 整合並顯示狀態                                                                                                                                                                     |
| `/init`                   | 使用 `CLAUDE.md` 指南初始化專案                                                                                                                                                             |
| `/insights`               | 生成分析您的 Claude Code 會話的報告，包括專案區域、互動模式和摩擦點                                                                                                                                           |
| `/install-github-app`     | 為存放庫設定 [Claude GitHub Actions](/zh-TW/github-actions) 應用程式。引導您選擇存放庫並配置整合                                                                                                           |
| `/install-slack-app`      | 安裝 Claude Slack 應用程式。開啟瀏覽器以完成 OAuth 流程                                                                                                                                             |
| `/keybindings`            | 開啟或建立您的快捷鍵配置檔案                                                                                                                                                                     |
| `/login`                  | 登入您的 Anthropic 帳戶                                                                                                                                                                  |
| `/logout`                 | 登出您的 Anthropic 帳戶                                                                                                                                                                  |
| `/mcp`                    | 管理 MCP server 連線和 OAuth 驗證                                                                                                                                                         |
| `/memory`                 | 編輯 `CLAUDE.md` 記憶檔案、啟用或停用 [auto-memory](/zh-TW/memory#auto-memory)，以及檢視自動記憶項目                                                                                                      |
| `/mobile`                 | 顯示 QR 碼以下載 Claude 行動應用程式。別名：`/ios`、`/android`                                                                                                                                      |
| `/model [model]`          | 選擇或變更 AI 模型。對於支援的模型，使用左/右箭頭[調整努力等級](/zh-TW/model-config#adjust-effort-level)。變更立即生效，無需等待目前回應完成                                                                                     |
| `/passes`                 | 與朋友分享免費一週的 Claude Code。僅在您的帳戶符合條件時可見                                                                                                                                               |
| `/permissions`            | 檢視或更新[權限](/zh-TW/permissions#manage-permissions)。別名：`/allowed-tools`                                                                                                               |
| `/plan`                   | 直接從提示進入 Plan Mode                                                                                                                                                                  |
| `/plugin`                 | 管理 Claude Code [plugins](/zh-TW/plugins)                                                                                                                                           |
| `/pr-comments [PR]`       | 從 GitHub pull request 擷取並顯示評論。自動偵測目前分支的 PR，或傳遞 PR URL 或編號。需要 `gh` CLI                                                                                                              |
| `/privacy-settings`       | 檢視和更新您的隱私設定。僅適用於 Pro 和 Max 計畫訂閱者                                                                                                                                                   |
| `/release-notes`          | 檢視完整變更日誌，最新版本最接近您的提示                                                                                                                                                               |
| `/reload-plugins`         | 重新載入所有作用中的 [plugins](/zh-TW/plugins) 以套用待處理變更，無需重新啟動。報告已載入的內容並記錄需要重新啟動的任何變更                                                                                                        |
| `/remote-control`         | 使此會話可從 claude.ai 進行[遠端控制](/zh-TW/remote-control)。別名：`/rc`                                                                                                                          |
| `/remote-env`             | 為 [teleport 會話](/zh-TW/claude-code-on-the-web#teleport-a-web-session-to-your-terminal)配置預設遠端環境                                                                                     |
| `/rename [name]`          | 重新命名目前會話。不使用名稱時，從對話歷史自動生成                                                                                                                                                          |
| `/resume [session]`       | 按 ID 或名稱繼續對話，或開啟會話選擇器。別名：`/continue`                                                                                                                                               |
| `/review`                 | 已棄用。改為安裝 [`code-review` plugin](https://github.com/anthropics/claude-code-marketplace/blob/main/code-review/README.md)：`claude plugin install code-review@claude-code-marketplace` |
| `/rewind`                 | 回溯對話和/或程式碼到先前的點，或從選定的訊息進行摘要。詳見 [checkpointing](/zh-TW/checkpointing)。別名：`/checkpoint`                                                                                              |
| `/sandbox`                | 切換 [sandbox mode](/zh-TW/sandboxing)。僅在支援的平台上可用                                                                                                                                    |
| `/security-review`        | 分析目前分支上的待處理變更以查找安全漏洞。檢查 git 差異並識別注入、驗證問題和資料洩露等風險                                                                                                                                   |
| `/skills`                 | 列出可用的 [skills](/zh-TW/skills)                                                                                                                                                      |
| `/stats`                  | 視覺化每日使用情況、會話歷史、連勝和模型偏好                                                                                                                                                             |
| `/status`                 | 開啟設定介面（狀態標籤），顯示版本、模型、帳戶和連線性                                                                                                                                                        |
| `/statusline`             | 配置 Claude Code 的[狀態行](/zh-TW/statusline)。描述您想要的內容，或不帶引數執行以從您的 shell 提示自動配置                                                                                                         |
| `/stickers`               | 訂購 Claude Code 貼紙                                                                                                                                                                  |
| `/tasks`                  | 列出並管理背景工作                                                                                                                                                                          |
| `/terminal-setup`         | 為 Shift+Enter 和其他快捷鍵配置終端快捷鍵。僅在需要它的終端中可見，例如 VS Code、Alacritty 或 Warp                                                                                                                |
| `/theme`                  | 變更色彩主題。包括淺色和深色變體、色盲無障礙（daltonized）主題和使用終端色彩調色板的 ANSI 主題                                                                                                                            |
| `/upgrade`                | 開啟升級頁面以切換到更高的計畫層級                                                                                                                                                                  |
| `/usage`                  | 顯示計畫使用限制和速率限制狀態                                                                                                                                                                    |
| `/vim`                    | 在 Vim 和正常編輯模式之間切換                                                                                                                                                                  |

### MCP prompts

MCP servers 可以公開顯示為命令的 prompts。這些使用格式 `/mcp__<server>__<prompt>`，並從連線的 servers 動態發現。詳見 [MCP prompts](/zh-TW/mcp#use-mcp-prompts-as-commands)。

## Vim 編輯器模式

使用 `/vim` 命令啟用 vim 風格編輯，或透過 `/config` 永久配置。

### 模式切換

| 命令    | 動作           | 來自模式   |
| :---- | :----------- | :----- |
| `Esc` | 進入 NORMAL 模式 | INSERT |
| `i`   | 在游標前插入       | NORMAL |
| `I`   | 在行首插入        | NORMAL |
| `a`   | 在游標後插入       | NORMAL |
| `A`   | 在行尾插入        | NORMAL |
| `o`   | 在下方開啟行       | NORMAL |
| `O`   | 在上方開啟行       | NORMAL |

### 導航（NORMAL 模式）

| 命令              | 動作                  |
| :-------------- | :------------------ |
| `h`/`j`/`k`/`l` | 向左/下/上/右移動          |
| `w`             | 下一個單字               |
| `e`             | 單字結尾                |
| `b`             | 上一個單字               |
| `0`             | 行首                  |
| `$`             | 行尾                  |
| `^`             | 第一個非空白字元            |
| `gg`            | 輸入開始                |
| `G`             | 輸入結尾                |
| `f{char}`       | 跳到下一個字元出現           |
| `F{char}`       | 跳到上一個字元出現           |
| `t{char}`       | 跳到下一個字元出現之前         |
| `T{char}`       | 跳到上一個字元出現之後         |
| `;`             | 重複最後一個 f/F/t/T 動作   |
| `,`             | 反向重複最後一個 f/F/t/T 動作 |

<Note>
  在 vim 正常模式中，如果游標在輸入的開始或結尾，無法進一步移動，箭頭鍵將導航命令歷史。
</Note>

### 編輯（NORMAL 模式）

| 命令             | 動作          |
| :------------- | :---------- |
| `x`            | 刪除字元        |
| `dd`           | 刪除行         |
| `D`            | 刪除到行尾       |
| `dw`/`de`/`db` | 刪除單字/到結尾/向後 |
| `cc`           | 變更行         |
| `C`            | 變更到行尾       |
| `cw`/`ce`/`cb` | 變更單字/到結尾/向後 |
| `yy`/`Y`       | 複製（yank）行   |
| `yw`/`ye`/`yb` | 複製單字/到結尾/向後 |
| `p`            | 在游標後貼上      |
| `P`            | 在游標前貼上      |
| `>>`           | 縮排行         |
| `<<`           | 取消縮排行       |
| `J`            | 合併行         |
| `.`            | 重複最後一個變更    |

### 文字物件（NORMAL 模式）

文字物件與運算子（如 `d`、`c` 和 `y`）搭配使用：

| 命令        | 動作               |
| :-------- | :--------------- |
| `iw`/`aw` | 內部/周圍單字          |
| `iW`/`aW` | 內部/周圍 WORD（空白分隔） |
| `i"`/`a"` | 內部/周圍雙引號         |
| `i'`/`a'` | 內部/周圍單引號         |
| `i(`/`a(` | 內部/周圍括號          |
| `i[`/`a[` | 內部/周圍方括號         |
| `i{`/`a{` | 內部/周圍大括號         |

## 命令歷史

Claude Code 維護目前會話的命令歷史：

* 輸入歷史按工作目錄儲存
* 當您執行 `/clear` 以啟動新會話時，輸入歷史會重設。先前會話的對話會保留，可以繼續。
* 使用上/下箭頭導航（請參閱上面的鍵盤快捷鍵）
* **注意**：歷史擴展（`!`）預設停用

### 使用 Ctrl+R 反向搜尋

按 `Ctrl+R` 以互動方式搜尋您的命令歷史：

1. **開始搜尋**：按 `Ctrl+R` 啟動反向歷史搜尋
2. **輸入查詢**：輸入文字以在先前的命令中搜尋。搜尋詞在匹配結果中醒目提示
3. **導航匹配**：再次按 `Ctrl+R` 以循環瀏覽較舊的匹配
4. **接受匹配**：
   * 按 `Tab` 或 `Esc` 以接受目前匹配並繼續編輯
   * 按 `Enter` 以接受並立即執行命令
5. **取消搜尋**：
   * 按 `Ctrl+C` 以取消並恢復您的原始輸入
   * 在空搜尋上按 `Backspace` 以取消

搜尋顯示匹配的命令，搜尋詞醒目提示，因此您可以找到並重複使用先前的輸入。

## 背景 bash 命令

Claude Code 支援在背景執行 bash 命令，允許您在長時間執行的程序執行時繼續工作。

### 背景執行的工作原理

當 Claude Code 在背景執行命令時，它以非同步方式執行命令並立即傳回背景工作 ID。Claude Code 可以在命令在背景繼續執行時回應新的提示。

若要在背景執行命令，您可以：

* 提示 Claude Code 在背景執行命令
* 按 Ctrl+B 將常規 Bash 工具呼叫移到背景。（Tmux 使用者必須按 Ctrl+B 兩次，因為 tmux 的前綴鍵。）

**主要功能：**

* 輸出被緩衝，Claude 可以使用 TaskOutput 工具擷取它
* 背景工作有唯一的 ID 用於追蹤和輸出擷取
* 當 Claude Code 退出時，背景工作會自動清理

若要停用所有背景工作功能，請將 `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` 環境變數設定為 `1`。詳見[環境變數](/zh-TW/settings#environment-variables)。

**常見的背景執行命令：**

* 建置工具（webpack、vite、make）
* 套件管理器（npm、yarn、pnpm）
* 測試執行器（jest、pytest）
* 開發伺服器
* 長時間執行的程序（docker、terraform）

### 使用 `!` 前綴的 Bash 模式

透過在輸入前加上 `!` 直接執行 bash 命令，無需透過 Claude：

```bash  theme={null}
! npm test
! git status
! ls -la
```

Bash 模式：

* 將命令及其輸出新增到對話上下文
* 顯示即時進度和輸出
* 支援相同的 `Ctrl+B` 背景執行以用於長時間執行的命令
* 不需要 Claude 解釋或批准命令
* 支援基於歷史的自動完成：輸入部分命令並按 **Tab** 以從目前專案中的先前 `!` 命令完成
* 在空提示上使用 `Escape`、`Backspace` 或 `Ctrl+U` 退出

這對於快速 shell 操作同時維護對話上下文很有用。

## 提示建議

當您首次開啟會話時，灰色的範例命令會出現在提示輸入中以幫助您開始。Claude Code 從您的專案的 git 歷史中選擇此項，因此它反映您最近一直在處理的檔案。

Claude 回應後，建議會根據您的對話歷史繼續出現，例如多部分請求的後續步驟或工作流程的自然延續。

* 按 **Tab** 以接受建議，或按 **Enter** 以接受並提交
* 開始輸入以關閉它

建議作為背景請求執行，重複使用父對話的 prompt cache，因此額外成本最少。當 cache 冷時，Claude Code 會跳過建議生成以避免不必要的成本。

建議在對話的第一個回合之後、在非互動模式中以及在 Plan Mode 中自動跳過。

若要完全停用提示建議，請設定環境變數或在 `/config` 中切換設定：

```bash  theme={null}
export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false
```

## 使用 /btw 的側面問題

使用 `/btw` 提出有關您目前工作的快速問題，無需新增到對話歷史。當您想要快速答案但不想雜亂主要上下文或使 Claude 偏離長時間執行的工作時，這很有用。

```
/btw what was the name of that config file again?
```

側面問題可以完全看到目前對話，因此您可以詢問 Claude 已經讀過的程式碼、它之前做出的決定或會話中的任何其他內容。問題和答案是短暫的：它們出現在可關閉的覆蓋層中，永遠不會進入對話歷史。

* **在 Claude 工作時可用**：即使 Claude 正在處理回應時，您也可以執行 `/btw`。側面問題獨立執行，不會中斷主要回合。
* **無工具存取**：側面問題僅從已在上下文中的內容回答。Claude 在回答側面問題時無法讀取檔案、執行命令或搜尋。
* **單一回應**：沒有後續回合。如果您需要來回往返，請改用正常提示。
* **低成本**：側面問題重複使用父對話的 prompt cache，因此額外成本最少。

按 **Space**、**Enter** 或 **Escape** 以關閉答案並返回提示。

`/btw` 是 [subagent](/zh-TW/sub-agents) 的反面：它看到您的完整對話但沒有工具，而 subagent 有完整工具但以空上下文開始。使用 `/btw` 詢問 Claude 已經從此會話中知道的內容；使用 subagent 去發現新的東西。

## 工作清單

在處理複雜的多步驟工作時，Claude 會建立工作清單以追蹤進度。工作會在終端的狀態區域中出現，指示器顯示待處理、進行中或完成的內容。

* 按 `Ctrl+T` 以切換工作清單檢視。顯示一次最多 10 個工作
* 若要查看所有工作或清除它們，直接詢問 Claude：「show me all tasks」或「clear all tasks」
* 工作在上下文壓縮中持續，幫助 Claude 在較大的專案上保持組織
* 若要在會話之間共享工作清單，請設定 `CLAUDE_CODE_TASK_LIST_ID` 以使用 `~/.claude/tasks/` 中的命名目錄：`CLAUDE_CODE_TASK_LIST_ID=my-project claude`
* 若要還原到先前的 TODO 清單，請設定 `CLAUDE_CODE_ENABLE_TASKS=false`。

## PR 審查狀態

在處理具有開啟 pull request 的分支時，Claude Code 在頁尾顯示可點擊的 PR 連結（例如「PR #446」）。連結有一個彩色底線，指示審查狀態：

* 綠色：已批准
* 黃色：待審查
* 紅色：要求變更
* 灰色：草稿
* 紫色：已合併

`Cmd+click`（Mac）或 `Ctrl+click`（Windows/Linux）連結以在瀏覽器中開啟 pull request。狀態每 60 秒自動更新。

<Note>
  PR 狀態需要安裝並驗證 `gh` CLI（`gh auth login`）。
</Note>

## 另請參閱

* [Skills](/zh-TW/skills) - 自訂提示和工作流程
* [Checkpointing](/zh-TW/checkpointing) - 回溯 Claude 的編輯並恢復先前的狀態
* [CLI 參考](/zh-TW/cli-reference) - 命令列旗標和選項
* [設定](/zh-TW/settings) - 配置選項
* [記憶管理](/zh-TW/memory) - 管理 CLAUDE.md 檔案
