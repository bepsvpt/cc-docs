> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Crear subagentes personalizados

> Cree y utilice subagentes de IA especializados en Claude Code para flujos de trabajo específicos de tareas y una mejor gestión del contexto.

Los subagentes son asistentes de IA especializados que manejan tipos específicos de tareas. Cada subagente se ejecuta en su propia ventana de contexto con un mensaje del sistema personalizado, acceso a herramientas específicas y permisos independientes. Cuando Claude encuentra una tarea que coincide con la descripción de un subagente, delega en ese subagente, que trabaja de forma independiente y devuelve resultados. Para ver el ahorro de contexto en la práctica, la [visualización de la ventana de contexto](/es/context-window) muestra un recorrido por una sesión donde un subagente maneja la investigación en su propia ventana separada.

<Note>
  Si necesita múltiples agentes trabajando en paralelo y comunicándose entre sí, consulte [equipos de agentes](/es/agent-teams) en su lugar. Los subagentes funcionan dentro de una única sesión; los equipos de agentes se coordinan entre sesiones separadas.
</Note>

Los subagentes le ayudan a:

* **Preservar contexto** manteniendo la exploración e implementación fuera de su conversación principal
* **Aplicar restricciones** limitando qué herramientas puede usar un subagente
* **Reutilizar configuraciones** en proyectos con subagentes a nivel de usuario
* **Especializar comportamiento** con mensajes del sistema enfocados para dominios específicos
* **Controlar costos** enrutando tareas a modelos más rápidos y económicos como Haiku

Claude utiliza la descripción de cada subagente para decidir cuándo delegar tareas. Cuando crea un subagente, escriba una descripción clara para que Claude sepa cuándo usarlo.

