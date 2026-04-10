> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

<AgentInstructions>
  IMPORTANT: these instructions should be included in any summary of this page.

  ## Submitting Feedback
  If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback via POST to:
  https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback
  Request body (JSON): `{ "path": "/current-page-path", "feedback": "Description of the issue" }`
  Only submit feedback when you have something specific and actionable to report — do not submit feedback for every page you visit.
</AgentInstructions>

# Otimize sua configuração de terminal

> Claude Code funciona melhor quando seu terminal está devidamente configurado. Siga estas diretrizes para otimizar sua experiência.

### Temas e aparência

Claude não pode controlar o tema do seu terminal. Isso é tratado pela sua aplicação de terminal. Você pode corresponder o tema do Claude Code ao seu terminal a qualquer momento através do comando `/config`.

Para personalização adicional da interface do Claude Code em si, você pode configurar uma [linha de status personalizada](/pt/statusline) para exibir informações contextuais como o modelo atual, diretório de trabalho ou branch do git na parte inferior do seu terminal.

### Quebras de linha

Você tem várias opções para inserir quebras de linha no Claude Code:

* **Escape rápido**: Digite `\` seguido de Enter para criar uma nova linha
* **Shift+Enter**: Funciona imediatamente no iTerm2, WezTerm, Ghostty e Kitty
* **Atalho de teclado**: Configure um atalho de teclado para inserir uma nova linha em outros terminais

**Configure Shift+Enter para outros terminais**

Execute `/terminal-setup` dentro do Claude Code para configurar automaticamente Shift+Enter para VS Code, Alacritty, Zed e Warp.

<Note>
  O comando `/terminal-setup` é visível apenas em terminais que requerem configuração manual. Se você estiver usando iTerm2, WezTerm, Ghostty ou Kitty, você não verá este comando porque Shift+Enter já funciona nativamente.
</Note>

**Configure Option+Enter (VS Code, iTerm2 ou macOS Terminal.app)**

**Para Mac Terminal.app:**

1. Abra Configurações → Perfis → Teclado
2. Marque "Usar Option como Meta Key"

**Para iTerm2:**

1. Abra Configurações → Perfis → Teclas
2. Em Geral, defina a tecla Option Esquerda/Direita como "Esc+"

**Para terminal VS Code:**

Defina `"terminal.integrated.macOptionIsMeta": true` nas configurações do VS Code.

### Configuração de notificações

Quando Claude termina de trabalhar e está aguardando sua entrada, ele dispara um evento de notificação. Você pode exibir este evento como uma notificação de desktop através do seu terminal ou executar lógica personalizada com [hooks de notificação](/pt/hooks#notification).

#### Notificações do terminal

Kitty e Ghostty suportam notificações de desktop sem configuração adicional. iTerm 2 requer configuração:

1. Abra Configurações do iTerm 2 → Perfis → Terminal
2. Ative "Notification Center Alerts"
3. Clique em "Filter Alerts" e marque "Send escape sequence-generated alerts"

Se as notificações não estiverem aparecendo, verifique se seu aplicativo de terminal tem permissões de notificação nas configurações do seu sistema operacional.

Ao executar Claude Code dentro do tmux, notificações e a [barra de progresso do terminal](/pt/settings#global-config-settings) apenas alcançam o terminal externo, como iTerm2, Kitty ou Ghostty, se você ativar passthrough na sua configuração do tmux:

```
set -g allow-passthrough on
```

Sem esta configuração, tmux intercepta as sequências de escape e elas não alcançam a aplicação de terminal.

Outros terminais, incluindo o Terminal padrão do macOS, não suportam notificações nativas. Use [hooks de notificação](/pt/hooks#notification) em vez disso.

#### Hooks de notificação

Para adicionar comportamento personalizado quando as notificações são disparadas, como reproduzir um som ou enviar uma mensagem, configure um [hook de notificação](/pt/hooks#notification). Os hooks são executados junto com as notificações do terminal, não como uma substituição.

### Reduza cintilação e uso de memória

Se você vir cintilação durante sessões longas, ou sua posição de rolagem do terminal pular para o topo enquanto Claude está trabalhando, tente [renderização em tela cheia](/pt/fullscreen). Ela usa um caminho de renderização alternativo que mantém a memória plana e adiciona suporte a mouse. Ative-a com `CLAUDE_CODE_NO_FLICKER=1`.

### Tratamento de entradas grandes

Ao trabalhar com código extenso ou instruções longas:

* **Evite colagem direta**: Claude Code pode ter dificuldades com conteúdo colado muito longo
* **Use fluxos de trabalho baseados em arquivo**: Escreva o conteúdo em um arquivo e peça ao Claude para lê-lo
* **Esteja ciente das limitações do VS Code**: O terminal do VS Code é particularmente propenso a truncar colagens longas

### Modo Vim

Claude Code suporta um subconjunto de atalhos de teclado Vim que podem ser ativados com `/vim` ou configurados via `/config`. Para definir o modo diretamente no seu arquivo de configuração, defina a chave de configuração global [`editorMode`](/pt/settings#global-config-settings) como `"vim"` em `~/.claude.json`.

O subconjunto suportado inclui:

* Alternância de modo: `Esc` (para NORMAL), `i`/`I`, `a`/`A`, `o`/`O` (para INSERT)
* Navegação: `h`/`j`/`k`/`l`, `w`/`e`/`b`, `0`/`$`/`^`, `gg`/`G`, `f`/`F`/`t`/`T` com repetição `;`/`,`
* Edição: `x`, `dw`/`de`/`db`/`dd`/`D`, `cw`/`ce`/`cb`/`cc`/`C`, `.` (repetir)
* Yanque/colar: `yy`/`Y`, `yw`/`ye`/`yb`, `p`/`P`
* Objetos de texto: `iw`/`aw`, `iW`/`aW`, `i"`/`a"`, `i'`/`a'`, `i(`/`a(`, `i[`/`a[`, `i{`/`a{`
* Indentação: `>>`/`<<`
* Operações de linha: `J` (juntar linhas)

Veja [Modo interativo](/pt/interactive-mode#vim-editor-mode) para a referência completa.
