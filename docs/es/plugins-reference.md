> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Referencia de plugins

> Referencia técnica completa para el sistema de plugins de Claude Code, incluyendo esquemas, comandos CLI y especificaciones de componentes.

<Tip>
  ¿Buscas instalar plugins? Consulta [Descubrir e instalar plugins](/es/discover-plugins). Para crear plugins, consulta [Plugins](/es/plugins). Para distribuir plugins, consulta [Marketplaces de plugins](/es/plugin-marketplaces).
</Tip>

Esta referencia proporciona especificaciones técnicas completas para el sistema de plugins de Claude Code, incluyendo esquemas de componentes, comandos CLI y herramientas de desarrollo.

Un **plugin** es un directorio independiente de componentes que extiende Claude Code con funcionalidad personalizada. Los componentes del plugin incluyen skills, agents, hooks, MCP servers y LSP servers.

## Referencia de componentes de plugins

### Skills

Los plugins añaden skills a Claude Code, creando atajos `/name` que usted o Claude pueden invocar.

**Ubicación**: Directorio `skills/` o `commands/` en la raíz del plugin

**Formato de archivo**: Los skills son directorios con `SKILL.md`; los comandos son archivos markdown simples

**Estructura de skill**:

```text  theme={null}
skills/
├── pdf-processor/
│   ├── SKILL.md
│   ├── reference.md (opcional)
│   └── scripts/ (opcional)
└── code-reviewer/
    └── SKILL.md
```

**Comportamiento de integración**:

* Los skills y comandos se descubren automáticamente cuando se instala el plugin
* Claude puede invocarlos automáticamente según el contexto de la tarea
* Los skills pueden incluir archivos de apoyo junto a SKILL.md

Para obtener detalles completos, consulta [Skills](/es/skills).

### Agents

Los plugins pueden proporcionar subagents especializados para tareas específicas que Claude puede invocar automáticamente cuando sea apropiado.

**Ubicación**: Directorio `agents/` en la raíz del plugin

**Formato de archivo**: Archivos markdown que describen las capacidades del agent

**Estructura del agent**:

```markdown  theme={null}
---
name: agent-name
description: En qué se especializa este agent y cuándo Claude debe invocarlo
---

Prompt del sistema detallado para el agent describiendo su rol, experiencia y comportamiento.
```

**Puntos de integración**:

* Los agents aparecen en la interfaz `/agents`
* Claude puede invocar agents automáticamente según el contexto de la tarea
* Los agents pueden ser invocados manualmente por los usuarios
* Los agents del plugin funcionan junto con los agents integrados de Claude

Para obtener detalles completos, consulta [Subagents](/es/sub-agents).

### Hooks

Los plugins pueden proporcionar manejadores de eventos que responden automáticamente a eventos de Claude Code.

**Ubicación**: `hooks/hooks.json` en la raíz del plugin, o en línea en plugin.json

**Formato**: Configuración JSON con coincidencias de eventos y acciones

**Configuración de hook**:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

**Eventos disponibles**:

* `PreToolUse`: Antes de que Claude use cualquier herramienta
* `PostToolUse`: Después de que Claude use exitosamente cualquier herramienta
* `PostToolUseFailure`: Después de que falle la ejecución de una herramienta de Claude
* `PermissionRequest`: Cuando se muestra un diálogo de permiso
* `UserPromptSubmit`: Cuando el usuario envía un prompt
* `Notification`: Cuando Claude Code envía notificaciones
* `Stop`: Cuando Claude intenta detenerse
* `SubagentStart`: Cuando se inicia un subagent
* `SubagentStop`: Cuando un subagent intenta detenerse
* `SessionStart`: Al comienzo de las sesiones
* `SessionEnd`: Al final de las sesiones
* `TeammateIdle`: Cuando un compañero del equipo de agents está a punto de quedarse inactivo
* `TaskCompleted`: Cuando una tarea está siendo marcada como completada
* `PreCompact`: Antes de que se compacte el historial de conversación

**Tipos de hook**:

