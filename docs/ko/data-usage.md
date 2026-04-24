> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 데이터 사용

> Anthropic의 Claude 데이터 사용 정책에 대해 알아봅니다

## 데이터 정책

### 데이터 학습 정책

**소비자 사용자(Free, Pro, Max 플랜)**:
향후 Claude 모델 개선을 위해 데이터 사용을 허용할 수 있는 선택권을 제공합니다. 이 설정이 켜져 있을 때 Free, Pro, Max 계정의 데이터를 사용하여 새로운 모델을 학습합니다(이러한 계정에서 Claude Code를 사용할 때 포함).

**상업용 사용자**: (Team 및 Enterprise 플랜, API, 타사 플랫폼, Claude Gov)는 기존 정책을 유지합니다: Anthropic은 상업 약관에 따라 Claude Code로 전송된 코드 또는 프롬프트를 사용하여 생성형 모델을 학습하지 않습니다. 단, 고객이 모델 개선을 위해 데이터를 제공하기로 선택한 경우는 예외입니다(예: [Developer Partner Program](https://support.claude.com/ko/articles/11174108-about-the-development-partner-program)).

### Development Partner Program

[Development Partner Program](https://support.claude.com/ko/articles/11174108-about-the-development-partner-program)을 통해 학습할 자료를 제공하는 방법에 명시적으로 옵트인하는 경우, 제공된 자료를 사용하여 모델을 학습할 수 있습니다. 조직 관리자는 조직에 대해 Development Partner Program에 명시적으로 옵트인할 수 있습니다. 이 프로그램은 Anthropic 자체 API에만 사용 가능하며 Bedrock 또는 Vertex 사용자는 이용할 수 없습니다.

### `/feedback` 명령을 사용한 피드백

`/feedback` 명령을 사용하여 Claude Code에 대한 피드백을 보내기로 선택한 경우, 피드백을 사용하여 제품 및 서비스를 개선할 수 있습니다. `/feedback`을 통해 공유된 대화 기록은 5년 동안 보관됩니다.

### 세션 품질 설문조사

Claude Code에서 "Claude가 이 세션을 어떻게 수행하고 있나요?"라는 메시지가 표시될 때, 이 설문조사에 응답하면("Dismiss" 선택 포함) 숫자 등급(1, 2, 3 또는 dismiss)만 기록됩니다. 이 설문조사의 일부로 대화 기록, 입력, 출력 또는 기타 세션 데이터를 수집하거나 저장하지 않습니다. 엄지손가락 위/아래 피드백이나 `/feedback` 보고서와 달리, 이 세션 품질 설문조사는 간단한 제품 만족도 지표입니다. 이 설문조사에 대한 응답은 데이터 학습 선호도에 영향을 주지 않으며 AI 모델을 학습하는 데 사용될 수 없습니다.

이러한 설문조사를 비활성화하려면 `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1`을 설정합니다. `DISABLE_TELEMETRY` 또는 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`이 설정되면 설문조사도 비활성화됩니다. 빈도를 제어하려면 설정 파일에서 [`feedbackSurveyRate`](/ko/settings#available-settings)를 `0`과 `1` 사이의 확률로 설정합니다.

### 데이터 보관

Anthropic은 계정 유형 및 선호도에 따라 Claude Code 데이터를 보관합니다.

**소비자 사용자(Free, Pro, Max 플랜)**:

* 모델 개선을 위한 데이터 사용을 허용하는 사용자: 모델 개발 및 안전 개선을 지원하기 위한 5년 보관 기간
* 모델 개선을 위한 데이터 사용을 허용하지 않는 사용자: 30일 보관 기간
* 개인정보 보호 설정은 [claude.ai/settings/data-privacy-controls](https://claude.ai/settings/data-privacy-controls)에서 언제든지 변경할 수 있습니다.

**상업용 사용자(Team, Enterprise, API)**:

* 표준: 30일 보관 기간
* [Zero data retention](/ko/zero-data-retention): Claude for Enterprise의 Claude Code에서 사용 가능합니다. ZDR은 조직별로 활성화되며, 각 새로운 조직은 계정 팀에서 별도로 ZDR을 활성화해야 합니다.
* 로컬 캐싱: Claude Code 클라이언트는 세션 재개를 활성화하기 위해 `~/.claude/projects/` 아래의 일반 텍스트로 세션 기록을 로컬에 저장합니다(기본값 30일). `cleanupPeriodDays`로 기간을 조정합니다. 저장되는 내용 및 삭제 방법은 [application data](/ko/claude-directory#application-data)를 참조하세요.

웹에서 개별 Claude Code 세션을 언제든지 삭제할 수 있습니다. 세션을 삭제하면 세션의 이벤트 데이터가 영구적으로 제거됩니다. 세션 삭제 방법에 대한 지침은 [Delete sessions](/ko/claude-code-on-the-web#delete-sessions)를 참조하세요.

[Privacy Center](https://privacy.anthropic.com/)에서 데이터 보관 관행에 대해 자세히 알아보세요.

전체 세부 사항은 [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms)(Team, Enterprise, API 사용자용) 또는 [Consumer Terms](https://www.anthropic.com/legal/consumer-terms)(Free, Pro, Max 사용자용) 및 [Privacy Policy](https://www.anthropic.com/legal/privacy)를 검토하세요.

## 데이터 액세스

모든 자체 플랫폼 사용자의 경우, [로컬 Claude Code](#local-claude-code-data-flow-and-dependencies) 및 [원격 Claude Code](#cloud-execution-data-flow-and-dependencies)에 대해 기록되는 데이터에 대해 자세히 알아볼 수 있습니다. [Remote Control](/ko/remote-control) 세션은 모든 실행이 사용자의 머신에서 발생하므로 로컬 데이터 흐름을 따릅니다. 원격 Claude Code의 경우 Claude는 Claude Code 세션을 시작한 저장소에 액세스합니다. Claude는 연결했지만 세션을 시작하지 않은 저장소에는 액세스하지 않습니다.

## 로컬 Claude Code: 데이터 흐름 및 종속성

아래 다이어그램은 설치 및 정상 작동 중에 Claude Code가 외부 서비스에 어떻게 연결되는지 보여줍니다. 실선은 필수 연결을 나타내고, 점선은 선택적 또는 사용자가 시작한 데이터 흐름을 나타냅니다.

<img src="https://mintcdn.com/claude-code/YcBW2H7CArGcduPb/images/claude-code-data-flow.svg?fit=max&auto=format&n=YcBW2H7CArGcduPb&q=85&s=b600a89f84fc86f9ff7be00a466c0635" alt="Claude Code의 외부 연결을 보여주는 다이어그램: 설치/업데이트는 배포 서버에 연결되고, 사용자 요청은 Console auth, public-api, 그리고 선택적으로 Statsig, Sentry, 버그 보고를 포함한 Anthropic 서비스에 연결됩니다" width="720" height="520" data-path="images/claude-code-data-flow.svg" />

Claude Code는 로컬에서 실행됩니다. LLM과 상호작용하기 위해 Claude Code는 네트워크를 통해 데이터를 전송합니다. 이 데이터에는 모든 사용자 프롬프트 및 모델 출력이 포함되며, TLS 1.2+ 이상을 통해 전송 중에 암호화됩니다. Claude Code는 대부분의 인기 있는 VPN 및 LLM 프록시와 호환됩니다.

저장 시 암호화는 모델 제공자에 따라 달라집니다:

| 제공자                    | 저장 시 암호화                                                                                          |
| ---------------------- | ------------------------------------------------------------------------------------------------- |
| Anthropic API          | 인프라 수준 디스크 암호화(AES-256). [Zero Data Retention](/ko/zero-data-retention)을 활성화하여 서버 측 지속성이 없도록 합니다. |
| Amazon Bedrock         | AWS 관리 키를 사용한 AES-256. AWS KMS를 통해 고객 관리 키를 사용할 수 있습니다.                                           |
| Google Cloud Vertex AI | Google 관리 암호화 키. CMEK를 사용할 수 있습니다.                                                                |
| Microsoft Foundry      | 요청은 AES-256 디스크 암호화를 사용하는 Anthropic 인프라로 라우팅됩니다.                                                  |

Claude Code는 Anthropic의 API를 기반으로 구축되었습니다. API 로깅 절차를 포함한 API 보안 제어에 대한 자세한 내용은 [Anthropic Trust Center](https://trust.anthropic.com)의 규정 준수 아티팩트를 참조하세요.

### 클라우드 실행: 데이터 흐름 및 종속성

[Claude Code on the web](/ko/claude-code-on-the-web)을 사용할 때, 세션은 로컬이 아닌 Anthropic 관리 가상 머신에서 실행됩니다. 클라우드 환경에서:

* **코드 및 데이터 저장소:** 저장소가 격리된 VM으로 복제됩니다. 코드 및 세션 데이터는 계정 유형에 대한 보관 및 사용 정책의 적용을 받습니다(위의 데이터 보관 섹션 참조).
* **자격 증명:** GitHub 인증은 보안 프록시를 통해 처리되며, GitHub 자격 증명은 샌드박스에 절대 입력되지 않습니다.
* **네트워크 트래픽:** 모든 아웃바운드 트래픽은 감사 로깅 및 악용 방지를 위해 보안 프록시를 통해 이동합니다.
* **세션 데이터:** 프롬프트, 코드 변경 및 출력은 로컬 Claude Code 사용과 동일한 데이터 정책을 따릅니다.

클라우드 실행의 보안 세부 사항은 [Security](/ko/security#cloud-execution-security)를 참조하세요.

## 원격 측정 서비스

Claude Code는 사용자의 머신에서 Statsig 서비스에 연결하여 지연 시간, 안정성 및 사용 패턴과 같은 운영 메트릭을 기록합니다. 이 로깅에는 코드 또는 파일 경로가 포함되지 않습니다. 데이터는 TLS를 사용하여 전송 중에 암호화되고 256비트 AES 암호화를 사용하여 저장 시에 암호화됩니다. [Statsig 보안 문서](https://www.statsig.com/trust/security)에서 자세히 알아보세요. Statsig 원격 측정을 거부하려면 `DISABLE_TELEMETRY` 환경 변수를 설정합니다.

Claude Code는 사용자의 머신에서 Sentry에 연결하여 운영 오류 로깅을 수행합니다. 데이터는 TLS를 사용하여 전송 중에 암호화되고 256비트 AES 암호화를 사용하여 저장 시에 암호화됩니다. [Sentry 보안 문서](https://sentry.io/security/)에서 자세히 알아보세요. 오류 로깅을 거부하려면 `DISABLE_ERROR_REPORTING` 환경 변수를 설정합니다.

사용자가 `/feedback` 명령을 실행하면 코드를 포함한 전체 대화 기록의 복사본이 Anthropic으로 전송됩니다. 데이터는 전송 중 TLS를 통해 암호화됩니다. 선택적으로 공개 저장소에 GitHub 이슈가 생성됩니다. 거부하려면 `DISABLE_FEEDBACK_COMMAND` 환경 변수를 `1`로 설정합니다.

## API 제공자별 기본 동작

기본적으로 Bedrock, Vertex 또는 Foundry를 사용할 때 오류 보고, 원격 측정 및 버그 보고가 비활성화됩니다. 세션 품질 설문조사 및 WebFetch 도메인 안전 검사는 예외이며 제공자와 관계없이 실행됩니다. `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`을 설정하여 설문조사를 포함한 모든 필수가 아닌 트래픽을 한 번에 거부할 수 있습니다. 이 변수는 WebFetch 검사에 영향을 주지 않으며, WebFetch 검사는 자체 거부 옵션이 있습니다. 다음은 전체 기본 동작입니다:

| 서비스                             | Claude API                                                                     | Vertex API                                                                     | Bedrock API                                                                    | Foundry API                                                                    |
| ------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| **Statsig (메트릭)**               | 기본 켜짐.<br />`DISABLE_TELEMETRY=1`로 비활성화합니다.                                    | 기본 꺼짐.<br />`CLAUDE_CODE_USE_VERTEX`는 1이어야 합니다.                                | 기본 꺼짐.<br />`CLAUDE_CODE_USE_BEDROCK`은 1이어야 합니다.                               | 기본 꺼짐.<br />`CLAUDE_CODE_USE_FOUNDRY`는 1이어야 합니다.                               |
| **Sentry (오류)**                 | 기본 켜짐.<br />`DISABLE_ERROR_REPORTING=1`로 비활성화합니다.                              | 기본 꺼짐.<br />`CLAUDE_CODE_USE_VERTEX`는 1이어야 합니다.                                | 기본 꺼짐.<br />`CLAUDE_CODE_USE_BEDROCK`은 1이어야 합니다.                               | 기본 꺼짐.<br />`CLAUDE_CODE_USE_FOUNDRY`는 1이어야 합니다.                               |
| **Claude API (`/feedback` 보고)** | 기본 켜짐.<br />`DISABLE_FEEDBACK_COMMAND=1`로 비활성화합니다.                             | 기본 꺼짐.<br />`CLAUDE_CODE_USE_VERTEX`는 1이어야 합니다.                                | 기본 꺼짐.<br />`CLAUDE_CODE_USE_BEDROCK`은 1이어야 합니다.                               | 기본 꺼짐.<br />`CLAUDE_CODE_USE_FOUNDRY`는 1이어야 합니다.                               |
| **세션 품질 설문조사**                  | 기본 켜짐.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1`로 비활성화합니다.                  | 기본 켜짐.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1`로 비활성화합니다.                  | 기본 켜짐.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1`로 비활성화합니다.                  | 기본 켜짐.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1`로 비활성화합니다.                  |
| **WebFetch 도메인 안전 검사**          | 기본 켜짐.<br />[settings](/ko/settings)에서 `skipWebFetchPreflight: true`로 비활성화합니다. | 기본 켜짐.<br />[settings](/ko/settings)에서 `skipWebFetchPreflight: true`로 비활성화합니다. | 기본 켜짐.<br />[settings](/ko/settings)에서 `skipWebFetchPreflight: true`로 비활성화합니다. | 기본 켜짐.<br />[settings](/ko/settings)에서 `skipWebFetchPreflight: true`로 비활성화합니다. |

모든 환경 변수는 `settings.json`에 체크인할 수 있습니다([settings reference](/ko/settings) 참조).

### WebFetch 도메인 안전 검사

URL을 가져오기 전에 WebFetch 도구는 요청된 호스트명을 `api.anthropic.com`으로 전송하여 Anthropic에서 유지 관리하는 안전 차단 목록에 대해 확인합니다. 전체 URL, 경로 또는 페이지 내용이 아닌 호스트명만 전송됩니다. 결과는 호스트명당 5분 동안 캐시됩니다.

이 검사는 사용하는 모델 제공자와 관계없이 실행되며 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`의 영향을 받지 않습니다. 네트워크가 `api.anthropic.com`을 차단하는 경우, WebFetch 요청은 도메인을 허용 목록에 추가하거나 [settings](/ko/settings)에서 `skipWebFetchPreflight: true`를 설정할 때까지 실패합니다. 검사를 비활성화하면 WebFetch가 차단 목록을 참조하지 않고 모든 URL을 검색하려고 시도하므로, Claude가 도달할 수 있는 도메인을 제한해야 하는 경우 [`WebFetch` permission rules](/ko/permissions#webfetch)와 함께 사용합니다.
