> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Referência de plugins

> Referência técnica completa para o sistema de plugins do Claude Code, incluindo esquemas, comandos CLI e especificações de componentes.

<Tip>
  Procurando instalar plugins? Veja [Descobrir e instalar plugins](/pt/discover-plugins). Para criar plugins, veja [Plugins](/pt/plugins). Para distribuir plugins, veja [Marketplaces de plugins](/pt/plugin-marketplaces).
</Tip>

Esta referência fornece especificações técnicas completas para o sistema de plugins do Claude Code, incluindo esquemas de componentes, comandos CLI e ferramentas de desenvolvimento.

Um **plugin** é um diretório independente de componentes que estende o Claude Code com funcionalidade personalizada. Os componentes do plugin incluem skills, agents, hooks, servidores MCP, servidores LSP e monitors.

## Referência de componentes de plugin

### Skills

Os plugins adicionam skills ao Claude Code, criando atalhos `/name` que você ou Claude podem invocar.

**Localização**: Diretório `skills/` ou `commands/` na raiz do plugin

**Formato de arquivo**: Skills são diretórios com `SKILL.md`; comandos são arquivos markdown simples

**Estrutura de skill**:

```text theme={null}
skills/
├── pdf-processor/
│   ├── SKILL.md
│   ├── reference.md (opcional)
│   └── scripts/ (opcional)
└── code-reviewer/
    └── SKILL.md
```

**Comportamento de integração**:

* Skills e comandos são descobertos automaticamente quando o plugin é instalado
* Claude pode invocá-los automaticamente com base no contexto da tarefa
* Skills podem incluir arquivos de suporte ao lado de SKILL.md

Para detalhes completos, veja [Skills](/pt/skills).

### Agents

Os plugins podem fornecer subagents especializados para tarefas específicas que Claude pode invocar automaticamente quando apropriado.

**Localização**: Diretório `agents/` na raiz do plugin

**Formato de arquivo**: Arquivos markdown descrevendo capacidades do agent

**Estrutura de agent**:

```markdown theme={null}
---
name: agent-name
description: No que este agent se especializa e quando Claude deve invocá-lo
model: sonnet
effort: medium
maxTurns: 20
disallowedTools: Write, Edit
---

Prompt de sistema detalhado para o agent descrevendo seu papel, expertise e comportamento.
```

Os agents de plugin suportam campos frontmatter `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background` e `isolation`. O único valor válido de `isolation` é `"worktree"`. Por razões de segurança, `hooks`, `mcpServers` e `permissionMode` não são suportados para agents fornecidos por plugin.

**Pontos de integração**:

* Agents aparecem na interface `/agents`
* Claude pode invocar agents automaticamente com base no contexto da tarefa
* Agents podem ser invocados manualmente por usuários
* Agents de plugin funcionam ao lado de agents Claude integrados

Para detalhes completos, veja [Subagents](/pt/sub-agents).

### Hooks

Os plugins podem fornecer manipuladores de eventos que respondem a eventos do Claude Code automaticamente.

**Localização**: `hooks/hooks.json` na raiz do plugin, ou inline em plugin.json

**Formato**: Configuração JSON com matchers de eventos e ações

**Configuração de hook**:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

Os hooks de plugin respondem aos mesmos eventos de ciclo de vida que [hooks definidos pelo usuário](/pt/hooks):

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

**Tipos de hook**:

* `command`: executar comandos shell ou scripts
* `http`: enviar o JSON do evento como uma solicitação POST para uma URL
* `mcp_tool`: chamar uma ferramenta em um servidor [MCP](/pt/mcp) configurado
* `prompt`: avaliar um prompt com um LLM (usa placeholder `$ARGUMENTS` para contexto)
* `agent`: executar um verificador agentic com ferramentas para tarefas de verificação complexas

### MCP servers

Os plugins podem agrupar servidores Model Context Protocol (MCP) para conectar Claude Code com ferramentas e serviços externos.

**Localização**: `.mcp.json` na raiz do plugin, ou inline em plugin.json

**Formato**: Configuração padrão de servidor MCP

**Configuração de servidor MCP**:

```json theme={null}
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    },
    "plugin-api-client": {
      "command": "npx",
      "args": ["@company/mcp-server", "--plugin-mode"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

**Comportamento de integração**:

* Servidores MCP de plugin iniciam automaticamente quando o plugin é habilitado
* Servidores aparecem como ferramentas MCP padrão no kit de ferramentas de Claude
* Capacidades do servidor se integram perfeitamente com as ferramentas existentes de Claude
* Servidores de plugin podem ser configurados independentemente de servidores MCP do usuário

### LSP servers

<Tip>
  Procurando usar plugins LSP? Instale-os do marketplace oficial: procure por "lsp" na aba Discover do `/plugin`. Esta seção documenta como criar plugins LSP para linguagens não cobertas pelo marketplace oficial.
</Tip>

Os plugins podem fornecer servidores [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) (LSP) para dar a Claude inteligência de código em tempo real enquanto trabalha em seu codebase.

A integração LSP fornece:

* **Diagnósticos instantâneos**: Claude vê erros e avisos imediatamente após cada edição
* **Navegação de código**: ir para definição, encontrar referências e informações de hover
* **Consciência de linguagem**: informações de tipo e documentação para símbolos de código

**Localização**: `.lsp.json` na raiz do plugin, ou inline em `plugin.json`

**Formato**: Configuração JSON mapeando nomes de servidores de linguagem para suas configurações

**Formato de arquivo `.lsp.json`**:

```json theme={null}
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

**Inline em `plugin.json`**:

```json theme={null}
{
  "name": "my-plugin",
  "lspServers": {
    "go": {
      "command": "gopls",
      "args": ["serve"],
      "extensionToLanguage": {
        ".go": "go"
      }
    }
  }
}
```

**Campos obrigatórios:**

| Campo                 | Descrição                                                     |
| :-------------------- | :------------------------------------------------------------ |
| `command`             | O binário LSP a executar (deve estar em PATH)                 |
| `extensionToLanguage` | Mapeia extensões de arquivo para identificadores de linguagem |

**Campos opcionais:**