* `command`: Ejecutar comandos de shell o scripts
* `prompt`: Evaluar un prompt con un LLM (usa el marcador de posición `$ARGUMENTS` para el contexto)
* `agent`: Ejecutar un verificador agentic con herramientas para tareas de verificación complejas

### MCP servers

Los plugins pueden agrupar servidores Model Context Protocol (MCP) para conectar Claude Code con herramientas y servicios externos.

**Ubicación**: `.mcp.json` en la raíz del plugin, o en línea en plugin.json

**Formato**: Configuración estándar del servidor MCP

**Configuración del servidor MCP**:

```json  theme={null}
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    },
    "plugin-api-client": {
      "command": "npx",
      "args": ["@company/mcp-server", "--plugin-mode"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

**Comportamiento de integración**:

* Los servidores MCP del plugin se inician automáticamente cuando se habilita el plugin
* Los servidores aparecen como herramientas MCP estándar en el kit de herramientas de Claude
* Las capacidades del servidor se integran sin problemas con las herramientas existentes de Claude
* Los servidores del plugin se pueden configurar independientemente de los servidores MCP del usuario

### LSP servers

<Tip>
  ¿Buscas usar plugins LSP? Instálalos desde el marketplace oficial: busca "lsp" en la pestaña Discover de `/plugin`. Esta sección documenta cómo crear plugins LSP para lenguajes no cubiertos por el marketplace oficial.
</Tip>

Los plugins pueden proporcionar servidores [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) (LSP) para dar a Claude inteligencia de código en tiempo real mientras trabajas en tu base de código.

La integración de LSP proporciona:

* **Diagnósticos instantáneos**: Claude ve errores y advertencias inmediatamente después de cada edición
* **Navegación de código**: ir a definición, encontrar referencias e información al pasar el ratón
* **Conciencia del lenguaje**: información de tipo y documentación para símbolos de código

**Ubicación**: `.lsp.json` en la raíz del plugin, o en línea en `plugin.json`

**Formato**: Configuración JSON que asigna nombres de servidores de lenguaje a sus configuraciones

**Formato del archivo `.lsp.json`**:

```json  theme={null}
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

**En línea en `plugin.json`**:

```json  theme={null}
{
  "name": "my-plugin",
  "lspServers": {
    "go": {
      "command": "gopls",
      "args": ["serve"],
      "extensionToLanguage": {
        ".go": "go"
      }
    }
  }
}
```

**Campos requeridos:**

| Campo                 | Descripción                                                 |
| :-------------------- | :---------------------------------------------------------- |
| `command`             | El binario LSP a ejecutar (debe estar en PATH)              |
| `extensionToLanguage` | Asigna extensiones de archivo a identificadores de lenguaje |

**Campos opcionales:**

| Campo                   | Descripción                                                         |
| :---------------------- | :------------------------------------------------------------------ |
| `args`                  | Argumentos de línea de comandos para el servidor LSP                |
| `transport`             | Transporte de comunicación: `stdio` (predeterminado) o `socket`     |
| `env`                   | Variables de entorno a establecer al iniciar el servidor            |
| `initializationOptions` | Opciones pasadas al servidor durante la inicialización              |
| `settings`              | Configuración pasada a través de `workspace/didChangeConfiguration` |
| `workspaceFolder`       | Ruta de carpeta de espacio de trabajo para el servidor              |
| `startupTimeout`        | Tiempo máximo para esperar el inicio del servidor (milisegundos)    |
| `shutdownTimeout`       | Tiempo máximo para esperar el apagado elegante (milisegundos)       |
| `restartOnCrash`        | Si se debe reiniciar automáticamente el servidor si se bloquea      |
| `maxRestarts`           | Número máximo de intentos de reinicio antes de rendirse             |

<Warning>
  **Debes instalar el binario del servidor de lenguaje por separado.** Los plugins LSP configuran cómo Claude Code se conecta a un servidor de lenguaje, pero no incluyen el servidor en sí. Si ves `Executable not found in $PATH` en la pestaña Errors de `/plugin`, instala el binario requerido para tu lenguaje.
</Warning>

**Plugins LSP disponibles:**

