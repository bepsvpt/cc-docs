> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# CLI 참조

> Claude Code 명령줄 인터페이스의 완전한 참조로, 명령어와 플래그를 포함합니다.

## CLI 명령어

이러한 명령어를 사용하여 세션을 시작하고, 콘텐츠를 파이프하고, 대화를 재개하고, 업데이트를 관리할 수 있습니다:

| 명령어                             | 설명                                                                                                                                                         | 예시                                                 |
| :------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------- |
| `claude`                        | 대화형 세션 시작                                                                                                                                                  | `claude`                                           |
| `claude "query"`                | 초기 프롬프트로 대화형 세션 시작                                                                                                                                         | `claude "explain this project"`                    |
| `claude -p "query"`             | SDK를 통해 쿼리하고 종료                                                                                                                                            | `claude -p "explain this function"`                |
| `cat file \| claude -p "query"` | 파이프된 콘텐츠 처리                                                                                                                                                | `cat logs.txt \| claude -p "explain"`              |
| `claude -c`                     | 현재 디렉토리에서 가장 최근 대화 계속                                                                                                                                      | `claude -c`                                        |
| `claude -c -p "query"`          | SDK를 통해 계속                                                                                                                                                 | `claude -c -p "Check for type errors"`             |
| `claude -r "<session>" "query"` | ID 또는 이름으로 세션 재개                                                                                                                                           | `claude -r "auth-refactor" "Finish this PR"`       |
| `claude update`                 | 최신 버전으로 업데이트                                                                                                                                               | `claude update`                                    |
| `claude auth login`             | Anthropic 계정에 로그인합니다. `--email`을 사용하여 이메일 주소를 미리 입력하고 `--sso`를 사용하여 SSO 인증을 강제할 수 있습니다                                                                     | `claude auth login --email user@example.com --sso` |
| `claude auth logout`            | Anthropic 계정에서 로그아웃합니다                                                                                                                                     | `claude auth logout`                               |
| `claude auth status`            | 인증 상태를 JSON으로 표시합니다. 사람이 읽을 수 있는 출력을 위해 `--text`를 사용합니다. 로그인되어 있으면 코드 0으로, 로그인되어 있지 않으면 1로 종료됩니다                                                           | `claude auth status`                               |
| `claude agents`                 | 모든 구성된 [subagents](/ko/sub-agents)를 소스별로 그룹화하여 나열합니다                                                                                                       | `claude agents`                                    |
| `claude mcp`                    | Model Context Protocol (MCP) 서버 구성                                                                                                                         | [Claude Code MCP 문서](/ko/mcp)를 참조하세요.              |
| `claude remote-control`         | 로컬에서 실행하는 동안 Claude.ai 또는 Claude 앱에서 Claude Code를 제어하기 위한 [Remote Control 세션](/ko/remote-control)을 시작합니다. 플래그는 [Remote Control](/ko/remote-control)을 참조하세요 | `claude remote-control`                            |

## CLI 플래그

이러한 명령줄 플래그를 사용하여 Claude Code의 동작을 사용자 정의합니다:

