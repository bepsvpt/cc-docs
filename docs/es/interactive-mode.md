> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Modo interactivo

> Referencia completa de atajos de teclado, modos de entrada y características interactivas en sesiones de Claude Code.

## Atajos de teclado

<Note>
  Los atajos de teclado pueden variar según la plataforma y la terminal. Presione `?` para ver los atajos disponibles en su entorno.

  **Usuarios de macOS**: Los atajos de la tecla Option/Alt (`Alt+B`, `Alt+F`, `Alt+Y`, `Alt+M`, `Alt+P`) requieren configurar Option como Meta en su terminal:

  * **iTerm2**: Configuración → Perfiles → Teclas → General → establecer la tecla Option izquierda/derecha en "Esc+"
  * **Terminal de Apple**: Configuración → Perfiles → Teclado → marcar "Usar Option como tecla Meta"
  * **VS Code**: establecer `"terminal.integrated.macOptionIsMeta": true` en la configuración de VS Code

  Consulte [Configuración de terminal](/es/terminal-config) para obtener más detalles.
</Note>

### Controles generales

| Atajo                                           | Descripción                                                                          | Contexto                                                                                                                                                                                                                                                                                                                                                      |
| :---------------------------------------------- | :----------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Ctrl+C`                                        | Cancelar entrada o generación actual                                                 | Interrupción estándar                                                                                                                                                                                                                                                                                                                                         |
| `Ctrl+X Ctrl+K`                                 | Terminar todos los agentes de fondo. Presione dos veces en 3 segundos para confirmar | Control de agentes de fondo                                                                                                                                                                                                                                                                                                                                   |
| `Ctrl+D`                                        | Salir de la sesión de Claude Code                                                    | Señal EOF                                                                                                                                                                                                                                                                                                                                                     |
| `Ctrl+G` o `Ctrl+X Ctrl+E`                      | Abrir en el editor de texto predeterminado                                           | Edite su indicación o respuesta personalizada en su editor de texto predeterminado. `Ctrl+X Ctrl+E` es el enlace nativo de readline. Active Mostrar última respuesta en editor externo en `/config` para anteponer la respuesta anterior de Claude como contexto comentado con `#` encima de su indicación; el bloque de comentarios se elimina cuando guarda |
| `Ctrl+L`                                        | Redibujar pantalla                                                                   | Fuerza un redibujado completo de la terminal. La entrada y el historial de conversación se mantienen. Use esto para recuperarse si la pantalla se vuelve distorsionada o parcialmente en blanco                                                                                                                                                               |
| `Ctrl+O`                                        | Alternar visor de transcripción                                                      | Muestra el uso y la ejecución detallada de herramientas. También expande las llamadas de MCP, que se contraen a una sola línea como "Llamó a slack 3 veces" de forma predeterminada                                                                                                                                                                           |
| `Ctrl+R`                                        | Búsqueda inversa del historial de comandos                                           | Buscar a través de comandos anteriores de forma interactiva                                                                                                                                                                                                                                                                                                   |
| `Ctrl+V` o `Cmd+V` (iTerm2) o `Alt+V` (Windows) | Pegar imagen desde el portapapeles                                                   | Inserta un chip `[Image #N]` en el cursor para que pueda hacer referencia a él posicionalmente en su indicación                                                                                                                                                                                                                                               |
| `Ctrl+B`                                        | Tareas en ejecución de fondo                                                         | Coloca comandos bash y agentes en segundo plano. Los usuarios de Tmux presionan dos veces                                                                                                                                                                                                                                                                     |
| `Ctrl+T`                                        | Alternar lista de tareas                                                             | Mostrar u ocultar la [lista de tareas](#task-list) en el área de estado de la terminal                                                                                                                                                                                                                                                                        |
| `Flechas izquierda/derecha`                     | Ciclar a través de pestañas de diálogo                                               | Navegar entre pestañas en diálogos de permisos y menús                                                                                                                                                                                                                                                                                                        |
| `Flechas arriba/abajo` o `Ctrl+P`/`Ctrl+N`      | Mover cursor o navegar por el historial de comandos                                  | En entrada multilínea, primero mueve el cursor dentro de la indicación. Una vez que el cursor ya está en el borde superior o inferior, presionar nuevamente navega por el historial de comandos                                                                                                                                                               |
| `Esc` + `Esc`                                   | Rebobinar o resumir                                                                  | Restaurar código y/o conversación a un punto anterior, o resumir desde un mensaje seleccionado                                                                                                                                                                                                                                                                |
| `Shift+Tab` o `Alt+M` (algunas configuraciones) | Ciclar modos de permiso                                                              | Ciclar a través de `default`, `acceptEdits`, `plan` y cualquier modo que haya habilitado, como `auto` o `bypassPermissions`. Consulte [modos de permiso](/es/permission-modes).                                                                                                                                                                               |
| `Option+P` (macOS) o `Alt+P` (Windows/Linux)    | Cambiar modelo                                                                       | Cambiar modelos sin borrar su indicación                                                                                                                                                                                                                                                                                                                      |
| `Option+T` (macOS) o `Alt+T` (Windows/Linux)    | Alternar pensamiento extendido                                                       | Habilitar o deshabilitar el modo de pensamiento extendido. {/* min-version: 2.1.132 */}A partir de v2.1.132, este atajo funciona en macOS sin configurar Option como Meta                                                                                                                                                                                     |
| `Option+O` (macOS) o `Alt+O` (Windows/Linux)    | Alternar modo rápido                                                                 | Habilitar o deshabilitar [modo rápido](/es/fast-mode)                                                                                                                                                                                                                                                                                                         |

### Edición de texto

| Atajo                         | Descripción                                          | Contexto                                                                                                                                                                                                           |
| :---------------------------- | :--------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+A`                      | Mover cursor al inicio de la línea actual            | En entrada multilínea, mueve al inicio de la línea lógica actual                                                                                                                                                   |
| `Ctrl+E`                      | Mover cursor al final de la línea actual             | En entrada multilínea, mueve al final de la línea lógica actual                                                                                                                                                    |
| `Ctrl+K`                      | Eliminar hasta el final de la línea                  | Almacena el texto eliminado para pegarlo                                                                                                                                                                           |
| `Ctrl+U`                      | Eliminar desde el cursor hasta el inicio de la línea | Almacena el texto eliminado para pegarlo. Repita para borrar en múltiples líneas en entrada multilínea. En macOS, los emuladores de terminal incluyendo iTerm2 y Terminal.app asignan `Cmd+Backspace` a este atajo |
| `Ctrl+W`                      | Eliminar palabra anterior                            | Almacena el texto eliminado para pegarlo. En Windows, `Ctrl+Backspace` también elimina la palabra anterior                                                                                                         |
| `Ctrl+Y`                      | Pegar texto eliminado                                | Pegar texto eliminado con `Ctrl+K`, `Ctrl+U` o `Ctrl+W`                                                                                                                                                            |
| `Alt+Y` (después de `Ctrl+Y`) | Ciclar historial de pegado                           | Después de pegar, ciclar a través del texto eliminado anteriormente. Requiere [Option como Meta](#keyboard-shortcuts) en macOS                                                                                     |
| `Alt+B`                       | Mover cursor una palabra hacia atrás                 | Navegación de palabras. Requiere [Option como Meta](#keyboard-shortcuts) en macOS                                                                                                                                  |
| `Alt+F`                       | Mover cursor una palabra hacia adelante              | Navegación de palabras. Requiere [Option como Meta](#keyboard-shortcuts) en macOS                                                                                                                                  |

### Tema y visualización

| Atajo    | Descripción                                           | Contexto                                                                                                                       |
| :------- | :---------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+T` | Alternar resaltado de sintaxis para bloques de código | Solo funciona dentro del menú del selector `/theme`. Controla si el código en las respuestas de Claude usa colores de sintaxis |

### Entrada multilínea

| Método               | Atajo              | Contexto                                                                                                   |
| :------------------- | :----------------- | :--------------------------------------------------------------------------------------------------------- |
| Escape rápido        | `\` + `Enter`      | Funciona en todas las terminales                                                                           |
| Tecla Option         | `Option+Enter`     | Después de habilitar [Option como Meta](/es/terminal-config#enable-option-key-shortcuts-on-macos) en macOS |
| Shift+Enter          | `Shift+Enter`      | Nativo en iTerm2, WezTerm, Ghostty, Kitty, Warp, Terminal de Apple, Windows Terminal                       |
| Secuencia de control | `Ctrl+J`           | Funciona en cualquier terminal sin configuración                                                           |
| Modo de pegado       | Pegar directamente | Para bloques de código, registros                                                                          |

<Tip>
  Shift+Enter funciona sin configuración en iTerm2, WezTerm, Ghostty, Kitty, Warp, Terminal de Apple y Windows Terminal. Para VS Code, Cursor, Windsurf, Alacritty y Zed, ejecute `/terminal-setup` para instalar el enlace.
</Tip>

### Comandos rápidos

| Atajo         | Descripción                | Notas                                                                       |
| :------------ | :------------------------- | :-------------------------------------------------------------------------- |
| `/` al inicio | Comando o skill            | Consulte [comandos](#commands) y [skills](/es/skills)                       |
| `!` al inicio | Modo Bash                  | Ejecutar comandos directamente y agregar la salida de ejecución a la sesión |
| `@`           | Mención de ruta de archivo | Activar autocompletado de ruta de archivo                                   |

### Visor de transcripción

Cuando el visor de transcripción está abierto (alternado con `Ctrl+O`), estos atajos están disponibles. `Ctrl+E` se puede reasignar a través de [`transcript:toggleShowAll`](/es/keybindings).

| Atajo                | Descripción                                                                                                                                                                                                                                                     |
| :------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+E`             | Alternar mostrar todo el contenido                                                                                                                                                                                                                              |
| `[`                  | Escribir la conversación completa en el scrollback nativo de su terminal para que `Cmd+F`, el modo de copia de tmux y otras herramientas nativas puedan buscarla. Requiere [renderizado a pantalla completa](/es/fullscreen#search-and-review-the-conversation) |
| `v`                  | Escribir la conversación en un archivo temporal y abrirlo en `$VISUAL` o `$EDITOR`. Requiere [renderizado a pantalla completa](/es/fullscreen)                                                                                                                  |
| `q`, `Ctrl+C`, `Esc` | Salir de la vista de transcripción. Los tres se pueden reasignar a través de [`transcript:exit`](/es/keybindings)                                                                                                                                               |

### Entrada de voz

| Atajo                                  | Descripción    | Notas                                                                                                                                                                                                             |
| :------------------------------------- | :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Mantener presionado o pulsar `Espacio` | Dictado de voz | Requiere que [dictado de voz](/es/voice-dictation) esté habilitado. Mantenga presionado para grabar, o ejecute `/voice tap` para alternar con pulsar. [Reasignable](/es/voice-dictation#rebind-the-dictation-key) |

## Comandos

Escriba `/` en Claude Code para ver todos los comandos disponibles, o escriba `/` seguido de cualquier letra para filtrar. El menú `/` muestra todo lo que puede invocar: comandos integrados, [skills](/es/skills) incluidos y creados por el usuario, y comandos contribuidos por [plugins](/es/plugins) y [servidores MCP](/es/mcp#use-mcp-prompts-as-commands). No todos los comandos integrados son visibles para todos los usuarios ya que algunos dependen de su plataforma o plan.

Consulte la [referencia de comandos](/es/commands) para obtener la lista completa de comandos incluidos en Claude Code.

## Modo editor Vim

Habilite la edición de estilo vim a través de `/config` → Editor mode.

### Cambio de modo

| Comando | Acción                                         | Desde el modo  |
| :------ | :--------------------------------------------- | :------------- |
| `Esc`   | Entrar en modo NORMAL                          | INSERT, VISUAL |
| `i`     | Insertar antes del cursor                      | NORMAL         |
| `I`     | Insertar al principio de la línea              | NORMAL         |
| `a`     | Insertar después del cursor                    | NORMAL         |
| `A`     | Insertar al final de la línea                  | NORMAL         |
| `o`     | Abrir línea debajo                             | NORMAL         |
| `O`     | Abrir línea arriba                             | NORMAL         |
| `v`     | Iniciar selección visual carácter por carácter | NORMAL         |
| `V`     | Iniciar selección visual línea por línea       | NORMAL         |

### Navegación (modo NORMAL)

| Comando         | Acción                                                      |
| :-------------- | :---------------------------------------------------------- |
| `h`/`j`/`k`/`l` | Mover izquierda/abajo/arriba/derecha                        |
| `Space`         | Mover a la derecha                                          |
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
  En modo normal de vim, si el cursor está al principio o al final de la entrada y no puede moverse más, `j`/`k` y las teclas de flecha navegan por el historial de comandos en su lugar.
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
| `u`            | Deshacer                                    |
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

### Modo visual

Presione `v` para selección carácter por carácter o `V` para selección línea por línea. Los movimientos extienden la selección, y los operadores actúan sobre ella directamente.

| Comando          | Acción                                                          |
| :--------------- | :-------------------------------------------------------------- |
| `d`/`x`          | Eliminar selección                                              |
| `y`              | Yanquear selección                                              |
| `c`/`s`          | Cambiar selección                                               |
| `p`              | Reemplazar selección con contenido del registro                 |
| `r{char}`        | Reemplazar cada carácter seleccionado con `{char}`              |
| `~`/`u`/`U`      | Alternar, minúsculas o mayúsculas de selección                  |
| `>`/`<`          | Indentar o desindentación de líneas seleccionadas               |
| `J`              | Unir líneas seleccionadas                                       |
| `o`              | Intercambiar cursor y ancla                                     |
| `iw`/`aw`/`i"`/… | Seleccionar un objeto de texto                                  |
| `v`/`V`          | Alternar entre carácter por carácter y línea por línea, o salir |

El modo visual por bloques con `Ctrl+V` no es compatible.

## Historial de comandos

Claude Code mantiene el historial de comandos para la sesión actual:

* El historial de entrada se almacena por directorio de trabajo
* El historial de entrada se reinicia cuando ejecuta `/clear` para iniciar una nueva sesión. La conversación de la sesión anterior se conserva y se puede reanudar.
* Use las flechas arriba/abajo para navegar (consulte los atajos de teclado anteriores)
* **Nota**: la expansión del historial (`!`) está deshabilitada de forma predeterminada

### Búsqueda inversa con Ctrl+R

Presione `Ctrl+R` para buscar de forma interactiva a través de su historial de comandos:

1. **Iniciar búsqueda**: presione `Ctrl+R` para activar la búsqueda de historial inverso
2. **Escribir consulta**: ingrese texto para buscar en comandos anteriores. El término de búsqueda se resalta en los resultados coincidentes
3. **Navegar coincidencias**: presione `Ctrl+R` nuevamente para ciclar a través de coincidencias más antiguas
4. **Cambiar alcance**: la búsqueda se establece de forma predeterminada en indicaciones de todos los proyectos. Presione `Ctrl+S` para ciclar el alcance entre esta sesión, este proyecto y todos los proyectos
5. **Aceptar coincidencia**:
   * Presione `Tab` o `Esc` para aceptar la coincidencia actual y continuar editando
   * Presione `Enter` para aceptar y ejecutar el comando inmediatamente
6. **Cancelar búsqueda**:
   * Presione `Ctrl+C` para cancelar y restaurar su entrada original
   * Presione `Backspace` en búsqueda vacía para cancelar

La búsqueda muestra comandos coincidentes con el término de búsqueda resaltado, para que pueda encontrar y reutilizar entradas anteriores.

## Comandos bash en segundo plano

Claude Code admite la ejecución de comandos bash en segundo plano, lo que le permite continuar trabajando mientras se ejecutan procesos de larga duración.

### Cómo funciona el envío a segundo plano

Cuando Claude Code ejecuta un comando en segundo plano, ejecuta el comando de forma asincrónica e inmediatamente devuelve un ID de tarea de fondo. Claude Code puede responder a nuevas indicaciones mientras el comando continúa ejecutándose en segundo plano.

Para ejecutar comandos en segundo plano, puede:

* Indicar a Claude Code que ejecute un comando en segundo plano
* Presione Ctrl+B para mover una invocación regular de herramienta Bash al segundo plano. (Los usuarios de Tmux deben presionar Ctrl+B dos veces debido a la tecla de prefijo de tmux).

**Características clave:**

* La salida se escribe en un archivo y Claude puede recuperarla usando la herramienta Read
* Las tareas de fondo tienen ID únicos para el seguimiento y la recuperación de salida
* Las tareas de fondo se limpian automáticamente cuando Claude Code sale
* Las tareas de fondo se terminan automáticamente si la salida excede 5GB, con una nota en stderr explicando por qué

Para deshabilitar toda la funcionalidad de tareas de fondo, establezca la variable de entorno `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` en `1`. Consulte [Variables de entorno](/es/env-vars) para obtener más detalles.

**Comandos comúnmente enviados a segundo plano:**

* Herramientas de compilación (webpack, vite, make)
* Gestores de paquetes (npm, yarn, pnpm)
* Ejecutores de pruebas (jest, pytest)
* Servidores de desarrollo
* Procesos de larga duración (docker, terraform)

### Modo shell con prefijo `!`

Ejecute comandos shell directamente sin pasar por Claude prefijando su entrada con `!`:

```bash theme={null}
! npm test
! git status
! ls -la
```

Modo shell:

* Agrega el comando y su salida al contexto de la conversación
* Muestra el progreso y la salida en tiempo real
* Admite el mismo envío a segundo plano `Ctrl+B` para comandos de larga duración
* No requiere que Claude interprete o apruebe el comando
* Admite autocompletado basado en historial: escriba un comando parcial y presione **Tab** para completar desde comandos `!` anteriores en el proyecto actual
* Salir con `Escape`, `Backspace` o `Ctrl+U` en un indicador vacío
* Pegar texto que comienza con `!` en un indicador vacío entra automáticamente en modo shell, coincidiendo con el comportamiento de `!` escrito

Esto es útil para operaciones rápidas de shell mientras se mantiene el contexto de la conversación.

## Sugerencias de indicación

Cuando abre una sesión por primera vez, aparece un comando de ejemplo atenuado en la entrada de indicación para ayudarle a comenzar. Claude Code elige esto del historial de git de su proyecto, por lo que refleja archivos en los que ha estado trabajando recientemente.

Después de que Claude responde, las sugerencias continúan apareciendo según su historial de conversación, como un paso de seguimiento de una solicitud de varias partes o una continuación natural de su flujo de trabajo.

* Presione **Tab** o **Flecha derecha** para colocar la sugerencia en la entrada de indicación, luego **Intro** para enviar
* Comience a escribir para descartarla

La sugerencia se ejecuta como una solicitud de fondo que reutiliza el caché de indicación de la conversación principal, por lo que el costo adicional es mínimo. Claude Code omite la generación de sugerencias cuando el caché está frío para evitar costos innecesarios.

Las sugerencias se omiten automáticamente después del primer turno de una conversación, en modo no interactivo y en modo plan.

Para deshabilitar completamente las sugerencias de indicación, establezca la variable de entorno o alterne la configuración en `/config`:

```bash theme={null}
export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false
```

## Preguntas laterales con /btw

Use `/btw` para hacer una pregunta rápida sobre su trabajo actual sin agregar al historial de conversación. Esto es útil cuando desea una respuesta rápida pero no desea saturar el contexto principal o desviar a Claude de una tarea de larga duración.

```
/btw what was the name of that config file again?
```

Las preguntas laterales tienen visibilidad completa de la conversación actual, por lo que puede preguntar sobre código que Claude ya ha leído, decisiones que tomó anteriormente, o cualquier otra cosa de la sesión. La pregunta y la respuesta son efímeras: aparecen en una superposición descartable y nunca entran en el historial de conversación.

* **Disponible mientras Claude está trabajando**: puede ejecutar `/btw` incluso mientras Claude está procesando una respuesta. La pregunta lateral se ejecuta de forma independiente y no interrumpe el turno principal.
* **Sin acceso a herramientas**: las preguntas laterales responden solo desde lo que ya está en contexto. Claude no puede leer archivos, ejecutar comandos o buscar al responder una pregunta lateral.
* **Respuesta única**: no hay turnos de seguimiento. Si necesita una conversación de ida y vuelta, use una indicación normal en su lugar.
* **Bajo costo**: la pregunta lateral reutiliza el caché de indicación de la conversación principal, por lo que el costo adicional es mínimo.

Presione **Espacio**, **Enter** o **Escape** para descartar la respuesta y volver a la indicación.

`/btw` es lo opuesto a un [subagent](/es/sub-agents): ve su conversación completa pero no tiene herramientas, mientras que un subagent tiene herramientas completas pero comienza con un contexto vacío. Use `/btw` para preguntar sobre lo que Claude ya sabe de esta sesión; use un subagent para descubrir algo nuevo.

## Lista de tareas

Cuando trabaja en trabajo complejo de varios pasos, Claude crea una lista de tareas para rastrear el progreso. Las tareas aparecen en el área de estado de su terminal con indicadores que muestran qué está pendiente, en progreso o completado.

* Presione `Ctrl+T` para alternar la vista de la lista de tareas. La pantalla muestra hasta 5 tareas a la vez
* Para ver todas las tareas o borrarlas, pregunte a Claude directamente: "show me all tasks" o "clear all tasks"
* Las tareas persisten en compactaciones de contexto, ayudando a Claude a mantenerse organizado en proyectos más grandes
* Para compartir una lista de tareas entre sesiones, establezca `CLAUDE_CODE_TASK_LIST_ID` para usar un directorio nombrado en `~/.claude/tasks/`: `CLAUDE_CODE_TASK_LIST_ID=my-project claude`

## Resumen de sesión

Cuando regresa a la terminal después de alejarse, Claude Code muestra un resumen de una línea de lo que sucedió en la sesión hasta ahora. El resumen se genera en segundo plano una vez que han pasado al menos tres minutos desde el último turno completado y la terminal no está enfocada, por lo que está listo cuando vuelve a cambiar. Los resúmenes solo aparecen una vez que la sesión tiene al menos tres turnos, y nunca dos seguidas.

Ejecute `/recap` para generar un resumen bajo demanda. Para desactivar los resúmenes automáticos, abra `/config` y desactive **Session recap**.

El resumen de sesión está activado de forma predeterminada para todos los planes y proveedores. El resumen siempre se omite en modo no interactivo.

## Estado de revisión de PR

Cuando trabaja en una rama con una solicitud de extracción abierta, Claude Code muestra un enlace de PR en el que se puede hacer clic en el pie de página (por ejemplo, "PR #446"). El enlace tiene un subrayado de color que indica el estado de revisión:

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

* [Skills](/es/skills) - Indicaciones personalizadas y flujos de trabajo
* [Checkpointing](/es/checkpointing) - Rebobinar las ediciones de Claude y restaurar estados anteriores
* [Referencia de CLI](/es/cli-reference) - Banderas y opciones de línea de comandos
* [Configuración](/es/settings) - Opciones de configuración
* [Gestión de memoria](/es/memory) - Gestión de archivos CLAUDE.md