| Plugin           | Servidor de lenguaje       | Comando de instalación                                                                       |
| :--------------- | :------------------------- | :------------------------------------------------------------------------------------------- |
| `pyright-lsp`    | Pyright (Python)           | `pip install pyright` o `npm install -g pyright`                                             |
| `typescript-lsp` | TypeScript Language Server | `npm install -g typescript-language-server typescript`                                       |
| `rust-lsp`       | rust-analyzer              | [Ver instalación de rust-analyzer](https://rust-analyzer.github.io/manual.html#installation) |

Instala el servidor de lenguaje primero, luego instala el plugin desde el marketplace.

***

## Alcances de instalación de plugins

Cuando instalas un plugin, eliges un **alcance** que determina dónde está disponible el plugin y quién más puede usarlo:

| Alcance   | Archivo de configuración                                  | Caso de uso                                                            |
| :-------- | :-------------------------------------------------------- | :--------------------------------------------------------------------- |
| `user`    | `~/.claude/settings.json`                                 | Plugins personales disponibles en todos los proyectos (predeterminado) |
| `project` | `.claude/settings.json`                                   | Plugins de equipo compartidos a través del control de versiones        |
| `local`   | `.claude/settings.local.json`                             | Plugins específicos del proyecto, ignorados por git                    |
| `managed` | [Configuración administrada](/es/settings#settings-files) | Plugins administrados (solo lectura, solo actualizar)                  |

Los plugins utilizan el mismo sistema de alcance que otras configuraciones de Claude Code. Para instrucciones de instalación y banderas de alcance, consulta [Instalar plugins](/es/discover-plugins#install-plugins). Para una explicación completa de los alcances, consulta [Alcances de configuración](/es/settings#configuration-scopes).

***

## Esquema del manifiesto del plugin

El archivo `.claude-plugin/plugin.json` define los metadatos y la configuración de tu plugin. Esta sección documenta todos los campos y opciones soportados.

El manifiesto es opcional. Si se omite, Claude Code descubre automáticamente componentes en [ubicaciones predeterminadas](#file-locations-reference) y deriva el nombre del plugin del nombre del directorio. Usa un manifiesto cuando necesites proporcionar metadatos o rutas de componentes personalizadas.

### Esquema completo

```json  theme={null}
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json"
}
```

### Campos requeridos

Si incluyes un manifiesto, `name` es el único campo requerido.

| Campo  | Tipo   | Descripción                                    | Ejemplo              |
| :----- | :----- | :--------------------------------------------- | :------------------- |
| `name` | string | Identificador único (kebab-case, sin espacios) | `"deployment-tools"` |

Este nombre se utiliza para espacios de nombres de componentes. Por ejemplo, en la interfaz de usuario, el agent `agent-creator` para el plugin con nombre `plugin-dev` aparecerá como `plugin-dev:agent-creator`.

### Campos de metadatos

| Campo         | Tipo   | Descripción                                                                                                                                       | Ejemplo                                            |
| :------------ | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------- |
| `version`     | string | Versión semántica. Si también se establece en la entrada del marketplace, `plugin.json` tiene prioridad. Solo necesitas establecerlo en un lugar. | `"2.1.0"`                                          |
| `description` | string | Explicación breve del propósito del plugin                                                                                                        | `"Deployment automation tools"`                    |
| `author`      | object | Información del autor                                                                                                                             | `{"name": "Dev Team", "email": "dev@company.com"}` |
| `homepage`    | string | URL de documentación                                                                                                                              | `"https://docs.example.com"`                       |
| `repository`  | string | URL del código fuente                                                                                                                             | `"https://github.com/user/plugin"`                 |
| `license`     | string | Identificador de licencia                                                                                                                         | `"MIT"`, `"Apache-2.0"`                            |
| `keywords`    | array  | Etiquetas de descubrimiento                                                                                                                       | `["deployment", "ci-cd"]`                          |

### Campos de ruta de componentes

| Campo          | Tipo                  | Descripción                                                                                                                                                                     | Ejemplo                               |
| :------------- | :-------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------ |
| `commands`     | string\|array         | Archivos/directorios de comandos adicionales                                                                                                                                    | `"./custom/cmd.md"` o `["./cmd1.md"]` |
| `agents`       | string\|array         | Archivos de agents adicionales                                                                                                                                                  | `"./custom/agents/reviewer.md"`       |
| `skills`       | string\|array         | Directorios de skills adicionales                                                                                                                                               | `"./custom/skills/"`                  |
| `hooks`        | string\|array\|object | Rutas de configuración de hooks o configuración en línea                                                                                                                        | `"./my-extra-hooks.json"`             |
| `mcpServers`   | string\|array\|object | Rutas de configuración de MCP o configuración en línea                                                                                                                          | `"./my-extra-mcp-config.json"`        |
| `outputStyles` | string\|array         | Archivos/directorios de estilos de salida adicionales                                                                                                                           | `"./styles/"`                         |
| `lspServers`   | string\|array\|object | Configuraciones de [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) para inteligencia de código (ir a definición, encontrar referencias, etc.) | `"./.lsp.json"`                       |

### Reglas de comportamiento de rutas

**Importante**: Las rutas personalizadas complementan los directorios predeterminados - no los reemplazan.

* Si `commands/` existe, se carga además de las rutas de comandos personalizadas
* Todas las rutas deben ser relativas a la raíz del plugin y comenzar con `./`
* Los comandos de rutas personalizadas utilizan las mismas reglas de nomenclatura y espacios de nombres
* Se pueden especificar múltiples rutas como arrays para flexibilidad

**Ejemplos de rutas**:

```json  theme={null}
{
  "commands": [
    "./specialized/deploy.md",
    "./utilities/batch-process.md"
  ],
  "agents": [
    "./custom-agents/reviewer.md",
    "./custom-agents/tester.md"
  ]
}
```

### Variables de entorno

**`${CLAUDE_PLUGIN_ROOT}`**: Contiene la ruta absoluta a tu directorio de plugin. Úsala en hooks, servidores MCP y scripts para asegurar rutas correctas independientemente de la ubicación de instalación.

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

***

## Almacenamiento en caché de plugins y resolución de archivos

Los plugins se especifican de una de dos formas:

* A través de `claude --plugin-dir`, durante la duración de una sesión.
* A través de un marketplace, instalado para sesiones futuras.

Por razones de seguridad y verificación, Claude Code copia plugins del *marketplace* a la **caché de plugins** local del usuario (`~/.claude/plugins/cache`) en lugar de usarlos en su lugar. Entender este comportamiento es importante al desarrollar plugins que hacen referencia a archivos externos.

### Limitaciones de traversal de rutas

Los plugins instalados no pueden hacer referencia a archivos fuera de su directorio. Las rutas que traversan fuera de la raíz del plugin (como `../shared-utils`) no funcionarán después de la instalación porque esos archivos externos no se copian a la caché.

### Trabajar con dependencias externas

Si tu plugin necesita acceder a archivos fuera de su directorio, puedes crear enlaces simbólicos a archivos externos dentro de tu directorio de plugin. Los enlaces simbólicos se respetan durante el proceso de copia:

```bash  theme={null}
# Dentro de tu directorio de plugin
ln -s /path/to/shared-utils ./shared-utils
```

El contenido vinculado simbólicamente se copiará en la caché del plugin. Esto proporciona flexibilidad mientras se mantienen los beneficios de seguridad del sistema de almacenamiento en caché.

***

## Estructura del directorio del plugin

### Diseño estándar del plugin

Un plugin completo sigue esta estructura:

```text  theme={null}
enterprise-plugin/
├── .claude-plugin/           # Directorio de metadatos (opcional)
│   └── plugin.json             # manifiesto del plugin
├── commands/                 # Ubicación de comando predeterminada
│   ├── status.md
│   └── logs.md
├── agents/                   # Ubicación de agent predeterminada
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── skills/                   # Skills del Agent
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── hooks/                    # Configuraciones de hooks
│   ├── hooks.json           # Configuración principal de hooks
│   └── security-hooks.json  # Hooks adicionales
├── settings.json            # Configuración predeterminada para el plugin
├── .mcp.json                # Definiciones del servidor MCP
├── .lsp.json                # Configuraciones del servidor LSP
├── scripts/                 # Scripts de hooks y utilidades
│   ├── security-scan.sh
│   ├── format-code.py
│   └── deploy.js
├── LICENSE                  # Archivo de licencia
└── CHANGELOG.md             # Historial de versiones
```

<Warning>
  El directorio `.claude-plugin/` contiene el archivo `plugin.json`. Todos los otros directorios (commands/, agents/, skills/, hooks/) deben estar en la raíz del plugin, no dentro de `.claude-plugin/`.
</Warning>

### Referencia de ubicaciones de archivos

| Componente         | Ubicación predeterminada     | Propósito                                                                                                                                     |
| :----------------- | :--------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| **Manifiesto**     | `.claude-plugin/plugin.json` | Metadatos y configuración del plugin (opcional)                                                                                               |
| **Comandos**       | `commands/`                  | Archivos Markdown de Skill (heredado; usa `skills/` para nuevos skills)                                                                       |
| **Agents**         | `agents/`                    | Archivos Markdown de Subagent                                                                                                                 |
| **Skills**         | `skills/`                    | Skills con estructura `<name>/SKILL.md`                                                                                                       |
| **Hooks**          | `hooks/hooks.json`           | Configuración de hooks                                                                                                                        |
| **Servidores MCP** | `.mcp.json`                  | Definiciones del servidor MCP                                                                                                                 |
| **Servidores LSP** | `.lsp.json`                  | Configuraciones del servidor de lenguaje                                                                                                      |
| **Configuración**  | `settings.json`              | Configuración predeterminada aplicada cuando se habilita el plugin. Actualmente solo se soportan configuraciones de [`agent`](/es/sub-agents) |

***

## Referencia de comandos CLI

Claude Code proporciona comandos CLI para la gestión de plugins no interactiva, útil para scripting y automatización.

### plugin install

Instala un plugin desde los marketplaces disponibles.

```bash  theme={null}
claude plugin install <plugin> [options]
```

**Argumentos:**

* `<plugin>`: Nombre del plugin o `plugin-name@marketplace-name` para un marketplace específico

**Opciones:**

| Opción                | Descripción                                          | Predeterminado |
| :-------------------- | :--------------------------------------------------- | :------------- |
| `-s, --scope <scope>` | Alcance de instalación: `user`, `project`, o `local` | `user`         |
| `-h, --help`          | Mostrar ayuda para el comando                        |                |

El alcance determina qué archivo de configuración se añade el plugin instalado. Por ejemplo, --scope project escribe en `enabledPlugins` en .claude/settings.json, haciendo que el plugin esté disponible para todos los que clonan el repositorio del proyecto.

**Ejemplos:**

```bash  theme={null}
# Instalar en alcance de usuario (predeterminado)
claude plugin install formatter@my-marketplace

# Instalar en alcance de proyecto (compartido con el equipo)
claude plugin install formatter@my-marketplace --scope project

# Instalar en alcance local (ignorado por git)
claude plugin install formatter@my-marketplace --scope local
```

### plugin uninstall

Elimina un plugin instalado.

```bash  theme={null}
claude plugin uninstall <plugin> [options]
```

**Argumentos:**

* `<plugin>`: Nombre del plugin o `plugin-name@marketplace-name`

**Opciones:**

| Opción                | Descripción                                           | Predeterminado |
| :-------------------- | :---------------------------------------------------- | :------------- |
| `-s, --scope <scope>` | Desinstalar del alcance: `user`, `project`, o `local` | `user`         |
| `-h, --help`          | Mostrar ayuda para el comando                         |                |

**Alias:** `remove`, `rm`

### plugin enable

Habilita un plugin deshabilitado.

```bash  theme={null}
claude plugin enable <plugin> [options]
```

**Argumentos:**

* `<plugin>`: Nombre del plugin o `plugin-name@marketplace-name`

**Opciones:**

| Opción                | Descripción                                       | Predeterminado |
| :-------------------- | :------------------------------------------------ | :------------- |
| `-s, --scope <scope>` | Alcance a habilitar: `user`, `project`, o `local` | `user`         |
| `-h, --help`          | Mostrar ayuda para el comando                     |                |

### plugin disable

Deshabilita un plugin sin desinstalarlo.

```bash  theme={null}
claude plugin disable <plugin> [options]
```

**Argumentos:**

* `<plugin>`: Nombre del plugin o `plugin-name@marketplace-name`

**Opciones:**

| Opción                | Descripción                                          | Predeterminado |
| :-------------------- | :--------------------------------------------------- | :------------- |
| `-s, --scope <scope>` | Alcance a deshabilitar: `user`, `project`, o `local` | `user`         |
| `-h, --help`          | Mostrar ayuda para el comando                        |                |

### plugin update

Actualiza un plugin a la versión más reciente.

```bash  theme={null}
claude plugin update <plugin> [options]
```

**Argumentos:**

* `<plugin>`: Nombre del plugin o `plugin-name@marketplace-name`

**Opciones:**

| Opción                | Descripción                                                   | Predeterminado |
| :-------------------- | :------------------------------------------------------------ | :------------- |
| `-s, --scope <scope>` | Alcance a actualizar: `user`, `project`, `local`, o `managed` | `user`         |
| `-h, --help`          | Mostrar ayuda para el comando                                 |                |

***

## Herramientas de depuración y desarrollo

### Comandos de depuración

Usa `claude --debug` (o `/debug` dentro de la TUI) para ver detalles de carga de plugins:

Esto muestra:

* Qué plugins se están cargando
* Cualquier error en los manifiestos del plugin
* Registro de comandos, agents y hooks
* Inicialización del servidor MCP

### Problemas comunes

| Problema                            | Causa                               | Solución                                                                            |
| :---------------------------------- | :---------------------------------- | :---------------------------------------------------------------------------------- |
| Plugin no se carga                  | `plugin.json` inválido              | Valida la sintaxis JSON con `claude plugin validate` o `/plugin validate`           |
| Los comandos no aparecen            | Estructura de directorio incorrecta | Asegúrate de que `commands/` esté en la raíz, no en `.claude-plugin/`               |
| Los hooks no se disparan            | Script no ejecutable                | Ejecuta `chmod +x script.sh`                                                        |
| El servidor MCP falla               | Falta `${CLAUDE_PLUGIN_ROOT}`       | Usa la variable para todas las rutas del plugin                                     |
| Errores de ruta                     | Se utilizan rutas absolutas         | Todas las rutas deben ser relativas y comenzar con `./`                             |
| LSP `Executable not found in $PATH` | Servidor de lenguaje no instalado   | Instala el binario (p. ej., `npm install -g typescript-language-server typescript`) |

### Mensajes de error de ejemplo

**Errores de validación de manifiesto**:

* `Invalid JSON syntax: Unexpected token } in JSON at position 142`: busca comas faltantes, comas extra o cadenas sin comillas
* `Plugin has an invalid manifest file at .claude-plugin/plugin.json. Validation errors: name: Required`: falta un campo requerido
* `Plugin has a corrupt manifest file at .claude-plugin/plugin.json. JSON parse error: ...`: error de sintaxis JSON

**Errores de carga de plugin**:

* `Warning: No commands found in plugin my-plugin custom directory: ./cmds. Expected .md files or SKILL.md in subdirectories.`: la ruta del comando existe pero no contiene archivos de comando válidos
* `Plugin directory not found at path: ./plugins/my-plugin. Check that the marketplace entry has the correct path.`: la ruta `source` en marketplace.json apunta a un directorio inexistente
* `Plugin my-plugin has conflicting manifests: both plugin.json and marketplace entry specify components.`: elimina definiciones de componentes duplicadas o elimina `strict: false` en la entrada del marketplace

### Solución de problemas de hooks

**El script del hook no se ejecuta**:

1. Verifica que el script sea ejecutable: `chmod +x ./scripts/your-script.sh`
2. Verifica la línea shebang: La primera línea debe ser `#!/bin/bash` o `#!/usr/bin/env bash`
3. Verifica que la ruta use `${CLAUDE_PLUGIN_ROOT}`: `"command": "${CLAUDE_PLUGIN_ROOT}/scripts/your-script.sh"`
4. Prueba el script manualmente: `./scripts/your-script.sh`

**El hook no se dispara en los eventos esperados**:

1. Verifica que el nombre del evento sea correcto (sensible a mayúsculas): `PostToolUse`, no `postToolUse`
2. Verifica que el patrón del matcher coincida con tus herramientas: `"matcher": "Write|Edit"` para operaciones de archivo
3. Confirma que el tipo de hook sea válido: `command`, `prompt`, o `agent`

### Solución de problemas del servidor MCP

**El servidor no se inicia**:

1. Verifica que el comando exista y sea ejecutable
2. Verifica que todas las rutas usen la variable `${CLAUDE_PLUGIN_ROOT}`
3. Verifica los registros del servidor MCP: `claude --debug` muestra errores de inicialización
4. Prueba el servidor manualmente fuera de Claude Code

**Las herramientas del servidor no aparecen**:

1. Asegúrate de que el servidor esté correctamente configurado en `.mcp.json` o `plugin.json`
2. Verifica que el servidor implemente correctamente el protocolo MCP
3. Busca tiempos de espera de conexión en la salida de depuración

### Errores de estructura de directorio

**Síntomas**: El plugin se carga pero faltan componentes (comandos, agents, hooks).

**Estructura correcta**: Los componentes deben estar en la raíz del plugin, no dentro de `.claude-plugin/`. Solo `plugin.json` pertenece a `.claude-plugin/`.

```text  theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json      ← Solo el manifiesto aquí
├── commands/            ← A nivel de raíz
├── agents/              ← A nivel de raíz
└── hooks/               ← A nivel de raíz
```

Si tus componentes están dentro de `.claude-plugin/`, muévelos a la raíz del plugin.

**Lista de verificación de depuración**:

1. Ejecuta `claude --debug` y busca mensajes "loading plugin"
2. Verifica que cada directorio de componentes esté listado en la salida de depuración
3. Verifica que los permisos de archivo permitan leer los archivos del plugin

***

## Referencia de distribución y versionado

### Gestión de versiones

Sigue el versionado semántico para las versiones del plugin:

```json  theme={null}
{
  "name": "my-plugin",
  "version": "2.1.0"
}
```

**Formato de versión**: `MAJOR.MINOR.PATCH`

* **MAJOR**: Cambios de ruptura (cambios de API incompatibles)
* **MINOR**: Nuevas características (adiciones compatibles hacia atrás)
* **PATCH**: Correcciones de errores (correcciones compatibles hacia atrás)

**Mejores prácticas**:

* Comienza en `1.0.0` para tu primer lanzamiento estable
* Actualiza la versión en `plugin.json` antes de distribuir cambios
* Documenta los cambios en un archivo `CHANGELOG.md`
* Usa versiones previas al lanzamiento como `2.0.0-beta.1` para pruebas

<Warning>
  Claude Code utiliza la versión para determinar si debe actualizar tu plugin. Si cambias el código de tu plugin pero no aumentas la versión en `plugin.json`, los usuarios existentes de tu plugin no verán tus cambios debido al almacenamiento en caché.

  Si tu plugin está dentro de un directorio de [marketplace](/es/plugin-marketplaces), puedes gestionar la versión a través de `marketplace.json` en su lugar y omitir el campo `version` de `plugin.json`.
</Warning>

***

## Ver también

* [Plugins](/es/plugins) - Tutoriales y uso práctico
* [Marketplaces de plugins](/es/plugin-marketplaces) - Crear y gestionar marketplaces
* [Skills](/es/skills) - Detalles de desarrollo de skills
* [Subagents](/es/sub-agents) - Configuración y capacidades del agent
* [Hooks](/es/hooks) - Manejo de eventos y automatización
* [MCP](/es/mcp) - Integración de herramientas externas
* [Configuración](/es/settings) - Opciones de configuración para plugins
