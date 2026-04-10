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

# 플러그인 참조

> Claude Code 플러그인 시스템의 완전한 기술 참조, 스키마, CLI 명령어 및 컴포넌트 사양 포함.

<Tip>
  플러그인을 설치하려고 하시나요? [플러그인 발견 및 설치](/ko/discover-plugins)를 참조하세요. 플러그인 생성에 대해서는 [플러그인](/ko/plugins)을 참조하세요. 플러그인 배포에 대해서는 [플러그인 마켓플레이스](/ko/plugin-marketplaces)를 참조하세요.
</Tip>

이 참조는 Claude Code 플러그인 시스템의 완전한 기술 사양을 제공하며, 컴포넌트 스키마, CLI 명령어 및 개발 도구를 포함합니다.

**플러그인**은 Claude Code를 사용자 정의 기능으로 확장하는 자체 포함된 컴포넌트 디렉토리입니다. 플러그인 컴포넌트에는 skills, agents, hooks, MCP servers 및 LSP servers가 포함됩니다.

## 플러그인 컴포넌트 참조

### Skills

플러그인은 Claude Code에 skills를 추가하여 사용자나 Claude가 호출할 수 있는 `/name` 바로가기를 생성합니다.

**위치**: 플러그인 루트의 `skills/` 또는 `commands/` 디렉토리

**파일 형식**: Skills는 `SKILL.md`가 있는 디렉토리이고, commands는 간단한 마크다운 파일입니다.

**Skill 구조**:

```text  theme={null}
skills/
├── pdf-processor/
│   ├── SKILL.md
│   ├── reference.md (선택사항)
│   └── scripts/ (선택사항)
└── code-reviewer/
    └── SKILL.md
```

**통합 동작**:

* Skills와 commands는 플러그인이 설치될 때 자동으로 발견됩니다.
* Claude는 작업 컨텍스트에 따라 자동으로 이들을 호출할 수 있습니다.
* Skills는 SKILL.md와 함께 지원 파일을 포함할 수 있습니다.

완전한 세부 정보는 [Skills](/ko/skills)를 참조하세요.

### Agents

플러그인은 Claude가 적절할 때 자동으로 호출할 수 있는 특정 작업을 위한 특화된 subagents를 제공할 수 있습니다.

**위치**: 플러그인 루트의 `agents/` 디렉토리

**파일 형식**: 에이전트 기능을 설명하는 마크다운 파일

**Agent 구조**:

```markdown  theme={null}
---
name: agent-name
description: 이 에이전트가 전문으로 하는 분야와 Claude가 이를 호출해야 할 때
model: sonnet
effort: medium
maxTurns: 20
disallowedTools: Write, Edit
---

에이전트의 역할, 전문성 및 동작을 설명하는 상세한 시스템 프롬프트입니다.
```

플러그인 agents는 `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background` 및 `isolation` frontmatter 필드를 지원합니다. 유일한 유효한 `isolation` 값은 `"worktree"`입니다. 보안상의 이유로 `hooks`, `mcpServers` 및 `permissionMode`는 플러그인 제공 agents에서 지원되지 않습니다.

**통합 지점**:

* Agents는 `/agents` 인터페이스에 나타납니다.
* Claude는 작업 컨텍스트에 따라 agents를 자동으로 호출할 수 있습니다.
* Agents는 사용자가 수동으로 호출할 수 있습니다.
* 플러그인 agents는 기본 제공 Claude agents와 함께 작동합니다.

완전한 세부 정보는 [Subagents](/ko/sub-agents)를 참조하세요.

### Hooks

플러그인은 Claude Code 이벤트에 자동으로 응답하는 이벤트 핸들러를 제공할 수 있습니다.

**위치**: 플러그인 루트의 `hooks/hooks.json` 또는 plugin.json에 인라인

**형식**: 이벤트 매처 및 작업이 있는 JSON 구성

**Hook 구성**:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

플러그인 hooks는 [사용자 정의 hooks](/ko/hooks)와 동일한 라이프사이클 이벤트에 응답합니다:

