> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code no Amazon Bedrock

> Saiba como configurar Claude Code através do Amazon Bedrock, incluindo configuração, configuração de IAM e resolução de problemas.

export const ContactSalesCard = ({surface}) => {
  const utm = content => `utm_source=claude_code&utm_medium=docs&utm_content=${surface}_${content}`;
  const iconArrowRight = (size = 13) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="5" y1="12" x2="19" y2="12" />
      <polyline points="12 5 19 12 12 19" />
    </svg>;
  const STYLES = `
.cc-cs {
  --cs-slate: #141413;
  --cs-clay: #d97757;
  --cs-clay-deep: #c6613f;
  --cs-gray-000: #ffffff;
  --cs-gray-700: #3d3d3a;
  --cs-border-default: rgba(31, 30, 29, 0.15);
  font-family: inherit;
}
.dark .cc-cs {
  --cs-slate: #f0eee6;
  --cs-gray-000: #262624;
  --cs-gray-700: #bfbdb4;
  --cs-border-default: rgba(240, 238, 230, 0.14);
}
.cc-cs-card {
  display: flex; align-items: center; justify-content: space-between;
  gap: 16px; padding: 14px 16px; margin: 0;
  background: var(--cs-gray-000); border: 0.5px solid var(--cs-border-default);
  border-radius: 8px; flex-wrap: wrap;
}
.cc-cs-text { font-size: 13px; color: var(--cs-gray-700); line-height: 1.5; flex: 1; min-width: 240px; }
.cc-cs-text strong { font-weight: 550; color: var(--cs-slate); }
.cc-cs-actions { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.cc-cs-btn-clay {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--cs-clay-deep); color: #fff; border: none;
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
  transition: background-color 0.15s; white-space: nowrap;
}
.cc-cs-btn-clay:hover { background: var(--cs-clay); }
.cc-cs-btn-ghost {
  display: inline-flex; align-items: center; gap: 8px;
  background: transparent; color: var(--cs-gray-700);
  border: 0.5px solid var(--cs-border-default);
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
}
.cc-cs-btn-ghost:hover { background: rgba(0, 0, 0, 0.04); }
.dark .cc-cs-btn-ghost:hover { background: rgba(255, 255, 255, 0.04); }
@media (max-width: 720px) {
  .cc-cs-actions { width: 100%; }
}
`;
  return <div className="cc-cs not-prose">
      <style>{STYLES}</style>
      <div className="cc-cs-card">
        <div className="cc-cs-text">
          <strong>Deploying Claude Code across your organization?</strong> Talk to sales about enterprise plans, SSO, and centralized billing.
        </div>
        <div className="cc-cs-actions">
          <a href={`https://claude.com/pricing?${utm('view_plans')}#plans-business`} className="cc-cs-btn-ghost">
            View plans
          </a>
          <a href={`https://claude.com/contact-sales?${utm('contact_sales')}`} className="cc-cs-btn-clay">
            Contact sales {iconArrowRight()}
          </a>
        </div>
      </div>
    </div>;
};

<ContactSalesCard surface="bedrock" />

## Pré-requisitos

Antes de configurar Claude Code com Bedrock, certifique-se de que você tem:

* Uma conta AWS com acesso ao Bedrock habilitado
* Acesso aos modelos Claude desejados (por exemplo, Claude Sonnet 4.6) no Bedrock
* AWS CLI instalado e configurado (opcional - necessário apenas se você não tiver outro mecanismo para obter credenciais)
* Permissões IAM apropriadas

