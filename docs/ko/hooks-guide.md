> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# hooks를 사용하여 워크플로우 자동화

> Claude Code가 파일을 편집하거나 작업을 완료하거나 입력이 필요할 때 자동으로 셸 명령을 실행합니다. 코드 형식 지정, 알림 전송, 명령 검증 및 프로젝트 규칙 적용.

Hooks는 Claude Code의 라이프사이클의 특정 지점에서 실행되는 사용자 정의 셸 명령입니다. 이들은 Claude Code의 동작에 대한 결정론적 제어를 제공하여 LLM이 실행하도록 선택하는 것에 의존하기보다는 특정 작업이 항상 발생하도록 보장합니다. Hooks를 사용하여 프로젝트 규칙을 적용하고, 반복적인 작업을 자동화하며, Claude Code를 기존 도구와 통합합니다.

판단이 필요한 결정의 경우 결정론적 규칙이 아닌 경우, [프롬프트 기반 hooks](#prompt-based-hooks) 또는 [에이전트 기반 hooks](#agent-based-hooks)를 사용할 수도 있습니다. 이들은 Claude 모델을 사용하여 조건을 평가합니다.

Claude Code를 확장하는 다른 방법은 [skills](/ko/skills)를 참조하여 Claude에 추가 지침과 실행 가능한 명령을 제공하고, [subagents](/ko/sub-agents)를 사용하여 격리된 컨텍스트에서 작업을 실행하며, [plugins](/ko/plugins)를 사용하여 프로젝트 전체에서 공유할 확장을 패키징합니다.

<Tip>
  이 가이드는 일반적인 사용 사례와 시작 방법을 다룹니다. 전체 이벤트 스키마, JSON 입출력 형식 및 비동기 hooks 및 MCP 도구 hooks와 같은 고급 기능은 [Hooks 참조](/ko/hooks)를 참조하세요.
</Tip>

## 첫 번째 hook 설정

Hook을 만들려면 [설정 파일](#configure-hook-location)에 `hooks` 블록을 추가합니다. 이 연습은 데스크톱 알림 hook을 만들므로 Claude가 터미널을 보는 대신 입력을 기다릴 때마다 알림을 받습니다.

<Steps>
  <Step title="설정에 hook 추가">
    `~/.claude/settings.json`을 열고 `Notification` hook을 추가합니다. 아래 예제는 macOS용 `osascript`를 사용합니다. Linux 및 Windows 명령은 [Claude가 입력이 필요할 때 알림 받기](#get-notified-when-claude-needs-input)를 참조하세요.

    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
              }
            ]
          }
        ]
      }
    }
    ```

    설정 파일에 이미 `hooks` 키가 있으면 전체 객체를 바꾸는 대신 `Notification` 항목을 병합합니다. CLI에서 원하는 것을 설명하여 Claude에게 hook을 작성하도록 요청할 수도 있습니다.
  </Step>

  <Step title="구성 확인">
    `/hooks`를 입력하여 hooks 브라우저를 엽니다. 구성된 hooks가 있는 각 이벤트 옆에 개수가 있는 사용 가능한 모든 hook 이벤트 목록이 표시됩니다. `Notification`을 선택하여 새 hook이 목록에 나타나는지 확인합니다. Hook을 선택하면 세부 정보가 표시됩니다: 이벤트, matcher, 유형, 소스 파일 및 명령.
  </Step>

  <Step title="hook 테스트">
    `Esc`를 눌러 CLI로 돌아갑니다. Claude에게 권한이 필요한 작업을 수행하도록 요청한 다음 터미널에서 전환합니다. 데스크톱 알림을 받아야 합니다.
  </Step>
</Steps>

<Tip>
  `/hooks` 메뉴는 읽기 전용입니다. Hooks를 추가, 수정 또는 제거하려면 설정 JSON을 직접 편집하거나 Claude에게 변경을 요청합니다.
</Tip>

## 자동화할 수 있는 것

Hooks를 사용하면 Claude Code의 라이프사이클의 주요 지점에서 코드를 실행할 수 있습니다: 편집 후 파일 형식 지정, 실행 전 명령 차단, Claude가 입력이 필요할 때 알림 전송, 세션 시작 시 컨텍스트 주입 등. 전체 hook 이벤트 목록은 [Hooks 참조](/ko/hooks#hook-lifecycle)를 참조하세요.

각 예제에는 [설정 파일](#configure-hook-location)에 추가하는 즉시 사용 가능한 구성 블록이 포함되어 있습니다. 가장 일반적인 패턴:

* [Claude가 입력이 필요할 때 알림 받기](#get-notified-when-claude-needs-input)
* [편집 후 코드 자동 형식 지정](#auto-format-code-after-edits)
* [보호된 파일에 대한 편집 차단](#block-edits-to-protected-files)
* [압축 후 컨텍스트 다시 주입](#re-inject-context-after-compaction)
* [구성 변경 감사](#audit-configuration-changes)
* [특정 권한 프롬프트 자동 승인](#auto-approve-specific-permission-prompts)

### Claude가 입력이 필요할 때 알림 받기

Claude가 작업을 완료하고 입력이 필요할 때마다 데스크톱 알림을 받으므로 터미널을 확인하지 않고 다른 작업으로 전환할 수 있습니다.

이 hook은 Claude가 입력 또는 권한을 기다릴 때 발생하는 `Notification` 이벤트를 사용합니다. 각 탭은 플랫폼의 기본 알림 명령을 사용합니다. `~/.claude/settings.json`에 추가합니다:

<Tabs>
  <Tab title="macOS">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Linux">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "notify-send 'Claude Code' 'Claude Code needs your attention'"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Windows (PowerShell)">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "powershell.exe -Command \"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')\""
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>
</Tabs>

### 편집 후 코드 자동 형식 지정

Claude가 편집하는 모든 파일에서 [Prettier](https://prettier.io/)를 자동으로 실행하여 수동 개입 없이 형식이 일관되게 유지되도록 합니다.

이 hook은 `PostToolUse` 이벤트를 `Edit|Write` matcher와 함께 사용하므로 파일 편집 도구 후에만 실행됩니다. 명령은 [`jq`](https://jqlang.github.io/jq/)를 사용하여 편집된 파일 경로를 추출하고 Prettier에 전달합니다. 프로젝트 루트의 `.claude/settings.json`에 추가합니다:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

<Note>
  이 페이지의 Bash 예제는 JSON 구문 분석을 위해 `jq`를 사용합니다. `brew install jq` (macOS), `apt-get install jq` (Debian/Ubuntu)로 설치하거나 [`jq` 다운로드](https://jqlang.github.io/jq/download/)를 참조하세요.
</Note>

### 보호된 파일에 대한 편집 차단

Claude가 `.env`, `package-lock.json` 또는 `.git/`의 모든 항목과 같은 민감한 파일을 수정하지 못하도록 방지합니다. Claude는 편집이 차단된 이유를 설명하는 피드백을 받으므로 접근 방식을 조정할 수 있습니다.

이 예제는 hook이 호출하는 별도의 스크립트 파일을 사용합니다. 스크립트는 대상 파일 경로를 보호된 패턴 목록과 비교하고 종료 코드 2로 종료하여 편집을 차단합니다.

<Steps>
  <Step title="hook 스크립트 만들기">
    이를 `.claude/hooks/protect-files.sh`에 저장합니다:

    ```bash  theme={null}
    #!/bin/bash
    # protect-files.sh

    INPUT=$(cat)
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

    PROTECTED_PATTERNS=(".env" "package-lock.json" ".git/")

    for pattern in "${PROTECTED_PATTERNS[@]}"; do
      if [[ "$FILE_PATH" == *"$pattern"* ]]; then
        echo "Blocked: $FILE_PATH matches protected pattern '$pattern'" >&2
        exit 2
      fi
    done

    exit 0
    ```
  </Step>

  <Step title="스크립트를 실행 가능하게 만들기 (macOS/Linux)">
    Hook 스크립트는 Claude Code가 실행하려면 실행 가능해야 합니다:

    ```bash  theme={null}
    chmod +x .claude/hooks/protect-files.sh
    ```
  </Step>

  <Step title="hook 등록">
    모든 `Edit` 또는 `Write` 도구 호출 전에 스크립트를 실행하는 `PreToolUse` hook을 `.claude/settings.json`에 추가합니다:

    ```json  theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Edit|Write",
            "hooks": [
              {
                "type": "command",
                "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Step>
</Steps>

### 압축 후 컨텍스트 다시 주입

Claude의 컨텍스트 윈도우가 가득 차면 압축은 대화를 요약하여 공간을 확보합니다. 이는 중요한 세부 정보를 잃을 수 있습니다. `compact` matcher와 함께 `SessionStart` hook을 사용하여 모든 압축 후 중요한 컨텍스트를 다시 주입합니다.

명령이 stdout에 쓰는 모든 텍스트는 Claude의 컨텍스트에 추가됩니다. 이 예제는 Claude에게 프로젝트 규칙과 최근 작업을 상기시킵니다. 프로젝트 루트의 `.claude/settings.json`에 추가합니다:

```json  theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Reminder: use Bun, not npm. Run bun test before committing. Current sprint: auth refactor.'"
          }
        ]
      }
    ]
  }
}
```

`echo`를 `git log --oneline -5`와 같이 동적 출력을 생성하는 모든 명령으로 바꿀 수 있습니다. 모든 세션 시작 시 컨텍스트를 주입하려면 [CLAUDE.md](/ko/memory) 사용을 고려하세요. 환경 변수는 [`CLAUDE_ENV_FILE`](/ko/hooks#persist-environment-variables)을 참조하세요.

### 구성 변경 감사

세션 중에 설정 또는 skills 파일이 변경될 때를 추적합니다. `ConfigChange` 이벤트는 외부 프로세스 또는 편집기가 구성 파일을 수정할 때 발생하므로 규정 준수를 위해 변경 사항을 기록하거나 무단 수정을 차단할 수 있습니다.

이 예제는 각 변경을 감사 로그에 추가합니다. `~/.claude/settings.json`에 추가합니다:

```json  theme={null}
{
  "hooks": {
    "ConfigChange": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "jq -c '{timestamp: now | todate, source: .source, file: .file_path}' >> ~/claude-config-audit.log"
          }
        ]
      }
    ]
  }
}
```

Matcher는 구성 유형으로 필터링합니다: `user_settings`, `project_settings`, `local_settings`, `policy_settings` 또는 `skills`. 변경이 적용되지 않도록 차단하려면 종료 코드 2로 종료하거나 `{"decision": "block"}`을 반환합니다. 전체 입력 스키마는 [ConfigChange 참조](/ko/hooks#configchange)를 참조하세요.

### 특정 권한 프롬프트 자동 승인

항상 허용하는 도구 호출에 대한 승인 대화를 건너뜁니다. 이 예제는 `ExitPlanMode`를 자동 승인합니다. 이는 Claude가 계획 제시를 완료하고 진행을 요청할 때 호출하는 도구이므로 계획이 준비될 때마다 프롬프트가 표시되지 않습니다.

위의 종료 코드 예제와 달리 자동 승인을 위해서는 hook이 JSON 결정을 stdout에 작성해야 합니다. `PermissionRequest` hook은 Claude Code가 권한 대화를 표시하려고 할 때 발생하며 `"behavior": "allow"`를 반환하면 사용자 대신 답변합니다.

Matcher는 hook을 `ExitPlanMode`로만 범위를 지정하므로 다른 프롬프트는 영향을 받지 않습니다. `~/.claude/settings.json`에 추가합니다:

```json  theme={null}
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "ExitPlanMode",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\": {\"hookEventName\": \"PermissionRequest\", \"decision\": {\"behavior\": \"allow\"}}}'"
          }
        ]
      }
    ]
  }
}
```

Hook이 승인하면 Claude Code는 계획 모드를 종료하고 계획 모드에 들어가기 전에 활성화되었던 권한 모드를 복원합니다. 트랜스크립트는 대화가 나타났을 위치에 "Allowed by PermissionRequest hook"을 표시합니다. Hook 경로는 항상 현재 대화를 유지합니다: 대화가 할 수 있는 방식으로 컨텍스트를 지우고 새로운 구현 세션을 시작할 수 없습니다.

대신 특정 권한 모드를 설정하려면 hook의 출력에 `setMode` 항목이 있는 `updatedPermissions` 배열이 포함될 수 있습니다. `mode` 값은 `default`, `acceptEdits` 또는 `bypassPermissions`과 같은 모든 권한 모드이며 `destination: "session"`은 현재 세션에만 적용합니다.

세션을 `acceptEdits`로 전환하려면 hook이 이 JSON을 stdout에 작성합니다:

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedPermissions": [
        { "type": "setMode", "mode": "acceptEdits", "destination": "session" }
      ]
    }
  }
}
```

Matcher를 가능한 한 좁게 유지합니다. `.*`와 일치하거나 matcher를 비워두면 파일 쓰기 및 셸 명령을 포함한 모든 권한 프롬프트를 자동 승인합니다. 전체 결정 필드 집합은 [PermissionRequest 참조](/ko/hooks#permissionrequest-decision-control)를 참조하세요.

## Hooks 작동 방식

Hook 이벤트는 Claude Code의 라이프사이클의 특정 지점에서 발생합니다. 이벤트가 발생하면 일치하는 모든 hooks가 병렬로 실행되고 동일한 hook 명령은 자동으로 중복 제거됩니다. 아래 표는 각 이벤트와 발생 시기를 보여줍니다:

| Event                | When it fires                                                                                                                                  |
| :------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`       | When a session begins or resumes                                                                                                               |
| `UserPromptSubmit`   | When you submit a prompt, before Claude processes it                                                                                           |
| `PreToolUse`         | Before a tool call executes. Can block it                                                                                                      |
| `PermissionRequest`  | When a permission dialog appears                                                                                                               |
| `PostToolUse`        | After a tool call succeeds                                                                                                                     |
| `PostToolUseFailure` | After a tool call fails                                                                                                                        |
| `Notification`       | When Claude Code sends a notification                                                                                                          |
| `SubagentStart`      | When a subagent is spawned                                                                                                                     |
| `SubagentStop`       | When a subagent finishes                                                                                                                       |
| `Stop`               | When Claude finishes responding                                                                                                                |
| `StopFailure`        | When the turn ends due to an API error. Output and exit code are ignored                                                                       |
| `TeammateIdle`       | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                             |
| `TaskCompleted`      | When a task is being marked as completed                                                                                                       |
| `InstructionsLoaded` | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session |
| `ConfigChange`       | When a configuration file changes during a session                                                                                             |
| `WorktreeCreate`     | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                    |
| `WorktreeRemove`     | When a worktree is being removed, either at session exit or when a subagent finishes                                                           |
| `PreCompact`         | Before context compaction                                                                                                                      |
| `PostCompact`        | After context compaction completes                                                                                                             |
| `Elicitation`        | When an MCP server requests user input during a tool call                                                                                      |
| `ElicitationResult`  | After a user responds to an MCP elicitation, before the response is sent back to the server                                                    |
| `SessionEnd`         | When a session terminates                                                                                                                      |

