> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 엔터프라이즈 네트워크 구성

> 프록시 서버, 사용자 정의 인증 기관(CA), 상호 전송 계층 보안(mTLS) 인증을 통해 엔터프라이즈 환경에서 Claude Code를 구성합니다.

Claude Code는 환경 변수를 통해 다양한 엔터프라이즈 네트워크 및 보안 구성을 지원합니다. 여기에는 기업 프록시 서버를 통한 트래픽 라우팅, 사용자 정의 인증 기관(CA) 신뢰, 향상된 보안을 위한 상호 전송 계층 보안(mTLS) 인증서를 사용한 인증이 포함됩니다.

<Note>
  이 페이지에 표시된 모든 환경 변수는 [`settings.json`](/ko/settings)에서도 구성할 수 있습니다.
</Note>

## 프록시 구성

### 환경 변수

Claude Code는 표준 프록시 환경 변수를 준수합니다:

```bash  theme={null}
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

```bash  theme={null}
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

<Warning>
  스크립트에 암호를 하드코딩하지 마십시오. 대신 환경 변수 또는 보안 자격 증명 저장소를 사용하십시오.
</Warning>

<Tip>
  고급 인증(NTLM, Kerberos 등)이 필요한 프록시의 경우 인증 방법을 지원하는 LLM Gateway 서비스 사용을 고려하십시오.
</Tip>

## 사용자 정의 CA 인증서

엔터프라이즈 환경에서 HTTPS 연결을 위해 사용자 정의 CA를 사용하는 경우(프록시를 통하든 직접 API 액세스를 통하든) Claude Code를 구성하여 이를 신뢰하도록 합니다:

```bash  theme={null}
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## mTLS 인증

클라이언트 인증서 인증이 필요한 엔터프라이즈 환경의 경우:

```bash  theme={null}
# 인증용 클라이언트 인증서
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# 클라이언트 개인 키
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# 선택 사항: 암호화된 개인 키의 암호
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

## 네트워크 액세스 요구 사항

Claude Code는 다음 URL에 대한 액세스가 필요합니다:

* `api.anthropic.com`: Claude API 엔드포인트
* `claude.ai`: claude.ai 계정 인증
* `platform.claude.com`: Anthropic Console 계정 인증

프록시 구성 및 방화벽 규칙에서 이러한 URL이 허용 목록에 있는지 확인하십시오. 이는 특히 컨테이너화되거나 제한된 네트워크 환경에서 Claude Code를 사용할 때 중요합니다.

## 추가 리소스

* [Claude Code 설정](/ko/settings)
* [환경 변수 참조](/ko/settings#environment-variables)
* [문제 해결 가이드](/ko/troubleshooting)
