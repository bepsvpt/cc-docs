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

Claude Code admite varios modos de permisos que controlan cómo se aprueban las herramientas. Consulte [Permission modes](/es/permission-modes) para saber cuándo usar cada uno. Establezca `defaultMode` en sus [archivos de configuración](/es/settings#settings-files):

| Modo                | Descripción                                                                                                                                                                                          |
| :------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `default`           | Comportamiento estándar: solicita permiso en el primer uso de cada herramienta                                                                                                                       |
| `acceptEdits`       | Acepta automáticamente los permisos de edición de archivos para la sesión, excepto escrituras en directorios protegidos                                                                              |
| `plan`              | Plan Mode: Claude puede analizar pero no modificar archivos ni ejecutar comandos                                                                                                                     |
| `auto`              | Auto-aprueba las llamadas de herramientas con comprobaciones de seguridad en segundo plano que verifican que las acciones se alineen con su solicitud. Actualmente una vista previa de investigación |
| `dontAsk`           | Deniega automáticamente las herramientas a menos que estén preaprobadas a través de `/permissions` o reglas `permissions.allow`                                                                      |
| `bypassPermissions` | Omite los avisos de permisos excepto para escrituras en directorios protegidos (ver advertencia a continuación)                                                                                      |

<Warning>
  El modo `bypassPermissions` omite los avisos de permisos. Las escrituras en directorios `.git`, `.claude`, `.vscode`, `.idea` y `.husky` aún solicitan confirmación para evitar la corrupción accidental del estado del repositorio, la configuración del editor y los git hooks. Las escrituras en `.claude/commands`, `.claude/agents` y `.claude/skills` están exentas y no solicitan, porque Claude escribe rutinariamente allí al crear skills, subagents y comandos. Use este modo solo en entornos aislados como contenedores o máquinas virtuales donde Claude Code no pueda causar daño. Los administradores pueden evitar este modo estableciendo `permissions.disableBypassPermissionsMode` en `"disable"` en [configuración administrada](#managed-settings).
</Warning>

Para evitar que se use el modo `bypassPermissions` o `auto`, establezca `permissions.disableBypassPermissionsMode` o `permissions.disableAutoMode` en `"disable"` en cualquier [archivo de configuración](/es/settings#settings-files). Estos son más útiles en [configuración administrada](#managed-settings) donde no pueden ser anulados.

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

```json theme={null}
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

Cuando aprueba un comando compuesto con "Sí, no preguntar de nuevo", Claude Code guarda una regla separada para cada subcomando que requiere aprobación, en lugar de una sola regla para la cadena completa. Por ejemplo, aprobar `git status && npm test` guarda una regla para `npm test`, por lo que futuras invocaciones de `npm test` se reconocen independientemente de lo que preceda a `&&`. Los subcomandos como `cd` en un subdirectorio generan su propia regla Read para esa ruta. Se pueden guardar hasta 5 reglas para un solo comando compuesto.

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

<Warning>
  Las reglas de negación Read y Edit se aplican a las herramientas de archivo integradas de Claude, no a los subprocesos de Bash. Una regla de negación `Read(./.env)` bloquea la herramienta Read pero no previene `cat .env` en Bash. Para aplicación a nivel del SO que bloquea todos los procesos de acceder a una ruta, [habilite el sandbox](/es/sandboxing).
</Warning>

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

En Windows, las rutas se normalizan a forma POSIX antes de coincidir. `C:\Users\alice` se convierte en `/c/Users/alice`, así que use `//c/**/.env` para coincidir con archivos `.env` en cualquier lugar de esa unidad. Para coincidir en todas las unidades, use `//**/.env`.

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

```json theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)"]
  }
}
```

## Extender permisos con hooks

Los [hooks de Claude Code](/es/hooks-guide) proporcionan una forma de registrar comandos de shell personalizados para realizar evaluación de permisos en tiempo de ejecución. Cuando Claude Code realiza una llamada de herramienta, los hooks PreToolUse se ejecutan antes del aviso de permisos. La salida del hook puede denegar la llamada de herramienta, forzar un aviso u omitir el aviso para permitir que la llamada continúe.

Omitir el aviso no omite las reglas de permisos. Las reglas de negación y solicitud aún se evalúan después de que un hook devuelve `"allow"`, por lo que una regla de negación coincidente aún bloquea la llamada. Esto preserva la precedencia de negación primero descrita en [Administrar permisos](#manage-permissions), incluyendo reglas de negación establecidas en configuración administrada.

Un hook de bloqueo también tiene precedencia sobre las reglas de permiso. Un hook que sale con código 2 detiene la llamada de herramienta antes de que se evalúen las reglas de permisos, por lo que el bloqueo se aplica incluso cuando una regla de permiso permitiría que la llamada continúe. Para ejecutar todos los comandos Bash sin avisos excepto algunos que desea bloquear, agregue `"Bash"` a su lista de permiso y registre un hook PreToolUse que rechace esos comandos específicos. Consulte [Bloquear ediciones a archivos protegidos](/es/hooks-guide#block-edits-to-protected-files) para un script de hook que puede adaptar.

## Directorios de trabajo

Por defecto, Claude tiene acceso a archivos en el directorio donde fue lanzado. Puede extender este acceso:

* **Durante el inicio**: use el argumento CLI `--add-dir <path>`
* **Durante la sesión**: use el comando `/add-dir`
* **Configuración persistente**: agregue a `additionalDirectories` en [archivos de configuración](/es/settings#settings-files)

Los archivos en directorios adicionales siguen las mismas reglas de permisos que el directorio de trabajo original: se vuelven legibles sin avisos, y los permisos de edición de archivos siguen el modo de permisos actual.

### Los directorios adicionales otorgan acceso a archivos, no configuración

Agregar un directorio extiende dónde Claude puede leer y editar archivos. No hace que ese directorio sea una raíz de configuración completa: la mayoría de la configuración `.claude/` no se descubre desde directorios adicionales, aunque algunos tipos se cargan como excepciones.

Los siguientes tipos de configuración se cargan desde directorios `--add-dir`:

| Configuración                                       | Cargado desde `--add-dir`                                                     |
| :-------------------------------------------------- | :---------------------------------------------------------------------------- |
| [Skills](/es/skills) en `.claude/skills/`           | Sí, con recarga en vivo                                                       |
| Configuración de plugins en `.claude/settings.json` | Solo `enabledPlugins` y `extraKnownMarketplaces`                              |
| Archivos [CLAUDE.md](/es/memory) y `.claude/rules/` | Solo cuando `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` está establecido |

Todo lo demás, incluyendo subagents, comandos, estilos de salida, hooks y otras configuraciones, se descubre solo desde el directorio de trabajo actual y sus padres, su directorio de usuario en `~/.claude/` y configuración administrada. Para compartir esa configuración entre proyectos, use uno de estos enfoques:

* **Configuración a nivel de usuario**: coloque archivos en `~/.claude/agents/`, `~/.claude/output-styles/` o `~/.claude/settings.json` para hacerlos disponibles en cada proyecto
* **Plugins**: empaquete y distribuya configuración como un [plugin](/es/plugins) que los equipos pueden instalar
* **Lanzar desde el directorio de configuración**: ejecute Claude Code desde el directorio que contiene la configuración `.claude/` que desea

## Cómo interactúan los permisos con el sandboxing

Los permisos y el [sandboxing](/es/sandboxing) son capas de seguridad complementarias:

* **Permisos** controlan qué herramientas puede usar Claude Code y qué archivos o dominios puede acceder. Se aplican a todas las herramientas (Bash, Read, Edit, WebFetch, MCP y otras).
* **Sandboxing** proporciona aplicación a nivel del SO que restringe el acceso del sistema de archivos y red de la herramienta Bash. Se aplica solo a comandos Bash y sus procesos secundarios.

Use ambos para defensa en profundidad:

* Las reglas de negación de permisos bloquean que Claude intente acceder a recursos restringidos
* Las restricciones de sandbox previenen que comandos Bash alcancen recursos fuera de límites definidos, incluso si una inyección de solicitud omite la toma de decisiones de Claude
* Las restricciones del sistema de archivos en el sandbox usan reglas de negación Read y Edit, no configuración de sandbox separada
* Las restricciones de red combinan reglas de permisos WebFetch con la lista `allowedDomains` del sandbox

## Configuración administrada

Para organizaciones que necesitan control centralizado sobre la configuración de Claude Code, los administradores pueden implementar configuración administrada que no puede ser anulada por configuración de usuario o proyecto. Estas configuraciones de política siguen el mismo formato que archivos de configuración regulares y se pueden entregar a través de políticas MDM/a nivel del SO, archivos de configuración administrada o [configuración administrada por servidor](/es/server-managed-settings). Consulte [archivos de configuración](/es/settings#settings-files) para mecanismos de entrega y ubicaciones de archivos.

### Configuración solo administrada

Las siguientes configuraciones solo se leen desde configuración administrada. Colocarlas en archivos de configuración de usuario o proyecto no tiene efecto.

| Configuración                                  | Descripción                                                                                                                                                                                                                                                                                               |
| :--------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowedChannelPlugins`                        | Lista de permitidos de plugins de canal que pueden enviar mensajes. Reemplaza la lista de permitidos predeterminada de Anthropic cuando se establece. Requiere `channelsEnabled: true`. Consulte [Restringir qué plugins de canal pueden ejecutarse](/es/channels#restrict-which-channel-plugins-can-run) |
| `allowManagedHooksOnly`                        | Cuando es `true`, evita la carga de hooks de usuario, proyecto y plugin. Solo se permiten hooks administrados y hooks SDK                                                                                                                                                                                 |
| `allowManagedMcpServersOnly`                   | Cuando es `true`, solo se respetan `allowedMcpServers` de configuración administrada. `deniedMcpServers` aún se fusiona de todas las fuentes. Consulte [Configuración MCP administrada](/es/mcp#managed-mcp-configuration)                                                                                |
| `allowManagedPermissionRulesOnly`              | Cuando es `true`, evita que la configuración de usuario y proyecto defina reglas de permisos `allow`, `ask` o `deny`. Solo se aplican las reglas en configuración administrada                                                                                                                            |
| `blockedMarketplaces`                          | Lista de bloqueo de fuentes de marketplace. Las fuentes bloqueadas se verifican antes de descargar, por lo que nunca tocan el sistema de archivos. Consulte [restricciones de marketplace administradas](/es/plugin-marketplaces#managed-marketplace-restrictions)                                        |
| `channelsEnabled`                              | Permitir [channels](/es/channels) para usuarios de Team y Enterprise. Sin establecer o `false` bloquea la entrega de mensajes de canal independientemente de lo que los usuarios pasen a `--channels`                                                                                                     |
| `pluginTrustMessage`                           | Mensaje personalizado agregado a la advertencia de confianza de plugin mostrada antes de la instalación                                                                                                                                                                                                   |
| `sandbox.filesystem.allowManagedReadPathsOnly` | Cuando es `true`, solo se respetan rutas `filesystem.allowRead` de configuración administrada. `denyRead` aún se fusiona de todas las fuentes                                                                                                                                                             |
| `sandbox.network.allowManagedDomainsOnly`      | Cuando es `true`, solo se respetan `allowedDomains` y reglas de permiso `WebFetch(domain:...)` de configuración administrada. Los dominios no permitidos se bloquean automáticamente sin solicitar al usuario. Los dominios denegados aún se fusionan de todas las fuentes                                |
| `strictKnownMarketplaces`                      | Controla qué marketplaces de plugins pueden agregar los usuarios. Consulte [restricciones de marketplace administradas](/es/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                         |

`disableBypassPermissionsMode` generalmente se coloca en configuración administrada para aplicar la política organizacional, pero funciona desde cualquier alcance. Un usuario puede establecerlo en su propia configuración para bloquearse a sí mismo del modo de bypass.

<Note>
  El acceso a [Remote Control](/es/remote-control) y [sesiones web](/es/claude-code-on-the-web) no se controla mediante una clave de configuración administrada. En planes Team y Enterprise, un administrador habilita o deshabilita estas características en [configuración de administrador de Claude Code](https://claude.ai/admin-settings/claude-code).
</Note>

## Revisar denegaciones del modo auto

Cuando el [modo auto](/es/permission-modes#eliminate-prompts-with-auto-mode) deniega una llamada de herramienta, aparece una notificación y la acción denegada se registra en `/permissions` bajo la pestaña Recently denied. Presione `r` en una acción denegada para marcarla para reintentar: cuando salga del diálogo, Claude Code envía un mensaje indicando al modelo que puede reintentar esa llamada de herramienta y reanuda la conversación.

Para reaccionar a denegaciones programáticamente, use el [hook `PermissionDenied`](/es/hooks#permissiondenied).

## Configurar el clasificador del modo auto

El [modo auto](/es/permission-modes#eliminate-prompts-with-auto-mode) utiliza un modelo clasificador para decidir si cada acción es segura de ejecutar sin solicitar. De fábrica, solo confía en el directorio de trabajo y, si está presente, los remotos del repositorio actual. Acciones como empujar a la organización de control de fuente de su empresa o escribir en un bucket de nube de equipo serán bloqueadas como posible exfiltración de datos. El bloque de configuración `autoMode` le permite decirle al clasificador qué infraestructura confía su organización.

El clasificador lee `autoMode` de configuración de usuario, `.claude/settings.local.json` y configuración administrada. No lee de configuración de proyecto compartida en `.claude/settings.json`, porque un repositorio registrado podría inyectar sus propias reglas de permiso.

| Alcance                       | Archivo                       | Usar para                                                         |
| :---------------------------- | :---------------------------- | :---------------------------------------------------------------- |
| Un desarrollador              | `~/.claude/settings.json`     | Infraestructura confiable personal                                |
| Un proyecto, un desarrollador | `.claude/settings.local.json` | Buckets o servicios confiables por proyecto, gitignored           |
| Organización completa         | Configuración administrada    | Infraestructura confiable aplicada para todos los desarrolladores |

Las entradas de cada alcance se combinan. Un desarrollador puede extender `environment`, `allow` y `soft_deny` con entradas personales pero no puede eliminar entradas que proporciona la configuración administrada. Porque las reglas de permiso actúan como excepciones a las reglas de bloqueo dentro del clasificador, una entrada `allow` agregada por desarrollador puede anular una entrada `soft_deny` de organización: la combinación es aditiva, no un límite de política duro. Si necesita una regla que los desarrolladores no puedan eludir, use `permissions.deny` en configuración administrada en su lugar, que bloquea acciones antes de que se consulte el clasificador.

### Definir infraestructura confiable

Para la mayoría de las organizaciones, `autoMode.environment` es el único campo que necesita establecer. Le dice al clasificador qué repositorios, buckets y dominios son confiables, sin tocar las reglas de bloqueo y permiso integradas. El clasificador usa `environment` para decidir qué significa "externo": cualquier destino no listado es un objetivo potencial de exfiltración.

```json theme={null}
{
  "autoMode": {
    "environment": [
      "Source control: github.example.com/acme-corp and all repos under it",
      "Trusted cloud buckets: s3://acme-build-artifacts, gs://acme-ml-datasets",
      "Trusted internal domains: *.corp.example.com, api.internal.example.com",
      "Key internal services: Jenkins at ci.example.com, Artifactory at artifacts.example.com"
    ]
  }
}
```

Las entradas son prosa, no regex o patrones de herramienta. El clasificador las lee como reglas de lenguaje natural. Escríbalas de la manera que describiría su infraestructura a un ingeniero nuevo. Una sección de entorno exhaustiva cubre:

* **Organización**: el nombre de su empresa y para qué se usa principalmente Claude Code, como desarrollo de software, automatización de infraestructura o ingeniería de datos
* **Control de fuente**: cada organización de GitHub, GitLab o Bitbucket a la que sus desarrolladores empujan
* **Proveedores de nube y buckets confiables**: nombres de buckets o prefijos a los que Claude debería poder leer y escribir
* **Dominios internos confiables**: nombres de host para APIs, paneles y servicios dentro de su red, como `*.internal.example.com`
* **Servicios internos clave**: CI, registros de artefactos, índices de paquetes internos, herramientas de incidentes
* **Contexto adicional**: restricciones de industria regulada, infraestructura multiinquilino o requisitos de cumplimiento que afecten lo que el clasificador debería tratar como riesgoso

Una plantilla de inicio útil: complete los campos entre corchetes y elimine cualquier línea que no se aplique:

```json theme={null}
{
  "autoMode": {
    "environment": [
      "Organization: {COMPANY_NAME}. Primary use: {PRIMARY_USE_CASE, e.g. software development, infrastructure automation}",
      "Source control: {SOURCE_CONTROL, e.g. GitHub org github.example.com/acme-corp}",
      "Cloud provider(s): {CLOUD_PROVIDERS, e.g. AWS, GCP, Azure}",
      "Trusted cloud buckets: {TRUSTED_BUCKETS, e.g. s3://acme-builds, gs://acme-datasets}",
      "Trusted internal domains: {TRUSTED_DOMAINS, e.g. *.internal.example.com, api.example.com}",
      "Key internal services: {SERVICES, e.g. Jenkins at ci.example.com, Artifactory at artifacts.example.com}",
      "Additional context: {EXTRA, e.g. regulated industry, multi-tenant infrastructure, compliance requirements}"
    ]
  }
}
```

Cuanto más contexto específico proporcione, mejor el clasificador puede distinguir operaciones internas rutinarias de intentos de exfiltración.

No necesita completar todo a la vez. Un despliegue razonable: comience con los valores predeterminados y agregue su organización de control de fuente y servicios internos clave, que resuelve los falsos positivos más comunes como empujar a sus propios repositorios. Agregue dominios confiables y buckets de nube a continuación. Complete el resto a medida que surjan bloqueos.

### Anular las reglas de bloqueo y permiso

Dos campos adicionales le permiten reemplazar las listas de reglas integradas del clasificador: `autoMode.soft_deny` controla qué se bloquea, y `autoMode.allow` controla qué excepciones se aplican. Cada uno es una matriz de descripciones en prosa, leídas como reglas de lenguaje natural.

Dentro del clasificador, la precedencia es: las reglas `soft_deny` bloquean primero, luego las reglas `allow` anulan como excepciones, luego la intención explícita del usuario anula ambas. Si el mensaje del usuario describe directa y específicamente la acción exacta que Claude está a punto de tomar, el clasificador la permite incluso si una regla `soft_deny` coincide. Las solicitudes generales no cuentan: pedir a Claude que "limpie el repositorio" no autoriza un force-push, pero pedir a Claude que "force-push esta rama" sí.

Para aflojar: elimine reglas de `soft_deny` cuando los valores predeterminados bloquean algo que su pipeline ya protege con revisión de PR, CI o entornos de ensayo, o agregue a `allow` cuando el clasificador marca repetidamente un patrón rutinario que las excepciones predeterminadas no cubren. Para apretar: agregue a `soft_deny` para riesgos específicos de su entorno que los valores predeterminados pierden, o elimine de `allow` para mantener una excepción predeterminada a las reglas de bloqueo. En todos los casos, ejecute `claude auto-mode defaults` para obtener las listas predeterminadas completas, luego copie y edite: nunca comience desde una lista vacía.

```json theme={null}
{
  "autoMode": {
    "environment": [
      "Source control: github.example.com/acme-corp and all repos under it"
    ],
    "allow": [
      "Deploying to the staging namespace is allowed: staging is isolated from production and resets nightly",
      "Writing to s3://acme-scratch/ is allowed: ephemeral bucket with a 7-day lifecycle policy"
    ],
    "soft_deny": [
      "Never run database migrations outside the migrations CLI, even against dev databases",
      "Never modify files under infra/terraform/prod/: production infrastructure changes go through the review workflow",
      "...copy full default soft_deny list here first, then add your rules..."
    ]
  }
}
```

<Danger>
  Establecer `allow` o `soft_deny` reemplaza la lista predeterminada completa para esa sección. Si establece `soft_deny` con una sola entrada, cada regla de bloqueo integrada se descarta: force push, exfiltración de datos, `curl | bash`, despliegues de producción y todas las otras reglas de bloqueo predeterminadas se permiten. Para personalizar de forma segura, ejecute `claude auto-mode defaults` para imprimir las reglas integradas, cópielas en su archivo de configuración, luego revise cada regla contra su propio pipeline y tolerancia de riesgo. Solo elimine reglas para riesgos que su infraestructura ya mitiga.
</Danger>

Las tres secciones se evalúan independientemente, por lo que establecer `environment` solo deja intactas las listas predeterminadas `allow` y `soft_deny`.

### Inspeccionar los valores predeterminados y su configuración efectiva

Porque establecer `allow` o `soft_deny` reemplaza los valores predeterminados, comience cualquier personalización copiando las listas predeterminadas completas. Tres subcomandos CLI lo ayudan a inspeccionar y validar:

```bash theme={null}
claude auto-mode defaults  # the built-in environment, allow, and soft_deny rules
claude auto-mode config    # what the classifier actually uses: your settings where set, defaults otherwise
claude auto-mode critique  # get AI feedback on your custom allow and soft_deny rules
```

Guarde la salida de `claude auto-mode defaults` en un archivo, edite las listas para que coincidan con su política y pegue el resultado en su archivo de configuración. Después de guardar, ejecute `claude auto-mode config` para confirmar que las reglas efectivas son lo que espera. Si ha escrito reglas personalizadas, `claude auto-mode critique` las revisa y marca entradas que son ambiguas, redundantes o probables de causar falsos positivos.

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

* [Settings](/es/settings): referencia de configuración completa incluyendo la tabla de configuración de permisos
* [Sandboxing](/es/sandboxing): aislamiento del sistema de archivos y red a nivel del SO para comandos Bash
* [Authentication](/es/authentication): configure el acceso de usuario a Claude Code
* [Security](/es/security): salvaguardas de seguridad y mejores prácticas
* [Hooks](/es/hooks-guide): automatice flujos de trabajo y extienda la evaluación de permisos
