> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 透過市場探索和安裝預建外掛程式

> 從市場探索和安裝外掛程式，以使用新命令、代理和功能擴展 Claude Code。

外掛程式透過技能、代理、hooks 和 MCP servers 擴展 Claude Code。外掛程式市場是幫助您探索和安裝這些擴展的目錄，無需自己構建它們。

想要建立和分發您自己的市場？請參閱[建立和分發外掛程式市場](/zh-TW/plugin-marketplaces)。

## 市場如何運作

市場是他人建立和共享的外掛程式目錄。使用市場是一個兩步流程：

<Steps>
  <Step title="新增市場">
    這會向 Claude Code 註冊目錄，以便您可以瀏覽可用內容。尚未安裝任何外掛程式。
  </Step>

  <Step title="安裝個別外掛程式">
    瀏覽目錄並安裝您想要的外掛程式。
  </Step>
</Steps>

將其視為新增應用程式商店：新增商店可讓您存取瀏覽其集合，但您仍然可以選擇個別下載哪些應用程式。

## 官方 Anthropic 市場

官方 Anthropic 市場 (`claude-plugins-official`) 在您啟動 Claude Code 時自動可用。執行 `/plugin` 並前往 **Discover** 標籤以瀏覽可用內容。

若要從官方市場安裝外掛程式：

```shell  theme={null}
/plugin install plugin-name@claude-plugins-official
```

