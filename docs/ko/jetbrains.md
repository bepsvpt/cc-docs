> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# JetBrains IDEs

> Claude Code를 IntelliJ, PyCharm, WebStorm 등 JetBrains IDE와 함께 사용합니다

Claude Code는 전용 플러그인을 통해 JetBrains IDE와 통합되며, 대화형 diff 보기, 선택 영역 컨텍스트 공유 등의 기능을 제공합니다.

## 지원되는 IDE

Claude Code 플러그인은 다음을 포함한 대부분의 JetBrains IDE와 호환됩니다:

* IntelliJ IDEA
* PyCharm
* Android Studio
* WebStorm
* PhpStorm
* GoLand

## 기능

* **빠른 실행**: `Cmd+Esc` (Mac) 또는 `Ctrl+Esc` (Windows/Linux)를 사용하여 편집기에서 직접 Claude Code를 열거나, UI의 Claude Code 버튼을 클릭합니다
* **Diff 보기**: 코드 변경 사항을 터미널 대신 IDE diff 뷰어에 직접 표시할 수 있습니다
* **선택 영역 컨텍스트**: IDE의 현재 선택 영역 또는 탭이 Claude Code와 자동으로 공유됩니다
* **파일 참조 바로가기**: `Cmd+Option+K` (Mac) 또는 `Alt+Ctrl+K` (Linux/Windows)를 사용하여 `@src/auth.ts#L1-99`와 같은 파일 참조를 삽입합니다
* **진단 공유**: IDE의 진단 오류 (lint 및 구문 오류 등)가 작업할 때 Claude와 자동으로 공유됩니다

## 설치

### 마켓플레이스 설치

JetBrains 마켓플레이스에서 [Claude Code 플러그인](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-)을 찾아 설치하고 IDE를 다시 시작합니다.

Claude Code를 아직 설치하지 않았다면, [빠른 시작 가이드](/ko/quickstart)에서 설치 지침을 참조하세요.

<Note>
  플러그인을 설치한 후 IDE를 완전히 다시 시작해야 적용될 수 있습니다.
</Note>

## 사용법

### IDE에서

IDE의 통합 터미널에서 `claude`를 실행하면 모든 통합 기능이 활성화됩니다.

### 외부 터미널에서

모든 외부 터미널에서 `/ide` 명령을 사용하여 Claude Code를 JetBrains IDE에 연결하고 모든 기능을 활성화합니다:

```bash theme={null}
claude
```

```text theme={null}
/ide
```

Claude가 IDE와 동일한 파일에 액세스하도록 하려면, IDE 프로젝트 루트와 동일한 디렉터리에서 Claude Code를 시작합니다.

## 구성

### Claude Code 설정

Claude Code의 설정을 통해 IDE 통합을 구성합니다:

1. `claude` 실행
2. `/config` 명령 입력
3. diff 도구를 `auto`로 설정하여 IDE에서 diff를 표시하거나, `terminal`로 설정하여 터미널에 유지합니다

### 플러그인 설정

\*\*설정 → 도구 → Claude Code \[Beta]\*\*로 이동하여 Claude Code 플러그인을 구성합니다:

#### 일반 설정

* **Claude 명령**: Claude를 실행할 사용자 정의 명령을 지정합니다 (예: `claude`, `/usr/local/bin/claude`, 또는 `npx @anthropic-ai/claude-code`)
* **Claude 명령을 찾을 수 없음에 대한 알림 표시 안 함**: Claude 명령을 찾을 수 없다는 알림을 건너뜁니다
* **다중 줄 프롬프트에 Option+Enter 사용 활성화**: macOS만 해당합니다. 활성화되면 Option+Enter가 Claude Code 프롬프트에 새 줄을 삽입합니다. Option 키가 예기치 않게 캡처되는 문제가 발생하면 비활성화합니다. 터미널 다시 시작이 필요합니다.
* **자동 업데이트 활성화**: 플러그인 업데이트를 자동으로 확인하고 설치합니다. 다시 시작 시 적용됩니다.

<Tip>
  WSL 사용자의 경우: Claude 명령으로 `wsl -d Ubuntu -- bash -lic "claude"`를 설정합니다 (`Ubuntu`를 WSL 배포판 이름으로 바꿉니다)
</Tip>

#### ESC 키 구성

ESC 키가 JetBrains 터미널에서 Claude Code 작업을 중단하지 않는 경우:

1. **설정 → 도구 → 터미널**로 이동합니다
2. 다음 중 하나를 수행합니다:
   * "Escape로 편집기에 포커스 이동" 선택 해제, 또는
   * "터미널 키 바인딩 구성"을 클릭하고 "편집기로 포커스 전환" 바로가기 삭제
3. 변경 사항을 적용합니다

