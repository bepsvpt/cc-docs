> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 엔터프라이즈 배포 개요

> Claude Code가 다양한 타사 서비스 및 인프라와 통합되어 엔터프라이즈 배포 요구사항을 충족하는 방법을 알아봅니다.

이 페이지는 사용 가능한 배포 옵션의 개요를 제공하며 조직에 맞는 올바른 구성을 선택하는 데 도움을 줍니다.

## 제공자 비교

<table>
  <thead>
    <tr>
      <th>기능</th>
      <th>Anthropic</th>
      <th>Amazon Bedrock</th>
      <th>Google Vertex AI</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>지역</td>
      <td>지원되는 [국가](https://www.anthropic.com/supported-countries)</td>
      <td>여러 AWS [지역](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html)</td>
      <td>여러 GCP [지역](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations)</td>
      <td>여러 Azure [지역](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/)</td>
    </tr>

    <tr>
      <td>프롬프트 캐싱</td>
      <td>기본적으로 활성화됨</td>
      <td>기본적으로 활성화됨</td>
      <td>기본적으로 활성화됨</td>
      <td>기본적으로 활성화됨</td>
    </tr>

    <tr>
      <td>인증</td>
      <td>API 키</td>
      <td>API 키 또는 AWS 자격증명</td>
      <td>GCP 자격증명</td>
      <td>API 키 또는 Microsoft Entra ID</td>
    </tr>

    <tr>
      <td>비용 추적</td>
      <td>대시보드</td>
      <td>AWS Cost Explorer</td>
      <td>GCP Billing</td>
      <td>Azure Cost Management</td>
    </tr>

    <tr>
      <td>엔터프라이즈 기능</td>
      <td>팀, 사용량 모니터링</td>
      <td>IAM 정책, CloudTrail</td>
      <td>IAM 역할, Cloud Audit Logs</td>
      <td>RBAC 정책, Azure Monitor</td>
    </tr>
  </tbody>
</table>

## 클라우드 제공자

<CardGroup cols={3}>
  <Card title="Amazon Bedrock" icon="aws" href="/ko/amazon-bedrock">
    API 키 또는 IAM 기반 인증 및 AWS 네이티브 모니터링을 통해 AWS 인프라를 통해 Claude 모델 사용
  </Card>

  <Card title="Google Vertex AI" icon="google" href="/ko/google-vertex-ai">
    엔터프라이즈급 보안 및 규정 준수를 통해 Google Cloud Platform을 통해 Claude 모델에 액세스
  </Card>

  <Card title="Microsoft Foundry" icon="microsoft" href="/ko/microsoft-foundry">
    API 키 또는 Microsoft Entra ID 인증 및 Azure 청구를 통해 Azure를 통해 Claude에 액세스
  </Card>
</CardGroup>

## 기업 인프라

<CardGroup cols={2}>
  <Card title="엔터프라이즈 네트워크" icon="shield" href="/ko/network-config">
    조직의 프록시 서버 및 SSL/TLS 요구사항과 함께 작동하도록 Claude Code 구성
  </Card>

  <Card title="LLM Gateway" icon="server" href="/ko/llm-gateway">
    사용량 추적, 예산 책정 및 감사 로깅을 통해 중앙 집중식 모델 액세스 배포
  </Card>
</CardGroup>

## 구성 개요

Claude Code는 다양한 제공자 및 인프라를 결합할 수 있는 유연한 구성 옵션을 지원합니다:

<Note>
  다음의 차이점을 이해하세요:

  * **기업 프록시**: 트래픽 라우팅을 위한 HTTP/HTTPS 프록시 (`HTTPS_PROXY` 또는 `HTTP_PROXY`를 통해 설정)
  * **LLM Gateway**: 인증을 처리하고 제공자 호환 엔드포인트를 제공하는 서비스 (`ANTHROPIC_BASE_URL`, `ANTHROPIC_BEDROCK_BASE_URL` 또는 `ANTHROPIC_VERTEX_BASE_URL`을 통해 설정)

  두 구성을 함께 사용할 수 있습니다.
</Note>

### 기업 프록시를 사용한 Bedrock

기업 HTTP/HTTPS 프록시를 통해 Bedrock 트래픽 라우팅:

```bash  theme={null}
# Bedrock 활성화
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1

# 기업 프록시 구성
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### LLM Gateway를 사용한 Bedrock

Bedrock 호환 엔드포인트를 제공하는 게이트웨이 서비스 사용:

```bash  theme={null}
# Bedrock 활성화
export CLAUDE_CODE_USE_BEDROCK=1

# LLM 게이트웨이 구성
export ANTHROPIC_BEDROCK_BASE_URL='https://your-llm-gateway.com/bedrock'
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1  # 게이트웨이가 AWS 인증을 처리하는 경우
```

### 기업 프록시를 사용한 Foundry

기업 HTTP/HTTPS 프록시를 통해 Azure 트래픽 라우팅:

```bash  theme={null}
# Microsoft Foundry 활성화
export CLAUDE_CODE_USE_FOUNDRY=1
export ANTHROPIC_FOUNDRY_RESOURCE=your-resource
export ANTHROPIC_FOUNDRY_API_KEY=your-api-key  # 또는 Entra ID 인증의 경우 생략

# 기업 프록시 구성
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### LLM Gateway를 사용한 Foundry

Azure 호환 엔드포인트를 제공하는 게이트웨이 서비스 사용:

```bash  theme={null}
# Microsoft Foundry 활성화
export CLAUDE_CODE_USE_FOUNDRY=1

# LLM 게이트웨이 구성
export ANTHROPIC_FOUNDRY_BASE_URL='https://your-llm-gateway.com'
export CLAUDE_CODE_SKIP_FOUNDRY_AUTH=1  # 게이트웨이가 Azure 인증을 처리하는 경우
```

### 기업 프록시를 사용한 Vertex AI

기업 HTTP/HTTPS 프록시를 통해 Vertex AI 트래픽 라우팅:

```bash  theme={null}
# Vertex 활성화
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id

# 기업 프록시 구성
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### LLM Gateway를 사용한 Vertex AI

중앙 집중식 관리를 위해 Google Vertex AI 모델을 LLM 게이트웨이와 결합:

```bash  theme={null}
# Vertex 활성화
export CLAUDE_CODE_USE_VERTEX=1

# LLM 게이트웨이 구성
export ANTHROPIC_VERTEX_BASE_URL='https://your-llm-gateway.com/vertex'
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1  # 게이트웨이가 GCP 인증을 처리하는 경우
```

### 인증 구성

Claude Code는 필요할 때 `Authorization` 헤더에 대해 `ANTHROPIC_AUTH_TOKEN`을 사용합니다. `SKIP_AUTH` 플래그 (`CLAUDE_CODE_SKIP_BEDROCK_AUTH`, `CLAUDE_CODE_SKIP_VERTEX_AUTH`)는 게이트웨이가 제공자 인증을 처리하는 LLM 게이트웨이 시나리오에서 사용됩니다.

## 올바른 배포 구성 선택

배포 방식을 선택할 때 다음 요소를 고려하세요:

### 직접 제공자 액세스

다음과 같은 조직에 최적:

* 가장 간단한 설정을 원함
* 기존 AWS 또는 GCP 인프라 보유
* 제공자 네이티브 모니터링 및 규정 준수 필요

### 기업 프록시

다음과 같은 조직에 최적:

* 기존 기업 프록시 요구사항 보유
* 트래픽 모니터링 및 규정 준수 필요
* 모든 트래픽을 특정 네트워크 경로를 통해 라우팅해야 함

### LLM Gateway

다음과 같은 조직에 최적:

* 팀 전체의 사용량 추적 필요
* 모델 간 동적 전환 원함
* 사용자 정의 속도 제한 또는 예산 필요
* 중앙 집중식 인증 관리 필요

## 디버깅

배포를 디버깅할 때:

* `claude /status` [슬래시 명령어](/ko/slash-commands)를 사용하세요. 이 명령어는 적용된 인증, 프록시 및 URL 설정에 대한 관찰성을 제공합니다.
* 환경 변수 `export ANTHROPIC_LOG=debug`를 설정하여 요청을 로깅합니다.

## 조직을 위한 모범 사례

### 1. 문서화 및 메모리에 투자

Claude Code가 코드베이스를 이해하도록 문서화에 투자할 것을 강력히 권장합니다. 조직은 여러 수준에서 CLAUDE.md 파일을 배포할 수 있습니다:

* **조직 전체**: 회사 전체 표준을 위해 `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS)와 같은 시스템 디렉토리에 배포
* **저장소 수준**: 프로젝트 아키텍처, 빌드 명령 및 기여 지침을 포함하는 저장소 루트에 `CLAUDE.md` 파일 생성. 소스 제어에 체크인하여 모든 사용자가 이점을 얻도록 함

  [자세히 알아보기](/ko/memory).

