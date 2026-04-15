> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Mejores prácticas para Claude Code

> Consejos y patrones para aprovechar al máximo Claude Code, desde configurar su entorno hasta escalar entre sesiones paralelas.

Claude Code es un entorno de codificación agencial. A diferencia de un chatbot que responde preguntas y espera, Claude Code puede leer sus archivos, ejecutar comandos, hacer cambios y trabajar autónomamente a través de problemas mientras usted observa, redirige o se aleja completamente.

Esto cambia cómo trabaja. En lugar de escribir código usted mismo y pedirle a Claude que lo revise, describe lo que desea y Claude descubre cómo construirlo. Claude explora, planifica e implementa.

Pero esta autonomía aún viene con una curva de aprendizaje. Claude trabaja dentro de ciertas restricciones que necesita entender.

Esta guía cubre patrones que han demostrado ser efectivos en los equipos internos de Anthropic y para ingenieros que usan Claude Code en varios códigos base, lenguajes y entornos. Para saber cómo funciona el bucle agencial bajo el capó, consulte [Cómo funciona Claude Code](/es/how-claude-code-works).

***

La mayoría de las mejores prácticas se basan en una restricción: la ventana de contexto de Claude se llena rápidamente y el rendimiento se degrada a medida que se llena.

La ventana de contexto de Claude contiene toda su conversación, incluido cada mensaje, cada archivo que Claude lee y cada salida de comando. Sin embargo, esto puede llenarse rápidamente. Una única sesión de depuración o exploración de código base podría generar y consumir decenas de miles de tokens.

