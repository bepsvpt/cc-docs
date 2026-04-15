> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Criar e distribuir um marketplace de plugins

> Crie e hospede marketplaces de plugins para distribuir extensões Claude Code em equipes e comunidades.

Um **marketplace de plugins** é um catálogo que permite distribuir plugins para outros. Os marketplaces fornecem descoberta centralizada, rastreamento de versão, atualizações automáticas e suporte para múltiplos tipos de fonte (repositórios git, caminhos locais e muito mais). Este guia mostra como criar seu próprio marketplace para compartilhar plugins com sua equipe ou comunidade.

Procurando instalar plugins de um marketplace existente? Veja [Descobrir e instalar plugins pré-construídos](/pt/discover-plugins).

## Visão geral

Criar e distribuir um marketplace envolve:

1. **Criar plugins**: construir um ou mais plugins com commands, agents, hooks, MCP servers ou LSP servers. Este guia assume que você já tem plugins para distribuir; veja [Criar plugins](/pt/plugins) para detalhes sobre como criá-los.
2. **Criar um arquivo de marketplace**: definir um `marketplace.json` que lista seus plugins e onde encontrá-los (veja [Criar o arquivo de marketplace](#create-the-marketplace-file)).
3. **Hospedar o marketplace**: fazer push para GitHub, GitLab ou outro host git (veja [Hospedar e distribuir marketplaces](#host-and-distribute-marketplaces)).
4. **Compartilhar com usuários**: usuários adicionam seu marketplace com `/plugin marketplace add` e instalam plugins individuais (veja [Descobrir e instalar plugins](/pt/discover-plugins)).

Depois que seu marketplace estiver ativo, você pode atualizá-lo fazendo push de alterações para seu repositório. Os usuários atualizam sua cópia local com `/plugin marketplace update`.

## Passo a passo: criar um marketplace local

Este exemplo cria um marketplace com um plugin: uma skill `/quality-review` para revisões de código. Você criará a estrutura de diretórios, adicionará uma skill, criará o manifesto do plugin e o catálogo do marketplace, depois instalará e testará.

<Steps>
  <Step title="Criar a estrutura de diretórios">
    ```bash theme={null}
    mkdir -p my-marketplace/.claude-plugin
    mkdir -p my-marketplace/plugins/quality-review-plugin/.claude-plugin
    mkdir -p my-marketplace/plugins/quality-review-plugin/skills/quality-review
    ```
  </Step>

  <Step title="Criar a skill">
    Crie um arquivo `SKILL.md` que define o que a skill `/quality-review` faz.

    ```markdown my-marketplace/plugins/quality-review-plugin/skills/quality-review/SKILL.md theme={null}
    ---
    description: Revisar código para bugs, segurança e desempenho
    disable-model-invocation: true
    ---

    Revise o código que selecionei ou as alterações recentes para:
    - Possíveis bugs ou casos extremos
    - Preocupações de segurança
    - Problemas de desempenho
    - Melhorias de legibilidade

    Seja conciso e acionável.
    ```
  </Step>

  <Step title="Criar o manifesto do plugin">
    Crie um arquivo `plugin.json` que descreve o plugin. O manifesto vai no diretório `.claude-plugin/`.

    ```json my-marketplace/plugins/quality-review-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "quality-review-plugin",
      "description": "Adiciona uma skill /quality-review para revisões rápidas de código",
      "version": "1.0.0"
    }
    ```
  </Step>

  <Step title="Criar o arquivo de marketplace">
    Crie o catálogo de marketplace que lista seu plugin.

    ```json my-marketplace/.claude-plugin/marketplace.json theme={null}
    {
      "name": "my-plugins",
      "owner": {
        "name": "Seu Nome"
      },
      "plugins": [
        {
          "name": "quality-review-plugin",
          "source": "./plugins/quality-review-plugin",
          "description": "Adiciona uma skill /quality-review para revisões rápidas de código"
        }
      ]
    }
    ```
  </Step>

  <Step title="Adicionar e instalar">
    Adicione o marketplace e instale o plugin.

    ```shell theme={null}
    /plugin marketplace add ./my-marketplace
    /plugin install quality-review-plugin@my-plugins
    ```
  </Step>

  <Step title="Experimentar">
    Selecione algum código em seu editor e execute seu novo comando.

    ```shell theme={null}
    /quality-review
    ```
  </Step>
</Steps>

Para saber mais sobre o que os plugins podem fazer, incluindo hooks, agents, MCP servers e LSP servers, veja [Plugins](/pt/plugins).

<Note>
  **Como os plugins são instalados**: Quando os usuários instalam um plugin, Claude Code copia o diretório do plugin para um local de cache. Isso significa que os plugins não podem referenciar arquivos fora de seu diretório usando caminhos como `../shared-utils`, porque esses arquivos não serão copiados.

  Se você precisar compartilhar arquivos entre plugins, use symlinks (que são seguidos durante a cópia). Veja [Plugin caching and file resolution](/pt/plugins-reference#plugin-caching-and-file-resolution) para detalhes.
</Note>

## Criar o arquivo de marketplace

Crie `.claude-plugin/marketplace.json` na raiz do seu repositório. Este arquivo define o nome do seu marketplace, informações do proprietário e uma lista de plugins com suas fontes.

Cada entrada de plugin precisa no mínimo de um `name` e `source` (onde buscá-lo). Veja o [esquema completo](#marketplace-schema) abaixo para todos os campos disponíveis.

```json theme={null}
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@example.com"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "Formatação automática de código ao salvar",
      "version": "2.1.0",
      "author": {
        "name": "DevTools Team"
      }
    },
    {
      "name": "deployment-tools",
      "source": {
        "source": "github",
        "repo": "company/deploy-plugin"
      },
      "description": "Ferramentas de automação de implantação"
    }
  ]
}
```

## Esquema de marketplace

### Campos obrigatórios

| Campo     | Tipo   | Descrição                                                                                                                                                                 | Exemplo        |
| :-------- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------- |
| `name`    | string | Identificador de marketplace (kebab-case, sem espaços). Isso é público: os usuários o veem ao instalar plugins (por exemplo, `/plugin install my-tool@your-marketplace`). | `"acme-tools"` |
| `owner`   | object | Informações do mantenedor do marketplace ([veja campos abaixo](#owner-fields))                                                                                            |                |
| `plugins` | array  | Lista de plugins disponíveis                                                                                                                                              | Veja abaixo    |

<Note>
  **Nomes reservados**: Os seguintes nomes de marketplace são reservados para uso oficial da Anthropic e não podem ser usados por marketplaces de terceiros: `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `knowledge-work-plugins`, `life-sciences`. Nomes que imitam marketplaces oficiais (como `official-claude-plugins` ou `anthropic-tools-v2`) também são bloqueados.
</Note>

### Campos do proprietário

| Campo   | Tipo   | Obrigatório | Descrição                      |
| :------ | :----- | :---------- | :----------------------------- |
| `name`  | string | Sim         | Nome do mantenedor ou equipe   |
| `email` | string | Não         | Email de contato do mantenedor |

### Metadados opcionais

| Campo                  | Tipo   | Descrição                                                                                                                                                                             |
| :--------------------- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `metadata.description` | string | Breve descrição do marketplace                                                                                                                                                        |
| `metadata.version`     | string | Versão do marketplace                                                                                                                                                                 |
| `metadata.pluginRoot`  | string | Diretório base adicionado aos caminhos de fonte de plugin relativos (por exemplo, `"./plugins"` permite escrever `"source": "formatter"` em vez de `"source": "./plugins/formatter"`) |

## Entradas de plugin

Cada entrada de plugin no array `plugins` descreve um plugin e onde encontrá-lo. Você pode incluir qualquer campo do [esquema de manifesto de plugin](/pt/plugins-reference#plugin-manifest-schema) (como `description`, `version`, `author`, `commands`, `hooks`, etc.), além destes campos específicos do marketplace: `source`, `category`, `tags` e `strict`.

### Campos obrigatórios

| Campo    | Tipo           | Descrição                                                                                                                                                 |
| :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`   | string         | Identificador de plugin (kebab-case, sem espaços). Isso é público: os usuários o veem ao instalar (por exemplo, `/plugin install my-plugin@marketplace`). |
| `source` | string\|object | Onde buscar o plugin (veja [Fontes de plugin](#plugin-sources) abaixo)                                                                                    |

### Campos de plugin opcionais

**Campos de metadados padrão:**

| Campo         | Tipo    | Descrição                                                                                                                        |
| :------------ | :------ | :------------------------------------------------------------------------------------------------------------------------------- |
| `description` | string  | Breve descrição do plugin                                                                                                        |
| `version`     | string  | Versão do plugin                                                                                                                 |
| `author`      | object  | Informações do autor do plugin (`name` obrigatório, `email` opcional)                                                            |
| `homepage`    | string  | URL da página inicial ou documentação do plugin                                                                                  |
| `repository`  | string  | URL do repositório de código-fonte                                                                                               |
| `license`     | string  | Identificador de licença SPDX (por exemplo, MIT, Apache-2.0)                                                                     |
| `keywords`    | array   | Tags para descoberta e categorização de plugins                                                                                  |
| `category`    | string  | Categoria do plugin para organização                                                                                             |
| `tags`        | array   | Tags para pesquisabilidade                                                                                                       |
| `strict`      | boolean | Controla se `plugin.json` é a autoridade para definições de componentes (padrão: true). Veja [Modo strict](#strict-mode) abaixo. |

**Campos de configuração de componentes:**

| Campo        | Tipo           | Descrição                                                            |
| :----------- | :------------- | :------------------------------------------------------------------- |
| `commands`   | string\|array  | Caminhos personalizados para arquivos ou diretórios de command       |
| `agents`     | string\|array  | Caminhos personalizados para arquivos de agent                       |
| `hooks`      | string\|object | Configuração de hooks personalizada ou caminho para arquivo de hooks |
| `mcpServers` | string\|object | Configurações de MCP server ou caminho para config de MCP            |
| `lspServers` | string\|object | Configurações de LSP server ou caminho para config de LSP            |

## Fontes de plugin

As fontes de plugin informam ao Claude Code onde buscar cada plugin individual listado em seu marketplace. Elas são definidas no campo `source` de cada entrada de plugin em `marketplace.json`.

Depois que um plugin é clonado ou copiado para a máquina local, ele é copiado para o cache de plugin versionado local em `~/.claude/plugins/cache`.

| Fonte            | Tipo                                    | Campos                             | Notas                                                                                                        |
| ---------------- | --------------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Caminho relativo | `string` (por exemplo, `"./my-plugin"`) | nenhum                             | Diretório local dentro do repositório de marketplace. Deve começar com `./`                                  |
| `github`         | object                                  | `repo`, `ref?`, `sha?`             |                                                                                                              |
| `url`            | object                                  | `url`, `ref?`, `sha?`              | Fonte de URL Git                                                                                             |
| `git-subdir`     | object                                  | `url`, `path`, `ref?`, `sha?`      | Subdiretório dentro de um repositório git. Clona esparsamente para minimizar largura de banda para monorepos |
| `npm`            | object                                  | `package`, `version?`, `registry?` | Instalado via `npm install`                                                                                  |

<Note>
  **Fontes de marketplace vs fontes de plugin**: Estes são conceitos diferentes que controlam coisas diferentes.

  * **Fonte de marketplace** — onde buscar o próprio catálogo `marketplace.json`. Definido quando os usuários executam `/plugin marketplace add` ou em configurações `extraKnownMarketplaces`. Suporta `ref` (branch/tag) mas não `sha`.
  * **Fonte de plugin** — onde buscar um plugin individual listado no marketplace. Definido no campo `source` de cada entrada de plugin dentro de `marketplace.json`. Suporta tanto `ref` (branch/tag) quanto `sha` (commit exato).

  Por exemplo, um marketplace hospedado em `acme-corp/plugin-catalog` (fonte de marketplace) pode listar um plugin buscado de `acme-corp/code-formatter` (fonte de plugin). A fonte de marketplace e a fonte de plugin apontam para repositórios diferentes e são fixadas independentemente.
</Note>

### Caminhos relativos

Para plugins no mesmo repositório, use um caminho começando com `./`:

```json theme={null}
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

Os caminhos são resolvidos relativos à raiz do marketplace, que é o diretório contendo `.claude-plugin/`. No exemplo acima, `./plugins/my-plugin` aponta para `<repo>/plugins/my-plugin`, mesmo que `marketplace.json` viva em `<repo>/.claude-plugin/marketplace.json`. Não use `../` para sair de `.claude-plugin/`.

<Note>
  Caminhos relativos funcionam apenas quando os usuários adicionam seu marketplace via Git (GitHub, GitLab ou URL git). Se os usuários adicionarem seu marketplace via URL direta para o arquivo `marketplace.json`, caminhos relativos não serão resolvidos corretamente. Para distribuição baseada em URL, use fontes GitHub, npm ou URL git. Veja [Troubleshooting](#plugins-with-relative-paths-fail-in-url-based-marketplaces) para detalhes.
</Note>

### Repositórios GitHub

```json theme={null}
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```

Você pode fixar a um branch, tag ou commit específico:

```json theme={null}
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| Campo  | Tipo   | Descrição                                                                           |
| :----- | :----- | :---------------------------------------------------------------------------------- |
| `repo` | string | Obrigatório. Repositório GitHub no formato `owner/repo`                             |
| `ref`  | string | Opcional. Branch ou tag Git (padrão é o branch padrão do repositório)               |
| `sha`  | string | Opcional. SHA de commit git completo de 40 caracteres para fixar a uma versão exata |

### Repositórios Git

```json theme={null}
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

Você pode fixar a um branch, tag ou commit específico:

```json theme={null}
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git",
    "ref": "main",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| Campo | Tipo   | Descrição                                                                                                                                                           |
| :---- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `url` | string | Obrigatório. URL completa do repositório git (`https://` ou `git@`). O sufixo `.git` é opcional, então URLs do Azure DevOps e AWS CodeCommit sem o sufixo funcionam |
| `ref` | string | Opcional. Branch ou tag Git (padrão é o branch padrão do repositório)                                                                                               |
| `sha` | string | Opcional. SHA de commit git completo de 40 caracteres para fixar a uma versão exata                                                                                 |

### Subdiretórios Git

Use `git-subdir` para apontar para um plugin que vive dentro de um subdiretório de um repositório git. Claude Code usa um clone parcial e esparso para buscar apenas o subdiretório, minimizando largura de banda para grandes monorepos.

```json theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin"
  }
}
```

Você pode fixar a um branch, tag ou commit específico:

```json theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

O campo `url` também aceita atalho GitHub (`owner/repo`) ou URLs SSH (`git@github.com:owner/repo.git`).

| Campo  | Tipo   | Descrição                                                                                                           |
| :----- | :----- | :------------------------------------------------------------------------------------------------------------------ |
| `url`  | string | Obrigatório. URL do repositório Git, atalho GitHub `owner/repo` ou URL SSH                                          |
| `path` | string | Obrigatório. Caminho do subdiretório dentro do repositório contendo o plugin (por exemplo, `"tools/claude-plugin"`) |
| `ref`  | string | Opcional. Branch ou tag Git (padrão é o branch padrão do repositório)                                               |
| `sha`  | string | Opcional. SHA de commit git completo de 40 caracteres para fixar a uma versão exata                                 |

### Pacotes npm

Plugins distribuídos como pacotes npm são instalados usando `npm install`. Isso funciona com qualquer pacote no registro npm público ou um registro privado que sua equipe hospeda.

```json theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin"
  }
}
```

Para fixar a uma versão específica, adicione o campo `version`:

```json theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "2.1.0"
  }
}
```

Para instalar de um registro privado ou interno, adicione o campo `registry`:

```json theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "^2.0.0",
    "registry": "https://npm.example.com"
  }
}
```

| Campo      | Tipo   | Descrição                                                                                               |
| :--------- | :----- | :------------------------------------------------------------------------------------------------------ |
| `package`  | string | Obrigatório. Nome do pacote ou pacote com escopo (por exemplo, `@org/plugin`)                           |
| `version`  | string | Opcional. Versão ou intervalo de versão (por exemplo, `2.1.0`, `^2.0.0`, `~1.5.0`)                      |
| `registry` | string | Opcional. URL de registro npm personalizado. Padrão é o registro npm do sistema (tipicamente npmjs.org) |

### Entradas de plugin avançadas

Este exemplo mostra uma entrada de plugin usando muitos dos campos opcionais, incluindo caminhos personalizados para commands, agents, hooks e MCP servers:

```json theme={null}
{
  "name": "enterprise-tools",
  "source": {
    "source": "github",
    "repo": "company/enterprise-plugin"
  },
  "description": "Ferramentas de automação de fluxo de trabalho empresarial",
  "version": "2.1.0",
  "author": {
    "name": "Enterprise Team",
    "email": "enterprise@example.com"
  },
  "homepage": "https://docs.example.com/plugins/enterprise-tools",
  "repository": "https://github.com/company/enterprise-plugin",
  "license": "MIT",
  "keywords": ["enterprise", "workflow", "automation"],
  "category": "productivity",
  "commands": [
    "./commands/core/",
    "./commands/enterprise/",
    "./commands/experimental/preview.md"
  ],
  "agents": ["./agents/security-reviewer.md", "./agents/compliance-checker.md"],
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  },
  "mcpServers": {
    "enterprise-db": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  },
  "strict": false
}
```

Coisas importantes a notar:

* **`commands` e `agents`**: Você pode especificar múltiplos diretórios ou arquivos individuais. Os caminhos são relativos à raiz do plugin.
* **`${CLAUDE_PLUGIN_ROOT}`**: use esta variável em hooks e configurações de MCP server para referenciar arquivos dentro do diretório de instalação do plugin. Isso é necessário porque os plugins são copiados para um local de cache quando instalados. Para dependências ou estado que devem sobreviver a atualizações de plugin, use [`${CLAUDE_PLUGIN_DATA}`](/pt/plugins-reference#persistent-data-directory) em vez disso.
* **`strict: false`**: Como isso está definido como false, o plugin não precisa de seu próprio `plugin.json`. A entrada de marketplace define tudo. Veja [Modo strict](#strict-mode) abaixo.

### Modo strict

O campo `strict` controla se `plugin.json` é a autoridade para definições de componentes (commands, agents, hooks, skills, MCP servers, output styles).

| Valor           | Comportamento                                                                                                                                                      |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `true` (padrão) | `plugin.json` é a autoridade. A entrada de marketplace pode complementá-lo com componentes adicionais, e ambas as fontes são mescladas.                            |
| `false`         | A entrada de marketplace é a definição completa. Se o plugin também tem um `plugin.json` que declara componentes, isso é um conflito e o plugin falha ao carregar. |

**Quando usar cada modo:**

* **`strict: true`**: o plugin tem seu próprio `plugin.json` e gerencia seus próprios componentes. A entrada de marketplace pode adicionar commands ou hooks extras no topo. Este é o padrão e funciona para a maioria dos plugins.
* **`strict: false`**: o operador do marketplace quer controle total. O repositório do plugin fornece arquivos brutos, e a entrada de marketplace define quais desses arquivos são expostos como commands, agents, hooks, etc. Útil quando o marketplace reestrutura ou curada os componentes de um plugin de forma diferente do que o autor do plugin pretendia.

## Hospedar e distribuir marketplaces

### Hospedar no GitHub (recomendado)

GitHub fornece o método de distribuição mais fácil:

1. **Criar um repositório**: Configure um novo repositório para seu marketplace
2. **Adicionar arquivo de marketplace**: Crie `.claude-plugin/marketplace.json` com suas definições de plugin
3. **Compartilhar com equipes**: Os usuários adicionam seu marketplace com `/plugin marketplace add owner/repo`

**Benefícios**: Controle de versão integrado, rastreamento de problemas e recursos de colaboração em equipe.

### Hospedar em outros serviços git

Qualquer serviço de hospedagem git funciona, como GitLab, Bitbucket e servidores auto-hospedados. Os usuários adicionam com a URL completa do repositório:

```shell theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git
```

### Repositórios privados

Claude Code suporta instalar plugins de repositórios privados. Para instalação manual e atualizações, Claude Code usa seus ajudantes de credencial git existentes. Se `git clone` funciona para um repositório privado em seu terminal, funciona em Claude Code também. Os ajudantes de credencial comuns incluem `gh auth login` para GitHub, Keychain do macOS e `git-credential-store`.

As atualizações automáticas em segundo plano são executadas na inicialização sem ajudantes de credencial, já que prompts interativos bloqueariam Claude Code de iniciar. Para habilitar atualizações automáticas para marketplaces privados, defina o token de autenticação apropriado em seu ambiente:

| Provedor  | Variáveis de ambiente        | Notas                                          |
| :-------- | :--------------------------- | :--------------------------------------------- |
| GitHub    | `GITHUB_TOKEN` ou `GH_TOKEN` | Token de acesso pessoal ou token de GitHub App |
| GitLab    | `GITLAB_TOKEN` ou `GL_TOKEN` | Token de acesso pessoal ou token de projeto    |
| Bitbucket | `BITBUCKET_TOKEN`            | Senha de app ou token de acesso ao repositório |

Defina o token em sua configuração de shell (por exemplo, `.bashrc`, `.zshrc`) ou passe-o ao executar Claude Code:

```bash theme={null}
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

<Note>
  Para ambientes CI/CD, configure o token como uma variável de ambiente secreta. GitHub Actions fornece automaticamente `GITHUB_TOKEN` para repositórios na mesma organização.
</Note>

### Testar localmente antes da distribuição

Teste seu marketplace localmente antes de compartilhar:

```shell theme={null}
/plugin marketplace add ./my-local-marketplace
/plugin install test-plugin@my-local-marketplace
```

Para a gama completa de comandos add (GitHub, URLs Git, caminhos locais, URLs remotas), veja [Adicionar marketplaces](/pt/discover-plugins#add-marketplaces).

### Exigir marketplaces para sua equipe

Você pode configurar seu repositório para que os membros da equipe sejam automaticamente solicitados a instalar seu marketplace quando confiarem na pasta do projeto. Adicione seu marketplace a `.claude/settings.json`:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

Você também pode especificar quais plugins devem ser habilitados por padrão:

```json theme={null}
{
  "enabledPlugins": {
    "code-formatter@company-tools": true,
    "deployment-tools@company-tools": true
  }
}
```

Para opções de configuração completas, veja [Plugin settings](/pt/settings#plugin-settings).

<Note>
  Se você usar uma fonte local `directory` ou `file` com um caminho relativo, o caminho é resolvido contra o checkout principal do seu repositório. Quando você executa Claude Code de um git worktree, o caminho ainda aponta para o checkout principal, então todos os worktrees compartilham o mesmo local de marketplace. O estado do marketplace é armazenado uma vez por usuário em `~/.claude/plugins/known_marketplaces.json`, não por projeto.
</Note>

### Pré-popular plugins para containers

Para imagens de container e ambientes CI, você pode pré-popular um diretório de plugins no tempo de construção para que Claude Code inicie com marketplaces e plugins já disponíveis, sem clonar nada em tempo de execução. Defina a variável de ambiente `CLAUDE_CODE_PLUGIN_SEED_DIR` para apontar para este diretório.

Para colocar em camadas múltiplos diretórios seed, separe caminhos com `:` em Unix ou `;` no Windows. Claude Code procura cada diretório em ordem, e o primeiro seed que contém um determinado marketplace ou cache de plugin vence.

O diretório seed espelha a estrutura de `~/.claude/plugins`:

```
$CLAUDE_CODE_PLUGIN_SEED_DIR/
  known_marketplaces.json
  marketplaces/<name>/...
  cache/<marketplace>/<plugin>/<version>/...
```

A forma mais simples de construir um diretório seed é executar Claude Code uma vez durante a construção da imagem, instalar os plugins que você precisa, depois copiar o diretório `~/.claude/plugins` resultante em sua imagem e apontar `CLAUDE_CODE_PLUGIN_SEED_DIR` para ele.

Na inicialização, Claude Code registra marketplaces encontrados no `known_marketplaces.json` do seed na configuração primária, e usa caches de plugin encontrados sob `cache/` no local sem re-clonar. Isso funciona tanto em modo interativo quanto em modo não-interativo com a flag `-p`.

Detalhes de comportamento:

* **Somente leitura**: o diretório seed nunca é escrito. As atualizações automáticas são desabilitadas para marketplaces seed já que git pull falharia em um sistema de arquivos somente leitura.
* **Entradas seed têm precedência**: marketplaces declarados no seed sobrescrevem qualquer entrada correspondente na configuração do usuário em cada inicialização. Para optar por não usar um plugin seed, use `/plugin disable` em vez de remover o marketplace.
* **Resolução de caminho**: Claude Code localiza conteúdo de marketplace sondando `$CLAUDE_CODE_PLUGIN_SEED_DIR/marketplaces/<name>/` em tempo de execução, não confiando em caminhos armazenados dentro do JSON do seed. Isso significa que o seed funciona corretamente mesmo quando montado em um caminho diferente de onde foi construído.
* **Compõe com configurações**: se `extraKnownMarketplaces` ou `enabledPlugins` declaram um marketplace que já existe no seed, Claude Code usa a cópia do seed em vez de clonar.

### Restrições de marketplace gerenciado

Para organizações que exigem controle rigoroso sobre fontes de plugin, administradores podem restringir quais marketplaces de plugin os usuários podem adicionar usando a configuração [`strictKnownMarketplaces`](/pt/settings#strictknownmarketplaces) em configurações gerenciadas.

Quando `strictKnownMarketplaces` é configurado em configurações gerenciadas, o comportamento de restrição depende do valor:

| Valor               | Comportamento                                                                                     |
| ------------------- | ------------------------------------------------------------------------------------------------- |
| Indefinido (padrão) | Sem restrições. Os usuários podem adicionar qualquer marketplace                                  |
| Array vazio `[]`    | Bloqueio completo. Os usuários não podem adicionar novos marketplaces                             |
| Lista de fontes     | Os usuários podem apenas adicionar marketplaces que correspondem exatamente à lista de permissões |

#### Configurações comuns

Desabilitar todas as adições de marketplace:

```json theme={null}
{
  "strictKnownMarketplaces": []
}
```

Permitir apenas marketplaces específicos:

```json theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    }
  ]
}
```

Permitir todos os marketplaces de um servidor git interno usando correspondência de padrão regex no host. Esta é a abordagem recomendada para [GitHub Enterprise Server](/pt/github-enterprise-server#plugin-marketplaces-on-ghes) ou instâncias GitLab auto-hospedadas:

```json theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

Permitir marketplaces baseados em sistema de arquivos de um diretório específico usando correspondência de padrão regex no caminho:

```json theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "pathPattern",
      "pathPattern": "^/opt/approved/"
    }
  ]
}
```

Use `".*"` como `pathPattern` para permitir qualquer caminho de sistema de arquivos enquanto ainda controla fontes de rede com `hostPattern`.

<Note>
  `strictKnownMarketplaces` restringe o que os usuários podem adicionar, mas não registra marketplaces por conta própria. Para tornar marketplaces permitidos disponíveis automaticamente sem usuários executarem `/plugin marketplace add`, combine com [`extraKnownMarketplaces`](/pt/settings#extraknownmarketplaces) no mesmo `managed-settings.json`. Veja [Usando ambos juntos](/pt/settings#strictknownmarketplaces).
</Note>

#### Como as restrições funcionam

As restrições são validadas no início do processo de instalação de plugin, antes de qualquer solicitação de rede ou operação de sistema de arquivos ocorrer. Isso previne tentativas de acesso não autorizado a marketplace.

A lista de permissões usa correspondência exata para a maioria dos tipos de fonte. Para um marketplace ser permitido, todos os campos especificados devem corresponder exatamente:

* Para fontes GitHub: `repo` é obrigatório, e `ref` ou `path` também devem corresponder se especificados na lista de permissões
* Para fontes de URL: a URL completa deve corresponder exatamente
* Para fontes `hostPattern`: o host do marketplace é correspondido contra o padrão regex
* Para fontes `pathPattern`: o caminho do sistema de arquivos do marketplace é correspondido contra o padrão regex

Como `strictKnownMarketplaces` é definido em [configurações gerenciadas](/pt/settings#settings-files), configurações individuais de usuários e projetos não podem substituir essas restrições.

Para detalhes de configuração completos incluindo todos os tipos de fonte suportados e comparação com `extraKnownMarketplaces`, veja a [referência strictKnownMarketplaces](/pt/settings#strictknownmarketplaces).

### Resolução de versão e canais de lançamento

As versões de plugin determinam caminhos de cache e detecção de atualização. Você pode especificar a versão no manifesto do plugin (`plugin.json`) ou na entrada de marketplace (`marketplace.json`).

<Warning>
  Quando possível, evite definir a versão em ambos os lugares. O manifesto do plugin sempre vence silenciosamente, o que pode fazer com que a versão do marketplace seja ignorada. Para plugins com caminho relativo, defina a versão na entrada de marketplace. Para todas as outras fontes de plugin, defina-a no manifesto do plugin.
</Warning>

#### Configurar canais de lançamento

Para suportar canais de lançamento "stable" e "latest" para seus plugins, você pode configurar dois marketplaces que apontam para diferentes refs ou SHAs do mesmo repositório. Você pode então atribuir os dois marketplaces a diferentes grupos de usuários através de [configurações gerenciadas](/pt/settings#settings-files).

<Warning>
  O `plugin.json` do plugin deve declarar uma `version` diferente em cada ref ou commit fixado. Se dois refs ou commits tiverem a mesma versão de manifesto, Claude Code os trata como idênticos e pula a atualização.
</Warning>

##### Exemplo

```json theme={null}
{
  "name": "stable-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": {
        "source": "github",
        "repo": "acme-corp/code-formatter",
        "ref": "stable"
      }
    }
  ]
}
```

```json theme={null}
{
  "name": "latest-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": {
        "source": "github",
        "repo": "acme-corp/code-formatter",
        "ref": "latest"
      }
    }
  ]
}
```

##### Atribuir canais a grupos de usuários

Atribua cada marketplace ao grupo de usuários apropriado através de configurações gerenciadas. Por exemplo, o grupo stable recebe:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "stable-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/stable-tools"
      }
    }
  }
}
```

O grupo early-access recebe `latest-tools` em vez disso:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "latest-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/latest-tools"
      }
    }
  }
}
```

## Validação e testes

Teste seu marketplace antes de compartilhar.

Valide a sintaxe JSON do seu marketplace:

```bash theme={null}
claude plugin validate .
```

Ou de dentro de Claude Code:

```shell theme={null}
/plugin validate .
```

Adicione o marketplace para testes:

```shell theme={null}
/plugin marketplace add ./path/to/marketplace
```

Instale um plugin de teste para verificar se tudo funciona:

```shell theme={null}
/plugin install test-plugin@marketplace-name
```

Para fluxos de trabalho completos de testes de plugin, veja [Testar seus plugins localmente](/pt/plugins#test-your-plugins-locally). Para troubleshooting técnico, veja [Plugins reference](/pt/plugins-reference).

## Troubleshooting

### Marketplace não carregando

**Sintomas**: Não consegue adicionar marketplace ou ver plugins dele

**Soluções**:

* Verifique se a URL do marketplace é acessível
* Verifique se `.claude-plugin/marketplace.json` existe no caminho especificado
* Garanta que a sintaxe JSON é válida e o frontmatter está bem formado usando `claude plugin validate` ou `/plugin validate`
* Para repositórios privados, confirme que você tem permissões de acesso

### Erros de validação de marketplace

Execute `claude plugin validate .` ou `/plugin validate .` do seu diretório de marketplace para verificar problemas. O validador verifica `plugin.json`, frontmatter de skill/agent/command e `hooks/hooks.json` para erros de sintaxe e esquema. Erros comuns:

| Erro                                              | Causa                                                  | Solução                                                                                               |
| :------------------------------------------------ | :----------------------------------------------------- | :---------------------------------------------------------------------------------------------------- |
| `File not found: .claude-plugin/marketplace.json` | Manifesto ausente                                      | Crie `.claude-plugin/marketplace.json` com campos obrigatórios                                        |
| `Invalid JSON syntax: Unexpected token...`        | Erro de sintaxe JSON em marketplace.json               | Verifique vírgulas ausentes, vírgulas extras ou strings não citadas                                   |
| `Duplicate plugin name "x" found in marketplace`  | Dois plugins compartilham o mesmo nome                 | Dê a cada plugin um valor `name` único                                                                |
| `plugins[0].source: Path contains ".."`           | Caminho de fonte contém `..`                           | Use caminhos relativos à raiz do marketplace sem `..`. Veja [Caminhos relativos](#relative-paths)     |
| `YAML frontmatter failed to parse: ...`           | YAML inválido em um arquivo de skill, agent ou command | Corrija a sintaxe YAML no bloco frontmatter. Em tempo de execução este arquivo carrega sem metadados. |
| `Invalid JSON syntax: ...` (hooks.json)           | `hooks/hooks.json` malformado                          | Corrija a sintaxe JSON. Um `hooks/hooks.json` malformado previne o plugin inteiro de carregar.        |

**Avisos** (não bloqueadores):

* `Marketplace has no plugins defined`: adicione pelo menos um plugin ao array `plugins`
* `No marketplace description provided`: adicione `metadata.description` para ajudar os usuários a entender seu marketplace
* `Plugin name "x" is not kebab-case`: o nome do plugin contém letras maiúsculas, espaços ou caracteres especiais. Renomeie para apenas letras minúsculas, dígitos e hífens (por exemplo, `my-plugin`). Claude Code aceita outras formas, mas a sincronização de marketplace do Claude.ai as rejeita.

### Falhas de instalação de plugin

**Sintomas**: Marketplace aparece mas a instalação do plugin falha

**Soluções**:

* Verifique se as URLs de fonte do plugin são acessíveis
* Verifique se os diretórios de plugin contêm arquivos obrigatórios
* Para fontes GitHub, garanta que repositórios são públicos ou você tem acesso
* Teste fontes de plugin manualmente clonando/baixando

### Falha de autenticação de repositório privado

**Sintomas**: Erros de autenticação ao instalar plugins de repositórios privados

**Soluções**:

Para instalação manual e atualizações:

* Verifique se você está autenticado com seu provedor git (por exemplo, execute `gh auth status` para GitHub)
* Verifique se seu ajudante de credencial está configurado corretamente: `git config --global credential.helper`
* Tente clonar o repositório manualmente para verificar se suas credenciais funcionam

Para atualizações automáticas em segundo plano:

* Defina o token apropriado em seu ambiente: `echo $GITHUB_TOKEN`
* Verifique se o token tem as permissões obrigatórias (acesso de leitura ao repositório)
* Para GitHub, garanta que o token tem o escopo `repo` para repositórios privados
* Para GitLab, garanta que o token tem pelo menos escopo `read_repository`
* Verifique se o token não expirou

### Atualizações de marketplace falham em ambientes offline

**Sintomas**: `git pull` do marketplace falha e Claude Code limpa o cache existente, causando plugins ficarem indisponíveis.

**Causa**: Por padrão, quando um `git pull` falha, Claude Code remove o clone obsoleto e tenta re-clonar. Em ambientes offline ou airgapped, re-clonar falha da mesma forma, deixando o diretório de marketplace vazio.

**Solução**: Defina `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1` para manter o cache existente quando o pull falhar em vez de limpá-lo:

```bash theme={null}
export CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1
```

Com esta variável definida, Claude Code retém o clone obsoleto do marketplace em falha de `git pull` e continua usando o último estado conhecido como bom. Para implantações totalmente offline onde o repositório nunca será alcançável, use [`CLAUDE_CODE_PLUGIN_SEED_DIR`](#pre-populate-plugins-for-containers) para pré-popular o diretório de plugins no tempo de construção em vez disso.

### Operações Git expiram

**Sintomas**: Instalação de plugin ou atualizações de marketplace falham com um erro de timeout como "Git clone timed out after 120s" ou "Git pull timed out after 120s".

**Causa**: Claude Code usa um timeout de 120 segundos para todas as operações git, incluindo clonagem de repositórios de plugin e puxar atualizações de marketplace. Repositórios grandes ou conexões de rede lentas podem exceder este limite.

**Solução**: Aumente o timeout usando a variável de ambiente `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`. O valor está em milissegundos:

```bash theme={null}
export CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=300000  # 5 minutos
```

### Plugins com caminhos relativos falham em marketplaces baseados em URL

**Sintomas**: Adicionou um marketplace via URL (como `https://example.com/marketplace.json`), mas plugins com fontes de caminho relativo como `"./plugins/my-plugin"` falham ao instalar com erros "path not found".

