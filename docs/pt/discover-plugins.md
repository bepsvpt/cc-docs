> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Descubra e instale plugins pré-construídos através de marketplaces

> Encontre e instale plugins de marketplaces para estender Claude Code com novos comandos, agentes e capacidades.

Plugins estendem Claude Code com skills, agentes, hooks e MCP servers. Marketplaces de plugins são catálogos que ajudam você a descobrir e instalar essas extensões sem construí-las você mesmo.

Procurando criar e distribuir seu próprio marketplace? Veja [Criar e distribuir um marketplace de plugins](/pt/plugin-marketplaces).

## Como os marketplaces funcionam

Um marketplace é um catálogo de plugins que alguém criou e compartilhou. Usar um marketplace é um processo de duas etapas:

<Steps>
  <Step title="Adicione o marketplace">
    Isso registra o catálogo com Claude Code para que você possa navegar o que está disponível. Nenhum plugin é instalado ainda.
  </Step>

  <Step title="Instale plugins individuais">
    Navegue pelo catálogo e instale os plugins que você deseja.
  </Step>
</Steps>

Pense nisso como adicionar uma loja de aplicativos: adicionar a loja oferece acesso para navegar sua coleção, mas você ainda escolhe quais aplicativos baixar individualmente.

## Marketplace oficial da Anthropic

O marketplace oficial da Anthropic (`claude-plugins-official`) está automaticamente disponível quando você inicia Claude Code. Execute `/plugin` e vá para a aba **Discover** para navegar o que está disponível.

Para instalar um plugin do marketplace oficial:

```shell  theme={null}
/plugin install plugin-name@claude-plugins-official
```

