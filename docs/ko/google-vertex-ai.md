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

# Google Vertex AI에서 Claude Code 사용하기

> Google Vertex AI를 통해 Claude Code를 구성하는 방법을 알아봅니다. 설정, IAM 구성 및 문제 해결을 포함합니다.

## 필수 요구사항

Vertex AI를 사용하여 Claude Code를 구성하기 전에 다음을 확인하십시오:

* 청구가 활성화된 Google Cloud Platform(GCP) 계정
* Vertex AI API가 활성화된 GCP 프로젝트
* 원하는 Claude 모델에 대한 액세스(예: Claude Sonnet 4.6)
* Google Cloud SDK(`gcloud`) 설치 및 구성
* 원하는 GCP 지역에 할당된 할당량

<Note>
  Claude Code를 여러 사용자에게 배포하는 경우, Anthropic이 새 모델을 출시할 때 중단을 방지하기 위해 [모델 버전을 고정](#5-pin-model-versions)하십시오.
</Note>

## 지역 구성

Claude Code는 Vertex AI [전역](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai) 및 지역 엔드포인트 모두에서 사용할 수 있습니다.

<Note>
  Vertex AI는 모든 [지역](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models)에서 또는 [전역 엔드포인트](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models)에서 Claude Code 기본 모델을 지원하지 않을 수 있습니다. 지원되는 지역으로 전환하거나, 지역 엔드포인트를 사용하거나, 지원되는 모델을 지정해야 할 수 있습니다.
</Note>

## 설정

### 1. Vertex AI API 활성화

GCP 프로젝트에서 Vertex AI API를 활성화합니다:

```bash  theme={null}
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

<Note>
  인증할 때 Claude Code는 `ANTHROPIC_VERTEX_PROJECT_ID` 환경 변수에서 프로젝트 ID를 자동으로 사용합니다. 이를 재정의하려면 다음 환경 변수 중 하나를 설정하십시오: `GCLOUD_PROJECT`, `GOOGLE_CLOUD_PROJECT` 또는 `GOOGLE_APPLICATION_CREDENTIALS`.
</Note>

### 4. Claude Code 구성

다음 환경 변수를 설정합니다:

```bash  theme={null}
# Vertex AI 통합 활성화
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# 선택사항: 사용자 정의 엔드포인트 또는 게이트웨이를 위해 Vertex 엔드포인트 URL 재정의
# export ANTHROPIC_VERTEX_BASE_URL=https://aiplatform.googleapis.com

# 선택사항: 필요한 경우 prompt caching 비활성화
export DISABLE_PROMPT_CACHING=1

# CLOUD_ML_REGION=global일 때, 전역 엔드포인트를 지원하지 않는 모델의 지역 재정의
export VERTEX_REGION_CLAUDE_HAIKU_4_5=us-east5
export VERTEX_REGION_CLAUDE_4_6_SONNET=europe-west1
```

각 모델 버전에는 자체 `VERTEX_REGION_CLAUDE_*` 변수가 있습니다. 전체 목록은 [환경 변수 참조](/ko/env-vars)를 참조하십시오. [Vertex Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)에서 어떤 모델이 전역 엔드포인트를 지원하는지 또는 지역 전용인지 확인하십시오.

[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)은 `cache_control` ephemeral 플래그를 지정할 때 자동으로 지원됩니다. 이를 비활성화하려면 `DISABLE_PROMPT_CACHING=1`을 설정하십시오. 높은 속도 제한을 위해 Google Cloud 지원팀에 문의하십시오. Vertex AI를 사용할 때 `/login` 및 `/logout` 명령은 Google Cloud 자격증명을 통해 인증이 처리되므로 비활성화됩니다.

### 5. 모델 버전 고정

<Warning>
  모든 배포에 대해 특정 모델 버전을 고정합니다. 모델 별칭(`sonnet`, `opus`, `haiku`)을 고정하지 않고 사용하면 Claude Code가 Vertex AI 프로젝트에서 활성화되지 않은 최신 모델 버전을 사용하려고 시도하여 Anthropic이 업데이트를 출시할 때 기존 사용자가 중단될 수 있습니다.
</Warning>

이러한 환경 변수를 특정 Vertex AI 모델 ID로 설정합니다:

```bash  theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

현재 및 레거시 모델 ID는 [모델 개요](https://platform.claude.com/docs/en/about-claude/models/overview)를 참조하십시오. 환경 변수의 전체 목록은 [모델 구성](/ko/model-config#pin-models-for-third-party-deployments)을 참조하십시오.

Claude Code는 고정 변수가 설정되지 않았을 때 이러한 기본 모델을 사용합니다:

| 모델 유형    | 기본값                         |
| :------- | :-------------------------- |
| 주 모델     | `claude-sonnet-4-6`         |
| 소형/빠른 모델 | `claude-haiku-4-5@20251001` |

모델을 추가로 사용자 정의하려면:

```bash  theme={null}
export ANTHROPIC_MODEL='claude-opus-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

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

Claude Opus 4.6, Sonnet 4.6, Sonnet 4.5 및 Sonnet 4는 Vertex AI에서 [1M 토큰 context window](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window)를 지원합니다. Claude Code는 1M 모델 변형을 선택할 때 확장된 context window를 자동으로 활성화합니다.

고정된 모델에 대해 1M context window를 활성화하려면 모델 ID에 `[1m]`을 추가합니다. 자세한 내용은 [타사 배포를 위한 모델 고정](/ko/model-config#pin-models-for-third-party-deployments)을 참조하십시오.

## 문제 해결

할당량 문제가 발생하는 경우:

* [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)을 통해 현재 할당량을 확인하거나 할당량 증가를 요청합니다

"모델을 찾을 수 없음" 404 오류가 발생하는 경우:

* [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)에서 모델이 활성화되어 있는지 확인합니다
* 지정된 지역에 액세스할 수 있는지 확인합니다
* `CLOUD_ML_REGION=global`을 사용하는 경우 [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)의 "지원되는 기능" 아래에서 모델이 전역 엔드포인트를 지원하는지 확인합니다. 전역 엔드포인트를 지원하지 않는 모델의 경우:
  * `ANTHROPIC_MODEL` 또는 `ANTHROPIC_DEFAULT_HAIKU_MODEL`을 통해 지원되는 모델을 지정하거나,
  * `VERTEX_REGION_<MODEL_NAME>` 환경 변수를 사용하여 지역 엔드포인트를 설정합니다

429 오류가 발생하는 경우:

* 지역 엔드포인트의 경우 주 모델과 소형/빠른 모델이 선택한 지역에서 지원되는지 확인합니다
* `CLOUD_ML_REGION=global`로 전환하여 더 나은 가용성을 고려합니다

## 추가 리소스

* [Vertex AI 설명서](https://cloud.google.com/vertex-ai/docs)
* [Vertex AI 가격](https://cloud.google.com/vertex-ai/pricing)
* [Vertex AI 할당량 및 제한](https://cloud.google.com/vertex-ai/docs/quotas)