<Note>
  官方市場由 Anthropic 維護。若要將外掛程式提交到官方市場，請使用其中一個應用內提交表單：

  * **Claude.ai**: [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
  * **Console**: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

  若要獨立分發外掛程式，請[建立您自己的市場](/zh-TW/plugin-marketplaces)並與使用者共享。
</Note>

官方市場包括多個外掛程式類別：

### 程式碼智能

程式碼智能外掛程式啟用 Claude Code 的內建 LSP 工具，使 Claude 能夠跳轉到定義、尋找參考資料，並在編輯後立即查看類型錯誤。這些外掛程式配置[語言伺服器協議](https://microsoft.github.io/language-server-protocol/)連接，這是為 VS Code 程式碼智能提供動力的相同技術。

這些外掛程式需要在您的系統上安裝語言伺服器二進位檔。如果您已經安裝了語言伺服器，當您開啟專案時，Claude 可能會提示您安裝相應的外掛程式。

| 語言         | 外掛程式                | 所需的二進位檔                      |
| :--------- | :------------------ | :--------------------------- |
| C/C++      | `clangd-lsp`        | `clangd`                     |
| C#         | `csharp-lsp`        | `csharp-ls`                  |
| Go         | `gopls-lsp`         | `gopls`                      |
| Java       | `jdtls-lsp`         | `jdtls`                      |
| Kotlin     | `kotlin-lsp`        | `kotlin-language-server`     |
| Lua        | `lua-lsp`           | `lua-language-server`        |
| PHP        | `php-lsp`           | `intelephense`               |
| Python     | `pyright-lsp`       | `pyright-langserver`         |
| Rust       | `rust-analyzer-lsp` | `rust-analyzer`              |
| Swift      | `swift-lsp`         | `sourcekit-lsp`              |
| TypeScript | `typescript-lsp`    | `typescript-language-server` |

您也可以[為其他語言建立您自己的 LSP 外掛程式](/zh-TW/plugins-reference#lsp-servers)。

<Note>
  如果在安裝外掛程式後在 `/plugin` Errors 標籤中看到 `Executable not found in $PATH`，請從上表安裝所需的二進位檔。
</Note>

#### Claude 從程式碼智能外掛程式獲得的功能

安裝程式碼智能外掛程式並且其語言伺服器二進位檔可用後，Claude 獲得兩項功能：

* **自動診斷**：在 Claude 進行每次檔案編輯後，語言伺服器分析變更並自動報告錯誤和警告。Claude 看到類型錯誤、遺漏的匯入和語法問題，無需執行編譯器或 linter。如果 Claude 引入錯誤，它會注意到並在同一輪中修復問題。這不需要超出安裝外掛程式的任何配置。當「找到診斷」指示器出現時，您可以按 **Ctrl+O** 來內聯查看診斷。
* **程式碼導航**：Claude 可以使用語言伺服器跳轉到定義、尋找參考資料、懸停時取得類型資訊、列出符號、尋找實現和追蹤呼叫層次結構。這些操作為 Claude 提供比基於 grep 的搜尋更精確的導航，儘管可用性可能因語言和環境而異。

如果您遇到問題，請參閱[程式碼智能故障排除](#code-intelligence-issues)。

### 外部整合

這些外掛程式捆綁預先配置的 [MCP servers](/zh-TW/mcp)，以便您可以連接 Claude 到外部服務，無需手動設定：

* **原始碼控制**：`github`、`gitlab`
* **專案管理**：`atlassian`（Jira/Confluence）、`asana`、`linear`、`notion`
* **設計**：`figma`
* **基礎設施**：`vercel`、`firebase`、`supabase`
* **通訊**：`slack`
* **監控**：`sentry`

### 開發工作流程

為常見開發任務新增命令和代理的外掛程式：

* **commit-commands**：Git 提交工作流程，包括提交、推送和 PR 建立
* **pr-review-toolkit**：用於審查拉取請求的專門代理
* **agent-sdk-dev**：使用 Claude Agent SDK 構建的工具
* **plugin-dev**：建立您自己的外掛程式的工具組

### 輸出樣式

自訂 Claude 的回應方式：

* **explanatory-output-style**：關於實現選擇的教育見解
* **learning-output-style**：用於技能建立的互動式學習模式

## 試試看：新增演示市場

Anthropic 也維護一個[演示外掛程式市場](https://github.com/anthropics/claude-code/tree/main/plugins)（`claude-code-plugins`），其中包含展示外掛程式系統可能性的範例外掛程式。與官方市場不同，您需要手動新增此市場。

<Steps>
  <Step title="新增市場">
    在 Claude Code 中，為 `anthropics/claude-code` 市場執行 `plugin marketplace add` 命令：

    ```shell  theme={null}
    /plugin marketplace add anthropics/claude-code
    ```

    這會下載市場目錄並使其外掛程式可供您使用。
  </Step>

  <Step title="瀏覽可用外掛程式">
    執行 `/plugin` 以開啟外掛程式管理器。這會開啟一個標籤式介面，其中有四個標籤，您可以使用 **Tab** 鍵（或 **Shift+Tab** 向後）循環瀏覽：

    * **Discover**：從所有市場瀏覽可用外掛程式
    * **Installed**：檢視和管理已安裝的外掛程式
    * **Marketplaces**：新增、移除或更新已新增的市場
    * **Errors**：檢視任何外掛程式載入錯誤

    前往 **Discover** 標籤以查看您剛新增的市場中的外掛程式。
  </Step>

  <Step title="安裝外掛程式">
    選擇外掛程式以檢視其詳細資訊，然後選擇安裝範圍：

    * **User scope**：在所有專案中為自己安裝
    * **Project scope**：為此儲存庫上的所有協作者安裝
    * **Local scope**：僅在此儲存庫中為自己安裝

    例如，選擇 **commit-commands**（新增 git 工作流程命令的外掛程式）並將其安裝到您的使用者範圍。

    您也可以直接從命令列安裝：

    ```shell  theme={null}
    /plugin install commit-commands@anthropics-claude-code
    ```

    請參閱[配置範圍](/zh-TW/settings#configuration-scopes)以深入瞭解範圍。
  </Step>

  <Step title="使用您的新外掛程式">
    安裝後，執行 `/reload-plugins` 以啟動外掛程式。外掛程式命令由外掛程式名稱命名空間，因此 **commit-commands** 提供 `/commit-commands:commit` 之類的命令。

    透過對檔案進行變更並執行以下命令來試試看：

    ```shell  theme={null}
    /commit-commands:commit
    ```

    這會暫存您的變更、產生提交訊息並建立提交。

    每個外掛程式的工作方式不同。檢查 **Discover** 標籤中的外掛程式描述或其首頁，以瞭解它提供的命令和功能。
  </Step>
</Steps>

本指南的其餘部分涵蓋了您可以新增市場、安裝外掛程式和管理配置的所有方式。

## 新增市場

使用 `/plugin marketplace add` 命令從不同來源新增市場。

<Tip>
  **快捷方式**：您可以使用 `/plugin market` 代替 `/plugin marketplace`，以及 `rm` 代替 `remove`。
</Tip>

* **GitHub 儲存庫**：`owner/repo` 格式（例如，`anthropics/claude-code`）
* **Git URL**：任何 git 儲存庫 URL（GitLab、Bitbucket、自託管）
* **本機路徑**：目錄或 `marketplace.json` 檔案的直接路徑
* **遠端 URL**：託管 `marketplace.json` 檔案的直接 URL

### 從 GitHub 新增

使用 `owner/repo` 格式新增包含 `.claude-plugin/marketplace.json` 檔案的 GitHub 儲存庫，其中 `owner` 是 GitHub 使用者名稱或組織，`repo` 是儲存庫名稱。

例如，`anthropics/claude-code` 指的是由 `anthropics` 擁有的 `claude-code` 儲存庫：

```shell  theme={null}
/plugin marketplace add anthropics/claude-code
```

### 從其他 Git 主機新增

透過提供完整 URL 新增任何 git 儲存庫。這適用於任何 Git 主機，包括 GitLab、Bitbucket 和自託管伺服器：

使用 HTTPS：

```shell  theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git
```

使用 SSH：

```shell  theme={null}
/plugin marketplace add git@gitlab.com:company/plugins.git
```

若要新增特定分支或標籤，請在 `#` 後面附加 ref：

```shell  theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git#v1.0.0
```

### 從本機路徑新增

新增包含 `.claude-plugin/marketplace.json` 檔案的本機目錄：

```shell  theme={null}
/plugin marketplace add ./my-marketplace
```

您也可以新增 `marketplace.json` 檔案的直接路徑：

```shell  theme={null}
/plugin marketplace add ./path/to/marketplace.json
```

### 從遠端 URL 新增

透過 URL 新增遠端 `marketplace.json` 檔案：

```shell  theme={null}
/plugin marketplace add https://example.com/marketplace.json
```

<Note>
  與基於 Git 的市場相比，基於 URL 的市場有一些限制。如果在安裝外掛程式時遇到「找不到路徑」錯誤，請參閱[故障排除](/zh-TW/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces)。
</Note>

## 安裝外掛程式

新增市場後，您可以直接安裝外掛程式（預設安裝到使用者範圍）：

```shell  theme={null}
/plugin install plugin-name@marketplace-name
```

若要選擇不同的[安裝範圍](/zh-TW/settings#configuration-scopes)，請使用互動式 UI：執行 `/plugin`，前往 **Discover** 標籤，然後在外掛程式上按 **Enter**。您將看到以下選項：

* **User scope**（預設）：在所有專案中為自己安裝
* **Project scope**：為此儲存庫上的所有協作者安裝（新增到 `.claude/settings.json`）
* **Local scope**：僅在此儲存庫中為自己安裝（不與協作者共享）

您也可能看到具有 **managed** 範圍的外掛程式，這些是由管理員透過[受管設定](/zh-TW/settings#settings-files)安裝的，無法修改。

執行 `/plugin` 並前往 **Installed** 標籤以查看按範圍分組的外掛程式。

<Warning>
  在安裝外掛程式之前，請確保您信任它。Anthropic 不控制外掛程式中包含的 MCP servers、檔案或其他軟體，也無法驗證它們是否按預期工作。檢查每個外掛程式的首頁以獲取更多資訊。
</Warning>

## 管理已安裝的外掛程式

執行 `/plugin` 並前往 **Installed** 標籤以檢視、啟用、停用或解除安裝外掛程式。輸入以按外掛程式名稱或描述篩選清單。

您也可以使用直接命令管理外掛程式。

停用外掛程式而不解除安裝：

```shell  theme={null}
/plugin disable plugin-name@marketplace-name
```

重新啟用已停用的外掛程式：

```shell  theme={null}
/plugin enable plugin-name@marketplace-name
```

完全移除外掛程式：

```shell  theme={null}
/plugin uninstall plugin-name@marketplace-name
```

`--scope` 選項可讓您使用 CLI 命令針對特定範圍：

```shell  theme={null}
claude plugin install formatter@your-org --scope project
claude plugin uninstall formatter@your-org --scope project
```

### 在不重新啟動的情況下套用外掛程式變更

當您在工作階段期間安裝、啟用或停用外掛程式時，執行 `/reload-plugins` 以在不重新啟動的情況下啟動所有變更：

```shell  theme={null}
/reload-plugins
```

Claude Code 重新載入所有活動外掛程式，並顯示已重新載入的命令、技能、代理、hooks、外掛程式 MCP servers 和外掛程式 LSP servers 的計數。

## 管理市場

您可以透過互動式 `/plugin` 介面或使用 CLI 命令管理市場。

### 使用互動式介面

執行 `/plugin` 並前往 **Marketplaces** 標籤以：

* 檢視所有已新增的市場及其來源和狀態
* 新增新市場
* 更新市場清單以取得最新外掛程式
* 移除您不再需要的市場

### 使用 CLI 命令

您也可以使用直接命令管理市場。

列出所有已配置的市場：

```shell  theme={null}
/plugin marketplace list
```

從市場重新整理外掛程式清單：

```shell  theme={null}
/plugin marketplace update marketplace-name
```

移除市場：

```shell  theme={null}
/plugin marketplace remove marketplace-name
```

<Warning>
  移除市場將解除安裝您從中安裝的任何外掛程式。
</Warning>

### 配置自動更新

Claude Code 可以在啟動時自動更新市場及其已安裝的外掛程式。為市場啟用自動更新後，Claude Code 會重新整理市場資料並將已安裝的外掛程式更新到其最新版本。如果任何外掛程式已更新，您將看到提示您執行 `/reload-plugins` 的通知。

透過 UI 為個別市場切換自動更新：

1. 執行 `/plugin` 以開啟外掛程式管理器
2. 選擇 **Marketplaces**
3. 從清單中選擇市場
4. 選擇 **Enable auto-update** 或 **Disable auto-update**

官方 Anthropic 市場預設啟用自動更新。第三方和本機開發市場預設停用自動更新。

若要完全停用 Claude Code 和所有外掛程式的所有自動更新，請設定 `DISABLE_AUTOUPDATER` 環境變數。有關詳細資訊，請參閱[自動更新](/zh-TW/setup#auto-updates)。

若要在停用 Claude Code 自動更新的同時保持外掛程式自動更新啟用，請設定 `FORCE_AUTOUPDATE_PLUGINS=true` 以及 `DISABLE_AUTOUPDATER`：

```shell  theme={null}
export DISABLE_AUTOUPDATER=true
export FORCE_AUTOUPDATE_PLUGINS=true
```

當您想要手動管理 Claude Code 更新但仍然接收自動外掛程式更新時，這很有用。

## 配置團隊市場

團隊管理員可以透過將市場配置新增到 `.claude/settings.json` 來為專案設定自動市場安裝。當團隊成員信任儲存庫資料夾時，Claude Code 會提示他們安裝這些市場和外掛程式。

將 `extraKnownMarketplaces` 新增到您的專案的 `.claude/settings.json`：

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "my-team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

如需完整配置選項（包括 `extraKnownMarketplaces` 和 `enabledPlugins`），請參閱[外掛程式設定](/zh-TW/settings#plugin-settings)。

## 安全性

外掛程式和市場是高度受信任的元件，可以使用您的使用者權限在您的機器上執行任意程式碼。僅從您信任的來源安裝外掛程式和新增市場。組織可以使用[受管市場限制](/zh-TW/plugin-marketplaces#managed-marketplace-restrictions)限制使用者可以新增的市場。

## 故障排除

### /plugin 命令無法識別

如果您看到「未知命令」或 `/plugin` 命令未出現：

1. **檢查您的版本**：執行 `claude --version`。外掛程式需要版本 1.0.33 或更高版本。
2. **更新 Claude Code**：
   * **Homebrew**：`brew upgrade claude-code`
   * **npm**：`npm update -g @anthropic-ai/claude-code`
   * **原生安裝程式**：從[設定](/zh-TW/setup)重新執行安裝命令
3. **重新啟動 Claude Code**：更新後，重新啟動您的終端機並再次執行 `claude`。

### 常見問題

* **市場未載入**：驗證 URL 是否可存取以及 `.claude-plugin/marketplace.json` 是否存在於路徑中
* **外掛程式安裝失敗**：檢查外掛程式來源 URL 是否可存取以及儲存庫是否為公開（或您有存取權）
* **安裝後找不到檔案**：外掛程式被複製到快取中，因此參考外掛程式目錄外檔案的路徑將無法運作
* **外掛程式技能未出現**：使用 `rm -rf ~/.claude/plugins/cache` 清除快取，重新啟動 Claude Code，然後重新安裝外掛程式。

如需詳細的故障排除和解決方案，請參閱市場指南中的[故障排除](/zh-TW/plugin-marketplaces#troubleshooting)。如需偵錯工具，請參閱[偵錯和開發工具](/zh-TW/plugins-reference#debugging-and-development-tools)。

### 程式碼智能問題

* **語言伺服器未啟動**：驗證二進位檔已安裝且在您的 `$PATH` 中可用。檢查 `/plugin` Errors 標籤以獲取詳細資訊。
* **高記憶體使用量**：`rust-analyzer` 和 `pyright` 等語言伺服器在大型專案上可能會消耗大量記憶體。如果您遇到記憶體問題，請使用 `/plugin disable <plugin-name>` 停用外掛程式，並改為依賴 Claude 的內建搜尋工具。
* **monorepos 中的誤報診斷**：如果工作區配置不正確，語言伺服器可能會報告內部套件的未解決匯入錯誤。這些不會影響 Claude 編輯程式碼的能力。

## 後續步驟

* **構建您自己的外掛程式**：請參閱[外掛程式](/zh-TW/plugins)以建立技能、代理和 hooks
* **建立市場**：請參閱[建立外掛程式市場](/zh-TW/plugin-marketplaces)以將外掛程式分發給您的團隊或社群
* **技術參考**：請參閱[外掛程式參考](/zh-TW/plugins-reference)以取得完整規格
