> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configurar permisos

> Controle lo que Claude Code puede acceder y hacer con reglas de permisos granulares, modos y políticas administradas.

Claude Code admite permisos granulares para que pueda especificar exactamente qué puede hacer el agente y qué no puede hacer. La configuración de permisos se puede registrar en el control de versiones y distribuir a todos los desarrolladores de su organización, así como personalizarse por desarrolladores individuales.

## Sistema de permisos

Claude Code utiliza un sistema de permisos escalonado para equilibrar potencia y seguridad:

| Tipo de herramienta      | Ejemplo                    | Se requiere aprobación | Comportamiento de "Sí, no preguntar de nuevo"        |
| :----------------------- | :------------------------- | :--------------------- | :--------------------------------------------------- |
| Solo lectura             | Lecturas de archivos, Grep | No                     | N/A                                                  |
| Comandos Bash            | Ejecución de shell         | Sí                     | Permanentemente por directorio de proyecto y comando |
| Modificación de archivos | Editar/escribir archivos   | Sí                     | Hasta el final de la sesión                          |

## Administrar permisos

Puede ver y administrar los permisos de herramientas de Claude Code con `/permissions`. Esta interfaz de usuario enumera todas las reglas de permisos y el archivo settings.json del que se obtienen.

* Las reglas **Allow** permiten que Claude Code use la herramienta especificada sin aprobación manual.
* Las reglas **Ask** solicitan confirmación cada vez que Claude Code intenta usar la herramienta especificada.
* Las reglas **Deny** impiden que Claude Code use la herramienta especificada.

Las reglas se evalúan en orden: **deny -> ask -> allow**. La primera regla coincidente gana, por lo que las reglas de negación siempre tienen prioridad.

## Modos de permisos

