> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Referência de CLI

> Referência completa para a interface de linha de comando do Claude Code, incluindo comandos e sinalizadores.

## Comandos CLI

Você pode iniciar sessões, canalizar conteúdo, retomar conversas e gerenciar atualizações com estes comandos:

| Comando                         | Descrição                                                                                                                                                                                                                       | Exemplo                                            |
| :------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------- |
| `claude`                        | Iniciar sessão interativa                                                                                                                                                                                                       | `claude`                                           |
| `claude "query"`                | Iniciar sessão interativa com prompt inicial                                                                                                                                                                                    | `claude "explain this project"`                    |
| `claude -p "query"`             | Consultar via SDK e sair                                                                                                                                                                                                        | `claude -p "explain this function"`                |
| `cat file \| claude -p "query"` | Processar conteúdo canalizado                                                                                                                                                                                                   | `cat logs.txt \| claude -p "explain"`              |
| `claude -c`                     | Continuar a conversa mais recente no diretório atual                                                                                                                                                                            | `claude -c`                                        |
| `claude -c -p "query"`          | Continuar via SDK                                                                                                                                                                                                               | `claude -c -p "Check for type errors"`             |
| `claude -r "<session>" "query"` | Retomar sessão por ID ou nome                                                                                                                                                                                                   | `claude -r "auth-refactor" "Finish this PR"`       |
| `claude update`                 | Atualizar para a versão mais recente                                                                                                                                                                                            | `claude update`                                    |
| `claude auth login`             | Faça login em sua conta Anthropic. Use `--email` para preencher previamente seu endereço de email e `--sso` para forçar autenticação SSO                                                                                        | `claude auth login --email user@example.com --sso` |
| `claude auth logout`            | Fazer logout de sua conta Anthropic                                                                                                                                                                                             | `claude auth logout`                               |
| `claude auth status`            | Mostrar status de autenticação como JSON. Use `--text` para saída legível por humanos. Sai com código 0 se conectado, 1 se não                                                                                                  | `claude auth status`                               |
| `claude agents`                 | Listar todos os [subagents](/pt/sub-agents) configurados, agrupados por fonte                                                                                                                                                   | `claude agents`                                    |
| `claude mcp`                    | Configurar servidores Model Context Protocol (MCP)                                                                                                                                                                              | Veja a [documentação do Claude Code MCP](/pt/mcp). |
| `claude remote-control`         | Iniciar uma [sessão de Remote Control](/pt/remote-control) para controlar Claude Code a partir de Claude.ai ou do aplicativo Claude enquanto executado localmente. Veja [Remote Control](/pt/remote-control) para sinalizadores | `claude remote-control`                            |

## Sinalizadores CLI

Personalize o comportamento do Claude Code com estes sinalizadores de linha de comando:

