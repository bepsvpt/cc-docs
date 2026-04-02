> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 고급 설정

> Claude Code의 시스템 요구사항, 플랫폼별 설치, 버전 관리 및 제거.

이 페이지에서는 시스템 요구사항, 플랫폼별 설치 세부사항, 업데이트 및 제거에 대해 다룹니다. 첫 번째 세션의 단계별 안내는 [빠른 시작](/ko/quickstart)을 참조하세요. 터미널을 처음 사용하는 경우 [터미널 가이드](/ko/terminal-guide)를 참조하세요.

## 시스템 요구사항

Claude Code는 다음 플랫폼 및 구성에서 실행됩니다:

* **운영 체제**:
  * macOS 13.0+
  * Windows 10 1809+ 또는 Windows Server 2019+
  * Ubuntu 20.04+
  * Debian 10+
  * Alpine Linux 3.19+
* **하드웨어**: 4GB 이상 RAM
* **네트워크**: 인터넷 연결 필수. [네트워크 구성](/ko/network-config#network-access-requirements)을 참조하세요.
* **셸**: Bash, Zsh, PowerShell 또는 CMD. Windows에서는 [Git for Windows](https://git-scm.com/downloads/win)가 필요합니다.
* **위치**: [Anthropic 지원 국가](https://www.anthropic.com/supported-countries)

### 추가 종속성

* **ripgrep**: 일반적으로 Claude Code에 포함됩니다. 검색이 실패하면 [검색 문제 해결](/ko/troubleshooting#search-and-discovery-issues)을 참조하세요.

## Claude Code 설치

<Tip>
  그래픽 인터페이스를 선호하시나요? [Desktop 앱](/ko/desktop-quickstart)을 사용하면 터미널 없이 Claude Code를 사용할 수 있습니다. [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) 또는 [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs)용으로 다운로드하세요.

  터미널이 처음이신가요? 단계별 지침은 [터미널 가이드](/ko/terminal-guide)를 참조하세요.
</Tip>

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

    If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. Use the PowerShell command above instead. Your prompt shows `PS C:\` when you're in PowerShell.

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

설치가 완료된 후 작업하려는 프로젝트에서 터미널을 열고 Claude Code를 시작하세요:

```bash  theme={null}
claude
```

설치 중에 문제가 발생하면 [문제 해결 가이드](/ko/troubleshooting)를 참조하세요.

### Windows에서 설정

Windows의 Claude Code는 [Git for Windows](https://git-scm.com/downloads/win) 또는 WSL이 필요합니다. PowerShell, CMD 또는 Git Bash에서 `claude`를 실행할 수 있습니다. Claude Code는 명령을 실행하기 위해 내부적으로 Git Bash를 사용합니다. PowerShell을 관리자로 실행할 필요가 없습니다.

**옵션 1: Git Bash를 사용한 네이티브 Windows**

[Git for Windows](https://git-scm.com/downloads/win)를 설치한 후 PowerShell 또는 CMD에서 설치 명령을 실행하세요.

Claude Code가 Git Bash 설치를 찾을 수 없으면 [settings.json 파일](/ko/settings)에서 경로를 설정하세요:

```json  theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

**옵션 2: WSL**

WSL 1과 WSL 2 모두 지원됩니다. WSL 2는 향상된 보안을 위해 [샌드박싱](/ko/sandboxing)을 지원합니다. WSL 1은 샌드박싱을 지원하지 않습니다.

### Alpine Linux 및 musl 기반 배포판

Alpine 및 기타 musl/uClibc 기반 배포판의 네이티브 설치 프로그램에는 `libgcc`, `libstdc++` 및 `ripgrep`이 필요합니다. 배포판의 패키지 관리자를 사용하여 이들을 설치한 후 `USE_BUILTIN_RIPGREP=0`을 설정하세요.

이 예제는 Alpine에 필요한 패키지를 설치합니다:

```bash  theme={null}
apk add libgcc libstdc++ ripgrep
```

그런 다음 [`settings.json`](/ko/settings#available-settings) 파일에서 `USE_BUILTIN_RIPGREP`을 `0`으로 설정하세요:

```json  theme={null}
{
  "env": {
    "USE_BUILTIN_RIPGREP": "0"
  }
}
```

## 설치 확인

설치 후 Claude Code가 작동하는지 확인하세요:

```bash  theme={null}
claude --version
```

설치 및 구성을 더 자세히 확인하려면 [`claude doctor`](/ko/troubleshooting#get-more-help)를 실행하세요:

```bash  theme={null}
claude doctor
```

## 인증

Claude Code는 Pro, Max, Teams, Enterprise 또는 Console 계정이 필요합니다. 무료 Claude.ai 플랜에는 Claude Code 액세스가 포함되지 않습니다. [Amazon Bedrock](/ko/amazon-bedrock), [Google Vertex AI](/ko/google-vertex-ai) 또는 [Microsoft Foundry](/ko/microsoft-foundry)와 같은 타사 API 제공자와 함께 Claude Code를 사용할 수도 있습니다.

설치 후 `claude`를 실행하고 브라우저 프롬프트를 따라 로그인하세요. 모든 계정 유형 및 팀 설정 옵션은 [인증](/ko/authentication)을 참조하세요.

## Claude Code 업데이트

네이티브 설치는 백그라운드에서 자동으로 업데이트됩니다. [릴리스 채널을 구성](#configure-release-channel)하여 즉시 업데이트를 받을지 또는 지연된 안정적인 일정으로 받을지 제어하거나 [자동 업데이트를 비활성화](#disable-auto-updates)할 수 있습니다. Homebrew 및 WinGet 설치는 수동 업데이트가 필요합니다.

### 자동 업데이트

Claude Code는 시작 시 및 실행 중에 주기적으로 업데이트를 확인합니다. 업데이트는 백그라운드에서 다운로드 및 설치되며 다음 번에 Claude Code를 시작할 때 적용됩니다.

<Note>
  Homebrew 및 WinGet 설치는 자동으로 업데이트되지 않습니다. `brew upgrade claude-code` 또는 `winget upgrade Anthropic.ClaudeCode`를 사용하여 수동으로 업데이트하세요.

  **알려진 문제:** Claude Code는 새 버전이 이러한 패키지 관리자에서 사용 가능하기 전에 업데이트를 알릴 수 있습니다. 업그레이드가 실패하면 잠시 기다렸다가 나중에 다시 시도하세요.

  Homebrew는 업그레이드 후 디스크에 이전 버전을 유지합니다. 디스크 공간을 확보하려면 주기적으로 `brew cleanup claude-code`를 실행하세요.
</Note>

### 릴리스 채널 구성

`autoUpdatesChannel` 설정으로 Claude Code가 자동 업데이트 및 `claude update`에 대해 따르는 릴리스 채널을 제어하세요:

* `"latest"`, 기본값: 새 기능이 릴리스되는 즉시 받기
* `"stable"`: 일반적으로 약 1주일 된 버전을 사용하여 주요 회귀가 있는 릴리스 건너뛰기

이를 `/config` → **자동 업데이트 채널**을 통해 구성하거나 [settings.json 파일](/ko/settings)에 추가하세요:

```json  theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

엔터프라이즈 배포의 경우 [관리 설정](/ko/permissions#managed-settings)을 사용하여 조직 전체에서 일관된 릴리스 채널을 적용할 수 있습니다.

### 자동 업데이트 비활성화

[`settings.json`](/ko/settings#available-settings) 파일의 `env` 키에서 `DISABLE_AUTOUPDATER`를 `"1"`로 설정하세요:

```json  theme={null}
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

### 수동으로 업데이트

다음 백그라운드 확인을 기다리지 않고 즉시 업데이트를 적용하려면 다음을 실행하세요:

```bash  theme={null}
claude update
```

## 고급 설치 옵션

이러한 옵션은 버전 고정, npm에서 마이그레이션 및 바이너리 무결성 확인을 위한 것입니다.

### 특정 버전 설치

네이티브 설치 프로그램은 특정 버전 번호 또는 릴리스 채널(`latest` 또는 `stable`)을 허용합니다. 설치 시 선택한 채널이 자동 업데이트의 기본값이 됩니다. 자세한 내용은 [릴리스 채널 구성](#configure-release-channel)을 참조하세요.

최신 버전을 설치하려면(기본값):

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```
  </Tab>
</Tabs>

안정적인 버전을 설치하려면:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s stable
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) stable
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd stable && del install.cmd
    ```
  </Tab>
</Tabs>

특정 버전 번호를 설치하려면:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 1.0.58 && del install.cmd
    ```
  </Tab>
</Tabs>

### 더 이상 사용되지 않는 npm 설치

npm 설치는 더 이상 사용되지 않습니다. 네이티브 설치 프로그램이 더 빠르고 종속성이 필요 없으며 백그라운드에서 자동으로 업데이트됩니다. 가능하면 [네이티브 설치](#install-claude-code) 방법을 사용하세요.

#### npm에서 네이티브로 마이그레이션

이전에 npm으로 Claude Code를 설치한 경우 네이티브 설치 프로그램으로 전환하세요:

```bash  theme={null}
# 네이티브 바이너리 설치
curl -fsSL https://claude.ai/install.sh | bash

# 이전 npm 설치 제거
npm uninstall -g @anthropic-ai/claude-code
```

기존 npm 설치에서 `claude install`을 실행하여 네이티브 바이너리를 나란히 설치한 후 npm 버전을 제거할 수도 있습니다.

#### npm으로 설치

호환성 이유로 npm 설치가 필요한 경우 [Node.js 18+](https://nodejs.org/en/download)가 설치되어 있어야 합니다. 패키지를 전역으로 설치하세요:

```bash  theme={null}
npm install -g @anthropic-ai/claude-code
```

<Warning>
  `sudo npm install -g`를 사용하지 마세요. 이는 권한 문제 및 보안 위험으로 이어질 수 있습니다. 권한 오류가 발생하면 [권한 오류 문제 해결](/ko/troubleshooting#permission-errors-during-installation)을 참조하세요.
</Warning>

### 바이너리 무결성 및 코드 서명

SHA256 체크섬 및 코드 서명을 사용하여 Claude Code 바이너리의 무결성을 확인할 수 있습니다.

* 모든 플랫폼의 SHA256 체크섬은 `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json`의 릴리스 매니페스트에 게시됩니다. `{VERSION}`을 `2.0.30`과 같은 버전 번호로 바꾸세요.
* 서명된 바이너리는 다음 플랫폼에 배포됩니다:
  * **macOS**: "Anthropic PBC"에서 서명하고 Apple에서 공증
  * **Windows**: "Anthropic, PBC"에서 서명

## Claude Code 제거

Claude Code를 제거하려면 설치 방법에 따른 지침을 따르세요.

### 네이티브 설치

Claude Code 바이너리 및 버전 파일을 제거하세요:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    rm -f ~/.local/bin/claude
    rm -rf ~/.local/share/claude
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
    Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
    ```
  </Tab>
</Tabs>

### Homebrew 설치

Homebrew cask를 제거하세요:

```bash  theme={null}
brew uninstall --cask claude-code
```

### WinGet 설치

WinGet 패키지를 제거하세요:

```powershell  theme={null}
winget uninstall Anthropic.ClaudeCode
```

### npm

전역 npm 패키지를 제거하세요:

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### 구성 파일 제거

<Warning>
  구성 파일을 제거하면 모든 설정, 허용된 도구, MCP 서버 구성 및 세션 기록이 삭제됩니다.
</Warning>

Claude Code 설정 및 캐시된 데이터를 제거하려면:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    # 사용자 설정 및 상태 제거
    rm -rf ~/.claude
    rm ~/.claude.json

    # 프로젝트별 설정 제거(프로젝트 디렉토리에서 실행)
    rm -rf .claude
    rm -f .mcp.json
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    # 사용자 설정 및 상태 제거
    Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
    Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

    # 프로젝트별 설정 제거(프로젝트 디렉토리에서 실행)
    Remove-Item -Path ".claude" -Recurse -Force
    Remove-Item -Path ".mcp.json" -Force
    ```
  </Tab>
</Tabs>
