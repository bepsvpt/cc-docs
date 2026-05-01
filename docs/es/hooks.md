> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Referencia de hooks

> Referencia para eventos de hooks de Claude Code, esquema de configuración, formatos de entrada/salida JSON, códigos de salida, hooks asincronos, hooks HTTP, hooks de prompt y hooks de herramientas MCP.

<Tip>
  Para una guía de inicio rápido con ejemplos, consulte [Automatizar flujos de trabajo con hooks](/es/hooks-guide).
</Tip>

Los hooks son comandos de shell definidos por el usuario, puntos finales HTTP o prompts de LLM que se ejecutan automáticamente en puntos específicos del ciclo de vida de Claude Code. Utilice esta referencia para buscar esquemas de eventos, opciones de configuración, formatos de entrada/salida JSON y características avanzadas como hooks asincronos, hooks HTTP y hooks de herramientas MCP. Si está configurando hooks por primera vez, comience con la [guía](/es/hooks-guide) en su lugar.

## Ciclo de vida de los hooks

Los hooks se activan en puntos específicos durante una sesión de Claude Code. Cuando se activa un evento y un matcher coincide, Claude Code pasa contexto JSON sobre el evento a su controlador de hook. Para hooks de comando, la entrada llega en stdin. Para hooks HTTP, llega como el cuerpo de la solicitud POST. Su controlador puede entonces inspeccionar la entrada, tomar medidas y opcionalmente devolver una decisión. Los eventos se dividen en tres cadencias: una vez por sesión (`SessionStart`, `SessionEnd`), una vez por turno (`UserPromptSubmit`, `Stop`, `StopFailure`) y en cada llamada a herramienta dentro del bucle agentico (`PreToolUse`, `PostToolUse`):

<div style={{maxWidth: "500px", margin: "0 auto"}}>
  <Frame>
    <img src="https://mintcdn.com/claude-code/ZIW26Z9pnpsXLhbS/images/hooks-lifecycle.svg?fit=max&auto=format&n=ZIW26Z9pnpsXLhbS&q=85&s=ee23691324deb6501df09bfdae560b64" alt="Diagrama del ciclo de vida de hooks que muestra Setup opcional alimentando a SessionStart, luego un bucle por turno que contiene UserPromptSubmit, UserPromptExpansion para slash commands, el bucle agentico anidado (PreToolUse, PermissionRequest, PostToolUse, PostToolUseFailure, PostToolBatch, SubagentStart/Stop, TaskCreated, TaskCompleted) y Stop o StopFailure, seguido de TeammateIdle, PreCompact, PostCompact y SessionEnd, con Elicitation y ElicitationResult anidados dentro de la ejecución de herramientas MCP, PermissionDenied como una rama lateral de PermissionRequest para denegaciones en modo automático, y WorktreeCreate, WorktreeRemove, Notification, ConfigChange, InstructionsLoaded, CwdChanged y FileChanged como eventos asincronos independientes" width="520" height="1228" data-path="images/hooks-lifecycle.svg" />
  </Frame>
</div>

La tabla a continuación resume cuándo se activa cada evento. La sección [Hook events](#hook-events) documenta el esquema de entrada completo y las opciones de control de decisión para cada uno.

| Event                 | When it fires                                                                                                                                          |
| :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`        | When a session begins or resumes                                                                                                                       |
| `Setup`               | When you start Claude Code with `--init-only`, or with `--init` or `--maintenance` in `-p` mode. For one-time preparation in CI or scripts             |
| `UserPromptSubmit`    | When you submit a prompt, before Claude processes it                                                                                                   |
| `UserPromptExpansion` | When a user-typed command expands into a prompt, before it reaches Claude. Can block the expansion                                                     |
| `PreToolUse`          | Before a tool call executes. Can block it                                                                                                              |
| `PermissionRequest`   | When a permission dialog appears                                                                                                                       |
| `PermissionDenied`    | When a tool call is denied by the auto mode classifier. Return `{retry: true}` to tell the model it may retry the denied tool call                     |
| `PostToolUse`         | After a tool call succeeds                                                                                                                             |
| `PostToolUseFailure`  | After a tool call fails                                                                                                                                |
| `PostToolBatch`       | After a full batch of parallel tool calls resolves, before the next model call                                                                         |
| `Notification`        | When Claude Code sends a notification                                                                                                                  |
| `SubagentStart`       | When a subagent is spawned                                                                                                                             |
| `SubagentStop`        | When a subagent finishes                                                                                                                               |
| `TaskCreated`         | When a task is being created via `TaskCreate`                                                                                                          |
| `TaskCompleted`       | When a task is being marked as completed                                                                                                               |
| `Stop`                | When Claude finishes responding                                                                                                                        |
| `StopFailure`         | When the turn ends due to an API error. Output and exit code are ignored                                                                               |
| `TeammateIdle`        | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                                     |
| `InstructionsLoaded`  | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session         |
| `ConfigChange`        | When a configuration file changes during a session                                                                                                     |
| `CwdChanged`          | When the working directory changes, for example when Claude executes a `cd` command. Useful for reactive environment management with tools like direnv |
| `FileChanged`         | When a watched file changes on disk. The `matcher` field specifies which filenames to watch                                                            |
| `WorktreeCreate`      | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                            |
| `WorktreeRemove`      | When a worktree is being removed, either at session exit or when a subagent finishes                                                                   |
| `PreCompact`          | Before context compaction                                                                                                                              |
| `PostCompact`         | After context compaction completes                                                                                                                     |
| `Elicitation`         | When an MCP server requests user input during a tool call                                                                                              |
| `ElicitationResult`   | After a user responds to an MCP elicitation, before the response is sent back to the server                                                            |
| `SessionEnd`          | When a session terminates                                                                                                                              |

### Cómo se resuelve un hook

Para ver cómo encajan estas piezas, considere este hook `PreToolUse` que bloquea comandos de shell destructivos. El `matcher` se reduce a llamadas a herramientas Bash y la condición `if` se reduce aún más a subcomandos Bash que coinciden con `rm *`, por lo que `block-rm.sh` solo se genera cuando ambos filtros coinciden:

```json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-rm.sh"
          }
        ]
      }
    ]
  }
}
```

El script lee la entrada JSON desde stdin, extrae el comando y devuelve una `permissionDecision` de `"deny"` si contiene `rm -rf`:

```bash theme={null}
#!/bin/bash
# .claude/hooks/block-rm.sh
COMMAND=$(jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q 'rm -rf'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Destructive command blocked by hook"
    }
  }'
else
  exit 0  # allow the command
fi
```

Ahora suponga que Claude Code decide ejecutar `Bash "rm -rf /tmp/build"`. Esto es lo que sucede:

<Frame>
  <img src="https://mintcdn.com/claude-code/-tYw1BD_DEqfyyOZ/images/hook-resolution.svg?fit=max&auto=format&n=-tYw1BD_DEqfyyOZ&q=85&s=c73ebc1eeda2037570427d7af1e0a891" alt="Flujo de resolución de hooks: se activa el evento PreToolUse, el matcher verifica la coincidencia de Bash, la condición if verifica la coincidencia de Bash(rm *), se ejecuta el controlador de hooks, el resultado se devuelve a Claude Code" width="930" height="290" data-path="images/hook-resolution.svg" />
</Frame>

<Steps>
  <Step title="Se activa el evento">
    El evento `PreToolUse` se activa. Claude Code envía la entrada de la herramienta como JSON en stdin al hook:

    ```json theme={null}
    { "tool_name": "Bash", "tool_input": { "command": "rm -rf /tmp/build" }, ... }
    ```
  </Step>

  <Step title="El matcher verifica">
    El matcher `"Bash"` coincide con el nombre de la herramienta, por lo que se activa este grupo de hooks. Si omite el matcher o usa `"*"`, el grupo se activa en cada ocurrencia del evento.
  </Step>

  <Step title="La condición if verifica">
    La condición `if` `"Bash(rm *)"` coincide porque `rm -rf /tmp/build` es un subcomando que coincide con `rm *`, por lo que se genera este controlador. Si el comando hubiera sido `npm test`, la verificación `if` habría fallado y `block-rm.sh` nunca se habría ejecutado, evitando la sobrecarga de generación de procesos. El campo `if` es opcional; sin él, cada controlador en el grupo coincidente se ejecuta.
  </Step>

  <Step title="Se ejecuta el controlador de hooks">
    El script inspecciona el comando completo y encuentra `rm -rf`, por lo que imprime una decisión en stdout:

    ```json theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Destructive command blocked by hook"
      }
    }
    ```

    Si el comando hubiera sido una variante más segura de `rm` como `rm file.txt`, el script habría alcanzado `exit 0` en su lugar, lo que le dice a Claude Code que permita la llamada a la herramienta sin más acciones.
  </Step>

  <Step title="Claude Code actúa sobre el resultado">
    Claude Code lee la decisión JSON, bloquea la llamada a la herramienta y muestra a Claude la razón.
  </Step>
</Steps>

La sección [Configuration](#configuration) a continuación documenta el esquema completo, y cada sección [hook event](#hook-events) documenta qué entrada recibe su comando y qué salida puede devolver.

## Configuración

Los hooks se definen en archivos de configuración JSON. La configuración tiene tres niveles de anidamiento:

1. Elija un [hook event](#hook-events) al que responder, como `PreToolUse` o `Stop`
2. Agregue un [matcher group](#matcher-patterns) para filtrar cuándo se activa, como "solo para la herramienta Bash"
3. Defina uno o más [hook handlers](#hook-handler-fields) para ejecutar cuando coincida

Consulte [Cómo se resuelve un hook](#how-a-hook-resolves) arriba para un recorrido completo con un ejemplo anotado.

<Note>
  Esta página utiliza términos específicos para cada nivel: **hook event** para el punto del ciclo de vida, **matcher group** para el filtro y **hook handler** para el comando de shell, punto final HTTP, herramienta MCP, prompt o agente que se ejecuta. "Hook" por sí solo se refiere a la característica general.
</Note>

### Ubicaciones de hooks

Dónde defina un hook determina su alcance:

| Ubicación                                                 | Alcance                            | Compartible                                |
| :-------------------------------------------------------- | :--------------------------------- | :----------------------------------------- |
| `~/.claude/settings.json`                                 | Todos sus proyectos                | No, local en su máquina                    |
| `.claude/settings.json`                                   | Proyecto único                     | Sí, puede ser confirmado en el repositorio |
| `.claude/settings.local.json`                             | Proyecto único                     | No, ignorado por git                       |
| Configuración de política administrada                    | Toda la organización               | Sí, controlado por administrador           |
| [Plugin](/es/plugins) `hooks/hooks.json`                  | Cuando el plugin está habilitado   | Sí, incluido con el plugin                 |
| [Skill](/es/skills) o [agent](/es/sub-agents) frontmatter | Mientras el componente está activo | Sí, definido en el archivo del componente  |

Para obtener detalles sobre la resolución de archivos de configuración, consulte [settings](/es/settings). Los administradores empresariales pueden usar `allowManagedHooksOnly` para bloquear hooks de usuario, proyecto y plugin. Los hooks de plugins habilitados forzosamente en la configuración administrada `enabledPlugins` están exentos, por lo que los administradores pueden distribuir hooks verificados a través de un mercado de la organización. Consulte [Hook configuration](/es/settings#hook-configuration).

### Patrones de matcher

El campo `matcher` filtra cuándo se activan los hooks. Cómo se evalúa un matcher depende de los caracteres que contenga:

| Valor del matcher                | Evaluado como                                                | Ejemplo                                                                                                                                         |
| :------------------------------- | :----------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| `"*"`, `""` u omitido            | Coincidir todo                                               | se activa en cada ocurrencia del evento                                                                                                         |
| Solo letras, dígitos, `_` y `\|` | Cadena exacta, o lista de cadenas exactas separadas por `\|` | `Bash` coincide solo con la herramienta Bash; `Edit\|Write` coincide con cualquiera de las herramientas exactamente                             |
| Contiene cualquier otro carácter | Expresión regular de JavaScript                              | `^Notebook` coincide con cualquier herramienta que comience con Notebook; `mcp__memory__.*` coincide con cada herramienta del servidor `memory` |

El evento `FileChanged` no sigue estas reglas al construir su lista de vigilancia. Consulte [FileChanged](#filechanged).

Cada tipo de evento coincide en un campo diferente:

| Evento                                                                                                                          | En qué filtra el matcher                                                      | Valores de matcher de ejemplo                                                                                                                      |
| :------------------------------------------------------------------------------------------------------------------------------ | :---------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`                                      | nombre de la herramienta                                                      | `Bash`, `Edit\|Write`, `mcp__.*`                                                                                                                   |
| `SessionStart`                                                                                                                  | cómo comenzó la sesión                                                        | `startup`, `resume`, `clear`, `compact`                                                                                                            |
| `Setup`                                                                                                                         | qué bandera CLI desencadenó la configuración                                  | `init`, `maintenance`                                                                                                                              |
| `SessionEnd`                                                                                                                    | por qué terminó la sesión                                                     | `clear`, `resume`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`                                                           |
| `Notification`                                                                                                                  | tipo de notificación                                                          | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`, `elicitation_complete`, `elicitation_response`                           |
| `SubagentStart`                                                                                                                 | tipo de agente                                                                | `general-purpose`, `Explore`, `Plan` o nombres de agentes personalizados                                                                           |
| `PreCompact`, `PostCompact`                                                                                                     | qué desencadenó la compactación                                               | `manual`, `auto`                                                                                                                                   |
| `SubagentStop`                                                                                                                  | tipo de agente                                                                | los mismos valores que `SubagentStart`                                                                                                             |
| `ConfigChange`                                                                                                                  | fuente de configuración                                                       | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills`                                                                 |
| `CwdChanged`                                                                                                                    | sin soporte de matcher                                                        | siempre se activa en cada cambio de directorio                                                                                                     |
| `FileChanged`                                                                                                                   | nombres de archivo literales a vigilar (consulte [FileChanged](#filechanged)) | `.envrc\|.env`                                                                                                                                     |
| `StopFailure`                                                                                                                   | tipo de error                                                                 | `rate_limit`, `authentication_failed`, `oauth_org_not_allowed`, `billing_error`, `invalid_request`, `server_error`, `max_output_tokens`, `unknown` |
| `InstructionsLoaded`                                                                                                            | razón de carga                                                                | `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact`                                                                       |
| `UserPromptExpansion`                                                                                                           | nombre del comando                                                            | sus nombres de skill o comando                                                                                                                     |
| `Elicitation`                                                                                                                   | nombre del servidor MCP                                                       | sus nombres de servidor MCP configurados                                                                                                           |
| `ElicitationResult`                                                                                                             | nombre del servidor MCP                                                       | los mismos valores que `Elicitation`                                                                                                               |
| `UserPromptSubmit`, `PostToolBatch`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` | sin soporte de matcher                                                        | siempre se activa en cada ocurrencia                                                                                                               |

El matcher se ejecuta contra un campo de la [entrada JSON](#hook-input-and-output) que Claude Code envía a su hook en stdin. Para eventos de herramientas, ese campo es `tool_name`. Cada sección [hook event](#hook-events) enumera el conjunto completo de valores de matcher y el esquema de entrada para ese evento.

Este ejemplo ejecuta un script de linting solo cuando Claude escribe o edita un archivo:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/lint-check.sh"
          }
        ]
      }
    ]
  }
}
```

`UserPromptSubmit`, `PostToolBatch`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` y `CwdChanged` no admiten matchers y siempre se activan en cada ocurrencia. Si agrega un campo `matcher` a estos eventos, se ignora silenciosamente.

