> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code 설정

> 전역 및 프로젝트 수준 설정과 환경 변수로 Claude Code를 구성합니다.

Claude Code는 사용자의 필요에 맞게 동작을 구성할 수 있는 다양한 설정을 제공합니다. 대화형 REPL을 사용할 때 `/config` 명령을 실행하여 Claude Code를 구성할 수 있으며, 이는 상태 정보를 보고 구성 옵션을 수정할 수 있는 탭 형식의 설정 인터페이스를 엽니다.

## 구성 범위

Claude Code는 **범위 시스템**을 사용하여 구성이 적용되는 위치와 공유 대상을 결정합니다. 범위를 이해하면 개인 사용, 팀 협업 또는 엔터프라이즈 배포를 위해 Claude Code를 구성하는 방법을 결정하는 데 도움이 됩니다.

### 사용 가능한 범위

| 범위          | 위치                                                        | 영향을 받는 대상     | 팀과 공유?           |
| :---------- | :-------------------------------------------------------- | :------------ | :--------------- |
| **Managed** | 서버 관리 설정, plist / 레지스트리 또는 시스템 수준 `managed-settings.json` | 머신의 모든 사용자    | 예 (IT에서 배포)      |
| **User**    | `~/.claude/` 디렉토리                                         | 모든 프로젝트에서 사용자 | 아니오              |
| **Project** | 저장소의 `.claude/`                                           | 이 저장소의 모든 협업자 | 예 (git에 커밋됨)     |
| **Local**   | `.claude/settings.local.json`                             | 이 저장소에서만 사용자  | 아니오 (gitignored) |

### 각 범위를 사용할 시기

**Managed 범위**는 다음을 위한 것입니다:

* 조직 전체에서 적용해야 하는 보안 정책
* 재정의할 수 없는 규정 준수 요구사항
* IT/DevOps에서 배포한 표준화된 구성

**User 범위**는 다음에 가장 적합합니다:

* 모든 곳에서 원하는 개인 설정 (테마, 편집기 설정)
* 모든 프로젝트에서 사용하는 도구 및 플러그인
* API 키 및 인증 (안전하게 저장됨)

**Project 범위**는 다음에 가장 적합합니다:

* 팀 공유 설정 (권한, hooks, MCP servers)
* 전체 팀이 가져야 할 플러그인
* 협업자 간 도구 표준화

**Local 범위**는 다음에 가장 적합합니다:

* 특정 프로젝트에 대한 개인 재정의
* 팀과 공유하기 전에 구성 테스트
* 다른 사용자에게는 작동하지 않을 머신 특정 설정

### 범위 상호작용 방식

동일한 설정이 여러 범위에서 구성되면 더 구체적인 범위가 우선합니다:

1. **Managed** (최상위) - 아무것도 재정의할 수 없음
2. **명령줄 인수** - 임시 세션 재정의
3. **Local** - 프로젝트 및 사용자 설정 재정의
4. **Project** - 사용자 설정 재정의
5. **User** (최하위) - 다른 것이 설정을 지정하지 않을 때 적용

예를 들어, 사용자 설정에서는 권한이 허용되지만 프로젝트 설정에서는 거부되면, 프로젝트 설정이 우선하고 권한이 차단됩니다.

### 범위를 사용하는 것

범위는 많은 Claude Code 기능에 적용됩니다:

| 기능              | 사용자 위치                    | 프로젝트 위치                            | Local 위치                      |
| :-------------- | :------------------------ | :--------------------------------- | :---------------------------- |
| **Settings**    | `~/.claude/settings.json` | `.claude/settings.json`            | `.claude/settings.local.json` |
| **Subagents**   | `~/.claude/agents/`       | `.claude/agents/`                  | —                             |
| **MCP servers** | `~/.claude.json`          | `.mcp.json`                        | `~/.claude.json` (프로젝트별)      |
| **Plugins**     | `~/.claude/settings.json` | `.claude/settings.json`            | `.claude/settings.local.json` |
| **CLAUDE.md**   | `~/.claude/CLAUDE.md`     | `CLAUDE.md` 또는 `.claude/CLAUDE.md` | —                             |

***

## 설정 파일

`settings.json` 파일은 계층적 설정을 통해 Claude Code를 구성하기 위한 공식 메커니즘입니다:

* **사용자 설정**은 `~/.claude/settings.json`에 정의되며 모든 프로젝트에 적용됩니다.
* **프로젝트 설정**은 프로젝트 디렉토리에 저장됩니다:
  * `.claude/settings.json` - 소스 제어에 체크인되고 팀과 공유되는 설정
  * `.claude/settings.local.json` - 체크인되지 않는 설정으로, 개인 설정 및 실험에 유용합니다. Claude Code는 생성될 때 `.claude/settings.local.json`을 무시하도록 git을 구성합니다.
