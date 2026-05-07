> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configuração do gateway LLM

> Saiba como configurar Claude Code para trabalhar com soluções de gateway LLM. Abrange requisitos de gateway, configuração de autenticação, seleção de modelo e configuração de endpoint específica do provedor.

Gateways LLM fornecem uma camada proxy centralizada entre Claude Code e provedores de modelos, frequentemente fornecendo:

* **Autenticação centralizada** - Ponto único para gerenciamento de chaves de API
* **Rastreamento de uso** - Monitore o uso em equipes e projetos
* **Controles de custo** - Implemente orçamentos e limites de taxa
* **Registro de auditoria** - Rastreie todas as interações de modelo para conformidade
* **Roteamento de modelo** - Alterne entre provedores sem alterações de código

## Requisitos do gateway

Para que um gateway LLM funcione com Claude Code, ele deve atender aos seguintes requisitos:

**Formato de API**

O gateway deve expor aos clientes pelo menos um dos seguintes formatos de API:

1. **Anthropic Messages**: `/v1/messages`, `/v1/messages/count_tokens`
   * Deve encaminhar cabeçalhos de solicitação: `anthropic-beta`, `anthropic-version`

2. **Bedrock InvokeModel**: `/invoke`, `/invoke-with-response-stream`
   * Deve preservar campos do corpo da solicitação: `anthropic_beta`, `anthropic_version`

3. **Vertex rawPredict**: `:rawPredict`, `:streamRawPredict`, `/count-tokens:rawPredict`
   * Deve encaminhar cabeçalhos de solicitação: `anthropic-beta`, `anthropic-version`

A falha ao encaminhar cabeçalhos ou preservar campos do corpo pode resultar em funcionalidade reduzida ou incapacidade de usar recursos do Claude Code.

<Note>
  Claude Code determina quais recursos ativar com base no formato da API. Ao usar o formato Anthropic Messages com Bedrock ou Vertex, você pode precisar definir a variável de ambiente `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`.
</Note>

**Cabeçalhos de solicitação**

Claude Code inclui os seguintes cabeçalhos em cada solicitação de API:

| Cabeçalho                  | Descrição                                                                                                                                                                             |
| :------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `X-Claude-Code-Session-Id` | Um identificador único para a sessão atual do Claude Code. Proxies podem usar isso para agregar todas as solicitações de API de uma única sessão sem analisar o corpo da solicitação. |

Claude Code também adiciona um bloco de atribuição curto ao prompt do sistema contendo a versão do cliente e uma impressão digital derivada da conversa. A API Anthropic remove este bloco antes do processamento, portanto não afeta o cache de prompt de primeira parte. Se seu gateway implementa seu próprio cache de prompt com chave no corpo completo da solicitação, defina [`CLAUDE_CODE_ATTRIBUTION_HEADER=0`](/pt/env-vars) para omiti-lo.

## Configuração

### Seleção de modelo

Por padrão, Claude Code usa nomes de modelo padrão para o formato de API selecionado.

Quando `ANTHROPIC_BASE_URL` aponta para um gateway que expõe o formato Anthropic Messages, Claude Code consulta o endpoint `/v1/models` do gateway na inicialização e adiciona os modelos retornados ao seletor `/model`. Defina `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` para ativar isso. A descoberta está desativada por padrão para que gateways apoiados por uma chave de API compartilhada não exponham todos os modelos que a chave pode acessar para cada usuário. Cada entrada descoberta é rotulada como "From gateway" e usa o campo `display_name` da resposta quando um é fornecido. Isso requer Claude Code v2.1.129 ou posterior.

A descoberta se aplica apenas ao formato Anthropic Messages. Ela não é executada para endpoints de passagem Bedrock ou Vertex, e não é executada quando `ANTHROPIC_BASE_URL` não está definido ou aponta para `api.anthropic.com`.

A solicitação de descoberta autentica da mesma forma que as solicitações de inferência: ela envia `ANTHROPIC_AUTH_TOKEN` como um token de portador, ou `ANTHROPIC_API_KEY` como o cabeçalho `x-api-key` quando nenhum token de autenticação está definido, junto com quaisquer cabeçalhos de `ANTHROPIC_CUSTOM_HEADERS`. Apenas modelos cujo ID começa com `claude` ou `anthropic` são adicionados ao seletor. Os resultados são armazenados em cache em `~/.claude/cache/gateway-models.json` e atualizados a cada inicialização. Se a solicitação falhar ou o gateway não implementar `/v1/models`, o seletor volta para a lista em cache da inicialização anterior ou para a lista de modelos integrada.

