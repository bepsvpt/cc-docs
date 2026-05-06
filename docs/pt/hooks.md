> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Referência de hooks

> Referência para eventos de hooks do Claude Code, esquema de configuração, formatos de entrada/saída JSON, códigos de saída, hooks assíncronos, hooks HTTP, hooks de prompt e hooks de ferramentas MCP.

<Tip>
  Para um guia de início rápido com exemplos, consulte [Automatizar fluxos de trabalho com hooks](/pt/hooks-guide).
</Tip>

Hooks são comandos shell definidos pelo usuário, endpoints HTTP ou prompts LLM que executam automaticamente em pontos específicos do ciclo de vida do Claude Code. Use esta referência para consultar esquemas de eventos, opções de configuração, formatos de entrada/saída JSON e recursos avançados como hooks assíncronos, hooks HTTP e hooks de ferramentas MCP. Se você está configurando hooks pela primeira vez, comece com o [guia](/pt/hooks-guide) em vez disso.

## Ciclo de vida do hook

Hooks disparam em pontos específicos durante uma sessão do Claude Code. Quando um evento dispara e um matcher corresponde, o Claude Code passa contexto JSON sobre o evento para seu manipulador de hook. Para hooks de comando, a entrada chega em stdin. Para hooks HTTP, chega como corpo da solicitação POST. Seu manipulador pode então inspecionar a entrada, tomar ação e opcionalmente retornar uma decisão. Os eventos caem em três cadências: uma vez por sessão (`SessionStart`, `SessionEnd`), uma vez por turno (`UserPromptSubmit`, `Stop`, `StopFailure`) e em cada chamada de ferramenta dentro do loop agentic (`PreToolUse`, `PostToolUse`):

<div style={{maxWidth: "500px", margin: "0 auto"}}>
  <Frame>
    <img src="https://mintcdn.com/claude-code/ZIW26Z9pnpsXLhbS/images/hooks-lifecycle.svg?fit=max&auto=format&n=ZIW26Z9pnpsXLhbS&q=85&s=ee23691324deb6501df09bfdae560b64" alt="Diagrama do ciclo de vida do hook mostrando Setup opcional alimentando SessionStart, depois um loop por turno contendo UserPromptSubmit, UserPromptExpansion para slash commands, o loop agentic aninhado (PreToolUse, PermissionRequest, PostToolUse, PostToolUseFailure, PostToolBatch, SubagentStart/Stop, TaskCreated, TaskCompleted) e Stop ou StopFailure, seguido por TeammateIdle, PreCompact, PostCompact e SessionEnd, com Elicitation e ElicitationResult aninhados dentro da execução de ferramenta MCP, PermissionDenied como um ramo lateral de PermissionRequest para negações em modo automático, e WorktreeCreate, WorktreeRemove, Notification, ConfigChange, InstructionsLoaded, CwdChanged e FileChanged como eventos assíncronos independentes" width="520" height="1228" data-path="images/hooks-lifecycle.svg" />
  </Frame>
</div>

A tabela abaixo resume quando cada evento dispara. A seção [Eventos de hook](#hook-events) documenta o esquema de entrada completo e as opções de controle de decisão para cada um.

| Event                 | When it fires                                                                                                                                          |
| :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`        | When a session begins or resumes                                                                                                                       |
| `Setup`               | When you start Claude Code with `--init-only`, or with `--init` or `--maintenance` in `-p` mode. For one-time preparation in CI or scripts             |
| `UserPromptSubmit`    | When you submit a prompt, before Claude processes it                                                                                                   |
| `UserPromptExpansion` | When a user-typed command expands into a prompt, before it reaches Claude. Can block the expansion                                                     |
| `PreToolUse`          | Before a tool call executes. Can block it                                                                                                              |
| `PermissionRequest`   | When a permission dialog appears                                                                                                                       |
| `PermissionDenied`    | When a tool call is denied by the auto mode classifier. Return `{retry: true}` to tell the model it may retry the denied tool call                     |
| `PostToolUse`         | After a tool call succeeds                                                                                                                             |
| `PostToolUseFailure`  | After a tool call fails                                                                                                                                |
| `PostToolBatch`       | After a full batch of parallel tool calls resolves, before the next model call                                                                         |
| `Notification`        | When Claude Code sends a notification                                                                                                                  |
| `SubagentStart`       | When a subagent is spawned                                                                                                                             |
| `SubagentStop`        | When a subagent finishes                                                                                                                               |
| `TaskCreated`         | When a task is being created via `TaskCreate`                                                                                                          |
| `TaskCompleted`       | When a task is being marked as completed                                                                                                               |
| `Stop`                | When Claude finishes responding                                                                                                                        |
| `StopFailure`         | When the turn ends due to an API error. Output and exit code are ignored                                                                               |
| `TeammateIdle`        | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                                     |
| `InstructionsLoaded`  | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session         |
| `ConfigChange`        | When a configuration file changes during a session                                                                                                     |
| `CwdChanged`          | When the working directory changes, for example when Claude executes a `cd` command. Useful for reactive environment management with tools like direnv |
| `FileChanged`         | When a watched file changes on disk. The `matcher` field specifies which filenames to watch                                                            |
| `WorktreeCreate`      | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                            |
| `WorktreeRemove`      | When a worktree is being removed, either at session exit or when a subagent finishes                                                                   |
| `PreCompact`          | Before context compaction                                                                                                                              |
| `PostCompact`         | After context compaction completes                                                                                                                     |
| `Elicitation`         | When an MCP server requests user input during a tool call                                                                                              |
| `ElicitationResult`   | After a user responds to an MCP elicitation, before the response is sent back to the server                                                            |
| `SessionEnd`          | When a session terminates                                                                                                                              |

### Como um hook é resolvido

Para ver como essas peças se encaixam, considere este hook `PreToolUse` que bloqueia comandos shell destrutivos. O `matcher` se restringe a chamadas de ferramenta Bash e a condição `if` se restringe ainda mais a subcomandos Bash correspondendo a `rm *`, então `block-rm.sh` apenas é gerado quando ambos os filtros correspondem:

```json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-rm.sh"
          }
        ]
      }
    ]
  }
}
```

O script lê a entrada JSON de stdin, extrai o comando e retorna uma `permissionDecision` de `"deny"` se contiver `rm -rf`:

```bash theme={null}
#!/bin/bash
# .claude/hooks/block-rm.sh
COMMAND=$(jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q 'rm -rf'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Destructive command blocked by hook"
    }
  }'
else
  exit 0  # allow the command
fi
```

Agora suponha que o Claude Code decida executar `Bash "rm -rf /tmp/build"`. Aqui está o que acontece:

<Frame>
  <img src="https://mintcdn.com/claude-code/-tYw1BD_DEqfyyOZ/images/hook-resolution.svg?fit=max&auto=format&n=-tYw1BD_DEqfyyOZ&q=85&s=c73ebc1eeda2037570427d7af1e0a891" alt="Fluxo de resolução de hook: evento PreToolUse dispara, matcher verifica correspondência de Bash, condição if verifica correspondência de Bash(rm *), manipulador de hook executa, resultado retorna ao Claude Code" width="930" height="290" data-path="images/hook-resolution.svg" />
</Frame>

<Steps>
  <Step title="Evento dispara">
    O evento `PreToolUse` dispara. O Claude Code envia a entrada da ferramenta como JSON em stdin para o hook:

    ```json theme={null}
    { "tool_name": "Bash", "tool_input": { "command": "rm -rf /tmp/build" }, ... }
    ```
  </Step>

  <Step title="Matcher verifica">
    O matcher `"Bash"` corresponde ao nome da ferramenta, então este grupo de hook é ativado. Se você omitir o matcher ou usar `"*"`, o grupo é ativado em cada ocorrência do evento.
  </Step>

  <Step title="Condição if verifica">
    A condição `if` `"Bash(rm *)"` corresponde porque `rm -rf /tmp/build` é um subcomando correspondendo a `rm *`, então este manipulador é gerado. Se o comando tivesse sido `npm test`, a verificação `if` falharia e `block-rm.sh` nunca seria executado, evitando a sobrecarga de geração de processo. O campo `if` é opcional; sem ele, cada manipulador no grupo correspondido é executado.
  </Step>

  <Step title="Manipulador de hook executa">
    O script inspeciona o comando completo e encontra `rm -rf`, então imprime uma decisão em stdout:

    ```json theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Destructive command blocked by hook"
      }
    }
    ```

    Se o comando tivesse sido uma variante mais segura de `rm` como `rm file.txt`, o script teria atingido `exit 0` em vez disso, o que diz ao Claude Code para permitir a chamada da ferramenta sem ação adicional.
  </Step>

  <Step title="Claude Code age sobre o resultado">
    O Claude Code lê a decisão JSON, bloqueia a chamada da ferramenta e mostra a razão ao Claude.
  </Step>
</Steps>

A seção [Configuração](#configuration) abaixo documenta o esquema completo, e cada seção [evento de hook](#hook-events) documenta qual entrada seu comando recebe e qual saída pode retornar.

## Configuração

Hooks são definidos em arquivos de configurações JSON. A configuração tem três níveis de aninhamento:

1. Escolha um [evento de hook](#hook-events) para responder, como `PreToolUse` ou `Stop`
2. Adicione um [grupo de matcher](#matcher-patterns) para filtrar quando dispara, como "apenas para a ferramenta Bash"
3. Defina um ou mais [manipuladores de hook](#hook-handler-fields) para executar quando correspondido

Consulte [Como um hook é resolvido](#how-a-hook-resolves) acima para um passo a passo completo com um exemplo anotado.

<Note>
  Esta página usa termos específicos para cada nível: **evento de hook** para o ponto do ciclo de vida, **grupo de matcher** para o filtro e **manipulador de hook** para o comando shell, endpoint HTTP, ferramenta MCP, prompt ou agente que executa. "Hook" por si só refere-se ao recurso geral.
</Note>

### Locais de hooks

Onde você define um hook determina seu escopo:

| Local                                                          | Escopo                           | Compartilhável                          |
| :------------------------------------------------------------- | :------------------------------- | :-------------------------------------- |
| `~/.claude/settings.json`                                      | Todos os seus projetos           | Não, local para sua máquina             |
| `.claude/settings.json`                                        | Projeto único                    | Sim, pode ser confirmado no repositório |
| `.claude/settings.local.json`                                  | Projeto único                    | Não, gitignored                         |
| Configurações de política gerenciada                           | Organização inteira              | Sim, controlado por administrador       |
| [Plugin](/pt/plugins) `hooks/hooks.json`                       | Quando o plugin está ativado     | Sim, agrupado com o plugin              |
| Frontmatter de [Skill](/pt/skills) ou [agente](/pt/sub-agents) | Enquanto o componente está ativo | Sim, definido no arquivo do componente  |

Para detalhes sobre resolução de arquivo de configurações, consulte [configurações](/pt/settings). Administradores corporativos podem usar `allowManagedHooksOnly` para bloquear hooks de usuário, projeto e plugin. Hooks de plugins forçadamente ativados em configurações gerenciadas `enabledPlugins` são isentos, para que administradores possam distribuir hooks verificados através de um marketplace de organização. Consulte [Configuração de hook](/pt/settings#hook-configuration).

### Padrões de matcher

O campo `matcher` filtra quando hooks disparam. Como um matcher é avaliado depende dos caracteres que contém:

| Valor do matcher                   | Avaliado como                                              | Exemplo                                                                                                                                    |
| :--------------------------------- | :--------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| `"*"`, `""` ou omitido             | Corresponder a todos                                       | dispara em cada ocorrência do evento                                                                                                       |
| Apenas letras, dígitos, `_` e `\|` | String exata ou lista de strings exatas separadas por `\|` | `Bash` corresponde apenas à ferramenta Bash; `Edit\|Write` corresponde a qualquer ferramenta exatamente                                    |
| Contém qualquer outro caractere    | Expressão regular JavaScript                               | `^Notebook` corresponde a qualquer ferramenta começando com Notebook; `mcp__memory__.*` corresponde a cada ferramenta do servidor `memory` |

O evento `FileChanged` não segue essas regras ao construir sua lista de monitoramento. Consulte [FileChanged](#filechanged).

Cada tipo de evento corresponde em um campo diferente:

| Evento                                                                                                                          | O que o matcher filtra                                                          | Valores de matcher de exemplo                                                                                                                      |
| :------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`                                      | nome da ferramenta                                                              | `Bash`, `Edit\|Write`, `mcp__.*`                                                                                                                   |
| `SessionStart`                                                                                                                  | como a sessão começou                                                           | `startup`, `resume`, `clear`, `compact`                                                                                                            |
| `Setup`                                                                                                                         | qual sinalizador CLI acionou a configuração                                     | `init`, `maintenance`                                                                                                                              |
| `SessionEnd`                                                                                                                    | por que a sessão terminou                                                       | `clear`, `resume`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`                                                           |
| `Notification`                                                                                                                  | tipo de notificação                                                             | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`, `elicitation_complete`, `elicitation_response`                           |
| `SubagentStart`                                                                                                                 | tipo de agente                                                                  | `general-purpose`, `Explore`, `Plan` ou nomes de agentes personalizados                                                                            |
| `PreCompact`, `PostCompact`                                                                                                     | o que acionou a compactação                                                     | `manual`, `auto`                                                                                                                                   |
| `SubagentStop`                                                                                                                  | tipo de agente                                                                  | mesmos valores que `SubagentStart`                                                                                                                 |
| `ConfigChange`                                                                                                                  | fonte de configuração                                                           | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills`                                                                 |
| `CwdChanged`                                                                                                                    | sem suporte a matcher                                                           | sempre dispara em cada mudança de diretório                                                                                                        |
| `FileChanged`                                                                                                                   | nomes de arquivo literais para monitorar (consulte [FileChanged](#filechanged)) | `.envrc\|.env`                                                                                                                                     |
| `StopFailure`                                                                                                                   | tipo de erro                                                                    | `rate_limit`, `authentication_failed`, `oauth_org_not_allowed`, `billing_error`, `invalid_request`, `server_error`, `max_output_tokens`, `unknown` |
| `InstructionsLoaded`                                                                                                            | razão de carregamento                                                           | `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact`                                                                       |
| `UserPromptExpansion`                                                                                                           | nome do comando                                                                 | seus nomes de skill ou comando                                                                                                                     |
| `Elicitation`                                                                                                                   | nome do servidor MCP                                                            | seus nomes de servidor MCP configurados                                                                                                            |
| `ElicitationResult`                                                                                                             | nome do servidor MCP                                                            | mesmos valores que `Elicitation`                                                                                                                   |
| `UserPromptSubmit`, `PostToolBatch`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` | sem suporte a matcher                                                           | sempre dispara em cada ocorrência                                                                                                                  |

O matcher executa contra um campo da [entrada JSON](#hook-input-and-output) que o Claude Code envia para seu hook em stdin. Para eventos de ferramenta, esse campo é `tool_name`. Cada seção [evento de hook](#hook-events) lista o conjunto completo de valores de matcher e o esquema de entrada para esse evento.

Este exemplo executa um script de linting apenas quando Claude escreve ou edita um arquivo:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/lint-check.sh"
          }
        ]
      }
    ]
  }
}
```

`UserPromptSubmit`, `PostToolBatch`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` e `CwdChanged` não suportam matchers e sempre disparam em cada ocorrência. Se você adicionar um campo `matcher` a esses eventos, ele é silenciosamente ignorado.

