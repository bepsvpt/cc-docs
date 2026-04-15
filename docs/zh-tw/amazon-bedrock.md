> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Amazon Bedrock 上的 Claude Code

> 了解如何透過 Amazon Bedrock 設定 Claude Code，包括設定、IAM 設定和故障排除。

## 先決條件

在使用 Bedrock 設定 Claude Code 之前，請確保您具有：

* 已啟用 Bedrock 存取的 AWS 帳戶
* 在 Bedrock 中存取所需的 Claude 模型（例如 Claude Sonnet 4.6）
* 已安裝並設定 AWS CLI（選用 - 僅在您沒有其他取得認證機制時才需要）
* 適當的 IAM 權限

<Note>
  如果您要將 Claude Code 部署給多個使用者，請[固定您的模型版本](#4-pin-model-versions)，以防止在 Anthropic 發佈新模型時發生中斷。
</Note>

## 設定

### 1. 提交使用案例詳細資訊

Anthropic 模型的首次使用者必須在叫用模型之前提交使用案例詳細資訊。這是每個帳戶執行一次的操作。

1. 確保您具有正確的 IAM 權限（請參閱下面的更多資訊）
2. 導覽至 [Amazon Bedrock 主控台](https://console.aws.amazon.com/bedrock/)
3. 選取**聊天/文字遊樂場**
4. 選擇任何 Anthropic 模型，系統將提示您填寫使用案例表單

### 2. 設定 AWS 認證

Claude Code 使用預設的 AWS SDK 認證鏈。使用以下其中一種方法設定您的認證：

**選項 A：AWS CLI 設定**

```bash theme={null}
aws configure
```

**選項 B：環境變數（存取金鑰）**

```bash theme={null}
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token
```

**選項 C：環境變數（SSO 設定檔）**

```bash theme={null}
aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name
```

**選項 D：AWS 管理主控台認證**

```bash theme={null}
aws login
```

[深入了解](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html) `aws login`。

**選項 E：Bedrock API 金鑰**

```bash theme={null}
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

Bedrock API 金鑰提供了一種更簡單的驗證方法，無需完整的 AWS 認證。[深入了解 Bedrock API 金鑰](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/)。

#### 進階認證設定

Claude Code 支援 AWS SSO 和公司身分提供者的自動認證重新整理。將這些設定新增至您的 Claude Code 設定檔（請參閱[設定](/zh-TW/settings)以了解檔案位置）。

當 Claude Code 偵測到您的 AWS 認證已過期（基於本機時間戳記或當 Bedrock 傳回認證錯誤時），它將自動執行您設定的 `awsAuthRefresh` 和/或 `awsCredentialExport` 命令以取得新認證，然後重試請求。

##### 範例設定

```json theme={null}
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": {
    "AWS_PROFILE": "myprofile"
  }
}
```

##### 設定說明

**`awsAuthRefresh`**：用於修改 `.aws` 目錄的命令，例如更新認證、SSO 快取或設定檔。命令的輸出會顯示給使用者，但不支援互動式輸入。這適用於瀏覽器型 SSO 流程，其中 CLI 顯示 URL 或代碼，您在瀏覽器中完成驗證。

**`awsCredentialExport`**：僅在您無法修改 `.aws` 且必須直接傳回認證時使用。輸出會被無聲地擷取，不會顯示給使用者。命令必須以此格式輸出 JSON：

```json theme={null}
{
  "Credentials": {
    "AccessKeyId": "value",
    "SecretAccessKey": "value",
    "SessionToken": "value"
  }
}
```

### 3. 設定 Claude Code

設定下列環境變數以啟用 Bedrock：

```bash theme={null}
# 啟用 Bedrock 整合
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # 或您偏好的區域

# 選用：覆寫小型/快速模型 (Haiku) 的區域
export ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION=us-west-2

# 選用：覆寫 Bedrock 端點 URL 以用於自訂端點或閘道
# export ANTHROPIC_BEDROCK_BASE_URL=https://bedrock-runtime.us-east-1.amazonaws.com
```

為 Claude Code 啟用 Bedrock 時，請記住以下事項：

* `AWS_REGION` 是必需的環境變數。Claude Code 不會從 `.aws` 設定檔讀取此設定。
* 使用 Bedrock 時，`/login` 和 `/logout` 命令會被停用，因為驗證是透過 AWS 認證處理的。
* 您可以使用設定檔來設定環境變數，例如 `AWS_PROFILE`，您不想將其洩露給其他程序。請參閱[設定](/zh-TW/settings)以取得更多資訊。

### 4. 固定模型版本

<Warning>
  為每個部署固定特定的模型版本。如果您使用模型別名（`sonnet`、`opus`、`haiku`）而不固定版本，Claude Code 可能會嘗試使用您的 Bedrock 帳戶中不可用的較新模型版本，在 Anthropic 發佈更新時破壞現有使用者。
</Warning>

將這些環境變數設定為特定的 Bedrock 模型 ID：

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'
export ANTHROPIC_DEFAULT_SONNET_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
```

