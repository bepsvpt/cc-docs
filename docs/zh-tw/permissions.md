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
| 檔案修改    | Edit/write 檔案 | 是    | 直到工作階段結束      |

## 管理權限

您可以使用 `/permissions` 檢視和管理 Claude Code 的工具權限。此 UI 列出所有權限規則及其來源的 settings.json 檔案。

* **Allow** 規則讓 Claude Code 使用指定的工具，無需手動批准。
* **Ask** 規則在 Claude Code 嘗試使用指定工具時提示確認。
* **Deny** 規則防止 Claude Code 使用指定的工具。

規則按順序評估：**deny -> ask -> allow**。第一個符合的規則獲勝，因此 deny 規則始終優先。

## 權限模式

Claude Code 支援多種權限模式來控制工具的批准方式。在您的[設定檔案](/zh-TW/settings#settings-files)中設定 `defaultMode`：

| 模式                  | 描述                                                      |
| :------------------ | :------------------------------------------------------ |
| `default`           | 標準行為：在首次使用每個工具時提示權限                                     |
| `acceptEdits`       | 自動接受工作階段的檔案編輯權限                                         |
| `plan`              | Plan Mode：Claude 可以分析但不能修改檔案或執行命令                       |
| `dontAsk`           | 自動拒絕工具，除非透過 `/permissions` 或 `permissions.allow` 規則預先批准 |
| `bypassPermissions` | 跳過所有權限提示（需要安全環境，請參閱下方警告）                                |

<Warning>
  `bypassPermissions` 模式會停用所有權限檢查。僅在隔離環境（如容器或虛擬機）中使用此模式，其中 Claude Code 無法造成損害。管理員可以透過在[受管理設定](#managed-settings)中將 `disableBypassPermissionsMode` 設定為 `"disable"` 來防止此模式。
</Warning>

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

```json  theme={null}
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

`*` 前的空格很重要：`Bash(ls *)` 符合 `ls -la` 但不符合 `lsof`，而 `Bash(ls*)` 兩者都符合。舊版 `:*` 後綴語法等同於 ` *` 但已棄用。

## 工具特定的權限規則

### Bash

Bash 權限規則支援使用 `*` 的萬用字元符合。萬用字元可以出現在命令中的任何位置，包括開頭、中間或結尾：

* `Bash(npm run build)` 符合確切的 Bash 命令 `npm run build`
* `Bash(npm run test *)` 符合以 `npm run test` 開頭的 Bash 命令
* `Bash(npm *)` 符合任何以 `npm ` 開頭的命令
* `Bash(* install)` 符合任何以 ` install` 結尾的命令
* `Bash(git * main)` 符合命令如 `git checkout main`、`git merge main`

當 `*` 出現在末尾且前面有空格時（如 `Bash(ls *)`），它會強制執行字邊界，要求前綴後面跟著空格或字串結尾。例如，`Bash(ls *)` 符合 `ls -la` 但不符合 `lsof`。相比之下，`Bash(ls*)` 沒有空格會同時符合 `ls -la` 和 `lsof`，因為沒有字邊界限制。

<Tip>
  Claude Code 知道 shell 運算子（如 `&&`），所以前綴符合規則如 `Bash(safe-cmd *)` 不會給它執行命令 `safe-cmd && other-cmd` 的權限。
</Tip>

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

### Read 和 Edit

`Edit` 規則適用於所有編輯檔案的內建工具。Claude 會盡力嘗試將 `Read` 規則應用於所有讀取檔案的內建工具，如 Grep 和 Glob。

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

範例：

* `Edit(/docs/**)`: 編輯 `<project>/docs/` 中的檔案（不是 `/docs/` 也不是 `<project>/.claude/docs/`）
* `Read(~/.zshrc)`: 讀取您主目錄的 `.zshrc`
* `Edit(//tmp/scratch.txt)`: 編輯絕對路徑 `/tmp/scratch.txt`
* `Read(src/**)`: 從 `<current-directory>/src/` 讀取

<Note>
  在 gitignore 模式中，`*` 符合單一目錄中的檔案，而 `**` 遞迴符合目錄。若要允許所有檔案存取，請使用不帶括號的工具名稱：`Read`、`Edit` 或 `Write`。
</Note>

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

```json  theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)"]
  }
}
```

## 使用 hooks 擴展權限

[Claude Code hooks](/zh-TW/hooks-guide) 提供了一種方式來註冊自訂 shell 命令，以在執行時執行權限評估。當 Claude Code 進行工具呼叫時，PreToolUse hooks 在權限系統之前執行，hook 輸出可以決定是否批准或拒絕工具呼叫，以取代權限系統。

## 工作目錄

根據預設，Claude 可以存取啟動它的目錄中的檔案。您可以擴展此存取：

* **在啟動期間**：使用 `--add-dir <path>` CLI 引數
* **在工作階段期間**：使用 `/add-dir` 命令
* **持久設定**：新增到[設定檔案](/zh-TW/settings#settings-files)中的 `additionalDirectories`

其他目錄中的檔案遵循與原始工作目錄相同的權限規則：它們變成可讀的而無需提示，檔案編輯權限遵循目前的權限模式。

## 權限如何與沙箱互動

權限和[沙箱](/zh-TW/sandboxing)是互補的安全層：

* **權限**控制 Claude Code 可以使用哪些工具以及它可以存取哪些檔案或網域。它們適用於所有工具（Bash、Read、Edit、WebFetch、MCP 和其他）。
* **沙箱**提供作業系統級別的強制執行，限制 Bash 工具的檔案系統和網路存取。它僅適用於 Bash 命令及其子程序。

使用兩者進行深度防禦：

* 權限 deny 規則阻止 Claude 甚至嘗試存取受限資源
* 沙箱限制防止 Bash 命令到達定義邊界外的資源，即使提示注入繞過 Claude 的決策制定
* 沙箱中的檔案系統限制使用 Read 和 Edit deny 規則，而不是單獨的沙箱設定
* 網路限制結合 WebFetch 權限規則與沙箱的 `allowedDomains` 清單

## 受管理設定

對於需要集中控制 Claude Code 設定的組織，管理員可以部署無法被使用者或專案設定覆蓋的受管理設定。這些原則設定遵循與一般設定檔案相同的格式，可以透過 MDM/OS 級別原則、受管理設定檔案或[伺服器管理的設定](/zh-TW/server-managed-settings)傳遞。請參閱[設定檔案](/zh-TW/settings#settings-files)以了解傳遞機制和檔案位置。

### 僅受管理的設定

某些設定僅在受管理設定中有效：

| 設定                                        | 描述                                                                                                                            |
| :---------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| `disableBypassPermissionsMode`            | 設定為 `"disable"` 以防止 `bypassPermissions` 模式和 `--dangerously-skip-permissions` 旗標                                               |
| `allowManagedPermissionRulesOnly`         | 當為 `true` 時，防止使用者和專案設定定義 `allow`、`ask` 或 `deny` 權限規則。僅套用受管理設定中的規則                                                             |
| `allowManagedHooksOnly`                   | 當為 `true` 時，防止載入使用者、專案和外掛 hooks。僅允許受管理 hooks 和 SDK hooks                                                                      |
| `allowManagedMcpServersOnly`              | 當為 `true` 時，僅尊重受管理設定中的 `allowedMcpServers`。`deniedMcpServers` 仍然從所有來源合併。請參閱[受管理 MCP 設定](/zh-TW/mcp#managed-mcp-configuration) |
| `blockedMarketplaces`                     | 市場來源的封鎖清單。在下載前檢查被封鎖的來源，因此它們永遠不會接觸檔案系統。請參閱[受管理市場限制](/zh-TW/plugin-marketplaces#managed-marketplace-restrictions)               |
| `sandbox.network.allowManagedDomainsOnly` | 當為 `true` 時，僅尊重來自受管理設定的 `allowedDomains` 和 `WebFetch(domain:...)` allow 規則。非允許的網域會自動被阻止，無需提示使用者。被拒絕的網域仍然從所有來源合併               |
| `strictKnownMarketplaces`                 | 控制使用者可以新增哪些外掛市場。請參閱[受管理市場限制](/zh-TW/plugin-marketplaces#managed-marketplace-restrictions)                                     |
| `allow_remote_sessions`                   | 當為 `true` 時，允許使用者啟動[遠端控制](/zh-TW/remote-control)和[網頁工作階段](/zh-TW/claude-code-on-the-web)。預設為 `true`。設定為 `false` 以防止遠端工作階段存取   |

## 設定優先順序

權限規則遵循與所有其他 Claude Code 設定相同的[設定優先順序](/zh-TW/settings#settings-precedence)：

1. **受管理設定**：無法被任何其他級別覆蓋，包括命令列引數
2. **命令列引數**：臨時工作階段覆蓋
3. **本機專案設定** (`.claude/settings.local.json`)
4. **共用專案設定** (`.claude/settings.json`)
5. **使用者設定** (`~/.claude/settings.json`)

如果工具在任何級別被拒絕，沒有其他級別可以允許它。例如，受管理設定 deny 無法被 `--allowedTools` 覆蓋，`--disallowedTools` 可以新增超出受管理設定定義的限制。

如果權限在使用者設定中被允許但在專案設定中被拒絕，專案設定優先，權限被阻止。

## 範例設定

此[儲存庫](https://github.com/anthropics/claude-code/tree/main/examples/settings)包含常見部署情境的入門設定設定。使用這些作為起點並根據您的需求進行調整。

## 另請參閱

* [Settings](/zh-TW/settings)：完整設定參考，包括權限設定表
* [Sandboxing](/zh-TW/sandboxing)：Bash 命令的作業系統級別檔案系統和網路隔離
* [Authentication](/zh-TW/authentication)：設定使用者對 Claude Code 的存取
* [Security](/zh-TW/security)：安全防護措施和最佳實踐
* [Hooks](/zh-TW/hooks-guide)：自動化工作流程並擴展權限評估
