> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Optimiza tu configuración de terminal

> Claude Code funciona mejor cuando tu terminal está correctamente configurada. Sigue estas directrices para optimizar tu experiencia.

### Temas y apariencia

Claude no puede controlar el tema de tu terminal. Eso se maneja por tu aplicación de terminal. Puedes hacer coincidir el tema de Claude Code con tu terminal en cualquier momento a través del comando `/config`.

Para personalización adicional de la interfaz de Claude Code en sí, puedes configurar una [línea de estado personalizada](/es/statusline) para mostrar información contextual como el modelo actual, directorio de trabajo o rama de git en la parte inferior de tu terminal.

### Saltos de línea

Tienes varias opciones para ingresar saltos de línea en Claude Code:

* **Escape rápido**: Escribe `\` seguido de Enter para crear una nueva línea
* **Shift+Enter**: Funciona de forma nativa en iTerm2, WezTerm, Ghostty y Kitty
* **Atajo de teclado**: Configura un enlace de tecla para insertar una nueva línea en otras terminales

**Configura Shift+Enter para otras terminales**

Ejecuta `/terminal-setup` dentro de Claude Code para configurar automáticamente Shift+Enter para VS Code, Alacritty, Zed y Warp.

<Note>
  El comando `/terminal-setup` solo es visible en terminales que requieren configuración manual. Si estás usando iTerm2, WezTerm, Ghostty o Kitty, no verás este comando porque Shift+Enter ya funciona de forma nativa.
</Note>

**Configura Option+Enter (VS Code, iTerm2 o macOS Terminal.app)**

**Para Mac Terminal.app:**

1. Abre Configuración → Perfiles → Teclado
2. Marca "Usar Opción como tecla Meta"

**Para iTerm2 y terminal de VS Code:**

1. Abre Configuración → Perfiles → Teclas
2. En General, establece la tecla Opción Izquierda/Derecha en "Esc+"

### Configuración de notificaciones

Nunca te pierdas cuando Claude completa una tarea con la configuración adecuada de notificaciones:

#### Notificaciones del sistema iTerm 2

Para alertas de iTerm 2 cuando se completan tareas:

1. Abre Preferencias de iTerm 2
2. Navega a Perfiles → Terminal
3. Habilita "Silenciar campana" y Filtrar Alertas → "Enviar alertas generadas por secuencia de escape"
4. Establece tu retraso de notificación preferido

Ten en cuenta que estas notificaciones son específicas de iTerm 2 y no están disponibles en la Terminal predeterminada de macOS.

#### Ganchos de notificación personalizados

Para manejo avanzado de notificaciones, puedes crear [ganchos de notificación](/es/hooks#notification) para ejecutar tu propia lógica.

### Manejo de entradas grandes

Cuando trabajes con código extenso o instrucciones largas:

* **Evita pegar directamente**: Claude Code puede tener dificultades con contenido pegado muy largo
* **Usa flujos de trabajo basados en archivos**: Escribe contenido en un archivo y pide a Claude que lo lea
* **Ten en cuenta las limitaciones de VS Code**: La terminal de VS Code es particularmente propensa a truncar pegados largos

### Modo Vim

Claude Code admite un subconjunto de enlaces de teclas Vim que se pueden habilitar con `/vim` o configurar a través de `/config`.

El subconjunto admitido incluye:

* Cambio de modo: `Esc` (a NORMAL), `i`/`I`, `a`/`A`, `o`/`O` (a INSERT)
* Navegación: `h`/`j`/`k`/`l`, `w`/`e`/`b`, `0`/`$`/`^`, `gg`/`G`, `f`/`F`/`t`/`T` con repetición `;`/`,`
* Edición: `x`, `dw`/`de`/`db`/`dd`/`D`, `cw`/`ce`/`cb`/`cc`/`C`, `.` (repetir)
* Copiar/pegar: `yy`/`Y`, `yw`/`ye`/`yb`, `p`/`P`
* Objetos de texto: `iw`/`aw`, `iW`/`aW`, `i"`/`a"`, `i'`/`a'`, `i(`/`a(`, `i[`/`a[`, `i{`/`a{`
* Indentación: `>>`/`<<`
* Operaciones de línea: `J` (unir líneas)

Consulta [Modo interactivo](/es/interactive-mode#vim-editor-mode) para la referencia completa.
