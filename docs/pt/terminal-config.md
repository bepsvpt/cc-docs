> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Otimize sua configuração de terminal

> Claude Code funciona melhor quando seu terminal está devidamente configurado. Siga estas diretrizes para otimizar sua experiência.

### Temas e aparência

Claude não pode controlar o tema do seu terminal. Isso é tratado pela sua aplicação de terminal. Você pode corresponder o tema do Claude Code ao seu terminal a qualquer momento através do comando `/config`.

Para personalização adicional da interface do Claude Code em si, você pode configurar uma [linha de status personalizada](/pt/statusline) para exibir informações contextuais como o modelo atual, diretório de trabalho ou branch do git na parte inferior do seu terminal.

### Quebras de linha

Você tem várias opções para inserir quebras de linha no Claude Code:

* **Escape rápido**: Digite `\` seguido de Enter para criar uma nova linha
* **Shift+Enter**: Funciona imediatamente no iTerm2, WezTerm, Ghostty e Kitty
* **Atalho de teclado**: Configure uma associação de tecla para inserir uma nova linha em outros terminais

**Configure Shift+Enter para outros terminais**

Execute `/terminal-setup` dentro do Claude Code para configurar automaticamente Shift+Enter para VS Code, Alacritty, Zed e Warp.

<Note>
  O comando `/terminal-setup` é visível apenas em terminais que requerem configuração manual. Se você estiver usando iTerm2, WezTerm, Ghostty ou Kitty, você não verá este comando porque Shift+Enter já funciona nativamente.
</Note>

**Configure Option+Enter (VS Code, iTerm2 ou macOS Terminal.app)**

**Para Mac Terminal.app:**

1. Abra Configurações → Perfis → Teclado
2. Marque "Usar Option como Meta Key"

**Para terminal iTerm2 e VS Code:**

1. Abra Configurações → Perfis → Teclas
2. Em Geral, defina a tecla Option Esquerda/Direita como "Esc+"

### Configuração de notificações

Nunca perca quando Claude completa uma tarefa com configuração adequada de notificações:

#### Notificações do sistema iTerm 2

Para alertas do iTerm 2 quando as tarefas são concluídas:

1. Abra Preferências do iTerm 2
2. Navegue até Perfis → Terminal
3. Ative "Silence bell" e Filtrar Alertas → "Enviar alertas gerados por sequência de escape"
4. Defina seu atraso de notificação preferido

Observe que essas notificações são específicas do iTerm 2 e não estão disponíveis no Terminal padrão do macOS.

#### Hooks de notificação personalizados

Para tratamento avançado de notificações, você pode criar [hooks de notificação](/pt/hooks#notification) para executar sua própria lógica.

### Tratamento de entradas grandes

Ao trabalhar com código extenso ou instruções longas:

* **Evite colagem direta**: Claude Code pode ter dificuldades com conteúdo colado muito longo
* **Use fluxos de trabalho baseados em arquivo**: Escreva o conteúdo em um arquivo e peça ao Claude para lê-lo
* **Esteja ciente das limitações do VS Code**: O terminal do VS Code é particularmente propenso a truncar colagens longas

### Modo Vim

Claude Code suporta um subconjunto de associações de teclas Vim que podem ser ativadas com `/vim` ou configuradas via `/config`.

O subconjunto suportado inclui:

* Alternância de modo: `Esc` (para NORMAL), `i`/`I`, `a`/`A`, `o`/`O` (para INSERT)
* Navegação: `h`/`j`/`k`/`l`, `w`/`e`/`b`, `0`/`$`/`^`, `gg`/`G`, `f`/`F`/`t`/`T` com repetição `;`/`,`
* Edição: `x`, `dw`/`de`/`db`/`dd`/`D`, `cw`/`ce`/`cb`/`cc`/`C`, `.` (repetir)
* Yanque/colar: `yy`/`Y`, `yw`/`ye`/`yb`, `p`/`P`
* Objetos de texto: `iw`/`aw`, `iW`/`aW`, `i"`/`a"`, `i'`/`a'`, `i(`/`a(`, `i[`/`a[`, `i{`/`a{`
* Indentação: `>>`/`<<`
* Operações de linha: `J` (juntar linhas)

Veja [Modo interativo](/pt/interactive-mode#vim-editor-mode) para a referência completa.
