> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Usar Claude Code Desktop

> Aproveche al máximo Claude Code Desktop: sesiones paralelas con aislamiento de Git, diseño de panel de arrastrar y soltar, terminal integrada y editor de archivos, chats laterales, uso de computadora, envíe sesiones desde su teléfono, revisión visual de diferencias, vistas previas de aplicaciones, monitoreo de PR, conectores y configuración empresarial.

La pestaña Code dentro de la aplicación Claude Desktop le permite usar Claude Code a través de una interfaz gráfica en lugar de la terminal.

<CardGroup cols={2}>
  <Card title="Download for macOS" icon="apple" href="https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs">
    Universal build for Intel and Apple Silicon
  </Card>

  <Card title="Download for Windows" icon="windows" href="https://claude.ai/api/desktop/win32/x64/setup/latest/redirect?utm_source=claude_code&utm_medium=docs">
    For x64 processors
  </Card>
</CardGroup>

For Windows ARM64, download the [ARM64 installer](https://claude.ai/api/desktop/win32/arm64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs). Linux is not supported.

Después de instalar, inicie Claude, inicie sesión y haga clic en la pestaña **Code**. Consulte la [guía de introducción](/es/desktop-quickstart) para obtener un recorrido completo de su primera sesión.

Desktop añade estas capacidades además de la experiencia estándar de Claude Code:

* [Sesiones paralelas](#work-in-parallel-with-sessions) con aislamiento automático de Git worktree
* [Diseño de arrastrar y soltar](#arrange-your-workspace) con terminal integrada, editor de archivos y panel de vista previa
* [Chats laterales](#ask-a-side-question-without-derailing-the-session) que se ramifican sin afectar el hilo principal
* [Revisión visual de diferencias](#review-changes-with-diff-view) con comentarios en línea
* [Vista previa de aplicación en vivo](#preview-your-app) con servidores de desarrollo, archivos HTML y PDF
* [Uso de computadora](#let-claude-use-your-computer) para abrir aplicaciones y controlar su pantalla en macOS y Windows
* [Monitoreo de PR de GitHub](#monitor-pull-request-status) con corrección automática, fusión automática y archivo automático
* [Dispatch](#sessions-from-dispatch) integración: envíe una tarea desde su teléfono, obtenga una sesión aquí
* [Tareas programadas](/es/desktop-scheduled-tasks) que ejecutan Claude en un horario recurrente
* [Conectores](#connect-external-tools) para GitHub, Slack, Linear y más
* Entornos locales, [SSH](#ssh-sessions) y [en la nube](#run-long-running-tasks-remotely)

<Note>
  El diseño del espacio de trabajo, terminal, editor de archivos, chats laterales y modos de vista descritos en esta página requieren Claude Desktop v1.2581.0 o posterior. Abra **Claude → Check for Updates** en macOS o **Help → Check for Updates** en Windows para actualizar.
</Note>

Esta página cubre [trabajar con código](#work-with-code), [organizar su espacio de trabajo](#arrange-your-workspace), [uso de computadora](#let-claude-use-your-computer), [gestionar sesiones](#manage-sessions), [extender Claude Code](#extend-claude-code) y [configuración](#environment-configuration). También incluye una [comparación de CLI](#coming-from-the-cli) y [solución de problemas](#troubleshooting).

## Iniciar una sesión

Antes de enviar su primer mensaje, configure cuatro cosas en el área de solicitud:

* **Entorno**: elija dónde se ejecuta Claude. Seleccione **Local** para su máquina, **Remote** para sesiones en la nube alojadas por Anthropic, o una [**conexión SSH**](#ssh-sessions) para una máquina remota que usted administra. Consulte [configuración del entorno](#environment-configuration).
* **Carpeta del proyecto**: seleccione la carpeta o repositorio en el que Claude trabaja. Para sesiones remotas, puede agregar [múltiples repositorios](#run-long-running-tasks-remotely).
* **Modelo**: elija un [modelo](/es/model-config#available-models) del menú desplegable junto al botón de envío. Puede cambiar esto durante la sesión.
* **Modo de permisos**: elija cuánta autonomía tiene Claude desde el [selector de modo](#choose-a-permission-mode). Puede cambiar esto durante la sesión.

Escriba su tarea y presione **Enter** para comenzar. Cada sesión rastrea su propio contexto y cambios de forma independiente.

## Trabajar con código

Proporcione a Claude el contexto correcto, controle cuánto hace por su cuenta y revise lo que cambió.

### Usar el cuadro de solicitud

Escriba lo que desea que Claude haga y presione **Enter** para enviar. Claude lee los archivos de su proyecto, realiza cambios y ejecuta comandos según su [modo de permisos](#choose-a-permission-mode). Puede interrumpir a Claude en cualquier momento: haga clic en el botón de parada o escriba su corrección y presione **Enter**. Claude detiene lo que está haciendo y se ajusta según su entrada.

El botón **+** junto al cuadro de solicitud le da acceso a archivos adjuntos, [skills](#use-skills), [conectores](#connect-external-tools) y [plugins](#install-plugins).

### Agregar archivos y contexto a las solicitudes

El cuadro de solicitud admite dos formas de traer contexto externo:

* **Archivos @mention**: escriba `@` seguido de un nombre de archivo para agregar un archivo al contexto de la conversación. Claude puede entonces leer y hacer referencia a ese archivo. @mention no está disponible en sesiones remotas.
* **Adjuntar archivos**: adjunte imágenes, PDF y otros archivos a su solicitud usando el botón de adjuntos, o arrastre y suelte archivos directamente en la solicitud. Esto es útil para compartir capturas de pantalla de errores, maquetas de diseño o documentos de referencia.

### Elegir un modo de permisos

Los modos de permisos controlan cuánta autonomía tiene Claude durante una sesión: si pregunta antes de editar archivos, ejecutar comandos o ambos. Puede cambiar de modo en cualquier momento usando el selector de modo junto al botón de envío. Comience con Ask permissions para ver exactamente qué hace Claude, luego pase a Auto accept edits o Plan mode a medida que se sienta cómodo.

| Modo                   | Clave de configuración | Comportamiento                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ---------------------- | ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ask permissions**    | `default`              | Claude pregunta antes de editar archivos o ejecutar comandos. Usted ve una diferencia y puede aceptar o rechazar cada cambio. Recomendado para nuevos usuarios.                                                                                                                                                                                                                                                                                                                                                               |
| **Auto accept edits**  | `acceptEdits`          | Claude acepta automáticamente ediciones de archivos y comandos comunes del sistema de archivos como `mkdir`, `touch` y `mv`, pero aún pregunta antes de ejecutar otros comandos de terminal. Use esto cuando confíe en cambios de archivos y desee una iteración más rápida.                                                                                                                                                                                                                                                  |
| **Plan mode**          | `plan`                 | Claude lee archivos y ejecuta comandos para explorar, luego propone un plan sin editar su código fuente. Bueno para tareas complejas donde desea revisar el enfoque primero.                                                                                                                                                                                                                                                                                                                                                  |
| **Auto**               | `auto`                 | Claude ejecuta todas las acciones con verificaciones de seguridad en segundo plano que verifican la alineación con su solicitud. Reduce solicitudes de permisos mientras mantiene supervisión. Actualmente una vista previa de investigación. Disponible en planes Max, Team, Enterprise y API. Requiere Claude Sonnet 4.6, Opus 4.6 u Opus 4.7 en planes Team, Enterprise y API; Claude Opus 4.7 solamente en planes Max. No disponible en planes Pro o proveedores de terceros. Habilite en su Configuración → Claude Code. |
| **Bypass permissions** | `bypassPermissions`    | Claude se ejecuta sin ningún aviso de permisos, equivalente a `--dangerously-skip-permissions` en la CLI. Habilite en su Configuración → Claude Code bajo "Allow bypass permissions mode". Use solo en contenedores o máquinas virtuales sandboxed. Los administradores empresariales pueden deshabilitar esta opción.                                                                                                                                                                                                        |

El modo de permisos `dontAsk` está disponible solo en la [CLI](/es/permission-modes#allow-only-pre-approved-tools-with-dontask-mode).

<Tip title="Mejor práctica">
  Comience tareas complejas en Plan mode para que Claude mapee un enfoque antes de realizar cambios. Una vez que apruebe el plan, cambie a Auto accept edits o Ask permissions para ejecutarlo. Consulte [explorar primero, luego planificar, luego codificar](/es/best-practices#explore-first-then-plan-then-code) para obtener más información sobre este flujo de trabajo.
</Tip>

Las sesiones remotas admiten Auto accept edits y Plan mode. Ask permissions no está disponible porque las sesiones remotas aceptan automáticamente ediciones de archivos de forma predeterminada, y Bypass permissions no está disponible porque el entorno remoto ya está sandboxed.

Los administradores empresariales pueden restringir qué modos de permisos están disponibles. Consulte [configuración empresarial](#enterprise-configuration) para obtener detalles.

### Vista previa de su aplicación

Claude puede iniciar un servidor de desarrollo y abrir un navegador integrado para verificar sus cambios. Esto funciona tanto para aplicaciones web frontend como para servidores backend: Claude puede probar puntos finales de API, ver registros del servidor e iterar sobre problemas que encuentra. En la mayoría de los casos, Claude inicia el servidor automáticamente después de editar archivos del proyecto. También puede pedirle a Claude que haga una vista previa en cualquier momento. De forma predeterminada, Claude [verifica automáticamente](#auto-verify-changes) cambios después de cada edición.

El panel de vista previa también puede abrir archivos HTML estáticos, PDF e imágenes de su proyecto. Haga clic en una ruta HTML, PDF o imagen en el chat para abrirla en vista previa.

Desde el panel de vista previa, puede:

* Interactuar con su aplicación en ejecución directamente en el navegador integrado
* Ver a Claude verificar sus propios cambios automáticamente: toma capturas de pantalla, inspecciona el DOM, hace clic en elementos, completa formularios y corrige problemas que encuentra
* Iniciar o detener servidores desde el menú desplegable **Preview** en la barra de herramientas de la sesión
* Persistir cookies y almacenamiento local en reinicios del servidor seleccionando **Persist sessions** en el menú desplegable, para que no tenga que volver a iniciar sesión durante el desarrollo
* Editar la configuración del servidor o detener todos los servidores a la vez

Claude crea la configuración inicial del servidor basada en su proyecto. Si su aplicación usa un comando de desarrollo personalizado, edite `.claude/launch.json` para que coincida con su configuración. Consulte [Configurar servidores de vista previa](#configure-preview-servers) para la referencia completa.

Para borrar datos de sesión guardados, alterne **Persist preview sessions** en Configuración → Claude Code. Para deshabilitar la vista previa por completo, alterne **Preview** en Configuración → Claude Code.

### Revisar cambios con vista de diferencias

Después de que Claude realiza cambios en su código, la vista de diferencias le permite revisar modificaciones archivo por archivo antes de crear una solicitud de extracción.

Cuando Claude cambia archivos, aparece un indicador de estadísticas de diferencias que muestra el número de líneas agregadas y eliminadas, como `+12 -1`. Haga clic en este indicador para abrir el visor de diferencias, que muestra una lista de archivos a la izquierda y los cambios para cada archivo a la derecha.

Para comentar en líneas específicas, haga clic en cualquier línea en la diferencia para abrir un cuadro de comentarios. Escriba su comentario y presione **Enter** para agregar el comentario. Después de agregar comentarios a varias líneas, envíe todos los comentarios a la vez:

* **macOS**: presione **Cmd+Enter**
* **Windows**: presione **Ctrl+Enter**

Claude lee sus comentarios y realiza los cambios solicitados, que aparecen como una nueva diferencia que puede revisar.

### Revisar su código

En la vista de diferencias, haga clic en **Review code** en la barra de herramientas superior derecha para pedirle a Claude que evalúe los cambios antes de confirmar. Claude examina las diferencias actuales y deja comentarios directamente en la vista de diferencias. Puede responder a cualquier comentario o pedirle a Claude que revise.

La revisión se enfoca en problemas de alta señal: errores de compilación, errores de lógica definitivos, vulnerabilidades de seguridad y errores obvios. No marca estilo, formato, problemas preexistentes o nada que un linter detectaría.

### Monitorear el estado de la solicitud de extracción

Después de abrir una solicitud de extracción, aparece una barra de estado de CI en la sesión. Claude Code usa la CLI de GitHub para sondear resultados de verificación y mostrar fallas.

* **Auto-fix**: cuando está habilitado, Claude intenta automáticamente corregir verificaciones de CI fallidas leyendo la salida de falla e iterando.
* **Auto-merge**: cuando está habilitado, Claude fusiona el PR una vez que todas las verificaciones pasan. El método de fusión es squash. Auto-merge debe estar [habilitado en la configuración de su repositorio de GitHub](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-auto-merge-for-pull-requests-in-your-repository) para que esto funcione.

Use los controles deslizantes **Auto-fix** y **Auto-merge** en la barra de estado de CI para habilitar cualquiera de las opciones. Claude Code también envía una notificación de escritorio cuando CI finaliza. Para archivar la sesión automáticamente una vez que el PR se fusiona o cierra, active [auto-archive](#work-in-parallel-with-sessions) en Configuración → Claude Code.

<Note>
  El monitoreo de PR requiere que la [CLI de GitHub (`gh`)](https://cli.github.com/) esté instalada y autenticada en su máquina. Si `gh` no está instalado, Desktop le solicita que lo instale la primera vez que intente crear un PR.
</Note>

## Organizar su espacio de trabajo

La aplicación de escritorio está construida alrededor de paneles que puede organizar en cualquier diseño: chat, diferencia, vista previa, terminal, archivo, plan, tareas y subagente. Arrastre un panel por su encabezado para reposicionarlo, o arrastre un borde de panel para redimensionarlo. Presione **Cmd+\\** en macOS o **Ctrl+\\** en Windows para cerrar el panel enfocado. Abra paneles adicionales desde el menú **Views** en la barra de herramientas de la sesión.

### Ejecutar comandos en la terminal

La terminal integrada le permite ejecutar comandos junto a su sesión sin cambiar a otra aplicación. Ábrala desde el menú **Views** o presione **Ctrl+\`** en macOS o Windows. La terminal se abre en el directorio de trabajo de su sesión y comparte el mismo entorno que Claude, por lo que comandos como `npm test` o `git status` ven los mismos archivos que Claude está editando. La terminal está disponible solo en sesiones locales.

### Abrir y editar archivos

Haga clic en una ruta de archivo en el chat o visor de diferencias para abrirlo en el panel de archivos. Las rutas HTML, PDF e imagen se abren en el [panel de vista previa](#preview-your-app) en su lugar. Realice ediciones puntuales y haga clic en **Save** para escribirlas de vuelta. Si el archivo cambió en el disco desde que lo abrió, el panel le advierte y le permite anular o descartar. Haga clic en **Discard** para revertir sus ediciones, o haga clic en la ruta en el encabezado del panel para copiar la ruta absoluta.

El panel de archivos está disponible en sesiones locales y SSH. Para sesiones remotas, pídale a Claude que realice el cambio.

### Abrir archivos en otras aplicaciones

Haga clic con el botón derecho en cualquier ruta de archivo en el chat, visor de diferencias o panel de archivos para abrir un menú contextual:

* **Attach as context**: agregue el archivo a su siguiente solicitud
* **Open in**: abra el archivo en un editor instalado como VS Code, Cursor o Zed
* **Show in Finder** en macOS, **Show in Explorer** en Windows: abra la carpeta contenedora
* **Copy path**: copie la ruta absoluta a su portapapeles

### Cambiar modos de vista

Los modos de vista controlan cuánto detalle aparece en la transcripción del chat. Cambie de modo desde el menú desplegable **Transcript view** junto al botón de envío, o presione **Ctrl+O** en macOS o Windows para ciclar a través de ellos.

| Modo        | Lo que muestra                                                                     |
| ----------- | ---------------------------------------------------------------------------------- |
| **Normal**  | Llamadas de herramientas contraídas en resúmenes, con respuestas de texto completo |
| **Verbose** | Cada llamada de herramienta, lectura de archivo y paso intermedio que Claude toma  |
| **Summary** | Solo las respuestas finales de Claude y los cambios que realizó                    |

Use Verbose cuando depure por qué Claude tomó una acción particular. Use Summary cuando esté ejecutando múltiples sesiones y desee escanear resultados rápidamente.

### Atajos de teclado

Presione **Cmd+/** en macOS o **Ctrl+/** en Windows para ver todos los atajos disponibles en la pestaña Code. En Windows, use **Ctrl** en lugar de **Cmd** para los atajos a continuación. El ciclismo de sesiones, el alternador de terminal y el alternador de modo de vista usan **Ctrl** en todas las plataformas.

| Atajo                                 | Acción                                  |
| ------------------------------------- | --------------------------------------- |
| `Cmd` `/`                             | Mostrar atajos de teclado               |
| `Cmd` `N`                             | Nueva sesión                            |
| `Cmd` `W`                             | Cerrar sesión                           |
| `Ctrl` `Tab` / `Ctrl` `Shift` `Tab`   | Siguiente o sesión anterior             |
| `Cmd` `Shift` `]` / `Cmd` `Shift` `[` | Siguiente o sesión anterior             |
| `Esc`                                 | Detener respuesta de Claude             |
| `Cmd` `Shift` `D`                     | Alternar panel de diferencias           |
| `Cmd` `Shift` `P`                     | Alternar panel de vista previa          |
| `Cmd` `Shift` `S`                     | Seleccionar un elemento en vista previa |
| `Ctrl` `` ` ``                        | Alternar panel de terminal              |
| `Cmd` `\`                             | Cerrar panel enfocado                   |
| `Cmd` `;`                             | Abrir chat lateral                      |
| `Ctrl` `O`                            | Ciclar modos de vista                   |
| `Cmd` `Shift` `M`                     | Abrir menú de modo de permisos          |
| `Cmd` `Shift` `I`                     | Abrir menú de modelo                    |
| `Cmd` `Shift` `E`                     | Abrir menú de esfuerzo                  |
| `1`–`9`                               | Seleccionar elemento en un menú abierto |

Estos atajos se aplican solo a la pestaña Code. Los [atajos de modo interactivo](/es/interactive-mode#keyboard-shortcuts) basados en terminal, como `Shift+Tab` para ciclar modos, no se aplican en Desktop.

### Verificar uso

Haga clic en el anillo de uso junto al selector de modelo para ver su uso actual de la ventana de contexto y su uso del plan para el período. El uso de contexto es por sesión; el uso del plan se comparte en todas sus superficies de Claude Code.

## Permitir que Claude use su computadora

El uso de computadora permite que Claude abra sus aplicaciones, controle su pantalla y trabaje directamente en su máquina de la manera que lo haría. Pídale a Claude que pruebe una aplicación nativa en un simulador móvil, interactúe con una herramienta de escritorio que no tiene CLI, o automatice algo que solo funciona a través de una GUI.

<Note>
  El uso de computadora es una vista previa de investigación en macOS y Windows que requiere un plan Pro o Max. No está disponible en planes Team o Enterprise. La aplicación Claude Desktop debe estar en ejecución.
</Note>

El uso de computadora está deshabilitado de forma predeterminada. [Habilítelo en Configuración](#enable-computer-use) antes de que Claude pueda controlar su pantalla. En macOS, también necesita otorgar permisos de Accesibilidad y Grabación de pantalla.

<Warning>
  A diferencia de la [herramienta Bash sandboxed](/es/sandboxing), el uso de computadora se ejecuta en su escritorio real con acceso a lo que apruebe. Claude verifica cada acción e identifica posibles inyecciones de solicitud desde contenido en pantalla, pero el límite de confianza es diferente. Consulte la [guía de seguridad de uso de computadora](https://support.claude.com/en/articles/14128542) para obtener mejores prácticas.
</Warning>

### Cuándo se aplica el uso de computadora

Claude tiene varias formas de interactuar con una aplicación o servicio, y el uso de computadora es la más amplia y lenta. Intenta la herramienta más precisa primero:

* Si tiene un [conector](#connect-external-tools) para un servicio, Claude usa el conector.
* Si la tarea es un comando de shell, Claude usa Bash.
* Si la tarea es trabajo en navegador y tiene [Claude en Chrome](/es/chrome) configurado, Claude usa eso.
* Si ninguno de esos se aplica, Claude usa el uso de computadora.

Los [niveles de acceso por aplicación](#app-permissions) refuerzan esto: los navegadores están limitados a solo lectura, y las terminales e IDE a solo clic, dirigiendo a Claude hacia la herramienta dedicada incluso cuando el uso de computadora está activo. El control de pantalla se reserva para cosas que nada más puede alcanzar, como aplicaciones nativas, paneles de control de hardware, simuladores móviles o herramientas propietarias sin una API.

### Habilitar el uso de computadora

El uso de computadora está deshabilitado de forma predeterminada. Si le pide a Claude que haga algo que lo necesita mientras está deshabilitado, Claude le dice que podría hacer la tarea si habilita el uso de computadora en Configuración.

<Steps>
  <Step title="Actualizar la aplicación de escritorio">
    Asegúrese de tener la última versión de Claude Desktop. Descargue o actualice en [claude.com/download](https://claude.com/download), luego reinicie la aplicación.
  </Step>

  <Step title="Activar el control deslizante">
    En la aplicación de escritorio, vaya a **Configuración > General** (bajo **Aplicación de escritorio**). Encuentre el control deslizante **Computer use** y actívelo. En Windows, el control deslizante surte efecto inmediatamente y la configuración está completa. En macOS, continúe con el siguiente paso.

    Si no ve el control deslizante, confirme que está en macOS o Windows con un plan Pro o Max, luego actualice y reinicie la aplicación.
  </Step>

  <Step title="Otorgar permisos de macOS">
    En macOS, otorgue dos permisos del sistema antes de que el control deslizante surta efecto:

    * **Accessibility**: permite que Claude haga clic, escriba y desplace
    * **Screen Recording**: permite que Claude vea lo que hay en su pantalla

    La página de Configuración muestra el estado actual de cada permiso. Si alguno se deniega, haga clic en la insignia para abrir el panel de Configuración del Sistema relevante.
  </Step>
</Steps>

### Permisos de aplicación

La primera vez que Claude necesita usar una aplicación, aparece un aviso en su sesión. Haga clic en **Allow for this session** o **Deny**. Las aprobaciones duran para la sesión actual, o 30 minutos en [sesiones generadas por Dispatch](#sessions-from-dispatch).

El aviso también muestra qué nivel de control obtiene Claude para esa aplicación. Estos niveles se fijan por categoría de aplicación y no se pueden cambiar:

| Nivel        | Lo que Claude puede hacer                                            | Se aplica a                         |
| :----------- | :------------------------------------------------------------------- | :---------------------------------- |
| View only    | Ver la aplicación en capturas de pantalla                            | Navegadores, plataformas de trading |
| Click only   | Hacer clic y desplazarse, pero no escribir ni usar atajos de teclado | Terminales, IDE                     |
| Full control | Hacer clic, escribir, arrastrar y usar atajos de teclado             | Todo lo demás                       |

Las aplicaciones con amplio alcance como terminales, Finder o File Explorer y Configuración del Sistema o Settings muestran una advertencia adicional en el aviso para que sepa qué aprobación les otorga.

Puede configurar dos configuraciones en **Configuración > General** (bajo **Aplicación de escritorio**):

* **Denied apps**: agregue aplicaciones aquí para rechazarlas sin solicitar. Claude aún puede afectar una aplicación denegada indirectamente a través de acciones en una aplicación permitida, pero no puede interactuar directamente con la aplicación denegada.
* **Unhide apps when Claude finishes**: mientras Claude está trabajando, sus otras ventanas se ocultan para que interactúe solo con la aplicación aprobada. Cuando Claude termina, las ventanas ocultas se restauran a menos que desactive esta configuración.

## Gestionar sesiones

Cada sesión es una conversación independiente con su propio contexto y cambios. Puede ejecutar múltiples sesiones en paralelo, ramificar chats laterales, enviar trabajo a la nube o permitir que Dispatch inicie sesiones para usted desde su teléfono.

### Trabajar en paralelo con sesiones

Haga clic en **+ New session** en la barra lateral, o presione **Cmd+N** en macOS o **Ctrl+N** en Windows, para trabajar en múltiples tareas en paralelo. Presione **Ctrl+Tab** y **Ctrl+Shift+Tab** para ciclar a través de sesiones en la barra lateral. Para repositorios de Git, cada sesión obtiene su propia copia aislada de su proyecto usando [Git worktrees](/es/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees), por lo que los cambios en una sesión no afectan otras sesiones hasta que los confirme.

Los worktrees se almacenan en `<project-root>/.claude/worktrees/` de forma predeterminada. Puede cambiar esto a un directorio personalizado en Configuración → Claude Code bajo "Worktree location". También puede establecer un prefijo de rama que se antepone a cada nombre de rama de worktree, lo que es útil para mantener las ramas creadas por Claude organizadas. Para eliminar un worktree cuando haya terminado, pase el cursor sobre la sesión en la barra lateral y haga clic en el icono de archivo. Para que las sesiones se archiven automáticamente cuando su solicitud de extracción se fusiona o cierra, active **Auto-archive after PR merge or close** en Configuración → Claude Code. Auto-archive solo se aplica a sesiones locales que han terminado de ejecutarse.

Para incluir archivos ignorados por git como `.env` en nuevos worktrees, cree un [archivo `.worktreeinclude`](/es/common-workflows#copy-gitignored-files-to-worktrees) en la raíz de su proyecto.

<Note>
  El aislamiento de sesión requiere [Git](https://git-scm.com/downloads). La mayoría de las Macs incluyen Git de forma predeterminada. Ejecute `git --version` en Terminal para verificar. En Windows, Git es necesario para que la pestaña Code funcione: [descargue Git para Windows](https://git-scm.com/downloads/win), instálelo y reinicie la aplicación. Si encuentra errores de Git, intente una sesión de Cowork para ayudar a solucionar problemas de su configuración.
</Note>

Use los controles en la parte superior de la barra lateral para filtrar sesiones por estado, proyecto o entorno, y para agrupar sesiones por proyecto. Para renombrar una sesión, haga clic en el título de la sesión en la barra de herramientas en la parte superior de la sesión activa. Para verificar el uso del contexto, consulte [Verificar uso](#check-usage). Cuando el contexto se llena, Claude resume automáticamente la conversación y continúa trabajando. También puede escribir `/compact` para activar la compresión antes y liberar espacio de contexto. Consulte [la ventana de contexto](/es/how-claude-code-works#the-context-window) para obtener detalles sobre cómo funciona la compresión.

### Hacer una pregunta lateral sin descarrilar la sesión

Un chat lateral le permite hacer una pregunta a Claude que usa el contexto de su sesión pero no agrega nada de vuelta a la conversación principal. Úselo cuando desee entender un fragmento de código, verificar una suposición o explorar una idea sin dirigir la sesión fuera de curso.

Presione **Cmd+;** en macOS o **Ctrl+;** en Windows para abrir un chat lateral, o escriba `/btw` en el cuadro de solicitud. El chat lateral puede leer todo en el hilo principal hasta ese punto. Cuando haya terminado, cierre el chat lateral y continúe la sesión principal donde la dejó. Los chats laterales están disponibles en sesiones locales y SSH.

### Ver tareas en segundo plano

El panel de tareas muestra el trabajo en segundo plano que se ejecuta dentro de la sesión actual: subagentes, comandos de shell en segundo plano y flujos de trabajo. Ábralo desde el menú **Views** o arrástrelo a su diseño.

Haga clic en cualquier entrada para ver su salida en el panel de subagente o detenerla. Para ver qué están haciendo otras sesiones, use la [barra lateral](#work-in-parallel-with-sessions).

### Ejecutar tareas de larga duración de forma remota

Para refactorizaciones grandes, suites de pruebas, migraciones u otras tareas de larga duración, seleccione **Remote** en lugar de **Local** al iniciar una sesión. Las sesiones remotas se ejecutan en la infraestructura en la nube de Anthropic y continúan incluso si cierra la aplicación o apaga su computadora. Regrese en cualquier momento para ver el progreso o dirigir a Claude en una dirección diferente. También puede monitorear sesiones remotas desde [claude.ai/code](https://claude.ai/code) o la aplicación Claude iOS.

Las sesiones remotas también admiten múltiples repositorios. Después de seleccionar un entorno en la nube, haga clic en el botón **+** junto a la píldora de repositorio para agregar repositorios adicionales a la sesión. Cada repositorio obtiene su propio selector de rama. Esto es útil para tareas que abarcan múltiples bases de código, como actualizar una biblioteca compartida y sus consumidores.

Consulte [Claude Code en la web](/es/claude-code-on-the-web) para obtener más información sobre cómo funcionan las sesiones remotas.

### Continuar en otra superficie

El menú **Continue in**, accesible desde el icono de VS Code en la esquina inferior derecha de la barra de herramientas de la sesión, le permite mover su sesión a otra superficie:

* **Claude Code on the Web**: envía su sesión local para continuar ejecutándose de forma remota. Desktop empuja su rama, genera un resumen de la conversación y crea una nueva sesión remota con el contexto completo. Luego puede elegir archivar la sesión local o mantenerla. Esto requiere un árbol de trabajo limpio y no está disponible para sesiones SSH.
* **Your IDE**: abre su proyecto en un IDE compatible en el directorio de trabajo actual.

### Sesiones desde Dispatch

[Dispatch](https://support.claude.com/en/articles/13947068) es una conversación persistente con Claude que vive en la pestaña [Cowork](https://claude.com/product/cowork#dispatch-and-computer-use). Usted envía un mensaje a Dispatch con una tarea, y decide cómo manejarla.

Una tarea puede terminar como una sesión de Code de dos formas: usted solicita una directamente, como "abra una sesión de Claude Code y corrija el error de inicio de sesión", o Dispatch decide que la tarea es trabajo de desarrollo e inicia una por su cuenta. Las tareas que típicamente se enrutan a Code incluyen corregir errores, actualizar dependencias, ejecutar pruebas o abrir solicitudes de extracción. La investigación, edición de documentos y trabajo con hojas de cálculo permanecen en Cowork.

De cualquier forma, la sesión de Code aparece en la barra lateral de la pestaña Code con una insignia **Dispatch**. Obtiene una notificación push en su teléfono cuando termina o necesita su aprobación.

Si tiene [uso de computadora](#let-claude-use-your-computer) habilitado, las sesiones de Code generadas por Dispatch también pueden usarlo. Las aprobaciones de aplicaciones en esas sesiones expiran después de 30 minutos y vuelven a solicitar, en lugar de durar la sesión completa como las sesiones de Code regulares.

Para configuración, emparejamiento y configuración de Dispatch, consulte el [artículo de ayuda de Dispatch](https://support.claude.com/en/articles/13947068). Dispatch requiere un plan Pro o Max y no está disponible en planes Team o Enterprise.

Dispatch es una de varias formas de trabajar con Claude cuando está lejos de su terminal. Consulte [Plataformas e integraciones](/es/platforms#work-when-you-are-away-from-your-terminal) para compararlo con Remote Control, Channels, Slack y tareas programadas.

## Extender Claude Code

Conecte servicios externos, agregue flujos de trabajo reutilizables, personalice el comportamiento de Claude y configure servidores de vista previa.

### Conectar herramientas externas

Para sesiones locales y [SSH](#ssh-sessions), haga clic en el botón **+** junto al cuadro de solicitud y seleccione **Connectors** para agregar integraciones como Google Calendar, Slack, GitHub, Linear, Notion y más. Puede agregar conectores antes o durante una sesión. El botón **+** no está disponible en sesiones remotas, pero [routines](/es/routines) configuran conectores en el momento de la creación de la rutina.

Para administrar o desconectar conectores, vaya a Configuración → Connectors en la aplicación de escritorio, o seleccione **Manage connectors** desde el menú Connectors en el cuadro de solicitud.

Una vez conectado, Claude puede leer su calendario, enviar mensajes, crear problemas e interactuar con sus herramientas directamente. Puede preguntarle a Claude qué conectores están configurados en su sesión.

Los conectores son [MCP servers](/es/mcp) con un flujo de configuración gráfico. Úselos para integración rápida con servicios compatibles. Para integraciones no listadas en Connectors, agregue MCP servers manualmente a través de [archivos de configuración](/es/mcp#installing-mcp-servers). También puede [crear conectores personalizados](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp).

### Usar skills

[Skills](/es/skills) extienden lo que Claude puede hacer. Claude los carga automáticamente cuando son relevantes, o puede invocar uno directamente: escriba `/` en el cuadro de solicitud o haga clic en el botón **+** y seleccione **Slash commands** para ver lo que está disponible. Esto incluye [comandos integrados](/es/commands), sus [skills personalizados](/es/skills#create-your-first-skill), skills del proyecto desde su base de código y skills de cualquier [plugin instalado](/es/plugins). Seleccione uno y aparecerá resaltado en el campo de entrada. Escriba su tarea después de él y envíe como de costumbre.

### Instalar plugins

[Plugins](/es/plugins) son paquetes reutilizables que agregan skills, agentes, hooks, MCP servers y configuraciones LSP a Claude Code. Puede instalar plugins desde la aplicación de escritorio sin usar la terminal.

Para sesiones locales y [SSH](#ssh-sessions), haga clic en el botón **+** junto al cuadro de solicitud y seleccione **Plugins** para ver sus plugins instalados y sus skills. Para agregar un plugin, seleccione **Add plugin** del submenú para abrir el navegador de plugins, que muestra plugins disponibles desde sus [marketplaces](/es/plugin-marketplaces) configurados incluyendo el marketplace oficial de Anthropic. Seleccione **Manage plugins** para habilitar, deshabilitar o desinstalar plugins.

Los plugins pueden estar limitados a su cuenta de usuario, un proyecto específico o solo locales. Si su organización gestiona plugins centralmente, esos plugins están disponibles en sesiones de escritorio de la misma manera que en la CLI. Los plugins no están disponibles para sesiones remotas. Para la referencia completa de plugins incluyendo crear sus propios plugins, consulte [plugins](/es/plugins).

### Configurar servidores de vista previa

Claude detecta automáticamente su configuración de servidor de desarrollo y almacena la configuración en `.claude/launch.json` en la raíz de la carpeta que seleccionó al iniciar la sesión. Preview usa esta carpeta como su directorio de trabajo, por lo que si seleccionó una carpeta principal, las subcarpetas con sus propios servidores de desarrollo no se detectarán automáticamente. Para trabajar con el servidor de una subcarpeta, inicie una sesión en esa carpeta directamente o agregue una configuración manualmente.

Para personalizar cómo se inicia su servidor, por ejemplo para usar `yarn dev` en lugar de `npm run dev` o para cambiar el puerto, edite el archivo manualmente o haga clic en **Edit configuration** en el menú desplegable Preview para abrirlo en su editor de código. El archivo admite JSON con comentarios.

```json theme={null}
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "my-app",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "port": 3000
    }
  ]
}
```

Puede definir múltiples configuraciones para ejecutar diferentes servidores desde el mismo proyecto, como un frontend y una API. Consulte los [ejemplos](#examples) a continuación.

#### Verificación automática de cambios

Cuando `autoVerify` está habilitado, Claude verifica automáticamente cambios de código después de editar archivos. Toma capturas de pantalla, verifica errores y confirma que los cambios funcionan antes de completar su respuesta.

Auto-verify está habilitado de forma predeterminada. Desactívelo por proyecto agregando `"autoVerify": false` a `.claude/launch.json`, o alterne desde el menú desplegable **Preview**.

```json theme={null}
{
  "version": "0.0.1",
  "autoVerify": false,
  "configurations": [...]
}
```

Cuando está deshabilitado, las herramientas de vista previa aún están disponibles y puede pedirle a Claude que verifique en cualquier momento. Auto-verify lo hace automático después de cada edición.

#### Campos de configuración

Cada entrada en el array `configurations` acepta los siguientes campos:

| Campo               | Tipo      | Descripción                                                                                                                                                                                                                                                                                           |
| ------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`              | string    | Un identificador único para este servidor                                                                                                                                                                                                                                                             |
| `runtimeExecutable` | string    | El comando a ejecutar, como `npm`, `yarn` o `node`                                                                                                                                                                                                                                                    |
| `runtimeArgs`       | string\[] | Argumentos pasados a `runtimeExecutable`, como `["run", "dev"]`                                                                                                                                                                                                                                       |
| `port`              | number    | El puerto en el que escucha su servidor. Por defecto es 3000                                                                                                                                                                                                                                          |
| `cwd`               | string    | Directorio de trabajo relativo a la raíz de su proyecto. Por defecto es la raíz del proyecto. Use `${workspaceFolder}` para hacer referencia a la raíz del proyecto explícitamente                                                                                                                    |
| `env`               | object    | Variables de entorno adicionales como pares clave-valor, como `{ "NODE_ENV": "development" }`. No ponga secretos aquí ya que este archivo se confirma en su repositorio. Para pasar secretos a su servidor de desarrollo, establézcalos en el [editor de entorno local](#local-sessions) en su lugar. |
| `autoPort`          | boolean   | Cómo manejar conflictos de puerto. Consulte a continuación                                                                                                                                                                                                                                            |
| `program`           | string    | Un script a ejecutar con `node`. Consulte [cuándo usar `program` vs `runtimeExecutable`](#when-to-use-program-vs-runtimeexecutable)                                                                                                                                                                   |
| `args`              | string\[] | Argumentos pasados a `program`. Solo se usa cuando `program` está establecido                                                                                                                                                                                                                         |

##### Cuándo usar `program` vs `runtimeExecutable`

Use `runtimeExecutable` con `runtimeArgs` para iniciar un servidor de desarrollo a través de un administrador de paquetes. Por ejemplo, `"runtimeExecutable": "npm"` con `"runtimeArgs": ["run", "dev"]` ejecuta `npm run dev`.

Use `program` cuando tenga un script independiente que desee ejecutar con `node` directamente. Por ejemplo, `"program": "server.js"` ejecuta `node server.js`. Pase banderas adicionales con `args`.

#### Conflictos de puerto

El campo `autoPort` controla qué sucede cuando su puerto preferido ya está en uso:

* **`true`**: Claude encuentra y usa un puerto libre automáticamente. Adecuado para la mayoría de servidores de desarrollo.
* **`false`**: Claude falla con un error. Use esto cuando su servidor debe usar un puerto específico, como para devoluciones de llamada OAuth o listas de permitidos CORS.
* **No establecido (predeterminado)**: Claude pregunta si el servidor necesita ese puerto exacto, luego guarda su respuesta.

Cuando Claude elige un puerto diferente, pasa el puerto asignado a su servidor a través de la variable de entorno `PORT`.

#### Ejemplos

Estas configuraciones muestran configuraciones comunes para diferentes tipos de proyectos:

<Tabs>
  <Tab title="Next.js">
    Esta configuración ejecuta una aplicación Next.js usando Yarn en el puerto 3000:

    ```json theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "web",
          "runtimeExecutable": "yarn",
          "runtimeArgs": ["dev"],
          "port": 3000
        }
      ]
    }
    ```
  </Tab>

  <Tab title="Multiple servers">
    Para un monorepo con un servidor frontend y API, defina múltiples configuraciones. El frontend usa `autoPort: true` para que elija un puerto libre si 3000 está ocupado, mientras que el servidor API requiere el puerto 8080 exactamente:

    ```json theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "frontend",
          "runtimeExecutable": "npm",
          "runtimeArgs": ["run", "dev"],
          "cwd": "apps/web",
          "port": 3000,
          "autoPort": true
        },
        {
          "name": "api",
          "runtimeExecutable": "npm",
          "runtimeArgs": ["run", "start"],
          "cwd": "server",
          "port": 8080,
          "env": { "NODE_ENV": "development" },
          "autoPort": false
        }
      ]
    }
    ```
  </Tab>

  <Tab title="Node.js script">
    Para ejecutar un script Node.js directamente en lugar de usar un comando del administrador de paquetes, use el campo `program`:

    ```json theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "server",
          "program": "server.js",
          "args": ["--verbose"],
          "port": 4000
        }
      ]
    }
    ```
  </Tab>
</Tabs>

## Configuración del entorno

El entorno que elige al [iniciar una sesión](#start-a-session) determina dónde Claude se ejecuta y cómo se conecta:

* **Local**: se ejecuta en su máquina con acceso directo a sus archivos
* **Remote**: se ejecuta en la infraestructura en la nube de Anthropic. Las sesiones continúan incluso si cierra la aplicación.
* **SSH**: se ejecuta en una máquina remota a la que se conecta a través de SSH, como sus propios servidores, máquinas virtuales en la nube o contenedores de desarrollo

### Sesiones locales

La aplicación de escritorio no siempre hereda su entorno de shell completo. En macOS, cuando inicia la aplicación desde el Dock o Finder, lee su perfil de shell, como `~/.zshrc` o `~/.bashrc`, para extraer `PATH` y un conjunto fijo de variables de Claude Code, pero otras variables que exporta allí no se recogen. En Windows, la aplicación hereda variables de entorno de usuario y sistema pero no lee perfiles de PowerShell.

Para establecer variables de entorno para sesiones locales y servidores de desarrollo en cualquier plataforma, abra el menú desplegable de entorno en el cuadro de solicitud, pase el cursor sobre **Local** y haga clic en el icono de engranaje para abrir el editor de entorno local. Las variables que guarda aquí se almacenan cifradas en su máquina y se aplican a cada sesión local y servidor de vista previa que inicia. También puede agregar variables a la clave `env` en su archivo `~/.claude/settings.json`, aunque estas llegan solo a sesiones de Claude y no a servidores de desarrollo. Consulte [variables de entorno](/es/env-vars) para la lista completa de variables compatibles.

[Extended thinking](/es/common-workflows#use-extended-thinking-thinking-mode) está habilitado de forma predeterminada, lo que mejora el rendimiento en tareas de razonamiento complejo pero usa tokens adicionales. Para deshabilitar el pensamiento por completo, establezca `MAX_THINKING_TOKENS` en `0` en el editor de entorno local. En modelos con [razonamiento adaptativo](/es/model-config#adjust-effort-level), cualquier otro valor de `MAX_THINKING_TOKENS` se ignora porque el razonamiento adaptativo controla la profundidad del pensamiento en su lugar. En Opus 4.6 y Sonnet 4.6, establezca `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` en `1` para usar un presupuesto de pensamiento fijo; Opus 4.7 siempre usa razonamiento adaptativo y no tiene modo de presupuesto fijo.

### Sesiones remotas

Las sesiones remotas continúan en segundo plano incluso si cierra la aplicación. El uso cuenta hacia los límites de su [plan de suscripción](/es/costs) sin cargos de computación separados.

Puede crear entornos en la nube personalizados con diferentes niveles de acceso a la red y variables de entorno. Seleccione el menú desplegable de entorno al iniciar una sesión remota y elija **Add environment**. Consulte [el entorno en la nube](/es/claude-code-on-the-web#the-cloud-environment) para obtener detalles sobre la configuración del acceso a la red y variables de entorno.

### Sesiones SSH

Las sesiones SSH le permiten ejecutar Claude Code en una máquina remota mientras usa la aplicación de escritorio como su interfaz. Esto es útil para trabajar con bases de código que viven en máquinas virtuales en la nube, contenedores de desarrollo o servidores con hardware o dependencias específicas.

Para agregar una conexión SSH, haga clic en el menú desplegable de entorno antes de iniciar una sesión y seleccione **+ Add SSH connection**. El diálogo solicita:

* **Name**: una etiqueta amigable para esta conexión
* **SSH Host**: `user@hostname` o un host definido en `~/.ssh/config`
* **SSH Port**: por defecto es 22 si se deja vacío, o usa el puerto de su configuración SSH
* **Identity File**: ruta a su clave privada, como `~/.ssh/id_rsa`. Déjelo vacío para usar la clave predeterminada o su configuración SSH.

Una vez agregada, la conexión aparece en el menú desplegable de entorno. Selecciónela para iniciar una sesión en esa máquina. Claude se ejecuta en la máquina remota con acceso a sus archivos y herramientas.

La máquina remota debe ejecutar Linux o macOS, y Claude Code debe estar instalado en ella. Una vez conectado, las sesiones SSH admiten modos de permisos, conectores, plugins y MCP servers.

#### Pre-configurar conexiones SSH para su equipo

Los administradores pueden distribuir conexiones SSH a los miembros del equipo agregando `sshConfigs` a un archivo de [configuración administrada](/es/settings#settings-precedence). Las conexiones definidas de esta manera aparecen en el menú desplegable de entorno de cada usuario automáticamente y se muestran como administradas, por lo que los usuarios pueden seleccionarlas pero no pueden editarlas ni eliminarlas en la aplicación.

El siguiente ejemplo pre-configura una única conexión que se abre en `~/projects` en el host remoto:

```json theme={null}
{
  "sshConfigs": [
    {
      "id": "shared-dev-vm",
      "name": "Shared Dev VM",
      "sshHost": "user@dev.example.com",
      "sshPort": 22,
      "sshIdentityFile": "~/.ssh/id_ed25519",
      "startDirectory": "~/projects"
    }
  ]
}
```

Cada entrada requiere `id`, `name` y `sshHost`. Los campos `sshPort`, `sshIdentityFile` y `startDirectory` son opcionales. Los usuarios también pueden agregar `sshConfigs` a su propio `~/.claude/settings.json`, que es donde se almacenan las conexiones agregadas a través del diálogo.

## Configuración empresarial

Las organizaciones en planes Team o Enterprise pueden gestionar el comportamiento de la aplicación de escritorio a través de controles de consola de administración, archivos de configuración administrados y políticas de gestión de dispositivos.

### Controles de consola de administración

Estas configuraciones se configuran a través de la [consola de configuración de administración](https://claude.ai/admin-settings/claude-code):

* **Code in the desktop**: controle si los usuarios en su organización pueden acceder a Claude Code en la aplicación de escritorio
* **Code in the web**: habilite o deshabilite [sesiones web](/es/claude-code-on-the-web) para su organización
* **Remote Control**: habilite o deshabilite [Remote Control](/es/remote-control) para su organización
* **Disable Bypass permissions mode**: evite que los usuarios en su organización habiliten el modo bypass permissions

### Configuración administrada

La configuración administrada anula la configuración del proyecto y usuario y se aplica cuando Desktop genera sesiones de CLI. Puede establecer estas claves en el archivo de [configuración administrada](/es/settings#settings-precedence) de su organización o enviarlas de forma remota a través de la consola de administración.

| Clave                                      | Descripción                                                                                                                                                                                                     |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `permissions.disableBypassPermissionsMode` | establezca en `"disable"` para evitar que los usuarios habiliten el modo bypass permissions.                                                                                                                    |
| `disableAutoMode`                          | establezca en `"disable"` para evitar que los usuarios habiliten el modo [Auto](/es/permission-modes#eliminate-prompts-with-auto-mode). Elimina Auto del selector de modo. También aceptado bajo `permissions`. |
| `autoMode`                                 | personalice lo que el clasificador de modo auto confía y bloquea en toda su organización. Consulte [Configurar el clasificador de modo auto](/es/permissions#configure-the-auto-mode-classifier).               |
| `sshConfigs`                               | pre-configure [conexiones SSH](#pre-configure-ssh-connections-for-your-team) que aparecen en el menú desplegable de entorno. Los usuarios no pueden editar ni eliminar conexiones administradas.                |

`permissions.disableBypassPermissionsMode` y `disableAutoMode` también funcionan en configuración de usuario y proyecto, pero colocarlos en configuración administrada evita que los usuarios los anulen. `autoMode` se lee desde configuración de usuario, `.claude/settings.local.json` y configuración administrada, pero no desde `.claude/settings.json` verificado: un repositorio clonado no puede inyectar sus propias reglas de clasificador. Para la lista completa de configuraciones solo administradas incluyendo `allowManagedPermissionRulesOnly` y `allowManagedHooksOnly`, consulte [configuraciones solo administradas](/es/permissions#managed-only-settings).

La configuración administrada remota cargada a través de la consola de administración actualmente se aplica solo a sesiones de CLI e IDE. Para restricciones específicas de Desktop, use los controles de consola de administración anteriores.

### Políticas de gestión de dispositivos

Los equipos de TI pueden gestionar la aplicación de escritorio a través de MDM en macOS o política de grupo en Windows. Las políticas disponibles incluyen habilitar o deshabilitar la función Claude Code, controlar actualizaciones automáticas y establecer una URL de implementación personalizada.

* **macOS**: configure a través del dominio de preferencia `com.anthropic.Claude` usando herramientas como Jamf o Kandji
* **Windows**: configure a través del registro en `SOFTWARE\Policies\Claude`

### Autenticación y SSO

Las organizaciones empresariales pueden requerir SSO para todos los usuarios. Consulte [autenticación](/es/authentication) para obtener detalles a nivel de plan y [Configurar SSO](https://support.claude.com/en/articles/13132885-setting-up-single-sign-on-sso) para la configuración de SAML y OIDC.

### Manejo de datos

Claude Code procesa su código localmente en sesiones locales o en la infraestructura en la nube de Anthropic en sesiones remotas. Las conversaciones y el contexto del código se envían a la API de Anthropic para procesamiento. Consulte [manejo de datos](/es/data-usage) para obtener detalles sobre retención de datos, privacidad y cumplimiento.

### Implementación

Desktop se puede distribuir a través de herramientas de implementación empresarial:

* **macOS**: distribuya a través de MDM como Jamf o Kandji usando el instalador `.dmg`
* **Windows**: implemente a través del paquete MSIX o instalador `.exe`. Consulte [Deploy Claude Desktop for Windows](https://support.claude.com/en/articles/12622703-deploy-claude-desktop-for-windows) para opciones de implementación empresarial incluyendo instalación silenciosa

Para configuración de red como configuración de proxy, lista de permitidos de firewall y puertas de enlace LLM, consulte [configuración de red](/es/network-config).

Para la referencia completa de configuración empresarial, consulte la [guía de configuración empresarial](https://support.claude.com/en/articles/12622667-enterprise-configuration).

## ¿Viene de la CLI?

Si ya usa la CLI de Claude Code, Desktop ejecuta el mismo motor subyacente con una interfaz gráfica. Puede ejecutar ambos simultáneamente en la misma máquina, incluso en el mismo proyecto. Cada uno mantiene historial de sesión separado, pero comparten configuración y memoria del proyecto a través de archivos CLAUDE.md.

Para mover una sesión de CLI a Desktop, ejecute `/desktop` en la terminal. Claude guarda su sesión y la abre en la aplicación de escritorio, luego sale de la CLI. Este comando está disponible solo en macOS y Windows.

<Tip>
  Cuándo usar Desktop vs CLI: use Desktop cuando desee gestionar sesiones paralelas en una ventana, organizar paneles lado a lado o revisar cambios visualmente. Use la CLI cuando necesite scripting, automatización o prefiera un flujo de trabajo de terminal.
</Tip>

### Equivalentes de banderas de CLI

Esta tabla muestra el equivalente de la aplicación de escritorio para banderas de CLI comunes. Las banderas no listadas no tienen equivalente de escritorio porque están diseñadas para scripting o automatización.

| CLI                                       | Equivalente de Desktop                                                                                                                                                        |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--model sonnet`                          | Menú desplegable de modelo junto al botón de envío                                                                                                                            |
| `--resume`, `--continue`                  | Haga clic en una sesión en la barra lateral                                                                                                                                   |
| `--permission-mode`                       | Selector de modo junto al botón de envío                                                                                                                                      |
| `--dangerously-skip-permissions`          | Modo Bypass permissions. Habilite en Configuración → Claude Code → "Allow bypass permissions mode". Los administradores empresariales pueden deshabilitar esta configuración. |
| `--add-dir`                               | Agregue múltiples repositorios con el botón **+** en sesiones remotas                                                                                                         |
| `--allowedTools`, `--disallowedTools`     | No disponible en Desktop                                                                                                                                                      |
| `--verbose`                               | Modo de vista [Verbose](#switch-view-modes) en el menú desplegable Transcript view                                                                                            |
| `--print`, `--output-format`              | No disponible. Desktop es solo interactivo.                                                                                                                                   |
| Variable de entorno `ANTHROPIC_MODEL`     | Menú desplegable de modelo junto al botón de envío                                                                                                                            |
| Variable de entorno `MAX_THINKING_TOKENS` | Establezca en el editor de entorno local. Consulte [configuración del entorno](#environment-configuration).                                                                   |

### Configuración compartida

Desktop y CLI leen los mismos archivos de configuración, por lo que su configuración se transfiere:

* Los archivos **[CLAUDE.md](/es/memory)** y `CLAUDE.local.md` en su proyecto son utilizados por ambos
* Los **[MCP servers](/es/mcp)** configurados en `~/.claude.json` o `.mcp.json` funcionan en ambos
* Los **[Hooks](/es/hooks)** y **[skills](/es/skills)** definidos en configuración se aplican a ambos
* La **[Configuración](/es/settings)** en `~/.claude.json` y `~/.claude/settings.json` se comparte. Las reglas de permisos, herramientas permitidas y otras configuraciones en `settings.json` se aplican a sesiones de Desktop.
* **Modelos**: Sonnet, Opus y Haiku están disponibles en ambos. En Desktop, seleccione el modelo del menú desplegable junto al botón de envío. Puede cambiar el modelo durante la sesión desde el mismo menú desplegable.

<Note>
  **MCP servers: aplicación de chat de Desktop vs Claude Code**: Los MCP servers configurados para la aplicación de chat de Claude Desktop en `claude_desktop_config.json` son separados de Claude Code y no aparecerán en la pestaña Code. Para usar MCP servers en Claude Code, configúrelos en `~/.claude.json` o en el archivo `.mcp.json` de su proyecto. Consulte [configuración de MCP](/es/mcp#installing-mcp-servers) para obtener detalles.
</Note>

### Comparación de características

Esta tabla compara capacidades principales entre la CLI y Desktop. Para una lista completa de banderas de CLI, consulte la [referencia de CLI](/es/cli-reference).

| Característica                                          | CLI                                                       | Desktop                                                                                                                                                                                                                                                                |
| ------------------------------------------------------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Modos de permisos                                       | Todos los modos incluyendo `dontAsk`                      | Ask permissions, Auto accept edits, Plan mode, Auto y Bypass permissions a través de Configuración                                                                                                                                                                     |
| `--dangerously-skip-permissions`                        | Bandera de CLI                                            | Modo Bypass permissions. Habilite en Configuración → Claude Code → "Allow bypass permissions mode"                                                                                                                                                                     |
| [Proveedores de terceros](/es/third-party-integrations) | Bedrock, Vertex, Foundry                                  | API de Anthropic de forma predeterminada. Las implementaciones empresariales pueden configurar Vertex AI y proveedores de puerta de enlace. Consulte la [guía de configuración empresarial](https://support.claude.com/en/articles/12622667-enterprise-configuration). |
| [MCP servers](/es/mcp)                                  | Configurar en archivos de configuración                   | UI de Connectors para sesiones locales y SSH, o archivos de configuración                                                                                                                                                                                              |
| [Plugins](/es/plugins)                                  | Comando `/plugin`                                         | UI del administrador de plugins                                                                                                                                                                                                                                        |
| Archivos @mention                                       | Basado en texto                                           | Con autocompletado; sesiones locales y SSH solamente                                                                                                                                                                                                                   |
| Archivos adjuntos                                       | No disponible                                             | Imágenes, PDF                                                                                                                                                                                                                                                          |
| Aislamiento de sesión                                   | Bandera [`--worktree`](/es/cli-reference)                 | Worktrees automáticos                                                                                                                                                                                                                                                  |
| Múltiples sesiones                                      | Terminales separadas                                      | Pestañas de barra lateral                                                                                                                                                                                                                                              |
| Tareas recurrentes                                      | Trabajos cron, tuberías de CI                             | [Tareas programadas](/es/desktop-scheduled-tasks)                                                                                                                                                                                                                      |
| Uso de computadora                                      | [Habilitar a través de `/mcp`](/es/computer-use) en macOS | [Control de aplicaciones y pantalla](#let-claude-use-your-computer) en macOS y Windows                                                                                                                                                                                 |
| Integración de Dispatch                                 | No disponible                                             | [Sesiones de Dispatch](#sessions-from-dispatch) en la barra lateral                                                                                                                                                                                                    |
| Scripting y automatización                              | [`--print`](/es/cli-reference), [Agent SDK](/es/headless) | No disponible                                                                                                                                                                                                                                                          |

### Lo que no está disponible en Desktop

Las siguientes características están disponibles solo en la CLI o extensión de VS Code:

* **Proveedores de terceros**: Desktop se conecta a la API de Anthropic de forma predeterminada. Las implementaciones empresariales pueden configurar Vertex AI y proveedores de puerta de enlace a través de [configuración administrada](https://support.claude.com/en/articles/12622667-enterprise-configuration). Para Bedrock o Foundry, use la [CLI](/es/quickstart).
* **Linux**: la aplicación de escritorio está disponible solo en macOS y Windows.
* **Sugerencias de código en línea**: Desktop no proporciona sugerencias de estilo autocompletado. Funciona a través de solicitudes conversacionales y cambios de código explícitos.
* **Equipos de agentes**: la orquestación de múltiples agentes está disponible a través de la [CLI](/es/agent-teams) y [Agent SDK](/es/headless), no en Desktop.

## Solución de problemas

Las secciones a continuación cubren problemas específicos de la aplicación de escritorio. Para errores de API en tiempo de ejecución que aparecen en el chat como `API Error: 500`, `529 Overloaded`, `429` o `Prompt is too long`, consulte la [referencia de errores](/es/errors). Esos errores y sus soluciones son los mismos en la CLI, escritorio y web.

### Verificar su versión

Para ver qué versión de la aplicación de escritorio está ejecutando:

* **macOS**: haga clic en **Claude** en la barra de menú, luego **About Claude**
* **Windows**: haga clic en **Help**, luego **About**

Haga clic en el número de versión para copiarlo a su portapapeles.

### Errores 403 o de autenticación en la pestaña Code

Si ve `Error 403: Forbidden` u otros fallos de autenticación al usar la pestaña Code:

1. Cierre sesión e inicie sesión nuevamente desde el menú de la aplicación. Esta es la solución más común.
2. Verifique que tenga una suscripción de pago activa: Pro, Max, Team o Enterprise.
3. Si la CLI funciona pero Desktop no, cierre completamente la aplicación de escritorio, no solo cierre la ventana, luego reabrala e inicie sesión nuevamente.
4. Verifique su conexión a Internet y configuración de proxy.

### Pantalla en blanco o atascada al iniciar

Si la aplicación se abre pero muestra una pantalla en blanco o sin respuesta:

1. Reinicie la aplicación.
2. Verifique si hay actualizaciones pendientes. La aplicación se actualiza automáticamente al iniciar.
3. En Windows, verifique Event Viewer para registros de bloqueo bajo **Windows Logs → Application**.

### "Failed to load session"

Si ve `Failed to load session`, la carpeta seleccionada puede no existir más, un repositorio de Git puede requerir Git LFS que no está instalado, o los permisos de archivo pueden impedir el acceso. Intente seleccionar una carpeta diferente o reinicie la aplicación.

### La sesión no encuentra herramientas instaladas

Si Claude no puede encontrar herramientas como `npm`, `node` u otros comandos de CLI, verifique que las herramientas funcionen en su terminal regular, verifique que su perfil de shell configure correctamente PATH y reinicie la aplicación de escritorio para recargar variables de entorno.

### Errores de Git y Git LFS

En Windows, Git es necesario para que la pestaña Code inicie sesiones locales. Si ve "Git is required," instale [Git para Windows](https://git-scm.com/downloads/win) y reinicie la aplicación.

Si ve "Git LFS is required by this repository but is not installed," instale Git LFS desde [git-lfs.com](https://git-lfs.com/), ejecute `git lfs install` y reinicie la aplicación.

### Los MCP servers no funcionan en Windows

Si los controles deslizantes de MCP server no responden o los servidores no se conectan en Windows, verifique que el servidor esté configurado correctamente en su configuración, reinicie la aplicación, verifique que el proceso del servidor se esté ejecutando en Task Manager y revise los registros del servidor para errores de conexión.

### La aplicación no se cierra

* **macOS**: presione Cmd+Q. Si la aplicación no responde, use Force Quit con Cmd+Option+Esc, seleccione Claude y haga clic en Force Quit.
* **Windows**: use Task Manager con Ctrl+Shift+Esc para finalizar el proceso de Claude.

### Problemas específicos de Windows

* **PATH no actualizado después de instalar**: abra una nueva ventana de terminal. Las actualizaciones de PATH solo se aplican a nuevas sesiones de terminal.
* **Error de instalación concurrente**: si ve un error sobre otra instalación en progreso pero no la hay, intente ejecutar el instalador como Administrador.

### "Branch doesn't exist yet" al abrir en CLI

Las sesiones remotas pueden crear ramas que no existen en su máquina local. Haga clic en el nombre de la rama en la barra de herramientas de la sesión para copiarlo, luego obténgalo localmente:

```bash theme={null}
git fetch origin <branch-name>
git checkout <branch-name>
```

### ¿Aún atascado?

* Busque o presente un error en [GitHub Issues](https://github.com/anthropics/claude-code/issues)
* Visite el [centro de soporte de Claude](https://support.claude.com/)

Al presentar un error, incluya la versión de su aplicación de escritorio, su sistema operativo, el mensaje de error exacto y registros relevantes. En macOS, verifique Console.app. En Windows, verifique Event Viewer → Windows Logs → Application.