각 hook에는 실행 방식을 결정하는 `type`이 있습니다. 대부분의 hooks는 `"type": "command"`를 사용하여 셸 명령을 실행합니다. 세 가지 다른 유형을 사용할 수 있습니다:

* `"type": "http"`: 이벤트 데이터를 URL에 POST합니다. [HTTP hooks](#http-hooks)를 참조하세요.
* `"type": "prompt"`: 단일 턴 LLM 평가. [프롬프트 기반 hooks](#prompt-based-hooks)를 참조하세요.
* `"type": "agent"`: 도구 액세스를 통한 다중 턴 검증. [에이전트 기반 hooks](#agent-based-hooks)를 참조하세요.

### 입력 읽기 및 출력 반환

Hooks는 stdin, stdout, stderr 및 종료 코드를 통해 Claude Code와 통신합니다. 이벤트가 발생하면 Claude Code는 이벤트별 데이터를 JSON으로 스크립트의 stdin에 전달합니다. 스크립트는 해당 데이터를 읽고 작업을 수행한 다음 종료 코드를 통해 Claude Code에 다음 작업을 알립니다.

#### Hook 입력

모든 이벤트에는 `session_id` 및 `cwd`와 같은 공통 필드가 포함되지만 각 이벤트 유형은 다른 데이터를 추가합니다. 예를 들어 Claude가 Bash 명령을 실행할 때 `PreToolUse` hook은 stdin에서 다음과 같은 것을 받습니다:

```json  theme={null}
{
  "session_id": "abc123",          // 이 세션의 고유 ID
  "cwd": "/Users/sarah/myproject", // 이벤트가 발생했을 때의 작업 디렉토리
  "hook_event_name": "PreToolUse", // 이 hook을 트리거한 이벤트
  "tool_name": "Bash",             // Claude가 사용하려는 도구
  "tool_input": {                  // Claude가 도구에 전달한 인수
    "command": "npm test"          // Bash의 경우 이것은 셸 명령입니다
  }
}
```

스크립트는 해당 JSON을 구문 분석하고 해당 필드에 대해 작동할 수 있습니다. `UserPromptSubmit` hooks는 `prompt` 텍스트를 대신 받고, `SessionStart` hooks는 `source` (startup, resume, clear, compact)를 받으며, 등등입니다. 공유 필드는 참조의 [공통 입력 필드](/ko/hooks#common-input-fields)를 참조하고 각 이벤트별 섹션에서 이벤트별 스키마를 참조하세요.

#### Hook 출력

스크립트는 stdout 또는 stderr에 쓰고 특정 코드로 종료하여 Claude Code에 다음 작업을 알립니다. 예를 들어 명령을 차단하려는 `PreToolUse` hook:

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q "drop table"; then
  echo "Blocked: dropping tables is not allowed" >&2  # stderr는 Claude의 피드백이 됩니다
  exit 2 # exit 2 = 작업 차단
fi

exit 0  # exit 0 = 진행 허용
```

종료 코드는 다음에 일어날 일을 결정합니다:

* **Exit 0**: 작업이 진행됩니다. `UserPromptSubmit` 및 `SessionStart` hooks의 경우 stdout에 쓰는 모든 것이 Claude의 컨텍스트에 추가됩니다.
* **Exit 2**: 작업이 차단됩니다. stderr에 이유를 쓰면 Claude가 피드백으로 받아 조정할 수 있습니다.
* **다른 종료 코드**: 작업이 진행됩니다. Stderr는 기록되지만 Claude에 표시되지 않습니다. `Ctrl+O`로 자세한 모드를 전환하여 트랜스크립트에서 이 메시지를 확인합니다.

#### 구조화된 JSON 출력

종료 코드는 두 가지 옵션을 제공합니다: 허용 또는 차단. 더 많은 제어를 위해 exit 0을 하고 stdout에 JSON 객체를 인쇄합니다.

<Note>
  Exit 2를 사용하여 stderr 메시지로 차단하거나 exit 0을 사용하여 구조화된 제어를 위해 JSON을 사용합니다. 혼합하지 마세요: Claude Code는 exit 2일 때 JSON을 무시합니다.
</Note>

예를 들어 `PreToolUse` hook은 도구 호출을 거부하고 이유를 알리거나 사용자 승인을 위해 에스컬레이션할 수 있습니다:

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Use rg instead of grep for better performance"
  }
}
```

Claude Code는 `permissionDecision`을 읽고 도구 호출을 취소한 다음 `permissionDecisionReason`을 Claude에게 피드백으로 전달합니다. 이 세 가지 옵션은 `PreToolUse`에만 해당합니다:

* `"allow"`: 권한 프롬프트를 표시하지 않고 진행
* `"deny"`: 도구 호출을 취소하고 이유를 Claude에 전송
* `"ask"`: 일반적으로 사용자에게 권한 프롬프트 표시

다른 이벤트는 다른 결정 패턴을 사용합니다. 예를 들어 `PostToolUse` 및 `Stop` hooks는 최상위 `decision: "block"` 필드를 사용하고 `PermissionRequest`는 `hookSpecificOutput.decision.behavior`를 사용합니다. 이벤트별 전체 분석은 참조의 [요약 표](/ko/hooks#decision-control)를 참조하세요.

`UserPromptSubmit` hooks의 경우 `additionalContext`를 대신 사용하여 Claude의 컨텍스트에 텍스트를 주입합니다. 프롬프트 기반 hooks (`type: "prompt"`)는 출력을 다르게 처리합니다: [프롬프트 기반 hooks](#prompt-based-hooks)를 참조하세요.

### Matchers로 hooks 필터링

Matcher가 없으면 hook은 이벤트의 모든 발생에서 발생합니다. Matchers를 사용하면 범위를 좁힐 수 있습니다. 예를 들어 모든 도구 호출 후가 아닌 파일 편집 후에만 포매터를 실행하려면 `PostToolUse` hook에 matcher를 추가합니다:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "prettier --write ..." }
        ]
      }
    ]
  }
}
```

`"Edit|Write"` matcher는 도구 이름과 일치하는 정규식 패턴입니다. Hook은 Claude가 `Edit` 또는 `Write` 도구를 사용할 때만 발생하고 `Bash`, `Read` 또는 다른 도구를 사용할 때는 발생하지 않습니다.

각 이벤트 유형은 특정 필드에서 일치합니다. Matchers는 정확한 문자열과 정규식 패턴을 지원합니다:

| 이벤트                                                                                             | Matcher가 필터링하는 것 | 예제 matcher 값                                                                       |
| :---------------------------------------------------------------------------------------------- | :--------------- | :--------------------------------------------------------------------------------- |
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`                          | 도구 이름            | `Bash`, `Edit\|Write`, `mcp__.*`                                                   |
| `SessionStart`                                                                                  | 세션이 시작된 방식       | `startup`, `resume`, `clear`, `compact`                                            |
| `SessionEnd`                                                                                    | 세션이 종료된 이유       | `clear`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`     |
| `Notification`                                                                                  | 알림 유형            | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`           |
| `SubagentStart`                                                                                 | 에이전트 유형          | `Bash`, `Explore`, `Plan` 또는 사용자 정의 에이전트 이름                                        |
| `PreCompact`                                                                                    | 압축을 트리거한 것       | `manual`, `auto`                                                                   |
| `SubagentStop`                                                                                  | 에이전트 유형          | `SubagentStart`와 동일한 값                                                             |
| `ConfigChange`                                                                                  | 구성 소스            | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |
| `UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` | matcher 지원 없음    | 모든 발생에서 항상 발생                                                                      |

