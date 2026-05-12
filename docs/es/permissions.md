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

<Note>
  Las reglas de permisos se aplican mediante Claude Code, no por el modelo. Las instrucciones en su prompt o `CLAUDE.md` determinan lo que Claude intenta hacer, pero no cambian lo que Claude Code permite. Para otorgar o revocar acceso, use `/permissions`, las reglas descritas aquí, un [modo de permisos](/es/permission-modes), o un [hook PreToolUse](#extend-permissions-with-hooks).
</Note>

## Modos de permisos

Claude Code admite varios modos de permisos que controlan cómo se aprueban las herramientas. Consulte [Permission modes](/es/permission-modes) para saber cuándo usar cada uno. Establezca `defaultMode` en sus [archivos de configuración](/es/settings#settings-files):

| Modo                | Descripción                                                                                                                                                                                      |
| :------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `default`           | Comportamiento estándar: solicita permiso en el primer uso de cada herramienta                                                                                                                   |
| `acceptEdits`       | Acepta automáticamente ediciones de archivos y comandos comunes del sistema de archivos (`mkdir`, `touch`, `mv`, `cp`, etc.) para rutas en el directorio de trabajo o `additionalDirectories`    |
| `plan`              | Plan Mode: Claude lee archivos y ejecuta comandos de shell de solo lectura para explorar pero no edita sus archivos de origen                                                                    |
| `auto`              | Auto-aprueba llamadas de herramientas con comprobaciones de seguridad en segundo plano que verifican que las acciones se alineen con su solicitud. Actualmente una vista previa de investigación |
| `dontAsk`           | Deniega automáticamente las herramientas a menos que estén preaprobadas a través de `/permissions` o reglas `permissions.allow`                                                                  |
| `bypassPermissions` | Omite todos los avisos de permisos. Las eliminaciones de directorio raíz y directorio de inicio como `rm -rf /` aún solicitan como un disyuntor de circuito                                      |

<Warning>
  El modo `bypassPermissions` omite todos los avisos de permisos, incluyendo escrituras en `.git`, `.claude`, `.vscode`, `.idea` y `.husky`. Las eliminaciones dirigidas al directorio raíz del sistema de archivos o al directorio de inicio, como `rm -rf /` y `rm -rf ~`, aún solicitan como un disyuntor de circuito contra errores del modelo. Use este modo solo en entornos aislados como contenedores o máquinas virtuales donde Claude Code no pueda causar daño. Los administradores pueden evitar este modo estableciendo `permissions.disableBypassPermissionsMode` en `"disable"` en [configuración administrada](#managed-settings).
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

El espacio antes de `*` importa: `Bash(ls *)` coincide con `ls -la` pero no con `lsof`, mientras que `Bash(ls*)` coincide con ambos. El sufijo `:*` es una forma equivalente de escribir un comodín final, por lo que `Bash(ls:*)` coincide con los mismos comandos que `Bash(ls *)`.

El diálogo de permisos escribe la forma separada por espacios cuando selecciona "Sí, no preguntar de nuevo" para un prefijo de comando. La forma `:*` solo se reconoce al final de un patrón. En un patrón como `Bash(git:* push)`, el dos puntos se trata como un carácter literal y no coincidirá con comandos git.

## Reglas de permisos específicas de herramientas

### Bash

Las reglas de permisos de Bash admiten coincidencia de comodines con `*`. Los comodines pueden aparecer en cualquier posición del comando, incluyendo al principio, en el medio o al final:

* `Bash(npm run build)` coincide con el comando Bash exacto `npm run build`
* `Bash(npm run test *)` coincide con comandos Bash que comienzan con `npm run test`
* `Bash(npm *)` coincide con cualquier comando que comience con `npm `
* `Bash(* install)` coincide con cualquier comando que termine con ` install`
* `Bash(git * main)` coincide con comandos como `git checkout main` y `git log --oneline main`

Un único `*` coincide con cualquier secuencia de caracteres incluyendo espacios, por lo que un comodín puede abarcar múltiples argumentos. `Bash(git *)` coincide con `git log --oneline --all`, y `Bash(git * main)` coincide con `git push origin main` así como con `git merge main`.

Cuando `*` aparece al final con un espacio antes (como `Bash(ls *)`), aplica un límite de palabra, requiriendo que el prefijo sea seguido por un espacio o fin de cadena. Por ejemplo, `Bash(ls *)` coincide con `ls -la` pero no con `lsof`. En contraste, `Bash(ls*)` sin espacio coincide con ambos `ls -la` y `lsof` porque no hay restricción de límite de palabra.

#### Comandos compuestos

<Tip>
  Claude Code es consciente de los operadores de shell, por lo que una regla como `Bash(safe-cmd *)` no le dará permiso para ejecutar el comando `safe-cmd && other-cmd`. Los separadores de comando reconocidos son `&&`, `||`, `;`, `|`, `|&`, `&` y saltos de línea. Una regla debe coincidir con cada subcomando de forma independiente.
</Tip>

Cuando aprueba un comando compuesto con "Sí, no preguntar de nuevo", Claude Code guarda una regla separada para cada subcomando que requiere aprobación, en lugar de una sola regla para la cadena completa. Por ejemplo, aprobar `git status && npm test` guarda una regla para `npm test`, por lo que futuras invocaciones de `npm test` se reconocen independientemente de lo que preceda a `&&`. Los subcomandos como `cd` en un subdirectorio generan su propia regla Read para esa ruta. Se pueden guardar hasta 5 reglas para un solo comando compuesto.

#### Envoltorios de procesos

Antes de coincidir con reglas de Bash, Claude Code elimina un conjunto fijo de envoltorios de procesos para que una regla como `Bash(npm test *)` también coincida con `timeout 30 npm test`. Los envoltorios reconocidos son `timeout`, `time`, `nice`, `nohup` y `stdbuf`.

`xargs` desnudo también se elimina, por lo que `Bash(grep *)` coincide con `xargs grep pattern`. La eliminación solo se aplica cuando `xargs` no tiene banderas: una invocación como `xargs -n1 grep pattern` se coincide como un comando `xargs`, por lo que las reglas escritas para el comando interno no la cubren.

Esta lista de envoltorios está integrada y no es configurable. Los ejecutores de entorno de desarrollo como `direnv exec`, `devbox run`, `mise exec`, `npx` y `docker exec` no están en la lista. Porque estas herramientas ejecutan sus argumentos como un comando, una regla como `Bash(devbox run *)` coincide con lo que viene después de `run`, incluyendo `devbox run rm -rf .`. Para aprobar trabajo dentro de un ejecutor de entorno, escriba una regla específica que incluya tanto el ejecutor como el comando interno, como `Bash(devbox run npm test)`. Agregue una regla por comando interno que desee permitir.

Los envoltorios exec como `watch`, `setsid`, `ionice` y `flock` siempre solicitan y no pueden ser auto-aprobados por una regla de prefijo como `Bash(watch *)`. Lo mismo se aplica a `find` con `-exec` o `-delete`: una regla `Bash(find *)` no cubre estas formas. Para aprobar una invocación específica, escriba una regla de coincidencia exacta para la cadena de comando completa.

#### Comandos de solo lectura

Claude Code reconoce un conjunto integrado de comandos Bash como de solo lectura y los ejecuta sin un aviso de permisos en cada modo. Estos incluyen `ls`, `cat`, `head`, `tail`, `grep`, `find`, `wc`, `diff`, `stat`, `du`, `cd` y formas de solo lectura de `git`. El conjunto no es configurable; para requerir un aviso para uno de estos comandos, agregue una regla `ask` o `deny` para él.

Los patrones glob sin comillas se permiten para comandos cuya cada bandera es de solo lectura, por lo que `ls *.ts` y `wc -l src/*.py` se ejecutan sin un aviso. Los comandos con banderas capaces de escritura o ejecución, como `find`, `sort`, `sed` y `git`, aún solicitan cuando un glob sin comillas está presente porque el glob podría expandirse a una bandera como `-delete`.

Un `cd` en una ruta dentro de su directorio de trabajo o un [directorio adicional](#working-directories) también es de solo lectura. Un comando compuesto como `cd packages/api && ls` se ejecuta sin un aviso cuando cada parte se califica por su cuenta. Combinar `cd` con `git` en un comando compuesto siempre solicita, independientemente del directorio de destino.

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
  * **Agregar orientación CLAUDE.md**: describa sus patrones curl permitidos en `CLAUDE.md`. Esto forma lo que Claude intenta pero no aplica un límite, así que emparéjelo con una de las opciones anteriores

  Tenga en cuenta que usar WebFetch solo no previene el acceso a la red. Si se permite Bash, Claude aún puede usar `curl`, `wget` u otras herramientas para alcanzar cualquier URL.
</Warning>

### PowerShell

Las reglas de permisos de PowerShell usan la misma forma que las reglas de Bash. Los comodines con `*` coinciden en cualquier posición, el sufijo `:*` es equivalente a un ` *` final, y un `PowerShell` desnudo o `PowerShell(*)` coincide con cada comando. Esta configuración permite comandos `Get-ChildItem` y `git commit` mientras bloquea `Remove-Item`:

```json theme={null}
{
  "permissions": {
    "allow": [
      "PowerShell(Get-ChildItem *)",
      "PowerShell(git commit *)"
    ],
    "deny": [
      "PowerShell(Remove-Item *)"
    ]
  }
}
```

Los alias comunes se canonicalizan antes de coincidir. Una regla escrita para el nombre del cmdlet también coincide con sus alias, por lo que `PowerShell(Get-ChildItem *)` coincide con `gci`, `ls` y `dir` también. La coincidencia no distingue mayúsculas de minúsculas.

Claude Code analiza el AST de PowerShell y verifica cada comando en un comando compuesto de forma independiente. Los operadores de tubería `|`, separadores de declaración `;` y en PowerShell 7+ los operadores de cadena `&&` y `||` dividen un comando compuesto en subcomandos. Una regla debe coincidir con cada subcomando para que se permita el comando compuesto.

### Read y Edit

Las reglas `Edit` se aplican a todas las herramientas integradas que editan archivos. Claude hace un esfuerzo de mejor intento para aplicar reglas `Read` a todas las herramientas integradas que leen archivos como Grep y Glob.

<Warning>
  Las reglas de negación Read y Edit se aplican a las herramientas de archivo integradas de Claude y a los comandos de archivo que Claude Code reconoce en Bash, como `cat`, `head`, `tail` y `sed`. No se aplican a subprocesos arbitrarios que leen o escriben archivos indirectamente, como un script de Python o Node que abre archivos por sí mismo. Para aplicación a nivel del SO que bloquea todos los procesos de acceder a una ruta, [habilite el sandbox](/es/sandboxing).
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

Una regla solo coincide con archivos bajo su anclaje, por lo que el anclaje determina cuán lejos llega una regla de negación. Los nombres de archivo desnudos siguen la semántica de gitignore y coinciden en cualquier profundidad, por lo que `Read(.env)` y `Read(**/.env)` son equivalentes:

| Regla de negación              | Bloquea                                                     | No bloquea                                                     |
| ------------------------------ | ----------------------------------------------------------- | -------------------------------------------------------------- |
| `Read(.env)` o `Read(**/.env)` | cualquier `.env` en o bajo el directorio actual             | `.env` en un directorio padre u otro proyecto                  |
| `Read(//**/.env)`              | cualquier `.env` en cualquier lugar del sistema de archivos | nada; la regla está anclada en la raíz del sistema de archivos |

<Note>
  En patrones gitignore, `*` coincide con archivos en un solo directorio mientras que `**` coincide recursivamente en directorios. Para permitir todo acceso a archivos, use solo el nombre de la herramienta sin paréntesis: `Read`, `Edit` o `Write`.
</Note>

Cuando Claude accede a un symlink, las reglas de permisos verifican dos rutas: el symlink mismo y el archivo al que se resuelve. Las reglas de permiso y negación tratan ese par de manera diferente: las reglas de permiso recurren a solicitarle, mientras que las reglas de negación bloquean directamente.

* **Reglas de permiso**: se aplican solo cuando tanto la ruta del symlink como su destino coinciden. Un symlink dentro de un directorio permitido que apunta fuera de él aún le solicita.
* **Reglas de negación**: se aplican cuando la ruta del symlink o su destino coincide. Un symlink que apunta a un archivo denegado está denegado.

Por ejemplo, con `Read(./project/**)` permitido y `Read(~/.ssh/**)` denegado, un symlink en `./project/key` que apunta a `~/.ssh/id_rsa` está bloqueado: el destino falla la regla de permiso y coincide con la regla de negación.

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

Las decisiones del hook no omiten las reglas de permisos. Las reglas de negación y solicitud se evalúan independientemente de lo que devuelva un hook PreToolUse, por lo que una regla de negación coincidente bloquea la llamada y una regla de solicitud coincidente aún solicita incluso cuando el hook devolvió `"allow"` u `"ask"`. Esto preserva la precedencia de negación primero descrita en [Administrar permisos](#manage-permissions), incluyendo reglas de negación establecidas en configuración administrada.

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

| Configuración                                                          | Cargado desde `--add-dir`                                                                                                                                                            |
| :--------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Skills](/es/skills) en `.claude/skills/`                              | Sí, con recarga en vivo                                                                                                                                                              |
| Configuración de plugins en `.claude/settings.json`                    | Solo `enabledPlugins` y `extraKnownMarketplaces`                                                                                                                                     |
| Archivos [CLAUDE.md](/es/memory), `.claude/rules/` y `CLAUDE.local.md` | Solo cuando `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` está establecido. `CLAUDE.local.md` además requiere la fuente de configuración `local`, que está habilitada por defecto |

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
* Las restricciones del sistema de archivos en el sandbox combinan la configuración [`sandbox.filesystem`](/es/sandboxing) con reglas de negación Read y Edit; ambas se fusionan en el límite final del sandbox
* Las restricciones de red combinan reglas de permisos WebFetch con las listas `allowedDomains` y `deniedDomains` del sandbox

Cuando el sandboxing está habilitado con `autoAllowBashIfSandboxed: true`, que es el valor predeterminado, los comandos Bash en sandbox se ejecutan sin solicitar incluso si sus permisos incluyen `ask: Bash(*)`. El límite del sandbox sustituye el aviso por comando. Las reglas de negación explícitas aún se aplican, y los comandos `rm` o `rmdir` que apunten a `/`, su directorio de inicio u otras rutas críticas del sistema aún desencadenan un aviso. Consulte [modos de sandbox](/es/sandboxing#sandbox-modes) para cambiar este comportamiento.

## Configuración administrada

Para organizaciones que necesitan control centralizado sobre la configuración de Claude Code, los administradores pueden implementar configuración administrada que no puede ser anulada por configuración de usuario o proyecto. Estas configuraciones de política siguen el mismo formato que archivos de configuración regulares y se pueden entregar a través de políticas MDM/a nivel del SO, archivos de configuración administrada o [configuración administrada por servidor](/es/server-managed-settings). Consulte [archivos de configuración](/es/settings#settings-files) para mecanismos de entrega y ubicaciones de archivos.

### Configuración solo administrada

Las siguientes configuraciones solo se leen desde configuración administrada. Colocarlas en archivos de configuración de usuario o proyecto no tiene efecto.

| Configuración                                  | Descripción                                                                                                                                                                                                                                                                                               |
| :--------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowedChannelPlugins`                        | Lista de permitidos de plugins de canal que pueden enviar mensajes. Reemplaza la lista de permitidos predeterminada de Anthropic cuando se establece. Requiere `channelsEnabled: true`. Consulte [Restringir qué plugins de canal pueden ejecutarse](/es/channels#restrict-which-channel-plugins-can-run) |
| `allowManagedHooksOnly`                        | Cuando es `true`, solo se cargan hooks administrados, hooks SDK y hooks de plugins forzados habilitados en la configuración administrada `enabledPlugins`. Los hooks de usuario, proyecto y todos los demás plugins están bloqueados                                                                      |
| `allowManagedMcpServersOnly`                   | Cuando es `true`, solo se respetan `allowedMcpServers` de configuración administrada. `deniedMcpServers` aún se fusiona de todas las fuentes. Consulte [Configuración MCP administrada](/es/mcp#managed-mcp-configuration)                                                                                |
| `allowManagedPermissionRulesOnly`              | Cuando es `true`, evita que la configuración de usuario y proyecto defina reglas de permisos `allow`, `ask` o `deny`. Solo se aplican las reglas en configuración administrada                                                                                                                            |
| `blockedMarketplaces`                          | Lista de bloqueo de fuentes de marketplace. Las fuentes bloqueadas se verifican antes de descargar, por lo que nunca tocan el sistema de archivos. Consulte [restricciones de marketplace administradas](/es/plugin-marketplaces#managed-marketplace-restrictions)                                        |
| `channelsEnabled`                              | Permitir [channels](/es/channels) para la organización. Consulte [controles empresariales](/es/channels#enterprise-controls) para el valor predeterminado en cada plan                                                                                                                                    |
| `forceRemoteSettingsRefresh`                   | Cuando es `true`, bloquea el inicio de CLI hasta que la configuración administrada remota se obtenga recientemente y sale si la obtención falla. Consulte [aplicación de cierre de falla](/es/server-managed-settings#enforce-fail-closed-startup)                                                        |
| `pluginTrustMessage`                           | Mensaje personalizado agregado a la advertencia de confianza de plugin mostrada antes de la instalación                                                                                                                                                                                                   |
| `sandbox.filesystem.allowManagedReadPathsOnly` | Cuando es `true`, solo se respetan rutas `filesystem.allowRead` de configuración administrada. `denyRead` aún se fusiona de todas las fuentes                                                                                                                                                             |
| `sandbox.network.allowManagedDomainsOnly`      | Cuando es `true`, solo se respetan `allowedDomains` y reglas de permiso `WebFetch(domain:...)` de configuración administrada. Los dominios no permitidos se bloquean automáticamente sin solicitar al usuario. Los dominios denegados aún se fusionan de todas las fuentes                                |
| `strictKnownMarketplaces`                      | Controla qué marketplaces de plugins pueden agregar los usuarios e instalar plugins desde. Consulte [restricciones de marketplace administradas](/es/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                |
| `wslInheritsWindowsSettings`                   | Cuando es `true` en la clave del registro HKLM de Windows o `C:\Program Files\ClaudeCode\managed-settings.json`, WSL lee configuración administrada de la cadena de política de Windows además de `/etc/claude-code`. Consulte [Archivos de configuración](/es/settings#settings-files)                   |

`disableBypassPermissionsMode` generalmente se coloca en configuración administrada para aplicar la política organizacional, pero funciona desde cualquier alcance. Un usuario puede establecerlo en su propia configuración para bloquearse a sí mismo del modo de bypass.

<Note>
  En planes Team y Enterprise, un administrador habilita o deshabilita [Remote Control](/es/remote-control) y [sesiones web](/es/claude-code-on-the-web) en toda la organización en [configuración de administrador de Claude Code](https://claude.ai/admin-settings/claude-code). Remote Control puede deshabilitarse adicionalmente por dispositivo con la configuración administrada [`disableRemoteControl`](/es/settings#available-settings). Las sesiones web no tienen clave de configuración administrada por dispositivo.
</Note>

## Configuración de precedencia

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
* [Configure auto mode](/es/auto-mode-config): indique al clasificador del modo auto qué infraestructura confía su organización
* [Sandboxing](/es/sandboxing): aislamiento del sistema de archivos y red a nivel del SO para comandos Bash
* [Authentication](/es/authentication): configure el acceso de usuario a Claude Code
* [Security](/es/security): salvaguardas de seguridad y mejores prácticas
* [Hooks](/es/hooks-guide): automatice flujos de trabajo y extienda la evaluación de permisos
