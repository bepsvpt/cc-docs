> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Google Vertex AI 上的 Claude Code

> 了解如何通过 Google Vertex AI 配置 Claude Code，包括设置、IAM 配置和故障排除。

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

## 前置条件

在使用 Vertex AI 配置 Claude Code 之前，请确保您拥有：

* 启用了计费的 Google Cloud Platform (GCP) 账户
* 启用了 Vertex AI API 的 GCP 项目
* 对所需 Claude 模型的访问权限（例如，Claude Sonnet 4.6）
* 已安装并配置的 Google Cloud SDK (`gcloud`)
* 在所需 GCP 区域中分配的配额

要使用您自己的 Vertex AI 凭证登录，请按照下面的[使用 Vertex AI 登录](#sign-in-with-vertex-ai)进行操作。要在团队中部署 Claude Code，请使用[手动设置](#set-up-manually)步骤并在推出前[固定您的模型版本](#5-pin-model-versions)。

## 使用 Vertex AI 登录

如果您拥有 Google Cloud 凭证并想开始通过 Vertex AI 使用 Claude Code，登录向导会引导您完成整个过程。您需要在每个项目中完成一次 GCP 端的前置条件；向导会处理 Claude Code 端的事务。

<Note>
  Vertex AI 设置向导需要 Claude Code v2.1.98 或更高版本。运行 `claude --version` 来检查。
</Note>

<Steps>
  <Step title="在您的 GCP 项目中启用 Claude 模型">
    为您的项目[启用 Vertex AI API](#1-enable-vertex-ai-api)，然后在 [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) 中请求访问您想要的 Claude 模型。有关您的账户需要的权限，请参阅 [IAM 配置](#iam-configuration)。
  </Step>

  <Step title="启动 Claude Code 并选择 Vertex AI">
    运行 `claude`。在登录提示处，选择 **3rd-party platform**，然后选择 **Google Vertex AI**。
  </Step>

  <Step title="按照向导提示进行操作">
    选择您如何向 Google Cloud 进行身份验证：来自 `gcloud` 的应用默认凭证、服务账户密钥文件或已在您的环境中的凭证。向导会检测您的项目和区域，验证您的项目可以调用哪些 Claude 模型，并让您固定它们。它将结果保存到您的[用户设置文件](/zh-CN/settings)的 `env` 块中，因此您无需自己导出环境变量。
  </Step>
</Steps>

登录后，您可以随时运行 `/setup-vertex` 来重新打开向导并更改您的凭证、项目、区域或模型固定。

## 区域配置

Claude Code 支持 Vertex AI [全局](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai)、多区域和区域端点。将 `CLOUD_ML_REGION` 设置为 `global`、多区域位置（如 `eu` 或 `us`）或特定区域（如 `us-east5`）。Claude Code 为每种形式选择正确的 Vertex AI 主机名，包括多区域位置的 `aiplatform.eu.rep.googleapis.com` 和 `aiplatform.us.rep.googleapis.com` 主机。

<Note>
  Vertex AI 可能不支持 Claude Code 默认模型在每个端点类型上。模型可用性在[特定区域](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models)、多区域位置和[全局端点](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models)之间有所不同。您可能需要切换到支持的位置或指定支持的模型。
</Note>

## 手动设置

要通过环境变量而不是向导配置 Vertex AI，例如在 CI 或脚本化企业推出中，请按照下面的步骤进行。

### 1. 启用 Vertex AI API

在您的 GCP 项目中启用 Vertex AI API：

```bash theme={null}
# 设置您的项目 ID
gcloud config set project YOUR-PROJECT-ID

# 启用 Vertex AI API
gcloud services enable aiplatform.googleapis.com
```

### 2. 请求模型访问权限

请求访问 Vertex AI 中的 Claude 模型：

1. 导航到 [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. 搜索"Claude"模型
3. 请求访问所需的 Claude 模型（例如，Claude Sonnet 4.6）
4. 等待批准（可能需要 24-48 小时）

### 3. 配置 GCP 凭证

Claude Code 使用标准的 Google Cloud 身份验证。

有关更多信息，请参阅 [Google Cloud 身份验证文档](https://cloud.google.com/docs/authentication)。

Claude Code v2.1.121 或更高版本通过相同的应用默认凭证链支持[基于 X.509 证书的工作负载身份联合](https://cloud.google.com/iam/docs/workload-identity-federation-with-x509-certificates)。将 `GOOGLE_APPLICATION_CREDENTIALS` 设置为您的凭证配置文件的路径。

<Note>
  进行身份验证时，Claude Code 将自动使用 `ANTHROPIC_VERTEX_PROJECT_ID` 环境变量中的项目 ID。要覆盖此设置，请设置以下环境变量之一：`GCLOUD_PROJECT`、`GOOGLE_CLOUD_PROJECT` 或 `GOOGLE_APPLICATION_CREDENTIALS`。
</Note>

### 4. 配置 Claude Code

设置以下环境变量：

```bash theme={null}
# 启用 Vertex AI 集成
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# 可选：为自定义端点或网关覆盖 Vertex 端点 URL
# export ANTHROPIC_VERTEX_BASE_URL=https://aiplatform.googleapis.com

# 可选：如果需要，禁用 prompt caching
export DISABLE_PROMPT_CACHING=1

# 可选：请求 1 小时的 prompt cache TTL 而不是 5 分钟的默认值
export ENABLE_PROMPT_CACHING_1H=1

# 当 CLOUD_ML_REGION=global 时，为不支持全局端点的模型覆盖区域
export VERTEX_REGION_CLAUDE_HAIKU_4_5=us-east5
export VERTEX_REGION_CLAUDE_4_6_SONNET=europe-west1
```

大多数模型版本都有对应的 `VERTEX_REGION_CLAUDE_*` 变量。有关完整列表，请参阅[环境变量参考](/zh-CN/env-vars)。检查 [Vertex Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) 以确定哪些模型支持全局端点与仅区域端点。

[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) 会自动启用。要禁用它，请设置 `DISABLE_PROMPT_CACHING=1`。要请求 1 小时的缓存 TTL 而不是 5 分钟的默认值，请设置 `ENABLE_PROMPT_CACHING_1H=1`；具有 1 小时 TTL 的缓存写入按更高费率计费。如需提高速率限制，请联系 Google Cloud 支持。使用 Vertex AI 时，`/login` 和 `/logout` 命令被禁用，因为身份验证通过 Google Cloud 凭证处理。

[MCP tool search](/zh-CN/mcp#scale-with-mcp-tool-search) 在 Vertex AI 上默认被禁用，因为端点不接受所需的 beta 标头。所有 MCP 工具定义会预先加载。要选择加入，请设置 `ENABLE_TOOL_SEARCH=true`。

### 5. 固定模型版本

<Warning>
  在部署到多个用户时固定特定的模型版本。如果不固定，模型别名（如 `sonnet` 和 `opus`）会解析为最新版本，当 Anthropic 发布更新时，该版本可能尚未在您的 Vertex AI 项目中启用。Claude Code 在启动时当最新版本不可用时会[回退](#startup-model-checks)到之前的版本，但固定让您可以控制用户何时迁移到新模型。
</Warning>

将这些环境变量设置为特定的 Vertex AI 模型 ID。

如果没有 `ANTHROPIC_DEFAULT_OPUS_MODEL`，Vertex 上的 `opus` 别名会解析为 Opus 4.6。将其设置为 Opus 4.7 ID 以使用最新模型：

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

有关当前和旧版模型 ID，请参阅[模型概览](https://platform.claude.com/docs/en/about-claude/models/overview)。有关完整的环境变量列表，请参阅[模型配置](/zh-CN/model-config#pin-models-for-third-party-deployments)。

Claude Code 在未设置固定变量时使用这些默认模型：

| 模型类型    | 默认值                          |
| :------ | :--------------------------- |
| 主模型     | `claude-sonnet-4-5@20250929` |
| 小型/快速模型 | `claude-haiku-4-5@20251001`  |

要进一步自定义模型：

```bash theme={null}
export ANTHROPIC_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

## 启动模型检查

当 Claude Code 启动并配置了 Vertex AI 时，它会验证它打算使用的模型在您的项目中是否可访问。此检查需要 Claude Code v2.1.98 或更高版本。

如果您固定了一个比当前 Claude Code 默认值更旧的模型版本，并且您的项目可以调用较新版本，Claude Code 会提示您更新固定。接受会将新的模型 ID 写入您的[用户设置文件](/zh-CN/settings)并重启 Claude Code。拒绝会被记住，直到下一个默认版本更改。

如果您没有固定模型，并且当前默认值在您的项目中不可用，Claude Code 会在当前会话中回退到之前的版本并显示通知。回退不会被持久化。在 [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) 中启用较新的模型或[固定一个版本](#5-pin-model-versions)以使选择永久化。

## IAM 配置

分配所需的 IAM 权限：

`roles/aiplatform.user` 角色包括所需的权限：

* `aiplatform.endpoints.predict` - 模型调用和令牌计数所需

对于更严格的权限，请创建仅包含上述权限的自定义角色。

有关详细信息，请参阅 [Vertex IAM 文档](https://cloud.google.com/vertex-ai/docs/general/access-control)。

<Note>
  为 Claude Code 创建专用的 GCP 项目，以简化成本跟踪和访问控制。
</Note>

## 1M token context window

Claude Opus 4.7、Opus 4.6 和 Sonnet 4.6 在 Vertex AI 上支持 [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window)。当您选择 1M 模型变体时，Claude Code 会自动启用扩展 context window。

[设置向导](#sign-in-with-vertex-ai)在固定模型时提供 1M context 选项。要为手动固定的模型启用它，请在模型 ID 后附加 `[1m]`。有关详细信息，请参阅[为第三方部署固定模型](/zh-CN/model-config#pin-models-for-third-party-deployments)。

## 故障排除

如果您遇到配额问题：

* 通过 [Cloud Console](https://cloud.google.com/docs/quotas/view-manage) 检查当前配额或请求增加配额

如果您遇到"模型未找到"404 错误：

* 确认模型在 [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) 中已启用
* 验证该模型在您指定的位置可用。某些模型仅在 `global` 或多区域位置（如 `eu` 和 `us`）上提供，而不是在特定区域
* 如果使用 `CLOUD_ML_REGION=global`，请检查您的模型是否在 [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) 中的"支持的功能"下支持全局端点。对于不支持全局端点的模型，请执行以下任一操作：
  * 通过 `ANTHROPIC_MODEL` 或 `ANTHROPIC_DEFAULT_HAIKU_MODEL` 指定支持的模型，或
  * 使用 `VERTEX_REGION_<MODEL_NAME>` 环境变量设置区域或多区域位置

如果您遇到 429 错误：

* 对于区域端点，请确保主模型和小型/快速模型在您选择的区域中受支持
* 考虑切换到 `CLOUD_ML_REGION=global` 以获得更好的可用性

## 其他资源

* [Vertex AI 文档](https://cloud.google.com/vertex-ai/docs)
* [Vertex AI 定价](https://cloud.google.com/vertex-ai/pricing)
* [Vertex AI 配额和限制](https://cloud.google.com/vertex-ai/docs/quotas)