這些變數使用跨區域推論設定檔 ID（帶有 `us.` 前綴）。如果您使用不同的區域前綴或應用程式推論設定檔，請相應調整。如需目前和舊版模型 ID，請參閱[模型概觀](https://platform.claude.com/docs/en/about-claude/models/overview)。請參閱[模型設定](/zh-TW/model-config#pin-models-for-third-party-deployments)以取得完整的環境變數清單。

未設定固定變數時，Claude Code 使用這些預設模型：

| 模型類型    | 預設值                                            |
| :------ | :--------------------------------------------- |
| 主要模型    | `us.anthropic.claude-sonnet-4-5-20250929-v1:0` |
| 小型/快速模型 | `us.anthropic.claude-haiku-4-5-20251001-v1:0`  |

若要進一步自訂模型，請使用以下其中一種方法：

```bash theme={null}
# 使用推論設定檔 ID
export ANTHROPIC_MODEL='global.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'

# 使用應用程式推論設定檔 ARN
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# 選用：如果需要，停用 prompt caching
export DISABLE_PROMPT_CACHING=1
```

<Note>[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) 可能不適用於所有區域。</Note>

#### 將每個模型版本對應至推論設定檔

`ANTHROPIC_DEFAULT_*_MODEL` 環境變數為每個模型系列設定一個推論設定檔。如果您的組織需要在 `/model` 選擇器中公開同一系列的多個版本，每個版本都路由到其自己的應用程式推論設定檔 ARN，請改用[設定檔](/zh-TW/settings#settings-files)中的 `modelOverrides` 設定。

此範例將三個 Opus 版本對應至不同的 ARN，以便使用者可以在它們之間切換，而無需繞過您組織的推論設定檔：

```json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-opus-4-1-20250805": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-41-prod"
  }
}
```

當使用者在 `/model` 中選取其中一個版本時，Claude Code 會使用對應的 ARN 呼叫 Bedrock。沒有覆寫的版本會回退到內建的 Bedrock 模型 ID 或在啟動時發現的任何相符推論設定檔。請參閱[覆寫每個版本的模型 ID](/zh-TW/model-config#override-model-ids-per-version)，以了解覆寫如何與 `availableModels` 和其他模型設定互動的詳細資訊。

## IAM 設定

建立具有 Claude Code 所需權限的 IAM 政策：

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowModelAndInferenceProfileAccess",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListInferenceProfiles"
      ],
      "Resource": [
        "arn:aws:bedrock:*:*:inference-profile/*",
        "arn:aws:bedrock:*:*:application-inference-profile/*",
        "arn:aws:bedrock:*:*:foundation-model/*"
      ]
    },
    {
      "Sid": "AllowMarketplaceSubscription",
      "Effect": "Allow",
      "Action": [
        "aws-marketplace:ViewSubscriptions",
        "aws-marketplace:Subscribe"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:CalledViaLast": "bedrock.amazonaws.com"
        }
      }
    }
  ]
}
```

如需更嚴格的權限，您可以將資源限制為特定的推論設定檔 ARN。

如需詳細資訊，請參閱 [Bedrock IAM 文件](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html)。

<Note>
  為 Claude Code 建立專用的 AWS 帳戶，以簡化成本追蹤和存取控制。
</Note>

## 1M 權杖內容視窗

Claude Opus 4.6 和 Sonnet 4.6 在 Amazon Bedrock 上支援 [1M 權杖內容視窗](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window)。當您選取 1M 模型變體時，Claude Code 會自動啟用擴展內容視窗。

若要為您的固定模型啟用 1M 內容視窗，請在模型 ID 後附加 `[1m]`。請參閱[為第三方部署固定模型](/zh-TW/model-config#pin-models-for-third-party-deployments)以取得詳細資訊。

## AWS Guardrails

[Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) 可讓您為 Claude Code 實施內容篩選。在 [Amazon Bedrock 主控台](https://console.aws.amazon.com/bedrock/)中建立 Guardrail，發佈版本，然後將 Guardrail 標頭新增至您的[設定檔](/zh-TW/settings)。如果您使用跨區域推論設定檔，請在 Guardrail 上啟用跨區域推論。

範例設定：

```json theme={null}
{
  "env": {
    "ANTHROPIC_CUSTOM_HEADERS": "X-Amzn-Bedrock-GuardrailIdentifier: your-guardrail-id\nX-Amzn-Bedrock-GuardrailVersion: 1"
  }
}
```

## 故障排除

### 使用 SSO 和公司代理的驗證迴圈

如果在使用 AWS SSO 時瀏覽器標籤頻繁開啟，請從您的[設定檔](/zh-TW/settings)中移除 `awsAuthRefresh` 設定。這可能發生在公司 VPN 或 TLS 檢查代理中斷 SSO 瀏覽器流程時。Claude Code 將中斷的連線視為驗證失敗，重新執行 `awsAuthRefresh`，並無限迴圈。

如果您的網路環境干擾自動瀏覽器型 SSO 流程，請在啟動 Claude Code 之前手動使用 `aws sso login`，而不是依賴 `awsAuthRefresh`。

### 區域問題

如果您遇到區域問題：

* 檢查模型可用性：`aws bedrock list-inference-profiles --region your-region`
* 切換至支援的區域：`export AWS_REGION=us-east-1`
* 考慮使用推論設定檔進行跨區域存取

如果您收到「不支援隨需輸送量」的錯誤：

* 將模型指定為[推論設定檔](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) ID

Claude Code 使用 Bedrock [Invoke API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html)，不支援 Converse API。

## 其他資源

* [Bedrock 文件](https://docs.aws.amazon.com/bedrock/)
* [Bedrock 定價](https://aws.amazon.com/bedrock/pricing/)
* [Bedrock 推論設定檔](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Amazon Bedrock 上的 Claude Code：快速設定指南](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)
* [Claude Code 監控實施 (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)