| 플래그                                    | 설명                                                                                                                                                                   | 예시                                                                                                 |
| :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| `--add-dir`                            | Claude가 액세스할 추가 작업 디렉토리 추가(각 경로가 디렉토리로 존재하는지 검증)                                                                                                                     | `claude --add-dir ../apps ../lib`                                                                  |
| `--agent`                              | 현재 세션에 대한 에이전트 지정(`agent` 설정 재정의)                                                                                                                                    | `claude --agent my-custom-agent`                                                                   |
| `--agents`                             | JSON을 통해 사용자 정의 [subagents](/ko/sub-agents)를 동적으로 정의(형식은 아래 참조)                                                                                                      | `claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'` |
| `--allow-dangerously-skip-permissions` | 권한 우회를 옵션으로 활성화하되 즉시 활성화하지 않습니다. `--permission-mode`와 함께 구성 가능(주의하여 사용)                                                                                              | `claude --permission-mode plan --allow-dangerously-skip-permissions`                               |
| `--allowedTools`                       | 권한 프롬프트 없이 실행되는 도구입니다. 패턴 매칭을 위해 [권한 규칙 구문](/ko/settings#permission-rule-syntax)을 참조하세요. 사용 가능한 도구를 제한하려면 `--tools`를 대신 사용하세요                                        | `"Bash(git log *)" "Bash(git diff *)" "Read"`                                                      |
| `--append-system-prompt`               | 기본 시스템 프롬프트의 끝에 사용자 정의 텍스트 추가                                                                                                                                        | `claude --append-system-prompt "Always use TypeScript"`                                            |
| `--append-system-prompt-file`          | 파일에서 추가 시스템 프롬프트 텍스트를 로드하고 기본 프롬프트에 추가                                                                                                                               | `claude --append-system-prompt-file ./extra-rules.txt`                                             |
| `--betas`                              | API 요청에 포함할 베타 헤더(API 키 사용자만 해당)                                                                                                                                     | `claude --betas interleaved-thinking`                                                              |
| `--chrome`                             | 웹 자동화 및 테스트를 위한 [Chrome 브라우저 통합](/ko/chrome) 활성화                                                                                                                     | `claude --chrome`                                                                                  |
| `--continue`, `-c`                     | 현재 디렉토리에서 가장 최근 대화 로드                                                                                                                                                | `claude --continue`                                                                                |
| `--dangerously-skip-permissions`       | 모든 권한 프롬프트 건너뛰기(주의하여 사용)                                                                                                                                             | `claude --dangerously-skip-permissions`                                                            |
| `--debug`                              | 선택적 카테고리 필터링을 사용하여 디버그 모드 활성화(예: `"api,hooks"` 또는 `"!statsig,!file"`)                                                                                                | `claude --debug "api,mcp"`                                                                         |
| `--disable-slash-commands`             | 이 세션에 대한 모든 skills 및 명령어 비활성화                                                                                                                                        | `claude --disable-slash-commands`                                                                  |
| `--disallowedTools`                    | 모델의 컨텍스트에서 제거되고 사용할 수 없는 도구                                                                                                                                          | `"Bash(git log *)" "Bash(git diff *)" "Edit"`                                                      |
| `--fallback-model`                     | 기본 모델이 과부하일 때 지정된 모델로 자동 폴백 활성화(인쇄 모드만 해당)                                                                                                                           | `claude -p --fallback-model sonnet "query"`                                                        |
| `--fork-session`                       | 재개할 때 원본을 재사용하는 대신 새 세션 ID 생성(`--resume` 또는 `--continue`와 함께 사용)                                                                                                     | `claude --resume abc123 --fork-session`                                                            |
| `--from-pr`                            | 특정 GitHub PR에 연결된 세션 재개. PR 번호 또는 URL을 허용합니다. `gh pr create`를 통해 생성된 세션은 자동으로 연결됩니다                                                                                  | `claude --from-pr 123`                                                                             |
| `--ide`                                | 정확히 하나의 유효한 IDE를 사용할 수 있는 경우 시작 시 IDE에 자동으로 연결                                                                                                                       | `claude --ide`                                                                                     |
| `--init`                               | 초기화 hooks를 실행하고 대화형 모드 시작                                                                                                                                            | `claude --init`                                                                                    |
| `--init-only`                          | 초기화 hooks를 실행하고 종료(대화형 세션 없음)                                                                                                                                        | `claude --init-only`                                                                               |
| `--include-partial-messages`           | 부분 스트리밍 이벤트를 출력에 포함(`--print`와 `--output-format=stream-json` 필요)                                                                                                     | `claude -p --output-format stream-json --include-partial-messages "query"`                         |
| `--input-format`                       | 인쇄 모드의 입력 형식 지정(옵션: `text`, `stream-json`)                                                                                                                           | `claude -p --output-format json --input-format stream-json`                                        |
| `--json-schema`                        | 에이전트가 워크플로우를 완료한 후 JSON Schema와 일치하는 검증된 JSON 출력 가져오기(인쇄 모드만 해당, [구조화된 출력](https://platform.claude.com/docs/en/agent-sdk/structured-outputs) 참조)                     | `claude -p --json-schema '{"type":"object","properties":{...}}' "query"`                           |
| `--maintenance`                        | 유지 관리 hooks를 실행하고 종료                                                                                                                                                 | `claude --maintenance`                                                                             |
| `--max-budget-usd`                     | 중지하기 전에 API 호출에 소비할 최대 달러 금액(인쇄 모드만 해당)                                                                                                                              | `claude -p --max-budget-usd 5.00 "query"`                                                          |
| `--max-turns`                          | 에이전트 턴의 수 제한(인쇄 모드만 해당). 제한에 도달하면 오류로 종료됩니다. 기본적으로 제한 없음                                                                                                             | `claude -p --max-turns 3 "query"`                                                                  |
| `--mcp-config`                         | JSON 파일 또는 문자열에서 MCP 서버 로드(공백으로 구분)                                                                                                                                  | `claude --mcp-config ./mcp.json`                                                                   |
| `--model`                              | 최신 모델의 별칭(`sonnet` 또는 `opus`) 또는 모델의 전체 이름으로 현재 세션의 모델 설정                                                                                                            | `claude --model claude-sonnet-4-6`                                                                 |
| `--no-chrome`                          | 이 세션에 대한 [Chrome 브라우저 통합](/ko/chrome) 비활성화                                                                                                                           | `claude --no-chrome`                                                                               |
| `--no-session-persistence`             | 세션 지속성 비활성화하여 세션이 디스크에 저장되지 않고 재개할 수 없음(인쇄 모드만 해당)                                                                                                                   | `claude -p --no-session-persistence "query"`                                                       |
| `--output-format`                      | 인쇄 모드의 출력 형식 지정(옵션: `text`, `json`, `stream-json`)                                                                                                                   | `claude -p "query" --output-format json`                                                           |
| `--permission-mode`                    | 지정된 [권한 모드](/ko/permissions#permission-modes)에서 시작                                                                                                                   | `claude --permission-mode plan`                                                                    |
| `--permission-prompt-tool`             | 비대화형 모드에서 권한 프롬프트를 처리할 MCP 도구 지정                                                                                                                                     | `claude -p --permission-prompt-tool mcp_auth_tool "query"`                                         |
| `--plugin-dir`                         | 이 세션에만 플러그인 디렉토리에서 플러그인 로드(반복 가능)                                                                                                                                    | `claude --plugin-dir ./my-plugins`                                                                 |
| `--print`, `-p`                        | 대화형 모드 없이 응답 인쇄([Agent SDK 문서](https://platform.claude.com/docs/en/agent-sdk/overview)에서 프로그래밍 방식 사용 세부 정보 참조)                                                       | `claude -p "query"`                                                                                |
| `--remote`                             | 제공된 작업 설명으로 claude.ai에서 새 [웹 세션](/ko/claude-code-on-the-web) 생성                                                                                                      | `claude --remote "Fix the login bug"`                                                              |
| `--resume`, `-r`                       | ID 또는 이름으로 특정 세션 재개하거나 세션을 선택할 대화형 선택기 표시                                                                                                                            | `claude --resume auth-refactor`                                                                    |
| `--session-id`                         | 대화에 특정 세션 ID 사용(유효한 UUID여야 함)                                                                                                                                        | `claude --session-id "550e8400-e29b-41d4-a716-446655440000"`                                       |
| `--setting-sources`                    | 로드할 설정 소스의 쉼표로 구분된 목록(`user`, `project`, `local`)                                                                                                                    | `claude --setting-sources user,project`                                                            |
| `--settings`                           | 추가 설정을 로드할 설정 JSON 파일 또는 JSON 문자열의 경로                                                                                                                                | `claude --settings ./settings.json`                                                                |
| `--strict-mcp-config`                  | `--mcp-config`의 MCP 서버만 사용하고 다른 모든 MCP 구성 무시                                                                                                                         | `claude --strict-mcp-config --mcp-config ./mcp.json`                                               |
| `--system-prompt`                      | 전체 시스템 프롬프트를 사용자 정의 텍스트로 바꾸기                                                                                                                                         | `claude --system-prompt "You are a Python expert"`                                                 |
| `--system-prompt-file`                 | 파일에서 시스템 프롬프트를 로드하여 기본 프롬프트 바꾸기                                                                                                                                      | `claude --system-prompt-file ./custom-prompt.txt`                                                  |
| `--teleport`                           | 로컬 터미널에서 [웹 세션](/ko/claude-code-on-the-web) 재개                                                                                                                       | `claude --teleport`                                                                                |
| `--teammate-mode`                      | [에이전트 팀](/ko/agent-teams) 팀원 표시 방식 설정: `auto`(기본값), `in-process`, 또는 `tmux`. [에이전트 팀 설정](/ko/agent-teams#set-up-agent-teams) 참조                                      | `claude --teammate-mode in-process`                                                                |
| `--tools`                              | Claude가 사용할 수 있는 기본 제공 도구 제한. `""`를 사용하여 모두 비활성화, `"default"`를 사용하여 모두 활성화, 또는 `"Bash,Edit,Read"`와 같은 도구 이름 사용                                                       | `claude --tools "Bash,Edit,Read"`                                                                  |
| `--verbose`                            | 자세한 로깅 활성화, 전체 턴별 출력 표시                                                                                                                                              | `claude --verbose`                                                                                 |
| `--version`, `-v`                      | 버전 번호 출력                                                                                                                                                             | `claude -v`                                                                                        |
| `--worktree`, `-w`                     | `<repo>/.claude/worktrees/<name>`에서 격리된 [git worktree](/ko/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees)에서 Claude 시작. 이름이 지정되지 않으면 자동으로 생성됨 | `claude -w feature-auth`                                                                           |

<Tip>
  `--output-format json` 플래그는 스크립팅 및 자동화에 특히 유용하며,
  Claude의 응답을 프로그래밍 방식으로 구문 분석할 수 있습니다.
</Tip>

### Agents 플래그 형식

`--agents` 플래그는 하나 이상의 사용자 정의 subagents를 정의하는 JSON 객체를 허용합니다. 각 subagent는 고유한 이름(키로 사용)과 다음 필드를 포함하는 정의 객체가 필요합니다:

| 필드                | 필수  | 설명                                                                                                                                                                  |
| :---------------- | :-- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `description`     | 예   | subagent를 호출해야 할 때를 설명하는 자연어 설명                                                                                                                                     |
| `prompt`          | 예   | subagent의 동작을 안내하는 시스템 프롬프트                                                                                                                                         |
| `tools`           | 아니오 | subagent가 사용할 수 있는 특정 도구의 배열(예: `["Read", "Edit", "Bash"]`). 생략하면 모든 도구를 상속합니다. [`Agent(agent_type)`](/ko/sub-agents#restrict-which-subagents-can-be-spawned) 구문 지원 |
| `disallowedTools` | 아니오 | 이 subagent에 대해 명시적으로 거부할 도구 이름의 배열                                                                                                                                  |
| `model`           | 아니오 | 사용할 모델 별칭: `sonnet`, `opus`, `haiku`, 또는 `inherit`. 생략하면 `inherit`로 기본 설정됨                                                                                          |
| `skills`          | 아니오 | subagent의 컨텍스트에 미리 로드할 [skill](/ko/skills) 이름의 배열                                                                                                                   |
| `mcpServers`      | 아니오 | 이 subagent에 대한 [MCP servers](/ko/mcp)의 배열. 각 항목은 서버 이름 문자열 또는 `{name: config}` 객체                                                                                   |
| `maxTurns`        | 아니오 | subagent가 중지되기 전의 최대 에이전트 턴 수                                                                                                                                       |

예시:

```bash  theme={null}
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

subagents 생성 및 사용에 대한 자세한 내용은 [subagents 문서](/ko/sub-agents)를 참조하세요.

### 시스템 프롬프트 플래그

Claude Code는 시스템 프롬프트를 사용자 정의하기 위한 4가지 플래그를 제공합니다. 4가지 모두 대화형 및 비대화형 모드에서 작동합니다.

| 플래그                           | 동작                        | 사용 사례                             |
| :---------------------------- | :------------------------ | :-------------------------------- |
| `--system-prompt`             | **전체** 기본 프롬프트 **바꾸기**    | Claude의 동작 및 지침에 대한 완전한 제어        |
| `--system-prompt-file`        | **파일 내용으로** **바꾸기**       | 재현성 및 버전 제어를 위해 파일에서 프롬프트 로드      |
| `--append-system-prompt`      | **기본 프롬프트에** **추가**       | 기본 Claude Code 동작을 유지하면서 특정 지침 추가 |
| `--append-system-prompt-file` | **기본 프롬프트에 파일 내용** **추가** | 기본값을 유지하면서 파일에서 추가 지침 로드          |

**각각을 사용할 때:**

* **`--system-prompt`**: Claude의 시스템 프롬프트를 완전히 제어해야 할 때 사용합니다. 이는 모든 기본 Claude Code 지침을 제거하여 백지 상태를 제공합니다.
  ```bash  theme={null}
  claude --system-prompt "You are a Python expert who only writes type-annotated code"
  ```

* **`--system-prompt-file`**: 파일에서 사용자 정의 프롬프트를 로드하려고 할 때 사용합니다. 팀 일관성 또는 버전 제어 프롬프트 템플릿에 유용합니다.
  ```bash  theme={null}
  claude --system-prompt-file ./prompts/code-review.txt
  ```

* **`--append-system-prompt`**: Claude Code의 기본 기능을 유지하면서 특정 지침을 추가하려고 할 때 사용합니다. 대부분의 사용 사례에서 가장 안전한 옵션입니다.
  ```bash  theme={null}
  claude --append-system-prompt "Always use TypeScript and include JSDoc comments"
  ```

* **`--append-system-prompt-file`**: Claude Code의 기본값을 유지하면서 파일에서 지침을 추가하려고 할 때 사용합니다. 버전 제어 추가에 유용합니다.
  ```bash  theme={null}
  claude --append-system-prompt-file ./prompts/style-rules.txt
  ```

`--system-prompt`와 `--system-prompt-file`은 상호 배타적입니다. 추가 플래그는 바꾸기 플래그 중 하나와 함께 사용할 수 있습니다.

대부분의 사용 사례에서 `--append-system-prompt` 또는 `--append-system-prompt-file`을 권장합니다. 이들은 Claude Code의 기본 제공 기능을 유지하면서 사용자 정의 요구 사항을 추가합니다. 시스템 프롬프트를 완전히 제어해야 할 때만 `--system-prompt` 또는 `--system-prompt-file`을 사용하세요.

## 참고 항목

* [Chrome 확장 프로그램](/ko/chrome) - 브라우저 자동화 및 웹 테스트
* [대화형 모드](/ko/interactive-mode) - 단축키, 입력 모드 및 대화형 기능
* [빠른 시작 가이드](/ko/quickstart) - Claude Code 시작하기
* [일반적인 워크플로우](/ko/common-workflows) - 고급 워크플로우 및 패턴
* [설정](/ko/settings) - 구성 옵션
* [Agent SDK 문서](https://platform.claude.com/docs/en/agent-sdk/overview) - 프로그래밍 방식 사용 및 통합
