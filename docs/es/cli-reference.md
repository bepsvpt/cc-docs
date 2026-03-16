> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Referencia de CLI

> Referencia completa de la interfaz de línea de comandos de Claude Code, incluidos comandos y banderas.

## Comandos CLI

Puede iniciar sesiones, canalizar contenido, reanudar conversaciones y administrar actualizaciones con estos comandos:

| Comando                         | Descripción                                                                                                                                                                                                              | Ejemplo                                                  |
| :------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------- |
| `claude`                        | Iniciar sesión interactiva                                                                                                                                                                                               | `claude`                                                 |
| `claude "query"`                | Iniciar sesión interactiva con indicación inicial                                                                                                                                                                        | `claude "explain this project"`                          |
| `claude -p "query"`             | Consultar a través de SDK, luego salir                                                                                                                                                                                   | `claude -p "explain this function"`                      |
| `cat file \| claude -p "query"` | Procesar contenido canalizado                                                                                                                                                                                            | `cat logs.txt \| claude -p "explain"`                    |
| `claude -c`                     | Continuar la conversación más reciente en el directorio actual                                                                                                                                                           | `claude -c`                                              |
| `claude -c -p "query"`          | Continuar a través de SDK                                                                                                                                                                                                | `claude -c -p "Check for type errors"`                   |
| `claude -r "<session>" "query"` | Reanudar sesión por ID o nombre                                                                                                                                                                                          | `claude -r "auth-refactor" "Finish this PR"`             |
| `claude update`                 | Actualizar a la versión más reciente                                                                                                                                                                                     | `claude update`                                          |
| `claude auth login`             | Inicie sesión en su cuenta de Anthropic. Use `--email` para rellenar previamente su dirección de correo electrónico y `--sso` para forzar la autenticación SSO                                                           | `claude auth login --email user@example.com --sso`       |
| `claude auth logout`            | Cerrar sesión en su cuenta de Anthropic                                                                                                                                                                                  | `claude auth logout`                                     |
| `claude auth status`            | Mostrar estado de autenticación como JSON. Use `--text` para salida legible por humanos. Sale con código 0 si ha iniciado sesión, 1 si no                                                                                | `claude auth status`                                     |
| `claude agents`                 | Enumerar todos los [subagents](/es/sub-agents) configurados, agrupados por fuente                                                                                                                                        | `claude agents`                                          |
| `claude mcp`                    | Configurar servidores Model Context Protocol (MCP)                                                                                                                                                                       | Consulte la [documentación de Claude Code MCP](/es/mcp). |
| `claude remote-control`         | Iniciar una [sesión de Remote Control](/es/remote-control) para controlar Claude Code desde Claude.ai o la aplicación Claude mientras se ejecuta localmente. Consulte [Remote Control](/es/remote-control) para banderas | `claude remote-control`                                  |

## Banderas CLI

Personalice el comportamiento de Claude Code con estas banderas de línea de comandos:

| Bandera                                | Descripción                                                                                                                                                                                                                                     | Ejemplo                                                                                            |
| :------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| `--add-dir`                            | Agregar directorios de trabajo adicionales para que Claude acceda (valida que cada ruta exista como directorio)                                                                                                                                 | `claude --add-dir ../apps ../lib`                                                                  |
| `--agent`                              | Especificar un agente para la sesión actual (anula la configuración `agent`)                                                                                                                                                                    | `claude --agent my-custom-agent`                                                                   |
| `--agents`                             | Definir [subagents](/es/sub-agents) personalizados dinámicamente a través de JSON (consulte a continuación el formato)                                                                                                                          | `claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'` |
| `--allow-dangerously-skip-permissions` | Habilitar el bypass de permisos como opción sin activarlo inmediatamente. Permite componer con `--permission-mode` (usar con cuidado)                                                                                                           | `claude --permission-mode plan --allow-dangerously-skip-permissions`                               |
| `--allowedTools`                       | Herramientas que se ejecutan sin solicitar permiso. Consulte [sintaxis de regla de permiso](/es/settings#permission-rule-syntax) para coincidencia de patrones. Para restringir qué herramientas están disponibles, use `--tools` en su lugar   | `"Bash(git log *)" "Bash(git diff *)" "Read"`                                                      |
| `--append-system-prompt`               | Agregar texto personalizado al final del indicador del sistema predeterminado                                                                                                                                                                   | `claude --append-system-prompt "Always use TypeScript"`                                            |
| `--append-system-prompt-file`          | Cargar texto de indicación del sistema adicional desde un archivo y agregar al indicador predeterminado                                                                                                                                         | `claude --append-system-prompt-file ./extra-rules.txt`                                             |
| `--betas`                              | Encabezados beta para incluir en solicitudes de API (solo usuarios con clave API)                                                                                                                                                               | `claude --betas interleaved-thinking`                                                              |
| `--chrome`                             | Habilitar [integración del navegador Chrome](/es/chrome) para automatización web y pruebas                                                                                                                                                      | `claude --chrome`                                                                                  |
| `--continue`, `-c`                     | Cargar la conversación más reciente en el directorio actual                                                                                                                                                                                     | `claude --continue`                                                                                |
| `--dangerously-skip-permissions`       | Omitir todos los indicadores de permiso (usar con cuidado)                                                                                                                                                                                      | `claude --dangerously-skip-permissions`                                                            |
| `--debug`                              | Habilitar modo de depuración con filtrado de categoría opcional (por ejemplo, `"api,hooks"` o `"!statsig,!file"`)                                                                                                                               | `claude --debug "api,mcp"`                                                                         |
| `--disable-slash-commands`             | Deshabilitar todas las skills y comandos para esta sesión                                                                                                                                                                                       | `claude --disable-slash-commands`                                                                  |
| `--disallowedTools`                    | Herramientas que se eliminan del contexto del modelo y no se pueden usar                                                                                                                                                                        | `"Bash(git log *)" "Bash(git diff *)" "Edit"`                                                      |
| `--fallback-model`                     | Habilitar conmutación automática al modelo especificado cuando el modelo predeterminado está sobrecargado (solo modo de impresión)                                                                                                              | `claude -p --fallback-model sonnet "query"`                                                        |
| `--fork-session`                       | Al reanudar, crear un nuevo ID de sesión en lugar de reutilizar el original (usar con `--resume` o `--continue`)                                                                                                                                | `claude --resume abc123 --fork-session`                                                            |
| `--from-pr`                            | Reanudar sesiones vinculadas a un PR específico de GitHub. Acepta un número de PR o URL. Las sesiones se vinculan automáticamente cuando se crean a través de `gh pr create`                                                                    | `claude --from-pr 123`                                                                             |
| `--ide`                                | Conectarse automáticamente al IDE al iniciar si exactamente un IDE válido está disponible                                                                                                                                                       | `claude --ide`                                                                                     |
| `--init`                               | Ejecutar hooks de inicialización e iniciar modo interactivo                                                                                                                                                                                     | `claude --init`                                                                                    |
| `--init-only`                          | Ejecutar hooks de inicialización y salir (sin sesión interactiva)                                                                                                                                                                               | `claude --init-only`                                                                               |
| `--include-partial-messages`           | Incluir eventos de transmisión parcial en la salida (requiere `--print` y `--output-format=stream-json`)                                                                                                                                        | `claude -p --output-format stream-json --include-partial-messages "query"`                         |
| `--input-format`                       | Especificar formato de entrada para modo de impresión (opciones: `text`, `stream-json`)                                                                                                                                                         | `claude -p --output-format json --input-format stream-json`                                        |
| `--json-schema`                        | Obtener salida JSON validada que coincida con un JSON Schema después de que el agente complete su flujo de trabajo (solo modo de impresión, consulte [salidas estructuradas](https://platform.claude.com/docs/en/agent-sdk/structured-outputs)) | `claude -p --json-schema '{"type":"object","properties":{...}}' "query"`                           |
| `--maintenance`                        | Ejecutar hooks de mantenimiento y salir                                                                                                                                                                                                         | `claude --maintenance`                                                                             |
| `--max-budget-usd`                     | Cantidad máxima en dólares a gastar en llamadas API antes de detener (solo modo de impresión)                                                                                                                                                   | `claude -p --max-budget-usd 5.00 "query"`                                                          |
| `--max-turns`                          | Limitar el número de turnos agentes (solo modo de impresión). Sale con un error cuando se alcanza el límite. Sin límite por defecto                                                                                                             | `claude -p --max-turns 3 "query"`                                                                  |
| `--mcp-config`                         | Cargar servidores MCP desde archivos JSON o cadenas (separados por espacios)                                                                                                                                                                    | `claude --mcp-config ./mcp.json`                                                                   |
| `--model`                              | Establece el modelo para la sesión actual con un alias para el modelo más reciente (`sonnet` u `opus`) o el nombre completo de un modelo                                                                                                        | `claude --model claude-sonnet-4-6`                                                                 |
| `--no-chrome`                          | Deshabilitar [integración del navegador Chrome](/es/chrome) para esta sesión                                                                                                                                                                    | `claude --no-chrome`                                                                               |
| `--no-session-persistence`             | Deshabilitar la persistencia de sesión para que las sesiones no se guarden en disco y no se puedan reanudar (solo modo de impresión)                                                                                                            | `claude -p --no-session-persistence "query"`                                                       |
| `--output-format`                      | Especificar formato de salida para modo de impresión (opciones: `text`, `json`, `stream-json`)                                                                                                                                                  | `claude -p "query" --output-format json`                                                           |
| `--permission-mode`                    | Comenzar en un [modo de permiso](/es/permissions#permission-modes) especificado                                                                                                                                                                 | `claude --permission-mode plan`                                                                    |
| `--permission-prompt-tool`             | Especificar una herramienta MCP para manejar indicadores de permiso en modo no interactivo                                                                                                                                                      | `claude -p --permission-prompt-tool mcp_auth_tool "query"`                                         |
| `--plugin-dir`                         | Cargar plugins desde directorios solo para esta sesión (repetible)                                                                                                                                                                              | `claude --plugin-dir ./my-plugins`                                                                 |
| `--print`, `-p`                        | Imprimir respuesta sin modo interactivo (consulte la [documentación de Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) para detalles de uso programático)                                                                    | `claude -p "query"`                                                                                |
| `--remote`                             | Crear una nueva [sesión web](/es/claude-code-on-the-web) en claude.ai con la descripción de tarea proporcionada                                                                                                                                 | `claude --remote "Fix the login bug"`                                                              |
| `--resume`, `-r`                       | Reanudar una sesión específica por ID o nombre, o mostrar un selector interactivo para elegir una sesión                                                                                                                                        | `claude --resume auth-refactor`                                                                    |
| `--session-id`                         | Usar un ID de sesión específico para la conversación (debe ser un UUID válido)                                                                                                                                                                  | `claude --session-id "550e8400-e29b-41d4-a716-446655440000"`                                       |
| `--setting-sources`                    | Lista separada por comas de fuentes de configuración a cargar (`user`, `project`, `local`)                                                                                                                                                      | `claude --setting-sources user,project`                                                            |
| `--settings`                           | Ruta a un archivo JSON de configuración o una cadena JSON para cargar configuración adicional desde                                                                                                                                             | `claude --settings ./settings.json`                                                                |
| `--strict-mcp-config`                  | Usar solo servidores MCP de `--mcp-config`, ignorando todas las demás configuraciones de MCP                                                                                                                                                    | `claude --strict-mcp-config --mcp-config ./mcp.json`                                               |
| `--system-prompt`                      | Reemplazar todo el indicador del sistema con texto personalizado                                                                                                                                                                                | `claude --system-prompt "You are a Python expert"`                                                 |
| `--system-prompt-file`                 | Cargar indicador del sistema desde un archivo, reemplazando el indicador predeterminado                                                                                                                                                         | `claude --system-prompt-file ./custom-prompt.txt`                                                  |
| `--teleport`                           | Reanudar una [sesión web](/es/claude-code-on-the-web) en su terminal local                                                                                                                                                                      | `claude --teleport`                                                                                |
| `--teammate-mode`                      | Establecer cómo se muestran los compañeros del [equipo de agentes](/es/agent-teams): `auto` (predeterminado), `in-process` o `tmux`. Consulte [configurar equipos de agentes](/es/agent-teams#set-up-agent-teams)                               | `claude --teammate-mode in-process`                                                                |
| `--tools`                              | Restringir qué herramientas integradas puede usar Claude. Use `""` para deshabilitar todas, `"default"` para todas, o nombres de herramientas como `"Bash,Edit,Read"`                                                                           | `claude --tools "Bash,Edit,Read"`                                                                  |
| `--verbose`                            | Habilitar registro detallado, muestra salida completa turno por turno                                                                                                                                                                           | `claude --verbose`                                                                                 |
| `--version`, `-v`                      | Mostrar el número de versión                                                                                                                                                                                                                    | `claude -v`                                                                                        |
| `--worktree`, `-w`                     | Iniciar Claude en un [git worktree](/es/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) aislado en `<repo>/.claude/worktrees/<name>`. Si no se proporciona un nombre, se genera automáticamente                          | `claude -w feature-auth`                                                                           |

<Tip>
  La bandera `--output-format json` es particularmente útil para scripting y
  automatización, permitiéndole analizar las respuestas de Claude mediante programación.
</Tip>

### Formato de bandera de agentes

La bandera `--agents` acepta un objeto JSON que define uno o más subagents personalizados. Cada subagent requiere un nombre único (como clave) y un objeto de definición con los siguientes campos:

| Campo             | Requerido | Descripción                                                                                                                                                                                                                                      |
| :---------------- | :-------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `description`     | Sí        | Descripción en lenguaje natural de cuándo se debe invocar el subagent                                                                                                                                                                            |
| `prompt`          | Sí        | El indicador del sistema que guía el comportamiento del subagent                                                                                                                                                                                 |
| `tools`           | No        | Matriz de herramientas específicas que el subagent puede usar, por ejemplo `["Read", "Edit", "Bash"]`. Si se omite, hereda todas las herramientas. Admite sintaxis [`Agent(agent_type)`](/es/sub-agents#restrict-which-subagents-can-be-spawned) |
| `disallowedTools` | No        | Matriz de nombres de herramientas a negar explícitamente para este subagent                                                                                                                                                                      |
| `model`           | No        | Alias de modelo a usar: `sonnet`, `opus`, `haiku` o `inherit`. Si se omite, por defecto es `inherit`                                                                                                                                             |
| `skills`          | No        | Matriz de nombres de [skill](/es/skills) para precargar en el contexto del subagent                                                                                                                                                              |
| `mcpServers`      | No        | Matriz de [servidores MCP](/es/mcp) para este subagent. Cada entrada es una cadena de nombre de servidor o un objeto `{name: config}`                                                                                                            |
| `maxTurns`        | No        | Número máximo de turnos agentes antes de que el subagent se detenga                                                                                                                                                                              |

Ejemplo:

```bash  theme={null}
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

Para más detalles sobre cómo crear y usar subagents, consulte la [documentación de subagents](/es/sub-agents).

### Banderas de indicador del sistema

Claude Code proporciona cuatro banderas para personalizar el indicador del sistema. Las cuatro funcionan tanto en modo interactivo como no interactivo.

| Bandera                       | Comportamiento                                               | Caso de uso                                                                                            |
| :---------------------------- | :----------------------------------------------------------- | :----------------------------------------------------------------------------------------------------- |
| `--system-prompt`             | **Reemplaza** todo el indicador predeterminado               | Control completo sobre el comportamiento e instrucciones de Claude                                     |
| `--system-prompt-file`        | **Reemplaza** con contenido del archivo                      | Cargar indicadores desde archivos para reproducibilidad y control de versiones                         |
| `--append-system-prompt`      | **Agrega** al indicador predeterminado                       | Agregar instrucciones específicas mientras se mantiene el comportamiento predeterminado de Claude Code |
| `--append-system-prompt-file` | **Agrega** contenido del archivo al indicador predeterminado | Cargar instrucciones adicionales desde archivos mientras se mantienen los valores predeterminados      |

**Cuándo usar cada una:**

* **`--system-prompt`**: usar cuando necesite control completo sobre el indicador del sistema de Claude. Esto elimina todas las instrucciones predeterminadas de Claude Code, dándole una pizarra en blanco.
  ```bash  theme={null}
  claude --system-prompt "You are a Python expert who only writes type-annotated code"
  ```

* **`--system-prompt-file`**: usar cuando desee cargar un indicador personalizado desde un archivo, útil para la consistencia del equipo o plantillas de indicadores controladas por versiones.
  ```bash  theme={null}
  claude --system-prompt-file ./prompts/code-review.txt
  ```

* **`--append-system-prompt`**: usar cuando desee agregar instrucciones específicas mientras mantiene intactas las capacidades predeterminadas de Claude Code. Esta es la opción más segura para la mayoría de los casos de uso.
  ```bash  theme={null}
  claude --append-system-prompt "Always use TypeScript and include JSDoc comments"
  ```

* **`--append-system-prompt-file`**: usar cuando desee agregar instrucciones desde un archivo mientras mantiene los valores predeterminados de Claude Code. Útil para adiciones controladas por versiones.
  ```bash  theme={null}
  claude --append-system-prompt-file ./prompts/style-rules.txt
  ```

`--system-prompt` y `--system-prompt-file` son mutuamente excluyentes. Las banderas de adición se pueden usar junto con cualquiera de las banderas de reemplazo.

Para la mayoría de los casos de uso, se recomienda `--append-system-prompt` o `--append-system-prompt-file` ya que preservan las capacidades integradas de Claude Code mientras agregan sus requisitos personalizados. Use `--system-prompt` o `--system-prompt-file` solo cuando necesite control completo sobre el indicador del sistema.

## Ver también

* [Extensión de Chrome](/es/chrome) - Automatización de navegador y pruebas web
* [Modo interactivo](/es/interactive-mode) - Atajos de teclado, modos de entrada y características interactivas
* [Guía de inicio rápido](/es/quickstart) - Introducción a Claude Code
* [Flujos de trabajo comunes](/es/common-workflows) - Flujos de trabajo y patrones avanzados
* [Configuración](/es/settings) - Opciones de configuración
* [Documentación de Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) - Uso programático e integraciones
