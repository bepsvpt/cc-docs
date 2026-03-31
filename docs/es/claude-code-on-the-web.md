> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code en la web

> Ejecuta tareas de Claude Code de forma asincrónica en infraestructura en la nube segura

<Note>
  Claude Code en la web está actualmente en vista previa de investigación.
</Note>

## ¿Qué es Claude Code en la web?

Claude Code en la web permite a los desarrolladores iniciar Claude Code desde la aplicación Claude. Esto es perfecto para:

* **Responder preguntas**: Pregunta sobre la arquitectura del código y cómo se implementan las características
* **Correcciones de errores y tareas rutinarias**: Tareas bien definidas que no requieren dirección frecuente
* **Trabajo en paralelo**: Aborda múltiples correcciones de errores en paralelo
* **Repositorios no en su máquina local**: Trabaja en código que no tiene desprotegido localmente
* **Cambios de backend**: Donde Claude Code puede escribir pruebas y luego escribir código para pasar esas pruebas

Claude Code también está disponible en la aplicación Claude para [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) y [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) para iniciar tareas sobre la marcha y monitorear el trabajo en progreso.

Puede [iniciar nuevas tareas en la web desde su terminal](#from-terminal-to-web) con `--remote`, o [teleportar sesiones web de vuelta a su terminal](#from-web-to-terminal) para continuar localmente. Para usar la interfaz web mientras ejecuta Claude Code en su propia máquina en lugar de infraestructura en la nube, consulte [Control Remoto](/es/remote-control).

## ¿Quién puede usar Claude Code en la web?

Claude Code en la web está disponible en vista previa de investigación para:

* **Usuarios Pro**
* **Usuarios Max**
* **Usuarios de Team**
* **Usuarios Enterprise** con asientos premium o asientos Chat + Claude Code

## Primeros pasos

Configure Claude Code en la web desde el navegador o desde su terminal.

### Desde el navegador

1. Visite [claude.ai/code](https://claude.ai/code)
2. Conecte su cuenta de GitHub
3. Instale la aplicación Claude GitHub en sus repositorios
4. Seleccione su entorno predeterminado
5. Envíe su tarea de codificación
6. Revise los cambios en la vista de diferencias, itere con comentarios y luego cree una solicitud de extracción

### Desde el terminal

Ejecute `/web-setup` dentro de Claude Code para conectar GitHub usando sus credenciales locales de `gh` CLI. El comando sincroniza su `gh auth token` a Claude Code en la web, crea un entorno en la nube predeterminado y abre claude.ai/code en su navegador cuando finaliza.

Esta ruta requiere que la CLI `gh` esté instalada y autenticada con `gh auth login`. Si `gh` no está disponible, `/web-setup` abre claude.ai/code para que pueda conectar GitHub desde el navegador en su lugar.

Sus credenciales de `gh` le dan a Claude acceso para clonar e insertar, por lo que puede omitir la aplicación GitHub para sesiones básicas. Instale la aplicación más tarde si desea [Auto-fix](#auto-fix-pull-requests), que usa la aplicación para recibir webhooks de PR.

<Note>
  Los administradores de Team y Enterprise pueden deshabilitar la configuración del terminal con el interruptor de configuración web rápida en [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code).
</Note>

## Cómo funciona

Cuando inicia una tarea en Claude Code en la web:

1. **Clonación de repositorio**: Su repositorio se clona en una máquina virtual administrada por Anthropic
2. **Configuración del entorno**: Claude prepara un entorno en la nube seguro con su código, luego ejecuta su [script de configuración](#setup-scripts) si está configurado
3. **Configuración de red**: El acceso a Internet se configura según su configuración
4. **Ejecución de tareas**: Claude analiza el código, realiza cambios, ejecuta pruebas y verifica su trabajo
5. **Finalización**: Se le notifica cuando finaliza y puede crear una PR con los cambios
6. **Resultados**: Los cambios se insertan en una rama, listos para la creación de solicitud de extracción

## Revise los cambios con la vista de diferencias

La vista de diferencias le permite ver exactamente qué cambió Claude antes de crear una solicitud de extracción. En lugar de hacer clic en "Crear PR" para revisar cambios en GitHub, vea la diferencia directamente en la aplicación e itere con Claude hasta que los cambios estén listos.

Cuando Claude realiza cambios en archivos, aparece un indicador de estadísticas de diferencias que muestra el número de líneas agregadas y eliminadas (por ejemplo, `+12 -1`). Seleccione este indicador para abrir el visor de diferencias, que muestra una lista de archivos a la izquierda y los cambios para cada archivo a la derecha.

Desde la vista de diferencias, puede:

* Revisar cambios archivo por archivo
* Comentar sobre cambios específicos para solicitar modificaciones
* Continuar iterando con Claude según lo que vea

Esto le permite refinar cambios a través de múltiples rondas de retroalimentación sin crear PRs de borrador o cambiar a GitHub.

## Correcciones automáticas de solicitudes de extracción

Claude puede observar una solicitud de extracción y responder automáticamente a fallos de CI y comentarios de revisión. Claude se suscribe a la actividad de GitHub en la PR, y cuando falla una verificación o un revisor deja un comentario, Claude investiga e inserta una corrección si es clara.

<Note>
  Auto-fix requiere que la aplicación Claude GitHub esté instalada en su repositorio. Si aún no lo ha hecho, instálela desde la [página de la aplicación GitHub](https://github.com/apps/claude) o cuando se le solicite durante la [configuración](#getting-started).
</Note>

Hay algunas formas de activar auto-fix dependiendo de dónde provenga la PR y qué dispositivo esté usando:

* **PRs creadas en Claude Code en la web**: abra la barra de estado de CI y seleccione **Auto-fix**
* **Desde la aplicación móvil**: dígale a Claude que corrija automáticamente la PR, por ejemplo "observa esta PR y corrige cualquier fallo de CI o comentario de revisión"
* **Cualquier PR existente**: pegue la URL de la PR en una sesión y dígale a Claude que la corrija automáticamente

### Cómo Claude responde a la actividad de PR

Cuando auto-fix está activo, Claude recibe eventos de GitHub para la PR incluyendo nuevos comentarios de revisión y fallos de verificación de CI. Para cada evento, Claude investiga y decide cómo proceder:

* **Correcciones claras**: si Claude está seguro de una corrección y no entra en conflicto con instrucciones anteriores, Claude realiza el cambio, lo inserta y explica qué se hizo en la sesión
* **Solicitudes ambiguas**: si el comentario de un revisor podría interpretarse de múltiples formas o implica algo arquitectónicamente significativo, Claude le pregunta antes de actuar
* **Eventos duplicados o sin acción**: si un evento es un duplicado o no requiere cambio, Claude lo anota en la sesión y continúa

Claude puede responder a hilos de comentarios de revisión en GitHub como parte de resolverlos. Estas respuestas se publican usando su cuenta de GitHub, por lo que aparecen bajo su nombre de usuario, pero cada respuesta está etiquetada como proveniente de Claude Code para que los revisores sepan que fue escrita por el agente y no por usted directamente.

## Mover tareas entre web y terminal

Puede iniciar nuevas tareas en la web desde su terminal, o extraer sesiones web en su terminal para continuar localmente. Las sesiones web persisten incluso si cierra su portátil, y puede monitorearlas desde cualquier lugar, incluida la aplicación móvil Claude.

<Note>
  La transferencia de sesión es unidireccional: puede extraer sesiones web en su terminal, pero no puede insertar una sesión de terminal existente en la web. La bandera `--remote` crea una *nueva* sesión web para su repositorio actual.
</Note>

### De terminal a web

Inicie una sesión web desde la línea de comandos con la bandera `--remote`:

```bash  theme={null}
claude --remote "Fix the authentication bug in src/auth/login.ts"
```

Esto crea una nueva sesión web en claude.ai. La tarea se ejecuta en la nube mientras continúa trabajando localmente. Use `/tasks` para verificar el progreso, o abra la sesión en claude.ai o la aplicación móvil Claude para interactuar directamente. Desde allí puede dirigir Claude, proporcionar retroalimentación o responder preguntas como en cualquier otra conversación.

#### Consejos para tareas remotas

**Planifique localmente, ejecute remotamente**: Para tareas complejas, inicie Claude en modo de plan para colaborar en el enfoque, luego envíe el trabajo a la web:

```bash  theme={null}
claude --permission-mode plan
```

En modo de plan, Claude solo puede leer archivos y explorar la base de código. Una vez que esté satisfecho con el plan, inicie una sesión remota para ejecución autónoma:

```bash  theme={null}
claude --remote "Execute the migration plan in docs/migration-plan.md"
```

Este patrón le da control sobre la estrategia mientras permite que Claude ejecute de forma autónoma en la nube.

**Ejecute tareas en paralelo**: Cada comando `--remote` crea su propia sesión web que se ejecuta de forma independiente. Puede iniciar múltiples tareas y todas se ejecutarán simultáneamente en sesiones separadas:

```bash  theme={null}
claude --remote "Fix the flaky test in auth.spec.ts"
claude --remote "Update the API documentation"
claude --remote "Refactor the logger to use structured output"
```

Monitoree todas las sesiones con `/tasks`. Cuando una sesión se completa, puede crear una PR desde la interfaz web o [teleportar](#from-web-to-terminal) la sesión a su terminal para continuar trabajando.

### De web a terminal

Hay varias formas de extraer una sesión web en su terminal:

* **Usando `/teleport`**: Desde Claude Code, ejecute `/teleport` (o `/tp`) para ver un selector interactivo de sus sesiones web. Si tiene cambios sin confirmar, se le pedirá que los guarde primero.
* **Usando `--teleport`**: Desde la línea de comandos, ejecute `claude --teleport` para un selector de sesión interactivo, o `claude --teleport <session-id>` para reanudar una sesión específica directamente.
* **Desde `/tasks`**: Ejecute `/tasks` para ver sus sesiones de fondo, luego presione `t` para teleportarse a una
* **Desde la interfaz web**: Haga clic en "Abrir en CLI" para copiar un comando que puede pegar en su terminal

Cuando teleporta una sesión, Claude verifica que esté en el repositorio correcto, obtiene y verifica la rama de la sesión remota, y carga el historial de conversación completo en su terminal.

#### Requisitos para teleportar

Teleport verifica estos requisitos antes de reanudar una sesión. Si algún requisito no se cumple, verá un error o se le pedirá que resuelva el problema.

| Requisito            | Detalles                                                                                                               |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Estado de git limpio | Su directorio de trabajo no debe tener cambios sin confirmar. Teleport le pide que guarde los cambios si es necesario. |
| Repositorio correcto | Debe ejecutar `--teleport` desde una desprotección del mismo repositorio, no desde una bifurcación.                    |
| Rama disponible      | La rama de la sesión web debe haber sido insertada en el remoto. Teleport la obtiene y verifica automáticamente.       |
| Misma cuenta         | Debe estar autenticado en la misma cuenta de Claude.ai utilizada en la sesión web.                                     |

### Compartir sesiones

Para compartir una sesión, alterne su visibilidad según los tipos de cuenta a continuación. Después de eso, comparta el enlace de sesión tal como está. Los destinatarios que abran su sesión compartida verán el estado más reciente de la sesión al cargar, pero la página del destinatario no se actualizará en tiempo real.

#### Compartir desde una cuenta Enterprise o Teams

Para cuentas Enterprise y Teams, las dos opciones de visibilidad son **Privada** y **Team**. La visibilidad de Team hace que la sesión sea visible para otros miembros de su organización de Claude.ai. La verificación de acceso al repositorio está habilitada de forma predeterminada, según la cuenta de GitHub conectada a la cuenta del destinatario. El nombre para mostrar de su cuenta es visible para todos los destinatarios con acceso. Las sesiones de [Claude en Slack](/es/slack) se comparten automáticamente con visibilidad de Team.

#### Compartir desde una cuenta Max o Pro

Para cuentas Max y Pro, las dos opciones de visibilidad son **Privada** y **Pública**. La visibilidad pública hace que la sesión sea visible para cualquier usuario que haya iniciado sesión en claude.ai.

Verifique su sesión para contenido sensible antes de compartir. Las sesiones pueden contener código y credenciales de repositorios privados de GitHub. La verificación de acceso al repositorio no está habilitada de forma predeterminada.

Habilite la verificación de acceso al repositorio y/o retenga su nombre de sus sesiones compartidas yendo a Configuración > Claude Code > Configuración de uso compartido.

## Programar tareas recurrentes

Ejecute Claude en un cronograma recurrente para automatizar trabajo como revisiones diarias de PR, auditorías de dependencias y análisis de fallos de CI. Consulte [Programar tareas en la web](/es/web-scheduled-tasks) para la guía completa.

## Administrar sesiones

### Archivar sesiones

Puede archivar sesiones para mantener su lista de sesiones organizada. Las sesiones archivadas se ocultan de la lista de sesiones predeterminada pero se pueden ver filtrando sesiones archivadas.

Para archivar una sesión, pase el cursor sobre la sesión en la barra lateral y haga clic en el icono de archivo.

### Eliminar sesiones

Eliminar una sesión elimina permanentemente la sesión y sus datos. Esta acción no se puede deshacer. Puede eliminar una sesión de dos formas:

* **Desde la barra lateral**: Filtre sesiones archivadas, luego pase el cursor sobre la sesión que desea eliminar y haga clic en el icono de eliminar
* **Desde el menú de sesión**: Abra una sesión, haga clic en el menú desplegable junto al título de la sesión y seleccione **Eliminar**

Se le pedirá que confirme antes de que se elimine una sesión.

## Entorno en la nube

### Imagen predeterminada

Construimos y mantenemos una imagen universal con cadenas de herramientas comunes y ecosistemas de lenguaje preinstalados. Esta imagen incluye:

* Lenguajes de programación populares y tiempos de ejecución
* Herramientas de compilación comunes y administradores de paquetes
* Marcos de prueba y linters

#### Verificar herramientas disponibles

Para ver qué está preinstalado en su entorno, pida a Claude Code que ejecute:

```bash  theme={null}
check-tools
```

Este comando muestra:

* Lenguajes de programación y sus versiones
* Administradores de paquetes disponibles
* Herramientas de desarrollo instaladas

#### Configuraciones específicas del idioma

La imagen universal incluye entornos preconfigurados para:

* **Python**: Python 3.x con pip, poetry y bibliotecas científicas comunes
* **Node.js**: Últimas versiones LTS con npm, yarn, pnpm y bun
* **Ruby**: Versiones 3.1.6, 3.2.6, 3.3.6 (predeterminado: 3.3.6) con gem, bundler y rbenv para gestión de versiones
* **PHP**: Versión 8.4.14
* **Java**: OpenJDK con Maven y Gradle
* **Go**: Última versión estable con soporte de módulos
* **Rust**: Cadena de herramientas Rust con cargo
* **C++**: Compiladores GCC y Clang

#### Bases de datos

La imagen universal incluye las siguientes bases de datos:

* **PostgreSQL**: Versión 16
* **Redis**: Versión 7.0

### Configuración del entorno

Cuando inicia una sesión en Claude Code en la web, esto es lo que sucede bajo el capó:

1. **Preparación del entorno**: Clonamos su repositorio y ejecutamos cualquier [script de configuración](#setup-scripts) configurado. El repositorio se clonará con la rama predeterminada en su repositorio de GitHub. Si desea desproteger una rama específica, puede especificar eso en el mensaje.

2. **Configuración de red**: Configuramos el acceso a Internet para el agente. El acceso a Internet es limitado de forma predeterminada, pero puede configurar el entorno para que no tenga acceso a Internet o acceso completo a Internet según sus necesidades.

3. **Ejecución de Claude Code**: Claude Code se ejecuta para completar su tarea, escribiendo código, ejecutando pruebas y verificando su trabajo. Puede guiar y dirigir Claude durante toda la sesión a través de la interfaz web. Claude respeta el contexto que ha definido en su `CLAUDE.md`.

4. **Resultado**: Cuando Claude completa su trabajo, insertará la rama en remoto. Podrá crear una PR para la rama.

<Note>
  Claude opera completamente a través del terminal y las herramientas CLI disponibles en el entorno. Utiliza las herramientas preinstaladas en la imagen universal y cualquier herramienta adicional que instale a través de hooks o gestión de dependencias.
</Note>

**Para agregar un nuevo entorno:** Seleccione el entorno actual para abrir el selector de entorno y luego seleccione "Agregar entorno". Esto abrirá un diálogo donde puede especificar el nombre del entorno, el nivel de acceso de red, las variables de entorno y un [script de configuración](#setup-scripts).

**Para actualizar un entorno existente:** Seleccione el entorno actual, a la derecha del nombre del entorno, y seleccione el botón de configuración. Esto abrirá un diálogo donde puede actualizar el nombre del entorno, el acceso de red, las variables de entorno y el script de configuración.

**Para seleccionar su entorno predeterminado desde el terminal:** Si tiene múltiples entornos configurados, ejecute `/remote-env` para elegir cuál usar al iniciar sesiones web desde su terminal con `--remote`. Con un único entorno, este comando muestra su configuración actual.

<Note>
  Las variables de entorno deben especificarse como pares clave-valor, en [formato `.env`](https://www.dotenv.org/). Por ejemplo:

  ```text  theme={null}
  API_KEY=your_api_key
  DEBUG=true
  ```
</Note>

### Scripts de configuración

Un script de configuración es un script Bash que se ejecuta cuando comienza una nueva sesión en la nube, antes de que se lance Claude Code. Use scripts de configuración para instalar dependencias, configurar herramientas o preparar cualquier cosa que el entorno en la nube necesite que no esté en la [imagen predeterminada](#default-image).

Los scripts se ejecutan como root en Ubuntu 24.04, por lo que `apt install` y la mayoría de los administradores de paquetes de lenguaje funcionan.

<Tip>
  Para verificar qué ya está instalado antes de agregarlo a su script, pida a Claude que ejecute `check-tools` en una sesión en la nube.
</Tip>

Para agregar un script de configuración, abra el diálogo de configuración del entorno e ingrese su script en el campo **Script de configuración**.

Este ejemplo instala la CLI `gh`, que no está en la imagen predeterminada:

```bash  theme={null}
#!/bin/bash
apt update && apt install -y gh
```

Los scripts de configuración se ejecutan solo cuando se crea una nueva sesión. Se omiten cuando se reanuda una sesión existente.

Si el script sale con un código distinto de cero, la sesión no se inicia. Agregue `|| true` a comandos no críticos para evitar bloquear la sesión en una instalación inestable.

<Note>
  Los scripts de configuración que instalan paquetes necesitan acceso a la red para llegar a los registros. El acceso a la red predeterminado permite conexiones a [registros de paquetes comunes](#default-allowed-domains) incluyendo npm, PyPI, RubyGems y crates.io. Los scripts fallarán al instalar paquetes si su entorno tiene acceso a la red deshabilitado.
</Note>

#### Scripts de configuración vs. hooks SessionStart

Use un script de configuración para instalar cosas que la nube necesita pero su portátil ya tiene, como un tiempo de ejecución de lenguaje o herramienta CLI. Use un [hook SessionStart](/es/hooks#sessionstart) para la configuración del proyecto que debe ejecutarse en todas partes, nube y local, como `npm install`.

Ambos se ejecutan al inicio de una sesión, pero pertenecen a diferentes lugares:

|                | Scripts de configuración                                   | Hooks SessionStart                                                        |
| -------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------- |
| Adjunto a      | El entorno en la nube                                      | Su repositorio                                                            |
| Configurado en | Interfaz de usuario del entorno en la nube                 | `.claude/settings.json` en su repositorio                                 |
| Se ejecuta     | Antes de que se lance Claude Code, solo en sesiones nuevas | Después de que se lance Claude Code, en cada sesión incluyendo reanudadas |
| Alcance        | Solo entornos en la nube                                   | Tanto local como nube                                                     |

Los hooks SessionStart también se pueden definir en su `~/.claude/settings.json` a nivel de usuario localmente, pero la configuración a nivel de usuario no se transfiere a sesiones en la nube. En la nube, solo se ejecutan los hooks comprometidos con el repositorio.

### Gestión de dependencias

Las imágenes de entorno personalizadas y las instantáneas aún no son compatibles. Use [scripts de configuración](#setup-scripts) para instalar paquetes cuando comienza una sesión, o [hooks SessionStart](/es/hooks#sessionstart) para la instalación de dependencias que también debe ejecutarse en entornos locales. Los hooks SessionStart tienen [limitaciones conocidas](#dependency-management-limitations).

Para configurar la instalación automática de dependencias con un script de configuración, abra la configuración de su entorno y agregue un script:

```bash  theme={null}
#!/bin/bash
npm install
pip install -r requirements.txt
```

Alternativamente, puede usar hooks SessionStart en el archivo `.claude/settings.json` de su repositorio para la instalación de dependencias que también debe ejecutarse en entornos locales:

```json  theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/scripts/install_pkgs.sh"
          }
        ]
      }
    ]
  }
}
```

Cree el script correspondiente en `scripts/install_pkgs.sh`:

```bash  theme={null}
#!/bin/bash

# Only run in remote environments
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

npm install
pip install -r requirements.txt
exit 0
```

Hágalo ejecutable: `chmod +x scripts/install_pkgs.sh`

#### Persistir variables de entorno

Los hooks SessionStart pueden persistir variables de entorno para comandos Bash posteriores escribiendo en el archivo especificado en la variable de entorno `CLAUDE_ENV_FILE`. Para más detalles, consulte [hooks SessionStart](/es/hooks#sessionstart) en la referencia de hooks.

#### Limitaciones de gestión de dependencias

* **Los hooks se disparan para todas las sesiones**: Los hooks SessionStart se ejecutan en entornos locales y remotos. No hay configuración de hook para limitar un hook solo a sesiones remotas. Para omitir la ejecución local, verifique la variable de entorno `CLAUDE_CODE_REMOTE` en su script como se muestra arriba.
* **Requiere acceso a la red**: Los comandos de instalación necesitan acceso a la red para llegar a los registros de paquetes. Si su entorno está configurado con acceso "Sin internet", estos hooks fallarán. Use acceso de red "Limitado" (el predeterminado) o "Completo". La [lista de permitidos predeterminada](#default-allowed-domains) incluye registros comunes como npm, PyPI, RubyGems y crates.io.
* **Compatibilidad de proxy**: Todo el tráfico saliente en entornos remotos pasa a través de un [proxy de seguridad](#security-proxy). Algunos administradores de paquetes no funcionan correctamente con este proxy. Bun es un ejemplo conocido.
* **Se ejecuta en cada inicio de sesión**: Los hooks se ejecutan cada vez que comienza o se reanuda una sesión, agregando latencia de inicio. Mantenga los scripts de instalación rápidos verificando si las dependencias ya están presentes antes de reinstalar.

## Acceso a la red y seguridad

### Política de red

#### Proxy de GitHub

Por seguridad, todas las operaciones de GitHub pasan a través de un servicio de proxy dedicado que maneja de forma transparente todas las interacciones de git. Dentro del sandbox, el cliente de git se autentica usando una credencial de alcance personalizada. Este proxy:

* Gestiona la autenticación de GitHub de forma segura: el cliente de git usa una credencial de alcance dentro del sandbox, que el proxy verifica y traduce a su token de autenticación real de GitHub
* Restringe las operaciones de inserción de git a la rama de trabajo actual por seguridad
* Permite operaciones de clonación, obtención y PR sin problemas mientras mantiene límites de seguridad

#### Proxy de seguridad

Los entornos se ejecutan detrás de un proxy de red HTTP/HTTPS para propósitos de seguridad y prevención de abuso. Todo el tráfico de Internet saliente pasa a través de este proxy, que proporciona:

* Protección contra solicitudes maliciosas
* Limitación de velocidad y prevención de abuso
* Filtrado de contenido para mayor seguridad

### Niveles de acceso

De forma predeterminada, el acceso a la red se limita a [dominios en la lista de permitidos](#default-allowed-domains).

Puede configurar acceso a la red personalizado, incluyendo deshabilitar el acceso a la red.

### Dominios permitidos predeterminados

Cuando se usa acceso de red "Limitado", los siguientes dominios están permitidos de forma predeterminada:

#### Servicios Anthropic

* api.anthropic.com
* statsig.anthropic.com
* platform.claude.com
* code.claude.com
* claude.ai

#### Control de versiones

* github.com
* [www.github.com](http://www.github.com)
* api.github.com
* npm.pkg.github.com
* raw\.githubusercontent.com
* pkg-npm.githubusercontent.com
* objects.githubusercontent.com
* codeload.github.com
* avatars.githubusercontent.com
* camo.githubusercontent.com
* gist.github.com
* gitlab.com
* [www.gitlab.com](http://www.gitlab.com)
* registry.gitlab.com
* bitbucket.org
* [www.bitbucket.org](http://www.bitbucket.org)
* api.bitbucket.org

#### Registros de contenedores

* registry-1.docker.io
* auth.docker.io
* index.docker.io
* hub.docker.com
* [www.docker.com](http://www.docker.com)
* production.cloudflare.docker.com
* download.docker.com
* gcr.io
* \*.gcr.io
* ghcr.io
* mcr.microsoft.com
* \*.data.mcr.microsoft.com
* public.ecr.aws

#### Plataformas en la nube

* cloud.google.com
* accounts.google.com
* gcloud.google.com
* \*.googleapis.com
* storage.googleapis.com
* compute.googleapis.com
* container.googleapis.com
* azure.com
* portal.azure.com
* microsoft.com
* [www.microsoft.com](http://www.microsoft.com)
* \*.microsoftonline.com
* packages.microsoft.com
* dotnet.microsoft.com
* dot.net
* visualstudio.com
* dev.azure.com
* \*.amazonaws.com
* \*.api.aws
* oracle.com
* [www.oracle.com](http://www.oracle.com)
* java.com
* [www.java.com](http://www.java.com)
* java.net
* [www.java.net](http://www.java.net)
* download.oracle.com
* yum.oracle.com

#### Administradores de paquetes - JavaScript/Node

* registry.npmjs.org
* [www.npmjs.com](http://www.npmjs.com)
* [www.npmjs.org](http://www.npmjs.org)
* npmjs.com
* npmjs.org
* yarnpkg.com
* registry.yarnpkg.com

#### Administradores de paquetes - Python

* pypi.org
* [www.pypi.org](http://www.pypi.org)
* files.pythonhosted.org
* pythonhosted.org
* test.pypi.org
* pypi.python.org
* pypa.io
* [www.pypa.io](http://www.pypa.io)

#### Administradores de paquetes - Ruby

* rubygems.org
* [www.rubygems.org](http://www.rubygems.org)
* api.rubygems.org
* index.rubygems.org
* ruby-lang.org
* [www.ruby-lang.org](http://www.ruby-lang.org)
* rubyforge.org
* [www.rubyforge.org](http://www.rubyforge.org)
* rubyonrails.org
* [www.rubyonrails.org](http://www.rubyonrails.org)
* rvm.io
* get.rvm.io

#### Administradores de paquetes - Rust

* crates.io
* [www.crates.io](http://www.crates.io)
* index.crates.io
* static.crates.io
* rustup.rs
* static.rust-lang.org
* [www.rust-lang.org](http://www.rust-lang.org)

#### Administradores de paquetes - Go

* proxy.golang.org
* sum.golang.org
* index.golang.org
* golang.org
* [www.golang.org](http://www.golang.org)
* goproxy.io
* pkg.go.dev

#### Administradores de paquetes - JVM

* maven.org
* repo.maven.org
* central.maven.org
* repo1.maven.org
* jcenter.bintray.com
* gradle.org
* [www.gradle.org](http://www.gradle.org)
* services.gradle.org
* plugins.gradle.org
* kotlin.org
* [www.kotlin.org](http://www.kotlin.org)
* spring.io
* repo.spring.io

#### Administradores de paquetes - Otros idiomas

* packagist.org (PHP Composer)
* [www.packagist.org](http://www.packagist.org)
* repo.packagist.org
* nuget.org (.NET NuGet)
* [www.nuget.org](http://www.nuget.org)
* api.nuget.org
* pub.dev (Dart/Flutter)
* api.pub.dev
* hex.pm (Elixir/Erlang)
* [www.hex.pm](http://www.hex.pm)
* cpan.org (Perl CPAN)
* [www.cpan.org](http://www.cpan.org)
* metacpan.org
* [www.metacpan.org](http://www.metacpan.org)
* api.metacpan.org
* cocoapods.org (iOS/macOS)
* [www.cocoapods.org](http://www.cocoapods.org)
* cdn.cocoapods.org
* haskell.org
* [www.haskell.org](http://www.haskell.org)
* hackage.haskell.org
* swift.org
* [www.swift.org](http://www.swift.org)

#### Distribuciones de Linux

* archive.ubuntu.com
* security.ubuntu.com
* ubuntu.com
* [www.ubuntu.com](http://www.ubuntu.com)
* \*.ubuntu.com
* ppa.launchpad.net
* launchpad.net
* [www.launchpad.net](http://www.launchpad.net)

#### Herramientas de desarrollo y plataformas

* dl.k8s.io (Kubernetes)
* pkgs.k8s.io
* k8s.io
* [www.k8s.io](http://www.k8s.io)
* releases.hashicorp.com (HashiCorp)
* apt.releases.hashicorp.com
* rpm.releases.hashicorp.com
* archive.releases.hashicorp.com
* hashicorp.com
* [www.hashicorp.com](http://www.hashicorp.com)
* repo.anaconda.com (Anaconda/Conda)
* conda.anaconda.org
* anaconda.org
* [www.anaconda.com](http://www.anaconda.com)
* anaconda.com
* continuum.io
* apache.org (Apache)
* [www.apache.org](http://www.apache.org)
* archive.apache.org
* downloads.apache.org
* eclipse.org (Eclipse)
* [www.eclipse.org](http://www.eclipse.org)
* download.eclipse.org
* nodejs.org (Node.js)
* [www.nodejs.org](http://www.nodejs.org)

#### Servicios en la nube y monitoreo

* statsig.com
* [www.statsig.com](http://www.statsig.com)
* api.statsig.com
* sentry.io
* \*.sentry.io
* http-intake.logs.datadoghq.com
* \*.datadoghq.com
* \*.datadoghq.eu

#### Entrega de contenido y espejos

* sourceforge.net
* \*.sourceforge.net
* packagecloud.io
* \*.packagecloud.io

#### Esquema y configuración

* json-schema.org
* [www.json-schema.org](http://www.json-schema.org)
* json.schemastore.org
* [www.schemastore.org](http://www.schemastore.org)

#### Protocolo de contexto de modelo

* \*.modelcontextprotocol.io

<Note>
  Los dominios marcados con `*` indican coincidencia de subdominio comodín. Por ejemplo, `*.gcr.io` permite acceso a cualquier subdominio de `gcr.io`.
</Note>

### Mejores prácticas de seguridad para acceso a la red personalizado

1. **Principio de menor privilegio**: Solo habilite el acceso a la red mínimo requerido
2. **Audite regularmente**: Revise los dominios permitidos periódicamente
3. **Use HTTPS**: Siempre prefiera puntos finales HTTPS sobre HTTP

## Seguridad y aislamiento

Claude Code en la web proporciona garantías de seguridad sólidas:

* **Máquinas virtuales aisladas**: Cada sesión se ejecuta en una VM aislada administrada por Anthropic
* **Controles de acceso a la red**: El acceso a la red es limitado de forma predeterminada y puede deshabilitarse

<Note>
  Cuando se ejecuta con acceso a la red deshabilitado, Claude Code puede comunicarse con la API de Anthropic, lo que aún puede permitir que los datos salgan de la VM aislada de Claude Code.
</Note>

* **Protección de credenciales**: Las credenciales sensibles (como credenciales de git o claves de firma) nunca están dentro del sandbox con Claude Code. La autenticación se maneja a través de un proxy seguro usando credenciales de alcance
* **Análisis seguro**: El código se analiza y modifica dentro de VMs aisladas antes de crear PRs

## Precios y límites de velocidad

Claude Code en la web comparte límites de velocidad con todo otro uso de Claude y Claude Code dentro de su cuenta. Ejecutar múltiples tareas en paralelo consumirá más límites de velocidad proporcionalmente.

## Limitaciones

* **Autenticación de repositorio**: Solo puede mover sesiones de web a local cuando está autenticado en la misma cuenta
* **Restricciones de plataforma**: Claude Code en la web solo funciona con código alojado en GitHub. Las instancias de [GitHub Enterprise Server](/es/github-enterprise-server) autohospedadas son compatibles con planes de Teams y Enterprise. GitLab y otros repositorios que no sean GitHub no se pueden usar con sesiones en la nube

## Mejores prácticas

1. **Automatice la configuración del entorno**: Use [scripts de configuración](#setup-scripts) para instalar dependencias y configurar herramientas antes de que se lance Claude Code. Para escenarios más avanzados, configure [hooks SessionStart](/es/hooks#sessionstart).
2. **Documente los requisitos**: Especifique claramente las dependencias y comandos en su archivo `CLAUDE.md`. Si tiene un archivo `AGENTS.md`, puede obtenerlo en su `CLAUDE.md` usando `@AGENTS.md` para mantener una única fuente de verdad.

## Recursos relacionados

* [Configuración de hooks](/es/hooks)
* [Referencia de configuración](/es/settings)
* [Seguridad](/es/security)
* [Uso de datos](/es/data-usage)
