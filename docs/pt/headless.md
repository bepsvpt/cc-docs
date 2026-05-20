> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Executar Claude Code programaticamente

> Use o Agent SDK para executar Claude Code programaticamente a partir da CLI, Python ou TypeScript.

<Note>
  Starting June 15, 2026, Agent SDK and `claude -p` usage on subscription plans will draw from a new monthly Agent SDK credit, separate from your interactive usage limits. See [Use the Claude Agent SDK with your Claude plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan) for details.
</Note>

O [Agent SDK](/pt/agent-sdk/overview) oferece as mesmas ferramentas, loop de agente e gerenciamento de contexto que alimentam Claude Code. Está disponível como uma CLI para scripts e CI/CD, ou como pacotes [Python](/pt/agent-sdk/python) e [TypeScript](/pt/agent-sdk/typescript) para controle programático completo.

Para executar Claude Code em modo não interativo, passe `-p` com seu prompt e qualquer [opção de CLI](/pt/cli-reference):

```bash theme={null}
claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"
```

Esta página aborda o uso do Agent SDK via CLI (`claude -p`). Para os pacotes SDK Python e TypeScript com saídas estruturadas, callbacks de aprovação de ferramentas e objetos de mensagem nativos, consulte a [documentação completa do Agent SDK](/pt/agent-sdk/overview).

## Uso básico

Adicione o sinalizador `-p` (ou `--print`) a qualquer comando `claude` para executá-lo de forma não interativa. Todas as [opções de CLI](/pt/cli-reference) funcionam com `-p`, incluindo:

