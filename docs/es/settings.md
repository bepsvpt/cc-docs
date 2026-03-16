> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configuración de Claude Code

> Configure Claude Code con configuraciones globales y a nivel de proyecto, y variables de entorno.

Claude Code ofrece una variedad de configuraciones para personalizar su comportamiento según sus necesidades. Puede configurar Claude Code ejecutando el comando `/config` cuando utiliza el REPL interactivo, que abre una interfaz de Configuración con pestañas donde puede ver información de estado y modificar opciones de configuración.

## Alcances de configuración

Claude Code utiliza un **sistema de alcances** para determinar dónde se aplican las configuraciones y quién las comparte. Comprender los alcances le ayuda a decidir cómo configurar Claude Code para uso personal, colaboración en equipo o implementación empresarial.

### Alcances disponibles

| Alcance     | Ubicación                                                                                                  | A quién afecta                              | ¿Se comparte con el equipo? |
| :---------- | :--------------------------------------------------------------------------------------------------------- | :------------------------------------------ | :-------------------------- |
| **Managed** | Configuraciones administradas por servidor, plist / registro, o `managed-settings.json` a nivel de sistema | Todos los usuarios en la máquina            | Sí (implementado por TI)    |
| **User**    | Directorio `~/.claude/`                                                                                    | Usted, en todos los proyectos               | No                          |
| **Project** | `.claude/` en el repositorio                                                                               | Todos los colaboradores en este repositorio | Sí (confirmado en git)      |
| **Local**   | `.claude/settings.local.json`                                                                              | Usted, solo en este repositorio             | No (ignorado por git)       |

### Cuándo usar cada alcance

El alcance **Managed** es para:

* Políticas de seguridad que deben aplicarse en toda la organización
* Requisitos de cumplimiento que no se pueden anular
* Configuraciones estandarizadas implementadas por TI/DevOps

El alcance **User** es mejor para:

* Preferencias personales que desea en todas partes (temas, configuraciones del editor)
* Herramientas y plugins que utiliza en todos los proyectos
* Claves API y autenticación (almacenadas de forma segura)

El alcance **Project** es mejor para:

* Configuraciones compartidas por el equipo (permisos, hooks, MCP servers)
* Plugins que todo el equipo debe tener
* Estandarización de herramientas entre colaboradores

El alcance **Local** es mejor para:

* Anulaciones personales para un proyecto específico
* Configuraciones de prueba antes de compartir con el equipo
* Configuraciones específicas de la máquina que no funcionarán para otros

### Cómo interactúan los alcances

Cuando la misma configuración se configura en múltiples alcances, los alcances más específicos tienen prioridad:

1. **Managed** (más alto) - no puede ser anulado por nada
2. **Argumentos de línea de comandos** - anulaciones de sesión temporal
3. **Local** - anula configuraciones de proyecto y usuario
4. **Project** - anula configuraciones de usuario
5. **User** (más bajo) - se aplica cuando nada más especifica la configuración

Por ejemplo, si un permiso se permite en la configuración de usuario pero se deniega en la configuración del proyecto, la configuración del proyecto tiene prioridad y el permiso se bloquea.

### Qué usa alcances

Los alcances se aplican a muchas características de Claude Code:

| Característica  | Ubicación de usuario      | Ubicación de proyecto             | Ubicación local                 |
| :-------------- | :------------------------ | :-------------------------------- | :------------------------------ |
| **Settings**    | `~/.claude/settings.json` | `.claude/settings.json`           | `.claude/settings.local.json`   |
| **Subagents**   | `~/.claude/agents/`       | `.claude/agents/`                 | —                               |
| **MCP servers** | `~/.claude.json`          | `.mcp.json`                       | `~/.claude.json` (por proyecto) |
| **Plugins**     | `~/.claude/settings.json` | `.claude/settings.json`           | `.claude/settings.local.json`   |
| **CLAUDE.md**   | `~/.claude/CLAUDE.md`     | `CLAUDE.md` o `.claude/CLAUDE.md` | —                               |

***

## Archivos de configuración

El archivo `settings.json` es nuestro mecanismo oficial para configurar Claude Code a través de configuraciones jerárquicas:

* **Configuraciones de usuario** se definen en `~/.claude/settings.json` y se aplican a todos los proyectos.
* **Configuraciones de proyecto** se guardan en su directorio de proyecto:
  * `.claude/settings.json` para configuraciones que se verifican en el control de código fuente y se comparten con su equipo
  * `.claude/settings.local.json` para configuraciones que no se verifican, útiles para preferencias personales y experimentación. Claude Code configurará git para ignorar `.claude/settings.local.json` cuando se cree.
