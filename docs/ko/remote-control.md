> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 모든 기기에서 로컬 세션 계속하기 (Remote Control)

> Remote Control을 사용하여 휴대폰, 태블릿 또는 모든 브라우저에서 로컬 Claude Code 세션을 계속할 수 있습니다. claude.ai/code 및 Claude 모바일 앱과 함께 작동합니다.

<Note>
  Remote Control은 모든 요금제에서 사용할 수 있습니다. Team 및 Enterprise의 경우 관리자가 [Claude Code 관리자 설정](https://claude.ai/admin-settings/claude-code)에서 Remote Control 토글을 활성화할 때까지 기본적으로 꺼져 있습니다.
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

* **구독**: Pro, Max, Team 및 Enterprise 요금제에서 사용 가능합니다. API 키는 지원되지 않습니다. Team 및 Enterprise의 경우 관리자가 먼저 [Claude Code 관리자 설정](https://claude.ai/admin-settings/claude-code)에서 Remote Control 토글을 활성화해야 합니다.
* **인증**: `claude`를 실행하고 아직 로그인하지 않았다면 `/login`을 사용하여 claude.ai를 통해 로그인하세요.
* **작업 공간 신뢰**: 작업 공간 신뢰 대화를 수락하려면 프로젝트 디렉토리에서 최소한 한 번 `claude`를 실행하세요.

## Remote Control 세션 시작

CLI 또는 VS Code 확장에서 Remote Control 세션을 시작할 수 있습니다. CLI는 세 가지 호출 모드를 제공하며, VS Code는 `/remote-control` 명령을 사용합니다.

<Tabs>
  <Tab title="서버 모드">
    프로젝트 디렉토리로 이동하여 다음을 실행하세요:

    ```bash theme={null}
    claude remote-control
    ```

    프로세스는 터미널에서 서버 모드로 계속 실행되어 원격 연결을 기다립니다. [다른 기기에서 연결](#다른-기기에서-연결)하는 데 사용할 수 있는 세션 URL을 표시하며, 스페이스바를 눌러 휴대폰에서 빠르게 액세스할 수 있는 QR 코드를 표시할 수 있습니다. 원격 세션이 활성화되어 있는 동안 터미널은 연결 상태 및 도구 활동을 표시합니다.

    사용 가능한 플래그:

    | 플래그                                             | 설명                                                                                                                                                                                                                                                                                                                                                                                 |
    | ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `--name "My Project"`                           | claude.ai/code의 세션 목록에 표시되는 사용자 정의 세션 제목을 설정합니다.                                                                                                                                                                                                                                                                                                                                   |
    | `--remote-control-session-name-prefix <prefix>` | 명시적 이름이 설정되지 않았을 때 자동 생성된 세션 이름의 접두사입니다. 기본값은 컴퓨터의 호스트 이름이며, `myhost-graceful-unicorn`과 같은 이름을 생성합니다. 동일한 효과를 위해 `CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX`를 설정하세요.                                                                                                                                                                                                               |
    | `--spawn <mode>`                                | 서버가 세션을 생성하는 방식입니다.<br />• `same-dir` (기본값): 모든 세션이 현재 작업 디렉토리를 공유하므로 동일한 파일을 편집할 때 충돌할 수 있습니다.<br />• `worktree`: 각 온디맨드 세션은 자체 [git worktree](/ko/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees)를 가져옵니다. git 저장소가 필요합니다.<br />• `session`: 단일 세션 모드입니다. 정확히 하나의 세션을 제공하고 추가 연결을 거부합니다. 시작 시에만 설정합니다.<br />런타임에 `w`를 눌러 `same-dir`과 `worktree` 사이를 전환하세요. |
    | `--capacity <N>`                                | 최대 동시 세션 수입니다. 기본값은 32입니다. `--spawn=session`과 함께 사용할 수 없습니다.                                                                                                                                                                                                                                                                                                                       |
    | `--verbose`                                     | 자세한 연결 및 세션 로그를 표시합니다.                                                                                                                                                                                                                                                                                                                                                             |
    | `--sandbox` / `--no-sandbox`                    | 파일 시스템 및 네트워크 격리를 위해 [샌드박싱](/ko/sandboxing)을 활성화하거나 비활성화합니다. 기본적으로 꺼져 있습니다.                                                                                                                                                                                                                                                                                                        |
  </Tab>

  <Tab title="대화형 세션">
    Remote Control이 활성화된 일반 대화형 Claude Code 세션을 시작하려면 `--remote-control` 플래그(또는 `--rc`)를 사용하세요:

    ```bash theme={null}
    claude --remote-control
    ```

    선택적으로 세션의 이름을 전달하세요:

    ```bash theme={null}
    claude --remote-control "My Project"
    ```

    이렇게 하면 터미널에서 전체 대화형 세션을 얻을 수 있으며, claude.ai 또는 Claude 앱에서도 제어할 수 있습니다. `claude remote-control`(서버 모드)과 달리 세션이 원격으로도 사용 가능한 동안 로컬에서 메시지를 입력할 수 있습니다.
  </Tab>

  <Tab title="기존 세션에서">
    이미 Claude Code 세션에 있고 원격으로 계속하려면 `/remote-control`(또는 `/rc`) 명령을 사용하세요:

    ```text theme={null}
    /remote-control
    ```

    인수로 이름을 전달하여 사용자 정의 세션 제목을 설정하세요:

    ```text theme={null}
    /remote-control My Project
    ```

    이렇게 하면 현재 대화 기록을 이어받는 Remote Control 세션이 시작되며, [다른 기기에서 연결](#다른-기기에서-연결)하는 데 사용할 수 있는 세션 URL 및 QR 코드를 표시합니다. `--verbose`, `--sandbox` 및 `--no-sandbox` 플래그는 이 명령에서 사용할 수 없습니다.
  </Tab>

  <Tab title="VS Code">
    [Claude Code VS Code 확장](/ko/vs-code)에서 프롬프트 상자에 `/remote-control` 또는 `/rc`를 입력하거나 `/`로 명령 메뉴를 열고 선택하세요. Claude Code v2.1.79 이상이 필요합니다.

    ```text theme={null}
    /remote-control
    ```

    프롬프트 상자 위에 연결 상태를 표시하는 배너가 나타납니다. 연결되면 배너의 **브라우저에서 열기**를 클릭하여 세션으로 직접 이동하거나 [claude.ai/code](https://claude.ai/code)의 세션 목록에서 찾으세요. 세션 URL도 대화에 게시됩니다.

    연결을 끊으려면 배너의 닫기 아이콘을 클릭하거나 `/remote-control`을 다시 실행하세요.

    CLI와 달리 VS Code 명령은 이름 인수를 허용하지 않으며 QR 코드를 표시하지 않습니다. 세션 제목은 대화 기록 또는 첫 번째 프롬프트에서 파생됩니다.
  </Tab>
</Tabs>

### 다른 기기에서 연결

Remote Control 세션이 활성화되면 다른 기기에서 연결하는 몇 가지 방법이 있습니다:

* **세션 URL 열기**: 모든 브라우저에서 URL을 열어 [claude.ai/code](https://claude.ai/code)의 세션으로 직접 이동합니다.
* **QR 코드 스캔**: 세션 URL 옆에 표시된 QR 코드를 스캔하여 Claude 앱에서 직접 열 수 있습니다. `claude remote-control`을 사용하면 스페이스바를 눌러 QR 코드 표시를 전환할 수 있습니다.
* **[claude.ai/code](https://claude.ai/code) 또는 Claude 앱 열기**: 세션 목록에서 이름으로 세션을 찾습니다. Remote Control 세션은 온라인 상태일 때 녹색 상태 점이 있는 컴퓨터 아이콘을 표시합니다.

원격 세션 제목은 다음 순서로 선택됩니다:

1. `--name`, `--remote-control` 또는 `/remote-control`에 전달한 이름
2. `/rename`으로 설정한 제목
3. 기존 대화 기록의 마지막 의미 있는 메시지
4. `myhost-graceful-unicorn`과 같은 자동 생성된 이름입니다. 여기서 `myhost`는 컴퓨터의 호스트 이름 또는 `--remote-control-session-name-prefix`로 설정한 접두사입니다.

명시적 이름을 설정하지 않았다면 메시지를 보낸 후 제목이 프롬프트를 반영하도록 업데이트됩니다.

환경에 이미 활성 세션이 있으면 계속할지 새로 시작할지 묻는 메시지가 표시됩니다.

Claude 앱이 아직 없으면 Claude Code 내에서 `/mobile` 명령을 사용하여 [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) 또는 [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude)용 다운로드 QR 코드를 표시하세요.

### 모든 세션에 대해 Remote Control 활성화

기본적으로 Remote Control은 `claude remote-control`, `claude --remote-control` 또는 `/remote-control`을 명시적으로 실행할 때만 활성화됩니다. 모든 대화형 세션에 대해 자동으로 활성화하려면 Claude Code 내에서 `/config`를 실행하고 **모든 세션에 대해 Remote Control 활성화**를 `true`로 설정하세요. 비활성화하려면 `false`로 다시 설정하세요.

이 설정이 켜져 있으면 각 대화형 Claude Code 프로세스는 하나의 원격 세션을 등록합니다. 여러 인스턴스를 실행하면 각각 자체 환경 및 세션을 가져옵니다. 단일 프로세스에서 여러 동시 세션을 실행하려면 [서버 모드](#remote-control-세션-시작)를 대신 사용하세요.

## 연결 및 보안

로컬 Claude Code 세션은 아웃바운드 HTTPS 요청만 수행하며 컴퓨터에서 인바운드 포트를 열지 않습니다. Remote Control을 시작하면 Anthropic API에 등록되고 작업을 폴링합니다. 다른 기기에서 연결하면 서버는 웹 또는 모바일 클라이언트와 로컬 세션 간의 메시지를 스트리밍 연결을 통해 라우팅합니다.

모든 트래픽은 TLS를 통해 Anthropic API를 통해 이동하며, 이는 모든 Claude Code 세션과 동일한 전송 보안입니다. 연결은 각각 단일 목적으로 범위가 지정되고 독립적으로 만료되는 여러 단기 자격 증명을 사용합니다.

## Remote Control과 웹의 Claude Code 비교

Remote Control과 [웹의 Claude Code](/ko/claude-code-on-the-web)는 모두 claude.ai/code 인터페이스를 사용합니다. 주요 차이점은 세션이 실행되는 위치입니다: Remote Control은 컴퓨터에서 실행되므로 로컬 MCP servers, 도구 및 프로젝트 구성이 사용 가능하게 유지됩니다. 웹의 Claude Code는 Anthropic 관리 클라우드 인프라에서 실행됩니다.

로컬 작업 중간에 있고 다른 기기에서 계속하려고 할 때 Remote Control을 사용하세요. 로컬 설정 없이 작업을 시작하거나, 복제하지 않은 저장소에서 작업하거나, 여러 작업을 병렬로 실행하려고 할 때 웹의 Claude Code를 사용하세요.

## 모바일 푸시 알림

Remote Control이 활성화되면 Claude는 휴대폰으로 푸시 알림을 보낼 수 있습니다.

Claude는 언제 푸시할지 결정합니다. 일반적으로 오래 실행되는 작업이 완료되거나 계속하기 위해 사용자의 결정이 필요할 때 하나를 보냅니다. 프롬프트에서 푸시를 요청할 수도 있습니다. 예를 들어 `테스트가 완료되면 알려주세요`. 아래의 켜기/끄기 토글 외에는 이벤트별 구성이 없습니다.

<Note>
  모바일 푸시 알림에는 Claude Code v2.1.110 이상이 필요합니다.
</Note>

모바일 푸시 알림을 설정하려면:

<Steps>
  <Step title="Claude 모바일 앱 설치">
    [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) 또는 [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude)용 Claude 앱을 다운로드하세요.
  </Step>

  <Step title="Claude Code 계정으로 로그인">
    터미널에서 Claude Code에 사용하는 동일한 계정 및 조직을 사용하세요.
  </Step>

  <Step title="알림 허용">
    운영 체제의 알림 권한 프롬프트를 수락하세요.
  </Step>

  <Step title="Claude Code에서 푸시 활성화">
    터미널에서 `/config`를 실행하고 **Claude가 결정할 때 푸시**를 활성화하세요.
  </Step>
</Steps>

알림이 도착하지 않으면:

* `/config`에 **등록된 모바일 없음**이 표시되면 휴대폰에서 Claude 앱을 열어 푸시 토큰을 새로 고칠 수 있습니다. Remote Control이 다음에 연결할 때 경고가 지워집니다.
* iOS에서 포커스 모드 및 알림 요약이 푸시를 억제하거나 지연시킬 수 있습니다. 설정 → 알림 → Claude를 확인하세요.
* Android에서 적극적인 배터리 최적화가 전달을 지연시킬 수 있습니다. 시스템 설정에서 Claude 앱을 배터리 최적화에서 제외하세요.

## 제한 사항

* **대화형 프로세스당 하나의 원격 세션**: 서버 모드 외부에서 각 Claude Code 인스턴스는 한 번에 하나의 원격 세션을 지원합니다. 단일 프로세스에서 여러 동시 세션을 실행하려면 [서버 모드](#remote-control-세션-시작)를 사용하세요.
* **로컬 프로세스는 계속 실행되어야 함**: Remote Control은 로컬 프로세스로 실행됩니다. 터미널을 닫거나, VS Code를 종료하거나, 다른 방식으로 `claude` 프로세스를 중지하면 세션이 종료됩니다.
* **장시간 네트워크 중단**: 컴퓨터가 켜져 있지만 약 10분 이상 네트워크에 도달할 수 없으면 세션이 시간 초과되고 프로세스가 종료됩니다. `claude remote-control`을 다시 실행하여 새 세션을 시작하세요.
* **Ultraplan이 Remote Control 연결 해제**: [ultraplan](/ko/ultraplan) 세션을 시작하면 활성 Remote Control 세션이 연결 해제됩니다. 두 기능 모두 claude.ai/code 인터페이스를 차지하고 한 번에 하나만 연결될 수 있기 때문입니다.

## 문제 해결

### "Remote Control에는 claude.ai 구독이 필요합니다"

claude.ai 계정으로 인증되지 않았습니다. `claude auth login`을 실행하고 claude.ai 옵션을 선택하세요. `ANTHROPIC_API_KEY`가 환경에 설정되어 있으면 먼저 설정을 해제하세요.

### "Remote Control에는 전체 범위 로그인 토큰이 필요합니다"

`claude setup-token` 또는 `CLAUDE_CODE_OAUTH_TOKEN` 환경 변수의 장기 토큰으로 인증되었습니다. 이러한 토큰은 추론 전용으로 제한되며 Remote Control 세션을 설정할 수 없습니다. 대신 `claude auth login`을 실행하여 전체 범위 세션 토큰으로 인증하세요.

### "Remote Control 적격성을 위해 조직을 결정할 수 없습니다"

캐시된 계정 정보가 오래되었거나 불완전합니다. `claude auth login`을 실행하여 새로 고치세요.

### "Remote Control이 아직 계정에 대해 활성화되지 않았습니다"

특정 환경 변수가 있으면 적격성 확인이 실패할 수 있습니다:

* `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 또는 `DISABLE_TELEMETRY`: 설정을 해제하고 다시 시도하세요.
* `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX` 또는 `CLAUDE_CODE_USE_FOUNDRY`: Remote Control은 claude.ai 인증이 필요하며 타사 제공자와 작동하지 않습니다.

이 중 어느 것도 설정되지 않았다면 `/logout`을 실행한 다음 `/login`을 실행하여 새로 고치세요.

### "Remote Control이 조직의 정책에 의해 비활성화되었습니다"

이 오류에는 세 가지 서로 다른 원인이 있습니다. 먼저 `/status`를 실행하여 사용 중인 로그인 방법과 구독을 확인하세요.

* **API 키 또는 Console 계정으로 인증됨**: Remote Control은 claude.ai OAuth가 필요합니다. `/login`을 실행하고 claude.ai 옵션을 선택하세요. `ANTHROPIC_API_KEY`가 환경에 설정되어 있으면 설정을 해제하세요.
* **Team 또는 Enterprise 관리자가 활성화하지 않음**: Remote Control은 이러한 요금제에서 기본적으로 꺼져 있습니다. 관리자는 [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code)에서 **Remote Control** 토글을 켜서 활성화할 수 있습니다. 이는 서버 측 조직 설정이며 [관리 전용 설정](/ko/permissions#managed-only-settings) 키가 아닙니다.
* **관리자 토글이 회색으로 표시됨**: 조직에 Remote Control과 호환되지 않는 데이터 보존 또는 규정 준수 구성이 있습니다. 이는 관리자 패널에서 변경할 수 없습니다. Anthropic 지원팀에 문의하여 옵션을 논의하세요.

### "원격 자격 증명 가져오기 실패"

Claude Code가 Anthropic API에서 연결을 설정하기 위한 단기 자격 증명을 얻을 수 없습니다. `--verbose`로 다시 실행하여 전체 오류를 확인하세요:

```bash theme={null}
claude remote-control --verbose
```

일반적인 원인:

* 로그인하지 않음: `claude`를 실행하고 `/login`을 사용하여 claude.ai 계정으로 인증하세요. API 키 인증은 Remote Control에서 지원되지 않습니다.
* 네트워크 또는 프록시 문제: 방화벽 또는 프록시가 아웃바운드 HTTPS 요청을 차단할 수 있습니다. Remote Control은 포트 443의 Anthropic API에 대한 액세스가 필요합니다.
* 세션 생성 실패: `Session creation failed — see debug log`도 표시되면 설정 초기에 실패가 발생했습니다. 구독이 활성 상태인지 확인하세요.

## 올바른 접근 방식 선택

Claude Code offers several ways to work when you're not at your terminal. They differ in what triggers the work, where Claude runs, and how much you need to set up.

|                                                | Trigger                                                                                        | Claude runs on                                                                               | Setup                                                                                                                                | Best for                                                      |
| :--------------------------------------------- | :--------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------ |
| [Dispatch](/en/desktop#sessions-from-dispatch) | Message a task from the Claude mobile app                                                      | Your machine (Desktop)                                                                       | [Pair the mobile app with Desktop](https://support.claude.com/en/articles/13947068)                                                  | Delegating work while you're away, minimal setup              |
| [Remote Control](/en/remote-control)           | Drive a running session from [claude.ai/code](https://claude.ai/code) or the Claude mobile app | Your machine (CLI or VS Code)                                                                | Run `claude remote-control`                                                                                                          | Steering in-progress work from another device                 |
| [Channels](/en/channels)                       | Push events from a chat app like Telegram or Discord, or your own server                       | Your machine (CLI)                                                                           | [Install a channel plugin](/en/channels#quickstart) or [build your own](/en/channels-reference)                                      | Reacting to external events like CI failures or chat messages |
| [Slack](/en/slack)                             | Mention `@Claude` in a team channel                                                            | Anthropic cloud                                                                              | [Install the Slack app](/en/slack#setting-up-claude-code-in-slack) with [Claude Code on the web](/en/claude-code-on-the-web) enabled | PRs and reviews from team chat                                |
| [Scheduled tasks](/en/scheduled-tasks)         | Set a schedule                                                                                 | [CLI](/en/scheduled-tasks), [Desktop](/en/desktop-scheduled-tasks), or [cloud](/en/routines) | Pick a frequency                                                                                                                     | Recurring automation like daily reviews                       |

## 관련 리소스

* [웹의 Claude Code](/ko/claude-code-on-the-web): 컴퓨터 대신 Anthropic 관리 클라우드 환경에서 세션 실행
* [Ultraplan](/ko/ultraplan): 터미널에서 클라우드 계획 세션을 시작하고 브라우저에서 계획을 검토합니다
* [채널](/ko/channels): Telegram, Discord 또는 iMessage를 세션으로 전달하여 Claude가 자리를 비운 동안 메시지에 반응하도록 합니다
* [Dispatch](/ko/desktop#sessions-from-dispatch): 휴대폰에서 작업을 메시지로 보내면 Desktop 세션을 생성하여 처리할 수 있습니다
* [인증](/ko/authentication): `/login` 설정 및 claude.ai 자격 증명 관리
* [CLI 참조](/ko/cli-reference): `claude remote-control`을 포함한 플래그 및 명령의 전체 목록
* [보안](/ko/security): Remote Control 세션이 Claude Code 보안 모델에 어떻게 적합한지
* [데이터 사용](/ko/data-usage): 로컬 및 원격 세션 중에 Anthropic API를 통해 흐르는 데이터