| Sinalizador                            | Descrição                                                                                                                                                                                                                                    | Exemplo                                                                                            |
| :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| `--add-dir`                            | Adicionar diretórios de trabalho adicionais para Claude acessar (valida se cada caminho existe como um diretório)                                                                                                                            | `claude --add-dir ../apps ../lib`                                                                  |
| `--agent`                              | Especificar um agente para a sessão atual (substitui a configuração `agent`)                                                                                                                                                                 | `claude --agent my-custom-agent`                                                                   |
| `--agents`                             | Definir [subagents](/pt/sub-agents) personalizados dinamicamente via JSON (veja abaixo o formato)                                                                                                                                            | `claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'` |
| `--allow-dangerously-skip-permissions` | Ativar bypass de permissão como uma opção sem ativá-lo imediatamente. Permite compor com `--permission-mode` (use com cuidado)                                                                                                               | `claude --permission-mode plan --allow-dangerously-skip-permissions`                               |
| `--allowedTools`                       | Ferramentas que executam sem solicitar permissão. Veja [sintaxe de regra de permissão](/pt/settings#permission-rule-syntax) para correspondência de padrões. Para restringir quais ferramentas estão disponíveis, use `--tools` em vez disso | `"Bash(git log *)" "Bash(git diff *)" "Read"`                                                      |
| `--append-system-prompt`               | Anexar texto personalizado ao final do prompt do sistema padrão                                                                                                                                                                              | `claude --append-system-prompt "Always use TypeScript"`                                            |
| `--append-system-prompt-file`          | Carregar texto de prompt do sistema adicional de um arquivo e anexar ao prompt padrão                                                                                                                                                        | `claude --append-system-prompt-file ./extra-rules.txt`                                             |
| `--betas`                              | Cabeçalhos beta para incluir em solicitações de API (apenas usuários de chave de API)                                                                                                                                                        | `claude --betas interleaved-thinking`                                                              |
| `--chrome`                             | Ativar [integração do navegador Chrome](/pt/chrome) para automação e testes da web                                                                                                                                                           | `claude --chrome`                                                                                  |
| `--continue`, `-c`                     | Carregar a conversa mais recente no diretório atual                                                                                                                                                                                          | `claude --continue`                                                                                |
| `--dangerously-skip-permissions`       | Pular todos os prompts de permissão (use com cuidado)                                                                                                                                                                                        | `claude --dangerously-skip-permissions`                                                            |
| `--debug`                              | Ativar modo de depuração com filtragem de categoria opcional (por exemplo, `"api,hooks"` ou `"!statsig,!file"`)                                                                                                                              | `claude --debug "api,mcp"`                                                                         |
| `--disable-slash-commands`             | Desativar todas as skills e comandos para esta sessão                                                                                                                                                                                        | `claude --disable-slash-commands`                                                                  |
| `--disallowedTools`                    | Ferramentas que são removidas do contexto do modelo e não podem ser usadas                                                                                                                                                                   | `"Bash(git log *)" "Bash(git diff *)" "Edit"`                                                      |
| `--fallback-model`                     | Ativar fallback automático para modelo especificado quando o modelo padrão está sobrecarregado (apenas modo print)                                                                                                                           | `claude -p --fallback-model sonnet "query"`                                                        |
| `--fork-session`                       | Ao retomar, criar um novo ID de sessão em vez de reutilizar o original (usar com `--resume` ou `--continue`)                                                                                                                                 | `claude --resume abc123 --fork-session`                                                            |
| `--from-pr`                            | Retomar sessões vinculadas a um PR específico do GitHub. Aceita um número de PR ou URL. As sessões são vinculadas automaticamente quando criadas via `gh pr create`                                                                          | `claude --from-pr 123`                                                                             |
| `--ide`                                | Conectar automaticamente ao IDE na inicialização se exatamente um IDE válido estiver disponível                                                                                                                                              | `claude --ide`                                                                                     |
| `--init`                               | Executar hooks de inicialização e iniciar modo interativo                                                                                                                                                                                    | `claude --init`                                                                                    |
| `--init-only`                          | Executar hooks de inicialização e sair (sem sessão interativa)                                                                                                                                                                               | `claude --init-only`                                                                               |
| `--include-partial-messages`           | Incluir eventos de streaming parcial na saída (requer `--print` e `--output-format=stream-json`)                                                                                                                                             | `claude -p --output-format stream-json --include-partial-messages "query"`                         |
| `--input-format`                       | Especificar formato de entrada para modo print (opções: `text`, `stream-json`)                                                                                                                                                               | `claude -p --output-format json --input-format stream-json`                                        |
| `--json-schema`                        | Obter saída JSON validada correspondendo a um JSON Schema após o agente completar seu fluxo de trabalho (apenas modo print, veja [saídas estruturadas](https://platform.claude.com/docs/en/agent-sdk/structured-outputs))                    | `claude -p --json-schema '{"type":"object","properties":{...}}' "query"`                           |
| `--maintenance`                        | Executar hooks de manutenção e sair                                                                                                                                                                                                          | `claude --maintenance`                                                                             |
| `--max-budget-usd`                     | Valor máximo em dólares a gastar em chamadas de API antes de parar (apenas modo print)                                                                                                                                                       | `claude -p --max-budget-usd 5.00 "query"`                                                          |
| `--max-turns`                          | Limitar o número de turnos agênticos (apenas modo print). Sai com um erro quando o limite é atingido. Sem limite por padrão                                                                                                                  | `claude -p --max-turns 3 "query"`                                                                  |
| `--mcp-config`                         | Carregar servidores MCP de arquivos JSON ou strings (separados por espaço)                                                                                                                                                                   | `claude --mcp-config ./mcp.json`                                                                   |
| `--model`                              | Define o modelo para a sessão atual com um alias para o modelo mais recente (`sonnet` ou `opus`) ou o nome completo de um modelo                                                                                                             | `claude --model claude-sonnet-4-6`                                                                 |
| `--no-chrome`                          | Desativar [integração do navegador Chrome](/pt/chrome) para esta sessão                                                                                                                                                                      | `claude --no-chrome`                                                                               |
| `--no-session-persistence`             | Desativar persistência de sessão para que as sessões não sejam salvas em disco e não possam ser retomadas (apenas modo print)                                                                                                                | `claude -p --no-session-persistence "query"`                                                       |
| `--output-format`                      | Especificar formato de saída para modo print (opções: `text`, `json`, `stream-json`)                                                                                                                                                         | `claude -p "query" --output-format json`                                                           |
| `--permission-mode`                    | Começar em um [modo de permissão](/pt/permissions#permission-modes) especificado                                                                                                                                                             | `claude --permission-mode plan`                                                                    |
| `--permission-prompt-tool`             | Especificar uma ferramenta MCP para lidar com prompts de permissão em modo não interativo                                                                                                                                                    | `claude -p --permission-prompt-tool mcp_auth_tool "query"`                                         |
| `--plugin-dir`                         | Carregar plugins de diretórios apenas para esta sessão (repetível)                                                                                                                                                                           | `claude --plugin-dir ./my-plugins`                                                                 |
| `--print`, `-p`                        | Imprimir resposta sem modo interativo (veja [documentação do Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) para detalhes de uso programático)                                                                           | `claude -p "query"`                                                                                |
| `--remote`                             | Criar uma nova [sessão web](/pt/claude-code-on-the-web) em claude.ai com a descrição da tarefa fornecida                                                                                                                                     | `claude --remote "Fix the login bug"`                                                              |
| `--resume`, `-r`                       | Retomar uma sessão específica por ID ou nome, ou mostrar um seletor interativo para escolher uma sessão                                                                                                                                      | `claude --resume auth-refactor`                                                                    |
| `--session-id`                         | Usar um ID de sessão específico para a conversa (deve ser um UUID válido)                                                                                                                                                                    | `claude --session-id "550e8400-e29b-41d4-a716-446655440000"`                                       |
| `--setting-sources`                    | Lista separada por vírgula de fontes de configuração a carregar (`user`, `project`, `local`)                                                                                                                                                 | `claude --setting-sources user,project`                                                            |
| `--settings`                           | Caminho para um arquivo JSON de configurações ou uma string JSON para carregar configurações adicionais                                                                                                                                      | `claude --settings ./settings.json`                                                                |
| `--strict-mcp-config`                  | Usar apenas servidores MCP de `--mcp-config`, ignorando todas as outras configurações de MCP                                                                                                                                                 | `claude --strict-mcp-config --mcp-config ./mcp.json`                                               |
| `--system-prompt`                      | Substituir todo o prompt do sistema por texto personalizado                                                                                                                                                                                  | `claude --system-prompt "You are a Python expert"`                                                 |
| `--system-prompt-file`                 | Carregar prompt do sistema de um arquivo, substituindo o prompt padrão                                                                                                                                                                       | `claude --system-prompt-file ./custom-prompt.txt`                                                  |
| `--teleport`                           | Retomar uma [sessão web](/pt/claude-code-on-the-web) em seu terminal local                                                                                                                                                                   | `claude --teleport`                                                                                |
| `--teammate-mode`                      | Definir como [equipe de agentes](/pt/agent-teams) colegas de equipe são exibidos: `auto` (padrão), `in-process` ou `tmux`. Veja [configurar equipes de agentes](/pt/agent-teams#set-up-agent-teams)                                          | `claude --teammate-mode in-process`                                                                |
| `--tools`                              | Restringir quais ferramentas integradas Claude pode usar. Use `""` para desativar todas, `"default"` para todas, ou nomes de ferramentas como `"Bash,Edit,Read"`                                                                             | `claude --tools "Bash,Edit,Read"`                                                                  |
| `--verbose`                            | Ativar logging detalhado, mostra saída completa turno a turno                                                                                                                                                                                | `claude --verbose`                                                                                 |
| `--version`, `-v`                      | Exibir o número da versão                                                                                                                                                                                                                    | `claude -v`                                                                                        |
| `--worktree`, `-w`                     | Iniciar Claude em um [git worktree](/pt/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) isolado em `<repo>/.claude/worktrees/<name>`. Se nenhum nome for fornecido, um será gerado automaticamente                    | `claude -w feature-auth`                                                                           |

<Tip>
  O sinalizador `--output-format json` é particularmente útil para scripts e
  automação, permitindo que você analise as respostas do Claude programaticamente.
</Tip>

### Formato do sinalizador agents

O sinalizador `--agents` aceita um objeto JSON que define um ou mais subagents personalizados. Cada subagent requer um nome único (como a chave) e um objeto de definição com os seguintes campos:

| Campo             | Obrigatório | Descrição                                                                                                                                                                                                                                |
| :---------------- | :---------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `description`     | Sim         | Descrição em linguagem natural de quando o subagent deve ser invocado                                                                                                                                                                    |
| `prompt`          | Sim         | O prompt do sistema que guia o comportamento do subagent                                                                                                                                                                                 |
| `tools`           | Não         | Array de ferramentas específicas que o subagent pode usar, por exemplo `["Read", "Edit", "Bash"]`. Se omitido, herda todas as ferramentas. Suporta sintaxe [`Agent(agent_type)`](/pt/sub-agents#restrict-which-subagents-can-be-spawned) |
| `disallowedTools` | Não         | Array de nomes de ferramentas para negar explicitamente para este subagent                                                                                                                                                               |
| `model`           | Não         | Alias de modelo a usar: `sonnet`, `opus`, `haiku` ou `inherit`. Se omitido, padrão é `inherit`                                                                                                                                           |
| `skills`          | Não         | Array de nomes de [skill](/pt/skills) para pré-carregar no contexto do subagent                                                                                                                                                          |
| `mcpServers`      | Não         | Array de [servidores MCP](/pt/mcp) para este subagent. Cada entrada é uma string de nome de servidor ou um objeto `{name: config}`                                                                                                       |
| `maxTurns`        | Não         | Número máximo de turnos agênticos antes do subagent parar                                                                                                                                                                                |

Exemplo:

```bash  theme={null}
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

Para mais detalhes sobre como criar e usar subagents, veja a [documentação de subagents](/pt/sub-agents).

### Sinalizadores de prompt do sistema

Claude Code fornece quatro sinalizadores para personalizar o prompt do sistema. Todos os quatro funcionam em modos interativo e não interativo.

| Sinalizador                   | Comportamento                                  | Caso de uso                                                                     |
| :---------------------------- | :--------------------------------------------- | :------------------------------------------------------------------------------ |
| `--system-prompt`             | **Substitui** todo o prompt padrão             | Controle completo sobre o comportamento e instruções do Claude                  |
| `--system-prompt-file`        | **Substitui** com conteúdo do arquivo          | Carregar prompts de arquivos para reprodutibilidade e controle de versão        |
| `--append-system-prompt`      | **Anexa** ao prompt padrão                     | Adicionar instruções específicas mantendo o comportamento padrão do Claude Code |
| `--append-system-prompt-file` | **Anexa** conteúdo do arquivo ao prompt padrão | Carregar instruções adicionais de arquivos mantendo os padrões                  |

**Quando usar cada um:**

* **`--system-prompt`**: use quando você precisa de controle completo sobre o prompt do sistema do Claude. Isso remove todas as instruções padrão do Claude Code, dando a você uma folha em branco.
  ```bash  theme={null}
  claude --system-prompt "You are a Python expert who only writes type-annotated code"
  ```

* **`--system-prompt-file`**: use quando você quer carregar um prompt personalizado de um arquivo, útil para consistência de equipe ou modelos de prompt controlados por versão.
  ```bash  theme={null}
  claude --system-prompt-file ./prompts/code-review.txt
  ```

* **`--append-system-prompt`**: use quando você quer adicionar instruções específicas mantendo as capacidades padrão do Claude Code intactas. Esta é a opção mais segura para a maioria dos casos de uso.
  ```bash  theme={null}
  claude --append-system-prompt "Always use TypeScript and include JSDoc comments"
  ```

* **`--append-system-prompt-file`**: use quando você quer anexar instruções de um arquivo mantendo os padrões do Claude Code. Útil para adições controladas por versão.
  ```bash  theme={null}
  claude --append-system-prompt-file ./prompts/style-rules.txt
  ```

`--system-prompt` e `--system-prompt-file` são mutuamente exclusivos. Os sinalizadores de anexação podem ser usados juntos com qualquer sinalizador de substituição.

Para a maioria dos casos de uso, `--append-system-prompt` ou `--append-system-prompt-file` é recomendado, pois preservam as capacidades integradas do Claude Code enquanto adicionam seus requisitos personalizados. Use `--system-prompt` ou `--system-prompt-file` apenas quando você precisar de controle completo sobre o prompt do sistema.

## Veja também

* [Extensão Chrome](/pt/chrome) - Automação de navegador e testes da web
* [Modo interativo](/pt/interactive-mode) - Atalhos, modos de entrada e recursos interativos
* [Guia de início rápido](/pt/quickstart) - Começar com Claude Code
* [Fluxos de trabalho comuns](/pt/common-workflows) - Fluxos de trabalho e padrões avançados
* [Configurações](/pt/settings) - Opções de configuração
* [Documentação do Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) - Uso programático e integrações
