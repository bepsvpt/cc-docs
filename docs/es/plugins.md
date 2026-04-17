> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Crear plugins

> Crea plugins personalizados para extender Claude Code con skills, agentes, hooks y servidores MCP.

Los plugins le permiten extender Claude Code con funcionalidad personalizada que se puede compartir entre proyectos y equipos. Esta guía cubre la creación de sus propios plugins con skills, agentes, hooks y servidores MCP.

¿Buscando instalar plugins existentes? Consulte [Descubrir e instalar plugins](/es/discover-plugins). Para especificaciones técnicas completas, consulte [Referencia de plugins](/es/plugins-reference).

## Cuándo usar plugins versus configuración independiente

Claude Code admite dos formas de agregar skills, agentes y hooks personalizados:

| Enfoque                                                    | Nombres de skills    | Mejor para                                                                                                                   |
| :--------------------------------------------------------- | :------------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| **Independiente** (directorio `.claude/`)                  | `/hello`             | Flujos de trabajo personales, personalizaciones específicas del proyecto, experimentos rápidos                               |
| **Plugins** (directorios con `.claude-plugin/plugin.json`) | `/plugin-name:hello` | Compartir con compañeros de equipo, distribuir a la comunidad, lanzamientos versionados, reutilizable en múltiples proyectos |

**Use configuración independiente cuando**:

* Esté personalizando Claude Code para un único proyecto
* La configuración es personal y no necesita ser compartida
* Esté experimentando con skills o hooks antes de empaquetarlos
* Quiera nombres de skills cortos como `/hello` o `/deploy`

**Use plugins cuando**:

* Quiera compartir funcionalidad con su equipo o comunidad
* Necesite los mismos skills/agentes en múltiples proyectos
* Quiera control de versiones y actualizaciones fáciles para sus extensiones
* Esté distribuyendo a través de un marketplace
* Esté de acuerdo con skills con espacios de nombres como `/my-plugin:hello` (los espacios de nombres previenen conflictos entre plugins)

