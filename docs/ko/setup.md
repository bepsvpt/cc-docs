> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code 설정

> 개발 머신에 Claude Code를 설치, 인증하고 사용을 시작합니다.

## 시스템 요구사항

* **운영 체제**:
  * macOS 13.0+
  * Windows 10 1809+ 또는 Windows Server 2019+ ([설정 참고 사항 참조](#platform-specific-setup))
  * Ubuntu 20.04+
  * Debian 10+
  * Alpine Linux 3.19+ ([추가 종속성 필요](#platform-specific-setup))
* **하드웨어**: 4GB 이상 RAM
* **네트워크**: 인터넷 연결 필수 ([네트워크 구성](/ko/network-config#network-access-requirements) 참조)
* **Shell**: Bash 또는 Zsh에서 최적으로 작동합니다
* **위치**: [Anthropic 지원 국가](https://www.anthropic.com/supported-countries)

### 추가 종속성

* **ripgrep**: 일반적으로 Claude Code에 포함됩니다. 검색이 실패하면 [검색 문제 해결](/ko/troubleshooting#search-and-discovery-issues)을 참조하십시오.
* **[Node.js 18+](https://nodejs.org/en/download)**: [더 이상 사용되지 않는 npm 설치](#npm-installation-deprecated)에만 필요합니다

## 설치

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

설치 프로세스가 완료된 후 프로젝트로 이동하여 Claude Code를 시작합니다:

```bash  theme={null}
cd your-awesome-project
claude
```

설치 중에 문제가 발생하면 [문제 해결 가이드](/ko/troubleshooting)를 참조하십시오.

<Tip>
  설치 후 `claude doctor`를 실행하여 설치 유형 및 버전을 확인합니다.
</Tip>

### 플랫폼별 설정

**Windows**: Claude Code를 기본적으로 실행하거나 ([Git Bash](https://git-scm.com/downloads/win) 필요) WSL 내에서 실행합니다. WSL 1과 WSL 2 모두 지원되지만 WSL 1은 제한된 지원을 받으며 Bash 도구 sandboxing과 같은 기능을 지원하지 않습니다.

**Alpine Linux 및 기타 musl/uClibc 기반 배포판**:

Alpine 및 기타 musl/uClibc 기반 배포판의 기본 설치 프로그램에는 `libgcc`, `libstdc++` 및 `ripgrep`이 필요합니다. 배포판의 패키지 관리자를 사용하여 이를 설치한 후 `USE_BUILTIN_RIPGREP=0`을 설정합니다.

Alpine에서:

```bash  theme={null}
apk add libgcc libstdc++ ripgrep
```

### 인증

#### 개인 사용자의 경우

1. **Claude Pro 또는 Max 플랜** (권장): Claude의 [Pro 또는 Max 플랜](https://claude.ai/pricing)을 구독하여 Claude Code와 웹의 Claude를 모두 포함하는 통합 구독을 받습니다. 한 곳에서 계정을 관리하고 Claude.ai 계정으로 로그인합니다.
2. **Claude Console**: [Claude Console](https://console.anthropic.com)을 통해 연결하고 OAuth 프로세스를 완료합니다. Anthropic Console에서 활성 청구가 필요합니다. "Claude Code" 워크스페이스가 사용 추적 및 비용 관리를 위해 자동으로 생성됩니다. Claude Code 워크스페이스에 대한 API 키를 만들 수 없습니다. 이는 Claude Code 사용 전용입니다.

#### 팀 및 조직의 경우

1. **Claude for Teams 또는 Enterprise** (권장): [Claude for Teams](https://claude.com/pricing#team-&-enterprise) 또는 [Claude for Enterprise](https://anthropic.com/contact-sales)를 구독하여 중앙 집중식 청구, 팀 관리 및 Claude Code와 웹의 Claude에 대한 액세스를 받습니다. 팀 멤버는 Claude.ai 계정으로 로그인합니다.
2. **팀 청구를 포함한 Claude Console**: 팀 청구를 사용하여 공유 [Claude Console](https://console.anthropic.com) 조직을 설정합니다. 팀 멤버를 초대하고 사용 추적을 위한 역할을 할당합니다.
3. **클라우드 제공자**: 기존 클라우드 인프라를 사용한 배포를 위해 Claude Code를 [Amazon Bedrock, Google Vertex AI 또는 Microsoft Foundry](/ko/third-party-integrations)를 사용하도록 구성합니다.

### 특정 버전 설치

기본 설치 프로그램은 특정 버전 번호 또는 릴리스 채널(`latest` 또는 `stable`)을 허용합니다. 설치 시 선택한 채널이 자동 업데이트의 기본값이 됩니다. 자세한 내용은 [릴리스 채널 구성](#configure-release-channel)을 참조하십시오.

최신 버전을 설치하려면 (기본값):

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

안정 버전을 설치하려면:

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

### 바이너리 무결성 및 코드 서명

* 모든 플랫폼의 SHA256 체크섬은 릴리스 매니페스트에 게시되며, 현재 `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json`에 위치합니다 (예: `{VERSION}`을 `2.0.30`으로 바꿈).
* 서명된 바이너리는 다음 플랫폼에 배포됩니다:
  * macOS: "Anthropic PBC"에서 서명하고 Apple에서 공증
  * Windows: "Anthropic, PBC"에서 서명

## NPM 설치 (더 이상 사용되지 않음)

NPM 설치는 더 이상 사용되지 않습니다. 가능하면 [기본 설치](#installation) 방법을 사용하십시오. 기존 npm 설치를 기본으로 마이그레이션하려면 `claude install`을 실행합니다.

**전역 npm 설치**

```sh  theme={null}
npm install -g @anthropic-ai/claude-code
```

<Warning>
  `sudo npm install -g`를 사용하지 마십시오. 이는 권한 문제 및 보안 위험으로 이어질 수 있습니다.
  권한 오류가 발생하면 권장 솔루션에 대해 [권한 오류 문제 해결](/ko/troubleshooting#command-not-found-claude-or-permission-errors)을 참조하십시오.
</Warning>

## Windows 설정

**옵션 1: WSL 내 Claude Code**

* WSL 1과 WSL 2 모두 지원됩니다
* WSL 2는 향상된 보안을 위해 [sandboxing](/ko/sandboxing)을 지원합니다. WSL 1은 sandboxing을 지원하지 않습니다.

**옵션 2: Git Bash를 사용한 기본 Windows의 Claude Code**

* [Git for Windows](https://git-scm.com/downloads/win) 필요
* 휴대용 Git 설치의 경우 `bash.exe`의 경로를 지정합니다:
  ```powershell  theme={null}
  $env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
  ```

## Claude Code 업데이트

### 자동 업데이트

Claude Code는 최신 기능과 보안 수정 사항을 보유하도록 자동으로 최신 상태를 유지합니다.

* **업데이트 확인**: 시작 시 및 실행 중 주기적으로 수행됨
* **업데이트 프로세스**: 백그라운드에서 자동으로 다운로드 및 설치
* **알림**: 업데이트가 설치되면 알림이 표시됨
* **업데이트 적용**: 업데이트는 다음 번 Claude Code를 시작할 때 적용됨

<Note>
  Homebrew 및 WinGet 설치는 자동 업데이트되지 않습니다. `brew upgrade claude-code` 또는 `winget upgrade Anthropic.ClaudeCode`를 사용하여 수동으로 업데이트합니다.

  **알려진 문제:** Claude Code는 새 버전이 이러한 패키지 관리자에서 사용 가능하기 전에 업데이트를 알릴 수 있습니다. 업그레이드가 실패하면 잠시 기다렸다가 나중에 다시 시도하십시오.
</Note>

### 릴리스 채널 구성

자동 업데이트 및 `claude update`에 대해 Claude Code가 따르는 릴리스 채널을 `autoUpdatesChannel` 설정으로 구성합니다:

* `"latest"` (기본값): 새 기능이 릴리스되는 즉시 받습니다
* `"stable"`: 일반적으로 약 1주일 된 버전을 사용하여 주요 회귀가 있는 릴리스를 건너뜁니다

`/config` → **자동 업데이트 채널**을 통해 또는 [settings.json 파일](/ko/settings)에 추가하여 구성합니다:

```json  theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

엔터프라이즈 배포의 경우 [관리되는 설정](/ko/settings#settings-files)을 사용하여 조직 전체에서 일관된 릴리스 채널을 적용할 수 있습니다.

### 자동 업데이트 비활성화

셸 또는 [settings.json 파일](/ko/settings)에서 `DISABLE_AUTOUPDATER` 환경 변수를 설정합니다:

```bash  theme={null}
export DISABLE_AUTOUPDATER=1
```

### 수동으로 업데이트

```bash  theme={null}
claude update
```

## Claude Code 제거

Claude Code를 제거해야 하는 경우 설치 방법에 따른 지침을 따릅니다.

### 기본 설치

Claude Code 바이너리 및 버전 파일을 제거합니다:

**macOS, Linux, WSL:**

```bash  theme={null}
rm -f ~/.local/bin/claude
rm -rf ~/.local/share/claude
```

**Windows PowerShell:**

```powershell  theme={null}
Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
```

**Windows CMD:**

```batch  theme={null}
del "%USERPROFILE%\.local\bin\claude.exe"
rmdir /s /q "%USERPROFILE%\.local\share\claude"
```

### Homebrew 설치

```bash  theme={null}
brew uninstall --cask claude-code
```

### WinGet 설치

```powershell  theme={null}
winget uninstall Anthropic.ClaudeCode
```

### NPM 설치

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### 구성 파일 정리 (선택 사항)

<Warning>
  구성 파일을 제거하면 모든 설정, 허용된 도구, MCP 서버 구성 및 세션 기록이 삭제됩니다.
</Warning>

Claude Code 설정 및 캐시된 데이터를 제거하려면:

**macOS, Linux, WSL:**

```bash  theme={null}
# 사용자 설정 및 상태 제거
rm -rf ~/.claude
rm ~/.claude.json

# 프로젝트별 설정 제거 (프로젝트 디렉토리에서 실행)
rm -rf .claude
rm -f .mcp.json
```

**Windows PowerShell:**

```powershell  theme={null}
# 사용자 설정 및 상태 제거
Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

# 프로젝트별 설정 제거 (프로젝트 디렉토리에서 실행)
Remove-Item -Path ".claude" -Recurse -Force
Remove-Item -Path ".mcp.json" -Force
```

**Windows CMD:**

```batch  theme={null}
REM 사용자 설정 및 상태 제거
rmdir /s /q "%USERPROFILE%\.claude"
del "%USERPROFILE%\.claude.json"

REM 프로젝트별 설정 제거 (프로젝트 디렉토리에서 실행)
rmdir /s /q ".claude"
del ".mcp.json"
```
