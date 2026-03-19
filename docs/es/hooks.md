> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Referencia de hooks

> Referencia para eventos de hooks de Claude Code, esquema de configuración, formatos de entrada/salida JSON, códigos de salida, hooks asincronos, hooks HTTP, hooks de prompt y hooks de herramientas MCP.

<Tip>
  Para una guía de inicio rápido con ejemplos, consulte [Automatizar flujos de trabajo con hooks](/es/hooks-guide).
</Tip>

Los hooks son comandos de shell definidos por el usuario, puntos finales HTTP o prompts de LLM que se ejecutan automáticamente en puntos específicos del ciclo de vida de Claude Code. Utilice esta referencia para buscar esquemas de eventos, opciones de configuración, formatos de entrada/salida JSON y características avanzadas como hooks asincronos, hooks HTTP y hooks de herramientas MCP. Si está configurando hooks por primera vez, comience con la [guía](/es/hooks-guide) en su lugar.

## Ciclo de vida del hook

Los hooks se activan en puntos específicos durante una sesión de Claude Code. Cuando se activa un evento y un matcher coincide, Claude Code pasa contexto JSON sobre el evento a su controlador de hook. Para hooks de comando, la entrada llega en stdin. Para hooks HTTP, llega como el cuerpo de la solicitud POST. Su controlador puede entonces inspeccionar la entrada, tomar medidas y opcionalmente devolver una decisión. Algunos eventos se activan una vez por sesión, mientras que otros se activan repetidamente dentro del bucle agentico:

<div style={{maxWidth: "500px", margin: "0 auto"}}>
  <Frame>
    <img src="https://mintcdn.com/claude-code/2YzYcIR7V1VggfgF/images/hooks-lifecycle.svg?fit=max&auto=format&n=2YzYcIR7V1VggfgF&q=85&s=3004e6c5dc95c4fe7fa3eb40fdc4176c" alt="Diagrama del ciclo de vida del hook que muestra la secuencia de hooks desde SessionStart a través del bucle agentico hasta SessionEnd, con WorktreeCreate, WorktreeRemove e InstructionsLoaded como eventos asincronos independientes" width="520" height="1100" data-path="images/hooks-lifecycle.svg" />
  </Frame>
</div>

La tabla a continuación resume cuándo se activa cada evento. La sección [Hook events](#hook-events) documenta el esquema de entrada completo y las opciones de control de decisión para cada uno.

| Event                | When it fires                                                                                                                                  |
| :------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`       | When a session begins or resumes                                                                                                               |
| `UserPromptSubmit`   | When you submit a prompt, before Claude processes it                                                                                           |
| `PreToolUse`         | Before a tool call executes. Can block it                                                                                                      |
| `PermissionRequest`  | When a permission dialog appears                                                                                                               |
| `PostToolUse`        | After a tool call succeeds                                                                                                                     |
| `PostToolUseFailure` | After a tool call fails                                                                                                                        |
| `Notification`       | When Claude Code sends a notification                                                                                                          |
| `SubagentStart`      | When a subagent is spawned                                                                                                                     |
| `SubagentStop`       | When a subagent finishes                                                                                                                       |
| `Stop`               | When Claude finishes responding                                                                                                                |
| `StopFailure`        | When the turn ends due to an API error. Output and exit code are ignored                                                                       |
| `TeammateIdle`       | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                             |
| `TaskCompleted`      | When a task is being marked as completed                                                                                                       |
| `InstructionsLoaded` | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session |
| `ConfigChange`       | When a configuration file changes during a session                                                                                             |
| `WorktreeCreate`     | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                    |
| `WorktreeRemove`     | When a worktree is being removed, either at session exit or when a subagent finishes                                                           |
| `PreCompact`         | Before context compaction                                                                                                                      |
| `PostCompact`        | After context compaction completes                                                                                                             |
| `Elicitation`        | When an MCP server requests user input during a tool call                                                                                      |
| `ElicitationResult`  | After a user responds to an MCP elicitation, before the response is sent back to the server                                                    |
| `SessionEnd`         | When a session terminates                                                                                                                      |

### Cómo se resuelve un hook

Para ver cómo encajan estas piezas, considere este hook `PreToolUse` que bloquea comandos de shell destructivos. El hook ejecuta `block-rm.sh` antes de cada llamada a la herramienta Bash:

```json  theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/block-rm.sh"
          }
        ]
      }
    ]
  }
}
```

El script lee la entrada JSON desde stdin, extrae el comando y devuelve una `permissionDecision` de `"deny"` si contiene `rm -rf`:

```bash  theme={null}
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
  <img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/hook-resolution.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=ad667ee6d86ab2276aa48a4e73e220df" alt="Flujo de resolución de hook: se activa el evento PreToolUse, el matcher verifica la coincidencia de Bash, se ejecuta el controlador de hook, el resultado se devuelve a Claude Code" width="780" height="290" data-path="images/hook-resolution.svg" />
</Frame>

<Steps>
  <Step title="Se activa el evento">
    El evento `PreToolUse` se activa. Claude Code envía la entrada de la herramienta como JSON en stdin al hook:

    ```json  theme={null}
    { "tool_name": "Bash", "tool_input": { "command": "rm -rf /tmp/build" }, ... }
    ```
  </Step>

  <Step title="El matcher verifica">
    El matcher `"Bash"` coincide con el nombre de la herramienta, por lo que se ejecuta `block-rm.sh`. Si omite el matcher o usa `"*"`, el hook se ejecuta en cada ocurrencia del evento. Los hooks solo se omiten cuando se define un matcher y no coincide.
  </Step>

  <Step title="Se ejecuta el controlador de hook">
    El script extrae `"rm -rf /tmp/build"` de la entrada y encuentra `rm -rf`, por lo que imprime una decisión en stdout:

    ```json  theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Destructive command blocked by hook"
      }
    }
    ```

    Si el comando hubiera sido seguro (como `npm test`), el script habría alcanzado `exit 0` en su lugar, lo que le dice a Claude Code que permita la llamada a la herramienta sin más acciones.
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
  Esta página utiliza términos específicos para cada nivel: **hook event** para el punto del ciclo de vida, **matcher group** para el filtro y **hook handler** para el comando de shell, punto final HTTP, prompt o agente que se ejecuta. "Hook" por sí solo se refiere a la característica general.
</Note>

### Ubicaciones de hooks

Dónde define un hook determina su alcance:

| Ubicación                                                 | Alcance                            | Compartible                                |
| :-------------------------------------------------------- | :--------------------------------- | :----------------------------------------- |
| `~/.claude/settings.json`                                 | Todos sus proyectos                | No, local en su máquina                    |
| `.claude/settings.json`                                   | Proyecto único                     | Sí, puede ser confirmado en el repositorio |
| `.claude/settings.local.json`                             | Proyecto único                     | No, ignorado por git                       |
| Configuración de política administrada                    | Toda la organización               | Sí, controlado por administrador           |
| [Plugin](/es/plugins) `hooks/hooks.json`                  | Cuando el plugin está habilitado   | Sí, incluido con el plugin                 |
| [Skill](/es/skills) o [agent](/es/sub-agents) frontmatter | Mientras el componente está activo | Sí, definido en el archivo del componente  |