<Note>
  O marketplace oficial é mantido pela Anthropic. Para enviar um plugin para o marketplace oficial, use um dos formulários de envio no aplicativo:

  * **Claude.ai**: [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
  * **Console**: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

  Para distribuir plugins independentemente, [crie seu próprio marketplace](/pt/plugin-marketplaces) e compartilhe com usuários.
</Note>

O marketplace oficial inclui várias categorias de plugins:

### Code intelligence

Plugins de code intelligence habilitam a ferramenta LSP integrada do Claude Code, dando a Claude a capacidade de pular para definições, encontrar referências e ver erros de tipo imediatamente após edições. Esses plugins configuram conexões do [Language Server Protocol](https://microsoft.github.io/language-server-protocol/), a mesma tecnologia que alimenta a code intelligence do VS Code.

Esses plugins requerem que o binário do language server esteja instalado no seu sistema. Se você já tem um language server instalado, Claude pode solicitar que você instale o plugin correspondente quando abrir um projeto.

| Linguagem  | Plugin              | Binário necessário           |
| :--------- | :------------------ | :--------------------------- |
| C/C++      | `clangd-lsp`        | `clangd`                     |
| C#         | `csharp-lsp`        | `csharp-ls`                  |
| Go         | `gopls-lsp`         | `gopls`                      |
| Java       | `jdtls-lsp`         | `jdtls`                      |
| Kotlin     | `kotlin-lsp`        | `kotlin-language-server`     |
| Lua        | `lua-lsp`           | `lua-language-server`        |
| PHP        | `php-lsp`           | `intelephense`               |
| Python     | `pyright-lsp`       | `pyright-langserver`         |
| Rust       | `rust-analyzer-lsp` | `rust-analyzer`              |
| Swift      | `swift-lsp`         | `sourcekit-lsp`              |
| TypeScript | `typescript-lsp`    | `typescript-language-server` |

Você também pode [criar seu próprio plugin LSP](/pt/plugins-reference#lsp-servers) para outras linguagens.

<Note>
  Se você vir `Executable not found in $PATH` na aba Errors do `/plugin` após instalar um plugin, instale o binário necessário da tabela acima.
</Note>

#### O que Claude ganha com plugins de code intelligence

Uma vez que um plugin de code intelligence está instalado e seu binário de language server está disponível, Claude ganha duas capacidades:

* **Diagnósticos automáticos**: após cada edição de arquivo que Claude faz, o language server analisa as mudanças e relata erros e avisos automaticamente. Claude vê erros de tipo, importações faltantes e problemas de sintaxe sem precisar executar um compilador ou linter. Se Claude introduzir um erro, ele percebe e corrige o problema na mesma volta. Isso não requer configuração além de instalar o plugin. Você pode ver diagnósticos inline pressionando **Ctrl+O** quando o indicador "diagnostics found" aparecer.
* **Navegação de código**: Claude pode usar o language server para pular para definições, encontrar referências, obter informações de tipo ao passar o mouse, listar símbolos, encontrar implementações e rastrear hierarquias de chamadas. Essas operações dão a Claude navegação mais precisa do que busca baseada em grep, embora a disponibilidade possa variar por linguagem e ambiente.

Se você encontrar problemas, veja [Troubleshooting de code intelligence](#code-intelligence-issues).

### Integrações externas

Esses plugins agrupam [MCP servers](/pt/mcp) pré-configurados para que você possa conectar Claude a serviços externos sem configuração manual:

* **Controle de fonte**: `github`, `gitlab`
* **Gerenciamento de projetos**: `atlassian` (Jira/Confluence), `asana`, `linear`, `notion`
* **Design**: `figma`
* **Infraestrutura**: `vercel`, `firebase`, `supabase`
* **Comunicação**: `slack`
* **Monitoramento**: `sentry`

### Fluxos de trabalho de desenvolvimento

Plugins que adicionam comandos e agentes para tarefas comuns de desenvolvimento:

* **commit-commands**: Fluxos de trabalho de commit do Git incluindo commit, push e criação de PR
* **pr-review-toolkit**: Agentes especializados para revisar pull requests
* **agent-sdk-dev**: Ferramentas para construir com o Claude Agent SDK
* **plugin-dev**: Toolkit para criar seus próprios plugins

### Estilos de saída

Customize como Claude responde:

* **explanatory-output-style**: Insights educacionais sobre escolhas de implementação
* **learning-output-style**: Modo de aprendizado interativo para construção de skills

## Experimente: adicione o marketplace de demonstração

Anthropic também mantém um [marketplace de plugins de demonstração](https://github.com/anthropics/claude-code/tree/main/plugins) (`claude-code-plugins`) com plugins de exemplo que mostram o que é possível com o sistema de plugins. Diferentemente do marketplace oficial, você precisa adicionar este manualmente.

<Steps>
  <Step title="Adicione o marketplace">
    De dentro do Claude Code, execute o comando `plugin marketplace add` para o marketplace `anthropics/claude-code`:

    ```shell  theme={null}
    /plugin marketplace add anthropics/claude-code
    ```

    Isso baixa o catálogo do marketplace e torna seus plugins disponíveis para você.
  </Step>

  <Step title="Navegue pelos plugins disponíveis">
    Execute `/plugin` para abrir o gerenciador de plugins. Isso abre uma interface com abas com quatro abas que você pode percorrer usando **Tab** (ou **Shift+Tab** para ir para trás):

    * **Discover**: navegue pelos plugins disponíveis de todos os seus marketplaces
    * **Installed**: visualize e gerencie seus plugins instalados
    * **Marketplaces**: adicione, remova ou atualize seus marketplaces adicionados
    * **Errors**: visualize quaisquer erros de carregamento de plugins

    Vá para a aba **Discover** para ver plugins do marketplace que você acabou de adicionar.
  </Step>

  <Step title="Instale um plugin">
    Selecione um plugin para visualizar seus detalhes e escolha um escopo de instalação:

    * **User scope**: instale para você em todos os projetos
    * **Project scope**: instale para todos os colaboradores neste repositório
    * **Local scope**: instale para você neste repositório apenas

    Por exemplo, selecione **commit-commands** (um plugin que adiciona comandos de fluxo de trabalho git) e instale-o no seu escopo de usuário.

    Você também pode instalar diretamente da linha de comando:

    ```shell  theme={null}
    /plugin install commit-commands@anthropics-claude-code
    ```

    Veja [Configuration scopes](/pt/settings#configuration-scopes) para aprender mais sobre escopos.
  </Step>

  <Step title="Use seu novo plugin">
    Após instalar, execute `/reload-plugins` para ativar o plugin. Comandos de plugin são nomeados com namespace pelo nome do plugin, então **commit-commands** fornece comandos como `/commit-commands:commit`.

    Experimente fazendo uma mudança em um arquivo e executando:

    ```shell  theme={null}
    /commit-commands:commit
    ```

    Isso prepara suas mudanças, gera uma mensagem de commit e cria o commit.

    Cada plugin funciona diferentemente. Verifique a descrição do plugin na aba **Discover** ou sua página inicial para aprender quais comandos e capacidades ele fornece.
  </Step>
</Steps>

O resto deste guia cobre todas as maneiras que você pode adicionar marketplaces, instalar plugins e gerenciar sua configuração.

## Adicione marketplaces

Use o comando `/plugin marketplace add` para adicionar marketplaces de diferentes fontes.

<Tip>
  **Atalhos**: Você pode usar `/plugin market` em vez de `/plugin marketplace` e `rm` em vez de `remove`.
</Tip>

* **Repositórios GitHub**: formato `owner/repo` (por exemplo, `anthropics/claude-code`)
* **URLs Git**: qualquer URL de repositório git (GitLab, Bitbucket, auto-hospedado)
* **Caminhos locais**: diretórios ou caminhos diretos para arquivos `marketplace.json`
* **URLs remotas**: URLs diretas para arquivos `marketplace.json` hospedados

### Adicione do GitHub

Adicione um repositório GitHub que contém um arquivo `.claude-plugin/marketplace.json` usando o formato `owner/repo`—onde `owner` é o nome de usuário ou organização do GitHub e `repo` é o nome do repositório.

Por exemplo, `anthropics/claude-code` refere-se ao repositório `claude-code` de propriedade de `anthropics`:

```shell  theme={null}
/plugin marketplace add anthropics/claude-code
```

### Adicione de outros hosts Git

Adicione qualquer repositório git fornecendo a URL completa. Isso funciona com qualquer host Git, incluindo GitLab, Bitbucket e servidores auto-hospedados:

Usando HTTPS:

```shell  theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git
```

Usando SSH:

```shell  theme={null}
/plugin marketplace add git@gitlab.com:company/plugins.git
```

Para adicionar um branch ou tag específico, acrescente `#` seguido pela ref:

```shell  theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git#v1.0.0
```

### Adicione de caminhos locais

Adicione um diretório local que contém um arquivo `.claude-plugin/marketplace.json`:

```shell  theme={null}
/plugin marketplace add ./my-marketplace
```

Você também pode adicionar um caminho direto para um arquivo `marketplace.json`:

```shell  theme={null}
/plugin marketplace add ./path/to/marketplace.json
```

### Adicione de URLs remotas

Adicione um arquivo `marketplace.json` remoto via URL:

```shell  theme={null}
/plugin marketplace add https://example.com/marketplace.json
```

<Note>
  Marketplaces baseados em URL têm algumas limitações comparadas a marketplaces baseados em Git. Se você encontrar erros "path not found" ao instalar plugins, veja [Troubleshooting](/pt/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces).
</Note>

## Instale plugins

Uma vez que você adicionou marketplaces, você pode instalar plugins diretamente (instala no escopo de usuário por padrão):

```shell  theme={null}
/plugin install plugin-name@marketplace-name
```

Para escolher um [escopo de instalação](/pt/settings#configuration-scopes) diferente, use a UI interativa: execute `/plugin`, vá para a aba **Discover** e pressione **Enter** em um plugin. Você verá opções para:

* **User scope** (padrão): instale para você em todos os projetos
* **Project scope**: instale para todos os colaboradores neste repositório (adiciona a `.claude/settings.json`)
* **Local scope**: instale para você neste repositório apenas (não compartilhado com colaboradores)

Você também pode ver plugins com escopo **managed**—esses são instalados por administradores via [managed settings](/pt/settings#settings-files) e não podem ser modificados.

Execute `/plugin` e vá para a aba **Installed** para ver seus plugins agrupados por escopo.

<Warning>
  Certifique-se de confiar em um plugin antes de instalá-lo. Anthropic não controla quais MCP servers, arquivos ou outro software estão incluídos em plugins e não pode verificar que funcionam conforme pretendido. Verifique a página inicial de cada plugin para mais informações.
</Warning>

## Gerencie plugins instalados

Execute `/plugin` e vá para a aba **Installed** para visualizar, habilitar, desabilitar ou desinstalar seus plugins. Digite para filtrar a lista por nome ou descrição do plugin.

Você também pode gerenciar plugins com comandos diretos.

Desabilite um plugin sem desinstalá-lo:

```shell  theme={null}
/plugin disable plugin-name@marketplace-name
```

Reabilite um plugin desabilitado:

```shell  theme={null}
/plugin enable plugin-name@marketplace-name
```

Remova completamente um plugin:

```shell  theme={null}
/plugin uninstall plugin-name@marketplace-name
```

A opção `--scope` permite que você direcione um escopo específico com comandos CLI:

```shell  theme={null}
claude plugin install formatter@your-org --scope project
claude plugin uninstall formatter@your-org --scope project
```

### Aplique mudanças de plugin sem reiniciar

Quando você instala, habilita ou desabilita plugins durante uma sessão, execute `/reload-plugins` para ativar todas as mudanças sem reiniciar:

```shell  theme={null}
/reload-plugins
```

Claude Code recarrega todos os plugins ativos e mostra contagens para comandos recarregados, skills, agentes, hooks, MCP servers de plugin e servidores LSP de plugin.

## Gerencie marketplaces

Você pode gerenciar marketplaces através da interface interativa `/plugin` ou com comandos CLI.

### Use a interface interativa

Execute `/plugin` e vá para a aba **Marketplaces** para:

* Visualize todos os seus marketplaces adicionados com suas fontes e status
* Adicione novos marketplaces
* Atualize listagens de marketplace para buscar os plugins mais recentes
* Remova marketplaces que você não precisa mais

### Use comandos CLI

Você também pode gerenciar marketplaces com comandos diretos.

Liste todos os marketplaces configurados:

```shell  theme={null}
/plugin marketplace list
```

Atualize listagens de plugins de um marketplace:

```shell  theme={null}
/plugin marketplace update marketplace-name
```

Remova um marketplace:

```shell  theme={null}
/plugin marketplace remove marketplace-name
```

<Warning>
  Remover um marketplace desinstalará quaisquer plugins que você instalou dele.
</Warning>

### Configure atualizações automáticas

Claude Code pode atualizar automaticamente marketplaces e seus plugins instalados na inicialização. Quando a atualização automática está habilitada para um marketplace, Claude Code atualiza os dados do marketplace e atualiza plugins instalados para suas versões mais recentes. Se quaisquer plugins foram atualizados, você verá uma notificação solicitando que execute `/reload-plugins`.

Alterne a atualização automática para marketplaces individuais através da UI:

1. Execute `/plugin` para abrir o gerenciador de plugins
2. Selecione **Marketplaces**
3. Escolha um marketplace da lista
4. Selecione **Enable auto-update** ou **Disable auto-update**

Marketplaces oficiais da Anthropic têm atualização automática habilitada por padrão. Marketplaces de terceiros e de desenvolvimento local têm atualização automática desabilitada por padrão.

Para desabilitar todas as atualizações automáticas inteiramente para Claude Code e todos os plugins, defina a variável de ambiente `DISABLE_AUTOUPDATER`. Veja [Auto updates](/pt/setup#auto-updates) para detalhes.

Para manter atualizações automáticas de plugins habilitadas enquanto desabilita atualizações automáticas de Claude Code, defina `FORCE_AUTOUPDATE_PLUGINS=true` junto com `DISABLE_AUTOUPDATER`:

```shell  theme={null}
export DISABLE_AUTOUPDATER=true
export FORCE_AUTOUPDATE_PLUGINS=true
```

Isso é útil quando você quer gerenciar atualizações de Claude Code manualmente mas ainda receber atualizações automáticas de plugins.

## Configure marketplaces de equipe

Administradores de equipe podem configurar instalação automática de marketplace para projetos adicionando configuração de marketplace a `.claude/settings.json`. Quando membros da equipe confiam na pasta do repositório, Claude Code os solicita a instalar esses marketplaces e plugins.

Adicione `extraKnownMarketplaces` ao `.claude/settings.json` do seu projeto:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "my-team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

Para opções de configuração completas incluindo `extraKnownMarketplaces` e `enabledPlugins`, veja [Plugin settings](/pt/settings#plugin-settings).

## Segurança

Plugins e marketplaces são componentes altamente confiáveis que podem executar código arbitrário em sua máquina com seus privilégios de usuário. Instale apenas plugins e adicione marketplaces de fontes que você confia. Organizações podem restringir quais marketplaces os usuários podem adicionar usando [managed marketplace restrictions](/pt/plugin-marketplaces#managed-marketplace-restrictions).

## Troubleshooting

### Comando /plugin não reconhecido

Se você vir "unknown command" ou o comando `/plugin` não aparecer:

1. **Verifique sua versão**: Execute `claude --version`. Plugins requerem versão 1.0.33 ou posterior.
2. **Atualize Claude Code**:
   * **Homebrew**: `brew upgrade claude-code`
   * **npm**: `npm update -g @anthropic-ai/claude-code`
   * **Native installer**: Re-execute o comando de instalação de [Setup](/pt/setup)
3. **Reinicie Claude Code**: Após atualizar, reinicie seu terminal e execute `claude` novamente.

### Problemas comuns

* **Marketplace não carregando**: Verifique se a URL está acessível e se `.claude-plugin/marketplace.json` existe no caminho
* **Falhas de instalação de plugin**: Verifique se as URLs de fonte do plugin estão acessíveis e repositórios são públicos (ou você tem acesso)
* **Arquivos não encontrados após instalação**: Plugins são copiados para um cache, então caminhos referenciando arquivos fora do diretório do plugin não funcionarão
* **Skills de plugin não aparecendo**: Limpe o cache com `rm -rf ~/.claude/plugins/cache`, reinicie Claude Code e reinstale o plugin.

Para troubleshooting detalhado com soluções, veja [Troubleshooting](/pt/plugin-marketplaces#troubleshooting) no guia de marketplace. Para ferramentas de debugging, veja [Debugging and development tools](/pt/plugins-reference#debugging-and-development-tools).

### Problemas de code intelligence

* **Language server não iniciando**: verifique se o binário está instalado e disponível em seu `$PATH`. Verifique a aba Errors do `/plugin` para detalhes.
* **Alto uso de memória**: language servers como `rust-analyzer` e `pyright` podem consumir memória significativa em projetos grandes. Se você experimentar problemas de memória, desabilite o plugin com `/plugin disable <plugin-name>` e confie nas ferramentas de busca integradas do Claude.
* **Diagnósticos falsos positivos em monorepos**: language servers podem relatar erros de importação não resolvida para pacotes internos se o workspace não estiver configurado corretamente. Esses não afetam a capacidade do Claude de editar código.

## Próximos passos

* **Construa seus próprios plugins**: Veja [Plugins](/pt/plugins) para criar skills, agentes e hooks
* **Crie um marketplace**: Veja [Criar um marketplace de plugins](/pt/plugin-marketplaces) para distribuir plugins para sua equipe ou comunidade
* **Referência técnica**: Veja [Plugins reference](/pt/plugins-reference) para especificações completas
