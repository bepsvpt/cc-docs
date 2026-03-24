> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Usar Claude Code Desktop

> Aproveche al máximo Claude Code Desktop: sesiones paralelas con aislamiento de Git, revisión visual de diferencias, vistas previas de aplicaciones, monitoreo de PR, modos de permisos, conectores y configuración empresarial.

La pestaña Code dentro de la aplicación Claude Desktop le permite usar Claude Code a través de una interfaz gráfica en lugar de la terminal.

Desktop añade estas capacidades además de la experiencia estándar de Claude Code:

* [Revisión visual de diferencias](#review-changes-with-diff-view) con comentarios en línea
* [Vista previa de aplicación en vivo](#preview-your-app) con servidores de desarrollo
* [Monitoreo de PR de GitHub](#monitor-pull-request-status) con corrección automática y fusión automática
* [Sesiones paralelas](#work-in-parallel-with-sessions) con aislamiento automático de Git worktrees
* [Tareas programadas](#schedule-recurring-tasks) que ejecutan Claude en un horario recurrente
* [Conectores](#connect-external-tools) para GitHub, Slack, Linear y más
* Entornos locales, [SSH](#ssh-sessions) y [en la nube](#run-long-running-tasks-remotely)

<Tip>
  ¿Nuevo en Desktop? Comience con [Introducción](/es/desktop-quickstart) para instalar la aplicación y realizar su primera edición.
</Tip>

Esta página cubre [trabajar con código](#work-with-code), [gestionar sesiones](#manage-sessions), [extender Claude Code](#extend-claude-code), [tareas programadas](#schedule-recurring-tasks) y [configuración](#environment-configuration). También incluye una [comparación de CLI](#coming-from-the-cli) y [solución de problemas](#troubleshooting).

## Iniciar una sesión

Antes de enviar su primer mensaje, configure cuatro cosas en el área de solicitud:

* **Entorno**: elija dónde se ejecuta Claude. Seleccione **Local** para su máquina, **Remote** para sesiones en la nube alojadas por Anthropic, o una [**conexión SSH**](#ssh-sessions) para una máquina remota que usted administra. Consulte [configuración del entorno](#environment-configuration).
* **Carpeta del proyecto**: seleccione la carpeta o repositorio en el que Claude trabaja. Para sesiones remotas, puede agregar [múltiples repositorios](#run-long-running-tasks-remotely).
* **Modelo**: elija un [modelo](/es/model-config#available-models) del menú desplegable junto al botón de envío. El modelo se bloquea una vez que la sesión comienza.
* **Modo de permisos**: elija cuánta autonomía tiene Claude desde el [selector de modo](#choose-a-permission-mode). Puede cambiar esto durante la sesión.

Escriba su tarea y presione **Enter** para comenzar. Cada sesión rastrea su propio contexto y cambios de forma independiente.

## Trabajar con código

Proporcione a Claude el contexto correcto, controle cuánto hace por su cuenta y revise lo que cambió.

### Usar el cuadro de solicitud

Escriba lo que desea que Claude haga y presione **Enter** para enviar. Claude lee los archivos de su proyecto, realiza cambios y ejecuta comandos según su [modo de permisos](#choose-a-permission-mode). Puede interrumpir a Claude en cualquier momento: haga clic en el botón de parada o escriba su corrección y presione **Enter**. Claude detiene lo que está haciendo y se ajusta según su entrada.

El botón **+** junto al cuadro de solicitud le da acceso a archivos adjuntos, [skills](#use-skills), [conectores](#connect-external-tools) y [plugins](#install-plugins).

### Agregar archivos y contexto a las solicitudes

El cuadro de solicitud admite dos formas de traer contexto externo:

* **Archivos @mention**: escriba `@` seguido de un nombre de archivo para agregar un archivo al contexto de la conversación. Claude puede entonces leer y hacer referencia a ese archivo.
* **Adjuntar archivos**: adjunte imágenes, PDF y otros archivos a su solicitud usando el botón de adjuntos, o arrastre y suelte archivos directamente en la solicitud. Esto es útil para compartir capturas de pantalla de errores, maquetas de diseño o documentos de referencia.

### Elegir un modo de permisos

Los modos de permisos controlan cuánta autonomía tiene Claude durante una sesión: si pregunta antes de editar archivos, ejecutar comandos o ambos. Puede cambiar de modo en cualquier momento usando el selector de modo junto al botón de envío. Comience con Ask permissions para ver exactamente qué hace Claude, luego pase a Auto accept edits o Plan mode a medida que se sienta cómodo.

| Modo                   | Clave de configuración | Comportamiento                                                                                                                                                                                                                                                                                                         |
| ---------------------- | ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ask permissions**    | `default`              | Claude pregunta antes de editar archivos o ejecutar comandos. Usted ve una diferencia y puede aceptar o rechazar cada cambio. Recomendado para nuevos usuarios.                                                                                                                                                        |
| **Auto accept edits**  | `acceptEdits`          | Claude acepta automáticamente ediciones de archivos pero aún pregunta antes de ejecutar comandos de terminal. Use esto cuando confíe en cambios de archivos y desee una iteración más rápida.                                                                                                                          |
| **Plan mode**          | `plan`                 | Claude analiza su código y crea un plan sin modificar archivos ni ejecutar comandos. Bueno para tareas complejas donde desea revisar el enfoque primero.                                                                                                                                                               |
| **Bypass permissions** | `bypassPermissions`    | Claude se ejecuta sin ningún aviso de permisos, equivalente a `--dangerously-skip-permissions` en la CLI. Habilite en su Configuración → Claude Code bajo "Allow bypass permissions mode". Use solo en contenedores o máquinas virtuales sandboxed. Los administradores empresariales pueden deshabilitar esta opción. |

El modo de permisos `dontAsk` está disponible solo en la [CLI](/es/permissions#permission-modes).

<Tip title="Mejor práctica">
  Comience tareas complejas en Plan mode para que Claude mapee un enfoque antes de realizar cambios. Una vez que apruebe el plan, cambie a Auto accept edits o Ask permissions para ejecutarlo. Consulte [explorar primero, luego planificar, luego codificar](/es/best-practices#explore-first-then-plan-then-code) para obtener más información sobre este flujo de trabajo.
</Tip>

Las sesiones remotas admiten Auto accept edits y Plan mode. Ask permissions no está disponible porque las sesiones remotas aceptan automáticamente ediciones de archivos de forma predeterminada, y Bypass permissions no está disponible porque el entorno remoto ya está sandboxed.

Los administradores empresariales pueden restringir qué modos de permisos están disponibles. Consulte [configuración empresarial](#enterprise-configuration) para obtener detalles.

### Vista previa de su aplicación

Claude puede iniciar un servidor de desarrollo y abrir un navegador integrado para verificar sus cambios. Esto funciona tanto para aplicaciones web frontend como para servidores backend: Claude puede probar puntos finales de API, ver registros del servidor e iterar sobre problemas que encuentra. En la mayoría de los casos, Claude inicia el servidor automáticamente después de editar archivos del proyecto. También puede pedirle a Claude que haga una vista previa en cualquier momento. De forma predeterminada, Claude [verifica automáticamente](#auto-verify-changes) cambios después de cada edición.

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

Use los controles deslizantes **Auto-fix** y **Auto-merge** en la barra de estado de CI para habilitar cualquiera de las opciones. Claude Code también envía una notificación de escritorio cuando CI finaliza.

<Note>
  El monitoreo de PR requiere que la [CLI de GitHub (`gh`)](https://cli.github.com/) esté instalada y autenticada en su máquina. Si `gh` no está instalado, Desktop le solicita que lo instale la primera vez que intente crear un PR.
</Note>

## Gestionar sesiones

Cada sesión es una conversación independiente con su propio contexto y cambios. Puede ejecutar múltiples sesiones en paralelo o enviar trabajo a la nube.

### Trabajar en paralelo con sesiones

Haga clic en **+ New session** en la barra lateral para trabajar en múltiples tareas en paralelo. Para repositorios de Git, cada sesión obtiene su propia copia aislada de su proyecto usando [Git worktrees](/es/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees), por lo que los cambios en una sesión no afectan otras sesiones hasta que los confirme.

Los worktrees se almacenan en `<project-root>/.claude/worktrees/` de forma predeterminada. Puede cambiar esto a un directorio personalizado en Configuración → Claude Code bajo "Worktree location". También puede establecer un prefijo de rama que se antepone a cada nombre de rama de worktree, lo que es útil para mantener las ramas creadas por Claude organizadas. Para eliminar un worktree cuando haya terminado, pase el cursor sobre la sesión en la barra lateral y haga clic en el icono de archivo.

<Note>
  El aislamiento de sesión requiere [Git](https://git-scm.com/downloads). La mayoría de las Macs incluyen Git de forma predeterminada. Ejecute `git --version` en Terminal para verificar. En Windows, Git es necesario para que la pestaña Code funcione: [descargue Git para Windows](https://git-scm.com/downloads/win), instálelo y reinicie la aplicación. Si encuentra errores de Git, intente una sesión de Cowork para ayudar a solucionar problemas de su configuración.
</Note>

Use el icono de filtro en la parte superior de la barra lateral para filtrar sesiones por estado (Active, Archived) y entorno (Local, Cloud). Para renombrar una sesión o verificar el uso del contexto, haga clic en el título de la sesión en la barra de herramientas en la parte superior de la sesión activa. Cuando el contexto se llena, Claude resume automáticamente la conversación y continúa trabajando. También puede escribir `/compact` para activar la compresión antes y liberar espacio de contexto. Consulte [la ventana de contexto](/es/how-claude-code-works#the-context-window) para obtener detalles sobre cómo funciona la compresión.

### Ejecutar tareas de larga duración de forma remota

Para refactorizaciones grandes, suites de pruebas, migraciones u otras tareas de larga duración, seleccione **Remote** en lugar de **Local** al iniciar una sesión. Las sesiones remotas se ejecutan en la infraestructura en la nube de Anthropic y continúan incluso si cierra la aplicación o apaga su computadora. Regrese en cualquier momento para ver el progreso o dirigir a Claude en una dirección diferente. También puede monitorear sesiones remotas desde [claude.ai/code](https://claude.ai/code) o la aplicación Claude iOS.

Las sesiones remotas también admiten múltiples repositorios. Después de seleccionar un entorno en la nube, haga clic en el botón **+** junto a la píldora de repositorio para agregar repositorios adicionales a la sesión. Cada repositorio obtiene su propio selector de rama. Esto es útil para tareas que abarcan múltiples bases de código, como actualizar una biblioteca compartida y sus consumidores.

Consulte [Claude Code en la web](/es/claude-code-on-the-web) para obtener más información sobre cómo funcionan las sesiones remotas.

### Continuar en otra superficie

El menú **Continue in**, accesible desde el icono de VS Code en la esquina inferior derecha de la barra de herramientas de la sesión, le permite mover su sesión a otra superficie:

* **Claude Code on the Web**: envía su sesión local para continuar ejecutándose de forma remota. Desktop empuja su rama, genera un resumen de la conversación y crea una nueva sesión remota con el contexto completo. Luego puede elegir archivar la sesión local o mantenerla. Esto requiere un árbol de trabajo limpio y no está disponible para sesiones SSH.
* **Your IDE**: abre su proyecto en un IDE compatible en el directorio de trabajo actual.

## Extender Claude Code

Conecte servicios externos, agregue flujos de trabajo reutilizables, personalice el comportamiento de Claude y configure servidores de vista previa.

### Conectar herramientas externas

Para sesiones locales y [SSH](#ssh-sessions), haga clic en el botón **+** junto al cuadro de solicitud y seleccione **Connectors** para agregar integraciones como Google Calendar, Slack, GitHub, Linear, Notion y más. Puede agregar conectores antes o durante una sesión. Los conectores no están disponibles para sesiones remotas.

Para administrar o desconectar conectores, vaya a Configuración → Connectors en la aplicación de escritorio, o seleccione **Manage connectors** desde el menú Connectors en el cuadro de solicitud.

Una vez conectado, Claude puede leer su calendario, enviar mensajes, crear problemas e interactuar con sus herramientas directamente. Puede preguntarle a Claude qué conectores están configurados en su sesión.

Los conectores son [MCP servers](/es/mcp) con un flujo de configuración gráfico. Úselos para integración rápida con servicios compatibles. Para integraciones no listadas en Connectors, agregue MCP servers manualmente a través de [archivos de configuración](/es/mcp#installing-mcp-servers). También puede [crear conectores personalizados](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp).

### Usar skills

[Skills](/es/skills) extienden lo que Claude puede hacer. Claude los carga automáticamente cuando son relevantes, o puede invocar uno directamente: escriba `/` en el cuadro de solicitud o haga clic en el botón **+** y seleccione **Slash commands** para ver lo que está disponible. Esto incluye [comandos integrados](/es/commands), sus [skills personalizados](/es/skills#create-custom-skills), skills del proyecto desde su base de código y skills de cualquier [plugin instalado](/es/plugins). Seleccione uno y aparecerá resaltado en el campo de entrada. Escriba su tarea después de él y envíe como de costumbre.

### Instalar plugins

[Plugins](/es/plugins) son paquetes reutilizables que agregan skills, agents, hooks, MCP servers y configuraciones LSP a Claude Code. Puede instalar plugins desde la aplicación de escritorio sin usar la terminal.

Para sesiones locales y [SSH](#ssh-sessions), haga clic en el botón **+** junto al cuadro de solicitud y seleccione **Plugins** para ver sus plugins instalados y sus comandos. Para agregar un plugin, seleccione **Add plugin** del submenú para abrir el navegador de plugins, que muestra plugins disponibles desde sus [marketplaces](/es/plugin-marketplaces) configurados incluyendo el marketplace oficial de Anthropic. Seleccione **Manage plugins** para habilitar, deshabilitar o desinstalar plugins.

Los plugins pueden estar limitados a su cuenta de usuario, un proyecto específico o solo locales. Los plugins no están disponibles para sesiones remotas. Para la referencia completa de plugins incluyendo crear sus propios plugins, consulte [plugins](/es/plugins).

### Configurar servidores de vista previa

Claude detecta automáticamente su configuración de servidor de desarrollo y almacena la configuración en `.claude/launch.json` en la raíz de la carpeta que seleccionó al iniciar la sesión. Preview usa esta carpeta como su directorio de trabajo, por lo que si seleccionó una carpeta principal, las subcarpetas con sus propios servidores de desarrollo no se detectarán automáticamente. Para trabajar con el servidor de una subcarpeta, inicie una sesión en esa carpeta directamente o agregue una configuración manualmente.

Para personalizar cómo se inicia su servidor, por ejemplo para usar `yarn dev` en lugar de `npm run dev` o para cambiar el puerto, edite el archivo manualmente o haga clic en **Edit configuration** en el menú desplegable Preview para abrirlo en su editor de código. El archivo admite JSON con comentarios.

```json  theme={null}
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

```json  theme={null}
{
  "version": "0.0.1",
  "autoVerify": false,
  "configurations": [...]
}
```

Cuando está deshabilitado, las herramientas de vista previa aún están disponibles y puede pedirle a Claude que verifique en cualquier momento. Auto-verify lo hace automático después de cada edición.

#### Campos de configuración

Cada entrada en el array `configurations` acepta los siguientes campos:

| Campo               | Tipo      | Descripción                                                                                                                                                                                                                                          |
| ------------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`              | string    | Un identificador único para este servidor                                                                                                                                                                                                            |
| `runtimeExecutable` | string    | El comando a ejecutar, como `npm`, `yarn` o `node`                                                                                                                                                                                                   |
| `runtimeArgs`       | string\[] | Argumentos pasados a `runtimeExecutable`, como `["run", "dev"]`                                                                                                                                                                                      |
| `port`              | number    | El puerto en el que escucha su servidor. Por defecto es 3000                                                                                                                                                                                         |
| `cwd`               | string    | Directorio de trabajo relativo a la raíz de su proyecto. Por defecto es la raíz del proyecto. Use `${workspaceFolder}` para hacer referencia a la raíz del proyecto explícitamente                                                                   |
| `env`               | object    | Variables de entorno adicionales como pares clave-valor, como `{ "NODE_ENV": "development" }`. No ponga secretos aquí ya que este archivo se confirma en su repositorio. Los secretos establecidos en su perfil de shell se heredan automáticamente. |
| `autoPort`          | boolean   | Cómo manejar conflictos de puerto. Consulte a continuación                                                                                                                                                                                           |
| `program`           | string    | Un script a ejecutar con `node`. Consulte [cuándo usar `program` vs `runtimeExecutable`](#when-to-use-program-vs-runtimeexecutable)                                                                                                                  |
| `args`              | string\[] | Argumentos pasados a `program`. Solo se usa cuando `program` está establecido                                                                                                                                                                        |

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

    ```json  theme={null}
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

    ```json  theme={null}
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

    ```json  theme={null}
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

## Programar tareas recurrentes

Las tareas programadas inician una nueva sesión local automáticamente en una hora y frecuencia que usted elige. Úselas para trabajo recurrente como revisiones de código diarias, verificaciones de actualización de dependencias o resúmenes matutinos que extraigan de su calendario e bandeja de entrada.

Las tareas se ejecutan en su máquina, por lo que la aplicación de escritorio debe estar abierta y su computadora despierta para que se ejecuten. Consulte [Cómo se ejecutan las tareas programadas](#how-scheduled-tasks-run) para obtener detalles sobre ejecuciones perdidas y comportamiento de recuperación.

<Note>
  De forma predeterminada, las tareas programadas se ejecutan contra cualquier estado en el que se encuentre su directorio de trabajo, incluyendo cambios no confirmados. Habilite el control deslizante de worktree en la entrada de solicitud para dar a cada ejecución su propio worktree de Git aislado, de la misma manera que [sesiones paralelas](#work-in-parallel-with-sessions) funcionan.
</Note>

Para crear una tarea programada, haga clic en **Schedule** en la barra lateral, luego **+ New task**. Configure estos campos:

| Campo       | Descripción                                                                                                                                                                                                                                                                 |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Name        | Identificador para la tarea. Se convierte a kebab-case en minúsculas y se usa como nombre de carpeta en disco. Debe ser único en todas sus tareas.                                                                                                                          |
| Description | Resumen corto mostrado en la lista de tareas.                                                                                                                                                                                                                               |
| Prompt      | Las instrucciones enviadas a Claude cuando se ejecuta la tarea. Escriba esto de la misma manera que escribiría cualquier mensaje en el cuadro de solicitud. La entrada de solicitud también incluye controles para modelo, modo de permisos, carpeta de trabajo y worktree. |
| Frequency   | Con qué frecuencia se ejecuta la tarea. Consulte [opciones de frecuencia](#frequency-options) a continuación.                                                                                                                                                               |

También puede crear una tarea describiendo lo que desea en cualquier sesión. Por ejemplo, "configurar una revisión de código diaria que se ejecute cada mañana a las 9am."

### Opciones de frecuencia

* **Manual**: sin horario, solo se ejecuta cuando hace clic en **Run now**. Útil para guardar una solicitud que activa bajo demanda
* **Hourly**: se ejecuta cada hora. Cada tarea obtiene un desplazamiento fijo de hasta 10 minutos desde la parte superior de la hora para escalonar el tráfico de API
* **Daily**: muestra un selector de hora, por defecto a las 9:00 AM hora local
* **Weekdays**: igual que Daily pero omite sábado y domingo
* **Weekly**: muestra un selector de hora y un selector de día

Para intervalos que el selector no ofrece (cada 15 minutos, primer día de cada mes, etc.), pídale a Claude en cualquier sesión de Desktop que establezca el horario. Use lenguaje natural; por ejemplo, "programar una tarea para ejecutar todas las pruebas cada 6 horas."

### Cómo se ejecutan las tareas programadas

Las tareas programadas se ejecutan localmente en su máquina. Desktop verifica el horario cada minuto mientras la aplicación está abierta e inicia una sesión nueva cuando una tarea vence, independientemente de cualquier sesión manual que tenga abierta. Cada tarea obtiene un retraso fijo de hasta 10 minutos después de la hora programada para escalonar el tráfico de API. El retraso es determinista: la misma tarea siempre comienza en el mismo desplazamiento.

Cuando se ejecuta una tarea, obtiene una notificación de escritorio y aparece una nueva sesión bajo una sección **Scheduled** en la barra lateral. Ábrala para ver qué hizo Claude, revisar cambios o responder a solicitudes de permisos. La sesión funciona como cualquier otra: Claude puede editar archivos, ejecutar comandos, crear confirmaciones y abrir solicitudes de extracción.

Las tareas solo se ejecutan mientras la aplicación de escritorio está en ejecución y su computadora está despierta. Si su computadora se duerme durante una hora programada, la ejecución se omite. Para evitar el sueño inactivo, habilite **Keep computer awake** en Configuración bajo **Desktop app → General**. Cerrar la tapa del portátil aún lo pone a dormir.

### Ejecuciones perdidas

Cuando la aplicación se inicia o su computadora se despierta, Desktop verifica si cada tarea perdió alguna ejecución en los últimos siete días. Si lo hizo, Desktop inicia exactamente una ejecución de recuperación para la hora más recientemente perdida y descarta cualquier cosa más antigua. Una tarea diaria que perdió seis días se ejecuta una vez al despertar. Desktop muestra una notificación cuando comienza una ejecución de recuperación.

Tenga esto en cuenta al escribir solicitudes. Una tarea programada para las 9am podría ejecutarse a las 11pm si su computadora estuvo dormida todo el día. Si el tiempo es importante, agregue protecciones a la solicitud misma, por ejemplo: "Solo revise las confirmaciones de hoy. Si es después de las 5pm, omita la revisión y solo publique un resumen de lo que se perdió."

### Permisos para tareas programadas

Cada tarea tiene su propio modo de permisos, que establece al crear o editar la tarea. Las reglas de permitir de `~/.claude/settings.json` también se aplican a sesiones de tareas programadas. Si una tarea se ejecuta en modo Ask y necesita ejecutar una herramienta para la que no tiene permiso, la ejecución se detiene hasta que la apruebe. La sesión permanece abierta en la barra lateral para que pueda responder más tarde.

Para evitar detenciones, haga clic en **Run now** después de crear una tarea, observe solicitudes de permisos y seleccione "always allow" para cada una. Las ejecuciones futuras de esa tarea aprueban automáticamente las mismas herramientas sin solicitar. Puede revisar y revocar estas aprobaciones desde la página de detalles de la tarea.

### Gestionar tareas programadas

Haga clic en una tarea en la lista **Schedule** para abrir su página de detalles. Desde aquí puede:

* **Run now**: inicie la tarea inmediatamente sin esperar la próxima hora programada
* **Toggle repeats**: pause o reanude ejecuciones programadas sin eliminar la tarea
* **Edit**: cambie la solicitud, frecuencia, carpeta u otras configuraciones
* **Review history**: vea cada ejecución pasada, incluyendo las que se omitieron porque su computadora estaba dormida
* **Review allowed permissions**: vea y revoque aprobaciones de herramientas guardadas para esta tarea desde el panel **Always allowed**
* **Delete**: elimine la tarea y archive todas las sesiones que creó

También puede gestionar tareas pidiendo a Claude en cualquier sesión de Desktop. Por ejemplo, "pause my dependency-audit task", "delete the standup-prep task" o "show me my scheduled tasks."

Para editar la solicitud de una tarea en disco, abra `~/.claude/scheduled-tasks/<task-name>/SKILL.md` (o bajo [`CLAUDE_CONFIG_DIR`](/es/env-vars) si está establecido). El archivo usa frontmatter YAML para `name` y `description`, con la solicitud como cuerpo. Los cambios surten efecto en la próxima ejecución. El horario, carpeta, modelo y estado habilitado no están en este archivo: cámbielos a través del formulario Edit o pídale a Claude.

## Configuración del entorno

El entorno que elige al [iniciar una sesión](#start-a-session) determina dónde Claude se ejecuta y cómo se conecta:

* **Local**: se ejecuta en su máquina con acceso directo a sus archivos
* **Remote**: se ejecuta en la infraestructura en la nube de Anthropic. Las sesiones continúan incluso si cierra la aplicación.
* **SSH**: se ejecuta en una máquina remota a la que se conecta a través de SSH, como sus propios servidores, máquinas virtuales en la nube o contenedores de desarrollo

### Sesiones locales

Las sesiones locales heredan variables de entorno de su shell. Si necesita variables adicionales, establézcalas en su perfil de shell, como `~/.zshrc` o `~/.bashrc`, y reinicie la aplicación de escritorio. Consulte [variables de entorno](/es/env-vars) para la lista completa de variables compatibles.

[Extended thinking](/es/common-workflows#use-extended-thinking-thinking-mode) está habilitado de forma predeterminada, lo que mejora el rendimiento en tareas de razonamiento complejo pero usa tokens adicionales. Para deshabilitar el pensamiento por completo, establezca `MAX_THINKING_TOKENS=0` en su perfil de shell. En Opus, `MAX_THINKING_TOKENS` se ignora excepto para `0` porque el razonamiento adaptativo controla la profundidad del pensamiento en su lugar.

### Sesiones remotas

Las sesiones remotas continúan en segundo plano incluso si cierra la aplicación. El uso cuenta hacia los límites de su [plan de suscripción](/es/costs) sin cargos de computación separados.

Puede crear entornos en la nube personalizados con diferentes niveles de acceso a la red y variables de entorno. Seleccione el menú desplegable de entorno al iniciar una sesión remota y elija **Add environment**. Consulte [entornos en la nube](/es/claude-code-on-the-web#cloud-environment) para obtener detalles sobre la configuración del acceso a la red y variables de entorno.

### Sesiones SSH

Las sesiones SSH le permiten ejecutar Claude Code en una máquina remota mientras usa la aplicación de escritorio como su interfaz. Esto es útil para trabajar con bases de código que viven en máquinas virtuales en la nube, contenedores de desarrollo o servidores con hardware o dependencias específicas.

Para agregar una conexión SSH, haga clic en el menú desplegable de entorno antes de iniciar una sesión y seleccione **+ Add SSH connection**. El diálogo solicita:

* **Name**: una etiqueta amigable para esta conexión
* **SSH Host**: `user@hostname` o un host definido en `~/.ssh/config`
* **SSH Port**: por defecto es 22 si se deja vacío, o usa el puerto de su configuración SSH
* **Identity File**: ruta a su clave privada, como `~/.ssh/id_rsa`. Déjelo vacío para usar la clave predeterminada o su configuración SSH.

Una vez agregada, la conexión aparece en el menú desplegable de entorno. Selecciónela para iniciar una sesión en esa máquina. Claude se ejecuta en la máquina remota con acceso a sus archivos y herramientas.

Claude Code debe estar instalado en la máquina remota. Una vez conectado, las sesiones SSH admiten modos de permisos, conectores, plugins y MCP servers.

## Configuración empresarial

Las organizaciones en planes Teams o Enterprise pueden gestionar el comportamiento de la aplicación de escritorio a través de controles de consola de administración, archivos de configuración administrados y políticas de gestión de dispositivos.

### Controles de consola de administración

Estas configuraciones se configuran a través de la [consola de configuración de administración](https://claude.ai/admin-settings/claude-code):

* **Habilitar o deshabilitar la pestaña Code**: controle si los usuarios en su organización pueden acceder a Claude Code en la aplicación de escritorio
* **Deshabilitar modo Bypass permissions**: evite que los usuarios en su organización habiliten el modo bypass permissions
* **Deshabilitar Claude Code en la web**: habilite o deshabilite sesiones remotas para su organización

### Configuración administrada

La configuración administrada anula la configuración del proyecto y usuario y se aplica cuando Desktop genera sesiones de CLI. Puede establecer estas claves en el archivo de [configuración administrada](/es/settings#settings-precedence) de su organización o enviarlas de forma remota a través de la consola de administración.

| Clave                          | Descripción                                                                                                                                                                |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `disableBypassPermissionsMode` | establezca en `"disable"` para evitar que los usuarios habiliten el modo bypass permissions. Consulte [configuración administrada](/es/permissions#managed-only-settings). |

Para la lista completa de configuraciones solo administradas incluyendo `allowManagedPermissionRulesOnly` y `allowManagedHooksOnly`, consulte [configuraciones solo administradas](/es/permissions#managed-only-settings).

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
  Cuándo usar Desktop vs CLI: use Desktop cuando desee revisión visual de diferencias, archivos adjuntos o gestión de sesiones en una barra lateral. Use la CLI cuando necesite scripting, automatización, proveedores de terceros o prefiera un flujo de trabajo de terminal.
</Tip>

### Equivalentes de banderas de CLI

Esta tabla muestra el equivalente de la aplicación de escritorio para banderas de CLI comunes. Las banderas no listadas no tienen equivalente de escritorio porque están diseñadas para scripting o automatización.

| CLI                                       | Equivalente de Desktop                                                                                                                                                        |
| ----------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--model sonnet`                          | menú desplegable de modelo junto al botón de envío, antes de iniciar una sesión                                                                                               |
| `--resume`, `--continue`                  | haga clic en una sesión en la barra lateral                                                                                                                                   |
| `--permission-mode`                       | selector de modo junto al botón de envío                                                                                                                                      |
| `--dangerously-skip-permissions`          | Modo Bypass permissions. Habilite en Configuración → Claude Code → "Allow bypass permissions mode". Los administradores empresariales pueden deshabilitar esta configuración. |
| `--add-dir`                               | agregue múltiples repositorios con el botón **+** en sesiones remotas                                                                                                         |
| `--allowedTools`, `--disallowedTools`     | no disponible en Desktop                                                                                                                                                      |
| `--verbose`                               | no disponible. Verifique registros del sistema: Console.app en macOS, Event Viewer → Windows Logs → Application en Windows                                                    |
| `--print`, `--output-format`              | no disponible. Desktop es solo interactivo.                                                                                                                                   |
| Variable de entorno `ANTHROPIC_MODEL`     | menú desplegable de modelo junto al botón de envío                                                                                                                            |
| Variable de entorno `MAX_THINKING_TOKENS` | establezca en perfil de shell; se aplica a sesiones locales. Consulte [configuración del entorno](#environment-configuration).                                                |

### Configuración compartida

Desktop y CLI leen los mismos archivos de configuración, por lo que su configuración se transfiere:

* Los archivos **[CLAUDE.md](/es/memory)** en su proyecto son utilizados por ambos
* Los **[MCP servers](/es/mcp)** configurados en `~/.claude.json` o `.mcp.json` funcionan en ambos
* Los **[Hooks](/es/hooks)** y **[skills](/es/skills)** definidos en configuración se aplican a ambos
* La **[Configuración](/es/settings)** en `~/.claude.json` y `~/.claude/settings.json` se comparte. Las reglas de permisos, herramientas permitidas y otras configuraciones en `settings.json` se aplican a sesiones de Desktop.
* **Modelos**: Sonnet, Opus y Haiku están disponibles en ambos. En Desktop, seleccione el modelo del menú desplegable junto al botón de envío antes de iniciar una sesión. No puede cambiar el modelo durante una sesión activa.

<Note>
  **MCP servers: aplicación de chat de Desktop vs Claude Code**: Los MCP servers configurados para la aplicación de chat de Claude Desktop en `claude_desktop_config.json` son separados de Claude Code y no aparecerán en la pestaña Code. Para usar MCP servers en Claude Code, configúrelos en `~/.claude.json` o en el archivo `.mcp.json` de su proyecto. Consulte [configuración de MCP](/es/mcp#installing-mcp-servers) para obtener detalles.
</Note>

### Comparación de características

Esta tabla compara capacidades principales entre la CLI y Desktop. Para una lista completa de banderas de CLI, consulte la [referencia de CLI](/es/cli-reference).

| Característica                                          | CLI                                                       | Desktop                                                                                            |
| ------------------------------------------------------- | --------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Modos de permisos                                       | todos los modos incluyendo `dontAsk`                      | Ask permissions, Auto accept edits, Plan mode y Bypass permissions a través de Configuración       |
| `--dangerously-skip-permissions`                        | Bandera de CLI                                            | Modo Bypass permissions. Habilite en Configuración → Claude Code → "Allow bypass permissions mode" |
| [Proveedores de terceros](/es/third-party-integrations) | Bedrock, Vertex, Foundry                                  | no disponible. Desktop se conecta directamente a la API de Anthropic.                              |
| [MCP servers](/es/mcp)                                  | configurar en archivos de configuración                   | UI de Connectors para sesiones locales y SSH, o archivos de configuración                          |
| [Plugins](/es/plugins)                                  | comando `/plugin`                                         | UI del administrador de plugins                                                                    |
| Archivos @mention                                       | basado en texto                                           | con autocompletado                                                                                 |
| Archivos adjuntos                                       | no disponible                                             | imágenes, PDF                                                                                      |
| Aislamiento de sesión                                   | bandera [`--worktree`](/es/cli-reference)                 | worktrees automáticos                                                                              |
| Múltiples sesiones                                      | terminales separadas                                      | pestañas de barra lateral                                                                          |
| Tareas recurrentes                                      | trabajos cron, tuberías de CI                             | [tareas programadas](#schedule-recurring-tasks)                                                    |
| Scripting y automatización                              | [`--print`](/es/cli-reference), [Agent SDK](/es/headless) | no disponible                                                                                      |

### Lo que no está disponible en Desktop

Las siguientes características están disponibles solo en la CLI o extensión de VS Code:

* **Proveedores de terceros**: Desktop se conecta directamente a la API de Anthropic. Use la [CLI](/es/quickstart) con Bedrock, Vertex o Foundry en su lugar.
* **Linux**: la aplicación de escritorio está disponible solo en macOS y Windows.
* **Sugerencias de código en línea**: Desktop no proporciona sugerencias de estilo autocompletado. Funciona a través de solicitudes conversacionales y cambios de código explícitos.
* **Equipos de agentes**: la orquestación de múltiples agentes está disponible a través de la [CLI](/es/agent-teams) y [Agent SDK](/es/headless), no en Desktop.

## Solución de problemas

### Verificar su versión

Para ver qué versión de la aplicación de escritorio está ejecutando:

* **macOS**: haga clic en **Claude** en la barra de menú, luego **About Claude**
* **Windows**: haga clic en **Help**, luego **About**

Haga clic en el número de versión para copiarlo a su portapapeles.

### Errores 403 o de autenticación en la pestaña Code

Si ve `Error 403: Forbidden` u otros fallos de autenticación al usar la pestaña Code:

1. Cierre sesión e inicie sesión nuevamente desde el menú de la aplicación. Esta es la solución más común.
2. Verifique que tenga una suscripción de pago activa: Pro, Max, Teams o Enterprise.
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
* **ARM64**: los dispositivos Windows ARM64 son totalmente compatibles.

### Pestaña Cowork no disponible en Macs Intel

La pestaña Cowork requiere Apple Silicon (M1 o posterior) en macOS. En Windows, Cowork está disponible en todo el hardware compatible. Las pestañas Chat y Code funcionan normalmente en Macs Intel.

### "Branch doesn't exist yet" al abrir en CLI

Las sesiones remotas pueden crear ramas que no existen en su máquina local. Haga clic en el nombre de la rama en la barra de herramientas de la sesión para copiarlo, luego obténgalo localmente:

```bash  theme={null}
git fetch origin <branch-name>
git checkout <branch-name>
```

### ¿Aún atascado?

* Busque o presente un error en [GitHub Issues](https://github.com/anthropics/claude-code/issues)
* Visite el [centro de soporte de Claude](https://support.claude.com/)

Al presentar un error, incluya la versión de su aplicación de escritorio, su sistema operativo, el mensaje de error exacto y registros relevantes. En macOS, verifique Console.app. En Windows, verifique Event Viewer → Windows Logs → Application.
