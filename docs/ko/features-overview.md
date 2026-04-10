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

# Claude Code 확장하기

> CLAUDE.md, Skills, subagents, hooks, MCP, 플러그인을 언제 사용할지 이해합니다.

Claude Code는 코드를 추론하는 모델과 파일 작업, 검색, 실행 및 웹 접근을 위한 [내장 도구](/ko/how-claude-code-works#tools)를 결합합니다. 내장 도구는 대부분의 코딩 작업을 다룹니다. 이 가이드는 확장 계층을 다룹니다. Claude가 알아야 할 내용을 사용자 정의하고, 외부 서비스에 연결하고, 워크플로우를 자동화하기 위해 추가하는 기능입니다.

<Note>
  핵심 에이전트 루프가 어떻게 작동하는지 알아보려면 [Claude Code 작동 방식](/ko/how-claude-code-works)을 참조하세요.
</Note>

**Claude Code를 처음 사용하시나요?** 프로젝트 규칙을 위해 [CLAUDE.md](/ko/memory)로 시작하세요. 필요에 따라 다른 확장을 추가하세요.

## 개요

확장은 에이전트 루프의 다양한 부분에 연결됩니다.

* \*\*[CLAUDE.md](/ko/memory)\*\*는 Claude가 모든 세션에서 보는 지속적인 컨텍스트를 추가합니다.
* \*\*[Skills](/ko/skills)\*\*는 재사용 가능한 지식과 호출 가능한 워크플로우를 추가합니다.
* \*\*[MCP](/ko/mcp)\*\*는 Claude를 외부 서비스 및 도구에 연결합니다.
* \*\*[Subagents](/ko/sub-agents)\*\*는 격리된 컨텍스트에서 자신의 루프를 실행하고 요약을 반환합니다.
* \*\*[Agent teams](/ko/agent-teams)\*\*는 공유 작업 및 피어 투 피어 메시징으로 여러 독립적인 세션을 조정합니다.
* \*\*[Hooks](/ko/hooks)\*\*는 결정론적 스크립트로 루프 외부에서 완전히 실행됩니다.
* **[Plugins](/ko/plugins)** 및 \*\*[marketplaces](/ko/plugin-marketplaces)\*\*는 이러한 기능을 패키징하고 배포합니다.

[Skills](/ko/skills)는 가장 유연한 확장입니다. Skill은 지식, 워크플로우 또는 지침을 포함하는 마크다운 파일입니다. `/deploy`와 같은 명령으로 skill을 호출하거나, Claude가 관련이 있을 때 자동으로 로드할 수 있습니다. Skill은 현재 대화에서 실행되거나 subagents를 통해 격리된 컨텍스트에서 실행될 수 있습니다.

## 기능을 목표에 맞추기

기능은 Claude가 모든 세션에서 보는 항상 켜진 컨텍스트부터 사용자나 Claude가 호출할 수 있는 온디맨드 기능, 특정 이벤트에서 실행되는 백그라운드 자동화까지 다양합니다. 아래 표는 사용 가능한 기능과 각 기능이 언제 적절한지 보여줍니다.

| 기능                                 | 수행 작업                           | 사용 시기                          | 예시                                                    |
| ---------------------------------- | ------------------------------- | ------------------------------ | ----------------------------------------------------- |
| **CLAUDE.md**                      | 모든 대화에서 로드되는 지속적인 컨텍스트          | 프로젝트 규칙, "항상 X를 수행" 규칙         | "npm이 아닌 pnpm을 사용하세요. 커밋하기 전에 테스트를 실행하세요."            |
| **Skill**                          | Claude가 사용할 수 있는 지침, 지식 및 워크플로우 | 재사용 가능한 콘텐츠, 참조 문서, 반복 가능한 작업  | `/deploy`는 배포 체크리스트를 실행합니다. 엔드포인트 패턴이 있는 API 문서 skill |
| **Subagent**                       | 요약된 결과를 반환하는 격리된 실행 컨텍스트        | 컨텍스트 격리, 병렬 작업, 특화된 워커         | 많은 파일을 읽지만 주요 결과만 반환하는 연구 작업                          |
| **[Agent teams](/ko/agent-teams)** | 여러 독립적인 Claude Code 세션 조정       | 병렬 연구, 새로운 기능 개발, 경쟁하는 가설로 디버깅 | 보안, 성능 및 테스트를 동시에 확인하는 검토자 생성                         |
| **MCP**                            | 외부 서비스에 연결                      | 외부 데이터 또는 작업                   | 데이터베이스 쿼리, Slack에 게시, 브라우저 제어                         |
| **Hook**                           | 이벤트에서 실행되는 결정론적 스크립트            | 예측 가능한 자동화, LLM 없음             | 모든 파일 편집 후 ESLint 실행                                  |

\*\*[Plugins](/ko/plugins)\*\*는 패키징 계층입니다. 플러그인은 skill, hook, subagent 및 MCP 서버를 단일 설치 가능한 단위로 번들합니다. 플러그인 skill은 네임스페이스됩니다(예: `/my-plugin:review`). 따라서 여러 플러그인이 공존할 수 있습니다. 여러 저장소에서 동일한 설정을 재사용하거나 \*\*[marketplace](/ko/plugin-marketplaces)\*\*를 통해 다른 사용자에게 배포하려는 경우 플러그인을 사용하세요.

### 유사한 기능 비교

일부 기능은 유사해 보일 수 있습니다. 구별하는 방법은 다음과 같습니다.

<Tabs>
  <Tab title="Skill vs Subagent">
    Skill과 subagent는 다양한 문제를 해결합니다.

    * **Skills**는 모든 컨텍스트에 로드할 수 있는 재사용 가능한 콘텐츠입니다.
    * **Subagents**는 주 대화와 별도로 실행되는 격리된 워커입니다.

    | 측면        | Skill                   | Subagent                         |
    | --------- | ----------------------- | -------------------------------- |
    | **정의**    | 재사용 가능한 지침, 지식 또는 워크플로우 | 자신의 컨텍스트를 가진 격리된 워커              |
    | **주요 이점** | 컨텍스트 간 콘텐츠 공유           | 컨텍스트 격리. 작업은 별도로 발생하고 요약만 반환됩니다. |
    | **최적 용도** | 참조 자료, 호출 가능한 워크플로우     | 많은 파일을 읽는 작업, 병렬 작업, 특화된 워커      |

    **Skill은 참조 또는 작업일 수 있습니다.** 참조 skill은 Claude가 세션 전체에서 사용하는 지식을 제공합니다(API 스타일 가이드처럼). 작업 skill은 Claude에게 특정 작업을 수행하도록 지시합니다(배포 워크플로우를 실행하는 `/deploy`처럼).

    **컨텍스트 격리가 필요하거나 컨텍스트 윈도우가 가득 찰 때 subagent를 사용하세요.** Subagent는 수십 개의 파일을 읽거나 광범위한 검색을 실행할 수 있지만, 주 대화는 요약만 받습니다. Subagent 작업이 주 컨텍스트를 소비하지 않으므로, 중간 작업이 표시되어야 할 필요가 없을 때도 유용합니다. 사용자 정의 subagent는 자신의 지침을 가질 수 있고 skill을 미리 로드할 수 있습니다.

    **결합할 수 있습니다.** Subagent는 특정 skill을 미리 로드할 수 있습니다(`skills:` 필드). Skill은 `context: fork`를 사용하여 격리된 컨텍스트에서 실행될 수 있습니다. 자세한 내용은 [Skills](/ko/skills)를 참조하세요.
  </Tab>

  <Tab title="CLAUDE.md vs Skill">
    둘 다 지침을 저장하지만 로드 방식과 목적이 다릅니다.

    | 측면               | CLAUDE.md          | Skill               |
    | ---------------- | ------------------ | ------------------- |
    | **로드**           | 모든 세션, 자동으로        | 온디맨드                |
    | **파일 포함 가능**     | 예, `@path` 가져오기 사용 | 예, `@path` 가져오기 사용  |
    | **워크플로우 트리거 가능** | 아니요                | 예, `/<name>` 사용     |
    | **최적 용도**        | "항상 X를 수행" 규칙      | 참조 자료, 호출 가능한 워크플로우 |

    **CLAUDE.md에 넣으세요.** Claude가 항상 알아야 할 경우: 코딩 규칙, 빌드 명령, 프로젝트 구조, "X를 하지 마세요" 규칙.

    **Skill에 넣으세요.** 참조 자료인 경우 Claude가 때때로 필요합니다(API 문서, 스타일 가이드) 또는 `/<name>`으로 트리거하는 워크플로우입니다(배포, 검토, 릴리스).

    **경험 법칙:** CLAUDE.md를 200줄 이하로 유지하세요. 증가하면 참조 콘텐츠를 skill로 이동하거나 [`.claude/rules/`](/ko/memory#organize-rules-with-clauderules) 파일로 분할하세요.
  </Tab>

  <Tab title="CLAUDE.md vs Rules vs Skills">
    세 가지 모두 지침을 저장하지만 로드 방식이 다릅니다.

    | 측면        | CLAUDE.md     | `.claude/rules/`        | Skill                |
    | --------- | ------------- | ----------------------- | -------------------- |
    | **로드**    | 모든 세션         | 모든 세션, 또는 일치하는 파일이 열릴 때 | 온디맨드, 호출되거나 관련이 있을 때 |
    | **범위**    | 전체 프로젝트       | 파일 경로로 범위 지정 가능         | 작업별                  |
    | **최적 용도** | 핵심 규칙 및 빌드 명령 | 언어별 또는 디렉토리별 가이드라인      | 참조 자료, 반복 가능한 워크플로우  |

    **CLAUDE.md를 사용하세요.** 모든 세션이 필요한 지침: 빌드 명령, 테스트 규칙, 프로젝트 아키텍처.

    **규칙을 사용하세요.** CLAUDE.md를 집중시키기 위해. [`paths` frontmatter](/ko/memory#path-specific-rules)가 있는 규칙은 Claude가 일치하는 파일로 작업할 때만 로드되어 컨텍스트를 절약합니다.

    **Skill을 사용하세요.** Claude가 때때로만 필요한 콘텐츠, API 문서 또는 `/<name>`으로 트리거하는 배포 체크리스트.
  </Tab>

  <Tab title="Subagent vs Agent team">
    둘 다 작업을 병렬화하지만 아키텍처가 다릅니다.

    * **Subagents**는 세션 내에서 실행되고 결과를 주 컨텍스트에 보고합니다.
    * **Agent teams**는 서로 통신하는 독립적인 Claude Code 세션입니다.

    | 측면        | Subagent                    | Agent team                |
    | --------- | --------------------------- | ------------------------- |
    | **컨텍스트**  | 자신의 컨텍스트 윈도우; 결과는 호출자에게 반환됨 | 자신의 컨텍스트 윈도우; 완전히 독립적     |
    | **통신**    | 주 에이전트에게만 결과 보고             | 팀원이 서로 직접 메시지             |
    | **조정**    | 주 에이전트가 모든 작업 관리            | 공유 작업 목록과 자체 조정           |
    | **최적 용도** | 결과만 중요한 집중된 작업              | 논의 및 협력이 필요한 복잡한 작업       |
    | **토큰 비용** | 낮음: 결과가 주 컨텍스트로 요약됨         | 높음: 각 팀원은 별도의 Claude 인스턴스 |

    **빠르고 집중된 워커가 필요할 때 subagent를 사용하세요.** 질문을 연구하고, 주장을 확인하고, 파일을 검토하세요. Subagent는 작업을 수행하고 요약을 반환합니다. 주 대화는 깔끔하게 유지됩니다.

    **팀원이 결과를 공유하고, 서로 도전하고, 독립적으로 조정해야 할 때 agent team을 사용하세요.** Agent team은 경쟁하는 가설이 있는 연구, 병렬 코드 검토, 각 팀원이 별도의 부분을 소유하는 새로운 기능 개발에 최적입니다.

    **전환점:** 병렬 subagent를 실행하지만 컨텍스트 제한에 도달하거나, subagent가 서로 통신해야 할 경우, agent team이 자연스러운 다음 단계입니다.

    <Note>
      Agent team은 실험적이며 기본적으로 비활성화됩니다. 설정 및 현재 제한 사항은 [agent teams](/ko/agent-teams)를 참조하세요.
    </Note>
  </Tab>

  <Tab title="MCP vs Skill">
    MCP는 Claude를 외부 서비스에 연결합니다. Skill은 Claude가 알아야 할 내용을 확장하며, 이러한 서비스를 효과적으로 사용하는 방법도 포함합니다.

    | 측면     | MCP                          | Skill                              |
    | ------ | ---------------------------- | ---------------------------------- |
    | **정의** | 외부 서비스 연결 프로토콜               | 지식, 워크플로우 및 참조 자료                  |
    | **제공** | 도구 및 데이터 접근                  | 지식, 워크플로우, 참조 자료                   |
    | **예시** | Slack 통합, 데이터베이스 쿼리, 브라우저 제어 | 코드 검토 체크리스트, 배포 워크플로우, API 스타일 가이드 |

    이들은 다양한 문제를 해결하며 함께 잘 작동합니다.

    **MCP**는 Claude에게 외부 시스템과 상호 작용할 수 있는 능력을 제공합니다. MCP 없이는 Claude가 데이터베이스를 쿼리하거나 Slack에 게시할 수 없습니다.

    **Skill**은 Claude에게 이러한 도구를 효과적으로 사용하는 방법에 대한 지식을 제공하며, `/<name>`으로 트리거할 수 있는 워크플로우도 포함합니다. Skill에는 팀의 데이터베이스 스키마 및 쿼리 패턴, 또는 팀의 메시지 형식 규칙이 있는 `/post-to-slack` 워크플로우가 포함될 수 있습니다.

    예: MCP 서버는 Claude를 데이터베이스에 연결합니다. Skill은 Claude에게 데이터 모델, 일반적인 쿼리 패턴, 다양한 작업에 사용할 테이블을 가르칩니다.
  </Tab>
</Tabs>

### 기능이 어떻게 계층화되는지 이해하기

기능은 여러 수준에서 정의될 수 있습니다. 사용자 전체, 프로젝트별, 플러그인을 통해, 또는 관리 정책을 통해. 또한 CLAUDE.md 파일을 하위 디렉토리에 중첩하거나 monorepo의 특정 패키지에 skill을 배치할 수 있습니다. 동일한 기능이 여러 수준에 존재할 때, 계층화 방식은 다음과 같습니다.

* **CLAUDE.md 파일**은 추가적입니다. 모든 수준이 동시에 Claude의 컨텍스트에 콘텐츠를 제공합니다. 작업 디렉토리 및 위의 파일은 시작 시 로드되고, 하위 디렉토리는 작업할 때 로드됩니다. 지침이 충돌할 때, Claude는 판단을 사용하여 조정하며, 더 구체적인 지침이 일반적으로 우선합니다. [CLAUDE.md 파일이 로드되는 방식](/ko/memory#how-claudemd-files-load)을 참조하세요.
* **Skill과 subagent**는 이름으로 재정의됩니다. 동일한 이름이 여러 수준에 존재할 때, 우선순위에 따라 하나의 정의가 승리합니다(skill의 경우 관리 > 사용자 > 프로젝트; subagent의 경우 관리 > CLI 플래그 > 프로젝트 > 사용자 > 플러그인). 플러그인 skill은 [네임스페이스됩니다](/ko/plugins#add-skills-to-your-plugin). 충돌을 피하기 위해. [Skill 검색](/ko/skills#where-skills-live) 및 [subagent 범위](/ko/sub-agents#choose-the-subagent-scope)를 참조하세요.
* **MCP 서버**는 이름으로 재정의됩니다. 로컬 > 프로젝트 > 사용자. [MCP 범위](/ko/mcp#scope-hierarchy-and-precedence)를 참조하세요.
* **Hooks**는 병합됩니다. 모든 등록된 hook은 소스에 관계없이 일치하는 이벤트에 대해 실행됩니다. [Hooks](/ko/hooks)를 참조하세요.

### 기능 결합하기

각 확장은 다양한 문제를 해결합니다. CLAUDE.md는 항상 켜진 컨텍스트를 처리하고, skill은 온디맨드 지식과 워크플로우를 처리하고, MCP는 외부 연결을 처리하고, subagent는 격리를 처리하고, hook은 자동화를 처리합니다. 실제 설정은 워크플로우에 따라 이들을 결합합니다.

예를 들어, CLAUDE.md를 프로젝트 규칙에 사용하고, skill을 배포 워크플로우에 사용하고, MCP를 데이터베이스에 연결하고, hook을 모든 편집 후 린팅을 실행하는 데 사용할 수 있습니다. 각 기능은 최적의 작업을 처리합니다.

| 패턴                    | 작동 방식                                                      | 예시                                                             |
| --------------------- | ---------------------------------------------------------- | -------------------------------------------------------------- |
| **Skill + MCP**       | MCP는 연결을 제공하고, skill은 Claude에게 잘 사용하는 방법을 가르칩니다.           | MCP는 데이터베이스에 연결하고, skill은 스키마 및 쿼리 패턴을 문서화합니다.                 |
| **Skill + Subagent**  | Skill은 병렬 작업을 위해 subagent를 생성합니다.                          | `/audit` skill은 보안, 성능 및 스타일 subagent를 시작하여 격리된 컨텍스트에서 작동합니다.  |
| **CLAUDE.md + Skill** | CLAUDE.md는 항상 켜진 규칙을 보유하고, skill은 온디맨드로 로드되는 참조 자료를 보유합니다. | CLAUDE.md는 "API 규칙을 따르세요"라고 말하고, skill은 전체 API 스타일 가이드를 포함합니다. |
| **Hook + MCP**        | Hook은 MCP를 통해 외부 작업을 트리거합니다.                               | 편집 후 hook은 Claude가 중요한 파일을 수정할 때 Slack 알림을 보냅니다.               |

## 컨텍스트 비용 이해하기

추가하는 모든 기능은 Claude의 컨텍스트를 소비합니다. 너무 많으면 컨텍스트 윈도우를 채울 수 있지만, 노이즈를 추가하여 Claude를 덜 효과적으로 만들 수도 있습니다. Skill이 올바르게 트리거되지 않거나 Claude가 규칙을 잃을 수 있습니다. 이러한 트레이드오프를 이해하면 효과적인 설정을 구축하는 데 도움이 됩니다.

### 기능별 컨텍스트 비용

각 기능은 다양한 로딩 전략과 컨텍스트 비용을 가집니다.

| 기능            | 로드 시기        | 로드되는 내용                | 컨텍스트 비용                     |
| ------------- | ------------ | ---------------------- | --------------------------- |
| **CLAUDE.md** | 세션 시작        | 전체 콘텐츠                 | 모든 요청                       |
| **Skill**     | 세션 시작 + 사용 시 | 시작 시 설명, 사용 시 전체 콘텐츠   | 낮음(모든 요청마다 설명)\*            |
| **MCP 서버**    | 세션 시작        | 모든 도구 정의 및 스키마         | 모든 요청                       |
| **Subagent**  | 생성 시         | 지정된 skill이 있는 신선한 컨텍스트 | 주 세션에서 격리됨                  |
| **Hooks**     | 트리거 시        | 없음(외부에서 실행)            | 0, hook이 추가 컨텍스트를 반환하지 않는 한 |

\*기본적으로 skill 설명은 세션 시작 시 로드되므로 Claude가 사용할 시기를 결정할 수 있습니다. Skill의 frontmatter에서 `disable-model-invocation: true`를 설정하여 수동으로 호출할 때까지 Claude에서 완전히 숨깁니다. 이는 skill의 컨텍스트 비용을 0으로 줄입니다.

### 기능이 어떻게 로드되는지 이해하기

각 기능은 세션의 다양한 지점에서 로드됩니다. 아래 탭은 각 기능이 언제 로드되고 무엇이 컨텍스트에 들어가는지 설명합니다.

<img src="https://mintcdn.com/claude-code/6yTCYq1p37ZB8-CQ/images/context-loading.svg?fit=max&auto=format&n=6yTCYq1p37ZB8-CQ&q=85&s=5a58ce953a35a2412892015e2ad6cb67" alt="컨텍스트 로딩: CLAUDE.md와 MCP는 세션 시작 시 로드되고 모든 요청에 유지됩니다. Skill은 시작 시 설명을 로드하고 호출 시 전체 콘텐츠를 로드합니다. Subagent는 격리된 컨텍스트를 받습니다. Hook은 외부에서 실행됩니다." width="720" height="410" data-path="images/context-loading.svg" />

<Tabs>
  <Tab title="CLAUDE.md">
    **시기:** 세션 시작

    **로드되는 내용:** 모든 CLAUDE.md 파일의 전체 콘텐츠(관리, 사용자 및 프로젝트 수준).

    **상속:** Claude는 작업 디렉토리에서 루트까지 CLAUDE.md 파일을 읽고, 해당 파일에 접근할 때 하위 디렉토리에서 중첩된 파일을 검색합니다. 자세한 내용은 [CLAUDE.md 파일이 로드되는 방식](/ko/memory#how-claudemd-files-load)을 참조하세요.

    <Tip>CLAUDE.md를 약 500줄 이하로 유지하세요. 참조 자료를 skill로 이동하면 온디맨드로 로드됩니다.</Tip>
  </Tab>

  <Tab title="Skills">
    Skill은 Claude의 도구 키트에 있는 추가 기능입니다. 참조 자료(API 스타일 가이드처럼) 또는 `/<name>`으로 트리거하는 호출 가능한 워크플로우(배포처럼)일 수 있습니다. Claude Code는 기본적으로 작동하는 `/simplify`, `/batch`, `/debug`와 같은 [번들 skill](/ko/skills#bundled-skills)과 함께 제공됩니다. 자신의 것을 만들 수도 있습니다. Claude는 적절할 때 skill을 사용하거나 직접 호출할 수 있습니다.

    **시기:** Skill의 구성에 따라 다릅니다. 기본적으로 설명은 세션 시작 시 로드되고 전체 콘텐츠는 사용 시 로드됩니다. 사용자 전용 skill(`disable-model-invocation: true`)의 경우, 호출할 때까지 아무것도 로드되지 않습니다.

    **로드되는 내용:** 모델 호출 가능 skill의 경우, Claude는 모든 요청에서 이름과 설명을 봅니다. `/<name>`으로 skill을 호출하거나 Claude가 자동으로 로드할 때, 전체 콘텐츠가 대화에 로드됩니다.

    **Claude가 skill을 선택하는 방식:** Claude는 작업을 skill 설명과 비교하여 관련성이 있는지 결정합니다. 설명이 모호하거나 겹치면, Claude가 잘못된 skill을 로드하거나 도움이 될 skill을 놓칠 수 있습니다. Claude에게 특정 skill을 사용하도록 지시하려면 `/<name>`으로 호출하세요. `disable-model-invocation: true`가 있는 Skill은 호출할 때까지 Claude에게 보이지 않습니다.

    **컨텍스트 비용:** 사용할 때까지 낮음. 사용자 전용 skill은 호출할 때까지 0 비용입니다.

    **Subagent에서:** Skill은 subagent에서 다르게 작동합니다. 온디맨드 로딩 대신, subagent에 전달된 skill은 시작 시 컨텍스트에 완전히 미리 로드됩니다. Subagent는 주 세션에서 skill을 상속하지 않습니다. 명시적으로 지정해야 합니다.

    <Tip>부작용이 있는 skill에 `disable-model-invocation: true`를 사용하세요. 이는 컨텍스트를 절약하고 오직 사용자만 트리거하도록 보장합니다.</Tip>
  </Tab>

  <Tab title="MCP servers">
    **시기:** 세션 시작.

    **로드되는 내용:** 연결된 서버의 모든 도구 정의 및 JSON 스키마.

    **컨텍스트 비용:** [도구 검색](/ko/mcp#scale-with-mcp-tool-search)(기본적으로 활성화)은 MCP 도구를 컨텍스트의 최대 10%까지 로드하고 나머지는 필요할 때까지 연기합니다.

    **신뢰성 참고:** MCP 연결은 세션 중간에 조용히 실패할 수 있습니다. 서버가 연결 해제되면 도구가 경고 없이 사라집니다. Claude가 이전에 접근할 수 있었던 MCP 도구를 사용하지 못하는 경우, `/mcp`로 연결을 확인하세요.

    <Tip>서버당 토큰 비용을 보려면 `/mcp`를 실행하세요. 적극적으로 사용하지 않는 서버를 연결 해제하세요.</Tip>
  </Tab>

  <Tab title="Subagents">
    **시기:** 온디맨드, 작업을 위해 사용자나 Claude가 생성할 때.

    **로드되는 내용:** 신선한, 격리된 컨텍스트 포함:

    * 시스템 프롬프트(캐시 효율성을 위해 부모와 공유)
    * 에이전트의 `skills:` 필드에 나열된 skill의 전체 콘텐츠
    * CLAUDE.md 및 git 상태(부모에서 상속)
    * 리드 에이전트가 프롬프트에서 전달하는 모든 컨텍스트

    **컨텍스트 비용:** 주 세션에서 격리됨. Subagent는 대화 기록이나 호출된 skill을 상속하지 않습니다.

    <Tip>전체 대화 컨텍스트가 필요하지 않은 작업에 subagent를 사용하세요. 격리는 주 세션이 부풀어지는 것을 방지합니다.</Tip>
  </Tab>

  <Tab title="Hooks">
    **시기:** 트리거 시. Hook은 도구 실행, 세션 경계, 프롬프트 제출, 권한 요청 및 압축과 같은 특정 라이프사이클 이벤트에서 실행됩니다. 전체 목록은 [Hooks](/ko/hooks)를 참조하세요.

    **로드되는 내용:** 기본적으로 없음. Hook은 외부 스크립트로 실행됩니다.

    **컨텍스트 비용:** 0, hook이 대화에 메시지로 추가되는 출력을 반환하지 않는 한.

    <Tip>Hook은 Claude의 컨텍스트에 영향을 주지 않아야 하는 부작용(린팅, 로깅)에 이상적입니다.</Tip>
  </Tab>
</Tabs>

## 더 알아보기

각 기능에는 설정 지침, 예시 및 구성 옵션이 있는 자신의 가이드가 있습니다.

<CardGroup cols={2}>
  <Card title="CLAUDE.md" icon="file-lines" href="/ko/memory">
    프로젝트 컨텍스트, 규칙 및 지침 저장
  </Card>

  <Card title="Skills" icon="brain" href="/ko/skills">
    Claude에게 도메인 전문성 및 재사용 가능한 워크플로우 제공
  </Card>

  <Card title="Subagents" icon="users" href="/ko/sub-agents">
    격리된 컨텍스트로 작업 오프로드
  </Card>

  <Card title="Agent teams" icon="network" href="/ko/agent-teams">
    병렬로 작동하는 여러 세션 조정
  </Card>

  <Card title="MCP" icon="plug" href="/ko/mcp">
    Claude를 외부 서비스에 연결
  </Card>

  <Card title="Hooks" icon="bolt" href="/ko/hooks-guide">
    Hook으로 워크플로우 자동화
  </Card>

  <Card title="Plugins" icon="puzzle-piece" href="/ko/plugins">
    기능 세트 번들 및 공유
  </Card>

  <Card title="Marketplaces" icon="store" href="/ko/plugin-marketplaces">
    플러그인 컬렉션 호스트 및 배포
  </Card>
</CardGroup>
