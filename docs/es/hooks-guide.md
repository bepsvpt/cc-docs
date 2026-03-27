> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Automatizar flujos de trabajo con hooks

> Ejecuta comandos de shell automáticamente cuando Claude Code edita archivos, finaliza tareas o necesita entrada. Formatea código, envía notificaciones, valida comandos y aplica reglas del proyecto.

Los hooks son comandos de shell definidos por el usuario que se ejecutan en puntos específicos del ciclo de vida de Claude Code. Proporcionan control determinista sobre el comportamiento de Claude Code, asegurando que ciertas acciones siempre ocurran en lugar de depender de que el LLM elija ejecutarlas. Usa hooks para aplicar reglas del proyecto, automatizar tareas repetitivas e integrar Claude Code con tus herramientas existentes.

Para decisiones que requieren criterio en lugar de reglas deterministas, también puedes usar [hooks basados en prompts](#prompt-based-hooks) o [hooks basados en agentes](#agent-based-hooks) que utilizan un modelo Claude para evaluar condiciones.

Para otras formas de extender Claude Code, consulta [skills](/es/skills) para dar a Claude instrucciones adicionales y comandos ejecutables, [subagents](/es/sub-agents) para ejecutar tareas en contextos aislados, y [plugins](/es/plugins) para empaquetar extensiones para compartir entre proyectos.

<Tip>
  Esta guía cubre casos de uso comunes y cómo comenzar. Para esquemas de eventos completos, formatos de entrada/salida JSON y características avanzadas como hooks asincronos y hooks de herramientas MCP, consulta la [referencia de Hooks](/es/hooks).
</Tip>

## Configura tu primer hook

Para crear un hook, añade un bloque `hooks` a un [archivo de configuración](#configure-hook-location). Este tutorial crea un hook de notificación de escritorio, para que recibas una alerta cada vez que Claude esté esperando tu entrada en lugar de ver la terminal.

<Steps>
  <Step title="Añade el hook a tu configuración">
    Abre `~/.claude/settings.json` y añade un hook `Notification`. El ejemplo a continuación usa `osascript` para macOS; consulta [Recibe notificaciones cuando Claude necesita entrada](#get-notified-when-claude-needs-input) para comandos de Linux y Windows.

    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
              }
            ]
          }
        ]
      }
    }
    ```

    Si tu archivo de configuración ya tiene una clave `hooks`, fusiona la entrada `Notification` en ella en lugar de reemplazar el objeto completo. También puedes pedirle a Claude que escriba el hook por ti describiendo lo que quieres en la CLI.
  </Step>

  <Step title="Verifica la configuración">
    Escribe `/hooks` para abrir el navegador de hooks. Verás una lista de todos los eventos de hook disponibles, con un contador junto a cada evento que tiene hooks configurados. Selecciona `Notification` para confirmar que tu nuevo hook aparece en la lista. Seleccionar el hook muestra sus detalles: el evento, matcher, tipo, archivo de origen y comando.
  </Step>

  <Step title="Prueba el hook">
    Presiona `Esc` para volver a la CLI. Pídele a Claude que haga algo que requiera permiso, luego cambia de la terminal. Deberías recibir una notificación de escritorio.
  </Step>
</Steps>

<Tip>
  El menú `/hooks` es de solo lectura. Para añadir, modificar o eliminar hooks, edita tu JSON de configuración directamente o pídele a Claude que haga el cambio.
</Tip>

## Qué puedes automatizar

Los hooks te permiten ejecutar código en puntos clave del ciclo de vida de Claude Code: formatear archivos después de ediciones, bloquear comandos antes de que se ejecuten, enviar notificaciones cuando Claude necesita entrada, inyectar contexto al inicio de la sesión, y más. Para la lista completa de eventos de hook, consulta la [referencia de Hooks](/es/hooks#hook-lifecycle).

Cada ejemplo incluye un bloque de configuración listo para usar que añades a un [archivo de configuración](#configure-hook-location). Los patrones más comunes:

* [Recibe notificaciones cuando Claude necesita entrada](#get-notified-when-claude-needs-input)
* [Formatea automáticamente el código después de ediciones](#auto-format-code-after-edits)
* [Bloquea ediciones a archivos protegidos](#block-edits-to-protected-files)
* [Reinyecta contexto después de compactación](#re-inject-context-after-compaction)
* [Audita cambios de configuración](#audit-configuration-changes)
* [Recarga el entorno cuando el directorio o los archivos cambian](#reload-environment-when-directory-or-files-change)
* [Aprueba automáticamente avisos de permiso específicos](#auto-approve-specific-permission-prompts)

### Recibe notificaciones cuando Claude necesita entrada

Obtén una notificación de escritorio cada vez que Claude termine de trabajar y necesite tu entrada, para que puedas cambiar a otras tareas sin verificar la terminal.

Este hook usa el evento `Notification`, que se activa cuando Claude está esperando entrada o permiso. Cada pestaña a continuación usa el comando de notificación nativo de la plataforma. Añade esto a `~/.claude/settings.json`:

<Tabs>
  <Tab title="macOS">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Linux">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "notify-send 'Claude Code' 'Claude Code needs your attention'"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Windows (PowerShell)">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "powershell.exe -Command \"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')\""
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>
</Tabs>

### Formatea automáticamente el código después de ediciones

Ejecuta automáticamente [Prettier](https://prettier.io/) en cada archivo que Claude edita, para que el formato se mantenga consistente sin intervención manual.

Este hook usa el evento `PostToolUse` con un matcher `Edit|Write`, por lo que se ejecuta solo después de herramientas de edición de archivos. El comando extrae la ruta del archivo editado con [`jq`](https://jqlang.github.io/jq/) y la pasa a Prettier. Añade esto a `.claude/settings.json` en la raíz de tu proyecto:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

<Note>
  Los ejemplos de Bash en esta página usan `jq` para análisis JSON. Instálalo con `brew install jq` (macOS), `apt-get install jq` (Debian/Ubuntu), o consulta [descargas de `jq`](https://jqlang.github.io/jq/download/).
</Note>

### Bloquea ediciones a archivos protegidos

Evita que Claude modifique archivos sensibles como `.env`, `package-lock.json`, o cualquier cosa en `.git/`. Claude recibe retroalimentación explicando por qué se bloqueó la edición, para que pueda ajustar su enfoque.

Este ejemplo usa un archivo de script separado que el hook llama. El script verifica la ruta del archivo de destino contra una lista de patrones protegidos y sale con código 2 para bloquear la edición.

<Steps>
  <Step title="Crea el script del hook">
    Guarda esto en `.claude/hooks/protect-files.sh`:

    ```bash  theme={null}
    #!/bin/bash
    # protect-files.sh

    INPUT=$(cat)
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

    PROTECTED_PATTERNS=(".env" "package-lock.json" ".git/")

    for pattern in "${PROTECTED_PATTERNS[@]}"; do
      if [[ "$FILE_PATH" == *"$pattern"* ]]; then
        echo "Blocked: $FILE_PATH matches protected pattern '$pattern'" >&2
        exit 2
      fi
    done

    exit 0
    ```
  </Step>

  <Step title="Haz el script ejecutable (macOS/Linux)">
    Los scripts de hook deben ser ejecutables para que Claude Code los ejecute:

    ```bash  theme={null}
    chmod +x .claude/hooks/protect-files.sh
    ```
  </Step>

  <Step title="Registra el hook">
    Añade un hook `PreToolUse` a `.claude/settings.json` que ejecute el script antes de cualquier llamada a herramienta `Edit` o `Write`:

    ```json  theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Edit|Write",
            "hooks": [
              {
                "type": "command",
                "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Step>
</Steps>

### Reinyecta contexto después de compactación

Cuando la ventana de contexto de Claude se llena, la compactación resume la conversación para liberar espacio. Esto puede perder detalles importantes. Usa un hook `SessionStart` con un matcher `compact` para reinyectar contexto crítico después de cada compactación.

Cualquier texto que tu comando escriba en stdout se añade al contexto de Claude. Este ejemplo recuerda a Claude las convenciones del proyecto y el trabajo reciente. Añade esto a `.claude/settings.json` en la raíz de tu proyecto:

```json  theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Reminder: use Bun, not npm. Run bun test before committing. Current sprint: auth refactor.'"
          }
        ]
      }
    ]
  }
}
```

Puedes reemplazar el `echo` con cualquier comando que produzca salida dinámica, como `git log --oneline -5` para mostrar commits recientes. Para inyectar contexto en cada inicio de sesión, considera usar [CLAUDE.md](/es/memory) en su lugar. Para variables de entorno, consulta [`CLAUDE_ENV_FILE`](/es/hooks#persist-environment-variables) en la referencia.

### Audita cambios de configuración

Realiza un seguimiento de cuándo los archivos de configuración o skills cambian durante una sesión. El evento `ConfigChange` se activa cuando un proceso externo o editor modifica un archivo de configuración, para que puedas registrar cambios para cumplimiento o bloquear modificaciones no autorizadas.

Este ejemplo añade cada cambio a un registro de auditoría. Añade esto a `~/.claude/settings.json`:

```json  theme={null}
{
  "hooks": {
    "ConfigChange": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "jq -c '{timestamp: now | todate, source: .source, file: .file_path}' >> ~/claude-config-audit.log"
          }
        ]
      }
    ]
  }
}
```

El matcher filtra por tipo de configuración: `user_settings`, `project_settings`, `local_settings`, `policy_settings`, o `skills`. Para bloquear que un cambio tenga efecto, sal con código 2 o devuelve `{"decision": "block"}`. Consulta la [referencia de ConfigChange](/es/hooks#configchange) para el esquema de entrada completo.

### Recarga el entorno cuando el directorio o los archivos cambian

Algunos proyectos establecen diferentes variables de entorno dependiendo de en qué directorio estés. Herramientas como [direnv](https://direnv.net/) hacen esto automáticamente en tu shell, pero la herramienta Bash de Claude no recoge esos cambios por sí sola.

Un hook `CwdChanged` arregla esto: se ejecuta cada vez que Claude cambia de directorio, para que puedas recargar las variables correctas para la nueva ubicación. El hook escribe los valores actualizados en `CLAUDE_ENV_FILE`, que Claude Code aplica antes de cada comando Bash. Añade esto a `~/.claude/settings.json`:

```json  theme={null}
{
  "hooks": {
    "CwdChanged": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "direnv export bash >> \"$CLAUDE_ENV_FILE\""
          }
        ]
      }
    ]
  }
}
```

Para reaccionar a archivos específicos en lugar de cada cambio de directorio, usa `FileChanged` con un `matcher` listando los nombres de archivo a observar (separados por tuberías). El `matcher` tanto configura qué archivos observar como filtra qué hooks se ejecutan. Este ejemplo observa `.envrc` y `.env` para cambios en el directorio actual:

```json  theme={null}
{
  "hooks": {
    "FileChanged": [
      {
        "matcher": ".envrc|.env",
        "hooks": [
          {
            "type": "command",
            "command": "direnv export bash >> \"$CLAUDE_ENV_FILE\""
          }
        ]
      }
    ]
  }
}
```

Consulta las entradas de referencia [CwdChanged](/es/hooks#cwdchanged) y [FileChanged](/es/hooks#filechanged) para esquemas de entrada, salida `watchPaths`, y detalles de `CLAUDE_ENV_FILE`.

### Aprueba automáticamente avisos de permiso específicos

Omite el diálogo de aprobación para llamadas a herramientas que siempre permites. Este ejemplo aprueba automáticamente `ExitPlanMode`, la herramienta que Claude llama cuando termina de presentar un plan y pide proceder, para que no se te solicite cada vez que un plan esté listo.

A diferencia de los ejemplos de código de salida anteriores, la aprobación automática requiere que tu hook escriba una decisión JSON en stdout. Un hook `PermissionRequest` se activa cuando Claude Code está a punto de mostrar un diálogo de permiso, y devolver `"behavior": "allow"` lo responde en tu nombre.

El matcher limita el hook a `ExitPlanMode` solamente, para que ningún otro aviso se vea afectado. Añade esto a `~/.claude/settings.json`:

```json  theme={null}
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "ExitPlanMode",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\": {\"hookEventName\": \"PermissionRequest\", \"decision\": {\"behavior\": \"allow\"}}}'"
          }
        ]
      }
    ]
  }
}
```

Cuando el hook aprueba, Claude Code sale del modo plan y restaura cualquier modo de permiso que estuviera activo antes de entrar en modo plan. La transcripción muestra "Allowed by PermissionRequest hook" donde habría aparecido el diálogo. La ruta del hook siempre mantiene la conversación actual: no puede limpiar contexto e iniciar una sesión de implementación fresca de la manera que el diálogo puede.

Para establecer un modo de permiso específico en su lugar, la salida de tu hook puede incluir un array `updatedPermissions` con una entrada `setMode`. El valor `mode` es cualquier modo de permiso como `default`, `acceptEdits`, o `bypassPermissions`, y `destination: "session"` lo aplica solo para la sesión actual.

Para cambiar la sesión a `acceptEdits`, tu hook escribe este JSON en stdout:

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedPermissions": [
        { "type": "setMode", "mode": "acceptEdits", "destination": "session" }
      ]
    }
  }
}
```

Mantén el matcher lo más estrecho posible. Coincidir con `.*` o dejar el matcher vacío aprobaría automáticamente cada aviso de permiso, incluyendo escrituras de archivos y comandos de shell. Consulta la [referencia de PermissionRequest](/es/hooks#permissionrequest-decision-control) para el conjunto completo de campos de decisión.

## Cómo funcionan los hooks

Los eventos de hook se activan en puntos específicos del ciclo de vida de Claude Code. Cuando se activa un evento, todos los hooks coincidentes se ejecutan en paralelo, y los comandos de hook idénticos se deduplicarán automáticamente. La tabla a continuación muestra cada evento y cuándo se activa:

| Event                | When it fires                                                                                                                                          |
| :------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`       | When a session begins or resumes                                                                                                                       |
| `UserPromptSubmit`   | When you submit a prompt, before Claude processes it                                                                                                   |
| `PreToolUse`         | Before a tool call executes. Can block it                                                                                                              |
| `PermissionRequest`  | When a permission dialog appears                                                                                                                       |
| `PostToolUse`        | After a tool call succeeds                                                                                                                             |
| `PostToolUseFailure` | After a tool call fails                                                                                                                                |
| `Notification`       | When Claude Code sends a notification                                                                                                                  |
| `SubagentStart`      | When a subagent is spawned                                                                                                                             |
| `SubagentStop`       | When a subagent finishes                                                                                                                               |
| `TaskCreated`        | When a task is being created via `TaskCreate`                                                                                                          |
| `TaskCompleted`      | When a task is being marked as completed                                                                                                               |
| `Stop`               | When Claude finishes responding                                                                                                                        |
| `StopFailure`        | When the turn ends due to an API error. Output and exit code are ignored                                                                               |
| `TeammateIdle`       | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                                     |
| `InstructionsLoaded` | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session         |
| `ConfigChange`       | When a configuration file changes during a session                                                                                                     |
| `CwdChanged`         | When the working directory changes, for example when Claude executes a `cd` command. Useful for reactive environment management with tools like direnv |
| `FileChanged`        | When a watched file changes on disk. The `matcher` field specifies which filenames to watch                                                            |
| `WorktreeCreate`     | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                            |
| `WorktreeRemove`     | When a worktree is being removed, either at session exit or when a subagent finishes                                                                   |
| `PreCompact`         | Before context compaction                                                                                                                              |
| `PostCompact`        | After context compaction completes                                                                                                                     |
| `Elicitation`        | When an MCP server requests user input during a tool call                                                                                              |
| `ElicitationResult`  | After a user responds to an MCP elicitation, before the response is sent back to the server                                                            |
| `SessionEnd`         | When a session terminates                                                                                                                              |

Cada hook tiene un `type` que determina cómo se ejecuta. La mayoría de los hooks usan `"type": "command"`, que ejecuta un comando de shell. Hay otros tres tipos disponibles:

* `"type": "http"`: POST de datos de evento a una URL. Consulta [HTTP hooks](#http-hooks).
* `"type": "prompt"`: evaluación LLM de un solo turno. Consulta [Hooks basados en prompts](#prompt-based-hooks).
* `"type": "agent"`: verificación multi-turno con acceso a herramientas. Consulta [Hooks basados en agentes](#agent-based-hooks).

### Lee entrada y devuelve salida

Los hooks se comunican con Claude Code a través de stdin, stdout, stderr y códigos de salida. Cuando se activa un evento, Claude Code pasa datos específicos del evento como JSON a stdin de tu script. Tu script lee esos datos, hace su trabajo, y le dice a Claude Code qué hacer a continuación a través del código de salida.

#### Entrada del hook

Cada evento incluye campos comunes como `session_id` y `cwd`, pero cada tipo de evento añade datos diferentes. Por ejemplo, cuando Claude ejecuta un comando Bash, un hook `PreToolUse` recibe algo como esto en stdin:

```json  theme={null}
{
  "session_id": "abc123",          // ID único para esta sesión
  "cwd": "/Users/sarah/myproject", // directorio de trabajo cuando se activó el evento
  "hook_event_name": "PreToolUse", // qué evento activó este hook
  "tool_name": "Bash",             // la herramienta que Claude está a punto de usar
  "tool_input": {                  // los argumentos que Claude pasó a la herramienta
    "command": "npm test"          // para Bash, este es el comando de shell
  }
}
```

Tu script puede analizar ese JSON y actuar sobre cualquiera de esos campos. Los hooks `UserPromptSubmit` obtienen el texto `prompt` en su lugar, los hooks `SessionStart` obtienen la `source` (startup, resume, clear, compact), y así sucesivamente. Consulta [Campos de entrada comunes](/es/hooks#common-input-fields) en la referencia para campos compartidos, y la sección de cada evento para esquemas específicos del evento.

#### Salida del hook

Tu script le dice a Claude Code qué hacer a continuación escribiendo en stdout o stderr y saliendo con un código específico. Por ejemplo, un hook `PreToolUse` que quiere bloquear un comando:

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q "drop table"; then
  echo "Blocked: dropping tables is not allowed" >&2  // stderr se convierte en retroalimentación de Claude
  exit 2 // exit 2 = bloquea la acción
fi

exit 0  // exit 0 = permite que proceda
```

El código de salida determina qué sucede a continuación:

* **Exit 0**: la acción procede. Para hooks `UserPromptSubmit` y `SessionStart`, cualquier cosa que escribas en stdout se añade al contexto de Claude.
* **Exit 2**: la acción se bloquea. Escribe una razón en stderr, y Claude la recibe como retroalimentación para que pueda ajustar.
* **Cualquier otro código de salida**: la acción procede. Stderr se registra pero no se muestra a Claude. Alterna el modo detallado con `Ctrl+O` para ver estos mensajes en la transcripción.

#### Salida JSON estructurada

Los códigos de salida te dan dos opciones: permitir o bloquear. Para más control, sal con 0 e imprime un objeto JSON a stdout en su lugar.

<Note>
  Usa exit 2 para bloquear con un mensaje de stderr, o exit 0 con JSON para control estructurado. No los mezcles: Claude Code ignora JSON cuando sales con 2.
</Note>

Por ejemplo, un hook `PreToolUse` puede negar una llamada a herramienta y decirle a Claude por qué, o escalarla al usuario para aprobación:

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Use rg instead of grep for better performance"
  }
}
```

Claude Code lee `permissionDecision` y cancela la llamada a herramienta, luego alimenta `permissionDecisionReason` de vuelta a Claude como retroalimentación. Estas tres opciones son específicas de `PreToolUse`:

* `"allow"`: procede sin mostrar un aviso de permiso
* `"deny"`: cancela la llamada a herramienta y envía la razón a Claude
* `"ask"`: muestra el aviso de permiso al usuario como es normal

Devolver `"allow"` omite el aviso interactivo pero no anula [reglas de permiso](/es/permissions#manage-permissions). Si una regla de negación coincide con la llamada a herramienta, la llamada se bloquea incluso cuando tu hook devuelve `"allow"`. Si una regla de solicitud coincide, el usuario sigue siendo solicitado. Esto significa que las reglas de negación de cualquier ámbito de configuración, incluyendo [configuración gestionada](/es/settings#settings-files), siempre tienen prioridad sobre las aprobaciones de hooks.

Otros eventos usan patrones de decisión diferentes. Por ejemplo, los hooks `PostToolUse` y `Stop` usan un campo `decision: "block"` de nivel superior, mientras que `PermissionRequest` usa `hookSpecificOutput.decision.behavior`. Consulta la [tabla de resumen](/es/hooks#decision-control) en la referencia para un desglose completo por evento.

Para hooks `UserPromptSubmit`, usa `additionalContext` en su lugar para inyectar texto en el contexto de Claude. Los hooks basados en prompts (`type: "prompt"`) manejan la salida de manera diferente: consulta [Hooks basados en prompts](#prompt-based-hooks).

### Filtra hooks con matchers

Sin un matcher, un hook se activa en cada ocurrencia de su evento. Los matchers te permiten estrecharlo. Por ejemplo, si quieres ejecutar un formateador solo después de ediciones de archivos (no después de cada llamada a herramienta), añade un matcher a tu hook `PostToolUse`:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "prettier --write ..." }
        ]
      }
    ]
  }
}
```

El matcher `"Edit|Write"` es un patrón regex que coincide con el nombre de la herramienta. El hook solo se activa cuando Claude usa la herramienta `Edit` o `Write`, no cuando usa `Bash`, `Read`, u otra herramienta.

Cada tipo de evento coincide en un campo específico. Los matchers soportan cadenas exactas y patrones regex:

| Evento                                                                                                        | En qué filtra el matcher                          | Valores de matcher de ejemplo                                                                                             |
| :------------------------------------------------------------------------------------------------------------ | :------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------ |
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`                                        | nombre de herramienta                             | `Bash`, `Edit\|Write`, `mcp__.*`                                                                                          |
| `SessionStart`                                                                                                | cómo comenzó la sesión                            | `startup`, `resume`, `clear`, `compact`                                                                                   |
| `SessionEnd`                                                                                                  | por qué terminó la sesión                         | `clear`, `resume`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`                                  |
| `Notification`                                                                                                | tipo de notificación                              | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`                                                  |
| `SubagentStart`                                                                                               | tipo de agente                                    | `Bash`, `Explore`, `Plan`, o nombres de agentes personalizados                                                            |
| `PreCompact`, `PostCompact`                                                                                   | qué activó la compactación                        | `manual`, `auto`                                                                                                          |
| `SubagentStop`                                                                                                | tipo de agente                                    | los mismos valores que `SubagentStart`                                                                                    |
| `ConfigChange`                                                                                                | fuente de configuración                           | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills`                                        |
| `StopFailure`                                                                                                 | tipo de error                                     | `rate_limit`, `authentication_failed`, `billing_error`, `invalid_request`, `server_error`, `max_output_tokens`, `unknown` |
| `InstructionsLoaded`                                                                                          | razón de carga                                    | `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact`                                              |
| `Elicitation`                                                                                                 | nombre del servidor MCP                           | tus nombres de servidor MCP configurados                                                                                  |
| `ElicitationResult`                                                                                           | nombre del servidor MCP                           | los mismos valores que `Elicitation`                                                                                      |
| `FileChanged`                                                                                                 | nombre de archivo (basename del archivo cambiado) | `.envrc`, `.env`, cualquier nombre de archivo que quieras observar                                                        |
| `UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove`, `CwdChanged` | sin soporte de matcher                            | siempre se activa en cada ocurrencia                                                                                      |

Algunos ejemplos más mostrando matchers en diferentes tipos de eventos:

<Tabs>
  <Tab title="Registra cada comando Bash">
    Coincide solo con llamadas a herramienta `Bash` y registra cada comando en un archivo. El evento `PostToolUse` se activa después de que el comando se completa, por lo que `tool_input.command` contiene lo que se ejecutó. El hook recibe los datos del evento como JSON en stdin, y `jq -r '.tool_input.command'` extrae solo la cadena de comando, que `>>` añade al archivo de registro:

    ```json  theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Bash",
            "hooks": [
              {
                "type": "command",
                "command": "jq -r '.tool_input.command' >> ~/.claude/command-log.txt"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Coincide con herramientas MCP">
    Las herramientas MCP usan una convención de nombres diferente a las herramientas integradas: `mcp__<server>__<tool>`, donde `<server>` es el nombre del servidor MCP y `<tool>` es la herramienta que proporciona. Por ejemplo, `mcp__github__search_repositories` o `mcp__filesystem__read_file`. Usa un matcher regex para dirigirse a todas las herramientas de un servidor específico, o coincide entre servidores con un patrón como `mcp__.*__write.*`. Consulta [Coincide con herramientas MCP](/es/hooks#match-mcp-tools) en la referencia para la lista completa de ejemplos.

    El comando a continuación extrae el nombre de la herramienta de la entrada JSON del hook con `jq` y lo escribe en stderr, donde aparece en modo detallado (`Ctrl+O`):

    ```json  theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "mcp__github__.*",
            "hooks": [
              {
                "type": "command",
                "command": "echo \"GitHub tool called: $(jq -r '.tool_name')\" >&2"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Limpia al final de la sesión">
    El evento `SessionEnd` soporta matchers en la razón por la que terminó la sesión. Este hook solo se activa en `clear` (cuando ejecutas `/clear`), no en salidas normales:

    ```json  theme={null}
    {
      "hooks": {
        "SessionEnd": [
          {
            "matcher": "clear",
            "hooks": [
              {
                "type": "command",
                "command": "rm -f /tmp/claude-scratch-*.txt"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>
</Tabs>

Para sintaxis de matcher completa, consulta la [referencia de Hooks](/es/hooks#configuration).

### Configura la ubicación del hook

Dónde añadas un hook determina su ámbito:

| Ubicación                                                  | Ámbito                                 | Compartible                                |
| :--------------------------------------------------------- | :------------------------------------- | :----------------------------------------- |
| `~/.claude/settings.json`                                  | Todos tus proyectos                    | No, local a tu máquina                     |
| `.claude/settings.json`                                    | Proyecto único                         | Sí, puede ser confirmado en el repositorio |
| `.claude/settings.local.json`                              | Proyecto único                         | No, gitignored                             |
| Configuración de política gestionada                       | Organización completa                  | Sí, controlado por administrador           |
| [Plugin](/es/plugins) `hooks/hooks.json`                   | Cuando el plugin está habilitado       | Sí, incluido con el plugin                 |
| [Skill](/es/skills) o [agente](/es/sub-agents) frontmatter | Mientras el skill o agente está activo | Sí, definido en el archivo del componente  |

Ejecuta [`/hooks`](/es/hooks#the-hooks-menu) en Claude Code para examinar todos los hooks configurados agrupados por evento. Para desactivar todos los hooks a la vez, establece `"disableAllHooks": true` en tu archivo de configuración.

Si editas archivos de configuración directamente mientras Claude Code está ejecutándose, el observador de archivos normalmente recoge cambios de hooks automáticamente.

## Hooks basados en prompts

Para decisiones que requieren criterio en lugar de reglas deterministas, usa hooks `type: "prompt"`. En lugar de ejecutar un comando de shell, Claude Code envía tu prompt y los datos de entrada del hook a un modelo Claude (Haiku por defecto) para tomar la decisión. Puedes especificar un modelo diferente con el campo `model` si necesitas más capacidad.

El único trabajo del modelo es devolver una decisión sí/no como JSON:

* `"ok": true`: la acción procede
* `"ok": false`: la acción se bloquea. La `"reason"` del modelo se alimenta de vuelta a Claude para que pueda ajustar.

Este ejemplo usa un hook `Stop` para preguntarle al modelo si todas las tareas solicitadas están completas. Si el modelo devuelve `"ok": false`, Claude sigue trabajando y usa la `reason` como su siguiente instrucción:

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if all tasks are complete. If not, respond with {\"ok\": false, \"reason\": \"what remains to be done\"}."
          }
        ]
      }
    ]
  }
}
```

Para opciones de configuración completas, consulta [Hooks basados en prompts](/es/hooks#prompt-based-hooks) en la referencia.

## Hooks basados en agentes

Cuando la verificación requiere inspeccionar archivos o ejecutar comandos, usa hooks `type: "agent"`. A diferencia de los hooks de prompt que hacen una sola llamada LLM, los hooks de agente generan un subagente que puede leer archivos, buscar código y usar otras herramientas para verificar condiciones antes de devolver una decisión.

Los hooks de agente usan el mismo formato de respuesta `"ok"` / `"reason"` que los hooks de prompt, pero con un tiempo de espera predeterminado más largo de 60 segundos y hasta 50 turnos de uso de herramientas.

Este ejemplo verifica que las pruebas pasen antes de permitir que Claude se detenga:

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

Usa hooks de prompt cuando los datos de entrada del hook por sí solos son suficientes para tomar una decisión. Usa hooks de agente cuando necesites verificar algo contra el estado real del código base.

Para opciones de configuración completas, consulta [Hooks basados en agentes](/es/hooks#agent-based-hooks) en la referencia.

## HTTP hooks

Usa hooks `type: "http"` para POST de datos de evento a un punto final HTTP en lugar de ejecutar un comando de shell. El punto final recibe el mismo JSON que un hook de comando recibiría en stdin, y devuelve resultados a través del cuerpo de respuesta HTTP usando el mismo formato JSON.

Los HTTP hooks son útiles cuando quieres que un servidor web, función en la nube o servicio externo maneje la lógica del hook: por ejemplo, un servicio de auditoría compartido que registra eventos de uso de herramientas en un equipo.

Este ejemplo publica cada uso de herramienta a un servicio de registro local:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/tool-use",
            "headers": {
              "Authorization": "Bearer $MY_TOKEN"
            },
            "allowedEnvVars": ["MY_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

El punto final debe devolver un cuerpo de respuesta JSON usando el mismo [formato de salida](/es/hooks#json-output) que los hooks de comando. Para bloquear una llamada a herramienta, devuelve una respuesta 2xx con los campos `hookSpecificOutput` apropiados. Los códigos de estado HTTP por sí solos no pueden bloquear acciones.

Los valores de encabezado soportan interpolación de variables de entorno usando la sintaxis `$VAR_NAME` o `${VAR_NAME}`. Solo las variables listadas en el array `allowedEnvVars` se resuelven; todas las otras referencias `$VAR` permanecen vacías.

Para opciones de configuración completas y manejo de respuestas, consulta [HTTP hooks](/es/hooks#http-hook-fields) en la referencia.

## Limitaciones y solución de problemas

### Limitaciones

* Los hooks de comando se comunican solo a través de stdout, stderr y códigos de salida. No pueden activar comandos o llamadas a herramientas directamente. Los HTTP hooks se comunican a través del cuerpo de respuesta en su lugar.
* El tiempo de espera del hook es 10 minutos por defecto, configurable por hook con el campo `timeout` (en segundos).
* Los hooks `PostToolUse` no pueden deshacer acciones ya que la herramienta ya se ha ejecutado.
* Los hooks `PermissionRequest` no se activan en [modo no interactivo](/es/headless) (`-p`). Usa hooks `PreToolUse` para decisiones de permiso automatizadas.
* Los hooks `Stop` se activan cada vez que Claude termina de responder, no solo en la finalización de tareas. No se activan en interrupciones del usuario. Los errores de API activan [StopFailure](/es/hooks#stopfailure) en su lugar.

### Hook no se activa

El hook está configurado pero nunca se ejecuta.

* Ejecuta `/hooks` y confirma que el hook aparece bajo el evento correcto
* Verifica que el patrón del matcher coincida exactamente con el nombre de la herramienta (los matchers distinguen mayúsculas de minúsculas)
* Verifica que estés activando el tipo de evento correcto (por ejemplo, `PreToolUse` se activa antes de la ejecución de la herramienta, `PostToolUse` se activa después)
* Si usas hooks `PermissionRequest` en modo no interactivo (`-p`), cambia a `PreToolUse` en su lugar

### Error de hook en la salida

Ves un mensaje como "PreToolUse hook error: ..." en la transcripción.

* Tu script salió con un código no cero inesperadamente. Pruébalo manualmente canalizando JSON de muestra:
  ```bash  theme={null}
  echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./my-hook.sh
  echo $?  // Verifica el código de salida
  ```
* Si ves "command not found", usa rutas absolutas o `$CLAUDE_PROJECT_DIR` para referenciar scripts
* Si ves "jq: command not found", instala `jq` o usa Python/Node.js para análisis JSON
* Si el script no se ejecuta en absoluto, hazlo ejecutable: `chmod +x ./my-hook.sh`

### `/hooks` no muestra hooks configurados

Editaste un archivo de configuración pero los hooks no aparecen en el menú.

* Las ediciones de archivos normalmente se recogen automáticamente. Si no han aparecido después de unos segundos, el observador de archivos puede haber perdido el cambio: reinicia tu sesión para forzar una recarga.
* Verifica que tu JSON sea válido (las comas finales y comentarios no están permitidos)
* Confirma que el archivo de configuración está en la ubicación correcta: `.claude/settings.json` para hooks de proyecto, `~/.claude/settings.json` para hooks globales

### El hook Stop se ejecuta para siempre

Claude sigue trabajando en un bucle infinito en lugar de detenerse.

Tu script de hook Stop necesita verificar si ya activó una continuación. Analiza el campo `stop_hook_active` de la entrada JSON y sal temprano si es `true`:

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0  // Permite que Claude se detenga
fi
// ... resto de tu lógica de hook
```

### Falló la validación JSON

Claude Code muestra un error de análisis JSON aunque tu script de hook produzca JSON válido.

Cuando Claude Code ejecuta un hook, genera un shell que obtiene tu perfil (`~/.zshrc` o `~/.bashrc`). Si tu perfil contiene declaraciones `echo` incondicionales, esa salida se antepone a tu JSON del hook:

```text  theme={null}
Shell ready on arm64
{"decision": "block", "reason": "Not allowed"}
```

Claude Code intenta analizar esto como JSON y falla. Para arreglarlo, envuelve las declaraciones echo en tu perfil de shell para que solo se ejecuten en shells interactivos:

```bash  theme={null}
# En ~/.zshrc o ~/.bashrc
if [[ $- == *i* ]]; then
  echo "Shell ready"
fi
```

La variable `$-` contiene banderas de shell, e `i` significa interactivo. Los hooks se ejecutan en shells no interactivos, por lo que el echo se omite.

### Técnicas de depuración

Alterna el modo detallado con `Ctrl+O` para ver la salida del hook en la transcripción, o ejecuta `claude --debug` para detalles de ejecución completos incluyendo qué hooks coincidieron y sus códigos de salida.

## Aprende más

* [Referencia de Hooks](/es/hooks): esquemas de eventos completos, formato de salida JSON, hooks asincronos y hooks de herramientas MCP
* [Consideraciones de seguridad](/es/hooks#security-considerations): revisa antes de desplegar hooks en entornos compartidos o de producción
* [Ejemplo de validador de comandos Bash](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py): implementación de referencia completa
