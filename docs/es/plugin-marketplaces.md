> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Crear y distribuir un marketplace de plugins

> Cree y aloje marketplaces de plugins para distribuir extensiones de Claude Code en equipos y comunidades.

Un **marketplace de plugins** es un catálogo que le permite distribuir plugins a otros. Los marketplaces proporcionan descubrimiento centralizado, seguimiento de versiones, actualizaciones automáticas y soporte para múltiples tipos de fuentes (repositorios git, rutas locales y más). Esta guía le muestra cómo crear su propio marketplace para compartir plugins con su equipo o comunidad.

¿Busca instalar plugins desde un marketplace existente? Consulte [Descubrir e instalar plugins precompilados](/es/discover-plugins).

## Descripción general

Crear y distribuir un marketplace implica:

1. **Crear plugins**: construya uno o más plugins con comandos, agentes, hooks, MCP servers o servidores LSP. Esta guía asume que ya tiene plugins para distribuir; consulte [Crear plugins](/es/plugins) para obtener detalles sobre cómo crearlos.
2. **Crear un archivo de marketplace**: defina un `marketplace.json` que enumere sus plugins y dónde encontrarlos (consulte [Crear el archivo de marketplace](#create-the-marketplace-file)).
3. **Alojar el marketplace**: envíe a GitHub, GitLab u otro host git (consulte [Alojar y distribuir marketplaces](#host-and-distribute-marketplaces)).
4. **Compartir con usuarios**: los usuarios agregan su marketplace con `/plugin marketplace add` e instalan plugins individuales (consulte [Descubrir e instalar plugins](/es/discover-plugins)).

Una vez que su marketplace esté activo, puede actualizarlo enviando cambios a su repositorio. Los usuarios actualizan su copia local con `/plugin marketplace update`.

## Tutorial: crear un marketplace local

Este ejemplo crea un marketplace con un plugin: una skill `/quality-review` para revisiones de código. Creará la estructura de directorios, agregará una skill, creará el manifiesto del plugin y el catálogo del marketplace, luego lo instalará y probará.

<Steps>
  <Step title="Crear la estructura de directorios">
    ```bash  theme={null}
    mkdir -p my-marketplace/.claude-plugin
    mkdir -p my-marketplace/plugins/quality-review-plugin/.claude-plugin
    mkdir -p my-marketplace/plugins/quality-review-plugin/skills/quality-review
    ```
  </Step>

  <Step title="Crear la skill">
    Cree un archivo `SKILL.md` que defina qué hace la skill `/quality-review`.

    ```markdown my-marketplace/plugins/quality-review-plugin/skills/quality-review/SKILL.md theme={null}
    ---
    description: Review code for bugs, security, and performance
    disable-model-invocation: true
    ---

    Review the code I've selected or the recent changes for:
    - Potential bugs or edge cases
    - Security concerns
    - Performance issues
    - Readability improvements

    Be concise and actionable.
    ```
  </Step>

  <Step title="Crear el manifiesto del plugin">
    Cree un archivo `plugin.json` que describa el plugin. El manifiesto va en el directorio `.claude-plugin/`.

    ```json my-marketplace/plugins/quality-review-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "quality-review-plugin",
      "description": "Adds a /quality-review skill for quick code reviews",
      "version": "1.0.0"
    }
    ```
  </Step>

  <Step title="Crear el archivo de marketplace">
    Cree el catálogo de marketplace que enumera su plugin.

    ```json my-marketplace/.claude-plugin/marketplace.json theme={null}
    {
      "name": "my-plugins",
      "owner": {
        "name": "Your Name"
      },
      "plugins": [
        {
          "name": "quality-review-plugin",
          "source": "./plugins/quality-review-plugin",
          "description": "Adds a /quality-review skill for quick code reviews"
        }
      ]
    }
    ```
  </Step>

  <Step title="Agregar e instalar">
    Agregue el marketplace e instale el plugin.

    ```shell  theme={null}
    /plugin marketplace add ./my-marketplace
    /plugin install quality-review-plugin@my-plugins
    ```
  </Step>

  <Step title="Pruébelo">
    Seleccione algo de código en su editor y ejecute su nuevo comando.

    ```shell  theme={null}
    /quality-review
    ```
  </Step>
</Steps>

Para obtener más información sobre lo que los plugins pueden hacer, incluidos hooks, agentes, MCP servers y servidores LSP, consulte [Plugins](/es/plugins).

<Note>
  **Cómo se instalan los plugins**: Cuando los usuarios instalan un plugin, Claude Code copia el directorio del plugin a una ubicación de caché. Esto significa que los plugins no pueden hacer referencia a archivos fuera de su directorio usando rutas como `../shared-utils`, porque esos archivos no se copiarán.

  Si necesita compartir archivos entre plugins, use enlaces simbólicos (que se siguen durante la copia). Consulte [Plugin caching and file resolution](/es/plugins-reference#plugin-caching-and-file-resolution) para obtener detalles.
</Note>

## Crear el archivo de marketplace

Cree `.claude-plugin/marketplace.json` en la raíz de su repositorio. Este archivo define el nombre de su marketplace, información del propietario y una lista de plugins con sus fuentes.

Cada entrada de plugin necesita como mínimo un `name` y `source` (dónde obtenerlo). Consulte el [esquema completo](#marketplace-schema) a continuación para todos los campos disponibles.

```json  theme={null}
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@example.com"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "Automatic code formatting on save",
      "version": "2.1.0",
      "author": {
        "name": "DevTools Team"
      }
    },
    {
      "name": "deployment-tools",
      "source": {
        "source": "github",
        "repo": "company/deploy-plugin"
      },
      "description": "Deployment automation tools"
    }
  ]
}
```

## Esquema de marketplace

### Campos requeridos

| Campo     | Tipo   | Descripción                                                                                                                                                                  | Ejemplo            |
| :-------- | :----- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------- |
| `name`    | string | Identificador de marketplace (kebab-case, sin espacios). Esto es público: los usuarios lo ven al instalar plugins (por ejemplo, `/plugin install my-tool@your-marketplace`). | `"acme-tools"`     |
| `owner`   | object | Información del mantenedor del marketplace ([consulte los campos a continuación](#owner-fields))                                                                             |                    |
| `plugins` | array  | Lista de plugins disponibles                                                                                                                                                 | Ver a continuación |

<Note>
  **Nombres reservados**: Los siguientes nombres de marketplace están reservados para uso oficial de Anthropic y no pueden ser utilizados por marketplaces de terceros: `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `knowledge-work-plugins`, `life-sciences`. Los nombres que se hacen pasar por marketplaces oficiales (como `official-claude-plugins` o `anthropic-tools-v2`) también están bloqueados.
</Note>

### Campos del propietario

| Campo   | Tipo   | Requerido | Descripción                                   |
| :------ | :----- | :-------- | :-------------------------------------------- |
| `name`  | string | Sí        | Nombre del mantenedor o equipo                |
| `email` | string | No        | Correo electrónico de contacto del mantenedor |

### Metadatos opcionales

| Campo                  | Tipo   | Descripción                                                                                                                                                                             |
| :--------------------- | :----- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `metadata.description` | string | Descripción breve del marketplace                                                                                                                                                       |
| `metadata.version`     | string | Versión del marketplace                                                                                                                                                                 |
| `metadata.pluginRoot`  | string | Directorio base antepuesto a rutas de fuente de plugin relativas (por ejemplo, `"./plugins"` le permite escribir `"source": "formatter"` en lugar de `"source": "./plugins/formatter"`) |

## Entradas de plugins

Cada entrada de plugin en el array `plugins` describe un plugin y dónde encontrarlo. Puede incluir cualquier campo del [esquema de manifiesto de plugin](/es/plugins-reference#plugin-manifest-schema) (como `description`, `version`, `author`, `commands`, `hooks`, etc.), más estos campos específicos del marketplace: `source`, `category`, `tags` y `strict`.

### Campos requeridos

| Campo    | Tipo           | Descripción                                                                                                                                                  |
| :------- | :------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`   | string         | Identificador de plugin (kebab-case, sin espacios). Esto es público: los usuarios lo ven al instalar (por ejemplo, `/plugin install my-plugin@marketplace`). |
| `source` | string\|object | Dónde obtener el plugin (consulte [Fuentes de plugins](#plugin-sources) a continuación)                                                                      |

### Campos de plugin opcionales

**Campos de metadatos estándar:**

| Campo         | Tipo    | Descripción                                                                                                                                               |
| :------------ | :------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `description` | string  | Descripción breve del plugin                                                                                                                              |
| `version`     | string  | Versión del plugin                                                                                                                                        |
| `author`      | object  | Información del autor del plugin (`name` requerido, `email` opcional)                                                                                     |
| `homepage`    | string  | URL de página de inicio o documentación del plugin                                                                                                        |
| `repository`  | string  | URL del repositorio de código fuente                                                                                                                      |
| `license`     | string  | Identificador de licencia SPDX (por ejemplo, MIT, Apache-2.0)                                                                                             |
| `keywords`    | array   | Etiquetas para descubrimiento y categorización de plugins                                                                                                 |
| `category`    | string  | Categoría del plugin para organización                                                                                                                    |
| `tags`        | array   | Etiquetas para búsqueda                                                                                                                                   |
| `strict`      | boolean | Controla si `plugin.json` es la autoridad para definiciones de componentes (predeterminado: true). Consulte [Modo estricto](#strict-mode) a continuación. |

**Campos de configuración de componentes:**

| Campo        | Tipo           | Descripción                                                    |
| :----------- | :------------- | :------------------------------------------------------------- |
| `commands`   | string\|array  | Rutas personalizadas a archivos o directorios de comandos      |
| `agents`     | string\|array  | Rutas personalizadas a archivos de agentes                     |
| `hooks`      | string\|object | Configuración de hooks personalizada o ruta a archivo de hooks |
| `mcpServers` | string\|object | Configuraciones de MCP server o ruta a configuración de MCP    |
| `lspServers` | string\|object | Configuraciones de servidor LSP o ruta a configuración de LSP  |

## Fuentes de plugins

Las fuentes de plugins le indican a Claude Code dónde obtener cada plugin individual listado en su marketplace. Estos se establecen en el campo `source` de cada entrada de plugin en `marketplace.json`.

Una vez que un plugin se clona o copia en la máquina local, se copia en el caché de plugins versionado local en `~/.claude/plugins/cache`.

| Fuente        | Tipo                              | Campos                             | Notas                                                                                                         |
| ------------- | --------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Ruta relativa | `string` (p. ej. `"./my-plugin"`) | ninguno                            | Directorio local dentro del repositorio de marketplace. Debe comenzar con `./`                                |
| `github`      | object                            | `repo`, `ref?`, `sha?`             |                                                                                                               |
| `url`         | object                            | `url`, `ref?`, `sha?`              | Fuente de URL de Git                                                                                          |
| `git-subdir`  | object                            | `url`, `path`, `ref?`, `sha?`      | Subdirectorio dentro de un repositorio git. Clona escasamente para minimizar el ancho de banda para monorepos |
| `npm`         | object                            | `package`, `version?`, `registry?` | Instalado vía `npm install`                                                                                   |

<Note>
  **Fuentes de marketplace vs fuentes de plugins**: Estos son conceptos diferentes que controlan cosas diferentes.

  * **Fuente de marketplace** — dónde obtener el catálogo `marketplace.json` en sí. Se establece cuando los usuarios ejecutan `/plugin marketplace add` o en la configuración `extraKnownMarketplaces`. Soporta `ref` (rama/etiqueta) pero no `sha`.
  * **Fuente de plugin** — dónde obtener un plugin individual listado en el marketplace. Se establece en el campo `source` de cada entrada de plugin dentro de `marketplace.json`. Soporta tanto `ref` (rama/etiqueta) como `sha` (commit exacto).

  Por ejemplo, un marketplace alojado en `acme-corp/plugin-catalog` (fuente de marketplace) puede listar un plugin obtenido de `acme-corp/code-formatter` (fuente de plugin). La fuente de marketplace y la fuente de plugin apuntan a diferentes repositorios y se fijan independientemente.
</Note>

### Rutas relativas

Para plugins en el mismo repositorio, use una ruta que comience con `./`:

```json  theme={null}
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

Las rutas se resuelven relativas a la raíz del marketplace, que es el directorio que contiene `.claude-plugin/`. En el ejemplo anterior, `./plugins/my-plugin` apunta a `<repo>/plugins/my-plugin`, aunque `marketplace.json` vive en `<repo>/.claude-plugin/marketplace.json`. No use `../` para salir de `.claude-plugin/`.

<Note>
  Las rutas relativas solo funcionan cuando los usuarios agregan su marketplace a través de Git (GitHub, GitLab o URL de git). Si los usuarios agregan su marketplace a través de una URL directa al archivo `marketplace.json`, las rutas relativas no se resolverán correctamente. Para distribución basada en URL, use fuentes de GitHub, npm o URL de git en su lugar. Consulte [Solución de problemas](#plugins-with-relative-paths-fail-in-url-based-marketplaces) para obtener detalles.
</Note>

### Repositorios de GitHub

```json  theme={null}
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```

Puede fijar a una rama, etiqueta o commit específico:

```json  theme={null}
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| Campo  | Tipo   | Descripción                                                                              |
| :----- | :----- | :--------------------------------------------------------------------------------------- |
| `repo` | string | Requerido. Repositorio de GitHub en formato `owner/repo`                                 |
| `ref`  | string | Opcional. Rama o etiqueta de Git (por defecto es la rama predeterminada del repositorio) |
| `sha`  | string | Opcional. SHA de commit de git completo de 40 caracteres para fijar a una versión exacta |

### Repositorios de Git

```json  theme={null}
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

Puede fijar a una rama, etiqueta o commit específico:

```json  theme={null}
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git",
    "ref": "main",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| Campo | Tipo   | Descripción                                                                                                                                                                      |
| :---- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url` | string | Requerido. URL completa del repositorio de git (`https://` o `git@`). El sufijo `.git` es opcional, por lo que las URLs de Azure DevOps y AWS CodeCommit sin el sufijo funcionan |
| `ref` | string | Opcional. Rama o etiqueta de Git (por defecto es la rama predeterminada del repositorio)                                                                                         |
| `sha` | string | Opcional. SHA de commit de git completo de 40 caracteres para fijar a una versión exacta                                                                                         |

### Subdirectorios de Git

Use `git-subdir` para apuntar a un plugin que vive dentro de un subdirectorio de un repositorio de git. Claude Code usa un clon parcial y escaso para obtener solo el subdirectorio, minimizando el ancho de banda para monorepos grandes.

```json  theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin"
  }
}
```

Puede fijar a una rama, etiqueta o commit específico:

```json  theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

El campo `url` también acepta una abreviatura de GitHub (`owner/repo`) o URLs SSH (`git@github.com:owner/repo.git`).

| Campo  | Tipo   | Descripción                                                                                                            |
| :----- | :----- | :--------------------------------------------------------------------------------------------------------------------- |
| `url`  | string | Requerido. URL del repositorio de Git, abreviatura de GitHub `owner/repo` o URL SSH                                    |
| `path` | string | Requerido. Ruta del subdirectorio dentro del repositorio que contiene el plugin (por ejemplo, `"tools/claude-plugin"`) |
| `ref`  | string | Opcional. Rama o etiqueta de Git (por defecto es la rama predeterminada del repositorio)                               |
| `sha`  | string | Opcional. SHA de commit de git completo de 40 caracteres para fijar a una versión exacta                               |

### Paquetes npm

Los plugins distribuidos como paquetes npm se instalan usando `npm install`. Esto funciona con cualquier paquete en el registro npm público o un registro privado que su equipo aloje.

```json  theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin"
  }
}
```

Para fijar a una versión específica, agregue el campo `version`:

```json  theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "2.1.0"
  }
}
```

Para instalar desde un registro privado o interno, agregue el campo `registry`:

```json  theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "^2.0.0",
    "registry": "https://npm.example.com"
  }
}
```

| Campo      | Tipo   | Descripción                                                                                                     |
| :--------- | :----- | :-------------------------------------------------------------------------------------------------------------- |
| `package`  | string | Requerido. Nombre del paquete o paquete con alcance (por ejemplo, `@org/plugin`)                                |
| `version`  | string | Opcional. Versión o rango de versión (por ejemplo, `2.1.0`, `^2.0.0`, `~1.5.0`)                                 |
| `registry` | string | Opcional. URL de registro npm personalizado. Por defecto es el registro npm del sistema (típicamente npmjs.org) |

### Entradas de plugins avanzadas

Este ejemplo muestra una entrada de plugin usando muchos de los campos opcionales, incluidas rutas personalizadas para comandos, agentes, hooks y MCP servers:

```json  theme={null}
{
  "name": "enterprise-tools",
  "source": {
    "source": "github",
    "repo": "company/enterprise-plugin"
  },
  "description": "Enterprise workflow automation tools",
  "version": "2.1.0",
  "author": {
    "name": "Enterprise Team",
    "email": "enterprise@example.com"
  },
  "homepage": "https://docs.example.com/plugins/enterprise-tools",
  "repository": "https://github.com/company/enterprise-plugin",
  "license": "MIT",
  "keywords": ["enterprise", "workflow", "automation"],
  "category": "productivity",
  "commands": [
    "./commands/core/",
    "./commands/enterprise/",
    "./commands/experimental/preview.md"
  ],
  "agents": ["./agents/security-reviewer.md", "./agents/compliance-checker.md"],
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  },
  "mcpServers": {
    "enterprise-db": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  },
  "strict": false
}
```

Cosas clave a notar:

* **`commands` y `agents`**: Puede especificar múltiples directorios o archivos individuales. Las rutas son relativas a la raíz del plugin.
* **`${CLAUDE_PLUGIN_ROOT}`**: Use esta variable en hooks y configuraciones de MCP server para hacer referencia a archivos dentro del directorio de instalación del plugin. Esto es necesario porque los plugins se copian a una ubicación de caché cuando se instalan. Para dependencias o estado que deben sobrevivir a las actualizaciones de plugins, use [`${CLAUDE_PLUGIN_DATA}`](/es/plugins-reference#persistent-data-directory) en su lugar.
* **`strict: false`**: Dado que esto se establece en false, el plugin no necesita su propio `plugin.json`. La entrada del marketplace define todo. Consulte [Modo estricto](#strict-mode) a continuación.

### Modo estricto

El campo `strict` controla si `plugin.json` es la autoridad para definiciones de componentes (comandos, agentes, hooks, skills, MCP servers, estilos de salida).

| Valor                   | Comportamiento                                                                                                                                                              |
| :---------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `true` (predeterminado) | `plugin.json` es la autoridad. La entrada del marketplace puede complementarla con componentes adicionales, y ambas fuentes se fusionan.                                    |
| `false`                 | La entrada del marketplace es la definición completa. Si el plugin también tiene un `plugin.json` que declara componentes, eso es un conflicto y el plugin falla al cargar. |

**Cuándo usar cada modo:**

* **`strict: true`**: el plugin tiene su propio `plugin.json` y gestiona sus propios componentes. La entrada del marketplace puede agregar comandos o hooks adicionales encima. Este es el predeterminado y funciona para la mayoría de los plugins.
* **`strict: false`**: el operador del marketplace quiere control total. El repositorio del plugin proporciona archivos sin procesar, y la entrada del marketplace define cuáles de esos archivos se exponen como comandos, agentes, hooks, etc. Útil cuando el marketplace reestructura o cura los componentes de un plugin de manera diferente a la que el autor del plugin pretendía.

## Alojar y distribuir marketplaces

### Alojar en GitHub (recomendado)

GitHub proporciona el método de distribución más fácil:

1. **Crear un repositorio**: Configure un nuevo repositorio para su marketplace
2. **Agregar archivo de marketplace**: Cree `.claude-plugin/marketplace.json` con sus definiciones de plugins
3. **Compartir con equipos**: Los usuarios agregan su marketplace con `/plugin marketplace add owner/repo`

**Beneficios**: Control de versiones integrado, seguimiento de problemas y características de colaboración en equipo.

### Alojar en otros servicios de git

Cualquier servicio de alojamiento de git funciona, como GitLab, Bitbucket y servidores autohospedados. Los usuarios agregan con la URL completa del repositorio:

```shell  theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git
```

### Repositorios privados

Claude Code soporta instalar plugins desde repositorios privados. Para instalación manual y actualizaciones, Claude Code usa sus ayudantes de credenciales de git existentes. Si `git clone` funciona para un repositorio privado en su terminal, funciona en Claude Code también. Los ayudantes de credenciales comunes incluyen `gh auth login` para GitHub, Keychain de macOS y `git-credential-store`.

Las actualizaciones automáticas en segundo plano se ejecutan al inicio sin ayudantes de credenciales, ya que los mensajes interactivos bloquearían que Claude Code se inicie. Para habilitar actualizaciones automáticas para marketplaces privados, establezca el token de autenticación apropiado en su entorno:

| Proveedor | Variables de entorno        | Notas                                                     |
| :-------- | :-------------------------- | :-------------------------------------------------------- |
| GitHub    | `GITHUB_TOKEN` o `GH_TOKEN` | Token de acceso personal o token de GitHub App            |
| GitLab    | `GITLAB_TOKEN` o `GL_TOKEN` | Token de acceso personal o token de proyecto              |
| Bitbucket | `BITBUCKET_TOKEN`           | Contraseña de aplicación o token de acceso al repositorio |

Establezca el token en su configuración de shell (por ejemplo, `.bashrc`, `.zshrc`) o páselo al ejecutar Claude Code:

```bash  theme={null}
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

<Note>
  Para entornos de CI/CD, configure el token como una variable de entorno secreta. GitHub Actions proporciona automáticamente `GITHUB_TOKEN` para repositorios en la misma organización.
</Note>

### Probar localmente antes de la distribución

Pruebe su marketplace localmente antes de compartirlo:

```shell  theme={null}
/plugin marketplace add ./my-local-marketplace
/plugin install test-plugin@my-local-marketplace
```

Para el rango completo de comandos add (GitHub, URLs de Git, rutas locales, URLs remotas), consulte [Agregar marketplaces](/es/discover-plugins#add-marketplaces).

### Requerir marketplaces para su equipo

Puede configurar su repositorio para que los miembros del equipo sean automáticamente solicitados para instalar su marketplace cuando confíen en la carpeta del proyecto. Agregue su marketplace a `.claude/settings.json`:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

También puede especificar qué plugins deben estar habilitados de forma predeterminada:

```json  theme={null}
{
  "enabledPlugins": {
    "code-formatter@company-tools": true,
    "deployment-tools@company-tools": true
  }
}
```

Para opciones de configuración completas, consulte [Configuración de plugins](/es/settings#plugin-settings).

### Precargar plugins para contenedores

Para imágenes de contenedor y entornos de CI, puede precargar un directorio de plugins en tiempo de compilación para que Claude Code comience con marketplaces y plugins ya disponibles, sin clonar nada en tiempo de ejecución. Establezca la variable de entorno `CLAUDE_CODE_PLUGIN_SEED_DIR` para apuntar a este directorio.

Para superponer múltiples directorios seed, separe las rutas con `:` en Unix o `;` en Windows. Claude Code busca cada directorio en orden, y el primer seed que contiene un marketplace o caché de plugin dado gana.

El directorio seed refleja la estructura de `~/.claude/plugins`:

```
$CLAUDE_CODE_PLUGIN_SEED_DIR/
  known_marketplaces.json
  marketplaces/<name>/...
  cache/<marketplace>/<plugin>/<version>/...
```

La forma más simple de construir un directorio seed es ejecutar Claude Code una vez durante la compilación de la imagen, instalar los plugins que necesita, luego copiar el directorio `~/.claude/plugins` resultante en su imagen y apuntar `CLAUDE_CODE_PLUGIN_SEED_DIR` a él.

Al inicio, Claude Code registra los marketplaces encontrados en el `known_marketplaces.json` del seed en la configuración principal, y usa cachés de plugins encontrados bajo `cache/` en su lugar sin re-clonar. Esto funciona tanto en modo interactivo como en modo no interactivo con la bandera `-p`.

Detalles de comportamiento:

* **Solo lectura**: el directorio seed nunca se escribe. Las actualizaciones automáticas están deshabilitadas para marketplaces seed ya que git pull fallaría en un sistema de archivos de solo lectura.
* **Las entradas seed tienen precedencia**: los marketplaces declarados en el seed sobrescriben cualquier entrada coincidente en la configuración del usuario en cada inicio. Para optar por no participar en un plugin seed, use `/plugin disable` en lugar de eliminar el marketplace.
* **Resolución de rutas**: Claude Code localiza contenido de marketplace sondeando `$CLAUDE_CODE_PLUGIN_SEED_DIR/marketplaces/<name>/` en tiempo de ejecución, no confiando en rutas almacenadas dentro del JSON del seed. Esto significa que el seed funciona correctamente incluso cuando se monta en una ruta diferente a donde fue construido.
* **Se compone con configuración**: si `extraKnownMarketplaces` o `enabledPlugins` declaran un marketplace que ya existe en el seed, Claude Code usa la copia del seed en lugar de clonar.

### Restricciones de marketplace administrado

Para organizaciones que requieren control estricto sobre las fuentes de plugins, los administradores pueden restringir qué marketplaces de plugins se permite a los usuarios agregar usando la configuración [`strictKnownMarketplaces`](/es/settings#strictknownmarketplaces) en configuración administrada.

Cuando `strictKnownMarketplaces` se configura en configuración administrada, el comportamiento de restricción depende del valor:

| Valor                       | Comportamiento                                                                                     |
| --------------------------- | -------------------------------------------------------------------------------------------------- |
| Indefinido (predeterminado) | Sin restricciones. Los usuarios pueden agregar cualquier marketplace                               |
| Array vacío `[]`            | Bloqueo completo. Los usuarios no pueden agregar nuevos marketplaces                               |
| Lista de fuentes            | Los usuarios solo pueden agregar marketplaces que coincidan exactamente con la lista de permitidos |

#### Configuraciones comunes

Deshabilitar todas las adiciones de marketplace:

```json  theme={null}
{
  "strictKnownMarketplaces": []
}
```

Permitir solo marketplaces específicos:

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
    }
  ]
}
```

Permitir todos los marketplaces desde un servidor git interno usando coincidencia de patrón regex en el host:

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

Permitir marketplaces basados en sistema de archivos desde un directorio específico usando coincidencia de patrón regex en la ruta:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "pathPattern",
      "pathPattern": "^/opt/approved/"
    }
  ]
}
```

Use `".*"` como `pathPattern` para permitir cualquier ruta del sistema de archivos mientras aún controla fuentes de red con `hostPattern`.

<Note>
  `strictKnownMarketplaces` restringe lo que los usuarios pueden agregar, pero no registra marketplaces por sí solo. Para hacer que los marketplaces permitidos estén disponibles automáticamente sin que los usuarios ejecuten `/plugin marketplace add`, emparéjelo con [`extraKnownMarketplaces`](/es/settings#extraknownmarketplaces) en el mismo `managed-settings.json`. Consulte [Usar ambos juntos](/es/settings#strictknownmarketplaces).
</Note>

#### Cómo funcionan las restricciones

Las restricciones se validan temprano en el proceso de instalación de plugins, antes de cualquier solicitud de red u operación del sistema de archivos. Esto previene intentos de acceso no autorizado a marketplaces.

La lista de permitidos usa coincidencia exacta para la mayoría de tipos de fuente. Para que un marketplace sea permitido, todos los campos especificados deben coincidir exactamente:

* Para fuentes de GitHub: `repo` es requerido, y `ref` o `path` también deben coincidir si se especifican en la lista de permitidos
* Para fuentes de URL: la URL completa debe coincidir exactamente
* Para fuentes `hostPattern`: el host del marketplace se compara contra el patrón regex
* Para fuentes `pathPattern`: la ruta del sistema de archivos del marketplace se compara contra el patrón regex

Debido a que `strictKnownMarketplaces` se establece en [configuración administrada](/es/settings#settings-files), los usuarios individuales y las configuraciones del proyecto no pueden anular estas restricciones.

Para detalles de configuración completos incluyendo todos los tipos de fuente soportados y comparación con `extraKnownMarketplaces`, consulte la [referencia de strictKnownMarketplaces](/es/settings#strictknownmarketplaces).

### Resolución de versiones y canales de lanzamiento

Las versiones de plugins determinan rutas de caché y detección de actualizaciones. Puede especificar la versión en el manifiesto del plugin (`plugin.json`) o en la entrada del marketplace (`marketplace.json`).

<Warning>
  Cuando sea posible, evite establecer la versión en ambos lugares. El manifiesto del plugin siempre gana silenciosamente, lo que puede causar que la versión del marketplace sea ignorada. Para plugins de ruta relativa, establezca la versión en la entrada del marketplace. Para todas las otras fuentes de plugins, establézcala en el manifiesto del plugin.
</Warning>

#### Configurar canales de lanzamiento

Para soportar canales de lanzamiento "estable" y "último" para sus plugins, puede configurar dos marketplaces que apunten a diferentes refs o SHAs del mismo repositorio. Luego puede asignar los dos marketplaces a diferentes grupos de usuarios a través de [configuración administrada](/es/settings#settings-files).

<Warning>
  El `plugin.json` del plugin debe declarar una `version` diferente en cada ref o commit fijado. Si dos refs o commits tienen la misma versión de manifiesto, Claude Code los trata como idénticos y omite la actualización.
</Warning>

##### Ejemplo

```json  theme={null}
{
  "name": "stable-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": {
        "source": "github",
        "repo": "acme-corp/code-formatter",
        "ref": "stable"
      }
    }
  ]
}
```

```json  theme={null}
{
  "name": "latest-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": {
        "source": "github",
        "repo": "acme-corp/code-formatter",
        "ref": "latest"
      }
    }
  ]
}
```

##### Asignar canales a grupos de usuarios

Asigne cada marketplace al grupo de usuarios apropiado a través de configuración administrada. Por ejemplo, el grupo estable recibe:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "stable-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/stable-tools"
      }
    }
  }
}
```

El grupo de acceso temprano recibe `latest-tools` en su lugar:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "latest-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/latest-tools"
      }
    }
  }
}
```

## Validación y pruebas

Pruebe su marketplace antes de compartirlo.

Valide la sintaxis JSON de su marketplace:

```bash  theme={null}
claude plugin validate .
```

O desde dentro de Claude Code:

```shell  theme={null}
/plugin validate .
```

Agregue el marketplace para pruebas:

```shell  theme={null}
/plugin marketplace add ./path/to/marketplace
```

Instale un plugin de prueba para verificar que todo funciona:

```shell  theme={null}
/plugin install test-plugin@marketplace-name
```

Para flujos de trabajo completos de prueba de plugins, consulte [Pruebe sus plugins localmente](/es/plugins#test-your-plugins-locally). Para solución de problemas técnicos, consulte [Referencia de plugins](/es/plugins-reference).

## Solución de problemas

### Marketplace no se carga

**Síntomas**: No puede agregar marketplace o ver plugins de él

**Soluciones**:

* Verifique que la URL del marketplace sea accesible
* Compruebe que `.claude-plugin/marketplace.json` existe en la ruta especificada
* Asegúrese de que la sintaxis JSON sea válida y el frontmatter esté bien formado usando `claude plugin validate` o `/plugin validate`
* Para repositorios privados, confirme que tiene permisos de acceso

### Errores de validación de marketplace

Ejecute `claude plugin validate .` o `/plugin validate .` desde su directorio de marketplace para verificar problemas. El validador verifica `plugin.json`, frontmatter de skill/agente/comando y `hooks/hooks.json` para errores de sintaxis y esquema. Errores comunes:

| Error                                             | Causa                                                  | Solución                                                                                                       |
| :------------------------------------------------ | :----------------------------------------------------- | :------------------------------------------------------------------------------------------------------------- |
| `File not found: .claude-plugin/marketplace.json` | Manifiesto faltante                                    | Cree `.claude-plugin/marketplace.json` con campos requeridos                                                   |
| `Invalid JSON syntax: Unexpected token...`        | Error de sintaxis JSON en marketplace.json             | Verifique comas faltantes, comas extra o cadenas sin comillas                                                  |
| `Duplicate plugin name "x" found in marketplace`  | Dos plugins comparten el mismo nombre                  | Dé a cada plugin un valor `name` único                                                                         |
| `plugins[0].source: Path contains ".."`           | La ruta de fuente contiene `..`                        | Use rutas relativas a la raíz del marketplace sin `..`. Consulte [Rutas relativas](#relative-paths)            |
| `YAML frontmatter failed to parse: ...`           | YAML inválido en un archivo de skill, agente o comando | Corrija la sintaxis YAML en el bloque frontmatter. En tiempo de ejecución este archivo se carga sin metadatos. |
| `Invalid JSON syntax: ...` (hooks.json)           | `hooks/hooks.json` malformado                          | Corrija la sintaxis JSON. Un `hooks/hooks.json` malformado previene que todo el plugin se cargue.              |

**Advertencias** (no bloqueantes):

* `Marketplace has no plugins defined`: agregue al menos un plugin al array `plugins`
* `No marketplace description provided`: agregue `metadata.description` para ayudar a los usuarios a entender su marketplace
* `Plugin name "x" is not kebab-case`: el nombre del plugin contiene letras mayúsculas, espacios o caracteres especiales. Renombre a letras minúsculas, dígitos y guiones solamente (por ejemplo, `my-plugin`). Claude Code acepta otras formas, pero la sincronización del marketplace de Claude.ai las rechaza.

### Fallos de instalación de plugins

**Síntomas**: El marketplace aparece pero la instalación del plugin falla

**Soluciones**:

* Verifique que las URLs de fuente del plugin sean accesibles
* Compruebe que los directorios de plugins contengan archivos requeridos
* Para fuentes de GitHub, asegúrese de que los repositorios sean públicos o tenga acceso
* Pruebe las fuentes de plugins manualmente clonando/descargando

### La autenticación del repositorio privado falla

**Síntomas**: Errores de autenticación al instalar plugins desde repositorios privados

**Soluciones**:

Para instalación manual y actualizaciones:

* Verifique que esté autenticado con su proveedor de git (por ejemplo, ejecute `gh auth status` para GitHub)
* Compruebe que su ayudante de credenciales esté configurado correctamente: `git config --global credential.helper`
* Intente clonar el repositorio manualmente para verificar que sus credenciales funcionan

Para actualizaciones automáticas en segundo plano:

* Establezca el token apropiado en su entorno: `echo $GITHUB_TOKEN`
* Compruebe que el token tiene los permisos requeridos (acceso de lectura al repositorio)
* Para GitHub, asegúrese de que el token tiene el alcance `repo` para repositorios privados
* Para GitLab, asegúrese de que el token tiene al menos alcance `read_repository`
* Verifique que el token no haya expirado

### Las operaciones de Git agotan el tiempo de espera

**Síntomas**: La instalación del plugin o las actualizaciones del marketplace fallan con un error de tiempo de espera como "Git clone timed out after 120s" o "Git pull timed out after 120s".

**Causa**: Claude Code usa un tiempo de espera de 120 segundos para todas las operaciones de git, incluida la clonación de repositorios de plugins y la extracción de actualizaciones de marketplace. Los repositorios grandes o las conexiones de red lentas pueden exceder este límite.

**Solución**: Aumente el tiempo de espera usando la variable de entorno `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`. El valor está en milisegundos:

```bash  theme={null}
export CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=300000  # 5 minutos
```

### Los plugins con rutas relativas fallan en marketplaces basados en URL

**Síntomas**: Agregó un marketplace a través de URL (como `https://example.com/marketplace.json`), pero los plugins con fuentes de ruta relativa como `"./plugins/my-plugin"` fallan al instalar con errores "path not found".

**Causa**: Los marketplaces basados en URL solo descargan el archivo `marketplace.json` en sí. No descargan archivos de plugins del servidor. Las rutas relativas en la entrada del marketplace hacen referencia a archivos en el servidor remoto que no fueron descargados.

**Soluciones**:

* **Use fuentes externas**: Cambie las entradas de plugins para usar fuentes de GitHub, npm o URL de git en lugar de rutas relativas:
  ```json  theme={null}
  { "name": "my-plugin", "source": { "source": "github", "repo": "owner/repo" } }
  ```
* **Use un marketplace basado en Git**: Aloje su marketplace en un repositorio de Git y agréguelo con la URL de git. Los marketplaces basados en Git clonan el repositorio completo, haciendo que las rutas relativas funcionen correctamente.

### Archivos no encontrados después de la instalación

**Síntomas**: El plugin se instala pero las referencias a archivos fallan, especialmente archivos fuera del directorio del plugin

**Causa**: Los plugins se copian a un directorio de caché en lugar de usarse en el lugar. Las rutas que hacen referencia a archivos fuera del directorio del plugin (como `../shared-utils`) no funcionarán porque esos archivos no se copian.

**Soluciones**: Consulte [Plugin caching and file resolution](/es/plugins-reference#plugin-caching-and-file-resolution) para soluciones alternativas incluyendo enlaces simbólicos y reestructuración de directorios.

Para herramientas de depuración adicionales y problemas comunes, consulte [Debugging and development tools](/es/plugins-reference#debugging-and-development-tools).

## Ver también

* [Descubrir e instalar plugins precompilados](/es/discover-plugins) - Instalación de plugins desde marketplaces existentes
* [Plugins](/es/plugins) - Creación de sus propios plugins
* [Referencia de plugins](/es/plugins-reference) - Especificaciones técnicas completas y esquemas
* [Configuración de plugins](/es/settings#plugin-settings) - Opciones de configuración de plugins
* [Referencia de strictKnownMarketplaces](/es/settings#strictknownmarketplaces) - Restricciones de marketplace administrado
