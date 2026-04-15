> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 建立並分發 plugin marketplace

> 建立並託管 plugin marketplace，以在團隊和社群中分發 Claude Code 擴充功能。

**plugin marketplace** 是一個目錄，可讓您將 plugin 分發給他人。Marketplace 提供集中式發現、版本追蹤、自動更新，以及對多種來源類型（git 儲存庫、本機路徑等）的支援。本指南將向您展示如何建立自己的 marketplace，以與您的團隊或社群分享 plugin。

想要從現有 marketplace 安裝 plugin？請參閱[探索並安裝預先建立的 plugin](/zh-TW/discover-plugins)。

## 概述

建立並分發 marketplace 涉及：

1. **建立 plugin**：使用命令、agent、hook、MCP server 或 LSP server 建立一個或多個 plugin。本指南假設您已經有要分發的 plugin；有關如何建立 plugin 的詳細資訊，請參閱[建立 plugin](/zh-TW/plugins)。
2. **建立 marketplace 檔案**：定義 `marketplace.json`，列出您的 plugin 及其位置（請參閱[建立 marketplace 檔案](#create-the-marketplace-file)）。
3. **託管 marketplace**：推送到 GitHub、GitLab 或其他 git 主機（請參閱[託管並分發 marketplace](#host-and-distribute-marketplaces)）。
4. **與使用者分享**：使用者使用 `/plugin marketplace add` 新增您的 marketplace 並安裝個別 plugin（請參閱[探索並安裝 plugin](/zh-TW/discover-plugins)）。

一旦您的 marketplace 上線，您可以透過推送變更到您的儲存庫來更新它。使用者使用 `/plugin marketplace update` 重新整理其本機副本。

## 逐步解說：建立本機 marketplace

此範例建立一個包含一個 plugin 的 marketplace：用於程式碼審查的 `/quality-review` skill。您將建立目錄結構、新增 skill、建立 plugin manifest 和 marketplace 目錄，然後安裝並測試它。

<Steps>
  <Step title="建立目錄結構">
    ```bash theme={null}
    mkdir -p my-marketplace/.claude-plugin
    mkdir -p my-marketplace/plugins/quality-review-plugin/.claude-plugin
    mkdir -p my-marketplace/plugins/quality-review-plugin/skills/quality-review
    ```
  </Step>

  <Step title="建立 skill">
    建立 `SKILL.md` 檔案，定義 `/quality-review` skill 的功能。

    ```markdown my-marketplace/plugins/quality-review-plugin/skills/quality-review/SKILL.md theme={null}
    ---
    description: 檢查程式碼中的錯誤、安全性和效能問題
    disable-model-invocation: true
    ---

    檢查我選擇的程式碼或最近的變更，查找：
    - 潛在的錯誤或邊界情況
    - 安全性問題
    - 效能問題
    - 可讀性改進

    簡潔且可行動。
    ```
  </Step>

  <Step title="建立 plugin manifest">
    建立 `plugin.json` 檔案，描述 plugin。manifest 位於 `.claude-plugin/` 目錄中。

    ```json my-marketplace/plugins/quality-review-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "quality-review-plugin",
      "description": "新增 /quality-review skill 以進行快速程式碼審查",
      "version": "1.0.0"
    }
    ```
  </Step>

  <Step title="建立 marketplace 檔案">
    建立列出您的 plugin 的 marketplace 目錄。

    ```json my-marketplace/.claude-plugin/marketplace.json theme={null}
    {
      "name": "my-plugins",
      "owner": {
        "name": "Your Name"
      },
      "plugins": [
        {
          "name": "quality-review-plugin",
          "source": "./plugins/quality-review-plugin",
          "description": "新增 /quality-review skill 以進行快速程式碼審查"
        }
      ]
    }
    ```
  </Step>

  <Step title="新增並安裝">
    新增 marketplace 並安裝 plugin。

    ```shell theme={null}
    /plugin marketplace add ./my-marketplace
    /plugin install quality-review-plugin@my-plugins
    ```
  </Step>

  <Step title="試試看">
    在編輯器中選擇一些程式碼並執行您的新命令。

    ```shell theme={null}
    /quality-review
    ```
  </Step>
</Steps>

若要深入瞭解 plugin 可以執行的操作，包括 hook、agent、MCP server 和 LSP server，請參閱 [Plugins](/zh-TW/plugins)。

<Note>
  **plugin 如何安裝**：當使用者安裝 plugin 時，Claude Code 會將 plugin 目錄複製到快取位置。這表示 plugin 無法使用 `../shared-utils` 之類的路徑參考其目錄外的檔案，因為這些檔案不會被複製。

  如果您需要在 plugin 之間共享檔案，請使用符號連結（在複製期間會被追蹤）。有關詳細資訊，請參閱 [Plugin caching and file resolution](/zh-TW/plugins-reference#plugin-caching-and-file-resolution)。
</Note>

## 建立 marketplace 檔案

在您的儲存庫根目錄中建立 `.claude-plugin/marketplace.json`。此檔案定義您的 marketplace 名稱、擁有者資訊以及包含其來源的 plugin 清單。

每個 plugin 項目至少需要 `name` 和 `source`（從何處取得）。有關所有可用欄位，請參閱下面的[完整架構](#marketplace-schema)。

```json theme={null}
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@example.com"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "在保存時自動格式化程式碼",
      "version": "2.1.0",
      "author": {
        "name": "DevTools Team"
      }
    },
    {
      "name": "deployment-tools",
      "source": {
        "source": "github",
        "repo": "company/deploy-plugin"
      },
      "description": "部署自動化工具"
    }
  ]
}
```

## Marketplace 架構

### 必需欄位

| 欄位        | 類型     | 描述                                                                                                        | 範例             |
| :-------- | :----- | :-------------------------------------------------------------------------------------------------------- | :------------- |
| `name`    | string | Marketplace 識別碼（kebab-case，無空格）。這是公開的：使用者在安裝 plugin 時會看到它（例如，`/plugin install my-tool@your-marketplace`）。 | `"acme-tools"` |
| `owner`   | object | Marketplace 維護者資訊（[請參閱下面的欄位](#owner-fields)）                                                              |                |
| `plugins` | array  | 可用 plugin 的清單                                                                                             | 請參閱下面          |

<Note>
  **保留名稱**：以下 marketplace 名稱保留供 Anthropic 官方使用，第三方 marketplace 無法使用：`claude-code-marketplace`、`claude-code-plugins`、`claude-plugins-official`、`anthropic-marketplace`、`anthropic-plugins`、`agent-skills`、`knowledge-work-plugins`、`life-sciences`。模仿官方 marketplace 的名稱（如 `official-claude-plugins` 或 `anthropic-tools-v2`）也被阻止。
</Note>

### 擁有者欄位

| 欄位      | 類型     | 必需 | 描述         |
| :------ | :----- | :- | :--------- |
| `name`  | string | 是  | 維護者或團隊的名稱  |
| `email` | string | 否  | 維護者的聯絡電子郵件 |

### 選用中繼資料

| 欄位                     | 類型     | 描述                                                                                                           |
| :--------------------- | :----- | :----------------------------------------------------------------------------------------------------------- |
| `metadata.description` | string | 簡短的 marketplace 描述                                                                                           |
| `metadata.version`     | string | Marketplace 版本                                                                                               |
| `metadata.pluginRoot`  | string | 前置於相對 plugin 來源路徑的基本目錄（例如，`"./plugins"` 可讓您寫入 `"source": "formatter"` 而不是 `"source": "./plugins/formatter"`） |

## Plugin 項目

`plugins` 陣列中的每個 plugin 項目描述一個 plugin 及其位置。您可以包含 [plugin manifest 架構](/zh-TW/plugins-reference#plugin-manifest-schema)中的任何欄位（如 `description`、`version`、`author`、`commands`、`hooks` 等），加上這些 marketplace 特定欄位：`source`、`category`、`tags` 和 `strict`。

### 必需欄位

| 欄位       | 類型             | 描述                                                                                        |
| :------- | :------------- | :---------------------------------------------------------------------------------------- |
| `name`   | string         | Plugin 識別碼（kebab-case，無空格）。這是公開的：使用者在安裝時會看到它（例如，`/plugin install my-plugin@marketplace`）。 |
| `source` | string\|object | 從何處取得 plugin（請參閱下面的 [Plugin 來源](#plugin-sources)）                                         |

### 選用 plugin 欄位

**標準中繼資料欄位：**

| 欄位            | 類型      | 描述                                                                        |
| :------------ | :------ | :------------------------------------------------------------------------ |
| `description` | string  | 簡短的 plugin 描述                                                             |
| `version`     | string  | Plugin 版本                                                                 |
| `author`      | object  | Plugin 作者資訊（`name` 必需，`email` 選用）                                         |
| `homepage`    | string  | Plugin 首頁或文件 URL                                                          |
| `repository`  | string  | 原始碼儲存庫 URL                                                                |
| `license`     | string  | SPDX 授權識別碼（例如，MIT、Apache-2.0）                                             |
| `keywords`    | array   | 用於 plugin 發現和分類的標籤                                                        |
| `category`    | string  | Plugin 類別以供組織                                                             |
| `tags`        | array   | 用於可搜尋性的標籤                                                                 |
| `strict`      | boolean | 控制 `plugin.json` 是否為元件定義的權威（預設值：true）。請參閱下面的 [Strict mode](#strict-mode)。 |

**元件配置欄位：**

| 欄位           | 類型             | 描述                       |
| :----------- | :------------- | :----------------------- |
| `commands`   | string\|array  | 命令檔案或目錄的自訂路徑             |
| `agents`     | string\|array  | agent 檔案的自訂路徑            |
| `hooks`      | string\|object | 自訂 hook 配置或 hook 檔案的路徑   |
| `mcpServers` | string\|object | MCP server 配置或 MCP 配置的路徑 |
| `lspServers` | string\|object | LSP server 配置或 LSP 配置的路徑 |

## Plugin 來源

Plugin 來源告訴 Claude Code 在您的 marketplace 中列出的每個個別 plugin 從何處取得。這些在 `marketplace.json` 中每個 plugin 項目的 `source` 欄位中設定。

一旦 plugin 被複製或複製到本機，它就會被複製到本機版本化 plugin 快取中，位於 `~/.claude/plugins/cache`。

| 來源           | 類型                           | 欄位                               | 備註                                   |
| ------------ | ---------------------------- | -------------------------------- | ------------------------------------ |
| 相對路徑         | `string`（例如 `"./my-plugin"`） | 無                                | marketplace 儲存庫內的本機目錄。必須以 `./` 開頭    |
| `github`     | object                       | `repo`、`ref?`、`sha?`             |                                      |
| `url`        | object                       | `url`、`ref?`、`sha?`              | Git URL 來源                           |
| `git-subdir` | object                       | `url`、`path`、`ref?`、`sha?`       | git 儲存庫內的子目錄。稀疏複製以最小化大型 monorepo 的頻寬 |
| `npm`        | object                       | `package`、`version?`、`registry?` | 透過 `npm install` 安裝                  |

<Note>
  **Marketplace 來源與 plugin 來源**：這些是控制不同事物的不同概念。

  * **Marketplace 來源** — 從何處取得 `marketplace.json` 目錄本身。在使用者執行 `/plugin marketplace add` 或在 `extraKnownMarketplaces` 設定中設定。支援 `ref`（分支/標籤）但不支援 `sha`。
  * **Plugin 來源** — 從何處取得 marketplace 中列出的個別 plugin。在 `marketplace.json` 內每個 plugin 項目的 `source` 欄位中設定。支援 `ref`（分支/標籤）和 `sha`（確切提交）。

  例如，託管在 `acme-corp/plugin-catalog`（marketplace 來源）的 marketplace 可以列出從 `acme-corp/code-formatter`（plugin 來源）取得的 plugin。marketplace 來源和 plugin 來源指向不同的儲存庫，並獨立固定。
</Note>

### 相對路徑

對於同一儲存庫中的 plugin，使用以 `./` 開頭的路徑：

```json theme={null}
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

路徑相對於 marketplace 根目錄解析，即包含 `.claude-plugin/` 的目錄。在上面的範例中，`./plugins/my-plugin` 指向 `<repo>/plugins/my-plugin`，即使 `marketplace.json` 位於 `<repo>/.claude-plugin/marketplace.json`。不要使用 `../` 爬出 `.claude-plugin/`。

<Note>
  相對路徑僅在使用者透過 Git（GitHub、GitLab 或 git URL）新增您的 marketplace 時有效。如果使用者透過直接 URL 新增您的 marketplace 到 `marketplace.json` 檔案，相對路徑將無法正確解析。對於基於 URL 的分發，請改用 GitHub、npm 或 git URL 來源。有關詳細資訊，請參閱[疑難排解](#plugins-with-relative-paths-fail-in-url-based-marketplaces)。
</Note>

### GitHub 儲存庫

```json theme={null}
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```

您可以固定到特定分支、標籤或提交：

```json theme={null}
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| 欄位     | 類型     | 描述                               |
| :----- | :----- | :------------------------------- |
| `repo` | string | 必需。`owner/repo` 格式的 GitHub 儲存庫   |
| `ref`  | string | 選用。Git 分支或標籤（預設為儲存庫預設分支）         |
| `sha`  | string | 選用。完整的 40 字元 git 提交 SHA 以固定到確切版本 |

### Git 儲存庫

```json theme={null}
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

您可以固定到特定分支、標籤或提交：

```json theme={null}
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git",
    "ref": "main",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| 欄位    | 類型     | 描述                                                                                                   |
| :---- | :----- | :--------------------------------------------------------------------------------------------------- |
| `url` | string | 必需。完整的 git 儲存庫 URL（`https://` 或 `git@`）。`.git` 後綴是選用的，因此 Azure DevOps 和 AWS CodeCommit URL 不含後綴也可以運作 |
| `ref` | string | 選用。Git 分支或標籤（預設為儲存庫預設分支）                                                                             |
| `sha` | string | 選用。完整的 40 字元 git 提交 SHA 以固定到確切版本                                                                     |

### Git 子目錄

使用 `git-subdir` 指向位於 git 儲存庫子目錄內的 plugin。Claude Code 使用稀疏、部分複製來僅取得子目錄，最小化大型 monorepo 的頻寬。

```json theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin"
  }
}
```

您可以固定到特定分支、標籤或提交：

```json theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

`url` 欄位也接受 GitHub 簡寫（`owner/repo`）或 SSH URL（`git@github.com:owner/repo.git`）。

| 欄位     | 類型     | 描述                                                  |
| :----- | :----- | :-------------------------------------------------- |
| `url`  | string | 必需。Git 儲存庫 URL、GitHub `owner/repo` 簡寫或 SSH URL      |
| `path` | string | 必需。儲存庫內包含 plugin 的子目錄路徑（例如，`"tools/claude-plugin"`） |
| `ref`  | string | 選用。Git 分支或標籤（預設為儲存庫預設分支）                            |
| `sha`  | string | 選用。完整的 40 字元 git 提交 SHA 以固定到確切版本                    |

### npm 套件

作為 npm 套件分發的 plugin 使用 `npm install` 安裝。這適用於公開 npm 登錄表或您的團隊託管的任何私人登錄表上的任何套件。

```json theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin"
  }
}
```

若要固定到特定版本，請新增 `version` 欄位：

```json theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "2.1.0"
  }
}
```

若要從私人或內部登錄表安裝，請新增 `registry` 欄位：

```json theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "^2.0.0",
    "registry": "https://npm.example.com"
  }
}
```

| 欄位         | 類型     | 描述                                             |
| :--------- | :----- | :--------------------------------------------- |
| `package`  | string | 必需。套件名稱或範圍套件（例如，`@org/plugin`）                 |
| `version`  | string | 選用。版本或版本範圍（例如，`2.1.0`、`^2.0.0`、`~1.5.0`）       |
| `registry` | string | 選用。自訂 npm 登錄表 URL。預設為系統 npm 登錄表（通常為 npmjs.org） |

### 進階 plugin 項目

此範例顯示使用許多選用欄位的 plugin 項目，包括命令、agent、hook 和 MCP server 的自訂路徑：

```json theme={null}
{
  "name": "enterprise-tools",
  "source": {
    "source": "github",
    "repo": "company/enterprise-plugin"
  },
  "description": "企業工作流程自動化工具",
  "version": "2.1.0",
  "author": {
    "name": "Enterprise Team",
    "email": "enterprise@example.com"
  },
  "homepage": "https://docs.example.com/plugins/enterprise-tools",
  "repository": "https://github.com/company/enterprise-plugin",
  "license": "MIT",
  "keywords": ["enterprise", "workflow", "automation"],
  "category": "productivity",
  "commands": [
    "./commands/core/",
    "./commands/enterprise/",
    "./commands/experimental/preview.md"
  ],
  "agents": ["./agents/security-reviewer.md", "./agents/compliance-checker.md"],
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  },
  "mcpServers": {
    "enterprise-db": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  },
  "strict": false
}
```

需要注意的關鍵事項：

* **`commands` 和 `agents`**：您可以指定多個目錄或個別檔案。路徑相對於 plugin 根目錄。
* **`${CLAUDE_PLUGIN_ROOT}`**：在 hook 和 MCP server 配置中使用此變數來參考 plugin 安裝目錄內的檔案。這是必要的，因為 plugin 在安裝時被複製到快取位置。對於應在 plugin 更新後保留的相依性或狀態，請改用 [`${CLAUDE_PLUGIN_DATA}`](/zh-TW/plugins-reference#persistent-data-directory)。
* **`strict: false`**：由於此設定為 false，plugin 不需要自己的 `plugin.json`。marketplace 項目定義所有內容。請參閱下面的 [Strict mode](#strict-mode)。

### Strict mode

`strict` 欄位控制 `plugin.json` 是否為元件定義（命令、agent、hook、skill、MCP server、輸出樣式）的權威。

| 值          | 行為                                                                     |
| :--------- | :--------------------------------------------------------------------- |
| `true`（預設） | `plugin.json` 是權威。marketplace 項目可以用額外的元件補充它，兩個來源都會合併。                  |
| `false`    | marketplace 項目是完整定義。如果 plugin 也有宣告元件的 `plugin.json`，那就是衝突，plugin 無法載入。 |

**何時使用每種模式：**

* **`strict: true`**：plugin 有自己的 `plugin.json` 並管理自己的元件。marketplace 項目可以在頂部新增額外的命令或 hook。這是預設值，適用於大多數 plugin。
* **`strict: false`**：marketplace 運營商想要完全控制。plugin 儲存庫提供原始檔案，marketplace 項目定義這些檔案中的哪些被公開為命令、agent、hook 等。當 marketplace 以不同於 plugin 作者預期的方式重組或策劃 plugin 的元件時很有用。

## 託管並分發 marketplace

### 在 GitHub 上託管（推薦）

GitHub 提供最簡單的分發方法：

1. **建立儲存庫**：為您的 marketplace 設定新儲存庫
2. **新增 marketplace 檔案**：使用您的 plugin 定義建立 `.claude-plugin/marketplace.json`
3. **與團隊分享**：使用者使用 `/plugin marketplace add owner/repo` 新增您的 marketplace

**優點**：內建版本控制、問題追蹤和團隊協作功能。

### 在其他 git 服務上託管

任何 git 託管服務都可以使用，例如 GitLab、Bitbucket 和自託管伺服器。使用者使用完整儲存庫 URL 新增：

```shell theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git
```

### 私人儲存庫

Claude Code 支援從私人儲存庫安裝 plugin。對於手動安裝和更新，Claude Code 使用您現有的 git 認證助手。如果 `git clone` 在您的終端中適用於私人儲存庫，它在 Claude Code 中也適用。常見的認證助手包括用於 GitHub 的 `gh auth login`、macOS Keychain 和 `git-credential-store`。

背景自動更新在啟動時執行，不使用認證助手，因為互動式提示會阻止 Claude Code 啟動。若要為私人 marketplace 啟用自動更新，請在您的環境中設定適當的驗證令牌：

| 提供者       | 環境變數                        | 備註                    |
| :-------- | :-------------------------- | :-------------------- |
| GitHub    | `GITHUB_TOKEN` 或 `GH_TOKEN` | 個人存取令牌或 GitHub App 令牌 |
| GitLab    | `GITLAB_TOKEN` 或 `GL_TOKEN` | 個人存取令牌或專案令牌           |
| Bitbucket | `BITBUCKET_TOKEN`           | 應用程式密碼或儲存庫存取令牌        |

在您的 shell 配置中設定令牌（例如，`.bashrc`、`.zshrc`）或在執行 Claude Code 時傳遞它：

```bash theme={null}
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

<Note>
  對於 CI/CD 環境，將令牌配置為秘密環境變數。GitHub Actions 自動為同一組織中的儲存庫提供 `GITHUB_TOKEN`。
</Note>

### 在分發前在本機測試

在分享前在本機測試您的 marketplace：

```shell theme={null}
/plugin marketplace add ./my-local-marketplace
/plugin install test-plugin@my-local-marketplace
```

有關完整的新增命令範圍（GitHub、Git URL、本機路徑、遠端 URL），請參閱[新增 marketplace](/zh-TW/discover-plugins#add-marketplaces)。

### 為您的團隊要求 marketplace

您可以配置您的儲存庫，以便當團隊成員信任專案資料夾時，他們會自動被提示安裝您的 marketplace。將您的 marketplace 新增到 `.claude/settings.json`：

```json theme={null}
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

您也可以指定預設應啟用哪些 plugin：

```json theme={null}
{
  "enabledPlugins": {
    "code-formatter@company-tools": true,
    "deployment-tools@company-tools": true
  }
}
```

有關完整的配置選項，請參閱 [Plugin settings](/zh-TW/settings#plugin-settings)。

<Note>
  如果您使用具有相對路徑的本機 `directory` 或 `file` 來源，路徑會針對您的儲存庫的主要簽出進行解析。當您從 git worktree 執行 Claude Code 時，路徑仍然指向主要簽出，因此所有 worktree 共享相同的 marketplace 位置。Marketplace 狀態每個使用者儲存一次在 `~/.claude/plugins/known_marketplaces.json` 中，而不是每個專案。
</Note>

### 為容器預先填充 plugin

對於容器映像和 CI 環境，您可以在建置時預先填充 plugin 目錄，以便 Claude Code 啟動時已有 marketplace 和 plugin 可用，無需在執行時複製任何內容。設定 `CLAUDE_CODE_PLUGIN_SEED_DIR` 環境變數以指向此目錄。

若要分層多個種子目錄，請在 Unix 上使用 `:` 或在 Windows 上使用 `;` 分隔路徑。Claude Code 按順序搜尋每個目錄，第一個包含給定 marketplace 或 plugin 快取的種子獲勝。

種子目錄鏡像 `~/.claude/plugins` 的結構：

```
$CLAUDE_CODE_PLUGIN_SEED_DIR/
  known_marketplaces.json
  marketplaces/<name>/...
  cache/<marketplace>/<plugin>/<version>/...
```

建立種子目錄的最簡單方法是在映像建置期間執行 Claude Code 一次，安裝您需要的 plugin，然後將產生的 `~/.claude/plugins` 目錄複製到您的映像中，並將 `CLAUDE_CODE_PLUGIN_SEED_DIR` 指向它。

在啟動時，Claude Code 將種子的 `known_marketplaces.json` 中找到的 marketplace 註冊到主要配置中，並使用在 `cache/` 下找到的 plugin 快取，而無需重新複製。這在互動模式和使用 `-p` 旗標的非互動模式中都有效。

行為詳細資訊：

* **唯讀**：種子目錄永遠不會被寫入。自動更新對種子 marketplace 被停用，因為 git pull 在唯讀檔案系統上會失敗。
* **種子項目優先**：種子中宣告的 marketplace 在每次啟動時覆蓋使用者配置中的任何相符項目。若要選擇退出種子 plugin，請使用 `/plugin disable` 而不是移除 marketplace。
* **路徑解析**：Claude Code 在執行時透過探測 `$CLAUDE_CODE_PLUGIN_SEED_DIR/marketplaces/<name>/` 來定位 marketplace 內容，而不是信任儲存在種子 JSON 內的路徑。這表示即使在與建置位置不同的路徑上掛載，種子也能正確運作。
* **與設定組合**：如果 `extraKnownMarketplaces` 或 `enabledPlugins` 宣告已存在於種子中的 marketplace，Claude Code 使用種子副本而不是複製。

### 受管 marketplace 限制

對於需要對 plugin 來源進行嚴格控制的組織，管理員可以使用受管設定中的 [`strictKnownMarketplaces`](/zh-TW/settings#strictknownmarketplaces) 設定限制使用者允許新增的 plugin marketplace。

當在受管設定中配置 `strictKnownMarketplaces` 時，限制行為取決於值：

| 值        | 行為                            |
| -------- | ----------------------------- |
| 未定義（預設）  | 無限制。使用者可以新增任何 marketplace     |
| 空陣列 `[]` | 完全鎖定。使用者無法新增任何新 marketplace   |
| 來源清單     | 使用者只能新增與允許清單完全相符的 marketplace |

#### 常見配置

停用所有 marketplace 新增：

```json theme={null}
{
  "strictKnownMarketplaces": []
}
```

僅允許特定 marketplace：

```json theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    }
  ]
}
```

使用主機上的正規表達式模式匹配允許來自內部 git 伺服器的所有 marketplace。這是 [GitHub Enterprise Server](/zh-TW/github-enterprise-server#plugin-marketplaces-on-ghes) 或自託管 GitLab 執行個體的推薦方法：

```json theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

