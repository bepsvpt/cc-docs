> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Continúa sesiones locales desde cualquier dispositivo con Control Remoto

> Continúa una sesión local de Claude Code desde tu teléfono, tableta o cualquier navegador usando Remote Control. Funciona con claude.ai/code y la aplicación móvil de Claude.

<Note>
  Remote Control está disponible en todos los planes. Los administradores de Team y Enterprise deben habilitar primero Claude Code en [configuración de administración](https://claude.ai/admin-settings/claude-code).
</Note>

Remote Control conecta [claude.ai/code](https://claude.ai/code) o la aplicación Claude para [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) y [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) a una sesión de Claude Code que se ejecuta en tu máquina. Inicia una tarea en tu escritorio y luego continúa desde tu teléfono en el sofá o desde un navegador en otra computadora.

Cuando inicias una sesión de Remote Control en tu máquina, Claude sigue ejecutándose localmente todo el tiempo, por lo que nada se mueve a la nube. Con Remote Control puedes:

* **Usar tu entorno local completo de forma remota**: tu sistema de archivos, [MCP servers](/es/mcp), herramientas y configuración del proyecto permanecen disponibles
* **Trabajar desde ambas superficies a la vez**: la conversación se mantiene sincronizada en todos los dispositivos conectados, para que puedas enviar mensajes desde tu terminal, navegador y teléfono indistintamente
* **Sobrevivir a interrupciones**: si tu portátil se duerme o tu red se cae, la sesión se reconecta automáticamente cuando tu máquina vuelve a estar en línea

A diferencia de [Claude Code en la web](/es/claude-code-on-the-web), que se ejecuta en infraestructura en la nube, las sesiones de Remote Control se ejecutan directamente en tu máquina e interactúan con tu sistema de archivos local. Las interfaces web y móvil son solo una ventana a esa sesión local.

<Note>
  Remote Control requiere Claude Code v2.1.51 o posterior. Verifica tu versión con `claude --version`.
</Note>

Esta página cubre la configuración, cómo iniciar y conectarse a sesiones, y cómo Remote Control se compara con Claude Code en la web.

## Requisitos

Antes de usar Remote Control, confirma que tu entorno cumple con estas condiciones:

* **Suscripción**: disponible en planes Pro, Max, Team y Enterprise. Los administradores de Team y Enterprise deben habilitar primero Claude Code en [configuración de administración](https://claude.ai/admin-settings/claude-code). Las claves API no son compatibles.
* **Autenticación**: ejecuta `claude` y usa `/login` para iniciar sesión a través de claude.ai si aún no lo has hecho.
* **Confianza del espacio de trabajo**: ejecuta `claude` en tu directorio de proyecto al menos una vez para aceptar el diálogo de confianza del espacio de trabajo.

## Inicia una sesión de Remote Control

Puedes iniciar una nueva sesión directamente en Remote Control, o conectar una sesión que ya está en ejecución.

<Tabs>
  <Tab title="Nueva sesión">
    Navega a tu directorio de proyecto y ejecuta:

    ```bash  theme={null}
    claude remote-control
    ```

    El proceso sigue ejecutándose en tu terminal, esperando conexiones remotas. Muestra una URL de sesión que puedes usar para [conectarte desde otro dispositivo](#connect-from-another-device), y puedes presionar la barra espaciadora para mostrar un código QR para acceso rápido desde tu teléfono. Mientras una sesión remota está activa, la terminal muestra el estado de la conexión y la actividad de las herramientas.

    Este comando admite las siguientes banderas:

    * **`--name "My Project"`**: establece un título de sesión personalizado visible en la lista de sesiones en claude.ai/code. También puedes pasar el nombre como argumento posicional: `claude remote-control "My Project"`
    * **`--verbose`**: muestra registros detallados de conexión y sesión
    * **`--sandbox`** / **`--no-sandbox`**: habilita o deshabilita [sandboxing](/es/sandboxing) para aislamiento del sistema de archivos y red durante la sesión. El sandboxing está deshabilitado de forma predeterminada.
  </Tab>

  <Tab title="Desde una sesión existente">
    Si ya estás en una sesión de Claude Code y deseas continuarla de forma remota, usa el comando `/remote-control` (o `/rc`):

    ```text  theme={null}
    /remote-control
    ```

    Pasa un nombre como argumento para establecer un título de sesión personalizado:

    ```text  theme={null}
    /remote-control My Project
    ```

    Esto inicia una sesión de Remote Control que lleva tu historial de conversación actual y muestra una URL de sesión y código QR que puedes usar para [conectarte desde otro dispositivo](#connect-from-another-device). Las banderas `--verbose`, `--sandbox` y `--no-sandbox` no están disponibles con este comando.
  </Tab>
</Tabs>

### Conectarse desde otro dispositivo

Una vez que una sesión de Remote Control está activa, tienes varias formas de conectarte desde otro dispositivo:

* **Abre la URL de sesión** en cualquier navegador para ir directamente a la sesión en [claude.ai/code](https://claude.ai/code). Tanto `claude remote-control` como `/remote-control` muestran esta URL en la terminal.
* **Escanea el código QR** que se muestra junto a la URL de sesión para abrirlo directamente en la aplicación Claude. Con `claude remote-control`, presiona la barra espaciadora para alternar la visualización del código QR.
* **Abre [claude.ai/code](https://claude.ai/code) o la aplicación Claude** y encuentra la sesión por nombre en la lista de sesiones. Las sesiones de Remote Control muestran un icono de computadora con un punto de estado verde cuando están en línea.

La sesión remota toma su nombre del argumento `--name` (o el nombre pasado a `/remote-control`), tu último mensaje, tu valor `/rename`, o "Remote Control session" si no hay historial de conversación. Si el entorno ya tiene una sesión activa, se te preguntará si deseas continuarla o iniciar una nueva.

Si aún no tienes la aplicación Claude, usa el comando `/mobile` dentro de Claude Code para mostrar un código QR de descarga para [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) o [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude).

### Habilita Remote Control para todas las sesiones

De forma predeterminada, Remote Control solo se activa cuando ejecutas explícitamente `claude remote-control` o `/remote-control`. Para habilitarlo automáticamente para cada sesión, ejecuta `/config` dentro de Claude Code y establece **Enable Remote Control for all sessions** en `true`. Establécelo de nuevo en `false` para deshabilitarlo.

Cada instancia de Claude Code admite una sesión remota a la vez. Si ejecutas múltiples instancias, cada una obtiene su propio entorno y sesión.

## Conexión y seguridad

Tu sesión local de Claude Code realiza solo solicitudes HTTPS salientes y nunca abre puertos entrantes en tu máquina. Cuando inicias Remote Control, se registra con la API de Anthropic y sondea en busca de trabajo. Cuando te conectas desde otro dispositivo, el servidor enruta mensajes entre el cliente web o móvil y tu sesión local a través de una conexión de transmisión.

Todo el tráfico viaja a través de la API de Anthropic sobre TLS, el mismo transporte de seguridad que cualquier sesión de Claude Code. La conexión utiliza múltiples credenciales de corta duración, cada una limitada a un propósito único y expirando de forma independiente.

## Remote Control vs Claude Code en la web

Remote Control y [Claude Code en la web](/es/claude-code-on-the-web) ambos usan la interfaz claude.ai/code. La diferencia clave es dónde se ejecuta la sesión: Remote Control se ejecuta en tu máquina, por lo que tus MCP servers locales, herramientas y configuración del proyecto permanecen disponibles. Claude Code en la web se ejecuta en infraestructura en la nube administrada por Anthropic.

Usa Remote Control cuando estés en medio de trabajo local y desees continuar desde otro dispositivo. Usa Claude Code en la web cuando desees iniciar una tarea sin ninguna configuración local, trabajar en un repositorio que no tienes clonado, o ejecutar múltiples tareas en paralelo.

## Limitaciones

* **Una sesión remota a la vez**: cada sesión de Claude Code admite una conexión remota.
* **La terminal debe permanecer abierta**: Remote Control se ejecuta como un proceso local. Si cierras la terminal o detienes el proceso `claude`, la sesión termina. Ejecuta `claude remote-control` de nuevo para iniciar una nueva.
* **Interrupción de red extendida**: si tu máquina está despierta pero no puede alcanzar la red durante más de aproximadamente 10 minutos, la sesión agota el tiempo de espera y el proceso se cierra. Ejecuta `claude remote-control` de nuevo para iniciar una nueva sesión.

## Recursos relacionados

* [Claude Code en la web](/es/claude-code-on-the-web): ejecuta sesiones en entornos en la nube administrados por Anthropic en lugar de en tu máquina
* [Autenticación](/es/authentication): configura `/login` y gestiona credenciales para claude.ai
* [Referencia de CLI](/es/cli-reference): lista completa de banderas y comandos incluyendo `claude remote-control`
* [Seguridad](/es/security): cómo las sesiones de Remote Control se ajustan al modelo de seguridad de Claude Code
* [Uso de datos](/es/data-usage): qué datos fluyen a través de la API de Anthropic durante sesiones locales y remotas
