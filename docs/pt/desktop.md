> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Aplicativo Desktop

> Aproveite ao máximo o Claude Code Desktop: sessões paralelas com isolamento Git, layout de painel com arrastar e soltar, terminal integrado e editor de arquivo, chats laterais, computer use, Dispatch sessions do seu telefone, revisão visual de diff, visualizações de aplicativos, monitoramento de PR, conectores e configuração corporativa.

O aplicativo Claude Desktop tem três abas: **Chat** para conversas, **Cowork** para [Dispatch e trabalho agentic mais longo](https://claude.com/product/cowork), e **Code** para desenvolvimento de software. Esta página é a referência para a aba Code.

<CardGroup cols={2}>
  <Card title="Download for macOS" icon="apple" href="https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs">
    Universal build for Intel and Apple Silicon
  </Card>

  <Card title="Download for Windows" icon="windows" href="https://claude.ai/api/desktop/win32/x64/setup/latest/redirect?utm_source=claude_code&utm_medium=docs">
    For x64 processors
  </Card>
</CardGroup>

For Windows ARM64, download the [ARM64 installer](https://claude.ai/api/desktop/win32/arm64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs). The desktop app is not available on Linux; use the [CLI](/en/quickstart) instead.

Após instalar, inicie Claude, faça login e clique na aba **Code**. A primeira vez que você a abrir no Windows, você precisa ter o [Git for Windows](https://git-scm.com/downloads/win) instalado; reinicie o aplicativo após instalá-lo. Para um passo a passo de sua primeira sessão, consulte o [guia de primeiros passos](/pt/desktop-quickstart).

Na aba Code, cada conversa é uma **sessão**: ela tem seu próprio histórico de chat, pasta de projeto e alterações de código, independente de qualquer outra sessão. A barra lateral lista suas sessões e permite que você execute várias em paralelo. Dentro de uma sessão você pode:

* [Revisar e comentar em diffs](#review-changes-with-diff-view), depois [monitorar o PR resultante através do CI](#monitor-pull-request-status)
* [Visualizar seu aplicativo em execução](#preview-your-app) em um navegador integrado enquanto Claude verifica suas próprias alterações
* [Organizar painéis](#arrange-your-workspace) para o chat, diff, visualização, terminal e editor de arquivo lado a lado
* Fazer uma [pergunta lateral](#ask-a-side-question-without-derailing-the-session) que usa o contexto da sessão sem desviá-la
* [Conectar ferramentas externas](#connect-external-tools) como GitHub, Slack e Linear
* Permitir que Claude [abra aplicativos e controle sua tela](#let-claude-use-your-computer)
* Executar em sua máquina, na [nuvem](#run-long-running-tasks-remotely), ou sobre [SSH](#ssh-sessions)

Para [trabalho recorrente agendado](/pt/desktop-scheduled-tasks), [atalhos de teclado](#keyboard-shortcuts), ou [envio de tarefas do seu telefone](#sessions-from-dispatch), consulte as páginas e seções vinculadas. Se você já usa o CLI baseado em terminal, consulte a [comparação CLI](#coming-from-the-cli) para ver o que é transferido.

## Iniciar uma sessão

Antes de enviar sua primeira mensagem, configure quatro coisas na área de prompt:

* **Ambiente**: escolha onde Claude é executado. Selecione **Local** para sua máquina, **Remote** para sessões em nuvem hospedadas pela Anthropic, ou uma [**conexão SSH**](#ssh-sessions) para uma máquina remota que você gerencia. Veja [configuração de ambiente](#environment-configuration).
* **Pasta do projeto**: selecione a pasta ou repositório em que Claude trabalha. Para sessões remotas, você pode adicionar [múltiplos repositórios](#run-long-running-tasks-remotely).
* **Modelo**: escolha um [modelo](/pt/model-config#available-models) no menu suspenso ao lado do botão enviar. Você pode alterar isso durante a sessão.
* **Modo de permissão**: escolha quanto de autonomia Claude tem no [seletor de modo](#choose-a-permission-mode). Você pode alterar isso durante a sessão.

Digite sua tarefa e pressione **Enter** para começar. Cada sessão rastreia seu próprio contexto e alterações independentemente.

## Trabalhar com código

Dê a Claude o contexto certo, controle quanto ele faz por conta própria e revise o que ele alterou.

### Use a caixa de prompt

Digite o que você quer que Claude faça e pressione **Enter** para enviar. Claude lê seus arquivos de projeto, faz alterações e executa comandos com base no seu [modo de permissão](#choose-a-permission-mode). Você pode interromper Claude a qualquer momento: clique no botão parar ou digite sua correção e pressione **Enter**. Claude para o que está fazendo e se ajusta com base em sua entrada.

O botão **+** ao lado da caixa de prompt oferece acesso a anexos de arquivo, [skills](#use-skills), [conectores](#connect-external-tools) e [plugins](#install-plugins).

### Adicionar arquivos e contexto aos prompts

A caixa de prompt suporta duas maneiras de trazer contexto externo:

* **@mention de arquivos**: digite `@` seguido de um nome de arquivo para adicionar um arquivo ao contexto da conversa. Claude pode então ler e referenciar esse arquivo. @mention não está disponível em sessões remotas.
* **Anexar arquivos**: anexe imagens, PDFs e outros arquivos ao seu prompt usando o botão de anexo, ou arraste e solte arquivos diretamente no prompt. Isso é útil para compartilhar capturas de tela de bugs, mockups de design ou documentos de referência.

### Escolher um modo de permissão

Os modos de permissão controlam quanto de autonomia Claude tem durante uma sessão: se ele pergunta antes de editar arquivos, executar comandos ou ambos. Você pode alternar modos a qualquer momento usando o seletor de modo ao lado do botão enviar. Comece com Ask permissions para ver exatamente o que Claude faz, depois mude para Auto accept edits ou Plan mode conforme você fica confortável.

| Modo                   | Chave de configuração | Comportamento                                                                                                                                                                                                                                                                                  |
| ---------------------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ask permissions**    | `default`             | Claude pergunta antes de editar arquivos ou executar comandos. Você vê um diff e pode aceitar ou rejeitar cada alteração. Recomendado para novos usuários.                                                                                                                                     |
| **Auto accept edits**  | `acceptEdits`         | Claude aceita automaticamente edições de arquivo e comandos comuns do sistema de arquivos como `mkdir`, `touch` e `mv`, mas ainda pergunta antes de executar outros comandos de terminal. Use isso quando você confia em alterações de arquivo e quer iteração mais rápida.                    |
| **Plan mode**          | `plan`                | Claude lê arquivos e executa comandos para explorar, depois propõe um plano sem editar seu código-fonte. Bom para tarefas complexas onde você quer revisar a abordagem primeiro.                                                                                                               |
| **Auto**               | `auto`                | Claude executa todas as ações com verificações de segurança em segundo plano que verificam o alinhamento com sua solicitação. Reduz prompts de permissão mantendo supervisão. Ative em suas Configurações → Claude Code. Veja [requisitos de disponibilidade](#auto-mode-availability) abaixo. |
| **Bypass permissions** | `bypassPermissions`   | Claude é executado sem nenhum prompt de permissão, equivalente a `--dangerously-skip-permissions` no CLI. Ative em suas Configurações → Claude Code em "Allow bypass permissions mode". Use apenas em containers ou VMs sandboxed. Administradores corporativos podem desabilitar essa opção.  |

O modo de permissão `dontAsk` está disponível apenas no [CLI](/pt/permission-modes#allow-only-pre-approved-tools-with-dontask-mode).

<span id="auto-mode-availability" />

Auto mode é uma visualização de pesquisa disponível em planos Max, Team, Enterprise e API. Não está disponível em planos Pro ou provedores de terceiros. Em planos Team, Enterprise e API, requer Claude Sonnet 4.6, Opus 4.6 ou Opus 4.7. Em planos Max, requer Claude Opus 4.7.

<Tip title="Melhor prática">
  Comece tarefas complexas em Plan mode para que Claude mapeie uma abordagem antes de fazer alterações. Depois de aprovar o plano, mude para Auto accept edits ou Ask permissions para executá-lo. Veja [explorar primeiro, depois planejar, depois codificar](/pt/best-practices#explore-first-then-plan-then-code) para mais sobre esse fluxo de trabalho.
</Tip>

Sessões remotas suportam Auto accept edits e Plan mode. Ask permissions não está disponível porque sessões remotas aceitam automaticamente edições de arquivo por padrão, e Bypass permissions não está disponível porque o ambiente remoto já é sandboxed.

Administradores corporativos podem restringir quais modos de permissão estão disponíveis. Veja [configuração corporativa](#enterprise-configuration) para detalhes.

### Visualizar seu aplicativo

Claude pode iniciar um servidor de desenvolvimento e abrir um navegador incorporado para verificar suas alterações. Isso funciona para aplicativos web frontend e também para servidores backend: Claude pode testar endpoints de API, visualizar logs do servidor e iterar em problemas que encontra. Na maioria dos casos, Claude inicia o servidor automaticamente após editar arquivos de projeto. Você também pode pedir a Claude para visualizar a qualquer momento. Por padrão, Claude [verifica automaticamente](#auto-verify-changes) alterações após cada edição.

O painel de visualização também pode abrir arquivos HTML estáticos, PDFs, imagens e vídeos do seu projeto. Clique em um caminho HTML, PDF, imagem ou vídeo no chat para abri-lo em visualização.

No painel de visualização, você pode:

* Interagir com seu aplicativo em execução diretamente no navegador incorporado
* Assistir Claude verificar suas próprias alterações automaticamente: ele tira capturas de tela, inspeciona o DOM, clica em elementos, preenche formulários e corrige problemas que encontra
* Iniciar ou parar servidores no menu suspenso **Preview** na barra de ferramentas da sessão
* Persistir cookies e armazenamento local entre reinicializações do servidor selecionando **Persist sessions** no menu suspenso, para que você não tenha que fazer login novamente durante o desenvolvimento
* Editar a configuração do servidor ou parar todos os servidores de uma vez

Claude cria a configuração inicial do servidor com base em seu projeto. Se seu aplicativo usa um comando dev personalizado, edite `.claude/launch.json` para corresponder à sua configuração. Veja [Configurar servidores de visualização](#configure-preview-servers) para a referência completa.

Para limpar dados de sessão salvos, alterne **Persist preview sessions** desligado em Configurações → Claude Code. Para desabilitar a visualização completamente, alterne **Preview** desligado em Configurações → Claude Code.

### Revisar alterações com visualização de diff

Depois que Claude faz alterações em seu código, a visualização de diff permite que você revise modificações arquivo por arquivo antes de criar um pull request.

Quando Claude altera arquivos, um indicador de estatísticas de diff aparece mostrando o número de linhas adicionadas e removidas, como `+12 -1`. Clique neste indicador para abrir o visualizador de diff, que exibe uma lista de arquivos à esquerda e as alterações para cada arquivo à direita.

Para comentar em linhas específicas, clique em qualquer linha no diff para abrir uma caixa de comentário. Digite seu feedback e pressione **Enter** para adicionar o comentário. Depois de adicionar comentários a várias linhas, envie todos os comentários de uma vez:

* **macOS**: pressione **Cmd+Enter**
* **Windows**: pressione **Ctrl+Enter**

Claude lê seus comentários e faz as alterações solicitadas, que aparecem como um novo diff que você pode revisar.

### Revisar seu código

Na visualização de diff, clique em **Review code** na barra de ferramentas superior direita para pedir a Claude para avaliar as alterações antes de você fazer commit. Claude examina os diffs atuais e deixa comentários diretamente na visualização de diff. Você pode responder a qualquer comentário ou pedir a Claude para revisar.

A revisão se concentra em problemas de alto sinal: erros de compilação, erros de lógica definidos, vulnerabilidades de segurança e bugs óbvios. Não sinaliza estilo, formatação, problemas pré-existentes ou qualquer coisa que um linter capturaria.

### Monitorar status de pull request

Depois de abrir um pull request, uma barra de status de CI aparece na sessão. Claude Code usa o GitHub CLI para pesquisar resultados de verificação e exibir falhas.

* **Auto-fix**: quando ativado, Claude tenta automaticamente corrigir verificações de CI falhando lendo a saída de falha e iterando.
* **Auto-merge**: quando ativado, Claude mescla o PR assim que todas as verificações passam. O método de mesclagem é squash. Auto-merge deve ser [ativado nas configurações do seu repositório GitHub](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-auto-merge-for-pull-requests-in-your-repository) para isso funcionar.

Use os toggles **Auto-fix** e **Auto-merge** na barra de status de CI para ativar qualquer opção. Claude Code também envia uma notificação de desktop quando CI termina. Para arquivar a sessão automaticamente assim que o PR mescla ou fecha, ative [auto-archive](#work-in-parallel-with-sessions) em Configurações → Claude Code.

<Note>
  O monitoramento de PR requer que o [GitHub CLI (`gh`)](https://cli.github.com/) esteja instalado e autenticado em sua máquina. Se `gh` não estiver instalado, Desktop o solicita a instalar na primeira vez que você tentar criar um PR.
</Note>

## Organizar seu workspace

A aba Code é construída em torno de painéis que você pode organizar em qualquer layout: chat, diff, preview, terminal, file, plan, tasks e subagent. Arraste um painel por seu cabeçalho para reposicioná-lo, ou arraste uma borda de painel para redimensioná-lo. Pressione **Cmd+\\** no macOS ou **Ctrl+\\** no Windows para fechar o painel focado. Abra painéis adicionais no menu **Views** na barra de ferramentas da sessão.

<Note>
  O layout do painel, terminal, editor de arquivo e modos de visualização nesta seção requerem Claude Desktop v1.2581.0 ou posterior. Abra **Claude → Check for Updates** no macOS ou **Help → Check for Updates** no Windows para atualizar.
</Note>

### Executar comandos no terminal

O terminal integrado permite que você execute comandos ao lado de sua sessão sem alternar para outro aplicativo. Abra-o no menu **Views** ou pressione **Ctrl+\`** no macOS ou Windows. O terminal abre no diretório de trabalho de sua sessão e compartilha o mesmo ambiente que Claude, então comandos como `npm test` ou `git status` veem os mesmos arquivos que Claude está editando. Para abrir uma segunda aba de terminal, clique em **+** no cabeçalho do painel de terminal ou clique com o botão direito em uma pasta no chat para escolher **Open in terminal**. O terminal está disponível apenas em sessões locais.

### Abrir e editar arquivos

Clique em um caminho de arquivo no chat ou visualizador de diff para abri-lo no painel de arquivo. Caminhos HTML, PDF, imagem e vídeo abrem no [painel de preview](#preview-your-app) em vez disso. Faça edições pontuais e clique em **Save** para escrevê-las de volta. Se o arquivo mudou no disco desde que você o abriu, o painel o avisa e permite que você sobrescreva ou descarte. Clique em **Discard** para reverter suas edições, ou clique no caminho no cabeçalho do painel para copiar o caminho absoluto.

O painel de arquivo está disponível em sessões locais e SSH. Para sessões remotas, peça a Claude para fazer a alteração.

### Abrir arquivos em outros aplicativos

Clique com o botão direito em qualquer caminho de arquivo no chat, visualizador de diff ou painel de arquivo para abrir um menu de contexto:

* **Attach as context**: adicione o arquivo ao seu próximo prompt
* **Open in**: abra o arquivo em um editor instalado como VS Code, Cursor ou Zed
* **Show in Finder** no macOS, **Show in Explorer** no Windows: abra a pasta contendo
* **Copy path**: copie o caminho absoluto para sua área de transferência

### Alternar modos de visualização

Os modos de visualização controlam quanto detalhe aparece na transcrição do chat. Alterne modos no menu suspenso **Transcript view** ao lado do botão enviar, ou pressione **Ctrl+O** no macOS ou Windows para ciclar através deles.

| Modo        | O que mostra                                                                         |
| ----------- | ------------------------------------------------------------------------------------ |
| **Normal**  | Chamadas de ferramenta recolhidas em resumos, com respostas de texto completo        |
| **Verbose** | Cada chamada de ferramenta, leitura de arquivo e passo intermediário que Claude toma |
| **Summary** | Apenas as respostas finais de Claude e as alterações que fez                         |

Use Verbose ao depurar por que Claude tomou uma ação particular. Use Summary quando você está executando múltiplas sessões e quer escanear resultados rapidamente.

### Atalhos de teclado

Pressione **Cmd+/** no macOS ou **Ctrl+/** no Windows para ver todos os atalhos disponíveis na aba Code. No Windows, use **Ctrl** no lugar de **Cmd** para os atalhos abaixo. Ciclagem de sessão, alternância de terminal e alternância de modo de visualização usam **Ctrl** em todas as plataformas.

| Atalho                                | Ação                              |
| ------------------------------------- | --------------------------------- |
| `Cmd` `/`                             | Mostrar atalhos de teclado        |
| `Cmd` `N`                             | Nova sessão                       |
| `Cmd` `W`                             | Fechar sessão                     |
| `Ctrl` `Tab` / `Ctrl` `Shift` `Tab`   | Próxima ou sessão anterior        |
| `Cmd` `Shift` `]` / `Cmd` `Shift` `[` | Próxima ou sessão anterior        |
| `Esc`                                 | Parar resposta de Claude          |
| `Cmd` `Shift` `D`                     | Alternar painel de diff           |
| `Cmd` `Shift` `P`                     | Alternar painel de preview        |
| `Cmd` `Shift` `S`                     | Selecionar um elemento em preview |
| `Ctrl` `` ` ``                        | Alternar painel de terminal       |
| `Cmd` `\`                             | Fechar painel focado              |
| `Cmd` `;`                             | Abrir chat lateral                |
| `Ctrl` `O`                            | Ciclar modos de visualização      |
| `Cmd` `Shift` `M`                     | Abrir menu de modo de permissão   |
| `Cmd` `Shift` `I`                     | Abrir menu de modelo              |
| `Cmd` `Shift` `E`                     | Abrir menu de esforço             |
| `1`–`9`                               | Selecionar item em um menu aberto |

Esses atalhos se aplicam apenas à aba Code. Os [atalhos de modo interativo](/pt/interactive-mode#keyboard-shortcuts) baseados em terminal, como `Shift+Tab` para ciclar modos, não se aplicam em Desktop.

### Verificar uso

Clique no anel de uso ao lado do seletor de modelo para ver seu uso atual da janela de contexto e seu uso do plano para o período. O uso de contexto é por sessão; o uso do plano é compartilhado em todas as suas superfícies Claude Code.

## Deixar Claude usar seu computador

Computer use permite que Claude abra seus aplicativos, controle sua tela e trabalhe diretamente em sua máquina da forma como você faria. Peça a Claude para testar um aplicativo nativo em um simulador móvel, interagir com uma ferramenta de desktop que não tem CLI ou automatizar algo que só funciona através de uma GUI.

<Note>
  Computer use é uma visualização de pesquisa no macOS e Windows que requer um plano Pro ou Max. Não está disponível em planos Team ou Enterprise. O aplicativo Claude Desktop deve estar em execução.
</Note>

Computer use está desativado por padrão. [Ative-o em Configurações](#enable-computer-use) antes que Claude possa controlar sua tela. No macOS, você também precisa conceder permissões de Acessibilidade e Gravação de Tela.

<Warning>
  Diferentemente da [ferramenta Bash sandboxed](/pt/sandboxing), computer use é executado em seu desktop real com acesso a tudo que você aprova. Claude verifica cada ação e sinaliza possível injeção de prompt do conteúdo na tela, mas o limite de confiança é diferente. Veja o [guia de segurança de computer use](https://support.claude.com/en/articles/14128542) para melhores práticas.
</Warning>

### Quando computer use se aplica

Claude tem várias maneiras de interagir com um aplicativo ou serviço, e computer use é a mais ampla e lenta. Ele tenta a ferramenta mais precisa primeiro:

* Se você tem um [connector](#connect-external-tools) para um serviço, Claude usa o connector.
* Se a tarefa é um comando shell, Claude usa Bash.
* Se a tarefa é trabalho de navegador e você tem [Claude no Chrome](/pt/chrome) configurado, Claude usa isso.
* Se nenhum desses se aplica, Claude usa computer use.

Os [níveis de acesso por aplicativo](#app-permissions) reforçam isso: navegadores são limitados a apenas visualização, e terminais e IDEs a apenas clique, direcionando Claude para a ferramenta dedicada mesmo quando computer use está ativo. O controle de tela é reservado para coisas que nada mais pode alcançar, como aplicativos nativos, painéis de controle de hardware, simuladores móveis ou ferramentas proprietárias sem uma API.

### Ativar computer use

Computer use está desativado por padrão. Se você pedir a Claude para fazer algo que precisa disso enquanto está desativado, Claude diz que poderia fazer a tarefa se você ativar computer use em Configurações.

<Steps>
  <Step title="Atualizar o aplicativo desktop">
    Certifique-se de que você tem a versão mais recente do Claude Desktop. Baixe ou atualize em [claude.com/download](https://claude.com/download), depois reinicie o aplicativo.
  </Step>

  <Step title="Ativar o toggle">
    No aplicativo desktop, vá para **Configurações > Geral** (em **Aplicativo Desktop**). Encontre o toggle **Computer use** e ative-o. No Windows, o toggle entra em efeito imediatamente e a configuração está completa. No macOS, continue para o próximo passo.

    Se você não vir o toggle, confirme que você está em macOS ou Windows com um plano Pro ou Max, depois atualize e reinicie o aplicativo.
  </Step>

  <Step title="Conceder permissões macOS">
    No macOS, conceda duas permissões do sistema antes do toggle entrar em efeito:

    * **Accessibility**: permite que Claude clique, digite e role
    * **Screen Recording**: permite que Claude veja o que está em sua tela

    A página de Configurações mostra o status atual de cada permissão. Se alguma for negada, clique no badge para abrir o painel de Configurações do Sistema relevante.
  </Step>
</Steps>

### Permissões de aplicativo

A primeira vez que Claude precisa usar um aplicativo, um prompt aparece em sua sessão. Clique em **Allow for this session** ou **Deny**. As aprovações duram para a sessão atual, ou 30 minutos em [sessões geradas por Dispatch](#sessions-from-dispatch).

O prompt também mostra que nível de controle Claude obtém para esse aplicativo. Esses níveis são fixos por categoria de aplicativo e não podem ser alterados:

| Nível        | O que Claude pode fazer                                    | Se aplica a                            |
| :----------- | :--------------------------------------------------------- | :------------------------------------- |
| View only    | Ver o aplicativo em capturas de tela                       | Navegadores, plataformas de negociação |
| Click only   | Clicar e rolar, mas não digitar ou usar atalhos de teclado | Terminais, IDEs                        |
| Full control | Clicar, digitar, arrastar e usar atalhos de teclado        | Tudo mais                              |

Aplicativos com alcance amplo como terminais, Finder ou File Explorer e System Settings ou Settings mostram um aviso extra no prompt para que você saiba o que aprovar concede.

Você pode configurar duas configurações em **Configurações > Geral** (em **Aplicativo Desktop**):

* **Denied apps**: adicione aplicativos aqui para rejeitá-los sem solicitar. Claude ainda pode afetar um aplicativo negado indiretamente através de ações em um aplicativo permitido, mas não pode interagir com o aplicativo negado diretamente.
* **Unhide apps when Claude finishes**: enquanto Claude está trabalhando, suas outras janelas são ocultadas para que ele interaja apenas com o aplicativo aprovado. Quando Claude termina, as janelas ocultas são restauradas a menos que você desative essa configuração.

## Gerenciar sessões

Cada sessão é uma conversa independente com seu próprio contexto e alterações. Você pode executar múltiplas sessões em paralelo, ramificar chats laterais, enviar trabalho para a nuvem ou deixar Dispatch iniciar sessões para você do seu telefone.

### Trabalhar em paralelo com sessões

Clique em **+ New session** na barra lateral, ou pressione **Cmd+N** no macOS ou **Ctrl+N** no Windows, para trabalhar em múltiplas tarefas em paralelo. Pressione **Ctrl+Tab** e **Ctrl+Shift+Tab** para ciclar através de sessões na barra lateral. Para repositórios Git, cada sessão obtém sua própria cópia isolada do seu projeto usando [Git worktrees](/pt/worktrees), para que alterações em uma sessão não afetem outras sessões até que você as faça commit.

Para visualizar duas sessões ao mesmo tempo, mantenha **Cmd** no macOS ou **Ctrl** no Windows e clique em uma sessão na barra lateral. A sessão abre em um segundo painel ao lado daquele que você já tem aberto. Enquanto a divisão está ativa, clicar em outra sessão da barra lateral substitui o painel que tem foco. Pressione **Cmd+\\** no macOS ou **Ctrl+\\** no Windows para fechar o painel focado e retornar a uma única sessão.

Worktrees são armazenadas em `<project-root>/.claude/worktrees/` por padrão. Você pode alterar isso para um diretório personalizado em Configurações → Claude Code em "Worktree location". Você também pode definir um prefixo de branch que é adicionado a cada nome de branch worktree, o que é útil para manter branches criadas por Claude organizadas. Para remover um worktree quando terminar, passe o mouse sobre a sessão na barra lateral e clique no ícone de arquivo. Para ter sessões se arquivarem automaticamente quando seu pull request mescla ou fecha, ative **Auto-archive after PR merge or close** em Configurações → Claude Code. Auto-archive se aplica apenas a sessões locais que terminaram de executar.

Para incluir arquivos gitignored como `.env` em novos worktrees, crie um [arquivo `.worktreeinclude`](/pt/worktrees#copy-gitignored-files-into-worktrees) na raiz do seu projeto.

<Note>
  O isolamento de sessão requer [Git](https://git-scm.com/downloads). A maioria dos Macs inclui Git por padrão. Execute `git --version` no Terminal para verificar. No Windows, Git é necessário para a aba Code funcionar: [baixe Git para Windows](https://git-scm.com/downloads/win), instale-o e reinicie o aplicativo. Se você encontrar erros de Git, peça a Claude na aba [Cowork](https://claude.com/product/cowork) para ajudar a solucionar problemas de sua configuração.
</Note>

Use os controles no topo da barra lateral para filtrar sessões por status, projeto ou ambiente, e para agrupar sessões por projeto. Para renomear uma sessão, clique no título da sessão na barra de ferramentas no topo da sessão ativa. Para verificar o uso de contexto, veja [Verificar uso](#check-usage). Quando o contexto se enche, Claude automaticamente resume a conversa e continua trabalhando. Você também pode digitar `/compact` para disparar a sumarização mais cedo e liberar espaço de contexto. Veja [a janela de contexto](/pt/how-claude-code-works#the-context-window) para detalhes sobre como a compactação funciona.

O aplicativo desktop envia uma notificação do SO quando uma sessão de Code termina uma tarefa e você não está visualizando essa sessão no momento.

### Fazer uma pergunta lateral sem descarrilar a sessão

Um chat lateral permite que você faça a Claude uma pergunta que usa o contexto de sua sessão mas não adiciona nada de volta à conversa principal. Use-o quando você quer entender um pedaço de código, verificar uma suposição ou explorar uma ideia sem descarrilar a sessão.

Pressione **Cmd+;** no macOS ou **Ctrl+;** no Windows para abrir um chat lateral, ou digite `/btw` na caixa de prompt. O chat lateral pode ler tudo no thread principal até esse ponto. Quando terminar, feche o chat lateral e continue a sessão principal onde deixou. Chats laterais estão disponíveis em sessões locais e SSH.

### Assistir tarefas em segundo plano

O painel de tarefas mostra o trabalho em segundo plano em execução dentro da sessão atual: subagents, comandos shell em segundo plano e workflows. Abra-o no menu **Views** ou arraste-o para seu layout.

Clique em qualquer entrada para ver sua saída no painel de subagent ou pará-la. Para ver o que outras sessões estão fazendo, use a [barra lateral](#work-in-parallel-with-sessions).

### Executar tarefas de longa duração remotamente

Para grandes refatorações, suites de teste, migrações ou outras tarefas de longa duração, selecione **Remote** em vez de **Local** ao iniciar uma sessão. Sessões remotas são executadas na infraestrutura em nuvem da Anthropic e continuam mesmo se você fechar o aplicativo ou desligar seu computador. Verifique a qualquer momento para ver o progresso ou direcionar Claude em uma direção diferente. Você também pode monitorar sessões remotas de [claude.ai/code](https://claude.ai/code) ou do aplicativo Claude iOS.

Sessões remotas também suportam múltiplos repositórios. Depois de selecionar um ambiente em nuvem, clique no botão **+** ao lado do pill de repo para adicionar repositórios adicionais à sessão. Cada repo obtém seu próprio seletor de branch. Isso é útil para tarefas que abrangem múltiplas bases de código, como atualizar uma biblioteca compartilhada e seus consumidores.

Veja [Claude Code na web](/pt/claude-code-on-the-web) para mais sobre como sessões remotas funcionam.

### Continuar em outra superfície

O menu **Continue in**, acessível do ícone VS Code no canto inferior direito da barra de ferramentas da sessão, permite que você mova sua sessão para outra superfície:

* **Claude Code on the Web**: envia sua sessão local para continuar executando remotamente. Desktop envia seu branch, gera um resumo da conversa e cria uma nova sessão remota com o contexto completo. Você pode então escolher arquivar a sessão local ou mantê-la. Isso requer uma árvore de trabalho limpa e não está disponível para sessões SSH.
* **Your IDE**: abre seu projeto em um IDE suportado no diretório de trabalho atual.

### Sessões do Dispatch

[Dispatch](https://support.claude.com/en/articles/13947068) é uma conversa persistente com Claude que vive na aba [Cowork](https://claude.com/product/cowork#dispatch-and-computer-use). Você envia uma mensagem ao Dispatch com uma tarefa, e ele decide como lidar com ela.

Uma tarefa pode acabar como uma sessão de Code de duas maneiras: você pede uma diretamente, como "abra uma sessão Claude Code e corrija o bug de login", ou Dispatch decide que a tarefa é trabalho de desenvolvimento e gera uma por conta própria. Tarefas que normalmente são roteadas para Code incluem corrigir bugs, atualizar dependências, executar testes ou abrir pull requests. Pesquisa, edição de documentos e trabalho em planilhas ficam em Cowork.

De qualquer forma, a sessão de Code aparece na barra lateral da aba Code com um badge **Dispatch**. Você recebe uma notificação push em seu telefone quando termina ou precisa de sua aprovação.

Se você tem [computer use](#let-claude-use-your-computer) ativado, sessões de Code geradas por Dispatch também podem usá-lo. As aprovações de aplicativo nessas sessões expiram após 30 minutos e solicitam novamente, em vez de durarem a sessão completa como sessões de Code regulares.

Para configuração, emparelhamento e configurações de Dispatch, veja o [artigo de ajuda do Dispatch](https://support.claude.com/en/articles/13947068). Dispatch requer um plano Pro ou Max e não está disponível em planos Team ou Enterprise.

Dispatch é uma de várias maneiras de trabalhar com Claude quando você está longe de seu terminal. Veja [Plataformas e integrações](/pt/platforms#work-when-you-are-away-from-your-terminal) para compará-lo com Remote Control, Channels, Slack e tarefas agendadas.

## Estender Claude Code

Conecte serviços externos, adicione fluxos de trabalho reutilizáveis, customize o comportamento de Claude e configure servidores de visualização. Para gerenciar conectores, skills e plugins em um único lugar, clique em **Customize** na barra lateral.

### Conectar ferramentas externas

Para sessões locais e [SSH](#ssh-sessions), clique no botão **+** ao lado da caixa de prompt e selecione **Connectors** para adicionar integrações como Google Calendar, Slack, GitHub, Linear, Notion e muito mais. Você pode adicionar conectores antes ou durante uma sessão. O botão **+** não está disponível em sessões remotas, mas [routines](/pt/routines) configuram conectores no momento da criação da rotina.

Para gerenciar ou desconectar conectores, vá para Configurações → Connectors no aplicativo desktop, ou selecione **Manage connectors** no menu Connectors na caixa de prompt.

Uma vez conectado, Claude pode ler seu calendário, enviar mensagens, criar problemas e interagir com suas ferramentas diretamente. Você pode perguntar a Claude quais conectores estão configurados em sua sessão.

Conectores são [MCP servers](/pt/mcp) com um fluxo de configuração gráfica. Use-os para integração rápida com serviços suportados. Para integrações não listadas em Connectors, adicione MCP servers manualmente via [arquivos de configuração](/pt/mcp#installing-mcp-servers). Você também pode [criar conectores personalizados](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp).

### Use skills

[Skills](/pt/skills) estendem o que Claude pode fazer. Claude as carrega automaticamente quando relevante, ou você pode invocar uma diretamente: digite `/` na caixa de prompt ou clique no botão **+** e selecione **Slash commands** para navegar pelo que está disponível. Isso inclui [comandos integrados](/pt/commands), suas [skills personalizadas](/pt/skills#create-your-first-skill), skills de projeto de sua base de código e skills de qualquer [plugins instalados](/pt/plugins). Selecione uma e ela aparece destacada no campo de entrada. Digite sua tarefa depois dela e envie como usual.

### Instalar plugins

[Plugins](/pt/plugins) são pacotes reutilizáveis que adicionam skills, agents, hooks, MCP servers e configurações LSP ao Claude Code. Você pode instalar plugins do aplicativo desktop sem usar o terminal.

Para sessões locais e [SSH](#ssh-sessions), clique no botão **+** ao lado da caixa de prompt e selecione **Plugins** para ver seus plugins instalados e seus skills. Para adicionar um plugin, selecione **Add plugin** no submenu para abrir o navegador de plugins, que mostra plugins disponíveis de seus [marketplaces](/pt/plugin-marketplaces) configurados incluindo o marketplace oficial da Anthropic. Selecione **Manage plugins** para ativar, desativar ou desinstalar plugins.

Plugins podem ser escopo para sua conta de usuário, um projeto específico ou apenas local. Se sua organização gerencia plugins centralmente, esses plugins estão disponíveis em sessões desktop da mesma forma que estão no CLI. Plugins não estão disponíveis para sessões remotas. Para a referência completa de plugins incluindo criar seus próprios plugins, veja [plugins](/pt/plugins).

### Configurar servidores de visualização

Claude detecta automaticamente sua configuração de servidor de desenvolvimento e armazena a configuração em `.claude/launch.json` na raiz da pasta que você selecionou ao iniciar a sessão. Preview usa essa pasta como seu diretório de trabalho, então se você selecionou uma pasta pai, subpastas com seus próprios servidores de desenvolvimento não serão detectadas automaticamente. Para trabalhar com o servidor de uma subpasta, inicie uma sessão nessa pasta diretamente ou adicione uma configuração manualmente.

Para personalizar como seu servidor inicia, por exemplo para usar `yarn dev` em vez de `npm run dev` ou para alterar a porta, edite o arquivo manualmente ou clique em **Edit configuration** no menu Preview para abri-lo em seu editor de código. O arquivo suporta JSON com comentários.

```json theme={null}
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "my-app",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "port": 3000
    }
  ]
}
```

Você pode definir múltiplas configurações para executar diferentes servidores do mesmo projeto, como um frontend e uma API. Veja os [exemplos](#examples) abaixo.

#### Auto-verify changes

Quando `autoVerify` está ativado, Claude verifica automaticamente alterações de código após editar arquivos. Ele tira capturas de tela, verifica erros e confirma que as alterações funcionam antes de completar sua resposta.

Auto-verify está ativado por padrão. Desative-o por projeto adicionando `"autoVerify": false` a `.claude/launch.json`, ou alterne-o no menu **Preview**.

```json theme={null}
{
  "version": "0.0.1",
  "autoVerify": false,
  "configurations": [...]
}
```

Quando desativado, ferramentas de visualização ainda estão disponíveis e você pode pedir a Claude para verificar a qualquer momento. Auto-verify torna isso automático após cada edição.

#### Configuration fields

Cada entrada no array `configurations` aceita os seguintes campos:

| Campo               | Tipo      | Descrição                                                                                                                                                                                                                                                                                             |
| ------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`              | string    | Um identificador único para este servidor                                                                                                                                                                                                                                                             |
| `runtimeExecutable` | string    | O comando a executar, como `npm`, `yarn` ou `node`                                                                                                                                                                                                                                                    |
| `runtimeArgs`       | string\[] | Argumentos passados para `runtimeExecutable`, como `["run", "dev"]`                                                                                                                                                                                                                                   |
| `port`              | number    | A porta em que seu servidor escuta. Padrão é 3000                                                                                                                                                                                                                                                     |
| `cwd`               | string    | Diretório de trabalho relativo à raiz do seu projeto. Padrão é a raiz do projeto. Use `${workspaceFolder}` para referenciar a raiz do projeto explicitamente                                                                                                                                          |
| `env`               | object    | Variáveis de ambiente adicionais como pares chave-valor, como `{ "NODE_ENV": "development" }`. Não coloque segredos aqui já que este arquivo é commitado em seu repo. Para passar segredos ao seu servidor de desenvolvimento, defina-os no [editor de ambiente local](#local-sessions) em vez disso. |
| `autoPort`          | boolean   | Como lidar com conflitos de porta. Veja abaixo                                                                                                                                                                                                                                                        |
| `program`           | string    | Um script a executar com `node`. Veja [quando usar `program` vs `runtimeExecutable`](#when-to-use-program-vs-runtimeexecutable)                                                                                                                                                                       |
| `args`              | string\[] | Argumentos passados para `program`. Usado apenas quando `program` está definido                                                                                                                                                                                                                       |

##### When to use `program` vs `runtimeExecutable`

Use `runtimeExecutable` com `runtimeArgs` para iniciar um servidor de desenvolvimento através de um gerenciador de pacotes. Por exemplo, `"runtimeExecutable": "npm"` com `"runtimeArgs": ["run", "dev"]` executa `npm run dev`.

Use `program` quando você tem um script independente que quer executar com `node` diretamente. Por exemplo, `"program": "server.js"` executa `node server.js`. Passe flags adicionais com `args`.

#### Port conflicts

O campo `autoPort` controla o que acontece quando sua porta preferida já está em uso:

* **`true`**: Claude encontra e usa uma porta livre automaticamente. Adequado para a maioria dos servidores de desenvolvimento.
* **`false`**: Claude falha com um erro. Use isso quando seu servidor deve usar uma porta específica, como para callbacks OAuth ou allowlists CORS.
* **Não definido (padrão)**: Claude pergunta se o servidor precisa dessa porta exata, depois salva sua resposta.

Quando Claude escolhe uma porta diferente, ele passa a porta atribuída ao seu servidor via a variável de ambiente `PORT`.

#### Examples

Essas configurações mostram setups comuns para diferentes tipos de projeto:

<Tabs>
  <Tab title="Next.js">
    Esta configuração executa um aplicativo Next.js usando Yarn na porta 3000:

    ```json theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "web",
          "runtimeExecutable": "yarn",
          "runtimeArgs": ["dev"],
          "port": 3000
        }
      ]
    }
    ```
  </Tab>

  <Tab title="Multiple servers">
    Para um monorepo com um servidor frontend e API, defina múltiplas configurações. O frontend usa `autoPort: true` para que escolha uma porta livre se 3000 estiver ocupada, enquanto o servidor API requer a porta 8080 exatamente:

    ```json theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "frontend",
          "runtimeExecutable": "npm",
          "runtimeArgs": ["run", "dev"],
          "cwd": "apps/web",
          "port": 3000,
          "autoPort": true
        },
        {
          "name": "api",
          "runtimeExecutable": "npm",
          "runtimeArgs": ["run", "start"],
          "cwd": "server",
          "port": 8080,
          "env": { "NODE_ENV": "development" },
          "autoPort": false
        }
      ]
    }
    ```
  </Tab>

  <Tab title="Node.js script">
    Para executar um script Node.js diretamente em vez de usar um comando do gerenciador de pacotes, use o campo `program`:

    ```json theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "server",
          "program": "server.js",
          "args": ["--verbose"],
          "port": 4000
        }
      ]
    }
    ```
  </Tab>
</Tabs>

## Configuração de ambiente

O ambiente que você escolhe ao [iniciar uma sessão](#start-a-session) determina onde Claude é executado e como você se conecta:

* **Local**: é executado em sua máquina com acesso direto aos seus arquivos
* **Remote**: é executado na infraestrutura em nuvem da Anthropic. Sessões continuam mesmo se você fechar o aplicativo.
* **SSH**: é executado em uma máquina remota à qual você se conecta via SSH, como seus próprios servidores, VMs em nuvem ou dev containers

### Local sessions

O aplicativo desktop nem sempre herda seu ambiente de shell completo. No macOS, quando você inicia o aplicativo do Dock ou Finder, ele lê seu perfil de shell, como `~/.zshrc` ou `~/.bashrc`, para extrair `PATH` e um conjunto fixo de variáveis Claude Code, mas outras variáveis que você exporta lá não são capturadas. No Windows, o aplicativo herda variáveis de ambiente de usuário e sistema mas não lê perfis PowerShell.

Para definir variáveis de ambiente para sessões locais e servidores de desenvolvimento em qualquer plataforma, abra o menu suspenso de ambiente na caixa de prompt, passe o mouse sobre **Local** e clique no ícone de engrenagem para abrir o editor de ambiente local. Variáveis que você salva aqui são armazenadas criptografadas em sua máquina e se aplicam a cada sessão local e servidor de visualização que você inicia. Você também pode adicionar variáveis à chave `env` em seu arquivo `~/.claude/settings.json`, embora essas alcancem apenas sessões Claude e não servidores de desenvolvimento. Veja [variáveis de ambiente](/pt/env-vars) para a lista completa de variáveis suportadas.

[Extended thinking](/pt/model-config#extended-thinking) está ativado por padrão, o que melhora o desempenho em tarefas de raciocínio complexo mas usa tokens adicionais. Para desabilitar o thinking completamente, defina `MAX_THINKING_TOKENS` para `0` no editor de ambiente local. Em modelos com [adaptive reasoning](/pt/model-config#adjust-effort-level), qualquer outro valor de `MAX_THINKING_TOKENS` é ignorado porque adaptive reasoning controla a profundidade do thinking. Em Opus 4.6 e Sonnet 4.6, defina `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` para `1` para usar um orçamento de thinking fixo; Opus 4.7 sempre usa adaptive reasoning e não tem modo de orçamento fixo.

### Remote sessions

Sessões remotas continuam em segundo plano mesmo se você fechar o aplicativo. O uso conta para seus [limites do plano de assinatura](/pt/costs) sem cobranças de computação separadas.

Você pode criar ambientes em nuvem personalizados com diferentes níveis de acesso de rede e variáveis de ambiente. Selecione o menu suspenso de ambiente ao iniciar uma sessão remota e escolha **Add environment**. Veja [o ambiente em nuvem](/pt/claude-code-on-the-web#the-cloud-environment) para detalhes sobre configuração de acesso de rede e variáveis de ambiente.

### SSH sessions

Sessões SSH permitem que você execute Claude Code em uma máquina remota enquanto usa o aplicativo desktop como sua interface. Isso é útil para trabalhar com bases de código que vivem em VMs em nuvem, dev containers ou servidores com hardware ou dependências específicas.

Para adicionar uma conexão SSH, clique no menu suspenso de ambiente antes de iniciar uma sessão e selecione **+ Add SSH connection**. O diálogo solicita:

* **Name**: um rótulo amigável para esta conexão
* **SSH Host**: `user@hostname` ou um host definido em `~/.ssh/config`
* **SSH Port**: padrão é 22 se deixado vazio, ou usa a porta de seu SSH config
* **Identity File**: caminho para sua chave privada, como `~/.ssh/id_rsa`. Deixe vazio para usar a chave padrão ou seu SSH config.

Uma vez adicionada, a conexão aparece no menu suspenso de ambiente. Selecione-a para iniciar uma sessão naquela máquina. Claude é executado na máquina remota com acesso aos seus arquivos e ferramentas.

A máquina remota deve executar Linux ou macOS. O aplicativo desktop instala Claude Code na máquina remota automaticamente na primeira vez que você se conecta. Uma vez conectado, sessões SSH suportam modos de permissão, conectores, plugins e MCP servers.

#### Pré-configurar conexões SSH para sua equipe

Administradores podem distribuir conexões SSH para membros da equipe adicionando `sshConfigs` a um arquivo de [configurações gerenciadas](/pt/settings#settings-precedence). Conexões definidas desta forma aparecem no menu suspenso de ambiente de cada usuário automaticamente e são mostradas como gerenciadas, para que os usuários possam selecioná-las mas não possam editá-las ou deletá-las no aplicativo.

O exemplo a seguir pré-configura uma única conexão que abre em `~/projects` no host remoto:

```json theme={null}
{
  "sshConfigs": [
    {
      "id": "shared-dev-vm",
      "name": "Shared Dev VM",
      "sshHost": "user@dev.example.com",
      "sshPort": 22,
      "sshIdentityFile": "~/.ssh/id_ed25519",
      "startDirectory": "~/projects"
    }
  ]
}
```

Cada entrada requer `id`, `name` e `sshHost`. Os campos `sshPort`, `sshIdentityFile` e `startDirectory` são opcionais. Os usuários também podem adicionar `sshConfigs` ao seu próprio `~/.claude/settings.json`, que é onde as conexões adicionadas através do diálogo são armazenadas.

#### Restringir quais hosts SSH os usuários podem se conectar

Administradores podem limitar as sessões SSH do Desktop a um conjunto aprovado de hosts adicionando `sshHostAllowlist` a um arquivo de [configurações gerenciadas](/pt/settings#settings-precedence). Quando definido, os usuários podem se conectar apenas a hosts cujo nome de host resolvido corresponde a um dos padrões. Defina-o como um array vazio para desabilitar sessões SSH completamente.

O exemplo a seguir permite conexões a qualquer host sob `devboxes.example.com` e a um único host bastion nomeado:

```json theme={null}
{
  "sshHostAllowlist": ["*.devboxes.example.com", "bastion.example.com"]
}
```

Padrões são insensíveis a maiúsculas e minúsculas. `*` corresponde a qualquer host, e `*.example.com` corresponde a `example.com` e qualquer subdomínio. Qualquer outra coisa é uma correspondência exata. A verificação é executada contra o nome de host após resolução `~/.ssh/config` via `ssh -G`, portanto entradas `Host` aliases e `ProxyCommand`/`ProxyJump` são permitidas desde que o `HostName` resolvido corresponda.

`sshHostAllowlist` é lido apenas de configurações gerenciadas; valores em configurações de usuário ou projeto são ignorados. Apenas o aplicativo Claude Desktop honra esta configuração; a CLI Claude Code e extensões IDE não a leem, e não restringe comandos `ssh` executados através da ferramenta Bash. Governa quais hosts o aplicativo Desktop se conecta, não saída de rede, portanto combine-o com controles de rede ou zero-trust da sua organização se você precisar de um limite rígido.

## Configuração corporativa

Organizações em planos Team ou Enterprise podem gerenciar o comportamento do aplicativo desktop através de controles do console de administração, arquivos de configurações gerenciadas e políticas de gerenciamento de dispositivos.

### Controles do console de administração

Essas configurações são configuradas através do [console de configurações de administração](https://claude.ai/admin-settings/claude-code):

* **Code in the desktop**: controle se usuários em sua organização podem acessar Claude Code no aplicativo desktop
* **Code in the web**: ative ou desative [sessões web](/pt/claude-code-on-the-web) para sua organização
* **Remote Control**: ative ou desative [Remote Control](/pt/remote-control) para sua organização
* **Disable Bypass permissions mode**: impeça usuários em sua organização de ativar o modo bypass permissions

### Managed settings

Configurações gerenciadas sobrescrevem configurações de projeto e usuário e se aplicam quando Desktop gera sessões CLI. Você pode definir essas chaves no arquivo de [configurações gerenciadas](/pt/settings#settings-precedence) de sua organização ou enviá-las remotamente através do console de administração.

| Chave                                      | Descrição                                                                                                                                                                                                                                                                                                                                                            |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `permissions.disableBypassPermissionsMode` | defina como `"disable"` para impedir usuários de ativar o modo Bypass permissions.                                                                                                                                                                                                                                                                                   |
| `disableAutoMode`                          | defina como `"disable"` para impedir usuários de ativar o modo [Auto](/pt/permission-modes#eliminate-prompts-with-auto-mode). Remove Auto do seletor de modo. Também aceito em `permissions`.                                                                                                                                                                        |
| `autoMode`                                 | customize o que o classificador de modo auto confia e bloqueia em sua organização. Veja [Configurar o modo auto](/pt/auto-mode-config).                                                                                                                                                                                                                              |
| `sshConfigs`                               | pré-configure [conexões SSH](#pre-configure-ssh-connections-for-your-team) que aparecem no dropdown de ambiente. Usuários não podem editar ou excluir conexões gerenciadas.                                                                                                                                                                                          |
| `sshHostAllowlist`                         | restrinja [sessões SSH](#restrict-which-ssh-hosts-users-can-connect-to) a hosts cujo nome de host resolvido corresponde a um desses padrões. Uma matriz vazia desativa sessões SSH. Lido apenas de configurações gerenciadas.                                                                                                                                        |
| `managedMcpServers`                        | envie configurações de servidor MCP para todos os usuários em uma implantação de terceiros. Cada entrada especifica um transporte de `"http"`, `"sse"` ou `"stdio"`, detalhes de conexão e opcionalmente um mapa `toolPolicy` que restringe quais ferramentas nesse servidor os usuários podem invocar. Disponível apenas em implantações Desktop de terceiros (3P). |

Um arquivo de configurações gerenciadas implantado em disco em cada máquina se aplica a sessões Desktop. Configurações gerenciadas enviadas remotamente através do console de administração atualmente alcançam apenas sessões CLI e IDE, portanto, para implantações Desktop, distribua o arquivo via MDM ou use os [controles do console de administração](#admin-console-controls) acima.

`permissions.disableBypassPermissionsMode` e `disableAutoMode` também funcionam em configurações de usuário e projeto, mas colocá-los em configurações gerenciadas impede que usuários os sobrescrevam. `autoMode` é lido de configurações de usuário, `.claude/settings.local.json` e configurações gerenciadas, mas não de `.claude/settings.json` verificado: um repo clonado não pode injetar suas próprias regras de classificador. Para a lista completa de configurações apenas gerenciadas incluindo `allowManagedPermissionRulesOnly` e `allowManagedHooksOnly`, veja [configurações apenas gerenciadas](/pt/permissions#managed-only-settings).

### Políticas de gerenciamento de dispositivos

Equipes de TI podem gerenciar o aplicativo desktop através de MDM em macOS ou group policy no Windows. As políticas disponíveis incluem ativar ou desativar o recurso Claude Code, controlar atualizações automáticas e definir uma URL de implantação personalizada.

* **macOS**: configure via domínio de preferência `com.anthropic.Claude` usando ferramentas como Jamf ou Kandji
* **Windows**: configure via registro em `SOFTWARE\Policies\Claude`

### Autenticação e SSO

Organizações corporativas podem exigir SSO para todos os usuários. Veja [autenticação](/pt/authentication) para detalhes de nível de plano e [Configurando SSO](https://support.claude.com/en/articles/13132885-setting-up-single-sign-on-sso) para configuração SAML e OIDC.

### Manipulação de dados

Claude Code processa seu código localmente em sessões locais ou na infraestrutura em nuvem da Anthropic em sessões remotas. Conversas e contexto de código são enviados para a API da Anthropic para processamento. Veja [manipulação de dados](/pt/data-usage) para detalhes sobre retenção de dados, privacidade e conformidade.

### Implantação

Desktop pode ser distribuído através de ferramentas de implantação corporativa:

* **macOS**: distribua via MDM como Jamf ou Kandji usando o instalador `.dmg`
* **Windows**: implante via pacote MSIX ou instalador `.exe`. Veja [Deploy Claude Desktop for Windows](https://support.claude.com/en/articles/12622703-deploy-claude-desktop-for-windows) para opções de implantação corporativa incluindo instalação silenciosa

Para configuração de rede como configurações de proxy, allowlisting de firewall e gateways LLM, veja [configuração de rede](/pt/network-config).

Para a referência completa de configuração corporativa, veja o [guia de configuração corporativa](https://support.claude.com/en/articles/12622667-enterprise-configuration).

## Vindo do CLI?

Se você já usa o CLI do Claude Code, Desktop executa o mesmo mecanismo subjacente com uma interface gráfica. Você pode executar ambos simultaneamente na mesma máquina, até mesmo no mesmo projeto. Cada um mantém histórico de sessão separado, mas compartilham configuração e memória de projeto via arquivos CLAUDE.md.

Para mover uma sessão CLI para Desktop, execute `/desktop` no terminal. Claude salva sua sessão e a abre no aplicativo desktop, depois sai do CLI. Este comando está disponível apenas em macOS e Windows.

<Tip>
  Quando usar Desktop vs CLI: use Desktop quando você quer gerenciar sessões paralelas em uma janela, organizar painéis lado a lado ou revisar alterações visualmente. Use o CLI quando você precisa de scripting, automação ou prefere um fluxo de trabalho de terminal.
</Tip>

### CLI flag equivalents

Esta tabela mostra o equivalente do aplicativo desktop para flags CLI comuns. Flags não listadas não têm equivalente desktop porque são projetadas para scripting ou automação.

| CLI                                        | Equivalente desktop                                                                                                                                                |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `--model sonnet`                           | Menu suspenso de modelo ao lado do botão enviar                                                                                                                    |
| `--resume`, `--continue`                   | Clique em uma sessão na barra lateral                                                                                                                              |
| `--permission-mode`                        | Seletor de modo ao lado do botão enviar                                                                                                                            |
| `--dangerously-skip-permissions`           | Modo Bypass permissions. Ative em Configurações → Claude Code → "Allow bypass permissions mode". Administradores corporativos podem desabilitar essa configuração. |
| `--add-dir`                                | Adicione múltiplos repos com o botão **+** em sessões remotas                                                                                                      |
| `--allowedTools`, `--disallowedTools`      | Nenhum equivalente por sessão. Regras de permissão em [arquivos de configuração](/pt/settings) ainda se aplicam.                                                   |
| `--verbose`                                | [Modo de visualização Verbose](#switch-view-modes) no menu suspenso Transcript view                                                                                |
| `--print`, `--output-format`               | Não disponível. Desktop é apenas interativo.                                                                                                                       |
| Variável de ambiente `ANTHROPIC_MODEL`     | Menu suspenso de modelo ao lado do botão enviar                                                                                                                    |
| Variável de ambiente `MAX_THINKING_TOKENS` | Defina no editor de ambiente local. Veja [configuração de ambiente](#environment-configuration).                                                                   |

### Shared configuration

Desktop e CLI leem os mesmos arquivos de configuração, então sua configuração é transferida:

* Arquivos **[CLAUDE.md](/pt/memory)** e `CLAUDE.local.md` em seu projeto são usados por ambos
* **[MCP servers](/pt/mcp)** configurados em `~/.claude.json` ou `.mcp.json` funcionam em ambos
* **[Hooks](/pt/hooks)** e **[skills](/pt/skills)** definidos em configurações se aplicam a ambos
* **[Configurações](/pt/settings)** em `~/.claude.json` e `~/.claude/settings.json` são compartilhadas. Regras de permissão, ferramentas permitidas e outras configurações em `settings.json` se aplicam a sessões Desktop.
* **Modelos**: Sonnet, Opus e Haiku estão disponíveis em ambos. Em Desktop, selecione o modelo no menu suspenso ao lado do botão enviar. Você pode alterar o modelo durante a sessão a partir do mesmo menu suspenso.

<Note>
  **MCP servers: aplicativo de chat desktop vs Claude Code**: MCP servers configurados para o aplicativo de chat Claude Desktop em `claude_desktop_config.json` são separados do Claude Code e não aparecerão na aba Code. Para usar MCP servers em Claude Code, configure-os em `~/.claude.json` ou no arquivo `.mcp.json` do seu projeto. Veja [configuração MCP](/pt/mcp#installing-mcp-servers) para detalhes.
</Note>

### Feature comparison

Esta tabela compara capacidades principais entre CLI e Desktop. Para uma lista completa de flags CLI, veja a [referência CLI](/pt/cli-reference).

| Recurso                                                 | CLI                                                       | Desktop                                                                                                                                                                                                                         |
| ------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Modos de permissão                                      | Todos os modos incluindo `dontAsk`                        | Ask permissions, Auto accept edits, Plan mode, Auto e Bypass permissions via Configurações                                                                                                                                      |
| `--dangerously-skip-permissions`                        | Flag CLI                                                  | Modo Bypass permissions. Ative em Configurações → Claude Code → "Allow bypass permissions mode"                                                                                                                                 |
| [Provedores de terceiros](/pt/third-party-integrations) | Bedrock, Vertex, Foundry                                  | API da Anthropic por padrão. Implantações corporativas podem configurar Vertex AI e provedores de gateway. Veja o [guia de configuração corporativa](https://support.claude.com/en/articles/12622667-enterprise-configuration). |
| [MCP servers](/pt/mcp)                                  | Configure em arquivos de configuração                     | UI de Connectors para sessões locais e SSH, ou arquivos de configuração                                                                                                                                                         |
| [Plugins](/pt/plugins)                                  | Comando `/plugin`                                         | UI do gerenciador de plugins                                                                                                                                                                                                    |
| @mention de arquivos                                    | Baseado em texto                                          | Com autocompletar; sessões locais e SSH apenas                                                                                                                                                                                  |
| Anexos de arquivo                                       | Não disponível                                            | Imagens, PDFs                                                                                                                                                                                                                   |
| Isolamento de sessão                                    | Flag [`--worktree`](/pt/cli-reference)                    | Worktrees automáticos                                                                                                                                                                                                           |
| Múltiplas sessões                                       | Terminais separados                                       | Abas na barra lateral                                                                                                                                                                                                           |
| Tarefas recorrentes                                     | Cron jobs, pipelines CI                                   | [Tarefas agendadas](/pt/desktop-scheduled-tasks)                                                                                                                                                                                |
| Computer use                                            | [Ativar via `/mcp`](/pt/computer-use) no macOS            | [Controle de aplicativo e tela](#let-claude-use-your-computer) no macOS e Windows                                                                                                                                               |
| Integração Dispatch                                     | Não disponível                                            | [Sessões Dispatch](#sessions-from-dispatch) na barra lateral                                                                                                                                                                    |
| Scripting e automação                                   | [`--print`](/pt/cli-reference), [Agent SDK](/pt/headless) | Não disponível                                                                                                                                                                                                                  |

### What's not available in Desktop

Os seguintes recursos estão disponíveis apenas no CLI ou extensão VS Code:

* **Provedores de terceiros**: Desktop se conecta à API da Anthropic por padrão. Implantações corporativas podem configurar Vertex AI e provedores de gateway via [configurações gerenciadas](https://support.claude.com/en/articles/12622667-enterprise-configuration). Para Bedrock ou Foundry, use o [CLI](/pt/quickstart).
* **Linux**: o aplicativo desktop está disponível apenas em macOS e Windows. No Linux, use o [CLI](/pt/quickstart).
* **Sugestões de código inline**: Desktop não fornece sugestões no estilo autocompletar. Funciona através de prompts conversacionais e alterações de código explícitas.
* **Equipes de agentes**: orquestração multi-agente está disponível via [CLI](/pt/agent-teams) e [Agent SDK](/pt/headless), não em Desktop.
* **Comandos terminal-dialog**: comandos integrados que abrem um painel interativo no terminal, como `/permissions`, `/config`, `/agents` e `/doctor`, não estão disponíveis na aba Code e respondem com `isn't available in this environment`. Edite [arquivos de configuração](/pt/settings) diretamente para gerenciar regras de permissão e configuração, ou execute o comando a partir do CLI autônomo.

## Solução de problemas

As seções abaixo cobrem problemas específicos do aplicativo desktop. Para erros de API de tempo de execução que aparecem no chat como `API Error: 500`, `529 Overloaded`, `429` ou `Prompt is too long`, veja a [referência de erros](/pt/errors). Esses erros e suas correções são os mesmos em CLI, desktop e web.

### Verificar sua versão

Para ver qual versão do aplicativo desktop você está executando:

* **macOS**: clique em **Claude** na barra de menu, depois **About Claude**
* **Windows**: clique em **Help**, depois **About**

Clique no número da versão para copiá-lo para sua área de transferência.

### Erros 403 ou autenticação na aba Code

Se você vê `Error 403: Forbidden` ou outras falhas de autenticação ao usar a aba Code:

1. Saia e entre novamente no menu do aplicativo. Esta é a correção mais comum.
2. Verifique se você tem uma assinatura paga ativa: Pro, Max, Team ou Enterprise.
3. Se o CLI funciona mas Desktop não, saia completamente do aplicativo desktop, não apenas feche a janela, depois reabra e entre novamente.
4. Verifique sua conexão de internet e configurações de proxy.

### Tela em branco ou travada ao iniciar

Se o aplicativo abre mas mostra uma tela em branco ou não responsiva:

1. Reinicie o aplicativo.
2. Verifique se há atualizações pendentes. O aplicativo se atualiza automaticamente ao iniciar.
3. No Windows, verifique o Event Viewer para logs de crash em **Windows Logs → Application**.

### "Failed to load session"

Se você vê `Failed to load session`, a pasta selecionada pode não existir mais, um repositório Git pode exigir Git LFS que não está instalado, ou permissões de arquivo podem impedir acesso. Tente selecionar uma pasta diferente ou reinicie o aplicativo.

### Sessão não encontrando ferramentas instaladas

Se Claude não consegue encontrar ferramentas como `npm`, `node` ou outros comandos CLI, verifique se as ferramentas funcionam em seu terminal regular, verifique se seu perfil de shell configura adequadamente PATH e reinicie o aplicativo desktop para recarregar variáveis de ambiente.

### Erros de Git e Git LFS

No Windows, Git é necessário para a aba Code iniciar sessões locais. Se você vê "Git is required," instale [Git para Windows](https://git-scm.com/downloads/win) e reinicie o aplicativo.

Se você vê "Git LFS is required by this repository but is not installed," instale Git LFS de [git-lfs.com](https://git-lfs.com/), execute `git lfs install` e reinicie o aplicativo.

### MCP servers não funcionando no Windows

Se toggles de MCP server não respondem ou servidores falham em conectar no Windows, verifique se o servidor está adequadamente configurado em suas configurações, reinicie o aplicativo, verifique se o processo do servidor está em execução no Task Manager e revise logs do servidor para erros de conexão.

### Aplicativo não quer sair

* **macOS**: pressione Cmd+Q. Se o aplicativo não responder, use Force Quit com Cmd+Option+Esc, selecione Claude e clique Force Quit.
* **Windows**: use Task Manager com Ctrl+Shift+Esc para encerrar o processo Claude.

### Problemas específicos do Windows

* **PATH não atualizado após instalação**: abra uma nova janela de terminal. PATH é atualizado apenas para novas sessões de terminal.
* **Erro de instalação concorrente**: se você vê um erro sobre outra instalação em progresso mas não há uma, tente executar o instalador como Administrador.

### "Branch doesn't exist yet" ao abrir em CLI

Sessões remotas podem criar branches que não existem em sua máquina local. Clique no nome do branch na barra de ferramentas da sessão para copiá-lo, depois busque-o localmente:

```bash theme={null}
git fetch origin <branch-name>
git checkout <branch-name>
```

### Ainda preso?

* Pesquise ou registre um bug em [GitHub Issues](https://github.com/anthropics/claude-code/issues)
* Visite o [centro de suporte Claude](https://support.claude.com/)

Ao registrar um bug, inclua a versão do seu aplicativo desktop, seu sistema operacional, a mensagem de erro exata e logs relevantes. Em macOS, verifique Console.app. No Windows, verifique Event Viewer → Windows Logs → Application.
