> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Usar Claude Code en VS Code

> Instala y configura la extensión Claude Code para VS Code. Obtén asistencia de codificación con IA con diffs en línea, menciones @, revisión de planes y atajos de teclado.

<img src="https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=300652d5678c63905e6b0ea9e50835f8" alt="Editor de VS Code con el panel de extensión Claude Code abierto en el lado derecho, mostrando una conversación con Claude" width="2500" height="1155" data-path="images/vs-code-extension-interface.jpg" />

La extensión de VS Code proporciona una interfaz gráfica nativa para Claude Code, integrada directamente en tu IDE. Esta es la forma recomendada de usar Claude Code en VS Code.

Con la extensión, puedes revisar y editar los planes de Claude antes de aceptarlos, aceptar automáticamente ediciones a medida que se realizan, mencionar archivos con rangos de líneas específicas desde tu selección, acceder al historial de conversaciones y abrir múltiples conversaciones en pestañas o ventanas separadas.

## Requisitos previos

Antes de instalar, asegúrate de tener:

* VS Code 1.98.0 o superior
* Una cuenta de Anthropic (iniciarás sesión cuando abras la extensión por primera vez). Si estás usando un proveedor de terceros como Amazon Bedrock o Google Vertex AI, consulta [Usar proveedores de terceros](#usar-proveedores-de-terceros) en su lugar.

<Tip>
  La extensión incluye la CLI (interfaz de línea de comandos), a la que puedes acceder desde la terminal integrada de VS Code para funciones avanzadas. Consulta [Extensión de VS Code frente a Claude Code CLI](#extensión-de-vs-code-frente-a-claude-code-cli) para obtener más detalles.
</Tip>

## Instalar la extensión

Haz clic en el enlace de tu IDE para instalar directamente:

* [Instalar para VS Code](vscode:extension/anthropic.claude-code)
* [Instalar para Cursor](cursor:extension/anthropic.claude-code)

O en VS Code, presiona `Cmd+Shift+X` (Mac) o `Ctrl+Shift+X` (Windows/Linux) para abrir la vista de Extensiones, busca "Claude Code" y haz clic en **Instalar**.

<Note>Si la extensión no aparece después de la instalación, reinicia VS Code o ejecuta "Developer: Reload Window" desde la Paleta de comandos.</Note>

## Comenzar

Una vez instalada, puedes comenzar a usar Claude Code a través de la interfaz de VS Code:

<Steps>
  <Step title="Abre el panel de Claude Code">
    En todo VS Code, el icono Spark indica Claude Code: <img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/vs-code-spark-icon.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=3ca45e00deadec8c8f4b4f807da94505" alt="Icono Spark" style={{display: "inline", height: "0.85em", verticalAlign: "middle"}} width="16" height="16" data-path="images/vs-code-spark-icon.svg" />

    La forma más rápida de abrir Claude es hacer clic en el icono Spark en la **Barra de herramientas del editor** (esquina superior derecha del editor). El icono solo aparece cuando tienes un archivo abierto.

        <img src="https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=eb4540325d94664c51776dbbfec4cf02" alt="Editor de VS Code mostrando el icono Spark en la Barra de herramientas del editor" width="2796" height="734" data-path="images/vs-code-editor-icon.png" />

    Otras formas de abrir Claude Code:

    * **Barra de actividades**: haz clic en el icono Spark en la barra lateral izquierda para abrir la lista de sesiones. Haz clic en cualquier sesión para abrirla como una pestaña de editor completa, o inicia una nueva. Este icono siempre es visible en la Barra de actividades.
    * **Paleta de comandos**: `Cmd+Shift+P` (Mac) o `Ctrl+Shift+P` (Windows/Linux), escribe "Claude Code" y selecciona una opción como "Abrir en Nueva Pestaña"
    * **Barra de estado**: haz clic en **✱ Claude Code** en la esquina inferior derecha de la ventana. Esto funciona incluso cuando no hay ningún archivo abierto.

    Cuando abres el panel por primera vez, aparece una lista de verificación **Aprender Claude Code**. Trabaja en cada elemento haciendo clic en **Mostrarme**, o descártalo con la X. Para reabrirlo más tarde, desactiva **Ocultar incorporación** en la configuración de VS Code en Extensiones → Claude Code.

    Puedes arrastrar el panel de Claude para reposicionarlo en cualquier lugar de VS Code. Consulta [Personaliza tu flujo de trabajo](#personaliza-tu-flujo-de-trabajo) para obtener más detalles.
  </Step>

  <Step title="Envía un mensaje">
    Pídele a Claude que te ayude con tu código o archivos, ya sea explicando cómo funciona algo, depurando un problema o realizando cambios.

    <Tip>Claude ve automáticamente tu texto seleccionado. Presiona `Option+K` (Mac) / `Alt+K` (Windows/Linux) para también insertar una referencia de mención @ (como `@file.ts#5-10`) en tu mensaje.</Tip>

    Aquí hay un ejemplo de cómo hacer una pregunta sobre una línea particular en un archivo:

        <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-send-prompt.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=ede3ed8d8d5f940e01c5de636d009cfd" alt="Editor de VS Code con las líneas 2-3 seleccionadas en un archivo Python, y el panel de Claude Code mostrando una pregunta sobre esas líneas con una referencia de mención @" width="3288" height="1876" data-path="images/vs-code-send-prompt.png" />
  </Step>

  <Step title="Revisa los cambios">
    Cuando Claude quiere editar un archivo, muestra una comparación lado a lado del original y los cambios propuestos, luego solicita permiso. Puedes aceptar, rechazar o decirle a Claude qué hacer en su lugar.

        <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-edits.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=e005f9b41c541c5c7c59c082f7c4841c" alt="VS Code mostrando un diff de los cambios propuestos por Claude con un mensaje de permiso preguntando si realizar la edición" width="3292" height="1876" data-path="images/vs-code-edits.png" />
  </Step>
</Steps>

Para más ideas sobre lo que puedes hacer con Claude Code, consulta [Flujos de trabajo comunes](/es/common-workflows).

<Tip>
  Ejecuta "Claude Code: Open Walkthrough" desde la Paleta de comandos para un tour guiado de los conceptos básicos.
</Tip>

## Usa el cuadro de mensaje

El cuadro de mensaje admite varias funciones:

* **Modos de permiso**: haz clic en el indicador de modo en la parte inferior del cuadro de mensaje para cambiar de modo. En modo normal, Claude solicita permiso antes de cada acción. En Plan Mode, Claude describe lo que hará y espera aprobación antes de realizar cambios. VS Code abre automáticamente el plan como un documento markdown completo donde puedes agregar comentarios en línea para dar retroalimentación antes de que Claude comience. En modo de aceptación automática, Claude realiza ediciones sin preguntar. Establece el valor predeterminado en la configuración de VS Code en `claudeCode.initialPermissionMode`.
* **Menú de comandos**: haz clic en `/` o escribe `/` para abrir el menú de comandos. Las opciones incluyen adjuntar archivos, cambiar modelos, alternar pensamiento extendido y ver el uso del plan (`/usage`). La sección Personalizar proporciona acceso a MCP servers, hooks, memoria, permisos y plugins. Los elementos con un icono de terminal se abren en la terminal integrada.
* **Indicador de contexto**: el cuadro de mensaje muestra cuánto de la ventana de contexto de Claude estás usando. Claude se compacta automáticamente cuando es necesario, o puedes ejecutar `/compact` manualmente.
* **Pensamiento extendido**: permite que Claude dedique más tiempo a razonar sobre problemas complejos. Actívalo a través del menú de comandos (`/`). Consulta [Pensamiento extendido](/es/common-workflows#use-extended-thinking-thinking-mode) para obtener más detalles.
* **Entrada multilínea**: presiona `Shift+Enter` para agregar una nueva línea sin enviar. Esto también funciona en la entrada de texto libre "Otro" de los diálogos de preguntas.

### Referencia de archivos y carpetas

Usa menciones @ para darle a Claude contexto sobre archivos o carpetas específicas. Cuando escribes `@` seguido de un nombre de archivo o carpeta, Claude lee ese contenido y puede responder preguntas sobre él o realizar cambios en él. Claude Code admite coincidencia difusa, por lo que puedes escribir nombres parciales para encontrar lo que necesitas:

```text  theme={null}
> Explain the logic in @auth (fuzzy matches auth.js, AuthService.ts, etc.)
> What's in @src/components/ (include a trailing slash for folders)
```

Para archivos PDF grandes, puedes pedirle a Claude que lea páginas específicas en lugar del archivo completo: una sola página, un rango como páginas 1-10, o un rango abierto como página 3 en adelante.

Cuando seleccionas texto en el editor, Claude puede ver tu código resaltado automáticamente. El pie de página del cuadro de mensaje muestra cuántas líneas están seleccionadas. Presiona `Option+K` (Mac) / `Alt+K` (Windows/Linux) para insertar una mención @ con la ruta del archivo y los números de línea (por ejemplo, `@app.ts#5-10`). Haz clic en el indicador de selección para alternar si Claude puede ver tu texto resaltado: el icono de barra diagonal significa que la selección está oculta para Claude.

También puedes mantener presionado `Shift` mientras arrastras archivos al cuadro de mensaje para agregarlos como adjuntos. Haz clic en la X en cualquier adjunto para eliminarlo del contexto.

### Reanuda conversaciones pasadas

Haz clic en el menú desplegable en la parte superior del panel de Claude Code para acceder a tu historial de conversaciones. Puedes buscar por palabra clave o explorar por tiempo (Hoy, Ayer, Últimos 7 días, etc.). Haz clic en cualquier conversación para reanudarla con el historial de mensajes completo. Pasa el cursor sobre una sesión para revelar acciones de cambio de nombre y eliminación: cambia el nombre para darle un título descriptivo, o elimina para borrarlo de la lista. Para más información sobre cómo reanudar sesiones, consulta [Flujos de trabajo comunes](/es/common-workflows#resume-previous-conversations).

### Reanuda sesiones remotas desde Claude.ai

Si usas [Claude Code en la web](/es/claude-code-on-the-web), puedes reanudar esas sesiones remotas directamente en VS Code. Esto requiere iniciar sesión con **Claude.ai Subscription**, no Anthropic Console.

<Steps>
  <Step title="Abre Conversaciones pasadas">
    Haz clic en el menú desplegable **Conversaciones pasadas** en la parte superior del panel de Claude Code.
  </Step>

  <Step title="Selecciona la pestaña Remota">
    El diálogo muestra dos pestañas: Local y Remota. Haz clic en **Remota** para ver sesiones desde claude.ai.
  </Step>

  <Step title="Selecciona una sesión para reanudar">
    Explora o busca tus sesiones remotas. Haz clic en cualquier sesión para descargarla y continuar la conversación localmente.
  </Step>
</Steps>

<Note>
  Solo las sesiones web iniciadas con un repositorio de GitHub aparecen en la pestaña Remota. Reanudar carga el historial de conversaciones localmente; los cambios no se sincronizan de vuelta a claude.ai.
</Note>

## Personaliza tu flujo de trabajo

Una vez que estés en funcionamiento, puedes reposicionar el panel de Claude, ejecutar múltiples sesiones o cambiar al modo terminal.

### Elige dónde vive Claude

Puedes arrastrar el panel de Claude para reposicionarlo en cualquier lugar de VS Code. Agarra la pestaña o barra de título del panel y arrástralo a:

* **Barra lateral secundaria**: el lado derecho de la ventana. Mantiene a Claude visible mientras codificas.
* **Barra lateral principal**: la barra lateral izquierda con iconos para Explorador, Búsqueda, etc.
* **Área del editor**: abre Claude como una pestaña junto a tus archivos. Útil para tareas secundarias.

<Tip>
  Usa la barra lateral para tu sesión principal de Claude y abre pestañas adicionales para tareas secundarias. Claude recuerda tu ubicación preferida. El icono de lista de sesiones de la Barra de actividades es separado del panel de Claude: la lista de sesiones siempre es visible en la Barra de actividades, mientras que el icono del panel de Claude solo aparece allí cuando el panel está acoplado a la barra lateral izquierda.
</Tip>

### Ejecuta múltiples conversaciones

Usa **Abrir en Nueva Pestaña** u **Abrir en Nueva Ventana** desde la Paleta de comandos para iniciar conversaciones adicionales. Cada conversación mantiene su propio historial y contexto, permitiéndote trabajar en diferentes tareas en paralelo.

Cuando usas pestañas, un pequeño punto de color en el icono spark indica el estado: azul significa que hay una solicitud de permiso pendiente, naranja significa que Claude terminó mientras la pestaña estaba oculta.

### Cambia al modo terminal

De forma predeterminada, la extensión abre un panel de chat gráfico. Si prefieres la interfaz de estilo CLI, abre la [configuración Usar terminal](vscode://settings/claudeCode.useTerminal) y marca la casilla.

También puedes abrir la configuración de VS Code (`Cmd+,` en Mac o `Ctrl+,` en Windows/Linux), ve a Extensiones → Claude Code y marca **Usar terminal**.

## Gestiona plugins

La extensión de VS Code incluye una interfaz gráfica para instalar y gestionar [plugins](/es/plugins). Escribe `/plugins` en el cuadro de mensaje para abrir la interfaz **Gestionar plugins**.

### Instala plugins

El diálogo de plugins muestra dos pestañas: **Plugins** y **Marketplaces**.

En la pestaña Plugins:

* Los **plugins instalados** aparecen en la parte superior con interruptores de alternancia para habilitarlos o deshabilitarlos
* Los **plugins disponibles** de tus marketplaces configurados aparecen a continuación
* Busca para filtrar plugins por nombre o descripción
* Haz clic en **Instalar** en cualquier plugin disponible

Cuando instalas un plugin, elige el alcance de instalación:

* **Instalar para ti**: disponible en todos tus proyectos (alcance de usuario)
* **Instalar para este proyecto**: compartido con colaboradores del proyecto (alcance del proyecto)
* **Instalar localmente**: solo para ti, solo en este repositorio (alcance local)

### Gestiona marketplaces

Cambia a la pestaña **Marketplaces** para agregar o eliminar fuentes de plugins:

* Ingresa un repositorio de GitHub, URL o ruta local para agregar un nuevo marketplace
* Haz clic en el icono de actualización para actualizar la lista de plugins de un marketplace
* Haz clic en el icono de papelera para eliminar un marketplace

Después de realizar cambios, un banner te solicita que reinicies Claude Code para aplicar las actualizaciones.

<Note>
  La gestión de plugins en VS Code usa los mismos comandos CLI bajo el capó. Los plugins y marketplaces que configures en la extensión también están disponibles en la CLI, y viceversa.
</Note>

Para más información sobre el sistema de plugins, consulta [Plugins](/es/plugins) y [Marketplaces de plugins](/es/plugin-marketplaces).

## Automatiza tareas del navegador con Chrome

Conecta Claude a tu navegador Chrome para probar aplicaciones web, depurar con registros de consola y automatizar flujos de trabajo del navegador sin salir de VS Code. Esto requiere la [extensión Claude in Chrome](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) versión 1.0.36 o superior.

Escribe `@browser` en el cuadro de mensaje seguido de lo que quieres que Claude haga:

```text  theme={null}
@browser go to localhost:3000 and check the console for errors
```

También puedes abrir el menú de adjuntos para seleccionar herramientas específicas del navegador como abrir una nueva pestaña o leer el contenido de la página.

Claude abre nuevas pestañas para tareas del navegador y comparte el estado de inicio de sesión de tu navegador, por lo que puede acceder a cualquier sitio en el que ya hayas iniciado sesión.

Para instrucciones de configuración, la lista completa de capacidades y solución de problemas, consulta [Usar Claude Code con Chrome](/es/chrome).

## Comandos y atajos de teclado de VS Code

Abre la Paleta de comandos (`Cmd+Shift+P` en Mac o `Ctrl+Shift+P` en Windows/Linux) y escribe "Claude Code" para ver todos los comandos de VS Code disponibles para la extensión Claude Code.

Algunos atajos dependen de qué panel esté "enfocado" (recibiendo entrada de teclado). Cuando tu cursor está en un archivo de código, el editor está enfocado. Cuando tu cursor está en el cuadro de mensaje de Claude, Claude está enfocado. Usa `Cmd+Esc` / `Ctrl+Esc` para alternar entre ellos.

<Note>
  Estos son comandos de VS Code para controlar la extensión. No todos los comandos integrados de Claude Code están disponibles en la extensión. Consulta [Extensión de VS Code frente a Claude Code CLI](#extensión-de-vs-code-frente-a-claude-code-cli) para obtener más detalles.
</Note>

| Comando                    | Atajo                                                    | Descripción                                                                                    |
| -------------------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Focus Input                | `Cmd+Esc` (Mac) / `Ctrl+Esc` (Windows/Linux)             | Alterna el enfoque entre el editor y Claude                                                    |
| Open in Side Bar           | -                                                        | Abre Claude en la barra lateral izquierda                                                      |
| Open in Terminal           | -                                                        | Abre Claude en modo terminal                                                                   |
| Open in New Tab            | `Cmd+Shift+Esc` (Mac) / `Ctrl+Shift+Esc` (Windows/Linux) | Abre una nueva conversación como una pestaña del editor                                        |
| Open in New Window         | -                                                        | Abre una nueva conversación en una ventana separada                                            |
| New Conversation           | `Cmd+N` (Mac) / `Ctrl+N` (Windows/Linux)                 | Inicia una nueva conversación (requiere que Claude esté enfocado)                              |
| Insert @-Mention Reference | `Option+K` (Mac) / `Alt+K` (Windows/Linux)               | Inserta una referencia al archivo actual y la selección (requiere que el editor esté enfocado) |
| Show Logs                  | -                                                        | Ver registros de depuración de la extensión                                                    |
| Logout                     | -                                                        | Cierra sesión de tu cuenta de Anthropic                                                        |

## Configura la configuración

La extensión tiene dos tipos de configuración:

* **Configuración de extensión** en VS Code: controla el comportamiento de la extensión dentro de VS Code. Abre con `Cmd+,` (Mac) o `Ctrl+,` (Windows/Linux), luego ve a Extensiones → Claude Code. También puedes escribir `/` y seleccionar **General Config** para abrir la configuración.
* **Configuración de Claude Code** en `~/.claude/settings.json`: compartida entre la extensión y la CLI. Úsala para comandos permitidos, variables de entorno, hooks y MCP servers. Consulta [Configuración](/es/settings) para obtener más detalles.

<Tip>
  Agrega `"$schema": "https://json.schemastore.org/claude-code-settings.json"` a tu `settings.json` para obtener autocompletado y validación en línea para todas las configuraciones disponibles directamente en VS Code.
</Tip>

### Configuración de extensión

| Configuración                     | Predeterminado | Descripción                                                                                                                              |
| --------------------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `selectedModel`                   | `default`      | Modelo para nuevas conversaciones. Cambia por sesión con `/model`.                                                                       |
| `useTerminal`                     | `false`        | Lanza Claude en modo terminal en lugar de panel gráfico                                                                                  |
| `initialPermissionMode`           | `default`      | Controla mensajes de aprobación: `default` (preguntar cada vez), `plan`, `acceptEdits` o `bypassPermissions`                             |
| `preferredLocation`               | `panel`        | Dónde se abre Claude: `sidebar` (derecha) o `panel` (nueva pestaña)                                                                      |
| `autosave`                        | `true`         | Guarda automáticamente archivos antes de que Claude los lea o escriba                                                                    |
| `useCtrlEnterToSend`              | `false`        | Usa Ctrl/Cmd+Enter en lugar de Enter para enviar mensajes                                                                                |
| `enableNewConversationShortcut`   | `true`         | Habilita Cmd/Ctrl+N para iniciar una nueva conversación                                                                                  |
| `hideOnboarding`                  | `false`        | Oculta la lista de verificación de incorporación (icono de gorro de graduación)                                                          |
| `respectGitIgnore`                | `true`         | Excluye patrones de .gitignore de búsquedas de archivos                                                                                  |
| `environmentVariables`            | `[]`           | Establece variables de entorno para el proceso de Claude. Usa la configuración de Claude Code en su lugar para configuración compartida. |
| `disableLoginPrompt`              | `false`        | Omite mensajes de autenticación (para configuraciones de proveedores de terceros)                                                        |
| `allowDangerouslySkipPermissions` | `false`        | Omite todos los mensajes de permiso. **Usa con extrema precaución.**                                                                     |
| `claudeProcessWrapper`            | -              | Ruta ejecutable utilizada para lanzar el proceso de Claude                                                                               |

## Extensión de VS Code frente a Claude Code CLI

Claude Code está disponible tanto como una extensión de VS Code (panel gráfico) como una CLI (interfaz de línea de comandos en la terminal). Algunas funciones solo están disponibles en la CLI. Si necesitas una función solo de CLI, ejecuta `claude` en la terminal integrada de VS Code.

| Función                     | CLI                                             | Extensión de VS Code                                                                                       |
| --------------------------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Comandos y skills           | [Todos](/es/interactive-mode#built-in-commands) | Subconjunto (escribe `/` para ver disponibles)                                                             |
| Configuración de MCP server | Sí                                              | Parcial (agrega servidores a través de CLI; gestiona servidores existentes con `/mcp` en el panel de chat) |
| Checkpoints                 | Sí                                              | Sí                                                                                                         |
| Atajo bash `!`              | Sí                                              | No                                                                                                         |
| Autocompletado de pestañas  | Sí                                              | No                                                                                                         |

### Retrocede con checkpoints

La extensión de VS Code admite checkpoints, que rastrean las ediciones de archivos de Claude y te permiten retroceder a un estado anterior. Pasa el cursor sobre cualquier mensaje para revelar el botón de retroceso, luego elige entre tres opciones:

* **Bifurcar conversación desde aquí**: inicia una nueva rama de conversación desde este mensaje mientras mantienes todos los cambios de código intactos
* **Retroceder código a aquí**: revierte los cambios de archivo a este punto en la conversación mientras mantienes el historial de conversación completo
* **Bifurcar conversación y retroceder código**: inicia una nueva rama de conversación y revierte los cambios de archivo a este punto

Para obtener detalles completos sobre cómo funcionan los checkpoints y sus limitaciones, consulta [Checkpointing](/es/checkpointing).

### Ejecuta CLI en VS Code

Para usar la CLI mientras permaneces en VS Code, abre la terminal integrada (`` Ctrl+` `` en Windows/Linux o `` Cmd+` `` en Mac) y ejecuta `claude`. La CLI se integra automáticamente con tu IDE para funciones como visualización de diffs y compartir diagnósticos.

Si usas una terminal externa, ejecuta `/ide` dentro de Claude Code para conectarlo a VS Code.

### Cambia entre extensión y CLI

La extensión y la CLI comparten el mismo historial de conversaciones. Para continuar una conversación de extensión en la CLI, ejecuta `claude --resume` en la terminal. Esto abre un selector interactivo donde puedes buscar y seleccionar tu conversación.

### Incluye salida de terminal en mensajes

Referencia la salida de terminal en tus mensajes usando `@terminal:name` donde `name` es el título de la terminal. Esto permite que Claude vea la salida del comando, mensajes de error o registros sin copiar y pegar.

### Monitorea procesos en segundo plano

Cuando Claude ejecuta comandos de larga duración, la extensión muestra el progreso en la barra de estado. Sin embargo, la visibilidad de tareas en segundo plano es limitada en comparación con la CLI. Para mejor visibilidad, haz que Claude genere el comando para que puedas ejecutarlo en la terminal integrada de VS Code.

### Conecta con herramientas externas con MCP

Los servidores MCP (Model Context Protocol) dan a Claude acceso a herramientas externas, bases de datos y APIs.

Para agregar un servidor MCP, abre la terminal integrada (`` Ctrl+` `` o `` Cmd+` ``) y ejecuta:

```bash  theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

Una vez configurado, pídele a Claude que use las herramientas (por ejemplo, "Review PR #456").

Para gestionar servidores MCP sin salir de VS Code, escribe `/mcp` en el panel de chat. El diálogo de gestión de MCP te permite habilitar o deshabilitar servidores, reconectarse a un servidor y gestionar la autenticación OAuth. Consulta la [documentación de MCP](/es/mcp) para servidores disponibles.

## Trabaja con git

Claude Code se integra con git para ayudarte con flujos de trabajo de control de versiones directamente en VS Code. Pídele a Claude que confirme cambios, cree solicitudes de extracción o trabaje en diferentes ramas.

### Crea commits y solicitudes de extracción

Claude puede preparar cambios, escribir mensajes de commit y crear solicitudes de extracción basadas en tu trabajo:

```text  theme={null}
> commit my changes with a descriptive message
> create a pr for this feature
> summarize the changes I've made to the auth module
```

Al crear solicitudes de extracción, Claude genera descripciones basadas en los cambios de código reales y puede agregar contexto sobre pruebas o decisiones de implementación.

### Usa git worktrees para tareas paralelas

Usa el indicador `--worktree` (`-w`) para iniciar Claude en un worktree aislado con sus propios archivos y rama:

```bash  theme={null}
claude --worktree feature-auth
```

Cada worktree mantiene un estado de archivo independiente mientras comparte el historial de git. Esto evita que las instancias de Claude interfieran entre sí cuando trabajan en diferentes tareas. Para más detalles, consulta [Ejecuta sesiones paralelas de Claude Code con Git worktrees](/es/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees).

## Usa proveedores de terceros

De forma predeterminada, Claude Code se conecta directamente a la API de Anthropic. Si tu organización usa Amazon Bedrock, Google Vertex AI o Microsoft Foundry para acceder a Claude, configura la extensión para usar tu proveedor en su lugar:

<Steps>
  <Step title="Desactiva el mensaje de inicio de sesión">
    Abre la [configuración Desactivar mensaje de inicio de sesión](vscode://settings/claudeCode.disableLoginPrompt) y marca la casilla.

    También puedes abrir la configuración de VS Code (`Cmd+,` en Mac o `Ctrl+,` en Windows/Linux), buscar "Claude Code login" y marcar **Desactivar mensaje de inicio de sesión**.
  </Step>

  <Step title="Configura tu proveedor">
    Sigue la guía de configuración para tu proveedor:

    * [Claude Code en Amazon Bedrock](/es/amazon-bedrock)
    * [Claude Code en Google Vertex AI](/es/google-vertex-ai)
    * [Claude Code en Microsoft Foundry](/es/microsoft-foundry)

    Estas guías cubren la configuración de tu proveedor en `~/.claude/settings.json`, lo que garantiza que tus configuraciones se compartan entre la extensión de VS Code y la CLI.
  </Step>
</Steps>

## Seguridad y privacidad

Tu código permanece privado. Claude Code procesa tu código para proporcionar asistencia pero no lo usa para entrenar modelos. Para obtener detalles sobre el manejo de datos y cómo optar por no participar en el registro, consulta [Datos y privacidad](/es/data-usage).

Con permisos de edición automática habilitados, Claude Code puede modificar archivos de configuración de VS Code (como `settings.json` o `tasks.json`) que VS Code puede ejecutar automáticamente. Para reducir el riesgo al trabajar con código no confiable:

* Habilita [Modo restringido de VS Code](https://code.visualstudio.com/docs/editor/workspace-trust#_restricted-mode) para espacios de trabajo no confiables
* Usa modo de aprobación manual en lugar de aceptación automática para ediciones
* Revisa cuidadosamente los cambios antes de aceptarlos

## Soluciona problemas comunes

### La extensión no se instala

* Asegúrate de tener una versión compatible de VS Code (1.98.0 o posterior)
* Verifica que VS Code tenga permiso para instalar extensiones
* Intenta instalar directamente desde [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)

### El icono Spark no es visible

El icono Spark aparece en la **Barra de herramientas del editor** (esquina superior derecha del editor) cuando tienes un archivo abierto. Si no lo ves:

1. **Abre un archivo**: El icono requiere que un archivo esté abierto. Solo tener una carpeta abierta no es suficiente.
2. **Verifica la versión de VS Code**: Requiere 1.98.0 o superior (Ayuda → Acerca de)
3. **Reinicia VS Code**: Ejecuta "Developer: Reload Window" desde la Paleta de comandos
4. **Desactiva extensiones conflictivas**: Desactiva temporalmente otras extensiones de IA (Cline, Continue, etc.)
5. **Verifica la confianza del espacio de trabajo**: La extensión no funciona en Modo restringido

Alternativamente, haz clic en "✱ Claude Code" en la **Barra de estado** (esquina inferior derecha). Esto funciona incluso sin un archivo abierto. También puedes usar la **Paleta de comandos** (`Cmd+Shift+P` / `Ctrl+Shift+P`) y escribir "Claude Code".

### Claude Code nunca responde

Si Claude Code no responde a tus mensajes:

1. **Verifica tu conexión a Internet**: Asegúrate de tener una conexión a Internet estable
2. **Inicia una nueva conversación**: Intenta iniciar una conversación nueva para ver si el problema persiste
3. **Prueba la CLI**: Ejecuta `claude` desde la terminal para ver si obtienes mensajes de error más detallados

Si los problemas persisten, [abre un problema en GitHub](https://github.com/anthropics/claude-code/issues) con detalles sobre el error.

## Desinstala la extensión

Para desinstalar la extensión Claude Code:

1. Abre la vista de Extensiones (`Cmd+Shift+X` en Mac o `Ctrl+Shift+X` en Windows/Linux)
2. Busca "Claude Code"
3. Haz clic en **Desinstalar**

Para también eliminar datos de extensión y restablecer toda la configuración:

```bash  theme={null}
rm -rf ~/.vscode/globalStorage/anthropic.claude-code
```

Para obtener ayuda adicional, consulta la [guía de solución de problemas](/es/troubleshooting).

## Próximos pasos

Ahora que tienes Claude Code configurado en VS Code:

* [Explora flujos de trabajo comunes](/es/common-workflows) para aprovechar al máximo Claude Code
* [Configura MCP servers](/es/mcp) para extender las capacidades de Claude con herramientas externas. Agrega servidores usando la CLI, luego gestiónalos con `/mcp` en el panel de chat.
* [Configura la configuración de Claude Code](/es/settings) para personalizar comandos permitidos, hooks y más. Estas configuraciones se comparten entre la extensión y la CLI.
