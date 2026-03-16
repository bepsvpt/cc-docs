> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Referência de plugins

> Referência técnica completa para o sistema de plugins do Claude Code, incluindo esquemas, comandos CLI e especificações de componentes.

<Tip>
  Procurando instalar plugins? Veja [Descobrir e instalar plugins](/pt/discover-plugins). Para criar plugins, veja [Plugins](/pt/plugins). Para distribuir plugins, veja [Marketplaces de plugins](/pt/plugin-marketplaces).
</Tip>

Esta referência fornece especificações técnicas completas para o sistema de plugins do Claude Code, incluindo esquemas de componentes, comandos CLI e ferramentas de desenvolvimento.

Um **plugin** é um diretório independente de componentes que estende o Claude Code com funcionalidade personalizada. Os componentes do plugin incluem skills, agents, hooks, MCP servers e LSP servers.

## Referência de componentes de plugin

### Skills

Os plugins adicionam skills ao Claude Code, criando atalhos `/name` que você ou Claude podem invocar.

**Localização**: Diretório `skills/` ou `commands/` na raiz do plugin

**Formato de arquivo**: Skills são diretórios com `SKILL.md`; comandos são arquivos markdown simples

**Estrutura de skill**:

```text  theme={null}
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

```markdown  theme={null}
---
name: agent-name
description: No que este agent se especializa e quando Claude deve invocá-lo
---

Prompt de sistema detalhado para o agent descrevendo seu papel, expertise e comportamento.
```

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

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

**Eventos disponíveis**:

* `PreToolUse`: Antes de Claude usar qualquer ferramenta
* `PostToolUse`: Depois que Claude usa com sucesso qualquer ferramenta
* `PostToolUseFailure`: Depois que a execução da ferramenta Claude falha
* `PermissionRequest`: Quando um diálogo de permissão é mostrado
* `UserPromptSubmit`: Quando o usuário envia um prompt
* `Notification`: Quando Claude Code envia notificações
* `Stop`: Quando Claude tenta parar
* `SubagentStart`: Quando um subagent é iniciado
* `SubagentStop`: Quando um subagent tenta parar
* `SessionStart`: No início das sessões
* `SessionEnd`: No final das sessões
* `TeammateIdle`: Quando um colega de equipe de agent está prestes a ficar ocioso
* `TaskCompleted`: Quando uma tarefa está sendo marcada como concluída
* `PreCompact`: Antes do histórico de conversa ser compactado

**Tipos de hook**:

* `command`: Executar comandos shell ou scripts
* `prompt`: Avaliar um prompt com um LLM (usa placeholder `$ARGUMENTS` para contexto)
* `agent`: Executar um verificador agentic com ferramentas para tarefas de verificação complexas

### MCP servers

Os plugins podem agrupar servidores Model Context Protocol (MCP) para conectar Claude Code com ferramentas e serviços externos.

**Localização**: `.mcp.json` na raiz do plugin, ou inline em plugin.json

**Formato**: Configuração padrão de servidor MCP

**Configuração de servidor MCP**:

```json  theme={null}
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

```json  theme={null}
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

```json  theme={null}
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

