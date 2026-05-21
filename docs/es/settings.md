> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configuración de Claude Code

> Configure Claude Code con configuraciones globales y a nivel de proyecto, y variables de entorno.

Claude Code ofrece una variedad de configuraciones para personalizar su comportamiento según sus necesidades. Puede configurar Claude Code ejecutando el comando `/config` cuando utiliza el REPL interactivo, que abre una interfaz de Configuración con pestañas donde puede ver información de estado y modificar opciones de configuración.

## Ámbitos de configuración

Claude Code utiliza un **sistema de ámbitos** para determinar dónde se aplican las configuraciones y quién las comparte. Comprender los ámbitos le ayuda a decidir cómo configurar Claude Code para uso personal, colaboración en equipo o implementación empresarial.

### Ámbitos disponibles

| Ámbito      | Ubicación                                                                                                  | A quién afecta                              | ¿Se comparte con el equipo? |
| :---------- | :--------------------------------------------------------------------------------------------------------- | :------------------------------------------ | :-------------------------- |
| **Managed** | Configuraciones administradas por servidor, plist / registro, o `managed-settings.json` a nivel de sistema | Todos los usuarios en la máquina            | Sí (implementado por TI)    |
| **User**    | Directorio `~/.claude/`                                                                                    | Usted, en todos los proyectos               | No                          |
| **Project** | `.claude/` en el repositorio                                                                               | Todos los colaboradores en este repositorio | Sí (confirmado en git)      |
| **Local**   | `.claude/settings.local.json`                                                                              | Usted, solo en este repositorio             | No (ignorado por git)       |

### Cuándo usar cada ámbito

El **ámbito Managed** es para:

* Políticas de seguridad que deben aplicarse en toda la organización
* Requisitos de cumplimiento que no se pueden anular
* Configuraciones estandarizadas implementadas por TI/DevOps

El **ámbito User** es mejor para:

* Preferencias personales que desea en todas partes (temas, configuración del editor)
* Herramientas y plugins que utiliza en todos los proyectos
* Claves API y autenticación (almacenadas de forma segura)

El **ámbito Project** es mejor para:

* Configuraciones compartidas por el equipo (permisos, hooks, MCP servers)
* Plugins que todo el equipo debe tener
* Estandarizar herramientas entre colaboradores

El **ámbito Local** es mejor para:

* Anulaciones personales para un proyecto específico
* Probar configuraciones antes de compartirlas con el equipo
* Configuraciones específicas de la máquina que no funcionarán para otros

### Cómo interactúan los ámbitos

Cuando la misma configuración aparece en múltiples ámbitos, Claude Code las aplica en orden de prioridad:

1. **Managed** (más alto) - no puede ser anulado por nada
2. **Argumentos de línea de comandos** - anulaciones de sesión temporal
3. **Local** - anula configuraciones de proyecto y usuario
4. **Project** - anula configuraciones de usuario
5. **User** (más bajo) - se aplica cuando nada más especifica la configuración

