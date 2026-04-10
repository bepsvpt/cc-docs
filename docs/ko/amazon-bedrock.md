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

# Amazon Bedrock의 Claude Code

> Amazon Bedrock을 통한 Claude Code 구성, 설정, IAM 구성 및 문제 해결에 대해 알아봅니다.

## 필수 조건

Claude Code를 Bedrock으로 구성하기 전에 다음을 확인하십시오:

* Bedrock 액세스가 활성화된 AWS 계정
* Bedrock에서 원하는 Claude 모델(예: Claude Sonnet 4.6)에 대한 액세스
* AWS CLI 설치 및 구성(선택 사항 - 자격 증명을 얻을 다른 메커니즘이 없는 경우에만 필요)
* 적절한 IAM 권한

<Note>
  Claude Code를 여러 사용자에게 배포하는 경우 Anthropic이 새 모델을 출시할 때 중단을 방지하기 위해 [모델 버전을 고정](#4-pin-model-versions)하십시오.
</Note>

## 설정

### 1. 사용 사례 세부 정보 제출

Anthropic 모델의 첫 사용자는 모델을 호출하기 전에 사용 사례 세부 정보를 제출해야 합니다. 이는 계정당 한 번 수행됩니다.

1. 올바른 IAM 권한이 있는지 확인하십시오(아래에서 자세히 알아보기)
2. [Amazon Bedrock 콘솔](https://console.aws.amazon.com/bedrock/)로 이동하십시오
3. **Chat/Text playground**를 선택하십시오
4. 모든 Anthropic 모델을 선택하면 사용 사례 양식을 작성하라는 메시지가 표시됩니다

### 2. AWS 자격 증명 구성

Claude Code는 기본 AWS SDK 자격 증명 체인을 사용합니다. 다음 방법 중 하나를 사용하여 자격 증명을 설정하십시오:

**옵션 A: AWS CLI 구성**

```bash  theme={null}
aws configure
```

**옵션 B: 환경 변수(액세스 키)**

```bash  theme={null}
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token
```

**옵션 C: 환경 변수(SSO 프로필)**

```bash  theme={null}
aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name
```

**옵션 D: AWS Management Console 자격 증명**

```bash  theme={null}
aws login
```

`aws login`에 대해 [자세히 알아보기](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html).

**옵션 E: Bedrock API 키**

```bash  theme={null}
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

Bedrock API 키는 전체 AWS 자격 증명이 필요 없는 더 간단한 인증 방법을 제공합니다. [Bedrock API 키에 대해 자세히 알아보기](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/).

#### 고급 자격 증명 구성

Claude Code는 AWS SSO 및 회사 ID 공급자에 대한 자동 자격 증명 새로 고침을 지원합니다. Claude Code 설정 파일에 이러한 설정을 추가하십시오([설정](/ko/settings)에서 파일 위치 참조).

Claude Code가 AWS 자격 증명이 만료되었음을 감지하면(타임스탬프를 기반으로 로컬에서 또는 Bedrock이 자격 증명 오류를 반환할 때), 요청을 다시 시도하기 전에 새 자격 증명을 얻기 위해 구성된 `awsAuthRefresh` 및/또는 `awsCredentialExport` 명령을 자동으로 실행합니다.

##### 예제 구성

```json  theme={null}
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

```json  theme={null}
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

```bash  theme={null}
# Bedrock 통합 활성화
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # 또는 선호하는 지역

# 선택 사항: 소형/빠른 모델(Haiku)의 지역 재정의
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
  모든 배포에 대해 특정 모델 버전을 고정하십시오. 모델 별칭(`sonnet`, `opus`, `haiku`)을 고정하지 않고 사용하면 Claude Code가 Bedrock 계정에서 사용할 수 없는 최신 모델 버전을 사용하려고 시도하여 Anthropic이 업데이트를 출시할 때 기존 사용자가 중단될 수 있습니다.
</Warning>

이러한 환경 변수를 특정 Bedrock 모델 ID로 설정하십시오:

```bash  theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'
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

```bash  theme={null}
# 추론 프로필 ID 사용
export ANTHROPIC_MODEL='global.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'

# 애플리케이션 추론 프로필 ARN 사용
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# 선택 사항: 필요한 경우 프롬프트 캐싱 비활성화
export DISABLE_PROMPT_CACHING=1
```

<Note>[프롬프트 캐싱](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)은 모든 지역에서 사용할 수 없을 수 있습니다.</Note>

#### 각 모델 버전을 추론 프로필에 매핑

`ANTHROPIC_DEFAULT_*_MODEL` 환경 변수는 모델 제품군당 하나의 추론 프로필을 구성합니다. 조직이 `/model` 선택기에서 동일한 제품군의 여러 버전을 노출하고 각각 자신의 애플리케이션 추론 프로필 ARN으로 라우팅해야 하는 경우 [설정 파일](/ko/settings#settings-files)에서 `modelOverrides` 설정을 대신 사용하십시오.

이 예제는 세 개의 Opus 버전을 고유한 ARN에 매핑하므로 사용자는 조직의 추론 프로필을 우회하지 않고 버전 간에 전환할 수 있습니다:

```json  theme={null}
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-opus-4-1-20250805": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-41-prod"
  }
}
```

사용자가 `/model`에서 이러한 버전 중 하나를 선택하면 Claude Code는 매핑된 ARN으로 Bedrock을 호출합니다. 재정의가 없는 버전은 기본 제공 Bedrock 모델 ID 또는 시작 시 발견된 일치하는 추론 프로필로 폴백됩니다. 재정의가 `availableModels` 및 기타 모델 설정과 상호 작용하는 방식에 대한 자세한 내용은 [버전별 모델 ID 재정의](/ko/model-config#override-model-ids-per-version)를 참조하십시오.

## IAM 구성

Claude Code에 필요한 권한이 있는 IAM 정책을 만드십시오:

```json  theme={null}
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

Claude Opus 4.6 및 Sonnet 4.6은 Amazon Bedrock에서 [1M 토큰 컨텍스트 윈도우](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window)를 지원합니다. Claude Code는 1M 모델 변형을 선택할 때 확장된 컨텍스트 윈도우를 자동으로 활성화합니다.

고정된 모델에 대해 1M 컨텍스트 윈도우를 활성화하려면 모델 ID에 `[1m]`을 추가하십시오. 자세한 내용은 [타사 배포를 위한 모델 고정](/ko/model-config#pin-models-for-third-party-deployments)을 참조하십시오.

## AWS Guardrails

[Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html)를 사용하면 Claude Code에 대한 콘텐츠 필터링을 구현할 수 있습니다. [Amazon Bedrock 콘솔](https://console.aws.amazon.com/bedrock/)에서 Guardrail을 만들고 버전을 게시한 다음 Guardrail 헤더를 [설정 파일](/ko/settings)에 추가하십시오. 교차 지역 추론 프로필을 사용하는 경우 Guardrail에서 교차 지역 추론을 활성화하십시오.

예제 구성:

```json  theme={null}
{
  "env": {
    "ANTHROPIC_CUSTOM_HEADERS": "X-Amzn-Bedrock-GuardrailIdentifier: your-guardrail-id\nX-Amzn-Bedrock-GuardrailVersion: 1"
  }
}
```

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

## 추가 리소스

* [Bedrock 설명서](https://docs.aws.amazon.com/bedrock/)
* [Bedrock 가격](https://aws.amazon.com/bedrock/pricing/)
* [Bedrock 추론 프로필](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Claude Code on Amazon Bedrock: Quick Setup Guide](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)
* [Claude Code Monitoring Implementation (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)