| Event                | When it fires                                                                                                                                          |
| :------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`       | When a session begins or resumes                                                                                                                       |
| `UserPromptSubmit`   | When you submit a prompt, before Claude processes it                                                                                                   |
| `PreToolUse`         | Before a tool call executes. Can block it                                                                                                              |
| `PermissionRequest`  | When a permission dialog appears                                                                                                                       |
| `PermissionDenied`   | When a tool call is denied by the auto mode classifier. Return `{retry: true}` to tell the model it may retry the denied tool call                     |
| `PostToolUse`        | After a tool call succeeds                                                                                                                             |
| `PostToolUseFailure` | After a tool call fails                                                                                                                                |
| `Notification`       | When Claude Code sends a notification                                                                                                                  |
| `SubagentStart`      | When a subagent is spawned                                                                                                                             |
| `SubagentStop`       | When a subagent finishes                                                                                                                               |
| `TaskCreated`        | When a task is being created via `TaskCreate`                                                                                                          |
| `TaskCompleted`      | When a task is being marked as completed                                                                                                               |
| `Stop`               | When Claude finishes responding                                                                                                                        |
| `StopFailure`        | When the turn ends due to an API error. Output and exit code are ignored                                                                               |
| `TeammateIdle`       | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                                     |
| `InstructionsLoaded` | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session         |
| `ConfigChange`       | When a configuration file changes during a session                                                                                                     |
| `CwdChanged`         | When the working directory changes, for example when Claude executes a `cd` command. Useful for reactive environment management with tools like direnv |
| `FileChanged`        | When a watched file changes on disk. The `matcher` field specifies which filenames to watch                                                            |
| `WorktreeCreate`     | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                            |
| `WorktreeRemove`     | When a worktree is being removed, either at session exit or when a subagent finishes                                                                   |
| `PreCompact`         | Before context compaction                                                                                                                              |
| `PostCompact`        | After context compaction completes                                                                                                                     |
| `Elicitation`        | When an MCP server requests user input during a tool call                                                                                              |
| `ElicitationResult`  | After a user responds to an MCP elicitation, before the response is sent back to the server                                                            |
| `SessionEnd`         | When a session terminates                                                                                                                              |

**Hook 유형**:

* `command`: 셸 명령어 또는 스크립트 실행
* `http`: 이벤트 JSON을 URL로 POST 요청으로 전송
* `prompt`: LLM으로 프롬프트 평가 (컨텍스트에 대해 `$ARGUMENTS` 플레이스홀더 사용)
* `agent`: 복잡한 검증 작업을 위해 도구가 있는 에이전트 검증자 실행

### MCP servers

플러그인은 Claude Code를 외부 도구 및 서비스와 연결하기 위해 Model Context Protocol (MCP) servers를 번들로 제공할 수 있습니다.

**위치**: 플러그인 루트의 `.mcp.json` 또는 plugin.json에 인라인

**형식**: 표준 MCP 서버 구성

**MCP 서버 구성**:

```json  theme={null}
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    },
    "plugin-api-client": {
      "command": "npx",
      "args": ["@company/mcp-server", "--plugin-mode"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

**통합 동작**:

* 플러그인 MCP servers는 플러그인이 활성화될 때 자동으로 시작됩니다.
* Servers는 Claude의 도구 키트에서 표준 MCP 도구로 나타납니다.
* 서버 기능은 Claude의 기존 도구와 원활하게 통합됩니다.
* 플러그인 servers는 사용자 MCP servers와 독립적으로 구성할 수 있습니다.

### LSP servers

<Tip>
  LSP 플러그인을 사용하려고 하시나요? 공식 마켓플레이스에서 설치하세요: `/plugin` Discover 탭에서 "lsp"를 검색하세요. 이 섹션은 공식 마켓플레이스에서 다루지 않는 언어에 대해 LSP 플러그인을 만드는 방법을 문서화합니다.
</Tip>

플러그인은 [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) (LSP) servers를 제공하여 코드베이스에서 작업할 때 Claude에게 실시간 코드 인텔리전스를 제공할 수 있습니다.

LSP 통합은 다음을 제공합니다:

* **즉시 진단**: Claude는 각 편집 후 즉시 오류 및 경고를 봅니다.
* **코드 네비게이션**: 정의로 이동, 참조 찾기 및 호버 정보
* **언어 인식**: 코드 기호에 대한 타입 정보 및 문서

**위치**: 플러그인 루트의 `.lsp.json` 또는 `plugin.json`에 인라인

**형식**: 언어 서버 이름을 해당 구성에 매핑하는 JSON 구성

**`.lsp.json` 파일 형식**:

```json  theme={null}
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

**`plugin.json`에 인라인**:

```json  theme={null}
{
  "name": "my-plugin",
  "lspServers": {
    "go": {
      "command": "gopls",
      "args": ["serve"],
      "extensionToLanguage": {
        ".go": "go"
      }
    }
  }
}
```

**필수 필드:**

| 필드                    | 설명                         |
| :-------------------- | :------------------------- |
| `command`             | 실행할 LSP 바이너리 (PATH에 있어야 함) |
| `extensionToLanguage` | 파일 확장자를 언어 식별자에 매핑         |

**선택사항 필드:**

| 필드                      | 설명                                             |
| :---------------------- | :--------------------------------------------- |
| `args`                  | LSP 서버의 명령줄 인수                                 |
| `transport`             | 통신 전송: `stdio` (기본값) 또는 `socket`               |
| `env`                   | 서버 시작 시 설정할 환경 변수                              |
| `initializationOptions` | 초기화 중에 서버에 전달되는 옵션                             |
| `settings`              | `workspace/didChangeConfiguration`을 통해 전달되는 설정 |
| `workspaceFolder`       | 서버의 작업 공간 폴더 경로                                |
| `startupTimeout`        | 서버 시작을 기다릴 최대 시간 (밀리초)                         |
| `shutdownTimeout`       | 정상 종료를 기다릴 최대 시간 (밀리초)                         |
| `restartOnCrash`        | 서버가 충돌하면 자동으로 다시 시작할지 여부                       |
| `maxRestarts`           | 포기하기 전 최대 재시작 시도 횟수                            |

<Warning>
  **언어 서버 바이너리를 별도로 설치해야 합니다.** LSP 플러그인은 Claude Code가 언어 서버에 연결하는 방법을 구성하지만, 서버 자체는 포함하지 않습니다. `/plugin` Errors 탭에서 `Executable not found in $PATH`를 보면 언어에 필요한 바이너리를 설치하세요.
</Warning>

**사용 가능한 LSP 플러그인:**

| 플러그인             | 언어 서버                      | 설치 명령어                                                                          |
| :--------------- | :------------------------- | :------------------------------------------------------------------------------ |
| `pyright-lsp`    | Pyright (Python)           | `pip install pyright` 또는 `npm install -g pyright`                               |
| `typescript-lsp` | TypeScript Language Server | `npm install -g typescript-language-server typescript`                          |
| `rust-lsp`       | rust-analyzer              | [rust-analyzer 설치 참조](https://rust-analyzer.github.io/manual.html#installation) |

먼저 언어 서버를 설치한 다음 마켓플레이스에서 플러그인을 설치하세요.

***

## 플러그인 설치 범위

플러그인을 설치할 때 플러그인이 사용 가능한 위치와 다른 사람이 사용할 수 있는지를 결정하는 **범위**를 선택합니다:

| 범위        | 설정 파일                                  | 사용 사례                          |
| :-------- | :------------------------------------- | :----------------------------- |
| `user`    | `~/.claude/settings.json`              | 모든 프로젝트에서 사용 가능한 개인 플러그인 (기본값) |
| `project` | `.claude/settings.json`                | 버전 제어를 통해 공유되는 팀 플러그인          |
| `local`   | `.claude/settings.local.json`          | 프로젝트별 플러그인, gitignored         |
| `managed` | [관리되는 설정](/ko/settings#settings-files) | 관리되는 플러그인 (읽기 전용, 업데이트만 가능)    |

플러그인은 다른 Claude Code 구성과 동일한 범위 시스템을 사용합니다. 설치 지침 및 범위 플래그는 [플러그인 설치](/ko/discover-plugins#install-plugins)를 참조하세요. 범위에 대한 완전한 설명은 [구성 범위](/ko/settings#configuration-scopes)를 참조하세요.

***

## 플러그인 매니페스트 스키마

`.claude-plugin/plugin.json` 파일은 플러그인의 메타데이터 및 구성을 정의합니다. 이 섹션은 지원되는 모든 필드 및 옵션을 문서화합니다.

매니페스트는 선택사항입니다. 생략하면 Claude Code는 [기본 위치](#file-locations-reference)에서 컴포넌트를 자동으로 발견하고 디렉토리 이름에서 플러그인 이름을 파생합니다. 메타데이터를 제공하거나 사용자 정의 컴포넌트 경로가 필요할 때 매니페스트를 사용하세요.

### 완전한 스키마

```json  theme={null}
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "간단한 플러그인 설명",
  "author": {
    "name": "작성자 이름",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json"
}
```

### 필수 필드

매니페스트를 포함하는 경우 `name`이 유일한 필수 필드입니다.

| 필드     | 타입     | 설명                         | 예시                   |
| :----- | :----- | :------------------------- | :------------------- |
| `name` | string | 고유 식별자 (kebab-case, 공백 없음) | `"deployment-tools"` |

이 이름은 컴포넌트 네임스페이싱에 사용됩니다. 예를 들어 UI에서 이름이 `plugin-dev`인 플러그인의 agent `agent-creator`는 `plugin-dev:agent-creator`로 나타납니다.

### 메타데이터 필드

| 필드            | 타입     | 설명                                                                 | 예시                                                 |
| :------------ | :----- | :----------------------------------------------------------------- | :------------------------------------------------- |
| `version`     | string | 의미 있는 버전. 마켓플레이스 항목에도 설정된 경우 `plugin.json`이 우선합니다. 한 곳에만 설정하면 됩니다. | `"2.1.0"`                                          |
| `description` | string | 플러그인 목적에 대한 간단한 설명                                                 | `"배포 자동화 도구"`                                      |
| `author`      | object | 작성자 정보                                                             | `{"name": "Dev Team", "email": "dev@company.com"}` |
| `homepage`    | string | 문서 URL                                                             | `"https://docs.example.com"`                       |
| `repository`  | string | 소스 코드 URL                                                          | `"https://github.com/user/plugin"`                 |
| `license`     | string | 라이선스 식별자                                                           | `"MIT"`, `"Apache-2.0"`                            |
| `keywords`    | array  | 발견 태그                                                              | `["deployment", "ci-cd"]`                          |

### 컴포넌트 경로 필드

| 필드             | 타입                    | 설명                                                                                                              | 예시                                     |
| :------------- | :-------------------- | :-------------------------------------------------------------------------------------------------------------- | :------------------------------------- |
| `commands`     | string\|array         | 추가 명령어 파일/디렉토리                                                                                                  | `"./custom/cmd.md"` 또는 `["./cmd1.md"]` |
| `agents`       | string\|array         | 추가 agent 파일                                                                                                     | `"./custom/agents/reviewer.md"`        |
| `skills`       | string\|array         | 추가 skill 디렉토리                                                                                                   | `"./custom/skills/"`                   |
| `hooks`        | string\|array\|object | Hook 구성 경로 또는 인라인 구성                                                                                            | `"./my-extra-hooks.json"`              |
| `mcpServers`   | string\|array\|object | MCP 구성 경로 또는 인라인 구성                                                                                             | `"./my-extra-mcp-config.json"`         |
| `outputStyles` | string\|array         | 추가 출력 스타일 파일/디렉토리                                                                                               | `"./styles/"`                          |
| `lspServers`   | string\|array\|object | [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) 코드 인텔리전스 구성 (정의로 이동, 참조 찾기 등) | `"./.lsp.json"`                        |
| `userConfig`   | object                | 플러그인이 활성화될 때 사용자에게 프롬프트하는 사용자 구성 가능 값. [사용자 구성](#user-configuration) 참조                                         | 아래 참조                                  |
| `channels`     | array                 | 메시지 주입을 위한 채널 선언 (Telegram, Slack, Discord 스타일). [채널](#channels) 참조                                             | 아래 참조                                  |

### 사용자 구성

`userConfig` 필드는 플러그인이 활성화될 때 Claude Code가 사용자에게 프롬프트하는 값을 선언합니다. 사용자가 `settings.json`을 수동으로 편집하도록 요구하는 대신 이를 사용하세요.

```json  theme={null}
{
  "userConfig": {
    "api_endpoint": {
      "description": "팀의 API 엔드포인트",
      "sensitive": false
    },
    "api_token": {
      "description": "API 인증 토큰",
      "sensitive": true
    }
  }
}
```

키는 유효한 식별자여야 합니다. 각 값은 MCP 및 LSP 서버 구성, hook 명령어 및 (민감하지 않은 값만) skill 및 agent 콘텐츠에서 `${user_config.KEY}`로 대체할 수 있습니다. 값은 또한 플러그인 서브프로세스에 `CLAUDE_PLUGIN_OPTION_<KEY>` 환경 변수로 내보내집니다.

민감하지 않은 값은 `settings.json`의 `pluginConfigs[<plugin-id>].options` 아래에 저장됩니다. 민감한 값은 시스템 키체인 (또는 키체인을 사용할 수 없는 경우 `~/.claude/.credentials.json`)으로 이동합니다. 키체인 저장소는 OAuth 토큰과 공유되며 약 2 KB의 총 제한이 있으므로 민감한 값을 작게 유지하세요.

### 채널

`channels` 필드를 사용하면 플러그인이 하나 이상의 메시지 채널을 선언하여 대화에 콘텐츠를 주입할 수 있습니다. 각 채널은 플러그인이 제공하는 MCP 서버에 바인딩됩니다.

```json  theme={null}
{
  "channels": [
    {
      "server": "telegram",
      "userConfig": {
        "bot_token": { "description": "Telegram 봇 토큰", "sensitive": true },
        "owner_id": { "description": "Telegram 사용자 ID", "sensitive": false }
      }
    }
  ]
}
```

`server` 필드는 필수이며 플러그인의 `mcpServers`의 키와 일치해야 합니다. 선택사항인 채널별 `userConfig`는 최상위 필드와 동일한 스키마를 사용하여 플러그인이 플러그인이 활성화될 때 봇 토큰 또는 소유자 ID를 프롬프트할 수 있습니다.

### 경로 동작 규칙

**중요**: 사용자 정의 경로는 기본 디렉토리를 대체하지 않고 보완합니다.

* `commands/`가 존재하면 사용자 정의 명령어 경로와 함께 로드됩니다.
* 모든 경로는 플러그인 루트에 상대적이어야 하며 `./`로 시작해야 합니다.
* 사용자 정의 경로의 명령어는 동일한 명명 및 네임스페이싱 규칙을 사용합니다.
* 유연성을 위해 여러 경로를 배열로 지정할 수 있습니다.

**경로 예시**:

```json  theme={null}
{
  "commands": [
    "./specialized/deploy.md",
    "./utilities/batch-process.md"
  ],
  "agents": [
    "./custom-agents/reviewer.md",
    "./custom-agents/tester.md"
  ]
}
```

### 환경 변수

Claude Code는 플러그인 경로를 참조하기 위한 두 가지 변수를 제공합니다. 둘 다 skill 콘텐츠, agent 콘텐츠, hook 명령어 및 MCP 또는 LSP 서버 구성에 나타나는 모든 곳에서 인라인으로 대체됩니다. 둘 다 hook 프로세스 및 MCP 또는 LSP 서버 서브프로세스에 환경 변수로 내보내집니다.

**`${CLAUDE_PLUGIN_ROOT}`**: 플러그인 설치 디렉토리의 절대 경로입니다. 플러그인과 함께 번들로 제공되는 스크립트, 바이너리 및 구성 파일을 참조하는 데 사용하세요. 이 경로는 플러그인이 업데이트될 때 변경되므로 여기에 작성하는 파일은 업데이트 후 유지되지 않습니다.

**`${CLAUDE_PLUGIN_DATA}`**: 업데이트 후에도 유지되는 플러그인 상태를 위한 영구 디렉토리입니다. `node_modules` 또는 Python 가상 환경과 같은 설치된 종속성, 생성된 코드, 캐시 및 플러그인 버전 전체에서 유지되어야 하는 기타 파일에 사용하세요. 이 변수가 처음 참조될 때 디렉토리가 자동으로 생성됩니다.

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

#### 영구 데이터 디렉토리

`${CLAUDE_PLUGIN_DATA}` 디렉토리는 `~/.claude/plugins/data/{id}/`로 확인되며, 여기서 `{id}`는 `a-z`, `A-Z`, `0-9`, `_` 및 `-` 외부의 문자가 `-`로 대체된 플러그인 식별자입니다. `formatter@my-marketplace`로 설치된 플러그인의 경우 디렉토리는 `~/.claude/plugins/data/formatter-my-marketplace/`입니다.

일반적인 사용은 언어 종속성을 한 번 설치하고 세션 및 플러그인 업데이트 전체에서 재사용하는 것입니다. 데이터 디렉토리가 단일 플러그인 버전보다 오래 지속되므로 디렉토리 존재 여부만 확인하면 업데이트가 플러그인의 종속성 매니페스트를 변경할 때를 감지할 수 없습니다. 권장 패턴은 번들된 매니페스트를 데이터 디렉토리의 복사본과 비교하고 다를 때 다시 설치합니다.

이 `SessionStart` hook은 첫 실행 시 `node_modules`를 설치하고 플러그인 업데이트가 변경된 `package.json`을 포함할 때마다 다시 설치합니다:

```json  theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cd \"${CLAUDE_PLUGIN_DATA}\" && cp \"${CLAUDE_PLUGIN_ROOT}/package.json\" . && npm install) || rm -f \"${CLAUDE_PLUGIN_DATA}/package.json\""
          }
        ]
      }
    ]
  }
}
```

`diff`는 저장된 복사본이 누락되거나 번들된 복사본과 다를 때 0이 아닌 값으로 종료되어 첫 실행과 종속성 변경 업데이트를 모두 다룹니다. `npm install`이 실패하면 후행 `rm`은 복사된 매니페스트를 제거하므로 다음 세션이 다시 시도합니다.

`${CLAUDE_PLUGIN_ROOT}`에 번들된 스크립트는 지속된 `node_modules`에 대해 실행할 수 있습니다:

```json  theme={null}
{
  "mcpServers": {
    "routines": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
      "env": {
        "NODE_PATH": "${CLAUDE_PLUGIN_DATA}/node_modules"
      }
    }
  }
}
```

데이터 디렉토리는 플러그인을 설치한 마지막 범위에서 제거할 때 자동으로 삭제됩니다. `/plugin` 인터페이스는 디렉토리 크기를 표시하고 삭제 전에 프롬프트합니다. CLI는 기본적으로 삭제합니다. [`--keep-data`](#plugin-uninstall)를 전달하여 유지하세요.

***

## 플러그인 캐싱 및 파일 해석

플러그인은 두 가지 방법 중 하나로 지정됩니다:

* `claude --plugin-dir`을 통해, 세션 기간 동안.
* 마켓플레이스를 통해, 향후 세션을 위해 설치됨.

보안 및 검증 목적으로 Claude Code는 *마켓플레이스* 플러그인을 제자리에서 사용하는 대신 사용자의 로컬 **플러그인 캐시** (`~/.claude/plugins/cache`)에 복사합니다. 외부 파일을 참조하는 플러그인을 개발할 때 이 동작을 이해하는 것이 중요합니다.

### 경로 순회 제한

설치된 플러그인은 해당 디렉토리 외부의 파일을 참조할 수 없습니다. 플러그인 루트 외부를 순회하는 경로 (예: `../shared-utils`)는 설치 후 작동하지 않습니다. 왜냐하면 이러한 외부 파일이 캐시에 복사되지 않기 때문입니다.

### 외부 종속성 작업

플러그인이 디렉토리 외부의 파일에 액세스해야 하는 경우 플러그인 디렉토리 내에서 외부 파일에 대한 심볼릭 링크를 만들 수 있습니다. 심볼릭 링크는 복사 프로세스 중에 인정됩니다:

```bash  theme={null}
# 플러그인 디렉토리 내부
ln -s /path/to/shared-utils ./shared-utils
```

심볼릭 링크된 콘텐츠는 플러그인 캐시에 복사됩니다. 이는 캐싱 시스템의 보안 이점을 유지하면서 유연성을 제공합니다.

***

## 플러그인 디렉토리 구조

### 표준 플러그인 레이아웃

완전한 플러그인은 다음 구조를 따릅니다:

```text  theme={null}
enterprise-plugin/
├── .claude-plugin/           # 메타데이터 디렉토리 (선택사항)
│   └── plugin.json             # 플러그인 매니페스트
├── commands/                 # 기본 명령어 위치
│   ├── status.md
│   └── logs.md
├── agents/                   # 기본 agent 위치
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── skills/                   # Agent Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── hooks/                    # Hook 구성
│   ├── hooks.json           # 주 hook 구성
│   └── security-hooks.json  # 추가 hooks
├── settings.json            # 플러그인의 기본 설정
├── .mcp.json                # MCP 서버 정의
├── .lsp.json                # LSP 서버 구성
├── scripts/                 # Hook 및 유틸리티 스크립트
│   ├── security-scan.sh
│   ├── format-code.py
│   └── deploy.js
├── LICENSE                  # 라이선스 파일
└── CHANGELOG.md             # 버전 기록
```

<Warning>
  `.claude-plugin/` 디렉토리는 `plugin.json` 파일을 포함합니다. 다른 모든 디렉토리 (commands/, agents/, skills/, hooks/)는 `.claude-plugin/` 내부가 아닌 플러그인 루트에 있어야 합니다.
</Warning>

### 파일 위치 참조

| 컴포넌트            | 기본 위치                        | 목적                                                               |
| :-------------- | :--------------------------- | :--------------------------------------------------------------- |
| **매니페스트**       | `.claude-plugin/plugin.json` | 플러그인 메타데이터 및 구성 (선택사항)                                           |
| **명령어**         | `commands/`                  | Skill 마크다운 파일 (레거시; 새 skills에는 `skills/` 사용)                     |
| **Agents**      | `agents/`                    | Subagent 마크다운 파일                                                 |
| **Skills**      | `skills/`                    | `<name>/SKILL.md` 구조의 Skills                                     |
| **Hooks**       | `hooks/hooks.json`           | Hook 구성                                                          |
| **MCP servers** | `.mcp.json`                  | MCP 서버 정의                                                        |
| **LSP servers** | `.lsp.json`                  | 언어 서버 구성                                                         |
| **설정**          | `settings.json`              | 플러그인이 활성화될 때 적용되는 기본 구성. 현재 [`agent`](/ko/sub-agents) 설정만 지원됩니다. |

***

## CLI 명령어 참조

Claude Code는 스크립팅 및 자동화에 유용한 비대화형 플러그인 관리를 위한 CLI 명령어를 제공합니다.

### plugin install

사용 가능한 마켓플레이스에서 플러그인을 설치합니다.

```bash  theme={null}
claude plugin install <plugin> [options]
```

**인수:**

* `<plugin>`: 플러그인 이름 또는 특정 마켓플레이스의 경우 `plugin-name@marketplace-name`

**옵션:**

| 옵션                    | 설명                                  | 기본값    |
| :-------------------- | :---------------------------------- | :----- |
| `-s, --scope <scope>` | 설치 범위: `user`, `project` 또는 `local` | `user` |
| `-h, --help`          | 명령어 도움말 표시                          |        |

범위는 설치된 플러그인이 추가되는 설정 파일을 결정합니다. 예를 들어 --scope project는 `.claude/settings.json`의 `enabledPlugins`에 쓰므로 프로젝트 저장소를 복제하는 모든 사람이 플러그인을 사용할 수 있습니다.

**예시:**

```bash  theme={null}
# 사용자 범위에 설치 (기본값)
claude plugin install formatter@my-marketplace

