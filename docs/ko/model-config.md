> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 모델 구성

> Claude Code 모델 구성에 대해 알아보기, opusplan과 같은 모델 별칭 포함

## 사용 가능한 모델

Claude Code의 `model` 설정에서 다음 중 하나를 구성할 수 있습니다:

* **모델 별칭**
* **모델 이름**
  * Anthropic API: 전체 **[모델 이름](https://platform.claude.com/docs/ko/about-claude/models/overview)**
  * Bedrock: 추론 프로필 ARN
  * Foundry: 배포 이름
  * Vertex: 버전 이름

### 모델 별칭

모델 별칭은 정확한 버전 번호를 기억할 필요 없이 모델 설정을 선택하는 편리한 방법을 제공합니다:

| 모델 별칭            | 동작                                                                                                                                         |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **`default`**    | 계정 유형에 따른 권장 모델 설정                                                                                                                         |
| **`sonnet`**     | 일일 코딩 작업을 위해 최신 Sonnet 모델(현재 Sonnet 4.6) 사용                                                                                                |
| **`opus`**       | 복잡한 추론 작업을 위해 최신 Opus 모델(현재 Opus 4.6) 사용                                                                                                   |
| **`haiku`**      | 간단한 작업을 위해 빠르고 효율적인 Haiku 모델 사용                                                                                                            |
| **`sonnet[1m]`** | 긴 세션을 위해 [100만 토큰 컨텍스트 윈도우](https://platform.claude.com/docs/ko/build-with-claude/context-windows#1m-token-context-window)를 사용하는 Sonnet 사용 |
| **`opus[1m]`**   | 긴 세션을 위해 [100만 토큰 컨텍스트 윈도우](https://platform.claude.com/docs/ko/build-with-claude/context-windows#1m-token-context-window)를 사용하는 Opus 사용   |
| **`opusplan`**   | Plan Mode 중에 `opus`를 사용한 후 실행을 위해 `sonnet`으로 전환하는 특수 모드                                                                                    |

별칭은 항상 최신 버전을 가리킵니다. 특정 버전으로 고정하려면 전체 모델 이름(예: `claude-opus-4-6`)을 사용하거나 `ANTHROPIC_DEFAULT_OPUS_MODEL`과 같은 해당 환경 변수를 설정합니다.

### 모델 설정

다음과 같은 여러 방법으로 모델을 구성할 수 있으며, 우선순위 순서대로 나열되어 있습니다:

1. **세션 중** - `/model <alias|name>`을 사용하여 세션 중에 모델 전환
2. **시작 시** - `claude --model <alias|name>`으로 실행
3. **환경 변수** - `ANTHROPIC_MODEL=<alias|name>` 설정
4. **설정** - `model` 필드를 사용하여 설정 파일에서 영구적으로 구성

사용 예시:

```bash  theme={null}
# Opus로 시작
claude --model opus

# 세션 중에 Sonnet으로 전환
/model sonnet
```

설정 파일 예시:

```json  theme={null}
{
    "permissions": {
        ...
    },
    "model": "opus"
}
```

## 모델 선택 제한

엔터프라이즈 관리자는 [관리 또는 정책 설정](/ko/settings#settings-files)에서 `availableModels`을 사용하여 사용자가 선택할 수 있는 모델을 제한할 수 있습니다.

`availableModels`이 설정되면 사용자는 `/model`, `--model` 플래그, Config 도구 또는 `ANTHROPIC_MODEL` 환경 변수를 통해 목록에 없는 모델로 전환할 수 없습니다.

```json  theme={null}
{
  "availableModels": ["sonnet", "haiku"]
}
```

### 기본 모델 동작

모델 선택기의 Default 옵션은 `availableModels`의 영향을 받지 않습니다. 항상 사용 가능하며 [사용자의 구독 계층을 기반으로 한](#default-model-setting) 시스템의 런타임 기본값을 나타냅니다.

`availableModels: []`인 경우에도 사용자는 자신의 계층에 대한 Default 모델로 Claude Code를 사용할 수 있습니다.

### 사용자가 실행하는 모델 제어

모델 경험을 완전히 제어하려면 `availableModels`과 `model` 설정을 함께 사용합니다:

* **availableModels**: 사용자가 전환할 수 있는 항목을 제한합니다
* **model**: 명시적 모델 재정의를 설정하여 Default보다 우선합니다

이 예시는 모든 사용자가 Sonnet 4.6을 실행하고 Sonnet과 Haiku 중에서만 선택할 수 있도록 합니다:

```json  theme={null}
{
  "model": "sonnet",
  "availableModels": ["sonnet", "haiku"]
}
```

### 병합 동작

`availableModels`이 사용자 설정 및 프로젝트 설정과 같은 여러 수준에서 설정되면 배열이 병합되고 중복이 제거됩니다. 엄격한 허용 목록을 적용하려면 가장 높은 우선순위를 가지는 관리 또는 정책 설정에서 `availableModels`을 설정합니다.

## 특수 모델 동작

### `default` 모델 설정

`default`의 동작은 계정 유형에 따라 다릅니다:

* **Max 및 Team Premium**: Opus 4.6으로 기본값 설정
* **Pro 및 Team Standard**: Sonnet 4.6으로 기본값 설정
* **Enterprise**: Opus 4.6을 사용할 수 있지만 기본값이 아님

Claude Code는 Opus의 사용 임계값에 도달하면 자동으로 Sonnet으로 폴백할 수 있습니다.

### `opusplan` 모델 설정

`opusplan` 모델 별칭은 자동화된 하이브리드 접근 방식을 제공합니다:

* **Plan Mode에서** - 복잡한 추론 및 아키텍처 결정을 위해 `opus` 사용
* **실행 모드에서** - 코드 생성 및 구현을 위해 자동으로 `sonnet`으로 전환

이는 계획을 위한 Opus의 우수한 추론과 실행을 위한 Sonnet의 효율성이라는 두 가지 장점을 모두 제공합니다.

### 노력 수준 조정

[노력 수준](https://platform.claude.com/docs/ko/build-with-claude/effort)은 적응형 추론을 제어하며, 작업 복잡도에 따라 동적으로 사고를 할당합니다. 낮은 노력은 간단한 작업의 경우 더 빠르고 저렴하며, 높은 노력은 복잡한 문제에 대해 더 깊은 추론을 제공합니다.

세 가지 수준이 세션 전체에 유지됩니다: **low**, **medium**, **high**. 네 번째 수준인 **max**는 토큰 지출에 제약이 없어 가장 깊은 추론을 제공하므로 응답이 더 느리고 `high`보다 비용이 더 많이 듭니다. `max`는 Opus 4.6에서만 사용 가능하며 현재 세션에만 적용되고 유지되지 않습니다. Opus 4.6은 Max 및 Team 구독자의 경우 기본적으로 중간 노력으로 설정됩니다.

**노력 수준 설정:**

* **`/effort`**: `/effort low`, `/effort medium`, `/effort high` 또는 `/effort max`를 실행하여 수준을 변경하거나 `/effort auto`를 실행하여 모델 기본값으로 재설정합니다
* **`/model`에서**: 모델을 선택할 때 좌우 화살표 키를 사용하여 노력 슬라이더 조정
* **`--effort` 플래그**: Claude Code를 시작할 때 단일 세션에 대한 수준을 설정하려면 `low`, `medium`, `high` 또는 `max`를 전달합니다
* **환경 변수**: `CLAUDE_CODE_EFFORT_LEVEL`을 `low`, `medium`, `high`, `max` 또는 `auto`로 설정합니다
* **설정**: 설정 파일에서 `effortLevel`을 `"low"`, `"medium"` 또는 `"high"`로 설정합니다

환경 변수가 우선하고, 그 다음 구성된 수준, 그 다음 모델 기본값입니다.

노력은 Opus 4.6 및 Sonnet 4.6에서 지원됩니다. 지원되는 모델이 선택되면 노력 슬라이더가 `/model`에 나타납니다. 현재 노력 수준은 로고 및 스피너 옆에도 표시되므로(예: "with low effort"), `/model`을 열지 않고도 어떤 설정이 활성화되어 있는지 확인할 수 있습니다.

Opus 4.6 및 Sonnet 4.6에서 적응형 추론을 비활성화하고 이전의 고정 사고 예산으로 되돌리려면 `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`을 설정합니다. 비활성화되면 이러한 모델은 `MAX_THINKING_TOKENS`로 제어되는 고정 예산을 사용합니다. [환경 변수](/ko/env-vars)를 참조하세요.

### 확장 컨텍스트

Opus 4.6 및 Sonnet 4.6은 대규모 코드베이스를 사용한 긴 세션을 위해 [100만 토큰 컨텍스트 윈도우](https://platform.claude.com/docs/ko/build-with-claude/context-windows#1m-token-context-window)를 지원합니다.

가용성은 모델 및 플랜에 따라 다릅니다. Max, Team 및 Enterprise 플랜에서 Opus는 추가 구성 없이 자동으로 1M 컨텍스트로 업그레이드됩니다. 이는 Team Standard 및 Team Premium 시트 모두에 적용됩니다.

| 플랜                     | 1M 컨텍스트를 사용하는 Opus 4.6                                                                        | 1M 컨텍스트를 사용하는 Sonnet 4.6                                                                      |
| ---------------------- | --------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Max, Team 및 Enterprise | 구독에 포함됨                                                                                       | [추가 사용](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) 필요 |
| Pro                    | [추가 사용](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) 필요 | [추가 사용](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) 필요 |
| API 및 종량제              | 전체 액세스                                                                                        | 전체 액세스                                                                                        |

1M 컨텍스트를 완전히 비활성화하려면 `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`을 설정합니다. 이는 모델 선택기에서 1M 모델 변형을 제거합니다. [환경 변수](/ko/env-vars)를 참조하세요.

1M 컨텍스트 윈도우는 200K를 초과하는 토큰에 대한 프리미엄 없이 표준 모델 가격을 사용합니다. 확장 컨텍스트가 구독에 포함된 플랜의 경우 사용량은 구독으로 계속 적용됩니다. 추가 사용을 통해 확장 컨텍스트에 액세스하는 플랜의 경우 토큰은 추가 사용으로 청구됩니다.

계정이 1M 컨텍스트를 지원하면 최신 버전의 Claude Code에서 모델 선택기(`/model`)에 옵션이 나타납니다. 표시되지 않으면 세션을 다시 시작해 보세요.

모델 별칭 또는 전체 모델 이름과 함께 `[1m]` 접미사를 사용할 수도 있습니다:

```bash  theme={null}
# opus[1m] 또는 sonnet[1m] 별칭 사용
/model opus[1m]
/model sonnet[1m]

# 또는 전체 모델 이름에 [1m] 추가
/model claude-opus-4-6[1m]
```

## 현재 모델 확인

현재 사용 중인 모델을 여러 방법으로 확인할 수 있습니다:

1. [상태 줄](/ko/statusline)에서(구성된 경우)
2. `/status`에서, 계정 정보도 표시합니다.

## 환경 변수

다음 환경 변수를 사용할 수 있으며, 이는 별칭이 매핑되는 모델 이름을 제어하기 위해 전체 **모델 이름**(또는 API 제공자에 해당하는 이름)이어야 합니다.

| 환경 변수                            | 설명                                                              |
| -------------------------------- | --------------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`   | `opus`에 사용할 모델 또는 Plan Mode가 활성화되었을 때 `opusplan`에 사용할 모델        |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | `sonnet`에 사용할 모델 또는 Plan Mode가 활성화되지 않았을 때 `opusplan`에 사용할 모델   |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`  | `haiku`에 사용할 모델 또는 [백그라운드 기능](/ko/costs#background-token-usage) |
| `CLAUDE_CODE_SUBAGENT_MODEL`     | [subagents](/ko/sub-agents)에 사용할 모델                             |

참고: `ANTHROPIC_SMALL_FAST_MODEL`은 `ANTHROPIC_DEFAULT_HAIKU_MODEL`을 위해 더 이상 사용되지 않습니다.

### 타사 배포를 위한 모델 고정

[Bedrock](/ko/amazon-bedrock), [Vertex AI](/ko/google-vertex-ai) 또는 [Foundry](/ko/microsoft-foundry)를 통해 Claude Code를 배포할 때 사용자에게 롤아웃하기 전에 모델 버전을 고정합니다.

고정하지 않으면 Claude Code는 최신 버전으로 확인되는 모델 별칭(`sonnet`, `opus`, `haiku`)을 사용합니다. Anthropic이 새 모델을 출시할 때 새 버전이 활성화되지 않은 계정의 사용자는 조용히 중단됩니다.

<Warning>
  초기 설정의 일부로 세 가지 모델 환경 변수를 모두 특정 버전 ID로 설정합니다. 이 단계를 건너뛰면 Claude Code 업데이트로 인해 사용자가 아무 조치 없이 중단될 수 있습니다.
</Warning>

제공자에 대한 버전별 모델 ID와 함께 다음 환경 변수를 사용합니다:

| 제공자       | 예시                                                                      |
| :-------- | :---------------------------------------------------------------------- |
| Bedrock   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'` |
| Vertex AI | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'`                 |
| Foundry   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'`                 |

`ANTHROPIC_DEFAULT_SONNET_MODEL` 및 `ANTHROPIC_DEFAULT_HAIKU_MODEL`에 대해 동일한 패턴을 적용합니다. 모든 제공자의 현재 및 레거시 모델 ID는 [모델 개요](https://platform.claude.com/docs/ko/about-claude/models/overview)를 참조하세요. 사용자를 새 모델 버전으로 업그레이드하려면 이러한 환경 변수를 업데이트하고 다시 배포합니다.

고정된 모델에 대해 [확장 컨텍스트](#extended-context)를 활성화하려면 `ANTHROPIC_DEFAULT_OPUS_MODEL` 또는 `ANTHROPIC_DEFAULT_SONNET_MODEL`의 모델 ID에 `[1m]`을 추가합니다:

```bash  theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6[1m]'
```

`[1m]` 접미사는 `opusplan`을 포함한 해당 별칭의 모든 사용에 1M 컨텍스트 윈도우를 적용합니다. Claude Code는 모델 ID를 제공자에게 보내기 전에 접미사를 제거합니다. Opus 4.6 또는 Sonnet 4.6과 같이 기본 모델이 1M 컨텍스트를 지원할 때만 `[1m]`을 추가합니다.

<Note>
  `settings.availableModels` 허용 목록은 타사 제공자를 사용할 때도 적용됩니다. 필터링은 제공자별 모델 ID가 아닌 모델 별칭(`opus`, `sonnet`, `haiku`)과 일치합니다.
</Note>

### 버전별 모델 ID 재정의

위의 패밀리 수준 환경 변수는 패밀리 별칭당 하나의 모델 ID를 구성합니다. 동일한 패밀리 내의 여러 버전을 서로 다른 제공자 ID에 매핑해야 하는 경우 대신 `modelOverrides` 설정을 사용합니다.

`modelOverrides`는 개별 Anthropic 모델 ID를 Claude Code가 제공자의 API에 보내는 제공자별 문자열에 매핑합니다. 사용자가 `/model` 선택기에서 매핑된 모델을 선택하면 Claude Code는 기본 제공 기본값 대신 구성된 값을 사용합니다.

이를 통해 엔터프라이즈 관리자는 거버넌스, 비용 할당 또는 지역 라우팅을 위해 각 모델 버전을 특정 Bedrock 추론 프로필 ARN, Vertex AI 버전 이름 또는 Foundry 배포 이름으로 라우팅할 수 있습니다.

[설정 파일](/ko/settings#settings-files)에서 `modelOverrides`를 설정합니다:

```json  theme={null}
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-sonnet-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/sonnet-prod"
  }
}
```

키는 [모델 개요](https://platform.claude.com/docs/ko/about-claude/models/overview)에 나열된 Anthropic 모델 ID여야 합니다. 날짜가 지정된 모델 ID의 경우 날짜 접미사를 정확히 표시된 대로 포함합니다. 알 수 없는 키는 무시됩니다.

재정의는 `/model` 선택기의 각 항목을 지원하는 기본 제공 모델 ID를 대체합니다. Bedrock에서 재정의는 Claude Code가 시작 시 자동으로 발견하는 모든 추론 프로필보다 우선합니다. `ANTHROPIC_MODEL`, `--model` 또는 `ANTHROPIC_DEFAULT_*_MODEL` 환경 변수를 통해 직접 제공하는 값은 제공자에게 그대로 전달되며 `modelOverrides`로 변환되지 않습니다.

`modelOverrides`는 `availableModels`과 함께 작동합니다. 허용 목록은 재정의 값이 아닌 Anthropic 모델 ID에 대해 평가되므로 `availableModels`의 `"opus"`와 같은 항목은 Opus 버전이 ARN에 매핑되어도 계속 일치합니다.

### Prompt caching 구성

Claude Code는 성능을 최적화하고 비용을 절감하기 위해 [prompt caching](https://platform.claude.com/docs/ko/build-with-claude/prompt-caching)을 자동으로 사용합니다. 전역적으로 또는 특정 모델 계층에 대해 prompt caching을 비활성화할 수 있습니다:

| 환경 변수                           | 설명                                                     |
| ------------------------------- | ------------------------------------------------------ |
| `DISABLE_PROMPT_CACHING`        | 모든 모델에 대해 prompt caching을 비활성화하려면 `1`로 설정(모델별 설정보다 우선) |
| `DISABLE_PROMPT_CACHING_HAIKU`  | Haiku 모델에 대해서만 prompt caching을 비활성화하려면 `1`로 설정         |
| `DISABLE_PROMPT_CACHING_SONNET` | Sonnet 모델에 대해서만 prompt caching을 비활성화하려면 `1`로 설정        |
| `DISABLE_PROMPT_CACHING_OPUS`   | Opus 모델에 대해서만 prompt caching을 비활성화하려면 `1`로 설정          |

이러한 환경 변수는 prompt caching 동작에 대한 세밀한 제어를 제공합니다. 전역 `DISABLE_PROMPT_CACHING` 설정은 모델별 설정보다 우선하므로 필요할 때 모든 캐싱을 빠르게 비활성화할 수 있습니다. 모델별 설정은 특정 모델 디버깅 또는 다양한 캐싱 구현을 가질 수 있는 클라우드 제공자와 작업할 때와 같이 선택적 제어에 유용합니다.
