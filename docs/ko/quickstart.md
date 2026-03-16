> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 빠른 시작

> Claude Code에 오신 것을 환영합니다!

이 빠른 시작 가이드를 통해 몇 분 안에 AI 기반 코딩 지원을 사용할 수 있습니다. 이 가이드를 마치면 일반적인 개발 작업에 Claude Code를 사용하는 방법을 이해하게 됩니다.

## 시작하기 전에

다음을 확인하십시오:

* 열려 있는 터미널 또는 명령 프롬프트
  * 터미널을 처음 사용하는 경우 [터미널 가이드](/ko/terminal-guide)를 확인하십시오
* 작업할 코드 프로젝트
* [Claude 구독](https://claude.com/pricing)(Pro, Max, Teams 또는 Enterprise), [Claude Console](https://console.anthropic.com/) 계정 또는 [지원되는 클라우드 제공자](/ko/third-party-integrations)를 통한 액세스

<Note>
  이 가이드는 터미널 CLI를 다룹니다. Claude Code는 [웹](https://claude.ai/code), [데스크톱 앱](/ko/desktop), [VS Code](/ko/vs-code) 및 [JetBrains IDE](/ko/jetbrains), [Slack](/ko/slack), [GitHub Actions](/ko/github-actions) 및 [GitLab](/ko/gitlab-ci-cd)의 CI/CD에서도 사용할 수 있습니다. [모든 인터페이스](/ko/overview#use-claude-code-everywhere)를 참조하십시오.
</Note>

## 단계 1: Claude Code 설치

To install Claude Code, use one of the following methods:

<Tabs>
  <Tab title="Native Install (Recommended)">
    **macOS, Linux, WSL:**

    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell:**

    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD:**

    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```

    **Windows requires [Git for Windows](https://git-scm.com/downloads/win).** Install it first if you don't have it.

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash  theme={null}
    brew install --cask claude-code
    ```

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` periodically to get the latest features and security fixes.
    </Info>
  </Tab>

  <Tab title="WinGet">
    ```powershell  theme={null}
    winget install Anthropic.ClaudeCode
    ```

    <Info>
      WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
    </Info>
  </Tab>
</Tabs>

## 단계 2: 계정에 로그인

Claude Code를 사용하려면 계정이 필요합니다. `claude` 명령으로 대화형 세션을 시작할 때 로그인해야 합니다:

```bash  theme={null}
claude
# 처음 사용할 때 로그인하라는 메시지가 표시됩니다
```

```bash  theme={null}
/login
# 프롬프트를 따라 계정으로 로그인하십시오
```

다음 계정 유형 중 하나로 로그인할 수 있습니다:

* [Claude Pro, Max, Teams 또는 Enterprise](https://claude.com/pricing)(권장)
* [Claude Console](https://console.anthropic.com/)(선불 크레딧이 있는 API 액세스). 처음 로그인할 때 "Claude Code" 작업 공간이 Console에서 자동으로 생성되어 비용 추적을 중앙화합니다.
* [Amazon Bedrock, Google Vertex AI 또는 Microsoft Foundry](/ko/third-party-integrations)(엔터프라이즈 클라우드 제공자)

로그인하면 자격 증명이 저장되고 다시 로그인할 필요가 없습니다. 나중에 계정을 전환하려면 `/login` 명령을 사용하십시오.

## 단계 3: 첫 번째 세션 시작

프로젝트 디렉토리에서 터미널을 열고 Claude Code를 시작하십시오:

```bash  theme={null}
cd /path/to/your/project
claude
```

세션 정보, 최근 대화 및 최신 업데이트가 포함된 Claude Code 환영 화면이 표시됩니다. 사용 가능한 명령을 보려면 `/help`를 입력하거나 이전 대화를 계속하려면 `/resume`을 입력하십시오.

<Tip>
  로그인(단계 2) 후 자격 증명이 시스템에 저장됩니다. [자격 증명 관리](/ko/authentication#credential-management)에서 자세히 알아보십시오.
</Tip>

## 단계 4: 첫 번째 질문 하기

코드베이스를 이해하는 것부터 시작하겠습니다. 다음 명령 중 하나를 시도하십시오:

```text  theme={null}
이 프로젝트는 무엇을 하나요?
```

Claude가 파일을 분석하고 요약을 제공합니다. 더 구체적인 질문을 할 수도 있습니다:

```text  theme={null}
이 프로젝트는 어떤 기술을 사용하나요?
```

```text  theme={null}
주요 진입점은 어디인가요?
```

```text  theme={null}
폴더 구조를 설명해주세요
```

Claude의 기능에 대해 물어볼 수도 있습니다:

```text  theme={null}
Claude Code는 무엇을 할 수 있나요?
```

```text  theme={null}
Claude Code에서 사용자 정의 skills를 만드는 방법은?
```

```text  theme={null}
Claude Code는 Docker와 함께 작동할 수 있나요?
```

<Note>
  Claude Code는 필요에 따라 프로젝트 파일을 읽습니다. 수동으로 컨텍스트를 추가할 필요가 없습니다.
</Note>

## 단계 5: 첫 번째 코드 변경 수행

이제 Claude Code가 실제 코딩을 하도록 해봅시다. 간단한 작업을 시도하십시오:

```text  theme={null}
주 파일에 hello world 함수 추가
```

Claude Code는 다음을 수행합니다:

1. 적절한 파일 찾기
2. 제안된 변경 사항 표시
3. 승인 요청
4. 편집 수행

<Note>
  Claude Code는 파일을 수정하기 전에 항상 권한을 요청합니다. 개별 변경 사항을 승인하거나 세션에 대해 "모두 수락" 모드를 활성화할 수 있습니다.
</Note>

## 단계 6: Claude Code와 함께 Git 사용

Claude Code는 Git 작업을 대화형으로 만듭니다:

```text  theme={null}
어떤 파일을 변경했나요?
```

```text  theme={null}
설명적인 메시지로 변경 사항 커밋
```

더 복잡한 Git 작업을 요청할 수도 있습니다:

```text  theme={null}
feature/quickstart라는 새 브랜치 생성
```

```text  theme={null}
마지막 5개의 커밋 표시
```

```text  theme={null}
병합 충돌을 해결하는 데 도움을 주세요
```

## 단계 7: 버그 수정 또는 기능 추가

Claude는 디버깅 및 기능 구현에 능숙합니다.

자연어로 원하는 것을 설명하십시오:

```text  theme={null}
사용자 등록 양식에 입력 유효성 검사 추가
```

또는 기존 문제를 수정하십시오:

```text  theme={null}
사용자가 빈 양식을 제출할 수 있는 버그가 있습니다 - 수정하세요
```

Claude Code는 다음을 수행합니다:

* 관련 코드 찾기
* 컨텍스트 이해
* 솔루션 구현
* 사용 가능한 경우 테스트 실행

## 단계 8: 다른 일반적인 워크플로우 시도

Claude와 함께 작업하는 방법은 여러 가지입니다:

**코드 리팩토링**

```text  theme={null}
인증 모듈을 콜백 대신 async/await를 사용하도록 리팩토링
```

**테스트 작성**

```text  theme={null}
계산기 함수에 대한 단위 테스트 작성
```

**문서 업데이트**

```text  theme={null}
설치 지침으로 README 업데이트
```

**코드 검토**

```text  theme={null}
내 변경 사항을 검토하고 개선 사항을 제안해주세요
```

<Tip>
  도움이 되는 동료와 대화하듯이 Claude와 대화하십시오. 달성하고 싶은 것을 설명하면 도움을 드릴 것입니다.
</Tip>

## 필수 명령

일상적인 사용을 위한 가장 중요한 명령은 다음과 같습니다:

| 명령                  | 기능                    | 예시                                  |
| ------------------- | --------------------- | ----------------------------------- |
| `claude`            | 대화형 모드 시작             | `claude`                            |
| `claude "task"`     | 일회성 작업 실행             | `claude "fix the build error"`      |
| `claude -p "query"` | 일회성 쿼리 실행 후 종료        | `claude -p "explain this function"` |
| `claude -c`         | 현재 디렉토리에서 가장 최근 대화 계속 | `claude -c`                         |
| `claude -r`         | 이전 대화 재개              | `claude -r`                         |
| `claude commit`     | Git 커밋 생성             | `claude commit`                     |
| `/clear`            | 대화 기록 지우기             | `/clear`                            |
| `/help`             | 사용 가능한 명령 표시          | `/help`                             |
| `exit` 또는 Ctrl+C    | Claude Code 종료        | `exit`                              |

전체 명령 목록은 [CLI 참조](/ko/cli-reference)를 참조하십시오.

## 초보자를 위한 팁

자세한 내용은 [모범 사례](/ko/best-practices) 및 [일반적인 워크플로우](/ko/common-workflows)를 참조하십시오.

<AccordionGroup>
  <Accordion title="요청을 구체적으로 하기">
    대신: "버그 수정"

    시도: "사용자가 잘못된 자격 증명을 입력한 후 빈 화면을 보는 로그인 버그 수정"
  </Accordion>

  <Accordion title="단계별 지침 사용">
    복잡한 작업을 단계로 나누기:

    ```text  theme={null}
    1. 사용자 프로필을 위한 새 데이터베이스 테이블 생성
    2. 사용자 프로필을 가져오고 업데이트하는 API 엔드포인트 생성
    3. 사용자가 자신의 정보를 보고 편집할 수 있는 웹페이지 구축
    ```
  </Accordion>

  <Accordion title="Claude가 먼저 탐색하도록 하기">
    변경하기 전에 Claude가 코드를 이해하도록 하기:

    ```text  theme={null}
    데이터베이스 스키마 분석
    ```

    ```text  theme={null}
    영국 고객이 가장 자주 반품하는 제품을 보여주는 대시보드 구축
    ```
  </Accordion>

  <Accordion title="바로가기로 시간 절약">
    * `?`를 눌러 사용 가능한 모든 키보드 바로가기 보기
    * 명령 완성을 위해 Tab 사용
    * ↑를 눌러 명령 기록 보기
    * `/`를 입력하여 모든 명령 및 skills 보기
  </Accordion>
</AccordionGroup>

## 다음은?

기본 사항을 배웠으므로 더 고급 기능을 살펴보십시오:

<CardGroup cols={2}>
  <Card title="Claude Code 작동 방식" icon="microchip" href="/ko/how-claude-code-works">
    에이전트 루프, 기본 제공 도구 및 Claude Code가 프로젝트와 상호 작용하는 방식 이해
  </Card>

  <Card title="모범 사례" icon="star" href="/ko/best-practices">
    효과적인 프롬프팅 및 프로젝트 설정으로 더 나은 결과 얻기
  </Card>

  <Card title="일반적인 워크플로우" icon="graduation-cap" href="/ko/common-workflows">
    일반적인 작업에 대한 단계별 가이드
  </Card>

  <Card title="Claude Code 확장" icon="puzzle-piece" href="/ko/features-overview">
    CLAUDE.md, skills, hooks, MCP 등으로 사용자 정의
  </Card>
</CardGroup>

## 도움 받기

* **Claude Code에서**: `/help`를 입력하거나 "어떻게..."를 물어보기
* **문서**: 여기 있습니다! 다른 가이드 찾아보기
* **커뮤니티**: 팁과 지원을 위해 [Discord](https://www.anthropic.com/discord)에 참여하기
