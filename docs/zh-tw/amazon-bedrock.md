> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Amazon Bedrock 上的 Claude Code

> 了解如何透過 Amazon Bedrock 設定 Claude Code，包括設定、IAM 設定和故障排除。

export const ContactSalesCard = ({surface}) => {
  const utm = content => `utm_source=claude_code&utm_medium=docs&utm_content=${surface}_${content}`;
  const iconArrowRight = (size = 13) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="5" y1="12" x2="19" y2="12" />
      <polyline points="12 5 19 12 12 19" />
    </svg>;
  const STYLES = `
.cc-cs {
  --cs-slate: #141413;
  --cs-clay: #d97757;
  --cs-clay-deep: #c6613f;
  --cs-gray-000: #ffffff;
  --cs-gray-700: #3d3d3a;
  --cs-border-default: rgba(31, 30, 29, 0.15);
  font-family: inherit;
}
.dark .cc-cs {
  --cs-slate: #f0eee6;
  --cs-gray-000: #262624;
  --cs-gray-700: #bfbdb4;
  --cs-border-default: rgba(240, 238, 230, 0.14);
}
.cc-cs-card {
  display: flex; align-items: center; justify-content: space-between;
  gap: 16px; padding: 14px 16px; margin: 0;
  background: var(--cs-gray-000); border: 0.5px solid var(--cs-border-default);
  border-radius: 8px; flex-wrap: wrap;
}
.cc-cs-text { font-size: 13px; color: var(--cs-gray-700); line-height: 1.5; flex: 1; min-width: 240px; }
.cc-cs-text strong { font-weight: 550; color: var(--cs-slate); }
.cc-cs-actions { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.cc-cs-btn-clay {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--cs-clay-deep); color: #fff; border: none;
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
  transition: background-color 0.15s; white-space: nowrap;
}
.cc-cs-btn-clay:hover { background: var(--cs-clay); }
.cc-cs-btn-ghost {
  display: inline-flex; align-items: center; gap: 8px;
  background: transparent; color: var(--cs-gray-700);
  border: 0.5px solid var(--cs-border-default);
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
}
.cc-cs-btn-ghost:hover { background: rgba(0, 0, 0, 0.04); }
.dark .cc-cs-btn-ghost:hover { background: rgba(255, 255, 255, 0.04); }
@media (max-width: 720px) {
  .cc-cs-actions { width: 100%; }
}
`;
  return <div className="cc-cs not-prose">
      <style>{STYLES}</style>
      <div className="cc-cs-card">
        <div className="cc-cs-text">
          <strong>Deploying Claude Code across your organization?</strong> Talk to sales about enterprise plans, SSO, and centralized billing.
        </div>
        <div className="cc-cs-actions">
          <a href={`https://claude.com/pricing?${utm('view_plans')}#plans-business`} className="cc-cs-btn-ghost">
            View plans
          </a>
          <a href={`https://claude.com/contact-sales?${utm('contact_sales')}`} className="cc-cs-btn-clay">
            Contact sales {iconArrowRight()}
          </a>
        </div>
      </div>
    </div>;
};

