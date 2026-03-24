> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Cómo Claude recuerda su proyecto

> Proporcione a Claude instrucciones persistentes con archivos CLAUDE.md, y permita que Claude acumule aprendizajes automáticamente con auto memory.

Cada sesión de Claude Code comienza con una ventana de contexto nueva. Dos mecanismos llevan el conocimiento entre sesiones:

* **Archivos CLAUDE.md**: instrucciones que usted escribe para dar a Claude contexto persistente
* **Auto memory**: notas que Claude escribe por sí mismo basadas en sus correcciones y preferencias

Esta página cubre cómo:

* [Escribir y organizar archivos CLAUDE.md](#claudemd-files)
* [Limitar reglas a tipos de archivo específicos](#organize-rules-with-clauderules) con `.claude/rules/`
* [Configurar auto memory](#auto-memory) para que Claude tome notas automáticamente
* [Solucionar problemas](#troubleshoot-memory-issues) cuando las instrucciones no se siguen

## CLAUDE.md vs auto memory

Claude Code tiene dos sistemas de memoria complementarios. Ambos se cargan al inicio de cada conversación. Claude los trata como contexto, no como configuración forzada. Cuanto más específicas y concisas sean sus instrucciones, más consistentemente Claude las seguirá.

|                      | Archivos CLAUDE.md                                                       | Auto memory                                                                          |
| :------------------- | :----------------------------------------------------------------------- | :----------------------------------------------------------------------------------- |
| **Quién lo escribe** | Usted                                                                    | Claude                                                                               |
| **Qué contiene**     | Instrucciones y reglas                                                   | Aprendizajes y patrones                                                              |
| **Alcance**          | Proyecto, usuario u organización                                         | Por worktree                                                                         |
| **Se carga en**      | Cada sesión                                                              | Cada sesión (primeras 200 líneas)                                                    |
| **Usar para**        | Estándares de codificación, flujos de trabajo, arquitectura del proyecto | Comandos de compilación, información de depuración, preferencias que Claude descubre |

Use archivos CLAUDE.md cuando quiera guiar el comportamiento de Claude. Auto memory permite que Claude aprenda de sus correcciones sin esfuerzo manual.

Los subagents también pueden mantener su propia auto memory. Consulte [configuración de subagent](/es/sub-agents#enable-persistent-memory) para obtener detalles.

## Archivos CLAUDE.md

Los archivos CLAUDE.md son archivos markdown que dan a Claude instrucciones persistentes para un proyecto, su flujo de trabajo personal o toda su organización. Usted escribe estos archivos en texto plano; Claude los lee al inicio de cada sesión.

### Elija dónde colocar los archivos CLAUDE.md

Los archivos CLAUDE.md pueden vivir en varios lugares, cada uno con un alcance diferente. Las ubicaciones más específicas tienen prioridad sobre las más amplias.

| Alcance                        | Ubicación                                                                                                                                                             | Propósito                                                       | Ejemplos de casos de uso                                                                     | Compartido con                                        |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| **Política gestionada**        | • macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`<br />• Linux y WSL: `/etc/claude-code/CLAUDE.md`<br />• Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` | Instrucciones de toda la organización gestionadas por TI/DevOps | Estándares de codificación de la empresa, políticas de seguridad, requisitos de cumplimiento | Todos los usuarios de la organización                 |
| **Instrucciones del proyecto** | `./CLAUDE.md` o `./.claude/CLAUDE.md`                                                                                                                                 | Instrucciones compartidas por el equipo para el proyecto        | Arquitectura del proyecto, estándares de codificación, flujos de trabajo comunes             | Miembros del equipo a través del control de versiones |
| **Instrucciones del usuario**  | `~/.claude/CLAUDE.md`                                                                                                                                                 | Preferencias personales para todos los proyectos                | Preferencias de estilo de código, atajos de herramientas personales                          | Solo usted (todos los proyectos)                      |

Los archivos CLAUDE.md en la jerarquía de directorios por encima del directorio de trabajo se cargan completamente al iniciar. Los archivos CLAUDE.md en subdirectorios se cargan bajo demanda cuando Claude lee archivos en esos directorios. Consulte [Cómo se cargan los archivos CLAUDE.md](#how-claudemd-files-load) para el orden de resolución completo.

Para proyectos grandes, puede dividir las instrucciones en archivos específicos de temas usando [reglas de proyecto](#organize-rules-with-clauderules). Las reglas le permiten limitar las instrucciones a tipos de archivo específicos o subdirectorios.

### Configure un CLAUDE.md de proyecto

Un CLAUDE.md de proyecto puede almacenarse en `./CLAUDE.md` o `./.claude/CLAUDE.md`. Cree este archivo y agregue instrucciones que se apliquen a cualquiera que trabaje en el proyecto: comandos de compilación y prueba, estándares de codificación, decisiones arquitectónicas, convenciones de nomenclatura y flujos de trabajo comunes. Estas instrucciones se comparten con su equipo a través del control de versiones, así que enfóquese en estándares a nivel de proyecto en lugar de preferencias personales.

<Tip>
  Ejecute `/init` para generar un CLAUDE.md inicial automáticamente. Claude analiza su base de código y crea un archivo con comandos de compilación, instrucciones de prueba y convenciones de proyecto que descubre. Si ya existe un CLAUDE.md, `/init` sugiere mejoras en lugar de sobrescribirlo. Refine desde allí con instrucciones que Claude no descubriría por sí solo.
</Tip>

### Escriba instrucciones efectivas

Los archivos CLAUDE.md se cargan en la ventana de contexto al inicio de cada sesión, consumiendo tokens junto con su conversación. Debido a que son contexto en lugar de configuración forzada, cómo escribe las instrucciones afecta qué tan confiablemente Claude las sigue. Las instrucciones específicas, concisas y bien estructuradas funcionan mejor.

**Tamaño**: apunte a menos de 200 líneas por archivo CLAUDE.md. Los archivos más largos consumen más contexto y reducen la adherencia. Si sus instrucciones están creciendo mucho, divídalas usando [importaciones](#import-additional-files) o archivos [`.claude/rules/`](#organize-rules-with-clauderules).

**Estructura**: use encabezados y viñetas de markdown para agrupar instrucciones relacionadas. Claude escanea la estructura de la misma manera que los lectores: las secciones organizadas son más fáciles de seguir que los párrafos densos.

**Especificidad**: escriba instrucciones que sean lo suficientemente concretas para verificar. Por ejemplo:

* "Usar indentación de 2 espacios" en lugar de "Formatear código correctamente"
* "Ejecutar `npm test` antes de hacer commit" en lugar de "Probar sus cambios"
* "Los controladores de API viven en `src/api/handlers/`" en lugar de "Mantener los archivos organizados"

**Consistencia**: si dos reglas se contradicen entre sí, Claude puede elegir una arbitrariamente. Revise sus archivos CLAUDE.md, archivos CLAUDE.md anidados en subdirectorios y archivos [`.claude/rules/`](#organize-rules-with-clauderules) periódicamente para eliminar instrucciones desactualizadas o conflictivas. En monorepos, use [`claudeMdExcludes`](#exclude-specific-claudemd-files) para omitir archivos CLAUDE.md de otros equipos que no sean relevantes para su trabajo.

### Importar archivos adicionales

Los archivos CLAUDE.md pueden importar archivos adicionales usando la sintaxis `@path/to/import`. Los archivos importados se expanden y se cargan en contexto al iniciar junto con el CLAUDE.md que los referencia.

Se permiten rutas relativas y absolutas. Las rutas relativas se resuelven en relación con el archivo que contiene la importación, no con el directorio de trabajo. Los archivos importados pueden importar recursivamente otros archivos, con una profundidad máxima de cinco saltos.

Para incluir un README, package.json y una guía de flujo de trabajo, haga referencia a ellos con la sintaxis `@` en cualquier lugar de su CLAUDE.md:

```text  theme={null}
Consulte @README para obtener una descripción general del proyecto y @package.json para los comandos npm disponibles para este proyecto.

# Instrucciones adicionales
- flujo de trabajo git @docs/git-instructions.md
```

Para preferencias personales que no desea registrar, importe un archivo desde su directorio de inicio. La importación va en el CLAUDE.md compartido, pero el archivo al que apunta permanece en su máquina:

```text  theme={null}
# Preferencias individuales
- @~/.claude/my-project-instructions.md
```

<Warning>
  La primera vez que Claude Code encuentra importaciones externas en un proyecto, muestra un diálogo de aprobación que enumera los archivos. Si rechaza, las importaciones permanecen deshabilitadas y el diálogo no aparece nuevamente.
</Warning>

Para un enfoque más estructurado para organizar instrucciones, consulte [`.claude/rules/`](#organize-rules-with-clauderules).

### Cómo se cargan los archivos CLAUDE.md

Claude Code lee los archivos CLAUDE.md caminando hacia arriba en el árbol de directorios desde su directorio de trabajo actual, verificando cada directorio en el camino. Esto significa que si ejecuta Claude Code en `foo/bar/`, carga instrucciones tanto de `foo/bar/CLAUDE.md` como de `foo/CLAUDE.md`.

Claude también descubre archivos CLAUDE.md en subdirectorios bajo su directorio de trabajo actual. En lugar de cargarlos al iniciar, se incluyen cuando Claude lee archivos en esos subdirectorios.

Si trabaja en un monorepo grande donde se recogen archivos CLAUDE.md de otros equipos, use [`claudeMdExcludes`](#exclude-specific-claudemd-files) para omitirlos.

#### Cargar desde directorios adicionales

La bandera `--add-dir` da a Claude acceso a directorios adicionales fuera de su directorio de trabajo principal. De forma predeterminada, los archivos CLAUDE.md de estos directorios no se cargan.

Para cargar también archivos CLAUDE.md de directorios adicionales, incluyendo `CLAUDE.md`, `.claude/CLAUDE.md` y `.claude/rules/*.md`, establezca la variable de entorno `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD`:

```bash  theme={null}
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config
```

### Organizar reglas con `.claude/rules/`

Para proyectos más grandes, puede organizar instrucciones en múltiples archivos usando el directorio `.claude/rules/`. Esto mantiene las instrucciones modulares y más fáciles de mantener para los equipos. Las reglas también pueden ser [limitadas a rutas de archivo específicas](#path-specific-rules), por lo que solo se cargan en contexto cuando Claude trabaja con archivos coincidentes, reduciendo ruido y ahorrando espacio de contexto.

<Note>
  Las reglas se cargan en contexto cada sesión o cuando se abren archivos coincidentes. Para instrucciones específicas de tareas que no necesitan estar en contexto todo el tiempo, use [skills](/es/skills) en su lugar, que solo se cargan cuando las invoca o cuando Claude determina que son relevantes para su prompt.
</Note>

#### Configurar reglas

Coloque archivos markdown en el directorio `.claude/rules/` de su proyecto. Cada archivo debe cubrir un tema, con un nombre de archivo descriptivo como `testing.md` o `api-design.md`. Todos los archivos `.md` se descubren recursivamente, por lo que puede organizar reglas en subdirectorios como `frontend/` o `backend/`:

```text  theme={null}
your-project/
├── .claude/
│   ├── CLAUDE.md           # Instrucciones principales del proyecto
│   └── rules/
│       ├── code-style.md   # Directrices de estilo de código
│       ├── testing.md      # Convenciones de prueba
│       └── security.md     # Requisitos de seguridad
```

Las reglas sin [frontmatter `paths`](#path-specific-rules) se cargan al iniciar con la misma prioridad que `.claude/CLAUDE.md`.

#### Reglas específicas de ruta

Las reglas pueden limitarse a archivos específicos usando frontmatter YAML con el campo `paths`. Estas reglas condicionales solo se aplican cuando Claude trabaja con archivos que coinciden con los patrones especificados.

```markdown  theme={null}
---
paths:
  - "src/api/**/*.ts"
---

# Reglas de desarrollo de API

- Todos los puntos finales de API deben incluir validación de entrada
- Usar el formato de respuesta de error estándar
- Incluir comentarios de documentación OpenAPI
```

Las reglas sin un campo `paths` se cargan incondicionalmente y se aplican a todos los archivos. Las reglas con alcance de ruta se activan cuando Claude lee archivos que coinciden con el patrón, no en cada uso de herramienta.

Use patrones glob en el campo `paths` para hacer coincidir archivos por extensión, directorio o cualquier combinación:

| Patrón                 | Coincide con                                          |
| ---------------------- | ----------------------------------------------------- |
| `**/*.ts`              | Todos los archivos TypeScript en cualquier directorio |
| `src/**/*`             | Todos los archivos bajo el directorio `src/`          |
| `*.md`                 | Archivos Markdown en la raíz del proyecto             |
| `src/components/*.tsx` | Componentes React en un directorio específico         |

Puede especificar múltiples patrones y usar expansión de llaves para hacer coincidir múltiples extensiones en un patrón:

```markdown  theme={null}
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---
```

#### Compartir reglas entre proyectos con enlaces simbólicos

El directorio `.claude/rules/` admite enlaces simbólicos, por lo que puede mantener un conjunto compartido de reglas y vincularlas en múltiples proyectos. Los enlaces simbólicos se resuelven y se cargan normalmente, y los enlaces simbólicos circulares se detectan y se manejan correctamente.

Este ejemplo vincula tanto un directorio compartido como un archivo individual:

```bash  theme={null}
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

#### Reglas a nivel de usuario

Las reglas personales en `~/.claude/rules/` se aplican a cada proyecto en su máquina. Úselas para preferencias que no son específicas del proyecto:

```text  theme={null}
~/.claude/rules/
├── preferences.md    # Sus preferencias personales de codificación
└── workflows.md      # Sus flujos de trabajo preferidos
```

Las reglas a nivel de usuario se cargan antes que las reglas del proyecto, dando a las reglas del proyecto mayor prioridad.

### Gestionar CLAUDE.md para equipos grandes

Para organizaciones que implementan Claude Code en equipos, puede centralizar instrucciones y controlar qué archivos CLAUDE.md se cargan.

#### Implementar CLAUDE.md en toda la organización

Las organizaciones pueden implementar un CLAUDE.md gestionado centralmente que se aplique a todos los usuarios en una máquina. Este archivo no puede ser excluido por configuraciones individuales.

<Steps>
  <Step title="Crear el archivo en la ubicación de política gestionada">
    * macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
    * Linux y WSL: `/etc/claude-code/CLAUDE.md`
    * Windows: `C:\Program Files\ClaudeCode\CLAUDE.md`
  </Step>

  <Step title="Implementar con su sistema de gestión de configuración">
    Use MDM, Group Policy, Ansible o herramientas similares para distribuir el archivo en máquinas de desarrolladores. Consulte [configuración gestionada](/es/permissions#managed-settings) para otras opciones de configuración de toda la organización.
  </Step>
</Steps>

#### Excluir archivos CLAUDE.md específicos

En monorepos grandes, los archivos CLAUDE.md ancestros pueden contener instrucciones que no son relevantes para su trabajo. La configuración `claudeMdExcludes` le permite omitir archivos específicos por ruta o patrón glob.

Este ejemplo excluye un CLAUDE.md de nivel superior y un directorio de reglas de una carpeta principal. Agréguelo a `.claude/settings.local.json` para que la exclusión permanezca local en su máquina:

```json  theme={null}
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

Los patrones se comparan contra rutas de archivo absolutas usando sintaxis glob. Puede configurar `claudeMdExcludes` en cualquier [capa de configuración](/es/settings#settings-files): usuario, proyecto, local o política gestionada. Los arrays se fusionan entre capas.

Los archivos CLAUDE.md de política gestionada no pueden ser excluidos. Esto asegura que las instrucciones de toda la organización siempre se apliquen independientemente de la configuración individual.

## Auto memory

Auto memory permite que Claude acumule conocimiento entre sesiones sin que usted escriba nada. Claude guarda notas para sí mismo mientras trabaja: comandos de compilación, información de depuración, notas de arquitectura, preferencias de estilo de código y hábitos de flujo de trabajo. Claude no guarda algo cada sesión. Decide qué vale la pena recordar basándose en si la información sería útil en una conversación futura.

<Note>
  Auto memory requiere Claude Code v2.1.59 o posterior. Verifique su versión con `claude --version`.
</Note>

### Habilitar o deshabilitar auto memory

Auto memory está habilitado de forma predeterminada. Para alternarlo, abra `/memory` en una sesión y use el botón de alternancia de auto memory, o establezca `autoMemoryEnabled` en la configuración de su proyecto:

```json  theme={null}
{
  "autoMemoryEnabled": false
}
```

Para deshabilitar auto memory a través de variable de entorno, establezca `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.

### Ubicación de almacenamiento

Cada proyecto obtiene su propio directorio de memoria en `~/.claude/projects/<project>/memory/`. La ruta `<project>` se deriva del repositorio git, por lo que todos los worktrees y subdirectorios dentro del mismo repositorio comparten un directorio de auto memory. Fuera de un repositorio git, se usa la raíz del proyecto en su lugar.

Para almacenar auto memory en una ubicación diferente, establezca `autoMemoryDirectory` en la configuración de usuario o local:

```json  theme={null}
{
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}
```

Esta configuración se acepta desde la política, local y configuración de usuario. No se acepta desde la configuración del proyecto (`.claude/settings.json`) para evitar que un proyecto compartido redirija escrituras de auto memory a ubicaciones sensibles.

El directorio contiene un punto de entrada `MEMORY.md` y archivos de tema opcionales:

```text  theme={null}
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Índice conciso, cargado en cada sesión
├── debugging.md       # Notas detalladas sobre patrones de depuración
├── api-conventions.md # Decisiones de diseño de API
└── ...                # Cualquier otro archivo de tema que Claude cree
```

`MEMORY.md` actúa como un índice del directorio de memoria. Claude lee y escribe archivos en este directorio durante su sesión, usando `MEMORY.md` para mantener un registro de lo que se almacena dónde.

Auto memory es local de la máquina. Todos los worktrees y subdirectorios dentro del mismo repositorio git comparten un directorio de auto memory. Los archivos no se comparten entre máquinas o entornos en la nube.

### Cómo funciona

Las primeras 200 líneas de `MEMORY.md` se cargan al inicio de cada conversación. El contenido más allá de la línea 200 no se carga al inicio de la sesión. Claude mantiene `MEMORY.md` conciso moviendo notas detalladas a archivos de tema separados.

Este límite de 200 líneas se aplica solo a `MEMORY.md`. Los archivos CLAUDE.md se cargan completamente independientemente de la longitud, aunque los archivos más cortos producen mejor adherencia.

Los archivos de tema como `debugging.md` o `patterns.md` no se cargan al iniciar. Claude los lee bajo demanda usando sus herramientas de archivo estándar cuando necesita la información.

Claude lee y escribe archivos de memoria durante su sesión. Cuando ve "Writing memory" o "Recalled memory" en la interfaz de Claude Code, Claude está actualizando o leyendo activamente desde `~/.claude/projects/<project>/memory/`.

### Auditar y editar su memoria

Los archivos de auto memory son markdown plano que puede editar o eliminar en cualquier momento. Ejecute [`/memory`](#view-and-edit-with-memory) para examinar y abrir archivos de memoria desde dentro de una sesión.

## Ver y editar con `/memory`

El comando `/memory` enumera todos los archivos CLAUDE.md y rules cargados en su sesión actual, le permite alternar auto memory activado o desactivado, y proporciona un enlace para abrir la carpeta de auto memory. Seleccione cualquier archivo para abrirlo en su editor.

Cuando le pide a Claude que recuerde algo, como "siempre usar pnpm, no npm" o "recuerde que las pruebas de API requieren una instancia local de Redis", Claude lo guarda en auto memory. Para agregar instrucciones a CLAUDE.md en su lugar, pídale a Claude directamente, como "agregue esto a CLAUDE.md", o edite el archivo usted mismo a través de `/memory`.

## Solucionar problemas de memoria

Estos son los problemas más comunes con CLAUDE.md y auto memory, junto con pasos para depurarlos.

### Claude no está siguiendo mi CLAUDE.md

El contenido de CLAUDE.md se entrega como un mensaje de usuario después del prompt del sistema, no como parte del prompt del sistema en sí. Claude lo lee e intenta seguirlo, pero no hay garantía de cumplimiento estricto, especialmente para instrucciones vagas o conflictivas.

Para depurar:

* Ejecute `/memory` para verificar que sus archivos CLAUDE.md se están cargando. Si un archivo no aparece en la lista, Claude no puede verlo.
* Verifique que el CLAUDE.md relevante esté en una ubicación que se cargue para su sesión (consulte [Elija dónde colocar los archivos CLAUDE.md](#choose-where-to-put-claudemd-files)).
* Haga instrucciones más específicas. "Usar indentación de 2 espacios" funciona mejor que "formatear código bien".
* Busque instrucciones conflictivas en archivos CLAUDE.md. Si dos archivos dan orientación diferente para el mismo comportamiento, Claude puede elegir uno arbitrariamente.

Para instrucciones que desea a nivel de prompt del sistema, use [`--append-system-prompt`](/es/cli-reference#system-prompt-flags). Esto debe pasarse en cada invocación, por lo que es más adecuado para scripts y automatización que para uso interactivo.

<Tip>
  Use el hook [`InstructionsLoaded`](/es/hooks#instructionsloaded) para registrar exactamente qué archivos de instrucciones se cargan, cuándo se cargan y por qué. Esto es útil para depurar reglas específicas de ruta o archivos cargados perezosamente en subdirectorios.
</Tip>

### No sé qué guardó auto memory

Ejecute `/memory` y seleccione la carpeta de auto memory para examinar lo que Claude ha guardado. Todo es markdown plano que puede leer, editar o eliminar.

### Mi CLAUDE.md es demasiado grande

Los archivos de más de 200 líneas consumen más contexto y pueden reducir la adherencia. Mueva contenido detallado a archivos separados referenciados con importaciones `@path` (consulte [Importar archivos adicionales](#import-additional-files)), o divida sus instrucciones entre archivos `.claude/rules/`.

### Las instrucciones parecen perdidas después de `/compact`

CLAUDE.md sobrevive completamente a la compactación. Después de `/compact`, Claude vuelve a leer su CLAUDE.md desde el disco e lo reinyecta fresco en la sesión. Si una instrucción desapareció después de la compactación, se dio solo en la conversación, no se escribió en CLAUDE.md. Agréguelo a CLAUDE.md para que persista entre sesiones.

Consulte [Escriba instrucciones efectivas](#write-effective-instructions) para obtener orientación sobre tamaño, estructura y especificidad.

## Recursos relacionados

* [Skills](/es/skills): empaquetar flujos de trabajo repetibles que se cargan bajo demanda
* [Settings](/es/settings): configurar el comportamiento de Claude Code con archivos de configuración
* [Manage sessions](/es/sessions): gestionar contexto, reanudar conversaciones y ejecutar sesiones paralelas
* [Subagent memory](/es/sub-agents#enable-persistent-memory): permitir que los subagents mantengan su propia auto memory