# 프로젝트 범위에 설치 (팀과 공유)
claude plugin install formatter@my-marketplace --scope project

# 로컬 범위에 설치 (gitignored)
claude plugin install formatter@my-marketplace --scope local
```

### plugin uninstall

설치된 플러그인을 제거합니다.

```bash  theme={null}
claude plugin uninstall <plugin> [options]
```

**인수:**

* `<plugin>`: 플러그인 이름 또는 `plugin-name@marketplace-name`

**옵션:**

| 옵션                    | 설명                                                 | 기본값    |
| :-------------------- | :------------------------------------------------- | :----- |
| `-s, --scope <scope>` | 범위에서 제거: `user`, `project` 또는 `local`              | `user` |
| `--keep-data`         | 플러그인의 [영구 데이터 디렉토리](#persistent-data-directory) 유지 |        |
| `-h, --help`          | 명령어 도움말 표시                                         |        |

**별칭:** `remove`, `rm`

기본적으로 마지막 남은 범위에서 제거하면 플러그인의 `${CLAUDE_PLUGIN_DATA}` 디렉토리도 삭제됩니다. 새 버전 테스트 후 재설치할 때와 같이 유지하려면 `--keep-data`를 사용하세요.

### plugin enable

비활성화된 플러그인을 활성화합니다.

```bash  theme={null}
claude plugin enable <plugin> [options]
```

**인수:**

* `<plugin>`: 플러그인 이름 또는 `plugin-name@marketplace-name`

**옵션:**

| 옵션                    | 설명                                    | 기본값    |
| :-------------------- | :------------------------------------ | :----- |
| `-s, --scope <scope>` | 활성화할 범위: `user`, `project` 또는 `local` | `user` |
| `-h, --help`          | 명령어 도움말 표시                            |        |

### plugin disable

플러그인을 제거하지 않고 비활성화합니다.

```bash  theme={null}
claude plugin disable <plugin> [options]
```

**인수:**

* `<plugin>`: 플러그인 이름 또는 `plugin-name@marketplace-name`

**옵션:**

| 옵션                    | 설명                                     | 기본값    |
| :-------------------- | :------------------------------------- | :----- |
| `-s, --scope <scope>` | 비활성화할 범위: `user`, `project` 또는 `local` | `user` |
| `-h, --help`          | 명령어 도움말 표시                             |        |

### plugin update

플러그인을 최신 버전으로 업데이트합니다.

```bash  theme={null}
claude plugin update <plugin> [options]
```

**인수:**

* `<plugin>`: 플러그인 이름 또는 `plugin-name@marketplace-name`

**옵션:**

| 옵션                    | 설명                                                | 기본값    |
| :-------------------- | :------------------------------------------------ | :----- |
| `-s, --scope <scope>` | 업데이트할 범위: `user`, `project`, `local` 또는 `managed` | `user` |
| `-h, --help`          | 명령어 도움말 표시                                        |        |

***

## 디버깅 및 개발 도구

### 디버깅 명령어

`claude --debug`를 사용하여 플러그인 로딩 세부 정보를 확인하세요:

이는 다음을 표시합니다:

* 로드되는 플러그인
* 플러그인 매니페스트의 오류
* 명령어, agent 및 hook 등록
* MCP 서버 초기화

### 일반적인 문제

| 문제                                  | 원인                         | 해결책                                                                                                                                      |
| :---------------------------------- | :------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| 플러그인이 로드되지 않음                       | 잘못된 `plugin.json`          | `claude plugin validate` 또는 `/plugin validate`를 실행하여 `plugin.json`, skill/agent/command frontmatter 및 `hooks/hooks.json`의 구문 및 스키마 오류 확인 |
| 명령어가 나타나지 않음                        | 잘못된 디렉토리 구조                | `commands/`가 루트에 있는지 확인, `.claude-plugin/` 내부가 아님                                                                                        |
| Hooks가 실행되지 않음                      | 스크립트가 실행 가능하지 않음           | `chmod +x script.sh` 실행                                                                                                                  |
| MCP 서버 실패                           | `${CLAUDE_PLUGIN_ROOT}` 누락 | 모든 플러그인 경로에 변수 사용                                                                                                                        |
| 경로 오류                               | 절대 경로 사용됨                  | 모든 경로는 상대적이어야 하며 `./`로 시작해야 함                                                                                                            |
| LSP `Executable not found in $PATH` | 언어 서버가 설치되지 않음             | 바이너리 설치 (예: `npm install -g typescript-language-server typescript`)                                                                      |

### 예시 오류 메시지

**매니페스트 검증 오류**:

* `Invalid JSON syntax: Unexpected token } in JSON at position 142`: 누락된 쉼표, 추가 쉼표 또는 따옴표 없는 문자열 확인
* `Plugin has an invalid manifest file at .claude-plugin/plugin.json. Validation errors: name: Required`: 필수 필드가 누락됨
* `Plugin has a corrupt manifest file at .claude-plugin/plugin.json. JSON parse error: ...`: JSON 구문 오류

**플러그인 로딩 오류**:

* `Warning: No commands found in plugin my-plugin custom directory: ./cmds. Expected .md files or SKILL.md in subdirectories.`: 명령어 경로가 존재하지만 유효한 명령어 파일이 없음
* `Plugin directory not found at path: ./plugins/my-plugin. Check that the marketplace entry has the correct path.`: marketplace.json의 `source` 경로가 존재하지 않는 디렉토리를 가리킴
* `Plugin my-plugin has conflicting manifests: both plugin.json and marketplace entry specify components.`: 중복 컴포넌트 정의 제거 또는 marketplace 항목에서 `strict: false` 제거

### Hook 문제 해결

**Hook 스크립트가 실행되지 않음**:

1. 스크립트가 실행 가능한지 확인: `chmod +x ./scripts/your-script.sh`
2. shebang 라인 확인: 첫 번째 줄은 `#!/bin/bash` 또는 `#!/usr/bin/env bash`여야 함
3. 경로가 `${CLAUDE_PLUGIN_ROOT}` 사용하는지 확인: `"command": "${CLAUDE_PLUGIN_ROOT}/scripts/your-script.sh"`
4. 스크립트를 수동으로 테스트: `./scripts/your-script.sh`

