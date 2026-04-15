> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Gestionar costos de manera efectiva

> Realice un seguimiento del uso de tokens, establezca límites de gasto del equipo y reduzca los costos de Claude Code con la gestión del contexto, la selección de modelos, la configuración del pensamiento extendido y los hooks de preprocesamiento.

Claude Code consume tokens en cada interacción. Los costos varían según el tamaño de la base de código, la complejidad de la consulta y la duración de la conversación. El costo promedio es de \$6 por desarrollador por día, con costos diarios que se mantienen por debajo de \$12 para el 90% de los usuarios.

Para el uso en equipo, Claude Code cobra por consumo de tokens de API. En promedio, Claude Code cuesta aproximadamente \$100-200 por desarrollador por mes con Sonnet 4.6, aunque hay una gran variación dependiendo de cuántas instancias ejecutan los usuarios y si la están utilizando en automatización.

Esta página cubre cómo [realizar un seguimiento de sus costos](#track-your-costs), [gestionar costos para equipos](#managing-costs-for-teams) y [reducir el uso de tokens](#reduce-token-usage).

## Realice un seguimiento de sus costos

### Uso del comando `/cost`

<Note>
  El comando `/cost` muestra el uso de tokens de API y está destinado a usuarios de API. Los suscriptores de Claude Max y Pro tienen el uso incluido en su suscripción, por lo que los datos de `/cost` no son relevantes para fines de facturación. Los suscriptores pueden usar `/stats` para ver patrones de uso.
</Note>

El comando `/cost` proporciona estadísticas detalladas de uso de tokens para su sesión actual:

```text theme={null}
Total cost:            $0.55
Total duration (API):  6m 19.7s
Total duration (wall): 6h 33m 10.2s
Total code changes:    0 lines added, 0 lines removed
```

## Gestión de costos para equipos

Cuando utiliza Claude API, puede [establecer límites de gasto del espacio de trabajo](https://platform.claude.com/docs/es/build-with-claude/workspaces#workspace-limits) en el gasto total del espacio de trabajo de Claude Code. Los administradores pueden [ver informes de costos y uso](https://platform.claude.com/docs/es/build-with-claude/workspaces#usage-and-cost-tracking) en la Consola.

<Note>
  Cuando autentica por primera vez Claude Code con su cuenta de Claude Console, se crea automáticamente un espacio de trabajo llamado "Claude Code" para usted. Este espacio de trabajo proporciona seguimiento y gestión centralizada de costos para todo el uso de Claude Code en su organización. No puede crear claves de API para este espacio de trabajo; es exclusivamente para autenticación y uso de Claude Code.
</Note>

En Bedrock, Vertex y Foundry, Claude Code no envía métricas desde su nube. Para obtener métricas de costos, varias grandes empresas informaron usar [LiteLLM](/es/llm-gateway#litellm-configuration), que es una herramienta de código abierto que ayuda a las empresas a [realizar un seguimiento del gasto por clave](https://docs.litellm.ai/docs/proxy/virtual_keys#tracking-spend). Este proyecto no está afiliado con Anthropic y no ha sido auditado por seguridad.

### Recomendaciones de límite de velocidad

Al configurar Claude Code para equipos, considere estas recomendaciones de Tokens Por Minuto (TPM) y Solicitudes Por Minuto (RPM) por usuario según el tamaño de su organización:

| Tamaño del equipo | TPM por usuario | RPM por usuario |
| ----------------- | --------------- | --------------- |
| 1-5 usuarios      | 200k-300k       | 5-7             |
| 5-20 usuarios     | 100k-150k       | 2.5-3.5         |
| 20-50 usuarios    | 50k-75k         | 1.25-1.75       |
| 50-100 usuarios   | 25k-35k         | 0.62-0.87       |
| 100-500 usuarios  | 15k-20k         | 0.37-0.47       |
| 500+ usuarios     | 10k-15k         | 0.25-0.35       |

Por ejemplo, si tiene 200 usuarios, podría solicitar 20k TPM para cada usuario, o 4 millones de TPM totales (200\*20,000 = 4 millones).

El TPM por usuario disminuye a medida que crece el tamaño del equipo porque menos usuarios tienden a usar Claude Code simultáneamente en organizaciones más grandes. Estos límites de velocidad se aplican a nivel de organización, no por usuario individual, lo que significa que los usuarios individuales pueden consumir temporalmente más que su parte calculada cuando otros no están usando activamente el servicio.

<Note>
  Si anticipa escenarios con uso concurrente inusualmente alto (como sesiones de capacitación en vivo con grupos grandes), es posible que necesite asignaciones de TPM más altas por usuario.
</Note>

### Costos de tokens del equipo de agentes

[Los equipos de agentes](/es/agent-teams) generan múltiples instancias de Claude Code, cada una con su propia ventana de contexto. El uso de tokens se escala con el número de compañeros de equipo activos y cuánto tiempo se ejecuta cada uno.

Para mantener los costos del equipo de agentes manejables:

* Use Sonnet para compañeros de equipo. Equilibra capacidad y costo para tareas de coordinación.
* Mantenga los equipos pequeños. Cada compañero de equipo ejecuta su propia ventana de contexto, por lo que el uso de tokens es aproximadamente proporcional al tamaño del equipo.
* Mantenga los prompts de generación enfocados. Los compañeros de equipo cargan CLAUDE.md, servidores MCP y skills automáticamente, pero todo en el prompt de generación se suma a su contexto desde el principio.
* Limpie los equipos cuando el trabajo esté hecho. Los compañeros de equipo activos continúan consumiendo tokens incluso si están inactivos.
* Los equipos de agentes están deshabilitados por defecto. Establezca `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` en su [settings.json](/es/settings) o entorno para habilitarlos. Consulte [habilitar equipos de agentes](/es/agent-teams#enable-agent-teams).

## Reducir el uso de tokens

Los costos de tokens se escalan con el tamaño del contexto: cuanto más contexto procesa Claude, más tokens utiliza. Claude Code optimiza automáticamente los costos a través del almacenamiento en caché de prompts (que reduce costos para contenido repetido como prompts del sistema) y auto-compactación (que resume el historial de conversación cuando se acerca a los límites del contexto).

Las siguientes estrategias lo ayudan a mantener el contexto pequeño y reducir los costos por mensaje.

### Gestione el contexto de manera proactiva

Use `/cost` para verificar su uso actual de tokens, o [configure su línea de estado](/es/statusline#context-window-usage) para mostrarla continuamente.

* **Limpie entre tareas**: Use `/clear` para comenzar de nuevo cuando cambie a trabajo no relacionado. El contexto obsoleto desperdicia tokens en cada mensaje posterior. Use `/rename` antes de limpiar para que pueda encontrar fácilmente la sesión más tarde, luego `/resume` para volver a ella.
* **Agregue instrucciones de compactación personalizadas**: `/compact Focus on code samples and API usage` le dice a Claude qué preservar durante la summarización.

También puede personalizar el comportamiento de compactación en su CLAUDE.md:

```markdown theme={null}
# Compact instructions

When you are using compact, please focus on test output and code changes
```

### Elija el modelo correcto

Sonnet maneja bien la mayoría de tareas de codificación y cuesta menos que Opus. Reserve Opus para decisiones arquitectónicas complejas o razonamiento de múltiples pasos. Use `/model` para cambiar modelos a mitad de sesión, o establezca un valor predeterminado en `/config`. Para tareas simples de subagent, especifique `model: haiku` en su [configuración de subagent](/es/sub-agents#choose-a-model).

### Reduzca la sobrecarga del servidor MCP

Cada servidor MCP agrega definiciones de herramientas a su contexto, incluso cuando está inactivo. Ejecute `/context` para ver qué está consumiendo espacio.

* **Prefiera herramientas CLI cuando estén disponibles**: Herramientas como `gh`, `aws`, `gcloud` y `sentry-cli` son más eficientes en contexto que los servidores MCP porque no agregan definiciones de herramientas persistentes. Claude puede ejecutar comandos CLI directamente sin la sobrecarga.
* **Deshabilite servidores no utilizados**: Ejecute `/mcp` para ver servidores configurados y deshabilite cualquiera que no esté usando activamente.
* **La búsqueda de herramientas es automática**: Cuando las descripciones de herramientas MCP exceden el 10% de su ventana de contexto, Claude Code automáticamente las difiere y carga herramientas bajo demanda a través de [búsqueda de herramientas](/es/mcp#scale-with-mcp-tool-search). Dado que las herramientas diferidas solo entran en contexto cuando se usan realmente, un umbral más bajo significa menos definiciones de herramientas inactivas consumiendo espacio. Establezca un umbral más bajo con `ENABLE_TOOL_SEARCH=auto:<N>` (por ejemplo, `auto:5` se activa cuando las herramientas exceden el 5% de su ventana de contexto).

### Instale plugins de inteligencia de código para lenguajes tipados

[Los plugins de inteligencia de código](/es/discover-plugins#code-intelligence) le dan a Claude navegación de símbolos precisa en lugar de búsqueda basada en texto, reduciendo lecturas de archivos innecesarias al explorar código desconocido. Una única llamada "ir a definición" reemplaza lo que de otro modo sería un grep seguido de lectura de múltiples archivos candidatos. Los servidores de lenguaje instalados también reportan errores de tipo automáticamente después de ediciones, por lo que Claude detecta errores sin ejecutar un compilador.

### Descargue el procesamiento en hooks y skills

Los [hooks](/es/hooks) personalizados pueden preprocesar datos antes de que Claude los vea. En lugar de que Claude lea un archivo de registro de 10,000 líneas para encontrar errores, un hook puede buscar `ERROR` y devolver solo las líneas coincidentes, reduciendo el contexto de decenas de miles de tokens a cientos.

Una [skill](/es/skills) puede darle a Claude conocimiento de dominio para que no tenga que explorar. Por ejemplo, una skill "codebase-overview" podría describir la arquitectura de su proyecto, directorios clave y convenciones de nomenclatura. Cuando Claude invoca la skill, obtiene este contexto inmediatamente en lugar de gastar tokens leyendo múltiples archivos para entender la estructura.

Por ejemplo, este hook PreToolUse filtra la salida de prueba para mostrar solo fallos:

<Tabs>
  <Tab title="settings.json">
    Agregue esto a su [settings.json](/es/settings#settings-files) para ejecutar el hook antes de cada comando Bash:

    ```json theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Bash",
            "hooks": [
              {
                "type": "command",
                "command": "~/.claude/hooks/filter-test-output.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="filter-test-output.sh">
    El hook llama a este script, que verifica si el comando es un ejecutor de pruebas y lo modifica para mostrar solo fallos:

    ```bash theme={null}
    #!/bin/bash
    input=$(cat)
    cmd=$(echo "$input" | jq -r '.tool_input.command')

    # If running tests, filter to show only failures
    if [[ "$cmd" =~ ^(npm test|pytest|go test) ]]; then
      filtered_cmd="$cmd 2>&1 | grep -A 5 -E '(FAIL|ERROR|error:)' | head -100"
      echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"updatedInput\":{\"command\":\"$filtered_cmd\"}}}"
    else
      echo "{}"
    fi
    ```
  </Tab>
</Tabs>

### Mueva instrucciones de CLAUDE.md a skills

Su archivo [CLAUDE.md](/es/memory) se carga en contexto al inicio de la sesión. Si contiene instrucciones detalladas para flujos de trabajo específicos (como revisiones de PR o migraciones de bases de datos), esos tokens están presentes incluso cuando está haciendo trabajo no relacionado. [Skills](/es/skills) se cargan bajo demanda solo cuando se invocan, por lo que mover instrucciones especializadas a skills mantiene su contexto base más pequeño. Apunte a mantener CLAUDE.md bajo aproximadamente \~500 líneas incluyendo solo lo esencial.

### Ajuste el pensamiento extendido

El pensamiento extendido está habilitado por defecto con un presupuesto de 31,999 tokens porque mejora significativamente el rendimiento en tareas complejas de planificación y razonamiento. Sin embargo, los tokens de pensamiento se facturan como tokens de salida, por lo que para tareas más simples donde el razonamiento profundo no es necesario, puede reducir costos bajando el [nivel de esfuerzo](/es/model-config#adjust-effort-level) con `/effort` o en `/model`, deshabilitando el pensamiento en `/config`, o bajando el presupuesto (por ejemplo, `MAX_THINKING_TOKENS=8000`).

### Delegue operaciones detalladas a subagents

Ejecutar pruebas, obtener documentación o procesar archivos de registro puede consumir contexto significativo. Delegue estos a [subagents](/es/sub-agents#isolate-high-volume-operations) para que la salida detallada permanezca en el contexto del subagent mientras solo un resumen regresa a su conversación principal.

### Gestione los costos del equipo de agentes

Los equipos de agentes usan aproximadamente 7 veces más tokens que sesiones estándar cuando los compañeros de equipo se ejecutan en plan mode, porque cada compañero de equipo mantiene su propia ventana de contexto y se ejecuta como una instancia separada de Claude. Mantenga las tareas del equipo pequeñas y autónomas para limitar el uso de tokens por compañero de equipo. Consulte [equipos de agentes](/es/agent-teams) para obtener detalles.

### Escriba prompts específicos

Solicitudes vagas como "mejorar esta base de código" desencadenan escaneo amplio. Solicitudes específicas como "agregar validación de entrada a la función de inicio de sesión en auth.ts" permiten que Claude trabaje eficientemente con lecturas de archivos mínimas.

### Trabaje eficientemente en tareas complejas

Para trabajo más largo o más complejo, estos hábitos ayudan a evitar tokens desperdiciados por tomar el camino equivocado:

* **Use plan mode para tareas complejas**: Presione Shift+Tab para entrar en [plan mode](/es/common-workflows#use-plan-mode-for-safe-code-analysis) antes de la implementación. Claude explora la base de código y propone un enfoque para su aprobación, previniendo re-trabajo costoso cuando la dirección inicial es incorrecta.
* **Corrija el curso temprano**: Si Claude comienza a ir en la dirección equivocada, presione Escape para detener inmediatamente. Use `/rewind` o presione Escape dos veces para restaurar la conversación y el código a un checkpoint anterior.
* **Proporcione objetivos de verificación**: Incluya casos de prueba, pegue capturas de pantalla o defina la salida esperada en su prompt. Cuando Claude puede verificar su propio trabajo, detecta problemas antes de que necesite solicitar correcciones.
* **Pruebe incrementalmente**: Escriba un archivo, pruébelo, luego continúe. Esto detecta problemas temprano cuando son baratos de arreglar.

## Uso de tokens en segundo plano

Claude Code usa tokens para algunas funcionalidades en segundo plano incluso cuando está inactivo:

* **Summarización de conversación**: Trabajos en segundo plano que resumen conversaciones anteriores para la característica `claude --resume`
* **Procesamiento de comandos**: Algunos comandos como `/cost` pueden generar solicitudes para verificar el estado

Estos procesos en segundo plano consumen una pequeña cantidad de tokens (típicamente menos de \$0.04 por sesión) incluso sin interacción activa.

## Comprensión de cambios en el comportamiento de Claude Code

Claude Code recibe actualizaciones regularmente que pueden cambiar cómo funcionan las características, incluido el reporte de costos. Ejecute `claude --version` para verificar su versión actual. Para preguntas específicas de facturación, contacte al soporte de Anthropic a través de su [cuenta de Consola](https://platform.claude.com/login). Para implementaciones de equipo, comience con un pequeño grupo piloto para establecer patrones de uso antes de un despliegue más amplio.
