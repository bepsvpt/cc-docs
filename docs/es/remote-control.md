> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Continúe sesiones locales desde cualquier dispositivo con Remote Control

> Continúe una sesión local de Claude Code desde su teléfono, tableta o cualquier navegador usando Remote Control. Funciona con claude.ai/code y la aplicación móvil de Claude.

<Note>
  Remote Control está disponible en todos los planes. Los administradores de Team y Enterprise deben habilitar primero Claude Code en [configuración de administración](https://claude.ai/admin-settings/claude-code).
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

* **Suscripción**: disponible en planes Pro, Max, Team y Enterprise. Los administradores de Team y Enterprise deben habilitar primero Claude Code en [configuración de administración](https://claude.ai/admin-settings/claude-code). Las claves API no son compatibles.
* **Autenticación**: ejecute `claude` y use `/login` para iniciar sesión a través de claude.ai si aún no lo ha hecho.
* **Confianza del espacio de trabajo**: ejecute `claude` en su directorio de proyecto al menos una vez para aceptar el diálogo de confianza del espacio de trabajo.

## Inicie una sesión de Remote Control

Puede iniciar un servidor dedicado de Remote Control, iniciar una sesión interactiva con Remote Control habilitado, o conectarse a una sesión que ya se está ejecutando.

<Tabs>
  <Tab title="Modo servidor">
    Navegue a su directorio de proyecto y ejecute:

    ```bash  theme={null}
    claude remote-control
    ```

    El proceso sigue ejecutándose en su terminal en modo servidor, esperando conexiones remotas. Muestra una URL de sesión que puede usar para [conectarse desde otro dispositivo](#connect-from-another-device), y puede presionar la barra espaciadora para mostrar un código QR para acceso rápido desde su teléfono. Mientras una sesión remota está activa, la terminal muestra el estado de la conexión y la actividad de las herramientas.

    Banderas disponibles:

    | Bandera                      | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                              |
    | ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `--name "My Project"`        | Establezca un título de sesión personalizado visible en la lista de sesiones en claude.ai/code.                                                                                                                                                                                                                                                                                                                                                          |
    | `--spawn <mode>`             | Cómo se crean las sesiones concurrentes. Presione `w` en tiempo de ejecución para alternar.<br />• `same-dir` (predeterminado): todas las sesiones comparten el directorio de trabajo actual, por lo que pueden entrar en conflicto si editan los mismos archivos.<br />• `worktree`: cada sesión bajo demanda obtiene su propio [git worktree](/es/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees). Requiere un repositorio git. |
    | `--capacity <N>`             | Número máximo de sesiones concurrentes. El valor predeterminado es 32.                                                                                                                                                                                                                                                                                                                                                                                   |
    | `--verbose`                  | Mostrar registros detallados de conexión y sesión.                                                                                                                                                                                                                                                                                                                                                                                                       |
    | `--sandbox` / `--no-sandbox` | Habilitar o deshabilitar [sandboxing](/es/sandboxing) para aislamiento del sistema de archivos y red. Deshabilitado de forma predeterminada.                                                                                                                                                                                                                                                                                                             |
  </Tab>

  <Tab title="Sesión interactiva">
    Para iniciar una sesión normal interactiva de Claude Code con Remote Control habilitado, use la bandera `--remote-control` (o `--rc`):

    ```bash  theme={null}
    claude --remote-control
    ```

    Opcionalmente, pase un nombre para la sesión:

    ```bash  theme={null}
    claude --remote-control "My Project"
    ```

    Esto le proporciona una sesión interactiva completa en su terminal que también puede controlar desde claude.ai o la aplicación Claude. A diferencia de `claude remote-control` (modo servidor), puede escribir mensajes localmente mientras la sesión también está disponible de forma remota.
  </Tab>

  <Tab title="Desde una sesión existente">
    Si ya está en una sesión de Claude Code y desea continuarla de forma remota, use el comando `/remote-control` (o `/rc`):

    ```text  theme={null}
    /remote-control
    ```

    Pase un nombre como argumento para establecer un título de sesión personalizado:

    ```text  theme={null}
    /remote-control My Project
    ```

    Esto inicia una sesión de Remote Control que lleva su historial de conversación actual y muestra una URL de sesión y código QR que puede usar para [conectarse desde otro dispositivo](#connect-from-another-device). Las banderas `--verbose`, `--sandbox` y `--no-sandbox` no están disponibles con este comando.
  </Tab>
</Tabs>

### Conectarse desde otro dispositivo

Una vez que una sesión de Remote Control está activa, tiene varias formas de conectarse desde otro dispositivo:

* **Abra la URL de la sesión** en cualquier navegador para ir directamente a la sesión en [claude.ai/code](https://claude.ai/code). Tanto `claude remote-control` como `/remote-control` muestran esta URL en la terminal.
* **Escanee el código QR** que se muestra junto a la URL de la sesión para abrirlo directamente en la aplicación Claude. Con `claude remote-control`, presione la barra espaciadora para alternar la visualización del código QR.
* **Abra [claude.ai/code](https://claude.ai/code) o la aplicación Claude** y encuentre la sesión por nombre en la lista de sesiones. Las sesiones de Remote Control muestran un icono de computadora con un punto de estado verde cuando están en línea.

La sesión remota toma su nombre del argumento `--name` (o el nombre pasado a `/remote-control`), su último mensaje, su valor `/rename`, o "Remote Control session" si no hay historial de conversación. Si el entorno ya tiene una sesión activa, se le preguntará si desea continuarla o iniciar una nueva.

Si aún no tiene la aplicación Claude, use el comando `/mobile` dentro de Claude Code para mostrar un código QR de descarga para [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) o [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude).

### Habilite Remote Control para todas las sesiones

De forma predeterminada, Remote Control solo se activa cuando ejecuta explícitamente `claude remote-control`, `claude --remote-control`, o `/remote-control`. Para habilitarlo automáticamente para cada sesión interactiva, ejecute `/config` dentro de Claude Code y establezca **Enable Remote Control for all sessions** en `true`. Establézcalo de nuevo en `false` para deshabilitar.

Con esta configuración activada, cada proceso interactivo de Claude Code registra una sesión remota. Si ejecuta varias instancias, cada una obtiene su propio entorno y sesión. Para ejecutar varias sesiones concurrentes desde un único proceso, use el modo servidor con `--spawn` en su lugar.

## Conexión y seguridad

Su sesión local de Claude Code realiza solo solicitudes HTTPS salientes y nunca abre puertos entrantes en su máquina. Cuando inicia Remote Control, se registra con la API de Anthropic y sondea el trabajo. Cuando se conecta desde otro dispositivo, el servidor enruta mensajes entre el cliente web o móvil y su sesión local a través de una conexión de transmisión.

Todo el tráfico viaja a través de la API de Anthropic sobre TLS, el mismo transporte de seguridad que cualquier sesión de Claude Code. La conexión utiliza múltiples credenciales de corta duración, cada una limitada a un único propósito y expirando de forma independiente.

## Remote Control vs Claude Code en la web

Remote Control y [Claude Code en la web](/es/claude-code-on-the-web) ambos usan la interfaz claude.ai/code. La diferencia clave es dónde se ejecuta la sesión: Remote Control se ejecuta en su máquina, por lo que sus MCP servers locales, herramientas y configuración del proyecto permanecen disponibles. Claude Code en la web se ejecuta en infraestructura en la nube administrada por Anthropic.

Use Remote Control cuando esté en medio del trabajo local y desee continuar desde otro dispositivo. Use Claude Code en la web cuando desee iniciar una tarea sin ninguna configuración local, trabajar en un repositorio que no tiene clonado, o ejecutar varias tareas en paralelo.

## Limitaciones

* **Una sesión remota por proceso interactivo**: fuera del modo servidor, cada instancia de Claude Code admite una sesión remota a la vez. Use el modo servidor con `--spawn` para ejecutar varias sesiones concurrentes desde un único proceso.
* **La terminal debe permanecer abierta**: Remote Control se ejecuta como un proceso local. Si cierra la terminal o detiene el proceso `claude`, la sesión finaliza. Ejecute `claude remote-control` nuevamente para iniciar una nueva.
* **Interrupción de red extendida**: si su máquina está despierta pero no puede alcanzar la red durante más de aproximadamente 10 minutos, la sesión agota el tiempo de espera y el proceso se cierra. Ejecute `claude remote-control` nuevamente para iniciar una nueva sesión.

## Recursos relacionados

* [Claude Code en la web](/es/claude-code-on-the-web): ejecute sesiones en entornos en la nube administrados por Anthropic en lugar de en su máquina
* [Autenticación](/es/authentication): configure `/login` y administre credenciales para claude.ai
* [Referencia de CLI](/es/cli-reference): lista completa de banderas y comandos incluyendo `claude remote-control`
* [Seguridad](/es/security): cómo las sesiones de Remote Control se ajustan al modelo de seguridad de Claude Code
* [Uso de datos](/es/data-usage): qué datos fluyen a través de la API de Anthropic durante sesiones locales y remotas
