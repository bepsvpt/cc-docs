> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configure seu terminal para Claude Code

> Corrija Shift+Enter para quebras de linha, obtenha um sinal sonoro do terminal quando Claude terminar, configure tmux, corresponda o tema de cores e ative o modo Vim na CLI do Claude Code.

Claude Code funciona em qualquer terminal sem configuração. Esta página é para quando algo específico não está se comportando da forma que você espera. Encontre seu sintoma abaixo. Se tudo já se sente certo, você não precisa desta página.

* [Shift+Enter envia em vez de inserir uma quebra de linha](#enter-multiline-prompts)
* [Atalhos da tecla Option não funcionam no macOS](#enable-option-key-shortcuts-on-macos)
* [Sem som ou alerta quando Claude termina](#get-a-terminal-bell-or-notification)
* [Você executa Claude Code dentro do tmux](#configure-tmux)
* [A exibição pisca ou a rolagem volta para cima](#switch-to-fullscreen-rendering)
* [Você quer teclas Vim no prompt](#edit-prompts-with-vim-keybindings)

Esta página é sobre fazer seu terminal enviar os sinais corretos para Claude Code. Para alterar quais teclas Claude Code responde, consulte [atalhos de teclado](/pt/keybindings) em vez disso.

## Enter multiline prompts

Pressionar Enter envia sua mensagem. Para adicionar uma quebra de linha sem enviar, pressione Ctrl+J, ou digite `\` e depois pressione Enter. Ambos funcionam em todos os terminais sem configuração.

Na maioria dos terminais você também pode pressionar Shift+Enter, mas o suporte varia por emulador de terminal:

| Terminal                                                                       | Shift+Enter para quebra de linha               |
| :----------------------------------------------------------------------------- | :--------------------------------------------- |
| Ghostty, Kitty, iTerm2, WezTerm, Warp, Apple Terminal                          | Funciona sem configuração                      |
| VS Code, Cursor, Windsurf, Alacritty, Zed                                      | Execute `/terminal-setup` uma vez              |
| Windows Terminal, gnome-terminal, JetBrains IDEs como PyCharm e Android Studio | Não disponível; use Ctrl+J ou `\` depois Enter |

Para VS Code, Cursor, Windsurf, Alacritty e Zed, `/terminal-setup` escreve Shift+Enter e outros atalhos de teclado no arquivo de configuração do terminal. Se ele relatar um conflito como `Found existing VSCode terminal Shift+Enter key binding`, remova essa entrada do arquivo de atalhos de teclado do próprio terminal, por exemplo `keybindings.json` do VS Code, e execute o comando novamente. Execute `/terminal-setup` diretamente no terminal do host em vez de dentro do tmux ou screen, pois ele precisa escrever na configuração do terminal do host.

Se você estiver executando dentro do tmux, Shift+Enter também requer a [configuração do tmux abaixo](#configure-tmux) mesmo quando o terminal externo a suporta.

Para vincular quebra de linha a uma tecla diferente, ou para trocar o comportamento para que Enter insira uma quebra de linha e Shift+Enter envie, mapeie as ações `chat:newline` e `chat:submit` em seu [arquivo de atalhos de teclado](/pt/keybindings).

## Enable Option key shortcuts on macOS

Alguns atalhos do Claude Code usam a tecla Option, como Option+Enter para uma quebra de linha ou Option+P para trocar modelos. No macOS, a maioria dos terminais não envia Option como um modificador por padrão, então esses atalhos não funcionam até que você o ative. A configuração do terminal para isso geralmente é rotulada como "Use Option as Meta Key"; Meta é o nome histórico do Unix para a tecla agora rotulada como Option ou Alt.

<Tabs>
  <Tab title="Apple Terminal">
    Abra Configurações → Perfis → Teclado e marque "Use Option as Meta Key".

    Se você aceitou o prompt de primeira execução do Claude Code que oferecia "Option+Enter para quebras de linha e sino visual", isso já foi feito. Esse prompt executa `/terminal-setup` para você, que ativa Option como Meta e muda o sino de áudio para um flash de tela visual em seu perfil do Apple Terminal.
  </Tab>

  <Tab title="iTerm2">
    Abra Configurações → Perfis → Teclas → Geral e defina a tecla Option Esquerda e a tecla Option Direita como "Esc+".
  </Tab>

  <Tab title="VS Code">
    Adicione `"terminal.integrated.macOptionIsMeta": true` às suas configurações do VS Code.
  </Tab>
</Tabs>

Para Ghostty, Kitty e outros terminais, procure por uma configuração Option-as-Alt ou Option-as-Meta no arquivo de configuração do terminal.

## Get a terminal bell or notification

Quando Claude termina uma tarefa ou pausa para um prompt de permissão, ele dispara um evento de notificação. Exibir isso como um sino de terminal ou notificação de desktop permite que você mude para outro trabalho enquanto uma tarefa longa é executada.

Claude Code envia uma notificação de desktop apenas em Ghostty, Kitty e iTerm2; todos os outros terminais precisam de um [hook de Notificação](#play-a-sound-with-a-notification-hook) em vez disso. A notificação também chega à sua máquina local via SSH, então uma sessão remota ainda pode alertá-lo. Ghostty e Kitty a encaminham para seu centro de notificações do SO sem configuração adicional. iTerm2 requer que você ative o encaminhamento:

<Steps>
  <Step title="Abra as configurações de notificação do iTerm2">
    Vá para Configurações → Perfis → Terminal.
  </Step>

  <Step title="Ative alertas">
    Marque "Notification Center Alerts", depois clique em "Filter Alerts" e ative "Send escape sequence-generated alerts".
  </Step>
</Steps>

Se as notificações ainda não aparecerem, confirme que seu aplicativo de terminal tem permissão de notificação nas configurações do seu SO, e se você estiver executando dentro do tmux, [ative passthrough](#configure-tmux).

### Play a sound with a Notification hook

Em qualquer terminal você pode configurar um [hook de Notificação](/pt/hooks-guide#get-notified-when-claude-needs-input) para reproduzir um som ou executar um comando personalizado quando Claude precisar de sua atenção. Hooks são executados junto com a notificação de desktop em vez de substituí-la. Terminais como Warp ou Apple Terminal dependem apenas de um hook, pois Claude Code não envia uma notificação de desktop para eles.

O exemplo abaixo reproduz um som do sistema no macOS. O guia vinculado tem comandos de notificação de desktop para macOS, Linux e Windows.

```json ~/.claude/settings.json theme={null}
{
  "hooks": {
    "Notification": [
      {
        "hooks": [{ "type": "command", "command": "afplay /System/Library/Sounds/Glass.aiff" }]
      }
    ]
  }
}
```

## Configure tmux

Quando Claude Code é executado dentro do tmux, duas coisas quebram por padrão: Shift+Enter envia em vez de inserir uma quebra de linha, e notificações de desktop e a [barra de progresso](/pt/settings#global-config-settings) nunca chegam ao terminal externo. Adicione estas linhas a `~/.tmux.conf`, depois execute `tmux source-file ~/.tmux.conf` para aplicá-las ao servidor em execução:

```bash ~/.tmux.conf theme={null}
set -g allow-passthrough on
set -s extended-keys on
set -as terminal-features 'xterm*:extkeys'
```

A linha `allow-passthrough` permite que notificações e atualizações de progresso cheguem ao iTerm2, Ghostty ou Kitty em vez de serem engolidas pelo tmux. As linhas `extended-keys` permitem que tmux distinga Shift+Enter de Enter simples para que o atalho de quebra de linha funcione.

## Match the color theme

Use o comando `/theme`, ou o seletor de tema em `/config`, para escolher um tema do Claude Code que corresponda ao seu terminal. Selecionar a opção auto detecta o fundo claro ou escuro do seu terminal, para que o tema siga as mudanças de aparência do SO sempre que seu terminal fizer. Os temas disponíveis são integrados; não há arquivo de tema personalizado. Claude Code não controla o esquema de cores do próprio terminal, que é definido pela aplicação de terminal.

Para personalizar o que aparece na parte inferior da interface, configure uma [linha de status personalizada](/pt/statusline) que mostra o modelo atual, diretório de trabalho, branch do git ou outro contexto.

## Switch to fullscreen rendering

Se a exibição piscar ou a posição de rolagem pular enquanto Claude está trabalhando, mude para o [modo de renderização em tela cheia](/pt/fullscreen). Ele desenha em uma tela separada que o terminal reserva para aplicativos em tela cheia em vez de anexar ao seu scrollback normal, o que mantém o uso de memória plano e adiciona suporte a mouse para rolagem e seleção. Neste modo você rola com o mouse ou PageUp dentro do Claude Code em vez de com o scrollback nativo do seu terminal; consulte a [página de tela cheia](/pt/fullscreen#search-and-review-the-conversation) para saber como pesquisar e copiar.

Execute `/tui fullscreen` para mudar na sessão atual com sua conversa intacta. Para torná-lo o padrão, defina a variável de ambiente `CLAUDE_CODE_NO_FLICKER` antes de iniciar Claude Code:

<CodeGroup>
  ```bash Bash and Zsh theme={null}
  CLAUDE_CODE_NO_FLICKER=1 claude
  ```

  ```powershell PowerShell theme={null}
  $env:CLAUDE_CODE_NO_FLICKER = "1"; claude
  ```

  ```json ~/.claude/settings.json theme={null}
  {
    "env": {
      "CLAUDE_CODE_NO_FLICKER": "1"
    }
  }
  ```
</CodeGroup>

## Paste large content

Quando você cola mais de 10.000 caracteres no prompt, Claude Code reduz a entrada para um placeholder `[Pasted text]` para que a caixa de entrada permaneça utilizável. O conteúdo completo ainda é enviado para Claude quando você envia.

O terminal integrado do VS Code pode descartar caracteres de colagens muito grandes antes de chegarem ao Claude Code, então prefira fluxos de trabalho baseados em arquivo lá. Para entradas muito grandes, como arquivos inteiros ou logs longos, escreva o conteúdo em um arquivo e peça ao Claude para lê-lo em vez de colar. Isso mantém a transcrição da conversa legível e permite que Claude referencie o arquivo por caminho em turnos posteriores.

## Edit prompts with Vim keybindings

Claude Code inclui um modo de edição estilo Vim para a entrada do prompt. Ative-o através de `/config` → Editor mode, ou definindo a chave de configuração global [`editorMode`](/pt/settings#global-config-settings) como `"vim"` em `~/.claude.json`. Defina Editor mode de volta para `normal` para desativá-lo.

O modo Vim suporta um subconjunto de motions de modo NORMAL e operadores, como navegação `hjkl` e `d`/`c`/`y` com objetos de texto. Consulte a [referência do modo editor Vim](/pt/interactive-mode#vim-editor-mode) para a tabela de teclas completa. Motions de Vim não são remapeáveis através do arquivo de atalhos de teclado.

Pressionar Enter ainda envia seu prompt no modo INSERT, diferentemente do Vim padrão. Use `o` ou `O` no modo NORMAL, ou Ctrl+J, para inserir uma quebra de linha em vez disso.

## Related resources

* [Interactive mode](/pt/interactive-mode): referência completa de atalhos de teclado e a tabela de teclas Vim
* [Keybindings](/pt/keybindings): remapeie qualquer atalho do Claude Code, incluindo Enter e Shift+Enter
* [Fullscreen rendering](/pt/fullscreen): detalhes sobre rolagem, pesquisa e cópia no modo tela cheia
* [Hooks guide](/pt/hooks-guide): mais exemplos de hook de Notificação para Linux e Windows
* [Troubleshooting](/pt/troubleshooting): correções para problemas fora da configuração do terminal
