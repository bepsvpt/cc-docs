> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Executar Claude Code programaticamente

> Use o Agent SDK para executar Claude Code programaticamente a partir da CLI, Python ou TypeScript.

O [Agent SDK](https://platform.claude.com/docs/pt/agent-sdk/overview) oferece as mesmas ferramentas, loop de agente e gerenciamento de contexto que alimentam Claude Code. Está disponível como uma CLI para scripts e CI/CD, ou como pacotes [Python](https://platform.claude.com/docs/pt/agent-sdk/python) e [TypeScript](https://platform.claude.com/docs/pt/agent-sdk/typescript) para controle programático completo.

<Note>
  A CLI era anteriormente chamada de "modo headless". O sinalizador `-p` e todas as opções de CLI funcionam da mesma forma.
</Note>

Para executar Claude Code programaticamente a partir da CLI, passe `-p` com seu prompt e qualquer [opção de CLI](/pt/cli-reference):

```bash  theme={null}
claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"
```

Esta página aborda o uso do Agent SDK via CLI (`claude -p`). Para os pacotes SDK Python e TypeScript com saídas estruturadas, callbacks de aprovação de ferramentas e objetos de mensagem nativos, consulte a [documentação completa do Agent SDK](https://platform.claude.com/docs/pt/agent-sdk/overview).

## Uso básico

Adicione o sinalizador `-p` (ou `--print`) a qualquer comando `claude` para executá-lo de forma não interativa. Todas as [opções de CLI](/pt/cli-reference) funcionam com `-p`, incluindo:

* `--continue` para [continuar conversas](#continue-conversations)
* `--allowedTools` para [aprovar ferramentas automaticamente](#auto-approve-tools)
* `--output-format` para [saída estruturada](#get-structured-output)

Este exemplo faz uma pergunta ao Claude sobre sua base de código e imprime a resposta:

```bash  theme={null}
claude -p "What does the auth module do?"
```

## Exemplos

Estes exemplos destacam padrões comuns de CLI.

### Obter saída estruturada

Use `--output-format` para controlar como as respostas são retornadas:

* `text` (padrão): saída de texto simples
* `json`: JSON estruturado com resultado, ID de sessão e metadados
* `stream-json`: JSON delimitado por quebra de linha para streaming em tempo real

Este exemplo retorna um resumo do projeto como JSON com metadados de sessão, com o resultado de texto no campo `result`:

```bash  theme={null}
claude -p "Summarize this project" --output-format json
```

Para obter saída em conformidade com um esquema específico, use `--output-format json` com `--json-schema` e uma definição de [JSON Schema](https://json-schema.org/). A resposta inclui metadados sobre a solicitação (ID de sessão, uso, etc.) com a saída estruturada no campo `structured_output`.

Este exemplo extrai nomes de funções e os retorna como uma matriz de strings:

```bash  theme={null}
claude -p "Extract the main function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

<Tip>
  Use uma ferramenta como [jq](https://jqlang.github.io/jq/) para analisar a resposta e extrair campos específicos:

  ```bash  theme={null}
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

```bash  theme={null}
claude -p "Explain recursion" --output-format stream-json --verbose --include-partial-messages
```

O exemplo a seguir usa [jq](https://jqlang.github.io/jq/) para filtrar deltas de texto e exibir apenas o texto de streaming. O sinalizador `-r` produz strings brutas (sem aspas) e `-j` une sem quebras de linha para que os tokens façam streaming continuamente:

```bash  theme={null}
claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

Para streaming programático com callbacks e objetos de mensagem, consulte [Stream responses in real-time](https://platform.claude.com/docs/pt/agent-sdk/streaming-output) na documentação do Agent SDK.

### Aprovar ferramentas automaticamente

Use `--allowedTools` para permitir que Claude use certas ferramentas sem solicitar. Este exemplo executa um conjunto de testes e corrige falhas, permitindo que Claude execute comandos Bash e leia/edite arquivos sem pedir permissão:

```bash  theme={null}
claude -p "Run the test suite and fix any failures" \
  --allowedTools "Bash,Read,Edit"
```

### Criar um commit

Este exemplo revisa as alterações preparadas e cria um commit com uma mensagem apropriada:

```bash  theme={null}
claude -p "Look at my staged changes and create an appropriate commit" \
  --allowedTools "Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git commit *)"
```

O sinalizador `--allowedTools` usa [sintaxe de regra de permissão](/pt/settings#permission-rule-syntax). O ` *` à direita habilita correspondência de prefixo, então `Bash(git diff *)` permite qualquer comando começando com `git diff`. O espaço antes de `*` é importante: sem ele, `Bash(git diff*)` também corresponderia a `git diff-index`.

<Note>
  [skills](/pt/skills) invocadas pelo usuário como `/commit` e [comandos integrados](/pt/commands) estão disponíveis apenas no modo interativo. No modo `-p`, descreva a tarefa que você deseja realizar.
</Note>

### Personalizar o prompt do sistema

Use `--append-system-prompt` para adicionar instruções mantendo o comportamento padrão do Claude Code. Este exemplo envia um diff de PR para Claude e o instrui a revisar vulnerabilidades de segurança:

```bash  theme={null}
gh pr diff "$1" | claude -p \
  --append-system-prompt "You are a security engineer. Review for vulnerabilities." \
  --output-format json
```

Consulte [system prompt flags](/pt/cli-reference#system-prompt-flags) para mais opções, incluindo `--system-prompt` para substituir completamente o prompt padrão.

### Continuar conversas

Use `--continue` para continuar a conversa mais recente, ou `--resume` com um ID de sessão para continuar uma conversa específica. Este exemplo executa uma revisão e depois envia prompts de acompanhamento:

```bash  theme={null}
# First request
claude -p "Review this codebase for performance issues"

# Continue the most recent conversation
claude -p "Now focus on the database queries" --continue
claude -p "Generate a summary of all issues found" --continue
```

Se você estiver executando várias conversas, capture o ID da sessão para retomar uma específica:

```bash  theme={null}
session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')
claude -p "Continue that review" --resume "$session_id"
```

## Próximas etapas

* [Agent SDK quickstart](https://platform.claude.com/docs/pt/agent-sdk/quickstart): construa seu primeiro agente com Python ou TypeScript
* [CLI reference](/pt/cli-reference): todos os sinalizadores e opções de CLI
* [GitHub Actions](/pt/github-actions): use o Agent SDK em fluxos de trabalho do GitHub
* [GitLab CI/CD](/pt/gitlab-ci-cd): use o Agent SDK em pipelines do GitLab
