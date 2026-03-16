> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Visão geral da implantação empresarial

> Saiba como Claude Code pode se integrar com vários serviços de terceiros e infraestrutura para atender aos requisitos de implantação empresarial.

Esta página fornece uma visão geral das opções de implantação disponíveis e ajuda você a escolher a configuração certa para sua organização.

## Comparação de provedores

<table>
  <thead>
    <tr>
      <th>Recurso</th>
      <th>Anthropic</th>
      <th>Amazon Bedrock</th>
      <th>Google Vertex AI</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Regiões</td>
      <td>[Países](https://www.anthropic.com/supported-countries) suportados</td>
      <td>Múltiplas [regiões](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html) AWS</td>
      <td>Múltiplas [regiões](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations) GCP</td>
      <td>Múltiplas [regiões](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/) Azure</td>
    </tr>

    <tr>
      <td>Cache de prompt</td>
      <td>Ativado por padrão</td>
      <td>Ativado por padrão</td>
      <td>Ativado por padrão</td>
      <td>Ativado por padrão</td>
    </tr>

    <tr>
      <td>Autenticação</td>
      <td>Chave de API</td>
      <td>Chave de API ou credenciais AWS</td>
      <td>Credenciais GCP</td>
      <td>Chave de API ou Microsoft Entra ID</td>
    </tr>

    <tr>
      <td>Rastreamento de custos</td>
      <td>Painel</td>
      <td>AWS Cost Explorer</td>
      <td>Faturamento GCP</td>
      <td>Gerenciamento de Custos do Azure</td>
    </tr>

    <tr>
      <td>Recursos empresariais</td>
      <td>Equipes, monitoramento de uso</td>
      <td>Políticas IAM, CloudTrail</td>
      <td>Funções IAM, Logs de Auditoria da Nuvem</td>
      <td>Políticas RBAC, Azure Monitor</td>
    </tr>
  </tbody>
</table>

## Provedores de nuvem

<CardGroup cols={3}>
  <Card title="Amazon Bedrock" icon="aws" href="/pt/amazon-bedrock">
    Use modelos Claude através da infraestrutura AWS com autenticação baseada em chave de API ou IAM e monitoramento nativo do AWS
  </Card>

  <Card title="Google Vertex AI" icon="google" href="/pt/google-vertex-ai">
    Acesse modelos Claude via Google Cloud Platform com segurança e conformidade de nível empresarial
  </Card>

  <Card title="Microsoft Foundry" icon="microsoft" href="/pt/microsoft-foundry">
    Acesse Claude através do Azure com autenticação por chave de API ou Microsoft Entra ID e faturamento do Azure
  </Card>
</CardGroup>

## Infraestrutura corporativa

<CardGroup cols={2}>
  <Card title="Rede Empresarial" icon="shield" href="/pt/network-config">
    Configure Claude Code para funcionar com servidores proxy e requisitos SSL/TLS da sua organização
  </Card>

  <Card title="Gateway LLM" icon="server" href="/pt/llm-gateway">
    Implante acesso centralizado a modelos com rastreamento de uso, orçamento e registro de auditoria
  </Card>
</CardGroup>

## Visão geral da configuração

Claude Code suporta opções de configuração flexíveis que permitem combinar diferentes provedores e infraestrutura:

<Note>
  Entenda a diferença entre:

  * **Proxy corporativo**: Um proxy HTTP/HTTPS para roteamento de tráfego (definido via `HTTPS_PROXY` ou `HTTP_PROXY`)
  * **Gateway LLM**: Um serviço que lida com autenticação e fornece endpoints compatíveis com provedores (definido via `ANTHROPIC_BASE_URL`, `ANTHROPIC_BEDROCK_BASE_URL` ou `ANTHROPIC_VERTEX_BASE_URL`)

  Ambas as configurações podem ser usadas em conjunto.
</Note>

### Usando Bedrock com proxy corporativo

Roteie o tráfego do Bedrock através de um proxy HTTP/HTTPS corporativo:

```bash  theme={null}
# Ativar Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1

# Configurar proxy corporativo
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Usando Bedrock com Gateway LLM

Use um serviço de gateway que fornece endpoints compatíveis com Bedrock:

```bash  theme={null}
# Ativar Bedrock
export CLAUDE_CODE_USE_BEDROCK=1

# Configurar gateway LLM
export ANTHROPIC_BEDROCK_BASE_URL='https://your-llm-gateway.com/bedrock'
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1  # Se o gateway lidar com autenticação AWS
```

### Usando Foundry com proxy corporativo

Roteie o tráfego do Azure através de um proxy HTTP/HTTPS corporativo:

```bash  theme={null}
# Ativar Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1
export ANTHROPIC_FOUNDRY_RESOURCE=your-resource
export ANTHROPIC_FOUNDRY_API_KEY=your-api-key  # Ou omita para autenticação Entra ID

# Configurar proxy corporativo
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Usando Foundry com Gateway LLM

Use um serviço de gateway que fornece endpoints compatíveis com Azure:

```bash  theme={null}
# Ativar Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1

# Configurar gateway LLM
export ANTHROPIC_FOUNDRY_BASE_URL='https://your-llm-gateway.com'
export CLAUDE_CODE_SKIP_FOUNDRY_AUTH=1  # Se o gateway lidar com autenticação Azure
```

### Usando Vertex AI com proxy corporativo

Roteie o tráfego do Vertex AI através de um proxy HTTP/HTTPS corporativo:

```bash  theme={null}
# Ativar Vertex
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id

# Configurar proxy corporativo
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Usando Vertex AI com Gateway LLM

Combine modelos Google Vertex AI com um gateway LLM para gerenciamento centralizado:

```bash  theme={null}
# Ativar Vertex
export CLAUDE_CODE_USE_VERTEX=1

# Configurar gateway LLM
export ANTHROPIC_VERTEX_BASE_URL='https://your-llm-gateway.com/vertex'
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1  # Se o gateway lidar com autenticação GCP
```

### Configuração de autenticação

Claude Code usa `ANTHROPIC_AUTH_TOKEN` para o cabeçalho `Authorization` quando necessário. Os sinalizadores `SKIP_AUTH` (`CLAUDE_CODE_SKIP_BEDROCK_AUTH`, `CLAUDE_CODE_SKIP_VERTEX_AUTH`) são usados em cenários de gateway LLM onde o gateway lida com autenticação do provedor.

## Escolhendo a configuração de implantação correta

Considere estes fatores ao selecionar sua abordagem de implantação:

### Acesso direto ao provedor

Melhor para organizações que:

* Desejam a configuração mais simples
* Têm infraestrutura AWS ou GCP existente
* Precisam de monitoramento e conformidade nativos do provedor

### Proxy corporativo

Melhor para organizações que:

* Têm requisitos de proxy corporativo existentes
* Precisam de monitoramento de tráfego e conformidade
* Devem rotear todo o tráfego através de caminhos de rede específicos

### Gateway LLM

Melhor para organizações que:

* Precisam de rastreamento de uso entre equipes
* Desejam alternar dinamicamente entre modelos
* Exigem limitação de taxa personalizada ou orçamentos
* Precisam de gerenciamento centralizado de autenticação

## Depuração

Ao depurar sua implantação:

* Use o [comando de barra](/pt/slash-commands) `claude /status`. Este comando fornece observabilidade em qualquer autenticação, proxy e configurações de URL aplicadas.
* Defina a variável de ambiente `export ANTHROPIC_LOG=debug` para registrar solicitações.

## Melhores práticas para organizações

### 1. Invista em documentação e memória

Recomendamos fortemente investir em documentação para que Claude Code entenda sua base de código. As organizações podem implantar arquivos CLAUDE.md em vários níveis:

* **Em toda a organização**: Implante em diretórios do sistema como `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) para padrões de toda a empresa
* **Nível de repositório**: Crie arquivos `CLAUDE.md` nas raízes dos repositórios contendo arquitetura do projeto, comandos de compilação e diretrizes de contribuição. Verifique-os no controle de origem para que todos os usuários se beneficiem

  [Saiba mais](/pt/memory).