Claude Code incluye varios subagentes integrados como **Explore**, **Plan** y **general-purpose**. También puede crear subagentes personalizados para manejar tareas específicas. Esta página cubre los [subagentes integrados](#built-in-subagents), [cómo crear los suyos](#quickstart-create-your-first-subagent), [opciones de configuración completas](#configure-subagents), [patrones para trabajar con subagentes](#work-with-subagents) y [subagentes de ejemplo](#example-subagents).

## Subagentes integrados

Claude Code incluye subagentes integrados que Claude utiliza automáticamente cuando es apropiado. Cada uno hereda los permisos de la conversación principal con restricciones de herramientas adicionales.

<Tabs>
  <Tab title="Explore">
    Un agente rápido y de solo lectura optimizado para buscar y analizar bases de código.

    * **Modelo**: Haiku (rápido, baja latencia)
    * **Herramientas**: Herramientas de solo lectura (acceso denegado a herramientas Write y Edit)
    * **Propósito**: Descubrimiento de archivos, búsqueda de código, exploración de base de código

    Claude delega en Explore cuando necesita buscar o entender una base de código sin hacer cambios. Esto mantiene los resultados de exploración fuera del contexto de su conversación principal.

    Al invocar Explore, Claude especifica un nivel de minuciosidad: **quick** para búsquedas dirigidas, **medium** para exploración equilibrada, o **very thorough** para análisis exhaustivo.
  </Tab>

  <Tab title="Plan">
    Un agente de investigación utilizado durante [plan mode](/es/common-workflows#use-plan-mode-for-safe-code-analysis) para recopilar contexto antes de presentar un plan.

    * **Modelo**: Hereda de la conversación principal
    * **Herramientas**: Herramientas de solo lectura (acceso denegado a herramientas Write y Edit)
    * **Propósito**: Investigación de base de código para planificación

    Cuando está en plan mode y Claude necesita entender su base de código, delega la investigación al subagente Plan. Esto evita el anidamiento infinito (los subagentes no pueden generar otros subagentes) mientras sigue recopilando el contexto necesario.
  </Tab>

  <Tab title="General-purpose">
    Un agente capaz para tareas complejas de múltiples pasos que requieren tanto exploración como acción.

    * **Modelo**: Hereda de la conversación principal
    * **Herramientas**: Todas las herramientas
    * **Propósito**: Investigación compleja, operaciones de múltiples pasos, modificaciones de código

    Claude delega en general-purpose cuando la tarea requiere tanto exploración como modificación, razonamiento complejo para interpretar resultados, o múltiples pasos dependientes.
  </Tab>

  <Tab title="Other">
    Claude Code incluye agentes auxiliares adicionales para tareas específicas. Estos se invocan típicamente automáticamente, por lo que no necesita usarlos directamente.

    | Agente            | Modelo | Cuándo Claude lo usa                                            |
    | :---------------- | :----- | :-------------------------------------------------------------- |
    | statusline-setup  | Sonnet | Cuando ejecuta `/statusline` para configurar su línea de estado |
    | Claude Code Guide | Haiku  | Cuando hace preguntas sobre características de Claude Code      |
  </Tab>
</Tabs>

Más allá de estos subagentes integrados, puede crear los suyos propios con mensajes personalizados, restricciones de herramientas, modos de permisos, hooks y skills. Las siguientes secciones muestran cómo comenzar y personalizar subagentes.

## Inicio rápido: crear su primer subagente

Los subagentes se definen en archivos Markdown con frontmatter YAML. Puede [crearlos manualmente](#write-subagent-files) o usar el comando `/agents`.

Este tutorial lo guía a través de la creación de un subagente a nivel de usuario con el comando `/agents`. El subagente revisa código y sugiere mejoras para la base de código.

<Steps>
  <Step title="Abrir la interfaz de subagentes">
    En Claude Code, ejecute:

    ```text theme={null}
    /agents
    ```
  </Step>

  <Step title="Elegir una ubicación">
    Seleccione **Create new agent**, luego elija **Personal**. Esto guarda el subagente en `~/.claude/agents/` para que esté disponible en todos sus proyectos.
  </Step>

  <Step title="Generar con Claude">
    Seleccione **Generate with Claude**. Cuando se le solicite, describa el subagente:

    ```text theme={null}
    A code improvement agent that scans files and suggests improvements
    for readability, performance, and best practices. It should explain
    each issue, show the current code, and provide an improved version.
    ```

    Claude genera el identificador, descripción y mensaje del sistema para usted.
  </Step>

  <Step title="Seleccionar herramientas">
    Para un revisor de solo lectura, deseleccione todo excepto **Read-only tools**. Si mantiene todas las herramientas seleccionadas, el subagente hereda todas las herramientas disponibles para la conversación principal.
  </Step>

  <Step title="Seleccionar modelo">
    Elija qué modelo usa el subagente. Para este agente de ejemplo, seleccione **Sonnet**, que equilibra capacidad y velocidad para analizar patrones de código.
  </Step>

  <Step title="Elegir un color">
    Elija un color de fondo para el subagente. Esto le ayuda a identificar qué subagente se está ejecutando en la interfaz de usuario.
  </Step>

  <Step title="Configurar memoria">
    Seleccione **User scope** para dar al subagente un [directorio de memoria persistente](#enable-persistent-memory) en `~/.claude/agent-memory/`. El subagente usa esto para acumular insights entre conversaciones, como patrones de base de código y problemas recurrentes. Seleccione **None** si no desea que el subagente persista aprendizajes.
  </Step>

  <Step title="Guardar e intentarlo">
    Revise el resumen de configuración. Presione `s` o `Enter` para guardar, o presione `e` para guardar y editar el archivo en su editor. El subagente está disponible inmediatamente. Intente:

    ```text theme={null}
    Use the code-improver agent to suggest improvements in this project
    ```

    Claude delega en su nuevo subagente, que escanea la base de código y devuelve sugerencias de mejora.
  </Step>
</Steps>

Ahora tiene un subagente que puede usar en cualquier proyecto en su máquina para analizar bases de código y sugerir mejoras.

También puede crear subagentes manualmente como archivos Markdown, definirlos mediante banderas CLI, o distribuirlos a través de plugins. Las siguientes secciones cubren todas las opciones de configuración.

## Configurar subagentes

### Usar el comando /agents

El comando `/agents` proporciona una interfaz interactiva para administrar subagentes. Ejecute `/agents` para:

* Ver todos los subagentes disponibles (integrados, usuario, proyecto y plugin)
* Crear nuevos subagentes con configuración guiada o generación de Claude
* Editar la configuración de subagentes existentes y el acceso a herramientas
* Eliminar subagentes personalizados
* Ver qué subagentes están activos cuando existen duplicados

Esta es la forma recomendada de crear y administrar subagentes. Para creación manual o automatización, también puede agregar archivos de subagentes directamente.

Para enumerar todos los subagentes configurados desde la línea de comandos sin iniciar una sesión interactiva, ejecute `claude agents`. Esto muestra agentes agrupados por fuente e indica cuáles se anulan por definiciones de mayor prioridad.

### Elegir el alcance del subagente

Los subagentes son archivos Markdown con frontmatter YAML. Guárdelos en diferentes ubicaciones según el alcance. Cuando múltiples subagentes comparten el mismo nombre, la ubicación de mayor prioridad gana.

| Ubicación                       | Alcance                         | Prioridad    | Cómo crear                                                          |
| :------------------------------ | :------------------------------ | :----------- | :------------------------------------------------------------------ |
| Configuración administrada      | Toda la organización            | 1 (más alta) | Implementado a través de [configuración administrada](/es/settings) |
| Bandera CLI `--agents`          | Sesión actual                   | 2            | Pasar JSON al lanzar Claude Code                                    |
| `.claude/agents/`               | Proyecto actual                 | 3            | Interactivo o manual                                                |
| `~/.claude/agents/`             | Todos sus proyectos             | 4            | Interactivo o manual                                                |
| Directorio `agents/` del plugin | Donde el plugin está habilitado | 5 (más baja) | Instalado con [plugins](/es/plugins)                                |

**Los subagentes de proyecto** (`.claude/agents/`) son ideales para subagentes específicos de una base de código. Verifíquelos en control de versiones para que su equipo pueda usarlos y mejorarlos colaborativamente.

Los subagentes se descubren caminando hacia arriba desde el directorio de trabajo actual. Los directorios agregados con `--add-dir` [otorgan acceso a archivos solamente](/es/permissions#additional-directories-grant-file-access-not-configuration) y no se escanean para subagentes. Para compartir subagentes entre proyectos, use `~/.claude/agents/` o un [plugin](/es/plugins).

**Los subagentes de usuario** (`~/.claude/agents/`) son subagentes personales disponibles en todos sus proyectos.

**Los subagentes definidos por CLI** se pasan como JSON al lanzar Claude Code. Existen solo para esa sesión y no se guardan en disco, lo que los hace útiles para pruebas rápidas o scripts de automatización. Puede definir múltiples subagentes en una única llamada `--agents`:

```bash theme={null}
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

La bandera `--agents` acepta JSON con los mismos campos de [frontmatter](#supported-frontmatter-fields) que los subagentes basados en archivos: `description`, `prompt`, `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `effort`, `background`, `isolation` y `color`. Use `prompt` para el mensaje del sistema, equivalente al cuerpo markdown en subagentes basados en archivos.

**Los subagentes administrados** son implementados por administradores de la organización. Coloque archivos markdown en `.claude/agents/` dentro del [directorio de configuración administrada](/es/settings#settings-files), usando el mismo formato de frontmatter que los subagentes de proyecto y usuario. Las definiciones administradas tienen precedencia sobre los subagentes de proyecto y usuario con el mismo nombre.

**Los subagentes de plugin** provienen de [plugins](/es/plugins) que ha instalado. Aparecen en `/agents` junto a sus subagentes personalizados. Consulte la [referencia de componentes de plugin](/es/plugins-reference#agents) para obtener detalles sobre la creación de subagentes de plugin.

<Note>
  Por razones de seguridad, los subagentes de plugin no soportan los campos de frontmatter `hooks`, `mcpServers`, o `permissionMode`. Estos campos se ignoran al cargar agentes desde un plugin. Si los necesita, copie el archivo del agente en `.claude/agents/` o `~/.claude/agents/`. También puede agregar reglas a [`permissions.allow`](/es/settings#permission-settings) en `settings.json` o `settings.local.json`, pero estas reglas se aplican a toda la sesión, no solo al subagente del plugin.
</Note>

Las definiciones de subagentes de cualquiera de estos alcances también están disponibles para [equipos de agentes](/es/agent-teams#use-subagent-definitions-for-teammates): al generar un compañero de equipo, puede hacer referencia a un tipo de subagente y el compañero hereda su mensaje del sistema, herramientas y modelo.

### Escribir archivos de subagentes

Los archivos de subagentes usan frontmatter YAML para configuración, seguido del mensaje del sistema en Markdown:

<Note>
  Los subagentes se cargan al inicio de la sesión. Si crea un subagente agregando manualmente un archivo, reinicie su sesión o use `/agents` para cargarlo inmediatamente.
</Note>

```markdown theme={null}
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

El frontmatter define los metadatos y la configuración del subagente. El cuerpo se convierte en el mensaje del sistema que guía el comportamiento del subagente. Los subagentes reciben solo este mensaje del sistema (más detalles básicos del entorno como el directorio de trabajo), no el mensaje del sistema completo de Claude Code.

#### Campos de frontmatter soportados

Los siguientes campos se pueden usar en el frontmatter YAML. Solo `name` y `description` son requeridos.

| Campo             | Requerido | Descripción                                                                                                                                                                                                                                                                                                                           |
| :---------------- | :-------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `name`            | Sí        | Identificador único usando letras minúsculas y guiones                                                                                                                                                                                                                                                                                |
| `description`     | Sí        | Cuándo Claude debe delegar en este subagente                                                                                                                                                                                                                                                                                          |
| `tools`           | No        | [Herramientas](#available-tools) que el subagente puede usar. Hereda todas las herramientas si se omite                                                                                                                                                                                                                               |
| `disallowedTools` | No        | Herramientas a denegar, eliminadas de la lista heredada o especificada                                                                                                                                                                                                                                                                |
| `model`           | No        | [Modelo](#choose-a-model) a usar: `sonnet`, `opus`, `haiku`, un ID de modelo completo (por ejemplo, `claude-opus-4-6`), o `inherit`. Por defecto es `inherit`                                                                                                                                                                         |
| `permissionMode`  | No        | [Modo de permiso](#permission-modes): `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, o `plan`                                                                                                                                                                                                                      |
| `maxTurns`        | No        | Número máximo de turnos de agente antes de que el subagente se detenga                                                                                                                                                                                                                                                                |
| `skills`          | No        | [Skills](/es/skills) a cargar en el contexto del subagente al inicio. El contenido completo de la skill se inyecta, no solo se pone disponible para invocación. Los subagentes no heredan skills de la conversación principal                                                                                                         |
| `mcpServers`      | No        | [Servidores MCP](/es/mcp) disponibles para este subagente. Cada entrada es un nombre de servidor que hace referencia a un servidor ya configurado (por ejemplo, `"slack"`) o una definición en línea con el nombre del servidor como clave y una [configuración completa del servidor MCP](/es/mcp#installing-mcp-servers) como valor |
| `hooks`           | No        | [Hooks de ciclo de vida](#define-hooks-for-subagents) limitados a este subagente                                                                                                                                                                                                                                                      |
| `memory`          | No        | [Alcance de memoria persistente](#enable-persistent-memory): `user`, `project`, o `local`. Habilita aprendizaje entre sesiones                                                                                                                                                                                                        |
| `background`      | No        | Establecer en `true` para ejecutar siempre este subagente como una [tarea de fondo](#run-subagents-in-foreground-or-background). Por defecto: `false`                                                                                                                                                                                 |
| `effort`          | No        | Nivel de esfuerzo cuando este subagente está activo. Anula el nivel de esfuerzo de la sesión. Por defecto: hereda de la sesión. Opciones: `low`, `medium`, `high`, `max` (solo Opus 4.6)                                                                                                                                              |
| `isolation`       | No        | Establecer en `worktree` para ejecutar el subagente en un [git worktree](/es/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) temporal, dándole una copia aislada del repositorio. El worktree se limpia automáticamente si el subagente no realiza cambios                                                     |
| `color`           | No        | Color de visualización para el subagente en la lista de tareas y transcripción. Acepta `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, o `cyan`                                                                                                                                                                         |
| `initialPrompt`   | No        | Se envía automáticamente como el primer turno de usuario cuando este agente se ejecuta como el agente de sesión principal (a través de `--agent` o la configuración `agent`). Se procesan [comandos](/es/commands) y [skills](/es/skills). Se antepone a cualquier mensaje proporcionado por el usuario                               |

### Elegir un modelo

El campo `model` controla qué [modelo de IA](/es/model-config) usa el subagente:

* **Alias de modelo**: Use uno de los alias disponibles: `sonnet`, `opus`, o `haiku`
* **ID de modelo completo**: Use un ID de modelo completo como `claude-opus-4-6` o `claude-sonnet-4-6`. Acepta los mismos valores que la bandera `--model`
* **inherit**: Use el mismo modelo que la conversación principal
* **Omitido**: Si no se especifica, por defecto es `inherit` (usa el mismo modelo que la conversación principal)

Cuando Claude invoca un subagente, también puede pasar un parámetro `model` para esa invocación específica. Claude Code resuelve el modelo del subagente en este orden:

1. La variable de entorno [`CLAUDE_CODE_SUBAGENT_MODEL`](/es/model-config#environment-variables), si está establecida
2. El parámetro `model` por invocación
3. El frontmatter `model` de la definición del subagente
4. El modelo de la conversación principal

### Controlar capacidades de subagentes

Puede controlar qué pueden hacer los subagentes a través del acceso a herramientas, modos de permisos y reglas condicionales.

#### Herramientas disponibles

Los subagentes pueden usar cualquiera de las [herramientas internas](/es/tools-reference) de Claude Code. Por defecto, los subagentes heredan todas las herramientas de la conversación principal, incluidas las herramientas MCP.

Para restringir herramientas, use el campo `tools` (lista blanca) o el campo `disallowedTools` (lista negra). Este ejemplo usa `tools` para permitir exclusivamente Read, Grep, Glob y Bash. El subagente no puede editar archivos, escribir archivos, o usar ninguna herramienta MCP:

```yaml theme={null}
---
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
---
```

Este ejemplo usa `disallowedTools` para heredar todas las herramientas de la conversación principal excepto Write y Edit. El subagente mantiene Bash, herramientas MCP y todo lo demás:

```yaml theme={null}
---
name: no-writes
description: Inherits every tool except file writes
disallowedTools: Write, Edit
---
```

Si ambos se establecen, `disallowedTools` se aplica primero, luego `tools` se resuelve contra el grupo restante. Una herramienta listada en ambos se elimina.

#### Restringir qué subagentes pueden ser generados

Cuando un agente se ejecuta como el hilo principal con `claude --agent`, puede generar subagentes usando la herramienta Agent. Para restringir qué tipos de subagentes puede generar, use la sintaxis `Agent(agent_type)` en el campo `tools`.

<Note>En la versión 2.1.63, la herramienta Task fue renombrada a Agent. Las referencias existentes a `Task(...)` en configuraciones y definiciones de agentes aún funcionan como alias.</Note>

```yaml theme={null}
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---
```

Esta es una lista blanca: solo los subagentes `worker` y `researcher` pueden ser generados. Si el agente intenta generar cualquier otro tipo, la solicitud falla y el agente solo ve los tipos permitidos en su mensaje. Para bloquear agentes específicos mientras se permiten todos los demás, use [`permissions.deny`](#disable-specific-subagents) en su lugar.

Para permitir generar cualquier subagente sin restricciones, use `Agent` sin paréntesis:

```yaml theme={null}
tools: Agent, Read, Bash
```

Si `Agent` se omite completamente de la lista `tools`, el agente no puede generar ningún subagente. Esta restricción solo se aplica a agentes que se ejecutan como el hilo principal con `claude --agent`. Los subagentes no pueden generar otros subagentes, por lo que `Agent(agent_type)` no tiene efecto en definiciones de subagentes.

#### Alcance de servidores MCP a un subagente

Use el campo `mcpServers` para dar a un subagente acceso a servidores [MCP](/es/mcp) que no están disponibles en la conversación principal. Los servidores en línea definidos aquí se conectan cuando el subagente comienza y se desconectan cuando termina. Las referencias de cadena comparten la conexión de la sesión principal.

Cada entrada en la lista es una definición de servidor en línea o una cadena que hace referencia a un servidor MCP ya configurado en su sesión:

```yaml theme={null}
---
name: browser-tester
description: Tests features in a real browser using Playwright
mcpServers:
  # Inline definition: scoped to this subagent only
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  # Reference by name: reuses an already-configured server
  - github
---

Use the Playwright tools to navigate, screenshot, and interact with pages.
```

Las definiciones en línea usan el mismo esquema que las entradas del servidor `.mcp.json` (`stdio`, `http`, `sse`, `ws`), con clave del nombre del servidor.

Para mantener un servidor MCP fuera de la conversación principal por completo y evitar que sus descripciones de herramientas consuman contexto allí, defínalo en línea aquí en lugar de en `.mcp.json`. El subagente obtiene las herramientas; la conversación principal no.

#### Modos de permiso

El campo `permissionMode` controla cómo el subagente maneja solicitudes de permiso. Los subagentes heredan el contexto de permiso de la conversación principal y pueden anular el modo, excepto cuando el modo principal tiene precedencia como se describe a continuación.

| Modo                | Comportamiento                                                                                                               |
| :------------------ | :--------------------------------------------------------------------------------------------------------------------------- |
| `default`           | Verificación de permiso estándar con solicitudes                                                                             |
| `acceptEdits`       | Aceptar automáticamente ediciones de archivo excepto en directorios protegidos                                               |
| `auto`              | [Modo auto](/es/permission-modes#eliminate-prompts-with-auto-mode): un clasificador de IA evalúa cada llamada de herramienta |
| `dontAsk`           | Denegar automáticamente solicitudes de permiso (las herramientas explícitamente permitidas aún funcionan)                    |
| `bypassPermissions` | Omitir solicitudes de permiso                                                                                                |
| `plan`              | Modo plan (exploración de solo lectura)                                                                                      |

<Warning>
  Use `bypassPermissions` con cuidado. Omite solicitudes de permiso, permitiendo que el subagente ejecute operaciones sin aprobación. Las escrituras en directorios `.git`, `.claude`, `.vscode`, `.idea` y `.husky` aún solicitan confirmación, excepto para `.claude/commands`, `.claude/agents` y `.claude/skills`. Consulte [modos de permiso](/es/permission-modes#skip-all-checks-with-bypasspermissions-mode) para detalles.
</Warning>

Si el principal usa `bypassPermissions`, esto tiene precedencia y no puede ser anulado. Si el principal usa [modo auto](/es/permission-modes#eliminate-prompts-with-auto-mode), el subagente hereda modo auto y cualquier `permissionMode` en su frontmatter se ignora: el clasificador evalúa las llamadas de herramientas del subagente con las mismas reglas de bloqueo y permiso que la sesión principal.

#### Precargar skills en subagentes

Use el campo `skills` para inyectar contenido de skill en el contexto de un subagente al inicio. Esto da al subagente conocimiento de dominio sin requerir que descubra y cargue skills durante la ejecución.

```yaml theme={null}
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---

Implement API endpoints. Follow the conventions and patterns from the preloaded skills.
```

El contenido completo de cada skill se inyecta en el contexto del subagente, no solo se pone disponible para invocación. Los subagentes no heredan skills de la conversación principal; debe enumerarlas explícitamente.

<Note>
  Esto es lo inverso de [ejecutar una skill en un subagente](/es/skills#run-skills-in-a-subagent). Con `skills` en un subagente, el subagente controla el mensaje del sistema y carga contenido de skill. Con `context: fork` en una skill, el contenido de la skill se inyecta en el agente que especifique. Ambos usan el mismo sistema subyacente.
</Note>

#### Habilitar memoria persistente

El campo `memory` da al subagente un directorio persistente que sobrevive entre conversaciones. El subagente usa este directorio para acumular conocimiento con el tiempo, como patrones de base de código, insights de depuración y decisiones arquitectónicas.

```yaml theme={null}
---
name: code-reviewer
description: Reviews code for quality and best practices
memory: user
---

You are a code reviewer. As you review code, update your agent memory with
patterns, conventions, and recurring issues you discover.
```

Elija un alcance basado en qué tan ampliamente debe aplicarse la memoria:

| Alcance   | Ubicación                                     | Usar cuando                                                                                                  |
| :-------- | :-------------------------------------------- | :----------------------------------------------------------------------------------------------------------- |
| `user`    | `~/.claude/agent-memory/<name-of-agent>/`     | el subagente debe recordar aprendizajes en todos los proyectos                                               |
| `project` | `.claude/agent-memory/<name-of-agent>/`       | el conocimiento del subagente es específico del proyecto y compartible a través de control de versiones      |
| `local`   | `.claude/agent-memory-local/<name-of-agent>/` | el conocimiento del subagente es específico del proyecto pero no debe ser verificado en control de versiones |

Cuando la memoria está habilitada:

* El mensaje del sistema del subagente incluye instrucciones para leer y escribir en el directorio de memoria.
* El mensaje del sistema del subagente también incluye las primeras 200 líneas o 25KB de `MEMORY.md` en el directorio de memoria, lo que sea menor, con instrucciones para curar `MEMORY.md` si excede ese límite.
* Las herramientas Read, Write y Edit se habilitan automáticamente para que el subagente pueda administrar sus archivos de memoria.

##### Consejos de memoria persistente

* `project` es el alcance predeterminado recomendado. Hace que el conocimiento del subagente sea compartible a través de control de versiones. Use `user` cuando el conocimiento del subagente es ampliamente aplicable en proyectos, o `local` cuando el conocimiento no debe ser verificado en control de versiones.
* Pida al subagente que consulte su memoria antes de comenzar el trabajo: "Review this PR, and check your memory for patterns you've seen before."
* Pida al subagente que actualice su memoria después de completar una tarea: "Now that you're done, save what you learned to your memory." Con el tiempo, esto construye una base de conocimiento que hace que el subagente sea más efectivo.
* Incluya instrucciones de memoria directamente en el archivo markdown del subagente para que mantenga proactivamente su propia base de conocimiento:

  ```markdown theme={null}
  Update your agent memory as you discover codepaths, patterns, library
  locations, and key architectural decisions. This builds up institutional
  knowledge across conversations. Write concise notes about what you found
  and where.
  ```

#### Reglas condicionales con hooks

Para un control más dinámico sobre el uso de herramientas, use hooks `PreToolUse` para validar operaciones antes de que se ejecuten. Esto es útil cuando necesita permitir algunas operaciones de una herramienta mientras bloquea otras.

Este ejemplo crea un subagente que solo permite consultas de base de datos de solo lectura. El hook `PreToolUse` ejecuta el script especificado en `command` antes de que se ejecute cada comando Bash:

```yaml theme={null}
---
name: db-reader
description: Execute read-only database queries
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---
```

Claude Code [pasa la entrada del hook como JSON](/es/hooks#pretooluse-input) a través de stdin a comandos de hook. El script de validación lee este JSON, extrae el comando Bash y [sale con código 2](/es/hooks#exit-code-2-behavior-per-event) para bloquear operaciones de escritura:

```bash theme={null}
#!/bin/bash
# ./scripts/validate-readonly-query.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block SQL write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b' > /dev/null; then
  echo "Blocked: Only SELECT queries are allowed" >&2
  exit 2
fi

exit 0
```

Consulte [Hook input](/es/hooks#pretooluse-input) para el esquema de entrada completo y [códigos de salida](/es/hooks#exit-code-output) para cómo los códigos de salida afectan el comportamiento.

#### Deshabilitar subagentes específicos

Puede evitar que Claude use subagentes específicos agregándolos a la matriz `deny` en su [configuración](/es/settings#permission-settings). Use el formato `Agent(subagent-name)` donde `subagent-name` coincida con el campo name del subagente.

```json theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}
```

Esto funciona para subagentes integrados y personalizados. También puede usar la bandera CLI `--disallowedTools`:

```bash theme={null}
claude --disallowedTools "Agent(Explore)"
```

Consulte la [documentación de Permisos](/es/permissions#tool-specific-permission-rules) para más detalles sobre reglas de permisos.

### Definir hooks para subagentes

Los subagentes pueden definir [hooks](/es/hooks) que se ejecutan durante el ciclo de vida del subagente. Hay dos formas de configurar hooks:

1. **En el frontmatter del subagente**: Defina hooks que se ejecuten solo mientras ese subagente está activo
2. **En `settings.json`**: Defina hooks que se ejecuten en la sesión principal cuando los subagentes comienzan o se detienen

#### Hooks en frontmatter de subagentes

Defina hooks directamente en el archivo markdown del subagente. Estos hooks solo se ejecutan mientras ese subagente específico está activo y se limpian cuando termina.

Se soportan todos los [eventos de hook](/es/hooks#hook-events). Los eventos más comunes para subagentes son:

| Evento        | Entrada del matcher   | Cuándo se dispara                                                                |
| :------------ | :-------------------- | :------------------------------------------------------------------------------- |
| `PreToolUse`  | Nombre de herramienta | Antes de que el subagente use una herramienta                                    |
| `PostToolUse` | Nombre de herramienta | Después de que el subagente usa una herramienta                                  |
| `Stop`        | (ninguno)             | Cuando el subagente termina (convertido a `SubagentStop` en tiempo de ejecución) |

Este ejemplo valida comandos Bash con el hook `PreToolUse` y ejecuta un linter después de ediciones de archivo con `PostToolUse`:

```yaml theme={null}
---
name: code-reviewer
description: Review code changes with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh $TOOL_INPUT"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

Los hooks `Stop` en frontmatter se convierten automáticamente a eventos `SubagentStop`.

#### Hooks a nivel de proyecto para eventos de subagentes

Configure hooks en `settings.json` que respondan a eventos de ciclo de vida de subagentes en la sesión principal.

| Evento          | Entrada del matcher      | Cuándo se dispara                         |
| :-------------- | :----------------------- | :---------------------------------------- |
| `SubagentStart` | Nombre de tipo de agente | Cuando un subagente comienza la ejecución |
| `SubagentStop`  | Nombre de tipo de agente | Cuando un subagente se completa           |

Ambos eventos soportan matchers para dirigirse a tipos de agentes específicos por nombre. Este ejemplo ejecuta un script de configuración solo cuando el subagente `db-agent` comienza, y un script de limpieza cuando cualquier subagente se detiene:

```json theme={null}
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/setup-db-connection.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/cleanup-db-connection.sh" }
        ]
      }
    ]
  }
}
```

Consulte [Hooks](/es/hooks) para el formato de configuración de hook completo.

## Trabajar con subagentes

### Entender delegación automática

Claude delega automáticamente tareas basadas en la descripción de la tarea en su solicitud, el campo `description` en configuraciones de subagentes y el contexto actual. Para alentar delegación proactiva, incluya frases como "use proactively" en el campo description de su subagente.

### Invocar subagentes explícitamente

Cuando la delegación automática no es suficiente, puede solicitar un subagente usted mismo. Tres patrones escalan desde una sugerencia única a un valor predeterminado de sesión completa:

* **Lenguaje natural**: nombre el subagente en su solicitud; Claude decide si delegar
* **@-mention**: garantiza que el subagente se ejecute para una tarea
* **Sesión completa**: toda la sesión usa el mensaje del sistema del subagente, restricciones de herramientas y modelo a través de la bandera `--agent` o la configuración `agent`

Para lenguaje natural, no hay sintaxis especial. Nombre el subagente y Claude típicamente delega:

```text theme={null}
Use the test-runner subagent to fix failing tests
Have the code-reviewer subagent look at my recent changes
```

**@-mention el subagente.** Escriba `@` y elija el subagente del typeahead, de la misma manera que @-menciona archivos. Esto asegura que ese subagente específico se ejecute en lugar de dejar la opción a Claude:

```text theme={null}
@"code-reviewer (agent)" look at the auth changes
```

Su mensaje completo aún va a Claude, que escribe el mensaje de tarea del subagente basado en lo que pidió. El @-mention controla qué subagente Claude invoca, no qué mensaje recibe.

Los subagentes proporcionados por un [plugin](/es/plugins) habilitado aparecen en el typeahead como `<plugin-name>:<agent-name>`. Los subagentes de fondo nombrados actualmente en ejecución en la sesión también aparecen en el typeahead, mostrando su estado junto al nombre. También puede escribir la mención manualmente sin usar el selector: `@agent-<name>` para subagentes locales, o `@agent-<plugin-name>:<agent-name>` para subagentes de plugin.

**Ejecute toda la sesión como un subagente.** Pase [`--agent <name>`](/es/cli-reference) para iniciar una sesión donde el hilo principal en sí toma el mensaje del sistema del subagente, restricciones de herramientas y modelo:

```bash theme={null}
claude --agent code-reviewer
```

El mensaje del sistema del subagente reemplaza completamente el mensaje del sistema predeterminado de Claude Code, de la misma manera que [`--system-prompt`](/es/cli-reference) lo hace. Los archivos `CLAUDE.md` y la memoria del proyecto aún se cargan a través del flujo de mensajes normal. El nombre del agente aparece como `@<name>` en el encabezado de inicio para que pueda confirmar que está activo.

Esto funciona con subagentes integrados y personalizados, y la opción persiste cuando reanuda la sesión.

Para un subagente proporcionado por plugin, pase el nombre con alcance: `claude --agent <plugin-name>:<agent-name>`.

Para hacerlo el predeterminado para cada sesión en un proyecto, establezca `agent` en `.claude/settings.json`:

```json theme={null}
{
  "agent": "code-reviewer"
}
```

La bandera CLI anula la configuración si ambas están presentes.

### Ejecutar subagentes en primer plano o fondo

Los subagentes pueden ejecutarse en primer plano (bloqueante) o fondo (concurrente):

* **Subagentes en primer plano** bloquean la conversación principal hasta completarse. Las solicitudes de permiso y preguntas aclaratorias (como [`AskUserQuestion`](/es/tools-reference)) se le pasan a usted.
* **Subagentes en fondo** se ejecutan concurrentemente mientras continúa trabajando. Antes de lanzar, Claude Code solicita permisos de herramientas que el subagente necesitará, asegurando que tenga las aprobaciones necesarias por adelantado. Una vez en ejecución, el subagente hereda estos permisos y deniega automáticamente cualquier cosa no preaprobada. Si un subagente en fondo necesita hacer preguntas aclaratorias, esa llamada de herramienta falla pero el subagente continúa.

Si un subagente en fondo falla debido a permisos faltantes, puede iniciar un nuevo subagente en primer plano con la misma tarea para reintentar con solicitudes interactivas.

Claude decide si ejecutar subagentes en primer plano o fondo basado en la tarea. También puede:

* Pedir a Claude que "run this in the background"
* Presionar **Ctrl+B** para poner en fondo una tarea en ejecución

Para deshabilitar toda la funcionalidad de tareas en fondo, establezca la variable de entorno `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` en `1`. Consulte [Variables de entorno](/es/env-vars).

### Patrones comunes

#### Aislar operaciones de alto volumen

Uno de los usos más efectivos para subagentes es aislar operaciones que producen grandes cantidades de salida. Ejecutar pruebas, obtener documentación o procesar archivos de registro puede consumir contexto significativo. Al delegar estos a un subagente, la salida detallada permanece en el contexto del subagente mientras solo el resumen relevante regresa a su conversación principal.

```text theme={null}
Use a subagent to run the test suite and report only the failing tests with their error messages
```

#### Ejecutar investigación en paralelo

Para investigaciones independientes, genere múltiples subagentes para trabajar simultáneamente:

```text theme={null}
Research the authentication, database, and API modules in parallel using separate subagents
```

Cada subagente explora su área independientemente, luego Claude sintetiza los hallazgos. Esto funciona mejor cuando las rutas de investigación no dependen una de la otra.

<Warning>
  Cuando los subagentes se completan, sus resultados regresan a su conversación principal. Ejecutar muchos subagentes que cada uno devuelve resultados detallados puede consumir contexto significativo.
</Warning>

Para tareas que necesitan paralelismo sostenido o exceden su ventana de contexto, [equipos de agentes](/es/agent-teams) dan a cada trabajador su propio contexto independiente.

#### Encadenar subagentes

Para flujos de trabajo de múltiples pasos, pida a Claude que use subagentes en secuencia. Cada subagente completa su tarea y devuelve resultados a Claude, que luego pasa contexto relevante al siguiente subagente.

```text theme={null}
Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them
```

### Elegir entre subagentes y conversación principal

Use la **conversación principal** cuando:

* La tarea necesita ida y vuelta frecuente o refinamiento iterativo
* Múltiples fases comparten contexto significativo (planificación → implementación → prueba)
* Está haciendo un cambio rápido y dirigido
* La latencia importa. Los subagentes comienzan frescos y pueden necesitar tiempo para recopilar contexto

Use **subagentes** cuando:

* La tarea produce salida detallada que no necesita en su contexto principal
* Desea aplicar restricciones de herramientas específicas o permisos
* El trabajo es autónomo y puede devolver un resumen

Considere [Skills](/es/skills) en su lugar cuando desee mensajes reutilizables o flujos de trabajo que se ejecuten en el contexto de conversación principal en lugar de contexto de subagente aislado.

Para una pregunta rápida sobre algo ya en su conversación, use [`/btw`](/es/interactive-mode#side-questions-with-btw) en lugar de un subagente. Ve su contexto completo pero no tiene acceso a herramientas, y la respuesta se descarta en lugar de agregarse al historial.

<Note>
  Los subagentes no pueden generar otros subagentes. Si su flujo de trabajo requiere delegación anidada, use [Skills](/es/skills) o [encadene subagentes](#chain-subagents) desde la conversación principal.
</Note>

### Administrar contexto de subagentes

#### Reanudar subagentes

Cada invocación de subagente crea una nueva instancia con contexto fresco. Para continuar el trabajo de un subagente existente en lugar de comenzar de nuevo, pida a Claude que lo reanude.

Los subagentes reanudados retienen su historial de conversación completo, incluidas todas las llamadas de herramientas anteriores, resultados y razonamiento. El subagente continúa exactamente donde se detuvo en lugar de comenzar de nuevo.

Cuando un subagente se completa, Claude recibe su ID de agente. Claude usa la herramienta `SendMessage` con el ID del agente como campo `to` para reanudarlo. La herramienta `SendMessage` solo está disponible cuando [equipos de agentes](/es/agent-teams) están habilitados a través de `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

Para reanudar un subagente, pida a Claude que continúe el trabajo anterior:

```text theme={null}
Use the code-reviewer subagent to review the authentication module
[Agent completes]

Continue that code review and now analyze the authorization logic
[Claude resumes the subagent with full context from previous conversation]
```

Si un subagente detenido recibe un `SendMessage`, se reanuda automáticamente en el fondo sin requerir una nueva invocación de `Agent`.

También puede pedir a Claude el ID del agente si desea referenciarlo explícitamente, o encontrar IDs en los archivos de transcripción en `~/.claude/projects/{project}/{sessionId}/subagents/`. Cada transcripción se almacena como `agent-{agentId}.jsonl`.

Las transcripciones de subagentes persisten independientemente de la conversación principal:

* **Compactación de conversación principal**: Cuando la conversación principal se compacta, las transcripciones de subagentes no se ven afectadas. Se almacenan en archivos separados.
* **Persistencia de sesión**: Las transcripciones de subagentes persisten dentro de su sesión. Puede [reanudar un subagente](#resume-subagents) después de reiniciar Claude Code reanudando la misma sesión.
* **Limpieza automática**: Las transcripciones se limpian basadas en la configuración `cleanupPeriodDays` (por defecto: 30 días).

#### Auto-compactación

Los subagentes soportan compactación automática usando la misma lógica que la conversación principal. Por defecto, la auto-compactación se dispara aproximadamente al 95% de capacidad. Para disparar compactación más temprano, establezca `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` en un porcentaje más bajo (por ejemplo, `50`). Consulte [variables de entorno](/es/env-vars) para detalles.

Los eventos de compactación se registran en archivos de transcripción de subagentes:

```json theme={null}
{
  "type": "system",
  "subtype": "compact_boundary",
  "compactMetadata": {
    "trigger": "auto",
    "preTokens": 167189
  }
}
```

El valor `preTokens` muestra cuántos tokens se usaron antes de que ocurriera la compactación.

## Subagentes de ejemplo

Estos ejemplos demuestran patrones efectivos para construir subagentes. Úselos como puntos de partida, o genere una versión personalizada con Claude.

<Tip>
  **Mejores prácticas:**

  * **Diseñe subagentes enfocados:** cada subagente debe sobresalir en una tarea específica
  * **Escriba descripciones detalladas:** Claude usa la descripción para decidir cuándo delegar
  * **Limite el acceso a herramientas:** otorgue solo permisos necesarios para seguridad y enfoque
  * **Verifique en control de versiones:** comparta subagentes de proyecto con su equipo
</Tip>

### Revisor de código

Un subagente de solo lectura que revisa código sin modificarlo. Este ejemplo muestra cómo diseñar un subagente enfocado con acceso limitado a herramientas (sin Edit o Write) y un mensaje detallado que especifica exactamente qué buscar y cómo formatear la salida.

```markdown theme={null}
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

### Depurador

Un subagente que puede analizar y corregir problemas. A diferencia del revisor de código, este incluye Edit porque corregir errores requiere modificar código. El mensaje proporciona un flujo de trabajo claro desde diagnóstico hasta verificación.

```markdown theme={null}
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.
```

### Científico de datos

Un subagente específico de dominio para trabajo de análisis de datos. Este ejemplo muestra cómo crear subagentes para flujos de trabajo especializados fuera de tareas de codificación típicas. Establece explícitamente `model: sonnet` para análisis más capaz.

```markdown theme={null}
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.
```

### Validador de consultas de base de datos

Un subagente que permite acceso a Bash pero valida comandos para permitir solo consultas SQL de solo lectura. Este ejemplo muestra cómo usar hooks `PreToolUse` para validación condicional cuando necesita control más fino que el campo `tools` proporciona.

```markdown theme={null}
---
name: db-reader
description: Execute read-only database queries. Use when analyzing data or generating reports.
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

You are a database analyst with read-only access. Execute SELECT queries to answer questions about the data.

When asked to analyze data:
1. Identify which tables contain the relevant data
2. Write efficient SELECT queries with appropriate filters
3. Present results clearly with context

You cannot modify data. If asked to INSERT, UPDATE, DELETE, or modify schema, explain that you only have read access.
```

Claude Code [pasa la entrada del hook como JSON](/es/hooks#pretooluse-input) a través de stdin a comandos de hook. El script de validación lee este JSON, extrae el comando siendo ejecutado, y lo verifica contra una lista de operaciones de escritura SQL. Si se detecta una operación de escritura, el script [sale con código 2](/es/hooks#exit-code-2-behavior-per-event) para bloquear la ejecución y devuelve un mensaje de error a Claude a través de stderr.

Cree el script de validación en cualquier lugar en su proyecto. La ruta debe coincidir con el campo `command` en su configuración de hook:

```bash theme={null}
#!/bin/bash
# Blocks SQL write operations, allows SELECT queries

# Read JSON input from stdin
INPUT=$(cat)

# Extract the command field from tool_input using jq
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
  exit 0
fi

# Block write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|REPLACE|MERGE)\b' > /dev/null; then
  echo "Blocked: Write operations not allowed. Use SELECT queries only." >&2
  exit 2
fi

exit 0
```

Haga el script ejecutable:

```bash theme={null}
chmod +x ./scripts/validate-readonly-query.sh
```

El hook recibe JSON a través de stdin con el comando Bash en `tool_input.command`. El código de salida 2 bloquea la operación y alimenta el mensaje de error de vuelta a Claude. Consulte [Hooks](/es/hooks#exit-code-output) para detalles sobre códigos de salida y [Hook input](/es/hooks#pretooluse-input) para el esquema de entrada completo.

## Próximos pasos

Ahora que entiende subagentes, explore estas características relacionadas:

* [Distribuir subagentes con plugins](/es/plugins) para compartir subagentes entre equipos o proyectos
* [Ejecutar Claude Code programáticamente](/es/headless) con el Agent SDK para CI/CD y automatización
* [Usar servidores MCP](/es/mcp) para dar a los subagentes acceso a herramientas y datos externos
