> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Comenzar con la aplicación de escritorio

> Instale Claude Code en el escritorio e inicie su primera sesión de codificación

La aplicación de escritorio le proporciona Claude Code con una interfaz gráfica: revisión visual de diferencias, vista previa de aplicaciones en vivo, monitoreo de PR de GitHub con fusión automática, sesiones paralelas con aislamiento de Git worktrees, tareas programadas y la capacidad de ejecutar tareas de forma remota. No se requiere terminal.

Esta página lo guía a través de la instalación de la aplicación e iniciando su primera sesión. Si ya está configurado, consulte [Usar Claude Code Desktop](/es/desktop) para la referencia completa.

<Frame>
  <img src="https://mintlify.s3.us-west-1.amazonaws.com/claude-code/images/desktop-code-tab-light.png" className="block dark:hidden" alt="La interfaz de Claude Code Desktop mostrando la pestaña Code seleccionada, con un cuadro de solicitud, selector de modo de permisos establecido en Ask permissions, selector de modelo, selector de carpeta y opción de entorno local" />

  <img src="https://mintlify.s3.us-west-1.amazonaws.com/claude-code/images/desktop-code-tab-dark.png" className="hidden dark:block" alt="La interfaz de Claude Code Desktop en modo oscuro mostrando la pestaña Code seleccionada, con un cuadro de solicitud, selector de modo de permisos establecido en Ask permissions, selector de modelo, selector de carpeta y opción de entorno local" />
</Frame>

La aplicación de escritorio tiene tres pestañas:

* **Chat**: Conversación general sin acceso a archivos, similar a claude.ai.
* **Cowork**: Un agente autónomo de fondo que trabaja en tareas en una VM en la nube con su propio entorno. Puede ejecutarse de forma independiente mientras realiza otro trabajo.
* **Code**: Un asistente de codificación interactivo con acceso directo a sus archivos locales. Revisa y aprueba cada cambio en tiempo real.

