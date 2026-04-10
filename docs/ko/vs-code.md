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

# VS Code에서 Claude Code 사용하기

> VS Code용 Claude Code 확장 프로그램을 설치하고 구성합니다. 인라인 diff, @-멘션, 계획 검토 및 키보드 단축키를 통해 AI 코딩 지원을 받습니다.

<img src="https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=300652d5678c63905e6b0ea9e50835f8" alt="VS Code 편집기와 오른쪽에 열린 Claude Code 확장 프로그램 패널, Claude와의 대화를 표시" width="2500" height="1155" data-path="images/vs-code-extension-interface.jpg" />

VS Code 확장 프로그램은 Claude Code를 위한 기본 그래픽 인터페이스를 제공하며, IDE에 직접 통합됩니다. 이것이 VS Code에서 Claude Code를 사용하는 권장 방법입니다.

확장 프로그램을 사용하면 Claude의 계획을 수락하기 전에 검토하고 편집할 수 있으며, 편집이 이루어질 때 자동으로 수락하고, 선택 항목에서 특정 줄 범위가 있는 파일을 @-멘션으로 표시하고, 대화 기록에 액세스하고, 별도의 탭이나 창에서 여러 대화를 열 수 있습니다.

## 필수 조건

설치하기 전에 다음을 확인하십시오:

