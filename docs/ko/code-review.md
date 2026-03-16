> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Code Review

> 다중 에이전트 분석을 통해 전체 코드베이스를 검토하여 논리 오류, 보안 취약점 및 회귀를 감지하는 자동화된 PR 검토를 설정합니다

<Note>
  Code Review는 연구 미리보기 상태이며 [Teams 및 Enterprise](https://claude.ai/admin-settings/claude-code) 구독에서 사용 가능합니다. [Zero Data Retention](/ko/zero-data-retention)이 활성화된 조직에서는 사용할 수 없습니다.
</Note>

Code Review는 GitHub 풀 요청을 분석하고 문제를 발견한 코드 라인에 인라인 댓글로 결과를 게시합니다. 전문화된 에이전트 집합이 전체 코드베이스의 맥락에서 코드 변경 사항을 검토하여 논리 오류, 보안 취약점, 손상된 엣지 케이스 및 미묘한 회귀를 찾습니다.

결과는 심각도별로 태그가 지정되며 PR을 승인하거나 차단하지 않으므로 기존 검토 워크플로우는 그대로 유지됩니다. 저장소에 `CLAUDE.md` 또는 `REVIEW.md` 파일을 추가하여 Claude가 플래그하는 항목을 조정할 수 있습니다.

관리되는 서비스 대신 자신의 CI 인프라에서 Claude를 실행하려면 [GitHub Actions](/ko/github-actions) 또는 [GitLab CI/CD](/ko/gitlab-ci-cd)를 참조하십시오.

이 페이지에서 다루는 내용:

* [검토 작동 방식](#how-reviews-work)
* [설정](#set-up-code-review)
* [`CLAUDE.md` 및 `REVIEW.md`를 사용한 검토 사용자 정의](#customize-reviews)
* [가격](#pricing)

## 검토 작동 방식

관리자가 조직에 대해 [Code Review를 활성화](#set-up-code-review)하면 풀 요청이 열리거나 업데이트될 때 검토가 자동으로 실행됩니다. 여러 에이전트가 Anthropic 인프라에서 병렬로 diff 및 주변 코드를 분석합니다. 각 에이전트는 다른 클래스의 문제를 찾고, 검증 단계에서 후보를 실제 코드 동작과 비교하여 거짓 양성을 필터링합니다. 결과는 중복 제거되고 심각도별로 순위가 지정되며 문제가 발견된 특정 라인에 인라인 댓글로 게시됩니다. 문제가 발견되지 않으면 Claude는 PR에 짧은 확인 댓글을 게시합니다.

검토는 PR 크기 및 복잡도에 따라 비용이 증가하며 평균 20분 내에 완료됩니다. 관리자는 [분석 대시보드](#view-usage)를 통해 검토 활동 및 지출을 모니터링할 수 있습니다.

### 심각도 수준

각 결과는 심각도 수준으로 태그가 지정됩니다:

| 마커 | 심각도          | 의미                             |
| :- | :----------- | :----------------------------- |
| 🔴 | Normal       | 병합 전에 수정해야 하는 버그               |
| 🟡 | Nit          | 사소한 문제, 수정할 가치가 있지만 차단하지는 않음   |
| 🟣 | Pre-existing | 코드베이스에 존재하지만 이 PR에서 도입되지 않은 버그 |

결과에는 Claude가 문제를 플래그한 이유와 문제를 어떻게 검증했는지 이해하기 위해 확장할 수 있는 축소 가능한 확장 추론 섹션이 포함됩니다.

### Code Review가 확인하는 항목

기본적으로 Code Review는 정확성에 중점을 두고 있습니다: 형식 기본 설정이나 누락된 테스트 범위가 아닌 프로덕션을 중단할 버그입니다. 저장소에 [지침 파일을 추가](#customize-reviews)하여 확인하는 항목을 확장할 수 있습니다.

## Code Review 설정

관리자가 조직에 대해 Code Review를 한 번 활성화하고 포함할 저장소를 선택합니다.

<Steps>
  <Step title="Claude Code 관리자 설정 열기">
    [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code)로 이동하여 Code Review 섹션을 찾습니다. Claude 조직에 대한 관리자 액세스 권한과 GitHub 조직에 GitHub 앱을 설치할 수 있는 권한이 필요합니다.
  </Step>

  <Step title="설정 시작">
    **Setup**을 클릭합니다. 이렇게 하면 GitHub 앱 설치 흐름이 시작됩니다.
  </Step>

  <Step title="Claude GitHub 앱 설치">
    프롬프트를 따라 Claude GitHub 앱을 GitHub 조직에 설치합니다. 앱은 다음 저장소 권한을 요청합니다:

    * **Contents**: 읽기 및 쓰기
    * **Issues**: 읽기 및 쓰기
    * **Pull requests**: 읽기 및 쓰기

    Code Review는 콘텐츠에 대한 읽기 액세스와 풀 요청에 대한 쓰기 액세스를 사용합니다. 더 광범위한 권한 집합은 나중에 활성화하는 경우 [GitHub Actions](/ko/github-actions)도 지원합니다.
  </Step>

  <Step title="저장소 선택">
    Code Review를 활성화할 저장소를 선택합니다. 저장소가 보이지 않으면 설치 중에 Claude GitHub 앱에 액세스 권한을 부여했는지 확인하십시오. 나중에 더 많은 저장소를 추가할 수 있습니다.
  </Step>

  <Step title="저장소별 검토 트리거 설정">
    설정이 완료되면 Code Review 섹션에 저장소가 테이블에 표시됩니다. 각 저장소에 대해 드롭다운을 사용하여 검토가 실행되는 시기를 선택합니다:

    * **After PR creation only**: PR이 열리거나 검토 준비 완료로 표시될 때 한 번 검토가 실행됩니다
    * **After every push to PR branch**: 모든 푸시에서 검토가 실행되어 PR이 진화함에 따라 새로운 문제를 감지하고 플래그된 문제를 수정할 때 스레드를 자동으로 해결합니다

    모든 푸시에서 검토하면 더 많은 검토가 실행되고 비용이 더 많이 듭니다. PR 생성만으로 시작하고 지속적인 범위 적용 및 자동 스레드 정리를 원하는 저장소의 경우 푸시 시로 전환합니다.
  </Step>
</Steps>

저장소 테이블은 또한 최근 활동을 기반으로 각 저장소의 평균 검토 비용을 표시합니다. 행 작업 메뉴를 사용하여 저장소별로 Code Review를 켜거나 끄거나 저장소를 완전히 제거합니다.

설정을 확인하려면 테스트 PR을 열어봅니다. **Claude Code Review**라는 이름의 확인 실행이 몇 분 내에 나타납니다. 나타나지 않으면 저장소가 관리자 설정에 나열되어 있고 Claude GitHub 앱이 액세스할 수 있는지 확인합니다.

## 검토 사용자 정의

Code Review는 저장소에서 두 파일을 읽어 플래그할 항목을 안내합니다. 둘 다 기본 정확성 확인 위에 추가됩니다:

* **`CLAUDE.md`**: Claude Code가 검토뿐만 아니라 모든 작업에 사용하는 공유 프로젝트 지침입니다. 지침이 대화형 Claude Code 세션에도 적용될 때 사용합니다.
* **`REVIEW.md`**: 검토 전용 지침으로 코드 검토 중에만 읽습니다. 검토 중에 플래그하거나 건너뛸 항목에 대한 규칙이 엄격하고 일반 `CLAUDE.md`를 복잡하게 할 규칙에 사용합니다.

### CLAUDE.md

Code Review는 저장소의 `CLAUDE.md` 파일을 읽고 새로 도입된 위반을 nit 수준 결과로 취급합니다. 이는 양방향으로 작동합니다: PR이 `CLAUDE.md` 문을 오래된 것으로 만드는 방식으로 코드를 변경하면 Claude는 문서도 업데이트해야 한다고 플래그합니다.

Claude는 디렉토리 계층의 모든 수준에서 `CLAUDE.md` 파일을 읽으므로 하위 디렉토리의 `CLAUDE.md`의 규칙은 해당 경로 아래의 파일에만 적용됩니다. `CLAUDE.md` 작동 방식에 대한 자세한 내용은 [메모리 설명서](/ko/memory)를 참조하십시오.

일반 Claude Code 세션에 적용하고 싶지 않은 검토 특정 지침의 경우 대신 [`REVIEW.md`](#review-md)를 사용합니다.

### REVIEW\.md

검토 특정 규칙에 대해 저장소 루트에 `REVIEW.md` 파일을 추가합니다. 다음을 인코딩하는 데 사용합니다:

* 회사 또는 팀 스타일 지침: "중첩된 조건부보다 조기 반환 선호"
* 린터로 다루지 않는 언어 또는 프레임워크 특정 규칙
* Claude가 항상 플래그해야 할 항목: "새로운 API 경로에는 통합 테스트가 있어야 함"
* Claude가 건너뛸 항목: "생성된 코드 아래 `/gen/`의 형식 지정에 대해 댓글을 달지 마십시오"

`REVIEW.md` 예:

```markdown  theme={null}
# Code Review Guidelines

## Always check
- New API endpoints have corresponding integration tests
- Database migrations are backward-compatible
- Error messages don't leak internal details to users

## Style
- Prefer `match` statements over chained `isinstance` checks
- Use structured logging, not f-string interpolation in log calls

## Skip
- Generated files under `src/gen/`
- Formatting-only changes in `*.lock` files
```

Claude는 저장소 루트에서 `REVIEW.md`를 자동으로 검색합니다. 구성이 필요하지 않습니다.

## 사용량 보기

[claude.ai/analytics/code-review](https://claude.ai/analytics/code-review)로 이동하여 조직 전체의 Code Review 활동을 확인합니다. 대시보드는 다음을 표시합니다:

| 섹션                   | 표시 내용                                     |
| :------------------- | :---------------------------------------- |
| PRs reviewed         | 선택한 시간 범위 동안 검토된 풀 요청의 일일 개수              |
| Cost weekly          | Code Review의 주간 지출                        |
| Feedback             | 개발자가 플래그된 문제를 해결했기 때문에 자동으로 해결된 검토 댓글의 개수 |
| Repository breakdown | 저장소별 검토된 PR 개수 및 해결된 댓글                   |

관리자 설정의 저장소 테이블은 각 저장소의 검토당 평균 비용도 표시합니다.

## 가격

Code Review는 토큰 사용량을 기반으로 청구됩니다. 검토는 평균 \$15-25이며 PR 크기, 코드베이스 복잡도 및 검증이 필요한 문제 수에 따라 확장됩니다. Code Review 사용량은 [추가 사용량](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)을 통해 별도로 청구되며 계획의 포함된 사용량에 포함되지 않습니다.

선택한 검토 트리거는 총 비용에 영향을 미칩니다:

* **After PR creation only**: PR당 한 번 실행됩니다
* **After every push**: 각 커밋에서 실행되어 푸시 수만큼 비용을 곱합니다

비용은 조직이 다른 Claude Code 기능에 AWS Bedrock 또는 Google Vertex AI를 사용하는지 여부와 관계없이 Anthropic 청구서에 나타납니다. Code Review의 월간 지출 한도를 설정하려면 [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage)로 이동하여 Claude Code Review 서비스의 한도를 구성합니다.

[분석](#view-usage)의 주간 비용 차트 또는 관리자 설정의 저장소별 평균 비용 열을 통해 지출을 모니터링합니다.

## 관련 리소스

Code Review는 Claude Code의 나머지 부분과 함께 작동하도록 설계되었습니다. PR을 열기 전에 로컬에서 검토를 실행하거나, 자체 호스팅 설정이 필요하거나, `CLAUDE.md`가 도구 전체에서 Claude의 동작을 어떻게 형성하는지에 대해 더 깊이 알고 싶다면 다음 페이지가 좋은 다음 단계입니다:

* [Plugins](/ko/discover-plugins): 푸시 전에 로컬에서 온디맨드 검토를 실행하기 위한 `code-review` 플러그인을 포함한 플러그인 마켓플레이스 찾아보기
* [GitHub Actions](/ko/github-actions): 코드 검토 이상의 사용자 정의 자동화를 위해 자신의 GitHub Actions 워크플로우에서 Claude 실행
* [GitLab CI/CD](/ko/gitlab-ci-cd): GitLab 파이프라인을 위한 자체 호스팅 Claude 통합
* [Memory](/ko/memory): Claude Code 전체에서 `CLAUDE.md` 파일이 작동하는 방식
* [Analytics](/ko/analytics): 코드 검토 이상의 Claude Code 사용량 추적