export const Experiment = ({flag, treatment, children}) => {
  const VID_KEY = 'exp_vid';
  const CONSENT_COUNTRIES = new Set(['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'RE', 'GP', 'MQ', 'GF', 'YT', 'BL', 'MF', 'PM', 'WF', 'PF', 'NC', 'AW', 'CW', 'SX', 'FO', 'GL', 'AX', 'GB', 'UK', 'AI', 'BM', 'IO', 'VG', 'KY', 'FK', 'GI', 'MS', 'PN', 'SH', 'TC', 'GG', 'JE', 'IM', 'CA', 'BR', 'IN']);
  const fnv1a = s => {
    let h = 0x811c9dc5;
    for (let i = 0; i < s.length; i++) {
      h ^= s.charCodeAt(i);
      h += (h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24);
    }
    return h >>> 0;
  };
  const bucket = (seed, vid) => fnv1a(fnv1a(seed + vid) + '') % 10000 < 5000 ? 'control' : 'treatment';
  const [decision] = useState(() => {
    const params = new URLSearchParams(location.search);
    const preBucketed = document.documentElement.dataset['gb_' + flag.replace(/-/g, '_')];
    const force = params.get('gb-force');
    if (force) {
      for (const p of force.split(',')) {
        const [k, v] = p.split(':');
        if (k === flag) return {
          variant: v || 'treatment',
          track: false
        };
      }
    }
    if (navigator.globalPrivacyControl) {
      return {
        variant: 'control',
        track: false
      };
    }
    const prefsMatch = document.cookie.match(/(?:^|; )anthropic-consent-preferences=([^;]+)/);
    if (prefsMatch) {
      try {
        if (JSON.parse(decodeURIComponent(prefsMatch[1])).analytics !== true) {
          return {
            variant: 'control',
            track: false
          };
        }
      } catch {
        return {
          variant: 'control',
          track: false
        };
      }
    } else {
      const country = params.get('country')?.toUpperCase() || (document.cookie.match(/(?:^|; )cf_geo=([A-Z]{2})/) || [])[1];
      if (!country || CONSENT_COUNTRIES.has(country)) {
        return {
          variant: 'control',
          track: false
        };
      }
    }
    let vid;
    try {
      const ajsMatch = document.cookie.match(/(?:^|; )ajs_anonymous_id=([^;]+)/);
      if (ajsMatch) {
        vid = decodeURIComponent(ajsMatch[1]).replace(/^"|"$/g, '');
      } else {
        vid = localStorage.getItem(VID_KEY);
        if (!vid) {
          vid = crypto.randomUUID();
        }
        document.cookie = `ajs_anonymous_id=${vid}; domain=.claude.com; path=/; Secure; SameSite=Lax; max-age=31536000`;
      }
      try {
        localStorage.setItem(VID_KEY, vid);
      } catch {}
    } catch {
      return {
        variant: 'control',
        track: false
      };
    }
    const variant = preBucketed === '1' ? 'treatment' : preBucketed === '0' ? 'control' : bucket(flag, vid);
    return {
      variant,
      track: true,
      vid
    };
  });
  useEffect(() => {
    if (!decision.track) return;
    fetch('https://api.anthropic.com/api/event_logging/v2/batch', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-service-name': 'claude_code_docs'
      },
      body: JSON.stringify({
        events: [{
          event_type: 'GrowthbookExperimentEvent',
          event_data: {
            device_id: decision.vid,
            anonymous_id: decision.vid,
            timestamp: new Date().toISOString(),
            experiment_id: flag,
            variation_id: decision.variant === 'treatment' ? 1 : 0,
            environment: 'production'
          }
        }]
      }),
      keepalive: true
    }).catch(() => {});
  }, []);
  return decision.variant === 'treatment' ? treatment : children;
};

<Experiment flag="docs-contact-sales-cta" treatment={<ContactSalesCard surface="bedrock" />} />

## 先決條件

在使用 Bedrock 設定 Claude Code 之前，請確保您具有：

* 已啟用 Bedrock 存取的 AWS 帳戶
* 在 Bedrock 中存取所需的 Claude 模型（例如 Claude Sonnet 4.6）
* 已安裝並設定 AWS CLI（選用 - 僅在您沒有其他取得認證機制時才需要）
* 適當的 IAM 權限

