> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Comenzar con la aplicación de escritorio

> Instale Claude Code en el escritorio e inicie su primera sesión de codificación

La aplicación de escritorio te proporciona Claude Code con una interfaz gráfica: revisión visual de diferencias, vista previa de aplicaciones en vivo, monitoreo de PR de GitHub con fusión automática, sesiones paralelas con aislamiento de Git worktree, tareas programadas y la capacidad de ejecutar tareas de forma remota. No se requiere terminal.

Esta página te guía a través de la instalación de la aplicación e iniciando tu primera sesión. Si ya estás configurado, consulta [Usar Claude Code Desktop](/es/desktop) para la referencia completa.

<Frame>
  <img src="https://mintcdn.com/claude-code/CNLUpFGiXoc9mhvD/images/desktop-code-tab-light.png?fit=max&auto=format&n=CNLUpFGiXoc9mhvD&q=85&s=9a36a7a27b9f4c6f2e1c83bdb34f69ce" className="block dark:hidden" alt="La interfaz de Claude Code Desktop mostrando la pestaña Code seleccionada, con un cuadro de solicitud, selector de modo de permisos establecido en Pedir permisos, selector de modelo, selector de carpeta y opción de entorno local" width="2500" height="1376" data-path="images/desktop-code-tab-light.png" />

  <img src="https://mintcdn.com/claude-code/CNLUpFGiXoc9mhvD/images/desktop-code-tab-dark.png?fit=max&auto=format&n=CNLUpFGiXoc9mhvD&q=85&s=5463defe81c459fb9b1f91f6a958cfb8" className="hidden dark:block" alt="La interfaz de Claude Code Desktop en modo oscuro mostrando la pestaña Code seleccionada, con un cuadro de solicitud, selector de modo de permisos establecido en Pedir permisos, selector de modelo, selector de carpeta y opción de entorno local" width="2504" height="1374" data-path="images/desktop-code-tab-dark.png" />
</Frame>

La aplicación de escritorio tiene tres pestañas:

* **Chat**: Conversación general sin acceso a archivos, similar a claude.ai.
* **Cowork**: Un agente autónomo de fondo que trabaja en tareas en una VM en la nube con su propio entorno. Puede funcionar de forma independiente mientras realizas otro trabajo.
* **Code**: Un asistente de codificación interactivo con acceso directo a tus archivos locales. Revisas y apruebas cada cambio en tiempo real.

