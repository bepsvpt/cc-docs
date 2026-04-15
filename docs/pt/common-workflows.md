> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Fluxos de trabalho comuns

> Guias passo a passo para explorar bases de código, corrigir bugs, refatorar, testar e outras tarefas cotidianas com Claude Code.

Esta página aborda fluxos de trabalho práticos para desenvolvimento cotidiano: explorar código desconhecido, depuração, refatoração, escrita de testes, criação de PRs e gerenciamento de sessões. Cada seção inclui exemplos de prompts que você pode adaptar aos seus próprios projetos. Para padrões e dicas de nível superior, consulte [Melhores práticas](/pt/best-practices).

## Entender novas bases de código

### Obter uma visão geral rápida da base de código

Suponha que você acabou de ingressar em um novo projeto e precisa entender sua estrutura rapidamente.

<Steps>
  <Step title="Navegue até o diretório raiz do projeto">
    ```bash theme={null}
    cd /path/to/project 
    ```
  </Step>

  <Step title="Inicie Claude Code">
    ```bash theme={null}
    claude 
    ```
  </Step>

  <Step title="Peça uma visão geral de alto nível">
    ```text theme={null}
    give me an overview of this codebase
    ```
  </Step>

  <Step title="Aprofunde-se em componentes específicos">
    ```text theme={null}
    explain the main architecture patterns used here
    ```

    ```text theme={null}
    what are the key data models?
    ```

    ```text theme={null}
    how is authentication handled?
    ```
  </Step>
</Steps>

<Tip>
  Dicas:

  * Comece com perguntas amplas e depois estreite para áreas específicas
  * Pergunte sobre convenções de codificação e padrões usados no projeto
  * Solicite um glossário de termos específicos do projeto
</Tip>

### Encontrar código relevante

Suponha que você precise localizar código relacionado a um recurso ou funcionalidade específica.

<Steps>
  <Step title="Peça ao Claude para encontrar arquivos relevantes">
    ```text theme={null}
    find the files that handle user authentication
    ```
  </Step>

  <Step title="Obtenha contexto sobre como os componentes interagem">
    ```text theme={null}
    how do these authentication files work together?
    ```
  </Step>

  <Step title="Entenda o fluxo de execução">
    ```text theme={null}
    trace the login process from front-end to database
    ```
  </Step>
</Steps>