<Tip>
  Comience con configuración independiente en `.claude/` para iteración rápida, luego [convierta a un plugin](#convert-existing-configurations-to-plugins) cuando esté listo para compartir.
</Tip>

## Inicio rápido

Este inicio rápido le guía a través de la creación de un plugin con un skill personalizado. Creará un manifiesto (el archivo de configuración que define su plugin), agregará un skill y lo probará localmente usando la bandera `--plugin-dir`.

### Requisitos previos

* Claude Code [instalado y autenticado](/es/quickstart#step-1-install-claude-code)

<Note>
  Si no ve el comando `/plugin`, actualice Claude Code a la última versión. Consulte [Troubleshooting](/es/troubleshooting) para obtener instrucciones de actualización.
</Note>

### Cree su primer plugin

<Steps>
  <Step title="Cree el directorio del plugin">
    Cada plugin vive en su propio directorio que contiene un manifiesto y sus skills, agentes o hooks. Cree uno ahora:

    ```bash theme={null}
    mkdir my-first-plugin
    ```
  </Step>

  <Step title="Cree el manifiesto del plugin">
    El archivo de manifiesto en `.claude-plugin/plugin.json` define la identidad de su plugin: su nombre, descripción y versión. Claude Code usa estos metadatos para mostrar su plugin en el administrador de plugins.

    Cree el directorio `.claude-plugin` dentro de su carpeta de plugin:

    ```bash theme={null}
    mkdir my-first-plugin/.claude-plugin
    ```

    Luego cree `my-first-plugin/.claude-plugin/plugin.json` con este contenido:

    ```json my-first-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "my-first-plugin",
      "description": "A greeting plugin to learn the basics",
      "version": "1.0.0",
      "author": {
        "name": "Your Name"
      }
    }
    ```

    | Campo         | Propósito                                                                                                                  |
    | :------------ | :------------------------------------------------------------------------------------------------------------------------- |
    | `name`        | Identificador único y espacio de nombres de skill. Los skills tienen este prefijo (por ejemplo, `/my-first-plugin:hello`). |
    | `description` | Se muestra en el administrador de plugins al examinar o instalar plugins.                                                  |
    | `version`     | Rastrear lanzamientos usando [versionado semántico](/es/plugins-reference#version-management).                             |
    | `author`      | Opcional. Útil para atribución.                                                                                            |

    Para campos adicionales como `homepage`, `repository` y `license`, consulte el [esquema de manifiesto completo](/es/plugins-reference#plugin-manifest-schema).
  </Step>

  <Step title="Agregue un skill">
    Los skills viven en el directorio `skills/`. Cada skill es una carpeta que contiene un archivo `SKILL.md`. El nombre de la carpeta se convierte en el nombre del skill, con el prefijo del espacio de nombres del plugin (`hello/` en un plugin llamado `my-first-plugin` crea `/my-first-plugin:hello`).

    Cree un directorio de skill en su carpeta de plugin:

    ```bash theme={null}
    mkdir -p my-first-plugin/skills/hello
    ```

    Luego cree `my-first-plugin/skills/hello/SKILL.md` con este contenido:

    ```markdown my-first-plugin/skills/hello/SKILL.md theme={null}
    ---
    description: Greet the user with a friendly message
    disable-model-invocation: true
    ---

    Greet the user warmly and ask how you can help them today.
    ```
  </Step>

  <Step title="Pruebe su plugin">
    Ejecute Claude Code con la bandera `--plugin-dir` para cargar su plugin:

    ```bash theme={null}
    claude --plugin-dir ./my-first-plugin
    ```

    Una vez que Claude Code se inicie, pruebe su nuevo skill:

    ```shell theme={null}
    /my-first-plugin:hello
    ```

    Verá que Claude responde con un saludo. Ejecute `/help` para ver su skill listado bajo el espacio de nombres del plugin.

    <Note>
      **¿Por qué espacios de nombres?** Los skills de plugin siempre tienen espacios de nombres (como `/my-first-plugin:hello`) para prevenir conflictos cuando múltiples plugins tienen skills con el mismo nombre.

      Para cambiar el prefijo del espacio de nombres, actualice el campo `name` en `plugin.json`.
    </Note>
  </Step>

  <Step title="Agregue argumentos de skill">
    Haga su skill dinámico aceptando entrada del usuario. El marcador de posición `$ARGUMENTS` captura cualquier texto que el usuario proporcione después del nombre del skill.

    Actualice su archivo `SKILL.md`:

    ```markdown my-first-plugin/skills/hello/SKILL.md theme={null}
    ---
    description: Greet the user with a personalized message
    ---

    # Hello Skill

    Greet the user named "$ARGUMENTS" warmly and ask how you can help them today. Make the greeting personal and encouraging.
    ```

    Ejecute `/reload-plugins` para recoger los cambios, luego pruebe el skill con su nombre:

    ```shell theme={null}
    /my-first-plugin:hello Alex
    ```

    Claude le saludará por su nombre. Para más información sobre pasar argumentos a skills, consulte [Skills](/es/skills#pass-arguments-to-skills).
  </Step>
</Steps>

Ha creado y probado exitosamente un plugin con estos componentes clave:

* **Manifiesto del plugin** (`.claude-plugin/plugin.json`): describe los metadatos de su plugin
* **Directorio de skills** (`skills/`): contiene sus skills personalizados
* **Argumentos de skill** (`$ARGUMENTS`): captura entrada del usuario para comportamiento dinámico

<Tip>
  La bandera `--plugin-dir` es útil para desarrollo y pruebas. Cuando esté listo para compartir su plugin con otros, consulte [Crear y distribuir un marketplace de plugins](/es/plugin-marketplaces).
</Tip>

## Descripción general de la estructura del plugin

Ha creado un plugin con un skill, pero los plugins pueden incluir mucho más: agentes personalizados, hooks, servidores MCP y servidores LSP.

<Warning>
  **Error común**: No ponga `commands/`, `agents/`, `skills/` o `hooks/` dentro del directorio `.claude-plugin/`. Solo `plugin.json` va dentro de `.claude-plugin/`. Todos los otros directorios deben estar en el nivel raíz del plugin.
</Warning>

| Directorio        | Ubicación       | Propósito                                                                                           |
| :---------------- | :-------------- | :-------------------------------------------------------------------------------------------------- |
| `.claude-plugin/` | Raíz del plugin | Contiene el manifiesto `plugin.json` (opcional si los componentes usan ubicaciones predeterminadas) |
| `skills/`         | Raíz del plugin | Skills como directorios `<name>/SKILL.md`                                                           |
| `commands/`       | Raíz del plugin | Skills como archivos Markdown planos. Use `skills/` para plugins nuevos                             |
| `agents/`         | Raíz del plugin | Definiciones de agentes personalizados                                                              |
| `hooks/`          | Raíz del plugin | Manejadores de eventos en `hooks.json`                                                              |
| `.mcp.json`       | Raíz del plugin | Configuraciones de servidor MCP                                                                     |
| `.lsp.json`       | Raíz del plugin | Configuraciones de servidor LSP para inteligencia de código                                         |
| `monitors/`       | Raíz del plugin | Configuraciones de monitor de fondo en `monitors.json`                                              |
| `bin/`            | Raíz del plugin | Ejecutables agregados a la `PATH` de la herramienta Bash mientras el plugin está habilitado         |
| `settings.json`   | Raíz del plugin | [Configuraciones](/es/settings) predeterminadas aplicadas cuando el plugin está habilitado          |

<Note>
  **Próximos pasos**: ¿Listo para agregar más características? Salte a [Desarrollar plugins más complejos](#develop-more-complex-plugins) para agregar agentes, hooks, servidores MCP y servidores LSP. Para especificaciones técnicas completas de todos los componentes del plugin, consulte [Referencia de plugins](/es/plugins-reference).
</Note>

## Desarrollar plugins más complejos

Una vez que se sienta cómodo con plugins básicos, puede crear extensiones más sofisticadas.

### Agregue Skills a su plugin

Los plugins pueden incluir [Agent Skills](/es/skills) para extender las capacidades de Claude. Los skills son invocados por el modelo: Claude los usa automáticamente basándose en el contexto de la tarea.

Agregue un directorio `skills/` en la raíz de su plugin con carpetas de Skill que contengan archivos `SKILL.md`:

```text theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── code-review/
        └── SKILL.md
```

Cada `SKILL.md` contiene frontmatter YAML e instrucciones. Incluya una `description` para que Claude sepa cuándo usar el skill:

```yaml theme={null}
---
description: Reviews code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
---

When reviewing code, check for:
1. Code organization and structure
2. Error handling
3. Security concerns
4. Test coverage
```

Después de instalar el plugin, ejecute `/reload-plugins` para cargar los Skills. Para orientación completa sobre la autoría de Skills incluyendo divulgación progresiva y restricciones de herramientas, consulte [Agent Skills](/es/skills).

### Agregue servidores LSP a su plugin

<Tip>
  Para lenguajes comunes como TypeScript, Python y Rust, instale los plugins LSP precompilados desde el marketplace oficial. Cree plugins LSP personalizados solo cuando necesite soporte para lenguajes que aún no están cubiertos.
</Tip>

Los plugins LSP (Language Server Protocol) dan a Claude inteligencia de código en tiempo real. Si necesita soportar un lenguaje que no tiene un plugin LSP oficial, puede crear uno propio agregando un archivo `.lsp.json` a su plugin:

```json .lsp.json theme={null}
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

Los usuarios que instalen su plugin deben tener el binario del servidor de lenguaje instalado en su máquina.

Para opciones de configuración LSP completas, consulte [Servidores LSP](/es/plugins-reference#lsp-servers).

### Agregue monitores de fondo a su plugin

Los monitores de fondo permiten que su plugin observe registros, archivos o estado externo en el fondo y notifique a Claude cuando lleguen eventos. Claude Code inicia cada monitor automáticamente cuando el plugin está activo, por lo que no necesita instruir a Claude para que inicie la observación.

Agregue un archivo `monitors/monitors.json` en la raíz del plugin con una matriz de entradas de monitor:

```json monitors/monitors.json theme={null}
[
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Application error log"
  }
]
```

Cada línea de stdout del `command` se entrega a Claude como una notificación durante la sesión. Para el esquema completo, incluyendo el disparador `when` y la sustitución de variables, consulte [Monitors](/es/plugins-reference#monitors).

### Envíe configuraciones predeterminadas con su plugin

Los plugins pueden incluir un archivo `settings.json` en la raíz del plugin para aplicar configuración predeterminada cuando el plugin está habilitado. Actualmente, solo se admiten las claves `agent` y `subagentStatusLine`.

Establecer `agent` activa uno de los [agentes personalizados](/es/sub-agents) del plugin como el hilo principal, aplicando su indicación del sistema, restricciones de herramientas y modelo. Esto permite que un plugin cambie cómo se comporta Claude Code por defecto cuando está habilitado.

```json settings.json theme={null}
{
  "agent": "security-reviewer"
}
```

Este ejemplo activa el agente `security-reviewer` definido en el directorio `agents/` del plugin. Las configuraciones de `settings.json` tienen prioridad sobre `settings` declarados en `plugin.json`. Las claves desconocidas se ignoran silenciosamente.

### Organice plugins complejos

Para plugins con muchos componentes, organice su estructura de directorios por funcionalidad. Para diseños de directorios completos y patrones de organización, consulte [Estructura de directorios del plugin](/es/plugins-reference#plugin-directory-structure).

### Pruebe sus plugins localmente

Use la bandera `--plugin-dir` para probar plugins durante el desarrollo. Esto carga su plugin directamente sin requerir instalación.

```bash theme={null}
claude --plugin-dir ./my-plugin
```

Cuando un plugin `--plugin-dir` tiene el mismo nombre que un plugin de marketplace instalado, la copia local tiene prioridad para esa sesión. Esto le permite probar cambios en un plugin que ya tiene instalado sin desinstalarlo primero. Los plugins de marketplace forzados a estar habilitados por configuraciones administradas son la única excepción y no pueden ser anulados.

A medida que haga cambios en su plugin, ejecute `/reload-plugins` para recoger las actualizaciones sin reiniciar. Esto recarga plugins, skills, agentes, hooks, servidores MCP de plugin y servidores LSP de plugin. Pruebe los componentes de su plugin:

* Pruebe sus skills con `/plugin-name:skill-name`
* Verifique que los agentes aparezcan en `/agents`
* Verifique que los hooks funcionen como se espera

<Tip>
  Puede cargar múltiples plugins a la vez especificando la bandera varias veces:

  ```bash theme={null}
  claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two
  ```
</Tip>

### Depure problemas del plugin

Si su plugin no funciona como se espera:

1. **Verifique la estructura**: Asegúrese de que sus directorios estén en la raíz del plugin, no dentro de `.claude-plugin/`
2. **Pruebe componentes individualmente**: Verifique cada skill, agente y hook por separado
3. **Use herramientas de validación y depuración**: Consulte [Herramientas de depuración y desarrollo](/es/plugins-reference#debugging-and-development-tools) para comandos CLI y técnicas de solución de problemas

### Comparta sus plugins

Cuando su plugin esté listo para compartir:

1. **Agregue documentación**: Incluya un `README.md` con instrucciones de instalación y uso
2. **Versione su plugin**: Use [versionado semántico](/es/plugins-reference#version-management) en su `plugin.json`
3. **Cree o use un marketplace**: Distribuya a través de [marketplaces de plugins](/es/plugin-marketplaces) para instalación
4. **Pruebe con otros**: Haga que los miembros del equipo prueben el plugin antes de una distribución más amplia

Una vez que su plugin esté en un marketplace, otros pueden instalarlo usando las instrucciones en [Descubrir e instalar plugins](/es/discover-plugins).

### Envíe su plugin al marketplace oficial

Para enviar un plugin al marketplace oficial de Anthropic, use uno de los formularios de envío en la aplicación:

* **Claude.ai**: [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
* **Console**: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

Una vez que su plugin esté listado, puede tener su propio CLI que solicite a los usuarios de Claude Code que lo instalen. Consulte [Recomienda su plugin desde su CLI](/es/plugin-hints).

<Note>
  Para especificaciones técnicas completas, técnicas de depuración y estrategias de distribución, consulte [Referencia de plugins](/es/plugins-reference).
</Note>

## Convierta configuraciones existentes en plugins

Si ya tiene skills o hooks en su directorio `.claude/`, puede convertirlos en un plugin para compartir y distribución más fácil.

### Pasos de migración

<Steps>
  <Step title="Cree la estructura del plugin">
    Cree un nuevo directorio de plugin:

    ```bash theme={null}
    mkdir -p my-plugin/.claude-plugin
    ```

    Cree el archivo de manifiesto en `my-plugin/.claude-plugin/plugin.json`:

    ```json my-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "my-plugin",
      "description": "Migrated from standalone configuration",
      "version": "1.0.0"
    }
    ```
  </Step>

  <Step title="Copie sus archivos existentes">
    Copie sus configuraciones existentes al directorio del plugin:

    ```bash theme={null}
    # Copy commands
    cp -r .claude/commands my-plugin/

    # Copy agents (if any)
    cp -r .claude/agents my-plugin/

    # Copy skills (if any)
    cp -r .claude/skills my-plugin/
    ```
  </Step>

  <Step title="Migre hooks">
    Si tiene hooks en su configuración, cree un directorio de hooks:

    ```bash theme={null}
    mkdir my-plugin/hooks
    ```

    Cree `my-plugin/hooks/hooks.json` con su configuración de hooks. Copie el objeto `hooks` de su `.claude/settings.json` o `settings.local.json`, ya que el formato es el mismo. El comando recibe entrada de hook como JSON en stdin, así que use `jq` para extraer la ruta del archivo:

    ```json my-plugin/hooks/hooks.json theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [{ "type": "command", "command": "jq -r '.tool_input.file_path' | xargs npm run lint:fix" }]
          }
        ]
      }
    }
    ```
  </Step>

  <Step title="Pruebe su plugin migrado">
    Cargue su plugin para verificar que todo funciona:

    ```bash theme={null}
    claude --plugin-dir ./my-plugin
    ```

    Pruebe cada componente: ejecute sus skills, verifique que los agentes aparezcan en `/agents` y verifique que los hooks se activen correctamente.
  </Step>
</Steps>

### Qué cambia al migrar

| Independiente (`.claude/`)             | Plugin                                      |
| :------------------------------------- | :------------------------------------------ |
| Solo disponible en un proyecto         | Se puede compartir a través de marketplaces |
| Archivos en `.claude/commands/`        | Archivos en `plugin-name/commands/`         |
| Hooks en `settings.json`               | Hooks en `hooks/hooks.json`                 |
| Debe copiar manualmente para compartir | Instalar con `/plugin install`              |

<Note>
  Después de migrar, puede eliminar los archivos originales de `.claude/` para evitar duplicados. La versión del plugin tendrá prioridad cuando se cargue.
</Note>

## Próximos pasos

Ahora que entiende el sistema de plugins de Claude Code, aquí hay caminos sugeridos para diferentes objetivos:

### Para usuarios de plugins

* [Descubrir e instalar plugins](/es/discover-plugins): examine marketplaces e instale plugins
* [Configure marketplaces de equipo](/es/discover-plugins#configure-team-marketplaces): configure plugins a nivel de repositorio para su equipo

### Para desarrolladores de plugins

* [Crear y distribuir un marketplace](/es/plugin-marketplaces): empaquete y comparta sus plugins
* [Referencia de plugins](/es/plugins-reference): especificaciones técnicas completas
* Profundice en componentes específicos del plugin:
  * [Skills](/es/skills): detalles de desarrollo de skills
  * [Subagents](/es/sub-agents): configuración y capacidades del agente
  * [Hooks](/es/hooks): manejo de eventos y automatización
  * [MCP](/es/mcp): integración de herramientas externas
