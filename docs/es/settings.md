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

Cuando la misma configuración se configura en múltiples ámbitos, los ámbitos más específicos tienen precedencia:

1. **Managed** (más alto) - no puede ser anulado por nada
2. **Argumentos de línea de comandos** - anulaciones de sesión temporal
3. **Local** - anula configuraciones de proyecto y usuario
4. **Project** - anula configuraciones de usuario
5. **User** (más bajo) - se aplica cuando nada más especifica la configuración

Por ejemplo, si un permiso se permite en la configuración de usuario pero se deniega en la configuración de proyecto, la configuración de proyecto tiene precedencia y el permiso se bloquea.

### Qué usa ámbitos

Los ámbitos se aplican a muchas características de Claude Code:

| Característica  | Ubicación de usuario      | Ubicación de proyecto             | Ubicación local                 |
| :-------------- | :------------------------ | :-------------------------------- | :------------------------------ |
| **Settings**    | `~/.claude/settings.json` | `.claude/settings.json`           | `.claude/settings.local.json`   |
| **Subagents**   | `~/.claude/agents/`       | `.claude/agents/`                 | Ninguno                         |
| **MCP servers** | `~/.claude.json`          | `.mcp.json`                       | `~/.claude.json` (por proyecto) |
| **Plugins**     | `~/.claude/settings.json` | `.claude/settings.json`           | `.claude/settings.local.json`   |
| **CLAUDE.md**   | `~/.claude/CLAUDE.md`     | `CLAUDE.md` o `.claude/CLAUDE.md` | Ninguno                         |

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
    * macOS: dominio de preferencias administradas `com.anthropic.claudecode` (implementado a través de perfiles de configuración en Jamf, Kandji u otras herramientas MDM)
    * Windows: clave de registro `HKLM\SOFTWARE\Policies\ClaudeCode` con un valor `Settings` (REG\_SZ o REG\_EXPAND\_SZ) que contiene JSON (implementado a través de Política de grupo o Intune)
    * Windows (nivel de usuario): `HKCU\SOFTWARE\Policies\ClaudeCode` (prioridad de política más baja, solo se usa cuando no existe una fuente a nivel de administrador)
  * **Basado en archivos**: `managed-settings.json` y `managed-mcp.json` implementados en directorios del sistema:

    * macOS: `/Library/Application Support/ClaudeCode/`
    * Linux y WSL: `/etc/claude-code/`
    * Windows: `C:\Program Files\ClaudeCode\`

    <Warning>
      La ruta heredada de Windows `C:\ProgramData\ClaudeCode\managed-settings.json` ya no se admite a partir de v2.1.75. Los administradores que implementaron configuraciones en esa ubicación deben migrar archivos a `C:\Program Files\ClaudeCode\managed-settings.json`.
    </Warning>

  Consulte [configuraciones administradas](/es/permissions#managed-only-settings) y [Configuración de MCP administrada](/es/mcp#managed-mcp-configuration) para obtener detalles.

  <Note>
    Las implementaciones administradas también pueden restringir **adiciones de marketplace de plugins** usando `strictKnownMarketplaces`. Para obtener más información, consulte [Restricciones de marketplace administradas](/es/plugin-marketplaces#managed-marketplace-restrictions).
  </Note>
* **Otra configuración** se almacena en `~/.claude.json`. Este archivo contiene sus preferencias (tema, configuración de notificaciones, modo de editor), sesión OAuth, configuraciones de [MCP server](/es/mcp) para ámbitos de usuario y local, estado por proyecto (herramientas permitidas, configuración de confianza) y varios cachés. Los MCP servers con ámbito de proyecto se almacenan por separado en `.mcp.json`.

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

| Clave                             | Descripción                                                                                                                                                                                                                                                                                                                                                                                                                | Ejemplo                                                                 |
| :-------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------- |
| `apiKeyHelper`                    | Script personalizado, a ejecutarse en `/bin/sh`, para generar un valor de autenticación. Este valor se enviará como encabezados `X-Api-Key` y `Authorization: Bearer` para solicitudes de modelo                                                                                                                                                                                                                           | `/bin/generate_temp_api_key.sh`                                         |
| `autoMemoryDirectory`             | Directorio personalizado para almacenamiento de [memoria automática](/es/memory#storage-location). Acepta rutas expandidas con `~/`. No se acepta en configuraciones de proyecto (`.claude/settings.json`) para evitar que repositorios compartidos redirijan escrituras de memoria a ubicaciones sensibles. Se acepta desde configuraciones de política, local y usuario                                                  | `"~/my-memory-dir"`                                                     |
| `cleanupPeriodDays`               | Las sesiones inactivas durante más tiempo que este período se eliminan al inicio (predeterminado: 30 días).<br /><br />Establecer en `0` elimina todas las transcripciones existentes al inicio e inhabilita completamente la persistencia de sesión. No se escriben nuevos archivos `.jsonl`, `/resume` no muestra conversaciones, y los hooks reciben una `transcript_path` vacía.                                       | `20`                                                                    |
| `companyAnnouncements`            | Anuncio a mostrar a los usuarios al inicio. Si se proporcionan múltiples anuncios, se alternarán aleatoriamente.                                                                                                                                                                                                                                                                                                           | `["Welcome to Acme Corp! Review our code guidelines at docs.acme.com"]` |
| `env`                             | Variables de entorno que se aplicarán a cada sesión                                                                                                                                                                                                                                                                                                                                                                        | `{"FOO": "bar"}`                                                        |
| `attribution`                     | Personalizar atribución para commits de git y solicitudes de extracción. Consulte [Configuración de atribución](#attribution-settings)                                                                                                                                                                                                                                                                                     | `{"commit": "🤖 Generated with Claude Code", "pr": ""}`                 |
| `includeCoAuthoredBy`             | **Obsoleto**: Use `attribution` en su lugar. Si incluir la línea `co-authored-by Claude` en commits de git y solicitudes de extracción (predeterminado: `true`)                                                                                                                                                                                                                                                            | `false`                                                                 |
| `includeGitInstructions`          | Incluir instrucciones de flujo de trabajo de commit y PR integradas y la instantánea de estado de git en el indicador del sistema de Claude (predeterminado: `true`). Establecer en `false` para eliminar ambas, por ejemplo cuando se usan skills de flujo de trabajo de git personalizados. La variable de entorno `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` tiene precedencia sobre esta configuración cuando se establece | `false`                                                                 |
| `permissions`                     | Consulte la tabla a continuación para la estructura de permisos.                                                                                                                                                                                                                                                                                                                                                           |                                                                         |
| `autoMode`                        | Personalizar qué bloquea y permite el clasificador de [modo automático](/es/permission-modes#eliminate-prompts-with-auto-mode). Contiene matrices `environment`, `allow` y `soft_deny` de reglas en prosa. Consulte [Configurar el clasificador de modo automático](/es/permissions#configure-the-auto-mode-classifier). No se lee desde configuraciones de proyecto compartidas                                           | `{"environment": ["Trusted repo: github.example.com/acme"]}`            |
| `disableAutoMode`                 | Establecer en `"disable"` para evitar que se active el [modo automático](/es/permission-modes#eliminate-prompts-with-auto-mode). Elimina `auto` del ciclo `Shift+Tab` y rechaza `--permission-mode auto` al inicio. Más útil en [configuraciones administradas](/es/permissions#managed-settings) donde los usuarios no pueden anularlo                                                                                    | `"disable"`                                                             |
| `hooks`                           | Configurar comandos personalizados para ejecutarse en eventos del ciclo de vida. Consulte [documentación de hooks](/es/hooks) para el formato                                                                                                                                                                                                                                                                              | Consulte [hooks](/es/hooks)                                             |
| `disableAllHooks`                 | Deshabilitar todos los [hooks](/es/hooks) y cualquier [línea de estado](/es/statusline) personalizada                                                                                                                                                                                                                                                                                                                      | `true`                                                                  |
| `allowManagedHooksOnly`           | (Solo configuraciones administradas) Evitar la carga de hooks de usuario, proyecto y plugin. Solo permite hooks administrados y hooks SDK. Consulte [Configuración de hooks](#hook-configuration)                                                                                                                                                                                                                          | `true`                                                                  |
| `allowedHttpHookUrls`             | Lista blanca de patrones de URL que los hooks HTTP pueden dirigirse. Admite `*` como comodín. Cuando se establece, los hooks con URLs que no coinciden se bloquean. Sin definir = sin restricción, matriz vacía = bloquear todos los hooks HTTP. Las matrices se fusionan entre fuentes de configuración. Consulte [Configuración de hooks](#hook-configuration)                                                           | `["https://hooks.example.com/*"]`                                       |
| `httpHookAllowedEnvVars`          | Lista blanca de nombres de variables de entorno que los hooks HTTP pueden interpolar en encabezados. Cuando se establece, el `allowedEnvVars` efectivo de cada hook es la intersección con esta lista. Sin definir = sin restricción. Las matrices se fusionan entre fuentes de configuración. Consulte [Configuración de hooks](#hook-configuration)                                                                      | `["MY_TOKEN", "HOOK_SECRET"]`                                           |
| `allowManagedPermissionRulesOnly` | (Solo configuraciones administradas) Evitar que configuraciones de usuario y proyecto definan reglas de permiso `allow`, `ask` o `deny`. Solo se aplican las reglas en configuraciones administradas. Consulte [Configuraciones solo administradas](/es/permissions#managed-only-settings)                                                                                                                                 | `true`                                                                  |
| `allowManagedMcpServersOnly`      | (Solo configuraciones administradas) Solo se respetan `allowedMcpServers` de configuraciones administradas. `deniedMcpServers` aún se fusiona desde todas las fuentes. Los usuarios aún pueden agregar MCP servers, pero solo se aplica la lista blanca definida por el administrador. Consulte [Configuración de MCP administrada](/es/mcp#managed-mcp-configuration)                                                     | `true`                                                                  |
| `model`                           | Anular el modelo predeterminado a usar para Claude Code                                                                                                                                                                                                                                                                                                                                                                    | `"claude-sonnet-4-6"`                                                   |
| `availableModels`                 | Restringir qué modelos pueden seleccionar los usuarios a través de `/model`, `--model`, herramienta Config, o `ANTHROPIC_MODEL`. No afecta la opción Predeterminado. Consulte [Restringir selección de modelo](/es/model-config#restrict-model-selection)                                                                                                                                                                  | `["sonnet", "haiku"]`                                                   |
| `modelOverrides`                  | Asignar IDs de modelo de Anthropic a IDs de modelo específicos del proveedor como ARNs de perfil de inferencia de Bedrock. Cada entrada del selector de modelo usa su valor asignado al llamar a la API del proveedor. Consulte [Anular IDs de modelo por versión](/es/model-config#override-model-ids-per-version)                                                                                                        | `{"claude-opus-4-6": "arn:aws:bedrock:..."}`                            |
| `effortLevel`                     | Persistir el [nivel de esfuerzo](/es/model-config#adjust-effort-level) entre sesiones. Acepta `"low"`, `"medium"`, o `"high"`. Se escribe automáticamente cuando ejecuta `/effort low`, `/effort medium`, o `/effort high`. Compatible con Opus 4.6 y Sonnet 4.6                                                                                                                                                           | `"medium"`                                                              |
| `otelHeadersHelper`               | Script para generar encabezados dinámicos de OpenTelemetry. Se ejecuta al inicio y periódicamente (consulte [Encabezados dinámicos](/es/monitoring-usage#dynamic-headers))                                                                                                                                                                                                                                                 | `/bin/generate_otel_headers.sh`                                         |
| `statusLine`                      | Configurar una línea de estado personalizada para mostrar contexto. Consulte [documentación de `statusLine`](/es/statusline)                                                                                                                                                                                                                                                                                               | `{"type": "command", "command": "~/.claude/statusline.sh"}`             |
| `fileSuggestion`                  | Configurar un script personalizado para autocompletado de archivo `@`. Consulte [Configuración de sugerencia de archivo](#file-suggestion-settings)                                                                                                                                                                                                                                                                        | `{"type": "command", "command": "~/.claude/file-suggestion.sh"}`        |
| `respectGitignore`                | Controlar si el selector de archivo `@` respeta patrones `.gitignore`. Cuando es `true` (predeterminado), los archivos que coinciden con patrones `.gitignore` se excluyen de las sugerencias                                                                                                                                                                                                                              | `false`                                                                 |
| `outputStyle`                     | Configurar un estilo de salida para ajustar el indicador del sistema. Consulte [documentación de estilos de salida](/es/output-styles)                                                                                                                                                                                                                                                                                     | `"Explanatory"`                                                         |
| `agent`                           | Ejecutar el hilo principal como un subagent nombrado. Aplica el indicador del sistema del subagent, restricciones de herramientas y modelo. Consulte [Invocar subagents explícitamente](/es/sub-agents#invoke-subagents-explicitly)                                                                                                                                                                                        | `"code-reviewer"`                                                       |
| `forceLoginMethod`                | Use `claudeai` para restringir el inicio de sesión a cuentas de Claude.ai, `console` para restringir el inicio de sesión a cuentas de Claude Console (facturación de uso de API)                                                                                                                                                                                                                                           | `claudeai`                                                              |
| `forceLoginOrgUUID`               | Especificar el UUID de una organización para seleccionarla automáticamente durante el inicio de sesión, omitiendo el paso de selección de organización. Requiere que `forceLoginMethod` esté establecido                                                                                                                                                                                                                   | `"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"`                                |
| `enableAllProjectMcpServers`      | Aprobar automáticamente todos los MCP servers definidos en archivos `.mcp.json` de proyecto                                                                                                                                                                                                                                                                                                                                | `true`                                                                  |
| `enabledMcpjsonServers`           | Lista de MCP servers específicos de archivos `.mcp.json` para aprobar                                                                                                                                                                                                                                                                                                                                                      | `["memory", "github"]`                                                  |
| `disabledMcpjsonServers`          | Lista de MCP servers específicos de archivos `.mcp.json` para rechazar                                                                                                                                                                                                                                                                                                                                                     | `["filesystem"]`                                                        |
| `channelsEnabled`                 | (Solo configuraciones administradas) Permitir [canales](/es/channels) para usuarios de Team y Enterprise. Sin definir o `false` bloquea la entrega de mensajes de canal independientemente de lo que los usuarios pasen a `--channels`                                                                                                                                                                                     | `true`                                                                  |
| `allowedMcpServers`               | Cuando se establece en managed-settings.json, lista blanca de MCP servers que los usuarios pueden configurar. Sin definir = sin restricciones, matriz vacía = bloqueo. Se aplica a todos los ámbitos. La lista de denegación tiene precedencia. Consulte [Configuración de MCP administrada](/es/mcp#managed-mcp-configuration)                                                                                            | `[{ "serverName": "github" }]`                                          |
| `deniedMcpServers`                | Cuando se establece en managed-settings.json, lista negra de MCP servers que están explícitamente bloqueados. Se aplica a todos los ámbitos incluyendo servers administrados. La lista de denegación tiene precedencia sobre la lista blanca. Consulte [Configuración de MCP administrada](/es/mcp#managed-mcp-configuration)                                                                                              | `[{ "serverName": "filesystem" }]`                                      |
| `strictKnownMarketplaces`         | Cuando se establece en managed-settings.json, lista blanca de marketplaces de plugins que los usuarios pueden agregar. Sin definir = sin restricciones, matriz vacía = bloqueo. Se aplica solo a adiciones de marketplace. Consulte [Restricciones de marketplace administradas](/es/plugin-marketplaces#managed-marketplace-restrictions)                                                                                 | `[{ "source": "github", "repo": "acme-corp/plugins" }]`                 |
| `blockedMarketplaces`             | (Solo configuraciones administradas) Lista negra de fuentes de marketplace. Las fuentes bloqueadas se verifican antes de descargar, por lo que nunca tocan el sistema de archivos. Consulte [Restricciones de marketplace administradas](/es/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                         | `[{ "source": "github", "repo": "untrusted/plugins" }]`                 |
| `pluginTrustMessage`              | (Solo configuraciones administradas) Mensaje personalizado agregado a la advertencia de confianza de plugin mostrada antes de la instalación. Use esto para agregar contexto específico de la organización, por ejemplo para confirmar que los plugins de su marketplace interno están verificados.                                                                                                                        | `"All plugins from our marketplace are approved by IT"`                 |
| `awsAuthRefresh`                  | Script personalizado que modifica el directorio `.aws` (consulte [configuración avanzada de credenciales](/es/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                                                                           | `aws sso login --profile myprofile`                                     |
| `awsCredentialExport`             | Script personalizado que genera JSON con credenciales de AWS (consulte [configuración avanzada de credenciales](/es/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                                                                     | `/bin/generate_aws_grant.sh`                                            |
| `alwaysThinkingEnabled`           | Habilitar [pensamiento extendido](/es/common-workflows#use-extended-thinking-thinking-mode) de forma predeterminada para todas las sesiones. Típicamente configurado a través del comando `/config` en lugar de editar directamente                                                                                                                                                                                        | `true`                                                                  |
| `plansDirectory`                  | Personalizar dónde se almacenan los archivos de plan. La ruta es relativa a la raíz del proyecto. Predeterminado: `~/.claude/plans`                                                                                                                                                                                                                                                                                        | `"./plans"`                                                             |
| `showClearContextOnPlanAccept`    | Mostrar la opción "borrar contexto" en la pantalla de aceptación del plan. Predeterminado: `false`. Establecer en `true` para restaurar la opción                                                                                                                                                                                                                                                                          | `true`                                                                  |
| `spinnerVerbs`                    | Personalizar los verbos de acción mostrados en el spinner y mensajes de duración de turno. Establecer `mode` en `"replace"` para usar solo sus verbos, o `"append"` para agregarlos a los predeterminados                                                                                                                                                                                                                  | `{"mode": "append", "verbs": ["Pondering", "Crafting"]}`                |
| `language`                        | Configurar el idioma de respuesta preferido de Claude (por ejemplo, `"japanese"`, `"spanish"`, `"french"`). Claude responderá en este idioma de forma predeterminada. También establece el idioma de [dictado de voz](/es/voice-dictation#change-the-dictation-language)                                                                                                                                                   | `"japanese"`                                                            |
| `voiceEnabled`                    | Habilitar [dictado de voz](/es/voice-dictation) de pulsar para hablar. Se escribe automáticamente cuando ejecuta `/voice`. Requiere una cuenta de Claude.ai                                                                                                                                                                                                                                                                | `true`                                                                  |
| `autoUpdatesChannel`              | Canal de lanzamiento a seguir para actualizaciones. Use `"stable"` para una versión que típicamente tiene aproximadamente una semana de antigüedad y omite versiones con regresiones importantes, o `"latest"` (predeterminado) para el lanzamiento más reciente                                                                                                                                                           | `"stable"`                                                              |
| `spinnerTipsEnabled`              | Mostrar consejos en el spinner mientras Claude está trabajando. Establecer en `false` para deshabilitar consejos (predeterminado: `true`)                                                                                                                                                                                                                                                                                  | `false`                                                                 |
| `spinnerTipsOverride`             | Anular consejos del spinner con cadenas personalizadas. `tips`: matriz de cadenas de consejo. `excludeDefault`: si es `true`, mostrar solo consejos personalizados; si es `false` o está ausente, los consejos personalizados se fusionan con consejos integrados                                                                                                                                                          | `{ "excludeDefault": true, "tips": ["Use our internal tool X"] }`       |
| `prefersReducedMotion`            | Reducir o deshabilitar animaciones de UI (spinners, shimmer, efectos flash) para accesibilidad                                                                                                                                                                                                                                                                                                                             | `true`                                                                  |
| `fastModePerSessionOptIn`         | Cuando es `true`, el modo rápido no persiste entre sesiones. Cada sesión comienza con el modo rápido desactivado, requiriendo que los usuarios lo habiliten con `/fast`. La preferencia de modo rápido del usuario aún se guarda. Consulte [Requerir opt-in por sesión](/es/fast-mode#require-per-session-opt-in)                                                                                                          | `true`                                                                  |
| `teammateMode`                    | Cómo se muestran los compañeros de [equipo de agentes](/es/agent-teams): `auto` (elige paneles divididos en tmux o iTerm2, en proceso de otra manera), `in-process`, o `tmux`. Consulte [configurar equipos de agentes](/es/agent-teams#set-up-agent-teams)                                                                                                                                                                | `"in-process"`                                                          |
| `feedbackSurveyRate`              | Probabilidad (0–1) de que la [encuesta de calidad de sesión](/es/data-usage#session-quality-surveys) aparezca cuando sea elegible. Establecer en `0` para suprimir completamente. Útil cuando se usa Bedrock, Vertex, o Foundry donde la tasa de muestreo predeterminada no se aplica                                                                                                                                      | `0.05`                                                                  |

### Configuración de config global

Estas configuraciones se almacenan en `~/.claude.json` en lugar de `settings.json`. Agregarlas a `settings.json` activará un error de validación de esquema.

| Clave                        | Descripción                                                                                                                                                                                                                                                                                                                                                     | Ejemplo |
| :--------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------ |
| `autoConnectIde`             | Conectarse automáticamente a un IDE en ejecución cuando Claude Code se inicia desde una terminal externa. Predeterminado: `false`. Aparece en `/config` como **Auto-connect to IDE (external terminal)** cuando se ejecuta fuera de una terminal de VS Code o JetBrains                                                                                         | `true`  |
| `autoInstallIdeExtension`    | Instalar automáticamente la extensión de Claude Code IDE cuando se ejecuta desde una terminal de VS Code. Predeterminado: `true`. Aparece en `/config` como **Auto-install IDE extension** cuando se ejecuta dentro de una terminal de VS Code o JetBrains. También puede establecer la variable de entorno [`CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`](/es/env-vars) | `false` |
| `editorMode`                 | Modo de atajos de teclado para el indicador de entrada: `"normal"` o `"vim"`. Predeterminado: `"normal"`. Se escribe automáticamente cuando ejecuta `/vim`. Aparece en `/config` como **Key binding mode**                                                                                                                                                      | `"vim"` |
| `showTurnDuration`           | Mostrar mensajes de duración de turno después de respuestas, por ejemplo "Cooked for 1m 6s". Predeterminado: `true`. Aparece en `/config` como **Show turn duration**                                                                                                                                                                                           | `false` |
| `terminalProgressBarEnabled` | Mostrar la barra de progreso del terminal en terminales compatibles: ConEmu, Ghostty 1.2.0+, e iTerm2 3.6.6+. Predeterminado: `true`. Aparece en `/config` como **Terminal progress bar**                                                                                                                                                                       | `false` |

### Configuración de worktrees

Configure cómo `--worktree` crea y gestiona git worktrees. Use estas configuraciones para reducir el uso de disco y el tiempo de inicio en monorepos grandes.

| Clave                         | Descripción                                                                                                                                                                               | Ejemplo                               |
| :---------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------ |
| `worktree.symlinkDirectories` | Directorios a enlazar simbólicamente desde el repositorio principal en cada worktree para evitar duplicar directorios grandes en disco. No se enlazan directorios de forma predeterminada | `["node_modules", ".cache"]`          |
| `worktree.sparsePaths`        | Directorios a verificar en cada worktree a través de git sparse-checkout (modo cone). Solo las rutas listadas se escriben en disco, lo que es más rápido en monorepos grandes             | `["packages/my-app", "shared/utils"]` |

### Configuración de permisos

| Claves                         | Descripción                                                                                                                                                                                                                                                                               | Ejemplo                                                                |
| :----------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `allow`                        | Matriz de reglas de permiso para permitir el uso de herramientas. Consulte [Sintaxis de regla de permiso](#permission-rule-syntax) a continuación para detalles de coincidencia de patrones                                                                                               | `[ "Bash(git diff *)" ]`                                               |
| `ask`                          | Matriz de reglas de permiso para pedir confirmación al usar herramientas. Consulte [Sintaxis de regla de permiso](#permission-rule-syntax) a continuación                                                                                                                                 | `[ "Bash(git push *)" ]`                                               |
| `deny`                         | Matriz de reglas de permiso para denegar el uso de herramientas. Use esto para excluir archivos sensibles del acceso de Claude Code. Consulte [Sintaxis de regla de permiso](#permission-rule-syntax) y [Limitaciones de permiso de Bash](/es/permissions#tool-specific-permission-rules) | `[ "WebFetch", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)" ]` |
| `additionalDirectories`        | [Directorios de trabajo](/es/permissions#working-directories) adicionales a los que Claude tiene acceso                                                                                                                                                                                   | `[ "../docs/" ]`                                                       |
| `defaultMode`                  | [Modo de permiso](/es/permission-modes) predeterminado al abrir Claude Code                                                                                                                                                                                                               | `"acceptEdits"`                                                        |
| `disableBypassPermissionsMode` | Establecer en `"disable"` para evitar que se active el modo `bypassPermissions`. Esto deshabilita la bandera de línea de comandos `--dangerously-skip-permissions`. Más útil en [configuraciones administradas](/es/permissions#managed-settings) donde los usuarios no pueden anularlo   | `"disable"`                                                            |

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

| Claves                                 | Descripción                                                                                                                                                                                                                                                                                                                                                                                                    | Ejemplo                         |
| :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------ |
| `enabled`                              | Habilitar sandboxing de bash (macOS, Linux y WSL2). Predeterminado: false                                                                                                                                                                                                                                                                                                                                      | `true`                          |
| `autoAllowBashIfSandboxed`             | Aprobar automáticamente comandos bash cuando están en sandbox. Predeterminado: true                                                                                                                                                                                                                                                                                                                            | `true`                          |
| `excludedCommands`                     | Comandos que deben ejecutarse fuera del sandbox                                                                                                                                                                                                                                                                                                                                                                | `["git", "docker"]`             |
| `allowUnsandboxedCommands`             | Permitir que los comandos se ejecuten fuera del sandbox a través del parámetro `dangerouslyDisableSandbox`. Cuando se establece en `false`, el escape hatch `dangerouslyDisableSandbox` se deshabilita completamente y todos los comandos deben ejecutarse en sandbox (o estar en `excludedCommands`). Útil para políticas empresariales que requieren sandboxing estricto. Predeterminado: true               | `false`                         |
| `filesystem.allowWrite`                | Rutas adicionales donde los comandos en sandbox pueden escribir. Las matrices se fusionan en todos los ámbitos de configuración: las rutas de usuario, proyecto y administradas se combinan, no se reemplazan. También se fusionan con rutas de reglas de permiso `Edit(...)` permitidas. Consulte [prefijos de ruta de sandbox](#sandbox-path-prefixes) a continuación.                                       | `["/tmp/build", "~/.kube"]`     |
| `filesystem.denyWrite`                 | Rutas donde los comandos en sandbox no pueden escribir. Las matrices se fusionan en todos los ámbitos de configuración. También se fusionan con rutas de reglas de permiso `Edit(...)` denegadas.                                                                                                                                                                                                              | `["/etc", "/usr/local/bin"]`    |
| `filesystem.denyRead`                  | Rutas donde los comandos en sandbox no pueden leer. Las matrices se fusionan en todos los ámbitos de configuración. También se fusionan con rutas de reglas de permiso `Read(...)` denegadas.                                                                                                                                                                                                                  | `["~/.aws/credentials"]`        |
| `filesystem.allowRead`                 | Rutas para permitir nuevamente la lectura dentro de regiones `denyRead`. Tiene precedencia sobre `denyRead`. Las matrices se fusionan en todos los ámbitos de configuración. Use esto para crear patrones de acceso de lectura solo para el espacio de trabajo.                                                                                                                                                | `["."]`                         |
| `filesystem.allowManagedReadPathsOnly` | (Solo configuraciones administradas) Solo se respetan rutas `allowRead` de configuraciones administradas. Las entradas `allowRead` de configuraciones de usuario, proyecto y local se ignoran. Predeterminado: false                                                                                                                                                                                           | `true`                          |
| `network.allowUnixSockets`             | Rutas de socket Unix accesibles en sandbox (para agentes SSH, etc.)                                                                                                                                                                                                                                                                                                                                            | `["~/.ssh/agent-socket"]`       |
| `network.allowAllUnixSockets`          | Permitir todas las conexiones de socket Unix en sandbox. Predeterminado: false                                                                                                                                                                                                                                                                                                                                 | `true`                          |
| `network.allowLocalBinding`            | Permitir vinculación a puertos localhost (solo macOS). Predeterminado: false                                                                                                                                                                                                                                                                                                                                   | `true`                          |
| `network.allowedDomains`               | Matriz de dominios para permitir tráfico de red saliente. Admite comodines (por ejemplo, `*.example.com`).                                                                                                                                                                                                                                                                                                     | `["github.com", "*.npmjs.org"]` |
| `network.allowManagedDomainsOnly`      | (Solo configuraciones administradas) Solo se respetan `allowedDomains` y reglas de permiso `WebFetch(domain:...)` permitidas de configuraciones administradas. Los dominios de configuraciones de usuario, proyecto y local se ignoran. Los dominios no permitidos se bloquean automáticamente sin solicitar al usuario. Los dominios denegados aún se respetan desde todas las fuentes. Predeterminado: false | `true`                          |
| `network.httpProxyPort`                | Puerto de proxy HTTP usado si desea traer su propio proxy. Si no se especifica, Claude ejecutará su propio proxy.                                                                                                                                                                                                                                                                                              | `8080`                          |
| `network.socksProxyPort`               | Puerto de proxy SOCKS5 usado si desea traer su propio proxy. Si no se especifica, Claude ejecutará su propio proxy.                                                                                                                                                                                                                                                                                            | `8081`                          |
| `enableWeakerNestedSandbox`            | Habilitar sandbox más débil para entornos Docker sin privilegios (solo Linux y WSL2). **Reduce la seguridad.** Predeterminado: false                                                                                                                                                                                                                                                                           | `true`                          |
| `enableWeakerNetworkIsolation`         | (Solo macOS) Permitir acceso al servicio de confianza TLS del sistema (`com.apple.trustd.agent`) en el sandbox. Requerido para herramientas basadas en Go como `gh`, `gcloud` y `terraform` para verificar certificados TLS cuando se usa `httpProxyPort` con un proxy MITM y CA personalizada. **Reduce la seguridad** al abrir una posible ruta de exfiltración de datos. Predeterminado: false              | `true`                          |

#### Prefijos de ruta de sandbox

Las rutas en `filesystem.allowWrite`, `filesystem.denyWrite`, `filesystem.denyRead` y `filesystem.allowRead` admiten estos prefijos:

| Prefijo            | Significado                                                                                                       | Ejemplo                                                                     |
| :----------------- | :---------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------- |
| `/`                | Ruta absoluta desde la raíz del sistema de archivos                                                               | `/tmp/build` se mantiene como `/tmp/build`                                  |
| `~/`               | Relativo al directorio de inicio                                                                                  | `~/.kube` se convierte en `$HOME/.kube`                                     |
| `./` o sin prefijo | Relativo a la raíz del proyecto para configuraciones de proyecto, o a `~/.claude` para configuraciones de usuario | `./output` en `.claude/settings.json` se resuelve a `<project-root>/output` |

El prefijo anterior `//path` para rutas absolutas aún funciona. Si anteriormente usó `/path` esperando resolución relativa al proyecto, cambie a `./path`. Esta sintaxis difiere de [reglas de permiso Read y Edit](/es/permissions#read-and-edit), que usan `//path` para absoluto y `/path` para relativo al proyecto. Las rutas del sistema de archivos de sandbox usan convenciones estándar: `/tmp/build` es una ruta absoluta.

**Ejemplo de configuración:**

```json  theme={null}
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker"],
    "filesystem": {
      "allowWrite": ["/tmp/build", "~/.kube"],
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
  La configuración `attribution` tiene precedencia sobre la configuración `includeCoAuthoredBy` obsoleta. Para ocultar toda la atribución, establezca `commit` y `pr` en cadenas vacías.
</Note>

### Configuración de sugerencia de archivo

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

Estas configuraciones controlan qué hooks se pueden ejecutar y a qué pueden acceder los hooks HTTP. La configuración `allowManagedHooksOnly` solo se puede configurar en [configuraciones administradas](#settings-files). Las listas blancas de URL y variables de entorno se pueden establecer en cualquier nivel de configuración y se fusionan entre fuentes.

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

Limitar qué nombres de variables de entorno pueden interpolar los hooks HTTP en valores de encabezado. El `allowedEnvVars` efectivo de cada hook es la intersección de su propia lista y esta configuración.

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
   * Configuraciones personales globales

Esta jerarquía asegura que las políticas organizacionales siempre se apliquen mientras aún permite que equipos e individuos personalicen su experiencia.

Por ejemplo, si su configuración de usuario permite `Bash(npm run *)` pero la configuración compartida de un proyecto la deniega, la configuración del proyecto tiene precedencia y el comando se bloquea.

<Note>
  **Las configuraciones de matriz se fusionan entre ámbitos.** Cuando la misma configuración con valor de matriz (como `sandbox.filesystem.allowWrite` o `permissions.allow`) aparece en múltiples ámbitos, las matrices se **concatenan y se deduplicán**, no se reemplazan. Esto significa que los ámbitos de menor prioridad pueden agregar entradas sin anular las establecidas por ámbitos de mayor prioridad, y viceversa. Por ejemplo, si las configuraciones administradas establecen `allowWrite` en `["/opt/company-tools"]` y un usuario agrega `["~/.kube"]`, ambas rutas se incluyen en la configuración final.
</Note>

### Verificar configuraciones activas

Ejecute `/status` dentro de Claude Code para ver qué fuentes de configuración están activas y de dónde provienen. La salida muestra cada capa de configuración (administrada, usuario, proyecto) junto con su origen, como `Enterprise managed settings (remote)`, `Enterprise managed settings (plist)`, `Enterprise managed settings (HKLM)`, o `Enterprise managed settings (file)`. Si un archivo de configuración contiene errores, `/status` reporta el problema para que pueda corregirlo.

### Puntos clave sobre el sistema de configuración

* **Archivos de memoria (`CLAUDE.md`)**: Contienen instrucciones y contexto que Claude carga al inicio
* **Archivos de configuración (JSON)**: Configurar permisos, variables de entorno y comportamiento de herramientas
* **Skills**: Indicaciones personalizadas que se pueden invocar con `/skill-name` o cargar automáticamente por Claude
* **MCP servers**: Extender Claude Code con herramientas e integraciones adicionales
* **Precedencia**: Las configuraciones de nivel superior (Managed) anulan las de nivel inferior (User/Project)
* **Herencia**: Las configuraciones se fusionan, con configuraciones más específicas agregando o anulando las más amplias

### Indicador del sistema

El indicador del sistema interno de Claude Code no se publica. Para agregar instrucciones personalizadas, use archivos `CLAUDE.md` o la bandera `--append-system-prompt`.

### Excluyendo archivos sensibles

Para evitar que Claude Code acceda a archivos que contienen información sensible como claves API, secretos y archivos de entorno, use la configuración `permissions.deny` en su archivo `.claude/settings.json`:

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

Esto reemplaza la configuración `ignorePatterns` obsoleta. Los archivos que coinciden con estos patrones se excluyen del descubrimiento de archivos y resultados de búsqueda, y las operaciones de lectura en estos archivos se deniegan.

## Configuración de subagents

Claude Code admite subagents de IA personalizados que se pueden configurar en niveles de usuario y proyecto. Estos subagents se almacenan como archivos Markdown con frontmatter YAML:

* **Subagents de usuario**: `~/.claude/agents/` - Disponibles en todos sus proyectos
* **Subagents de proyecto**: `.claude/agents/` - Específicos de su proyecto y se pueden compartir con su equipo

Los archivos de subagent definen asistentes de IA especializados con indicaciones personalizadas y permisos de herramientas. Obtenga más información sobre cómo crear y usar subagents en la [documentación de subagents](/es/sub-agents).

## Configuración de plugins

Claude Code admite un sistema de plugins que le permite extender la funcionalidad con skills, agentes, hooks y MCP servers. Los plugins se distribuyen a través de marketplaces y se pueden configurar en niveles de usuario y repositorio.

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

**Ámbitos**:

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

1. Los miembros del equipo reciben un aviso para instalar el marketplace cuando confían en la carpeta
2. Los miembros del equipo reciben un aviso para instalar plugins de ese marketplace
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
* `settings`: marketplace en línea declarado directamente en settings.json sin un repositorio alojado separado (usa `name` y `plugins`)

Use `source: 'settings'` para declarar un pequeño conjunto de plugins en línea sin configurar un repositorio de marketplace alojado. Los plugins listados aquí deben hacer referencia a fuentes externas como GitHub o npm. Aún necesita habilitar cada plugin por separado en `enabledPlugins`.

```json  theme={null}
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

**Solo configuraciones administradas**: Controla qué marketplaces de plugins se permite a los usuarios agregar. Esta configuración solo se puede configurar en [configuraciones administradas](/es/settings#settings-files) y proporciona a los administradores control estricto sobre fuentes de marketplace.

**Ubicaciones de archivos de configuraciones administradas**:

* **macOS**: `/Library/Application Support/ClaudeCode/managed-settings.json`
* **Linux y WSL**: `/etc/claude-code/managed-settings.json`
* **Windows**: `C:\Program Files\ClaudeCode\managed-settings.json`

**Características clave**:

* Solo disponible en configuraciones administradas (`managed-settings.json`)
* No puede ser anulada por configuraciones de usuario o proyecto (precedencia más alta)
* Se aplica ANTES de operaciones de red/sistema de archivos (las fuentes bloqueadas nunca se ejecutan)
* Usa coincidencia exacta para especificaciones de fuente (incluyendo `ref`, `path` para fuentes de git), excepto `hostPattern`, que usa coincidencia regex

**Comportamiento de lista blanca**:

* `undefined` (predeterminado): Sin restricciones - los usuarios pueden agregar cualquier marketplace
* Matriz vacía `[]`: Bloqueo completo - los usuarios no pueden agregar nuevos marketplaces
* Lista de fuentes: Los usuarios solo pueden agregar marketplaces que coincidan exactamente

**Todos los tipos de fuente admitidos**:

La lista blanca admite múltiples tipos de fuente de marketplace. La mayoría de las fuentes usan coincidencia exacta, mientras que `hostPattern` usa coincidencia regex contra el host del marketplace.

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
  Los marketplaces basados en URL solo descargan el archivo `marketplace.json`. No descargan archivos de plugins del servidor. Los plugins en marketplaces basados en URL deben usar fuentes externas (URLs de GitHub, npm o git) en lugar de rutas relativas. Para plugins con rutas relativas, use un marketplace basado en Git en su lugar. Consulte [Troubleshooting](/es/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces) para obtener detalles.
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

Use coincidencia de patrón de host cuando desee permitir todos los marketplaces de un host específico sin enumerar cada repositorio individualmente. Esto es útil para organizaciones con GitHub Enterprise interno o servidores GitLab donde los desarrolladores crean sus propios marketplaces.

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

**Usando ambos juntos**:

`strictKnownMarketplaces` es una puerta de política: controla qué pueden agregar los usuarios pero no registra ningún marketplace. Para restringir y pre-registrar un marketplace para todos los usuarios, establezca ambos en `managed-settings.json`:

```json  theme={null}
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

Las variables de entorno le permiten controlar el comportamiento de Claude Code sin editar archivos de configuración. Cualquier variable también se puede configurar en [`settings.json`](#available-settings) bajo la clave `env` para aplicarla a cada sesión o implementarla en su equipo.

Consulte la [referencia de variables de entorno](/es/env-vars) para la lista completa.

## Herramientas disponibles para Claude

Claude Code tiene acceso a un conjunto de herramientas para leer, editar, buscar, ejecutar comandos y orquestar subagents. Los nombres de herramientas son las cadenas exactas que utiliza en reglas de permiso y coincidencias de hooks.

Consulte la [referencia de herramientas](/es/tools-reference) para la lista completa y detalles del comportamiento de la herramienta Bash.

## Ver también

* [Permisos](/es/permissions): sistema de permisos, sintaxis de regla, patrones específicos de herramientas y políticas administradas
* [Autenticación](/es/authentication): configurar acceso de usuario a Claude Code
* [Troubleshooting](/es/troubleshooting): soluciones para problemas de configuración comunes
