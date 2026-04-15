> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Modo interativo

> Referência completa para atalhos de teclado, modos de entrada e recursos interativos em sessões do Claude Code.

## Atalhos de teclado

<Note>
  Os atalhos de teclado podem variar por plataforma e terminal. Pressione `?` para ver os atalhos disponíveis para seu ambiente.

  **Usuários de macOS**: Os atalhos da tecla Option/Alt (`Alt+B`, `Alt+F`, `Alt+Y`, `Alt+M`, `Alt+P`, `Alt+T`) exigem configurar Option como Meta no seu terminal:

  * **iTerm2**: configurações → Profiles → Keys → defina Left/Right Option key para "Esc+"
  * **Terminal.app**: configurações → Profiles → Keyboard → marque "Use Option as Meta Key"
  * **VS Code**: defina `"terminal.integrated.macOptionIsMeta": true` nas configurações do VS Code

  Veja [Configuração de terminal](/pt/terminal-config) para detalhes.
</Note>

### Controles gerais

| Atalho                                            | Descrição                                                                                     | Contexto                                                                                                                                                                     |
| :------------------------------------------------ | :-------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+C`                                          | Cancelar entrada ou geração atual                                                             | Interrupção padrão                                                                                                                                                           |
| `Ctrl+X Ctrl+K`                                   | Encerrar todos os agentes em segundo plano. Pressione duas vezes em 3 segundos para confirmar | Controle de agente em segundo plano                                                                                                                                          |
| `Ctrl+D`                                          | Sair da sessão do Claude Code                                                                 | Sinal EOF                                                                                                                                                                    |
| `Ctrl+G` ou `Ctrl+X Ctrl+E`                       | Abrir no editor de texto padrão                                                               | Edite seu prompt ou resposta personalizada no seu editor de texto padrão. `Ctrl+X Ctrl+E` é a ligação nativa do readline                                                     |
| `Ctrl+L`                                          | Redesenhar a tela                                                                             | Redesenha a interface do usuário atual sem limpar o histórico de conversa                                                                                                    |
| `Ctrl+O`                                          | Alternar saída detalhada                                                                      | Mostra uso e execução de ferramentas detalhados. Também expande chamadas de leitura e pesquisa do MCP, que se contraem para uma única linha como "Queried slack" por padrão  |
| `Ctrl+R`                                          | Pesquisa reversa no histórico de comandos                                                     | Pesquise através de comandos anteriores interativamente                                                                                                                      |
| `Ctrl+V` ou `Cmd+V` (iTerm2) ou `Alt+V` (Windows) | Colar imagem da área de transferência                                                         | Insere um chip `[Image #N]` no cursor para que você possa referenciá-lo posicionalmente no seu prompt                                                                        |
| `Ctrl+B`                                          | Tarefas em execução em segundo plano                                                          | Coloca comandos bash e agentes em segundo plano. Usuários de Tmux pressione duas vezes                                                                                       |
| `Ctrl+T`                                          | Alternar lista de tarefas                                                                     | Mostrar ou ocultar a [lista de tarefas](#task-list) na área de status do terminal                                                                                            |
| `Left/Right arrows`                               | Ciclar através de abas de diálogo                                                             | Navegue entre abas em diálogos de permissão e menus                                                                                                                          |
| `Up/Down arrows`                                  | Navegar histórico de comandos                                                                 | Recuperar entradas anteriores                                                                                                                                                |
| `Esc` + `Esc`                                     | Retroceder ou resumir                                                                         | Restaurar código e/ou conversa para um ponto anterior, ou resumir a partir de uma mensagem selecionada                                                                       |
| `Shift+Tab` ou `Alt+M` (algumas configurações)    | Alternar modos de permissão                                                                   | Alternar entre `default`, `acceptEdits`, `plan` e qualquer modo que você tenha ativado, como `auto` ou `bypassPermissions`. Veja [modos de permissão](/pt/permission-modes). |
| `Option+P` (macOS) ou `Alt+P` (Windows/Linux)     | Alternar modelo                                                                               | Alternar modelos sem limpar seu prompt                                                                                                                                       |
| `Option+T` (macOS) ou `Alt+T` (Windows/Linux)     | Alternar pensamento estendido                                                                 | Ativar ou desativar modo de pensamento estendido. No macOS, configure seu terminal para enviar Option como Meta para que este atalho funcione                                |
| `Option+O` (macOS) ou `Alt+O` (Windows/Linux)     | Alternar modo rápido                                                                          | Ativar ou desativar [modo rápido](/pt/fast-mode)                                                                                                                             |

### Edição de texto

| Atalho                  | Descrição                               | Contexto                                                                                                           |
| :---------------------- | :-------------------------------------- | :----------------------------------------------------------------------------------------------------------------- |
| `Ctrl+K`                | Deletar até o final da linha            | Armazena texto deletado para colar                                                                                 |
| `Ctrl+U`                | Deletar do cursor até o início da linha | Armazena texto deletado para colar. Repita para limpar entre linhas em entrada multilinha                          |
| `Ctrl+Y`                | Colar texto deletado                    | Cole texto deletado com `Ctrl+K` ou `Ctrl+U`                                                                       |
| `Alt+Y` (após `Ctrl+Y`) | Ciclar histórico de cola                | Após colar, cicle através de texto deletado anteriormente. Requer [Option como Meta](#keyboard-shortcuts) no macOS |
| `Alt+B`                 | Mover cursor uma palavra para trás      | Navegação de palavra. Requer [Option como Meta](#keyboard-shortcuts) no macOS                                      |
| `Alt+F`                 | Mover cursor uma palavra para frente    | Navegação de palavra. Requer [Option como Meta](#keyboard-shortcuts) no macOS                                      |

### Tema e exibição

| Atalho   | Descrição                                          | Contexto                                                                                                               |
| :------- | :------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+T` | Alternar destaque de sintaxe para blocos de código | Funciona apenas dentro do menu seletor `/theme`. Controla se o código nas respostas do Claude usa coloração de sintaxe |

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

| Atalho        | Descrição                    | Notas                                                                 |
| :------------ | :--------------------------- | :-------------------------------------------------------------------- |
| `/` no início | Comando ou skill             | Veja [comandos integrados](#built-in-commands) e [skills](/pt/skills) |
| `!` no início | Modo Bash                    | Execute comandos diretamente e adicione saída de execução à sessão    |
| `@`           | Menção de caminho de arquivo | Ativar preenchimento automático de caminho de arquivo                 |

### Visualizador de transcrição

Quando o visualizador de transcrição está aberto (alternado com `Ctrl+O`), estes atalhos estão disponíveis. `Ctrl+E` pode ser reatribuído via [`transcript:toggleShowAll`](/pt/keybindings).

| Atalho               | Descrição                                                                                                          |
| :------------------- | :----------------------------------------------------------------------------------------------------------------- |
| `Ctrl+E`             | Alternar mostrar todo o conteúdo                                                                                   |
| `q`, `Ctrl+C`, `Esc` | Sair da visualização de transcrição. Todos os três podem ser reatribuídos via [`transcript:exit`](/pt/keybindings) |

### Entrada de voz

| Atalho         | Descrição            | Notas                                                                                                                                                                |
| :------------- | :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Manter `Space` | Ditação push-to-talk | Requer que [ditação de voz](/pt/voice-dictation) esteja ativada. A transcrição é inserida no cursor. [Reatribuível](/pt/voice-dictation#rebind-the-push-to-talk-key) |

## Comandos integrados

Digite `/` no Claude Code para ver todos os comandos disponíveis, ou digite `/` seguido de qualquer letra para filtrar. O menu `/` mostra tanto comandos integrados quanto [skills agrupados](/pt/skills#bundled-skills) como `/simplify`. Nem todos os comandos são visíveis para todos os usuários, pois alguns dependem de sua plataforma ou plano.

Veja a [referência de comandos](/pt/commands) para a lista completa de comandos integrados. Para criar seus próprios comandos, veja [skills](/pt/skills).

## Modo editor Vim

Ative edição no estilo vim com o comando `/vim` ou configure permanentemente via `/config`.

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
  No modo normal vim, se o cursor estiver no início ou final da entrada e não puder se mover mais, as setas de navegação navegam pelo histórico de comandos.
</Note>

### Edição (modo NORMAL)

| Comando        | Ação                                |
| :------------- | :---------------------------------- |
| `x`            | Deletar caractere                   |
| `dd`           | Deletar linha                       |
| `D`            | Deletar até o final da linha        |
| `dw`/`de`/`db` | Deletar palavra/até final/para trás |
| `cc`           | Mudar linha                         |
| `C`            | Mudar até o final da linha          |
| `cw`/`ce`/`cb` | Mudar palavra/até final/para trás   |
| `yy`/`Y`       | Yancar (copiar) linha               |
| `yw`/`ye`/`yb` | Yancar palavra/até final/para trás  |
| `p`            | Colar após o cursor                 |
| `P`            | Colar antes do cursor               |
| `>>`           | Indentar linha                      |
| `<<`           | Desindentação de linha              |
| `J`            | Juntar linhas                       |
| `.`            | Repetir última mudança              |

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

Claude Code mantém histórico de comandos para a sessão atual:

* O histórico de entrada é armazenado por diretório de trabalho
* O histórico de entrada é redefinido quando você executa `/clear` para iniciar uma nova sessão. A conversa da sessão anterior é preservada e pode ser retomada.
* Use as setas Para cima/Para baixo para navegar (veja atalhos de teclado acima)
* **Nota**: expansão de histórico (`!`) está desabilitada por padrão

### Pesquisa reversa com Ctrl+R

Pressione `Ctrl+R` para pesquisar interativamente através do seu histórico de comandos:

1. **Iniciar pesquisa**: pressione `Ctrl+R` para ativar pesquisa de histórico reverso
2. **Digitar consulta**: insira texto para pesquisar em comandos anteriores. O termo de pesquisa é destacado nos resultados correspondentes
3. **Navegar correspondências**: pressione `Ctrl+R` novamente para ciclar através de correspondências mais antigas
4. **Aceitar correspondência**:
   * Pressione `Tab` ou `Esc` para aceitar a correspondência atual e continuar editando
   * Pressione `Enter` para aceitar e executar o comando imediatamente
5. **Cancelar pesquisa**:
   * Pressione `Ctrl+C` para cancelar e restaurar sua entrada original
   * Pressione `Backspace` em pesquisa vazia para cancelar

A pesquisa exibe comandos correspondentes com o termo de pesquisa destacado, para que você possa encontrar e reutilizar entradas anteriores.

## Comandos bash em segundo plano

Claude Code suporta execução de comandos bash em segundo plano, permitindo que você continue trabalhando enquanto processos de longa duração são executados.

### Como o segundo plano funciona

Quando Claude Code executa um comando em segundo plano, ele executa o comando de forma assíncrona e retorna imediatamente um ID de tarefa em segundo plano. Claude Code pode responder a novos prompts enquanto o comando continua sendo executado em segundo plano.

Para executar comandos em segundo plano, você pode:

* Solicitar ao Claude Code para executar um comando em segundo plano
* Pressionar Ctrl+B para mover uma invocação regular da ferramenta Bash para o segundo plano. (Usuários de Tmux devem pressionar Ctrl+B duas vezes devido à tecla de prefixo do tmux.)

**Recursos principais:**

* A saída é escrita em um arquivo e Claude pode recuperá-la usando a ferramenta Read
* Tarefas em segundo plano têm IDs únicos para rastreamento e recuperação de saída
* Tarefas em segundo plano são limpas automaticamente quando Claude Code sai
* Tarefas em segundo plano são automaticamente encerradas se a saída exceder 5GB, com uma nota em stderr explicando o motivo

Para desabilitar toda a funcionalidade de tarefa em segundo plano, defina a variável de ambiente `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` para `1`. Veja [Variáveis de ambiente](/pt/env-vars) para detalhes.

**Comandos comuns em segundo plano:**

* Ferramentas de compilação (webpack, vite, make)
* Gerenciadores de pacotes (npm, yarn, pnpm)
* Executores de teste (jest, pytest)
* Servidores de desenvolvimento
* Processos de longa duração (docker, terraform)

### Modo Bash com prefixo `!`

Execute comandos bash diretamente sem passar por Claude prefixando sua entrada com `!`:

```bash theme={null}
! npm test
! git status
! ls -la
```

Modo Bash:

* Adiciona o comando e sua saída ao contexto de conversa
* Mostra progresso e saída em tempo real
* Suporta o mesmo segundo plano `Ctrl+B` para comandos de longa duração
* Não requer que Claude interprete ou aprove o comando
* Suporta preenchimento automático baseado em histórico: digite um comando parcial e pressione **Tab** para completar a partir de comandos `!` anteriores no projeto atual
* Saia com `Escape`, `Backspace` ou `Ctrl+U` em um prompt vazio
* Colar texto que começa com `!` em um prompt vazio entra no modo bash automaticamente, correspondendo ao comportamento digitado `!`

Isso é útil para operações rápidas de shell mantendo contexto de conversa.

## Sugestões de prompt

Quando você abre uma sessão pela primeira vez, um comando de exemplo acinzentado aparece na entrada de prompt para ajudá-lo a começar. Claude Code escolhe isso do histórico git do seu projeto, então reflete arquivos nos quais você trabalhou recentemente.

Após Claude responder, as sugestões continuam aparecendo com base no seu histórico de conversa, como uma etapa de acompanhamento de uma solicitação de várias partes ou uma continuação natural do seu fluxo de trabalho.

* Pressione **Tab** ou **Right arrow** para aceitar a sugestão, ou pressione **Enter** para aceitar e enviar
* Comece a digitar para descartá-la

A sugestão é executada como uma solicitação em segundo plano que reutiliza o cache de prompt da conversa pai, então o custo adicional é mínimo. Claude Code pula a geração de sugestão quando o cache está frio para evitar custo desnecessário.

As sugestões são automaticamente puladas após a primeira volta de uma conversa, em modo não interativo e em plan mode.

Para desabilitar sugestões de prompt inteiramente, defina a variável de ambiente ou alterne a configuração em `/config`:

```bash theme={null}
export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false
```

## Perguntas laterais com /btw

Use `/btw` para fazer uma pergunta rápida sobre seu trabalho atual sem adicionar ao histórico de conversa. Isso é útil quando você quer uma resposta rápida mas não quer bagunçar o contexto principal ou desviar Claude de uma tarefa de longa duração.

```
/btw what was the name of that config file again?
```

Perguntas laterais têm visibilidade completa da conversa atual, então você pode perguntar sobre código que Claude já leu, decisões que tomou anteriormente, ou qualquer outra coisa da sessão. A pergunta e resposta são efêmeras: aparecem em uma sobreposição descartável e nunca entram no histórico de conversa.

* **Disponível enquanto Claude está trabalhando**: você pode executar `/btw` mesmo enquanto Claude está processando uma resposta. A pergunta lateral é executada independentemente e não interrompe a volta principal.
* **Sem acesso a ferramentas**: perguntas laterais respondem apenas a partir do que já está em contexto. Claude não pode ler arquivos, executar comandos ou pesquisar ao responder uma pergunta lateral.
* **Resposta única**: não há voltas de acompanhamento. Se você precisar de uma conversa de ida e volta, use um prompt normal.
* **Custo baixo**: a pergunta lateral reutiliza o cache de prompt da conversa pai, então o custo adicional é mínimo.

Pressione **Space**, **Enter** ou **Escape** para descartar a resposta e retornar ao prompt.

`/btw` é o inverso de um [subagent](/pt/sub-agents): vê sua conversa completa mas não tem ferramentas, enquanto um subagent tem ferramentas completas mas começa com contexto vazio. Use `/btw` para perguntar sobre o que Claude já sabe desta sessão; use um subagent para descobrir algo novo.

## Lista de tarefas

Ao trabalhar em trabalho complexo e multi-etapas, Claude cria uma lista de tarefas para rastrear progresso. As tarefas aparecem na área de status do seu terminal com indicadores mostrando o que está pendente, em progresso ou completo.

* Pressione `Ctrl+T` para alternar a visualização da lista de tarefas. A exibição mostra até 10 tarefas por vez
* Para ver todas as tarefas ou limpá-las, peça ao Claude diretamente: "show me all tasks" ou "clear all tasks"
* As tarefas persistem através de compactações de contexto, ajudando Claude a se manter organizado em projetos maiores
* Para compartilhar uma lista de tarefas entre sessões, defina `CLAUDE_CODE_TASK_LIST_ID` para usar um diretório nomeado em `~/.claude/tasks/`: `CLAUDE_CODE_TASK_LIST_ID=my-project claude`

## Status de revisão de PR

Ao trabalhar em uma branch com um pull request aberto, Claude Code exibe um link de PR clicável no rodapé (por exemplo, "PR #446"). O link tem um sublinhado colorido indicando o estado de revisão:

* Verde: aprovado
* Amarelo: revisão pendente
* Vermelho: mudanças solicitadas
* Cinza: rascunho
* Roxo: mesclado

`Cmd+click` (Mac) ou `Ctrl+click` (Windows/Linux) no link para abrir o pull request no seu navegador. O status é atualizado automaticamente a cada 60 segundos.

<Note>
  O status de PR requer que o CLI `gh` esteja instalado e autenticado (`gh auth login`).
</Note>

## Veja também

* [Skills](/pt/skills) - Prompts e fluxos de trabalho personalizados
* [Checkpointing](/pt/checkpointing) - Retroceder edições do Claude e restaurar estados anteriores
* [Referência CLI](/pt/cli-reference) - Sinalizadores e opções de linha de comando
* [Configurações](/pt/settings) - Opções de configuração
* [Gerenciamento de memória](/pt/memory) - Gerenciando arquivos CLAUDE.md