**Causa**: Marketplaces baseados em URL apenas baixam o próprio arquivo `marketplace.json`. Eles não baixam arquivos de plugin do servidor. Caminhos relativos na entrada de marketplace referenciam arquivos no servidor remoto que não foram baixados.

**Soluções**:

* **Use fontes externas**: Altere entradas de plugin para usar fontes GitHub, npm ou URL git em vez de caminhos relativos:
  ```json theme={null}
  { "name": "my-plugin", "source": { "source": "github", "repo": "owner/repo" } }
  ```
* **Use um marketplace baseado em Git**: Hospede seu marketplace em um repositório Git e adicione-o com a URL git. Marketplaces baseados em Git clonam o repositório inteiro, tornando caminhos relativos funcionarem corretamente.

### Arquivos não encontrados após instalação

**Sintomas**: Plugin instala mas referências a arquivos falham, especialmente arquivos fora do diretório do plugin

**Causa**: Plugins são copiados para um diretório de cache em vez de serem usados no local. Caminhos que referenciam arquivos fora do diretório do plugin (como `../shared-utils`) não funcionarão porque esses arquivos não são copiados.

**Soluções**: Veja [Plugin caching and file resolution](/pt/plugins-reference#plugin-caching-and-file-resolution) para workarounds incluindo symlinks e reestruturação de diretório.

Para ferramentas de debugging adicionais e problemas comuns, veja [Debugging and development tools](/pt/plugins-reference#debugging-and-development-tools).

## Veja também

* [Descobrir e instalar plugins pré-construídos](/pt/discover-plugins) - Instalando plugins de marketplaces existentes
* [Plugins](/pt/plugins) - Criando seus próprios plugins
* [Plugins reference](/pt/plugins-reference) - Especificações técnicas completas e esquemas
* [Plugin settings](/pt/settings#plugin-settings) - Opções de configuração de plugin
* [strictKnownMarketplaces reference](/pt/settings#strictknownmarketplaces) - Restrições de marketplace gerenciado
