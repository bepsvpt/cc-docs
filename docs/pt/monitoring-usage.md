> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Monitoramento

> Saiba como ativar e configurar OpenTelemetry para Claude Code.

Rastreie o uso, custos e atividade de ferramentas do Claude Code em toda a sua organização exportando dados de telemetria através do OpenTelemetry (OTel). Claude Code exporta métricas como dados de série temporal via protocolo de métricas padrão, eventos via protocolo de logs/eventos e, opcionalmente, rastreamentos distribuídos via [protocolo de rastreamentos](#traces-beta). Configure seus backends de métricas, logs e rastreamentos para corresponder aos seus requisitos de monitoramento.

## Início rápido

Configure OpenTelemetry usando variáveis de ambiente:

```bash theme={null}
# 1. Ativar telemetria
export CLAUDE_CODE_ENABLE_TELEMETRY=1

# 2. Escolher exportadores (ambos são opcionais - configure apenas o que você precisa)
export OTEL_METRICS_EXPORTER=otlp       # Opções: otlp, prometheus, console, none
export OTEL_LOGS_EXPORTER=otlp          # Opções: otlp, console, none

# 3. Configurar endpoint OTLP (para exportador OTLP)
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# 4. Definir autenticação (se necessário)
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer your-token"

# 5. Para depuração: reduzir intervalos de exportação
export OTEL_METRIC_EXPORT_INTERVAL=10000  # 10 segundos (padrão: 60000ms)
export OTEL_LOGS_EXPORT_INTERVAL=5000     # 5 segundos (padrão: 5000ms)

# 6. Executar Claude Code
claude
```

<Note>
  Os intervalos de exportação padrão são 60 segundos para métricas e 5 segundos para logs. Durante a configuração, você pode querer usar intervalos mais curtos para fins de depuração. Lembre-se de redefinir esses valores para uso em produção.
</Note>

Para opções de configuração completas, consulte a [especificação OpenTelemetry](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options).

## Configuração do administrador

Os administradores podem configurar as definições de OpenTelemetry para todos os usuários através do [arquivo de configurações gerenciadas](/pt/settings#settings-files). Isso permite controle centralizado das configurações de telemetria em toda a organização. Consulte a [precedência de configurações](/pt/settings#settings-precedence) para obter mais informações sobre como as configurações são aplicadas.

Exemplo de configuração de configurações gerenciadas:

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.example.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer example-token"
  }
}
```

<Note>
  As configurações gerenciadas podem ser distribuídas via MDM (Mobile Device Management) ou outras soluções de gerenciamento de dispositivos. As variáveis de ambiente definidas no arquivo de configurações gerenciadas têm alta precedência e não podem ser substituídas pelos usuários.
</Note>

## Detalhes de configuração

### Variáveis de configuração comuns

| Variável de Ambiente                                | Descrição                                                                                                                                                                                                                                                                                                                                                 | Valores de Exemplo                                                                                                                 |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                      | Ativa coleta de telemetria (obrigatório)                                                                                                                                                                                                                                                                                                                  | `1`                                                                                                                                |
| `OTEL_METRICS_EXPORTER`                             | Tipos de exportador de métricas, separados por vírgula. Use `none` para desativar                                                                                                                                                                                                                                                                         | `console`, `otlp`, `prometheus`, `none`                                                                                            |
| `OTEL_LOGS_EXPORTER`                                | Tipos de exportador de logs/eventos, separados por vírgula. Use `none` para desativar                                                                                                                                                                                                                                                                     | `console`, `otlp`, `none`                                                                                                          |
| `OTEL_EXPORTER_OTLP_PROTOCOL`                       | Protocolo para exportador OTLP, aplica-se a todos os sinais                                                                                                                                                                                                                                                                                               | `grpc`, `http/json`, `http/protobuf`                                                                                               |
| `OTEL_EXPORTER_OTLP_ENDPOINT`                       | Endpoint do coletor OTLP para todos os sinais                                                                                                                                                                                                                                                                                                             | `http://localhost:4317`                                                                                                            |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL`               | Protocolo para métricas, substitui configuração geral                                                                                                                                                                                                                                                                                                     | `grpc`, `http/json`, `http/protobuf`                                                                                               |
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`               | Endpoint de métricas OTLP, substitui configuração geral                                                                                                                                                                                                                                                                                                   | `http://localhost:4318/v1/metrics`                                                                                                 |
| `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL`                  | Protocolo para logs, substitui configuração geral                                                                                                                                                                                                                                                                                                         | `grpc`, `http/json`, `http/protobuf`                                                                                               |
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`                  | Endpoint de logs OTLP, substitui configuração geral                                                                                                                                                                                                                                                                                                       | `http://localhost:4318/v1/logs`                                                                                                    |
| `OTEL_EXPORTER_OTLP_HEADERS`                        | Cabeçalhos de autenticação para OTLP                                                                                                                                                                                                                                                                                                                      | `Authorization=Bearer token`                                                                                                       |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY`             | Chave do cliente para autenticação mTLS                                                                                                                                                                                                                                                                                                                   | Caminho para arquivo de chave do cliente                                                                                           |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE`     | Certificado do cliente para autenticação mTLS                                                                                                                                                                                                                                                                                                             | Caminho para arquivo de certificado do cliente                                                                                     |
| `OTEL_METRIC_EXPORT_INTERVAL`                       | Intervalo de exportação em milissegundos (padrão: 60000)                                                                                                                                                                                                                                                                                                  | `5000`, `60000`                                                                                                                    |
| `OTEL_LOGS_EXPORT_INTERVAL`                         | Intervalo de exportação de logs em milissegundos (padrão: 5000)                                                                                                                                                                                                                                                                                           | `1000`, `10000`                                                                                                                    |
| `OTEL_LOG_USER_PROMPTS`                             | Ativar registro de conteúdo de prompt do usuário (padrão: desativado)                                                                                                                                                                                                                                                                                     | `1` para ativar                                                                                                                    |
| `OTEL_LOG_TOOL_DETAILS`                             | Ativar registro de parâmetros de ferramenta e argumentos de entrada em eventos de ferramenta e atributos de span de rastreamento: comandos Bash, nomes de servidor MCP e ferramenta, nomes de skill e entrada de ferramenta. Também ativa nomes de comando customizado, plugin e MCP em eventos `user_prompt` (padrão: desativado)                        | `1` para ativar                                                                                                                    |
| `OTEL_LOG_TOOL_CONTENT`                             | Ativar registro de conteúdo de entrada e saída de ferramenta em eventos de span (padrão: desativado). Requer [rastreamento](#traces-beta). O conteúdo é truncado em 60 KB                                                                                                                                                                                 | `1` para ativar                                                                                                                    |
| `OTEL_LOG_RAW_API_BODIES`                           | Emitir o corpo JSON completo da solicitação e resposta da API Anthropic Messages como eventos de log `api_request_body` / `api_response_body` (padrão: desativado). Os corpos incluem todo o histórico de conversa. Ativar isso implica consentimento para tudo que `OTEL_LOG_USER_PROMPTS`, `OTEL_LOG_TOOL_DETAILS` e `OTEL_LOG_TOOL_CONTENT` revelariam | `1` para corpos inline truncados em 60 KB, ou `file:<dir>` para corpos não truncados em disco com um ponteiro `body_ref` no evento |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` | Preferência de temporalidade de métricas (padrão: `delta`). Defina como `cumulative` se seu backend espera temporalidade cumulativa                                                                                                                                                                                                                       | `delta`, `cumulative`                                                                                                              |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`       | Intervalo para atualizar cabeçalhos dinâmicos (padrão: 1740000ms / 29 minutos)                                                                                                                                                                                                                                                                            | `900000`                                                                                                                           |

### Controle de cardinalidade de métricas

As seguintes variáveis de ambiente controlam quais atributos são incluídos nas métricas para gerenciar a cardinalidade:

| Variável de Ambiente                | Descrição                                                           | Valor Padrão | Exemplo para Desativar |
| ----------------------------------- | ------------------------------------------------------------------- | ------------ | ---------------------- |
| `OTEL_METRICS_INCLUDE_SESSION_ID`   | Incluir atributo session.id em métricas                             | `true`       | `false`                |
| `OTEL_METRICS_INCLUDE_VERSION`      | Incluir atributo app.version em métricas                            | `false`      | `true`                 |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | Incluir atributos user.account\_uuid e user.account\_id em métricas | `true`       | `false`                |

Essas variáveis ajudam a controlar a cardinalidade das métricas, o que afeta os requisitos de armazenamento e o desempenho de consultas no seu backend de métricas. Cardinalidade mais baixa geralmente significa melhor desempenho e custos de armazenamento mais baixos, mas dados menos granulares para análise.

### Rastreamentos (beta)

O rastreamento distribuído exporta spans que vinculam cada prompt do usuário às solicitações de API e execuções de ferramentas que ele dispara, para que você possa visualizar uma solicitação completa como um único rastreamento no seu backend de rastreamento.

O rastreamento está desativado por padrão. Para ativá-lo, defina tanto `CLAUDE_CODE_ENABLE_TELEMETRY=1` quanto `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`, depois defina `OTEL_TRACES_EXPORTER` para escolher para onde os spans são enviados. Os rastreamentos reutilizam a [configuração OTLP comum](#variáveis-de-configuração-comuns) para endpoint, protocolo e cabeçalhos.

| Variável de Ambiente                  | Descrição                                                                                   | Valores de Exemplo                   |
| ------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------ |
| `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` | Ativar rastreamento de span (obrigatório). `ENABLE_ENHANCED_TELEMETRY_BETA` também é aceito | `1`                                  |
| `OTEL_TRACES_EXPORTER`                | Tipos de exportador de rastreamentos, separados por vírgula. Use `none` para desativar      | `console`, `otlp`, `none`            |
| `OTEL_EXPORTER_OTLP_TRACES_PROTOCOL`  | Protocolo para rastreamentos, substitui `OTEL_EXPORTER_OTLP_PROTOCOL`                       | `grpc`, `http/json`, `http/protobuf` |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT`  | Endpoint de rastreamentos OTLP, substitui `OTEL_EXPORTER_OTLP_ENDPOINT`                     | `http://localhost:4318/v1/traces`    |
| `OTEL_TRACES_EXPORT_INTERVAL`         | Intervalo de exportação de lote de span em milissegundos (padrão: 5000)                     | `1000`, `10000`                      |

Os spans reduzem o texto do prompt do usuário, detalhes de entrada de ferramenta e conteúdo de ferramenta por padrão. Defina `OTEL_LOG_USER_PROMPTS=1`, `OTEL_LOG_TOOL_DETAILS=1` e `OTEL_LOG_TOOL_CONTENT=1` para incluí-los.

Quando o rastreamento está ativo, subprocessos Bash e PowerShell herdam automaticamente uma variável de ambiente `TRACEPARENT` contendo o contexto de rastreamento W3C do span de execução de ferramenta ativo. Isso permite que qualquer subprocesso que leia `TRACEPARENT` coloque seus próprios spans sob o mesmo rastreamento, permitindo rastreamento distribuído de ponta a ponta através de scripts e comandos que Claude executa.

No Agent SDK e sessões não-interativas iniciadas com `-p`, Claude Code também lê `TRACEPARENT` e `TRACESTATE` de seu próprio ambiente ao iniciar cada span de interação. Isso permite que um processo de incorporação passe seu contexto de rastreamento W3C ativo para o subprocesso para que os spans do Claude Code apareçam como filhos do rastreamento distribuído do chamador. Sessões interativas ignoram `TRACEPARENT` de entrada para evitar herdar acidentalmente valores ambientes de CI ou ambientes de contêiner.

#### Hierarquia de span

Cada prompt do usuário inicia um span raiz `claude_code.interaction`. Chamadas de API, chamadas de ferramenta e execuções de hook são registradas como seus filhos. Os spans de ferramenta têm dois spans filhos próprios: um para o tempo gasto esperando uma decisão de permissão e outro para a execução em si. Quando a ferramenta Task gera um subagente, os spans de API e ferramenta do subagente se aninham sob o span `claude_code.tool` do pai.

```text theme={null}
claude_code.interaction
├── claude_code.llm_request
├── claude_code.hook                    (requer rastreamento beta detalhado)
└── claude_code.tool
    ├── claude_code.tool.blocked_on_user
    ├── claude_code.tool.execution
    └── (ferramenta Task) spans claude_code.llm_request / claude_code.tool do subagente
```

No Agent SDK e sessões `claude -p`, `claude_code.interaction` em si se torna um filho do span do chamador quando `TRACEPARENT` está definido no ambiente.

#### Atributos de span

Cada span carrega os [atributos padrão](#atributos-padrão) mais um atributo `span.type` correspondendo ao seu nome. As tabelas abaixo listam os atributos adicionais definidos em cada span. Os spans `llm_request`, `tool.execution` e `hook` definem status OpenTelemetry `ERROR` quando registram uma falha; os outros spans sempre terminam com status `UNSET`.

**`claude_code.interaction`**

| Atributo                  | Descrição                                                                  | Controlado Por          |
| ------------------------- | -------------------------------------------------------------------------- | ----------------------- |
| `user_prompt`             | Texto do prompt. O valor é `<REDACTED>` a menos que o gate esteja definido | `OTEL_LOG_USER_PROMPTS` |
| `user_prompt_length`      | Comprimento do prompt em caracteres                                        |                         |
| `interaction.sequence`    | Contador baseado em 1 de interações nesta sessão                           |                         |
| `interaction.duration_ms` | Duração de parede do turno                                                 |                         |

**`claude_code.llm_request`**

| Atributo                         | Descrição                                                                                                         | Controlado Por |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------- | -------------- |
| `model`                          | Identificador do modelo                                                                                           |                |
| `gen_ai.system`                  | Sempre `anthropic`. Convenção semântica GenAI OpenTelemetry                                                       |                |
| `gen_ai.request.model`           | Mesmo valor que `model`. Convenção semântica GenAI OpenTelemetry                                                  |                |
| `query_source`                   | Subsistema que emitiu a solicitação, como `repl_main_thread` ou um nome de subagente                              |                |
| `speed`                          | `fast` ou `normal`                                                                                                |                |
| `llm_request.context`            | `interaction`, `tool` ou `standalone` dependendo do span pai                                                      |                |
| `duration_ms`                    | Duração de parede incluindo tentativas                                                                            |                |
| `ttft_ms`                        | Tempo até o primeiro token em milissegundos                                                                       |                |
| `input_tokens`                   | Contagem de tokens de entrada do bloco de uso da API                                                              |                |
| `output_tokens`                  | Contagem de tokens de saída                                                                                       |                |
| `cache_read_tokens`              | Tokens lidos do cache de prompt                                                                                   |                |
| `cache_creation_tokens`          | Tokens escritos no cache de prompt                                                                                |                |
| `request_id`                     | ID de solicitação da API Anthropic do cabeçalho de resposta `request-id`                                          |                |
| `gen_ai.response.id`             | Mesmo valor que `request_id`. Convenção semântica GenAI OpenTelemetry                                             |                |
| `client_request_id`              | `x-client-request-id` gerado pelo cliente da tentativa final                                                      |                |
| `attempt`                        | Total de tentativas feitas para esta solicitação                                                                  |                |
| `success`                        | `true` ou `false`                                                                                                 |                |
| `status_code`                    | Código de status HTTP quando a solicitação falhou                                                                 |                |
| `error`                          | Mensagem de erro quando a solicitação falhou                                                                      |                |
| `response.has_tool_call`         | `true` quando a resposta continha blocos de uso de ferramenta                                                     |                |
| `stop_reason`                    | API response `stop_reason`, como `end_turn`, `tool_use`, `max_tokens`, `stop_sequence`, `pause_turn` ou `refusal` |                |
| `gen_ai.response.finish_reasons` | Mesmo valor que `stop_reason`, envolvido em um array de string. Convenção semântica GenAI OpenTelemetry           |                |

Cada tentativa de repetição também é registrada como um evento de span `gen_ai.request.attempt` com atributos `attempt` e `client_request_id`.

**`claude_code.tool`**

| Atributo        | Descrição                                                   | Controlado Por          |
| --------------- | ----------------------------------------------------------- | ----------------------- |
| `tool_name`     | Nome da ferramenta                                          |                         |
| `duration_ms`   | Duração de parede incluindo espera de permissão e execução  |                         |
| `result_tokens` | Tamanho aproximado em tokens do resultado da ferramenta     |                         |
| `file_path`     | Caminho de arquivo alvo para ferramentas Read, Edit e Write | `OTEL_LOG_TOOL_DETAILS` |
| `full_command`  | String de comando para a ferramenta Bash                    | `OTEL_LOG_TOOL_DETAILS` |
| `skill_name`    | Nome da skill para a ferramenta Skill                       | `OTEL_LOG_TOOL_DETAILS` |
| `subagent_type` | Tipo de subagente para a ferramenta Task                    | `OTEL_LOG_TOOL_DETAILS` |

Quando `OTEL_LOG_TOOL_CONTENT=1`, este span também registra um evento de span `tool.output` cujos atributos contêm os corpos de entrada e saída da ferramenta, truncados em 60 KB por atributo.

**`claude_code.tool.blocked_on_user`**

| Atributo      | Descrição                                                                              | Controlado Por |
| ------------- | -------------------------------------------------------------------------------------- | -------------- |
| `duration_ms` | Tempo gasto esperando a decisão de permissão                                           |                |
| `decision`    | `accept` ou `reject`                                                                   |                |
| `source`      | Fonte de decisão, correspondendo ao evento [Tool decision event](#tool-decision-event) |                |

**`claude_code.tool.execution`**

| Atributo      | Descrição                                                                                                                                                              | Controlado Por          |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| `duration_ms` | Tempo gasto executando o corpo da ferramenta                                                                                                                           |                         |
| `success`     | `true` ou `false`                                                                                                                                                      |                         |
| `error`       | String de categoria de erro quando a execução falhou, como `Error:ENOENT` ou `ShellError`. Contém a mensagem de erro completa em vez disso quando o gate está definido | `OTEL_LOG_TOOL_DETAILS` |

**`claude_code.hook`**

Este span é emitido apenas quando rastreamento beta detalhado está ativo, o que requer `ENABLE_BETA_TRACING_DETAILED=1` e `BETA_TRACING_ENDPOINT` além da configuração do exportador de rastreamento acima. Em sessões CLI interativas, isso também requer que sua organização esteja na lista de permissões para o recurso. Sessões Agent SDK e não-interativas `-p` não são controladas. Não é emitido quando apenas `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` está definido.

| Atributo                 | Descrição                                                | Controlado Por          |
| ------------------------ | -------------------------------------------------------- | ----------------------- |
| `hook_event`             | Tipo de evento de hook, como `PreToolUse`                |                         |
| `hook_name`              | Nome completo do hook, como `PreToolUse:Write`           |                         |
| `num_hooks`              | Número de comandos de hook correspondentes executados    |                         |
| `hook_definitions`       | Configuração de hook serializada em JSON                 | `OTEL_LOG_TOOL_DETAILS` |
| `duration_ms`            | Duração de parede de todos os hooks correspondentes      |                         |
| `num_success`            | Contagem de hooks que completaram com sucesso            |                         |
| `num_blocking`           | Contagem de hooks que retornaram uma decisão de bloqueio |                         |
| `num_non_blocking_error` | Contagem de hooks que falharam sem bloquear              |                         |
| `num_cancelled`          | Contagem de hooks cancelados antes da conclusão          |                         |

<Note>
  Atributos adicionais que contêm conteúdo, como `new_context`, `system_prompt_preview`, `user_system_prompt`, `tool_input` e `response.model_output`, são emitidos apenas quando rastreamento beta detalhado está ativo. Eles não fazem parte do esquema de span estável. `user_system_prompt` também requer `OTEL_LOG_USER_PROMPTS=1`. Ele carrega apenas o texto do prompt do sistema que você fornece através da opção SDK `systemPrompt` ou dos sinalizadores `--system-prompt` e `--append-system-prompt`, truncado em 60 KB, e é emitido uma vez por sessão em vez de por solicitação.
</Note>

### Cabeçalhos dinâmicos

Para ambientes corporativos que exigem autenticação dinâmica, você pode configurar um script para gerar cabeçalhos dinamicamente:

#### Configuração de configurações

Adicione ao seu `.claude/settings.json`:

```json theme={null}
{
  "otelHeadersHelper": "/bin/generate_opentelemetry_headers.sh"
}
```

#### Requisitos do script

O script deve gerar JSON válido com pares de chave-valor de string representando cabeçalhos HTTP:

```bash theme={null}
#!/bin/bash
# Exemplo: Múltiplos cabeçalhos
echo "{\"Authorization\": \"Bearer $(get-token.sh)\", \"X-API-Key\": \"$(get-api-key.sh)\"}"
```

#### Comportamento de atualização

O script auxiliar de cabeçalhos é executado na inicialização e periodicamente depois para suportar atualização de token. Por padrão, o script é executado a cada 29 minutos. Personalize o intervalo com a variável de ambiente `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`.

### Suporte a organizações multi-equipe

Organizações com múltiplas equipes ou departamentos podem adicionar atributos personalizados para distinguir entre diferentes grupos usando a variável de ambiente `OTEL_RESOURCE_ATTRIBUTES`:

```bash theme={null}
# Adicionar atributos personalizados para identificação de equipe
export OTEL_RESOURCE_ATTRIBUTES="department=engineering,team.id=platform,cost_center=eng-123"
```

Esses atributos personalizados serão incluídos em todas as métricas e eventos, permitindo que você:

* Filtre métricas por equipe ou departamento
* Rastreie custos por centro de custo
* Crie dashboards específicos de equipe
* Configure alertas para equipes específicas

<Warning>
  **Requisitos importantes de formatação para OTEL\_RESOURCE\_ATTRIBUTES:**

  A variável de ambiente `OTEL_RESOURCE_ATTRIBUTES` usa pares chave=valor separados por vírgula com requisitos rigorosos de formatação:

  * **Sem espaços permitidos**: Os valores não podem conter espaços. Por exemplo, `user.organizationName=My Company` é inválido
  * **Formato**: Deve ser pares chave=valor separados por vírgula: `key1=value1,key2=value2`
  * **Caracteres permitidos**: Apenas caracteres US-ASCII excluindo caracteres de controle, espaços em branco, aspas duplas, vírgulas, ponto-e-vírgula e barras invertidas
  * **Caracteres especiais**: Caracteres fora do intervalo permitido devem ser codificados em percentual

  **Exemplos:**

  ```bash theme={null}
  # ❌ Inválido - contém espaços
  export OTEL_RESOURCE_ATTRIBUTES="org.name=John's Organization"

  # ✅ Válido - use sublinhados ou camelCase em vez disso
  export OTEL_RESOURCE_ATTRIBUTES="org.name=Johns_Organization"
  export OTEL_RESOURCE_ATTRIBUTES="org.name=JohnsOrganization"

  # ✅ Válido - codifique em percentual caracteres especiais se necessário
  export OTEL_RESOURCE_ATTRIBUTES="org.name=John%27s%20Organization"
  ```

  Nota: envolver valores em aspas não escapa espaços. Por exemplo, `org.name="My Company"` resulta no valor literal `"My Company"` (com aspas incluídas), não `My Company`.
</Warning>

### Configurações de exemplo

Defina essas variáveis de ambiente antes de executar `claude`. Cada bloco mostra uma configuração completa para um exportador diferente ou cenário de implantação:

```bash theme={null}
# Depuração de console (intervalos de 1 segundo)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console
export OTEL_METRIC_EXPORT_INTERVAL=1000

# OTLP/gRPC
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Prometheus
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=prometheus

# Múltiplos exportadores
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console,otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=http/json

# Diferentes endpoints/backends para métricas e logs
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_METRICS_PROTOCOL=http/protobuf
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://metrics.example.com:4318
export OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://logs.example.com:4317

# Apenas métricas (sem eventos/logs)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Apenas eventos/logs (sem métricas)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

## Métricas e eventos disponíveis

### Atributos padrão

Todas as métricas e eventos compartilham esses atributos padrão:

| Atributo            | Descrição                                                                                                                       | Controlado Por                                     |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| `session.id`        | Identificador de sessão único                                                                                                   | `OTEL_METRICS_INCLUDE_SESSION_ID` (padrão: true)   |
| `app.version`       | Versão atual do Claude Code                                                                                                     | `OTEL_METRICS_INCLUDE_VERSION` (padrão: false)     |
| `organization.id`   | UUID da organização (quando autenticado)                                                                                        | Sempre incluído quando disponível                  |
| `user.account_uuid` | UUID da conta (quando autenticado)                                                                                              | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (padrão: true) |
| `user.account_id`   | ID da conta em formato marcado correspondendo às APIs de administrador Anthropic (quando autenticado), como `user_01BWBeN28...` | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (padrão: true) |
| `user.id`           | Identificador anônimo de dispositivo/instalação, gerado por instalação do Claude Code                                           | Sempre incluído                                    |
| `user.email`        | Endereço de email do usuário (quando autenticado via OAuth)                                                                     | Sempre incluído quando disponível                  |
| `terminal.type`     | Tipo de terminal, como `iTerm.app`, `vscode`, `cursor` ou `tmux`                                                                | Sempre incluído quando detectado                   |

Os eventos incluem adicionalmente os seguintes atributos. Estes nunca são anexados a métricas porque causariam cardinalidade ilimitada:

* `prompt.id`: UUID correlacionando um prompt do usuário com todos os eventos subsequentes até o próximo prompt. Veja [Atributos de correlação de evento](#atributos-de-correlação-de-evento).
* `workspace.host_paths`: diretórios de workspace do host selecionados no aplicativo desktop, como um array de string

### Métricas

Claude Code exporta as seguintes métricas:

| Nome da Métrica                       | Descrição                                                           | Unidade |
| ------------------------------------- | ------------------------------------------------------------------- | ------- |
| `claude_code.session.count`           | Contagem de sessões CLI iniciadas                                   | count   |
| `claude_code.lines_of_code.count`     | Contagem de linhas de código modificadas                            | count   |
| `claude_code.pull_request.count`      | Número de pull requests criados                                     | count   |
| `claude_code.commit.count`            | Número de commits git criados                                       | count   |
| `claude_code.cost.usage`              | Custo da sessão Claude Code                                         | USD     |
| `claude_code.token.usage`             | Número de tokens usados                                             | tokens  |
| `claude_code.code_edit_tool.decision` | Contagem de decisões de permissão da ferramenta de edição de código | count   |
| `claude_code.active_time.total`       | Tempo ativo total em segundos                                       | s       |

### Detalhes das métricas

Cada métrica inclui os atributos padrão listados acima. Métricas com atributos adicionais específicos do contexto são observadas abaixo.

#### Contador de sessão

Incrementado no início de cada sessão.

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `start_type`: Como a sessão foi iniciada. Um de `"fresh"`, `"resume"` ou `"continue"`

#### Contador de linhas de código

Incrementado quando código é adicionado ou removido.

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `type`: (`"added"`, `"removed"`)

#### Contador de pull request

Incrementado ao criar pull requests via Claude Code.

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)

#### Contador de commit

Incrementado ao criar commits git via Claude Code.

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)

#### Contador de custo

Incrementado após cada solicitação de API.

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `model`: Identificador do modelo (por exemplo, "claude-sonnet-4-6")
* `query_source`: Categoria do subsistema que emitiu a solicitação. Um de `"main"`, `"subagent"` ou `"auxiliary"`
* `speed`: `"fast"` quando a solicitação usou modo rápido. Ausente caso contrário
* `effort`: [Nível de esforço](/pt/model-config#adjust-effort-level) aplicado à solicitação: `"low"`, `"medium"`, `"high"`, `"xhigh"` ou `"max"`. Ausente quando o modelo não suporta esforço.

#### Contador de token

Incrementado após cada solicitação de API.

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `type`: (`"input"`, `"output"`, `"cacheRead"`, `"cacheCreation"`)
* `model`: Identificador do modelo (por exemplo, "claude-sonnet-4-6")
* `query_source`: Categoria do subsistema que emitiu a solicitação. Um de `"main"`, `"subagent"` ou `"auxiliary"`
* `speed`: `"fast"` quando a solicitação usou modo rápido. Ausente caso contrário
* `effort`: [Nível de esforço](/pt/model-config#adjust-effort-level) aplicado à solicitação. Veja [Contador de custo](#contador-de-custo) para detalhes.

#### Contador de decisão da ferramenta de edição de código

Incrementado quando o usuário aceita ou rejeita o uso da ferramenta Edit, Write ou NotebookEdit.

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `tool_name`: Nome da ferramenta (`"Edit"`, `"Write"`, `"NotebookEdit"`)
* `decision`: Decisão do usuário (`"accept"`, `"reject"`)
* `source`: Onde a decisão veio. Um de `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"` ou `"user_reject"`. Veja o [Evento de decisão da ferramenta](#evento-de-decisão-da-ferramenta) para o que cada valor significa.
* `language`: Linguagem de programação do arquivo editado, como `"TypeScript"`, `"Python"`, `"JavaScript"` ou `"Markdown"`. Retorna `"unknown"` para extensões de arquivo não reconhecidas.

#### Contador de tempo ativo

Rastreia o tempo real gasto usando ativamente Claude Code, excluindo tempo ocioso. Essa métrica é incrementada durante interações do usuário (digitação, leitura de respostas) e durante processamento CLI (execução de ferramentas, geração de resposta de IA).

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `type`: `"user"` para interações de teclado, `"cli"` para execução de ferramentas e respostas de IA

### Eventos

Claude Code exporta os seguintes eventos via logs/eventos OpenTelemetry (quando `OTEL_LOGS_EXPORTER` está configurado):

#### Atributos de correlação de evento

Quando um usuário envia um prompt, Claude Code pode fazer múltiplas chamadas de API e executar várias ferramentas. O atributo `prompt.id` permite vincular todos esses eventos de volta ao único prompt que os acionou.

| Atributo    | Descrição                                                                                            |
| ----------- | ---------------------------------------------------------------------------------------------------- |
| `prompt.id` | Identificador UUID v4 vinculando todos os eventos produzidos ao processar um único prompt do usuário |

Para rastrear toda a atividade acionada por um único prompt, filtre seus eventos por um valor específico de `prompt.id`. Isso retorna o evento user\_prompt, quaisquer eventos api\_request e quaisquer eventos tool\_result que ocorreram ao processar esse prompt.

<Note>
  `prompt.id` é intencionalmente excluído de métricas porque cada prompt gera um ID único, o que criaria um número sempre crescente de séries temporais. Use-o apenas para análise em nível de evento e trilhas de auditoria.
</Note>

#### Evento de prompt do usuário

Registrado quando um usuário envia um prompt.

**Nome do Evento**: `claude_code.user_prompt`

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `event.name`: `"user_prompt"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contador monotonicamente crescente para ordenar eventos dentro de uma sessão
* `prompt_length`: Comprimento do prompt
* `prompt`: Conteúdo do prompt (reduzido por padrão, ativar com `OTEL_LOG_USER_PROMPTS=1`)
* `command_name`: Nome do comando quando o prompt invoca um. Nomes de comando integrados e agrupados como `compact` ou `debug` são emitidos como estão; aliases como `reset` emitem como digitados em vez do nome canônico. Nomes de comando customizado, plugin e MCP colapsam para `custom` ou `mcp` a menos que `OTEL_LOG_TOOL_DETAILS=1` esteja definido
* `command_source`: Origem do comando quando presente: `builtin`, `custom` ou `mcp`. Comandos fornecidos por plugin relatam como `custom`

#### Evento de resultado da ferramenta

Registrado quando uma ferramenta conclui a execução.

**Nome do Evento**: `claude_code.tool_result`

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `event.name`: `"tool_result"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contador monotonicamente crescente para ordenar eventos dentro de uma sessão
* `tool_name`: Nome da ferramenta
* `tool_use_id`: Identificador único para esta invocação de ferramenta. Corresponde ao `tool_use_id` passado para hooks, permitindo correlação entre eventos OTel e dados capturados por hook.
* `success`: `"true"` ou `"false"`
* `duration_ms`: Tempo de execução em milissegundos
* `error_type`: String de categoria de erro quando a ferramenta falhou, como `"Error:ENOENT"` ou `"ShellError"`
* `error` (quando `OTEL_LOG_TOOL_DETAILS=1`): Mensagem de erro completa quando a ferramenta falhou
* `decision_type`: Ou `"accept"` ou `"reject"`
* `decision_source`: Onde a decisão veio. Um de `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"` ou `"user_reject"`. Veja o [Evento de decisão da ferramenta](#evento-de-decisão-da-ferramenta) para o que cada valor significa.
* `tool_input_size_bytes`: Tamanho da entrada da ferramenta serializada em JSON em bytes
* `tool_result_size_bytes`: Tamanho do resultado da ferramenta em bytes
* `mcp_server_scope`: Identificador de escopo do servidor MCP (para ferramentas MCP)
* `tool_parameters` (quando `OTEL_LOG_TOOL_DETAILS=1`): String JSON contendo parâmetros específicos da ferramenta:
  * Para ferramenta Bash: inclui `bash_command`, `full_command`, `timeout`, `description`, `dangerouslyDisableSandbox` e `git_commit_id` (o SHA do commit, quando um comando `git commit` é bem-sucedido)
  * Para ferramentas MCP: inclui `mcp_server_name`, `mcp_tool_name`
  * Para ferramenta Skill: inclui `skill_name`
  * Para ferramenta Task: inclui `subagent_type`
* `tool_input` (quando `OTEL_LOG_TOOL_DETAILS=1`): Argumentos de ferramenta serializados em JSON. Valores individuais com mais de 512 caracteres são truncados, e a carga útil completa é limitada a \~4 K caracteres. Aplica-se a todas as ferramentas, incluindo ferramentas MCP.

#### Evento de solicitação de API

Registrado para cada solicitação de API para Claude.

**Nome do Evento**: `claude_code.api_request`

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `event.name`: `"api_request"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contador monotonicamente crescente para ordenar eventos dentro de uma sessão
* `model`: Modelo usado (por exemplo, "claude-sonnet-4-6")
* `cost_usd`: Custo estimado em USD
* `duration_ms`: Duração da solicitação em milissegundos
* `input_tokens`: Número de tokens de entrada
* `output_tokens`: Número de tokens de saída
* `cache_read_tokens`: Número de tokens lidos do cache
* `cache_creation_tokens`: Número de tokens usados para criação de cache
* `request_id`: ID de solicitação da API Anthropic do cabeçalho `request-id` da resposta, como `"req_011..."`. Presente apenas quando a API retorna um.
* `speed`: `"fast"` ou `"normal"`, indicando se o modo rápido estava ativo
* `query_source`: Subsistema que emitiu a solicitação, como `"repl_main_thread"`, `"compact"` ou um nome de subagente
* `effort`: [Nível de esforço](/pt/model-config#adjust-effort-level) aplicado à solicitação: `"low"`, `"medium"`, `"high"`, `"xhigh"` ou `"max"`. Ausente quando o modelo não suporta esforço.

#### Evento de erro de API

Registrado quando uma solicitação de API para Claude falha.

**Nome do Evento**: `claude_code.api_error`

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `event.name`: `"api_error"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contador monotonicamente crescente para ordenar eventos dentro de uma sessão
* `model`: Modelo usado (por exemplo, "claude-sonnet-4-6")
* `error`: Mensagem de erro
* `status_code`: Código de status HTTP como número. Ausente para erros não-HTTP, como falhas de conexão.
* `duration_ms`: Duração da solicitação em milissegundos
* `attempt`: Número total de tentativas feitas, incluindo a solicitação inicial (`1` significa que nenhuma tentativa ocorreu)
* `request_id`: ID de solicitação da API Anthropic do cabeçalho `request-id` da resposta, como `"req_011..."`. Presente apenas quando a API retorna um.
* `speed`: `"fast"` ou `"normal"`, indicando se o modo rápido estava ativo
* `query_source`: Subsistema que emitiu a solicitação, como `"repl_main_thread"`, `"compact"` ou um nome de subagente
* `effort`: [Nível de esforço](/pt/model-config#adjust-effort-level) aplicado à solicitação. Ausente quando o modelo não suporta esforço.

#### Evento de corpo de solicitação de API

Registrado para cada tentativa de solicitação de API quando `OTEL_LOG_RAW_API_BODIES` está definido. Um evento é emitido por tentativa, então tentativas com parâmetros ajustados cada uma produzem seu próprio evento.

**Nome do Evento**: `claude_code.api_request_body`

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `event.name`: `"api_request_body"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contador monotonicamente crescente para ordenar eventos dentro de uma sessão
* `body`: Parâmetros de solicitação da API Messages serializados em JSON (prompt do sistema, mensagens, ferramentas, etc.), truncados em 60 KB. Conteúdo de pensamento estendido em turnos anteriores do assistente é reduzido. Emitido apenas em modo inline (`OTEL_LOG_RAW_API_BODIES=1`).
* `body_ref`: Caminho absoluto para um arquivo `<dir>/<uuid>.request.json` contendo o corpo não truncado. Emitido apenas em modo arquivo (`OTEL_LOG_RAW_API_BODIES=file:<dir>`).
* `body_length`: Comprimento do corpo não truncado. Bytes UTF-8 quando `OTEL_LOG_RAW_API_BODIES=file:<dir>`, ou unidades de código UTF-16 quando `=1`
* `body_truncated`: `"true"` quando truncamento inline ocorreu. Ausente em modo arquivo e quando nenhum truncamento ocorreu.
* `model`: Identificador do modelo dos parâmetros de solicitação
* `query_source`: Subsistema que emitiu a solicitação (por exemplo, `"compact"`)

#### Evento de corpo de resposta de API

Registrado para cada resposta de API bem-sucedida quando `OTEL_LOG_RAW_API_BODIES` está definido.

**Nome do Evento**: `claude_code.api_response_body`

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `event.name`: `"api_response_body"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contador monotonicamente crescente para ordenar eventos dentro de uma sessão
* `body`: Resposta da API Messages serializada em JSON (id, blocos de conteúdo, uso, razão de parada), truncada em 60 KB. Conteúdo de pensamento estendido é reduzido. Emitido apenas em modo inline (`OTEL_LOG_RAW_API_BODIES=1`).
* `body_ref`: Caminho absoluto para um arquivo `<dir>/<request_id>.response.json` contendo o corpo não truncado. Emitido apenas em modo arquivo (`OTEL_LOG_RAW_API_BODIES=file:<dir>`).
* `body_length`: Comprimento do corpo não truncado. Bytes UTF-8 quando `OTEL_LOG_RAW_API_BODIES=file:<dir>`, ou unidades de código UTF-16 quando `=1`
* `body_truncated`: `"true"` quando truncamento inline ocorreu. Ausente em modo arquivo e quando nenhum truncamento ocorreu.
* `model`: Identificador do modelo
* `query_source`: Subsistema que emitiu a solicitação
* `request_id`: ID de solicitação da API Anthropic do cabeçalho `request-id` da resposta, como `"req_011..."`. Presente apenas quando a API retorna um.

#### Evento de decisão da ferramenta

Registrado quando uma decisão de permissão da ferramenta é feita (aceitar/rejeitar).

**Nome do Evento**: `claude_code.tool_decision`

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `event.name`: `"tool_decision"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contador monotonicamente crescente para ordenar eventos dentro de uma sessão
* `tool_name`: Nome da ferramenta (por exemplo, "Read", "Edit", "Write", "NotebookEdit")
* `tool_use_id`: Identificador único para esta invocação de ferramenta. Corresponde ao `tool_use_id` passado para hooks, permitindo correlação entre eventos OTel e dados capturados por hook.
* `decision`: Ou `"accept"` ou `"reject"`
* `source`: Onde a decisão veio:
  * `"config"`: Decidido automaticamente sem avisar, baseado em configurações de projeto, política gerenciada corporativa, sinalizadores `--allowedTools` ou `--disallowedTools`, o modo de permissão ativo ou porque a ferramenta é inerentemente segura.
  * `"hook"`: Um hook `PreToolUse` ou `PermissionRequest` retornou a decisão.
  * `"user_permanent"`: Emitido quando o usuário escolheu "Sempre permitir" quando solicitado, salvando uma regra em suas configurações pessoais. Também emitido para chamadas posteriores que correspondem a essa regra salva. Tratado como uma aceitação.
  * `"user_temporary"`: Emitido quando o usuário escolheu "Sim" ou "Sim, para esta sessão" quando solicitado, sem salvar uma regra. Também emitido para chamadas posteriores na mesma sessão que correspondem a essa permissão com escopo de sessão. Tratado como uma aceitação.
  * `"user_abort"`: Emitido quando o usuário descartou o aviso de permissão sem responder. Tratado como uma rejeição.
  * `"user_reject"`: Emitido quando o usuário escolheu "Não" quando solicitado, ou uma chamada correspondeu a uma regra de negação em suas configurações pessoais. Tratado como uma rejeição.

#### Evento de modo de permissão alterado

Registrado quando o modo de permissão muda, por exemplo de ciclagem Shift+Tab, saída do modo plano ou verificação de gate de modo automático.

**Nome do Evento**: `claude_code.permission_mode_changed`

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `event.name`: `"permission_mode_changed"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contador monotonicamente crescente para ordenar eventos dentro de uma sessão
* `from_mode`: O modo de permissão anterior, por exemplo `"default"`, `"plan"`, `"acceptEdits"`, `"auto"` ou `"bypassPermissions"`
* `to_mode`: O novo modo de permissão
* `trigger`: O que causou a mudança. Um de `"shift_tab"`, `"exit_plan_mode"`, `"auto_gate_denied"` ou `"auto_opt_in"`. Ausente quando a transição se origina do SDK ou bridge

#### Evento de autenticação

Registrado quando `/login` ou `/logout` é concluído.

**Nome do Evento**: `claude_code.auth`

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `event.name`: `"auth"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contador monotonicamente crescente para ordenar eventos dentro de uma sessão
* `action`: `"login"` ou `"logout"`
* `success`: `"true"` ou `"false"`
* `auth_method`: Método de autenticação, como `"oauth"`
* `error_category`: Tipo de erro categórico quando a ação falhou. A mensagem de erro bruta nunca é incluída
* `status_code`: Código de status HTTP como string quando a ação falhou com um erro HTTP

#### Evento de conexão do servidor MCP

Registrado quando um servidor MCP se conecta, desconecta ou falha ao conectar.

**Nome do Evento**: `claude_code.mcp_server_connection`

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `event.name`: `"mcp_server_connection"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contador monotonicamente crescente para ordenar eventos dentro de uma sessão
* `status`: `"connected"`, `"failed"` ou `"disconnected"`
* `transport_type`: Transporte do servidor, como `"stdio"`, `"sse"` ou `"http"`
* `server_scope`: Escopo em que o servidor está configurado, como `"user"`, `"project"` ou `"local"`
* `duration_ms`: Duração da tentativa de conexão em milissegundos
* `error_code`: Código de erro quando a conexão falhou
* `server_name` (quando `OTEL_LOG_TOOL_DETAILS=1`): Nome do servidor configurado
* `error` (quando `OTEL_LOG_TOOL_DETAILS=1`): Mensagem de erro completa quando a conexão falhou

#### Evento de erro interno

Registrado quando Claude Code captura um erro interno inesperado. Apenas o nome da classe de erro e um código estilo errno são registrados. A mensagem de erro e rastreamento de pilha nunca são incluídos. Este evento não é emitido ao executar contra Bedrock, Vertex ou Foundry, ou quando `DISABLE_ERROR_REPORTING` está definido.

**Nome do Evento**: `claude_code.internal_error`

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `event.name`: `"internal_error"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contador monotonicamente crescente para ordenar eventos dentro de uma sessão
* `error_name`: Nome da classe de erro, como `"TypeError"` ou `"SyntaxError"`
* `error_code`: Código errno Node.js como `"ENOENT"` quando presente no erro

#### Evento de plugin instalado

Registrado quando um plugin termina de instalar, tanto do comando CLI `claude plugin install` quanto da UI interativa `/plugin`.

**Nome do Evento**: `claude_code.plugin_installed`

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `event.name`: `"plugin_installed"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contador monotonicamente crescente para ordenar eventos dentro de uma sessão
* `marketplace.is_official`: `"true"` se o marketplace é um marketplace oficial Anthropic, `"false"` caso contrário
* `install.trigger`: `"cli"` ou `"ui"`
* `plugin.name`: Nome do plugin instalado. Para marketplaces de terceiros isso é incluído apenas quando `OTEL_LOG_TOOL_DETAILS=1`
* `plugin.version`: Versão do plugin quando declarada na entrada do marketplace. Para marketplaces de terceiros isso é incluído apenas quando `OTEL_LOG_TOOL_DETAILS=1`
* `marketplace.name`: Marketplace do qual o plugin foi instalado. Para marketplaces de terceiros isso é incluído apenas quando `OTEL_LOG_TOOL_DETAILS=1`

#### Evento de skill ativado

Registrado quando uma skill é invocada, seja Claude a chama através da ferramenta Skill ou você a executa como um comando `/`.

**Nome do Evento**: `claude_code.skill_activated`

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `event.name`: `"skill_activated"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contador monotonicamente crescente para ordenar eventos dentro de uma sessão
* `skill.name`: Nome da skill. Para skills definidas pelo usuário e de plugin de terceiros o valor é o placeholder `"custom_skill"` a menos que `OTEL_LOG_TOOL_DETAILS=1`
* `invocation_trigger`: Como a skill foi acionada (`"user-slash"`, `"claude-proactive"` ou `"nested-skill"`)
* `skill.source`: De onde a skill foi carregada (por exemplo, `"bundled"`, `"userSettings"`, `"projectSettings"`, `"plugin"`)
* `plugin.name` (quando `OTEL_LOG_TOOL_DETAILS=1` ou o plugin é de um marketplace oficial): Nome do plugin proprietário quando a skill é fornecida por um plugin
* `marketplace.name` (quando `OTEL_LOG_TOOL_DETAILS=1` ou o plugin é de um marketplace oficial): Marketplace do qual o plugin proprietário foi instalado, quando a skill é fornecida por um plugin

#### Evento de menção @

Registrado quando Claude Code resolve uma menção `@` em um prompt. Nem toda menção emite um evento: caminhos de saída antecipada, como negações de permissão, arquivos superdimensionados, anexos de referência PDF e falhas de listagem de diretório retornam sem registrar.

**Nome do Evento**: `claude_code.at_mention`

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `event.name`: `"at_mention"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contador monotonicamente crescente para ordenar eventos dentro de uma sessão
* `mention_type`: Tipo de menção (`"file"`, `"directory"`, `"agent"`, `"mcp_resource"`)
* `success`: Se a menção foi resolvida com sucesso (`"true"` ou `"false"`)

#### Evento de tentativas de API esgotadas

Registrado uma vez quando uma solicitação de API falha após mais de uma tentativa. Emitido junto com o evento `api_error` final.

**Nome do Evento**: `claude_code.api_retries_exhausted`

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `event.name`: `"api_retries_exhausted"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contador monotonicamente crescente para ordenar eventos dentro de uma sessão
* `model`: Modelo usado
* `error`: Mensagem de erro final
* `status_code`: Código de status HTTP como número. Ausente para erros não-HTTP.
* `total_attempts`: Número total de tentativas feitas
* `total_retry_duration_ms`: Tempo total de parede em todas as tentativas
* `speed`: `"fast"` ou `"normal"`

#### Evento de início de execução de hook

Registrado quando um ou mais hooks começam a executar para um evento de hook.

**Nome do Evento**: `claude_code.hook_execution_start`

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `event.name`: `"hook_execution_start"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contador monotonicamente crescente para ordenar eventos dentro de uma sessão
* `hook_event`: Tipo de evento de hook, como `"PreToolUse"` ou `"PostToolUse"`
* `hook_name`: Nome completo do hook incluindo matcher, como `"PreToolUse:Write"`
* `num_hooks`: Número de comandos de hook correspondentes
* `managed_only`: `"true"` quando apenas hooks de política gerenciada são permitidos
* `hook_source`: `"policySettings"` ou `"merged"`
* `hook_definitions`: Configuração de hook serializada em JSON. Incluído apenas quando rastreamento beta detalhado e `OTEL_LOG_TOOL_DETAILS=1` estão ambos ativados

#### Evento de conclusão de execução de hook

Registrado quando todos os hooks para um evento de hook terminaram.

**Nome do Evento**: `claude_code.hook_execution_complete`

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `event.name`: `"hook_execution_complete"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contador monotonicamente crescente para ordenar eventos dentro de uma sessão
* `hook_event`: Tipo de evento de hook
* `hook_name`: Nome completo do hook incluindo matcher
* `num_hooks`: Número de comandos de hook correspondentes
* `num_success`: Contagem que completou com sucesso
* `num_blocking`: Contagem que retornou uma decisão de bloqueio
* `num_non_blocking_error`: Contagem que falhou sem bloquear
* `num_cancelled`: Contagem cancelada antes da conclusão
* `total_duration_ms`: Duração de parede de todos os hooks correspondentes
* `managed_only`: `"true"` quando apenas hooks de política gerenciada são permitidos
* `hook_source`: `"policySettings"` ou `"merged"`
* `hook_definitions`: Configuração de hook serializada em JSON. Incluído apenas quando rastreamento beta detalhado e `OTEL_LOG_TOOL_DETAILS=1` estão ambos ativados

#### Evento de compactação

Registrado quando a compactação de conversa é concluída.

**Nome do Evento**: `claude_code.compaction`

**Atributos**:

* Todos os [atributos padrão](#atributos-padrão)
* `event.name`: `"compaction"`
* `event.timestamp`: Timestamp ISO 8601
* `event.sequence`: Contador monotonicamente crescente para ordenar eventos dentro de uma sessão
* `trigger`: `"auto"` ou `"manual"`
* `success`: `"true"` ou `"false"`
* `duration_ms`: Duração da compactação
* `pre_tokens`: Contagem aproximada de tokens antes da compactação
* `post_tokens`: Contagem aproximada de tokens após compactação
* `error`: Mensagem de erro quando a compactação falhou

## Interpretar dados de métricas e eventos

As métricas e eventos exportados suportam uma gama de análises:

### Monitoramento de uso

| Métrica                                                       | Oportunidade de Análise                                       |
| ------------------------------------------------------------- | ------------------------------------------------------------- |
| `claude_code.token.usage`                                     | Dividir por `type` (entrada/saída), usuário, equipe ou modelo |
| `claude_code.session.count`                                   | Rastrear adoção e engajamento ao longo do tempo               |
| `claude_code.lines_of_code.count`                             | Medir produtividade rastreando adições/remoções de código     |
| `claude_code.commit.count` & `claude_code.pull_request.count` | Entender o impacto nos fluxos de trabalho de desenvolvimento  |

### Monitoramento de custo

A métrica `claude_code.cost.usage` ajuda com:

* Rastreamento de tendências de uso entre equipes ou indivíduos
* Identificação de sessões de alto uso para otimização

<Note>
  As métricas de custo são aproximações. Para dados de faturamento oficiais, consulte seu provedor de API (Claude Console, Amazon Bedrock ou Google Cloud Vertex).
</Note>

### Alertas e segmentação

Alertas comuns a considerar:

* Picos de custo
* Consumo incomum de tokens
* Alto volume de sessão de usuários específicos

Todas as métricas podem ser segmentadas por `user.account_uuid`, `user.account_id`, `organization.id`, `session.id`, `model` e `app.version`.

### Detectar esgotamento de tentativas

Claude Code retenta solicitações de API falhadas internamente e emite um único evento `claude_code.api_error` apenas depois de desistir, então o evento em si é o sinal terminal para essa solicitação. Tentativas de repetição intermediárias não são registradas como eventos separados.

O atributo `attempt` no evento registra quantas tentativas foram feitas no total. Um valor maior que `CLAUDE_CODE_MAX_RETRIES` (padrão `10`) indica que a solicitação esgotou todas as tentativas em um erro transitório. Um valor menor indica um erro não retentável como uma resposta `400`.

Para distinguir uma sessão que se recuperou de uma que travou, agrupe eventos por `session.id` e verifique se um evento `api_request` posterior existe após o erro.

### Análise de eventos

Os dados de eventos fornecem insights detalhados sobre interações do Claude Code:

**Padrões de Uso de Ferramentas**: analise eventos de resultado de ferramentas para identificar:

* Ferramentas mais frequentemente usadas
* Taxas de sucesso da ferramenta
* Tempos médios de execução da ferramenta
* Padrões de erro por tipo de ferramenta

**Monitoramento de Desempenho**: rastreie durações de solicitações de API e tempos de execução de ferramentas para identificar gargalos de desempenho.

## Considerações de backend

Sua escolha de backends de métricas, logs e rastreamentos determina os tipos de análises que você pode realizar:

### Para métricas

* **Bancos de dados de série temporal (por exemplo, Prometheus)**: Cálculos de taxa, métricas agregadas
* **Armazenamentos colunares (por exemplo, ClickHouse)**: Consultas complexas, análise de usuário único
* **Plataformas de observabilidade completas (por exemplo, Honeycomb, Datadog)**: Consultas avançadas, visualização, alertas

### Para eventos/logs

* **Sistemas de agregação de logs (por exemplo, Elasticsearch, Loki)**: Busca de texto completo, análise de logs
* **Armazenamentos colunares (por exemplo, ClickHouse)**: Análise de eventos estruturados
* **Plataformas de observabilidade completas (por exemplo, Honeycomb, Datadog)**: Correlação entre métricas e eventos

### Para rastreamentos

Escolha um backend que suporte armazenamento de rastreamento distribuído e correlação de span:

* **Sistemas de rastreamento distribuído (por exemplo, Jaeger, Zipkin, Grafana Tempo)**: Visualização de span, waterfalls de solicitação, análise de latência
* **Plataformas de observabilidade completas (por exemplo, Honeycomb, Datadog)**: Busca de rastreamento e correlação com métricas e logs

Para organizações que exigem métricas de Usuário Ativo Diário/Semanal/Mensal (DAU/WAU/MAU), considere backends que suportam consultas eficientes de valor único.

## Informações de serviço

Todas as métricas e eventos são exportados com os seguintes atributos de recurso:

* `service.name`: `claude-code`
* `service.version`: Versão atual do Claude Code
* `os.type`: Tipo de sistema operacional (por exemplo, `linux`, `darwin`, `windows`)
* `os.version`: String de versão do sistema operacional
* `host.arch`: Arquitetura do host (por exemplo, `amd64`, `arm64`)
* `wsl.version`: Número de versão do WSL (apenas presente ao executar no Windows Subsystem for Linux)
* Nome do Medidor: `com.anthropic.claude_code`

## Recursos de medição de ROI

Para um guia abrangente sobre como medir o retorno sobre investimento para Claude Code, incluindo configuração de telemetria, análise de custo, métricas de produtividade e relatórios automatizados, consulte o [Guia de Medição de ROI do Claude Code](https://github.com/anthropics/claude-code-monitoring-guide). Este repositório fornece configurações Docker Compose prontas para uso, configurações Prometheus e OpenTelemetry, e modelos para gerar relatórios de produtividade integrados com ferramentas como Linear.

## Segurança e privacidade

* A exportação OpenTelemetry para seu backend é opt-in e requer configuração explícita. Para a telemetria operacional separada da Anthropic e como desabilitá-la, consulte [Uso de dados](/pt/data-usage#telemetry-services)
* Conteúdos de arquivo brutos e trechos de código não são incluídos em métricas ou eventos. Os spans de rastreamento são um caminho de dados separado: veja o ponto `OTEL_LOG_TOOL_CONTENT` abaixo
* Quando autenticado via OAuth, `user.email` é incluído em atributos de telemetria. Se isso for uma preocupação para sua organização, trabalhe com seu backend de telemetria para filtrar ou reduzir este campo
* O conteúdo do prompt do usuário não é coletado por padrão. Apenas o comprimento do prompt é registrado. Para incluir conteúdo do prompt, defina `OTEL_LOG_USER_PROMPTS=1`
* Argumentos de entrada de ferramenta e parâmetros não são registrados por padrão. Para incluí-los, defina `OTEL_LOG_TOOL_DETAILS=1`. Quando ativado, eventos `tool_result` incluem um atributo `tool_parameters` com comandos Bash, nomes de servidor MCP e ferramenta, e nomes de skill, mais um atributo `tool_input` com caminhos de arquivo, URLs, padrões de busca e outros argumentos. Eventos `user_prompt` incluem o `command_name` verbatim para comandos customizado, plugin e MCP. Spans de rastreamento incluem o mesmo atributo `tool_input` e atributos derivados de entrada como `file_path`. Valores individuais com mais de 512 caracteres são truncados e o total é limitado a \~4 K caracteres, mas os argumentos ainda podem conter valores sensíveis. Configure seu backend de telemetria para filtrar ou reduzir esses atributos conforme necessário
* O conteúdo de entrada e saída de ferramenta não é registrado em spans de rastreamento por padrão. Para incluí-lo, defina `OTEL_LOG_TOOL_CONTENT=1`. Quando ativado, eventos de span incluem conteúdo completo de entrada e saída de ferramenta truncado em 60 KB por span. Isso pode incluir conteúdos de arquivo brutos de resultados da ferramenta Read e saída de comando Bash. Configure seu backend de telemetria para filtrar ou reduzir esses atributos conforme necessário
* Corpos de solicitação e resposta da API Anthropic Messages brutos não são registrados por padrão. Para incluí-los, defina `OTEL_LOG_RAW_API_BODIES`. Com `=1`, cada chamada de API emite eventos de log `api_request_body` e `api_response_body` cujo atributo `body` é a carga útil serializada em JSON, truncada em 60 KB. Com `=file:<dir>`, corpos não truncados são escritos em arquivos `.request.json` e `.response.json` sob esse diretório e os eventos carregam um caminho `body_ref` em vez do corpo inline. Envie o diretório com um coletor de log ou sidecar em vez de através do fluxo de telemetria. Em ambos os modos, os corpos contêm o histórico de conversa completo (prompt do sistema, cada turno anterior de usuário e assistente, resultados de ferramenta), então ativar isso implica consentimento para tudo que os outros sinalizadores de conteúdo `OTEL_LOG_*` revelariam. O conteúdo de pensamento estendido do Claude é sempre reduzido desses corpos independentemente de outras configurações

## Monitorar Claude Code no Amazon Bedrock

Para orientação detalhada de monitoramento de uso do Claude Code para Amazon Bedrock, consulte [Implementação de Monitoramento do Claude Code (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md).
