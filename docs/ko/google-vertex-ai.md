> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Google Vertex AI에서 Claude Code 사용하기

> Google Vertex AI를 통한 Claude Code 구성, 설정, IAM 구성 및 문제 해결에 대해 알아봅니다.

## 필수 요구사항

Claude Code를 Vertex AI로 구성하기 전에 다음을 확인하십시오:

* 청구가 활성화된 Google Cloud Platform(GCP) 계정
* Vertex AI API가 활성화된 GCP 프로젝트
* 원하는 Claude 모델에 대한 액세스(예: Claude Sonnet 4.5)
* Google Cloud SDK(`gcloud`) 설치 및 구성
* 원하는 GCP 지역에 할당된 할당량

## 지역 구성

Claude Code는 Vertex AI [글로벌](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai) 및 지역 엔드포인트 모두에서 사용할 수 있습니다.

<Note>
  Vertex AI는 모든 지역에서 Claude Code 기본 모델을 지원하지 않을 수 있습니다. [지원되는 지역 또는 모델](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models)로 전환해야 할 수 있습니다.
</Note>

<Note>
  Vertex AI는 글로벌 엔드포인트에서 Claude Code 기본 모델을 지원하지 않을 수 있습니다. 지역 엔드포인트 또는 [지원되는 모델](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models)로 전환해야 할 수 있습니다.
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
3. 원하는 Claude 모델에 대한 액세스를 요청합니다(예: Claude Sonnet 4.5)
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

# 선택사항: 필요한 경우 prompt caching 비활성화
export DISABLE_PROMPT_CACHING=1

# CLOUD_ML_REGION=global일 때 지원되지 않는 모델의 지역 재정의
export VERTEX_REGION_CLAUDE_3_5_HAIKU=us-east5

# 선택사항: 다른 특정 모델의 지역 재정의
export VERTEX_REGION_CLAUDE_3_5_SONNET=us-east5
export VERTEX_REGION_CLAUDE_3_7_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_0_OPUS=europe-west1
export VERTEX_REGION_CLAUDE_4_0_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_1_OPUS=europe-west1
```

<Note>
  [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)은 `cache_control` 임시 플래그를 지정할 때 자동으로 지원됩니다. 이를 비활성화하려면 `DISABLE_PROMPT_CACHING=1`을 설정하십시오. 높은 속도 제한을 위해 Google Cloud 지원팀에 문의하십시오.
</Note>

<Note>
  Vertex AI를 사용할 때 `/login` 및 `/logout` 명령은 Google Cloud 자격증명을 통해 인증이 처리되므로 비활성화됩니다.
</Note>

### 5. 모델 구성

Claude Code는 Vertex AI에 대해 다음 기본 모델을 사용합니다:

| 모델 유형    | 기본값                          |
| :------- | :--------------------------- |
| 주 모델     | `claude-sonnet-4-5@20250929` |
| 소형/빠른 모델 | `claude-haiku-4-5@20251001`  |

<Note>
  Vertex AI 사용자의 경우 Claude Code는 Haiku 3.5에서 Haiku 4.5로 자동 업그레이드되지 않습니다. 최신 Haiku 모델로 수동으로 전환하려면 `ANTHROPIC_DEFAULT_HAIKU_MODEL` 환경 변수를 전체 모델 이름으로 설정하십시오(예: `claude-haiku-4-5@20251001`).
</Note>

모델을 사용자 정의하려면:

```bash  theme={null}
export ANTHROPIC_MODEL='claude-opus-4-1@20250805'
export ANTHROPIC_SMALL_FAST_MODEL='claude-haiku-4-5@20251001'
```

## IAM 구성

필요한 IAM 권한을 할당합니다:

`roles/aiplatform.user` 역할에는 필요한 권한이 포함됩니다:

* `aiplatform.endpoints.predict` - 모델 호출 및 토큰 계산에 필요

더 제한적인 권한의 경우 위의 권한만 포함하는 사용자 정의 역할을 만듭니다.

자세한 내용은 [Vertex IAM 설명서](https://cloud.google.com/vertex-ai/docs/general/access-control)를 참조하십시오.

<Note>
  비용 추적 및 액세스 제어를 단순화하기 위해 Claude Code용 전용 GCP 프로젝트를 만드는 것을 권장합니다.
</Note>

## 1M 토큰 context window

Claude Sonnet 4 및 Sonnet 4.5는 Vertex AI에서 [1M 토큰 context window](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window)를 지원합니다.

<Note>
  1M 토큰 context window는 현재 베타 버전입니다. 확장된 context window를 사용하려면 Vertex AI 요청에 `context-1m-2025-08-07` 베타 헤더를 포함하십시오.
</Note>

## 문제 해결

할당량 문제가 발생하는 경우:

* [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)을 통해 현재 할당량을 확인하거나 할당량 증가를 요청합니다

"모델을 찾을 수 없음" 404 오류가 발생하는 경우:

* [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)에서 모델이 활성화되어 있는지 확인합니다
* 지정된 지역에 액세스할 수 있는지 확인합니다
* `CLOUD_ML_REGION=global`을 사용하는 경우 [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)의 "Supported features"에서 모델이 글로벌 엔드포인트를 지원하는지 확인합니다. 글로벌 엔드포인트를 지원하지 않는 모델의 경우:
  * `ANTHROPIC_MODEL` 또는 `ANTHROPIC_SMALL_FAST_MODEL`을 통해 지원되는 모델을 지정하거나
  * `VERTEX_REGION_<MODEL_NAME>` 환경 변수를 사용하여 지역 엔드포인트를 설정합니다

429 오류가 발생하는 경우:

* 지역 엔드포인트의 경우 주 모델과 소형/빠른 모델이 선택한 지역에서 지원되는지 확인합니다
* 더 나은 가용성을 위해 `CLOUD_ML_REGION=global`로 전환하는 것을 고려합니다

## 추가 리소스

* [Vertex AI 설명서](https://cloud.google.com/vertex-ai/docs)
* [Vertex AI 가격](https://cloud.google.com/vertex-ai/pricing)
* [Vertex AI 할당량 및 제한](https://cloud.google.com/vertex-ai/docs/quotas)
