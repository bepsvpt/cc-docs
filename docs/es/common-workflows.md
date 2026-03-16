> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Flujos de trabajo comunes

> Guías paso a paso para explorar bases de código, corregir errores, refactorizar, probar y otras tareas cotidianas con Claude Code.

Esta página cubre flujos de trabajo prácticos para el desarrollo cotidiano: explorar código desconocido, depuración, refactorización, escritura de pruebas, creación de solicitudes de extracción y gestión de sesiones. Cada sección incluye ejemplos de indicaciones que puede adaptar a sus propios proyectos. Para patrones y consejos de nivel superior, consulte [Mejores prácticas](/es/best-practices).

## Comprender nuevas bases de código

### Obtener una descripción general rápida de la base de código

Supongamos que acaba de unirse a un nuevo proyecto y necesita comprender su estructura rápidamente.

<Steps>
  <Step title="Navegue al directorio raíz del proyecto">
    ```bash  theme={null}
    cd /path/to/project 
    ```
  </Step>

  <Step title="Inicie Claude Code">
    ```bash  theme={null}
    claude 
    ```
  </Step>

  <Step title="Solicite una descripción general de alto nivel">
    ```text  theme={null}
    dame una descripción general de esta base de código
    ```
  </Step>

  <Step title="Profundice en componentes específicos">
    ```text  theme={null}
    explica los patrones de arquitectura principales utilizados aquí
    ```

    ```text  theme={null}
    ¿cuáles son los modelos de datos clave?
    ```

    ```text  theme={null}
    ¿cómo se maneja la autenticación?
    ```
  </Step>
</Steps>

<Tip>
  Consejos:

  * Comience con preguntas amplias, luego reduzca a áreas específicas
  * Pregunte sobre convenciones de codificación y patrones utilizados en el proyecto
  * Solicite un glosario de términos específicos del proyecto
</Tip>

### Encontrar código relevante

Supongamos que necesita localizar código relacionado con una característica o funcionalidad específica.

<Steps>
  <Step title="Pida a Claude que encuentre archivos relevantes">
    ```text  theme={null}
    encuentra los archivos que manejan la autenticación de usuarios
    ```
  </Step>

  <Step title="Obtenga contexto sobre cómo interactúan los componentes">
    ```text  theme={null}
    ¿cómo funcionan juntos estos archivos de autenticación?
    ```
  </Step>

  <Step title="Comprenda el flujo de ejecución">
    ```text  theme={null}
    rastrear el proceso de inicio de sesión de front-end a base de datos
    ```
  </Step>
</Steps>

