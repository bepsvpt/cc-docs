> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 엔터프라이즈 네트워크 구성

> 프록시 서버, 사용자 정의 인증 기관(CA), 상호 전송 계층 보안(mTLS) 인증을 통해 엔터프라이즈 환경에서 Claude Code를 구성합니다.

Claude Code는 환경 변수를 통해 다양한 엔터프라이즈 네트워크 및 보안 구성을 지원합니다. 여기에는 회사 프록시 서버를 통한 트래픽 라우팅, 사용자 정의 인증 기관(CA) 신뢰, 향상된 보안을 위한 상호 전송 계층 보안(mTLS) 인증서를 사용한 인증이 포함됩니다.

<Note>
  이 페이지에 표시된 모든 환경 변수는 [`settings.json`](/ko/settings)에서도 구성할 수 있습니다.
</Note>

## 프록시 구성

### 환경 변수

Claude Code는 표준 프록시 환경 변수를 준수합니다:

```bash theme={null}
# HTTPS 프록시 (권장)
export HTTPS_PROXY=https://proxy.example.com:8080

# HTTP 프록시 (HTTPS를 사용할 수 없는 경우)
export HTTP_PROXY=http://proxy.example.com:8080

# 특정 요청에 대해 프록시 우회 - 공백으로 구분된 형식
export NO_PROXY="localhost 192.168.1.1 example.com .example.com"
# 특정 요청에 대해 프록시 우회 - 쉼표로 구분된 형식
export NO_PROXY="localhost,192.168.1.1,example.com,.example.com"
# 모든 요청에 대해 프록시 우회
export NO_PROXY="*"
```

<Note>
  Claude Code는 SOCKS 프록시를 지원하지 않습니다.
</Note>

### 기본 인증

프록시에 기본 인증이 필요한 경우 프록시 URL에 자격 증명을 포함합니다:

```bash theme={null}
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

<Warning>
  스크립트에 암호를 하드코딩하지 마십시오. 대신 환경 변수 또는 보안 자격 증명 저장소를 사용하십시오.
</Warning>

<Tip>
  고급 인증(NTLM, Kerberos 등)이 필요한 프록시의 경우 인증 방법을 지원하는 LLM Gateway 서비스 사용을 고려하십시오.
</Tip>

## CA 인증서 저장소

기본적으로 Claude Code는 번들로 제공되는 Mozilla CA 인증서와 운영 체제의 인증서 저장소를 모두 신뢰합니다. CrowdStrike Falcon 및 Zscaler와 같은 엔터프라이즈 TLS 검사 프록시는 루트 인증서가 OS 신뢰 저장소에 설치되어 있으면 추가 구성 없이 작동합니다.

<Note>
  시스템 CA 저장소 통합에는 네이티브 Claude Code 바이너리 배포가 필요합니다. Node.js 런타임에서 실행할 때는 시스템 CA 저장소가 자동으로 병합되지 않습니다. 이 경우 `NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem`을 설정하여 엔터프라이즈 루트 CA를 신뢰합니다.
</Note>

`CLAUDE_CODE_CERT_STORE`는 쉼표로 구분된 소스 목록을 허용합니다. 인식되는 값은 Claude Code와 함께 제공되는 Mozilla CA 세트의 경우 `bundled`, 운영 체제 신뢰 저장소의 경우 `system`입니다. 기본값은 `bundled,system`입니다.

번들로 제공되는 Mozilla CA 세트만 신뢰하려면:

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=bundled
```

OS 인증서 저장소만 신뢰하려면:

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=system
```

<Note>
  `CLAUDE_CODE_CERT_STORE`에는 전용 `settings.json` 스키마 키가 없습니다. `~/.claude/settings.json`의 `env` 블록에서 또는 프로세스 환경에서 직접 설정합니다.
</Note>

## 사용자 정의 CA 인증서

엔터프라이즈 환경에서 사용자 정의 CA를 사용하는 경우 Claude Code를 구성하여 이를 직접 신뢰하도록 합니다:

```bash theme={null}
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## mTLS 인증

