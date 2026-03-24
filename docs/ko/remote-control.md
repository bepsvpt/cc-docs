> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 모든 기기에서 로컬 세션 계속하기 (Remote Control)

> Remote Control을 사용하여 휴대폰, 태블릿 또는 모든 브라우저에서 로컬 Claude Code 세션을 계속할 수 있습니다. claude.ai/code 및 Claude 모바일 앱과 함께 작동합니다.

<Note>
  Remote Control은 모든 요금제에서 사용할 수 있습니다. Team 및 Enterprise 관리자는 먼저 [관리자 설정](https://claude.ai/admin-settings/claude-code)에서 Claude Code를 활성화해야 합니다.
</Note>

Remote Control은 [claude.ai/code](https://claude.ai/code) 또는 [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) 및 [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude)용 Claude 앱을 컴퓨터에서 실행 중인 Claude Code 세션에 연결합니다. 책상에서 작업을 시작한 다음 소파의 휴대폰이나 다른 컴퓨터의 브라우저에서 계속할 수 있습니다.

컴퓨터에서 Remote Control 세션을 시작하면 Claude는 전체 시간 동안 로컬에서 실행되므로 클라우드로 이동하는 것이 없습니다. Remote Control을 사용하면 다음을 수행할 수 있습니다:

* **전체 로컬 환경을 원격으로 사용**: 파일 시스템, [MCP servers](/ko/mcp), 도구 및 프로젝트 구성이 모두 사용 가능하게 유지됩니다
* **두 표면에서 동시에 작업**: 대화가 모든 연결된 기기에서 동기화되므로 터미널, 브라우저 및 휴대폰에서 메시지를 교대로 보낼 수 있습니다
* **중단 극복**: 노트북이 절전 모드로 전환되거나 네트워크가 끊어지면 컴퓨터가 다시 온라인 상태가 될 때 세션이 자동으로 다시 연결됩니다

클라우드 인프라에서 실행되는 [웹의 Claude Code](/ko/claude-code-on-the-web)와 달리 Remote Control 세션은 컴퓨터에서 직접 실행되며 로컬 파일 시스템과 상호 작용합니다. 웹 및 모바일 인터페이스는 단지 해당 로컬 세션의 창일 뿐입니다.

<Note>
  Remote Control에는 Claude Code v2.1.51 이상이 필요합니다. `claude --version`으로 버전을 확인하세요.
</Note>

이 페이지에서는 설정, 세션을 시작하고 연결하는 방법, Remote Control과 웹의 Claude Code를 비교하는 방법을 다룹니다.

## 요구 사항

Remote Control을 사용하기 전에 환경이 다음 조건을 충족하는지 확인하세요:

* **구독**: Pro, Max, Team 및 Enterprise 요금제에서 사용 가능합니다. Team 및 Enterprise 관리자는 먼저 [관리자 설정](https://claude.ai/admin-settings/claude-code)에서 Claude Code를 활성화해야 합니다. API 키는 지원되지 않습니다.
* **인증**: `claude`를 실행하고 아직 로그인하지 않았다면 `/login`을 사용하여 claude.ai를 통해 로그인하세요.
* **작업 공간 신뢰**: 작업 공간 신뢰 대화를 수락하려면 프로젝트 디렉토리에서 최소한 한 번 `claude`를 실행하세요.

## Remote Control 세션 시작

전용 Remote Control 서버를 시작하거나, Remote Control이 활성화된 대화형 세션을 시작하거나, 이미 실행 중인 세션에 연결할 수 있습니다.

<Tabs>
  <Tab title="서버 모드">
    프로젝트 디렉토리로 이동하여 다음을 실행하세요:

    ```bash  theme={null}
    claude remote-control
    ```

    프로세스는 터미널에서 서버 모드로 계속 실행되어 원격 연결을 기다립니다. [다른 기기에서 연결](#다른-기기에서-연결)하는 데 사용할 수 있는 세션 URL을 표시하며, 스페이스바를 눌러 휴대폰에서 빠르게 액세스할 수 있는 QR 코드를 표시할 수 있습니다. 원격 세션이 활성화되어 있는 동안 터미널은 연결 상태 및 도구 활동을 표시합니다.

    사용 가능한 플래그:

    | 플래그                          | 설명                                                                                                                                                                                                                                                                    |
    | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `--name "My Project"`        | claude.ai/code의 세션 목록에 표시되는 사용자 정의 세션 제목을 설정합니다.                                                                                                                                                                                                                      |
    | `--spawn <mode>`             | 동시 세션이 생성되는 방식입니다. 런타임에 `w`를 눌러 전환하세요.<br />• `same-dir` (기본값): 모든 세션이 현재 작업 디렉토리를 공유하므로 동일한 파일을 편집할 때 충돌할 수 있습니다.<br />• `worktree`: 각 온디맨드 세션은 자체 [git worktree](/ko/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees)를 가져옵니다. git 저장소가 필요합니다. |
    | `--capacity <N>`             | 최대 동시 세션 수입니다. 기본값은 32입니다.                                                                                                                                                                                                                                            |
    | `--verbose`                  | 자세한 연결 및 세션 로그를 표시합니다.                                                                                                                                                                                                                                                |
    | `--sandbox` / `--no-sandbox` | 파일 시스템 및 네트워크 격리를 위해 [샌드박싱](/ko/sandboxing)을 활성화하거나 비활성화합니다. 기본적으로 꺼져 있습니다.                                                                                                                                                                                           |
  </Tab>

  <Tab title="대화형 세션">
    Remote Control이 활성화된 일반 대화형 Claude Code 세션을 시작하려면 `--remote-control` 플래그(또는 `--rc`)를 사용하세요:

    ```bash  theme={null}
    claude --remote-control
    ```

    선택적으로 세션의 이름을 전달하세요:

    ```bash  theme={null}
    claude --remote-control "My Project"
    ```

    이렇게 하면 터미널에서 전체 대화형 세션을 얻을 수 있으며, claude.ai 또는 Claude 앱에서도 제어할 수 있습니다. `claude remote-control`(서버 모드)과 달리 세션이 원격으로도 사용 가능한 동안 로컬에서 메시지를 입력할 수 있습니다.
  </Tab>

  <Tab title="기존 세션에서">
    이미 Claude Code 세션에 있고 원격으로 계속하려면 `/remote-control`(또는 `/rc`) 명령을 사용하세요:

    ```text  theme={null}
    /remote-control
    ```

    인수로 이름을 전달하여 사용자 정의 세션 제목을 설정하세요:

    ```text  theme={null}
    /remote-control My Project
    ```

    이렇게 하면 현재 대화 기록을 이어받는 Remote Control 세션이 시작되며, [다른 기기에서 연결](#다른-기기에서-연결)하는 데 사용할 수 있는 세션 URL 및 QR 코드를 표시합니다. `--verbose`, `--sandbox` 및 `--no-sandbox` 플래그는 이 명령에서 사용할 수 없습니다.
  </Tab>
</Tabs>

### 다른 기기에서 연결

Remote Control 세션이 활성화되면 다른 기기에서 연결하는 몇 가지 방법이 있습니다:

* **세션 URL 열기**: 모든 브라우저에서 URL을 열어 [claude.ai/code](https://claude.ai/code)의 세션으로 직접 이동합니다. `claude remote-control`과 `/remote-control` 모두 이 URL을 터미널에 표시합니다.
* **QR 코드 스캔**: 세션 URL 옆에 표시된 QR 코드를 스캔하여 Claude 앱에서 직접 열 수 있습니다. `claude remote-control`을 사용하면 스페이스바를 눌러 QR 코드 표시를 전환할 수 있습니다.
* **[claude.ai/code](https://claude.ai/code) 또는 Claude 앱 열기**: 세션 목록에서 이름으로 세션을 찾습니다. Remote Control 세션은 온라인 상태일 때 녹색 상태 점이 있는 컴퓨터 아이콘을 표시합니다.

원격 세션은 `--name` 인수(또는 `/remote-control`에 전달된 이름), 마지막 메시지, `/rename` 값 또는 대화 기록이 없으면 "Remote Control session"에서 이름을 가져옵니다. 환경에 이미 활성 세션이 있으면 계속할지 새로 시작할지 묻는 메시지가 표시됩니다.

Claude 앱이 아직 없으면 Claude Code 내에서 `/mobile` 명령을 사용하여 [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) 또는 [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude)용 다운로드 QR 코드를 표시하세요.

### 모든 세션에 대해 Remote Control 활성화

기본적으로 Remote Control은 `claude remote-control`, `claude --remote-control` 또는 `/remote-control`을 명시적으로 실행할 때만 활성화됩니다. 모든 대화형 세션에 대해 자동으로 활성화하려면 Claude Code 내에서 `/config`를 실행하고 **모든 세션에 대해 Remote Control 활성화**를 `true`로 설정하세요. 비활성화하려면 `false`로 다시 설정하세요.

이 설정이 켜져 있으면 각 대화형 Claude Code 프로세스는 하나의 원격 세션을 등록합니다. 여러 인스턴스를 실행하면 각각 자체 환경 및 세션을 가져옵니다. 단일 프로세스에서 여러 동시 세션을 실행하려면 대신 `--spawn`과 함께 서버 모드를 사용하세요.

## 연결 및 보안

로컬 Claude Code 세션은 아웃바운드 HTTPS 요청만 수행하며 컴퓨터에서 인바운드 포트를 열지 않습니다. Remote Control을 시작하면 Anthropic API에 등록되고 작업을 폴링합니다. 다른 기기에서 연결하면 서버는 웹 또는 모바일 클라이언트와 로컬 세션 간의 메시지를 스트리밍 연결을 통해 라우팅합니다.

모든 트래픽은 TLS를 통해 Anthropic API를 통해 이동하며, 이는 모든 Claude Code 세션과 동일한 전송 보안입니다. 연결은 각각 단일 목적으로 범위가 지정되고 독립적으로 만료되는 여러 단기 자격 증명을 사용합니다.

## Remote Control과 웹의 Claude Code 비교

Remote Control과 [웹의 Claude Code](/ko/claude-code-on-the-web)는 모두 claude.ai/code 인터페이스를 사용합니다. 주요 차이점은 세션이 실행되는 위치입니다: Remote Control은 컴퓨터에서 실행되므로 로컬 MCP servers, 도구 및 프로젝트 구성이 사용 가능하게 유지됩니다. 웹의 Claude Code는 Anthropic 관리 클라우드 인프라에서 실행됩니다.

로컬 작업 중간에 있고 다른 기기에서 계속하려고 할 때 Remote Control을 사용하세요. 로컬 설정 없이 작업을 시작하거나, 복제하지 않은 저장소에서 작업하거나, 여러 작업을 병렬로 실행하려고 할 때 웹의 Claude Code를 사용하세요.

## 제한 사항

* **대화형 프로세스당 하나의 원격 세션**: 서버 모드 외부에서 각 Claude Code 인스턴스는 한 번에 하나의 원격 세션을 지원합니다. 단일 프로세스에서 여러 동시 세션을 실행하려면 `--spawn`과 함께 서버 모드를 사용하세요.
* **터미널은 열려 있어야 함**: Remote Control은 로컬 프로세스로 실행됩니다. 터미널을 닫거나 `claude` 프로세스를 중지하면 세션이 종료됩니다. 새 세션을 시작하려면 `claude remote-control`을 다시 실행하세요.
* **장시간 네트워크 중단**: 컴퓨터가 켜져 있지만 약 10분 이상 네트워크에 도달할 수 없으면 세션이 시간 초과되고 프로세스가 종료됩니다. 새 세션을 시작하려면 `claude remote-control`을 다시 실행하세요.

## 관련 리소스

* [웹의 Claude Code](/ko/claude-code-on-the-web): 컴퓨터 대신 Anthropic 관리 클라우드 환경에서 세션 실행
* [인증](/ko/authentication): `/login` 설정 및 claude.ai 자격 증명 관리
* [CLI 참조](/ko/cli-reference): `claude remote-control`을 포함한 플래그 및 명령의 전체 목록
* [보안](/ko/security): Remote Control 세션이 Claude Code 보안 모델에 어떻게 적합한지
* [데이터 사용](/ko/data-usage): 로컬 및 원격 세션 중에 Anthropic API를 통해 흐르는 데이터