**Hook이 예상 이벤트에서 트리거되지 않음**:

1. 이벤트 이름이 올바른지 확인 (대소문자 구분): `PostToolUse`, `postToolUse` 아님
2. 매처 패턴이 도구와 일치하는지 확인: 파일 작업의 경우 `"matcher": "Write|Edit"`
3. Hook 유형이 유효한지 확인: `command`, `http`, `prompt` 또는 `agent`

### MCP 서버 문제 해결

**서버가 시작되지 않음**:

1. 명령어가 존재하고 실행 가능한지 확인
2. 모든 경로가 `${CLAUDE_PLUGIN_ROOT}` 변수를 사용하는지 확인
3. MCP 서버 로그 확인: `claude --debug`는 초기화 오류를 표시합니다.
4. Claude Code 외부에서 서버를 수동으로 테스트

**서버 도구가 나타나지 않음**:

1. 서버가 `.mcp.json` 또는 `plugin.json`에 올바르게 구성되었는지 확인
2. 서버가 MCP 프로토콜을 올바르게 구현하는지 확인
3. 디버그 출력에서 연결 시간 초과 확인

### 디렉토리 구조 실수

**증상**: 플러그인이 로드되지만 컴포넌트 (명령어, agents, hooks)가 누락됨.

**올바른 구조**: 컴포넌트는 플러그인 루트에 있어야 하며 `.claude-plugin/` 내부가 아닙니다. `plugin.json`만 `.claude-plugin/`에 속합니다.

