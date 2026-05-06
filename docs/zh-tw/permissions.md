> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 設定權限

> 使用細粒度權限規則、模式和受管理原則來控制 Claude Code 可以存取和執行的操作。

Claude Code 支援細粒度權限，讓您可以精確指定代理允許執行和不允許執行的操作。權限設定可以簽入版本控制並分發給組織中的所有開發人員，也可以由個別開發人員自訂。

## 權限系統

Claude Code 使用分層權限系統來平衡功能和安全性：

| 工具類型    | 範例            | 需要批准 | "是，不要再問"行為    |
| :------ | :------------ | :--- | :------------ |
| 唯讀      | 檔案讀取、Grep     | 否    | 不適用           |
| Bash 命令 | Shell 執行      | 是    | 每個專案目錄和命令永久有效 |
| 檔案修改    | Edit/Write 檔案 | 是    | 直到工作階段結束      |

## 管理權限

您可以使用 `/permissions` 檢視和管理 Claude Code 的工具權限。此 UI 列出所有權限規則及其來源的 settings.json 檔案。

* **Allow** 規則讓 Claude Code 使用指定的工具，無需手動批准。
* **Ask** 規則在 Claude Code 嘗試使用指定工具時提示確認。
* **Deny** 規則防止 Claude Code 使用指定的工具。

規則按順序評估：**deny -> ask -> allow**。第一個符合的規則獲勝，因此 deny 規則始終優先。

## 權限模式