Esto importa porque el rendimiento del LLM se degrada a medida que se llena el contexto. Cuando la ventana de contexto se está llenando, Claude puede comenzar a "olvidar" instrucciones anteriores o cometer más errores. La ventana de contexto es el recurso más importante a gestionar. Rastree el uso de contexto continuamente con una [línea de estado personalizada](/es/statusline), y consulte [Reducir el uso de tokens](/es/costs#reduce-token-usage) para estrategias sobre cómo reducir el uso de tokens.

***

## Dé a Claude una forma de verificar su trabajo

<Tip>
  Incluya pruebas, capturas de pantalla o salidas esperadas para que Claude pueda verificarse a sí mismo. Esta es la cosa de mayor apalancamiento que puede hacer.
</Tip>

Claude funciona dramáticamente mejor cuando puede verificar su propio trabajo, como ejecutar pruebas, comparar capturas de pantalla y validar salidas.

Sin criterios de éxito claros, podría producir algo que se vea bien pero que en realidad no funcione. Usted se convierte en el único bucle de retroalimentación, y cada error requiere su atención.

| Estrategia                                 | Antes                                                                    | Después                                                                                                                                                                                                                              |
| ------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Proporcionar criterios de verificación** | *"implementar una función que valide direcciones de correo electrónico"* | *"escribir una función validateEmail. casos de prueba de ejemplo: [user@example.com](mailto:user@example.com) es verdadero, inválido es falso, [user@.com](mailto:user@.com) es falso. ejecutar las pruebas después de implementar"* |
| **Verificar cambios de UI visualmente**    | *"hacer que el panel de control se vea mejor"*                           | *"\[pegar captura de pantalla] implementar este diseño. tomar una captura de pantalla del resultado y compararla con la original. listar diferencias y corregirlas"*                                                                 |
| **Abordar causas raíz, no síntomas**       | *"la compilación está fallando"*                                         | *"la compilación falla con este error: \[pegar error]. corregirlo y verificar que la compilación tenga éxito. abordar la causa raíz, no suprimir el error"*                                                                          |

Los cambios de UI se pueden verificar usando la [extensión Claude en Chrome](/es/chrome). Abre nuevas pestañas en su navegador, prueba la UI e itera hasta que el código funcione.

Su verificación también puede ser un conjunto de pruebas, un linter o un comando Bash que verifique la salida. Invierta en hacer que su verificación sea sólida.

***

## Explore primero, luego planifique, luego codifique

<Tip>
  Separe la investigación y la planificación de la implementación para evitar resolver el problema incorrecto.
</Tip>

Dejar que Claude salte directamente a la codificación puede producir código que resuelve el problema incorrecto. Use [Plan Mode](/es/common-workflows#use-plan-mode-for-safe-code-analysis) para separar la exploración de la ejecución.

El flujo de trabajo recomendado tiene cuatro fases:

<Steps>
  <Step title="Explorar">
    Ingrese Plan Mode. Claude lee archivos y responde preguntas sin hacer cambios.

    ```txt claude (Plan Mode) theme={null}
    read /src/auth and understand how we handle sessions and login.
    also look at how we manage environment variables for secrets.
    ```
  </Step>

  <Step title="Planificar">
    Pida a Claude que cree un plan de implementación detallado.

    ```txt claude (Plan Mode) theme={null}
    I want to add Google OAuth. What files need to change?
    What's the session flow? Create a plan.
    ```

    Presione `Ctrl+G` para abrir el plan en su editor de texto para edición directa antes de que Claude continúe.
  </Step>

  <Step title="Implementar">
    Vuelva al Modo Normal y deje que Claude codifique, verificando contra su plan.

    ```txt claude (Normal Mode) theme={null}
    implement the OAuth flow from your plan. write tests for the
    callback handler, run the test suite and fix any failures.
    ```
  </Step>

  <Step title="Confirmar">
    Pida a Claude que confirme con un mensaje descriptivo y cree un PR.

    ```txt claude (Normal Mode) theme={null}
    commit with a descriptive message and open a PR
    ```
  </Step>
</Steps>

<Callout>
  Plan Mode es útil, pero también agrega sobrecarga.

  Para tareas donde el alcance es claro y la corrección es pequeña (como corregir un error tipográfico, agregar una línea de registro o renombrar una variable) pida a Claude que lo haga directamente.

  La planificación es más útil cuando no está seguro del enfoque, cuando el cambio modifica múltiples archivos o cuando no está familiarizado con el código que se está modificando. Si pudiera describir el diff en una oración, omita el plan.
</Callout>

***

## Proporcione contexto específico en sus indicaciones

<Tip>
  Cuanto más precisas sean sus instrucciones, menos correcciones necesitará.
</Tip>

Claude puede inferir intención, pero no puede leer su mente. Haga referencia a archivos específicos, mencione restricciones y señale patrones de ejemplo.

| Estrategia                                                                                           | Antes                                                    | Después                                                                                                                                                                                                                                                                                                                                                                                       |
| ---------------------------------------------------------------------------------------------------- | -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Delimitar la tarea.** Especifique qué archivo, qué escenario y preferencias de prueba.             | *"agregar pruebas para foo.py"*                          | *"escribir una prueba para foo.py cubriendo el caso extremo donde el usuario ha cerrado sesión. evitar mocks."*                                                                                                                                                                                                                                                                               |
| **Señalar fuentes.** Dirija a Claude a la fuente que puede responder una pregunta.                   | *"¿por qué ExecutionFactory tiene una API tan extraña?"* | *"revisar el historial de git de ExecutionFactory y resumir cómo su API llegó a ser así"*                                                                                                                                                                                                                                                                                                     |
| **Hacer referencia a patrones existentes.** Señale a Claude los patrones en su código base.          | *"agregar un widget de calendario"*                      | *"ver cómo se implementan los widgets existentes en la página de inicio para entender los patrones. HotDogWidget.php es un buen ejemplo. seguir el patrón para implementar un nuevo widget de calendario que permita al usuario seleccionar un mes y paginar hacia adelante/atrás para elegir un año. construir desde cero sin bibliotecas que no sean las ya utilizadas en el código base."* |
| **Describir el síntoma.** Proporcione el síntoma, la ubicación probable y qué significa "corregido". | *"corregir el error de inicio de sesión"*                | *"los usuarios informan que el inicio de sesión falla después del agotamiento de la sesión. verificar el flujo de autenticación en src/auth/, especialmente la actualización de tokens. escribir una prueba fallida que reproduzca el problema, luego corregirlo"*                                                                                                                            |

Los indicaciones vagas pueden ser útiles cuando está explorando y puede permitirse corregir el curso. Una indicación como `"¿qué mejoraría en este archivo?"` puede revelar cosas en las que no habría pensado en preguntar.

### Proporcionar contenido enriquecido

<Tip>
  Use `@` para hacer referencia a archivos, pegue capturas de pantalla/imágenes o canalice datos directamente.
</Tip>

Puede proporcionar datos enriquecidos a Claude de varias maneras:

* **Haga referencia a archivos con `@`** en lugar de describir dónde vive el código. Claude lee el archivo antes de responder.
* **Pegue imágenes directamente**. Copie/pegue o arrastre y suelte imágenes en la indicación.
* **Proporcione URLs** para documentación y referencias de API. Use `/permissions` para permitir dominios de uso frecuente.
* **Canalice datos** ejecutando `cat error.log | claude` para enviar contenidos de archivo directamente.
* **Deje que Claude obtenga lo que necesita**. Diga a Claude que extraiga contexto por sí mismo usando comandos Bash, herramientas MCP o leyendo archivos.

***

## Configure su entorno

Algunos pasos de configuración hacen que Claude Code sea significativamente más efectivo en todas sus sesiones. Para una descripción general completa de las características de extensión y cuándo usar cada una, consulte [Extender Claude Code](/es/features-overview).

### Escriba un CLAUDE.md efectivo

<Tip>
  Ejecute `/init` para generar un archivo CLAUDE.md inicial basado en la estructura de su proyecto actual, luego refine con el tiempo.
</Tip>

CLAUDE.md es un archivo especial que Claude lee al inicio de cada conversación. Incluya comandos Bash, estilo de código y reglas de flujo de trabajo. Esto le da a Claude contexto persistente que no puede inferir solo del código.

El comando `/init` analiza su código base para detectar sistemas de compilación, marcos de prueba y patrones de código, dándole una base sólida para refinar.

No hay un formato requerido para archivos CLAUDE.md, pero manténgalo corto y legible por humanos. Por ejemplo:

```markdown CLAUDE.md theme={null}
# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible (eg. import { foo } from 'bar')

# Workflow
- Be sure to typecheck when you're done making a series of code changes
- Prefer running single tests, and not the whole test suite, for performance
```

CLAUDE.md se carga cada sesión, así que solo incluya cosas que se apliquen ampliamente. Para conocimiento de dominio o flujos de trabajo que solo son relevantes a veces, use [skills](/es/skills) en su lugar. Claude los carga bajo demanda sin inflar cada conversación.

Manténgalo conciso. Para cada línea, pregúntese: *"¿Causaría que Claude cometiera errores si elimino esto?"* Si no, elimínelo. Los archivos CLAUDE.md inflados hacen que Claude ignore sus instrucciones reales.

| ✅ Incluir                                                                  | ❌ Excluir                                                        |
| -------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| Comandos Bash que Claude no puede adivinar                                 | Cualquier cosa que Claude pueda descubrir leyendo código         |
| Reglas de estilo de código que difieren de los valores predeterminados     | Convenciones de lenguaje estándar que Claude ya conoce           |
| Instrucciones de prueba y ejecutores de prueba preferidos                  | Documentación detallada de API (enlace a documentos en su lugar) |
| Etiqueta del repositorio (nomenclatura de rama, convenciones de PR)        | Información que cambia frecuentemente                            |
| Decisiones arquitectónicas específicas de su proyecto                      | Explicaciones largas o tutoriales                                |
| Peculiaridades del entorno de desarrollo (variables de entorno requeridas) | Prácticas evidentes por sí solas como "escribir código limpio"   |
| Errores comunes o comportamientos no obvios                                |                                                                  |

Si Claude sigue haciendo algo que no desea a pesar de tener una regla en su contra, el archivo probablemente sea demasiado largo y la regla se está perdiendo. Si Claude le hace preguntas que se responden en CLAUDE.md, la redacción podría ser ambigua. Trate CLAUDE.md como código: revíselo cuando las cosas salgan mal, elimine regularmente y pruebe cambios observando si el comportamiento de Claude realmente cambia.

Puede ajustar instrucciones agregando énfasis (por ejemplo, "IMPORTANTE" o "DEBE") para mejorar la adherencia. Verifique CLAUDE.md en git para que su equipo pueda contribuir. El archivo se compone en valor con el tiempo.

Los archivos CLAUDE.md pueden importar archivos adicionales usando la sintaxis `@path/to/import`:

```markdown CLAUDE.md theme={null}
See @README.md for project overview and @package.json for available npm commands.

# Additional Instructions
- Git workflow: @docs/git-instructions.md
- Personal overrides: @~/.claude/my-project-instructions.md
```

Puede colocar archivos CLAUDE.md en varias ubicaciones:

* **Carpeta de inicio (`~/.claude/CLAUDE.md`)**: se aplica a todas las sesiones de Claude
* **Raíz del proyecto (`./CLAUDE.md`)**: verificar en git para compartir con su equipo
* **Directorios principales**: útil para monorepos donde tanto `root/CLAUDE.md` como `root/foo/CLAUDE.md` se extraen automáticamente
* **Directorios secundarios**: Claude extrae archivos CLAUDE.md secundarios bajo demanda cuando trabaja con archivos en esos directorios

### Configurar permisos

<Tip>
  Use [modo automático](/es/permission-modes#eliminate-prompts-with-auto-mode) para dejar que un clasificador maneje aprobaciones, `/permissions` para permitir comandos específicos, o `/sandbox` para aislamiento a nivel del SO. Cada uno reduce interrupciones mientras lo mantiene en control.
</Tip>

De forma predeterminada, Claude Code solicita permiso para acciones que podrían modificar su sistema: escrituras de archivo, comandos Bash, herramientas MCP, etc. Esto es seguro pero tedioso. Después de la décima aprobación, realmente no está revisando, solo está haciendo clic. Hay tres formas de reducir estas interrupciones:

* **Modo automático**: un modelo clasificador separado revisa comandos y bloquea solo lo que se ve arriesgado: escalada de alcance, infraestructura desconocida o acciones impulsadas por contenido hostil. Mejor cuando confía en la dirección general de una tarea pero no desea hacer clic en cada paso
* **Listas de permisos**: permitir herramientas específicas que sabe que son seguras, como `npm run lint` o `git commit`
* **Sandboxing**: habilitar aislamiento a nivel del SO que restrinja el acceso al sistema de archivos y red, permitiendo que Claude trabaje más libremente dentro de límites definidos

Lea más sobre [modos de permiso](/es/permission-modes), [reglas de permiso](/es/permissions) y [sandboxing](/es/sandboxing).

### Usar herramientas CLI

<Tip>
  Diga a Claude Code que use herramientas CLI como `gh`, `aws`, `gcloud` y `sentry-cli` cuando interactúe con servicios externos.
</Tip>

Las herramientas CLI son la forma más eficiente en contexto de interactuar con servicios externos. Si usa GitHub, instale la CLI `gh`. Claude sabe cómo usarla para crear problemas, abrir solicitudes de extracción y leer comentarios. Sin `gh`, Claude aún puede usar la API de GitHub, pero las solicitudes no autenticadas a menudo alcanzan límites de velocidad.

Claude también es efectivo en aprender herramientas CLI que no conoce. Intente indicaciones como `Use 'foo-cli-tool --help' to learn about foo tool, then use it to solve A, B, C.`

### Conectar servidores MCP

<Tip>
  Ejecute `claude mcp add` para conectar herramientas externas como Notion, Figma o su base de datos.
</Tip>

Con [servidores MCP](/es/mcp), puede pedir a Claude que implemente características desde rastreadores de problemas, consulte bases de datos, analice datos de monitoreo, integre diseños de Figma y automatice flujos de trabajo.

### Configurar hooks

<Tip>
  Use hooks para acciones que deben suceder cada vez sin excepciones.
</Tip>

[Hooks](/es/hooks-guide) ejecutan scripts automáticamente en puntos específicos del flujo de trabajo de Claude. A diferencia de las instrucciones CLAUDE.md que son consultivas, los hooks son deterministas y garantizan que la acción suceda.

Claude puede escribir hooks para usted. Intente indicaciones como *"Write a hook that runs eslint after every file edit"* o *"Write a hook that blocks writes to the migrations folder."* Edite `.claude/settings.json` directamente para configurar hooks a mano, y ejecute `/hooks` para explorar lo que está configurado.

### Crear skills

<Tip>
  Cree archivos `SKILL.md` en `.claude/skills/` para dar a Claude conocimiento de dominio y flujos de trabajo reutilizables.
</Tip>

[Skills](/es/skills) extienden el conocimiento de Claude con información específica de su proyecto, equipo o dominio. Claude los aplica automáticamente cuando son relevantes, o puede invocarlos directamente con `/skill-name`.

Cree una skill agregando un directorio con un `SKILL.md` a `.claude/skills/`:

```markdown .claude/skills/api-conventions/SKILL.md theme={null}
---
name: api-conventions
description: REST API design conventions for our services
---
# API Conventions
- Use kebab-case for URL paths
- Use camelCase for JSON properties
- Always include pagination for list endpoints
- Version APIs in the URL path (/v1/, /v2/)
```

Las skills también pueden definir flujos de trabajo repetibles que invoca directamente:

```markdown .claude/skills/fix-issue/SKILL.md theme={null}
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---
Analyze and fix the GitHub issue: $ARGUMENTS.

1. Use `gh issue view` to get the issue details
2. Understand the problem described in the issue
3. Search the codebase for relevant files
4. Implement the necessary changes to fix the issue
5. Write and run tests to verify the fix
6. Ensure code passes linting and type checking
7. Create a descriptive commit message
8. Push and create a PR
```

Ejecute `/fix-issue 1234` para invocarlo. Use `disable-model-invocation: true` para flujos de trabajo con efectos secundarios que desea activar manualmente.

### Crear subagents personalizados

<Tip>
  Defina asistentes especializados en `.claude/agents/` que Claude pueda delegar para tareas aisladas.
</Tip>

[Subagents](/es/sub-agents) se ejecutan en su propio contexto con su propio conjunto de herramientas permitidas. Son útiles para tareas que leen muchos archivos o necesitan enfoque especializado sin saturar su conversación principal.

```markdown .claude/agents/security-reviewer.md theme={null}
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
- Insecure data handling

Provide specific line references and suggested fixes.
```

Diga a Claude que use subagents explícitamente: *"Use a subagent to review this code for security issues."*

### Instalar plugins

<Tip>
  Ejecute `/plugin` para explorar el marketplace. Los plugins agregan skills, herramientas e integraciones sin configuración.
</Tip>

[Plugins](/es/plugins) agrupan skills, hooks, subagents y servidores MCP en una única unidad instalable de la comunidad y Anthropic. Si trabaja con un lenguaje tipado, instale un [plugin de inteligencia de código](/es/discover-plugins#code-intelligence) para dar a Claude navegación de símbolos precisa y detección automática de errores después de ediciones.

Para orientación sobre cómo elegir entre skills, subagents, hooks y MCP, consulte [Extender Claude Code](/es/features-overview#match-features-to-your-goal).

***

## Comuníquese efectivamente

La forma en que se comunica con Claude Code impacta significativamente la calidad de los resultados.

### Haga preguntas sobre el código base

<Tip>
  Haga a Claude preguntas que haría a un ingeniero senior.
</Tip>

Al incorporarse a un nuevo código base, use Claude Code para aprender y explorar. Puede hacer a Claude el mismo tipo de preguntas que haría a otro ingeniero:

* ¿Cómo funciona el registro?
* ¿Cómo hago un nuevo punto final de API?
* ¿Qué hace `async move { ... }` en la línea 134 de `foo.rs`?
* ¿Qué casos extremos maneja `CustomerOnboardingFlowImpl`?
* ¿Por qué este código llama a `foo()` en lugar de `bar()` en la línea 333?

Usar Claude Code de esta manera es un flujo de trabajo de incorporación efectivo, mejorando el tiempo de rampa y reduciendo la carga en otros ingenieros. No se requiere indicación especial: haga preguntas directamente.

### Deje que Claude lo entreviste

<Tip>
  Para características más grandes, deje que Claude lo entreviste primero. Comience con una indicación mínima y pida a Claude que lo entreviste usando la herramienta `AskUserQuestion`.
</Tip>

Claude hace preguntas sobre cosas que podría no haber considerado, incluyendo implementación técnica, UI/UX, casos extremos y compensaciones.

```text theme={null}
I want to build [brief description]. Interview me in detail using the AskUserQuestion tool.

Ask about technical implementation, UI/UX, edge cases, concerns, and tradeoffs. Don't ask obvious questions, dig into the hard parts I might not have considered.

Keep interviewing until we've covered everything, then write a complete spec to SPEC.md.
```

Una vez que la especificación esté completa, inicie una sesión nueva para ejecutarla. La nueva sesión tiene contexto limpio enfocado completamente en la implementación, y tiene una especificación escrita para hacer referencia.

***

## Gestione su sesión

Las conversaciones son persistentes y reversibles. ¡Úselo a su favor!

### Corrija el curso temprano y a menudo

<Tip>
  Corrija a Claude tan pronto como note que se desvía del camino.
</Tip>

Los mejores resultados provienen de bucles de retroalimentación ajustados. Aunque Claude ocasionalmente resuelve problemas perfectamente en el primer intento, corregirlo rápidamente generalmente produce mejores soluciones más rápido.

* **`Esc`**: detener a Claude a mitad de acción con la tecla `Esc`. El contexto se preserva, para que pueda redirigir.
* **`Esc + Esc` o `/rewind`**: presione `Esc` dos veces o ejecute `/rewind` para abrir el menú de rebobinado y restaurar la conversación anterior y el estado del código, o resumir desde un mensaje seleccionado.
* **`"Undo that"`**: haga que Claude revierta sus cambios.
* **`/clear`**: restablecer contexto entre tareas no relacionadas. Las sesiones largas con contexto irrelevante pueden reducir el rendimiento.

Si ha corregido a Claude más de dos veces en el mismo problema en una sesión, el contexto está saturado de enfoques fallidos. Ejecute `/clear` e inicie de nuevo con una indicación más específica que incorpore lo que aprendió. Una sesión limpia con una indicación mejor casi siempre supera una sesión larga con correcciones acumuladas.

### Gestione el contexto agresivamente

<Tip>
  Ejecute `/clear` entre tareas no relacionadas para restablecer el contexto.
</Tip>

Claude Code compacta automáticamente el historial de conversación cuando se acerca a los límites de contexto, lo que preserva código importante y decisiones mientras libera espacio.

Durante sesiones largas, la ventana de contexto de Claude puede llenarse con conversación irrelevante, contenidos de archivo y comandos. Esto puede reducir el rendimiento y a veces distraer a Claude.

* Use `/clear` frecuentemente entre tareas para restablecer completamente la ventana de contexto
* Cuando se activa la compactación automática, Claude resume lo que más importa, incluyendo patrones de código, estados de archivo y decisiones clave
* Para más control, ejecute `/compact <instructions>`, como `/compact Focus on the API changes`
* Para compactar solo parte de la conversación, use `Esc + Esc` o `/rewind`, seleccione un punto de control de mensaje y elija **Summarize from here**. Esto condensa mensajes desde ese punto hacia adelante mientras mantiene el contexto anterior intacto.
* Personalice el comportamiento de compactación en CLAUDE.md con instrucciones como `"When compacting, always preserve the full list of modified files and any test commands"` para asegurar que el contexto crítico sobreviva a la resumición
* Para preguntas rápidas que no necesitan permanecer en contexto, use [`/btw`](/es/interactive-mode#side-questions-with-btw). La respuesta aparece en una superposición descaritable y nunca entra en el historial de conversación, para que pueda verificar un detalle sin aumentar el contexto.

### Use subagents para investigación

<Tip>
  Delegue investigación con `"use subagents to investigate X"`. Exploran en un contexto separado, manteniendo su conversación principal limpia para la implementación.
</Tip>

Dado que el contexto es su restricción fundamental, los subagents son una de las herramientas más poderosas disponibles. Cuando Claude investiga un código base, lee muchos archivos, todos los cuales consumen su contexto. Los subagents se ejecutan en ventanas de contexto separadas e informan resúmenes:

```text theme={null}
Use subagents to investigate how our authentication system handles token
refresh, and whether we have any existing OAuth utilities I should reuse.
```

El subagent explora el código base, lee archivos relevantes e informa hallazgos, todo sin saturar su conversación principal.

También puede usar subagents para verificación después de que Claude implemente algo:

```text theme={null}
use a subagent to review this code for edge cases
```

### Rebobine con puntos de control

<Tip>
  Cada acción que Claude realiza crea un punto de control. Puede restaurar conversación, código o ambos a cualquier punto de control anterior.
</Tip>

Claude automáticamente crea puntos de control antes de cambios. Presione Escape dos veces o ejecute `/rewind` para abrir el menú de rebobinado. Puede restaurar solo conversación, restaurar solo código, restaurar ambos o resumir desde un mensaje seleccionado. Consulte [Checkpointing](/es/checkpointing) para detalles.

En lugar de planificar cuidadosamente cada movimiento, puede decirle a Claude que intente algo arriesgado. Si no funciona, rebobine e intente un enfoque diferente. Los puntos de control persisten entre sesiones, para que pueda cerrar su terminal y aún rebobinar más tarde.

<Warning>
  Los puntos de control solo rastrean cambios realizados *por Claude*, no procesos externos. Esto no es un reemplazo para git.
</Warning>

### Reanudar conversaciones

<Tip>
  Ejecute `claude --continue` para continuar donde lo dejó, o `--resume` para elegir entre sesiones recientes.
</Tip>

Claude Code guarda conversaciones localmente. Cuando una tarea abarca múltiples sesiones, no tiene que re-explicar el contexto:

```bash theme={null}
claude --continue    # Resume the most recent conversation
claude --resume      # Select from recent conversations
```

Use `/rename` para dar a las sesiones nombres descriptivos como `"oauth-migration"` o `"debugging-memory-leak"` para que pueda encontrarlas más tarde. Trate las sesiones como ramas: diferentes flujos de trabajo pueden tener contextos separados y persistentes.

***

## Automatice y escale

Una vez que sea efectivo con un Claude, multiplique su salida con sesiones paralelas, modo no interactivo y patrones de abanico.

Todo hasta ahora asume un humano, un Claude y una conversación. Pero Claude Code escala horizontalmente. Las técnicas en esta sección muestran cómo puede hacer más.

### Ejecutar modo no interactivo

<Tip>
  Use `claude -p "prompt"` en CI, hooks previos a la confirmación o scripts. Agregue `--output-format stream-json` para salida JSON de transmisión.
</Tip>

Con `claude -p "your prompt"`, puede ejecutar Claude de forma no interactiva, sin una sesión. El modo no interactivo es cómo integra Claude en canalizaciones de CI, hooks previos a la confirmación o cualquier flujo de trabajo automatizado. Los formatos de salida le permiten analizar resultados mediante programación: texto sin formato, JSON o JSON de transmisión.

```bash theme={null}
# One-off queries
claude -p "Explain what this project does"

# Structured output for scripts
claude -p "List all API endpoints" --output-format json

# Streaming for real-time processing
claude -p "Analyze this log file" --output-format stream-json
```

### Ejecutar múltiples sesiones de Claude

<Tip>
  Ejecute múltiples sesiones de Claude en paralelo para acelerar el desarrollo, ejecutar experimentos aislados o iniciar flujos de trabajo complejos.
</Tip>

Hay tres formas principales de ejecutar sesiones paralelas:

* [Aplicación de escritorio Claude Code](/es/desktop#work-in-parallel-with-sessions): Gestione múltiples sesiones locales visualmente. Cada sesión obtiene su propio worktree aislado.
* [Claude Code en la web](/es/claude-code-on-the-web): Ejecutar en la infraestructura en la nube segura de Anthropic en máquinas virtuales aisladas.
* [Equipos de agentes](/es/agent-teams): Coordinación automatizada de múltiples sesiones con tareas compartidas, mensajería y un líder de equipo.

Más allá de paralelizar el trabajo, múltiples sesiones habilitan flujos de trabajo enfocados en la calidad. Un contexto nuevo mejora la revisión de código ya que Claude no estará sesgado hacia el código que acaba de escribir.

Por ejemplo, use un patrón Escritor/Revisor:

| Sesión A (Escritor)                                                     | Sesión B (Revisor)                                                                                                                                                       |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Implement a rate limiter for our API endpoints`                        |                                                                                                                                                                          |
|                                                                         | `Review the rate limiter implementation in @src/middleware/rateLimiter.ts. Look for edge cases, race conditions, and consistency with our existing middleware patterns.` |
| `Here's the review feedback: [Session B output]. Address these issues.` |                                                                                                                                                                          |

Puede hacer algo similar con pruebas: haga que un Claude escriba pruebas, luego otro escriba código para pasarlas.

### Abanico a través de archivos

<Tip>
  Recorra tareas llamando a `claude -p` para cada una. Use `--allowedTools` para permisos de alcance para operaciones por lotes.
</Tip>

Para migraciones o análisis grandes, puede distribuir trabajo entre muchas invocaciones paralelas de Claude:

<Steps>
  <Step title="Generar una lista de tareas">
    Haga que Claude enumere todos los archivos que necesitan migración (por ejemplo, `list all 2,000 Python files that need migrating`)
  </Step>

  <Step title="Escribir un script para recorrer la lista">
    ```bash theme={null}
    for file in $(cat files.txt); do
      claude -p "Migrate $file from React to Vue. Return OK or FAIL." \
        --allowedTools "Edit,Bash(git commit *)"
    done
    ```
  </Step>

  <Step title="Probar en algunos archivos, luego ejecutar a escala">
    Refine su indicación basada en lo que sale mal con los primeros 2-3 archivos, luego ejecute en el conjunto completo. La bandera `--allowedTools` restringe lo que Claude puede hacer, lo que importa cuando está ejecutando desatendido.
  </Step>
</Steps>

También puede integrar Claude en canalizaciones de datos/procesamiento existentes:

```bash theme={null}
claude -p "<your prompt>" --output-format json | your_command
```

Use `--verbose` para depuración durante el desarrollo, y apáguelo en producción.

### Ejecutar autónomamente con modo automático

Para ejecución ininterrumpida con verificaciones de seguridad en segundo plano, use [modo automático](/es/permission-modes#eliminate-prompts-with-auto-mode). Un modelo clasificador revisa comandos antes de que se ejecuten, bloqueando escalada de alcance, infraestructura desconocida y acciones impulsadas por contenido hostil mientras permite que el trabajo rutinario continúe sin indicaciones.

```bash theme={null}
claude --permission-mode auto -p "fix all lint errors"
```

Para ejecuciones no interactivas con la bandera `-p`, el modo automático se cancela si el clasificador bloquea repetidamente acciones, ya que no hay usuario al que recurrir. Consulte [cuándo el modo automático se cancela](/es/permission-modes#when-auto-mode-falls-back) para umbrales.

***

## Evite patrones de falla comunes

Estos son errores comunes. Reconocerlos temprano ahorra tiempo:

* **La sesión de todo incluido.** Comienza con una tarea, luego pregunta a Claude algo no relacionado, luego vuelve a la primera tarea. El contexto está lleno de información irrelevante.
  > **Solución**: `/clear` entre tareas no relacionadas.
* **Corrección una y otra vez.** Claude hace algo mal, lo corrige, sigue siendo incorrecto, lo corrige de nuevo. El contexto está contaminado con enfoques fallidos.
  > **Solución**: Después de dos correcciones fallidas, `/clear` y escriba una indicación inicial mejor incorporando lo que aprendió.
* **El CLAUDE.md sobre especificado.** Si su CLAUDE.md es demasiado largo, Claude ignora la mitad porque las reglas importantes se pierden en el ruido.
  > **Solución**: Elimine sin piedad. Si Claude ya hace algo correctamente sin la instrucción, elimínelo o conviértalo en un hook.
* **La brecha de confianza-luego-verificación.** Claude produce una implementación que se ve plausible pero no maneja casos extremos.
  > **Solución**: Siempre proporcione verificación (pruebas, scripts, capturas de pantalla). Si no puede verificarlo, no lo envíe.
* **La exploración infinita.** Pide a Claude que "investigue" algo sin delimitarlo. Claude lee cientos de archivos, llenando el contexto.
  > **Solución**: Delimite investigaciones estrechamente o use subagents para que la exploración no consuma su contexto principal.

***

## Desarrolle su intuición

Los patrones en esta guía no están grabados en piedra. Son puntos de partida que funcionan bien en general, pero podrían no ser óptimos para cada situación.

A veces *debería* dejar que el contexto se acumule porque está profundo en un problema complejo y el historial es valioso. A veces debería omitir la planificación y dejar que Claude lo descubra porque la tarea es exploratoria. A veces una indicación vaga es exactamente lo correcto porque desea ver cómo Claude interpreta el problema antes de limitarlo.

Preste atención a lo que funciona. Cuando Claude produce una salida excelente, note lo que hizo: la estructura de la indicación, el contexto que proporcionó, el modo en que estaba. Cuando Claude lucha, pregúntese por qué. ¿Fue el contexto demasiado ruidoso? ¿La indicación demasiado vaga? ¿La tarea demasiado grande para un pase?

Con el tiempo, desarrollará intuición que ninguna guía puede capturar. Sabrá cuándo ser específico y cuándo ser abierto, cuándo planificar y cuándo explorar, cuándo limpiar contexto y cuándo dejarlo acumular.

## Recursos relacionados

* [Cómo funciona Claude Code](/es/how-claude-code-works): el bucle agencial, herramientas y gestión de contexto
* [Extender Claude Code](/es/features-overview): skills, hooks, MCP, subagents y plugins
* [Flujos de trabajo comunes](/es/common-workflows): recetas paso a paso para depuración, pruebas, PRs y más
* [CLAUDE.md](/es/memory): almacenar convenciones de proyecto y contexto persistente