이렇게 하면 ESC 키가 Claude Code 작업을 제대로 중단할 수 있습니다.

## 특수 구성

### 원격 개발

<Warning>
  JetBrains 원격 개발을 사용할 때는 \*\*설정 → 플러그인 (호스트)\*\*를 통해 원격 호스트에 플러그인을 설치해야 합니다.
</Warning>

플러그인은 로컬 클라이언트 머신이 아닌 원격 호스트에 설치해야 합니다.

### WSL 구성

Claude Code를 WSL2의 JetBrains IDE와 함께 사용하고 "사용 가능한 IDE가 감지되지 않음"이 표시되는 경우, 원인은 일반적으로 WSL2의 NAT 네트워킹 또는 Windows 방화벽이 WSL2와 Windows 호스트에서 실행 중인 IDE 간의 연결을 차단하기 때문입니다. WSL1은 호스트의 네트워크를 직접 사용하므로 영향을 받지 않습니다.

#### Windows 방화벽을 통해 WSL2 트래픽 허용

이것이 권장되는 해결책입니다. 기존 WSL2 네트워킹 모드를 유지하기 때문입니다.

<Steps>
  <Step title="WSL2 IP 주소 찾기">
    WSL 셸 내에서 다음을 실행합니다:

    ```bash theme={null}
    hostname -I
    ```

    서브넷을 기록합니다. 예를 들어 `172.21.123.45`는 `172.21.0.0/16`에 있습니다.
  </Step>

  <Step title="방화벽 규칙 만들기">
    PowerShell을 관리자로 열고 다음을 실행합니다. IP 범위를 서브넷과 일치하도록 조정합니다:

    ```powershell theme={null}
    New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
    ```
  </Step>

  <Step title="IDE 및 Claude Code 다시 시작">
    새 규칙이 적용되도록 둘 다 닫았다가 다시 엽니다.
  </Step>
</Steps>

#### WSL2를 미러링된 네트워킹으로 전환

미러링된 네트워킹에는 Windows 11 22H2 이상이 필요합니다. Windows 10을 사용 중이면 대신 위의 방화벽 규칙을 사용합니다.

Windows 사용자 디렉터리의 `.wslconfig`에 다음을 추가합니다:

```ini theme={null}
[wsl2]
networkingMode=mirrored
```

그런 다음 PowerShell에서 `wsl --shutdown`으로 WSL을 다시 시작합니다.

## 문제 해결

### 플러그인이 작동하지 않음

플러그인이 설치되었지만 Claude Code 기능이 IDE에 나타나지 않는 경우:

* 프로젝트 루트 디렉터리에서 Claude Code를 실행 중인지 확인합니다
* JetBrains 플러그인이 IDE 설정에서 활성화되어 있는지 확인합니다
* IDE를 완전히 다시 시작합니다 (여러 번 수행해야 할 수 있습니다)
* 원격 개발의 경우 플러그인이 원격 호스트에 설치되어 있는지 확인합니다

### IDE가 감지되지 않음

`claude` 실행 시 "사용 가능한 IDE가 감지되지 않음"이 표시되는 경우:

* 플러그인이 설치되고 활성화되어 있는지 확인합니다
* IDE를 완전히 다시 시작합니다
* 통합 터미널에서 Claude Code를 실행 중인지 확인합니다
* WSL 사용자의 경우 위의 [WSL 구성](#wsl-구성)을 참조하세요

### 명령을 찾을 수 없음

Claude 아이콘을 클릭하면 "명령을 찾을 수 없음"이 표시되는 경우:

1. Claude Code가 설치되어 있는지 확인합니다: `claude --version`을 터미널에서 실행합니다
2. 플러그인 설정에서 Claude 명령 경로를 구성합니다
3. WSL 사용자의 경우 구성 섹션에서 언급한 WSL 명령 형식을 사용합니다

## 보안 고려 사항

Claude Code가 자동 편집 권한이 활성화된 JetBrains IDE에서 실행될 때, IDE에서 자동으로 실행될 수 있는 IDE 구성 파일을 수정할 수 있습니다. 이는 자동 편집 모드에서 Claude Code를 실행하는 위험을 증가시킬 수 있으며 bash 실행에 대한 Claude Code의 권한 프롬프트를 우회할 수 있습니다.

JetBrains IDE에서 실행할 때 다음을 고려합니다:

* 편집에 대한 수동 승인 모드 사용
* Claude가 신뢰할 수 있는 프롬프트로만 사용되도록 각별히 주의
* Claude Code가 수정할 수 있는 파일이 무엇인지 인식

Claude Code 설치 또는 로그인 문제가 IDE 외부에서 발생하는 경우 [설치 및 로그인 문제 해결](/ko/troubleshoot-install)을 참조하세요.
