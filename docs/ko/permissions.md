> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 권한 구성

> 세분화된 권한 규칙, 모드 및 관리형 정책을 통해 Claude Code가 액세스하고 수행할 수 있는 작업을 제어합니다.

Claude Code는 에이전트가 수행할 수 있는 작업과 수행할 수 없는 작업을 정확하게 지정할 수 있도록 세분화된 권한을 지원합니다. 권한 설정은 버전 제어에 체크인할 수 있으며 조직의 모든 개발자에게 배포할 수 있을 뿐만 아니라 개별 개발자가 사용자 정의할 수 있습니다.

## 권한 시스템

Claude Code는 강력함과 안전성의 균형을 맞추기 위해 계층화된 권한 시스템을 사용합니다:

| 도구 유형   | 예시            | 승인 필요 | "예, 다시 묻지 않기" 동작    |
| :------ | :------------ | :---- | :------------------ |
| 읽기 전용   | 파일 읽기, Grep   | 아니오   | 해당 없음               |
| Bash 명령 | 셸 실행          | 예     | 프로젝트 디렉토리 및 명령당 영구적 |
| 파일 수정   | Edit/Write 파일 | 예     | 세션 종료까지             |

## 권한 관리

`/permissions`를 사용하여 Claude Code의 도구 권한을 보고 관리할 수 있습니다. 이 UI는 모든 권한 규칙과 이들이 출처한 settings.json 파일을 나열합니다.

* **Allow** 규칙을 사용하면 Claude Code가 수동 승인 없이 지정된 도구를 사용할 수 있습니다.
* **Ask** 규칙은 Claude Code가 지정된 도구를 사용하려고 할 때마다 확인을 요청합니다.
* **Deny** 규칙은 Claude Code가 지정된 도구를 사용하지 못하도록 방지합니다.

규칙은 순서대로 평가됩니다: **deny -> ask -> allow**. 첫 번째 일치하는 규칙이 우선이므로 deny 규칙이 항상 우선합니다.

## 권한 모드

