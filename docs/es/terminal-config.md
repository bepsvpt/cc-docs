> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configura tu terminal para Claude Code

> Corrige Shift+Enter para saltos de línea, obtén una campana de terminal cuando Claude termine, configura tmux, haz coincidir el tema de color y habilita el modo Vim en la CLI de Claude Code.

Claude Code funciona en cualquier terminal sin configuración. Esta página es para cuando algo específico no se comporta como esperas. Encuentra tu síntoma a continuación. Si todo ya se siente bien, no necesitas esta página.

* [Shift+Enter envía en lugar de insertar un salto de línea](#enter-multiline-prompts)
* [Los atajos de tecla Option no funcionan en macOS](#enable-option-key-shortcuts-on-macos)
* [Sin sonido ni alerta cuando Claude termina](#get-a-terminal-bell-or-notification)
* [Ejecutas Claude Code dentro de tmux](#configure-tmux)
* [La pantalla parpadea o el desplazamiento salta](#switch-to-fullscreen-rendering)
* [Quieres teclas Vim en el indicador](#edit-prompts-with-vim-keybindings)

Esta página trata sobre lograr que tu terminal envíe las señales correctas a Claude Code. Para cambiar qué teclas responde Claude Code, consulta [atajos de teclado](/es/keybindings) en su lugar.

## Ingresa indicadores multilínea

Presionar Enter envía tu mensaje. Para agregar un salto de línea sin enviar, presiona Ctrl+J, o escribe `\` y luego presiona Enter. Ambos funcionan en cada terminal sin configuración.

En la mayoría de terminales también puedes presionar Shift+Enter, pero el soporte varía según el emulador de terminal:

| Terminal                                                                          | Shift+Enter para salto de línea             |
| :-------------------------------------------------------------------------------- | :------------------------------------------ |
| Ghostty, Kitty, iTerm2, WezTerm, Warp, Apple Terminal                             | Funciona sin configuración                  |
| VS Code, Cursor, Windsurf, Alacritty, Zed                                         | Ejecuta `/terminal-setup` una vez           |
| Windows Terminal, gnome-terminal, IDEs de JetBrains como PyCharm y Android Studio | No disponible; usa Ctrl+J o `\` luego Enter |

Para VS Code, Cursor, Windsurf, Alacritty y Zed, `/terminal-setup` escribe Shift+Enter y otros atajos de teclado en el archivo de configuración de la terminal. Si reporta un conflicto como `Found existing VSCode terminal Shift+Enter key binding`, elimina esa entrada del archivo de atajos de teclado de la terminal, por ejemplo `keybindings.json` de VS Code, y ejecuta el comando nuevamente. Ejecuta `/terminal-setup` directamente en la terminal del host en lugar de dentro de tmux o screen, ya que necesita escribir en la configuración de la terminal del host.

Si estás ejecutando dentro de tmux, Shift+Enter también requiere la [configuración de tmux a continuación](#configure-tmux) incluso cuando la terminal externa la soporta.

Para vincular salto de línea a una tecla diferente, o para intercambiar el comportamiento de modo que Enter inserte un salto de línea y Shift+Enter envíe, mapea las acciones `chat:newline` y `chat:submit` en tu [archivo de atajos de teclado](/es/keybindings).

## Habilita atajos de tecla Option en macOS

Algunos atajos de Claude Code usan la tecla Option, como Option+Enter para un salto de línea u Option+P para cambiar modelos. En macOS, la mayoría de terminales no envían Option como modificador por defecto, por lo que estos atajos no hacen nada hasta que lo habilites. La configuración de terminal para esto generalmente se etiqueta como "Use Option as Meta Key"; Meta es el nombre histórico de Unix para la tecla ahora etiquetada como Option o Alt.

<Tabs>
  <Tab title="Apple Terminal">
    Abre Configuración → Perfiles → Teclado y marca "Use Option as Meta Key".

    Si aceptaste el indicador de primera ejecución de Claude Code que ofrecía "Option+Enter para saltos de línea y campana visual", esto ya está hecho. Ese indicador ejecuta `/terminal-setup` para ti, que habilita Option como Meta y cambia la campana de audio a un destello de pantalla visual en tu perfil de Apple Terminal.
  </Tab>

  <Tab title="iTerm2">
    Abre Configuración → Perfiles → Teclas → General y establece la tecla Option Izquierda y la tecla Option Derecha en "Esc+".
  </Tab>

  <Tab title="VS Code">
    Agrega `"terminal.integrated.macOptionIsMeta": true` a tu configuración de VS Code.
  </Tab>
</Tabs>

Para Ghostty, Kitty y otras terminales, busca una configuración de Option-as-Alt u Option-as-Meta en el archivo de configuración de la terminal.

## Obtén una campana de terminal o notificación

Cuando Claude termina una tarea o se pausa para un indicador de permiso, dispara un evento de notificación. Mostrar esto como una campana de terminal o notificación de escritorio te permite cambiar a otro trabajo mientras se ejecuta una tarea larga.

Claude Code envía una notificación de escritorio solo en Ghostty, Kitty e iTerm2; cada otra terminal necesita un [gancho de Notificación](#play-a-sound-with-a-notification-hook) en su lugar. La notificación también llega a tu máquina local sobre SSH, por lo que una sesión remota aún puede alertarte. Ghostty y Kitty la reenvían a tu centro de notificaciones del SO sin configuración adicional. iTerm2 requiere que habilites el reenvío:

<Steps>
  <Step title="Abre la configuración de notificaciones de iTerm2">
    Ve a Configuración → Perfiles → Terminal.
  </Step>

  <Step title="Habilita alertas">
    Marca "Notification Center Alerts", luego haz clic en "Filter Alerts" y habilita "Send escape sequence-generated alerts".
  </Step>
</Steps>

Si las notificaciones aún no aparecen, confirma que tu aplicación de terminal tenga permiso de notificación en tu configuración del SO, y si estás ejecutando dentro de tmux, [habilita passthrough](#configure-tmux).

### Reproduce un sonido con un gancho de Notificación

En cualquier terminal puedes configurar un [gancho de Notificación](/es/hooks-guide#get-notified-when-claude-needs-input) para reproducir un sonido o ejecutar un comando personalizado cuando Claude necesite tu atención. Los ganchos se ejecutan junto con la notificación de escritorio en lugar de reemplazarla. Terminales como Warp o Apple Terminal dependen de un gancho solo ya que Claude Code no les envía una notificación de escritorio.

El ejemplo a continuación reproduce un sonido del sistema en macOS. La guía vinculada tiene comandos de notificación de escritorio para macOS, Linux y Windows.

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

## Configura tmux

Cuando Claude Code se ejecuta dentro de tmux, dos cosas se rompen por defecto: Shift+Enter envía en lugar de insertar un salto de línea, y las notificaciones de escritorio y la [barra de progreso](/es/settings#global-config-settings) nunca llegan a la terminal externa. Agrega estas líneas a `~/.tmux.conf`, luego ejecuta `tmux source-file ~/.tmux.conf` para aplicarlas al servidor en ejecución:

```bash ~/.tmux.conf theme={null}
set -g allow-passthrough on
set -s extended-keys on
set -as terminal-features 'xterm*:extkeys'
```

La línea `allow-passthrough` permite que las notificaciones y actualizaciones de progreso lleguen a iTerm2, Ghostty o Kitty en lugar de ser tragadas por tmux. Las líneas `extended-keys` permiten que tmux distinga Shift+Enter de Enter simple para que el atajo de salto de línea funcione.

## Haz coincidir el tema de color

Usa el comando `/theme`, o el selector de tema en `/config`, para elegir un tema de Claude Code que coincida con tu terminal. Seleccionar la opción auto detecta el fondo claro u oscuro de tu terminal, por lo que el tema sigue los cambios de apariencia del SO siempre que tu terminal lo haga. Los temas disponibles están integrados; no hay archivo de tema personalizado. Claude Code no controla el esquema de color de la terminal, que se establece por la aplicación de terminal.

Para personalizar lo que aparece en la parte inferior de la interfaz, configura una [línea de estado personalizada](/es/statusline) que muestre el modelo actual, directorio de trabajo, rama de git u otro contexto.

## Cambia a renderizado a pantalla completa

Si la pantalla parpadea o la posición de desplazamiento salta mientras Claude está trabajando, cambia al [modo de renderizado a pantalla completa](/es/fullscreen). Dibuja en una pantalla separada que la terminal reserva para aplicaciones a pantalla completa en lugar de agregar a tu desplazamiento normal, lo que mantiene el uso de memoria plano y agrega soporte de ratón para desplazamiento y selección. En este modo desplazas con el ratón o PageUp dentro de Claude Code en lugar de con el desplazamiento nativo de tu terminal; consulta la [página de pantalla completa](/es/fullscreen#search-and-review-the-conversation) para saber cómo buscar y copiar.

Ejecuta `/tui fullscreen` para cambiar en la sesión actual con tu conversación intacta. Para hacerlo el predeterminado, establece la variable de entorno `CLAUDE_CODE_NO_FLICKER` antes de iniciar Claude Code:

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

## Pega contenido grande

Cuando pegas más de 10,000 caracteres en el indicador, Claude Code colapsa la entrada a un marcador de posición `[Pasted text]` para que la caja de entrada siga siendo utilizable. El contenido completo aún se envía a Claude cuando envías.

La terminal integrada de VS Code puede soltar caracteres de pegados muy grandes antes de que lleguen a Claude Code, así que prefiere flujos de trabajo basados en archivos allí. Para entradas muy grandes como archivos completos o registros largos, escribe el contenido en un archivo y pide a Claude que lo lea en lugar de pegar. Esto mantiene la transcripción de conversación legible y permite que Claude haga referencia al archivo por ruta en turnos posteriores.

## Edita indicadores con atajos de teclado Vim

Claude Code incluye un modo de edición de estilo Vim para la entrada del indicador. Habilítalo a través de `/config` → Editor mode, o estableciendo la clave de configuración global [`editorMode`](/es/settings#global-config-settings) en `"vim"` en `~/.claude.json`. Establece Editor mode de nuevo en `normal` para desactivarlo.

El modo Vim soporta un subconjunto de movimientos y operadores de modo NORMAL, como navegación `hjkl` y `d`/`c`/`y` con objetos de texto. Consulta la [referencia del modo editor Vim](/es/interactive-mode#vim-editor-mode) para la tabla de teclas completa. Los movimientos Vim no son remapeables a través del archivo de atajos de teclado.

Presionar Enter aún envía tu indicador en modo INSERT, a diferencia del Vim estándar. Usa `o` u `O` en modo NORMAL, o Ctrl+J, para insertar un salto de línea en su lugar.

## Recursos relacionados

* [Modo interactivo](/es/interactive-mode): referencia completa de atajos de teclado y tabla de teclas Vim
* [Atajos de teclado](/es/keybindings): remapea cualquier atajo de Claude Code, incluyendo Enter y Shift+Enter
* [Renderizado a pantalla completa](/es/fullscreen): detalles sobre desplazamiento, búsqueda y copia en modo pantalla completa
* [Guía de ganchos](/es/hooks-guide): más ejemplos de ganchos de Notificación para Linux y Windows
* [Solución de problemas](/es/troubleshooting): correcciones para problemas fuera de la configuración de terminal
