> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Modo interactivo

> Referencia completa de atajos de teclado, modos de entrada y características interactivas en sesiones de Claude Code.

## Atajos de teclado

<Note>
  Los atajos de teclado pueden variar según la plataforma y la terminal. Presione `?` para ver los atajos disponibles en su entorno.

  **Usuarios de macOS**: Los atajos de la tecla Option/Alt (`Alt+B`, `Alt+F`, `Alt+Y`, `Alt+M`, `Alt+P`) requieren configurar Option como Meta en su terminal:

  * **iTerm2**: configuración → Perfiles → Teclas → establecer la tecla Option izquierda/derecha en "Esc+"
  * **Terminal.app**: configuración → Perfiles → Teclado → marcar "Usar Option como tecla Meta"
  * **VS Code**: configuración → Perfiles → Teclas → establecer la tecla Option izquierda/derecha en "Esc+"

  Consulte [Configuración de terminal](/es/terminal-config) para obtener más detalles.
</Note>

### Controles generales

| Atajo                                           | Descripción                                                                                  | Contexto                                                                                                               |
| :---------------------------------------------- | :------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+C`                                        | Cancelar entrada o generación actual                                                         | Interrupción estándar                                                                                                  |
| `Ctrl+F`                                        | Terminar todos los agentes en segundo plano. Presione dos veces en 3 segundos para confirmar | Control de agentes en segundo plano                                                                                    |
| `Ctrl+D`                                        | Salir de la sesión de Claude Code                                                            | Señal EOF                                                                                                              |
| `Ctrl+G`                                        | Abrir en el editor de texto predeterminado                                                   | Editar su prompt o respuesta personalizada en su editor de texto predeterminado                                        |
| `Ctrl+L`                                        | Limpiar pantalla de terminal                                                                 | Mantiene el historial de conversación                                                                                  |
| `Ctrl+O`                                        | Alternar salida detallada                                                                    | Muestra el uso detallado de herramientas y ejecución                                                                   |
| `Ctrl+R`                                        | Búsqueda inversa del historial de comandos                                                   | Buscar a través de comandos anteriores de forma interactiva                                                            |
| `Ctrl+V` o `Cmd+V` (iTerm2) o `Alt+V` (Windows) | Pegar imagen desde el portapapeles                                                           | Pega una imagen o ruta a un archivo de imagen                                                                          |
| `Ctrl+B`                                        | Tareas en ejecución en segundo plano                                                         | Pone en segundo plano comandos bash y agentes. Los usuarios de Tmux presionan dos veces                                |
| `Ctrl+T`                                        | Alternar lista de tareas                                                                     | Mostrar u ocultar la [lista de tareas](#task-list) en el área de estado de la terminal                                 |
| `Flechas izquierda/derecha`                     | Ciclar a través de pestañas de diálogo                                                       | Navegar entre pestañas en diálogos de permisos y menús                                                                 |
| `Flechas arriba/abajo`                          | Navegar por el historial de comandos                                                         | Recuperar entradas anteriores                                                                                          |
| `Esc` + `Esc`                                   | Rebobinar o resumir                                                                          | Restaurar código y/o conversación a un punto anterior, o resumir desde un mensaje seleccionado                         |
| `Shift+Tab` o `Alt+M` (algunas configuraciones) | Alternar modos de permisos                                                                   | Cambiar entre Modo de Aceptación Automática, Plan Mode y modo normal.                                                  |
| `Option+P` (macOS) o `Alt+P` (Windows/Linux)    | Cambiar modelo                                                                               | Cambiar modelos sin borrar su prompt                                                                                   |
| `Option+T` (macOS) o `Alt+T` (Windows/Linux)    | Alternar pensamiento extendido                                                               | Habilitar o deshabilitar el modo de pensamiento extendido. Ejecute `/terminal-setup` primero para habilitar este atajo |

### Edición de texto

| Atajo                         | Descripción                             | Contexto                                                                                                                       |
| :---------------------------- | :-------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+K`                      | Eliminar hasta el final de la línea     | Almacena el texto eliminado para pegarlo                                                                                       |
| `Ctrl+U`                      | Eliminar línea completa                 | Almacena el texto eliminado para pegarlo                                                                                       |
| `Ctrl+Y`                      | Pegar texto eliminado                   | Pegar texto eliminado con `Ctrl+K` o `Ctrl+U`                                                                                  |
| `Alt+Y` (después de `Ctrl+Y`) | Ciclar por el historial de pegado       | Después de pegar, ciclar a través del texto eliminado anteriormente. Requiere [Option como Meta](#keyboard-shortcuts) en macOS |
| `Alt+B`                       | Mover cursor una palabra hacia atrás    | Navegación de palabras. Requiere [Option como Meta](#keyboard-shortcuts) en macOS                                              |
| `Alt+F`                       | Mover cursor una palabra hacia adelante | Navegación de palabras. Requiere [Option como Meta](#keyboard-shortcuts) en macOS                                              |

### Tema y visualización

| Atajo    | Descripción                                           | Contexto                                                                                                                       |
| :------- | :---------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+T` | Alternar resaltado de sintaxis para bloques de código | Solo funciona dentro del menú del selector `/theme`. Controla si el código en las respuestas de Claude usa colores de sintaxis |

<Note>
  El resaltado de sintaxis solo está disponible en la compilación nativa de Claude Code.
</Note>

### Entrada multilínea

| Método                  | Atajo              | Contexto                                                      |
| :---------------------- | :----------------- | :------------------------------------------------------------ |
| Escape rápido           | `\` + `Enter`      | Funciona en todas las terminales                              |
| Predeterminado de macOS | `Option+Enter`     | Predeterminado en macOS                                       |
| Shift+Enter             | `Shift+Enter`      | Funciona sin configuración en iTerm2, WezTerm, Ghostty, Kitty |
| Secuencia de control    | `Ctrl+J`           | Carácter de salto de línea para multilínea                    |
| Modo de pegado          | Pegar directamente | Para bloques de código, registros                             |

<Tip>
  Shift+Enter funciona sin configuración en iTerm2, WezTerm, Ghostty y Kitty. Para otras terminales (VS Code, Alacritty, Zed, Warp), ejecute `/terminal-setup` para instalar el enlace.
</Tip>

### Comandos rápidos

| Atajo         | Descripción                | Notas                                                                     |
| :------------ | :------------------------- | :------------------------------------------------------------------------ |
| `/` al inicio | Comando o skill            | Consulte [comandos integrados](#built-in-commands) y [skills](/es/skills) |
| `!` al inicio | Modo Bash                  | Ejecutar comandos directamente y agregar salida de ejecución a la sesión  |
| `@`           | Mención de ruta de archivo | Activar autocompletado de ruta de archivo                                 |

## Comandos integrados

Escriba `/` en Claude Code para ver todos los comandos disponibles, o escriba `/` seguido de cualquier letra para filtrar. No todos los comandos son visibles para todos los usuarios. Algunos dependen de su plataforma, plan o entorno. Por ejemplo, `/desktop` solo aparece en macOS y Windows, `/upgrade` y `/privacy-settings` solo están disponibles en planes Pro y Max, y `/terminal-setup` está oculto cuando su terminal admite nativamente sus atajos de teclado.

Claude Code también incluye [skills agrupados](/es/skills#bundled-skills) como `/simplify`, `/batch` y `/debug` que aparecen junto a comandos integrados cuando escribe `/`. Para crear sus propios comandos, consulte [skills](/es/skills).

En la tabla siguiente, `<arg>` indica un argumento requerido y `[arg]` indica uno opcional.

| Comando                   | Propósito                                                                                                                                                                                                                                                                  |
| :------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/add-dir <path>`         | Agregar un nuevo directorio de trabajo a la sesión actual                                                                                                                                                                                                                  |
| `/agents`                 | Administrar configuraciones de [agent](/es/sub-agents)                                                                                                                                                                                                                     |
| `/btw <question>`         | Hacer una [pregunta lateral](#side-questions-with-%2Fbtw) rápida sin agregar a la conversación                                                                                                                                                                             |
| `/chrome`                 | Configurar ajustes de [Claude en Chrome](/es/chrome)                                                                                                                                                                                                                       |
| `/clear`                  | Limpiar historial de conversación y liberar contexto. Alias: `/reset`, `/new`                                                                                                                                                                                              |
| `/compact [instructions]` | Compactar conversación con instrucciones de enfoque opcionales                                                                                                                                                                                                             |
| `/config`                 | Abrir la interfaz de [Configuración](/es/settings) para ajustar tema, modelo, [estilo de salida](/es/output-styles) y otras preferencias. Alias: `/settings`                                                                                                               |
| `/context`                | Visualizar el uso actual del contexto como una cuadrícula de colores                                                                                                                                                                                                       |
| `/copy`                   | Copiar la última respuesta del asistente al portapapeles. Cuando hay bloques de código presentes, muestra un selector interactivo para seleccionar bloques individuales o la respuesta completa                                                                            |
| `/cost`                   | Mostrar estadísticas de uso de tokens. Consulte [guía de seguimiento de costos](/es/costs#using-the-cost-command) para detalles específicos de suscripción                                                                                                                 |
| `/desktop`                | Continuar la sesión actual en la aplicación de escritorio de Claude Code. Solo macOS y Windows. Alias: `/app`                                                                                                                                                              |
| `/diff`                   | Abrir un visor de diferencias interactivo que muestra cambios sin confirmar y diferencias por turno. Use las flechas izquierda/derecha para cambiar entre el diff de git actual y los turnos individuales de Claude, y arriba/abajo para examinar archivos                 |
| `/doctor`                 | Diagnosticar y verificar su instalación y configuración de Claude Code                                                                                                                                                                                                     |
| `/exit`                   | Salir de la CLI. Alias: `/quit`                                                                                                                                                                                                                                            |
| `/export [filename]`      | Exportar la conversación actual como texto sin formato. Con un nombre de archivo, escribe directamente en ese archivo. Sin uno, abre un diálogo para copiar al portapapeles o guardar en un archivo                                                                        |
| `/extra-usage`            | Configurar uso extra para continuar trabajando cuando se alcanzan los límites de velocidad                                                                                                                                                                                 |
| `/fast [on\|off]`         | Alternar [modo rápido](/es/fast-mode) activado o desactivado                                                                                                                                                                                                               |
| `/feedback [report]`      | Enviar comentarios sobre Claude Code. Alias: `/bug`                                                                                                                                                                                                                        |
| `/fork [name]`            | Crear una bifurcación de la conversación actual en este punto                                                                                                                                                                                                              |
| `/help`                   | Mostrar ayuda y comandos disponibles                                                                                                                                                                                                                                       |
| `/hooks`                  | Administrar configuraciones de [hook](/es/hooks) para eventos de herramientas                                                                                                                                                                                              |
| `/ide`                    | Administrar integraciones de IDE y mostrar estado                                                                                                                                                                                                                          |
| `/init`                   | Inicializar proyecto con guía `CLAUDE.md`                                                                                                                                                                                                                                  |
| `/insights`               | Generar un informe que analice sus sesiones de Claude Code, incluidas áreas de proyecto, patrones de interacción y puntos de fricción                                                                                                                                      |
| `/install-github-app`     | Configurar la aplicación [Claude GitHub Actions](/es/github-actions) para un repositorio. Lo guía a través de la selección de un repositorio y la configuración de la integración                                                                                          |
| `/install-slack-app`      | Instalar la aplicación Claude Slack. Abre un navegador para completar el flujo OAuth                                                                                                                                                                                       |
| `/keybindings`            | Abrir o crear su archivo de configuración de atajos de teclado                                                                                                                                                                                                             |
| `/login`                  | Iniciar sesión en su cuenta de Anthropic                                                                                                                                                                                                                                   |
| `/logout`                 | Cerrar sesión de su cuenta de Anthropic                                                                                                                                                                                                                                    |
| `/mcp`                    | Administrar conexiones de servidor MCP y autenticación OAuth                                                                                                                                                                                                               |
| `/memory`                 | Editar archivos de memoria `CLAUDE.md`, habilitar o deshabilitar [auto-memory](/es/memory#auto-memory) y ver entradas de auto-memory                                                                                                                                       |
| `/mobile`                 | Mostrar código QR para descargar la aplicación móvil de Claude. Alias: `/ios`, `/android`                                                                                                                                                                                  |
| `/model [model]`          | Seleccionar o cambiar el modelo de IA. Para modelos que lo admiten, use las flechas izquierda/derecha para [ajustar el nivel de esfuerzo](/es/model-config#adjust-effort-level). El cambio entra en vigor inmediatamente sin esperar a que se complete la respuesta actual |
| `/passes`                 | Compartir una semana gratuita de Claude Code con amigos. Solo visible si su cuenta es elegible                                                                                                                                                                             |
| `/permissions`            | Ver o actualizar [permisos](/es/permissions#manage-permissions). Alias: `/allowed-tools`                                                                                                                                                                                   |
| `/plan`                   | Entrar en Plan Mode directamente desde el prompt                                                                                                                                                                                                                           |
| `/plugin`                 | Administrar [plugins](/es/plugins) de Claude Code                                                                                                                                                                                                                          |
| `/pr-comments [PR]`       | Obtener y mostrar comentarios de una solicitud de extracción de GitHub. Detecta automáticamente el PR para la rama actual, o pase una URL o número de PR. Requiere la CLI `gh`                                                                                             |
| `/privacy-settings`       | Ver y actualizar su configuración de privacidad. Solo disponible para suscriptores del plan Pro y Max                                                                                                                                                                      |
| `/release-notes`          | Ver el registro de cambios completo, con la versión más reciente más cercana a su prompt                                                                                                                                                                                   |
| `/reload-plugins`         | Recargar todos los [plugins](/es/plugins) activos para aplicar cambios pendientes sin reiniciar. Informa qué se cargó y anota los cambios que requieren un reinicio                                                                                                        |
| `/remote-control`         | Hacer que esta sesión esté disponible para [control remoto](/es/remote-control) desde claude.ai. Alias: `/rc`                                                                                                                                                              |
| `/remote-env`             | Configurar el entorno remoto predeterminado para [sesiones de teleport](/es/claude-code-on-the-web#teleport-a-web-session-to-your-terminal)                                                                                                                                |
| `/rename [name]`          | Renombrar la sesión actual. Sin un nombre, genera automáticamente uno a partir del historial de conversación                                                                                                                                                               |
| `/resume [session]`       | Reanudar una conversación por ID o nombre, o abrir el selector de sesión. Alias: `/continue`                                                                                                                                                                               |
| `/review`                 | Obsoleto. Instale el [plugin `code-review`](https://github.com/anthropics/claude-code-marketplace/blob/main/code-review/README.md) en su lugar: `claude plugin install code-review@claude-code-marketplace`                                                                |
| `/rewind`                 | Rebobinar la conversación y/o código a un punto anterior, o resumir desde un mensaje seleccionado. Consulte [checkpointing](/es/checkpointing). Alias: `/checkpoint`                                                                                                       |
| `/sandbox`                | Alternar [modo sandbox](/es/sandboxing). Disponible solo en plataformas compatibles                                                                                                                                                                                        |
| `/security-review`        | Analizar cambios pendientes en la rama actual para detectar vulnerabilidades de seguridad. Revisa el diff de git e identifica riesgos como inyección, problemas de autenticación y exposición de datos                                                                     |
| `/skills`                 | Listar [skills](/es/skills) disponibles                                                                                                                                                                                                                                    |
| `/stats`                  | Visualizar uso diario, historial de sesiones, rachas y preferencias de modelo                                                                                                                                                                                              |
| `/status`                 | Abrir la interfaz de Configuración (pestaña Estado) mostrando versión, modelo, cuenta y conectividad                                                                                                                                                                       |
| `/statusline`             | Configurar la [línea de estado](/es/statusline) de Claude Code. Describa lo que desea, o ejecute sin argumentos para auto-configurar desde su prompt de shell                                                                                                              |
| `/stickers`               | Pedir pegatinas de Claude Code                                                                                                                                                                                                                                             |
| `/tasks`                  | Listar y administrar tareas en segundo plano                                                                                                                                                                                                                               |
| `/terminal-setup`         | Configurar atajos de teclado de terminal para Shift+Enter y otros atajos. Solo visible en terminales que lo necesitan, como VS Code, Alacritty o Warp                                                                                                                      |
| `/theme`                  | Cambiar el tema de color. Incluye variantes claras y oscuras, temas accesibles para daltónicos (daltonizados) y temas ANSI que usan la paleta de colores de su terminal                                                                                                    |
| `/upgrade`                | Abrir la página de actualización para cambiar a un nivel de plan superior                                                                                                                                                                                                  |
| `/usage`                  | Mostrar límites de uso del plan y estado del límite de velocidad                                                                                                                                                                                                           |
| `/vim`                    | Alternar entre modos de edición Vim y Normal                                                                                                                                                                                                                               |

### Prompts de MCP

Los servidores MCP pueden exponer prompts que aparecen como comandos. Estos usan el formato `/mcp__<server>__<prompt>` y se descubren dinámicamente desde servidores conectados. Consulte [prompts de MCP](/es/mcp#use-mcp-prompts-as-commands) para obtener detalles.

## Modo editor Vim

Habilitar edición de estilo vim con el comando `/vim` o configurar permanentemente a través de `/config`.

### Cambio de modo

| Comando | Acción                            | Desde modo |
| :------ | :-------------------------------- | :--------- |
| `Esc`   | Entrar en modo NORMAL             | INSERT     |
| `i`     | Insertar antes del cursor         | NORMAL     |
| `I`     | Insertar al principio de la línea | NORMAL     |
| `a`     | Insertar después del cursor       | NORMAL     |
| `A`     | Insertar al final de la línea     | NORMAL     |
| `o`     | Abrir línea debajo                | NORMAL     |
| `O`     | Abrir línea arriba                | NORMAL     |

### Navegación (modo NORMAL)

| Comando         | Acción                                                      |
| :-------------- | :---------------------------------------------------------- |
| `h`/`j`/`k`/`l` | Mover izquierda/abajo/arriba/derecha                        |
| `w`             | Siguiente palabra                                           |
| `e`             | Final de palabra                                            |
| `b`             | Palabra anterior                                            |
| `0`             | Principio de línea                                          |
| `$`             | Final de línea                                              |
| `^`             | Primer carácter no en blanco                                |
| `gg`            | Principio de entrada                                        |
| `G`             | Final de entrada                                            |
| `f{char}`       | Saltar a la siguiente ocurrencia del carácter               |
| `F{char}`       | Saltar a la ocurrencia anterior del carácter                |
| `t{char}`       | Saltar justo antes de la siguiente ocurrencia del carácter  |
| `T{char}`       | Saltar justo después de la ocurrencia anterior del carácter |
| `;`             | Repetir último movimiento f/F/t/T                           |
| `,`             | Repetir último movimiento f/F/t/T en orden inverso          |

<Note>
  En modo normal de vim, si el cursor está al principio o al final de la entrada y no puede moverse más, las flechas de dirección navegan por el historial de comandos en su lugar.
</Note>

### Edición (modo NORMAL)

| Comando        | Acción                                      |
| :------------- | :------------------------------------------ |
| `x`            | Eliminar carácter                           |
| `dd`           | Eliminar línea                              |
| `D`            | Eliminar hasta el final de la línea         |
| `dw`/`de`/`db` | Eliminar palabra/hasta el final/hacia atrás |
| `cc`           | Cambiar línea                               |
| `C`            | Cambiar hasta el final de la línea          |
| `cw`/`ce`/`cb` | Cambiar palabra/hasta el final/hacia atrás  |
| `yy`/`Y`       | Yanquear (copiar) línea                     |
| `yw`/`ye`/`yb` | Yanquear palabra/hasta el final/hacia atrás |
| `p`            | Pegar después del cursor                    |
| `P`            | Pegar antes del cursor                      |
| `>>`           | Indentar línea                              |
| `<<`           | Desindentación de línea                     |
| `J`            | Unir líneas                                 |
| `.`            | Repetir último cambio                       |

### Objetos de texto (modo NORMAL)

Los objetos de texto funcionan con operadores como `d`, `c` e `y`:

| Comando   | Acción                                                         |
| :-------- | :------------------------------------------------------------- |
| `iw`/`aw` | Palabra interior/alrededor                                     |
| `iW`/`aW` | PALABRA interior/alrededor (delimitada por espacios en blanco) |
| `i"`/`a"` | Comillas dobles interior/alrededor                             |
| `i'`/`a'` | Comillas simples interior/alrededor                            |
| `i(`/`a(` | Paréntesis interior/alrededor                                  |
| `i[`/`a[` | Corchetes interior/alrededor                                   |
| `i{`/`a{` | Llaves interior/alrededor                                      |

## Historial de comandos

Claude Code mantiene el historial de comandos para la sesión actual:

* El historial de entrada se almacena por directorio de trabajo
* El historial de entrada se reinicia cuando ejecuta `/clear` para iniciar una nueva sesión. La conversación de la sesión anterior se conserva y se puede reanudar.
* Use las flechas arriba/abajo para navegar (consulte los atajos de teclado anteriores)
* **Nota**: la expansión del historial (`!`) está deshabilitada de forma predeterminada

### Búsqueda inversa con Ctrl+R

Presione `Ctrl+R` para buscar de forma interactiva a través de su historial de comandos:

1. **Iniciar búsqueda**: presione `Ctrl+R` para activar la búsqueda inversa del historial
2. **Escribir consulta**: ingrese texto para buscar en comandos anteriores. El término de búsqueda se resalta en los resultados coincidentes
3. **Navegar coincidencias**: presione `Ctrl+R` nuevamente para ciclar a través de coincidencias más antiguas
4. **Aceptar coincidencia**:
   * Presione `Tab` o `Esc` para aceptar la coincidencia actual y continuar editando
   * Presione `Enter` para aceptar y ejecutar el comando inmediatamente
5. **Cancelar búsqueda**:
   * Presione `Ctrl+C` para cancelar y restaurar su entrada original
   * Presione `Backspace` en búsqueda vacía para cancelar

La búsqueda muestra comandos coincidentes con el término de búsqueda resaltado, para que pueda encontrar y reutilizar entradas anteriores.

## Comandos bash en segundo plano

Claude Code admite la ejecución de comandos bash en segundo plano, lo que le permite continuar trabajando mientras se ejecutan procesos de larga duración.

### Cómo funciona el segundo plano

Cuando Claude Code ejecuta un comando en segundo plano, ejecuta el comando de forma asincrónica e inmediatamente devuelve un ID de tarea en segundo plano. Claude Code puede responder a nuevos prompts mientras el comando continúa ejecutándose en segundo plano.

Para ejecutar comandos en segundo plano, puede:

* Solicitar a Claude Code que ejecute un comando en segundo plano
* Presionar Ctrl+B para mover una invocación de herramienta Bash regular al segundo plano. (Los usuarios de Tmux deben presionar Ctrl+B dos veces debido a la tecla de prefijo de tmux).

**Características clave:**

* La salida se almacena en búfer y Claude puede recuperarla usando la herramienta TaskOutput
* Las tareas en segundo plano tienen ID únicos para seguimiento y recuperación de salida
* Las tareas en segundo plano se limpian automáticamente cuando Claude Code sale

Para deshabilitar toda la funcionalidad de tareas en segundo plano, establezca la variable de entorno `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` en `1`. Consulte [Variables de entorno](/es/settings#environment-variables) para obtener detalles.

**Comandos comúnmente puestos en segundo plano:**

* Herramientas de compilación (webpack, vite, make)
* Administradores de paquetes (npm, yarn, pnpm)
* Ejecutores de pruebas (jest, pytest)
* Servidores de desarrollo
* Procesos de larga duración (docker, terraform)

### Modo Bash con prefijo `!`

Ejecutar comandos bash directamente sin pasar por Claude prefijando su entrada con `!`:

```bash  theme={null}
! npm test
! git status
! ls -la
```

Modo Bash:

* Agrega el comando y su salida al contexto de conversación
* Muestra progreso y salida en tiempo real
* Admite el mismo segundo plano `Ctrl+B` para comandos de larga duración
* No requiere que Claude interprete o apruebe el comando
* Admite autocompletado basado en historial: escriba un comando parcial y presione **Tab** para completar desde comandos `!` anteriores en el proyecto actual
* Salir con `Escape`, `Backspace` o `Ctrl+U` en un prompt vacío

Esto es útil para operaciones rápidas de shell mientras se mantiene el contexto de conversación.

## Sugerencias de prompt

Cuando abre una sesión por primera vez, aparece un comando de ejemplo atenuado en la entrada del prompt para ayudarle a comenzar. Claude Code elige esto del historial de git de su proyecto, por lo que refleja archivos en los que ha estado trabajando recientemente.

Después de que Claude responde, las sugerencias continúan apareciendo según su historial de conversación, como un paso de seguimiento de una solicitud de varias partes o una continuación natural de su flujo de trabajo.

* Presione **Tab** para aceptar la sugerencia, o presione **Enter** para aceptar y enviar
* Comience a escribir para descartarla

La sugerencia se ejecuta como una solicitud en segundo plano que reutiliza el caché de prompt de la conversación principal, por lo que el costo adicional es mínimo. Claude Code omite la generación de sugerencias cuando el caché está frío para evitar costos innecesarios.

Las sugerencias se omiten automáticamente después del primer turno de una conversación, en modo no interactivo y en Plan Mode.

Para deshabilitar completamente las sugerencias de prompt, establezca la variable de entorno o alterne la configuración en `/config`:

```bash  theme={null}
export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false
```

## Preguntas laterales con /btw

Use `/btw` para hacer una pregunta rápida sobre su trabajo actual sin agregar al historial de conversación. Esto es útil cuando desea una respuesta rápida pero no desea saturar el contexto principal o desviar a Claude de una tarea de larga duración.

```
/btw what was the name of that config file again?
```

Las preguntas laterales tienen visibilidad completa de la conversación actual, por lo que puede preguntar sobre código que Claude ya ha leído, decisiones que tomó anteriormente, o cualquier otra cosa de la sesión. La pregunta y la respuesta son efímeras: aparecen en una superposición descartable y nunca entran en el historial de conversación.

* **Disponible mientras Claude está trabajando**: puede ejecutar `/btw` incluso mientras Claude está procesando una respuesta. La pregunta lateral se ejecuta de forma independiente y no interrumpe el turno principal.
* **Sin acceso a herramientas**: las preguntas laterales responden solo a partir de lo que ya está en contexto. Claude no puede leer archivos, ejecutar comandos o buscar al responder una pregunta lateral.
* **Respuesta única**: no hay turnos de seguimiento. Si necesita una conversación de ida y vuelta, use un prompt normal en su lugar.
* **Bajo costo**: la pregunta lateral reutiliza el caché de prompt de la conversación principal, por lo que el costo adicional es mínimo.

Presione **Espacio**, **Enter** o **Escape** para descartar la respuesta y volver al prompt.

`/btw` es lo opuesto a un [subagent](/es/sub-agents): ve su conversación completa pero no tiene herramientas, mientras que un subagent tiene herramientas completas pero comienza con un contexto vacío. Use `/btw` para preguntar sobre lo que Claude ya sabe de esta sesión; use un subagent para descubrir algo nuevo.

## Lista de tareas

Cuando trabaja en trabajo complejo y de varios pasos, Claude crea una lista de tareas para rastrear el progreso. Las tareas aparecen en el área de estado de su terminal con indicadores que muestran qué está pendiente, en progreso o completado.

* Presione `Ctrl+T` para alternar la vista de la lista de tareas. La pantalla muestra hasta 10 tareas a la vez
* Para ver todas las tareas o borrarlas, pregunte a Claude directamente: "show me all tasks" o "clear all tasks"
* Las tareas persisten en compactaciones de contexto, ayudando a Claude a mantenerse organizado en proyectos más grandes
* Para compartir una lista de tareas entre sesiones, establezca `CLAUDE_CODE_TASK_LIST_ID` para usar un directorio nombrado en `~/.claude/tasks/`: `CLAUDE_CODE_TASK_LIST_ID=my-project claude`
* Para revertir a la lista TODO anterior, establezca `CLAUDE_CODE_ENABLE_TASKS=false`.

## Estado de revisión de PR

Cuando trabaja en una rama con una solicitud de extracción abierta, Claude Code muestra un enlace de PR en el pie de página (por ejemplo, "PR #446"). El enlace tiene un subrayado de color que indica el estado de revisión:

* Verde: aprobado
* Amarillo: revisión pendiente
* Rojo: cambios solicitados
* Gris: borrador
* Púrpura: fusionado

`Cmd+clic` (Mac) o `Ctrl+clic` (Windows/Linux) en el enlace para abrir la solicitud de extracción en su navegador. El estado se actualiza automáticamente cada 60 segundos.

<Note>
  El estado de PR requiere que la CLI `gh` esté instalada y autenticada (`gh auth login`).
</Note>

## Ver también

* [Skills](/es/skills) - Prompts personalizados y flujos de trabajo
* [Checkpointing](/es/checkpointing) - Rebobinar ediciones de Claude y restaurar estados anteriores
* [Referencia de CLI](/es/cli-reference) - Banderas y opciones de línea de comandos
* [Configuración](/es/settings) - Opciones de configuración
* [Gestión de memoria](/es/memory) - Administración de archivos CLAUDE.md
