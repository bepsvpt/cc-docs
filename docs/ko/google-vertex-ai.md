> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Google Vertex AI에서 Claude Code 사용하기

> Google Vertex AI를 통해 Claude Code를 구성하는 방법을 알아봅니다. 설정, IAM 구성 및 문제 해결을 포함합니다.

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

## 필수 요구사항

Vertex AI를 사용하여 Claude Code를 구성하기 전에 다음을 확인하십시오:

* 청구가 활성화된 Google Cloud Platform(GCP) 계정
* Vertex AI API가 활성화된 GCP 프로젝트
* 원하는 Claude 모델에 대한 액세스(예: Claude Sonnet 4.6)
* Google Cloud SDK(`gcloud`) 설치 및 구성
* 원하는 GCP 지역에 할당된 할당량

자신의 Vertex AI 자격증명으로 로그인하려면 아래의 [Vertex AI로 로그인](#sign-in-with-vertex-ai)을 따르십시오. 팀 전체에 Claude Code를 배포하려면 [수동 설정](#set-up-manually) 단계를 사용하고 롤아웃 전에 [모델 버전을 고정](#5-pin-model-versions)하십시오.

## Vertex AI로 로그인

Google Cloud 자격증명이 있고 Vertex AI를 통해 Claude Code 사용을 시작하려면 로그인 마법사가 이를 안내합니다. GCP 측 필수 요구사항을 프로젝트당 한 번 완료하면 마법사가 Claude Code 측을 처리합니다.

<Note>
  Vertex AI 설정 마법사는 Claude Code v2.1.98 이상이 필요합니다. `claude --version`을 실행하여 확인하십시오.
</Note>

<Steps>
  <Step title="GCP 프로젝트에서 Claude 모델 활성화">
    프로젝트에 대해 [Vertex AI API를 활성화](#1-enable-vertex-ai-api)한 다음 [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)에서 원하는 Claude 모델에 대한 액세스를 요청합니다. 계정에 필요한 권한은 [IAM 구성](#iam-configuration)을 참조하십시오.
  </Step>

  <Step title="Claude Code를 시작하고 Vertex AI 선택">
    `claude`를 실행합니다. 로그인 프롬프트에서 **3rd-party platform**을 선택한 다음 **Google Vertex AI**를 선택합니다.
  </Step>

  <Step title="마법사 프롬프트 따르기">
    Google Cloud에 인증하는 방법을 선택합니다: `gcloud`의 Application Default Credentials, 서비스 계정 키 파일 또는 환경에 이미 있는 자격증명. 마법사는 프로젝트와 지역을 감지하고, 프로젝트가 호출할 수 있는 Claude 모델을 확인하며, 이를 고정할 수 있게 합니다. 결과를 [사용자 설정 파일](/ko/settings)의 `env` 블록에 저장하므로 환경 변수를 직접 내보낼 필요가 없습니다.
  </Step>
</Steps>

로그인한 후 언제든지 `/setup-vertex`를 실행하여 마법사를 다시 열고 자격증명, 프로젝트, 지역 또는 모델 고정을 변경할 수 있습니다.

## 지역 구성

Claude Code는 Vertex AI [전역](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai), 다중 지역 및 지역 엔드포인트를 지원합니다. `CLOUD_ML_REGION`을 `global`, `eu` 또는 `us`와 같은 다중 지역 위치 또는 `us-east5`와 같은 특정 지역으로 설정합니다. Claude Code는 `aiplatform.eu.rep.googleapis.com` 및 `aiplatform.us.rep.googleapis.com` 호스트를 포함한 다중 지역 위치에 대해 각 형식에 맞는 올바른 Vertex AI 호스트명을 선택합니다.

<Note>
  Vertex AI는 모든 엔드포인트 유형에서 Claude Code 기본 모델을 지원하지 않을 수 있습니다. 모델 가용성은 [특정 지역](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models), 다중 지역 위치 및 [전역 엔드포인트](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models)에 따라 다릅니다. 지원되는 위치로 전환하거나 지원되는 모델을 지정해야 할 수 있습니다.
</Note>

## 수동 설정

마법사 대신 환경 변수를 통해 Vertex AI를 구성하려면(예: CI 또는 스크립트된 엔터프라이즈 롤아웃의 경우) 아래 단계를 따르십시오.

### 1. Vertex AI API 활성화

GCP 프로젝트에서 Vertex AI API를 활성화합니다:

```bash theme={null}
# 프로젝트 ID 설정
gcloud config set project YOUR-PROJECT-ID

# Vertex AI API 활성화
gcloud services enable aiplatform.googleapis.com
```

### 2. 모델 액세스 요청

Vertex AI에서 Claude 모델에 대한 액세스를 요청합니다:

1. [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)으로 이동합니다
2. "Claude" 모델을 검색합니다
3. 원하는 Claude 모델에 대한 액세스를 요청합니다(예: Claude Sonnet 4.6)
4. 승인을 기다립니다(24-48시간이 소요될 수 있습니다)

### 3. GCP 자격증명 구성

Claude Code는 표준 Google Cloud 인증을 사용합니다.

자세한 내용은 [Google Cloud 인증 설명서](https://cloud.google.com/docs/authentication)를 참조하십시오.

Claude Code v2.1.121 이상은 동일한 Application Default Credentials 체인을 통해 [X.509 인증서 기반 Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation-with-x509-certificates)을 지원합니다. `GOOGLE_APPLICATION_CREDENTIALS`를 자격증명 구성 파일의 경로로 설정합니다.

<Note>
  인증할 때 Claude Code는 `ANTHROPIC_VERTEX_PROJECT_ID` 환경 변수에서 프로젝트 ID를 자동으로 사용합니다. 이를 재정의하려면 다음 환경 변수 중 하나를 설정하십시오: `GCLOUD_PROJECT`, `GOOGLE_CLOUD_PROJECT` 또는 `GOOGLE_APPLICATION_CREDENTIALS`.
</Note>

### 4. Claude Code 구성

다음 환경 변수를 설정합니다:

```bash theme={null}
# Vertex AI 통합 활성화
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# 선택사항: 사용자 정의 엔드포인트 또는 게이트웨이를 위해 Vertex 엔드포인트 URL 재정의
# export ANTHROPIC_VERTEX_BASE_URL=https://aiplatform.googleapis.com

# 선택사항: 필요한 경우 prompt caching 비활성화
export DISABLE_PROMPT_CACHING=1

# 선택사항: 기본 5분 대신 1시간 prompt cache TTL 요청
export ENABLE_PROMPT_CACHING_1H=1

# CLOUD_ML_REGION=global일 때, 전역 엔드포인트를 지원하지 않는 모델의 지역 재정의
export VERTEX_REGION_CLAUDE_HAIKU_4_5=us-east5
export VERTEX_REGION_CLAUDE_4_6_SONNET=europe-west1
```

대부분의 모델 버전에는 해당하는 `VERTEX_REGION_CLAUDE_*` 변수가 있습니다. 전체 목록은 [환경 변수 참조](/ko/env-vars)를 참조하십시오. [Vertex Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)에서 어떤 모델이 전역 엔드포인트를 지원하는지 또는 지역 전용인지 확인하십시오.

[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)은 자동으로 활성화됩니다. 이를 비활성화하려면 `DISABLE_PROMPT_CACHING=1`을 설정하십시오. 기본 5분 대신 1시간 캐시 TTL을 요청하려면 `ENABLE_PROMPT_CACHING_1H=1`을 설정하십시오. 1시간 TTL을 사용한 캐시 쓰기는 더 높은 요금으로 청구됩니다. 높은 속도 제한을 위해 Google Cloud 지원팀에 문의하십시오. Vertex AI를 사용할 때 `/login` 및 `/logout` 명령은 Google Cloud 자격증명을 통해 인증이 처리되므로 비활성화됩니다.

[MCP tool search](/ko/mcp#scale-with-mcp-tool-search)는 엔드포인트가 필요한 베타 헤더를 허용하지 않으므로 Vertex AI에서 기본적으로 비활성화됩니다. 모든 MCP 도구 정의는 대신 미리 로드됩니다. 옵트인하려면 `ENABLE_TOOL_SEARCH=true`를 설정하십시오.

### 5. 모델 버전 고정

<Warning>
  여러 사용자에게 배포할 때 특정 모델 버전을 고정합니다. 고정하지 않으면 `sonnet` 및 `opus`와 같은 모델 별칭이 최신 버전으로 확인되며, Anthropic이 업데이트를 출시할 때 Vertex AI 프로젝트에서 아직 활성화되지 않았을 수 있습니다. Claude Code는 최신 버전을 사용할 수 없을 때 시작 시 [이전 버전으로 폴백](#startup-model-checks)하지만, 고정하면 사용자가 새 모델로 이동하는 시기를 제어할 수 있습니다.
</Warning>

이러한 환경 변수를 특정 Vertex AI 모델 ID로 설정합니다.

`ANTHROPIC_DEFAULT_OPUS_MODEL`이 없으면 Vertex의 `opus` 별칭이 Opus 4.6으로 확인됩니다. 최신 모델을 사용하려면 Opus 4.7 ID로 설정합니다:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

현재 및 레거시 모델 ID는 [모델 개요](https://platform.claude.com/docs/en/about-claude/models/overview)를 참조하십시오. 환경 변수의 전체 목록은 [모델 구성](/ko/model-config#pin-models-for-third-party-deployments)을 참조하십시오.

Claude Code는 고정 변수가 설정되지 않았을 때 이러한 기본 모델을 사용합니다:

| 모델 유형    | 기본값                          |
| :------- | :--------------------------- |
| 주 모델     | `claude-sonnet-4-5@20250929` |
| 소형/빠른 모델 | `claude-haiku-4-5@20251001`  |

모델을 추가로 사용자 정의하려면:

```bash theme={null}
export ANTHROPIC_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

## 시작 모델 확인

Claude Code가 Vertex AI로 구성되어 시작할 때 사용하려는 모델이 프로젝트에서 액세스 가능한지 확인합니다. 이 확인에는 Claude Code v2.1.98 이상이 필요합니다.

현재 Claude Code 기본값보다 오래된 모델 버전을 고정했고 프로젝트가 최신 버전을 호출할 수 있으면 Claude Code는 고정을 업데이트하라는 메시지를 표시합니다. 수락하면 새 모델 ID를 [사용자 설정 파일](/ko/settings)에 쓰고 Claude Code를 다시 시작합니다. 거절하면 다음 기본 버전 변경까지 기억됩니다.

모델을 고정하지 않았고 현재 기본값을 프로젝트에서 사용할 수 없으면 Claude Code는 현재 세션에 대해 이전 버전으로 폴백하고 알림을 표시합니다. 폴백은 유지되지 않습니다. [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)에서 최신 모델을 활성화하거나 [버전을 고정](#5-pin-model-versions)하여 선택을 영구적으로 만듭니다.

## IAM 구성

필요한 IAM 권한을 할당합니다:

`roles/aiplatform.user` 역할에는 필요한 권한이 포함됩니다:

* `aiplatform.endpoints.predict` - 모델 호출 및 토큰 계산에 필요

더 제한적인 권한의 경우 위의 권한만 포함하는 사용자 정의 역할을 만듭니다.

자세한 내용은 [Vertex IAM 설명서](https://cloud.google.com/vertex-ai/docs/general/access-control)를 참조하십시오.

<Note>
  비용 추적 및 액세스 제어를 단순화하기 위해 Claude Code용 전용 GCP 프로젝트를 만듭니다.
</Note>

## 1M 토큰 context window

Claude Opus 4.7, Opus 4.6 및 Sonnet 4.6은 Vertex AI에서 [1M 토큰 context window](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window)를 지원합니다. Claude Code는 1M 모델 변형을 선택할 때 확장된 context window를 자동으로 활성화합니다.

[설정 마법사](#sign-in-with-vertex-ai)는 모델을 고정할 때 1M context 옵션을 제공합니다. 수동으로 고정된 모델에 대해 대신 활성화하려면 모델 ID에 `[1m]`을 추가합니다. 자세한 내용은 [타사 배포를 위한 모델 고정](/ko/model-config#pin-models-for-third-party-deployments)을 참조하십시오.

## 문제 해결

할당량 문제가 발생하는 경우:

* [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)을 통해 현재 할당량을 확인하거나 할당량 증가를 요청합니다

"모델을 찾을 수 없음" 404 오류가 발생하는 경우:

* [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)에서 모델이 활성화되어 있는지 확인합니다
* 지정된 위치에서 모델을 사용할 수 있는지 확인합니다. 일부 모델은 특정 지역이 아닌 `global` 또는 `eu` 및 `us`와 같은 다중 지역 위치에서만 제공됩니다
* `CLOUD_ML_REGION=global`을 사용하는 경우 [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)의 "지원되는 기능" 아래에서 모델이 전역 엔드포인트를 지원하는지 확인합니다. 전역 엔드포인트를 지원하지 않는 모델의 경우:
  * `ANTHROPIC_MODEL` 또는 `ANTHROPIC_DEFAULT_HAIKU_MODEL`을 통해 지원되는 모델을 지정하거나,
  * `VERTEX_REGION_<MODEL_NAME>` 환경 변수를 사용하여 지역 또는 다중 지역 위치를 설정합니다

429 오류가 발생하는 경우:

* 지역 엔드포인트의 경우 주 모델과 소형/빠른 모델이 선택한 지역에서 지원되는지 확인합니다
* `CLOUD_ML_REGION=global`로 전환하여 더 나은 가용성을 고려합니다

## 추가 리소스

* [Vertex AI 설명서](https://cloud.google.com/vertex-ai/docs)
* [Vertex AI 가격](https://cloud.google.com/vertex-ai/pricing)
* [Vertex AI 할당량 및 제한](https://cloud.google.com/vertex-ai/docs/quotas)
