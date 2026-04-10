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

# 문제 해결

> Claude Code 설치 및 사용 중 발생하는 일반적인 문제에 대한 해결책을 알아봅니다.

## 설치 문제 해결

<Tip>
  터미널을 완전히 건너뛰고 싶다면, [Claude Code Desktop 앱](/ko/desktop-quickstart)을 사용하여 그래픽 인터페이스를 통해 Claude Code를 설치하고 사용할 수 있습니다. [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) 또는 [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs)용으로 다운로드하고 명령줄 설정 없이 코딩을 시작하세요.
</Tip>

표시되는 오류 메시지 또는 증상을 찾으세요:

| 표시되는 내용                                                     | 해결책                                                                                            |
| :---------------------------------------------------------- | :--------------------------------------------------------------------------------------------- |
| `command not found: claude` 또는 `'claude' is not recognized` | [PATH 수정](#command-not-found-claude-after-installation)                                        |
| `syntax error near unexpected token '<'`                    | [설치 스크립트가 HTML 반환](#install-script-returns-html-instead-of-a-shell-script)                     |
| `curl: (56) Failure writing output to destination`          | [스크립트를 먼저 다운로드한 후 실행](#curl-56-failure-writing-output-to-destination)                          |
| Linux에서 설치 중 `Killed`                                       | [저메모리 서버에 스왑 공간 추가](#install-killed-on-low-memory-linux-servers)                               |
| `TLS connect error` 또는 `SSL/TLS secure channel`             | [CA 인증서 업데이트](#tls-or-ssl-connection-errors)                                                   |
| `Failed to fetch version` 또는 다운로드 서버에 연결할 수 없음              | [네트워크 및 프록시 설정 확인](#check-network-connectivity)                                                |
| `irm is not recognized` 또는 `&& is not valid`                | [셸에 맞는 명령 사용](#windows-irm-or--not-recognized)                                                 |
| `Claude Code on Windows requires git-bash`                  | [Git Bash 설치 또는 구성](#windows-claude-code-on-windows-requires-git-bash)                         |
| `Error loading shared library`                              | [시스템에 맞지 않는 바이너리 변형](#linux-wrong-binary-variant-installed-muslglibc-mismatch)                 |
| Linux에서 `Illegal instruction`                               | [아키텍처 불일치](#illegal-instruction-on-linux)                                                      |
| macOS에서 `dyld: cannot load` 또는 `Abort trap`                 | [바이너리 호환성 문제](#dyld-cannot-load-on-macos)                                                      |
| `Invoke-Expression: Missing argument in parameter list`     | [설치 스크립트가 HTML 반환](#install-script-returns-html-instead-of-a-shell-script)                     |
| `App unavailable in region`                                 | Claude Code는 귀국에서 사용할 수 없습니다. [지원되는 국가](https://www.anthropic.com/supported-countries)를 참조하세요. |
| `unable to get local issuer certificate`                    | [기업 CA 인증서 구성](#tls-or-ssl-connection-errors)                                                  |
| `OAuth error` 또는 `403 Forbidden`                            | [인증 수정](#authentication-issues)                                                                |

문제가 나열되지 않은 경우 다음 진단 단계를 진행하세요.

## 설치 문제 디버깅

### 네트워크 연결 확인

설치 프로그램은 `storage.googleapis.com`에서 다운로드합니다. 연결할 수 있는지 확인하세요:

```bash  theme={null}
curl -sI https://storage.googleapis.com
```

이것이 실패하면 네트워크가 연결을 차단할 수 있습니다. 일반적인 원인:

* Google Cloud Storage를 차단하는 기업 방화벽 또는 프록시
* 지역 네트워크 제한: VPN 또는 대체 네트워크 시도
* TLS/SSL 문제: 시스템의 CA 인증서를 업데이트하거나 `HTTPS_PROXY`가 구성되어 있는지 확인

기업 프록시 뒤에 있는 경우 설치하기 전에 `HTTPS_PROXY` 및 `HTTP_PROXY`를 프록시 주소로 설정하세요. 프록시 URL을 모르면 IT 팀에 문의하거나 브라우저의 프록시 설정을 확인하세요.

이 예제는 두 프록시 변수를 설정한 후 프록시를 통해 설치 프로그램을 실행합니다:

```bash  theme={null}
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
curl -fsSL https://claude.ai/install.sh | bash
```

### PATH 확인

설치가 성공했지만 `claude`를 실행할 때 `command not found` 또는 `not recognized` 오류가 나타나면 설치 디렉토리가 PATH에 없습니다. 셸은 PATH에 나열된 디렉토리에서 프로그램을 검색하며, 설치 프로그램은 macOS/Linux에서 `~/.local/bin/claude`에, Windows에서 `%USERPROFILE%\.local\bin\claude.exe`에 `claude`를 배치합니다.

PATH 항목을 나열하고 `local/bin`으로 필터링하여 설치 디렉토리가 PATH에 있는지 확인하세요:

<Tabs>
  <Tab title="macOS/Linux">
    ```bash  theme={null}
    echo $PATH | tr ':' '\n' | grep local/bin
    ```

    출력이 없으면 디렉토리가 없습니다. 셸 구성에 추가하세요:

    ```bash  theme={null}
    # Zsh (macOS 기본값)
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc

    # Bash (Linux 기본값)
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
    ```

    또는 터미널을 닫았다가 다시 여세요.

    수정이 작동했는지 확인하세요:

    ```bash  theme={null}
    claude --version
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    $env:PATH -split ';' | Select-String 'local\\bin'
    ```

    출력이 없으면 설치 디렉토리를 사용자 PATH에 추가하세요:

    ```powershell  theme={null}
    $currentPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
    [Environment]::SetEnvironmentVariable('PATH', "$currentPath;$env:USERPROFILE\.local\bin", 'User')
    ```

    변경 사항을 적용하려면 터미널을 다시 시작하세요.

    수정이 작동했는지 확인하세요:

    ```powershell  theme={null}
    claude --version
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    echo %PATH% | findstr /i "local\bin"
    ```

    출력이 없으면 시스템 설정을 열고 환경 변수로 이동한 후 `%USERPROFILE%\.local\bin`을 사용자 PATH 변수에 추가하세요. 터미널을 다시 시작하세요.

    수정이 작동했는지 확인하세요:

    ```batch  theme={null}
    claude --version
    ```
  </Tab>
</Tabs>

### 충돌하는 설치 확인

여러 Claude Code 설치로 인해 버전 불일치 또는 예기치 않은 동작이 발생할 수 있습니다. 설치된 항목을 확인하세요:

<Tabs>
  <Tab title="macOS/Linux">
    PATH에서 찾은 모든 `claude` 바이너리를 나열하세요:

    ```bash  theme={null}
    which -a claude
    ```

    네이티브 설치 프로그램과 npm 버전이 있는지 확인하세요:

    ```bash  theme={null}
    ls -la ~/.local/bin/claude
    ```

    ```bash  theme={null}
    ls -la ~/.claude/local/
    ```

    ```bash  theme={null}
    npm -g ls @anthropic-ai/claude-code 2>/dev/null
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    where.exe claude
    Test-Path "$env:LOCALAPPDATA\Claude Code\claude.exe"
    ```
  </Tab>
</Tabs>

여러 설치를 찾으면 하나만 유지하세요. `~/.local/bin/claude`의 네이티브 설치가 권장됩니다. 추가 설치를 제거하세요:

npm 전역 설치 제거:

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

macOS에서 Homebrew 설치 제거:

```bash  theme={null}
brew uninstall --cask claude-code
```

### 디렉토리 권한 확인

설치 프로그램은 `~/.local/bin/` 및 `~/.claude/`에 대한 쓰기 액세스가 필요합니다. 설치가 권한 오류로 실패하면 이 디렉토리가 쓰기 가능한지 확인하세요:

```bash  theme={null}
test -w ~/.local/bin && echo "writable" || echo "not writable"
test -w ~/.claude && echo "writable" || echo "not writable"
```

디렉토리가 쓰기 가능하지 않으면 설치 디렉토리를 만들고 사용자를 소유자로 설정하세요:

```bash  theme={null}
sudo mkdir -p ~/.local/bin
sudo chown -R $(whoami) ~/.local
```

### 바이너리 작동 확인

`claude`가 설치되었지만 시작 시 충돌하거나 중단되면 다음 검사를 실행하여 원인을 좁혀보세요.

바이너리가 존재하고 실행 가능한지 확인하세요:

```bash  theme={null}
ls -la $(which claude)
```

Linux에서 누락된 공유 라이브러리를 확인하세요. `ldd`가 누락된 라이브러리를 표시하면 시스템 패키지를 설치해야 할 수 있습니다. Alpine Linux 및 기타 musl 기반 배포판의 경우 [Alpine Linux 설정](/ko/setup#alpine-linux-and-musl-based-distributions)을 참조하세요.

```bash  theme={null}
ldd $(which claude) | grep "not found"
```

바이너리가 실행될 수 있는지 빠른 건전성 검사를 실행하세요:

```bash  theme={null}
claude --version
```

## 일반적인 설치 문제

가장 자주 발생하는 설치 문제와 해결책입니다.

### 설치 스크립트가 셸 스크립트 대신 HTML 반환

설치 명령을 실행할 때 다음 오류 중 하나가 표시될 수 있습니다:

```text  theme={null}
bash: line 1: syntax error near unexpected token `<'
bash: line 1: `<!DOCTYPE html>'
```

PowerShell에서 동일한 문제는 다음과 같이 나타납니다:

```text  theme={null}
Invoke-Expression: Missing argument in parameter list.
```

이는 설치 URL이 설치 스크립트 대신 HTML 페이지를 반환했음을 의미합니다. HTML 페이지에 "App unavailable in region"이 표시되면 Claude Code는 귀국에서 사용할 수 없습니다. [지원되는 국가](https://www.anthropic.com/supported-countries)를 참조하세요.

그렇지 않으면 네트워크 문제, 지역 라우팅 또는 일시적인 서비스 중단으로 인해 발생할 수 있습니다.

**해결책:**

1. **대체 설치 방법 사용**:

   macOS 또는 Linux에서 Homebrew를 통해 설치하세요:

   ```bash  theme={null}
   brew install --cask claude-code
   ```

   Windows에서 WinGet을 통해 설치하세요:

   ```powershell  theme={null}
   winget install Anthropic.ClaudeCode
   ```

2. **몇 분 후 다시 시도하세요**: 문제는 종종 일시적입니다. 기다렸다가 원래 명령을 다시 시도하세요.

### 설치 후 `command not found: claude`

설치가 완료되었지만 `claude`가 작동하지 않습니다. 정확한 오류는 플랫폼에 따라 다릅니다:

| 플랫폼         | 오류 메시지                                                                 |
| :---------- | :--------------------------------------------------------------------- |
| macOS       | `zsh: command not found: claude`                                       |
| Linux       | `bash: claude: command not found`                                      |
| Windows CMD | `'claude' is not recognized as an internal or external command`        |
| PowerShell  | `claude : The term 'claude' is not recognized as the name of a cmdlet` |

이는 설치 디렉토리가 셸의 검색 경로에 없음을 의미합니다. 각 플랫폼의 수정 사항은 [PATH 확인](#verify-your-path)을 참조하세요.

### `curl: (56) Failure writing output to destination`

`curl ... | bash` 명령은 스크립트를 다운로드하고 파이프(`|`)를 사용하여 Bash에 직접 전달하여 실행합니다. 이 오류는 스크립트 다운로드가 완료되기 전에 연결이 끊어졌음을 의미합니다. 일반적인 원인은 네트워크 중단, 다운로드가 중간에 차단되거나 시스템 리소스 제한입니다.

**해결책:**

1. **네트워크 안정성 확인**: Claude Code 바이너리는 Google Cloud Storage에서 호스팅됩니다. 연결할 수 있는지 테스트하세요:
   ```bash  theme={null}
   curl -fsSL https://storage.googleapis.com -o /dev/null
   ```
   명령이 조용히 완료되면 연결이 정상이고 문제는 일시적일 가능성이 높습니다. 설치 명령을 다시 시도하세요. 오류가 표시되면 네트워크가 다운로드를 차단할 수 있습니다.

2. **대체 설치 방법 시도**:

   macOS 또는 Linux에서:

   ```bash  theme={null}
   brew install --cask claude-code
   ```

   Windows에서:

   ```powershell  theme={null}
   winget install Anthropic.ClaudeCode
   ```

### TLS 또는 SSL 연결 오류

`curl: (35) TLS connect error`, `schannel: next InitializeSecurityContext failed` 또는 PowerShell의 `Could not establish trust relationship for the SSL/TLS secure channel`과 같은 오류는 TLS 핸드셰이크 실패를 나타냅니다.

**해결책:**

1. **시스템 CA 인증서 업데이트**:

   Ubuntu/Debian에서:

   ```bash  theme={null}
   sudo apt-get update && sudo apt-get install ca-certificates
   ```

   Homebrew를 통한 macOS에서:

   ```bash  theme={null}
   brew install ca-certificates
   ```

2. **Windows에서 설치 프로그램을 실행하기 전에 PowerShell에서 TLS 1.2 활성화**:
   ```powershell  theme={null}
   [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
   irm https://claude.ai/install.ps1 | iex
   ```

3. **프록시 또는 방화벽 간섭 확인**: TLS 검사를 수행하는 기업 프록시는 `unable to get local issuer certificate`를 포함한 이러한 오류를 유발할 수 있습니다. `NODE_EXTRA_CA_CERTS`를 기업 CA 인증서 번들로 설정하세요:
   ```bash  theme={null}
   export NODE_EXTRA_CA_CERTS=/path/to/corporate-ca.pem
   ```
   인증서 파일이 없으면 IT 팀에 문의하세요. 프록시가 원인인지 확인하기 위해 직접 연결에서도 시도할 수 있습니다.

### `Failed to fetch version from storage.googleapis.com`

설치 프로그램이 다운로드 서버에 연결할 수 없습니다. 이는 일반적으로 `storage.googleapis.com`이 네트워크에서 차단되었음을 의미합니다.

**해결책:**

1. **연결 직접 테스트**:
   ```bash  theme={null}
   curl -sI https://storage.googleapis.com
   ```

2. **프록시 뒤에 있는 경우** `HTTPS_PROXY`를 설정하여 설치 프로그램이 프록시를 통해 라우팅할 수 있도록 하세요. 자세한 내용은 [프록시 구성](/ko/network-config#proxy-configuration)을 참조하세요.
   ```bash  theme={null}
   export HTTPS_PROXY=http://proxy.example.com:8080
   curl -fsSL https://claude.ai/install.sh | bash
   ```

3. **제한된 네트워크에 있는 경우** 다른 네트워크 또는 VPN을 시도하거나 대체 설치 방법을 사용하세요:

   macOS 또는 Linux에서:

   ```bash  theme={null}
   brew install --cask claude-code
   ```

   Windows에서:

   ```powershell  theme={null}
   winget install Anthropic.ClaudeCode
   ```

### Windows: `irm` 또는 `&&` 인식 안 됨

`'irm' is not recognized` 또는 `The token '&&' is not valid`가 표시되면 셸에 맞지 않는 명령을 실행하고 있습니다.

* **`irm` 인식 안 됨**: PowerShell이 아닌 CMD에 있습니다. 두 가지 옵션이 있습니다:

  시작 메뉴에서 "PowerShell"을 검색하여 PowerShell을 열고 원래 설치 명령을 실행하세요:

  ```powershell  theme={null}
  irm https://claude.ai/install.ps1 | iex
  ```

  또는 CMD에 머물러 있고 CMD 설치 프로그램을 대신 사용하세요:

  ```batch  theme={null}
  curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
  ```

* **`&&` 유효하지 않음**: PowerShell에 있지만 CMD 설치 프로그램 명령을 실행했습니다. PowerShell 설치 프로그램을 사용하세요:
  ```powershell  theme={null}
  irm https://claude.ai/install.ps1 | iex
  ```

### 저메모리 Linux 서버에서 설치 중단됨

VPS 또는 클라우드 인스턴스에서 설치 중에 `Killed`가 표시되면:

```text  theme={null}
Setting up Claude Code...
Installing Claude Code native build latest...
bash: line 142: 34803 Killed    "$binary_path" install ${TARGET:+"$TARGET"}
```

Linux OOM 킬러가 시스템 메모리 부족으로 인해 프로세스를 종료했습니다. Claude Code는 최소 4GB의 사용 가능한 RAM이 필요합니다.

**해결책:**

1. **서버의 RAM이 제한된 경우 스왑 공간 추가**. 스왑은 디스크 공간을 오버플로우 메모리로 사용하여 물리적 RAM이 낮아도 설치를 완료할 수 있습니다.

   2GB 스왑 파일을 만들고 활성화하세요:

   ```bash  theme={null}
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

   그런 다음 설치를 다시 시도하세요:

   ```bash  theme={null}
   curl -fsSL https://claude.ai/install.sh | bash
   ```

2. **다른 프로세스를 닫아** 설치하기 전에 메모리를 확보하세요.

3. **가능하면 더 큰 인스턴스 사용**. Claude Code는 최소 4GB의 RAM이 필요합니다.

### Docker에서 설치 중단

Docker 컨테이너에서 Claude Code를 설치할 때 root로 `/`에 설치하면 중단될 수 있습니다.

**해결책:**

1. **설치 프로그램을 실행하기 전에 작업 디렉토리 설정**. `/`에서 실행하면 설치 프로그램이 전체 파일 시스템을 스캔하여 과도한 메모리 사용을 유발합니다. `WORKDIR`을 설정하면 스캔이 작은 디렉토리로 제한됩니다:
   ```dockerfile  theme={null}
   WORKDIR /tmp
   RUN curl -fsSL https://claude.ai/install.sh | bash
   ```

2. **Docker 메모리 제한 증가** (Docker Desktop 사용 시):
   ```bash  theme={null}
   docker build --memory=4g .
   ```

### Windows: Claude Desktop이 `claude` CLI 명령 재정의

이전 버전의 Claude Desktop을 설치한 경우 `WindowsApps` 디렉토리에 `Claude.exe`를 등록하여 Claude Code CLI보다 PATH 우선순위를 가질 수 있습니다. `claude`를 실행하면 CLI 대신 Desktop 앱이 열립니다.

이 문제를 해결하려면 Claude Desktop을 최신 버전으로 업데이트하세요.

### Windows: "Claude Code on Windows requires git-bash"

Windows의 Claude Code는 Git Bash를 포함하는 [Git for Windows](https://git-scm.com/downloads/win)가 필요합니다.

**Git이 설치되지 않은 경우** [git-scm.com/downloads/win](https://git-scm.com/downloads/win)에서 다운로드하여 설치하세요. 설정 중에 "Add to PATH"를 선택하세요. 설치 후 터미널을 다시 시작하세요.

**Git이 이미 설치되어 있지만** Claude Code가 여전히 찾을 수 없으면 [settings.json 파일](/ko/settings)에서 경로를 설정하세요:

```json  theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

Git이 다른 곳에 설치된 경우 PowerShell에서 `where.exe git`을 실행하여 경로를 찾고 해당 디렉토리의 `bin\bash.exe` 경로를 사용하세요.

### Linux: 잘못된 바이너리 변형 설치됨 (musl/glibc 불일치)

설치 후 `libstdc++.so.6` 또는 `libgcc_s.so.1`과 같은 누락된 공유 라이브러리에 대한 오류가 표시되면 설치 프로그램이 시스템에 맞지 않는 바이너리 변형을 다운로드했을 수 있습니다.

```text  theme={null}
Error loading shared library libstdc++.so.6: No such file or directory
```

이는 musl 교차 컴파일 패키지가 설치된 glibc 기반 시스템에서 발생할 수 있으며, 설치 프로그램이 시스템을 musl로 잘못 감지하게 합니다.

**해결책:**

1. **시스템이 어떤 libc를 사용하는지 확인**:
   ```bash  theme={null}
   ldd /bin/ls | head -1
   ```
   `linux-vdso.so` 또는 `/lib/x86_64-linux-gnu/`에 대한 참조가 표시되면 glibc를 사용하고 있습니다. `musl`이 표시되면 musl을 사용하고 있습니다.

2. **glibc에 있지만 musl 바이너리를 받은 경우** 설치를 제거하고 다시 설치하세요. `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json`의 GCS 버킷에서 올바른 바이너리를 수동으로 다운로드할 수도 있습니다. `ldd /bin/ls` 및 `ls /lib/libc.musl*`의 출력과 함께 [GitHub 이슈](https://github.com/anthropics/claude-code/issues)를 제출하세요.

3. **실제로 musl에 있는 경우** (Alpine Linux) 필요한 패키지를 설치하세요:
   ```bash  theme={null}
   apk add libgcc libstdc++ ripgrep
   ```

### Linux에서 `Illegal instruction`

설치 프로그램이 OOM `Killed` 메시지 대신 `Illegal instruction`을 인쇄하면 다운로드된 바이너리가 CPU 아키텍처와 일치하지 않습니다. 이는 ARM 서버가 x86 바이너리를 받거나 필요한 명령 세트가 없는 이전 CPU에서 일반적으로 발생합니다.

```text  theme={null}
bash: line 142: 2238232 Illegal instruction    "$binary_path" install ${TARGET:+"$TARGET"}
```

**해결책:**

1. **아키텍처 확인**:
   ```bash  theme={null}
   uname -m
   ```
   `x86_64`는 64비트 Intel/AMD를 의미하고 `aarch64`는 ARM64를 의미합니다. 바이너리가 일치하지 않으면 출력과 함께 [GitHub 이슈](https://github.com/anthropics/claude-code/issues)를 제출하세요.

2. **아키텍처 문제가 해결될 때까지 대체 설치 방법 시도**:
   ```bash  theme={null}
   brew install --cask claude-code
   ```

### macOS에서 `dyld: cannot load`

설치 중에 `dyld: cannot load` 또는 `Abort trap: 6`이 표시되면 바이너리가 macOS 버전 또는 하드웨어와 호환되지 않습니다.

```text  theme={null}
dyld: cannot load 'claude-2.1.42-darwin-x64' (load command 0x80000034 is unknown)
Abort trap: 6
```

**해결책:**

1. **macOS 버전 확인**: Claude Code는 macOS 13.0 이상이 필요합니다. Apple 메뉴를 열고 "이 Mac에 관하여"를 선택하여 버전을 확인하세요.

2. **이전 버전을 사용 중인 경우 macOS 업데이트**. 바이너리는 이전 macOS 버전이 지원하지 않는 로드 명령을 사용합니다.

3. **대체 설치 방법으로 Homebrew 시도**:
   ```bash  theme={null}
   brew install --cask claude-code
   ```

### Windows 설치 문제: WSL의 오류

WSL에서 다음 문제가 발생할 수 있습니다:

**OS/플랫폼 감지 문제**: 설치 중에 오류가 발생하면 WSL이 Windows `npm`을 사용할 수 있습니다. 다음을 시도하세요:

* 설치하기 전에 `npm config set os linux` 실행
* `npm install -g @anthropic-ai/claude-code --force --no-os-check`로 설치하세요. `sudo`를 사용하지 마세요.

**Node를 찾을 수 없는 오류**: `claude`를 실행할 때 `exec: node: not found`가 표시되면 WSL 환경이 Windows Node.js 설치를 사용할 수 있습니다. `which npm` 및 `which node`로 확인할 수 있으며, `/usr/`로 시작하는 Linux 경로가 아닌 `/mnt/c/`로 시작하는 경로를 가리켜야 합니다. 이를 해결하려면 Linux 배포판의 패키지 관리자 또는 [`nvm`](https://github.com/nvm-sh/nvm)을 통해 Node를 설치해 보세요.

**nvm 버전 충돌**: WSL과 Windows 모두에 nvm이 설치된 경우 WSL에서 Node 버전을 전환할 때 버전 충돌이 발생할 수 있습니다. WSL이 기본적으로 Windows PATH를 가져오기 때문에 Windows nvm/npm이 WSL 설치보다 우선순위를 가집니다.

다음을 실행하여 이 문제를 식별할 수 있습니다:

* `which npm` 및 `which node` 실행 - `/mnt/c/`로 시작하는 Windows 경로를 가리키면 Windows 버전이 사용 중입니다
* WSL에서 nvm으로 Node 버전을 전환한 후 기능이 손상됨

이 문제를 해결하려면 Linux PATH를 수정하여 Linux node/npm 버전이 우선순위를 갖도록 하세요:

**기본 해결책: nvm이 셸에 제대로 로드되는지 확인**

가장 일반적인 원인은 nvm이 비대화형 셸에 로드되지 않는 것입니다. 셸 구성 파일(`~/.bashrc`, `~/.zshrc` 등)에 다음을 추가하세요:

```bash  theme={null}
# nvm이 있으면 로드
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
```

또는 현재 세션에서 직접 실행하세요:

```bash  theme={null}
source ~/.nvm/nvm.sh
```

**대체: PATH 순서 조정**

nvm이 제대로 로드되었지만 Windows 경로가 여전히 우선순위를 가지면 셸 구성에서 Linux 경로를 PATH 앞에 명시적으로 추가할 수 있습니다:

```bash  theme={null}
export PATH="$HOME/.nvm/versions/node/$(node -v)/bin:$PATH"
```

<Warning>
  WSL에서 Windows 실행 파일을 호출할 수 있는 기능이 손상되므로 `appendWindowsPath = false`를 통해 Windows PATH 가져오기를 비활성화하지 마세요. 마찬가지로 Windows 개발에 사용하는 경우 Windows에서 Node.js를 제거하지 마세요.
</Warning>

### WSL2 샌드박스 설정

[샌드박싱](/ko/sandboxing)은 WSL2에서 지원되지만 추가 패키지를 설치해야 합니다. `/sandbox`를 실행할 때 "Sandbox requires socat and bubblewrap"과 같은 오류가 표시되면 종속성을 설치하세요:

<Tabs>
  <Tab title="Ubuntu/Debian">
    ```bash  theme={null}
    sudo apt-get install bubblewrap socat
    ```
  </Tab>

  <Tab title="Fedora">
    ```bash  theme={null}
    sudo dnf install bubblewrap socat
    ```
  </Tab>
</Tabs>

WSL1은 샌드박싱을 지원하지 않습니다. "Sandboxing requires WSL2"가 표시되면 WSL2로 업그레이드하거나 샌드박싱 없이 Claude Code를 실행해야 합니다.

### 설치 중 권한 오류

네이티브 설치 프로그램이 권한 오류로 실패하면 대상 디렉토리가 쓰기 가능하지 않을 수 있습니다. [디렉토리 권한 확인](#check-directory-permissions)을 참조하세요.

이전에 npm으로 설치했고 npm 관련 권한 오류가 발생하면 네이티브 설치 프로그램으로 전환하세요:

```bash  theme={null}
curl -fsSL https://claude.ai/install.sh | bash
```

## 권한 및 인증

이 섹션에서는 로그인 실패, 토큰 문제 및 권한 프롬프트 동작을 다룹니다.

### 반복되는 권한 프롬프트

동일한 명령을 반복해서 승인해야 하는 경우 `/permissions` 명령을 사용하여 특정 도구가 승인 없이 실행되도록 허용할 수 있습니다. [권한 문서](/ko/permissions#manage-permissions)를 참조하세요.

### 인증 문제

인증 문제가 발생하는 경우:

1. `/logout`을 실행하여 완전히 로그아웃하세요
2. Claude Code 닫기
3. `claude`로 다시 시작하고 인증 프로세스를 완료하세요

로그인 중에 브라우저가 자동으로 열리지 않으면 `c`를 눌러 OAuth URL을 클립보드에 복사한 후 브라우저에 수동으로 붙여넣으세요.

### OAuth 오류: 유효하지 않은 코드

`OAuth error: Invalid code. Please make sure the full code was copied`가 표시되면 로그인 코드가 만료되었거나 복사-붙여넣기 중에 잘렸습니다.

**해결책:**

* Enter를 눌러 다시 시도하고 브라우저가 열린 후 빠르게 로그인을 완료하세요
* 브라우저가 자동으로 열리지 않으면 `c`를 입력하여 전체 URL을 복사하세요
* 원격/SSH 세션을 사용하는 경우 브라우저가 잘못된 머신에서 열릴 수 있습니다. 터미널에 표시된 URL을 복사하여 로컬 브라우저에서 열어보세요.

### 로그인 후 403 Forbidden

로그인 후 `API Error: 403 {"error":{"type":"forbidden","message":"Request not allowed"}}`가 표시되면:

* **Claude Pro/Max 사용자**: [claude.ai/settings](https://claude.ai/settings)에서 구독이 활성화되어 있는지 확인하세요
* **Console 사용자**: 관리자가 계정에 "Claude Code" 또는 "Developer" 역할을 할당했는지 확인하세요
* **프록시 뒤에 있음**: 기업 프록시가 API 요청을 방해할 수 있습니다. 프록시 설정은 [네트워크 구성](/ko/network-config)을 참조하세요.

### WSL2에서 OAuth 로그인 실패

WSL2의 브라우저 기반 로그인은 WSL이 Windows 브라우저를 열 수 없는 경우 실패할 수 있습니다. `BROWSER` 환경 변수를 설정하세요:

```bash  theme={null}
export BROWSER="/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
claude
```

또는 수동으로 URL을 복사하세요: 로그인 프롬프트가 나타나면 `c`를 눌러 OAuth URL을 복사한 후 Windows 브라우저에 붙여넣으세요.

### "Not logged in" 또는 토큰 만료됨

Claude Code가 세션 후 다시 로그인하도록 요청하면 OAuth 토큰이 만료되었을 수 있습니다.

`/login`을 실행하여 다시 인증하세요. 이것이 자주 발생하면 시스템 시계가 정확한지 확인하세요. 토큰 검증은 올바른 타임스탬프에 따라 달라집니다.

## 구성 파일 위치

Claude Code는 여러 위치에 구성을 저장합니다:

| 파일                            | 목적                                                                    |
| :---------------------------- | :-------------------------------------------------------------------- |
| `~/.claude/settings.json`     | 사용자 설정 (권한, hooks, 모델 재정의)                                            |
| `.claude/settings.json`       | 프로젝트 설정 (소스 제어에 체크인됨)                                                 |
| `.claude/settings.local.json` | 로컬 프로젝트 설정 (커밋되지 않음)                                                  |
| `~/.claude.json`              | 전역 상태 (테마, OAuth, MCP 서버)                                             |
| `.mcp.json`                   | 프로젝트 MCP 서버 (소스 제어에 체크인됨)                                             |
| `managed-mcp.json`            | [관리되는 MCP 서버](/ko/mcp#managed-mcp-configuration)                      |
| 관리되는 설정                       | [관리되는 설정](/ko/settings#settings-files) (서버 관리, MDM/OS 수준 정책 또는 파일 기반) |

Windows에서 `~`는 `C:\Users\YourName`과 같은 사용자 홈 디렉토리를 나타냅니다.

이 파일 구성에 대한 자세한 내용은 [설정](/ko/settings) 및 [MCP](/ko/mcp)를 참조하세요.

### 구성 재설정

Claude Code를 기본 설정으로 재설정하려면 구성 파일을 제거할 수 있습니다:

```bash  theme={null}
# 모든 사용자 설정 및 상태 재설정
rm ~/.claude.json
rm -rf ~/.claude/

# 프로젝트별 설정 재설정
rm -rf .claude/
rm .mcp.json
```

<Warning>
  이렇게 하면 모든 설정, MCP 서버 구성 및 세션 기록이 제거됩니다.
</Warning>

## 성능 및 안정성

이 섹션에서는 리소스 사용, 응답성 및 검색 동작과 관련된 문제를 다룹니다.

### 높은 CPU 또는 메모리 사용량

Claude Code는 대부분의 개발 환경에서 작동하도록 설계되었지만 대규모 코드베이스를 처리할 때 상당한 리소스를 소비할 수 있습니다. 성능 문제가 발생하는 경우:

1. `/compact`를 정기적으로 사용하여 컨텍스트 크기 감소
2. 주요 작업 사이에 Claude Code 닫기 및 다시 시작
3. 큰 빌드 디렉토리를 `.gitignore` 파일에 추가하는 것을 고려하세요

### 명령 중단 또는 정지

Claude Code가 응답하지 않는 것처럼 보이면:

1. Ctrl+C를 눌러 현재 작업을 취소하세요
2. 응답하지 않으면 터미널을 닫고 다시 시작해야 할 수 있습니다

### 검색 및 발견 문제

Search 도구, `@file` 언급, 사용자 정의 에이전트 및 사용자 정의 skills가 작동하지 않으면 시스템 `ripgrep`을 설치하세요:

```bash  theme={null}
# macOS (Homebrew)  
brew install ripgrep

# Windows (winget)
winget install BurntSushi.ripgrep.MSVC

# Ubuntu/Debian
sudo apt install ripgrep

# Alpine Linux
apk add ripgrep

# Arch Linux
pacman -S ripgrep
```

그런 다음 [환경](/ko/env-vars)에서 `USE_BUILTIN_RIPGREP=0`을 설정하세요.

### WSL에서 느리거나 불완전한 검색 결과

[WSL에서 파일 시스템 간 작업](https://learn.microsoft.com/en-us/windows/wsl/filesystems)할 때 디스크 읽기 성능 저하로 인해 WSL에서 Claude Code를 사용할 때 예상보다 적은 일치 항목이 발생할 수 있습니다. 검색은 여전히 작동하지만 네이티브 파일 시스템보다 적은 결과를 반환합니다.

<Note>
  이 경우 `/doctor`는 검색을 OK로 표시합니다.
</Note>

**해결책:**

1. **더 구체적인 검색 제출**: 디렉토리 또는 파일 유형을 지정하여 검색되는 파일 수를 줄이세요: "auth-service 패키지에서 JWT 검증 로직 검색" 또는 "JS 파일에서 md5 해시 사용 찾기".

2. **프로젝트를 Linux 파일 시스템으로 이동**: 가능하면 프로젝트가 Windows 파일 시스템(`/mnt/c/`) 대신 Linux 파일 시스템(`/home/`)에 있는지 확인하세요.

3. **Windows 기본 사용**: 더 나은 파일 시스템 성능을 위해 WSL 대신 Windows에서 기본적으로 Claude Code를 실행하는 것을 고려하세요.

## IDE 통합 문제

Claude Code가 IDE에 연결되지 않거나 IDE 터미널 내에서 예기치 않게 동작하면 아래 해결책을 시도하세요.

### WSL2에서 JetBrains IDE 감지 안 됨

WSL2에서 Claude Code를 사용하고 JetBrains IDE를 사용하며 "No available IDEs detected" 오류가 발생하면 WSL2의 네트워킹 구성 또는 Windows 방화벽이 연결을 차단할 가능성이 높습니다.

#### WSL2 네트워킹 모드

WSL2는 기본적으로 NAT 네트워킹을 사용하므로 IDE 감지를 방지할 수 있습니다. 두 가지 옵션이 있습니다:

**옵션 1: Windows 방화벽 구성** (권장)

1. WSL2 IP 주소 찾기:
   ```bash  theme={null}
   wsl hostname -I
   # 예제 출력: 172.21.123.45
   ```

2. PowerShell을 관리자로 열고 방화벽 규칙을 만드세요:
   ```powershell  theme={null}
   New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
   ```
   1단계의 WSL2 서브넷을 기반으로 IP 범위를 조정하세요.

3. IDE와 Claude Code를 모두 다시 시작하세요

**옵션 2: 미러링된 네트워킹으로 전환**

Windows 사용자 디렉토리의 `.wslconfig`에 추가하세요:

```ini  theme={null}
[wsl2]
networkingMode=mirrored
```

그런 다음 PowerShell에서 `wsl --shutdown`으로 WSL을 다시 시작하세요.

<Note>
  이러한 네트워킹 문제는 WSL2에만 영향을 미칩니다. WSL1은 호스트의 네트워크를 직접 사용하며 이러한 구성이 필요하지 않습니다.
</Note>

추가 JetBrains 구성 팁은 [JetBrains IDE 가이드](/ko/jetbrains#plugin-settings)를 참조하세요.

### Windows IDE 통합 문제 보고

Windows에서 IDE 통합 문제가 발생하는 경우 다음 정보와 함께 [이슈를 생성](https://github.com/anthropics/claude-code/issues)하세요:

* 환경 유형: 네이티브 Windows (Git Bash) 또는 WSL1/WSL2
* WSL 네트워킹 모드 (해당하는 경우): NAT 또는 미러링됨
* IDE 이름 및 버전
* Claude Code 확장/플러그인 버전
* 셸 유형: Bash, Zsh, PowerShell 등

### JetBrains IDE 터미널에서 Escape 키가 작동하지 않음

JetBrains 터미널에서 Claude Code를 사용하고 `Esc` 키가 예상대로 에이전트를 중단하지 않으면 JetBrains의 기본 단축키와 키 바인딩이 충돌할 가능성이 높습니다.

이 문제를 해결하려면:

1. 설정 → 도구 → 터미널로 이동하세요
2. 다음 중 하나를 수행하세요:
   * "Move focus to the editor with Escape" 선택 해제, 또는
   * "Configure terminal keybindings"을 클릭하고 "Switch focus to Editor" 단축키 삭제
3. 변경 사항 적용

이렇게 하면 `Esc` 키가 Claude Code 작업을 제대로 중단할 수 있습니다.

## Markdown 형식 문제

Claude Code는 때때로 코드 펜스에 언어 태그가 누락된 markdown 파일을 생성하므로 GitHub, 편집기 및 문서 도구에서 구문 강조 및 가독성에 영향을 미칠 수 있습니다.

### 코드 블록의 누락된 언어 태그

생성된 markdown에서 다음과 같은 코드 블록을 발견하면:

````markdown  theme={null}
```
function example() {
  return "hello";
}
```text
````

다음과 같이 적절히 태그된 블록 대신:

````markdown  theme={null}
```javascript
function example() {
  return "hello";
}
```text
````

**해결책:**

1. **Claude에게 언어 태그 추가 요청**: "이 markdown 파일의 모든 코드 블록에 적절한 언어 태그를 추가하세요."라고 요청하세요.

2. **사후 처리 hooks 사용**: 누락된 언어 태그를 감지하고 추가하는 자동 형식 지정 hooks를 설정하세요. [편집 후 자동 형식](/ko/hooks-guide#auto-format-code-after-edits)에서 PostToolUse 형식 지정 hook의 예를 참조하세요.

3. **수동 확인**: markdown 파일을 생성한 후 적절한 코드 블록 형식을 검토하고 필요하면 수정을 요청하세요.

### 일관성 없는 간격 및 형식

생성된 markdown에 과도한 빈 줄이나 일관성 없는 간격이 있으면:

**해결책:**

1. **형식 수정 요청**: Claude에게 "이 markdown 파일의 간격 및 형식 문제를 수정하세요."라고 요청하세요.

2. **형식 지정 도구 사용**: `prettier` 또는 사용자 정의 형식 지정 스크립트와 같은 markdown 포매터를 실행하는 hooks를 설정하세요.

3. **형식 지정 기본 설정 지정**: 프롬프트 또는 프로젝트 [메모리](/ko/memory) 파일에 형식 지정 요구 사항을 포함하세요.

### Markdown 형식 문제 감소

형식 지정 문제를 최소화하려면:

* **요청에서 명시적**: "언어 태그가 있는 코드 블록이 있는 적절히 형식된 markdown"을 요청하세요
* **프로젝트 규칙 사용**: [`CLAUDE.md`](/ko/memory)에서 선호하는 markdown 스타일을 문서화하세요
* **검증 hooks 설정**: 사후 처리 hooks를 사용하여 일반적인 형식 지정 문제를 자동으로 확인하고 수정하세요

## 추가 도움 받기

여기에 다루지 않은 문제가 발생하는 경우:

1. Claude Code 내에서 `/bug` 명령을 사용하여 Anthropic에 문제를 직접 보고하세요
2. [GitHub 저장소](https://github.com/anthropics/claude-code)에서 알려진 문제를 확인하세요
3. `/doctor`를 실행하여 문제를 진단하세요. 다음을 확인합니다:
   * 설치 유형, 버전 및 검색 기능
   * 자동 업데이트 상태 및 사용 가능한 버전
   * 잘못된 설정 파일 (형식이 잘못된 JSON, 잘못된 유형)
   * MCP 서버 구성 오류
   * 키 바인딩 구성 문제
   * 컨텍스트 사용 경고 (큰 CLAUDE.md 파일, 높은 MCP 토큰 사용량, 도달할 수 없는 권한 규칙)
   * 플러그인 및 에이전트 로딩 오류
4. Claude에게 직접 기능 및 특징에 대해 물어보세요 - Claude는 문서에 대한 기본 제공 액세스 권한이 있습니다