클라이언트 인증서 인증이 필요한 엔터프라이즈 환경의 경우:

```bash theme={null}
# 인증용 클라이언트 인증서
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# 클라이언트 개인 키
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# 선택 사항: 암호화된 개인 키의 암호
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

## 네트워크 액세스 요구 사항

Claude Code는 다음 URL에 대한 액세스가 필요합니다. 특히 컨테이너화되거나 제한된 네트워크 환경에서 프록시 구성 및 방화벽 규칙에 이러한 URL을 허용 목록에 추가하십시오.

| URL                            | 필요한 용도                                                                |
| ------------------------------ | --------------------------------------------------------------------- |
| `api.anthropic.com`            | Claude API 요청                                                         |
| `claude.ai`                    | claude.ai 계정 인증                                                       |
| `platform.claude.com`          | Anthropic Console 계정 인증                                               |
| `downloads.claude.ai`          | 플러그인 실행 파일 다운로드; 네이티브 설치 관리자 및 네이티브 자동 업데이터                           |
| `storage.googleapis.com`       | {/* max-version: 2.1.115 */}2.1.116 이전 버전의 네이티브 설치 관리자 및 네이티브 자동 업데이터 |
| `bridge.claudeusercontent.com` | [Chrome의 Claude](/ko/chrome) 확장 프로그램 WebSocket 브리지                    |

npm을 통해 Claude Code를 설치하거나 자신의 바이너리 배포를 관리하는 경우 최종 사용자는 `downloads.claude.ai` 또는 `storage.googleapis.com`에 대한 액세스가 필요하지 않을 수 있습니다.

Claude Code는 기본적으로 선택적 운영 원격 분석을 전송하며, 환경 변수를 사용하여 이를 비활성화할 수 있습니다. 허용 목록을 최종 확정하기 전에 원격 분석을 비활성화하는 방법은 [원격 분석 서비스](/ko/data-usage#telemetry-services)를 참조하십시오.

[Amazon Bedrock](/ko/amazon-bedrock), [Google Vertex AI](/ko/google-vertex-ai) 또는 [Microsoft Foundry](/ko/microsoft-foundry)를 사용할 때 모델 트래픽 및 인증은 `api.anthropic.com`, `claude.ai` 또는 `platform.claude.com` 대신 공급자로 이동합니다. WebFetch 도구는 [설정](/ko/settings)에서 `skipWebFetchPreflight: true`를 설정하지 않는 한 [도메인 안전 검사](/ko/data-usage#webfetch-domain-safety-check)를 위해 여전히 `api.anthropic.com`을 호출합니다.

[웹의 Claude Code](/ko/claude-code-on-the-web) 및 [Code Review](/ko/code-review)는 Anthropic 관리 인프라에서 리포지토리에 연결합니다. GitHub Enterprise Cloud 조직이 IP 주소로 액세스를 제한하는 경우 [설치된 GitHub Apps에 대한 IP 허용 목록 상속 활성화](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#allowing-access-by-github-apps)를 수행하십시오. Claude GitHub App은 IP 범위를 등록하므로 이 설정을 활성화하면 수동 구성 없이 액세스할 수 있습니다. 대신 [범위를 허용 목록에 수동으로 추가](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#adding-an-allowed-ip-address)하거나 다른 방화벽을 구성하려면 [Anthropic API IP 주소](https://platform.claude.com/docs/en/api/ip-addresses)를 참조하십시오.

자체 호스팅 [GitHub Enterprise Server](/ko/github-enterprise-server) 인스턴스가 방화벽 뒤에 있는 경우 동일한 [Anthropic API IP 주소](https://platform.claude.com/docs/en/api/ip-addresses)를 허용 목록에 추가하여 Anthropic 인프라가 GHES 호스트에 도달하여 리포지토리를 복제하고 검토 의견을 게시할 수 있도록 합니다.

## 추가 리소스

* [Claude Code 설정](/ko/settings)
* [환경 변수 참조](/ko/env-vars)
* [문제 해결 가이드](/ko/troubleshooting)