### 2. Simplifique a implantação

Se você tiver um ambiente de desenvolvimento personalizado, descobrimos que criar uma maneira "com um clique" de instalar Claude Code é fundamental para aumentar a adoção em toda a organização.

### 3. Comece com uso orientado

Incentive novos usuários a experimentar Claude Code para perguntas sobre a base de código, ou em correções de bugs menores ou solicitações de recursos. Peça ao Claude Code para fazer um plano. Verifique as sugestões do Claude e forneça feedback se estiver fora do caminho. Com o tempo, conforme os usuários entendem melhor esse novo paradigma, eles serão mais eficazes em permitir que Claude Code funcione de forma mais autônoma.

### 4. Configure políticas de segurança

As equipes de segurança podem configurar permissões gerenciadas para o que Claude Code é e não é permitido fazer, o que não pode ser substituído pela configuração local. [Saiba mais](/pt/security).

### 5. Aproveite MCP para integrações

MCP é uma ótima maneira de dar ao Claude Code mais informações, como conectar a sistemas de gerenciamento de tickets ou logs de erros. Recomendamos que uma equipe central configure servidores MCP e verifique uma configuração `.mcp.json` na base de código para que todos os usuários se beneficiem. [Saiba mais](/pt/mcp).

Na Anthropic, confiamos que Claude Code impulsione o desenvolvimento em todas as bases de código da Anthropic. Esperamos que você goste de usar Claude Code tanto quanto nós.

## Próximas etapas

* [Configure Amazon Bedrock](/pt/amazon-bedrock) para implantação nativa do AWS
* [Configure Google Vertex AI](/pt/google-vertex-ai) para implantação GCP
* [Configure Microsoft Foundry](/pt/microsoft-foundry) para implantação do Azure
* [Configure Rede Empresarial](/pt/network-config) para requisitos de rede
* [Implante Gateway LLM](/pt/llm-gateway) para gerenciamento empresarial
* [Configurações](/pt/settings) para opções de configuração e variáveis de ambiente