* **Managed 설정**: 중앙 집중식 제어가 필요한 조직의 경우, Claude Code는 managed 설정을 위한 여러 전달 메커니즘을 지원합니다. 모두 동일한 JSON 형식을 사용하며 사용자 또는 프로젝트 설정으로 재정의할 수 없습니다:

  * **서버 관리 설정**: Anthropic의 서버에서 Claude.ai 관리 콘솔을 통해 전달됩니다. [서버 관리 설정](/ko/server-managed-settings)을 참조하세요.
  * **MDM/OS 수준 정책**: macOS 및 Windows의 기본 장치 관리를 통해 전달됩니다:
    * macOS: `com.anthropic.claudecode` managed preferences domain (Jamf, Kandji 또는 기타 MDM 도구의 구성 프로필을 통해 배포)
    * Windows: `HKLM\SOFTWARE\Policies\ClaudeCode` 레지스트리 키와 JSON을 포함하는 `Settings` 값 (REG\_SZ 또는 REG\_EXPAND\_SZ) (그룹 정책 또는 Intune을 통해 배포)
    * Windows (사용자 수준): `HKCU\SOFTWARE\Policies\ClaudeCode` (최하위 정책 우선순위, 관리자 수준 소스가 없을 때만 사용)
  * **파일 기반**: `managed-settings.json` 및 `managed-mcp.json`이 시스템 디렉토리에 배포됩니다:
    * macOS: `/Library/Application Support/ClaudeCode/`
    * Linux 및 WSL: `/etc/claude-code/`
    * Windows: `C:\Program Files\ClaudeCode\`

  자세한 내용은 [managed 설정](/ko/permissions#managed-only-settings) 및 [Managed MCP 구성](/ko/mcp#managed-mcp-configuration)을 참조하세요.

  <Note>
    Managed 배포는 `strictKnownMarketplaces`를 사용하여 **플러그인 마켓플레이스 추가**를 제한할 수도 있습니다. 자세한 내용은 [Managed 마켓플레이스 제한](/ko/plugin-marketplaces#managed-marketplace-restrictions)을 참조하세요.
  </Note>
* **기타 구성**은 `~/.claude.json`에 저장됩니다. 이 파일에는 사용자의 설정 (테마, 알림 설정, 편집기 모드), OAuth 세션, 사용자 및 local 범위에 대한 [MCP server](/ko/mcp) 구성, 프로젝트별 상태 (허용된 도구, 신뢰 설정) 및 다양한 캐시가 포함됩니다. 프로젝트 범위 MCP 서버는 `.mcp.json`에 별도로 저장됩니다.

<Note>
  Claude Code는 자동으로 구성 파일의 타임스탬프가 지정된 백업을 생성하고 데이터 손실을 방지하기 위해 가장 최근의 5개 백업을 유지합니다.
</Note>

```JSON 예제 settings.json theme={null}
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test *)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  },
  "companyAnnouncements": [
    "Welcome to Acme Corp! Review our code guidelines at docs.acme.com",
    "Reminder: Code reviews required for all PRs",
    "New security policy in effect"
  ]
}
```

위의 예제에서 `$schema` 줄은 Claude Code 설정에 대한 [공식 JSON 스키마](https://json.schemastore.org/claude-code-settings.json)를 가리킵니다. 이를 `settings.json`에 추가하면 VS Code, Cursor 및 JSON 스키마 검증을 지원하는 다른 편집기에서 자동 완성 및 인라인 검증이 활성화됩니다.

### 사용 가능한 설정

`settings.json`은 여러 옵션을 지원합니다:

| 키                                 | 설명                                                                                                                                                                                                  | 예제                                                                      |
| :-------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------- |
| `apiKeyHelper`                    | `/bin/sh`에서 실행할 사용자 정의 스크립트로 인증 값을 생성합니다. 이 값은 모델 요청에 대해 `X-Api-Key` 및 `Authorization: Bearer` 헤더로 전송됩니다                                                                                            | `/bin/generate_temp_api_key.sh`                                         |
| `cleanupPeriodDays`               | 이 기간보다 오래 비활성 상태인 세션은 시작 시 삭제됩니다. `0`으로 설정하면 모든 세션이 즉시 삭제됩니다. (기본값: 30일)                                                                                                                            | `20`                                                                    |
| `companyAnnouncements`            | 시작 시 사용자에게 표시할 공지사항입니다. 여러 공지사항이 제공되면 무작위로 순환됩니다.                                                                                                                                                   | `["Welcome to Acme Corp! Review our code guidelines at docs.acme.com"]` |
| `env`                             | 모든 세션에 적용될 환경 변수                                                                                                                                                                                    | `{"FOO": "bar"}`                                                        |
| `attribution`                     | git 커밋 및 풀 요청에 대한 속성을 사용자 정의합니다. [속성 설정](#attribution-settings)을 참조하세요                                                                                                                              | `{"commit": "🤖 Generated with Claude Code", "pr": ""}`                 |
| `includeCoAuthoredBy`             | **더 이상 사용되지 않음**: 대신 `attribution`을 사용하세요. git 커밋 및 풀 요청에 `co-authored-by Claude` 바이라인을 포함할지 여부 (기본값: `true`)                                                                                       | `false`                                                                 |
| `includeGitInstructions`          | Claude의 시스템 프롬프트에 기본 제공 커밋 및 PR 워크플로우 지침을 포함합니다 (기본값: `true`). 예를 들어 자신의 git 워크플로우 skills을 사용할 때 이러한 지침을 제거하려면 `false`로 설정하세요. `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` 환경 변수가 설정되면 이 설정보다 우선합니다      | `false`                                                                 |
| `permissions`                     | 권한 구조는 아래 표를 참조하세요.                                                                                                                                                                                 |                                                                         |
| `hooks`                           | 라이프사이클 이벤트에서 실행할 사용자 정의 명령을 구성합니다. [hooks 문서](/ko/hooks)에서 형식을 참조하세요                                                                                                                                | [hooks](/ko/hooks) 참조                                                   |
| `disableAllHooks`                 | 모든 [hooks](/ko/hooks) 및 사용자 정의 [status line](/ko/statusline) 비활성화                                                                                                                                   | `true`                                                                  |
| `allowManagedHooksOnly`           | (Managed 설정만) 사용자, 프로젝트 및 플러그인 hooks 로드 방지. Managed hooks 및 SDK hooks만 허용합니다. [Hook 구성](#hook-configuration) 참조                                                                                     | `true`                                                                  |
| `allowedHttpHookUrls`             | HTTP hooks가 대상으로 할 수 있는 URL 패턴의 허용 목록입니다. `*`를 와일드카드로 지원합니다. 설정되면 일치하지 않는 URL을 가진 hooks는 차단됩니다. 정의되지 않음 = 제한 없음, 빈 배열 = 모든 HTTP hooks 차단. 배열은 설정 소스 전체에서 병합됩니다. [Hook 구성](#hook-configuration) 참조   | `["https://hooks.example.com/*"]`                                       |
| `httpHookAllowedEnvVars`          | HTTP hooks가 헤더에 보간할 수 있는 환경 변수 이름의 허용 목록입니다. 설정되면 각 hook의 유효한 `allowedEnvVars`는 이 목록과의 교집합입니다. 정의되지 않음 = 제한 없음. 배열은 설정 소스 전체에서 병합됩니다. [Hook 구성](#hook-configuration) 참조                             | `["MY_TOKEN", "HOOK_SECRET"]`                                           |
| `allowManagedPermissionRulesOnly` | (Managed 설정만) 사용자 및 프로젝트 설정이 `allow`, `ask` 또는 `deny` 권한 규칙을 정의하는 것을 방지합니다. Managed 설정의 규칙만 적용됩니다. [Managed 전용 설정](/ko/permissions#managed-only-settings) 참조                                        | `true`                                                                  |
| `allowManagedMcpServersOnly`      | (Managed 설정만) Managed 설정의 `allowedMcpServers`만 존중됩니다. `deniedMcpServers`는 여전히 모든 소스에서 병합됩니다. 사용자는 여전히 MCP 서버를 추가할 수 있지만 관리자 정의 허용 목록만 적용됩니다. [Managed MCP 구성](/ko/mcp#managed-mcp-configuration) 참조 | `true`                                                                  |
| `model`                           | Claude Code에 사용할 기본 모델을 재정의합니다                                                                                                                                                                      | `"claude-sonnet-4-6"`                                                   |
| `availableModels`                 | `/model`, `--model`, Config 도구 또는 `ANTHROPIC_MODEL`을 통해 사용자가 선택할 수 있는 모델을 제한합니다. 기본 옵션에는 영향을 주지 않습니다. [모델 선택 제한](/ko/model-config#restrict-model-selection) 참조                                      | `["sonnet", "haiku"]`                                                   |
| `modelOverrides`                  | Anthropic 모델 ID를 Bedrock 추론 프로필 ARN과 같은 공급자 특정 모델 ID로 매핑합니다. 각 모델 선택기 항목은 공급자 API를 호출할 때 매핑된 값을 사용합니다. [버전별 모델 ID 재정의](/ko/model-config#override-model-ids-per-version) 참조                          | `{"claude-opus-4-6": "arn:aws:bedrock:..."}`                            |
| `otelHeadersHelper`               | 동적 OpenTelemetry 헤더를 생성하는 스크립트입니다. 시작 시 및 주기적으로 실행됩니다 ([동적 헤더](/ko/monitoring-usage#dynamic-headers) 참조)                                                                                            | `/bin/generate_otel_headers.sh`                                         |
| `statusLine`                      | 컨텍스트를 표시하는 사용자 정의 상태 줄을 구성합니다. [`statusLine` 문서](/ko/statusline) 참조                                                                                                                                 | `{"type": "command", "command": "~/.claude/statusline.sh"}`             |
| `fileSuggestion`                  | `@` 파일 자동 완성을 위한 사용자 정의 스크립트를 구성합니다. [파일 제안 설정](#file-suggestion-settings) 참조                                                                                                                       | `{"type": "command", "command": "~/.claude/file-suggestion.sh"}`        |
| `respectGitignore`                | `@` 파일 선택기가 `.gitignore` 패턴을 존중할지 여부를 제어합니다. `true` (기본값)일 때 `.gitignore` 패턴과 일치하는 파일은 제안에서 제외됩니다                                                                                                   | `false`                                                                 |
| `outputStyle`                     | 시스템 프롬프트를 조정하는 출력 스타일을 구성합니다. [출력 스타일 문서](/ko/output-styles) 참조                                                                                                                                     | `"Explanatory"`                                                         |
| `forceLoginMethod`                | `claudeai`를 사용하여 Claude.ai 계정으로만 로그인을 제한하거나, `console`을 사용하여 Claude Console (API 사용 청구) 계정으로만 로그인을 제한합니다                                                                                            | `claudeai`                                                              |
| `forceLoginOrgUUID`               | 로그인 중에 자동으로 선택할 조직의 UUID를 지정하여 조직 선택 단계를 건너뜁니다. `forceLoginMethod`가 설정되어야 합니다                                                                                                                       | `"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"`                                |
| `enableAllProjectMcpServers`      | 프로젝트 `.mcp.json` 파일에 정의된 모든 MCP 서버를 자동으로 승인합니다                                                                                                                                                      | `true`                                                                  |
| `enabledMcpjsonServers`           | `.mcp.json` 파일에서 승인할 특정 MCP 서버 목록                                                                                                                                                                   | `["memory", "github"]`                                                  |
| `disabledMcpjsonServers`          | `.mcp.json` 파일에서 거부할 특정 MCP 서버 목록                                                                                                                                                                   | `["filesystem"]`                                                        |
| `allowedMcpServers`               | Managed 설정에서 설정되면 사용자가 구성할 수 있는 MCP 서버의 허용 목록입니다. 정의되지 않음 = 제한 없음, 빈 배열 = 잠금. 모든 범위에 적용됩니다. 거부 목록이 우선합니다. [Managed MCP 구성](/ko/mcp#managed-mcp-configuration) 참조                                    | `[{ "serverName": "github" }]`                                          |
| `deniedMcpServers`                | Managed 설정에서 설정되면 명시적으로 차단된 MCP 서버의 거부 목록입니다. Managed 서버를 포함한 모든 범위에 적용됩니다. 거부 목록이 허용 목록보다 우선합니다. [Managed MCP 구성](/ko/mcp#managed-mcp-configuration) 참조                                            | `[{ "serverName": "filesystem" }]`                                      |
| `strictKnownMarketplaces`         | Managed 설정에서 설정되면 사용자가 추가할 수 있는 플러그인 마켓플레이스의 허용 목록입니다. 정의되지 않음 = 제한 없음, 빈 배열 = 잠금. 마켓플레이스 추가에만 적용됩니다. [Managed 마켓플레이스 제한](/ko/plugin-marketplaces#managed-marketplace-restrictions) 참조              | `[{ "source": "github", "repo": "acme-corp/plugins" }]`                 |
| `blockedMarketplaces`             | (Managed 설정만) 마켓플레이스 소스의 차단 목록입니다. 차단된 소스는 다운로드 전에 확인되므로 파일 시스템에 닿지 않습니다. [Managed 마켓플레이스 제한](/ko/plugin-marketplaces#managed-marketplace-restrictions) 참조                                          | `[{ "source": "github", "repo": "untrusted/plugins" }]`                 |
| `pluginTrustMessage`              | (Managed 설정만) 설치 전에 표시되는 플러그인 신뢰 경고에 추가되는 사용자 정의 메시지입니다. 이를 사용하여 조직 특정 컨텍스트를 추가합니다. 예를 들어 내부 마켓플레이스의 플러그인이 검증되었음을 확인합니다.                                                                            | `"All plugins from our marketplace are approved by IT"`                 |
| `awsAuthRefresh`                  | `.aws` 디렉토리를 수정하는 사용자 정의 스크립트 ([고급 자격증명 구성](/ko/amazon-bedrock#advanced-credential-configuration) 참조)                                                                                               | `aws sso login --profile myprofile`                                     |
| `awsCredentialExport`             | AWS 자격증명이 포함된 JSON을 출력하는 사용자 정의 스크립트 ([고급 자격증명 구성](/ko/amazon-bedrock#advanced-credential-configuration) 참조)                                                                                        | `/bin/generate_aws_grant.sh`                                            |
| `alwaysThinkingEnabled`           | 모든 세션에 대해 기본적으로 [확장 사고](/ko/common-workflows#use-extended-thinking-thinking-mode)를 활성화합니다. 일반적으로 직접 편집하기보다는 `/config` 명령을 통해 구성됩니다                                                                  | `true`                                                                  |
| `plansDirectory`                  | 계획 파일이 저장되는 위치를 사용자 정의합니다. 경로는 프로젝트 루트에 상대적입니다. 기본값: `~/.claude/plans`                                                                                                                              | `"./plans"`                                                             |
| `showTurnDuration`                | 응답 후 턴 지속 시간 메시지를 표시합니다 (예: "Cooked for 1m 6s"). 이러한 메시지를 숨기려면 `false`로 설정하세요                                                                                                                       | `true`                                                                  |
| `spinnerVerbs`                    | 스피너 및 턴 지속 시간 메시지에 표시되는 작업 동사를 사용자 정의합니다. `mode`를 `"replace"`로 설정하여 동사만 사용하거나 `"append"`로 설정하여 기본값에 추가합니다                                                                                           | `{"mode": "append", "verbs": ["Pondering", "Crafting"]}`                |
| `language`                        | Claude의 선호 응답 언어를 구성합니다 (예: `"japanese"`, `"spanish"`, `"french"`). Claude는 기본적으로 이 언어로 응답합니다                                                                                                       | `"japanese"`                                                            |
| `autoUpdatesChannel`              | 업데이트를 따를 릴리스 채널입니다. 일반적으로 약 1주일 된 버전이고 주요 회귀가 있는 버전을 건너뛰는 `"stable"`을 사용하거나 가장 최근 릴리스인 `"latest"` (기본값)를 사용합니다                                                                                      | `"stable"`                                                              |
| `spinnerTipsEnabled`              | Claude가 작업 중일 때 스피너에 팁을 표시합니다. 팁을 비활성화하려면 `false`로 설정하세요 (기본값: `true`)                                                                                                                              | `false`                                                                 |
| `spinnerTipsOverride`             | 스피너 팁을 사용자 정의 문자열로 재정의합니다. `tips`: 팁 문자열 배열. `excludeDefault`: `true`이면 사용자 정의 팁만 표시하고, `false`이거나 없으면 사용자 정의 팁이 기본 제공 팁과 병합됩니다                                                                     | `{ "excludeDefault": true, "tips": ["Use our internal tool X"] }`       |
| `terminalProgressBarEnabled`      | Windows Terminal 및 iTerm2와 같은 지원되는 터미널에서 진행률을 표시하는 터미널 진행률 표시줄을 활성화합니다 (기본값: `true`)                                                                                                                | `false`                                                                 |
| `prefersReducedMotion`            | 접근성을 위해 UI 애니메이션 (스피너, shimmer, flash 효과) 감소 또는 비활성화                                                                                                                                                | `true`                                                                  |
| `fastModePerSessionOptIn`         | `true`일 때 빠른 모드는 세션 간에 지속되지 않습니다. 각 세션은 빠른 모드가 꺼진 상태로 시작되며 사용자가 `/fast`로 활성화해야 합니다. 사용자의 빠른 모드 설정은 여전히 저장됩니다. [세션별 옵트인 필요](/ko/fast-mode#require-per-session-opt-in) 참조                             | `true`                                                                  |
| `teammateMode`                    | [에이전트 팀](/ko/agent-teams) 팀원이 표시되는 방식: `auto` (tmux 또는 iTerm2에서 분할 창 선택, 그 외에는 in-process), `in-process` 또는 `tmux`. [에이전트 팀 설정](/ko/agent-teams#set-up-agent-teams) 참조                              | `"in-process"`                                                          |

### 권한 설정

| 키                              | 설명                                                                                                                                                                      | 예제                                                                     |
| :----------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `allow`                        | 도구 사용을 허용하는 권한 규칙 배열입니다. 패턴 매칭 세부사항은 아래 [권한 규칙 구문](#permission-rule-syntax)을 참조하세요                                                                                      | `[ "Bash(git diff *)" ]`                                               |
| `ask`                          | 도구 사용 시 확인을 요청하는 권한 규칙 배열입니다. 패턴 매칭 세부사항은 아래 [권한 규칙 구문](#permission-rule-syntax)을 참조하세요                                                                                 | `[ "Bash(git push *)" ]`                                               |
| `deny`                         | 도구 사용을 거부하는 권한 규칙 배열입니다. 이를 사용하여 Claude Code 액세스에서 민감한 파일을 제외합니다. [권한 규칙 구문](#permission-rule-syntax) 및 [Bash 권한 제한](/ko/permissions#tool-specific-permission-rules) 참조 | `[ "WebFetch", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)" ]` |
| `additionalDirectories`        | Claude가 액세스할 수 있는 추가 [작업 디렉토리](/ko/permissions#working-directories)                                                                                                     | `[ "../docs/" ]`                                                       |
| `defaultMode`                  | Claude Code를 열 때 기본 [권한 모드](/ko/permissions#permission-modes)                                                                                                           | `"acceptEdits"`                                                        |
| `disableBypassPermissionsMode` | `bypassPermissions` 모드가 활성화되는 것을 방지하려면 `"disable"`로 설정합니다. 이는 `--dangerously-skip-permissions` 명령줄 플래그를 비활성화합니다. [managed 설정](/ko/permissions#managed-only-settings) 참조 | `"disable"`                                                            |

### 권한 규칙 구문

권한 규칙은 `Tool` 또는 `Tool(specifier)` 형식을 따릅니다. 규칙은 순서대로 평가됩니다: 먼저 거부 규칙, 그 다음 요청, 그 다음 허용. 첫 번째 일치 규칙이 우선합니다.

빠른 예제:

| 규칙                             | 효과                          |
| :----------------------------- | :-------------------------- |
| `Bash`                         | 모든 Bash 명령과 일치              |
| `Bash(npm run *)`              | `npm run`으로 시작하는 명령과 일치     |
| `Read(./.env)`                 | `.env` 파일 읽기와 일치            |
| `WebFetch(domain:example.com)` | example.com으로의 fetch 요청과 일치 |

와일드카드 동작, Read, Edit, WebFetch, MCP 및 Agent 규칙에 대한 도구 특정 패턴, Bash 패턴의 보안 제한을 포함한 완전한 규칙 구문 참조는 [권한 규칙 구문](/ko/permissions#permission-rule-syntax)을 참조하세요.

### Sandbox 설정

고급 샌드박싱 동작을 구성합니다. 샌드박싱은 bash 명령을 파일 시스템 및 네트워크에서 격리합니다. 자세한 내용은 [Sandboxing](/ko/sandboxing)을 참조하세요.

| 키                                 | 설명                                                                                                                                                                                                                                        | 예제                              |
| :-------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------ |
| `enabled`                         | bash 샌드박싱 활성화 (macOS, Linux 및 WSL2). 기본값: false                                                                                                                                                                                           | `true`                          |
| `autoAllowBashIfSandboxed`        | 샌드박싱되면 bash 명령 자동 승인. 기본값: true                                                                                                                                                                                                           | `true`                          |
| `excludedCommands`                | 샌드박스 외부에서 실행해야 할 명령                                                                                                                                                                                                                       | `["git", "docker"]`             |
| `allowUnsandboxedCommands`        | `dangerouslyDisableSandbox` 매개변수를 통해 샌드박스 외부에서 명령을 실행하도록 허용합니다. `false`로 설정하면 `dangerouslyDisableSandbox` 이스케이프 해치가 완전히 비활성화되고 모든 명령은 샌드박싱되거나 `excludedCommands`에 있어야 합니다. 엄격한 샌드박싱을 요구하는 엔터프라이즈 정책에 유용합니다. 기본값: true                     | `false`                         |
| `filesystem.allowWrite`           | 샌드박싱된 명령이 쓸 수 있는 추가 경로입니다. 배열은 모든 설정 범위에서 병합됩니다: 사용자, 프로젝트 및 managed 경로가 결합되고 대체되지 않습니다. `Edit(...)` 허용 권한 규칙의 경로와도 병합됩니다. [경로 접두사](#sandbox-path-prefixes) 아래를 참조하세요.                                                                    | `["//tmp/build", "~/.kube"]`    |
| `filesystem.denyWrite`            | 샌드박싱된 명령이 쓸 수 없는 경로입니다. 배열은 모든 설정 범위에서 병합됩니다. `Edit(...)` 거부 권한 규칙의 경로와도 병합됩니다.                                                                                                                                                           | `["//etc", "//usr/local/bin"]`  |
| `filesystem.denyRead`             | 샌드박싱된 명령이 읽을 수 없는 경로입니다. 배열은 모든 설정 범위에서 병합됩니다. `Read(...)` 거부 권한 규칙의 경로와도 병합됩니다.                                                                                                                                                          | `["~/.aws/credentials"]`        |
| `network.allowUnixSockets`        | 샌드박스에서 액세스 가능한 Unix 소켓 경로 (SSH 에이전트 등)                                                                                                                                                                                                    | `["~/.ssh/agent-socket"]`       |
| `network.allowAllUnixSockets`     | 샌드박스에서 모든 Unix 소켓 연결을 허용합니다. 기본값: false                                                                                                                                                                                                   | `true`                          |
| `network.allowLocalBinding`       | localhost 포트에 바인딩 허용 (macOS만). 기본값: false                                                                                                                                                                                                 | `true`                          |
| `network.allowedDomains`          | 아웃바운드 네트워크 트래픽을 허용할 도메인 배열입니다. 와일드카드를 지원합니다 (예: `*.example.com`).                                                                                                                                                                         | `["github.com", "*.npmjs.org"]` |
| `network.allowManagedDomainsOnly` | (Managed 설정만) Managed 설정의 `allowedDomains` 및 `WebFetch(domain:...)` 허용 규칙만 존중됩니다. 사용자, 프로젝트 및 local 설정의 도메인은 무시됩니다. 허용되지 않은 도메인은 사용자에게 메시지를 표시하지 않고 자동으로 차단됩니다. 거부된 도메인은 여전히 모든 소스에서 존중됩니다. 기본값: false                                    | `true`                          |
| `network.httpProxyPort`           | 자신의 프록시를 가져오려는 경우 사용할 HTTP 프록시 포트입니다. 지정하지 않으면 Claude가 자신의 프록시를 실행합니다.                                                                                                                                                                    | `8080`                          |
| `network.socksProxyPort`          | 자신의 프록시를 가져오려는 경우 사용할 SOCKS5 프록시 포트입니다. 지정하지 않으면 Claude가 자신의 프록시를 실행합니다.                                                                                                                                                                  | `8081`                          |
| `enableWeakerNestedSandbox`       | 권한이 없는 Docker 환경에서 더 약한 샌드박스를 활성화합니다 (Linux 및 WSL2만). **보안을 감소시킵니다.** 기본값: false                                                                                                                                                          | `true`                          |
| `enableWeakerNetworkIsolation`    | (macOS만) 샌드박스에서 시스템 TLS 신뢰 서비스 (`com.apple.trustd.agent`)에 대한 액세스를 허용합니다. `httpProxyPort`와 함께 MITM 프록시 및 사용자 정의 CA를 사용할 때 `gh`, `gcloud` 및 `terraform`과 같은 Go 기반 도구가 TLS 인증서를 확인하는 데 필요합니다. **보안을 감소시킵니다** 잠재적 데이터 유출 경로를 열어서. 기본값: false | `true`                          |

#### Sandbox 경로 접두사

`filesystem.allowWrite`, `filesystem.denyWrite` 및 `filesystem.denyRead`의 경로는 다음 접두사를 지원합니다:

| 접두사            | 의미                     | 예제                                 |
| :------------- | :--------------------- | :--------------------------------- |
| `//`           | 파일 시스템 루트의 절대 경로       | `//tmp/build`는 `/tmp/build`가 됨     |
| `~/`           | 홈 디렉토리에 상대적            | `~/.kube`는 `$HOME/.kube`가 됨        |
| `/`            | 설정 파일의 디렉토리에 상대적       | `/build`는 `$SETTINGS_DIR/build`가 됨 |
| `./` 또는 접두사 없음 | 상대 경로 (샌드박스 런타임에서 해석됨) | `./output`                         |

**구성 예제:**

```json  theme={null}
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker"],
    "filesystem": {
      "allowWrite": ["//tmp/build", "~/.kube"],
      "denyRead": ["~/.aws/credentials"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org", "registry.yarnpkg.com"],
      "allowUnixSockets": [
        "/var/run/docker.sock"
      ],
      "allowLocalBinding": true
    }
  }
}
```

**파일 시스템 및 네트워크 제한**은 함께 병합되는 두 가지 방식으로 구성할 수 있습니다:

* **`sandbox.filesystem` 설정** (위에 표시됨): OS 수준 샌드박스 경계에서 경로를 제어합니다. 이러한 제한은 Claude의 파일 도구뿐만 아니라 모든 서브프로세스 명령 (예: `kubectl`, `terraform`, `npm`)에 적용됩니다.
* **권한 규칙**: `Edit` 허용/거부 규칙을 사용하여 Claude의 파일 도구 액세스를 제어하고, `Read` 거부 규칙을 사용하여 읽기를 차단하고, `WebFetch` 허용/거부 규칙을 사용하여 네트워크 도메인을 제어합니다. 이러한 규칙의 경로도 샌드박스 구성에 병합됩니다.

### 속성 설정

Claude Code는 git 커밋 및 풀 요청에 속성을 추가합니다. 이들은 별도로 구성됩니다:

* 커밋은 기본적으로 [git trailers](https://git-scm.com/docs/git-interpret-trailers) (예: `Co-Authored-By`)를 사용하며 사용자 정의하거나 비활성화할 수 있습니다
* 풀 요청 설명은 일반 텍스트입니다

| 키        | 설명                                                 |
| :------- | :------------------------------------------------- |
| `commit` | git 커밋에 대한 속성 (모든 trailers 포함). 빈 문자열은 커밋 속성을 숨깁니다 |
| `pr`     | 풀 요청 설명에 대한 속성입니다. 빈 문자열은 풀 요청 속성을 숨깁니다            |

**기본 커밋 속성:**

```text  theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**기본 풀 요청 속성:**

```text  theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**예제:**

```json  theme={null}
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": ""
  }
}
```

<Note>
  `attribution` 설정은 더 이상 사용되지 않는 `includeCoAuthoredBy` 설정보다 우선합니다. 모든 속성을 숨기려면 `commit` 및 `pr`을 빈 문자열로 설정하세요.
</Note>

### 파일 제안 설정

`@` 파일 경로 자동 완성을 위한 사용자 정의 명령을 구성합니다. 기본 제공 파일 제안은 빠른 파일 시스템 순회를 사용하지만 대규모 모노레포는 사전 구축된 파일 인덱스 또는 사용자 정의 도구와 같은 프로젝트 특정 인덱싱의 이점을 얻을 수 있습니다.

```json  theme={null}
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

명령은 `CLAUDE_PROJECT_DIR`을 포함한 [hooks](/ko/hooks)와 동일한 환경 변수로 실행됩니다. stdin을 통해 `query` 필드가 있는 JSON을 수신합니다:

```json  theme={null}
{"query": "src/comp"}
```

stdout에 줄 바꿈으로 구분된 파일 경로를 출력합니다 (현재 15개로 제한됨):

```text  theme={null}
src/components/Button.tsx
src/components/Modal.tsx
src/components/Form.tsx
```

**예제:**

```bash  theme={null}
#!/bin/bash
query=$(cat | jq -r '.query')
your-repo-file-index --query "$query" | head -20
```

### Hook 구성

이러한 설정은 실행할 수 있는 hooks와 HTTP hooks가 액세스할 수 있는 것을 제어합니다. `allowManagedHooksOnly` 설정은 [managed 설정](#settings-files)에서만 구성할 수 있습니다. URL 및 env var 허용 목록은 모든 설정 수준에서 설정할 수 있으며 소스 전체에서 병합됩니다.

**`allowManagedHooksOnly`가 `true`일 때의 동작:**

* Managed hooks 및 SDK hooks가 로드됨
* 사용자 hooks, 프로젝트 hooks 및 플러그인 hooks가 차단됨

**HTTP hook URL 제한:**

HTTP hooks가 대상으로 할 수 있는 URL을 제한합니다. 일치를 위해 `*`를 와일드카드로 지원합니다. 배열이 정의되면 일치하지 않는 URL을 대상으로 하는 HTTP hooks는 자동으로 차단됩니다.

```json  theme={null}
{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}
```

**HTTP hook 환경 변수 제한:**

HTTP hooks가 헤더 값에 보간할 수 있는 환경 변수 이름을 제한합니다. 각 hook의 유효한 `allowedEnvVars`는 자신의 목록과 이 설정의 교집합입니다.

```json  theme={null}
{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}
```

### 설정 우선순위

설정은 우선순위 순서대로 적용됩니다. 최상위에서 최하위로:

1. **Managed 설정** ([서버 관리](/ko/server-managed-settings), [MDM/OS 수준 정책](#configuration-scopes) 또는 [managed 설정](/ko/settings#settings-files))
   * IT에서 서버 전달, MDM 구성 프로필, 레지스트리 정책 또는 managed 설정 파일을 통해 배포한 정책
   * 명령줄 인수를 포함한 다른 수준으로 재정의할 수 없음
   * Managed 계층 내에서 우선순위: 서버 관리 > MDM/OS 수준 정책 > `managed-settings.json` > HKCU 레지스트리 (Windows만). 하나의 managed 소스만 사용되며 소스는 병합되지 않습니다.

2. **명령줄 인수**
   * 특정 세션에 대한 임시 재정의

3. **Local 프로젝트 설정** (`.claude/settings.local.json`)
   * 개인 프로젝트 특정 설정

4. **공유 프로젝트 설정** (`.claude/settings.json`)
   * 소스 제어의 팀 공유 프로젝트 설정

5. **사용자 설정** (`~/.claude/settings.json`)
   * 개인 전역 설정

이 계층 구조는 조직 정책이 항상 적용되면서도 팀과 개인이 자신의 경험을 사용자 정의할 수 있도록 보장합니다.

예를 들어, 사용자 설정에서 `Bash(npm run *)`을 허용하지만 프로젝트의 공유 설정에서 거부하면, 프로젝트 설정이 우선하고 명령이 차단됩니다.

<Note>
  **배열 설정은 범위 전체에서 병합됩니다.** 동일한 배열 값 설정 (예: `sandbox.filesystem.allowWrite` 또는 `permissions.allow`)이 여러 범위에 나타나면 배열은 **연결되고 중복 제거되며** 대체되지 않습니다. 이는 낮은 우선순위 범위가 높은 우선순위 범위에서 설정한 항목을 재정의하지 않고 항목을 추가할 수 있음을 의미합니다. 예를 들어, managed 설정이 `allowWrite`를 `["//opt/company-tools"]`로 설정하고 사용자가 `["~/.kube"]`를 추가하면 두 경로 모두 최종 구성에 포함됩니다.
</Note>

### 활성 설정 확인

Claude Code 내에서 `/status`를 실행하여 활성 설정 소스와 출처를 확인합니다. 출력은 각 구성 계층 (managed, user, project)과 `Enterprise managed settings (remote)`, `Enterprise managed settings (plist)`, `Enterprise managed settings (HKLM)` 또는 `Enterprise managed settings (file)`과 같은 출처를 표시합니다. 설정 파일에 오류가 있으면 `/status`는 문제를 보고하여 수정할 수 있습니다.

### 구성 시스템의 핵심 사항

* **메모리 파일 (`CLAUDE.md`)**: Claude가 시작 시 로드하는 지침 및 컨텍스트를 포함합니다
* **설정 파일 (JSON)**: 권한, 환경 변수 및 도구 동작을 구성합니다
* **Skills**: `/skill-name`으로 호출하거나 Claude가 자동으로 로드할 수 있는 사용자 정의 프롬프트
* **MCP servers**: 추가 도구 및 통합으로 Claude Code를 확장합니다
* **우선순위**: 높은 수준 구성 (Managed)이 낮은 수준 (User/Project)을 재정의합니다
* **상속**: 설정은 병합되며 더 구체적인 설정이 더 광범위한 설정을 추가하거나 재정의합니다

### 시스템 프롬프트

Claude Code의 내부 시스템 프롬프트는 게시되지 않습니다. 사용자 정의 지침을 추가하려면 `CLAUDE.md` 파일 또는 `--append-system-prompt` 플래그를 사용하세요.

### 민감한 파일 제외

API 키, 비밀 및 환경 파일과 같은 민감한 정보가 포함된 파일에서 Claude Code가 액세스하는 것을 방지하려면 `.claude/settings.json` 파일에서 `permissions.deny` 설정을 사용하세요:

```json  theme={null}
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Read(./build)"
    ]
  }
}
```

이는 더 이상 사용되지 않는 `ignorePatterns` 구성을 대체합니다. 이러한 패턴과 일치하는 파일은 파일 검색 및 검색 결과에서 제외되며 이러한 파일에 대한 읽기 작업이 거부됩니다.

## Subagent 구성

Claude Code는 사용자 및 프로젝트 수준에서 구성할 수 있는 사용자 정의 AI subagents를 지원합니다. 이러한 subagents는 YAML frontmatter가 있는 Markdown 파일로 저장됩니다:

* **사용자 subagents**: `~/.claude/agents/` - 모든 프로젝트에서 사용 가능
* **프로젝트 subagents**: `.claude/agents/` - 프로젝트에 특정이며 팀과 공유할 수 있음

Subagent 파일은 사용자 정의 프롬프트 및 도구 권한이 있는 특화된 AI 어시스턴트를 정의합니다. [subagents 문서](/ko/sub-agents)에서 subagents를 만들고 사용하는 방법에 대해 자세히 알아보세요.

## 플러그인 구성

Claude Code는 skills, agents, hooks 및 MCP servers로 기능을 확장할 수 있는 플러그인 시스템을 지원합니다. 플러그인은 마켓플레이스를 통해 배포되며 사용자 및 저장소 수준에서 구성할 수 있습니다.

### 플러그인 설정

`settings.json`의 플러그인 관련 설정:

```json  theme={null}
{
  "enabledPlugins": {
    "formatter@acme-tools": true,
    "deployer@acme-tools": true,
    "analyzer@security-plugins": false
  },
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": "github",
      "repo": "acme-corp/claude-plugins"
    }
  }
}
```

#### `enabledPlugins`

활성화된 플러그인을 제어합니다. 형식: `"plugin-name@marketplace-name": true/false`

**범위**:

* **사용자 설정** (`~/.claude/settings.json`): 개인 플러그인 설정
* **프로젝트 설정** (`.claude/settings.json`): 팀과 공유되는 프로젝트 특정 플러그인
* **Local 설정** (`.claude/settings.local.json`): 머신별 재정의 (커밋되지 않음)

**예제**:

```json  theme={null}
{
  "enabledPlugins": {
    "code-formatter@team-tools": true,
    "deployment-tools@team-tools": true,
    "experimental-features@personal": false
  }
}
```

#### `extraKnownMarketplaces`

저장소에서 사용 가능하게 해야 할 추가 마켓플레이스를 정의합니다. 일반적으로 팀 멤버가 필요한 플러그인 소스에 액세스할 수 있도록 저장소 수준 설정에서 사용됩니다.

**저장소에 `extraKnownMarketplaces`가 포함되면**:

1. 팀 멤버는 폴더를 신뢰할 때 마켓플레이스를 설치하라는 메시지를 받습니다
2. 그 다음 팀 멤버는 해당 마켓플레이스에서 플러그인을 설치하라는 메시지를 받습니다
3. 사용자는 원하지 않는 마켓플레이스 또는 플러그인을 건너뛸 수 있습니다 (사용자 설정에 저장됨)
4. 설치는 신뢰 경계를 존중하고 명시적 동의가 필요합니다

**예제**:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    },
    "security-plugins": {
      "source": {
        "source": "git",
        "url": "https://git.example.com/security/plugins.git"
      }
    }
  }
}
```

**마켓플레이스 소스 유형**:

* `github`: GitHub 저장소 (`repo` 사용)
* `git`: 모든 git URL (`url` 사용)
* `directory`: 로컬 파일 시스템 경로 (`path` 사용, 개발 전용)
* `hostPattern`: 마켓플레이스 호스트와 일치하는 정규식 패턴 (`hostPattern` 사용)

#### `strictKnownMarketplaces`

**Managed 설정만**: 사용자가 추가할 수 있는 플러그인 마켓플레이스를 제어합니다. 이 설정은 [managed 설정](/ko/settings#settings-files)에서만 구성할 수 있으며 관리자에게 마켓플레이스 소스에 대한 엄격한 제어를 제공합니다.

**Managed 설정 파일 위치**:

* **macOS**: `/Library/Application Support/ClaudeCode/managed-settings.json`
* **Linux 및 WSL**: `/etc/claude-code/managed-settings.json`
* **Windows**: `C:\Program Files\ClaudeCode\managed-settings.json`

**주요 특성**:

* Managed 설정 (`managed-settings.json`)에서만 사용 가능
* 사용자 또는 프로젝트 설정으로 재정의할 수 없음 (최상위 우선순위)
* 네트워크/파일 시스템 작업 전에 적용됨 (차단된 소스는 실행되지 않음)
* `hostPattern`을 제외한 소스 사양에 대해 정확한 일치를 사용합니다. `hostPattern`은 정규식 일치를 사용합니다

**허용 목록 동작**:

* `undefined` (기본값): 제한 없음 - 사용자는 모든 마켓플레이스를 추가할 수 있음
* 빈 배열 `[]`: 완전 잠금 - 사용자는 새 마켓플레이스를 추가할 수 없음
* 소스 목록: 사용자는 정확히 일치하는 마켓플레이스만 추가할 수 있음

**지원되는 모든 소스 유형**:

허용 목록은 7가지 마켓플레이스 소스 유형을 지원합니다. 대부분의 소스는 정확한 일치를 사용하는 반면 `hostPattern`은 마켓플레이스 호스트에 대해 정규식 일치를 사용합니다.

1. **GitHub 저장소**:

```json  theme={null}
{ "source": "github", "repo": "acme-corp/approved-plugins" }
{ "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main", "path": "marketplace" }
```

필드: `repo` (필수), `ref` (선택: 분기/태그/SHA), `path` (선택: 하위 디렉토리)

2. **Git 저장소**:

```json  theme={null}
{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git" }
{ "source": "git", "url": "https://bitbucket.org/acme-corp/plugins.git", "ref": "production" }
{ "source": "git", "url": "ssh://git@git.example.com/plugins.git", "ref": "v3.1", "path": "approved" }
```

필드: `url` (필수), `ref` (선택: 분기/태그/SHA), `path` (선택: 하위 디렉토리)

3. **URL 기반 마켓플레이스**:

```json  theme={null}
{ "source": "url", "url": "https://plugins.example.com/marketplace.json" }
{ "source": "url", "url": "https://cdn.example.com/marketplace.json", "headers": { "Authorization": "Bearer ${TOKEN}" } }
```

필드: `url` (필수), `headers` (선택: 인증된 액세스를 위한 HTTP 헤더)

<Note>
  URL 기반 마켓플레이스는 `marketplace.json` 파일만 다운로드합니다. 서버에서 플러그인 파일을 다운로드하지 않습니다. URL 기반 마켓플레이스의 플러그인은 상대 경로가 아닌 외부 소스 (GitHub, npm 또는 git URL)를 사용해야 합니다. 상대 경로가 있는 플러그인의 경우 대신 Git 기반 마켓플레이스를 사용하세요. [문제 해결](/ko/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces)에서 자세한 내용을 참조하세요.
</Note>

4. **NPM 패키지**:

```json  theme={null}
{ "source": "npm", "package": "@acme-corp/claude-plugins" }
{ "source": "npm", "package": "@acme-corp/approved-marketplace" }
```

필드: `package` (필수, 범위가 지정된 패키지 지원)

5. **파일 경로**:

```json  theme={null}
{ "source": "file", "path": "/usr/local/share/claude/acme-marketplace.json" }
{ "source": "file", "path": "/opt/acme-corp/plugins/marketplace.json" }
```

필드: `path` (필수: marketplace.json 파일의 절대 경로)

6. **디렉토리 경로**:

```json  theme={null}
{ "source": "directory", "path": "/usr/local/share/claude/acme-plugins" }
{ "source": "directory", "path": "/opt/acme-corp/approved-marketplaces" }
```

필드: `path` (필수: `.claude-plugin/marketplace.json`을 포함하는 디렉토리의 절대 경로)

7. **호스트 패턴 일치**:

```json  theme={null}
{ "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" }
{ "source": "hostPattern", "hostPattern": "^gitlab\\.internal\\.example\\.com$" }
```

필드: `hostPattern` (필수: 마켓플레이스 호스트와 일치하는 정규식 패턴)

각 저장소를 열거하지 않고 특정 호스트의 모든 마켓플레이스를 허용하려면 호스트 패턴 일치를 사용하세요. 이는 개발자가 자신의 마켓플레이스를 만드는 내부 GitHub Enterprise 또는 GitLab 서버가 있는 조직에 유용합니다.

소스 유형별 호스트 추출:

* `github`: 항상 `github.com`에 대해 일치
* `git`: URL에서 호스트명 추출 (HTTPS 및 SSH 형식 지원)
* `url`: URL에서 호스트명 추출
* `npm`, `file`, `directory`: 호스트 패턴 일치에 지원되지 않음

**구성 예제**:

예제: 특정 마켓플레이스만 허용:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    },
    {
      "source": "npm",
      "package": "@acme-corp/compliance-plugins"
    }
  ]
}
```

예제 - 모든 마켓플레이스 추가 비활성화:

```json  theme={null}
{
  "strictKnownMarketplaces": []
}
```

예제: 내부 git 서버의 모든 마켓플레이스 허용:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

**정확한 일치 요구사항**:

마켓플레이스 소스는 사용자의 추가가 허용되려면 **정확히** 일치해야 합니다. Git 기반 소스 (`github` 및 `git`)의 경우 모든 선택적 필드를 포함합니다:

* `repo` 또는 `url`이 정확히 일치해야 함
* `ref` 필드가 정확히 일치해야 함 (또는 둘 다 정의되지 않음)
* `path` 필드가 정확히 일치해야 함 (또는 둘 다 정의되지 않음)

일치하지 **않는** 소스의 예:

```json  theme={null}
// 이들은 다른 소스입니다:
{ "source": "github", "repo": "acme-corp/plugins" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main" }

// 이것도 다릅니다:
{ "source": "github", "repo": "acme-corp/plugins", "path": "marketplace" }
{ "source": "github", "repo": "acme-corp/plugins" }
```

**`extraKnownMarketplaces`와의 비교**:

| 측면         | `strictKnownMarketplaces` | `extraKnownMarketplaces` |
| ---------- | ------------------------- | ------------------------ |
| **목적**     | 조직 정책 적용                  | 팀 편의                     |
| **설정 파일**  | `managed-settings.json`만  | 모든 설정 파일                 |
| **동작**     | 허용 목록에 없는 추가 차단           | 누락된 마켓플레이스 자동 설치         |
| **적용 시기**  | 네트워크/파일 시스템 작업 전          | 사용자 신뢰 프롬프트 후            |
| **재정의 가능** | 아니오 (최상위 우선순위)            | 예 (높은 우선순위 설정으로)         |
| **소스 형식**  | 직접 소스 객체                  | 중첩된 소스가 있는 명명된 마켓플레이스    |
| **사용 사례**  | 규정 준수, 보안 제한              | 온보딩, 표준화                 |

**형식 차이**:

`strictKnownMarketplaces`는 직접 소스 객체를 사용합니다:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ]
}
```

`extraKnownMarketplaces`는 명명된 마켓플레이스가 필요합니다:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

**중요 참고사항**:

* 제한은 네트워크 요청 또는 파일 시스템 작업 전에 확인됨
* 차단되면 사용자는 소스가 managed 정책으로 차단되었음을 나타내는 명확한 오류 메시지를 봅니다
* 제한은 새 마켓플레이스 추가에만 적용되며 이전에 설치된 마켓플레이스는 계속 액세스 가능합니다
* Managed 설정은 최상위 우선순위를 가지며 재정의할 수 없습니다

[Managed 마켓플레이스 제한](/ko/plugin-marketplaces#managed-marketplace-restrictions)에서 사용자 대면 문서를 참조하세요.

### 플러그인 관리

`/plugin` 명령을 사용하여 플러그인을 대화형으로 관리합니다:

* 마켓플레이스에서 사용 가능한 플러그인 찾아보기
* 플러그인 설치/제거
* 플러그인 활성화/비활성화
* 플러그인 세부사항 보기 (제공되는 명령, agents, hooks)
* 마켓플레이스 추가/제거

[플러그인 문서](/ko/plugins)에서 플러그인 시스템에 대해 자세히 알아보세요.

## 환경 변수

Claude Code는 동작을 제어하기 위해 다음 환경 변수를 지원합니다:

<Note>
  모든 환경 변수는 [`settings.json`](#available-settings)에서도 구성할 수 있습니다. 이는 각 세션에 대해 환경 변수를 자동으로 설정하거나 전체 팀 또는 조직에 대해 환경 변수 집합을 배포하는 방법으로 유용합니다.
</Note>

| 변수                                             | 목적                                                                                                                                                                                                                                                                                                                                                       |     |
| :--------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- |
| `ANTHROPIC_API_KEY`                            | API 키로 `X-Api-Key` 헤더로 전송됨, 일반적으로 Claude SDK용 (대화형 사용의 경우 `/login` 실행)                                                                                                                                                                                                                                                                                   |     |
| `ANTHROPIC_AUTH_TOKEN`                         | `Authorization` 헤더의 사용자 정의 값 (여기서 설정한 값은 `Bearer ` 접두사가 붙음)                                                                                                                                                                                                                                                                                              |     |
| `ANTHROPIC_CUSTOM_HEADERS`                     | 요청에 추가할 사용자 정의 헤더 (`Name: Value` 형식, 여러 헤더의 경우 줄 바꿈으로 구분)                                                                                                                                                                                                                                                                                                |     |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`                | [모델 구성](/ko/model-config#environment-variables) 참조                                                                                                                                                                                                                                                                                                       |     |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`                 | [모델 구성](/ko/model-config#environment-variables) 참조                                                                                                                                                                                                                                                                                                       |     |
| `ANTHROPIC_DEFAULT_SONNET_MODEL`               | [모델 구성](/ko/model-config#environment-variables) 참조                                                                                                                                                                                                                                                                                                       |     |
| `ANTHROPIC_FOUNDRY_API_KEY`                    | Microsoft Foundry 인증을 위한 API 키 ([Microsoft Foundry](/ko/microsoft-foundry) 참조)                                                                                                                                                                                                                                                                           |     |
| `ANTHROPIC_FOUNDRY_BASE_URL`                   | Foundry 리소스의 전체 기본 URL (예: `https://my-resource.services.ai.azure.com/anthropic`). `ANTHROPIC_FOUNDRY_RESOURCE`의 대안 ([Microsoft Foundry](/ko/microsoft-foundry) 참조)                                                                                                                                                                                      |     |
| `ANTHROPIC_FOUNDRY_RESOURCE`                   | Foundry 리소스 이름 (예: `my-resource`). `ANTHROPIC_FOUNDRY_BASE_URL`이 설정되지 않은 경우 필수 ([Microsoft Foundry](/ko/microsoft-foundry) 참조)                                                                                                                                                                                                                           |     |
| `ANTHROPIC_MODEL`                              | 사용할 모델 설정의 이름 ([모델 구성](/ko/model-config#environment-variables) 참조)                                                                                                                                                                                                                                                                                       |     |
| `ANTHROPIC_SMALL_FAST_MODEL`                   | \[더 이상 사용되지 않음] 백그라운드 작업을 위한 [Haiku 클래스 모델](/ko/costs)의 이름                                                                                                                                                                                                                                                                                               |     |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION`        | Bedrock을 사용할 때 Haiku 클래스 모델의 AWS 지역 재정의                                                                                                                                                                                                                                                                                                                  |     |
| `AWS_BEARER_TOKEN_BEDROCK`                     | Bedrock API 인증을 위한 API 키 ([Bedrock API 키](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/) 참조)                                                                                                                                                                                                     |     |
| `BASH_DEFAULT_TIMEOUT_MS`                      | 장시간 실행되는 bash 명령의 기본 타임아웃                                                                                                                                                                                                                                                                                                                                |     |
| `BASH_MAX_OUTPUT_LENGTH`                       | bash 출력이 중간 잘림되기 전의 최대 문자 수                                                                                                                                                                                                                                                                                                                              |     |
| `BASH_MAX_TIMEOUT_MS`                          | 모델이 장시간 실행되는 bash 명령에 대해 설정할 수 있는 최대 타임아웃                                                                                                                                                                                                                                                                                                                |     |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`              | 자동 압축이 트리거되는 컨텍스트 용량의 백분율 (1-100)을 설정합니다. 기본적으로 자동 압축은 약 95% 용량에서 트리거됩니다. 더 빨리 압축하려면 `50`과 같은 낮은 값을 사용하세요. 기본 임계값보다 높은 값은 효과가 없습니다. 주 대화 및 subagents에 적용됩니다. 이 백분율은 [status line](/ko/statusline)에서 사용 가능한 `context_window.used_percentage` 필드와 일치합니다                                                                                                    |     |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR`     | 각 Bash 명령 후 원래 작업 디렉토리로 돌아갑니다                                                                                                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_ACCOUNT_UUID`                     | 인증된 사용자의 계정 UUID입니다. SDK 호출자가 계정 정보를 동기적으로 제공하여 초기 원격 분석 이벤트가 계정 메타데이터를 갖지 않는 경쟁 조건을 피하는 데 사용됩니다. `CLAUDE_CODE_USER_EMAIL` 및 `CLAUDE_CODE_ORGANIZATION_UUID`도 설정되어야 합니다                                                                                                                                                                                  |     |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | `--add-dir`로 지정된 디렉토리에서 CLAUDE.md 파일을 로드하려면 `1`로 설정합니다. 기본적으로 추가 디렉토리는 메모리 파일을 로드하지 않습니다                                                                                                                                                                                                                                                                 | `1` |
| `CLAUDE_CODE_API_KEY_HELPER_TTL_MS`            | 자격증명을 새로 고쳐야 하는 간격 (밀리초) (`apiKeyHelper` 사용 시)                                                                                                                                                                                                                                                                                                           |     |
| `CLAUDE_CODE_CLIENT_CERT`                      | mTLS 인증을 위한 클라이언트 인증서 파일의 경로                                                                                                                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_CLIENT_KEY`                       | mTLS 인증을 위한 클라이언트 개인 키 파일의 경로                                                                                                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE`            | 암호화된 CLAUDE\_CODE\_CLIENT\_KEY의 암호 (선택사항)                                                                                                                                                                                                                                                                                                                |     |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT`               | [1M 컨텍스트 윈도우](/ko/model-config#extended-context) 지원을 비활성화하려면 `1`로 설정합니다. 설정되면 1M 모델 변형은 모델 선택기에서 사용할 수 없습니다. 규정 준수 요구사항이 있는 엔터프라이즈 환경에 유용합니다                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING`        | Opus 4.6 및 Sonnet 4.6에 대해 [적응형 추론](/ko/model-config#adjust-effort-level)을 비활성화하려면 `1`로 설정합니다. 비활성화되면 이러한 모델은 `MAX_THINKING_TOKENS`로 제어되는 고정 사고 예산으로 돌아갑니다                                                                                                                                                                                                |     |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY`              | [자동 메모리](/ko/memory#auto-memory)를 비활성화하려면 `1`로 설정합니다. 점진적 롤아웃 중에 자동 메모리를 강제로 켜려면 `0`으로 설정합니다. 비활성화되면 Claude는 자동 메모리 파일을 생성하거나 로드하지 않습니다                                                                                                                                                                                                                  |     |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS`         | Claude의 시스템 프롬프트에서 기본 제공 커밋 및 PR 워크플로우 지침을 제거하려면 `1`로 설정합니다. 자신의 git 워크플로우 skills을 사용할 때 유용합니다. 설정되면 [`includeGitInstructions`](#available-settings) 설정보다 우선합니다                                                                                                                                                                                          |     |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`         | 모든 백그라운드 작업 기능을 비활성화하려면 `1`로 설정합니다. Bash 및 subagent 도구의 `run_in_background` 매개변수, 자동 백그라운드 처리 및 Ctrl+B 단축키 포함                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_DISABLE_CRON`                     | [예약된 작업](/ko/scheduled-tasks)을 비활성화하려면 `1`로 설정합니다. `/loop` skill 및 cron 도구를 사용할 수 없게 되고 이미 예약된 작업은 중지되며, 세션 중에 이미 실행 중인 작업도 포함됩니다                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`       | Anthropic API 특정 `anthropic-beta` 헤더를 비활성화하려면 `1`로 설정합니다. LLM 게이트웨이와 함께 타사 공급자를 사용할 때 "Unexpected value(s) for the `anthropic-beta` header"와 같은 문제가 발생하는 경우 사용하세요                                                                                                                                                                                        |     |
| `CLAUDE_CODE_DISABLE_FAST_MODE`                | [빠른 모드](/ko/fast-mode)를 비활성화하려면 `1`로 설정합니다                                                                                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY`          | "Claude가 어떻게 하고 있나요?" 세션 품질 설문조사를 비활성화하려면 `1`로 설정합니다. 타사 공급자를 사용하거나 원격 분석이 비활성화되면 자동으로 비활성화됩니다. [세션 품질 설문조사](/ko/data-usage#session-quality-surveys) 참조                                                                                                                                                                                                  |     |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`     | `DISABLE_AUTOUPDATER`, `DISABLE_BUG_COMMAND`, `DISABLE_ERROR_REPORTING` 및 `DISABLE_TELEMETRY` 설정과 동일                                                                                                                                                                                                                                                     |     |
| `CLAUDE_CODE_DISABLE_TERMINAL_TITLE`           | 대화 컨텍스트를 기반으로 자동 터미널 제목 업데이트를 비활성화하려면 `1`로 설정합니다                                                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_CODE_EFFORT_LEVEL`                     | 지원되는 모델의 노력 수준을 설정합니다. 값: `low`, `medium`, `high`. 낮은 노력은 더 빠르고 저렴하며, 높은 노력은 더 깊은 추론을 제공합니다. Opus 4.6 및 Sonnet 4.6에서 지원됩니다. [노력 수준 조정](/ko/model-config#adjust-effort-level) 참조                                                                                                                                                                          |     |
| `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION`         | 프롬프트 제안을 비활성화하려면 `false`로 설정합니다 (`/config`의 "프롬프트 제안" 토글). 이들은 Claude가 응답한 후 프롬프트 입력에 나타나는 회색으로 표시된 예측입니다. [프롬프트 제안](/ko/interactive-mode#prompt-suggestions) 참조                                                                                                                                                                                         |     |
| `CLAUDE_CODE_ENABLE_TASKS`                     | 이전 TODO 목록으로 임시로 되돌리려면 `false`로 설정합니다. 기본값: `true`. [작업 목록](/ko/interactive-mode#task-list) 참조                                                                                                                                                                                                                                                           |     |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                 | OpenTelemetry 데이터 수집을 메트릭 및 로깅에 대해 활성화하려면 `1`로 설정합니다. OTel 내보내기를 구성하기 전에 필요합니다. [모니터링](/ko/monitoring-usage) 참조                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY`            | 쿼리 루프가 유휴 상태가 된 후 자동으로 종료되기 전에 대기할 시간 (밀리초)입니다. 자동화된 워크플로우 및 SDK 모드를 사용하는 스크립트에 유용합니다                                                                                                                                                                                                                                                                    |     |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`         | [에이전트 팀](/ko/agent-teams)을 활성화하려면 `1`로 설정합니다. 에이전트 팀은 실험적이며 기본적으로 비활성화됩니다                                                                                                                                                                                                                                                                                |     |
| `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS`      | 파일 읽기의 기본 토큰 제한을 재정의합니다. 전체 파일을 읽어야 할 때 유용합니다                                                                                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_HIDE_ACCOUNT_INFO`                | Claude Code UI에서 이메일 주소 및 조직 이름을 숨기려면 `1`로 설정합니다. 스트리밍 또는 녹화할 때 유용합니다                                                                                                                                                                                                                                                                                    |     |
| `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`            | IDE 확장 자동 설치 건너뛰기                                                                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS`                | 대부분의 요청에 대한 최대 출력 토큰 수를 설정합니다. 기본값: 32,000. 최대값: 64,000. 이 값을 증가시키면 [자동 압축](/ko/costs#reduce-token-usage)이 트리거되기 전에 사용 가능한 유효 컨텍스트 윈도우가 감소합니다.                                                                                                                                                                                                           |     |
| `CLAUDE_CODE_ORGANIZATION_UUID`                | 인증된 사용자의 조직 UUID입니다. SDK 호출자가 계정 정보를 동기적으로 제공하는 데 사용됩니다. `CLAUDE_CODE_ACCOUNT_UUID` 및 `CLAUDE_CODE_USER_EMAIL`도 설정되어야 합니다                                                                                                                                                                                                                                |     |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`  | 동적 OpenTelemetry 헤더를 새로 고치는 간격 (밀리초) (기본값: 1740000 / 29분). [동적 헤더](/ko/monitoring-usage#dynamic-headers) 참조                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_PLAN_MODE_REQUIRED`               | [에이전트 팀](/ko/agent-teams) 팀원이 계획 승인을 요구할 때 자동으로 `true`로 설정됩니다. 읽기 전용: Claude Code가 팀원을 생성할 때 설정됩니다. [팀원에 대한 계획 승인 필요](/ko/agent-teams#require-plan-approval-for-teammates) 참조                                                                                                                                                                            |     |
| `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`            | 플러그인을 설치하거나 업데이트할 때 git 작업의 타임아웃 (밀리초) (기본값: 120000). 대규모 저장소 또는 느린 네트워크 연결의 경우 이 값을 증가시키세요. [Git 작업 시간 초과](/ko/plugin-marketplaces#git-operations-time-out) 참조                                                                                                                                                                                          |     |
| `CLAUDE_CODE_PROXY_RESOLVES_HOSTS`             | 프록시가 호출자 대신 DNS 해석을 수행하도록 허용하려면 `true`로 설정합니다. 프록시가 호스트명 해석을 처리해야 하는 환경에서 옵트인합니다                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_CODE_SHELL`                            | 자동 셸 감지를 재정의합니다. 로그인 셸이 선호하는 작업 셸과 다를 때 유용합니다 (예: `bash` vs `zsh`)                                                                                                                                                                                                                                                                                       |     |
| `CLAUDE_CODE_SHELL_PREFIX`                     | 모든 bash 명령을 래핑할 명령 접두사 (예: 로깅 또는 감사용). 예: `/path/to/logger.sh`는 `/path/to/logger.sh <command>`를 실행합니다                                                                                                                                                                                                                                                    |     |
| `CLAUDE_CODE_SIMPLE`                           | 최소 시스템 프롬프트 및 Bash, 파일 읽기 및 파일 편집 도구만으로 실행하려면 `1`로 설정합니다. MCP 도구, 첨부 파일, hooks 및 CLAUDE.md 파일을 비활성화합니다                                                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_SKIP_BEDROCK_AUTH`                | Bedrock에 대한 AWS 인증을 건너뜁니다 (예: LLM 게이트웨이를 사용할 때)                                                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_SKIP_FOUNDRY_AUTH`                | Microsoft Foundry에 대한 Azure 인증을 건너뜁니다 (예: LLM 게이트웨이를 사용할 때)                                                                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_SKIP_VERTEX_AUTH`                 | Vertex에 대한 Google 인증을 건너뜁니다 (예: LLM 게이트웨이를 사용할 때)                                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_SUBAGENT_MODEL`                   | [모델 구성](/ko/model-config) 참조                                                                                                                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_TASK_LIST_ID`                     | 세션 간에 작업 목록을 공유합니다. 여러 Claude Code 인스턴스에서 동일한 ID를 설정하여 공유 작업 목록을 조정합니다. [작업 목록](/ko/interactive-mode#task-list) 참조                                                                                                                                                                                                                                       |     |
| `CLAUDE_CODE_TEAM_NAME`                        | 이 팀원이 속한 에이전트 팀의 이름입니다. [에이전트 팀](/ko/agent-teams) 멤버에서 자동으로 설정됩니다                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_TMPDIR`                           | 내부 임시 파일에 사용할 임시 디렉토리를 재정의합니다. Claude Code는 이 경로에 `/claude/`를 추가합니다. 기본값: Unix/macOS에서 `/tmp`, Windows에서 `os.tmpdir()`                                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_USER_EMAIL`                       | 인증된 사용자의 이메일 주소입니다. SDK 호출자가 계정 정보를 동기적으로 제공하는 데 사용됩니다. `CLAUDE_CODE_ACCOUNT_UUID` 및 `CLAUDE_CODE_ORGANIZATION_UUID`도 설정되어야 합니다                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_USE_BEDROCK`                      | [Bedrock](/ko/amazon-bedrock) 사용                                                                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_CODE_USE_FOUNDRY`                      | [Microsoft Foundry](/ko/microsoft-foundry) 사용                                                                                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_USE_VERTEX`                       | [Vertex](/ko/google-vertex-ai) 사용                                                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CONFIG_DIR`                            | Claude Code가 구성 및 데이터 파일을 저장하는 위치를 사용자 정의합니다                                                                                                                                                                                                                                                                                                             |     |
| `DISABLE_AUTOUPDATER`                          | 자동 업데이트를 비활성화하려면 `1`로 설정합니다.                                                                                                                                                                                                                                                                                                                             |     |
| `DISABLE_BUG_COMMAND`                          | `/bug` 명령을 비활성화하려면 `1`로 설정합니다                                                                                                                                                                                                                                                                                                                            |     |
| `DISABLE_COST_WARNINGS`                        | 비용 경고 메시지를 비활성화하려면 `1`로 설정합니다                                                                                                                                                                                                                                                                                                                            |     |
| `DISABLE_ERROR_REPORTING`                      | Sentry 오류 보고를 거부하려면 `1`로 설정합니다                                                                                                                                                                                                                                                                                                                           |     |
| `DISABLE_INSTALLATION_CHECKS`                  | 설치 경고를 비활성화하려면 `1`로 설정합니다. 설치 위치를 수동으로 관리할 때만 사용하세요. 표준 설치의 문제를 숨길 수 있습니다                                                                                                                                                                                                                                                                                |     |
| `DISABLE_NON_ESSENTIAL_MODEL_CALLS`            | 맛 텍스트와 같은 중요하지 않은 경로에 대한 모델 호출을 비활성화하려면 `1`로 설정합니다                                                                                                                                                                                                                                                                                                       |     |
| `DISABLE_PROMPT_CACHING`                       | 모든 모델에 대해 prompt caching을 비활성화하려면 `1`로 설정합니다 (모델별 설정보다 우선)                                                                                                                                                                                                                                                                                               |     |
| `DISABLE_PROMPT_CACHING_HAIKU`                 | Haiku 모델에 대해 prompt caching을 비활성화하려면 `1`로 설정합니다                                                                                                                                                                                                                                                                                                          |     |
| `DISABLE_PROMPT_CACHING_OPUS`                  | Opus 모델에 대해 prompt caching을 비활성화하려면 `1`로 설정합니다                                                                                                                                                                                                                                                                                                           |     |
| `DISABLE_PROMPT_CACHING_SONNET`                | Sonnet 모델에 대해 prompt caching을 비활성화하려면 `1`로 설정합니다                                                                                                                                                                                                                                                                                                         |     |
| `DISABLE_TELEMETRY`                            | Statsig 원격 분석을 거부하려면 `1`로 설정합니다 (Statsig 이벤트는 코드, 파일 경로 또는 bash 명령과 같은 사용자 데이터를 포함하지 않음)                                                                                                                                                                                                                                                                 |     |
| `ENABLE_CLAUDEAI_MCP_SERVERS`                  | Claude Code에서 [claude.ai MCP servers](/ko/mcp#use-mcp-servers-from-claudeai)를 비활성화하려면 `false`로 설정합니다. 로그인한 사용자에 대해 기본적으로 활성화됨                                                                                                                                                                                                                            |     |
| `ENABLE_TOOL_SEARCH`                           | [MCP 도구 검색](/ko/mcp#scale-with-mcp-tool-search)을 제어합니다. 값: `auto` (기본값, 10% 컨텍스트에서 활성화), `auto:N` (사용자 정의 임계값, 예: 5%의 경우 `auto:5`), `true` (항상 켜짐), `false` (비활성화)                                                                                                                                                                                       |     |
| `FORCE_AUTOUPDATE_PLUGINS`                     | 주 자동 업데이터가 `DISABLE_AUTOUPDATER`를 통해 비활성화된 경우에도 플러그인 자동 업데이트를 강제하려면 `true`로 설정합니다                                                                                                                                                                                                                                                                        |     |
| `HTTP_PROXY`                                   | 네트워크 연결을 위한 HTTP 프록시 서버를 지정합니다                                                                                                                                                                                                                                                                                                                           |     |
| `HTTPS_PROXY`                                  | 네트워크 연결을 위한 HTTPS 프록시 서버를 지정합니다                                                                                                                                                                                                                                                                                                                          |     |
| `IS_DEMO`                                      | 데모 모드를 활성화하려면 `true`로 설정합니다: UI에서 이메일 및 조직을 숨기고, 온보딩을 건너뛰고, 내부 명령을 숨깁니다. 스트리밍 또는 녹화 세션에 유용합니다                                                                                                                                                                                                                                                            |     |
| `MAX_MCP_OUTPUT_TOKENS`                        | MCP 도구 응답에서 허용되는 최대 토큰 수입니다. Claude Code는 출력이 10,000 토큰을 초과할 때 경고를 표시합니다 (기본값: 25000)                                                                                                                                                                                                                                                                    |     |
| `MAX_THINKING_TOKENS`                          | [확장 사고](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) 토큰 예산을 재정의합니다. 사고는 기본적으로 최대 예산 (31,999 토큰)에서 활성화됩니다. 예산을 제한하려면 (예: `MAX_THINKING_TOKENS=10000`) 또는 사고를 완전히 비활성화하려면 (`MAX_THINKING_TOKENS=0`) 사용하세요. Opus 4.6의 경우 사고 깊이는 대신 [노력 수준](/ko/model-config#adjust-effort-level)으로 제어되며 `0`으로 설정하여 사고를 비활성화하지 않는 한 이 변수는 무시됩니다. |     |
| `MCP_CLIENT_SECRET`                            | [사전 구성된 자격증명](/ko/mcp#use-pre-configured-oauth-credentials)이 필요한 MCP 서버에 대한 OAuth 클라이언트 비밀입니다. MCP 서버를 `--client-secret`으로 추가할 때 대화형 프롬프트를 피합니다                                                                                                                                                                                                          |     |
| `MCP_OAUTH_CALLBACK_PORT`                      | [사전 구성된 자격증명](/ko/mcp#use-pre-configured-oauth-credentials)으로 MCP 서버를 추가할 때 `--callback-port`의 대안으로 OAuth 리디렉션 콜백의 고정 포트                                                                                                                                                                                                                                 |     |
| `MCP_TIMEOUT`                                  | MCP 서버 시작의 타임아웃 (밀리초)                                                                                                                                                                                                                                                                                                                                    |     |
| `MCP_TOOL_TIMEOUT`                             | MCP 도구 실행의 타임아웃 (밀리초)                                                                                                                                                                                                                                                                                                                                    |     |
| `NO_PROXY`                                     | 프록시를 우회하여 직접 발급될 요청의 도메인 및 IP 목록                                                                                                                                                                                                                                                                                                                         |     |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET`               | [Skill 도구](/ko/skills#control-who-invokes-a-skill)에 표시되는 skill 메타데이터의 문자 예산을 재정의합니다. 예산은 컨텍스트 윈도우의 2%에서 동적으로 확장되며 16,000 문자의 폴백이 있습니다. 이전 버전과의 호환성을 위해 레거시 이름 유지                                                                                                                                                                                         |     |
| `USE_BUILTIN_RIPGREP`                          | Claude Code에 포함된 `rg` 대신 시스템 설치 `rg`를 사용하려면 `0`으로 설정합니다                                                                                                                                                                                                                                                                                                  |     |
| `VERTEX_REGION_CLAUDE_3_5_HAIKU`               | Vertex AI를 사용할 때 Claude 3.5 Haiku의 지역 재정의                                                                                                                                                                                                                                                                                                                |     |
| `VERTEX_REGION_CLAUDE_3_7_SONNET`              | Vertex AI를 사용할 때 Claude 3.7 Sonnet의 지역 재정의                                                                                                                                                                                                                                                                                                               |     |
| `VERTEX_REGION_CLAUDE_4_0_OPUS`                | Vertex AI를 사용할 때 Claude 4.0 Opus의 지역 재정의                                                                                                                                                                                                                                                                                                                 |     |
| `VERTEX_REGION_CLAUDE_4_0_SONNET`              | Vertex AI를 사용할 때 Claude 4.0 Sonnet의 지역 재정의                                                                                                                                                                                                                                                                                                               |     |
| `VERTEX_REGION_CLAUDE_4_1_OPUS`                | Vertex AI를 사용할 때 Claude 4.1 Opus의 지역 재정의                                                                                                                                                                                                                                                                                                                 |     |

## Claude가 사용할 수 있는 도구

Claude Code는 코드베이스를 이해하고 수정하는 데 도움이 되는 강력한 도구 집합에 액세스할 수 있습니다:

| 도구                       | 설명                                                                                                                                                                                                       | 권한 필요 |
| :----------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---- |
| **Agent**                | 작업을 처리하기 위해 자신의 컨텍스트 윈도우가 있는 [subagent](/ko/sub-agents)를 생성합니다                                                                                                                                           | 아니오   |
| **AskUserQuestion**      | 요구사항을 수집하거나 모호함을 명확히 하기 위해 객관식 질문을 합니다                                                                                                                                                                   | 아니오   |
| **Bash**                 | 환경에서 셸 명령을 실행합니다. [Bash 도구 동작](#bash-tool-behavior) 참조                                                                                                                                                   | 예     |
| **CronCreate**           | 현재 세션 내에서 반복 또는 일회성 프롬프트를 예약합니다 (Claude가 종료되면 사라짐). [예약된 작업](/ko/scheduled-tasks) 참조                                                                                                                     | 아니오   |
| **CronDelete**           | ID로 예약된 작업을 취소합니다                                                                                                                                                                                        | 아니오   |
| **CronList**             | 세션의 모든 예약된 작업을 나열합니다                                                                                                                                                                                     | 아니오   |
| **Edit**                 | 특정 파일에 대한 대상 편집을 수행합니다                                                                                                                                                                                   | 예     |
| **EnterPlanMode**        | 코딩 전에 접근 방식을 설계하기 위해 계획 모드로 전환합니다                                                                                                                                                                        | 아니오   |
| **EnterWorktree**        | 격리된 [git worktree](/ko/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees)를 생성하고 전환합니다                                                                                                | 아니오   |
| **ExitPlanMode**         | 승인을 위해 계획을 제시하고 계획 모드를 종료합니다                                                                                                                                                                             | 예     |
| **ExitWorktree**         | worktree 세션을 종료하고 원래 디렉토리로 돌아갑니다                                                                                                                                                                         | 아니오   |
| **Glob**                 | 패턴 매칭을 기반으로 파일을 찾습니다                                                                                                                                                                                     | 아니오   |
| **Grep**                 | 파일 내용에서 패턴을 검색합니다                                                                                                                                                                                        | 아니오   |
| **ListMcpResourcesTool** | 연결된 [MCP servers](/ko/mcp)에서 노출된 리소스를 나열합니다                                                                                                                                                              | 아니오   |
| **LSP**                  | 언어 서버를 통한 코드 인텔리전스입니다. 파일 편집 후 유형 오류 및 경고를 자동으로 보고합니다. 또한 탐색 작업을 지원합니다: 정의로 이동, 참조 찾기, 유형 정보 가져오기, 기호 나열, 구현 찾기, 호출 계층 추적. [코드 인텔리전스 플러그인](/ko/discover-plugins#code-intelligence)과 해당 언어 서버 바이너리가 필요합니다 | 아니오   |
| **NotebookEdit**         | Jupyter 노트북 셀을 수정합니다                                                                                                                                                                                     | 예     |
| **Read**                 | 파일의 내용을 읽습니다                                                                                                                                                                                             | 아니오   |
| **ReadMcpResourceTool**  | URI로 특정 MCP 리소스를 읽습니다                                                                                                                                                                                    | 아니오   |
| **Skill**                | 주 대화 내에서 [skill](/ko/skills#control-who-invokes-a-skill)을 실행합니다                                                                                                                                          | 예     |
| **TaskCreate**           | 작업 목록에 새 작업을 생성합니다                                                                                                                                                                                       | 아니오   |
| **TaskGet**              | 특정 작업의 전체 세부사항을 검색합니다                                                                                                                                                                                    | 아니오   |
| **TaskList**             | 현재 상태가 있는 모든 작업을 나열합니다                                                                                                                                                                                   | 아니오   |
| **TaskOutput**           | 백그라운드 작업에서 출력을 검색합니다                                                                                                                                                                                     | 아니오   |
| **TaskStop**             | ID로 실행 중인 백그라운드 작업을 중지합니다                                                                                                                                                                                | 아니오   |
| **TaskUpdate**           | 작업 상태, 종속성, 세부사항을 업데이트하거나 작업을 삭제합니다                                                                                                                                                                      | 아니오   |
| **TodoWrite**            | 세션 작업 체크리스트를 관리합니다. 비대화형 모드 및 [Agent SDK](/ko/headless)에서 사용 가능합니다. 대화형 세션은 대신 TaskCreate, TaskGet, TaskList 및 TaskUpdate를 사용합니다                                                                         | 아니오   |
| **ToolSearch**           | [도구 검색](/ko/mcp#scale-with-mcp-tool-search)이 활성화되면 지연된 도구를 검색하고 로드합니다                                                                                                                                    | 아니오   |
| **WebFetch**             | 지정된 URL에서 콘텐츠를 가져옵니다                                                                                                                                                                                     | 예     |
| **WebSearch**            | 웹 검색을 수행합니다                                                                                                                                                                                              | 예     |
| **Write**                | 파일을 생성하거나 덮어씁니다                                                                                                                                                                                          | 예     |

권한 규칙은 `/allowed-tools`를 사용하거나 [권한 설정](/ko/settings#available-settings)에서 구성할 수 있습니다. [도구 특정 권한 규칙](/ko/permissions#tool-specific-permission-rules)도 참조하세요.

### Bash 도구 동작

Bash 도구는 다음 지속성 동작으로 셸 명령을 실행합니다:

* **작업 디렉토리 지속**: Claude가 작업 디렉토리를 변경하면 (예: `cd /path/to/dir`), 후속 Bash 명령은 해당 디렉토리에서 실행됩니다. `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1`을 사용하여 각 명령 후 프로젝트 디렉토리로 재설정할 수 있습니다.
* **환경 변수는 지속되지 않음**: 한 Bash 명령에서 설정된 환경 변수 (예: `export MY_VAR=value`)는 **후속 Bash 명령에서 사용할 수 없습니다**. 각 Bash 명령은 새로운 셸 환경에서 실행됩니다.

Bash 명령에서 환경 변수를 사용 가능하게 하려면 **3가지 옵션**이 있습니다:

**옵션 1: Claude Code를 시작하기 전에 환경 활성화** (가장 간단한 접근)

Claude Code를 시작하기 전에 터미널에서 가상 환경을 활성화합니다:

```bash  theme={null}
conda activate myenv
# 또는: source /path/to/venv/bin/activate
claude
```

이는 셸 환경에서 작동하지만 Claude의 Bash 명령 내에서 설정된 환경 변수는 명령 간에 지속되지 않습니다.

**옵션 2: Claude Code를 시작하기 전에 CLAUDE\_ENV\_FILE 설정** (지속적인 환경 설정)

환경 설정을 포함하는 셸 스크립트의 경로를 내보냅니다:

```bash  theme={null}
export CLAUDE_ENV_FILE=/path/to/env-setup.sh
claude
```

여기서 `/path/to/env-setup.sh`에는:

```bash  theme={null}
conda activate myenv
# 또는: source /path/to/venv/bin/activate
# 또는: export MY_VAR=value
```

Claude Code는 각 Bash 명령 전에 이 파일을 소싱하여 모든 명령에서 환경을 지속시킵니다.

**옵션 3: SessionStart hook 사용** (프로젝트 특정 구성)

`.claude/settings.json`에서 구성합니다:

```json  theme={null}
{
  "hooks": {
    "SessionStart": [{
      "matcher": "startup",
      "hooks": [{
        "type": "command",
        "command": "echo 'conda activate myenv' >> \"$CLAUDE_ENV_FILE\""
      }]
    }]
  }
}
```

Hook은 `$CLAUDE_ENV_FILE`에 쓰며, 이는 각 Bash 명령 전에 소싱됩니다. 이는 팀 공유 프로젝트 구성에 이상적입니다.

[SessionStart hooks](/ko/hooks#persist-environment-variables)에서 옵션 3에 대한 자세한 내용을 참조하세요.

### hooks로 도구 확장

[Claude Code hooks](/ko/hooks-guide)를 사용하여 모든 도구 실행 전후에 사용자 정의 명령을 실행할 수 있습니다.

예를 들어 Claude가 Python 파일을 수정한 후 Python 포매터를 자동으로 실행하거나 특정 경로에 대한 Write 작업을 차단하여 프로덕션 구성 파일 수정을 방지할 수 있습니다.

## 참고 항목

* [권한](/ko/permissions): 권한 시스템, 규칙 구문, 도구 특정 패턴 및 managed 정책
* [인증](/ko/authentication): Claude Code에 대한 사용자 액세스 설정
* [문제 해결](/ko/troubleshooting): 일반적인 구성 문제에 대한 솔루션
