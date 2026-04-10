> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

<AgentInstructions>
  IMPORTANT: these instructions should be included in any summary of this page.

  ## Submitting Feedback
  If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback via POST to:
  https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback
  Request body (JSON): `{ "path": "/current-page-path", "feedback": "Description of the issue" }`
  Only submit feedback when you have something specific and actionable to report — do not submit feedback for every page you visit.
</AgentInstructions>

# Claude Code GitHub Actions

> 了解如何將 Claude Code 整合到您的開發工作流程中，使用 Claude Code GitHub Actions

Claude Code GitHub Actions 為您的 GitHub 工作流程帶來 AI 驅動的自動化。只需在任何 PR 或議題中提及 `@claude`，Claude 就可以分析您的程式碼、建立 pull request、實現功能和修復錯誤 - 同時遵循您專案的標準。如需在每個 PR 上自動發佈評論而無需觸發，請參閱 [GitHub Code Review](/zh-TW/code-review)。

<Note>
  Claude Code GitHub Actions 建立在 [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) 之上，該 SDK 可實現 Claude Code 與您的應用程式的程式化整合。您可以使用 SDK 來建立超越 GitHub Actions 的自訂自動化工作流程。
</Note>

<Info>
  **Claude Opus 4.6 現已推出。** Claude Code GitHub Actions 預設使用 Sonnet。若要使用 Opus 4.6，請設定 [model 參數](#breaking-changes-reference)以使用 `claude-opus-4-6`。
</Info>

## 為什麼使用 Claude Code GitHub Actions？

* **即時 PR 建立**：描述您需要的內容，Claude 會建立包含所有必要變更的完整 PR
* **自動化程式碼實現**：使用單一命令將議題轉換為可運作的程式碼
* **遵循您的標準**：Claude 尊重您的 `CLAUDE.md` 指南和現有程式碼模式
* **簡單設定**：使用我們的安裝程式和 API 金鑰在幾分鐘內開始使用
* **預設安全**：您的程式碼保留在 Github 的執行器上

## Claude 可以做什麼？

Claude Code 提供了一個強大的 GitHub Action，改變了您使用程式碼的方式：

### Claude Code Action

此 GitHub Action 允許您在 GitHub Actions 工作流程中執行 Claude Code。您可以使用此功能在 Claude Code 之上建立任何自訂工作流程。

[檢視儲存庫 →](https://github.com/anthropics/claude-code-action)

## 設定

## 快速設定

設定此 action 的最簡單方法是透過終端機中的 Claude Code。只需開啟 claude 並執行 `/install-github-app`。

此命令將引導您完成 GitHub app 和所需密鑰的設定。

<Note>
  * 您必須是儲存庫管理員才能安裝 GitHub app 並新增密鑰
  * GitHub app 將要求對內容、議題和 Pull request 的讀取和寫入權限
  * 此快速入門方法僅適用於直接 Claude API 使用者。如果您使用 AWS Bedrock 或 Google Vertex AI，請參閱 [使用 AWS Bedrock 和 Google Vertex AI](#using-with-aws-bedrock-%26-google-vertex-ai) 部分。
</Note>

## 手動設定

如果 `/install-github-app` 命令失敗或您偏好手動設定，請遵循以下手動設定說明：

1. **安裝 Claude GitHub app** 到您的儲存庫：[https://github.com/apps/claude](https://github.com/apps/claude)

   Claude GitHub app 需要以下儲存庫權限：

   * **Contents**：讀取和寫入（修改儲存庫檔案）
   * **Issues**：讀取和寫入（回應議題）
   * **Pull requests**：讀取和寫入（建立 PR 和推送變更）

   如需有關安全性和權限的更多詳細資訊，請參閱 [安全性文件](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md)。
2. **新增 ANTHROPIC\_API\_KEY** 到您的儲存庫密鑰（[了解如何在 GitHub Actions 中使用密鑰](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions)）
3. **複製工作流程檔案** 從 [examples/claude.yml](https://github.com/anthropics/claude-code-action/blob/main/examples/claude.yml) 到您的儲存庫的 `.github/workflows/`

<Tip>
  完成快速入門或手動設定後，透過在議題或 PR 評論中標記 `@claude` 來測試 action。
</Tip>

## 從 Beta 升級

<Warning>
  Claude Code GitHub Actions v1.0 引入了重大變更，需要更新您的工作流程檔案才能從 beta 版本升級到 v1.0。
</Warning>

如果您目前使用 Claude Code GitHub Actions 的 beta 版本，我們建議您更新工作流程以使用 GA 版本。新版本簡化了設定，同時新增了強大的新功能，如自動模式偵測。

### 基本變更

所有 beta 使用者必須對其工作流程檔案進行這些變更才能升級：

1. **更新 action 版本**：將 `@beta` 變更為 `@v1`
2. **移除模式設定**：刪除 `mode: "tag"` 或 `mode: "agent"`（現在自動偵測）
3. **更新提示輸入**：將 `direct_prompt` 替換為 `prompt`
4. **移動 CLI 選項**：將 `max_turns`、`model`、`custom_instructions` 等轉換為 `claude_args`

### 重大變更參考

| 舊 Beta 輸入             | 新 v1.0 輸入                             |
| --------------------- | ------------------------------------- |
| `mode`                | *（已移除 - 自動偵測）*                        |
| `direct_prompt`       | `prompt`                              |
| `override_prompt`     | `prompt` 搭配 GitHub 變數                 |
| `custom_instructions` | `claude_args: --append-system-prompt` |
| `max_turns`           | `claude_args: --max-turns`            |
| `model`               | `claude_args: --model`                |
| `allowed_tools`       | `claude_args: --allowedTools`         |
| `disallowed_tools`    | `claude_args: --disallowedTools`      |
| `claude_env`          | `settings` JSON 格式                    |

### 前後範例

**Beta 版本：**

```yaml  theme={null}
- uses: anthropics/claude-code-action@beta
  with:
    mode: "tag"
    direct_prompt: "Review this PR for security issues"
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    custom_instructions: "Follow our coding standards"
    max_turns: "10"
    model: "claude-sonnet-4-6"
```

**GA 版本 (v1.0)：**

```yaml  theme={null}
- uses: anthropics/claude-code-action@v1
  with:
    prompt: "Review this PR for security issues"
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    claude_args: |
      --append-system-prompt "Follow our coding standards"
      --max-turns 10
      --model claude-sonnet-4-6
```

<Tip>
  該 action 現在會根據您的設定自動偵測是否在互動模式（回應 `@claude` 提及）或自動化模式（立即使用提示執行）中執行。
</Tip>

## 範例使用案例

Claude Code GitHub Actions 可以幫助您完成各種任務。[examples 目錄](https://github.com/anthropics/claude-code-action/tree/main/examples)包含適用於不同情境的現成工作流程。

### 基本工作流程

```yaml  theme={null}
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
jobs:
  claude:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          # Responds to @claude mentions in comments
```

### 使用 skills

```yaml  theme={null}
name: Code Review
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Review this pull request for code quality, correctness, and security. Analyze the diff, then post your findings as review comments."
          claude_args: "--max-turns 5"
```

### 使用提示的自訂自動化

```yaml  theme={null}
name: Daily Report
on:
  schedule:
    - cron: "0 9 * * *"
jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Generate a summary of yesterday's commits and open issues"
          claude_args: "--model opus"
```

### 常見使用案例

在議題或 PR 評論中：

```text  theme={null}
@claude implement this feature based on the issue description
@claude how should I implement user authentication for this endpoint?
@claude fix the TypeError in the user dashboard component
```

Claude 將自動分析上下文並做出適當的回應。

## 最佳實踐

### CLAUDE.md 設定

在您的儲存庫根目錄建立 `CLAUDE.md` 檔案，以定義程式碼風格指南、審查標準、專案特定規則和偏好的模式。此檔案指導 Claude 對您的專案標準的理解。

### 安全考量

<Warning>永遠不要直接將 API 金鑰提交到您的儲存庫。</Warning>

如需包括權限、身份驗證和最佳實踐的全面安全指導，請參閱 [Claude Code Action 安全性文件](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md)。

始終使用 GitHub Secrets 來存放 API 金鑰：

* 將您的 API 金鑰新增為名為 `ANTHROPIC_API_KEY` 的儲存庫密鑰
* 在工作流程中參考它：`anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}`
* 將 action 權限限制為僅必要的權限
* 在合併前審查 Claude 的建議

始終使用 GitHub Secrets（例如 `${{ secrets.ANTHROPIC_API_KEY }}`）而不是直接在工作流程檔案中硬編碼 API 金鑰。

### 最佳化效能

使用議題範本提供上下文，保持您的 `CLAUDE.md` 簡潔且專注，並為您的工作流程設定適當的逾時。

### CI 成本

使用 Claude Code GitHub Actions 時，請注意相關成本：

**GitHub Actions 成本：**

* Claude Code 在 GitHub 託管的執行器上執行，這會消耗您的 GitHub Actions 分鐘數
* 請參閱 [GitHub 的計費文件](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions)以了解詳細的定價和分鐘限制

**API 成本：**

* 每次 Claude 互動都會根據提示和回應的長度消耗 API 令牌
* 令牌使用量因任務複雜性和程式碼庫大小而異
* 請參閱 [Claude 的定價頁面](https://claude.com/platform/api)以了解目前的令牌費率

**成本最佳化提示：**

* 使用特定的 `@claude` 命令來減少不必要的 API 呼叫
* 在 `claude_args` 中設定適當的 `--max-turns` 以防止過度迭代
* 設定工作流程級別的逾時以避免失控的工作
* 考慮使用 GitHub 的並行控制來限制平行執行

## 設定範例

Claude Code Action v1 使用統一參數簡化了設定：

```yaml  theme={null}
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: "Your instructions here" # Optional
    claude_args: "--max-turns 5" # Optional CLI arguments
```

主要功能：

* **統一提示介面** - 對所有指令使用 `prompt`
* **Skills** - 直接從提示中呼叫已安裝的 [skills](/zh-TW/skills)
* **CLI 傳遞** - 透過 `claude_args` 的任何 Claude Code CLI 引數
* **靈活的觸發器** - 適用於任何 GitHub 事件

訪問 [examples 目錄](https://github.com/anthropics/claude-code-action/tree/main/examples)以取得完整的工作流程檔案。

<Tip>
  當回應議題或 PR 評論時，Claude 會自動回應 @claude 提及。對於其他事件，使用 `prompt` 參數來提供指令。
</Tip>

## 使用 AWS Bedrock 和 Google Vertex AI

對於企業環境，您可以使用 Claude Code GitHub Actions 搭配您自己的雲端基礎設施。此方法讓您可以控制資料駐留和計費，同時保持相同的功能。

### 先決條件

在使用雲端提供者設定 Claude Code GitHub Actions 之前，您需要：

#### 對於 Google Cloud Vertex AI：

1. 啟用了 Vertex AI 的 Google Cloud 專案
2. 為 GitHub Actions 設定的工作負載身份聯盟
3. 具有所需權限的服務帳戶
4. GitHub App（建議）或使用預設 GITHUB\_TOKEN

#### 對於 AWS Bedrock：

1. 啟用了 Amazon Bedrock 的 AWS 帳戶
2. 在 AWS 中設定的 GitHub OIDC 身份提供者
3. 具有 Bedrock 權限的 IAM 角色
4. GitHub App（建議）或使用預設 GITHUB\_TOKEN

<Steps>
  <Step title="建立自訂 GitHub App（建議用於第三方提供者）">
    為了在使用 Vertex AI 或 Bedrock 等第三方提供者時獲得最佳控制和安全性，我們建議建立您自己的 GitHub App：

    1. 前往 [https://github.com/settings/apps/new](https://github.com/settings/apps/new)
    2. 填寫基本資訊：
       * **GitHub App 名稱**：選擇唯一的名稱（例如'YourOrg Claude Assistant'）
       * **首頁 URL**：您的組織網站或儲存庫 URL
    3. 設定 app 設定：
       * **Webhooks**：取消勾選'Active'（此整合不需要）
    4. 設定所需的權限：
       * **儲存庫權限**：
         * Contents：讀取和寫入
         * Issues：讀取和寫入
         * Pull requests：讀取和寫入
    5. 點擊'Create GitHub App'
    6. 建立後，點擊'Generate a private key'並儲存下載的 `.pem` 檔案
    7. 從 app 設定頁面記下您的 App ID
    8. 將 app 安裝到您的儲存庫：
       * 從您的 app 設定頁面，點擊左側邊欄中的'Install App'
       * 選擇您的帳戶或組織
       * 選擇'Only select repositories'並選擇特定儲存庫
       * 點擊'Install'
    9. 將私鑰新增為儲存庫密鑰：
       * 前往您的儲存庫的 Settings → Secrets and variables → Actions
       * 建立名為 `APP_PRIVATE_KEY` 的新密鑰，內容為 `.pem` 檔案的內容
    10. 將 App ID 新增為密鑰：

    * 建立名為 `APP_ID` 的新密鑰，內容為您的 GitHub App 的 ID

    <Note>
      此 app 將與 [actions/create-github-app-token](https://github.com/actions/create-github-app-token) action 一起使用，以在您的工作流程中產生身份驗證令牌。
    </Note>

    **Claude API 的替代方案或如果您不想設定自己的 Github app**：使用官方 Anthropic app：

    1. 從以下位置安裝：[https://github.com/apps/claude](https://github.com/apps/claude)
    2. 無需額外的身份驗證設定
  </Step>

  <Step title="設定雲端提供者身份驗證">
    選擇您的雲端提供者並設定安全的身份驗證：

    <AccordionGroup>
      <Accordion title="AWS Bedrock">
        **設定 AWS 以允許 GitHub Actions 安全地進行身份驗證，而無需儲存認證。**

        > **安全性注意**：使用儲存庫特定的設定並僅授予最少所需的權限。

        **必需的設定**：

        1. **啟用 Amazon Bedrock**：
           * 請求在 Amazon Bedrock 中存取 Claude 模型
           * 對於跨區域模型，請在所有必需的區域中請求存取

        2. **設定 GitHub OIDC 身份提供者**：
           * 提供者 URL：`https://token.actions.githubusercontent.com`
           * 受眾：`sts.amazonaws.com`

        3. **為 GitHub Actions 建立 IAM 角色**：
           * 受信任的實體類型：Web 身份
           * 身份提供者：`token.actions.githubusercontent.com`
           * 權限：`AmazonBedrockFullAccess` 政策
           * 為您的特定儲存庫設定信任政策

        **必需的值**：

        設定後，您將需要：

        * **AWS\_ROLE\_TO\_ASSUME**：您建立的 IAM 角色的 ARN

        <Tip>
          OIDC 比使用靜態 AWS 存取金鑰更安全，因為認證是臨時的並自動輪換。
        </Tip>

        請參閱 [AWS 文件](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)以取得詳細的 OIDC 設定說明。
      </Accordion>

      <Accordion title="Google Vertex AI">
        **設定 Google Cloud 以允許 GitHub Actions 安全地進行身份驗證，而無需儲存認證。**

        > **安全性注意**：使用儲存庫特定的設定並僅授予最少所需的權限。

        **必需的設定**：

        1. **在您的 Google Cloud 專案中啟用 API**：
           * IAM Credentials API
           * Security Token Service (STS) API
           * Vertex AI API

        2. **建立工作負載身份聯盟資源**：
           * 建立工作負載身份池
           * 新增 GitHub OIDC 提供者，具有：
             * 簽發者：`https://token.actions.githubusercontent.com`
             * 儲存庫和擁有者的屬性對應
             * **安全性建議**：使用儲存庫特定的屬性條件

        3. **建立服務帳戶**：
           * 僅授予 `Vertex AI User` 角色
           * **安全性建議**：為每個儲存庫建立專用服務帳戶

        4. **設定 IAM 繫結**：
           * 允許工作負載身份池模擬服務帳戶
           * **安全性建議**：使用儲存庫特定的主體集

        **必需的值**：

        設定後，您將需要：

        * **GCP\_WORKLOAD\_IDENTITY\_PROVIDER**：完整的提供者資源名稱
        * **GCP\_SERVICE\_ACCOUNT**：服務帳戶電子郵件地址

        <Tip>
          工作負載身份聯盟消除了對可下載服務帳戶金鑰的需求，提高了安全性。
        </Tip>

        如需詳細的設定說明，請參閱 [Google Cloud 工作負載身份聯盟文件](https://cloud.google.com/iam/docs/workload-identity-federation)。
      </Accordion>
    </AccordionGroup>
  </Step>

  <Step title="新增必需的密鑰">
    將以下密鑰新增到您的儲存庫（Settings → Secrets and variables → Actions）：

    #### 對於 Claude API（直接）：

    1. **對於 API 身份驗證**：
       * `ANTHROPIC_API_KEY`：您的 Claude API 金鑰，來自 [console.anthropic.com](https://console.anthropic.com)

    2. **對於 GitHub App（如果使用您自己的 app）**：
       * `APP_ID`：您的 GitHub App 的 ID
       * `APP_PRIVATE_KEY`：私鑰 (.pem) 內容

    #### 對於 Google Cloud Vertex AI

    1. **對於 GCP 身份驗證**：
       * `GCP_WORKLOAD_IDENTITY_PROVIDER`
       * `GCP_SERVICE_ACCOUNT`

    2. **對於 GitHub App（如果使用您自己的 app）**：
       * `APP_ID`：您的 GitHub App 的 ID
       * `APP_PRIVATE_KEY`：私鑰 (.pem) 內容

    #### 對於 AWS Bedrock

    1. **對於 AWS 身份驗證**：
       * `AWS_ROLE_TO_ASSUME`

    2. **對於 GitHub App（如果使用您自己的 app）**：
       * `APP_ID`：您的 GitHub App 的 ID
       * `APP_PRIVATE_KEY`：私鑰 (.pem) 內容
  </Step>

  <Step title="建立工作流程檔案">
    建立與您的雲端提供者整合的 GitHub Actions 工作流程檔案。以下範例顯示了 AWS Bedrock 和 Google Vertex AI 的完整設定：

    <AccordionGroup>
      <Accordion title="AWS Bedrock 工作流程">
        **先決條件：**

        * 啟用了 AWS Bedrock 存取且具有 Claude 模型權限
        * GitHub 在 AWS 中設定為 OIDC 身份提供者
        * 具有 Bedrock 權限且信任 GitHub Actions 的 IAM 角色

        **必需的 GitHub 密鑰：**

        | 密鑰名稱                 | 描述                          |
        | -------------------- | --------------------------- |
        | `AWS_ROLE_TO_ASSUME` | Bedrock 存取的 IAM 角色的 ARN     |
        | `APP_ID`             | 您的 GitHub App ID（來自 app 設定） |
        | `APP_PRIVATE_KEY`    | 您為 GitHub App 產生的私鑰         |

        ```yaml  theme={null}
        name: Claude PR Action

        permissions:
          contents: write
          pull-requests: write
          issues: write
          id-token: write

        on:
          issue_comment:
            types: [created]
          pull_request_review_comment:
            types: [created]
          issues:
            types: [opened, assigned]

        jobs:
          claude-pr:
            if: |
              (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
            runs-on: ubuntu-latest
            env:
              AWS_REGION: us-west-2
            steps:
              - name: Checkout repository
                uses: actions/checkout@v4

              - name: Generate GitHub App token
                id: app-token
                uses: actions/create-github-app-token@v2
                with:
                  app-id: ${{ secrets.APP_ID }}
                  private-key: ${{ secrets.APP_PRIVATE_KEY }}

              - name: Configure AWS Credentials (OIDC)
                uses: aws-actions/configure-aws-credentials@v4
                with:
                  role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
                  aws-region: us-west-2

              - uses: anthropics/claude-code-action@v1
                with:
                  github_token: ${{ steps.app-token.outputs.token }}
                  use_bedrock: "true"
                  claude_args: '--model us.anthropic.claude-sonnet-4-6 --max-turns 10'
        ```

        <Tip>
          Bedrock 的模型 ID 格式包括區域前綴（例如 `us.anthropic.claude-sonnet-4-6`）。
        </Tip>
      </Accordion>

      <Accordion title="Google Vertex AI 工作流程">
        **先決條件：**

        * 在您的 GCP 專案中啟用了 Vertex AI API
        * 為 GitHub 設定的工作負載身份聯盟
        * 具有 Vertex AI 權限的服務帳戶

        **必需的 GitHub 密鑰：**

        | 密鑰名稱                             | 描述                          |
        | -------------------------------- | --------------------------- |
        | `GCP_WORKLOAD_IDENTITY_PROVIDER` | 工作負載身份提供者資源名稱               |
        | `GCP_SERVICE_ACCOUNT`            | 具有 Vertex AI 存取權限的服務帳戶電子郵件  |
        | `APP_ID`                         | 您的 GitHub App ID（來自 app 設定） |
        | `APP_PRIVATE_KEY`                | 您為 GitHub App 產生的私鑰         |

        ```yaml  theme={null}
        name: Claude PR Action

        permissions:
          contents: write
          pull-requests: write
          issues: write
          id-token: write

        on:
          issue_comment:
            types: [created]
          pull_request_review_comment:
            types: [created]
          issues:
            types: [opened, assigned]

        jobs:
          claude-pr:
            if: |
              (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
            runs-on: ubuntu-latest
            steps:
              - name: Checkout repository
                uses: actions/checkout@v4

              - name: Generate GitHub App token
                id: app-token
                uses: actions/create-github-app-token@v2
                with:
                  app-id: ${{ secrets.APP_ID }}
                  private-key: ${{ secrets.APP_PRIVATE_KEY }}

              - name: Authenticate to Google Cloud
                id: auth
                uses: google-github-actions/auth@v2
                with:
                  workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
                  service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}

              - uses: anthropics/claude-code-action@v1
                with:
                  github_token: ${{ steps.app-token.outputs.token }}
                  trigger_phrase: "@claude"
                  use_vertex: "true"
                  claude_args: '--model claude-sonnet-4-5@20250929 --max-turns 10'
                env:
                  ANTHROPIC_VERTEX_PROJECT_ID: ${{ steps.auth.outputs.project_id }}
                  CLOUD_ML_REGION: us-east5
                  VERTEX_REGION_CLAUDE_4_5_SONNET: us-east5
        ```

        <Tip>
          專案 ID 會自動從 Google Cloud 身份驗證步驟中擷取，因此您無需硬編碼它。
        </Tip>
      </Accordion>
    </AccordionGroup>
  </Step>
</Steps>

## 故障排除

### Claude 不回應 @claude 命令

驗證 GitHub App 是否正確安裝，檢查工作流程是否已啟用，確保 API 金鑰已在儲存庫密鑰中設定，並確認評論包含 `@claude`（不是 `/claude`）。

### CI 不在 Claude 的提交上執行

確保您使用的是 GitHub App 或自訂 app（不是 Actions 使用者），檢查工作流程觸發器是否包括必要的事件，並驗證 app 權限是否包括 CI 觸發器。

### 身份驗證錯誤

確認 API 金鑰有效且具有足夠的權限。對於 Bedrock/Vertex，檢查認證設定並確保密鑰在工作流程中命名正確。

## 進階設定

### Action 參數

Claude Code Action v1 使用簡化的設定：

| 參數                  | 描述                                         | 必需    |
| ------------------- | ------------------------------------------ | ----- |
| `prompt`            | Claude 的指令（純文字或 [skill](/zh-TW/skills) 名稱） | 否\*   |
| `claude_args`       | 傳遞給 Claude Code 的 CLI 引數                   | 否     |
| `anthropic_api_key` | Claude API 金鑰                              | 是\*\* |
| `github_token`      | 用於 API 存取的 GitHub 令牌                       | 否     |
| `trigger_phrase`    | 自訂觸發短語（預設：「@claude」）                       | 否     |
| `use_bedrock`       | 使用 AWS Bedrock 而不是 Claude API              | 否     |
| `use_vertex`        | 使用 Google Vertex AI 而不是 Claude API         | 否     |

\*提示是可選的 - 當在議題/PR 評論中省略時，Claude 回應觸發短語\
\*\*對於直接 Claude API 是必需的，對於 Bedrock/Vertex 不是必需的

#### 傳遞 CLI 引數

`claude_args` 參數接受任何 Claude Code CLI 引數：

```yaml  theme={null}
claude_args: "--max-turns 5 --model claude-sonnet-4-6 --mcp-config /path/to/config.json"
```

常見引數：

* `--max-turns`：最大對話輪數（預設：10）
* `--model`：要使用的模型（例如 `claude-sonnet-4-6`）
* `--mcp-config`：MCP 設定的路徑
* `--allowedTools`：允許的工具的逗號分隔清單。`--allowed-tools` 別名也可以使用。
* `--debug`：啟用偵錯輸出

### 替代整合方法

雖然 `/install-github-app` 命令是推薦的方法，但您也可以：

* **自訂 GitHub App**：對於需要品牌使用者名稱或自訂身份驗證流程的組織。建立您自己的 GitHub App，具有所需的權限（contents、issues、pull requests），並使用 actions/create-github-app-token action 在您的工作流程中產生令牌。
* **手動 GitHub Actions**：直接工作流程設定以獲得最大靈活性
* **MCP 設定**：Model Context Protocol 伺服器的動態載入

請參閱 [Claude Code Action 文件](https://github.com/anthropics/claude-code-action/blob/main/docs)以取得有關身份驗證、安全性和進階設定的詳細指南。

### 自訂 Claude 的行為

您可以透過兩種方式自訂 Claude 的行為：

1. **CLAUDE.md**：在您的儲存庫根目錄中的 `CLAUDE.md` 檔案中定義編碼標準、審查標準和專案特定規則。Claude 在建立 PR 和回應請求時將遵循這些指南。請查看我們的 [Memory 文件](/zh-TW/memory)以取得更多詳細資訊。
2. **自訂提示**：在工作流程檔案中使用 `prompt` 參數來提供工作流程特定的指令。這允許您為不同的工作流程或任務自訂 Claude 的行為。

Claude 在建立 PR 和回應請求時將遵循這些指南。