### 2. 배포 단순화

사용자 정의 개발 환경이 있는 경우, Claude Code를 설치하는 "원클릭" 방식을 만드는 것이 조직 전체에서 채택을 늘리는 핵심이라고 생각합니다.

### 3. 안내된 사용으로 시작

새 사용자가 코드베이스 Q\&A 또는 더 작은 버그 수정이나 기능 요청에 Claude Code를 시도하도록 권장합니다. Claude Code에 계획을 세우도록 요청하세요. Claude의 제안을 확인하고 잘못된 경우 피드백을 제공하세요. 시간이 지남에 따라 사용자가 이 새로운 패러다임을 더 잘 이해하게 되면, Claude Code를 더 자율적으로 실행하는 데 더 효과적이 될 것입니다.

### 4. 보안 정책 구성

보안 팀은 Claude Code가 할 수 있는 것과 할 수 없는 것에 대한 관리 권한을 구성할 수 있으며, 이는 로컬 구성으로 덮어쓸 수 없습니다. [자세히 알아보기](/ko/security).

### 5. MCP를 통합에 활용

MCP는 Claude Code에 더 많은 정보를 제공하는 좋은 방법입니다. 예를 들어 티켓 관리 시스템이나 오류 로그에 연결할 수 있습니다. 한 중앙 팀이 MCP 서버를 구성하고 `.mcp.json` 구성을 코드베이스에 체크인하여 모든 사용자가 이점을 얻도록 할 것을 권장합니다. [자세히 알아보기](/ko/mcp).

Anthropic에서는 Claude Code가 모든 Anthropic 코드베이스 전체에서 개발을 강화하도록 신뢰합니다. Claude Code를 우리만큼 즐기시기를 바랍니다.

## 다음 단계

* [Amazon Bedrock 설정](/ko/amazon-bedrock) - AWS 네이티브 배포
* [Google Vertex AI 구성](/ko/google-vertex-ai) - GCP 배포
* [Microsoft Foundry 설정](/ko/microsoft-foundry) - Azure 배포
* [엔터프라이즈 네트워크 구성](/ko/network-config) - 네트워크 요구사항
* [LLM Gateway 배포](/ko/llm-gateway) - 엔터프라이즈 관리
* [설정](/ko/settings) - 구성 옵션 및 환경 변수
