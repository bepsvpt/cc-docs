> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Use Claude Code in VS Code

> Instale e configure a extensão Claude Code para VS Code. Obtenha assistência de codificação com IA com diffs inline, @-mentions, revisão de plano e atalhos de teclado.

<img src="https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=300652d5678c63905e6b0ea9e50835f8" alt="Editor VS Code com o painel de extensão Claude Code aberto no lado direito, mostrando uma conversa com Claude" width="2500" height="1155" data-path="images/vs-code-extension-interface.jpg" />

A extensão VS Code fornece uma interface gráfica nativa para Claude Code, integrada diretamente ao seu IDE. Esta é a forma recomendada de usar Claude Code no VS Code.

Com a extensão, você pode revisar e editar os planos do Claude antes de aceitá-los, aceitar automaticamente edições conforme são feitas, @-mention arquivos com intervalos de linhas específicas da sua seleção, acessar histórico de conversas e abrir múltiplas conversas em abas separadas ou janelas.

## Pré-requisitos

Antes de instalar, certifique-se de que você tem:

* VS Code 1.98.0 ou superior
* Uma conta Anthropic (você fará login quando abrir a extensão pela primeira vez). Se você estiver usando um provedor de terceiros como Amazon Bedrock ou Google Vertex AI, veja [Use third-party providers](#use-third-party-providers) em vez disso.

<Tip>
  A extensão inclui o CLI (interface de linha de comando), que você pode acessar do terminal integrado do VS Code para recursos avançados. Veja [VS Code extension vs. Claude Code CLI](#vs-code-extension-vs-claude-code-cli) para detalhes.
</Tip>

## Instale a extensão

Clique no link do seu IDE para instalar diretamente:

* [Install for VS Code](vscode:extension/anthropic.claude-code)
* [Install for Cursor](cursor:extension/anthropic.claude-code)

Ou no VS Code, pressione `Cmd+Shift+X` (Mac) ou `Ctrl+Shift+X` (Windows/Linux) para abrir a visualização de Extensões, procure por "Claude Code" e clique em **Install**.

<Note>Se a extensão não aparecer após a instalação, reinicie o VS Code ou execute "Developer: Reload Window" na Paleta de Comandos.</Note>

## Comece

Depois de instalada, você pode começar a usar Claude Code através da interface VS Code:

<Steps>
  <Step title="Abra o painel Claude Code">
    Em todo o VS Code, o ícone Spark indica Claude Code: <img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/vs-code-spark-icon.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=3ca45e00deadec8c8f4b4f807da94505" alt="Spark icon" style={{display: "inline", height: "0.85em", verticalAlign: "middle"}} width="16" height="16" data-path="images/vs-code-spark-icon.svg" />

    A forma mais rápida de abrir Claude é clicar no ícone Spark na **Editor Toolbar** (canto superior direito do editor). O ícone só aparece quando você tem um arquivo aberto.

        <img src="https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=eb4540325d94664c51776dbbfec4cf02" alt="Editor VS Code mostrando o ícone Spark na Editor Toolbar" width="2796" height="734" data-path="images/vs-code-editor-icon.png" />

    Outras formas de abrir Claude Code:

    * **Activity Bar**: clique no ícone Spark na barra lateral esquerda para abrir a lista de sessões. Clique em qualquer sessão para abri-la como uma aba de editor completa, ou inicie uma nova. Este ícone está sempre visível na Activity Bar.
    * **Command Palette**: `Cmd+Shift+P` (Mac) ou `Ctrl+Shift+P` (Windows/Linux), digite "Claude Code" e selecione uma opção como "Open in New Tab"
    * **Status Bar**: clique em **✱ Claude Code** no canto inferior direito da janela. Isto funciona mesmo quando nenhum arquivo está aberto.

    Quando você abre o painel pela primeira vez, uma lista de verificação **Learn Claude Code** aparece. Trabalhe em cada item clicando em **Show me**, ou descarte-a com o X. Para reabri-la mais tarde, desmarque **Hide Onboarding** nas configurações do VS Code em Extensions → Claude Code.

    Você pode arrastar o painel Claude para reposicioná-lo em qualquer lugar no VS Code. Veja [Customize your workflow](#customize-your-workflow) para detalhes.
  </Step>

  <Step title="Envie um prompt">
    Peça ao Claude para ajudar com seu código ou arquivos, seja explicando como algo funciona, depurando um problema ou fazendo alterações.

    <Tip>Claude vê automaticamente seu texto selecionado. Pressione `Option+K` (Mac) / `Alt+K` (Windows/Linux) para também inserir uma referência @-mention (como `@file.ts#5-10`) em seu prompt.</Tip>

    Aqui está um exemplo de pergunta sobre uma linha particular em um arquivo:

        <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-send-prompt.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=ede3ed8d8d5f940e01c5de636d009cfd" alt="Editor VS Code com as linhas 2-3 selecionadas em um arquivo Python, e o painel Claude Code mostrando uma pergunta sobre essas linhas com uma referência @-mention" width="3288" height="1876" data-path="images/vs-code-send-prompt.png" />
  </Step>

  <Step title="Revise as alterações">
    Quando Claude quer editar um arquivo, ele mostra uma comparação lado a lado do original e das alterações propostas, depois pede permissão. Você pode aceitar, rejeitar ou dizer ao Claude o que fazer em vez disso.

        <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-edits.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=e005f9b41c541c5c7c59c082f7c4841c" alt="VS Code mostrando um diff das alterações propostas por Claude com um prompt de permissão perguntando se deve fazer a edição" width="3292" height="1876" data-path="images/vs-code-edits.png" />
  </Step>
</Steps>

Para mais ideias sobre o que você pode fazer com Claude Code, veja [Common workflows](/pt/common-workflows).

<Tip>
  Execute "Claude Code: Open Walkthrough" na Paleta de Comandos para um tour guiado dos conceitos básicos.
</Tip>

## Use a caixa de prompt

A caixa de prompt suporta vários recursos:

* **Permission modes**: clique no indicador de modo na parte inferior da caixa de prompt para alternar modos. No modo normal, Claude pede permissão antes de cada ação. Em Plan Mode, Claude descreve o que fará e aguarda aprovação antes de fazer alterações. VS Code abre automaticamente o plano como um documento markdown completo onde você pode adicionar comentários inline para dar feedback antes de Claude começar. Em modo auto-accept, Claude faz edições sem perguntar. Defina o padrão nas configurações do VS Code em `claudeCode.initialPermissionMode`.
* **Command menu**: clique em `/` ou digite `/` para abrir o menu de comandos. As opções incluem anexar arquivos, alternar modelos, alternar pensamento estendido e visualizar uso de plano (`/usage`). A seção Customize fornece acesso a MCP servers, hooks, memory, permissions e plugins. Itens com um ícone de terminal abrem no terminal integrado.
* **Context indicator**: a caixa de prompt mostra quanto da janela de contexto do Claude você está usando. Claude compacta automaticamente quando necessário, ou você pode executar `/compact` manualmente.
* **Extended thinking**: permite que Claude gaste mais tempo raciocinando sobre problemas complexos. Alterne-o via menu de comandos (`/`). Veja [Extended thinking](/pt/common-workflows#use-extended-thinking-thinking-mode) para detalhes.
* **Multi-line input**: pressione `Shift+Enter` para adicionar uma nova linha sem enviar. Isto também funciona na entrada de texto livre "Other" de diálogos de pergunta.

### Reference files and folders

Use @-mentions para dar ao Claude contexto sobre arquivos ou pastas específicas. Quando você digita `@` seguido de um nome de arquivo ou pasta, Claude lê esse conteúdo e pode responder perguntas sobre ele ou fazer alterações nele. Claude Code suporta fuzzy matching, então você pode digitar nomes parciais para encontrar o que precisa:

```text  theme={null}
> Explain the logic in @auth (fuzzy matches auth.js, AuthService.ts, etc.)
> What's in @src/components/ (include a trailing slash for folders)
```

Para PDFs grandes, você pode pedir ao Claude para ler páginas específicas em vez do arquivo inteiro: uma única página, um intervalo como páginas 1-10, ou um intervalo aberto como página 3 em diante.

Quando você seleciona texto no editor, Claude pode ver seu código destacado automaticamente. O rodapé da caixa de prompt mostra quantas linhas estão selecionadas. Pressione `Option+K` (Mac) / `Alt+K` (Windows/Linux) para inserir um @-mention com o caminho do arquivo e números de linha (por exemplo, `@app.ts#5-10`). Clique no indicador de seleção para alternar se Claude pode ver seu texto destacado - o ícone de barra de olho significa que a seleção está oculta do Claude.

Você também pode manter `Shift` pressionado enquanto arrasta arquivos para a caixa de prompt para adicioná-los como anexos. Clique no X em qualquer anexo para removê-lo do contexto.

### Resume past conversations

Clique no dropdown na parte superior do painel Claude Code para acessar seu histórico de conversas. Você pode pesquisar por palavra-chave ou navegar por tempo (Today, Yesterday, Last 7 days, etc.). Clique em qualquer conversa para retomá-la com o histórico completo de mensagens. Passe o mouse sobre uma sessão para revelar ações de renomear e remover: renomeie para dar um título descritivo, ou remova para deletá-la da lista. Para mais sobre retomar sessões, veja [Common workflows](/pt/common-workflows#resume-previous-conversations).

### Resume remote sessions from Claude.ai

Se você usar [Claude Code on the web](/pt/claude-code-on-the-web), você pode retomar essas sessões remotas diretamente no VS Code. Isto requer fazer login com **Claude.ai Subscription**, não Anthropic Console.

<Steps>
  <Step title="Open Past Conversations">
    Clique no dropdown **Past Conversations** na parte superior do painel Claude Code.
  </Step>

  <Step title="Select the Remote tab">
    O diálogo mostra duas abas: Local e Remote. Clique em **Remote** para ver sessões de claude.ai.
  </Step>

  <Step title="Select a session to resume">
    Navegue ou pesquise suas sessões remotas. Clique em qualquer sessão para baixá-la e continuar a conversa localmente.
  </Step>
</Steps>

<Note>
  Apenas sessões web iniciadas com um repositório GitHub aparecem na aba Remote. Retomar carrega o histórico de conversas localmente; as alterações não são sincronizadas de volta para claude.ai.
</Note>

## Customize your workflow

Depois que você estiver funcionando, você pode reposicionar o painel Claude, executar múltiplas sessões ou alternar para modo terminal.

### Choose where Claude lives

Você pode arrastar o painel Claude para reposicioná-lo em qualquer lugar no VS Code. Pegue a aba ou barra de título do painel e arraste para:

* **Secondary sidebar**: o lado direito da janela. Mantém Claude visível enquanto você codifica.
* **Primary sidebar**: a barra lateral esquerda com ícones para Explorer, Search, etc.
* **Editor area**: abre Claude como uma aba ao lado de seus arquivos. Útil para tarefas secundárias.

<Tip>
  Use a barra lateral para sua sessão principal do Claude e abra abas adicionais para tarefas secundárias. Claude lembra sua localização preferida. O ícone da lista de sessões da Activity Bar é separado do painel Claude: a lista de sessões está sempre visível na Activity Bar, enquanto o ícone do painel Claude só aparece lá quando o painel está encaixado na barra lateral esquerda.
</Tip>

### Run multiple conversations

Use **Open in New Tab** ou **Open in New Window** na Paleta de Comandos para iniciar conversas adicionais. Cada conversa mantém seu próprio histórico e contexto, permitindo que você trabalhe em diferentes tarefas em paralelo.

Ao usar abas, um pequeno ponto colorido no ícone spark indica status: azul significa que uma solicitação de permissão está pendente, laranja significa que Claude terminou enquanto a aba estava oculta.

### Switch to terminal mode

Por padrão, a extensão abre um painel de chat gráfico. Se você preferir a interface estilo CLI, abra a [Use Terminal setting](vscode://settings/claudeCode.useTerminal) e marque a caixa.

Você também pode abrir as configurações do VS Code (`Cmd+,` no Mac ou `Ctrl+,` no Windows/Linux), ir para Extensions → Claude Code e marcar **Use Terminal**.

## Manage plugins

A extensão VS Code inclui uma interface gráfica para instalar e gerenciar [plugins](/pt/plugins). Digite `/plugins` na caixa de prompt para abrir a interface **Manage plugins**.

### Install plugins

O diálogo de plugin mostra duas abas: **Plugins** e **Marketplaces**.

Na aba Plugins:

* **Installed plugins** aparecem no topo com interruptores de alternância para habilitá-los ou desabilitá-los
* **Available plugins** de seus marketplaces configurados aparecem abaixo
* Pesquise para filtrar plugins por nome ou descrição
* Clique em **Install** em qualquer plugin disponível

Quando você instala um plugin, escolha o escopo de instalação:

* **Install for you**: disponível em todos os seus projetos (escopo de usuário)
* **Install for this project**: compartilhado com colaboradores do projeto (escopo de projeto)
* **Install locally**: apenas para você, apenas neste repositório (escopo local)

### Manage marketplaces

Alterne para a aba **Marketplaces** para adicionar ou remover fontes de plugin:

* Digite um repositório GitHub, URL ou caminho local para adicionar um novo marketplace
* Clique no ícone de atualização para atualizar a lista de plugins de um marketplace
* Clique no ícone de lixeira para remover um marketplace

Depois de fazer alterações, um banner o solicita a reiniciar Claude Code para aplicar as atualizações.

<Note>
  O gerenciamento de plugins no VS Code usa os mesmos comandos CLI sob o capô. Plugins e marketplaces que você configura na extensão também estão disponíveis no CLI, e vice-versa.
</Note>

Para mais sobre o sistema de plugins, veja [Plugins](/pt/plugins) e [Plugin marketplaces](/pt/plugin-marketplaces).

## Automate browser tasks with Chrome

Conecte Claude ao seu navegador Chrome para testar aplicativos web, depurar com logs de console e automatizar fluxos de trabalho do navegador sem sair do VS Code. Isto requer a [Claude in Chrome extension](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) versão 1.0.36 ou superior.

Digite `@browser` na caixa de prompt seguido do que você quer que Claude faça:

```text  theme={null}
@browser go to localhost:3000 and check the console for errors
```

Você também pode abrir o menu de anexos para selecionar ferramentas específicas do navegador como abrir uma nova aba ou ler conteúdo da página.

Claude abre novas abas para tarefas do navegador e compartilha o estado de login do seu navegador, então pode acessar qualquer site em que você já esteja conectado.

Para instruções de configuração, a lista completa de capacidades e solução de problemas, veja [Use Claude Code with Chrome](/pt/chrome).

## VS Code commands and shortcuts

Abra a Paleta de Comandos (`Cmd+Shift+P` no Mac ou `Ctrl+Shift+P` no Windows/Linux) e digite "Claude Code" para ver todos os comandos VS Code disponíveis para a extensão Claude Code.

Alguns atalhos dependem de qual painel está "focused" (recebendo entrada de teclado). Quando seu cursor está em um arquivo de código, o editor está focado. Quando seu cursor está na caixa de prompt do Claude, Claude está focado. Use `Cmd+Esc` / `Ctrl+Esc` para alternar entre eles.

<Note>
  Estes são comandos VS Code para controlar a extensão. Nem todos os comandos Claude Code integrados estão disponíveis na extensão. Veja [VS Code extension vs. Claude Code CLI](#vs-code-extension-vs-claude-code-cli) para detalhes.
</Note>

| Command                    | Shortcut                                                 | Description                                                                          |
| -------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Focus Input                | `Cmd+Esc` (Mac) / `Ctrl+Esc` (Windows/Linux)             | Alterne o foco entre editor e Claude                                                 |
| Open in Side Bar           | -                                                        | Abra Claude na barra lateral esquerda                                                |
| Open in Terminal           | -                                                        | Abra Claude em modo terminal                                                         |
| Open in New Tab            | `Cmd+Shift+Esc` (Mac) / `Ctrl+Shift+Esc` (Windows/Linux) | Abra uma nova conversa como uma aba de editor                                        |
| Open in New Window         | -                                                        | Abra uma nova conversa em uma janela separada                                        |
| New Conversation           | `Cmd+N` (Mac) / `Ctrl+N` (Windows/Linux)                 | Inicie uma nova conversa (requer que Claude esteja focado)                           |
| Insert @-Mention Reference | `Option+K` (Mac) / `Alt+K` (Windows/Linux)               | Insira uma referência ao arquivo atual e seleção (requer que o editor esteja focado) |
| Show Logs                  | -                                                        | Visualize logs de depuração da extensão                                              |
| Logout                     | -                                                        | Saia de sua conta Anthropic                                                          |

## Configure settings

A extensão tem dois tipos de configurações:

* **Extension settings** no VS Code: controlam o comportamento da extensão dentro do VS Code. Abra com `Cmd+,` (Mac) ou `Ctrl+,` (Windows/Linux), depois vá para Extensions → Claude Code. Você também pode digitar `/` e selecionar **General Config** para abrir as configurações.
* **Claude Code settings** em `~/.claude/settings.json`: compartilhadas entre a extensão e CLI. Use para comandos permitidos, variáveis de ambiente, hooks e MCP servers. Veja [Settings](/pt/settings) para detalhes.

<Tip>
  Adicione `"$schema": "https://json.schemastore.org/claude-code-settings.json"` ao seu `settings.json` para obter autocomplete e validação inline para todas as configurações disponíveis diretamente no VS Code.
</Tip>

### Extension settings

| Setting                           | Default   | Description                                                                                                                      |
| --------------------------------- | --------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `selectedModel`                   | `default` | Modelo para novas conversas. Altere por sessão com `/model`.                                                                     |
| `useTerminal`                     | `false`   | Inicie Claude em modo terminal em vez de painel gráfico                                                                          |
| `initialPermissionMode`           | `default` | Controla prompts de aprovação: `default` (pergunte cada vez), `plan`, `acceptEdits` ou `bypassPermissions`                       |
| `preferredLocation`               | `panel`   | Onde Claude abre: `sidebar` (direita) ou `panel` (nova aba)                                                                      |
| `autosave`                        | `true`    | Auto-salve arquivos antes de Claude lê-los ou escrevê-los                                                                        |
| `useCtrlEnterToSend`              | `false`   | Use Ctrl/Cmd+Enter em vez de Enter para enviar prompts                                                                           |
| `enableNewConversationShortcut`   | `true`    | Habilite Cmd/Ctrl+N para iniciar uma nova conversa                                                                               |
| `hideOnboarding`                  | `false`   | Oculte a lista de verificação de onboarding (ícone de chapéu de formatura)                                                       |
| `respectGitIgnore`                | `true`    | Exclua padrões .gitignore de pesquisas de arquivo                                                                                |
| `environmentVariables`            | `[]`      | Defina variáveis de ambiente para o processo Claude. Use configurações Claude Code em vez disso para configuração compartilhada. |
| `disableLoginPrompt`              | `false`   | Pule prompts de autenticação (para configurações de provedor de terceiros)                                                       |
| `allowDangerouslySkipPermissions` | `false`   | Contorne todos os prompts de permissão. **Use com extrema cautela.**                                                             |
| `claudeProcessWrapper`            | -         | Caminho executável usado para iniciar o processo Claude                                                                          |

## VS Code extension vs. Claude Code CLI

Claude Code está disponível tanto como uma extensão VS Code (painel gráfico) quanto como um CLI (interface de linha de comando no terminal). Alguns recursos estão disponíveis apenas no CLI. Se você precisar de um recurso apenas CLI, execute `claude` no terminal integrado do VS Code.

| Feature             | CLI                                           | VS Code Extension                                                                                  |
| ------------------- | --------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Commands and skills | [All](/pt/interactive-mode#built-in-commands) | Subset (digite `/` para ver disponíveis)                                                           |
| MCP server config   | Yes                                           | Partial (adicione servidores via CLI; gerencie servidores existentes com `/mcp` no painel de chat) |
| Checkpoints         | Yes                                           | Yes                                                                                                |
| `!` bash shortcut   | Yes                                           | No                                                                                                 |
| Tab completion      | Yes                                           | No                                                                                                 |

### Rewind with checkpoints

A extensão VS Code suporta checkpoints, que rastreiam edições de arquivo do Claude e permitem que você retroceda para um estado anterior. Passe o mouse sobre qualquer mensagem para revelar o botão de retrocesso, depois escolha entre três opções:

* **Fork conversation from here**: inicie um novo ramo de conversa a partir desta mensagem mantendo todas as alterações de código intactas
* **Rewind code to here**: reverta alterações de arquivo de volta a este ponto na conversa mantendo o histórico completo de conversas
* **Fork conversation and rewind code**: inicie um novo ramo de conversa e reverta alterações de arquivo para este ponto

Para detalhes completos sobre como checkpoints funcionam e suas limitações, veja [Checkpointing](/pt/checkpointing).

### Run CLI in VS Code

Para usar o CLI enquanto permanece no VS Code, abra o terminal integrado (`` Ctrl+` `` no Windows/Linux ou `` Cmd+` `` no Mac) e execute `claude`. O CLI se integra automaticamente com seu IDE para recursos como visualização de diff e compartilhamento de diagnósticos.

Se usar um terminal externo, execute `/ide` dentro de Claude Code para conectá-lo ao VS Code.

### Switch between extension and CLI

A extensão e CLI compartilham o mesmo histórico de conversas. Para continuar uma conversa de extensão no CLI, execute `claude --resume` no terminal. Isto abre um seletor interativo onde você pode pesquisar e selecionar sua conversa.

### Include terminal output in prompts

Referencie saída de terminal em seus prompts usando `@terminal:name` onde `name` é o título do terminal. Isto permite que Claude veja saída de comando, mensagens de erro ou logs sem copiar e colar.

### Monitor background processes

Quando Claude executa comandos de longa duração, a extensão mostra progresso na barra de status. No entanto, a visibilidade para tarefas em segundo plano é limitada em comparação com o CLI. Para melhor visibilidade, peça ao Claude para exibir o comando para que você possa executá-lo no terminal integrado do VS Code.

### Connect to external tools with MCP

MCP (Model Context Protocol) servers dão ao Claude acesso a ferramentas externas, bancos de dados e APIs.

Para adicionar um MCP server, abra o terminal integrado (`` Ctrl+` `` ou `` Cmd+` ``) e execute:

```bash  theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

Uma vez configurado, peça ao Claude para usar as ferramentas (por exemplo, "Review PR #456").

Para gerenciar MCP servers sem sair do VS Code, digite `/mcp` no painel de chat. O diálogo de gerenciamento MCP permite que você habilite ou desabilite servidores, reconecte a um servidor e gerencie autenticação OAuth. Veja a [MCP documentation](/pt/mcp) para servidores disponíveis.

## Work with git

Claude Code se integra com git para ajudar com fluxos de trabalho de controle de versão diretamente no VS Code. Peça ao Claude para fazer commit de alterações, criar pull requests ou trabalhar entre branches.

### Create commits and pull requests

Claude pode preparar alterações, escrever mensagens de commit e criar pull requests com base em seu trabalho:

```text  theme={null}
> commit my changes with a descriptive message
> create a pr for this feature
> summarize the changes I've made to the auth module
```

Ao criar pull requests, Claude gera descrições com base nas alterações de código reais e pode adicionar contexto sobre testes ou decisões de implementação.

### Use git worktrees for parallel tasks

Use a flag `--worktree` (`-w`) para iniciar Claude em um worktree isolado com seus próprios arquivos e branch:

```bash  theme={null}
claude --worktree feature-auth
```

Cada worktree mantém estado de arquivo independente enquanto compartilha histórico git. Isto previne que instâncias do Claude interfiram uma com a outra ao trabalhar em diferentes tarefas. Para mais detalhes, veja [Run parallel sessions with Git worktrees](/pt/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees).

## Use third-party providers

Por padrão, Claude Code se conecta diretamente à API do Anthropic. Se sua organização usa Amazon Bedrock, Google Vertex AI ou Microsoft Foundry para acessar Claude, configure a extensão para usar seu provedor em vez disso:

<Steps>
  <Step title="Disable login prompt">
    Abra a [Disable Login Prompt setting](vscode://settings/claudeCode.disableLoginPrompt) e marque a caixa.

    Você também pode abrir as configurações do VS Code (`Cmd+,` no Mac ou `Ctrl+,` no Windows/Linux), pesquisar por "Claude Code login" e marcar **Disable Login Prompt**.
  </Step>

  <Step title="Configure your provider">
    Siga o guia de configuração para seu provedor:

    * [Claude Code on Amazon Bedrock](/pt/amazon-bedrock)
    * [Claude Code on Google Vertex AI](/pt/google-vertex-ai)
    * [Claude Code on Microsoft Foundry](/pt/microsoft-foundry)

    Estes guias cobrem a configuração de seu provedor em `~/.claude/settings.json`, o que garante que suas configurações sejam compartilhadas entre a extensão VS Code e o CLI.
  </Step>
</Steps>

## Security and privacy

Seu código permanece privado. Claude Code processa seu código para fornecer assistência, mas não o usa para treinar modelos. Para detalhes sobre manipulação de dados e como optar por não fazer logging, veja [Data and privacy](/pt/data-usage).

Com permissões de auto-edição habilitadas, Claude Code pode modificar arquivos de configuração do VS Code (como `settings.json` ou `tasks.json`) que o VS Code pode executar automaticamente. Para reduzir o risco ao trabalhar com código não confiável:

* Habilite [VS Code Restricted Mode](https://code.visualstudio.com/docs/editor/workspace-trust#_restricted-mode) para espaços de trabalho não confiáveis
* Use modo de aprovação manual em vez de auto-accept para edições
* Revise as alterações cuidadosamente antes de aceitá-las

## Fix common issues

### Extension won't install

* Certifique-se de que você tem uma versão compatível do VS Code (1.98.0 ou posterior)
* Verifique se o VS Code tem permissão para instalar extensões
* Tente instalar diretamente do [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)

### Spark icon not visible

O ícone Spark aparece na **Editor Toolbar** (canto superior direito do editor) quando você tem um arquivo aberto. Se você não o vê:

1. **Open a file**: O ícone requer um arquivo aberto. Ter apenas uma pasta aberta não é suficiente.
2. **Check VS Code version**: Requer 1.98.0 ou superior (Help → About)
3. **Restart VS Code**: Execute "Developer: Reload Window" na Paleta de Comandos
4. **Disable conflicting extensions**: Desabilite temporariamente outras extensões de IA (Cline, Continue, etc.)
5. **Check workspace trust**: A extensão não funciona em Restricted Mode

Alternativamente, clique em "✱ Claude Code" na **Status Bar** (canto inferior direito). Isto funciona mesmo sem um arquivo aberto. Você também pode usar a **Command Palette** (`Cmd+Shift+P` / `Ctrl+Shift+P`) e digitar "Claude Code".

### Claude Code never responds

Se Claude Code não está respondendo aos seus prompts:

1. **Check your internet connection**: Certifique-se de que você tem uma conexão de internet estável
2. **Start a new conversation**: Tente iniciar uma nova conversa para ver se o problema persiste
3. **Try the CLI**: Execute `claude` do terminal para ver se você obtém mensagens de erro mais detalhadas

Se os problemas persistirem, [file an issue on GitHub](https://github.com/anthropics/claude-code/issues) com detalhes sobre o erro.

## Uninstall the extension

Para desinstalar a extensão Claude Code:

1. Abra a visualização de Extensões (`Cmd+Shift+X` no Mac ou `Ctrl+Shift+X` no Windows/Linux)
2. Pesquise por "Claude Code"
3. Clique em **Uninstall**

Para também remover dados de extensão e redefinir todas as configurações:

```bash  theme={null}
rm -rf ~/.vscode/globalStorage/anthropic.claude-code
```

Para ajuda adicional, veja o [troubleshooting guide](/pt/troubleshooting).

## Next steps

Agora que você tem Claude Code configurado no VS Code:

* [Explore common workflows](/pt/common-workflows) para aproveitar ao máximo Claude Code
* [Set up MCP servers](/pt/mcp) para estender as capacidades do Claude com ferramentas externas. Adicione servidores usando o CLI, depois gerencie-os com `/mcp` no painel de chat.
* [Configure Claude Code settings](/pt/settings) para personalizar comandos permitidos, hooks e mais. Estas configurações são compartilhadas entre a extensão e CLI.