Claude Code는 도구 승인 방식을 제어하는 여러 권한 모드를 지원합니다. [설정 파일](/ko/settings#settings-files)에서 `defaultMode`를 설정합니다:

| 모드                  | 설명                                                                       |
| :------------------ | :----------------------------------------------------------------------- |
| `default`           | 표준 동작: 각 도구를 처음 사용할 때 권한을 요청합니다                                          |
| `acceptEdits`       | 세션에 대해 파일 편집 권한을 자동으로 수락합니다                                              |
| `plan`              | Plan Mode: Claude는 파일을 분석할 수 있지만 수정하거나 명령을 실행할 수 없습니다                    |
| `dontAsk`           | `/permissions` 또는 `permissions.allow` 규칙을 통해 사전 승인되지 않은 한 도구를 자동으로 거부합니다 |
| `bypassPermissions` | 모든 권한 프롬프트를 건너뜁니다(안전한 환경 필요, 아래 경고 참조)                                   |

<Warning>
  `bypassPermissions` 모드는 모든 권한 검사를 비활성화합니다. 컨테이너나 VM과 같은 Claude Code가 손상을 일으킬 수 없는 격리된 환경에서만 사용합니다. 관리자는 [관리형 설정](#managed-settings)에서 `disableBypassPermissionsMode`를 `"disable"`로 설정하여 이 모드를 방지할 수 있습니다.
</Warning>

## 권한 규칙 구문

권한 규칙은 `Tool` 또는 `Tool(specifier)` 형식을 따릅니다.

### 도구의 모든 사용 일치

도구의 모든 사용을 일치시키려면 괄호 없이 도구 이름만 사용합니다:

| 규칙         | 효과                  |
| :--------- | :------------------ |
| `Bash`     | 모든 Bash 명령과 일치합니다   |
| `WebFetch` | 모든 웹 가져오기 요청과 일치합니다 |
| `Read`     | 모든 파일 읽기와 일치합니다     |

`Bash(*)`는 `Bash`와 동등하며 모든 Bash 명령과 일치합니다.

### 세분화된 제어를 위해 지정자 사용

괄호 안에 지정자를 추가하여 특정 도구 사용과 일치시킵니다:

| 규칙                             | 효과                            |
| :----------------------------- | :---------------------------- |
| `Bash(npm run build)`          | 정확한 명령 `npm run build`와 일치합니다 |
| `Read(./.env)`                 | 현재 디렉토리의 `.env` 파일 읽기와 일치합니다  |
| `WebFetch(domain:example.com)` | example.com으로의 가져오기 요청과 일치합니다 |

### 와일드카드 패턴

Bash 규칙은 `*`를 사용한 glob 패턴을 지원합니다. 와일드카드는 명령의 어느 위치에나 나타날 수 있습니다. 이 구성은 npm 및 git commit 명령을 허용하면서 git push를 차단합니다:

```json  theme={null}
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git commit *)",
      "Bash(git * main)",
      "Bash(* --version)",
      "Bash(* --help *)"
    ],
    "deny": [
      "Bash(git push *)"
    ]
  }
}
```

`*` 앞의 공백이 중요합니다: `Bash(ls *)`는 `ls -la`와 일치하지만 `lsof`와는 일치하지 않으며, `Bash(ls*)`는 둘 다 일치합니다. 레거시 `:*` 접미사 구문은 ` *`와 동등하지만 더 이상 사용되지 않습니다.

## 도구별 권한 규칙

### Bash

Bash 권한 규칙은 `*`를 사용한 와일드카드 일치를 지원합니다. 와일드카드는 명령의 시작, 중간 또는 끝을 포함하여 어느 위치에나 나타날 수 있습니다:

* `Bash(npm run build)`는 정확한 Bash 명령 `npm run build`와 일치합니다
* `Bash(npm run test *)`는 `npm run test`로 시작하는 Bash 명령과 일치합니다
* `Bash(npm *)`는 `npm `로 시작하는 모든 명령과 일치합니다
* `Bash(* install)`은 ` install`로 끝나는 모든 명령과 일치합니다
* `Bash(git * main)`은 `git checkout main`, `git merge main`과 같은 명령과 일치합니다

`*`가 앞에 공백이 있는 끝에 나타날 때(예: `Bash(ls *)`), 단어 경계를 적용하여 접두사 뒤에 공백이나 문자열 끝이 필요합니다. 예를 들어, `Bash(ls *)`는 `ls -la`와 일치하지만 `lsof`와는 일치하지 않습니다. 반대로, 공백이 없는 `Bash(ls*)`는 단어 경계 제약이 없으므로 `ls -la`와 `lsof` 모두와 일치합니다.

<Tip>
  Claude Code는 셸 연산자(예: `&&`)를 인식하므로 `Bash(safe-cmd *)`와 같은 접두사 일치 규칙은 `safe-cmd && other-cmd` 명령을 실행할 권한을 부여하지 않습니다.
</Tip>

<Warning>
  명령 인수를 제약하려고 시도하는 Bash 권한 패턴은 취약합니다. 예를 들어, `Bash(curl http://github.com/ *)`는 curl을 GitHub URL로 제한하려고 하지만 다음과 같은 변형과는 일치하지 않습니다:

  * URL 앞의 옵션: `curl -X GET http://github.com/...`
  * 다른 프로토콜: `curl https://github.com/...`
  * 리다이렉트: `curl -L http://bit.ly/xyz` (github로 리다이렉트)
  * 변수: `URL=http://github.com && curl $URL`
  * 추가 공백: `curl  http://github.com`

  더 안정적인 URL 필터링을 위해 다음을 고려합니다:

  * **Bash 네트워크 도구 제한**: deny 규칙을 사용하여 `curl`, `wget` 및 유사한 명령을 차단한 다음 허용된 도메인에 대해 `WebFetch(domain:github.com)` 권한으로 WebFetch 도구를 사용합니다
  * **PreToolUse 훅 사용**: Bash 명령의 URL을 검증하고 허용되지 않은 도메인을 차단하는 훅을 구현합니다
  * CLAUDE.md를 통해 Claude Code에 허용된 curl 패턴에 대해 지시합니다

  WebFetch만 사용하는 것은 네트워크 액세스를 방지하지 않습니다. Bash가 허용되면 Claude는 여전히 `curl`, `wget` 또는 다른 도구를 사용하여 모든 URL에 도달할 수 있습니다.
</Warning>

### Read 및 Edit

`Edit` 규칙은 파일을 편집하는 모든 기본 제공 도구에 적용됩니다. Claude는 Grep 및 Glob과 같이 파일을 읽는 모든 기본 제공 도구에 `Read` 규칙을 적용하기 위해 최선을 다합니다.

Read 및 Edit 규칙은 모두 [gitignore](https://git-scm.com/docs/gitignore) 사양을 따르며 4가지 고유한 패턴 유형이 있습니다:

| 패턴                 | 의미                   | 예시                               | 일치                             |
| ------------------ | -------------------- | -------------------------------- | ------------------------------ |
| `//path`           | 파일 시스템 루트의 **절대** 경로 | `Read(//Users/alice/secrets/**)` | `/Users/alice/secrets/**`      |
| `~/path`           | **홈** 디렉토리의 경로       | `Read(~/Documents/*.pdf)`        | `/Users/alice/Documents/*.pdf` |
| `/path`            | 프로젝트 루트에 **상대적인** 경로 | `Edit(/src/**/*.ts)`             | `<project root>/src/**/*.ts`   |
| `path` 또는 `./path` | 현재 디렉토리에 **상대적인** 경로 | `Read(*.env)`                    | `<cwd>/*.env`                  |

<Warning>
  `/Users/alice/file`과 같은 패턴은 절대 경로가 아닙니다. 프로젝트 루트에 상대적입니다. 절대 경로의 경우 `//Users/alice/file`을 사용합니다.
</Warning>

예시:

* `Edit(/docs/**)`: `<project>/docs/`의 편집 (NOT `/docs/` and NOT `<project>/.claude/docs/`)
* `Read(~/.zshrc)`: 홈 디렉토리의 `.zshrc` 읽기
* `Edit(//tmp/scratch.txt)`: 절대 경로 `/tmp/scratch.txt` 편집
* `Read(src/**)`: `<current-directory>/src/`에서 읽기

<Note>
  gitignore 패턴에서 `*`는 단일 디렉토리의 파일과 일치하고 `**`는 디렉토리 전체에서 재귀적으로 일치합니다. 모든 파일 액세스를 허용하려면 괄호 없이 도구 이름만 사용합니다: `Read`, `Edit` 또는 `Write`.
</Note>

### WebFetch

* `WebFetch(domain:example.com)`은 example.com으로의 가져오기 요청과 일치합니다

### MCP

* `mcp__puppeteer`는 `puppeteer` 서버(Claude Code에서 구성된 이름)에서 제공하는 모든 도구와 일치합니다
* `mcp__puppeteer__*` 와일드카드 구문은 `puppeteer` 서버의 모든 도구와도 일치합니다
* `mcp__puppeteer__puppeteer_navigate`는 `puppeteer` 서버에서 제공하는 `puppeteer_navigate` 도구와 일치합니다

### Agent (subagents)

`Agent(AgentName)` 규칙을 사용하여 Claude가 사용할 수 있는 [subagents](/ko/sub-agents)를 제어합니다:

* `Agent(Explore)`는 Explore subagent와 일치합니다
* `Agent(Plan)`은 Plan subagent와 일치합니다
* `Agent(my-custom-agent)`는 `my-custom-agent`라는 사용자 정의 subagent와 일치합니다

이러한 규칙을 설정의 `deny` 배열에 추가하거나 `--disallowedTools` CLI 플래그를 사용하여 특정 에이전트를 비활성화합니다. Explore 에이전트를 비활성화하려면:

```json  theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)"]
  }
}
```

## 훅으로 권한 확장

[Claude Code 훅](/ko/hooks-guide)은 런타임에 권한 평가를 수행하기 위해 사용자 정의 셸 명령을 등록하는 방법을 제공합니다. Claude Code가 도구 호출을 할 때, PreToolUse 훅은 권한 시스템 전에 실행되며, 훅 출력은 권한 시스템 대신 도구 호출을 승인하거나 거부할지 여부를 결정할 수 있습니다.

## 작업 디렉토리

기본적으로 Claude는 시작된 디렉토리의 파일에 액세스할 수 있습니다. 이 액세스를 확장할 수 있습니다:

* **시작 중**: `--add-dir <path>` CLI 인수 사용
* **세션 중**: `/add-dir` 명령 사용
* **영구 구성**: [설정 파일](/ko/settings#settings-files)의 `additionalDirectories`에 추가

추가 디렉토리의 파일은 원래 작업 디렉토리와 동일한 권한 규칙을 따릅니다: 프롬프트 없이 읽을 수 있게 되며, 파일 편집 권한은 현재 권한 모드를 따릅니다.

## 권한이 샌드박싱과 상호 작용하는 방식

권한과 [샌드박싱](/ko/sandboxing)은 상호 보완적인 보안 계층입니다:

* **권한**은 Claude Code가 사용할 수 있는 도구와 액세스할 수 있는 파일 또는 도메인을 제어합니다. 모든 도구(Bash, Read, Edit, WebFetch, MCP 등)에 적용됩니다.
* **샌드박싱**은 Bash 도구의 파일 시스템 및 네트워크 액세스를 제한하는 OS 수준 적용을 제공합니다. Bash 명령 및 해당 자식 프로세스에만 적용됩니다.

심층 방어를 위해 둘 다 사용합니다:

* 권한 deny 규칙은 Claude가 제한된 리소스에 액세스하려고 시도하는 것을 차단합니다
* 샌드박스 제한은 프롬프트 주입이 Claude의 의사 결정을 우회하더라도 Bash 명령이 정의된 경계 외부의 리소스에 도달하는 것을 방지합니다
* 샌드박스의 파일 시스템 제한은 Read 및 Edit deny 규칙을 사용하며, 별도의 샌드박스 구성은 사용하지 않습니다
* 네트워크 제한은 WebFetch 권한 규칙과 샌드박스의 `allowedDomains` 목록을 결합합니다

## 관리형 설정

Claude Code 구성에 대한 중앙 집중식 제어가 필요한 조직의 경우, 관리자는 사용자 또는 프로젝트 설정으로 재정의할 수 없는 관리형 설정을 배포할 수 있습니다. 이러한 정책 설정은 일반 설정 파일과 동일한 형식을 따르며 MDM/OS 수준 정책, 관리형 설정 파일 또는 [서버 관리형 설정](/ko/server-managed-settings)을 통해 전달될 수 있습니다. 전달 메커니즘 및 파일 위치는 [설정 파일](/ko/settings#settings-files)을 참조합니다.

### 관리형 전용 설정

일부 설정은 관리형 설정에서만 효과적입니다:

| 설정                                        | 설명                                                                                                                                                     |
| :---------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `disableBypassPermissionsMode`            | `bypassPermissions` 모드 및 `--dangerously-skip-permissions` 플래그를 방지하려면 `"disable"`로 설정합니다                                                                |
| `allowManagedPermissionRulesOnly`         | `true`일 때, 사용자 및 프로젝트 설정이 `allow`, `ask` 또는 `deny` 권한 규칙을 정의하는 것을 방지합니다. 관리형 설정의 규칙만 적용됩니다                                                             |
| `allowManagedHooksOnly`                   | `true`일 때, 사용자, 프로젝트 및 플러그인 훅의 로드를 방지합니다. 관리형 훅 및 SDK 훅만 허용됩니다                                                                                         |
| `allowManagedMcpServersOnly`              | `true`일 때, 관리형 설정의 `allowedMcpServers`만 존중됩니다. `deniedMcpServers`는 여전히 모든 소스에서 병합됩니다. [관리형 MCP 구성](/ko/mcp#managed-mcp-configuration) 참조               |
| `blockedMarketplaces`                     | 마켓플레이스 소스의 차단 목록입니다. 차단된 소스는 다운로드 전에 확인되므로 파일 시스템에 닿지 않습니다. [관리형 마켓플레이스 제한](/ko/plugin-marketplaces#managed-marketplace-restrictions) 참조               |
| `sandbox.network.allowManagedDomainsOnly` | `true`일 때, 관리형 설정의 `allowedDomains` 및 `WebFetch(domain:...)` allow 규칙만 존중됩니다. 허용되지 않은 도메인은 사용자에게 프롬프트하지 않고 자동으로 차단됩니다. 거부된 도메인은 여전히 모든 소스에서 병합됩니다      |
| `strictKnownMarketplaces`                 | 사용자가 추가할 수 있는 플러그인 마켓플레이스를 제어합니다. [관리형 마켓플레이스 제한](/ko/plugin-marketplaces#managed-marketplace-restrictions) 참조                                         |
| `allow_remote_sessions`                   | `true`일 때, 사용자가 [Remote Control](/ko/remote-control) 및 [웹 세션](/ko/claude-code-on-the-web)을 시작할 수 있습니다. 기본값은 `true`입니다. 원격 세션 액세스를 방지하려면 `false`로 설정합니다 |

## 설정 우선순위

권한 규칙은 다른 모든 Claude Code 설정과 동일한 [설정 우선순위](/ko/settings#settings-precedence)를 따릅니다:

1. **관리형 설정**: 명령줄 인수를 포함한 다른 수준으로 재정의할 수 없습니다
2. **명령줄 인수**: 임시 세션 재정의
3. **로컬 프로젝트 설정** (`.claude/settings.local.json`)
4. **공유 프로젝트 설정** (`.claude/settings.json`)
5. **사용자 설정** (`~/.claude/settings.json`)

도구가 어느 수준에서든 거부되면 다른 수준은 이를 허용할 수 없습니다. 예를 들어, 관리형 설정 deny는 `--allowedTools`로 재정의할 수 없으며, `--disallowedTools`는 관리형 설정이 정의하는 것 이상의 제한을 추가할 수 있습니다.

권한이 사용자 설정에서 허용되지만 프로젝트 설정에서 거부되면, 프로젝트 설정이 우선이며 권한이 차단됩니다.

## 예시 구성

이 [저장소](https://github.com/anthropics/claude-code/tree/main/examples/settings)에는 일반적인 배포 시나리오에 대한 시작 설정 구성이 포함되어 있습니다. 이를 시작점으로 사용하고 필요에 맞게 조정합니다.

## 참고 항목

* [설정](/ko/settings): 권한 설정 테이블을 포함한 완전한 구성 참조
* [샌드박싱](/ko/sandboxing): Bash 명령에 대한 OS 수준 파일 시스템 및 네트워크 격리
* [인증](/ko/authentication): Claude Code에 대한 사용자 액세스 설정
* [보안](/ko/security): 보안 보호 및 모범 사례
* [훅](/ko/hooks-guide): 워크플로우 자동화 및 권한 평가 확장
