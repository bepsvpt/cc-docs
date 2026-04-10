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

# Claude를 skills로 확장하기

> Claude Code에서 skills를 생성, 관리, 공유하여 Claude의 기능을 확장합니다. 사용자 정의 명령어와 번들 skills를 포함합니다.

Skills는 Claude가 할 수 있는 작업을 확장합니다. `SKILL.md` 파일을 지침과 함께 생성하면 Claude가 이를 자신의 도구 모음에 추가합니다. Claude는 관련이 있을 때 skills를 사용하거나 `/skill-name`으로 직접 호출할 수 있습니다.

<Note>
  `/help` 및 `/compact`와 같은 기본 제공 명령어는 [기본 제공 명령어 참조](/ko/commands)를 참조하세요.

  **사용자 정의 명령어가 skills로 병합되었습니다.** `.claude/commands/deploy.md`의 파일과 `.claude/skills/deploy/SKILL.md`의 skill은 모두 `/deploy`를 생성하고 동일하게 작동합니다. 기존 `.claude/commands/` 파일은 계속 작동합니다. Skills는 선택적 기능을 추가합니다: 지원 파일을 위한 디렉토리, [skill을 누가 호출하는지 제어](#control-who-invokes-a-skill)하기 위한 frontmatter, 그리고 Claude가 관련이 있을 때 자동으로 로드할 수 있는 기능입니다.
</Note>

Claude Code skills는 [Agent Skills](https://agentskills.io) 개방형 표준을 따르며, 이는 여러 AI 도구에서 작동합니다. Claude Code는 [호출 제어](#control-who-invokes-a-skill), [subagent 실행](#run-skills-in-a-subagent), [동적 컨텍스트 주입](#inject-dynamic-context)과 같은 추가 기능으로 표준을 확장합니다.

## 번들 skills

번들 skills는 Claude Code와 함께 제공되며 모든 세션에서 사용 가능합니다. 고정 로직을 직접 실행하는 [기본 제공 명령어](/ko/commands)와 달리, 번들 skills는 프롬프트 기반입니다: Claude에 상세한 플레이북을 제공하고 도구를 사용하여 작업을 조율하도록 합니다. 이는 번들 skills가 병렬 에이전트를 생성하고, 파일을 읽고, 코드베이스에 적응할 수 있음을 의미합니다.

번들 skills는 다른 skill과 동일한 방식으로 호출합니다: `/` 다음에 skill 이름을 입력합니다. 아래 표에서 `<arg>`는 필수 인수를 나타내고 `[arg]`는 선택적 인수를 나타냅니다.

| Skill                       | 목적                                                                                                                                                                                                                                                                                                                                  |
| :-------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/batch <instruction>`      | 코드베이스 전체에서 대규모 변경을 병렬로 조율합니다. 코드베이스를 조사하고, 작업을 5\~30개의 독립적인 단위로 분해하고, 계획을 제시합니다. 승인되면 각 단위당 하나의 백그라운드 에이전트를 격리된 [git worktree](/ko/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees)에서 생성합니다. 각 에이전트는 자신의 단위를 구현하고, 테스트를 실행하고, pull request를 엽니다. git 저장소가 필요합니다. 예: `/batch migrate src/ from Solid to React` |
| `/claude-api`               | 프로젝트의 언어(Python, TypeScript, Java, Go, Ruby, C#, PHP 또는 cURL)에 대한 Claude API 참조 자료와 Python 및 TypeScript에 대한 Agent SDK 참조를 로드합니다. 도구 사용, 스트리밍, 배치, 구조화된 출력 및 일반적인 함정을 다룹니다. 또한 코드가 `anthropic`, `@anthropic-ai/sdk` 또는 `claude_agent_sdk`를 가져올 때 자동으로 활성화됩니다.                                                                        |
| `/debug [description]`      | 현재 세션에 대해 디버그 로깅을 활성화하고 세션 디버그 로그를 읽어 문제를 해결합니다. 디버그 로깅은 `claude --debug`로 시작하지 않는 한 기본적으로 꺼져 있으므로, 세션 중간에 `/debug`를 실행하면 그 시점부터 로그 캡처를 시작합니다. 선택적으로 문제를 설명하여 분석에 초점을 맞춥니다.                                                                                                                                                         |
| `/loop [interval] <prompt>` | 세션이 열려 있는 동안 프롬프트를 간격에 따라 반복적으로 실행합니다. 배포를 폴링하거나, PR을 감시하거나, 다른 skill을 주기적으로 다시 실행하는 데 유용합니다. 예: `/loop 5m check if the deploy finished`. [일정에 따라 프롬프트 실행](/ko/scheduled-tasks)을 참조하세요.                                                                                                                                             |
| `/simplify [focus]`         | 최근에 변경된 파일에서 코드 재사용, 품질 및 효율성 문제를 검토한 후 수정합니다. 3개의 검토 에이전트를 병렬로 생성하고, 결과를 집계하고, 수정 사항을 적용합니다. 특정 관심사에 초점을 맞추기 위해 텍스트를 전달합니다: `/simplify focus on memory efficiency`                                                                                                                                                                 |

## 시작하기

### 첫 번째 skill 생성

이 예제는 Claude에게 시각적 다이어그램과 유추를 사용하여 코드를 설명하도록 가르치는 skill을 생성합니다. 기본 frontmatter를 사용하므로 Claude는 코드가 어떻게 작동하는지 물어볼 때 자동으로 로드하거나 `/explain-code`로 직접 호출할 수 있습니다.

<Steps>
  <Step title="skill 디렉토리 생성">
    개인 skills 폴더에 skill을 위한 디렉토리를 생성합니다. 개인 skills는 모든 프로젝트에서 사용 가능합니다.

    ```bash  theme={null}
    mkdir -p ~/.claude/skills/explain-code
    ```
  </Step>

  <Step title="SKILL.md 작성">
    모든 skill에는 두 부분이 있는 `SKILL.md` 파일이 필요합니다: Claude에게 skill을 언제 사용할지 알려주는 YAML frontmatter (`---` 마커 사이)와 skill이 호출될 때 Claude가 따르는 지침이 있는 markdown 콘텐츠입니다. `name` 필드는 `/slash-command`가 되고, `description`은 Claude가 자동으로 로드할 시기를 결정하는 데 도움이 됩니다.

    `~/.claude/skills/explain-code/SKILL.md` 생성:

    ```yaml  theme={null}
    ---
    name: explain-code
    description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
    ---

    When explaining code, always include:

    1. **Start with an analogy**: Compare the code to something from everyday life
    2. **Draw a diagram**: Use ASCII art to show the flow, structure, or relationships
    3. **Walk through the code**: Explain step-by-step what happens
    4. **Highlight a gotcha**: What's a common mistake or misconception?

    Keep explanations conversational. For complex concepts, use multiple analogies.
    ```
  </Step>

  <Step title="skill 테스트">
    두 가지 방법으로 테스트할 수 있습니다:

    **Claude가 자동으로 호출하도록 하기** - 설명과 일치하는 항목을 물어봅니다:

    ```text  theme={null}
    How does this code work?
    ```

    **또는 skill 이름으로 직접 호출하기**:

    ```text  theme={null}
    /explain-code src/auth/login.ts
    ```

    어느 쪽이든 Claude는 설명에 유추와 ASCII 다이어그램을 포함해야 합니다.
  </Step>
</Steps>

### Skills가 있는 위치

skill을 저장하는 위치에 따라 누가 사용할 수 있는지가 결정됩니다:

| 위치         | 경로                                       | 적용 대상         |
| :--------- | :--------------------------------------- | :------------ |
| Enterprise | [관리 설정](/ko/settings#settings-files) 참조  | 조직의 모든 사용자    |
| Personal   | `~/.claude/skills/<skill-name>/SKILL.md` | 모든 프로젝트       |
| Project    | `.claude/skills/<skill-name>/SKILL.md`   | 이 프로젝트만       |
| Plugin     | `<plugin>/skills/<skill-name>/SKILL.md`  | 플러그인이 활성화된 위치 |

Skills가 여러 수준에서 같은 이름을 공유할 때, 우선순위가 높은 위치가 우선합니다: enterprise > personal > project. Plugin skills는 `plugin-name:skill-name` 네임스페이스를 사용하므로 다른 수준과 충돌할 수 없습니다. `.claude/commands/`에 파일이 있으면 동일한 방식으로 작동하지만, skill과 명령어가 같은 이름을 공유하면 skill이 우선합니다.

#### 중첩된 디렉토리에서 자동 검색

하위 디렉토리의 파일로 작업할 때, Claude Code는 중첩된 `.claude/skills/` 디렉토리에서 skills를 자동으로 검색합니다. 예를 들어, `packages/frontend/`의 파일을 편집하는 경우, Claude Code는 `packages/frontend/.claude/skills/`에서도 skills를 찾습니다. 이는 패키지가 자신의 skills를 가진 monorepo 설정을 지원합니다.

각 skill은 `SKILL.md`를 진입점으로 하는 디렉토리입니다:

```text  theme={null}
my-skill/
├── SKILL.md           # 주요 지침 (필수)
├── template.md        # Claude가 채울 템플릿
├── examples/
│   └── sample.md      # 예상 형식을 보여주는 예제 출력
└── scripts/
    └── validate.sh    # Claude가 실행할 수 있는 스크립트
```

`SKILL.md`는 주요 지침을 포함하며 필수입니다. 다른 파일은 선택적이며 더 강력한 skills를 구축할 수 있습니다: Claude가 채울 템플릿, 예상 형식을 보여주는 예제 출력, Claude가 실행할 수 있는 스크립트 또는 상세한 참조 문서. `SKILL.md`에서 이러한 파일을 참조하여 Claude가 각 파일의 내용과 로드 시기를 알 수 있도록 합니다. 자세한 내용은 [지원 파일 추가](#add-supporting-files)를 참조하세요.

<Note>
  `.claude/commands/`의 파일은 계속 작동하며 동일한 [frontmatter](#frontmatter-reference)를 지원합니다. Skills는 지원 파일과 같은 추가 기능을 지원하므로 권장됩니다.
</Note>

#### 추가 디렉토리의 Skills

`--add-dir` 플래그는 [파일 액세스를 부여](/ko/permissions#additional-directories-grant-file-access-not-configuration)하지만 구성 검색은 하지 않습니다. 그러나 skills는 예외입니다: 추가된 디렉토리 내의 `.claude/skills/`는 자동으로 로드되고 라이브 변경 감지에 의해 선택되므로 세션을 다시 시작하지 않고도 이러한 skills를 편집할 수 있습니다.

subagents, 명령어 및 출력 스타일과 같은 다른 `.claude/` 구성은 추가 디렉토리에서 로드되지 않습니다. 로드되는 항목과 로드되지 않는 항목의 전체 목록과 프로젝트 간 구성을 공유하는 권장 방법은 [예외 표](/ko/permissions#additional-directories-grant-file-access-not-configuration)를 참조하세요.

<Note>
  `--add-dir` 디렉토리의 CLAUDE.md 파일은 기본적으로 로드되지 않습니다. 로드하려면 `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`을 설정하세요. [추가 디렉토리에서 로드](/ko/memory#load-from-additional-directories)를 참조하세요.
</Note>

## Skills 구성

Skills는 `SKILL.md` 상단의 YAML frontmatter와 그 뒤의 markdown 콘텐츠를 통해 구성됩니다.

### Skill 콘텐츠 유형

Skill 파일은 모든 지침을 포함할 수 있지만, 호출 방식을 생각하면 포함할 내용을 안내하는 데 도움이 됩니다:

**참조 콘텐츠**는 Claude가 현재 작업에 적용하는 지식을 추가합니다. 규칙, 패턴, 스타일 가이드, 도메인 지식. 이 콘텐츠는 인라인으로 실행되므로 Claude가 대화 컨텍스트와 함께 사용할 수 있습니다.

```yaml  theme={null}
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation
```

**작업 콘텐츠**는 배포, 커밋 또는 코드 생성과 같은 특정 작업에 대한 단계별 지침을 제공합니다. 이는 Claude가 자동으로 실행하도록 하기보다는 `/skill-name`으로 직접 호출하려는 작업입니다. `disable-model-invocation: true`를 추가하여 Claude가 자동으로 트리거하는 것을 방지합니다.

```yaml  theme={null}
---
name: deploy
description: Deploy the application to production
context: fork
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target
```

`SKILL.md`는 모든 것을 포함할 수 있지만, skill을 호출하는 방식(사용자, Claude 또는 둘 다)과 실행 위치(인라인 또는 subagent)를 생각하면 포함할 내용을 안내하는 데 도움이 됩니다. 복잡한 skills의 경우, [지원 파일을 추가](#add-supporting-files)하여 주요 skill을 집중적으로 유지할 수도 있습니다.

### Frontmatter 참조

markdown 콘텐츠 외에도, `SKILL.md` 파일 상단의 `---` 마커 사이의 YAML frontmatter 필드를 사용하여 skill 동작을 구성할 수 있습니다:

```yaml  theme={null}
---
name: my-skill
description: What this skill does
disable-model-invocation: true
allowed-tools: Read Grep
---

Your skill instructions here...
```

모든 필드는 선택적입니다. Claude가 skill을 언제 사용할지 알 수 있도록 `description`만 권장됩니다.

| 필드                         | 필수  | 설명                                                                                                                                                                                         |
| :------------------------- | :-- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                     | 아니오 | skill의 표시 이름. 생략하면 디렉토리 이름을 사용합니다. 소문자, 숫자 및 하이픈만 사용 가능(최대 64자).                                                                                                                           |
| `description`              | 권장  | skill이 무엇을 하는지, 언제 사용할지. Claude는 이를 사용하여 skill을 자동으로 적용할 시기를 결정합니다. 생략하면 markdown 콘텐츠의 첫 번째 단락을 사용합니다. 주요 사용 사례를 앞에 배치합니다: 250자보다 긴 설명은 컨텍스트 사용을 줄이기 위해 skill 목록에서 잘립니다.                   |
| `argument-hint`            | 아니오 | 예상 인수를 나타내기 위해 자동 완성 중에 표시되는 힌트. 예: `[issue-number]` 또는 `[filename] [format]`.                                                                                                             |
| `disable-model-invocation` | 아니오 | Claude가 이 skill을 자동으로 로드하는 것을 방지하려면 `true`로 설정합니다. `/name`으로 수동으로 트리거하려는 워크플로우에 사용합니다. 기본값: `false`.                                                                                       |
| `user-invocable`           | 아니오 | `/` 메뉴에서 숨기려면 `false`로 설정합니다. 사용자가 직접 호출하지 않아야 하는 배경 지식에 사용합니다. 기본값: `true`.                                                                                                               |
| `allowed-tools`            | 아니오 | 이 skill이 활성화되었을 때 Claude가 권한을 요청하지 않고 사용할 수 있는 도구. 공백으로 구분된 문자열 또는 YAML 목록을 허용합니다.                                                                                                         |
| `model`                    | 아니오 | 이 skill이 활성화되었을 때 사용할 모델.                                                                                                                                                                  |
| `effort`                   | 아니오 | [노력 수준](/ko/model-config#adjust-effort-level) - 이 skill이 활성화되었을 때. 세션 노력 수준을 재정의합니다. 기본값: 세션에서 상속. 옵션: `low`, `medium`, `high`, `max` (Opus 4.6만 해당).                                      |
| `context`                  | 아니오 | forked subagent 컨텍스트에서 실행하려면 `fork`로 설정합니다.                                                                                                                                                |
| `agent`                    | 아니오 | `context: fork`가 설정되었을 때 사용할 subagent 유형.                                                                                                                                                  |
| `hooks`                    | 아니오 | 이 skill의 라이프사이클에 범위가 지정된 hooks. 구성 형식은 [Skills 및 agents의 Hooks](/ko/hooks#hooks-in-skills-and-agents)를 참조하세요.                                                                              |
| `paths`                    | 아니오 | 이 skill이 활성화되는 시기를 제한하는 Glob 패턴. 쉼표로 구분된 문자열 또는 YAML 목록을 허용합니다. 설정하면 Claude는 패턴과 일치하는 파일로 작업할 때만 자동으로 skill을 로드합니다. [경로별 규칙](/ko/memory#path-specific-rules)과 동일한 형식을 사용합니다.               |
| `shell`                    | 아니오 | 이 skill의 `` !`command` `` 블록에 사용할 shell. `bash`(기본값) 또는 `powershell`을 허용합니다. `powershell`을 설정하면 Windows에서 PowerShell을 통해 인라인 shell 명령어를 실행합니다. `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`이 필요합니다. |

#### 사용 가능한 문자열 치환

Skills는 skill 콘텐츠의 동적 값에 대한 문자열 치환을 지원합니다:

| 변수                     | 설명                                                                                                                                                                      |
| :--------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$ARGUMENTS`           | skill을 호출할 때 전달된 모든 인수. `$ARGUMENTS`가 콘텐츠에 없으면 인수가 `ARGUMENTS: <value>`로 추가됩니다.                                                                                         |
| `$ARGUMENTS[N]`        | 0 기반 인덱스로 특정 인수에 액세스합니다(예: `$ARGUMENTS[0]`은 첫 번째 인수).                                                                                                                   |
| `$N`                   | `$ARGUMENTS[N]`의 약자(예: `$0`은 첫 번째 인수, `$1`은 두 번째 인수).                                                                                                                   |
| `${CLAUDE_SESSION_ID}` | 현재 세션 ID. 로깅, 세션별 파일 생성 또는 skill 출력을 세션과 연관시키는 데 유용합니다.                                                                                                                 |
| `${CLAUDE_SKILL_DIR}`  | skill의 `SKILL.md` 파일을 포함하는 디렉토리. plugin skills의 경우, 이는 plugin 루트가 아닌 plugin 내의 skill 하위 디렉토리입니다. bash 주입 명령어에서 현재 작업 디렉토리와 관계없이 skill과 함께 번들된 스크립트 또는 파일을 참조하는 데 사용합니다. |

**치환을 사용한 예제:**

```yaml  theme={null}
---
name: session-logger
description: Log activity for this session
---

Log the following to logs/${CLAUDE_SESSION_ID}.log:

$ARGUMENTS
```

### 지원 파일 추가

Skills는 디렉토리에 여러 파일을 포함할 수 있습니다. 이는 `SKILL.md`를 필수 항목에 집중하게 하면서 Claude가 필요할 때만 상세한 참조 자료에 액세스할 수 있게 합니다. 큰 참조 문서, API 사양 또는 예제 컬렉션은 skill이 실행될 때마다 컨텍스트에 로드될 필요가 없습니다.

```text  theme={null}
my-skill/
├── SKILL.md (required - overview and navigation)
├── reference.md (detailed API docs - loaded when needed)
├── examples.md (usage examples - loaded when needed)
└── scripts/
    └── helper.py (utility script - executed, not loaded)
```

`SKILL.md`에서 지원 파일을 참조하여 Claude가 각 파일의 내용과 로드 시기를 알 수 있도록 합니다:

```markdown  theme={null}
## Additional resources

- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

<Tip>`SKILL.md`를 500줄 이하로 유지합니다. 상세한 참조 자료를 별도 파일로 이동합니다.</Tip>

### Skill을 호출하는 사람 제어

기본적으로 사용자와 Claude 모두 모든 skill을 호출할 수 있습니다. `/skill-name`을 입력하여 직접 호출할 수 있고, Claude는 대화와 관련이 있을 때 자동으로 로드할 수 있습니다. 두 frontmatter 필드를 사용하여 이를 제한할 수 있습니다:

* **`disable-model-invocation: true`**: 사용자만 skill을 호출할 수 있습니다. 부작용이 있거나 타이밍을 제어하려는 워크플로우(예: `/commit`, `/deploy` 또는 `/send-slack-message`)에 사용합니다. Claude가 코드가 준비된 것처럼 보인다고 해서 배포하기로 결정하지 않기를 원합니다.

* **`user-invocable: false`**: Claude만 skill을 호출할 수 있습니다. 명령어로 실행할 수 없는 배경 지식에 사용합니다. `legacy-system-context` skill은 오래된 시스템이 어떻게 작동하는지 설명합니다. Claude는 관련이 있을 때 이를 알아야 하지만, `/legacy-system-context`는 사용자가 취할 의미 있는 작업이 아닙니다.

이 예제는 사용자만 트리거할 수 있는 배포 skill을 생성합니다. `disable-model-invocation: true` 필드는 Claude가 자동으로 실행하는 것을 방지합니다:

```yaml  theme={null}
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
---

Deploy $ARGUMENTS to production:

1. Run the test suite
2. Build the application
3. Push to the deployment target
4. Verify the deployment succeeded
```

두 필드가 호출 및 컨텍스트 로딩에 미치는 영향은 다음과 같습니다:

| Frontmatter                      | 사용자가 호출 가능 | Claude가 호출 가능 | 컨텍스트에 로드되는 시기                          |
| :------------------------------- | :--------- | :------------ | :------------------------------------- |
| (기본값)                            | 예          | 예             | 설명은 항상 컨텍스트에 있고, 호출될 때 전체 skill이 로드됨   |
| `disable-model-invocation: true` | 예          | 아니오           | 설명은 컨텍스트에 없고, 사용자가 호출할 때 전체 skill이 로드됨 |
| `user-invocable: false`          | 아니오        | 예             | 설명은 항상 컨텍스트에 있고, 호출될 때 전체 skill이 로드됨   |

<Note>
  일반 세션에서 skill 설명은 Claude가 사용 가능한 항목을 알 수 있도록 컨텍스트에 로드되지만, 전체 skill 콘텐츠는 호출될 때만 로드됩니다. [미리 로드된 skills가 있는 Subagents](/ko/sub-agents#preload-skills-into-subagents)는 다르게 작동합니다: 전체 skill 콘텐츠는 시작 시 주입됩니다.
</Note>

### 도구 액세스 제한

`allowed-tools` 필드를 사용하여 skill이 활성화되었을 때 Claude가 사용할 수 있는 도구를 제한합니다. 이 skill은 Claude가 파일을 탐색할 수 있지만 수정할 수 없는 읽기 전용 모드를 생성합니다:

```yaml  theme={null}
---
name: safe-reader
description: Read files without making changes
allowed-tools: Read Grep Glob
---
```

### Skills에 인수 전달

사용자와 Claude 모두 skill을 호출할 때 인수를 전달할 수 있습니다. 인수는 `$ARGUMENTS` 플레이스홀더를 통해 사용 가능합니다.

이 skill은 GitHub 이슈를 번호로 수정합니다. `$ARGUMENTS` 플레이스홀더는 skill 이름 뒤에 오는 모든 것으로 대체됩니다:

```yaml  theme={null}
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.

1. Read the issue description
2. Understand the requirements
3. Implement the fix
4. Write tests
5. Create a commit
```

`/fix-issue 123`을 실행하면 Claude는 "Fix GitHub issue 123 following our coding standards..."를 받습니다.

인수를 사용하여 skill을 호출하지만 skill에 `$ARGUMENTS`가 포함되지 않으면, Claude Code는 `ARGUMENTS: <your input>`을 skill 콘텐츠의 끝에 추가하므로 Claude는 여전히 입력한 내용을 봅니다.

위치별로 개별 인수에 액세스하려면 `$ARGUMENTS[N]` 또는 더 짧은 `$N`을 사용합니다:

```yaml  theme={null}
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $ARGUMENTS[0] component from $ARGUMENTS[1] to $ARGUMENTS[2].
Preserve all existing behavior and tests.
```

`/migrate-component SearchBar React Vue`를 실행하면 `$ARGUMENTS[0]`을 `SearchBar`로, `$ARGUMENTS[1]`을 `React`로, `$ARGUMENTS[2]`를 `Vue`로 대체합니다. `$N` 약자를 사용하는 동일한 skill:

```yaml  theme={null}
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.
```

## 고급 패턴

### 동적 컨텍스트 주입

`` !`<command>` `` 구문은 skill 콘텐츠가 Claude로 전송되기 전에 shell 명령어를 실행합니다. 명령어 출력이 플레이스홀더를 대체하므로 Claude는 명령어 자체가 아닌 실제 데이터를 받습니다.

이 skill은 GitHub CLI를 사용하여 라이브 PR 데이터를 가져와 pull request를 요약합니다. `` !`gh pr diff` `` 및 기타 명령어가 먼저 실행되고, 출력이 프롬프트에 삽입됩니다:

```yaml  theme={null}
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

이 skill이 실행될 때:

1. 각 `` !`<command>` ``가 즉시 실행됩니다(Claude가 보기 전에).
2. 출력이 skill 콘텐츠의 플레이스홀더를 대체합니다.
3. Claude는 실제 PR 데이터가 있는 완전히 렌더링된 프롬프트를 받습니다.

이는 전처리이며, Claude가 실행하는 것이 아닙니다. Claude는 최종 결과만 봅니다.

<Tip>
  skill에서 [확장 사고](/ko/common-workflows#use-extended-thinking-thinking-mode)를 활성화하려면 skill 콘텐츠의 어디든 "ultrathink"라는 단어를 포함합니다.
</Tip>

### Subagent에서 Skills 실행

skill을 격리 상태에서 실행하려면 frontmatter에 `context: fork`를 추가합니다. skill 콘텐츠는 subagent를 구동하는 프롬프트가 됩니다. 대화 기록에 액세스할 수 없습니다.

<Warning>
  `context: fork`는 명시적 지침이 있는 skills에만 의미가 있습니다. skill에 작업 없이 "이 API 규칙을 사용하세요"와 같은 지침이 포함되어 있으면, subagent는 지침을 받지만 실행 가능한 프롬프트가 없으므로 의미 있는 출력 없이 반환됩니다.
</Warning>

Skills와 [subagents](/ko/sub-agents)는 두 방향으로 함께 작동합니다:

| 접근 방식                     | 시스템 프롬프트                       | 작업             | 또한 로드                     |
| :------------------------ | :----------------------------- | :------------- | :------------------------ |
| `context: fork`가 있는 Skill | 에이전트 유형(`Explore`, `Plan` 등)에서 | SKILL.md 콘텐츠   | CLAUDE.md                 |
| `skills` 필드가 있는 Subagent  | Subagent의 markdown 본문          | Claude의 위임 메시지 | 미리 로드된 skills + CLAUDE.md |

`context: fork`를 사용하면 skill에 작업을 작성하고 실행할 에이전트 유형을 선택합니다. 역방향(skills를 참조 자료로 사용하는 사용자 정의 subagent 정의)은 [Subagents](/ko/sub-agents#preload-skills-into-subagents)를 참조하세요.

#### 예제: Explore 에이전트를 사용하는 Research Skill

이 skill은 forked Explore 에이전트에서 연구를 실행합니다. skill 콘텐츠는 작업이 되고, 에이전트는 코드베이스 탐색에 최적화된 읽기 전용 도구를 제공합니다:

```yaml  theme={null}
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

이 skill이 실행될 때:

1. 새로운 격리된 컨텍스트가 생성됩니다.
2. subagent는 skill 콘텐츠를 프롬프트로 받습니다("Research \$ARGUMENTS thoroughly...").
3. `agent` 필드는 실행 환경(모델, 도구 및 권한)을 결정합니다.
4. 결과는 요약되어 주 대화로 반환됩니다.

`agent` 필드는 사용할 subagent 구성을 지정합니다. 옵션에는 기본 제공 에이전트(`Explore`, `Plan`, `general-purpose`) 또는 `.claude/agents/`의 모든 사용자 정의 subagent가 포함됩니다. 생략하면 `general-purpose`를 사용합니다.

### Claude의 Skill 액세스 제한

기본적으로 Claude는 `disable-model-invocation: true`가 설정되지 않은 모든 skill을 호출할 수 있습니다. `allowed-tools`를 정의하는 Skills는 skill이 활성화되었을 때 사용자별 승인 없이 Claude에게 이러한 도구에 대한 액세스를 부여합니다. [권한 설정](/ko/permissions)은 여전히 다른 모든 도구에 대한 기본 승인 동작을 관리합니다. `/compact` 및 `/init`과 같은 기본 제공 명령어는 Skill 도구를 통해 사용할 수 없습니다.

Claude가 호출할 수 있는 skills를 제어하는 세 가지 방법:

**`/permissions`에서 Skill 도구를 거부하여 모든 skills를 비활성화합니다:**

```text  theme={null}
# Add to deny rules:
Skill
```

**[권한 규칙](/ko/permissions)을 사용하여 특정 skills를 허용하거나 거부합니다:**

```text  theme={null}
# Allow only specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)
```

권한 구문: 정확한 일치는 `Skill(name)`, 모든 인수를 사용한 접두사 일치는 `Skill(name *)`.

**개별 skills를 숨기기** - frontmatter에 `disable-model-invocation: true`를 추가합니다. 이는 Claude의 컨텍스트에서 skill을 완전히 제거합니다.

<Note>
  `user-invocable` 필드는 메뉴 가시성만 제어하고 Skill 도구 액세스는 제어하지 않습니다. 프로그래밍 방식 호출을 차단하려면 `disable-model-invocation: true`를 사용합니다.
</Note>

## Skills 공유

Skills는 대상에 따라 다양한 범위에서 배포할 수 있습니다:

* **프로젝트 skills**: `.claude/skills/`를 버전 제어에 커밋합니다.
* **플러그인**: [플러그인](/ko/plugins)에서 `skills/` 디렉토리를 생성합니다.
* **관리**: [관리 설정](/ko/settings#settings-files)을 통해 조직 전체에 배포합니다.

### 시각적 출력 생성

Skills는 모든 언어의 스크립트를 번들하고 실행할 수 있으므로 Claude에게 단일 프롬프트로 가능한 것 이상의 기능을 제공합니다. 강력한 패턴 중 하나는 시각적 출력을 생성하는 것입니다: 브라우저에서 열리는 대화형 HTML 파일로 데이터 탐색, 디버깅 또는 보고서 생성에 사용됩니다.

이 예제는 코드베이스 탐색기를 생성합니다: 디렉토리를 확장 및 축소할 수 있는 대화형 트리 보기로, 한눈에 파일 크기를 보고, 색상으로 파일 유형을 식별할 수 있습니다.

Skill 디렉토리 생성:

```bash  theme={null}
mkdir -p ~/.claude/skills/codebase-visualizer/scripts
```

`~/.claude/skills/codebase-visualizer/SKILL.md` 생성. 설명은 Claude에게 이 Skill을 언제 활성화할지 알려주고, 지침은 Claude에게 번들 스크립트를 실행하도록 알려줍니다:

````yaml  theme={null}
---
name: codebase-visualizer
description: Generate an interactive collapsible tree visualization of your codebase. Use when exploring a new repo, understanding project structure, or identifying large files.
allowed-tools: Bash(python *)
---

# Codebase Visualizer

Generate an interactive HTML tree view that shows your project's file structure with collapsible directories.

## Usage

Run the visualization script from your project root:

```bash
python ~/.claude/skills/codebase-visualizer/scripts/visualize.py .
```

This creates `codebase-map.html` in the current directory and opens it in your default browser.

## What the visualization shows

- **Collapsible directories**: Click folders to expand/collapse
- **File sizes**: Displayed next to each file
- **Colors**: Different colors for different file types
- **Directory totals**: Shows aggregate size of each folder
````

`~/.claude/skills/codebase-visualizer/scripts/visualize.py` 생성. 이 스크립트는 디렉토리 트리를 스캔하고 다음을 포함하는 자체 포함 HTML 파일을 생성합니다:

* 파일 수, 디렉토리 수, 총 크기 및 파일 유형 수를 보여주는 **요약 사이드바**
* 파일 유형별로 코드베이스를 분석하는 **막대 차트**(크기 기준 상위 8개)
* 디렉토리를 확장 및 축소할 수 있는 **축소 가능한 트리**로, 색상으로 코딩된 파일 유형 표시기 포함

스크립트는 Python이 필요하지만 기본 제공 라이브러리만 사용하므로 설치할 패키지가 없습니다:

```python expandable theme={null}
#!/usr/bin/env python3
"""Generate an interactive collapsible tree visualization of a codebase."""

import json
import sys
import webbrowser
from pathlib import Path
from collections import Counter

IGNORE = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}

def scan(path: Path, stats: dict) -> dict:
    result = {"name": path.name, "children": [], "size": 0}
    try:
        for item in sorted(path.iterdir()):
            if item.name in IGNORE or item.name.startswith('.'):
                continue
            if item.is_file():
                size = item.stat().st_size
                ext = item.suffix.lower() or '(no ext)'
                result["children"].append({"name": item.name, "size": size, "ext": ext})
                result["size"] += size
                stats["files"] += 1
                stats["extensions"][ext] += 1
                stats["ext_sizes"][ext] += size
            elif item.is_dir():
                stats["dirs"] += 1
                child = scan(item, stats)
                if child["children"]:
                    result["children"].append(child)
                    result["size"] += child["size"]
    except PermissionError:
        pass
    return result

def generate_html(data: dict, stats: dict, output: Path) -> None:
    ext_sizes = stats["ext_sizes"]
    total_size = sum(ext_sizes.values()) or 1
    sorted_exts = sorted(ext_sizes.items(), key=lambda x: -x[1])[:8]
    colors = {
        '.js': '#f7df1e', '.ts': '#3178c6', '.py': '#3776ab', '.go': '#00add8',
        '.rs': '#dea584', '.rb': '#cc342d', '.css': '#264de4', '.html': '#e34c26',
        '.json': '#6b7280', '.md': '#083fa1', '.yaml': '#cb171e', '.yml': '#cb171e',
        '.mdx': '#083fa1', '.tsx': '#3178c6', '.jsx': '#61dafb', '.sh': '#4eaa25',
    }
    lang_bars = "".join(
        f'<div class="bar-row"><span class="bar-label">{ext}</span>'
        f'<div class="bar" style="width:{(size/total_size)*100}%;background:{colors.get(ext,"#6b7280")}"></div>'
        f'<span class="bar-pct">{(size/total_size)*100:.1f}%</span></div>'
        for ext, size in sorted_exts
    )
    def fmt(b):
        if b < 1024: return f"{b} B"
        if b < 1048576: return f"{b/1024:.1f} KB"
        return f"{b/1048576:.1f} MB"

    html = f'''<!DOCTYPE html>
<html><head>
  <meta charset="utf-8"><title>Codebase Explorer</title>
  <style>
    body {{ font: 14px/1.5 system-ui, sans-serif; margin: 0; background: #1a1a2e; color: #eee; }}
    .container {{ display: flex; height: 100vh; }}
    .sidebar {{ width: 280px; background: #252542; padding: 20px; border-right: 1px solid #3d3d5c; overflow-y: auto; flex-shrink: 0; }}
    .main {{ flex: 1; padding: 20px; overflow-y: auto; }}
    h1 {{ margin: 0 0 10px 0; font-size: 18px; }}
    h2 {{ margin: 20px 0 10px 0; font-size: 14px; color: #888; text-transform: uppercase; }}
    .stat {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #3d3d5c; }}
    .stat-value {{ font-weight: bold; }}
    .bar-row {{ display: flex; align-items: center; margin: 6px 0; }}
    .bar-label {{ width: 55px; font-size: 12px; color: #aaa; }}
    .bar {{ height: 18px; border-radius: 3px; }}
    .bar-pct {{ margin-left: 8px; font-size: 12px; color: #666; }}
    .tree {{ list-style: none; padding-left: 20px; }}
    details {{ cursor: pointer; }}
    summary {{ padding: 4px 8px; border-radius: 4px; }}
    summary:hover {{ background: #2d2d44; }}
    .folder {{ color: #ffd700; }}
    .file {{ display: flex; align-items: center; padding: 4px 8px; border-radius: 4px; }}
    .file:hover {{ background: #2d2d44; }}
    .size {{ color: #888; margin-left: auto; font-size: 12px; }}
    .dot {{ width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; }}
  </style>
</head><body>
  <div class="container">
    <div class="sidebar">
      <h1>📊 Summary</h1>
      <div class="stat"><span>Files</span><span class="stat-value">{stats["files"]:,}</span></div>
      <div class="stat"><span>Directories</span><span class="stat-value">{stats["dirs"]:,}</span></div>
      <div class="stat"><span>Total size</span><span class="stat-value">{fmt(data["size"])}</span></div>
      <div class="stat"><span>File types</span><span class="stat-value">{len(stats["extensions"])}</span></div>
      <h2>By file type</h2>
      {lang_bars}
    </div>
    <div class="main">
      <h1>📁 {data["name"]}</h1>
      <ul class="tree" id="root"></ul>
    </div>
  </div>
  <script>
    const data = {json.dumps(data)};
    const colors = {json.dumps(colors)};
    function fmt(b) {{ if (b < 1024) return b + ' B'; if (b < 1048576) return (b/1024).toFixed(1) + ' KB'; return (b/1048576).toFixed(1) + ' MB'; }}
    function render(node, parent) {{
      if (node.children) {{
        const det = document.createElement('details');
        det.open = parent === document.getElementById('root');
        det.innerHTML = `<summary><span class="folder">📁 ${{node.name}}</span><span class="size">${{fmt(node.size)}}</span></summary>`;
        const ul = document.createElement('ul'); ul.className = 'tree';
        node.children.sort((a,b) => (b.children?1:0)-(a.children?1:0) || a.name.localeCompare(b.name));
        node.children.forEach(c => render(c, ul));
        det.appendChild(ul);
        const li = document.createElement('li'); li.appendChild(det); parent.appendChild(li);
      }} else {{
        const li = document.createElement('li'); li.className = 'file';
        li.innerHTML = `<span class="dot" style="background:${{colors[node.ext]||'#6b7280'}}"></span>${{node.name}}<span class="size">${{fmt(node.size)}}</span>`;
        parent.appendChild(li);
      }}
    }}
    data.children.forEach(c => render(c, document.getElementById('root')));
  </script>
</body></html>'''
    output.write_text(html)

if __name__ == '__main__':
    target = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    stats = {"files": 0, "dirs": 0, "extensions": Counter(), "ext_sizes": Counter()}
    data = scan(target, stats)
    out = Path('codebase-map.html')
    generate_html(data, stats, out)
    print(f'Generated {out.absolute()}')
    webbrowser.open(f'file://{out.absolute()}')
```

테스트하려면 모든 프로젝트에서 Claude Code를 열고 "Visualize this codebase"를 요청합니다. Claude는 스크립트를 실행하고, `codebase-map.html`을 생성하고, 브라우저에서 엽니다.

이 패턴은 모든 시각적 출력에 작동합니다: 종속성 그래프, 테스트 커버리지 보고서, API 문서 또는 데이터베이스 스키마 시각화. 번들 스크립트가 무거운 작업을 수행하는 동안 Claude는 조율을 처리합니다.

## 문제 해결

### Skill이 트리거되지 않음

Claude가 예상대로 skill을 사용하지 않는 경우:

1. 설명에 사용자가 자연스럽게 말할 키워드가 포함되어 있는지 확인합니다.
2. skill이 `What skills are available?`에 나타나는지 확인합니다.
3. 설명과 더 가깝게 일치하도록 요청을 다시 표현해봅니다.
4. skill이 사용자 호출 가능하면 `/skill-name`으로 직접 호출합니다.

### Skill이 너무 자주 트리거됨

Claude가 원하지 않을 때 skill을 사용하는 경우:

1. 설명을 더 구체적으로 만듭니다.
2. 수동 호출만 원하면 `disable-model-invocation: true`를 추가합니다.

### Skill 설명이 잘림

Skill 설명은 Claude가 사용 가능한 항목을 알 수 있도록 컨텍스트에 로드됩니다. 모든 skill 이름은 항상 포함되지만, 많은 skills가 있으면 설명이 단축되어 문자 예산에 맞출 수 있으며, 이는 Claude가 요청과 일치하는 데 필요한 키워드를 제거할 수 있습니다. 예산은 컨텍스트 윈도우의 1%에서 동적으로 확장되며, 8,000자의 폴백이 있습니다.

제한을 높이려면 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 환경 변수를 설정합니다. 또는 소스에서 설명을 자릅니다: 주요 사용 사례를 앞에 배치합니다. 각 항목은 예산과 관계없이 250자로 제한됩니다.

## 관련 리소스

* **[Subagents](/ko/sub-agents)**: 특화된 에이전트에 작업 위임
* **[플러그인](/ko/plugins)**: 다른 확장과 함께 skills 패키징 및 배포
* **[Hooks](/ko/hooks)**: 도구 이벤트 주변 워크플로우 자동화
* **[메모리](/ko/memory)**: 지속적인 컨텍스트를 위한 CLAUDE.md 파일 관리
* **[기본 제공 명령어](/ko/commands)**: 기본 제공 `/` 명령어 참조
* **[권한](/ko/permissions)**: 도구 및 skill 액세스 제어
