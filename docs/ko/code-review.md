> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Code Review

> 다중 에이전트 분석을 통해 전체 코드베이스를 검토하여 논리 오류, 보안 취약점 및 회귀를 감지하는 자동화된 PR 검토를 설정합니다

<Note>
  Code Review는 연구 미리보기 상태이며 [Teams 및 Enterprise](https://claude.ai/admin-settings/claude-code) 구독에서 사용 가능합니다. [Zero Data Retention](/ko/zero-data-retention)이 활성화된 조직에서는 사용할 수 없습니다.
</Note>

Code Review는 GitHub 풀 요청을 분석하고 문제를 발견한 코드 라인에 인라인 댓글로 결과를 게시합니다. 전문화된 에이전트 집합이 전체 코드베이스의 맥락에서 코드 변경 사항을 검토하여 논리 오류, 보안 취약점, 손상된 엣지 케이스 및 미묘한 회귀를 찾습니다.

결과는 심각도별로 태그가 지정되며 PR을 승인하거나 차단하지 않으므로 기존 검토 워크플로우는 그대로 유지됩니다. 리포지토리에 `CLAUDE.md` 또는 `REVIEW.md` 파일을 추가하여 Claude가 플래그하는 항목을 조정할 수 있습니다.

관리되는 서비스 대신 자신의 CI 인프라에서 Claude를 실행하려면 [GitHub Actions](/ko/github-actions) 또는 [GitLab CI/CD](/ko/gitlab-ci-cd)를 참조하십시오.

이 페이지에서 다루는 내용:

* [검토 작동 방식](#how-reviews-work)
* [설정](#set-up-code-review)
* [`CLAUDE.md` 및 `REVIEW.md`를 사용한 검토 사용자 정의](#customize-reviews)
* [가격](#pricing)

## 검토 작동 방식

관리자가 조직에 대해 Code Review를 [활성화](#set-up-code-review)하면 리포지토리의 구성된 동작에 따라 PR이 열릴 때, 모든 푸시 시 또는 수동으로 요청할 때 검토가 트리거됩니다. PR에서 `@claude review`를 [댓글로 작성](#manually-trigger-reviews)하면 모든 모드에서 검토가 시작됩니다.

검토가 실행되면 여러 에이전트가 Anthropic 인프라에서 병렬로 diff 및 주변 코드를 분석합니다. 각 에이전트는 다른 클래스의 문제를 찾고, 검증 단계에서 후보를 실제 코드 동작과 비교하여 거짓 양성을 필터링합니다. 결과는 중복 제거되고 심각도별로 순위가 지정되며 문제가 발견된 특정 라인에 인라인 댓글로 게시됩니다. 문제가 발견되지 않으면 Claude는 PR에 짧은 확인 댓글을 게시합니다.

검토는 PR 크기 및 복잡도에 따라 비용이 증가하며 평균 20분 내에 완료됩니다. 관리자는 [분석 대시보드](#view-usage)를 통해 검토 활동 및 지출을 모니터링할 수 있습니다.

### 심각도 수준

각 결과는 심각도 수준으로 태그가 지정됩니다:

| 마커 | 심각도          | 의미                             |
| :- | :----------- | :----------------------------- |
| 🔴 | Normal       | 병합 전에 수정해야 하는 버그               |
| 🟡 | Nit          | 경미한 문제, 수정할 가치가 있지만 차단하지는 않음   |
| 🟣 | Pre-existing | 코드베이스에 존재하지만 이 PR에서 도입되지 않은 버그 |

결과에는 확장 가능한 확장 추론 섹션이 포함되어 있으므로 Claude가 문제를 플래그한 이유와 문제를 검증한 방법을 이해할 수 있습니다.

### Code Review가 확인하는 항목

기본적으로 Code Review는 정확성에 중점을 두고 있습니다: 형식 기본 설정이나 누락된 테스트 범위가 아닌 프로덕션을 중단할 버그입니다. 리포지토리에 [지침 파일을 추가](#customize-reviews)하여 확인하는 항목을 확장할 수 있습니다.

## Code Review 설정

관리자는 조직에 대해 한 번 Code Review를 활성화하고 포함할 리포지토리를 선택합니다.

<Steps>
  <Step title="Claude Code 관리자 설정 열기">
    [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code)로 이동하여 Code Review 섹션을 찾습니다. Claude 조직에 대한 관리자 액세스 권한과 GitHub 조직에 GitHub 앱을 설치할 수 있는 권한이 필요합니다.
  </Step>

  <Step title="설정 시작">
    **Setup**을 클릭합니다. 이렇게 하면 GitHub 앱 설치 흐름이 시작됩니다.
  </Step>

  <Step title="Claude GitHub 앱 설치">
    프롬프트를 따라 Claude GitHub 앱을 GitHub 조직에 설치합니다. 앱은 다음 리포지토리 권한을 요청합니다:

    * **Contents**: 읽기 및 쓰기
    * **Issues**: 읽기 및 쓰기
    * **Pull requests**: 읽기 및 쓰기

    Code Review는 콘텐츠에 대한 읽기 액세스와 풀 요청에 대한 쓰기 액세스를 사용합니다. 더 광범위한 권한 집합은 나중에 활성화하는 경우 [GitHub Actions](/ko/github-actions)도 지원합니다.
  </Step>

  <Step title="리포지토리 선택">
    Code Review를 활성화할 리포지토리를 선택합니다. 리포지토리가 보이지 않으면 설치 중에 Claude GitHub 앱에 액세스 권한을 부여했는지 확인하십시오. 나중에 더 많은 리포지토리를 추가할 수 있습니다.
  </Step>

  <Step title="리포지토리별 검토 트리거 설정">
    설정이 완료되면 Code Review 섹션에 리포지토리가 테이블에 표시됩니다. 각 리포지토리에 대해 **Review Behavior** 드롭다운을 사용하여 검토가 실행되는 시기를 선택합니다:

    * **Once after PR creation**: PR이 열리거나 검토 준비 완료로 표시될 때 한 번 검토가 실행됩니다
    * **After every push**: PR 브랜치에 대한 모든 푸시에서 검토가 실행되어 PR이 진화함에 따라 새로운 문제를 감지하고 플래그된 문제를 수정할 때 스레드를 자동으로 해결합니다
    * **Manual**: [PR에서 `@claude review`를 댓글로 작성](#manually-trigger-reviews)할 때만 검토가 시작되며, 그 이후 해당 PR에 대한 푸시는 자동으로 검토됩니다

    모든 푸시에서 검토하면 가장 많은 검토가 실행되고 비용이 가장 많이 듭니다. 수동 모드는 특정 PR을 검토에 옵트인하려는 트래픽이 많은 리포지토리나 PR이 준비될 때까지만 검토를 시작하려는 경우에 유용합니다.
  </Step>
</Steps>

리포지토리 테이블은 최근 활동을 기반으로 각 리포지토리의 평균 검토 비용도 표시합니다. 행 작업 메뉴를 사용하여 리포지토리별로 Code Review를 켜거나 끄거나 리포지토리를 완전히 제거할 수 있습니다.

설정을 확인하려면 테스트 PR을 열어보십시오. 자동 트리거를 선택한 경우 **Claude Code Review**라는 확인 실행이 몇 분 내에 나타납니다. 수동을 선택한 경우 PR에서 `@claude review`를 댓글로 작성하여 첫 번째 검토를 시작합니다. 확인 실행이 나타나지 않으면 리포지토리가 관리자 설정에 나열되어 있고 Claude GitHub 앱이 액세스할 수 있는지 확인하십시오.

## 수동으로 검토 트리거

풀 요청에서 `@claude review`를 댓글로 작성하여 검토를 시작하고 해당 PR을 앞으로 푸시 트리거 검토에 옵트인합니다. 이는 리포지토리의 구성된 트리거와 관계없이 작동합니다: 수동 모드에서 특정 PR을 검토에 옵트인하거나 다른 모드에서 즉시 재검토를 받으려면 이를 사용하십시오. 어느 쪽이든 해당 PR에 대한 푸시는 그 이후로 검토를 트리거합니다.

댓글이 검토를 트리거하려면:

* 최상위 PR 댓글로 게시하고 diff 라인의 인라인 댓글로는 게시하지 않습니다
* 댓글의 시작 부분에 `@claude review`를 입력합니다
* 리포지토리에 대한 소유자, 멤버 또는 협력자 액세스 권한이 있어야 합니다
* PR은 열려 있어야 하며 초안이 아니어야 합니다

해당 PR에서 검토가 이미 실행 중인 경우 요청은 진행 중인 검토가 완료될 때까지 대기열에 추가됩니다. PR의 확인 실행을 통해 진행 상황을 모니터링할 수 있습니다.

## 검토 사용자 정의

Code Review는 리포지토리에서 두 개의 파일을 읽어 플래그할 항목을 안내합니다. 둘 다 기본 정확성 확인 위에 추가됩니다:

* **`CLAUDE.md`**: Claude Code가 검토뿐만 아니라 모든 작업에 사용하는 공유 프로젝트 지침입니다. 지침이 대화형 Claude Code 세션에도 적용될 때 사용하십시오.
* **`REVIEW.md`**: 검토 전용 지침으로 코드 검토 중에만 읽습니다. 플래그하거나 검토 중에 건너뛸 항목에 대한 규칙이 일반 `CLAUDE.md`를 복잡하게 만들 때 사용하십시오.

### CLAUDE.md

Code Review는 리포지토리의 `CLAUDE.md` 파일을 읽고 새로 도입된 위반을 nit 수준 결과로 처리합니다. 이는 양방향으로 작동합니다: PR이 `CLAUDE.md` 문을 오래된 것으로 만드는 방식으로 코드를 변경하면 Claude는 문서도 업데이트해야 한다고 플래그합니다.

Claude는 디렉토리 계층 구조의 모든 수준에서 `CLAUDE.md` 파일을 읽으므로 하위 디렉토리의 `CLAUDE.md`의 규칙은 해당 경로 아래의 파일에만 적용됩니다. `CLAUDE.md` 작동 방식에 대한 자세한 내용은 [메모리 설명서](/ko/memory)를 참조하십시오.

일반 Claude Code 세션에 적용하지 않으려는 검토 전용 지침의 경우 대신 [`REVIEW.md`](#review-md)를 사용하십시오.

### REVIEW\.md

검토 전용 규칙을 위해 리포지토리 루트에 `REVIEW.md` 파일을 추가합니다. 다음을 인코딩하는 데 사용합니다:

* 회사 또는 팀 스타일 가이드라인: "중첩된 조건부보다 조기 반환 선호"
* 린터에서 다루지 않는 언어 또는 프레임워크별 규칙
* Claude가 항상 플래그해야 할 항목: "모든 새 API 경로에는 통합 테스트가 있어야 함"
* Claude가 건너뛸 항목: "생성된 코드 아래 `/gen/`의 형식 지정에 대해 댓글을 달지 마십시오"

`REVIEW.md` 예시:

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

Claude는 리포지토리 루트에서 `REVIEW.md`를 자동으로 검색합니다. 구성이 필요하지 않습니다.

## 사용량 보기

[claude.ai/analytics/code-review](https://claude.ai/analytics/code-review)로 이동하여 조직 전체의 Code Review 활동을 확인합니다. 대시보드는 다음을 표시합니다:

| 섹션                   | 표시 내용                            |
| :------------------- | :------------------------------- |
| PRs reviewed         | 선택한 시간 범위 동안 검토된 풀 요청의 일일 개수     |
| Cost weekly          | Code Review의 주간 지출               |
| Feedback             | 개발자가 문제를 해결하여 자동으로 해결된 검토 댓글의 개수 |
| Repository breakdown | 리포지토리별 검토된 PR 개수 및 해결된 댓글        |

관리자 설정의 리포지토리 테이블은 각 리포지토리의 검토당 평균 비용도 표시합니다.

## 가격

Code Review는 토큰 사용량을 기반으로 청구됩니다. 검토는 평균 \$15-25이며 PR 크기, 코드베이스 복잡도 및 검증이 필요한 문제 수에 따라 확장됩니다. Code Review 사용량은 [추가 사용량](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)을 통해 별도로 청구되며 계획의 포함된 사용량에 포함되지 않습니다.

선택한 검토 트리거는 총 비용에 영향을 미칩니다:

* **Once after PR creation**: PR당 한 번 실행됩니다
* **After every push**: 각 푸시에서 실행되어 푸시 수만큼 비용이 증가합니다
* **Manual**: PR에서 누군가 `@claude review`를 댓글로 작성할 때까지 검토가 없습니다

모든 모드에서 `@claude review`를 [댓글로 작성](#manually-trigger-reviews)하면 PR이 푸시 트리거 검토에 옵트인되므로 해당 댓글 이후 푸시당 추가 비용이 발생합니다.

비용은 조직이 다른 Claude Code 기능에 AWS Bedrock 또는 Google Vertex AI를 사용하는지 여부와 관계없이 Anthropic 청구서에 나타납니다. Code Review의 월간 지출 한도를 설정하려면 [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage)로 이동하여 Claude Code Review 서비스의 한도를 구성합니다.

[분석](#view-usage)의 주간 비용 차트 또는 관리자 설정의 리포지토리별 평균 비용 열을 통해 지출을 모니터링합니다.

## 관련 리소스

Code Review는 Claude Code의 나머지 부분과 함께 작동하도록 설계되었습니다. PR을 열기 전에 로컬에서 검토를 실행하거나, 자체 호스팅 설정이 필요하거나, `CLAUDE.md`가 도구 전체에서 Claude의 동작을 형성하는 방식에 대해 더 깊이 알고 싶다면 다음 페이지가 좋은 다음 단계입니다:

* [Plugins](/ko/discover-plugins): 푸시 전에 로컬에서 온디맨드 검토를 실행하기 위한 `code-review` 플러그인을 포함한 플러그인 마켓플레이스를 찾아봅니다
* [GitHub Actions](/ko/github-actions): 코드 검토 이상의 사용자 정의 자동화를 위해 자신의 GitHub Actions 워크플로우에서 Claude를 실행합니다
* [GitLab CI/CD](/ko/gitlab-ci-cd): GitLab 파이프라인을 위한 자체 호스팅 Claude 통합
* [Memory](/ko/memory): Claude Code 전체에서 `CLAUDE.md` 파일이 작동하는 방식
* [Analytics](/ko/analytics): 코드 검토 이상으로 Claude Code 사용량을 추적합니다
