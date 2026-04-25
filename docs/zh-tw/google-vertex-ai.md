> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Google Vertex AI 上的 Claude Code

> 了解如何透過 Google Vertex AI 設定 Claude Code，包括設定、IAM 設定和故障排除。

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

<Experiment flag="docs-contact-sales-cta" treatment={<ContactSalesCard surface="vertex" />} />

## 先決條件

在使用 Vertex AI 設定 Claude Code 之前，請確保您具有：

* 已啟用計費的 Google Cloud Platform (GCP) 帳戶
* 已啟用 Vertex AI API 的 GCP 專案
* 存取所需的 Claude 模型（例如 Claude Sonnet 4.6）
* 已安裝並設定 Google Cloud SDK (`gcloud`)
* 在所需的 GCP 區域中分配的配額

若要使用您自己的 Vertex AI 認證登入，請遵循下方的[使用 Vertex AI 登入](#sign-in-with-vertex-ai)。若要在整個團隊中部署 Claude Code，請使用[手動設定](#set-up-manually)步驟並在推出前[固定您的模型版本](#5-pin-model-versions)。

## 使用 Vertex AI 登入

如果您有 Google Cloud 認證並想開始透過 Vertex AI 使用 Claude Code，登入精靈會引導您完成整個過程。您只需在每個專案中完成一次 GCP 端的先決條件；精靈會處理 Claude Code 端的設定。

<Note>
  Vertex AI 設定精靈需要 Claude Code v2.1.98 或更新版本。執行 `claude --version` 以檢查。
</Note>

<Steps>
  <Step title="在您的 GCP 專案中啟用 Claude 模型">
    為您的專案[啟用 Vertex AI API](#1-enable-vertex-ai-api)，然後在 [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) 中要求存取您想要的 Claude 模型。請參閱 [IAM 設定](#iam-configuration)以了解您的帳戶需要的權限。
  </Step>

  <Step title="啟動 Claude Code 並選擇 Vertex AI">
    執行 `claude`。在登入提示處，選擇**第三方平台**，然後選擇 **Google Vertex AI**。
  </Step>

  <Step title="遵循精靈提示">
    選擇您如何向 Google Cloud 進行驗證：來自 `gcloud` 的應用程式預設認證、服務帳戶金鑰檔案，或已在您的環境中的認證。精靈會偵測您的專案和區域，驗證您的專案可以呼叫哪些 Claude 模型，並讓您固定它們。它會將結果儲存到您的[使用者設定檔](/zh-TW/settings)的 `env` 區塊，因此您不需要自己匯出環境變數。
  </Step>
</Steps>

登入後，您可以隨時執行 `/setup-vertex` 以重新開啟精靈並變更您的認證、專案、區域或模型固定。

## 區域設定

Claude Code 支援 Vertex AI [全球](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai)、多區域和區域端點。將 `CLOUD_ML_REGION` 設定為 `global`、多區域位置（例如 `eu` 或 `us`）或特定區域（例如 `us-east5`）。Claude Code 為每種形式選擇正確的 Vertex AI 主機名稱，包括多區域位置的 `aiplatform.eu.rep.googleapis.com` 和 `aiplatform.us.rep.googleapis.com` 主機。

<Note>
  Vertex AI 可能不支援每個端點類型上的 Claude Code 預設模型。模型可用性在[特定區域](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models)、多區域位置和[全球端點](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models)之間有所不同。您可能需要切換到支援的位置或指定支援的模型。
</Note>

## 手動設定

若要透過環境變數而不是精靈來設定 Vertex AI，例如在 CI 或指令碼化企業推出中，請遵循下列步驟。

### 1. 啟用 Vertex AI API

在您的 GCP 專案中啟用 Vertex AI API：

```bash theme={null}
# 設定您的專案 ID
gcloud config set project YOUR-PROJECT-ID

# 啟用 Vertex AI API
gcloud services enable aiplatform.googleapis.com
```

### 2. 要求模型存取

在 Vertex AI 中要求存取 Claude 模型：

1. 導覽至 [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. 搜尋「Claude」模型
3. 要求存取所需的 Claude 模型（例如 Claude Sonnet 4.6）
4. 等待核准（可能需要 24-48 小時）

### 3. 設定 GCP 認證

Claude Code 使用標準的 Google Cloud 驗證。

如需詳細資訊，請參閱 [Google Cloud 驗證文件](https://cloud.google.com/docs/authentication)。

<Note>
  進行驗證時，Claude Code 將自動使用 `ANTHROPIC_VERTEX_PROJECT_ID` 環境變數中的專案 ID。若要覆寫此設定，請設定下列其中一個環境變數：`GCLOUD_PROJECT`、`GOOGLE_CLOUD_PROJECT` 或 `GOOGLE_APPLICATION_CREDENTIALS`。
</Note>

### 4. 設定 Claude Code

設定下列環境變數：

```bash theme={null}
# 啟用 Vertex AI 整合
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# 選用：覆寫 Vertex 端點 URL 以用於自訂端點或閘道
# export ANTHROPIC_VERTEX_BASE_URL=https://aiplatform.googleapis.com

# 選用：如需要，停用 prompt caching
export DISABLE_PROMPT_CACHING=1

# 選用：要求 1 小時 prompt cache TTL 而不是 5 分鐘預設值
export ENABLE_PROMPT_CACHING_1H=1

# 當 CLOUD_ML_REGION=global 時，覆寫不支援全球端點的模型的區域
export VERTEX_REGION_CLAUDE_HAIKU_4_5=us-east5
export VERTEX_REGION_CLAUDE_4_6_SONNET=europe-west1
```

大多數模型版本都有對應的 `VERTEX_REGION_CLAUDE_*` 變數。如需完整清單，請參閱[環境變數參考](/zh-TW/env-vars)。檢查 [Vertex Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) 以確定哪些模型支援全球端點與僅限區域端點。

[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) 會自動啟用。若要停用它，請設定 `DISABLE_PROMPT_CACHING=1`。若要要求 1 小時 cache TTL 而不是 5 分鐘預設值，請設定 `ENABLE_PROMPT_CACHING_1H=1`；具有 1 小時 TTL 的 cache 寫入會以更高費率計費。如需提高速率限制，請聯絡 Google Cloud 支援。使用 Vertex AI 時，`/login` 和 `/logout` 命令會被停用，因為驗證是透過 Google Cloud 認證處理的。

[MCP tool search](/zh-TW/mcp#scale-with-mcp-tool-search) 在 Vertex AI 上預設為停用，因為端點不接受所需的 beta 標頭。所有 MCP 工具定義會改為預先載入。若要選擇加入，請設定 `ENABLE_TOOL_SEARCH=true`。

### 5. 固定模型版本

<Warning>
  在部署到多個使用者時固定特定模型版本。如果不固定，模型別名（例如 `sonnet` 和 `opus`）會解析為最新版本，當 Anthropic 發佈更新時，該版本可能尚未在您的 Vertex AI 專案中啟用。Claude Code 在啟動時會在最新版本無法使用時[回退](#startup-model-checks)到先前版本，但固定可讓您控制使用者何時移至新模型。
</Warning>

將這些環境變數設定為特定的 Vertex AI 模型 ID。

如果沒有 `ANTHROPIC_DEFAULT_OPUS_MODEL`，Vertex 上的 `opus` 別名會解析為 Opus 4.6。將其設定為 Opus 4.7 ID 以使用最新模型：

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

如需目前和舊版模型 ID，請參閱[模型概覽](https://platform.claude.com/docs/en/about-claude/models/overview)。如需完整的環境變數清單，請參閱[模型設定](/zh-TW/model-config#pin-models-for-third-party-deployments)。

未設定固定變數時，Claude Code 使用這些預設模型：

| 模型類型    | 預設值                          |
| :------ | :--------------------------- |
| 主要模型    | `claude-sonnet-4-5@20250929` |
| 小型/快速模型 | `claude-haiku-4-5@20251001`  |

若要進一步自訂模型：

```bash theme={null}
export ANTHROPIC_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

## 啟動模型檢查

當 Claude Code 以設定的 Vertex AI 啟動時，它會驗證它打算使用的模型在您的專案中是否可存取。此檢查需要 Claude Code v2.1.98 或更新版本。

如果您已固定的模型版本比目前 Claude Code 預設值更舊，且您的專案可以呼叫較新版本，Claude Code 會提示您更新固定。接受會將新模型 ID 寫入您的[使用者設定檔](/zh-TW/settings)並重新啟動 Claude Code。拒絕會被記住，直到下一次預設版本變更。

如果您尚未固定模型，且目前預設值在您的專案中無法使用，Claude Code 會在目前工作階段中回退到先前版本並顯示通知。回退不會被保留。在 [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) 中啟用較新模型或[固定版本](#5-pin-model-versions)以使選擇永久化。

## IAM 設定

指派所需的 IAM 權限：

`roles/aiplatform.user` 角色包含所需的權限：

* `aiplatform.endpoints.predict` - 模型呼叫和權杖計數所需

如需更嚴格的權限，請建立只包含上述權限的自訂角色。

如需詳細資訊，請參閱 [Vertex IAM 文件](https://cloud.google.com/vertex-ai/docs/general/access-control)。

<Note>
  為 Claude Code 建立專用的 GCP 專案，以簡化成本追蹤和存取控制。
</Note>

## 1M token context window

Claude Opus 4.7、Opus 4.6 和 Sonnet 4.6 在 Vertex AI 上支援 [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window)。當您選擇 1M 模型變體時，Claude Code 會自動啟用擴展 context window。

[設定精靈](#sign-in-with-vertex-ai)在固定模型時提供 1M context 選項。若要為手動固定的模型啟用它，請在模型 ID 後附加 `[1m]`。如需詳細資訊，請參閱[為第三方部署固定模型](/zh-TW/model-config#pin-models-for-third-party-deployments)。

## 故障排除

如果您遇到配額問題：

* 透過 [Cloud Console](https://cloud.google.com/docs/quotas/view-manage) 檢查目前配額或要求增加配額

如果您遇到「找不到模型」404 錯誤：

* 確認模型在 [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) 中已啟用
* 驗證模型在您指定的位置中可用。某些模型僅在 `global` 或多區域位置（例如 `eu` 和 `us`）上提供，不在特定區域中
* 如果使用 `CLOUD_ML_REGION=global`，請檢查您的模型是否在 [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) 中的「支援的功能」下支援全球端點。對於不支援全球端點的模型，請執行下列其中一項：
  * 透過 `ANTHROPIC_MODEL` 或 `ANTHROPIC_DEFAULT_HAIKU_MODEL` 指定支援的模型，或
  * 使用 `VERTEX_REGION_<MODEL_NAME>` 環境變數設定區域或多區域位置

如果您遇到 429 錯誤：

* 對於區域端點，請確保主要模型和小型/快速模型在您選擇的區域中受支援
* 考慮切換到 `CLOUD_ML_REGION=global` 以獲得更好的可用性

## 其他資源

* [Vertex AI 文件](https://cloud.google.com/vertex-ai/docs)
* [Vertex AI 定價](https://cloud.google.com/vertex-ai/pricing)
* [Vertex AI 配額和限制](https://cloud.google.com/vertex-ai/docs/quotas)