| Plugin           | Servidor de linguagem      | Comando de instalação                                                                        |
| :--------------- | :------------------------- | :------------------------------------------------------------------------------------------- |
| `pyright-lsp`    | Pyright (Python)           | `pip install pyright` ou `npm install -g pyright`                                            |
| `typescript-lsp` | TypeScript Language Server | `npm install -g typescript-language-server typescript`                                       |
| `rust-lsp`       | rust-analyzer              | [Veja instalação de rust-analyzer](https://rust-analyzer.github.io/manual.html#installation) |

Instale o servidor de linguagem primeiro, depois instale o plugin do marketplace.

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

```json  theme={null}
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
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json"
}
```

### Campos obrigatórios

Se você incluir um manifesto, `name` é o único campo obrigatório.

| Campo  | Tipo   | Descrição                                     | Exemplo              |
| :----- | :----- | :-------------------------------------------- | :------------------- |
| `name` | string | Identificador único (kebab-case, sem espaços) | `"deployment-tools"` |

Este nome é usado para namespacing de componentes. Por exemplo, na UI, o agent `agent-creator` para o plugin com nome `plugin-dev` aparecerá como `plugin-dev:agent-creator`.

### Campos de metadados

| Campo         | Tipo   | Descrição                                                                                                                            | Exemplo                                            |
| :------------ | :----- | :----------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------- |
| `version`     | string | Versão semântica. Se também definida na entrada do marketplace, `plugin.json` tem prioridade. Você só precisa defini-la em um lugar. | `"2.1.0"`                                          |
| `description` | string | Explicação breve do propósito do plugin                                                                                              | `"Deployment automation tools"`                    |
| `author`      | object | Informações do autor                                                                                                                 | `{"name": "Dev Team", "email": "dev@company.com"}` |
| `homepage`    | string | URL de documentação                                                                                                                  | `"https://docs.example.com"`                       |
| `repository`  | string | URL do código-fonte                                                                                                                  | `"https://github.com/user/plugin"`                 |
| `license`     | string | Identificador de licença                                                                                                             | `"MIT"`, `"Apache-2.0"`                            |
| `keywords`    | array  | Tags de descoberta                                                                                                                   | `["deployment", "ci-cd"]`                          |

### Campos de caminho de componente

| Campo          | Tipo                  | Descrição                                                                                                                                                                    | Exemplo                                |
| :------------- | :-------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------- |
| `commands`     | string\|array         | Arquivos/diretórios de comando adicionais                                                                                                                                    | `"./custom/cmd.md"` ou `["./cmd1.md"]` |
| `agents`       | string\|array         | Arquivos de agent adicionais                                                                                                                                                 | `"./custom/agents/reviewer.md"`        |
| `skills`       | string\|array         | Diretórios de skill adicionais                                                                                                                                               | `"./custom/skills/"`                   |
| `hooks`        | string\|array\|object | Caminhos de configuração de hooks ou configuração inline                                                                                                                     | `"./my-extra-hooks.json"`              |
| `mcpServers`   | string\|array\|object | Caminhos de configuração MCP ou configuração inline                                                                                                                          | `"./my-extra-mcp-config.json"`         |
| `outputStyles` | string\|array         | Arquivos/diretórios de estilo de saída adicionais                                                                                                                            | `"./styles/"`                          |
| `lspServers`   | string\|array\|object | Configurações [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) para inteligência de código (ir para definição, encontrar referências, etc.) | `"./.lsp.json"`                        |

### Regras de comportamento de caminho

**Importante**: Caminhos personalizados complementam diretórios padrão - eles não os substituem.

* Se `commands/` existe, é carregado além de caminhos de comando personalizados
* Todos os caminhos devem ser relativos à raiz do plugin e começar com `./`
* Comandos de caminhos personalizados usam as mesmas regras de nomenclatura e namespacing
* Múltiplos caminhos podem ser especificados como arrays para flexibilidade

**Exemplos de caminho**:

```json  theme={null}
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

**`${CLAUDE_PLUGIN_ROOT}`**: Contém o caminho absoluto para seu diretório de plugin. Use isso em hooks, servidores MCP e scripts para garantir caminhos corretos independentemente da localização de instalação.

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

***

## Cache de plugin e resolução de arquivo

Os plugins são especificados de uma de duas maneiras:

* Através de `claude --plugin-dir`, pela duração de uma sessão.
* Através de um marketplace, instalado para sessões futuras.

Para fins de segurança e verificação, Claude Code copia plugins do *marketplace* para o **cache de plugin** local do usuário (`~/.claude/plugins/cache`) em vez de usá-los no local. Entender esse comportamento é importante ao desenvolver plugins que referenciam arquivos externos.

### Limitações de travessia de caminho

Plugins instalados não podem referenciar arquivos fora de seu diretório. Caminhos que atravessam fora da raiz do plugin (como `../shared-utils`) não funcionarão após a instalação porque esses arquivos externos não são copiados para o cache.

### Trabalhando com dependências externas

Se seu plugin precisa acessar arquivos fora de seu diretório, você pode criar links simbólicos para arquivos externos dentro de seu diretório de plugin. Links simbólicos são honrados durante o processo de cópia:

```bash  theme={null}
# Dentro de seu diretório de plugin
ln -s /path/to/shared-utils ./shared-utils
```

O conteúdo vinculado será copiado para o cache de plugin. Isso fornece flexibilidade enquanto mantém os benefícios de segurança do sistema de cache.

***

## Estrutura de diretório de plugin

### Layout de plugin padrão

Um plugin completo segue esta estrutura:

```text  theme={null}
enterprise-plugin/
├── .claude-plugin/           # Diretório de metadados (opcional)
│   └── plugin.json             # manifesto de plugin
├── commands/                 # Localização de comando padrão
│   ├── status.md
│   └── logs.md
├── agents/                   # Localização de agent padrão
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── skills/                   # Skills de Agent
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── hooks/                    # Configurações de hook
│   ├── hooks.json           # Configuração de hook principal
│   └── security-hooks.json  # Hooks adicionais
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
  O diretório `.claude-plugin/` contém o arquivo `plugin.json`. Todos os outros diretórios (commands/, agents/, skills/, hooks/) devem estar na raiz do plugin, não dentro de `.claude-plugin/`.
</Warning>

### Referência de localizações de arquivo

| Componente         | Localização padrão           | Propósito                                                                                                                           |
| :----------------- | :--------------------------- | :---------------------------------------------------------------------------------------------------------------------------------- |
| **Manifesto**      | `.claude-plugin/plugin.json` | Metadados e configuração de plugin (opcional)                                                                                       |
| **Comandos**       | `commands/`                  | Arquivos Markdown de Skill (legado; use `skills/` para novas skills)                                                                |
| **Agents**         | `agents/`                    | Arquivos Markdown de Subagent                                                                                                       |
| **Skills**         | `skills/`                    | Skills com estrutura `<name>/SKILL.md`                                                                                              |
| **Hooks**          | `hooks/hooks.json`           | Configuração de hook                                                                                                                |
| **Servidores MCP** | `.mcp.json`                  | Definições de servidor MCP                                                                                                          |
| **Servidores LSP** | `.lsp.json`                  | Configurações de servidor de linguagem                                                                                              |
| **Configurações**  | `settings.json`              | Configuração padrão aplicada quando o plugin é habilitado. Atualmente apenas configurações [`agent`](/pt/sub-agents) são suportadas |

***

## Referência de comandos CLI

Claude Code fornece comandos CLI para gerenciamento de plugin não interativo, útil para scripting e automação.

### plugin install

Instale um plugin dos marketplaces disponíveis.

```bash  theme={null}
claude plugin install <plugin> [options]
```

**Argumentos:**

* `<plugin>`: Nome do plugin ou `plugin-name@marketplace-name` para um marketplace específico

**Opções:**

| Opção                 | Descrição                                           | Padrão |
| :-------------------- | :-------------------------------------------------- | :----- |
| `-s, --scope <scope>` | Escopo de instalação: `user`, `project`, ou `local` | `user` |
| `-h, --help`          | Exibir ajuda para comando                           |        |

O escopo determina qual arquivo de configurações o plugin instalado é adicionado. Por exemplo, --scope project escreve em `enabledPlugins` em .claude/settings.json, tornando o plugin disponível para todos que clonam o repositório do projeto.

**Exemplos:**

```bash  theme={null}
# Instalar em escopo de usuário (padrão)
claude plugin install formatter@my-marketplace

# Instalar em escopo de projeto (compartilhado com equipe)
claude plugin install formatter@my-marketplace --scope project

# Instalar em escopo local (gitignored)
claude plugin install formatter@my-marketplace --scope local
```

### plugin uninstall

Remova um plugin instalado.

```bash  theme={null}
claude plugin uninstall <plugin> [options]
```

**Argumentos:**

* `<plugin>`: Nome do plugin ou `plugin-name@marketplace-name`

**Opções:**

| Opção                 | Descrição                                            | Padrão |
| :-------------------- | :--------------------------------------------------- | :----- |
| `-s, --scope <scope>` | Desinstalar do escopo: `user`, `project`, ou `local` | `user` |
| `-h, --help`          | Exibir ajuda para comando                            |        |

**Aliases:** `remove`, `rm`

### plugin enable

Habilite um plugin desabilitado.

```bash  theme={null}
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

```bash  theme={null}
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

```bash  theme={null}
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

## Ferramentas de depuração e desenvolvimento

### Comandos de depuração

Use `claude --debug` (ou `/debug` dentro do TUI) para ver detalhes de carregamento de plugin:

Isso mostra:

* Quais plugins estão sendo carregados
* Quaisquer erros em manifestos de plugin
* Registro de comando, agent e hook
* Inicialização de servidor MCP

### Problemas comuns

| Problema                            | Causa                               | Solução                                                                         |
| :---------------------------------- | :---------------------------------- | :------------------------------------------------------------------------------ |
| Plugin não carregando               | `plugin.json` inválido              | Validar sintaxe JSON com `claude plugin validate` ou `/plugin validate`         |
| Comandos não aparecendo             | Estrutura de diretório errada       | Garantir `commands/` na raiz, não em `.claude-plugin/`                          |
| Hooks não disparando                | Script não executável               | Executar `chmod +x script.sh`                                                   |
| Servidor MCP falha                  | `${CLAUDE_PLUGIN_ROOT}` ausente     | Usar variável para todos os caminhos de plugin                                  |
| Erros de caminho                    | Caminhos absolutos usados           | Todos os caminhos devem ser relativos e começar com `./`                        |
| LSP `Executable not found in $PATH` | Servidor de linguagem não instalado | Instalar o binário (ex: `npm install -g typescript-language-server typescript`) |

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
3. Verificar se o caminho usa `${CLAUDE_PLUGIN_ROOT}`: `"command": "${CLAUDE_PLUGIN_ROOT}/scripts/your-script.sh"`
4. Testar o script manualmente: `./scripts/your-script.sh`

**Hook não disparando em eventos esperados**:

1. Verificar se o nome do evento está correto (sensível a maiúsculas): `PostToolUse`, não `postToolUse`
2. Verificar se o padrão de matcher corresponde às suas ferramentas: `"matcher": "Write|Edit"` para operações de arquivo
3. Confirmar se o tipo de hook é válido: `command`, `prompt`, ou `agent`

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

**Sintomas**: Plugin carrega mas componentes (comandos, agents, hooks) estão faltando.

**Estrutura correta**: Componentes devem estar na raiz do plugin, não dentro de `.claude-plugin/`. Apenas `plugin.json` pertence em `.claude-plugin/`.

```text  theme={null}
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

Siga versionamento semântico para lançamentos de plugin:

```json  theme={null}
{
  "name": "my-plugin",
  "version": "2.1.0"
}
```

**Formato de versão**: `MAJOR.MINOR.PATCH`

* **MAJOR**: Mudanças de quebra (mudanças de API incompatíveis)
* **MINOR**: Novos recursos (adições compatíveis com versões anteriores)
* **PATCH**: Correções de bugs (correções compatíveis com versões anteriores)

**Melhores práticas**:

* Começar em `1.0.0` para seu primeiro lançamento estável
* Atualizar a versão em `plugin.json` antes de distribuir mudanças
* Documentar mudanças em um arquivo `CHANGELOG.md`
* Usar versões de pré-lançamento como `2.0.0-beta.1` para testes

<Warning>
  Claude Code usa a versão para determinar se deve atualizar seu plugin. Se você alterar o código do seu plugin mas não aumentar a versão em `plugin.json`, os usuários existentes do seu plugin não verão suas mudanças devido ao cache.

  Se seu plugin está dentro de um diretório [marketplace](/pt/plugin-marketplaces), você pode gerenciar a versão através de `marketplace.json` em vez disso e omitir o campo `version` de `plugin.json`.
</Warning>

***

## Veja também

* [Plugins](/pt/plugins) - Tutoriais e uso prático
* [Marketplaces de plugins](/pt/plugin-marketplaces) - Criando e gerenciando marketplaces
* [Skills](/pt/skills) - Detalhes de desenvolvimento de skill
* [Subagents](/pt/sub-agents) - Configuração e capacidades de agent
* [Hooks](/pt/hooks) - Manipulação de eventos e automação
* [MCP](/pt/mcp) - Integração de ferramenta externa
* [Configurações](/pt/settings) - Opções de configuração para plugins
