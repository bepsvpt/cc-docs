> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 터미널 설정 최적화

> Claude Code는 터미널이 제대로 구성되었을 때 최적으로 작동합니다. 이 지침을 따라 환경을 최적화하세요.

### 테마 및 모양

Claude는 터미널의 테마를 제어할 수 없습니다. 이는 터미널 애플리케이션에서 처리됩니다. `/config` 명령을 통해 언제든지 Claude Code의 테마를 터미널과 일치시킬 수 있습니다.

Claude Code 인터페이스 자체를 추가로 사용자 정의하려면 [사용자 정의 상태 표시줄](/ko/statusline)을 구성하여 현재 모델, 작업 디렉토리 또는 git 분기와 같은 상황별 정보를 터미널 하단에 표시할 수 있습니다.

### 줄 바꿈

Claude Code에 줄 바꿈을 입력하는 여러 옵션이 있습니다:

* **빠른 이스케이프**: `\`를 입력한 후 Enter를 눌러 새 줄을 만듭니다
* **Shift+Enter**: iTerm2, WezTerm, Ghostty 및 Kitty에서 기본적으로 작동합니다
* **키보드 단축키**: 다른 터미널에서 새 줄을 삽입하도록 키 바인딩을 설정합니다

**다른 터미널에서 Shift+Enter 설정**

Claude Code 내에서 `/terminal-setup`을 실행하여 VS Code, Alacritty, Zed 및 Warp에 대해 Shift+Enter를 자동으로 구성합니다.

<Note>
  `/terminal-setup` 명령은 수동 구성이 필요한 터미널에서만 표시됩니다. iTerm2, WezTerm, Ghostty 또는 Kitty를 사용 중인 경우 Shift+Enter가 이미 기본적으로 작동하므로 이 명령이 표시되지 않습니다.
</Note>

**Option+Enter 설정 (VS Code, iTerm2 또는 macOS Terminal.app)**

**Mac Terminal.app의 경우:**

1. 설정 → 프로필 → 키보드 열기
2. "Option을 Meta 키로 사용" 확인

**iTerm2 및 VS Code 터미널의 경우:**

1. 설정 → 프로필 → 키 열기
2. 일반에서 왼쪽/오른쪽 Option 키를 "Esc+"로 설정

### 알림 설정

적절한 알림 구성으로 Claude가 작업을 완료할 때 놓치지 마세요:

#### iTerm 2 시스템 알림

작업 완료 시 iTerm 2 알림의 경우:

1. iTerm 2 환경설정 열기
2. 프로필 → 터미널로 이동
3. "Silence bell" 활성화 및 필터 알림 → "이스케이프 시퀀스 생성 알림 전송"
4. 선호하는 알림 지연 설정

이러한 알림은 iTerm 2에만 해당되며 기본 macOS 터미널에서는 사용할 수 없습니다.

#### 사용자 정의 알림 훅

고급 알림 처리의 경우 [알림 훅](/ko/hooks#notification)을 만들어 자신의 로직을 실행할 수 있습니다.

### 큰 입력 처리

광범위한 코드 또는 긴 지침으로 작업할 때:

* **직접 붙여넣기 피하기**: Claude Code는 매우 긴 붙여넣은 콘텐츠로 어려움을 겪을 수 있습니다
* **파일 기반 워크플로우 사용**: 파일에 콘텐츠를 작성하고 Claude에 읽도록 요청합니다
* **VS Code 제한 사항 인식**: VS Code 터미널은 특히 긴 붙여넣기를 자르는 경향이 있습니다

### Vim 모드

Claude Code는 `/vim`으로 활성화하거나 `/config`를 통해 구성할 수 있는 Vim 키 바인딩의 부분 집합을 지원합니다.

지원되는 부분 집합에는 다음이 포함됩니다:

* 모드 전환: `Esc` (NORMAL로), `i`/`I`, `a`/`A`, `o`/`O` (INSERT로)
* 네비게이션: `h`/`j`/`k`/`l`, `w`/`e`/`b`, `0`/`$`/`^`, `gg`/`G`, `f`/`F`/`t`/`T` (`;`/`,` 반복 포함)
* 편집: `x`, `dw`/`de`/`db`/`dd`/`D`, `cw`/`ce`/`cb`/`cc`/`C`, `.` (반복)
* 복사/붙여넣기: `yy`/`Y`, `yw`/`ye`/`yb`, `p`/`P`
* 텍스트 객체: `iw`/`aw`, `iW`/`aW`, `i"`/`a"`, `i'`/`a'`, `i(`/`a(`, `i[`/`a[`, `i{`/`a{`
* 들여쓰기: `>>`/`<<`
* 줄 작업: `J` (줄 결합)

완전한 참조는 [대화형 모드](/ko/interactive-mode#vim-editor-mode)를 참조하세요.
