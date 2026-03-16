> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Modo interativo

> Referência completa para atalhos de teclado, modos de entrada e recursos interativos em sessões do Claude Code.

## Atalhos de teclado

<Note>
  Os atalhos de teclado podem variar por plataforma e terminal. Pressione `?` para ver os atalhos disponíveis para seu ambiente.

  **Usuários de macOS**: Os atalhos da tecla Option/Alt (`Alt+B`, `Alt+F`, `Alt+Y`, `Alt+M`, `Alt+P`) exigem configurar Option como Meta no seu terminal:

  * **iTerm2**: configurações → Profiles → Keys → defina Left/Right Option key para "Esc+"
  * **Terminal.app**: configurações → Profiles → Keyboard → marque "Use Option as Meta Key"
  * **VS Code**: configurações → Profiles → Keys → defina Left/Right Option key para "Esc+"

  Consulte [Configuração de terminal](/pt/terminal-config) para detalhes.
</Note>

### Controles gerais

| Atalho                                            | Descrição                                                                                     | Contexto                                                                                                     |
| :------------------------------------------------ | :-------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------- |
| `Ctrl+C`                                          | Cancelar entrada ou geração atual                                                             | Interrupção padrão                                                                                           |
| `Ctrl+F`                                          | Encerrar todos os agentes em segundo plano. Pressione duas vezes em 3 segundos para confirmar | Controle de agente em segundo plano                                                                          |
| `Ctrl+D`                                          | Sair da sessão do Claude Code                                                                 | Sinal EOF                                                                                                    |
| `Ctrl+G`                                          | Abrir no editor de texto padrão                                                               | Edite seu prompt ou resposta personalizada no seu editor de texto padrão                                     |
| `Ctrl+L`                                          | Limpar tela do terminal                                                                       | Mantém histórico de conversa                                                                                 |
| `Ctrl+O`                                          | Alternar saída detalhada                                                                      | Mostra uso e execução de ferramentas detalhados                                                              |
| `Ctrl+R`                                          | Pesquisa reversa no histórico de comandos                                                     | Pesquise através de comandos anteriores interativamente                                                      |
| `Ctrl+V` ou `Cmd+V` (iTerm2) ou `Alt+V` (Windows) | Colar imagem da área de transferência                                                         | Cola uma imagem ou caminho para um arquivo de imagem                                                         |
| `Ctrl+B`                                          | Tarefas em execução em segundo plano                                                          | Coloca comandos bash e agentes em segundo plano. Usuários de Tmux pressionam duas vezes                      |
| `Ctrl+T`                                          | Alternar lista de tarefas                                                                     | Mostrar ou ocultar a [lista de tarefas](#task-list) na área de status do terminal                            |
| `Left/Right arrows`                               | Ciclar através de abas de diálogo                                                             | Navegue entre abas em diálogos de permissão e menus                                                          |
| `Up/Down arrows`                                  | Navegar histórico de comandos                                                                 | Recuperar entradas anteriores                                                                                |
| `Esc` + `Esc`                                     | Retroceder ou resumir                                                                         | Restaurar código e/ou conversa para um ponto anterior, ou resumir a partir de uma mensagem selecionada       |
| `Shift+Tab` ou `Alt+M` (algumas configurações)    | Alternar modos de permissão                                                                   | Alternar entre Auto-Accept Mode, Plan Mode e modo normal.                                                    |
| `Option+P` (macOS) ou `Alt+P` (Windows/Linux)     | Alternar modelo                                                                               | Alternar modelos sem limpar seu prompt                                                                       |
| `Option+T` (macOS) ou `Alt+T` (Windows/Linux)     | Alternar pensamento estendido                                                                 | Ativar ou desativar modo de pensamento estendido. Execute `/terminal-setup` primeiro para ativar este atalho |

### Edição de texto

| Atalho                  | Descrição                            | Contexto                                                                                                           |
| :---------------------- | :----------------------------------- | :----------------------------------------------------------------------------------------------------------------- |
| `Ctrl+K`                | Deletar até o final da linha         | Armazena texto deletado para colar                                                                                 |
| `Ctrl+U`                | Deletar linha inteira                | Armazena texto deletado para colar                                                                                 |
| `Ctrl+Y`                | Colar texto deletado                 | Cole texto deletado com `Ctrl+K` ou `Ctrl+U`                                                                       |
| `Alt+Y` (após `Ctrl+Y`) | Ciclar histórico de cola             | Após colar, cicle através de texto deletado anteriormente. Requer [Option como Meta](#keyboard-shortcuts) no macOS |
| `Alt+B`                 | Mover cursor uma palavra para trás   | Navegação de palavra. Requer [Option como Meta](#keyboard-shortcuts) no macOS                                      |
| `Alt+F`                 | Mover cursor uma palavra para frente | Navegação de palavra. Requer [Option como Meta](#keyboard-shortcuts) no macOS                                      |

### Tema e exibição

| Atalho   | Descrição                                          | Contexto                                                                                                               |
| :------- | :------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+T` | Alternar destaque de sintaxe para blocos de código | Funciona apenas dentro do menu seletor `/theme`. Controla se o código nas respostas do Claude usa coloração de sintaxe |

<Note>
  O destaque de sintaxe está disponível apenas na compilação nativa do Claude Code.
</Note>

### Entrada multilinha

| Método                | Atalho            | Contexto                                           |
| :-------------------- | :---------------- | :------------------------------------------------- |
| Escape rápido         | `\` + `Enter`     | Funciona em todos os terminais                     |
| Padrão macOS          | `Option+Enter`    | Padrão no macOS                                    |
| Shift+Enter           | `Shift+Enter`     | Funciona pronto em iTerm2, WezTerm, Ghostty, Kitty |
| Sequência de controle | `Ctrl+J`          | Caractere de alimentação de linha para multilinha  |
| Modo de cola          | Colar diretamente | Para blocos de código, logs                        |

<Tip>
  Shift+Enter funciona sem configuração em iTerm2, WezTerm, Ghostty e Kitty. Para outros terminais (VS Code, Alacritty, Zed, Warp), execute `/terminal-setup` para instalar a ligação.
</Tip>

### Comandos rápidos

| Atalho        | Descrição                    | Notas                                                                     |
| :------------ | :--------------------------- | :------------------------------------------------------------------------ |
| `/` no início | Comando ou skill             | Consulte [comandos integrados](#built-in-commands) e [skills](/pt/skills) |
| `!` no início | Modo Bash                    | Execute comandos diretamente e adicione saída de execução à sessão        |
| `@`           | Menção de caminho de arquivo | Ativar preenchimento automático de caminho de arquivo                     |

## Comandos integrados

Digite `/` no Claude Code para ver todos os comandos disponíveis, ou digite `/` seguido de qualquer letra para filtrar. Nem todos os comandos são visíveis para todos os usuários. Alguns dependem de sua plataforma, plano ou ambiente. Por exemplo, `/desktop` aparece apenas no macOS e Windows, `/upgrade` e `/privacy-settings` estão disponíveis apenas em planos Pro e Max, e `/terminal-setup` fica oculto quando seu terminal suporta nativamente seus atalhos de teclado.

O Claude Code também vem com [skills agrupadas](/pt/skills#bundled-skills) como `/simplify`, `/batch` e `/debug` que aparecem junto com comandos integrados quando você digita `/`. Para criar seus próprios comandos, consulte [skills](/pt/skills).

Na tabela abaixo, `<arg>` indica um argumento obrigatório e `[arg]` indica um opcional.

| Comando                   | Propósito                                                                                                                                                                                                                                         |
| :------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `/add-dir <path>`         | Adicionar um novo diretório de trabalho à sessão atual                                                                                                                                                                                            |
| `/agents`                 | Gerenciar configurações de [agent](/pt/sub-agents)                                                                                                                                                                                                |
| `/btw <question>`         | Fazer uma [pergunta lateral](#side-questions-with-%2Fbtw) rápida sem adicionar à conversa                                                                                                                                                         |
| `/chrome`                 | Configurar configurações do [Claude no Chrome](/pt/chrome)                                                                                                                                                                                        |
| `/clear`                  | Limpar histórico de conversa e liberar contexto. Aliases: `/reset`, `/new`                                                                                                                                                                        |
| `/compact [instructions]` | Compactar conversa com instruções de foco opcionais                                                                                                                                                                                               |
| `/config`                 | Abrir a interface de [Configurações](/pt/settings) para ajustar tema, modelo, [estilo de saída](/pt/output-styles) e outras preferências. Alias: `/settings`                                                                                      |
| `/context`                | Visualizar uso de contexto atual como uma grade colorida                                                                                                                                                                                          |
| `/copy`                   | Copiar a última resposta do assistente para a área de transferência. Quando blocos de código estão presentes, mostra um seletor interativo para selecionar blocos individuais ou a resposta completa                                              |
| `/cost`                   | Mostrar estatísticas de uso de tokens. Consulte [guia de rastreamento de custos](/pt/costs#using-the-cost-command) para detalhes específicos de assinatura                                                                                        |
| `/desktop`                | Continuar a sessão atual no aplicativo Claude Code Desktop. Apenas macOS e Windows. Alias: `/app`                                                                                                                                                 |
| `/diff`                   | Abrir um visualizador de diff interativo mostrando alterações não confirmadas e diffs por turno. Use setas esquerda/direita para alternar entre o diff git atual e turnos individuais do Claude, e cima/baixo para navegar em arquivos            |
| `/doctor`                 | Diagnosticar e verificar sua instalação e configurações do Claude Code                                                                                                                                                                            |
| `/exit`                   | Sair do CLI. Alias: `/quit`                                                                                                                                                                                                                       |
| `/export [filename]`      | Exportar a conversa atual como texto simples. Com um nome de arquivo, escreve diretamente nesse arquivo. Sem, abre um diálogo para copiar para a área de transferência ou salvar em um arquivo                                                    |
| `/extra-usage`            | Configurar uso extra para continuar trabalhando quando os limites de taxa são atingidos                                                                                                                                                           |
| `/fast [on\|off]`         | Alternar [modo rápido](/pt/fast-mode) ativado ou desativado                                                                                                                                                                                       |
| `/feedback [report]`      | Enviar feedback sobre Claude Code. Alias: `/bug`                                                                                                                                                                                                  |
| `/fork [name]`            | Criar um fork da conversa atual neste ponto                                                                                                                                                                                                       |
| `/help`                   | Mostrar ajuda e comandos disponíveis                                                                                                                                                                                                              |
| `/hooks`                  | Gerenciar configurações de [hook](/pt/hooks) para eventos de ferramentas                                                                                                                                                                          |
| `/ide`                    | Gerenciar integrações de IDE e mostrar status                                                                                                                                                                                                     |
| `/init`                   | Inicializar projeto com guia `CLAUDE.md`                                                                                                                                                                                                          |
| `/insights`               | Gerar um relatório analisando suas sessões do Claude Code, incluindo áreas de projeto, padrões de interação e pontos de atrito                                                                                                                    |
| `/install-github-app`     | Configurar o aplicativo [Claude GitHub Actions](/pt/github-actions) para um repositório. Orienta você na seleção de um repositório e configuração da integração                                                                                   |
| `/install-slack-app`      | Instalar o aplicativo Claude Slack. Abre um navegador para completar o fluxo OAuth                                                                                                                                                                |
| `/keybindings`            | Abrir ou criar seu arquivo de configuração de atalhos de teclado                                                                                                                                                                                  |
| `/login`                  | Entrar em sua conta Anthropic                                                                                                                                                                                                                     |
| `/logout`                 | Sair de sua conta Anthropic                                                                                                                                                                                                                       |
| `/mcp`                    | Gerenciar conexões de servidor MCP e autenticação OAuth                                                                                                                                                                                           |
| `/memory`                 | Editar arquivos de memória `CLAUDE.md`, ativar ou desativar [auto-memory](/pt/memory#auto-memory) e visualizar entradas de auto-memory                                                                                                            |
| `/mobile`                 | Mostrar código QR para baixar o aplicativo Claude mobile. Aliases: `/ios`, `/android`                                                                                                                                                             |
| `/model [model]`          | Selecionar ou alterar o modelo de IA. Para modelos que suportam, use setas esquerda/direita para [ajustar nível de esforço](/pt/model-config#adjust-effort-level). A alteração entra em vigor imediatamente sem esperar a resposta atual terminar |
| `/passes`                 | Compartilhar uma semana gratuita do Claude Code com amigos. Visível apenas se sua conta for elegível                                                                                                                                              |
| `/permissions`            | Visualizar ou atualizar [permissões](/pt/permissions#manage-permissions). Alias: `/allowed-tools`                                                                                                                                                 |
| `/plan`                   | Entrar no modo plano diretamente do prompt                                                                                                                                                                                                        |
| `/plugin`                 | Gerenciar [plugins](/pt/plugins) do Claude Code                                                                                                                                                                                                   |
| `/pr-comments [PR]`       | Buscar e exibir comentários de uma solicitação de pull do GitHub. Detecta automaticamente o PR para o branch atual, ou passe uma URL ou número de PR. Requer o CLI `gh`                                                                           |
| `/privacy-settings`       | Visualizar e atualizar suas configurações de privacidade. Disponível apenas para assinantes de planos Pro e Max                                                                                                                                   |
| `/release-notes`          | Visualizar o changelog completo, com a versão mais recente mais próxima do seu prompt                                                                                                                                                             |
| `/reload-plugins`         | Recarregar todos os [plugins](/pt/plugins) ativos para aplicar alterações pendentes sem reiniciar. Relata o que foi carregado e anota quaisquer alterações que exijam reinicialização                                                             |
| `/remote-control`         | Disponibilizar esta sessão para [controle remoto](/pt/remote-control) do claude.ai. Alias: `/rc`                                                                                                                                                  |
| `/remote-env`             | Configurar o ambiente remoto padrão para [sessões de teleporte](/pt/claude-code-on-the-web#teleport-a-web-session-to-your-terminal)                                                                                                               |
| `/rename [name]`          | Renomear a sessão atual. Sem um nome, gera automaticamente um a partir do histórico de conversa                                                                                                                                                   |
| `/resume [session]`       | Retomar uma conversa por ID ou nome, ou abrir o seletor de sessão. Alias: `/continue`                                                                                                                                                             |
| `/review`                 | Descontinuado. Instale o [plugin `code-review`](https://github.com/anthropics/claude-code-marketplace/blob/main/code-review/README.md) em vez disso: `claude plugin install code-review@claude-code-marketplace`                                  |
| `/rewind`                 | Retroceder a conversa e/ou código para um ponto anterior, ou resumir a partir de uma mensagem selecionada. Consulte [checkpointing](/pt/checkpointing). Alias: `/checkpoint`                                                                      |
| `/sandbox`                | Alternar [modo sandbox](/pt/sandboxing). Disponível apenas em plataformas suportadas                                                                                                                                                              |
| `/security-review`        | Analisar alterações pendentes no branch atual para vulnerabilidades de segurança. Revisa o diff git e identifica riscos como injeção, problemas de autenticação e exposição de dados                                                              |
| `/skills`                 | Listar [skills](/pt/skills) disponíveis                                                                                                                                                                                                           |
| `/stats`                  | Visualizar uso diário, histórico de sessão, sequências e preferências de modelo                                                                                                                                                                   |
| `/status`                 | Abrir a interface de Configurações (aba Status) mostrando versão, modelo, conta e conectividade                                                                                                                                                   |
| `/statusline`             | Configurar a [linha de status](/pt/statusline) do Claude Code. Descreva o que você quer, ou execute sem argumentos para auto-configurar a partir do seu prompt de shell                                                                           |
| `/stickers`               | Encomendar adesivos do Claude Code                                                                                                                                                                                                                |
| `/tasks`                  | Listar e gerenciar tarefas em segundo plano                                                                                                                                                                                                       |
| `/terminal-setup`         | Configurar atalhos de teclado do terminal para Shift+Enter e outros atalhos. Visível apenas em terminais que precisam, como VS Code, Alacritty ou Warp                                                                                            |
| `/theme`                  | Alterar o tema de cor. Inclui variantes claro e escuro, temas acessíveis para daltônicos (daltonizados) e temas ANSI que usam a paleta de cores do seu terminal                                                                                   |
| `/upgrade`                | Abrir a página de upgrade para alternar para um nível de plano superior                                                                                                                                                                           |
| `/usage`                  | Mostrar limites de uso do plano e status de limite de taxa                                                                                                                                                                                        |
| `/vim`                    | Alternar entre modos de edição Vim e Normal                                                                                                                                                                                                       |

### MCP prompts

Os servidores MCP podem expor prompts que aparecem como comandos. Estes usam o formato `/mcp__<server>__<prompt>` e são descobertos dinamicamente a partir de servidores conectados. Consulte [MCP prompts](/pt/mcp#use-mcp-prompts-as-commands) para detalhes.

## Modo editor Vim

Ativar edição no estilo Vim com o comando `/vim` ou configurar permanentemente via `/config`.

### Alternância de modo

| Comando | Ação                       | Do modo |
| :------ | :------------------------- | :------ |
| `Esc`   | Entrar no modo NORMAL      | INSERT  |
| `i`     | Inserir antes do cursor    | NORMAL  |
| `I`     | Inserir no início da linha | NORMAL  |
| `a`     | Inserir após o cursor      | NORMAL  |
| `A`     | Inserir no final da linha  | NORMAL  |
| `o`     | Abrir linha abaixo         | NORMAL  |
| `O`     | Abrir linha acima          | NORMAL  |

### Navegação (modo NORMAL)

| Comando         | Ação                                                     |
| :-------------- | :------------------------------------------------------- |
| `h`/`j`/`k`/`l` | Mover esquerda/baixo/cima/direita                        |
| `w`             | Próxima palavra                                          |
| `e`             | Final da palavra                                         |
| `b`             | Palavra anterior                                         |
| `0`             | Início da linha                                          |
| `$`             | Final da linha                                           |
| `^`             | Primeiro caractere não em branco                         |
| `gg`            | Início da entrada                                        |
| `G`             | Final da entrada                                         |
| `f{char}`       | Pular para próxima ocorrência do caractere               |
| `F{char}`       | Pular para ocorrência anterior do caractere              |
| `t{char}`       | Pular para logo antes da próxima ocorrência do caractere |
| `T{char}`       | Pular para logo após a ocorrência anterior do caractere  |
| `;`             | Repetir último movimento f/F/t/T                         |
| `,`             | Repetir último movimento f/F/t/T em reverso              |

<Note>
  No modo normal vim, se o cursor estiver no início ou final da entrada e não puder se mover mais, as setas de navegação navegam pelo histórico de comandos em vez disso.
</Note>

### Edição (modo NORMAL)

| Comando        | Ação                                |
| :------------- | :---------------------------------- |
| `x`            | Deletar caractere                   |
| `dd`           | Deletar linha                       |
| `D`            | Deletar até o final da linha        |
| `dw`/`de`/`db` | Deletar palavra/até final/para trás |
| `cc`           | Alterar linha                       |
| `C`            | Alterar até o final da linha        |
| `cw`/`ce`/`cb` | Alterar palavra/até final/para trás |
| `yy`/`Y`       | Yancar (copiar) linha               |
| `yw`/`ye`/`yb` | Yancar palavra/até final/para trás  |
| `p`            | Colar após o cursor                 |
| `P`            | Colar antes do cursor               |
| `>>`           | Indentar linha                      |
| `<<`           | Desindentação de linha              |
| `J`            | Juntar linhas                       |
| `.`            | Repetir última alteração            |

### Objetos de texto (modo NORMAL)

Objetos de texto funcionam com operadores como `d`, `c` e `y`:

| Comando   | Ação                                                       |
| :-------- | :--------------------------------------------------------- |
| `iw`/`aw` | Palavra interna/ao redor                                   |
| `iW`/`aW` | PALAVRA interna/ao redor (delimitada por espaço em branco) |
| `i"`/`a"` | Aspas duplas internas/ao redor                             |
| `i'`/`a'` | Aspas simples internas/ao redor                            |
| `i(`/`a(` | Parênteses internos/ao redor                               |
| `i[`/`a[` | Colchetes internos/ao redor                                |
| `i{`/`a{` | Chaves internas/ao redor                                   |

## Histórico de comandos

O Claude Code mantém histórico de comandos para a sessão atual:

* O histórico de entrada é armazenado por diretório de trabalho
* O histórico de entrada é redefinido quando você executa `/clear` para iniciar uma nova sessão. A conversa da sessão anterior é preservada e pode ser retomada.
* Use setas Para cima/Para baixo para navegar (consulte atalhos de teclado acima)
* **Nota**: expansão de histórico (`!`) está desativada por padrão

### Pesquisa reversa com Ctrl+R

Pressione `Ctrl+R` para pesquisar interativamente através do seu histórico de comandos:

1. **Iniciar pesquisa**: pressione `Ctrl+R` para ativar pesquisa de histórico reverso
2. **Digitar consulta**: insira texto para pesquisar em comandos anteriores. O termo de pesquisa é destacado em resultados correspondentes
3. **Navegar correspondências**: pressione `Ctrl+R` novamente para ciclar através de correspondências mais antigas
4. **Aceitar correspondência**:
   * Pressione `Tab` ou `Esc` para aceitar a correspondência atual e continuar editando
   * Pressione `Enter` para aceitar e executar o comando imediatamente
5. **Cancelar pesquisa**:
   * Pressione `Ctrl+C` para cancelar e restaurar sua entrada original
   * Pressione `Backspace` em pesquisa vazia para cancelar

A pesquisa exibe comandos correspondentes com o termo de pesquisa destacado, para que você possa encontrar e reutilizar entradas anteriores.

## Comandos bash em segundo plano

O Claude Code suporta a execução de comandos bash em segundo plano, permitindo que você continue trabalhando enquanto processos de longa duração são executados.

### Como o backgrounding funciona

Quando o Claude Code executa um comando em segundo plano, ele executa o comando de forma assíncrona e retorna imediatamente um ID de tarefa em segundo plano. O Claude Code pode responder a novos prompts enquanto o comando continua sendo executado em segundo plano.

Para executar comandos em segundo plano, você pode:

* Solicitar ao Claude Code para executar um comando em segundo plano
* Pressionar Ctrl+B para mover uma invocação regular da ferramenta Bash para o segundo plano. (Usuários de Tmux devem pressionar Ctrl+B duas vezes devido à tecla de prefixo do tmux.)

**Recursos principais:**

* A saída é armazenada em buffer e o Claude pode recuperá-la usando a ferramenta TaskOutput
* Tarefas em segundo plano têm IDs únicos para rastreamento e recuperação de saída
* Tarefas em segundo plano são limpas automaticamente quando o Claude Code sai

Para desativar toda a funcionalidade de tarefa em segundo plano, defina a variável de ambiente `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` como `1`. Consulte [Variáveis de ambiente](/pt/settings#environment-variables) para detalhes.

**Comandos comuns em segundo plano:**

* Ferramentas de compilação (webpack, vite, make)
* Gerenciadores de pacotes (npm, yarn, pnpm)
* Executores de teste (jest, pytest)
* Servidores de desenvolvimento
* Processos de longa duração (docker, terraform)

### Modo Bash com prefixo `!`

Execute comandos bash diretamente sem passar pelo Claude prefixando sua entrada com `!`:

```bash  theme={null}
! npm test
! git status
! ls -la
```

Modo Bash:

* Adiciona o comando e sua saída ao contexto de conversa
* Mostra progresso e saída em tempo real
* Suporta o mesmo backgrounding `Ctrl+B` para comandos de longa duração
* Não requer que Claude interprete ou aprove o comando
* Suporta preenchimento automático baseado em histórico: digite um comando parcial e pressione **Tab** para completar a partir de comandos `!` anteriores no projeto atual
* Sair com `Escape`, `Backspace` ou `Ctrl+U` em um prompt vazio

Isso é útil para operações rápidas de shell enquanto mantém contexto de conversa.

## Sugestões de prompt

Quando você abre uma sessão pela primeira vez, um comando de exemplo acinzentado aparece na entrada de prompt para ajudá-lo a começar. O Claude Code escolhe isso do histórico git do seu projeto, então reflete arquivos nos quais você tem trabalhado recentemente.

Após o Claude responder, as sugestões continuam a aparecer com base no seu histórico de conversa, como uma etapa de acompanhamento de uma solicitação de várias partes ou uma continuação natural do seu fluxo de trabalho.

* Pressione **Tab** para aceitar a sugestão, ou pressione **Enter** para aceitar e enviar
* Comece a digitar para descartá-la

A sugestão é executada como uma solicitação em segundo plano que reutiliza o cache de prompt da conversa pai, então o custo adicional é mínimo. O Claude Code pula a geração de sugestão quando o cache está frio para evitar custo desnecessário.

As sugestões são automaticamente puladas após o primeiro turno de uma conversa, em modo não interativo e em modo plano.

Para desativar completamente as sugestões de prompt, defina a variável de ambiente ou alterne a configuração em `/config`:

```bash  theme={null}
export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false
```

## Perguntas laterais com /btw

Use `/btw` para fazer uma pergunta rápida sobre seu trabalho atual sem adicionar ao histórico de conversa. Isso é útil quando você quer uma resposta rápida mas não quer bagunçar o contexto principal ou desviar o Claude de uma tarefa de longa duração.

```
/btw what was the name of that config file again?
```

Perguntas laterais têm visibilidade completa da conversa atual, então você pode perguntar sobre código que o Claude já leu, decisões que tomou anteriormente ou qualquer outra coisa da sessão. A pergunta e resposta são efêmeras: aparecem em uma sobreposição descartável e nunca entram no histórico de conversa.

* **Disponível enquanto o Claude está trabalhando**: você pode executar `/btw` mesmo enquanto o Claude está processando uma resposta. A pergunta lateral é executada independentemente e não interrompe o turno principal.
* **Sem acesso a ferramentas**: perguntas laterais respondem apenas a partir do que já está em contexto. O Claude não pode ler arquivos, executar comandos ou pesquisar ao responder uma pergunta lateral.
* **Resposta única**: não há turnos de acompanhamento. Se você precisar de uma conversa de ida e volta, use um prompt normal em vez disso.
* **Custo baixo**: a pergunta lateral reutiliza o cache de prompt da conversa pai, então o custo adicional é mínimo.

Pressione **Space**, **Enter** ou **Escape** para descartar a resposta e retornar ao prompt.

`/btw` é o inverso de um [subagent](/pt/sub-agents): vê sua conversa completa mas não tem ferramentas, enquanto um subagent tem ferramentas completas mas começa com contexto vazio. Use `/btw` para perguntar sobre o que o Claude já sabe desta sessão; use um subagent para descobrir algo novo.

## Lista de tarefas

Ao trabalhar em trabalho complexo e de várias etapas, o Claude cria uma lista de tarefas para rastrear o progresso. As tarefas aparecem na área de status do seu terminal com indicadores mostrando o que está pendente, em progresso ou completo.

* Pressione `Ctrl+T` para alternar a visualização da lista de tarefas. A exibição mostra até 10 tarefas por vez
* Para ver todas as tarefas ou limpá-las, peça ao Claude diretamente: "show me all tasks" ou "clear all tasks"
* As tarefas persistem através de compactações de contexto, ajudando o Claude a se manter organizado em projetos maiores
* Para compartilhar uma lista de tarefas entre sessões, defina `CLAUDE_CODE_TASK_LIST_ID` para usar um diretório nomeado em `~/.claude/tasks/`: `CLAUDE_CODE_TASK_LIST_ID=my-project claude`
* Para reverter para a lista TODO anterior, defina `CLAUDE_CODE_ENABLE_TASKS=false`.

## Status de revisão de PR

Ao trabalhar em um branch com uma solicitação de pull aberta, o Claude Code exibe um link de PR clicável no rodapé (por exemplo, "PR #446"). O link tem um sublinhado colorido indicando o estado de revisão:

* Verde: aprovado
* Amarelo: revisão pendente
* Vermelho: alterações solicitadas
* Cinza: rascunho
* Roxo: mesclado

`Cmd+click` (Mac) ou `Ctrl+click` (Windows/Linux) no link para abrir a solicitação de pull no seu navegador. O status é atualizado automaticamente a cada 60 segundos.

<Note>
  O status de PR requer que o CLI `gh` esteja instalado e autenticado (`gh auth login`).
</Note>

## Veja também

* [Skills](/pt/skills) - Prompts e fluxos de trabalho personalizados
* [Checkpointing](/pt/checkpointing) - Retroceder edições do Claude e restaurar estados anteriores
* [Referência CLI](/pt/cli-reference) - Sinalizadores e opções de linha de comando
* [Configurações](/pt/settings) - Opções de configuração
* [Gerenciamento de memória](/pt/memory) - Gerenciando arquivos CLAUDE.md