使用路徑上的正規表達式模式匹配允許來自特定目錄的檔案系統型 marketplace：

```json theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "pathPattern",
      "pathPattern": "^/opt/approved/"
    }
  ]
}
```

使用 `".*"` 作為 `pathPattern` 以允許任何檔案系統路徑，同時仍使用 `hostPattern` 控制網路來源。

<Note>
  `strictKnownMarketplaces` 限制使用者可以新增的內容，但不會自行註冊 marketplace。若要在不需要使用者執行 `/plugin marketplace add` 的情況下自動提供允許的 marketplace，請將其與同一 `managed-settings.json` 中的 [`extraKnownMarketplaces`](/zh-TW/settings#extraknownmarketplaces) 配對。請參閱[同時使用兩者](/zh-TW/settings#strictknownmarketplaces)。
</Note>

#### 限制如何運作

限制在 plugin 安裝過程的早期進行驗證，在任何網路請求或檔案系統操作之前。這可防止未授權的 marketplace 存取嘗試。

允許清單對大多數來源類型使用精確匹配。若要允許 marketplace，所有指定的欄位必須完全相符：

* 對於 GitHub 來源：`repo` 是必需的，如果在允許清單中指定，`ref` 或 `path` 也必須相符
* 對於 URL 來源：完整 URL 必須完全相符
* 對於 `hostPattern` 來源：marketplace 主機與正規表達式模式相符
* 對於 `pathPattern` 來源：marketplace 的檔案系統路徑與正規表達式模式相符

因為 `strictKnownMarketplaces` 在[受管設定](/zh-TW/settings#settings-files)中設定，個別使用者和專案配置無法覆蓋這些限制。

有關完整的配置詳細資訊，包括所有支援的來源類型和與 `extraKnownMarketplaces` 的比較，請參閱 [strictKnownMarketplaces 參考](/zh-TW/settings#strictknownmarketplaces)。

### 版本解析和發行通道

Plugin 版本決定快取路徑和更新偵測。您可以在 plugin manifest（`plugin.json`）或 marketplace 項目（`marketplace.json`）中指定版本。

<Warning>
  盡可能避免在兩個地方設定版本。plugin manifest 總是無聲地獲勝，這可能導致 marketplace 版本被忽略。對於相對路徑 plugin，在 marketplace 項目中設定版本。對於所有其他 plugin 來源，在 plugin manifest 中設定它。
</Warning>

#### 設定發行通道

若要為您的 plugin 支援「穩定」和「最新」發行通道，您可以設定兩個指向同一儲存庫的不同 ref 或 SHA 的 marketplace。然後，您可以透過[受管設定](/zh-TW/settings#settings-files)將兩個 marketplace 指派給不同的使用者群組。

<Warning>
  plugin 的 `plugin.json` 必須在每個固定的 ref 或提交處宣告不同的 `version`。如果兩個 ref 或提交具有相同的 manifest 版本，Claude Code 會將它們視為相同並跳過更新。
</Warning>

##### 範例

```json theme={null}
{
  "name": "stable-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": {
        "source": "github",
        "repo": "acme-corp/code-formatter",
        "ref": "stable"
      }
    }
  ]
}
```

```json theme={null}
{
  "name": "latest-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": {
        "source": "github",
        "repo": "acme-corp/code-formatter",
        "ref": "latest"
      }
    }
  ]
}
```

##### 將通道指派給使用者群組

透過受管設定將每個 marketplace 指派給適當的使用者群組。例如，穩定群組接收：

```json theme={null}
{
  "extraKnownMarketplaces": {
    "stable-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/stable-tools"
      }
    }
  }
}
```

早期存取群組改為接收 `latest-tools`：

```json theme={null}
{
  "extraKnownMarketplaces": {
    "latest-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/latest-tools"
      }
    }
  }
}
```

## 驗證和測試

在分享前測試您的 marketplace。

驗證您的 marketplace JSON 語法：

```bash theme={null}
claude plugin validate .
```

或從 Claude Code 內：

```shell theme={null}
/plugin validate .
```

新增 marketplace 進行測試：

```shell theme={null}
/plugin marketplace add ./path/to/marketplace
```

安裝測試 plugin 以驗證一切正常運作：

```shell theme={null}
/plugin install test-plugin@marketplace-name
```

有關完整的 plugin 測試工作流程，請參閱[在本機測試您的 plugin](/zh-TW/plugins#test-your-plugins-locally)。有關技術疑難排解，請參閱 [Plugins reference](/zh-TW/plugins-reference)。

## 疑難排解

### Marketplace 未載入

**症狀**：無法新增 marketplace 或看不到其中的 plugin

**解決方案**：

* 驗證 marketplace URL 可存取
* 檢查 `.claude-plugin/marketplace.json` 是否存在於指定路徑
* 使用 `claude plugin validate` 或 `/plugin validate` 確保 JSON 語法有效且 frontmatter 格式正確
* 對於私人儲存庫，確認您有存取權限

### Marketplace 驗證錯誤

從您的 marketplace 目錄執行 `claude plugin validate .` 或 `/plugin validate .` 以檢查問題。驗證器檢查 `plugin.json`、skill/agent/command frontmatter 和 `hooks/hooks.json` 是否有語法和架構錯誤。常見錯誤：

| 錯誤                                                | 原因                                 | 解決方案                                                        |
| :------------------------------------------------ | :--------------------------------- | :---------------------------------------------------------- |
| `File not found: .claude-plugin/marketplace.json` | 缺少 manifest                        | 使用必需欄位建立 `.claude-plugin/marketplace.json`                  |
| `Invalid JSON syntax: Unexpected token...`        | JSON 語法錯誤                          | 檢查缺少的逗號、多餘的逗號或未引用的字串                                        |
| `Duplicate plugin name "x" found in marketplace`  | 兩個 plugin 共享相同名稱                   | 為每個 plugin 指定唯一的 `name` 值                                   |
| `plugins[0].source: Path contains ".."`           | 來源路徑包含 `..`                        | 使用相對於 marketplace 根目錄的路徑，不含 `..`。請參閱[相對路徑](#relative-paths) |
| `YAML frontmatter failed to parse: ...`           | skill、agent 或 command 檔案中的 YAML 無效 | 修正 frontmatter 區塊中的 YAML 語法。在執行時，此檔案載入時不含中繼資料。              |
| `Invalid JSON syntax: ...`（hooks.json）            | 格式不正確的 `hooks/hooks.json`          | 修正 JSON 語法。格式不正確的 `hooks/hooks.json` 會防止整個 plugin 載入。       |

**警告**（非阻止性）：

* `Marketplace has no plugins defined`：將至少一個 plugin 新增到 `plugins` 陣列
* `No marketplace description provided`：新增 `metadata.description` 以幫助使用者瞭解您的 marketplace
* `Plugin name "x" is not kebab-case`：plugin 名稱包含大寫字母、空格或特殊字元。重新命名為僅包含小寫字母、數字和連字號（例如，`my-plugin`）。Claude Code 接受其他形式，但 Claude.ai marketplace 同步會拒絕它們。

### Plugin 安裝失敗

**症狀**：Marketplace 出現但 plugin 安裝失敗

**解決方案**：

* 驗證 plugin 來源 URL 可存取
* 檢查 plugin 目錄是否包含必需的檔案
* 對於 GitHub 來源，確保儲存庫是公開的或您有存取權
* 透過手動複製/下載測試 plugin 來源

### 私人儲存庫驗證失敗

**症狀**：從私人儲存庫安裝 plugin 時出現驗證錯誤

**解決方案**：

對於手動安裝和更新：

* 驗證您已使用您的 git 提供者進行驗證（例如，為 GitHub 執行 `gh auth status`）
* 檢查您的認證助手是否正確配置：`git config --global credential.helper`
* 嘗試手動複製儲存庫以驗證您的認證有效

對於背景自動更新：

* 在您的環境中設定適當的令牌：`echo $GITHUB_TOKEN`
* 檢查令牌是否具有必需的權限（對儲存庫的讀取存取權）
* 對於 GitHub，確保令牌對私人儲存庫具有 `repo` 範圍
* 對於 GitLab，確保令牌至少具有 `read_repository` 範圍
* 驗證令牌未過期

### Marketplace 更新在離線環境中失敗

**症狀**：Marketplace `git pull` 失敗，Claude Code 清除現有快取，導致 plugin 變得不可用。

**原因**：預設情況下，當 `git pull` 失敗時，Claude Code 會移除過時的複製並嘗試重新複製。在離線或隔離環境中，重新複製以相同方式失敗，導致 marketplace 目錄為空。

**解決方案**：設定 `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1` 以在拉取失敗時保留現有快取，而不是清除它：

```bash theme={null}
export CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1
```

設定此變數後，Claude Code 在 `git pull` 失敗時保留過時的 marketplace 複製，並繼續使用最後已知的良好狀態。對於儲存庫永遠無法到達的完全離線部署，請改用 [`CLAUDE_CODE_PLUGIN_SEED_DIR`](#pre-populate-plugins-for-containers) 在建置時預先填充 plugin 目錄。

### Git 操作逾時

**症狀**：Plugin 安裝或 marketplace 更新失敗，出現逾時錯誤，例如「Git clone timed out after 120s」或「Git pull timed out after 120s」。

**原因**：Claude Code 對所有 git 操作（包括複製 plugin 儲存庫和拉取 marketplace 更新）使用 120 秒逾時。大型儲存庫或緩慢的網路連線可能超過此限制。

**解決方案**：使用 `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS` 環境變數增加逾時。值以毫秒為單位：

```bash theme={null}
export CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=300000  # 5 分鐘
```

### 相對路徑 plugin 在基於 URL 的 marketplace 中失敗

**症狀**：透過 URL（例如 `https://example.com/marketplace.json`）新增 marketplace，但具有相對路徑來源（如 `"./plugins/my-plugin"`）的 plugin 無法安裝，出現「path not found」錯誤。

**原因**：基於 URL 的 marketplace 僅下載 `marketplace.json` 檔案本身。它們不從伺服器下載 plugin 檔案。marketplace 項目中的相對路徑參考未下載的遠端伺服器上的檔案。

**解決方案**：

* **使用外部來源**：將 plugin 項目變更為使用 GitHub、npm 或 git URL 來源，而不是相對路徑：
  ```json theme={null}
  { "name": "my-plugin", "source": { "source": "github", "repo": "owner/repo" } }
  ```
* **使用基於 Git 的 marketplace**：在 Git 儲存庫中託管您的 marketplace 並使用 git URL 新增它。基於 Git 的 marketplace 複製整個儲存庫，使相對路徑正常運作。

### 安裝後找不到檔案

**症狀**：Plugin 安裝但對檔案的參考失敗，特別是 plugin 目錄外的檔案

**原因**：Plugin 被複製到快取目錄而不是就地使用。參考 plugin 目錄外檔案的路徑（例如 `../shared-utils`）無法運作，因為這些檔案不會被複製。

**解決方案**：有關解決方案（包括符號連結和目錄重組），請參閱 [Plugin caching and file resolution](/zh-TW/plugins-reference#plugin-caching-and-file-resolution)。

有關其他偵錯工具和常見問題，請參閱[Debugging and development tools](/zh-TW/plugins-reference#debugging-and-development-tools)。

## 另請參閱

* [探索並安裝預先建立的 plugin](/zh-TW/discover-plugins) - 從現有 marketplace 安裝 plugin
* [Plugins](/zh-TW/plugins) - 建立您自己的 plugin
* [Plugins reference](/zh-TW/plugins-reference) - 完整的技術規格和架構
* [Plugin settings](/zh-TW/settings#plugin-settings) - Plugin 配置選項
* [strictKnownMarketplaces reference](/zh-TW/settings#strictknownmarketplaces) - 受管 marketplace 限制
