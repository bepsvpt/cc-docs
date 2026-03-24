> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Usar Claude Code en VS Code

> Instala y configura la extensión Claude Code para VS Code. Obtén asistencia de codificación con IA con diffs en línea, menciones @, revisión de planes y atajos de teclado.

<img src="https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=300652d5678c63905e6b0ea9e50835f8" alt="Editor de VS Code con el panel de extensión Claude Code abierto en el lado derecho, mostrando una conversación con Claude" width="2500" height="1155" data-path="images/vs-code-extension-interface.jpg" />

La extensión de VS Code proporciona una interfaz gráfica nativa para Claude Code, integrada directamente en su IDE. Esta es la forma recomendada de usar Claude Code en VS Code.

Con la extensión, puede revisar y editar los planes de Claude antes de aceptarlos, aceptar automáticamente ediciones a medida que se realizan, mencionar archivos con rangos de líneas específicas de su selección, acceder al historial de conversaciones y abrir múltiples conversaciones en pestañas o ventanas separadas.

## Requisitos previos

Antes de instalar, asegúrese de tener:

* VS Code 1.98.0 o superior
* Una cuenta de Anthropic (iniciará sesión cuando abra la extensión por primera vez). Si está utilizando un proveedor de terceros como Amazon Bedrock o Google Vertex AI, consulte [Usar proveedores de terceros](#usar-proveedores-de-terceros) en su lugar.

<Tip>
  La extensión incluye la CLI (interfaz de línea de comandos), a la que puede acceder desde la terminal integrada de VS Code para funciones avanzadas. Consulte [Extensión de VS Code frente a CLI de Claude Code](#extensión-de-vs-code-frente-a-cli-de-claude-code) para obtener más detalles.
</Tip>

## Instalar la extensión

Haga clic en el enlace de su IDE para instalar directamente:

* [Instalar para VS Code](vscode:extension/anthropic.claude-code)
* [Instalar para Cursor](cursor:extension/anthropic.claude-code)

O en VS Code, presione `Cmd+Shift+X` (Mac) o `Ctrl+Shift+X` (Windows/Linux) para abrir la vista Extensiones, busque "Claude Code" y haga clic en **Instalar**.

<Note>Si la extensión no aparece después de la instalación, reinicie VS Code o ejecute "Developer: Reload Window" desde la Paleta de comandos.</Note>

## Comenzar

Una vez instalada, puede comenzar a usar Claude Code a través de la interfaz de VS Code:

<Steps>
  <Step title="Abrir el panel de Claude Code">
    En todo VS Code, el icono Spark indica Claude Code: <img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/vs-code-spark-icon.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=3ca45e00deadec8c8f4b4f807da94505" alt="Icono Spark" style={{display: "inline", height: "0.85em", verticalAlign: "middle"}} width="16" height="16" data-path="images/vs-code-spark-icon.svg" />

    La forma más rápida de abrir Claude es hacer clic en el icono Spark en la **Barra de herramientas del editor** (esquina superior derecha del editor). El icono solo aparece cuando tiene un archivo abierto.

        <img src="https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=eb4540325d94664c51776dbbfec4cf02" alt="Editor de VS Code mostrando el icono Spark en la Barra de herramientas del editor" width="2796" height="734" data-path="images/vs-code-editor-icon.png" />

    Otras formas de abrir Claude Code:

    * **Barra de actividades**: haga clic en el icono Spark en la barra lateral izquierda para abrir la lista de sesiones. Haga clic en cualquier sesión para abrirla como una pestaña de editor completa, o inicie una nueva. Este icono siempre es visible en la Barra de actividades.
    * **Paleta de comandos**: `Cmd+Shift+P` (Mac) o `Ctrl+Shift+P` (Windows/Linux), escriba "Claude Code" y seleccione una opción como "Abrir en Nueva Pestaña"
    * **Barra de estado**: haga clic en **✱ Claude Code** en la esquina inferior derecha de la ventana. Esto funciona incluso cuando no hay ningún archivo abierto.

    Cuando abre el panel por primera vez, aparece una lista de verificación **Aprender Claude Code**. Trabaje en cada elemento haciendo clic en **Mostrarme**, o descártelo con la X. Para reabrirlo más tarde, desmarque **Ocultar incorporación** en la configuración de VS Code en Extensiones → Claude Code.

    Puede arrastrar el panel de Claude para reposicionarlo en cualquier lugar de VS Code. Consulte [Personalizar su flujo de trabajo](#personalizar-su-flujo-de-trabajo) para obtener más detalles.
  </Step>

  <Step title="Enviar un mensaje">
    Pida a Claude que le ayude con su código o archivos, ya sea explicando cómo funciona algo, depurando un problema o realizando cambios.

    <Tip>Claude ve automáticamente su texto seleccionado. Presione `Option+K` (Mac) / `Alt+K` (Windows/Linux) para también insertar una referencia de mención @ (como `@file.ts#5-10`) en su mensaje.</Tip>

    Aquí hay un ejemplo de cómo hacer una pregunta sobre una línea particular en un archivo:

        <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-send-prompt.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=ede3ed8d8d5f940e01c5de636d009cfd" alt="Editor de VS Code con las líneas 2-3 seleccionadas en un archivo Python, y el panel de Claude Code mostrando una pregunta sobre esas líneas con una referencia de mención @" width="3288" height="1876" data-path="images/vs-code-send-prompt.png" />
  </Step>

  <Step title="Revisar cambios">
    Cuando Claude quiere editar un archivo, muestra una comparación lado a lado del original y los cambios propuestos, luego solicita permiso. Puede aceptar, rechazar o decirle a Claude qué hacer en su lugar.

        <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-edits.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=e005f9b41c541c5c7c59c082f7c4841c" alt="VS Code mostrando un diff de los cambios propuestos por Claude con un mensaje de permiso preguntando si realizar la edición" width="3292" height="1876" data-path="images/vs-code-edits.png" />
  </Step>
</Steps>

Para más ideas sobre lo que puede hacer con Claude Code, consulte [Flujos de trabajo comunes](/es/common-workflows).

<Tip>
  Ejecute "Claude Code: Open Walkthrough" desde la Paleta de comandos para un tour guiado de los conceptos básicos.
</Tip>

## Usar el cuadro de mensaje

El cuadro de mensaje admite varias características:

* **Modos de permiso**: haga clic en el indicador de modo en la parte inferior del cuadro de mensaje para cambiar de modo. En modo normal, Claude solicita permiso antes de cada acción. En Plan Mode, Claude describe lo que hará y espera aprobación antes de realizar cambios. VS Code abre automáticamente el plan como un documento markdown completo donde puede agregar comentarios en línea para dar retroalimentación antes de que Claude comience. En modo de aceptación automática, Claude realiza ediciones sin preguntar. Establezca el valor predeterminado en la configuración de VS Code en `claudeCode.initialPermissionMode`.
* **Menú de comandos**: haga clic en `/` o escriba `/` para abrir el menú de comandos. Las opciones incluyen adjuntar archivos, cambiar modelos, alternar pensamiento extendido y ver uso del plan (`/usage`). La sección Personalizar proporciona acceso a MCP servers, hooks, memoria, permisos y plugins. Los elementos con un icono de terminal se abren en la terminal integrada.
* **Indicador de contexto**: el cuadro de mensaje muestra cuánto de la ventana de contexto de Claude está utilizando. Claude se compacta automáticamente cuando es necesario, o puede ejecutar `/compact` manualmente.
* **Pensamiento extendido**: permite que Claude dedique más tiempo a razonar sobre problemas complejos. Actívelo a través del menú de comandos (`/`). Consulte [Pensamiento extendido](/es/common-workflows#usar-pensamiento-extendido-thinking-mode) para obtener más detalles.
* **Entrada multilínea**: presione `Shift+Enter` para agregar una nueva línea sin enviar. Esto también funciona en la entrada de texto libre "Otro" de los diálogos de preguntas.

### Referenciar archivos y carpetas

Use menciones @ para dar a Claude contexto sobre archivos o carpetas específicas. Cuando escribe `@` seguido de un nombre de archivo o carpeta, Claude lee ese contenido y puede responder preguntas sobre él o realizar cambios en él. Claude Code admite coincidencia difusa, por lo que puede escribir nombres parciales para encontrar lo que necesita:

```text  theme={null}
> Explain the logic in @auth (fuzzy matches auth.js, AuthService.ts, etc.)
> What's in @src/components/ (include a trailing slash for folders)
```

Para archivos PDF grandes, puede pedirle a Claude que lea páginas específicas en lugar del archivo completo: una sola página, un rango como páginas 1-10, o un rango abierto como página 3 en adelante.

Cuando selecciona texto en el editor, Claude puede ver su código resaltado automáticamente. El pie de página del cuadro de mensaje muestra cuántas líneas están seleccionadas. Presione `Option+K` (Mac) / `Alt+K` (Windows/Linux) para insertar una mención @ con la ruta del archivo y los números de línea (por ejemplo, `@app.ts#5-10`). Haga clic en el indicador de selección para alternar si Claude puede ver su texto resaltado: el icono de barra diagonal significa que la selección está oculta para Claude.

También puede mantener presionado `Shift` mientras arrastra archivos al cuadro de mensaje para agregarlos como adjuntos. Haga clic en la X en cualquier adjunto para eliminarlo del contexto.

### Reanudar conversaciones pasadas

Haga clic en el menú desplegable en la parte superior del panel de Claude Code para acceder al historial de conversaciones. Puede buscar por palabra clave o examinar por tiempo (Hoy, Ayer, Últimos 7 días, etc.). Haga clic en cualquier conversación para reanudarla con el historial de mensajes completo. Pase el cursor sobre una sesión para revelar acciones de cambio de nombre y eliminación: cambie el nombre para darle un título descriptivo, o elimine para borrarlo de la lista. Para más información sobre cómo reanudar sesiones, consulte [Flujos de trabajo comunes](/es/common-workflows#reanudar-conversaciones-anteriores).

### Reanudar sesiones remotas desde Claude.ai

Si utiliza [Claude Code en la web](/es/claude-code-on-the-web), puede reanudar esas sesiones remotas directamente en VS Code. Esto requiere iniciar sesión con **Claude.ai Subscription**, no Anthropic Console.

<Steps>
  <Step title="Abrir conversaciones pasadas">
    Haga clic en el menú desplegable **Conversaciones pasadas** en la parte superior del panel de Claude Code.
  </Step>

  <Step title="Seleccionar la pestaña Remoto">
    El diálogo muestra dos pestañas: Local y Remoto. Haga clic en **Remoto** para ver sesiones desde claude.ai.
  </Step>

  <Step title="Seleccionar una sesión para reanudar">
    Examine o busque sus sesiones remotas. Haga clic en cualquier sesión para descargarla y continuar la conversación localmente.
  </Step>
</Steps>

<Note>
  Solo las sesiones web iniciadas con un repositorio de GitHub aparecen en la pestaña Remoto. Reanudar carga el historial de conversaciones localmente; los cambios no se sincronizan de vuelta a claude.ai.
</Note>

## Personalizar su flujo de trabajo

Una vez que esté en funcionamiento, puede reposicionar el panel de Claude, ejecutar múltiples sesiones o cambiar al modo terminal.

### Elegir dónde vive Claude

Puede arrastrar el panel de Claude para reposicionarlo en cualquier lugar de VS Code. Agarre la pestaña o barra de título del panel y arrástrelo a:

* **Barra lateral secundaria**: el lado derecho de la ventana. Mantiene a Claude visible mientras codifica.
* **Barra lateral principal**: la barra lateral izquierda con iconos para Explorador, Búsqueda, etc.
* **Área del editor**: abre Claude como una pestaña junto a sus archivos. Útil para tareas secundarias.

<Tip>
  Use la barra lateral para su sesión principal de Claude y abra pestañas adicionales para tareas secundarias. Claude recuerda su ubicación preferida. El icono de lista de sesiones de la Barra de actividades es separado del panel de Claude: la lista de sesiones siempre es visible en la Barra de actividades, mientras que el icono del panel de Claude solo aparece allí cuando el panel está acoplado a la barra lateral izquierda.
</Tip>

### Ejecutar múltiples conversaciones

Use **Abrir en Nueva Pestaña** u **Abrir en Nueva Ventana** desde la Paleta de comandos para iniciar conversaciones adicionales. Cada conversación mantiene su propio historial y contexto, permitiéndole trabajar en diferentes tareas en paralelo.

Cuando usa pestañas, un pequeño punto de color en el icono spark indica el estado: azul significa que hay una solicitud de permiso pendiente, naranja significa que Claude terminó mientras la pestaña estaba oculta.

### Cambiar al modo terminal

De forma predeterminada, la extensión abre un panel de chat gráfico. Si prefiere la interfaz de estilo CLI, abra la [configuración Usar terminal](vscode://settings/claudeCode.useTerminal) y marque la casilla.

También puede abrir la configuración de VS Code (`Cmd+,` en Mac o `Ctrl+,` en Windows/Linux), ir a Extensiones → Claude Code y marcar **Usar terminal**.

## Administrar plugins

La extensión de VS Code incluye una interfaz gráfica para instalar y administrar [plugins](/es/plugins). Escriba `/plugins` en el cuadro de mensaje para abrir la interfaz **Administrar plugins**.

### Instalar plugins

El diálogo de plugins muestra dos pestañas: **Plugins** y **Marketplaces**.

En la pestaña Plugins:

* Los **plugins instalados** aparecen en la parte superior con interruptores de alternancia para habilitarlos o deshabilitarlos
* Los **plugins disponibles** de sus marketplaces configurados aparecen a continuación
* Busque para filtrar plugins por nombre o descripción
* Haga clic en **Instalar** en cualquier plugin disponible

Cuando instala un plugin, elija el alcance de instalación:

* **Instalar para usted**: disponible en todos sus proyectos (alcance de usuario)
* **Instalar para este proyecto**: compartido con colaboradores del proyecto (alcance del proyecto)
* **Instalar localmente**: solo para usted, solo en este repositorio (alcance local)

### Administrar marketplaces

Cambie a la pestaña **Marketplaces** para agregar o eliminar fuentes de plugins:

* Ingrese un repositorio de GitHub, URL o ruta local para agregar un nuevo marketplace
* Haga clic en el icono de actualización para actualizar la lista de plugins de un marketplace
* Haga clic en el icono de papelera para eliminar un marketplace

Después de realizar cambios, un banner le solicita que reinicie Claude Code para aplicar las actualizaciones.

<Note>
  La administración de plugins en VS Code utiliza los mismos comandos CLI bajo el capó. Los plugins y marketplaces que configura en la extensión también están disponibles en la CLI, y viceversa.
</Note>

Para más información sobre el sistema de plugins, consulte [Plugins](/es/plugins) y [Marketplaces de plugins](/es/plugin-marketplaces).

## Automatizar tareas del navegador con Chrome

Conecte Claude a su navegador Chrome para probar aplicaciones web, depurar con registros de consola y automatizar flujos de trabajo del navegador sin salir de VS Code. Esto requiere la [extensión Claude in Chrome](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) versión 1.0.36 o superior.

Escriba `@browser` en el cuadro de mensaje seguido de lo que desea que Claude haga:

```text  theme={null}
@browser go to localhost:3000 and check the console for errors
```

También puede abrir el menú de adjuntos para seleccionar herramientas específicas del navegador como abrir una nueva pestaña o leer contenido de la página.

Claude abre nuevas pestañas para tareas del navegador y comparte el estado de inicio de sesión de su navegador, por lo que puede acceder a cualquier sitio en el que ya haya iniciado sesión.

Para instrucciones de configuración, la lista completa de capacidades y solución de problemas, consulte [Usar Claude Code con Chrome](/es/chrome).

## Comandos y atajos de teclado de VS Code

Abra la Paleta de comandos (`Cmd+Shift+P` en Mac o `Ctrl+Shift+P` en Windows/Linux) y escriba "Claude Code" para ver todos los comandos de VS Code disponibles para la extensión Claude Code.

Algunos atajos de teclado dependen de qué panel esté "enfocado" (recibiendo entrada de teclado). Cuando su cursor está en un archivo de código, el editor está enfocado. Cuando su cursor está en el cuadro de mensaje de Claude, Claude está enfocado. Use `Cmd+Esc` / `Ctrl+Esc` para alternar entre ellos.

<Note>
  Estos son comandos de VS Code para controlar la extensión. No todos los comandos integrados de Claude Code están disponibles en la extensión. Consulte [Extensión de VS Code frente a CLI de Claude Code](#extensión-de-vs-code-frente-a-cli-de-claude-code) para obtener más detalles.
</Note>

| Comando                    | Atajo de teclado                                         | Descripción                                                                                  |
| -------------------------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Focus Input                | `Cmd+Esc` (Mac) / `Ctrl+Esc` (Windows/Linux)             | Alternar el enfoque entre el editor y Claude                                                 |
| Open in Side Bar           | -                                                        | Abrir Claude en la barra lateral izquierda                                                   |
| Open in Terminal           | -                                                        | Abrir Claude en modo terminal                                                                |
| Open in New Tab            | `Cmd+Shift+Esc` (Mac) / `Ctrl+Shift+Esc` (Windows/Linux) | Abrir una nueva conversación como una pestaña del editor                                     |
| Open in New Window         | -                                                        | Abrir una nueva conversación en una ventana separada                                         |
| New Conversation           | `Cmd+N` (Mac) / `Ctrl+N` (Windows/Linux)                 | Iniciar una nueva conversación (requiere que Claude esté enfocado)                           |
| Insert @-Mention Reference | `Option+K` (Mac) / `Alt+K` (Windows/Linux)               | Insertar una referencia al archivo actual y selección (requiere que el editor esté enfocado) |
| Show Logs                  | -                                                        | Ver registros de depuración de la extensión                                                  |
| Logout                     | -                                                        | Cerrar sesión de su cuenta de Anthropic                                                      |

## Configurar ajustes

La extensión tiene dos tipos de configuración:

* **Configuración de extensión** en VS Code: controla el comportamiento de la extensión dentro de VS Code. Abra con `Cmd+,` (Mac) o `Ctrl+,` (Windows/Linux), luego vaya a Extensiones → Claude Code. También puede escribir `/` y seleccionar **General Config** para abrir la configuración.
* **Configuración de Claude Code** en `~/.claude/settings.json`: compartida entre la extensión y la CLI. Use para comandos permitidos, variables de entorno, hooks y MCP servers. Consulte [Configuración](/es/settings) para obtener más detalles.

<Tip>
  Agregue `"$schema": "https://json.schemastore.org/claude-code-settings.json"` a su `settings.json` para obtener autocompletado y validación en línea para todos los ajustes disponibles directamente en VS Code.
</Tip>

### Configuración de extensión

| Configuración                     | Predeterminado | Descripción                                                                                                                               |
| --------------------------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `selectedModel`                   | `default`      | Modelo para nuevas conversaciones. Cambie por sesión con `/model`.                                                                        |
| `useTerminal`                     | `false`        | Lanzar Claude en modo terminal en lugar de panel gráfico                                                                                  |
| `initialPermissionMode`           | `default`      | Controla mensajes de aprobación: `default` (preguntar cada vez), `plan`, `acceptEdits` o `bypassPermissions`                              |
| `preferredLocation`               | `panel`        | Dónde se abre Claude: `sidebar` (derecha) o `panel` (nueva pestaña)                                                                       |
| `autosave`                        | `true`         | Guardar archivos automáticamente antes de que Claude los lea o escriba                                                                    |
| `useCtrlEnterToSend`              | `false`        | Usar Ctrl/Cmd+Enter en lugar de Enter para enviar mensajes                                                                                |
| `enableNewConversationShortcut`   | `true`         | Habilitar Cmd/Ctrl+N para iniciar una nueva conversación                                                                                  |
| `hideOnboarding`                  | `false`        | Ocultar la lista de verificación de incorporación (icono de gorro de graduación)                                                          |
| `respectGitIgnore`                | `true`         | Excluir patrones de .gitignore de búsquedas de archivos                                                                                   |
| `environmentVariables`            | `[]`           | Establecer variables de entorno para el proceso de Claude. Use la configuración de Claude Code en su lugar para configuración compartida. |
| `disableLoginPrompt`              | `false`        | Omitir mensajes de autenticación (para configuraciones de proveedores de terceros)                                                        |
| `allowDangerouslySkipPermissions` | `false`        | Omitir todos los mensajes de permiso. **Use con extrema precaución.**                                                                     |
| `claudeProcessWrapper`            | -              | Ruta ejecutable utilizada para lanzar el proceso de Claude                                                                                |

## Extensión de VS Code frente a CLI de Claude Code

Claude Code está disponible tanto como una extensión de VS Code (panel gráfico) como una CLI (interfaz de línea de comandos en la terminal). Algunas características solo están disponibles en la CLI. Si necesita una característica solo de CLI, ejecute `claude` en la terminal integrada de VS Code.

| Característica              | CLI                   | Extensión de VS Code                                                                                          |
| --------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------- |
| Comandos y skills           | [Todos](/es/commands) | Subconjunto (escriba `/` para ver disponibles)                                                                |
| Configuración de MCP server | Sí                    | Parcial (agregue servidores a través de CLI; administre servidores existentes con `/mcp` en el panel de chat) |
| Checkpoints                 | Sí                    | Sí                                                                                                            |
| Atajo bash `!`              | Sí                    | No                                                                                                            |
| Autocompletado de pestañas  | Sí                    | No                                                                                                            |

### Retroceder con checkpoints

La extensión de VS Code admite checkpoints, que rastrean las ediciones de archivos de Claude y le permiten retroceder a un estado anterior. Pase el cursor sobre cualquier mensaje para revelar el botón de retroceso, luego elija entre tres opciones:

* **Bifurcar conversación desde aquí**: iniciar una nueva rama de conversación desde este mensaje mientras mantiene todos los cambios de código intactos
* **Retroceder código a aquí**: revertir cambios de archivo a este punto en la conversación mientras mantiene el historial de conversación completo
* **Bifurcar conversación y retroceder código**: iniciar una nueva rama de conversación y revertir cambios de archivo a este punto

Para obtener detalles completos sobre cómo funcionan los checkpoints y sus limitaciones, consulte [Checkpointing](/es/checkpointing).

### Ejecutar CLI en VS Code

Para usar la CLI mientras permanece en VS Code, abra la terminal integrada (`` Ctrl+` `` en Windows/Linux o `` Cmd+` `` en Mac) y ejecute `claude`. La CLI se integra automáticamente con su IDE para características como visualización de diffs y uso compartido de diagnósticos.

Si usa una terminal externa, ejecute `/ide` dentro de Claude Code para conectarlo a VS Code.

### Cambiar entre extensión y CLI

La extensión y la CLI comparten el mismo historial de conversaciones. Para continuar una conversación de extensión en la CLI, ejecute `claude --resume` en la terminal. Esto abre un selector interactivo donde puede buscar y seleccionar su conversación.

### Incluir salida de terminal en mensajes

Haga referencia a la salida de terminal en sus mensajes usando `@terminal:name` donde `name` es el título de la terminal. Esto permite que Claude vea la salida del comando, mensajes de error o registros sin copiar y pegar.

### Monitorear procesos en segundo plano

Cuando Claude ejecuta comandos de larga duración, la extensión muestra el progreso en la barra de estado. Sin embargo, la visibilidad de tareas en segundo plano es limitada en comparación con la CLI. Para mejor visibilidad, haga que Claude genere el comando para que pueda ejecutarlo en la terminal integrada de VS Code.

### Conectar a herramientas externas con MCP

Los servidores MCP (Model Context Protocol) dan a Claude acceso a herramientas externas, bases de datos y APIs.

Para agregar un servidor MCP, abra la terminal integrada (`` Ctrl+` `` o `` Cmd+` ``) y ejecute:

```bash  theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

Una vez configurado, pida a Claude que use las herramientas (por ejemplo, "Review PR #456").

Para administrar servidores MCP sin salir de VS Code, escriba `/mcp` en el panel de chat. El diálogo de administración de MCP le permite habilitar o deshabilitar servidores, reconectarse a un servidor y administrar la autenticación OAuth. Consulte la [documentación de MCP](/es/mcp) para servidores disponibles.

## Trabajar con git

Claude Code se integra con git para ayudar con flujos de trabajo de control de versiones directamente en VS Code. Pida a Claude que confirme cambios, cree solicitudes de extracción o trabaje en diferentes ramas.

### Crear confirmaciones y solicitudes de extracción

Claude puede preparar cambios, escribir mensajes de confirmación y crear solicitudes de extracción basadas en su trabajo:

```text  theme={null}
> commit my changes with a descriptive message
> create a pr for this feature
> summarize the changes I've made to the auth module
```

Al crear solicitudes de extracción, Claude genera descripciones basadas en los cambios de código reales y puede agregar contexto sobre pruebas o decisiones de implementación.

### Usar git worktrees para tareas paralelas

Use la bandera `--worktree` (`-w`) para iniciar Claude en un worktree aislado con sus propios archivos y rama:

```bash  theme={null}
claude --worktree feature-auth
```

Cada worktree mantiene un estado de archivo independiente mientras comparte el historial de git. Esto evita que las instancias de Claude interfieran entre sí cuando trabajan en diferentes tareas. Para más detalles, consulte [Ejecutar sesiones paralelas de Claude Code con Git worktrees](/es/common-workflows#ejecutar-sesiones-paralelas-de-claude-code-con-git-worktrees).

## Usar proveedores de terceros

De forma predeterminada, Claude Code se conecta directamente a la API de Anthropic. Si su organización utiliza Amazon Bedrock, Google Vertex AI o Microsoft Foundry para acceder a Claude, configure la extensión para usar su proveedor en su lugar:

<Steps>
  <Step title="Deshabilitar mensaje de inicio de sesión">
    Abra la [configuración Deshabilitar mensaje de inicio de sesión](vscode://settings/claudeCode.disableLoginPrompt) y marque la casilla.

    También puede abrir la configuración de VS Code (`Cmd+,` en Mac o `Ctrl+,` en Windows/Linux), buscar "Claude Code login" y marcar **Deshabilitar mensaje de inicio de sesión**.
  </Step>

  <Step title="Configurar su proveedor">
    Siga la guía de configuración para su proveedor:

    * [Claude Code en Amazon Bedrock](/es/amazon-bedrock)
    * [Claude Code en Google Vertex AI](/es/google-vertex-ai)
    * [Claude Code en Microsoft Foundry](/es/microsoft-foundry)

    Estas guías cubren la configuración de su proveedor en `~/.claude/settings.json`, lo que garantiza que su configuración se comparta entre la extensión de VS Code y la CLI.
  </Step>
</Steps>

## Seguridad y privacidad

Su código permanece privado. Claude Code procesa su código para proporcionar asistencia pero no lo utiliza para entrenar modelos. Para obtener detalles sobre el manejo de datos y cómo optar por no participar en el registro, consulte [Datos y privacidad](/es/data-usage).

Con permisos de edición automática habilitados, Claude Code puede modificar archivos de configuración de VS Code (como `settings.json` o `tasks.json`) que VS Code puede ejecutar automáticamente. Para reducir el riesgo al trabajar con código no confiable:

* Habilite [Modo restringido de VS Code](https://code.visualstudio.com/docs/editor/workspace-trust#_restricted-mode) para espacios de trabajo no confiables
* Use el modo de aprobación manual en lugar de aceptación automática para ediciones
* Revise cuidadosamente los cambios antes de aceptarlos

## Solucionar problemas comunes

### La extensión no se instala

* Asegúrese de tener una versión compatible de VS Code (1.98.0 o posterior)
* Verifique que VS Code tenga permiso para instalar extensiones
* Intente instalar directamente desde [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)

### El icono Spark no es visible

El icono Spark aparece en la **Barra de herramientas del editor** (esquina superior derecha del editor) cuando tiene un archivo abierto. Si no lo ve:

1. **Abra un archivo**: El icono requiere que un archivo esté abierto. Solo tener una carpeta abierta no es suficiente.
2. **Verifique la versión de VS Code**: Requiere 1.98.0 o superior (Ayuda → Acerca de)
3. **Reinicie VS Code**: Ejecute "Developer: Reload Window" desde la Paleta de comandos
4. **Deshabilite extensiones conflictivas**: Deshabilite temporalmente otras extensiones de IA (Cline, Continue, etc.)
5. **Verifique la confianza del espacio de trabajo**: La extensión no funciona en Modo restringido

Alternativamente, haga clic en "✱ Claude Code" en la **Barra de estado** (esquina inferior derecha). Esto funciona incluso sin un archivo abierto. También puede usar la **Paleta de comandos** (`Cmd+Shift+P` / `Ctrl+Shift+P`) y escribir "Claude Code".

### Claude Code nunca responde

Si Claude Code no responde a sus mensajes:

1. **Verifique su conexión a Internet**: Asegúrese de tener una conexión a Internet estable
2. **Inicie una nueva conversación**: Intente iniciar una conversación nueva para ver si el problema persiste
3. **Intente la CLI**: Ejecute `claude` desde la terminal para ver si obtiene mensajes de error más detallados

Si los problemas persisten, [presente un problema en GitHub](https://github.com/anthropics/claude-code/issues) con detalles sobre el error.

## Desinstalar la extensión

Para desinstalar la extensión Claude Code:

1. Abra la vista Extensiones (`Cmd+Shift+X` en Mac o `Ctrl+Shift+X` en Windows/Linux)
2. Busque "Claude Code"
3. Haga clic en **Desinstalar**

Para también eliminar datos de extensión y restablecer toda la configuración:

```bash  theme={null}
rm -rf ~/.vscode/globalStorage/anthropic.claude-code
```

Para obtener ayuda adicional, consulte la [guía de solución de problemas](/es/troubleshooting).

## Próximos pasos

Ahora que tiene Claude Code configurado en VS Code:

* [Explore flujos de trabajo comunes](/es/common-workflows) para aprovechar al máximo Claude Code
* [Configure MCP servers](/es/mcp) para extender las capacidades de Claude con herramientas externas. Agregue servidores usando la CLI, luego adminístrelos con `/mcp` en el panel de chat.
* [Configure la configuración de Claude Code](/es/settings) para personalizar comandos permitidos, hooks y más. Esta configuración se comparte entre la extensión y la CLI.