* VS Code 1.98.0 이상
* Anthropic 계정(확장 프로그램을 처음 열 때 로그인합니다). Amazon Bedrock이나 Google Vertex AI와 같은 타사 공급자를 사용하는 경우 대신 [타사 공급자 사용](#use-third-party-providers)을 참조하십시오.

<Tip>
  확장 프로그램에는 CLI(명령줄 인터페이스)가 포함되어 있으며, VS Code의 통합 터미널에서 고급 기능에 액세스할 수 있습니다. 자세한 내용은 [VS Code 확장 프로그램 vs. Claude Code CLI](#vs-code-extension-vs-claude-code-cli)를 참조하십시오.
</Tip>

## 확장 프로그램 설치

IDE에 대한 링크를 클릭하여 직접 설치합니다:

* [VS Code용 설치](vscode:extension/anthropic.claude-code)
* [Cursor용 설치](cursor:extension/anthropic.claude-code)

또는 VS Code에서 `Cmd+Shift+X`(Mac) 또는 `Ctrl+Shift+X`(Windows/Linux)를 눌러 확장 프로그램 보기를 열고, "Claude Code"를 검색한 후 **설치**를 클릭합니다.

<Note>설치 후 확장 프로그램이 나타나지 않으면 VS Code를 다시 시작하거나 명령 팔레트에서 "Developer: Reload Window"를 실행합니다.</Note>

## 시작하기

설치 후 VS Code 인터페이스를 통해 Claude Code를 사용할 수 있습니다:

<Steps>
  <Step title="Claude Code 패널 열기">
    VS Code 전체에서 Spark 아이콘은 Claude Code를 나타냅니다: <img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/vs-code-spark-icon.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=3ca45e00deadec8c8f4b4f807da94505" alt="Spark 아이콘" style={{display: "inline", height: "0.85em", verticalAlign: "middle"}} width="16" height="16" data-path="images/vs-code-spark-icon.svg" />

    Claude를 여는 가장 빠른 방법은 **편집기 도구 모음**(편집기의 오른쪽 위 모서리)에서 Spark 아이콘을 클릭하는 것입니다. 이 아이콘은 파일을 열었을 때만 나타납니다.

        <img src="https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=eb4540325d94664c51776dbbfec4cf02" alt="편집기 도구 모음에서 Spark 아이콘을 표시하는 VS Code 편집기" width="2796" height="734" data-path="images/vs-code-editor-icon.png" />

    Claude Code를 여는 다른 방법:

    * **활동 표시줄**: 왼쪽 사이드바에서 Spark 아이콘을 클릭하여 세션 목록을 엽니다. 세션을 클릭하여 전체 편집기 탭으로 열거나 새 세션을 시작합니다. 이 아이콘은 항상 활동 표시줄에 표시됩니다.
    * **명령 팔레트**: `Cmd+Shift+P`(Mac) 또는 `Ctrl+Shift+P`(Windows/Linux)를 누르고, "Claude Code"를 입력한 후 "새 탭에서 열기"와 같은 옵션을 선택합니다.
    * **상태 표시줄**: 창의 오른쪽 아래 모서리에서 **✱ Claude Code**를 클릭합니다. 파일을 열지 않았을 때도 작동합니다.

    패널을 처음 열 때 **Learn Claude Code** 체크리스트가 나타납니다. **보여주기**를 클릭하여 각 항목을 진행하거나 X로 닫습니다. 나중에 다시 열려면 VS Code 설정의 확장 프로그램 → Claude Code에서 **Hide Onboarding**을 선택 해제합니다.

    Claude 패널을 드래그하여 VS Code의 어느 곳이든 다시 배치할 수 있습니다. 자세한 내용은 [워크플로우 사용자 정의](#customize-your-workflow)를 참조하십시오.
  </Step>

  <Step title="프롬프트 보내기">
    Claude에게 코드나 파일을 도와달라고 요청합니다. 작동 방식 설명, 문제 디버깅 또는 변경 사항 만들기 등이 있습니다.

    <Tip>Claude는 자동으로 선택한 텍스트를 봅니다. `Option+K`(Mac) / `Alt+K`(Windows/Linux)를 눌러 프롬프트에 @-멘션 참조(예: `@file.ts#5-10`)를 삽입합니다.</Tip>

    파일의 특정 줄에 대해 묻는 예시입니다:

        <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-send-prompt.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=ede3ed8d8d5f940e01c5de636d009cfd" alt="Python 파일에서 2-3줄이 선택되고 Claude Code 패널에 @-멘션 참조가 있는 해당 줄에 대한 질문을 표시하는 VS Code 편집기" width="3288" height="1876" data-path="images/vs-code-send-prompt.png" />
  </Step>

  <Step title="변경 사항 검토">
    Claude가 파일을 편집하려고 할 때, 원본과 제안된 변경 사항을 나란히 비교하고 권한을 요청합니다. 수락하거나 거부하거나 Claude에게 대신 수행할 작업을 알릴 수 있습니다.

        <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-edits.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=e005f9b41c541c5c7c59c082f7c4841c" alt="Claude의 제안된 변경 사항의 diff를 표시하고 편집을 수행할지 여부를 묻는 권한 프롬프트가 있는 VS Code" width="3292" height="1876" data-path="images/vs-code-edits.png" />
  </Step>
</Steps>

Claude Code로 수행할 수 있는 작업에 대한 더 많은 아이디어는 [일반적인 워크플로우](/ko/common-workflows)를 참조하십시오.

<Tip>
  명령 팔레트에서 "Claude Code: Open Walkthrough"를 실행하여 기본 사항에 대한 안내 투어를 받습니다.
</Tip>

## 프롬프트 상자 사용

프롬프트 상자는 여러 기능을 지원합니다:

* **권한 모드**: 프롬프트 상자 하단의 모드 표시기를 클릭하여 모드를 전환합니다. 일반 모드에서 Claude는 각 작업 전에 권한을 요청합니다. Plan Mode에서 Claude는 수행할 작업을 설명하고 변경을 수행하기 전에 승인을 기다립니다. VS Code는 자동으로 계획을 전체 markdown 문서로 열어서 Claude가 시작하기 전에 피드백을 제공하기 위해 인라인 주석을 추가할 수 있습니다. 자동 수락 모드에서 Claude는 요청 없이 편집을 수행합니다. VS Code 설정의 `claudeCode.initialPermissionMode`에서 기본값을 설정합니다.
* **명령 메뉴**: `/`를 클릭하거나 입력하여 명령 메뉴를 엽니다. 옵션에는 파일 첨부, 모델 전환, 확장 사고 토글 및 계획 사용량 보기(`/usage`)와 [Remote Control](/ko/remote-control) 세션 시작(`/remote-control`)이 포함됩니다. 사용자 정의 섹션은 MCP 서버, hooks, 메모리, 권한 및 플러그인에 대한 액세스를 제공합니다. 터미널 아이콘이 있는 항목은 통합 터미널에서 열립니다.
* **컨텍스트 표시기**: 프롬프트 상자는 Claude의 context window를 얼마나 사용하고 있는지 표시합니다. Claude는 필요할 때 자동으로 압축하거나 `/compact`를 수동으로 실행할 수 있습니다.
* **확장 사고**: Claude가 복잡한 문제를 추론하는 데 더 많은 시간을 소비할 수 있습니다. 명령 메뉴(`/`)를 통해 켭니다. 자세한 내용은 [확장 사고](/ko/common-workflows#use-extended-thinking-thinking-mode)를 참조하십시오.
* **여러 줄 입력**: `Shift+Enter`를 눌러 보내지 않고 새 줄을 추가합니다. 이것은 질문 대화의 "기타" 자유 텍스트 입력에서도 작동합니다.

### 파일 및 폴더 참조

@-멘션을 사용하여 특정 파일이나 폴더에 대한 컨텍스트를 Claude에게 제공합니다. `@` 다음에 파일 또는 폴더 이름을 입력하면 Claude는 해당 콘텐츠를 읽고 이에 대해 질문하거나 변경할 수 있습니다. Claude Code는 fuzzy matching을 지원하므로 부분 이름을 입력하여 필요한 것을 찾을 수 있습니다:

```text  theme={null}
> Explain the logic in @auth (fuzzy matches auth.js, AuthService.ts, etc.)
> What's in @src/components/ (include a trailing slash for folders)
```

큰 PDF의 경우 Claude에게 전체 파일 대신 특정 페이지를 읽도록 요청할 수 있습니다: 단일 페이지, 1-10페이지와 같은 범위 또는 3페이지 이상과 같은 개방형 범위입니다.

편집기에서 텍스트를 선택하면 Claude는 강조 표시된 코드를 자동으로 볼 수 있습니다. 프롬프트 상자 바닥글은 선택된 줄 수를 표시합니다. `Option+K`(Mac) / `Alt+K`(Windows/Linux)를 눌러 파일 경로 및 줄 번호(예: `@app.ts#5-10`)가 있는 @-멘션을 삽입합니다. 선택 표시기를 클릭하여 Claude가 강조 표시된 텍스트를 볼 수 있는지 여부를 전환합니다. 눈 슬래시 아이콘은 선택이 Claude에서 숨겨져 있음을 의미합니다.

프롬프트 상자에 파일을 드래그할 때 `Shift`를 누르고 있으면 첨부 파일로 추가할 수 있습니다. 첨부 파일의 X를 클릭하여 컨텍스트에서 제거합니다.

### 과거 대화 재개

Claude Code 패널 상단의 드롭다운을 클릭하여 대화 기록에 액세스합니다. 키워드로 검색하거나 시간별로 찾아볼 수 있습니다(오늘, 어제, 지난 7일 등). 대화를 클릭하여 전체 메시지 기록으로 재개합니다. 새 세션은 첫 번째 메시지를 기반으로 AI가 생성한 제목을 받습니다. 세션 위에 마우스를 올려 이름 바꾸기 및 제거 작업을 표시합니다: 설명적인 제목으로 이름을 바꾸거나 목록에서 삭제하려면 제거합니다. 세션 재개에 대한 자세한 내용은 [일반적인 워크플로우](/ko/common-workflows#resume-previous-conversations)를 참조하십시오.

### Claude.ai에서 원격 세션 재개

[웹에서 Claude Code](/ko/claude-code-on-the-web)를 사용하는 경우 VS Code에서 직접 해당 원격 세션을 재개할 수 있습니다. 이를 위해서는 Anthropic Console이 아닌 **Claude.ai Subscription**으로 로그인해야 합니다.

<Steps>
  <Step title="과거 대화 열기">
    Claude Code 패널 상단의 **과거 대화** 드롭다운을 클릭합니다.
  </Step>

  <Step title="원격 탭 선택">
    대화 상자에는 로컬 및 원격의 두 탭이 표시됩니다. **원격**을 클릭하여 claude.ai의 세션을 봅니다.
  </Step>

  <Step title="재개할 세션 선택">
    원격 세션을 찾아보거나 검색합니다. 세션을 클릭하여 다운로드하고 대화를 로컬에서 계속합니다.
  </Step>
</Steps>

<Note>
  원격 탭에는 GitHub 저장소로 시작된 웹 세션만 나타납니다. 재개하면 대화 기록이 로컬로 로드되며, 변경 사항은 claude.ai로 다시 동기화되지 않습니다.
</Note>

## 워크플로우 사용자 정의

실행 중이면 Claude 패널을 다시 배치하거나, 여러 세션을 실행하거나, 터미널 모드로 전환할 수 있습니다.

### Claude가 있는 위치 선택

Claude 패널을 드래그하여 VS Code의 어느 곳이든 다시 배치할 수 있습니다. 패널의 탭이나 제목 표시줄을 잡고 다음으로 드래그합니다:

* **보조 사이드바**: 창의 오른쪽. 코딩하는 동안 Claude를 표시된 상태로 유지합니다.
* **기본 사이드바**: 탐색기, 검색 등의 아이콘이 있는 왼쪽 사이드바입니다.
* **편집기 영역**: Claude를 파일과 함께 탭으로 엽니다. 부수적인 작업에 유용합니다.

<Tip>
  주 Claude 세션에 사이드바를 사용하고 부수적인 작업을 위해 추가 탭을 엽니다. Claude는 선호하는 위치를 기억합니다. 활동 표시줄 세션 목록 아이콘은 Claude 패널과 별개입니다: 세션 목록은 항상 활동 표시줄에 표시되지만 Claude 패널 아이콘은 패널이 왼쪽 사이드바에 도킹되어 있을 때만 나타납니다.
</Tip>

### 여러 대화 실행

명령 팔레트에서 **새 탭에서 열기** 또는 **새 창에서 열기**를 사용하여 추가 대화를 시작합니다. 각 대화는 자체 기록 및 컨텍스트를 유지하므로 다양한 작업을 병렬로 작업할 수 있습니다.

탭을 사용할 때 spark 아이콘의 작은 색상 점은 상태를 나타냅니다: 파란색은 권한 요청이 보류 중임을 의미하고, 주황색은 탭이 숨겨져 있는 동안 Claude가 완료되었음을 의미합니다.

### 터미널 모드로 전환

기본적으로 확장 프로그램은 그래픽 채팅 패널을 엽니다. CLI 스타일 인터페이스를 선호하는 경우 [Use Terminal 설정](vscode://settings/claudeCode.useTerminal)을 열고 상자를 선택합니다.

VS Code 설정(`Cmd+,` Mac 또는 `Ctrl+,` Windows/Linux)을 열고 확장 프로그램 → Claude Code로 이동한 후 **Use Terminal**을 선택할 수도 있습니다.

## 플러그인 관리

VS Code 확장 프로그램에는 [플러그인](/ko/plugins)을 설치하고 관리하기 위한 그래픽 인터페이스가 포함되어 있습니다. 프롬프트 상자에 `/plugins`를 입력하여 **플러그인 관리** 인터페이스를 엽니다.

### 플러그인 설치

플러그인 대화 상자에는 **플러그인** 및 **마켓플레이스**의 두 탭이 표시됩니다.

플러그인 탭에서:

* **설치된 플러그인**은 토글 스위치와 함께 상단에 나타나 활성화 또는 비활성화합니다.
* **구성된 마켓플레이스의 사용 가능한 플러그인**이 아래에 나타납니다.
* 이름 또는 설명으로 플러그인을 필터링하려면 검색합니다.
* 사용 가능한 플러그인에서 **설치**를 클릭합니다.

플러그인을 설치할 때 설치 범위를 선택합니다:

* **사용자용 설치**: 모든 프로젝트에서 사용 가능(사용자 범위)
* **이 프로젝트용 설치**: 프로젝트 협력자와 공유(프로젝트 범위)
* **로컬로 설치**: 이 저장소에서만 사용자용(로컬 범위)

### 마켓플레이스 관리

**마켓플레이스** 탭으로 전환하여 플러그인 소스를 추가하거나 제거합니다:

* GitHub 저장소, URL 또는 로컬 경로를 입력하여 새 마켓플레이스를 추가합니다.
* 새로 고침 아이콘을 클릭하여 마켓플레이스의 플러그인 목록을 업데이트합니다.
* 휴지통 아이콘을 클릭하여 마켓플레이스를 제거합니다.

변경 후 배너가 Claude Code를 다시 시작하여 업데이트를 적용하라는 메시지를 표시합니다.

<Note>
  VS Code의 플러그인 관리는 내부적으로 동일한 CLI 명령을 사용합니다. 확장 프로그램에서 구성한 플러그인 및 마켓플레이스는 CLI에서도 사용 가능하며 그 반대도 마찬가지입니다.
</Note>

플러그인 시스템에 대한 자세한 내용은 [플러그인](/ko/plugins) 및 [플러그인 마켓플레이스](/ko/plugin-marketplaces)를 참조하십시오.

## Chrome으로 브라우저 작업 자동화

Claude를 Chrome 브라우저에 연결하여 웹 앱을 테스트하고, 콘솔 로그로 디버깅하고, VS Code를 떠나지 않고 브라우저 워크플로우를 자동화합니다. 이를 위해서는 [Chrome의 Claude 확장 프로그램](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) 버전 1.0.36 이상이 필요합니다.

프롬프트 상자에 `@browser`를 입력한 후 Claude가 수행할 작업을 입력합니다:

```text  theme={null}
@browser go to localhost:3000 and check the console for errors
```

첨부 메뉴를 열어 새 탭 열기 또는 페이지 콘텐츠 읽기와 같은 특정 브라우저 도구를 선택할 수도 있습니다.

Claude는 브라우저 작업을 위해 새 탭을 열고 브라우저의 로그인 상태를 공유하므로 이미 로그인한 모든 사이트에 액세스할 수 있습니다.

설정 지침, 전체 기능 목록 및 문제 해결은 [Chrome에서 Claude Code 사용](/ko/chrome)을 참조하십시오.

## VS Code 명령 및 단축키

명령 팔레트(`Cmd+Shift+P` Mac 또는 `Ctrl+Shift+P` Windows/Linux)를 열고 "Claude Code"를 입력하여 Claude Code 확장 프로그램에 사용 가능한 모든 VS Code 명령을 봅니다.

일부 단축키는 어느 패널이 "포커스"되어 있는지(키보드 입력을 받는지)에 따라 다릅니다. 커서가 코드 파일에 있으면 편집기가 포커스됩니다. 커서가 Claude의 프롬프트 상자에 있으면 Claude가 포커스됩니다. `Cmd+Esc` / `Ctrl+Esc`를 사용하여 둘 사이를 전환합니다.

<Note>
  이는 확장 프로그램을 제어하기 위한 VS Code 명령입니다. 모든 기본 제공 Claude Code 명령을 확장 프로그램에서 사용할 수 있는 것은 아닙니다. 자세한 내용은 [VS Code 확장 프로그램 vs. Claude Code CLI](#vs-code-extension-vs-claude-code-cli)를 참조하십시오.
</Note>

| 명령                         | 단축키                                                    | 설명                                  |
| -------------------------- | ------------------------------------------------------ | ----------------------------------- |
| Focus Input                | `Cmd+Esc`(Mac) / `Ctrl+Esc`(Windows/Linux)             | 편집기와 Claude 사이의 포커스 전환              |
| Open in Side Bar           | -                                                      | 왼쪽 사이드바에서 Claude 열기                 |
| Open in Terminal           | -                                                      | 터미널 모드에서 Claude 열기                  |
| Open in New Tab            | `Cmd+Shift+Esc`(Mac) / `Ctrl+Shift+Esc`(Windows/Linux) | 편집기 탭으로 새 대화 열기                     |
| Open in New Window         | -                                                      | 별도 창에서 새 대화 열기                      |
| New Conversation           | `Cmd+N`(Mac) / `Ctrl+N`(Windows/Linux)                 | 새 대화 시작(Claude가 포커스되어야 함)           |
| Insert @-Mention Reference | `Option+K`(Mac) / `Alt+K`(Windows/Linux)               | 현재 파일 및 선택에 대한 참조 삽입(편집기가 포커스되어야 함) |
| Show Logs                  | -                                                      | 확장 프로그램 디버그 로그 보기                   |
| Logout                     | -                                                      | Anthropic 계정에서 로그아웃                 |

### 다른 도구에서 VS Code 탭 시작

확장 프로그램은 `vscode://anthropic.claude-code/open`에서 URI 핸들러를 등록합니다. 이를 사용하여 자신의 도구에서 새 Claude Code 탭을 열 수 있습니다: 셸 별칭, 브라우저 북마크렛 또는 URL을 열 수 있는 모든 스크립트입니다. VS Code가 아직 실행 중이 아니면 URL을 열면 먼저 시작됩니다. VS Code가 이미 실행 중이면 URL은 현재 포커스된 창에서 열립니다.

운영 체제의 URL 오프너로 핸들러를 호출합니다. macOS에서:

```bash  theme={null}
open "vscode://anthropic.claude-code/open"
```

Linux에서 `xdg-open`을 사용하거나 Windows에서 `start`를 사용합니다.

핸들러는 두 개의 선택적 쿼리 매개변수를 허용합니다:

| 매개변수      | 설명                                                                                                                                                                                                         |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prompt`  | 프롬프트 상자에 미리 채울 텍스트입니다. URL 인코딩되어야 합니다. 프롬프트는 미리 채워지지만 자동으로 제출되지 않습니다.                                                                                                                                      |
| `session` | 새 대화를 시작하는 대신 재개할 세션 ID입니다. 세션은 VS Code에서 현재 열려 있는 작업 공간에 속해야 합니다. 세션을 찾을 수 없으면 새 대화가 시작됩니다. 세션이 이미 탭에서 열려 있으면 해당 탭이 포커스됩니다. 프로그래밍 방식으로 세션 ID를 캡처하려면 [대화 계속](/ko/headless#continue-conversations)을 참조하십시오. |

예를 들어 "review my changes"로 미리 채워진 탭을 열려면:

```text  theme={null}
vscode://anthropic.claude-code/open?prompt=review%20my%20changes
```

## 설정 구성

확장 프로그램에는 두 가지 유형의 설정이 있습니다:

* **확장 프로그램 설정** VS Code에서: VS Code 내에서 확장 프로그램의 동작을 제어합니다. `Cmd+,`(Mac) 또는 `Ctrl+,`(Windows/Linux)로 열고 확장 프로그램 → Claude Code로 이동합니다. `/`를 입력하고 **General Config**를 선택하여 설정을 열 수도 있습니다.
* **Claude Code 설정** `~/.claude/settings.json`에서: 확장 프로그램과 CLI 간에 공유됩니다. 허용된 명령, 환경 변수, hooks 및 MCP 서버에 사용합니다. 자세한 내용은 [설정](/ko/settings)을 참조하십시오.

<Tip>
  `"$schema": "https://json.schemastore.org/claude-code-settings.json"`을 `settings.json`에 추가하여 VS Code에서 직접 사용 가능한 모든 설정에 대한 자동 완성 및 인라인 유효성 검사를 받습니다.
</Tip>

### 확장 프로그램 설정

| 설정                                | 기본값       | 설명                                                                                                                                                                                                                   |
| --------------------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `selectedModel`                   | `default` | 새 대화를 위한 모델. `/model`로 세션별로 변경합니다.                                                                                                                                                                                   |
| `useTerminal`                     | `false`   | 그래픽 패널 대신 터미널 모드에서 Claude 시작                                                                                                                                                                                         |
| `initialPermissionMode`           | `default` | 새 대화에 대한 승인 프롬프트 제어: `default`, `plan`, `acceptEdits`, `auto` 또는 `bypassPermissions`. [권한 모드](/ko/permission-modes)를 참조하십시오.                                                                                         |
| `preferredLocation`               | `panel`   | Claude가 열리는 위치: `sidebar`(오른쪽) 또는 `panel`(새 탭)                                                                                                                                                                       |
| `autosave`                        | `true`    | Claude가 파일을 읽거나 쓰기 전에 자동 저장                                                                                                                                                                                          |
| `useCtrlEnterToSend`              | `false`   | Enter 대신 Ctrl/Cmd+Enter를 사용하여 프롬프트 보내기                                                                                                                                                                               |
| `enableNewConversationShortcut`   | `true`    | Cmd/Ctrl+N을 사용하여 새 대화 시작 활성화                                                                                                                                                                                         |
| `hideOnboarding`                  | `false`   | 온보딩 체크리스트 숨기기(졸업 모자 아이콘)                                                                                                                                                                                             |
| `respectGitIgnore`                | `true`    | 파일 검색에서 .gitignore 패턴 제외                                                                                                                                                                                             |
| `environmentVariables`            | `[]`      | Claude 프로세스에 대한 환경 변수 설정. 공유 구성을 위해 Claude Code 설정을 대신 사용합니다.                                                                                                                                                        |
| `disableLoginPrompt`              | `false`   | 인증 프롬프트 건너뛰기(타사 공급자 설정용)                                                                                                                                                                                             |
| `allowDangerouslySkipPermissions` | `false`   | [Auto](/ko/permission-modes#eliminate-prompts-with-auto-mode) 및 Bypass 권한을 모드 선택기에 추가합니다. Auto는 Team 플랜과 Claude Sonnet 4.6 또는 Opus 4.6이 필요하므로 이 토글이 켜져 있어도 옵션이 사용 불가능할 수 있습니다. Bypass 권한은 인터넷 액세스가 없는 샌드박스에서만 사용합니다. |
| `claudeProcessWrapper`            | -         | Claude 프로세스를 시작하는 데 사용되는 실행 파일 경로                                                                                                                                                                                    |

## VS Code 확장 프로그램 vs. Claude Code CLI

Claude Code는 VS Code 확장 프로그램(그래픽 패널)과 CLI(터미널의 명령줄 인터페이스) 모두로 사용 가능합니다. 일부 기능은 CLI에서만 사용 가능합니다. CLI 전용 기능이 필요한 경우 VS Code의 통합 터미널에서 `claude`를 실행합니다.

| 기능           | CLI                | VS Code 확장 프로그램                             |
| ------------ | ------------------ | ------------------------------------------- |
| 명령 및 skills  | [모두](/ko/commands) | 부분 집합(`/`를 입력하여 사용 가능한 항목 보기)               |
| MCP 서버 구성    | 예                  | 부분(CLI를 통해 서버 추가; 채팅 패널에서 `/mcp`로 기존 서버 관리) |
| Checkpoints  | 예                  | 예                                           |
| `!` bash 단축키 | 예                  | 아니요                                         |
| Tab 완성       | 예                  | 아니요                                         |

### Checkpoints로 되감기

VS Code 확장 프로그램은 Claude의 파일 편집을 추적하고 이전 상태로 되감을 수 있는 checkpoints를 지원합니다. 메시지 위에 마우스를 올려 되감기 버튼을 표시한 후 세 가지 옵션 중에서 선택합니다:

* **여기서 대화 분기**: 모든 코드 변경 사항을 유지하면서 이 메시지에서 새 대화 분기 시작
* **여기로 코드 되감기**: 전체 대화 기록을 유지하면서 파일 변경 사항을 이 지점으로 되돌리기
* **대화 분기 및 코드 되감기**: 새 대화 분기 시작 및 파일 변경 사항을 이 지점으로 되돌리기

checkpoints 작동 방식 및 제한 사항에 대한 전체 세부 정보는 [Checkpointing](/ko/checkpointing)을 참조하십시오.

### VS Code에서 CLI 실행

VS Code에 머물면서 CLI를 사용하려면 통합 터미널(Windows/Linux에서 `` Ctrl+` `` 또는 Mac에서 `` Cmd+` ``)을 열고 `claude`를 실행합니다. CLI는 diff 보기 및 진단 공유와 같은 기능을 위해 IDE와 자동으로 통합됩니다.

외부 터미널을 사용하는 경우 Claude Code 내에서 `/ide`를 실행하여 VS Code에 연결합니다.

### 확장 프로그램과 CLI 간 전환

확장 프로그램과 CLI는 동일한 대화 기록을 공유합니다. 확장 프로그램 대화를 CLI에서 계속하려면 터미널에서 `claude --resume`을 실행합니다. 이렇게 하면 대화를 검색하고 선택할 수 있는 대화형 선택기가 열립니다.

### 프롬프트에 터미널 출력 포함

`@terminal:name`을 사용하여 프롬프트에서 터미널 출력을 참조합니다. 여기서 `name`은 터미널의 제목입니다. 이를 통해 Claude는 복사 붙여넣기 없이 명령 출력, 오류 메시지 또는 로그를 볼 수 있습니다.

### 백그라운드 프로세스 모니터링

Claude가 장기 실행 명령을 실행할 때 확장 프로그램은 상태 표시줄에 진행 상황을 표시합니다. 그러나 백그라운드 작업의 가시성은 CLI에 비해 제한적입니다. 더 나은 가시성을 위해 Claude가 명령을 출력하도록 하여 VS Code의 통합 터미널에서 실행할 수 있습니다.

### MCP를 사용하여 외부 도구에 연결

MCP(Model Context Protocol) 서버는 Claude에게 외부 도구, 데이터베이스 및 API에 대한 액세스를 제공합니다.

MCP 서버를 추가하려면 통합 터미널(`` Ctrl+` `` 또는 `` Cmd+` ``)을 열고 다음을 실행합니다:

```bash  theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

구성되면 Claude에게 도구를 사용하도록 요청합니다(예: "Review PR #456").

VS Code를 떠나지 않고 MCP 서버를 관리하려면 채팅 패널에 `/mcp`를 입력합니다. MCP 관리 대화 상자를 사용하면 서버를 활성화 또는 비활성화하고, 서버에 다시 연결하고, OAuth 인증을 관리할 수 있습니다. 사용 가능한 서버는 [MCP 문서](/ko/mcp)를 참조하십시오.

## git으로 작업

Claude Code는 git과 통합되어 VS Code에서 직접 버전 제어 워크플로우를 지원합니다. Claude에게 변경 사항을 커밋하거나, 풀 요청을 생성하거나, 분기 간에 작업하도록 요청합니다.

### 커밋 및 풀 요청 생성

Claude는 변경 사항을 스테이징하고, 커밋 메시지를 작성하고, 작업을 기반으로 풀 요청을 생성할 수 있습니다:

```text  theme={null}
> commit my changes with a descriptive message
> create a pr for this feature
> summarize the changes I've made to the auth module
```

풀 요청을 생성할 때 Claude는 실제 코드 변경을 기반으로 설명을 생성하고 테스트 또는 구현 결정에 대한 컨텍스트를 추가할 수 있습니다.

### 병렬 작업을 위해 git worktrees 사용

`--worktree`(`-w`) 플래그를 사용하여 자체 파일 및 분기가 있는 격리된 worktree에서 Claude를 시작합니다:

```bash  theme={null}
claude --worktree feature-auth
```

각 worktree는 git 기록을 공유하면서 독립적인 파일 상태를 유지합니다. 이렇게 하면 Claude 인스턴스가 다양한 작업을 수행할 때 서로 간섭하지 않습니다. 자세한 내용은 [Git worktrees를 사용하여 병렬 Claude Code 세션 실행](/ko/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees)을 참조하십시오.

## 타사 공급자 사용

기본적으로 Claude Code는 Anthropic의 API에 직접 연결됩니다. 조직에서 Amazon Bedrock, Google Vertex AI 또는 Microsoft Foundry를 사용하여 Claude에 액세스하는 경우 대신 공급자를 사용하도록 확장 프로그램을 구성합니다:

<Steps>
  <Step title="로그인 프롬프트 비활성화">
    [로그인 프롬프트 비활성화 설정](vscode://settings/claudeCode.disableLoginPrompt)을 열고 상자를 선택합니다.

    VS Code 설정(`Cmd+,` Mac 또는 `Ctrl+,` Windows/Linux)을 열고 "Claude Code login"을 검색한 후 **로그인 프롬프트 비활성화**를 선택할 수도 있습니다.
  </Step>

  <Step title="공급자 구성">
    공급자에 대한 설정 가이드를 따릅니다:

    * [Amazon Bedrock의 Claude Code](/ko/amazon-bedrock)
    * [Google Vertex AI의 Claude Code](/ko/google-vertex-ai)
    * [Microsoft Foundry의 Claude Code](/ko/microsoft-foundry)

    이 가이드는 `~/.claude/settings.json`에서 공급자를 구성하는 방법을 다루며, 이는 VS Code 확장 프로그램과 CLI 간에 설정이 공유되도록 합니다.
  </Step>
</Steps>

## 보안 및 개인 정보 보호

코드는 비공개로 유지됩니다. Claude Code는 코드를 처리하여 지원을 제공하지만 모델 학습에 사용하지 않습니다. 데이터 처리 및 로깅을 거부하는 방법에 대한 자세한 내용은 [데이터 및 개인 정보 보호](/ko/data-usage)를 참조하십시오.

자동 편집 권한이 활성화되면 Claude Code는 VS Code가 자동으로 실행할 수 있는 VS Code 구성 파일(예: `settings.json` 또는 `tasks.json`)을 수정할 수 있습니다. 신뢰할 수 없는 코드로 작업할 때 위험을 줄이려면:

* 신뢰할 수 없는 작업 공간에 대해 [VS Code 제한 모드](https://code.visualstudio.com/docs/editor/workspace-trust#_restricted-mode)를 활성화합니다.
* 편집에 대해 자동 수락 대신 수동 승인 모드를 사용합니다.
* 수락하기 전에 변경 사항을 주의 깊게 검토합니다.

### 기본 제공 IDE MCP 서버

확장 프로그램이 활성화되면 CLI가 자동으로 연결하는 로컬 MCP 서버를 실행합니다. 이것이 CLI가 VS Code의 기본 diff 뷰어에서 diff를 열고, `@`-멘션에 대한 현재 선택을 읽고, Jupyter 노트북에서 작업할 때 VS Code에 셀을 실행하도록 요청하는 방법입니다.

서버의 이름은 `ide`이며 구성할 것이 없으므로 `/mcp`에서 숨겨져 있습니다. 그러나 조직에서 `PreToolUse` hook을 사용하여 MCP 도구를 허용 목록에 추가하는 경우 이것이 존재한다는 것을 알아야 합니다.

**전송 및 인증.** 서버는 `127.0.0.1`에 바인드되고 임의의 높은 포트에서 다른 머신에서 도달할 수 없습니다. 각 확장 프로그램 활성화는 CLI가 연결하기 위해 제시해야 하는 새로운 임의의 인증 토큰을 생성합니다. 토큰은 `0600` 권한이 있는 `0700` 디렉토리 아래 `~/.claude/ide/`의 잠금 파일에 기록되므로 VS Code를 실행하는 사용자만 읽을 수 있습니다.

**모델에 노출된 도구.** 서버는 약 12개의 도구를 호스팅하지만 모델에만 2개가 표시됩니다. 나머지는 CLI가 자체 UI(diff 열기, 선택 읽기, 파일 저장)에 사용하는 내부 RPC이며 도구 목록이 Claude에 도달하기 전에 필터링됩니다.

| 도구 이름(hooks에서 보이는 대로)      | 수행하는 작업                                                          | 쓰기? |
| -------------------------- | ---------------------------------------------------------------- | --- |
| `mcp__ide__getDiagnostics` | 언어 서버 진단을 반환합니다 — VS Code의 문제 패널의 오류 및 경고. 선택적으로 한 파일로 범위 지정됩니다. | 아니요 |
| `mcp__ide__executeCode`    | 활성 Jupyter 노트북의 커널에서 Python 코드를 실행합니다. 아래 확인 흐름을 참조하십시오.         | 예   |

**Jupyter 실행은 항상 먼저 묻습니다.** `mcp__ide__executeCode`는 아무것도 조용히 실행할 수 없습니다. 각 호출에서 코드는 활성 노트북의 끝에 새 셀로 삽입되고, VS Code는 이를 보기로 스크롤하고, 기본 Quick Pick은 **실행** 또는 **취소**를 요청합니다. 취소하거나 `Esc`로 선택기를 닫으면 Claude에 오류를 반환하고 아무것도 실행되지 않습니다. 도구는 활성 노트북이 없을 때, Jupyter 확장 프로그램(`ms-toolsai.jupyter`)이 설치되지 않았을 때 또는 커널이 Python이 아닐 때 완전히 거부합니다.

<Note>
  Quick Pick 확인은 `PreToolUse` hooks와 별개입니다. `mcp__ide__executeCode`에 대한 허용 목록 항목을 사용하면 Claude가 셀 실행을 *제안*할 수 있습니다. VS Code 내의 Quick Pick은 실제로 *실행*할 수 있게 해줍니다.
</Note>

## 일반적인 문제 해결

### 확장 프로그램이 설치되지 않음

* VS Code의 호환 버전(1.98.0 이상)이 있는지 확인합니다.
* VS Code에 확장 프로그램을 설치할 권한이 있는지 확인합니다.
* [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)에서 직접 설치를 시도합니다.

### Spark 아이콘이 표시되지 않음

Spark 아이콘은 파일을 열었을 때 **편집기 도구 모음**(편집기의 오른쪽 위)에 나타납니다. 표시되지 않으면:

1. **파일 열기**: 아이콘에는 파일을 열어야 합니다. 폴더만 열어서는 충분하지 않습니다.
2. **VS Code 버전 확인**: 1.98.0 이상 필요(도움말 → 정보)
3. **VS Code 다시 시작**: 명령 팔레트에서 "Developer: Reload Window" 실행
4. **충돌하는 확장 프로그램 비활성화**: 다른 AI 확장 프로그램(Cline, Continue 등)을 일시적으로 비활성화합니다.
5. **작업 공간 신뢰 확인**: 확장 프로그램은 제한 모드에서 작동하지 않습니다.

또는 **상태 표시줄**(오른쪽 아래 모서리)에서 "✱ Claude Code"를 클릭합니다. 파일을 열지 않았을 때도 작동합니다. **명령 팔레트**(`Cmd+Shift+P` / `Ctrl+Shift+P`)를 사용하고 "Claude Code"를 입력할 수도 있습니다.

### Claude Code가 응답하지 않음

Claude Code가 프롬프트에 응답하지 않으면:

1. **인터넷 연결 확인**: 안정적인 인터넷 연결이 있는지 확인합니다.
2. **새 대화 시작**: 새 대화를 시작하여 문제가 지속되는지 확인합니다.
3. **CLI 시도**: 터미널에서 `claude`를 실행하여 더 자세한 오류 메시지를 확인합니다.

문제가 지속되면 오류에 대한 세부 정보와 함께 [GitHub에서 문제를 제출합니다](https://github.com/anthropics/claude-code/issues).

## 확장 프로그램 제거

Claude Code 확장 프로그램을 제거하려면:

1. 확장 프로그램 보기 열기(`Cmd+Shift+X` Mac 또는 `Ctrl+Shift+X` Windows/Linux)
2. "Claude Code" 검색
3. **제거** 클릭

확장 프로그램 데이터를 제거하고 모든 설정을 재설정하려면:

```bash  theme={null}
rm -rf ~/.vscode/globalStorage/anthropic.claude-code
```

추가 도움말은 [문제 해결 가이드](/ko/troubleshooting)를 참조하십시오.

## 다음 단계

이제 VS Code에서 Claude Code를 설정했습니다:

* [일반적인 워크플로우 탐색](/ko/common-workflows)하여 Claude Code를 최대한 활용합니다.
* [MCP 서버 설정](/ko/mcp)하여 외부 도구로 Claude의 기능을 확장합니다. CLI를 사용하여 서버를 추가한 후 채팅 패널에서 `/mcp`로 관리합니다.
* [Claude Code 설정 구성](/ko/settings)하여 허용된 명령, hooks 등을 사용자 정의합니다. 이 설정은 확장 프로그램과 CLI 간에 공유됩니다.