Se seu gateway usa nomes de modelo que não correspondem ao filtro de descoberta, use as variáveis de ambiente documentadas em [Configuração de modelo](/pt/model-config) para adicioná-los manualmente.

## Configuração do LiteLLM

<Warning>
  As versões PyPI do LiteLLM 1.82.7 e 1.82.8 foram comprometidas com malware que rouba credenciais. Não instale essas versões. Se você já as instalou:

  * Remova o pacote
  * Rotacione todas as credenciais nos sistemas afetados
  * Siga as etapas de remediação em [BerriAI/litellm#24518](https://github.com/BerriAI/litellm/issues/24518)

  LiteLLM é um serviço proxy de terceiros. Anthropic não endossa, mantém ou audita a segurança ou funcionalidade do LiteLLM. Este guia é fornecido para fins informativos e pode ficar desatualizado. Use por sua conta e risco.
</Warning>

### Pré-requisitos

* Claude Code atualizado para a versão mais recente
* LiteLLM Proxy Server implantado e acessível
* Acesso aos modelos Claude através do seu provedor escolhido

### Configuração básica do LiteLLM

**Configure Claude Code**:

#### Métodos de autenticação

##### Chave de API estática

Método mais simples usando uma chave de API fixa:

```bash theme={null}
# Defina no ambiente
export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key

# Ou nas configurações do Claude Code
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-litellm-static-key"
  }
}
```

Este valor será enviado como o cabeçalho `Authorization`.

##### Chave de API dinâmica com auxiliar

Para chaves rotativas ou autenticação por usuário:

1. Crie um script auxiliar de chave de API:

```bash theme={null}
#!/bin/bash
# ~/bin/get-litellm-key.sh

# Exemplo: Buscar chave do cofre
vault kv get -field=api_key secret/litellm/claude-code

# Exemplo: Gerar token JWT
jwt encode \
  --secret="${JWT_SECRET}" \
  --exp="+1h" \
  '{"user":"'${USER}'","team":"engineering"}'
```

2. Configure as configurações do Claude Code para usar o auxiliar:

```json theme={null}
{
  "apiKeyHelper": "~/bin/get-litellm-key.sh"
}
```

3. Defina o intervalo de atualização de token:

```bash theme={null}
# Atualizar a cada hora (3600000 ms)
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000
```

Este valor será enviado como cabeçalhos `Authorization` e `X-Api-Key`. O `apiKeyHelper` tem precedência menor que `ANTHROPIC_AUTH_TOKEN` ou `ANTHROPIC_API_KEY`.

#### Endpoint unificado (recomendado)

Usando o [endpoint de formato Anthropic](https://docs.litellm.ai/docs/anthropic_unified) do LiteLLM:

```bash theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000
```

**Benefícios do endpoint unificado sobre endpoints pass-through:**

* Balanceamento de carga
* Fallbacks
* Suporte consistente para rastreamento de custo e rastreamento de usuário final

#### Endpoints pass-through específicos do provedor (alternativa)

##### Claude API através do LiteLLM

Usando [endpoint pass-through](https://docs.litellm.ai/docs/pass_through/anthropic_completion):

```bash theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic
```

##### Amazon Bedrock através do LiteLLM

Usando [endpoint pass-through](https://docs.litellm.ai/docs/pass_through/bedrock):

```bash theme={null}
export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1
```

##### Google Vertex AI através do LiteLLM

Usando [endpoint pass-through](https://docs.litellm.ai/docs/pass_through/vertex_ai):

```bash theme={null}
export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
```

Para informações mais detalhadas, consulte a [documentação do LiteLLM](https://docs.litellm.ai/).

## Recursos adicionais

* [Documentação do LiteLLM](https://docs.litellm.ai/)
* [Configurações do Claude Code](/pt/settings)
* [Configuração de rede corporativa](/pt/network-config)
* [Visão geral de integrações de terceiros](/pt/third-party-integrations)