Claude Code 支援多種權限模式來控制工具的批准方式。請參閱 [Permission modes](/zh-TW/permission-modes) 以了解何時使用每一種。在您的 [settings files](/zh-TW/settings#settings-files) 中設定 `defaultMode`：

| 模式                  | 描述                                                                               |
| :------------------ | :------------------------------------------------------------------------------- |
| `default`           | 標準行為：在首次使用每個工具時提示權限                                                              |
| `acceptEdits`       | 自動接受工作目錄或 `additionalDirectories` 中路徑的檔案編輯和常見檔案系統命令（`mkdir`、`touch`、`mv`、`cp` 等） |
| `plan`              | Plan Mode：Claude 讀取檔案並執行唯讀 shell 命令以探索，但不編輯您的原始檔案                                |
| `auto`              | 自動批准工具呼叫，並進行背景安全檢查以驗證操作是否符合您的要求。目前為研究預覽版                                         |
| `dontAsk`           | 自動拒絕工具，除非透過 `/permissions` 或 `permissions.allow` 規則預先批准                          |
| `bypassPermissions` | 跳過所有權限提示。根目錄和主目錄移除（例如 `rm -rf /`）仍會作為斷路器提示                                       |

<Warning>
  `bypassPermissions` 模式會跳過所有權限提示，包括對 `.git`、`.claude`、`.vscode`、`.idea` 和 `.husky` 的寫入。針對檔案系統根目錄或主目錄的移除，例如 `rm -rf /` 和 `rm -rf ~`，仍會作為斷路器提示以防止模型錯誤。僅在隔離環境（如容器或虛擬機）中使用此模式，其中 Claude Code 無法造成損害。管理員可以透過在 [managed settings](#managed-settings) 中將 `permissions.disableBypassPermissionsMode` 設定為 `"disable"` 來防止此模式。
</Warning>

若要防止 `bypassPermissions` 或 `auto` 模式被使用，請在任何 [settings files](/zh-TW/settings#settings-files) 中將 `permissions.disableBypassPermissionsMode` 或 `permissions.disableAutoMode` 設定為 `"disable"`。這些在 [managed settings](#managed-settings) 中最有用，因為它們無法被覆蓋。

## 權限規則語法

權限規則遵循格式 `Tool` 或 `Tool(specifier)`。

### 符合工具的所有使用

若要符合工具的所有使用，請使用不帶括號的工具名稱：

| 規則         | 效果           |
| :--------- | :----------- |
| `Bash`     | 符合所有 Bash 命令 |
| `WebFetch` | 符合所有網頁擷取請求   |
| `Read`     | 符合所有檔案讀取     |

`Bash(*)` 等同於 `Bash` 並符合所有 Bash 命令。

### 使用指定符進行細粒度控制

在括號中新增指定符以符合特定工具使用：

| 規則                             | 效果                     |
| :----------------------------- | :--------------------- |
| `Bash(npm run build)`          | 符合確切命令 `npm run build` |
| `Read(./.env)`                 | 符合讀取目前目錄中的 `.env` 檔案   |
| `WebFetch(domain:example.com)` | 符合對 example.com 的擷取請求  |

### 萬用字元模式

Bash 規則支援使用 `*` 的 glob 模式。萬用字元可以出現在命令中的任何位置。此設定允許 npm 和 git commit 命令，同時阻止 git push：

```json theme={null}
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git commit *)",
      "Bash(git * main)",
      "Bash(* --version)",
      "Bash(* --help *)"
    ],
    "deny": [
      "Bash(git push *)"
    ]
  }
}
```

`*` 前的空格很重要：`Bash(ls *)` 符合 `ls -la` 但不符合 `lsof`，而 `Bash(ls*)` 兩者都符合。`:*` 後綴是寫入尾部萬用字元的等效方式，所以 `Bash(ls:*)` 符合與 `Bash(ls *)` 相同的命令。

當您為命令前綴選擇"是，不要再問"時，權限對話框會寫入空格分隔的形式。`:*` 形式僅在模式末尾被識別。在像 `Bash(git:* push)` 這樣的模式中，冒號被視為字面字元，不會符合 git 命令。

## 工具特定的權限規則

### Bash

Bash 權限規則支援使用 `*` 的萬用字元符合。萬用字元可以出現在命令中的任何位置，包括開頭、中間或結尾：

* `Bash(npm run build)` 符合確切的 Bash 命令 `npm run build`
* `Bash(npm run test *)` 符合以 `npm run test` 開頭的 Bash 命令
* `Bash(npm *)` 符合任何以 `npm ` 開頭的命令
* `Bash(* install)` 符合任何以 ` install` 結尾的命令
* `Bash(git * main)` 符合命令如 `git checkout main` 和 `git log --oneline main`

單一 `*` 符合任何字元序列，包括空格，所以一個萬用字元可以跨越多個引數。`Bash(git *)` 符合 `git log --oneline --all`，而 `Bash(git * main)` 符合 `git push origin main` 以及 `git merge main`。

當 `*` 出現在末尾且前面有空格時（如 `Bash(ls *)`），它會強制執行字邊界，要求前綴後面跟著空格或字串結尾。例如，`Bash(ls *)` 符合 `ls -la` 但不符合 `lsof`。相比之下，`Bash(ls*)` 沒有空格會同時符合 `ls -la` 和 `lsof`，因為沒有字邊界限制。

#### 複合命令

<Tip>
  Claude Code 知道 shell 運算子，所以前綴符合規則如 `Bash(safe-cmd *)` 不會給它執行命令 `safe-cmd && other-cmd` 的權限。已識別的命令分隔符是 `&&`、`||`、`;`、`|`、`|&`、`&` 和換行符。規則必須獨立符合每個子命令。
</Tip>

當您使用"是，不要再問"批准複合命令時，Claude Code 會為每個需要批准的子命令儲存一個單獨的規則，而不是為完整複合字串儲存單一規則。例如，批准 `git status && npm test` 會為 `npm test` 儲存一個規則，因此未來的 `npm test` 呼叫會被識別，無論 `&&` 前面是什麼。子命令如 `cd` 進入子目錄會為該路徑產生自己的 Read 規則。單一複合命令最多可能儲存 5 個規則。

#### 程序包裝器

在符合 Bash 規則之前，Claude Code 會移除一組固定的程序包裝器，所以像 `Bash(npm test *)` 這樣的規則也符合 `timeout 30 npm test`。已識別的包裝器是 `timeout`、`time`、`nice`、`nohup` 和 `stdbuf`。

裸 `xargs` 也會被移除，所以 `Bash(grep *)` 符合 `xargs grep pattern`。移除僅在 `xargs` 沒有旗標時適用：像 `xargs -n1 grep pattern` 這樣的呼叫被符合為 `xargs` 命令，所以為內部命令編寫的規則不涵蓋它。

此包裝器清單是內建的，不可設定。開發環境執行器如 `direnv exec`、`devbox run`、`mise exec`、`npx` 和 `docker exec` 不在清單中。因為這些工具將其引數作為命令執行，像 `Bash(devbox run *)` 這樣的規則符合 `run` 後面的任何內容，包括 `devbox run rm -rf .`。若要批准環境執行器內的工作，請編寫包含執行器和內部命令的特定規則，如 `Bash(devbox run npm test)`。為您想要允許的每個內部命令新增一個規則。

Exec 包裝器如 `watch`、`setsid`、`ionice` 和 `flock` 始終提示，無法透過像 `Bash(watch *)` 這樣的前綴規則自動批准。同樣適用於帶有 `-exec` 或 `-delete` 的 `find`：`Bash(find *)` 規則不涵蓋這些形式。若要批准特定呼叫，請為完整命令字串編寫精確符合規則。

#### 唯讀命令

Claude Code 將一組內建的 Bash 命令識別為唯讀，並在每種模式中無需權限提示即可執行它們。這些包括 `ls`、`cat`、`head`、`tail`、`grep`、`find`、`wc`、`diff`、`stat`、`du`、`cd` 和 `git` 的唯讀形式。該集合不可設定；若要要求其中一個命令的提示，請為其新增 `ask` 或 `deny` 規則。

對於每個旗標都是唯讀的命令，允許未引用的 glob 模式，所以 `ls *.ts` 和 `wc -l src/*.py` 無需提示即可執行。具有寫入能力或執行能力旗標的命令，如 `find`、`sort`、`sed` 和 `git`，在存在未引用的 glob 時仍會提示，因為 glob 可能會擴展為像 `-delete` 這樣的旗標。

`cd` 進入工作目錄或 [additional directory](#working-directories) 內的路徑也是唯讀的。像 `cd packages/api && ls` 這樣的複合命令在每個部分都符合時無需提示即可執行。在一個複合命令中結合 `cd` 和 `git` 始終提示，無論目標目錄如何。

<Warning>
  嘗試限制命令引數的 Bash 權限模式很脆弱。例如，`Bash(curl http://github.com/ *)` 旨在將 curl 限制為 GitHub URL，但不會符合以下變化：

  * URL 前的選項：`curl -X GET http://github.com/...`
  * 不同的協定：`curl https://github.com/...`
  * 重新導向：`curl -L http://bit.ly/xyz`（重新導向到 github）
  * 變數：`URL=http://github.com && curl $URL`
  * 額外空格：`curl  http://github.com`

  為了更可靠的 URL 篩選，請考慮：

  * **限制 Bash 網路工具**：使用 deny 規則阻止 `curl`、`wget` 和類似命令，然後使用 WebFetch 工具搭配 `WebFetch(domain:github.com)` 權限以允許的網域
  * **使用 PreToolUse hooks**：實作一個 hook 來驗證 Bash 命令中的 URL 並阻止不允許的網域
  * 透過 CLAUDE.md 指示 Claude Code 關於您允許的 curl 模式

  請注意，單獨使用 WebFetch 不會防止網路存取。如果允許 Bash，Claude 仍然可以使用 `curl`、`wget` 或其他工具來存取任何 URL。
</Warning>

### PowerShell

PowerShell 權限規則使用與 Bash 規則相同的形式。使用 `*` 的萬用字元在任何位置符合，`:*` 後綴等同於尾部 ` *`，而裸 `PowerShell` 或 `PowerShell(*)` 符合每個命令。此設定允許 `Get-ChildItem` 和 `git commit` 命令，同時阻止 `Remove-Item`：

```json theme={null}
{
  "permissions": {
    "allow": [
      "PowerShell(Get-ChildItem *)",
      "PowerShell(git commit *)"
    ],
    "deny": [
      "PowerShell(Remove-Item *)"
    ]
  }
}
```

常見別名在符合前會被正規化。為 cmdlet 名稱編寫的規則也符合其別名，所以 `PowerShell(Get-ChildItem *)` 符合 `gci`、`ls` 和 `dir`。符合不區分大小寫。

Claude Code 解析 PowerShell AST 並獨立檢查複合命令中的每個命令。管道運算子 `|`、陳述式分隔符 `;` 和在 PowerShell 7+ 上的鏈運算子 `&&` 和 `||` 將複合命令分割為子命令。規則必須符合每個子命令才能允許複合命令。

### Read 和 Edit

`Edit` 規則適用於所有編輯檔案的內建工具。Claude 會盡力嘗試將 `Read` 規則應用於所有讀取檔案的內建工具，如 Grep 和 Glob。

<Warning>
  Read 和 Edit deny 規則適用於 Claude 的內建檔案工具，不適用於 Bash 子程序。`Read(./.env)` deny 規則會阻止 Read 工具，但不會防止 Bash 中的 `cat .env`。為了進行作業系統級別的強制執行，以阻止所有程序存取路徑，請 [enable the sandbox](/zh-TW/sandboxing)。
</Warning>

Read 和 Edit 規則都遵循 [gitignore](https://git-scm.com/docs/gitignore) 規格，具有四種不同的模式類型：

| 模式                | 意義                 | 範例                               | 符合                             |
| ----------------- | ------------------ | -------------------------------- | ------------------------------ |
| `//path`          | 來自檔案系統根目錄的**絕對**路徑 | `Read(//Users/alice/secrets/**)` | `/Users/alice/secrets/**`      |
| `~/path`          | 來自**主目錄**的路徑       | `Read(~/Documents/*.pdf)`        | `/Users/alice/Documents/*.pdf` |
| `/path`           | **相對於專案根目錄**的路徑    | `Edit(/src/**/*.ts)`             | `<project root>/src/**/*.ts`   |
| `path` 或 `./path` | **相對於目前目錄**的路徑     | `Read(*.env)`                    | `<cwd>/*.env`                  |

<Warning>
  像 `/Users/alice/file` 這樣的模式不是絕對路徑。它相對於專案根目錄。使用 `//Users/alice/file` 表示絕對路徑。
</Warning>

在 Windows 上，路徑在符合前會被正規化為 POSIX 形式。`C:\Users\alice` 變成 `/c/Users/alice`，所以使用 `//c/**/.env` 來符合該磁碟上任何位置的 `.env` 檔案。若要符合所有磁碟，請使用 `//**/.env`。

範例：

* `Edit(/docs/**)`: 編輯 `<project>/docs/` 中的檔案（不是 `/docs/` 也不是 `<project>/.claude/docs/`）
* `Read(~/.zshrc)`: 讀取您主目錄的 `.zshrc`
* `Edit(//tmp/scratch.txt)`: 編輯絕對路徑 `/tmp/scratch.txt`
* `Read(src/**)`: 從 `<current-directory>/src/` 讀取

<Note>
  在 gitignore 模式中，`*` 符合單一目錄中的檔案，而 `**` 遞迴符合目錄。若要允許所有檔案存取，請使用不帶括號的工具名稱：`Read`、`Edit` 或 `Write`。
</Note>

當 Claude 存取符號連結時，權限規則檢查兩個路徑：符號連結本身和它解析到的檔案。Allow 和 deny 規則對該對的處理方式不同：allow 規則回退到提示您，而 deny 規則直接阻止。

* **Allow 規則**：僅在符號連結路徑及其目標都符合時適用。允許目錄內的符號連結指向外部仍會提示您。
* **Deny 規則**：在符號連結路徑或其目標符合時適用。指向被拒絕檔案的符號連結本身被拒絕。

例如，使用 `Read(./project/**)` 允許和 `Read(~/.ssh/**)` 拒絕，位於 `./project/key` 指向 `~/.ssh/id_rsa` 的符號連結被阻止：目標未通過 allow 規則且符合 deny 規則。

### WebFetch

* `WebFetch(domain:example.com)` 符合對 example.com 的擷取請求

### MCP

* `mcp__puppeteer` 符合由 `puppeteer` 伺服器提供的任何工具（在 Claude Code 中設定的名稱）
* `mcp__puppeteer__*` 萬用字元語法，也符合來自 `puppeteer` 伺服器的所有工具
* `mcp__puppeteer__puppeteer_navigate` 符合由 `puppeteer` 伺服器提供的 `puppeteer_navigate` 工具

### Agent（subagents）

使用 `Agent(AgentName)` 規則來控制 Claude 可以使用哪些 [subagents](/zh-TW/sub-agents)：

* `Agent(Explore)` 符合 Explore subagent
* `Agent(Plan)` 符合 Plan subagent
* `Agent(my-custom-agent)` 符合名為 `my-custom-agent` 的自訂 subagent

將這些規則新增到您設定中的 `deny` 陣列，或使用 `--disallowedTools` CLI 旗標來停用特定代理。若要停用 Explore 代理：

```json theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)"]
  }
}
```

## 使用 hooks 擴展權限

[Claude Code hooks](/zh-TW/hooks-guide) 提供了一種方式來註冊自訂 shell 命令，以在執行時執行權限評估。當 Claude Code 進行工具呼叫時，PreToolUse hooks 在權限提示之前執行。hook 輸出可以拒絕工具呼叫、強制提示或跳過提示以讓呼叫繼續進行。

Hook 決定不會繞過權限規則。Deny 和 ask 規則在 hook 返回 `"allow"` 或 `"ask"` 後仍會被評估，因此符合的 deny 規則仍會阻止呼叫，符合的 ask 規則即使在 hook 返回 `"allow"` 或 `"ask"` 時仍會提示。這保留了 [Manage permissions](#manage-permissions) 中描述的 deny 優先順序，包括在受管理設定中設定的 deny 規則。

阻止 hook 也優先於 allow 規則。以代碼 2 退出的 hook 會在評估權限規則之前停止工具呼叫，因此即使 allow 規則會允許呼叫，該阻止也會適用。若要執行所有 Bash 命令而無需提示，除了您想要阻止的少數幾個，請將 `"Bash"` 新增到您的 allow 清單，並註冊一個 PreToolUse hook 來拒絕那些特定命令。請參閱 [Block edits to protected files](/zh-TW/hooks-guide#block-edits-to-protected-files) 以取得您可以調整的 hook 指令碼。

## 工作目錄

根據預設，Claude 可以存取啟動它的目錄中的檔案。您可以擴展此存取：

* **在啟動期間**：使用 `--add-dir <path>` CLI 引數
* **在工作階段期間**：使用 `/add-dir` 命令
* **持久設定**：新增到 [settings files](/zh-TW/settings#settings-files) 中的 `additionalDirectories`

其他目錄中的檔案遵循與原始工作目錄相同的權限規則：它們變成可讀的而無需提示，檔案編輯權限遵循目前的權限模式。

### 其他目錄授予檔案存取權，而非設定

新增目錄會擴展 Claude 可以讀取和編輯檔案的位置。它不會使該目錄成為完整的設定根目錄：大多數 `.claude/` 設定不會從其他目錄發現，儘管有幾種類型作為例外被載入。

以下設定類型從 `--add-dir` 目錄載入：

| 設定                                                                 | 從 `--add-dir` 載入                                                                                 |
| :----------------------------------------------------------------- | :----------------------------------------------------------------------------------------------- |
| `.claude/skills/` 中的 [Skills](/zh-TW/skills)                       | 是，具有即時重新載入                                                                                       |
| `.claude/settings.json` 中的外掛設定                                     | 僅 `enabledPlugins` 和 `extraKnownMarketplaces`                                                    |
| [CLAUDE.md](/zh-TW/memory) 檔案、`.claude/rules/` 和 `CLAUDE.local.md` | 僅當設定 `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` 時。`CLAUDE.local.md` 另外需要 `local` 設定來源，預設啟用 |

其他所有內容，包括 subagents、命令、輸出樣式、hooks 和其他設定，僅從目前工作目錄及其父目錄、您在 `~/.claude/` 的使用者目錄和受管理設定發現。若要在專案間共享該設定，請使用以下方法之一：

* **使用者級別設定**：將檔案放在 `~/.claude/agents/`、`~/.claude/output-styles/` 或 `~/.claude/settings.json` 中，使其在每個專案中可用
* **外掛**：將設定打包並分發為 [plugin](/zh-TW/plugins)，供團隊安裝
* **從設定目錄啟動**：從包含您想要的 `.claude/` 設定的目錄執行 Claude Code

## 權限如何與沙箱互動

權限和 [sandboxing](/zh-TW/sandboxing) 是互補的安全層：

* **權限**控制 Claude Code 可以使用哪些工具以及它可以存取哪些檔案或網域。它們適用於所有工具（Bash、Read、Edit、WebFetch、MCP 和其他）。
* **沙箱**提供作業系統級別的強制執行，限制 Bash 工具的檔案系統和網路存取。它僅適用於 Bash 命令及其子程序。

使用兩者進行深度防禦：

* 權限 deny 規則阻止 Claude 甚至嘗試存取受限資源
* 沙箱限制防止 Bash 命令到達定義邊界外的資源，即使提示注入繞過 Claude 的決策制定
* 沙箱中的檔案系統限制結合 [`sandbox.filesystem`](/zh-TW/sandboxing) 設定與 Read 和 Edit deny 規則；兩者都合併到最終沙箱邊界中
* 網路限制結合 WebFetch 權限規則與沙箱的 `allowedDomains` 和 `deniedDomains` 清單

當沙箱啟用 `autoAllowBashIfSandboxed: true`（預設值）時，沙箱化 Bash 命令無需提示即可執行，即使您的權限包括 `ask: Bash(*)`。沙箱邊界替代每個命令提示。明確的 deny 規則仍然適用，以及針對 `/`、您的主目錄或其他關鍵系統路徑的 `rm` 或 `rmdir` 命令仍然會觸發提示。請參閱 [sandbox modes](/zh-TW/sandboxing#sandbox-modes) 以變更此行為。

## 受管理設定

對於需要集中控制 Claude Code 設定的組織，管理員可以部署無法被使用者或專案設定覆蓋的受管理設定。這些原則設定遵循與一般設定檔案相同的格式，可以透過 MDM/OS 級別原則、受管理設定檔案或 [server-managed settings](/zh-TW/server-managed-settings) 傳遞。請參閱 [settings files](/zh-TW/settings#settings-files) 以了解傳遞機制和檔案位置。

### 僅受管理的設定

以下設定僅在受管理設定中有效。將它們放在使用者或專案設定檔案中沒有效果。

| 設定                                             | 描述                                                                                                                                                                                        |
| :--------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowedChannelPlugins`                        | 可能推送訊息的頻道外掛的允許清單。設定時替換預設 Anthropic 允許清單。需要 `channelsEnabled: true`。請參閱 [Restrict which channel plugins can run](/zh-TW/channels#restrict-which-channel-plugins-can-run)                   |
| `allowManagedHooksOnly`                        | 當為 `true` 時，僅載入受管理 hooks、SDK hooks 和在受管理設定 `enabledPlugins` 中強制啟用的外掛中的 hooks。使用者、專案和所有其他外掛 hooks 被阻止                                                                                      |
| `allowManagedMcpServersOnly`                   | 當為 `true` 時，僅尊重受管理設定中的 `allowedMcpServers`。`deniedMcpServers` 仍然從所有來源合併。請參閱 [Managed MCP configuration](/zh-TW/mcp#managed-mcp-configuration)                                             |
| `allowManagedPermissionRulesOnly`              | 當為 `true` 時，防止使用者和專案設定定義 `allow`、`ask` 或 `deny` 權限規則。僅套用受管理設定中的規則                                                                                                                         |
| `blockedMarketplaces`                          | 市場來源的封鎖清單。在下載前檢查被封鎖的來源，因此它們永遠不會接觸檔案系統。請參閱 [managed marketplace restrictions](/zh-TW/plugin-marketplaces#managed-marketplace-restrictions)                                                 |
| `channelsEnabled`                              | 允許組織使用 [channels](/zh-TW/channels)。請參閱 [enterprise controls](/zh-TW/channels#enterprise-controls) 以了解每個方案的預設值                                                                             |
| `forceRemoteSettingsRefresh`                   | 當為 `true` 時，阻止 CLI 啟動直到遠端受管理設定被新鮮擷取，如果擷取失敗則退出。請參閱 [fail-closed enforcement](/zh-TW/server-managed-settings#enforce-fail-closed-startup)                                                   |
| `pluginTrustMessage`                           | 自訂訊息，附加到安裝前顯示的外掛信任警告                                                                                                                                                                      |
| `sandbox.filesystem.allowManagedReadPathsOnly` | 當為 `true` 時，僅尊重受管理設定中的 `filesystem.allowRead` 路徑。`denyRead` 仍然從所有來源合併                                                                                                                     |
| `sandbox.network.allowManagedDomainsOnly`      | 當為 `true` 時，僅尊重來自受管理設定的 `allowedDomains` 和 `WebFetch(domain:...)` allow 規則。非允許的網域會自動被阻止，無需提示使用者。被拒絕的網域仍然從所有來源合併                                                                           |
| `strictKnownMarketplaces`                      | 控制使用者可以新增和安裝外掛的外掛市場來源。請參閱 [managed marketplace restrictions](/zh-TW/plugin-marketplaces#managed-marketplace-restrictions)                                                                 |
| `wslInheritsWindowsSettings`                   | 當在 Windows HKLM 登錄機碼或 `C:\Program Files\ClaudeCode\managed-settings.json` 中為 `true` 時，WSL 從 Windows 原則鏈以及 `/etc/claude-code` 讀取受管理設定。請參閱 [Settings files](/zh-TW/settings#settings-files) |

`disableBypassPermissionsMode` 通常放在受管理設定中以強制執行組織原則，但它可以從任何範圍工作。使用者可以在自己的設定中設定它以鎖定自己的繞過模式。

<Note>
  在 Team 和 Enterprise 方案上，管理員在 [Claude Code admin settings](https://claude.ai/admin-settings/claude-code) 中啟用或停用 [Remote Control](/zh-TW/remote-control) 和 [web sessions](/zh-TW/claude-code-on-the-web)。Remote Control 可以另外透過 [`disableRemoteControl`](/zh-TW/settings#available-settings) 受管理設定按裝置停用。Web sessions 沒有按裝置受管理設定金鑰。
</Note>

## 設定優先順序

權限規則遵循與所有其他 Claude Code 設定相同的 [settings precedence](/zh-TW/settings#settings-precedence)：

1. **受管理設定**：無法被任何其他級別覆蓋，包括命令列引數
2. **命令列引數**：臨時工作階段覆蓋
3. **本機專案設定** (`.claude/settings.local.json`)
4. **共用專案設定** (`.claude/settings.json`)
5. **使用者設定** (`~/.claude/settings.json`)

如果工具在任何級別被拒絕，沒有其他級別可以允許它。例如，受管理設定 deny 無法被 `--allowedTools` 覆蓋，`--disallowedTools` 可以新增超出受管理設定定義的限制。

如果權限在使用者設定中被允許但在專案設定中被拒絕，專案設定優先，權限被阻止。

## 範例設定

此 [repository](https://github.com/anthropics/claude-code/tree/main/examples/settings) 包含常見部署情境的入門設定設定。使用這些作為起點並根據您的需求進行調整。

## 另請參閱

* [Settings](/zh-TW/settings)：完整設定參考，包括權限設定表
* [Configure auto mode](/zh-TW/auto-mode-config)：告訴 auto mode 分類器您的組織信任哪些基礎設施
* [Sandboxing](/zh-TW/sandboxing)：Bash 命令的作業系統級別檔案系統和網路隔離
* [Authentication](/zh-TW/authentication)：設定使用者對 Claude Code 的存取
* [Security](/zh-TW/security)：安全防護措施和最佳實踐
* [Hooks](/zh-TW/hooks-guide)：自動化工作流程並擴展權限評估