Para obtener detalles sobre la resolución de archivos de configuración, consulte [settings](/es/settings). Los administradores empresariales pueden usar `allowManagedHooksOnly` para bloquear hooks de usuario, proyecto y plugin. Consulte [Hook configuration](/es/settings#hook-configuration).

### Patrones de matcher

El campo `matcher` es una cadena regex que filtra cuándo se activan los hooks. Use `"*"`, `""` u omita `matcher` completamente para coincidir con todas las ocurrencias. Cada tipo de evento coincide en un campo diferente:

| Evento                                                                                                                | En qué filtra el matcher        | Valores de matcher de ejemplo                                                      |
| :-------------------------------------------------------------------------------------------------------------------- | :------------------------------ | :--------------------------------------------------------------------------------- |
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`                                                | nombre de la herramienta        | `Bash`, `Edit\|Write`, `mcp__.*`                                                   |
| `SessionStart`                                                                                                        | cómo comenzó la sesión          | `startup`, `resume`, `clear`, `compact`                                            |
| `SessionEnd`                                                                                                          | por qué terminó la sesión       | `clear`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`     |
| `Notification`                                                                                                        | tipo de notificación            | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`           |
| `SubagentStart`                                                                                                       | tipo de agente                  | `Bash`, `Explore`, `Plan` o nombres de agentes personalizados                      |
| `PreCompact`                                                                                                          | qué desencadenó la compactación | `manual`, `auto`                                                                   |
| `SubagentStop`                                                                                                        | tipo de agente                  | los mismos valores que `SubagentStart`                                             |
| `ConfigChange`                                                                                                        | fuente de configuración         | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |
| `UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove`, `InstructionsLoaded` | sin soporte de matcher          | siempre se activa en cada ocurrencia                                               |

El matcher es un regex, por lo que `Edit|Write` coincide con cualquiera de las herramientas y `Notebook.*` coincide con cualquier herramienta que comience con Notebook. El matcher se ejecuta contra un campo de la [entrada JSON](#hook-input-and-output) que Claude Code envía a su hook en stdin. Para eventos de herramientas, ese campo es `tool_name`. Cada sección [hook event](#hook-events) enumera el conjunto completo de valores de matcher y el esquema de entrada para ese evento.

Este ejemplo ejecuta un script de linting solo cuando Claude escribe o edita un archivo:

```json  theme={null}
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

`UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` e `InstructionsLoaded` no admiten matchers y siempre se activan en cada ocurrencia. Si agrega un campo `matcher` a estos eventos, se ignora silenciosamente.

#### Coincidir herramientas MCP

Las herramientas del servidor [MCP](/es/mcp) aparecen como herramientas normales en eventos de herramientas (`PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`), por lo que puede hacerlas coincidir de la misma manera que cualquier otro nombre de herramienta.

Las herramientas MCP siguen el patrón de nomenclatura `mcp__<server>__<tool>`, por ejemplo:

* `mcp__memory__create_entities`: herramienta crear entidades del servidor Memory
* `mcp__filesystem__read_file`: herramienta leer archivo del servidor Filesystem
* `mcp__github__search_repositories`: herramienta de búsqueda del servidor GitHub

Use patrones regex para dirigirse a herramientas MCP específicas o grupos de herramientas:

* `mcp__memory__.*` coincide con todas las herramientas del servidor `memory`
* `mcp__.*__write.*` coincide con cualquier herramienta que contenga "write" de cualquier servidor

Este ejemplo registra todas las operaciones del servidor de memoria y valida operaciones de escritura de cualquier servidor MCP:

```json  theme={null}
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

### Campos del controlador de hook

Cada objeto en el array `hooks` interno es un controlador de hook: el comando de shell, punto final HTTP, prompt de LLM o agente que se ejecuta cuando el matcher coincide. Hay cuatro tipos:

* **[Command hooks](#command-hook-fields)** (`type: "command"`): ejecuta un comando de shell. Su script recibe la [entrada JSON](#hook-input-and-output) del evento en stdin y comunica los resultados a través de códigos de salida y stdout.
* **[HTTP hooks](#http-hook-fields)** (`type: "http"`): envía la entrada JSON del evento como una solicitud HTTP POST a una URL. El punto final comunica los resultados a través del cuerpo de la respuesta usando el mismo [formato de salida JSON](#json-output) que los hooks de comando.
* **[Prompt hooks](#prompt-and-agent-hook-fields)** (`type: "prompt"`): envía un prompt a un modelo Claude para evaluación de un solo turno. El modelo devuelve una decisión sí/no como JSON. Consulte [Prompt-based hooks](#prompt-based-hooks).
* **[Agent hooks](#prompt-and-agent-hook-fields)** (`type: "agent"`): genera un subagente que puede usar herramientas como Read, Grep y Glob para verificar condiciones antes de devolver una decisión. Consulte [Agent-based hooks](#agent-based-hooks).

#### Campos comunes

Estos campos se aplican a todos los tipos de hooks:

| Campo           | Requerido | Descripción                                                                                                                                                      |
| :-------------- | :-------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`          | sí        | `"command"`, `"http"`, `"prompt"` o `"agent"`                                                                                                                    |
| `timeout`       | no        | Segundos antes de cancelar. Valores predeterminados: 600 para comando, 30 para prompt, 60 para agente                                                            |
| `statusMessage` | no        | Mensaje de spinner personalizado mostrado mientras se ejecuta el hook                                                                                            |
| `once`          | no        | Si es `true`, se ejecuta solo una vez por sesión y luego se elimina. Solo skills, no agentes. Consulte [Hooks in skills and agents](#hooks-in-skills-and-agents) |

#### Campos de comando hook

Además de los [campos comunes](#common-fields), los hooks de comando aceptan estos campos:

| Campo     | Requerido | Descripción                                                                                                                  |
| :-------- | :-------- | :--------------------------------------------------------------------------------------------------------------------------- |
| `command` | sí        | Comando de shell a ejecutar                                                                                                  |
| `async`   | no        | Si es `true`, se ejecuta en segundo plano sin bloquear. Consulte [Run hooks in the background](#run-hooks-in-the-background) |

#### Campos de hook HTTP

Además de los [campos comunes](#common-fields), los hooks HTTP aceptan estos campos:

| Campo            | Requerido | Descripción                                                                                                                                                                                                                                       |
| :--------------- | :-------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `url`            | sí        | URL a la que enviar la solicitud POST                                                                                                                                                                                                             |
| `headers`        | no        | Encabezados HTTP adicionales como pares clave-valor. Los valores admiten interpolación de variables de entorno usando la sintaxis `$VAR_NAME` o `${VAR_NAME}`. Solo se resuelven las variables enumeradas en `allowedEnvVars`                     |
| `allowedEnvVars` | no        | Lista de nombres de variables de entorno que pueden interpolarse en valores de encabezado. Las referencias a variables no enumeradas se reemplazan con cadenas vacías. Requerido para que funcione cualquier interpolación de variable de entorno |

Claude Code envía la [entrada JSON](#hook-input-and-output) del hook como el cuerpo de la solicitud POST con `Content-Type: application/json`. El cuerpo de la respuesta usa el mismo [formato de salida JSON](#json-output) que los hooks de comando.

El manejo de errores difiere de los hooks de comando: las respuestas que no son 2xx, los fallos de conexión y los tiempos de espera agotados producen errores que no bloquean y permiten que la ejecución continúe. Para bloquear una llamada a herramienta o denegar un permiso, devuelva una respuesta 2xx con un cuerpo JSON que contenga `decision: "block"` o un `hookSpecificOutput` con `permissionDecision: "deny"`.

Este ejemplo envía eventos `PreToolUse` a un servicio de validación local, autenticándose con un token de la variable de entorno `MY_TOKEN`:

```json  theme={null}
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

<Note>
  Los hooks HTTP deben configurarse editando JSON de configuración directamente. El menú interactivo `/hooks` solo admite agregar hooks de comando.
</Note>

#### Campos de hook de prompt y agente

Además de los [campos comunes](#common-fields), los hooks de prompt y agente aceptan estos campos:

| Campo    | Requerido | Descripción                                                                                                   |
| :------- | :-------- | :------------------------------------------------------------------------------------------------------------ |
| `prompt` | sí        | Texto del prompt a enviar al modelo. Use `$ARGUMENTS` como marcador de posición para la entrada JSON del hook |
| `model`  | no        | Modelo a usar para evaluación. Por defecto es un modelo rápido                                                |

Todos los hooks coincidentes se ejecutan en paralelo, y los controladores idénticos se deduplicarán automáticamente. Los hooks de comando se deduplicarán por cadena de comando, y los hooks HTTP se deduplicarán por URL. Los controladores se ejecutan en el directorio actual con el entorno de Claude Code. La variable de entorno `$CLAUDE_CODE_REMOTE` se establece en `"true"` en entornos web remotos y no se establece en la CLI local.

### Referenciar scripts por ruta

Use variables de entorno para referenciar scripts de hook relativos a la raíz del proyecto o plugin, independientemente del directorio de trabajo cuando se ejecuta el hook:

* `$CLAUDE_PROJECT_DIR`: la raíz del proyecto. Envuelva entre comillas para manejar rutas con espacios.
* `${CLAUDE_PLUGIN_ROOT}`: el directorio raíz del plugin, para scripts incluidos con un [plugin](/es/plugins).

<Tabs>
  <Tab title="Scripts de proyecto">
    Este ejemplo usa `$CLAUDE_PROJECT_DIR` para ejecutar un verificador de estilo desde el directorio `.claude/hooks/` del proyecto después de cualquier llamada a herramienta `Write` o `Edit`:

    ```json  theme={null}
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

    ```json  theme={null}
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

Además de archivos de configuración y plugins, los hooks pueden definirse directamente en [skills](/es/skills) y [subagentes](/es/sub-agents) usando frontmatter. Estos hooks están limitados al ciclo de vida del componente y solo se ejecutan cuando ese componente está activo.

Se admiten todos los eventos de hook. Para subagentes, los hooks `Stop` se convierten automáticamente a `SubagentStop` ya que ese es el evento que se activa cuando un subagente se completa.

Los hooks usan el mismo formato de configuración que los hooks basados en configuración pero están limitados a la vida útil del componente y se limpian cuando finaliza.

Esta skill define un hook `PreToolUse` que ejecuta un script de validación de seguridad antes de cada comando `Bash`:

```yaml  theme={null}
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

Escriba `/hooks` en Claude Code para abrir el administrador de hooks interactivo, donde puede ver, agregar y eliminar hooks sin editar archivos de configuración directamente. Para un recorrido paso a paso, consulte [Set up your first hook](/es/hooks-guide#set-up-your-first-hook) en la guía.

Cada hook en el menú está etiquetado con un prefijo de corchete que indica su fuente:

* `[User]`: de `~/.claude/settings.json`
* `[Project]`: de `.claude/settings.json`
* `[Local]`: de `.claude/settings.local.json`
* `[Plugin]`: de `hooks/hooks.json` de un plugin, solo lectura

### Deshabilitar o eliminar hooks

Para eliminar un hook, elimine su entrada del archivo de configuración JSON o use el menú `/hooks` y seleccione el hook para eliminarlo.

Para deshabilitar temporalmente todos los hooks sin eliminarlos, establezca `"disableAllHooks": true` en su archivo de configuración o use el botón de alternancia en el menú `/hooks`. No hay forma de deshabilitar un hook individual mientras se mantiene en la configuración.

La configuración `disableAllHooks` respeta la jerarquía de configuración administrada. Si un administrador ha configurado hooks a través de configuración de política administrada, `disableAllHooks` establecido en configuración de usuario, proyecto o local no puede deshabilitar esos hooks administrados. Solo `disableAllHooks` establecido en el nivel de configuración administrada puede deshabilitar hooks administrados.

Las ediciones directas de hooks en archivos de configuración no tienen efecto inmediato. Claude Code captura una instantánea de hooks al inicio y la usa durante toda la sesión. Esto evita que modificaciones de hooks maliciosas o accidentales tengan efecto a mitad de sesión sin su revisión. Si los hooks se modifican externamente, Claude Code le advierte y requiere revisión en el menú `/hooks` antes de que los cambios se apliquen.

## Entrada y salida de hook

Los hooks de comando reciben datos JSON a través de stdin y comunican resultados a través de códigos de salida, stdout y stderr. Los hooks HTTP reciben el mismo JSON que el cuerpo de la solicitud POST y comunican resultados a través del cuerpo de la respuesta HTTP. Esta sección cubre campos y comportamiento comunes a todos los eventos. Cada sección de evento bajo [Hook events](#hook-events) incluye su esquema de entrada específico y opciones de control de decisión.

### Campos de entrada comunes

Todos los eventos de hook reciben estos campos como JSON, además de campos específicos del evento documentados en cada sección [hook event](#hook-events). Para hooks de comando, este JSON llega a través de stdin. Para hooks HTTP, llega como el cuerpo de la solicitud POST.

| Campo             | Descripción                                                                                                                             |
| :---------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| `session_id`      | Identificador de sesión actual                                                                                                          |
| `transcript_path` | Ruta al JSON de conversación                                                                                                            |
| `cwd`             | Directorio de trabajo actual cuando se invoca el hook                                                                                   |
| `permission_mode` | [Modo de permiso](/es/permissions#permission-modes) actual: `"default"`, `"plan"`, `"acceptEdits"`, `"dontAsk"` o `"bypassPermissions"` |
| `hook_event_name` | Nombre del evento que se activó                                                                                                         |

Cuando se ejecuta con `--agent` o dentro de un subagente, se incluyen dos campos adicionales:

| Campo        | Descripción                                                                                                                                                                                                                                               |
| :----------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agent_id`   | Identificador único para el subagente. Presente solo cuando el hook se activa dentro de una llamada de subagente. Úselo para distinguir llamadas de hook de subagente de llamadas de hilo principal.                                                      |
| `agent_type` | Nombre del agente (por ejemplo, `"Explore"` o `"security-reviewer"`). Presente cuando la sesión usa `--agent` o el hook se activa dentro de un subagente. Para subagentes, el tipo del subagente tiene precedencia sobre el valor `--agent` de la sesión. |

Por ejemplo, un hook `PreToolUse` para un comando Bash recibe esto en stdin:

```json  theme={null}
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

**Exit 0** significa éxito. Claude Code analiza stdout para [campos de salida JSON](#json-output). La salida JSON solo se procesa en exit 0. Para la mayoría de eventos, stdout solo se muestra en modo detallado (`Ctrl+O`). Las excepciones son `UserPromptSubmit` y `SessionStart`, donde stdout se agrega como contexto que Claude puede ver y actuar.

**Exit 2** significa un error de bloqueo. Claude Code ignora stdout y cualquier JSON en él. En su lugar, el texto de stderr se devuelve a Claude como un mensaje de error. El efecto depende del evento: `PreToolUse` bloquea la llamada a herramienta, `UserPromptSubmit` rechaza el prompt, y así sucesivamente. Consulte [exit code 2 behavior](#exit-code-2-behavior-per-event) para la lista completa.

**Cualquier otro código de salida** es un error que no bloquea. stderr se muestra en modo detallado (`Ctrl+O`) y la ejecución continúa.

Por ejemplo, un script de comando de hook que bloquea comandos Bash peligrosos:

```bash  theme={null}
#!/bin/bash
# Lee la entrada JSON desde stdin, verifica el comando
command=$(jq -r '.tool_input.command' < /dev/stdin)

if [[ "$command" == rm* ]]; then
  echo "Blocked: rm commands are not allowed" >&2
  exit 2  # Blocking error: tool call is prevented
fi

exit 0  # Success: tool call proceeds
```

#### Comportamiento del código de salida 2 por evento

El código de salida 2 es la forma en que un hook señala "detente, no hagas esto". El efecto depende del evento, porque algunos eventos representan acciones que pueden bloquearse (como una llamada a herramienta que aún no ha sucedido) y otros representan cosas que ya sucedieron o no pueden prevenirse.

| Evento de hook       | ¿Puede bloquear? | Qué sucede en exit 2                                                                |
| :------------------- | :--------------- | :---------------------------------------------------------------------------------- |
| `PreToolUse`         | Sí               | Bloquea la llamada a herramienta                                                    |
| `PermissionRequest`  | Sí               | Deniega el permiso                                                                  |
| `UserPromptSubmit`   | Sí               | Bloquea el procesamiento del prompt y borra el prompt                               |
| `Stop`               | Sí               | Evita que Claude se detenga, continúa la conversación                               |
| `SubagentStop`       | Sí               | Evita que el subagente se detenga                                                   |
| `TeammateIdle`       | Sí               | Evita que el compañero se quede inactivo (el compañero continúa trabajando)         |
| `TaskCompleted`      | Sí               | Evita que la tarea se marque como completada                                        |
| `ConfigChange`       | Sí               | Bloquea que el cambio de configuración tenga efecto (excepto `policy_settings`)     |
| `PostToolUse`        | No               | Muestra stderr a Claude (la herramienta ya se ejecutó)                              |
| `PostToolUseFailure` | No               | Muestra stderr a Claude (la herramienta ya falló)                                   |
| `Notification`       | No               | Muestra stderr solo al usuario                                                      |
| `SubagentStart`      | No               | Muestra stderr solo al usuario                                                      |
| `SessionStart`       | No               | Muestra stderr solo al usuario                                                      |
| `SessionEnd`         | No               | Muestra stderr solo al usuario                                                      |
| `PreCompact`         | No               | Muestra stderr solo al usuario                                                      |
| `WorktreeCreate`     | Sí               | Cualquier código de salida distinto de cero causa que la creación de worktree falle |
| `WorktreeRemove`     | No               | Los fallos se registran solo en modo de depuración                                  |
| `InstructionsLoaded` | No               | El código de salida se ignora                                                       |

### Manejo de respuesta HTTP

Los hooks HTTP usan códigos de estado HTTP y cuerpos de respuesta en lugar de códigos de salida y stdout:

* **2xx con un cuerpo vacío**: éxito, equivalente a código de salida 0 sin salida
* **2xx con un cuerpo de texto plano**: éxito, el texto se agrega como contexto
* **2xx con un cuerpo JSON**: éxito, analizado usando el mismo esquema [JSON output](#json-output) que los hooks de comando
* **Estado que no es 2xx**: error que no bloquea, la ejecución continúa
* **Fallo de conexión o tiempo de espera agotado**: error que no bloquea, la ejecución continúa

A diferencia de los hooks de comando, los hooks HTTP no pueden señalar un error de bloqueo solo a través de códigos de estado. Para bloquear una llamada a herramienta o denegar un permiso, devuelva una respuesta 2xx con un cuerpo JSON que contenga los campos de decisión apropiados.

### Salida JSON

Los códigos de salida le permiten permitir o bloquear, pero la salida JSON le da un control más granular. En lugar de salir con código 2 para bloquear, salga 0 e imprima un objeto JSON en stdout. Claude Code lee campos específicos de ese JSON para controlar el comportamiento, incluido [decision control](#decision-control) para bloquear, permitir o escalar al usuario.

<Note>
  Debe elegir un enfoque por hook, no ambos: use códigos de salida solos para señalización, o salga 0 e imprima JSON para control estructurado. Claude Code solo procesa JSON en exit 0. Si sale 2, cualquier JSON se ignora.
</Note>

El stdout de su hook debe contener solo el objeto JSON. Si su perfil de shell imprime texto al inicio, puede interferir con el análisis JSON. Consulte [JSON validation failed](/es/hooks-guide#json-validation-failed) en la guía de solución de problemas.

El objeto JSON admite tres tipos de campos:

* **Campos universales** como `continue` funcionan en todos los eventos. Estos se enumeran en la tabla a continuación.
* **`decision` y `reason` de nivel superior** son utilizados por algunos eventos para bloquear o proporcionar retroalimentación.
* **`hookSpecificOutput`** es un objeto anidado para eventos que necesitan control más rico. Requiere un campo `hookEventName` establecido en el nombre del evento.

| Campo            | Predeterminado | Descripción                                                                                                                                                               |
| :--------------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `continue`       | `true`         | Si es `false`, Claude detiene el procesamiento completamente después de que se ejecuta el hook. Tiene precedencia sobre cualquier campo de decisión específico del evento |
| `stopReason`     | ninguno        | Mensaje mostrado al usuario cuando `continue` es `false`. No se muestra a Claude                                                                                          |
| `suppressOutput` | `false`        | Si es `true`, oculta stdout de la salida del modo detallado                                                                                                               |
| `systemMessage`  | ninguno        | Mensaje de advertencia mostrado al usuario                                                                                                                                |

Para detener Claude completamente independientemente del tipo de evento:

```json  theme={null}
{ "continue": false, "stopReason": "Build failed, fix errors before continuing" }
```

#### Control de decisión

No todos los eventos admiten bloqueo o control de comportamiento a través de JSON. Los eventos que lo hacen cada uno usan un conjunto diferente de campos para expresar esa decisión. Use esta tabla como referencia rápida antes de escribir un hook:

| Eventos                                                                             | Patrón de decisión                   | Campos clave                                                                                                                                                                                                            |
| :---------------------------------------------------------------------------------- | :----------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| UserPromptSubmit, PostToolUse, PostToolUseFailure, Stop, SubagentStop, ConfigChange | `decision` de nivel superior         | `decision: "block"`, `reason`                                                                                                                                                                                           |
| TeammateIdle, TaskCompleted                                                         | Código de salida o `continue: false` | El código de salida 2 bloquea la acción con retroalimentación de stderr. JSON `{"continue": false, "stopReason": "..."}` también detiene al compañero completamente, coincidiendo con el comportamiento del hook `Stop` |
| PreToolUse                                                                          | `hookSpecificOutput`                 | `permissionDecision` (allow/deny/ask), `permissionDecisionReason`                                                                                                                                                       |
| PermissionRequest                                                                   | `hookSpecificOutput`                 | `decision.behavior` (allow/deny)                                                                                                                                                                                        |
| WorktreeCreate                                                                      | ruta stdout                          | El hook imprime la ruta absoluta del worktree creado. La salida que no es cero falla la creación                                                                                                                        |
| WorktreeRemove, Notification, SessionEnd, PreCompact, InstructionsLoaded            | Ninguno                              | Sin control de decisión. Se usa para efectos secundarios como registro o limpieza                                                                                                                                       |

Aquí hay ejemplos de cada patrón en acción:

<Tabs>
  <Tab title="Decisión de nivel superior">
    Utilizado por `UserPromptSubmit`, `PostToolUse`, `PostToolUseFailure`, `Stop`, `SubagentStop` y `ConfigChange`. El único valor es `"block"`. Para permitir que la acción continúe, omita `decision` de su JSON, o salga 0 sin ningún JSON en absoluto:

    ```json  theme={null}
    {
      "decision": "block",
      "reason": "Test suite must pass before proceeding"
    }
    ```
  </Tab>

  <Tab title="PreToolUse">
    Usa `hookSpecificOutput` para control más rico: permitir, denegar o escalar al usuario. También puede modificar la entrada de la herramienta antes de que se ejecute o inyectar contexto adicional para Claude. Consulte [PreToolUse decision control](#pretooluse-decision-control) para el conjunto completo de opciones.

    ```json  theme={null}
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

    ```json  theme={null}
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

Para ejemplos extendidos incluyendo validación de comandos Bash, filtrado de prompts y scripts de aprobación automática, consulte [What you can automate](/es/hooks-guide#what-you-can-automate) en la guía y la [Bash command validator reference implementation](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py).

## Eventos de hook

Cada evento corresponde a un punto en el ciclo de vida de Claude Code donde los hooks pueden ejecutarse. Las secciones a continuación están ordenadas para coincidir con el ciclo de vida: desde la configuración de sesión a través del bucle agentico hasta el final de la sesión. Cada sección describe cuándo se activa el evento, qué matchers admite, la entrada JSON que recibe y cómo controlar el comportamiento a través de la salida.

### SessionStart

Se ejecuta cuando Claude Code inicia una nueva sesión o reanuda una sesión existente. Útil para cargar contexto de desarrollo como problemas existentes o cambios recientes en su base de código, o configurar variables de entorno. Para contexto estático que no requiere un script, use [CLAUDE.md](/es/memory) en su lugar.

SessionStart se ejecuta en cada sesión, así que mantenga estos hooks rápidos. Solo se admiten hooks `type: "command"`.

El valor del matcher corresponde a cómo se inició la sesión:

| Matcher   | Cuándo se activa                     |
| :-------- | :----------------------------------- |
| `startup` | Nueva sesión                         |
| `resume`  | `--resume`, `--continue` o `/resume` |
| `clear`   | `/clear`                             |
| `compact` | Compactación automática o manual     |

#### Entrada de SessionStart

Además de los [campos de entrada comunes](#common-input-fields), los hooks SessionStart reciben `source`, `model` y opcionalmente `agent_type`. El campo `source` indica cómo comenzó la sesión: `"startup"` para nuevas sesiones, `"resume"` para sesiones reanudadas, `"clear"` después de `/clear` o `"compact"` después de compactación. El campo `model` contiene el identificador del modelo. Si inicia Claude Code con `claude --agent <name>`, un campo `agent_type` contiene el nombre del agente.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SessionStart",
  "source": "startup",
  "model": "claude-sonnet-4-6"
}
```

#### Control de decisión de SessionStart

Cualquier texto que su script de hook imprima en stdout se agrega como contexto para Claude. Además de los [campos de salida JSON](#json-output) disponibles para todos los hooks, puede devolver estos campos específicos del evento:

| Campo               | Descripción                                                                         |
| :------------------ | :---------------------------------------------------------------------------------- |
| `additionalContext` | Cadena agregada al contexto de Claude. Los valores de múltiples hooks se concatenan |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "My additional context here"
  }
}
```

#### Persistir variables de entorno

Los hooks SessionStart tienen acceso a la variable de entorno `CLAUDE_ENV_FILE`, que proporciona una ruta de archivo donde puede persistir variables de entorno para comandos Bash posteriores.

Para establecer variables de entorno individuales, escriba declaraciones `export` en `CLAUDE_ENV_FILE`. Use append (`>>`) para preservar variables establecidas por otros hooks:

```bash  theme={null}
#!/bin/bash

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG_LOG=true' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

Para capturar todos los cambios de entorno de comandos de configuración, compare las variables exportadas antes y después:

```bash  theme={null}
#!/bin/bash

ENV_BEFORE=$(export -p | sort)

# Run your setup commands that modify the environment
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
  `CLAUDE_ENV_FILE` está disponible para hooks SessionStart. Otros tipos de hooks no tienen acceso a esta variable.
</Note>

### InstructionsLoaded

Se activa cuando se carga un archivo `CLAUDE.md` o `.claude/rules/*.md` en contexto. Este evento se activa al inicio de la sesión para archivos cargados con entusiasmo y nuevamente más tarde cuando se cargan archivos de forma perezosa, por ejemplo cuando Claude accede a un subdirectorio que contiene un `CLAUDE.md` anidado o cuando reglas condicionales con frontmatter `paths:` coinciden. El hook no admite bloqueo o control de decisión. Se ejecuta de forma asincrónica con fines de observabilidad.

InstructionsLoaded no admite matchers y se activa en cada ocurrencia de carga.

#### Entrada de InstructionsLoaded

Además de los [campos de entrada comunes](#common-input-fields), los hooks InstructionsLoaded reciben estos campos:

| Campo               | Descripción                                                                                                            |
| :------------------ | :--------------------------------------------------------------------------------------------------------------------- |
| `file_path`         | Ruta absoluta al archivo de instrucciones que se cargó                                                                 |
| `memory_type`       | Alcance del archivo: `"User"`, `"Project"`, `"Local"` o `"Managed"`                                                    |
| `load_reason`       | Por qué se cargó el archivo: `"session_start"`, `"nested_traversal"`, `"path_glob_match"` o `"include"`                |
| `globs`             | Patrones de glob de ruta del frontmatter `paths:` del archivo, si los hay. Presente solo para cargas `path_glob_match` |
| `trigger_file_path` | Ruta al archivo cuyo acceso desencadenó esta carga, para cargas perezosas                                              |
| `parent_file_path`  | Ruta al archivo de instrucciones padre que incluyó este, para cargas `include`                                         |

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "permission_mode": "default",
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

```json  theme={null}
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

| Campo               | Descripción                                                                                                  |
| :------------------ | :----------------------------------------------------------------------------------------------------------- |
| `decision`          | `"block"` evita que el prompt se procese y lo borra del contexto. Omita para permitir que el prompt continúe |
| `reason`            | Se muestra al usuario cuando `decision` es `"block"`. No se agrega al contexto                               |
| `additionalContext` | Cadena agregada al contexto de Claude                                                                        |

```json  theme={null}
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here"
  }
}
```

<Note>
  El formato JSON no es necesario para casos simples. Para agregar contexto, puede imprimir texto plano en stdout con código de salida 0. Use JSON cuando necesite bloquear prompts o desee un control más estructurado.
</Note>

### PreToolUse

Se ejecuta después de que Claude crea parámetros de herramienta y antes de procesar la llamada a herramienta. Coincide en el nombre de la herramienta: `Bash`, `Edit`, `Write`, `Read`, `Glob`, `Grep`, `Agent`, `WebFetch`, `WebSearch` y cualquier [nombre de herramienta MCP](#match-mcp-tools).

Use [PreToolUse decision control](#pretooluse-decision-control) para permitir, denegar o pedir permiso para usar la herramienta.

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

#### Control de decisión de PreToolUse

Los hooks `PreToolUse` pueden controlar si una llamada a herramienta continúa. A diferencia de otros hooks que usan un campo `decision` de nivel superior, PreToolUse devuelve su decisión dentro de un objeto `hookSpecificOutput`. Esto le da control más rico: tres resultados (permitir, denegar o preguntar) más la capacidad de modificar la entrada de la herramienta antes de la ejecución.

| Campo                      | Descripción                                                                                                                                                                           |
| :------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `permissionDecision`       | `"allow"` omite el sistema de permisos, `"deny"` evita la llamada a herramienta, `"ask"` solicita al usuario que confirme                                                             |
| `permissionDecisionReason` | Para `"allow"` y `"ask"`, se muestra al usuario pero no a Claude. Para `"deny"`, se muestra a Claude                                                                                  |
| `updatedInput`             | Modifica los parámetros de entrada de la herramienta antes de la ejecución. Combine con `"allow"` para aprobación automática, o `"ask"` para mostrar la entrada modificada al usuario |
| `additionalContext`        | Cadena agregada al contexto de Claude antes de que se ejecute la herramienta                                                                                                          |

```json  theme={null}
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

<Note>
  PreToolUse anteriormente usaba campos `decision` y `reason` de nivel superior, pero estos están deprecados para este evento. Use `hookSpecificOutput.permissionDecision` y `hookSpecificOutput.permissionDecisionReason` en su lugar. Los valores deprecados `"approve"` y `"block"` se asignan a `"allow"` y `"deny"` respectivamente. Otros eventos como PostToolUse y Stop continúan usando `decision` y `reason` de nivel superior como su formato actual.
</Note>

### PermissionRequest

Se ejecuta cuando se muestra un diálogo de permiso al usuario.
Use [PermissionRequest decision control](#permissionrequest-decision-control) para permitir o denegar en nombre del usuario.

Coincide en el nombre de la herramienta, los mismos valores que PreToolUse.

#### Entrada de PermissionRequest

Los hooks PermissionRequest reciben campos `tool_name` y `tool_input` como los hooks PreToolUse, pero sin `tool_use_id`. Un array `permission_suggestions` opcional contiene las opciones "siempre permitir" que el usuario normalmente vería en el diálogo de permiso. La diferencia es cuándo se activa el hook: los hooks PermissionRequest se ejecutan cuando un diálogo de permiso está a punto de mostrarse al usuario, mientras que los hooks PreToolUse se ejecutan antes de la ejecución de la herramienta independientemente del estado de permiso.

```json  theme={null}
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
    { "type": "toolAlwaysAllow", "tool": "Bash" }
  ]
}
```

#### Control de decisión de PermissionRequest

Los hooks `PermissionRequest` pueden permitir o denegar solicitudes de permiso. Además de los [campos de salida JSON](#json-output) disponibles para todos los hooks, su script de hook puede devolver un objeto `decision` con estos campos específicos del evento:

| Campo                | Descripción                                                                                                                             |
| :------------------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| `behavior`           | `"allow"` otorga el permiso, `"deny"` lo deniega                                                                                        |
| `updatedInput`       | Solo para `"allow"`: modifica los parámetros de entrada de la herramienta antes de la ejecución                                         |
| `updatedPermissions` | Solo para `"allow"`: aplica actualizaciones de reglas de permiso, equivalente a que el usuario seleccione una opción "siempre permitir" |
| `message`            | Solo para `"deny"`: le dice a Claude por qué se denegó el permiso                                                                       |
| `interrupt`          | Solo para `"deny"`: si es `true`, detiene a Claude                                                                                      |

```json  theme={null}
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

### PostToolUse

Se ejecuta inmediatamente después de que una herramienta se completa exitosamente.

Coincide en el nombre de la herramienta, los mismos valores que PreToolUse.

#### Entrada de PostToolUse

Los hooks `PostToolUse` se activan después de que una herramienta ya se ha ejecutado exitosamente. La entrada incluye tanto `tool_input`, los argumentos enviados a la herramienta, como `tool_response`, el resultado que devolvió. El esquema exacto para ambos depende de la herramienta.

```json  theme={null}
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
  "tool_use_id": "toolu_01ABC123..."
}
```

#### Control de decisión de PostToolUse

Los hooks `PostToolUse` pueden proporcionar retroalimentación a Claude después de la ejecución de la herramienta. Además de los [campos de salida JSON](#json-output) disponibles para todos los hooks, su script de hook puede devolver estos campos específicos del evento:

| Campo                  | Descripción                                                                                                      |
| :--------------------- | :--------------------------------------------------------------------------------------------------------------- |
| `decision`             | `"block"` solicita a Claude con la `reason`. Omita para permitir que la acción continúe                          |
| `reason`               | Explicación mostrada a Claude cuando `decision` es `"block"`                                                     |
| `additionalContext`    | Contexto adicional para que Claude considere                                                                     |
| `updatedMCPToolOutput` | Solo para [herramientas MCP](#match-mcp-tools): reemplaza la salida de la herramienta con el valor proporcionado |

```json  theme={null}
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude"
  }
}
```

### PostToolUseFailure

Se ejecuta cuando falla la ejecución de una herramienta. Este evento se activa para llamadas a herramientas que lanzan errores o devuelven resultados de fallo. Úselo para registrar fallos, enviar alertas o proporcionar retroalimentación correctiva a Claude.

Coincide en el nombre de la herramienta, los mismos valores que PreToolUse.

#### Entrada de PostToolUseFailure

Los hooks PostToolUseFailure reciben los mismos campos `tool_name` y `tool_input` que PostToolUse, junto con información de error como campos de nivel superior:

```json  theme={null}
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
  "is_interrupt": false
}
```

| Campo          | Descripción                                                                       |
| :------------- | :-------------------------------------------------------------------------------- |
| `error`        | Cadena que describe qué salió mal                                                 |
| `is_interrupt` | Booleano opcional que indica si el fallo fue causado por interrupción del usuario |

#### Control de decisión de PostToolUseFailure

Los hooks `PostToolUseFailure` pueden proporcionar contexto a Claude después de un fallo de herramienta. Además de los [campos de salida JSON](#json-output) disponibles para todos los hooks, su script de hook puede devolver estos campos específicos del evento:

| Campo               | Descripción                                                     |
| :------------------ | :-------------------------------------------------------------- |
| `additionalContext` | Contexto adicional para que Claude considere junto con el error |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUseFailure",
    "additionalContext": "Additional information about the failure for Claude"
  }
}
```

### Notification

Se ejecuta cuando Claude Code envía notificaciones. Coincide en el tipo de notificación: `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`. Omita el matcher para ejecutar hooks para todos los tipos de notificación.

Use matchers separados para ejecutar diferentes controladores dependiendo del tipo de notificación. Esta configuración desencadena un script de alerta específico de permiso cuando Claude necesita aprobación de permiso y una notificación diferente cuando Claude ha estado inactivo:

```json  theme={null}
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

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Notification",
  "message": "Claude needs your permission to use Bash",
  "title": "Permission needed",
  "notification_type": "permission_prompt"
}
```

Los hooks Notification no pueden bloquear o modificar notificaciones. Además de los [campos de salida JSON](#json-output) disponibles para todos los hooks, puede devolver `additionalContext` para agregar contexto a la conversación:

| Campo               | Descripción                           |
| :------------------ | :------------------------------------ |
| `additionalContext` | Cadena agregada al contexto de Claude |

### SubagentStart

Se ejecuta cuando se genera un subagente de Claude Code a través de la herramienta Agent. Admite matchers para filtrar por nombre de tipo de agente (agentes integrados como `Bash`, `Explore`, `Plan` o nombres de agentes personalizados de `.claude/agents/`).

#### Entrada de SubagentStart

Además de los [campos de entrada comunes](#common-input-fields), los hooks SubagentStart reciben `agent_id` con el identificador único para el subagente y `agent_type` con el nombre del agente (agentes integrados como `"Bash"`, `"Explore"`, `"Plan"` o nombres de agentes personalizados).

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SubagentStart",
  "agent_id": "agent-abc123",
  "agent_type": "Explore"
}
```

Los hooks SubagentStart no pueden bloquear la creación de subagentes, pero pueden inyectar contexto en el subagente. Además de los [campos de salida JSON](#json-output) disponibles para todos los hooks, puede devolver:

| Campo               | Descripción                               |
| :------------------ | :---------------------------------------- |
| `additionalContext` | Cadena agregada al contexto del subagente |

```json  theme={null}
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

Además de los [campos de entrada comunes](#common-input-fields), los hooks SubagentStop reciben `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path` y `last_assistant_message`. El campo `agent_type` es el valor utilizado para filtrado de matcher. El `transcript_path` es la transcripción de la sesión principal, mientras que `agent_transcript_path` es la propia transcripción del subagente almacenada en una carpeta `subagents/` anidada. El campo `last_assistant_message` contiene el contenido de texto de la respuesta final del subagente, por lo que los hooks pueden acceder a él sin analizar el archivo de transcripción.

```json  theme={null}
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

### Stop

Se ejecuta cuando el agente principal de Claude Code ha terminado de responder. No se ejecuta si la detención ocurrió debido a una interrupción del usuario.

#### Entrada de Stop

Además de los [campos de entrada comunes](#common-input-fields), los hooks Stop reciben `stop_hook_active` y `last_assistant_message`. El campo `stop_hook_active` es `true` cuando Claude Code ya está continuando como resultado de un hook de parada. Verifique este valor o procese la transcripción para evitar que Claude Code se ejecute indefinidamente. El campo `last_assistant_message` contiene el contenido de texto de la respuesta final de Claude, por lo que los hooks pueden acceder a él sin analizar el archivo de transcripción.

```json  theme={null}
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

```json  theme={null}
{
  "decision": "block",
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

### TeammateIdle

Se ejecuta cuando un compañero de [equipo de agentes](/es/agent-teams) está a punto de quedarse inactivo después de terminar su turno. Úselo para aplicar puertas de calidad antes de que un compañero deje de trabajar, como requerir que pasen verificaciones de lint o verificar que existan archivos de salida.

Cuando un hook `TeammateIdle` sale con código 2, el compañero recibe el mensaje de stderr como retroalimentación y continúa trabajando en lugar de quedarse inactivo. Para detener al compañero completamente en lugar de re-ejecutarlo, devuelva JSON con `{"continue": false, "stopReason": "..."}`. Los hooks TeammateIdle no admiten matchers y se activan en cada ocurrencia.

#### Entrada de TeammateIdle

Además de los [campos de entrada comunes](#common-input-fields), los hooks TeammateIdle reciben `teammate_name` y `team_name`.

```json  theme={null}
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

```bash  theme={null}
#!/bin/bash

if [ ! -f "./dist/output.js" ]; then
  echo "Build artifact missing. Run the build before stopping." >&2
  exit 2
fi

exit 0
```

### TaskCompleted

Se ejecuta cuando una tarea está siendo marcada como completada. Esto se activa en dos situaciones: cuando cualquier agente marca explícitamente una tarea como completada a través de la herramienta TaskUpdate, o cuando un compañero de [equipo de agentes](/es/agent-teams) termina su turno con tareas en progreso. Úselo para aplicar criterios de finalización como pasar pruebas o verificaciones de lint antes de que una tarea pueda cerrarse.

Cuando un hook `TaskCompleted` sale con código 2, la tarea no se marca como completada y el mensaje de stderr se devuelve al modelo como retroalimentación. Para detener al compañero completamente en lugar de re-ejecutarlo, devuelva JSON con `{"continue": false, "stopReason": "..."}`. Los hooks TaskCompleted no admiten matchers y se activan en cada ocurrencia.

#### Entrada de TaskCompleted

Además de los [campos de entrada comunes](#common-input-fields), los hooks TaskCompleted reciben `task_id`, `task_subject` y opcionalmente `task_description`, `teammate_name` y `team_name`.

```json  theme={null}
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

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

# Run the test suite
if ! npm test 2>&1; then
  echo "Tests not passing. Fix failing tests before completing: $TASK_SUBJECT" >&2
  exit 2
fi

exit 0
```

### ConfigChange

Se ejecuta cuando un archivo de configuración cambia durante una sesión. Úselo para auditar cambios de configuración, aplicar políticas de seguridad o bloquear modificaciones no autorizadas a archivos de configuración.

Los hooks ConfigChange se activan para cambios en archivos de configuración, configuración de política administrada y archivos de skill. El campo `source` en la entrada le dice qué tipo de configuración cambió, y el campo `file_path` opcional proporciona la ruta al archivo cambiado.

El matcher filtra en la fuente de configuración:

| Matcher            | Cuándo se activa                                 |
| :----------------- | :----------------------------------------------- |
| `user_settings`    | `~/.claude/settings.json` cambia                 |
| `project_settings` | `.claude/settings.json` cambia                   |
| `local_settings`   | `.claude/settings.local.json` cambia             |
| `policy_settings`  | La configuración de política administrada cambia |
| `skills`           | Un archivo de skill en `.claude/skills/` cambia  |

Este ejemplo registra todos los cambios de configuración para auditoría de seguridad:

```json  theme={null}
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

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
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

```json  theme={null}
{
  "decision": "block",
  "reason": "Configuration changes to project settings require admin approval"
}
```

Los cambios de `policy_settings` no pueden bloquearse. Los hooks aún se activan para fuentes de `policy_settings`, por lo que puede usarlos para registro de auditoría, pero cualquier decisión de bloqueo se ignora. Esto asegura que la configuración administrada por la empresa siempre tenga efecto.

### WorktreeCreate

Cuando ejecuta `claude --worktree` o un [subagente usa `isolation: "worktree"`](/es/sub-agents#choose-the-subagent-scope), Claude Code crea una copia de trabajo aislada usando `git worktree`. Si configura un hook WorktreeCreate, reemplaza el comportamiento predeterminado de git, permitiéndole usar un sistema de control de versiones diferente como SVN, Perforce o Mercurial.

El hook debe imprimir la ruta absoluta al directorio de worktree creado en stdout. Claude Code usa esta ruta como el directorio de trabajo para la sesión aislada.

Este ejemplo crea una copia de trabajo SVN e imprime la ruta para que Claude Code la use. Reemplace la URL del repositorio con la suya:

```json  theme={null}
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

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeCreate",
  "name": "feature-auth"
}
```

#### Salida de WorktreeCreate

El hook debe imprimir la ruta absoluta al directorio de worktree creado en stdout. Si el hook falla o no produce salida, la creación de worktree falla con un error.

Los hooks WorktreeCreate no usan el modelo de decisión de permitir/bloquear estándar. En su lugar, el éxito o fallo del hook determina el resultado. Solo se admiten hooks `type: "command"`.

### WorktreeRemove

La contraparte de limpieza de [WorktreeCreate](#worktreecreate). Este hook se activa cuando se está eliminando un worktree, ya sea cuando sale de una sesión `--worktree` y elige eliminarlo, o cuando un subagente con `isolation: "worktree"` finaliza. Para worktrees basados en git, Claude maneja la limpieza automáticamente con `git worktree remove`. Si configuró un hook WorktreeCreate para un sistema de control de versiones que no es git, emparéjelo con un hook WorktreeRemove para manejar la limpieza. Sin uno, el directorio de worktree se deja en el disco.

Claude Code pasa la ruta que WorktreeCreate imprimió en stdout como `worktree_path` en la entrada del hook. Este ejemplo lee esa ruta y elimina el directorio:

```json  theme={null}
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

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeRemove",
  "worktree_path": "/Users/.../my-project/.claude/worktrees/feature-auth"
}
```

Los hooks WorktreeRemove no tienen control de decisión. No pueden bloquear la eliminación de worktree pero pueden realizar tareas de limpieza como eliminar estado de control de versiones o archivar cambios. Los fallos de hook se registran solo en modo de depuración. Solo se admiten hooks `type: "command"`.

### PreCompact

Se ejecuta antes de que Claude Code esté a punto de ejecutar una operación de compactación.

El valor del matcher indica si la compactación fue desencadenada manualmente o automáticamente:

| Matcher  | Cuándo se activa                                                 |
| :------- | :--------------------------------------------------------------- |
| `manual` | `/compact`                                                       |
| `auto`   | Compactación automática cuando la ventana de contexto está llena |

#### Entrada de PreCompact

Además de los [campos de entrada comunes](#common-input-fields), los hooks PreCompact reciben `trigger` y `custom_instructions`. Para `manual`, `custom_instructions` contiene lo que el usuario pasa a `/compact`. Para `auto`, `custom_instructions` está vacío.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```

### SessionEnd

Se ejecuta cuando termina una sesión de Claude Code. Útil para tareas de limpieza, registro de estadísticas de sesión o guardado del estado de sesión. Admite matchers para filtrar por razón de salida.

El campo `reason` en la entrada del hook indica por qué terminó la sesión:

| Razón                         | Descripción                                                 |
| :---------------------------- | :---------------------------------------------------------- |
| `clear`                       | Sesión borrada con comando `/clear`                         |
| `logout`                      | El usuario cerró sesión                                     |
| `prompt_input_exit`           | El usuario salió mientras la entrada del prompt era visible |
| `bypass_permissions_disabled` | El modo de permisos de omisión fue deshabilitado            |
| `other`                       | Otras razones de salida                                     |

#### Entrada de SessionEnd

Además de los [campos de entrada comunes](#common-input-fields), los hooks SessionEnd reciben un campo `reason` que indica por qué terminó la sesión. Consulte la [tabla de razones](#sessionend) anterior para todos los valores.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SessionEnd",
  "reason": "other"
}
```

Los hooks SessionEnd no tienen control de decisión. No pueden bloquear la terminación de sesión pero pueden realizar tareas de limpieza.

## Hooks basados en prompt

Además de hooks de comando y HTTP, Claude Code admite hooks basados en prompt (`type: "prompt"`) que usan un LLM para evaluar si permitir o bloquear una acción, y hooks de agente (`type: "agent"`) que generan un verificador agentico con acceso a herramientas. No todos los eventos admiten todos los tipos de hooks.

Eventos que admiten los cuatro tipos de hooks (`command`, `http`, `prompt` y `agent`):

* `PermissionRequest`
* `PostToolUse`
* `PostToolUseFailure`
* `PreToolUse`
* `Stop`
* `SubagentStop`
* `TaskCompleted`
* `UserPromptSubmit`

Eventos que solo admiten hooks `type: "command"`:

* `ConfigChange`
* `InstructionsLoaded`
* `Notification`
* `PreCompact`
* `SessionEnd`
* `SessionStart`
* `SubagentStart`
* `TeammateIdle`
* `WorktreeCreate`
* `WorktreeRemove`

### Cómo funcionan los hooks basados en prompt

En lugar de ejecutar un comando Bash, los hooks basados en prompt:

1. Envían la entrada del hook y su prompt a un modelo Claude, Haiku por defecto
2. El LLM responde con JSON estructurado que contiene una decisión
3. Claude Code procesa la decisión automáticamente

### Configuración de hook de prompt

Establezca `type` en `"prompt"` y proporcione una cadena `prompt` en lugar de un `command`. Use el marcador de posición `$ARGUMENTS` para inyectar datos de entrada JSON del hook en su texto de prompt. Claude Code envía el prompt combinado e entrada a un modelo Claude rápido, que devuelve una decisión JSON.

Este hook `Stop` le pide al LLM que evalúe si Claude debe detenerse antes de permitir que finalice:

```json  theme={null}
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

```json  theme={null}
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

```json  theme={null}
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

## Hooks basados en agente

Los hooks basados en agente (`type: "agent"`) son como hooks basados en prompt pero con acceso a herramientas de múltiples turnos. En lugar de una única llamada LLM, un hook de agente genera un subagente que puede leer archivos, buscar código e inspeccionar la base de código para verificar condiciones. Los hooks de agente admiten los mismos eventos que los hooks basados en prompt.

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

## Ejecutar hooks en segundo plano

Por defecto, los hooks bloquean la ejecución de Claude hasta que se completen. Para tareas de larga duración como implementaciones, suites de prueba o llamadas a API externas, establezca `"async": true` para ejecutar el hook en segundo plano mientras Claude continúa trabajando. Los hooks asincronos no pueden bloquear o controlar el comportamiento de Claude: campos de respuesta como `decision`, `permissionDecision` y `continue` no tienen efecto, porque la acción que habrían controlado ya se ha completado.

### Configurar un hook asincrónico

Agregue `"async": true` a la configuración de un hook de comando para ejecutarlo en segundo plano sin bloquear a Claude. Este campo solo está disponible en hooks `type: "command"`.

Este hook ejecuta un script de prueba después de cada llamada a herramienta `Write`. Claude continúa trabajando inmediatamente mientras `run-tests.sh` se ejecuta durante hasta 120 segundos. Cuando el script finaliza, su salida se entrega en el siguiente turno de conversación:

```json  theme={null}
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

### Ejemplo: ejecutar pruebas después de cambios de archivo

Este hook inicia una suite de prueba en segundo plano cada vez que Claude escribe un archivo, luego reporta los resultados a Claude cuando las pruebas finalizan. Guarde este script en `.claude/hooks/run-tests-async.sh` en su proyecto y hágalo ejecutable con `chmod +x`:

```bash  theme={null}
#!/bin/bash
# run-tests-async.sh

# Read hook input from stdin
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only run tests for source files
if [[ "$FILE_PATH" != *.ts && "$FILE_PATH" != *.js ]]; then
  exit 0
fi

# Run tests and report results via systemMessage
RESULT=$(npm test 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "{\"systemMessage\": \"Tests passed after editing $FILE_PATH\"}"
else
  echo "{\"systemMessage\": \"Tests failed after editing $FILE_PATH: $RESULT\"}"
fi
```

Luego agregue esta configuración a `.claude/settings.json` en la raíz de su proyecto. La bandera `async: true` permite que Claude continúe trabajando mientras se ejecutan las pruebas:

```json  theme={null}
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

* Solo los hooks `type: "command"` admiten `async`. Los hooks basados en prompt no pueden ejecutarse de forma asincrónica.
* Los hooks asincronos no pueden bloquear llamadas a herramientas o devolver decisiones. Para cuando se completa el hook, la acción desencadenante ya ha procedido.
* La salida del hook se entrega en el siguiente turno de conversación. Si la sesión está inactiva, la respuesta espera hasta la siguiente interacción del usuario.
* Cada ejecución crea un proceso de fondo separado. No hay deduplicación en múltiples activaciones del mismo hook asincrónico.

## Consideraciones de seguridad

### Descargo de responsabilidad

Los hooks de comando se ejecutan con los permisos completos de su usuario del sistema.

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

## Depurar hooks

Ejecute `claude --debug` para ver detalles de ejecución de hooks, incluyendo qué hooks coincidieron, sus códigos de salida y salida. Alterne el modo detallado con `Ctrl+O` para ver el progreso del hook en la transcripción.

```text  theme={null}
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Getting matching hook commands for PostToolUse with query: Write
[DEBUG] Found 1 hook matchers in settings
[DEBUG] Matched 1 hooks for query "Write"
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 600000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

Para solucionar problemas comunes como hooks que no se activan, bucles infinitos de Stop hook o errores de configuración, consulte [Limitations and troubleshooting](/es/hooks-guide#limitations-and-troubleshooting) en la guía.
