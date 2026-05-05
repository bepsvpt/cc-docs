> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Usar Claude Code en VS Code

> Instala y configura la extensión Claude Code para VS Code. Obtén asistencia de codificación con IA con diffs en línea, menciones @, revisión de planes y atajos de teclado.

<img src="https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=300652d5678c63905e6b0ea9e50835f8" alt="Editor de VS Code con el panel de extensión Claude Code abierto en el lado derecho, mostrando una conversación con Claude" width="2500" height="1155" data-path="images/vs-code-extension-interface.jpg" />

La extensión de VS Code proporciona una interfaz gráfica nativa para Claude Code, integrada directamente en tu IDE. Esta es la forma recomendada de usar Claude Code en VS Code.

Con la extensión, puedes revisar y editar los planes de Claude antes de aceptarlos, aceptar automáticamente ediciones a medida que se realizan, mencionar archivos con rangos de líneas específicas de tu selección, acceder al historial de conversaciones y abrir múltiples conversaciones en pestañas o ventanas separadas.

## Requisitos previos

Antes de instalar, asegúrate de tener:

* VS Code 1.98.0 o superior
* Una cuenta de Anthropic (iniciarás sesión cuando abras la extensión por primera vez). Si estás utilizando un proveedor de terceros como Amazon Bedrock o Google Vertex AI, consulta [Usar proveedores de terceros](#usar-proveedores-de-terceros) en su lugar.

<Tip>
  La extensión incluye la CLI (interfaz de línea de comandos), a la que puedes acceder desde la terminal integrada de VS Code para funciones avanzadas. Consulta [Extensión de VS Code frente a CLI de Claude Code](#extensión-de-vs-code-frente-a-cli-de-claude-code) para obtener más detalles.
</Tip>

## Instalar la extensión

Haz clic en el enlace de tu IDE para instalar directamente:

* [Instalar para VS Code](vscode:extension/anthropic.claude-code)
* [Instalar para Cursor](cursor:extension/anthropic.claude-code)

O en VS Code, presiona `Cmd+Shift+X` (Mac) o `Ctrl+Shift+X` (Windows/Linux) para abrir la vista Extensiones, busca "Claude Code" y haz clic en **Instalar**.

<Note>Si la extensión no aparece después de la instalación, reinicia VS Code o ejecuta "Developer: Reload Window" desde la Paleta de comandos.</Note>

## Comenzar

Una vez instalada, puedes comenzar a usar Claude Code a través de la interfaz de VS Code:

<Steps>
  <Step title="Abrir el panel de Claude Code">
    En todo VS Code, el icono Spark indica Claude Code: <img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/vs-code-spark-icon.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=3ca45e00deadec8c8f4b4f807da94505" alt="Icono Spark" style={{display: "inline", height: "0.85em", verticalAlign: "middle"}} width="16" height="16" data-path="images/vs-code-spark-icon.svg" />

    La forma más rápida de abrir Claude es hacer clic en el icono Spark en la **Barra de herramientas del editor** (esquina superior derecha del editor). El icono solo aparece cuando tienes un archivo abierto.

    <img src="https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=eb4540325d94664c51776dbbfec4cf02" alt="Editor de VS Code mostrando el icono Spark en la Barra de herramientas del editor" width="2796" height="734" data-path="images/vs-code-editor-icon.png" />

    Otras formas de abrir Claude Code:

    * **Barra de actividades**: haz clic en el icono Spark en la barra lateral izquierda para abrir la lista de sesiones. Haz clic en cualquier sesión para abrirla como una pestaña de editor completa, o inicia una nueva. Este icono siempre es visible en la Barra de actividades.
    * **Paleta de comandos**: `Cmd+Shift+P` (Mac) o `Ctrl+Shift+P` (Windows/Linux), escribe "Claude Code" y selecciona una opción como "Abrir en Nueva Pestaña"
    * **Barra de estado**: haz clic en **✱ Claude Code** en la esquina inferior derecha de la ventana. Esto funciona incluso cuando no hay ningún archivo abierto.

    Puedes arrastrar el panel de Claude para reposicionarlo en cualquier lugar de VS Code. Consulta [Personalizar tu flujo de trabajo](#personalizar-tu-flujo-de-trabajo) para obtener más detalles.
  </Step>

  <Step title="Iniciar sesión">
    La primera vez que abres el panel, aparece una pantalla de inicio de sesión. Haz clic en **Iniciar sesión** y completa la autorización en tu navegador.

    Si ves **No iniciado sesión · Por favor ejecuta /login** más tarde, la extensión reabre la pantalla de inicio de sesión automáticamente. Si no aparece, recarga la ventana desde la Paleta de comandos con **Developer: Reload Window**.

    Si tienes `ANTHROPIC_API_KEY` configurada en tu shell pero aún ves el mensaje de inicio de sesión, VS Code puede no haber heredado tu entorno de shell. Lanza VS Code desde una terminal con `code .` para que herede tus variables de entorno, o inicia sesión con tu cuenta de Claude en su lugar.

    Después de iniciar sesión, aparece una lista de verificación **Aprender Claude Code**. Trabaja en cada elemento haciendo clic en **Mostrarme**, o descártalo con la X. Para reabrirlo más tarde, desmarque **Ocultar incorporación** en la configuración de VS Code en Extensiones → Claude Code.
  </Step>

  <Step title="Enviar un mensaje">
    Pide a Claude que te ayude con tu código o archivos, ya sea explicando cómo funciona algo, depurando un problema o realizando cambios.

    <Tip>Claude ve automáticamente tu texto seleccionado. Presiona `Option+K` (Mac) / `Alt+K` (Windows/Linux) para también insertar una referencia de mención @ (como `@file.ts#5-10`) en tu mensaje.</Tip>

    Aquí hay un ejemplo de cómo hacer una pregunta sobre una línea particular en un archivo:

    <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-send-prompt.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=ede3ed8d8d5f940e01c5de636d009cfd" alt="Editor de VS Code con las líneas 2-3 seleccionadas en un archivo Python, y el panel de Claude Code mostrando una pregunta sobre esas líneas con una referencia de mención @" width="3288" height="1876" data-path="images/vs-code-send-prompt.png" />
  </Step>

  <Step title="Revisar cambios">
    Cuando Claude quiere editar un archivo, muestra una comparación lado a lado del original y los cambios propuestos, luego solicita permiso. Puedes aceptar, rechazar o decirle a Claude qué hacer en su lugar. Si editas el contenido propuesto directamente en la vista de diff antes de aceptar, Claude es informado de que lo modificaste para que no asuma que el archivo coincide con su propuesta original.

    <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-edits.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=e005f9b41c541c5c7c59c082f7c4841c" alt="VS Code mostrando un diff de los cambios propuestos por Claude con un mensaje de permiso preguntando si realizar la edición" width="3292" height="1876" data-path="images/vs-code-edits.png" />
  </Step>
</Steps>

Para más ideas sobre lo que puedes hacer con Claude Code, consulta [Flujos de trabajo comunes](/es/common-workflows).

<Tip>
  Ejecuta "Claude Code: Open Walkthrough" desde la Paleta de comandos para un tour guiado de los conceptos básicos.
</Tip>

## Usar el cuadro de mensaje

El cuadro de mensaje admite varias características:

* **Modos de permiso**: haz clic en el indicador de modo en la parte inferior del cuadro de mensaje para cambiar de modo. En modo normal, Claude solicita permiso antes de cada acción. En Plan Mode, Claude describe lo que hará y espera aprobación antes de realizar cambios. VS Code abre automáticamente el plan como un documento markdown completo donde puedes agregar comentarios en línea para dar retroalimentación antes de que Claude comience. En modo de aceptación automática, Claude realiza ediciones sin preguntar. Establece el valor predeterminado en la configuración de VS Code en `claudeCode.initialPermissionMode`.
* **Menú de comandos**: haz clic en `/` o escribe `/` para abrir el menú de comandos. Las opciones incluyen adjuntar archivos, cambiar modelos, alternar pensamiento extendido, ver uso del plan (`/usage`) e iniciar una sesión de [Control remoto](/es/remote-control) (`/remote-control`). La sección Personalizar proporciona acceso a MCP servers, hooks, memoria, permisos y plugins. Los elementos con un icono de terminal se abren en la terminal integrada.
* **Indicador de contexto**: el cuadro de mensaje muestra cuánto de la ventana de contexto de Claude estás utilizando. Claude se compacta automáticamente cuando es necesario, o puedes ejecutar `/compact` manualmente.
* **Pensamiento extendido**: permite que Claude dedique más tiempo a razonar sobre problemas complejos. Actívalo a través del menú de comandos (`/`). El razonamiento de Claude aparece en la conversación como bloques contraídos: haz clic en un bloque para leerlo, o presiona `Ctrl+O` para expandir o contraer cada bloque de pensamiento en la sesión. Consulta [Pensamiento extendido](/es/model-config#extended-thinking) para obtener más detalles.
* **Entrada multilínea**: presiona `Shift+Enter` para agregar una nueva línea sin enviar. Esto también funciona en la entrada de texto libre "Otro" de los diálogos de preguntas.

### Referenciar archivos y carpetas

Usa menciones @ para dar a Claude contexto sobre archivos o carpetas específicas. Cuando escribes `@` seguido de un nombre de archivo o carpeta, Claude lee ese contenido y puede responder preguntas sobre él o realizar cambios en él. Claude Code admite coincidencia difusa, por lo que puedes escribir nombres parciales para encontrar lo que necesitas:

```text theme={null}
> Explain the logic in @auth (fuzzy matches auth.js, AuthService.ts, etc.)
> What's in @src/components/ (include a trailing slash for folders)
```

Para archivos PDF grandes, puedes pedirle a Claude que lea páginas específicas en lugar del archivo completo: una sola página, un rango como páginas 1-10, o un rango abierto como página 3 en adelante.

Cuando seleccionas texto en el editor, Claude puede ver tu código resaltado automáticamente. El pie de página del cuadro de mensaje muestra cuántas líneas están seleccionadas. Presiona `Option+K` (Mac) / `Alt+K` (Windows/Linux) para insertar una mención @ con la ruta del archivo y los números de línea (por ejemplo, `@app.ts#5-10`). Haz clic en el indicador de selección para alternar si Claude puede ver tu texto resaltado: el icono de barra diagonal significa que la selección está oculta para Claude.

También puedes mantener presionado `Shift` mientras arrastras archivos al cuadro de mensaje para agregarlos como adjuntos. Haz clic en la X en cualquier adjunto para eliminarlo del contexto.

### Reanudar conversaciones pasadas

Haz clic en el botón **Historial de sesiones** en la parte superior del panel de Claude Code para acceder a tu historial de conversaciones. Puedes buscar por palabra clave o examinar por tiempo (Hoy, Ayer, Últimos 7 días, etc.). Haz clic en cualquier conversación para reanudarla con el historial de mensajes completo. Las nuevas sesiones reciben títulos generados por IA basados en tu primer mensaje. Pasa el cursor sobre una sesión para revelar acciones de cambio de nombre y eliminación: cambia el nombre para darle un título descriptivo, o elimina para borrarlo de la lista. Para más información sobre cómo reanudar sesiones, consulta [Administrar sesiones](/es/sessions).

### Reanudar sesiones remotas desde Claude.ai

Si utilizas [Claude Code en la web](/es/claude-code-on-the-web), puedes reanudar esas sesiones remotas directamente en VS Code. Esto requiere iniciar sesión con **Claude.ai Subscription**, no Anthropic Console.

<Steps>
  <Step title="Abrir historial de sesiones">
    Haz clic en el botón **Historial de sesiones** en la parte superior del panel de Claude Code.
  </Step>

  <Step title="Seleccionar la pestaña Remoto">
    El diálogo muestra dos pestañas: Local y Remoto. Haz clic en **Remoto** para ver sesiones desde claude.ai.
  </Step>

  <Step title="Seleccionar una sesión para reanudar">
    Examina o busca tus sesiones remotas. Haz clic en cualquier sesión para descargarla y continuar la conversación localmente.
  </Step>
</Steps>

<Note>
  Solo las sesiones web iniciadas con un repositorio de GitHub aparecen en la pestaña Remoto. Reanudar carga el historial de conversaciones localmente; los cambios no se sincronizan de vuelta a claude.ai.
</Note>

## Personalizar tu flujo de trabajo

Una vez que estés en funcionamiento, puedes reposicionar el panel de Claude, ejecutar múltiples sesiones o cambiar al modo terminal.

### Elegir dónde vive Claude

Puedes arrastrar el panel de Claude para reposicionarlo en cualquier lugar de VS Code. Agarra la pestaña o barra de título del panel y arrástralo a:

* **Barra lateral secundaria**: el lado derecho de la ventana. Mantiene a Claude visible mientras codificas.
* **Barra lateral principal**: la barra lateral izquierda con iconos para Explorador, Búsqueda, etc.
* **Área del editor**: abre Claude como una pestaña junto a tus archivos. Útil para tareas secundarias.

<Tip>
  Usa la barra lateral para tu sesión principal de Claude y abre pestañas adicionales para tareas secundarias. Claude recuerda tu ubicación preferida. El icono de lista de sesiones de la Barra de actividades es separado del panel de Claude: la lista de sesiones siempre es visible en la Barra de actividades, mientras que el icono del panel de Claude solo aparece allí cuando el panel está acoplado a la barra lateral izquierda.
</Tip>

### Ejecutar múltiples conversaciones

Usa **Abrir en Nueva Pestaña** u **Abrir en Nueva Ventana** desde la Paleta de comandos para iniciar conversaciones adicionales. Cada conversación mantiene su propio historial y contexto, permitiéndote trabajar en diferentes tareas en paralelo.

Cuando usas pestañas, un pequeño punto de color en el icono spark indica el estado: azul significa que hay una solicitud de permiso pendiente, naranja significa que Claude terminó mientras la pestaña estaba oculta.

### Cambiar al modo terminal

De forma predeterminada, la extensión abre un panel de chat gráfico. Si prefieres la interfaz de estilo CLI, abre la [configuración Usar terminal](vscode://settings/claudeCode.useTerminal) y marca la casilla.

También puedes abrir la configuración de VS Code (`Cmd+,` en Mac o `Ctrl+,` en Windows/Linux), ir a Extensiones → Claude Code y marcar **Usar terminal**.

## Administrar plugins

La extensión de VS Code incluye una interfaz gráfica para instalar y administrar [plugins](/es/plugins). Escribe `/plugins` en el cuadro de mensaje para abrir la interfaz **Administrar plugins**.

### Instalar plugins

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

### Administrar marketplaces

Cambia a la pestaña **Marketplaces** para agregar o eliminar fuentes de plugins:

* Ingresa un repositorio de GitHub, URL o ruta local para agregar un nuevo marketplace
* Haz clic en el icono de actualización para actualizar la lista de plugins de un marketplace
* Haz clic en el icono de papelera para eliminar un marketplace

Después de realizar cambios, un banner te solicita que reinicies Claude Code para aplicar las actualizaciones.

<Note>
  La administración de plugins en VS Code utiliza los mismos comandos CLI bajo el capó. Los plugins y marketplaces que configuras en la extensión también están disponibles en la CLI, y viceversa.
</Note>

Para más información sobre el sistema de plugins, consulta [Plugins](/es/plugins) y [Marketplaces de plugins](/es/plugin-marketplaces).

## Automatizar tareas del navegador con Chrome

Conecta Claude a tu navegador Chrome para probar aplicaciones web, depurar con registros de consola y automatizar flujos de trabajo del navegador sin salir de VS Code. Esto requiere la [extensión Claude in Chrome](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) versión 1.0.36 o superior.

Escribe `@browser` en el cuadro de mensaje seguido de lo que deseas que Claude haga:

```text theme={null}
@browser go to localhost:3000 and check the console for errors
```

También puedes abrir el menú de adjuntos para seleccionar herramientas específicas del navegador como abrir una nueva pestaña o leer contenido de la página.

Claude abre nuevas pestañas para tareas del navegador y comparte el estado de inicio de sesión de tu navegador, por lo que puedes acceder a cualquier sitio en el que ya hayas iniciado sesión.

Para instrucciones de configuración, la lista completa de capacidades y solución de problemas, consulta [Usar Claude Code con Chrome](/es/chrome).

## Comandos y atajos de teclado de VS Code

Abre la Paleta de comandos (`Cmd+Shift+P` en Mac o `Ctrl+Shift+P` en Windows/Linux) y escribe "Claude Code" para ver todos los comandos de VS Code disponibles para la extensión Claude Code.

Algunos atajos de teclado dependen de qué panel esté "enfocado" (recibiendo entrada de teclado). Cuando tu cursor está en un archivo de código, el editor está enfocado. Cuando tu cursor está en el cuadro de mensaje de Claude, Claude está enfocado. Usa `Cmd+Esc` / `Ctrl+Esc` para alternar entre ellos.

<Note>
  Estos son comandos de VS Code para controlar la extensión. No todos los comandos integrados de Claude Code están disponibles en la extensión. Consulta [Extensión de VS Code frente a CLI de Claude Code](#extensión-de-vs-code-frente-a-cli-de-claude-code) para obtener más detalles.
</Note>

| Comando                    | Atajo de teclado                                         | Descripción                                                                                                               |
| -------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Focus Input                | `Cmd+Esc` (Mac) / `Ctrl+Esc` (Windows/Linux)             | Alternar el enfoque entre el editor y Claude                                                                              |
| Open in Side Bar           | -                                                        | Abrir Claude en la barra lateral izquierda                                                                                |
| Open in Terminal           | -                                                        | Abrir Claude en modo terminal                                                                                             |
| Open in New Tab            | `Cmd+Shift+Esc` (Mac) / `Ctrl+Shift+Esc` (Windows/Linux) | Abrir una nueva conversación como una pestaña del editor                                                                  |
| Open in New Window         | -                                                        | Abrir una nueva conversación en una ventana separada                                                                      |
| New Conversation           | `Cmd+N` (Mac) / `Ctrl+N` (Windows/Linux)                 | Iniciar una nueva conversación. Requiere que Claude esté enfocado y `enableNewConversationShortcut` establecido en `true` |
| Insert @-Mention Reference | `Option+K` (Mac) / `Alt+K` (Windows/Linux)               | Insertar una referencia al archivo actual y selección (requiere que el editor esté enfocado)                              |
| Show Logs                  | -                                                        | Ver registros de depuración de la extensión                                                                               |
| Logout                     | -                                                        | Cerrar sesión de tu cuenta de Anthropic                                                                                   |

### Lanzar una pestaña de VS Code desde otras herramientas

La extensión registra un controlador URI en `vscode://anthropic.claude-code/open`. Úsalo para abrir una nueva pestaña de Claude Code desde tu propia herramienta: un alias de shell, un marcador de navegador, o cualquier script que pueda abrir una URL. Si VS Code no está ejecutándose, abrir la URL lo lanza primero. Si VS Code ya está ejecutándose, la URL se abre en la ventana que está actualmente enfocada.

Invoca el controlador con el abridor de URL de tu sistema operativo.

<Tabs>
  <Tab title="macOS">
    ```bash theme={null}
    open "vscode://anthropic.claude-code/open"
    ```
  </Tab>

  <Tab title="Linux">
    ```bash theme={null}
    xdg-open "vscode://anthropic.claude-code/open"
    ```
  </Tab>

  <Tab title="Windows">
    En PowerShell:

    ```powershell theme={null}
    Start-Process "vscode://anthropic.claude-code/open"
    ```

    En `cmd.exe`, `start` trata su primer argumento entrecomillado como un título de ventana, así que pasa un título vacío antes de la URL:

    ```cmd theme={null}
    start "" "vscode://anthropic.claude-code/open"
    ```
  </Tab>
</Tabs>

El controlador acepta dos parámetros de consulta opcionales:

| Parámetro | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                  |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prompt`  | Texto para rellenar previamente en el cuadro de mensaje. Debe estar codificado en URL. El mensaje se rellena previamente pero no se envía automáticamente.                                                                                                                                                                                                                                                                   |
| `session` | Un ID de sesión para reanudar en lugar de iniciar una nueva conversación. La sesión debe pertenecer al espacio de trabajo actualmente abierto en VS Code. Si la sesión no se encuentra, se inicia una conversación nueva. Si la sesión ya está abierta en una pestaña, esa pestaña se enfoca. Para capturar un ID de sesión mediante programación, consulta [Continuar conversaciones](/es/headless#continue-conversations). |

Por ejemplo, para abrir una pestaña rellenada previamente con "review my changes":

```text theme={null}
vscode://anthropic.claude-code/open?prompt=review%20my%20changes
```

Para lanzar una sesión de terminal en lugar de una pestaña de VS Code, usa el controlador `claude-cli://` de la CLI. Consulta [Lanzar sesiones desde enlaces](/es/deep-links).

## Configurar ajustes

La extensión tiene dos tipos de configuración:

* **Configuración de extensión** en VS Code: controla el comportamiento de la extensión dentro de VS Code. Abre con `Cmd+,` (Mac) o `Ctrl+,` (Windows/Linux), luego ve a Extensiones → Claude Code. También puedes escribir `/` y seleccionar **General Config** para abrir la configuración.
* **Configuración de Claude Code** en `~/.claude/settings.json`: compartida entre la extensión y la CLI. Usa para comandos permitidos, variables de entorno, hooks y MCP servers. Consulta [Configuración](/es/settings) para obtener más detalles.

<Tip>
  Agrega `"$schema": "https://json.schemastore.org/claude-code-settings.json"` a tu `settings.json` para obtener autocompletado y validación en línea para todos los ajustes disponibles directamente en VS Code.
</Tip>

### Configuración de extensión

| Configuración                     | Predeterminado | Descripción                                                                                                                                                                                                                                                                                                                                                                               |
| --------------------------------- | -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `useTerminal`                     | `false`        | Lanzar Claude en modo terminal en lugar de panel gráfico                                                                                                                                                                                                                                                                                                                                  |
| `initialPermissionMode`           | `default`      | Controla mensajes de aprobación para nuevas conversaciones: `default`, `plan`, `acceptEdits`, o `bypassPermissions`. Consulta [modos de permiso](/es/permission-modes).                                                                                                                                                                                                                   |
| `preferredLocation`               | `panel`        | Dónde se abre Claude: `sidebar` (derecha) o `panel` (nueva pestaña)                                                                                                                                                                                                                                                                                                                       |
| `autosave`                        | `true`         | Guardar archivos automáticamente antes de que Claude los lea o escriba                                                                                                                                                                                                                                                                                                                    |
| `useCtrlEnterToSend`              | `false`        | Usar Ctrl/Cmd+Enter en lugar de Enter para enviar mensajes                                                                                                                                                                                                                                                                                                                                |
| `enableNewConversationShortcut`   | `false`        | Habilitar Cmd/Ctrl+N para iniciar una nueva conversación                                                                                                                                                                                                                                                                                                                                  |
| `hideOnboarding`                  | `false`        | Ocultar la lista de verificación de incorporación (icono de gorro de graduación)                                                                                                                                                                                                                                                                                                          |
| `respectGitIgnore`                | `true`         | Excluir patrones de .gitignore de búsquedas de archivos                                                                                                                                                                                                                                                                                                                                   |
| `usePythonEnvironment`            | `true`         | Activar el entorno de Python del espacio de trabajo cuando se ejecuta Claude. Requiere la extensión de Python.                                                                                                                                                                                                                                                                            |
| `environmentVariables`            | `[]`           | Establecer variables de entorno para el proceso de Claude. Usa la configuración de Claude Code en su lugar para configuración compartida.                                                                                                                                                                                                                                                 |
| `disableLoginPrompt`              | `false`        | Omitir mensajes de autenticación (para configuraciones de proveedores de terceros)                                                                                                                                                                                                                                                                                                        |
| `allowDangerouslySkipPermissions` | `false`        | Agrega [Modo Auto](/es/permission-modes#eliminate-prompts-with-auto-mode) y Bypass permissions a la selector de modo. Auto mode tiene [requisitos de plan, admin, modelo y proveedor](/es/permission-modes#eliminate-prompts-with-auto-mode), por lo que puede permanecer no disponible incluso con este toggle activado. Usa Bypass permissions solo en sandboxes sin acceso a Internet. |
| `claudeProcessWrapper`            | -              | Ruta ejecutable utilizada para lanzar el proceso de Claude                                                                                                                                                                                                                                                                                                                                |

## Extensión de VS Code frente a CLI de Claude Code

Claude Code está disponible tanto como una extensión de VS Code (panel gráfico) como una CLI (interfaz de línea de comandos en la terminal). Algunas características solo están disponibles en la CLI. Si necesitas una característica solo de CLI, ejecuta `claude` en la terminal integrada de VS Code.

| Característica              | CLI                   | Extensión de VS Code                                                                                         |
| --------------------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ |
| Comandos y skills           | [Todos](/es/commands) | Subconjunto (escribe `/` para ver disponibles)                                                               |
| Configuración de MCP server | Sí                    | Parcial (agrega servidores a través de CLI; administra servidores existentes con `/mcp` en el panel de chat) |
| Checkpoints                 | Sí                    | Sí                                                                                                           |
| Atajo bash `!`              | Sí                    | No                                                                                                           |
| Autocompletado de pestañas  | Sí                    | No                                                                                                           |

### Retroceder con checkpoints

La extensión de VS Code admite checkpoints, que rastrean las ediciones de archivos de Claude y te permiten retroceder a un estado anterior. Pasa el cursor sobre cualquier mensaje para revelar el botón de retroceso, luego elige entre tres opciones:

* **Bifurcar conversación desde aquí**: iniciar una nueva rama de conversación desde este mensaje mientras mantienes todos los cambios de código intactos
* **Retroceder código a aquí**: revertir cambios de archivo a este punto en la conversación mientras mantienes el historial de conversación completo
* **Bifurcar conversación y retroceder código**: iniciar una nueva rama de conversación y revertir cambios de archivo a este punto

Para obtener detalles completos sobre cómo funcionan los checkpoints y sus limitaciones, consulta [Checkpointing](/es/checkpointing).

### Ejecutar CLI en VS Code

Para usar la CLI mientras permaneces en VS Code, abre la terminal integrada (`` Ctrl+` `` en Windows/Linux o `` Cmd+` `` en Mac) y ejecuta `claude`. La CLI se integra automáticamente con tu IDE para características como visualización de diffs y uso compartido de diagnósticos.

Si usas una terminal externa, ejecuta `/ide` dentro de Claude Code para conectarlo a VS Code.

### Cambiar entre extensión y CLI

La extensión y la CLI comparten el mismo historial de conversaciones. Para continuar una conversación de extensión en la CLI, ejecuta `claude --resume` en la terminal. Esto abre un selector interactivo donde puedes buscar y seleccionar tu conversación.

### Incluir salida de terminal en mensajes

Haz referencia a la salida de terminal en tus mensajes usando `@terminal:name` donde `name` es el título de la terminal. Esto permite que Claude vea la salida del comando, mensajes de error o registros sin copiar y pegar.

### Monitorear procesos en segundo plano

Cuando Claude ejecuta comandos de larga duración, la extensión muestra el progreso en la barra de estado. Sin embargo, la visibilidad de tareas en segundo plano es limitada en comparación con la CLI. Para mejor visibilidad, haz que Claude genere el comando para que puedas ejecutarlo en la terminal integrada de VS Code.

### Conectar a herramientas externas con MCP

Los servidores MCP (Model Context Protocol) dan a Claude acceso a herramientas externas, bases de datos y APIs.

Para agregar un servidor MCP, abre la terminal integrada (`` Ctrl+` `` o `` Cmd+` ``) y ejecuta `claude mcp add`. El ejemplo a continuación agrega el servidor MCP remoto de GitHub, que se autentica con un [token de acceso personal](https://github.com/settings/personal-access-tokens) pasado como encabezado:

```bash theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
  --header "Authorization: Bearer YOUR_GITHUB_PAT"
```

Una vez configurado, pide a Claude que use las herramientas (por ejemplo, "Review PR #456").

Para administrar servidores MCP sin salir de VS Code, escribe `/mcp` en el panel de chat. El diálogo de administración de MCP te permite habilitar o deshabilitar servidores, reconectarse a un servidor y administrar la autenticación OAuth. Consulta la [documentación de MCP](/es/mcp) para servidores disponibles.

## Trabajar con git

Claude Code se integra con git para ayudarte con flujos de trabajo de control de versiones directamente en VS Code. Pide a Claude que confirme cambios, cree solicitudes de extracción o trabaje en diferentes ramas.

### Crear confirmaciones y solicitudes de extracción

Claude puede preparar cambios, escribir mensajes de confirmación y crear solicitudes de extracción basadas en tu trabajo:

```text theme={null}
> commit my changes with a descriptive message
> create a pr for this feature
> summarize the changes I've made to the auth module
```

Al crear solicitudes de extracción, Claude genera descripciones basadas en los cambios de código reales y puede agregar contexto sobre pruebas o decisiones de implementación.

### Usar git worktrees para tareas paralelas

Usa la bandera `--worktree` (`-w`) para iniciar Claude en un worktree aislado con sus propios archivos y rama:

```bash theme={null}
claude --worktree feature-auth
```

Cada worktree mantiene un estado de archivo independiente mientras comparte el historial de git. Esto evita que las instancias de Claude interfieran entre sí cuando trabajan en diferentes tareas. Para más detalles, consulta [Ejecutar sesiones paralelas con Git worktrees](/es/worktrees).

## Usar proveedores de terceros

De forma predeterminada, Claude Code se conecta directamente a la API de Anthropic. Si tu organización utiliza Amazon Bedrock, Google Vertex AI o Microsoft Foundry para acceder a Claude, configura la extensión para usar tu proveedor en su lugar:

<Steps>
  <Step title="Deshabilitar mensaje de inicio de sesión">
    Abre la [configuración Deshabilitar mensaje de inicio de sesión](vscode://settings/claudeCode.disableLoginPrompt) y marca la casilla.

    También puedes abrir la configuración de VS Code (`Cmd+,` en Mac o `Ctrl+,` en Windows/Linux), buscar "Claude Code login" y marcar **Deshabilitar mensaje de inicio de sesión**.
  </Step>

  <Step title="Configurar tu proveedor">
    Sigue la guía de configuración para tu proveedor:

    * [Claude Code en Amazon Bedrock](/es/amazon-bedrock)
    * [Claude Code en Google Vertex AI](/es/google-vertex-ai)
    * [Claude Code en Microsoft Foundry](/es/microsoft-foundry)

    Estas guías cubren la configuración de tu proveedor en `~/.claude/settings.json`, lo que garantiza que tu configuración se comparta entre la extensión de VS Code y la CLI.
  </Step>
</Steps>

## Seguridad y privacidad

Tu código permanece privado. Claude Code procesa tu código para proporcionar asistencia pero no lo utiliza para entrenar modelos. Para obtener detalles sobre el manejo de datos y cómo optar por no participar en el registro, consulta [Datos y privacidad](/es/data-usage).

Con permisos de edición automática habilitados, Claude Code puede modificar archivos de configuración de VS Code (como `settings.json` o `tasks.json`) que VS Code puede ejecutar automáticamente. Para reducir el riesgo al trabajar con código no confiable:

* Habilita [Modo restringido de VS Code](https://code.visualstudio.com/docs/editor/workspace-trust#_restricted-mode) para espacios de trabajo no confiables
* Usa el modo de aprobación manual en lugar de aceptación automática para ediciones
* Revisa cuidadosamente los cambios antes de aceptarlos

### El servidor MCP IDE integrado

Cuando la extensión está activa, ejecuta un servidor MCP local al que la CLI se conecta automáticamente. Así es como la CLI abre diffs en el visor de diffs nativo de VS Code, lee tu selección actual para menciones `@` y, cuando estás trabajando en un notebook de Jupyter, le pide a VS Code que ejecute celdas.

El servidor se llama `ide` y está oculto de `/mcp` porque no hay nada que configurar. Sin embargo, si tu organización utiliza un hook `PreToolUse` para permitir herramientas MCP, necesitarás saber que existe.

**Transporte y autenticación.** El servidor se vincula a `127.0.0.1` en un puerto alto aleatorio y no es accesible desde otras máquinas. Cada activación de extensión genera un token de autenticación aleatorio nuevo que la CLI debe presentar para conectarse. El token se escribe en un archivo de bloqueo bajo `~/.claude/ide/` con permisos `0600` en un directorio `0700`, por lo que solo el usuario que ejecuta VS Code puede leerlo.

**Herramientas expuestas al modelo.** El servidor aloja una docena de herramientas, pero solo dos son visibles para el modelo. El resto son RPC internas que la CLI usa para su propia interfaz de usuario (abrir diffs, leer selecciones, guardar archivos) y se filtran antes de que la lista de herramientas llegue a Claude.

| Nombre de herramienta (como se ve en hooks) | Qué hace                                                                                                                                          | ¿Escribe? |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| `mcp__ide__getDiagnostics`                  | Devuelve diagnósticos del servidor de lenguaje: los errores y advertencias en el panel Problemas de VS Code. Opcionalmente limitado a un archivo. | No        |
| `mcp__ide__executeCode`                     | Ejecuta código Python en el kernel del notebook de Jupyter activo. Consulta el flujo de confirmación a continuación.                              | Sí        |

**La ejecución de Jupyter siempre pregunta primero.** `mcp__ide__executeCode` no puede ejecutar nada silenciosamente. En cada llamada, el código se inserta como una nueva celda al final del notebook activo, VS Code lo desplaza a la vista y una Quick Pick nativa te pregunta si **Ejecutar** o **Cancelar**. Cancelar (o descartar la selección con `Esc`) devuelve un error a Claude y nada se ejecuta. La herramienta también se niega rotundamente cuando no hay un notebook activo, cuando la extensión de Jupyter (`ms-toolsai.jupyter`) no está instalada, o cuando el kernel no es Python.

<Note>
  La confirmación de Quick Pick es separada de los hooks `PreToolUse`. Una entrada de lista de permitidos para `mcp__ide__executeCode` permite que Claude *proponga* ejecutar una celda; la Quick Pick dentro de VS Code es lo que permite que *realmente* se ejecute.
</Note>

<a id="troubleshooting" />

## Solucionar problemas comunes

### La extensión no se instala

* Asegúrate de tener una versión compatible de VS Code (1.98.0 o posterior)
* Verifica que VS Code tenga permiso para instalar extensiones
* Intenta instalar directamente desde [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)

### El icono Spark no es visible

El icono Spark aparece en la **Barra de herramientas del editor** (esquina superior derecha del editor) cuando tienes un archivo abierto. Si no lo ves:

1. **Abre un archivo**: El icono requiere que un archivo esté abierto. Solo tener una carpeta abierta no es suficiente.
2. **Verifica la versión de VS Code**: Requiere 1.98.0 o superior (Ayuda → Acerca de)
3. **Reinicia VS Code**: Ejecuta "Developer: Reload Window" desde la Paleta de comandos
4. **Deshabilita extensiones conflictivas**: Deshabilita temporalmente otras extensiones de IA (Cline, Continue, etc.)
5. **Verifica la confianza del espacio de trabajo**: La extensión no funciona en Modo restringido

Alternativamente, haz clic en "✱ Claude Code" en la **Barra de estado** (esquina inferior derecha). Esto funciona incluso sin un archivo abierto. También puedes usar la **Paleta de comandos** (`Cmd+Shift+P` / `Ctrl+Shift+P`) y escribir "Claude Code".

### Cmd+Esc no hace nada en macOS

En macOS Tahoe y posterior, el atajo del sistema Game Overlay está vinculado a `Cmd+Esc` de forma predeterminada e intercepta la pulsación de tecla antes de que llegue a VS Code. Para liberar el atajo:

1. Abre Configuración del sistema
2. Ve a Teclado, luego Atajos de teclado, luego Controladores de juegos
3. Desactiva la casilla de verificación Game Overlay

Alternativamente, vuelve a vincular la extensión a una tecla diferente: abre el editor de [Atajos de teclado](https://code.visualstudio.com/docs/configure/keybindings) de VS Code (`Cmd+K Cmd+S`), busca `Claude Code: Focus input`, y asigna un nuevo atajo.

### Claude Code nunca responde

Si Claude Code no responde a tus mensajes:

1. **Verifica tu conexión a Internet**: Asegúrate de tener una conexión a Internet estable
2. **Inicia una nueva conversación**: Intenta iniciar una conversación nueva para ver si el problema persiste
3. **Intenta la CLI**: Ejecuta `claude` desde la terminal para ver si obtienes mensajes de error más detallados

Si los problemas persisten, [presenta un problema en GitHub](https://github.com/anthropics/claude-code/issues) con detalles sobre el error.

## Desinstalar la extensión

Para desinstalar la extensión Claude Code:

1. Abre la vista Extensiones (`Cmd+Shift+X` en Mac o `Ctrl+Shift+X` en Windows/Linux)
2. Busca "Claude Code"
3. Haz clic en **Desinstalar**

Para también eliminar datos de extensión y restablecer toda la configuración:

```bash theme={null}
rm -rf ~/.vscode/globalStorage/anthropic.claude-code
```

Para obtener ayuda adicional, consulta la [guía de solución de problemas](/es/troubleshooting).

## Próximos pasos

Ahora que tienes Claude Code configurado en VS Code:

* [Explora flujos de trabajo comunes](/es/common-workflows) para aprovechar al máximo Claude Code
* [Configura MCP servers](/es/mcp) para extender las capacidades de Claude con herramientas externas. Agrega servidores usando la CLI, luego adminístralos con `/mcp` en el panel de chat.
* [Configura la configuración de Claude Code](/es/settings) para personalizar comandos permitidos, hooks y más. Esta configuración se comparte entre la extensión y la CLI.
