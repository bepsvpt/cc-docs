> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 문제 해결

> Claude Code에서 높은 CPU 또는 메모리 사용량, 중단, 자동 압축 스래싱 및 검색 문제를 해결하고 다른 문제에 대한 올바른 페이지를 찾습니다.

이 페이지는 Claude Code가 실행 중일 때의 성능, 안정성 및 검색 문제를 다룹니다. 다른 문제의 경우 문제가 있는 위치와 일치하는 페이지부터 시작하세요:

| 증상                                                                                       | 이동                                                                  |
| :--------------------------------------------------------------------------------------- | :------------------------------------------------------------------ |
| `command not found`, 설치 실패, PATH 문제, `EACCES`, TLS 오류                                    | [설치 및 로그인 문제 해결](/ko/troubleshoot-install)                          |
| 로그인 루프, OAuth 오류, `403 Forbidden`, "organization disabled", Bedrock/Vertex/Foundry 자격 증명 | [설치 및 로그인 문제 해결](/ko/troubleshoot-install#login-and-authentication) |
| 설정이 적용되지 않음, hooks가 실행되지 않음, MCP 서버가 로드되지 않음                                             | [구성 디버깅](/ko/debug-your-config)                                     |
| `API Error: 5xx`, `529 Overloaded`, `429`, 요청 검증 오류                                      | [오류 참조](/ko/errors)                                                 |
| `model not found` 또는 `you may not have access to it`                                     | [오류 참조](/ko/errors#theres-an-issue-with-the-selected-model)         |
| VS Code 확장이 Claude에 연결되지 않거나 감지하지 못함                                                     | [VS Code 통합](/ko/vs-code#fix-common-issues)                         |
| JetBrains 플러그인 또는 IDE가 감지되지 않음                                                           | [JetBrains 통합](/ko/jetbrains#troubleshooting)                       |
| 높은 CPU 또는 메모리, 느린 응답, 중단, 검색이 파일을 찾지 못함                                                  | [성능 및 안정성](#performance-and-stability) 아래                           |

어떤 것이 적용되는지 확실하지 않으면 Claude Code 내에서 `/doctor`를 실행하여 설치, 설정, MCP 서버 및 컨텍스트 사용을 자동으로 확인하세요. `claude`가 전혀 시작되지 않으면 셸에서 `claude doctor`를 대신 실행하세요.

## 성능 및 안정성

이 섹션에서는 리소스 사용, 응답성 및 검색 동작과 관련된 문제를 다룹니다.

### 높은 CPU 또는 메모리 사용량

Claude Code는 대부분의 개발 환경에서 작동하도록 설계되었지만 대규모 코드베이스를 처리할 때 상당한 리소스를 소비할 수 있습니다. 성능 문제가 발생하는 경우:

1. `/compact`를 정기적으로 사용하여 컨텍스트 크기 감소
2. 주요 작업 사이에 Claude Code 닫기 및 다시 시작
3. 큰 빌드 디렉토리를 `.gitignore` 파일에 추가하는 것을 고려하세요

메모리 사용량이 이 단계 후에도 높게 유지되면 `/heapdump`를 실행하여 JavaScript 힙 스냅샷과 메모리 분석을 `~/Desktop`에 작성하세요. Linux에 Desktop 폴더가 없으면 파일이 홈 디렉토리에 작성됩니다.

분석은 상주 집합 크기, JS 힙, 배열 버퍼 및 설명되지 않은 네이티브 메모리를 표시하며, 이는 증가가 JavaScript 객체인지 네이티브 코드인지 식별하는 데 도움이 됩니다. Chrome DevTools의 메모리 → 로드에서 `.heapsnapshot` 파일을 열어 보유자를 검사하세요. [GitHub](https://github.com/anthropics/claude-code/issues)에서 메모리 문제를 보고할 때 두 파일을 모두 첨부하세요.

### 자동 압축이 스래싱 오류로 중단됨

`Autocompact is thrashing: the context refilled to the limit...`이 표시되면 자동 압축이 성공했지만 파일 또는 도구 출력이 즉시 컨텍스트 창을 여러 번 연속으로 다시 채웠습니다. Claude Code는 진행되지 않는 루프에서 API 호출을 낭비하지 않기 위해 재시도를 중단합니다.

복구하려면:

1. Claude에게 전체 파일 대신 특정 줄 범위 또는 함수와 같은 더 작은 청크로 큰 파일을 읽도록 요청하세요
2. 큰 출력을 삭제하는 포커스로 `/compact`를 실행하세요. 예: `/compact keep only the plan and the diff`
3. 큰 파일 작업을 [서브에이전트](/ko/sub-agents)로 이동하여 별도의 컨텍스트 창에서 실행하세요
4. 이전 대화가 더 이상 필요하지 않으면 `/clear`를 실행하세요

### 명령 중단 또는 정지

Claude Code가 응답하지 않는 것처럼 보이면:

1. Ctrl+C를 눌러 현재 작업을 취소하세요
2. 응답하지 않으면 터미널을 닫고 다시 시작해야 할 수 있습니다

다시 시작해도 대화가 손실되지 않습니다. 같은 디렉토리에서 `claude --resume`을 실행하여 세션을 다시 시작하세요.

### 검색 및 발견 문제

Search 도구, `@file` 언급, 사용자 정의 에이전트 또는 사용자 정의 skills가 파일을 찾지 못하면 번들된 `ripgrep` 바이너리가 시스템에서 실행되지 않을 수 있습니다. 플랫폼의 `ripgrep` 패키지를 설치하고 Claude Code에 대신 사용하도록 지시하세요:

<Tabs>
  <Tab title="macOS">
    ```bash theme={null}
    brew install ripgrep
    ```
  </Tab>

  <Tab title="Ubuntu/Debian">
    ```bash theme={null}
    sudo apt install ripgrep
    ```
  </Tab>

  <Tab title="Alpine">
    ```bash theme={null}
    apk add ripgrep
    ```
  </Tab>

  <Tab title="Arch">
    ```bash theme={null}
    pacman -S ripgrep
    ```
  </Tab>

  <Tab title="Windows">
    ```powershell theme={null}
    winget install BurntSushi.ripgrep.MSVC
    ```
  </Tab>
</Tabs>

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

## 추가 도움 받기

여기에 다루지 않은 문제가 발생하는 경우:

1. `/doctor`를 실행하여 설치 상태, 설정 유효성, MCP 구성 및 컨텍스트 사용을 한 번에 확인하세요
2. Claude Code 내에서 `/feedback` 명령을 사용하여 Anthropic에 문제를 직접 보고하세요
3. [GitHub 저장소](https://github.com/anthropics/claude-code)에서 알려진 문제를 확인하세요
4. Claude에게 직접 기능 및 특징에 대해 물어보세요. Claude는 문서에 대한 기본 제공 액세스 권한이 있습니다.