다양한 이벤트 유형에서 matchers를 보여주는 몇 가지 추가 예제:

<Tabs>
  <Tab title="모든 Bash 명령 기록">
    `Bash` 도구 호출만 일치시키고 각 명령을 파일에 기록합니다. `PostToolUse` 이벤트는 명령이 완료된 후 발생하므로 `tool_input.command`는 실행된 내용을 포함합니다. Hook은 stdin에서 이벤트 데이터를 JSON으로 받고 `jq -r '.tool_input.command'`는 명령 문자열만 추출하며 `>>`는 로그 파일에 추가합니다:

    ```json  theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Bash",
            "hooks": [
              {
                "type": "command",
                "command": "jq -r '.tool_input.command' >> ~/.claude/command-log.txt"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="MCP 도구 일치">
    MCP 도구는 기본 제공 도구와 다른 명명 규칙을 사용합니다: `mcp__<server>__<tool>`. 여기서 `<server>`는 MCP 서버 이름이고 `<tool>`은 제공하는 도구입니다. 예를 들어 `mcp__github__search_repositories` 또는 `mcp__filesystem__read_file`. 정규식 matcher를 사용하여 특정 서버의 모든 도구를 대상으로 하거나 `mcp__.*__write.*`와 같은 패턴으로 서버 전체에서 일치합니다. 전체 예제 목록은 참조의 [MCP 도구 일치](/ko/hooks#match-mcp-tools)를 참조하세요.

    아래 명령은 hook의 JSON 입력에서 `jq`를 사용하여 도구 이름을 추출하고 자세한 모드 (`Ctrl+O`)에 표시되는 stderr에 씁니다:

    ```json  theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "mcp__github__.*",
            "hooks": [
              {
                "type": "command",
                "command": "echo \"GitHub tool called: $(jq -r '.tool_name')\" >&2"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="세션 종료 시 정리">
    `SessionEnd` 이벤트는 세션이 종료된 이유에 대한 matchers를 지원합니다. 이 hook은 일반 종료가 아닌 `/clear`를 실행할 때만 발생합니다:

    ```json  theme={null}
    {
      "hooks": {
        "SessionEnd": [
          {
            "matcher": "clear",
            "hooks": [
              {
                "type": "command",
                "command": "rm -f /tmp/claude-scratch-*.txt"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>
</Tabs>

전체 matcher 구문은 [Hooks 참조](/ko/hooks#configuration)를 참조하세요.

### Hook 위치 구성

Hook을 추가하는 위치는 범위를 결정합니다:

| 위치                                                         | 범위                         | 공유 가능           |
| :--------------------------------------------------------- | :------------------------- | :-------------- |
| `~/.claude/settings.json`                                  | 모든 프로젝트                    | 아니오, 컴퓨터에 로컬    |
| `.claude/settings.json`                                    | 단일 프로젝트                    | 예, 리포지토리에 커밋 가능 |
| `.claude/settings.local.json`                              | 단일 프로젝트                    | 아니오, gitignored |
| 관리형 정책 설정                                                  | 조직 전체                      | 예, 관리자 제어       |
| [Plugin](/ko/plugins) `hooks/hooks.json`                   | 플러그인이 활성화되었을 때             | 예, 플러그인과 함께 번들됨 |
| [Skill](/ko/skills) 또는 [agent](/ko/sub-agents) frontmatter | Skill 또는 에이전트가 활성화되어 있는 동안 | 예, 컴포넌트 파일에 정의됨 |

Claude Code에서 [`/hooks`](/ko/hooks#the-hooks-menu)를 실행하여 이벤트별로 그룹화된 모든 구성된 hooks를 찾아봅니다. 모든 hooks를 한 번에 비활성화하려면 설정 파일에서 `"disableAllHooks": true`를 설정합니다.

Claude Code가 실행 중인 동안 설정 파일을 직접 편집하면 파일 감시자가 일반적으로 hook 변경을 자동으로 선택합니다.

## 프롬프트 기반 hooks

결정론적 규칙이 아닌 판단이 필요한 결정의 경우 `type: "prompt"` hooks를 사용합니다. 셸 명령을 실행하는 대신 Claude Code는 프롬프트와 hook의 입력 데이터를 Claude 모델 (기본적으로 Haiku)에 전송하여 결정을 내립니다. 더 많은 기능이 필요한 경우 `model` 필드로 다른 모델을 지정할 수 있습니다.

모델의 유일한 작업은 yes/no 결정을 JSON으로 반환하는 것입니다:

* `"ok": true`: 작업이 진행됩니다
* `"ok": false`: 작업이 차단됩니다. 모델의 `"reason"`은 Claude가 조정할 수 있도록 피드백으로 전달됩니다.

이 예제는 `Stop` hook을 사용하여 모든 요청된 작업이 완료되었는지 모델에 묻습니다. 모델이 `"ok": false`를 반환하면 Claude는 계속 작업하고 `reason`을 다음 지침으로 사용합니다:

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if all tasks are complete. If not, respond with {\"ok\": false, \"reason\": \"what remains to be done\"}."
          }
        ]
      }
    ]
  }
}
```

전체 구성 옵션은 참조의 [프롬프트 기반 hooks](/ko/hooks#prompt-based-hooks)를 참조하세요.

## 에이전트 기반 hooks

검증에 파일 검사 또는 명령 실행이 필요한 경우 `type: "agent"` hooks를 사용합니다. 단일 LLM 호출을 수행하는 프롬프트 hooks와 달리 에이전트 hooks는 파일을 읽고 코드를 검색하며 결정을 반환하기 전에 다른 도구를 사용할 수 있는 subagent를 생성합니다.

에이전트 hooks는 프롬프트 hooks와 동일한 `"ok"` / `"reason"` 응답 형식을 사용하지만 기본 타임아웃이 60초이고 최대 50개의 도구 사용 턴입니다.

이 예제는 Claude가 중지되기 전에 테스트가 통과하는지 확인합니다:

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

Hook 입력 데이터만으로 결정을 내릴 수 있을 때 프롬프트 hooks를 사용합니다. 코드베이스의 실제 상태에 대해 무언가를 확인해야 할 때 에이전트 hooks를 사용합니다.

전체 구성 옵션은 참조의 [에이전트 기반 hooks](/ko/hooks#agent-based-hooks)를 참조하세요.

## HTTP hooks

`type: "http"` hooks를 사용하여 셸 명령을 실행하는 대신 이벤트 데이터를 HTTP 엔드포인트에 POST합니다. 엔드포인트는 명령 hook이 stdin에서 받을 것과 동일한 JSON을 받고 동일한 JSON 형식을 사용하여 HTTP 응답 본문을 통해 결과를 반환합니다.

HTTP hooks는 웹 서버, 클라우드 함수 또는 외부 서비스가 hook 로직을 처리하기를 원할 때 유용합니다: 예를 들어 팀 전체에서 도구 사용 이벤트를 기록하는 공유 감사 서비스입니다.

이 예제는 모든 도구 사용을 로컬 로깅 서비스에 게시합니다:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/tool-use",
            "headers": {
              "Authorization": "Bearer $MY_TOKEN"
            },
            "allowedEnvVars": ["MY_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

엔드포인트는 명령 hooks와 동일한 [출력 형식](/ko/hooks#json-output)을 사용하여 JSON 응답 본문을 반환해야 합니다. 도구 호출을 차단하려면 적절한 `hookSpecificOutput` 필드와 함께 2xx 응답을 반환합니다. HTTP 상태 코드만으로는 작업을 차단할 수 없습니다.

헤더 값은 `$VAR_NAME` 또는 `${VAR_NAME}` 구문을 사용한 환경 변수 보간을 지원합니다. `allowedEnvVars` 배열에 나열된 변수만 해결됩니다. 다른 모든 `$VAR` 참조는 비어 있습니다.

전체 구성 옵션 및 응답 처리는 참조의 [HTTP hooks](/ko/hooks#http-hook-fields)를 참조하세요.

## 제한 사항 및 문제 해결

### 제한 사항

* 명령 hooks는 stdout, stderr 및 종료 코드를 통해서만 통신합니다. 직접 명령이나 도구 호출을 트리거할 수 없습니다. HTTP hooks는 응답 본문을 통해 통신합니다.
* Hook 타임아웃은 기본적으로 10분이며 `timeout` 필드 (초 단위)로 hook당 구성 가능합니다.
* `PostToolUse` hooks는 도구가 이미 실행되었으므로 작업을 취소할 수 없습니다.
* `PermissionRequest` hooks는 [비대화형 모드](/ko/headless) (`-p`)에서 발생하지 않습니다. 자동화된 권한 결정을 위해 `PreToolUse` hooks를 사용합니다.
* `Stop` hooks는 작업 완료 시에만이 아니라 Claude가 응답을 완료할 때마다 발생합니다. 사용자 중단 시에는 발생하지 않습니다.

### Hook이 발생하지 않음

Hook이 구성되었지만 실행되지 않습니다.

* `/hooks`를 실행하고 hook이 올바른 이벤트 아래에 나타나는지 확인합니다
* Matcher 패턴이 도구 이름과 정확히 일치하는지 확인합니다 (matchers는 대소문자 구분)
* 올바른 이벤트 유형을 트리거하는지 확인합니다 (예: `PreToolUse`는 도구 실행 전에 발생하고 `PostToolUse`는 후에 발생)
* 비대화형 모드 (`-p`)에서 `PermissionRequest` hooks를 사용하는 경우 대신 `PreToolUse`로 전환합니다

### 출력에 Hook 오류

트랜스크립트에 "PreToolUse hook error: ..." 같은 메시지가 표시됩니다.

* 스크립트가 예기치 않게 0이 아닌 코드로 종료되었습니다. 샘플 JSON을 파이프하여 수동으로 테스트합니다:
  ```bash  theme={null}
  echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./my-hook.sh
  echo $?  # 종료 코드 확인
  ```
* "command not found"가 표시되면 절대 경로를 사용하거나 `$CLAUDE_PROJECT_DIR`을 사용하여 스크립트를 참조합니다
* "jq: command not found"가 표시되면 `jq`를 설치하거나 JSON 구문 분석을 위해 Python/Node.js를 사용합니다
* 스크립트가 실행되지 않으면 실행 가능하게 만듭니다: `chmod +x ./my-hook.sh`

### `/hooks`에 구성된 hooks가 없음

설정 파일을 편집했지만 hooks가 메뉴에 나타나지 않습니다.

* 파일 편집은 일반적으로 자동으로 선택됩니다. 몇 초 후에 나타나지 않으면 파일 감시자가 변경을 놓쳤을 수 있습니다: 세션을 다시 시작하여 강제로 다시 로드합니다.
* JSON이 유효한지 확인합니다 (후행 쉼표 및 주석은 허용되지 않음)
* 설정 파일이 올바른 위치에 있는지 확인합니다: 프로젝트 hooks의 경우 `.claude/settings.json`, 전역 hooks의 경우 `~/.claude/settings.json`

### Stop hook이 무한 실행됨

Claude가 무한 루프에서 계속 작업하는 대신 중지합니다.

Stop hook 스크립트는 이미 트리거되었는지 확인해야 합니다. JSON 입력에서 `stop_hook_active` 필드를 구문 분석하고 `true`인 경우 조기에 종료합니다:

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0  # Claude가 중지되도록 허용
fi
# ... hook 로직의 나머지
```

### JSON 검증 실패

Hook 스크립트가 유효한 JSON을 출력하더라도 Claude Code에 JSON 구문 분석 오류가 표시됩니다.

Claude Code가 hook을 실행할 때 프로필 (`~/.zshrc` 또는 `~/.bashrc`)을 소싱하는 셸을 생성합니다. 프로필에 무조건적인 `echo` 문이 포함되어 있으면 해당 출력이 hook의 JSON에 앞에 붙습니다:

```text  theme={null}
Shell ready on arm64
{"decision": "block", "reason": "Not allowed"}
```

Claude Code는 이를 JSON으로 구문 분석하려고 하고 실패합니다. 이를 수정하려면 셸 프로필의 echo 문을 래핑하여 대화형 셸에서만 실행되도록 합니다:

```bash  theme={null}
# ~/.zshrc 또는 ~/.bashrc에서
if [[ $- == *i* ]]; then
  echo "Shell ready"
fi
```

`$-` 변수는 셸 플래그를 포함하고 `i`는 대화형을 의미합니다. Hooks는 비대화형 셸에서 실행되므로 echo는 건너뜁니다.

### 디버그 기법

`Ctrl+O`로 자세한 모드를 전환하여 트랜스크립트에서 hook 출력을 보거나 `claude --debug`를 실행하여 일치한 hooks 및 종료 코드를 포함한 전체 실행 세부 정보를 확인합니다.

## 자세히 알아보기

* [Hooks 참조](/ko/hooks): 전체 이벤트 스키마, JSON 출력 형식, 비동기 hooks 및 MCP 도구 hooks
* [보안 고려 사항](/ko/hooks#security-considerations): 공유 또는 프로덕션 환경에서 hooks를 배포하기 전에 검토합니다
* [Bash 명령 검증기 예제](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py): 완전한 참조 구현