Claude Code admite varios modos de permisos que controlan cómo se aprueban las herramientas. Establezca `defaultMode` en sus [archivos de configuración](/es/settings#settings-files):

| Modo                | Descripción                                                                                                                     |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------ |
| `default`           | Comportamiento estándar: solicita permiso en el primer uso de cada herramienta                                                  |
| `acceptEdits`       | Acepta automáticamente los permisos de edición de archivos para la sesión                                                       |
| `plan`              | Plan Mode: Claude puede analizar pero no modificar archivos ni ejecutar comandos                                                |
| `dontAsk`           | Deniega automáticamente las herramientas a menos que estén preaprobadas a través de `/permissions` o reglas `permissions.allow` |
| `bypassPermissions` | Omite todos los avisos de permisos (requiere entorno seguro, ver advertencia a continuación)                                    |

<Warning>
  El modo `bypassPermissions` desactiva todas las comprobaciones de permisos. Use esto solo en entornos aislados como contenedores o máquinas virtuales donde Claude Code no pueda causar daño. Los administradores pueden evitar este modo estableciendo `disableBypassPermissionsMode` en `"disable"` en [configuración administrada](#managed-settings).
</Warning>

## Sintaxis de reglas de permisos

Las reglas de permisos siguen el formato `Tool` o `Tool(specifier)`.

### Coincidir con todos los usos de una herramienta

Para coincidir con todos los usos de una herramienta, use solo el nombre de la herramienta sin paréntesis:

| Regla      | Efecto                                              |
| :--------- | :-------------------------------------------------- |
| `Bash`     | Coincide con todos los comandos Bash                |
| `WebFetch` | Coincide con todas las solicitudes de obtención web |
| `Read`     | Coincide con todas las lecturas de archivos         |

`Bash(*)` es equivalente a `Bash` y coincide con todos los comandos Bash.

### Usar especificadores para control granular

Agregue un especificador entre paréntesis para coincidir con usos específicos de herramientas:

| Regla                          | Efecto                                                             |
| :----------------------------- | :----------------------------------------------------------------- |
| `Bash(npm run build)`          | Coincide con el comando exacto `npm run build`                     |
| `Read(./.env)`                 | Coincide con la lectura del archivo `.env` en el directorio actual |
| `WebFetch(domain:example.com)` | Coincide con solicitudes de obtención a example.com                |

### Patrones de comodín

Las reglas de Bash admiten patrones glob con `*`. Los comodines pueden aparecer en cualquier posición del comando. Esta configuración permite comandos npm y git commit mientras bloquea git push:

```json  theme={null}
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git commit *)",
      "Bash(git * main)",
      "Bash(* --version)",
      "Bash(* --help *)"
    ],
    "deny": [
      "Bash(git push *)"
    ]
  }
}
```

El espacio antes de `*` importa: `Bash(ls *)` coincide con `ls -la` pero no con `lsof`, mientras que `Bash(ls*)` coincide con ambos. La sintaxis de sufijo heredada `:*` es equivalente a ` *` pero está deprecada.

## Reglas de permisos específicas de herramientas

### Bash

Las reglas de permisos de Bash admiten coincidencia de comodines con `*`. Los comodines pueden aparecer en cualquier posición del comando, incluyendo al principio, en el medio o al final:

* `Bash(npm run build)` coincide con el comando Bash exacto `npm run build`
* `Bash(npm run test *)` coincide con comandos Bash que comienzan con `npm run test`
* `Bash(npm *)` coincide con cualquier comando que comience con `npm `
* `Bash(* install)` coincide con cualquier comando que termine con ` install`
* `Bash(git * main)` coincide con comandos como `git checkout main`, `git merge main`

Cuando `*` aparece al final con un espacio antes (como `Bash(ls *)`), aplica un límite de palabra, requiriendo que el prefijo sea seguido por un espacio o fin de cadena. Por ejemplo, `Bash(ls *)` coincide con `ls -la` pero no con `lsof`. En contraste, `Bash(ls*)` sin espacio coincide con ambos `ls -la` y `lsof` porque no hay restricción de límite de palabra.

<Tip>
  Claude Code es consciente de los operadores de shell (como `&&`) por lo que una regla de coincidencia de prefijo como `Bash(safe-cmd *)` no le dará permiso para ejecutar el comando `safe-cmd && other-cmd`.
</Tip>

<Warning>
  Los patrones de permisos de Bash que intentan restringir argumentos de comando son frágiles. Por ejemplo, `Bash(curl http://github.com/ *)` intenta restringir curl a URLs de GitHub, pero no coincidirá con variaciones como:

  * Opciones antes de URL: `curl -X GET http://github.com/...`
  * Protocolo diferente: `curl https://github.com/...`
  * Redirecciones: `curl -L http://bit.ly/xyz` (redirige a github)
  * Variables: `URL=http://github.com && curl $URL`
  * Espacios adicionales: `curl  http://github.com`

  Para un filtrado de URL más confiable, considere:

  * **Restringir herramientas de red de Bash**: use reglas de negación para bloquear `curl`, `wget` y comandos similares, luego use la herramienta WebFetch con permiso `WebFetch(domain:github.com)` para dominios permitidos
  * **Usar hooks PreToolUse**: implemente un hook que valide URLs en comandos Bash y bloquee dominios no permitidos
  * Instruir a Claude Code sobre sus patrones curl permitidos a través de CLAUDE.md

  Tenga en cuenta que usar WebFetch solo no previene el acceso a la red. Si se permite Bash, Claude aún puede usar `curl`, `wget` u otras herramientas para alcanzar cualquier URL.
</Warning>

### Read y Edit

Las reglas `Edit` se aplican a todas las herramientas integradas que editan archivos. Claude hace un esfuerzo de mejor intento para aplicar reglas `Read` a todas las herramientas integradas que leen archivos como Grep y Glob.

Las reglas Read y Edit siguen la especificación [gitignore](https://git-scm.com/docs/gitignore) con cuatro tipos de patrones distintos:

| Patrón            | Significado                                             | Ejemplo                          | Coincide                       |
| ----------------- | ------------------------------------------------------- | -------------------------------- | ------------------------------ |
| `//path`          | Ruta **absoluta** desde la raíz del sistema de archivos | `Read(//Users/alice/secrets/**)` | `/Users/alice/secrets/**`      |
| `~/path`          | Ruta desde el directorio **home**                       | `Read(~/Documents/*.pdf)`        | `/Users/alice/Documents/*.pdf` |
| `/path`           | Ruta **relativa a la raíz del proyecto**                | `Edit(/src/**/*.ts)`             | `<project root>/src/**/*.ts`   |
| `path` o `./path` | Ruta **relativa al directorio actual**                  | `Read(*.env)`                    | `<cwd>/*.env`                  |

<Warning>
  Un patrón como `/Users/alice/file` NO es una ruta absoluta. Es relativa a la raíz del proyecto. Use `//Users/alice/file` para rutas absolutas.
</Warning>

Ejemplos:

* `Edit(/docs/**)`: edita en `<project>/docs/` (NO `/docs/` y NO `<project>/.claude/docs/`)
* `Read(~/.zshrc)`: lee el `.zshrc` de su directorio home
* `Edit(//tmp/scratch.txt)`: edita la ruta absoluta `/tmp/scratch.txt`
* `Read(src/**)`: lee desde `<current-directory>/src/`

<Note>
  En patrones gitignore, `*` coincide con archivos en un solo directorio mientras que `**` coincide recursivamente en directorios. Para permitir todo acceso a archivos, use solo el nombre de la herramienta sin paréntesis: `Read`, `Edit` o `Write`.
</Note>

### WebFetch

* `WebFetch(domain:example.com)` coincide con solicitudes de obtención a example.com

### MCP

* `mcp__puppeteer` coincide con cualquier herramienta proporcionada por el servidor `puppeteer` (nombre configurado en Claude Code)
* `mcp__puppeteer__*` sintaxis de comodín que también coincide con todas las herramientas del servidor `puppeteer`
* `mcp__puppeteer__puppeteer_navigate` coincide con la herramienta `puppeteer_navigate` proporcionada por el servidor `puppeteer`

### Agent (subagents)

Use reglas `Agent(AgentName)` para controlar qué [subagents](/es/sub-agents) puede usar Claude:

* `Agent(Explore)` coincide con el subagent Explore
* `Agent(Plan)` coincide con el subagent Plan
* `Agent(my-custom-agent)` coincide con un subagent personalizado llamado `my-custom-agent`

Agregue estas reglas a la matriz `deny` en su configuración o use la bandera CLI `--disallowedTools` para deshabilitar agentes específicos. Para deshabilitar el agente Explore:

```json  theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)"]
  }
}
```

## Extender permisos con hooks

Los [hooks de Claude Code](/es/hooks-guide) proporcionan una forma de registrar comandos de shell personalizados para realizar evaluación de permisos en tiempo de ejecución. Cuando Claude Code realiza una llamada de herramienta, los hooks PreToolUse se ejecutan antes del sistema de permisos, y la salida del hook puede determinar si aprobar o denegar la llamada de herramienta en lugar del sistema de permisos.

## Directorios de trabajo

Por defecto, Claude tiene acceso a archivos en el directorio donde fue lanzado. Puede extender este acceso:

* **Durante el inicio**: use el argumento CLI `--add-dir <path>`
* **Durante la sesión**: use el comando `/add-dir`
* **Configuración persistente**: agregue a `additionalDirectories` en [archivos de configuración](/es/settings#settings-files)

Los archivos en directorios adicionales siguen las mismas reglas de permisos que el directorio de trabajo original: se vuelven legibles sin avisos, y los permisos de edición de archivos siguen el modo de permisos actual.

## Cómo interactúan los permisos con el sandboxing

Los permisos y el [sandboxing](/es/sandboxing) son capas de seguridad complementarias:

* **Permisos** controlan qué herramientas puede usar Claude Code y qué archivos o dominios puede acceder. Se aplican a todas las herramientas (Bash, Read, Edit, WebFetch, MCP y otras).
* **Sandboxing** proporciona aplicación a nivel del SO que restringe el acceso del sistema de archivos y red de la herramienta Bash. Se aplica solo a comandos Bash y sus procesos secundarios.

Use ambos para defensa en profundidad:

* Las reglas de negación de permisos impiden que Claude intente acceder a recursos restringidos
* Las restricciones de sandbox previenen que comandos Bash alcancen recursos fuera de límites definidos, incluso si una inyección de solicitud omite la toma de decisiones de Claude
* Las restricciones del sistema de archivos en el sandbox usan reglas de negación Read y Edit, no configuración de sandbox separada
* Las restricciones de red combinan reglas de permisos WebFetch con la lista `allowedDomains` del sandbox

## Configuración administrada

Para organizaciones que necesitan control centralizado sobre la configuración de Claude Code, los administradores pueden implementar configuración administrada que no puede ser anulada por configuración de usuario o proyecto. Estas configuraciones de política siguen el mismo formato que archivos de configuración regulares y se pueden entregar a través de políticas MDM/a nivel del SO, archivos de configuración administrada o [configuración administrada por servidor](/es/server-managed-settings). Consulte [archivos de configuración](/es/settings#settings-files) para mecanismos de entrega y ubicaciones de archivos.

### Configuración solo administrada

Algunas configuraciones solo son efectivas en configuración administrada:

| Configuración                             | Descripción                                                                                                                                                                                                                                                                |
| :---------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `disableBypassPermissionsMode`            | Establezca en `"disable"` para evitar el modo `bypassPermissions` y la bandera `--dangerously-skip-permissions`                                                                                                                                                            |
| `allowManagedPermissionRulesOnly`         | Cuando es `true`, evita que la configuración de usuario y proyecto defina reglas de permisos `allow`, `ask` o `deny`. Solo se aplican las reglas en configuración administrada                                                                                             |
| `allowManagedHooksOnly`                   | Cuando es `true`, evita la carga de hooks de usuario, proyecto y plugin. Solo se permiten hooks administrados y hooks SDK                                                                                                                                                  |
| `allowManagedMcpServersOnly`              | Cuando es `true`, solo se respetan `allowedMcpServers` de configuración administrada. `deniedMcpServers` aún se fusiona de todas las fuentes. Consulte [Configuración MCP administrada](/es/mcp#managed-mcp-configuration)                                                 |
| `blockedMarketplaces`                     | Lista de bloqueo de fuentes de marketplace. Las fuentes bloqueadas se verifican antes de descargar, por lo que nunca tocan el sistema de archivos. Consulte [restricciones de marketplace administradas](/es/plugin-marketplaces#managed-marketplace-restrictions)         |
| `sandbox.network.allowManagedDomainsOnly` | Cuando es `true`, solo se respetan `allowedDomains` y reglas de permiso `WebFetch(domain:...)` de configuración administrada. Los dominios no permitidos se bloquean automáticamente sin solicitar al usuario. Los dominios denegados aún se fusionan de todas las fuentes |
| `strictKnownMarketplaces`                 | Controla qué marketplaces de plugins pueden agregar los usuarios. Consulte [restricciones de marketplace administradas](/es/plugin-marketplaces#managed-marketplace-restrictions)                                                                                          |
| `allow_remote_sessions`                   | Cuando es `true`, permite a los usuarios iniciar [Control Remoto](/es/remote-control) y [sesiones web](/es/claude-code-on-the-web). Por defecto es `true`. Establezca en `false` para evitar acceso a sesiones remotas                                                     |

## Precedencia de configuración

Las reglas de permisos siguen la misma [precedencia de configuración](/es/settings#settings-precedence) que todas las demás configuraciones de Claude Code:

1. **Configuración administrada**: no puede ser anulada por ningún otro nivel, incluyendo argumentos de línea de comandos
2. **Argumentos de línea de comandos**: anulaciones de sesión temporal
3. **Configuración de proyecto local** (`.claude/settings.local.json`)
4. **Configuración de proyecto compartida** (`.claude/settings.json`)
5. **Configuración de usuario** (`~/.claude/settings.json`)

Si una herramienta se deniega en cualquier nivel, ningún otro nivel puede permitirla. Por ejemplo, una negación de configuración administrada no puede ser anulada por `--allowedTools`, y `--disallowedTools` puede agregar restricciones más allá de lo que define la configuración administrada.

Si un permiso se permite en configuración de usuario pero se deniega en configuración de proyecto, la configuración de proyecto tiene prioridad y el permiso se bloquea.

## Configuraciones de ejemplo

Este [repositorio](https://github.com/anthropics/claude-code/tree/main/examples/settings) incluye configuraciones de configuración inicial para escenarios de implementación comunes. Use estos como puntos de partida y ajústelos para que se adapten a sus necesidades.

## Ver también

* [Configuración](/es/settings): referencia de configuración completa incluyendo la tabla de configuración de permisos
* [Sandboxing](/es/sandboxing): aislamiento del sistema de archivos y red a nivel del SO para comandos Bash
* [Autenticación](/es/authentication): configure el acceso de usuario a Claude Code
* [Seguridad](/es/security): salvaguardas de seguridad y mejores prácticas
* [Hooks](/es/hooks-guide): automatice flujos de trabajo y extienda la evaluación de permisos
