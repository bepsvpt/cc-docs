> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Como Claude Code funciona

> Entenda o loop agentic, as ferramentas integradas e como Claude Code interage com seu projeto.

Claude Code é um assistente agentic que funciona em seu terminal. Embora se destaque em codificação, pode ajudar com qualquer coisa que você possa fazer a partir da linha de comando: escrever documentação, executar compilações, pesquisar arquivos, pesquisar tópicos e muito mais.

Este guia cobre a arquitetura principal, capacidades integradas e [dicas para trabalhar efetivamente](#work-effectively-with-claude-code). Para instruções passo a passo, consulte [Fluxos de trabalho comuns](/pt/common-workflows). Para recursos de extensibilidade como skills, MCP e hooks, consulte [Estender Claude Code](/pt/features-overview).

## O loop agentic

Quando você dá uma tarefa a Claude, ele trabalha através de três fases: **reunir contexto**, **tomar ação** e **verificar resultados**. Essas fases se misturam. Claude usa ferramentas ao longo do processo, seja pesquisando arquivos para entender seu código, editando para fazer alterações ou executando testes para verificar seu trabalho.

<img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/agentic-loop.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=5f1827dec8539f38adee90ead3a85a38" alt="O loop agentic: Seu prompt leva Claude a reunir contexto, tomar ação, verificar resultados e repetir até que a tarefa seja concluída. Você pode interromper em qualquer ponto." width="720" height="280" data-path="images/agentic-loop.svg" />

O loop se adapta ao que você pede. Uma pergunta sobre sua base de código pode precisar apenas de coleta de contexto. Uma correção de bug passa por todas as três fases repetidamente. Uma refatoração pode envolver verificação extensiva. Claude decide o que cada etapa requer com base no que aprendeu da etapa anterior, encadeando dezenas de ações e se autocorrigindo ao longo do caminho.

Você também faz parte deste loop. Você pode interromper em qualquer ponto para orientar Claude em uma direção diferente, fornecer contexto adicional ou pedir que tente uma abordagem diferente. Claude trabalha autonomamente, mas permanece responsivo à sua entrada.

O loop agentic é alimentado por dois componentes: [modelos](#models) que raciocinam e [ferramentas](#tools) que agem. Claude Code serve como o **agentic harness** ao redor de Claude: fornece as ferramentas, gerenciamento de contexto e ambiente de execução que transformam um modelo de linguagem em um agente de codificação capaz.

### Models

Claude Code usa modelos Claude para entender seu código e raciocinar sobre tarefas. Claude pode ler código em qualquer linguagem, entender como os componentes se conectam e descobrir o que precisa mudar para alcançar seu objetivo. Para tarefas complexas, ele divide o trabalho em etapas, as executa e se ajusta com base no que aprende.

[Múltiplos modelos](/pt/model-config) estão disponíveis com diferentes compensações. Sonnet lida bem com a maioria das tarefas de codificação. Opus fornece raciocínio mais forte para decisões arquitetônicas complexas. Mude com `/model` durante uma sessão ou comece com `claude --model <name>`.

Quando este guia diz "Claude escolhe" ou "Claude decide", é o modelo fazendo o raciocínio.

### Tools

Ferramentas são o que tornam Claude Code agentic. Sem ferramentas, Claude pode apenas responder com texto. Com ferramentas, Claude pode agir: ler seu código, editar arquivos, executar comandos, pesquisar a web e interagir com serviços externos. Cada uso de ferramenta retorna informações que alimentam o loop, informando a próxima decisão de Claude.

As ferramentas integradas geralmente se enquadram em cinco categorias, cada uma representando um tipo diferente de agência.

| Categoria                  | O que Claude pode fazer                                                                                                                                                    |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Operações de arquivo**   | Ler arquivos, editar código, criar novos arquivos, renomear e reorganizar                                                                                                  |
| **Pesquisa**               | Encontrar arquivos por padrão, pesquisar conteúdo com regex, explorar bases de código                                                                                      |
| **Execução**               | Executar comandos shell, iniciar servidores, executar testes, usar git                                                                                                     |
| **Web**                    | Pesquisar a web, buscar documentação, procurar mensagens de erro                                                                                                           |
| **Inteligência de código** | Ver erros de tipo e avisos após edições, pular para definições, encontrar referências (requer [plugins de inteligência de código](/pt/discover-plugins#code-intelligence)) |

Essas são as capacidades principais. Claude também tem ferramentas para gerar subagents, fazer perguntas a você e outras tarefas de orquestração. Consulte [Ferramentas disponíveis para Claude](/pt/tools-reference) para a lista completa.

Claude escolhe quais ferramentas usar com base em seu prompt e no que aprende ao longo do caminho. Quando você diz "corrigir os testes falhando", Claude pode:

1. Executar o conjunto de testes para ver o que está falhando
2. Ler a saída de erro
3. Pesquisar os arquivos de código-fonte relevantes
4. Ler esses arquivos para entender o código
5. Editar os arquivos para corrigir o problema
6. Executar os testes novamente para verificar

Cada uso de ferramenta dá a Claude novas informações que informam a próxima etapa. Este é o loop agentic em ação.

**Estendendo as capacidades base:** As ferramentas integradas são a base. Você pode estender o que Claude sabe com [skills](/pt/skills), conectar a serviços externos com [MCP](/pt/mcp), automatizar fluxos de trabalho com [hooks](/pt/hooks) e delegar tarefas a [subagents](/pt/sub-agents). Essas extensões formam uma camada sobre o loop agentic principal. Consulte [Estender Claude Code](/pt/features-overview) para orientação sobre como escolher a extensão certa para suas necessidades.

## O que Claude pode acessar

Este guia se concentra no terminal. Claude Code também funciona em [VS Code](/pt/vs-code), [IDEs JetBrains](/pt/jetbrains) e outros ambientes.

Quando você executa `claude` em um diretório, Claude Code ganha acesso a:

* **Seu projeto.** Arquivos em seu diretório e subdiretórios, além de arquivos em outro lugar com sua permissão.
* **Seu terminal.** Qualquer comando que você possa executar: ferramentas de compilação, git, gerenciadores de pacotes, utilitários do sistema, scripts. Se você pode fazer a partir da linha de comando, Claude também pode.
* **Seu estado git.** Branch atual, alterações não confirmadas e histórico de commits recentes.
* **Seu [CLAUDE.md](/pt/memory).** Um arquivo markdown onde você armazena instruções específicas do projeto, convenções e contexto que Claude deve conhecer a cada sessão.
* **[Auto memory](/pt/memory#auto-memory).** Aprendizados que Claude salva automaticamente conforme você trabalha, como padrões de projeto e suas preferências. As primeiras 200 linhas ou 25KB de MEMORY.md, o que vier primeiro, são carregadas no início de cada sessão.
* **Extensões que você configura.** [Servidores MCP](/pt/mcp) para serviços externos, [skills](/pt/skills) para fluxos de trabalho, [subagents](/pt/sub-agents) para trabalho delegado e [Claude no Chrome](/pt/chrome) para interação com navegador.

Como Claude vê seu projeto inteiro, pode trabalhar em todo ele. Quando você pede a Claude para "corrigir o bug de autenticação", ele pesquisa arquivos relevantes, lê múltiplos arquivos para entender o contexto, faz edições coordenadas entre eles, executa testes para verificar a correção e confirma as alterações se você pedir. Isso é diferente de assistentes de código inline que apenas veem o arquivo atual.

## Ambientes e interfaces

O loop agentic, ferramentas e capacidades descritos acima são os mesmos em qualquer lugar que você use Claude Code. O que muda é onde o código é executado e como você interage com ele.

### Ambientes de execução

Claude Code funciona em três ambientes, cada um com diferentes compensações para onde seu código é executado.

| Ambiente           | Onde o código é executado                        | Caso de uso                                                            |
| ------------------ | ------------------------------------------------ | ---------------------------------------------------------------------- |
| **Local**          | Sua máquina                                      | Padrão. Acesso completo aos seus arquivos, ferramentas e ambiente      |
| **Cloud**          | VMs gerenciadas pela Anthropic                   | Delegar tarefas, trabalhar em repositórios que você não tem localmente |
| **Remote Control** | Sua máquina, controlada a partir de um navegador | Use a interface web mantendo tudo local                                |

### Interfaces

Você pode acessar Claude Code através do terminal, do [aplicativo desktop](/pt/desktop), [extensões IDE](/pt/vs-code), [claude.ai/code](https://claude.ai/code), [Remote Control](/pt/remote-control), [Slack](/pt/slack) e [pipelines CI/CD](/pt/github-actions). A interface determina como você vê e interage com Claude, mas o loop agentic subjacente é idêntico. Consulte [Use Claude Code em qualquer lugar](/pt/overview#use-claude-code-everywhere) para a lista completa.

## Trabalhe com sessões

Claude Code salva sua conversa localmente conforme você trabalha. Cada mensagem, uso de ferramenta e resultado é armazenado, o que permite [retroceder](#undo-changes-with-checkpoints), [retomar e bifurcar](#resume-or-fork-sessions) sessões. Antes de Claude fazer alterações de código, ele também tira um snapshot dos arquivos afetados para que você possa reverter se necessário.

**As sessões são independentes.** Cada nova sessão começa com uma janela de contexto fresca, sem o histórico de conversa de sessões anteriores. Claude pode persistir aprendizados entre sessões usando [auto memory](/pt/memory#auto-memory), e você pode adicionar suas próprias instruções persistentes em [CLAUDE.md](/pt/memory).

### Trabalhe entre branches

Cada conversa de Claude Code é uma sessão vinculada ao seu diretório atual. Quando você retoma, você só vê sessões desse diretório.

Claude vê os arquivos do seu branch atual. Quando você muda de branch, Claude vê os arquivos do novo branch, mas seu histórico de conversa permanece o mesmo. Claude se lembra do que você discutiu mesmo após mudar de branch.

Como as sessões estão vinculadas a diretórios, você pode executar sessões paralelas de Claude Code usando [git worktrees](/pt/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees), que criam diretórios separados para branches individuais.

### Retome ou bifurque sessões

Quando você retoma uma sessão com `claude --continue` ou `claude --resume`, você continua de onde parou usando o mesmo ID de sessão. Novas mensagens são anexadas à conversa existente. Seu histórico de conversa completo é restaurado, mas as permissões com escopo de sessão não são. Você precisará re-aprovar essas.

<img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/session-continuity.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=fa41d12bfb57579cabfeece907151d30" alt="Continuidade de sessão: retomar continua a mesma sessão, bifurcar cria um novo branch com um novo ID." width="560" height="280" data-path="images/session-continuity.svg" />

Para ramificar e tentar uma abordagem diferente sem afetar a sessão original, use a flag `--fork-session`:

```bash theme={null}
claude --continue --fork-session
```

Isso cria um novo ID de sessão enquanto preserva o histórico de conversa até esse ponto. A sessão original permanece inalterada. Como retomar, sessões bifurcadas não herdam permissões com escopo de sessão.

**Mesma sessão em múltiplos terminais**: Se você retomar a mesma sessão em múltiplos terminais, ambos os terminais escrevem no mesmo arquivo de sessão. Mensagens de ambos ficam intercaladas, como duas pessoas escrevendo no mesmo caderno. Nada se corrompe, mas a conversa fica confusa. Cada terminal vê apenas suas próprias mensagens durante a sessão, mas se você retomar essa sessão mais tarde, verá tudo intercalado. Para trabalho paralelo a partir do mesmo ponto de partida, use `--fork-session` para dar a cada terminal sua própria sessão limpa.

### A janela de contexto

A janela de contexto de Claude contém seu histórico de conversa, conteúdo de arquivos, saídas de comando, [CLAUDE.md](/pt/memory), [auto memory](/pt/memory#auto-memory), skills carregadas e instruções do sistema. Conforme você trabalha, o contexto se enche. Claude compacta automaticamente, mas instruções do início da conversa podem ser perdidas. Coloque regras persistentes em CLAUDE.md e execute `/context` para ver o que está usando espaço.

Para um passo a passo interativo do que é carregado e quando, consulte [Explore a janela de contexto](/pt/context-window).

#### Quando o contexto se enche

Claude Code gerencia o contexto automaticamente conforme você se aproxima do limite. Ele limpa saídas de ferramentas mais antigas primeiro, depois resume a conversa se necessário. Suas solicitações e trechos de código-chave são preservados; instruções detalhadas do início da conversa podem ser perdidas. Coloque regras persistentes em CLAUDE.md em vez de confiar no histórico de conversa.

Para controlar o que é preservado durante a compactação, adicione uma seção "Compact Instructions" a CLAUDE.md ou execute `/compact` com um foco (como `/compact focus on the API changes`).

Execute `/context` para ver o que está usando espaço. Definições de ferramentas MCP são adiadas por padrão e carregadas sob demanda via [busca de ferramentas](/pt/mcp#scale-with-mcp-tool-search), então apenas nomes de ferramentas consomem contexto até Claude usar uma ferramenta específica. Execute `/mcp` para verificar custos por servidor.

#### Gerencie contexto com skills e subagents

Além da compactação, você pode usar outros recursos para controlar o que é carregado no contexto.

[Skills](/pt/skills) carregam sob demanda. Claude vê descrições de skills no início da sessão, mas o conteúdo completo só carrega quando uma skill é usada. Para skills que você invoca manualmente, defina `disable-model-invocation: true` para manter descrições fora do contexto até que você precise delas.

[Subagents](/pt/sub-agents) obtêm seu próprio contexto fresco, completamente separado de sua conversa principal. Seu trabalho não incha seu contexto. Quando terminado, eles retornam um resumo. Esse isolamento é por que subagents ajudam em sessões longas.

Consulte [custos de contexto](/pt/features-overview#understand-context-costs) para o que cada recurso custa e [reduzir uso de tokens](/pt/costs#reduce-token-usage) para dicas sobre como gerenciar contexto.

## Fique seguro com checkpoints e permissões

Claude tem dois mecanismos de segurança: checkpoints permitem que você desfaça alterações de arquivo e permissões controlam o que Claude pode fazer sem perguntar.

### Desfaça alterações com checkpoints

**Cada edição de arquivo é reversível.** Antes de Claude editar qualquer arquivo, ele tira um snapshot do conteúdo atual. Se algo der errado, pressione `Esc` duas vezes para retroceder a um estado anterior ou peça a Claude para desfazer.

Checkpoints são locais para sua sessão, separados do git. Eles cobrem apenas alterações de arquivo. Ações que afetam sistemas remotos (bancos de dados, APIs, implantações) não podem ser checkpointed, é por isso que Claude pergunta antes de executar comandos com efeitos colaterais externos.

### Controle o que Claude pode fazer

Pressione `Shift+Tab` para percorrer os modos de permissão:

* **Padrão**: Claude pergunta antes de edições de arquivo e comandos shell
* **Auto-aceitar edições**: Claude edita arquivos sem perguntar, ainda pergunta por comandos
* **Plan Mode**: Claude usa apenas ferramentas somente leitura, criando um plano que você pode aprovar antes da execução
* **Auto mode**: Claude avalia todas as ações com verificações de segurança em segundo plano. Atualmente uma visualização de pesquisa

Você também pode permitir comandos específicos em `.claude/settings.json` para que Claude não pergunte cada vez. Isso é útil para comandos confiáveis como `npm test` ou `git status`. As configurações podem ser escopo de políticas em toda a organização até preferências pessoais. Consulte [Permissões](/pt/permissions) para detalhes.

***

## Trabalhe efetivamente com Claude Code

Essas dicas ajudam você a obter melhores resultados de Claude Code.

### Peça ajuda a Claude Code

Claude Code pode ensinar você como usá-lo. Faça perguntas como "como configuro hooks?" ou "qual é a melhor maneira de estruturar meu CLAUDE.md?" e Claude explicará.

Comandos integrados também o guiam através da configuração:

* `/init` o guia através da criação de um CLAUDE.md para seu projeto
* `/agents` ajuda você a configurar subagents personalizados
* `/doctor` diagnostica problemas comuns com sua instalação

### É uma conversa

Claude Code é conversacional. Você não precisa de prompts perfeitos. Comece com o que você quer, depois refine:

```text theme={null}
Corrigir o bug de login
```

\[Claude investiga, tenta algo]

```text theme={null}
Isso não é bem certo. O problema está no tratamento de sessão.
```

\[Claude ajusta a abordagem]

Quando a primeira tentativa não está certa, você não começa do zero. Você itera.

#### Interrompa e oriente

Você pode interromper Claude em qualquer ponto. Se ele está indo pelo caminho errado, apenas digite sua correção e pressione Enter. Claude parará o que está fazendo e ajustará sua abordagem com base em sua entrada. Você não precisa esperar que termine ou começar do zero.

### Seja específico desde o início

Quanto mais preciso seu prompt inicial, menos correções você precisará. Referencie arquivos específicos, mencione restrições e aponte para padrões de exemplo.

```text theme={null}
O fluxo de checkout está quebrado para usuários com cartões expirados.
Verifique src/payments/ para o problema, especialmente atualização de token.
Escreva um teste falhando primeiro, depois corrija.
```

Prompts vagos funcionam, mas você gastará mais tempo orientando. Prompts específicos como o acima geralmente têm sucesso na primeira tentativa.

### Dê a Claude algo para verificar

Claude funciona melhor quando pode verificar seu próprio trabalho. Inclua casos de teste, cole screenshots da UI esperada ou defina a saída que você quer.

```text theme={null}
Implementar validateEmail. Casos de teste: 'user@example.com' → true,
'invalid' → false, 'user@.com' → false. Execute os testes depois.
```

Para trabalho visual, cole um screenshot do design e peça a Claude para comparar sua implementação com ele.

### Explore antes de implementar

Para problemas complexos, separe pesquisa de codificação. Use plan mode (`Shift+Tab` duas vezes) para analisar a base de código primeiro:

```text theme={null}
Leia src/auth/ e entenda como lidamos com sessões.
Depois crie um plano para adicionar suporte OAuth.
```

Revise o plano, refine-o através de conversa, depois deixe Claude implementar. Essa abordagem de duas fases produz melhores resultados do que pular direto para código.

### Delegue, não dite

Pense em delegar a um colega capaz. Dê contexto e direção, depois confie em Claude para descobrir os detalhes:

```text theme={null}
O fluxo de checkout está quebrado para usuários com cartões expirados.
O código relevante está em src/payments/. Você pode investigar e corrigir?
```

Você não precisa especificar quais arquivos ler ou quais comandos executar. Claude descobre isso.

## O que vem a seguir

<CardGroup cols={2}>
  <Card title="Estender com recursos" icon="puzzle-piece" href="/pt/features-overview">
    Adicione Skills, conexões MCP e comandos personalizados
  </Card>

  <Card title="Fluxos de trabalho comuns" icon="graduation-cap" href="/pt/common-workflows">
    Guias passo a passo para tarefas típicas
  </Card>
</CardGroup>
