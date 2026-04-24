> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Amazon Bedrock의 Claude Code

> Amazon Bedrock을 통한 Claude Code 구성, 설정, IAM 구성 및 문제 해결에 대해 알아봅니다.

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

## 필수 조건

Claude Code를 Bedrock으로 구성하기 전에 다음을 확인하십시오:

* Bedrock 액세스가 활성화된 AWS 계정
* Bedrock에서 원하는 Claude 모델(예: Claude Sonnet 4.6)에 대한 액세스
* AWS CLI 설치 및 구성(선택 사항 - 자격 증명을 얻을 다른 메커니즘이 없는 경우에만 필요)
* 적절한 IAM 권한

Bedrock 자격 증명으로 로그인하려면 아래의 [Bedrock으로 로그인](#sign-in-with-bedrock)을 따르십시오. 팀 전체에 Claude Code를 배포하려면 [수동 설정](#set-up-manually) 단계를 사용하고 롤아웃 전에 [모델 버전을 고정](#4-pin-model-versions)하십시오.

## Bedrock으로 로그인

AWS 자격 증명이 있고 Bedrock을 통해 Claude Code 사용을 시작하려면 로그인 마법사가 이를 안내합니다. AWS 측 필수 조건은 계정당 한 번 완료하며, 마법사가 Claude Code 측을 처리합니다.

<Steps>
  <Step title="AWS 계정에서 Anthropic 모델 활성화">
    [Amazon Bedrock 콘솔](https://console.aws.amazon.com/bedrock/)에서 모델 카탈로그를 열고 Anthropic 모델을 선택한 후 사용 사례 양식을 제출하십시오. 제출 후 즉시 액세스가 부여됩니다. AWS Organizations의 경우 [사용 사례 세부 정보 제출](#1-submit-use-case-details)을 참조하고 권한의 경우 [IAM 구성](#iam-configuration)을 참조하십시오.
  </Step>

  <Step title="Claude Code를 시작하고 Bedrock 선택">
    `claude`를 실행하십시오. 로그인 프롬프트에서 **3rd-party platform**을 선택한 후 **Amazon Bedrock**을 선택하십시오.
  </Step>

  <Step title="마법사 프롬프트 따르기">
    AWS에 인증하는 방법을 선택하십시오: `~/.aws` 디렉토리에서 감지된 AWS 프로필, Bedrock API 키, 액세스 키 및 시크릿, 또는 환경에 이미 있는 자격 증명. 마법사가 지역을 선택하고 계정이 호출할 수 있는 Claude 모델을 확인한 후 고정할 수 있도록 합니다. 결과를 [사용자 설정 파일](/ko/settings)의 `env` 블록에 저장하므로 환경 변수를 직접 내보낼 필요가 없습니다.
  </Step>
</Steps>

로그인한 후 언제든지 `/setup-bedrock`을 실행하여 마법사를 다시 열고 자격 증명, 지역 또는 모델 고정을 변경할 수 있습니다.

## 수동으로 설정

예를 들어 CI 또는 스크립트된 엔터프라이즈 롤아웃에서 마법사 대신 환경 변수를 통해 Bedrock을 구성하려면 아래 단계를 따르십시오.

### 1. 사용 사례 세부 정보 제출

Anthropic 모델의 첫 사용자는 모델을 호출하기 전에 사용 사례 세부 정보를 제출해야 합니다. 이는 AWS 계정당 한 번 수행됩니다.

1. 아래에 설명된 올바른 IAM 권한이 있는지 확인하십시오
2. [Amazon Bedrock 콘솔](https://console.aws.amazon.com/bedrock/)로 이동하십시오
3. **모델 카탈로그**에서 Anthropic 모델을 선택하십시오
4. 사용 사례 양식을 완료하십시오. 제출 후 즉시 액세스가 부여됩니다.

AWS Organizations를 사용하는 경우 관리 계정에서 [`PutUseCaseForModelAccess` API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_PutUseCaseForModelAccess.html)를 사용하여 양식을 한 번 제출할 수 있습니다. 이 호출에는 `bedrock:PutUseCaseForModelAccess` IAM 권한이 필요합니다. 승인은 자동으로 하위 계정으로 확장됩니다.

### 2. AWS 자격 증명 구성

Claude Code는 기본 AWS SDK 자격 증명 체인을 사용합니다. 다음 방법 중 하나를 사용하여 자격 증명을 설정하십시오:

**옵션 A: AWS CLI 구성**

```bash theme={null}
aws configure
```

**옵션 B: 환경 변수(액세스 키)**

```bash theme={null}
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token
```

**옵션 C: 환경 변수(SSO 프로필)**

```bash theme={null}
aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name
```

**옵션 D: AWS Management Console 자격 증명**

```bash theme={null}
aws login
```

`aws login`에 대해 [자세히 알아보기](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html).

**옵션 E: Bedrock API 키**

```bash theme={null}
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

Bedrock API 키는 전체 AWS 자격 증명이 필요 없는 더 간단한 인증 방법을 제공합니다. [Bedrock API 키에 대해 자세히 알아보기](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/).

#### 고급 자격 증명 구성

Claude Code는 AWS SSO 및 회사 ID 공급자에 대한 자동 자격 증명 새로 고침을 지원합니다. Claude Code 설정 파일에 이러한 설정을 추가하십시오([설정](/ko/settings)에서 파일 위치 참조).

Claude Code가 AWS 자격 증명이 만료되었음을 감지하면(타임스탬프를 기반으로 로컬에서 또는 Bedrock이 자격 증명 오류를 반환할 때), 요청을 다시 시도하기 전에 새 자격 증명을 얻기 위해 구성된 `awsAuthRefresh` 및/또는 `awsCredentialExport` 명령을 자동으로 실행합니다.

##### 예제 구성

```json theme={null}
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": {
    "AWS_PROFILE": "myprofile"
  }
}
```

##### 구성 설정 설명

**`awsAuthRefresh`**: `.aws` 디렉토리를 수정하는 명령(예: 자격 증명, SSO 캐시 또는 구성 파일 업데이트)에 사용하십시오. 명령의 출력이 사용자에게 표시되지만 대화형 입력은 지원되지 않습니다. 이는 CLI가 URL 또는 코드를 표시하고 브라우저에서 인증을 완료하는 브라우저 기반 SSO 흐름에 적합합니다.

**`awsCredentialExport`**: `.aws`를 수정할 수 없고 자격 증명을 직접 반환해야 하는 경우에만 사용하십시오. 출력은 자동으로 캡처되며 사용자에게 표시되지 않습니다. 명령은 다음 형식으로 JSON을 출력해야 합니다:

```json theme={null}
{
  "Credentials": {
    "AccessKeyId": "value",
    "SecretAccessKey": "value",
    "SessionToken": "value"
  }
}
```

### 3. Claude Code 구성

Bedrock을 활성화하려면 다음 환경 변수를 설정하십시오:

```bash theme={null}
# Bedrock 통합 활성화
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # 또는 선호하는 지역

# 선택 사항: 소형/빠른 모델(Haiku)의 지역 재정의
# Bedrock Mantle에도 적용됩니다.
export ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION=us-west-2

# 선택 사항: 사용자 정의 엔드포인트 또는 게이트웨이를 위한 Bedrock 엔드포인트 URL 재정의
# export ANTHROPIC_BEDROCK_BASE_URL=https://bedrock-runtime.us-east-1.amazonaws.com
```

Claude Code에 대해 Bedrock을 활성화할 때 다음을 염두에 두십시오:

* `AWS_REGION`은 필수 환경 변수입니다. Claude Code는 이 설정에 대해 `.aws` 구성 파일을 읽지 않습니다.
* Bedrock을 사용할 때 `/login` 및 `/logout` 명령은 AWS 자격 증명을 통해 인증이 처리되므로 비활성화됩니다.
* 다른 프로세스에 유출되지 않도록 하려는 `AWS_PROFILE`과 같은 환경 변수에 설정 파일을 사용할 수 있습니다. 자세한 내용은 [설정](/ko/settings)을 참조하십시오.

### 4. 모델 버전 고정

<Warning>
  여러 사용자에게 배포할 때 특정 모델 버전을 고정하십시오. 고정하지 않으면 `sonnet` 및 `opus`와 같은 모델 별칭이 최신 버전으로 확인되며, Anthropic이 업데이트를 출시할 때 Bedrock 계정에서 아직 사용할 수 없을 수 있습니다. Claude Code는 [시작 시](#startup-model-checks) 최신 버전을 사용할 수 없을 때 이전 버전으로 폴백하지만, 고정하면 사용자가 새 모델로 이동하는 시기를 제어할 수 있습니다.
</Warning>

이러한 환경 변수를 특정 Bedrock 모델 ID로 설정하십시오.

`ANTHROPIC_DEFAULT_OPUS_MODEL`이 없으면 Bedrock의 `opus` 별칭이 Opus 4.6으로 확인됩니다. 최신 모델을 사용하려면 Opus 4.7 ID로 설정하십시오:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
```

이러한 변수는 교차 지역 추론 프로필 ID(`us.` 접두사 포함)를 사용합니다. 다른 지역 접두사 또는 애플리케이션 추론 프로필을 사용하는 경우 적절히 조정하십시오. 현재 및 레거시 모델 ID는 [모델 개요](https://platform.claude.com/docs/en/about-claude/models/overview)를 참조하십시오. 전체 환경 변수 목록은 [모델 구성](/ko/model-config#pin-models-for-third-party-deployments)을 참조하십시오.

고정 변수가 설정되지 않은 경우 Claude Code는 이러한 기본 모델을 사용합니다:

| 모델 유형    | 기본값                                            |
| :------- | :--------------------------------------------- |
| 기본 모델    | `us.anthropic.claude-sonnet-4-5-20250929-v1:0` |
| 소형/빠른 모델 | `us.anthropic.claude-haiku-4-5-20251001-v1:0`  |

모델을 추가로 사용자 정의하려면 다음 방법 중 하나를 사용하십시오:

```bash theme={null}
# 추론 프로필 ID 사용
export ANTHROPIC_MODEL='global.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'

# 애플리케이션 추론 프로필 ARN 사용
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# 선택 사항: 필요한 경우 프롬프트 캐싱 비활성화
export DISABLE_PROMPT_CACHING=1

# 선택 사항: 5분 기본값 대신 1시간 프롬프트 캐시 TTL 요청
export ENABLE_PROMPT_CACHING_1H=1
```

<Note>[프롬프트 캐싱](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)은 모든 지역에서 사용할 수 없을 수 있습니다. 1시간 TTL이 있는 캐시 쓰기는 5분 쓰기보다 높은 요금으로 청구됩니다.</Note>

#### 각 모델 버전을 추론 프로필에 매핑

`ANTHROPIC_DEFAULT_*_MODEL` 환경 변수는 모델 제품군당 하나의 추론 프로필을 구성합니다. 조직이 `/model` 선택기에서 동일한 제품군의 여러 버전을 노출하고 각각 자신의 애플리케이션 추론 프로필 ARN으로 라우팅해야 하는 경우 [설정 파일](/ko/settings#settings-files)에서 `modelOverrides` 설정을 대신 사용하십시오.

이 예제는 네 개의 Opus 버전을 고유한 ARN에 매핑하므로 사용자는 조직의 추론 프로필을 우회하지 않고 버전 간에 전환할 수 있습니다:

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

사용자가 `/model`에서 이러한 버전 중 하나를 선택하면 Claude Code는 매핑된 ARN으로 Bedrock을 호출합니다. 재정의가 없는 버전은 기본 제공 Bedrock 모델 ID 또는 시작 시 발견된 일치하는 추론 프로필로 폴백됩니다. 재정의가 `availableModels` 및 기타 모델 설정과 상호 작용하는 방식에 대한 자세한 내용은 [버전별 모델 ID 재정의](/ko/model-config#override-model-ids-per-version)를 참조하십시오.

## 시작 모델 확인

Claude Code가 Bedrock으로 구성되어 시작되면 사용하려는 모델이 계정에서 액세스 가능한지 확인합니다. 이 확인에는 Claude Code v2.1.94 이상이 필요합니다.

현재 Claude Code 기본값보다 오래된 모델 버전을 고정했고 계정이 최신 버전을 호출할 수 있는 경우 Claude Code는 고정을 업데이트하라는 메시지를 표시합니다. 수락하면 새 모델 ID를 [사용자 설정 파일](/ko/settings)에 쓰고 Claude Code를 다시 시작합니다. 거부하면 다음 기본 버전 변경까지 기억됩니다. [애플리케이션 추론 프로필 ARN](#map-each-model-version-to-an-inference-profile)을 가리키는 고정은 관리자가 관리하므로 건너뜁니다.

모델을 고정하지 않았고 현재 기본값을 계정에서 사용할 수 없는 경우 Claude Code는 현재 세션에서 이전 버전으로 폴백하고 알림을 표시합니다. 폴백은 유지되지 않습니다. Bedrock 계정에서 최신 모델을 활성화하거나 [버전을 고정](#4-pin-model-versions)하여 선택을 영구적으로 만드십시오.

## IAM 구성

Claude Code에 필요한 권한이 있는 IAM 정책을 만드십시오:

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

더 제한적인 권한의 경우 리소스를 특정 추론 프로필 ARN으로 제한할 수 있습니다.

자세한 내용은 [Bedrock IAM 설명서](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html)를 참조하십시오.

<Note>
  비용 추적 및 액세스 제어를 단순화하기 위해 Claude Code용 전용 AWS 계정을 만드십시오.
</Note>

## 1M 토큰 컨텍스트 윈도우

Claude Opus 4.7, Opus 4.6 및 Sonnet 4.6은 Amazon Bedrock에서 [1M 토큰 컨텍스트 윈도우](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window)를 지원합니다. Claude Code는 1M 모델 변형을 선택할 때 확장된 컨텍스트 윈도우를 자동으로 활성화합니다.

[설정 마법사](#sign-in-with-bedrock)는 모델을 고정할 때 1M 컨텍스트 옵션을 제공합니다. 수동으로 고정된 모델에 대해 대신 활성화하려면 모델 ID에 `[1m]`을 추가하십시오. 자세한 내용은 [타사 배포를 위한 모델 고정](/ko/model-config#pin-models-for-third-party-deployments)을 참조하십시오.

## AWS Guardrails

[Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)를 사용하면 Claude Code에 대한 콘텐츠 필터링을 구현할 수 있습니다. [Amazon Bedrock 콘솔](https://console.aws.amazon.com/bedrock/)에서 Guardrail을 만들고 버전을 게시한 다음 Guardrail 헤더를 [설정 파일](/ko/settings)에 추가하십시오. 교차 지역 추론 프로필을 사용하는 경우 Guardrail에서 교차 지역 추론을 활성화하십시오.

예제 구성:

```json theme={null}
{
  "env": {
    "ANTHROPIC_CUSTOM_HEADERS": "X-Amzn-Bedrock-GuardrailIdentifier: your-guardrail-id\nX-Amzn-Bedrock-GuardrailVersion: 1"
  }
}
```

## Mantle 엔드포인트 사용

Mantle은 Bedrock Invoke API 대신 기본 Anthropic API 형태를 통해 Claude 모델을 제공하는 Amazon Bedrock 엔드포인트입니다. 이 페이지의 앞부분에서 설명한 동일한 AWS 자격 증명, IAM 권한 및 `awsAuthRefresh` 구성을 사용합니다.

<Note>
  Mantle에는 Claude Code v2.1.94 이상이 필요합니다. `claude --version`을 실행하여 확인하십시오.
</Note>

### Mantle 활성화

AWS 자격 증명이 이미 구성되어 있으면 `CLAUDE_CODE_USE_MANTLE`을 설정하여 요청을 Mantle 엔드포인트로 라우팅하십시오:

```bash theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export AWS_REGION=us-east-1
```

Claude Code는 `AWS_REGION`에서 엔드포인트 URL을 구성합니다. 사용자 정의 엔드포인트 또는 게이트웨이를 위해 재정의하려면 `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`을 설정하십시오.

Claude Code 내에서 `/status`를 실행하여 확인하십시오. Mantle이 활성화되면 제공자 줄에 `Amazon Bedrock (Mantle)`이 표시됩니다.

### Mantle 모델 선택

Mantle은 `anthropic.` 접두사가 있고 버전 접미사가 없는 모델 ID를 사용합니다(예: `anthropic.claude-haiku-4-5`). 계정에서 사용 가능한 모델은 조직에 부여된 것에 따라 다르며, 추가 모델 ID는 AWS의 온보딩 자료에 나열됩니다. 허용 목록에 있는 모델에 대한 액세스를 요청하려면 AWS 계정 팀에 문의하십시오.

`--model` 플래그 또는 Claude Code 내의 `/model`로 모델을 설정하십시오:

```bash theme={null}
claude --model anthropic.claude-haiku-4-5
```

### Invoke API와 함께 Mantle 실행

Mantle에서 사용 가능한 모델이 현재 사용하는 모든 모델을 포함하지 않을 수 있습니다. `CLAUDE_CODE_USE_BEDROCK` 및 `CLAUDE_CODE_USE_MANTLE`을 모두 설정하면 Claude Code가 동일한 세션에서 두 엔드포인트를 모두 호출할 수 있습니다. Mantle 형식과 일치하는 모델 ID는 Mantle으로 라우팅되고 다른 모든 모델 ID는 Bedrock Invoke API로 이동합니다.

```bash theme={null}
export CLAUDE_CODE_USE_BEDROCK=1
export CLAUDE_CODE_USE_MANTLE=1
```

Mantle 모델을 `/model` 선택기에 표시하려면 [설정 파일](/ko/settings)의 `availableModels`에 ID를 나열하십시오. 이 설정은 선택기를 나열된 항목으로 제한하므로 유지하려는 모든 별칭을 포함하십시오:

```json theme={null}
{
  "availableModels": ["opus", "sonnet", "haiku", "anthropic.claude-haiku-4-5"]
}
```

`anthropic.` 접두사가 있는 항목은 사용자 정의 선택기 옵션으로 추가되고 Mantle으로 라우팅됩니다. `anthropic.claude-haiku-4-5`를 계정에 부여된 모델 ID로 바꾸십시오. `availableModels`가 다른 모델 설정과 상호 작용하는 방식에 대한 자세한 내용은 [모델 선택 제한](/ko/model-config#restrict-model-selection)을 참조하십시오.

두 공급자가 모두 활성화되면 `/status`는 `Amazon Bedrock + Amazon Bedrock (Mantle)`을 표시합니다.

### 게이트웨이를 통해 Mantle 라우팅

조직이 모델 트래픽을 AWS 자격 증명을 서버 측에 주입하는 중앙 집중식 [LLM 게이트웨이](/ko/llm-gateway)를 통해 라우팅하는 경우 클라이언트 측 인증을 비활성화하여 Claude Code가 SigV4 서명 또는 `x-api-key` 헤더 없이 요청을 보내도록 하십시오:

```bash theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export CLAUDE_CODE_SKIP_MANTLE_AUTH=1
export ANTHROPIC_BEDROCK_MANTLE_BASE_URL=https://your-gateway.example.com
```

### Mantle 환경 변수

이러한 변수는 Mantle 엔드포인트에만 해당됩니다. 전체 목록은 [환경 변수](/ko/env-vars)를 참조하십시오.

| 변수                                      | 목적                                           |
| :-------------------------------------- | :------------------------------------------- |
| `CLAUDE_CODE_USE_MANTLE`                | Mantle 엔드포인트를 활성화합니다. `1` 또는 `true`로 설정하십시오. |
| `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`     | 기본 Mantle 엔드포인트 URL 재정의                      |
| `CLAUDE_CODE_SKIP_MANTLE_AUTH`          | 프록시 설정을 위해 클라이언트 측 인증 건너뛰기                   |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` | Haiku 클래스 모델의 AWS 지역 재정의(Bedrock과 공유)        |

## 문제 해결

### SSO 및 회사 프록시를 사용한 인증 루프

AWS SSO를 사용할 때 브라우저 탭이 반복적으로 생성되면 [설정 파일](/ko/settings)에서 `awsAuthRefresh` 설정을 제거하십시오. 이는 회사 VPN 또는 TLS 검사 프록시가 SSO 브라우저 흐름을 중단할 때 발생할 수 있습니다. Claude Code는 중단된 연결을 인증 실패로 취급하고 `awsAuthRefresh`를 다시 실행하여 무한 루프를 발생시킵니다.

네트워크 환경이 자동 브라우저 기반 SSO 흐름을 방해하는 경우 `awsAuthRefresh`에 의존하는 대신 Claude Code를 시작하기 전에 `aws sso login`을 수동으로 사용하십시오.

### 지역 문제

지역 문제가 발생하는 경우:

* 모델 가용성 확인: `aws bedrock list-inference-profiles --region your-region`
* 지원되는 지역으로 전환: `export AWS_REGION=us-east-1`
* 교차 지역 액세스를 위해 추론 프로필 사용 고려

"on-demand throughput isn't supported" 오류가 발생하는 경우:

* 모델을 [추론 프로필](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html) ID로 지정하십시오

Claude Code는 Bedrock [Invoke API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html)를 사용하며 Converse API를 지원하지 않습니다.

### Mantle 엔드포인트 오류

`CLAUDE_CODE_USE_MANTLE`을 설정한 후 `/status`에 `Amazon Bedrock (Mantle)`이 표시되지 않으면 변수가 프로세스에 도달하지 않습니다. Claude Code를 시작한 셸에서 내보내졌는지 확인하거나 [설정 파일](/ko/settings)의 `env` 블록에 설정하십시오.

유효한 자격 증명이 있는 Mantle 엔드포인트의 `403`은 AWS 계정이 요청한 모델에 대한 액세스 권한을 부여받지 않았음을 의미합니다. 액세스를 요청하려면 AWS 계정 팀에 문의하십시오.

모델 ID를 이름으로 지정하는 `400`은 해당 모델이 Mantle에서 제공되지 않음을 의미합니다. Mantle은 표준 Bedrock 카탈로그와 별개의 자체 모델 라인업을 가지고 있으므로 `us.anthropic.claude-sonnet-4-6`과 같은 추론 프로필 ID는 작동하지 않습니다. Mantle 형식 ID를 사용하거나 [두 엔드포인트를 모두 활성화](#run-mantle-alongside-the-invoke-api)하여 Claude Code가 각 요청을 모델을 사용할 수 있는 엔드포인트로 라우팅하도록 하십시오.

## 추가 리소스

* [Bedrock 설명서](https://docs.aws.amazon.com/bedrock/)
* [Bedrock 가격](https://aws.amazon.com/bedrock/pricing/)
* [Bedrock 추론 프로필](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Bedrock 토큰 번다운 및 할당량](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas-token-burndown.html)
* [Claude Code on Amazon Bedrock: Quick Setup Guide](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)
* [Claude Code Monitoring Implementation (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)