Por ejemplo, si la configuración de usuario establece `spinnerTipsEnabled` en `true` y la configuración de proyecto lo establece en `false`, se aplica el valor del proyecto. Las reglas de permisos se comportan de manera diferente porque se fusionan en todos los ámbitos en lugar de anular. Consulte [Precedencia de configuración](#settings-precedence).

### Qué usa ámbitos

Los ámbitos se aplican a muchas características de Claude Code:

| Característica  | Ubicación de usuario      | Ubicación de proyecto             | Ubicación local                 |
| :-------------- | :------------------------ | :-------------------------------- | :------------------------------ |
| **Settings**    | `~/.claude/settings.json` | `.claude/settings.json`           | `.claude/settings.local.json`   |
| **Subagents**   | `~/.claude/agents/`       | `.claude/agents/`                 | Ninguno                         |
| **MCP servers** | `~/.claude.json`          | `.mcp.json`                       | `~/.claude.json` (por proyecto) |
| **Plugins**     | `~/.claude/settings.json` | `.claude/settings.json`           | `.claude/settings.local.json`   |
| **CLAUDE.md**   | `~/.claude/CLAUDE.md`     | `CLAUDE.md` o `.claude/CLAUDE.md` | `CLAUDE.local.md`               |

En Windows, las rutas mostradas como `~/.claude` se resuelven en `%USERPROFILE%\.claude`.

***

## Archivos de configuración

El archivo `settings.json` es el mecanismo oficial para configurar Claude Code a través de configuraciones jerárquicas:

* **Configuraciones de usuario** se definen en `~/.claude/settings.json` y se aplican a todos los proyectos.
* **Configuraciones de proyecto** se guardan en su directorio de proyecto:
  * `.claude/settings.json` para configuraciones que se verifican en el control de código fuente y se comparten con su equipo
  * `.claude/settings.local.json` para configuraciones que no se verifican, útil para preferencias personales y experimentación. Claude Code configurará git para ignorar `.claude/settings.local.json` cuando se cree.
* **Configuraciones administradas**: Para organizaciones que necesitan control centralizado, Claude Code admite múltiples mecanismos de entrega para configuraciones administradas. Todos utilizan el mismo formato JSON y no pueden ser anulados por configuraciones de usuario o proyecto:

  * **Configuraciones administradas por servidor**: entregadas desde los servidores de Anthropic a través de la consola de administración de Claude.ai. Consulte [configuraciones administradas por servidor](/es/server-managed-settings).
  * **Políticas de MDM/nivel de SO**: entregadas a través de administración de dispositivos nativa en macOS y Windows:
    * macOS: dominio de preferencias administradas `com.anthropic.claudecode`. El plist de nivel superior refleja las claves de `managed-settings.json`, con configuraciones anidadas como diccionarios y matrices como matrices de plist. Implemente a través de perfiles de configuración en Jamf, Iru (Kandji) u herramientas MDM similares.
    * Windows: clave de registro `HKLM\SOFTWARE\Policies\ClaudeCode` con un valor `Settings` (REG\_SZ o REG\_EXPAND\_SZ) que contiene JSON (implementado a través de Política de grupo o Intune)
    * Windows (nivel de usuario): `HKCU\SOFTWARE\Policies\ClaudeCode` (prioridad de política más baja, solo se usa cuando no existe una fuente a nivel de administrador)
  * **Basado en archivos**: `managed-settings.json` y `managed-mcp.json` implementados en directorios del sistema:

    * macOS: `/Library/Application Support/ClaudeCode/`
    * Linux y WSL: `/etc/claude-code/`
    * Windows: `C:\Program Files\ClaudeCode\`

    <Warning>
      La ruta heredada de Windows `C:\ProgramData\ClaudeCode\managed-settings.json` ya no se admite a partir de v2.1.75. Los administradores que implementaron configuraciones en esa ubicación deben migrar archivos a `C:\Program Files\ClaudeCode\managed-settings.json`.
    </Warning>

    Las configuraciones administradas basadas en archivos también admiten un directorio de entrega en `managed-settings.d/` en el mismo directorio del sistema junto a `managed-settings.json`. Esto permite que equipos separados implementen fragmentos de política independientes sin coordinar ediciones a un único archivo.

    Siguiendo la convención de systemd, `managed-settings.json` se fusiona primero como base, luego todos los archivos `*.json` en el directorio de entrega se ordenan alfabéticamente y se fusionan encima. Los archivos posteriores anulan los anteriores para valores escalares; las matrices se concatenan y se deduplicán; los objetos se fusionan profundamente. Se ignoran los archivos ocultos que comienzan con `.`.

    Use prefijos numéricos para controlar el orden de fusión, por ejemplo `10-telemetry.json` y `20-security.json`.

  Consulte [configuraciones administradas](/es/permissions#managed-only-settings) y [Configuración de MCP administrada](/es/mcp#managed-mcp-configuration) para obtener detalles.

  Este [repositorio](https://github.com/anthropics/claude-code/tree/main/examples/mdm) incluye plantillas de implementación de inicio para Jamf, Iru (Kandji), Intune y Política de grupo. Use estas como puntos de partida y ajústelas para que se adapten a sus necesidades.

  <Note>
    Las implementaciones administradas también pueden restringir **adiciones de marketplace de plugins** usando `strictKnownMarketplaces`. Para obtener más información, consulte [Restricciones de marketplace administradas](/es/plugin-marketplaces#managed-marketplace-restrictions).
  </Note>
* **Otra configuración** se almacena en `~/.claude.json`. Este archivo contiene su sesión OAuth, configuraciones de [MCP server](/es/mcp) para ámbitos de usuario y local, estado por proyecto (herramientas permitidas, configuración de confianza) y varios cachés. Los MCP servers con ámbito de proyecto se almacenan por separado en `.mcp.json`.

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

El esquema publicado se actualiza periódicamente y puede no incluir configuraciones agregadas en los lanzamientos de CLI más recientes, por lo que una advertencia de validación en un campo documentado recientemente no necesariamente significa que su configuración sea inválida.

### Cuándo entran en vigor las ediciones

Claude Code observa sus archivos de configuración y los recarga cuando cambian, por lo que las ediciones en la mayoría de las claves se aplican a la sesión en ejecución sin necesidad de reinicio. Esto incluye `permissions`, `hooks` y asistentes de credenciales como `apiKeyHelper`. La recarga cubre configuraciones de usuario, proyecto, local y administradas, y el [hook `ConfigChange`](/es/hooks#configchange) se activa para cada cambio detectado.

Algunas claves se leen una sola vez al inicio de la sesión y se aplican en el siguiente reinicio:

* `model`: use [`/model`](/es/model-config#setting-your-model) para cambiar en mitad de sesión
* [`outputStyle`](/es/output-styles): parte del indicador del sistema, que se reconstruye en `/clear` o reinicio

### Configuraciones disponibles

`settings.json` admite varias opciones:

| Clave                             | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Ejemplo                                                                                                                       |
| :-------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---------------------------------------------------------------------------------------------------------------------------- |
| `agent`                           | Ejecutar el hilo principal como un subagent nombrado. Aplica el indicador del sistema del subagent, restricciones de herramientas y modelo. Consulte [Invocar subagents explícitamente](/es/sub-agents#invoke-subagents-explicitly)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `"code-reviewer"`                                                                                                             |
| `allowedChannelPlugins`           | (Solo configuraciones administradas) Lista blanca de plugins de canal que pueden enviar mensajes. Reemplaza la lista blanca predeterminada de Anthropic cuando se establece. Sin definir = recurrir a la predeterminada, matriz vacía = bloquear todos los plugins de canal. Requiere `channelsEnabled: true`. Consulte [Restringir qué plugins de canal pueden ejecutarse](/es/channels#restrict-which-channel-plugins-can-run)                                                                                                                                                                                                                                                                                                                                    | `[{ "marketplace": "claude-plugins-official", "plugin": "telegram" }]`                                                        |
| `allowedHttpHookUrls`             | Lista blanca de patrones de URL que los hooks HTTP pueden dirigirse. Admite `*` como comodín. Cuando se establece, los hooks con URLs que no coinciden se bloquean. Sin definir = sin restricción, matriz vacía = bloquear todos los hooks HTTP. Las matrices se fusionan entre fuentes de configuración. Consulte [Configuración de hooks](#hook-configuration)                                                                                                                                                                                                                                                                                                                                                                                                    | `["https://hooks.example.com/*"]`                                                                                             |
| `allowedMcpServers`               | Cuando se establece en managed-settings.json, lista blanca de MCP servers que los usuarios pueden configurar. Sin definir = sin restricciones, matriz vacía = bloqueo. Se aplica a todos los ámbitos. La lista de denegación tiene precedencia. Consulte [Configuración de MCP administrada](/es/mcp#managed-mcp-configuration)                                                                                                                                                                                                                                                                                                                                                                                                                                     | `[{ "serverName": "github" }]`                                                                                                |
| `allowManagedHooksOnly`           | (Solo configuraciones administradas) Solo se cargan hooks administrados, hooks SDK y hooks de plugins forzadamente habilitados en la configuración administrada `enabledPlugins`. Se bloquean hooks de usuario, proyecto y todos los demás plugins. Consulte [Configuración de hooks](#hook-configuration)                                                                                                                                                                                                                                                                                                                                                                                                                                                          | `true`                                                                                                                        |
| `allowManagedMcpServersOnly`      | (Solo configuraciones administradas) Solo se respetan `allowedMcpServers` de configuraciones administradas. `deniedMcpServers` aún se fusiona desde todas las fuentes. Los usuarios aún pueden agregar MCP servers, pero solo se aplica la lista blanca definida por el administrador. Consulte [Configuración de MCP administrada](/es/mcp#managed-mcp-configuration)                                                                                                                                                                                                                                                                                                                                                                                              | `true`                                                                                                                        |
| `allowManagedPermissionRulesOnly` | (Solo configuraciones administradas) Evitar que configuraciones de usuario y proyecto definan reglas de permiso `allow`, `ask` o `deny`. Solo se aplican las reglas en configuraciones administradas. Consulte [Configuraciones solo administradas](/es/permissions#managed-only-settings)                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | `true`                                                                                                                        |
| `alwaysThinkingEnabled`           | Habilitar [pensamiento extendido](/es/model-config#extended-thinking) de forma predeterminada para todas las sesiones. Típicamente configurado a través del comando `/config` en lugar de editar directamente. Para forzar el pensamiento desactivado independientemente de esta configuración, establezca [`CLAUDE_CODE_DISABLE_THINKING`](/es/env-vars) en `env`                                                                                                                                                                                                                                                                                                                                                                                                  | `true`                                                                                                                        |
| `apiKeyHelper`                    | Script personalizado, a ejecutarse en `/bin/sh`, para generar un valor de autenticación. Este valor se enviará como encabezados `X-Api-Key` y `Authorization: Bearer` para solicitudes de modelo. Establezca el intervalo de actualización con [`CLAUDE_CODE_API_KEY_HELPER_TTL_MS`](/es/env-vars)                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | `/bin/generate_temp_api_key.sh`                                                                                               |
| `attribution`                     | Personalizar atribución para commits de git y solicitudes de extracción. Consulte [Configuración de atribución](#attribution-settings)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `{"commit": "🤖 Generated with Claude Code", "pr": ""}`                                                                       |
| `autoMemoryDirectory`             | Directorio personalizado para almacenamiento de [memoria automática](/es/memory#storage-location). Acepta una ruta absoluta o una ruta con prefijo `~/`. Se acepta desde configuraciones de política y usuario, y desde la bandera `--settings`. No se acepta desde configuraciones de proyecto o local, ya que un repositorio clonado podría proporcionar cualquiera de los archivos para redirigir escrituras de memoria a ubicaciones sensibles                                                                                                                                                                                                                                                                                                                  | `"~/my-memory-dir"`                                                                                                           |
| `autoMemoryEnabled`               | Habilitar [memoria automática](/es/memory#enable-or-disable-auto-memory). Cuando es `false`, Claude no lee ni escribe en el directorio de memoria automática. Predeterminado: `true`. También puede alternar esto con `/memory` durante una sesión. Para deshabilitar a través de variable de entorno, establezca [`CLAUDE_CODE_DISABLE_AUTO_MEMORY`](/es/env-vars) en `env`                                                                                                                                                                                                                                                                                                                                                                                        | `false`                                                                                                                       |
| `autoMode`                        | Personalizar qué bloquea y permite el clasificador de [modo automático](/es/permission-modes#eliminate-prompts-with-auto-mode). Contiene matrices `environment`, `allow`, `soft_deny` y `hard_deny` de reglas en prosa. Incluya la cadena literal `"$defaults"` en una matriz para heredar las reglas integradas en esa posición. Consulte [Configurar modo automático](/es/auto-mode-config). No se lee desde configuraciones de proyecto compartidas                                                                                                                                                                                                                                                                                                              | `{"soft_deny": ["$defaults", "Never run terraform apply"]}`                                                                   |
| `autoScrollEnabled`               | En [renderizado de pantalla completa](/es/fullscreen), seguir la nueva salida hasta el final de la conversación. Predeterminado: `true`. Aparece en `/config` como **Auto-scroll**. Los avisos de permiso aún se desplazan a la vista cuando esto está desactivado                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | `false`                                                                                                                       |
| `autoUpdatesChannel`              | Canal de lanzamiento a seguir para actualizaciones. Use `"stable"` para una versión que típicamente tiene aproximadamente una semana de antigüedad y omite versiones con regresiones importantes, o `"latest"` (predeterminado) para el lanzamiento más reciente. Para deshabilitar completamente las actualizaciones automáticas, establezca [`DISABLE_AUTOUPDATER`](/es/setup#disable-auto-updates) en `env`                                                                                                                                                                                                                                                                                                                                                      | `"stable"`                                                                                                                    |
| `availableModels`                 | Restringir qué modelos pueden seleccionar los usuarios a través de `/model`, `--model`, o `ANTHROPIC_MODEL`. No afecta la opción Predeterminado. Consulte [Restringir selección de modelo](/es/model-config#restrict-model-selection)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `["sonnet", "haiku"]`                                                                                                         |
| `awaySummaryEnabled`              | Mostrar un resumen de sesión de una línea cuando regresa a la terminal después de estar ausente unos minutos. Establezca en `false` o desactive Resumen de sesión en `/config` para deshabilitar. Igual que [`CLAUDE_CODE_ENABLE_AWAY_SUMMARY`](/es/env-vars)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | `true`                                                                                                                        |
| `awsAuthRefresh`                  | Script personalizado que modifica el directorio `.aws` (consulte [configuración avanzada de credenciales](/es/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `aws sso login --profile myprofile`                                                                                           |
| `awsCredentialExport`             | Script personalizado que genera JSON con credenciales de AWS (consulte [configuración avanzada de credenciales](/es/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `/bin/generate_aws_grant.sh`                                                                                                  |
| `blockedMarketplaces`             | (Solo configuraciones administradas) Lista negra de fuentes de marketplace. Aplicada en adición de marketplace y en instalación, actualización, actualización y auto-actualización de plugins, por lo que un marketplace agregado antes de que se estableciera la política no puede usarse para obtener plugins. Las fuentes bloqueadas se verifican antes de descargar, por lo que nunca tocan el sistema de archivos. Consulte [Restricciones de marketplace administradas](/es/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                                                                                                                             | `[{ "source": "github", "repo": "untrusted/plugins" }]`                                                                       |
| `channelsEnabled`                 | (Solo configuraciones administradas) Permitir [canales](/es/channels) para la organización. En planes de Claude.ai Team y Enterprise, los canales se bloquean cuando esto no está definido o es `false`. Para cuentas de [Anthropic Console](/es/authentication#claude-console-authentication) que usan autenticación de clave API, los canales se permiten de forma predeterminada a menos que su organización implemente configuraciones administradas, en cuyo caso esta clave debe establecerse en `true`                                                                                                                                                                                                                                                       | `true`                                                                                                                        |
| `claudeMd`                        | (Solo configuraciones administradas) Instrucciones de estilo CLAUDE.md inyectadas como memoria administrada por la organización. Solo se honra cuando se establece en configuraciones administradas o de política e ignorado en configuraciones de usuario, proyecto y local. Consulte [CLAUDE.md en toda la organización](/es/memory#deploy-organization-wide-claude-md)                                                                                                                                                                                                                                                                                                                                                                                           | `"Always run make lint before committing."`                                                                                   |
| `claudeMdExcludes`                | Patrones Glob o rutas absolutas de archivos `CLAUDE.md` a omitir al cargar [memoria](/es/memory). Los patrones coinciden con rutas de archivo absolutas. Solo se aplica a memoria de usuario, proyecto y local; los archivos de política administrada no pueden excluirse                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | `["**/vendor/**/CLAUDE.md"]`                                                                                                  |
| `cleanupPeriodDays`               | Las sesiones inactivas durante más tiempo que este período se eliminan al inicio (predeterminado: 30 días, mínimo 1). Establecer en `0` se rechaza con un error de validación. También controla el corte de edad para la eliminación automática de [worktrees de subagent huérfanos](/es/worktrees#clean-up-worktrees) al inicio. Para deshabilitar completamente las escrituras de transcripción, establezca la variable de entorno [`CLAUDE_CODE_SKIP_PROMPT_HISTORY`](/es/env-vars), o en modo no interactivo (`-p`) use la bandera `--no-session-persistence` o la opción SDK `persistSession: false`.                                                                                                                                                          | `20`                                                                                                                          |
| `companyAnnouncements`            | Anuncio a mostrar a los usuarios al inicio. Si se proporcionan múltiples anuncios, se alternarán aleatoriamente.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `["Welcome to Acme Corp! Review our code guidelines at docs.acme.com"]`                                                       |
| `defaultShell`                    | Shell predeterminado para comandos `!` de cuadro de entrada. Acepta `"bash"` (predeterminado) o `"powershell"`. Establecer `"powershell"` enruta comandos `!` interactivos a través de PowerShell en Windows. Requiere `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`. Consulte [herramienta PowerShell](/es/tools-reference#powershell-tool)                                                                                                                                                                                                                                                                                                                                                                                                                                  | `"powershell"`                                                                                                                |
| `deniedMcpServers`                | Cuando se establece en managed-settings.json, lista negra de MCP servers que están explícitamente bloqueados. Se aplica a todos los ámbitos incluyendo servers administrados. La lista de denegación tiene precedencia sobre la lista blanca. Consulte [Configuración de MCP administrada](/es/mcp#managed-mcp-configuration)                                                                                                                                                                                                                                                                                                                                                                                                                                       | `[{ "serverName": "filesystem" }]`                                                                                            |
| `disableAgentView`                | Establecer en `true` para desactivar [agentes de fondo y vista de agentes](/es/agent-view): `claude agents`, `--bg`, `/background` y el supervisor bajo demanda. Típicamente establecido en [configuraciones administradas](/es/permissions#managed-settings). Equivalente a establecer `CLAUDE_CODE_DISABLE_AGENT_VIEW` en `1`                                                                                                                                                                                                                                                                                                                                                                                                                                     | `true`                                                                                                                        |
| `disableAllHooks`                 | Deshabilitar todos los [hooks](/es/hooks) y cualquier [línea de estado](/es/statusline) personalizada                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `true`                                                                                                                        |
| `disableAutoMode`                 | Establecer en `"disable"` para evitar que se active el [modo automático](/es/permission-modes#eliminate-prompts-with-auto-mode). Elimina `auto` del ciclo `Shift+Tab` y rechaza `--permission-mode auto` al inicio. Más útil en [configuraciones administradas](/es/permissions#managed-settings) donde los usuarios no pueden anularlo                                                                                                                                                                                                                                                                                                                                                                                                                             | `"disable"`                                                                                                                   |
| `disableDeepLinkRegistration`     | Establecer en `"disable"` para evitar que Claude Code registre el controlador de protocolo `claude-cli://` con el sistema operativo al inicio. Los [enlaces profundos](/es/deep-links) permiten que herramientas externas abran una sesión de Claude Code con un indicador rellenado previamente. Útil en entornos donde el registro del controlador de protocolo está restringido o se gestiona por separado                                                                                                                                                                                                                                                                                                                                                       | `"disable"`                                                                                                                   |
| `disabledMcpjsonServers`          | Lista de MCP servers específicos de archivos `.mcp.json` para rechazar                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `["filesystem"]`                                                                                                              |
| `disableRemoteControl`            | {/* min-version: 2.1.128 */}Deshabilitar [Control Remoto](/es/remote-control): bloquea `claude remote-control`, la bandera `--remote-control`, auto-inicio y el toggle en sesión. Típicamente colocado en [configuraciones administradas](/es/permissions#managed-settings) para aplicación de MDM por dispositivo, pero funciona desde cualquier ámbito. Requiere Claude Code v2.1.128 o posterior                                                                                                                                                                                                                                                                                                                                                                 | `true`                                                                                                                        |
| `disableSkillShellExecution`      | Deshabilitar la ejecución de shell en línea para bloques `` !`...` `` y ` ```! ` en [skills](/es/skills) y comandos personalizados de fuentes de usuario, proyecto, plugin o directorio adicional. Los comandos se reemplazan con `[shell command execution disabled by policy]` en lugar de ejecutarse. Los skills agrupados y administrados no se ven afectados. Más útil en [configuraciones administradas](/es/permissions#managed-settings) donde los usuarios no pueden anularlo                                                                                                                                                                                                                                                                              | `true`                                                                                                                        |
| `editorMode`                      | Modo de atajos de teclado para el indicador de entrada: `"normal"` o `"vim"`. Predeterminado: `"normal"`. Aparece en `/config` como **Editor mode**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `"vim"`                                                                                                                       |
| `effortLevel`                     | Persistir el [nivel de esfuerzo](/es/model-config#adjust-effort-level) entre sesiones. Acepta `"low"`, `"medium"`, `"high"`, o `"xhigh"`. Se escribe automáticamente cuando ejecuta `/effort` con uno de esos valores. `--effort` y [`CLAUDE_CODE_EFFORT_LEVEL`](/es/env-vars) anulan esto para una sesión. Consulte [Ajustar nivel de esfuerzo](/es/model-config#adjust-effort-level) para modelos compatibles                                                                                                                                                                                                                                                                                                                                                     | `"xhigh"`                                                                                                                     |
| `enableAllProjectMcpServers`      | Aprobar automáticamente todos los MCP servers definidos en archivos `.mcp.json` de proyecto                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | `true`                                                                                                                        |
| `enabledMcpjsonServers`           | Lista de MCP servers específicos de archivos `.mcp.json` para aprobar                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `["memory", "github"]`                                                                                                        |
| `env`                             | Variables de entorno aplicadas a cada sesión y a subprocesos que Claude Code genera desde ella. {/* min-version: 2.1.143 */}A partir de v2.1.143, `NO_COLOR` y `FORCE_COLOR` establecidos aquí se pasan a subprocesos pero no cambian los colores de la interfaz propia de Claude Code. Establezca esos en su shell antes de lanzar `claude` para cambiar los colores de la interfaz                                                                                                                                                                                                                                                                                                                                                                                | `{"FOO": "bar"}`                                                                                                              |
| `fastModePerSessionOptIn`         | Cuando es `true`, el modo rápido no persiste entre sesiones. Cada sesión comienza con el modo rápido desactivado, requiriendo que los usuarios lo habiliten con `/fast`. La preferencia de modo rápido del usuario aún se guarda. Consulte [Requerir opt-in por sesión](/es/fast-mode#require-per-session-opt-in)                                                                                                                                                                                                                                                                                                                                                                                                                                                   | `true`                                                                                                                        |
| `feedbackSurveyRate`              | Probabilidad (0–1) de que la [encuesta de calidad de sesión](/es/data-usage#session-quality-surveys) aparezca cuando sea elegible. Establecer en `0` para suprimir completamente, o establezca [`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY`](/es/env-vars) en `env`. Útil cuando se usa Bedrock, Vertex, o Foundry donde la tasa de muestreo predeterminada no se aplica                                                                                                                                                                                                                                                                                                                                                                                                  | `0.05`                                                                                                                        |
| `fileSuggestion`                  | Configurar un script personalizado para autocompletado de archivo `@`. Consulte [Configuración de sugerencia de archivo](#file-suggestion-settings)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `{"type": "command", "command": "~/.claude/file-suggestion.sh"}`                                                              |
| `forceLoginMethod`                | Use `claudeai` para restringir el inicio de sesión a cuentas de Claude.ai, `console` para restringir el inicio de sesión a cuentas de Claude Console (facturación de uso de API)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `claudeai`                                                                                                                    |
| `forceLoginOrgUUID`               | Requerir que el inicio de sesión pertenezca a una organización específica. Acepta una cadena UUID única, que también preselecciona esa organización durante el inicio de sesión, o una matriz de UUID donde se acepta cualquier organización listada sin preselección. Cuando se establece en configuraciones administradas, el inicio de sesión falla si la cuenta autenticada no pertenece a una organización listada; una matriz vacía falla cerrada y bloquea el inicio de sesión con un mensaje de configuración incorrecta                                                                                                                                                                                                                                    | `"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"` o `["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"]` |
| `forceRemoteSettingsRefresh`      | (Solo configuraciones administradas) Bloquear el inicio de CLI hasta que se obtengan configuraciones administradas remotas recientemente del servidor. Si la obtención falla, la CLI se cierra en lugar de continuar con configuraciones en caché o sin configuraciones. Cuando no se establece, el inicio continúa sin esperar configuraciones remotas. Consulte [aplicación de cierre de falla](/es/server-managed-settings#enforce-fail-closed-startup)                                                                                                                                                                                                                                                                                                          | `true`                                                                                                                        |
| `gcpAuthRefresh`                  | Script personalizado que actualiza las Credenciales Predeterminadas de Aplicación de GCP cuando expiran o no se pueden cargar. Consulte [configuración avanzada de credenciales](/es/google-vertex-ai#advanced-credential-configuration)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `gcloud auth application-default login`                                                                                       |
| `hooks`                           | Configurar comandos personalizados para ejecutarse en eventos del ciclo de vida. Consulte [documentación de hooks](/es/hooks) para el formato                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Consulte [hooks](/es/hooks)                                                                                                   |
| `httpHookAllowedEnvVars`          | Lista blanca de nombres de variables de entorno que los hooks HTTP pueden interpolar en encabezados. Cuando se establece, el `allowedEnvVars` efectivo de cada hook es la intersección con esta lista. Sin definir = sin restricción. Las matrices se fusionan entre fuentes de configuración. Consulte [Configuración de hooks](#hook-configuration)                                                                                                                                                                                                                                                                                                                                                                                                               | `["MY_TOKEN", "HOOK_SECRET"]`                                                                                                 |
| `includeCoAuthoredBy`             | **Obsoleto**: Use `attribution` en su lugar. Si incluir la línea `co-authored-by Claude` en commits de git y solicitudes de extracción (predeterminado: `true`)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `false`                                                                                                                       |
| `includeGitInstructions`          | Incluir instrucciones de flujo de trabajo de commit y PR integradas y la instantánea de estado de git en el indicador del sistema de Claude (predeterminado: `true`). Establecer en `false` para eliminar ambas, por ejemplo cuando se usan skills de flujo de trabajo de git personalizados. La variable de entorno `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` tiene precedencia sobre esta configuración cuando se establece                                                                                                                                                                                                                                                                                                                                          | `false`                                                                                                                       |
| `language`                        | Configurar el idioma de respuesta preferido de Claude (por ejemplo, `"japanese"`, `"spanish"`, `"french"`). Claude responderá en este idioma de forma predeterminada. También establece el idioma de [dictado de voz](/es/voice-dictation#change-the-dictation-language)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `"japanese"`                                                                                                                  |
| `maxSkillDescriptionChars`        | {/* min-version: 2.1.105 */}Límite de caracteres por skill en el texto combinado de `description` y `when_to_use` en el [listado de skills](/es/skills#skill-descriptions-are-cut-short) que Claude ve cada turno (predeterminado: `1536`). El texto más largo que esto se trunca. Aumente para mantener descripciones largas intactas al costo de más contexto por turno; disminuya para ajustar más skills bajo [`skillListingBudgetFraction`](#available-settings). Requiere Claude Code v2.1.105 o posterior                                                                                                                                                                                                                                                    | `2048`                                                                                                                        |
| `minimumVersion`                  | Piso que evita que las actualizaciones automáticas en segundo plano e `claude update` instalen una versión por debajo de esta. Cambiar del canal `"latest"` a `"stable"` a través de `/config` le solicita que permanezca en la versión actual o permita la degradación. Elegir permanecer establece este valor. También útil en [configuraciones administradas](/es/permissions#managed-settings) para fijar un mínimo en toda la organización                                                                                                                                                                                                                                                                                                                     | `"2.1.100"`                                                                                                                   |
| `model`                           | Anular el modelo predeterminado a usar para Claude Code. `--model` y [`ANTHROPIC_MODEL`](/es/model-config#environment-variables) anulan esto para una sesión                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | `"claude-sonnet-4-6"`                                                                                                         |
| `modelOverrides`                  | Asignar IDs de modelo de Anthropic a IDs de modelo específicos del proveedor como ARNs de perfil de inferencia de Bedrock. Cada entrada del selector de modelo usa su valor asignado al llamar a la API del proveedor. Consulte [Anular IDs de modelo por versión](/es/model-config#override-model-ids-per-version)                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `{"claude-opus-4-6": "arn:aws:bedrock:..."}`                                                                                  |
| `otelHeadersHelper`               | Script para generar encabezados dinámicos de OpenTelemetry. Se ejecuta al inicio y periódicamente. Establezca el intervalo de actualización con [`CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`](/es/env-vars). Consulte [Encabezados dinámicos](/es/monitoring-usage#dynamic-headers)                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `/bin/generate_otel_headers.sh`                                                                                               |
| `outputStyle`                     | Configurar un estilo de salida para ajustar el indicador del sistema. Consulte [documentación de estilos de salida](/es/output-styles)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `"Explanatory"`                                                                                                               |
| `parentSettingsBehavior`          | {/* min-version: 2.1.133 */}(Solo configuraciones administradas) Controla si las configuraciones administradas suministradas programáticamente por un proceso host de incrustación, como el Agent SDK o una extensión IDE, se aplican cuando también está presente un nivel administrado implementado por administrador. `"first-wins"`: las configuraciones suministradas por el padre se descartan y solo se aplica el nivel administrado. `"merge"`: las configuraciones suministradas por el padre se aplican bajo el nivel administrado, filtradas para que puedan restringir la política pero no flexibilizarla. No tiene efecto cuando no se implementa ningún nivel administrado. Predeterminado: `"first-wins"`. Requiere Claude Code v2.1.133 o posterior | `"merge"`                                                                                                                     |
| `permissions`                     | Consulte la tabla a continuación para la estructura de permisos.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |                                                                                                                               |
| `plansDirectory`                  | Personalizar dónde se almacenan los archivos de plan. La ruta es relativa a la raíz del proyecto. Predeterminado: `~/.claude/plans`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `"./plans"`                                                                                                                   |
| `pluginTrustMessage`              | (Solo configuraciones administradas) Mensaje personalizado agregado a la advertencia de confianza de plugin mostrada antes de la instalación. Use esto para agregar contexto específico de la organización, por ejemplo para confirmar que los plugins de su marketplace interno están verificados.                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `"All plugins from our marketplace are approved by IT"`                                                                       |
| `policyHelper`                    | {/* min-version: 2.1.136 */}Ejecutable implementado por administrador que calcula configuraciones administradas dinámicamente al inicio. Solo se honra desde MDM o un archivo `managed-settings.json` del sistema. Consulte [Calcular configuraciones administradas con un asistente de política](#compute-managed-settings-with-a-policy-helper). Requiere Claude Code v2.1.136 o posterior                                                                                                                                                                                                                                                                                                                                                                        | `{"path": "/usr/local/bin/claude-policy"}`                                                                                    |
| `preferredNotifChannel`           | Método para notificaciones de tarea completada y solicitud de permiso: `"auto"`, `"terminal_bell"`, `"iterm2"`, `"iterm2_with_bell"`, `"kitty"`, `"ghostty"`, o `"notifications_disabled"`. Predeterminado: `"auto"`, que envía una notificación de escritorio en iTerm2, Ghostty y Kitty y no hace nada en otras terminales. Establezca `"terminal_bell"` para sonar el carácter de campana en cualquier terminal. Aparece en `/config` como **Notifications**. Consulte [Obtener una campana de terminal o notificación](/es/terminal-config#get-a-terminal-bell-or-notification)                                                                                                                                                                                 | `"terminal_bell"`                                                                                                             |
| `prefersReducedMotion`            | Reducir o deshabilitar animaciones de UI (spinners, shimmer, efectos flash) para accesibilidad                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | `true`                                                                                                                        |
| `prUrlTemplate`                   | Plantilla de URL para la insignia de PR mostrada en el pie de página y en resúmenes de resultados de herramientas. Sustituye `{host}`, `{owner}`, `{repo}`, `{number}` y `{url}` de la URL de PR reportada por `gh`. Use para apuntar enlaces de PR a una herramienta de revisión de código interna en lugar de `github.com`. No afecta autolinks `#123` en la prosa de Claude                                                                                                                                                                                                                                                                                                                                                                                      | `"https://reviews.example.com/{owner}/{repo}/pull/{number}"`                                                                  |
| `respectGitignore`                | Controlar si el selector de archivo `@` respeta patrones `.gitignore`. Cuando es `true` (predeterminado), los archivos que coinciden con patrones `.gitignore` se excluyen de las sugerencias                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | `false`                                                                                                                       |
| `showClearContextOnPlanAccept`    | Mostrar la opción "borrar contexto" en la pantalla de aceptación del plan. Predeterminado: `false`. Establecer en `true` para restaurar la opción                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | `true`                                                                                                                        |
| `showThinkingSummaries`           | Mostrar resúmenes de [pensamiento extendido](/es/model-config#extended-thinking) en sesiones interactivas. Cuando no está definido o es `false` (predeterminado en modo interactivo), los bloques de pensamiento se redactan por la API y se muestran como un stub contraído. La redacción solo cambia lo que ve, no lo que genera el modelo: para reducir el gasto de pensamiento, [baje el presupuesto o deshabilite el pensamiento](/es/model-config#extended-thinking) en su lugar. Esta configuración no tiene efecto en modo no interactivo (`-p`), el Agent SDK, o extensiones IDE como VS Code                                                                                                                                                              | `true`                                                                                                                        |
| `showTurnDuration`                | Mostrar mensajes de duración de turno después de respuestas, por ejemplo "Cooked for 1m 6s". Predeterminado: `true`. Aparece en `/config` como **Show turn duration**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `false`                                                                                                                       |
| `skillListingBudgetFraction`      | {/* min-version: 2.1.105 */}Fracción del contexto del modelo reservada para el [listado de skills](/es/skills#skill-descriptions-are-cut-short) que Claude ve cada turno (predeterminado: `0.01` = 1%). Cuando el listado excede el presupuesto, las descripciones de los skills menos utilizados se contraen a nombres desnudos para que Claude aún pueda invocarlos pero no verá por qué. Aumente para mantener más descripciones visibles al costo de más contexto por turno. `/doctor` muestra el recuento de truncamiento actual y qué skills se ven afectados. Requiere Claude Code v2.1.105 o posterior                                                                                                                                                      | `0.02`                                                                                                                        |
| `skillOverrides`                  | {/* min-version: 2.1.129 */}Anulaciones de visibilidad por skill con clave de nombre de skill. El valor es `"on"`, `"name-only"`, `"user-invocable-only"`, o `"off"`. Permite ocultar o contraer un skill sin editar su SKILL.md. No se aplica a skills de plugin, que se gestionan a través de `/plugin`. El menú `/skills` escribe estos en `.claude/settings.local.json`. Consulte [Anular visibilidad de skill desde configuraciones](/es/skills#override-skill-visibility-from-settings). Requiere Claude Code v2.1.129 o posterior                                                                                                                                                                                                                            | `{"legacy-context": "name-only", "deploy": "off"}`                                                                            |
| `skipWebFetchPreflight`           | Omitir la [verificación de seguridad de dominio de WebFetch](/es/data-usage#webfetch-domain-safety-check) que envía cada nombre de host solicitado a `api.anthropic.com` antes de obtener. Establecer en `true` en entornos que bloquean tráfico a Anthropic, como implementaciones de Bedrock, Vertex AI, o Foundry con salida restrictiva. Cuando se omite, WebFetch intenta cualquier URL sin consultar la lista de bloqueos                                                                                                                                                                                                                                                                                                                                     | `true`                                                                                                                        |
| `spinnerTipsEnabled`              | Mostrar consejos en el spinner mientras Claude está trabajando. Establecer en `false` para deshabilitar consejos (predeterminado: `true`)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | `false`                                                                                                                       |
| `spinnerTipsOverride`             | Anular consejos del spinner con cadenas personalizadas. `tips`: matriz de cadenas de consejo. `excludeDefault`: si es `true`, mostrar solo consejos personalizados; si es `false` o está ausente, los consejos personalizados se fusionan con consejos integrados                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | `{ "excludeDefault": true, "tips": ["Use our internal tool X"] }`                                                             |
| `spinnerVerbs`                    | Personalizar los verbos de acción mostrados mientras un turno está en progreso. Establezca `mode` en `"replace"` para usar solo sus verbos, o `"append"` para agregarlos a los predeterminados                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | `{"mode": "append", "verbs": ["Pondering", "Crafting"]}`                                                                      |
| `sshConfigs`                      | Conexiones SSH a mostrar en el menú desplegable de entorno de [Desktop](/es/desktop#pre-configure-ssh-connections-for-your-team). Cada entrada requiere `id`, `name` y `sshHost`; `sshPort`, `sshIdentityFile` y `startDirectory` son opcionales. Cuando se establece en configuraciones administradas, las conexiones son de solo lectura para los usuarios. Se lee desde configuraciones administradas y de usuario solamente                                                                                                                                                                                                                                                                                                                                     | `[{"id": "dev-vm", "name": "Dev VM", "sshHost": "user@dev.example.com"}]`                                                     |
| `statusLine`                      | Configurar una línea de estado personalizada para mostrar contexto. Consulte [documentación de `statusLine`](/es/statusline)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | `{"type": "command", "command": "~/.claude/statusline.sh"}`                                                                   |
| `strictKnownMarketplaces`         | (Solo configuraciones administradas) Lista blanca de fuentes de marketplace de plugins. Sin definir = sin restricciones, matriz vacía = bloqueo. Aplicada en adición de marketplace y en instalación, actualización, actualización y auto-actualización de plugins, por lo que un marketplace agregado antes de que se estableciera la política no puede usarse para obtener plugins. Consulte [Restricciones de marketplace administradas](/es/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                                                                                                                                                               | `[{ "source": "github", "repo": "acme-corp/plugins" }]`                                                                       |
| `strictPluginOnlyCustomization`   | (Solo configuraciones administradas) Bloquear skills, agents, hooks y MCP servers de fuentes de usuario y proyecto, para que solo puedan provenir de plugins o configuraciones administradas. `true` bloquea las cuatro superficies; una matriz bloquea solo las nombradas. Consulte [`strictPluginOnlyCustomization`](#strictpluginonlycustomization)                                                                                                                                                                                                                                                                                                                                                                                                              | `["skills", "hooks"]`                                                                                                         |
| `syntaxHighlightingDisabled`      | Deshabilitar resaltado de sintaxis en diffs, bloques de código y vistas previas de archivos                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | `true`                                                                                                                        |
| `teammateMode`                    | Cómo se muestran los compañeros de [equipo de agentes](/es/agent-teams): `auto` (elige paneles divididos en tmux o iTerm2, en proceso de otra manera), `in-process`, o `tmux`. `--teammate-mode` anula esto para una sesión. Consulte [elegir un modo de visualización](/es/agent-teams#choose-a-display-mode)                                                                                                                                                                                                                                                                                                                                                                                                                                                      | `"in-process"`                                                                                                                |
| `terminalProgressBarEnabled`      | Mostrar la barra de progreso del terminal en terminales compatibles: ConEmu, Ghostty 1.2.0+, e iTerm2 3.6.6+. Predeterminado: `true`. Aparece en `/config` como **Terminal progress bar**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | `false`                                                                                                                       |
| `tui`                             | Renderizador de interfaz de usuario de terminal. Use `"fullscreen"` para el renderizador [alt-screen](/es/fullscreen) sin parpadeos con scrollback virtualizado. Use `"default"` para el renderizador clásico de pantalla principal. Establezca a través de `/tui`. También puede establecer la variable de entorno [`CLAUDE_CODE_NO_FLICKER`](/es/env-vars)                                                                                                                                                                                                                                                                                                                                                                                                        | `"fullscreen"`                                                                                                                |
| `useAutoModeDuringPlan`           | Si el modo de plan usa semántica de modo automático cuando el modo automático está disponible. Predeterminado: `true`. No se lee desde configuraciones de proyecto compartidas. Aparece en `/config` como "Use auto mode during plan"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `false`                                                                                                                       |
| `viewMode`                        | Modo de vista de transcripción predeterminado al inicio: `"default"`, `"verbose"`, o `"focus"`. Anula la selección pegajosa de `/focus` cuando se establece. La bandera `--verbose` anula esto para una sesión                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | `"verbose"`                                                                                                                   |
| `voice`                           | Configuración de [dictado de voz](/es/voice-dictation): `enabled` activa el dictado, `mode` selecciona `"hold"` o `"tap"`, y `autoSubmit` envía el indicador al soltar la tecla en modo hold. Se escribe automáticamente cuando ejecuta `/voice`. Requiere una cuenta de Claude.ai                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | `{ "enabled": true, "mode": "tap" }`                                                                                          |
| `voiceEnabled`                    | Alias heredado para `voice.enabled`. Prefiera el objeto `voice`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `true`                                                                                                                        |
| `wslInheritsWindowsSettings`      | (Solo configuraciones administradas de Windows) Cuando es `true`, Claude Code en WSL lee configuraciones administradas de la cadena de política de Windows además de `/etc/claude-code`, con fuentes de Windows teniendo prioridad. Solo se honra cuando se establece en la clave de registro HKLM o `C:\Program Files\ClaudeCode\managed-settings.json`, ambas requieren administrador de Windows para escribir. Para que la política HKCU también se aplique en WSL, la bandera debe establecerse además en HKCU mismo. No tiene efecto en Windows nativo                                                                                                                                                                                                         | `true`                                                                                                                        |

### Configuración de config global

Estas configuraciones se almacenan en `~/.claude.json` en lugar de `settings.json`. Agregarlas a `settings.json` activará un error de validación de esquema.

<Note>
  Las versiones anteriores a v2.1.119 también almacenan `autoScrollEnabled`, `editorMode`, `showTurnDuration`, `teammateMode` y `terminalProgressBarEnabled` aquí en lugar de en `settings.json`.
</Note>

| Clave                     | Descripción                                                                                                                                                                                                                                                                                                                                                                   | Ejemplo    |
| :------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------- |
| `autoConnectIde`          | Conectarse automáticamente a un IDE en ejecución cuando Claude Code se inicia desde una terminal externa. Predeterminado: `false`. Aparece en `/config` como **Auto-connect to IDE (external terminal)** cuando se ejecuta fuera de una terminal de VS Code o JetBrains. La variable de entorno [`CLAUDE_CODE_AUTO_CONNECT_IDE`](/es/env-vars) anula esto cuando se establece | `true`     |
| `autoInstallIdeExtension` | Instalar automáticamente la extensión de Claude Code IDE cuando se ejecuta desde una terminal de VS Code. Predeterminado: `true`. Aparece en `/config` como **Auto-install IDE extension** cuando se ejecuta dentro de una terminal de VS Code o JetBrains. También puede establecer la variable de entorno [`CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`](/es/env-vars)               | `false`    |
| `externalEditorContext`   | Anteponer la respuesta anterior de Claude como contexto comentado con `#` cuando abre el editor externo con `Ctrl+G`. Predeterminado: `false`. Aparece en `/config` como **Show last response in external editor**                                                                                                                                                            | `true`     |
| `teammateDefaultModel`    | Modelo predeterminado para compañeros de [equipo de agentes](/es/agent-teams) cuando el indicador de generación no especifica uno. Establezca en un alias de modelo como `"sonnet"`, o `null` para heredar la selección actual de `/model` del líder. Aparece en `/config` como **Default teammate model**                                                                    | `"sonnet"` |

### Configuración de worktrees

Configure cómo `--worktree` crea y gestiona git worktrees.

| Clave                         | Descripción                                                                                                                                                                                                                                                                                                                                                                                                  | Ejemplo                               |
| :---------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------ |
| `worktree.baseRef`            | Qué ref ramifican los nuevos worktrees. `"fresh"` (predeterminado) ramifica desde `origin/<default-branch>` para un árbol limpio que coincida con el remoto. `"head"` ramifica desde su `HEAD` local actual, por lo que los commits no enviados y el estado de rama de características están presentes en el worktree. Se aplica a `--worktree`, la herramienta `EnterWorktree` y el aislamiento de subagent | `"head"`                              |
| `worktree.symlinkDirectories` | Directorios a enlazar simbólicamente desde el repositorio principal en cada worktree para evitar duplicar directorios grandes en disco. No se enlazan directorios de forma predeterminada                                                                                                                                                                                                                    | `["node_modules", ".cache"]`          |
| `worktree.sparsePaths`        | Directorios a verificar en cada worktree a través de git sparse-checkout. Solo las rutas listadas más archivos de nivel raíz se escriben en disco, lo que es más rápido en monorepos grandes                                                                                                                                                                                                                 | `["packages/my-app", "shared/utils"]` |
| `worktree.bgIsolation`        | {/* min-version: 2.1.143 */}Modo de aislamiento para [sesiones de fondo](/es/agent-view#how-file-edits-are-isolated). `"worktree"` (predeterminado) bloquea `Edit`/`Write` en el checkout principal hasta que se llame a `EnterWorktree`. `"none"` permite que los trabajos de fondo editen la copia de trabajo directamente. Requiere Claude Code v2.1.143 o posterior                                      | `"none"`                              |

Para copiar archivos ignorados por git como `.env` en nuevos worktrees, use un [archivo `.worktreeinclude`](/es/worktrees#copy-gitignored-files-into-worktrees) en la raíz de su proyecto en lugar de una configuración.

### Configuración de permisos

| Claves                              | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Ejemplo                                                                |
| :---------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `allow`                             | Matriz de reglas de permiso para permitir el uso de herramientas. Consulte [Sintaxis de regla de permiso](#permission-rule-syntax) a continuación para detalles de coincidencia de patrones                                                                                                                                                                                                                                                                                                                                                                                                | `[ "Bash(git diff *)" ]`                                               |
| `ask`                               | Matriz de reglas de permiso para pedir confirmación al usar herramientas. Consulte [Sintaxis de regla de permiso](#permission-rule-syntax) a continuación                                                                                                                                                                                                                                                                                                                                                                                                                                  | `[ "Bash(git push *)" ]`                                               |
| `deny`                              | Matriz de reglas de permiso para denegar el uso de herramientas. Use esto para excluir archivos sensibles del acceso de Claude Code. Consulte [Sintaxis de regla de permiso](#permission-rule-syntax) y [Limitaciones de permiso de Bash](/es/permissions#tool-specific-permission-rules)                                                                                                                                                                                                                                                                                                  | `[ "WebFetch", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)" ]` |
| `additionalDirectories`             | [Directorios de trabajo](/es/permissions#working-directories) adicionales para acceso a archivos. La mayoría de la configuración de `.claude/` [no se descubre](/es/permissions#additional-directories-grant-file-access-not-configuration) desde estos directorios                                                                                                                                                                                                                                                                                                                        | `[ "../docs/" ]`                                                       |
| `defaultMode`                       | [Modo de permiso](/es/permission-modes) predeterminado al abrir Claude Code. Valores válidos: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`. {/* min-version: 2.1.142 */}A partir de Claude Code v2.1.142, `auto` se ignora cuando se establece en configuraciones de proyecto o local (`.claude/settings.json`, `.claude/settings.local.json`) para que un repositorio no pueda otorgarse a sí mismo modo automático. Establézcalo en `~/.claude/settings.json` en su lugar. La bandera CLI `--permission-mode` anula esta configuración para una única sesión | `"acceptEdits"`                                                        |
| `disableBypassPermissionsMode`      | Establecer en `"disable"` para evitar que se active el modo `bypassPermissions`. Esto deshabilita la bandera de línea de comandos `--dangerously-skip-permissions`. Típicamente colocado en [configuraciones administradas](/es/permissions#managed-settings) para aplicar política organizacional, pero funciona desde cualquier ámbito                                                                                                                                                                                                                                                   | `"disable"`                                                            |
| `skipDangerousModePermissionPrompt` | Omitir el aviso de confirmación mostrado antes de entrar en modo de permisos de derivación a través de `--dangerously-skip-permissions` o `defaultMode: "bypassPermissions"`. Se ignora cuando se establece en configuraciones de proyecto (`.claude/settings.json`) para evitar que repositorios no confiables omitan automáticamente el aviso                                                                                                                                                                                                                                            | `true`                                                                 |

### Sintaxis de regla de permiso

Las reglas de permiso siguen el formato `Tool` o `Tool(specifier)`. Las reglas se evalúan en orden: primero reglas de denegación, luego preguntar, luego permitir. La primera regla coincidente gana.

Ejemplos rápidos:

| Regla                          | Efecto                                             |
| :----------------------------- | :------------------------------------------------- |
| `Bash`                         | Coincide con todos los comandos Bash               |
| `Bash(npm run *)`              | Coincide con comandos que comienzan con `npm run`  |
| `Read(./.env)`                 | Coincide con la lectura del archivo `.env`         |
| `WebFetch(domain:example.com)` | Coincide con solicitudes de búsqueda a example.com |

Para la referencia completa de sintaxis de regla, incluyendo comportamiento de comodín, patrones específicos de herramientas para Read, Edit, WebFetch, MCP, y reglas de Agent, y limitaciones de seguridad de patrones de Bash, consulte [Sintaxis de regla de permiso](/es/permissions#permission-rule-syntax).

### Configuración de sandbox

Configure el comportamiento avanzado de sandboxing. El sandboxing aísla comandos bash de su sistema de archivos y red. Consulte [Sandboxing](/es/sandboxing) para obtener detalles.

| Claves                                 | Descripción                                                                                                                                                                                                                                                                                                                                                                                                    | Ejemplo                           |
| :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------- |
| `enabled`                              | Habilitar sandboxing de bash (macOS, Linux y WSL2). Predeterminado: false                                                                                                                                                                                                                                                                                                                                      | `true`                            |
| `failIfUnavailable`                    | Salir con un error al inicio si `sandbox.enabled` es true pero el sandbox no puede iniciarse (dependencias faltantes o plataforma no compatible). Cuando es false (predeterminado), se muestra una advertencia y los comandos se ejecutan sin sandbox. Destinado a implementaciones de configuraciones administradas que requieren sandboxing como una puerta dura                                             | `true`                            |
| `autoAllowBashIfSandboxed`             | Aprobar automáticamente comandos bash cuando están en sandbox. Predeterminado: true                                                                                                                                                                                                                                                                                                                            | `true`                            |
| `excludedCommands`                     | Comandos que deben ejecutarse fuera del sandbox                                                                                                                                                                                                                                                                                                                                                                | `["docker *"]`                    |
| `allowUnsandboxedCommands`             | Permitir que los comandos se ejecuten fuera del sandbox a través del parámetro `dangerouslyDisableSandbox`. Cuando se establece en `false`, el escape hatch `dangerouslyDisableSandbox` se deshabilita completamente y todos los comandos deben ejecutarse en sandbox (o estar en `excludedCommands`). Útil para políticas empresariales que requieren sandboxing estricto. Predeterminado: true               | `false`                           |
| `filesystem.allowWrite`                | Rutas adicionales donde los comandos en sandbox pueden escribir. Las matrices se fusionan en todos los ámbitos de configuración: las rutas de usuario, proyecto y administradas se combinan, no se reemplazan. También se fusionan con rutas de reglas de permiso `Edit(...)` permitidas. Consulte [prefijos de ruta de sandbox](#sandbox-path-prefixes) a continuación.                                       | `["/tmp/build", "~/.kube"]`       |
| `filesystem.denyWrite`                 | Rutas donde los comandos en sandbox no pueden escribir. Las matrices se fusionan en todos los ámbitos de configuración. También se fusionan con rutas de reglas de permiso `Edit(...)` denegadas.                                                                                                                                                                                                              | `["/etc", "/usr/local/bin"]`      |
| `filesystem.denyRead`                  | Rutas donde los comandos en sandbox no pueden leer. Las matrices se fusionan en todos los ámbitos de configuración. También se fusionan con rutas de reglas de permiso `Read(...)` denegadas.                                                                                                                                                                                                                  | `["~/.aws/credentials"]`          |
| `filesystem.allowRead`                 | Rutas para permitir nuevamente la lectura dentro de regiones `denyRead`. Tiene precedencia sobre `denyRead`. Las matrices se fusionan en todos los ámbitos de configuración. Use esto para crear patrones de acceso de lectura solo para el espacio de trabajo.                                                                                                                                                | `["."]`                           |
| `filesystem.allowManagedReadPathsOnly` | (Solo configuraciones administradas) Solo se respetan rutas `allowRead` de configuraciones administradas. Las entradas `denyRead` aún se fusionan desde todas las fuentes. Predeterminado: false                                                                                                                                                                                                               | `true`                            |
| `network.allowUnixSockets`             | (Solo macOS) Rutas de socket Unix accesibles en sandbox. Se ignora en Linux y WSL2, donde el filtro seccomp no puede inspeccionar rutas de socket; use `allowAllUnixSockets` en su lugar.                                                                                                                                                                                                                      | `["~/.ssh/agent-socket"]`         |
| `network.allowAllUnixSockets`          | Permitir todas las conexiones de socket Unix en sandbox. En Linux y WSL2 esta es la única forma de permitir sockets Unix, ya que omite el filtro seccomp que de otra manera bloquea llamadas `socket(AF_UNIX, ...)`. Predeterminado: false                                                                                                                                                                     | `true`                            |
| `network.allowLocalBinding`            | Permitir vinculación a puertos localhost (solo macOS). Predeterminado: false                                                                                                                                                                                                                                                                                                                                   | `true`                            |
| `network.allowMachLookup`              | Nombres de servicio XPC/Mach adicionales que el sandbox puede buscar (solo macOS). Admite un único `*` final para coincidencia de prefijo. Necesario para herramientas que se comunican a través de XPC como el Simulador de iOS o Playwright.                                                                                                                                                                 | `["com.apple.coresimulator.*"]`   |
| `network.allowedDomains`               | Matriz de dominios para permitir tráfico de red saliente. Admite comodines (por ejemplo, `*.example.com`).                                                                                                                                                                                                                                                                                                     | `["github.com", "*.npmjs.org"]`   |
| `network.deniedDomains`                | Matriz de dominios para bloquear tráfico de red saliente. Admite la misma sintaxis de comodín que `allowedDomains`. Tiene precedencia sobre `allowedDomains` cuando ambos coinciden. Se fusiona desde todas las fuentes de configuración independientemente de `allowManagedDomainsOnly`.                                                                                                                      | `["sensitive.cloud.example.com"]` |
| `network.allowManagedDomainsOnly`      | (Solo configuraciones administradas) Solo se respetan `allowedDomains` y reglas de permiso `WebFetch(domain:...)` permitidas de configuraciones administradas. Los dominios de configuraciones de usuario, proyecto y local se ignoran. Los dominios no permitidos se bloquean automáticamente sin solicitar al usuario. Los dominios denegados aún se respetan desde todas las fuentes. Predeterminado: false | `true`                            |
| `network.httpProxyPort`                | Puerto de proxy HTTP usado si desea traer su propio proxy. Si no se especifica, Claude ejecutará su propio proxy.                                                                                                                                                                                                                                                                                              | `8080`                            |
| `network.socksProxyPort`               | Puerto de proxy SOCKS5 usado si desea traer su propio proxy. Si no se especifica, Claude ejecutará su propio proxy.                                                                                                                                                                                                                                                                                            | `8081`                            |
| `enableWeakerNestedSandbox`            | Habilitar sandbox más débil para entornos Docker sin privilegios (solo Linux y WSL2). **Reduce la seguridad.** Predeterminado: false                                                                                                                                                                                                                                                                           | `true`                            |
| `enableWeakerNetworkIsolation`         | (Solo macOS) Permitir acceso al servicio de confianza TLS del sistema (`com.apple.trustd.agent`) en el sandbox. Requerido para herramientas basadas en Go como `gh`, `gcloud` y `terraform` para verificar certificados TLS cuando se usa `httpProxyPort` con un proxy MITM y CA personalizada. **Reduce la seguridad** al abrir una posible ruta de exfiltración de datos. Predeterminado: false              | `true`                            |
| `bwrapPath`                            | (Solo configuraciones administradas, Linux/WSL2) Ruta absoluta al binario bubblewrap (`bwrap`). Anula la detección automática a través de `PATH`. Solo se honra desde [configuraciones administradas](/es/settings#settings-files), no desde configuraciones de usuario o proyecto. Útil cuando `bwrap` se instala en una ubicación no estándar en entornos administrados.                                     | `/opt/admin/bwrap`                |
| `socatPath`                            | (Solo configuraciones administradas, Linux/WSL2) Ruta absoluta al binario `socat` usado para el proxy de red del sandbox. Anula la detección automática a través de `PATH`. Solo se honra desde configuraciones administradas.                                                                                                                                                                                 | `/opt/admin/socat`                |

#### Prefijos de ruta de sandbox

Las rutas en `filesystem.allowWrite`, `filesystem.denyWrite`, `filesystem.denyRead` y `filesystem.allowRead` admiten estos prefijos:

| Prefijo            | Significado                                                                                                       | Ejemplo                                                                     |
| :----------------- | :---------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `/`                | Ruta absoluta desde la raíz del sistema de archivos                                                               | `/tmp/build` se mantiene como `/tmp/build`                                  |
| `~/`               | Relativo al directorio de inicio                                                                                  | `~/.kube` se convierte en `$HOME/.kube`                                     |
| `./` o sin prefijo | Relativo a la raíz del proyecto para configuraciones de proyecto, o a `~/.claude` para configuraciones de usuario | `./output` en `.claude/settings.json` se resuelve a `<project-root>/output` |

El prefijo anterior `//path` para rutas absolutas aún funciona. Si anteriormente usó `/path` esperando resolución relativa al proyecto, cambie a `./path`. Esta sintaxis difiere de [reglas de permiso Read y Edit](/es/permissions#read-and-edit), que usan `//path` para absoluto y `/path` para relativo al proyecto. Las rutas del sistema de archivos de sandbox usan convenciones estándar: `/tmp/build` es una ruta absoluta.

**Ejemplo de configuración:**

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker *"],
    "filesystem": {
      "allowWrite": ["/tmp/build", "~/.kube"],
      "denyRead": ["~/.aws/credentials"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org", "registry.yarnpkg.com"],
      "deniedDomains": ["uploads.github.com"],
      "allowUnixSockets": [
        "/var/run/docker.sock"
      ],
      "allowLocalBinding": true
    }
  }
}
```

**Las restricciones de sistema de archivos y red** se pueden configurar de dos formas que se fusionan:

* **Configuraciones `sandbox.filesystem`** (mostradas arriba): Controlan rutas en el límite del sandbox a nivel de SO. Estas restricciones se aplican a todos los comandos de subproceso (por ejemplo, `kubectl`, `terraform`, `npm`), no solo a las herramientas de archivo de Claude.
* **Reglas de permiso**: Use reglas de permiso `Edit` permitidas/denegadas para controlar el acceso a la herramienta de archivo de Claude, reglas de denegación `Read` para bloquear lecturas, y reglas de permiso `WebFetch` permitidas/denegadas para controlar dominios de red. Las rutas de estas reglas también se fusionan en la configuración del sandbox.

### Configuración de atribución

Claude Code agrega atribución a commits de git y solicitudes de extracción. Estos se configuran por separado:

* Los commits usan [git trailers](https://git-scm.com/docs/git-interpret-trailers) (como `Co-Authored-By`) de forma predeterminada, que se pueden personalizar o deshabilitar
* Las descripciones de solicitudes de extracción son texto sin formato

| Claves   | Descripción                                                                                                                 |
| :------- | :-------------------------------------------------------------------------------------------------------------------------- |
| `commit` | Atribución para commits de git, incluyendo cualquier trailer. La cadena vacía oculta la atribución de commit                |
| `pr`     | Atribución para descripciones de solicitudes de extracción. La cadena vacía oculta la atribución de solicitud de extracción |

**Atribución de commit predeterminada:**

```text theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**Atribución de solicitud de extracción predeterminada:**

```text theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**Ejemplo:**

```json theme={null}
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": ""
  }
}
```

<Note>
  La configuración `attribution` tiene precedencia sobre la configuración `includeCoAuthoredBy` obsoleta. Para ocultar toda la atribución, establezca `commit` y `pr` en cadenas vacías.
</Note>

### Configuración de sugerencia de archivo

Configure un comando personalizado para autocompletado de ruta de archivo `@`. La sugerencia de archivo integrada utiliza recorrido rápido del sistema de archivos, pero los monorepos grandes pueden beneficiarse de indexación específica del proyecto como un índice de archivo precompilado o herramientas personalizadas.

```json theme={null}
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

El comando se ejecuta con las mismas variables de entorno que [hooks](/es/hooks), incluyendo `CLAUDE_PROJECT_DIR`. Recibe JSON a través de stdin con un campo `query`:

```json theme={null}
{"query": "src/comp"}
```

Genere rutas de archivo separadas por saltos de línea a stdout (actualmente limitado a 15):

```text theme={null}
src/components/Button.tsx
src/components/Modal.tsx
src/components/Form.tsx
```

**Ejemplo:**

```bash theme={null}
#!/bin/bash
query=$(cat | jq -r '.query')
your-repo-file-index --query "$query" | head -20
```

### Configuración de hooks

Estas configuraciones controlan qué hooks se pueden ejecutar y a qué pueden acceder los hooks HTTP. La configuración `allowManagedHooksOnly` solo se puede configurar en [configuraciones administradas](#settings-files). Las listas blancas de URL y variables de entorno se pueden establecer en cualquier nivel de configuración y se fusionan entre fuentes.

**Comportamiento cuando `allowManagedHooksOnly` es `true`:**

* Se cargan hooks administrados y hooks SDK
* Se cargan hooks de plugins forzadamente habilitados en la configuración administrada `enabledPlugins`. Esto permite que los administradores distribuyan hooks verificados a través de un marketplace de organización mientras bloquean todo lo demás. La confianza se otorga por ID completo de `plugin@marketplace`, por lo que un plugin con el mismo nombre de un marketplace diferente permanece bloqueado
* Se bloquean hooks de usuario, proyecto y todos los demás plugins

**Restringir URLs de hooks HTTP:**

Limitar qué URLs pueden dirigirse los hooks HTTP. Admite `*` como comodín para coincidencia. Cuando la matriz se define, los hooks HTTP que se dirigen a URLs que no coinciden se bloquean silenciosamente. La coincidencia de nombre de host no distingue entre mayúsculas y minúsculas e ignora un punto FQDN final, coincidiendo con la semántica de DNS.

```json theme={null}
{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}
```

**Restringir variables de entorno de hooks HTTP:**

Limitar qué nombres de variables de entorno pueden interpolar los hooks HTTP en valores de encabezado. El `allowedEnvVars` efectivo de cada hook es la intersección de su propia lista y esta configuración.

```json theme={null}
{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}
```

### Calcular configuraciones administradas con un asistente de política

La configuración `policyHelper` apunta a un ejecutable que calcula configuraciones administradas al inicio, para que los administradores puedan derivar política de postura de dispositivo, identidad, o un servicio remoto en lugar de un archivo estático. Configúrelo desde MDM o un archivo `managed-settings.json` del sistema. Claude Code ignora `policyHelper` cuando aparece en cualquier otro ámbito, incluyendo configuraciones de usuario, configuraciones de proyecto, el hive de registro HKCU, y [configuraciones administradas por servidor](/es/server-managed-settings).

La configuración acepta estas claves:

| Clave               | Tipo   | Descripción                                                                                                                               |
| ------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `path`              | string | Ruta absoluta al ejecutable del asistente                                                                                                 |
| `timeoutMs`         | number | Cuánto tiempo esperar al asistente antes de tratar la ejecución como fallida                                                              |
| `refreshIntervalMs` | number | Con qué frecuencia re-ejecutar el asistente en segundo plano. Establezca en `0` para deshabilitar la actualización, o en al menos `60000` |

El asistente escribe una envoltura JSON a stdout. Ponga las configuraciones bajo una clave `managedSettings` en lugar de en el nivel superior, ya que un objeto de configuraciones desnudo se analiza con `managedSettings` indefinido y no aplica nada:

```json theme={null}
{
  "managedSettings": {
    "permissions": { "deny": ["Read(//etc/secrets/**)"] }
  },
  "claudeMd": "# Organization context\n...",
  "appendSystemPrompt": "Always cite the internal style guide."
}
```

Cuando el asistente emite `managedSettings`, ese objeto reemplaza las configuraciones administradas basadas en archivos para la ejecución. Cuando el asistente sale con código no cero al inicio, Claude Code imprime el error y se niega a iniciar, por lo que un asistente que necesita resiliencia de interrupción debe servir desde su propio caché y salir con `0`.

### Precedencia de configuración

Las configuraciones se aplican en orden de precedencia. De mayor a menor:

1. **Configuraciones administradas** ([administradas por servidor](/es/server-managed-settings), [políticas de MDM/nivel de SO](#configuration-scopes), o [configuraciones administradas](/es/settings#settings-files))
   * Políticas implementadas por TI a través de entrega de servidor, perfiles de configuración MDM, políticas de registro o archivos de configuración administrados
   * No pueden ser anuladas por ningún otro nivel, incluyendo argumentos de línea de comandos
   * Dentro del nivel administrado, la precedencia es: administrado por servidor > políticas de MDM/nivel de SO > archivo basado (`managed-settings.d/*.json` + `managed-settings.json`) > registro HKCU (solo Windows). Solo se usa una fuente administrada; las fuentes no se fusionan entre niveles. Dentro del nivel basado en archivos, los archivos de entrega y el archivo base se fusionan juntos.
   * Los hosts de incrustación como Claude Desktop pueden suministrar política a través de la opción SDK `managedSettings`. De forma predeterminada, esto se ignora cuando está presente cualquier nivel administrado. Los administradores pueden optar por establecer [`parentSettingsBehavior`](#available-settings) en `"merge"`. Los valores del incrustador se filtran para que puedan restringir la política administrada pero no flexibilizarla.

2. **Argumentos de línea de comandos**
   * Anulaciones temporales para una sesión específica. JSON pasado a través de `--settings <file-or-json>` se fusiona con configuraciones basadas en archivos usando las mismas reglas que las otras capas: una clave establecida aquí anula la misma clave en configuraciones locales, de proyecto o de usuario, y omitir una clave deja el valor de capa inferior en su lugar

3. **Configuraciones de proyecto local** (`.claude/settings.local.json`)
   * Configuraciones personales específicas del proyecto

4. **Configuraciones de proyecto compartidas** (`.claude/settings.json`)
   * Configuraciones de proyecto compartidas por el equipo en control de código fuente

5. **Configuraciones de usuario** (`~/.claude/settings.json`)
   * Configuraciones personales globales

Esta jerarquía asegura que las políticas organizacionales siempre se apliquen mientras aún permite que equipos e individuos personalicen su experiencia. La misma precedencia se aplica si ejecuta Claude Code desde la CLI, la [extensión de VS Code](/es/vs-code), o un [IDE de JetBrains](/es/jetbrains).

Por ejemplo, si su configuración de usuario establece `permissions.defaultMode` en `acceptEdits` y la configuración compartida de un proyecto la establece en `default`, el valor del proyecto se aplica. El ejemplo a continuación cubre cómo se combinan las configuraciones con valores de matriz como reglas de permiso en su lugar.

<Note>
  **Las configuraciones de matriz se fusionan entre ámbitos.** Cuando la misma configuración con valor de matriz (como `sandbox.filesystem.allowWrite` o `permissions.allow`) aparece en múltiples ámbitos, las matrices se **concatenan y se deduplicán**, no se reemplazan. Esto significa que los ámbitos de menor prioridad pueden agregar entradas sin anular las establecidas por ámbitos de mayor prioridad, y viceversa. Por ejemplo, si las configuraciones administradas establecen `allowWrite` en `["/opt/company-tools"]` y un usuario agrega `["~/.kube"]`, ambas rutas se incluyen en la configuración final.
</Note>

### Verificar configuraciones activas

Ejecute `/status` dentro de Claude Code para ver qué fuentes de configuración están activas. La pestaña Status incluye una línea `Setting sources` que enumera cada capa que Claude Code cargó para la sesión actual, como `User settings` o `Project local settings`. Cuando [configuraciones administradas](/es/managed-settings) están en efecto, la entrada muestra el canal de entrega entre paréntesis, por ejemplo `Enterprise managed settings (remote)`, `(plist)`, `(HKLM)`, `(HKCU)`, o `(file)`. Una capa aparece en la lista solo cuando esa fuente se carga con al menos una clave, por lo que una lista vacía significa que no se encontraron fuentes de configuración.

La línea `Setting sources` confirma qué fuentes se están leyendo. No muestra qué capa suministró cada clave individual. La pestaña Config en el mismo diálogo es un editor para un conjunto fijo de toggles como tema y salida detallada, no una vista de los contenidos de su `settings.json`. Si un archivo de configuración contiene errores, como JSON inválido o un valor que falla la validación, `/status` reporta el problema para que pueda corregirlo.

### Puntos clave sobre el sistema de configuración

* **Archivos de memoria (`CLAUDE.md`)**: Contienen instrucciones y contexto que Claude carga al inicio
* **Archivos de configuración (JSON)**: Configurar permisos, variables de entorno y comportamiento de herramientas
* **Skills**: Indicaciones personalizadas que se pueden invocar con `/skill-name` o cargar automáticamente por Claude
* **MCP servers**: Extender Claude Code con herramientas e integraciones adicionales
* **Precedencia**: Las configuraciones de nivel superior (Managed) anulan las de nivel inferior (User/Project)
* **Herencia**: Las configuraciones se fusionan entre ámbitos; los valores escalares de ámbitos de mayor prioridad anulan, y las matrices se concatenan

### Indicador del sistema

El indicador del sistema interno de Claude Code no se publica. Para agregar instrucciones personalizadas, use archivos `CLAUDE.md` o la bandera `--append-system-prompt`.

### Excluyendo archivos sensibles

Para evitar que Claude Code acceda a archivos que contienen información sensible como claves API, secretos y archivos de entorno, use la configuración `permissions.deny` en su archivo `.claude/settings.json`:

```json theme={null}
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

Esto reemplaza la configuración `ignorePatterns` obsoleta. Los archivos que coinciden con estos patrones se excluyen del descubrimiento de archivos y resultados de búsqueda, y las operaciones de lectura en estos archivos se deniegan.

## Configuración de subagents

Claude Code admite subagents de IA personalizados que se pueden configurar en niveles de usuario y proyecto. Estos subagents se almacenan como archivos Markdown con frontmatter YAML:

* **Subagents de usuario**: `~/.claude/agents/` - Disponibles en todos sus proyectos
* **Subagents de proyecto**: `.claude/agents/` - Específicos de su proyecto y se pueden compartir con su equipo

Los archivos de subagent definen asistentes de IA especializados con indicaciones personalizadas y permisos de herramientas. Obtenga más información sobre cómo crear y usar subagents en la [documentación de subagents](/es/sub-agents).

## Configuración de plugins

Claude Code admite un sistema de plugins que le permite extender la funcionalidad con skills, agentes, hooks y servidores MCP. Los plugins se distribuyen a través de marketplaces y se pueden configurar en niveles de usuario y repositorio.

### Configuración de plugins

Configuraciones relacionadas con plugins en `settings.json`:

```json theme={null}
{
  "enabledPlugins": {
    "formatter@acme-tools": true,
    "deployer@acme-tools": true,
    "analyzer@security-plugins": false
  },
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    }
  }
}
```

#### `enabledPlugins`

Controla qué plugins están habilitados. Formato: `"plugin-name@marketplace-name": true/false`

**Ámbitos**:

* **Configuraciones de usuario** (`~/.claude/settings.json`): Preferencias personales de plugins
* **Configuraciones de proyecto** (`.claude/settings.json`): Plugins específicos del proyecto compartidos con el equipo
* **Configuraciones locales** (`.claude/settings.local.json`): Anulaciones por máquina (no confirmadas)
* **Configuraciones administradas** (`managed-settings.json`): Anulaciones de política a nivel de organización que bloquean la instalación en todos los ámbitos y ocultan el plugin del marketplace

<Note>
  Las configuraciones de proyecto tienen precedencia sobre las configuraciones de usuario, por lo que establecer un plugin en `false` en `~/.claude/settings.json` no deshabilita un plugin que la `.claude/settings.json` del proyecto habilita. Para optar por no participar en un plugin habilitado por el proyecto en su máquina, establézcalo en `false` en `.claude/settings.local.json` en su lugar.

  Los plugins forzados a estar habilitados por configuraciones administradas no pueden deshabilitarse de esta manera, ya que las configuraciones administradas anulan las configuraciones locales.
</Note>

**Ejemplo**:

```json theme={null}
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

1. Los miembros del equipo reciben un aviso para instalar el marketplace cuando confían en la carpeta
2. Los miembros del equipo reciben un aviso para instalar plugins de ese marketplace
3. Los usuarios pueden omitir marketplaces o plugins no deseados (almacenados en configuraciones de usuario)
4. La instalación respeta límites de confianza y requiere consentimiento explícito

**Ejemplo**:

```json theme={null}
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
* `settings`: marketplace en línea declarado directamente en settings.json sin un repositorio alojado separado (usa `name` y `plugins`)

Cada entrada de marketplace también acepta un Boolean `autoUpdate` opcional. Establezca `"autoUpdate": true` junto a `source` para hacer que Claude Code actualice ese marketplace e instale sus plugins instalados al inicio. Cuando se omite, los marketplaces oficiales de Anthropic tienen por defecto `true` y todos los demás marketplaces tienen por defecto `false`. Consulte [Configurar actualizaciones automáticas](/es/discover-plugins#configure-auto-updates).

Use `source: 'settings'` para declarar un pequeño conjunto de plugins en línea sin configurar un repositorio de marketplace alojado. Los plugins listados aquí deben hacer referencia a fuentes externas como GitHub o npm. Aún necesita habilitar cada plugin por separado en `enabledPlugins`.

```json theme={null}
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "settings",
        "name": "team-tools",
        "plugins": [
          {
            "name": "code-formatter",
            "source": {
              "source": "github",
              "repo": "acme-corp/code-formatter"
            }
          }
        ]
      }
    }
  }
}
```

#### `strictKnownMarketplaces`

**Solo configuraciones administradas**: Controla qué marketplaces de plugins se permite a los usuarios agregar e instalar plugins desde. Esta configuración solo se puede configurar en [configuraciones administradas](/es/settings#settings-files) y proporciona a los administradores control estricto sobre fuentes de marketplace.

**Ubicaciones de archivos de configuraciones administradas**:

* **macOS**: `/Library/Application Support/ClaudeCode/managed-settings.json`
* **Linux y WSL**: `/etc/claude-code/managed-settings.json`
* **Windows**: `C:\Program Files\ClaudeCode\managed-settings.json`

**Características clave**:

* Solo disponible en configuraciones administradas (`managed-settings.json`)
* No puede ser anulada por configuraciones de usuario o proyecto (precedencia más alta)
* Se aplica ANTES de operaciones de red/sistema de archivos (las fuentes bloqueadas nunca se ejecutan)
* Usa coincidencia exacta para especificaciones de fuente (incluyendo `ref`, `path` para fuentes de git), excepto `hostPattern` y `pathPattern`, que usan coincidencia regex

**Comportamiento de lista blanca**:

* `undefined` (predeterminado): Sin restricciones - los usuarios pueden agregar cualquier marketplace
* Matriz vacía `[]`: Bloqueo completo - los usuarios no pueden agregar nuevos marketplaces
* Lista de fuentes: Los usuarios solo pueden agregar marketplaces que coincidan exactamente

**Todos los tipos de fuente admitidos**:

La lista blanca admite múltiples tipos de fuente de marketplace. La mayoría de las fuentes usan coincidencia exacta, mientras que `hostPattern` y `pathPattern` usan coincidencia regex contra el host del marketplace y la ruta del sistema de archivos respectivamente.

1. **Repositorios de GitHub**:

```json theme={null}
{ "source": "github", "repo": "acme-corp/approved-plugins" }
{ "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main", "path": "marketplace" }
```

Campos: `repo` (requerido), `ref` (opcional: rama/etiqueta/SHA), `path` (opcional: subdirectorio)

2. **Repositorios de Git**:

```json theme={null}
{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git" }
{ "source": "git", "url": "https://bitbucket.org/acme-corp/plugins.git", "ref": "production" }
{ "source": "git", "url": "ssh://git@git.example.com/plugins.git", "ref": "v3.1", "path": "approved" }
```

Campos: `url` (requerido), `ref` (opcional: rama/etiqueta/SHA), `path` (opcional: subdirectorio)

3. **Marketplaces basados en URL**:

```json theme={null}
{ "source": "url", "url": "https://plugins.example.com/marketplace.json" }
{ "source": "url", "url": "https://cdn.example.com/marketplace.json", "headers": { "Authorization": "Bearer ${TOKEN}" } }
```

Campos: `url` (requerido), `headers` (opcional: encabezados HTTP para acceso autenticado)

<Note>
  Los marketplaces basados en URL solo descargan el archivo `marketplace.json`. No descargan archivos de plugins del servidor. Los plugins en marketplaces basados en URL deben usar fuentes externas (URLs de GitHub, npm o git) en lugar de rutas relativas. Para plugins con rutas relativas, use un marketplace basado en Git en su lugar. Consulte [Troubleshooting](/es/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces) para obtener detalles.
</Note>

4. **Paquetes NPM**:

```json theme={null}
{ "source": "npm", "package": "@acme-corp/claude-plugins" }
{ "source": "npm", "package": "@acme-corp/approved-marketplace" }
```

Campos: `package` (requerido, admite paquetes con alcance)

5. **Rutas de archivo**:

```json theme={null}
{ "source": "file", "path": "/usr/local/share/claude/acme-marketplace.json" }
{ "source": "file", "path": "/opt/acme-corp/plugins/marketplace.json" }
```

Campos: `path` (requerido: ruta absoluta al archivo marketplace.json)

6. **Rutas de directorio**:

```json theme={null}
{ "source": "directory", "path": "/usr/local/share/claude/acme-plugins" }
{ "source": "directory", "path": "/opt/acme-corp/approved-marketplaces" }
```

Campos: `path` (requerido: ruta absoluta al directorio que contiene `.claude-plugin/marketplace.json`)

7. **Coincidencia de patrón de host**:

```json theme={null}
{ "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" }
{ "source": "hostPattern", "hostPattern": "^gitlab\\.internal\\.example\\.com$" }
```

Campos: `hostPattern` (requerido: patrón regex para coincidir contra el host del marketplace)

Use coincidencia de patrón de host cuando desee permitir todos los marketplaces de un host específico sin enumerar cada repositorio individualmente. Esto es útil para organizaciones con GitHub Enterprise interno o servidores GitLab donde los desarrolladores crean sus propios marketplaces.

Extracción de host por tipo de fuente:

* `github`: siempre coincide contra `github.com`
* `git`: extrae nombre de host de la URL (admite formatos HTTPS y SSH)
* `url`: extrae nombre de host de la URL
* `npm`, `file`, `directory`: no admitido para coincidencia de patrón de host

8. **Coincidencia de patrón de ruta**:

```json theme={null}
{ "source": "pathPattern", "pathPattern": "^/opt/approved/" }
{ "source": "pathPattern", "pathPattern": ".*" }
```

Campos: `pathPattern` (requerido: patrón regex coincidido contra el campo `path` de fuentes `file` y `directory`)

Use coincidencia de patrón de ruta para permitir marketplaces basados en sistema de archivos junto con restricciones `hostPattern` para fuentes de red. Establezca `".*"` para permitir todas las rutas locales, o un patrón más estrecho para restringir a directorios específicos.

**Ejemplos de configuración**:

Ejemplo: permitir solo marketplaces específicos:

```json theme={null}
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

```json theme={null}
{
  "strictKnownMarketplaces": []
}
```

Ejemplo: permitir todos los marketplaces de un servidor git interno:

```json theme={null}
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

```json theme={null}
// Estas son fuentes DIFERENTES:
{ "source": "github", "repo": "acme-corp/plugins" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main" }

// Estas también son DIFERENTES:
{ "source": "github", "repo": "acme-corp/plugins", "path": "marketplace" }
{ "source": "github", "repo": "acme-corp/plugins" }
```

**Comparación con `extraKnownMarketplaces`**:

| Aspecto                      | `strictKnownMarketplaces`                       | `extraKnownMarketplaces`                       |
| ---------------------------- | ----------------------------------------------- | ---------------------------------------------- |
| **Propósito**                | Aplicación de política organizacional           | Conveniencia del equipo                        |
| **Archivo de configuración** | Solo `managed-settings.json`                    | Cualquier archivo de configuración             |
| **Comportamiento**           | Bloquea adiciones no permitidas                 | Instala automáticamente marketplaces faltantes |
| **Cuándo se aplica**         | Antes de operaciones de red/sistema de archivos | Después del aviso de confianza del usuario     |
| **Puede ser anulada**        | No (precedencia más alta)                       | Sí (por configuraciones de mayor precedencia)  |
| **Formato de fuente**        | Objeto de fuente directo                        | Marketplace nombrado con fuente anidada        |
| **Caso de uso**              | Restricciones de cumplimiento y seguridad       | Incorporación, estandarización                 |

**Diferencia de formato**:

`strictKnownMarketplaces` usa objetos de fuente directos:

```json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ]
}
```

`extraKnownMarketplaces` requiere marketplaces nombrados:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

**Usando ambos juntos**:

`strictKnownMarketplaces` es una puerta de política: controla qué pueden agregar los usuarios pero no registra ningún marketplace. Para restringir y pre-registrar un marketplace para todos los usuarios, establezca ambos en `managed-settings.json`:

```json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ],
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

Con solo `strictKnownMarketplaces` establecido, los usuarios aún pueden agregar el marketplace permitido manualmente a través de `/plugin marketplace add`, pero no está disponible automáticamente.

**Notas importantes**:

* Las restricciones se verifican ANTES de cualquier solicitud de red u operación del sistema de archivos
* Cuando se bloquea, los usuarios ven mensajes de error claros indicando que la fuente está bloqueada por política administrada
* La restricción se aplica en agregar marketplace y en instalar, actualizar, actualizar y auto-actualizar plugins. Un marketplace agregado antes de que se estableciera la política no puede usarse para instalar o actualizar plugins una vez que su fuente ya no coincida con la lista blanca
* Las configuraciones administradas tienen la precedencia más alta y no pueden ser anuladas

Consulte [Restricciones de marketplace administradas](/es/plugin-marketplaces#managed-marketplace-restrictions) para documentación dirigida al usuario.

#### `strictPluginOnlyCustomization`

**Solo configuraciones administradas**: bloquea skills, agentes, hooks y servidores MCP de fuentes de usuario y proyecto, por lo que solo pueden provenir de plugins o configuraciones administradas. Combínelo con `strictKnownMarketplaces` para controlar la cadena de suministro de personalización completa: la lista blanca de marketplace controla qué plugins pueden instalar los usuarios, y esta configuración bloquea todo lo que no proviene de un plugin o de configuraciones administradas.

<Note>
  `strictPluginOnlyCustomization` requiere Claude Code v2.1.82 o posterior. Las versiones anteriores ignoran la clave y continúan cargando personalizaciones de usuario y proyecto, por lo que el bloqueo no se aplica hasta que los clientes se actualicen.
</Note>

El valor es `true` para bloquear las cuatro superficies, o una matriz que nombra las superficies a bloquear:

```json theme={null}
{
  "strictPluginOnlyCustomization": ["skills", "hooks"]
}
```

Para cada superficie bloqueada, Claude Code omite fuentes a nivel de usuario y proyecto y carga solo fuentes proporcionadas por plugins y administradas:

| Superficie | Bloqueado cuando está bloqueado                       | Aún carga                                                                                     |
| :--------- | :---------------------------------------------------- | :-------------------------------------------------------------------------------------------- |
| `skills`   | `~/.claude/skills/`, `.claude/skills/`                | Skills de plugins, skills incluidos, skills en el directorio de política administrada         |
| `agents`   | `~/.claude/agents/`, `.claude/agents/`                | Agentes de plugins, agentes integrados, agentes en el directorio de política administrada     |
| `hooks`    | Hooks en `settings.json` de usuario, proyecto y local | Hooks de plugins, hooks en configuraciones administradas                                      |
| `mcp`      | Servidores en `~/.claude.json` y `.mcp.json`          | Servidores MCP de plugins, servidores [`managed-mcp.json`](/es/mcp#managed-mcp-configuration) |

Los nombres de superficie que una versión de Claude Code no reconoce se ignoran en lugar de fallar en el archivo de configuración, por lo que puede agregar nuevos nombres de superficie antes de que todos los clientes se hayan actualizado.

### Gestionar plugins

Use el comando `/plugin` para gestionar plugins interactivamente:

* Examinar plugins disponibles de marketplaces
* Instalar/desinstalar plugins
* Habilitar/deshabilitar plugins
* Ver detalles de plugins (skills, agentes, hooks proporcionados)
* Agregar/eliminar marketplaces

Obtenga más información sobre el sistema de plugins en la [documentación de plugins](/es/plugins).

## Variables de entorno

Las variables de entorno le permiten controlar el comportamiento de Claude Code sin editar archivos de configuración. Cualquier variable también se puede configurar en [`settings.json`](#available-settings) bajo la clave `env` para aplicarla a cada sesión o implementarla en su equipo.

Consulte la [referencia de variables de entorno](/es/env-vars) para la lista completa.

## Herramientas disponibles para Claude

Claude Code tiene acceso a un conjunto de herramientas para leer, editar, buscar, ejecutar comandos y orquestar subagents. Los nombres de herramientas son las cadenas exactas que utiliza en reglas de permiso y coincidencias de hooks.

Consulte la [referencia de herramientas](/es/tools-reference) para la lista completa y detalles del comportamiento de la herramienta Bash.

## Ver también

* [Permisos](/es/permissions): sistema de permisos, sintaxis de regla, patrones específicos de herramientas y políticas administradas
* [Autenticación](/es/authentication): configurar acceso de usuario a Claude Code
* [Depurar su configuración](/es/debug-your-config): diagnosticar por qué una configuración, hook o servidor MCP no está surtiendo efecto
* [Solucionar problemas de instalación e inicio de sesión](/es/troubleshoot-install): problemas de instalación, autenticación y plataforma
