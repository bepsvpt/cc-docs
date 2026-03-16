> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 快速入門

> 歡迎使用 Claude Code！

本快速入門指南將在幾分鐘內讓您使用 AI 驅動的編碼協助。完成後，您將了解如何使用 Claude Code 進行常見的開發任務。

## 開始前

確保您擁有：

* 已開啟的終端或命令提示字元
  * 如果您從未使用過終端，請查看[終端指南](/zh-TW/terminal-guide)
* 一個要使用的程式碼專案
* 一個 [Claude 訂閱](https://claude.com/pricing)（Pro、Max、Teams 或 Enterprise）、[Claude Console](https://console.anthropic.com/) 帳戶，或透過[支援的雲端提供商](/zh-TW/third-party-integrations)的存取權

<Note>
  本指南涵蓋終端 CLI。Claude Code 也可在[網頁](https://claude.ai/code)、[桌面應用程式](/zh-TW/desktop)、[VS Code](/zh-TW/vs-code) 和 [JetBrains IDE](/zh-TW/jetbrains)、[Slack](/zh-TW/slack) 中使用，以及透過 [GitHub Actions](/zh-TW/github-actions) 和 [GitLab](/zh-TW/gitlab-ci-cd) 進行 CI/CD。請參閱[所有介面](/zh-TW/overview#use-claude-code-everywhere)。
</Note>

## 步驟 1：安裝 Claude Code

To install Claude Code, use one of the following methods:

<Tabs>
  <Tab title="Native Install (Recommended)">
    **macOS, Linux, WSL:**

    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell:**

    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD:**

    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```

    **Windows requires [Git for Windows](https://git-scm.com/downloads/win).** Install it first if you don't have it.

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash  theme={null}
    brew install --cask claude-code
    ```

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` periodically to get the latest features and security fixes.
    </Info>
  </Tab>

  <Tab title="WinGet">
    ```powershell  theme={null}
    winget install Anthropic.ClaudeCode
    ```

    <Info>
      WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
    </Info>
  </Tab>
</Tabs>

## 步驟 2：登入您的帳戶

Claude Code 需要帳戶才能使用。當您使用 `claude` 命令啟動互動式工作階段時，您需要登入：

```bash  theme={null}
claude
# 首次使用時系統會提示您登入
```

```bash  theme={null}
/login
# 按照提示使用您的帳戶登入
```

您可以使用以下任何帳戶類型登入：

* [Claude Pro、Max、Teams 或 Enterprise](https://claude.com/pricing)（推薦）
* [Claude Console](https://console.anthropic.com/)（具有預付額度的 API 存取）。首次登入時，Console 中會自動為集中式成本追蹤建立一個「Claude Code」工作區。
* [Amazon Bedrock、Google Vertex AI 或 Microsoft Foundry](/zh-TW/third-party-integrations)（企業雲端提供商）

登入後，您的認證將被儲存，您無需再次登入。若要稍後切換帳戶，請使用 `/login` 命令。

## 步驟 3：啟動您的第一個工作階段

在任何專案目錄中開啟您的終端並啟動 Claude Code：

```bash  theme={null}
cd /path/to/your/project
claude
```

您將看到 Claude Code 歡迎畫面，其中包含您的工作階段資訊、最近的對話和最新更新。輸入 `/help` 以查看可用命令，或輸入 `/resume` 以繼續之前的對話。

<Tip>
  登入後（步驟 2），您的認證將儲存在您的系統上。在[認證管理](/zh-TW/authentication#credential-management)中了解更多。
</Tip>

## 步驟 4：提出您的第一個問題

讓我們從了解您的程式碼庫開始。嘗試以下命令之一：

```text  theme={null}
what does this project do?
```

Claude 將分析您的檔案並提供摘要。您也可以提出更具體的問題：

```text  theme={null}
what technologies does this project use?
```

```text  theme={null}
where is the main entry point?
```

```text  theme={null}
explain the folder structure
```

您也可以詢問 Claude 其自身的功能：

```text  theme={null}
what can Claude Code do?
```

```text  theme={null}
how do I create custom skills in Claude Code?
```

```text  theme={null}
can Claude Code work with Docker?
```

<Note>
  Claude Code 根據需要讀取您的專案檔案。您無需手動新增內容。
</Note>

## 步驟 5：進行您的第一次程式碼變更

現在讓我們讓 Claude Code 進行一些實際的編碼。嘗試一個簡單的任務：

```text  theme={null}
add a hello world function to the main file
```

Claude Code 將：

1. 找到適當的檔案
2. 向您顯示建議的變更
3. 要求您的批准
4. 進行編輯

<Note>
  Claude Code 在修改檔案前始終要求許可。您可以批准個別變更或為工作階段啟用「全部接受」模式。
</Note>

## 步驟 6：使用 Git 與 Claude Code

Claude Code 使 Git 操作變得對話式：

```text  theme={null}
what files have I changed?
```

```text  theme={null}
commit my changes with a descriptive message
```

您也可以提示進行更複雜的 Git 操作：

```text  theme={null}
create a new branch called feature/quickstart
```

```text  theme={null}
show me the last 5 commits
```

```text  theme={null}
help me resolve merge conflicts
```

## 步驟 7：修復錯誤或新增功能

Claude 擅長除錯和功能實現。

用自然語言描述您想要的內容：

```text  theme={null}
add input validation to the user registration form
```

或修復現有問題：

```text  theme={null}
there's a bug where users can submit empty forms - fix it
```

Claude Code 將：

* 定位相關程式碼
* 理解上下文
* 實現解決方案
* 如果可用，執行測試

## 步驟 8：測試其他常見工作流程

有許多方式可以與 Claude 合作：

**重構程式碼**

```text  theme={null}
refactor the authentication module to use async/await instead of callbacks
```

**編寫測試**

```text  theme={null}
write unit tests for the calculator functions
```

**更新文件**

```text  theme={null}
update the README with installation instructions
```

**程式碼審查**

```text  theme={null}
review my changes and suggest improvements
```

<Tip>
  像與有幫助的同事交談一樣與 Claude 交談。描述您想要達成的目標，它將幫助您實現。
</Tip>

## 基本命令

以下是日常使用中最重要的命令：

| 命令                  | 功能             | 範例                                  |
| ------------------- | -------------- | ----------------------------------- |
| `claude`            | 啟動互動模式         | `claude`                            |
| `claude "task"`     | 執行一次性任務        | `claude "fix the build error"`      |
| `claude -p "query"` | 執行一次性查詢，然後退出   | `claude -p "explain this function"` |
| `claude -c`         | 在目前目錄中繼續最近的對話  | `claude -c`                         |
| `claude -r`         | 恢復之前的對話        | `claude -r`                         |
| `claude commit`     | 建立 Git 提交      | `claude commit`                     |
| `/clear`            | 清除對話歷史         | `/clear`                            |
| `/help`             | 顯示可用命令         | `/help`                             |
| `exit` 或 Ctrl+C     | 退出 Claude Code | `exit`                              |

請參閱 [CLI 參考](/zh-TW/cli-reference)以取得完整的命令列表。

## 初學者的專業提示

如需更多資訊，請參閱[最佳實踐](/zh-TW/best-practices)和[常見工作流程](/zh-TW/common-workflows)。

<AccordionGroup>
  <Accordion title="對您的請求要具體">
    不要這樣做：'修復錯誤'

    試試這樣：'修復登入錯誤，使用者輸入錯誤認證後看到空白畫面'
  </Accordion>

  <Accordion title="使用逐步說明">
    將複雜任務分解為步驟：

    ```text  theme={null}
    1. create a new database table for user profiles
    2. create an API endpoint to get and update user profiles
    3. build a webpage that allows users to see and edit their information
    ```
  </Accordion>

  <Accordion title="讓 Claude 先探索">
    在進行變更之前，讓 Claude 了解您的程式碼：

    ```text  theme={null}
    analyze the database schema
    ```

    ```text  theme={null}
    build a dashboard showing products that are most frequently returned by our UK customers
    ```
  </Accordion>

  <Accordion title="使用快捷方式節省時間">
    * 按 `?` 查看所有可用的快捷鍵
    * 使用 Tab 進行命令完成
    * 按 ↑ 查看命令歷史
    * 輸入 `/` 查看所有命令和 skills
  </Accordion>
</AccordionGroup>

## 接下來呢？

現在您已經學習了基礎知識，請探索更多進階功能：

<CardGroup cols={2}>
  <Card title="Claude Code 如何運作" icon="microchip" href="/zh-TW/how-claude-code-works">
    了解代理迴圈、內建工具以及 Claude Code 如何與您的專案互動
  </Card>

  <Card title="最佳實踐" icon="star" href="/zh-TW/best-practices">
    透過有效的提示和專案設定獲得更好的結果
  </Card>

  <Card title="常見工作流程" icon="graduation-cap" href="/zh-TW/common-workflows">
    常見任務的逐步指南
  </Card>

  <Card title="擴展 Claude Code" icon="puzzle-piece" href="/zh-TW/features-overview">
    使用 CLAUDE.md、skills、hooks、MCP 等進行自訂
  </Card>
</CardGroup>

## 獲取幫助

* **在 Claude Code 中**：輸入 `/help` 或詢問「how do I...」
* **文件**：您在這裡！瀏覽其他指南
* **社群**：加入我們的 [Discord](https://www.anthropic.com/discord) 以獲取提示和支援
