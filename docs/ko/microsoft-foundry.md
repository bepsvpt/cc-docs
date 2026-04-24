> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Microsoft Foundry의 Claude Code

> 설정, 구성 및 문제 해결을 포함하여 Microsoft Foundry를 통해 Claude Code를 구성하는 방법을 알아봅니다.

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

<Experiment flag="docs-contact-sales-cta" treatment={<ContactSalesCard surface="foundry" />} />

## 필수 조건

Microsoft Foundry로 Claude Code를 구성하기 전에 다음을 확인하세요:

* Microsoft Foundry에 액세스할 수 있는 Azure 구독
* Microsoft Foundry 리소스 및 배포를 만들 수 있는 RBAC 권한
* Azure CLI 설치 및 구성(선택 사항 - 자격 증명을 얻을 다른 메커니즘이 없는 경우에만 필요)

<Note>
  Claude Code를 여러 사용자에게 배포하는 경우 Anthropic이 새 모델을 출시할 때 중단을 방지하기 위해 [모델 버전을 고정](#4-pin-model-versions)하세요.
</Note>

## 설정

### 1. Microsoft Foundry 리소스 프로비저닝

먼저 Azure에서 Claude 리소스를 만듭니다:

1. [Microsoft Foundry 포털](https://ai.azure.com/)로 이동합니다
2. 새 리소스를 만들고 리소스 이름을 기록합니다
3. Claude 모델에 대한 배포를 만듭니다:
   * Claude Opus
   * Claude Sonnet
   * Claude Haiku

### 2. Azure 자격 증명 구성

Claude Code는 Microsoft Foundry에 대해 두 가지 인증 방법을 지원합니다. 보안 요구 사항에 가장 적합한 방법을 선택하세요.

**옵션 A: API 키 인증**

1. Microsoft Foundry 포털에서 리소스로 이동합니다
2. **엔드포인트 및 키** 섹션으로 이동합니다
3. **API 키**를 복사합니다
4. 환경 변수를 설정합니다:

```bash theme={null}
export ANTHROPIC_FOUNDRY_API_KEY=your-azure-api-key
```

**옵션 B: Microsoft Entra ID 인증**

`ANTHROPIC_FOUNDRY_API_KEY`가 설정되지 않으면 Claude Code는 자동으로 Azure SDK [기본 자격 증명 체인](https://learn.microsoft.com/en-us/azure/developer/javascript/sdk/authentication/credential-chains#defaultazurecredential-overview)을 사용합니다.
이는 로컬 및 원격 워크로드를 인증하기 위한 다양한 방법을 지원합니다.

로컬 환경에서는 일반적으로 Azure CLI를 사용할 수 있습니다:

```bash theme={null}
az login
```

<Note>
  Microsoft Foundry를 사용할 때 `/login` 및 `/logout` 명령은 Azure 자격 증명을 통해 인증이 처리되므로 비활성화됩니다.
</Note>

### 3. Claude Code 구성

Microsoft Foundry를 활성화하려면 다음 환경 변수를 설정합니다:

```bash theme={null}
# Microsoft Foundry 통합 활성화
export CLAUDE_CODE_USE_FOUNDRY=1

# Azure 리소스 이름 ({resource}를 리소스 이름으로 바꾸기)
export ANTHROPIC_FOUNDRY_RESOURCE={resource}
# 또는 전체 기본 URL 제공:
# export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com/anthropic
```

### 4. 모델 버전 고정

<Warning>
  모든 배포에 대해 특정 모델 버전을 고정합니다. 고정하지 않고 모델 별칭(`sonnet`, `opus`, `haiku`)을 사용하면 Claude Code가 Foundry 계정에서 사용할 수 없는 최신 모델 버전을 사용하려고 시도하여 Anthropic이 업데이트를 출시할 때 기존 사용자가 중단될 수 있습니다. Azure 배포를 만들 때 "최신으로 자동 업데이트" 대신 특정 모델 버전을 선택합니다.
</Warning>

모델 변수를 1단계에서 만든 배포 이름과 일치하도록 설정합니다.

`ANTHROPIC_DEFAULT_OPUS_MODEL`이 없으면 Foundry의 `opus` 별칭은 Opus 4.6으로 확인됩니다. 최신 모델을 사용하려면 Opus 4.7 ID로 설정합니다:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5'
```

현재 및 레거시 모델 ID는 [모델 개요](https://platform.claude.com/docs/en/about-claude/models/overview)를 참조하세요. 전체 환경 변수 목록은 [모델 구성](/ko/model-config#pin-models-for-third-party-deployments)을 참조하세요.

[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)은 자동으로 활성화됩니다. 기본 5분 대신 1시간 캐시 TTL을 요청하려면 다음 변수를 설정합니다. 1시간 TTL로 캐시 쓰기는 더 높은 요금으로 청구됩니다:

```bash theme={null}
export ENABLE_PROMPT_CACHING_1H=1
```

## Azure RBAC 구성

`Azure AI User` 및 `Cognitive Services User` 기본 역할에는 Claude 모델을 호출하는 데 필요한 모든 권한이 포함됩니다.

더 제한적인 권한의 경우 다음을 포함하는 사용자 지정 역할을 만듭니다:

```json theme={null}
{
  "permissions": [
    {
      "dataActions": [
        "Microsoft.CognitiveServices/accounts/providers/*"
      ]
    }
  ]
}
```

자세한 내용은 [Microsoft Foundry RBAC 설명서](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry)를 참조하세요.

## 문제 해결

"Failed to get token from azureADTokenProvider: ChainedTokenCredential authentication failed" 오류가 발생하면:

* 환경에서 Entra ID를 구성하거나 `ANTHROPIC_FOUNDRY_API_KEY`를 설정합니다.

## 추가 리소스

* [Microsoft Foundry 설명서](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)
* [Microsoft Foundry 모델](https://ai.azure.com/explore/models)
* [Microsoft Foundry 가격](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/)
