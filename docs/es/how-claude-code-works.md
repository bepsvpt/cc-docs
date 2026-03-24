> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Cómo funciona Claude Code

> Comprenda el bucle agentico, las herramientas integradas y cómo Claude Code interactúa con su proyecto.

Claude Code es un asistente agentico que se ejecuta en su terminal. Aunque destaca en codificación, puede ayudarle con cualquier cosa que pueda hacer desde la línea de comandos: escribir documentación, ejecutar compilaciones, buscar archivos, investigar temas y más.

Esta guía cubre la arquitectura principal, las capacidades integradas y [consejos para trabajar efectivamente](#work-effectively-with-claude-code). Para tutoriales paso a paso, consulte [Flujos de trabajo comunes](/es/common-workflows). Para características de extensibilidad como skills, MCP y hooks, consulte [Extender Claude Code](/es/features-overview).

## El bucle agentico

Cuando le da una tarea a Claude, trabaja a través de tres fases: **recopilar contexto**, **tomar acción** y **verificar resultados**. Estas fases se mezclan entre sí. Claude utiliza herramientas en todo momento, ya sea buscando archivos para entender su código, editando para hacer cambios o ejecutando pruebas para verificar su trabajo.

<img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/agentic-loop.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=5f1827dec8539f38adee90ead3a85a38" alt="El bucle agentico: Su indicación lleva a Claude a recopilar contexto, tomar acción, verificar resultados y repetir hasta completar la tarea. Puede interrumpir en cualquier momento." width="720" height="280" data-path="images/agentic-loop.svg" />

El bucle se adapta a lo que pregunta. Una pregunta sobre su base de código podría necesitar solo recopilación de contexto. Una corrección de errores cicla a través de las tres fases repetidamente. Una refactorización podría implicar una verificación extensa. Claude decide qué requiere cada paso basándose en lo que aprendió del paso anterior, encadenando docenas de acciones juntas y corrigiendo el curso en el camino.

Usted también es parte de este bucle. Puede interrumpir en cualquier momento para dirigir a Claude en una dirección diferente, proporcionar contexto adicional o pedirle que intente un enfoque diferente. Claude trabaja de forma autónoma pero permanece receptivo a su entrada.

El bucle agentico está impulsado por dos componentes: [modelos](#models) que razonan y [herramientas](#tools) que actúan. Claude Code sirve como el **arnés agentico** alrededor de Claude: proporciona las herramientas, la gestión del contexto y el entorno de ejecución que convierten un modelo de lenguaje en un agente de codificación capaz.

### Modelos

Claude Code utiliza modelos Claude para entender su código y razonar sobre tareas. Claude puede leer código en cualquier idioma, entender cómo se conectan los componentes y determinar qué necesita cambiar para lograr su objetivo. Para tareas complejas, divide el trabajo en pasos, los ejecuta y se ajusta basándose en lo que aprende.

[Múltiples modelos](/es/model-config) están disponibles con diferentes compensaciones. Sonnet maneja bien la mayoría de tareas de codificación. Opus proporciona un razonamiento más fuerte para decisiones arquitectónicas complejas. Cambie con `/model` durante una sesión o comience con `claude --model <name>`.

Cuando esta guía dice "Claude elige" o "Claude decide", es el modelo el que está haciendo el razonamiento.

### Herramientas

Las herramientas son lo que hace que Claude Code sea agentico. Sin herramientas, Claude solo puede responder con texto. Con herramientas, Claude puede actuar: leer su código, editar archivos, ejecutar comandos, buscar en la web e interactuar con servicios externos. Cada uso de herramienta devuelve información que se retroalimenta en el bucle, informando la siguiente decisión de Claude.

Las herramientas integradas generalmente se dividen en cinco categorías, cada una representando un tipo diferente de agencia.

| Categoría                  | Lo que Claude puede hacer                                                                                                                                                                    |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Operaciones de archivo** | Leer archivos, editar código, crear nuevos archivos, renombrar y reorganizar                                                                                                                 |
| **Búsqueda**               | Encontrar archivos por patrón, buscar contenido con regex, explorar bases de código                                                                                                          |
| **Ejecución**              | Ejecutar comandos de shell, iniciar servidores, ejecutar pruebas, usar git                                                                                                                   |
| **Web**                    | Buscar en la web, obtener documentación, buscar mensajes de error                                                                                                                            |
| **Inteligencia de código** | Ver errores de tipo y advertencias después de ediciones, saltar a definiciones, encontrar referencias (requiere [plugins de inteligencia de código](/es/discover-plugins#code-intelligence)) |

Estas son las capacidades principales. Claude también tiene herramientas para generar subagents, hacerle preguntas y otras tareas de orquestación. Consulte [Herramientas disponibles para Claude](/es/tools-reference) para la lista completa.

Claude elige qué herramientas usar basándose en su indicación y lo que aprende en el camino. Cuando dice "arreglar las pruebas fallidas", Claude podría:

1. Ejecutar el conjunto de pruebas para ver qué está fallando
2. Leer la salida de error
3. Buscar los archivos de código fuente relevantes
4. Leer esos archivos para entender el código
5. Editar los archivos para arreglar el problema
6. Ejecutar las pruebas nuevamente para verificar

Cada uso de herramienta le da a Claude nueva información que informa el siguiente paso. Este es el bucle agentico en acción.

**Extender las capacidades base:** Las herramientas integradas son la base. Puede extender lo que Claude sabe con [skills](/es/skills), conectarse a servicios externos con [MCP](/es/mcp), automatizar flujos de trabajo con [hooks](/es/hooks) y delegar tareas a [subagents](/es/sub-agents). Estas extensiones forman una capa encima del bucle agentico principal. Consulte [Extender Claude Code](/es/features-overview) para orientación sobre cómo elegir la extensión correcta para sus necesidades.

## A qué puede acceder Claude

Esta guía se enfoca en la terminal. Claude Code también se ejecuta en [VS Code](/es/vs-code), [IDEs de JetBrains](/es/jetbrains) y otros entornos.

Cuando ejecuta `claude` en un directorio, Claude Code obtiene acceso a:

* **Su proyecto.** Archivos en su directorio y subdirectorios, más archivos en otros lugares con su permiso.
* **Su terminal.** Cualquier comando que pueda ejecutar: herramientas de compilación, git, gestores de paquetes, utilidades del sistema, scripts. Si puede hacerlo desde la línea de comandos, Claude también puede.
* **Su estado de git.** Rama actual, cambios sin confirmar e historial de confirmaciones recientes.
* **Su [CLAUDE.md](/es/memory).** Un archivo markdown donde almacena instrucciones específicas del proyecto, convenciones y contexto que Claude debe conocer en cada sesión.
* **[Auto memory](/es/memory#auto-memory).** Aprendizajes que Claude guarda automáticamente mientras trabaja, como patrones de proyecto y sus preferencias. Las primeras 200 líneas de MEMORY.md se cargan al inicio de cada sesión.
* **Extensiones que configure.** [Servidores MCP](/es/mcp) para servicios externos, [skills](/es/skills) para flujos de trabajo, [subagents](/es/sub-agents) para trabajo delegado y [Claude en Chrome](/es/chrome) para interacción del navegador.

Debido a que Claude ve todo su proyecto, puede trabajar en él. Cuando le pide a Claude que "arregle el error de autenticación", busca archivos relevantes, lee múltiples archivos para entender el contexto, realiza ediciones coordinadas en ellos, ejecuta pruebas para verificar la corrección y confirma los cambios si lo solicita. Esto es diferente de los asistentes de código en línea que solo ven el archivo actual.

## Entornos e interfaces

El bucle agentico, las herramientas y las capacidades descritas anteriormente son iguales en todas partes donde use Claude Code. Lo que cambia es dónde se ejecuta el código y cómo interactúa con él.

### Entornos de ejecución

Claude Code se ejecuta en tres entornos, cada uno con diferentes compensaciones para dónde se ejecuta su código.

| Entorno            | Dónde se ejecuta el código                | Caso de uso                                                            |
| ------------------ | ----------------------------------------- | ---------------------------------------------------------------------- |
| **Local**          | Su máquina                                | Predeterminado. Acceso completo a sus archivos, herramientas y entorno |
| **Cloud**          | VMs administradas por Anthropic           | Delegar tareas, trabajar en repositorios que no tiene localmente       |
| **Control remoto** | Su máquina, controlada desde un navegador | Usar la interfaz web mientras mantiene todo local                      |

### Interfaces

Puede acceder a Claude Code a través de la terminal, la [aplicación de escritorio](/es/desktop), [extensiones de IDE](/es/ide-integrations), [claude.ai/code](https://claude.ai/code), [Control remoto](/es/remote-control), [Slack](/es/slack) y [canalizaciones CI/CD](/es/github-actions). La interfaz determina cómo ve e interactúa con Claude, pero el bucle agentico subyacente es idéntico. Consulte [Usar Claude Code en todas partes](/es/overview#use-claude-code-everywhere) para la lista completa.

## Trabajar con sesiones

Claude Code guarda su conversación localmente mientras trabaja. Cada mensaje, uso de herramienta y resultado se almacena, lo que permite [rebobinar](#undo-changes-with-checkpoints), [reanudar y bifurcar](#resume-or-fork-sessions) sesiones. Antes de que Claude realice cambios de código, también toma una instantánea de los archivos afectados para que pueda revertir si es necesario.

**Las sesiones son independientes.** Cada nueva sesión comienza con una ventana de contexto nueva, sin el historial de conversación de sesiones anteriores. Claude puede persistir aprendizajes entre sesiones usando [auto memory](/es/memory#auto-memory), y puede agregar sus propias instrucciones persistentes en [CLAUDE.md](/es/memory).

### Trabajar entre ramas

Cada conversación de Claude Code es una sesión vinculada a su directorio actual. Cuando reanuda, solo ve sesiones de ese directorio.

Claude ve los archivos de su rama actual. Cuando cambia de rama, Claude ve los archivos de la nueva rama, pero el historial de conversación permanece igual. Claude recuerda lo que discutió incluso después de cambiar de rama.

Dado que las sesiones están vinculadas a directorios, puede ejecutar sesiones paralelas de Claude Code usando [git worktrees](/es/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees), que crean directorios separados para ramas individuales.

### Reanudar o bifurcar sesiones

Cuando reanuda una sesión con `claude --continue` o `claude --resume`, continúa donde lo dejó usando el mismo ID de sesión. Los nuevos mensajes se agregan a la conversación existente. Su historial de conversación completo se restaura, pero los permisos con alcance de sesión no. Deberá volver a aprobarlos.

<img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/session-continuity.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=fa41d12bfb57579cabfeece907151d30" alt="Continuidad de sesión: reanudar continúa la misma sesión, bifurcar crea una nueva rama con un nuevo ID." width="560" height="280" data-path="images/session-continuity.svg" />

Para ramificar e intentar un enfoque diferente sin afectar la sesión original, use la bandera `--fork-session`:

```bash  theme={null}
claude --continue --fork-session
```

Esto crea un nuevo ID de sesión mientras preserva el historial de conversación hasta ese punto. La sesión original permanece sin cambios. Como reanudar, las sesiones bifurcadas no heredan permisos con alcance de sesión.

**Misma sesión en múltiples terminales**: Si reanuda la misma sesión en múltiples terminales, ambos terminales escriben en el mismo archivo de sesión. Los mensajes de ambos se intercalan, como dos personas escribiendo en el mismo cuaderno. Nada se corrompe, pero la conversación se vuelve confusa. Cada terminal solo ve sus propios mensajes durante la sesión, pero si reanuda esa sesión más tarde, verá todo intercalado. Para trabajo paralelo desde el mismo punto de partida, use `--fork-session` para dar a cada terminal su propia sesión limpia.

### La ventana de contexto

La ventana de contexto de Claude contiene el historial de su conversación, contenidos de archivos, salidas de comandos, [CLAUDE.md](/es/memory), skills cargadas e instrucciones del sistema. A medida que trabaja, el contexto se llena. Claude se compacta automáticamente, pero las instrucciones del principio de la conversación pueden perderse. Coloque reglas persistentes en CLAUDE.md y ejecute `/context` para ver qué está usando espacio.

#### Cuando el contexto se llena

Claude Code gestiona el contexto automáticamente a medida que se acerca al límite. Primero borra salidas de herramientas más antiguas, luego resume la conversación si es necesario. Sus solicitudes y fragmentos de código clave se preservan; las instrucciones detalladas del principio de la conversación pueden perderse. Coloque reglas persistentes en CLAUDE.md en lugar de depender del historial de conversación.

Para controlar qué se preserva durante la compactación, agregue una sección "Compact Instructions" a CLAUDE.md o ejecute `/compact` con un enfoque (como `/compact focus on the API changes`).

Ejecute `/context` para ver qué está usando espacio. Los servidores MCP agregan definiciones de herramientas a cada solicitud, por lo que algunos servidores pueden consumir contexto significativo antes de que comience a trabajar. Ejecute `/mcp` para verificar costos por servidor.

#### Gestionar contexto con skills y subagents

Más allá de la compactación, puede usar otras características para controlar qué se carga en el contexto.

[Skills](/es/skills) se cargan bajo demanda. Claude ve descripciones de skills al inicio de la sesión, pero el contenido completo solo se carga cuando se usa una skill. Para skills que invoca manualmente, establezca `disable-model-invocation: true` para mantener descripciones fuera del contexto hasta que las necesite.

[Subagents](/es/sub-agents) obtienen su propio contexto nuevo, completamente separado de su conversación principal. Su trabajo no infla su contexto. Cuando terminan, devuelven un resumen. Este aislamiento es por qué los subagents ayudan con sesiones largas.

Consulte [costos de contexto](/es/features-overview#understand-context-costs) para lo que cuesta cada característica y [reducir el uso de tokens](/es/costs#reduce-token-usage) para consejos sobre cómo gestionar el contexto.

## Manténgase seguro con checkpoints y permisos

Claude tiene dos mecanismos de seguridad: los checkpoints le permiten deshacer cambios de archivo y los permisos controlan qué puede hacer Claude sin preguntar.

### Deshacer cambios con checkpoints

**Cada edición de archivo es reversible.** Antes de que Claude edite cualquier archivo, toma una instantánea del contenido actual. Si algo sale mal, presione `Esc` dos veces para rebobinar a un estado anterior, o pida a Claude que deshaga.

Los checkpoints son locales a su sesión, separados de git. Solo cubren cambios de archivo. Las acciones que afectan sistemas remotos (bases de datos, APIs, implementaciones) no pueden ser checkpointed, por lo que Claude pregunta antes de ejecutar comandos con efectos secundarios externos.

### Controle qué puede hacer Claude

Presione `Shift+Tab` para ciclar a través de modos de permiso:

* **Predeterminado**: Claude pregunta antes de ediciones de archivo y comandos de shell
* **Auto-aceptar ediciones**: Claude edita archivos sin preguntar, aún pregunta por comandos
* **Plan Mode**: Claude usa solo herramientas de solo lectura, creando un plan que puede aprobar antes de la ejecución

También puede permitir comandos específicos en `.claude/settings.json` para que Claude no pregunte cada vez. Esto es útil para comandos confiables como `npm test` o `git status`. La configuración puede tener alcance desde políticas de toda la organización hasta preferencias personales. Consulte [Permisos](/es/permissions) para detalles.

***

## Trabajar efectivamente con Claude Code

Estos consejos le ayudan a obtener mejores resultados de Claude Code.

### Pida ayuda a Claude Code

Claude Code puede enseñarle cómo usarlo. Haga preguntas como "¿cómo configuro hooks?" o "¿cuál es la mejor manera de estructurar mi CLAUDE.md?" y Claude explicará.

Los comandos integrados también lo guían a través de la configuración:

* `/init` lo guía a través de la creación de un CLAUDE.md para su proyecto
* `/agents` lo ayuda a configurar subagents personalizados
* `/doctor` diagnostica problemas comunes con su instalación

### Es una conversación

Claude Code es conversacional. No necesita indicaciones perfectas. Comience con lo que desea, luego refine:

```text  theme={null}
Arreglar el error de inicio de sesión
```

\[Claude investiga, intenta algo]

```text  theme={null}
Eso no es del todo correcto. El problema está en el manejo de sesiones.
```

\[Claude ajusta el enfoque]

Cuando el primer intento no es correcto, no comienza de nuevo. Itera.

#### Interrumpir y dirigir

Puede interrumpir a Claude en cualquier momento. Si va por el camino equivocado, simplemente escriba su corrección y presione Enter. Claude dejará de hacer lo que está haciendo y ajustará su enfoque basándose en su entrada. No tiene que esperar a que termine o comenzar de nuevo.

### Sea específico desde el principio

Cuanto más precisa sea su indicación inicial, menos correcciones necesitará. Haga referencia a archivos específicos, mencione restricciones y señale patrones de ejemplo.

```text  theme={null}
El flujo de pago está roto para usuarios con tarjetas vencidas.
Verifique src/payments/ para el problema, especialmente la actualización de tokens.
Escriba una prueba fallida primero, luego arréglela.
```

Las indicaciones vagas funcionan, pero pasará más tiempo dirigiendo. Las indicaciones específicas como la anterior a menudo tienen éxito en el primer intento.

### Dé a Claude algo contra lo que verificar

Claude funciona mejor cuando puede verificar su propio trabajo. Incluya casos de prueba, pegue capturas de pantalla de la interfaz de usuario esperada o defina la salida que desea.

```text  theme={null}
Implementar validateEmail. Casos de prueba: 'user@example.com' → true,
'invalid' → false, 'user@.com' → false. Ejecute las pruebas después.
```

Para trabajo visual, pegue una captura de pantalla del diseño y pida a Claude que compare su implementación con ella.

### Explorar antes de implementar

Para problemas complejos, separe la investigación de la codificación. Use plan mode (`Shift+Tab` dos veces) para analizar la base de código primero:

```text  theme={null}
Lea src/auth/ y entienda cómo manejamos sesiones.
Luego cree un plan para agregar soporte OAuth.
```

Revise el plan, refínelo a través de la conversación, luego deje que Claude implemente. Este enfoque de dos fases produce mejores resultados que saltar directamente al código.

### Delegue, no dicte

Piense en delegar a un colega capaz. Dé contexto y dirección, luego confíe en que Claude descubra los detalles:

```text  theme={null}
El flujo de pago está roto para usuarios con tarjetas vencidas.
El código relevante está en src/payments/. ¿Puede investigar y arreglarlo?
```

No necesita especificar qué archivos leer o qué comandos ejecutar. Claude lo descubre.

## Qué sigue

<CardGroup cols={2}>
  <Card title="Extender con características" icon="puzzle-piece" href="/es/features-overview">
    Agregue Skills, conexiones MCP y comandos personalizados
  </Card>

  <Card title="Flujos de trabajo comunes" icon="graduation-cap" href="/es/common-workflows">
    Guías paso a paso para tareas típicas
  </Card>
</CardGroup>