Para eventos de ferramenta, você pode filtrar mais estreitamente definindo o campo [`if`](#common-fields) em manipuladores de hook individuais. `if` usa [sintaxe de regra de permissão](/pt/permissions) para corresponder contra o nome da ferramenta e argumentos juntos, então `"Bash(git *)"` executa quando qualquer subcomando da entrada Bash corresponde a `git *` e `"Edit(*.ts)"` executa apenas para arquivos TypeScript.

#### Corresponder ferramentas MCP

Ferramentas de servidor [MCP](/pt/mcp) aparecem como ferramentas regulares em eventos de ferramenta (`PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`), então você pode corresponder a elas da mesma forma que corresponde a qualquer outro nome de ferramenta.

Ferramentas MCP seguem o padrão de nomenclatura `mcp__<server>__<tool>`, por exemplo:

* `mcp__memory__create_entities`: ferramenta create entities do servidor Memory
* `mcp__filesystem__read_file`: ferramenta read file do servidor Filesystem
* `mcp__github__search_repositories`: ferramenta search do servidor GitHub

Para corresponder a cada ferramenta de um servidor, anexe `.*` ao prefixo do servidor. O `.*` é obrigatório: um matcher como `mcp__memory` contém apenas letras e underscores, então é comparado como uma string exata e não corresponde a nenhuma ferramenta.

* `mcp__memory__.*` corresponde a todas as ferramentas do servidor `memory`
* `mcp__.*__write.*` corresponde a qualquer ferramenta cujo nome começa com `write` de qualquer servidor

Este exemplo registra todas as operações do servidor memory e valida operações de escrita de qualquer servidor MCP:

```json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

### Campos do manipulador de hook

Cada objeto no array `hooks` interno é um manipulador de hook: o comando shell, endpoint HTTP, ferramenta MCP, prompt LLM ou agente que executa quando o matcher corresponde. Existem cinco tipos:

* **[Hooks de comando](#command-hook-fields)** (`type: "command"`): executam um comando shell. Seu script recebe a [entrada JSON](#hook-input-and-output) do evento em stdin e comunica resultados através de códigos de saída e stdout.
* **[Hooks HTTP](#http-hook-fields)** (`type: "http"`): enviam a entrada JSON do evento como uma solicitação HTTP POST para uma URL. O endpoint comunica resultados através do corpo da resposta usando o mesmo [formato de saída JSON](#json-output) que hooks de comando.
* **[Hooks de ferramenta MCP](#mcp-tool-hook-fields)** (`type: "mcp_tool"`): chamam uma ferramenta em um servidor [MCP](/pt/mcp) já conectado. A saída de texto da ferramenta é tratada como stdout de hook de comando.
* **[Hooks de prompt](#prompt-and-agent-hook-fields)** (`type: "prompt"`): enviam um prompt para um modelo Claude para avaliação de turno único. O modelo retorna uma decisão sim/não como JSON. Consulte [Hooks baseados em prompt](#prompt-based-hooks).
* **[Hooks de agente](#prompt-and-agent-hook-fields)** (`type: "agent"`): geram um subagente que pode usar ferramentas como Read, Grep e Glob para verificar condições antes de retornar uma decisão. Hooks de agente são experimentais e podem mudar. Consulte [Hooks baseados em agente](#agent-based-hooks).

#### Campos comuns

Esses campos se aplicam a todos os tipos de hook:

| Campo           | Obrigatório | Descrição                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| :-------------- | :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `type`          | sim         | `"command"`, `"http"`, `"mcp_tool"`, `"prompt"` ou `"agent"`                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `if`            | não         | Sintaxe de regra de permissão para filtrar quando este hook executa, como `"Bash(git *)"` ou `"Edit(*.ts)"`. O hook apenas é gerado se a chamada de ferramenta corresponde ao padrão, ou se um comando Bash é muito complexo para analisar. Apenas avaliado em eventos de ferramenta: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest` e `PermissionDenied`. Em outros eventos, um hook com `if` definido nunca executa. Usa a mesma sintaxe que [regras de permissão](/pt/permissions) |
| `timeout`       | não         | Segundos antes de cancelar. Padrões: 600 para comando, 30 para prompt, 60 para agente                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `statusMessage` | não         | Mensagem de spinner personalizada exibida enquanto o hook executa                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `once`          | não         | Se `true`, executa apenas uma vez por sessão e depois é removido. Apenas honrado para hooks declarados em [frontmatter de skill](#hooks-in-skills-and-agents); ignorado em arquivos de configurações e frontmatter de agente                                                                                                                                                                                                                                                                                  |

O campo `if` contém exatamente uma regra de permissão. Não há sintaxe `&&`, `||` ou lista para combinar regras; para aplicar múltiplas condições, defina um manipulador de hook separado para cada. Para Bash, a regra é correspondida contra cada subcomando da entrada da ferramenta após atribuições `VAR=value` iniciais serem removidas, então `if: "Bash(git push *)"` corresponde tanto a `FOO=bar git push` quanto a `npm test && git push`. O hook executa se qualquer subcomando corresponde, e sempre executa quando o comando é muito complexo para analisar.

#### Campos de hook de comando

Além dos [campos comuns](#common-fields), hooks de comando aceitam esses campos:

| Campo         | Obrigatório | Descrição                                                                                                                                                                                                                                                      |
| :------------ | :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `command`     | sim         | Comando shell a executar                                                                                                                                                                                                                                       |
| `async`       | não         | Se `true`, executa em background sem bloquear. Consulte [Executar hooks em background](#run-hooks-in-the-background)                                                                                                                                           |
| `asyncRewake` | não         | Se `true`, executa em background e acorda Claude na saída do código 2. Implica `async`. O stderr do hook, ou stdout se stderr estiver vazio, é mostrado ao Claude como um lembrete do sistema para que possa reagir a uma falha de background de longa duração |
| `shell`       | não         | Shell a usar para este hook. Aceita `"bash"` (padrão) ou `"powershell"`. Definir `"powershell"` executa o comando via PowerShell no Windows. Não requer `CLAUDE_CODE_USE_POWERSHELL_TOOL` já que hooks geram PowerShell diretamente                            |

#### Campos de hook HTTP

Além dos [campos comuns](#common-fields), hooks HTTP aceitam esses campos:

| Campo            | Obrigatório | Descrição                                                                                                                                                                                                                                      |
| :--------------- | :---------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`            | sim         | URL para enviar a solicitação POST                                                                                                                                                                                                             |
| `headers`        | não         | Cabeçalhos HTTP adicionais como pares chave-valor. Valores suportam interpolação de variável de ambiente usando sintaxe `$VAR_NAME` ou `${VAR_NAME}`. Apenas variáveis listadas em `allowedEnvVars` são resolvidas                             |
| `allowedEnvVars` | não         | Lista de nomes de variáveis de ambiente que podem ser interpoladas em valores de cabeçalho. Referências a variáveis não listadas são substituídas por strings vazias. Obrigatório para qualquer interpolação de variável de ambiente funcionar |

O Claude Code envia a [entrada JSON](#hook-input-and-output) do hook como corpo da solicitação POST com `Content-Type: application/json`. O corpo da resposta usa o mesmo [formato de saída JSON](#json-output) que hooks de comando.

O tratamento de erros difere dos hooks de comando: respostas não-2xx, falhas de conexão e timeouts todos produzem erros não-bloqueadores que permitem que a execução continue. Para bloquear uma chamada de ferramenta ou negar uma permissão, retorne uma resposta 2xx com um corpo JSON contendo `decision: "block"` ou um `hookSpecificOutput` com `permissionDecision: "deny"`.

Este exemplo envia eventos `PreToolUse` para um serviço de validação local, autenticando com um token da variável de ambiente `MY_TOKEN`:

```json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/pre-tool-use",
            "timeout": 30,
            "headers": {
              "Authorization": "Bearer $MY_TOKEN"
            },
            "allowedEnvVars": ["MY_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

#### Campos de hook de ferramenta MCP

Além dos [campos comuns](#common-fields), hooks de ferramenta MCP aceitam esses campos:

| Campo    | Obrigatório | Descrição                                                                                                                                                                    |
| :------- | :---------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `server` | sim         | Nome de um servidor MCP configurado. O servidor já deve estar conectado; o hook nunca dispara um fluxo OAuth ou de conexão                                                   |
| `tool`   | sim         | Nome da ferramenta a chamar naquele servidor                                                                                                                                 |
| `input`  | não         | Argumentos passados para a ferramenta. Valores de string suportam substituição `${path}` da [entrada JSON](#hook-input-and-output) do hook, como `"${tool_input.file_path}"` |

A saída de texto da ferramenta é tratada como stdout de hook de comando: se analisar como [saída JSON](#json-output) válida, é processada como uma decisão, caso contrário, é mostrada como texto simples. Se o servidor nomeado não estiver conectado, ou a ferramenta retornar `isError: true`, o hook produz um erro não-bloqueador e a execução continua.

Hooks de ferramenta MCP estão disponíveis em cada evento de hook uma vez que o Claude Code tenha se conectado aos seus servidores MCP. `SessionStart` e `Setup` normalmente disparam antes dos servidores terminarem de conectar, então hooks nesses eventos devem esperar o erro "não conectado" na primeira execução.

Este exemplo chama a ferramenta `security_scan` no servidor MCP `my_server` após cada `Write` ou `Edit`, passando o caminho do arquivo editado:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "mcp_tool",
            "server": "my_server",
            "tool": "security_scan",
            "input": { "file_path": "${tool_input.file_path}" }
          }
        ]
      }
    ]
  }
}
```

#### Campos de hook de prompt e agente

Além dos [campos comuns](#common-fields), hooks de prompt e agente aceitam esses campos:

| Campo    | Obrigatório | Descrição                                                                                             |
| :------- | :---------- | :---------------------------------------------------------------------------------------------------- |
| `prompt` | sim         | Texto do prompt a enviar para o modelo. Use `$ARGUMENTS` como placeholder para a entrada JSON do hook |
| `model`  | não         | Modelo a usar para avaliação. Padrão para um modelo rápido                                            |

Todos os hooks correspondentes executam em paralelo, e manipuladores idênticos são automaticamente desduplicados. Hooks de comando são desduplicados por string de comando, e hooks HTTP são desduplicados por URL. Manipuladores executam no diretório atual com o ambiente do Claude Code. A variável de ambiente `$CLAUDE_CODE_REMOTE` é definida como `"true"` em ambientes web remotos e não é definida na CLI local.

### Referenciar scripts por caminho

Use variáveis de ambiente para referenciar scripts de hook relativos à raiz do projeto ou plugin, independentemente do diretório de trabalho quando o hook executa:

* `$CLAUDE_PROJECT_DIR`: a raiz do projeto. Envolva em aspas para lidar com caminhos com espaços.
* `${CLAUDE_PLUGIN_ROOT}`: o diretório raiz do plugin, para scripts agrupados com um [plugin](/pt/plugins). Muda em cada atualização de plugin.
* `${CLAUDE_PLUGIN_DATA}`: o [diretório de dados persistentes](/pt/plugins-reference#persistent-data-directory) do plugin, para dependências e estado que devem sobreviver a atualizações de plugin.

<Tabs>
  <Tab title="Scripts de projeto">
    Este exemplo usa `$CLAUDE_PROJECT_DIR` para executar um verificador de estilo do diretório `.claude/hooks/` do projeto após qualquer chamada de ferramenta `Write` ou `Edit`:

    ```json theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-style.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Scripts de plugin">
    Defina hooks de plugin em `hooks/hooks.json` com um campo `description` opcional de nível superior. Quando um plugin está ativado, seus hooks se mesclam com seus hooks de usuário e projeto.

    Este exemplo executa um script de formatação agrupado com o plugin:

    ```json theme={null}
    {
      "description": "Automatic code formatting",
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
                "timeout": 30
              }
            ]
          }
        ]
      }
    }
    ```

    Consulte a [referência de componentes de plugin](/pt/plugins-reference#hooks) para detalhes sobre como criar hooks de plugin.
  </Tab>
</Tabs>

### Hooks em skills e agentes

Além de arquivos de configurações e plugins, hooks podem ser definidos diretamente em [skills](/pt/skills) e [subagentes](/pt/sub-agents) usando frontmatter. Esses hooks são escopo do ciclo de vida do componente e apenas executam quando esse componente está ativo.

Todos os eventos de hook são suportados. Para subagentes, hooks `Stop` são automaticamente convertidos para `SubagentStop` já que esse é o evento que dispara quando um subagente completa.

Hooks usam o mesmo formato de configuração que hooks baseados em configurações, mas são escopo da vida útil do componente e limpos quando termina.

Esta skill define um hook `PreToolUse` que executa um script de validação de segurança antes de cada comando `Bash`:

```yaml theme={null}
---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---
```

Agentes usam o mesmo formato em seu frontmatter YAML.

### O menu `/hooks`

Digite `/hooks` no Claude Code para abrir um navegador somente leitura para seus hooks configurados. O menu mostra cada evento de hook com uma contagem de hooks configurados, permite que você detalhe em matchers e mostra os detalhes completos de cada manipulador de hook. Use-o para verificar configuração, verificar qual arquivo de configurações um hook veio, ou inspecionar comando, prompt ou URL de um hook.

O menu exibe todos os cinco tipos de hook: `command`, `prompt`, `agent`, `http` e `mcp_tool`. Cada hook é rotulado com um prefixo `[type]` e uma fonte indicando onde foi definido:

* `User`: de `~/.claude/settings.json`
* `Project`: de `.claude/settings.json`
* `Local`: de `.claude/settings.local.json`
* `Plugin`: de `hooks/hooks.json` de um plugin
* `Session`: registrado em memória para a sessão atual
* `Built-in`: registrado internamente pelo Claude Code

Selecionar um hook abre uma visualização de detalhes mostrando seu evento, matcher, tipo, arquivo de origem e o comando, prompt ou URL completo. O menu é somente leitura: para adicionar, modificar ou remover hooks, edite o JSON de configurações diretamente ou peça ao Claude para fazer a mudança.

### Desabilitar ou remover hooks

Para remover um hook, delete sua entrada do arquivo de configurações JSON.

Para desabilitar temporariamente todos os hooks sem removê-los, defina `"disableAllHooks": true` em seu arquivo de configurações. Não há forma de desabilitar um hook individual mantendo-o na configuração.

A configuração `disableAllHooks` respeita a hierarquia de configurações gerenciadas. Se um administrador configurou hooks através de configurações de política gerenciada, `disableAllHooks` definido em configurações de usuário, projeto ou local não pode desabilitar esses hooks gerenciados. Apenas `disableAllHooks` definido no nível de configurações gerenciadas pode desabilitar hooks gerenciados.

Edições diretas a hooks em arquivos de configurações são normalmente capturadas automaticamente pelo observador de arquivo.

## Entrada e saída de hook

Hooks de comando recebem dados JSON via stdin e comunicam resultados através de códigos de saída, stdout e stderr. Hooks HTTP recebem o mesmo JSON como corpo da solicitação POST e comunicam resultados através do corpo da resposta HTTP. Esta seção cobre campos e comportamento comuns a todos os eventos. Cada seção de evento sob [Eventos de hook](#hook-events) inclui seu esquema de entrada específico e opções de controle de decisão.

### Campos de entrada comuns

Eventos de hook recebem esses campos como JSON, além de campos específicos do evento documentados em cada seção [evento de hook](#hook-events). Para hooks de comando, este JSON chega via stdin. Para hooks HTTP, chega como corpo da solicitação POST.

| Campo             | Descrição                                                                                                                                                                                                                                                |
| :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `session_id`      | Identificador de sessão atual                                                                                                                                                                                                                            |
| `transcript_path` | Caminho para JSON de conversa                                                                                                                                                                                                                            |
| `cwd`             | Diretório de trabalho atual quando o hook é invocado                                                                                                                                                                                                     |
| `permission_mode` | [Modo de permissão](/pt/permissions#permission-modes) atual: `"default"`, `"plan"`, `"acceptEdits"`, `"auto"`, `"dontAsk"` ou `"bypassPermissions"`. Nem todos os eventos recebem este campo: consulte cada exemplo JSON de evento abaixo para verificar |
| `hook_event_name` | Nome do evento que disparou                                                                                                                                                                                                                              |

Ao executar com `--agent` ou dentro de um subagente, dois campos adicionais são incluídos:

| Campo        | Descrição                                                                                                                                                                                                                                    |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agent_id`   | Identificador único para o subagente. Presente apenas quando o hook dispara dentro de uma chamada de subagente. Use isso para distinguir chamadas de hook de subagente de chamadas de thread principal.                                      |
| `agent_type` | Nome do agente (por exemplo, `"Explore"` ou `"security-reviewer"`). Presente quando a sessão usa `--agent` ou o hook dispara dentro de um subagente. Para subagentes, o tipo do subagente tem precedência sobre o valor `--agent` da sessão. |

Por exemplo, um hook `PreToolUse` para um comando Bash recebe isso em stdin:

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl",
  "cwd": "/home/user/my-project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}
```

Os campos `tool_name` e `tool_input` são específicos do evento. Cada seção [evento de hook](#hook-events) documenta os campos adicionais para esse evento.

### Saída de código de saída

O código de saída do seu comando de hook diz ao Claude Code se a ação deve prosseguir, ser bloqueada ou ser ignorada.

**Saída 0** significa sucesso. O Claude Code analisa stdout para [campos de saída JSON](#json-output). A saída JSON é apenas processada na saída 0. Para a maioria dos eventos, stdout é escrito no log de debug, mas não mostrado na transcrição. As exceções são `UserPromptSubmit`, `UserPromptExpansion` e `SessionStart`, onde stdout é adicionado como contexto que Claude pode ver e agir.

**Saída 2** significa um erro bloqueador. O Claude Code ignora stdout e qualquer JSON nele. Em vez disso, texto de stderr é alimentado de volta ao Claude como uma mensagem de erro. O efeito depende do evento: `PreToolUse` bloqueia a chamada da ferramenta, `UserPromptSubmit` rejeita o prompt e assim por diante. Consulte [comportamento de código de saída 2](#exit-code-2-behavior-per-event) para a lista completa.

**Qualquer outro código de saída** é um erro não-bloqueador para a maioria dos eventos de hook. A transcrição mostra um aviso `<hook name> hook error` seguido pela primeira linha de stderr, para que você possa identificar a causa sem `--debug`. A execução continua e o stderr completo é escrito no log de debug.

Por exemplo, um script de comando de hook que bloqueia comandos Bash perigosos:

```bash theme={null}
#!/bin/bash
# Lê entrada JSON de stdin, verifica o comando
command=$(jq -r '.tool_input.command' < /dev/stdin)

if [[ "$command" == rm* ]]; then
  echo "Blocked: rm commands are not allowed" >&2
  exit 2  # Erro bloqueador: chamada de ferramenta é prevenida
fi

exit 0  # Sucesso: chamada de ferramenta prossegue
```

<Warning>
  Para a maioria dos eventos de hook, apenas o código de saída 2 bloqueia a ação. O Claude Code trata o código de saída 1 como um erro não-bloqueador e prossegue com a ação, mesmo que 1 seja o código de falha Unix convencional. Se seu hook se destina a impor uma política, use `exit 2`. A exceção é `WorktreeCreate`, onde qualquer código de saída não-zero aborta a criação de worktree.
</Warning>

#### Comportamento de código de saída 2 por evento

Código de saída 2 é a forma de um hook sinalizar "pare, não faça isso". O efeito depende do evento, porque alguns eventos representam ações que podem ser bloqueadas (como uma chamada de ferramenta que ainda não aconteceu) e outros representam coisas que já aconteceram ou não podem ser prevenidas.

| Evento de hook        | Pode bloquear? | O que acontece na saída 2                                                                                                                             |
| :-------------------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PreToolUse`          | Sim            | Bloqueia a chamada da ferramenta                                                                                                                      |
| `PermissionRequest`   | Sim            | Nega a permissão                                                                                                                                      |
| `UserPromptSubmit`    | Sim            | Bloqueia o processamento de prompt e apaga o prompt                                                                                                   |
| `UserPromptExpansion` | Sim            | Bloqueia a expansão                                                                                                                                   |
| `Stop`                | Sim            | Previne Claude de parar, continua a conversa                                                                                                          |
| `SubagentStop`        | Sim            | Previne o subagente de parar                                                                                                                          |
| `TeammateIdle`        | Sim            | Previne o colega de ficar ocioso (colega continua trabalhando)                                                                                        |
| `TaskCreated`         | Sim            | Reverte a criação de tarefa                                                                                                                           |
| `TaskCompleted`       | Sim            | Previne a tarefa de ser marcada como concluída                                                                                                        |
| `ConfigChange`        | Sim            | Bloqueia a mudança de configuração de entrar em efeito (exceto `policy_settings`)                                                                     |
| `StopFailure`         | Não            | Saída e código de saída são ignorados                                                                                                                 |
| `PostToolUse`         | Não            | Mostra stderr ao Claude (ferramenta já executou)                                                                                                      |
| `PostToolUseFailure`  | Não            | Mostra stderr ao Claude (ferramenta já falhou)                                                                                                        |
| `PostToolBatch`       | Sim            | Para o loop agentic antes da próxima chamada de modelo                                                                                                |
| `PermissionDenied`    | Não            | Código de saída e stderr são ignorados (negação já ocorreu). Use JSON `hookSpecificOutput.retry: true` para dizer ao modelo que pode tentar novamente |
| `Notification`        | Não            | Mostra stderr apenas ao usuário                                                                                                                       |
| `SubagentStart`       | Não            | Mostra stderr apenas ao usuário                                                                                                                       |
| `SessionStart`        | Não            | Mostra stderr apenas ao usuário                                                                                                                       |
| `Setup`               | Não            | Mostra stderr apenas ao usuário                                                                                                                       |
| `SessionEnd`          | Não            | Mostra stderr apenas ao usuário                                                                                                                       |
| `CwdChanged`          | Não            | Mostra stderr apenas ao usuário                                                                                                                       |
| `FileChanged`         | Não            | Mostra stderr apenas ao usuário                                                                                                                       |
| `PreCompact`          | Sim            | Bloqueia compactação                                                                                                                                  |
| `PostCompact`         | Não            | Mostra stderr apenas ao usuário                                                                                                                       |
| `Elicitation`         | Sim            | Nega a elicitação                                                                                                                                     |
| `ElicitationResult`   | Sim            | Bloqueia a resposta (ação se torna decline)                                                                                                           |
| `WorktreeCreate`      | Sim            | Qualquer código de saída não-zero causa falha na criação de worktree                                                                                  |
| `WorktreeRemove`      | Não            | Falhas são registradas apenas em modo debug                                                                                                           |
| `InstructionsLoaded`  | Não            | Código de saída é ignorado                                                                                                                            |

### Tratamento de resposta HTTP

Hooks HTTP usam códigos de status HTTP e corpos de resposta em vez de códigos de saída e stdout:

* **2xx com corpo vazio**: sucesso, equivalente a código de saída 0 sem saída
* **2xx com corpo de texto simples**: sucesso, o texto é adicionado como contexto
* **2xx com corpo JSON**: sucesso, analisado usando o mesmo esquema [saída JSON](#json-output) que hooks de comando
* **Status não-2xx**: erro não-bloqueador, execução continua
* **Falha de conexão ou timeout**: erro não-bloqueador, execução continua

Diferentemente de hooks de comando, hooks HTTP não podem sinalizar um erro bloqueador apenas através de códigos de status. Para bloquear uma chamada de ferramenta ou negar uma permissão, retorne uma resposta 2xx com um corpo JSON contendo os campos de decisão apropriados.

### Saída JSON

Códigos de saída permitem você permitir ou bloquear, mas saída JSON oferece controle mais granular. Em vez de sair com código 2 para bloquear, saia 0 e imprima um objeto JSON em stdout. O Claude Code lê campos específicos desse JSON para controlar comportamento, incluindo [controle de decisão](#decision-control) para bloquear, permitir ou escalar para o usuário.

<Note>
  Você deve escolher uma abordagem por hook, não ambas: ou use códigos de saída sozinhos para sinalizar, ou saia 0 e imprima JSON para controle estruturado. O Claude Code apenas processa JSON na saída 0. Se você sair 2, qualquer JSON é ignorado.
</Note>

O stdout do seu hook deve conter apenas o objeto JSON. Se seu perfil shell imprime texto na inicialização, pode interferir com análise JSON. Consulte [Validação JSON falhou](/pt/hooks-guide#json-validation-failed) no guia de troubleshooting.

Saída de hook injetada em contexto (`additionalContext`, `systemMessage` ou stdout simples) é limitada a 10.000 caracteres. Saída que excede este limite é salva em um arquivo e substituída por uma visualização e caminho de arquivo, da mesma forma que resultados de ferramenta grandes são tratados.

O objeto JSON suporta três tipos de campos:

* **Campos universais** como `continue` funcionam em todos os eventos. Esses são listados na tabela abaixo.
* **`decision` e `reason` de nível superior** são usados por alguns eventos para bloquear ou fornecer feedback.
* **`hookSpecificOutput`** é um objeto aninhado para eventos que precisam de controle mais rico. Requer um campo `hookEventName` definido para o nome do evento.

| Campo            | Padrão  | Descrição                                                                                                                                    |
| :--------------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------- |
| `continue`       | `true`  | Se `false`, Claude para de processar inteiramente após o hook executar. Tem precedência sobre qualquer campo de decisão específico do evento |
| `stopReason`     | nenhum  | Mensagem mostrada ao usuário quando `continue` é `false`. Não mostrada ao Claude                                                             |
| `suppressOutput` | `false` | Se `true`, oculta stdout do log de debug                                                                                                     |
| `systemMessage`  | nenhum  | Mensagem de aviso mostrada ao usuário                                                                                                        |

Para parar Claude inteiramente independentemente do tipo de evento:

```json theme={null}
{ "continue": false, "stopReason": "Build failed, fix errors before continuing" }
```

#### Adicionar contexto para Claude

O campo `additionalContext` passa uma string do seu hook para a janela de contexto do Claude. O Claude Code envolve a string em um lembrete do sistema e a insere na conversa no ponto onde o hook disparou. Claude lê o lembrete na próxima solicitação de modelo, mas não aparece como uma mensagem de chat na interface.

Retorne `additionalContext` dentro de `hookSpecificOutput` ao lado do nome do evento:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "This file is generated. Edit src/schema.ts and run `bun generate` instead."
  }
}
```

Onde o lembrete aparece depende do evento:

* [SessionStart](#sessionstart), [Setup](#setup) e [SubagentStart](#subagentstart): no início da conversa, antes do primeiro prompt
* [UserPromptSubmit](#userpromptsubmit) e [UserPromptExpansion](#userpromptexpansion): ao lado do prompt enviado
* [PreToolUse](#pretooluse), [PostToolUse](#posttooluse), [PostToolUseFailure](#posttoolusefailure) e [PostToolBatch](#posttoolbatch): ao lado do resultado da ferramenta

Quando vários hooks retornam `additionalContext` para o mesmo evento, Claude recebe todos os valores. Se um valor exceder 10.000 caracteres, o Claude Code escreve o texto completo em um arquivo no diretório de sessão e passa ao Claude o caminho do arquivo com uma visualização curta em vez disso.

Use `additionalContext` para informações que Claude deve saber sobre o estado atual do seu ambiente ou a operação que acabou de executar:

* **Estado do ambiente**: o branch atual, alvo de implantação ou sinalizadores de recurso ativos
* **Regras de projeto condicional**: qual comando de teste se aplica ao arquivo que acabou de ser editado, quais diretórios são somente leitura nesta worktree
* **Dados externos**: problemas abertos atribuídos a você, resultados recentes de CI, conteúdo obtido de um serviço interno

Para instruções que nunca mudam, prefira [CLAUDE.md](/pt/memory). Ele carrega sem executar um script e é o lugar padrão para convenções de projeto estáticas.

Escreva o texto como declarações factuais em vez de instruções de sistema imperativas. Frases como "O alvo de implantação é produção" ou "Este repositório usa `bun test`" lê como informação de projeto. Texto enquadrado como comandos de sistema fora de banda pode disparar as defesas de injeção de prompt do Claude, o que faz com que Claude superficialize o texto para você em vez de tratá-lo como contexto.

Uma vez injetado, o texto é salvo na transcrição de sessão. Para eventos de mid-sessão como `PostToolUse` ou `UserPromptSubmit`, retomar com `--continue` ou `--resume` reproduz o texto salvo em vez de re-executar o hook para turnos anteriores, então valores como timestamps ou SHAs de commit ficam obsoletos na retomada. Hooks `SessionStart` executam novamente na retomada com `source` definido como `"resume"`, para que possam atualizar seu contexto.

#### Controle de decisão

Nem todo evento suporta bloqueio ou controle de comportamento através de JSON. Os eventos que fazem cada um usam um conjunto diferente de campos para expressar essa decisão. Use esta tabela como referência rápida antes de escrever um hook:

| Eventos                                                                                                                             | Padrão de decisão                    | Campos-chave                                                                                                                                                                                |
| :---------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| UserPromptSubmit, UserPromptExpansion, PostToolUse, PostToolUseFailure, PostToolBatch, Stop, SubagentStop, ConfigChange, PreCompact | `decision` de nível superior         | `decision: "block"`, `reason`                                                                                                                                                               |
| TeammateIdle, TaskCreated, TaskCompleted                                                                                            | Código de saída ou `continue: false` | Código de saída 2 bloqueia a ação com feedback de stderr. JSON `{"continue": false, "stopReason": "..."}` também para o colega inteiramente, correspondendo ao comportamento do hook `Stop` |
| PreToolUse                                                                                                                          | `hookSpecificOutput`                 | `permissionDecision` (allow/deny/ask/defer), `permissionDecisionReason`                                                                                                                     |
| PermissionRequest                                                                                                                   | `hookSpecificOutput`                 | `decision.behavior` (allow/deny)                                                                                                                                                            |
| PermissionDenied                                                                                                                    | `hookSpecificOutput`                 | `retry: true` diz ao modelo que pode tentar novamente a chamada de ferramenta negada                                                                                                        |
| WorktreeCreate                                                                                                                      | retorno de caminho                   | Hook de comando imprime caminho em stdout; hook HTTP retorna `hookSpecificOutput.worktreePath`. Falha de hook ou caminho ausente falha na criação                                           |
| Elicitation                                                                                                                         | `hookSpecificOutput`                 | `action` (accept/decline/cancel), `content` (valores de campo de formulário para accept)                                                                                                    |
| ElicitationResult                                                                                                                   | `hookSpecificOutput`                 | `action` (accept/decline/cancel), `content` (valores de campo de formulário override)                                                                                                       |
| WorktreeRemove, Notification, SessionEnd, PostCompact, InstructionsLoaded, StopFailure, CwdChanged, FileChanged                     | Nenhum                               | Sem controle de decisão. Usado para efeitos colaterais como logging ou limpeza                                                                                                              |

Aqui estão exemplos de cada padrão em ação:

<Tabs>
  <Tab title="Decisão de nível superior">
    Usado por `UserPromptSubmit`, `UserPromptExpansion`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `Stop`, `SubagentStop`, `ConfigChange` e `PreCompact`. O único valor é `"block"`. Para permitir que a ação prossiga, omita `decision` do seu JSON ou saia 0 sem qualquer JSON:

    ```json theme={null}
    {
      "decision": "block",
      "reason": "Test suite must pass before proceeding"
    }
    ```
  </Tab>

  <Tab title="PreToolUse">
    Usa `hookSpecificOutput` para controle mais rico: permitir, negar ou escalar para o usuário. Você também pode modificar a entrada da ferramenta antes de executar ou injetar contexto adicional para Claude. Consulte [Controle de decisão PreToolUse](#pretooluse-decision-control) para o conjunto completo de opções.

    ```json theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Database writes are not allowed"
      }
    }
    ```
  </Tab>

  <Tab title="PermissionRequest">
    Usa `hookSpecificOutput` para permitir ou negar uma solicitação de permissão em nome do usuário. Ao permitir, você também pode modificar a entrada da ferramenta ou aplicar regras de permissão para que o usuário não seja solicitado novamente. Consulte [Controle de decisão PermissionRequest](#permissionrequest-decision-control) para o conjunto completo de opções.

    ```json theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PermissionRequest",
        "decision": {
          "behavior": "allow",
          "updatedInput": {
            "command": "npm run lint"
          }
        }
      }
    }
    ```
  </Tab>
</Tabs>

Para exemplos estendidos incluindo validação de comando Bash, filtragem de prompt e scripts de aprovação automática, consulte [O que você pode automatizar](/pt/hooks-guide#what-you-can-automate) no guia e a [implementação de referência do validador de comando Bash](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py).

## Eventos de hook

Cada evento corresponde a um ponto no ciclo de vida do Claude Code onde hooks podem executar. As seções abaixo são ordenadas para corresponder ao ciclo de vida: da configuração de sessão através do loop agentic até o fim da sessão. Cada seção descreve quando o evento dispara, quais matchers suporta, a entrada JSON que recebe e como controlar comportamento através de saída.

### SessionStart

Executa quando Claude Code inicia uma nova sessão ou retoma uma sessão existente. Útil para carregar contexto de desenvolvimento como problemas existentes ou mudanças recentes em seu codebase, ou configurar variáveis de ambiente. Para contexto estático que não requer um script, use [CLAUDE.md](/pt/memory) em vez disso.

SessionStart executa em cada sessão, então mantenha esses hooks rápidos. Apenas hooks `type: "command"` e `type: "mcp_tool"` são suportados.

O valor do matcher corresponde a como a sessão foi iniciada:

| Matcher   | Quando dispara                        |
| :-------- | :------------------------------------ |
| `startup` | Nova sessão                           |
| `resume`  | `--resume`, `--continue` ou `/resume` |
| `clear`   | `/clear`                              |
| `compact` | Compactação automática ou manual      |

#### Entrada de SessionStart

Além dos [campos de entrada comuns](#common-input-fields), hooks SessionStart recebem `source`, `model` e opcionalmente `agent_type`. O campo `source` indica como a sessão começou: `"startup"` para novas sessões, `"resume"` para sessões retomadas, `"clear"` após `/clear` ou `"compact"` após compactação. O campo `model` contém o identificador do modelo. Se você iniciar Claude Code com `claude --agent <name>`, um campo `agent_type` contém o nome do agente.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionStart",
  "source": "startup",
  "model": "claude-sonnet-4-6"
}
```

#### Controle de decisão de SessionStart

Qualquer texto que seu script de hook imprima em stdout é adicionado como contexto para Claude. Além dos [campos de saída JSON](#json-output) disponíveis para todos os hooks, você pode retornar esses campos específicos do evento:

| Campo               | Descrição                                                                                                                                                                                                           |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `additionalContext` | String adicionada ao contexto de Claude no início da conversa, antes do primeiro prompt. Consulte [Adicionar contexto para Claude](#add-context-for-claude) para saber como o texto é entregue e o que colocar nele |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Branch atual: feat/auth-refactor\nMudanças não confirmadas: src/auth.ts, src/login.tsx\nProblema ativo: #4211 Migrar para OAuth2"
  }
}
```

Como stdout simples já chega ao Claude para este evento, um hook que apenas carrega contexto pode imprimir em stdout diretamente sem construir JSON. Use o formulário JSON quando você precisar combinar contexto com outros campos como `suppressOutput`.

#### Persistir variáveis de ambiente

Hooks SessionStart têm acesso à variável de ambiente `CLAUDE_ENV_FILE`, que fornece um caminho de arquivo onde você pode persistir variáveis de ambiente para comandos Bash subsequentes.

Para definir variáveis de ambiente individuais, escreva declarações `export` para `CLAUDE_ENV_FILE`. Use append (`>>`) para preservar variáveis definidas por outros hooks:

```bash theme={null}
#!/bin/bash

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG_LOG=true' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

Para capturar todas as mudanças de ambiente de comandos de configuração, compare as variáveis exportadas antes e depois:

```bash theme={null}
#!/bin/bash

ENV_BEFORE=$(export -p | sort)

# Execute seus comandos de configuração que modificam o ambiente
source ~/.nvm/nvm.sh
nvm use 20

if [ -n "$CLAUDE_ENV_FILE" ]; then
  ENV_AFTER=$(export -p | sort)
  comm -13 <(echo "$ENV_BEFORE") <(echo "$ENV_AFTER") >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

Qualquer variável escrita para este arquivo estará disponível em todos os comandos Bash subsequentes que o Claude Code executa durante a sessão.

<Note>
  `CLAUDE_ENV_FILE` está disponível para SessionStart, [Setup](#setup), [CwdChanged](#cwdchanged) e [FileChanged](#filechanged) hooks. Outros tipos de hook não têm acesso a esta variável.
</Note>

### Setup

Dispara apenas quando você lança Claude Code com `--init-only`, ou com `--init` ou `--maintenance` em modo de impressão (`-p`). Não dispara na inicialização normal. Use-o para instalação de dependência única ou limpeza agendada que você aciona explicitamente de CI ou scripts, separado da inicialização de sessão normal. Para inicialização por sessão, use [SessionStart](#sessionstart) em vez disso.

O valor do matcher corresponde à flag CLI que acionou o hook:

| Matcher       | Quando dispara                             |
| :------------ | :----------------------------------------- |
| `init`        | `claude --init-only` ou `claude -p --init` |
| `maintenance` | `claude -p --maintenance`                  |

`--init-only` executa hooks Setup e hooks SessionStart com o matcher `startup`, depois sai sem iniciar uma conversa. `--init` e `--maintenance` disparam hooks Setup apenas quando combinados com `-p` (modo de impressão); em uma sessão interativa essas duas flags atualmente não disparam hooks Setup.

Porque Setup não dispara em cada lançamento, um plugin que precisa de uma dependência instalada não pode confiar apenas em Setup. O padrão prático é verificar a dependência no primeiro uso e instalar se ausente, por exemplo um hook ou skill que testa `${CLAUDE_PLUGIN_DATA}/node_modules` e executa `npm install` se ausente. Consulte o [diretório de dados persistentes](/pt/plugins-reference#persistent-data-directory) para onde armazenar dependências instaladas.

#### Entrada de Setup

Além dos [campos de entrada comuns](#common-input-fields), hooks Setup recebem um campo `trigger` definido como `"init"` ou `"maintenance"`:

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Setup",
  "trigger": "init"
}
```

#### Controle de decisão de Setup

Hooks Setup não podem bloquear. Na saída de código 2, stderr é mostrado ao usuário; em qualquer outro código de saída não-zero, stderr aparece apenas quando você lança com `--verbose`. Em ambos os casos a execução continua. Para passar informação para o contexto de Claude, retorne `additionalContext` em saída JSON; stdout simples é escrito apenas no log de debug. Além dos [campos de saída JSON](#json-output) disponíveis para todos os hooks, você pode retornar esses campos específicos do evento:

| Campo               | Descrição                                                                               |
| :------------------ | :-------------------------------------------------------------------------------------- |
| `additionalContext` | String adicionada ao contexto de Claude. Os valores de múltiplos hooks são concatenados |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "Setup",
    "additionalContext": "Dependências instaladas: node_modules, .venv"
  }
}
```

Hooks Setup têm acesso a `CLAUDE_ENV_FILE`. Variáveis escritas para esse arquivo persistem em comandos Bash subsequentes para a sessão, assim como em [hooks SessionStart](#persist-environment-variables). Apenas hooks `type: "command"` e `type: "mcp_tool"` são suportados.

### InstructionsLoaded

Dispara quando um arquivo `CLAUDE.md` ou `.claude/rules/*.md` é carregado em contexto. Este evento dispara na inicialização da sessão para arquivos carregados com entusiasmo e novamente mais tarde quando arquivos são carregados preguiçosamente, por exemplo quando Claude acessa um subdiretório que contém um `CLAUDE.md` aninhado ou quando regras condicionais com frontmatter `paths:` correspondem. O hook não suporta bloqueio ou controle de decisão. Executa assincronamente para fins de observabilidade.

O matcher executa contra `load_reason`. Por exemplo, use `"matcher": "session_start"` para disparar apenas para arquivos carregados na inicialização da sessão, ou `"matcher": "path_glob_match|nested_traversal"` para disparar apenas para carregamentos preguiçosos.

#### Entrada de InstructionsLoaded

Além dos [campos de entrada comuns](#common-input-fields), hooks InstructionsLoaded recebem esses campos:

| Campo               | Descrição                                                                                                                                                                                                                           |
| :------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `file_path`         | Caminho absoluto para o arquivo de instrução que foi carregado                                                                                                                                                                      |
| `memory_type`       | Escopo do arquivo: `"User"`, `"Project"`, `"Local"` ou `"Managed"`                                                                                                                                                                  |
| `load_reason`       | Por que o arquivo foi carregado: `"session_start"`, `"nested_traversal"`, `"path_glob_match"`, `"include"` ou `"compact"`. O valor `"compact"` dispara quando arquivos de instrução são re-carregados após um evento de compactação |
| `globs`             | Padrões de glob de caminho do frontmatter `paths:` do arquivo, se houver. Presente apenas para carregamentos `path_glob_match`                                                                                                      |
| `trigger_file_path` | Caminho para o arquivo cujo acesso acionou este carregamento, para carregamentos preguiçosos                                                                                                                                        |
| `parent_file_path`  | Caminho para o arquivo de instrução pai que incluiu este, para carregamentos `include`                                                                                                                                              |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "InstructionsLoaded",
  "file_path": "/Users/my-project/CLAUDE.md",
  "memory_type": "Project",
  "load_reason": "session_start"
}
```

#### Controle de decisão de InstructionsLoaded

Hooks InstructionsLoaded não têm controle de decisão. Eles não podem bloquear ou modificar carregamento de instrução. Use este evento para logging de auditoria, rastreamento de conformidade ou observabilidade.

### UserPromptSubmit

Executa quando o usuário submete um prompt, antes do Claude processá-lo. Isso permite que você adicione contexto adicional baseado no prompt/conversa, valide prompts ou bloqueie certos tipos de prompts.

#### Entrada de UserPromptSubmit

Além dos [campos de entrada comuns](#common-input-fields), hooks UserPromptSubmit recebem o campo `prompt` contendo o texto que o usuário submeteu.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial of a number"
}
```

#### Controle de decisão de UserPromptSubmit

Hooks `UserPromptSubmit` podem controlar se um prompt de usuário é processado e adicionar contexto. Todos os [campos de saída JSON](#json-output) estão disponíveis.

Existem duas formas de adicionar contexto à conversa na saída 0:

* **Stdout de texto simples**: qualquer texto não-JSON escrito em stdout é adicionado como contexto
* **JSON com `additionalContext`**: use o formato JSON abaixo para mais controle. O campo `additionalContext` é adicionado como contexto

Stdout simples é mostrado como saída de hook na transcrição. O campo `additionalContext` é adicionado mais discretamente.

Para bloquear um prompt, retorne um objeto JSON com `decision` definido para `"block"`:

| Campo               | Descrição                                                                                                                                |
| :------------------ | :--------------------------------------------------------------------------------------------------------------------------------------- |
| `decision`          | `"block"` previne o prompt de ser processado e o apaga do contexto. Omita para permitir que o prompt prossiga                            |
| `reason`            | Mostrado ao usuário quando `decision` é `"block"`. Não adicionado ao contexto                                                            |
| `additionalContext` | String adicionada ao contexto de Claude junto com o prompt submetido. Consulte [Adicionar contexto para Claude](#add-context-for-claude) |
| `sessionTitle`      | Define o título da sessão. Use para nomear sessões automaticamente baseado no conteúdo do prompt                                         |

```json theme={null}
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here",
    "sessionTitle": "My session title"
  }
}
```

<Note>
  O formato JSON não é obrigatório para casos simples. Para adicionar contexto, você pode imprimir texto simples em stdout com saída 0. Use JSON quando precisar bloquear prompts ou quiser controle mais estruturado.
</Note>

### UserPromptExpansion

Executa quando um comando de barra invertida digitado pelo usuário se expande em um prompt antes de chegar ao Claude. Use isso para bloquear comandos específicos de invocação direta, injetar contexto para uma skill particular ou registrar quais comandos os usuários invocam. Por exemplo, um hook correspondendo a `deploy` pode bloquear `/deploy` a menos que um arquivo de aprovação esteja presente, ou um hook correspondendo a uma skill de revisão pode anexar a lista de verificação de revisão da equipe como `additionalContext`.

Este evento cobre o caminho que `PreToolUse` não cobre: um hook `PreToolUse` correspondendo à ferramenta `Skill` dispara apenas quando Claude chama a ferramenta, mas digitar `/skillname` diretamente ignora `PreToolUse`. `UserPromptExpansion` dispara nesse caminho direto.

Corresponde em `command_name`. Deixe o matcher vazio para disparar em cada comando de barra invertida do tipo prompt.

#### Entrada de UserPromptExpansion

Além dos [campos de entrada comuns](#common-input-fields), hooks UserPromptExpansion recebem `expansion_type`, `command_name`, `command_args`, `command_source` e a string `prompt` original. O campo `expansion_type` é `slash_command` para skills e comandos personalizados, ou `mcp_prompt` para prompts de servidor MCP.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../00893aaf.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptExpansion",
  "expansion_type": "slash_command",
  "command_name": "example-skill",
  "command_args": "arg1 arg2",
  "command_source": "plugin",
  "prompt": "/example-skill arg1 arg2"
}
```

#### Controle de decisão de UserPromptExpansion

Hooks `UserPromptExpansion` podem bloquear a expansão ou adicionar contexto. Todos os [campos de saída JSON](#json-output) estão disponíveis.

| Campo               | Descrição                                                                                                                                |
| :------------------ | :--------------------------------------------------------------------------------------------------------------------------------------- |
| `decision`          | `"block"` previne o comando de barra invertida de se expandir. Omita para permitir que prossiga                                          |
| `reason`            | Mostrado ao usuário quando `decision` é `"block"`                                                                                        |
| `additionalContext` | String adicionada ao contexto de Claude junto com o prompt expandido. Consulte [Adicionar contexto para Claude](#add-context-for-claude) |

```json theme={null}
{
  "decision": "block",
  "reason": "This slash command is not available",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptExpansion",
    "additionalContext": "Additional context for this expansion"
  }
}
```

### PreToolUse

Executa após Claude criar parâmetros de ferramenta e antes de processar a chamada da ferramenta. Corresponde no nome da ferramenta: `Bash`, `Edit`, `Write`, `Read`, `Glob`, `Grep`, `Agent`, `WebFetch`, `WebSearch`, `AskUserQuestion`, `ExitPlanMode` e qualquer [nome de ferramenta MCP](#match-mcp-tools).

Use [Controle de decisão PreToolUse](#pretooluse-decision-control) para permitir, negar, pedir ou adiar a chamada da ferramenta.

#### Entrada de PreToolUse

Além dos [campos de entrada comuns](#common-input-fields), hooks PreToolUse recebem `tool_name`, `tool_input` e `tool_use_id`. Os campos `tool_input` dependem da ferramenta:

##### Bash

Executa comandos shell.

| Campo               | Tipo    | Exemplo            | Descrição                                |
| :------------------ | :------ | :----------------- | :--------------------------------------- |
| `command`           | string  | `"npm test"`       | O comando shell a executar               |
| `description`       | string  | `"Run test suite"` | Descrição opcional do que o comando faz  |
| `timeout`           | number  | `120000`           | Timeout opcional em milissegundos        |
| `run_in_background` | boolean | `false`            | Se o comando deve executar em background |

##### Write

Cria ou sobrescreve um arquivo.

| Campo       | Tipo   | Exemplo               | Descrição                                  |
| :---------- | :----- | :-------------------- | :----------------------------------------- |
| `file_path` | string | `"/path/to/file.txt"` | Caminho absoluto para o arquivo a escrever |
| `content`   | string | `"file content"`      | Conteúdo a escrever no arquivo             |

##### Edit

Substitui uma string em um arquivo existente.

| Campo         | Tipo    | Exemplo               | Descrição                                |
| :------------ | :------ | :-------------------- | :--------------------------------------- |
| `file_path`   | string  | `"/path/to/file.txt"` | Caminho absoluto para o arquivo a editar |
| `old_string`  | string  | `"original text"`     | Texto a encontrar e substituir           |
| `new_string`  | string  | `"replacement text"`  | Texto de substituição                    |
| `replace_all` | boolean | `false`               | Se deve substituir todas as ocorrências  |

##### Read

Lê conteúdo de arquivo.

| Campo       | Tipo   | Exemplo               | Descrição                                   |
| :---------- | :----- | :-------------------- | :------------------------------------------ |
| `file_path` | string | `"/path/to/file.txt"` | Caminho absoluto para o arquivo a ler       |
| `offset`    | number | `10`                  | Número de linha opcional para começar a ler |
| `limit`     | number | `50`                  | Número opcional de linhas a ler             |

##### Glob

Encontra arquivos correspondendo a um padrão glob.

| Campo     | Tipo   | Exemplo          | Descrição                                                                  |
| :-------- | :----- | :--------------- | :------------------------------------------------------------------------- |
| `pattern` | string | `"**/*.ts"`      | Padrão glob para corresponder arquivos contra                              |
| `path`    | string | `"/path/to/dir"` | Diretório opcional para pesquisar. Padrão para diretório de trabalho atual |

##### Grep

Pesquisa conteúdo de arquivo com expressões regulares.

| Campo         | Tipo    | Exemplo          | Descrição                                                                            |
| :------------ | :------ | :--------------- | :----------------------------------------------------------------------------------- |
| `pattern`     | string  | `"TODO.*fix"`    | Padrão de expressão regular para pesquisar                                           |
| `path`        | string  | `"/path/to/dir"` | Arquivo ou diretório opcional para pesquisar                                         |
| `glob`        | string  | `"*.ts"`         | Padrão glob opcional para filtrar arquivos                                           |
| `output_mode` | string  | `"content"`      | `"content"`, `"files_with_matches"` ou `"count"`. Padrão para `"files_with_matches"` |
| `-i`          | boolean | `true`           | Pesquisa insensível a maiúsculas                                                     |
| `multiline`   | boolean | `false`          | Ativar correspondência multilinha                                                    |

##### WebFetch

Busca e processa conteúdo web.

| Campo    | Tipo   | Exemplo                       | Descrição                             |
| :------- | :----- | :---------------------------- | :------------------------------------ |
| `url`    | string | `"https://example.com/api"`   | URL para buscar conteúdo              |
| `prompt` | string | `"Extract the API endpoints"` | Prompt a executar no conteúdo buscado |

##### WebSearch

Pesquisa a web.

| Campo             | Tipo   | Exemplo                        | Descrição                                           |
| :---------------- | :----- | :----------------------------- | :-------------------------------------------------- |
| `query`           | string | `"react hooks best practices"` | Consulta de pesquisa                                |
| `allowed_domains` | array  | `["docs.example.com"]`         | Opcional: incluir apenas resultados desses domínios |
| `blocked_domains` | array  | `["spam.example.com"]`         | Opcional: excluir resultados desses domínios        |

##### Agent

Gera um [subagente](/pt/sub-agents).

| Campo           | Tipo   | Exemplo                    | Descrição                                           |
| :-------------- | :----- | :------------------------- | :-------------------------------------------------- |
| `prompt`        | string | `"Find all API endpoints"` | A tarefa para o agente executar                     |
| `description`   | string | `"Find API endpoints"`     | Descrição curta da tarefa                           |
| `subagent_type` | string | `"Explore"`                | Tipo de agente especializado a usar                 |
| `model`         | string | `"sonnet"`                 | Alias de modelo opcional para sobrescrever o padrão |

##### AskUserQuestion

Faz ao usuário uma a quatro perguntas de múltipla escolha.

| Campo       | Tipo   | Exemplo                                                                                                            | Descrição                                                                                                                                                                                                            |
| :---------- | :----- | :----------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `questions` | array  | `[{"question": "Which framework?", "header": "Framework", "options": [{"label": "React"}], "multiSelect": false}]` | Perguntas a apresentar, cada uma com uma string `question`, `header` curto, array `options` e flag `multiSelect` opcional                                                                                            |
| `answers`   | object | `{"Which framework?": "React"}`                                                                                    | Opcional. Mapeia texto de pergunta para rótulo de opção selecionada. Respostas multi-select juntam rótulos com vírgulas. Claude não define este campo; forneça-o via `updatedInput` para responder programaticamente |

#### Controle de decisão de PreToolUse

Hooks `PreToolUse` podem controlar se uma chamada de ferramenta prossegue. Diferentemente de outros hooks que usam um campo `decision` de nível superior, PreToolUse retorna sua decisão dentro de um objeto `hookSpecificOutput`. Isso oferece controle mais rico: quatro resultados (permitir, negar, pedir ou adiar) além da capacidade de modificar entrada de ferramenta antes da execução.

| Campo                      | Descrição                                                                                                                                                                                                                                                                                                                             |
| :------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `permissionDecision`       | `"allow"` ignora o prompt de permissão. `"deny"` previne a chamada da ferramenta. `"ask"` solicita ao usuário confirmar. `"defer"` sai graciosamente para que a ferramenta possa ser retomada mais tarde. [Regras de negação e pergunta](/pt/permissions#manage-permissions) ainda se aplicam independentemente do que o hook retorna |
| `permissionDecisionReason` | Para `"allow"` e `"ask"`, mostrado ao usuário mas não ao Claude. Para `"deny"`, mostrado ao Claude. Para `"defer"`, ignorado                                                                                                                                                                                                          |
| `updatedInput`             | Modifica os parâmetros de entrada da ferramenta antes da execução. Substitui o objeto de entrada inteiro, então inclua campos inalterados junto com os modificados. Combine com `"allow"` para aprovação automática ou `"ask"` para mostrar a entrada modificada ao usuário. Para `"defer"`, ignorado                                 |
| `additionalContext`        | String adicionada ao contexto de Claude junto com o resultado da ferramenta. Para `"defer"`, ignorado. Consulte [Adicionar contexto para Claude](#add-context-for-claude)                                                                                                                                                             |

Quando múltiplos hooks PreToolUse retornam decisões diferentes, a precedência é `deny` > `defer` > `ask` > `allow`.

Quando um hook retorna `"ask"`, o diálogo de permissão exibido ao usuário inclui um rótulo identificando de onde o hook veio: por exemplo, `[User]`, `[Project]`, `[Plugin]` ou `[Local]`. Isso ajuda os usuários a entender qual fonte de configuração está solicitando confirmação.

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "My reason here",
    "updatedInput": {
      "field_to_modify": "new value"
    },
    "additionalContext": "Current environment: production. Proceed with caution."
  }
}
```

`AskUserQuestion` e `ExitPlanMode` requerem interação do usuário e normalmente bloqueiam em [modo não-interativo](/pt/headless) com a flag `-p`. Retornar `permissionDecision: "allow"` junto com `updatedInput` satisfaz esse requisito: o hook lê a entrada da ferramenta de stdin, coleta a resposta através de sua própria UI e a retorna em `updatedInput` para que a ferramenta execute sem solicitar. Retornar `"allow"` sozinho não é suficiente para essas ferramentas. Para `AskUserQuestion`, ecoar de volta o array `questions` original e adicionar um objeto [`answers`](#askuserquestion) mapeando o texto de cada pergunta para a resposta escolhida.

<Note>
  PreToolUse anteriormente usava campos `decision` e `reason` de nível superior, mas esses estão deprecados para este evento. Use `hookSpecificOutput.permissionDecision` e `hookSpecificOutput.permissionDecisionReason` em vez disso. Os valores deprecados `"approve"` e `"block"` mapeiam para `"allow"` e `"deny"` respectivamente. Outros eventos como PostToolUse e Stop continuam usando `decision` e `reason` de nível superior como seu formato atual.
</Note>

#### Adiar uma chamada de ferramenta para mais tarde

`"defer"` é para integrações que executam `claude -p` como um subprocesso e leem sua saída JSON, como um aplicativo Agent SDK ou uma UI personalizada construída em cima do Claude Code. Permite que esse processo chamador pause Claude em uma chamada de ferramenta, colete entrada através de sua própria interface e retome onde parou. Claude Code honra este valor apenas em [modo não-interativo](/pt/headless) com a flag `-p`. Em sessões interativas ele registra um aviso e ignora o resultado do hook.

<Note>
  O valor `defer` requer Claude Code v2.1.89 ou posterior. Versões anteriores não o reconhecem e a ferramenta prossegue através do fluxo de permissão normal.
</Note>

A ferramenta `AskUserQuestion` é o caso típico: Claude quer fazer uma pergunta ao usuário, mas não há terminal para responder. A viagem de ida e volta funciona assim:

1. Claude chama `AskUserQuestion`. O hook `PreToolUse` dispara.
2. O hook retorna `permissionDecision: "defer"`. A ferramenta não executa. O processo sai com `stop_reason: "tool_deferred"` e a chamada de ferramenta pendente preservada na transcrição.
3. O processo chamador lê `deferred_tool_use` do resultado SDK, superficializa a pergunta em sua própria UI e espera por uma resposta.
4. O processo chamador executa `claude -p --resume <session-id>`. A mesma chamada de ferramenta dispara `PreToolUse` novamente.
5. O hook retorna `permissionDecision: "allow"` com a resposta em `updatedInput`. A ferramenta executa e Claude continua.

O campo `deferred_tool_use` carrega o `id`, `name` e `input` da ferramenta. O `input` são os parâmetros que Claude gerou para a chamada de ferramenta, capturados antes da execução:

```json theme={null}
{
  "type": "result",
  "subtype": "success",
  "stop_reason": "tool_deferred",
  "session_id": "abc123",
  "deferred_tool_use": {
    "id": "toolu_01abc",
    "name": "AskUserQuestion",
    "input": { "questions": [{ "question": "Which framework?", "header": "Framework", "options": [{"label": "React"}, {"label": "Vue"}], "multiSelect": false }] }
  }
}
```

Não há timeout ou limite de tentativas. A sessão permanece no disco até que você a retome, sujeita à varredura de retenção [`cleanupPeriodDays`](/pt/settings#available-settings) que deleta arquivos de sessão após 30 dias por padrão. Se a resposta não estiver pronta quando você retomar, o hook pode retornar `"defer"` novamente e o processo sai da mesma forma. O processo chamador controla quando quebrar o loop eventualmente retornando `"allow"` ou `"deny"` do hook.

`"defer"` apenas funciona quando Claude faz uma única chamada de ferramenta no turno. Se Claude faz várias chamadas de ferramenta de uma vez, `"defer"` é ignorado com um aviso e a ferramenta prossegue através do fluxo de permissão normal. A restrição existe porque resume pode apenas re-executar uma ferramenta: não há forma de adiar uma chamada de um lote sem deixar as outras não resolvidas.

Se a ferramenta adiada não estiver mais disponível quando você retomar, o processo sai com `stop_reason: "tool_deferred_unavailable"` e `is_error: true` antes do hook disparar. Isso acontece quando um servidor MCP que forneceu a ferramenta não está conectado para a sessão retomada. O payload `deferred_tool_use` ainda é incluído para que você possa identificar qual ferramenta desapareceu.

<Warning>
  `--resume` não restaura o modo de permissão da sessão anterior. Passe a mesma flag `--permission-mode` na retomada que estava ativa quando a ferramenta foi adiada. Claude Code registra um aviso se os modos diferem.
</Warning>

### PermissionRequest

Executa quando o usuário é mostrado um diálogo de permissão.
Use [Controle de decisão PermissionRequest](#permissionrequest-decision-control) para permitir ou negar em nome do usuário.

Corresponde no nome da ferramenta, mesmos valores que PreToolUse.

#### Entrada de PermissionRequest

Hooks PermissionRequest recebem campos `tool_name` e `tool_input` como hooks PreToolUse, mas sem `tool_use_id`. Um array `permission_suggestions` opcional contém as opções "sempre permitir" que o usuário normalmente veria no diálogo de permissão. A diferença é quando o hook dispara: hooks PermissionRequest executam quando um diálogo de permissão está prestes a ser mostrado ao usuário, enquanto hooks PreToolUse executam antes da execução da ferramenta independentemente do status de permissão.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PermissionRequest",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf node_modules",
    "description": "Remove node_modules directory"
  },
  "permission_suggestions": [
    {
      "type": "addRules",
      "rules": [{ "toolName": "Bash", "ruleContent": "rm -rf node_modules" }],
      "behavior": "allow",
      "destination": "localSettings"
    }
  ]
}
```

#### Controle de decisão de PermissionRequest

Hooks `PermissionRequest` podem permitir ou negar solicitações de permissão. Além dos [campos de saída JSON](#json-output) disponíveis para todos os hooks, seu script de hook pode retornar um objeto `decision` com esses campos específicos do evento:

| Campo                | Descrição                                                                                                                                                                                                                                                         |
| :------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `behavior`           | `"allow"` concede a permissão, `"deny"` nega. [Regras de negação e pergunta](/pt/permissions#manage-permissions) ainda são avaliadas, então um hook retornando `"allow"` não sobrescreve uma regra de negação correspondente                                      |
| `updatedInput`       | Apenas para `"allow"`: modifica os parâmetros de entrada da ferramenta antes da execução. Substitui o objeto de entrada inteiro, então inclua campos inalterados junto com os modificados. A entrada modificada é re-avaliada contra regras de negação e pergunta |
| `updatedPermissions` | Apenas para `"allow"`: array de [entradas de atualização de permissão](#permission-update-entries) a aplicar, como adicionar uma regra de permissão ou mudar o modo de permissão da sessão                                                                        |
| `message`            | Apenas para `"deny"`: diz ao Claude por que a permissão foi negada                                                                                                                                                                                                |
| `interrupt`          | Apenas para `"deny"`: se `true`, para Claude                                                                                                                                                                                                                      |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": {
        "command": "npm run lint"
      }
    }
  }
}
```

#### Entradas de atualização de permissão

O campo de saída `updatedPermissions` e o campo de entrada [`permission_suggestions`](#permissionrequest-input) ambos usam o mesmo array de objetos de entrada. Cada entrada tem um `type` que determina seus outros campos e um `destination` que controla onde a mudança é escrita.

| `type`              | Campos                             | Efeito                                                                                                                                                                                         |
| :------------------ | :--------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `addRules`          | `rules`, `behavior`, `destination` | Adiciona regras de permissão. `rules` é um array de objetos `{toolName, ruleContent?}`. Omita `ruleContent` para corresponder a toda a ferramenta. `behavior` é `"allow"`, `"deny"` ou `"ask"` |
| `replaceRules`      | `rules`, `behavior`, `destination` | Substitui todas as regras do `behavior` dado no `destination` pelas `rules` fornecidas                                                                                                         |
| `removeRules`       | `rules`, `behavior`, `destination` | Remove regras correspondentes do `behavior` dado                                                                                                                                               |
| `setMode`           | `mode`, `destination`              | Muda o modo de permissão. Modos válidos são `default`, `acceptEdits`, `dontAsk`, `bypassPermissions` e `plan`                                                                                  |
| `addDirectories`    | `directories`, `destination`       | Adiciona diretórios de trabalho. `directories` é um array de strings de caminho                                                                                                                |
| `removeDirectories` | `directories`, `destination`       | Remove diretórios de trabalho                                                                                                                                                                  |

<Note>
  `setMode` com `bypassPermissions` apenas toma efeito se a sessão foi lançada com modo bypass já disponível: `--dangerously-skip-permissions`, `--permission-mode bypassPermissions`, `--allow-dangerously-skip-permissions` ou `permissions.defaultMode: "bypassPermissions"` em configurações, e o modo não é desabilitado por [`permissions.disableBypassPermissionsMode`](/pt/permissions#managed-settings). Caso contrário, a atualização é um no-op. `bypassPermissions` nunca é persistido como `defaultMode` independentemente de `destination`.
</Note>

O campo `destination` em cada entrada determina se a mudança fica em memória ou persiste em um arquivo de configurações.

| `destination`     | Escreve para                                          |
| :---------------- | :---------------------------------------------------- |
| `session`         | apenas em memória, descartado quando a sessão termina |
| `localSettings`   | `.claude/settings.local.json`                         |
| `projectSettings` | `.claude/settings.json`                               |
| `userSettings`    | `~/.claude/settings.json`                             |

Um hook pode ecoar uma das `permission_suggestions` que recebeu como sua própria saída `updatedPermissions`, que é equivalente ao usuário selecionar essa opção "sempre permitir" no diálogo.

### PostToolUse

Executa imediatamente após uma ferramenta completar com sucesso.

Corresponde no nome da ferramenta, mesmos valores que PreToolUse.

#### Entrada de PostToolUse

Hooks `PostToolUse` disparam após uma ferramenta já ter executado com sucesso. A entrada inclui tanto `tool_input`, os argumentos enviados para a ferramenta, quanto `tool_response`, o resultado que retornou. O esquema exato para ambos depende da ferramenta.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  },
  "tool_use_id": "toolu_01ABC123...",
  "duration_ms": 12
}
```

| Campo         | Descrição                                                                                                                 |
| :------------ | :------------------------------------------------------------------------------------------------------------------------ |
| `duration_ms` | Opcional. Tempo de execução da ferramenta em milissegundos. Exclui tempo gasto em prompts de permissão e hooks PreToolUse |

#### Controle de decisão de PostToolUse

Hooks `PostToolUse` podem fornecer feedback ao Claude após execução de ferramenta. Além dos [campos de saída JSON](#json-output) disponíveis para todos os hooks, seu script de hook pode retornar esses campos específicos do evento:

| Campo                  | Descrição                                                                                                                                       |
| :--------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| `decision`             | `"block"` adiciona a `reason` próxima ao resultado da ferramenta. Claude ainda vê a saída original; para substituí-la, use `updatedToolOutput`  |
| `reason`               | Explicação mostrada ao Claude quando `decision` é `"block"`                                                                                     |
| `additionalContext`    | String adicionada ao contexto de Claude junto com o resultado da ferramenta. Consulte [Adicionar contexto para Claude](#add-context-for-claude) |
| `updatedToolOutput`    | Substitui a saída da ferramenta pelo valor fornecido antes de ser enviado ao Claude. O valor deve corresponder à forma de saída da ferramenta   |
| `updatedMCPToolOutput` | Substitui a saída apenas para [ferramentas MCP](#match-mcp-tools). Prefira `updatedToolOutput`, que funciona para todas as ferramentas          |

O exemplo abaixo substitui a saída de uma chamada `Bash`. O valor de substituição corresponde à forma de saída da ferramenta `Bash`:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude",
    "updatedToolOutput": {
      "stdout": "[redacted]",
      "stderr": "",
      "interrupted": false,
      "isImage": false
    }
  }
}
```

<Warning>
  `updatedToolOutput` apenas muda o que Claude vê. A ferramenta já executou no momento em que o hook dispara, então qualquer arquivo escrito, comandos executados ou requisições de rede enviadas já tiveram efeito. Telemetria como spans de ferramentas OpenTelemetry e eventos de análise também capturam a saída original antes do hook executar. Para prevenir ou modificar uma chamada de ferramenta antes de executar, use um hook [PreToolUse](#pretooluse) em vez disso.

  O valor de substituição deve corresponder à forma de saída da ferramenta. Ferramentas integradas retornam objetos estruturados em vez de strings simples. Por exemplo, `Bash` retorna um objeto com campos `stdout`, `stderr`, `interrupted` e `isImage`. Para ferramentas integradas, um valor que não corresponde ao esquema de saída da ferramenta é ignorado e a saída original é usada. A saída de ferramenta MCP é passada sem validação de esquema. Remover detalhes de erro que Claude precisa pode fazer com que ele prossiga em uma suposição falsa.
</Warning>

### PostToolUseFailure

Executa quando uma execução de ferramenta falha. Este evento dispara para chamadas de ferramenta que lançam erros ou retornam resultados de falha. Use isso para registrar falhas, enviar alertas ou fornecer feedback corretivo ao Claude.

Corresponde no nome da ferramenta, mesmos valores que PreToolUse.

#### Entrada de PostToolUseFailure

Hooks PostToolUseFailure recebem os mesmos campos `tool_name` e `tool_input` que PostToolUse, junto com informações de erro como campos de nível superior:

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUseFailure",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run test suite"
  },
  "tool_use_id": "toolu_01ABC123...",
  "error": "Command exited with non-zero status code 1",
  "is_interrupt": false,
  "duration_ms": 4187
}
```

| Campo          | Descrição                                                                                                                 |
| :------------- | :------------------------------------------------------------------------------------------------------------------------ |
| `error`        | String descrevendo o que deu errado                                                                                       |
| `is_interrupt` | Boolean opcional indicando se a falha foi causada por interrupção do usuário                                              |
| `duration_ms`  | Opcional. Tempo de execução da ferramenta em milissegundos. Exclui tempo gasto em prompts de permissão e hooks PreToolUse |

#### Controle de decisão de PostToolUseFailure

Hooks `PostToolUseFailure` podem fornecer contexto ao Claude após falha de ferramenta. Além dos [campos de saída JSON](#json-output) disponíveis para todos os hooks, seu script de hook pode retornar esses campos específicos do evento:

| Campo               | Descrição                                                                                                                    |
| :------------------ | :--------------------------------------------------------------------------------------------------------------------------- |
| `additionalContext` | String adicionada ao contexto de Claude junto com o erro. Consulte [Adicionar contexto para Claude](#add-context-for-claude) |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUseFailure",
    "additionalContext": "Additional information about the failure for Claude"
  }
}
```

### PostToolBatch

Executa uma vez após cada chamada de ferramenta em um lote ter sido resolvida, antes do Claude Code enviar a próxima solicitação para o modelo. `PostToolUse` dispara uma vez por ferramenta, o que significa que dispara concorrentemente quando Claude faz chamadas de ferramenta paralelas. `PostToolBatch` dispara exatamente uma vez com o lote completo, então é o lugar certo para injetar contexto que depende do conjunto de ferramentas que executaram em vez de em qualquer ferramenta única. Não há matcher para este evento.

#### Entrada de PostToolBatch

Além dos [campos de entrada comuns](#common-input-fields), hooks PostToolBatch recebem `tool_calls`, um array descrevendo cada chamada de ferramenta no lote:

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolBatch",
  "tool_calls": [
    {
      "tool_name": "Read",
      "tool_input": {"file_path": "/.../ledger/accounts.py"},
      "tool_use_id": "toolu_01...",
      "tool_response": "     1\tfrom __future__ import annotations\n     2\t..."
    },
    {
      "tool_name": "Read",
      "tool_input": {"file_path": "/.../ledger/transactions.py"},
      "tool_use_id": "toolu_02...",
      "tool_response": "     1\tfrom __future__ import annotations\n     2\t..."
    }
  ]
}
```

`tool_response` contém o mesmo conteúdo que o modelo recebe no bloco `tool_result` correspondente. O valor é uma string serializada ou array de bloco de conteúdo, exatamente como a ferramenta o emitiu. Para `Read`, isso significa texto com prefixo de número de linha em vez de conteúdo de arquivo bruto. Respostas podem ser grandes, então analise apenas os campos que você precisa.

<Note>
  A forma `tool_response` difere da de `PostToolUse`. `PostToolUse` passa o objeto `Output` estruturado da ferramenta, como `{filePath: "...", success: true}` para `Write`; `PostToolBatch` passa o conteúdo `tool_result` serializado que o modelo vê.
</Note>

#### Controle de decisão de PostToolBatch

Hooks `PostToolBatch` podem injetar contexto para Claude. Além dos [campos de saída JSON](#json-output) disponíveis para todos os hooks, seu script de hook pode retornar esses campos específicos do evento:

| Campo               | Descrição                                                                                                                                                                                                                                   |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `additionalContext` | String de contexto injetada uma vez antes da próxima chamada do modelo. Consulte [Adicionar contexto para Claude](#add-context-for-claude) para detalhes de entrega, o que colocar nele e como sessões retomadas lidam com valores passados |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolBatch",
    "additionalContext": "These files are part of the ledger module. Run pytest before marking the task complete."
  }
}
```

Retornar `decision: "block"` ou `continue: false` para o loop agentic antes da próxima chamada do modelo.

### PermissionDenied

Executa quando o classificador de [modo automático](/pt/permission-modes#eliminate-prompts-with-auto-mode) nega uma chamada de ferramenta. Este hook apenas dispara em modo automático: não executa quando você nega manualmente um diálogo de permissão, quando um hook `PreToolUse` bloqueia uma chamada ou quando uma regra `deny` corresponde. Use-o para registrar negações de classificador, ajustar configuração ou dizer ao modelo que pode tentar novamente a chamada de ferramenta.

Corresponde no nome da ferramenta, mesmos valores que PreToolUse.

#### Entrada de PermissionDenied

Além dos [campos de entrada comuns](#common-input-fields), hooks PermissionDenied recebem `tool_name`, `tool_input`, `tool_use_id` e `reason`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "auto",
  "hook_event_name": "PermissionDenied",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /tmp/build",
    "description": "Clean build directory"
  },
  "tool_use_id": "toolu_01ABC123...",
  "reason": "Auto mode denied: command targets a path outside the project"
}
```

| Campo    | Descrição                                                                     |
| :------- | :---------------------------------------------------------------------------- |
| `reason` | A explicação do classificador para por que a chamada de ferramenta foi negada |

#### Controle de decisão de PermissionDenied

Hooks PermissionDenied podem dizer ao modelo que pode tentar novamente a chamada de ferramenta negada. Retorne um objeto JSON com `hookSpecificOutput.retry` definido para `true`:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionDenied",
    "retry": true
  }
}
```

Quando `retry` é `true`, Claude Code adiciona uma mensagem à conversa dizendo ao modelo que pode tentar novamente a chamada de ferramenta. A negação em si não é revertida. Se seu hook não retorna JSON ou retorna `retry: false`, a negação permanece e o modelo recebe a mensagem de rejeição original.

### Notification

Executa quando Claude Code envia notificações. Corresponde no tipo de notificação: `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`, `elicitation_complete`, `elicitation_response`. Omita o matcher para executar hooks para todos os tipos de notificação.

Use matchers separados para executar diferentes manipuladores dependendo do tipo de notificação. Esta configuração aciona um script de alerta específico de permissão quando Claude precisa de aprovação de permissão e uma notificação diferente quando Claude está ocioso:

```json theme={null}
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/permission-alert.sh"
          }
        ]
      },
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/idle-notification.sh"
          }
        ]
      }
    ]
  }
}
```

#### Entrada de Notification

Além dos [campos de entrada comuns](#common-input-fields), hooks Notification recebem `message` com o texto de notificação, um `title` opcional e `notification_type` indicando qual tipo disparou.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Notification",
  "message": "Claude needs your permission to use Bash",
  "title": "Permission needed",
  "notification_type": "permission_prompt"
}
```

Hooks Notification não podem bloquear ou modificar notificações. Eles são destinados a efeitos colaterais como encaminhar a notificação para um serviço externo. Os [campos de saída JSON](#json-output) comuns como `systemMessage` se aplicam.

### SubagentStart

Executa quando um subagente do Claude Code é gerado via ferramenta Agent. Suporta matchers para filtrar por nome de tipo de agente (agentes integrados como `general-purpose`, `Explore`, `Plan` ou nomes de agentes personalizados de `.claude/agents/`).

#### Entrada de SubagentStart

Além dos [campos de entrada comuns](#common-input-fields), hooks SubagentStart recebem `agent_id` com o identificador único para o subagente e `agent_type` com o nome do agente (agentes integrados como `"general-purpose"`, `"Explore"`, `"Plan"` ou nomes de agentes personalizados).

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SubagentStart",
  "agent_id": "agent-abc123",
  "agent_type": "Explore"
}
```

Hooks SubagentStart não podem bloquear criação de subagente, mas podem injetar contexto no subagente. Além dos [campos de saída JSON](#json-output) disponíveis para todos os hooks, você pode retornar:

| Campo               | Descrição                                                                                                                                                              |
| :------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `additionalContext` | String adicionada ao contexto do subagente no início de sua conversa, antes de seu primeiro prompt. Consulte [Adicionar contexto para Claude](#add-context-for-claude) |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "Follow security guidelines for this task"
  }
}
```

### SubagentStop

Executa quando um subagente do Claude Code terminou de responder. Corresponde no tipo de agente, mesmos valores que SubagentStart.

#### Entrada de SubagentStop

Além dos [campos de entrada comuns](#common-input-fields), hooks SubagentStop recebem `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path` e `last_assistant_message`. O campo `agent_type` é o valor usado para filtragem de matcher. O `transcript_path` é a transcrição da sessão principal, enquanto `agent_transcript_path` é a própria transcrição do subagente armazenada em uma pasta `subagents/` aninhada. O campo `last_assistant_message` contém o conteúdo de texto da resposta final do subagente, então hooks podem acessá-lo sem analisar o arquivo de transcrição.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../abc123.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SubagentStop",
  "stop_hook_active": false,
  "agent_id": "def456",
  "agent_type": "Explore",
  "agent_transcript_path": "~/.claude/projects/.../abc123/subagents/agent-def456.jsonl",
  "last_assistant_message": "Analysis complete. Found 3 potential issues..."
}
```

Hooks SubagentStop usam o mesmo formato de controle de decisão que [hooks Stop](#stop-decision-control).

### TaskCreated

Executa quando uma tarefa está sendo criada via ferramenta `TaskCreate`. Use isso para impor convenções de nomenclatura, exigir descrições de tarefa ou prevenir que certas tarefas sejam criadas.

Quando um hook `TaskCreated` sai com código 2, a tarefa não é criada e a mensagem de stderr é alimentada de volta ao modelo como feedback. Para parar o colega inteiramente em vez de re-executá-lo, retorne JSON com `{"continue": false, "stopReason": "..."}`. Hooks TaskCreated não suportam matchers e disparam em cada ocorrência.

#### Entrada de TaskCreated

Além dos [campos de entrada comuns](#common-input-fields), hooks TaskCreated recebem `task_id`, `task_subject` e opcionalmente `task_description`, `teammate_name` e `team_name`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TaskCreated",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "my-project"
}
```

| Campo              | Descrição                                           |
| :----------------- | :-------------------------------------------------- |
| `task_id`          | Identificador da tarefa sendo criada                |
| `task_subject`     | Título da tarefa                                    |
| `task_description` | Descrição detalhada da tarefa. Pode estar ausente   |
| `teammate_name`    | Nome do colega criando a tarefa. Pode estar ausente |
| `team_name`        | Nome da equipe. Pode estar ausente                  |

#### Controle de decisão de TaskCreated

Hooks TaskCreated suportam duas formas de controlar criação de tarefa:

* **Código de saída 2**: a tarefa não é criada e a mensagem de stderr é alimentada de volta ao modelo como feedback.
* **JSON `{"continue": false, "stopReason": "..."}`**: para o colega inteiramente, correspondendo ao comportamento do hook `Stop`. O `stopReason` é mostrado ao usuário.

Este exemplo bloqueia tarefas cujos assuntos não seguem o formato obrigatório:

```bash theme={null}
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

if [[ ! "$TASK_SUBJECT" =~ ^\[TICKET-[0-9]+\] ]]; then
  echo "Task subject must start with a ticket number, e.g. '[TICKET-123] Add feature'" >&2
  exit 2
fi

exit 0
```

### TaskCompleted

Executa quando uma tarefa está sendo marcada como concluída. Isso dispara em duas situações: quando qualquer agente marca explicitamente uma tarefa como concluída através da ferramenta TaskUpdate, ou quando um colega de [equipe de agente](/pt/agent-teams) termina seu turno com tarefas em progresso. Use isso para impor critérios de conclusão como testes aprovados ou verificações de lint antes de uma tarefa fechar.

Quando um hook `TaskCompleted` sai com código 2, a tarefa não é marcada como concluída e a mensagem de stderr é alimentada de volta ao modelo como feedback. Para parar o colega inteiramente em vez de re-executá-lo, retorne JSON com `{"continue": false, "stopReason": "..."}`. Hooks TaskCompleted não suportam matchers e disparam em cada ocorrência.

#### Entrada de TaskCompleted

Além dos [campos de entrada comuns](#common-input-fields), hooks TaskCompleted recebem `task_id`, `task_subject` e opcionalmente `task_description`, `teammate_name` e `team_name`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TaskCompleted",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "my-project"
}
```

| Campo              | Descrição                                               |
| :----------------- | :------------------------------------------------------ |
| `task_id`          | Identificador da tarefa sendo concluída                 |
| `task_subject`     | Título da tarefa                                        |
| `task_description` | Descrição detalhada da tarefa. Pode estar ausente       |
| `teammate_name`    | Nome do colega completando a tarefa. Pode estar ausente |
| `team_name`        | Nome da equipe. Pode estar ausente                      |

#### Controle de decisão de TaskCompleted

Hooks TaskCompleted suportam duas formas de controlar conclusão de tarefa:

* **Código de saída 2**: a tarefa não é marcada como concluída e a mensagem de stderr é alimentada de volta ao modelo como feedback.
* **JSON `{"continue": false, "stopReason": "..."}`**: para o colega inteiramente, correspondendo ao comportamento do hook `Stop`. O `stopReason` é mostrado ao usuário.

Este exemplo executa testes e bloqueia conclusão de tarefa se falharem:

```bash theme={null}
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

# Execute a suite de testes
if ! npm test 2>&1; then
  echo "Tests not passing. Fix failing tests before completing: $TASK_SUBJECT" >&2
  exit 2
fi

exit 0
```

### Stop

Executa quando o agente Claude Code principal terminou de responder. Não executa se a parada ocorreu devido a uma interrupção do usuário. Erros de API disparam [StopFailure](#stopfailure) em vez disso.

#### Entrada de Stop

Além dos [campos de entrada comuns](#common-input-fields), hooks Stop recebem `stop_hook_active` e `last_assistant_message`. O campo `stop_hook_active` é `true` quando Claude Code já está continuando como resultado de um hook stop. Verifique este valor ou processe a transcrição para prevenir que Claude Code execute indefinidamente. O campo `last_assistant_message` contém o conteúdo de texto da resposta final de Claude, então hooks podem acessá-lo sem analisar o arquivo de transcrição.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": true,
  "last_assistant_message": "I've completed the refactoring. Here's a summary..."
}
```

#### Controle de decisão de Stop

Hooks `Stop` e `SubagentStop` podem controlar se Claude continua. Além dos [campos de saída JSON](#json-output) disponíveis para todos os hooks, seu script de hook pode retornar esses campos específicos do evento:

| Campo      | Descrição                                                                       |
| :--------- | :------------------------------------------------------------------------------ |
| `decision` | `"block"` previne Claude de parar. Omita para permitir que Claude pare          |
| `reason`   | Obrigatório quando `decision` é `"block"`. Diz ao Claude por que deve continuar |

```json theme={null}
{
  "decision": "block",
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

### StopFailure

Executa em vez de [Stop](#stop) quando o turno termina devido a um erro de API. Saída e código de saída são ignorados. Use isso para registrar falhas, enviar alertas ou tomar ações de recuperação quando Claude não consegue completar uma resposta devido a limites de taxa, problemas de autenticação ou outros erros de API.

#### Entrada de StopFailure

Além dos [campos de entrada comuns](#common-input-fields), hooks StopFailure recebem `error`, `error_details` opcional e `last_assistant_message` opcional. O campo `error` identifica o tipo de erro e é usado para filtragem de matcher.

| Campo                    | Descrição                                                                                                                                                                                                                                             |
| :----------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `error`                  | Tipo de erro: `rate_limit`, `authentication_failed`, `oauth_org_not_allowed`, `billing_error`, `invalid_request`, `server_error`, `max_output_tokens` ou `unknown`                                                                                    |
| `error_details`          | Detalhes adicionais sobre o erro, quando disponível                                                                                                                                                                                                   |
| `last_assistant_message` | O texto de erro renderizado mostrado na conversa. Diferentemente de `Stop` e `SubagentStop`, onde este campo contém a saída conversacional de Claude, para `StopFailure` contém a string de erro da API em si, como `"API Error: Rate limit reached"` |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "StopFailure",
  "error": "rate_limit",
  "error_details": "429 Too Many Requests",
  "last_assistant_message": "API Error: Rate limit reached"
}
```

Hooks StopFailure não têm controle de decisão. Eles executam apenas para fins de notificação e logging.

### TeammateIdle

Executa quando um colega de [equipe de agente](/pt/agent-teams) está prestes a ficar ocioso após terminar seu turno. Use isso para impor portões de qualidade antes de um colega parar de trabalhar, como exigir verificações de lint aprovadas ou verificar que arquivos de saída existem.

Quando um hook `TeammateIdle` sai com código 2, o colega recebe a mensagem de stderr como feedback e continua trabalhando em vez de ficar ocioso. Para parar o colega inteiramente em vez de re-executá-lo, retorne JSON com `{"continue": false, "stopReason": "..."}`. Hooks TeammateIdle não suportam matchers e disparam em cada ocorrência.

#### Entrada de TeammateIdle

Além dos [campos de entrada comuns](#common-input-fields), hooks TeammateIdle recebem `teammate_name` e `team_name`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TeammateIdle",
  "teammate_name": "researcher",
  "team_name": "my-project"
}
```

| Campo           | Descrição                                      |
| :-------------- | :--------------------------------------------- |
| `teammate_name` | Nome do colega que está prestes a ficar ocioso |
| `team_name`     | Nome da equipe                                 |

#### Controle de decisão de TeammateIdle

Hooks TeammateIdle suportam duas formas de controlar comportamento de colega:

* **Código de saída 2**: o colega recebe a mensagem de stderr como feedback e continua trabalhando em vez de ficar ocioso.
* **JSON `{"continue": false, "stopReason": "..."}`**: para o colega inteiramente, correspondendo ao comportamento do hook `Stop`. O `stopReason` é mostrado ao usuário.

Este exemplo verifica que um artefato de build existe antes de permitir que um colega fique ocioso:

```bash theme={null}
#!/bin/bash

if [ ! -f "./dist/output.js" ]; then
  echo "Build artifact missing. Run the build before stopping." >&2
  exit 2
fi

exit 0
```

### ConfigChange

Executa quando um arquivo de configuração muda durante uma sessão. Use isso para auditar mudanças de configurações, impor políticas de segurança ou bloquear modificações não autorizadas a arquivos de configuração.

Hooks ConfigChange disparam para mudanças em arquivos de configurações, configurações de política gerenciada e arquivos de skill. O campo `source` na entrada diz qual tipo de configuração mudou, e o campo `file_path` opcional fornece o caminho para o arquivo mudado.

O matcher filtra na fonte de configuração:

| Matcher            | Quando dispara                                |
| :----------------- | :-------------------------------------------- |
| `user_settings`    | `~/.claude/settings.json` muda                |
| `project_settings` | `.claude/settings.json` muda                  |
| `local_settings`   | `.claude/settings.local.json` muda            |
| `policy_settings`  | Configurações de política gerenciada mudam    |
| `skills`           | Um arquivo de skill em `.claude/skills/` muda |

Este exemplo registra todas as mudanças de configuração para auditoria de segurança:

```json theme={null}
{
  "hooks": {
    "ConfigChange": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/audit-config-change.sh"
          }
        ]
      }
    ]
  }
}
```

#### Entrada de ConfigChange

Além dos [campos de entrada comuns](#common-input-fields), hooks ConfigChange recebem `source` e opcionalmente `file_path`. O campo `source` indica qual tipo de configuração mudou, e `file_path` fornece o caminho para o arquivo específico que foi modificado.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "ConfigChange",
  "source": "project_settings",
  "file_path": "/Users/.../my-project/.claude/settings.json"
}
```

#### Controle de decisão de ConfigChange

Hooks ConfigChange podem bloquear mudanças de configuração de entrar em efeito. Use código de saída 2 ou um JSON `decision` para prevenir a mudança. Quando bloqueado, as novas configurações não são aplicadas à sessão em execução.

| Campo      | Descrição                                                                                  |
| :--------- | :----------------------------------------------------------------------------------------- |
| `decision` | `"block"` previne a mudança de configuração de ser aplicada. Omita para permitir a mudança |
| `reason`   | Explicação mostrada ao usuário quando `decision` é `"block"`                               |

```json theme={null}
{
  "decision": "block",
  "reason": "Configuration changes to project settings require admin approval"
}
```

Mudanças `policy_settings` não podem ser bloqueadas. Hooks ainda disparam para fontes `policy_settings`, então você pode usá-los para logging de auditoria, mas qualquer decisão de bloqueio é ignorada. Isso garante que configurações gerenciadas por empresa sempre entrem em efeito.

### CwdChanged

Executa quando o diretório de trabalho muda durante uma sessão, por exemplo quando Claude executa um comando `cd`. Use isso para reagir a mudanças de diretório: recarregar variáveis de ambiente, ativar toolchains específicas do projeto ou executar scripts de configuração automaticamente. Emparelha com [FileChanged](#filechanged) para ferramentas como [direnv](https://direnv.net/) que gerenciam ambiente por diretório.

Hooks CwdChanged têm acesso a `CLAUDE_ENV_FILE`. Variáveis escritas para esse arquivo persistem em comandos Bash subsequentes para a sessão, assim como em [hooks SessionStart](#persist-environment-variables).

CwdChanged não suporta matchers e dispara em cada mudança de diretório.

#### Entrada de CwdChanged

Além dos [campos de entrada comuns](#common-input-fields), hooks CwdChanged recebem `old_cwd` e `new_cwd`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project/src",
  "hook_event_name": "CwdChanged",
  "old_cwd": "/Users/my-project",
  "new_cwd": "/Users/my-project/src"
}
```

#### Saída de CwdChanged

Além dos [campos de saída JSON](#json-output) disponíveis para todos os hooks, hooks CwdChanged podem retornar `watchPaths` para definir dinamicamente quais caminhos de arquivo [FileChanged](#filechanged) monitora:

| Campo        | Descrição                                                                                                                                                                                                                                   |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `watchPaths` | Array de caminhos absolutos. Substitui a lista de monitoramento dinâmica atual (caminhos de sua configuração `matcher` são sempre monitorados). Retornar um array vazio limpa a lista dinâmica, que é típico ao entrar em um novo diretório |

Hooks CwdChanged não têm controle de decisão. Eles não podem bloquear a mudança de diretório.

### FileChanged

Executa quando um arquivo monitorado muda no disco. Útil para recarregar variáveis de ambiente quando arquivos de configuração do projeto são modificados.

O `matcher` para este evento serve dois papéis:

* **Construir a lista de monitoramento**: o valor é dividido em `|` e cada segmento é registrado como um nome de arquivo literal no diretório de trabalho, então `".envrc|.env"` monitora exatamente esses dois arquivos. Padrões regex não são úteis aqui: um valor como `^\.env` monitoraria um arquivo literalmente nomeado `^\.env`.
* **Filtrar quais hooks executam**: quando um arquivo monitorado muda, o mesmo valor filtra quais grupos de hook executam usando as [regras de matcher](#matcher-patterns) padrão contra o basename do arquivo alterado.

Hooks FileChanged têm acesso a `CLAUDE_ENV_FILE`. Variáveis escritas para esse arquivo persistem em comandos Bash subsequentes para a sessão, assim como em [hooks SessionStart](#persist-environment-variables).

#### Entrada de FileChanged

Além dos [campos de entrada comuns](#common-input-fields), hooks FileChanged recebem `file_path` e `event`.

| Campo       | Descrição                                                                                                   |
| :---------- | :---------------------------------------------------------------------------------------------------------- |
| `file_path` | Caminho absoluto para o arquivo que mudou                                                                   |
| `event`     | O que aconteceu: `"change"` (arquivo modificado), `"add"` (arquivo criado) ou `"unlink"` (arquivo deletado) |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "FileChanged",
  "file_path": "/Users/my-project/.envrc",
  "event": "change"
}
```

#### Saída de FileChanged

Além dos [campos de saída JSON](#json-output) disponíveis para todos os hooks, hooks FileChanged podem retornar `watchPaths` para atualizar dinamicamente quais caminhos de arquivo são monitorados:

| Campo        | Descrição                                                                                                                                                                                                                                                  |
| :----------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `watchPaths` | Array de caminhos absolutos. Substitui a lista de monitoramento dinâmica atual (caminhos de sua configuração `matcher` são sempre monitorados). Use isso quando seu script de hook descobre arquivos adicionais para monitorar baseado no arquivo alterado |

Hooks FileChanged não têm controle de decisão. Eles não podem bloquear a mudança de arquivo de ocorrer.

### WorktreeCreate

Quando você executa `claude --worktree` ou um [subagente usa `isolation: "worktree"`](/pt/sub-agents#choose-the-subagent-scope), Claude Code cria uma cópia de trabalho isolada usando `git worktree`. Se você configurar um hook WorktreeCreate, ele substitui o comportamento git padrão, permitindo que você use um sistema de controle de versão diferente como SVN, Perforce ou Mercurial.

Porque o hook substitui o comportamento padrão inteiramente, [`.worktreeinclude`](/pt/worktrees#copy-gitignored-files-into-worktrees) não é processado. Se você precisar copiar arquivos de configuração local como `.env` para o novo worktree, faça isso dentro de seu script de hook.

O hook deve retornar o caminho absoluto para o diretório worktree criado. Claude Code usa este caminho como o diretório de trabalho para a sessão isolada. Hooks de comando imprimem em stdout; hooks HTTP retornam via `hookSpecificOutput.worktreePath`.

Este exemplo cria uma cópia de trabalho SVN e imprime o caminho para Claude Code usar. Substitua a URL do repositório pela sua:

```json theme={null}
{
  "hooks": {
    "WorktreeCreate": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'NAME=$(jq -r .name); DIR=\"$HOME/.claude/worktrees/$NAME\"; svn checkout https://svn.example.com/repo/trunk \"$DIR\" >&2 && echo \"$DIR\"'"
          }
        ]
      }
    ]
  }
}
```

O hook lê o `name` do worktree da entrada JSON em stdin, verifica uma cópia fresca em um novo diretório e imprime o caminho do diretório. O `echo` na última linha é o que Claude Code lê como o caminho do worktree. Redirecione qualquer outra saída para stderr para que não interfira com o caminho.

#### Entrada de WorktreeCreate

Além dos [campos de entrada comuns](#common-input-fields), hooks WorktreeCreate recebem o campo `name`. Este é um identificador slug para o novo worktree, especificado pelo usuário ou auto-gerado (por exemplo, `bold-oak-a3f2`).

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeCreate",
  "name": "feature-auth"
}
```

#### Saída de WorktreeCreate

Hooks WorktreeCreate não usam o modelo de decisão permitir/bloquear padrão. Em vez disso, o sucesso ou falha do hook determina o resultado. O hook deve retornar o caminho absoluto para o diretório worktree criado:

* **Hooks de comando** (`type: "command"`): imprimem o caminho em stdout.
* **Hooks HTTP** (`type: "http"`): retornam `{ "hookSpecificOutput": { "hookEventName": "WorktreeCreate", "worktreePath": "/absolute/path" } }` no corpo da resposta.

Se o hook falhar ou não produzir caminho, a criação de worktree falha com um erro.

### WorktreeRemove

A contraparte de limpeza para [WorktreeCreate](#worktreecreate). Este hook dispara quando um worktree está sendo removido, seja quando você sai de uma sessão `--worktree` e escolhe removê-lo, ou quando um subagente com `isolation: "worktree"` termina. Para worktrees baseados em git, Claude lida com limpeza automaticamente com `git worktree remove`. Se você configurou um hook WorktreeCreate para um sistema de controle de versão não-git, emparelhe-o com um hook WorktreeRemove para lidar com limpeza. Sem um, o diretório worktree é deixado no disco.

Claude Code passa o caminho que WorktreeCreate retornou como `worktree_path` na entrada do hook. Este exemplo lê esse caminho e remove o diretório:

```json theme={null}
{
  "hooks": {
    "WorktreeRemove": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'jq -r .worktree_path | xargs rm -rf'"
          }
        ]
      }
    ]
  }
}
```

#### Entrada de WorktreeRemove

Além dos [campos de entrada comuns](#common-input-fields), hooks WorktreeRemove recebem o campo `worktree_path`, que é o caminho absoluto para o worktree sendo removido.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeRemove",
  "worktree_path": "/Users/.../my-project/.claude/worktrees/feature-auth"
}
```

Hooks WorktreeRemove não têm controle de decisão. Eles não podem bloquear remoção de worktree mas podem executar tarefas de limpeza como remover estado de controle de versão ou arquivar mudanças. Falhas de hook são registradas apenas em modo debug.

### PreCompact

Executa antes do Claude Code estar prestes a executar uma operação de compactação.

O valor do matcher indica se a compactação foi acionada manualmente ou automaticamente:

| Matcher  | Quando dispara                                          |
| :------- | :------------------------------------------------------ |
| `manual` | `/compact`                                              |
| `auto`   | Auto-compactação quando a janela de contexto está cheia |

Saia com código 2 para bloquear compactação. Para um `/compact` manual, a mensagem de stderr é mostrada ao usuário. Você também pode bloquear retornando JSON com `"decision": "block"`.

Bloquear compactação automática tem efeitos diferentes dependendo de quando dispara. Se a compactação foi acionada proativamente antes do limite de contexto, Claude Code a ignora e a conversa continua não compactada. Se a compactação foi acionada para recuperar de um erro de limite de contexto já retornado pela API, o erro subjacente superficializa e a solicitação atual falha.

#### Entrada de PreCompact

Além dos [campos de entrada comuns](#common-input-fields), hooks PreCompact recebem `trigger` e `custom_instructions`. Para `manual`, `custom_instructions` contém o que o usuário passa para `/compact`. Para `auto`, `custom_instructions` está vazio.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```

### PostCompact

Executa após Claude Code completar uma operação de compactação. Use este evento para reagir ao novo estado compactado, por exemplo para registrar o resumo gerado ou atualizar estado externo.

Os mesmos valores de matcher se aplicam como para `PreCompact`:

| Matcher  | Quando dispara                                               |
| :------- | :----------------------------------------------------------- |
| `manual` | Após `/compact`                                              |
| `auto`   | Após auto-compactação quando a janela de contexto está cheia |

#### Entrada de PostCompact

Além dos [campos de entrada comuns](#common-input-fields), hooks PostCompact recebem `trigger` e `compact_summary`. O campo `compact_summary` contém o resumo de conversa gerado pela operação de compactação.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PostCompact",
  "trigger": "manual",
  "compact_summary": "Summary of the compacted conversation..."
}
```

Hooks PostCompact não têm controle de decisão. Eles não podem afetar o resultado de compactação mas podem executar tarefas de acompanhamento.

### SessionEnd

Executa quando uma sessão do Claude Code termina. Útil para tarefas de limpeza, logging de estatísticas de sessão ou salvamento de estado de sessão. Suporta matchers para filtrar por razão de saída.

O campo `reason` na entrada do hook indica por que a sessão terminou:

| Razão                         | Descrição                                              |
| :---------------------------- | :----------------------------------------------------- |
| `clear`                       | Sessão limpa com comando `/clear`                      |
| `resume`                      | Sessão alternada via `/resume` interativo              |
| `logout`                      | Usuário fez logout                                     |
| `prompt_input_exit`           | Usuário saiu enquanto entrada de prompt estava visível |
| `bypass_permissions_disabled` | Modo de permissões de bypass foi desabilitado          |
| `other`                       | Outras razões de saída                                 |

#### Entrada de SessionEnd

Além dos [campos de entrada comuns](#common-input-fields), hooks SessionEnd recebem um campo `reason` indicando por que a sessão terminou. Consulte a [tabela de razão](#sessionend) acima para todos os valores.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionEnd",
  "reason": "other"
}
```

Hooks SessionEnd não têm controle de decisão. Eles não podem bloquear terminação de sessão mas podem executar tarefas de limpeza.

Hooks SessionEnd têm um timeout padrão de 1,5 segundos. Isso se aplica tanto à saída de sessão quanto a `/clear` e alternância de sessões via `/resume` interativo. Se um hook precisa de mais tempo, defina um `timeout` por hook na configuração do hook. O orçamento geral é automaticamente aumentado para o timeout por hook mais alto configurado em arquivos de configurações, até 60 segundos. Timeouts definidos em hooks fornecidos por plugin não aumentam o orçamento. Para sobrescrever o orçamento explicitamente, defina a variável de ambiente `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` em milissegundos.

```bash theme={null}
CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS=5000 claude
```

### Elicitation

Executa quando um servidor MCP solicita entrada do usuário no meio da tarefa. Por padrão, Claude Code mostra um diálogo interativo para o usuário responder. Hooks podem interceptar esta solicitação e responder programaticamente, pulando o diálogo inteiramente.

O campo matcher corresponde ao nome do servidor MCP.

#### Entrada de Elicitation

Além dos [campos de entrada comuns](#common-input-fields), hooks Elicitation recebem `mcp_server_name`, `message` e campos opcionais `mode`, `url`, `elicitation_id` e `requested_schema`.

Para elicitação em modo de formulário (o caso mais comum):

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please provide your credentials",
  "mode": "form",
  "requested_schema": {
    "type": "object",
    "properties": {
      "username": { "type": "string", "title": "Username" }
    }
  }
}
```

Para elicitação em modo URL (autenticação baseada em navegador):

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please authenticate",
  "mode": "url",
  "url": "https://auth.example.com/login"
}
```

#### Saída de Elicitation

Para responder programaticamente sem mostrar o diálogo, retorne um objeto JSON com `hookSpecificOutput`:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "Elicitation",
    "action": "accept",
    "content": {
      "username": "alice"
    }
  }
}
```

| Campo     | Valores                       | Descrição                                                                          |
| :-------- | :---------------------------- | :--------------------------------------------------------------------------------- |
| `action`  | `accept`, `decline`, `cancel` | Se deve aceitar, recusar ou cancelar a solicitação                                 |
| `content` | object                        | Valores de campo de formulário a submeter. Apenas usado quando `action` é `accept` |

Código de saída 2 nega a elicitação e mostra stderr ao usuário.

### ElicitationResult

Executa após um usuário responder a uma elicitação MCP. Hooks podem observar, modificar ou bloquear a resposta antes de ser enviada de volta ao servidor MCP.

O campo matcher corresponde ao nome do servidor MCP.

#### Entrada de ElicitationResult

Além dos [campos de entrada comuns](#common-input-fields), hooks ElicitationResult recebem `mcp_server_name`, `action` e campos opcionais `mode`, `elicitation_id` e `content`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "ElicitationResult",
  "mcp_server_name": "my-mcp-server",
  "action": "accept",
  "content": { "username": "alice" },
  "mode": "form",
  "elicitation_id": "elicit-123"
}
```

#### Saída de ElicitationResult

Para sobrescrever a resposta do usuário, retorne um objeto JSON com `hookSpecificOutput`:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "ElicitationResult",
    "action": "decline",
    "content": {}
  }
}
```

| Campo     | Valores                       | Descrição                                                                                   |
| :-------- | :---------------------------- | :------------------------------------------------------------------------------------------ |
| `action`  | `accept`, `decline`, `cancel` | Sobrescreve a ação do usuário                                                               |
| `content` | object                        | Sobrescreve valores de campo de formulário. Apenas significativo quando `action` é `accept` |

Código de saída 2 bloqueia a resposta, mudando a ação efetiva para `decline`.

## Hooks baseados em prompt

Além de hooks de comando, HTTP e MCP tool, Claude Code suporta hooks baseados em prompt (`type: "prompt"`) que usam um LLM para avaliar se deve permitir ou bloquear uma ação, e hooks de agente (`type: "agent"`) que geram um verificador agentic com acesso a ferramentas. Nem todos os eventos suportam cada tipo de hook.

Eventos que suportam todos os cinco tipos de hook (`command`, `http`, `mcp_tool`, `prompt` e `agent`):

* `PermissionRequest`
* `PostToolBatch`
* `PostToolUse`
* `PostToolUseFailure`
* `PreToolUse`
* `Stop`
* `SubagentStop`
* `TaskCompleted`
* `TaskCreated`
* `UserPromptExpansion`
* `UserPromptSubmit`

Eventos que suportam hooks `command`, `http` e `mcp_tool` mas não `prompt` ou `agent`:

* `ConfigChange`
* `CwdChanged`
* `Elicitation`
* `ElicitationResult`
* `FileChanged`
* `InstructionsLoaded`
* `Notification`
* `PermissionDenied`
* `PostCompact`
* `PreCompact`
* `SessionEnd`
* `StopFailure`
* `SubagentStart`
* `TeammateIdle`
* `WorktreeCreate`
* `WorktreeRemove`

`SessionStart` e `Setup` suportam hooks `command` e `mcp_tool`. Eles não suportam hooks `http`, `prompt` ou `agent`.

### Como hooks baseados em prompt funcionam

Em vez de executar um comando Bash, hooks baseados em prompt:

1. Enviam a entrada do hook e seu prompt para um modelo Claude, Haiku por padrão
2. O LLM responde com JSON estruturado contendo uma decisão
3. Claude Code processa a decisão automaticamente

### Configuração de hook de prompt

Defina `type` para `"prompt"` e forneça uma string `prompt` em vez de um `command`. Use o placeholder `$ARGUMENTS` para injetar dados de entrada do hook em seu texto de prompt. Claude Code envia o prompt combinado e entrada para um modelo Claude rápido, que retorna uma decisão JSON.

Este hook `Stop` pede ao LLM para avaliar se todas as tarefas estão completas antes de permitir que Claude termine:

```json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete."
          }
        ]
      }
    ]
  }
}
```

| Campo     | Obrigatório | Descrição                                                                                                                                                                    |
| :-------- | :---------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`    | sim         | Deve ser `"prompt"`                                                                                                                                                          |
| `prompt`  | sim         | O texto do prompt a enviar para o LLM. Use `$ARGUMENTS` como placeholder para a entrada JSON do hook. Se `$ARGUMENTS` não estiver presente, entrada JSON é anexada ao prompt |
| `model`   | não         | Modelo a usar para avaliação. Padrão para um modelo rápido                                                                                                                   |
| `timeout` | não         | Timeout em segundos. Padrão: 30                                                                                                                                              |

### Esquema de resposta

O LLM deve responder com JSON contendo:

```json theme={null}
{
  "ok": true | false,
  "reason": "Explanation for the decision"
}
```

| Campo    | Descrição                                                                         |
| :------- | :-------------------------------------------------------------------------------- |
| `ok`     | `true` permite a ação, `false` a bloqueia. Veja o comportamento por evento abaixo |
| `reason` | Obrigatório quando `ok` é `false`. Explicação para a decisão                      |

O que acontece em `ok: false` depende do evento:

* `Stop` e `SubagentStop`: a razão é retornada a Claude como sua próxima instrução e o turno continua
* `PreToolUse`: a chamada de ferramenta é negada e a razão é retornada a Claude como o erro da ferramenta, equivalente a um hook de comando com `permissionDecision: "deny"`
* `PostToolUse`, `PostToolBatch`, `UserPromptSubmit` e `UserPromptExpansion`: o turno termina e a razão aparece no chat como uma linha de aviso, equivalente a retornar `"continue": false` de um hook de comando
* `PostToolUseFailure`, `TaskCreated` e `TaskCompleted`: a razão é retornada a Claude como um erro de ferramenta, similar a `PreToolUse`
* `PermissionRequest`: `ok: false` não tem efeito. Para negar uma aprovação de um hook, use um [hook de comando](#command-hook-fields) retornando `hookSpecificOutput.decision.behavior: "deny"`

Se você precisar de controle mais fino em qualquer evento, use um [hook de comando](#command-hook-fields) com os campos por evento descritos em [Controle de decisão](#decision-control).

### Exemplo: Hook Stop com múltiplos critérios

Este hook `Stop` usa um prompt detalhado para verificar três condições antes de permitir que Claude pare. Se `"ok"` for `false`, Claude continua trabalhando com a razão fornecida como sua próxima instrução. Hooks `SubagentStop` usam o mesmo formato para avaliar se um [subagente](/pt/sub-agents) deve parar:

```json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are evaluating whether Claude should stop working. Context: $ARGUMENTS\n\nAnalyze the conversation and determine if:\n1. All user-requested tasks are complete\n2. Any errors need to be addressed\n3. Follow-up work is needed\n\nRespond with JSON: {\"ok\": true} to allow stopping, or {\"ok\": false, \"reason\": \"your explanation\"} to continue working.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Hooks baseados em agente

<Warning>
  Hooks de agente são experimentais. O comportamento e a configuração podem mudar em versões futuras. Para fluxos de trabalho em produção, prefira [command hooks](#command-hook-fields).
</Warning>

Hooks baseados em agente (`type: "agent"`) são como hooks baseados em prompt mas com acesso a ferramentas de múltiplos turnos. Em vez de uma única chamada LLM, um hook de agente gera um subagente que pode ler arquivos, pesquisar código e inspecionar o codebase para verificar condições. Hooks de agente suportam os mesmos eventos que hooks baseados em prompt.

### Como hooks de agente funcionam

Quando um hook de agente dispara:

1. Claude Code gera um subagente com seu prompt e a entrada JSON do hook
2. O subagente pode usar ferramentas como Read, Grep e Glob para investigar
3. Após até 50 turnos, o subagente retorna uma decisão estruturada `{ "ok": true/false }`
4. Claude Code processa a decisão da mesma forma que um hook de prompt

Hooks de agente são úteis quando a verificação requer inspecionar arquivos reais ou saída de teste, não apenas avaliar dados de entrada do hook sozinhos.

### Configuração de hook de agente

Defina `type` para `"agent"` e forneça uma string `prompt`. Os campos de configuração são os mesmos que [hooks de prompt](#prompt-hook-configuration), com um timeout padrão mais longo:

| Campo     | Obrigatório | Descrição                                                                                         |
| :-------- | :---------- | :------------------------------------------------------------------------------------------------ |
| `type`    | sim         | Deve ser `"agent"`                                                                                |
| `prompt`  | sim         | Prompt descrevendo o que verificar. Use `$ARGUMENTS` como placeholder para a entrada JSON do hook |
| `model`   | não         | Modelo a usar. Padrão para um modelo rápido                                                       |
| `timeout` | não         | Timeout em segundos. Padrão: 60                                                                   |

O esquema de resposta é o mesmo que hooks de prompt: `{ "ok": true }` para permitir ou `{ "ok": false, "reason": "..." }` para bloquear.

Este hook `Stop` verifica que todos os testes unitários passam antes de permitir que Claude termine:

```json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

## Executar hooks em background

Por padrão, hooks bloqueiam a execução de Claude até que completem. Para tarefas de longa duração como deployments, suites de teste ou chamadas de API externas, defina `"async": true` para executar o hook em background enquanto Claude continua trabalhando. Hooks assíncronos não podem bloquear ou controlar comportamento de Claude: campos de resposta como `decision`, `permissionDecision` e `continue` não têm efeito, porque a ação que controlariam já completou.

### Configurar um hook assíncrono

Adicione `"async": true` à configuração de um hook de comando para executá-lo em background sem bloquear Claude. Este campo está apenas disponível em hooks `type: "command"`.

Este hook executa um script de teste após cada chamada de ferramenta `Write`. Claude continua trabalhando imediatamente enquanto `run-tests.sh` executa por até 120 segundos. Quando o script termina, sua saída é entregue no próximo turno de conversa:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/run-tests.sh",
            "async": true,
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

O campo `timeout` define o tempo máximo em segundos para o processo em background. Se não especificado, hooks assíncronos usam o mesmo padrão de 10 minutos que hooks síncronos.

### Como hooks assíncronos executam

Quando um hook assíncrono dispara, Claude Code inicia o processo do hook e imediatamente continua sem esperar que termine. O hook recebe a mesma entrada JSON via stdin que um hook síncrono.

Após o processo em background sair, se o hook produziu uma resposta JSON com um campo `systemMessage` ou `additionalContext`, esse conteúdo é entregue ao Claude como contexto no próximo turno de conversa.

Notificações de conclusão de hook assíncrono são suprimidas por padrão. Para vê-las, ative modo verbose com `Ctrl+O` ou inicie Claude Code com `--verbose`.

### Exemplo: executar testes após mudanças de arquivo

Este hook inicia uma suite de testes em background sempre que Claude escreve um arquivo, então relata os resultados de volta ao Claude quando os testes terminam. Salve este script em `.claude/hooks/run-tests-async.sh` em seu projeto e torne-o executável com `chmod +x`:

```bash theme={null}
#!/bin/bash
# run-tests-async.sh

# Leia entrada de hook de stdin
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Apenas execute testes para arquivos de origem
if [[ "$FILE_PATH" != *.ts && "$FILE_PATH" != *.js ]]; then
  exit 0
fi

# Execute testes e relate resultados via systemMessage
RESULT=$(npm test 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "{\"systemMessage\": \"Tests passed after editing $FILE_PATH\"}"
else
  echo "{\"systemMessage\": \"Tests failed after editing $FILE_PATH: $RESULT\"}"
fi
```

Então adicione esta configuração a `.claude/settings.json` na raiz do seu projeto. A flag `async: true` permite que Claude continue trabalhando enquanto testes executam:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/run-tests-async.sh",
            "async": true,
            "timeout": 300
          }
        ]
      }
    ]
  }
}
```

### Limitações

Hooks assíncronos têm várias restrições comparados a hooks síncronos:

* Apenas hooks `type: "command"` suportam `async`. Hooks baseados em prompt não podem executar assincronamente.
* Hooks assíncronos não podem bloquear chamadas de ferramenta ou retornar decisões. Pelo tempo que o hook completa, a ação acionadora já prosseguiu.
* Saída de hook é entregue no próximo turno de conversa. Se a sessão está ociosa, a resposta espera até a próxima interação do usuário. Exceção: um hook `asyncRewake` que sai com código 2 acorda Claude imediatamente mesmo quando a sessão está ociosa.
* Cada execução cria um processo em background separado. Não há desduplicação através de múltiplos disparos do mesmo hook assíncrono.

## Considerações de segurança

### Aviso

Hooks de comando executam com as permissões completas do seu usuário do sistema.

<Warning>
  Hooks de comando executam comandos shell com suas permissões completas de usuário. Eles podem modificar, deletar ou acessar qualquer arquivo que sua conta de usuário pode acessar. Revise e teste todos os comandos de hook antes de adicioná-los à sua configuração.
</Warning>

### Melhores práticas de segurança

Mantenha essas práticas em mente ao escrever hooks:

* **Valide e sanitize entradas**: nunca confie em dados de entrada cegamente
* **Sempre cite variáveis shell**: use `"$VAR"` não `$VAR`
* **Bloqueie traversal de caminho**: verifique `..` em caminhos de arquivo
* **Use caminhos absolutos**: especifique caminhos completos para scripts, usando `"$CLAUDE_PROJECT_DIR"` para a raiz do projeto
* **Pule arquivos sensíveis**: evite `.env`, `.git/`, chaves, etc.

## Ferramenta Windows PowerShell

No Windows, você pode executar hooks individuais em PowerShell definindo `"shell": "powershell"` em um hook de comando. Hooks geram PowerShell diretamente, então isso funciona independentemente de `CLAUDE_CODE_USE_POWERSHELL_TOOL` estar definido. Claude Code auto-detecta `pwsh.exe` (PowerShell 7+) com fallback para `powershell.exe` (5.1).

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "shell": "powershell",
            "command": "Write-Host 'File written'"
          }
        ]
      }
    ]
  }
}
```

## Debug de hooks

Detalhes de execução de hook, incluindo quais hooks corresponderam, seus códigos de saída e saída completa de stdout e stderr, são escritos no arquivo de log de debug. Inicie Claude Code com `claude --debug-file <path>` para escrever o log em um local conhecido, ou execute `claude --debug` e leia o log em `~/.claude/debug/<session-id>.txt`. A flag `--debug` não imprime no terminal.

```text theme={null}
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 600000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

Para detalhes de correspondência de hook mais granulares, defina `CLAUDE_CODE_DEBUG_LOG_LEVEL=verbose` para ver linhas de log adicionais como contagens de matcher de hook e correspondência de consulta.

Para troubleshooting de problemas comuns como hooks não disparando, loops infinitos de hook Stop ou erros de configuração, consulte [Limitações e troubleshooting](/pt/hooks-guide#limitations-and-troubleshooting) no guia. Para um passo a passo de diagnóstico mais amplo cobrindo `/context`, `/doctor` e precedência de configurações, consulte [Debug your config](/pt/debug-your-config).
