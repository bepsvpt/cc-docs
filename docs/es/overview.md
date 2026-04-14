> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Descripción general de Claude Code

> Claude Code es una herramienta de codificación agencial que lee tu base de código, edita archivos, ejecuta comandos e integra con tus herramientas de desarrollo. Disponible en tu terminal, IDE, aplicación de escritorio y navegador.

Claude Code es un asistente de codificación impulsado por IA que te ayuda a construir características, corregir errores y automatizar tareas de desarrollo. Entiende tu base de código completa y puede trabajar en múltiples archivos y herramientas para lograr las cosas.

## Comenzar

Elige tu entorno para comenzar. La mayoría de las superficies requieren una [suscripción a Claude](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=overview_pricing) o una cuenta de [Anthropic Console](https://console.anthropic.com/). La CLI de Terminal y VS Code también admiten [proveedores de terceros](/es/third-party-integrations).

<Tabs>
  <Tab title="Terminal">
    La CLI completa para trabajar con Claude Code directamente en tu terminal. Edita archivos, ejecuta comandos y gestiona tu proyecto completo desde la línea de comandos.

    To install Claude Code, use one of the following methods:

    <Tabs>
      <Tab title="Native Install (Recommended)">
        **macOS, Linux, WSL:**

        ```bash  theme={null}
        curl -fsSL https://claude.ai/install.sh | bash
        ```

        **Windows PowerShell:**

        ```powershell  theme={null}
        irm https://claude.ai/install.ps1 | iex
        ```

        **Windows CMD:**

        ```batch  theme={null}
        curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
        ```

        If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. Use the PowerShell command above instead. Your prompt shows `PS C:\` when you're in PowerShell.

        **Native Windows setups require [Git for Windows](https://git-scm.com/downloads/win).** Install it first if you don't have it. WSL setups do not need it.

        <Info>
          Native installations automatically update in the background to keep you on the latest version.
        </Info>
      </Tab>

      <Tab title="Homebrew">
        ```bash  theme={null}
        brew install --cask claude-code
        ```

        Homebrew offers two casks. `claude-code` tracks the stable release channel, which is typically about a week behind and skips releases with major regressions. `claude-code@latest` tracks the latest channel and receives new versions as soon as they ship.

        <Info>
          Homebrew installations do not auto-update. Run `brew upgrade claude-code` or `brew upgrade claude-code@latest`, depending on which cask you installed, to get the latest features and security fixes.
        </Info>
      </Tab>

      <Tab title="WinGet">
        ```powershell  theme={null}
        winget install Anthropic.ClaudeCode
        ```

        <Info>
          WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
        </Info>
      </Tab>
    </Tabs>

    Luego inicia Claude Code en cualquier proyecto:

    ```bash  theme={null}
    cd your-project
    claude
    ```

    Se te pedirá que inicies sesión en el primer uso. ¡Eso es todo! [Continúa con la Guía de inicio rápido →](/es/quickstart)

    <Tip>
      Consulta [configuración avanzada](/es/setup) para opciones de instalación, actualizaciones manuales o instrucciones de desinstalación. Visita [solución de problemas](/es/troubleshooting) si encuentras problemas.
    </Tip>
  </Tab>

  <Tab title="VS Code">
    La extensión de VS Code proporciona diffs en línea, menciones @, revisión de planes e historial de conversación directamente en tu editor.

    * [Instalar para VS Code](vscode:extension/anthropic.claude-code)
    * [Instalar para Cursor](cursor:extension/anthropic.claude-code)

    O busca "Claude Code" en la vista de Extensiones (`Cmd+Shift+X` en Mac, `Ctrl+Shift+X` en Windows/Linux). Después de instalar, abre la Paleta de comandos (`Cmd+Shift+P` / `Ctrl+Shift+P`), escribe "Claude Code" y selecciona **Abrir en Nueva Pestaña**.

    [Comenzar con VS Code →](/es/vs-code#get-started)
  </Tab>

  <Tab title="Aplicación de escritorio">
    Una aplicación independiente para ejecutar Claude Code fuera de tu IDE o terminal. Revisa diffs visualmente, ejecuta múltiples sesiones lado a lado, programa tareas recurrentes e inicia sesiones en la nube.

    Descarga e instala:

    * [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) (Intel y Apple Silicon)
    * [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs) (x64)
    * [Windows ARM64](https://claude.ai/api/desktop/win32/arm64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs) (solo sesiones remotas)

    Después de instalar, lanza Claude, inicia sesión y haz clic en la pestaña **Code** para comenzar a codificar. Se requiere una [suscripción de pago](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=overview_desktop_pricing).

    [Obtén más información sobre la aplicación de escritorio →](/es/desktop-quickstart)
  </Tab>

  <Tab title="Web">
    Ejecuta Claude Code en tu navegador sin configuración local. Inicia tareas de larga duración y vuelve cuando estén listas, trabaja en repositorios que no tienes localmente o ejecuta múltiples tareas en paralelo. Disponible en navegadores de escritorio y la aplicación Claude iOS.

    Comienza a codificar en [claude.ai/code](https://claude.ai/code).

    [Comenzar en la web →](/es/claude-code-on-the-web#getting-started)
  </Tab>

  <Tab title="JetBrains">
    Un plugin para IntelliJ IDEA, PyCharm, WebStorm y otros IDEs de JetBrains con visualización de diff interactiva y compartición de contexto de selección.

    Instala el [plugin Claude Code](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) desde el Marketplace de JetBrains y reinicia tu IDE.

    [Comenzar con JetBrains →](/es/jetbrains)
  </Tab>
</Tabs>

## Lo que puedes hacer

Aquí hay algunas de las formas en que puedes usar Claude Code:

<AccordionGroup>
  <Accordion title="Automatiza el trabajo que sigues posponiendo" icon="wand-magic-sparkles">
    Claude Code maneja las tareas tediosas que consumen tu día: escribir pruebas para código sin probar, corregir errores de lint en un proyecto, resolver conflictos de fusión, actualizar dependencias y escribir notas de lanzamiento.

    ```bash  theme={null}
    claude "write tests for the auth module, run them, and fix any failures"
    ```
  </Accordion>

  <Accordion title="Construye características y corrige errores" icon="hammer">
    Describe lo que quieres en lenguaje natural. Claude Code planifica el enfoque, escribe el código en múltiples archivos y verifica que funcione.

    Para errores, pega un mensaje de error o describe el síntoma. Claude Code rastrea el problema a través de tu base de código, identifica la causa raíz e implementa una corrección. Consulta [flujos de trabajo comunes](/es/common-workflows) para más ejemplos.
  </Accordion>

  <Accordion title="Crea commits y solicitudes de extracción" icon="code-branch">
    Claude Code funciona directamente con git. Prepara cambios, escribe mensajes de commit, crea ramas y abre solicitudes de extracción.

    ```bash  theme={null}
    claude "commit my changes with a descriptive message"
    ```

    En CI, puedes automatizar la revisión de código y la clasificación de problemas con [GitHub Actions](/es/github-actions) o [GitLab CI/CD](/es/gitlab-ci-cd).
  </Accordion>

  <Accordion title="Conecta tus herramientas con MCP" icon="plug">
    El [Protocolo de Contexto de Modelo (MCP)](/es/mcp) es un estándar abierto para conectar herramientas de IA a fuentes de datos externas. Con MCP, Claude Code puede leer tus documentos de diseño en Google Drive, actualizar tickets en Jira, extraer datos de Slack o usar tu propia herramienta personalizada.
  </Accordion>

  <Accordion title="Personaliza con instrucciones, skills y hooks" icon="sliders">
    [`CLAUDE.md`](/es/memory) es un archivo markdown que añades a la raíz de tu proyecto que Claude Code lee al inicio de cada sesión. Úsalo para establecer estándares de codificación, decisiones de arquitectura, librerías preferidas y listas de verificación de revisión. Claude también construye [memoria automática](/es/memory#auto-memory) mientras trabaja, guardando aprendizajes como comandos de compilación e insights de depuración en sesiones sin que escribas nada.

    Crea [comandos personalizados](/es/skills) para empaquetar flujos de trabajo repetibles que tu equipo pueda compartir, como `/review-pr` o `/deploy-staging`.

    [Hooks](/es/hooks) te permiten ejecutar comandos de shell antes o después de acciones de Claude Code, como formateo automático después de cada edición de archivo o ejecución de lint antes de un commit.
  </Accordion>

  <Accordion title="Ejecuta equipos de agentes y construye agentes personalizados" icon="users">
    Genera [múltiples agentes de Claude Code](/es/sub-agents) que trabajen en diferentes partes de una tarea simultáneamente. Un agente líder coordina el trabajo, asigna subtareas y fusiona resultados.

    Para flujos de trabajo completamente personalizados, el [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) te permite construir tus propios agentes impulsados por las herramientas y capacidades de Claude Code, con control total sobre orquestación, acceso a herramientas y permisos.
  </Accordion>

  <Accordion title="Canaliza, secuencia y automatiza con la CLI" icon="terminal">
    Claude Code es componible y sigue la filosofía de Unix. Canaliza registros en él, ejecútalo en CI o encadénalo con otras herramientas:

    ```bash  theme={null}
    # Analiza la salida de registros recientes
    tail -200 app.log | claude -p "Slack me if you see any anomalies"

    # Automatiza traducciones en CI
    claude -p "translate new strings into French and raise a PR for review"

    # Operaciones en masa en archivos
    git diff main --name-only | claude -p "review these changed files for security issues"
    ```

    Consulta la [referencia de CLI](/es/cli-reference) para el conjunto completo de comandos y banderas.
  </Accordion>

  <Accordion title="Programa tareas recurrentes" icon="clock">
    Ejecuta Claude en un horario para automatizar el trabajo que se repite: revisiones de PR matutinas, análisis de fallos de CI durante la noche, auditorías de dependencias semanales o sincronización de documentos después de que se fusionen los PR.

    * [Tareas programadas en la nube](/es/web-scheduled-tasks) se ejecutan en infraestructura administrada por Anthropic, por lo que siguen ejecutándose incluso cuando tu computadora está apagada. Créalas desde la web, la aplicación de escritorio o ejecutando `/schedule` en la CLI.
    * [Tareas programadas de escritorio](/es/desktop#schedule-recurring-tasks) se ejecutan en tu máquina, con acceso directo a tus archivos y herramientas locales
    * [`/loop`](/es/scheduled-tasks) repite un prompt dentro de una sesión de CLI para sondeo rápido
  </Accordion>

  <Accordion title="Trabaja desde cualquier lugar" icon="globe">
    Las sesiones no están vinculadas a una única superficie. Mueve el trabajo entre entornos a medida que cambia tu contexto:

    * Aléjate de tu escritorio y sigue trabajando desde tu teléfono o cualquier navegador con [Control Remoto](/es/remote-control)
    * Envía un mensaje a [Dispatch](/es/desktop#sessions-from-dispatch) con una tarea desde tu teléfono y abre la sesión de escritorio que crea
    * Inicia una tarea de larga duración en la [web](/es/claude-code-on-the-web) o [aplicación iOS](https://apps.apple.com/app/claude-by-anthropic/id6473753684), luego extráela a tu terminal con `/teleport`
    * Transfiere una sesión de terminal a la [aplicación de escritorio](/es/desktop) con `/desktop` para revisión visual de diff
    * Enruta tareas desde el chat del equipo: menciona `@Claude` en [Slack](/es/slack) con un informe de error y obtén una solicitud de extracción de vuelta
  </Accordion>
</AccordionGroup>

## Usa Claude Code en todas partes

Cada superficie se conecta al mismo motor subyacente de Claude Code, por lo que tus archivos CLAUDE.md, configuración y servidores MCP funcionan en todos ellos.

Más allá de los entornos [Terminal](/es/quickstart), [VS Code](/es/vs-code), [JetBrains](/es/jetbrains), [Desktop](/es/desktop) y [Web](/es/claude-code-on-the-web) anteriores, Claude Code se integra con flujos de trabajo de CI/CD, chat y navegador:

| Quiero...                                                                  | Mejor opción                                                                                                                        |
| -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Continuar una sesión local desde mi teléfono u otro dispositivo            | [Control Remoto](/es/remote-control)                                                                                                |
| Enviar eventos desde Telegram, Discord o mis propios webhooks a una sesión | [Canales](/es/channels)                                                                                                             |
| Iniciar una tarea localmente, continuar en móvil                           | [Web](/es/claude-code-on-the-web) o [aplicación Claude iOS](https://apps.apple.com/app/claude-by-anthropic/id6473753684)            |
| Ejecutar Claude en un horario recurrente                                   | [Tareas programadas en la nube](/es/web-scheduled-tasks) o [Tareas programadas de escritorio](/es/desktop#schedule-recurring-tasks) |
| Automatizar revisiones de PR y clasificación de problemas                  | [GitHub Actions](/es/github-actions) o [GitLab CI/CD](/es/gitlab-ci-cd)                                                             |
| Obtener revisión de código automática en cada PR                           | [Revisión de código de GitHub](/es/code-review)                                                                                     |
| Enrutar informes de errores de Slack a solicitudes de extracción           | [Slack](/es/slack)                                                                                                                  |
| Depurar aplicaciones web en vivo                                           | [Chrome](/es/chrome)                                                                                                                |
| Construir agentes personalizados para tus propios flujos de trabajo        | [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)                                                                 |

## Próximos pasos

Una vez que hayas instalado Claude Code, estas guías te ayudan a profundizar.

* [Guía de inicio rápido](/es/quickstart): recorre tu primera tarea real, desde explorar una base de código hasta confirmar una corrección
* [Almacena instrucciones y memorias](/es/memory): proporciona a Claude instrucciones persistentes con archivos CLAUDE.md y memoria automática
* [Flujos de trabajo comunes](/es/common-workflows) y [mejores prácticas](/es/best-practices): patrones para obtener lo máximo de Claude Code
* [Configuración](/es/settings): personaliza Claude Code para tu flujo de trabajo
* [Solución de problemas](/es/troubleshooting): soluciones para problemas comunes
* [code.claude.com](https://code.claude.com/): demostraciones, precios y detalles del producto