| Campo                   | Descrição                                                            |
| :---------------------- | :------------------------------------------------------------------- |
| `args`                  | Argumentos de linha de comando para o servidor LSP                   |
| `transport`             | Transporte de comunicação: `stdio` (padrão) ou `socket`              |
| `env`                   | Variáveis de ambiente a definir ao iniciar o servidor                |
| `initializationOptions` | Opções passadas ao servidor durante a inicialização                  |
| `settings`              | Configurações passadas via `workspace/didChangeConfiguration`        |
| `workspaceFolder`       | Caminho da pasta de workspace para o servidor                        |
| `startupTimeout`        | Tempo máximo para aguardar inicialização do servidor (milissegundos) |
| `shutdownTimeout`       | Tempo máximo para aguardar encerramento gracioso (milissegundos)     |
| `restartOnCrash`        | Se deve reiniciar automaticamente o servidor se ele falhar           |
| `maxRestarts`           | Número máximo de tentativas de reinicialização antes de desistir     |

<Warning>
  **Você deve instalar o binário do servidor de linguagem separadamente.** Plugins LSP configuram como Claude Code se conecta a um servidor de linguagem, mas não incluem o servidor em si. Se você vir `Executable not found in $PATH` na aba Errors do `/plugin`, instale o binário necessário para sua linguagem.
</Warning>

**Plugins LSP disponíveis:**