Para eventos de herramientas, puede filtrar más estrechamente estableciendo el campo [`if`](#common-fields) en controladores de hooks individuales. `if` utiliza [sintaxis de regla de permiso](/es/permissions) para coincidir con el nombre de la herramienta y los argumentos juntos, por lo que `"Bash(git *)"` se ejecuta cuando cualquier subcomando de la entrada de Bash coincide con `git *` y `"Edit(*.ts)"` se ejecuta solo para archivos TypeScript.

#### Coincidir herramientas MCP

Las herramientas del servidor [MCP](/es/mcp) aparecen como herramientas normales en eventos de herramientas (`PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`), por lo que puede hacerlas coincidir de la misma manera que cualquier otro nombre de herramienta.

Las herramientas MCP siguen el patrón de nomenclatura `mcp__<server>__<tool>`, por ejemplo:

* `mcp__memory__create_entities`: herramienta crear entidades del servidor Memory
* `mcp__filesystem__read_file`: herramienta leer archivo del servidor Filesystem
* `mcp__github__search_repositories`: herramienta de búsqueda del servidor GitHub

Para coincidir con cada herramienta de un servidor, agregue `.*` al prefijo del servidor. El `.*` es requerido: un matcher como `mcp__memory` contiene solo letras y guiones bajos, por lo que se compara como una cadena exacta y no coincide con ninguna herramienta.

* `mcp__memory__.*` coincide con todas las herramientas del servidor `memory`
* `mcp__.*__write.*` coincide con cualquier herramienta cuyo nombre comience con `write` de cualquier servidor

Este ejemplo registra todas las operaciones del servidor de memoria y valida operaciones de escritura de cualquier servidor MCP:

```json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

### Campos del controlador de hooks

Cada objeto en el array `hooks` interno es un controlador de hook: el comando de shell, punto final HTTP, herramienta MCP, prompt de LLM o agente que se ejecuta cuando el matcher coincide. Hay cinco tipos:

* **[Command hooks](#command-hook-fields)** (`type: "command"`): ejecutan un comando de shell. Su script recibe la [entrada JSON](#hook-input-and-output) del evento en stdin y comunica resultados a través de códigos de salida y stdout.
* **[HTTP hooks](#http-hook-fields)** (`type: "http"`): envían la entrada JSON del evento como una solicitud HTTP POST a una URL. El punto final comunica resultados a través del cuerpo de la respuesta usando el mismo [formato de salida JSON](#json-output) que los hooks de comando.
* **[MCP tool hooks](#mcp-tool-hook-fields)** (`type: "mcp_tool"`): llaman a una herramienta en un servidor [MCP](/es/mcp) ya conectado. La salida de texto de la herramienta se trata como stdout de hook de comando.
* **[Prompt hooks](#prompt-and-agent-hook-fields)** (`type: "prompt"`): envían un prompt a un modelo Claude para evaluación de un solo turno. El modelo devuelve una decisión sí/no como JSON. Consulte [Prompt-based hooks](#prompt-based-hooks).
* **[Agent hooks](#prompt-and-agent-hook-fields)** (`type: "agent"`): generan un subagente que puede usar herramientas como Read, Grep y Glob para verificar condiciones antes de devolver una decisión. Los hooks de agente son experimentales y pueden cambiar. Consulte [Agent-based hooks](#agent-based-hooks).

#### Campos comunes

Estos campos se aplican a todos los tipos de hooks:

| Campo           | Requerido | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| :-------------- | :-------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`          | sí        | `"command"`, `"http"`, `"mcp_tool"`, `"prompt"` o `"agent"`                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `if`            | no        | Sintaxis de regla de permiso para filtrar cuándo se ejecuta este hook, como `"Bash(git *)"` o `"Edit(*.ts)"`. El hook solo se genera si la llamada a herramienta coincide con el patrón, o si un comando Bash es demasiado complejo para analizar. Solo se evalúa en eventos de herramientas: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest` y `PermissionDenied`. En otros eventos, un hook con `if` establecido nunca se ejecuta. Utiliza la misma sintaxis que [reglas de permiso](/es/permissions) |
| `timeout`       | no        | Segundos antes de cancelar. Valores predeterminados: 600 para comando, 30 para prompt, 60 para agente                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `statusMessage` | no        | Mensaje de spinner personalizado mostrado mientras se ejecuta el hook                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `once`          | no        | Si es `true`, se ejecuta una vez por sesión y luego se elimina. Solo se honra para hooks declarados en [skill frontmatter](#hooks-in-skills-and-agents); se ignora en archivos de configuración y frontmatter de agente                                                                                                                                                                                                                                                                                                        |

El campo `if` contiene exactamente una regla de permiso. No hay sintaxis `&&`, `||` o de lista para combinar reglas; para aplicar múltiples condiciones, defina un controlador de hook separado para cada una. Para Bash, la regla se compara contra cada subcomando de la entrada de herramienta después de que se eliminan las asignaciones `VAR=value` iniciales, por lo que `if: "Bash(git push *)"` coincide tanto con `FOO=bar git push` como con `npm test && git push`. El hook se ejecuta si algún subcomando coincide, y siempre se ejecuta cuando el comando es demasiado complejo para analizar.

#### Campos de comando hook

Además de los [campos comunes](#common-fields), los hooks de comando aceptan estos campos:

| Campo         | Requerido | Descripción                                                                                                                                                                                                                                                                    |
| :------------ | :-------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `command`     | sí        | Comando de shell a ejecutar                                                                                                                                                                                                                                                    |
| `async`       | no        | Si es `true`, se ejecuta en segundo plano sin bloquear. Consulte [Run hooks in the background](#run-hooks-in-the-background)                                                                                                                                                   |
| `asyncRewake` | no        | Si es `true`, se ejecuta en segundo plano y despierta a Claude en código de salida 2. Implica `async`. El stderr del hook, o stdout si stderr está vacío, se muestra a Claude como un recordatorio del sistema para que pueda reaccionar a un fallo de fondo de larga duración |
| `shell`       | no        | Shell a usar para este hook. Acepta `"bash"` (predeterminado) o `"powershell"`. Establecer `"powershell"` ejecuta el comando a través de PowerShell en Windows. No requiere `CLAUDE_CODE_USE_POWERSHELL_TOOL` ya que los hooks generan PowerShell directamente                 |

#### Campos de hook HTTP

Además de los [campos comunes](#common-fields), los hooks HTTP aceptan estos campos:

| Campo            | Requerido | Descripción                                                                                                                                                                                                                                       |
| :--------------- | :-------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `url`            | sí        | URL a la que enviar la solicitud POST                                                                                                                                                                                                             |
| `headers`        | no        | Encabezados HTTP adicionales como pares clave-valor. Los valores admiten interpolación de variables de entorno usando la sintaxis `$VAR_NAME` o `${VAR_NAME}`. Solo se resuelven las variables enumeradas en `allowedEnvVars`                     |
| `allowedEnvVars` | no        | Lista de nombres de variables de entorno que pueden interpolarse en valores de encabezado. Las referencias a variables no enumeradas se reemplazan con cadenas vacías. Requerido para que funcione cualquier interpolación de variable de entorno |

Claude Code envía la [entrada JSON](#hook-input-and-output) del hook como el cuerpo de la solicitud POST con `Content-Type: application/json`. El cuerpo de la respuesta usa el mismo [formato de salida JSON](#json-output) que los hooks de comando.

El manejo de errores difiere de los hooks de comando: las respuestas que no son 2xx, los fallos de conexión y los tiempos de espera agotados producen errores sin bloqueo que permiten que la ejecución continúe. Para bloquear una llamada a herramienta o denegar un permiso, devuelva una respuesta 2xx con un cuerpo JSON que contenga `decision: "block"` o un `hookSpecificOutput` con `permissionDecision: "deny"`.

Este ejemplo envía eventos `PreToolUse` a un servicio de validación local, autenticándose con un token de la variable de entorno `MY_TOKEN`:

```json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/pre-tool-use",
            "timeout": 30,
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

#### Campos de hook de herramienta MCP

Además de los [campos comunes](#common-fields), los hooks de herramienta MCP aceptan estos campos:

| Campo    | Requerido | Descripción                                                                                                                                                                      |
| :------- | :-------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `server` | sí        | Nombre de un servidor MCP configurado. El servidor ya debe estar conectado; el hook nunca desencadena un flujo OAuth o de conexión                                               |
| `tool`   | sí        | Nombre de la herramienta a llamar en ese servidor                                                                                                                                |
| `input`  | no        | Argumentos pasados a la herramienta. Los valores de cadena admiten sustitución `${path}` de la [entrada JSON](#hook-input-and-output) del hook, como `"${tool_input.file_path}"` |

La salida de texto de la herramienta se trata como stdout de hook de comando: si se analiza como [salida JSON](#json-output) válida, se procesa como una decisión; de lo contrario, se muestra como texto sin formato. Si el servidor nombrado no está conectado, o la herramienta devuelve `isError: true`, el hook produce un error sin bloqueo y la ejecución continúa.

Los hooks de herramienta MCP están disponibles en cada evento de hook una vez que Claude Code se ha conectado a sus servidores MCP. `SessionStart` y `Setup` típicamente se activan antes de que los servidores terminen de conectarse, por lo que los hooks en esos eventos deben esperar el error "no conectado" en la primera ejecución.

Este ejemplo llama a la herramienta `security_scan` en el servidor MCP `my_server` después de cada `Write` o `Edit`, pasando la ruta del archivo editado:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "mcp_tool",
            "server": "my_server",
            "tool": "security_scan",
            "input": { "file_path": "${tool_input.file_path}" }
          }
        ]
      }
    ]
  }
}
```

#### Campos de hook de prompt y agente

Además de los [campos comunes](#common-fields), los hooks de prompt y agente aceptan estos campos:

| Campo    | Requerido | Descripción                                                                                                   |
| :------- | :-------- | :------------------------------------------------------------------------------------------------------------ |
| `prompt` | sí        | Texto del prompt a enviar al modelo. Use `$ARGUMENTS` como marcador de posición para la entrada JSON del hook |
| `model`  | no        | Modelo a usar para evaluación. Por defecto es un modelo rápido                                                |

Todos los hooks coincidentes se ejecutan en paralelo, y los controladores idénticos se deduplicarán automáticamente. Los hooks de comando se deduplicarán por cadena de comando, y los hooks HTTP se deduplicarán por URL. Los controladores se ejecutan en el directorio actual con el entorno de Claude Code. La variable de entorno `$CLAUDE_CODE_REMOTE` se establece en `"true"` en entornos web remotos y no se establece en la CLI local.

### Referenciar scripts por ruta

Use variables de entorno para referenciar scripts de hooks relativos a la raíz del proyecto o plugin, independientemente del directorio de trabajo cuando se ejecuta el hook:

* `$CLAUDE_PROJECT_DIR`: la raíz del proyecto. Envuelva entre comillas para manejar rutas con espacios.
* `${CLAUDE_PLUGIN_ROOT}`: el directorio raíz del plugin, para scripts incluidos con un [plugin](/es/plugins). Cambia en cada actualización de plugin.
* `${CLAUDE_PLUGIN_DATA}`: el [directorio de datos persistentes](/es/plugins-reference#persistent-data-directory) del plugin, para dependencias y estado que deben sobrevivir a las actualizaciones de plugin.

<Tabs>
  <Tab title="Scripts de proyecto">
    Este ejemplo usa `$CLAUDE_PROJECT_DIR` para ejecutar un verificador de estilo desde el directorio `.claude/hooks/` del proyecto después de cualquier llamada a herramienta `Write` o `Edit`:

    ```json theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-style.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Scripts de plugin">
    Defina hooks de plugin en `hooks/hooks.json` con un campo `description` opcional de nivel superior. Cuando se habilita un plugin, sus hooks se fusionan con sus hooks de usuario y proyecto.

    Este ejemplo ejecuta un script de formato incluido con el plugin:

    ```json theme={null}
    {
      "description": "Automatic code formatting",
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
                "timeout": 30
              }
            ]
          }
        ]
      }
    }
    ```

    Consulte la [referencia de componentes de plugin](/es/plugins-reference#hooks) para obtener detalles sobre cómo crear hooks de plugin.
  </Tab>
</Tabs>

### Hooks en skills y agentes

Además de archivos de configuración y plugins, los hooks pueden definirse directamente en [skills](/es/skills) y [subagentes](/es/sub-agents) usando frontmatter. Estos hooks se limitan al ciclo de vida del componente y solo se ejecutan cuando ese componente está activo.

Se admiten todos los eventos de hook. Para subagentes, los hooks `Stop` se convierten automáticamente a `SubagentStop` ya que ese es el evento que se activa cuando un subagente se completa.

Los hooks usan el mismo formato de configuración que los hooks basados en configuración pero se limitan a la vida útil del componente y se limpian cuando finaliza.

Esta skill define un hook `PreToolUse` que ejecuta un script de validación de seguridad antes de cada comando `Bash`:

```yaml theme={null}
---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---
```

Los agentes usan el mismo formato en su frontmatter YAML.

### El menú `/hooks`

Escriba `/hooks` en Claude Code para abrir un navegador de solo lectura para sus hooks configurados. El menú muestra cada evento de hook con un recuento de hooks configurados, le permite profundizar en matchers y muestra los detalles completos de cada controlador de hook. Úselo para verificar la configuración, verificar desde qué archivo de configuración proviene un hook o inspeccionar el comando, prompt o URL de un hook.

El menú muestra los cinco tipos de hooks: `command`, `prompt`, `agent`, `http` y `mcp_tool`. Cada hook está etiquetado con un prefijo `[type]` y una fuente que indica dónde se definió:

* `User`: de `~/.claude/settings.json`
* `Project`: de `.claude/settings.json`
* `Local`: de `.claude/settings.local.json`
* `Plugin`: de `hooks/hooks.json` de un plugin
* `Session`: registrado en memoria para la sesión actual
* `Built-in`: registrado internamente por Claude Code

Seleccionar un hook abre una vista de detalle que muestra su evento, matcher, tipo, archivo de origen y el comando, prompt o URL completo. El menú es de solo lectura: para agregar, modificar o eliminar hooks, edite el JSON de configuración directamente o pida a Claude que haga el cambio.

### Deshabilitar o eliminar hooks

Para eliminar un hook, elimine su entrada del archivo de configuración JSON.

Para deshabilitar temporalmente todos los hooks sin eliminarlos, establezca `"disableAllHooks": true` en su archivo de configuración. No hay forma de deshabilitar un hook individual mientras se mantiene en la configuración.

La configuración `disableAllHooks` respeta la jerarquía de configuración administrada. Si un administrador ha configurado hooks a través de configuración de política administrada, `disableAllHooks` establecido en configuración de usuario, proyecto o local no puede deshabilitar esos hooks administrados. Solo `disableAllHooks` establecido en el nivel de configuración administrada puede deshabilitar hooks administrados.

Las ediciones directas de hooks en archivos de configuración normalmente se capturan automáticamente por el observador de archivos.

## Entrada y salida de hooks

Los hooks de comando reciben datos JSON a través de stdin y comunican resultados a través de códigos de salida, stdout y stderr. Los hooks HTTP reciben el mismo JSON que el cuerpo de la solicitud POST y comunican resultados a través del cuerpo de la respuesta HTTP. Esta sección cubre campos y comportamiento comunes a todos los eventos. Cada sección de evento bajo [Hook events](#hook-events) incluye su esquema de entrada específico y opciones de control de decisión.

### Campos de entrada comunes

Los eventos de hook reciben estos campos como JSON, además de campos específicos del evento documentados en cada sección [hook event](#hook-events). Para hooks de comando, este JSON llega a través de stdin. Para hooks HTTP, llega como el cuerpo de la solicitud POST.

| Campo             | Descripción                                                                                                                                                                                                                                                    |
| :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `session_id`      | Identificador de sesión actual                                                                                                                                                                                                                                 |
| `transcript_path` | Ruta al JSON de conversación                                                                                                                                                                                                                                   |
| `cwd`             | Directorio de trabajo actual cuando se invoca el hook                                                                                                                                                                                                          |
| `permission_mode` | [Modo de permiso](/es/permissions#permission-modes) actual: `"default"`, `"plan"`, `"acceptEdits"`, `"auto"`, `"dontAsk"` o `"bypassPermissions"`. No todos los eventos reciben este campo: consulte cada ejemplo JSON de evento a continuación para verificar |
| `hook_event_name` | Nombre del evento que se activó                                                                                                                                                                                                                                |

Cuando se ejecuta con `--agent` o dentro de un subagente, se incluyen dos campos adicionales:

| Campo        | Descripción                                                                                                                                                                                                                                               |
| :----------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agent_id`   | Identificador único para el subagente. Presente solo cuando el hook se activa dentro de una llamada de subagente. Use esto para distinguir llamadas de hook de subagente de llamadas de hilo principal.                                                   |
| `agent_type` | Nombre del agente (por ejemplo, `"Explore"` o `"security-reviewer"`). Presente cuando la sesión usa `--agent` o el hook se activa dentro de un subagente. Para subagentes, el tipo del subagente tiene precedencia sobre el valor `--agent` de la sesión. |

Por ejemplo, un hook `PreToolUse` para un comando Bash recibe esto en stdin:

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl",
  "cwd": "/home/user/my-project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}
```

Los campos `tool_name` y `tool_input` son específicos del evento. Cada sección [hook event](#hook-events) documenta los campos adicionales para ese evento.

### Salida de código de salida

El código de salida de su comando de hook le dice a Claude Code si la acción debe proceder, ser bloqueada o ser ignorada.

**Exit 0** significa éxito. Claude Code analiza stdout para [campos de salida JSON](#json-output). La salida JSON solo se procesa en exit 0. Para la mayoría de eventos, stdout se escribe en el registro de depuración pero no se muestra en la transcripción. Las excepciones son `UserPromptSubmit`, `UserPromptExpansion` y `SessionStart`, donde stdout se agrega como contexto que Claude puede ver y actuar.

**Exit 2** significa un error de bloqueo. Claude Code ignora stdout y cualquier JSON en él. En su lugar, el texto de stderr se devuelve a Claude como un mensaje de error. El efecto depende del evento: `PreToolUse` bloquea la llamada a herramienta, `UserPromptSubmit` rechaza el prompt, y así sucesivamente. Consulte [exit code 2 behavior](#exit-code-2-behavior-per-event) para la lista completa.

**Cualquier otro código de salida** es un error sin bloqueo para la mayoría de eventos de hook. La transcripción muestra un aviso `<hook name> hook error` seguido de la primera línea de stderr, para que pueda identificar la causa sin `--debug`. La ejecución continúa y el stderr completo se escribe en el registro de depuración.

Por ejemplo, un script de comando de hook que bloquea comandos Bash peligrosos:

```bash theme={null}
#!/bin/bash
# Lee entrada JSON desde stdin, verifica el comando
command=$(jq -r '.tool_input.command' < /dev/stdin)

if [[ "$command" == rm* ]]; then
  echo "Blocked: rm commands are not allowed" >&2
  exit 2  # Blocking error: tool call is prevented
fi

exit 0  # Success: tool call proceeds
```

<Warning>
  Para la mayoría de eventos de hook, solo el código de salida 2 bloquea la acción. Claude Code trata el código de salida 1 como un error sin bloqueo y procede con la acción, aunque 1 es el código de fallo convencional de Unix. Si su hook está destinado a aplicar una política, use `exit 2`. La excepción es `WorktreeCreate`, donde cualquier código de salida distinto de cero aborta la creación de worktree.
</Warning>

#### Comportamiento del código de salida 2 por evento

El código de salida 2 es la forma en que un hook señala "detente, no hagas esto". El efecto depende del evento, porque algunos eventos representan acciones que pueden bloquearse (como una llamada a herramienta que aún no ha sucedido) y otros representan cosas que ya sucedieron o no pueden prevenirse.

| Evento de hook        | ¿Puede bloquear? | Qué sucede en exit 2                                                                                                                                      |
| :-------------------- | :--------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PreToolUse`          | Sí               | Bloquea la llamada a herramienta                                                                                                                          |
| `PermissionRequest`   | Sí               | Deniega el permiso                                                                                                                                        |
| `UserPromptSubmit`    | Sí               | Bloquea el procesamiento del prompt y borra el prompt                                                                                                     |
| `UserPromptExpansion` | Sí               | Bloquea la expansión                                                                                                                                      |
| `Stop`                | Sí               | Evita que Claude se detenga, continúa la conversación                                                                                                     |
| `SubagentStop`        | Sí               | Evita que el subagente se detenga                                                                                                                         |
| `TeammateIdle`        | Sí               | Evita que el compañero se quede inactivo (el compañero continúa trabajando)                                                                               |
| `TaskCreated`         | Sí               | Revierte la creación de la tarea                                                                                                                          |
| `TaskCompleted`       | Sí               | Evita que la tarea se marque como completada                                                                                                              |
| `ConfigChange`        | Sí               | Bloquea que el cambio de configuración tenga efecto (excepto `policy_settings`)                                                                           |
| `StopFailure`         | No               | La salida y el código de salida se ignoran                                                                                                                |
| `PostToolUse`         | No               | Muestra stderr a Claude (la herramienta ya se ejecutó)                                                                                                    |
| `PostToolUseFailure`  | No               | Muestra stderr a Claude (la herramienta ya falló)                                                                                                         |
| `PostToolBatch`       | Sí               | Detiene el bucle agentico antes de la siguiente llamada al modelo                                                                                         |
| `PermissionDenied`    | No               | El código de salida y stderr se ignoran (la denegación ya ocurrió). Use JSON `hookSpecificOutput.retry: true` para decirle al modelo que puede reintentar |
| `Notification`        | No               | Muestra stderr solo al usuario                                                                                                                            |
| `SubagentStart`       | No               | Muestra stderr solo al usuario                                                                                                                            |
| `SessionStart`        | No               | Muestra stderr solo al usuario                                                                                                                            |
| `Setup`               | No               | Muestra stderr solo al usuario                                                                                                                            |
| `SessionEnd`          | No               | Muestra stderr solo al usuario                                                                                                                            |
| `CwdChanged`          | No               | Muestra stderr solo al usuario                                                                                                                            |
| `FileChanged`         | No               | Muestra stderr solo al usuario                                                                                                                            |
| `PreCompact`          | Sí               | Bloquea la compactación                                                                                                                                   |
| `PostCompact`         | No               | Muestra stderr solo al usuario                                                                                                                            |
| `Elicitation`         | Sí               | Deniega la elicitación                                                                                                                                    |
| `ElicitationResult`   | Sí               | Bloquea la respuesta (la acción se convierte en decline)                                                                                                  |
| `WorktreeCreate`      | Sí               | Cualquier código de salida distinto de cero causa que la creación de worktree falle                                                                       |
| `WorktreeRemove`      | No               | Los fallos se registran solo en modo de depuración                                                                                                        |
| `InstructionsLoaded`  | No               | El código de salida se ignora                                                                                                                             |

### Manejo de respuesta HTTP

Los hooks HTTP usan códigos de estado HTTP y cuerpos de respuesta en lugar de códigos de salida y stdout:

* **2xx con un cuerpo vacío**: éxito, equivalente a código de salida 0 sin salida
* **2xx con un cuerpo de texto plano**: éxito, el texto se agrega como contexto
* **2xx con un cuerpo JSON**: éxito, analizado usando el mismo esquema [JSON output](#json-output) que los hooks de comando
* **Estado que no es 2xx**: error sin bloqueo, la ejecución continúa
* **Fallo de conexión o tiempo de espera agotado**: error sin bloqueo, la ejecución continúa

A diferencia de los hooks de comando, los hooks HTTP no pueden señalar un error de bloqueo solo a través de códigos de estado. Para bloquear una llamada a herramienta o denegar un permiso, devuelva una respuesta 2xx con un cuerpo JSON que contenga los campos de decisión apropiados.

### Salida JSON

Los códigos de salida le permiten permitir o bloquear, pero la salida JSON le da un control más granular. En lugar de salir con código 2 para bloquear, salga 0 e imprima un objeto JSON en stdout. Claude Code lee campos específicos de ese JSON para controlar el comportamiento, incluyendo [decision control](#decision-control) para bloquear, permitir o escalar al usuario.

<Note>
  Debe elegir un enfoque por hook, no ambos: use códigos de salida solos para señalizar, o salga 0 e imprima JSON para control estructurado. Claude Code solo procesa JSON en exit 0. Si sale 2, cualquier JSON se ignora.
</Note>

El stdout de su hook debe contener solo el objeto JSON. Si su perfil de shell imprime texto al inicio, puede interferir con el análisis JSON. Consulte [JSON validation failed](/es/hooks-guide#json-validation-failed) en la guía de solución de problemas.

La salida de hook inyectada en contexto (`additionalContext`, `systemMessage` o stdout plano) está limitada a 10.000 caracteres. La salida que excede este límite se guarda en un archivo y se reemplaza con una vista previa y ruta de archivo, de la misma manera que se manejan los resultados de herramientas grandes.

El objeto JSON admite tres tipos de campos:

* **Campos universales** como `continue` funcionan en todos los eventos. Estos se enumeran en la tabla a continuación.
* **`decision` y `reason` de nivel superior** son utilizados por algunos eventos para bloquear o proporcionar retroalimentación.
* **`hookSpecificOutput`** es un objeto anidado para eventos que necesitan control más rico. Requiere un campo `hookEventName` establecido en el nombre del evento.

| Campo            | Predeterminado | Descripción                                                                                                                                                               |
| :--------------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `continue`       | `true`         | Si es `false`, Claude detiene el procesamiento completamente después de que se ejecuta el hook. Tiene precedencia sobre cualquier campo de decisión específico del evento |
| `stopReason`     | ninguno        | Mensaje mostrado al usuario cuando `continue` es `false`. No se muestra a Claude                                                                                          |
| `suppressOutput` | `false`        | Si es `true`, omite stdout del registro de depuración                                                                                                                     |
| `systemMessage`  | ninguno        | Mensaje de advertencia mostrado al usuario                                                                                                                                |

Para detener Claude completamente independientemente del tipo de evento:

```json theme={null}
{ "continue": false, "stopReason": "Build failed, fix errors before continuing" }
```

#### Agregar contexto para Claude

El campo `additionalContext` pasa una cadena de su hook a la ventana de contexto de Claude. Claude Code envuelve la cadena en un recordatorio del sistema e la inserta en la conversación en el punto donde se activó el hook. Claude lee el recordatorio en la siguiente solicitud del modelo, pero no aparece como un mensaje de chat en la interfaz.

Devuelva `additionalContext` dentro de `hookSpecificOutput` junto al nombre del evento:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "This file is generated. Edit src/schema.ts and run `bun generate` instead."
  }
}
```

Dónde aparece el recordatorio depende del evento:

* [SessionStart](#sessionstart), [Setup](#setup) y [SubagentStart](#subagentstart): al inicio de la conversación, antes del primer prompt
* [UserPromptSubmit](#userpromptsubmit) y [UserPromptExpansion](#userpromptexpansion): junto al prompt enviado
* [PreToolUse](#pretooluse), [PostToolUse](#posttooluse), [PostToolUseFailure](#posttoolusefailure) y [PostToolBatch](#posttoolbatch): junto al resultado de la herramienta

Cuando varios hooks devuelven `additionalContext` para el mismo evento, Claude recibe todos los valores. Si un valor excede 10.000 caracteres, Claude Code escribe el texto completo en un archivo en el directorio de sesión y pasa a Claude la ruta del archivo con una vista previa corta en su lugar.

Use `additionalContext` para información que Claude debe conocer sobre el estado actual de su entorno o la operación que acaba de ejecutarse:

* **Estado del entorno**: la rama actual, destino de implementación o banderas de características activas
* **Reglas de proyecto condicionales**: qué comando de prueba se aplica al archivo que acaba de editar, qué directorios son de solo lectura en este worktree
* **Datos externos**: problemas abiertos asignados a usted, resultados recientes de CI, contenido obtenido de un servicio interno

Para instrucciones que nunca cambian, prefiera [CLAUDE.md](/es/memory). Se carga sin ejecutar un script y es el lugar estándar para convenciones de proyecto estáticas.

Escriba el texto como declaraciones factuales en lugar de instrucciones de sistema imperativas. Frases como "El destino de implementación es producción" o "Este repositorio usa `bun test`" se leen como información del proyecto. El texto enmarcado como comandos de sistema fuera de banda puede activar las defensas de inyección de prompts de Claude, lo que hace que Claude le muestre el texto en lugar de tratarlo como contexto.

Una vez inyectado, el texto se guarda en la transcripción de sesión. Para eventos a mitad de sesión como `PostToolUse` o `UserPromptSubmit`, reanudar con `--continue` o `--resume` reproduce el texto guardado en lugar de volver a ejecutar el hook para turnos anteriores, por lo que valores como marcas de tiempo o SHAs de commit se vuelven obsoletos al reanudar. Los hooks `SessionStart` se ejecutan nuevamente al reanudar con `source` establecido en `"resume"`, por lo que pueden actualizar su contexto.

#### Control de decisión

No todos los eventos admiten bloqueo o control de comportamiento a través de JSON. Los eventos que lo hacen cada uno usan un conjunto diferente de campos para expresar esa decisión. Use esta tabla como referencia rápida antes de escribir un hook:

| Eventos                                                                                                                             | Patrón de decisión                   | Campos clave                                                                                                                                                                                                            |
| :---------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| UserPromptSubmit, UserPromptExpansion, PostToolUse, PostToolUseFailure, PostToolBatch, Stop, SubagentStop, ConfigChange, PreCompact | `decision` de nivel superior         | `decision: "block"`, `reason`                                                                                                                                                                                           |
| TeammateIdle, TaskCreated, TaskCompleted                                                                                            | Código de salida o `continue: false` | El código de salida 2 bloquea la acción con retroalimentación de stderr. JSON `{"continue": false, "stopReason": "..."}` también detiene al compañero completamente, coincidiendo con el comportamiento del hook `Stop` |
| PreToolUse                                                                                                                          | `hookSpecificOutput`                 | `permissionDecision` (allow/deny/ask/defer), `permissionDecisionReason`                                                                                                                                                 |
| PermissionRequest                                                                                                                   | `hookSpecificOutput`                 | `decision.behavior` (allow/deny)                                                                                                                                                                                        |
| PermissionDenied                                                                                                                    | `hookSpecificOutput`                 | `retry: true` le dice al modelo que puede reintentar la llamada a herramienta denegada                                                                                                                                  |
| WorktreeCreate                                                                                                                      | ruta return                          | El hook de comando imprime la ruta en stdout; el hook HTTP devuelve `hookSpecificOutput.worktreePath`. El fallo del hook o la ruta faltante falla la creación                                                           |
| Elicitation                                                                                                                         | `hookSpecificOutput`                 | `action` (accept/decline/cancel), `content` (valores de campo de formulario para accept)                                                                                                                                |
| ElicitationResult                                                                                                                   | `hookSpecificOutput`                 | `action` (accept/decline/cancel), `content` (valores de campo de formulario override)                                                                                                                                   |
| WorktreeRemove, Notification, SessionEnd, PostCompact, InstructionsLoaded, StopFailure, CwdChanged, FileChanged                     | Ninguno                              | Sin control de decisión. Se usa para efectos secundarios como registro o limpieza                                                                                                                                       |

Aquí hay ejemplos de cada patrón en acción:

<Tabs>
  <Tab title="Decisión de nivel superior">
    Utilizado por `UserPromptSubmit`, `UserPromptExpansion`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `Stop`, `SubagentStop`, `ConfigChange` y `PreCompact`. El único valor es `"block"`. Para permitir que la acción continúe, omita `decision` de su JSON, o salga 0 sin ningún JSON en absoluto:

    ```json theme={null}
    {
      "decision": "block",
      "reason": "Test suite must pass before proceeding"
    }
    ```
  </Tab>

  <Tab title="PreToolUse">
    Usa `hookSpecificOutput` para control más rico: permitir, denegar, o escalar al usuario. También puede modificar la entrada de la herramienta antes de que se ejecute o inyectar contexto adicional para Claude. Consulte [PreToolUse decision control](#pretooluse-decision-control) para el conjunto completo de opciones.

    ```json theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Database writes are not allowed"
      }
    }
    ```
  </Tab>

  <Tab title="PermissionRequest">
    Usa `hookSpecificOutput` para permitir o denegar una solicitud de permiso en nombre del usuario. Al permitir, también puede modificar la entrada de la herramienta o aplicar reglas de permiso para que el usuario no sea solicitado nuevamente. Consulte [PermissionRequest decision control](#permissionrequest-decision-control) para el conjunto completo de opciones.

    ```json theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PermissionRequest",
        "decision": {
          "behavior": "allow",
          "updatedInput": {
            "command": "npm run lint"
          }
        }
      }
    }
    ```
  </Tab>
</Tabs>

Para ejemplos extendidos incluyendo validación de comandos Bash, filtrado de prompts y scripts de aprobación automática, consulte [What you can automate](/es/hooks-guide#what-you-can-automate) en la guía y la [implementación de referencia del validador de comandos Bash](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py).

## Eventos de hook

Cada evento corresponde a un punto en el ciclo de vida de Claude Code donde los hooks pueden ejecutarse. Las secciones a continuación se ordenan para coincidir con el ciclo de vida: desde la configuración de sesión a través del bucle agentico hasta el final de la sesión. Cada sección describe cuándo se activa el evento, qué matchers admite, la entrada JSON que recibe y cómo controlar el comportamiento a través de la salida.

### SessionStart

Se ejecuta cuando Claude Code inicia una nueva sesión o reanuda una sesión existente. Útil para cargar contexto de desarrollo como problemas existentes o cambios recientes en su base de código, o configurar variables de entorno. Para contexto estático que no requiere un script, use [CLAUDE.md](/es/memory) en su lugar.

SessionStart se ejecuta en cada sesión, así que mantenga estos hooks rápidos. Solo se admiten hooks `type: "command"` y `type: "mcp_tool"`.

El valor del matcher corresponde a cómo se inició la sesión:

| Matcher   | Cuándo se activa                     |
| :-------- | :----------------------------------- |
| `startup` | Nueva sesión                         |
| `resume`  | `--resume`, `--continue` o `/resume` |
| `clear`   | `/clear`                             |
| `compact` | Compactación automática o manual     |

#### Entrada de SessionStart

Además de los [campos de entrada comunes](#common-input-fields), los hooks SessionStart reciben `source`, `model` y opcionalmente `agent_type`. El campo `source` indica cómo comenzó la sesión: `"startup"` para nuevas sesiones, `"resume"` para sesiones reanudadas, `"clear"` después de `/clear` o `"compact"` después de compactación. El campo `model` contiene el identificador del modelo. Si inicia Claude Code con `claude --agent <name>`, un campo `agent_type` contiene el nombre del agente.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionStart",
  "source": "startup",
  "model": "claude-sonnet-4-6"
}
```

#### Control de decisión de SessionStart

Cualquier texto que su script de hook imprima en stdout se agrega como contexto para Claude. Además de los [campos de salida JSON](#json-output) disponibles para todos los hooks, puede devolver estos campos específicos del evento:

| Campo               | Descripción                                                                                                                                                                                                         |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `additionalContext` | Cadena agregada al contexto de Claude al inicio de la conversación, antes del primer prompt. Consulte [Agregar contexto para Claude](#add-context-for-claude) para saber cómo se entrega el texto y qué poner en él |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Current branch: feat/auth-refactor\nUncommitted changes: src/auth.ts, src/login.tsx\nActive issue: #4211 Migrate to OAuth2"
  }
}
```

Dado que el stdout plano ya llega a Claude para este evento, un hook que solo carga contexto puede imprimir en stdout directamente sin construir JSON. Use el formulario JSON cuando necesite combinar contexto con otros campos como `suppressOutput`.

#### Persistir variables de entorno

Los hooks SessionStart tienen acceso a la variable de entorno `CLAUDE_ENV_FILE`, que proporciona una ruta de archivo donde puede persistir variables de entorno para comandos Bash posteriores.

Para establecer variables de entorno individuales, escriba declaraciones `export` en `CLAUDE_ENV_FILE`. Use append (`>>`) para preservar variables establecidas por otros hooks:

```bash theme={null}
#!/bin/bash

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG_LOG=true' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

Para capturar todos los cambios de entorno de comandos de configuración, compare las variables exportadas antes y después:

```bash theme={null}
#!/bin/bash

ENV_BEFORE=$(export -p | sort)

# Ejecute sus comandos de configuración que modifican el entorno
source ~/.nvm/nvm.sh
nvm use 20

if [ -n "$CLAUDE_ENV_FILE" ]; then
  ENV_AFTER=$(export -p | sort)
  comm -13 <(echo "$ENV_BEFORE") <(echo "$ENV_AFTER") >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

Cualquier variable escrita en este archivo estará disponible en todos los comandos Bash posteriores que Claude Code ejecute durante la sesión.

<Note>
  `CLAUDE_ENV_FILE` está disponible para hooks SessionStart, [Setup](#setup), [CwdChanged](#cwdchanged) y [FileChanged](#filechanged). Otros tipos de hooks no tienen acceso a esta variable.
</Note>

### Setup

Se activa solo cuando inicia Claude Code con `--init-only`, o con `--init` o `--maintenance` en modo de impresión (`-p`). No se activa en el inicio normal. Úselo para instalación de dependencias única o limpieza programada que desencadena explícitamente desde CI o scripts, separado del inicio de sesión normal. Para inicialización por sesión, use [SessionStart](#sessionstart) en su lugar.

El valor del matcher corresponde a la bandera CLI que desencadenó el hook:

| Matcher       | Cuándo se activa                          |
| :------------ | :---------------------------------------- |
| `init`        | `claude --init-only` o `claude -p --init` |
| `maintenance` | `claude -p --maintenance`                 |

`--init-only` ejecuta hooks Setup y hooks SessionStart con el matcher `startup`, luego sale sin iniciar una conversación. `--init` y `--maintenance` activan hooks Setup solo cuando se combinan con `-p` (modo de impresión); en una sesión interactiva esas dos banderas actualmente no activan hooks Setup.

Debido a que Setup no se activa en cada lanzamiento, un plugin que necesita una dependencia instalada no puede confiar solo en Setup. El patrón práctico es verificar la dependencia en el primer uso e instalar si falta, por ejemplo un hook o skill que pruebe `${CLAUDE_PLUGIN_DATA}/node_modules` y ejecute `npm install` si está ausente. Consulte el [directorio de datos persistentes](/es/plugins-reference#persistent-data-directory) para saber dónde almacenar dependencias instaladas.

#### Entrada de Setup

Además de los [campos de entrada comunes](#common-input-fields), los hooks Setup reciben un campo `trigger` establecido en `"init"` o `"maintenance"`:

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Setup",
  "trigger": "init"
}
```

#### Control de decisión de Setup

Los hooks Setup no pueden bloquear. En código de salida 2, stderr se muestra al usuario; en cualquier otro código de salida distinto de cero, stderr aparece solo cuando inicia con `--verbose`. En ambos casos la ejecución continúa. Para pasar información al contexto de Claude, devuelva `additionalContext` en salida JSON; el stdout plano se escribe solo en el registro de depuración. Además de los [campos de salida JSON](#json-output) disponibles para todos los hooks, puede devolver estos campos específicos del evento:

| Campo               | Descripción                                                                         |
| :------------------ | :---------------------------------------------------------------------------------- |
| `additionalContext` | Cadena agregada al contexto de Claude. Los valores de múltiples hooks se concatenan |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "Setup",
    "additionalContext": "Dependencies installed: node_modules, .venv"
  }
}
```

Los hooks Setup tienen acceso a `CLAUDE_ENV_FILE`. Las variables escritas en ese archivo persisten en comandos Bash posteriores para la sesión, al igual que en los [hooks SessionStart](#persist-environment-variables). Solo se admiten hooks `type: "command"` y `type: "mcp_tool"`.

### InstructionsLoaded

Se activa cuando se carga un archivo `CLAUDE.md` o `.claude/rules/*.md` en contexto. Este evento se activa al inicio de la sesión para archivos cargados con entusiasmo y nuevamente más tarde cuando se cargan archivos de forma perezosa, por ejemplo cuando Claude accede a un subdirectorio que contiene un `CLAUDE.md` anidado o cuando reglas condicionales con frontmatter `paths:` coinciden. El hook no admite bloqueo o control de decisión. Se ejecuta de forma asincrónica con fines de observabilidad.

El matcher se ejecuta contra `load_reason`. Por ejemplo, use `"matcher": "session_start"` para activarse solo para archivos cargados al inicio de la sesión, o `"matcher": "path_glob_match|nested_traversal"` para activarse solo para cargas perezosas.

#### Entrada de InstructionsLoaded

Además de los [campos de entrada comunes](#common-input-fields), los hooks InstructionsLoaded reciben estos campos:

| Campo               | Descripción                                                                                                                                                                                                                                |
| :------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `file_path`         | Ruta absoluta al archivo de instrucciones que se cargó                                                                                                                                                                                     |
| `memory_type`       | Alcance del archivo: `"User"`, `"Project"`, `"Local"` o `"Managed"`                                                                                                                                                                        |
| `load_reason`       | Por qué se cargó el archivo: `"session_start"`, `"nested_traversal"`, `"path_glob_match"`, `"include"` o `"compact"`. El valor `"compact"` se activa cuando los archivos de instrucciones se recargan después de un evento de compactación |
| `globs`             | Patrones de glob de ruta del frontmatter `paths:` del archivo, si los hay. Presente solo para cargas `path_glob_match`                                                                                                                     |
| `trigger_file_path` | Ruta al archivo cuyo acceso desencadenó esta carga, para cargas perezosas                                                                                                                                                                  |
| `parent_file_path`  | Ruta al archivo de instrucciones padre que incluyó este, para cargas `include`                                                                                                                                                             |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "InstructionsLoaded",
  "file_path": "/Users/my-project/CLAUDE.md",
  "memory_type": "Project",
  "load_reason": "session_start"
}
```

#### Control de decisión de InstructionsLoaded

Los hooks InstructionsLoaded no tienen control de decisión. No pueden bloquear o modificar la carga de instrucciones. Use este evento para registro de auditoría, seguimiento de cumplimiento u observabilidad.

### UserPromptSubmit

Se ejecuta cuando el usuario envía un prompt, antes de que Claude lo procese. Esto le permite agregar contexto adicional basado en el prompt/conversación, validar prompts o bloquear ciertos tipos de prompts.

#### Entrada de UserPromptSubmit

Además de los [campos de entrada comunes](#common-input-fields), los hooks UserPromptSubmit reciben el campo `prompt` que contiene el texto que el usuario envió.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial of a number"
}
```

#### Control de decisión de UserPromptSubmit

Los hooks `UserPromptSubmit` pueden controlar si se procesa un prompt de usuario y agregar contexto. Todos los [campos de salida JSON](#json-output) están disponibles.

Hay dos formas de agregar contexto a la conversación en código de salida 0:

* **Stdout de texto plano**: cualquier texto que no sea JSON escrito en stdout se agrega como contexto
* **JSON con `additionalContext`**: use el formato JSON a continuación para más control. El campo `additionalContext` se agrega como contexto

El stdout plano se muestra como salida de hook en la transcripción. El campo `additionalContext` se agrega de forma más discreta.

Para bloquear un prompt, devuelva un objeto JSON con `decision` establecido en `"block"`:

| Campo               | Descripción                                                                                                                                     |
| :------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| `decision`          | `"block"` evita que el prompt se procese y lo borra del contexto. Omita para permitir que el prompt continúe                                    |
| `reason`            | Se muestra al usuario cuando `decision` es `"block"`. No se agrega al contexto                                                                  |
| `additionalContext` | Cadena agregada al contexto de Claude junto con el prompt enviado. Consulte [Agregar contexto para Claude](#add-context-for-claude)             |
| `sessionTitle`      | Establece el título de la sesión, el mismo efecto que `/rename`. Use para nombrar sesiones automáticamente basándose en el contenido del prompt |

```json theme={null}
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here",
    "sessionTitle": "My session title"
  }
}
```

<Note>
  El formato JSON no es necesario para casos de uso simples. Para agregar contexto, puede imprimir texto plano en stdout con código de salida 0. Use JSON cuando necesite bloquear prompts o desee un control más estructurado.
</Note>

### UserPromptExpansion

Se ejecuta cuando un comando de barra diagonal escrito por el usuario se expande en un prompt antes de llegar a Claude. Use esto para bloquear comandos específicos de invocación directa, inyectar contexto para una skill particular o registrar qué comandos invocan los usuarios. Por ejemplo, un hook que coincida con `deploy` puede bloquear `/deploy` a menos que esté presente un archivo de aprobación, o un hook que coincida con una skill de revisión puede agregar la lista de verificación de revisión del equipo como `additionalContext`.

Este evento cubre la ruta que `PreToolUse` no cubre: un hook `PreToolUse` que coincida con la herramienta `Skill` se activa solo cuando Claude llama a la herramienta, pero escribir `/skillname` directamente omite `PreToolUse`. `UserPromptExpansion` se activa en esa ruta directa.

Coincide en `command_name`. Deje el matcher vacío para activarse en cada comando de barra diagonal de tipo prompt.

#### Entrada de UserPromptExpansion

Además de los [campos de entrada comunes](#common-input-fields), los hooks UserPromptExpansion reciben `expansion_type`, `command_name`, `command_args`, `command_source` y la cadena `prompt` original. El campo `expansion_type` es `slash_command` para skills y comandos personalizados, o `mcp_prompt` para prompts de servidor MCP.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../00893aaf.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptExpansion",
  "expansion_type": "slash_command",
  "command_name": "example-skill",
  "command_args": "arg1 arg2",
  "command_source": "plugin",
  "prompt": "/example-skill arg1 arg2"
}
```

#### Control de decisión de UserPromptExpansion

Los hooks `UserPromptExpansion` pueden bloquear la expansión o agregar contexto. Todos los [campos de salida JSON](#json-output) están disponibles.

| Campo               | Descripción                                                                                                                           |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------ |
| `decision`          | `"block"` evita que el comando de barra diagonal se expanda. Omita para permitir que continúe                                         |
| `reason`            | Se muestra al usuario cuando `decision` es `"block"`                                                                                  |
| `additionalContext` | Cadena agregada al contexto de Claude junto con el prompt expandido. Consulte [Agregar contexto para Claude](#add-context-for-claude) |

```json theme={null}
{
  "decision": "block",
  "reason": "This slash command is not available",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptExpansion",
    "additionalContext": "Additional context for this expansion"
  }
}
```

### PreToolUse

Se ejecuta después de que Claude crea parámetros de herramienta y antes de procesar la llamada a herramienta. Coincide en el nombre de la herramienta: `Bash`, `Edit`, `Write`, `Read`, `Glob`, `Grep`, `Agent`, `WebFetch`, `WebSearch`, `AskUserQuestion`, `ExitPlanMode` y cualquier [nombre de herramienta MCP](#match-mcp-tools).

Use [PreToolUse decision control](#pretooluse-decision-control) para permitir, denegar, preguntar o diferir la llamada a herramienta.

#### Entrada de PreToolUse

Además de los [campos de entrada comunes](#common-input-fields), los hooks PreToolUse reciben `tool_name`, `tool_input` y `tool_use_id`. Los campos `tool_input` dependen de la herramienta:

##### Bash

Ejecuta comandos de shell.

| Campo               | Tipo    | Ejemplo            | Descripción                                    |
| :------------------ | :------ | :----------------- | :--------------------------------------------- |
| `command`           | string  | `"npm test"`       | El comando de shell a ejecutar                 |
| `description`       | string  | `"Run test suite"` | Descripción opcional de lo que hace el comando |
| `timeout`           | number  | `120000`           | Tiempo de espera opcional en milisegundos      |
| `run_in_background` | boolean | `false`            | Si se ejecuta el comando en segundo plano      |

##### Write

Crea o sobrescribe un archivo.

| Campo       | Tipo   | Ejemplo               | Descripción                         |
| :---------- | :----- | :-------------------- | :---------------------------------- |
| `file_path` | string | `"/path/to/file.txt"` | Ruta absoluta al archivo a escribir |
| `content`   | string | `"file content"`      | Contenido a escribir en el archivo  |

##### Edit

Reemplaza una cadena en un archivo existente.

| Campo         | Tipo    | Ejemplo               | Descripción                            |
| :------------ | :------ | :-------------------- | :------------------------------------- |
| `file_path`   | string  | `"/path/to/file.txt"` | Ruta absoluta al archivo a editar      |
| `old_string`  | string  | `"original text"`     | Texto a encontrar y reemplazar         |
| `new_string`  | string  | `"replacement text"`  | Texto de reemplazo                     |
| `replace_all` | boolean | `false`               | Si se reemplazan todas las ocurrencias |

##### Read

Lee contenidos de archivo.

| Campo       | Tipo   | Ejemplo               | Descripción                                         |
| :---------- | :----- | :-------------------- | :-------------------------------------------------- |
| `file_path` | string | `"/path/to/file.txt"` | Ruta absoluta al archivo a leer                     |
| `offset`    | number | `10`                  | Número de línea opcional para comenzar a leer desde |
| `limit`     | number | `50`                  | Número opcional de líneas a leer                    |

##### Glob

Encuentra archivos que coincidan con un patrón glob.

| Campo     | Tipo   | Ejemplo          | Descripción                                                                     |
| :-------- | :----- | :--------------- | :------------------------------------------------------------------------------ |
| `pattern` | string | `"**/*.ts"`      | Patrón glob para coincidir archivos contra                                      |
| `path`    | string | `"/path/to/dir"` | Directorio opcional para buscar. Por defecto es el directorio de trabajo actual |

##### Grep

Busca contenidos de archivo con expresiones regulares.

| Campo         | Tipo    | Ejemplo          | Descripción                                                                            |
| :------------ | :------ | :--------------- | :------------------------------------------------------------------------------------- |
| `pattern`     | string  | `"TODO.*fix"`    | Patrón de expresión regular a buscar                                                   |
| `path`        | string  | `"/path/to/dir"` | Archivo o directorio opcional para buscar                                              |
| `glob`        | string  | `"*.ts"`         | Patrón glob opcional para filtrar archivos                                             |
| `output_mode` | string  | `"content"`      | `"content"`, `"files_with_matches"` o `"count"`. Por defecto es `"files_with_matches"` |
| `-i`          | boolean | `true`           | Búsqueda insensible a mayúsculas y minúsculas                                          |
| `multiline`   | boolean | `false`          | Habilitar coincidencia multilínea                                                      |

##### WebFetch

Obtiene y procesa contenido web.

| Campo    | Tipo   | Ejemplo                       | Descripción                                |
| :------- | :----- | :---------------------------- | :----------------------------------------- |
| `url`    | string | `"https://example.com/api"`   | URL para obtener contenido de              |
| `prompt` | string | `"Extract the API endpoints"` | Prompt a ejecutar en el contenido obtenido |

##### WebSearch

Busca en la web.

| Campo             | Tipo   | Ejemplo                        | Descripción                                         |
| :---------------- | :----- | :----------------------------- | :-------------------------------------------------- |
| `query`           | string | `"react hooks best practices"` | Consulta de búsqueda                                |
| `allowed_domains` | array  | `["docs.example.com"]`         | Opcional: incluir solo resultados de estos dominios |
| `blocked_domains` | array  | `["spam.example.com"]`         | Opcional: excluir resultados de estos dominios      |

##### Agent

Genera un [subagente](/es/sub-agents).

| Campo           | Tipo   | Ejemplo                    | Descripción                                            |
| :-------------- | :----- | :------------------------- | :----------------------------------------------------- |
| `prompt`        | string | `"Find all API endpoints"` | La tarea para que el agente realice                    |
| `description`   | string | `"Find API endpoints"`     | Descripción breve de la tarea                          |
| `subagent_type` | string | `"Explore"`                | Tipo de agente especializado a usar                    |
| `model`         | string | `"sonnet"`                 | Alias de modelo opcional para anular el predeterminado |

##### AskUserQuestion

Hace al usuario una a cuatro preguntas de opción múltiple.

| Campo       | Tipo   | Ejemplo                                                                                                            | Descripción                                                                                                                                                                                                                                       |
| :---------- | :----- | :----------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `questions` | array  | `[{"question": "Which framework?", "header": "Framework", "options": [{"label": "React"}], "multiSelect": false}]` | Preguntas a presentar, cada una con una cadena `question`, `header` corto, array `options` y bandera `multiSelect` opcional                                                                                                                       |
| `answers`   | object | `{"Which framework?": "React"}`                                                                                    | Opcional. Asigna texto de pregunta a la etiqueta de opción seleccionada. Las respuestas de selección múltiple unen etiquetas con comas. Claude no establece este campo; suministrarlo a través de `updatedInput` para responder programáticamente |

#### Control de decisión de PreToolUse

Los hooks `PreToolUse` pueden controlar si procede una llamada a herramienta. A diferencia de otros hooks que usan un campo `decision` de nivel superior, PreToolUse devuelve su decisión dentro de un objeto `hookSpecificOutput`. Esto le da control más rico: cuatro resultados (permitir, denegar, preguntar o diferir) más la capacidad de modificar la entrada de la herramienta antes de la ejecución.

| Campo                      | Descripción                                                                                                                                                                                                                                                                                                                            |
| :------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `permissionDecision`       | `"allow"` omite el sistema de permisos. `"deny"` evita la llamada a herramienta. `"ask"` solicita al usuario que confirme. `"defer"` sale correctamente para que la herramienta pueda reanudarse más tarde. Las reglas [Deny and ask](/es/permissions#manage-permissions) aún se evalúan independientemente de lo que devuelva el hook |
| `permissionDecisionReason` | Para `"allow"` y `"ask"`, se muestra al usuario pero no a Claude. Para `"deny"`, se muestra a Claude. Para `"defer"`, se ignora                                                                                                                                                                                                        |
| `updatedInput`             | Modifica los parámetros de entrada de la herramienta antes de la ejecución. Reemplaza el objeto de entrada completo, así que incluya campos sin cambios junto con los modificados. Combinar con `"allow"` para aprobación automática, o `"ask"` para mostrar la entrada modificada al usuario. Para `"defer"`, se ignora               |
| `additionalContext`        | Cadena agregada al contexto de Claude junto con el resultado de la herramienta. Para `"defer"`, se ignora. Consulte [Agregar contexto para Claude](#add-context-for-claude)                                                                                                                                                            |

Cuando múltiples hooks PreToolUse devuelven diferentes decisiones, la precedencia es `deny` > `defer` > `ask` > `allow`.

Cuando un hook devuelve `"ask"`, el diálogo de permiso mostrado al usuario incluye una etiqueta que identifica de dónde proviene el hook: por ejemplo, `[User]`, `[Project]`, `[Plugin]` o `[Local]`. Esto ayuda a los usuarios a entender qué fuente de configuración está solicitando confirmación.

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "My reason here",
    "updatedInput": {
      "field_to_modify": "new value"
    },
    "additionalContext": "Current environment: production. Proceed with caution."
  }
}
```

`AskUserQuestion` y `ExitPlanMode` requieren interacción del usuario y normalmente se bloquean en [modo no interactivo](/es/headless) con la bandera `-p`. Devolver `permissionDecision: "allow"` junto con `updatedInput` satisface ese requisito: el hook lee la entrada de la herramienta desde stdin, recopila la respuesta a través de su propia interfaz de usuario y la devuelve en `updatedInput` para que la herramienta se ejecute sin solicitar. Devolver `"allow"` solo no es suficiente para estas herramientas. Para `AskUserQuestion`, repita el array `questions` original y agregue un objeto [`answers`](#askuserquestion) que asigne el texto de cada pregunta a la respuesta elegida.

<Note>
  PreToolUse anteriormente usaba campos `decision` y `reason` de nivel superior, pero estos están deprecados para este evento. Use `hookSpecificOutput.permissionDecision` y `hookSpecificOutput.permissionDecisionReason` en su lugar. Los valores deprecados `"approve"` y `"block"` se asignan a `"allow"` y `"deny"` respectivamente. Otros eventos como PostToolUse y Stop continúan usando `decision` y `reason` de nivel superior como su formato actual.
</Note>

#### Diferir una llamada a herramienta para más tarde

`"defer"` es para integraciones que ejecutan `claude -p` como un subproceso y leen su salida JSON, como una aplicación del Agent SDK o una interfaz de usuario personalizada construida sobre Claude Code. Permite que ese proceso de llamada pause Claude en una llamada a herramienta, recopile entrada a través de su propia interfaz y reanude donde se quedó. Claude Code honra este valor solo en [modo no interactivo](/es/headless) con la bandera `-p`. En sesiones interactivas registra una advertencia e ignora el resultado del hook.

<Note>
  El valor `defer` requiere Claude Code v2.1.89 o posterior. Las versiones anteriores no lo reconocen y la herramienta procede a través del flujo de permiso normal.
</Note>

La herramienta `AskUserQuestion` es el caso típico: Claude quiere hacer algo al usuario, pero no hay terminal para responder. El viaje de ida y vuelta funciona así:

1. Claude llama a `AskUserQuestion`. Se activa el hook `PreToolUse`.
2. El hook devuelve `permissionDecision: "defer"`. La herramienta no se ejecuta. El proceso sale con `stop_reason: "tool_deferred"` y la llamada a herramienta pendiente preservada en la transcripción.
3. El proceso de llamada lee `deferred_tool_use` del resultado del SDK, muestra la pregunta en su propia interfaz de usuario y espera una respuesta.
4. El proceso de llamada ejecuta `claude -p --resume <session-id>`. La misma llamada a herramienta activa `PreToolUse` nuevamente.
5. El hook devuelve `permissionDecision: "allow"` con la respuesta en `updatedInput`. La herramienta se ejecuta y Claude continúa.

El campo `deferred_tool_use` lleva el `id`, `name` e `input` de la herramienta. El `input` son los parámetros que Claude generó para la llamada a herramienta, capturados antes de la ejecución:

```json theme={null}
{
  "type": "result",
  "subtype": "success",
  "stop_reason": "tool_deferred",
  "session_id": "abc123",
  "deferred_tool_use": {
    "id": "toolu_01abc",
    "name": "AskUserQuestion",
    "input": { "questions": [{ "question": "Which framework?", "header": "Framework", "options": [{"label": "React"}, {"label": "Vue"}], "multiSelect": false }] }
  }
}
```

No hay límite de tiempo de espera o reintento. La sesión permanece en el disco hasta que la reanude, sujeta al barrido de retención [`cleanupPeriodDays`](/es/settings#available-settings) que elimina archivos de sesión después de 30 días por defecto. Si la respuesta no está lista cuando reanuda, el hook puede devolver `"defer"` nuevamente y el proceso sale de la misma manera. El proceso de llamada controla cuándo romper el bucle devolviendo finalmente `"allow"` o `"deny"` del hook.

`"defer"` solo funciona cuando Claude hace una única llamada a herramienta en el turno. Si Claude hace varias llamadas a herramientas a la vez, `"defer"` se ignora con una advertencia y la herramienta procede a través del flujo de permiso normal. La restricción existe porque reanudar solo puede re-ejecutar una herramienta: no hay forma de diferir una llamada de un lote sin dejar las otras sin resolver.

Si la herramienta diferida ya no está disponible cuando reanuda, el proceso sale con `stop_reason: "tool_deferred_unavailable"` e `is_error: true` antes de que se active el hook. Esto sucede cuando un servidor MCP que proporcionó la herramienta no está conectado para la sesión reanudada. El payload `deferred_tool_use` aún se incluye para que pueda identificar qué herramienta desapareció.

<Warning>
  `--resume` no restaura el modo de permiso de la sesión anterior. Pase la misma bandera `--permission-mode` en reanudar que estaba activa cuando se diferió la herramienta. Claude Code registra una advertencia si los modos difieren.
</Warning>

### PermissionRequest

Se ejecuta cuando se muestra un diálogo de permiso al usuario.
Use [PermissionRequest decision control](#permissionrequest-decision-control) para permitir o denegar en nombre del usuario.

Coincide en el nombre de la herramienta, los mismos valores que PreToolUse.

#### Entrada de PermissionRequest

Los hooks PermissionRequest reciben campos `tool_name` y `tool_input` como los hooks PreToolUse, pero sin `tool_use_id`. Un array `permission_suggestions` opcional contiene las opciones "siempre permitir" que el usuario normalmente vería en el diálogo de permiso. La diferencia es cuándo se activa el hook: los hooks PermissionRequest se ejecutan cuando un diálogo de permiso está a punto de mostrarse al usuario, mientras que los hooks PreToolUse se ejecutan antes de la ejecución de la herramienta independientemente del estado de permiso.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PermissionRequest",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf node_modules",
    "description": "Remove node_modules directory"
  },
  "permission_suggestions": [
    {
      "type": "addRules",
      "rules": [{ "toolName": "Bash", "ruleContent": "rm -rf node_modules" }],
      "behavior": "allow",
      "destination": "localSettings"
    }
  ]
}
```

#### Control de decisión de PermissionRequest

Los hooks `PermissionRequest` pueden permitir o denegar solicitudes de permiso. Además de los [campos de salida JSON](#json-output) disponibles para todos los hooks, su script de hook puede devolver un objeto `decision` con estos campos específicos del evento:

| Campo                | Descripción                                                                                                                                                                                                                                                                       |
| :------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `behavior`           | `"allow"` otorga el permiso, `"deny"` lo deniega. Las reglas [Deny and ask](/es/permissions#manage-permissions) aún se evalúan, por lo que un hook que devuelve `"allow"` no anula una regla de denegación coincidente                                                            |
| `updatedInput`       | Solo para `"allow"`: modifica los parámetros de entrada de la herramienta antes de la ejecución. Reemplaza el objeto de entrada completo, así que incluya campos sin cambios junto con los modificados. La entrada modificada se re-evalúa contra reglas de denegación y pregunta |
| `updatedPermissions` | Solo para `"allow"`: array de [entradas de actualización de permiso](#permission-update-entries) a aplicar, como agregar una regla de permiso o cambiar el modo de permiso de sesión                                                                                              |
| `message`            | Solo para `"deny"`: le dice a Claude por qué se denegó el permiso                                                                                                                                                                                                                 |
| `interrupt`          | Solo para `"deny"`: si es `true`, detiene a Claude                                                                                                                                                                                                                                |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": {
        "command": "npm run lint"
      }
    }
  }
}
```

#### Entradas de actualización de permiso

El campo de salida `updatedPermissions` y el campo de entrada [`permission_suggestions`](#permissionrequest-input) ambos usan el mismo array de objetos de entrada. Cada entrada tiene un `type` que determina sus otros campos, y un `destination` que controla dónde se escribe el cambio.

| `type`              | Campos                             | Efecto                                                                                                                                                                                       |
| :------------------ | :--------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `addRules`          | `rules`, `behavior`, `destination` | Agrega reglas de permiso. `rules` es un array de objetos `{toolName, ruleContent?}`. Omita `ruleContent` para coincidir con toda la herramienta. `behavior` es `"allow"`, `"deny"` o `"ask"` |
| `replaceRules`      | `rules`, `behavior`, `destination` | Reemplaza todas las reglas del `behavior` dado en el `destination` con las `rules` proporcionadas                                                                                            |
| `removeRules`       | `rules`, `behavior`, `destination` | Elimina reglas coincidentes del `behavior` dado                                                                                                                                              |
| `setMode`           | `mode`, `destination`              | Cambia el modo de permiso. Los modos válidos son `default`, `acceptEdits`, `dontAsk`, `bypassPermissions` y `plan`                                                                           |
| `addDirectories`    | `directories`, `destination`       | Agrega directorios de trabajo. `directories` es un array de cadenas de ruta                                                                                                                  |
| `removeDirectories` | `directories`, `destination`       | Elimina directorios de trabajo                                                                                                                                                               |

<Note>
  `setMode` con `bypassPermissions` solo tiene efecto si la sesión se lanzó con modo de omisión ya disponible: `--dangerously-skip-permissions`, `--permission-mode bypassPermissions`, `--allow-dangerously-skip-permissions` o `permissions.defaultMode: "bypassPermissions"` en configuración, y el modo no está deshabilitado por [`permissions.disableBypassPermissionsMode`](/es/permissions#managed-settings). De lo contrario, la actualización es una no-op. `bypassPermissions` nunca se persiste como `defaultMode` independientemente de `destination`.
</Note>

El campo `destination` en cada entrada determina si el cambio permanece en memoria o persiste en un archivo de configuración.

| `destination`     | Escribe en                                           |
| :---------------- | :--------------------------------------------------- |
| `session`         | solo en memoria, descartado cuando termina la sesión |
| `localSettings`   | `.claude/settings.local.json`                        |
| `projectSettings` | `.claude/settings.json`                              |
| `userSettings`    | `~/.claude/settings.json`                            |

Un hook puede ecoar una de las `permission_suggestions` que recibió como su propia salida `updatedPermissions`, que es equivalente a que el usuario seleccione esa opción "siempre permitir" en el diálogo.

### PostToolUse

Se ejecuta inmediatamente después de que una herramienta se completa exitosamente.

Coincide en el nombre de la herramienta, los mismos valores que PreToolUse.

#### Entrada de PostToolUse

Los hooks `PostToolUse` se activan después de que una herramienta ya se ha ejecutado exitosamente. La entrada incluye tanto `tool_input`, los argumentos enviados a la herramienta, como `tool_response`, el resultado que devolvió. El esquema exacto para ambos depende de la herramienta.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  },
  "tool_use_id": "toolu_01ABC123...",
  "duration_ms": 12
}
```

| Campo         | Descripción                                                                                                                             |
| :------------ | :-------------------------------------------------------------------------------------------------------------------------------------- |
| `duration_ms` | Opcional. Tiempo de ejecución de la herramienta en milisegundos. Excluye el tiempo dedicado a solicitudes de permiso y hooks PreToolUse |

#### Control de decisión de PostToolUse

Los hooks `PostToolUse` pueden proporcionar retroalimentación a Claude después de la ejecución de la herramienta. Además de los [campos de salida JSON](#json-output) disponibles para todos los hooks, su script de hook puede devolver estos campos específicos del evento:

| Campo                  | Descripción                                                                                                                                                       |
| :--------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `decision`             | `"block"` solicita a Claude con la `reason`. Omita para permitir que la acción continúe                                                                           |
| `reason`               | Explicación mostrada a Claude cuando `decision` es `"block"`                                                                                                      |
| `additionalContext`    | Cadena agregada al contexto de Claude junto con el resultado de la herramienta. Consulte [Agregar contexto para Claude](#add-context-for-claude)                  |
| `updatedToolOutput`    | Reemplaza la salida de la herramienta con el valor proporcionado antes de que se envíe a Claude. El valor debe coincidir con la forma de salida de la herramienta |
| `updatedMCPToolOutput` | Reemplaza la salida para [herramientas MCP](#match-mcp-tools) solo. Prefiera `updatedToolOutput`, que funciona para todas las herramientas                        |

El ejemplo a continuación reemplaza la salida de una llamada `Bash`. El valor de reemplazo coincide con la forma de salida de la herramienta `Bash`:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude",
    "updatedToolOutput": {
      "stdout": "[redacted]",
      "stderr": "",
      "interrupted": false,
      "isImage": false
    }
  }
}
```

<Warning>
  `updatedToolOutput` solo cambia lo que Claude ve. La herramienta ya se ha ejecutado en el momento en que se activa el hook, por lo que cualquier archivo escrito, comando ejecutado o solicitud de red enviada ya ha tenido efecto. La telemetría como spans de herramientas OpenTelemetry y eventos de análisis también capturan la salida original antes de que se ejecute el hook. Para evitar o modificar una llamada a herramienta antes de que se ejecute, use un hook [PreToolUse](#pretooluse) en su lugar.

  El valor de reemplazo debe coincidir con la forma de salida de la herramienta. Las herramientas integradas devuelven objetos estructurados en lugar de cadenas simples. Por ejemplo, `Bash` devuelve un objeto con campos `stdout`, `stderr`, `interrupted` e `isImage`. Para herramientas integradas, un valor que no coincida con el esquema de salida de la herramienta se ignora y se usa la salida original. La salida de herramientas MCP se pasa sin validación de esquema. Eliminar detalles de error que Claude necesita puede hacer que continúe con una suposición falsa.
</Warning>

### PostToolUseFailure

Se ejecuta cuando falla la ejecución de una herramienta. Este evento se activa para llamadas a herramientas que lanzan errores o devuelven resultados de fallo. Use esto para registrar fallos, enviar alertas o proporcionar retroalimentación correctiva a Claude.

Coincide en el nombre de la herramienta, los mismos valores que PreToolUse.

#### Entrada de PostToolUseFailure

Los hooks PostToolUseFailure reciben los mismos campos `tool_name` y `tool_input` que PostToolUse, junto con información de error como campos de nivel superior:

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUseFailure",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run test suite"
  },
  "tool_use_id": "toolu_01ABC123...",
  "error": "Command exited with non-zero status code 1",
  "is_interrupt": false,
  "duration_ms": 4187
}
```

| Campo          | Descripción                                                                                                                             |
| :------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| `error`        | Cadena que describe qué salió mal                                                                                                       |
| `is_interrupt` | Booleano opcional que indica si el fallo fue causado por interrupción del usuario                                                       |
| `duration_ms`  | Opcional. Tiempo de ejecución de la herramienta en milisegundos. Excluye el tiempo dedicado a solicitudes de permiso y hooks PreToolUse |

#### Control de decisión de PostToolUseFailure

Los hooks `PostToolUseFailure` pueden proporcionar contexto a Claude después de un fallo de herramienta. Además de los [campos de salida JSON](#json-output) disponibles para todos los hooks, su script de hook puede devolver estos campos específicos del evento:

| Campo               | Descripción                                                                                                                |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------- |
| `additionalContext` | Cadena agregada al contexto de Claude junto con el error. Consulte [Agregar contexto para Claude](#add-context-for-claude) |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUseFailure",
    "additionalContext": "Additional information about the failure for Claude"
  }
}
```

### PostToolBatch

Se ejecuta una vez después de que cada llamada a herramienta en un lote se haya resuelto, antes de que Claude Code envíe la siguiente solicitud al modelo. `PostToolUse` se activa una vez por herramienta, lo que significa que se activa simultáneamente cuando Claude hace llamadas a herramientas paralelas. `PostToolBatch` se activa exactamente una vez con el lote completo, por lo que es el lugar correcto para inyectar contexto que dependa del conjunto de herramientas que se ejecutaron en lugar de cualquier herramienta individual. No hay matcher para este evento.

#### Entrada de PostToolBatch

Además de los [campos de entrada comunes](#common-input-fields), los hooks PostToolBatch reciben `tool_calls`, un array que describe cada llamada a herramienta en el lote:

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolBatch",
  "tool_calls": [
    {
      "tool_name": "Read",
      "tool_input": {"file_path": "/.../ledger/accounts.py"},
      "tool_use_id": "toolu_01...",
      "tool_response": "     1\tfrom __future__ import annotations\n     2\t..."
    },
    {
      "tool_name": "Read",
      "tool_input": {"file_path": "/.../ledger/transactions.py"},
      "tool_use_id": "toolu_02...",
      "tool_response": "     1\tfrom __future__ import annotations\n     2\t..."
    }
  ]
}
```

`tool_response` contiene el mismo contenido que el modelo recibe en el bloque `tool_result` correspondiente. El valor es una cadena serializada o un array de bloque de contenido, exactamente como lo emitió la herramienta. Para `Read`, eso significa texto con prefijo de número de línea en lugar de contenidos de archivo sin procesar. Las respuestas pueden ser grandes, así que analice solo los campos que necesita.

<Note>
  La forma de `tool_response` difiere de la de `PostToolUse`. `PostToolUse` pasa el objeto `Output` estructurado de la herramienta, como `{filePath: "...", success: true}` para `Write`; `PostToolBatch` pasa el contenido `tool_result` serializado que el modelo ve.
</Note>

#### Control de decisión de PostToolBatch

Los hooks `PostToolBatch` pueden inyectar contexto para Claude. Además de los [campos de salida JSON](#json-output) disponibles para todos los hooks, su script de hook puede devolver estos campos específicos del evento:

| Campo               | Descripción                                                                                                                                                                                                                                     |
| :------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `additionalContext` | Cadena de contexto inyectada una vez antes de la siguiente llamada al modelo. Consulte [Agregar contexto para Claude](#add-context-for-claude) para detalles de entrega, qué poner en él y cómo las sesiones reanudadas manejan valores pasados |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolBatch",
    "additionalContext": "These files are part of the ledger module. Run pytest before marking the task complete."
  }
}
```

Devolver `decision: "block"` o `continue: false` detiene el bucle agentico antes de la siguiente llamada al modelo.

### PermissionDenied

Se ejecuta cuando el clasificador de [modo automático](/es/permission-modes#eliminate-prompts-with-auto-mode) deniega una llamada a herramienta. Este hook solo se activa en modo automático: no se ejecuta cuando deniega manualmente un diálogo de permiso, cuando un hook `PreToolUse` bloquea una llamada o cuando una regla `deny` coincide. Use esto para registrar denegaciones del clasificador, ajustar configuración o decirle al modelo que puede reintentar la llamada a herramienta.

Coincide en el nombre de la herramienta, los mismos valores que PreToolUse.

#### Entrada de PermissionDenied

Además de los [campos de entrada comunes](#common-input-fields), los hooks PermissionDenied reciben `tool_name`, `tool_input`, `tool_use_id` y `reason`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "auto",
  "hook_event_name": "PermissionDenied",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /tmp/build",
    "description": "Clean build directory"
  },
  "tool_use_id": "toolu_01ABC123...",
  "reason": "Auto mode denied: command targets a path outside the project"
}
```

| Campo    | Descripción                                                                     |
| :------- | :------------------------------------------------------------------------------ |
| `reason` | La explicación del clasificador para por qué se denegó la llamada a herramienta |

#### Control de decisión de PermissionDenied

Los hooks PermissionDenied pueden decirle al modelo que puede reintentar la llamada a herramienta denegada. Devuelva un objeto JSON con `hookSpecificOutput.retry` establecido en `true`:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionDenied",
    "retry": true
  }
}
```

Cuando `retry` es `true`, Claude Code agrega un mensaje a la conversación diciéndole al modelo que puede reintentar la llamada a herramienta. La denegación en sí no se revierte. Si su hook no devuelve JSON, o devuelve `retry: false`, la denegación se mantiene y el modelo recibe el mensaje de rechazo original.

### Notification

Se ejecuta cuando Claude Code envía notificaciones. Coincide en el tipo de notificación: `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`, `elicitation_complete`, `elicitation_response`. Omita el matcher para ejecutar hooks para todos los tipos de notificación.

Use matchers separados para ejecutar diferentes controladores dependiendo del tipo de notificación. Esta configuración desencadena un script de alerta específico de permiso cuando Claude necesita aprobación de permiso y una notificación diferente cuando Claude ha estado inactivo:

```json theme={null}
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/permission-alert.sh"
          }
        ]
      },
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/idle-notification.sh"
          }
        ]
      }
    ]
  }
}
```

#### Entrada de Notification

Además de los [campos de entrada comunes](#common-input-fields), los hooks Notification reciben `message` con el texto de notificación, un `title` opcional y `notification_type` que indica qué tipo se activó.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Notification",
  "message": "Claude needs your permission to use Bash",
  "title": "Permission needed",
  "notification_type": "permission_prompt"
}
```

Los hooks Notification no pueden bloquear o modificar notificaciones. Están destinados a efectos secundarios como reenviar la notificación a un servicio externo. Los [campos de salida JSON](#json-output) comunes como `systemMessage` se aplican.

### SubagentStart

Se ejecuta cuando se genera un subagente de Claude Code a través de la herramienta Agent. Admite matchers para filtrar por nombre de tipo de agente (agentes integrados como `general-purpose`, `Explore`, `Plan` o nombres de agentes personalizados de `.claude/agents/`).

#### Entrada de SubagentStart

Además de los [campos de entrada comunes](#common-input-fields), los hooks SubagentStart reciben `agent_id` con el identificador único para el subagente y `agent_type` con el nombre del agente (agentes integrados como `"general-purpose"`, `"Explore"`, `"Plan"` o nombres de agentes personalizados).

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SubagentStart",
  "agent_id": "agent-abc123",
  "agent_type": "Explore"
}
```

Los hooks SubagentStart no pueden bloquear la creación de subagentes, pero pueden inyectar contexto en el subagente. Además de los [campos de salida JSON](#json-output) disponibles para todos los hooks, puede devolver:

| Campo               | Descripción                                                                                                                                                         |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `additionalContext` | Cadena agregada al contexto del subagente al inicio de su conversación, antes de su primer prompt. Consulte [Agregar contexto para Claude](#add-context-for-claude) |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "Follow security guidelines for this task"
  }
}
```

### SubagentStop

Se ejecuta cuando un subagente de Claude Code ha terminado de responder. Coincide en el tipo de agente, los mismos valores que SubagentStart.

#### Entrada de SubagentStop

Además de los [campos de entrada comunes](#common-input-fields), los hooks SubagentStop reciben `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path` y `last_assistant_message`. El campo `agent_type` es el valor usado para filtrado de matcher. El `transcript_path` es la transcripción de la sesión principal, mientras que `agent_transcript_path` es la propia transcripción del subagente almacenada en una carpeta `subagents/` anidada. El campo `last_assistant_message` contiene el contenido de texto de la respuesta final del subagente, por lo que los hooks pueden acceder a él sin analizar el archivo de transcripción.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../abc123.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SubagentStop",
  "stop_hook_active": false,
  "agent_id": "def456",
  "agent_type": "Explore",
  "agent_transcript_path": "~/.claude/projects/.../abc123/subagents/agent-def456.jsonl",
  "last_assistant_message": "Analysis complete. Found 3 potential issues..."
}
```

Los hooks SubagentStop usan el mismo formato de control de decisión que los [hooks Stop](#stop-decision-control).

### TaskCreated

Se ejecuta cuando se está creando una tarea a través de la herramienta `TaskCreate`. Use esto para aplicar convenciones de nomenclatura, requerir descripciones de tareas o evitar que se creen ciertas tareas.

Cuando un hook `TaskCreated` sale con código 2, la tarea no se crea y el mensaje de stderr se devuelve al modelo como retroalimentación. Para detener al compañero completamente en lugar de re-ejecutarlo, devuelva JSON con `{"continue": false, "stopReason": "..."}`. Los hooks TaskCreated no admiten matchers y se activan en cada ocurrencia.

#### Entrada de TaskCreated

Además de los [campos de entrada comunes](#common-input-fields), los hooks TaskCreated reciben `task_id`, `task_subject` y opcionalmente `task_description`, `teammate_name` y `team_name`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TaskCreated",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "my-project"
}
```

| Campo              | Descripción                                                 |
| :----------------- | :---------------------------------------------------------- |
| `task_id`          | Identificador de la tarea que se está creando               |
| `task_subject`     | Título de la tarea                                          |
| `task_description` | Descripción detallada de la tarea. Puede estar ausente      |
| `teammate_name`    | Nombre del compañero que crea la tarea. Puede estar ausente |
| `team_name`        | Nombre del equipo. Puede estar ausente                      |

#### Control de decisión de TaskCreated

Los hooks TaskCreated admiten dos formas de controlar la creación de tareas:

* **Código de salida 2**: la tarea no se crea y el mensaje de stderr se devuelve al modelo como retroalimentación.
* **JSON `{"continue": false, "stopReason": "..."}`**: detiene al compañero completamente, coincidiendo con el comportamiento del hook `Stop`. El `stopReason` se muestra al usuario.

Este ejemplo bloquea tareas cujos asuntos no siguen el formato requerido:

```bash theme={null}
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

if [[ ! "$TASK_SUBJECT" =~ ^\[TICKET-[0-9]+\] ]]; then
  echo "Task subject must start with a ticket number, e.g. '[TICKET-123] Add feature'" >&2
  exit 2
fi

exit 0
```

### TaskCompleted

Se ejecuta cuando una tarea está siendo marcada como completada. Esto se activa en dos situaciones: cuando cualquier agente marca explícitamente una tarea como completada a través de la herramienta TaskUpdate, o cuando un compañero de [equipo de agentes](/es/agent-teams) termina su turno con tareas en progreso. Use esto para aplicar criterios de finalización como pasar pruebas o verificaciones de lint antes de que una tarea pueda cerrarse.

Cuando un hook `TaskCompleted` sale con código 2, la tarea no se marca como completada y el mensaje de stderr se devuelve al modelo como retroalimentación. Para detener al compañero completamente en lugar de re-ejecutarlo, devuelva JSON con `{"continue": false, "stopReason": "..."}`. Los hooks TaskCompleted no admiten matchers y se activan en cada ocurrencia.

#### Entrada de TaskCompleted

Además de los [campos de entrada comunes](#common-input-fields), los hooks TaskCompleted reciben `task_id`, `task_subject` y opcionalmente `task_description`, `teammate_name` y `team_name`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TaskCompleted",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "my-project"
}
```

| Campo              | Descripción                                                     |
| :----------------- | :-------------------------------------------------------------- |
| `task_id`          | Identificador de la tarea que se está completando               |
| `task_subject`     | Título de la tarea                                              |
| `task_description` | Descripción detallada de la tarea. Puede estar ausente          |
| `teammate_name`    | Nombre del compañero que completa la tarea. Puede estar ausente |
| `team_name`        | Nombre del equipo. Puede estar ausente                          |

#### Control de decisión de TaskCompleted

Los hooks TaskCompleted admiten dos formas de controlar la finalización de tareas:

* **Código de salida 2**: la tarea no se marca como completada y el mensaje de stderr se devuelve al modelo como retroalimentación.
* **JSON `{"continue": false, "stopReason": "..."}`**: detiene al compañero completamente, coincidiendo con el comportamiento del hook `Stop`. El `stopReason` se muestra al usuario.

Este ejemplo ejecuta pruebas y bloquea la finalización de tareas si fallan:

```bash theme={null}
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

# Ejecute el conjunto de pruebas
if ! npm test 2>&1; then
  echo "Tests not passing. Fix failing tests before completing: $TASK_SUBJECT" >&2
  exit 2
fi

exit 0
```

### Stop

Se ejecuta cuando el agente principal de Claude Code ha terminado de responder. No se ejecuta si la detención ocurrió debido a una interrupción del usuario. Los errores de API activan [StopFailure](#stopfailure) en su lugar.

#### Entrada de Stop

Además de los [campos de entrada comunes](#common-input-fields), los hooks Stop reciben `stop_hook_active` y `last_assistant_message`. El campo `stop_hook_active` es `true` cuando Claude Code ya está continuando como resultado de un hook de parada. Verifique este valor o procese la transcripción para evitar que Claude Code se ejecute indefinidamente. El campo `last_assistant_message` contiene el contenido de texto de la respuesta final de Claude, por lo que los hooks pueden acceder a él sin analizar el archivo de transcripción.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": true,
  "last_assistant_message": "I've completed the refactoring. Here's a summary..."
}
```

#### Control de decisión de Stop

Los hooks `Stop` y `SubagentStop` pueden controlar si Claude continúa. Además de los [campos de salida JSON](#json-output) disponibles para todos los hooks, su script de hook puede devolver estos campos específicos del evento:

| Campo      | Descripción                                                                       |
| :--------- | :-------------------------------------------------------------------------------- |
| `decision` | `"block"` evita que Claude se detenga. Omita para permitir que Claude se detenga  |
| `reason`   | Requerido cuando `decision` es `"block"`. Le dice a Claude por qué debe continuar |

```json theme={null}
{
  "decision": "block",
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

### StopFailure

Se ejecuta en lugar de [Stop](#stop) cuando el turno termina debido a un error de API. La salida y el código de salida se ignoran. Use esto para registrar fallos, enviar alertas o tomar acciones de recuperación cuando Claude no puede completar una respuesta debido a límites de velocidad, problemas de autenticación u otros errores de API.

#### Entrada de StopFailure

Además de los [campos de entrada comunes](#common-input-fields), los hooks StopFailure reciben `error`, `error_details` opcional y `last_assistant_message` opcional. El campo `error` identifica el tipo de error y se usa para filtrado de matcher.

| Campo                    | Descripción                                                                                                                                                                                                                                                           |
| :----------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `error`                  | Tipo de error: `rate_limit`, `authentication_failed`, `oauth_org_not_allowed`, `billing_error`, `invalid_request`, `server_error`, `max_output_tokens` u `unknown`                                                                                                    |
| `error_details`          | Detalles adicionales sobre el error, cuando estén disponibles                                                                                                                                                                                                         |
| `last_assistant_message` | El texto de error renderizado mostrado en la conversación. A diferencia de `Stop` y `SubagentStop`, donde este campo contiene la salida conversacional de Claude, para `StopFailure` contiene la cadena de error de API en sí, como `"API Error: Rate limit reached"` |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "StopFailure",
  "error": "rate_limit",
  "error_details": "429 Too Many Requests",
  "last_assistant_message": "API Error: Rate limit reached"
}
```

Los hooks StopFailure no tienen control de decisión. Se ejecutan solo con fines de notificación y registro.

### TeammateIdle

Se ejecuta cuando un compañero de [equipo de agentes](/es/agent-teams) está a punto de quedarse inactivo después de terminar su turno. Use esto para aplicar puertas de calidad antes de que un compañero deje de trabajar, como requerir que pasen verificaciones de lint o verificar que existan archivos de salida.

Cuando un hook `TeammateIdle` sale con código 2, el compañero recibe el mensaje de stderr como retroalimentación y continúa trabajando en lugar de quedarse inactivo. Para detener al compañero completamente en lugar de re-ejecutarlo, devuelva JSON con `{"continue": false, "stopReason": "..."}`. Los hooks TeammateIdle no admiten matchers y se activan en cada ocurrencia.

#### Entrada de TeammateIdle

Además de los [campos de entrada comunes](#common-input-fields), los hooks TeammateIdle reciben `teammate_name` y `team_name`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TeammateIdle",
  "teammate_name": "researcher",
  "team_name": "my-project"
}
```

| Campo           | Descripción                                                |
| :-------------- | :--------------------------------------------------------- |
| `teammate_name` | Nombre del compañero que está a punto de quedarse inactivo |
| `team_name`     | Nombre del equipo                                          |

#### Control de decisión de TeammateIdle

Los hooks TeammateIdle admiten dos formas de controlar el comportamiento del compañero:

* **Código de salida 2**: el compañero recibe el mensaje de stderr como retroalimentación y continúa trabajando en lugar de quedarse inactivo.
* **JSON `{"continue": false, "stopReason": "..."}`**: detiene al compañero completamente, coincidiendo con el comportamiento del hook `Stop`. El `stopReason` se muestra al usuario.

Este ejemplo verifica que exista un artefacto de compilación antes de permitir que un compañero se quede inactivo:

```bash theme={null}
#!/bin/bash

if [ ! -f "./dist/output.js" ]; then
  echo "Build artifact missing. Run the build before stopping." >&2
  exit 2
fi

exit 0
```

### ConfigChange

Se ejecuta cuando un archivo de configuración cambia durante una sesión. Use esto para auditar cambios de configuración, aplicar políticas de seguridad o bloquear modificaciones no autorizadas a archivos de configuración.

Los hooks ConfigChange se activan para cambios en archivos de configuración, configuración de política administrada y archivos de skill. El campo `source` en la entrada le dice qué tipo de configuración cambió, y el campo `file_path` opcional proporciona la ruta al archivo cambiado.

El matcher filtra en la fuente de configuración:

| Matcher            | Cuándo se activa                                  |
| :----------------- | :------------------------------------------------ |
| `user_settings`    | `~/.claude/settings.json` cambia                  |
| `project_settings` | `.claude/settings.json` cambia                    |
| `local_settings`   | `.claude/settings.local.json` cambia              |
| `policy_settings`  | Cambios de configuración de política administrada |
| `skills`           | Un archivo de skill en `.claude/skills/` cambia   |

Este ejemplo registra todos los cambios de configuración para auditoría de seguridad:

```json theme={null}
{
  "hooks": {
    "ConfigChange": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/audit-config-change.sh"
          }
        ]
      }
    ]
  }
}
```

#### Entrada de ConfigChange

Además de los [campos de entrada comunes](#common-input-fields), los hooks ConfigChange reciben `source` y opcionalmente `file_path`. El campo `source` indica qué tipo de configuración cambió, y `file_path` proporciona la ruta al archivo específico que se modificó.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "ConfigChange",
  "source": "project_settings",
  "file_path": "/Users/.../my-project/.claude/settings.json"
}
```

#### Control de decisión de ConfigChange

Los hooks ConfigChange pueden bloquear cambios de configuración para que no tengan efecto. Use código de salida 2 o un JSON `decision` para evitar el cambio. Cuando se bloquea, la nueva configuración no se aplica a la sesión en ejecución.

| Campo      | Descripción                                                                              |
| :--------- | :--------------------------------------------------------------------------------------- |
| `decision` | `"block"` evita que el cambio de configuración se aplique. Omita para permitir el cambio |
| `reason`   | Explicación mostrada al usuario cuando `decision` es `"block"`                           |

```json theme={null}
{
  "decision": "block",
  "reason": "Configuration changes to project settings require admin approval"
}
```

Los cambios de `policy_settings` no pueden bloquearse. Los hooks aún se activan para fuentes de `policy_settings`, por lo que puede usarlos para registro de auditoría, pero cualquier decisión de bloqueo se ignora. Esto asegura que la configuración administrada por empresa siempre tenga efecto.

### CwdChanged

Se ejecuta cuando el directorio de trabajo cambia durante una sesión, por ejemplo cuando Claude ejecuta un comando `cd`. Use esto para reaccionar a cambios de directorio: recargar variables de entorno, activar cadenas de herramientas específicas del proyecto o ejecutar scripts de configuración automáticamente. Se empareja con [FileChanged](#filechanged) para herramientas como [direnv](https://direnv.net/) que administran el entorno por directorio.

Los hooks CwdChanged tienen acceso a `CLAUDE_ENV_FILE`. Las variables escritas en ese archivo persisten en comandos Bash posteriores para la sesión, al igual que en los [hooks SessionStart](#persist-environment-variables).

CwdChanged no admite matchers y se activa en cada cambio de directorio.

#### Entrada de CwdChanged

Además de los [campos de entrada comunes](#common-input-fields), los hooks CwdChanged reciben `old_cwd` y `new_cwd`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project/src",
  "hook_event_name": "CwdChanged",
  "old_cwd": "/Users/my-project",
  "new_cwd": "/Users/my-project/src"
}
```

#### Salida de CwdChanged

Además de los [campos de salida JSON](#json-output) disponibles para todos los hooks, los hooks CwdChanged pueden devolver `watchPaths` para establecer dinámicamente qué rutas de archivo [FileChanged](#filechanged) monitorea:

| Campo        | Descripción                                                                                                                                                                                                                                   |
| :----------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `watchPaths` | Array de rutas absolutas. Reemplaza la lista de monitoreo dinámica actual (las rutas de su configuración de `matcher` siempre se monitorean). Devolver un array vacío borra la lista dinámica, que es típico al entrar en un nuevo directorio |

Los hooks CwdChanged no tienen control de decisión. No pueden bloquear el cambio de directorio.

### FileChanged

Se ejecuta cuando un archivo monitoreado cambia en el disco. Útil para recargar variables de entorno cuando se modifican archivos de configuración del proyecto.

El `matcher` para este evento sirve dos propósitos:

* **Construir la lista de vigilancia**: el valor se divide en `|` y cada segmento se registra como un nombre de archivo literal en el directorio de trabajo, por lo que `".envrc|.env"` vigila exactamente esos dos archivos. Los patrones regex no son útiles aquí: un valor como `^\.env` vigilaría un archivo literalmente nombrado `^\.env`.
* **Filtrar qué hooks se ejecutan**: cuando cambia un archivo vigilado, el mismo valor filtra qué grupos de hooks se ejecutan usando las [reglas de matcher](#matcher-patterns) estándar contra el basename del archivo cambiado.

Los hooks FileChanged tienen acceso a `CLAUDE_ENV_FILE`. Las variables escritas en ese archivo persisten en comandos Bash posteriores para la sesión, al igual que en los [hooks SessionStart](#persist-environment-variables).

#### Entrada de FileChanged

Además de los [campos de entrada comunes](#common-input-fields), los hooks FileChanged reciben `file_path` y `event`.

| Campo       | Descripción                                                                                             |
| :---------- | :------------------------------------------------------------------------------------------------------ |
| `file_path` | Ruta absoluta al archivo que cambió                                                                     |
| `event`     | Qué sucedió: `"change"` (archivo modificado), `"add"` (archivo creado) o `"unlink"` (archivo eliminado) |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "FileChanged",
  "file_path": "/Users/my-project/.envrc",
  "event": "change"
}
```

#### Salida de FileChanged

Además de los [campos de salida JSON](#json-output) disponibles para todos los hooks, los hooks FileChanged pueden devolver `watchPaths` para actualizar dinámicamente qué rutas de archivo se monitorean:

| Campo        | Descripción                                                                                                                                                                                                                                                  |
| :----------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `watchPaths` | Array de rutas absolutas. Reemplaza la lista de monitoreo dinámica actual (las rutas de su configuración de `matcher` siempre se monitorean). Use esto cuando su script de hook descubra archivos adicionales para monitorear basados en el archivo cambiado |

Los hooks FileChanged no tienen control de decisión. No pueden bloquear el cambio de archivo.

### WorktreeCreate

Cuando ejecuta `claude --worktree` o un [subagente usa `isolation: "worktree"`](/es/sub-agents#choose-the-subagent-scope), Claude Code crea una copia de trabajo aislada usando `git worktree`. Si configura un hook WorktreeCreate, reemplaza el comportamiento predeterminado de git, permitiéndole usar un sistema de control de versiones diferente como SVN, Perforce o Mercurial.

Debido a que el hook reemplaza el comportamiento predeterminado completamente, [`.worktreeinclude`](/es/common-workflows#copy-gitignored-files-to-worktrees) no se procesa. Si necesita copiar archivos de configuración local como `.env` en el nuevo worktree, hágalo dentro de su script de hook.

El hook debe devolver la ruta absoluta al directorio de worktree creado. Claude Code usa esta ruta como el directorio de trabajo para la sesión aislada. Los hooks de comando la imprimen en stdout; los hooks HTTP la devuelven a través de `hookSpecificOutput.worktreePath`.

Este ejemplo crea una copia de trabajo SVN e imprime la ruta para que Claude Code la use. Reemplace la URL del repositorio con la suya:

```json theme={null}
{
  "hooks": {
    "WorktreeCreate": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'NAME=$(jq -r .name); DIR=\"$HOME/.claude/worktrees/$NAME\"; svn checkout https://svn.example.com/repo/trunk \"$DIR\" >&2 && echo \"$DIR\"'"
          }
        ]
      }
    ]
  }
}
```

El hook lee el `name` del worktree de la entrada JSON en stdin, verifica una copia fresca en un nuevo directorio e imprime la ruta del directorio. El `echo` en la última línea es lo que Claude Code lee como la ruta del worktree. Redirija cualquier otra salida a stderr para que no interfiera con la ruta.

#### Entrada de WorktreeCreate

Además de los [campos de entrada comunes](#common-input-fields), los hooks WorktreeCreate reciben el campo `name`. Este es un identificador slug para el nuevo worktree, especificado por el usuario o generado automáticamente (por ejemplo, `bold-oak-a3f2`).

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeCreate",
  "name": "feature-auth"
}
```

#### Salida de WorktreeCreate

Los hooks WorktreeCreate no usan el modelo de decisión de permitir/bloquear estándar. En su lugar, el éxito o fallo del hook determina el resultado. El hook debe devolver la ruta absoluta al directorio de worktree creado:

* **Hooks de comando** (`type: "command"`): imprimen la ruta en stdout.
* **Hooks HTTP** (`type: "http"`): devuelven `{ "hookSpecificOutput": { "hookEventName": "WorktreeCreate", "worktreePath": "/absolute/path" } }` en el cuerpo de la respuesta.

Si el hook falla o no produce ruta, la creación de worktree falla con un error.

### WorktreeRemove

La contraparte de limpieza de [WorktreeCreate](#worktreecreate). Este hook se activa cuando se está eliminando un worktree, ya sea cuando sale de una sesión `--worktree` y elige eliminarlo, o cuando un subagente con `isolation: "worktree"` finaliza. Para worktrees basados en git, Claude maneja la limpieza automáticamente con `git worktree remove`. Si configuró un hook WorktreeCreate para un sistema de control de versiones que no es git, emparéjelo con un hook WorktreeRemove para manejar la limpieza. Sin uno, el directorio de worktree se deja en el disco.

Claude Code pasa la ruta devuelta por WorktreeCreate como `worktree_path` en la entrada del hook. Este ejemplo lee esa ruta y elimina el directorio:

```json theme={null}
{
  "hooks": {
    "WorktreeRemove": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'jq -r .worktree_path | xargs rm -rf'"
          }
        ]
      }
    ]
  }
}
```

#### Entrada de WorktreeRemove

Además de los [campos de entrada comunes](#common-input-fields), los hooks WorktreeRemove reciben el campo `worktree_path`, que es la ruta absoluta al worktree que se está eliminando.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeRemove",
  "worktree_path": "/Users/.../my-project/.claude/worktrees/feature-auth"
}
```

Los hooks WorktreeRemove no tienen control de decisión. No pueden bloquear la eliminación de worktree pero pueden realizar tareas de limpieza como eliminar estado de control de versiones o archivar cambios. Los fallos de hook se registran solo en modo de depuración.

### PreCompact

Se ejecuta antes de que Claude Code esté a punto de ejecutar una operación de compactación.

El valor del matcher indica si la compactación fue desencadenada manualmente o automáticamente:

| Matcher  | Cuándo se activa                                                 |
| :------- | :--------------------------------------------------------------- |
| `manual` | `/compact`                                                       |
| `auto`   | Compactación automática cuando la ventana de contexto está llena |

Salga con código 2 para bloquear la compactación. Para un `/compact` manual, el mensaje de stderr se muestra al usuario. También puede bloquear devolviendo JSON con `"decision": "block"`.

Bloquear la compactación automática tiene diferentes efectos dependiendo de cuándo se active. Si la compactación fue desencadenada de forma proactiva antes del límite de contexto, Claude Code la omite y la conversación continúa sin compactar. Si la compactación fue desencadenada para recuperarse de un error de límite de contexto ya devuelto por la API, el error subyacente aparece y la solicitud actual falla.

#### Entrada de PreCompact

Además de los [campos de entrada comunes](#common-input-fields), los hooks PreCompact reciben `trigger` e `custom_instructions`. Para `manual`, `custom_instructions` contiene lo que el usuario pasa a `/compact`. Para `auto`, `custom_instructions` está vacío.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```

### PostCompact

Se ejecuta después de que Claude Code completa una operación de compactación. Use este evento para reaccionar al nuevo estado compactado, por ejemplo para registrar el resumen generado o actualizar el estado externo.

Los mismos valores de matcher se aplican que para `PreCompact`:

| Matcher  | Cuándo se activa                                                            |
| :------- | :-------------------------------------------------------------------------- |
| `manual` | Después de `/compact`                                                       |
| `auto`   | Después de compactación automática cuando la ventana de contexto está llena |

#### Entrada de PostCompact

Además de los [campos de entrada comunes](#common-input-fields), los hooks PostCompact reciben `trigger` y `compact_summary`. El campo `compact_summary` contiene el resumen de conversación generado por la operación de compactación.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PostCompact",
  "trigger": "manual",
  "compact_summary": "Summary of the compacted conversation..."
}
```

Los hooks PostCompact no tienen control de decisión. No pueden afectar el resultado de compactación pero pueden realizar tareas de seguimiento.

### SessionEnd

Se ejecuta cuando termina una sesión de Claude Code. Útil para tareas de limpieza, registro de estadísticas de sesión o guardado del estado de sesión. Admite matchers para filtrar por razón de salida.

El campo `reason` en la entrada del hook indica por qué terminó la sesión:

| Razón                         | Descripción                                              |
| :---------------------------- | :------------------------------------------------------- |
| `clear`                       | Sesión borrada con comando `/clear`                      |
| `resume`                      | Sesión cambiada a través de `/resume` interactivo        |
| `logout`                      | Usuario cerró sesión                                     |
| `prompt_input_exit`           | Usuario salió mientras la entrada del prompt era visible |
| `bypass_permissions_disabled` | El modo de permisos de omisión fue deshabilitado         |
| `other`                       | Otras razones de salida                                  |

#### Entrada de SessionEnd

Además de los [campos de entrada comunes](#common-input-fields), los hooks SessionEnd reciben un campo `reason` que indica por qué terminó la sesión. Consulte la [tabla de razones](#sessionend) anterior para todos los valores.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionEnd",
  "reason": "other"
}
```

Los hooks SessionEnd no tienen control de decisión. No pueden bloquear la terminación de sesión pero pueden realizar tareas de limpieza.

Los hooks SessionEnd tienen un tiempo de espera predeterminado de 1,5 segundos. Esto se aplica tanto a la salida de sesión como a `/clear` y al cambio de sesiones a través de `/resume` interactivo. Si un hook necesita más tiempo, establezca un `timeout` por hook en la configuración del hook. El presupuesto general se aumenta automáticamente al tiempo de espera por hook más alto configurado en archivos de configuración, hasta 60 segundos. Los tiempos de espera establecidos en hooks proporcionados por plugins no aumentan el presupuesto. Para anular el presupuesto explícitamente, establezca la variable de entorno `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` en milisegundos.

```bash theme={null}
CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS=5000 claude
```

### Elicitation

Se ejecuta cuando un servidor MCP solicita entrada del usuario a mitad de la tarea. Por defecto, Claude Code muestra un diálogo interactivo para que el usuario responda. Los hooks pueden interceptar esta solicitud y responder programáticamente, omitiendo el diálogo completamente.

El campo matcher coincide con el nombre del servidor MCP.

#### Entrada de Elicitation

Además de los [campos de entrada comunes](#common-input-fields), los hooks Elicitation reciben `mcp_server_name`, `message` y campos opcionales `mode`, `url`, `elicitation_id` y `requested_schema`.

Para elicitación en modo formulario (el caso más común):

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please provide your credentials",
  "mode": "form",
  "requested_schema": {
    "type": "object",
    "properties": {
      "username": { "type": "string", "title": "Username" }
    }
  }
}
```

Para elicitación en modo URL (autenticación basada en navegador):

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please authenticate",
  "mode": "url",
  "url": "https://auth.example.com/login"
}
```

#### Salida de Elicitation

Para responder programáticamente sin mostrar el diálogo, devuelva un objeto JSON con `hookSpecificOutput`:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "Elicitation",
    "action": "accept",
    "content": {
      "username": "alice"
    }
  }
}
```

| Campo     | Valores                       | Descripción                                                                      |
| :-------- | :---------------------------- | :------------------------------------------------------------------------------- |
| `action`  | `accept`, `decline`, `cancel` | Si aceptar, rechazar o cancelar la solicitud                                     |
| `content` | object                        | Valores de campo de formulario a enviar. Solo se usa cuando `action` es `accept` |

El código de salida 2 deniega la elicitación y muestra stderr al usuario.

### ElicitationResult

Se ejecuta después de que un usuario responde a una elicitación MCP. Los hooks pueden observar, modificar o bloquear la respuesta antes de que se envíe de vuelta al servidor MCP.

El campo matcher coincide con el nombre del servidor MCP.

#### Entrada de ElicitationResult

Además de los [campos de entrada comunes](#common-input-fields), los hooks ElicitationResult reciben `mcp_server_name`, `action` y campos opcionales `mode`, `elicitation_id` y `content`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "ElicitationResult",
  "mcp_server_name": "my-mcp-server",
  "action": "accept",
  "content": { "username": "alice" },
  "mode": "form",
  "elicitation_id": "elicit-123"
}
```

#### Salida de ElicitationResult

Para anular la respuesta del usuario, devuelva un objeto JSON con `hookSpecificOutput`:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "ElicitationResult",
    "action": "decline",
    "content": {}
  }
}
```

| Campo     | Valores                       | Descripción                                                                          |
| :-------- | :---------------------------- | :----------------------------------------------------------------------------------- |
| `action`  | `accept`, `decline`, `cancel` | Anula la acción del usuario                                                          |
| `content` | object                        | Anula valores de campo de formulario. Solo significativo cuando `action` es `accept` |

El código de salida 2 bloquea la respuesta, cambiando la acción efectiva a `decline`.

## Hooks basados en prompts

Además de hooks de comando, HTTP y herramientas MCP, Claude Code admite hooks basados en prompts (`type: "prompt"`) que usan un LLM para evaluar si permitir o bloquear una acción, y hooks de agente (`type: "agent"`) que generan un verificador agentico con acceso a herramientas. No todos los eventos admiten todos los tipos de hooks.

Eventos que admiten los cinco tipos de hooks (`command`, `http`, `mcp_tool`, `prompt` y `agent`):

* `PermissionRequest`
* `PostToolBatch`
* `PostToolUse`
* `PostToolUseFailure`
* `PreToolUse`
* `Stop`
* `SubagentStop`
* `TaskCompleted`
* `TaskCreated`
* `UserPromptExpansion`
* `UserPromptSubmit`

Eventos que admiten hooks `command`, `http` y `mcp_tool` pero no `prompt` o `agent`:

* `ConfigChange`
* `CwdChanged`
* `Elicitation`
* `ElicitationResult`
* `FileChanged`
* `InstructionsLoaded`
* `Notification`
* `PermissionDenied`
* `PostCompact`
* `PreCompact`
* `SessionEnd`
* `StopFailure`
* `SubagentStart`
* `TeammateIdle`
* `WorktreeCreate`
* `WorktreeRemove`

`SessionStart` y `Setup` admiten hooks `command` y `mcp_tool`. No admiten hooks `http`, `prompt` o `agent`.

### Cómo funcionan los hooks basados en prompts

En lugar de ejecutar un comando Bash, los hooks basados en prompts:

1. Envían la entrada del hook y su prompt a un modelo Claude, Haiku por defecto
2. El LLM responde con JSON estructurado que contiene una decisión
3. Claude Code procesa la decisión automáticamente

### Configuración de hook de prompt

Establezca `type` en `"prompt"` y proporcione una cadena `prompt` en lugar de un `command`. Use el marcador de posición `$ARGUMENTS` para inyectar datos de entrada JSON del hook en su texto de prompt. Claude Code envía el prompt combinado e entrada a un modelo Claude rápido, que devuelve una decisión JSON.

Este hook `Stop` le pide al LLM que evalúe si todas las tareas están completas antes de permitir que Claude finalice:

```json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete."
          }
        ]
      }
    ]
  }
}
```

| Campo     | Requerido | Descripción                                                                                                                                                                          |
| :-------- | :-------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`    | sí        | Debe ser `"prompt"`                                                                                                                                                                  |
| `prompt`  | sí        | El texto del prompt a enviar al LLM. Use `$ARGUMENTS` como marcador de posición para la entrada JSON del hook. Si `$ARGUMENTS` no está presente, la entrada JSON se agrega al prompt |
| `model`   | no        | Modelo a usar para evaluación. Por defecto es un modelo rápido                                                                                                                       |
| `timeout` | no        | Tiempo de espera en segundos. Predeterminado: 30                                                                                                                                     |

### Esquema de respuesta

El LLM debe responder con JSON que contenga:

```json theme={null}
{
  "ok": true | false,
  "reason": "Explanation for the decision"
}
```

| Campo    | Descripción                                                     |
| :------- | :-------------------------------------------------------------- |
| `ok`     | `true` permite la acción, `false` la previene                   |
| `reason` | Requerido cuando `ok` es `false`. Explicación mostrada a Claude |

### Ejemplo: Hook Stop de múltiples criterios

Este hook `Stop` usa un prompt detallado para verificar tres condiciones antes de permitir que Claude se detenga. Si `"ok"` es `false`, Claude continúa trabajando con la razón proporcionada como su siguiente instrucción. Los hooks `SubagentStop` usan el mismo formato para evaluar si un [subagente](/es/sub-agents) debe detenerse:

```json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are evaluating whether Claude should stop working. Context: $ARGUMENTS\n\nAnalyze the conversation and determine if:\n1. All user-requested tasks are complete\n2. Any errors need to be addressed\n3. Follow-up work is needed\n\nRespond with JSON: {\"ok\": true} to allow stopping, or {\"ok\": false, \"reason\": \"your explanation\"} to continue working.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Hooks basados en agentes

<Warning>
  Los hooks de agente son experimentales. El comportamiento y la configuración pueden cambiar en futuras versiones. Para flujos de trabajo de producción, prefiera [command hooks](#command-hook-fields).
</Warning>

Los hooks basados en agentes (`type: "agent"`) son como hooks basados en prompts pero con acceso a herramientas de múltiples turnos. En lugar de una única llamada LLM, un hook de agente genera un subagente que puede leer archivos, buscar código e inspeccionar la base de código para verificar condiciones. Los hooks de agente admiten los mismos eventos que los hooks basados en prompts.

### Cómo funcionan los hooks de agente

Cuando se activa un hook de agente:

1. Claude Code genera un subagente con su prompt y la entrada JSON del hook
2. El subagente puede usar herramientas como Read, Grep y Glob para investigar
3. Después de hasta 50 turnos, el subagente devuelve una decisión estructurada `{ "ok": true/false }`
4. Claude Code procesa la decisión de la misma manera que un hook de prompt

Los hooks de agente son útiles cuando la verificación requiere inspeccionar archivos reales o salida de prueba, no solo evaluar los datos de entrada del hook solos.

### Configuración de hook de agente

Establezca `type` en `"agent"` y proporcione una cadena `prompt`. Los campos de configuración son los mismos que los [hooks de prompt](#prompt-hook-configuration), con un tiempo de espera predeterminado más largo:

| Campo     | Requerido | Descripción                                                                                                 |
| :-------- | :-------- | :---------------------------------------------------------------------------------------------------------- |
| `type`    | sí        | Debe ser `"agent"`                                                                                          |
| `prompt`  | sí        | Prompt que describe qué verificar. Use `$ARGUMENTS` como marcador de posición para la entrada JSON del hook |
| `model`   | no        | Modelo a usar. Por defecto es un modelo rápido                                                              |
| `timeout` | no        | Tiempo de espera en segundos. Predeterminado: 60                                                            |

El esquema de respuesta es el mismo que los hooks de prompt: `{ "ok": true }` para permitir o `{ "ok": false, "reason": "..." }` para bloquear.

Este hook `Stop` verifica que todas las pruebas unitarias pasen antes de permitir que Claude finalice:

```json theme={null}
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

## Ejecutar hooks en segundo plano

Por defecto, los hooks bloquean la ejecución de Claude hasta que se completen. Para tareas de larga duración como implementaciones, conjuntos de pruebas o llamadas a API externas, establezca `"async": true` para ejecutar el hook en segundo plano mientras Claude continúa trabajando. Los hooks asincronos no pueden bloquear o controlar el comportamiento de Claude: campos de respuesta como `decision`, `permissionDecision` y `continue` no tienen efecto, porque la acción que habrían controlado ya se ha completado.

### Configurar un hook asincrónico

Agregue `"async": true` a la configuración de un hook de comando para ejecutarlo en segundo plano sin bloquear a Claude. Este campo solo está disponible en hooks `type: "command"`.

Este hook ejecuta un script de prueba después de cada llamada a herramienta `Write`. Claude continúa trabajando inmediatamente mientras `run-tests.sh` se ejecuta durante hasta 120 segundos. Cuando el script finaliza, su salida se entrega en el siguiente turno de conversación:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/run-tests.sh",
            "async": true,
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

El campo `timeout` establece el tiempo máximo en segundos para el proceso de fondo. Si no se especifica, los hooks asincronos usan el mismo predeterminado de 10 minutos que los hooks sincronos.

### Cómo se ejecutan los hooks asincronos

Cuando se activa un hook asincrónico, Claude Code inicia el proceso del hook e inmediatamente continúa sin esperar a que finalice. El hook recibe la misma entrada JSON a través de stdin que un hook sincrónico.

Después de que el proceso de fondo sale, si el hook produjo una respuesta JSON con un campo `systemMessage` o `additionalContext`, ese contenido se entrega a Claude como contexto en el siguiente turno de conversación.

Las notificaciones de finalización de hooks asincronos se suprimen por defecto. Para verlas, habilite el modo detallado con `Ctrl+O` o inicie Claude Code con `--verbose`.

### Ejemplo: ejecutar pruebas después de cambios de archivo

Este hook inicia un conjunto de pruebas en segundo plano cada vez que Claude escribe un archivo, luego reporta los resultados a Claude cuando las pruebas finalizan. Guarde este script en `.claude/hooks/run-tests-async.sh` en su proyecto y hágalo ejecutable con `chmod +x`:

```bash theme={null}
#!/bin/bash
# run-tests-async.sh

# Lee entrada de hook desde stdin
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Solo ejecute pruebas para archivos de origen
if [[ "$FILE_PATH" != *.ts && "$FILE_PATH" != *.js ]]; then
  exit 0
fi

# Ejecute pruebas e informe resultados a través de systemMessage
RESULT=$(npm test 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "{\"systemMessage\": \"Tests passed after editing $FILE_PATH\"}"
else
  echo "{\"systemMessage\": \"Tests failed after editing $FILE_PATH: $RESULT\"}"
fi
```

Luego agregue esta configuración a `.claude/settings.json` en la raíz de su proyecto. La bandera `async: true` permite que Claude continúe trabajando mientras se ejecutan las pruebas:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/run-tests-async.sh",
            "async": true,
            "timeout": 300
          }
        ]
      }
    ]
  }
}
```

### Limitaciones

Los hooks asincronos tienen varias restricciones en comparación con los hooks sincronos:

* Solo los hooks `type: "command"` admiten `async`. Los hooks basados en prompts no pueden ejecutarse de forma asincrónica.
* Los hooks asincronos no pueden bloquear llamadas a herramientas o devolver decisiones. En el momento en que se completa el hook, la acción desencadenante ya ha procedido.
* La salida del hook se entrega en el siguiente turno de conversación. Si la sesión está inactiva, la respuesta espera hasta la siguiente interacción del usuario. Excepción: un hook `asyncRewake` que sale con código 2 despierta a Claude inmediatamente incluso cuando la sesión está inactiva.
* Cada ejecución crea un proceso de fondo separado. No hay deduplicación en múltiples activaciones del mismo hook asincrónico.

## Consideraciones de seguridad

### Descargo de responsabilidad

Los hooks de comando se ejecutan con los permisos completos del usuario del sistema.

<Warning>
  Los hooks de comando ejecutan comandos de shell con sus permisos de usuario completos. Pueden modificar, eliminar o acceder a cualquier archivo al que su cuenta de usuario pueda acceder. Revise y pruebe todos los comandos de hook antes de agregarlos a su configuración.
</Warning>

### Mejores prácticas de seguridad

Tenga en cuenta estas prácticas al escribir hooks:

* **Validar y desinfectar entradas**: nunca confíe en datos de entrada ciegamente
* **Siempre entrecomillar variables de shell**: use `"$VAR"` no `$VAR`
* **Bloquear traversal de ruta**: verifique `..` en rutas de archivo
* **Usar rutas absolutas**: especifique rutas completas para scripts, usando `"$CLAUDE_PROJECT_DIR"` para la raíz del proyecto
* **Omitir archivos sensibles**: evite `.env`, `.git/`, claves, etc.

## Herramienta PowerShell en Windows

En Windows, puede ejecutar hooks individuales en PowerShell estableciendo `"shell": "powershell"` en un hook de comando. Los hooks generan PowerShell directamente, por lo que esto funciona independientemente de si `CLAUDE_CODE_USE_POWERSHELL_TOOL` está establecido. Claude Code detecta automáticamente `pwsh.exe` (PowerShell 7+) con un respaldo a `powershell.exe` (5.1).

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "shell": "powershell",
            "command": "Write-Host 'File written'"
          }
        ]
      }
    ]
  }
}
```

## Depurar hooks

Los detalles de ejecución de hooks, incluyendo qué hooks coincidieron, sus códigos de salida y stdout y stderr completos, se escriben en el archivo de registro de depuración. Inicie Claude Code con `claude --debug-file <path>` para escribir el registro en una ubicación conocida, o ejecute `claude --debug` y lea el registro en `~/.claude/debug/<session-id>.txt`. La bandera `--debug` no imprime en la terminal.

```text theme={null}
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 600000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

Para detalles de coincidencia de hooks más granulares, establezca `CLAUDE_CODE_DEBUG_LOG_LEVEL=verbose` para ver líneas de registro adicionales como recuentos de matchers de hooks y coincidencia de consultas.

Para solucionar problemas comunes como hooks que no se activan, bucles infinitos de hooks Stop o errores de configuración, consulte [Limitaciones y solución de problemas](/es/hooks-guide#limitations-and-troubleshooting) en la guía. Para un recorrido de diagnóstico más amplio que cubra `/context`, `/doctor` y precedencia de configuración, consulte [Depure su configuración](/es/debug-your-config).