```text  theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json      ← 매니페스트만 여기
├── commands/            ← 루트 수준
├── agents/              ← 루트 수준
└── hooks/               ← 루트 수준
```

컴포넌트가 `.claude-plugin/` 내부에 있으면 플러그인 루트로 이동하세요.

**디버그 체크리스트**:

1. `claude --debug`를 실행하고 "loading plugin" 메시지를 찾으세요.
2. 각 컴포넌트 디렉토리가 디버그 출력에 나열되는지 확인
3. 파일 권한이 플러그인 파일 읽기를 허용하는지 확인

***

## 배포 및 버전 관리 참조

### 버전 관리

플러그인 릴리스에 대해 의미 있는 버전 관리를 따르세요:

```json  theme={null}
{
  "name": "my-plugin",
  "version": "2.1.0"
}
```

**버전 형식**: `MAJOR.MINOR.PATCH`

* **MAJOR**: 주요 변경 사항 (호환되지 않는 API 변경)
* **MINOR**: 새로운 기능 (하위 호환 추가)
* **PATCH**: 버그 수정 (하위 호환 수정)

**모범 사례**:

* 첫 번째 안정 릴리스에서 `1.0.0`으로 시작
* 변경 사항을 배포하기 전에 `plugin.json`의 버전 업데이트
* `CHANGELOG.md` 파일에 변경 사항 문서화
* 테스트를 위해 `2.0.0-beta.1`과 같은 사전 릴리스 버전 사용

<Warning>
  Claude Code는 버전을 사용하여 플러그인을 업데이트할지 여부를 결정합니다. 플러그인의 코드를 변경했지만 `plugin.json`의 버전을 범프하지 않으면 캐싱으로 인해 플러그인의 기존 사용자가 변경 사항을 보지 못합니다.

  플러그인이 [마켓플레이스](/ko/plugin-marketplaces) 디렉토리 내에 있으면 `marketplace.json`을 통해 버전을 관리할 수 있으며 `plugin.json`에서 `version` 필드를 생략할 수 있습니다.
</Warning>

***

## 참고 항목

* [플러그인](/ko/plugins) - 튜토리얼 및 실제 사용
* [플러그인 마켓플레이스](/ko/plugin-marketplaces) - 마켓플레이스 생성 및 관리
* [Skills](/ko/skills) - Skill 개발 세부 정보
* [Subagents](/ko/sub-agents) - Agent 구성 및 기능
* [Hooks](/ko/hooks) - 이벤트 처리 및 자동화
* [MCP](/ko/mcp) - 외부 도구 통합
* [설정](/ko/settings) - 플러그인의 구성 옵션