若要使用您自己的 Bedrock 認證登入，請遵循下面的[使用 Bedrock 登入](#sign-in-with-bedrock)。若要在整個團隊中部署 Claude Code，請使用[手動設定](#set-up-manually)步驟並在推出前[固定您的模型版本](#4-pin-model-versions)。

## 使用 Bedrock 登入

如果您有 AWS 認證並想開始透過 Bedrock 使用 Claude Code，登入精靈會引導您完成整個過程。您每個帳戶完成一次 AWS 端的先決條件；精靈會處理 Claude Code 端。

<Steps>
  <Step title="在您的 AWS 帳戶中啟用 Anthropic 模型">
    在 [Amazon Bedrock 主控台](https://console.aws.amazon.com/bedrock/)中，開啟模型目錄，選取 Anthropic 模型，然後提交使用案例表單。提交後立即授予存取權限。請參閱[提交使用案例詳細資訊](#1-submit-use-case-details)以了解 AWS Organizations，以及[IAM 設定](#iam-configuration)以了解您的角色所需的權限。
  </Step>

  <Step title="啟動 Claude Code 並選擇 Bedrock">
    執行 `claude`。在登入提示處，選取**第三方平台**，然後選取 **Amazon Bedrock**。
  </Step>

  <Step title="遵循精靈提示">
    選擇您如何向 AWS 進行驗證：從您的 `~/.aws` 目錄偵測到的 AWS 設定檔、Bedrock API 金鑰、存取金鑰和密碼，或已在您的環境中的認證。精靈會選取您的區域，驗證您的帳戶可以叫用哪些 Claude 模型，並讓您固定它們。它會將結果儲存到您的[使用者設定檔](/zh-TW/settings)的 `env` 區塊，因此您不需要自己匯出環境變數。
  </Step>
</Steps>

登入後，隨時執行 `/setup-bedrock` 以重新開啟精靈並變更您的認證、區域或模型固定。

## 手動設定

若要透過環境變數而不是精靈來設定 Bedrock，例如在 CI 或指令碼化企業推出中，請遵循下面的步驟。

### 1. 提交使用案例詳細資訊

Anthropic 模型的首次使用者必須在叫用模型之前提交使用案例詳細資訊。這是每個 AWS 帳戶執行一次的操作。

1. 確保您具有下面所述的正確 IAM 權限
2. 導覽至 [Amazon Bedrock 主控台](https://console.aws.amazon.com/bedrock/)
3. 從**模型目錄**選取 Anthropic 模型
4. 完成使用案例表單。提交後立即授予存取權限。

如果您使用 AWS Organizations，您可以使用 [`PutUseCaseForModelAccess` API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_PutUseCaseForModelAccess.html) 從管理帳戶提交一次表單。此呼叫需要 `bedrock:PutUseCaseForModelAccess` IAM 權限。核准會自動延伸到子帳戶。

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

# 選用：覆寫小型/快速模型 (Haiku) 的區域。
# 也適用於 Bedrock Mantle。
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
  在部署給多個使用者時固定特定的模型版本。如果不固定，模型別名（例如 `sonnet` 和 `opus`）會解析為最新版本，當 Anthropic 發佈更新時，該版本可能在您的 Bedrock 帳戶中尚不可用。Claude Code 在啟動時會在最新版本不可用時[回退](#startup-model-checks)到先前版本，但固定可讓您控制使用者何時移至新模型。
</Warning>

將這些環境變數設定為特定的 Bedrock 模型 ID。

如果沒有 `ANTHROPIC_DEFAULT_OPUS_MODEL`，Bedrock 上的 `opus` 別名會解析為 Opus 4.6。將其設定為 Opus 4.7 ID 以使用最新模型：

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-7'
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

# 選用：要求 1 小時 prompt cache TTL 而不是 5 分鐘預設值
export ENABLE_PROMPT_CACHING_1H=1
```

<Note>[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) 可能不適用於所有區域。使用 1 小時 TTL 的快取寫入按比 5 分鐘寫入更高的費率計費。</Note>

#### 將每個模型版本對應至推論設定檔

`ANTHROPIC_DEFAULT_*_MODEL` 環境變數為每個模型系列設定一個推論設定檔。如果您的組織需要在 `/model` 選擇器中公開同一系列的多個版本，每個版本都路由到其自己的應用程式推論設定檔 ARN，請改用[設定檔](/zh-TW/settings#settings-files)中的 `modelOverrides` 設定。

此範例將四個 Opus 版本對應至不同的 ARN，以便使用者可以在它們之間切換，而無需繞過您組織的推論設定檔：

```json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-7": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-47-prod",
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-opus-4-1-20250805": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-41-prod"
  }
}
```

當使用者在 `/model` 中選取其中一個版本時，Claude Code 會使用對應的 ARN 呼叫 Bedrock。沒有覆寫的版本會回退到內建的 Bedrock 模型 ID 或在啟動時發現的任何相符推論設定檔。請參閱[覆寫每個版本的模型 ID](/zh-TW/model-config#override-model-ids-per-version)，以了解覆寫如何與 `availableModels` 和其他模型設定互動的詳細資訊。

## 啟動模型檢查

當 Claude Code 以 Bedrock 設定啟動時，它會驗證它打算使用的模型在您的帳戶中是否可存取。此檢查需要 Claude Code v2.1.94 或更新版本。

如果您已固定的模型版本比目前 Claude Code 預設值更舊，且您的帳戶可以叫用較新版本，Claude Code 會提示您更新固定。接受會將新模型 ID 寫入您的[使用者設定檔](/zh-TW/settings)並重新啟動 Claude Code。拒絕會被記住，直到下一次預設版本變更。指向[應用程式推論設定檔 ARN](#map-each-model-version-to-an-inference-profile) 的固定會被跳過，因為這些由您的管理員管理。

如果您尚未固定模型且目前預設值在您的帳戶中不可用，Claude Code 會在目前工作階段中回退到先前版本並顯示通知。回退不會被保留。在您的 Bedrock 帳戶中啟用較新模型或[固定版本](#4-pin-model-versions)以使選擇永久化。

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

Claude Opus 4.7、Opus 4.6 和 Sonnet 4.6 在 Amazon Bedrock 上支援 [1M 權杖內容視窗](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window)。當您選取 1M 模型變體時，Claude Code 會自動啟用擴展內容視窗。

[設定精靈](#sign-in-with-bedrock)在固定模型時提供 1M 內容選項。若要為手動固定的模型啟用它，請在模型 ID 後附加 `[1m]`。請參閱[為第三方部署固定模型](/zh-TW/model-config#pin-models-for-third-party-deployments)以取得詳細資訊。

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

## 使用 Mantle 端點

Mantle 是一個 Amazon Bedrock 端點，透過原生 Anthropic API 形狀而不是 Bedrock Invoke API 提供 Claude 模型。它使用相同的 AWS 認證、IAM 權限和本頁面前面所述的 `awsAuthRefresh` 設定。

<Note>
  Mantle 需要 Claude Code v2.1.94 或更新版本。執行 `claude --version` 以檢查。
</Note>

### 啟用 Mantle

已設定 AWS 認證後，設定 `CLAUDE_CODE_USE_MANTLE` 以將請求路由到 Mantle 端點：

```bash theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export AWS_REGION=us-east-1
```

Claude Code 從 `AWS_REGION` 構造端點 URL。若要為自訂端點或閘道覆寫它，請設定 `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`。

在 Claude Code 內執行 `/status` 以確認。當 Mantle 處於作用中時，提供者行會顯示 `Amazon Bedrock (Mantle)`。

### 選取 Mantle 模型

Mantle 使用以 `anthropic.` 為前綴且沒有版本尾碼的模型 ID，例如 `anthropic.claude-haiku-4-5`。您的帳戶可用的模型取決於您的組織已被授予的內容；其他模型 ID 列在來自 AWS 的您的上線材料中。請聯絡您的 AWS 帳戶團隊以要求存取允許清單模型。

使用 `--model` 旗標或 Claude Code 內的 `/model` 設定模型：

```bash theme={null}
claude --model anthropic.claude-haiku-4-5
```

### 與 Invoke API 並行執行 Mantle

您在 Mantle 上可用的模型可能不包括您今天使用的每個模型。設定 `CLAUDE_CODE_USE_BEDROCK` 和 `CLAUDE_CODE_USE_MANTLE` 可讓 Claude Code 從同一工作階段呼叫兩個端點。符合 Mantle 格式的模型 ID 會路由到 Mantle，所有其他模型 ID 會進入 Bedrock Invoke API。

```bash theme={null}
export CLAUDE_CODE_USE_BEDROCK=1
export CLAUDE_CODE_USE_MANTLE=1
```

若要在 `/model` 選擇器中顯示 Mantle 模型，請在[設定檔](/zh-TW/settings)中的 `availableModels` 中列出其 ID。此設定也會將選擇器限制為列出的項目，因此請包括您想保持可用的每個別名：

```json theme={null}
{
  "availableModels": ["opus", "sonnet", "haiku", "anthropic.claude-haiku-4-5"]
}
```

帶有 `anthropic.` 前綴的項目會新增為自訂選擇器選項並路由到 Mantle。將 `anthropic.claude-haiku-4-5` 替換為您的帳戶已被授予的模型 ID。請參閱[限制模型選擇](/zh-TW/model-config#restrict-model-selection)以了解 `availableModels` 如何與其他模型設定互動。

當兩個提供者都處於作用中時，`/status` 會顯示 `Amazon Bedrock + Amazon Bedrock (Mantle)`。

### 透過閘道路由 Mantle

如果您的組織透過集中式 [LLM 閘道](/zh-TW/llm-gateway)路由模型流量，該閘道在伺服器端注入 AWS 認證，請停用用戶端驗證，以便 Claude Code 傳送沒有 SigV4 簽名或 `x-api-key` 標頭的請求：

```bash theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export CLAUDE_CODE_SKIP_MANTLE_AUTH=1
export ANTHROPIC_BEDROCK_MANTLE_BASE_URL=https://your-gateway.example.com
```

### Mantle 環境變數

這些變數特定於 Mantle 端點。請參閱[環境變數](/zh-TW/env-vars)以取得完整清單。

| 變數                                      | 目的                                 |
| :-------------------------------------- | :--------------------------------- |
| `CLAUDE_CODE_USE_MANTLE`                | 啟用 Mantle 端點。設定為 `1` 或 `true`。     |
| `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`     | 覆寫預設 Mantle 端點 URL                 |
| `CLAUDE_CODE_SKIP_MANTLE_AUTH`          | 跳過用戶端驗證以進行代理設定                     |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` | 覆寫 Haiku 級模型的 AWS 區域（與 Bedrock 共用） |

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

### Mantle 端點錯誤

如果在設定 `CLAUDE_CODE_USE_MANTLE` 後 `/status` 未顯示 `Amazon Bedrock (Mantle)`，則該變數未到達程序。確認它已在您啟動 `claude` 的 shell 中匯出，或在[設定檔](/zh-TW/settings)的 `env` 區塊中設定它。

來自 Mantle 端點的 `403`（具有有效認證）表示您的 AWS 帳戶尚未被授予存取您要求的模型的權限。請聯絡您的 AWS 帳戶團隊以要求存取。

命名模型 ID 的 `400` 表示該模型未在 Mantle 上提供。Mantle 有其自己的模型陣容，與標準 Bedrock 目錄分開，因此推論設定檔 ID（例如 `us.anthropic.claude-sonnet-4-6`）將無法運作。使用 Mantle 格式的 ID，或啟用[兩個端點](#run-mantle-alongside-the-invoke-api)，以便 Claude Code 將每個請求路由到模型可用的端點。

## 其他資源

* [Bedrock 文件](https://docs.aws.amazon.com/bedrock/)
* [Bedrock 定價](https://aws.amazon.com/bedrock/pricing/)
* [Bedrock 推論設定檔](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Bedrock 權杖燃盡和配額](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas-token-burndown.html)
* [Amazon Bedrock 上的 Claude Code：快速設定指南](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)
* [Claude Code 監控實施 (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)
