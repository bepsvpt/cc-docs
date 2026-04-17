> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Continúe sesiones locales desde cualquier dispositivo con Remote Control

> Continúe una sesión local de Claude Code desde su teléfono, tableta o cualquier navegador usando Remote Control. Funciona con claude.ai/code y la aplicación móvil de Claude.

<Note>
  Remote Control está disponible en todos los planes. En Team y Enterprise, está deshabilitado de forma predeterminada hasta que un administrador habilite el botón de alternancia de Remote Control en [configuración de administración de Claude Code](https://claude.ai/admin-settings/claude-code).
</Note>

Remote Control conecta [claude.ai/code](https://claude.ai/code) o la aplicación Claude para [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) y [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) a una sesión de Claude Code que se ejecuta en su máquina. Inicie una tarea en su escritorio y luego continúela desde su teléfono en el sofá o desde un navegador en otra computadora.

Cuando inicia una sesión de Remote Control en su máquina, Claude sigue ejecutándose localmente todo el tiempo, por lo que nada se mueve a la nube. Con Remote Control puede:

* **Usar su entorno local completo de forma remota**: su sistema de archivos, [MCP servers](/es/mcp), herramientas y configuración del proyecto permanecen disponibles
* **Trabajar desde ambas superficies a la vez**: la conversación se mantiene sincronizada en todos los dispositivos conectados, por lo que puede enviar mensajes desde su terminal, navegador y teléfono indistintamente
* **Sobrevivir a interrupciones**: si su portátil se duerme o su red se cae, la sesión se reconecta automáticamente cuando su máquina vuelve a estar en línea

A diferencia de [Claude Code en la web](/es/claude-code-on-the-web), que se ejecuta en infraestructura en la nube, las sesiones de Remote Control se ejecutan directamente en su máquina e interactúan con su sistema de archivos local. Las interfaces web y móvil son solo una ventana a esa sesión local.

<Note>
  Remote Control requiere Claude Code v2.1.51 o posterior. Verifique su versión con `claude --version`.
</Note>

Esta página cubre la configuración, cómo iniciar y conectarse a sesiones, y cómo Remote Control se compara con Claude Code en la web.

## Requisitos

Antes de usar Remote Control, confirme que su entorno cumple con estas condiciones:

* **Suscripción**: disponible en planes Pro, Max, Team y Enterprise. Las claves API no son compatibles. En Team y Enterprise, un administrador debe habilitar primero el botón de alternancia de Remote Control en [configuración de administración de Claude Code](https://claude.ai/admin-settings/claude-code).
* **Autenticación**: ejecute `claude` y use `/login` para iniciar sesión a través de claude.ai si aún no lo ha hecho.
* **Confianza del espacio de trabajo**: ejecute `claude` en su directorio de proyecto al menos una vez para aceptar el diálogo de confianza del espacio de trabajo.

## Inicie una sesión de Remote Control

Puede iniciar una sesión de Remote Control desde la CLI o la extensión de VS Code. La CLI ofrece tres modos de invocación; VS Code usa el comando `/remote-control`.

<Tabs>
  <Tab title="Modo servidor">
    Navegue a su directorio de proyecto y ejecute:

    ```bash theme={null}
    claude remote-control
    ```

    El proceso sigue ejecutándose en su terminal en modo servidor, esperando conexiones remotas. Muestra una URL de sesión que puede usar para [conectarse desde otro dispositivo](#connect-from-another-device), y puede presionar la barra espaciadora para mostrar un código QR para acceso rápido desde su teléfono. Mientras una sesión remota está activa, la terminal muestra el estado de la conexión y la actividad de las herramientas.

    Banderas disponibles:

    | Bandera                                         | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
    | ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `--name "My Project"`                           | Establezca un título de sesión personalizado visible en la lista de sesiones en claude.ai/code.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
    | `--remote-control-session-name-prefix <prefix>` | Prefijo para nombres de sesión generados automáticamente cuando no se establece un nombre explícito. El valor predeterminado es el nombre de host de su máquina, produciendo nombres como `myhost-graceful-unicorn`. Establezca `CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX` para el mismo efecto.                                                                                                                                                                                                                                                                                                                      |
    | `--spawn <mode>`                                | Cómo el servidor crea sesiones.<br />• `same-dir` (predeterminado): todas las sesiones comparten el directorio de trabajo actual, por lo que pueden entrar en conflicto si editan los mismos archivos.<br />• `worktree`: cada sesión bajo demanda obtiene su propio [git worktree](/es/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees). Requiere un repositorio git.<br />• `session`: modo de sesión única. Sirve exactamente una sesión y rechaza conexiones adicionales. Se establece solo al inicio.<br />Presione `w` en tiempo de ejecución para alternar entre `same-dir` y `worktree`. |
    | `--capacity <N>`                                | Número máximo de sesiones concurrentes. El valor predeterminado es 32. No se puede usar con `--spawn=session`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
    | `--verbose`                                     | Mostrar registros detallados de conexión y sesión.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
    | `--sandbox` / `--no-sandbox`                    | Habilitar o deshabilitar [sandboxing](/es/sandboxing) para aislamiento del sistema de archivos y red. Deshabilitado de forma predeterminada.                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
  </Tab>

  <Tab title="Sesión interactiva">
    Para iniciar una sesión normal interactiva de Claude Code con Remote Control habilitado, use la bandera `--remote-control` (o `--rc`):

    ```bash theme={null}
    claude --remote-control
    ```

    Opcionalmente, pase un nombre para la sesión:

    ```bash theme={null}
    claude --remote-control "My Project"
    ```

    Esto le proporciona una sesión interactiva completa en su terminal que también puede controlar desde claude.ai o la aplicación Claude. A diferencia de `claude remote-control` (modo servidor), puede escribir mensajes localmente mientras la sesión también está disponible de forma remota.
  </Tab>

  <Tab title="Desde una sesión existente">
    Si ya está en una sesión de Claude Code y desea continuarla de forma remota, use el comando `/remote-control` (o `/rc`):

    ```text theme={null}
    /remote-control
    ```

    Pase un nombre como argumento para establecer un título de sesión personalizado:

    ```text theme={null}
    /remote-control My Project
    ```

    Esto inicia una sesión de Remote Control que lleva su historial de conversación actual y muestra una URL de sesión y código QR que puede usar para [conectarse desde otro dispositivo](#connect-from-another-device). Las banderas `--verbose`, `--sandbox` y `--no-sandbox` no están disponibles con este comando.
  </Tab>

  <Tab title="VS Code">
    En la [extensión de VS Code de Claude Code](/es/vs-code), escriba `/remote-control` o `/rc` en el cuadro de solicitud, o abra el menú de comandos con `/` y selecciónelo. Requiere Claude Code v2.1.79 o posterior.

    ```text theme={null}
    /remote-control
    ```

    Un banner aparece encima del cuadro de solicitud mostrando el estado de la conexión. Una vez conectado, haga clic en **Open in browser** en el banner para ir directamente a la sesión, o encuéntrela en la lista de sesiones en [claude.ai/code](https://claude.ai/code). La URL de la sesión también se publica en la conversación.

    Para desconectarse, haga clic en el icono de cierre en el banner o ejecute `/remote-control` nuevamente.

    A diferencia de la CLI, el comando de VS Code no acepta un argumento de nombre ni muestra un código QR. El título de la sesión se deriva del historial de conversación o del primer mensaje.
  </Tab>
</Tabs>

### Conectarse desde otro dispositivo

Una vez que una sesión de Remote Control está activa, tiene varias formas de conectarse desde otro dispositivo:

* **Abra la URL de la sesión** en cualquier navegador para ir directamente a la sesión en [claude.ai/code](https://claude.ai/code).
* **Escanee el código QR** que se muestra junto a la URL de la sesión para abrirlo directamente en la aplicación Claude. Con `claude remote-control`, presione la barra espaciadora para alternar la visualización del código QR.
* **Abra [claude.ai/code](https://claude.ai/code) o la aplicación Claude** y encuentre la sesión por nombre en la lista de sesiones. Las sesiones de Remote Control muestran un icono de computadora con un punto de estado verde cuando están en línea.

El título de la sesión remota se elige en este orden:

1. El nombre que pasó a `--name`, `--remote-control`, o `/remote-control`
2. El título que estableció con `/rename`
3. El último mensaje significativo en el historial de conversación existente
4. Un nombre generado automáticamente como `myhost-graceful-unicorn`, donde `myhost` es el nombre de host de su máquina o el prefijo que estableció con `--remote-control-session-name-prefix`

Si no estableció un nombre explícito, el título se actualiza para reflejar su solicitud una vez que envíe una.

Si el entorno ya tiene una sesión activa, se le preguntará si desea continuarla o iniciar una nueva.

Si aún no tiene la aplicación Claude, use el comando `/mobile` dentro de Claude Code para mostrar un código QR de descarga para [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) o [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude).

### Habilite Remote Control para todas las sesiones

De forma predeterminada, Remote Control solo se activa cuando ejecuta explícitamente `claude remote-control`, `claude --remote-control`, o `/remote-control`. Para habilitarlo automáticamente para cada sesión interactiva, ejecute `/config` dentro de Claude Code y establezca **Enable Remote Control for all sessions** en `true`. Establézcalo de nuevo en `false` para deshabilitar.

Con esta configuración activada, cada proceso interactivo de Claude Code registra una sesión remota. Si ejecuta varias instancias, cada una obtiene su propio entorno y sesión. Para ejecutar varias sesiones concurrentes desde un único proceso, use el [modo servidor](#start-a-remote-control-session) en su lugar.

## Conexión y seguridad

Su sesión local de Claude Code realiza solo solicitudes HTTPS salientes y nunca abre puertos entrantes en su máquina. Cuando inicia Remote Control, se registra con la API de Anthropic y sondea el trabajo. Cuando se conecta desde otro dispositivo, el servidor enruta mensajes entre el cliente web o móvil y su sesión local a través de una conexión de transmisión.

Todo el tráfico viaja a través de la API de Anthropic sobre TLS, el mismo transporte de seguridad que cualquier sesión de Claude Code. La conexión utiliza múltiples credenciales de corta duración, cada una limitada a un único propósito y expirando de forma independiente.

## Remote Control vs Claude Code en la web

Remote Control y [Claude Code en la web](/es/claude-code-on-the-web) ambos usan la interfaz claude.ai/code. La diferencia clave es dónde se ejecuta la sesión: Remote Control se ejecuta en su máquina, por lo que sus MCP servers locales, herramientas y configuración del proyecto permanecen disponibles. Claude Code en la web se ejecuta en infraestructura en la nube administrada por Anthropic.

Use Remote Control cuando esté en medio del trabajo local y desee continuar desde otro dispositivo. Use Claude Code en la web cuando desee iniciar una tarea sin ninguna configuración local, trabajar en un repositorio que no tiene clonado, o ejecutar varias tareas en paralelo.

## Notificaciones push móviles

Cuando Remote Control está activo, Claude puede enviar notificaciones push a su teléfono.

Claude decide cuándo enviar. Típicamente envía una cuando una tarea de larga duración finaliza o cuando necesita una decisión de usted para continuar. También puede solicitar un push en su solicitud, por ejemplo `notify me when the tests finish`. Más allá del botón de alternancia activado/desactivado a continuación, no hay configuración por evento.

<Note>
  Las notificaciones push móviles requieren Claude Code v2.1.110 o posterior.
</Note>

Para configurar notificaciones push móviles:

<Steps>
  <Step title="Instale la aplicación móvil Claude">
    Descargue la aplicación Claude para [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) o [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude).
  </Step>

  <Step title="Inicie sesión con su cuenta de Claude Code">
    Use la misma cuenta y organización que usa para Claude Code en la terminal.
  </Step>

  <Step title="Permita notificaciones">
    Acepte el mensaje de solicitud de permiso de notificación del sistema operativo.
  </Step>

  <Step title="Habilite push en Claude Code">
    En su terminal, ejecute `/config` y habilite **Push when Claude decides**.
  </Step>
</Steps>

Si las notificaciones no llegan:

* Si `/config` muestra **No mobile registered**, abra la aplicación Claude en su teléfono para que pueda actualizar su token push. La advertencia se borra la próxima vez que Remote Control se conecte.
* En iOS, los modos Focus y los resúmenes de notificaciones pueden suprimir o retrasar los pushes. Verifique Configuración → Notificaciones → Claude.
* En Android, la optimización agresiva de batería puede retrasar la entrega. Exima la aplicación Claude de la optimización de batería en la configuración del sistema.

## Limitaciones

* **Una sesión remota por proceso interactivo**: fuera del modo servidor, cada instancia de Claude Code admite una sesión remota a la vez. Use el [modo servidor](#start-a-remote-control-session) para ejecutar varias sesiones concurrentes desde un único proceso.
* **El proceso local debe seguir ejecutándose**: Remote Control se ejecuta como un proceso local. Si cierra la terminal, cierra VS Code, o detiene el proceso `claude` de otra manera, la sesión finaliza.
* **Interrupción de red extendida**: si su máquina está despierta pero no puede alcanzar la red durante más de aproximadamente 10 minutos, la sesión agota el tiempo de espera y el proceso se cierra. Ejecute `claude remote-control` nuevamente para iniciar una nueva sesión.
* **Ultraplan desconecta Remote Control**: iniciar una sesión de [ultraplan](/es/ultraplan) desconecta cualquier sesión de Remote Control activa porque ambas características ocupan la interfaz claude.ai/code y solo una puede estar conectada a la vez.

## Solución de problemas

### "Remote Control requires a claude.ai subscription"

No está autenticado con una cuenta de claude.ai. Ejecute `claude auth login` y elija la opción de claude.ai. Si `ANTHROPIC_API_KEY` está configurado en su entorno, desactívelo primero.

### "Remote Control requires a full-scope login token"

Está autenticado con un token de larga duración de `claude setup-token` o la variable de entorno `CLAUDE_CODE_OAUTH_TOKEN`. Estos tokens se limitan a solo inferencia y no pueden establecer sesiones de Remote Control. Ejecute `claude auth login` para autenticarse con un token de sesión de alcance completo en su lugar.

### "Unable to determine your organization for Remote Control eligibility"

Su información de cuenta en caché está obsoleta o incompleta. Ejecute `claude auth login` para actualizarla.

### "Remote Control is not yet enabled for your account"

La verificación de elegibilidad puede fallar con ciertas variables de entorno presentes:

* `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` o `DISABLE_TELEMETRY`: desactívelas e intente de nuevo.
* `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX`, o `CLAUDE_CODE_USE_FOUNDRY`: Remote Control requiere autenticación de claude.ai y no funciona con proveedores de terceros.

Si ninguno de estos está configurado, ejecute `/logout` luego `/login` para actualizar.

### "Remote Control is disabled by your organization's policy"

Este error tiene tres causas distintas. Ejecute `/status` primero para ver qué método de inicio de sesión y suscripción está usando.

* **Está autenticado con una clave API o cuenta de Console**: Remote Control requiere OAuth de claude.ai. Ejecute `/login` y elija la opción de claude.ai. Si `ANTHROPIC_API_KEY` está configurado en su entorno, desactívelo.
* **Su administrador de Team o Enterprise no lo ha habilitado**: Remote Control está deshabilitado de forma predeterminada en estos planes. Un administrador puede habilitarlo en [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) activando el botón de alternancia **Remote Control**. Esta es una configuración de organización del lado del servidor, no una clave de [configuración administrada](/es/permissions#managed-only-settings).
* **El botón de alternancia del administrador está atenuado**: su organización tiene una configuración de retención de datos o cumplimiento que es incompatible con Remote Control. Esto no se puede cambiar desde el panel de administración. Póngase en contacto con el soporte de Anthropic para discutir opciones.

### "Remote credentials fetch failed"

Claude Code no pudo obtener una credencial de corta duración de la API de Anthropic para establecer la conexión. Vuelva a ejecutar con `--verbose` para ver el error completo:

```bash theme={null}
claude remote-control --verbose
```

Causas comunes:

* No ha iniciado sesión: ejecute `claude` y use `/login` para autenticarse con su cuenta de claude.ai. La autenticación con clave API no es compatible con Remote Control.
* Problema de red o proxy: un firewall o proxy puede estar bloqueando la solicitud HTTPS saliente. Remote Control requiere acceso a la API de Anthropic en el puerto 443.
* Error en la creación de sesión: si también ve `Session creation failed — see debug log`, el error ocurrió antes en la configuración. Verifique que su suscripción esté activa.

## Elija el enfoque correcto

Claude Code offers several ways to work when you're not at your terminal. They differ in what triggers the work, where Claude runs, and how much you need to set up.

|                                                | Trigger                                                                                        | Claude runs on                                                                               | Setup                                                                                                                                | Best for                                                      |
| :--------------------------------------------- | :--------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------ |
| [Dispatch](/en/desktop#sessions-from-dispatch) | Message a task from the Claude mobile app                                                      | Your machine (Desktop)                                                                       | [Pair the mobile app with Desktop](https://support.claude.com/en/articles/13947068)                                                  | Delegating work while you're away, minimal setup              |
| [Remote Control](/en/remote-control)           | Drive a running session from [claude.ai/code](https://claude.ai/code) or the Claude mobile app | Your machine (CLI or VS Code)                                                                | Run `claude remote-control`                                                                                                          | Steering in-progress work from another device                 |
| [Channels](/en/channels)                       | Push events from a chat app like Telegram or Discord, or your own server                       | Your machine (CLI)                                                                           | [Install a channel plugin](/en/channels#quickstart) or [build your own](/en/channels-reference)                                      | Reacting to external events like CI failures or chat messages |
| [Slack](/en/slack)                             | Mention `@Claude` in a team channel                                                            | Anthropic cloud                                                                              | [Install the Slack app](/en/slack#setting-up-claude-code-in-slack) with [Claude Code on the web](/en/claude-code-on-the-web) enabled | PRs and reviews from team chat                                |
| [Scheduled tasks](/en/scheduled-tasks)         | Set a schedule                                                                                 | [CLI](/en/scheduled-tasks), [Desktop](/en/desktop-scheduled-tasks), or [cloud](/en/routines) | Pick a frequency                                                                                                                     | Recurring automation like daily reviews                       |

## Recursos relacionados

* [Claude Code en la web](/es/claude-code-on-the-web): ejecute sesiones en entornos en la nube administrados por Anthropic en lugar de en su máquina
* [Ultraplan](/es/ultraplan): inicie una sesión de planificación en la nube desde su terminal y revise el plan en su navegador
* [Channels](/es/channels): reenvíe Telegram, Discord o iMessage a una sesión para que Claude reaccione a los mensajes mientras está fuera
* [Dispatch](/es/desktop#sessions-from-dispatch): envíe un mensaje de una tarea desde su teléfono y puede generar una sesión de Desktop para manejarla
* [Autenticación](/es/authentication): configure `/login` y administre credenciales para claude.ai
* [Referencia de CLI](/es/cli-reference): lista completa de banderas y comandos incluyendo `claude remote-control`
* [Seguridad](/es/security): cómo las sesiones de Remote Control se ajustan al modelo de seguridad de Claude Code
* [Uso de datos](/es/data-usage): qué datos fluyen a través de la API de Anthropic durante sesiones locales y remotas