Para entrar com suas próprias credenciais do Bedrock, siga [Entrar com Bedrock](#sign-in-with-bedrock) abaixo. Para implantar Claude Code em toda uma equipe, use as etapas de [configuração manual](#set-up-manually) e [fixe suas versões de modelo](#4-pin-model-versions) antes de fazer o lançamento.

## Entrar com Bedrock

Se você tem credenciais AWS e quer começar a usar Claude Code através do Bedrock, o assistente de login o guia através disso. Você completa os pré-requisitos do lado AWS uma vez por conta; o assistente cuida do lado do Claude Code.

<Steps>
  <Step title="Habilitar modelos Anthropic em sua conta AWS">
    No [console do Amazon Bedrock](https://console.aws.amazon.com/bedrock/), abra o catálogo de modelos, selecione um modelo Anthropic e envie o formulário de caso de uso. O acesso é concedido imediatamente após o envio. Veja [Enviar detalhes do caso de uso](#1-submit-use-case-details) para AWS Organizations e [configuração de IAM](#iam-configuration) para as permissões que sua função precisa.
  </Step>

  <Step title="Iniciar Claude Code e escolher Bedrock">
    Execute `claude`. No prompt de login, selecione **plataforma de terceiros**, depois **Amazon Bedrock**.
  </Step>

  <Step title="Seguir os prompts do assistente">
    Escolha como você se autentica na AWS: um perfil AWS detectado do seu diretório `~/.aws`, uma chave de API do Bedrock, uma chave de acesso e segredo, ou credenciais já em seu ambiente. O assistente pega sua região, verifica quais modelos Claude sua conta pode invocar e permite que você os fixe. Ele salva o resultado no bloco `env` do seu [arquivo de configurações do usuário](/pt/settings), para que você não precise exportar variáveis de ambiente você mesmo.
  </Step>
</Steps>

Depois de entrar, execute `/setup-bedrock` a qualquer momento para reabrir o assistente e alterar suas credenciais, região ou fixações de modelo.

## Configurar manualmente

Para configurar Bedrock através de variáveis de ambiente em vez do assistente, por exemplo em CI ou um lançamento empresarial com script, siga as etapas abaixo.

### 1. Enviar detalhes do caso de uso

Os usuários pela primeira vez dos modelos Anthropic são obrigados a enviar detalhes do caso de uso antes de invocar um modelo. Isso é feito uma vez por conta AWS.

1. Certifique-se de que você tem as permissões IAM corretas descritas abaixo
2. Navegue até o [console do Amazon Bedrock](https://console.aws.amazon.com/bedrock/)
3. Selecione um modelo Anthropic do **catálogo de modelos**
4. Complete o formulário de caso de uso. O acesso é concedido imediatamente após o envio.

Se você usar AWS Organizations, você pode enviar o formulário uma vez da conta de gerenciamento usando a [API `PutUseCaseForModelAccess`](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_PutUseCaseForModelAccess.html). Esta chamada requer a permissão IAM `bedrock:PutUseCaseForModelAccess`. A aprovação se estende às contas filhas automaticamente.

### 2. Configurar credenciais AWS

Claude Code usa a cadeia de credenciais padrão do AWS SDK. Configure suas credenciais usando um destes métodos:

**Opção A: Configuração da AWS CLI**

```bash theme={null}
aws configure
```

**Opção B: Variáveis de ambiente (chave de acesso)**

```bash theme={null}
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token
```

**Opção C: Variáveis de ambiente (perfil SSO)**

```bash theme={null}
aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name
```

**Opção D: Credenciais do AWS Management Console**

```bash theme={null}
aws login
```

[Saiba mais](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html) sobre `aws login`.

**Opção E: Chaves de API do Bedrock**

```bash theme={null}
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

As chaves de API do Bedrock fornecem um método de autenticação mais simples sem precisar de credenciais AWS completas. [Saiba mais sobre chaves de API do Bedrock](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/).

#### Configuração avançada de credenciais

Claude Code suporta atualização automática de credenciais para AWS SSO e provedores de identidade corporativa. Adicione estas configurações ao seu arquivo de configurações do Claude Code (veja [Configurações](/pt/settings) para localizações de arquivo).

Estas duas configurações têm diferentes condições de acionamento:

* **`awsAuthRefresh`**: executa apenas quando Claude Code detecta que suas credenciais AWS expiraram, localmente com base em seu timestamp ou quando Bedrock retorna um erro de credencial, depois tenta novamente a solicitação com credenciais atualizadas.
* **`awsCredentialExport`**: executa no início da sessão e em cada recarga de credencial, mesmo quando as credenciais em sua cadeia de provedor de credenciais padrão AWS ainda são válidas. Use isso quando sua conta Bedrock requer credenciais entre contas que diferem das que a cadeia de provedor padrão resolveria.

##### Exemplo de configuração

```json theme={null}
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": {
    "AWS_PROFILE": "myprofile"
  }
}
```

##### Configurações explicadas

**`awsAuthRefresh`**: Use isso para comandos que modificam o diretório `.aws`, como atualizar credenciais, cache SSO ou arquivos de configuração. A saída do comando é exibida ao usuário, mas entrada interativa não é suportada. Isso funciona bem para fluxos SSO baseados em navegador onde a CLI exibe uma URL ou código e você completa a autenticação no navegador.

**`awsCredentialExport`**: Use apenas se você não puder modificar `.aws` e deve retornar credenciais diretamente. Este comando é executado sempre que as credenciais precisam ser atualizadas, não apenas quando as credenciais expiram. A saída é capturada silenciosamente e não é mostrada ao usuário. O comando deve gerar JSON neste formato:

```json theme={null}
{
  "Credentials": {
    "AccessKeyId": "value",
    "SecretAccessKey": "value",
    "SessionToken": "value"
  }
}
```

### 3. Configurar Claude Code

Defina as seguintes variáveis de ambiente para habilitar Bedrock:

```bash theme={null}
# Habilitar integração Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # ou sua região preferida

# Opcional: Substituir a região AWS para o modelo pequeno/rápido (Bedrock e Mantle).
# No Bedrock, não tem efeito sem ANTHROPIC_DEFAULT_HAIKU_MODEL
# ou o ANTHROPIC_SMALL_FAST_MODEL definido (descontinuado).
export ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION=us-west-2

# Opcional: Substituir a URL do endpoint Bedrock para endpoints personalizados ou gateways
# export ANTHROPIC_BEDROCK_BASE_URL=https://bedrock-runtime.us-east-1.amazonaws.com
```

Ao habilitar Bedrock para Claude Code, tenha em mente o seguinte:

* `AWS_REGION` é uma variável de ambiente obrigatória. Claude Code não lê do arquivo de configuração `.aws` para esta configuração.
* Ao usar Bedrock, os comandos `/login` e `/logout` são desabilitados, pois a autenticação é tratada através de credenciais AWS.
* Você pode usar arquivos de configurações para variáveis de ambiente como `AWS_PROFILE` que você não quer vazar para outros processos. Veja [Configurações](/pt/settings) para mais informações.

### 4. Fixar versões de modelo

<Warning>
  Fixe versões de modelo específicas ao implantar para vários usuários. Sem fixação, aliases de modelo como `sonnet` e `opus` resolvem para a versão mais recente, que pode não estar disponível em sua conta Bedrock quando Anthropic lançar uma atualização. Claude Code [volta](#startup-model-checks) para a versão anterior na inicialização quando a versão mais recente não está disponível, mas fixação permite que você controle quando seus usuários se movem para um novo modelo.
</Warning>

Defina estas variáveis de ambiente para IDs de modelo Bedrock específicos.

Sem `ANTHROPIC_DEFAULT_OPUS_MODEL`, o alias `opus` no Bedrock resolve para Opus 4.6. Defina-o para o ID do Opus 4.7 para usar o modelo mais recente:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
```

Estas variáveis usam IDs de perfil de inferência entre regiões (com o prefixo `us.`). Se você usar um prefixo de região diferente ou perfis de inferência de aplicação, ajuste de acordo. Para IDs de modelo atuais e legados, veja [Visão geral de modelos](https://platform.claude.com/docs/en/about-claude/models/overview). Veja [Configuração de modelo](/pt/model-config#pin-models-for-third-party-deployments) para a lista completa de variáveis de ambiente.

Claude Code usa estes modelos padrão quando nenhuma variável de fixação está definida:

| Tipo de modelo        | Valor padrão                                   |
| :-------------------- | :--------------------------------------------- |
| Modelo primário       | `us.anthropic.claude-sonnet-4-5-20250929-v1:0` |
| Modelo pequeno/rápido | Mesmo que o modelo primário                    |

Tarefas em segundo plano, como geração de título de sessão, usam o modelo pequeno/rápido, normalmente um modelo da classe Haiku. No Bedrock, Claude Code padroniza isso para o modelo primário porque Haiku pode não estar habilitado em todas as contas ou regiões. Para usar Haiku para tarefas em segundo plano, defina `ANTHROPIC_DEFAULT_HAIKU_MODEL` para um ID de modelo que está disponível em sua conta.

Para personalizar modelos ainda mais, use um destes métodos:

```bash theme={null}
# Usando ID de perfil de inferência
export ANTHROPIC_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'

# Usando ARN de perfil de inferência de aplicação
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# Opcional: Desabilitar cache de prompt se necessário
export DISABLE_PROMPT_CACHING=1

# Opcional: Solicitar TTL de cache de prompt de 1 hora em vez do padrão de 5 minutos
export ENABLE_PROMPT_CACHING_1H=1
```

O TTL de cache de 1 hora é cobrado a uma taxa mais alta do que o padrão de 5 minutos. Veja [tempo de vida do cache](/pt/prompt-caching#cache-lifetime).

<Note>O cache de prompt pode não estar disponível em todas as regiões do Bedrock. Se as contagens de tokens de cache permanecerem em zero, verifique [modelos, regiões e limites suportados](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html#prompt-caching-models) na documentação do Bedrock.</Note>

#### Mapear cada versão de modelo para um perfil de inferência

As variáveis de ambiente `ANTHROPIC_DEFAULT_*_MODEL` configuram um perfil de inferência por família de modelo. Se sua organização precisa expor várias versões da mesma família no seletor `/model`, cada uma roteada para seu próprio ARN de perfil de inferência de aplicação, use a configuração `modelOverrides` em seu [arquivo de configurações](/pt/settings#settings-files) em vez disso.

Este exemplo mapeia quatro versões de Opus para ARNs distintos para que os usuários possam alternar entre elas sem contornar os perfis de inferência de sua organização:

```json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-7": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-47-prod",
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-opus-4-1-20250805": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-41-prod"
  }
}
```

Quando um usuário seleciona uma dessas versões em `/model`, Claude Code chama Bedrock com o ARN mapeado. Versões sem uma substituição voltam para o ID de modelo Bedrock integrado ou qualquer perfil de inferência correspondente descoberto na inicialização. Veja [Substituir IDs de modelo por versão](/pt/model-config#override-model-ids-per-version) para detalhes sobre como as substituições interagem com `availableModels` e outras configurações de modelo.

## Verificações de modelo na inicialização

Quando Claude Code inicia com Bedrock configurado, ele verifica que os modelos que pretende usar estão acessíveis em sua conta. Esta verificação requer Claude Code v2.1.94 ou posterior.

Se você fixou uma versão de modelo que é mais antiga do que o padrão atual do Claude Code, e sua conta pode invocar a versão mais recente, Claude Code o solicita a atualizar a fixação. Aceitar escreve o novo ID de modelo em seu [arquivo de configurações do usuário](/pt/settings) e reinicia Claude Code. Recusar é lembrado até a próxima mudança de versão padrão. Fixações que apontam para um [ARN de perfil de inferência de aplicação](#map-each-model-version-to-an-inference-profile) são ignoradas, pois são gerenciadas pelo seu administrador.

Se você não fixou um modelo e o padrão atual não está disponível em sua conta, Claude Code volta para a versão anterior para a sessão atual e mostra um aviso. O fallback não é persistido. Habilite o modelo mais recente em sua conta Bedrock ou [fixe uma versão](#4-pin-model-versions) para tornar a escolha permanente.

## Configuração de IAM

Crie uma política de IAM com as permissões necessárias para Claude Code:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowModelAndInferenceProfileAccess",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListInferenceProfiles",
        "bedrock:GetInferenceProfile"
      ],
      "Resource": [
        "arn:aws:bedrock:*:*:inference-profile/*",
        "arn:aws:bedrock:*:*:application-inference-profile/*",
        "arn:aws:bedrock:*:*:foundation-model/*"
      ]
    },
    {
      "Sid": "AllowMarketplaceSubscription",
      "Effect": "Allow",
      "Action": [
        "aws-marketplace:ViewSubscriptions",
        "aws-marketplace:Subscribe"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:CalledViaLast": "bedrock.amazonaws.com"
        }
      }
    }
  ]
}
```

Para permissões mais restritivas, você pode limitar o Resource para ARNs de perfil de inferência específicos.

`bedrock:GetInferenceProfile` permite que Claude Code resolva um [ARN de perfil de inferência de aplicação](#map-each-model-version-to-an-inference-profile) para seu modelo de fundação de suporte, que é usado para selecionar a forma de solicitação correta para esse modelo.

Se o token não tiver essa permissão, Claude Code se recupera automaticamente tentando novamente uma vez com a forma alternativa, portanto as solicitações ainda têm sucesso, mas cada novo modelo adiciona uma viagem extra. Conceder a permissão evita a tentativa novamente. Isso se aplica com mais frequência a implantações `AWS_BEARER_TOKEN_BEDROCK`, onde a política do token é normalmente mais restrita do que uma função IAM completa.

Para detalhes, veja [documentação de IAM do Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html).

<Note>
  Crie uma conta AWS dedicada para Claude Code para simplificar o rastreamento de custos e controle de acesso.
</Note>

## Janela de contexto de 1M de tokens

Claude Opus 4.7, Opus 4.6 e Sonnet 4.6 suportam a [janela de contexto de 1M de tokens](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) no Amazon Bedrock. Claude Code habilita automaticamente a janela de contexto estendida quando você seleciona uma variante de modelo de 1M.

O [assistente de configuração](#sign-in-with-bedrock) oferece uma opção de contexto de 1M quando fixa modelos. Para habilitá-lo para um modelo fixado manualmente em vez disso, acrescente `[1m]` ao ID do modelo. Veja [Fixar modelos para implantações de terceiros](/pt/model-config#pin-models-for-third-party-deployments) para detalhes.

## Camadas de serviço

[Camadas de serviço do Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html) permitem que você negocie custo contra latência. Defina `ANTHROPIC_BEDROCK_SERVICE_TIER` como `default`, `flex` ou `priority`:

```bash theme={null}
export ANTHROPIC_BEDROCK_SERVICE_TIER=priority
```

Claude Code envia isso como o cabeçalho `X-Amzn-Bedrock-Service-Tier` em cada solicitação. A disponibilidade de camada varia por modelo e região. A capacidade reservada usa um [ARN de throughput provisionado](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html) como o ID do modelo em vez desta configuração.

## AWS Guardrails

[Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) permitem que você implemente filtragem de conteúdo para Claude Code. Crie um Guardrail no [console do Amazon Bedrock](https://console.aws.amazon.com/bedrock/), publique uma versão, então adicione os cabeçalhos do Guardrail ao seu [arquivo de configurações](/pt/settings). Habilite inferência entre regiões em seu Guardrail se você estiver usando perfis de inferência entre regiões.

Exemplo de configuração:

```json theme={null}
{
  "env": {
    "ANTHROPIC_CUSTOM_HEADERS": "X-Amzn-Bedrock-GuardrailIdentifier: your-guardrail-id\nX-Amzn-Bedrock-GuardrailVersion: 1"
  }
}
```

## Usar o endpoint Mantle

Mantle é um endpoint do Amazon Bedrock que serve modelos Claude através da forma de API Anthropic nativa em vez da API Invoke do Bedrock. Ele usa as mesmas credenciais AWS, permissões IAM e configuração `awsAuthRefresh` descritas anteriormente nesta página.

<Note>
  Mantle requer Claude Code v2.1.94 ou posterior. Execute `claude --version` para verificar.
</Note>

### Habilitar Mantle

Com credenciais AWS já configuradas, defina `CLAUDE_CODE_USE_MANTLE` para rotear solicitações para o endpoint Mantle:

```bash theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export AWS_REGION=us-east-1
```

Claude Code constrói a URL do endpoint a partir de `AWS_REGION`. Para substituí-la por um endpoint personalizado ou gateway, defina `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`.

Execute `/status` dentro do Claude Code para confirmar. A linha do provedor mostra `Amazon Bedrock (Mantle)` quando Mantle está ativo.

### Selecionar um modelo Mantle

Mantle usa IDs de modelo com prefixo `anthropic.` e sem sufixo de versão, por exemplo `anthropic.claude-haiku-4-5`. Os modelos disponíveis para sua conta dependem do que sua organização foi concedida; IDs de modelo adicionais estão listados em seus materiais de integração da AWS. Entre em contato com sua equipe de conta AWS para solicitar acesso aos modelos permitidos.

Defina o modelo com a flag `--model` ou com `/model` dentro do Claude Code:

```bash theme={null}
claude --model anthropic.claude-haiku-4-5
```

### Executar Mantle junto com a API Invoke

Os modelos disponíveis para você no Mantle podem não incluir todos os modelos que você usa hoje. Definir tanto `CLAUDE_CODE_USE_BEDROCK` quanto `CLAUDE_CODE_USE_MANTLE` permite que Claude Code chame ambos os endpoints da mesma sessão. IDs de modelo que correspondem ao formato Mantle são roteados para Mantle, e todos os outros IDs de modelo vão para a API Invoke do Bedrock.

```bash theme={null}
export CLAUDE_CODE_USE_BEDROCK=1
export CLAUDE_CODE_USE_MANTLE=1
```

Para exibir um modelo Mantle no seletor `/model`, liste seu ID em `availableModels` em seu [arquivo de configurações](/pt/settings). Esta configuração também restringe o seletor às entradas listadas, então inclua cada alias que você quer manter disponível:

```json theme={null}
{
  "availableModels": ["opus", "sonnet", "haiku", "anthropic.claude-haiku-4-5"]
}
```

Entradas com o prefixo `anthropic.` são adicionadas como opções de seletor personalizadas e roteadas para Mantle. Substitua `anthropic.claude-haiku-4-5` pelo ID de modelo que sua conta foi concedida. Veja [Restringir seleção de modelo](/pt/model-config#restrict-model-selection) para como `availableModels` interage com outras configurações de modelo.

Quando ambos os provedores estão ativos, `/status` mostra `Amazon Bedrock + Amazon Bedrock (Mantle)`.

### Rotear Mantle através de um gateway

Se sua organização roteia tráfego de modelo através de um [gateway LLM](/pt/llm-gateway) centralizado que injeta credenciais AWS no lado do servidor, desabilite a autenticação no lado do cliente para que Claude Code envie solicitações sem assinaturas SigV4 ou cabeçalhos `x-api-key`:

```bash theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export CLAUDE_CODE_SKIP_MANTLE_AUTH=1
export ANTHROPIC_BEDROCK_MANTLE_BASE_URL=https://your-gateway.example.com
```

### Variáveis de ambiente Mantle

Estas variáveis são específicas para o endpoint Mantle. Veja [Variáveis de ambiente](/pt/env-vars) para a lista completa.

| Variável                                | Propósito                                                                       |
| :-------------------------------------- | :------------------------------------------------------------------------------ |
| `CLAUDE_CODE_USE_MANTLE`                | Habilitar o endpoint Mantle. Defina como `1` ou `true`.                         |
| `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`     | Substituir a URL do endpoint Mantle padrão                                      |
| `CLAUDE_CODE_SKIP_MANTLE_AUTH`          | Pular autenticação no lado do cliente para configurações de proxy               |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` | Substituir região AWS para o modelo da classe Haiku (compartilhado com Bedrock) |

## Resolução de problemas

### Loop de autenticação com SSO e proxies corporativos

Se abas do navegador aparecem repetidamente ao usar AWS SSO, remova a configuração `awsAuthRefresh` do seu [arquivo de configurações](/pt/settings). Isso pode ocorrer quando VPNs corporativas ou proxies de inspeção TLS interrompem o fluxo do navegador SSO. Claude Code trata a conexão interrompida como uma falha de autenticação, executa novamente `awsAuthRefresh` e entra em loop indefinidamente.

Se seu ambiente de rede interfere com fluxos SSO automáticos baseados em navegador, use `aws sso login` manualmente antes de iniciar Claude Code em vez de depender de `awsAuthRefresh`.

### Problemas de região

Se você encontrar problemas de região:

* Verifique disponibilidade de modelo: `aws bedrock list-inference-profiles --region your-region`
* Mude para uma região suportada: `export AWS_REGION=us-east-1`
* Considere usar perfis de inferência para acesso entre regiões

Se você receber um erro "on-demand throughput isn't supported":

* Especifique o modelo como um ID de [perfil de inferência](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)

Claude Code usa a [API Invoke](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) do Bedrock e não suporta a API Converse.

### Erros de endpoint Mantle

Se `/status` não mostra `Amazon Bedrock (Mantle)` depois que você defina `CLAUDE_CODE_USE_MANTLE`, a variável não está chegando ao processo. Confirme que ela é exportada no shell onde você lançou `claude`, ou defina-a no bloco `env` do seu [arquivo de configurações](/pt/settings).

Um `403` do endpoint Mantle com credenciais válidas significa que sua conta AWS não foi concedida acesso ao modelo que você solicitou. Entre em contato com sua equipe de conta AWS para solicitar acesso.

Um `400` que nomeia o ID do modelo significa que esse modelo não é servido no Mantle. Mantle tem seu próprio lineup de modelo separado do catálogo Bedrock padrão, então IDs de perfil de inferência como `us.anthropic.claude-sonnet-4-6` não funcionarão. Use um ID de formato Mantle, ou habilite [ambos os endpoints](#run-mantle-alongside-the-invoke-api) para que Claude Code roteia cada solicitação para o endpoint onde o modelo está disponível.

## Recursos adicionais

* [Documentação do Bedrock](https://docs.aws.amazon.com/bedrock/)
* [Preços do Bedrock](https://aws.amazon.com/bedrock/pricing/)
* [Perfis de inferência do Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Burndown de token do Bedrock e cotas](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas-token-burndown.html)
* [Claude Code no Amazon Bedrock: Guia de Configuração Rápida](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)
* [Implementação de Monitoramento do Claude Code (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)