* **Configuraciones administradas**: Para organizaciones que necesitan control centralizado, Claude Code admite múltiples mecanismos de entrega para configuraciones administradas. Todos utilizan el mismo formato JSON y no pueden ser anulados por configuraciones de usuario o proyecto:

  * **Configuraciones administradas por servidor**: entregadas desde los servidores de Anthropic a través de la consola de administración de Claude.ai. Consulte [configuraciones administradas por servidor](/es/server-managed-settings).
  * **Políticas de MDM/nivel de SO**: entregadas a través de administración de dispositivos nativa en macOS y Windows:
    * macOS: dominio de preferencias administradas `com.anthropic.claudecode` (implementado a través de perfiles de configuración en Jamf, Kandji u otras herramientas MDM)
    * Windows: clave de registro `HKLM\SOFTWARE\Policies\ClaudeCode` con un valor `Settings` (REG\_SZ o REG\_EXPAND\_SZ) que contiene JSON (implementado a través de Política de Grupo o Intune)
    * Windows (nivel de usuario): `HKCU\SOFTWARE\Policies\ClaudeCode` (prioridad de política más baja, solo se usa cuando no existe una fuente a nivel de administrador)
  * **Basado en archivos**: `managed-settings.json` y `managed-mcp.json` implementados en directorios del sistema:
    * macOS: `/Library/Application Support/ClaudeCode/`
    * Linux y WSL: `/etc/claude-code/`
    * Windows: `C:\Program Files\ClaudeCode\`

  Consulte [configuraciones administradas](/es/permissions#managed-only-settings) y [Configuración de MCP administrada](/es/mcp#managed-mcp-configuration) para obtener detalles.

  <Note>
    Las implementaciones administradas también pueden restringir **adiciones de marketplace de plugins** usando `strictKnownMarketplaces`. Para obtener más información, consulte [Restricciones de marketplace administradas](/es/plugin-marketplaces#managed-marketplace-restrictions).
  </Note>
* **Otra configuración** se almacena en `~/.claude.json`. Este archivo contiene sus preferencias (tema, configuraciones de notificación, modo de editor), sesión OAuth, configuraciones de [MCP server](/es/mcp) para alcances de usuario y local, estado por proyecto (herramientas permitidas, configuraciones de confianza) y varios cachés. Los MCP servers con alcance de proyecto se almacenan por separado en `.mcp.json`.

<Note>
  Claude Code crea automáticamente copias de seguridad con marca de tiempo de archivos de configuración y retiene las cinco copias de seguridad más recientes para prevenir pérdida de datos.
</Note>

```JSON Ejemplo settings.json theme={null}
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test *)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  },
  "companyAnnouncements": [
    "Welcome to Acme Corp! Review our code guidelines at docs.acme.com",
    "Reminder: Code reviews required for all PRs",
    "New security policy in effect"
  ]
}
```

La línea `$schema` en el ejemplo anterior apunta al [esquema JSON oficial](https://json.schemastore.org/claude-code-settings.json) para configuraciones de Claude Code. Agregarlo a su `settings.json` habilita autocompletado y validación en línea en VS Code, Cursor y cualquier otro editor que admita validación de esquema JSON.

### Configuraciones disponibles

`settings.json` admite varias opciones:

| Clave                             | Descripción                                                                                                                                                                                                                                                                                                                                                                                       | Ejemplo                                                                 |
| :-------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---------------------------------------------------------------------- |
| `apiKeyHelper`                    | Script personalizado, a ejecutarse en `/bin/sh`, para generar un valor de autenticación. Este valor se enviará como encabezados `X-Api-Key` y `Authorization: Bearer` para solicitudes de modelo                                                                                                                                                                                                  | `/bin/generate_temp_api_key.sh`                                         |
| `cleanupPeriodDays`               | Las sesiones inactivas durante más tiempo que este período se eliminan al inicio. Establecer en `0` elimina inmediatamente todas las sesiones. (predeterminado: 30 días)                                                                                                                                                                                                                          | `20`                                                                    |
| `companyAnnouncements`            | Anuncio a mostrar a los usuarios al inicio. Si se proporcionan múltiples anuncios, se alternarán aleatoriamente.                                                                                                                                                                                                                                                                                  | `["Welcome to Acme Corp! Review our code guidelines at docs.acme.com"]` |
| `env`                             | Variables de entorno que se aplicarán a cada sesión                                                                                                                                                                                                                                                                                                                                               | `{"FOO": "bar"}`                                                        |
| `attribution`                     | Personalizar atribución para commits de git y solicitudes de extracción. Consulte [Configuración de atribución](#attribution-settings)                                                                                                                                                                                                                                                            | `{"commit": "🤖 Generated with Claude Code", "pr": ""}`                 |
| `includeCoAuthoredBy`             | **Obsoleto**: Use `attribution` en su lugar. Si incluir la línea `co-authored-by Claude` en commits de git y solicitudes de extracción (predeterminado: `true`)                                                                                                                                                                                                                                   | `false`                                                                 |
| `includeGitInstructions`          | Incluir instrucciones de flujo de trabajo de commit y PR integradas en el indicador del sistema de Claude (predeterminado: `true`). Establezca en `false` para eliminar estas instrucciones, por ejemplo cuando utiliza sus propias skills de flujo de trabajo de git. La variable de entorno `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` tiene prioridad sobre esta configuración cuando se establece | `false`                                                                 |
| `permissions`                     | Consulte la tabla a continuación para la estructura de permisos.                                                                                                                                                                                                                                                                                                                                  |                                                                         |
| `hooks`                           | Configurar comandos personalizados para ejecutarse en eventos del ciclo de vida. Consulte [documentación de hooks](/es/hooks) para el formato                                                                                                                                                                                                                                                     | Consulte [hooks](/es/hooks)                                             |
| `disableAllHooks`                 | Deshabilitar todos los [hooks](/es/hooks) y cualquier [línea de estado](/es/statusline) personalizada                                                                                                                                                                                                                                                                                             | `true`                                                                  |
| `allowManagedHooksOnly`           | (Solo configuraciones administradas) Prevenir la carga de hooks de usuario, proyecto y plugin. Solo permite hooks administrados y hooks SDK. Consulte [Configuración de hooks](#hook-configuration)                                                                                                                                                                                               | `true`                                                                  |
| `allowedHttpHookUrls`             | Lista blanca de patrones de URL que los hooks HTTP pueden dirigirse. Admite `*` como comodín. Cuando se establece, los hooks con URLs que no coinciden se bloquean. Sin definir = sin restricción, matriz vacía = bloquear todos los hooks HTTP. Las matrices se fusionan entre fuentes de configuración. Consulte [Configuración de hooks](#hook-configuration)                                  | `["https://hooks.example.com/*"]`                                       |
| `httpHookAllowedEnvVars`          | Lista blanca de nombres de variables de entorno que los hooks HTTP pueden interpolar en encabezados. Cuando se establece, el `allowedEnvVars` efectivo de cada hook es la intersección con esta lista. Sin definir = sin restricción. Las matrices se fusionan entre fuentes de configuración. Consulte [Configuración de hooks](#hook-configuration)                                             | `["MY_TOKEN", "HOOK_SECRET"]`                                           |
| `allowManagedPermissionRulesOnly` | (Solo configuraciones administradas) Prevenir que configuraciones de usuario y proyecto definan reglas de permiso `allow`, `ask` o `deny`. Solo se aplican las reglas en configuraciones administradas. Consulte [Configuraciones solo administradas](/es/permissions#managed-only-settings)                                                                                                      | `true`                                                                  |
| `allowManagedMcpServersOnly`      | (Solo configuraciones administradas) Solo se respetan `allowedMcpServers` de configuraciones administradas. `deniedMcpServers` aún se fusiona de todas las fuentes. Los usuarios aún pueden agregar MCP servers, pero solo se aplica la lista blanca definida por el administrador. Consulte [Configuración de MCP administrada](/es/mcp#managed-mcp-configuration)                               | `true`                                                                  |
| `model`                           | Anular el modelo predeterminado a usar para Claude Code                                                                                                                                                                                                                                                                                                                                           | `"claude-sonnet-4-6"`                                                   |
| `availableModels`                 | Restringir qué modelos pueden seleccionar los usuarios a través de `/model`, `--model`, herramienta Config o `ANTHROPIC_MODEL`. No afecta la opción Predeterminado. Consulte [Restringir selección de modelo](/es/model-config#restrict-model-selection)                                                                                                                                          | `["sonnet", "haiku"]`                                                   |
| `modelOverrides`                  | Asignar IDs de modelo de Anthropic a IDs de modelo específicos del proveedor como ARNs de perfil de inferencia de Bedrock. Cada entrada del selector de modelo utiliza su valor asignado al llamar a la API del proveedor. Consulte [Anular IDs de modelo por versión](/es/model-config#override-model-ids-per-version)                                                                           | `{"claude-opus-4-6": "arn:aws:bedrock:..."}`                            |
| `otelHeadersHelper`               | Script para generar encabezados dinámicos de OpenTelemetry. Se ejecuta al inicio y periódicamente (consulte [Encabezados dinámicos](/es/monitoring-usage#dynamic-headers))                                                                                                                                                                                                                        | `/bin/generate_otel_headers.sh`                                         |
| `statusLine`                      | Configurar una línea de estado personalizada para mostrar contexto. Consulte [documentación de `statusLine`](/es/statusline)                                                                                                                                                                                                                                                                      | `{"type": "command", "command": "~/.claude/statusline.sh"}`             |
| `fileSuggestion`                  | Configurar un script personalizado para autocompletado de archivos `@`. Consulte [Configuración de sugerencia de archivos](#file-suggestion-settings)                                                                                                                                                                                                                                             | `{"type": "command", "command": "~/.claude/file-suggestion.sh"}`        |
| `respectGitignore`                | Controlar si el selector de archivos `@` respeta patrones `.gitignore`. Cuando es `true` (predeterminado), los archivos que coinciden con patrones `.gitignore` se excluyen de las sugerencias                                                                                                                                                                                                    | `false`                                                                 |
| `outputStyle`                     | Configurar un estilo de salida para ajustar el indicador del sistema. Consulte [documentación de estilos de salida](/es/output-styles)                                                                                                                                                                                                                                                            | `"Explanatory"`                                                         |
| `forceLoginMethod`                | Use `claudeai` para restringir el inicio de sesión a cuentas de Claude.ai, `console` para restringir el inicio de sesión a cuentas de Claude Console (facturación de uso de API)                                                                                                                                                                                                                  | `claudeai`                                                              |
| `forceLoginOrgUUID`               | Especificar el UUID de una organización para seleccionarla automáticamente durante el inicio de sesión, omitiendo el paso de selección de organización. Requiere que `forceLoginMethod` esté establecido                                                                                                                                                                                          | `"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"`                                |
| `enableAllProjectMcpServers`      | Aprobar automáticamente todos los MCP servers definidos en archivos `.mcp.json` del proyecto                                                                                                                                                                                                                                                                                                      | `true`                                                                  |
| `enabledMcpjsonServers`           | Lista de MCP servers específicos de archivos `.mcp.json` para aprobar                                                                                                                                                                                                                                                                                                                             | `["memory", "github"]`                                                  |
| `disabledMcpjsonServers`          | Lista de MCP servers específicos de archivos `.mcp.json` para rechazar                                                                                                                                                                                                                                                                                                                            | `["filesystem"]`                                                        |
| `allowedMcpServers`               | Cuando se establece en managed-settings.json, lista blanca de MCP servers que los usuarios pueden configurar. Sin definir = sin restricciones, matriz vacía = bloqueo. Se aplica a todos los alcances. La lista de denegación tiene prioridad. Consulte [Configuración de MCP administrada](/es/mcp#managed-mcp-configuration)                                                                    | `[{ "serverName": "github" }]`                                          |
| `deniedMcpServers`                | Cuando se establece en managed-settings.json, lista de denegación de MCP servers que se bloquean explícitamente. Se aplica a todos los alcances incluyendo servidores administrados. La lista de denegación tiene prioridad sobre la lista blanca. Consulte [Configuración de MCP administrada](/es/mcp#managed-mcp-configuration)                                                                | `[{ "serverName": "filesystem" }]`                                      |
| `strictKnownMarketplaces`         | Cuando se establece en managed-settings.json, lista blanca de marketplaces de plugins que los usuarios pueden agregar. Sin definir = sin restricciones, matriz vacía = bloqueo. Se aplica solo a adiciones de marketplace. Consulte [Restricciones de marketplace administradas](/es/plugin-marketplaces#managed-marketplace-restrictions)                                                        | `[{ "source": "github", "repo": "acme-corp/plugins" }]`                 |
| `blockedMarketplaces`             | (Solo configuraciones administradas) Lista de bloqueo de fuentes de marketplace. Las fuentes bloqueadas se verifican antes de descargar, por lo que nunca tocan el sistema de archivos. Consulte [Restricciones de marketplace administradas](/es/plugin-marketplaces#managed-marketplace-restrictions)                                                                                           | `[{ "source": "github", "repo": "untrusted/plugins" }]`                 |
| `pluginTrustMessage`              | (Solo configuraciones administradas) Mensaje personalizado agregado a la advertencia de confianza de plugin mostrada antes de la instalación. Utilice esto para agregar contexto específico de la organización, por ejemplo para confirmar que los plugins de su marketplace interno están verificados.                                                                                           | `"All plugins from our marketplace are approved by IT"`                 |
| `awsAuthRefresh`                  | Script personalizado que modifica el directorio `.aws` (consulte [configuración de credenciales avanzada](/es/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                                                  | `aws sso login --profile myprofile`                                     |
| `awsCredentialExport`             | Script personalizado que genera JSON con credenciales de AWS (consulte [configuración de credenciales avanzada](/es/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                                            | `/bin/generate_aws_grant.sh`                                            |
| `alwaysThinkingEnabled`           | Habilitar [pensamiento extendido](/es/common-workflows#use-extended-thinking-thinking-mode) de forma predeterminada para todas las sesiones. Típicamente configurado a través del comando `/config` en lugar de editar directamente                                                                                                                                                               | `true`                                                                  |
| `plansDirectory`                  | Personalizar dónde se almacenan los archivos de plan. La ruta es relativa a la raíz del proyecto. Predeterminado: `~/.claude/plans`                                                                                                                                                                                                                                                               | `"./plans"`                                                             |
| `showTurnDuration`                | Mostrar mensajes de duración de turno después de respuestas (por ejemplo, "Cooked for 1m 6s"). Establezca en `false` para ocultar estos mensajes                                                                                                                                                                                                                                                  | `true`                                                                  |
| `spinnerVerbs`                    | Personalizar los verbos de acción mostrados en el spinner y mensajes de duración de turno. Establezca `mode` en `"replace"` para usar solo sus verbos, o `"append"` para agregarlos a los predeterminados                                                                                                                                                                                         | `{"mode": "append", "verbs": ["Pondering", "Crafting"]}`                |
| `language`                        | Configurar el idioma de respuesta preferido de Claude (por ejemplo, `"japanese"`, `"spanish"`, `"french"`). Claude responderá en este idioma de forma predeterminada                                                                                                                                                                                                                              | `"japanese"`                                                            |
| `autoUpdatesChannel`              | Canal de lanzamiento a seguir para actualizaciones. Use `"stable"` para una versión que típicamente tiene aproximadamente una semana de antigüedad y omite versiones con regresiones importantes, o `"latest"` (predeterminado) para el lanzamiento más reciente                                                                                                                                  | `"stable"`                                                              |
| `spinnerTipsEnabled`              | Mostrar consejos en el spinner mientras Claude está trabajando. Establezca en `false` para deshabilitar consejos (predeterminado: `true`)                                                                                                                                                                                                                                                         | `false`                                                                 |
| `spinnerTipsOverride`             | Anular consejos del spinner con cadenas personalizadas. `tips`: matriz de cadenas de consejo. `excludeDefault`: si es `true`, mostrar solo consejos personalizados; si es `false` o está ausente, los consejos personalizados se fusionan con consejos integrados                                                                                                                                 | `{ "excludeDefault": true, "tips": ["Use our internal tool X"] }`       |
| `terminalProgressBarEnabled`      | Habilitar la barra de progreso del terminal que muestra progreso en terminales compatibles como Windows Terminal e iTerm2 (predeterminado: `true`)                                                                                                                                                                                                                                                | `false`                                                                 |
| `prefersReducedMotion`            | Reducir o deshabilitar animaciones de UI (spinners, shimmer, efectos flash) para accesibilidad                                                                                                                                                                                                                                                                                                    | `true`                                                                  |
| `fastModePerSessionOptIn`         | Cuando es `true`, el modo rápido no persiste entre sesiones. Cada sesión comienza con el modo rápido desactivado, requiriendo que los usuarios lo habiliten con `/fast`. La preferencia de modo rápido del usuario aún se guarda. Consulte [Requerir opt-in por sesión](/es/fast-mode#require-per-session-opt-in)                                                                                 | `true`                                                                  |
| `teammateMode`                    | Cómo se muestran los compañeros del [equipo de agentes](/es/agent-teams): `auto` (elige paneles divididos en tmux o iTerm2, en proceso de otro modo), `in-process`, o `tmux`. Consulte [configurar equipos de agentes](/es/agent-teams#set-up-agent-teams)                                                                                                                                        | `"in-process"`                                                          |

### Configuración de permisos

| Claves                         | Descripción                                                                                                                                                                                                                                                                               | Ejemplo                                                                |
| :----------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `allow`                        | Matriz de reglas de permiso para permitir el uso de herramientas. Consulte [Sintaxis de regla de permiso](#permission-rule-syntax) a continuación para detalles de coincidencia de patrones                                                                                               | `[ "Bash(git diff *)" ]`                                               |
| `ask`                          | Matriz de reglas de permiso para pedir confirmación al usar herramientas. Consulte [Sintaxis de regla de permiso](#permission-rule-syntax) a continuación                                                                                                                                 | `[ "Bash(git push *)" ]`                                               |
| `deny`                         | Matriz de reglas de permiso para denegar el uso de herramientas. Use esto para excluir archivos sensibles del acceso de Claude Code. Consulte [Sintaxis de regla de permiso](#permission-rule-syntax) y [Limitaciones de permiso de Bash](/es/permissions#tool-specific-permission-rules) | `[ "WebFetch", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)" ]` |
| `additionalDirectories`        | [Directorios de trabajo](/es/permissions#working-directories) adicionales a los que Claude tiene acceso                                                                                                                                                                                   | `[ "../docs/" ]`                                                       |
| `defaultMode`                  | [Modo de permiso](/es/permissions#permission-modes) predeterminado al abrir Claude Code                                                                                                                                                                                                   | `"acceptEdits"`                                                        |
| `disableBypassPermissionsMode` | Establezca en `"disable"` para prevenir que el modo `bypassPermissions` sea activado. Esto deshabilita la bandera de línea de comandos `--dangerously-skip-permissions`. Consulte [configuraciones administradas](/es/permissions#managed-only-settings)                                  | `"disable"`                                                            |

### Sintaxis de regla de permiso

Las reglas de permiso siguen el formato `Tool` o `Tool(specifier)`. Las reglas se evalúan en orden: primero reglas de denegación, luego preguntar, luego permitir. La primera regla coincidente gana.

Ejemplos rápidos:

| Regla                          | Efecto                                             |
| :----------------------------- | :------------------------------------------------- |
| `Bash`                         | Coincide con todos los comandos Bash               |
| `Bash(npm run *)`              | Coincide con comandos que comienzan con `npm run`  |
| `Read(./.env)`                 | Coincide con la lectura del archivo `.env`         |
| `WebFetch(domain:example.com)` | Coincide con solicitudes de búsqueda a example.com |

Para la referencia completa de sintaxis de regla, incluyendo comportamiento de comodín, patrones específicos de herramientas para Read, Edit, WebFetch, MCP y reglas de Agent, y limitaciones de seguridad de patrones de Bash, consulte [Sintaxis de regla de permiso](/es/permissions#permission-rule-syntax).

### Configuración de sandbox

Configure el comportamiento avanzado de sandboxing. El sandboxing aísla comandos bash de su sistema de archivos y red. Consulte [Sandboxing](/es/sandboxing) para obtener detalles.

| Claves                            | Descripción                                                                                                                                                                                                                                                                                                                                                                                             | Ejemplo                         |
| :-------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------ |
| `enabled`                         | Habilitar sandboxing de bash (macOS, Linux y WSL2). Predeterminado: false                                                                                                                                                                                                                                                                                                                               | `true`                          |
| `autoAllowBashIfSandboxed`        | Aprobar automáticamente comandos bash cuando están en sandbox. Predeterminado: true                                                                                                                                                                                                                                                                                                                     | `true`                          |
| `excludedCommands`                | Comandos que deben ejecutarse fuera del sandbox                                                                                                                                                                                                                                                                                                                                                         | `["git", "docker"]`             |
| `allowUnsandboxedCommands`        | Permitir que los comandos se ejecuten fuera del sandbox a través del parámetro `dangerouslyDisableSandbox`. Cuando se establece en `false`, la escotilla de escape `dangerouslyDisableSandbox` se deshabilita completamente y todos los comandos deben ejecutarse en sandbox (o estar en `excludedCommands`). Útil para políticas empresariales que requieren sandboxing estricto. Predeterminado: true | `false`                         |
| `filesystem.allowWrite`           | Rutas adicionales donde los comandos en sandbox pueden escribir. Las matrices se fusionan en todos los alcances de configuración: las rutas de usuario, proyecto y administradas se combinan, no se reemplazan. También se fusionan con rutas de reglas de permiso `Edit(...)` allow. Consulte [prefijos de ruta de sandbox](#sandbox-path-prefixes) a continuación.                                    | `["//tmp/build", "~/.kube"]`    |
| `filesystem.denyWrite`            | Rutas donde los comandos en sandbox no pueden escribir. Las matrices se fusionan en todos los alcances de configuración. También se fusionan con rutas de reglas de permiso `Edit(...)` deny.                                                                                                                                                                                                           | `["//etc", "//usr/local/bin"]`  |
| `filesystem.denyRead`             | Rutas donde los comandos en sandbox no pueden leer. Las matrices se fusionan en todos los alcances de configuración. También se fusionan con rutas de reglas de permiso `Read(...)` deny.                                                                                                                                                                                                               | `["~/.aws/credentials"]`        |
| `network.allowUnixSockets`        | Rutas de socket Unix accesibles en sandbox (para agentes SSH, etc.)                                                                                                                                                                                                                                                                                                                                     | `["~/.ssh/agent-socket"]`       |
| `network.allowAllUnixSockets`     | Permitir todas las conexiones de socket Unix en sandbox. Predeterminado: false                                                                                                                                                                                                                                                                                                                          | `true`                          |
| `network.allowLocalBinding`       | Permitir vinculación a puertos localhost (solo macOS). Predeterminado: false                                                                                                                                                                                                                                                                                                                            | `true`                          |
| `network.allowedDomains`          | Matriz de dominios para permitir tráfico de red saliente. Admite comodines (por ejemplo, `*.example.com`).                                                                                                                                                                                                                                                                                              | `["github.com", "*.npmjs.org"]` |
| `network.allowManagedDomainsOnly` | (Solo configuraciones administradas) Solo se respetan `allowedDomains` y reglas allow `WebFetch(domain:...)` de configuraciones administradas. Los dominios de configuraciones de usuario, proyecto y local se ignoran. Los dominios no permitidos se bloquean automáticamente sin solicitar al usuario. Los dominios denegados aún se respetan de todas las fuentes. Predeterminado: false             | `true`                          |
| `network.httpProxyPort`           | Puerto de proxy HTTP usado si desea traer su propio proxy. Si no se especifica, Claude ejecutará su propio proxy.                                                                                                                                                                                                                                                                                       | `8080`                          |
| `network.socksProxyPort`          | Puerto de proxy SOCKS5 usado si desea traer su propio proxy. Si no se especifica, Claude ejecutará su propio proxy.                                                                                                                                                                                                                                                                                     | `8081`                          |
| `enableWeakerNestedSandbox`       | Habilitar sandbox más débil para entornos Docker sin privilegios (solo Linux y WSL2). **Reduce la seguridad.** Predeterminado: false                                                                                                                                                                                                                                                                    | `true`                          |
| `enableWeakerNetworkIsolation`    | (Solo macOS) Permitir acceso al servicio de confianza TLS del sistema (`com.apple.trustd.agent`) en el sandbox. Requerido para herramientas basadas en Go como `gh`, `gcloud` y `terraform` para verificar certificados TLS cuando se usa `httpProxyPort` con un proxy MITM y CA personalizada. **Reduce la seguridad** al abrir una posible ruta de exfiltración de datos. Predeterminado: false       | `true`                          |

#### Prefijos de ruta de sandbox

Las rutas en `filesystem.allowWrite`, `filesystem.denyWrite` y `filesystem.denyRead` admiten estos prefijos:

| Prefijo            | Significado                                                     | Ejemplo                                        |
| :----------------- | :-------------------------------------------------------------- | :--------------------------------------------- |
| `//`               | Ruta absoluta desde la raíz del sistema de archivos             | `//tmp/build` se convierte en `/tmp/build`     |
| `~/`               | Relativo al directorio de inicio                                | `~/.kube` se convierte en `$HOME/.kube`        |
| `/`                | Relativo al directorio del archivo de configuración             | `/build` se convierte en `$SETTINGS_DIR/build` |
| `./` o sin prefijo | Ruta relativa (resuelta por el tiempo de ejecución del sandbox) | `./output`                                     |

**Ejemplo de configuración:**

```json  theme={null}
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker"],
    "filesystem": {
      "allowWrite": ["//tmp/build", "~/.kube"],
      "denyRead": ["~/.aws/credentials"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org", "registry.yarnpkg.com"],
      "allowUnixSockets": [
        "/var/run/docker.sock"
      ],
      "allowLocalBinding": true
    }
  }
}
```

**Restricciones de sistema de archivos y red** pueden configurarse de dos formas que se fusionan:

* **Configuraciones `sandbox.filesystem`** (mostradas arriba): Controlan rutas en el límite del sandbox a nivel de SO. Estas restricciones se aplican a todos los comandos de subproceso (por ejemplo, `kubectl`, `terraform`, `npm`), no solo a las herramientas de archivo de Claude.
* **Reglas de permiso**: Use reglas allow/deny `Edit` para controlar el acceso a la herramienta de archivo de Claude, reglas deny `Read` para bloquear lecturas, y reglas allow/deny `WebFetch` para controlar dominios de red. Las rutas de estas reglas también se fusionan en la configuración del sandbox.

### Configuración de atribución

Claude Code agrega atribución a commits de git y solicitudes de extracción. Estos se configuran por separado:

* Los commits usan [git trailers](https://git-scm.com/docs/git-interpret-trailers) (como `Co-Authored-By`) de forma predeterminada, que pueden personalizarse o deshabilitarse
* Las descripciones de solicitudes de extracción son texto sin formato

| Claves   | Descripción                                                                                                                 |
| :------- | :-------------------------------------------------------------------------------------------------------------------------- |
| `commit` | Atribución para commits de git, incluyendo cualquier trailer. La cadena vacía oculta la atribución de commit                |
| `pr`     | Atribución para descripciones de solicitudes de extracción. La cadena vacía oculta la atribución de solicitud de extracción |

**Atribución de commit predeterminada:**

```text  theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**Atribución de solicitud de extracción predeterminada:**

```text  theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**Ejemplo:**

```json  theme={null}
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": ""
  }
}
```

<Note>
  La configuración `attribution` tiene prioridad sobre la configuración `includeCoAuthoredBy` obsoleta. Para ocultar toda la atribución, establezca `commit` y `pr` en cadenas vacías.
</Note>

### Configuración de sugerencia de archivos

Configure un comando personalizado para autocompletado de ruta de archivo `@`. La sugerencia de archivo integrada utiliza recorrido rápido del sistema de archivos, pero los monorepos grandes pueden beneficiarse de indexación específica del proyecto como un índice de archivo precompilado o herramientas personalizadas.

```json  theme={null}
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

El comando se ejecuta con las mismas variables de entorno que [hooks](/es/hooks), incluyendo `CLAUDE_PROJECT_DIR`. Recibe JSON a través de stdin con un campo `query`:

```json  theme={null}
{"query": "src/comp"}
```

Genere rutas de archivo separadas por saltos de línea a stdout (actualmente limitado a 15):

```text  theme={null}
src/components/Button.tsx
src/components/Modal.tsx
src/components/Form.tsx
```

**Ejemplo:**

```bash  theme={null}
#!/bin/bash
query=$(cat | jq -r '.query')
your-repo-file-index --query "$query" | head -20
```

### Configuración de hooks

Estas configuraciones controlan qué hooks se pueden ejecutar y a qué pueden acceder los hooks HTTP. La configuración `allowManagedHooksOnly` solo se puede configurar en [configuraciones administradas](#settings-files). Las listas blancas de URL y variable de entorno se pueden establecer en cualquier nivel de configuración y se fusionan entre fuentes.

**Comportamiento cuando `allowManagedHooksOnly` es `true`:**

* Se cargan hooks administrados y hooks SDK
* Se bloquean hooks de usuario, proyecto y plugin

**Restringir URLs de hooks HTTP:**

Limitar qué URLs pueden dirigirse los hooks HTTP. Admite `*` como comodín para coincidencia. Cuando la matriz se define, los hooks HTTP que se dirigen a URLs que no coinciden se bloquean silenciosamente.

```json  theme={null}
{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}
```

**Restringir variables de entorno de hooks HTTP:**

Limitar qué nombres de variables de entorno los hooks HTTP pueden interpolar en valores de encabezado. El `allowedEnvVars` efectivo de cada hook es la intersección de su propia lista y esta configuración.

```json  theme={null}
{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}
```

### Precedencia de configuración

Las configuraciones se aplican en orden de precedencia. De mayor a menor:

1. **Configuraciones administradas** ([administradas por servidor](/es/server-managed-settings), [políticas de MDM/nivel de SO](#configuration-scopes), o [configuraciones administradas](/es/settings#settings-files))
   * Políticas implementadas por TI a través de entrega de servidor, perfiles de configuración MDM, políticas de registro o archivos de configuración administrados
   * No pueden ser anuladas por ningún otro nivel, incluyendo argumentos de línea de comandos
   * Dentro del nivel administrado, la precedencia es: administrado por servidor > políticas de MDM/nivel de SO > `managed-settings.json` > registro HKCU (solo Windows). Solo se usa una fuente administrada; las fuentes no se fusionan.

2. **Argumentos de línea de comandos**
   * Anulaciones temporales para una sesión específica

3. **Configuraciones de proyecto local** (`.claude/settings.local.json`)
   * Configuraciones personales específicas del proyecto

4. **Configuraciones de proyecto compartidas** (`.claude/settings.json`)
   * Configuraciones de proyecto compartidas por el equipo en control de código fuente

5. **Configuraciones de usuario** (`~/.claude/settings.json`)
   * Configuraciones globales personales

Esta jerarquía asegura que las políticas organizacionales siempre se apliquen mientras aún permite que equipos e individuos personalicen su experiencia.

Por ejemplo, si su configuración de usuario permite `Bash(npm run *)` pero la configuración compartida de un proyecto la deniega, la configuración del proyecto tiene prioridad y el comando se bloquea.

<Note>
  **Las configuraciones de matriz se fusionan entre alcances.** Cuando la misma configuración con valor de matriz (como `sandbox.filesystem.allowWrite` o `permissions.allow`) aparece en múltiples alcances, las matrices se **concatenan y se deduplicán**, no se reemplazan. Esto significa que los alcances de menor prioridad pueden agregar entradas sin anular las establecidas por alcances de mayor prioridad, y viceversa. Por ejemplo, si las configuraciones administradas establecen `allowWrite` en `["//opt/company-tools"]` y un usuario agrega `["~/.kube"]`, ambas rutas se incluyen en la configuración final.
</Note>

### Verificar configuraciones activas

Ejecute `/status` dentro de Claude Code para ver qué fuentes de configuración están activas y de dónde provienen. La salida muestra cada capa de configuración (administrada, usuario, proyecto) junto con su origen, como `Enterprise managed settings (remote)`, `Enterprise managed settings (plist)`, `Enterprise managed settings (HKLM)`, o `Enterprise managed settings (file)`. Si un archivo de configuración contiene errores, `/status` reporta el problema para que pueda corregirlo.

### Puntos clave sobre el sistema de configuración

* **Archivos de memoria (`CLAUDE.md`)**: Contienen instrucciones y contexto que Claude carga al inicio
* **Archivos de configuración (JSON)**: Configurar permisos, variables de entorno y comportamiento de herramientas
* **Skills**: Indicaciones personalizadas que pueden invocarse con `/skill-name` o cargarse automáticamente por Claude
* **MCP servers**: Extender Claude Code con herramientas e integraciones adicionales
* **Precedencia**: Las configuraciones de nivel superior (Managed) anulan las de nivel inferior (User/Project)
* **Herencia**: Las configuraciones se fusionan, con configuraciones más específicas agregando o anulando las más amplias

### Indicador del sistema

El indicador del sistema interno de Claude Code no se publica. Para agregar instrucciones personalizadas, use archivos `CLAUDE.md` o la bandera `--append-system-prompt`.

### Excluyendo archivos sensibles

Para prevenir que Claude Code acceda a archivos que contienen información sensible como claves API, secretos y archivos de entorno, use la configuración `permissions.deny` en su archivo `.claude/settings.json`:

```json  theme={null}
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Read(./build)"
    ]
  }
}
```

Esto reemplaza la configuración `ignorePatterns` obsoleta. Los archivos que coinciden con estos patrones se excluyen del descubrimiento de archivos y resultados de búsqueda, y se deniegan las operaciones de lectura en estos archivos.

## Configuración de subagent

Claude Code admite subagents de IA personalizados que pueden configurarse en niveles de usuario y proyecto. Estos subagents se almacenan como archivos Markdown con frontmatter YAML:

* **Subagents de usuario**: `~/.claude/agents/` - Disponibles en todos sus proyectos
* **Subagents de proyecto**: `.claude/agents/` - Específicos de su proyecto y pueden compartirse con su equipo

Los archivos de subagent definen asistentes de IA especializados con indicaciones personalizadas y permisos de herramientas. Obtenga más información sobre cómo crear y usar subagents en la [documentación de subagents](/es/sub-agents).

## Configuración de plugins

Claude Code admite un sistema de plugins que le permite extender la funcionalidad con skills, agentes, hooks y MCP servers. Los plugins se distribuyen a través de marketplaces y pueden configurarse en niveles de usuario y repositorio.

### Configuración de plugins

Configuraciones relacionadas con plugins en `settings.json`:

```json  theme={null}
{
  "enabledPlugins": {
    "formatter@acme-tools": true,
    "deployer@acme-tools": true,
    "analyzer@security-plugins": false
  },
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": "github",
      "repo": "acme-corp/claude-plugins"
    }
  }
}
```

#### `enabledPlugins`

Controla qué plugins están habilitados. Formato: `"plugin-name@marketplace-name": true/false`

**Alcances**:

* **Configuraciones de usuario** (`~/.claude/settings.json`): Preferencias personales de plugins
* **Configuraciones de proyecto** (`.claude/settings.json`): Plugins específicos del proyecto compartidos con el equipo
* **Configuraciones locales** (`.claude/settings.local.json`): Anulaciones por máquina (no confirmadas)

**Ejemplo**:

```json  theme={null}
{
  "enabledPlugins": {
    "code-formatter@team-tools": true,
    "deployment-tools@team-tools": true,
    "experimental-features@personal": false
  }
}
```

#### `extraKnownMarketplaces`

Define marketplaces adicionales que deben estar disponibles para el repositorio. Típicamente se usa en configuraciones a nivel de repositorio para asegurar que los miembros del equipo tengan acceso a fuentes de plugins requeridas.

**Cuando un repositorio incluye `extraKnownMarketplaces`**:

1. Se solicita a los miembros del equipo instalar el marketplace cuando confían en la carpeta
2. Luego se solicita a los miembros del equipo instalar plugins de ese marketplace
3. Los usuarios pueden omitir marketplaces o plugins no deseados (almacenados en configuraciones de usuario)
4. La instalación respeta límites de confianza y requiere consentimiento explícito

**Ejemplo**:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    },
    "security-plugins": {
      "source": {
        "source": "git",
        "url": "https://git.example.com/security/plugins.git"
      }
    }
  }
}
```

**Tipos de fuente de marketplace**:

* `github`: Repositorio de GitHub (usa `repo`)
* `git`: Cualquier URL de git (usa `url`)
* `directory`: Ruta del sistema de archivos local (usa `path`, solo para desarrollo)
* `hostPattern`: Patrón regex para coincidir con hosts de marketplace (usa `hostPattern`)

#### `strictKnownMarketplaces`

**Solo configuraciones administradas**: Controla qué marketplaces de plugins se permite a los usuarios agregar. Esta configuración solo se puede configurar en [configuraciones administradas](/es/settings#settings-files) y proporciona a los administradores control estricto sobre fuentes de marketplace.

**Ubicaciones de archivos de configuración administrada**:

* **macOS**: `/Library/Application Support/ClaudeCode/managed-settings.json`
* **Linux y WSL**: `/etc/claude-code/managed-settings.json`
* **Windows**: `C:\Program Files\ClaudeCode\managed-settings.json`

**Características clave**:

* Solo disponible en configuraciones administradas (`managed-settings.json`)
* No puede ser anulado por configuraciones de usuario o proyecto (precedencia más alta)
* Se aplica ANTES de operaciones de red/sistema de archivos (las fuentes bloqueadas nunca se ejecutan)
* Usa coincidencia exacta para especificaciones de fuente (incluyendo `ref`, `path` para fuentes de git), excepto `hostPattern`, que usa coincidencia regex

**Comportamiento de lista blanca**:

* `undefined` (predeterminado): Sin restricciones - los usuarios pueden agregar cualquier marketplace
* Matriz vacía `[]`: Bloqueo completo - los usuarios no pueden agregar nuevos marketplaces
* Lista de fuentes: Los usuarios solo pueden agregar marketplaces que coincidan exactamente

**Todos los tipos de fuente admitidos**:

La lista blanca admite siete tipos de fuente de marketplace. La mayoría de las fuentes usan coincidencia exacta, mientras que `hostPattern` usa coincidencia regex contra el host del marketplace.

1. **Repositorios de GitHub**:

```json  theme={null}
{ "source": "github", "repo": "acme-corp/approved-plugins" }
{ "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main", "path": "marketplace" }
```

Campos: `repo` (requerido), `ref` (opcional: rama/etiqueta/SHA), `path` (opcional: subdirectorio)

2. **Repositorios de Git**:

```json  theme={null}
{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git" }
{ "source": "git", "url": "https://bitbucket.org/acme-corp/plugins.git", "ref": "production" }
{ "source": "git", "url": "ssh://git@git.example.com/plugins.git", "ref": "v3.1", "path": "approved" }
```

Campos: `url` (requerido), `ref` (opcional: rama/etiqueta/SHA), `path` (opcional: subdirectorio)

3. **Marketplaces basados en URL**:

```json  theme={null}
{ "source": "url", "url": "https://plugins.example.com/marketplace.json" }
{ "source": "url", "url": "https://cdn.example.com/marketplace.json", "headers": { "Authorization": "Bearer ${TOKEN}" } }
```

Campos: `url` (requerido), `headers` (opcional: encabezados HTTP para acceso autenticado)

<Note>
  Los marketplaces basados en URL solo descargan el archivo `marketplace.json`. No descargan archivos de plugins del servidor. Los plugins en marketplaces basados en URL deben usar fuentes externas (URLs de GitHub, npm o git) en lugar de rutas relativas. Para plugins con rutas relativas, use un marketplace basado en Git en su lugar. Consulte [Solución de problemas](/es/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces) para obtener detalles.
</Note>

4. **Paquetes NPM**:

```json  theme={null}
{ "source": "npm", "package": "@acme-corp/claude-plugins" }
{ "source": "npm", "package": "@acme-corp/approved-marketplace" }
```

Campos: `package` (requerido, admite paquetes con alcance)

5. **Rutas de archivo**:

```json  theme={null}
{ "source": "file", "path": "/usr/local/share/claude/acme-marketplace.json" }
{ "source": "file", "path": "/opt/acme-corp/plugins/marketplace.json" }
```

Campos: `path` (requerido: ruta absoluta al archivo marketplace.json)

6. **Rutas de directorio**:

```json  theme={null}
{ "source": "directory", "path": "/usr/local/share/claude/acme-plugins" }
{ "source": "directory", "path": "/opt/acme-corp/approved-marketplaces" }
```

Campos: `path` (requerido: ruta absoluta al directorio que contiene `.claude-plugin/marketplace.json`)

7. **Coincidencia de patrón de host**:

```json  theme={null}
{ "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" }
{ "source": "hostPattern", "hostPattern": "^gitlab\\.internal\\.example\\.com$" }
```

Campos: `hostPattern` (requerido: patrón regex para coincidir contra el host del marketplace)

Use coincidencia de patrón de host cuando desee permitir todos los marketplaces de un host específico sin enumerar cada repositorio individualmente. Esto es útil para organizaciones con servidores internos de GitHub Enterprise o GitLab donde los desarrolladores crean sus propios marketplaces.

Extracción de host por tipo de fuente:

* `github`: siempre coincide contra `github.com`
* `git`: extrae nombre de host de la URL (admite formatos HTTPS y SSH)
* `url`: extrae nombre de host de la URL
* `npm`, `file`, `directory`: no admitido para coincidencia de patrón de host

**Ejemplos de configuración**:

Ejemplo: permitir solo marketplaces específicos:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    },
    {
      "source": "npm",
      "package": "@acme-corp/compliance-plugins"
    }
  ]
}
```

Ejemplo - Deshabilitar todas las adiciones de marketplace:

```json  theme={null}
{
  "strictKnownMarketplaces": []
}
```

Ejemplo: permitir todos los marketplaces de un servidor git interno:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

**Requisitos de coincidencia exacta**:

Las fuentes de marketplace deben coincidir **exactamente** para que se permita la adición de un usuario. Para fuentes basadas en git (`github` y `git`), esto incluye todos los campos opcionales:

* El `repo` o `url` debe coincidir exactamente
* El campo `ref` debe coincidir exactamente (o ambos estar sin definir)
* El campo `path` debe coincidir exactamente (o ambos estar sin definir)

Ejemplos de fuentes que **NO coinciden**:

```json  theme={null}
// Estas son fuentes DIFERENTES:
{ "source": "github", "repo": "acme-corp/plugins" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main" }

// Estas también son DIFERENTES:
{ "source": "github", "repo": "acme-corp/plugins", "path": "marketplace" }
{ "source": "github", "repo": "acme-corp/plugins" }
```

**Comparación con `extraKnownMarketplaces`**:

| Aspecto                      | `strictKnownMarketplaces`                       | `extraKnownMarketplaces`                      |
| ---------------------------- | ----------------------------------------------- | --------------------------------------------- |
| **Propósito**                | Aplicación de política organizacional           | Conveniencia del equipo                       |
| **Archivo de configuración** | Solo `managed-settings.json`                    | Cualquier archivo de configuración            |
| **Comportamiento**           | Bloquea adiciones no permitidas                 | Auto-instala marketplaces faltantes           |
| **Cuándo se aplica**         | Antes de operaciones de red/sistema de archivos | Después de solicitud de confianza del usuario |
| **Puede ser anulado**        | No (precedencia más alta)                       | Sí (por configuraciones de mayor precedencia) |
| **Formato de fuente**        | Objeto de fuente directo                        | Marketplace nombrado con fuente anidada       |
| **Caso de uso**              | Cumplimiento, restricciones de seguridad        | Incorporación, estandarización                |

**Diferencia de formato**:

`strictKnownMarketplaces` usa objetos de fuente directos:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ]
}
```

`extraKnownMarketplaces` requiere marketplaces nombrados:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

**Notas importantes**:

* Las restricciones se verifican ANTES de cualquier solicitud de red u operación del sistema de archivos
* Cuando se bloquea, los usuarios ven mensajes de error claros indicando que la fuente está bloqueada por política administrada
* La restricción se aplica solo a agregar NUEVOS marketplaces; los marketplaces instalados previamente permanecen accesibles
* Las configuraciones administradas tienen la precedencia más alta y no pueden ser anuladas

Consulte [Restricciones de marketplace administradas](/es/plugin-marketplaces#managed-marketplace-restrictions) para documentación dirigida al usuario.

### Gestionar plugins

Use el comando `/plugin` para gestionar plugins interactivamente:

* Examinar plugins disponibles de marketplaces
* Instalar/desinstalar plugins
* Habilitar/deshabilitar plugins
* Ver detalles de plugins (comandos, agentes, hooks proporcionados)
* Agregar/eliminar marketplaces

Obtenga más información sobre el sistema de plugins en la [documentación de plugins](/es/plugins).

## Variables de entorno

Claude Code admite las siguientes variables de entorno para controlar su comportamiento:

<Note>
  Todas las variables de entorno también se pueden configurar en [`settings.json`](#available-settings). Esto es útil como una forma de establecer automáticamente variables de entorno para cada sesión, o para implementar un conjunto de variables de entorno para todo su equipo u organización.
</Note>

| Variable                                       | Propósito                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |     |
| :--------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --- |
| `ANTHROPIC_API_KEY`                            | Clave API enviada como encabezado `X-Api-Key`, típicamente para el SDK de Claude (para uso interactivo, ejecute `/login`)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |     |
| `ANTHROPIC_AUTH_TOKEN`                         | Valor personalizado para el encabezado `Authorization` (el valor que establezca aquí será prefijado con `Bearer `)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `ANTHROPIC_CUSTOM_HEADERS`                     | Encabezados personalizados para agregar a solicitudes (formato `Name: Value`, separados por saltos de línea para múltiples encabezados)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`                | Consulte [Configuración de modelo](/es/model-config#environment-variables)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`                 | Consulte [Configuración de modelo](/es/model-config#environment-variables)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `ANTHROPIC_DEFAULT_SONNET_MODEL`               | Consulte [Configuración de modelo](/es/model-config#environment-variables)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `ANTHROPIC_FOUNDRY_API_KEY`                    | Clave API para autenticación de Microsoft Foundry (consulte [Microsoft Foundry](/es/microsoft-foundry))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `ANTHROPIC_FOUNDRY_BASE_URL`                   | URL base completa para el recurso de Foundry (por ejemplo, `https://my-resource.services.ai.azure.com/anthropic`). Alternativa a `ANTHROPIC_FOUNDRY_RESOURCE` (consulte [Microsoft Foundry](/es/microsoft-foundry))                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `ANTHROPIC_FOUNDRY_RESOURCE`                   | Nombre del recurso de Foundry (por ejemplo, `my-resource`). Requerido si `ANTHROPIC_FOUNDRY_BASE_URL` no está establecido (consulte [Microsoft Foundry](/es/microsoft-foundry))                                                                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `ANTHROPIC_MODEL`                              | Nombre de la configuración de modelo a usar (consulte [Configuración de modelo](/es/model-config#environment-variables))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `ANTHROPIC_SMALL_FAST_MODEL`                   | \[OBSOLETO] Nombre de [modelo de clase Haiku para tareas de fondo](/es/costs)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION`        | Anular región de AWS para el modelo de clase Haiku cuando se usa Bedrock                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `AWS_BEARER_TOKEN_BEDROCK`                     | Clave API de Bedrock para autenticación (consulte [Claves API de Bedrock](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/))                                                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `BASH_DEFAULT_TIMEOUT_MS`                      | Tiempo de espera predeterminado para comandos bash de larga duración                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `BASH_MAX_OUTPUT_LENGTH`                       | Número máximo de caracteres en salidas de bash antes de que se truncen en el medio                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `BASH_MAX_TIMEOUT_MS`                          | Tiempo de espera máximo que el modelo puede establecer para comandos bash de larga duración                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`              | Establecer el porcentaje de capacidad de ventana de contexto (1-100) en el que se activa la compactación automática. De forma predeterminada, la compactación automática se activa aproximadamente al 95% de capacidad. Use valores más bajos como `50` para compactar antes. Los valores por encima del umbral predeterminado no tienen efecto. Se aplica a conversaciones principales y subagents. Este porcentaje se alinea con el campo `context_window.used_percentage` disponible en [línea de estado](/es/statusline)                                                                                              |     |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR`     | Volver al directorio de trabajo original después de cada comando Bash                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `CLAUDE_CODE_ACCOUNT_UUID`                     | UUID de cuenta para el usuario autenticado. Utilizado por llamadores de SDK para proporcionar información de cuenta de forma síncrona, evitando una condición de carrera donde eventos de telemetría tempranos carecen de metadatos de cuenta. Requiere que `CLAUDE_CODE_USER_EMAIL` y `CLAUDE_CODE_ORGANIZATION_UUID` también estén establecidos                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | Establecer en `1` para cargar archivos CLAUDE.md de directorios especificados con `--add-dir`. De forma predeterminada, los directorios adicionales no cargan archivos de memoria                                                                                                                                                                                                                                                                                                                                                                                                                                         | `1` |
| `CLAUDE_CODE_API_KEY_HELPER_TTL_MS`            | Intervalo en milisegundos en el que las credenciales deben actualizarse (cuando se usa `apiKeyHelper`)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `CLAUDE_CODE_CLIENT_CERT`                      | Ruta al archivo de certificado de cliente para autenticación mTLS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_CODE_CLIENT_KEY`                       | Ruta al archivo de clave privada de cliente para autenticación mTLS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE`            | Frase de contraseña para `CLAUDE_CODE_CLIENT_KEY` cifrado (opcional)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT`               | Establecer en `1` para deshabilitar soporte de [ventana de contexto de 1M](/es/model-config#extended-context). Cuando se establece, las variantes de modelo de 1M no están disponibles en el selector de modelo. Útil para entornos empresariales con requisitos de cumplimiento                                                                                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING`        | Establecer en `1` para deshabilitar [razonamiento adaptativo](/es/model-config#adjust-effort-level) para Opus 4.6 y Sonnet 4.6. Cuando se deshabilita, estos modelos vuelven al presupuesto de pensamiento fijo controlado por `MAX_THINKING_TOKENS`                                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY`              | Establecer en `1` para deshabilitar [memoria automática](/es/memory#auto-memory). Establecer en `0` para forzar memoria automática durante el despliegue gradual. Cuando se deshabilita, Claude no crea ni carga archivos de memoria automática                                                                                                                                                                                                                                                                                                                                                                           |     |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS`         | Establecer en `1` para eliminar instrucciones de flujo de trabajo de commit y PR integradas del indicador del sistema de Claude. Útil cuando se usan sus propias skills de flujo de trabajo de git. Tiene prioridad sobre la configuración [`includeGitInstructions`](#available-settings) cuando se establece                                                                                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`         | Establecer en `1` para deshabilitar toda la funcionalidad de tareas de fondo, incluyendo el parámetro `run_in_background` en herramientas Bash y subagent, auto-backgrounding y el atajo Ctrl+B                                                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `CLAUDE_CODE_DISABLE_CRON`                     | Establecer en `1` para deshabilitar [tareas programadas](/es/scheduled-tasks). La skill `/loop` y las herramientas cron se vuelven no disponibles y cualquier tarea ya programada deja de ejecutarse, incluyendo tareas que ya se están ejecutando a mitad de sesión                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`       | Establecer en `1` para deshabilitar encabezados `anthropic-beta` específicos de la API de Anthropic. Use esto si experimenta problemas como "Unexpected value(s) for the `anthropic-beta` header" cuando se usa una puerta de enlace LLM con proveedores de terceros                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_DISABLE_FAST_MODE`                | Establecer en `1` para deshabilitar [modo rápido](/es/fast-mode)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY`          | Establecer en `1` para deshabilitar las encuestas de calidad de sesión "¿Cómo está Claude?". También se deshabilita cuando se usan proveedores de terceros o cuando la telemetría está deshabilitada. Consulte [Encuestas de calidad de sesión](/es/data-usage#session-quality-surveys)                                                                                                                                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`     | Equivalente a establecer `DISABLE_AUTOUPDATER`, `DISABLE_BUG_COMMAND`, `DISABLE_ERROR_REPORTING` y `DISABLE_TELEMETRY`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `CLAUDE_CODE_DISABLE_TERMINAL_TITLE`           | Establecer en `1` para deshabilitar actualizaciones automáticas del título del terminal basadas en contexto de conversación                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_EFFORT_LEVEL`                     | Establecer el nivel de esfuerzo para modelos admitidos. Valores: `low`, `medium`, `high`. El esfuerzo más bajo es más rápido y barato, el esfuerzo más alto proporciona razonamiento más profundo. Admitido en Opus 4.6 y Sonnet 4.6. Consulte [Ajustar nivel de esfuerzo](/es/model-config#adjust-effort-level)                                                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION`         | Establecer en `false` para deshabilitar sugerencias de indicación (el toggle "Prompt suggestions" en `/config`). Estas son las predicciones atenuadas que aparecen en su entrada de indicación después de que Claude responde. Consulte [Sugerencias de indicación](/es/interactive-mode#prompt-suggestions)                                                                                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_ENABLE_TASKS`                     | Establecer en `false` para revertir temporalmente a la lista TODO anterior en lugar del sistema de seguimiento de tareas. Predeterminado: `true`. Consulte [Lista de tareas](/es/interactive-mode#task-list)                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                 | Establecer en `1` para habilitar la recopilación de datos de OpenTelemetry para métricas y registro. Requerido antes de configurar exportadores de OTel. Consulte [Monitoreo](/es/monitoring-usage)                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY`            | Tiempo en milisegundos a esperar después de que el bucle de consulta se vuelva inactivo antes de salir automáticamente. Útil para flujos de trabajo automatizados y scripts que usan modo SDK                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`         | Establecer en `1` para habilitar [equipos de agentes](/es/agent-teams). Los equipos de agentes son experimentales y están deshabilitados de forma predeterminada                                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS`      | Anular el límite de token predeterminado para lecturas de archivo. Útil cuando necesita leer archivos más grandes en su totalidad                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_CODE_HIDE_ACCOUNT_INFO`                | Establecer en `1` para ocultar su dirección de correo electrónico y nombre de organización de la UI de Claude Code. Útil cuando se transmite o se graban sesiones                                                                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`            | Omitir auto-instalación de extensiones IDE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS`                | Establecer el número máximo de tokens de salida para la mayoría de solicitudes. Predeterminado: 32,000. Máximo: 64,000. Aumentar este valor reduce la ventana de contexto efectiva disponible antes de que se active [compactación automática](/es/costs#reduce-token-usage).                                                                                                                                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_ORGANIZATION_UUID`                | UUID de organización para el usuario autenticado. Utilizado por llamadores de SDK para proporcionar información de cuenta de forma síncrona. Requiere que `CLAUDE_CODE_ACCOUNT_UUID` y `CLAUDE_CODE_USER_EMAIL` también estén establecidos                                                                                                                                                                                                                                                                                                                                                                                |     |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`  | Intervalo para actualizar encabezados dinámicos de OpenTelemetry en milisegundos (predeterminado: 1740000 / 29 minutos). Consulte [Encabezados dinámicos](/es/monitoring-usage#dynamic-headers)                                                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `CLAUDE_CODE_PLAN_MODE_REQUIRED`               | Auto-establecido en `true` en compañeros de [equipo de agentes](/es/agent-teams) que requieren aprobación de plan. Solo lectura: establecido por Claude Code al generar compañeros. Consulte [requerir aprobación de plan](/es/agent-teams#require-plan-approval-for-teammates)                                                                                                                                                                                                                                                                                                                                           |     |
| `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`            | Tiempo de espera en milisegundos para operaciones de git al instalar o actualizar plugins (predeterminado: 120000). Aumente este valor para repositorios grandes o conexiones de red lentas. Consulte [Las operaciones de Git agotan el tiempo](/es/plugin-marketplaces#git-operations-time-out)                                                                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_PROXY_RESOLVES_HOSTS`             | Establecer en `true` para permitir que el proxy realice resolución de DNS en lugar de la persona que llama. Opt-in para entornos donde el proxy debe manejar la resolución de nombres de host                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_SHELL`                            | Anular detección automática de shell. Útil cuando su shell de inicio difiere de su shell de trabajo preferido (por ejemplo, `bash` vs `zsh`)                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_SHELL_PREFIX`                     | Prefijo de comando para envolver todos los comandos bash (por ejemplo, para registro o auditoría). Ejemplo: `/path/to/logger.sh` ejecutará `/path/to/logger.sh <command>`                                                                                                                                                                                                                                                                                                                                                                                                                                                 |     |
| `CLAUDE_CODE_SIMPLE`                           | Establecer en `1` para ejecutar con un indicador del sistema mínimo y solo las herramientas Bash, lectura de archivo y edición de archivo. Deshabilita herramientas MCP, adjuntos, hooks y archivos CLAUDE.md                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_SKIP_BEDROCK_AUTH`                | Omitir autenticación de AWS para Bedrock (por ejemplo, cuando se usa una puerta de enlace LLM)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_SKIP_FOUNDRY_AUTH`                | Omitir autenticación de Azure para Microsoft Foundry (por ejemplo, cuando se usa una puerta de enlace LLM)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `CLAUDE_CODE_SKIP_VERTEX_AUTH`                 | Omitir autenticación de Google para Vertex (por ejemplo, cuando se usa una puerta de enlace LLM)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_SUBAGENT_MODEL`                   | Consulte [Configuración de modelo](/es/model-config)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_TASK_LIST_ID`                     | Compartir una lista de tareas entre sesiones. Establezca el mismo ID en múltiples instancias de Claude Code para coordinar en una lista de tareas compartida. Consulte [Lista de tareas](/es/interactive-mode#task-list)                                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `CLAUDE_CODE_TEAM_NAME`                        | Nombre del equipo de agentes al que pertenece este compañero. Se establece automáticamente en miembros de [equipo de agentes](/es/agent-teams)                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_TMPDIR`                           | Anular el directorio temporal usado para archivos temporales internos. Claude Code agrega `/claude/` a esta ruta. Predeterminado: `/tmp` en Unix/macOS, `os.tmpdir()` en Windows                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_USER_EMAIL`                       | Dirección de correo electrónico para el usuario autenticado. Utilizado por llamadores de SDK para proporcionar información de cuenta de forma síncrona. Requiere que `CLAUDE_CODE_ACCOUNT_UUID` y `CLAUDE_CODE_ORGANIZATION_UUID` también estén establecidos                                                                                                                                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_USE_BEDROCK`                      | Usar [Bedrock](/es/amazon-bedrock)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_USE_FOUNDRY`                      | Usar [Microsoft Foundry](/es/microsoft-foundry)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `CLAUDE_CODE_USE_VERTEX`                       | Usar [Vertex](/es/google-vertex-ai)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `CLAUDE_CONFIG_DIR`                            | Personalizar dónde Claude Code almacena sus archivos de configuración y datos                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `DISABLE_AUTOUPDATER`                          | Establecer en `1` para deshabilitar actualizaciones automáticas.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `DISABLE_BUG_COMMAND`                          | Establecer en `1` para deshabilitar el comando `/bug`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `DISABLE_COST_WARNINGS`                        | Establecer en `1` para deshabilitar mensajes de advertencia de costo                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `DISABLE_ERROR_REPORTING`                      | Establecer en `1` para optar por no participar en informes de errores de Sentry                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `DISABLE_INSTALLATION_CHECKS`                  | Establecer en `1` para deshabilitar advertencias de instalación. Use solo cuando administre manualmente la ubicación de instalación, ya que esto puede enmascarar problemas con instalaciones estándar                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `DISABLE_NON_ESSENTIAL_MODEL_CALLS`            | Establecer en `1` para deshabilitar llamadas de modelo para rutas no críticas como texto de sabor                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `DISABLE_PROMPT_CACHING`                       | Establecer en `1` para deshabilitar prompt caching para todos los modelos (tiene prioridad sobre configuraciones por modelo)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `DISABLE_PROMPT_CACHING_HAIKU`                 | Establecer en `1` para deshabilitar prompt caching para modelos Haiku                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `DISABLE_PROMPT_CACHING_OPUS`                  | Establecer en `1` para deshabilitar prompt caching para modelos Opus                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `DISABLE_PROMPT_CACHING_SONNET`                | Establecer en `1` para deshabilitar prompt caching para modelos Sonnet                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `DISABLE_TELEMETRY`                            | Establecer en `1` para optar por no participar en telemetría de Statsig (tenga en cuenta que los eventos de Statsig no incluyen datos de usuario como código, rutas de archivo o comandos bash)                                                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `ENABLE_CLAUDEAI_MCP_SERVERS`                  | Establecer en `false` para deshabilitar [MCP servers de claude.ai](/es/mcp#use-mcp-servers-from-claudeai) en Claude Code. Habilitado de forma predeterminada para usuarios conectados                                                                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `ENABLE_TOOL_SEARCH`                           | Controla [búsqueda de herramientas MCP](/es/mcp#scale-with-mcp-tool-search). Valores: `auto` (predeterminado, habilita al 10% de contexto), `auto:N` (umbral personalizado, por ejemplo, `auto:5` para 5%), `true` (siempre activado), `false` (deshabilitado)                                                                                                                                                                                                                                                                                                                                                            |     |
| `FORCE_AUTOUPDATE_PLUGINS`                     | Establecer en `true` para forzar auto-actualizaciones de plugins incluso cuando el auto-actualizador principal está deshabilitado a través de `DISABLE_AUTOUPDATER`                                                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `HTTP_PROXY`                                   | Especificar servidor proxy HTTP para conexiones de red                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `HTTPS_PROXY`                                  | Especificar servidor proxy HTTPS para conexiones de red                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `IS_DEMO`                                      | Establecer en `true` para habilitar modo de demostración: oculta correo electrónico y organización de la UI, omite incorporación y oculta comandos internos. Útil para transmitir o grabar sesiones                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `MAX_MCP_OUTPUT_TOKENS`                        | Número máximo de tokens permitidos en respuestas de herramientas MCP. Claude Code muestra una advertencia cuando la salida excede 10,000 tokens (predeterminado: 25000)                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `MAX_THINKING_TOKENS`                          | Anular el presupuesto de token de [pensamiento extendido](https://platform.claude.com/docs/en/build-with-claude/extended-thinking). El pensamiento está habilitado al presupuesto máximo (31,999 tokens) de forma predeterminada. Use esto para limitar el presupuesto (por ejemplo, `MAX_THINKING_TOKENS=10000`) o deshabilitar el pensamiento completamente (`MAX_THINKING_TOKENS=0`). Para Opus 4.6, la profundidad de pensamiento se controla por [nivel de esfuerzo](/es/model-config#adjust-effort-level) en su lugar, y esta variable se ignora a menos que se establezca en `0` para deshabilitar el pensamiento. |     |
| `MCP_CLIENT_SECRET`                            | Secreto de cliente OAuth para MCP servers que requieren [credenciales preconfiguradas](/es/mcp#use-pre-configured-oauth-credentials). Evita el indicador interactivo al agregar un servidor con `--client-secret`                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `MCP_OAUTH_CALLBACK_PORT`                      | Puerto fijo para la devolución de llamada de redirección de OAuth, como alternativa a `--callback-port` al agregar un MCP server con [credenciales preconfiguradas](/es/mcp#use-pre-configured-oauth-credentials)                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `MCP_TIMEOUT`                                  | Tiempo de espera en milisegundos para inicio de MCP server                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `MCP_TOOL_TIMEOUT`                             | Tiempo de espera en milisegundos para ejecución de herramienta MCP                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `NO_PROXY`                                     | Lista de dominios e IPs a los que se emitirán solicitudes directamente, omitiendo proxy                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET`               | Anular el presupuesto de caracteres para metadatos de skill mostrados a la [herramienta Skill](/es/skills#control-who-invokes-a-skill). El presupuesto se escala dinámicamente al 2% de la ventana de contexto, con un respaldo de 16,000 caracteres. Nombre heredado mantenido para compatibilidad hacia atrás                                                                                                                                                                                                                                                                                                           |     |
| `USE_BUILTIN_RIPGREP`                          | Establecer en `0` para usar `rg` instalado en el sistema en lugar de `rg` incluido con Claude Code                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `VERTEX_REGION_CLAUDE_3_5_HAIKU`               | Anular región para Claude 3.5 Haiku cuando se usa Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `VERTEX_REGION_CLAUDE_3_7_SONNET`              | Anular región para Claude 3.7 Sonnet cuando se usa Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `VERTEX_REGION_CLAUDE_4_0_OPUS`                | Anular región para Claude 4.0 Opus cuando se usa Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `VERTEX_REGION_CLAUDE_4_0_SONNET`              | Anular región para Claude 4.0 Sonnet cuando se usa Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `VERTEX_REGION_CLAUDE_4_1_OPUS`                | Anular región para Claude 4.1 Opus cuando se usa Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |

## Herramientas disponibles para Claude

Claude Code tiene acceso a un conjunto de herramientas poderosas que le ayudan a entender y modificar su base de código:

| Herramienta              | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Permiso requerido |
| :----------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------- |
| **Agent**                | Genera un [subagent](/es/sub-agents) con su propia ventana de contexto para manejar una tarea                                                                                                                                                                                                                                                                                                                                                                                     | No                |
| **AskUserQuestion**      | Hace preguntas de opción múltiple para recopilar requisitos o aclarar ambigüedad                                                                                                                                                                                                                                                                                                                                                                                                  | No                |
| **Bash**                 | Ejecuta comandos de shell en su entorno. Consulte [Comportamiento de herramienta Bash](#bash-tool-behavior)                                                                                                                                                                                                                                                                                                                                                                       | Sí                |
| **CronCreate**           | Programa una indicación recurrente o de una sola vez dentro de la sesión actual (desaparece cuando Claude sale). Consulte [tareas programadas](/es/scheduled-tasks)                                                                                                                                                                                                                                                                                                               | No                |
| **CronDelete**           | Cancela una tarea programada por ID                                                                                                                                                                                                                                                                                                                                                                                                                                               | No                |
| **CronList**             | Lista todas las tareas programadas en la sesión                                                                                                                                                                                                                                                                                                                                                                                                                                   | No                |
| **Edit**                 | Realiza ediciones dirigidas a archivos específicos                                                                                                                                                                                                                                                                                                                                                                                                                                | Sí                |
| **EnterPlanMode**        | Cambia a modo de plan para diseñar un enfoque antes de codificar                                                                                                                                                                                                                                                                                                                                                                                                                  | No                |
| **EnterWorktree**        | Crea un [git worktree](/es/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) aislado y cambia a él                                                                                                                                                                                                                                                                                                                                                           | No                |
| **ExitPlanMode**         | Presenta un plan para aprobación y sale del modo de plan                                                                                                                                                                                                                                                                                                                                                                                                                          | Sí                |
| **ExitWorktree**         | Sale de una sesión de worktree y vuelve al directorio original                                                                                                                                                                                                                                                                                                                                                                                                                    | No                |
| **Glob**                 | Encuentra archivos basados en coincidencia de patrones                                                                                                                                                                                                                                                                                                                                                                                                                            | No                |
| **Grep**                 | Busca patrones en contenidos de archivos                                                                                                                                                                                                                                                                                                                                                                                                                                          | No                |
| **ListMcpResourcesTool** | Lista recursos expuestos por [MCP servers](/es/mcp) conectados                                                                                                                                                                                                                                                                                                                                                                                                                    | No                |
| **LSP**                  | Inteligencia de código a través de servidores de lenguaje. Reporta errores de tipo y advertencias automáticamente después de ediciones de archivo. También admite operaciones de navegación: saltar a definiciones, encontrar referencias, obtener información de tipo, listar símbolos, encontrar implementaciones, rastrear jerarquías de llamadas. Requiere un [plugin de inteligencia de código](/es/discover-plugins#code-intelligence) y su binario de servidor de lenguaje | No                |
| **NotebookEdit**         | Modifica celdas de cuaderno Jupyter                                                                                                                                                                                                                                                                                                                                                                                                                                               | Sí                |
| **Read**                 | Lee el contenido de archivos                                                                                                                                                                                                                                                                                                                                                                                                                                                      | No                |
| **ReadMcpResourceTool**  | Lee un recurso MCP específico por URI                                                                                                                                                                                                                                                                                                                                                                                                                                             | No                |
| **Skill**                | Ejecuta una [skill](/es/skills#control-who-invokes-a-skill) dentro de la conversación principal                                                                                                                                                                                                                                                                                                                                                                                   | Sí                |
| **TaskCreate**           | Crea una nueva tarea en la lista de tareas                                                                                                                                                                                                                                                                                                                                                                                                                                        | No                |
| **TaskGet**              | Recupera detalles completos para una tarea específica                                                                                                                                                                                                                                                                                                                                                                                                                             | No                |
| **TaskList**             | Lista todas las tareas con su estado actual                                                                                                                                                                                                                                                                                                                                                                                                                                       | No                |
| **TaskOutput**           | Recupera salida de una tarea de fondo                                                                                                                                                                                                                                                                                                                                                                                                                                             | No                |
| **TaskStop**             | Mata una tarea de fondo en ejecución por ID                                                                                                                                                                                                                                                                                                                                                                                                                                       | No                |
| **TaskUpdate**           | Actualiza estado de tarea, dependencias, detalles o elimina tareas                                                                                                                                                                                                                                                                                                                                                                                                                | No                |
| **TodoWrite**            | Gestiona la lista de verificación de tareas de sesión. Disponible en modo no interactivo y el [SDK de Agent](/es/headless); las sesiones interactivas usan TaskCreate, TaskGet, TaskList y TaskUpdate en su lugar                                                                                                                                                                                                                                                                 | No                |
| **ToolSearch**           | Busca y carga herramientas diferidas cuando [búsqueda de herramientas](/es/mcp#scale-with-mcp-tool-search) está habilitada                                                                                                                                                                                                                                                                                                                                                        | No                |
| **WebFetch**             | Obtiene contenido de una URL especificada                                                                                                                                                                                                                                                                                                                                                                                                                                         | Sí                |
| **WebSearch**            | Realiza búsquedas web                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Sí                |
| **Write**                | Crea o sobrescribe archivos                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Sí                |

Las reglas de permiso se pueden configurar usando `/allowed-tools` o en [configuración de permisos](/es/settings#available-settings). También consulte [Reglas de permiso específicas de herramientas](/es/permissions#tool-specific-permission-rules).

### Comportamiento de herramienta Bash

La herramienta Bash ejecuta comandos de shell con el siguiente comportamiento de persistencia:

* **El directorio de trabajo persiste**: Cuando Claude cambia el directorio de trabajo (por ejemplo, `cd /path/to/dir`), los comandos Bash posteriores se ejecutarán en ese directorio. Puede usar `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1` para volver al directorio del proyecto después de cada comando.
* **Las variables de entorno NO persisten**: Las variables de entorno establecidas en un comando Bash (por ejemplo, `export MY_VAR=value`) **no** están disponibles en comandos Bash posteriores. Cada comando Bash se ejecuta en un entorno de shell fresco.

Para hacer que las variables de entorno estén disponibles en comandos Bash, tiene **tres opciones**:

**Opción 1: Activar entorno antes de iniciar Claude Code** (enfoque más simple)

Active su entorno virtual en su terminal antes de lanzar Claude Code:

```bash  theme={null}
conda activate myenv
# o: source /path/to/venv/bin/activate
claude
```

Esto funciona para entornos de shell pero las variables de entorno establecidas dentro de los comandos Bash de Claude no persistirán entre comandos.

**Opción 2: Establecer CLAUDE\_ENV\_FILE antes de iniciar Claude Code** (configuración de entorno persistente)

Exporte la ruta a un script de shell que contiene su configuración de entorno:

```bash  theme={null}
export CLAUDE_ENV_FILE=/path/to/env-setup.sh
claude
```

Donde `/path/to/env-setup.sh` contiene:

```bash  theme={null}
conda activate myenv
# o: source /path/to/venv/bin/activate
# o: export MY_VAR=value
```

Claude Code obtendrá este archivo antes de cada comando Bash, haciendo que el entorno sea persistente en todos los comandos.

**Opción 3: Usar un hook SessionStart** (configuración específica del proyecto)

Configure en `.claude/settings.json`:

```json  theme={null}
{
  "hooks": {
    "SessionStart": [{
      "matcher": "startup",
      "hooks": [{
        "type": "command",
        "command": "echo 'conda activate myenv' >> \"$CLAUDE_ENV_FILE\""
      }]
    }]
  }
}
```

El hook escribe en `$CLAUDE_ENV_FILE`, que luego se obtiene antes de cada comando Bash. Esto es ideal para configuraciones de proyecto compartidas por el equipo.

Consulte [hooks SessionStart](/es/hooks#persist-environment-variables) para obtener más detalles sobre la Opción 3.

### Extender herramientas con hooks

Puede ejecutar comandos personalizados antes o después de que cualquier herramienta se ejecute usando [hooks de Claude Code](/es/hooks-guide).

Por ejemplo, podría ejecutar automáticamente un formateador de Python después de que Claude modifique archivos de Python, o prevenir modificaciones a archivos de configuración de producción bloqueando operaciones de Write a ciertas rutas.

## Ver también

* [Permisos](/es/permissions): sistema de permisos, sintaxis de reglas, patrones específicos de herramientas y políticas administradas
* [Autenticación](/es/authentication): configurar acceso de usuario a Claude Code
* [Solución de problemas](/es/troubleshooting): soluciones para problemas de configuración comunes