Chat y Cowork se tratan en los [artículos de soporte de Claude Desktop](https://support.claude.com/en/collections/16163169-claude-desktop). Esta página se enfoca en la pestaña **Code**.

<Note>
  Claude Code requiere una [suscripción Pro, Max, Teams o Enterprise](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=desktop_quickstart_pricing).
</Note>

## Instalar

<Steps>
  <Step title="Descargar la aplicación">
    Descargue Claude para su plataforma.

    <CardGroup cols={2}>
      <Card title="macOS" icon="apple" href="https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs">
        Compilación universal para Intel y Apple Silicon
      </Card>

      <Card title="Windows" icon="windows" href="https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code&utm_medium=docs">
        Para procesadores x64
      </Card>
    </CardGroup>

    Para Windows ARM64, [descargue aquí](https://claude.ai/api/desktop/win32/arm64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs).

    Linux no es compatible actualmente.
  </Step>

  <Step title="Iniciar sesión">
    Inicie Claude desde su carpeta Aplicaciones (macOS) o menú Inicio (Windows). Inicie sesión con su cuenta de Anthropic.
  </Step>

  <Step title="Abrir la pestaña Code">
    Haga clic en la pestaña **Code** en el centro superior. Si hacer clic en Code le solicita actualizar, debe [suscribirse a un plan de pago](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=desktop_quickstart_upgrade) primero. Si le solicita iniciar sesión en línea, complete el inicio de sesión y reinicie la aplicación. Si ve un error 403, consulte [solución de problemas de autenticación](/es/desktop#403-or-authentication-errors-in-the-code-tab).
  </Step>
</Steps>

La aplicación de escritorio incluye Claude Code. No necesita instalar Node.js o la CLI por separado. Para usar `claude` desde la terminal, instale la CLI por separado. Consulte [Comenzar con la CLI](/es/quickstart).

## Inicie su primera sesión

Con la pestaña Code abierta, elija un proyecto y dele a Claude algo que hacer.

<Steps>
  <Step title="Elegir un entorno y carpeta">
    Seleccione **Local** para ejecutar Claude en su máquina usando sus archivos directamente. Haga clic en **Select folder** y elija su directorio de proyecto.

    <Tip>
      Comience con un proyecto pequeño que conozca bien. Es la forma más rápida de ver qué puede hacer Claude Code. En Windows, [Git](https://git-scm.com/downloads/win) debe estar instalado para que las sesiones locales funcionen. La mayoría de Macs incluyen Git de forma predeterminada.
    </Tip>

    También puede seleccionar:

    * **Remote**: Ejecute sesiones en la infraestructura en la nube de Anthropic que continúan incluso si cierra la aplicación. Las sesiones remotas utilizan la misma infraestructura que [Claude Code en la web](/es/claude-code-on-the-web).
    * **SSH**: Conéctese a una máquina remota a través de SSH (sus propios servidores, VMs en la nube o contenedores de desarrollo). Claude Code debe estar instalado en la máquina remota.
  </Step>

  <Step title="Elegir un modelo">
    Seleccione un modelo del menú desplegable junto al botón de envío. Consulte [modelos](/es/model-config#available-models) para una comparación de Opus, Sonnet y Haiku. No puede cambiar el modelo después de que la sesión comience.
  </Step>

  <Step title="Dígale a Claude qué hacer">
    Escriba lo que desea que Claude haga:

    * `Find a TODO comment and fix it`
    * `Add tests for the main function`
    * `Create a CLAUDE.md with instructions for this codebase`

    Una [sesión](/es/desktop#work-in-parallel-with-sessions) es una conversación con Claude sobre su código. Cada sesión rastrea su propio contexto y cambios, por lo que puede trabajar en múltiples tareas sin que se interfieran entre sí.
  </Step>

  <Step title="Revisar y aceptar cambios">
    De forma predeterminada, la pestaña Code comienza en [modo Ask permissions](/es/desktop#choose-a-permission-mode), donde Claude propone cambios y espera su aprobación antes de aplicarlos. Verá:

    1. Una [vista de diferencias](/es/desktop#review-changes-with-diff-view) que muestra exactamente qué cambiará en cada archivo
    2. Botones Aceptar/Rechazar para aprobar o rechazar cada cambio
    3. Actualizaciones en tiempo real mientras Claude trabaja en su solicitud

    Si rechaza un cambio, Claude le preguntará cómo le gustaría proceder de manera diferente. Sus archivos no se modifican hasta que acepte.
  </Step>
</Steps>

## ¿Ahora qué?

Ha realizado su primera edición. Para la referencia completa sobre todo lo que Desktop puede hacer, consulte [Usar Claude Code Desktop](/es/desktop). Aquí hay algunas cosas para probar a continuación.

**Interrumpir y dirigir.** Puede interrumpir a Claude en cualquier momento. Si va por el camino equivocado, haga clic en el botón de parada o escriba su corrección y presione **Enter**. Claude detiene lo que está haciendo y se ajusta según su entrada. No tiene que esperar a que termine o comenzar de nuevo.

**Proporcione más contexto a Claude.** Escriba `@filename` en el cuadro de solicitud para extraer un archivo específico a la conversación, adjunte imágenes y PDF usando el botón de adjuntos, o arrastre y suelte archivos directamente en la solicitud. Cuanto más contexto tenga Claude, mejores serán los resultados. Consulte [Agregar archivos y contexto](/es/desktop#add-files-and-context-to-prompts).

**Use skills para tareas repetibles.** Escriba `/` o haga clic en **+** → **Slash commands** para examinar [comandos integrados](/es/commands), [skills personalizados](/es/skills) y skills de plugins. Los skills son solicitudes reutilizables que puede invocar siempre que las necesite, como listas de verificación de revisión de código o pasos de implementación.

**Revise los cambios antes de confirmar.** Después de que Claude edita archivos, aparece un indicador `+12 -1`. Haga clic en él para abrir la [vista de diferencias](/es/desktop#review-changes-with-diff-view), revise las modificaciones archivo por archivo y comente en líneas específicas. Claude lee sus comentarios y revisa. Haga clic en **Review code** para que Claude evalúe las diferencias y deje sugerencias en línea.

**Ajuste cuánto control tiene.** Su [modo de permisos](/es/desktop#choose-a-permission-mode) controla el equilibrio. Ask permissions (predeterminado) requiere aprobación antes de cada edición. Auto accept edits acepta automáticamente ediciones de archivos para una iteración más rápida. Plan mode permite que Claude mapee un enfoque sin tocar ningún archivo, lo cual es útil antes de una refactorización grande.

**Agregue plugins para más capacidades.** Haga clic en el botón **+** junto al cuadro de solicitud y seleccione **Plugins** para examinar e instalar [plugins](/es/desktop#install-plugins) que agregan skills, agentes, MCP servers y más.

**Obtenga una vista previa de su aplicación.** Haga clic en el menú desplegable **Preview** para ejecutar su servidor de desarrollo directamente en el escritorio. Claude puede ver la aplicación en ejecución, probar puntos finales, inspeccionar registros e iterar en lo que ve. Consulte [Obtenga una vista previa de su aplicación](/es/desktop#preview-your-app).

**Rastree su solicitud de extracción.** Después de abrir un PR, Claude Code monitorea los resultados de verificación de CI y puede corregir automáticamente fallas o fusionar el PR una vez que todas las verificaciones pasen. Consulte [Monitorear el estado de la solicitud de extracción](/es/desktop#monitor-pull-request-status).

**Ponga a Claude en un horario.** Configure [tareas programadas](/es/desktop#schedule-recurring-tasks) para ejecutar Claude automáticamente de forma recurrente: una revisión de código diaria cada mañana, una auditoría de dependencias semanal o un resumen que extraiga de sus herramientas conectadas.

**Escale cuando esté listo.** Abra [sesiones paralelas](/es/desktop#work-in-parallel-with-sessions) desde la barra lateral para trabajar en múltiples tareas a la vez, cada una en su propio Git worktree. Envíe [trabajo de larga duración a la nube](/es/desktop#run-long-running-tasks-remotely) para que continúe incluso si cierra la aplicación, o [continúe una sesión en la web o en su IDE](/es/desktop#continue-in-another-surface) si una tarea toma más tiempo del esperado. [Conecte herramientas externas](/es/desktop#extend-claude-code) como GitHub, Slack y Linear para reunir su flujo de trabajo.

## ¿Viene de la CLI?

Desktop ejecuta el mismo motor que la CLI con una interfaz gráfica. Puede ejecutar ambos simultáneamente en el mismo proyecto y comparten configuración (archivos CLAUDE.md, MCP servers, hooks, skills y configuración). Para una comparación completa de características, equivalentes de banderas y lo que no está disponible en Desktop, consulte [Comparación de CLI](/es/desktop#coming-from-the-cli).

## Qué sigue

* [Usar Claude Code Desktop](/es/desktop): modos de permisos, sesiones paralelas, vista de diferencias, conectores y configuración empresarial
* [Solución de problemas](/es/desktop#troubleshooting): soluciones a errores comunes y problemas de configuración
* [Mejores prácticas](/es/best-practices): consejos para escribir solicitudes efectivas y aprovechar al máximo Claude Code
* [Flujos de trabajo comunes](/es/common-workflows): tutoriales para depuración, refactorización, pruebas y más
