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

# 웹에서 Claude Code 사용하기

> 안전한 클라우드 인프라에서 Claude Code 작업을 비동기적으로 실행합니다

<Note>
  웹에서 Claude Code는 현재 연구 미리보기 상태입니다.
</Note>

## 웹에서 Claude Code란 무엇입니까?

웹에서 Claude Code를 사용하면 개발자가 Claude 앱에서 Claude Code를 시작할 수 있습니다. 이는 다음과 같은 경우에 완벽합니다:

* **질문에 답변하기**: 코드 아키텍처 및 기능 구현 방식에 대해 질문하기
* **버그 수정 및 일상적인 작업**: 자주 조정할 필요가 없는 잘 정의된 작업
* **병렬 작업**: 여러 버그 수정을 동시에 처리하기
* **로컬 머신에 없는 저장소**: 로컬에 체크아웃하지 않은 코드 작업하기
* **백엔드 변경**: Claude Code가 테스트를 작성한 다음 해당 테스트를 통과하는 코드를 작성할 수 있는 경우

Claude Code는 [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) 및 [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude)용 Claude 앱에서도 사용 가능하므로 이동 중에 작업을 시작하고 진행 중인 작업을 모니터링할 수 있습니다.

`--remote`를 사용하여 [터미널에서 웹으로 새 작업을 시작](#from-terminal-to-web)하거나, [웹 세션을 터미널로 텔레포트](#from-web-to-terminal)하여 로컬에서 계속할 수 있습니다. 클라우드 인프라 대신 자신의 머신에서 Claude Code를 실행하면서 웹 인터페이스를 사용하려면 [Remote Control](/ko/remote-control)을 참조하세요.

## 웹에서 Claude Code를 누가 사용할 수 있습니까?

웹에서 Claude Code는 연구 미리보기로 다음에 사용 가능합니다:

* **Pro 사용자**
* **Max 사용자**
* **Team 사용자**
* **Enterprise 사용자** (프리미엄 시트 또는 Chat + Claude Code 시트 포함)

## 시작하기

브라우저 또는 터미널에서 웹에서 Claude Code를 설정합니다.

### 브라우저에서

1. [claude.ai/code](https://claude.ai/code) 방문
2. GitHub 계정 연결
3. 저장소에 Claude GitHub 앱 설치
4. 기본 환경 선택
5. 코딩 작업 제출
6. diff 보기에서 변경 사항 검토, 주석으로 반복, pull request 생성

### 터미널에서

Claude Code 내에서 `/web-setup`을 실행하여 로컬 `gh` CLI 자격 증명을 사용하여 GitHub를 연결합니다. 이 명령은 `gh auth token`을 웹에서 Claude Code로 동기화하고, 기본 클라우드 환경을 생성하고, 완료되면 브라우저에서 claude.ai/code를 엽니다.

이 경로는 `gh` CLI가 설치되고 `gh auth login`으로 인증되어야 합니다. `gh`를 사용할 수 없으면 `/web-setup`이 claude.ai/code를 열어 브라우저에서 GitHub를 연결할 수 있습니다.

`gh` 자격 증명은 Claude에 복제 및 푸시 액세스를 제공하므로 기본 세션의 경우 GitHub 앱을 건너뛸 수 있습니다. 자동 수정을 원하는 경우 나중에 앱을 설치합니다. 자동 수정은 앱을 사용하여 PR 웹훅을 수신합니다.

<Note>
  Team 및 Enterprise 관리자는 [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code)의 Quick web setup 토글을 사용하여 터미널 설정을 비활성화할 수 있습니다.
</Note>

## 작동 방식

웹에서 Claude Code에서 작업을 시작할 때:

1. **저장소 복제**: 저장소가 Anthropic 관리 가상 머신으로 복제됩니다
2. **환경 설정**: Claude가 코드를 포함한 안전한 클라우드 환경을 준비한 다음 구성된 경우 [설정 스크립트](#setup-scripts)를 실행합니다
3. **네트워크 구성**: 인터넷 액세스는 설정에 따라 구성됩니다
4. **작업 실행**: Claude가 코드를 분석하고, 변경을 수행하고, 테스트를 실행하고, 작업을 확인합니다
5. **완료**: 완료되면 알림을 받고 변경 사항으로 PR을 생성할 수 있습니다
6. **결과**: 변경 사항이 분기로 푸시되어 pull request 생성 준비가 됩니다

## diff 보기로 변경 사항 검토하기

Diff 보기를 사용하면 pull request를 생성하기 전에 Claude가 정확히 무엇을 변경했는지 볼 수 있습니다. GitHub에서 변경 사항을 검토하기 위해 "Create PR"을 클릭하는 대신 앱에서 직접 diff를 보고 변경 사항이 준비될 때까지 Claude와 반복합니다.

Claude가 파일을 변경하면 추가 및 제거된 줄 수를 표시하는 diff 통계 표시기가 나타납니다(예: `+12 -1`). 이 표시기를 선택하여 diff 뷰어를 열면 왼쪽에 파일 목록이 표시되고 오른쪽에 각 파일의 변경 사항이 표시됩니다.

diff 보기에서 다음을 수행할 수 있습니다:

* 파일별로 변경 사항 검토
* 특정 변경 사항에 주석을 달아 수정 요청
* 보이는 내용을 기반으로 Claude와 계속 반복

이를 통해 draft PR을 생성하거나 GitHub로 전환하지 않고도 여러 라운드의 피드백을 통해 변경 사항을 개선할 수 있습니다.

## 자동 수정 pull request

Claude는 pull request를 감시하고 CI 실패 및 검토 주석에 자동으로 응답할 수 있습니다. Claude는 PR의 GitHub 활동을 구독하고, 검사가 실패하거나 검토자가 주석을 남기면 Claude가 조사하고 명확한 수정이 있으면 푸시합니다.

<Note>
  자동 수정을 위해서는 Claude GitHub 앱이 저장소에 설치되어야 합니다. 아직 설치하지 않았으면 [GitHub 앱 페이지](https://github.com/apps/claude)에서 설치하거나 [설정](#getting-started) 중에 메시지가 표시될 때 설치합니다.
</Note>

PR이 어디에서 왔는지와 어떤 기기를 사용하는지에 따라 자동 수정을 켜는 방법은 몇 가지가 있습니다:

* **웹에서 Claude Code로 생성된 PR**: CI 상태 표시줄을 열고 **Auto-fix**를 선택합니다
* **모바일 앱에서**: Claude에 PR을 자동 수정하도록 지시합니다. 예를 들어 "watch this PR and fix any CI failures or review comments"
* **기존 PR**: PR URL을 세션에 붙여넣고 Claude에 자동 수정하도록 지시합니다

### Claude가 PR 활동에 응답하는 방식

자동 수정이 활성화되면 Claude는 새 검토 주석 및 CI 검사 실패를 포함한 PR의 GitHub 이벤트를 수신합니다. 각 이벤트에 대해 Claude는 조사하고 진행 방식을 결정합니다:

* **명확한 수정**: Claude가 수정에 확신하고 이전 지침과 충돌하지 않으면 Claude가 변경을 수행하고, 푸시하고, 세션에서 수행한 작업을 설명합니다
* **모호한 요청**: 검토자의 주석을 여러 방식으로 해석할 수 있거나 아키텍처적으로 중요한 사항이 포함되면 Claude가 행동하기 전에 확인합니다
* **중복 또는 조치 불필요 이벤트**: 이벤트가 중복이거나 변경이 필요 없으면 Claude가 세션에서 이를 기록하고 계속합니다

Claude는 GitHub의 검토 주석 스레드에 회신할 수 있습니다. 이러한 회신은 GitHub 계정을 사용하여 게시되므로 사용자 이름 아래에 나타나지만 각 회신은 Claude Code에서 온 것으로 표시되어 검토자가 에이전트에 의해 작성되었으며 직접 작성되지 않았음을 알 수 있습니다.

<Warning>
  저장소가 Atlantis, Terraform Cloud 또는 `issue_comment` 이벤트에서 실행되는 사용자 정의 GitHub Actions와 같은 주석 트리거 자동화를 사용하는 경우 Claude의 회신이 해당 워크플로우를 트리거할 수 있음을 알아두세요. 자동 수정을 활성화하기 전에 저장소의 자동화를 검토하고 PR 주석이 인프라를 배포하거나 권한 있는 작업을 실행할 수 있는 저장소에서는 자동 수정을 비활성화하는 것을 고려하세요.
</Warning>

## 웹과 터미널 간 작업 이동

터미널에서 웹으로 새 작업을 시작하거나 웹 세션을 터미널로 가져와 로컬에서 계속할 수 있습니다. 웹 세션은 노트북을 닫아도 유지되며 Claude 모바일 앱을 포함한 어디서나 모니터링할 수 있습니다.

<Note>
  세션 핸드오프는 일방향입니다: 웹 세션을 터미널로 가져올 수 있지만 기존 터미널 세션을 웹으로 푸시할 수 없습니다. `--remote` 플래그는 현재 저장소에 대한 *새로운* 웹 세션을 생성합니다.
</Note>

### 터미널에서 웹으로

`--remote` 플래그를 사용하여 명령줄에서 웹 세션을 시작합니다:

```bash  theme={null}
claude --remote "Fix the authentication bug in src/auth/login.ts"
```

이렇게 하면 claude.ai에서 새 웹 세션이 생성됩니다. 작업은 클라우드에서 실행되는 동안 로컬에서 계속 작업할 수 있습니다. `/tasks`를 사용하여 진행 상황을 확인하거나 claude.ai 또는 Claude 모바일 앱에서 세션을 열어 직접 상호 작용합니다. 여기서 Claude를 조종하고, 피드백을 제공하거나, 다른 대화처럼 질문에 답변할 수 있습니다.

#### 원격 작업 팁

**로컬에서 계획하고 원격으로 실행**: 복잡한 작업의 경우 Claude를 Plan Mode에서 시작하여 접근 방식을 협력한 다음 작업을 웹으로 보냅니다:

```bash  theme={null}
claude --permission-mode plan
```

Plan Mode에서 Claude는 파일만 읽고 코드베이스를 탐색할 수 있습니다. 계획에 만족하면 자율 실행을 위해 원격 세션을 시작합니다:

```bash  theme={null}
claude --remote "Execute the migration plan in docs/migration-plan.md"
```

이 패턴은 Claude가 클라우드에서 자율적으로 실행되도록 하면서 전략에 대한 제어를 제공합니다.

**작업을 병렬로 실행**: 각 `--remote` 명령은 독립적으로 실행되는 자체 웹 세션을 생성합니다. 여러 작업을 시작할 수 있으며 모두 별도의 세션에서 동시에 실행됩니다:

```bash  theme={null}
claude --remote "Fix the flaky test in auth.spec.ts"
claude --remote "Update the API documentation"
claude --remote "Refactor the logger to use structured output"
```

`/tasks`로 모든 세션을 모니터링합니다. 세션이 완료되면 웹 인터페이스에서 PR을 생성하거나 [세션을 텔레포트](#from-web-to-terminal)하여 터미널에서 계속 작업할 수 있습니다.

### 웹에서 터미널로

웹 세션을 터미널로 가져오는 방법은 여러 가지입니다:

* **`/teleport` 사용**: Claude Code 내에서 `/teleport`(또는 `/tp`)를 실행하여 웹 세션의 대화형 선택기를 봅니다. 커밋되지 않은 변경 사항이 있으면 먼저 stash하라는 메시지가 표시됩니다.
* **`--teleport` 사용**: 명령줄에서 `claude --teleport`를 실행하여 대화형 세션 선택기를 사용하거나 `claude --teleport <session-id>`를 실행하여 특정 세션을 직접 재개합니다.
* **`/tasks`에서**: `/tasks`를 실행하여 백그라운드 세션을 보고 `t`를 눌러 하나로 텔레포트합니다
* **웹 인터페이스에서**: "Open in CLI"를 클릭하여 터미널에 붙여넣을 수 있는 명령을 복사합니다

세션을 텔레포트하면 Claude가 올바른 저장소에 있는지 확인하고, 원격 세션에서 분기를 가져와 체크아웃하고, 전체 대화 기록을 터미널에 로드합니다.

#### 텔레포트 요구 사항

텔레포트는 세션을 재개하기 전에 이러한 요구 사항을 확인합니다. 요구 사항이 충족되지 않으면 오류가 표시되거나 문제를 해결하라는 메시지가 표시됩니다.

| 요구 사항           | 세부 정보                                                                     |
| --------------- | ------------------------------------------------------------------------- |
| Clean git state | 작업 디렉토리에 커밋되지 않은 변경 사항이 없어야 합니다. 필요한 경우 텔레포트가 변경 사항을 stash하라는 메시지를 표시합니다. |
| 올바른 저장소         | fork가 아닌 동일한 저장소의 체크아웃에서 `--teleport`를 실행해야 합니다.                          |
| 분기 사용 가능        | 웹 세션의 분기가 원격으로 푸시되어야 합니다. 텔레포트가 자동으로 가져와 체크아웃합니다.                         |
| 동일한 계정          | 웹 세션에서 사용한 Claude.ai 계정과 동일한 계정으로 인증되어야 합니다.                              |

### 세션 공유

세션을 공유하려면 아래 계정 유형에 따라 가시성을 전환합니다. 그 후 세션 링크를 그대로 공유합니다. 공유 세션을 열 수 있는 수신자는 로드 시 세션의 최신 상태를 보게 되지만 수신자의 페이지는 실시간으로 업데이트되지 않습니다.

#### Enterprise 또는 Teams 계정에서 공유

Enterprise 및 Teams 계정의 경우 두 가지 가시성 옵션은 **Private** 및 **Team**입니다. Team 가시성은 Claude.ai 조직의 다른 구성원에게 세션을 표시합니다. 저장소 액세스 확인은 기본적으로 수신자의 계정에 연결된 GitHub 계정을 기반으로 활성화됩니다. 계정의 표시 이름은 액세스 권한이 있는 모든 수신자에게 표시됩니다. [Claude in Slack](/ko/slack) 세션은 자동으로 Team 가시성으로 공유됩니다.

#### Max 또는 Pro 계정에서 공유

Max 및 Pro 계정의 경우 두 가지 가시성 옵션은 **Private** 및 **Public**입니다. Public 가시성은 claude.ai에 로그인한 모든 사용자에게 세션을 표시합니다.

공유하기 전에 민감한 내용이 있는지 세션을 확인합니다. 세션에는 개인 GitHub 저장소의 코드 및 자격 증명이 포함될 수 있습니다. 저장소 액세스 확인은 기본적으로 활성화되지 않습니다.

Settings > Claude Code > Sharing settings로 이동하여 저장소 액세스 확인을 활성화하거나 공유 세션에서 이름을 숨길 수 있습니다.

## 반복 작업 예약

Claude를 반복 일정에 따라 실행하여 일일 PR 검토, 종속성 감사 및 CI 실패 분석과 같은 작업을 자동화합니다. 전체 가이드는 [웹에서 작업 예약](/ko/web-scheduled-tasks)을 참조하세요.

## 세션 관리

### 세션 보관

세션을 보관하여 세션 목록을 정리할 수 있습니다. 보관된 세션은 기본 세션 목록에서 숨겨지지만 보관된 세션을 필터링하여 볼 수 있습니다.

세션을 보관하려면 사이드바의 세션 위에 마우스를 올리고 보관 아이콘을 클릭합니다.

### 세션 삭제

세션을 삭제하면 세션과 해당 데이터가 영구적으로 제거됩니다. 이 작업은 실행 취소할 수 없습니다. 두 가지 방법으로 세션을 삭제할 수 있습니다:

* **사이드바에서**: 보관된 세션을 필터링한 다음 삭제할 세션 위에 마우스를 올리고 삭제 아이콘을 클릭합니다
* **세션 메뉴에서**: 세션을 열고 세션 제목 옆의 드롭다운을 클릭한 다음 **Delete**를 선택합니다

세션이 삭제되기 전에 확인하라는 메시지가 표시됩니다.

## 클라우드 환경

### 기본 이미지

일반적인 도구 체인 및 언어 생태계가 사전 설치된 범용 이미지를 구축하고 유지합니다. 이 이미지에는 다음이 포함됩니다:

* 인기 있는 프로그래밍 언어 및 런타임
* 일반적인 빌드 도구 및 패키지 관리자
* 테스트 프레임워크 및 린터

#### 사용 가능한 도구 확인

환경에 사전 설치된 항목을 확인하려면 Claude Code에 다음을 실행하도록 요청합니다:

```bash  theme={null}
check-tools
```

이 명령은 다음을 표시합니다:

* 프로그래밍 언어 및 해당 버전
* 사용 가능한 패키지 관리자
* 설치된 개발 도구

#### 언어별 설정

범용 이미지에는 다음에 대해 사전 구성된 환경이 포함됩니다:

* **Python**: pip, poetry 및 일반적인 과학 라이브러리가 포함된 Python 3.x
* **Node.js**: npm, yarn, pnpm 및 bun이 포함된 최신 LTS 버전
* **Ruby**: 버전 3.1.6, 3.2.6, 3.3.6 (기본값: 3.3.6) (gem, bundler 및 버전 관리용 rbenv 포함)
* **PHP**: 버전 8.4.14
* **Java**: Maven 및 Gradle이 포함된 OpenJDK
* **Go**: 모듈 지원이 포함된 최신 안정 버전
* **Rust**: cargo가 포함된 Rust 도구 체인
* **C++**: GCC 및 Clang 컴파일러

#### 데이터베이스

범용 이미지에는 다음 데이터베이스가 포함됩니다:

* **PostgreSQL**: 버전 16
* **Redis**: 버전 7.0

### 환경 구성

웹에서 Claude Code에서 세션을 시작할 때 내부적으로 다음이 발생합니다:

1. **환경 준비**: 저장소를 복제하고 구성된 [설정 스크립트](#setup-scripts)를 실행합니다. 저장소는 GitHub 저장소의 기본 분기로 복제됩니다. 특정 분기를 체크아웃하려면 프롬프트에서 지정할 수 있습니다.

2. **네트워크 구성**: 에이전트에 대한 인터넷 액세스를 구성합니다. 인터넷 액세스는 기본적으로 제한되지만 필요에 따라 인터넷 액세스가 없거나 전체 인터넷 액세스를 갖도록 환경을 구성할 수 있습니다.

3. **Claude Code 실행**: Claude Code가 실행되어 작업을 완료하고, 코드를 작성하고, 테스트를 실행하고, 작업을 확인합니다. 웹 인터페이스를 통해 세션 전체에서 Claude를 안내하고 조종할 수 있습니다. Claude는 `CLAUDE.md`에서 정의한 컨텍스트를 존중합니다.

4. **결과**: Claude가 작업을 완료하면 분기를 원격으로 푸시합니다. 분기에 대한 PR을 생성할 수 있습니다.

<Note>
  Claude는 환경에서 사용 가능한 터미널 및 CLI 도구를 통해 전적으로 작동합니다. 범용 이미지의 사전 설치된 도구와 hooks 또는 종속성 관리를 통해 설치하는 추가 도구를 사용합니다.
</Note>

**새 환경을 추가하려면:** 현재 환경을 선택하여 환경 선택기를 열고 "Add environment"를 선택합니다. 이렇게 하면 환경 이름, 네트워크 액세스 수준, 환경 변수 및 [설정 스크립트](#setup-scripts)를 지정할 수 있는 대화 상자가 열립니다.

**기존 환경을 업데이트하려면:** 현재 환경을 선택하고 환경 이름의 오른쪽에서 설정 버튼을 선택합니다. 이렇게 하면 환경 이름, 네트워크 액세스, 환경 변수 및 설정 스크립트를 업데이트할 수 있는 대화 상자가 열립니다.

**터미널에서 기본 환경을 선택하려면:** 여러 환경이 구성된 경우 `/remote-env`를 실행하여 `--remote`를 사용하여 터미널에서 웹 세션을 시작할 때 사용할 환경을 선택합니다. 단일 환경의 경우 이 명령은 현재 구성을 표시합니다.

<Note>
  환경 변수는 [`.env` 형식](https://www.dotenv.org/)으로 키-값 쌍으로 지정해야 합니다. 예를 들어:

  ```text  theme={null}
  API_KEY=your_api_key
  DEBUG=true
  ```
</Note>

### 설정 스크립트

설정 스크립트는 새 클라우드 세션이 시작될 때 Claude Code가 시작되기 전에 실행되는 Bash 스크립트입니다. 설정 스크립트를 사용하여 종속성을 설치하고, 도구를 구성하거나, 클라우드 환경이 필요하지만 [기본 이미지](#default-image)에 없는 항목을 준비합니다.

스크립트는 Ubuntu 24.04에서 root로 실행되므로 `apt install` 및 대부분의 언어 패키지 관리자가 작동합니다.

<Tip>
  설정 스크립트에 추가하기 전에 이미 설치된 항목을 확인하려면 Claude에 클라우드 세션에서 `check-tools`를 실행하도록 요청합니다.
</Tip>

설정 스크립트를 추가하려면 환경 설정 대화 상자를 열고 **Setup script** 필드에 스크립트를 입력합니다.

이 예제는 기본 이미지에 없는 `gh` CLI를 설치합니다:

```bash  theme={null}
#!/bin/bash
apt update && apt install -y gh
```

설정 스크립트는 새 세션을 생성할 때만 실행됩니다. 기존 세션을 재개할 때는 건너뜁니다.

스크립트가 0이 아닌 값으로 종료되면 세션이 시작되지 않습니다. 세션을 차단하지 않으려면 중요하지 않은 명령에 `|| true`를 추가합니다.

<Note>
  패키지를 설치하는 설정 스크립트는 레지스트리에 도달하기 위해 네트워크 액세스가 필요합니다. 기본 네트워크 액세스는 npm, PyPI, RubyGems 및 crates.io를 포함한 [일반적인 패키지 레지스트리](#default-allowed-domains)에 대한 연결을 허용합니다. 환경에 네트워크 액세스가 비활성화되어 있으면 스크립트가 패키지 설치에 실패합니다.
</Note>

#### 설정 스크립트 vs. SessionStart hooks

클라우드가 필요하지만 노트북에 이미 있는 것(예: 언어 런타임 또는 CLI 도구)을 설치하려면 설정 스크립트를 사용합니다. 클라우드 및 로컬 모두에서 실행되어야 하는 프로젝트 설정(예: `npm install`)의 경우 [SessionStart hook](/ko/hooks#sessionstart)을 사용합니다.

둘 다 세션 시작 시 실행되지만 다른 위치에 속합니다:

|       | 설정 스크립트                   | SessionStart hooks                    |
| ----- | ------------------------- | ------------------------------------- |
| 첨부 대상 | 클라우드 환경                   | 저장소                                   |
| 구성 위치 | 클라우드 환경 UI                | 저장소의 `.claude/settings.json`          |
| 실행    | Claude Code 시작 전, 새 세션에서만 | Claude Code 시작 후, 재개된 세션을 포함한 모든 세션에서 |
| 범위    | 클라우드 환경만                  | 로컬 및 클라우드 모두                          |

SessionStart hooks는 로컬의 사용자 수준 `~/.claude/settings.json`에서도 정의할 수 있지만 사용자 수준 설정은 클라우드 세션으로 이월되지 않습니다. 클라우드에서는 저장소에 커밋된 hooks만 실행됩니다.

### 종속성 관리

사용자 정의 환경 이미지 및 스냅샷은 아직 지원되지 않습니다. [설정 스크립트](#setup-scripts)를 사용하여 세션이 시작될 때 패키지를 설치하거나 [SessionStart hooks](/ko/hooks#sessionstart)를 사용하여 로컬 환경에서도 실행되어야 하는 종속성 설치를 수행합니다. SessionStart hooks에는 [알려진 제한 사항](#dependency-management-limitations)이 있습니다.

설정 스크립트를 사용하여 자동 종속성 설치를 구성하려면 환경 설정을 열고 스크립트를 추가합니다:

```bash  theme={null}
#!/bin/bash
npm install
pip install -r requirements.txt
```

또는 저장소의 `.claude/settings.json` 파일에서 SessionStart hooks를 사용하여 로컬 환경에서도 실행되어야 하는 종속성 설치를 수행할 수 있습니다:

```json  theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/scripts/install_pkgs.sh"
          }
        ]
      }
    ]
  }
}
```

`scripts/install_pkgs.sh`에서 해당 스크립트를 생성합니다:

```bash  theme={null}
#!/bin/bash

# Only run in remote environments
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

npm install
pip install -r requirements.txt
exit 0
```

실행 가능하게 만듭니다: `chmod +x scripts/install_pkgs.sh`

#### 환경 변수 유지

SessionStart hooks는 `CLAUDE_ENV_FILE` 환경 변수에 지정된 파일에 쓰는 방식으로 후속 Bash 명령에 대한 환경 변수를 유지할 수 있습니다. 자세한 내용은 hooks 참조의 [SessionStart hooks](/ko/hooks#sessionstart)를 참조하세요.

#### 종속성 관리 제한 사항

* **모든 세션에 대해 Hooks 실행**: SessionStart hooks는 로컬 및 원격 환경 모두에서 실행됩니다. 원격 세션에만 hook을 범위 지정하는 hook 구성이 없습니다. 로컬 실행을 건너뛰려면 위에 표시된 대로 스크립트에서 `CLAUDE_CODE_REMOTE` 환경 변수를 확인합니다.
* **네트워크 액세스 필요**: 설치 명령은 패키지 레지스트리에 도달하기 위해 네트워크 액세스가 필요합니다. 환경이 "No internet" 액세스로 구성된 경우 이러한 hooks가 실패합니다. "Limited" (기본값) 또는 "Full" 네트워크 액세스를 사용합니다. [기본 허용 목록](#default-allowed-domains)에는 npm, PyPI, RubyGems 및 crates.io와 같은 일반적인 레지스트리가 포함됩니다.
* **프록시 호환성**: 원격 환경의 모든 아웃바운드 트래픽은 [보안 프록시](#security-proxy)를 통과합니다. 일부 패키지 관리자는 이 프록시에서 제대로 작동하지 않습니다. Bun은 알려진 예입니다.
* **모든 세션 시작 시 실행**: Hooks는 세션이 시작되거나 재개될 때마다 실행되어 시작 지연을 추가합니다. 재설치하기 전에 종속성이 이미 있는지 확인하여 설치 스크립트를 빠르게 유지합니다.

## 네트워크 액세스 및 보안

### 네트워크 정책

#### GitHub 프록시

보안을 위해 모든 GitHub 작업은 모든 git 상호 작용을 투명하게 처리하는 전용 프록시 서비스를 통해 진행됩니다. 샌드박스 내에서 git 클라이언트는 사용자 정의 빌드 범위 자격 증명을 사용하여 인증합니다. 이 프록시는:

* GitHub 인증을 안전하게 관리합니다 - git 클라이언트는 샌드박스 내에서 범위 자격 증명을 사용하며, 프록시가 이를 확인하고 실제 GitHub 인증 토큰으로 변환합니다
* 안전을 위해 git push 작업을 현재 작업 분기로 제한합니다
* 보안 경계를 유지하면서 원활한 복제, 가져오기 및 PR 작업을 활성화합니다

#### 보안 프록시

환경은 보안 및 남용 방지를 위해 HTTP/HTTPS 네트워크 프록시 뒤에서 실행됩니다. 모든 아웃바운드 인터넷 트래픽은 다음을 제공하는 이 프록시를 통과합니다:

* 악의적인 요청으로부터의 보호
* 속도 제한 및 남용 방지
* 향상된 보안을 위한 콘텐츠 필터링

### 액세스 수준

기본적으로 네트워크 액세스는 [허용 목록 도메인](#default-allowed-domains)으로 제한됩니다.

네트워크 액세스 비활성화를 포함한 사용자 정의 네트워크 액세스를 구성할 수 있습니다.

### 기본 허용 도메인

"Limited" 네트워크 액세스를 사용할 때 다음 도메인이 기본적으로 허용됩니다:

#### Anthropic 서비스

* api.anthropic.com
* statsig.anthropic.com
* platform.claude.com
* code.claude.com
* claude.ai

#### 버전 제어

* github.com
* [www.github.com](http://www.github.com)
* api.github.com
* npm.pkg.github.com
* raw\.githubusercontent.com
* pkg-npm.githubusercontent.com
* objects.githubusercontent.com
* codeload.github.com
* avatars.githubusercontent.com
* camo.githubusercontent.com
* gist.github.com
* gitlab.com
* [www.gitlab.com](http://www.gitlab.com)
* registry.gitlab.com
* bitbucket.org
* [www.bitbucket.org](http://www.bitbucket.org)
* api.bitbucket.org

#### 컨테이너 레지스트리

* registry-1.docker.io
* auth.docker.io
* index.docker.io
* hub.docker.com
* [www.docker.com](http://www.docker.com)
* production.cloudflare.docker.com
* download.docker.com
* gcr.io
* \*.gcr.io
* ghcr.io
* mcr.microsoft.com
* \*.data.mcr.microsoft.com
* public.ecr.aws

#### 클라우드 플랫폼

* cloud.google.com
* accounts.google.com
* gcloud.google.com
* \*.googleapis.com
* storage.googleapis.com
* compute.googleapis.com
* container.googleapis.com
* azure.com
* portal.azure.com
* microsoft.com
* [www.microsoft.com](http://www.microsoft.com)
* \*.microsoftonline.com
* packages.microsoft.com
* dotnet.microsoft.com
* dot.net
* visualstudio.com
* dev.azure.com
* \*.amazonaws.com
* \*.api.aws
* oracle.com
* [www.oracle.com](http://www.oracle.com)
* java.com
* [www.java.com](http://www.java.com)
* java.net
* [www.java.net](http://www.java.net)
* download.oracle.com
* yum.oracle.com

#### 패키지 관리자 - JavaScript/Node

* registry.npmjs.org
* [www.npmjs.com](http://www.npmjs.com)
* [www.npmjs.org](http://www.npmjs.org)
* npmjs.com
* npmjs.org
* yarnpkg.com
* registry.yarnpkg.com

#### 패키지 관리자 - Python

* pypi.org
* [www.pypi.org](http://www.pypi.org)
* files.pythonhosted.org
* pythonhosted.org
* test.pypi.org
* pypi.python.org
* pypa.io
* [www.pypa.io](http://www.pypa.io)

#### 패키지 관리자 - Ruby

* rubygems.org
* [www.rubygems.org](http://www.rubygems.org)
* api.rubygems.org
* index.rubygems.org
* ruby-lang.org
* [www.ruby-lang.org](http://www.ruby-lang.org)
* rubyforge.org
* [www.rubyforge.org](http://www.rubyforge.org)
* rubyonrails.org
* [www.rubyonrails.org](http://www.rubyonrails.org)
* rvm.io
* get.rvm.io

#### 패키지 관리자 - Rust

* crates.io
* [www.crates.io](http://www.crates.io)
* index.crates.io
* static.crates.io
* rustup.rs
* static.rust-lang.org
* [www.rust-lang.org](http://www.rust-lang.org)

#### 패키지 관리자 - Go

* proxy.golang.org
* sum.golang.org
* index.golang.org
* golang.org
* [www.golang.org](http://www.golang.org)
* goproxy.io
* pkg.go.dev

#### 패키지 관리자 - JVM

* maven.org
* repo.maven.org
* central.maven.org
* repo1.maven.org
* jcenter.bintray.com
* gradle.org
* [www.gradle.org](http://www.gradle.org)
* services.gradle.org
* plugins.gradle.org
* kotlin.org
* [www.kotlin.org](http://www.kotlin.org)
* spring.io
* repo.spring.io

#### 패키지 관리자 - 기타 언어

* packagist.org (PHP Composer)
* [www.packagist.org](http://www.packagist.org)
* repo.packagist.org
* nuget.org (.NET NuGet)
* [www.nuget.org](http://www.nuget.org)
* api.nuget.org
* pub.dev (Dart/Flutter)
* api.pub.dev
* hex.pm (Elixir/Erlang)
* [www.hex.pm](http://www.hex.pm)
* cpan.org (Perl CPAN)
* [www.cpan.org](http://www.cpan.org)
* metacpan.org
* [www.metacpan.org](http://www.metacpan.org)
* api.metacpan.org
* cocoapods.org (iOS/macOS)
* [www.cocoapods.org](http://www.cocoapods.org)
* cdn.cocoapods.org
* haskell.org
* [www.haskell.org](http://www.haskell.org)
* hackage.haskell.org
* swift.org
* [www.swift.org](http://www.swift.org)

#### Linux 배포판

* archive.ubuntu.com
* security.ubuntu.com
* ubuntu.com
* [www.ubuntu.com](http://www.ubuntu.com)
* \*.ubuntu.com
* ppa.launchpad.net
* launchpad.net
* [www.launchpad.net](http://www.launchpad.net)

#### 개발 도구 및 플랫폼

* dl.k8s.io (Kubernetes)
* pkgs.k8s.io
* k8s.io
* [www.k8s.io](http://www.k8s.io)
* releases.hashicorp.com (HashiCorp)
* apt.releases.hashicorp.com
* rpm.releases.hashicorp.com
* archive.releases.hashicorp.com
* hashicorp.com
* [www.hashicorp.com](http://www.hashicorp.com)
* repo.anaconda.com (Anaconda/Conda)
* conda.anaconda.org
* anaconda.org
* [www.anaconda.com](http://www.anaconda.com)
* anaconda.com
* continuum.io
* apache.org (Apache)
* [www.apache.org](http://www.apache.org)
* archive.apache.org
* downloads.apache.org
* eclipse.org (Eclipse)
* [www.eclipse.org](http://www.eclipse.org)
* download.eclipse.org
* nodejs.org (Node.js)
* [www.nodejs.org](http://www.nodejs.org)

#### 클라우드 서비스 및 모니터링

* statsig.com
* [www.statsig.com](http://www.statsig.com)
* api.statsig.com
* sentry.io
* \*.sentry.io
* http-intake.logs.datadoghq.com
* \*.datadoghq.com
* \*.datadoghq.eu

#### 콘텐츠 전달 및 미러

* sourceforge.net
* \*.sourceforge.net
* packagecloud.io
* \*.packagecloud.io

#### 스키마 및 구성

* json-schema.org
* [www.json-schema.org](http://www.json-schema.org)
* json.schemastore.org
* [www.schemastore.org](http://www.schemastore.org)

#### Model Context Protocol

* \*.modelcontextprotocol.io

<Note>
  `*`로 표시된 도메인은 와일드카드 하위 도메인 일치를 나타냅니다. 예를 들어 `*.gcr.io`는 `gcr.io`의 모든 하위 도메인에 대한 액세스를 허용합니다.
</Note>

### 사용자 정의 네트워크 액세스에 대한 보안 모범 사례

1. **최소 권한 원칙**: 필요한 최소 네트워크 액세스만 활성화합니다
2. **정기적으로 감사**: 허용된 도메인을 정기적으로 검토합니다
3. **HTTPS 사용**: 항상 HTTP 끝점보다 HTTPS 끝점을 선호합니다

## 보안 및 격리

웹에서 Claude Code는 강력한 보안 보장을 제공합니다:

* **격리된 가상 머신**: 각 세션은 격리된 Anthropic 관리 VM에서 실행됩니다
* **네트워크 액세스 제어**: 네트워크 액세스는 기본적으로 제한되며 비활성화할 수 있습니다

<Note>
  네트워크 액세스가 비활성화된 상태에서 실행할 때 Claude Code는 Anthropic API와 통신할 수 있으며, 이는 여전히 격리된 Claude Code VM에서 데이터가 나갈 수 있습니다.
</Note>

* **자격 증명 보호**: 민감한 자격 증명(예: git 자격 증명 또는 서명 키)은 Claude Code가 있는 샌드박스 내부에 없습니다. 인증은 범위 자격 증명을 사용하는 보안 프록시를 통해 처리됩니다
* **안전한 분석**: 코드는 PR을 생성하기 전에 격리된 VM 내에서 분석 및 수정됩니다

## 가격 및 속도 제한

웹에서 Claude Code는 계정 내의 다른 모든 Claude 및 Claude Code 사용과 속도 제한을 공유합니다. 여러 작업을 병렬로 실행하면 비례적으로 더 많은 속도 제한을 소비합니다.

## 제한 사항

* **저장소 인증**: 웹에서 로컬로 세션을 이동할 때 동일한 계정으로 인증된 경우에만 가능합니다
* **플랫폼 제한**: 웹에서 Claude Code는 GitHub에서 호스팅되는 코드에서만 작동합니다. 자체 호스팅 [GitHub Enterprise Server](/ko/github-enterprise-server) 인스턴스는 Teams 및 Enterprise 플랜에서 지원됩니다. GitLab 및 기타 비 GitHub 저장소는 클라우드 세션에서 사용할 수 없습니다

## 모범 사례

1. **환경 설정 자동화**: [설정 스크립트](#setup-scripts)를 사용하여 Claude Code가 시작되기 전에 종속성을 설치하고 도구를 구성합니다. 더 고급 시나리오의 경우 [SessionStart hooks](/ko/hooks#sessionstart)를 구성합니다.
2. **요구 사항 문서화**: `CLAUDE.md` 파일에서 종속성 및 명령을 명확하게 지정합니다. `AGENTS.md` 파일이 있는 경우 `@AGENTS.md`를 사용하여 `CLAUDE.md`에서 소싱하여 단일 정보 소스를 유지할 수 있습니다.

## 관련 리소스

* [Hooks 구성](/ko/hooks)
* [설정 참조](/ko/settings)
* [보안](/ko/security)
* [데이터 사용](/ko/data-usage)