Chat y Cowork se tratan en los [artículos de soporte de Claude Desktop](https://support.claude.com/en/collections/16163169-claude-desktop). Esta página se enfoca en la pestaña **Code**.

<Note>
  Claude Code requiere una [suscripción Pro, Max, Teams o Enterprise](https://claude.com/pricing).
</Note>

## Instalar

<Steps>
  <Step title="Descargar la aplicación">
    Descarga Claude para tu plataforma.

    <CardGroup cols={2}>
      <Card title="macOS" icon="apple" href="https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs">
        Compilación universal para Intel y Apple Silicon
      </Card>

      <Card title="Windows" icon="windows" href="https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code&utm_medium=docs">
        Para procesadores x64
      </Card>
    </CardGroup>

    Para Windows ARM64, [descarga aquí](https://claude.ai/api/desktop/win32/arm64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs).

    Linux no es compatible actualmente.
  </Step>

  <Step title="Iniciar sesión">
    Abre Claude desde tu carpeta de Aplicaciones (macOS) o menú Inicio (Windows). Inicia sesión con tu cuenta de Anthropic.
  </Step>

  <Step title="Abre la pestaña Code">
    Haz clic en la pestaña **Code** en el centro superior. Si hacer clic en Code te solicita actualizar, necesitas [suscribirte a un plan de pago](https://claude.com/pricing) primero. Si te solicita iniciar sesión en línea, completa el inicio de sesión y reinicia la aplicación. Si ves un error 403, consulta [solución de problemas de autenticación](/es/desktop#403-or-authentication-errors-in-the-code-tab).
  </Step>
</Steps>

La aplicación de escritorio incluye Claude Code. No necesitas instalar Node.js o la CLI por separado. Para usar `claude` desde la terminal, instala la CLI por separado. Consulta [Comenzar con la CLI](/es/quickstart).

## Inicia tu primera sesión

Con la pestaña Code abierta, elige un proyecto y dale a Claude algo que hacer.

<Steps>
  <Step title="Elige un entorno y carpeta">
    Selecciona **Local** para ejecutar Claude en tu máquina usando tus archivos directamente. Haz clic en **Seleccionar carpeta** y elige tu directorio de proyecto.

    <Tip>
      Comienza con un proyecto pequeño que conozcas bien. Es la forma más rápida de ver qué puede hacer Claude Code. En Windows, [Git](https://git-scm.com/downloads/win) debe estar instalado para que las sesiones locales funcionen. La mayoría de las Macs incluyen Git de forma predeterminada.
    </Tip>

    También puedes seleccionar:

    * **Remote**: Ejecuta sesiones en la infraestructura en la nube de Anthropic que continúan incluso si cierras la aplicación. Las sesiones remotas utilizan la misma infraestructura que [Claude Code en la web](/es/claude-code-on-the-web).
    * **SSH**: Conéctate a una máquina remota a través de SSH (tus propios servidores, VMs en la nube o contenedores de desarrollo). Claude Code debe estar instalado en la máquina remota.
  </Step>

  <Step title="Elige un modelo">
    Selecciona un modelo del menú desplegable junto al botón de envío. Consulta [modelos](/es/model-config#available-models) para una comparación de Opus, Sonnet y Haiku. No puedes cambiar el modelo después de que la sesión comience.
  </Step>

  <Step title="Dile a Claude qué hacer">
    Escribe lo que quieres que Claude haga:

    * `Encuentra un comentario TODO y corrígelo`
    * `Agrega pruebas para la función principal`
    * `Crea un CLAUDE.md con instrucciones para este repositorio de código`

    Una [sesión](/es/desktop#work-in-parallel-with-sessions) es una conversación con Claude sobre tu código. Cada sesión rastrea su propio contexto y cambios, para que puedas trabajar en múltiples tareas sin que se interfieran entre sí.
  </Step>

  <Step title="Revisa y acepta cambios">
    De forma predeterminada, la pestaña Code comienza en [modo Pedir permisos](/es/desktop#choose-a-permission-mode), donde Claude propone cambios y espera tu aprobación antes de aplicarlos. Verás:

    1. Una [vista de diferencias](/es/desktop#review-changes-with-diff-view) que muestra exactamente qué cambiará en cada archivo
    2. Botones Aceptar/Rechazar para aprobar o rechazar cada cambio
    3. Actualizaciones en tiempo real mientras Claude trabaja en tu solicitud

    Si rechazas un cambio, Claude te preguntará cómo te gustaría proceder de manera diferente. Tus archivos no se modifican hasta que aceptes.
  </Step>
</Steps>

## ¿Y ahora qué?

Has realizado tu primera edición. Para la referencia completa de todo lo que Desktop puede hacer, consulta [Usar Claude Code Desktop](/es/desktop). Aquí hay algunas cosas para probar a continuación.

**Interrumpe y dirige.** Puedes interrumpir a Claude en cualquier momento. Si va por el camino equivocado, haz clic en el botón de parada o escribe tu corrección y presiona **Enter**. Claude detiene lo que está haciendo y se ajusta según tu entrada. No tienes que esperar a que termine o empezar de nuevo.

**Dale a Claude más contexto.** Escribe `@nombre_de_archivo` en el cuadro de solicitud para incluir un archivo específico en la conversación, adjunta imágenes y PDFs usando el botón de adjuntos, o arrastra y suelta archivos directamente en la solicitud. Cuanto más contexto tenga Claude, mejores serán los resultados. Consulta [Agregar archivos y contexto](/es/desktop#add-files-and-context-to-prompts).

**Usa skills para tareas repetibles.** Escribe `/` o haz clic en **+** → **Slash commands** para explorar [comandos integrados](/es/interactive-mode#built-in-commands), [skills personalizados](/es/skills) y skills de plugins. Los skills son solicitudes reutilizables que puedes invocar cuando las necesites, como listas de verificación de revisión de código o pasos de implementación.

**Revisa cambios antes de confirmar.** Después de que Claude edita archivos, aparece un indicador `+12 -1`. Haz clic en él para abrir la [vista de diferencias](/es/desktop#review-changes-with-diff-view), revisa modificaciones archivo por archivo y comenta en líneas específicas. Claude lee tus comentarios y revisa. Haz clic en **Revisar código** para que Claude evalúe las diferencias y deje sugerencias en línea.

**Ajusta cuánto control tienes.** Tu [modo de permisos](/es/desktop#choose-a-permission-mode) controla el equilibrio. Pedir permisos (predeterminado) requiere aprobación antes de cada edición. Auto aceptar ediciones acepta automáticamente ediciones de archivos para una iteración más rápida. Plan mode permite que Claude trace un enfoque sin tocar ningún archivo, lo cual es útil antes de una refactorización grande.

**Agrega plugins para más capacidades.** Haz clic en el botón **+** junto al cuadro de solicitud y selecciona **Plugins** para explorar e instalar [plugins](/es/desktop#install-plugins) que agregan skills, agentes, MCP servers y más.

**Vista previa de tu aplicación.** Haz clic en el menú desplegable **Preview** para ejecutar tu servidor de desarrollo directamente en el escritorio. Claude puede ver la aplicación en ejecución, probar puntos finales, inspeccionar registros e iterar en lo que ve. Consulta [Vista previa de tu aplicación](/es/desktop#preview-your-app).

**Rastrea tu solicitud de extracción.** Después de abrir un PR, Claude Code monitorea los resultados de las verificaciones de CI y puede corregir automáticamente fallos o fusionar el PR una vez que todas las verificaciones pasen. Consulta [Monitorear estado de solicitud de extracción](/es/desktop#monitor-pull-request-status).

**Pon a Claude en un horario.** Configura [tareas programadas](/es/desktop#schedule-recurring-tasks) para ejecutar Claude automáticamente de forma recurrente: una revisión de código diaria cada mañana, una auditoría de dependencias semanal, o un resumen que extrae de tus herramientas conectadas.

**Escala cuando estés listo.** Abre [sesiones paralelas](/es/desktop#work-in-parallel-with-sessions) desde la barra lateral para trabajar en múltiples tareas a la vez, cada una en su propio Git worktree. Envía [trabajo de larga duración a la nube](/es/desktop#run-long-running-tasks-remotely) para que continúe incluso si cierras la aplicación, o [continúa una sesión en la web o en tu IDE](/es/desktop#continue-in-another-surface) si una tarea toma más tiempo del esperado. [Conecta herramientas externas](/es/desktop#extend-claude-code) como GitHub, Slack y Linear para unir tu flujo de trabajo.

## ¿Vienes de la CLI?

Desktop ejecuta el mismo motor que la CLI con una interfaz gráfica. Puedes ejecutar ambos simultáneamente en el mismo proyecto, y comparten configuración (archivos CLAUDE.md, MCP servers, hooks, skills y configuración). Para una comparación completa de características, equivalentes de banderas y lo que no está disponible en Desktop, consulta [Comparación de CLI](/es/desktop#coming-from-the-cli).

## Qué sigue

* [Usar Claude Code Desktop](/es/desktop): modos de permisos, sesiones paralelas, vista de diferencias, conectores y configuración empresarial
* [Solución de problemas](/es/desktop#troubleshooting): soluciones a errores comunes y problemas de configuración
* [Mejores prácticas](/es/best-practices): consejos para escribir solicitudes efectivas y aprovechar al máximo Claude Code
* [Flujos de trabajo comunes](/es/common-workflows): tutoriales para depuración, refactorización, pruebas y más