| Plugin              | Servidor de linguagem      | Comando de instalação                                                                        |
| :------------------ | :------------------------- | :------------------------------------------------------------------------------------------- |
| `pyright-lsp`       | Pyright (Python)           | `pip install pyright` ou `npm install -g pyright`                                            |
| `typescript-lsp`    | TypeScript Language Server | `npm install -g typescript-language-server typescript`                                       |
| `rust-analyzer-lsp` | rust-analyzer              | [Veja instalação de rust-analyzer](https://rust-analyzer.github.io/manual.html#installation) |

Instale o servidor de linguagem primeiro, depois instale o plugin do marketplace.

### Monitors

Os plugins podem declarar monitors de fundo que Claude Code inicia automaticamente quando o plugin está ativo. Cada monitor executa um comando shell pela duração da sessão e entrega cada linha stdout a Claude como uma notificação, para que Claude possa reagir a entradas de log, mudanças de status ou eventos pesquisados sem ser solicitado a iniciar o watch em si.

Os monitors de plugin usam o mesmo mecanismo que a [ferramenta Monitor](/pt/tools-reference#monitor-tool) e compartilham suas restrições de disponibilidade. Eles são executados apenas em sessões CLI interativas, executados sem sandbox no mesmo nível de confiança que [hooks](#hooks), e são ignorados em hosts onde a ferramenta Monitor não está disponível.

<Note>
  Os monitors de plugin requerem Claude Code v2.1.105 ou posterior.
</Note>

**Localização**: `monitors/monitors.json` na raiz do plugin, ou inline em `plugin.json`

**Formato**: Array JSON de entradas de monitor

O seguinte `monitors/monitors.json` monitora um endpoint de status de implantação e um log de erro local:

```json theme={null}
[
  {
    "name": "deploy-status",
    "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/poll-deploy.sh ${user_config.api_endpoint}",
    "description": "Mudanças de status de implantação"
  },
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Log de erro da aplicação",
    "when": "on-skill-invoke:debug"
  }
]
```

Para declarar monitors inline, defina `experimental.monitors` em `plugin.json` para o mesmo array. Para carregar de um caminho não padrão, defina `experimental.monitors` para uma string de caminho relativo como `"./config/monitors.json"`. Monitors são um [componente experimental](#experimental-components).

**Campos obrigatórios:**

| Campo         | Descrição                                                                                                                      |
| :------------ | :----------------------------------------------------------------------------------------------------------------------------- |
| `name`        | Identificador único dentro do plugin. Previne processos duplicados quando o plugin recarrega ou uma skill é invocada novamente |
| `command`     | Comando shell executado como um processo de fundo persistente no diretório de trabalho da sessão                               |
| `description` | Resumo breve do que está sendo monitorado. Mostrado no painel de tarefas e em resumos de notificação                           |

**Campos opcionais:**

| Campo  | Descrição                                                                                                                                                                                                                      |
| :----- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `when` | Controla quando o monitor inicia. `"always"` o inicia no início da sessão e no recarregamento do plugin, e é o padrão. `"on-skill-invoke:<skill-name>"` o inicia na primeira vez que a skill nomeada neste plugin é despachada |

O valor `command` suporta as mesmas [substituições de variáveis](#environment-variables) que configurações de servidor MCP e LSP: `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, `${CLAUDE_PROJECT_DIR}`, `${user_config.*}` e qualquer `${ENV_VAR}` do ambiente. Prefixe o comando com `cd "${CLAUDE_PLUGIN_ROOT}" && ` se o script precisa ser executado do próprio diretório do plugin.

Desabilitar um plugin no meio da sessão não para monitors que já estão em execução. Eles param quando a sessão termina.

### Themes

Os plugins podem fornecer temas de cor que aparecem em `/theme` ao lado das predefinições integradas e dos temas locais do usuário. Um tema é um arquivo JSON em `themes/` com uma predefinição `base` e um mapa esparso `overrides` de tokens de cor. Themes são um [componente experimental](#experimental-components).

```json theme={null}
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555",
    "success": "#50fa7b"
  }
}
```

Selecionar um tema de plugin persiste `custom:<plugin-name>:<slug>` na configuração do usuário. Temas de plugin são somente leitura; pressionar `Ctrl+E` em um em `/theme` o copia para `~/.claude/themes/` para que o usuário possa editar a cópia.

***

## Escopos de instalação de plugin

Quando você instala um plugin, você escolhe um **escopo** que determina onde o plugin está disponível e quem mais pode usá-lo:

| Escopo    | Arquivo de configurações                                 | Caso de uso                                                |
| :-------- | :------------------------------------------------------- | :--------------------------------------------------------- |
| `user`    | `~/.claude/settings.json`                                | Plugins pessoais disponíveis em todos os projetos (padrão) |
| `project` | `.claude/settings.json`                                  | Plugins de equipe compartilhados via controle de versão    |
| `local`   | `.claude/settings.local.json`                            | Plugins específicos do projeto, gitignored                 |
| `managed` | [Configurações gerenciadas](/pt/settings#settings-files) | Plugins gerenciados (somente leitura, apenas atualizar)    |

Os plugins usam o mesmo sistema de escopo que outras configurações do Claude Code. Para instruções de instalação e flags de escopo, veja [Instalar plugins](/pt/discover-plugins#install-plugins). Para uma explicação completa de escopos, veja [Escopos de configuração](/pt/settings#configuration-scopes).

***

## Esquema de manifesto de plugin

O arquivo `.claude-plugin/plugin.json` define os metadados e configuração do seu plugin. Esta seção documenta todos os campos e opções suportados.

O manifesto é opcional. Se omitido, Claude Code descobre automaticamente componentes em [localizações padrão](#file-locations-reference) e deriva o nome do plugin do nome do diretório. Use um manifesto quando você precisar fornecer metadados ou caminhos de componentes personalizados.

### Esquema completo

```json theme={null}
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "skills": "./custom/skills/",
  "commands": ["./custom/commands/special.md"],
  "agents": ["./custom/agents/reviewer.md"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json",
  "experimental": {
    "themes": "./themes/",
    "monitors": "./monitors.json"
  },
  "dependencies": [
    "helper-lib",
    { "name": "secrets-vault", "version": "~2.1.0" }
  ]
}
```

### Campos obrigatórios

Se você incluir um manifesto, `name` é o único campo obrigatório.

| Campo  | Tipo   | Descrição                                     | Exemplo              |
| :----- | :----- | :-------------------------------------------- | :------------------- |
| `name` | string | Identificador único (kebab-case, sem espaços) | `"deployment-tools"` |

Este nome é usado para namespacing de componentes. Por exemplo, na UI, o agent `agent-creator` para o plugin com nome `plugin-dev` aparecerá como `plugin-dev:agent-creator`.

### Campos de metadados

| Campo         | Tipo   | Descrição                                                                                                                                                                                                                                                                                                                                                                                | Exemplo                                                           |
| :------------ | :----- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------- |
| `$schema`     | string | URL do JSON Schema para autocomplete e validação do editor. Claude Code ignora este campo no momento do carregamento.                                                                                                                                                                                                                                                                    | `"https://json.schemastore.org/claude-code-plugin-manifest.json"` |
| `version`     | string | Opcional. Versão semântica. Definir isso fixa o plugin para essa string de versão, então os usuários só recebem atualizações quando você a incrementa. Se omitido, Claude Code volta para o SHA do commit git, então cada commit é tratado como uma nova versão. Se também definido na entrada do marketplace, `plugin.json` vence. Veja [Gerenciamento de versão](#version-management). | `"2.1.0"`                                                         |
| `description` | string | Explicação breve do propósito do plugin                                                                                                                                                                                                                                                                                                                                                  | `"Deployment automation tools"`                                   |
| `author`      | object | Informações do autor                                                                                                                                                                                                                                                                                                                                                                     | `{"name": "Dev Team", "email": "dev@company.com"}`                |
| `homepage`    | string | URL de documentação                                                                                                                                                                                                                                                                                                                                                                      | `"https://docs.example.com"`                                      |
| `repository`  | string | URL do código-fonte                                                                                                                                                                                                                                                                                                                                                                      | `"https://github.com/user/plugin"`                                |
| `license`     | string | Identificador de licença                                                                                                                                                                                                                                                                                                                                                                 | `"MIT"`, `"Apache-2.0"`                                           |
| `keywords`    | array  | Tags de descoberta                                                                                                                                                                                                                                                                                                                                                                       | `["deployment", "ci-cd"]`                                         |

### Campos de caminho de componente

| Campo                   | Tipo                  | Descrição                                                                                                                                                                    | Exemplo                                              |
| :---------------------- | :-------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------- |
| `skills`                | string\|array         | Diretórios de skill personalizados contendo `<name>/SKILL.md` (além do padrão `skills/`)                                                                                     | `"./custom/skills/"`                                 |
| `commands`              | string\|array         | Arquivos de skill `.md` planos personalizados ou diretórios (substitui padrão `commands/`)                                                                                   | `"./custom/cmd.md"` ou `["./cmd1.md"]`               |
| `agents`                | string\|array         | Arquivos de agent personalizados (substitui padrão `agents/`)                                                                                                                | `"./custom/agents/reviewer.md"`                      |
| `hooks`                 | string\|array\|object | Caminhos de configuração de hooks ou configuração inline                                                                                                                     | `"./my-extra-hooks.json"`                            |
| `mcpServers`            | string\|array\|object | Caminhos de configuração MCP ou configuração inline                                                                                                                          | `"./my-extra-mcp-config.json"`                       |
| `outputStyles`          | string\|array         | Arquivos/diretórios de estilo de saída personalizados (substitui padrão `output-styles/`)                                                                                    | `"./styles/"`                                        |
| `lspServers`            | string\|array\|object | Configurações [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) para inteligência de código (ir para definição, encontrar referências, etc.) | `"./.lsp.json"`                                      |
| `experimental.themes`   | string\|array         | Arquivos/diretórios de tema de cor (substitui padrão `themes/`). Veja [Temas](#themes)                                                                                       | `"./themes/"`                                        |
| `experimental.monitors` | string\|array         | Configurações de [Monitor](/pt/tools-reference#monitor-tool) de fundo que iniciam automaticamente quando o plugin está ativo. Veja [Monitors](#monitors)                     | `"./monitors.json"`                                  |
| `userConfig`            | object                | Valores configuráveis pelo usuário solicitados no momento da habilitação. Veja [Configuração do usuário](#user-configuration)                                                | Veja abaixo                                          |
| `channels`              | array                 | Declarações de canal para injeção de mensagens (estilo Telegram, Slack, Discord). Veja [Canais](#channels)                                                                   | Veja abaixo                                          |
| `dependencies`          | array                 | Outros plugins que este plugin requer, opcionalmente com restrições de versão semver. Veja [Restringir versões de dependência de plugin](/pt/plugin-dependencies)            | `[{ "name": "secrets-vault", "version": "~2.1.0" }]` |

### Componentes experimentais

Componentes sob a chave `experimental`, `themes` e `monitors`, têm um esquema de manifesto que pode mudar entre versões enquanto se estabilizam. Onde você os declara é uma migração separada: o nível superior ainda funciona, `claude plugin validate` avisa, e uma versão futura exigirá `experimental.*`.

### Configuração do usuário

O campo `userConfig` declara valores que Claude Code solicita ao usuário quando o plugin é habilitado. Use isso em vez de exigir que os usuários editem manualmente `settings.json`.

```json theme={null}
{
  "userConfig": {
    "api_endpoint": {
      "type": "string",
      "title": "API endpoint",
      "description": "O endpoint de API da sua equipe"
    },
    "api_token": {
      "type": "string",
      "title": "API token",
      "description": "Token de autenticação de API",
      "sensitive": true
    }
  }
}
```

As chaves devem ser identificadores válidos. Cada opção suporta estes campos:

| Campo         | Obrigatório | Descrição                                                                                       |
| :------------ | :---------- | :---------------------------------------------------------------------------------------------- |
| `type`        | Sim         | Um de `string`, `number`, `boolean`, `directory`, ou `file`                                     |
| `title`       | Sim         | Rótulo mostrado no diálogo de configuração                                                      |
| `description` | Sim         | Texto de ajuda mostrado abaixo do campo                                                         |
| `sensitive`   | Não         | Se `true`, mascara entrada e armazena o valor em armazenamento seguro em vez de `settings.json` |
| `required`    | Não         | Se `true`, validação falha quando o campo está vazio                                            |
| `default`     | Não         | Valor usado quando o usuário não fornece nada                                                   |
| `multiple`    | Não         | Para tipo `string`, permite um array de strings                                                 |
| `min` / `max` | Não         | Limites para tipo `number`                                                                      |

Cada valor está disponível para substituição como `${user_config.KEY}` em configurações de servidor MCP e LSP, comandos de hook e comandos de monitor. Valores não sensíveis também podem ser substituídos em conteúdo de skill e agent. Todos os valores são exportados para subprocessos de plugin como variáveis de ambiente `CLAUDE_PLUGIN_OPTION_<KEY>`.

Valores não sensíveis são armazenados em `settings.json` sob `pluginConfigs[<plugin-id>].options`. Valores sensíveis vão para o chaveiro do sistema (ou `~/.claude/.credentials.json` onde o chaveiro não está disponível). O armazenamento em chaveiro é compartilhado com tokens OAuth e tem um limite total aproximado de 2 KB, então mantenha valores sensíveis pequenos.

### Canais

O campo `channels` permite que um plugin declare um ou mais canais de mensagem que injetam conteúdo na conversa. Cada canal se vincula a um servidor MCP que o plugin fornece.

```json theme={null}
{
  "channels": [
    {
      "server": "telegram",
      "userConfig": {
        "bot_token": {
          "type": "string",
          "title": "Bot token",
          "description": "Token do bot Telegram",
          "sensitive": true
        },
        "owner_id": {
          "type": "string",
          "title": "Owner ID",
          "description": "Seu ID de usuário Telegram"
        }
      }
    }
  ]
}
```

O campo `server` é obrigatório e deve corresponder a uma chave em `mcpServers` do plugin. O `userConfig` opcional por canal usa o mesmo esquema que o campo de nível superior, permitindo que o plugin solicite tokens de bot ou IDs de proprietário quando o plugin é habilitado.

### Regras de comportamento de caminho

Se um caminho personalizado substitui ou estende o diretório padrão do plugin depende do campo:

* **Substitui o padrão**: `commands`, `agents`, `outputStyles`, `experimental.themes`, `experimental.monitors`. Por exemplo, quando o manifesto especifica `commands`, o diretório padrão `commands/` não é verificado. Para manter o padrão e adicionar mais, liste-o explicitamente: `"commands": ["./commands/", "./extras/"]`
* **Adiciona ao padrão**: `skills`. O diretório padrão `skills/` é sempre verificado, e diretórios listados em `skills` são carregados junto com ele
* **Regras de mesclagem próprias**: [hooks](#hooks), [MCP servers](#mcp-servers) e [LSP servers](#lsp-servers). Veja cada seção para como múltiplas fontes se combinam

Quando um plugin tem tanto uma pasta padrão quanto a chave de manifesto correspondente, Claude Code v2.1.140 e posterior sinaliza a pasta ignorada em `/doctor`, `claude plugin list` e a visualização de detalhes `/plugin`. O plugin ainda carrega usando os caminhos do manifesto. Nenhum aviso é mostrado quando a chave de manifesto aponta para a pasta padrão, por exemplo `"commands": ["./commands/deploy.md"]`, porque a pasta é abordada explicitamente nesse caso.

Para todos os campos de caminho:

* Todos os caminhos devem ser relativos à raiz do plugin e começar com `./`
* Componentes de caminhos personalizados usam as mesmas regras de nomenclatura e namespacing
* Múltiplos caminhos podem ser especificados como arrays
* Quando um caminho de skill aponta para um diretório que contém um `SKILL.md` diretamente, por exemplo `"skills": ["./"]` apontando para a raiz do plugin, o campo frontmatter `name` em `SKILL.md` determina o nome de invocação da skill. Isso fornece um nome estável independentemente do diretório de instalação. Se `name` não estiver definido no frontmatter, o nome base do diretório é usado como fallback.

**Exemplos de caminho**:

```json theme={null}
{
  "commands": [
    "./specialized/deploy.md",
    "./utilities/batch-process.md"
  ],
  "agents": [
    "./custom-agents/reviewer.md",
    "./custom-agents/tester.md"
  ]
}
```

### Variáveis de ambiente

Claude Code fornece três variáveis para referenciar caminhos. Todas são substituídas inline em qualquer lugar que apareçam em conteúdo de skill, conteúdo de agent, comandos de hook, comandos de monitor e configurações de servidor MCP ou LSP. Todas também são exportadas como variáveis de ambiente para processos de hook e subprocessos de servidor MCP ou LSP.

**`${CLAUDE_PLUGIN_ROOT}`**: o caminho absoluto para o diretório de instalação do seu plugin. Use isso para referenciar scripts, binários e arquivos de configuração agrupados com o plugin. Em comandos de hook, use [forma exec](/pt/hooks#exec-form-and-shell-form) com `args` para que o caminho seja passado como um argumento com nenhuma citação. Em hooks de forma shell e comandos de monitor, envolva-o em aspas duplas, como em `"${CLAUDE_PLUGIN_ROOT}"`. Este caminho muda quando o plugin é atualizado. O diretório da versão anterior permanece no disco por aproximadamente sete dias após uma atualização antes da limpeza, mas trate-o como efêmero e não escreva estado aqui.

Quando um plugin é atualizado no meio de uma sessão, comandos de hook, monitors, servidores MCP e servidores LSP continuam usando o caminho da versão anterior. Execute `/reload-plugins` para alternar hooks, servidores MCP e servidores LSP para o novo caminho; monitors requerem uma reinicialização de sessão.

**`${CLAUDE_PLUGIN_DATA}`**: um diretório persistente para estado do plugin que sobrevive a atualizações. Use isso para dependências instaladas como `node_modules` ou ambientes virtuais Python, código gerado, caches e quaisquer outros arquivos que devem persistir entre versões de plugin. O diretório é criado automaticamente na primeira vez que esta variável é referenciada.

**`${CLAUDE_PROJECT_DIR}`**: a raiz do projeto. Este é o mesmo diretório que hooks recebem em sua variável `CLAUDE_PROJECT_DIR`. Use isso para referenciar scripts ou arquivos de configuração locais do projeto. Envolva em aspas para lidar com caminhos com espaços, por exemplo `"${CLAUDE_PROJECT_DIR}/scripts/server.sh"`. Servidores MCP também podem chamar a solicitação MCP `roots/list`, que retorna o diretório do qual Claude Code foi iniciado.

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

#### Diretório de dados persistente

O diretório `${CLAUDE_PLUGIN_DATA}` resolve para `~/.claude/plugins/data/{id}/`, onde `{id}` é o identificador do plugin com caracteres fora de `a-z`, `A-Z`, `0-9`, `_` e `-` substituídos por `-`. Para um plugin instalado como `formatter@my-marketplace`, o diretório é `~/.claude/plugins/data/formatter-my-marketplace/`.

Um uso comum é instalar dependências de linguagem uma vez e reutilizá-las em sessões e atualizações de plugin. Como o diretório de dados sobrevive a qualquer versão única de plugin, uma verificação de existência de diretório sozinha não pode detectar quando uma atualização muda o manifesto de dependência do plugin. O padrão recomendado compara o manifesto agrupado contra uma cópia no diretório de dados e reinstala quando diferem.

Este hook `SessionStart` instala `node_modules` na primeira execução e novamente sempre que uma atualização de plugin inclui um `package.json` alterado:

```json theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cd \"${CLAUDE_PLUGIN_DATA}\" && cp \"${CLAUDE_PLUGIN_ROOT}/package.json\" . && npm install) || rm -f \"${CLAUDE_PLUGIN_DATA}/package.json\""
          }
        ]
      }
    ]
  }
}
```

O `diff` sai com código diferente de zero quando a cópia armazenada está faltando ou difere da agrupada, cobrindo tanto a primeira execução quanto atualizações que mudam dependências. Se `npm install` falhar, o `rm` final remove o manifesto copiado para que a próxima sessão tente novamente.

Scripts agrupados em `${CLAUDE_PLUGIN_ROOT}` podem então executar contra o `node_modules` persistido:

```json theme={null}
{
  "mcpServers": {
    "routines": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
      "env": {
        "NODE_PATH": "${CLAUDE_PLUGIN_DATA}/node_modules"
      }
    }
  }
}
```

O diretório de dados é deletado automaticamente quando você desinstala o plugin do último escopo onde está instalado. A interface `/plugin` mostra o tamanho do diretório e solicita confirmação antes de deletar. O CLI deleta por padrão; passe [`--keep-data`](#plugin-uninstall) para preservá-lo.

***

## Cache de plugin e resolução de arquivo

Os plugins são especificados de uma de duas maneiras:

* Através de `claude --plugin-dir` ou `claude --plugin-url`, pela duração de uma sessão.
* Através de um marketplace, instalado para sessões futuras.

Para fins de segurança e verificação, Claude Code copia plugins do *marketplace* para o **cache de plugin** local do usuário (`~/.claude/plugins/cache`) em vez de usá-los no local. Entender esse comportamento é importante ao desenvolver plugins que referenciam arquivos externos.

Cada versão instalada é um diretório separado no cache. Quando você atualiza ou desinstala um plugin, o diretório de versão anterior é marcado como órfão e removido automaticamente 7 dias depois. O período de carência permite que sessões Claude Code concorrentes que já carregaram a versão antiga continuem funcionando sem erros.

As ferramentas Glob e Grep de Claude pulam diretórios de versão órfã durante buscas, então resultados de arquivo não incluem código de plugin desatualizado.

### Limitações de travessia de caminho

Plugins instalados não podem referenciar arquivos fora de seu diretório. Caminhos que atravessam fora da raiz do plugin (como `../shared-utils`) não funcionarão após a instalação porque esses arquivos externos não são copiados para o cache.

### Compartilhar arquivos dentro de um marketplace com symlinks

Se seu plugin precisa compartilhar arquivos com outras partes do mesmo marketplace, você pode criar links simbólicos dentro de seu diretório de plugin. Como um symlink é tratado quando o plugin é copiado para o cache depende de onde seu alvo é resolvido:

* **Dentro do próprio diretório do plugin:** o symlink é preservado como um symlink relativo no cache, então ele continua resolvendo para o alvo copiado em tempo de execução.
* **Em outro lugar dentro do mesmo marketplace:** o symlink é desreferenciado. O conteúdo do alvo é copiado para o cache em seu lugar. Isso permite que o diretório `skills/` de um meta-plugin seja vinculado a skills definidas por outros plugins no marketplace.
* **Fora do marketplace:** o symlink é ignorado por segurança. Isso impede que plugins puxem arquivos arbitrários do host, como caminhos do sistema, para o cache.

Para plugins instalados com `--plugin-dir` ou de um caminho local, apenas symlinks que são resolvidos dentro do próprio diretório do plugin são preservados. Todos os outros são ignorados.

O seguinte comando cria um link de dentro de um plugin do marketplace para uma skill compartilhada definida por um plugin irmão. No Windows, use `mklink /D` de um Prompt de Comando elevado ou ative o Modo de Desenvolvedor:

```bash theme={null}
ln -s ../../shared-plugin/skills/foo ./skills/foo
```

Isso fornece flexibilidade enquanto mantém os benefícios de segurança do sistema de cache.

***

## Estrutura de diretório de plugin

### Layout de plugin padrão

Um plugin completo segue esta estrutura:

```text theme={null}
enterprise-plugin/
├── .claude-plugin/           # Diretório de metadados (opcional)
│   └── plugin.json             # manifesto de plugin
├── skills/                   # Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── commands/                 # Skills como arquivos .md planos
│   ├── status.md
│   └── logs.md
├── agents/                   # Definições de subagent
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── output-styles/            # Definições de estilo de saída
│   └── terse.md
├── themes/                   # Definições de tema de cor
│   └── dracula.json
├── monitors/                 # Configurações de monitor de fundo
│   └── monitors.json
├── hooks/                    # Configurações de hook
│   ├── hooks.json           # Configuração de hook principal
│   └── security-hooks.json  # Hooks adicionais
├── bin/                      # Executáveis de plugin adicionados a PATH
│   └── my-tool               # Invocável como comando bare na ferramenta Bash
├── settings.json            # Configurações padrão para o plugin
├── .mcp.json                # Definições de servidor MCP
├── .lsp.json                # Configurações de servidor LSP
├── scripts/                 # Scripts de hook e utilitário
│   ├── security-scan.sh
│   ├── format-code.py
│   └── deploy.js
├── LICENSE                  # Arquivo de licença
└── CHANGELOG.md             # Histórico de versão
```

<Warning>
  O diretório `.claude-plugin/` contém o arquivo `plugin.json`. Todos os outros diretórios (commands/, agents/, skills/, output-styles/, themes/, monitors/, hooks/) devem estar na raiz do plugin, não dentro de `.claude-plugin/`.
</Warning>

Um arquivo `CLAUDE.md` na raiz do plugin não é carregado como contexto do projeto. Os plugins contribuem contexto através de skills, agents e hooks em vez de CLAUDE.md. Para enviar instruções que sejam carregadas no contexto do Claude, coloque-as em uma [skill](#skills).

### Referência de localizações de arquivo

| Componente        | Localização padrão           | Propósito                                                                                                                                                                                      |
| :---------------- | :--------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Manifesto**     | `.claude-plugin/plugin.json` | Metadados e configuração de plugin (opcional)                                                                                                                                                  |
| **Skills**        | `skills/`                    | Skills com estrutura `<name>/SKILL.md`                                                                                                                                                         |
| **Commands**      | `commands/`                  | Skills como arquivos Markdown planos. Use `skills/` para novos plugins                                                                                                                         |
| **Agents**        | `agents/`                    | Arquivos Markdown de Subagent                                                                                                                                                                  |
| **Output styles** | `output-styles/`             | Definições de estilo de saída                                                                                                                                                                  |
| **Themes**        | `themes/`                    | Definições de tema de cor                                                                                                                                                                      |
| **Hooks**         | `hooks/hooks.json`           | Configuração de hook                                                                                                                                                                           |
| **MCP servers**   | `.mcp.json`                  | Definições de servidor MCP                                                                                                                                                                     |
| **LSP servers**   | `.lsp.json`                  | Configurações de servidor de linguagem                                                                                                                                                         |
| **Monitors**      | `monitors/monitors.json`     | Configurações de monitor de fundo                                                                                                                                                              |
| **Executáveis**   | `bin/`                       | Executáveis adicionados ao `PATH` da ferramenta Bash. Arquivos aqui são invocáveis como comandos bare em qualquer chamada de ferramenta Bash enquanto o plugin está habilitado                 |
| **Configurações** | `settings.json`              | Configuração padrão aplicada quando o plugin é habilitado. Atualmente apenas as chaves [`agent`](/pt/sub-agents) e [`subagentStatusLine`](/pt/statusline#subagent-status-lines) são suportadas |

***

## Referência de comandos CLI

Claude Code fornece comandos CLI para gerenciamento de plugin não interativo, útil para scripting e automação.

### plugin install

Instale um plugin dos marketplaces disponíveis.

```bash theme={null}
claude plugin install <plugin> [options]
```

**Argumentos:**

* `<plugin>`: Nome do plugin ou `plugin-name@marketplace-name` para um marketplace específico

**Opções:**

| Opção                 | Descrição                                           | Padrão |
| :-------------------- | :-------------------------------------------------- | :----- |
| `-s, --scope <scope>` | Escopo de instalação: `user`, `project`, ou `local` | `user` |
| `-h, --help`          | Exibir ajuda para comando                           |        |

O escopo determina qual arquivo de configurações o plugin instalado é adicionado. Por exemplo, `--scope project` escreve em `enabledPlugins` em .claude/settings.json, tornando o plugin disponível para todos que clonam o repositório do projeto.

**Exemplos:**

```bash theme={null}
# Instalar em escopo de usuário (padrão)
claude plugin install formatter@my-marketplace

# Instalar em escopo de projeto (compartilhado com equipe)
claude plugin install formatter@my-marketplace --scope project

# Instalar em escopo local (gitignored)
claude plugin install formatter@my-marketplace --scope local
```

### plugin uninstall

Remova um plugin instalado.

```bash theme={null}
claude plugin uninstall <plugin> [options]
```

**Argumentos:**

* `<plugin>`: Nome do plugin ou `plugin-name@marketplace-name`

**Opções:**

| Opção                 | Descrição                                                                                                      | Padrão |
| :-------------------- | :------------------------------------------------------------------------------------------------------------- | :----- |
| `-s, --scope <scope>` | Desinstalar do escopo: `user`, `project`, ou `local`                                                           | `user` |
| `--keep-data`         | Preservar o [diretório de dados persistente](#persistent-data-directory) do plugin                             |        |
| `--prune`             | Também remover dependências auto-instaladas que nenhum outro plugin requer. Veja [plugin prune](#plugin-prune) |        |
| `-y, --yes`           | Pular o prompt de confirmação `--prune`. Necessário quando stdin não é um TTY                                  |        |
| `-h, --help`          | Exibir ajuda para comando                                                                                      |        |

**Aliases:** `remove`, `rm`

Por padrão, desinstalar do último escopo restante também deleta o diretório `${CLAUDE_PLUGIN_DATA}` do plugin. Use `--keep-data` para preservá-lo, por exemplo ao reinstalar após testar uma nova versão.

### plugin prune

Remova dependências de plugin auto-instaladas que não são mais necessárias por nenhum plugin instalado. Dependências que Claude Code puxou para satisfazer o campo [`dependencies`](/pt/plugin-dependencies) de outro plugin são removidas; plugins que você instalou diretamente nunca são tocados.

```bash theme={null}
claude plugin prune [options]
```

**Opções:**

| Opção                 | Descrição                                                           | Padrão |
| :-------------------- | :------------------------------------------------------------------ | :----- |
| `-s, --scope <scope>` | Limpar no escopo: `user`, `project`, ou `local`                     | `user` |
| `--dry-run`           | Listar o que seria removido sem remover nada                        |        |
| `-y, --yes`           | Pular o prompt de confirmação. Necessário quando stdin não é um TTY |        |
| `-h, --help`          | Exibir ajuda para comando                                           |        |

**Aliases:** `autoremove`

O comando lista dependências órfãs e pede confirmação antes de removê-las. Para remover um plugin e limpar suas dependências em uma etapa, execute `claude plugin uninstall <plugin> --prune`.

<Note>
  `claude plugin prune` requer Claude Code v2.1.121 ou posterior.
</Note>

### plugin enable

Habilite um plugin desabilitado.

```bash theme={null}
claude plugin enable <plugin> [options]
```

**Argumentos:**

* `<plugin>`: Nome do plugin ou `plugin-name@marketplace-name`

**Opções:**

| Opção                 | Descrição                                            | Padrão |
| :-------------------- | :--------------------------------------------------- | :----- |
| `-s, --scope <scope>` | Escopo para habilitar: `user`, `project`, ou `local` | `user` |
| `-h, --help`          | Exibir ajuda para comando                            |        |

### plugin disable

Desabilite um plugin sem desinstalá-lo.

```bash theme={null}
claude plugin disable <plugin> [options]
```

**Argumentos:**

* `<plugin>`: Nome do plugin ou `plugin-name@marketplace-name`

**Opções:**

| Opção                 | Descrição                                              | Padrão |
| :-------------------- | :----------------------------------------------------- | :----- |
| `-s, --scope <scope>` | Escopo para desabilitar: `user`, `project`, ou `local` | `user` |
| `-h, --help`          | Exibir ajuda para comando                              |        |

### plugin update

Atualize um plugin para a versão mais recente.

```bash theme={null}
claude plugin update <plugin> [options]
```

**Argumentos:**

* `<plugin>`: Nome do plugin ou `plugin-name@marketplace-name`

**Opções:**

| Opção                 | Descrição                                                       | Padrão |
| :-------------------- | :-------------------------------------------------------------- | :----- |
| `-s, --scope <scope>` | Escopo para atualizar: `user`, `project`, `local`, ou `managed` | `user` |
| `-h, --help`          | Exibir ajuda para comando                                       |        |

***

### plugin list

Liste plugins instalados com sua versão, marketplace de origem e status de habilitação.

```bash theme={null}
claude plugin list [options]
```

**Opções:**

| Opção         | Descrição                                                    | Padrão |
| :------------ | :----------------------------------------------------------- | :----- |
| `--json`      | Saída como JSON                                              |        |
| `--available` | Incluir plugins disponíveis de marketplaces. Requer `--json` |        |
| `-h, --help`  | Exibir ajuda para comando                                    |        |

### plugin details

Mostre o inventário de componentes de um plugin e o custo de token projetado. A saída lista todos os componentes que o plugin contribui, agrupados como Skills (skills e comandos), Agents, Hooks e servidores MCP, juntamente com uma estimativa de quantos tokens ele adiciona a cada sessão.

```bash theme={null}
claude plugin details <name>
```

**Argumentos:**

* `<name>`: Nome do plugin ou `plugin-name@marketplace-name`

**Opções:**

| Opção        | Descrição                 | Padrão |
| :----------- | :------------------------ | :----- |
| `-h, --help` | Exibir ajuda para comando |        |

A saída mostra dois valores de custo para cada componente:

* **Always-on:** tokens adicionados a cada sessão pelo texto de listagem do plugin, como descrições de skill, descrições de agent e nomes de comando, independentemente de qualquer componente disparar.
* **On-invoke:** tokens que um componente custa quando dispara. Mostrado por componente, não como total do plugin, porque uma sessão típica invoca apenas um subconjunto de componentes.

Este exemplo mostra como a saída se parece para um plugin com duas skills:

```
security-guidance 1.2.0
  Real-time security analysis for Claude Code sessions
  Source: security-guidance@claude-code-marketplace

Component inventory
  Skills (2)  scan-dependencies, review-changes
  Agents (0)
  Hooks (1)  (harness-only — no model context cost)
  MCP servers (0)

Projected token cost
  Always-on:   ~180 tok   added to every session

Per-component (rounded)
  component            always-on  on-invoke
  scan-dependencies        ~100      ~2400
  review-changes            ~80      ~1800

  On-invoke cost is paid each time a skill or agent fires.
  Token counts are estimates and may differ from actual usage.
```

O total always-on é calculado via API `count_tokens` para seu modelo ativo. Os números por componente são dimensionados proporcionalmente a partir desse total. Se a API estiver inacessível, o comando volta para uma estimativa baseada em caracteres.

### plugin tag

Crie uma tag git de lançamento para o plugin no diretório atual. Execute de dentro da pasta do plugin. Veja [Tag plugin releases](/pt/plugin-dependencies#tag-plugin-releases-for-version-resolution).

```bash theme={null}
claude plugin tag [options]
```

**Opções:**

| Opção         | Descrição                                                                 | Padrão |
| :------------ | :------------------------------------------------------------------------ | :----- |
| `--push`      | Enviar a tag para o remoto após criá-la                                   |        |
| `--dry-run`   | Imprimir o que seria marcado sem criar a tag                              |        |
| `-f, --force` | Criar a tag mesmo que a árvore de trabalho esteja suja ou a tag já exista |        |
| `-h, --help`  | Exibir ajuda para comando                                                 |        |

***

## Ferramentas de depuração e desenvolvimento

### Comandos de depuração

Use `claude --debug` para ver detalhes de carregamento de plugin:

Isso mostra:

* Quais plugins estão sendo carregados
* Quaisquer erros em manifestos de plugin
* Registro de skill, agent e hook
* Inicialização de servidor MCP

### Problemas comuns

| Problema                            | Causa                               | Solução                                                                                                                                                                      |
| :---------------------------------- | :---------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Plugin não carregando               | `plugin.json` inválido              | Execute `claude plugin validate` ou `/plugin validate` para verificar `plugin.json`, frontmatter de skill/agent/comando e `hooks/hooks.json` para erros de sintaxe e esquema |
| Skills não aparecendo               | Estrutura de diretório errada       | Garanta `skills/` ou `commands/` na raiz do plugin, não dentro de `.claude-plugin/`                                                                                          |
| Hooks não disparando                | Script não executável               | Execute `chmod +x script.sh`                                                                                                                                                 |
| Servidor MCP falha                  | `${CLAUDE_PLUGIN_ROOT}` ausente     | Use variável para todos os caminhos de plugin                                                                                                                                |
| Erros de caminho                    | Caminhos absolutos usados           | Todos os caminhos devem ser relativos e começar com `./`                                                                                                                     |
| LSP `Executable not found in $PATH` | Servidor de linguagem não instalado | Instale o binário (ex: `npm install -g typescript-language-server typescript`)                                                                                               |

### Exemplos de mensagens de erro

**Erros de validação de manifesto**:

* `Invalid JSON syntax: Unexpected token } in JSON at position 142`: verificar vírgulas ausentes, vírgulas extras ou strings não citadas
* `Plugin has an invalid manifest file at .claude-plugin/plugin.json. Validation errors: name: Required`: um campo obrigatório está faltando
* `Plugin has a corrupt manifest file at .claude-plugin/plugin.json. JSON parse error: ...`: erro de sintaxe JSON

**Erros de carregamento de plugin**:

* `Warning: No commands found in plugin my-plugin custom directory: ./cmds. Expected .md files or SKILL.md in subdirectories.`: caminho de comando existe mas não contém arquivos de comando válidos
* `Plugin directory not found at path: ./plugins/my-plugin. Check that the marketplace entry has the correct path.`: o caminho `source` em marketplace.json aponta para um diretório inexistente
* `Plugin my-plugin has conflicting manifests: both plugin.json and marketplace entry specify components.`: remover definições de componentes duplicadas ou remover `strict: false` na entrada do marketplace

### Solução de problemas de hook

**Script de hook não executando**:

1. Verificar se o script é executável: `chmod +x ./scripts/your-script.sh`
2. Verificar a linha shebang: Primeira linha deve ser `#!/bin/bash` ou `#!/usr/bin/env bash`
3. Verificar se o caminho usa `${CLAUDE_PLUGIN_ROOT}`: `"command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/your-script.sh"`
4. Testar o script manualmente: `./scripts/your-script.sh`

**Hook não disparando em eventos esperados**:

1. Verificar se o nome do evento está correto (sensível a maiúsculas): `PostToolUse`, não `postToolUse`
2. Verificar se o padrão de matcher corresponde às suas ferramentas: `"matcher": "Write|Edit"` para operações de arquivo
3. Confirmar se o tipo de hook é válido: `command`, `http`, `mcp_tool`, `prompt`, ou `agent`

### Solução de problemas de servidor MCP

**Servidor não iniciando**:

1. Verificar se o comando existe e é executável
2. Verificar se todos os caminhos usam variável `${CLAUDE_PLUGIN_ROOT}`
3. Verificar os logs do servidor MCP: `claude --debug` mostra erros de inicialização
4. Testar o servidor manualmente fora do Claude Code

**Ferramentas do servidor não aparecendo**:

1. Garantir que o servidor está adequadamente configurado em `.mcp.json` ou `plugin.json`
2. Verificar se o servidor implementa o protocolo MCP corretamente
3. Verificar timeouts de conexão na saída de depuração

### Erros de estrutura de diretório

**Sintomas**: Plugin carrega mas componentes (skills, agents, hooks) estão faltando.

**Estrutura correta**: Componentes devem estar na raiz do plugin, não dentro de `.claude-plugin/`. Apenas `plugin.json` pertence em `.claude-plugin/`.

```text theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json      ← Apenas manifesto aqui
├── commands/            ← No nível raiz
├── agents/              ← No nível raiz
└── hooks/               ← No nível raiz
```

Se seus componentes estão dentro de `.claude-plugin/`, mova-os para a raiz do plugin.

**Checklist de depuração**:

1. Executar `claude --debug` e procurar por mensagens "loading plugin"
2. Verificar se cada diretório de componente está listado na saída de depuração
3. Verificar se as permissões de arquivo permitem ler os arquivos de plugin

***

## Referência de distribuição e versionamento

### Gerenciamento de versão

Claude Code usa a versão do plugin como a chave de cache que determina se uma atualização está disponível. Quando você executa `/plugin update` ou a atualização automática é acionada, Claude Code calcula a versão atual e ignora a atualização se ela corresponder ao que já está instalado.

A versão é resolvida a partir do primeiro destes que está definido:

1. O campo `version` no `plugin.json` do plugin
2. O campo `version` na entrada do marketplace do plugin em `marketplace.json`
3. O SHA do commit git do plugin, para fontes `github`, `url`, `git-subdir` e relative-path em um marketplace hospedado em git
4. `unknown`, para fontes `npm` ou diretórios locais não dentro de um repositório git

Isso oferece duas maneiras de versionar um plugin:

| Abordagem                | Como                                                                    | Comportamento de atualização                                                                                                                                                            | Melhor para                                            |
| :----------------------- | :---------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------- |
| **Versão explícita**     | Defina `"version": "2.1.0"` em `plugin.json`                            | Os usuários recebem atualizações apenas quando você aumenta este campo. Enviar novos commits sem aumentá-lo não tem efeito, e `/plugin update` relata "já está na versão mais recente". | Plugins publicados com ciclos de lançamento estáveis   |
| **Versão SHA do commit** | Omita `version` tanto de `plugin.json` quanto da entrada do marketplace | Os usuários recebem atualizações em cada novo commit para a fonte git do plugin                                                                                                         | Plugins internos ou de equipe em desenvolvimento ativo |

<Warning>
  Se você definir `version` em `plugin.json`, você deve aumentá-lo toda vez que quiser que os usuários recebam alterações. Enviar novos commits sozinho não é suficiente, porque Claude Code vê a mesma string de versão e mantém a cópia em cache. Se você está iterando rapidamente, deixe `version` indefinido para que o SHA do commit git seja usado em vez disso.
</Warning>

Se você usar versões explícitas, siga [versionamento semântico](https://semver.org) (`MAJOR.MINOR.PATCH`): aumente MAJOR para mudanças de quebra, MINOR para novos recursos, PATCH para correções de bugs. Documente as alterações em um `CHANGELOG.md`.

***

## Veja também

* [Plugins](/pt/plugins) - Tutoriais e uso prático
* [Marketplaces de plugins](/pt/plugin-marketplaces) - Criando e gerenciando marketplaces
* [Skills](/pt/skills) - Detalhes de desenvolvimento de skill
* [Subagents](/pt/sub-agents) - Configuração e capacidades de agent
* [Hooks](/pt/hooks) - Manipulação de eventos e automação
* [MCP](/pt/mcp) - Integração de ferramenta externa
* [Configurações](/pt/settings) - Opções de configuração para plugins
