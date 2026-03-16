> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 대화형 모드

> Claude Code 세션의 키보드 단축키, 입력 모드 및 대화형 기능에 대한 완전한 참조입니다.

## 키보드 단축키

<Note>
  키보드 단축키는 플랫폼 및 터미널에 따라 다를 수 있습니다. `?`를 눌러 사용자 환경에서 사용 가능한 단축키를 확인하세요.

  **macOS 사용자**: Option/Alt 키 단축키(`Alt+B`, `Alt+F`, `Alt+Y`, `Alt+M`, `Alt+P`)를 사용하려면 터미널에서 Option을 Meta로 구성해야 합니다:

  * **iTerm2**: 설정 → 프로필 → 키 → Left/Right Option 키를 "Esc+"로 설정
  * **Terminal.app**: 설정 → 프로필 → 키보드 → "Option을 Meta 키로 사용" 확인
  * **VS Code**: 설정 → 프로필 → 키 → Left/Right Option 키를 "Esc+"로 설정

  자세한 내용은 [터미널 구성](/ko/terminal-config)을 참조하세요.
</Note>

### 일반 제어

| 단축키                                               | 설명                                  | 컨텍스트                                                        |
| :------------------------------------------------ | :---------------------------------- | :---------------------------------------------------------- |
| `Ctrl+C`                                          | 현재 입력 또는 생성 취소                      | 표준 중단                                                       |
| `Ctrl+F`                                          | 모든 백그라운드 에이전트 종료. 3초 이내에 두 번 누르면 확인 | 백그라운드 에이전트 제어                                               |
| `Ctrl+D`                                          | Claude Code 세션 종료                   | EOF 신호                                                      |
| `Ctrl+G`                                          | 기본 텍스트 편집기에서 열기                     | 기본 텍스트 편집기에서 프롬프트 또는 사용자 정의 응답 편집                           |
| `Ctrl+L`                                          | 터미널 화면 지우기                          | 대화 기록 유지                                                    |
| `Ctrl+O`                                          | 상세 출력 토글                            | 자세한 도구 사용 및 실행 표시                                           |
| `Ctrl+R`                                          | 역방향 검색 명령 기록                        | 이전 명령을 대화형으로 검색                                             |
| `Ctrl+V` 또는 `Cmd+V` (iTerm2) 또는 `Alt+V` (Windows) | 클립보드에서 이미지 붙여넣기                     | 이미지 또는 이미지 파일 경로 붙여넣기                                       |
| `Ctrl+B`                                          | 백그라운드 실행 작업                         | bash 명령 및 에이전트를 백그라운드로 실행. Tmux 사용자는 두 번 누르기                |
| `Ctrl+T`                                          | 작업 목록 토글                            | 터미널 상태 영역에서 [작업 목록](#task-list) 표시 또는 숨기기                   |
| `Left/Right 화살표`                                  | 대화 상자 탭 순환                          | 권한 대화 상자 및 메뉴의 탭 간 탐색                                       |
| `Up/Down 화살표`                                     | 명령 기록 탐색                            | 이전 입력 회상                                                    |
| `Esc` + `Esc`                                     | 되돌리기 또는 요약                          | 코드 및/또는 대화를 이전 지점으로 복원하거나 선택한 메시지에서 요약                      |
| `Shift+Tab` 또는 `Alt+M` (일부 구성)                    | 권한 모드 토글                            | 자동 수락 모드, Plan Mode 및 일반 모드 간 전환.                           |
| `Option+P` (macOS) 또는 `Alt+P` (Windows/Linux)     | 모델 전환                               | 프롬프트를 지우지 않고 모델 전환                                          |
| `Option+T` (macOS) 또는 `Alt+T` (Windows/Linux)     | 확장 사고 토글                            | 확장 사고 모드 활성화 또는 비활성화. 이 단축키를 활성화하려면 먼저 `/terminal-setup` 실행 |

### 텍스트 편집

| 단축키                   | 설명              | 컨텍스트                                                                       |
| :-------------------- | :-------------- | :------------------------------------------------------------------------- |
| `Ctrl+K`              | 줄 끝까지 삭제        | 삭제된 텍스트를 붙여넣기용으로 저장                                                        |
| `Ctrl+U`              | 전체 줄 삭제         | 삭제된 텍스트를 붙여넣기용으로 저장                                                        |
| `Ctrl+Y`              | 삭제된 텍스트 붙여넣기    | `Ctrl+K` 또는 `Ctrl+U`로 삭제한 텍스트 붙여넣기                                         |
| `Alt+Y` (`Ctrl+Y` 이후) | 붙여넣기 기록 순환      | 붙여넣은 후 이전에 삭제한 텍스트를 순환합니다. macOS에서 [Option을 Meta로](#keyboard-shortcuts) 필요 |
| `Alt+B`               | 커서를 한 단어 뒤로 이동  | 단어 탐색. macOS에서 [Option을 Meta로](#keyboard-shortcuts) 필요                     |
| `Alt+F`               | 커서를 한 단어 앞으로 이동 | 단어 탐색. macOS에서 [Option을 Meta로](#keyboard-shortcuts) 필요                     |

### 테마 및 표시

| 단축키      | 설명              | 컨텍스트                                                                |
| :------- | :-------------- | :------------------------------------------------------------------ |
| `Ctrl+T` | 코드 블록의 구문 강조 토글 | `/theme` 선택기 메뉴 내에서만 작동합니다. Claude의 응답에서 코드가 구문 색상을 사용하는지 여부를 제어합니다 |

<Note>
  구문 강조는 Claude Code의 네이티브 빌드에서만 사용 가능합니다.
</Note>

### 여러 줄 입력

| 방법          | 단축키            | 컨텍스트                                       |
| :---------- | :------------- | :----------------------------------------- |
| 빠른 이스케이프    | `\` + `Enter`  | 모든 터미널에서 작동                                |
| macOS 기본값   | `Option+Enter` | macOS의 기본값                                 |
| Shift+Enter | `Shift+Enter`  | iTerm2, WezTerm, Ghostty, Kitty에서 기본적으로 작동 |
| 제어 시퀀스      | `Ctrl+J`       | 여러 줄의 라인 피드 문자                             |
| 붙여넣기 모드     | 직접 붙여넣기        | 코드 블록, 로그의 경우                              |

<Tip>
  Shift+Enter는 iTerm2, WezTerm, Ghostty 및 Kitty에서 구성 없이 작동합니다. 다른 터미널(VS Code, Alacritty, Zed, Warp)의 경우 `/terminal-setup`을 실행하여 바인딩을 설치하세요.
</Tip>

### 빠른 명령

| 단축키    | 설명          | 참고                                                       |
| :----- | :---------- | :------------------------------------------------------- |
| `/` 시작 | 명령 또는 skill | [기본 제공 명령](#built-in-commands) 및 [skills](/ko/skills) 참조 |
| `!` 시작 | Bash 모드     | 명령을 직접 실행하고 실행 출력을 세션에 추가                                |
| `@`    | 파일 경로 언급    | 파일 경로 자동 완성 트리거                                          |

## 기본 제공 명령

Claude Code에서 `/`를 입력하여 사용 가능한 모든 명령을 보거나, `/` 다음에 문자를 입력하여 필터링하세요. 모든 명령이 모든 사용자에게 표시되지는 않습니다. 일부는 플랫폼, 요금제 또는 환경에 따라 다릅니다. 예를 들어, `/desktop`은 macOS 및 Windows에서만 나타나고, `/upgrade` 및 `/privacy-settings`는 Pro 및 Max 요금제에서만 사용 가능하며, `/terminal-setup`은 터미널이 기본적으로 키바인딩을 지원할 때 숨겨집니다.

Claude Code는 또한 `/`를 입력할 때 기본 제공 명령과 함께 나타나는 `/simplify`, `/batch` 및 `/debug`와 같은 [번들 skills](/ko/skills#bundled-skills)와 함께 제공됩니다. 자신의 명령을 만들려면 [skills](/ko/skills)를 참조하세요.

아래 표에서 `<arg>`는 필수 인수를 나타내고 `[arg]`는 선택적 인수를 나타냅니다.

| 명령                        | 목적                                                                                                                                                                                             |
| :------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/add-dir <path>`         | 현재 세션에 새 작업 디렉토리 추가                                                                                                                                                                            |
| `/agents`                 | [agent](/ko/sub-agents) 구성 관리                                                                                                                                                                  |
| `/btw <question>`         | 대화에 추가하지 않고 빠른 [부가 질문](#side-questions-with-%2Fbtw) 하기                                                                                                                                         |
| `/chrome`                 | [Chrome의 Claude](/ko/chrome) 설정 구성                                                                                                                                                             |
| `/clear`                  | 대화 기록을 지우고 컨텍스트 해제. 별칭: `/reset`, `/new`                                                                                                                                                       |
| `/compact [instructions]` | 선택적 포커스 지침으로 대화 압축                                                                                                                                                                             |
| `/config`                 | [설정](/ko/settings) 인터페이스를 열어 테마, 모델, [출력 스타일](/ko/output-styles) 및 기타 기본 설정 조정. 별칭: `/settings`                                                                                                |
| `/context`                | 현재 컨텍스트 사용을 색상 그리드로 시각화                                                                                                                                                                        |
| `/copy`                   | 마지막 어시스턴트 응답을 클립보드에 복사. 코드 블록이 있을 때 개별 블록 또는 전체 응답을 선택할 수 있는 대화형 선택기 표시                                                                                                                        |
| `/cost`                   | 토큰 사용 통계 표시. 구독별 세부 정보는 [비용 추적 가이드](/ko/costs#using-the-cost-command) 참조                                                                                                                       |
| `/desktop`                | 현재 세션을 Claude Code 데스크톱 앱에서 계속. macOS 및 Windows만 해당. 별칭: `/app`                                                                                                                                |
| `/diff`                   | 커밋되지 않은 변경 사항 및 턴별 diff를 보여주는 대화형 diff 뷰어 열기. 왼쪽/오른쪽 화살표를 사용하여 현재 git diff와 개별 Claude 턴 간 전환, 위/아래로 파일 탐색                                                                                      |
| `/doctor`                 | Claude Code 설치 및 설정 진단 및 확인                                                                                                                                                                    |
| `/exit`                   | CLI 종료. 별칭: `/quit`                                                                                                                                                                            |
| `/export [filename]`      | 현재 대화를 일반 텍스트로 내보내기. 파일 이름이 있으면 해당 파일에 직접 작성. 없으면 클립보드에 복사하거나 파일에 저장할 대화 열기                                                                                                                    |
| `/extra-usage`            | 속도 제한에 도달했을 때 계속 작동하도록 추가 사용 구성                                                                                                                                                                |
| `/fast [on\|off]`         | [빠른 모드](/ko/fast-mode) 켜기 또는 끄기                                                                                                                                                                |
| `/feedback [report]`      | Claude Code에 대한 피드백 제출. 별칭: `/bug`                                                                                                                                                             |
| `/fork [name]`            | 이 지점에서 현재 대화의 포크 생성                                                                                                                                                                            |
| `/help`                   | 도움말 및 사용 가능한 명령 표시                                                                                                                                                                             |
| `/hooks`                  | [hook](/ko/hooks) 구성 관리                                                                                                                                                                        |
| `/ide`                    | IDE 통합 관리 및 상태 표시                                                                                                                                                                              |
| `/init`                   | `CLAUDE.md` 가이드로 프로젝트 초기화                                                                                                                                                                      |
| `/insights`               | 프로젝트 영역, 상호 작용 패턴 및 마찰 지점을 포함하여 Claude Code 세션을 분석하는 보고서 생성                                                                                                                                    |
| `/install-github-app`     | 리포지토리에 대한 [Claude GitHub Actions](/ko/github-actions) 앱 설정. 리포지토리 선택 및 통합 구성을 안내합니다                                                                                                            |
| `/install-slack-app`      | Claude Slack 앱 설치. OAuth 흐름을 완료하기 위해 브라우저 열기                                                                                                                                                   |
| `/keybindings`            | 키바인딩 구성 파일 열기 또는 생성                                                                                                                                                                            |
| `/login`                  | Anthropic 계정에 로그인                                                                                                                                                                              |
| `/logout`                 | Anthropic 계정에서 로그아웃                                                                                                                                                                            |
| `/mcp`                    | MCP 서버 연결 및 OAuth 인증 관리                                                                                                                                                                        |
| `/memory`                 | `CLAUDE.md` 메모리 파일 편집, [자동 메모리](/ko/memory#auto-memory) 활성화 또는 비활성화, 자동 메모리 항목 보기                                                                                                              |
| `/mobile`                 | Claude 모바일 앱 다운로드 QR 코드 표시. 별칭: `/ios`, `/android`                                                                                                                                             |
| `/model [model]`          | AI 모델 선택 또는 변경. 지원하는 모델의 경우 왼쪽/오른쪽 화살표를 사용하여 [노력 수준 조정](/ko/model-config#adjust-effort-level). 변경 사항은 현재 응답이 완료될 때까지 기다리지 않고 즉시 적용됩니다                                                          |
| `/passes`                 | 친구와 Claude Code의 무료 1주일 공유. 계정이 적격인 경우에만 표시                                                                                                                                                    |
| `/permissions`            | [권한](/ko/permissions#manage-permissions) 보기 또는 업데이트. 별칭: `/allowed-tools`                                                                                                                      |
| `/plan`                   | 프롬프트에서 직접 Plan Mode 입력                                                                                                                                                                         |
| `/plugin`                 | Claude Code [plugins](/ko/plugins) 관리                                                                                                                                                          |
| `/pr-comments [PR]`       | GitHub 풀 요청에서 댓글 가져오기 및 표시. 현재 분기에 대한 PR을 자동으로 감지하거나 PR URL 또는 번호 전달. `gh` CLI 필요                                                                                                              |
| `/privacy-settings`       | 개인 정보 보호 설정 보기 및 업데이트. Pro 및 Max 요금제 구독자만 사용 가능                                                                                                                                                |
| `/release-notes`          | 가장 최근 버전이 프롬프트에 가장 가까운 전체 변경 로그 보기                                                                                                                                                             |
| `/reload-plugins`         | 모든 활성 [plugins](/ko/plugins)를 다시 로드하여 재시작 없이 보류 중인 변경 사항 적용. 로드된 내용을 보고하고 재시작이 필요한 변경 사항 기록                                                                                                    |
| `/remote-control`         | 이 세션을 claude.ai에서 [원격 제어](/ko/remote-control)할 수 있도록 설정. 별칭: `/rc`                                                                                                                             |
| `/remote-env`             | [teleport 세션](/ko/claude-code-on-the-web#teleport-a-web-session-to-your-terminal)의 기본 원격 환경 구성                                                                                                 |
| `/rename [name]`          | 현재 세션 이름 바꾸기. 이름 없이 대화 기록에서 자동 생성                                                                                                                                                              |
| `/resume [session]`       | ID 또는 이름으로 대화 재개 또는 세션 선택기 열기. 별칭: `/continue`                                                                                                                                                 |
| `/review`                 | 더 이상 사용되지 않음. 대신 [`code-review` plugin](https://github.com/anthropics/claude-code-marketplace/blob/main/code-review/README.md) 설치: `claude plugin install code-review@claude-code-marketplace` |
| `/rewind`                 | 대화 및/또는 코드를 이전 지점으로 되돌리거나 선택한 메시지에서 요약. [checkpointing](/ko/checkpointing) 참조. 별칭: `/checkpoint`                                                                                               |
| `/sandbox`                | [sandbox 모드](/ko/sandboxing) 토글. 지원되는 플랫폼에서만 사용 가능                                                                                                                                             |
| `/security-review`        | 현재 분기의 보류 중인 변경 사항을 보안 취약점에 대해 분석. git diff를 검토하고 주입, 인증 문제 및 데이터 노출과 같은 위험을 식별합니다                                                                                                             |
| `/skills`                 | 사용 가능한 [skills](/ko/skills) 나열                                                                                                                                                                 |
| `/stats`                  | 일일 사용, 세션 기록, 연속 기록 및 모델 기본 설정 시각화                                                                                                                                                             |
| `/status`                 | 버전, 모델, 계정 및 연결성을 보여주는 설정 인터페이스(상태 탭) 열기                                                                                                                                                       |
| `/statusline`             | Claude Code의 [상태 줄](/ko/statusline) 구성. 원하는 내용을 설명하거나 인수 없이 실행하여 셸 프롬프트에서 자동 구성                                                                                                                |
| `/stickers`               | Claude Code 스티커 주문                                                                                                                                                                             |
| `/tasks`                  | 백그라운드 작업 나열 및 관리                                                                                                                                                                               |
| `/terminal-setup`         | Shift+Enter 및 기타 단축키에 대한 터미널 키바인딩 구성. VS Code, Alacritty 또는 Warp와 같이 필요한 터미널에서만 표시                                                                                                             |
| `/theme`                  | 색상 테마 변경. 밝은 색과 어두운 색 변형, 색맹 접근 가능(daltonized) 테마 및 터미널의 색상 팔레트를 사용하는 ANSI 테마 포함                                                                                                               |
| `/upgrade`                | 업그레이드 페이지를 열어 더 높은 요금제로 전환                                                                                                                                                                     |
| `/usage`                  | 요금제 사용 제한 및 속도 제한 상태 표시                                                                                                                                                                        |
| `/vim`                    | Vim 및 일반 편집 모드 간 토글                                                                                                                                                                            |

### MCP 프롬프트

MCP 서버는 명령으로 나타나는 프롬프트를 노출할 수 있습니다. 이들은 `/mcp__<server>__<prompt>` 형식을 사용하며 연결된 서버에서 동적으로 발견됩니다. 자세한 내용은 [MCP 프롬프트](/ko/mcp#use-mcp-prompts-as-commands)를 참조하세요.

## Vim 편집기 모드

`/vim` 명령으로 vim 스타일 편집을 활성화하거나 `/config`를 통해 영구적으로 구성하세요.

### 모드 전환

| 명령    | 작업           | 모드에서   |
| :---- | :----------- | :----- |
| `Esc` | NORMAL 모드 입력 | INSERT |
| `i`   | 커서 앞에 삽입     | NORMAL |
| `I`   | 줄의 시작에 삽입    | NORMAL |
| `a`   | 커서 뒤에 삽입     | NORMAL |
| `A`   | 줄의 끝에 삽입     | NORMAL |
| `o`   | 아래 줄 열기      | NORMAL |
| `O`   | 위 줄 열기       | NORMAL |

### 탐색 (NORMAL 모드)

| 명령              | 작업                      |
| :-------------- | :---------------------- |
| `h`/`j`/`k`/`l` | 왼쪽/아래/위/오른쪽 이동          |
| `w`             | 다음 단어                   |
| `e`             | 단어 끝                    |
| `b`             | 이전 단어                   |
| `0`             | 줄의 시작                   |
| `$`             | 줄의 끝                    |
| `^`             | 첫 번째 공백이 아닌 문자          |
| `gg`            | 입력의 시작                  |
| `G`             | 입력의 끝                   |
| `f{char}`       | 다음 문자 발생으로 점프           |
| `F{char}`       | 이전 문자 발생으로 점프           |
| `t{char}`       | 다음 문자 발생 직전으로 점프        |
| `T{char}`       | 이전 문자 발생 직후로 점프         |
| `;`             | 마지막 f/F/t/T 모션 반복       |
| `,`             | 마지막 f/F/t/T 모션을 역순으로 반복 |

<Note>
  vim 일반 모드에서 커서가 입력의 시작 또는 끝에 있고 더 이상 이동할 수 없으면 화살표 키가 명령 기록을 탐색합니다.
</Note>

### 편집 (NORMAL 모드)

| 명령             | 작업           |
| :------------- | :----------- |
| `x`            | 문자 삭제        |
| `dd`           | 줄 삭제         |
| `D`            | 줄 끝까지 삭제     |
| `dw`/`de`/`db` | 단어 삭제/끝까지/뒤로 |
| `cc`           | 줄 변경         |
| `C`            | 줄 끝까지 변경     |
| `cw`/`ce`/`cb` | 단어 변경/끝까지/뒤로 |
| `yy`/`Y`       | 줄 복사         |
| `yw`/`ye`/`yb` | 단어 복사/끝까지/뒤로 |
| `p`            | 커서 뒤에 붙여넣기   |
| `P`            | 커서 앞에 붙여넣기   |
| `>>`           | 줄 들여쓰기       |
| `<<`           | 줄 내어쓰기       |
| `J`            | 줄 결합         |
| `.`            | 마지막 변경 반복    |

### 텍스트 객체 (NORMAL 모드)

텍스트 객체는 `d`, `c` 및 `y`와 같은 연산자와 함께 작동합니다:

| 명령        | 작업                 |
| :-------- | :----------------- |
| `iw`/`aw` | 내부/주변 단어           |
| `iW`/`aW` | 내부/주변 WORD (공백 구분) |
| `i"`/`a"` | 내부/주변 큰따옴표         |
| `i'`/`a'` | 내부/주변 작은따옴표        |
| `i(`/`a(` | 내부/주변 괄호           |
| `i[`/`a[` | 내부/주변 대괄호          |
| `i{`/`a{` | 내부/주변 중괄호          |

## 명령 기록

Claude Code는 현재 세션의 명령 기록을 유지합니다:

* 입력 기록은 작업 디렉토리별로 저장됩니다
* 입력 기록은 `/clear`를 실행하여 새 세션을 시작할 때 재설정됩니다. 이전 세션의 대화는 보존되며 재개할 수 있습니다.
* Up/Down 화살표를 사용하여 탐색 (위의 키보드 단축키 참조)
* **참고**: 기록 확장(`!`)은 기본적으로 비활성화됩니다

### Ctrl+R을 사용한 역방향 검색

`Ctrl+R`을 눌러 명령 기록을 대화형으로 검색합니다:

1. **검색 시작**: `Ctrl+R`을 눌러 역방향 기록 검색 활성화
2. **쿼리 입력**: 이전 명령에서 검색할 텍스트 입력. 검색 용어는 일치하는 결과에서 강조 표시됩니다
3. **일치 탐색**: `Ctrl+R`을 다시 눌러 더 오래된 일치 항목을 순환합니다
4. **일치 수락**:
   * `Tab` 또는 `Esc`를 눌러 현재 일치 항목을 수락하고 편집 계속
   * `Enter`를 눌러 명령을 수락하고 즉시 실행
5. **검색 취소**:
   * `Ctrl+C`를 눌러 취소하고 원래 입력 복원
   * 빈 검색에서 `Backspace`를 눌러 취소

검색은 검색 용어가 강조된 일치하는 명령을 표시하므로 이전 입력을 찾아 재사용할 수 있습니다.

## 백그라운드 bash 명령

Claude Code는 bash 명령을 백그라운드에서 실행하여 장시간 실행되는 프로세스가 실행되는 동안 계속 작업할 수 있도록 지원합니다.

### 백그라운드 실행 작동 방식

Claude Code가 명령을 백그라운드에서 실행하면 명령을 비동기적으로 실행하고 즉시 백그라운드 작업 ID를 반환합니다. Claude Code는 명령이 백그라운드에서 계속 실행되는 동안 새 프롬프트에 응답할 수 있습니다.

명령을 백그라운드에서 실행하려면 다음 중 하나를 수행할 수 있습니다:

* Claude Code에 명령을 백그라운드에서 실행하도록 프롬프트
* Ctrl+B를 눌러 일반 Bash 도구 호출을 백그라운드로 이동. (Tmux 사용자는 tmux의 접두사 키로 인해 Ctrl+B를 두 번 눌러야 합니다.)

**주요 기능:**

* 출력은 버퍼링되고 Claude는 TaskOutput 도구를 사용하여 검색할 수 있습니다
* 백그라운드 작업에는 추적 및 출력 검색을 위한 고유 ID가 있습니다
* 백그라운드 작업은 Claude Code가 종료될 때 자동으로 정리됩니다

모든 백그라운드 작업 기능을 비활성화하려면 `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` 환경 변수를 `1`로 설정하세요. 자세한 내용은 [환경 변수](/ko/settings#environment-variables)를 참조하세요.

**일반적인 백그라운드 명령:**

* 빌드 도구 (webpack, vite, make)
* 패키지 관리자 (npm, yarn, pnpm)
* 테스트 러너 (jest, pytest)
* 개발 서버
* 장시간 실행 프로세스 (docker, terraform)

### `!` 접두사를 사용한 Bash 모드

입력 앞에 `!`를 붙여 Claude를 거치지 않고 bash 명령을 직접 실행합니다:

```bash  theme={null}
! npm test
! git status
! ls -la
```

Bash 모드:

* 명령 및 출력을 대화 컨텍스트에 추가합니다
* 실시간 진행 상황 및 출력 표시
* 장시간 실행 명령에 대해 동일한 `Ctrl+B` 백그라운드 실행 지원
* Claude가 명령을 해석하거나 승인할 필요가 없습니다
* 기록 기반 자동 완성 지원: 부분 명령을 입력하고 **Tab**을 눌러 현재 프로젝트의 이전 `!` 명령에서 완성
* `Escape`, `Backspace` 또는 빈 프롬프트에서 `Ctrl+U`로 종료

이는 대화 컨텍스트를 유지하면서 빠른 셸 작업에 유용합니다.

## 프롬프트 제안

세션을 처음 열 때 시작하는 데 도움이 되는 회색 예제 명령이 프롬프트 입력에 나타납니다. Claude Code는 프로젝트의 git 기록에서 이를 선택하므로 최근에 작업한 파일을 반영합니다.

Claude가 응답한 후 제안은 대화 기록을 기반으로 계속 나타나며, 예를 들어 다중 부분 요청의 후속 단계 또는 워크플로우의 자연스러운 연속입니다.

* **Tab**을 눌러 제안을 수락하거나 **Enter**를 눌러 수락하고 제출
* 입력을 시작하여 제안 해제

제안은 부모 대화의 프롬프트 캐시를 재사용하는 백그라운드 요청으로 실행되므로 추가 비용은 최소입니다. Claude Code는 불필요한 비용을 피하기 위해 캐시가 콜드일 때 제안 생성을 건너뜁니다.

제안은 대화의 첫 번째 턴 후, 비대화형 모드에서 및 Plan Mode에서 자동으로 건너뜁니다.

프롬프트 제안을 완전히 비활성화하려면 환경 변수를 설정하거나 `/config`에서 설정을 토글하세요:

```bash  theme={null}
export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false
```

## /btw를 사용한 부가 질문

`/btw`를 사용하여 현재 작업에 대한 빠른 질문을 대화 기록에 추가하지 않고 합니다. 이는 빠른 답변을 원하지만 주 컨텍스트를 복잡하게 하거나 Claude를 장시간 실행 작업에서 벗어나게 하고 싶지 않을 때 유용합니다.

```
/btw what was the name of that config file again?
```

부가 질문은 현재 대화에 완전히 표시되므로 Claude가 이미 읽은 코드, 이전에 내린 결정 또는 세션의 다른 항목에 대해 질문할 수 있습니다. 질문과 답변은 임시입니다: 해제 가능한 오버레이에 나타나며 대화 기록에 절대 입력되지 않습니다.

* **Claude가 작업하는 동안 사용 가능**: Claude가 응답을 처리하는 동안에도 `/btw`를 실행할 수 있습니다. 부가 질문은 독립적으로 실행되며 주 턴을 중단하지 않습니다.
* **도구 접근 없음**: 부가 질문은 이미 컨텍스트에 있는 것에서만 답변합니다. Claude는 부가 질문에 답할 때 파일을 읽거나 명령을 실행하거나 검색할 수 없습니다.
* **단일 응답**: 후속 턴이 없습니다. 왕복이 필요하면 일반 프롬프트를 대신 사용하세요.
* **낮은 비용**: 부가 질문은 부모 대화의 프롬프트 캐시를 재사용하므로 추가 비용은 최소입니다.

**Space**, **Enter** 또는 **Escape**를 눌러 답변을 해제하고 프롬프트로 돌아갑니다.

`/btw`는 [subagent](/ko/sub-agents)의 역입니다: 전체 대화를 보지만 도구가 없는 반면, subagent는 전체 도구를 가지지만 빈 컨텍스트로 시작합니다. `/btw`를 사용하여 Claude가 이 세션에서 이미 알고 있는 것에 대해 질문하세요; subagent를 사용하여 새로운 것을 찾아보세요.

## 작업 목록

복잡한 다단계 작업을 수행할 때 Claude는 진행 상황을 추적하기 위해 작업 목록을 만듭니다. 작업은 터미널의 상태 영역에 보류 중, 진행 중 또는 완료를 나타내는 표시기와 함께 나타납니다.

* `Ctrl+T`를 눌러 작업 목록 보기를 토글합니다. 디스플레이는 한 번에 최대 10개의 작업을 표시합니다
* 모든 작업을 보거나 지우려면 Claude에 직접 요청하세요: "show me all tasks" 또는 "clear all tasks"
* 작업은 컨텍스트 압축 전체에서 지속되어 Claude가 더 큰 프로젝트에서 조직화된 상태를 유지하도록 도와줍니다
* 세션 간 작업 목록을 공유하려면 `CLAUDE_CODE_TASK_LIST_ID`를 `~/.claude/tasks/`의 명명된 디렉토리로 사용하도록 설정하세요: `CLAUDE_CODE_TASK_LIST_ID=my-project claude`
* 이전 TODO 목록으로 되돌리려면 `CLAUDE_CODE_ENABLE_TASKS=false`를 설정하세요.

## PR 검토 상태

열린 풀 요청이 있는 분기에서 작업할 때 Claude Code는 바닥글에 클릭 가능한 PR 링크를 표시합니다 (예: "PR #446"). 링크에는 검토 상태를 나타내는 색상 밑줄이 있습니다:

* 녹색: 승인됨
* 노란색: 검토 대기 중
* 빨간색: 변경 요청됨
* 회색: 초안
* 보라색: 병합됨

`Cmd+click` (Mac) 또는 `Ctrl+click` (Windows/Linux)로 링크를 클릭하여 브라우저에서 풀 요청을 엽니다. 상태는 60초마다 자동으로 업데이트됩니다.

<Note>
  PR 상태는 `gh` CLI가 설치되고 인증되어야 합니다 (`gh auth login`).
</Note>

## 참고 항목

* [Skills](/ko/skills) - 사용자 정의 프롬프트 및 워크플로우
* [Checkpointing](/ko/checkpointing) - Claude의 편집 되돌리기 및 이전 상태 복원
* [CLI 참조](/ko/cli-reference) - 명령줄 플래그 및 옵션
* [설정](/ko/settings) - 구성 옵션
* [메모리 관리](/ko/memory) - CLAUDE.md 파일 관리