<Tip>
  Dicas:

  * Seja específico sobre o que você está procurando
  * Use linguagem de domínio do projeto
  * Instale um [plugin de inteligência de código](/pt/discover-plugins#code-intelligence) para sua linguagem para dar ao Claude navegação precisa de "ir para definição" e "encontrar referências"
</Tip>

***

## Corrigir bugs com eficiência

Suponha que você tenha encontrado uma mensagem de erro e precise encontrar e corrigir sua origem.

<Steps>
  <Step title="Compartilhe o erro com Claude">
    ```text theme={null}
    I'm seeing an error when I run npm test
    ```
  </Step>

  <Step title="Peça recomendações de correção">
    ```text theme={null}
    suggest a few ways to fix the @ts-ignore in user.ts
    ```
  </Step>

  <Step title="Aplique a correção">
    ```text theme={null}
    update user.ts to add the null check you suggested
    ```
  </Step>
</Steps>

<Tip>
  Dicas:

  * Diga ao Claude o comando para reproduzir o problema e obtenha um rastreamento de pilha
  * Mencione quaisquer etapas para reproduzir o erro
  * Deixe Claude saber se o erro é intermitente ou consistente
</Tip>

***

## Refatorar código

Suponha que você precise atualizar código antigo para usar padrões e práticas modernas.

<Steps>
  <Step title="Identifique código legado para refatoração">
    ```text theme={null}
    find deprecated API usage in our codebase
    ```
  </Step>

  <Step title="Obtenha recomendações de refatoração">
    ```text theme={null}
    suggest how to refactor utils.js to use modern JavaScript features
    ```
  </Step>

  <Step title="Aplique as alterações com segurança">
    ```text theme={null}
    refactor utils.js to use ES2024 features while maintaining the same behavior
    ```
  </Step>

  <Step title="Verifique a refatoração">
    ```text theme={null}
    run tests for the refactored code
    ```
  </Step>
</Steps>

<Tip>
  Dicas:

  * Peça ao Claude para explicar os benefícios da abordagem moderna
  * Solicite que as alterações mantenham compatibilidade com versões anteriores quando necessário
  * Faça refatoração em pequenos incrementos testáveis
</Tip>

***

## Usar subagents especializados

Suponha que você queira usar subagents de IA especializados para lidar com tarefas específicas de forma mais eficaz.

<Steps>
  <Step title="Visualize subagents disponíveis">
    ```text theme={null}
    /agents
    ```

    Isso mostra todos os subagents disponíveis e permite que você crie novos.
  </Step>

  <Step title="Use subagents automaticamente">
    Claude Code delega automaticamente tarefas apropriadas para subagents especializados:

    ```text theme={null}
    review my recent code changes for security issues
    ```

    ```text theme={null}
    run all tests and fix any failures
    ```
  </Step>

  <Step title="Solicite explicitamente subagents específicos">
    ```text theme={null}
    use the code-reviewer subagent to check the auth module
    ```

    ```text theme={null}
    have the debugger subagent investigate why users can't log in
    ```
  </Step>

  <Step title="Crie subagents personalizados para seu fluxo de trabalho">
    ```text theme={null}
    /agents
    ```

    Em seguida, selecione "Create New subagent" e siga os prompts para definir:

    * Um identificador único que descreve o propósito do subagent (por exemplo, `code-reviewer`, `api-designer`).
    * Quando Claude deve usar este agente
    * Quais ferramentas ele pode acessar
    * Um prompt do sistema descrevendo o papel e comportamento do agente
  </Step>
</Steps>

<Tip>
  Dicas:

  * Crie subagents específicos do projeto em `.claude/agents/` para compartilhamento em equipe
  * Use campos `description` descritivos para permitir delegação automática
  * Limite o acesso a ferramentas ao que cada subagent realmente precisa
  * Consulte a [documentação de subagents](/pt/sub-agents) para exemplos detalhados
</Tip>

***

## Usar Plan Mode para análise segura de código

Plan Mode instrui Claude a criar um plano analisando a base de código com operações somente leitura, perfeito para explorar bases de código, planejar alterações complexas ou revisar código com segurança. Em Plan Mode, Claude usa [`AskUserQuestion`](/pt/tools-reference) para reunir requisitos e esclarecer seus objetivos antes de propor um plano.

### Quando usar Plan Mode

* **Implementação multi-etapa**: Quando seu recurso requer fazer edições em muitos arquivos
* **Exploração de código**: Quando você quer pesquisar a base de código completamente antes de alterar qualquer coisa
* **Desenvolvimento interativo**: Quando você quer iterar na direção com Claude

### Como usar Plan Mode

**Ative Plan Mode durante uma sessão**

Você pode mudar para Plan Mode durante uma sessão usando **Shift+Tab** para percorrer os modos de permissão.

Se você estiver em Normal Mode, **Shift+Tab** primeiro muda para Auto-Accept Mode, indicado por `⏵⏵ accept edits on` na parte inferior do terminal. Um **Shift+Tab** subsequente mudará para Plan Mode, indicado por `⏸ plan mode on`.

**Inicie uma nova sessão em Plan Mode**

Para iniciar uma nova sessão em Plan Mode, use a flag `--permission-mode plan`:

```bash theme={null}
claude --permission-mode plan
```

**Execute consultas "headless" em Plan Mode**

Você também pode executar uma consulta em Plan Mode diretamente com `-p` (ou seja, em ["modo headless"](/pt/headless)):

```bash theme={null}
claude --permission-mode plan -p "Analyze the authentication system and suggest improvements"
```

### Exemplo: Planejando uma refatoração complexa

```bash theme={null}
claude --permission-mode plan
```

```text theme={null}
I need to refactor our authentication system to use OAuth2. Create a detailed migration plan.
```

Claude analisa a implementação atual e cria um plano abrangente. Refine com acompanhamentos:

```text theme={null}
What about backward compatibility?
```

```text theme={null}
How should we handle database migration?
```

<Tip>Pressione `Ctrl+G` para abrir o plano em seu editor de texto padrão, onde você pode editá-lo diretamente antes de Claude prosseguir.</Tip>

Quando você aceita um plano, Claude automaticamente nomeia a sessão a partir do conteúdo do plano. O nome aparece na barra de prompt e no seletor de sessão. Se você já definiu um nome com `--name` ou `/rename`, aceitar um plano não o sobrescreverá.

### Configure Plan Mode como padrão

```json theme={null}
// .claude/settings.json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

Consulte a [documentação de configurações](/pt/settings#available-settings) para mais opções de configuração.

***

## Trabalhar com testes

Suponha que você precise adicionar testes para código não coberto.

<Steps>
  <Step title="Identifique código não testado">
    ```text theme={null}
    find functions in NotificationsService.swift that are not covered by tests
    ```
  </Step>

  <Step title="Gere scaffolding de teste">
    ```text theme={null}
    add tests for the notification service
    ```
  </Step>

  <Step title="Adicione casos de teste significativos">
    ```text theme={null}
    add test cases for edge conditions in the notification service
    ```
  </Step>

  <Step title="Execute e verifique os testes">
    ```text theme={null}
    run the new tests and fix any failures
    ```
  </Step>
</Steps>

Claude pode gerar testes que seguem os padrões e convenções existentes do seu projeto. Ao solicitar testes, seja específico sobre qual comportamento você quer verificar. Claude examina seus arquivos de teste existentes para corresponder ao estilo, frameworks e padrões de asserção já em uso.

Para cobertura abrangente, peça ao Claude para identificar casos extremos que você pode ter perdido. Claude pode analisar seus caminhos de código e sugerir testes para condições de erro, valores de limite e entradas inesperadas que são fáceis de negligenciar.

***

## Criar pull requests

Você pode criar pull requests pedindo ao Claude diretamente ("create a pr for my changes"), ou guiar Claude através disso passo a passo:

<Steps>
  <Step title="Resuma suas alterações">
    ```text theme={null}
    summarize the changes I've made to the authentication module
    ```
  </Step>

  <Step title="Gere uma pull request">
    ```text theme={null}
    create a pr
    ```
  </Step>

  <Step title="Revise e refine">
    ```text theme={null}
    enhance the PR description with more context about the security improvements
    ```
  </Step>
</Steps>

Quando você cria uma PR usando `gh pr create`, a sessão é automaticamente vinculada a essa PR. Você pode retomá-la mais tarde com `claude --from-pr <number>`.

<Tip>
  Revise a PR gerada por Claude antes de enviar e peça ao Claude para destacar riscos ou considerações potenciais.
</Tip>

## Lidar com documentação

Suponha que você precise adicionar ou atualizar documentação para seu código.

<Steps>
  <Step title="Identifique código não documentado">
    ```text theme={null}
    find functions without proper JSDoc comments in the auth module
    ```
  </Step>

  <Step title="Gere documentação">
    ```text theme={null}
    add JSDoc comments to the undocumented functions in auth.js
    ```
  </Step>

  <Step title="Revise e melhore">
    ```text theme={null}
    improve the generated documentation with more context and examples
    ```
  </Step>

  <Step title="Verifique a documentação">
    ```text theme={null}
    check if the documentation follows our project standards
    ```
  </Step>
</Steps>

<Tip>
  Dicas:

  * Especifique o estilo de documentação que você deseja (JSDoc, docstrings, etc.)
  * Peça por exemplos na documentação
  * Solicite documentação para APIs públicas, interfaces e lógica complexa
</Tip>

***

## Trabalhar com imagens

Suponha que você precise trabalhar com imagens em sua base de código e queira ajuda do Claude para analisar o conteúdo da imagem.

<Steps>
  <Step title="Adicione uma imagem à conversa">
    Você pode usar qualquer um destes métodos:

    1. Arraste e solte uma imagem na janela do Claude Code
    2. Copie uma imagem e cole-a no CLI com ctrl+v (Não use cmd+v)
    3. Forneça um caminho de imagem ao Claude. Por exemplo, "Analyze this image: /path/to/your/image.png"
  </Step>

  <Step title="Peça ao Claude para analisar a imagem">
    ```text theme={null}
    What does this image show?
    ```

    ```text theme={null}
    Describe the UI elements in this screenshot
    ```

    ```text theme={null}
    Are there any problematic elements in this diagram?
    ```
  </Step>

  <Step title="Use imagens para contexto">
    ```text theme={null}
    Here's a screenshot of the error. What's causing it?
    ```

    ```text theme={null}
    This is our current database schema. How should we modify it for the new feature?
    ```
  </Step>

  <Step title="Obtenha sugestões de código do conteúdo visual">
    ```text theme={null}
    Generate CSS to match this design mockup
    ```

    ```text theme={null}
    What HTML structure would recreate this component?
    ```
  </Step>
</Steps>

<Tip>
  Dicas:

  * Use imagens quando descrições de texto seriam pouco claras ou complicadas
  * Inclua capturas de tela de erros, designs de UI ou diagramas para melhor contexto
  * Você pode trabalhar com múltiplas imagens em uma conversa
  * A análise de imagem funciona com diagramas, capturas de tela, mockups e muito mais
  * Quando Claude referencia imagens (por exemplo, `[Image #1]`), `Cmd+Click` (Mac) ou `Ctrl+Click` (Windows/Linux) o link para abrir a imagem em seu visualizador padrão
</Tip>

***

## Referenciar arquivos e diretórios

Use @ para incluir rapidamente arquivos ou diretórios sem esperar que Claude os leia.

<Steps>
  <Step title="Referencie um único arquivo">
    ```text theme={null}
    Explain the logic in @src/utils/auth.js
    ```

    Isso inclui o conteúdo completo do arquivo na conversa.
  </Step>

  <Step title="Referencie um diretório">
    ```text theme={null}
    What's the structure of @src/components?
    ```

    Isso fornece uma listagem de diretório com informações de arquivo.
  </Step>

  <Step title="Referencie recursos MCP">
    ```text theme={null}
    Show me the data from @github:repos/owner/repo/issues
    ```

    Isso busca dados de servidores MCP conectados usando o formato @server:resource. Consulte [recursos MCP](/pt/mcp#use-mcp-resources) para detalhes.
  </Step>
</Steps>

<Tip>
  Dicas:

  * Os caminhos de arquivo podem ser relativos ou absolutos
  * Referências de arquivo @ adicionam `CLAUDE.md` no diretório do arquivo e diretórios pai ao contexto
  * Referências de diretório mostram listagens de arquivo, não conteúdos
  * Você pode referenciar múltiplos arquivos em uma única mensagem (por exemplo, "@file1.js and @file2.js")
</Tip>

***

## Usar pensamento estendido (thinking mode)

[Pensamento estendido](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) é ativado por padrão, dando ao Claude espaço para raciocinar através de problemas complexos passo a passo antes de responder. Este raciocínio é visível em modo verboso, que você pode ativar com `Ctrl+O`.

Além disso, Opus 4.6 e Sonnet 4.6 suportam raciocínio adaptativo: em vez de um orçamento de token de pensamento fixo, o modelo aloca dinamicamente pensamento com base em sua configuração de [nível de esforço](/pt/model-config#adjust-effort-level). Pensamento estendido e raciocínio adaptativo trabalham juntos para lhe dar controle sobre o quão profundamente Claude raciocina antes de responder.

Pensamento estendido é particularmente valioso para decisões arquitetônicas complexas, bugs desafiadores, planejamento de implementação multi-etapa e avaliação de compensações entre diferentes abordagens.

<Note>
  Frases como "think", "think hard" e "think more" são interpretadas como instruções de prompt regulares e não alocam tokens de pensamento.
</Note>

### Configurar thinking mode

Pensamento é ativado por padrão, mas você pode ajustá-lo ou desativá-lo.

| Escopo                         | Como configurar                                                                             | Detalhes                                                                                                                                                                                                            |
| ------------------------------ | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Nível de esforço**           | Execute `/effort`, ajuste em `/model`, ou defina [`CLAUDE_CODE_EFFORT_LEVEL`](/pt/env-vars) | Controle a profundidade de pensamento para Opus 4.6 e Sonnet 4.6. Consulte [Ajustar nível de esforço](/pt/model-config#adjust-effort-level)                                                                         |
| **Palavra-chave `ultrathink`** | Inclua "ultrathink" em qualquer lugar em seu prompt                                         | Define esforço para alto para esse turno em Opus 4.6 e Sonnet 4.6. Útil para tarefas únicas que requerem raciocínio profundo sem alterar permanentemente sua configuração de esforço                                |
| **Atalho de alternância**      | Pressione `Option+T` (macOS) ou `Alt+T` (Windows/Linux)                                     | Alterne pensamento ligado/desligado para a sessão atual (todos os modelos). Pode exigir [configuração de terminal](/pt/terminal-config) para ativar atalhos de tecla Option                                         |
| **Padrão global**              | Use `/config` para alternar thinking mode                                                   | Define seu padrão em todos os projetos (todos os modelos).<br />Salvo como `alwaysThinkingEnabled` em `~/.claude/settings.json`                                                                                     |
| **Limitar orçamento de token** | Defina a variável de ambiente [`MAX_THINKING_TOKENS`](/pt/env-vars)                         | Limite o orçamento de pensamento para um número específico de tokens. Em Opus 4.6 e Sonnet 4.6, apenas `0` se aplica a menos que raciocínio adaptativo seja desativado. Exemplo: `export MAX_THINKING_TOKENS=10000` |

Para visualizar o processo de pensamento do Claude, pressione `Ctrl+O` para alternar o modo verboso e veja o raciocínio interno exibido como texto em itálico cinzento.

### Como funciona o pensamento estendido

Pensamento estendido controla quanto raciocínio interno Claude realiza antes de responder. Mais pensamento fornece mais espaço para explorar soluções, analisar casos extremos e autocorrigir erros.

**Com Opus 4.6 e Sonnet 4.6**, pensamento usa raciocínio adaptativo: o modelo aloca dinamicamente tokens de pensamento com base no [nível de esforço](/pt/model-config#adjust-effort-level) que você seleciona. Esta é a forma recomendada de ajustar a compensação entre velocidade e profundidade de raciocínio.

**Com modelos mais antigos**, pensamento usa um orçamento fixo de tokens extraído de sua alocação de saída. O orçamento varia por modelo; consulte [`MAX_THINKING_TOKENS`](/pt/env-vars) para limites por modelo. Você pode limitar o orçamento com essa variável de ambiente, ou desativar pensamento inteiramente via `/config` ou a alternância `Option+T`/`Alt+T`.

Em Opus 4.6 e Sonnet 4.6, [raciocínio adaptativo](/pt/model-config#adjust-effort-level) controla a profundidade de pensamento, então `MAX_THINKING_TOKENS` só se aplica quando definido como `0` para desativar pensamento, ou quando `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` reverte esses modelos para o orçamento fixo. Consulte [variáveis de ambiente](/pt/env-vars).

<Warning>
  Você é cobrado por todos os tokens de pensamento usados, mesmo quando resumos de pensamento são redatados. Em modo interativo, pensamento aparece como um stub recolhido por padrão. Defina `showThinkingSummaries: true` em `settings.json` para mostrar resumos completos.
</Warning>

***

## Retomar conversas anteriores

Ao iniciar Claude Code, você pode retomar uma sessão anterior:

* `claude --continue` continua a conversa mais recente no diretório atual
* `claude --resume` abre um seletor de conversa ou retoma por nome
* `claude --from-pr 123` retoma sessões vinculadas a uma pull request específica

De dentro de uma sessão ativa, use `/resume` para mudar para uma conversa diferente.

As sessões são armazenadas por diretório de projeto. O seletor `/resume` mostra sessões interativas do mesmo repositório git, incluindo worktrees. Sessões criadas por `claude -p` ou invocações SDK não aparecem no seletor, mas você ainda pode retomar uma passando seu ID de sessão diretamente para `claude --resume <session-id>`.

### Nomeie suas sessões

Dê nomes descritivos às sessões para encontrá-las mais tarde. Esta é uma prática recomendada ao trabalhar em múltiplas tarefas ou recursos.

<Steps>
  <Step title="Nomeie a sessão">
    Nomeie uma sessão na inicialização com `-n`:

    ```bash theme={null}
    claude -n auth-refactor
    ```

    Ou use `/rename` durante uma sessão, que também mostra o nome na barra de prompt:

    ```text theme={null}
    /rename auth-refactor
    ```

    Você também pode renomear qualquer sessão do seletor: execute `/resume`, navegue até uma sessão e pressione `R`.
  </Step>

  <Step title="Retome por nome mais tarde">
    Da linha de comando:

    ```bash theme={null}
    claude --resume auth-refactor
    ```

    Ou de dentro de uma sessão ativa:

    ```text theme={null}
    /resume auth-refactor
    ```
  </Step>
</Steps>

### Use o seletor de sessão

O comando `/resume` (ou `claude --resume` sem argumentos) abre um seletor de sessão interativo com estes recursos:

**Atalhos de teclado no seletor:**

| Atalho    | Ação                                              |
| :-------- | :------------------------------------------------ |
| `↑` / `↓` | Navegue entre sessões                             |
| `→` / `←` | Expanda ou recolha sessões agrupadas              |
| `Enter`   | Selecione e retome a sessão destacada             |
| `P`       | Visualize o conteúdo da sessão                    |
| `R`       | Renomeie a sessão destacada                       |
| `/`       | Pesquise para filtrar sessões                     |
| `A`       | Alterne entre diretório atual e todos os projetos |
| `B`       | Filtre para sessões do seu branch git atual       |
| `Esc`     | Saia do seletor ou modo de pesquisa               |

**Organização de sessão:**

O seletor exibe sessões com metadados úteis:

* Nome da sessão ou prompt inicial
* Tempo decorrido desde a última atividade
* Contagem de mensagens
* Branch git (se aplicável)

Sessões bifurcadas (criadas com `/branch`, `/rewind`, ou `--fork-session`) são agrupadas sob sua sessão raiz, facilitando encontrar conversas relacionadas.

<Tip>
  Dicas:

  * **Nomeie sessões cedo**: Use `/rename` ao iniciar trabalho em uma tarefa distinta—é muito mais fácil encontrar "payment-integration" do que "explain this function" mais tarde
  * Use `--continue` para acesso rápido à sua conversa mais recente no diretório atual
  * Use `--resume session-name` quando você sabe qual sessão precisa
  * Use `--resume` (sem um nome) quando você precisa navegar e selecionar
  * Para scripts, use `claude --continue --print "prompt"` para retomar em modo não interativo
  * Pressione `P` no seletor para visualizar uma sessão antes de retomá-la
  * A conversa retomada começa com o mesmo modelo e configuração do original

  Como funciona:

  1. **Armazenamento de Conversa**: Todas as conversas são automaticamente salvas localmente com seu histórico de mensagens completo
  2. **Desserialização de Mensagem**: Ao retomar, todo o histórico de mensagens é restaurado para manter contexto
  3. **Estado de Ferramenta**: O uso de ferramenta e resultados da conversa anterior são preservados
  4. **Restauração de Contexto**: A conversa retoma com todo o contexto anterior intacto
</Tip>

***

## Executar sessões paralelas de Claude Code com Git worktrees

Ao trabalhar em múltiplas tarefas ao mesmo tempo, você precisa que cada sessão do Claude tenha sua própria cópia da base de código para que as alterações não colidam. Git worktrees resolvem isso criando diretórios de trabalho separados que cada um tem seus próprios arquivos e branch, enquanto compartilham o mesmo histórico de repositório e conexões remotas. Isso significa que você pode ter Claude trabalhando em um recurso em um worktree enquanto corrige um bug em outro, sem que nenhuma sessão interfira com a outra.

Use a flag `--worktree` (`-w`) para criar um worktree isolado e iniciar Claude nele. O valor que você passa se torna o nome do diretório worktree e nome do branch:

```bash theme={null}
# Inicie Claude em um worktree nomeado "feature-auth"
# Cria .claude/worktrees/feature-auth/ com um novo branch
claude --worktree feature-auth

# Inicie outra sessão em um worktree separado
claude --worktree bugfix-123
```

Se você omitir o nome, Claude gera um automaticamente:

```bash theme={null}
# Auto-gera um nome como "bright-running-fox"
claude --worktree
```

Worktrees são criados em `<repo>/.claude/worktrees/<name>` e fazem branch a partir do branch remoto padrão, que é para onde `origin/HEAD` aponta. O branch worktree é nomeado `worktree-<name>`.

O branch base não é configurável através de um flag ou configuração do Claude Code. `origin/HEAD` é uma referência armazenada em seu diretório `.git` local que Git definiu uma vez quando você clonou. Se o branch padrão do repositório mudar mais tarde no GitHub ou GitLab, seu `origin/HEAD` local continua apontando para o antigo, e worktrees farão branch a partir daí. Para ressincronizar sua referência local com o que o remoto atualmente considera seu padrão:

```bash theme={null}
git remote set-head origin -a
```

Este é um comando Git padrão que apenas atualiza seu diretório `.git` local. Nada no servidor remoto muda. Se você quiser que worktrees façam base em um branch específico em vez do padrão do remoto, defina-o explicitamente com `git remote set-head origin your-branch-name`.

Para controle total sobre como worktrees são criados, incluindo escolher uma base diferente por invocação, configure um [hook WorktreeCreate](/pt/hooks#worktreecreate). O hook substitui a lógica padrão `git worktree` do Claude Code inteiramente, para que você possa buscar e fazer branch a partir de qualquer ref que você precise.

Você também pode pedir ao Claude para "work in a worktree" ou "start a worktree" durante uma sessão, e ele criará um automaticamente.

### Worktrees de subagent

Subagents também podem usar isolamento de worktree para trabalhar em paralelo sem conflitos. Peça ao Claude para "use worktrees for your agents" ou configure em um [subagent personalizado](/pt/sub-agents#supported-frontmatter-fields) adicionando `isolation: worktree` ao frontmatter do agente. Cada subagent obtém seu próprio worktree que é automaticamente limpo quando o subagent termina sem alterações.

### Limpeza de worktree

Quando você sai de uma sessão de worktree, Claude lida com limpeza com base em se você fez alterações:

* **Sem alterações**: o worktree e seu branch são removidos automaticamente
* **Alterações ou commits existem**: Claude o solicita para manter ou remover o worktree. Manter preserva o diretório e branch para que você possa retornar mais tarde. Remover exclui o diretório worktree e seu branch, descartando todas as alterações não confirmadas e commits

Para limpar worktrees fora de uma sessão do Claude, use [gerenciamento manual de worktree](#manage-worktrees-manually).

<Tip>
  Adicione `.claude/worktrees/` ao seu `.gitignore` para evitar que o conteúdo do worktree apareça como arquivos não rastreados em seu repositório principal.
</Tip>

### Copiar arquivos gitignored para worktrees

Git worktrees são checkouts frescos, então eles não incluem arquivos não rastreados como `.env` ou `.env.local` do seu repositório principal. Para copiar automaticamente esses arquivos quando Claude cria um worktree, adicione um arquivo `.worktreeinclude` à raiz do seu projeto.

O arquivo usa sintaxe `.gitignore` para listar quais arquivos copiar. Apenas arquivos que correspondem a um padrão e também são gitignored são copiados, então arquivos rastreados nunca são duplicados.

```text .worktreeinclude theme={null}
.env
.env.local
config/secrets.json
```

Isso se aplica a worktrees criados com `--worktree`, worktrees de subagent e sessões paralelas no [aplicativo desktop](/pt/desktop#work-in-parallel-with-sessions).

### Gerenciar worktrees manualmente

Para mais controle sobre localização de worktree e configuração de branch, crie worktrees com Git diretamente. Isso é útil quando você precisa fazer checkout de um branch existente específico ou colocar o worktree fora do repositório.

```bash theme={null}
# Crie um worktree com um novo branch
git worktree add ../project-feature-a -b feature-a

# Crie um worktree com um branch existente
git worktree add ../project-bugfix bugfix-123

# Inicie Claude no worktree
cd ../project-feature-a && claude

# Limpe quando terminar
git worktree list
git worktree remove ../project-feature-a
```

Saiba mais na [documentação oficial de Git worktree](https://git-scm.com/docs/git-worktree).

<Tip>
  Lembre-se de inicializar seu ambiente de desenvolvimento em cada novo worktree de acordo com seu projeto. Dependendo de sua stack, isso pode incluir executar instalação de dependência (`npm install`, `yarn`), configurar ambientes virtuais ou seguir o processo de configuração padrão do seu projeto.
</Tip>

### Controle de versão não-git

Isolamento de worktree funciona com git por padrão. Para outros sistemas de controle de versão como SVN, Perforce ou Mercurial, configure [hooks WorktreeCreate e WorktreeRemove](/pt/hooks#worktreecreate) para fornecer lógica personalizada de criação e limpeza de worktree. Quando configurados, esses hooks substituem o comportamento padrão do git quando você usa `--worktree`, então [`.worktreeinclude`](#copy-gitignored-files-to-worktrees) não é processado. Copie quaisquer arquivos de configuração local dentro de seu script de hook em vez disso.

Para coordenação automatizada de sessões paralelas com tarefas compartilhadas e mensagens, consulte [equipes de agentes](/pt/agent-teams).

***

## Obtenha notificações quando Claude precisa de sua atenção

Quando você inicia uma tarefa de longa duração e muda para outra janela, você pode configurar notificações de desktop para saber quando Claude termina ou precisa de sua entrada. Isso usa o evento de hook `Notification` [hook event](/pt/hooks-guide#get-notified-when-claude-needs-input), que dispara sempre que Claude está esperando permissão, ocioso e pronto para um novo prompt, ou completando autenticação.

<Steps>
  <Step title="Adicione o hook às suas configurações">
    Abra `~/.claude/settings.json` e adicione um hook `Notification` que chama o comando de notificação nativa da sua plataforma:

    <Tabs>
      <Tab title="macOS">
        ```json theme={null}
        {
          "hooks": {
            "Notification": [
              {
                "matcher": "",
                "hooks": [
                  {
                    "type": "command",
                    "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
                  }
                ]
              }
            ]
          }
        }
        ```
      </Tab>

      <Tab title="Linux">
        ```json theme={null}
        {
          "hooks": {
            "Notification": [
              {
                "matcher": "",
                "hooks": [
                  {
                    "type": "command",
                    "command": "notify-send 'Claude Code' 'Claude Code needs your attention'"
                  }
                ]
              }
            ]
          }
        }
        ```
      </Tab>

      <Tab title="Windows">
        ```json theme={null}
        {
          "hooks": {
            "Notification": [
              {
                "matcher": "",
                "hooks": [
                  {
                    "type": "command",
                    "command": "powershell.exe -Command \"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')\""
                  }
                ]
              }
            ]
          }
        }
        ```
      </Tab>
    </Tabs>

    Se seu arquivo de configurações já tiver uma chave `hooks`, mescle a entrada `Notification` nela em vez de sobrescrever. Você também pode pedir ao Claude para escrever o hook para você descrevendo o que você quer no CLI.
  </Step>

  <Step title="Opcionalmente, estreite o matcher">
    Por padrão, o hook dispara em todos os tipos de notificação. Para disparar apenas para eventos específicos, defina o campo `matcher` para um destes valores:

    | Matcher              | Dispara quando                                      |
    | :------------------- | :-------------------------------------------------- |
    | `permission_prompt`  | Claude precisa que você aprove um uso de ferramenta |
    | `idle_prompt`        | Claude terminou e está esperando seu próximo prompt |
    | `auth_success`       | Autenticação completa                               |
    | `elicitation_dialog` | Claude está fazendo uma pergunta                    |
  </Step>

  <Step title="Verifique o hook">
    Digite `/hooks` e selecione `Notification` para confirmar que o hook aparece. Selecioná-lo mostra o comando que será executado. Para testá-lo de ponta a ponta, peça ao Claude para executar um comando que requer permissão e mude para longe do terminal, ou peça ao Claude para disparar uma notificação diretamente.
  </Step>
</Steps>

Para o esquema de evento completo e tipos de notificação, consulte a [referência de Notificação](/pt/hooks#notification).

***

## Usar Claude como um utilitário estilo unix

### Adicione Claude ao seu processo de verificação

Suponha que você queira usar Claude Code como um linter ou revisor de código.

**Adicione Claude ao seu script de compilação:**

```json theme={null}
// package.json
{
    ...
    "scripts": {
        ...
        "lint:claude": "claude -p 'you are a linter. please look at the changes vs. main and report any issues related to typos. report the filename and line number on one line, and a description of the issue on the second line. do not return any other text.'"
    }
}
```

<Tip>
  Dicas:

  * Use Claude para revisão de código automatizada em seu pipeline CI/CD
  * Personalize o prompt para verificar problemas específicos relevantes ao seu projeto
  * Considere criar múltiplos scripts para diferentes tipos de verificação
</Tip>

### Pipe in, pipe out

Suponha que você queira canalizar dados para Claude e obter dados de volta em um formato estruturado.

**Canalize dados através do Claude:**

```bash theme={null}
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

<Tip>
  Dicas:

  * Use pipes para integrar Claude em scripts shell existentes
  * Combine com outras ferramentas Unix para fluxos de trabalho poderosos
  * Considere usar `--output-format` para saída estruturada
</Tip>

### Controlar formato de saída

Suponha que você precise da saída do Claude em um formato específico, especialmente ao integrar Claude Code em scripts ou outras ferramentas.

<Steps>
  <Step title="Use formato de texto (padrão)">
    ```bash theme={null}
    cat data.txt | claude -p 'summarize this data' --output-format text > summary.txt
    ```

    Isso produz apenas a resposta de texto simples do Claude (comportamento padrão).
  </Step>

  <Step title="Use formato JSON">
    ```bash theme={null}
    cat code.py | claude -p 'analyze this code for bugs' --output-format json > analysis.json
    ```

    Isso produz um array JSON de mensagens com metadados incluindo custo e duração.
  </Step>

  <Step title="Use formato JSON de streaming">
    ```bash theme={null}
    cat log.txt | claude -p 'parse this log file for errors' --output-format stream-json
    ```

    Isso produz uma série de objetos JSON em tempo real conforme Claude processa a solicitação. Cada mensagem é um objeto JSON válido, mas a saída inteira não é JSON válido se concatenado.
  </Step>
</Steps>

<Tip>
  Dicas:

  * Use `--output-format text` para integrações simples onde você apenas precisa da resposta do Claude
  * Use `--output-format json` quando você precisa do log de conversa completo
  * Use `--output-format stream-json` para saída em tempo real de cada turno de conversa
</Tip>

***

## Executar Claude em um cronograma

Suponha que você queira que Claude lide com uma tarefa automaticamente em uma base recorrente, como revisar PRs abertas todas as manhãs, auditar dependências semanalmente ou verificar falhas de CI durante a noite.

Escolha uma opção de agendamento com base em onde você quer que a tarefa seja executada:

| Opção                                                                | Onde é executado                         | Melhor para                                                                                                                                        |
| :------------------------------------------------------------------- | :--------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Tarefas agendadas na nuvem](/pt/web-scheduled-tasks)                | Infraestrutura gerenciada pela Anthropic | Tarefas que devem ser executadas mesmo quando seu computador está desligado. Configure em [claude.ai/code](https://claude.ai/code).                |
| [Tarefas agendadas no desktop](/pt/desktop#schedule-recurring-tasks) | Sua máquina, via aplicativo desktop      | Tarefas que precisam de acesso direto a arquivos locais, ferramentas ou alterações não confirmadas.                                                |
| [GitHub Actions](/pt/github-actions)                                 | Seu pipeline de CI                       | Tarefas vinculadas a eventos de repositório como PRs abertos, ou cronogramas cron que devem viver junto com sua configuração de fluxo de trabalho. |
| [`/loop`](/pt/scheduled-tasks)                                       | A sessão CLI atual                       | Polling rápido enquanto uma sessão está aberta. As tarefas são canceladas quando você sai.                                                         |

<Tip>
  Ao escrever prompts para tarefas agendadas, seja explícito sobre o que o sucesso parece e o que fazer com os resultados. A tarefa é executada autonomamente, então não pode fazer perguntas de esclarecimento. Por exemplo: "Review open PRs labeled `needs-review`, leave inline comments on any issues, and post a summary in the `#eng-reviews` Slack channel."
</Tip>

***

## Pergunte ao Claude sobre suas capacidades

Claude tem acesso integrado à sua documentação e pode responder perguntas sobre seus próprios recursos e limitações.

### Perguntas de exemplo

```text theme={null}
can Claude Code create pull requests?
```

```text theme={null}
how does Claude Code handle permissions?
```

```text theme={null}
what skills are available?
```

```text theme={null}
how do I use MCP with Claude Code?
```

```text theme={null}
how do I configure Claude Code for Amazon Bedrock?
```

```text theme={null}
what are the limitations of Claude Code?
```

<Note>
  Claude fornece respostas baseadas em documentação para essas perguntas. Para exemplos executáveis e demonstrações práticas, consulte as seções de fluxo de trabalho específicas acima.
</Note>

<Tip>
  Dicas:

  * Claude sempre tem acesso à documentação mais recente do Claude Code, independentemente da versão que você está usando
  * Faça perguntas específicas para obter respostas detalhadas
  * Claude pode explicar recursos complexos como integração MCP, configurações empresariais e fluxos de trabalho avançados
</Tip>

***

## Próximos passos

<CardGroup cols={2}>
  <Card title="Melhores práticas" icon="lightbulb" href="/pt/best-practices">
    Padrões para aproveitar ao máximo Claude Code
  </Card>

  <Card title="Como Claude Code funciona" icon="gear" href="/pt/how-claude-code-works">
    Entenda o loop agentic e gerenciamento de contexto
  </Card>

  <Card title="Estender Claude Code" icon="puzzle-piece" href="/pt/features-overview">
    Adicione skills, hooks, MCP, subagents e plugins
  </Card>

  <Card title="Implementação de referência" icon="code" href="https://github.com/anthropics/claude-code/tree/main/.devcontainer">
    Clone a implementação de referência do contêiner de desenvolvimento
  </Card>
</CardGroup>