* `--continue` para [continuar conversas](#continue-conversations)
* `--allowedTools` para [aprovar ferramentas automaticamente](#auto-approve-tools)
* `--output-format` para [saída estruturada](#get-structured-output)

Este exemplo faz uma pergunta ao Claude sobre sua base de código e imprime a resposta:

```bash theme={null}
claude -p "What does the auth module do?"
```

### Comece mais rápido com modo bare

Adicione `--bare` para reduzir o tempo de inicialização pulando a descoberta automática de hooks, skills, plugins, servidores MCP, memória automática e CLAUDE.md. Sem ele, `claude -p` carrega o mesmo [contexto](/pt/how-claude-code-works#the-context-window) que uma sessão interativa carregaria, incluindo qualquer coisa configurada no diretório de trabalho ou `~/.claude`.

O modo bare é útil para CI e scripts onde você precisa do mesmo resultado em cada máquina. Um hook no `~/.claude` de um colega de trabalho ou um servidor MCP no `.mcp.json` do projeto não serão executados, porque o modo bare nunca os lê. Apenas os sinalizadores que você passa explicitamente têm efeito.

Este exemplo executa uma tarefa de resumo única em modo bare e pré-aprova a ferramenta Read para que a chamada seja concluída sem um prompt de permissão:

```bash theme={null}
claude --bare -p "Summarize this file" --allowedTools "Read"
```

No modo bare, Claude tem acesso às ferramentas Bash, leitura de arquivo e edição de arquivo. Passe qualquer contexto que você precise com um sinalizador:

| Para carregar                | Use                                                     |
| ---------------------------- | ------------------------------------------------------- |
| Adições de prompt do sistema | `--append-system-prompt`, `--append-system-prompt-file` |
| Configurações                | `--settings <file-or-json>`                             |
| Servidores MCP               | `--mcp-config <file-or-json>`                           |
| Agentes personalizados       | `--agents <json>`                                       |
| Um plugin                    | `--plugin-dir <path>`, `--plugin-url <url>`             |

O modo bare pula leituras de OAuth e keychain. A autenticação do Anthropic deve vir de `ANTHROPIC_API_KEY` ou um `apiKeyHelper` no JSON passado para `--settings`. Bedrock, Vertex e Foundry usam suas credenciais de provedor usuais.

<Note>
  `--bare` é o modo recomendado para chamadas com script e SDK, e se tornará o padrão para `-p` em uma versão futura.
</Note>

## Exemplos

Estes exemplos destacam padrões comuns de CLI. Para CI e outras chamadas com script, adicione [`--bare`](#start-faster-with-bare-mode) para que não captem o que quer que esteja configurado localmente.

### Canalizar dados através do Claude

O modo não interativo lê stdin, então você pode canalizar dados e redirecionar a resposta como qualquer outra ferramenta de linha de comando.

Este exemplo canaliza um log de compilação para Claude e escreve a explicação em um arquivo:

```bash theme={null}
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

Com `--output-format json`, a carga de resposta inclui `total_cost_usd` e um detalhamento de custo por modelo, para que os chamadores com script possam rastrear gastos por invocação sem consultar o [painel de uso](/pt/costs).

<Note>
  A partir do Claude Code v2.1.128, stdin canalizado é limitado a 10MB. Se você exceder o limite, Claude Code sai com um erro claro e um status diferente de zero. Para trabalhar com entradas maiores, escreva o conteúdo em um arquivo e faça referência ao caminho do arquivo em seu prompt em vez de canalizá-lo.
</Note>

### Adicionar Claude a um script de compilação

Você pode envolver uma chamada não interativa em um script para usar Claude como um linter ou revisor específico do projeto.

Este script `package.json` canaliza o diff contra `main` para Claude e pede que ele relate erros de digitação. Canalizar o diff significa que Claude não precisa de permissão Bash para lê-lo, e as aspas duplas escapadas mantêm o script portável para Windows:

```json theme={null}
{
  "scripts": {
    "lint:claude": "git diff main | claude -p \"you are a typo linter. for each typo in this diff, report filename:line on one line and the issue on the next. return nothing else.\""
  }
}
```

### Obter saída estruturada

Use `--output-format` para controlar como as respostas são retornadas:

* `text` (padrão): saída de texto simples
* `json`: JSON estruturado com resultado, ID de sessão e metadados
* `stream-json`: JSON delimitado por quebra de linha para streaming em tempo real

Este exemplo retorna um resumo do projeto como JSON com metadados de sessão, com o resultado de texto no campo `result`:

```bash theme={null}
claude -p "Summarize this project" --output-format json
```

Para obter saída em conformidade com um esquema específico, use `--output-format json` com `--json-schema` e uma definição de [JSON Schema](https://json-schema.org/). A resposta inclui metadados sobre a solicitação (ID de sessão, uso, etc.) com a saída estruturada no campo `structured_output`.

Este exemplo extrai nomes de funções e os retorna como uma matriz de strings:

```bash theme={null}
claude -p "Extract the main function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

<Tip>
  Use uma ferramenta como [jq](https://jqlang.github.io/jq/) para analisar a resposta e extrair campos específicos:

  ```bash theme={null}
  # Extract the text result
  claude -p "Summarize this project" --output-format json | jq -r '.result'

  # Extract structured output
  claude -p "Extract function names from auth.py" \
    --output-format json \
    --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
    | jq '.structured_output'
  ```
</Tip>

### Respostas de stream

Use `--output-format stream-json` com `--verbose` e `--include-partial-messages` para receber tokens conforme são gerados. Cada linha é um objeto JSON representando um evento:

```bash theme={null}
claude -p "Explain recursion" --output-format stream-json --verbose --include-partial-messages
```

O exemplo a seguir usa [jq](https://jqlang.github.io/jq/) para filtrar deltas de texto e exibir apenas o texto de streaming. O sinalizador `-r` produz strings brutas (sem aspas) e `-j` une sem quebras de linha para que os tokens façam streaming continuamente:

```bash theme={null}
claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

Quando uma solicitação de API falha com um erro que pode ser repetido, Claude Code emite um evento `system/api_retry` antes de tentar novamente. Você pode usar isso para exibir o progresso de repetição ou implementar lógica de backoff personalizada.

| Campo            | Tipo            | Descrição                                                                                                                                                                                   |
| ---------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`           | `"system"`      | tipo de mensagem                                                                                                                                                                            |
| `subtype`        | `"api_retry"`   | identifica isso como um evento de repetição                                                                                                                                                 |
| `attempt`        | inteiro         | número da tentativa atual, começando em 1                                                                                                                                                   |
| `max_retries`    | inteiro         | total de repetições permitidas                                                                                                                                                              |
| `retry_delay_ms` | inteiro         | milissegundos até a próxima tentativa                                                                                                                                                       |
| `error_status`   | inteiro ou nulo | código de status HTTP, ou `null` para erros de conexão sem resposta HTTP                                                                                                                    |
| `error`          | string          | categoria de erro: `authentication_failed`, `oauth_org_not_allowed`, `billing_error`, `rate_limit`, `invalid_request`, `model_not_found`, `server_error`, `max_output_tokens`, ou `unknown` |
| `uuid`           | string          | identificador único do evento                                                                                                                                                               |
| `session_id`     | string          | sessão à qual o evento pertence                                                                                                                                                             |

O evento `system/init` relata metadados de sessão incluindo o modelo, ferramentas, servidores MCP e plugins carregados. É o primeiro evento no stream a menos que [`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`](/pt/env-vars) esteja definido, caso em que eventos `plugin_install` o precedem. Use os campos de plugin para falhar CI quando um plugin não foi carregado:

| Campo           | Tipo  | Descrição                                                                                                                                                                                                                                                                                                                 |
| --------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plugins`       | array | plugins que foram carregados com sucesso, cada um com `name` e `path`                                                                                                                                                                                                                                                     |
| `plugin_errors` | array | erros de tempo de carregamento de plugin, cada um com `plugin`, `type` e `message`. Inclui versões de dependência insatisfeitas e falhas de carregamento de `--plugin-dir` como um caminho ausente ou arquivo inválido. Os plugins afetados são rebaixados e ausentes de `plugins`. A chave é omitida quando não há erros |

Quando [`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`](/pt/env-vars) está definido, Claude Code emite eventos `system/plugin_install` enquanto plugins do marketplace instalam antes da primeira volta. Use estes para exibir o progresso de instalação em sua própria UI.

| Campo        | Tipo                                                     | Descrição                                                                                                    |
| ------------ | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| `type`       | `"system"`                                               | tipo de mensagem                                                                                             |
| `subtype`    | `"plugin_install"`                                       | identifica isso como um evento de instalação de plugin                                                       |
| `status`     | `"started"`, `"installed"`, `"failed"`, ou `"completed"` | `started` e `completed` envolvem a instalação geral; `installed` e `failed` relatam marketplaces individuais |
| `name`       | string, opcional                                         | nome do marketplace, presente em `installed` e `failed`                                                      |
| `error`      | string, opcional                                         | mensagem de falha, presente em `failed`                                                                      |
| `uuid`       | string                                                   | identificador único do evento                                                                                |
| `session_id` | string                                                   | sessão à qual o evento pertence                                                                              |

Para streaming programático com callbacks e objetos de mensagem, consulte [Stream responses in real-time](/pt/agent-sdk/streaming-output) na documentação do Agent SDK.

### Aprovar ferramentas automaticamente

Use `--allowedTools` para permitir que Claude use certas ferramentas sem solicitar. Este exemplo executa um conjunto de testes e corrige falhas, permitindo que Claude execute comandos Bash e leia/edite arquivos sem pedir permissão:

```bash theme={null}
claude -p "Run the test suite and fix any failures" \
  --allowedTools "Bash,Read,Edit"
```

Para definir uma linha de base para toda a sessão em vez de listar ferramentas individuais, passe um [modo de permissão](/pt/permission-modes). `dontAsk` nega qualquer coisa não em suas regras `permissions.allow` ou no [conjunto de comandos somente leitura](/pt/permissions#read-only-commands), o que é útil para execuções de CI bloqueadas. `acceptEdits` permite que Claude escreva arquivos sem solicitar e também aprova automaticamente comandos comuns do sistema de arquivos, como `mkdir`, `touch`, `mv` e `cp`. Outros comandos de shell e solicitações de rede ainda precisam de uma entrada `--allowedTools` ou uma regra `permissions.allow`, caso contrário a execução é abortada quando uma é tentada:

```bash theme={null}
claude -p "Apply the lint fixes" --permission-mode acceptEdits
```

### Criar um commit

Este exemplo revisa as alterações preparadas e cria um commit com uma mensagem apropriada:

```bash theme={null}
claude -p "Look at my staged changes and create an appropriate commit" \
  --allowedTools "Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git commit *)"
```

O sinalizador `--allowedTools` usa [sintaxe de regra de permissão](/pt/settings#permission-rule-syntax). O ` *` à direita habilita correspondência de prefixo, então `Bash(git diff *)` permite qualquer comando começando com `git diff`. O espaço antes de `*` é importante: sem ele, `Bash(git diff*)` também corresponderia a `git diff-index`.

<Note>
  [skills](/pt/skills) invocadas pelo usuário como `/commit` e [comandos integrados](/pt/commands) estão disponíveis apenas no modo interativo. No modo `-p`, descreva a tarefa que você deseja realizar.
</Note>

### Personalizar o prompt do sistema

Use `--append-system-prompt` para adicionar instruções mantendo o comportamento padrão do Claude Code. Este exemplo envia um diff de PR para Claude e o instrui a revisar vulnerabilidades de segurança:

```bash theme={null}
gh pr diff "$1" | claude -p \
  --append-system-prompt "You are a security engineer. Review for vulnerabilities." \
  --output-format json
```

Consulte [system prompt flags](/pt/cli-reference#system-prompt-flags) para mais opções, incluindo `--system-prompt` para substituir completamente o prompt padrão.

### Continuar conversas

Use `--continue` para continuar a conversa mais recente, ou `--resume` com um ID de sessão para continuar uma conversa específica. Este exemplo executa uma revisão e depois envia prompts de acompanhamento:

```bash theme={null}
# First request
claude -p "Review this codebase for performance issues"

# Continue the most recent conversation
claude -p "Now focus on the database queries" --continue
claude -p "Generate a summary of all issues found" --continue
```

Se você estiver executando várias conversas, capture o ID da sessão para retomar uma específica:

```bash theme={null}
session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')
claude -p "Continue that review" --resume "$session_id"
```

## Próximas etapas

* [Agent SDK quickstart](/pt/agent-sdk/quickstart): construa seu primeiro agente com Python ou TypeScript
* [CLI reference](/pt/cli-reference): todos os sinalizadores e opções de CLI
* [GitHub Actions](/pt/github-actions): use o Agent SDK em fluxos de trabalho do GitHub
* [GitLab CI/CD](/pt/gitlab-ci-cd): use o Agent SDK em pipelines do GitLab