<Tip>
  Consejos:

  * Sea específico sobre lo que está buscando
  * Utilice el lenguaje del dominio del proyecto
  * Instale un [complemento de inteligencia de código](/es/discover-plugins#code-intelligence) para su lenguaje para dar a Claude una navegación precisa de "ir a definición" y "buscar referencias"
</Tip>

***

## Corregir errores de manera eficiente

Supongamos que ha encontrado un mensaje de error y necesita encontrar y corregir su origen.

<Steps>
  <Step title="Comparta el error con Claude">
    ```text  theme={null}
    estoy viendo un error cuando ejecuto npm test
    ```
  </Step>

  <Step title="Solicite recomendaciones de corrección">
    ```text  theme={null}
    sugiere algunas formas de corregir el @ts-ignore en user.ts
    ```
  </Step>

  <Step title="Aplique la corrección">
    ```text  theme={null}
    actualiza user.ts para agregar la verificación nula que sugeriste
    ```
  </Step>
</Steps>

<Tip>
  Consejos:

  * Dígale a Claude el comando para reproducir el problema y obtener un seguimiento de pila
  * Mencione cualquier paso para reproducir el error
  * Hágale saber a Claude si el error es intermitente o consistente
</Tip>

***

## Refactorizar código

Supongamos que necesita actualizar código antiguo para utilizar patrones y prácticas modernas.

<Steps>
  <Step title="Identifique código heredado para refactorización">
    ```text  theme={null}
    encuentra el uso de API obsoleta en nuestra base de código
    ```
  </Step>

  <Step title="Obtenga recomendaciones de refactorización">
    ```text  theme={null}
    sugiere cómo refactorizar utils.js para usar características modernas de JavaScript
    ```
  </Step>

  <Step title="Aplique los cambios de manera segura">
    ```text  theme={null}
    refactoriza utils.js para usar características ES2024 manteniendo el mismo comportamiento
    ```
  </Step>

  <Step title="Verifique la refactorización">
    ```text  theme={null}
    ejecuta pruebas para el código refactorizado
    ```
  </Step>
</Steps>

<Tip>
  Consejos:

  * Pida a Claude que explique los beneficios del enfoque moderno
  * Solicite que los cambios mantengan la compatibilidad hacia atrás cuando sea necesario
  * Realice la refactorización en incrementos pequeños y comprobables
</Tip>

***

## Usar subagentes especializados

Supongamos que desea utilizar subagentes de IA especializados para manejar tareas específicas de manera más efectiva.

<Steps>
  <Step title="Ver subagentes disponibles">
    ```text  theme={null}
    /agents
    ```

    Esto muestra todos los subagentes disponibles y le permite crear otros nuevos.
  </Step>

  <Step title="Usar subagentes automáticamente">
    Claude Code delega automáticamente tareas apropiadas a subagentes especializados:

    ```text  theme={null}
    revisa mis cambios de código recientes para problemas de seguridad
    ```

    ```text  theme={null}
    ejecuta todas las pruebas y corrige cualquier fallo
    ```
  </Step>

  <Step title="Solicitar explícitamente subagentes específicos">
    ```text  theme={null}
    usa el subagente code-reviewer para verificar el módulo de autenticación
    ```

    ```text  theme={null}
    haz que el subagente debugger investigue por qué los usuarios no pueden iniciar sesión
    ```
  </Step>

  <Step title="Crear subagentes personalizados para su flujo de trabajo">
    ```text  theme={null}
    /agents
    ```

    Luego seleccione "Crear nuevo subagente" y siga las indicaciones para definir:

    * Un identificador único que describa el propósito del subagente (por ejemplo, `code-reviewer`, `api-designer`).
    * Cuándo Claude debe usar este agente
    * Qué herramientas puede acceder
    * Un indicador del sistema que describa el rol y comportamiento del agente
  </Step>
</Steps>

<Tip>
  Consejos:

  * Cree subagentes específicos del proyecto en `.claude/agents/` para compartir en equipo
  * Utilice campos `description` descriptivos para habilitar la delegación automática
  * Limite el acceso a herramientas a lo que cada subagente realmente necesita
  * Consulte la [documentación de subagentes](/es/sub-agents) para ejemplos detallados
</Tip>

***

## Usar Plan Mode para análisis seguro de código

Plan Mode instruye a Claude para crear un plan analizando la base de código con operaciones de solo lectura, perfecto para explorar bases de código, planificar cambios complejos o revisar código de manera segura. En Plan Mode, Claude utiliza [`AskUserQuestion`](/es/settings#tools-available-to-claude) para recopilar requisitos y aclarar sus objetivos antes de proponer un plan.

### Cuándo usar Plan Mode

* **Implementación de múltiples pasos**: Cuando su característica requiere hacer ediciones en muchos archivos
* **Exploración de código**: Cuando desea investigar la base de código a fondo antes de cambiar nada
* **Desarrollo interactivo**: Cuando desea iterar en la dirección con Claude

### Cómo usar Plan Mode

**Activar Plan Mode durante una sesión**

Puede cambiar a Plan Mode durante una sesión usando **Shift+Tab** para ciclar a través de modos de permiso.

Si está en Normal Mode, **Shift+Tab** primero cambia a Auto-Accept Mode, indicado por `⏵⏵ accept edits on` en la parte inferior de la terminal. Un **Shift+Tab** posterior cambiará a Plan Mode, indicado por `⏸ plan mode on`.

**Iniciar una nueva sesión en Plan Mode**

Para iniciar una nueva sesión en Plan Mode, use la bandera `--permission-mode plan`:

```bash  theme={null}
claude --permission-mode plan
```

**Ejecutar consultas "sin interfaz" en Plan Mode**

También puede ejecutar una consulta en Plan Mode directamente con `-p` (es decir, en ["modo sin interfaz"](/es/headless)):

```bash  theme={null}
claude --permission-mode plan -p "Analiza el sistema de autenticación y sugiere mejoras"
```

### Ejemplo: Planificar una refactorización compleja

```bash  theme={null}
claude --permission-mode plan
```

```text  theme={null}
Necesito refactorizar nuestro sistema de autenticación para usar OAuth2. Crea un plan de migración detallado.
```

Claude analiza la implementación actual y crea un plan integral. Refine con seguimientos:

```text  theme={null}
¿Qué hay sobre la compatibilidad hacia atrás?
```

```text  theme={null}
¿Cómo deberíamos manejar la migración de la base de datos?
```

<Tip>Presione `Ctrl+G` para abrir el plan en su editor de texto predeterminado, donde puede editarlo directamente antes de que Claude continúe.</Tip>

### Configurar Plan Mode como predeterminado

```json  theme={null}
// .claude/settings.json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

Consulte la [documentación de configuración](/es/settings#available-settings) para más opciones de configuración.

***

## Trabajar con pruebas

Supongamos que necesita agregar pruebas para código no cubierto.

<Steps>
  <Step title="Identifique código no probado">
    ```text  theme={null}
    encuentra funciones en NotificationsService.swift que no están cubiertas por pruebas
    ```
  </Step>

  <Step title="Genere andamiaje de prueba">
    ```text  theme={null}
    agrega pruebas para el servicio de notificaciones
    ```
  </Step>

  <Step title="Agregue casos de prueba significativos">
    ```text  theme={null}
    agrega casos de prueba para condiciones de borde en el servicio de notificaciones
    ```
  </Step>

  <Step title="Ejecute y verifique las pruebas">
    ```text  theme={null}
    ejecuta las nuevas pruebas y corrige cualquier fallo
    ```
  </Step>
</Steps>

Claude puede generar pruebas que sigan los patrones y convenciones existentes de su proyecto. Al solicitar pruebas, sea específico sobre qué comportamiento desea verificar. Claude examina sus archivos de prueba existentes para coincidir con el estilo, marcos y patrones de afirmación ya en uso.

Para una cobertura integral, pida a Claude que identifique casos extremos que podría haber perdido. Claude puede analizar sus rutas de código y sugerir pruebas para condiciones de error, valores límite e entradas inesperadas que son fáciles de pasar por alto.

***

## Crear solicitudes de extracción

Puede crear solicitudes de extracción pidiendo a Claude directamente ("crear una pr para mis cambios"), o guiar a Claude a través de ella paso a paso:

<Steps>
  <Step title="Resuma sus cambios">
    ```text  theme={null}
    resume los cambios que he hecho en el módulo de autenticación
    ```
  </Step>

  <Step title="Genere una solicitud de extracción">
    ```text  theme={null}
    crear una pr
    ```
  </Step>

  <Step title="Revise y refine">
    ```text  theme={null}
    mejora la descripción de PR con más contexto sobre las mejoras de seguridad
    ```
  </Step>
</Steps>

Cuando crea una PR usando `gh pr create`, la sesión se vincula automáticamente a esa PR. Puede reanudarla más tarde con `claude --from-pr <number>`.

<Tip>
  Revise la PR generada por Claude antes de enviarla y pida a Claude que destaque los riesgos potenciales o consideraciones.
</Tip>

## Manejar documentación

Supongamos que necesita agregar o actualizar documentación para su código.

<Steps>
  <Step title="Identifique código sin documentar">
    ```text  theme={null}
    encuentra funciones sin comentarios JSDoc adecuados en el módulo de autenticación
    ```
  </Step>

  <Step title="Genere documentación">
    ```text  theme={null}
    agrega comentarios JSDoc a las funciones sin documentar en auth.js
    ```
  </Step>

  <Step title="Revise y mejore">
    ```text  theme={null}
    mejora la documentación generada con más contexto y ejemplos
    ```
  </Step>

  <Step title="Verifique la documentación">
    ```text  theme={null}
    verifica si la documentación sigue los estándares de nuestro proyecto
    ```
  </Step>
</Steps>

<Tip>
  Consejos:

  * Especifique el estilo de documentación que desea (JSDoc, docstrings, etc.)
  * Solicite ejemplos en la documentación
  * Solicite documentación para API públicas, interfaces y lógica compleja
</Tip>

***

## Trabajar con imágenes

Supongamos que necesita trabajar con imágenes en su base de código y desea la ayuda de Claude para analizar el contenido de la imagen.

<Steps>
  <Step title="Agregue una imagen a la conversación">
    Puede usar cualquiera de estos métodos:

    1. Arrastre y suelte una imagen en la ventana de Claude Code
    2. Copie una imagen y péguéla en la CLI con ctrl+v (No use cmd+v)
    3. Proporcione una ruta de imagen a Claude. Por ejemplo, "Analiza esta imagen: /path/to/your/image.png"
  </Step>

  <Step title="Pida a Claude que analice la imagen">
    ```text  theme={null}
    ¿Qué muestra esta imagen?
    ```

    ```text  theme={null}
    Describe los elementos de la interfaz de usuario en esta captura de pantalla
    ```

    ```text  theme={null}
    ¿Hay algún elemento problemático en este diagrama?
    ```
  </Step>

  <Step title="Usar imágenes para contexto">
    ```text  theme={null}
    Aquí hay una captura de pantalla del error. ¿Qué lo está causando?
    ```

    ```text  theme={null}
    Este es nuestro esquema de base de datos actual. ¿Cómo deberíamos modificarlo para la nueva característica?
    ```
  </Step>

  <Step title="Obtenga sugerencias de código del contenido visual">
    ```text  theme={null}
    Generar CSS para coincidir con este mockup de diseño
    ```

    ```text  theme={null}
    ¿Qué estructura HTML recrearía este componente?
    ```
  </Step>
</Steps>

<Tip>
  Consejos:

  * Utilice imágenes cuando las descripciones de texto serían poco claras o engorrosas
  * Incluya capturas de pantalla de errores, diseños de interfaz de usuario o diagramas para un mejor contexto
  * Puede trabajar con múltiples imágenes en una conversación
  * El análisis de imágenes funciona con diagramas, capturas de pantalla, mockups y más
  * Cuando Claude hace referencia a imágenes (por ejemplo, `[Image #1]`), `Cmd+Click` (Mac) o `Ctrl+Click` (Windows/Linux) el enlace para abrir la imagen en su visor predeterminado
</Tip>

***

## Archivos y directorios de referencia

Use @ para incluir rápidamente archivos o directorios sin esperar a que Claude los lea.

<Steps>
  <Step title="Haga referencia a un archivo único">
    ```text  theme={null}
    Explica la lógica en @src/utils/auth.js
    ```

    Esto incluye el contenido completo del archivo en la conversación.
  </Step>

  <Step title="Haga referencia a un directorio">
    ```text  theme={null}
    ¿Cuál es la estructura de @src/components?
    ```

    Esto proporciona un listado de directorio con información de archivo.
  </Step>

  <Step title="Haga referencia a recursos MCP">
    ```text  theme={null}
    Muéstrame los datos de @github:repos/owner/repo/issues
    ```

    Esto obtiene datos de servidores MCP conectados usando el formato @server:resource. Consulte [recursos MCP](/es/mcp#use-mcp-resources) para más detalles.
  </Step>
</Steps>

<Tip>
  Consejos:

  * Las rutas de archivo pueden ser relativas o absolutas
  * Las referencias de archivo @ agregan `CLAUDE.md` en el directorio del archivo y directorios principales al contexto
  * Las referencias de directorio muestran listados de archivos, no contenidos
  * Puede hacer referencia a múltiples archivos en un solo mensaje (por ejemplo, "@file1.js y @file2.js")
</Tip>

***

## Usar pensamiento extendido (thinking mode)

[El pensamiento extendido](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) está habilitado de forma predeterminada, dando a Claude espacio para razonar a través de problemas complejos paso a paso antes de responder. Este razonamiento es visible en modo detallado, que puede alternar con `Ctrl+O`.

Además, Opus 4.6 introduce razonamiento adaptativo: en lugar de un presupuesto de token de pensamiento fijo, el modelo asigna dinámicamente el pensamiento basado en su configuración de [nivel de esfuerzo](/es/model-config#adjust-effort-level). El pensamiento extendido y el razonamiento adaptativo funcionan juntos para darle control sobre qué tan profundamente Claude razona antes de responder.

El pensamiento extendido es particularmente valioso para decisiones arquitectónicas complejas, errores desafiantes, planificación de implementación de múltiples pasos y evaluación de compensaciones entre diferentes enfoques.

<Note>
  Frases como "pensar", "pensar duro" y "pensar más" se interpretan como instrucciones de indicación regulares y no asignan tokens de pensamiento.
</Note>

### Configurar thinking mode

El pensamiento está habilitado de forma predeterminada, pero puede ajustarlo o deshabilitarlo.

| Alcance                         | Cómo configurar                                                                                  | Detalles                                                                                                                                                                                        |
| ------------------------------- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Nivel de esfuerzo**           | Ajuste en `/model` o establezca [`CLAUDE_CODE_EFFORT_LEVEL`](/es/settings#environment-variables) | Control de profundidad de pensamiento para Opus 4.6 y Sonnet 4.6: bajo, medio, alto. Consulte [Ajustar nivel de esfuerzo](/es/model-config#adjust-effort-level)                                 |
| **Palabra clave `ultrathink`**  | Incluya "ultrathink" en cualquier lugar de su indicación                                         | Establece el esfuerzo en alto para ese turno en Opus 4.6 y Sonnet 4.6. Útil para tareas únicas que requieren razonamiento profundo sin cambiar permanentemente su configuración de esfuerzo     |
| **Atajo de alternancia**        | Presione `Option+T` (macOS) o `Alt+T` (Windows/Linux)                                            | Alterne el pensamiento activado/desactivado para la sesión actual (todos los modelos). Puede requerir [configuración de terminal](/es/terminal-config) para habilitar atajos de tecla de opción |
| **Predeterminado global**       | Use `/config` para alternar thinking mode                                                        | Establece su predeterminado en todos los proyectos (todos los modelos).<br />Guardado como `alwaysThinkingEnabled` en `~/.claude/settings.json`                                                 |
| **Presupuesto de token límite** | Establezca la variable de entorno [`MAX_THINKING_TOKENS`](/es/settings#environment-variables)    | Limite el presupuesto de pensamiento a un número específico de tokens (ignorado en Opus 4.6 a menos que se establezca en 0). Ejemplo: `export MAX_THINKING_TOKENS=10000`                        |

Para ver el proceso de pensamiento de Claude, presione `Ctrl+O` para alternar el modo detallado y ver el razonamiento interno mostrado como texto gris en cursiva.

### Cómo funciona el pensamiento extendido

El pensamiento extendido controla cuánto razonamiento interno realiza Claude antes de responder. Más pensamiento proporciona más espacio para explorar soluciones, analizar casos extremos y autocorregir errores.

**Con Opus 4.6**, el pensamiento utiliza razonamiento adaptativo: el modelo asigna dinámicamente tokens de pensamiento basados en el [nivel de esfuerzo](/es/model-config#adjust-effort-level) que selecciona (bajo, medio, alto). Esta es la forma recomendada de ajustar la compensación entre velocidad y profundidad de razonamiento.

**Con otros modelos**, el pensamiento utiliza un presupuesto fijo de hasta 31.999 tokens de su presupuesto de salida. Puede limitar esto con la variable de entorno [`MAX_THINKING_TOKENS`](/es/settings#environment-variables), o deshabilitar el pensamiento completamente a través de `/config` o la alternancia `Option+T`/`Alt+T`.

`MAX_THINKING_TOKENS` se ignora en Opus 4.6 y Sonnet 4.6, ya que el razonamiento adaptativo controla la profundidad del pensamiento en su lugar. La única excepción: establecer `MAX_THINKING_TOKENS=0` aún deshabilita el pensamiento completamente en cualquier modelo. Para deshabilitar el pensamiento adaptativo y revertir al presupuesto de pensamiento fijo, establezca `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`. Consulte [variables de entorno](/es/settings#environment-variables).

<Warning>
  Se le cobra por todos los tokens de pensamiento utilizados, aunque los modelos Claude 4 muestren pensamiento resumido
</Warning>

***

## Reanudar conversaciones anteriores

Cuando inicia Claude Code, puede reanudar una sesión anterior:

* `claude --continue` continúa la conversación más reciente en el directorio actual
* `claude --resume` abre un selector de conversación o reanuda por nombre
* `claude --from-pr 123` reanuda sesiones vinculadas a una solicitud de extracción específica

Desde dentro de una sesión activa, use `/resume` para cambiar a una conversación diferente.

Las sesiones se almacenan por directorio de proyecto. El selector `/resume` muestra sesiones del mismo repositorio de git, incluidos worktrees.

### Nombrar sus sesiones

Dé a las sesiones nombres descriptivos para encontrarlas más tarde. Esta es una mejor práctica cuando se trabaja en múltiples tareas o características.

<Steps>
  <Step title="Nombre la sesión actual">
    Use `/rename` durante una sesión para darle un nombre memorable:

    ```text  theme={null}
    /rename auth-refactor
    ```

    También puede renombrar cualquier sesión desde el selector: ejecute `/resume`, navegue a una sesión y presione `R`.
  </Step>

  <Step title="Reanude por nombre más tarde">
    Desde la línea de comandos:

    ```bash  theme={null}
    claude --resume auth-refactor
    ```

    O desde dentro de una sesión activa:

    ```text  theme={null}
    /resume auth-refactor
    ```
  </Step>
</Steps>

### Usar el selector de sesión

El comando `/resume` (o `claude --resume` sin argumentos) abre un selector de sesión interactivo con estas características:

**Atajos de teclado en el selector:**

| Atajo     | Acción                                                |
| :-------- | :---------------------------------------------------- |
| `↑` / `↓` | Navegue entre sesiones                                |
| `→` / `←` | Expandir o contraer sesiones agrupadas                |
| `Enter`   | Seleccione y reanude la sesión resaltada              |
| `P`       | Vista previa del contenido de la sesión               |
| `R`       | Renombre la sesión resaltada                          |
| `/`       | Busque para filtrar sesiones                          |
| `A`       | Alterne entre directorio actual y todos los proyectos |
| `B`       | Filtrar a sesiones de su rama de git actual           |
| `Esc`     | Salga del selector o modo de búsqueda                 |

**Organización de sesiones:**

El selector muestra sesiones con metadatos útiles:

* Nombre de sesión o indicación inicial
* Tiempo transcurrido desde la última actividad
* Recuento de mensajes
* Rama de Git (si corresponde)

Las sesiones bifurcadas (creadas con `/rewind` o `--fork-session`) se agrupan bajo su sesión raíz, lo que facilita encontrar conversaciones relacionadas.

<Tip>
  Consejos:

  * **Nombre sesiones temprano**: Use `/rename` cuando comience a trabajar en una tarea distinta, es mucho más fácil encontrar "payment-integration" que "explica esta función" más tarde
  * Use `--continue` para acceso rápido a su conversación más reciente en el directorio actual
  * Use `--resume session-name` cuando sepa qué sesión necesita
  * Use `--resume` (sin nombre) cuando necesite examinar y seleccionar
  * Para scripts, use `claude --continue --print "prompt"` para reanudar en modo no interactivo
  * Presione `P` en el selector para obtener una vista previa de una sesión antes de reanudarla
  * La conversación reanudada comienza con el mismo modelo y configuración que el original

  Cómo funciona:

  1. **Almacenamiento de conversación**: Todas las conversaciones se guardan automáticamente localmente con su historial de mensajes completo
  2. **Deserialización de mensajes**: Al reanudar, se restaura el historial de mensajes completo para mantener el contexto
  3. **Estado de herramienta**: El uso de herramientas y los resultados de la conversación anterior se conservan
  4. **Restauración de contexto**: La conversación se reanuda con todo el contexto anterior intacto
</Tip>

***

## Ejecutar sesiones paralelas de Claude Code con Git worktrees

Cuando trabaja en múltiples tareas a la vez, necesita que cada sesión de Claude tenga su propia copia de la base de código para que los cambios no choquen. Los worktrees de Git resuelven esto creando directorios de trabajo separados que cada uno tiene sus propios archivos y rama, mientras comparten el mismo historial de repositorio y conexiones remotas. Esto significa que puede tener a Claude trabajando en una característica en un worktree mientras corrige un error en otro, sin que ninguna sesión interfiera con la otra.

Use la bandera `--worktree` (`-w`) para crear un worktree aislado e iniciar Claude en él. El valor que pasa se convierte en el nombre del directorio worktree y el nombre de la rama:

```bash  theme={null}
# Inicie Claude en un worktree llamado "feature-auth"
# Crea .claude/worktrees/feature-auth/ con una nueva rama
claude --worktree feature-auth

# Inicie otra sesión en un worktree separado
claude --worktree bugfix-123
```

Si omite el nombre, Claude genera uno automáticamente:

```bash  theme={null}
# Auto-genera un nombre como "bright-running-fox"
claude --worktree
```

Los worktrees se crean en `<repo>/.claude/worktrees/<name>` y se ramifican desde la rama remota predeterminada. La rama worktree se nombra `worktree-<name>`.

También puede pedir a Claude que "trabaje en un worktree" o "inicie un worktree" durante una sesión, y lo creará automáticamente.

### Worktrees de subagentes

Los subagentes también pueden usar aislamiento de worktree para trabajar en paralelo sin conflictos. Pida a Claude que "use worktrees para sus agentes" o configúrelo en un [subagente personalizado](/es/sub-agents#supported-frontmatter-fields) agregando `isolation: worktree` al frontmatter del agente. Cada subagente obtiene su propio worktree que se limpia automáticamente cuando el subagente termina sin cambios.

### Limpieza de worktree

Cuando sale de una sesión de worktree, Claude maneja la limpieza según si realizó cambios:

* **Sin cambios**: el worktree y su rama se eliminan automáticamente
* **Cambios o commits existen**: Claude le solicita que mantenga o elimine el worktree. Mantener preserva el directorio y la rama para que pueda regresar más tarde. Eliminar elimina el directorio worktree y su rama, descartando todos los cambios sin confirmar y commits

Para limpiar worktrees fuera de una sesión de Claude, use [gestión manual de worktree](#manage-worktrees-manually).

<Tip>
  Agregue `.claude/worktrees/` a su `.gitignore` para evitar que el contenido del worktree aparezca como archivos sin seguimiento en su repositorio principal.
</Tip>

### Gestionar worktrees manualmente

Para más control sobre la ubicación del worktree y la configuración de la rama, cree worktrees con Git directamente. Esto es útil cuando necesita verificar una rama existente específica o colocar el worktree fuera del repositorio.

```bash  theme={null}
# Crear un worktree con una nueva rama
git worktree add ../project-feature-a -b feature-a

# Crear un worktree con una rama existente
git worktree add ../project-bugfix bugfix-123

# Inicie Claude en el worktree
cd ../project-feature-a && claude

# Limpiar cuando termine
git worktree list
git worktree remove ../project-feature-a
```

Obtenga más información en la [documentación oficial de Git worktree](https://git-scm.com/docs/git-worktree).

<Tip>
  Recuerde inicializar su entorno de desarrollo en cada nuevo worktree de acuerdo con la configuración de su proyecto. Dependiendo de su pila, esto podría incluir ejecutar instalación de dependencias (`npm install`, `yarn`), configurar entornos virtuales o seguir el proceso de configuración estándar de su proyecto.
</Tip>

### Control de versiones no git

El aislamiento de worktree funciona con git de forma predeterminada. Para otros sistemas de control de versiones como SVN, Perforce o Mercurial, configure [hooks WorktreeCreate y WorktreeRemove](/es/hooks#worktreecreate) para proporcionar lógica personalizada de creación y limpieza de worktree. Cuando se configura, estos hooks reemplazan el comportamiento predeterminado de git cuando usa `--worktree`.

Para la coordinación automatizada de sesiones paralelas con tareas compartidas y mensajería, consulte [equipos de agentes](/es/agent-teams).

***

## Reciba notificaciones cuando Claude necesite su atención

Cuando inicia una tarea de larga duración y cambia a otra ventana, puede configurar notificaciones de escritorio para saber cuándo Claude termina o necesita su entrada. Esto utiliza el evento de hook `Notification` [hook event](/es/hooks-guide#get-notified-when-claude-needs-input), que se activa cada vez que Claude está esperando permiso, inactivo y listo para una nueva indicación, o completando autenticación.

<Steps>
  <Step title="Abra el menú de hooks">
    Escriba `/hooks` y seleccione `Notification` de la lista de eventos.
  </Step>

  <Step title="Configure el matcher">
    Seleccione `+ Match all (no filter)` para activarse en todos los tipos de notificación. Para notificar solo para eventos específicos, seleccione `+ Add new matcher…` e ingrese uno de estos valores:

    | Matcher              | Se activa cuando                                    |
    | :------------------- | :-------------------------------------------------- |
    | `permission_prompt`  | Claude necesita que apruebe un uso de herramienta   |
    | `idle_prompt`        | Claude está hecho y esperando su próxima indicación |
    | `auth_success`       | La autenticación se completa                        |
    | `elicitation_dialog` | Claude le está haciendo una pregunta                |
  </Step>

  <Step title="Agregue su comando de notificación">
    Seleccione `+ Add new hook…` e ingrese el comando para su SO:

    <Tabs>
      <Tab title="macOS">
        Utiliza [`osascript`](https://ss64.com/mac/osascript.html) para activar una notificación nativa de macOS a través de AppleScript:

        ```
        osascript -e 'display notification "Claude Code needs your attention" with title "Claude Code"'
        ```
      </Tab>

      <Tab title="Linux">
        Utiliza `notify-send`, que viene preinstalado en la mayoría de escritorios Linux con un demonio de notificación:

        ```
        notify-send 'Claude Code' 'Claude Code needs your attention'
        ```
      </Tab>

      <Tab title="Windows (PowerShell)">
        Utiliza PowerShell para mostrar un cuadro de mensaje nativo a través de .NET Windows Forms:

        ```
        powershell.exe -Command "[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')"
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Guardar en configuración de usuario">
    Seleccione `User settings` para aplicar la notificación en todos sus proyectos.
  </Step>
</Steps>

Para el tutorial completo con ejemplos de configuración JSON, consulte [Automatizar flujos de trabajo con hooks](/es/hooks-guide#get-notified-when-claude-needs-input). Para el esquema de evento completo y tipos de notificación, consulte la [referencia de notificación](/es/hooks#notification).

***

## Usar Claude como una utilidad de estilo unix

### Agregue Claude a su proceso de verificación

Supongamos que desea usar Claude Code como un linter o revisor de código.

**Agregue Claude a su script de compilación:**

```json  theme={null}
// package.json
{
    ...
    "scripts": {
        ...
        "lint:claude": "claude -p 'you are a linter. please look at the changes vs. main and report any issues related to typos. report the filename and line number on one line, and a description of the issue on the second line. do not return any other text.'"
    }
}
```

<Tip>
  Consejos:

  * Utilice Claude para revisión de código automatizada en su canalización CI/CD
  * Personalice la indicación para verificar problemas específicos relevantes para su proyecto
  * Considere crear múltiples scripts para diferentes tipos de verificación
</Tip>

### Canalizar entrada, canalizar salida

Supongamos que desea canalizar datos a Claude y obtener datos en un formato estructurado.

**Canalizar datos a través de Claude:**

```bash  theme={null}
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

<Tip>
  Consejos:

  * Utilice tuberías para integrar Claude en scripts de shell existentes
  * Combine con otras herramientas Unix para flujos de trabajo poderosos
  * Considere usar --output-format para salida estructurada
</Tip>

### Controlar el formato de salida

Supongamos que necesita la salida de Claude en un formato específico, especialmente cuando integra Claude Code en scripts u otras herramientas.

<Steps>
  <Step title="Usar formato de texto (predeterminado)">
    ```bash  theme={null}
    cat data.txt | claude -p 'summarize this data' --output-format text > summary.txt
    ```

    Esto genera solo la respuesta de texto sin formato de Claude (comportamiento predeterminado).
  </Step>

  <Step title="Usar formato JSON">
    ```bash  theme={null}
    cat code.py | claude -p 'analyze this code for bugs' --output-format json > analysis.json
    ```

    Esto genera una matriz JSON de mensajes con metadatos incluyendo costo y duración.
  </Step>

  <Step title="Usar formato JSON de transmisión">
    ```bash  theme={null}
    cat log.txt | claude -p 'parse this log file for errors' --output-format stream-json
    ```

    Esto genera una serie de objetos JSON en tiempo real mientras Claude procesa la solicitud. Cada mensaje es un objeto JSON válido, pero la salida completa no es JSON válido si se concatena.
  </Step>
</Steps>

<Tip>
  Consejos:

  * Utilice `--output-format text` para integraciones simples donde solo necesita la respuesta de Claude
  * Utilice `--output-format json` cuando necesite el registro de conversación completo
  * Utilice `--output-format stream-json` para salida en tiempo real de cada turno de conversación
</Tip>

***

## Pregunte a Claude sobre sus capacidades

Claude tiene acceso integrado a su documentación y puede responder preguntas sobre sus propias características y limitaciones.

### Preguntas de ejemplo

```text  theme={null}
¿puede Claude Code crear solicitudes de extracción?
```

```text  theme={null}
¿cómo maneja Claude Code los permisos?
```

```text  theme={null}
¿qué skills están disponibles?
```

```text  theme={null}
¿cómo uso MCP con Claude Code?
```

```text  theme={null}
¿cómo configuro Claude Code para Amazon Bedrock?
```

```text  theme={null}
¿cuáles son las limitaciones de Claude Code?
```

<Note>
  Claude proporciona respuestas basadas en documentación a estas preguntas. Para ejemplos ejecutables y demostraciones prácticas, consulte las secciones de flujo de trabajo específicas anteriores.
</Note>

<Tip>
  Consejos:

  * Claude siempre tiene acceso a la documentación más reciente de Claude Code, independientemente de la versión que esté utilizando
  * Haga preguntas específicas para obtener respuestas detalladas
  * Claude puede explicar características complejas como integración MCP, configuraciones empresariales y flujos de trabajo avanzados
</Tip>

***

## Próximos pasos

<CardGroup cols={2}>
  <Card title="Mejores prácticas" icon="lightbulb" href="/es/best-practices">
    Patrones para obtener lo máximo de Claude Code
  </Card>

  <Card title="Cómo funciona Claude Code" icon="gear" href="/es/how-claude-code-works">
    Comprenda el bucle agente y la gestión de contexto
  </Card>

  <Card title="Extender Claude Code" icon="puzzle-piece" href="/es/features-overview">
    Agregue skills, hooks, MCP, subagentes y complementos
  </Card>

  <Card title="Implementación de referencia" icon="code" href="https://github.com/anthropics/claude-code/tree/main/.devcontainer">
    Clone nuestra implementación de referencia del contenedor de desarrollo
  </Card>
</CardGroup>
