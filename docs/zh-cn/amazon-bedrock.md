> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Amazon Bedrock 上的 Claude Code

> 了解如何通过 Amazon Bedrock 配置 Claude Code，包括设置、IAM 配置和故障排除。

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

## 前置条件

在使用 Bedrock 配置 Claude Code 之前，请确保您拥有：

* 启用了 Bedrock 访问权限的 AWS 账户
* 在 Bedrock 中访问所需的 Claude 模型（例如 Claude Sonnet 4.6）
* 已安装并配置 AWS CLI（可选 - 仅在您没有其他获取凭证的机制时需要）
* 适当的 IAM 权限

要使用您自己的 Bedrock 凭证登录，请按照下面的[使用 Bedrock 登录](#sign-in-with-bedrock)进行操作。要在团队中部署 Claude Code，请使用[手动设置](#set-up-manually)步骤并在推出前[固定您的模型版本](#4-pin-model-versions)。

## 使用 Bedrock 登录

如果您拥有 AWS 凭证并想开始通过 Bedrock 使用 Claude Code，登录向导会引导您完成整个过程。您每个账户完成一次 AWS 端的前置条件；向导处理 Claude Code 端。

<Steps>
  <Step title="在您的 AWS 账户中启用 Anthropic 模型">
    在 [Amazon Bedrock 控制台](https://console.aws.amazon.com/bedrock/)中，打开模型目录，选择一个 Anthropic 模型，并提交用例表单。提交后立即授予访问权限。有关 AWS Organizations，请参阅[提交用例详情](#1-submit-use-case-details)，有关权限，请参阅 [IAM 配置](#iam-configuration)。
  </Step>

  <Step title="启动 Claude Code 并选择 Bedrock">
    运行 `claude`。在登录提示处，选择 **3rd-party platform**，然后选择 **Amazon Bedrock**。
  </Step>

  <Step title="按照向导提示操作">
    选择您如何向 AWS 进行身份验证：从您的 `~/.aws` 目录检测到的 AWS 配置文件、Bedrock API 密钥、访问密钥和密钥，或已在您的环境中的凭证。向导会获取您的区域，验证您的账户可以调用哪些 Claude 模型，并让您固定它们。它将结果保存到您的[用户设置文件](/zh-CN/settings)的 `env` 块中，因此您无需自己导出环境变量。
  </Step>
</Steps>

登录后，随时运行 `/setup-bedrock` 重新打开向导并更改您的凭证、区域或模型固定。

## 手动设置

要通过环境变量而不是向导配置 Bedrock，例如在 CI 或脚本化企业推出中，请按照下面的步骤操作。

### 1. 提交用例详情

Anthropic 模型的首次用户需要在调用模型之前提交用例详情。这是每个 AWS 账户执行一次的操作。

1. 确保您拥有下面描述的正确 IAM 权限
2. 导航到 [Amazon Bedrock 控制台](https://console.aws.amazon.com/bedrock/)
3. 从**模型目录**中选择一个 Anthropic 模型
4. 完成用例表单。提交后立即授予访问权限。

如果您使用 AWS Organizations，您可以使用 [`PutUseCaseForModelAccess` API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_PutUseCaseForModelAccess.html) 从管理账户提交一次表单。此调用需要 `bedrock:PutUseCaseForModelAccess` IAM 权限。批准自动扩展到子账户。

### 2. 配置 AWS 凭证

Claude Code 使用默认的 AWS SDK 凭证链。使用以下方法之一设置您的凭证：

**选项 A：AWS CLI 配置**

```bash theme={null}
aws configure
```

**选项 B：环境变量（访问密钥）**

```bash theme={null}
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token
```

**选项 C：环境变量（SSO 配置文件）**

```bash theme={null}
aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name
```

**选项 D：AWS 管理控制台凭证**

```bash theme={null}
aws login
```

[了解更多](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html)关于 `aws login`。

**选项 E：Bedrock API 密钥**

```bash theme={null}
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

Bedrock API 密钥提供了一种更简单的身份验证方法，无需完整的 AWS 凭证。[了解更多关于 Bedrock API 密钥](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/)。

#### 高级凭证配置

Claude Code 支持 AWS SSO 和企业身份提供商的自动凭证刷新。将这些设置添加到您的 Claude Code 设置文件（请参阅[设置](/zh-CN/settings)了解文件位置）。

当 Claude Code 检测到您的 AWS 凭证已过期（基于本地时间戳或当 Bedrock 返回凭证错误时），它将自动运行您配置的 `awsAuthRefresh` 和/或 `awsCredentialExport` 命令来获取新凭证，然后重试请求。

##### 示例配置

```json theme={null}
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": {
    "AWS_PROFILE": "myprofile"
  }
}
```

##### 配置设置说明

**`awsAuthRefresh`**：用于修改 `.aws` 目录的命令，例如更新凭证、SSO 缓存或配置文件。命令的输出显示给用户，但不支持交互式输入。这适用于基于浏览器的 SSO 流，其中 CLI 显示 URL 或代码，您在浏览器中完成身份验证。

**`awsCredentialExport`**：仅在您无法修改 `.aws` 且必须直接返回凭证时使用。输出被静默捕获，不显示给用户。命令必须以此格式输出 JSON：

```json theme={null}
{
  "Credentials": {
    "AccessKeyId": "value",
    "SecretAccessKey": "value",
    "SessionToken": "value"
  }
}
```

### 3. 配置 Claude Code

设置以下环境变量以启用 Bedrock：

```bash theme={null}
# 启用 Bedrock 集成
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # 或您首选的区域

# 可选：覆盖小型/快速模型 (Haiku) 的区域。
# 也适用于 Bedrock Mantle。
export ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION=us-west-2

# 可选：覆盖 Bedrock 端点 URL 以用于自定义端点或网关
# export ANTHROPIC_BEDROCK_BASE_URL=https://bedrock-runtime.us-east-1.amazonaws.com
```

为 Claude Code 启用 Bedrock 时，请记住以下几点：

* `AWS_REGION` 是必需的环境变量。Claude Code 不会从 `.aws` 配置文件中读取此设置。
* 使用 Bedrock 时，`/login` 和 `/logout` 命令被禁用，因为身份验证通过 AWS 凭证处理。
* 您可以使用设置文件来处理环境变量，如 `AWS_PROFILE`，您不希望泄露给其他进程。请参阅[设置](/zh-CN/settings)了解更多信息。

### 4. 固定模型版本

<Warning>
  在部署到多个用户时固定特定的模型版本。如果不固定，模型别名（如 `sonnet` 和 `opus`）会解析为最新版本，当 Anthropic 发布更新时，您的 Bedrock 账户中可能还没有该版本。Claude Code 在启动时会[回退](#startup-model-checks)到上一个版本（如果最新版本不可用），但固定让您可以控制用户何时迁移到新模型。
</Warning>

将这些环境变量设置为特定的 Bedrock 模型 ID。

如果没有 `ANTHROPIC_DEFAULT_OPUS_MODEL`，Bedrock 上的 `opus` 别名会解析为 Opus 4.6。将其设置为 Opus 4.7 ID 以使用最新模型：

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
```

这些变量使用跨区域推理配置文件 ID（带有 `us.` 前缀）。如果您使用不同的区域前缀或应用推理配置文件，请相应调整。有关当前和旧版模型 ID，请参阅[模型概览](https://platform.claude.com/docs/en/about-claude/models/overview)。请参阅[模型配置](/zh-CN/model-config#pin-models-for-third-party-deployments)了解完整的环境变量列表。

当未设置固定变量时，Claude Code 使用这些默认模型：

| 模型类型    | 默认值                                            |
| :------ | :--------------------------------------------- |
| 主模型     | `us.anthropic.claude-sonnet-4-5-20250929-v1:0` |
| 小型/快速模型 | `us.anthropic.claude-haiku-4-5-20251001-v1:0`  |

要进一步自定义模型，请使用以下方法之一：

```bash theme={null}
# 使用推理配置文件 ID
export ANTHROPIC_MODEL='global.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'

# 使用应用推理配置文件 ARN
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# 可选：如果需要，禁用 prompt caching
export DISABLE_PROMPT_CACHING=1

# 可选：请求 1 小时 prompt cache TTL 而不是 5 分钟默认值
export ENABLE_PROMPT_CACHING_1H=1
```

<Note>[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) 可能在所有区域都不可用。具有 1 小时 TTL 的缓存写入的计费费率高于 5 分钟写入。</Note>

#### 将每个模型版本映射到推理配置文件

`ANTHROPIC_DEFAULT_*_MODEL` 环境变量为每个模型系列配置一个推理配置文件。如果您的组织需要在 `/model` 选择器中公开同一系列的多个版本，每个版本路由到其自己的应用推理配置文件 ARN，请改用[设置文件](/zh-CN/settings#settings-files)中的 `modelOverrides` 设置。

此示例将四个 Opus 版本映射到不同的 ARN，以便用户可以在它们之间切换，而无需绕过您组织的推理配置文件：

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

当用户在 `/model` 中选择其中一个版本时，Claude Code 使用映射的 ARN 调用 Bedrock。没有覆盖的版本回退到内置的 Bedrock 模型 ID 或启动时发现的任何匹配推理配置文件。请参阅[按版本覆盖模型 ID](/zh-CN/model-config#override-model-ids-per-version)了解覆盖如何与 `availableModels` 和其他模型设置交互的详情。

## 启动模型检查

当 Claude Code 启动并配置了 Bedrock 时，它会验证它打算使用的模型在您的账户中是否可访问。此检查需要 Claude Code v2.1.94 或更高版本。

如果您固定了一个比当前 Claude Code 默认值更旧的模型版本，并且您的账户可以调用较新版本，Claude Code 会提示您更新固定。接受会将新模型 ID 写入您的[用户设置文件](/zh-CN/settings)并重启 Claude Code。拒绝会被记住，直到下一个默认版本更改。指向[应用推理配置文件 ARN](#map-each-model-version-to-an-inference-profile) 的固定会被跳过，因为这些由您的管理员管理。

如果您没有固定模型，并且当前默认值在您的账户中不可用，Claude Code 会在当前会话中回退到上一个版本并显示通知。回退不会被持久化。在您的 Bedrock 账户中启用较新的模型或[固定一个版本](#4-pin-model-versions)以使选择永久化。

## IAM 配置

创建具有 Claude Code 所需权限的 IAM 策略：

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

为了获得更严格的权限，您可以将资源限制为特定的推理配置文件 ARN。

有关详情，请参阅 [Bedrock IAM 文档](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html)。

<Note>
  为 Claude Code 创建一个专用的 AWS 账户，以简化成本跟踪和访问控制。
</Note>

## 1M 令牌上下文窗口

Claude Opus 4.7、Opus 4.6 和 Sonnet 4.6 在 Amazon Bedrock 上支持 [1M 令牌上下文窗口](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window)。当您选择 1M 模型变体时，Claude Code 会自动启用扩展上下文窗口。

[设置向导](#sign-in-with-bedrock)在固定模型时提供 1M 上下文选项。要为手动固定的模型启用它，请在模型 ID 后附加 `[1m]`。请参阅[为第三方部署固定模型](/zh-CN/model-config#pin-models-for-third-party-deployments)了解详情。

## AWS Guardrails

[Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) 让您为 Claude Code 实现内容过滤。在 [Amazon Bedrock 控制台](https://console.aws.amazon.com/bedrock/)中创建 Guardrail，发布一个版本，然后将 Guardrail 标头添加到您的[设置文件](/zh-CN/settings)。如果您使用跨区域推理配置文件，请在您的 Guardrail 上启用跨区域推理。

示例配置：

```json theme={null}
{
  "env": {
    "ANTHROPIC_CUSTOM_HEADERS": "X-Amzn-Bedrock-GuardrailIdentifier: your-guardrail-id\nX-Amzn-Bedrock-GuardrailVersion: 1"
  }
}
```

## 使用 Mantle 端点

Mantle 是一个 Amazon Bedrock 端点，通过原生 Anthropic API 形状而不是 Bedrock Invoke API 提供 Claude 模型。它使用相同的 AWS 凭证、IAM 权限和本页面前面描述的 `awsAuthRefresh` 配置。

<Note>
  Mantle 需要 Claude Code v2.1.94 或更高版本。运行 `claude --version` 来检查。
</Note>

### 启用 Mantle

配置了 AWS 凭证后，设置 `CLAUDE_CODE_USE_MANTLE` 以将请求路由到 Mantle 端点：

```bash theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export AWS_REGION=us-east-1
```

Claude Code 从 `AWS_REGION` 构造端点 URL。要为自定义端点或网关覆盖它，请设置 `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`。

在 Claude Code 内运行 `/status` 来确认。当 Mantle 处于活动状态时，提供者行显示 `Amazon Bedrock (Mantle)`。

### 选择 Mantle 模型

Mantle 使用以 `anthropic.` 为前缀且没有版本后缀的模型 ID，例如 `anthropic.claude-haiku-4-5`。您的账户可用的模型取决于您的组织被授予的内容；其他模型 ID 列在您来自 AWS 的入职材料中。联系您的 AWS 账户团队以请求访问允许列表中的模型。

使用 `--model` 标志或在 Claude Code 内使用 `/model` 设置模型：

```bash theme={null}
claude --model anthropic.claude-haiku-4-5
```

### 在 Invoke API 旁边运行 Mantle

您在 Mantle 上可用的模型可能不包括您今天使用的每个模型。设置 `CLAUDE_CODE_USE_BEDROCK` 和 `CLAUDE_CODE_USE_MANTLE` 让 Claude Code 从同一会话调用两个端点。与 Mantle 格式匹配的模型 ID 被路由到 Mantle，所有其他模型 ID 转到 Bedrock Invoke API。

```bash theme={null}
export CLAUDE_CODE_USE_BEDROCK=1
export CLAUDE_CODE_USE_MANTLE=1
```

要在 `/model` 选择器中显示 Mantle 模型，请在您的[设置文件](/zh-CN/settings)中的 `availableModels` 中列出其 ID。此设置也将选择器限制为列出的条目，因此包括您想保持可用的每个别名：

```json theme={null}
{
  "availableModels": ["opus", "sonnet", "haiku", "anthropic.claude-haiku-4-5"]
}
```

带有 `anthropic.` 前缀的条目被添加为自定义选择器选项并路由到 Mantle。将 `anthropic.claude-haiku-4-5` 替换为您的账户被授予的模型 ID。请参阅[限制模型选择](/zh-CN/model-config#restrict-model-selection)了解 `availableModels` 如何与其他模型设置交互。

当两个提供商都处于活动状态时，`/status` 显示 `Amazon Bedrock + Amazon Bedrock (Mantle)`。

### 通过网关路由 Mantle

如果您的组织通过集中式 [LLM 网关](/zh-CN/llm-gateway)路由模型流量，该网关在服务器端注入 AWS 凭证，请禁用客户端身份验证，以便 Claude Code 发送没有 SigV4 签名或 `x-api-key` 标头的请求：

```bash theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export CLAUDE_CODE_SKIP_MANTLE_AUTH=1
export ANTHROPIC_BEDROCK_MANTLE_BASE_URL=https://your-gateway.example.com
```

### Mantle 环境变量

这些变量特定于 Mantle 端点。请参阅[环境变量](/zh-CN/env-vars)了解完整列表。

| 变量                                      | 目的                                 |
| :-------------------------------------- | :--------------------------------- |
| `CLAUDE_CODE_USE_MANTLE`                | 启用 Mantle 端点。设置为 `1` 或 `true`。     |
| `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`     | 覆盖默认 Mantle 端点 URL                 |
| `CLAUDE_CODE_SKIP_MANTLE_AUTH`          | 跳过客户端身份验证以用于代理设置                   |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` | 覆盖 Haiku 类模型的 AWS 区域（与 Bedrock 共享） |

## 故障排除

### 使用 SSO 和企业代理的身份验证循环

如果在使用 AWS SSO 时浏览器标签页反复生成，请从您的[设置文件](/zh-CN/settings)中删除 `awsAuthRefresh` 设置。这可能发生在企业 VPN 或 TLS 检查代理中断 SSO 浏览器流时。Claude Code 将中断的连接视为身份验证失败，重新运行 `awsAuthRefresh`，并无限循环。

如果您的网络环境干扰自动基于浏览器的 SSO 流，请在启动 Claude Code 之前手动使用 `aws sso login`，而不是依赖 `awsAuthRefresh`。

### 区域问题

如果您遇到区域问题：

* 检查模型可用性：`aws bedrock list-inference-profiles --region your-region`
* 切换到支持的区域：`export AWS_REGION=us-east-1`
* 考虑使用推理配置文件进行跨区域访问

如果您收到错误"不支持按需吞吐量"：

* 将模型指定为[推理配置文件](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) ID

Claude Code 使用 Bedrock [Invoke API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html)，不支持 Converse API。

### Mantle 端点错误

如果在设置 `CLAUDE_CODE_USE_MANTLE` 后 `/status` 没有显示 `Amazon Bedrock (Mantle)`，则该变量没有到达进程。确认它在您启动 `claude` 的 shell 中被导出，或在您的[设置文件](/zh-CN/settings)的 `env` 块中设置它。

来自 Mantle 端点的 `403`（具有有效凭证）意味着您的 AWS 账户没有被授予访问您请求的模型的权限。联系您的 AWS 账户团队以请求访问。

命名模型 ID 的 `400` 意味着该模型不在 Mantle 上提供。Mantle 有其自己的模型阵容，与标准 Bedrock 目录分开，因此推理配置文件 ID（如 `us.anthropic.claude-sonnet-4-6`）将不起作用。使用 Mantle 格式的 ID，或启用[两个端点](#run-mantle-alongside-the-invoke-api)，以便 Claude Code 将每个请求路由到模型可用的端点。

## 其他资源

* [Bedrock 文档](https://docs.aws.amazon.com/bedrock/)
* [Bedrock 定价](https://aws.amazon.com/bedrock/pricing/)
* [Bedrock 推理配置文件](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Bedrock 令牌消耗和配额](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas-token-burndown.html)
* [Amazon Bedrock 上的 Claude Code：快速设置指南](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)
* [Claude Code 监控实现 (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)
