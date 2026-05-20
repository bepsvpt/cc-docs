> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Descubra e instale plugins pregenerados a través de mercados

> Encuentre e instale plugins de mercados para extender Claude Code con nuevas skills, agentes y capacidades.

Los plugins extienden Claude Code con skills, agentes, hooks y servidores MCP. Los mercados de plugins son catálogos que le ayudan a descubrir e instalar estas extensiones sin construirlas usted mismo.

¿Busca crear y distribuir su propio mercado? Consulte [Crear y distribuir un mercado de plugins](/es/plugin-marketplaces).

## Cómo funcionan los mercados

Un mercado es un catálogo de plugins que alguien más ha creado y compartido. Usar un mercado es un proceso de dos pasos:

<Steps>
  <Step title="Agregar el mercado">
    Esto registra el catálogo con Claude Code para que pueda explorar lo que está disponible. Aún no se instalan plugins.
  </Step>

  <Step title="Instalar plugins individuales">
    Explore el catálogo e instale los plugins que desee.
  </Step>
</Steps>

Piénselo como agregar una tienda de aplicaciones: agregar la tienda le da acceso para explorar su colección, pero usted sigue eligiendo qué aplicaciones descargar individualmente.

## Mercado oficial de Anthropic

El mercado oficial de Anthropic (`claude-plugins-official`) está disponible automáticamente cuando inicia Claude Code. Ejecute `/plugin` y vaya a la pestaña **Discover** para explorar lo que está disponible, o vea el catálogo en [claude.com/plugins](https://claude.com/plugins).

Para instalar un plugin del mercado oficial, use `/plugin install <name>@claude-plugins-official`. Por ejemplo, para instalar la integración de GitHub:

```shell theme={null}
/plugin install github@claude-plugins-official
```

Si Claude Code reporta que el plugin no se encuentra en ningún mercado, su mercado está faltando o desactualizado. Ejecute `/plugin marketplace update claude-plugins-official` para actualizarlo, o `/plugin marketplace add anthropics/claude-plugins-official` si no lo ha agregado antes. Luego reintente la instalación.

<Note>
  El mercado oficial es curado por Anthropic, y la inclusión está a discreción de Anthropic. Los formularios de envío en la aplicación agregan plugins al [mercado comunitario](#community-marketplace), no al oficial. Para distribuir plugins de forma independiente, [cree su propio mercado](/es/plugin-marketplaces) y compártalo con los usuarios.
</Note>

El mercado oficial incluye varias categorías de plugins:

### Code intelligence

Los plugins de code intelligence habilitan la herramienta LSP integrada de Claude Code, dándole a Claude la capacidad de saltar a definiciones, encontrar referencias y ver errores de tipo inmediatamente después de ediciones. Estos plugins configuran conexiones de [Language Server Protocol](https://microsoft.github.io/language-server-protocol/), la misma tecnología que potencia la inteligencia de código de VS Code.

Estos plugins requieren que el binario del servidor de lenguaje esté instalado en su sistema. Si ya tiene un servidor de lenguaje instalado, Claude puede solicitarle que instale el plugin correspondiente cuando abra un proyecto.

| Lenguaje   | Plugin              | Binario requerido            |
| :--------- | :------------------ | :--------------------------- |
| C/C++      | `clangd-lsp`        | `clangd`                     |
| C#         | `csharp-lsp`        | `csharp-ls`                  |
| Go         | `gopls-lsp`         | `gopls`                      |
| Java       | `jdtls-lsp`         | `jdtls`                      |
| Kotlin     | `kotlin-lsp`        | `kotlin-language-server`     |
| Lua        | `lua-lsp`           | `lua-language-server`        |
| PHP        | `php-lsp`           | `intelephense`               |
| Python     | `pyright-lsp`       | `pyright-langserver`         |
| Rust       | `rust-analyzer-lsp` | `rust-analyzer`              |
| Swift      | `swift-lsp`         | `sourcekit-lsp`              |
| TypeScript | `typescript-lsp`    | `typescript-language-server` |

También puede [crear su propio plugin LSP](/es/plugins-reference#lsp-servers) para otros lenguajes.

<Note>
  Si ve `Executable not found in $PATH` en la pestaña Errors de `/plugin` después de instalar un plugin, instale el binario requerido de la tabla anterior.
</Note>

#### Lo que Claude gana con los plugins de code intelligence

Una vez que se instala un plugin de code intelligence y su binario de servidor de lenguaje está disponible, Claude gana dos capacidades:

* **Diagnósticos automáticos**: después de cada edición de archivo que Claude realiza, el servidor de lenguaje analiza los cambios e informa errores y advertencias automáticamente. Claude ve errores de tipo, importaciones faltantes y problemas de sintaxis sin necesidad de ejecutar un compilador o linter. Si Claude introduce un error, lo nota y corrige el problema en el mismo turno. Esto no requiere configuración más allá de instalar el plugin. Puede ver diagnósticos en línea presionando **Ctrl+O** cuando aparece el indicador "diagnostics found".
* **Navegación de código**: Claude puede usar el servidor de lenguaje para saltar a definiciones, encontrar referencias, obtener información de tipo al pasar el ratón, listar símbolos, encontrar implementaciones y rastrear jerarquías de llamadas. Estas operaciones dan a Claude una navegación más precisa que la búsqueda basada en grep, aunque la disponibilidad puede variar según el lenguaje y el entorno.

Si encuentra problemas, consulte [Solución de problemas de code intelligence](#code-intelligence-issues).

### External integrations

Estos plugins incluyen [servidores MCP](/es/mcp) preconfigurados para que pueda conectar Claude a servicios externos sin configuración manual:

* **Source control**: `github`, `gitlab`
* **Project management**: `atlassian` (Jira/Confluence), `asana`, `linear`, `notion`
* **Design**: `figma`
* **Infrastructure**: `vercel`, `firebase`, `supabase`
* **Communication**: `slack`
* **Monitoring**: `sentry`

### Development workflows

Plugins que agregan skills y agentes para tareas de desarrollo comunes:

* **commit-commands**: Flujos de trabajo de confirmación de Git incluyendo confirmación, push y creación de PR
* **pr-review-toolkit**: Agentes especializados para revisar solicitudes de extracción
* **agent-sdk-dev**: Herramientas para construir con el Claude Agent SDK
* **plugin-dev**: Kit de herramientas para crear sus propios plugins

### Output styles

Personalice cómo responde Claude:

* **explanatory-output-style**: Información educativa sobre opciones de implementación
* **learning-output-style**: Modo de aprendizaje interactivo para construcción de skills

## Community marketplace

El mercado comunitario en [`anthropics/claude-plugins-community`](https://github.com/anthropics/claude-plugins-community) aloja plugins de terceros que han pasado la validación automatizada de Anthropic y el análisis de seguridad. Cada plugin está fijado a un SHA de confirmación específico en el catálogo. A diferencia del mercado oficial, lo agrega manualmente:

```shell theme={null}
/plugin marketplace add anthropics/claude-plugins-community
```

Luego instale plugins desde él usando el nombre de mercado `claude-community`:

```shell theme={null}
/plugin install <plugin-name>@claude-community
```

Para enviar su propio plugin al mercado comunitario, consulte [Enviar su plugin al mercado comunitario](/es/plugins#submit-your-plugin-to-the-community-marketplace) en la guía de creación de plugins.

## Pruébelo: agregue el mercado de demostración

Anthropic también mantiene un [mercado de plugins de demostración](https://github.com/anthropics/claude-code/tree/main/plugins) (`claude-code-plugins`) con plugins de ejemplo que muestran lo que es posible con el sistema de plugins. A diferencia del mercado oficial, debe agregar este manualmente.

<Steps>
  <Step title="Agregar el mercado">
    Desde dentro de Claude Code, ejecute el comando `plugin marketplace add` para el mercado `anthropics/claude-code`:

    ```shell theme={null}
    /plugin marketplace add anthropics/claude-code
    ```

    Esto descarga el catálogo del mercado y pone sus plugins a su disposición.
  </Step>

  <Step title="Explorar plugins disponibles">
    Ejecute `/plugin` para abrir el administrador de plugins. Esto abre una interfaz con pestañas con cuatro pestañas por las que puede ciclar usando **Tab** (o **Shift+Tab** para ir hacia atrás):

    * **Discover**: explore plugins disponibles de todos sus mercados
    * **Installed**: vea y administre sus plugins instalados
    * **Marketplaces**: agregue, elimine o actualice sus mercados agregados
    * **Errors**: vea cualquier error de carga de plugins

    Vaya a la pestaña **Discover** para ver plugins del mercado que acaba de agregar.
  </Step>

  <Step title="Instalar un plugin">
    Seleccione un plugin para ver sus detalles. El panel de detalles muestra lo que contiene el plugin y cuánto cuesta:

    * {/* min-version: 2.1.143 */}Una estimación de **Context cost** para que pueda ver cuántos tokens el plugin agregará a su [ventana de contexto](/es/features-overview#understand-context-costs) en cada turno (Claude Code v2.1.143 y posteriores)
    * {/* min-version: 2.1.144 */}La fecha de **Last updated** del plugin (v2.1.144 y posteriores)
    * {/* min-version: 2.1.145 */}Una sección **Will install** que enumera los comandos, agentes, skills, hooks y servidores MCP y LSP del plugin, para que pueda revisar exactamente qué agrega antes de instalar (v2.1.145 y posteriores)

    Elija un alcance de instalación:

    * **User scope**: instale para usted en todos los proyectos
    * **Project scope**: instale para todos los colaboradores en este repositorio
    * **Local scope**: instale para usted en este repositorio solamente

    Por ejemplo, seleccione **commit-commands** (un plugin que agrega skills de flujo de trabajo de git) e instálelo en su alcance de usuario.

    También puede instalar directamente desde la línea de comandos:

    ```shell theme={null}
    /plugin install commit-commands@anthropics-claude-code
    ```

    Consulte [Configuration scopes](/es/settings#configuration-scopes) para obtener más información sobre alcances.
  </Step>

  <Step title="Usar su nuevo plugin">
    Después de instalar, ejecute `/reload-plugins` para activar el plugin. Las skills de plugin tienen espacios de nombres por el nombre del plugin, por lo que **commit-commands** proporciona skills como `/commit-commands:commit`.

    Pruébelo haciendo un cambio en un archivo y ejecutando:

    ```shell theme={null}
    /commit-commands:commit
    ```

    Esto prepara sus cambios, genera un mensaje de confirmación y crea la confirmación.

    Cada plugin funciona de manera diferente. Consulte los detalles del plugin en la pestaña **Discover** para ver los comandos y skills que proporciona, o visite su página de inicio para obtener orientación sobre el uso.
  </Step>
</Steps>

El resto de esta guía cubre todas las formas en que puede agregar mercados, instalar plugins y administrar su configuración.

## Agregar mercados

Use el comando `/plugin marketplace add` para agregar mercados de diferentes fuentes.

<Tip>
  **Atajos**: Puede usar `/plugin market` en lugar de `/plugin marketplace`, y `rm` en lugar de `remove`.
</Tip>

* **Repositorios de GitHub**: formato `owner/repo` (por ejemplo, `anthropics/claude-code`)
* **URLs de Git**: cualquier URL de repositorio de git (GitLab, Bitbucket, auto-hospedado)
* **Rutas locales**: directorios o rutas directas a archivos `marketplace.json`
* **URLs remotas**: URLs directas a archivos `marketplace.json` hospedados

### Agregar desde GitHub

Agregue un repositorio de GitHub que contenga un archivo `.claude-plugin/marketplace.json` usando el formato `owner/repo`—donde `owner` es el nombre de usuario o la organización de GitHub y `repo` es el nombre del repositorio.

Por ejemplo, `anthropics/claude-code` se refiere al repositorio `claude-code` propiedad de `anthropics`:

```shell theme={null}
/plugin marketplace add anthropics/claude-code
```

### Agregar desde otros hosts de Git

Agregue cualquier repositorio de git proporcionando la URL completa. Esto funciona con cualquier host de Git, incluyendo GitLab, Bitbucket y servidores auto-hospedados. Incluya el sufijo `.git` para que Claude Code clone el repositorio en lugar de tratar la URL como un enlace directo a un archivo `marketplace.json` hospedado.

Usando HTTPS:

```shell theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git
```

Usando SSH:

```shell theme={null}
/plugin marketplace add git@gitlab.com:company/plugins.git
```

Para agregar una rama o etiqueta específica, agregue `#` seguido de la ref:

```shell theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git#v1.0.0
```

### Agregar desde rutas locales

Agregue un directorio local que contenga un archivo `.claude-plugin/marketplace.json`:

```shell theme={null}
/plugin marketplace add ./my-marketplace
```

También puede agregar una ruta directa a un archivo `marketplace.json`:

```shell theme={null}
/plugin marketplace add ./path/to/marketplace.json
```

### Agregar desde URLs remotas

Agregue un archivo `marketplace.json` remoto a través de URL:

```shell theme={null}
/plugin marketplace add https://example.com/marketplace.json
```

<Note>
  Los mercados basados en URL tienen algunas limitaciones en comparación con los mercados basados en Git. Si encuentra errores "path not found" al instalar plugins, consulte [Troubleshooting](/es/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces).
</Note>

## Instalar plugins

Una vez que haya agregado mercados, puede instalar plugins directamente (se instala en alcance de usuario por defecto):

```shell theme={null}
/plugin install plugin-name@marketplace-name
```

Para elegir un [alcance de instalación](/es/settings#configuration-scopes) diferente, use la interfaz interactiva: ejecute `/plugin`, vaya a la pestaña **Discover** y presione **Enter** en un plugin. Verá opciones para:

* **User scope** (predeterminado): instale para usted en todos los proyectos
* **Project scope**: instale para todos los colaboradores en este repositorio (agrega a `.claude/settings.json`)
* **Local scope**: instale para usted en este repositorio solamente (no compartido con colaboradores)

También puede ver plugins con alcance **managed**—estos son instalados por administradores a través de [managed settings](/es/settings#settings-files) y no pueden ser modificados.

<Warning>
  Asegúrese de confiar en un plugin antes de instalarlo. Anthropic no controla qué servidores MCP, archivos u otro software se incluyen en los plugins y no puede verificar que funcionen como se pretende. Consulte la página de inicio de cada plugin para obtener más información.
</Warning>

## Administrar plugins instalados

Ejecute `/plugin` y vaya a la pestaña **Installed** para ver, habilitar, deshabilitar o desinstalar sus plugins. La lista se agrupa por alcance y se ordena para que vea problemas primero: los plugins con errores de carga o dependencias no resueltas aparecen en la parte superior, seguidos de sus favoritos, con plugins deshabilitados plegados detrás de un encabezado colapsado en la parte inferior.

Desde la lista puede:

* presionar `f` para marcar como favorito o desmarcar como favorito el plugin seleccionado
* escribir para filtrar por nombre o descripción del plugin
* presionar Enter para abrir la vista de detalles de un plugin y habilitarlo, deshabilitarlo o desinstalarlo

Cuando instala un plugin que declara dependencias, la salida de instalación enumera qué dependencias se instalaron automáticamente junto con él.

También puede administrar plugins con comandos directos.

Deshabilite un plugin sin desinstalarlo:

```shell theme={null}
/plugin disable plugin-name@marketplace-name
```

Vuelva a habilitar un plugin deshabilitado:

```shell theme={null}
/plugin enable plugin-name@marketplace-name
```

Elimine completamente un plugin:

```shell theme={null}
/plugin uninstall plugin-name@marketplace-name
```

La opción `--scope` le permite dirigirse a un alcance específico con comandos CLI:

```shell theme={null}
claude plugin install formatter@your-org --scope project
claude plugin uninstall formatter@your-org --scope project
```

### Aplicar cambios de plugins sin reiniciar

Cuando instala, habilita o deshabilita plugins durante una sesión, ejecute `/reload-plugins` para recopilar todos los cambios sin reiniciar:

```shell theme={null}
/reload-plugins
```

Claude Code recarga todos los plugins activos y muestra conteos para plugins, skills, agentes, hooks, servidores MCP de plugins y servidores LSP de plugins.

## Administrar mercados

Puede administrar mercados a través de la interfaz interactiva `/plugin` o con comandos CLI.

### Usar la interfaz interactiva

Ejecute `/plugin` y vaya a la pestaña **Marketplaces** para:

* Ver todos sus mercados agregados con sus fuentes y estado
* Agregar nuevos mercados
* Actualizar listados de mercados para obtener los últimos plugins
* Eliminar mercados que ya no necesita

### Usar comandos CLI

También puede administrar mercados con comandos directos.

Enumere todos los mercados configurados:

```shell theme={null}
/plugin marketplace list
```

Actualice listados de plugins de un mercado:

```shell theme={null}
/plugin marketplace update marketplace-name
```

Elimine un mercado:

```shell theme={null}
/plugin marketplace remove marketplace-name
```

<Warning>
  Eliminar un mercado desinstalará cualquier plugin que haya instalado desde él.
</Warning>

### Configurar actualizaciones automáticas

Claude Code puede actualizar automáticamente mercados y sus plugins instalados al inicio. Cuando la actualización automática está habilitada para un mercado, Claude Code actualiza los datos del mercado e actualiza los plugins instalados a sus versiones más recientes. Si se actualizaron plugins, verá una notificación pidiéndole que ejecute `/reload-plugins`.

Alterne la actualización automática para mercados individuales a través de la interfaz:

1. Ejecute `/plugin` para abrir el administrador de plugins
2. Seleccione **Marketplaces**
3. Elija un mercado de la lista
4. Seleccione **Enable auto-update** o **Disable auto-update**

Los mercados oficiales de Anthropic tienen la actualización automática habilitada por defecto. Los mercados de terceros y de desarrollo local tienen la actualización automática deshabilitada por defecto.

Los administradores también pueden establecer `"autoUpdate": true` en cada entrada [`extraKnownMarketplaces`](/es/settings#extraknownmarketplaces) en la configuración administrada para habilitar la actualización automática para un mercado de la organización sin requerir que cada usuario la active.

Para deshabilitar todas las actualizaciones automáticas completamente tanto para Claude Code como para todos los plugins, establezca la variable de entorno `DISABLE_AUTOUPDATER`. Consulte [Auto updates](/es/setup#auto-updates) para obtener detalles.

Para mantener las actualizaciones automáticas de plugins habilitadas mientras se deshabilitan las actualizaciones automáticas de Claude Code, establezca `FORCE_AUTOUPDATE_PLUGINS=1` junto con `DISABLE_AUTOUPDATER`:

```bash theme={null}
export DISABLE_AUTOUPDATER=1
export FORCE_AUTOUPDATE_PLUGINS=1
```

Esto es útil cuando desea administrar las actualizaciones de Claude Code manualmente pero aún recibir actualizaciones automáticas de plugins.

## Configurar mercados de equipo

Los administradores de equipo pueden configurar la instalación automática de mercados para proyectos agregando configuración de mercado a `.claude/settings.json`. Cuando los miembros del equipo confían en la carpeta del repositorio, Claude Code les solicita que instalen estos mercados y plugins.

Agregue `extraKnownMarketplaces` a su `.claude/settings.json` del proyecto:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "my-team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

Para opciones de configuración completas incluyendo `extraKnownMarketplaces` y `enabledPlugins`, consulte [Plugin settings](/es/settings#plugin-settings).

## Seguridad

Los plugins y mercados son componentes altamente confiables que pueden ejecutar código arbitrario en su máquina con sus privilegios de usuario. Solo instale plugins y agregue mercados de fuentes en las que confíe. Las organizaciones pueden restringir qué mercados se permite a los usuarios agregar usando [managed marketplace restrictions](/es/plugin-marketplaces#managed-marketplace-restrictions).

## Troubleshooting

### /plugin command not recognized

Si ve "unknown command" o el comando `/plugin` no aparece:

1. **Verifique su versión**: Ejecute `claude --version` para ver qué está instalado.
2. **Actualice Claude Code**:
   * **Homebrew**: `brew upgrade claude-code` (o `brew upgrade claude-code@latest` si instaló ese cask)
   * **npm**: `npm install -g @anthropic-ai/claude-code@latest`
   * **Native installer**: Vuelva a ejecutar el comando de instalación desde [Setup](/es/setup)
3. **Reinicie Claude Code**: Después de actualizar, reinicie su terminal y ejecute `claude` nuevamente.

### Common issues

* **Marketplace not loading**: Verifique que la URL sea accesible y que `.claude-plugin/marketplace.json` exista en la ruta
* **Plugin installation failures**: Verifique que las URLs de fuente de plugins sean accesibles y que los repositorios sean públicos (o tenga acceso)
* **Files not found after installation**: Los plugins se copian a un caché, por lo que las rutas que hacen referencia a archivos fuera del directorio del plugin no funcionarán
* **Plugin skills not appearing**: Limpie el caché con `rm -rf ~/.claude/plugins/cache`, reinicie Claude Code y reinstale el plugin.

Para solución de problemas detallada con soluciones, consulte [Troubleshooting](/es/plugin-marketplaces#troubleshooting) en la guía de mercados. Para herramientas de depuración, consulte [Debugging and development tools](/es/plugins-reference#debugging-and-development-tools).

### Code intelligence issues

* **Language server not starting**: verifique que el binario esté instalado y disponible en su `$PATH`. Consulte la pestaña Errors de `/plugin` para obtener detalles.
* **High memory usage**: los servidores de lenguaje como `rust-analyzer` y `pyright` pueden consumir memoria significativa en proyectos grandes. Si experimenta problemas de memoria, deshabilite el plugin con `/plugin disable <plugin-name>` y confíe en las herramientas de búsqueda integradas de Claude en su lugar.
* **False positive diagnostics in monorepos**: los servidores de lenguaje pueden reportar errores de importación no resuelta para paquetes internos si el espacio de trabajo no está configurado correctamente. Estos no afectan la capacidad de Claude para editar código.

## Next steps

* **Build your own plugins**: Consulte [Plugins](/es/plugins) para crear skills, agentes y hooks
* **Create a marketplace**: Consulte [Create a plugin marketplace](/es/plugin-marketplaces) para distribuir plugins a su equipo o comunidad
* **Technical reference**: Consulte [Plugins reference](/es/plugins-reference) para especificaciones completas
